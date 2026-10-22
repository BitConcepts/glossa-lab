"""Build the Spec 033 freeze record (framework026).

Run from the repo root with the Glossa venv:
    python specs/033-sa-free-language-comparison/build_freeze.py

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
    "experiment_id": "spec033-sa-free-language-comparison",
    "spec": "specs/033-sa-free-language-comparison/spec.md",
    "freeze_doc": "specs/033-sa-free-language-comparison/freeze.md",
    "register": {
        "path": "specs/033-sa-free-language-comparison/claims.json",
        "register_version": "0.4-draft",
        "claims": 15,
        "aee_hook_pass": "pass at after_specify, after_plan, "
                         "after_tasks (0 failure modes, 0 below "
                         "the 0.70 threshold; aee/ artifacts)",
    },
    "basis": {
        "adjudication": "specs/033-sa-free-language-comparison/"
                        "adjudication.md",
        "decisions": "owner commission 2026-10-13 ('Design "
                     "experiments for all of the 35 that remain "
                     "in question or inconclusive') produced the "
                     "experiment-design portfolio (draft PR #195), "
                     "whose design D-03 this spec carries without "
                     "deviation; owner order 2026-10-13 06:39 EDT "
                     "('Freeze D-30, D-03, and D-20 for execution') "
                     "adopted the design as written and is the "
                     "adjudicating act for this freeze; the "
                     "freeze-time estimator fixing the design "
                     "prescribes is recorded in adjudication.md "
                     "section 2 and spec.md section 5; execution "
                     "runs after the OSF registration of this "
                     "frozen contract verifies public",
        "register_recovery": "AEE pass rounds 1-3 iterate "
                             "(9, then 5, then 1 failure modes); "
                             "recovered per the Spec 030/031 "
                             "pattern (one genuine split: the "
                             "SUPPORTED percentile condition "
                             "became F033-C15) and passed at all "
                             "three phases; record "
                             "aee/recovery-specify.md",
    },
    "design": {
        "phase": "Phase-397",
        "question_owner": "the adopted lane-2 record for "
                          "parpola_2010_dravidian_solution_"
                          "manual_001 (owner-adopted explanation "
                          "and not-understood texts, 2026-10-13); "
                          "Spec 033 owns the rerun design, its "
                          "freeze, and its registration",
        "sa_free": "no semantic anchoring, no anchor "
                   "promotion, and no SA-derived quantity "
                   "anywhere in the pipeline (governance H26); "
                   "the Phase-41/43 numbers are the reason for "
                   "the rerun, never an input to it",
        "estimator": "counted conditional distribution of "
                     "each unit given the preceding unit, "
                     "estimated from the corpus itself under "
                     "the family's mapping, add-one (Laplace) "
                     "smoothing; sequence score is its mean log "
                     "probability per sign; family score is the "
                     "mean over all scored sequences; anchor "
                     "signs contribute the phoneme sequences "
                     "their assigned values imply; non-anchor "
                     "strict signs contribute sign identity as "
                     "a single value-free unit; identical "
                     "pipeline for every family and control "
                     "(spec.md section 5)",
        "criteria": {
            "supported_margin_log_units": 0.10,
            "random_percentile": 99,
            "random_controls": 999,
            "supported": "margin AND percentile, both on "
                         "the primary run",
            "not_supported": "a rival at or above "
                             "Dravidian, or Dravidian inside "
                             "the random distribution's "
                             "range",
            "inconclusive": "Dravidian first by less than "
                            "0.10, or the Harappa-removed "
                            "sensitivity reverses the ranking",
        },
        "sensitivity": "Harappa-removed sensitivity "
                       "reported alongside the primary run; "
                       "the verdict rests on the primary "
                       "only; a ranking reversal there is "
                       "the INCONCLUSIVE trigger, declared "
                       "in advance",
        "robustness_arm": "a second pre-registered anchor "
                          "list (the next five published "
                          "candidates per family), run under "
                          "the identical pipeline and "
                          "reported beside the primary result; "
                          "the verdict rests on the primary "
                          "list",
        "status_handling": "the claim's status is "
                           "re-earned under this method or "
                           "replaced by an appended, dated "
                           "entry at execution; the freeze "
                           "changes no status",
        "execution_gate": "OSF registration of this frozen "
                          "contract before any execution "
                          "(program precedent pnqrx / 7m35w / "
                          "bge3k / jtwvc / 3htn8); execution "
                          "follows the verified approval "
                          "under the owner's 2026-10-13 order",
    },
    "inputs": {
        "prior_support": {
            "phase41_ratio": 1.0566,
            "phase43_log_units_per_sign": 0.484,
            "method": "semantic anchoring (SA), falsified "
                      "by Phase-107 (held-out 0.000, "
                      "0 of 115)",
            "record": "docs/ledger-archive.md",
        },
        "anchors_file": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "anchors_total": 287,
            "strict_sa_independent": 94,
        },
        "corpus": "the V3 corpus (the Mahadevan-lineage "
                  "corpus as held in the programme database), "
                  "the same corpus family the Phase-41/43 "
                  "originals used",
        "anchor_values": "published sources only (the DED "
                         "tradition for Dravidian; the "
                         "standard Sanskrit lexicon for "
                         "Indo-Aryan; published Munda "
                         "reconstructions for Munda)",
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend (venv glossa-lab)",
                    "aee": "1.0.4 (Glossa venv, PATH-pinned)",
                    "specify": "1.0.10"},
}

SOURCES = [
    "specs/033-sa-free-language-comparison/freeze.md",
    "specs/033-sa-free-language-comparison/spec.md",
    "specs/033-sa-free-language-comparison/claims.json",
    "specs/033-sa-free-language-comparison/adjudication.md",
    "specs/033-sa-free-language-comparison/aee/recovery-specify.md",
    "specs/033-sa-free-language-comparison/aee/freeze-aee-note.md",
    "specs/033-sa-free-language-comparison/build_freeze.py",
    "backend/tests/test_spec033_freeze.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/033-sa-free-language-comparison/freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
