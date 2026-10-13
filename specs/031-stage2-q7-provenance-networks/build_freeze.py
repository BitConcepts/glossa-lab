"""Build the Spec 031 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/031-stage2-q7-provenance-networks/build_freeze.py

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
    "experiment_id": "spec031-stage2-q7-provenance-networks",
    "spec": "specs/031-stage2-q7-provenance-networks/spec.md",
    "freeze_doc": "specs/031-stage2-q7-provenance-networks/freeze.md",
    "register": {
        "path": "specs/031-stage2-q7-provenance-networks/claims.json",
        "register_version": "0.3-draft",
        "claims": 12,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/031-stage2-q7-provenance-networks/"
                        "adjudication.md",
        "decisions": "owner instruction 'Freeze it' 2026-10-12 "
                     "adopted the Stage 2 / Q7 packet's asks as a "
                     "block (1B, 2B, 3A, 4A, 5A, 6A; confirmed "
                     "'correct, do it' 2026-10-12); owner order "
                     "2026-10-13 commissioned this design and its "
                     "freeze; execution not ordered",
        "register_recovery": "AEE pass rounds 1-2 iterate "
                             "(5 then 4 failure modes); recovered "
                             "per the Spec 030 pattern and passed "
                             "at all three phases; record "
                             "aee/recovery-specify.md",
    },
    "design": {
        "phase": "Phase-395",
        "question_owner": "Spec 027 section 8.1 (claim "
                          "F027-C15); Spec 031 owns the Stage 2 "
                          "design, its freeze, and its "
                          "registration",
        "link_tiers": "primary = Law (2011) determinations by a "
                      "named instrumental method only; "
                      "sensitivity = Law Chapter 4 reference-based "
                      "assignments, separately labelled, never "
                      "pooled, carries no verdict (adopted 2B)",
        "meluhha": "contributes no site-pair links under any "
                   "posture (catalogue_only; its 76 citations "
                   "name a region, never an Indus site)",
        "arms": "ceramic and bead/craft, each computed on its "
                "own eligible site set, never pooled (adopted "
                "3A)",
        "support_rules": {
            "site_link_eligible_min_primary_determinations": 3,
            "ceramic_site_min_classified_items": 20,
            "bead_site_min_classified_beads": 10,
            "arm_min_eligible_sites": 8,
            "arm_min_linked_pairs": 10,
        },
        "estimand": "MRM/MRQAP (double semi-partialling) partial "
                    "R^2 of the binary shared-source indicator "
                    "net of geographic distance, river-network "
                    "distance, pair sample size, and publication "
                    "intensity",
        "practical_margin_partial_r2": 0.02,
        "permutations": 9999,
        "bootstrap_replicates": 9999,
        "seed": 20261013,
        "controls": "R = 199 synthetic replicates of the "
                    "identical pipeline per arm; negative control "
                    "PASS iff the SUPPORTED rule fires in <= 5% "
                    "of replicates; positive control (planted "
                    "partial R^2 ~ 0.04) PASS iff >= 95%; a "
                    "non-discriminating control makes the run "
                    "INVALID",
        "ceramic_arm": "conditionally estimable (DD-7): closes "
                       "NOT ESTIMABLE at the execution margins "
                       "step if sources at audited postures "
                       "cannot evidence >= 8 eligible ceramic "
                       "sites; no ceramic response is computed "
                       "in that case",
        "declared_untestable": [
            "sub-period-resolution variants (adopted 4A)",
            "a visual-tier primary test (adopted 2B)",
            "dose-response as a verdict-bearing test "
            "(labelled sensitivity only)",
        ],
        "execution_gate": "OSF registration of this frozen "
                          "contract before any execution "
                          "(adopted 6A); execution itself is "
                          "not ordered by this freeze",
    },
    "inputs": {
        "d8_audit": "specs/027-movement-culture-language/"
                    "stage2-d8-audit.md",
        "law_determinations": {"harappa": ">2100",
                                "other_sites_combined": "~120",
                                "single_site_concentration": "~95%"},
        "meluhha_citations": 76,
        "gazetteer": {"file": "data/movement/gazetteer_rows.jsonl",
                      "rows": 36,
                      "program_sites": 30,
                      "verified_open_rows": 21,
                      "open_access_read_only_rows": 15},
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/031-stage2-q7-provenance-networks/freeze.md",
    "specs/031-stage2-q7-provenance-networks/spec.md",
    "specs/031-stage2-q7-provenance-networks/claims.json",
    "specs/031-stage2-q7-provenance-networks/adjudication.md",
    "specs/031-stage2-q7-provenance-networks/aee/recovery-specify.md",
    "specs/031-stage2-q7-provenance-networks/aee/freeze-aee-note.md",
    "specs/031-stage2-q7-provenance-networks/build_freeze.py",
    "backend/tests/test_spec031_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/031-stage2-q7-provenance-networks/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
