from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_drivers():
    response = client.get("/drivers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_summaries():
    response = client.get("/summaries/2026-08-01")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_exceptions():
    response = client.get("/exceptions/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)