from datetime import date, timedelta

import pytest


@pytest.mark.parametrize(
    'payload',
    [
        {'title': 'Read docs'},
        {'title': 'Plan sprint', 'priority': 'high'},
        {'title': 'Write notes', 'description': '  clean text  '},
    ],
)
def test_create_task_success_variants(client, payload):
    response = client.post('/tasks', json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body['title'] == payload['title'].strip()


@pytest.mark.parametrize(
    'payload, expected_status',
    [
        ({'title': ''}, 422),
        ({'title': '  '}, 422),
        ({'title': 'ab'}, 422),
        ({'description': 'missing title'}, 422),
    ],
)
def test_create_task_invalid_title_cases(client, payload, expected_status):
    response = client.post('/tasks', json=payload)

    assert response.status_code == expected_status


def test_create_task_rejects_description_too_long(client):
    payload = {'title': 'Valid title', 'description': 'x' * 501}

    response = client.post('/tasks', json=payload)

    assert response.status_code == 422


def test_create_task_rejects_invalid_priority(client):
    response = client.post('/tasks', json={'title': 'Task', 'priority': 'urgent'})

    assert response.status_code == 422


def test_create_task_rejects_past_due_date(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    response = client.post('/tasks', json={'title': 'Task', 'due_date': yesterday})

    assert response.status_code == 400
    assert response.json()['detail'] == 'due_date must be today or in the future'
