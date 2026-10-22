"""Build the Spec 028 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/028-harappa-robustness/build_freeze.py

Writes freeze.json next to freeze.md. A freeze is never
regenerated over a run (Spec 026 section 4.7).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze

DEFINITION = {
    "experiment_id": "spec028-phase393-harappa-robustness",
    "spec": "specs/028-harappa-robustness/spec.md",
    "freeze_doc": "specs/028-harappa-robustness/freeze.md",
    "script": "backend/scripts/phase393_harappa_robustness.py "
              "(created at execution)",
    "graph_module": "backend/glossa_lab/experiment_graph_phase393.py",
    "phase": 393,
    "estimand": {
        "response": "per-inscription M77 sign composition "
                    "(proportions, Bray-Curtis)",
        "grouping": "site (Arm A: 5 non-Harappa sites; "
                    "Arm B: 6 sites, equal-weight)",
        "statistic": "adjusted PERMANOVA R^2 for site, "
                     "rarefaction-averaged",
        "margin_r2": 0.01,
    },
    "design": {
        "sign_list_version": "M77 (governing; inherited from "
                             "Spec 027 Ask 2)",
        "eligible_records": 3144,
        "analysis_records": 3030,
        "analysis_sites": ["Harappa", "Mohenjo-daro", "Dholavira",
                           "Lothal", "Chanhu-daro", "Kalibangan"],
        "sign_columns": 125,
        "seed": 20261012,
        "rarefaction_draws": 199,
        "permutations_per_draw": 499,
        "permutation_strata": "object type class x legible-length "
                               "value (Amendment 1)",
        "arm_a": {
            "role": "confirmatory, primary",
            "population": "analysis population minus Harappa",
            "records": 1593,
            "n_cell_rarefaction": 49,
            "cells_included": 6,
            "inscriptions_per_draw": 294,
            "loso_sites": 5,
            "sensitivity": "S-complete (labelled, no verdict)",
        },
        "arm_b": {
            "role": "confirmatory, secondary",
            "population": "full analysis population",
            "records": 3030,
            "quota_per_site": 52,
            "inscriptions_per_draw": 312,
            "allocation_rule": "largest-remainder proportional "
                               "over the site's type-class counts; "
                               "ties by type-class name ascending; "
                               "caps reassigned in the same order",
            "loso_sites": 6,
            "sensitivity": "none (frozen design decision)",
        },
        "arm_c": {
            "role": "exploratory, descriptive only (no verdict, "
                    "no p-values, no margin rule)",
            "population": "Harappa analysis records (1437)",
        },
        "controls": "per arm: negative (pooled composition) and "
                    "positive (deterministic planted sets, x3), "
                    "identical arm pipeline, synthetic population "
                    "REGENERATED PER DRAW (Amendment 1); failure "
                    "= that arm INVALID",
        "multiplicity": "hierarchical: Arm A primary; Arm B a "
                        "separate secondary bounded claim; no "
                        "pooled cross-arm headline",
    },
    "inputs": {
        "store": "corpora/downloads/spec028_harappa/ (gitignored)",
        "sha256": {
            "icit_converted_v2_keyed.json":
                "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
            "horus_inscriptions.csv":
                "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
        },
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend/scripts (venv glossa-lab)"},
}

SOURCES = [
    "specs/028-harappa-robustness/freeze.md",
    "specs/028-harappa-robustness/adjudication.md",
    "specs/028-harappa-robustness/spec.md",
    "specs/028-harappa-robustness/claims.json",
    "specs/028-harappa-robustness/build_margins_audit.py",
    "specs/028-harappa-robustness/margins-audit.json",
    "specs/028-harappa-robustness/pipeline393.py",
    "specs/028-harappa-robustness/build_calibration.py",
    "specs/028-harappa-robustness/calibration.json",
    "specs/028-harappa-robustness/build_freeze.py",
    "backend/tests/test_phase393_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/028-harappa-robustness/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
