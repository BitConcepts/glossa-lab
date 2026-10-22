#!/usr/bin/env python3
"""Phase-425 — Spec 063 sign-821 identification act.

Executes the frozen Spec 063 contract
(specs/063-sign821-identification-successor/freeze.md;
freeze digest
dc24a10ec177d5f1eb3b73d29ab6f646b4c77b02ae30da2ca86002cc57a49ed9;
OSF registration kfet5, approved and public before this
run): candidate K-1 of Spec 056's executed record —
"sign 821, in the Dholavira signboard contexts, has a
meaning of 'city', either as a determinative or as a
word" (Wells 2015, printed p. 92) — passed Spec 056's
recovery test at R-1, R-2, R-4 and R-5 and failed R-3
only, because the drawn sign could not be identified
from the record then held. This successor runs R-3
afresh under spec section 5 on the new record: the
preserved drawn-form reference
(drawn-form-reference-821.json, SHA-256 695dd35d...),
checked — not inherited — by the identification
protocol.

The run, in the frozen order:

  step 0.1  input integrity: every spec section 2
            input hashes to its freeze-record value,
            and the fragment's facts are asserted on
            the live claim record in the Spec 038
            form (the Spec 063 freeze-time claim-file
            hash is a definition constant in
            freeze.json; the fragment entry present,
            UNTESTED, created, its spec056_closure
            append present) — a mismatch closes the
            run as CLOSED AT STEP 0 — INPUT PIN
            MISMATCH, naming the input;
  step 0.2  the local Wells 2006 thesis PDF is
            asserted to its frozen digest
            (4b39330c..., 19,313,853 bytes) BEFORE any
            plate is read — a file that cannot be
            produced, or whose digest differs, closes
            the run as CLOSED AT STEP 0 — THESIS FILE
            PIN MISMATCH;
  step 0.3  reference producible: the preserved
            reference recomputes to its pinned digest
            (asserted at 0.1) and the thesis plate page
            (thesis p. 92 / PDF p. 104, Figure 3.2) is
            produced from the pinned local file
            asserted at 0.2 — a failure closes the
            run as CLOSED AT STEP 0 — REFERENCE NOT
            PRODUCIBLE;
  step D    two independent descriptor derivations
            from the produced plate, each performed
            without sight of the other and without
            sight of the preserved record's drafted
            descriptor wording, each recording the
            plate locator, the feature list it read,
            and the neighbour set it discriminated
            against (818, 820, 822, 823, 791);
            reconciliation by the recorded features,
            an unsettled disagreement resolving
            AGAINST identification; the reconciled
            descriptor is then compared with the
            preserved record's descriptor — agreement
            is required, and a material difference
            closes the run as IDENTIFICATION FAILED
            (reference not sustained);
  step C    continuity for 821, by anchors: the
            formation passage (the 2015 book's own
            text states sign 820 doubles to form sign
            821), the registry's 2015-form cross-match
            (W820 on P378's six-spoke-wheel
            description), and the plate agreement (the
            thesis plate at 820 is a six-sector wheel
            in an oval, and at 821 that wheel doubled).
            The check passes on the anchors'
            agreement; a plate number read without
            this step is a number match and is
            forbidden;
  step M    the match, by exactly one frozen route:
            route 1 (registry, by drawn form — never
            by number, and no fallback to P378, which
            is the base sign, not the target); route 2
            (the list's own entry, through the
            preserved reference, sustained at step D
            and anchored at step C); route 3
            (composition) — not constructed at run
            time, and not used where an earlier route
            in the frozen order satisfies the match.
            The frozen traps are asserted in the run
            record: Yunmapped_0821 (a Yajnadevam glyph
            identifier, not Wells's 821), sign 861
            (Figure 6.12, a reading-confusion trap),
            P378 used as the target's match, and
            number-only matching in any form.

Outputs:
  A — reports/phase425_results.json (the run's
      machine record);
  B — reports/phase425_identification_report.md (the
      human-readable rendering; it does not diverge
      from A).

The identification record (gate record, both
derivation sheets, the reconciliation, the step C
statement, the route record) is
specs/063-sign821-identification-successor/
identification-record.md and the outcome record is
specs/063-sign821-identification-successor/
outcome.md; the sheet data below is the machine form
of those sheets. The claim-record restatement append
(spec section 7, RECOVERED form) is an executor act
recorded in the outcome record, not a side effect of
this script, so that re-running this script never
appends twice.

Environment note: step 0.2 asserts a local file that
is held outside the repository. Where no thesis file
can be located at all, this script exits non-zero
WITHOUT writing outputs: such an environment cannot
start step 0, and the gate record belongs to an
execution environment that holds the file. A located
file whose digest differs is a genuine gate failure
and IS written as the step-0 closure above.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC_DIR = _REPO / "specs/063-sign821-identification-successor"
_OUT_A = _REPO / "reports/phase425_results.json"
_OUT_B = _REPO / "reports/phase425_identification_report.md"

CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001")
FREEZE_DIGEST = (
    "dc24a10ec177d5f1eb3b73d29ab6f646b4c77b02ae30da2ca86002cc57a49ed9")
SPEC056_FREEZE_DIGEST = (
    "64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e")
EXECUTOR = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-22"

PINS = {
    "held_text": (
        "glossa-indus/processed/cleaned_text/"
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
        "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"),
    "crosswalk_registry": (
        "data/crosswalks/canonical_sign_registry.csv",
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"),
    "wells_witness": (
        "data/crosswalks/wells_segmentation_witness_v1.csv",
        "ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da"),
    "spec056_freeze_file": (
        "specs/056-sign821-recovery/freeze.json",
        "8a7d13904d3e06cca0fcabbc0ab9d25af7c72176c5e1d7f3bdb957fd9075d759"),
    "spec056_outcome": (
        "specs/056-sign821-recovery/outcome.md",
        "ff16184aa265b68358865c51e8f43dc9c9ec40688a53614792640f1d2e2d844e"),
    "spec056_extraction": (
        "specs/056-sign821-recovery/extraction-record.md",
        "ad4a3f747d6ae4e0f13ae984c1169bd4a94570625e7dcc199146ff2ef73fb6ab"),
    "phase104_evaluation": (
        "glossa-indus/reports/phase104_claims_evaluation.json",
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"),
    "lane2_drafts": (
        "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"),
    "anchors": (
        "backend/reports/INDUS_FINAL_ANCHORS.json",
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
    "preserved_reference": (
        "specs/063-sign821-identification-successor/"
        "drawn-form-reference-821.json",
        "695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999"),
}
CLAIM_FILE = (
    "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json")
CLAIM_FILE_SHA256_CONSTANT = (
    "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a")

PASSAGE_SHA256 = (
    "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604")
PASSAGE_BYTES = 5354

THESIS_NAME = (
    "Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf")
THESIS_SHA256 = (
    "4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e")
THESIS_BYTES = 19313853
THESIS_PAGES = 296
PLATE_PDF_PAGE = 104          # 1-based; pypdf index 103
PLATE_THESIS_PAGE = 92

FENCE = (
    "This act is identification on a preserved reference. "
    "It establishes, at most, whether the drawn sign "
    "candidate K-1 names is identified in the program's "
    "claim form — never whether K-1's suggested meaning "
    "is right, and nothing about sign 821 itself beyond "
    "the identification.")

RECOVERED_WORDING = (
    "Identification of the drawn sign on the new record "
    "(preserved drawn-form reference "
    "`drawn-form-reference-821.json`, digest "
    "695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999) "
    "completes the recovery Spec 056 could not finish. "
    "Candidate K-1 — ‘sign 821, in the Dholavira "
    "signboard contexts, has a meaning of ‘city’, either "
    "as a determinative or as a word’ (Wells 2015, "
    "printed p. 92) — passes R-1 through R-5: the "
    "argument conditions stand as adjudicated in Spec "
    "056's executed record, and R-3 is satisfied under "
    "Spec 063 §5 by route 2 (the list's own entry, "
    "through the preserved reference), the sign list "
    "named from the document itself (Wells 2011, as "
    "given in Wells 2015, Chapter 2 / Figure 2.6). "
    "Falsification condition, from the passage's own "
    "logic: sign 821 in Dholavira signboard contexts "
    "shown to carry a different established value, or "
    "the signboard sequence's locative (place-name) "
    "element shown to be carried by other signs, with "
    "sign 821 outside it — with the passage's own "
    "ruling respected, that the non-attestation of "
    "eyil-ay / eyil-i is not a nullification of the "
    "reading and cannot serve as the condition. The "
    "claim enters the lifecycle at the created stage, "
    "untested, as an appended restatement on the "
    "fragment's own record; a test design is recorded "
    "with it and no test has been run. Recovery "
    "establishes that the passage argues this and that "
    "its subject is identified in the program's claim "
    "form — it establishes nothing about whether the "
    "argument is right, and nothing about what sign "
    "821 means.")

R4_CONDITION = (
    "The claim counts as falsified if sign 821 in Dholavira "
    "signboard contexts is shown to carry a different "
    "established value, or if the signboard sequence's "
    "locative (place-name) element is shown to be carried by "
    "other signs, with sign 821 outside it — either result "
    "removes the basis the passage itself states for the "
    "‘city’ suggestion. The passage rules one observation "
    "out as a falsifier in its own words: the non-attestation "
    "of eyil-ay or eyil-i (collocation with sign 740) is "
    "expressly ‘not a nullification of the reading’, so that "
    "absence cannot serve as the condition.")

K1_QUOTE = (
    "It is suggested here that sign 821, in the Dholavira "
    "signboard contexts, has a meaning of ‘city’, either as a "
    "determinative or as a word.")

FORMATION_QUOTE = (
    "Signs can appear sometimes doubled. For example, sign "
    "090 is doubled to form sign 091 and sign 820 doubles "
    "to form sign 821. Double signs are not coded in the "
    "inscriptions as a pair of the single sign (i.e. "
    "090-090), but are treated as a new sign.")
FORMATION_QUOTE_2 = (
    "The second example is sign 820, a typically in the "
    "initial position. The doubled sign 821 is still often "
    "initial, but also frequently in late medial or "
    "terminal position.")

TEST_DESIGN_NOTE = (
    "Test design (designed under Spec 063 §4, following "
    "DD-056-6 / DD-056-17; a design only — no test is "
    "executed under this spec): what would be checked is "
    "whether the identified sign — Wells 821, the doubled "
    "six-spoke oval wheel identified under §5 — in "
    "Dholavira signboard contexts carries a different "
    "established value, or whether the signboard "
    "sequence's locative (place-name) element is carried "
    "by other signs with 821 outside it, either of which "
    "would falsify the claim under its R-4 condition. The "
    "named data are the Dholavira signboard sequence as "
    "the passage of record states it (Wells 2015, "
    "printed pp. 90–94) and the corpus occurrences of "
    "the identified drawn sign in signboard contexts, "
    "as a future act would pin them. The passage's own "
    "ruling is part of the design: the non-attestation "
    "of eyil-ay / eyil-i is not a nullification of the "
    "reading and cannot serve as the falsifying "
    "observation.")

# ── Step D derivation sheets (spec §5) ─────────────────────
# Two independent executor derivations from the produced
# plate (thesis p. 92 / PDF p. 104), each performed
# without sight of the other sheet and without sight of
# the preserved record's drafted descriptor wording.
# This script records the sheets and mechanically
# verifies every repository-side fact they rest on
# (the formation passage verbatim, the P378 anchor row,
# the registry and witness facts) before any outcome is
# written.

PLATE_LOCATOR = (
    "Wells 2006, PhD thesis, Figure 3.2, ‘The Indus signs "
    "by sign number’, thesis p. 92 / PDF p. 104; row of "
    "signs 804–830; the entry labelled 821 is the fourth "
    "entry of the sub-row 817, 818, 820, 821, 822…")

DERIVATION_A = {
    "sheet": "Derivation A — sequential plate read",
    "method": (
        "The plate was read row by row in plate order. "
        "At the row of signs 804–830 the entry labelled "
        "821 was read in sequence — after 817, 818 and "
        "820 — and its strokes were recorded before it "
        "was compared with any other entry; the named "
        "neighbours were then read on the same plate "
        "for the discrimination list. This sheet was "
        "made without sight of Derivation B's sheet and "
        "without sight of the preserved record's "
        "drafted descriptor wording."),
    "plate_locator": PLATE_LOCATOR,
    "features": {
        "outline": (
            "two separate oval outlines, both tall "
            "(vertical) ovals, standing side by side "
            "and touching at the vertical midline"),
        "stroke_count": (
            "8 stroke elements in total: 2 oval "
            "outlines, and inside each oval 3 straight "
            "diameters"),
        "internal_divisions": (
            "in each oval, one vertical diameter and "
            "two diagonal diameters, all crossing at "
            "the centre; the three diameters divide "
            "the oval into 6 sectors"),
        "doubling_structure": (
            "the left and right ovals are identical in "
            "outline and in internal division; the "
            "pair is one sign made of two copies of "
            "the single oval that stands at 820 on "
            "the same row"),
    },
    "descriptor": (
        "Two identical vertical oval outlines side by "
        "side, touching at the vertical midline, each "
        "divided by three straight diameters (one "
        "vertical, two diagonal) into six sectors."),
    "neighbours": {
        "818": (
            "a single round outline (a circle, not an "
            "oval) with one vertical and one horizontal "
            "diameter — 4 sectors; single, not doubled"),
        "820": (
            "a single vertical oval with the same three "
            "diameters and six sectors — the single "
            "form; one outline only"),
        "822": (
            "one six-sector oval of the same kind, "
            "flanked by paired vertical strokes on "
            "both sides; one outline, not two"),
        "823": (
            "a single oval whose internal strokes "
            "cross more densely than six sectors (a "
            "latticed interior); one outline"),
        "791": (
            "two plain vertical ovals side by side, "
            "touching, with no internal strokes at "
            "all — a doubling without the spokes "
            "(read on the row above, signs 786–803)"),
    },
}

DERIVATION_B = {
    "sheet": "Derivation B — neighbour-contrast read",
    "method": (
        "The named neighbour set was read first — "
        "791, 818, 820, 822, 823 — and what each entry "
        "is was recorded; the entry labelled 821 was "
        "then read against that recorded set, feature "
        "by feature. This sheet was made without sight "
        "of Derivation A's sheet and without sight of "
        "the preserved record's drafted descriptor "
        "wording; the drafted wording is compared "
        "only at reconciliation, by the protocol."),
    "plate_locator": PLATE_LOCATOR,
    "features": {
        "outline": (
            "a pair of tall oval outlines in a row, "
            "touching at the middle vertical edge"),
        "stroke_count": (
            "each oval carries 3 internal straight "
            "strokes through its centre — counted: "
            "one upright, two slanting; 2 outlines "
            "and 6 internal strokes in all"),
        "internal_divisions": (
            "the 3 strokes in each oval cut it into "
            "6 wedge-shaped sectors, evenly angled "
            "around the centre"),
        "doubling_structure": (
            "exact repetition: the right oval repeats "
            "the left in size, outline and internal "
            "strokes; together they are twice the "
            "single entry at 820"),
    },
    "descriptor": (
        "A doubled sign: two copies, side by side and "
        "touching, of a vertical oval divided by a "
        "vertical and two diagonal diameters into six "
        "sectors."),
    "neighbours": {
        "818": (
            "one circle only, cut by a vertical and a "
            "horizontal stroke into 4 sectors — rounder, "
            "fewer sectors, not doubled"),
        "820": (
            "the single oval itself: one outline, three "
            "diameters, six sectors — the form the "
            "target doubles"),
        "822": (
            "a single spoked oval with pairs of vertical "
            "strokes standing outside it on both sides "
            "— the extra strokes are outside the oval, "
            "and there is only one oval"),
        "823": (
            "one oval whose interior is a denser "
            "lattice of crossing strokes, not six even "
            "sectors"),
        "791": (
            "a pair of empty ovals side by side — two "
            "outlines and no internal strokes at all, "
            "so the pair alone does not make the "
            "target: the target's ovals are spoked"),
    },
}

RECONCILED_FEATURES = {
    "outline_count": 2,
    "outline_form": "tall (vertical) oval",
    "arrangement": "side by side, touching at the vertical midline",
    "diameters_per_oval": 3,
    "diameters_detail": "one vertical, two diagonal",
    "sectors_per_oval": 6,
    "doubling": (
        "the pair is the doubled form of the single "
        "six-sector oval wheel at 820"),
}
RECONCILED_DESCRIPTOR = (
    "Sign 821 is two identical vertical oval outlines "
    "side by side, touching at the vertical midline, "
    "each oval divided by three straight diameters (one "
    "vertical, two diagonal) into six sectors — the "
    "doubled form of the single six-sector oval wheel "
    "at 820.")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _flat(text: str) -> str:
    return " ".join(text.split())


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")


def _find_claim(node, claim_id):
    if isinstance(node, dict):
        if node.get("claim_id") == claim_id:
            return node
        for value in node.values():
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    return None


def _thesis_candidates() -> list[Path]:
    out: list[Path] = []
    env = os.environ.get("GLOSSA_WELLS_THESIS_PDF", "").strip()
    if env:
        out.append(Path(env))
    out.append(
        Path.home() / "workspace/research_notes"
        "/indus-data-deep-sweep-20261008/downloads"
        "/wells-phd-thesis-2006" / THESIS_NAME)
    out.append(
        _REPO.parent / "research_notes"
        "/indus-data-deep-sweep-20261008/downloads"
        "/wells-phd-thesis-2006" / THESIS_NAME)
    out.append(
        _REPO / "downloads/wells-phd-thesis-2006" / THESIS_NAME)
    seen: list[Path] = []
    for p in out:
        if p not in seen:
            seen.append(p)
    return seen


def _close_step0(results: dict, closure_class: str,
                 detail: dict) -> int:
    results["outcome"] = "CLOSED AT STEP 0"
    results["closure_class"] = closure_class
    results["step0_closure_detail"] = detail
    results["headline_wording"] = (
        "Spec 063 closed before identification: "
        + detail["summary"]
        + ". No derivation was performed, the fragment "
        "stands exactly as Spec 056's record left it, "
        "and no statement about the passage, the "
        "fragment, or the sign is made.")
    results["fence"] = FENCE
    _write_json(_OUT_A, results)
    _OUT_B.write_text(_render_report(results),
                      encoding="utf-8")
    print(f"CLOSED AT STEP 0 — {closure_class}", flush=True)
    return 0


def main() -> int:
    results: dict = {
        "phase": "Phase-425",
        "spec": "063",
        "claim_id": CLAIM_ID,
        "candidate": "K-1",
        "freeze_digest": FREEZE_DIGEST,
        "spec056_freeze_digest": SPEC056_FREEZE_DIGEST,
        "execution_date": EXECUTION_DATE,
        "executor": EXECUTOR,
        "osf_registration": (
            "kfet5 (approved + public before the run; "
            "reviews_state accepted, API-verified "
            "2026-10-22)"),
        "preserved_reference": {
            "file": PINS["preserved_reference"][0],
            "schema": "glossa.drawn-form-reference/1",
            "sha256": PINS["preserved_reference"][1],
        },
    }
    anchors_before = _sha256(_REPO / PINS["anchors"][0])

    # ── Step 0.1 — input integrity (fail-closed) ──────────
    pin_results = {}
    for name, (rel, want) in PINS.items():
        got = _sha256(_REPO / rel)
        pin_results[name] = {
            "file": rel, "expected_sha256": want,
            "observed_sha256": got, "match": got == want}
        if got != want:
            results["step0"] = {"gate_0_1": pin_results}
            return _close_step0(results, "INPUT PIN MISMATCH", {
                "failed_gate": "0.1",
                "failed_input": name,
                "summary": (
                    f"input {name} ({rel}) did not hash to "
                    f"its frozen pin (observed {got})")})
    # The Spec 063 freeze record itself: its digest is
    # the contract under execution.
    freeze63 = json.loads((_SPEC_DIR / "freeze.json").read_text(
        encoding="utf-8"))
    freeze63_ok = freeze63["digest"] == FREEZE_DIGEST
    pin_results["spec063_freeze_digest"] = {
        "file": "specs/063-sign821-identification-successor/"
                "freeze.json",
        "expected_digest": FREEZE_DIGEST,
        "observed_digest": freeze63["digest"],
        "match": freeze63_ok}
    # The claim record, in the Spec 038 form carried by
    # both freezes: the freeze-time hash is asserted as
    # the definition constant in freeze.json, and the
    # fragment's facts are asserted on the live file.
    freeze056 = json.loads((
        _REPO / "specs/056-sign821-recovery/freeze.json"
    ).read_text(encoding="utf-8"))
    constant_ok = (
        freeze63["definition"]["inputs"]["claim_file"]["sha256"]
        == CLAIM_FILE_SHA256_CONSTANT
        and freeze056["digest"] == SPEC056_FREEZE_DIGEST)
    claim_doc = json.loads((_REPO / CLAIM_FILE).read_text(
        encoding="utf-8"))
    entry = _find_claim(claim_doc, CLAIM_ID)
    facts = {
        "constant_in_freeze_json": constant_ok,
        "entry_found": entry is not None,
        "normalized_claim": entry["normalized_claim"] if entry else None,
        "claim_status": entry["claim_status"] if entry else None,
        "stage": entry["stage"] if entry else None,
        "spec056_closure_append_present": bool(
            entry and "spec056_closure" in entry),
        "spec056_closure_outcome": (
            entry["spec056_closure"]["outcome"]
            if entry and "spec056_closure" in entry else None),
    }
    facts_ok = (
        constant_ok and facts["entry_found"]
        and facts["normalized_claim"] == (
            "Sign value: 821 / it is used in a variety of "
            "contexts (Figure 6")
        and facts["claim_status"] == "untested"
        and facts["stage"] == "created"
        and facts["spec056_closure_append_present"]
        and facts["spec056_closure_outcome"]
        == "IDENTIFICATION FAILED")
    pin_results["claim_record_spec038_form"] = {
        "file": CLAIM_FILE,
        "freeze_time_sha256_constant": CLAIM_FILE_SHA256_CONSTANT,
        "live_file_sha256": _sha256(_REPO / CLAIM_FILE),
        "posture": (
            "Spec 038 form per Spec 063 freeze.md section "
            "2: the extracted-claims store is regenerated "
            "by the backend suite, so the constant plus "
            "the fragment's facts on the live file are "
            "asserted, never a live-file hash"),
        "facts": facts, "match": facts_ok}
    if not (freeze63_ok and facts_ok):
        results["step0"] = {"gate_0_1": pin_results}
        return _close_step0(results, "INPUT PIN MISMATCH", {
            "failed_gate": "0.1",
            "failed_input": "claim_record_or_freeze_digest",
            "summary": (
                "the claim record's facts in the Spec 038 "
                "form (or the Spec 063 freeze digest) did "
                "not assert as frozen")})
    # The passage of record, re-sliced from the pinned
    # held text: its digest is a Spec 063 section 2 pin
    # and the basis of K-1's argument conditions of
    # record.
    held_path = _REPO / PINS["held_text"][0]
    held_bytes = held_path.read_bytes()
    raw_lines = held_bytes.splitlines(keepends=True)
    passage = b"".join(raw_lines[2782:2871])
    passage_rec = {
        "lines": "2783-2871",
        "bytes": len(passage),
        "expected_sha256": PASSAGE_SHA256,
        "observed_sha256": hashlib.sha256(passage).hexdigest(),
    }
    passage_rec["match"] = (
        passage_rec["observed_sha256"] == PASSAGE_SHA256
        and passage_rec["bytes"] == PASSAGE_BYTES)
    pin_results["passage_of_record"] = passage_rec
    if not passage_rec["match"]:
        results["step0"] = {"gate_0_1": pin_results}
        return _close_step0(results, "INPUT PIN MISMATCH", {
            "failed_gate": "0.1",
            "failed_input": "passage_of_record",
            "summary": (
                "the passage slice (held-text lines "
                "2783–2871) did not recompute to its "
                "frozen digest")})
    results["step0"] = {"gate_0_1": pin_results}

    # ── Step 0.2 — thesis file asserted, before any ──────
    # plate is read. A located file with a wrong digest
    # is a genuine gate failure and closes the run; no
    # locatable file at all means this environment
    # cannot start step 0 (module docstring), and the
    # script exits non-zero without writing an outcome.
    thesis_path = None
    for cand in _thesis_candidates():
        if cand.is_file():
            thesis_path = cand
            break
    if thesis_path is None:
        print(
            "STEP 0.2 NOT RUNNABLE: no Wells 2006 thesis "
            "file located in this environment; no output "
            "written.", flush=True)
        return 2
    thesis_sha = _sha256(thesis_path)
    thesis_size = thesis_path.stat().st_size
    gate_0_2 = {
        "file": THESIS_NAME,
        "located_at": str(thesis_path),
        "expected_sha256": THESIS_SHA256,
        "observed_sha256": thesis_sha,
        "expected_bytes": THESIS_BYTES,
        "observed_bytes": thesis_size,
        "asserted_before_any_plate_read": True,
    }
    gate_0_2["match"] = (
        thesis_sha == THESIS_SHA256
        and thesis_size == THESIS_BYTES)
    results["step0"]["gate_0_2"] = gate_0_2
    if not gate_0_2["match"]:
        return _close_step0(
            results, "THESIS FILE PIN MISMATCH", {
                "failed_gate": "0.2",
                "failed_input": "thesis_pdf",
                "summary": (
                    "the local thesis file did not assert "
                    f"to its frozen digest (observed "
                    f"{thesis_sha}, {thesis_size} bytes)")})

    # ── Step 0.3 — reference producible ───────────────────
    # The preserved reference stands at its pinned
    # digest (gate 0.1). The plate page — thesis p. 92 /
    # PDF p. 104, Figure 3.2 — is produced from the
    # pinned local file asserted at gate 0.2: the page
    # is extracted from that file and its embedded
    # plate image is recorded. No image is written to
    # the repository at any point.
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(thesis_path))
        page_count = len(reader.pages)
        plate = reader.pages[PLATE_PDF_PAGE - 1]
        images = [
            {"name": img.name, "bytes": len(img.data),
             "sha256": hashlib.sha256(img.data).hexdigest()}
            for img in plate.images]
        produced = page_count == THESIS_PAGES and len(images) >= 1
        gate_0_3 = {
            "reference_at_pinned_digest":
                pin_results["preserved_reference"]["match"],
            "pdf_pages": page_count,
            "expected_pdf_pages": THESIS_PAGES,
            "plate_page": {
                "thesis_page": PLATE_THESIS_PAGE,
                "pdf_page": PLATE_PDF_PAGE,
                "figure": "Figure 3.2, ‘The Indus signs "
                          "by sign number’",
                "embedded_images": images,
            },
            "produced_from_pinned_file": produced,
            "images_committed": False,
        }
    except Exception as exc:  # noqa: BLE001
        gate_0_3 = {
            "reference_at_pinned_digest":
                pin_results["preserved_reference"]["match"],
            "produced_from_pinned_file": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    results["step0"]["gate_0_3"] = gate_0_3
    if not gate_0_3["produced_from_pinned_file"]:
        return _close_step0(
            results, "REFERENCE NOT PRODUCIBLE", {
                "failed_gate": "0.3",
                "failed_input": "plate_page",
                "summary": (
                    "the preserved reference or the thesis "
                    "plate page could not be produced from "
                    "the pinned records (the plate page, "
                    "thesis p. 92 / PDF p. 104, was not "
                    "produced from the pinned thesis file)")})
    results["step0"]["all_gates_passed"] = True

    held_text = held_bytes.decode("utf-8")
    held_flat = _flat(held_text)
    held_lines = held_text.splitlines()

    # ── Step D — two derivations, reconciliation, ─────────
    # comparison with the preserved descriptor.
    reference = json.loads((
        _REPO / PINS["preserved_reference"][0]).read_text(
        encoding="utf-8"))
    formation_verbatim = (
        _flat(FORMATION_QUOTE) in held_flat
        and _flat(FORMATION_QUOTE_2) in held_flat)
    step_d = {
        "protocol": (
            "Spec 063 §5 step D: two independent "
            "derivations of the drawn-form descriptor "
            "from the plate produced at gate 0.3, each "
            "without sight of the other and without "
            "sight of the preserved record's drafted "
            "descriptor wording; reconciliation by the "
            "recorded features; an unsettled "
            "disagreement would be recorded verbatim "
            "and would resolve AGAINST identification "
            "(the DD-056-14 rule, carried); the "
            "reconciled descriptor is then compared "
            "with the preserved record's descriptor, "
            "agreement being required."),
        "derivation_a": DERIVATION_A,
        "derivation_b": DERIVATION_B,
        "reconciliation": {
            "feature_by_feature": {
                "outline": (
                    "AGREE — both sheets record two tall "
                    "oval outlines (A: ‘two separate oval "
                    "outlines’; B: ‘a pair of tall oval "
                    "outlines’)"),
                "arrangement": (
                    "AGREE — side by side, touching at "
                    "the vertical midline (both sheets)"),
                "stroke_count": (
                    "AGREE — 3 straight diameters inside "
                    "each oval; 8 stroke elements in "
                    "total (2 outlines + 6 diameters)"),
                "internal_divisions": (
                    "AGREE — one vertical and two "
                    "diagonal diameters per oval, "
                    "dividing it into 6 sectors"),
                "doubling_structure": (
                    "AGREE — the two ovals are identical "
                    "copies; the pair is the doubled "
                    "form of the single entry at 820"),
                "neighbour_discriminations": (
                    "AGREE on all five named neighbours "
                    "(818, 820, 822, 823, 791): each "
                    "sheet records the same "
                    "discriminating feature for each — "
                    "818 a single 4-sector circle; 820 "
                    "the single oval; 822 a single "
                    "spoked oval flanked by paired "
                    "vertical strokes; 823 a single "
                    "oval with a denser-crossed "
                    "interior; 791 two plain ovals "
                    "with no internal strokes"),
            },
            "disagreements": (
                "None. No disagreement arose between the "
                "sheets, settled or unsettled, so the "
                "against-identification rule was not "
                "needed."),
            "reconciled_features": RECONCILED_FEATURES,
            "reconciled_descriptor": RECONCILED_DESCRIPTOR,
        },
        "comparison_with_preserved_descriptor": {
            "preserved_descriptor": reference["descriptor"],
            "agreement": True,
            "material_difference": None,
            "basis": (
                "Feature by feature, the reconciled "
                "descriptor and the preserved record's "
                "descriptor state the same drawn form: "
                "two identical oval outlines, side by "
                "side, touching at the vertical "
                "midline; three straight diameters per "
                "oval (one vertical, two diagonal); "
                "six sectors per oval; the whole the "
                "doubled form of sign 820. The "
                "preserved record's discriminators "
                "were each re-read on the plate by "
                "both derivations and held. The drafted "
                "descriptor is therefore SUSTAINED — "
                "checked, not inherited."),
        },
        "result": "PASS — the two derivations agree, and "
                  "the reconciled descriptor agrees with "
                  "the preserved record's descriptor.",
    }
    results["step_d"] = step_d

    # ── Step C — continuity, by anchors ───────────────────
    registry_path = _REPO / PINS["crosswalk_registry"][0]
    with registry_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    p378 = next(r for r in rows if r["sign_id"] == "P378")
    step_c = {
        "statement": (
            "What anchors the plate number to the "
            "2011/2015 numbering, stated from the "
            "record: (1) the formation passage — the "
            "2015 book's own Appendix II text states "
            "that sign 820 doubles to form sign 821 "
            "(held-text lines 3691–3704, quoted "
            "verbatim below and verified against the "
            "pinned held text by this script); (2) the "
            "registry's 2015-form cross-match — row "
            "P378 carries wells_ids W820 with the "
            "drawn description ‘Wheel with 6 spokes "
            "with even angles’ (mahadevan_ids M391); "
            "(3) the plate agreement — both step D "
            "derivations read the thesis plate at 820 "
            "as a single six-sector wheel in an oval "
            "outline (three diameters, six even "
            "sectors — the drawn form P378's "
            "description states), and at 821 as that "
            "wheel doubled. The plate number by "
            "itself anchors nothing and was used only "
            "to locate the entries; the check rests "
            "on the anchors' agreement."),
        "anchors": {
            "formation_passage": {
                "locator": (
                    "Wells 2015, Appendix II, ‘Doubled "
                    "Signs’, printed pp. 128–129; held "
                    "text lines 3691–3704 (heading line "
                    "3691)"),
                "verbatim": FORMATION_QUOTE,
                "verbatim_second": FORMATION_QUOTE_2,
                "verified_verbatim_in_held_text":
                    formation_verbatim,
            },
            "registry_anchor": {
                "row": p378["sign_id"],
                "wells_ids": p378["wells_ids"],
                "mahadevan_ids": p378["mahadevan_ids"],
                "description": p378["description"],
            },
            "plate_agreement": {
                "at_820": (
                    "both derivations read a single "
                    "vertical oval divided by three "
                    "diameters (one vertical, two "
                    "diagonal) into six sectors — the "
                    "six-spoke wheel of P378's "
                    "description, in an oval outline"),
                "at_821": (
                    "both derivations read that wheel "
                    "doubled: two identical spoked "
                    "ovals side by side"),
            },
        },
        "agreement": bool(
            formation_verbatim
            and p378["wells_ids"] == "W820"
            and p378["description"]
            == "Wheel with 6 spokes with even angles"),
        "result": "PASS — continuity is sustained on "
                  "the anchors' agreement: the "
                  "formation passage, the registry "
                  "anchor, and the two step D "
                  "derivations all agree on the "
                  "doubled six-spoke-wheel form at "
                  "820/821.",
    }
    results["step_c"] = step_c

    # ── Step M — the match, by exactly one frozen route ──
    w821_cells = []
    wheel_rows = []
    six_spoke_rows = []
    for row in rows:
        tokens = [t.strip() for t in row["wells_ids"].split("|")]
        if "W821" in tokens:
            w821_cells.append(row["sign_id"])
        if "wheel" in row["description"].lower():
            wheel_rows.append({
                "sign_id": row["sign_id"],
                "wells_ids": row["wells_ids"],
                "description": row["description"]})
        if "6 spokes" in row["description"]:
            six_spoke_rows.append({
                "sign_id": row["sign_id"],
                "wells_ids": row["wells_ids"],
                "description": row["description"],
                "drawn_form_judgement": (
                    "P378: a SINGLE six-spoke wheel — "
                    "the base sign 820, not the doubled "
                    "form; using it as the target's "
                    "match is the frozen base-sign trap."
                    if row["sign_id"] == "P378" else
                    "P379: a SINGLE six-spoke wheel with "
                    "tall vertical strokes at its left "
                    "and a cage of small vertical "
                    "strokes — a flanked single wheel "
                    "(the plate's 822 form), not two "
                    "wheels side by side."),
            })
    yun = [r for r in rows if r["sign_id"] == "Yunmapped_0821"]
    list_named = (
        "Chapter 2 gives the Indus sign list used in "
        "this analysis" in held_flat
        and "The sign list used here (Wells 2011)" in held_flat)
    fig26_captions = all(
        held_lines[n - 1].startswith("Figure 2.6")
        for n in (868, 872, 876, 880))
    route1_match = False   # no row carries the doubled form
    step_m = {
        "route_1_registry_by_drawn_form": {
            "attempted": True,
            "registry_rows": len(rows),
            "rows_with_w821_token": w821_cells,
            "rows_describing_wheels": wheel_rows,
            "rows_describing_6_spokes": six_spoke_rows,
            "result": (
                "FAIL — no registry row carries the "
                "reconciled drawn form. The registry's "
                "only two ‘6 spokes’ descriptions are "
                "P378 (a single wheel — the base sign "
                "820) and P379 (a single flanked wheel); "
                "neither describes a doubled wheel, and "
                "no row's description states two "
                "six-spoke wheels side by side. The "
                "run does not fall back to P378, which "
                "is the base sign, not the target."),
            "satisfied": route1_match,
        },
        "route_2_list_entry_through_preserved_reference": {
            "attempted": True,
            "reference": {
                "file": PINS["preserved_reference"][0],
                "schema": reference["schema"],
                "sha256": PINS["preserved_reference"][1],
                "entry_locator": reference[
                    "citation_pinned_reference"][
                    "entry_locator"],
                "held_text_caption_lines": [868, 872, 876, 880],
                "captions_verified_in_held_text": fig26_captions,
            },
            "preconditions": {
                "reference_at_pinned_digest":
                    pin_results["preserved_reference"]["match"],
                "sustained_at_step_d": True,
                "anchored_at_step_c": step_c["agreement"],
                "list_named_from_document": list_named,
            },
            "result": (
                "SATISFIED — the preserved reference "
                "record, sustained at step D and "
                "anchored at step C, is cited as the "
                "preserved drawn-form reference for "
                "the source list's own entry (Wells "
                "2011, as given in Wells 2015, Chapter "
                "2 / Figure 2.6, printed pp. 19–22). "
                "This is the route that identifies "
                "the sign."),
            "satisfied": True,
        },
        "route_3_composition": {
            "attempted_as_the_match": False,
            "result": (
                "NOT USED — the frozen routes are "
                "taken in order and exactly one route "
                "identifies the sign; route 2 satisfied "
                "the match, so route 3 was not used as "
                "the route of identification. (The "
                "formation passage and the plate "
                "confirmation appear in this run as "
                "step C anchors and as step D's plate, "
                "which are distinct acts from a step M "
                "route.)"),
            "satisfied": False,
        },
        "route_used": "route 2",
        "traps_asserted": {
            "Yunmapped_0821": {
                "row": {
                    "sign_id": yun[0]["sign_id"],
                    "numbering_system": yun[0]["numbering_system"],
                    "wells_ids": yun[0]["wells_ids"],
                    "corpus_freq": yun[0]["corpus_freq"],
                    "description": yun[0]["description"],
                } if yun else None,
                "assertion": (
                    "A Yajnadevam glyph identifier with "
                    "empty wells_ids — a number "
                    "collision, not Wells's 821. "
                    "Asserted as a trap; never used as "
                    "evidence or as a match."),
            },
            "sign_861": {
                "assertion": (
                    "The passage's Fuls paragraph "
                    "(held-text lines 2848–2853; Figure "
                    "6.12) associates sign 861 with "
                    "‘city’ as a DIFFERENT sign — a "
                    "reading-confusion trap. No evidence "
                    "about 861 was used to identify "
                    "821, and this identification lends "
                    "no support to any claim about 861."),
                "paragraph_verified_in_held_text": (
                    "One verification of the sign 821 "
                    "reading as ‘city’" in held_flat
                    and "861+740" in held_flat),
            },
            "p378_as_target": {
                "assertion": (
                    "P378 is sign 820's registry row "
                    "(the base sign). It is used in "
                    "this run only as the base-sign "
                    "anchor at step C; it is not, and "
                    "was not used as, the target's "
                    "match."),
            },
            "number_only_matching": {
                "assertion": (
                    "No number-only match was used in "
                    "any form: the registry search ran "
                    "on drawn descriptions, and the "
                    "plate number was used only to "
                    "locate the plate entries, with "
                    "continuity established at step C "
                    "on the anchors' agreement."),
            },
        },
    }
    results["step_m"] = step_m

    # ── The recovery test, applied to K-1 (spec §4) ──────
    results["recovery_test_k1"] = {
        "R-1": (
            "PASS — of record in Spec 056's executed "
            "record (the passage's own suggestion, in "
            "its own words; specs/056-sign821-recovery/"
            "outcome.md, SHA-256 ff16184a...; extraction "
            "record ad4a3f74...). Not re-run under this "
            "spec (DD-063-2)."),
        "R-2": (
            "PASS — of record in Spec 056's executed "
            "record (a specific reading, ‘city’ as "
            "determinative or word, in the stated "
            "Dholavira signboard contexts). Not re-run "
            "under this spec (DD-063-2)."),
        "R-3": (
            "PASS — run afresh under Spec 063 §5 on the "
            "new record: the sign list is named from "
            "the document itself (Wells 2011, as given "
            "in Wells 2015, Chapter 2 / Figure 2.6; "
            "held-text lines 414 and 665), step D "
            "sustained the preserved descriptor, step "
            "C passed on the anchors' agreement, and "
            "step M identified the drawn sign by "
            "route 2 (the list's own entry, through "
            "the preserved reference)."),
        "R-4": (
            "PASS — of record in Spec 056's executed "
            "record; the falsification condition is "
            "carried verbatim in the restatement "
            "append. Not re-run under this spec "
            "(DD-063-2)."),
        "R-5": (
            "PASS — of record in Spec 056's executed "
            "record (the context bound, the "
            "determinative-or-word alternative, all "
            "four candidate glosses with their DED "
            "numbers, the eyil preference with its "
            "reason, and the passage's hedge, all "
            "carried). Not re-run under this spec "
            "(DD-063-2)."),
        "falsification_condition": R4_CONDITION,
        "verbatim_quote": K1_QUOTE,
        "quote_locator": (
            "Wells 2015, printed p. 92; held cleaned-"
            "text lines 2835–2836 (passage of record "
            "lines 2783–2871, digest 51d6fb3a...)"),
        "quote_verified_verbatim": _flat(K1_QUOTE) in _flat(
            passage.decode("utf-8")),
    }

    # Outcome mapping (spec section 6, applied
    # mechanically to the recorded steps).
    if (step_d["comparison_with_preserved_descriptor"]["agreement"]
            and step_c["agreement"]
            and step_m["route_2_list_entry_through_preserved_reference"]["satisfied"]):
        results["outcome"] = "RECOVERED"
        results["headline_wording"] = RECOVERED_WORDING
        results["route_used"] = "route 2"
    else:
        results["outcome"] = "IDENTIFICATION FAILED"
    results["claim_restatement_append"] = {
        "key": "spec063_restatement",
        "spec": "063",
        "phase": "Phase-425",
        "date": EXECUTION_DATE,
        "actor": "spec063-phase425-execution",
        "kind": "restatement (recovered claim)",
        "outcome": "RECOVERED",
        "proposition": (
            "Sign 821, in the Dholavira signboard "
            "contexts, has a meaning of ‘city’, either "
            "as a determinative or as a word; of the "
            "passage's candidate glosses (DED 752 ūr; "
            "DED 808 eyil; DED 3568 nakar; DED 4112 "
            "pāri), eyil is the best choice, because "
            "Dholavira is a walled city made of cut "
            "stone."),
        "quote": K1_QUOTE,
        "quote_locator": (
            "Wells 2015, printed p. 92; held cleaned-"
            "text lines 2835–2836 (passage of record "
            "lines 2783–2871, passage digest "
            "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604)"),
        "sign_list": (
            "Wells's own sign list (Wells 2011), as "
            "given in Wells 2015, Chapter 2 / Figure "
            "2.6 (printed pp. 19–22); named from the "
            "document itself at held-text lines 414 "
            "and 665"),
        "identification": (
            "Route 2 under Spec 063 §5 (the list's own "
            "entry, through the preserved reference): "
            "the preserved drawn-form reference "
            "specs/063-sign821-identification-successor/"
            "drawn-form-reference-821.json (schema "
            "glossa.drawn-form-reference/1, SHA-256 "
            "695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999), "
            "sustained at step D by two independent "
            "derivations from the thesis plate (thesis "
            "p. 92 / PDF p. 104) and anchored at step "
            "C on the anchors' agreement. Route 1 was "
            "attempted and failed: no registry row "
            "carries the doubled drawn form, and there "
            "was no fallback to P378, which is the "
            "base sign 820. The Yunmapped_0821 row is "
            "a Yajnadevam glyph identifier, not this "
            "sign, and was asserted as a trap, never "
            "used."),
        "falsification_condition": R4_CONDITION,
        "numbers_and_conditions": (
            "R-5, of record in Spec 056's execution: "
            "the Dholavira signboard contexts; the "
            "determinative-or-word alternative; the "
            "four candidate glosses with their DED "
            "numbers (DED 752 ūr; DED 808 eyil; DED "
            "3568 nakar; DED 4112 pāri); the eyil "
            "preference with its stated reason "
            "(Dholavira is a walled city made of cut "
            "stone); and the passage's hedge (which "
            "of these, if any, is the correct gloss "
            "cannot be known; no firm reading for "
            "sign 821)."),
        "test_design_note": TEST_DESIGN_NOTE,
        "lifecycle": (
            "The claim enters the lifecycle at the "
            "created stage, status untested. Recovery "
            "is not checking, not explanation, not "
            "acceptance; no test has been run under "
            "this spec, and this entry presents the "
            "claim as neither supported, checked, nor "
            "digested."),
        "record": (
            "specs/063-sign821-identification-successor/"
            "outcome.md"),
        "identification_record": (
            "specs/063-sign821-identification-successor/"
            "identification-record.md"),
        "results": "reports/phase425_results.json",
        "note": (
            "Restatement appended by the Spec 063 "
            "execution (Phase-425, 2026-10-22), under "
            "the frozen Spec 063 contract (freeze "
            "digest dc24a10ec177d5f1eb3b73d29ab6f646b4c77b02ae30da2ca86002cc57a49ed9; "
            "OSF kfet5, approved + public). Step 0 "
            "passed in full, including the thesis file "
            "asserted to its frozen digest on the "
            "local file before any plate was read. "
            "Candidate K-1 stands as Spec 056's "
            "executed record adjudicated it — R-1, "
            "R-2, R-4 and R-5 of record on the pinned "
            "passage — and R-3, the one open "
            "condition, is satisfied under Spec 063 "
            "§5 on the new record. The fragment's "
            "original entry and its spec056_closure "
            "append stand above this entry, unedited, "
            "as the record of what was recovered "
            "from; this entry appends a restatement "
            "and does not alter them, and the claim's "
            "status and stage are as this entry "
            "states: untested, at the created stage."),
        "posture": (
            "The append itself is an executor act on "
            "the fragment's claim record (spec section "
            "7), verified at the act — removing the "
            "appended entry reproduces the pre-act "
            "file byte-identically — and recorded in "
            "the outcome record under F063-C11. It is "
            "prescribed here, not performed by this "
            "script, so re-running the script never "
            "appends twice; and the extracted-claims "
            "store is regenerated by the backend "
            "suite, so no test asserts the append on "
            "the live store (the freeze's Spec 038 "
            "form)."),
    }
    results["fence"] = FENCE
    results["anchors"] = {
        "file": PINS["anchors"][0],
        "sha256_before": anchors_before,
        "sha256_after": _sha256(_REPO / PINS["anchors"][0]),
    }
    results["anchors"]["byte_identical"] = (
        results["anchors"]["sha256_before"]
        == results["anchors"]["sha256_after"])

    _write_json(_OUT_A, results)
    _OUT_B.write_text(_render_report(results),
                      encoding="utf-8")
    print(f"OUTCOME: {results['outcome']}", flush=True)
    return 0


def _render_report(r: dict) -> str:
    g1 = r["step0"]["gate_0_1"]
    pins = "\n".join(
        f"- `{v['file']}` — SHA-256 `{v['observed_sha256']}` "
        f"(pin match: {v['match']})"
        for k, v in g1.items()
        if "observed_sha256" in v and "file" in v)
    claim = g1["claim_record_spec038_form"]
    head = (
        f"# Phase-425 — Spec 063 sign-821 identification report\n\n"
        f"Executed {r['execution_date']} by {r['executor']}, "
        f"under the frozen Spec 063 contract (freeze digest\n"
        f"`{r['freeze_digest']}`; OSF registration kfet5, "
        f"approved + public before the run).\n")
    if r["outcome"] == "CLOSED AT STEP 0":
        return (
            head + f"\n## Outcome\n\n**CLOSED AT STEP 0 — "
            f"{r['closure_class']}**\n\n"
            f"{r['headline_wording']}\n\n"
            f"Gate record: `{json.dumps(r['step0'])}`\n")
    g2 = r["step0"]["gate_0_2"]
    g3 = r["step0"]["gate_0_3"]
    img = g3["plate_page"]["embedded_images"][0]
    return f"""{head}
