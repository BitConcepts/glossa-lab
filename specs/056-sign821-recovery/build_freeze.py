#!/usr/bin/env python3
"""Build the Spec 056 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/056-sign821-recovery/build_freeze.py

Writes specs/056-sign821-recovery/freeze.json
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

SPEC_DIR = "specs/056-sign821-recovery"

DEFINITION = {
    "spec": "specs/056-sign821-recovery/spec.md",
    "freeze_doc": "specs/056-sign821-recovery/freeze.md",
    "experiment_id": "spec056-sign821-recovery",
    "register": {
        "path": "specs/056-sign821-recovery/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.0: after_specify cleared in "
            "adjudicated rounds over the recovered register (a loadability recovery from 0.5-draft to "
            "0.6-draft - the draft's free-form evidence kind and source_quality labels are not engine "
            "values and the loader refuses them; 57 failure modes over 0.6-draft: 14 irreducibility, 27 "
            "independence-unmodelled, 1 negation-conflict, 15 FR-2.3 draft-cap records; a final "
            "restatement of F056-C08's head cleared the last two correctness records; 15 draft-cap "
            "records only over 0.7-draft), after_plan and after_tasks clean at first pass on the final "
            "register; at every hook zero correctness failure modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.795); the engine outcome word reads iterate solely from "
            "the draft-cap records (gate reading DD-056-19; record in "
            "specs/056-sign821-recovery/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/056-sign821-recovery/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the runnable-experiments campaign "
            "plan approved AS WRITTEN (decision E-1; member 12) commissions the campaign of which "
            "design D-17 is a member; Spec 056 is D-17's specification. Draft decisions DD-056-1 to "
            "DD-056-8 are recorded in adjudication.md section 4 and are confirmed at the freeze. "
            "Freeze decisions DD-056-9 to DD-056-19 are recorded in adjudication.md section 7: the "
            "spec's own OSF contract registration filed at the freeze under E-1 (DD-056-9); the "
            "passage digest pinned byte-exactly and DD-056-1's bounds confirmed (DD-056-10); the "
            "IDENTIFICATION FAILED closure confirmed (DD-056-11); the recovered claim's placement "
            "as an appended restatement on the fragment's own record confirmed (DD-056-12); the "
            "text-only figure position confirmed - Figure 6.13 is graphic-only and does not join "
            "the passage of record (DD-056-13); the two-pass mechanics confirmed, with unsettled "
            "disagreement resolving against recovery (DD-056-14); the retirement's reach confirmed "
            "- the section 7 appends are the complete mechanical content of 'retired on the "
            "record', deleting nothing (DD-056-15); a dry-run of the sheet and checklist "
            "machinery on a non-record passage required (DD-056-16); the test-design note's "
            "minimum depth fixed, DD-056-6 confirmed (DD-056-17); Phase-418 allocated "
            "(DD-056-18); and the DD-038-10 AEE gate reading adopted as DD-056-19."
        ),
    },
    "design": {
        "phase": "Phase-418",
        "act": (
            "re-extract the pinned passage of record under the two-pass protocol of spec section 4 "
            "and apply the conjunctive recovery test of spec section 5, reaching exactly one of the "
            "four pre-registered outcomes of spec section 6 and writing it in the mechanical form "
            "of spec section 7"
        ),
        "claim_under_test": {
            "id": "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001",
            "fragment": "Sign value: 821 / it is used in a variety of contexts (Figure 6",
            "record": (
                "Phase-104 evaluation: verdict stays_untested, rule RULE-NUM - the sign number is "
                "cited without a stated numbering system, no matching entry was located in the "
                "crosswalk (86 numeric IDs then present), and the extraction carries no "
                "falsification condition; the fragment's own text is truncated mid-reference"
            ),
        },
        "falsifier": (
            "re-extraction under the section 4 protocol recovers no proposition passing the "
            "section 5 recovery test - the passage is a catalogue observation with no argument "
            "attached - in which case the outcome is RETIREMENT RECOMMENDED and the fragment is "
            "retired on the record as an extraction artefact; a candidate passing the argument "
            "conditions but failing identification at R-3 closes as IDENTIFICATION FAILED"
        ),
        "passage": {
            "document": "glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
            "start_anchor": "The Dholavira signboard, revisited",
            "end_anchor": "The Mohenjo-daro bangle pot",
            "lines": "2783-2871",
            "printed_pages": "90-94",
            "bytes": 5354,
            "sha256": "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604",
            "anchor_sentence": "Whatever sign 821 reads it is used in a variety of contexts (Figure 6.13).",
            "anchor_occurrences": 1,
            "ruling": (
                "DD-056-10 (OPEN-1 resolved): the slice from the start of the start-anchor line to "
                "the start of the end-anchor line was re-computed byte-exactly at the freeze from "
                "the pinned held text, both contents-API routes agreeing, and equals the "
                "draft-observed digest; DD-056-1's headed-section bounds are confirmed"
            ),
        },
        "figure_limit": (
            "DD-056-13 (OPEN-4 resolved): Figure 6.13 is graphic-only in the held text, present "
            "only as its caption, and the cleaned text drops the book's sign glyphs; inspection of "
            "the figure does NOT join the passage of record; a contention carried only by the "
            "figure's images or by a dropped glyph is unrecoverable under this spec, and the limit "
            "stands as a stated boundary of the recovery test, stated wherever the outcome is stated"
        ),
        "recovery_test": (
            "conjunctive, confirmed as drafted: a candidate is a recovered claim if and only if it "
            "passes all five conditions - R-1 stated from the passage's own argument, not the bare "
            "fragment restated; R-2 a specific contention a contrary finding could oppose; R-3 its "
            "subject identified under the identification rule; R-4 a falsification condition "
            "statable from the passage's own logic; R-5 the passage's stated numbers, contexts, "
            "and conditions carried with it; a candidate failing any one condition is not "
            "recovered, with the failing condition named on its checklist"
        ),
        "two_pass": (
            "DD-056-14 (OPEN-5 resolved): re-extraction is two independent executor runs over the "
            "pinned passage only, each producing an extraction sheet of candidate propositions "
            "carried by verbatim quotes with locators; each pass sees only the pinned passage and "
            "spec section 5 while extracting; reconciliation is by quotation, the candidate set "
            "is the union of the sheets, and an unsettled disagreement on the decisive candidate "
            "resolves AGAINST recovery - the candidate is treated as not recovered and the "
            "disagreement is carried into the outcome record verbatim"
        ),
        "dry_run": (
            "DD-056-16 (OPEN-7 resolved): a worked dry-run of the section 4-5 sheet and checklist "
            "machinery on a passage other than the passage of record is required, recorded before "
            "the protocol touches the fragment; it produces no candidate and no outcome"
        ),
        "identification": (
            "DD-056-11 (OPEN-2 resolved): R-3 - the sign list the passage's numbering belongs to "
            "is named from the document itself, and the drawn sign is identified by drawn form "
            "through the crosswalk registry or by the source list's own published entry quoted "
            "with its locator; matching is never by number alone; the pinned registry carries no "
            "wells_ids = W821 entry, and its Yunmapped_0821 row is a Yajnadevam glyph identifier, "
            "never the passage's sign; if a candidate passes R-1, R-2, R-4, and R-5 but R-3 cannot "
            "be satisfied, the run closes as IDENTIFICATION FAILED - neither recovered nor retired"
        ),
        "recovered_claim": {
            "placement": (
                "DD-056-12 (OPEN-3 resolved): an appended, dated restatement on the fragment's own "
                "claim record, same claim identifier, carrying the recovered proposition, its "
                "verbatim quote and locator, the named sign list and identification, the R-4 "
                "falsification condition, the R-5 numbers and conditions, and the test-design note; "
                "the fragment's original entry stands above the append, unedited"
            ),
            "lifecycle": (
                "DD-056-6 confirmed: the recovered claim enters at the created stage, status "
                "untested; recovery is not checking, explanation, or acceptance, and no output may "
                "present it as supported, checked, or digested"
            ),
            "test_note": (
                "DD-056-17 (OPEN-8 resolved): the test-design note states, at minimum, what would "
                "be checked, on what named data, against the R-4 condition; the test is designed "
                "as part of the recovery output, and no test is executed under this spec"
            ),
        },
        "retirement": {
            "ruling": (
                "DD-056-15 (OPEN-6 resolved), confirming DD-056-5: 'retired on the record' means "
                "exactly the entries spec section 7 enumerates, no more and no less, and those "
                "appends are the complete mechanical content of retirement for every program "
                "surface that presents the fragment as a claim"
            ),
            "entries": (
                "the outcome record in this directory carrying the section 6.1 wording and both "
                "extraction sheets with the reconciliation; an appended, dated disposition entry "
                "on the fragment's own claim record (disposition RETIREMENT RECOMMENDED - "
                "EXTRACTION ARTEFACT, with the passage of record and the recovery-test summary); "
                "the LEDGER entry (H1) recording the recommendation as the fragment's terminal "
                "disposition under this spec; and the experiment-graph node record (H15/H23); the "
                "execution deletes nothing, withdraws nothing, and edits no prior record - the "
                "fragment's extracted record, Phase-104 evaluation, and adopted lane-2 explanation "
                "stand unedited as its history"
            ),
        },
        "outcomes": [
            "RECOVERED",
            "RETIREMENT RECOMMENDED",
            "IDENTIFICATION FAILED",
            "CLOSED AT STEP 0",
        ],
        "step0_gates": (
            "fail-closed, in order, before any extraction pass (spec section 3): gate 0.1 input "
            "integrity - a mismatch closes as CLOSED AT STEP 0 - INPUT PIN MISMATCH, naming the "
            "input; gate 0.2 passage producible - an anchor line or the anchor sentence not "
            "located verbatim closes as CLOSED AT STEP 0 - PASSAGE NOT PRODUCIBLE; gate 0.3 "
            "passage pinnable - the slice not recomputing to the freeze-pinned digest closes as "
            "CLOSED AT STEP 0 - PASSAGE PIN MISMATCH; nothing is repaired at run time and no "
            "substitute document, edition, or passage is admitted"
        ),
        "freeze_does_not": (
            "this freeze does not itself recover or retire anything: no extraction pass has been "
            "run, no candidate has been scored against R-1..R-5, no sign has been identified, no "
            "test for any recovered claim has been designed, and the fragment stands exactly as "
            "recorded; recovery and retirement are execution outcomes under Phase-418, not freeze "
            "acts; the freeze also establishes nothing about sign 821 itself"
        ),
        "execution_gate": (
            "Not satisfied at the freeze of 2026-10-21: execution runs as Phase-418 only after "
            "this freeze has merged, the OSF contract registration's approval act has completed "
            "(the parent's approval click on OSF's admin notification), and a separate execution "
            "order is given, in campaign Wave 3 group 2"
        ),
    },
    "inputs": {
        "claim_file": {
            "file": "glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json",
            "sha256": "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a",
            "claim_id": "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001",
            "posture": (
                "the freeze-time hash is carried as this definition constant in the Spec 038 "
                "form: the extracted-claims store is regenerated by the backend suite, so the "
                "freeze tests assert the constant plus the fragment's facts on the live file, "
                "never a live-file hash on it"
            ),
        },
        "held_text": {
            "file": "glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
            "sha256": "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e",
        },
        "passage": {
            "sha256": "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604",
            "bytes": 5354,
            "lines": "2783-2871",
        },
        "phase104_evaluation": {
            "file": "glossa-indus/reports/phase104_claims_evaluation.json",
            "sha256": "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d",
            "claim_id": "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001",
            "verdict": "stays_untested",
            "rule": "RULE-NUM",
        },
        "registry": {
            "file": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
            "rows": 803,
            "w821_entries": 0,
            "trap": "the Yunmapped_0821 row is a Yajnadevam glyph identifier, not Wells's 821 (spec section 5, R-3)",
        },
        "lane2_drafts": {
            "file": "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
            "sha256": "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "posture": "this spec moves no anchor; the file is asserted byte-identical before and after any execution",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every pin above was re-derived by two independent "
            "routes (contents-API raw and git-blob) at main "
            "e339996194e1dd3c5336d87da37be0d5b0765556; the two routes agree byte-for-byte on "
            "every file and every hash equals its pin (freeze.md section 2)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.0 (adopted environment; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec056_freeze.py",
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
