#!/usr/bin/env python3
"""Build the Spec 071 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-22. The register was recovered at the
freeze from 0.5-draft to 0.9-frozen-candidate
(the rounds are recorded in aee/freeze-aee-note.md),
the AEE lifecycle hooks passed over it at the
freeze gate (DD-071-14), and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering.
Run with the Glossa backend venv python from
the repository root:

    python specs/071-hunt-sky-signs-successor/build_freeze.py

Writes specs/071-hunt-sky-signs-successor/freeze.json
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

SPEC_DIR = "specs/071-hunt-sky-signs-successor"

DEFINITION = {
    "spec": "specs/071-hunt-sky-signs-successor/spec.md",
    "freeze_doc": "specs/071-hunt-sky-signs-successor/freeze.md",
    "experiment_id": "spec071-hunt-sky-signs-successor",
    "register": {
        "path": "specs/071-hunt-sky-signs-successor/claims.json",
        "register_version": "0.9-frozen-candidate",
        "claims": 13,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-22 under aee 1.5.3: the register was "
            "recovered at the freeze from 0.5-draft (not loadable as drafted: evidence "
            "kinds and a source quality the engine does not accept) through 0.6 "
            "(loadability restatement), 0.7 (round 1: 6 failure modes - 4 "
            "irreducibility and 2 negation-conflict challenges, minimum propagated "
            "0.845) and a second round to 0.9-frozen-candidate, over which "
            "after_specify, after_plan and after_tasks each PASS with zero failure "
            "modes and no claim below the 0.70 threshold (minimum propagated "
            "0.845); the freeze rulings DD-071-9, DD-071-10 and DD-071-11 were "
            "carried into the boundaries of F071-C08 and F071-C07 before the final "
            "round (gate reading DD-071-14, the DD-038-10 form; record in "
            "specs/071-hunt-sky-signs-successor/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/071-hunt-sky-signs-successor/adjudication.md",
        "decisions": (
            "DD-071-1 to DD-071-7 as drafted (first measurement not reproduction; "
            "the commissioned freeze order 069-070-071; one battery statement; no "
            "phase at draft; Spec 050's criteria carried unchanged; evidence "
            "observed_at of the draft; the AEE freeze gate in the DD-038-10 form), "
            "and the freeze rulings DD-071-8 to DD-071-14 at adjudication section 8 "
            "(intake record landed; Asset A digest copied and the order recorded; "
            "the shared keying route; POPULATION NOT KEYED disposition; own OSF "
            "registration; Phase 434; the gate reading)"
        ),
    },
    "design": {
        "phase": "Phase 434",
        "question": (
            "Do the sky signs gather at the ends of texts - Spec 050's question "
            "in re-scoped form, measured on the graded ICIT corpus, the "
            "celestial class fixed by Spec 069's frozen Asset A classification"
        ),
        "celestial_class": (
            "Exactly the signs whose Asset A row carries depicted_kind = "
            "sky_cycle (section 4.1); the class is not widened to any "
            "jurisdiction-coded subset, to any sign whose label a reader might "
            "call celestial while its kind is object_goods, human or other, or "
            "to any worker's judgement; contested signs are excluded from the "
            "primary and enter only in S2 under their CISI-governed labels; "
            "unidentified signs are never celestial"
        ),
        "frame": (
            "The ending population is Shakti's own terminal-strong set: the "
            "signs classed TERMINAL_STRONG by the section 2 battery over the "
            "primary population (documented-lineage rows only), enumerated in "
            "full in Wells space and published at gate 0.4 before any test"
        ),
        "criteria": (
            "Spec 050's criteria carried unchanged (DD-071-5): enrichment "
            "ratio R_sky / R_cmp at least 1.5; Fisher's exact test, two-sided, "
            "at the 5 percent level; and the half-of-occurrences condition - "
            "at least half the celestial class's total occurrences come from "
            "member signs individually above the corpus-wide final-position "
            "rate. TOO THIN floor (DD-050-3): below 30 total occurrences for "
            "the celestial class or the comparison class at gate 0.4 closes "
            "TOO THIN, recorded as INCONCLUSIVE's thin form"
        ),
        "comparison_class": (
            "The frequency-matched class of section 4.2: non-celestial, "
            "non-contested signs in the primary whose total occurrence count "
            "lies within the celestial members' minimum-to-maximum band, "
            "inclusive; primary rates are pooled occurrence rates"
        ),
        "keying": (
            "DD-071-10: the route Spec 070's freeze fixed, stated in this "
            "spec's own record - a Shakti sign's ICIT code is its Wells "
            "number, resolved through the pinned canonical sign registry's "
            "parpola_1982 rows' wells_ids to exactly one Asset A sign_key; "
            "zero or multiple resolutions is unkeyable"
        ),
        "disposition": (
            "DD-071-11 (conservative): an unkeyable sign enumerated at gate "
            "0.4 closes the execution as POPULATION NOT KEYED, the sign named"
        ),
        "sensitivities": (
            "S1 borderline Asset A rows removed; S2 contested rows included "
            "under their CISI-governed sky labels; S3 the documented + "
            "corroborated population with the battery classes re-derived "
            "(P-F1 S4 both-ways reporting)"
        ),
        "outcomes": [
            "SUPPORTED",
            "NOT SUPPORTED",
            "INCONCLUSIVE",
            "TOO THIN",
            "CLOSED AT STEP 0 - ASSET NOT FROZEN",
            "CLOSED AT STEP 0 - ASSET PIN MISMATCH",
            "SHAKTI INTAKE NOT REPRODUCED",
            "POPULATION NOT KEYED",
            "INVALID",
            "NOT-RUN",
            "NOT ADJUDICATED",
        ],
        "osf": (
            "DD-071-12: this spec files its own OSF registration at its "
            "freeze under the programme's OSF project; the filing is "
            "recorded in osf-spec-registration.md in this directory"
        ),
        "execution_gate": (
            "Phase 434 executes only against this frozen record; step 0 "
            "asserts Asset A against the pin source this freeze fixes "
            "(Spec 069's asset-a-freeze.json in its merged executed record, "
            "gate 0.1) and the Shakti intake under P-F1 S1/S2 (gate 0.2), "
            "input integrity and coverage (gate 0.3), the enumeration, "
            "keying and class census with the TOO THIN floor (gate 0.4), "
            "and the freeze-order proof including this freeze following "
            "Spec 070's freeze (gate 0.5)"
        ),
        "limits": (
            "Position is not meaning: no outcome establishes that sky signs "
            "marked calendars, cycles, or any content; depiction is the "
            "published identification layer, not ground truth; Spec 037's "
            "49 percent census caution travels with every statement of the "
            "result"
        ),
    },
    "inputs": {
        "asset_a": {
            "path": "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv",
            "sha256": "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b",
            "rows": 187,
            "per_kind_counts": {
                "animal": 20, "sky_cycle": 0, "object_goods": 14,
                "human": 25, "other": 127, "contested": 0, "unidentified": 1,
            },
        },
        "shakti_corpus": {
            "record": "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
            "corpus_sha256": "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68",
            "row_grades_sha256": "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739",
            "rows": 5704,
            "grades": {"documented": 3212, "corroborated": 2087, "uncorroborated": 405},
        },
        "canonical_registry": {
            "path": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
            "rows": 803,
        },
        "crosswalk": {
            "path": "data/crosswalks/sign_crosswalk_master.csv",
            "sha256": "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
        },
        "anchors": {
            "path": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
        },
        "pin_verification": (
            "verified first-hand at the freeze act of 2026-10-22 on the merged "
            "record as it stands after Spec 070's freeze merge (1213029d): "
            "Asset A's digest recomputed from the canonical CSV on the merged "
            "tree equals the executed record's quoted value; the Shakti corpus "
            "and row-grades files hashed directly at their restricted-local "
            "paths and equal the intake record's pins, their grade census "
            "recounted from the grades file itself; the registry, crosswalk and "
            "anchors hashed in the tree and equal their pins; the registry's "
            "parpola_1982 Wells map recounted (498 Wells ids, zero ambiguous)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.3 (adopted environment; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec071_freeze.py",
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
