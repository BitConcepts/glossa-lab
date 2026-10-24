#!/usr/bin/env python3
"""Build the Spec 055 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/055-sign900-numeral/build_freeze.py

Writes specs/055-sign900-numeral/freeze.json
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

SPEC_DIR = "specs/055-sign900-numeral"

DEFINITION = {
    "spec": "specs/055-sign900-numeral/spec.md",
    "freeze_doc": "specs/055-sign900-numeral/freeze.md",
    "experiment_id": "spec055-sign900-numeral",
    "register": {
        "path": "specs/055-sign900-numeral/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.0: after_specify cleared in "
            "adjudicated rounds over the recovered register (a loadability recovery from 0.5-draft to "
            "0.6-draft - the draft's free-form evidence kind and source_quality labels are not engine "
            "values and the loader refuses them; 53 failure modes over 0.6-draft: 14 irreducibility, 22 "
            "independence-unmodelled, 2 negation-conflict, 15 FR-2.3 draft-cap records; a final "
            "restatement of F055-C13's head cleared the last two correctness records; 15 draft-cap "
            "records only over 0.7-draft), after_plan and after_tasks clean at first pass on the final "
            "register; at every hook zero correctness failure modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); the engine outcome word reads iterate solely from "
            "the draft-cap records (gate reading DD-055-18; record in "
            "specs/055-sign900-numeral/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/055-sign900-numeral/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the runnable-experiments campaign "
            "plan approved AS WRITTEN (decisions E-1, E-7; member 11) commissions the campaign of "
            "which design D-15 is a member; Spec 055 is D-15's specification. Draft decisions "
            "DD-055-1 to DD-055-8 are recorded in adjudication.md section 4 and are confirmed at "
            "the freeze. Freeze decisions DD-055-9 to DD-055-18 are recorded in adjudication.md "
            "section 7: the spec's own OSF contract registration filed at the freeze under E-1 "
            "(DD-055-9); the recovery-record form confirmed - source-table-recovery.json, schema "
            "glossa.source-table-recovery/1, on every terminal outcome (DD-055-10); the control-set "
            "rule and directional median clause confirmed (DD-055-11); the occurrence floor "
            "confirmed at 5 (DD-055-12); the strict-corpus pinning posture confirmed - pinned at "
            "execution gate 0.4, no freeze-time pin, with the reason (DD-055-13); hedged numeral-set "
            "members excluded and listed separately (DD-055-14); positional entropy confirmed as "
            "Shannon entropy in bits over positions as stored (DD-055-15); a dry-run on a "
            "non-target sign required (DD-055-16); Phase-414 allocated (DD-055-17); and the "
            "DD-038-10 AEE gate reading adopted as DD-055-18."
        ),
    },
    "design": {
        "phase": "Phase-414",
        "act": (
            "identify the sign the source document numbers 900 (stage 1, the source-table recovery "
            "of spec sections 4 and 6), then - only if identified - test its numeral behaviour on "
            "the pinned strict corpus under the three frozen measures of spec section 5"
        ),
        "claim_under_test": {
            "id": "ancient_writing_and_modern_technologies_51831ac9_sign_val_0001",
            "fragment": "Sign value: 900 / number six",
            "record": (
                "Phase-104 evaluation: verdict stays_untested, rule RULE-NUM - the sign number is "
                "cited without a stated numbering system, no matching entry was located in the "
                "crosswalk (86 numeric IDs then present), and the extraction carries no "
                "falsification condition"
            ),
        },
        "falsifier": (
            "two-stage: the source document does not identify the sign - its list cannot be named "
            "from the document's own text, or the drawn sign its number 900 labels cannot be "
            "matched - closing as IDENTIFICATION FAILED (a pre-registered outcome, in two "
            "sub-classes: list unnamed, sign unmatched); or, identification having succeeded, the "
            "identified sign's behaviour contradicts the numeral reading under spec section 5.3 "
            "(NOT NUMERAL-LIKE, or MIXED where the measures split)"
        ),
        "recovery": {
            "file": "source-table-recovery.json",
            "schema": "glossa.source-table-recovery/1",
            "produced": (
                "on every terminal outcome, including step-0 and identification closures, "
                "carrying its closure block and whatever recovery material was established "
                "before the closure"
            ),
            "ruling": "DD-055-10 (OPEN-1 confirmed): the form of spec section 6 stands as fixed by DD-055-1",
            "contents": [
                "the document's sign-list naming statements, quoted verbatim with locators",
                "the complete Sign 900 section, verbatim with locator",
                "the complete Numerical value of Sign 900 section including its Table 1, verbatim with locator",
                "the summary statement, verbatim with locator",
                "the figure captions carrying the drawn sign (Figures 11, 12, 29)",
                "the target_sign block: match basis, registry id or named-list locator, citation",
                "the sign_700_material block: locators only, no finding",
                "the recovery outcome, with the section 5.4 wording in closure where not IDENTIFIED",
            ],
        },
        "matching": (
            "drawn form only: the sign the document numbers 900 is matched by its drawn form to a "
            "crosswalk-registry entry or to the named list's own entry for 900, with the citation "
            "attached; never by number and never by registry string. The trap is carried: the "
            "registry as held today (803 rows) contains a W900 value inside the wells_ids cell of "
            "the P154 row (Right parenthesis, corpus frequency 93); that cell neither identifies "
            "nor excludes this fragment's sign (F055-C07)"
        ),
        "chain_rule": (
            "campaign decision E-7: the step-1 recovery is the act that would unblock design "
            "D-16, and its output does NOT admit D-16 to this campaign, in whole or in part, even "
            "if the recovery fully succeeds; no campaign member consumes the recovery record; the "
            "recovered document's sign-700 statements are recorded by locator only, adjudicated "
            "in no way; D-16 waits for its own planning gate"
        ),
        "not_six": (
            "no outcome of this spec establishes the value six: even NUMERAL-LIKE establishes only "
            "that the identified sign behaves as a numeral behaves; the source document's own "
            "argument for six is preserved in the recovery record as source material and is never "
            "cited as evidence at the behaviour stage (F055-C15)"
        ),
        "step0_gates": {
            "input_integrity": "every section 2 input carrying a pin hashes to its freeze-record value; a mismatch closes the run as CLOSED AT STEP 0 - INPUT PIN MISMATCH, naming the input (gate 0.1)",
            "source_producible": "the source document is produced from the program's held copy with the section 1 material located verbatim; failure closes as CLOSED AT STEP 0 - SOURCE NOT PRODUCIBLE, the recovery record still produced in closure form (gate 0.2)",
            "recovery_before_verdict": "no identification wording, in either direction, is recorded anywhere before the section 6 recovery record exists (gate 0.3)",
            "corpus_gate": (
                "before step 2 only (gate 0.4; DD-055-13): the strict-corpus layer of record is "
                "identified from the database, exported in full, and pinned by SHA-256 in the "
                "step-0 record, which states the export's file form and sort order as produced; "
                "no file pin is stated at this freeze, because the layer is a database posture "
                "(the Spec 048 precedent for the same layer) with no pinnable repository file on "
                "main; failure closes as CLOSED AT STEP 0 - CORPUS NOT PINNABLE"
            ),
            "occurrence_floor": 5,
            "floor_ruling": "DD-055-12: an identified sign absent from the pinned layer, or represented by fewer than 5 occurrences, closes as IDENTIFIED - TOO FEW OCCURRENCES TO TEST with the count named; no measure is computed past a failed gate",
        },
        "reference_sets": {
            "numeral_set": (
                "the known-numeral set is fixed from published identifications before counting, "
                "each member with its published source and its identifier in the pinned corpus "
                "layer; the target sign is not a member of the set, and adjacency to another "
                "occurrence of the target does not count as numeral adjacency (DD-055-3)"
            ),
            "hedged_members": (
                "DD-055-14: a numeral candidate whose published identification is hedged in its "
                "source does NOT enter the set for any range, median, or adjacency computation; "
                "hedged candidates are recorded as hedged and listed separately in the "
                "pre-counting record"
            ),
            "control_set": (
                "DD-055-11 (confirming DD-055-6): the 10 ordinary signs whose occurrence counts "
                "in the pinned layer are closest to the target's count, ties broken by corpus "
                "identifier in ascending order, all ordinary signs if fewer than 10 exist; "
                "ordinary means a member of neither the numeral set nor the target"
            ),
            "pre_counting_record": "both reference sets, with sources, plus the target census and the dry-run record, fixed before any section 5.2 measure is computed",
        },
        "test": {
            "measures": {
                "short_text_share": "the share of the sign's occurrences that stand in inscriptions of length three or less",
                "numeral_adjacency_share": "the share of the sign's occurrences immediately adjacent (either side, in the corpus's stored sequence order) to another numeral-class sign; adjacency to the target itself does not count",
                "positional_entropy": "DD-055-15: Shannon entropy in bits over positions as stored in the corpus sequence, computed by the identical formula for every sign compared",
            },
            "numeral_side": "the target's value lies inside the known-numeral set's range on the measure and differs from the control set's median on that measure in the direction of the known-numeral set's median (the directional clause, DD-055-11)",
            "control_side": "the target's value lies inside the control set's range on the measure",
            "mapping": {
                "numeral_like": "NUMERAL-LIKE iff numeral-side on at least two measures and control-side on fewer than two",
                "not_numeral_like": "NOT NUMERAL-LIKE iff control-side on at least two measures and numeral-side on fewer than two",
                "mixed": "every other pattern, including both-sides-on-two",
            },
            "dry_run": (
                "DD-055-16: a worked dry-run of the section 5 measures and mapping on a "
                "non-target sign is required before the target is touched, recorded in the "
                "pre-counting record; it produces no target quantity"
            ),
            "source_argument_excluded": "step 2 runs on corpus behaviour alone; the source document's derivation of six is not evidence at the behaviour stage",
        },
        "wordings": (
            "every terminal outcome uses one of spec section 5.4's pre-written wordings: "
            "NUMERAL-LIKE, NOT NUMERAL-LIKE, MIXED, IDENTIFICATION FAILED (list unnamed / sign "
            "unmatched), IDENTIFIED - TOO FEW OCCURRENCES TO TEST, CLOSED AT STEP 0 (pin "
            "mismatch / source not producible / corpus not pinnable)"
        ),
        "execution_gate": (
            "Not satisfied at the freeze of 2026-10-21: execution runs as Phase-414 only after "
            "this freeze has merged, the OSF contract registration's approval act has completed "
            "(the parent's approval click on OSF's admin notification), and a separate execution "
            "order is given, in campaign Wave 3 group 2; at the freeze itself the recovery has "
            "not been performed, no sign has been identified, the corpus layer has not been "
            "exported, and nothing has been counted"
        ),
    },
    "inputs": {
        "claim_file": {
            "file": "glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json",
            "sha256": "e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8",
            "claim_id": "ancient_writing_and_modern_technologies_51831ac9_sign_val_0001",
            "posture": (
                "the freeze-time hash is carried as this definition constant in the Spec 038 "
                "form: the extracted-claims store is regenerated by the backend suite, so the "
                "freeze tests assert the constant plus the fragment's facts on the live file, "
                "never a live-file hash on it"
            ),
        },
        "held_text": {
            "file": "glossa-indus/processed/cleaned_text/ancient_writing_and_modern_technologies_51831ac9.txt",
            "sha256": "1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4",
        },
        "literature_record": {
            "file": "glossa-indus/literature/documents/ancient_writing_and_modern_technologies_51831ac9.json",
            "sha256": "92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c",
            "file_size_bytes": 3565316,
            "license_status": "unclear",
        },
        "phase104_evaluation": {
            "file": "glossa-indus/reports/phase104_claims_evaluation.json",
            "sha256": "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d",
            "claim_id": "ancient_writing_and_modern_technologies_51831ac9_sign_val_0001",
            "verdict": "stays_untested",
            "rule": "RULE-NUM",
        },
        "registry": {
            "file": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
            "rows": 803,
            "trap": "a W900 value inside the wells_ids cell of the P154 row; neither an identification nor an exclusion (F055-C07)",
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
        "strict_corpus": {
            "pin": None,
            "posture": (
                "DD-055-13: no file pin is stated at this freeze, deliberately - the strict "
                "corpus is the program's V3 / Mahadevan-lineage corpus as held in the database "
                "(a database posture, per the Spec 048 precedent for the same layer), identified, "
                "exported, and pinned by SHA-256 at execution gate 0.4 before any counting; the "
                "run closes if it cannot be"
            ),
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every pin above was re-derived by two independent "
            "routes (contents-API raw and git-blob) at main "
            "3af269f660a9368e898cdece41132200d31b87cc; the two routes agree byte-for-byte on "
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
    "backend/tests/test_spec055_freeze.py",
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
