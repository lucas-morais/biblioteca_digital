import pytest
from fastapi.testclient import TestClient

from biblioteca_digital.app import app


@pytest.fixture
def client():
    return TestClient(app)
