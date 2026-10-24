"""Tests for the Spec 040 execution records.

Phase-439 (D-25: G1 with time held fixed — the
chronology-controlled rerun of the Spec 025 /
Phase-140 site-repertoire test) executed under
the frozen contract: step 0 passed all three
gates in order (pin verification; population
reproduction and the section 4.1 join under
derivation A1, reproducing the freeze section 3
counts exactly; determinism), the section 5
margins gate then failed on arms 1 and 2 (arm 3
passed), and the run closed NOT-YET-TESTABLE
(DD-040-5) with the section 7 regression, the
section 6 primary, and the section 8
sensitivities not reached and no outcome
quantity computed. These tests pin the recorded
facts: a gate verdict, a margins number, or a
record that drifts from the executed run fails
here.

Author: Spec 040 (Phase-439), 2026-10-24.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports/phase439_results.json"
REPORT = REPO_ROOT / "reports/phase439_report.md"
SPEC_DIR = REPO_ROOT / "specs/040-d25-g1-chronology-controlled"
FREEZE_DIGEST = (
    "16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515"
)
ARTIFACT_SHA256 = (
    "1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
RIDER = (
    "Chronology is NOT controlled in the primary test: "
    "period/phase (chronology) remain uncontrolled "
    "confounders; the S-chron sensitivity bound is reported "
    "alongside, never as the controlled verdict."
)
RIDER_FRAGMENTS = (
    "Chronology is NOT",
    "controlled in",
    "the primary test",
    "period/phase",
    "(chronology) remain uncontrolled confounders",
    "the S-chron",
    "sensitivity bound is reported",
    "alongside,",
    "never as the controlled verdict",
)


def _carries_rider(text: str) -> bool:
    """The rider, carried across the record's hard wrapping."""
    flat = " ".join(text.split())
    if RIDER in flat:
        return True
    return all(fragment in flat for fragment in RIDER_FRAGMENTS)


def _results() -> dict:
    return json.loads(RESULTS.read_text("utf-8"))


def test_phase439_results_record_complete():
    r = _results()
    text = RESULTS.read_text("utf-8")
    assert r["spec"] == "040"
    assert r["phase"] == 439
    assert r["claim_under_test"] == "STUDY-SPEC-025/G1"
    assert r["contract"]["freeze_digest"] == FREEZE_DIGEST
    assert r["contract"]["osf_registration"] == "2rgtb"
    assert r["contract"]["derivation"] == "A1"
    assert "successor-artifact substitution" in (
        r["contract"]["dependency"])
    assert "DD-040-5 confirmed" in " ".join(r["contract"]["rulings"])
    assert ARTIFACT_SHA256 in text
    assert r["execution"]["date"] == "2026-10-24"


