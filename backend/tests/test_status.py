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


def test_status_carries_service_identity(client):
    """Spec 081 FR-007: status carries identity, not liveness alone.

    The identity block lives on /status because /health's key set is
    pinned minimal by TEST-SEC-002.
    """
    response = client.get("/api/v1/status")
    data = response.json()
    assert data["app"] == "Glossa Lab"
    assert isinstance(data["host"], str) and data["host"]
    assert "started_at" in data
    assert "data_dir" in data
    assert "db_ready" in data


def test_status_jobs_counts_structure(client):
    """Job counts include expected keys."""
    response = client.get("/api/v1/status")
    data = response.json()
    jobs = data["jobs"]
    for key in ("total", "pending", "running", "completed", "failed", "cancelled"):
        assert key in jobs
        assert isinstance(jobs[key], int)


def test_status_reports_live_pipeline_count(client):
    """Status should expose the live registered pipeline list and counts."""
    response = client.get("/api/v1/status")
    data = response.json()

    assert data["pipeline_count"] == len(data["pipelines"])
    assert data["pipeline_count"] >= 17
    assert "catalog_counts" in data
    assert data["catalog_counts"]["pipelines"] == data["pipeline_count"]
