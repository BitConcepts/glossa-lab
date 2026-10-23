"""Spec 055 execution tests (Phase-414).

The execution's terminal outcome is NOT NUMERAL-LIKE:
stage 1 identified the sign (the extended Wells
(2011, 2015) list named from the document's own text;
the drawn sign matched by drawn form to registry row
P154, corpus identifier Mahadevan 287), gate 0.4
pinned the strict corpus (2,906 records; the target at
79 occurrences, above the frozen floor of 5), and
stage 2 assigned NOT NUMERAL-LIKE by the frozen
section 5.3 mapping alone (numeral-side 1,
control-side 3). These tests pin the delivered form:
the section 6 recovery record, the results record's
gate and mapping facts, and the frozen traps asserted
as traps (a match smuggled out of the W900 registry
string, a value-six statement, or a D-16 admission
would fail here).
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO / "specs/055-sign900-numeral"
RECOVERY = SPEC_DIR / "source-table-recovery.json"
EXPORT = SPEC_DIR / "strict-corpus-export.jsonl"
RESULTS = REPO / "reports/phase414_results.json"


def _recovery() -> dict:
    return json.loads(RECOVERY.read_text(encoding="utf-8"))


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_recovery_record_form_and_identification():
    rec = _recovery()
    assert rec["producer_spec"] == "055"
    assert rec["schema"] == "glossa.source-table-recovery/1"
    assert rec["producer_claim_id"] == (
        "ancient_writing_and_modern_technologies_"
        "51831ac9_sign_val_0001")
    assert rec["recovery_outcome"] == "IDENTIFIED"
    assert "closure" not in rec
    naming = rec["sign_list_naming"]
    assert "extended Wells (2011, 2015)" in naming["list_named"]
    assert len(naming["naming_statements"]) >= 2
    for stmt in naming["naming_statements"]:
        assert stmt["quote"] and stmt["locator"]
    headings = [m["section_heading"]
                for m in rec["recovered_material"]]
    assert "Sign 900" in headings
    assert "Numerical value of Sign 900" in headings
    assert "SUMMARY" in headings
    figs = {f["figure"] for f in rec["figure_refs"]}
    assert figs == {"Figure 11", "Figure 12", "Figure 29"}
    assert rec["sign_700_material"]["present"] is True
    assert rec["sign_700_material"]["locators"]


def test_target_sign_matched_by_drawn_form_not_number():
    rec = _recovery()
    ts = rec["target_sign"]
    assert ts["source_sign_no"] == "900"
    assert ts["drawn_sign_match_basis"] == "crosswalk-registry"
    assert ts["crosswalk_registry_id"] == "P154"
    assert "single-arc grapheme" in ts["match_citation"]
    r = _results()
    ev = r["step1"]["match_evidence"]
    # The trap is recorded as a trap: the W900 cell on the
    # P154 row exists, and the match evidence shows the
    # drawn-form basis (witness + plain-paren uniqueness).
    assert ev["p154_row"]["wells_ids"] == "W900"
    assert "NOT used as the identification" in ev["trap_note"]
    assert len(ev["plain_right_parenthesis_rows"]) == 1
    assert ev["plain_right_parenthesis_rows"][0]["sign_id"] == "P154"
    assert ev["witness_rows_for_grapheme_900"][0]["sign"] == "M287"
    assert ev["witness_rows_for_grapheme_900"][0][
        "verification"] == "verified"


def test_step0_and_gate04_facts():
    r = _results()
    for pin in r["step0"]["gate_0_1"].values():
        assert pin["match"] is True
        assert pin["observed_sha256"] == pin["expected_sha256"]
    assert r["step0"]["gate_0_2"]["located_verbatim"] is True
    g = r["gate_0_4"]
    assert g["verdict"] == "PASS"
    assert g["records_exported"] == 2906
    assert g["tokens_total"] == 11507
    assert g["target_occurrences"] == 79
    assert g["target_occurrences"] >= g["occurrence_floor"] == 5
    lines = EXPORT.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2906


def test_pre_counting_record():
    r = _results()
    pre = r["pre_counting"]
    ids = pre["known_numeral_set"]["corpus_identifiers"]
    assert "Mahadevan 287" not in ids  # target excluded
    assert len(ids) == 29
    hedged = {h["source_sign_no"]
              for h in pre["hedged_members_excluded"]}
    assert hedged == {"415", "70"}
    hedged_ids = {h["corpus_identifier"]
                  for h in pre["hedged_members_excluded"]}
    assert not (hedged_ids & set(ids))  # hedged excluded
    assert len(pre["control_set"]["members"]) == 10
    assert pre["dry_run"]["sign"] != "Mahadevan 287"
    assert pre["dry_run"]["measures"]["occurrences"] > 0


def test_outcome_is_the_frozen_mapping_alone():
    r = _results()
    assert r["outcome"] == "NOT NUMERAL-LIKE"
    m = r["step2"]["mapping"]
    assert m["numeral_side_count"] == 1
    assert m["control_side_count"] == 3
    t = r["step2"]["target"]
    assert t["occurrences"] == 79
    assert t["short_text_share"] == 0.164557
    assert t["numeral_adjacency_share"] == 0.455696
    assert t["positional_entropy_bits"] == 2.708415
    assert "does not establish the value six" in r["fence"]
    assert "D-16 does not join this campaign" in (
        r["chain_sentence"])
    assert "value is six; a distribution can support" not in (
        r["headline_wording"])
    assert r["anchors"]["byte_identical"] is True
