#!/usr/bin/env python3
"""Phase-426 — Spec 064 identification concordance act.

Executes the frozen Spec 064 contract
(specs/064-sign297-concordance-successor/freeze.md; freeze
digest cfeb7baf... in freeze.json; OSF registration s6hr9,
approved and public before this run): the drawn sign
Wells (2015) numbers 297 — the fragment "Sign value: 297
/ the horned tiger, or perhaps just 'tiger' generically"
(the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_
val_0002, stopped at Phase-104 under RULE-NUM; Spec 046 /
Phase-405 closed IDENTIFICATION FAILED (sign unmatched)
at step 1.2 for want of an inspectable drawn-form
reference) — is identified at step 1 through the
preserved drawn-form reference of this spec
(drawn-form-reference-297.json, SHA-256 33ee22ec...,
continuity status QUALIFIED) under the frozen protocol
of spec section 4 (steps D, C, M) and, only if
identified, scored at step 2 against the four published
sign lists of record (Wells as SOURCE; CISI, Parpola,
Mahadevan as INDEPENDENT).

The run, in the frozen order:

  step 0.1  every spec section 2 input hashes to its
            frozen pin, including the preserved
            reference record and the Spec 046 closure
            delivery (fail-closed: INPUT PIN MISMATCH);
  step 0.2  the source book is produced from the held
            cleaned text and the section 1 passage is
            located verbatim (SOURCE NOT PRODUCIBLE);
  step 0.3  each of the four lists is accounted for as
            HELD or CITABLE with its citation and
            locator form (LIST NOT PRODUCIBLE);
  step 0.4  the preserved reference is producible: it
            exists at its pinned digest, and the thesis
            plate page it cites (Figure 3.2, thesis
            p. 90 / PDF p. 102) is produced from the
            local thesis file after that file's digest
            is asserted against its section 2 pin
            (REFERENCE NOT PRODUCIBLE). The thesis file
            is local-store only and is never committed;
            if it cannot be located in the running
            environment the script aborts without
            writing (the committed record stands), and
            a located file whose digest differs is a
            genuine gate failure and writes the closure;
  step 1.1  the source's sign list is named from the
            book's own apparatus;
  step D    the drawn-form descriptor is derived twice
            from the thesis plate, independently (the
            two derivation sheets below are the
            executor's plate reads, recorded here as
            the machine form of the run record; the
            outcome record carries them in full),
            reconciled by the recorded features, and
            compared with the preserved descriptor:
            agreement is required, a material
            difference closes IDENTIFICATION FAILED
            (reference not sustained);
  step C    continuity / discrimination (MANDATORY):
            the family anchor is carried at its frozen
            status (corroboration only, NOT an
            identification), and each derivation must
            affirm that the reconciled descriptor picks
            out plate 297 and no neighbour in the
            289-308 run. If either cannot, the run
            closes IDENTIFICATION FAILED
            (continuity/discrimination not sustained)
            — the pre-registered closure. This run
            closes there: neither derivation affirms
            the discrimination (signs 299, 302 and 303
            satisfy every stated feature of the
            descriptor), so step M and step 2 are not
            reached and no list is scored.

The preserved reference's continuity status QUALIFIED
is carried on every output of this run and is never
upgraded or dropped.

Outputs (written on every terminal outcome):
  A — specs/064-sign297-concordance-successor/
      concordance-297.json (the section 6 delivery
      form, schema glossa.concordance/1; on a closure
      before scoring, signs is an empty array and the
      top level carries the closure block);
  B — reports/phase426_results.json (the run's results
      record);
  C — reports/phase426_concordance_report.md (the
      human-readable rendering; it does not diverge
      from A).

The claim-record append (spec section 8) is an executor
act recorded in the outcome record, not a side effect
of this script, so that re-running this script never
appends twice.

Fail-closed: any pin, passage, citation, registry,
witness, or reference fact that differs from the frozen
record aborts the run before any output is written,
except that a step-0 or step-1 closure IS an output
(the closure form of A, with B and C recording the
gate facts).
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC_DIR = _REPO / "specs/064-sign297-concordance-successor"
_OUT_A = _SPEC_DIR / "concordance-297.json"
_OUT_B = _REPO / "reports/phase426_results.json"
_OUT_C = _REPO / "reports/phase426_concordance_report.md"

CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002")
FREEZE_DIGEST = (
    "cfeb7baf71fad26e81ca80a08395c87a07d158974480923fd38eb2fed854c405")
EXECUTOR = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-22"
OSF_REGISTRATION = "s6hr9 (approved + public before the run)"

PINS = {
    "claim_record": (
        "glossa-indus/claims/extracted_claims/"
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json",
        "997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031"),
    "source_book_held_text": (
        "glossa-indus/processed/cleaned_text/"
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
        "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"),
    "phase104_evaluation": (
        "glossa-indus/reports/phase104_claims_evaluation.json",
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"),
    "crosswalk_registry": (
        "data/crosswalks/canonical_sign_registry.csv",
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"),
    "wells_witness": (
        "data/crosswalks/wells_segmentation_witness_v1.csv",
        "ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da"),
    "lane2_drafts": (
        "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"),
    "spec046_closure_delivery": (
        "specs/046-horned-tiger-concordance/concordance-297.json",
        "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"),
    "drawn_form_reference": (
        "specs/064-sign297-concordance-successor/"
        "drawn-form-reference-297.json",
        "33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4"),
}

THESIS_SHA256 = (
    "4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e")
THESIS_BYTES = 19313853
THESIS_PAGES = 296

PASSAGE_FRAGMENTS = (
    "Sign 532 and sign 297 are positioned in such a way",
    "sign 297 represents the horned tiger, or perhaps just",
    "‘tiger’ generically",
)
PASSAGE_QUOTE = (
    "Sign 532 and sign 297 are positioned in such a way as to "
    "resemble the position of the graphic element and several of "
    "their features are repeated in the image field. It is proposed "
    "here that sign 532 is a logograph for the anthropomorphic figure "
    "and that sign 297 represents the horned tiger, or perhaps just "
    "‘tiger’ generically.")

QUALIFICATION = (
    "Qualification (carried from the preserved reference, "
    "Spec 064 §1): the identification of Wells's 297 rests "
    "on a drawn-form reference whose continuity status is "
    "QUALIFIED — anchored at family level only; its step C "
    "discrimination check is part of this run's record.")

IDENTIFICATION_FAILED_WORDING = (
    "The fragment 'sign 297 is the horned tiger' cannot be carried "
    "to a concordance: the descriptor's discrimination of 297 from "
    "its neighbours in the 289–308 run was not sustained by both "
    "independent derivations. The record stays a stated gap. No "
    "statement about the sign is made, and nothing is fed to "
    "Asset A. " + QUALIFICATION)

FENCE = (
    "This result settles what the published lists say the drawn "
    "sign depicts. It is not evidence of what the sign meant in use.")

TRAPS_ASSERTED = [
    "P205's wells_ids cell used as an identification "
    "(Spec 046 frozen trap 1)",
    "P297 'Ladder motif. Two nearby vertical lines with a number "
    "of horizontal lines going across the middle...' (Spec 046 "
    "frozen trap 2 - a different sign, wells_ids empty)",
    "M297 in the Phase-123 witness (a Mahadevan sign whose Wells "
    "grapheme is 924 - the number 297 in a third list)",
    "P205's Mahadevan crosswalk M180 used as W297's identity "
    "(the family anchor's crosswalk is not the sign's crosswalk)",
    "any number-only match, including a plate number read "
    "without the protocol's step C continuity check",
]

# ── Step D derivation sheets (executor's plate reads) ─────
# Each sheet was recorded from renders of the thesis plate
# (Figure 3.2, thesis p. 90 / PDF p. 102) produced from the
# digest-asserted local file at gate 0.4: sheet A from the
# full-page read, sheet B from an independent re-render with
# per-sign cell crops. Feature lists were recorded from the
# plate before comparison with the preserved descriptor;
# the comparison and the step C affirmations follow the
# sheets. No image is committed anywhere in this run.
DERIVATION_A = {
    "sheet": "A",
    "method": (
        "First plate read: full-page render of PDF p. 102 "
        "at 300 dpi, read in page context against the whole "
        "Figure 3.2 plate."),
    "plate_locator": (
        "Wells 2006, PhD thesis, Figure 3.2, 'The Indus signs "
        "by sign number', thesis p. 90 / PDF p. 102; bottom "
        "row, signs 295-308; 297 is the third entry."),
    "features_read_for_297": [
        "a bundle of long parallel strokes",
        "bent once, at a single bend whose point is at the left",
        "the upper portions slant steeply down to the left",
        "the lower portions run down from the bend and splay "
        "slightly apart at the base",
        "stroke count read as four at the base, three clear "
        "above the bend",
    ],
    "neighbour_set_discriminated_against": (
        "the plates' bent-ray run, signs 289-308: the upper "
        "row (289-294) are compact chevron forms with no long "
        "lower run; in the bottom row, 295 carries a single "
        "broad upper stroke, 296 and 304 keep their upper "
        "portions near-vertical, and 307 and 308 carry a "
        "looped head; 299, 300, 301, 302, 303, 305 and 306 "
        "are the same bent bundle in differing widths and "
        "counts."),
    "step_c_affirmation": False,
    "step_c_statement": (
        "I cannot affirm that the descriptor picks out plate "
        "297 and no neighbour. Signs 299, 302 and 303 present "
        "the same feature set — a parallel bundle bent once, "
        "uppers slanting steeply down-left, lowers running "
        "down from the bend with a basal splay — and nothing "
        "in the features I read separates 297 from them. "
        "What fixes 297 on the plate is its printed position "
        "and number, which is the number-only reading the "
        "protocol names as a trap when it is used without "
        "this check."),
}

DERIVATION_B = {
    "sheet": "B",
    "method": (
        "Second plate read: independent re-render of PDF "
        "p. 102; per-sign cell crops at 600-700 dpi; stroke "
        "counts taken at the top edge and at the base of "
        "each glyph in the 289-308 run."),
    "plate_locator": (
        "Wells 2006, PhD thesis, Figure 3.2, thesis p. 90 / "
        "PDF p. 102; bottom row, signs 295-308; 297 is the "
        "third entry."),
    "features_read_for_297": [
        "three distinct strokes above the bend",
        "four distinct stroke ends at the base",
        "a single sharp bend, point at the left, at about "
        "55-60% of the glyph height",
        "upper portions slant about 50 degrees from vertical, "
        "down to the left",
        "lower portions slant about 30 degrees from vertical, "
        "down to the right — more vertical than the uppers, "
        "not strictly near-vertical",
        "moderate basal splay",
    ],
    "neighbour_counts_read": {
        "295": "1 above / 4 at base; single broad upper stroke",
        "296": "3 / 4; uppers near-vertical, bend shallow",
        "299": "2-3 above / 4 at base; same steep slant, same "
               "sharp bend, same basal splay as 297",
        "300": "2-3 / 4; bundle narrower, bend shallower — "
               "differences of degree, not of stated features",
        "301": "2 / 4; small narrow bundle — differences of "
               "degree, not of stated features",
        "302": "3 / 4-5; same steep slant, sharp bend and "
               "splay as 297",
        "303": "3 / 4; same steep slant, sharp bend and "
               "splay as 297",
        "304": "3 / 4; uppers near-vertical",
        "305": "4 / 4; uppers more vertical, chevron-like",
        "306": "3-4 / 5; uppers more vertical",
        "307": "looped head; 2-3 strokes",
        "308": "looped head; 2-3 strokes",
        "289-294": "compact chevron forms; lower runs "
                   "markedly shorter than 297's long lower run",
    },
    "step_c_affirmation": False,
    "step_c_statement": (
        "I cannot affirm the discrimination. Counted "
        "feature by feature, signs 299, 302 and 303 match "
        "297 on every feature the descriptor states "
        "(parallel bundle, single bend, steep upper slant, "
        "lower run with basal splay, four stroke ends at "
        "the base); 300, 301, 305 and 306 differ only in "
        "degree (width, bend sharpness, slant) on features "
        "the descriptor does not quantify. The descriptor "
        "fixes the family and 297's place in the run; it "
        "does not pick out 297 alone."),
}

RECONCILED_DESCRIPTOR = (
    "A bundle of long parallel strokes bent once at a single "
    "sharp bend — three strokes clear above the bend and four "
    "stroke ends at the base: the upper portions slant steeply "
    "down to the left; below the bend the strokes run down to "
    "the right, more vertical than the uppers, splaying at "
    "the base. A member of the thesis plates' bent-ray run "
    "(signs 289-308).")

STEP_D_COMPARISON = {
    "verdict": "AGREEMENT — the preserved reference is sustained",
    "noted_readings": [
        "stroke number: the preserved descriptor's 'four' is "
        "the count at the base; three strokes are clear above "
        "the bend, where the innermost strokes merge in the "
        "scan",
        "lower direction: the preserved descriptor's "
        "'near-vertical' reads on the plate as slanting down "
        "to the right at about 30 degrees from vertical — "
        "more vertical than the upper portions, not strictly "
        "vertical",
    ],
    "material_difference": False,
    "reasoning": (
        "Both derivations confirm the preserved descriptor's "
        "feature set — a parallel bent bundle, a single bend, "
        "a steep upper slant down-left, a basal splay, in the "
        "bent-ray run. The two noted readings loosen the "
        "descriptor's wording without changing any feature it "
        "asserts, and the preserved record itself carries "
        "discrimination, not description, as the open step "
        "(its recorded limitation). No material difference "
        "arises, so the run does not close as IDENTIFICATION "
        "FAILED (reference not sustained); it proceeds to "
        "step C, where the discrimination is tested."),
}

STEP_C = {
    "family_anchor_carried": (
        "Registry row P205 ('Prismed light rays, with opposite "
        "slanting on top vs bottom, more rays on bottom'), "
        "whose wells_ids cell groups W289-W306 as one Parpola "
        "sign's Wells counterparts — carried at its frozen "
        "status: corroboration only, expressly NOT an "
        "identification. It corroborates that the 2015 list's "
        "289-306 numbers belong to the bent-ray family the "
        "plate shows, and nothing more."),
    "derivation_a_affirms": False,
    "derivation_b_affirms": False,
    "sustained": False,
    "statement": (
        "Step C is not sustained. Neither independent "
        "derivation affirms that the reconciled descriptor "
        "picks out the plate's 297 and no neighbour in the "
        "289-308 run: signs 299, 302 and 303 satisfy every "
        "stated feature of the descriptor, and the remaining "
        "near neighbours differ only in degree on features "
        "the descriptor does not quantify. The family anchor "
        "is family-level only, exactly as the preserved "
        "reference records it. The run therefore closes "
        "under the pre-registered closure, before step M "
        "and before any scoring. The preserved reference's "
        "continuity status remains QUALIFIED."),
}


CLAIM_APPEND_KEY = "spec064_check"
CLAIM_APPEND_ENTRY = {
    "spec": "064",
    "phase": "Phase-426",
    "date": "2026-10-22",
    "actor": "spec064-phase426-execution",
    "kind": "successor-check (identification)",
    "outcome": (
        "IDENTIFICATION FAILED "
        "(continuity/discrimination not sustained)"),
    "wording": IDENTIFICATION_FAILED_WORDING,
    "record": "specs/064-sign297-concordance-successor/outcome.md",
    "delivery": (
        "specs/064-sign297-concordance-successor/concordance-297.json"),
    "delivery_sha256": (
        "9e765576349d4d294a4fc04f0d6750be3718dfc60fa267ea16c04c6130db7488"),
    "note": (
        "Successor check of this claim under the frozen Spec 064 contract "
        "(OSF s6hr9, approved + public), successor to Spec 046's first check, "
        "which stands unedited in this record under 'first_check'. Step 0 passed "
        "in full, including gate 0.4: the preserved drawn-form reference at its "
        "pinned digest (33ee22ec…) and the thesis file's digest asserted "
        "on the local file before any plate was read. Step 1 named the source's "
        "sign list from the book's own apparatus (Wells's own list, Wells 2011, "
        "in Wells 2015 Chapter 2 / Figure 2.6); step D derived the drawn-form "
        "descriptor twice, independently, from the thesis plate (Figure 3.2, "
        "thesis p. 90 / PDF p. 102) and sustained the preserved reference; "
        "step C — mandatory in Spec 064 — was not sustained: neither "
        "independent derivation affirms that the descriptor picks out plate 297 "
        "and no neighbour in the 289–308 run (signs 299, 302 and 303 satisfy "
        "every stated feature of the descriptor), so the run closed as "
        "IDENTIFICATION FAILED (continuity/discrimination not sustained) before "
        "step M and before any scoring. The preserved reference's continuity "
        "status is QUALIFIED — anchored at family level only — and is "
        "carried on every product of the run. This is a check of identification, "
        "recorded under F064-C15: it is not a verdict on the identification, and "
        "the claim's status and stage are unchanged. Appended by the Spec 064 "
        "execution; no pre-existing field of any claim in this file was altered, "
        "and the Spec 046 first_check entry is unedited."),
}
CLAIM_APPEND_SEGMENT_BYTES = 2669
CLAIM_APPEND_SEGMENT_SHA256 = (
    "fc973395394d87fd43c9ff31f0929c093424b79b298f27459c66660d170e9fcf")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")


def _closure_delivery(closure_class: str, wording: str) -> dict:
    return {
        "producer_spec": "064",
        "producer_claim_id": CLAIM_ID,
        "schema": "glossa.concordance/1",
        "signs": [],
        "closure": {"class": closure_class, "wording": wording},
    }


def _thesis_candidates() -> list[Path]:
    rel = (
        "research_notes/indus-data-deep-sweep-20261008/downloads/"
        "wells-phd-thesis-2006/"
        "Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf")
    out = []
    env = os.environ.get("GLOSSA_WELLS_THESIS_PDF")
    if env:
        out.append(Path(env))
    out.append(Path.home() / "workspace" / rel)
    out.append(_REPO.parent / rel)
    return out


def main() -> int:
    results: dict = {
        "phase": "Phase-426",
        "spec": "064",
        "claim_id": CLAIM_ID,
        "freeze_digest": FREEZE_DIGEST,
        "execution_date": EXECUTION_DATE,
        "executor": EXECUTOR,
        "osf_registration": OSF_REGISTRATION,
        "continuity_status": "QUALIFIED",
        "predecessor": (
            "Spec 046 / Phase-405 closed IDENTIFICATION FAILED "
            "(sign unmatched); its closure delivery stands "
            "unedited (SHA-256 772db4df...) and is asserted "
            "at gate 0.1 of this run."),
    }

    # ── Step 0.1 — input integrity (fail-closed) ──────────────
    # The claim record is asserted in the Spec 038 form: at
    # execution the file hashes to its frozen pin; after the
    # run's own append (an executor act, below) the live file
    # is the pin plus exactly the recorded spec064_check
    # segment, and the gate accepts precisely those two
    # states, asserting the fragment's facts on the live file
    # in both. Any other state is an INPUT PIN MISMATCH.
    pin_results = {}
    for name, (rel, want) in PINS.items():
        got = _sha256(_REPO / rel)
        entry = {
            "file": rel, "expected_sha256": want,
            "observed_sha256": got, "match": got == want}
        if name == "claim_record":
            entry["verification"] = "byte-pin (pristine)"
            if got != want:
                live = (_REPO / rel).read_text(encoding="utf-8")
                doc = json.loads(live)
                frag = next(
                    c for c in doc["claims"]
                    if c["claim_id"] == CLAIM_ID)
                seg_body = json.dumps(
                    CLAIM_APPEND_ENTRY, ensure_ascii=False, indent=2)
                seg = (",\n      \"spec064_check\": " + "\n".join(
                    ("      " + ln if ln else ln)
                    for ln in seg_body.split("\n")))
                facts_ok = (
                    frag.get("normalized_claim") == (
                        "Sign value: 297 / the horned tiger, or "
                        "perhaps just ‘tiger’ generically")
                    and frag.get("claim_status") == "untested"
                    and frag.get("stage") == "created"
                    and frag.get("first_check", {}).get("spec") == "046"
                    and frag.get("spec064_check") == CLAIM_APPEND_ENTRY
                    and live.count(seg) == 1
                    and hashlib.sha256(
                        live.replace(seg, "").encode("utf-8")
                    ).hexdigest() == want)
                entry["match"] = bool(facts_ok)
                entry["verification"] = (
                    "Spec 038 form: frozen pin plus exactly the "
                    "recorded spec064_check append (segment "
                    "SHA-256 " + CLAIM_APPEND_SEGMENT_SHA256 + "); "
                    "removing the segment reproduces the pin, and "
                    "the fragment's facts are asserted on the "
                    "live file")
                entry["fragment_facts_asserted"] = bool(facts_ok)
        pin_results[name] = entry
        if not entry["match"]:
            results["step0"] = {"gate_0_1": pin_results}
            results["outcome"] = "CLOSED AT STEP 0"
            results["closure_class"] = "INPUT PIN MISMATCH"
            _write_json(_OUT_A, _closure_delivery(
                "CLOSED AT STEP 0 — INPUT PIN MISMATCH",
                "Spec 064 closed before identification: input "
                f"{name} did not hash to its frozen pin. No "
                "concordance was run and no statement about the "
                "sign is made."))
            _write_json(_OUT_B, results)
            print(f"STEP 0.1 FAIL: {name} pin mismatch", flush=True)
            return 0
    results["step0"] = {"gate_0_1": pin_results}

    # ── Step 0.2 — source producible, passage verbatim ────────
    text_path = _REPO / PINS["source_book_held_text"][0]
    raw_lines = text_path.read_text(encoding="utf-8").splitlines()
    joined = "\n".join(raw_lines)
    flat = " ".join(joined.split())
    passage_found = all(
        " ".join(frag.split()) in flat for frag in PASSAGE_FRAGMENTS)
    passage_lines = [
        i + 1 for i, line in enumerate(raw_lines)
        if "sign 297 represents the horned tiger" in line]
    if not passage_found or not passage_lines:
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "SOURCE NOT PRODUCIBLE"
        _write_json(_OUT_A, _closure_delivery(
            "CLOSED AT STEP 0 — SOURCE NOT PRODUCIBLE",
            "Spec 064 closed before identification: the source "
            "book could not be produced from the program's held "
            "copy. No concordance was run and no statement about "
            "the sign is made."))
        _write_json(_OUT_B, results)
        print("STEP 0.2 FAIL: passage not located", flush=True)
        return 0
    results["step0"]["gate_0_2"] = {
        "source": PINS["source_book_held_text"][0],
        "passage_locator": "printed p. 97",
        "passage_lines_in_held_text": passage_lines,
        "passage_quote": PASSAGE_QUOTE,
        "located_verbatim": True,
    }

    # ── Step 0.3 — the four lists, HELD or CITABLE ────────────
    citations = (_REPO / "CITATIONS.md").read_text(encoding="utf-8")
    sections = {
        "MAHADEVAN": "### A.1 Mahadevan 1977",
        "CISI": "### A.2 Joshi & Parpola 1987",
        "CISI_vol2": "### A.3 Shah & Parpola 1991",
        "WELLS": "### A.7 Wells 2015",
        "PARPOLA": "### C.1 Parpola 1994a",
    }
    missing = [k for k, s in sections.items() if s not in citations]
    cisi_manifest = (
        _REPO / "reports/phase124_cisi_local_store_manifest.json")
    if missing or not cisi_manifest.exists():
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "LIST NOT PRODUCIBLE"
        _write_json(_OUT_A, _closure_delivery(
            "CLOSED AT STEP 0 — LIST NOT PRODUCIBLE",
            "Spec 064 closed before identification: a published "
            "list of record could be neither produced nor cited "
            "with a locator. No concordance was run and no "
            "statement about the sign is made."))
        _write_json(_OUT_B, results)
        print(f"STEP 0.3 FAIL: {missing}", flush=True)
        return 0
    results["step0"]["gate_0_3"] = {
        "WELLS": {
            "role": "SOURCE", "availability": "HELD",
            "citation": ("Wells, The Archaeology and Epigraphy of "
                         "Indus Writing, 2015 (CITATIONS.md §A.7)"),
            "locator_form": "chapter/figure plus the book's own "
                            "sign number",
            "basis": "held cleaned text, pin-verified at gate 0.1"},
        "CISI": {
            "role": "INDEPENDENT", "availability": "HELD",
            "citation": ("Joshi & Parpola (eds.), Corpus of Indus "
                         "Seals and Inscriptions 1 (1987; MASI 86); "
                         "Shah & Parpola (eds.), vol. 2 (1991) "
                         "(CITATIONS.md §§A.2–A.3)"),
            "locator_form": "volume plus catalogue/object entry "
                            "plus page or plate",
            "basis": ("Phase-124 catalogue layers; committed local-"
                      "store manifest reports/phase124_cisi_local_"
                      "store_manifest.json present")},
        "PARPOLA": {
            "role": "INDEPENDENT", "availability": "CITABLE",
            "citation": ("Parpola, Deciphering the Indus Script, "
                         "1994 (CITATIONS.md §C.1)"),
            "locator_form": "P-number (sign list of 386 signs)",
            "basis": ("full citation of record; the program's "
                      "crosswalk registry is keyed to Parpola "
                      "1982 numbering")},
        "MAHADEVAN": {
            "role": "INDEPENDENT", "availability": "CITABLE",
            "citation": ("Mahadevan, The Indus Script: Texts, "
                         "Concordance and Tables, 1977 (MASI No. "
                         "77) (CITATIONS.md §A.1)"),
            "locator_form": "M-number plus concordance/tables "
                            "page or entry",
            "basis": ("full citation of record; Mahadevan crosswalk "
                      "data held in the pinned registry")},
    }

    # ── Step 0.4 — reference producible ───────────────────────
    reference = json.loads((
        _REPO / PINS["drawn_form_reference"][0]).read_text(
            encoding="utf-8"))
    if reference["continuity_status"]["status"] != "QUALIFIED":
        print("STEP 0.4 FAIL: reference continuity status "
              "is not QUALIFIED as frozen", flush=True)
        return 2
    thesis_path = next(
        (p for p in _thesis_candidates() if p.exists()), None)
    if thesis_path is None:
        # The thesis file is local-store only. An environment
        # without the program's local store cannot re-run this
        # gate; abort without writing, so the committed
        # execution record stands (the graph node's serve
        # path falls back to it).
        print("STEP 0.4 ABORT: thesis file not locatable in "
              "this environment; no output written", flush=True)
        return 2
    thesis_sha = _sha256(thesis_path)
    thesis_bytes = thesis_path.stat().st_size
    if thesis_sha != THESIS_SHA256 or thesis_bytes != THESIS_BYTES:
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "REFERENCE NOT PRODUCIBLE"
        results["step0"]["gate_0_4"] = {
            "reference_file": PINS["drawn_form_reference"][0],
            "reference_sha256": PINS["drawn_form_reference"][1],
            "reference_at_pinned_digest": True,
            "thesis_file_asserted": False,
            "thesis_observed_sha256": thesis_sha,
            "thesis_observed_bytes": thesis_bytes,
        }
        _write_json(_OUT_A, _closure_delivery(
            "CLOSED AT STEP 0 — REFERENCE NOT PRODUCIBLE",
            "Spec 064 closed before identification: the "
            "preserved drawn-form reference could not be "
            "produced at its pinned digest, or the thesis "
            "file did not hash to its pin. No concordance "
            "was run and no statement about the sign is made."))
        _write_json(_OUT_B, results)
        print("STEP 0.4 FAIL: thesis digest mismatch", flush=True)
        return 0
    results["step0"]["gate_0_4"] = {
        "reference_file": PINS["drawn_form_reference"][0],
        "reference_sha256": PINS["drawn_form_reference"][1],
        "reference_at_pinned_digest": True,
        "continuity_status": "QUALIFIED",
        "thesis_file": (
            "local research store only (not committed): "
            "downloads/wells-phd-thesis-2006/"
            "Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf"),
        "thesis_expected_sha256": THESIS_SHA256,
        "thesis_observed_sha256": thesis_sha,
        "thesis_expected_bytes": THESIS_BYTES,
        "thesis_observed_bytes": thesis_bytes,
        "thesis_digest_asserted_before_plate_read": True,
        "thesis_pages": THESIS_PAGES,
        "plate_page_produced": (
            "Figure 3.2, thesis p. 90 / PDF p. 102, produced "
            "from the digest-asserted local file at execution "
            "(render read by the executor; bottom row signs "
            "295-308 present, 297 the third entry); no image "
            "is committed"),
    }

    # ── Step 1.1 — the source's list named from the document ──
    apparatus = {
        "chapter_2_gives_the_list": (
            "Chapter 2 gives the Indus sign list used in this "
            "analysis" in flat),
        "sign_list_used_here_wells_2011": (
            "The sign list used here (Wells 2011)" in flat),
        "figure_2_6_caption": "Figure 2.6 An Indus Sign List" in flat,
    }
    if not all(apparatus.values()):
        results["outcome"] = "IDENTIFICATION FAILED"
        results["closure_class"] = (
            "IDENTIFICATION FAILED (list unnamed)")
        _write_json(_OUT_A, _closure_delivery(
            "IDENTIFICATION FAILED (list unnamed)",
            "The fragment 'sign 297 is the horned tiger' cannot be "
            "carried to a concordance: the source document does not "
            "name its sign list. The record stays a stated gap. No "
            "statement about the sign is made, and nothing is fed "
            "to Asset A. " + QUALIFICATION))
        _write_json(_OUT_B, results)
        print("STEP 1.1 FAIL: list unnamed", flush=True)
        return 0
    results["step1"] = {
        "source_list_named": (
            "Wells's own sign list (Wells 2011), as given in "
            "Wells 2015, Chapter 2, 'The Indus Sign List' "
            "(Figure 2.6)"),
        "apparatus_evidence": apparatus,
        "drawn_form_reference": {
            "file": PINS["drawn_form_reference"][0],
            "sha256": PINS["drawn_form_reference"][1],
            "continuity_status": "QUALIFIED",
        },
        "traps_asserted": TRAPS_ASSERTED,
    }

    # ── Registry and witness facts (traps; step M record) ────
    registry_path = _REPO / PINS["crosswalk_registry"][0]
    with registry_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    w297_cells = []
    tiger_descriptions = 0
    for row in rows:
        tokens = [t.strip() for t in row["wells_ids"].split("|")]
        if "W297" in tokens:
            w297_cells.append({
                "sign_id": row["parpola_id"],
                "description": row["description"],
                "wells_ids": row["wells_ids"],
                "singleton": tokens == ["W297"],
            })
        if "tiger" in row["description"].lower():
            tiger_descriptions += 1
    p297 = [r for r in rows if r["parpola_id"] == "P297"]
    witness_path = _REPO / PINS["wells_witness"][0]
    with witness_path.open(encoding="utf-8", newline="") as fh:
        wrows = list(csv.DictReader(fh))
    witness_297 = [
        r["sign"] for r in wrows
        if "297" in [g.strip() for g in
                     r.get("wells_graphemes", "").split(";")]]
    m297 = [r for r in wrows if r["sign"] == "M297"]
    results["step1"]["registry_witness_facts"] = {
        "registry_rows": len(rows),
        "w297_cells": w297_cells,
        "registry_tiger_descriptions": tiger_descriptions,
        "p297_description": (
            p297[0]["description"] if p297 else None),
        "witness_rows": len(wrows),
        "witness_grapheme_297_rows": witness_297,
        "witness_m297_wells_grapheme": (
            m297[0]["wells_graphemes"] if m297 else None),
    }

    # ── Step D — descriptor derivation, twice ─────────────────
    results["step1"]["step_d"] = {
        "derivations": [DERIVATION_A, DERIVATION_B],
        "reconciled_descriptor": RECONCILED_DESCRIPTOR,
        "comparison_with_preserved": STEP_D_COMPARISON,
        "preserved_descriptor": reference["descriptor"]["text"],
    }

    # ── Step C — continuity / discrimination (MANDATORY) ──────
    results["step1"]["step_c"] = STEP_C
    if not STEP_C["sustained"]:
        results["step1"]["step_m"] = {
            "reached": False,
            "routes_frozen": [
                "Route 1 (registry, by drawn form)",
                "Route 2 (the preserved reference cited as the "
                "source list's own entry)",
            ],
            "note": (
                "Step M was not reached: the run closed at "
                "step C under its pre-registered closure. No "
                "route was attempted and no match is recorded."),
        }
        results["outcome"] = "IDENTIFICATION FAILED"
        results["closure_class"] = (
            "IDENTIFICATION FAILED "
            "(continuity/discrimination not sustained)")
        results["headline_wording"] = IDENTIFICATION_FAILED_WORDING
        results["qualification"] = QUALIFICATION
        results["fence"] = FENCE
        _write_json(_OUT_A, _closure_delivery(
            "IDENTIFICATION FAILED "
            "(continuity/discrimination not sustained)",
            IDENTIFICATION_FAILED_WORDING))
        assert _sha256(_OUT_A) == (
            CLAIM_APPEND_ENTRY["delivery_sha256"])
        results["claim_append"] = {
            "key": CLAIM_APPEND_KEY,
            "entry": CLAIM_APPEND_ENTRY,
            "segment_bytes": CLAIM_APPEND_SEGMENT_BYTES,
            "segment_sha256": CLAIM_APPEND_SEGMENT_SHA256,
            "verification": (
                "The append is an executor act, not a side "
                "effect of this script. Verified at the act "
                "(2026-10-22): removing the appended segment "
                "reproduces the pre-act claim file "
                "byte-identically, and the claim's status "
                "and stage are unchanged (outcome.md, "
                "F064-C15)."),
        }
        _write_json(_OUT_B, results)
        _OUT_C.write_text(_render_report(results), encoding="utf-8")
        print("OUTCOME: IDENTIFICATION FAILED "
              "(continuity/discrimination not sustained)",
              flush=True)
        return 0

    # Step C sustained is the only route past this gate, to
    # step M and step 2. There is deliberately no match or
    # scoring code in this script beyond this point: a future
    # sustained run extends this script openly rather than
    # this branch improvising one.
    print("STEP C SUSTAINED — step M not implemented in this run",
          flush=True)
    return 1


def _render_report(r: dict) -> str:
    g1 = r["step0"]["gate_0_1"]
    pins = "\n".join(
        f"- `{v['file']}` — SHA-256 `{v['observed_sha256']}` "
        f"(pin match: {v['match']})" for v in g1.values())
    d = r["step1"]["step_d"]
    c = r["step1"]["step_c"]
    return f"""# Phase-426 — Spec 064 identification concordance report

