from datetime import date
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, field_validator


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Priority = Priority.medium
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("Title must not be empty")
        return title

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        description = value.strip()
        return description or None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[Priority] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        title = value.strip()
        if not title:
            raise ValueError("Title must not be empty")
        return title

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        description = value.strip()
        return description or None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority
    due_date: Optional[date] = None
    completed: bool = False


app = FastAPI(title="Task Tracker API")
_tasks: dict[int, Task] = {}
_next_id = 1


def _title_exists(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def _validate_due_date(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date must be today or in the future",
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    global _next_id

    _validate_due_date(payload.due_date)
    if _title_exists(payload.title):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Task title already exists")

    task = Task(id=_next_id, completed=False, **payload.model_dump())
    _tasks[task.id] = task
    _next_id += 1
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    completed: Optional[bool] = Query(default=None),
    priority: Optional[Priority] = Query(default=None),
    q: Optional[str] = Query(default=None, min_length=1),
) -> list[Task]:
    items = list(_tasks.values())

    if completed is not None:
        items = [item for item in items if item.completed == completed]

    if priority is not None:
        items = [item for item in items if item.priority == priority]

    if q is not None:
        needle = q.casefold()
        items = [item for item in items if needle in item.title.casefold()]

    return sorted(items, key=lambda task: task.id)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    if "due_date" in updates:
        _validate_due_date(updates["due_date"])

    if "title" in updates and _title_exists(updates["title"], exclude_id=task_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Task title already exists")

    updated = task.model_copy(update=updates)
    _tasks[task_id] = updated
    return updated


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def mark_complete(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if task.completed:
        return task

    updated = task.model_copy(update={"completed": True})
    _tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if task_id not in _tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    del _tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
