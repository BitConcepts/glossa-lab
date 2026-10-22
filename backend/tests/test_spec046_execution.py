"""Spec 046 execution tests (Phase-405).

The execution's terminal outcome is IDENTIFICATION FAILED
(sign unmatched): step 0 passed in full, step 1 named the
source's list from the book's own apparatus, and the drawn
sign could not be matched by drawn form from the held
record. These tests pin the delivered form: the section 6
closure-form concordance file, the results record's gate
facts, and the frozen traps asserted as traps (a W297
match smuggled out of the P205 multi-value cell, or a
P297 number-match, would fail here).
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO / "specs/046-horned-tiger-concordance"
CONCORDANCE = SPEC_DIR / "concordance-297.json"
RESULTS = REPO / "reports/phase405_results.json"

WORDING = (
    "The fragment 'sign 297 is the horned tiger' cannot be carried "
    "to a concordance: the drawn sign could not be matched from "
    "Wells's published list. The record stays a stated gap. No "
    "statement about the sign is made, and nothing is fed to Asset A.")


def _concordance() -> dict:
    return json.loads(CONCORDANCE.read_text(encoding="utf-8"))


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_delivery_is_the_frozen_closure_form():
    c = _concordance()
    assert c["producer_spec"] == "046"
    assert c["schema"] == "glossa.concordance/1"
    assert c["producer_claim_id"] == (
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002")
    assert c["signs"] == []
    assert c["closure"]["class"] == "IDENTIFICATION FAILED (sign unmatched)"
    assert c["closure"]["wording"] == WORDING


def test_results_record_step0_passed():
    r = _results()
    assert r["outcome"] == "IDENTIFICATION FAILED"
    assert r["closure_class"] == "IDENTIFICATION FAILED (sign unmatched)"
    for pin in r["step0"]["gate_0_1"].values():
        assert pin["match"] is True
        assert pin["observed_sha256"] == pin["expected_sha256"]
    assert r["step0"]["gate_0_2"]["located_verbatim"] is True
    gates = r["step0"]["gate_0_3"]
    assert gates["WELLS"]["availability"] == "HELD"
    assert gates["CISI"]["availability"] == "HELD"
    assert gates["PARPOLA"]["availability"] == "CITABLE"
    assert gates["MAHADEVAN"]["availability"] == "CITABLE"


def test_results_record_step1_facts():
    r = _results()
    assert "Wells's own sign list" in r["step1"]["source_list_named"]
    ev = r["step1"]["match_evidence"]
    assert ev["registry_rows"] == 803
    assert ev["registry_tiger_descriptions"] == 0
    assert ev["p297_description"].startswith("Ladder motif")
    assert ev["wells_witness_grapheme_297_rows"] == []
    # The only W297 cell is the frozen trap: the P205
    # multi-value cell, not a singleton match.
    assert len(ev["w297_cells"]) == 1
    cell = ev["w297_cells"][0]
    assert cell["sign_id"] == "P205"
    assert cell["singleton"] is False
    assert "W297" in cell["wells_ids"].split("|")
    assert r["step1"]["drawn_sign_match"] is None


def test_no_scoring_was_reached_or_fed():
    r = _results()
    assert "step2" not in r
    c = _concordance()
    assert "asset_a_feed" not in json.dumps(c)
