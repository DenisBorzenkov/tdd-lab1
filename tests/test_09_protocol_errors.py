def test_post_tasks_with_invalid_json(client):
    response = client.post('/tasks', data='{"title":', headers={'Content-Type': 'application/json'})

    assert response.status_code == 422


def test_method_not_allowed_for_health_post(client):
    response = client.post('/health')

    assert response.status_code == 405


def test_unknown_route_returns_404(client):
    response = client.get('/missing-route')

    assert response.status_code == 404
