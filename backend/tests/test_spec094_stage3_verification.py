"""Spec 094 Stage 3 regression tests: verification redefined —
the flat-delta flip removed (T301, C094-7), per-candidate
verification + the MEDIUM binding (T302, C094-6, C094-8), and the
fabricated fallback delta removed (T303, C094-9).

- T301: a lifecycle run over approved candidates under a clean
  foundation check flips nothing; the lifecycle's remaining duty
  (expiry of stale rejections) is unchanged.
- T302: verification is a recorded per-candidate evaluation
  effected by a named human on the D-094-1 list (the design note's
  method, records/stage-3-design-note-2026-11-16.md). The verify
  transitions require it; promotion confers MEDIUM only on
  candidates so verified — an unverified candidate caps at LOW
  whatever its score, and a 'verified' record carrying no
  evaluation (the pre-094 stock shape) caps at LOW too.
- T303: no staging response carries an `sa_delta` for a candidate
  with no recorded SA comparison; a recorded delta is carried as
  its recorded value.
"""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from glossa_lab.api import research_loop as rl
from glossa_lab.main import create_app
from glossa_lab.pipelines import research_loop as pipe
from glossa_lab.pipelines.research_loop import ResearchLoop
from glossa_lab.verification import (
    CANDIDATE_VERIFICATION_FIELDS,
    VerificationError,
    is_run_level_citation,
    is_verified_under_spec094,
    record_verification,
    verification_refusal,
)

BASE = "/api/v1/research-loop"

_FALSIFIER = "the reading fails if the positional profile does not replicate"
_EVALUATED_AT = "2026-11-16T00:00:00Z"
_EVALUATION = ("evaluated this candidate's positional profile "
               "against the cited corpus record")


def _ledger_bytes() -> bytes:
    return (rl._REPO / "LEDGER.md").read_bytes()


def _ledger_pin() -> str:
    return hashlib.sha256(_ledger_bytes()).hexdigest()


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
        json.dumps({"canonical_grapheme_ids": ["777", "888", "001"]}) + "\n",
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
    """The conforming adjudicated shape through Stage 2: approval
    gate fields + the pinned, classed evidence standard."""
    c = {"sign": "M777", "proposed_reading": "test",
         "review_status": "approved", "evidence_score": 0.9,
         "evidence_type": "positional_profile",
         "source_experiment": "unit-test",
         "falsifier": _FALSIFIER, "approver": "Tristen Pierson",
         "evidence_ref": "LEDGER.md",
         "evidence_sha256": _ledger_pin(),
         "evidence_class": "external_corpus_record"}
    c.update(over)
    return c


def _verified(**over):
    """A candidate verified under C094-6: the conforming shape plus
    a per-candidate verification evaluation recorded through
    record_verification itself."""
    record = record_verification(
        _candidate(), evaluator="Tristen Pierson",
        evaluation=_EVALUATION, evidence_ref="LEDGER.md",
        evaluated_at=_EVALUATED_AT)
    record.update(over)
    return record


def _promote(client, promote_env, candidates, body=None):
    promote_env["archive"].write_text(
        json.dumps(candidates), encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json=body or {})
    assert r.status_code == 200
    return r.json()


def _anchors(promote_env):
    return json.loads(
        promote_env["anchors"].read_text(encoding="utf-8"))["anchors"]


# --- T302: the recording act and the refusal units -----------------------

def test_record_verification_records_the_evaluation():
    record = _candidate()
    verified = record_verification(
        record, evaluator="Tristen Pierson", evaluation=_EVALUATION,
        evidence_ref="LEDGER.md", evaluated_at=_EVALUATED_AT)
    assert verified["verification_evaluator"] == "Tristen Pierson"
    assert verified["verification_evaluated_at"] == _EVALUATED_AT
    assert verified["verification_evaluation"] == _EVALUATION
    assert verified["verification_evidence_ref"] == "LEDGER.md"
    assert verified["verification_outcome"] == "verified"
    # The input record is not mutated.
    assert "verification_evaluator" not in record
    assert verification_refusal(verified) is None
    assert is_verified_under_spec094(verified)


def test_record_verification_refuses_automated_and_unlisted_evaluators():
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="research_loop",
                            evaluation=_EVALUATION,
                            evidence_ref="LEDGER.md")
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="Jane Doe",
                            evaluation=_EVALUATION,
                            evidence_ref="LEDGER.md")


def test_record_verification_refuses_run_level_and_empty_inputs():
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="Tristen Pierson",
                            evaluation=_EVALUATION,
                            evidence_ref="foundation_check")
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="Tristen Pierson",
                            evaluation="  ",
                            evidence_ref="LEDGER.md")
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="Tristen Pierson",
                            evaluation=_EVALUATION, evidence_ref="")
    with pytest.raises(VerificationError):
        record_verification(_candidate(), evaluator="Tristen Pierson",
                            evaluation=_EVALUATION,
                            evidence_ref="LEDGER.md", outcome="passed")


