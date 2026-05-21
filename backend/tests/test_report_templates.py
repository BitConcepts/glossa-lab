"""Tests for user-definable report templates API (H16 Phase 2)."""



# ── helpers ────────────────────────────────────────────────────────────────────

def _create_template(client, **overrides):
    body = {"name": "Test Template", "description": "A test", "category": "Test", **overrides}
    resp = client.post("/api/v1/report-templates", json=body)
    assert resp.status_code == 201
    return resp.json()


# ── list ───────────────────────────────────────────────────────────────────────

def test_list_templates_empty(client):
    """GET /report-templates returns a list (may be empty on fresh DB)."""
    resp = client.get("/api/v1/report-templates")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── create ─────────────────────────────────────────────────────────────────────

def test_create_template_minimal(client):
    """POST /report-templates with name only succeeds (status 201)."""
    resp = client.post("/api/v1/report-templates", json={"name": "Minimal"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Minimal"
    assert data["sections"] == []
    assert "id" in data


def test_create_template_with_sections(client):
    """POST /report-templates accepts sections list."""
    sections = [{"title": "Results", "data_source": "exp1", "data_key": "accuracy",
                 "chart_type": "bar", "include_table": True, "description": ""}]
    t = _create_template(client, name="With Sections", sections=sections)
    assert len(t["sections"]) == 1
    assert t["sections"][0]["title"] == "Results"


def test_create_template_appears_in_list(client):
    """Created template appears in GET list."""
    t = _create_template(client, name="Listed Template")
    ids = [e["id"] for e in client.get("/api/v1/report-templates").json()]
    assert t["id"] in ids


# ── get ────────────────────────────────────────────────────────────────────────

def test_get_template_by_id(client):
    t = _create_template(client, name="Get By ID")
    resp = client.get(f"/api/v1/report-templates/{t['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == t["id"]


def test_get_template_not_found(client):
    resp = client.get("/api/v1/report-templates/nonexistent")
    assert resp.status_code == 404


# ── update ─────────────────────────────────────────────────────────────────────

def test_update_template_name(client):
    t = _create_template(client, name="Old Name")
    resp = client.put(f"/api/v1/report-templates/{t['id']}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


def test_update_template_sections(client):
    t = _create_template(client, name="Update Sections")
    sections = [{"title": "S1", "data_source": "", "data_key": "", "chart_type": "table",
                 "include_table": True, "description": ""}]
    resp = client.put(f"/api/v1/report-templates/{t['id']}", json={"sections": sections})
    assert resp.status_code == 200
    assert len(resp.json()["sections"]) == 1


def test_update_template_not_found(client):
    resp = client.put("/api/v1/report-templates/nonexistent", json={"name": "X"})
    assert resp.status_code == 404


# ── delete ─────────────────────────────────────────────────────────────────────

def test_delete_template(client):
    t = _create_template(client, name="Delete Me")
    resp = client.delete(f"/api/v1/report-templates/{t['id']}")
    assert resp.status_code == 200
    # Confirm gone
    assert client.get(f"/api/v1/report-templates/{t['id']}").status_code == 404


def test_delete_template_not_found(client):
    resp = client.delete("/api/v1/report-templates/nonexistent")
    assert resp.status_code == 404
