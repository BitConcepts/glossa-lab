#!/usr/bin/env python3
"""Build the Spec 072 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-22. The register was recovered from the
draft register (0.5-draft) to 0.8-draft in three
recovery rounds finished before the digest (the
record is in aee/freeze-aee-note.md and in the
register's own note), the AEE lifecycle hooks
passed over the recovered register, the
freeze-stage step-0 acts were performed in
order (gates 0.1-0.5; freeze.md sections 3-6),
and the digest is computed over the recovered
register and the finalised freeze texts exactly
once, at the freeze - the Spec 035 ordering.
Run with the Glossa backend venv python from
the repository root:

    python specs/072-fish-family-profiles-redesign/build_freeze.py

Writes specs/072-fish-family-profiles-redesign/freeze.json
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

SPEC_DIR = "specs/072-fish-family-profiles-redesign"

DEFINITION = {
    "spec": "specs/072-fish-family-profiles-redesign/spec.md",
    "freeze_doc": "specs/072-fish-family-profiles-redesign/freeze.md",
    "experiment_id": "spec072-fish-family-profiles-redesign",
    "register": {
        "path": "specs/072-fish-family-profiles-redesign/claims.json",
        "register_version": "0.8-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-22 under aee 1.5.3: the draft register "
            "(0.5-draft) was recovered in three rounds finished before the digest - round 1 "
            "(0.6-draft) restated every evidence item in engine values (kind observed, "
            "source_quality artifact) and carried the freeze rulings into the boundaries of "
            "F072-C03, C04, C07, C08, C09, C10, C12 and C14; round 2 (0.7-draft) restated "
            "nine irreducibility-challenged claim heads as single propositions with their "
            "clauses carried into their boundaries; round 3 (0.8-draft) restated the three "
            "remaining heads without compound connectives - and at the final round "
            "after_specify, after_plan and after_tasks each carried 15 FR-2.3 draft-cap "
            "records only, zero correctness failure modes, and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); the engine outcome word reads iterate "
            "solely from the draft-cap records (gate reading DD-038-10; record in "
            "specs/072-fish-family-profiles-redesign/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/072-fish-family-profiles-redesign/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-22 (not proposals): the freeze-gate package "
            "for the Shakti draft specs carried Spec 072's open items OPEN-072-1 to "
            "OPEN-072-10 to the freeze with the owner's rulings - the verdict line derived "
            "at the freeze by the draft's fixed rule and recorded with its reference "
            "record, or the freeze fails as VERDICT LINE NOT DERIVABLE with no fallback "
            "line (OPEN-072-1); the concordance per the draft, every member's ICIT "
            "identity stated and pinned on the stated basis, any unidentified member "
            "named UNIDENTIFIED IN ICIT with its disposition ruled in the freeze record "
            "(OPEN-072-2); the Roif gate confirmed in its drafted form (OPEN-072-10); "
            "all other items ruled per the draft's stated defaults; the execution phase "
            "allocated as Phase-431 (OPEN-072-8). The freeze record (freeze.md sections "
            "2-6) carries each ruling and the freeze-stage step-0 exhibits."
        ),
    },
    "design": {
        "phase": "Phase-431",
        "claim_under_test": {
            "id": "parpola_2010_dravidian_solution_manual_002",
            "record": (
                "The fish sign (meen in Dravidian) is the primary rebus sign in the Indus "
                "script - standing IN QUESTION, partially supported: Mahadevan sign 72 "
                "passed its Phase-43 T2.4 positional test; sign 267, the family's most "
                "frequent member, failed it clearly. That standing is Spec 048's record "
                "and this spec's starting point; this spec does not re-derive it and does "
                "not inherit Spec 048's calibration."
            ),
        },
        "verdict_line": {
            "L": 0.765,
            "rule": (
                "spec section 5.3, applied at the freeze (OPEN-072-1): L is the 95th "
                "percentile, nearest-rank, of the freeze-stage reference distribution of "
                "non-fish signs clearing the carried supported floor (total >= 20) on the "
                "primary (documented-lineage) population, measured from non-members only, "
                "before any member was scored, stated to three decimal places rounding "
                "the percentile value up at the fourth decimal place"
            ),
            "reference_record": {
                "path": "specs/072-fish-family-profiles-redesign/reference-distribution.json",
                "sha256": "55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5",
                "sign_count": 86,
                "nearest_rank_index_1based": 82,
                "p95_fraction": 0.7647058823529411,
                "p95_sign": "226",
                "p95_counts": "13 ending followers of 17 bigrams",
            },
            "degeneracy_rule": (
                "a reference population of fewer than 30 signs, or a 95th percentile of "
                "0 or 1, fails the freeze as VERDICT LINE NOT DERIVABLE, with no fallback "
                "line; neither condition fired (86 signs; percentile 0.7647)"
            ),
            "excluded_inputs": (
                "the Phase-43 reference points (25.9 percent for sign 72; 3.8 percent for "
                "sign 267) and Spec 048's 20 percent member bar are not inputs to this "
                "line in any form; the carried 0.15 supported label is not the line"
            ),
            "pass_rule": (
                "a member PASSES iff its primary-population ending-follower fraction is "
                "at or above L and it clears the carried supported floor (total >= 20)"
            ),
        },
        "concordance": {
            "ruling": (
                "OPEN-072-2: governing basis confirmed as two held files, each pinned by "
                "SHA-256; the member's ICIT identity, keyed by its Parpola number, is "
                "the unique code in the intersection of the registry row's wells_ids and "
                "the glyph ids of the crosswalk's confirmed rows whose best_parpola_match "
                "is that Parpola number; an intersection not holding exactly one code "
                "names the member UNIDENTIFIED IN ICIT"
            ),
            "basis": {
                "registry": {
                    "path": "data/crosswalks/canonical_sign_registry.csv",
                    "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
                },
                "yajnadevam_crosswalk": {
                    "path": "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv",
                    "sha256": "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2",
                },
                "considered_not_governing": (
                    "data/crosswalks/sign_crosswalk_master.csv (sha256 "
                    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf) "
                    "carries no Wells/ICIT code; the curated Mahadevan-Parpola crosswalk's "
                    "wells_id values for this family (W008-W042) appear in neither basis "
                    "file and are absent or near-absent in the pinned corpus"
                ),
            },
            "identified": {
                "M048": "243",
                "M050": "220",
                "M060": "235",
                "M145": "032",
                "M147": "033",
            },
            "unidentified": ["M047", "M052"],
            "disposition": (
                "DD-072-5 confirmed: each unidentified member is named UNIDENTIFIED IN "
                "ICIT in the headline block, excluded from both populations' weighting, "
                "never dropped silently and never substituted; its occurrence share in "
                "ICIT space cannot be measured and is reported as such"
            ),
            "divergence_named": (
                "the registry's depiction notes for P145 and P147 (stroke signs) and for "
                "P047 (a decorated vertical line) differ from Asset F's depiction notes "
                "for the same Parpola numbers; the concordance is a numbering "
                "concordance on the stated basis, membership remains Asset F's exactly "
                "as frozen, and the divergence is reported in freeze.md section 4 and in "
                "every execution headline block"
            ),
        },
        "populations": (
            "primary: documented-lineage rows only (3,212 rows, 3,045 analyzable); "
            "sensitivity (mandatory): documented-lineage + undocumented-corroborated "
            "rows (5,299 rows, 5,131 analyzable), the whole test recomputed against the "
            "same L; undocumented-uncorroborated rows (405) enter no count; rows "
            "entirely 000 enter no sign analysis; sequences counted as stored, in "
            "stored order, no direction normalisation, with the 000 placeholder gated "
            "out before any position or bigram is counted (OPEN-072-3)"
        ),
        "measure": (
            "the T2.4 analogue of spec section 5.2, method carried from Amendment Queue "
            "Item 2 and labelled carried: positional classes per population under the "
            "carried cascade (classification floor total >= 5; t_rate >= 0.60 "
            "TERMINAL_STRONG; i_rate >= 0.55 INITIAL_STRONG; m_rate >= 0.65 "
            "MEDIAL_STRONG; t_rate >= 0.40 TERMINAL_MODERATE; i_rate >= 0.40 "
            "INITIAL_MODERATE; otherwise MIXED); a member's ending-follower fraction is "
            "the share of bigrams whose first sign is the member whose second sign is "
            "TERMINAL_STRONG or TERMINAL_MODERATE on the same population; carried "
            "floors: scanned iff total >= 10, the carried descriptive label supported "
            "iff fraction > 0.15 and total >= 20 (a descriptive label carried with the "
            "method, never this spec's verdict); no chance-baseline step is added "
            "(OPEN-072-4)"
        ),
        "partition": (
            "OPEN-072-5, DD-072-2 confirmed: over the tested members (identified at "
            "gate 0.3, clearing the carried supported floor in the primary population), "
            "the passing members' token-weighted share w of the tested members' "
            "primary occurrences decides - w above 50 percent FAMILY SUPPORTED; w below "
            "50 percent FAMILY NOT SUPPORTED; w exactly 50 percent, or the coverage "
            "condition (members UNIDENTIFIED IN ICIT excepted as unmeasurable, "
            "identified members NOT SCANNED or SCANNED - BELOW SUPPORTED FLOOR together "
            "carrying more of the identified family's primary occurrences than the "
            "tested members), INCONCLUSIVE. Spec 048's 70 percent / 30 percent family "
            "lines are not carried"
        ),
        "grade_flip": (
            "OPEN-072-6, DD-072-6 confirmed: a member whose carried supported label or "
            "PASS word changes between the populations is reported as a grade-flip "
            "finding in the outcome record's first section and the headline block; if "
            "the family word differs between populations the headline is the primary "
            "population's verdict flagged GRADE-SENSITIVE, both verdicts reported"
        ),
        "step0_gates": (
            "in frozen order, re-asserted at execution step 0 before any member is "
            "scored: 0.1 Shakti intake assertion (P-F1 S1/S2 against the merged intake "
            "record; failure closes SHAKTI INTAKE NOT REPRODUCED) - PASS at the freeze; "
            "0.2 Asset F digest assertion under Spec 044 section 4.2's exclusion rule "
            "(ASSET F NOT AVAILABLE / ASSET F DIGEST MISMATCH) - PASS at the freeze; "
            "0.3 the concordance act (freeze.md section 4; CONCORDANCE FAILED if no "
            "member can be identified) - performed at the freeze, five identified, two "
            "UNIDENTIFIED IN ICIT; 0.4 positional classes and census, margins only (TOO "
            "THIN if no identified member clears the supported floor in the primary "
            "population) - four testable at the freeze; 0.5 verdict-line assertion (the "
            "freeze-fixed L of this record; INVALID if none exists) - L = 0.765 derived "
            "and recorded at the freeze"
        ),
        "outcomes": [
            "FAMILY SUPPORTED",
            "FAMILY NOT SUPPORTED",
            "INCONCLUSIVE",
            "TOO THIN",
            "SHAKTI INTAKE NOT REPRODUCED",
            "ASSET F DIGEST MISMATCH",
            "ASSET F NOT AVAILABLE",
            "CONCORDANCE FAILED",
            "INVALID",
        ],
        "roif_gate": (
            "OPEN-072-10 confirmed in its drafted form (spec section 7 limit 1; claim "
            "F072-C14): no publication of this spec's results in any form without both "
            "(i) citation of Roif 2025a (Academia.edu doc 129921039) and Roif 2025b "
            "(Academia.edu doc 143222807) and (ii) the owner's clearance of the specific "
            "act, regardless of outcome; the gate constrains publication, not execution; "
            "records under this spec are internal until both conditions are met"
        ),
        "freeze_does_not": (
            "the freeze does not itself score any member (no member ending-follower "
            "fraction exists at the freeze, in either population); it does not settle "
            "the depiction divergence named in the concordance; it re-opens nothing in "
            "Spec 044's asset, Spec 048's closure, or the Phase-43 record; it "
            "establishes nothing about what any fish sign meant or was pronounced"
        ),
        "execution_gate": (
            "execution (Phase-431) runs after this freeze has merged and the OSF "
            "contract registration is filed, under the execution order given in the "
            "same owner tasking that commissioned this freeze; the registration's "
            "approval act remains the owner's click and is not performed by the freeze "
            "or the execution"
        ),
    },
    "inputs": {
        "claim_record": {
            "path": "glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json",
            "sha256_as_pinned_in_spec_s2": "3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba20d06c1b22810dfb000c",
            "note": (
                "the pin Spec 048's frozen text carries, as stated in spec section 2; "
                "the live file carries Spec 048's dated outcome append and so does not "
                "recompute to this pin, which is recorded here as stated, not asserted "
                "on the live bytes"
            ),
        },
        "phase43_results": {
            "path": "outputs/phase43_all.json",
            "sha256": "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
        },
        "item2_battery_script": {
            "sha256": "6d5a079d47113937afd3340ab4b35781d1b7202644b180ba814d15f03f49699e",
            "note": "phase43_part2.py, as recorded in Amendment Queue Item 2 section 1.1; the carried method's source",
        },
        "asset_f": {
            "path": "specs/044-fish-sign-coastal-residue/asset-f-fish-family.json",
            "digest": "ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3",
            "member_count": 7,
            "frozen_at": "2026-10-21",
            "assertion": (
                "recomputed at the freeze under Spec 044 section 4.2's exclusion rule "
                "(canonical bytes: json.dumps indent=2, keys sorted, ensure_ascii=False, "
                "trailing newline; digest field excluded) - PASS"
            ),
        },
        "shakti_corpus": {
            "file": "sanitized_corpus.json (restricted-local, never in git)",
            "sha256": "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68",
            "bytes": 1570041,
        },
        "row_grades": {
            "file": "shakti_row_grades_2026-10-22.csv (restricted-local, never in git)",
            "sha256": "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739",
        },
        "intake_record": {
            "path": "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
            "merged": "PR #339, merge commit bfc811df",
            "census": (
                "5,704 rows; 5,536 analyzable; grades 3,212 documented-lineage / 2,087 "
                "undocumented-corroborated / 405 undocumented-uncorroborated; 4,904 of "
                "5,536 analyzable rows (88.6 percent) carrying a CISI identifier; 18,065 "
                "true sign tokens; 713 distinct signs; 77 sites - reproduced exactly at "
                "the freeze (gate 0.1 PASS)"
            ),
        },
        "mahadevan_parpola_crosswalk": {
            "path": "backend/glossa_lab/data/mahadevan_parpola_crosswalk.json",
            "sha256": "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b",
        },
        "pin_verification": (
            "at the freeze of 2026-10-22 every committed pin above was re-derived from "
            "the tree the freeze was built on (the PR #341 branch tree, whose crosswalk "
            "files are byte-identical to main's), and the restricted-local pins were "
            "recomputed on the held files by hashlib and sha256sum agreeing; every "
            "recomputed hash equals its pin (freeze.md sections 3-4)"
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
    "specs/072-fish-family-profiles-redesign/freeze.md",
    "specs/072-fish-family-profiles-redesign/spec.md",
    "specs/072-fish-family-profiles-redesign/claims.json",
    "specs/072-fish-family-profiles-redesign/adjudication.md",
    "specs/072-fish-family-profiles-redesign/reference-distribution.json",
    "specs/072-fish-family-profiles-redesign/aee/freeze-aee-note.md",
    "specs/072-fish-family-profiles-redesign/build_freeze.py",
    "backend/tests/test_spec072_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
