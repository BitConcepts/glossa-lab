#!/usr/bin/env python3
"""Build the Spec 078 freeze record (freeze.json).

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

    python specs/078-projected-constraint-bridge-redesign/build_freeze.py

Writes specs/078-projected-constraint-bridge-redesign/freeze.json
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

SPEC_DIR = "specs/078-projected-constraint-bridge-redesign"

DEFINITION = {
    "spec": "specs/078-projected-constraint-bridge-redesign/spec.md",
    "freeze_doc": "specs/078-projected-constraint-bridge-redesign/freeze.md",
    "experiment_id": "spec078-projected-constraint-bridge-redesign",
    "register": {
        "path": "specs/078-projected-constraint-bridge-redesign/claims.json",
        "register_version": "0.7-draft",
        "claims": 10,
        "aee_hook_pass": (
            "Run at the freeze act of 2026-10-26 under the pinned evaluator "
            "aee 1.5.3 in the freeze configuration (assess --lenient "
            "--no-ledger, phases after_specify / after_plan / after_tasks): "
            "each of the three artifacts carries 19 findings - the 10 FR-2.3 "
            "draft caps (one per claim) and 9 irreducibility challenges "
            "(F078-C01, C02, C03, C04, C06, C07, C08, C09, C10) - zero "
            "findings of contradiction, independence, ambiguity, or "
            "evidence-resolution kind, and no claim below the 0.70 "
            "confidence threshold (minimum propagated 0.7200). The "
            "challenges are answered in aee/freeze-aee-note.md from the "
            "spec's own structure (the inherited assumption set is itself "
            "filed as separate claims, C04/C05/C07; A-FACE-2's two "
            "falsification tests are its two named deaths, not two claims) "
            "and ruled at adjudication DD-078-4; the register was not "
            "reworded to silence them"
        ),
    },
    "basis": {
        "adjudication": "specs/078-projected-constraint-bridge-redesign/adjudication.md",
        "decisions": (
            "DD-078-1 to DD-078-7 at the adjudication (numbering 078 / "
            "Phase 444; the 10-claim set carrying the M13 design's "
            "D-M13-C04/C02/C03, A-FACE-2 as C06, and the inherited "
            "assumptions A-FRAME / A-DIR / A-KEY as claims; the "
            "freeze-fixed completions FF-078-1 to FF-078-5; the "
            "freeze-prep review outcome, no amendments required; an OSF "
            "registration IS filed at this freeze under the owner's "
            "express order, DD-078-5, in contrast to DD-076-5; the S4 "
            "note ruling, DD-078-6; this freeze a required-C4 freeze, "
            "DD-078-7)"
        ),
        "design": (
            "the M13 design draft of 2026-10-26 (programme goal record; "
            "SHA-256 8bb02c07a8ad3245a899da660c48430b4cf1e16a53b1fb53a132215093e9a211), "
            "carried as written except the freeze-fixed completions of "
            "spec section 0; parent record: the Spec 076 pilot record of "
            "2026-10-26 (ASSUMPTION SET DOES NOT HOLD; freeze digest "
            "83259ed3d3a20189e5c22e4645d26452c9c3b79a60348b3f5c38b8405addde9a)"
        ),
    },
    "design": {
        "phase": "Phase 444",
        "question": (
            "Does the redesigned bridge - the two-axis pair-form "
            "vocabulary, coding rules NC-1 to NC-8, and the successor "
            "assumption A-FACE-2 - carry the strict core's basis language "
            "into checkable claims without manufacturing contradictions, "
            "on the foundation Spec 076's pilot established (the census "
            "sound, the frame's constraint structure beyond its "
            "marginals) and against the failure it measured (36 "
            "exclusions under the one-axis bridge)"
        ),
        "method": (
            "A claim about a sign is a pair: a distributional component "
            "(M12 section 3.4's nine types, inherited unchanged; only "
            "this component can be contradicted by a census row) and a "
            "functional component (TERM-FUNC / INIT-FUNC / MED-FUNC / "
            "SOLO-FUNC, committing only to anchor attestation in the "
            "register and to anchor-share coherence in the pilot); "
            "basis language is coded at the strength at which it is "
            "stated under NC-1 to NC-8 (universal language as type-claims, "
            "functional language as functional claims, sample-marked "
            "language as summaries that file no checkable claim); a "
            "register entry is a triple (distributional possibility set, "
            "functional possibility set with anchor counts, claims "
            "ledger) recording membership and attested support, never "
            "identity"
        ),
        "pilot": (
            "Spec section 7, executed once after this freeze merges "
            "(FF-078-5): step 0 re-verification of the inherited census "
            "from the pins (2,906 records to 11,507 tokens; 5,883 strict "
            "tokens; slot totals 2,655 / 2,655 / 225 / 5,972; the finals "
            "partition summing to 2,655; headline numbers 677 / 178 / "
            "13), closing CANNOT BE RUN AS WRITTEN on any mismatch and "
            "voiding the inherited step-2 standing in the same record; "
            "step 2 not re-run (inherited standing from Spec 076: both "
            "shuffle bars passed, B = 999, seed 20261026); step 3-prime "
            "the blind positive control over the 94 strict signs under "
            "NC-1 to NC-8 and the FF-078-3 blindness protocol, on the "
            "counted population of 86 under FF-078-2 (frame-attested "
            "strict signs minus the worked examples M002, M342, M347; "
            "frame-absent strict signs on the NC-8 line)"
        ),
        "bars": (
            "Frozen, from the design, not movable after the freeze: "
            "the positive control passes iff total failures "
            "(distributional + functional) are at most 3 among the "
            "counted population of 86, with neither line exceeding 2, "
            "no pattern under FF-078-4, and administrability of at "
            "least 25 of the 86 counted signs yielding at least one "
            "checkable claim"
        ),
        "closures": [
            "PILOT PASSES",
            "CANNOT BE RUN AS WRITTEN",
            "CANNOT BE ADMINISTERED — THE CORE MAKES TOO FEW CHECKABLE CLAIMS",
            "BRIDGE DOES NOT HOLD",
            "NOT-RUN",
        ],
        "osf": (
            "An OSF registration IS filed at this freeze (DD-078-5) "
            "under the owner's express order for M13, in contrast to "
            "Spec 076's DD-076-5 where the design named none and none "
            "was filed; the coordinator performs the filing after merge "
            "via the ORCID/token-link route, and the registration "
            "identifier is recorded with the pilot record"
        ),
        "execution_gate": (
            "Phase 444's pilot executes only against this frozen "
            "record, on the owner's order of 2026-10-26 (review, freeze, "
            "and run), after the freeze PR merges on genuine CI "
            "including the required C4 check; one run, as frozen "
            "(FF-078-5); a premise failure is a halt-and-report under "
            "the design's own closure words, never an invitation to "
            "adjust a bar, the frame, or the coding rules"
        ),
        "limits": (
            "No register exists unless the pilot passes; the register "
            "records membership and attested support, never identity, "
            "on either axis; the pilot's coherence statistic never "
            "enters a register entry; no reading, value, or "
            "identification for any sign; M4's gate is untouched (the "
            "ranking feeds it ordering only) and M7's attack remains "
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
                "base_rates": {"init": 0.2307, "fin": 0.2307, "med": 0.519, "solo": 0.0196},
                "counted_population": {
                    "strict": 94, "frame_absent": 5, "frame_attested": 89,
                    "worked_examples": 3, "counted": 86,
                },
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
            "equal the design's pins; the inherited census re-derived "
            "from those files reproduces every pre-named figure exactly "
            "(11,507 tokens; 5,883 strict; the slot totals; the "
            "partition; 677 exclusions; solo-only 13; base rates to "
            "4dp; the counted population 86 under FF-078-2); every "
            "gate-turning quantity independently recomputed for the C2 "
            "record in gate-records/ from the pinned inputs only, by a "
            "fresh recomputation that does not import the spec's "
            "derivation code"
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
    "backend/tests/test_spec078_freeze.py",
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