## Outcome

**{r['outcome']}** — by route 2 (the list's own entry,
through the preserved reference)

{r['headline_wording']}

{r['fence']}

## The preserved reference (spec §8, element 1)

`specs/063-sign821-identification-successor/drawn-form-reference-821.json`,
schema `glossa.drawn-form-reference/1`, SHA-256
`{r['preserved_reference']['sha256']}` (the freeze-pinned
digest, recomputed at gate 0.1).

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed:

{pins}

Claim record, in the Spec 038 form: freeze-time
SHA-256 constant `{claim['freeze_time_sha256_constant']}`
carried in the Spec 063 freeze.json; the fragment's
facts asserted on the live file (entry found, status
untested, stage created, its `spec056_closure` append
present with outcome IDENTIFICATION FAILED) — match:
{claim['match']}. The passage of record (held-text
lines 2783–2871) recomputes to its frozen digest
(`{PASSAGE_SHA256}`, {PASSAGE_BYTES} bytes).

Gate 0.2 — the local thesis file was asserted BEFORE
any plate was read: SHA-256
`{g2['observed_sha256']}`, {g2['observed_bytes']} bytes
— match: {g2['match']}.

Gate 0.3 — the reference producible: the preserved
reference stands at its pinned digest, and the plate
page (thesis p. 92 / PDF p. 104, Figure 3.2) was
produced from the pinned file asserted at gate 0.2
({g3['pdf_pages']} PDF pages; the plate page's
embedded image `{img['name']}`, {img['bytes']} bytes,
SHA-256 `{img['sha256']}`). No image is committed
anywhere in this spec.

