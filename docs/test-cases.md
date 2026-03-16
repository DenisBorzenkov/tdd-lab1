# Тест-кейсы и тест-сюиты

Система: **Task Tracker API** на `FastAPI`.

Количество:
- тест-сюиты: **9**
- тест-кейсы: **45**

| ID | Тест-сюит | Проверка | Предусловие | Шаги | Ожидаемый результат |
|---|---|---|---|---|---|
| TC-01 | S1 Health | `GET /health` доступен | Нет | Отправить `GET /health` | `200`, тело `{"status":"ok"}` |
| TC-02 | S1 Health | Content-Type для health | Нет | Отправить `GET /health` | `Content-Type: application/json` |
| TC-03 | S2 Create | Создание минимальной задачи | Нет | `POST /tasks` с `{"title":"Read docs"}` | `201`, задача создана |
| TC-04 | S2 Create | Создание с `priority=high` | Нет | `POST /tasks` с `title+priority` | `201`, `priority=high` |
| TC-05 | S2 Create | Нормализация description | Нет | `POST /tasks` с `description` c пробелами | `201`, description обрезан |
| TC-06 | S2 Create | Пустой title `""` | Нет | `POST /tasks` с пустым title | `422` |
| TC-07 | S2 Create | Title только пробелы | Нет | `POST /tasks` с `"  "` | `422` |
| TC-08 | S2 Create | Title слишком короткий | Нет | `POST /tasks` с `"ab"` | `422` |
| TC-09 | S2 Create | Отсутствует обязательный title | Нет | `POST /tasks` без title | `422` |
| TC-10 | S2 Create | Description > 500 | Нет | `POST /tasks` с длинным description | `422` |
| TC-11 | S2 Create | Невалидный priority | Нет | `POST /tasks` с `priority=urgent` | `422` |
| TC-12 | S2 Create | Due date в прошлом | Нет | `POST /tasks` с вчерашней датой | `400`, сообщение об ошибке |
| TC-13 | S3 List | Пустой список задач | Хранилище пустое | `GET /tasks` | `200`, `[]` |
| TC-14 | S3 List | Возврат всех задач по возрастанию id | Есть 2 задачи | `GET /tasks` | `200`, id `[1,2]` |
| TC-15 | S3 List | Фильтр `priority=low` | Есть задачи low/medium/high | `GET /tasks?priority=low` | `200`, только low |
| TC-16 | S3 List | Фильтр `priority=medium` | Есть задачи low/medium/high | `GET /tasks?priority=medium` | `200`, только medium |
| TC-17 | S3 List | Фильтр `priority=high` | Есть задачи low/medium/high | `GET /tasks?priority=high` | `200`, только high |
| TC-18 | S3 List | Фильтр completed=true | Есть 2 задачи, 1 завершена | `GET /tasks?completed=true` | `200`, только завершенная |
| TC-19 | S3 List | Поиск по title (`q`) | Есть задачи `Buy milk`, `Read book` | `GET /tasks?q=buy` | `200`, найден `Buy milk` |
| TC-20 | S4 GetById | Получение существующей задачи | Есть задача id=1 | `GET /tasks/1` | `200`, корректный объект |
| TC-21 | S4 GetById | Получение несуществующей задачи | Нет id=999 | `GET /tasks/999` | `404` |
| TC-22 | S4 GetById | Невалидный формат id | Нет | `GET /tasks/not-int` | `422` |
| TC-23 | S4 GetById | Полный набор полей в ответе | Есть задача | `GET /tasks/1` | Поля: id,title,description,priority,due_date,completed |
| TC-24 | S5 Update | Обновление title | Есть задача id=1 | `PUT /tasks/1` с новым title | `200`, title обновлен |
| TC-25 | S5 Update | Обновление priority | Есть задача id=1 | `PUT /tasks/1` с новым priority | `200`, priority обновлен |
| TC-26 | S5 Update | Нормализация description при update | Есть задача id=1 | `PUT /tasks/1` с `"  text  "` | `200`, `description="text"` |
| TC-27 | S5 Update | Обновление due_date на будущую | Есть задача id=1 | `PUT /tasks/1` с завтрашней датой | `200` |
| TC-28 | S5 Update | Обновление несуществующей задачи | Нет id=99 | `PUT /tasks/99` | `404` |
| TC-29 | S5 Update | Невалидный title при update | Есть задача id=1 | `PUT /tasks/1` с title `"ab"` | `422` |
| TC-30 | S5 Update | Невалидный priority при update | Есть задача id=1 | `PUT /tasks/1` с `priority=critical` | `422` |
| TC-31 | S5 Update | Description > 500 при update | Есть задача id=1 | `PUT /tasks/1` с длинным description | `422` |
| TC-32 | S5 Update | due_date в прошлом при update | Есть задача id=1 | `PUT /tasks/1` с вчерашней датой | `400` |
| TC-33 | S6 Complete | Завершение задачи | Есть задача id=1 | `PATCH /tasks/1/complete` | `200`, `completed=true` |
| TC-34 | S6 Complete | Идемпотентность завершения | Есть уже завершенная задача | Повторный `PATCH /tasks/1/complete` | `200`, состояние не ломается |
| TC-35 | S6 Complete | Завершение несуществующей | Нет id=55 | `PATCH /tasks/55/complete` | `404` |
| TC-36 | S6 Complete | Завершенная попадает в фильтр completed=true | Есть завершенная задача | `GET /tasks?completed=true` | `200`, задача присутствует |
| TC-37 | S7 Delete | Удаление существующей задачи | Есть задача id=1 | `DELETE /tasks/1` | `204` |
| TC-38 | S7 Delete | Удаление несуществующей | Нет id=404 | `DELETE /tasks/404` | `404` |
| TC-39 | S7 Delete | Удаленная задача недоступна | Была задача id=1, затем удалена | `GET /tasks/1` | `404` |
| TC-40 | S7 Delete | Удаление уменьшает размер списка | Есть 2 задачи | Удалить одну, затем `GET /tasks` | `200`, остается 1 |
| TC-41 | S8 Business | Уникальность title (create), case-insensitive | Есть `Daily report` | `POST /tasks` с `DAILY REPORT` | `409` |
| TC-42 | S8 Business | Уникальность title (update), case-insensitive | Есть `Task A` и `Task B` | `PUT /tasks/2` с `task a` | `409` |
| TC-43 | S8 Business | Разрешена дата дедлайна = сегодня | Нет | `POST /tasks` с `due_date=today` | `201` |
| TC-44 | S8 Business | Сброс due_date в `null` при update | Есть задача с due_date | `PUT /tasks/1` с `{"due_date": null}` | `200`, `due_date=null` |
| TC-45 | S9 Protocol | Некорректный JSON в `POST /tasks` | Нет | Отправить сломанный JSON | `422` |
| TC-46 | S9 Protocol | Неверный HTTP-метод для health | Нет | `POST /health` | `405` |
| TC-47 | S9 Protocol | Неизвестный маршрут | Нет | `GET /missing-route` | `404` |

## Трассировка на автотесты

Тест-кейсы реализованы автотестами в файлах:
- `tests/test_01_health.py`
- `tests/test_02_create_task.py`
- `tests/test_03_list_tasks.py`
- `tests/test_04_get_task.py`
- `tests/test_05_update_task.py`
- `tests/test_06_complete_task.py`
- `tests/test_07_delete_task.py`
- `tests/test_08_business_rules.py`
- `tests/test_09_protocol_errors.py`
