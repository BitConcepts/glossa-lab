"""Phase-109 (spec 007 Step 4) regression tests: the promotion
evidence gate (governance H26) and the verify-sa rename.

- Promotion WITHOUT a recorded non-SA evidence reference must
  fail: nothing is promoted, nothing is written, and the blocked
  candidates are reported in `blocked_no_evidence`.
- Promotion WITH a reference (candidate field or request map)
  succeeds and records the reference in the promoted entry.
- POST /staging/verify-archive is the canonical route; the old
  /staging/verify-sa path remains only as a deprecated alias.
"""
from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from glossa_lab.api import research_loop as rl
from glossa_lab.main import create_app

BASE = "/api/v1/research-loop"


@pytest.fixture()
def staging_env(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    archive = tmp_path / "anchor_staging_archive.json"
    anchors = tmp_path / "INDUS_FINAL_ANCHORS.json"
    staging.write_text("[]", encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    anchors.write_text(json.dumps({
        "total": 1, "corpus_token_coverage": 0.5,
        "anchors": {"M001": {"reading": "a", "confidence": "HIGH",
                             "basis": "b", "source": "s"}},
    }), encoding="utf-8")
    monkeypatch.setattr(rl, "_STAGING_JSON", staging)
    monkeypatch.setattr(rl, "_ARCHIVE_JSON", archive)
    monkeypatch.setattr(rl, "_FA_PATH", anchors)
    return {"staging": staging, "archive": archive, "anchors": anchors}


@pytest.fixture()
def client():
    return TestClient(create_app())


def _candidate(**over):
    c = {"sign": "M777", "proposed_reading": "test",
         "review_status": "verified", "evidence_score": 0.9,
         "evidence_type": "positional_profile",
         "source_experiment": "unit-test"}
    c.update(over)
    return c


def test_promotion_without_evidence_ref_is_blocked(client, staging_env):
    staging_env["archive"].write_text(
        json.dumps([_candidate()]), encoding="utf-8")
    before = staging_env["anchors"].read_text(encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json={})
    assert r.status_code == 200
    data = r.json()
    assert data["promoted"] == 0
    assert data["blocked_no_evidence"] == ["M777"]
    assert data["sa_validation_jobs"] == []
    # Nothing written: anchors file byte-identical, sign absent.
    assert staging_env["anchors"].read_text(encoding="utf-8") == before
    assert "M777" not in json.loads(before)["anchors"]


def test_promotion_with_candidate_evidence_ref_succeeds(client, staging_env):
    staging_env["archive"].write_text(json.dumps([_candidate(
        evidence_ref="reports/phase999_example.json (positional "
                     "adjudication)")]), encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json={})
    data = r.json()
    assert data["promoted"] == 1
    assert data["blocked_no_evidence"] == []
    anchors = json.loads(
        staging_env["anchors"].read_text(encoding="utf-8"))["anchors"]
    assert anchors["M777"]["reading"] == "test"
    assert "evidence_ref=reports/phase999_example.json" in \
        anchors["M777"]["basis"]


def test_promotion_with_request_evidence_ref_map_succeeds(
        client, staging_env):
    staging_env["archive"].write_text(
        json.dumps([_candidate()]), encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json={
        "evidence_refs": {"M777": "glossa-indus/LEDGER.md Phase-X entry"}})
    data = r.json()
    assert data["promoted"] == 1
    assert data["blocked_no_evidence"] == []


def test_verify_archive_route_and_deprecated_alias(client, staging_env):
    candidate = {"sign": "M555", "proposed_reading": "x",
                 "review_status": "approved"}
    staging_env["staging"].write_text(
        json.dumps([candidate]), encoding="utf-8")
    r = client.post(f"{BASE}/staging/verify-archive")
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert r.json()["archived"] == 1
    # Deprecated alias still responds (committed frontend build).
    staging_env["staging"].write_text(
        json.dumps([candidate]), encoding="utf-8")
    r2 = client.post(f"{BASE}/staging/verify-sa")
    assert r2.status_code == 200
    assert r2.json()["ok"] is True
