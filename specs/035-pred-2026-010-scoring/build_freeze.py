#!/usr/bin/env python3
"""Build the Spec 035 freeze record (freeze.json).

This builder computed the DRAFT digest over the draft
contract under the owner's draft order of 2026-10-20
(adjudication.md), and the final digest over the
frozen contract at the freeze act of the same day
(the owner's freeze-and-execute order), after the
AEE lifecycle hooks passed over the recovered
register. Run with the Glossa backend venv python
from the repository root:

    python specs/035-pred-2026-010-scoring/build_freeze.py

Writes specs/035-pred-2026-010-scoring/freeze.json
(framework026 build_freeze payload: definition +
source hashes + environment, digest = SHA-256 of
the canonical JSON serialisation) and prints the
digest.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze  # noqa: E402

SPEC_DIR = "specs/035-pred-2026-010-scoring"

DEFINITION = {
    "spec": "specs/035-pred-2026-010-scoring/spec.md",
    "freeze_doc": "specs/035-pred-2026-010-scoring/freeze.md",
    "experiment_id": "spec035-pred-2026-010-scoring",
    "register": {
        "path": "specs/035-pred-2026-010-scoring/claims.json",
        "register_version": "0.8-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASS at the freeze act (2026-10-20): "
            "after_specify pass over register 0.8-draft "
            "after four rounds (30, then 9, then 8 failure "
            "modes, then 0; recovery-specify.md), "
            "after_plan pass and after_tasks pass on the "
            "recovered register; 0 claims below the 0.70 "
            "threshold at every pass (see "
            "specs/035-pred-2026-010-scoring/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/035-pred-2026-010-scoring/adjudication.md"
        ),
        "decisions": (
            "The owner's freeze-and-execute order of "
            "2026-10-20 (go with your recommendation) "
            "freezes this contract and orders Phase-399 "
            "execution; the draft was commissioned by the "
            "owner's draft order of the same day. DD-035-2 "
            "stands as drafted; DD-035-4 is decided: the "
            "frozen spec files its own OSF contract "
            "registration (the Spec 032-034 pattern). The "
            "contract implemented is the PRED-2026-010 "
            "registration (docs/PREDICTION_REGISTER.md, "
            "registered 2026-10-13) with its derivation "
            "record (reports/pred010_derivation_record.json)."
        ),
    },
    "design": {
        "phase": "Phase-399",
        "question_owner": (
            "docs/PREDICTION_REGISTER.md PRED-2026-010 (H3 "
            "successor: cross-site class preservation, clean "
            "withholding)"
        ),
        "registered_prediction": (
            "Signs assigned to the INITIAL class in training "
            "on CISI Mohenjo-daro inscriptions ONLY will "
            "appear preferentially in initial position in "
            "Harappa-specific Yajnadevam data as well."
        ),
        "trained_initial_set": ["P000", "P217", "P324"],
        "criterion": {
            "share_min": 0.7,
            "start_rate_min": 0.4,
            "trained_signs": 3,
            "pass_structure": (
                "with 3 trained signs the share can only be "
                "0, 1/3, 2/3, or 1; the 70% bar passes only "
                "at 3 of 3"
            ),
        },
        "step0": {
            "order": [
                "registration re-verification (OSF wjebq "
                "accepted + public)",
                "input integrity (the registered SHA-256 "
                "pins)",
                "training-pool re-verification (registered "
                "filter; 179 rows, all Mohenjo-daro, zero "
                "Yajnadevam; manifest hash; the verbatim "
                "classification reproducing {P000, P217, "
                "P324} exactly)",
                "crosswalk coverage (the unmappable cap, "
                "under the fixed best-match reading)",
            ],
            "failure_closure": (
                "CANNOT BE RUN AS WRITTEN, unscored, "
                "reported as a closure and never as a "
                "verdict; the withheld file's content is "
                "opened only after all checks pass"
            ),
        },
        "crosswalk_reading": (
            "the frozen Phase-396 build's fix_crosswalk "
            "reading: a trained sign's counterparts are the "
            "glyphs whose crosswalk row names it as "
            "best_parpola_match; top3_parpola alternatives "
            "never create a counterpart and set the "
            "conflict flag instead (DD-035-5)"
        ),
        "draft_stage_coverage_observation": (
            "under that reading on the pinned crosswalk: "
            "P217 -> glyph Y0520 (confidence 1.0, "
            "confirmed); P324 -> glyph Y0740 (confidence "
            "0.9867, confirmed); P000 has no best-match "
            "counterpart (top-3 alternative only, on the "
            "rows for Y0527, Y0740, Y0820, Y0892) - step 0 "
            "check 0.4 is therefore expected to close the "
            "study as CANNOT BE RUN AS WRITTEN, unscored; "
            "the formal determination remains a step-0 act"
        ),
        "unmappable": {
            "cap": 0.2,
            "one_sign_share": "1/3 (33%)",
            "over_cap_closure": (
                "CANNOT BE RUN AS WRITTEN before the "
                "withheld file is opened"
            ),
        },
        "method": (
            "positional classification only (SA-free): "
            "for each trained sign, through the frozen "
            "crosswalk, its start rate at Harappa is the "
            "share of its Harappa occurrences in the "
            "withheld sequences in which it stands in "
            "initial position (the first sign of a "
            "sequence); a mappable trained sign with zero "
            "Harappa occurrences counts as not meeting the "
            "bar (DD-035-2); the per-sign table is "
            "published descriptively and carries no "
            "criterion"
        ),
        "disclosure": (
            "the Yajnadevam Harappa pool was previously "
            "inspected in aggregate during the Spec 032 "
            "closure audit (970 Harappa inscriptions in "
            "the old combined training corpus, carrying "
            "1,013 occurrences of 11 of PRED-2026-006's 12 "
            "trained signs); no Harappa start rate has "
            "ever been computed for any sign; the "
            "cleanliness claimed is verified training-pool "
            "exclusion, not analyst blindness"
        ),
        "osf_registration": {
            "id": "wjebq",
            "doi": "10.17605/OSF.IO/WJEBQ",
            "state_at_draft_verification": (
                "accepted + public (API read-back "
                "2026-10-20); re-verified at execution "
                "step 0"
            ),
        },
        "execution_gate": (
            "satisfied at the freeze act of 2026-10-20: "
            "the owner's freeze order for this contract "
            "and the execution order were given in the "
            "same act (go with your recommendation); the "
            "freeze PR merged on green house gates; step "
            "0 re-verifies the OSF registration before "
            "any run"
        ),
    },
    "inputs": {
        "training_pool": {
            "file": "data/normalized/corpus_master.csv",
            "sha256": (
                "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
            ),
            "filter": (
                'source_name == "Corpus of Indus Seals and '
                'Inscriptions (mayig digitization)"'
            ),
            "pool_rows": 179,
            "pool_sites": {"Mohenjo-daro": 179},
            "yajnadevam_rows_in_pool": 0,
            "filtered_pool_manifest_sha256": (
                "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
            ),
        },
        "classification": {
            "classifiable_signs": 28,
            "class_counts": {
                "INITIAL": 3,
                "MEDIAL": 19,
                "MIXED": 3,
                "TERMINAL": 3,
            },
            "derivation_record": (
                "reports/pred010_derivation_record.json"
            ),
            "derivation_script": (
                "backend/scripts/pred010_register_derivation.py"
            ),
            "logic_carry": (
                "backend/scripts/phase396_pred006_step0.py "
                "(the recorded global_class_stability logic, "
                "carried verbatim)"
            ),
        },
        "withheld": {
            "file": (
                "backend/glossa_lab/data/"
                "yajnadevam_inscriptions.csv"
            ),
            "sha256": (
                "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
            ),
            "census_as_recorded_at_spec032_freeze": {
                "inscriptions": 5679,
                "sites": 77,
                "harappa": 2717,
            },
        },
        "crosswalk": {
            "file": (
                "data/crosswalks/"
                "yajnadevam_to_parpola_crosswalk.csv"
            ),
            "sha256": (
                "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
            ),
        },
        "predecessor": {
            "spec": "specs/032-pred-2026-006-harappa-breakdown",
            "freeze_digest": (
                "34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab"
            ),
            "closure": (
                "PRED-2026-006 closed at step 0 as CANNOT BE "
                "RUN AS WRITTEN, unscored"
            ),
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": (
            "1.0.4 (Glossa venv, PATH-pinned; package "
            "pinned >=1.0.4,<1.5 by PR #181)"
        ),
        "specify": "1.0.10",
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/osf-registration.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec035_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8"
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