def test_run_level_citation_shapes():
    for ref in ("foundation_check", "foundation check report",
                "test suite results", "sa_delta", "run delta",
                "the run's overall delta"):
        assert is_run_level_citation(ref), ref
    for ref in ("LEDGER.md", "CISI vol. 2 entry for this sign",
                "corpus record 342, run 12 of the concordance"):
        assert not is_run_level_citation(ref), ref
    assert not is_run_level_citation("")


def test_verification_refusal_units():
    # A bare 'verified' status is not a verification (C094-6/C094-8).
    assert verification_refusal(
        {"review_status": "verified"}) is not None
    assert verification_refusal(_candidate()) is not None
    # A run-level citation confers nothing.
    cited_run = record_verification(
        _candidate(), evaluator="Tristen Pierson",
        evaluation=_EVALUATION, evidence_ref="LEDGER.md",
        evaluated_at=_EVALUATED_AT)
    cited_run["verification_evidence_ref"] = "foundation_check"
    assert verification_refusal(cited_run) is not None
    # A recorded evaluation that did not conclude verified confers
    # nothing.
    negative = record_verification(
        _candidate(), evaluator="Tristen Pierson",
        evaluation="the cited record does not support this reading",
        evidence_ref="LEDGER.md", outcome="not_verified",
        evaluated_at=_EVALUATED_AT)
    assert verification_refusal(negative) is not None
    assert not is_verified_under_spec094(negative)
    # An automated evaluator recorded after the fact confers
    # nothing.
    automated = _verified()
    automated["verification_evaluator"] = "research_loop"
    assert verification_refusal(automated) is not None


