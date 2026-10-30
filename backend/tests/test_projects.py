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


def test_project_question_roundtrip(_client):
    """Spec 081: a program's question is stored and returned verbatim."""
    r = _client.put("/api/v1/projects/test_question_proj", json={
        "label": "Question Program",
        "question": "What do the signs mean — tested claim by claim?",
        "is_active": False,
    })
    assert r.status_code == 200
    assert r.json()["question"] == "What do the signs mean — tested claim by claim?"
    r = _client.get("/api/v1/projects/test_question_proj")
    assert r.status_code == 200
    assert r.json()["question"] == "What do the signs mean — tested claim by claim?"


def test_project_question_defaults_empty(_client):
    """Spec 081: legacy projects without a question read back ''."""
    r = _client.put("/api/v1/projects/test_noquestion_proj", json={
        "label": "No Question Program",
        "is_active": False,
    })
    assert r.status_code == 200
    assert r.json().get("question", "") == ""


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


def test_project_standing_position_roundtrip(_client):
    """Spec 081 Amendment 2: a program's standing position is stored on
    its record and returned verbatim (it is program data, rendered on
    the program home — never a shell constant)."""
    position = "The script is not deciphered. Readings are candidate claims."
    r = _client.put("/api/v1/projects/test_position_proj", json={
        "label": "Position Program",
        "standing_position": position,
        "is_active": False,
    })
    assert r.status_code == 200
    assert r.json()["standing_position"] == position
    r = _client.get("/api/v1/projects/test_position_proj")
    assert r.status_code == 200
    assert r.json()["standing_position"] == position


def test_project_standing_position_defaults_empty(_client):
    """Spec 081 Amendment 2: a program that states no position reads ''."""
    r = _client.put("/api/v1/projects/test_noposition_proj", json={
        "label": "No Position Program",
        "is_active": False,
    })
    assert r.status_code == 200
    assert r.json().get("standing_position", "") == ""


def test_scoped_claims_match_shim_for_store_program(_client):
    """Spec 081 step 3 (T015): the program-scoped claims register serves
    the store program's register identically to the /indus-evidence shim."""
    scoped = _client.get("/api/v1/programs/indus_decipherment/claims?limit=5")
    shim = _client.get("/api/v1/indus-evidence/claims?limit=5")
    assert scoped.status_code == 200
    assert shim.status_code == 200
    assert scoped.json()["total"] == shim.json()["total"]
    assert scoped.json()["total"] > 0


def test_scoped_library_and_hypotheses_for_store_program(_client):
    """Spec 081 step 3: scoped library + hypotheses answer for the store
    program with the same shapes as the shim endpoints."""
    lib = _client.get("/api/v1/programs/indus_decipherment/library?limit=1")
    assert lib.status_code == 200
    assert lib.json()["total"] > 0
    hyp = _client.get("/api/v1/programs/indus_decipherment/hypotheses")
    assert hyp.status_code == 200
    assert isinstance(hyp.json()["models"], list)


def test_scoped_routes_unknown_program_404(_client):
    """Spec 081 step 3: an unknown program id 404s on the scoped surface."""
    r = _client.get("/api/v1/programs/no_such_program_xyz/claims")
    assert r.status_code == 404


def test_scoped_routes_empty_for_other_program(_client):
    """Spec 081 step 3: an existing non-store program gets its own honest
    empty register — never the store program's data under its name."""
    r = _client.put("/api/v1/projects/test_empty_scope_proj", json={
        "label": "Empty Scope Program",
        "is_active": False,
    })
    assert r.status_code == 200
    claims = _client.get("/api/v1/programs/test_empty_scope_proj/claims")
    assert claims.status_code == 200
    assert claims.json() == {"claims": [], "total": 0, "limit": 200, "offset": 0}
    lib = _client.get("/api/v1/programs/test_empty_scope_proj/library")
    assert lib.status_code == 200
    assert lib.json()["total"] == 0
    hyp = _client.get("/api/v1/programs/test_empty_scope_proj/hypotheses")
    assert hyp.status_code == 200
    assert hyp.json() == {"models": []}
    scores = _client.get("/api/v1/programs/test_empty_scope_proj/claims/aee-scores")
    assert scores.status_code == 200
    assert scores.json()["total_claims"] == 0
    trail = _client.get(
        "/api/v1/programs/test_empty_scope_proj/claims/any_claim/trail")
    assert trail.status_code == 404
