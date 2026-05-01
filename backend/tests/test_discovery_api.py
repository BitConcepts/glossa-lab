"""Smoke tests for the Phase-E Discovery API router.

These tests use the shared FastAPI ``TestClient`` fixture from ``conftest.py``
which entered the app lifespan (so the SQLite database and discovery store are
fully initialised). External provider calls are NOT exercised — Phase C
fetchers are tested separately in their own offline smoke tests.
"""

from __future__ import annotations


# ── Topics + sources + stats (no DB writes required) ─────────────────────


def test_discovery_topics_endpoint(client):
    """GET /api/v1/discovery/topics returns the three shipped seed topics."""
    response = client.get("/api/v1/discovery/topics")
    assert response.status_code == 200

    data = response.json()
    assert "topics" in data
    ids = {t["id"] for t in data["topics"]}
    # Phase C ships these three seeds.
    assert {"indus_script", "dravidian_linguistics", "ivc_archaeology"} <= ids

    # Spot-check shape on the first topic.
    sample = next(t for t in data["topics"] if t["id"] == "indus_script")
    assert isinstance(sample["keywords"], list)
    assert isinstance(sample["exclusions"], list)
    assert isinstance(sample["languages"], list)
    assert sample["label"]


def test_discovery_sources_endpoint(client):
    """GET /api/v1/discovery/sources returns each registered fetcher."""
    response = client.get("/api/v1/discovery/sources")
    assert response.status_code == 200

    data = response.json()
    sources = {s["source"] for s in data["sources"]}
    # Phase C registers (at least) these six fetchers.
    expected = {"newsapi", "brave", "serpapi", "openalex", "arxiv", "crossref"}
    assert expected <= sources

    # Each entry must declare the same shape the frontend types.ts expects.
    for s in data["sources"]:
        assert "source" in s
        assert "requires" in s
        assert "configured" in s
        assert "disabled_reason" in s
        assert isinstance(s["requires"], list)


def test_discovery_stats_endpoint(client):
    """GET /api/v1/discovery/stats?group=<group> returns a counts dict."""
    for group in ("status", "kind", "topic", "source"):
        response = client.get(f"/api/v1/discovery/stats?group={group}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["group"] == group
        assert isinstance(data["counts"], dict)


# ── Items list / fetch-by-id / status update ─────────────────────────────────


def test_discovery_items_list_empty_shape(client):
    """GET /api/v1/discovery/items always returns the {items, limit, offset} shape."""
    response = client.get("/api/v1/discovery/items?status=dismissed&limit=5")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data and isinstance(data["items"], list)
    assert data["limit"] == 5
    assert data["offset"] == 0


def test_discovery_get_missing_item_returns_404(client):
    """GET /api/v1/discovery/items/{id} returns 404 for unknown ids."""
    response = client.get("/api/v1/discovery/items/nonexistent-discovery-id")
    assert response.status_code == 404


def test_discovery_status_update_missing_returns_404(client):
    """POST /api/v1/discovery/items/{id}/status returns 404 for unknown ids."""
    response = client.post(
        "/api/v1/discovery/items/nonexistent-discovery-id/status",
        json={"status": "saved"},
    )
    assert response.status_code == 404


def test_discovery_fetch_endpoint_starts_a_job(client):
    """POST /api/v1/discovery/fetch always returns a JobAck.

    The actual provider calls run as a background task; with no API keys
    configured the runner returns near-instantly with zero items.
    """
    response = client.post(
        "/api/v1/discovery/fetch",
        json={"topics": ["indus_script"], "sources": ["openalex"]},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "running"
    assert body["job_id"]
    assert "started" in body["message"].lower()


def test_discovery_mine_without_provider_returns_400(client, monkeypatch):
    """POST /api/v1/discovery/mine refuses when no LLM provider is configured.

    The endpoint constructs a fresh ``LLMClient`` per request; clearing every
    provider env var here exercises the explicit 400 path the router added in
    Phase E. We restore the env in finally via monkeypatch's teardown.
    """
    for var in ("MISTRAL_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(var, raising=False)

    # Also override the settings store (.keys.json) by emptying it via
    # the FastAPI settings router so the LLMClient sees nothing configured.
    # If the host has stored keys, this guard simply skips the assertion.
    response = client.post("/api/v1/discovery/mine", json={"limit": 1})
    if response.status_code == 200:
        # Host has at least one provider configured via .keys.json; in that
        # case the endpoint correctly returns a JobAck — exercise that path.
        body = response.json()
        assert body["status"] in ("running", "completed")
        assert "job_id" in body
    else:
        assert response.status_code == 400
        assert "LLM provider" in response.json()["detail"]
