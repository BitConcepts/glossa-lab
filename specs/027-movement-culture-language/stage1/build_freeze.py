"""Build the Spec 027 Stage 1 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/027-movement-culture-language/stage1/build_freeze.py

Writes stage1-freeze.json next to stage1-freeze.md. A freeze
is never regenerated over a run (Spec 026 section 4.7).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze  # noqa: E402

DEFINITION = {
    "experiment_id": "spec027-phase392-q2-gate",
    "spec": "specs/027-movement-culture-language/spec.md",
    "freeze_doc": "specs/027-movement-culture-language/stage1-freeze.md",
    "script": "backend/scripts/phase392_q2_gate.py (created at execution)",
    "graph_module": "backend/glossa_lab/experiment_graph_phase391_392.py",
    "phase": 392,
    "estimand": {
        "response": "per-inscription M77 sign composition "
                    "(proportions, Bray-Curtis)",
        "grouping": "site (6 analysis sites)",
        "statistic": "PERMANOVA R^2 for site, rarefaction-averaged",
        "margin_r2": 0.01,
    },
    "design": {
        "sign_list_version": "M77 (governing; Ask 2)",
        "eligible_records": 3144,
        "analysis_sites": ["Harappa", "Mohenjo-daro", "Dholavira",
                           "Lothal", "Chanhu-daro", "Kalibangan"],
        "analysis_records": 3030,
        "sign_columns": 125,
        "n_cell_rarefaction": 15,
        "rarefaction_draws": 199,
        "permutations_per_draw": 499,
        "permutation_strata": "object type class (SEAL/TAB)",
        "seed": 20261011,
        "alpha": 0.05,
        "loso_sites": 6,
        "parpola_sensitivity": "NOT ESTIMABLE at the frozen rule "
                               "(margins: 17.57% unambiguous "
                               "coverage); not run",
    },
    "inputs": {
        "store": "corpora/downloads/spec027_stage1/ (gitignored)",
        "sha256": {
            "icit_converted_v2_keyed.json":
                "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
            "horus_inscriptions.csv":
                "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
            "parpola_mahadevan_crosswalk_v1.csv":
                "3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823",
        },
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend/scripts (venv glossa-lab)"},
}

SOURCES = [
    "specs/027-movement-culture-language/stage1-freeze.md",
    "specs/027-movement-culture-language/adjudication.md",
    "specs/027-movement-culture-language/spec.md",
    "specs/027-movement-culture-language/stage1/build_margins_audit.py",
    "specs/027-movement-culture-language/stage1/margins-audit.json",
    "data/crosswalks/parpola_mahadevan_crosswalk_v1.csv",
    "backend/tests/test_phase392_stage1_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/027-movement-culture-language/stage1-freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
