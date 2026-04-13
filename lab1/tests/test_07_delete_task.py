def test_delete_task_success(client):
    client.post('/tasks', json={'title': 'Task'})

    response = client.delete('/tasks/1')

    assert response.status_code == 204


def test_delete_task_not_found(client):
    response = client.delete('/tasks/404')

    assert response.status_code == 404


def test_deleted_task_is_unavailable(client):
    client.post('/tasks', json={'title': 'Task'})
    client.delete('/tasks/1')

    response = client.get('/tasks/1')

    assert response.status_code == 404


def test_delete_reduces_list_count(client):
    client.post('/tasks', json={'title': 'AAA'})
    client.post('/tasks', json={'title': 'BBB'})

    client.delete('/tasks/1')
    response = client.get('/tasks')

    assert response.status_code == 200
    assert len(response.json()) == 1
