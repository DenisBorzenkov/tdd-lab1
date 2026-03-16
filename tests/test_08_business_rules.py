from datetime import date, timedelta


def test_create_task_unique_title_case_insensitive(client):
    client.post('/tasks', json={'title': 'Daily report'})

    response = client.post('/tasks', json={'title': 'DAILY REPORT'})

    assert response.status_code == 409


def test_update_task_unique_title_case_insensitive(client):
    client.post('/tasks', json={'title': 'Task A'})
    client.post('/tasks', json={'title': 'Task B'})

    response = client.put('/tasks/2', json={'title': 'task a'})

    assert response.status_code == 409


def test_create_accepts_today_due_date(client):
    today = date.today().isoformat()

    response = client.post('/tasks', json={'title': 'Today task', 'due_date': today})

    assert response.status_code == 201
    assert response.json()['due_date'] == today


def test_update_accepts_none_due_date(client):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.post('/tasks', json={'title': 'Task', 'due_date': tomorrow})

    response = client.put('/tasks/1', json={'due_date': None})

    assert response.status_code == 200
    assert response.json()['due_date'] is None
