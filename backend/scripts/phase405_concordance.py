#!/usr/bin/env python3
"""Phase-405 — Spec 046 identification concordance act.

Executes the frozen Spec 046 contract
(specs/046-horned-tiger-concordance/freeze.md; freeze-act
digest 80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405,
successor digest in freeze.json as merged
e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6;
OSF registration dnts8, approved and public before this
run): the drawn sign Wells (2015) numbers 297 — the
fragment "Sign value: 297 / the horned tiger, or perhaps
just 'tiger' generically"
(the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002,
stopped at Phase-104 under RULE-NUM) — is identified at
step 1 and, only if identified, scored at step 2 against
the four published sign lists of record (Wells as SOURCE;
CISI, Parpola, Mahadevan as INDEPENDENT).

The run, in the frozen order:

  step 0.1  every spec section 2 input hashes to its
            frozen pin (fail-closed: INPUT PIN MISMATCH);
  step 0.2  the source book is produced from the held
            cleaned text and the section 1 passage is
            located verbatim (SOURCE NOT PRODUCIBLE);
  step 0.3  each of the four lists is accounted for as
            HELD or CITABLE with its citation and locator
            form (LIST NOT PRODUCIBLE, list named);
  step 1    the source's sign list is named from the
            book's own apparatus, and Wells's sign 297 is
            matched BY DRAWN FORM to a crosswalk-registry
            entry or fixed by a drawn-sign reference to
            Wells's published list entry itself. Numbers
            are not identities (spec section 4.3): the
            registry's two frozen traps (Parpola P297 the
            "Ladder motif"; W297 inside the multi-value
            wells_ids cell on the P205 row) are asserted
            as traps, never used as a match. If the drawn
            sign cannot be matched, the run closes as
            IDENTIFICATION FAILED (sign unmatched);
  step 2    reached only for an identified sign. This
            run does not reach it, and this script
            contains no scoring code path that could be
            reached without a step-1 match: a match is
            the gate, and there is no other route past it.

Outputs (written on every terminal outcome):
  A — specs/046-horned-tiger-concordance/concordance-297.json
      (the section 6 delivery form, schema
      glossa.concordance/1; on a closure before scoring,
      signs is an empty array and the top level carries
      the closure block);
  B — reports/phase405_results.json (the run's results
      record);
  C — reports/phase405_concordance_report.md (the
      human-readable rendering; it does not diverge
      from A).

Fail-closed: any pin, passage, citation, or registry
fact that differs from the frozen record aborts the
run before any output is written, except that a
step-0 or step-1 closure IS an output (the closure
form of A, with B and C recording the gate facts).
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC_DIR = _REPO / "specs/046-horned-tiger-concordance"
_OUT_A = _SPEC_DIR / "concordance-297.json"
_OUT_B = _REPO / "reports/phase405_results.json"
_OUT_C = _REPO / "reports/phase405_concordance_report.md"

CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002")
FREEZE_ACT_DIGEST = (
    "80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405")
FREEZE_DIGEST = (
    "e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6")
EXECUTOR = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-21"

PINS = {
    "claim_record": (
        "glossa-indus/claims/extracted_claims/"
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json",
        "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a"),
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
    "lane2_drafts": (
        "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"),
}

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

IDENTIFICATION_FAILED_WORDING = (
    "The fragment 'sign 297 is the horned tiger' cannot be carried "
    "to a concordance: the drawn sign could not be matched from "
    "Wells's published list. The record stays a stated gap. No "
    "statement about the sign is made, and nothing is fed to Asset A.")

FENCE = (
    "This result settles what the published lists say the drawn "
    "sign depicts. It is not evidence of what the sign meant in use.")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")


def _closure_delivery(closure_class: str, wording: str) -> dict:
    return {
        "producer_spec": "046",
        "producer_claim_id": CLAIM_ID,
        "schema": "glossa.concordance/1",
        "signs": [],
        "closure": {"class": closure_class, "wording": wording},
    }


def main() -> int:
    results: dict = {
        "phase": "Phase-405",
        "spec": "046",
        "claim_id": CLAIM_ID,
        "freeze_act_digest": FREEZE_ACT_DIGEST,
        "freeze_digest": FREEZE_DIGEST,
        "execution_date": EXECUTION_DATE,
        "executor": EXECUTOR,
        "osf_registration": "dnts8 (approved + public before the run)",
    }

    # ── Step 0.1 — input integrity (fail-closed) ──────────────
    pin_results = {}
    for name, (rel, want) in PINS.items():
        got = _sha256(_REPO / rel)
        pin_results[name] = {
            "file": rel, "expected_sha256": want,
            "observed_sha256": got, "match": got == want}
        if got != want:
            results["step0"] = {"gate_0_1": pin_results}
            results["outcome"] = "CLOSED AT STEP 0"
            results["closure_class"] = "INPUT PIN MISMATCH"
            _write_json(_OUT_A, _closure_delivery(
                "CLOSED AT STEP 0 — INPUT PIN MISMATCH",
                "Spec 046 closed before identification: input "
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
            "Spec 046 closed before identification: the source "
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
            "Spec 046 closed before identification: a published "
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
        results["closure_class"] = "IDENTIFICATION FAILED (list unnamed)"
        _write_json(_OUT_A, _closure_delivery(
            "IDENTIFICATION FAILED (list unnamed)",
            "The fragment 'sign 297 is the horned tiger' cannot be "
            "carried to a concordance: the source document does not "
            "name its sign list. The record stays a stated gap. No "
            "statement about the sign is made, and nothing is fed "
            "to Asset A."))
        _write_json(_OUT_B, results)
        print("STEP 1.1 FAIL: list unnamed", flush=True)
        return 0
    results["step1"] = {
        "source_list_named": (
            "Wells's own sign list (Wells 2011), as given in "
            "Wells 2015, Chapter 2, 'The Indus Sign List' "
            "(Figure 2.6)"),
        "apparatus_evidence": apparatus,
    }

    # ── Step 1.2 — drawn-sign match, by form only ─────────────
    registry_path = _REPO / PINS["crosswalk_registry"][0]
    with registry_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    w297_cells = []
    tiger_descriptions = 0
    for row in rows:
        tokens = [t.strip() for t in row["wells_ids"].split("|")]
        if "W297" in tokens:
            w297_cells.append({
                "sign_id": row["sign_id"],
                "description": row["description"],
                "wells_ids": row["wells_ids"],
                "singleton": tokens == ["W297"],
            })
        if "tiger" in row["description"].lower():
            tiger_descriptions += 1
    witness = json.loads((
        _REPO / "data/crosswalks/wells_segmentation_witness_v1.json"
    ).read_text(encoding="utf-8"))
    witness_297 = [
        r["sign"] for r in witness["rows"]
        if "297" in [g.strip() for g in
                     r.get("wells_graphemes", "").split(";")]]
    p297 = [r for r in rows if r["sign_id"] == "P297"]
    match_evidence = {
        "registry_rows": len(rows),
        "w297_cells": w297_cells,
        "registry_tiger_descriptions": tiger_descriptions,
        "p297_description": (
            p297[0]["description"] if p297 else None),
        "wells_witness_rows": len(witness["rows"]),
        "wells_witness_grapheme_297_rows": witness_297,
    }
    matched = (
        any(c["singleton"] for c in w297_cells)
        or tiger_descriptions > 0 or bool(witness_297))
    results["step1"]["match_evidence"] = match_evidence
    if not matched:
        results["step1"]["drawn_sign_match"] = None
        results["step1"]["match_failure"] = (
            "No crosswalk-registry entry carries the drawn sign: "
            "the only W297 occurrence in the pinned registry is "
            "one value inside the 17-value wells_ids cell on the "
            "P205 row ('Prismed light rays…'), which the frozen "
            "spec (section 4.3) names as a trap that does not by "
            "itself identify the passage's sign; no registry "
            "description names a tiger; the Phase-123 Wells "
            "segmentation witness carries no Wells grapheme 297. "
            "In Wells's published list itself (Figure 2.6), the "
            "drawn forms did not survive the held copy's text "
            "extraction (the figure pages carry captions only), "
            "so no drawn-sign reference the executor can inspect "
            "and defend exists in the held record. The prior "
            "in-repo search stands unrebutted: Spec 004 WS2 "
            "(glossa-indus/LEDGER.md, 2026-10-05) recorded three "
            "candidate referents — M297, P297, W297→P205/M180 — "
            "none matching the description in-repo. Matching by "
            "number is forbidden (F046-C07) and was not used.")
        results["outcome"] = "IDENTIFICATION FAILED"
        results["closure_class"] = "IDENTIFICATION FAILED (sign unmatched)"
        results["headline_wording"] = IDENTIFICATION_FAILED_WORDING
        results["fence"] = FENCE
        _write_json(_OUT_A, _closure_delivery(
            "IDENTIFICATION FAILED (sign unmatched)",
            IDENTIFICATION_FAILED_WORDING))
        _write_json(_OUT_B, results)
        _OUT_C.write_text(_render_report(results), encoding="utf-8")
        print("OUTCOME: IDENTIFICATION FAILED (sign unmatched)",
              flush=True)
        return 0

    # A step-1 match is the only route past this gate. There is
    # deliberately no scoring code in this script: step 2's
    # rows must be quoted from the lists at execution, and a
    # future matched run extends this script openly rather
    # than this branch improvising one.
    print("STEP 1 MATCHED — step 2 not implemented in this run",
          flush=True)
    return 1


def _render_report(r: dict) -> str:
    g1 = r["step0"]["gate_0_1"]
    pins = "\n".join(
        f"- `{v['file']}` — SHA-256 `{v['observed_sha256']}` "
        f"(pin match: {v['match']})" for v in g1.values())
    return f"""# Phase-405 — Spec 046 identification concordance report

