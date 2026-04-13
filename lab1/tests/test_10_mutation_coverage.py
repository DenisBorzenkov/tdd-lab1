"""
Дополнительные тесты, добавленные по результатам мутационного тестирования.
Цель — убить мутантов, выживших при первом прогоне mutmut.
"""
from datetime import date, timedelta

import pytest


# ---------------------------------------------------------------------------
# Граничные значения длины title (max_length=100) — мутанты #8, #27
# ---------------------------------------------------------------------------

def test_create_title_exact_max_length(client):
    title = "a" * 100
    r = client.post("/tasks", json={"title": title})
    assert r.status_code == 201
    assert r.json()["title"] == title


def test_create_title_exceeds_max_length(client):
    title = "a" * 101
    r = client.post("/tasks", json={"title": title})
    assert r.status_code == 422


def test_update_title_exact_max_length(client):
    client.post("/tasks", json={"title": "Seed"})
    title = "b" * 100
    r = client.put("/tasks/1", json={"title": title})
    assert r.status_code == 200
    assert r.json()["title"] == title


def test_update_title_exceeds_max_length(client):
    client.post("/tasks", json={"title": "Seed"})
    title = "b" * 101
    r = client.put("/tasks/1", json={"title": title})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Нормализация title — trim (мутанты #14-16, #33-36)
# ---------------------------------------------------------------------------

def test_create_title_is_trimmed(client):
    r = client.post("/tasks", json={"title": "  Hello World  "})
    assert r.status_code == 201
    assert r.json()["title"] == "Hello World"


def test_create_whitespace_only_title_rejected(client):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422


def test_update_title_is_trimmed(client):
    client.post("/tasks", json={"title": "Seed"})
    r = client.put("/tasks/1", json={"title": "  Trimmed  "})
    assert r.status_code == 200
    assert r.json()["title"] == "Trimmed"


def test_update_whitespace_only_title_rejected(client):
    client.post("/tasks", json={"title": "Seed"})
    r = client.put("/tasks/1", json={"title": "   "})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Нормализация description — trim + empty→None (мутанты #20-25, #40, #42)
# ---------------------------------------------------------------------------

def test_create_description_whitespace_becomes_none(client):
    r = client.post("/tasks", json={"title": "Task", "description": "   "})
    assert r.status_code == 201
    assert r.json()["description"] is None


def test_create_description_trimmed(client):
    r = client.post("/tasks", json={"title": "Task", "description": "  hello  "})
    assert r.status_code == 201
    assert r.json()["description"] == "hello"


def test_create_description_none_stays_none(client):
    r = client.post("/tasks", json={"title": "Task", "description": None})
    assert r.status_code == 201
    assert r.json()["description"] is None


def test_update_description_whitespace_becomes_none(client):
    client.post("/tasks", json={"title": "Task"})
    r = client.put("/tasks/1", json={"description": "   "})
    assert r.status_code == 200
    assert r.json()["description"] is None


# ---------------------------------------------------------------------------
# Дефолтные значения Task (мутанты #46-49)
# ---------------------------------------------------------------------------

def test_created_task_defaults(client):
    r = client.post("/tasks", json={"title": "Defaults"})
    assert r.status_code == 201
    body = r.json()
    assert body["completed"] is False
    assert body["description"] is None
    assert body["due_date"] is None
    assert body["priority"] == "medium"


# ---------------------------------------------------------------------------
# Первая задача получает id=1 (мутанты #53, #54)
# ---------------------------------------------------------------------------

def test_first_task_has_id_one(client):
    r = client.post("/tasks", json={"title": "First"})
    assert r.json()["id"] == 1


# ---------------------------------------------------------------------------
# Поиск с одним символом (мутант #82)
# ---------------------------------------------------------------------------

def test_search_single_char(client):
    client.post("/tasks", json={"title": "XYZ"})
    client.post("/tasks", json={"title": "ABC"})
    r = client.get("/tasks?q=X")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "XYZ"


# ---------------------------------------------------------------------------
# Проверка detail-сообщений в ошибках (мутанты #73,99,104,114,121,129)
# ---------------------------------------------------------------------------

def test_create_duplicate_title_detail(client):
    client.post("/tasks", json={"title": "Unique"})
    r = client.post("/tasks", json={"title": "Unique"})
    assert r.status_code == 409
    assert r.json()["detail"] == "Task title already exists"


def test_get_not_found_detail(client):
    r = client.get("/tasks/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_update_not_found_detail(client):
    r = client.put("/tasks/999", json={"title": "XXX"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_update_duplicate_title_detail(client):
    client.post("/tasks", json={"title": "AAA"})
    client.post("/tasks", json={"title": "BBB"})
    r = client.put("/tasks/2", json={"title": "AAA"})
    assert r.status_code == 409
    assert r.json()["detail"] == "Task title already exists"


def test_complete_not_found_detail(client):
    r = client.patch("/tasks/999/complete")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_delete_not_found_detail(client):
    r = client.delete("/tasks/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


# ---------------------------------------------------------------------------
# Update сохраняется в хранилище (мутант #116)
# ---------------------------------------------------------------------------

def test_update_persists_in_storage(client):
    client.post("/tasks", json={"title": "Old"})
    client.put("/tasks/1", json={"title": "New"})

    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.json()["title"] == "New"


# ---------------------------------------------------------------------------
# _title_exists с exclude_id (мутанты #56, #59)
# ---------------------------------------------------------------------------

def test_update_same_title_on_same_task_ok(client):
    """Обновление задачи с тем же title не должно давать 409."""
    client.post("/tasks", json={"title": "Keep"})
    r = client.put("/tasks/1", json={"title": "Keep"})
    assert r.status_code == 200


def test_title_uniqueness_with_three_tasks(client):
    """Проверяем _title_exists при наличии нескольких задач."""
    client.post("/tasks", json={"title": "AAA"})
    client.post("/tasks", json={"title": "BBB"})
    client.post("/tasks", json={"title": "CCC"})
    # Обновление task 2 на title task 3 — должно быть 409
    r = client.put("/tasks/2", json={"title": "CCC"})
    assert r.status_code == 409


# ---------------------------------------------------------------------------
# Сообщение валидации title (мутанты #19, #39)
# ---------------------------------------------------------------------------

def test_create_empty_title_error_message(client):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422
    body = r.json()
    errors = body.get("detail", [])
    messages = [e.get("msg", "") for e in errors] if isinstance(errors, list) else [str(errors)]
    assert any("Title must not be empty" in m for m in messages)
    # Проверяем, что сообщение не содержит посторонних символов (мутант XX...XX)
    assert not any("XX" in m for m in messages)


def test_update_empty_title_error_message(client):
    client.post("/tasks", json={"title": "Seed"})
    r = client.put("/tasks/1", json={"title": "   "})
    assert r.status_code == 422
    body = r.json()
    errors = body.get("detail", [])
    messages = [e.get("msg", "") for e in errors] if isinstance(errors, list) else [str(errors)]
    assert any("Title must not be empty" in m for m in messages)
    assert not any("XX" in m for m in messages)
