"""Spec-study register API (Leg B hardening, 2026-10-29).

Pins: the register enumerates the real specs/ tree; known verdict
headlines surface verbatim from their outcome records; duplicate spec
numbers are reported as ambiguous, never silently picked; the
restricted spec's directory contents are never read.
"""
from __future__ import annotations

from pathlib import Path

from glossa_lab.api import spec_studies


def test_register_enumerates_real_specs(client):
    r = client.get("/api/v1/spec-studies")
    assert r.status_code == 200
    body = r.json()
    ids = [s["spec_id"] for s in body["studies"]]
    # The register on main carries Specs 001-081 (with duplicate numbers
    # 021/025/026 and no 049): at least 80 entries, 001 and 081 present.
    assert body["total"] >= 80
    assert "001" in ids and "081" in ids and "052" in ids
    assert body["with_outcome"] >= 30


def test_known_verdict_headline_surfaces(client):
    r = client.get("/api/v1/spec-studies/052")
    assert r.status_code == 200
    body = r.json()
    assert body["has_outcome"] is True
    assert "INCONSISTENT" in (body["outcome_headline"] or "")


def test_duplicate_number_is_ambiguous_not_picked(client):
    r = client.get("/api/v1/spec-studies/026")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ambiguous") is True
    assert len(body["matches"]) >= 2


def test_unknown_spec_404(client):
    r = client.get("/api/v1/spec-studies/999")
    assert r.status_code == 404


def test_restricted_spec_contents_never_read(client, tmp_path, monkeypatch):
    # Build a synthetic register with a restricted directory whose
    # files would change the entry if read; assert they are not.
    specs = tmp_path / "specs"
    restricted = specs / "072-synthetic-restricted"
    restricted.mkdir(parents=True)
    (restricted / "spec.md").write_text("# SECRET TITLE\n", encoding="utf-8")
    (restricted / "outcome.md").write_text("> SECRET VERDICT\n", encoding="utf-8")
    normal = specs / "001-synthetic-normal"
    normal.mkdir()
    (normal / "spec.md").write_text("# Spec 001 — Synthetic\n", encoding="utf-8")
    (normal / "outcome.md").write_text(
        "# Spec 001 — Outcome record (EXECUTED — SYNTHETIC VERDICT)\n\n"
        "> ## EXECUTED — 2026-01-01 — SYNTHETIC VERDICT\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(spec_studies, "RESTRICTED_SPEC_IDS", frozenset({"072"}))
    entries = spec_studies.list_spec_studies(Path(specs))
    by_id = {e["spec_id"]: e for e in entries}
    assert by_id["072"]["restricted"] is True
    assert by_id["072"]["title"] is None
    assert by_id["072"]["outcome_headline"] is None
    assert by_id["001"]["title"] == "Spec 001 — Synthetic"
    assert "SYNTHETIC VERDICT" in (by_id["001"]["outcome_headline"] or "")


def test_real_register_restricted_entry_is_directory_name_only(client):
    r = client.get("/api/v1/spec-studies/072")
    assert r.status_code == 200
    body = r.json()
    entry = body["matches"][0] if body.get("ambiguous") else body
    assert entry["restricted"] is True
    assert entry["title"] is None
    assert entry["outcome_headline"] is None
