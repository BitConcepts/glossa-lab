#!/usr/bin/env python3
"""Build the Spec 064 freeze record (freeze.json).

Written at the freeze act of 2026-10-21: the digest
is computed over the recovered register exactly
once, at the freeze (the Spec 035 ordering). Run
with the Glossa backend venv python from the
repository root:

    python specs/064-sign297-concordance-successor/build_freeze.py

Writes
specs/064-sign297-concordance-successor/freeze.json
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

SPEC_DIR = "specs/064-sign297-concordance-successor"

DEFINITION = {
    "spec": "specs/064-sign297-concordance-successor/spec.md",
    "freeze_doc": "specs/064-sign297-concordance-successor/freeze.md",
    "experiment_id": "spec064-sign297-concordance-successor",
    "register": {
        "path": "specs/064-sign297-concordance-successor/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.3: "
            "after_specify, after_plan, and after_tasks each cleared "
            "over the recovered register (the draft register already "
            "carried engine evidence values and mutual independent_of "
            "declarations, so no loadability recovery was needed; "
            "round 1 over 0.5-draft returned 17 failure modes: 15 "
            "FR-2.3 draft-cap records and 2 irreducibility challenges "
            "recorded under the coverage_gap category (F064-C06, "
            "C15); recovery to 0.6-draft restated the 2 challenged "
            "heads, and round 2 returned 16 failure modes with 1 "
            "challenge remaining on F064-C06; recovery to 0.7-draft "
            "restated the F064-C06 head as a single proposition with "
            "its instruments carried in the boundary; 15 draft-cap "
            "records only over the final 0.7-draft register), at "
            "every hook zero correctness failure modes and no claim "
            "below the 0.70 threshold (minimum propagated 0.72); the "
            "engine outcome word reads iterate solely from the "
            "draft-cap records (gate reading DD-064-18; record in "
            "specs/064-sign297-concordance-successor/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/064-sign297-concordance-successor/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the "
            "amendment package Item 5 approval (build Spec 064, the "
            "successor to Spec 046, through freeze and OSF filing), "
            "on the amendment-queue commission of the same date "
            "(item 5: drawn-form references for Wells's signs 821 "
            "and 297; the draft's section 6.2 is the reference "
            "record, section 7 the identification protocol, section "
            "8 the successor's charter, followed exactly). Draft "
            "decisions DD-064-1 to DD-064-13 are recorded in "
            "adjudication.md sections 4 and 6 and stand as drafted. "
            "Freeze decisions DD-064-14 to DD-064-18 are recorded "
            "in adjudication.md section 7: the freeze basis "
            "(DD-064-14); Phase-426 allocated (DD-064-15); the "
            "spec's own OSF contract registration filed at the "
            "freeze under E-1 (DD-064-16); the freeze and filing "
            "acts taken, execution not authorised (DD-064-17); and "
            "the carried freeze matter with the DD-038-10 AEE gate "
            "reading adopted (DD-064-18)."
        ),
    },
    "design": {
        "phase": "Phase-426",
        "predecessor": {
            "spec": "specs/046-horned-tiger-concordance",
            "phase": "Phase-405",
            "outcome": (
                "IDENTIFICATION FAILED (sign unmatched) at step 1.2, "
                "executed 2026-10-21: step 0 passed in full, step "
                "1.1 named the source's list from the book's own "
                "apparatus, and the drawn sign could not be matched "
                "by drawn form from the held record because Figure "
                "2.6's drawn forms did not survive the held copy's "
                "text extraction (captions only) and no inspectable "
                "drawn-form reference existed in the held record"
            ),
            "closure_delivery": (
                "specs/046-horned-tiger-concordance/concordance-297.json"
            ),
            "closure_delivery_sha256": (
                "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"
            ),
            "posture": (
                "Spec 046's frozen record, outcome, and closure "
                "delivery stand unedited (DD-064-9); its "
                "IDENTIFICATION FAILED stands until a successor "
                "execution produces its own outcome"
            ),
        },
        "act": (
            "an identification concordance for one fragment, "
            "re-run as Spec 046's successor: find the drawn sign "
            "Wells (2015) numbers 297 - step 1.2 now satisfiable "
            "through the preserved drawn-form reference under the "
            "frozen protocol (steps D, C, M) - then score what "
            "each of the four published sign lists of record says "
            "the sign depicts, in its own words, under rules frozen "
            "before any list is opened for scoring"
        ),
        "claim_id": (
            "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002"
        ),
        "hypothesis": (
            "the identification of the drawn sign as a tiger is the "
            "published consensus: at least two independent lists "
            "score AGREE and no list scores DISAGREE (spec section "
            "1.2; F064-C03)"
        ),
        "source_role": (
            "Wells is scored in the role SOURCE and never counts "
            "toward CONSENSUS, because the claim source document "
            "is Wells (2015) itself (DD-064-2; F064-C08)"
        ),
        "identification_protocol": {
            "reference": {
                "file": (
                    "specs/064-sign297-concordance-successor/"
                    "drawn-form-reference-297.json"
                ),
                "sha256": (
                    "33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4"
                ),
                "schema": "glossa.drawn-form-reference/1",
                "continuity_status": "QUALIFIED",
                "qualification": (
                    "anchored at family level only: no record the "
                    "program holds anchors the number 297 "
                    "individually from the 2015 side (no formation "
                    "text, no registry row, no witness row); the "
                    "P205 family anchor is corroboration only, NOT "
                    "an identification, with its frozen status "
                    "carried in the record"
                ),
                "descriptor": (
                    "a bundle of four long parallel strokes bent "
                    "once: the upper portions slant steeply down to "
                    "the left; below the bend the strokes run "
                    "near-vertical and splay slightly apart at the "
                    "base; in the plates' bent-ray run (signs "
                    "289-308)"
                ),
            },
            "step_d": (
                "descriptor derivation, twice: two independent "
                "derivations from the thesis plate (Figure 3.2, "
                "thesis p. 90 / PDF p. 102), each without sight of "
                "the other or of the preserved descriptor wording, "
                "each recording the plate locator, the feature list "
                "read, and the neighbour set discriminated against; "
                "reconciliation by the recorded features, an "
                "unsettled disagreement resolving against "
                "identification; agreement with the preserved "
                "descriptor required - a material difference closes "
                "IDENTIFICATION FAILED (reference not sustained)"
            ),
            "step_c": (
                "continuity/discrimination, MANDATORY in this "
                "successor (DD-064-11): the two step D derivations "
                "must each affirm that the descriptor picks out "
                "plate 297 and no neighbour in the 289-308 run, "
                "with the family anchor carried at its frozen "
                "status; if either derivation cannot affirm the "
                "discrimination, the run closes IDENTIFICATION "
                "FAILED (continuity/discrimination not sustained) - "
                "a pre-registered closure, not a defect discovered "
                "at scoring time"
            ),
            "step_m": (
                "the match, by exactly one frozen route: Route 1 "
                "(registry, by drawn form - a registry row whose "
                "drawn description matches the reconciled "
                "descriptor, never by number, the frozen traps "
                "asserted) or Route 2 (the preserved reference "
                "cited as the source list's own entry, quoted with "
                "its locator); the composition route is sign-821-only "
                "and is not a route under this spec; no route may "
                "be constructed at run time; neither route "
                "satisfiable closes IDENTIFICATION FAILED (sign "
                "unmatched)"
            ),
        },
        "scoring": {
            "agree": (
                "the list identifies the drawn sign as a tiger; "
                "the horned qualifier is recorded verbatim, not "
                "scored (DD-064-5)"
            ),
            "disagree": (
                "the list identifies the drawn sign as something "
                "other than a tiger, quoted verbatim"
            ),
            "silent": (
                "the list gives no referent identification for the "
                "drawn sign, with the entry_present sub-state "
                "recorded (DD-064-4)"
            ),
        },
        "outcome_mapping": {
            "rule": (
                "A is the number of INDEPENDENT lists (CISI, "
                "Parpola, Mahadevan) scored AGREE; D is the number "
                "of lists of any role scored DISAGREE, including a "
                "Wells-internal divergence"
            ),
            "CONSENSUS": "A >= 2 and D = 0",
            "CONTESTED": "D >= 1, whatever A is",
            "PARTIAL CONCURRENCE": "A = 1 and D = 0",
            "SINGLE-SOURCE": "A = 0 and D = 0",
            "totality": (
                "every pattern of scored rows lands in exactly one "
                "outcome; PARTIAL CONCURRENCE is Spec 046's "
                "freeze-confirmed word (DD-046-3, DD-046-9), "
                "carried unchanged (DD-064-3)"
            ),
        },
        "lists_of_record": {
            "WELLS": (
                "SOURCE; the sign apparatus of Wells 2015 itself - "
                "Chapter 2, The Indus Sign List (Figure 2.6), in "
                "Bryan K. Wells, The Archaeology and Epigraphy of "
                "Indus Writing (Archaeopress, 2015; ISBN 978 1 "
                "78491 046 4), held as cleaned text; locator "
                "chapter/figure plus the book sign number "
                "(DD-046-10, carried by DD-064-18)"
            ),
            "CISI": (
                "INDEPENDENT; the catalogue apparatus of CISI Vol. "
                "1 (Joshi and Parpola (eds.), 1987; MASI 86) and "
                "Vol. 2 (Shah and Parpola (eds.), 1991), as held "
                "digitally and complete and as catalogued in the "
                "Phase-124 catalogue layers; locator volume plus "
                "catalogue/object entry plus page or plate "
                "(DD-046-11, carried by DD-064-18)"
            ),
            "PARPOLA": (
                "INDEPENDENT; Parpola published sign "
                "identifications in Asko Parpola, Deciphering the "
                "Indus Script (Cambridge University Press, 1994), "
                "the sign list of 386 signs; locator P-number, the "
                "registry being keyed to Parpola 1982 numbering "
                "(DD-046-11, carried by DD-064-18)"
            ),
            "MAHADEVAN": (
                "INDEPENDENT; Iravatham Mahadevan, The Indus "
                "Script: Texts, Concordance and Tables (Memoirs of "
                "the Archaeological Survey of India, No. 77, 1977), "
                "the M77 sign list of 419 signs; locator M-number "
                "plus concordance/tables page or entry (DD-046-12, "
                "carried by DD-064-18)"
            ),
        },
        "delivery": {
            "file": (
                "concordance-297.json in this spec directory "
                "(specs/064-sign297-concordance-successor/), schema "
                "glossa.concordance/1, producer_spec 064, produced "
                "on every terminal outcome (DD-064-1; spec "
                "section 6)"
            ),
            "closure_form": (
                "on a closure before scoring, signs is an empty "
                "array and the top level carries closure {class, "
                "wording}; an empty feed is a stated state, never "
                "an absent file"
            ),
            "asset_a_feed": (
                "Asset A consumes only this successor's delivery "
                "if one is produced (DD-064-9); on CONSENSUS, "
                "PARTIAL CONCURRENCE, or SINGLE-SOURCE the feed "
                "carries depicted_kind animal, the source term "
                "horned tiger, and the concurrence state; on "
                "CONTESTED the kind fields are null, "
                "flagged_disputed is true, and every verbatim "
                "identification travels in disputed_identifications"
            ),
        },
        "lineage_note": (
            "independence is publication-level only; the lists' "
            "scholarly traditions borrow from each other and this "
            "concordance does not audit their genealogy; the note "
            "stands in the CONSENSUS wording before any row is "
            "scored (DD-046-13, carried by DD-064-18)"
        ),
        "fences": (
            "identification layer only; concordance is not "
            "correctness; one sign only; silence is not "
            "disagreement; the QUALIFIED continuity status is "
            "carried wherever the result is stated; negative, "
            "single-source, partial, and closure outcomes publish "
            "with the same prominence as consensus (spec "
            "section 9)"
        ),
        "freeze_does_not": (
            "this freeze does not establish that sign 297 is "
            "identified, and does not establish that the "
            "identification will survive its own step C "
            "discrimination check: the frozen reference is "
            "QUALIFIED, step C has not run, no list was opened "
            "for scoring, and no concordance row exists at the "
            "freeze; Spec 046's IDENTIFICATION FAILED stands "
            "until a successor execution produces its own outcome"
        ),
        "execution_gate": (
            "NOT satisfied at the freeze of 2026-10-21: the OSF "
            "contract registration was filed at the freeze under "
            "E-1 and execution awaits its approval plus a separate "
            "execution order; no list was opened for scoring and "
            "no concordance row exists at the freeze"
        ),
    },
    "inputs": {
        "claim_record": {
            "file": (
                "glossa-indus/claims/extracted_claims/"
                "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json"
            ),
            "sha256": (
                "997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031"
            ),
            "note": (
                "the record now carries Spec 046's dated "
                "first-check append of Phase-405 beside the frozen "
                "entry; the fragment entry itself is unchanged"
            ),
        },
        "source_book_held_text": {
            "file": (
                "glossa-indus/processed/cleaned_text/"
                "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt"
            ),
            "sha256": (
                "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"
            ),
            "passage_locator": "printed p. 97; held text lines 2938-2941",
        },
        "phase104_evaluation": {
            "file": "glossa-indus/reports/phase104_claims_evaluation.json",
            "sha256": (
                "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"
            ),
        },
        "crosswalk_registry": {
            "file": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": (
                "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
            ),
            "rows": 803,
            "traps": (
                "Parpola P297 is described in the registry as a "
                "Ladder motif, a different sign from Wells 297; "
                "the value W297 appears inside a multi-value "
                "wells_ids cell on the P205 row and does not by "
                "itself identify the passage sign"
            ),
        },
        "wells_witness": {
            "file": "data/crosswalks/wells_segmentation_witness_v1.csv",
            "sha256": (
                "ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da"
            ),
            "rows": 157,
            "note": (
                "carries no grapheme 297; the string 297 occurs "
                "in it only as the Mahadevan label M297, whose "
                "Wells grapheme is 924"
            ),
        },
        "lane2_drafts": {
            "file": "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
            "sha256": (
                "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"
            ),
        },
        "spec046_closure_delivery": {
            "file": "specs/046-horned-tiger-concordance/concordance-297.json",
            "sha256": (
                "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"
            ),
            "posture": "stands unedited (DD-064-9)",
        },
        "drawn_form_reference": {
            "file": (
                "specs/064-sign297-concordance-successor/"
                "drawn-form-reference-297.json"
            ),
            "sha256": (
                "33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4"
            ),
            "bytes": 7168,
            "posture": (
                "the preservation act of this spec (DD-064-10): "
                "committed in this directory, digest computed at "
                "commitment and pinned here; also a digest-covered "
                "source of this freeze; continuity_status "
                "QUALIFIED"
            ),
        },
        "thesis_pdf": {
            "file": (
                "local research store only: "
                "downloads/wells-phd-thesis-2006/"
                "Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf"
            ),
            "sha256": (
                "4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e"
            ),
            "bytes": 19313853,
            "posture": (
                "not committed; open deposit (Internet Archive "
                "epigraphicapproachestoinduswritingbryankennethwellsphd.thesis_230_Z); "
                "asserted on the local file at step 0 (gate 0.4) "
                "before any plate is read; Figure 3.2, thesis "
                "p. 90 / PDF p. 102"
            ),
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every repository pin "
            "above was re-derived by two independent routes "
            "(git-blob and contents-API raw) at main "
            "e03f7832f99463d3496241676e21bf85e62fb9cc, with the "
            "working tree agreeing as a third read; the routes "
            "agree byte-for-byte on every file and every hash "
            "equals its pin (freeze.md section 2)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.3 (venv glossa-aee153; package pinned >=1.5.0,<1.6)",
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
    f"{SPEC_DIR}/drawn-form-reference-297.json",
    "backend/tests/test_spec064_freeze.py",
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
