#!/usr/bin/env python3
"""Build the Spec 048 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (campaign Wave 2, under the campaign
plan approved AS WRITTEN on 2026-10-21; the draft
PR #247 carried no builder and no draft digest).
After the AEE lifecycle hooks passed over the
recovered register (0.7-draft), it computed the
final digest over the frozen contract exactly
once, and its DEFINITION text was finalised in
the same act (the Spec 035 pattern). Run with
the Glossa backend venv python from the
repository root:

    python specs/048-parpola-fish-family-profiles/build_freeze.py

Writes specs/048-parpola-fish-family-profiles/freeze.json
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

SPEC_DIR = "specs/048-parpola-fish-family-profiles"

DEFINITION = {
    "spec": "specs/048-parpola-fish-family-profiles/spec.md",
    "freeze_doc": "specs/048-parpola-fish-family-profiles/freeze.md",
    "experiment_id": "spec048-parpola-fish-family-profiles",
    "register": {
        "path": "specs/048-parpola-fish-family-profiles/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 "
            "under aee 1.5.0: the 0.5-draft register "
            "was refused at load (evidence kind and "
            "source_quality values outside the adopted "
            "engine's enums); normalised to the frozen "
            "house form at 0.6-draft; after_specify "
            "round 1 over 0.6-draft returned 48 failure "
            "modes (15 irreducibility, 17 independence, "
            "1 circular-inference on the C01/C05 "
            "dependency cycle, 15 FR-2.3 draft-cap "
            "records); recovered to 0.7-draft on the "
            "Spec 039 pattern (single head propositions, "
            "carried clauses in boundaries, "
            "independent_of declarations, C01 as root); "
            "round 2 carried 5 independence records and "
            "1 negation-conflict (C03 against C04), "
            "cleared by mutual independence declarations, "
            "boundary_confirmation metadata on the "
            "C03/C04 pair, and C04's head restated under "
            "a distinct subject; the final after_specify "
            "round and first passes at after_plan and "
            "after_tasks each carry 15 FR-2.3 draft-cap "
            "records only; at every hook zero correctness "
            "failure modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); the "
            "engine outcome word reads iterate solely "
            "from the draft-cap records (gate reading "
            "DD-048-17; record in "
            "specs/048-parpola-fish-family-profiles/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/048-parpola-fish-family-profiles/adjudication.md"
        ),
        "decisions": (
            "The runnable-experiments campaign plan, "
            "approved by the owner AS WRITTEN on "
            "2026-10-21, commissions this spec (Wave 1 "
            "member 3, design D-04; Asset F consumed "
            "here under E-6; Roif gate under E-2 / R-7; "
            "an OSF contract registration per spec at "
            "its freeze under E-1), and the Wave 2 "
            "freeze wave was delegated under that "
            "approval. Freeze decisions are recorded in "
            "adjudication.md section 7: DD-048-9 "
            "records the coordinator's Asset F "
            "pin-timing ruling as a decided item "
            "(OPEN-048-1); OPEN-048-2 confirmed - the "
            "strict corpus is the Spec 033 section 4 "
            "V3 / Mahadevan-lineage corpus with the "
            "gate-0.3 T2.4 reproduction (DD-048-10); "
            "OPEN-048-3 confirmed - the member bar is "
            "20% (DD-048-11); OPEN-048-4 confirmed - "
            "DD-048-4, the second arm is integral "
            "(DD-048-12); OPEN-048-5 decided - the "
            "control matching rule fixed and DD-048-7 "
            "confirmed (DD-048-13); OPEN-048-6 "
            "decided yes - own OSF registration under "
            "E-1 (DD-048-14); OPEN-048-7 confirmed - "
            "DD-048-5, the join via mahadevan_number "
            "with the UNMAPPED disposition "
            "(DD-048-15); OPEN-048-8 allocated "
            "Phase-408 (DD-048-16); DD-048-17 adopts "
            "the DD-038-10 AEE gate reading; "
            "DD-048-18 corrects the anchors fact for "
            "sign 72 (M072 exists, pending_non_sa_"
            "validation, not a strict reading)."
        ),
    },
    "design": {
        "phase": "Phase-408",
        "act": (
            "test Parpola's fish-sign family sign by "
            "sign under the Phase-43 T2.4 "
            "ending-follower measure on the strict "
            "corpus, repeated on the Holdat layer as a "
            "second arm, over family membership fixed "
            "in advance by Asset F as frozen at Spec "
            "044's step 0 and consumed by digest "
            "assertion at gate 0.1"
        ),
        "claim": {
            "id": "parpola_2010_dravidian_solution_manual_002",
            "state": (
                "IN QUESTION, partially supported: sign "
                "72 passed Phase-43 T2.4 and sign 267, "
                "the family's most frequent member, "
                "failed it; that split record is not "
                "re-adjudicated by this spec beyond the "
                "family verdict of section 6"
            ),
            "not_understood": (
                "the claim record's not-understood text: "
                "the same test run sign by sign across "
                "the whole fish family on the strict "
                "corpus, with the family's membership "
                "fixed in advance"
            ),
        },
        "asset_f": {
            "open": "OPEN-048-1 (ruled at freeze, DD-048-9)",
            "contract_anchor": {
                "freeze_digest": (
                    "6851f943d196fa389e48b67cb5161b90daa1"
                    "180d8a3e1cf3f020fcf25691d9c8"
                ),
                "source": (
                    "Spec 044's freeze digest, read at "
                    "this freeze from PR #243's branch "
                    "(head 66d4fd37) - Spec 044's "
                    "freeze had not yet merged when "
                    "read; the value is its corrected "
                    "freeze digest, superseding its "
                    "first freeze digest 9a0e6518 under "
                    "its own pre-merge test repair "
                    "(its freeze.md section 5)"
                ),
                "contract": (
                    "Spec 044 section 4: the canonical "
                    "file asset-f-fish-family.json (UTF-8, "
                    "keys sorted, members sorted by "
                    "sign_key, nine required member "
                    "fields), built solely from Parpola's "
                    "published list (Parpola 1994, "
                    "fig. 5.1, pp. 70-78), the digest the "
                    "SHA-256 of the canonical bytes with "
                    "the digest field itself excluded"
                ),
            },
            "pin_source": {
                "record": "Spec 044's step-0 outcome record",
                "asset_file": (
                    "specs/044-fish-sign-coastal-residue/"
                    "asset-f-fish-family.json"
                ),
                "posture": (
                    "the step-0 outcome record is the "
                    "results JSON deliverable of Spec "
                    "044 section 9, produced at Spec "
                    "044's execution step 0 (Wave 3); it "
                    "is the only authoritative statement "
                    "of Asset F's byte-digest (Spec 044 "
                    "section 4.4)"
                ),
            },
            "gate_0_1": (
                "at EXECUTION step 0 the exhibited "
                "canonical file is recomputed over its "
                "exact bytes with the digest field "
                "excluded and compared to the digest in "
                "the pin source: absence of the file or "
                "of the record closes ASSET F NOT "
                "AVAILABLE; a mismatch closes ASSET F "
                "DIGEST MISMATCH; in neither case is any "
                "count computed and the asset is never "
                "rebuilt, re-derived, or substituted "
                "under this spec"
            ),
        },
        "join": {
            "via": (
                "each Asset F member's mahadevan_number "
                "locator, through the pinned "
                "Mahadevan-Parpola crosswalk (gate 0.2); "
                "locators are never membership criteria"
            ),
            "unmapped": (
                "DD-048-5, confirmed at freeze "
                "(DD-048-15): a member carrying no "
                "Mahadevan mapping is recorded UNMAPPED, "
                "listed in the step-0 record with the "
                "reason, and excluded from both arms' "
                "weighting; it is never silently dropped "
                "and never counted as TOO THIN"
            ),
            "cross_check": (
                "the step-0 record reports Asset F's "
                "membership against the claim record's "
                "trio (Mahadevan 72, 64, 70) and the "
                "Phase-43 six candidates (267, 72, 65, "
                "59, 60, 70), every divergence named; "
                "the cross-check adds and removes no "
                "member"
            ),
        },
        "strict_corpus": {
            "open": "OPEN-048-2 (confirmed at freeze, DD-048-10)",
            "reading": (
                "the strict corpus is the program's "
                "V3 / Mahadevan-lineage corpus of "
                "Spec 033 section 4, as held in the "
                "database, identified, exported whole, "
                "and pinned by digest at gate 0.3; it "
                "is not a restriction of counted signs "
                "to the 94 strict_sa_independent "
                "readings, which would exclude sign 72 "
                "itself (DD-048-18)"
            ),
            "reproduction": {
                "candidates": [267, 72, 65, 59, 60, 70],
                "sign_72": {
                    "occurrences": 181,
                    "terminal_frac": 0.259,
                    "supported": True,
                },
                "sign_267": {
                    "occurrences": 356,
                    "terminal_frac": 0.038,
                    "supported": False,
                },
            },
            "closure": (
                "if the layer cannot be uniquely "
                "identified, cannot be exported whole, "
                "or the reference points do not "
                "reproduce, the execution closes as "
                "STRICT CORPUS NOT PINNABLE and nothing "
                "is counted"
            ),
        },
        "test": {
            "measure": (
                "the Phase-43 T2.4 ending-follower rate, "
                "unchanged, per mapped Asset F member, "
                "in the primary arm and repeated on the "
                "Holdat layer as the second arm"
            ),
            "member_bar": 0.20,
            "bar_open": (
                "OPEN-048-3 (confirmed at freeze, "
                "DD-048-11): the bar sits between sign "
                "72's recorded 0.259 (supported) and "
                "sign 267's recorded 0.038 (not "
                "supported), exactly as design D-04 "
                "fixed it"
            ),
            "family_lines": {
                "supported": 0.70,
                "not_supported": 0.30,
            },
            "family_rule": (
                "over tested members (mapped, at or "
                "above the floor), the passing members' "
                "token-weighted share of tested "
                "occurrences: at least 70% FAMILY "
                "SUPPORTED, at most 30% FAMILY NOT "
                "SUPPORTED, between or on a cross-arm "
                "disagreement about the most frequent "
                "tested member INCONCLUSIVE"
            ),
            "floor": 30,
            "second_arm": (
                "integral (DD-048-4, confirmed at "
                "freeze as DD-048-12): a Holdat layer or "
                "per-sign crosswalk failure closes the "
                "execution as SECOND ARM NOT RUNNABLE; "
                "crosswalk-conflict pairs are reported "
                "separately in both arms, never silently "
                "dropped"
            ),
            "sensitivity": (
                "the family verdict recomputed over "
                "only signs 72, 64, 70 (Asset F members, "
                "mapped, above the floor), reported "
                "alongside, never verdict-changing "
                "beyond section 6's stated rule"
            ),
        },
        "controls": {
            "open": "OPEN-048-5 (fixed at freeze, DD-048-13)",
            "matching_rule": (
                "a non-fish animal sign qualifies iff "
                "its published animal identification is "
                "citable from the program's records, "
                "its primary-corpus total is at least "
                "30, and its total lies between half "
                "the smallest tested member's total and "
                "twice the largest tested member's "
                "total; the set is enumerated in the "
                "step-0 record at gate 0.6 before any "
                "follower quantity is computed"
            ),
            "comparison": (
                "DD-048-7, confirmed: 'same rate' means "
                "the controls' token-weighted passing "
                "share at or above the family's; on "
                "that case the outcome record reports "
                "the fish result as a positional fact, "
                "not as support for the reading"
            ),
        },
        "outcomes": [
            "FAMILY SUPPORTED",
            "FAMILY NOT SUPPORTED",
            "INCONCLUSIVE",
            "TOO THIN",
            "ASSET F NOT AVAILABLE",
            "ASSET F DIGEST MISMATCH",
            "STRICT CORPUS NOT PINNABLE",
            "SECOND ARM NOT RUNNABLE",
            "INVALID",
        ],
        "fences": (
            "the Roif hold binds every output (records "
            "internal; campaign reporting names this "
            "member only as executed - held under the "
            "Roif gate, without result content); no "
            "outcome establishes what any fish sign was "
            "pronounced or meant; no outcome explains "
            "why sign 267 behaves differently; sign "
            "identities are compilation-relative to "
            "the two pinned arms and their crosswalk"
        ),
        "execution_gate": (
            "Execution is Phase-408 under this frozen "
            "contract, on a separate owner execution "
            "order, and awaits the verified approval "
            "of this spec's OSF contract registration "
            "(OPEN-048-6; osf-spec-registration.md); "
            "no count was made at the freeze itself, "
            "Asset F has not been built, no corpus "
            "layer has been pinned, and no member is "
            "named beyond the record's own reference "
            "signs"
        ),
    },
    "inputs": {
        "claim_file": {
            "file": (
                "glossa-indus/claims/extracted_claims/"
                "parpola_2010_dravidian_solution.json"
            ),
            "sha256": (
                "3202aeca1ddaf7e588ebf19b2eaf8c93d06a3"
                "4ecebba20d06c1b22810dfb000c"
            ),
            "entry": "parpola_2010_dravidian_solution_manual_002",
            "claim_status": "partially_supported",
            "stage": "explained",
        },
        "phase43": {
            "file": "outputs/phase43_all.json",
            "sha256": (
                "78a6c21908b9362854c54dd3d820d717be22f"
                "eab3af11135663fa14aaf554fe4"
            ),
            "section": "T2_4_fish_rebus",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": (
                "df0cf620a0d66b71d778300b93a91d96b2f30f2"
                "3580088e6086592b32d34f569"
            ),
            "total": 287,
            "strict_sa_independent": 94,
            "m072_status": (
                "pending_non_sa_validation (DD-048-18: "
                "the entry exists; it is not one of the "
                "94 strict readings)"
            ),
            "posture": (
                "asserted at the freeze from a fresh "
                "recompute; this spec moves no anchor; "
                "the file is asserted byte-identical "
                "before and after any execution"
            ),
        },
        "crosswalk": {
            "file": (
                "backend/glossa_lab/data/"
                "mahadevan_parpola_crosswalk.json"
            ),
            "sha256": (
                "9ebd7723472d888dc8a127ff840a108d4fbd546"
                "f7f8ed28ccc6e06444a2dc69b"
            ),
            "citation": (
                "Parpola, Asko. 1994b. Sign list "
                "(= Parpola 1994a fig. 5.1, pp. 70-78)"
            ),
        },
        "spec033": {
            "file": "specs/033-sa-free-language-comparison/spec.md",
            "sha256": (
                "eaea0e2e4f288e199acfa56cc401b80b5939175"
                "578ccb5f52c87adddf2f15ca9"
            ),
            "statement": (
                "section 4: the corpus is the program's "
                "V3/Mahadevan-lineage corpus as held in "
                "the database; the strict sign set is "
                "the 94 strict_sa_independent readings"
            ),
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every pin "
            "above was re-derived by two independent "
            "routes (contents-API raw and git-blob) at "
            "main 0cf9cd2f339328007c01b7909b77282e778e25e2; "
            "the two routes agree byte-for-byte on "
            "every file and every hash equals its pin "
            "(adjudication.md section 8)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-aee150)",
        "aee": "1.5.0 (adopted environment, PR #231; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec048_freeze.py",
]


def main() -> None:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(record["digest"])


if __name__ == "__main__":
    main()
