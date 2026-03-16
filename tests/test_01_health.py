def test_health_returns_ok(client):
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_health_content_type_json(client):
    response = client.get('/health')

    assert response.headers['content-type'].startswith('application/json')
