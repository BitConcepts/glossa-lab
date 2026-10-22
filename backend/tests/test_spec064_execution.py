"""Spec 064 execution tests (Phase-426).

The execution's terminal outcome is IDENTIFICATION FAILED
(continuity/discrimination not sustained): step 0 passed
in full (including gate 0.4, the preserved reference at
its pinned digest with the thesis digest asserted), step
1.1 named the source's list from the book's own
apparatus, step D derived the descriptor twice and
sustained the preserved reference, and step C —
mandatory in this successor — was not sustained by
either derivation, so the run closed before step M and
before any scoring. These tests pin the delivered form:
the section 6 closure-form concordance file in this
spec's own directory (with the QUALIFIED qualification
carried in its wording), the results record's gate and
step D/C facts, the frozen traps asserted as traps, the
Spec 046 closure delivery standing byte-unedited, and
the claim record's successor append carried beside the
unedited Spec 046 first check (facts only — the
extracted-claims store is regeneration-preserved, so no
whole-file hash is asserted here).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO / "specs/064-sign297-concordance-successor"
CONCORDANCE = SPEC_DIR / "concordance-297.json"
RESULTS = REPO / "reports/phase426_results.json"
CONC046 = REPO / "specs/046-horned-tiger-concordance/concordance-297.json"
REFERENCE = SPEC_DIR / "drawn-form-reference-297.json"
CLAIM_RECORD = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json")

CLOSURE_CLASS = (
    "IDENTIFICATION FAILED (continuity/discrimination not sustained)")
WORDING = (
    "The fragment 'sign 297 is the horned tiger' cannot be carried "
    "to a concordance: the descriptor's discrimination of 297 from "
    "its neighbours in the 289–308 run was not sustained by both "
    "independent derivations. The record stays a stated gap. No "
    "statement about the sign is made, and nothing is fed to "
    "Asset A. Qualification (carried from the preserved reference, "
    "Spec 064 §1): the identification of Wells's 297 rests on a "
    "drawn-form reference whose continuity status is QUALIFIED "
    "— anchored at family level only; its step C discrimination "
    "check is part of this run's record.")


def _concordance() -> dict:
    return json.loads(CONCORDANCE.read_text(encoding="utf-8"))


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_delivery_is_the_frozen_closure_form():
    c = _concordance()
    assert c["producer_spec"] == "064"
    assert c["schema"] == "glossa.concordance/1"
    assert c["producer_claim_id"] == (
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002")
    assert c["signs"] == []
    assert c["closure"]["class"] == CLOSURE_CLASS
    assert c["closure"]["wording"] == WORDING
    # The QUALIFIED status is carried, never dropped.
    assert "QUALIFIED" in c["closure"]["wording"]


def test_predecessor_delivery_and_reference_stand():
    assert hashlib.sha256(CONC046.read_bytes()).hexdigest() == (
        "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf")
    assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest() == (
        "33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4")
    ref = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert ref["continuity_status"]["status"] == "QUALIFIED"


def test_results_record_step0_passed():
    r = _results()
    assert r["outcome"] == "IDENTIFICATION FAILED"
    assert r["closure_class"] == CLOSURE_CLASS
    assert r["continuity_status"] == "QUALIFIED"
    for pin in r["step0"]["gate_0_1"].values():
        assert pin["match"] is True
        assert pin["observed_sha256"] == pin["expected_sha256"]
    assert r["step0"]["gate_0_2"]["located_verbatim"] is True
    gates = r["step0"]["gate_0_3"]
    assert gates["WELLS"]["availability"] == "HELD"
    assert gates["CISI"]["availability"] == "HELD"
    assert gates["PARPOLA"]["availability"] == "CITABLE"
    assert gates["MAHADEVAN"]["availability"] == "CITABLE"
    g4 = r["step0"]["gate_0_4"]
    assert g4["reference_at_pinned_digest"] is True
    assert g4["continuity_status"] == "QUALIFIED"
    assert g4["thesis_digest_asserted_before_plate_read"] is True
    assert g4["thesis_observed_sha256"] == g4["thesis_expected_sha256"]
    assert g4["thesis_observed_bytes"] == g4["thesis_expected_bytes"]


def test_results_record_step_d_and_step_c():
    r = _results()
    assert "Wells's own sign list" in r["step1"]["source_list_named"]
    facts = r["step1"]["registry_witness_facts"]
    assert facts["registry_rows"] == 803
    assert facts["registry_tiger_descriptions"] == 0
    assert facts["p297_description"].startswith("Ladder motif")
    assert facts["witness_grapheme_297_rows"] == []
    assert facts["witness_m297_wells_grapheme"] == "924"
    assert len(facts["w297_cells"]) == 1
    assert facts["w297_cells"][0]["singleton"] is False
    step_d = r["step1"]["step_d"]
    assert len(step_d["derivations"]) == 2
    comparison = step_d["comparison_with_preserved"]
    assert comparison["material_difference"] is False
    step_c = r["step1"]["step_c"]
    assert step_c["derivation_a_affirms"] is False
    assert step_c["derivation_b_affirms"] is False
    assert step_c["sustained"] is False
    assert "NOT an identification" in step_c["family_anchor_carried"]
    assert r["step1"]["step_m"]["reached"] is False
    # The traps are asserted as traps in the run record.
    traps = " ".join(r["step1"]["traps_asserted"])
    assert "P205" in traps and "Ladder motif" in traps
    assert "924" in traps and "M180" in traps


def test_no_scoring_was_reached_or_fed():
    r = _results()
    assert "step2" not in r
    c = _concordance()
    assert "asset_a_feed" not in json.dumps(c)


def test_claim_record_successor_append():
    doc = json.loads(CLAIM_RECORD.read_text(encoding="utf-8"))
    entry = next(
        c for c in doc["claims"] if c["claim_id"].endswith("sign_val_0002"))
    # The fragment's own facts are unchanged.
    assert entry["claim_status"] == "untested"
    assert entry["stage"] == "created"
    assert "horned tiger" in entry["normalized_claim"]
    # Spec 046's first check stands unedited beside the append.
    assert entry["first_check"]["spec"] == "046"
    assert entry["first_check"]["delivery_sha256"].startswith("772db4df")
    append = entry["spec064_check"]
    assert append["spec"] == "064"
    assert append["phase"] == "Phase-426"
    assert append["date"] == "2026-10-22"
    assert append["outcome"] == CLOSURE_CLASS
    assert append["wording"] == WORDING
    digest = hashlib.sha256(CONCORDANCE.read_bytes()).hexdigest()
    assert append["delivery_sha256"] == digest
