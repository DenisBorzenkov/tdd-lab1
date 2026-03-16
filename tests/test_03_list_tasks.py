import pytest


def _create(client, title, priority='medium'):
    return client.post('/tasks', json={'title': title, 'priority': priority})


def test_list_tasks_empty(client):
    response = client.get('/tasks')

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_all_sorted_by_id(client):
    _create(client, 'First')
    _create(client, 'Second')

    response = client.get('/tasks')

    assert [task['id'] for task in response.json()] == [1, 2]


@pytest.mark.parametrize(
    'priority, expected_count',
    [
        ('low', 1),
        ('medium', 1),
        ('high', 1),
    ],
)
def test_list_tasks_filter_by_priority(client, priority, expected_count):
    _create(client, 'Low task', 'low')
    _create(client, 'Medium task', 'medium')
    _create(client, 'High task', 'high')

    response = client.get(f'/tasks?priority={priority}')

    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_list_tasks_filter_by_completed_true(client):
    _create(client, 'Task A')
    _create(client, 'Task B')
    client.patch('/tasks/2/complete')

    response = client.get('/tasks?completed=true')

    assert response.status_code == 200
    assert [task['id'] for task in response.json()] == [2]


def test_list_tasks_filter_by_search_query(client):
    _create(client, 'Buy milk')
    _create(client, 'Read book')

    response = client.get('/tasks?q=buy')

    assert response.status_code == 200
    assert [task['title'] for task in response.json()] == ['Buy milk']
