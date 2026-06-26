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


def test_phase0_returns_fixed_connectivity_message() -> None:
    response = client.get("/api/phase0")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Wardrobe backend is reachable.",
        "next_phase": "Phase 1: item upload pipeline",
    }