def test_staging_write_carries_verification_fields(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    archive = tmp_path / "anchor_staging_archive.json"
    anchors = tmp_path / "INDUS_FINAL_ANCHORS.json"
    staging.write_text("[]", encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    anchors.write_text(json.dumps({"anchors": {}}), encoding="utf-8")
    monkeypatch.setattr(pipe, "_STAGING_JSON", staging)
    monkeypatch.setattr(pipe, "_STAGING_ARCHIVE_JSON", archive)
    monkeypatch.setattr(pipe, "_ANCHORS_JSON", anchors)

    loop = ResearchLoop(max_cycles=1)
    loop.anchor_candidates = [_candidate()]
    loop._save_staging()

    records = json.loads(staging.read_text(encoding="utf-8"))
    assert len(records) == 1
    for field in CANDIDATE_VERIFICATION_FIELDS:
        assert records[0][field] == ""


# --- T301: the lifecycle flip is gone ------------------------------------

def test_lifecycle_flips_nothing_under_clean_foundation_check(staging_env):
    """T301's acceptance test: a lifecycle run over approved
    candidates under a clean foundation check flips nothing —
    the candidates stay approved, in staging, with no verified_at
    and no sa_delta written onto them."""
    staging_env["staging"].write_text(json.dumps([
        _candidate(),
        _candidate(sign="M888", proposed_reading="other"),
    ]), encoding="utf-8")
    rl._run_anchor_lifecycle(
        object(), {"foundation_check": {"n_fail": 0}})
    records = json.loads(staging_env["staging"].read_text(encoding="utf-8"))
    assert len(records) == 2
    for c in records:
        assert c["review_status"] == "approved"
        assert "verified_at" not in c
        assert "sa_delta" not in c
    assert json.loads(
        staging_env["archive"].read_text(encoding="utf-8")) == []


def test_lifecycle_still_expires_stale_rejections(staging_env):
    """The lifecycle's other duty is unchanged: a rejection older
    than 7 days expires and is archived."""
    old = (datetime.now(UTC) - timedelta(days=8)).isoformat(
        timespec="seconds").replace("+00:00", "Z")
    staging_env["staging"].write_text(json.dumps([
        _candidate(review_status="rejected", rejected_at=old),
        _candidate(sign="M888", proposed_reading="fresh",
                   review_status="rejected",
                   rejected_at=datetime.now(UTC).isoformat(
                       timespec="seconds").replace("+00:00", "Z")),
    ]), encoding="utf-8")
    rl._run_anchor_lifecycle(
        object(), {"foundation_check": {"n_fail": 0}})
    remaining = json.loads(
        staging_env["staging"].read_text(encoding="utf-8"))
    assert [c["sign"] for c in remaining] == ["M888"]
    archived = json.loads(
        staging_env["archive"].read_text(encoding="utf-8"))
    assert len(archived) == 1
    assert archived[0]["review_status"] == "expired"
    assert archived[0]["archived_reason"] == "expired_after_7d"


# --- T302: the verify transitions require the evaluation -----------------

def test_verify_archive_refuses_unverified_record(client, staging_env):
    staging_env["staging"].write_text(
        json.dumps([_candidate()]), encoding="utf-8")
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is False
    assert data["blocked_no_verification"] == ["M777"]
    assert data["blocked_no_approval_gate"] == []
    # Nothing changed: still approved in staging, archive empty.
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert json.loads(
        staging_env["archive"].read_text(encoding="utf-8")) == []


def test_verify_archive_verifies_evaluated_record(client, staging_env):
    staging_env["staging"].write_text(
        json.dumps([_verified()]), encoding="utf-8")
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is True
    assert data["verified"] == 1
    assert data["blocked_no_verification"] == []
    archived = json.loads(
        staging_env["archive"].read_text(encoding="utf-8"))
    assert archived[0]["review_status"] == "verified"
    # The evaluation that verified it is on the archived record.
    assert archived[0]["verification_evaluator"] == "Tristen Pierson"
    assert archived[0]["verification_outcome"] == "verified"


def test_verify_archive_mixed_batch_partitions(client, staging_env):
    staging_env["staging"].write_text(json.dumps([
        _verified(),
        _candidate(sign="M888", proposed_reading="unevaluated"),
    ]), encoding="utf-8")
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is True
    assert data["verified"] == 1
    assert data["blocked_no_verification"] == ["M888"]
    remaining = json.loads(
        staging_env["staging"].read_text(encoding="utf-8"))
    assert [c["sign"] for c in remaining] == ["M888"]
    assert remaining[0]["review_status"] == "approved"


def test_cleanup_does_not_verify_unevaluated_record(client, staging_env):
    staging_env["staging"].write_text(json.dumps([
        _candidate(),
        _verified(sign="M888", proposed_reading="evaluated"),
    ]), encoding="utf-8")
    data = client.post(f"{BASE}/staging/cleanup").json()
    assert data["ok"] is True
    assert data["archived"] == 1
    assert data["blocked_no_verification"] == ["M777"]
    remaining = json.loads(
        staging_env["staging"].read_text(encoding="utf-8"))
    assert [c["sign"] for c in remaining] == ["M777"]
    assert remaining[0]["review_status"] == "approved"


# --- T302: the MEDIUM binding at promotion (C094-8) -----------------------

def test_verified_candidate_promotes_at_medium(client, promote_env):
    data = _promote(client, promote_env, [
        _verified(review_status="verified")])
    assert data["promoted"] == 1
    anchors = _anchors(promote_env)
    assert anchors["M777"]["confidence"] == "MEDIUM"
    assert "verification_evaluator=Tristen Pierson" in (
        anchors["M777"]["basis"])


def test_unverified_candidate_caps_at_low_whatever_its_score(
        client, promote_env):
    """An approved-but-unverified candidate at score 0.99 promotes
    at LOW: the former score>=0.8 MEDIUM rule is gone."""
    data = _promote(client, promote_env, [
        _candidate(review_status="approved", evidence_score=0.99)])
    assert data["promoted"] == 1
    assert _anchors(promote_env)["M777"]["confidence"] == "LOW"


def test_verified_status_without_evaluation_caps_at_low(
        client, promote_env):
    """C094-8's falsifier shape, including the pre-094 archive
    stock: a record whose review_status is 'verified' but which
    carries no per-candidate verification evaluation promotes at
    LOW, not MEDIUM."""
    data = _promote(client, promote_env, [
        _candidate(review_status="verified", evidence_score=0.99)])
    assert data["promoted"] == 1
    assert _anchors(promote_env)["M777"]["confidence"] == "LOW"


def test_evaluated_candidate_promotes_at_medium_even_when_approved(
        client, promote_env):
    """The binding reads the recorded evaluation, not the status
    string: a candidate carrying a valid verification evaluation
    is verified under C094-6 and promotes at MEDIUM."""
    data = _promote(client, promote_env, [
        _verified(review_status="approved", evidence_score=0.5)])
    assert data["promoted"] == 1
    assert _anchors(promote_env)["M777"]["confidence"] == "MEDIUM"


# --- T303: no fabricated SA delta -----------------------------------------

def test_get_staging_presents_no_delta_without_a_comparison(
        client, staging_env):
    staging_env["staging"].write_text(json.dumps([
        _candidate(review_status="staged"),
        _candidate(sign="M888", proposed_reading="null-delta",
                   review_status="staged", sa_delta=None),
    ]), encoding="utf-8")
    data = client.get(f"{BASE}/staging").json()
    assert len(data["candidates"]) == 2
    for c in data["candidates"]:
        assert "sa_delta" not in c
    # The derived fields no longer rest on a fabricated delta: the
    # 0.9-score candidate is still recommended on its score alone.
    first = data["candidates"][0]
    assert first["recommended"] is True
    assert first["statistically_sufficient"] is True


def test_get_staging_carries_a_recorded_delta_as_recorded(
        client, staging_env):
    staging_env["staging"].write_text(json.dumps([
        _candidate(review_status="staged", evidence_score=0.5,
                   sa_delta=0.07),
    ]), encoding="utf-8")
    data = client.get(f"{BASE}/staging").json()
    c = data["candidates"][0]
    assert c["sa_delta"] == 0.07
    assert c["recommended"] is True  # on the recorded delta > 0.05
