"""Spec 091 Stage 3 — battery v2 tests (T301 acceptance; T302 recomputation).

Fixture side (T301): for every pass-by-default path enumerated in
Stage 1's T104 record — P2 (no expectation), P3 (too short), P6
(missing model character), P7 (no anchor neighbours) — plus the
enumeration's named non-credit input default (a missing
avg_position silently defaulted to 0.5, historical line 110), a
fixture in which the HISTORICAL battery awards credit and battery
v2 returns not_run. Genuine checks are proven preserved: cases the
historical battery passes or fails on executed checks come out
the same in v2.

Real-record side (T302): when the T302 run record + acts file are
present (they are produced by the run), the filed dispositions are
recomputed from the run record's per-sign outcomes and checked
against the acts exactly, the census is re-derived from the WP5
audit, and the frozen inputs' hashes are checked against the
T104 record's pins. When the run artifacts are absent the
real-record tests skip — the stage record states why.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
V2_SCRIPT = REPO_ROOT / "backend" / "scripts" / "phase48_medium_validation_v2.py"
HIST_SCRIPT = REPO_ROOT / "backend" / "scripts" / "phase48_medium_validation.py"
SPEC_RECORDS = REPO_ROOT / "specs" / "091-anchor-comparison-integrity" / "records"
ACTS = SPEC_RECORDS / "t302-reclassification-acts.json"
RUN_INDEX = SPEC_RECORDS / "run-index.jsonl"
T104 = SPEC_RECORDS / "t104-pass-by-default-enumeration.json"
WP5_AUDIT = REPO_ROOT / "docs" / "repair-2026-10-26" / "anchor-support-audit.json"
ANCHORS = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v2 = _load_module("phase48_medium_validation_v2", V2_SCRIPT)
hist = _load_module("phase48_medium_validation_hist", HIST_SCRIPT)


# ---------------------------------------------------------------------------
# T301 — one fixture per removed path: historical credit, v2 not_run


def test_p2_no_expectation_default_removed():
    role = {
        "symbol": "X",
        "semantic_role": "UNLISTED_ROLE",
        "avg_position": "0.10",
        "is_starter": "False",
        "is_ending": "False",
    }
    h_pass, h_detail = hist.test_positional("X", "ka", role)
    assert h_pass is True and "pass_by_default" in h_detail
    outcome, _detail = v2.test_positional_v2("X", "ka", role)
    assert outcome == v2.NOT_RUN


def test_p3_too_short_default_removed():
    entries = [("nal", "good"), ("ka", "ear")]
    h_pass, h_detail = hist.test_dedr("ā", entries)
    assert h_pass is True and h_detail == "too_short_pass"
    outcome, _detail = v2.test_dedr_v2("ā", entries)
    assert outcome == v2.NOT_RUN


def test_p6_missing_model_character_default_removed():
    bigram_prob = {("a", "b"): 0.5, ("a", "c"): 0.5}
    h_pass, h_detail = hist.test_bigram_consistency("X1", "zū", [], bigram_prob)
    assert h_pass is True and "pass_by_default" in h_detail
    outcome, _detail = v2.test_bigram_consistency_v2("X1", "zū", [], bigram_prob, {})
    assert outcome == v2.NOT_RUN


def test_p7_no_anchor_neighbours_default_removed():
    bigram_prob = {("a", "b"): 1.0}
    seqs = [["X1", "M999"]]  # M999: no anchor record at all
    h_pass, h_detail = hist.test_bigram_consistency("X1", "a", seqs, bigram_prob)
    assert h_pass is True and "pass_by_default" in h_detail
    outcome, _detail = v2.test_bigram_consistency_v2("X1", "a", seqs, bigram_prob, {})
    assert outcome == v2.NOT_RUN


def test_avg_position_input_default_removed():
    # Historical line 110: a missing avg_position is defaulted to
    # 0.5, which satisfies CASE_MARKER_SUFFIX's avg_pos_min — a
    # credit computed on an input that does not exist.
    role = {
        "symbol": "X",
        "semantic_role": "CASE_MARKER_SUFFIX",
        "avg_position": "",
        "is_starter": "False",
        "is_ending": "True",
    }
    h_pass, h_detail = hist.test_positional("X", "ka", role)
    assert h_pass is True and h_detail == "PASS"
    outcome, _detail = v2.test_positional_v2("X", "ka", role)
    assert outcome == v2.NOT_RUN


def test_all_default_sign_earns_no_credit_in_v2():
    # A sign whose every historical pass would be a default:
    # unlisted role (P2), too-short reading (P3), reading char
    # absent from the LM (P6). v2 score is 0; never promoted.
    result = v2.evaluate_sign(
        "X1",
        {"reading": "ā"},
        {"semantic_role": "UNLISTED_ROLE", "avg_position": "0.1"},
        0,
        [],
        {("a", "b"): 1.0},
        [("nal", "good")],
        {},
    )
    assert result["n_pass"] == 0
    assert result["n_not_run"] == 3
    assert result["promote"] is False


# ---------------------------------------------------------------------------
# T301 — genuine checks preserved (historical and v2 agree)


def test_positional_genuine_pass_and_fail_preserved():
    role = {
        "symbol": "X",
        "semantic_role": "CASE_MARKER_SUFFIX",
        "avg_position": "0.60",
        "is_starter": "False",
        "is_ending": "True",
    }
    assert hist.test_positional("X", "ka", role)[0] is True
    assert v2.test_positional_v2("X", "ka", role)[0] == v2.PASS
    role_fail = dict(role, avg_position="0.20")
    assert hist.test_positional("X", "ka", role_fail)[0] is False
    assert v2.test_positional_v2("X", "ka", role_fail)[0] == v2.FAIL


def test_dedr_genuine_pass_and_fail_preserved():
    entries = [("nal", "good"), ("ka", "ear")]
    assert hist.test_dedr("nal", entries) == (True, "exact_match_1")
    assert v2.test_dedr_v2("nal", entries) == (v2.PASS, "exact_match_1")
    assert hist.test_dedr("zzz", entries)[0] is False
    assert v2.test_dedr_v2("zzz", entries)[0] == v2.FAIL


def test_bigram_genuine_pass_preserved():
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    neighbour = next(
        s for s, a in anchors.items() if a.get("confidence") == "HIGH" and a.get("reading")
    )
    neighbour_char = anchors[neighbour]["reading"][0]
    bigram_prob = {("a", neighbour_char): 1.0}
    seqs = [["X1", neighbour]]
    h_pass, h_detail = hist.test_bigram_consistency("X1", "a", seqs, bigram_prob)
    assert h_pass is True and h_detail.startswith("neighbour_match=")
    outcome, detail = v2.test_bigram_consistency_v2(
        "X1", "a", seqs, bigram_prob, anchors
    )
    assert outcome == v2.PASS and detail.startswith("neighbour_match=")


def test_dedr_dataset_not_held_is_not_run_never_a_scan():
    outcome, detail = v2.test_dedr_v2("nal", None)
    assert outcome == v2.NOT_RUN and "not_held" in detail


# ---------------------------------------------------------------------------
# Frozen-input pins (the T104 record's hashes must still hold)


def test_frozen_inputs_match_t104_pins():
    pins = json.loads(T104.read_text("utf-8"))["inputs"]
    for rel, expected in pins.items():
        actual = hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()
        assert actual == expected, f"frozen input changed: {rel}"


# ---------------------------------------------------------------------------
# T302 — the filed dispositions recompute exactly from the run record


def _run_record():
    if not ACTS.is_file() or not RUN_INDEX.is_file():
        return None, None
    acts = json.loads(ACTS.read_text("utf-8"))
    run_id = acts["run_id"]
    record = json.loads((SPEC_RECORDS / f"{run_id}.json").read_text("utf-8"))
    return acts, record


@pytest.fixture(scope="module")
def run_artifacts():
    acts, record = _run_record()
    if acts is None:
        pytest.skip("T302 run artifacts absent — the run has not executed")
    return acts, record


def test_t302_population_census(run_artifacts):
    acts, record = run_artifacts
    audit = json.loads(WP5_AUDIT.read_text("utf-8"))
    records = {r["sign"]: r for r in audit["records"]}
    expected = [
        s
        for s in audit["phase48_summary"]["promoted_signs_in_recorded_order"]
        if records[s]["current_evidential_status"] == "requires_revalidation"
    ]
    assert len(expected) == 28
    assert record["result"]["population"] == expected
    assert [a["sign"] for a in acts["acts"]] == expected
    assert record["result"]["census"]["n_tested"] == 28


def test_t302_dispositions_recompute_exactly(run_artifacts):
    acts, record = run_artifacts
    assert acts["run_id"] == record["run"]["run_id"]
    by_sign = {a["sign"]: a for a in acts["acts"]}
    for entry in record["result"]["results"]:
        act = by_sign[entry["sign"]]
        assert act["from_disposition"] == "requires_revalidation"
        assert act["to_disposition"] == v2.disposition_for(entry)
        assert act["basis"]["run_id"] == record["run"]["run_id"]
        assert act["basis"]["score"] == entry["score"]
        assert act["basis"]["tests"] == entry["tests"]
    retirement = acts["evidence_retirement"]
    assert retirement["scope_signs"] == record["result"]["population"]
    assert retirement["superseded_by_run"] == record["run"]["run_id"]
    census = record["result"]["census"]
    assert census["n_promoted"] + census["n_not_promoted"] == 28
    assert census["by_disposition"] == {
        a["to_disposition"]: sum(
            1 for x in acts["acts"] if x["to_disposition"] == a["to_disposition"]
        )
        for a in acts["acts"]
    }


def test_t302_run_record_validates(run_artifacts):
    _acts, record = run_artifacts
    from glossa_lab import run_records

    run_records.validate_record(record)
    assert record["run"]["surface"] == "study"
    assert record["run"]["determinism_class"] == "deterministic"
