from datetime import date, timedelta

import pytest


def _seed(client):
    client.post('/tasks', json={'title': 'Original', 'priority': 'low'})


def test_update_task_title_success(client):
    _seed(client)

    response = client.put('/tasks/1', json={'title': 'Updated'})

    assert response.status_code == 200
    assert response.json()['title'] == 'Updated'


def test_update_task_priority_success(client):
    _seed(client)

    response = client.put('/tasks/1', json={'priority': 'high'})

    assert response.status_code == 200
    assert response.json()['priority'] == 'high'


def test_update_task_description_trimmed(client):
    _seed(client)

    response = client.put('/tasks/1', json={'description': '  text  '})

    assert response.status_code == 200
    assert response.json()['description'] == 'text'


def test_update_task_due_date_success(client):
    _seed(client)
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    response = client.put('/tasks/1', json={'due_date': tomorrow})

    assert response.status_code == 200
    assert response.json()['due_date'] == tomorrow


def test_update_task_not_found(client):
    response = client.put('/tasks/99', json={'title': 'XXX'})

    assert response.status_code == 404


@pytest.mark.parametrize(
    'payload',
    [
        {'title': 'ab'},
        {'priority': 'critical'},
        {'description': 'x' * 501},
    ],
)
def test_update_task_invalid_payload(client, payload):
    _seed(client)

    response = client.put('/tasks/1', json=payload)

    assert response.status_code == 422


def test_update_task_reject_past_due_date(client):
    _seed(client)
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    response = client.put('/tasks/1', json={'due_date': yesterday})

    assert response.status_code == 400
