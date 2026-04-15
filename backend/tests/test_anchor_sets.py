"""Tests for user-definable anchor sets API (H16 Phase 4)."""

import pytest


def _create_set(client, **overrides):
    body = {"name": "Test Anchors", "language": "ugaritic", "pairs": [], **overrides}
    resp = client.post("/api/v1/anchor-sets", json=body)
    assert resp.status_code == 201
    return resp.json()


# ── list ───────────────────────────────────────────────────────────────────────

def test_list_anchor_sets_empty(client):
    resp = client.get("/api/v1/anchor-sets")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── create ─────────────────────────────────────────────────────────────────────

def test_create_anchor_set_minimal(client):
    resp = client.post("/api/v1/anchor-sets", json={"name": "Minimal Set"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Minimal Set"
    assert data["pairs"] == []
    assert "id" in data


def test_create_anchor_set_with_pairs(client):
    pairs = [
        {"cipher": "004", "target": "T", "confidence": "high", "note": "Fuls verified"},
        {"cipher": "066", "target": "m", "confidence": "high", "note": "Fuls verified"},
    ]
    a = _create_set(client, name="Fuls 6", pairs=pairs)
    assert len(a["pairs"]) == 2
    assert a["pairs"][0]["cipher"] == "004"
    assert a["pairs"][0]["target"] == "T"


def test_create_anchor_set_appears_in_list(client):
    a = _create_set(client, name="Listed")
    ids = [e["id"] for e in client.get("/api/v1/anchor-sets").json()]
    assert a["id"] in ids


def test_filter_by_corpus_id(client):
    """GET /anchor-sets?corpus_id=X returns only that corpus's sets."""
    _create_set(client, name="Set A", corpus_id="corpus-abc")
    _create_set(client, name="Set B", corpus_id="corpus-xyz")
    resp = client.get("/api/v1/anchor-sets?corpus_id=corpus-abc")
    assert resp.status_code == 200
    names = [e["name"] for e in resp.json()]
    assert "Set A" in names
    assert "Set B" not in names


# ── get ────────────────────────────────────────────────────────────────────────

def test_get_anchor_set_by_id(client):
    a = _create_set(client, name="Get By ID")
    resp = client.get(f"/api/v1/anchor-sets/{a['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == a["id"]


def test_get_anchor_set_not_found(client):
    resp = client.get("/api/v1/anchor-sets/nonexistent")
    assert resp.status_code == 404


# ── update ─────────────────────────────────────────────────────────────────────

def test_update_anchor_set_name(client):
    a = _create_set(client, name="Old")
    resp = client.put(f"/api/v1/anchor-sets/{a['id']}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"


def test_update_anchor_set_pairs(client):
    a = _create_set(client, name="Add Pairs")
    pairs = [{"cipher": "X", "target": "y", "confidence": "low", "note": ""}]
    resp = client.put(f"/api/v1/anchor-sets/{a['id']}", json={"pairs": pairs})
    assert resp.status_code == 200
    assert len(resp.json()["pairs"]) == 1


def test_update_anchor_set_not_found(client):
    resp = client.put("/api/v1/anchor-sets/nonexistent", json={"name": "X"})
    assert resp.status_code == 404


# ── delete ─────────────────────────────────────────────────────────────────────

def test_delete_anchor_set(client):
    a = _create_set(client, name="Delete Me")
    resp = client.delete(f"/api/v1/anchor-sets/{a['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/v1/anchor-sets/{a['id']}").status_code == 404


def test_delete_anchor_set_not_found(client):
    resp = client.delete("/api/v1/anchor-sets/nonexistent")
    assert resp.status_code == 404
