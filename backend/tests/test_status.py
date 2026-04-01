"""Tests for status endpoint (TEST-API-002)."""

from glossa_lab import __version__


def test_status_endpoint_returns_200(client):
    """TEST-API-002: Status endpoint returns system status."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ("healthy", "degraded", "down")
    assert data["version"] == __version__
    assert "uptime_seconds" in data
    assert "jobs" in data
    assert "pipelines" in data


def test_status_jobs_counts_structure(client):
    """Job counts include expected keys."""
    response = client.get("/api/v1/status")
    data = response.json()
    jobs = data["jobs"]
    for key in ("total", "pending", "running", "completed", "failed", "cancelled"):
        assert key in jobs
        assert isinstance(jobs[key], int)
