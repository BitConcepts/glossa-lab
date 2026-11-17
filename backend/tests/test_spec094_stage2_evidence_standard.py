"""Spec 094 Stage 2 regression tests: the promotion evidence
standard — evidence pinning (T201, C094-4) and registered evidence
classes (T202, C094-5).

- The registered list is exactly the four classes C094-5 names, each
  passing the registration guard; loop or anchor-path output about a
  candidate is not a class and cannot be registered as one.
- Pinning records the artifact's SHA-256, its registered class, and
  the pin's provenance on the candidate record; an automated or
  unlisted pinner, an unregistered class, and a self-referential
  class are all refused at pin time.
- Probe (b) variants at promotion: an existing-file reference with
  no pin refuses; a pin created by the promote request itself
  refuses; a pin whose bytes do not match refuses; a
  self-referential class refuses; an unregistered class refuses.
- A registered-class pinned artifact promotes on the record, and the
  promoted anchor's basis carries the pin and class.
"""
from __future__ import annotations

import hashlib
import json

import pytest
from fastapi.testclient import TestClient

from glossa_lab.api import research_loop as rl
from glossa_lab.evidence_standard import (
    CANDIDATE_EVIDENCE_FIELDS,
    REGISTERED_EVIDENCE_CLASSES,
    EvidenceStandardError,
    class_registration_refusal,
    evidence_class_refusal,
    evidence_pin_refusal,
    is_loop_output_class,
    is_registered_evidence_class,
    pin_evidence,
    registered_evidence_classes,
)
from glossa_lab.main import create_app
from glossa_lab.pipelines import research_loop as pipe
from glossa_lab.pipelines.research_loop import ResearchLoop

BASE = "/api/v1/research-loop"

_FALSIFIER = "the reading fails if the positional profile does not replicate"
_PINNED_AT = "2026-11-16T00:00:00Z"


def _ledger_bytes() -> bytes:
    return (rl._REPO / "LEDGER.md").read_bytes()


def _ledger_pin() -> str:
    return hashlib.sha256(_ledger_bytes()).hexdigest()


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
    c = {"sign": "M777", "proposed_reading": "test",
         "review_status": "verified", "evidence_score": 0.9,
         "evidence_type": "positional_profile",
         "source_experiment": "unit-test",
         "falsifier": _FALSIFIER, "approver": "Tristen Pierson",
         "evidence_ref": "LEDGER.md"}
    c.update(over)
    return c


def _pinned(**over):
    """A fully conforming record: Stage 1 gate fields plus the
    Stage 2 evidence standard, pinned through pin_evidence itself."""
    record = pin_evidence(
        _candidate(), _ledger_bytes(),
        evidence_class="external_corpus_record",
        pinned_by="Tristen Pierson", pinned_at=_PINNED_AT)
    record.update(over)
    return record


def _promote(client, promote_env, candidates, body=None):
    promote_env["archive"].write_text(
        json.dumps(candidates), encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json=body or {})
    assert r.status_code == 200
    return r.json()


# --- T202: the registered list and its guard ----------------------------

def test_registered_list_is_the_ratified_four():
    assert registered_evidence_classes() == (
        "adjudicated_claim_dossier",
        "external_corpus_record",
        "independent_expert_record",
        "published_concordance_entry",
    )
    assert set(REGISTERED_EVIDENCE_CLASSES) == set(
        registered_evidence_classes())
    # Every registered class carries its grounding and passes the
    # registration guard its own list must satisfy.
    for name, grounding in REGISTERED_EVIDENCE_CLASSES.items():
        assert grounding.strip()
        assert class_registration_refusal(name) is None
        assert is_registered_evidence_class(name)


def test_class_names_normalize_for_matching():
    assert is_registered_evidence_class("External Corpus Record")
    assert is_registered_evidence_class("external-corpus-record")
    assert not is_registered_evidence_class("corpus_record")


def test_loop_output_classes_cannot_be_registered():
    for name in ("self_referential_loop_output", "loop_run_synthesis",
                 "anchor_staging_archive", "pipeline_output",
                 "research_loop_output", "staging_file_dump",
                 "internal_run_report"):
        assert is_loop_output_class(name), name
        assert class_registration_refusal(name) is not None, name
        assert not is_registered_evidence_class(name), name
    assert class_registration_refusal("") is not None
    # A genuinely external class name passes the guard (it would
    # still need a recorded act to join the list).
    assert class_registration_refusal("museum_catalogue_record") is None
    assert not is_registered_evidence_class("museum_catalogue_record")


# --- T201: pinning ------------------------------------------------------

def test_pin_evidence_records_pin_class_and_provenance():
    record = _candidate()
    pinned = pin_evidence(
        record, b"synthetic artifact bytes",
        evidence_class="Published Concordance Entry",
        pinned_by="Tristen Pierson", pinned_at=_PINNED_AT)
    assert pinned["evidence_sha256"] == hashlib.sha256(
        b"synthetic artifact bytes").hexdigest()
    assert pinned["evidence_class"] == "published_concordance_entry"
    assert pinned["evidence_pinned_at"] == _PINNED_AT
    assert pinned["evidence_pinned_by"] == "Tristen Pierson"
    # The input record is not mutated.
    assert "evidence_sha256" not in record


def test_pin_evidence_refuses_unregistered_and_self_referential():
    with pytest.raises(EvidenceStandardError):
        pin_evidence(_candidate(), b"bytes",
                     evidence_class="conference_presentation",
                     pinned_by="Tristen Pierson")
    with pytest.raises(EvidenceStandardError):
        pin_evidence(_candidate(), b"bytes",
                     evidence_class="self_referential_loop_output",
                     pinned_by="Tristen Pierson")