Executed {r['execution_date']} by {r['executor']}, under the
frozen Spec 064 contract (freeze digest
`{r['freeze_digest']}` in freeze.json; OSF registration
s6hr9, approved + public before the run). Successor to
Spec 046 / Phase-405, whose closure delivery stands
unedited. The preserved reference's continuity status is
**QUALIFIED** — carried on this report as on every product
of this run.

## Outcome

**IDENTIFICATION FAILED (continuity/discrimination not sustained)**

{r['headline_wording']}

{r['fence']}

## The passage (spec section 8, element 1)

> "{r['step0']['gate_0_2']['passage_quote']}"

Locator: Wells (2015), printed p. 97 (held cleaned text,
lines {r['step0']['gate_0_2']['passage_lines_in_held_text']}).

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed,
including the preserved reference record at its pinned
digest and the Spec 046 closure delivery unedited:

{pins}

Gate 0.2 — the source book was produced from the held copy
and the passage located verbatim (above).

Gate 0.3 — all four lists accounted for as HELD or CITABLE
with citation plus locator form (CITATIONS.md §§A.1, A.2,
A.3, A.7, C.1; CISI Phase-124 catalogue layers): WELLS
HELD; CISI HELD; PARPOLA CITABLE; MAHADEVAN CITABLE.

