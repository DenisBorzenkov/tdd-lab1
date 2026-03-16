import pytest
from fastapi.testclient import TestClient

from app.main import _tasks, app
import app.main as main_module


@pytest.fixture
def client() -> TestClient:
    _tasks.clear()
    main_module._next_id = 1
    return TestClient(app)
