#!/usr/bin/env python3
"""Phase-119 (spec 018) PRED-2026 readiness harness — phase script.

Runs the fixture self-checks and the spec section 8 dry run
on the Phase-115 expanded ICIT converted layer
(class icit_lineage_derivative: clearly non-independent),
and writes reports/phase119_pred_harness_results.json +
reports/phase119_acquisition_log.json.

NO prediction is evaluated: the layer's class does not
qualify for any PRED-2026 item (spec section 4), and the
dry-run code path cannot compute a criterion statistic
(spec section 8). The dry-run numbers are asserted against
spec Appendix A; a mismatch exits nonzero.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.gpu_utils import detect_device  # noqa: E402
from glossa_lab.pred_harness import (  # noqa: E402
    DRY_RUN_LABEL, PREDICTIONS, NotEvaluable, Prediction,
    SignMapper, adapt_converted_layer, adapt_future_concordance,
    adapt_rmrl_concordance, build_sign_maps, dry_run, evaluate,
    load_sign_classes,
)

FIXTURES = REPO / "backend" / "tests" / "fixtures" / "pred_harness"
REPORTS = REPO / "reports"
MAIN_DL = Path.home() / "workspace" / "glossa-lab" / "corpora" / "downloads"

# Spec Appendix A expectations (frozen design-stage numbers).
EXPECTED_DEDUP = {"input": 4531, "stage_a_removed": 1468,
                  "stage_b_removed": 370, "stage_c_removed": 247,
                  "kept": 2446}
EXPECTED_TERM = {"P020": 19, "P076": 0, "P095": 49, "P099": 31,
                 "P108": 21, "P125": 0, "P210": 42, "P226": 10,
                 "P256": 70, "P346": 26, "P359": 11, "P378": 229,
                 "P384": 11, "P385": 397}
EXPECTED_INIT = {"P000": 0, "P001": 89, "P004": 157, "P013": 156,
                 "P051": 41, "P098": 304, "P217": 242, "P238": 14,
                 "P265": 23, "P301": 66, "P310": 555, "P324": 1413}
EXPECTED_MED_ATTESTED = 38
EXPECTED_CLASSIFIABLE_PRE = 2544
EXPECTED_CLASSIFIABLE_POST = 1045

TOY_PRED = Prediction(
    pid="PRED-TOY-001", kind="rate", rate="start", threshold=0.5,
    pass_count=2, sign_set=("P001", "P004"),
    prediction_text="toy prediction (self-check only)",
    criterion_text="toy criterion (self-check only)")


def layer_path() -> Path:
    for cand in (REPO / "corpora" / "downloads",
                 MAIN_DL):
        p = cand / "icit_fieldcady" / "icit_converted_v2.json"
        if p.exists():
            return p
    raise FileNotFoundError("icit_converted_v2.json not found in "
                            "worktree or main checkout downloads")


def self_checks(mapper, classes) -> dict:
    """Fixture self-checks through the real gating/scoring
    code: both toy verdict directions, the real PRED-2026-003
    scorer on toy fixtures, and the section 4 gate refusing
    the non-independent layer class."""
    out = {}
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_confirmed.csv",
                                mapper, "self-check", "synthetic",
                                "fixture")
    out["toy_rate_confirmed"] = evaluate(
        TOY_PRED, ds, classes, set())["verdict"]
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_refuted.csv",
                                mapper, "self-check", "synthetic",
                                "fixture")
    out["toy_rate_refuted"] = evaluate(
        TOY_PRED, ds, classes, set())["verdict"]
    ds = adapt_future_concordance(FIXTURES / "toy_future_confirmed.json",
                                  mapper, "self-check", "synthetic",
                                  "fixture")
    out["toy_template_confirmed"] = evaluate(
        PREDICTIONS["PRED-2026-003"], ds, classes, set())["verdict"]
    ds = adapt_future_concordance(FIXTURES / "toy_future_refuted.json",
                                  mapper, "self-check", "synthetic",
                                  "fixture")
    out["toy_template_refuted"] = evaluate(
        PREDICTIONS["PRED-2026-003"], ds, classes, set())["verdict"]
    layer = adapt_converted_layer(FIXTURES / "toy_layer.json",
                                  mapper, "self-check")
    try:
        evaluate(PREDICTIONS["PRED-2026-001"], layer, classes, set())
        out["gate_refuses_lineage"] = False
    except NotEvaluable:
        out["gate_refuses_lineage"] = True
    expected = {"toy_rate_confirmed": "CONFIRMED",
                "toy_rate_refuted": "REFUTED",
                "toy_template_confirmed": "CONFIRMED",
                "toy_template_refuted": "REFUTED",
                "gate_refuses_lineage": True}
    if out != expected:
        raise AssertionError(f"self-check mismatch: {out} != {expected}")
    return out


def main() -> int:
    classes = load_sign_classes(
        REPO / "data" / "crosswalks" / "sign_inventory.csv")
    mapper = SignMapper(build_sign_maps(
        REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"))

    checks = self_checks(mapper, classes)

    layer = adapt_converted_layer(layer_path(), mapper,
                                  "icit_converted_v2 (Phase-115 layer)")
    report_dry = dry_run(layer, classes)

    cov_pre = report_dry["coverage_pre_dedup"]
    cov_post = report_dry["coverage_post_dedup"]
    reproduction = {
        "dedup": report_dry["dedup"] == EXPECTED_DEDUP,
        "term_per_sign": cov_pre["TERMINAL"]["per_sign_occurrences"]
        == EXPECTED_TERM,
        "init_per_sign": cov_pre["INITIAL"]["per_sign_occurrences"]
        == EXPECTED_INIT,
        "med_attested": cov_pre["MEDIAL"]["attested"]
        == EXPECTED_MED_ATTESTED,
        "classifiable_pre": cov_pre["classifiability"]
        ["all_signs_labelled"] == EXPECTED_CLASSIFIABLE_PRE,
        "classifiable_post": cov_post["classifiability"]
        ["all_signs_labelled"] == EXPECTED_CLASSIFIABLE_POST,
    }
    if not all(reproduction.values()):
        print(f"APPENDIX A REPRODUCTION FAILED: {reproduction}",
              file=sys.stderr)
        return 1

    results = {
        "phase": 119,
        "spec": "018-phase119-pred2026-readiness",
        "date": "2026-10-07",
        "label": DRY_RUN_LABEL,
        "gpu_device": detect_device(),
        "harness_self_checks": checks,
        "appendix_a_reproduction": reproduction,
        "dry_run": report_dry,
        "verdicts": {},
        "note": "No PRED-2026 prediction was evaluated. The "
                "only dataset ingested is of class "
                "icit_lineage_derivative, which qualifies for "
                "no prediction (spec section 4); it was "
                "exercised in dry-run mode only (spec section 8).",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "phase119_pred_harness_results.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False),
        encoding="utf-8")

    acq = {
        "date": "2026-10-07",
        "ingested": [],
        "dry_run_only": [
            {**layer.provenance,
             "as_built": layer.stats,
             "note": "Phase-115 expanded ICIT converted layer; "
                     "class icit_lineage_derivative "
                     "(derivation-adjacent); exercised under "
                     "the spec section 8 dry-run rule only."},
        ],
        "found_but_not_obtainable": [
            {"name": "RMRL concordance export (Indus Research "
                     "Centre, Roja Muthiah Research Library)",
             "status": "GAP — not yet acquired; owner-sent "
                       "request pending (access workstream). "
                       "Class rmrl_concordance would qualify "
                       "for PRED-2026-001..003.",
             "license": "research use — contact required"},
            {"name": "Dixit–Mitra image-derived transcription "
                     "table",
             "status": "GAP — dataset not publicly deposited; "
                       "owner-sent request drafted. Class "
                       "image_transcription would qualify for "
                       "PRED-2026-001..003.",
             "license": "not deposited; no data-availability "
                        "statement in the article"},
            {"name": "Mahadevan Chair expanded concordance",
             "status": "GAP — future compilation, not yet "
                       "published. Class future_concordance "
                       "would qualify for PRED-2026-001..003.",
             "license": "not yet published"},
        ],
    }
    (REPORTS / "phase119_acquisition_log.json").write_text(
        json.dumps(acq, indent=1, ensure_ascii=False),
        encoding="utf-8")
    print(json.dumps({"self_checks": checks,
                      "appendix_a_reproduction": reproduction,
                      "dedup": report_dry["dedup"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
