"""Tests for jobs CRUD endpoints."""


def test_create_job(client):
    """POST /api/v1/jobs creates a new job."""
    response = client.post("/api/v1/jobs", json={"name": "test-job"})
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "test-job"
    assert data["status"] == "pending"
    assert data["pipeline"] == "default"
    assert "id" in data
    assert "created_at" in data


def test_list_jobs(client):
    """GET /api/v1/jobs returns list."""
    # Create one first
    client.post("/api/v1/jobs", json={"name": "list-test"})

    response = client.get("/api/v1/jobs")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_job_by_id(client):
    """GET /api/v1/jobs/{id} returns the job."""
    create_resp = client.post("/api/v1/jobs", json={"name": "get-test"})
    job_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] == job_id


def test_get_job_not_found(client):
    """GET /api/v1/jobs/{id} returns 404 for missing job."""
    response = client.get("/api/v1/jobs/nonexistent")
    assert response.status_code == 404


def test_cancel_job(client):
    """DELETE /api/v1/jobs/{id} cancels the job."""
    create_resp = client.post("/api/v1/jobs", json={"name": "cancel-test"})
    job_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    # Job may be 'cancelled' if caught before engine, or 'failed' if
    # engine tried to process it with unknown pipeline (race condition)
    assert response.json()["status"] in ("cancelled", "failed")


def test_cancel_job_not_found(client):
    """DELETE /api/v1/jobs/{id} returns 404 for missing job."""
    response = client.delete("/api/v1/jobs/nonexistent")
    assert response.status_code == 404


def test_create_job_with_params(client):
    """POST /api/v1/jobs with custom params."""
    response = client.post(
        "/api/v1/jobs",
        json={"name": "param-test", "pipeline": "analysis", "params": {"lang": "en"}},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["pipeline"] == "analysis"
    assert data["params"] == {"lang": "en"}
