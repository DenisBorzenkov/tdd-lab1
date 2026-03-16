def test_get_task_by_valid_id(client):
    client.post('/tasks', json={'title': 'One'})

    response = client.get('/tasks/1')

    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_get_task_not_found(client):
    response = client.get('/tasks/999')

    assert response.status_code == 404


def test_get_task_invalid_id_type(client):
    response = client.get('/tasks/not-int')

    assert response.status_code == 422


def test_get_task_contains_all_fields(client):
    client.post('/tasks', json={'title': 'Task', 'priority': 'high'})

    response = client.get('/tasks/1')

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {'id', 'title', 'description', 'priority', 'due_date', 'completed'}
