"""Tests for health endpoint (TEST-API-001, TEST-API-003, TEST-INT-002)."""

from fastapi.testclient import TestClient

from glossa_lab import __version__
from glossa_lab.main import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    """TEST-API-001: Health endpoint returns valid status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "uptime_seconds" in data
    assert data["status"] in ("healthy", "degraded", "down")
    assert isinstance(data["uptime_seconds"], (int, float))


def test_health_version_matches_package():
    """TEST-INT-002: Version in health response matches pyproject.toml."""
    response = client.get("/api/v1/health")
    data = response.json()
    assert data["version"] == __version__


def test_versioned_routes_only():
    """TEST-API-003: Only /api/v1/ prefixed routes are accessible."""
    assert client.get("/api/v1/health").status_code == 200
    assert client.get("/health").status_code != 200
    assert client.get("/api/health").status_code != 200
