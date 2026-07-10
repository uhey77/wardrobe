from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_returns_backend_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Wardrobe API",
        "environment": "local",
        "chroma_url": "http://localhost:8001",
    }


def test_connectivity_returns_item_registration_endpoint() -> None:
    response = client.get("/api/connectivity")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Wardrobe backend is reachable.",
        "item_registration_endpoint": "/api/items",
    }
