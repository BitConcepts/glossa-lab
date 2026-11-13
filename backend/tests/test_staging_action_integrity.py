"""Staging-action integrity regression tests (2026-11-13
acceptance-path probes (g) and (h), defects 5 and 6).

- Defect 5 — rejection was erasable: reject -> action "staged"
  wiped rejected_at / rejected_reason, after which approve
  succeeded with no trace of the rejection. Rejection history
  must be append-only on the record: re-staging or approving a
  candidate never erases a prior rejection (timestamp + reason).
- Defect 6 — no state guard on approval: approving an
  already-approved candidate returned ok:true a second time.
  Approve is valid only from the states the pipeline stages
  candidates in ("staged" / "blocked"); from any other state it
  is refused and changes nothing.
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
    staging.write_text("[]", encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(rl, "_STAGING_JSON", staging)
    monkeypatch.setattr(rl, "_ARCHIVE_JSON", archive)
    return {"staging": staging, "archive": archive}


@pytest.fixture()
def client():
    return TestClient(create_app())


def _candidate(**over):
    c = {"sign": "M777", "proposed_reading": "test",
         "review_status": "staged", "evidence_score": 0.9,
         "evidence_type": "positional_profile",
         "source_experiment": "unit-test"}
    c.update(over)
    return c


def _seed(staging_env, *candidates):
    staging_env["staging"].write_text(
        json.dumps(list(candidates)), encoding="utf-8")


def _record(staging_env, sign="M777"):
    records = json.loads(staging_env["staging"].read_text(encoding="utf-8"))
    for c in records:
        if c.get("sign") == sign:
            return c
    raise AssertionError(f"candidate {sign} missing from staging file")


def _action(client, action, **over):
    body = {"sign": "M777", "proposed_reading": "test", "action": action}
    body.update(over)
    return client.post(f"{BASE}/staging/action", json=body)


# --- Defect 5: rejection history is append-only --------------------

def test_restage_after_reject_preserves_rejection(client, staging_env):
    _seed(staging_env, _candidate())
    r = _action(client, "reject", reason="probe: should stay on record")
    assert r.json()["ok"] is True
    rejected = _record(staging_env)
    assert rejected["review_status"] == "rejected"
    rejected_at = rejected["rejected_at"]

    r = _action(client, "staged")
    assert r.json()["ok"] is True
    restaged = _record(staging_env)
    assert restaged["review_status"] == "staged"
    # The rejection survives the re-stage as permanent history.
    history = restaged.get("rejection_history")
    assert history == [{"rejected_at": rejected_at,
                        "rejected_reason": "probe: should stay on record"}]

    # Approving afterwards does not erase the trace either.
    r = _action(client, "approve")
    assert r.json()["ok"] is True
    approved = _record(staging_env)
    assert approved["review_status"] == "approved"
    assert approved.get("rejection_history") == history


def test_rejection_history_accumulates_across_cycles(client, staging_env):
    _seed(staging_env, _candidate())
    for reason in ("first rejection", "second rejection"):
        r = _action(client, "reject", reason=reason)
        assert r.json()["ok"] is True
        r = _action(client, "staged")
        assert r.json()["ok"] is True
    history = _record(staging_env).get("rejection_history")
    assert [h["rejected_reason"] for h in history] == [
        "first rejection", "second rejection"]


def test_restage_preserves_legacy_scalar_only_rejection(
        client, staging_env):
    """A record rejected before rejection_history existed carries
    only the scalar fields; re-staging must not lose them."""
    _seed(staging_env, _candidate(
        review_status="rejected",
        rejected_at="2026-01-01T00:00:00Z",
        rejected_reason="legacy rejection"))
    r = _action(client, "staged")
    assert r.json()["ok"] is True
    history = _record(staging_env).get("rejection_history")
    assert history == [{"rejected_at": "2026-01-01T00:00:00Z",
                        "rejected_reason": "legacy rejection"}]


# --- Defect 6: approve is state-guarded ----------------------------

def test_double_approve_is_refused_and_changes_nothing(
        client, staging_env):
    _seed(staging_env, _candidate())
    r = _action(client, "approve")
    assert r.json()["ok"] is True
    before = staging_env["staging"].read_text(encoding="utf-8")

    r = _action(client, "approve")
    data = r.json()
    assert data["ok"] is False
    assert "error" in data
    # Nothing changed: file byte-identical, still approved once.
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "approved"


def test_approve_rejected_candidate_is_refused(client, staging_env):
    _seed(staging_env, _candidate(
        review_status="rejected",
        rejected_at="2026-01-01T00:00:00Z",
        rejected_reason="not accepted"))
    before = staging_env["staging"].read_text(encoding="utf-8")
    r = _action(client, "approve")
    assert r.json()["ok"] is False
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "rejected"


def test_approve_verified_candidate_is_refused(client, staging_env):
    _seed(staging_env, _candidate(review_status="verified"))
    before = staging_env["staging"].read_text(encoding="utf-8")
    r = _action(client, "approve")
    assert r.json()["ok"] is False
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "verified"


def test_approve_from_blocked_is_allowed(client, staging_env):
    """The pipeline stages conflicted candidates as "blocked"
    (pipelines/research_loop.py); approve must remain valid
    from that state."""
    _seed(staging_env, _candidate(review_status="blocked"))
    r = _action(client, "approve")
    assert r.json()["ok"] is True
    record = _record(staging_env)
    assert record["review_status"] == "approved"
    assert record["approved_at"]
