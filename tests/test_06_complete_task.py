def test_complete_task_success(client):
    client.post('/tasks', json={'title': 'Task'})

    response = client.patch('/tasks/1/complete')

    assert response.status_code == 200
    assert response.json()['completed'] is True


def test_complete_task_idempotent(client):
    client.post('/tasks', json={'title': 'Task'})
    client.patch('/tasks/1/complete')

    response = client.patch('/tasks/1/complete')

    assert response.status_code == 200
    assert response.json()['completed'] is True


def test_complete_task_not_found(client):
    response = client.patch('/tasks/55/complete')

    assert response.status_code == 404


def test_complete_task_appears_in_completed_filter(client):
    client.post('/tasks', json={'title': 'Task'})
    client.patch('/tasks/1/complete')

    response = client.get('/tasks?completed=true')

    assert response.status_code == 200
    assert len(response.json()) == 1
