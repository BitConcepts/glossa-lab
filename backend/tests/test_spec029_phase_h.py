"""Spec 029 Phase H — anchor annotation and schema (tasks H1–H4).

These tests are the CI validator (H4) over the declared schema
(``specs/029-tao-claim-lifecycle/anchors-schema.json``, H3) and
pin the Phase H annotation of
``backend/reports/INDUS_FINAL_ANCHORS.json``:

* H1 — ``validation_status`` is total: every anchor carries one,
  pre-existing values are preserved verbatim (44
  ``pending_non_sa_validation`` = the Phase-108 register's
  SA-lineage set; 113 ``premise_superseded`` = the CANDIDATE
  'kur' cohort), and the 130 records that carried none now carry
  the value their own provenance establishes (94
  ``strict_sa_independent`` / 33 ``sa_in_provenance_chain`` /
  3 ``no_validation_record``; counts sum to 287);
* H2 — ``strict_set`` is a computed cache: for every record it
  equals the Phase-108 register + Phase-109 rule join
  (``strict_sa_independent_hm``, imported — never
  re-implemented), it reconciles to exactly 94 records
  (90 HIGH + 4 MEDIUM) with the canonical strict-core
  membership (the audit ledger's ``checked`` anchors, an
  independent inline recomputation, and the battery-style
  register computation all agree), and the rule's identifier
  and version are recorded in the file metadata;
* additive only — stripping exactly the Phase H annotation
  reproduces the Phase-D-stamped file byte-identically
  (SHA-256 ``18e6f4b2…``), and stripping Phase D + Phase H
  reproduces the pre-migration file (``eccea6d5…``): no tier,
  reading, basis, or pre-existing value changed;
* the validator discriminates: mutated copies of the live
  document (missing field, out-of-vocabulary value, flipped
  flag, undeclared field, missing metadata block) must fail.

The annotation script lives in the spec directory (house style
for spec tooling); it is loaded by path.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC_DIR = _REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
_ANCHORS_PATH = _REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_REGISTER_PATH = _REPO_ROOT / "reports" / "phase108_provenance_register.json"
_PHASE_D_ANCHORS_SHA256 = (
    "18e6f4b2caa7bc9ae1f5cc92dd96f95ce191a77c56144b95820a368d75a316d6")
_PRE_MIGRATION_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed")
_PHASE_D_KEYS = ("stage", "stage_source", "stage_as_of", "stage_history",
                 "verified_unexplained")


def _load_annotation():
    spec = importlib.util.spec_from_file_location(
        "annotate_phase_h_anchors", _SPEC_DIR / "annotate_phase_h_anchors.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ann = _load_annotation()
_DOC = json.loads(_ANCHORS_PATH.read_text("utf-8"))
_ANCHORS = _DOC["anchors"]
_RECORDS = json.loads(_REGISTER_PATH.read_text("utf-8"))["records"]
_SCHEMA = ann.load_schema()
_LEDGER = json.loads((_SPEC_DIR / "reclassification-ledger.json").read_text("utf-8"))


def _canonical(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False)


# ── H4: the live file validates under the declared schema ────────────────

def test_live_file_validates_clean():
    assert ann.validate_anchors_doc(_DOC, _RECORDS, _SCHEMA) == []


def test_verify_mode_reports_valid_and_reconciled():
    result = ann.verify()
    assert result["valid"], result["problems"]
    assert result["reconciliation"]["match"]


def test_schema_declares_exactly_the_observed_fields():
    shape = _SCHEMA["record_shape"]
    governed = set(shape["required_core_fields"]) \
        | set(shape["phase_d_additive_fields"]) \
        | set(shape["phase_h_additive_fields"])
    observed = set()
    for record in _ANCHORS.values():
        observed |= set(record)
    # No undeclared field is observed, and no declared optional
    # field is stale (declared but never observed).
    assert observed - governed == set(shape["optional_fields"])
    assert set(shape["optional_fields"]) <= observed


# ── H1: validation_status is total, provenance-derived ─────────────────

def test_validation_status_total_with_expected_counts():
    counts = Counter(r.get("validation_status") for r in _ANCHORS.values())
    assert None not in counts
    assert counts == Counter(ann.EXPECTED_VALUE_COUNTS)
    assert sum(counts.values()) == 287


def test_pre_existing_values_preserved_verbatim():
    pending = {s for s, r in _ANCHORS.items()
               if r.get("validation_status") == "pending_non_sa_validation"}
    lineage = {s for s, r in _RECORDS.items()
               if r.get("category") in ann.SA_LINEAGE_CATEGORIES
               if s in _ANCHORS}
    from glossa_lab.pipelines.phase109_followthrough import (  # noqa: PLC0415
        sa_lineage_anchors,
    )
    assert pending == set(sa_lineage_anchors(_RECORDS))
    assert pending == lineage
    assert len(pending) == 44
    premise = {s for s, r in _ANCHORS.items()
               if r.get("validation_status") == "premise_superseded"}
    assert len(premise) == 113
    assert all(_ANCHORS[s]["confidence"] == "CANDIDATE"
               and _ANCHORS[s]["reading"] == "kur" for s in premise)


def test_assigned_values_match_provenance_derivation():
    strict = ann.compute_strict_set(_ANCHORS, _RECORDS)
    for sign, record in _ANCHORS.items():
        if record["validation_status"] in ann.NEW_VALUES:
            assert record["validation_status"] == ann.derive_from_provenance(
                record, _RECORDS.get(sign), sign in strict)
    chained = {s for s, r in _ANCHORS.items()
               if r["validation_status"] == "sa_in_provenance_chain"}
    assert len(chained) == 33
    assert all(_ANCHORS[s]["confidence"] == "HIGH"
               and _RECORDS[s]["sa_in_chain"] for s in chained)
    unvalidated = {s for s, r in _ANCHORS.items()
                   if r["validation_status"] == "no_validation_record"}
    assert len(unvalidated) == 3
    assert all(_ANCHORS[s]["confidence"] == "LOW" for s in unvalidated)


def test_derive_validation_status_rules():
    reg_clean = {"category": "GRAMMAR", "sa_in_chain": False}
    reg_chain = {"category": "DEDR", "sa_in_chain": True}
    # An existing value is preserved verbatim, whatever the join says.
    assert ann.derive_validation_status(
        {"validation_status": "pending_non_sa_validation"},
        reg_clean, True) == "pending_non_sa_validation"
    # Absent: strict first, then SA-in-chain, then no record.
    assert ann.derive_validation_status({}, reg_clean, True) \
        == "strict_sa_independent"
    assert ann.derive_validation_status({}, reg_chain, False) \
        == "sa_in_provenance_chain"
    assert ann.derive_validation_status({}, reg_clean, False) \
        == "no_validation_record"
    assert ann.derive_validation_status({}, None, False) \
        == "no_validation_record"


# ── H2: strict_set is the computed rule join, reconciled to 94 ───────────

def test_strict_set_matches_rule_join_for_every_record():
    from glossa_lab.pipelines.phase109_followthrough import (  # noqa: PLC0415
        strict_sa_independent_hm,
    )
    strict = strict_sa_independent_hm(_ANCHORS, _RECORDS)
    for sign, record in _ANCHORS.items():
        assert isinstance(record["strict_set"], bool)
        assert record["strict_set"] is (sign in strict)


def test_strict_set_reconciles_to_94_with_canonical_membership():
    strict = {s for s, r in _ANCHORS.items() if r["strict_set"]}
    assert len(strict) == 94
    assert Counter(_ANCHORS[s]["confidence"] for s in strict) == \
        Counter({"HIGH": 90, "MEDIUM": 4})
    # Canonical membership, three independent ways: the audit
    # ledger's checked anchors, an inline recomputation from the
    # register fields, and the battery-style register computation.
    ledger_checked = {e["item_id"][len("ANCHOR-"):]
                      for e in _LEDGER["entries"]
                      if e["class"] == "anchor_reading"
                      and e["honest_stage"] == "checked"}
    assert strict == ledger_checked
    inline = {s for s, e in _ANCHORS.items()
              if (e.get("confidence") or "").upper() in ("HIGH", "MEDIUM")
              and _RECORDS[s].get("category")
              not in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
              and not _RECORDS[s].get("sa_in_chain")}
    assert strict == inline
    battery_style = {s for s, r in _RECORDS.items()
                     if r["category"] not in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
                     and not r["sa_in_chain"]
                     and _ANCHORS[s]["confidence"] in ("HIGH", "MEDIUM")}
    assert strict == battery_style


def test_strict_rule_recorded_in_file_metadata():
    block = _DOC["metadata"]["spec029_phase_h_annotation"]
    rule = block["strict_set_rule"]
    declared = _SCHEMA["strict_set_rule"]
    for key in ("rule_id", "rule_source", "rule_version", "register"):
        assert rule[key] == declared[key]
    assert rule["strict_count"] == 94
    assert set(block["validation_status_vocabulary"]) == \
        set(_SCHEMA["validation_status_vocabulary"])


# ── Additive only: canonical comparisons ────────────────────────────────

def test_strip_phase_h_reproduces_phase_d_bytes():
    digest = hashlib.sha256(
        _canonical(ann.strip_phase_h(_DOC)).encode("utf-8")).hexdigest()
    assert digest == _PHASE_D_ANCHORS_SHA256


def test_strip_phase_d_and_h_reproduces_pre_migration_bytes():
    stripped = ann.strip_phase_h(_DOC)
    for rec in stripped["anchors"].values():
        for key in _PHASE_D_KEYS:
            rec.pop(key, None)
    digest = hashlib.sha256(_canonical(stripped).encode("utf-8")).hexdigest()
    assert digest == _PRE_MIGRATION_ANCHORS_SHA256


# ── Script contract: states, idempotency, no smoothing ──────────────────

def _synthetic_doc() -> dict:
    return {"metadata": {}, "anchors": {
        "M001": {"reading": "a", "confidence": "HIGH", "basis": "b"},
        "M002": {"reading": "kur", "confidence": "CANDIDATE", "basis": "b",
                 "validation_status": "premise_superseded"},
    }}


def _synthetic_records() -> dict:
    return {"M001": {"category": "GRAMMAR", "sa_in_chain": False},
            "M002": {"category": "GRAMMAR", "sa_in_chain": False}}


def test_record_state_transitions_and_idempotency():
    doc, records = _synthetic_doc(), _synthetic_records()
    strict = ann.compute_strict_set(doc["anchors"], records)
    assert strict == {"M001"}
    for sign, record in doc["anchors"].items():
        assert ann.record_state(record, records.get(sign),
                                sign in strict) == "unannotated"
    ann.annotate_doc(doc, records)
    for sign, record in doc["anchors"].items():
        assert ann.record_state(record, records.get(sign),
                                sign in strict) == "annotated"
    assert doc["anchors"]["M001"]["validation_status"] \
        == "strict_sa_independent"
    assert doc["anchors"]["M002"]["validation_status"] \
        == "premise_superseded"  # preserved verbatim
    # A tampered flag is a conflict, never smoothed over.
    doc["anchors"]["M001"]["strict_set"] = False
    assert ann.record_state(doc["anchors"]["M001"], records["M001"],
                            True) == "conflict"


def test_reconcile_detects_mismatch_not_smoothed():
    doc = copy.deepcopy(_DOC)
    doc["anchors"]["M002"]["strict_set"] = False
    recon = ann.reconcile_counts(doc, _RECORDS)
    assert not recon["match"]
    assert recon["problems"]


# ── H4 discriminating controls: the validator must fail ─────────────────

def _problems_after(mutate) -> list[str]:
    doc = copy.deepcopy(_DOC)
    mutate(doc)
    return ann.validate_anchors_doc(doc, _RECORDS, _SCHEMA)


def test_validator_fails_on_missing_validation_status():
    problems = _problems_after(
        lambda d: d["anchors"]["M002"].pop("validation_status"))
    assert any("validation_status" in p for p in problems)


def test_validator_fails_on_out_of_vocabulary_value():
    def mutate(d):
        d["anchors"]["M002"]["validation_status"] = "totally_validated"
    problems = _problems_after(mutate)
    assert any("outside the declared vocabulary" in p for p in problems)


def test_validator_fails_on_flipped_strict_flag():
    def mutate(d):
        d["anchors"]["M002"]["strict_set"] = False
    problems = _problems_after(mutate)
    assert any("strict_set" in p for p in problems)


def test_validator_fails_on_undeclared_field():
    def mutate(d):
        d["anchors"]["M002"]["brand_new_field"] = "x"
    problems = _problems_after(mutate)
    assert any("undeclared" in p for p in problems)


def test_validator_fails_without_metadata_block():
    problems = _problems_after(
        lambda d: d["metadata"].pop("spec029_phase_h_annotation"))
    assert any("metadata block" in p for p in problems)


def test_validator_fails_on_wrong_provenance_value():
    def mutate(d):
        # M002 is a strict anchor; a chained value contradicts its
        # register evidence.
        d["anchors"]["M002"]["validation_status"] = "sa_in_provenance_chain"
    problems = _problems_after(mutate)
    assert any("provenance derivation" in p or "inconsistent" in p
               for p in problems)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
