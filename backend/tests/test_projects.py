"""Tests for the Projects API — CRUD, prompt_context (goals) roundtrip, activation."""

import pytest


@pytest.fixture(scope="module")
def _client(client):
    """Module-scoped alias so tests share the same client/DB."""
    return client


def test_list_projects(_client):
    """GET /api/v1/projects returns a list (may be seeded)."""
    r = _client.get("/api/v1/projects")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)


def test_create_project_with_goals(_client):
    """PUT /api/v1/projects/{id} creates a project with prompt_context (goals)."""
    r = _client.put("/api/v1/projects/test_goals_proj", json={
        "label": "Test Goals Project",
        "description": "Unit test project",
        "prompt_context": "Decipher script X using method Y.",
        "topic_ids": ["topic_a", "topic_b"],
        "experiment_ids": [],
        "corpus_ids": [],
        "is_active": False,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "test_goals_proj"
    assert body["label"] == "Test Goals Project"
    assert body["prompt_context"] == "Decipher script X using method Y."
    assert body["topic_ids"] == ["topic_a", "topic_b"]


def test_get_project_returns_goals(_client):
    """GET /api/v1/projects/{id} roundtrips prompt_context."""
    r = _client.get("/api/v1/projects/test_goals_proj")
    assert r.status_code == 200
    body = r.json()
    assert body["prompt_context"] == "Decipher script X using method Y."


def test_update_goals(_client):
    """PUT updates prompt_context (project goals) in-place."""
    r = _client.put("/api/v1/projects/test_goals_proj", json={
        "label": "Test Goals Project",
        "prompt_context": "Updated: decipher script Z.",
        "is_active": False,
    })
    assert r.status_code == 200
    assert r.json()["prompt_context"] == "Updated: decipher script Z."


def test_activate_project(_client):
    """POST /api/v1/projects/{id}/activate sets is_active."""
    r = _client.post("/api/v1/projects/test_goals_proj/activate")
    assert r.status_code == 200
    body = r.json()
    assert body["is_active"] in (1, True)


def test_active_project_endpoint(_client):
    """GET /api/v1/projects/active returns the activated project."""
    r = _client.get("/api/v1/projects/active")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "test_goals_proj"
    assert body["prompt_context"] == "Updated: decipher script Z."


def test_dashboard_highlights_has_n_hypotheses(_client):
    """GET /api/v1/dashboard/highlights includes n_hypotheses."""
    r = _client.get("/api/v1/dashboard/highlights?days=14&limit=5")
    assert r.status_code == 200
    body = r.json()
    assert "n_hypotheses" in body
    assert isinstance(body["n_hypotheses"], int)
    assert "n_experiments" in body


def test_delete_project(_client):
    """DELETE /api/v1/projects/{id} removes the project."""
    r = _client.delete("/api/v1/projects/test_goals_proj")
    assert r.status_code == 200
    assert r.json()["deleted"] is True
    # Confirm gone
    r2 = _client.get("/api/v1/projects/test_goals_proj")
    assert r2.status_code == 404
