"""Build the Spec 030 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/030-q6-chronology-spine-extension/build_freeze.py

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
    "experiment_id": "spec030-q6-chronology-spine-extension",
    "spec": "specs/030-q6-chronology-spine-extension/spec.md",
    "freeze_doc": "specs/030-q6-chronology-spine-extension/freeze.md",
    "register": {
        "path": "specs/030-q6-chronology-spine-extension/claims.json",
        "register_version": "0.2-draft",
        "claims": 7,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/030-q6-chronology-spine-extension/"
                        "adjudication.md",
        "decisions": "owner instruction 'Freeze it' 2026-10-12; "
                     "section 9 Asks 1, 3, 4, 5 adopted as proposed; "
                     "Ask 2 expressly NOT covered (no recommendation "
                     "stated in the design; bindingness of the "
                     "CONTESTED sensitivity reserved to a future Q6 "
                     "freeze adjudication)",
        "register_recovery": "freeze AEE pass round 1 iterate "
                             "(11 failure modes); recovered per the "
                             "Spec 028 pattern and re-passed; record "
                             "aee/recovery-specify.md",
    },
    "design": {
        "phase": "Phase-394",
        "criteria_source": "specs/027-movement-culture-language/"
                           "stage0-freeze.md section 4 (verbatim; "
                           "thresholds, 5250-3850 BP window, grade "
                           "and material vocabularies unchanged)",
        "routes_order": ["R5", "R1", "R2", "R4", "R3"],
        "tracing_order": "short-lived-first (adopted Ask 3); full "
                         "pool reported; no traced row excluded",
        "coordinate_less_rows": "admitted for gazetteer-established "
                                "sites; coordinate state "
                                "inherited-from-cluster (adopted "
                                "Ask 1; integrity rule 7)",
        "r3_posture": "open_access_read_only; internal-spine-only; "
                      "never in any CC BY release package (adopted "
                      "Ask 4; F030-C06)",
        "retest": "stage0-freeze.md section 4 assessment verbatim; "
                  "margins only; outcomes SUPPORTED-FOR-FREEZE-DESIGN "
                  "or NOT-YET-TESTABLE; negative extension outcome "
                  "is a valid closure (F030-C07)",
        "contested_sensitivity": "reported per criterion (integrity "
                                 "rule 5); bindingness NOT decided "
                                 "(Ask 2 not covered)",
        "execution_gate": "OSF registration of this frozen contract "
                          "before any execution (adopted Ask 5); "
                          "prescribed, not performed, by this freeze",
    },
    "inputs": {
        "stage0_results": "reports/phase391_results.json",
        "q6_timing_support": {
            "status": "NOT-YET-TESTABLE",
            "c1_regions_with_2plus_sites": {"value": 1,
                                            "threshold": 3,
                                            "pass": False},
            "c2_window_sites_direct_or_associated": {"value": 5,
                                                     "threshold": 10,
                                                     "pass": False},
            "c3_window_short_lived_share": {"value": 0.0,
                                            "threshold": 0.5,
                                            "pass": False},
            "c4_window_median_std_bp": {"value": 70,
                                        "threshold": 80,
                                        "pass": True},
            "window_rows_direct_or_associated": 31,
        },
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/030-q6-chronology-spine-extension/freeze.md",
    "specs/030-q6-chronology-spine-extension/spec.md",
    "specs/030-q6-chronology-spine-extension/claims.json",
    "specs/030-q6-chronology-spine-extension/adjudication.md",
    "specs/030-q6-chronology-spine-extension/aee/recovery-specify.md",
    "specs/030-q6-chronology-spine-extension/aee/freeze-aee-note.md",
    "specs/030-q6-chronology-spine-extension/build_freeze.py",
    "backend/tests/test_spec030_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/030-q6-chronology-spine-extension/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
