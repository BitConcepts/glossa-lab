"""Tests for the world language corpus catalogue API (H16 Phase 3)."""

import pytest


# ── Seeder ─────────────────────────────────────────────────────────────────────

def test_corpus_catalogue_seeded(client):
    """GET /corpus-catalogue returns at least 30 entries after seeding."""
    resp = client.get("/api/v1/corpus-catalogue")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) >= 30, f"Expected >= 30 catalogue entries, got {len(entries)}"


def test_catalogue_has_undeciphered_entries(client):
    """Catalogue includes undeciphered scripts."""
    resp = client.get("/api/v1/corpus-catalogue?undeciphered=true")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) >= 5
    ids = [e["id"] for e in entries]
    assert "cat-indus" in ids
    assert "cat-linear-a" in ids


def test_catalogue_has_deciphered_entries(client):
    """Catalogue includes deciphered ancient and modern scripts."""
    resp = client.get("/api/v1/corpus-catalogue?undeciphered=false")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) >= 10
    ids = [e["id"] for e in entries]
    assert "cat-old-hebrew" in ids
    assert "cat-geez" in ids


def test_catalogue_filter_by_script_type(client):
    """Filter by script_type returns matching subset."""
    resp = client.get("/api/v1/corpus-catalogue?script_type=abjad")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) >= 2
    for e in entries:
        assert e["script_type"] == "abjad"


def test_catalogue_already_imported_flag(client):
    """already_imported flag is present in every entry."""
    resp = client.get("/api/v1/corpus-catalogue")
    entries = resp.json()
    for e in entries:
        assert "already_imported" in e
        assert isinstance(e["already_imported"], bool)


def test_catalogue_entries_have_required_fields(client):
    """All entries have id, name, language, script_type, period, source_url."""
    resp = client.get("/api/v1/corpus-catalogue")
    for e in resp.json():
        for field in ("id", "name", "language", "language_family", "script_type",
                      "period", "source_url", "description"):
            assert field in e, f"Entry {e.get('id')} missing field '{field}'"


# ── Import ─────────────────────────────────────────────────────────────────────

def test_import_nonexistent_entry(client):
    """Importing a nonexistent catalogue ID returns 404."""
    resp = client.post("/api/v1/corpus-catalogue/nonexistent/import")
    assert resp.status_code == 404


def test_import_entry_without_local_module(client):
    """Entries without local_module (e.g. Linear A) return 501."""
    resp = client.post("/api/v1/corpus-catalogue/cat-linear-a/import")
    assert resp.status_code == 501
    assert "local module" in resp.json()["detail"].lower() or "source url" in resp.json()["detail"].lower()


def test_import_bundled_entry(client):
    """Importing an entry with a local_module creates a corpus text."""
    # proto_sinaitic has local_module='proto_sinaitic'
    resp = client.post("/api/v1/corpus-catalogue/cat-proto-sinaitic/import")
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert "name" in data
    if data.get("imported"):
        assert "corpus_id" in data
        assert data["tokens"] > 0
    else:
        assert data.get("reason") == "already_exists"


def test_import_creates_text_visible_in_corpora(client):
    """After import, the corpus appears in GET /texts."""
    # Use geez which has a local_module
    client.post("/api/v1/corpus-catalogue/cat-geez/import")  # may already exist
    resp = client.get("/api/v1/texts")
    assert resp.status_code == 200
    names = [t["name"] for t in resp.json()]
    # Either already existed or just created — either way should be there
    assert any("Ge" in n or "geez" in n.lower() or "Genesis" in n for n in names)
