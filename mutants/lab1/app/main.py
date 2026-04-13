from datetime import date
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


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
    args = [title, exclude_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__title_exists__mutmut_orig, x__title_exists__mutmut_mutants, args, kwargs, None)


def x__title_exists__mutmut_orig(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_1(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = None
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_2(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None or task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_3(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_4(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id != exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_5(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            break
        if task.title.casefold() == normalized:
            return True
    return False


def x__title_exists__mutmut_6(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() != normalized:
            return True
    return False


def x__title_exists__mutmut_7(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return False
    return False


def x__title_exists__mutmut_8(title: str, exclude_id: Optional[int] = None) -> bool:
    normalized = title.casefold()
    for task in _tasks.values():
        if exclude_id is not None and task.id == exclude_id:
            continue
        if task.title.casefold() == normalized:
            return True
    return True

x__title_exists__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__title_exists__mutmut_1': x__title_exists__mutmut_1, 
    'x__title_exists__mutmut_2': x__title_exists__mutmut_2, 
    'x__title_exists__mutmut_3': x__title_exists__mutmut_3, 
    'x__title_exists__mutmut_4': x__title_exists__mutmut_4, 
    'x__title_exists__mutmut_5': x__title_exists__mutmut_5, 
    'x__title_exists__mutmut_6': x__title_exists__mutmut_6, 
    'x__title_exists__mutmut_7': x__title_exists__mutmut_7, 
    'x__title_exists__mutmut_8': x__title_exists__mutmut_8
}
x__title_exists__mutmut_orig.__name__ = 'x__title_exists'


def _validate_due_date(value: Optional[date]) -> None:
    args = [value]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__validate_due_date__mutmut_orig, x__validate_due_date__mutmut_mutants, args, kwargs, None)


def x__validate_due_date__mutmut_orig(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_1(value: Optional[date]) -> None:
    if value is not None or value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_2(value: Optional[date]) -> None:
    if value is None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_3(value: Optional[date]) -> None:
    if value is not None and value <= date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_4(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=None,
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_5(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=None,
        )


def x__validate_due_date__mutmut_6(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            detail="due_date must be today or in the future",
        )


def x__validate_due_date__mutmut_7(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            )


def x__validate_due_date__mutmut_8(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="XXdue_date must be today or in the futureXX",
        )


def x__validate_due_date__mutmut_9(value: Optional[date]) -> None:
    if value is not None and value < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DUE_DATE MUST BE TODAY OR IN THE FUTURE",
        )

x__validate_due_date__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__validate_due_date__mutmut_1': x__validate_due_date__mutmut_1, 
    'x__validate_due_date__mutmut_2': x__validate_due_date__mutmut_2, 
    'x__validate_due_date__mutmut_3': x__validate_due_date__mutmut_3, 
    'x__validate_due_date__mutmut_4': x__validate_due_date__mutmut_4, 
    'x__validate_due_date__mutmut_5': x__validate_due_date__mutmut_5, 
    'x__validate_due_date__mutmut_6': x__validate_due_date__mutmut_6, 
    'x__validate_due_date__mutmut_7': x__validate_due_date__mutmut_7, 
    'x__validate_due_date__mutmut_8': x__validate_due_date__mutmut_8, 
    'x__validate_due_date__mutmut_9': x__validate_due_date__mutmut_9
}
x__validate_due_date__mutmut_orig.__name__ = 'x__validate_due_date'


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
