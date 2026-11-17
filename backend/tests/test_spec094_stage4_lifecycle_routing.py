"""Spec 094 Stage 4 regression tests: lifecycle routing (T401 /
C094-10) and atomic stores (T402 / C094-11).

- T401: every anchor-path status transition is effected through
  the single gated transition service
  (glossa_lab.anchor_transition), carrying transition_stage's
  guarantees — one-step moves on the anchor lifecycle, actor
  validation with the automated ceiling, an append-only evidence
  trail (review_history). The stage-vocabulary mapping is pinned
  here as data. The removal of direct review_status writes outside
  the service is proven by a code census over the package sources,
  not by reading the diff.
- T402: the three anchor-path stores are written only through the
  verified write path (glossa_lab.verified_write, Spec 092 Stage
  2's library). A simulated write failure leaves each store
  byte-identical under the named error (VerifiedWriteError).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from glossa_lab import anchor_transition as at
from glossa_lab.api import research_loop as rl
from glossa_lab.main import create_app
from glossa_lab.verified_write import VerifiedWriteError

BASE = "/api/v1/research-loop"

_FALSIFIER = "the reading fails if the positional profile does not replicate"


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
def promote_env(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    archive = tmp_path / "anchor_staging_archive.json"
    anchors = tmp_path / "INDUS_FINAL_ANCHORS.json"
    snapshot = tmp_path / "indus_research.jsonl"
    staging.write_text("[]", encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    anchors.write_text(json.dumps({
        "total": 1, "corpus_token_coverage": 0.5,
        "anchors": {"M001": {"reading": "a", "confidence": "HIGH",
                             "basis": "b", "source": "s"}},
    }), encoding="utf-8")
    snapshot.write_text(
        json.dumps({"canonical_grapheme_ids": ["777", "001"]}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(rl, "_STAGING_JSON", staging)
    monkeypatch.setattr(rl, "_ARCHIVE_JSON", archive)
    monkeypatch.setattr(rl, "_FA_PATH", anchors)
    monkeypatch.setattr(rl, "_CORPUS_SNAPSHOT", snapshot, raising=False)
    monkeypatch.setattr(rl, "_CORPUS_GRAPHEMES", None, raising=False)
    return {"staging": staging, "archive": archive, "anchors": anchors}


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


def _gated(**over):
    """A candidate carrying the full conforming gate record
    (Stages 1-3: falsifier + listed approver, pinned evidence of a
    registered class, recorded per-candidate verification)."""
    base = {"falsifier": _FALSIFIER, "approver": "Tristen Pierson",
            "evidence_ref": "LEDGER.md",
            "evidence_sha256": hashlib.sha256(
                (rl._REPO / "LEDGER.md").read_bytes()).hexdigest(),
            "evidence_class": "external_corpus_record",
            "verification_evaluator": "Tristen Pierson",
            "verification_evaluated_at": "2026-11-16T00:00:00Z",
            "verification_evaluation": "evaluated this candidate's positional profile against the cited corpus record",
            "verification_evidence_ref": "LEDGER.md",
            "verification_outcome": "verified"}
    base.update(over)
    return _candidate(**base)


def _seed(env, *candidates):
    env["staging"].write_text(
        json.dumps(list(candidates)), encoding="utf-8")


def _records(path):
    return json.loads(path.read_text(encoding="utf-8"))


# --- The stage-vocabulary mapping, pinned as data ----------------------

def test_stage_vocabulary_mapping():
    assert at.ANCHOR_STAGE_MAP == {
        "staged": "created",
        "blocked": "created",
        "approved": "checked",
        "verified": "explained",
        "promoted": "accepted",
        "rejected": "created",
        "expired": "created",
    }
    # Every anchor status is mapped, and no anchor status maps to
    # 'digested': digestion is a claim-axis act the anchor path
    # never performs (promotion is acceptance, not digestion).
    assert set(at.ANCHOR_STAGE_MAP) == set(at.ANCHOR_STATUSES)
    assert "digested" not in at.ANCHOR_STAGE_MAP.values()


# --- Service units: the spine and the trail ----------------------------

def test_forward_spine_one_step_each_with_trail():
    rec = _candidate()
    entry = at.transition_anchor_status(
        rec, "approved", actor="Tristen Pierson",
        evidence_refs=["LEDGER.md"], timestamp="2026-11-16T00:00:00Z")
    assert rec["review_status"] == "approved"
    assert entry["from_status"] == "staged"
    assert entry["to_status"] == "approved"
    assert (entry["from_stage"], entry["to_stage"]) == ("created", "checked")
    assert entry["actor"] == "Tristen Pierson"
    assert entry["evidence_refs"] == ["LEDGER.md"]
    assert rec["review_history"] == [entry]

    entry = at.transition_anchor_status(
        rec, "verified", actor="Tristen Pierson",
        evidence_refs=["LEDGER.md"], timestamp="2026-11-16T01:00:00Z")
    assert (entry["from_stage"], entry["to_stage"]) == ("checked", "explained")
    entry = at.transition_anchor_status(
        rec, "promoted", actor="Tristen Pierson",
        evidence_refs=["LEDGER.md"], timestamp="2026-11-16T02:00:00Z")
    assert (entry["from_stage"], entry["to_stage"]) == ("explained", "accepted")
    assert [e["to_status"] for e in rec["review_history"]] == [
        "approved", "verified", "promoted"]


def test_transitions_outside_the_table_do_not_exist():
    rec = _candidate()
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "verified", actor="Tristen Pierson",
            evidence_refs=["LEDGER.md"])  # staged → verified skips a step
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "promoted", actor="Tristen Pierson",
            evidence_refs=["LEDGER.md"])  # staged → promoted skips the spine
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "staged", actor="Tristen Pierson")  # no-op
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "bogus", actor="Tristen Pierson")  # unknown status
    assert rec["review_status"] == "staged"
    assert "review_history" not in rec  # refusals append nothing

    promoted = _candidate(review_status="promoted")
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            promoted, "rejected", actor="Tristen Pierson",
            reason="too late")  # promoted is terminal


def test_automated_ceiling():
    # The lifecycle's own move is admitted for an automated actor:
    # expiry sits at 'created' rank on both sides of the mapping.
    rec = _candidate(review_status="rejected")
    at.transition_anchor_status(
        rec, "expired", actor="research_loop", reason="expired_after_7d")
    assert rec["review_status"] == "expired"

    # Above 'checked', an automated actor fails closed — on either
    # side of the move.
    rec = _candidate(review_status="approved")
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "verified", actor="research_loop",
            evidence_refs=["LEDGER.md"])
    rec = _candidate(review_status="verified")
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "rejected", actor="research_loop", reason="operator error")
    assert rec["review_status"] == "verified"
    assert "review_history" not in rec


def test_demotion_and_terminal_moves_require_reason():
    rec = _candidate(review_status="approved")
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(rec, "staged", actor="staging_action")
    at.transition_anchor_status(
        rec, "staged", actor="staging_action",
        reason="re-staged by operator (staging_action)")
    assert rec["review_status"] == "staged"

    rec = _candidate()
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(rec, "rejected", actor="staging_action")
    at.transition_anchor_status(
        rec, "rejected", actor="staging_action", reason="user rejected")
    assert rec["review_status"] == "rejected"


def test_advance_above_checked_requires_evidence_trail():
    rec = _candidate(review_status="approved")
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "verified", actor="Tristen Pierson")  # no evidence refs
    assert rec["review_status"] == "approved"
    at.transition_anchor_status(
        rec, "verified", actor="Tristen Pierson",
        evidence_refs=["LEDGER.md"])
    assert rec["review_status"] == "verified"


def test_refusal_changes_nothing():
    rec = _gated(review_status="approved")
    before = copy.deepcopy(rec)
    with pytest.raises(at.AnchorTransitionError):
        at.transition_anchor_status(
            rec, "verified", actor="research_loop",
            evidence_refs=["LEDGER.md"])
    assert rec == before


def test_archive_stamp_rules():
    rec = _candidate(review_status="verified")
    with pytest.raises(at.AnchorTransitionError):
        at.stamp_archive_fields(
            rec, actor="research_loop", reason="cleanup_action")
    entry = at.stamp_archive_fields(
        rec, actor="Tristen Pierson", reason="cleanup_action",
        timestamp="2026-11-16T03:00:00Z")
    assert rec["archived_at"] == "2026-11-16T03:00:00Z"
    assert rec["archived_reason"] == "cleanup_action"
    assert entry["from_status"] == entry["to_status"] == "verified"
    # A record still in the review queue is not archivable.
    with pytest.raises(at.AnchorTransitionError):
        at.archive_anchor_record(
            _candidate(), actor="staging_archive", reason="manual_archive")


# --- Route level: the trail lands on the records ------------------------

def test_approve_route_effects_transition_through_service(client, staging_env):
    _seed(staging_env, _gated())
    data = client.post(f"{BASE}/staging/action", json={
        "sign": "M777", "proposed_reading": "test",
        "action": "approve"}).json()
    assert data["ok"] is True
    record = _records(staging_env["staging"])[0]
    assert record["review_status"] == "approved"
    (entry,) = record["review_history"]
    assert entry["actor"] == "Tristen Pierson"
    assert (entry["from_status"], entry["to_status"]) == ("staged", "approved")
    assert (entry["from_stage"], entry["to_stage"]) == ("created", "checked")
    assert entry["evidence_refs"] == ["LEDGER.md"]


def test_service_refusal_at_route_changes_nothing(client, staging_env):
    """A status the lifecycle table has no move from (an expired
    record sitting in staging) cannot be rejected through the
    route: the transition does not exist to attempt, the call
    refuses, and the file is byte-identical."""
    _seed(staging_env, _candidate(review_status="expired"))
    before = staging_env["staging"].read_bytes()
    data = client.post(f"{BASE}/staging/action", json={
        "sign": "M777", "proposed_reading": "test",
        "action": "reject", "reason": "no"}).json()
    assert data["ok"] is False
    assert staging_env["staging"].read_bytes() == before


def test_verify_archive_route_trail(client, staging_env):
    _seed(staging_env, _gated(review_status="approved"))
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is True
    archived = _records(staging_env["archive"])
    assert len(archived) == 1
    record = archived[0]
    assert record["review_status"] == "verified"
    assert record["archived_reason"] == "manual_verify_archive"
    moves = [(e["from_status"], e["to_status"])
             for e in record["review_history"]]
    assert moves == [("approved", "verified"), ("verified", "verified")]
    assert all(e["actor"] == "Tristen Pierson"
               for e in record["review_history"])


def test_cleanup_verified_bookkeeping_trail(client, staging_env):
    _seed(staging_env, _gated(review_status="verified"))
    data = client.post(f"{BASE}/staging/cleanup").json()
    assert data["ok"] is True
    assert data["archived"] == 1
    record = _records(staging_env["archive"])[0]
    assert record["review_status"] == "verified"
    assert record["archived_reason"] == "cleanup_action"
    assert record["review_history"]  # the act is on the trail


def test_lifecycle_expiry_routes_through_service(staging_env):
    old = (datetime.now(UTC) - timedelta(days=8)).isoformat(
        timespec="seconds").replace("+00:00", "Z")
    _seed(staging_env, _candidate(
        review_status="rejected", rejected_at=old,
        rejected_reason="user rejected"))
    rl._run_anchor_lifecycle(None, {})
    assert _records(staging_env["staging"]) == []
    record = _records(staging_env["archive"])[0]
    assert record["review_status"] == "expired"
    assert record["archived_reason"] == "expired_after_7d"
    moves = [(e["from_status"], e["to_status"], e["actor"])
             for e in record["review_history"]]
    assert moves == [("rejected", "expired", "research_loop"),
                     ("expired", "expired", "research_loop")]


def test_promote_route_trail(promote_env):
    client = TestClient(create_app())
    promote_env["archive"].write_text(
        json.dumps([_gated(review_status="verified")]), encoding="utf-8")
    data = client.post(f"{BASE}/staging/promote", json={}).json()
    assert data["promoted"] == 1
    record = _records(promote_env["archive"])[0]
    assert record["review_status"] == "promoted"
    (entry,) = record["review_history"]
    assert entry["actor"] == "Tristen Pierson"
    assert (entry["from_stage"], entry["to_stage"]) == ("explained", "accepted")
    assert entry["evidence_refs"] == ["LEDGER.md"]


def test_manual_archive_route_trail(client, staging_env):
    _seed(staging_env, _gated(review_status="approved"))
    data = client.post(f"{BASE}/staging/archive").json()
    assert data["ok"] is True
    record = _records(staging_env["archive"])[0]
    assert record["review_status"] == "approved"  # status unchanged
    assert record["archived_reason"] == "manual_archive"
    (entry,) = record["review_history"]
    assert entry["from_status"] == entry["to_status"] == "approved"
    assert entry["actor"] == "staging_archive"


# --- T402: the stores are written atomically ----------------------------

def test_write_failure_leaves_each_store_byte_identical(
        staging_env, promote_env, monkeypatch):
    """A simulated write failure (the rename itself fails, the
    ENOSPC shape) leaves each of the three stores byte-identical
    and surfaces as the named VerifiedWriteError."""
    def _boom(*args, **kwargs):
        raise OSError(28, "No space left on device")

    cases = [
        (rl._write_staging, staging_env["staging"], [{"sign": "M1"}]),
        (rl._write_archive, staging_env["archive"], [{"sign": "M1"}]),
        (rl._write_anchors, promote_env["anchors"], {"anchors": {}}),
    ]
    for writer, path, payload in cases:
        before = path.read_bytes()
        monkeypatch.setattr("os.replace", _boom)
        with pytest.raises(VerifiedWriteError):
            writer(payload)
        monkeypatch.undo()
        assert path.read_bytes() == before


def test_store_write_failure_at_route_leaves_file_unchanged(
        staging_env, monkeypatch):
    """At the route, a store write failure is the named error
    surfacing (HTTP 500), never a truncated store."""
    def _fail(path, content, **kwargs):
        raise VerifiedWriteError(f"verified write to {path} failed")

    monkeypatch.setattr(rl, "write_file_verified", _fail)
    _seed(staging_env, _gated())
    before = staging_env["staging"].read_bytes()
    client = TestClient(create_app(), raise_server_exceptions=False)
    response = client.post(f"{BASE}/staging/action", json={
        "sign": "M777", "proposed_reading": "test", "action": "approve"})
    assert response.status_code == 500
    assert staging_env["staging"].read_bytes() == before


# --- The exit censuses, as tests ----------------------------------------

_PACKAGE = Path(rl.__file__).resolve().parent.parent  # glossa_lab/


def _package_sources():
    return sorted(_PACKAGE.rglob("*.py"))


def test_census_no_direct_review_status_writes_outside_service():
    """C094-10's exit census: no module in the package assigns
    review_status except the transition service itself. (Dict
    literals in pipelines/research_loop.py set the field at record
    CREATION — staged/blocked on new records — which is not a
    transition; that is the only other occurrence, pinned below.)"""
    assignment = re.compile(r'\["review_status"\]\s*=')
    offenders = []
    for path in _package_sources():
        if path.name == "anchor_transition.py":
            continue
        if assignment.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(_PACKAGE)))
    assert offenders == []

    creation = re.compile(r'"review_status":')
    creators = []
    for path in _package_sources():
        if creation.search(path.read_text(encoding="utf-8")):
            creators.append(str(path.relative_to(_PACKAGE)))
    assert creators == ["pipelines/research_loop.py"]


def test_census_no_direct_truncating_writes_to_the_stores():
    """C094-11's exit census: no module in the package calls
    write_text on any of the three anchor-path stores; the anchor
    path's own modules hold no write_text call at all."""
    store_write = re.compile(
        r"(_STAGING_JSON|_ARCHIVE_JSON|_FA_PATH|_STAGING_ARCHIVE_JSON)"
        r"\.write_text")
    offenders = []
    for path in _package_sources():
        if store_write.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(_PACKAGE)))
    assert offenders == []
    # The API module — the drafting census's 12 sites — holds no
    # write_text call at all after the move. (The pipeline module
    # retains a write_text for outputs/partial_loop_result.json,
    # which is not one of the three stores.)
    text = (_PACKAGE / "api/research_loop.py").read_text(encoding="utf-8")
    assert ".write_text(" not in text
