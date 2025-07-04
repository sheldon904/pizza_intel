# pizza_tracker/tests/test_main.py

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

def test_get_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": "nominal"}

def test_get_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