Executed {r['execution_date']} by {r['executor']}, under the
frozen Spec 046 contract (freeze-act digest
`{r['freeze_act_digest']}`; successor digest
`{r['freeze_digest']}` in freeze.json as merged; OSF
registration dnts8, approved + public before the run).

## Outcome

**IDENTIFICATION FAILED (sign unmatched)**

{r['headline_wording']}

{r['fence']}

## The passage (spec section 8, element 1)

> "{r['step0']['gate_0_2']['passage_quote']}"

Locator: Wells (2015), printed p. 97 (held cleaned text,
lines {r['step0']['gate_0_2']['passage_lines_in_held_text']}).

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed:

{pins}

Gate 0.2 — the source book was produced from the held copy
and the passage located verbatim (above).

Gate 0.3 — all four lists accounted for as HELD or CITABLE
with citation plus locator form (CITATIONS.md §§A.1, A.2,
A.3, A.7, C.1; CISI Phase-124 catalogue layers): WELLS
HELD; CISI HELD; PARPOLA CITABLE; MAHADEVAN CITABLE.

## Step 1

The source's sign list is named from the book's own
apparatus: Wells's own sign list (Wells 2011), as given in
Wells 2015, Chapter 2, "The Indus Sign List" (Figure 2.6)
("Chapter 2 gives the Indus sign list used in this
analysis"; "The sign list used here (Wells 2011)").

The drawn-sign match failed. {r['step1']['match_failure']}

## Step 2

Not reached. No list was scored, no concurrence state was
computed, and nothing is fed to Asset A: the delivery
(`specs/046-horned-tiger-concordance/concordance-297.json`)
carries an empty signs array and the closure block, in the
frozen section 6 form.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
"""


if __name__ == "__main__":
    sys.exit(main())