def test_pin_evidence_refuses_automated_and_unlisted_pinners():
    with pytest.raises(EvidenceStandardError):
        pin_evidence(_candidate(), b"bytes",
                     evidence_class="external_corpus_record",
                     pinned_by="research_loop")
    with pytest.raises(EvidenceStandardError):
        pin_evidence(_candidate(), b"bytes",
                     evidence_class="external_corpus_record",
                     pinned_by="Jane Doe")


def test_pin_and_class_refusal_units():
    assert evidence_pin_refusal({}, b"bytes") is not None
    assert evidence_pin_refusal(
        {"evidence_sha256": "not-a-hash"}, b"bytes") is not None
    assert evidence_pin_refusal(
        {"evidence_sha256": _ledger_pin()}, None) is not None
    assert evidence_pin_refusal(
        {"evidence_sha256": _ledger_pin()}, b"other bytes") is not None
    assert evidence_pin_refusal(
        {"evidence_sha256": _ledger_pin()}, _ledger_bytes()) is None
    assert evidence_class_refusal({}) is not None
    assert evidence_class_refusal(
        {"evidence_class": "self_referential_loop_output"}) is not None
    assert evidence_class_refusal(
        {"evidence_class": "conference_presentation"}) is not None
    assert evidence_class_refusal(
        {"evidence_class": "external_corpus_record"}) is None


def test_staging_write_carries_evidence_fields(tmp_path, monkeypatch):
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
    for field in CANDIDATE_EVIDENCE_FIELDS:
        assert records[0][field] == ""


# --- T201/T202: probe (b) at promotion ----------------------------------

def test_probe_b_existing_file_ref_without_pin_refuses(
        client, promote_env):
    """The Stage 1 conforming shape (resolving ref, gated record)
    carries no pin: promotion now refuses on the pin gate."""
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [_candidate()])
    assert data["promoted"] == 0
    assert data["blocked_evidence_pin"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_probe_b_request_created_pin_refuses(client, promote_env):
    """The promote request supplies the CORRECT hash for the
    artifact — a pin created by the promote request itself still
    refuses (C094-4); the record's absence governs."""
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [_candidate()],
                    body={"evidence_pins": {"M777": _ledger_pin()}})
    assert data["promoted"] == 0
    assert data["blocked_evidence_pin"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_request_pin_conflicting_with_recorded_pin_refuses(
        client, promote_env):
    data = _promote(client, promote_env, [_pinned()],
                    body={"evidence_pins": {"M777": "0" * 64}})
    assert data["promoted"] == 0
    assert data["blocked_evidence_pin"] == ["M777"]


def test_request_pin_echoing_recorded_pin_is_a_noop(client, promote_env):
    data = _promote(client, promote_env, [_pinned()],
                    body={"evidence_pins": {"M777": _ledger_pin()}})
    assert data["promoted"] == 1
    assert data["blocked_evidence_pin"] == []


def test_pin_mismatch_refuses(client, promote_env):
    """The recorded pin is the hash of OTHER bytes: the artifact the
    ref names no longer matches its pin."""
    record = _pinned(evidence_sha256=hashlib.sha256(
        b"the artifact as it was at some earlier time").hexdigest())
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [record])
    assert data["promoted"] == 0
    assert data["blocked_evidence_pin"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_malformed_pin_refuses(client, promote_env):
    data = _promote(client, promote_env, [
        _pinned(evidence_sha256="LEDGER.md")])
    assert data["promoted"] == 0
    assert data["blocked_evidence_pin"] == ["M777"]


def test_self_referential_class_refuses(client, promote_env):
    """Probe (b)'s original shape, one gate later: the record is
    pinned and gated, but its class is the loop's own output about
    the candidate — the 2026-11-13 probe's evidence_type, verbatim."""
    record = _pinned(evidence_class="self_referential_loop_output")
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [record])
    assert data["promoted"] == 0
    assert data["blocked_evidence_class"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_unregistered_class_refuses(client, promote_env):
    data = _promote(client, promote_env, [
        _pinned(evidence_class="conference_presentation")])
    assert data["promoted"] == 0
    assert data["blocked_evidence_class"] == ["M777"]


def test_missing_class_refuses(client, promote_env):
    record = _pinned()
    del record["evidence_class"]
    data = _promote(client, promote_env, [record])
    assert data["promoted"] == 0
    assert data["blocked_evidence_class"] == ["M777"]


def test_registered_class_pinned_artifact_promotes(client, promote_env):
    data = _promote(client, promote_env, [_pinned()])
    assert data["promoted"] == 1
    assert data["blocked_evidence_pin"] == []
    assert data["blocked_evidence_class"] == []
    anchors = json.loads(
        promote_env["anchors"].read_text(encoding="utf-8"))["anchors"]
    assert anchors["M777"]["reading"] == "test"
    # The promotion's basis carries the standard it passed.
    assert f"evidence_sha256={_ledger_pin()}" in anchors["M777"]["basis"]
    assert "evidence_class=external_corpus_record" in (
        anchors["M777"]["basis"])


def test_promote_mixed_batch_partitions(client, promote_env):
    conforming = _pinned()
    unpinned = _candidate(sign="M888", proposed_reading="other")
    data = _promote(client, promote_env, [conforming, unpinned])
    assert data["promoted"] == 1
    assert data["blocked_evidence_pin"] == ["M888"]
    anchors = json.loads(
        promote_env["anchors"].read_text(encoding="utf-8"))["anchors"]
    assert "M777" in anchors and "M888" not in anchors
