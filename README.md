# tdd-lab1

Пример лабораторной работы по TDD на Python + FastAPI.

## Предметная область
Task Tracker API (управление задачами):
- создание задачи,
- просмотр списка и фильтрация,
- получение по id,
- обновление,
- завершение задачи,
- удаление.

## Запуск
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Запуск тестов
```bash
pytest -q
```

## Тест-кейсы
Полная таблица из 45 тест-кейсов и 9 тест-сюитов находится в `docs/test-cases.md`.

