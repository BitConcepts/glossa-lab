"""Spec 091 Stage 3 — site-statistics arm tests (T303).

Fixture side: the lineage table construction (parsing, binning,
site inclusion) and the outcome mapping are proven on synthetic
inputs, including the M176-shaped table whose computed p-value
(about 0.063) is one the historical Phase-69 routine could never
have emitted (it could only ever report p in {0.0, 0.5, 1.0} —
the repair record's summary of the defect this arm corrects).

Real-record side: when the T303 run record + acts file are
present (they are produced by the run), the filed dispositions
are recomputed from the run record's per-anchor checker
results and checked against the acts exactly, the census is
re-derived from the T105 split, and the frozen inputs' hashes
are checked against their pins. When the run artifacts are
absent the real-record tests skip — the stage record states
why.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER_SCRIPT = REPO_ROOT / "backend" / "scripts" / "spec091_stage3_site_stats.py"
SPEC_RECORDS = REPO_ROOT / "specs" / "091-anchor-comparison-integrity" / "records"
ACTS = SPEC_RECORDS / "t303-reclassification-acts.json"
RUN_INDEX = SPEC_RECORDS / "run-index.jsonl"
T105 = SPEC_RECORDS / "t105-checker-arm-split.json"
WP5_AUDIT = REPO_ROOT / "docs" / "repair-2026-10-26" / "anchor-support-audit.json"
ANCHORS = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
PHASE69 = REPO_ROOT / "backend" / "scripts" / "phase69_site_stratification.py"
SITE_STATS = REPO_ROOT / "backend" / "glossa_lab" / "site_stats_v2.py"

FIVE = ["M042", "M046", "M108", "M176", "M342"]

# Frozen-input pins, as they stand at the T303 base (main
# f44cef92). The WP5 audit and anchors pins are the program's
# standing pins (T104/T302 records); the T105 split and the
# lineage script were hashed at this leg's commissioning.
PINS = {
    WP5_AUDIT: "c1382017f44d63e7e811b71b77917d9e3bfb40849f95806987135bae895ea52a",
    ANCHORS: "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
    T105: "ae787ea2148591300b64012164098a5450638d408901f06b1f54e4fd34956347",
    PHASE69: "24ef7c5c2773328e6517dacf2ec19630c20974213b469a7ab5f3ae9e96eef21f",
    SITE_STATS: "1e407232a6592d2d6092e41cc3b4c52fdb75d19f72189ceed70d2cc3e1e4da25",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


arm = _load_module("spec091_stage3_site_stats", RUNNER_SCRIPT)


# ---------------------------------------------------------------------------
# The lineage table construction


def test_binning_matches_the_lineage_rule():
    # SiteB listed first in the dict on purpose: sites come out
    # sorted regardless of insertion order.
    site_inscriptions = {
        "SiteB": [["M042", "M100"], ["M100", "M042", "M100"], ["M042"]],
        "SiteA": [["M100", "M042"]],
    }
    counts = arm.sign_site_counts(site_inscriptions, "M042")
    # SiteB: initial (pos 0 of 2), medial (pos 1 of 3), medial
    # (single-sign inscription falls to the else branch).
    assert counts["SiteB"] == [1, 2, 0]
    # SiteA: terminal (last position of 2).
    assert counts["SiteA"] == [0, 0, 1]
    assert list(counts) == ["SiteA", "SiteB"]


def test_site_inclusion_rule_at_the_boundary():
    counts = {"Low": [1, 1, 0], "Edge": [3, 0, 0], "High": [0, 5, 5]}
    rows, included, excluded = arm.build_table(counts)
    assert included == ["Edge", "High"]
    assert rows == [[3, 0, 0], [0, 5, 5]]
    assert excluded == [{"site": "Low", "counts": [1, 1, 0], "total": 2}]


def test_population_derives_the_five_from_t105():
    population, phonotactic_required, phonotactic_gated, _ = (
        arm.derive_population(REPO_ROOT)
    )
    assert population == FIVE
    assert phonotactic_required == []
    assert phonotactic_gated == []


# ---------------------------------------------------------------------------
# The outcome mapping: every executed arm's disposition


def _checker(status, p_value=None, statistic=None, df=None):
    return {"status": status, "p_value": p_value, "statistic": statistic, "df": df}


def test_difference_detected_maps_to_insufficient_evidence():
    checker = _checker("OK", p_value=0.001)
    assert arm.outcome_kind_for(checker) == "difference_detected"
    assert arm.disposition_for(checker) == "insufficient_evidence"


def test_difference_not_detected_is_not_reearned_support():
    # A non-significant difference test is not evidence of
    # equivalence (the corrected doctrine): the outcome kind
    # records the non-detection, and the disposition is still
    # insufficient_evidence — never a supported class.
    checker = _checker("OK", p_value=0.40)
    assert arm.outcome_kind_for(checker) == "difference_not_detected"
    assert arm.disposition_for(checker) == "insufficient_evidence"


def test_insufficient_data_maps_to_insufficient_evidence():
    checker = _checker("INSUFFICIENT_DATA")
    assert arm.outcome_kind_for(checker) == "insufficient_data"
    assert arm.disposition_for(checker) == "insufficient_evidence"


def test_error_execution_produces_no_disposition():
    checker = _checker("ERROR")
    with pytest.raises(ValueError):
        arm.disposition_for(checker)


def test_checker_computes_a_p_value_the_historical_routine_could_not_emit():
    # The M176-shaped table (the lineage construction over the
    # held corpus): the corrected checker computes p ≈ 0.063.
    # The historical Phase-69 routine could only ever report
    # p ∈ {0.0, 0.5, 1.0}; a computed value strictly between
    # presets is the correction made visible.
    table = [
        [2, 7, 0],
        [2, 14, 3],
        [1, 14, 6],
        [4, 74, 25],
        [0, 22, 3],
        [2, 20, 7],
        [2, 110, 21],
        [0, 12, 3],
    ]
    from glossa_lab.site_stats_v2 import chi_square_independence

    result = chi_square_independence(table).to_dict()
    assert result["status"] == "OK"
    assert result["p_value"] not in (0.0, 0.5, 1.0)
    assert abs(result["p_value"] - 0.0626) < 0.001
    assert arm.outcome_kind_for(result) == "difference_not_detected"


def test_single_column_table_is_insufficient_data_not_a_placeholder():
    # M042's shape: every occurrence in one position bin. The
    # historical routine dressed this case with placeholder
    # numbers (statistic 0.0, p 1.0); the corrected checker
    # returns INSUFFICIENT_DATA with no numbers at all.
    from glossa_lab.site_stats_v2 import chi_square_independence

    result = chi_square_independence([[8, 0, 0], [3, 0, 0]]).to_dict()
    assert result["status"] == "INSUFFICIENT_DATA"
    assert result["statistic"] is None
    assert result["p_value"] is None
    assert arm.outcome_kind_for(result) == "insufficient_data"


# ---------------------------------------------------------------------------
# Frozen-input pins


def test_frozen_inputs_match_their_pins():
    for path, expected in PINS.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"frozen input changed: {path}"


# ---------------------------------------------------------------------------
# T303 — the filed dispositions recompute exactly from the run record


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
        pytest.skip("T303 run artifacts absent — the run has not executed")
    return acts, record


def test_t303_population_census(run_artifacts):
    acts, record = run_artifacts
    split = json.loads(T105.read_text("utf-8"))
    expected = [
        d["sign"]
        for d in split["determinations"]
        if d["determination"]["site_statistics_arm_required"]
    ]
    assert expected == FIVE
    assert record["result"]["population"] == expected
    assert [a["sign"] for a in acts["acts"]] == expected
    assert record["result"]["census"]["n_tested"] == 5


def test_t303_dispositions_recompute_exactly(run_artifacts):
    acts, record = run_artifacts
    assert acts["run_id"] == record["run"]["run_id"]
    audit = json.loads(WP5_AUDIT.read_text("utf-8"))
    audit_records = {r["sign"]: r for r in audit["records"]}
    by_sign = {a["sign"]: a for a in acts["acts"]}
    for entry in record["result"]["results"]:
        act = by_sign[entry["sign"]]
        assert act["from_disposition"] == "requires_revalidation"
        assert audit_records[entry["sign"]][
            "current_evidential_status"
        ] == "requires_revalidation"
        assert entry["outcome_kind"] == arm.outcome_kind_for(entry["checker"])
        assert act["to_disposition"] == arm.disposition_for(entry["checker"])
        assert act["to_disposition"] == entry["to_disposition"]
        assert act["basis"]["run_id"] == record["run"]["run_id"]
        assert act["basis"]["outcome_kind"] == entry["outcome_kind"]
        assert act["basis"]["checker_status"] == entry["checker"]["status"]
        assert act["basis"]["statistic"] == entry["checker"]["statistic"]
        assert act["basis"]["df"] == entry["checker"]["df"]
        assert act["basis"]["p_value"] == entry["checker"]["p_value"]
        assert act["basis"]["table"] == entry["table"]
        assert act["prior_basis"]["disposition_rule"] == entry["disposition_rule"]
    census = record["result"]["census"]
    assert sum(census["by_disposition"].values()) == 5
    assert sum(census["by_outcome_kind"].values()) == 5
    assert census["by_disposition"] == {
        a["to_disposition"]: sum(
            1 for x in acts["acts"] if x["to_disposition"] == a["to_disposition"]
        )
        for a in acts["acts"]
    }


def test_t303_phonotactic_arm_recorded_empty_with_dependency_named(run_artifacts):
    acts, record = run_artifacts
    block = acts["phonotactic_arm"]
    assert block["required_for"] == []
    assert block["gated_dispositions"] == []
    assert "GR-088-04" in block["dependency"]
    assert record["result"]["phonotactic_arm"] == block


def test_t303_run_record_validates(run_artifacts):
    _acts, record = run_artifacts
    from glossa_lab import run_records

    run_records.validate_record(record)
    assert record["run"]["surface"] == "study"
    assert record["run"]["determinism_class"] == "deterministic"
