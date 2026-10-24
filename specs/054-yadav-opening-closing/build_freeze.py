#!/usr/bin/env python3
"""Build the Spec 054 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-23 and run exactly once, in that act,
to compute the freeze digest over the recovered
register (0.8-draft) and the finalised freeze
texts (the Spec 035 ordering: the AEE lifecycle
hooks first, the digest after). Run with the
AEE 1.5.0 venv python from the repository root:

    python specs/054-yadav-opening-closing/build_freeze.py

Writes specs/054-yadav-opening-closing/freeze.json
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

SPEC_DIR = "specs/054-yadav-opening-closing"

FALSIFIER_TEXT = (
    "This claim, as evaluated under battery NB-1 "
    "(the Spec 054 amendment, as frozen), is "
    "falsified if any of the following holds when "
    "the frozen battery is run on the frozen "
    "arm-1 and arm-2 corpora: (1) either arm-1 "
    "positional-strong set (opening or closing) "
    "is empty; (2) for either class, fewer than "
    "half of arm 1's positional-strong signs are "
    "also positional-strong in arm 2 in the same "
    "class, through the pinned crosswalk; or (3) "
    "the pooled cross-arm overlap of "
    "positional-strong signs does not exceed the "
    "95th percentile of the 999-shuffle "
    "label-permutation null \u2014 the three "
    "conditions applied under the precedence "
    "rule of the Spec 054 amendment (\u00a75.5)."
)

DEFINITION = {
    "spec": "specs/054-yadav-opening-closing/spec.md",
    "freeze_doc": "specs/054-yadav-opening-closing/freeze.md",
    "experiment_id": "spec054-yadav-opening-closing",
    "register": {
        "path": "specs/054-yadav-opening-closing/claims.json",
        "register_version": "0.8-draft",
        "claims": 19,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-23 "
            "under aee 1.5.0: after_specify, "
            "after_plan, and after_tasks each carry "
            "19 failure modes, all FR-2.3 draft-cap "
            "records, with zero correctness failure "
            "modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); "
            "the engine outcome word reads iterate "
            "solely from the draft-cap records (gate "
            "reading DD-054-9, adopting DD-038-10; "
            "record in "
            "specs/054-yadav-opening-closing/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/054-yadav-opening-closing/adjudication.md"
        ),
        "amendment": (
            "specs/054-yadav-opening-closing/amendment.md"
        ),
        "decisions": (
            "The draft was commissioned by the "
            "owner-approved runnable-experiments "
            "campaign plan of 2026-10-21 (member 7, "
            "design D-08). Its freeze attempt of "
            "2026-10-21 failed (adjudication.md "
            "section 7: OPEN-054-1 battery not "
            "pinnable; the original sets not "
            "exhibitable). The owner's rulings of "
            "2026-10-23 (section 8) adopted the "
            "section 7.5(2) amended design (battery "
            "NB-1) and decided the section 7.5(3) "
            "generator act; the owner approved the "
            "amendment mini-gate as specified on "
            "2026-10-23 at 22:59 EDT. Freeze "
            "decisions are recorded in "
            "adjudication.md section 9: L5 decided "
            "as amended (OPEN-054-1 discharged; "
            "OPEN-054-2 discharged as a gate; "
            "OPEN-054-3, 4, 7 confirmed as amended; "
            "OPEN-054-5 answered; OPEN-054-6 "
            "reconciled; OPEN-054-8 yes, the OSF "
            "registration filed at the freeze); "
            "DD-054-9 adopts the DD-038-10 AEE gate "
            "reading; DD-054-10 allocates "
            "Phase-437. Execution is not ordered by "
            "the freeze and has not started."
        ),
    },
    "design": {
        "phase": "Phase-437",
        "statement": (
            "the amended statement of amendment.md "
            "section 2: there are specific "
            "text-beginning and text-ending signs "
            "in the Indus corpus, in the exact sense "
            "battery NB-1 makes checkable; a verdict "
            "on it is not a verdict on Yadav et al. "
            "(2010)'s original Phase-43 statement"
        ),
        "battery": {
            "name": "NB-1",
            "population": (
                "each corpus layer's own numbering "
                "and segmentation; no re-segmentation, "
                "no renumbering, and no crosswalk "
                "inside a run"
            ),
            "classes": (
                "initial / terminal / medial for "
                "sequences of length >= 2; length-1 "
                "sequences counted and reported "
                "separately, entering no count; "
                "I + T + M = N exactly"
            ),
            "floor": 20,
            "bands": {"STRONG": ">= 2/3", "MODERATE": ">= 1/2"},
            "opening_strong": "INITIAL_STRONG",
            "closing_strong": "TERMINAL_STRONG",
        },
        "arms": {
            "arm_1": (
                "the strict corpus: the "
                "Mahadevan-lineage V3 layer as held "
                "in the database, identified, "
                "exported, and pinned at step 0"
            ),
            "arm_2": (
                "the Holdat layer in its own "
                "numbering, through crosswalk v1 at "
                "the freeze pins"
            ),
        },
        "decision": {
            "reappearance": (
                "per class (DD-054-1): a class "
                "reappears iff the share of arm 1's "
                "strong set whose members are also "
                "strong in arm 2 in the same class, "
                "through the pinned crosswalk, is "
                ">= 1/2"
            ),
            "denominators": (
                "DD-054-5: arm-1 strong signs "
                "unmapped, conflict-paired, or below "
                "the floor in arm 2 count as not "
                "reappeared in the primary measure "
                "and are named with their reason "
                "(TOO THIN / UNMAPPED / CONFLICT); "
                "the sensitivity excluding named "
                "signs is reported with the same "
                "prominence; the verdict follows the "
                "primary"
            ),
            "null": {
                "construction": (
                    "label permutation: arm 2's "
                    "strong-set membership labels "
                    "permuted over arm 2's classifiable "
                    "signs, set sizes and the mapping "
                    "table held fixed"
                ),
                "shuffles": 999,
                "seed": 44054,
                "chance_level": (
                    "nearest-rank 95th percentile "
                    "(the 950th smallest)"
                ),
            },
            "precedence": [
                "either arm-1 strong set empty -> NOT SUPPORTED",
                "both classes reappear -> the pooled overlap decides: above the chance level SUPPORTED; at or below NOT SUPPORTED",
                "a class short -> overlap at or below the chance level NOT SUPPORTED; overlap above INCONCLUSIVE with the rates stated",
            ],
        },
        "step0_gates": [
            "pin checks (any mismatch -> INVALID)",
            "STRICT CORPUS NOT PINNABLE",
            "TOO THIN",
            "SECOND ARM NOT RUNNABLE",
            "determinism (failure -> INVALID)",
        ],
        "falsifier": {
            "claim": "yadav_2009_arxiv_manual_002",
            "appended_at": "the freeze act of 2026-10-23",
            "text": FALSIFIER_TEXT,
        },
        "verdict_wordings": (
            "amendment.md section 9, verbatim; the "
            "word RE-EARNED appears in no amended "
            "wording; the parent claim's recorded "
            "status is moved by no verdict"
        ),
        "spec045_fence": (
            "Spec 045's 'Holdat final-position "
            "concentration' and this spec's "
            "'closing-strong under NB-1' are "
            "different quantities, distinctly named "
            "in every outcome record"
        ),
        "execution_gate": (
            "NOT satisfied: no execution order "
            "exists for this contract; the freeze "
            "itself computes no positional quantity, "
            "counts no arm, and reaches no verdict"
        ),
    },
    "inputs": {
        "claim_store": {
            "file": "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json",
            "sha256_before_append": "904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3",
            "sha256_after_append": "dcbaf64a728bc4ff7a0a1f76f2c867f924734cbe7f9c8cab2554d131b22533d7",
            "bytes_after_append": 15402,
        },
        "phase43": {
            "file": "outputs/phase43_all.json",
            "sha256": "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
            "bytes": 15047,
        },
        "hunt_tripartite": {
            "file": "glossa-indus/analysis/positional/hunt_tripartite_test.json",
            "sha256": "0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48",
            "bytes": 923,
        },
        "crosswalk": {
            "json_sha256": "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb",
            "csv_sha256": "3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823",
            "rows": 766,
            "mapped_pairs": 762,
            "conflict_pairs": 383,
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "bytes": 570344,
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-aee150 for the freeze acts)",
        "aee": (
            "1.5.0 (adopted environment, PR #231; "
            "package pinned >=1.5.0,<1.6)"
        ),
        "specify": "1.0.10",
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/amendment.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec054_freeze.py",
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
