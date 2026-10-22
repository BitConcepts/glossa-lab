"""Build the Spec 034 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/034-matched-object-attribution/build_freeze.py

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
    "experiment_id": "spec034-matched-object-attribution",
    "spec": "specs/034-matched-object-attribution/spec.md",
    "freeze_doc": "specs/034-matched-object-attribution/freeze.md",
    "register": {
        "path": "specs/034-matched-object-attribution/claims.json",
        "register_version": "0.5-draft",
        "claims": 14,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/034-matched-object-attribution/"
                        "adjudication.md",
        "decisions": "owner commission 2026-10-13 ('Design "
                     "experiments for all of the 35 that remain "
                     "in question or inconclusive') produced the "
                     "experiment-design portfolio (draft PR #195), "
                     "whose design D-20 this spec carries without "
                     "deviation; owner order 2026-10-13 06:39 EDT "
                     "('Freeze D-30, D-03, and D-20 for execution') "
                     "adopted the design as written and is the "
                     "adjudicating act for this freeze; unlike "
                     "Spec 033, this design leaves nothing to "
                     "freeze-time fixing (adjudication.md "
                     "section 2); execution runs after the OSF "
                     "registration of this frozen contract "
                     "verifies public",
        "register_recovery": "AEE pass rounds 1-4 iterate "
                             "(12, then 4, then 1, then 1 "
                             "failure modes); recovered per the "
                             "Spec 030/031 pattern (atomic "
                             "rewrites, boundary transfers, "
                             "definitional verdict lines) and "
                             "passed at all three phases; record "
                             "aee/recovery-specify.md",
    },
    "design": {
        "phase": "Phase-398",
        "question_owner": "the settled STUDY-SPEC-019/"
                          "PHASE-125 record (FAIL - "
                          "DISAGREEMENT); Spec 034 owns the "
                          "attribution design, its freeze, and "
                          "its registration; the settled "
                          "verdict is an input, never a question",
        "step0_bridge": "object pairs built through three "
                        "routes, every pair cited data: (a) "
                        "the CISI catalogue layer (7,705 rows, "
                        "Phases 120-124); (b) Mahadevan-side "
                        "published object references through "
                        "the Phase-130 intake schema; (c) the "
                        "44 Phase-128 evidence dossiers",
        "gate": {
            "matched_objects_min": 150,
            "min_signs_each_compilation": 3,
            "below_gate_closure": "TOO THIN TO ATTRIBUTE, "
                                  "with the bridge census "
                                  "published as the finding",
        },
        "prohibited_join": "Holdat cisi_number is never a "
                           "join key (Phase-131: internal "
                           "sequential numbering, not a CISI "
                           "object ID; join rejected as "
                           "non-identity)",
        "method": "per-sign positional profiles on the "
                  "matched subset only, Phase-125's own "
                  "distance (total variation) and count "
                  "floors; decomposition in Phase-131's own "
                  "categories (segmentation / substitution, "
                  "checked against the crosswalk's conflict "
                  "pairs / composition residue); per-object "
                  "distances reported as a distribution",
        "criteria": {
            "composition_line": 0.20,
            "transcription_line": 0.32,
            "middle": "split attribution, with the "
                      "decomposition table as the result",
            "quantity": "the matched-object median "
                        "distance under the frozen method",
        },
        "selection_bias": "the matched subset's site and "
                          "object-type mix is reported "
                          "against both compilations' full "
                          "mixes, and the verdict statement "
                          "carries the subset's description",
        "crosswalk_posture": "a record of disagreement, "
                             "never ground truth (762 pairs, "
                             "383 conflict pairs)",
        "execution_gate": "OSF registration of this frozen "
                          "contract before any execution "
                          "(program precedent pnqrx / 7m35w / "
                          "bge3k / jtwvc / 3htn8); execution "
                          "follows the verified approval "
                          "under the owner's 2026-10-13 order",
    },
    "inputs": {
        "phase125": {
            "record": "reports/"
                      "phase125_cross_compilation_summary.md",
            "pairs": 286,
            "judgeable": 16,
            "median_tv": 0.636931,
            "verdict": "FAIL - DISAGREEMENT (settled)",
        },
        "phase127_noise_median": 0.083,
        "phase131": {
            "record": "reports/phase131_attribution.md",
            "attributed_share": 0.061,
            "shared_artifact_keys": 0,
        },
        "phase124_catalogue_rows": 7705,
        "phase128_dossiers": 44,
        "crosswalk": {"pairs": 762, "conflict_pairs": 383},
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/034-matched-object-attribution/freeze.md",
    "specs/034-matched-object-attribution/spec.md",
    "specs/034-matched-object-attribution/claims.json",
    "specs/034-matched-object-attribution/adjudication.md",
    "specs/034-matched-object-attribution/aee/recovery-specify.md",
    "specs/034-matched-object-attribution/aee/freeze-aee-note.md",
    "specs/034-matched-object-attribution/build_freeze.py",
    "backend/tests/test_spec034_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/034-matched-object-attribution/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
