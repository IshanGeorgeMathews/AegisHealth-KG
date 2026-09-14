"""Tests for the /health endpoint and basic API bootstrap."""

from fastapi.testclient import TestClient

from aegis.api.main import app

client = TestClient(app)


def test_health_returns_200():
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_body():
    """GET /health should return {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_openapi_docs_accessible():
    """The auto-generated OpenAPI schema should be reachable."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "AegisHealth-KG API"
    assert schema["info"]["version"] == "0.1.0"
