"""Build the Spec 032 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/032-pred-2026-006-harappa-breakdown/build_freeze.py

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
    "experiment_id": "spec032-pred-2026-006-harappa-breakdown",
    "spec": "specs/032-pred-2026-006-harappa-breakdown/spec.md",
    "freeze_doc": "specs/032-pred-2026-006-harappa-breakdown/freeze.md",
    "register": {
        "path": "specs/032-pred-2026-006-harappa-breakdown/claims.json",
        "register_version": "0.4-draft",
        "claims": 12,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/032-pred-2026-006-harappa-breakdown/"
                        "adjudication.md",
        "decisions": "owner commission 2026-10-13 ('Design "
                     "experiments for all of the 35 that remain "
                     "in question or inconclusive') produced the "
                     "experiment-design portfolio (draft PR #195), "
                     "whose design D-30 this spec carries without "
                     "deviation; owner order 2026-10-13 06:39 EDT "
                     "('Freeze D-30, D-03, and D-20 for execution') "
                     "adopted the design as written and is the "
                     "adjudicating act for this freeze; execution "
                     "runs after the OSF registration of this "
                     "frozen contract verifies public",
        "register_recovery": "AEE pass rounds 1-3 iterate "
                             "(17, then 4, then 1 failure modes); "
                             "recovered per the Spec 030/031 "
                             "pattern and passed at all three "
                             "phases; record aee/recovery-specify.md",
    },
    "design": {
        "phase": "Phase-396",
        "question_owner": "the PRED register (docs/"
                          "PREDICTION_REGISTER.md): PRED-2026-006, "
                          "registered 2026-04-22; Spec 032 owns "
                          "the scoring design, its freeze, and "
                          "its registration",
        "registered_criterion": {
            "share_min": 0.70,
            "start_rate_bar": 0.40,
            "quantity": "share of the frozen trained INITIAL "
                        "signs whose Harappa start rate is at "
                        "least 0.40, computed on the withheld "
                        "Harappa-site Yajnadevam sequences only",
        },
        "step0": "fails closed: (1) the trained INITIAL set is "
                 "reconstructed from the recorded "
                 "global_class_stability lineage and frozen; "
                 "(2) the withholding is verified as CISI "
                 "Mohenjo-daro only; (3) sign identity is "
                 "carried by the existing crosswalks under "
                 "data/crosswalks, fixed before counting. A "
                 "failed check closes the study as CANNOT BE "
                 "RUN AS WRITTEN",
        "unmappable_rule": "trained signs with no crosswalk "
                           "counterpart are counted and "
                           "reported as UNMAPPABLE; coverage "
                           "above 20 percent of the trained "
                           "set is stated in the verdict's "
                           "first sentence",
        "verdict_mapping": "CONFIRMED at a share of at least "
                           "70 percent; NOT CONFIRMED below "
                           "it; no inconclusive band exists "
                           "in the registered criterion and "
                           "none is invented; step-0 closures "
                           "are reported as themselves, never "
                           "as verdicts",
        "descriptive_addition": "the per-sign table (every "
                                "trained sign, its Harappa "
                                "count, its start rate) is "
                                "published with the outcome; "
                                "descriptive only, carries no "
                                "criterion",
        "register_handling": "the outcome is appended to the "
                             "PRED register as a dated entry "
                             "at execution; the register's "
                             "existing text is never edited",
        "execution_gate": "OSF registration of this frozen "
                          "contract before any execution "
                          "(program precedent pnqrx / 7m35w / "
                          "bge3k / jtwvc); execution follows "
                          "the verified approval under the "
                          "owner's 2026-10-13 order",
    },
    "inputs": {
        "prediction": {
            "id": "PRED-2026-006",
            "registered": "2026-04-22",
            "recorded_outcome": "PARTIALLY CONFIRMED",
            "global_initial_stability": 0.727,
            "register_note": "Harappa-specific breakdown "
                             "pending",
        },
        "yajnadevam_csv": {
            "file": "backend/glossa_lab/data/"
                    "yajnadevam_inscriptions.csv",
            "rows": 5679,
            "sites": 77,
            "harappa_rows": 2717,
        },
        "stability_lineage": [
            "scripts/global_class_stability.py",
            "outputs/analysis/global_class_stability.json",
            "reports/global_class_stability_report.md",
        ],
        "crosswalks": "data/crosswalks/ (Yajnadevam-to-"
                      "Parpola crosswalk files and their "
                      "recorded statistics)",
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/032-pred-2026-006-harappa-breakdown/freeze.md",
    "specs/032-pred-2026-006-harappa-breakdown/spec.md",
    "specs/032-pred-2026-006-harappa-breakdown/claims.json",
    "specs/032-pred-2026-006-harappa-breakdown/adjudication.md",
    "specs/032-pred-2026-006-harappa-breakdown/aee/recovery-specify.md",
    "specs/032-pred-2026-006-harappa-breakdown/aee/freeze-aee-note.md",
    "specs/032-pred-2026-006-harappa-breakdown/build_freeze.py",
    "backend/tests/test_spec032_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/032-pred-2026-006-harappa-breakdown/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
