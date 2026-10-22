"""Build the Spec 029 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/029-tao-claim-lifecycle/build_freeze.py

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
    "experiment_id": "spec029-tao-claim-lifecycle",
    "spec": "specs/029-tao-claim-lifecycle/spec.md",
    "freeze_doc": "specs/029-tao-claim-lifecycle/freeze.md",
    "register": {
        "path": "specs/029-tao-claim-lifecycle/claims.json",
        "register_version": "draft-2",
        "claims": 13,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/029-tao-claim-lifecycle/adjudication.md",
        "decisions": "OD-1..OD-6 ratified as a block 2026-10-12; "
                     "addendum ratifying audit section 9 items "
                     "D-A, D-B, D-D, D-E the same day; D-C excluded "
                     "(executed separately, PR #166)",
        "l3_recovery": "owner-authorized 2026-10-12; PR #167; "
                       "record aee/recovery-specify.md",
    },
    "design": {
        "stage_vocabulary": ["created", "checked", "explained",
                             "accepted", "digested"],
        "automation_cap": "checked",
        "contested_attribution_cap": "checked (OD-3)",
        "digestion_threshold": "OD-5: any one of independent "
                               "reuse, answered published "
                               "challenge, mechanism-engaging "
                               "citation",
        "priority_register": "OD-6: public at intake; claimant, "
                             "timestamp, reading hash; content "
                             "sealed, default reveal 24 months, "
                             "extendable once",
    },
    "inputs": {
        "ledger": "specs/029-tao-claim-lifecycle/"
                  "reclassification-ledger.json",
        "ledger_entries": 345,
        "ledger_stage_totals": {"created": 220, "checked": 116,
                                "explained": 0, "accepted": 0,
                                "digested": 0},
        "verified_unexplained_flags": 105,
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/029-tao-claim-lifecycle/freeze.md",
    "specs/029-tao-claim-lifecycle/spec.md",
    "specs/029-tao-claim-lifecycle/claims.json",
    "specs/029-tao-claim-lifecycle/adjudication.md",
    "specs/029-tao-claim-lifecycle/assessment.md",
    "specs/029-tao-claim-lifecycle/audit.md",
    "specs/029-tao-claim-lifecycle/reclassification-ledger.json",
    "specs/029-tao-claim-lifecycle/plan.md",
    "specs/029-tao-claim-lifecycle/tasks.md",
    "specs/029-tao-claim-lifecycle/build_freeze.py",
    "backend/tests/test_spec029_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/029-tao-claim-lifecycle/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
