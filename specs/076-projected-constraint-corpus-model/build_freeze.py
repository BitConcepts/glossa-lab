#!/usr/bin/env python3
"""Build the Spec 076 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-26. The register was drafted directly in
the recovered (0.7) form, the AEE lifecycle hooks
ran over it at the freeze with the pinned
evaluator (aee 1.5.3), and the digest is computed
over the register exactly once, at the freeze -
the Spec 035 ordering. This freeze is a
required-C4 freeze (the check became a required
branch-protection check after the Spec 075 shadow
freeze): the gate records under gate-records/ are
filed beside this record and are summarized in
freeze.md. Run with the Glossa backend venv python
from the repository root:

    python specs/076-projected-constraint-corpus-model/build_freeze.py

Writes specs/076-projected-constraint-corpus-model/freeze.json
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

SPEC_DIR = "specs/076-projected-constraint-corpus-model"

DEFINITION = {
    "spec": "specs/076-projected-constraint-corpus-model/spec.md",
    "freeze_doc": "specs/076-projected-constraint-corpus-model/freeze.md",
    "experiment_id": "spec076-projected-constraint-corpus-model",
    "register": {
        "path": "specs/076-projected-constraint-corpus-model/claims.json",
        "register_version": "0.7-draft",
        "claims": 10,
        "aee_hook_pass": (
            "Run at the freeze act of 2026-10-26 under the pinned evaluator "
            "aee 1.5.3 in the freeze configuration (assess --lenient "
            "--no-ledger, phases after_specify / after_plan / after_tasks): "
            "each of the three artifacts carries 19 findings - the 10 FR-2.3 "
            "draft caps (one per claim), 8 irreducibility challenges "
            "(F076-C01, C03, C04, C06, C07, C08, C09, C10) and 1 "
            "counterexample challenge (F076-C09) - zero findings of "
            "contradiction, independence, ambiguity, or evidence-resolution "
            "kind, and no claim below the 0.70 confidence threshold "
            "(minimum propagated 0.7200). The challenges are answered in "
            "aee/freeze-aee-note.md from the spec's own structure (the "
            "assumption set is itself filed as four separate claims, "
            "C04-C07; C09's universality is its content) and ruled at "
            "adjudication DD-076-3; the register was not reworded to "
            "silence them"
        ),
    },
    "basis": {
        "adjudication": "specs/076-projected-constraint-corpus-model/adjudication.md",
        "decisions": (
            "DD-076-1 to DD-076-7 at the adjudication (numbering 076 / "
            "Phase 442; the 10-claim set carrying the M12 design's "
            "D-M12-C01/C02/C03 and its assumption set as claims; the "
            "freeze-fixed completions FF-1 to FF-5; the A-KEY ruling "
            "DD-076-4; no OSF registration at this freeze, DD-076-5, the "
            "M12 design naming none; this freeze a required-C4 freeze, "
            "DD-076-7)"
        ),
        "design": (
            "the M12 design draft of 2026-10-26 (programme goal record; "
            "SHA-256 8945399d7621f9db9286ce3773538c0b9821a93f07d400556366fe0a474a4122), "
            "carried as written except the freeze-fixed completions of "
            "spec section 0"
        ),
    },
    "design": {
        "phase": "Phase 442",
        "question": (
            "What does the attested corpus, treated as a constraint "
            "system, demand of any completion - in particular of the "
            "signs we do not have: bounded possibility sets, forced "
            "exclusions, and forced co-variations, derived by exact "
            "census deduction within one pinned frame under a stated "
            "assumption set, never by scoring a proposed reading"
        ),
        "method": (
            "Tier-C census deduction over the nine-type positional "
            "vocabulary of spec section 3.4 (a sign's possibility set is "
            "the types its census row does not contradict); three tiers "
            "(C census / S structural under filed assumptions / T "
            "tendencies, annexed and never upgraded); every register "
            "entry carries its frame pin, assumption set, derivation "
            "route, and falsifier; the register records set membership, "
            "never identity"
        ),
        "pilot": (
            "Spec section 8, executed once after this freeze merges "
            "(FF-5): step 0 reproduction gate over the section 7 census "
            "(2,906 records to 11,507 tokens; 5,883 strict tokens; the "
            "slot identities exact; the finals partition summing to "
            "2,655), closing CANNOT BE RUN AS WRITTEN on any mismatch; "
            "step 1 derivation reproducing the pre-named headline "
            "numbers (677 exclusions over the 122 no-anchor signs; "
            "finals residual 178; solo-only set 13); step 2 the "
            "marginals-preserving shuffle null (B = 999, seed 20261026; "
            "label permutation named invalid in advance); step 3 the "
            "blind positive control over the 94 strict signs under "
            "coding rules CR-1 to CR-7"
        ),
        "bars": (
            "Frozen, from the design, not movable after the freeze: "
            "(i) the real U2 finals residual 178 falls below the null's "
            "5th percentile; (ii) the real solo-only count 13 exceeds "
            "the null's 95th percentile; (iii) the positive control "
            "excludes at most 5 of the 94 strict claimed types "
            "(frame-absent strict signs on their own line under CR-7)"
        ),
        "closures": [
            "PILOT PASSES",
            "CANNOT BE RUN AS WRITTEN",
            "THE FRAME'S CONSTRAINT STRUCTURE IS NOT DISTINGUISHABLE FROM A MARGINALS-PRESERVING SCRAMBLE IN THE TESTED FAMILY",
            "ASSUMPTION SET DOES NOT HOLD",
            "NOT-RUN",
        ],
        "osf": (
            "No OSF registration is filed at this freeze (DD-076-5): "
            "the M12 design's filing provisions name none, and the repo "
            "freeze record governs; the absence is recorded in "
            "freeze.md, not improvised around"
        ),
        "execution_gate": (
            "Phase 442's pilot executes only against this frozen "
            "record, on the owner's order of 2026-10-26 (freeze and "
            "run), after the freeze PR merges on genuine CI including "
            "the required C4 check; one run, as frozen (FF-5); a "
            "premise failure is a halt-and-report under the design's "
            "own closure words, never an invitation to adjust a bar, "
            "the frame, or the null"
        ),
        "limits": (
            "The register narrows a space it does not prove non-empty; "
            "no reading, value, or identification for any sign; "
            "frame-relativity is stated on every entry; the 24 "
            "frame-absent signs file empty constraint sets as a "
            "finding; M4's gate is untouched (the ranking feeds it "
            "ordering only, if it ever lifts) and M7's attack remains "
            "M7's (the register feeds it bounds only); the script is "
            "not deciphered"
        ),
    },
    "inputs": {
        "corpus_export": {
            "path": "glossa-corpus/indus/exports/indus_research.jsonl",
            "sha256": "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e",
            "m77_records": 2906,
            "frame": {
                "tokens": 11507,
                "dropped_placeholder_000": 680,
                "dropped_marked_star": 452,
                "strict_tokens": 5883,
                "nonempty_sequences": 2880,
                "distinct_signs": 393,
                "slot_totals": {"init": 2655, "fin": 2655, "solo": 225, "med": 5972},
                "finals_partition": {"strict": 1707, "pending": 250, "anchored_other": 520, "no_anchor": 178},
            },
        },
        "anchors": {
            "path": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "entries": 287,
            "strict": 94,
            "pending": 44,
        },
        "registry_v2": {
            "path": "data/crosswalks/canonical_sign_registry_v2.csv",
            "sha256": "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71",
            "rows": 1013,
        },
        "pin_verification": (
            "verified first-hand at the freeze act of 2026-10-26 from "
            "repo main: the export's, anchors', and Registry v2's "
            "digests recomputed from the files as fetched from main "
            "equal the design's pins; the section 7 census re-derived "
            "from those files reproduces every pre-named figure exactly "
            "(11,507 tokens; 5,883 strict; the identities; the "
            "partition; 677 exclusions; solo-only 13; the absent 24); "
            "every gate-turning quantity independently recomputed for "
            "the C2 record in gate-records/ by a worker who did not "
            "draft the spec"
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
    "backend/tests/test_spec076_freeze.py",
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