def test_step0_gates_in_order_all_pass():
    r = _results()
    verdicts = [(g["gate"], g["verdict"]) for g in r["gates"]]
    assert verdicts == [("1", "PASS"), ("2", "PASS"), ("3", "PASS")]
    pins = r["step0"]["pins"]
    for name, check in pins.items():
        assert check["match"], name
    assert pins["layer"]["observed"] == (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef")
    assert r["step0"]["determinism"] == {
        "runs": 2, "canonical_identical": True}


def test_join_reproduces_the_freeze_counts():
    j = _results()["step0"]["join"]
    assert j["population_rows"] == 5410
    assert j["population_by_site"] == {
        "Chanhu-daro": 74, "Dholavira": 238, "Harappa": 2717,
        "Kalibangan": 212, "Lothal": 208, "Mohenjo-daro": 1923,
        "Nausharo": 38}
    assert j["label_margins"] == {
        "period": 2266, "phase": 2638, "both": 1788,
        "union": 3116, "neither": 2294}
    assert j["covariate_layer_agreement"] == {
        "rows_checked": 5410, "mismatches": 0}
    assert j["census_triples"] == 78
    assert j["artifact_cells"]["contested"] == 0
    assert j["placed"] == {"EARLY": 32, "MATURE": 1386, "LATE": 39}
    assert j["unplaced"] == {
        "no_informative_label": 2294, "all_unassigned": 1658,
        "disagreement": 1}
    assert j["placed_by_site"] == {
        "Dholavira": 133, "Harappa": 1021, "Kalibangan": 157,
        "Lothal": 108, "Nausharo": 38}


def test_margins_gate_arms_and_values():
    m = _results()["margins"]
    assert m["assigned_total"] == 1457
    assert m["unassigned_total"] == 3953
    assert m["unassigned_share"] == 0.730684
    assert m["contested_excluded"] == 0
    assert m["sites_per_period"] == {
        "EARLY": 1, "MATURE": 5, "LATE": 2}
    assert m["sites_per_period_named"]["EARLY"] == ["Harappa"]
    assert m["sites_per_period_named"]["LATE"] == [
        "Dholavira", "Lothal"]
    assert m["strata"] == {
        "strata_total": 65, "strata_multi_site": 36,
        "permutable_inscriptions": 1205}
    assert [(a["arm"], a["verdict"]) for a in m["arms"]] == [
        (1, "FAIL"), (2, "FAIL"), (3, "PASS")]
    assert m["gate_verdict"] == "FAIL"
    assert m["by_site"]["Mohenjo-daro"]["assigned"] == 0
    assert m["by_site"]["Harappa"]["assigned_by_period"] == {
        "EARLY": 32, "MATURE": 989}
    assert m["by_site"]["Dholavira"]["assigned_by_period"] == {
        "MATURE": 97, "LATE": 36}


def test_closure_wording_and_unreached_stages():
    r = _results()
    assert r["outcome"] == "NOT-YET-TESTABLE"
    assert r["margins_gate"]["closure"] == "NOT-YET-TESTABLE"
    for stage in ("regression", "primary", "sensitivities"):
        assert r[stage]["status"] == "NOT REACHED", stage
    headline = r["headline_wording"]
    assert "ICIT-lineage layer (horus84)" in headline
    assert "NOT-YET-TESTABLE" in headline
    assert ARTIFACT_SHA256 in headline
    assert "assigned 1457 of 5,410" in headline
    assert "unassigned 3953 (73.1%)" in headline
    assert "contested-excluded 0" in headline
    report = REPORT.read_text("utf-8")
    assert "**NOT-YET-TESTABLE** (DD-040-5)" in report
    assert _carries_rider(report)


def test_anchors_byte_identical_after_run():
    r = _results()
    assert r["anchors"]["pin"] == ANCHORS_SHA256
    assert r["anchors"]["before"] == ANCHORS_SHA256
    assert r["anchors"]["after"] == ANCHORS_SHA256
    assert r["anchors"]["byte_identical"] is True


def test_records_on_disk_carry_the_outcome():
    outcome = (SPEC_DIR / "outcome.md").read_text("utf-8")
    assert "EXECUTION RECORD - appended 2026-10-24" in outcome
    assert "NOT-YET-TESTABLE" in outcome
    assert _carries_rider(outcome)
    step0 = (SPEC_DIR / "step0-record.md").read_text("utf-8")
    assert "STEP 0 PASSED" in step0
    assert "Arm 1 — FAIL" in step0
    assert "Arm 3 — PASS" in step0
    tasks = (SPEC_DIR / "tasks.md").read_text("utf-8")
    for task in ("E1", "E2", "E3", "E4", "E5", "E6", "E7"):
        assert f"- [x] **{task}" in tasks, task
    ledger = (REPO_ROOT / "LEDGER.md").read_text("utf-8")
    assert "Spec 040 EXECUTED (Phase-439)" in ledger
    assert "NOT-YET-TESTABLE at the section 5 margins gate" in ledger
    graph = (REPO_ROOT / "backend/glossa_lab"
             / "experiment_graph_phase439.py").read_text("utf-8")
    assert "IndusPhase439G1ChronologyControlled" in graph
    registry = (REPO_ROOT / "backend/glossa_lab"
                / "experiment_graph.py").read_text("utf-8")
    assert "_phase439_node_defs" in registry
