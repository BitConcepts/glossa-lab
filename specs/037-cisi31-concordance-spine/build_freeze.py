#!/usr/bin/env python3
"""Build the Spec 037 freeze record (freeze.json).

This builder computes the freeze digest over the
frozen contract exactly once, at the freeze act
of 2026-10-20 - after the AEE lifecycle hooks
passed over the recovered register (0.7-draft)
under the owner's standing pipeline
authorisation - with its DEFINITION text
finalised in the same act (the Spec 035
pattern). Run with the Glossa
backend venv python from the repository root:

    python specs/037-cisi31-concordance-spine/build_freeze.py

Writes specs/037-cisi31-concordance-spine/freeze.json
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

SPEC_DIR = "specs/037-cisi31-concordance-spine"

DEFINITION = {
    "spec": "specs/037-cisi31-concordance-spine/spec.md",
    "freeze_doc": "specs/037-cisi31-concordance-spine/freeze.md",
    "experiment_id": "spec037-cisi31-concordance-spine",
    "register": {
        "path": "specs/037-cisi31-concordance-spine/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-20 "
            "under aee 1.5.0: after_specify cleared "
            "in three adjudicated rounds (37 failure "
            "modes over 0.5-draft; 27 over 0.6-draft; "
            "15 FR-2.3 draft-cap records only over "
            "0.7-draft), after_plan and after_tasks "
            "clean at first pass; at every hook zero "
            "correctness failure modes and no claim "
            "below the 0.70 threshold (minimum "
            "propagated 0.72); the engine outcome "
            "word reads iterate solely from the "
            "draft-cap records (gate reading "
            "DD-037-9; record in "
            "specs/037-cisi31-concordance-spine/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/037-cisi31-concordance-spine/adjudication.md"
        ),
        "decisions": (
            "The owner's standing pipeline "
            "authorisation of 2026-10-20 (freeze "
            "order 038, then 037, then 039, then "
            "040) froze this contract and ordered "
            "its execution as Phase-402. The study "
            "implemented is the CISI 3.1 intake's "
            "first two assessed candidate uses "
            "(intake report sections 7.5-7.6, "
            "2026-10-20), over material held under "
            "the Phase-130 gate (restricted store "
            "PROVENANCE entry 22). Freeze decisions "
            "DD-037-4 to DD-037-9 are recorded in "
            "adjudication.md section 4: halt "
            "threshold confirmed at 20 percent of "
            "all candidates; hand-check stratum 60; "
            "Workstream B inside Phase-402 gated on "
            "step 0 only; the spec's own OSF "
            "registration filed at the freeze; phase "
            "allocation Phase-402; the DD-038-10 "
            "gate reading adopted as DD-037-9."
        ),
    },
    "design": {
        "phase": "Phase-402",
        "question_owner": (
            "the CISI 3.1 intake record (2026-10-20), "
            "candidate uses 1-2; no PRED-2026 entry is "
            "scored, advanced, or retired by this study"
        ),
        "workstream_a": (
            "object-level concordance spine: verify "
            "the intake's 693 exact-string matches "
            "between the portion's catalogue numbers "
            "and corpus_master object ids as "
            "same-object joins under the fixed ladder "
            "(spec section 4.3); build the spine from "
            "VERIFIED joins only, as a LOCAL table in "
            "the restricted store; report aggregate "
            "statistics only"
        ),
        "workstream_b": (
            "HARP provenance annex (descriptive): "
            "dig-year, lot, and period-code "
            "inventories and distributions from the "
            "HARP rows of the same local table, with "
            "the period-fill floor caveat; it does "
            "not change the Spec 031 (Q7) record and "
            "feeds no verdict"
        ),
        "pilot": {
            "candidates": 693,
            "candidate_split_by_section": {
                "mohenjo_daro": 289,
                "harappa_old": 102,
                "harappa_harp": 302,
            },
            "form": (
                "census of all candidates, not a "
                "sample (DD-037-2)"
            ),
            "ladder": [
                "site agreement (mandatory; the fixed "
                "section-to-site mapping)",
                "object-type agreement (mandatory "
                "where graded; closed class set; a "
                "seal and a seal impression are "
                "different classes)",
                "corroborating keys (FC number, "
                "excavation number, museum/"
                "registration) where both sides carry "
                "a value: contradiction is a conflict; "
                "absence is UNGRADED",
                "number-level ambiguity (the portion's "
                "own records under one number "
                "conflict) bars VERIFIED",
            ],
            "outcome_classes": [
                "VERIFIED", "CONFLICT", "UNRESOLVED",
            ],
            "conflict_reason_codes": [
                "SITE", "TYPE", "CORROB-FC",
                "CORROB-EXC", "CORROB-MUS",
                "NUMBER-AMBIGUOUS",
            ],
            "halt_rule": {
                "conflict_share_cap": 0.2,
                "base": "all 693 candidates",
                "on_halt": (
                    "the pilot completes and reports in "
                    "full; no spine file is written; "
                    "the outcome is PILOT COMPLETE - "
                    "SPINE HALTED"
                ),
            },
            "hand_check_stratum": (
                "seeded random sample stratified "
                "across the three outcome classes, "
                "attributing each sampled conflict to "
                "intake extraction error, programme-"
                "side record error, genuine "
                "compilation divergence, or true "
                "non-identity; its size is fixed at "
                "the freeze at 60 (DD-037-5: 30 "
                "VERIFIED / 15 CONFLICT / 15 "
                "UNRESOLVED, the whole class where a "
                "class is smaller; the seed is "
                "recorded in the build script before "
                "sampling)"
            ),
        },
        "reported_aggregates": (
            "outcome counts and shares overall, by "
            "portion section, and by corpus source; "
            "conflict breakdown by reason code; "
            "per-field graded bases; the stratum's "
            "cause attribution; spine coverage and "
            "field fill; the annex distributions - "
            "aggregate statistics only, never rows"
        ),
        "fences": {
            "string_match": (
                "an exact-string match is a candidate, "
                "never a join"
            ),
            "finding_aid": (
                "the concordance is a finding aid, "
                "not evidence about readings"
            ),
            "no_pred_scoring": (
                "the Basic data tables carry no sign "
                "transcriptions (zero sign tokens), so "
                "no PRED-2026 entry can be scored "
                "from this material"
            ),
            "q7": (
                "the annex does not change the Spec "
                "031 (Q7) finding: in-universe link "
                "mass 2 sites / 1 pair; bead/craft "
                "NOT-YET-TESTABLE; ceramic NOT "
                "ESTIMABLE"
            ),
            "join_keys": (
                "Holdat cisi_number is prohibited as a "
                "join key (the Spec 034 discipline)"
            ),
        },
        "execution_gate": (
            "Satisfied at the freeze of 2026-10-20: "
            "the owner's standing pipeline "
            "authorisation (freeze order 038, then "
            "037, then 039, then 040) ordered this "
            "contract frozen and executed; execution "
            "runs as Phase-402 under the frozen "
            "contract, fail-closed at step 0"
        ),
    },
    "inputs": {
        "portion_pdf": {
            "storage": (
                "restricted local store, research "
                "notes (never in git): downloads/"
                "oakland-ill-cisi31-portion/376929.pdf"
            ),
            "bytes": 8206446,
            "sha256": (
                "514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a"
            ),
        },
        "local_table": {
            "storage": (
                "restricted local store, beside the "
                "scan: cisi31-basic-data.csv"
            ),
            "records": 2123,
            "columns": 26,
            "distinct_catalogue_numbers": 2101,
            "sections": {
                "mohenjo_daro": 519,
                "harappa_old": 510,
                "harappa_harp": 1094,
            },
        },
        "corpus_master": {
            "file": "data/normalized/corpus_master.csv",
            "sha256": (
                "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
            ),
            "rows": 2722,
            "sources": {
                "mayig_cisi": 179,
                "yajnadevam": 2543,
            },
        },
        "gate": {
            "phase": "Phase-130",
            "record": (
                "restricted store PROVENANCE entry 22, "
                "recorded 2026-10-20 before any "
                "processing; in-repo pack "
                "specs/021-phase130-intake-pack/"
            ),
            "classification": (
                "restricted research material: local "
                "use, extraction, and publishable "
                "derived statistics permitted; "
                "redistribution of scans or row data "
                "prohibited; nothing derived enters git"
            ),
        },
        "local_products": {
            "spine": (
                "cisi31-concordance-spine.csv in the "
                "portion folder of the restricted "
                "store (VERIFIED joins only); named in "
                "the outcome record by filename and "
                "row count only"
            ),
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
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
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec037_freeze.py",
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