Gate 0.4 — the preserved reference exists at its pinned
digest (`33ee22ec...`), continuity status QUALIFIED; the
local thesis file's digest was asserted against its pin
(`4b39330c...`, 19,313,853 bytes) before any plate was
read, and the plate page (Figure 3.2, thesis p. 90 / PDF
p. 102) was produced from it. No image is committed.

## Step 1

The source's sign list is named from the book's own
apparatus: Wells's own sign list (Wells 2011), as given in
Wells 2015, Chapter 2, "The Indus Sign List" (Figure 2.6).

### Step D — the descriptor, derived twice

Reconciled descriptor: {d['reconciled_descriptor']}

Comparison with the preserved descriptor:
{d['comparison_with_preserved']['verdict']} — the two
noted readings are recorded in the results record and
judged not material. The preserved reference is
sustained.

### Step C — continuity / discrimination (mandatory)

Family anchor, carried at its frozen status:
{c['family_anchor_carried']}

{c['statement']}

### Step M and step 2

Not reached. No route was attempted, no list was scored,
no concurrence state was computed, and nothing is fed to
Asset A: the delivery
(`specs/064-sign297-concordance-successor/concordance-297.json`)
carries an empty signs array and the closure block, in the
frozen section 6 form. Qualification: the identification
of Wells's 297 rests on a drawn-form reference whose
continuity status is QUALIFIED.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
"""


if __name__ == "__main__":
    sys.exit(main())
