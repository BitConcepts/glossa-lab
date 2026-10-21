"""Spec 042 execution tests (Phase-407).

The execution's terminal outcome is THIN: step 0
gates 0.1-0.3 passed in the frozen order, and gate
0.4 found the tablet stratum TOO THIN (at least 20
inscriptions of the type at only 2 of the 6 sites),
so under DD-042-2 the execution closed with
headline THIN, neither stratum was computed, and
gate 0.5 was not reached. These tests pin the
delivered form: the results record's gate facts,
the census, the absence of any stratum quantity,
and the frozen section 4.3 THIN wording in the
report.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RESULTS = REPO / "reports/phase407_results.json"
REPORT = REPO / "reports/phase407_report.md"

WORDING = (
    "The object-type split cannot be run as designed: "
    "the tablet stratum carries fewer than six sites "
    "with at least twenty inscriptions of its type "
    "(Chanhu-daro 2; Dholavira 15; Harappa 1076; "
    "Kalibangan 3; Lothal 2; Mohenjo-daro 164). No "
    "stratum quantity was computed. Spec 028 Arm B "
    "stands exactly as recorded.")

CENSUS_TAB = {"Chanhu-daro": 2, "Dholavira": 15,
              "Harappa": 1076, "Kalibangan": 3,
              "Lothal": 2, "Mohenjo-daro": 164}
CENSUS_SEAL = {"Chanhu-daro": 52, "Dholavira": 96,
               "Harappa": 361, "Kalibangan": 49,
               "Lothal": 72, "Mohenjo-daro": 1138}


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_outcome_is_thin_at_gate_0_4():
    r = _results()
    assert r["outcome"] == "THIN"
    assert r["headline"] == "THIN"
    assert r["stop_gate"] == "0.4"
    assert r["freeze_digest"] == (
        "6be2988d7f4c290591d36f391ac84a772f18a"
        "9121e35ddd0e251956b5260f753")
    assert r["claim_under_test"] == "STUDY-SPEC-028/ARM-B"


def test_step0_gates_0_1_to_0_3_passed():
    r = _results()
    for pin in r["step0"]["gate_0_1"]["pins"].values():
        assert pin["match"] is True
        assert pin["observed_sha256"] == pin["expected_sha256"]
    g2 = r["step0"]["gate_0_2"]
    assert g2["pass"] is True
    assert g2["flow_counts_observed"] == [5679, 4531, 4505,
                                          3605, 3144, 3030]
    assert g2["flow_matches_recorded_results"] is True
    assert g2["flow_matches_margins_audit"] is True
    assert g2["cells_match_margins_audit"] is True
    assert g2["analysis_records"] == 3030
    assert g2["sign_columns"] == 125


def test_census_partitions_the_population():
    r = _results()
    g3 = r["step0"]["gate_0_3"]
    assert g3["pass"] is True
    assert g3["other_types_present"] == []
    assert g3["census"]["SEAL"] == CENSUS_SEAL
    assert g3["census"]["TAB"] == CENSUS_TAB
    assert g3["census"]["totals"] == {"SEAL": 1768,
                                       "TAB": 1262,
                                       "all": 3030}
    assert g3["strata_sum"] == 3030


def test_gate_0_4_tablet_stratum_too_thin():
    r = _results()
    g4 = r["step0"]["gate_0_4"]
    assert g4["pass"] is False
    assert g4["floors"]["SEAL"]["pass"] is True
    assert g4["floors"]["SEAL"]["sites_at_or_above_floor"] == 6
    tab = g4["floors"]["TAB"]
    assert tab["pass"] is False
    assert tab["too_thin"] is True
    assert tab["sites_at_or_above_floor"] == 2
    assert tab["per_site_counts"] == CENSUS_TAB


def test_no_stratum_quantity_and_gate_0_5_not_reached():
    r = _results()
    assert r["strata"] is None
    assert r["step0"]["gate_0_5"] == {"reached": False}
    assert r["anchors"]["byte_identical"] is True
    assert r["anchors"]["before"] == r["anchors"]["after"]


def test_report_carries_the_frozen_thin_wording():
    text = REPORT.read_text(encoding="utf-8")
    assert WORDING in text
    assert "This result is about repertoire association in " \
           "recorded data. It is not evidence that any " \
           "population moved." in text
    assert "Headline outcome: **THIN**" in text