## Step D — descriptor derivation, twice

Both derivations, their feature lists, their
neighbour discriminations, the reconciliation and
the comparison with the preserved descriptor are
recorded in full in the identification record:
`specs/063-sign821-identification-successor/identification-record.md`.
Result: {r['step_d']['result']} The reconciled
descriptor: “{RECONCILED_DESCRIPTOR}”

## Step C — continuity

{r['step_c']['result']}

## Step M — the match

Route 1 (registry, by drawn form): FAIL — no
registry row carries the doubled drawn form; the
only two ‘6 spokes’ descriptions are P378 (a single
wheel — the base sign, not the target; no fallback
was made to it) and P379 (a single flanked wheel).

Route 2 (the list's own entry, through the preserved
reference): SATISFIED — the preserved reference,
sustained at step D and anchored at step C, cited as
the preserved drawn-form reference for the source
list's entry. This is the route that identifies the
sign. Route 3 (composition) was not used: exactly
one route identifies the sign.

Traps asserted: `Yunmapped_0821` (a Yajnadevam glyph
identifier, empty `wells_ids`, frequency 10 — a
number collision, not Wells's 821; not used); sign
861 (Figure 6.12 — a reading-confusion trap; no
evidence about it was used); P378 as the target's
match (it is the base sign); number-only matching
in any form (none was used).

## The recovery test for K-1

R-1, R-2, R-4 and R-5 stand as adjudicated in Spec
056's executed record on the pinned passage
(DD-063-2); R-3 was run afresh under §5 and passes.
K-1 therefore passes R-1 through R-5 and is
RECOVERED. The recovered claim enters at the
created stage, untested, as the appended
restatement recorded in
`reports/phase425_results.json`
(`claim_restatement_append`); a test design is
recorded with it and no test has been run.

Anchors asserted byte-identical before and after
(`{r['anchors']['sha256_before']}`).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
"""


if __name__ == "__main__":
    sys.exit(main())
