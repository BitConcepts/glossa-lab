"""Spec 047 step-2 execution tests (Phase-406).

The step-2 act's terminal outcome is INCONCLUSIVE
(classification): step 0 was re-run and passed in the
frozen order, Asset B was re-asserted at the digest the
step-1 outcome record pins, and the section 6.3
classification gate fired on both clauses — 2 testable
sites against the frozen floor of 12, and an empty
domestic/ritual contrast side in the test population —
so the distribution test did not run and no distribution
quantity exists. These tests pin the delivered form:
the gate facts, the census identity with step 1, the
absence of any distribution quantity, and the frozen
section 7 INCONCLUSIVE (classification) wording in the
report.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RESULTS = REPO / "reports/phase406_step2_results.json"
REPORT = REPO / "reports/phase406_step2_report.md"
STEP1_RESULTS = REPO / "reports/phase406_results.json"

ASSET_B_SHA256 = (
    "a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85")
LEDGER_SHA256 = (
    "dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b")

WORDING = (
    "The distribution test did not run: 2 of the "
    "gazetteer's 30 sites survived the two-source "
    "agreement rule as testable (floor 12), and one side "
    "of the comparison is empty in the test population "
    "(the pooled ADMIN-TRADE-GATEWAY side carries both "
    "testable sites; the domestic/ritual contrast side "
    "carries none). The finding of this execution is the "
    "classification itself (Asset B, digest "
    "a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85): "
    "AGREED 3 (of which 1, shahr i sokhta, agreed at "
    "mixed/unknown and excluded by section 4.2), "
    "DISAGREED 1, SINGLE-SOURCE 10, NO-SOURCE 16, with "
    "the disagreed and unclassifiable sites named in "
    "full. No distribution quantity was computed. The "
    "claim stands UNTESTED for its distribution "
    "component, now with the reason measured rather "
    "than asserted.")


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_outcome_is_inconclusive_classification():
    r = _results()
    assert r["outcome"] == "INCONCLUSIVE"
    assert r["outcome_kind"] == "classification gate (spec section 6.3)"
    assert r["headline"] == "INCONCLUSIVE (classification)"
    assert r["stop_gate"] == "6.3 classification gate"
    assert r["freeze_digest"] == (
        "8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7")
    assert r["claim_under_test"] == (
        "indus_valley_script_deciphered_from_myth_"
        "65ff0a26_manual_001")


def test_step0_rerun_passed_and_census_matches_step1():
    r = _results()
    s1 = json.loads(STEP1_RESULTS.read_text(encoding="utf-8"))
    assert r["step0"]["gate_0_1_input_integrity"] == "PASS"
    assert r["step0"]["gate_0_2_spine_reproduction"] == "PASS"
    assert r["step0"]["gate_0_3_join_census"] == "PASS"
    for rel, digest in r["step0"]["gate_0_1_input_sha256"].items():
        assert digest == s1["step0"]["gate_0_1_input_sha256"][rel]
    assert r["step0"]["census"] == s1["step0"]["census"]
    census = r["step0"]["census"]
    assert census["total_records"] == 5679
    assert census["joined_total"] == 5106
    assert census["non_spine_total"] == 573
    assert census["no_site_value"] == 0


def test_asset_b_and_ledger_pins_match_step1_record():
    r = _results()
    asset = r["asset_b"]
    assert asset["sha256"] == ASSET_B_SHA256
    assert asset["pin_match"] is True
    assert asset["rows"] == 30
    assert asset["testable_count"] == 2
    assert asset["per_status_counts"] == {
        "AGREED": 3, "DISAGREED": 1,
        "NO-SOURCE": 16, "SINGLE-SOURCE": 10}
    sites = {t["program_site_id"]: t for t in asset["testable_sites"]}
    assert sites["harappa"]["primary_class"] == "administrative"
    assert sites["lothal"]["primary_class"] == "port/trade"
    ledger = r["ledger_sign_list"]
    assert ledger["sha256"] == LEDGER_SHA256
    assert ledger["pin_match"] is True
    assert ledger["extraction_census"] == {
        "entries_entered": 8, "entries_mapped": 3,
        "entries_unmapped": 5}
    assert ledger["all_unmapped_case_dd_047_13_fires"] is False


def test_classification_gate_fired_on_both_clauses():
    gate = _results()["classification_gate"]
    assert gate["testable_floor"] == 12
    assert gate["testable_count"] == 2
    assert gate["testable_floor_pass"] is False
    assert gate["pooled_sites_in_test_population"] == 2
    assert gate["contrast_sites_in_test_population"] == 0
    assert gate["pooled_nonempty"] is True
    assert gate["contrast_nonempty"] is False
    assert gate["gate_fires"] is True
    pop = {p["program_site_id"]: p for p in gate["test_population"]}
    assert pop["harappa"]["joined_records"] == 2717
    assert pop["lothal"]["joined_records"] == 208


def test_no_distribution_quantity_exists():
    r = _results()
    assert r["distribution_quantities"] is None
    assert r["permutation"] is None
    sens = r["sensitivities"]
    assert sens["each_source_alone"] is None
    assert sens["five_largest_sites"] is None
    excl = sens["exclusions_restated"]
    assert excl["DISAGREED"] == ["surkotada"]
    assert len(excl["SINGLE-SOURCE"]) == 10
    assert len(excl["NO-SOURCE"]) == 16
    assert excl["AGREED_mixed_unknown"] == ["shahr i sokhta"]
    assert excl["NO-CORPUS-COVERAGE"] == []
    assert r["anchors_byte_identical"] is True


def test_report_carries_the_frozen_classification_wording():
    r = _results()
    assert r["wording"] == WORDING
    text = REPORT.read_text(encoding="utf-8")
    assert WORDING in text
    assert "Headline outcome:" in text
    assert "**INCONCLUSIVE (classification)**" in text
    assert ("This result concerns the distribution "
            "component of Roif's ledger thesis only") in text
