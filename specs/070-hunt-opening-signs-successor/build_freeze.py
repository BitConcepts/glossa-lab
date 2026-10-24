#!/usr/bin/env python3
"""Build the Spec 070 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-22. The register was recovered at the
freeze from 0.5-draft to 0.9-frozen-candidate
(the rounds are recorded in aee/freeze-aee-note.md),
the AEE lifecycle hooks passed over it at the
freeze gate (DD-070-14), and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering.
Run with the Glossa backend venv python from
the repository root:

    python specs/070-hunt-opening-signs-successor/build_freeze.py

Writes specs/070-hunt-opening-signs-successor/freeze.json
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

SPEC_DIR = "specs/070-hunt-opening-signs-successor"

DEFINITION = {
    "spec": "specs/070-hunt-opening-signs-successor/spec.md",
    "freeze_doc": "specs/070-hunt-opening-signs-successor/freeze.md",
    "experiment_id": "spec070-hunt-opening-signs-successor",
    "register": {
        "path": "specs/070-hunt-opening-signs-successor/claims.json",
        "register_version": "0.9-frozen-candidate",
        "claims": 13,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-22 under aee 1.5.3: the register was "
            "recovered at the freeze from 0.5-draft (not loadable as drafted: evidence "
            "kinds and a source quality the engine does not accept) through 0.6 "
            "(loadability restatement), 0.7 (round 1: 25 failure modes - 13 "
            "irreducibility and 12 negation-conflict challenges, minimum propagated "
            "0.845), 0.8 (7 failure modes) and a third round to 0.9-frozen-candidate, "
            "over which after_specify, after_plan and after_tasks each PASS with zero "
            "failure modes and no claim below the 0.70 threshold (minimum propagated "
            "0.845); the freeze rulings DD-070-8, DD-070-9, DD-070-10 and DD-070-11 "
            "were carried into the boundaries of F070-C05, F070-C08 and F070-C11 "
            "before the final round (gate reading DD-070-14, the DD-038-10 form; "
            "record in specs/070-hunt-opening-signs-successor/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/070-hunt-opening-signs-successor/adjudication.md",
        "decisions": (
            "DD-070-1 to DD-070-6 as drafted (first measurement not reproduction; "
            "Spec 049's test form carried; population published before any join; no "
            "phase at draft; evidence observed_at of the draft; the AEE freeze gate "
            "in the DD-038-10 form), and the freeze rulings DD-070-7 to DD-070-14 at "
            "adjudication section 7 (intake record landed; Asset A digest copied; "
            "keying route; counting rule; POPULATION NOT KEYED disposition; own OSF "
            "registration; Phase 433; the gate reading)"
        ),
    },
    "design": {
        "phase": "Phase 433",
        "question": (
            "Are Shakti's opening-strong signs the animal signs - Spec 049's "
            "question in re-scoped form, measured on the graded ICIT corpus with "
            "Spec 049's Mahadevan-population rule expressly replaced"
        ),
        "battery": (
            "The recovered Phase-43 battery applied new to Shakti (section 2): "
            "sequences of length >= 2, I/M/T by position, floor total >= 5, cascade "
            "TERMINAL_STRONG t_rate >= 0.60, INITIAL_STRONG i_rate >= 0.55, "
            "MEDIAL_STRONG m_rate >= 0.65, TERMINAL_MODERATE t_rate >= 0.40, "
            "INITIAL_MODERATE i_rate >= 0.40, MIXED; threshold-only, no chance "
            "baseline (G5 attestation mandatory); the Phase-43 counts (805/2,267; "
            "the 40/61/20 classes) are never a basis for any product"
        ),
        "populations": (
            "Primary: documented-lineage rows only. Sensitivity S-C: documented + "
            "corroborated rows, classes and counts re-derived; rows graded "
            "undocumented-uncorroborated enter no count anywhere"
        ),
        "test": (
            "O is the INITIAL_STRONG set, enumerated in full in Wells space and "
            "published before any join; U is every sign with >= 30 occurrences in "
            "the primary population under the counting rule of DD-070-10; R1 is "
            "the animal share of O over the animal share of U, Fisher exact on "
            "the disjoint 2x2 (O against U minus O), the one-sided p the "
            "criterion and the two-sided p published; R2 the reversed arm"
        ),
        "precedence": (
            "Section 4.3, carried from Spec 049's DD-049-3: NOT SUPPORTED if R1 "
            "<= 1.0 or p >= 0.05; SUPPORTED if R1 >= 1.5, p < 0.05 and R2 > 1.0; "
            "otherwise INCONCLUSIVE"
        ),
        "keying": (
            "DD-070-9: a Shakti sign's ICIT code is its Wells number, resolved "
            "through the pinned canonical sign registry's parpola_1982 rows' "
            "wells_ids to exactly one Asset A sign_key; zero or multiple "
            "resolutions is unkeyable"
        ),
        "disposition": (
            "DD-070-11 (conservative): an unkeyable sign enumerated in the "
            "opening-strong set closes the execution at gate 0.4 as POPULATION "
            "NOT KEYED, the sign named"
        ),
        "sensitivities": (
            "S-A contested Asset A rows included under their CISI-governed labels "
            "(Asset A carries zero contested rows, so S-A equals the primary and "
            "is reported as such); S-B unicorn removed, the sign(s) named at gate "
            "0.5 from the frozen asset's verbatim labels or S-B recorded not "
            "applicable; S-C the corroborated sensitivity"
        ),
        "outcomes": [
            "SUPPORTED",
            "NOT SUPPORTED",
            "INCONCLUSIVE",
            "ASSET NOT FROZEN",
            "ASSET PIN MISMATCH",
            "SHAKTI INTAKE NOT REPRODUCED",
            "POPULATION NOT KEYED",
            "INVALID",
        ],
        "osf": (
            "DD-070-12: this spec files its own OSF registration at its freeze "
            "under the programme's OSF project; the filing is recorded in "
            "osf-spec-registration.md in this directory"
        ),
        "execution_gate": (
            "Phase 433 executes only against this frozen record; step 0 asserts "
            "Asset A's digest (gate 0.1) and the Shakti intake under P-F1 S1/S2 "
            "(gate 0.2) before the population is enumerated (gate 0.4), the "
            "inventory published (gate 0.5), and the freeze-order proof given "
            "(gate 0.6)"
        ),
        "limits": (
            "Depiction is the published identification layer, not ground truth; "
            "Spec 037's 49 percent census caution travels with every statement "
            "of the result; no outcome establishes that animal signs marked "
            "identity, a guild, or goods"
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
            "record as it stands after Spec 069's execution merge (6a981188): "
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
    "backend/tests/test_spec070_freeze.py",
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
