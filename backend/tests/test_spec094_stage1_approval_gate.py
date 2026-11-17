"""Spec 094 Stage 1 regression tests: the candidate-record schema
(T101 / C094-3) and the approval gate (T102 / C094-1, C094-2).

- T101: falsifier, approver, and evidence_ref are first-class fields
  of the candidate record, carried by the pipeline's staging write
  (present on every newly staged record, empty until adjudication
  records them); records already in the staging file are not
  rewritten (no migration, C094-12). A gate decision taken from
  request-only data is refused by construction: the approve route
  reads the record, never the request.
- T102: probe (a) — the 2026-11-13 acceptance-path approval probe —
  refuses in its original variant (the record carries no falsifier)
  and in its automated-actor variant (the recorded approver is an
  automated identity). A named human who is not on the D-094-1 list
  is refused as well. A conforming approval carries all three
  record fields. Automated identities are refused for verify and
  promote too: a record that never passed the approval gate is not
  verified by verify-archive or cleanup, and does not promote.
"""
from __future__ import annotations

import hashlib
import json

import pytest
from fastapi.testclient import TestClient

from glossa_lab.api import research_loop as rl
from glossa_lab.claim_stage import (
    CANDIDATE_GATE_FIELDS,
    NAMED_HUMAN_APPROVERS,
    is_listed_approver,
)
from glossa_lab.main import create_app
from glossa_lab.pipelines import research_loop as pipe
from glossa_lab.pipelines.research_loop import ResearchLoop

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
    # Membership precondition (defect 3): the snapshot names the test
    # sign's bare form (777 for candidate M777).
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
    """A candidate carrying the full conforming gate record.

    Spec 094 Stage 2 adds the evidence standard to the conforming
    shape: the LEDGER.md artifact pinned by its actual SHA-256 and
    a registered evidence class."""
    base = {"falsifier": _FALSIFIER, "approver": "Tristen Pierson",
            "evidence_ref": "LEDGER.md",
            "evidence_sha256": hashlib.sha256(
                (rl._REPO / "LEDGER.md").read_bytes()).hexdigest(),
            "evidence_class": "external_corpus_record"}
    base.update(over)
    return _candidate(**base)


def _seed(staging_env, *candidates):
    staging_env["staging"].write_text(
        json.dumps(list(candidates)), encoding="utf-8")


def _record(staging_env, sign="M777"):
    records = json.loads(staging_env["staging"].read_text(encoding="utf-8"))
    for c in records:
        if c.get("sign") == sign:
            return c
    raise AssertionError(f"candidate {sign} missing from staging file")


def _approve(client, **over):
    body = {"sign": "M777", "proposed_reading": "test", "action": "approve"}
    body.update(over)
    return client.post(f"{BASE}/staging/action", json=body)


# --- Actor rules: the D-094-1 list ------------------------------------

def test_gate_fields_and_approver_list_shape():
    assert CANDIDATE_GATE_FIELDS == ("falsifier", "approver", "evidence_ref")
    # D-094-1 as adopted: the list initially contains the owner alone.
    assert NAMED_HUMAN_APPROVERS == frozenset({"tristen_pierson"})


def test_is_listed_approver():
    assert is_listed_approver("Tristen Pierson") is True
    assert is_listed_approver("tristen pierson") is True  # normalized
    assert is_listed_approver("Tristen Pierson", actor_kind="human") is True
    # A named human who is not on the list does not validate.
    assert is_listed_approver("Jane Doe") is False
    # Automated identities never validate, by allowlist or process token.
    assert is_listed_approver("research_loop") is False
    assert is_listed_approver("aee_scoring") is False
    assert is_listed_approver("Tristen Pierson", actor_kind="automated") is False
    assert is_listed_approver("") is False


# --- T101: the staging write carries the fields ------------------------

