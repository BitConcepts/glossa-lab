#!/usr/bin/env python3
"""Phase-130 (spec 021) independent-data intake pack — phase script.

Runs the synthetic fixture dataset (invented signs/sites, no
real corpus data) end-to-end through the intake runbook
(docs/INTAKE_RUNBOOK.md): provenance/license gate -> schema
validation -> shared dedup -> evaluability-class assignment
-> Phase-119 harness DRY-RUN only. Also runs the
license-missing variant fixture (must reject at the license
gate) and writes reports/phase130_intake_pack_results.json.

NO real dataset is ingested, NO prediction is evaluated:
the intake pipeline cannot reach the harness scoring path
(spec 021 section 5).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.gpu_utils import detect_device  # noqa: E402
from glossa_lab.intake import run_intake  # noqa: E402
from glossa_lab.pred_harness import load_sign_classes  # noqa: E402

FIXTURES = REPO / "backend" / "tests" / "fixtures" / "intake"
REPORTS = REPO / "reports"
INVENTORY = REPO / "data" / "crosswalks" / "sign_inventory.csv"

EXPECTED_DEDUP = {"input": 7, "stage_a_removed": 1,
                  "stage_b_removed": 1, "stage_c_removed": 1,
                  "kept": 4}


def main() -> int:
    classes = load_sign_classes(INVENTORY)
    fixture = json.loads(
        (FIXTURES / "synthetic_dataset.json").read_text("utf-8"))
    report = run_intake(fixture, classes)
    assert report["outcome"] == "intake-complete-dry-run-only", report
    assert report["stages"]["dedup"] == EXPECTED_DEDUP, report["stages"]
    assert report["stages"]["license_gate"] == "pass"
    no_license = json.loads(
        (FIXTURES / "synthetic_dataset_no_license.json").read_text("utf-8"))
    rejected = run_intake(no_license, classes)
    assert rejected["outcome"] == "rejected", rejected
    assert rejected["stages"]["license_gate"] == "reject"
    out = {
        "phase": "Phase-130 (spec 021) intake pack",
        "label": report["label"],
        "synthetic_fixture": report,
        "no_license_variant_outcome": rejected["outcome"],
        "no_license_variant_errors": rejected["stages"]["validation"]["errors"],
        "gpu_device": detect_device(),
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "phase130_intake_pack_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print("intake fixture:", report["outcome"],
          "| dedup:", report["stages"]["dedup"],
          "| no-license variant:", rejected["outcome"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