def test_staging_write_carries_gate_fields(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    archive = tmp_path / "anchor_staging_archive.json"
    anchors = tmp_path / "INDUS_FINAL_ANCHORS.json"
    legacy = {"sign": "M001", "proposed_reading": "old",
              "review_status": "staged"}
    staging.write_text(json.dumps([legacy]), encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    anchors.write_text(json.dumps({"anchors": {}}), encoding="utf-8")
    monkeypatch.setattr(pipe, "_STAGING_JSON", staging)
    monkeypatch.setattr(pipe, "_STAGING_ARCHIVE_JSON", archive)
    monkeypatch.setattr(pipe, "_ANCHORS_JSON", anchors)

    loop = ResearchLoop(max_cycles=1)
    loop.anchor_candidates = [
        _candidate(),
        _candidate(sign="M888", proposed_reading="preset",
                   falsifier="preset falsifier"),
    ]
    loop._save_staging()

    records = {c["sign"]: c for c in
               json.loads(staging.read_text(encoding="utf-8"))}
    # Every newly staged record carries all three gate fields.
    for sign in ("M777", "M888"):
        for field in CANDIDATE_GATE_FIELDS:
            assert field in records[sign]
    assert records["M777"]["falsifier"] == ""
    assert records["M777"]["approver"] == ""
    assert records["M777"]["evidence_ref"] == ""
    # A producer-supplied value is carried, not overwritten.
    assert records["M888"]["falsifier"] == "preset falsifier"
    # The pre-existing record is not rewritten (no migration, C094-12).
    for field in CANDIDATE_GATE_FIELDS:
        assert field not in records["M001"]


# --- T102: probe (a) refuses, in both variants --------------------------

def test_probe_a_original_variant_refused(client, staging_env):
    """Probe (a) as run on 2026-11-13 approved a genuine candidate in
    one call. On the built gate the same call refuses: the record
    carries no falsifier, and nothing changes."""
    _seed(staging_env, _candidate())
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = _approve(client).json()
    assert data["ok"] is False
    assert "falsifier" in data["error"]
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "staged"


def test_gate_decision_from_request_only_data_refused(client, staging_env):
    """C094-3: falsifier and approver supplied ONLY in the approve
    request do not approve a record that lacks them — the gate reads
    the record, so the decision is refused by construction."""
    _seed(staging_env, _candidate())
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = _approve(client, falsifier=_FALSIFIER,
                    approver="Tristen Pierson").json()
    assert data["ok"] is False
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "staged"


def test_probe_a_automated_actor_variant_refused(client, staging_env):
    """Probe (a), automated-actor variant: the record carries a
    falsifier, but its recorded approver is the loop itself."""
    _seed(staging_env, _candidate(falsifier=_FALSIFIER,
                                  approver="research_loop",
                                  evidence_ref="LEDGER.md"))
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = _approve(client).json()
    assert data["ok"] is False
    assert "automated" in data["error"]
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert _record(staging_env)["review_status"] == "staged"


def test_unlisted_named_human_refused(client, staging_env):
    """A genuine named human who is not on the D-094-1 list does not
    validate as an approver."""
    _seed(staging_env, _candidate(falsifier=_FALSIFIER,
                                  approver="Jane Doe",
                                  evidence_ref="LEDGER.md"))
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = _approve(client).json()
    assert data["ok"] is False
    assert "D-094-1" in data["error"]
    assert staging_env["staging"].read_text(encoding="utf-8") == before


def test_missing_approver_refused(client, staging_env):
    _seed(staging_env, _candidate(falsifier=_FALSIFIER,
                                  evidence_ref="LEDGER.md"))
    data = _approve(client).json()
    assert data["ok"] is False
    assert "approver" in data["error"]
    assert _record(staging_env)["review_status"] == "staged"


def test_conforming_approval_carries_all_three_fields(client, staging_env):
    _seed(staging_env, _gated())
    data = _approve(client).json()
    assert data["ok"] is True
    record = _record(staging_env)
    assert record["review_status"] == "approved"
    assert record["approved_at"]
    # The approved record carries all three gate fields.
    assert record["falsifier"] == _FALSIFIER
    assert record["approver"] == "Tristen Pierson"
    assert record["evidence_ref"] == "LEDGER.md"


def test_conforming_approval_from_blocked(client, staging_env):
    _seed(staging_env, _gated(review_status="blocked"))
    data = _approve(client).json()
    assert data["ok"] is True
    assert _record(staging_env)["review_status"] == "approved"


# --- T102: verify routes refuse records that never passed the gate -----

def test_verify_archive_refuses_ungated_record(client, staging_env):
    _seed(staging_env, _candidate(review_status="approved"))
    before = staging_env["staging"].read_text(encoding="utf-8")
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is False
    assert data["blocked_no_approval_gate"] == ["M777"]
    # Nothing changed: still approved in staging, archive still empty.
    assert staging_env["staging"].read_text(encoding="utf-8") == before
    assert json.loads(
        staging_env["archive"].read_text(encoding="utf-8")) == []


def test_verify_archive_mixed_batch(client, staging_env):
    _seed(staging_env,
          _gated(review_status="approved"),
          _candidate(sign="M888", proposed_reading="ungated",
                     review_status="approved"))
    data = client.post(f"{BASE}/staging/verify-archive").json()
    assert data["ok"] is True
    assert data["verified"] == 1
    assert data["blocked_no_approval_gate"] == ["M888"]
    archived = json.loads(staging_env["archive"].read_text(encoding="utf-8"))
    assert [c["sign"] for c in archived] == ["M777"]
    assert archived[0]["review_status"] == "verified"
    # The ungated candidate stays in staging, still approved.
    assert _record(staging_env, "M888")["review_status"] == "approved"


def test_cleanup_does_not_verify_ungated_record(client, staging_env):
    _seed(staging_env,
          _candidate(review_status="approved"),
          _gated(sign="M888", proposed_reading="gated",
                 review_status="approved"))
    data = client.post(f"{BASE}/staging/cleanup").json()
    assert data["ok"] is True
    assert data["archived"] == 1
    assert data["blocked_no_approval_gate"] == ["M777"]
    # The ungated candidate was NOT verified: still approved, in staging.
    assert _record(staging_env)["review_status"] == "approved"
    archived = json.loads(staging_env["archive"].read_text(encoding="utf-8"))
    assert [c["sign"] for c in archived] == ["M888"]
    assert archived[0]["review_status"] == "verified"


# --- T102: promote refuses records that never passed the gate ----------

def test_promote_refuses_ungated_record(client, promote_env):
    """A verified archive record with a resolving evidence ref but
    no recorded falsifier/approver (the pre-gate shape) does not
    promote: C094-12's suspension, enforced by the gate."""
    promote_env["archive"].write_text(json.dumps([_candidate(
        review_status="verified", evidence_ref="LEDGER.md")]),
        encoding="utf-8")
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = client.post(f"{BASE}/staging/promote", json={}).json()
    assert data["promoted"] == 0
    assert data["blocked_no_approval_gate"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_promote_conforming_record_promotes(client, promote_env):
    promote_env["archive"].write_text(json.dumps([_gated(
        review_status="verified")]), encoding="utf-8")
    data = client.post(f"{BASE}/staging/promote", json={}).json()
    assert data["promoted"] == 1
    assert data["blocked_no_approval_gate"] == []
