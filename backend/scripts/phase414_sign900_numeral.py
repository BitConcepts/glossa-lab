#!/usr/bin/env python3
"""Phase-414 — Spec 055 sign-900 numeral test act.

Executes the frozen Spec 055 contract
(specs/055-sign900-numeral/freeze.md; freeze digest
42ef82829ade894918b0bf946ac44354224d689202e2f7bf00eb747821bdedfc;
OSF registration tbyqg, approved and public before this
run): the fragment "Sign value: 900 / number six"
(ancient_writing_and_modern_technologies_51831ac9_sign_val_0001,
stopped at Phase-104 under RULE-NUM) is carried through
the two frozen stages — stage 1 identifies the sign the
source document numbers 900 (the source-table recovery,
preserved as source-table-recovery.json on EVERY terminal
outcome), and stage 2, only if stage 1 succeeds, tests
the identified sign's numeral behaviour on the strict
corpus pinned at gate 0.4 under the three frozen
measures of spec section 5.

The run, in the frozen order:

  step 0.1  every spec section 2 input hashes to its
            frozen pin (fail-closed: INPUT PIN MISMATCH);
  step 0.2  the source document is produced from the
            held cleaned text and the section 1 material
            is located verbatim (SOURCE NOT PRODUCIBLE);
  step 0.3  recovery before verdict: the section 6
            recovery record is the FIRST output written;
            no identification wording exists anywhere
            before it;
  step 1    the source's sign list is named from the
            document's own text (verbatim quoted naming
            statements with locators), the full sign-900
            material is recovered verbatim, and the drawn
            sign is matched BY DRAWN FORM ONLY to a
            crosswalk-registry entry or to the named
            list's entry for 900. Numbers are not
            identities (F055-C07): the registry's W900
            value inside the wells_ids cell of the P154
            row is recorded as the frozen trap — it is
            neither the identification nor an exclusion;
            the match rests on drawn-form descriptions
            (the named list's sign 900 as a single-arc
            grapheme, per the verified Phase-123 Wells
            segmentation witness; the registry's plain
            right-parenthesis row, the only registry row
            whose drawn description is a single right
            parenthesis with no added element);
  gate 0.4  the strict-corpus layer of record (the
            program's V3 / Mahadevan-lineage corpus as
            held — the Mahadevan-1977-scheme records of
            the tracked primary corpus, per the executed
            Spec 033 precedent for the same layer) is
            exported in full and pinned by SHA-256; the
            identified sign's census is taken (floor 5,
            DD-055-12);
  step 2    the pre-counting record first (the
            known-numeral set from published
            identifications — the source document's own
            stroke-sign identification; the target
            excluded; hedged members excluded and listed
            separately, DD-055-14; the control set by the
            frozen nearest-10 rule, DD-055-11; and the
            DD-055-16 dry-run on a non-target sign), then
            the three frozen measures computed
            identically for target, numeral set, and
            controls, and the outcome assigned by the
            section 5.3 mapping alone.

No outcome of this spec establishes the value six
(F055-C15): the source document's own argument for six
is preserved in the recovery record as source material
and is evidence at no stage. Design D-16 does not join
this campaign even though this recovery is the act that
would unblock it; D-16 waits for its own planning gate
(campaign decision E-7).

Outputs:
  A — specs/055-sign900-numeral/source-table-recovery.json
      (spec section 6, schema glossa.source-table-recovery/1;
      produced on every terminal outcome, FIRST);
  B — reports/phase414_results.json (the run's results
      record: gates, census, pre-counting record,
      per-measure table, outcome);
  C — reports/phase414_sign900_report.md (the human-
      readable rendering; it does not diverge from A/B);
  D — specs/055-sign900-numeral/strict-corpus-export.jsonl
      (the gate-0.4 export of the pinned layer, in full,
      when gate 0.4 is reached).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC_DIR = _REPO / "specs/055-sign900-numeral"
_OUT_A = _SPEC_DIR / "source-table-recovery.json"
_OUT_B = _REPO / "reports/phase414_results.json"
_OUT_C = _REPO / "reports/phase414_sign900_report.md"
_OUT_D = _SPEC_DIR / "strict-corpus-export.jsonl"

CLAIM_ID = (
    "ancient_writing_and_modern_technologies_"
    "51831ac9_sign_val_0001")
FREEZE_DIGEST = (
    "42ef82829ade894918b0bf946ac44354224d689202e2f7bf00eb747821bdedfc")
EXECUTOR = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-21"
BASE_COMMIT = "3200b7b5b6841a7b9567a81368bf84004fd17255"

PINS = {
    "claim_record": (
        "glossa-indus/claims/extracted_claims/"
        "ancient_writing_and_modern_technologies_51831ac9.json",
        "e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8"),
    "held_text": (
        "glossa-indus/processed/cleaned_text/"
        "ancient_writing_and_modern_technologies_51831ac9.txt",
        "1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4"),
    "literature_record": (
        "glossa-indus/literature/documents/"
        "ancient_writing_and_modern_technologies_51831ac9.json",
        "92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c"),
    "phase104_evaluation": (
        "glossa-indus/reports/phase104_claims_evaluation.json",
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"),
    "crosswalk_registry": (
        "data/crosswalks/canonical_sign_registry.csv",
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"),
    "lane2_drafts": (
        "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"),
    "anchors": (
        "backend/reports/INDUS_FINAL_ANCHORS.json",
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
}

WITNESS_FILE = "data/crosswalks/wells_segmentation_witness_v1.json"
CORPUS_FILE = "glossa-corpus/indus/exports/indus_research.jsonl"
OCCURRENCE_FLOOR = 5

FENCE = (
    "This result is about how one identified sign behaves "
    "in recorded data. It is not evidence of what any sign "
    "means, and it does not establish the value six.")
CHAIN = (
    "Design D-16 does not join this campaign even though "
    "this recovery is the act that would unblock it; D-16 "
    "waits for its own planning gate (campaign decision "
    "E-7).")

# The known-numeral set's published identification (spec
# section 5.1): the source document's own statement, under
# SPECIAL NUMERICAL SIGNS, that "The numerical value of
# stroke signs is most likely the number of strokes" —
# the stroke signs are the script's known numeral signs.
# A member enters the set only through a registry row
# whose drawn description is a group of simple vertical
# strokes and nothing else (no added motif, bracket,
# cap, or cage), crosswalked to its Mahadevan corpus
# identifier(s). Registry sign_ids of the pure-stroke
# rows, in registry order:
STROKE_ROW_IDS = [
    "P121", "P122", "P123", "P124", "P125", "P126", "P127",
    "P128", "P129", "P130", "P139", "P140", "P141", "P142",
    "P144", "P145", "P147", "P150", "P151", "P152",
]
# Guard for the stroke rows: a pure-stroke drawn
# description uses only stroke vocabulary — any other
# word (a motif, a bracket, a cap, a cage) fails the run
# closed rather than letting a decorated sign into the
# numeral set.
_STROKE_VOCAB = {
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "adjacent", "half-height",
    "simple", "vertical", "stroke", "strokes", "short",
    "full-height", "tall", "stacked", "small", "over",
    "rows", "of", "off-center", "or", "slanted", "above",
    "the", "same", "third", "and", "maybe", "second",
    "is", "angled", "away", "slightly"}


def _is_pure_stroke_description(description: str) -> bool:
    words = re.findall(r"[a-z-]+", description.lower())
    return bool(words) and set(words) <= _STROKE_VOCAB

# Hedged numeral candidates (DD-055-14): published
# identifications hedged in the source document itself.
# They do NOT enter the set; they are listed separately.
HEDGED = [
    {"source_sign_no": "415",
     "source_quote": (
         "It is therefore suggested that Sign 415 is a "
         "special numerical sign, at least in some context"),
     "hedge": "suggested, and only 'at least in some context'"},
    {"source_sign_no": "70",
     "source_quote": (
         "Sign 70 may also be regarded as a numerical sign. "
         "It often appears together with stroke signs in "
         "positional notations (Figure 13). Since Sign 70 "
         "often follows two long or short strokes (Sign 2 "
         "or 32), a non-numerical interpretation as a "
         "bounded cluster is possible as well."),
     "hedge": ("'may also be regarded'; a non-numerical "
               "interpretation stated as possible in the "
               "same passage")},
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _sentence(flat: str, start: str, end: str) -> str | None:
    i = flat.find(start)
    if i < 0:
        return None
    j = flat.find(end, i)
    if j < 0:
        return None
    return flat[i:j + len(end)]


def _clean_tokens(tokens) -> list[str]:
    """The V3 loader's own cleaning rules (indus_corpus_v3,
    as applied by the executed Spec 033 run for this same
    layer): numeric Mahadevan ids only; '000'/'0'
    placeholders and '*'-prefixed supplementary tokens
    dropped."""
    out = []
    for t in tokens or []:
        if t is None:
            continue
        t = str(t)
        if t in ("000", "0") or t.startswith("*"):
            continue
        try:
            out.append(str(int(t)))
        except ValueError:
            continue
    return out


def _measures(sequences: list[list[str]], sign: str,
              numeral_ids: set[str]) -> dict:
    occ = 0
    short = 0
    adjacent = 0
    positions: Counter = Counter()
    for seq in sequences:
        for idx, tok in enumerate(seq):
            if tok != sign:
                continue
            occ += 1
            if len(seq) <= 3:
                short += 1
            neighbours = []
            if idx > 0:
                neighbours.append(seq[idx - 1])
            if idx + 1 < len(seq):
                neighbours.append(seq[idx + 1])
            if any(n in numeral_ids for n in neighbours):
                adjacent += 1
            positions[idx] += 1
    if occ == 0:
        return {"occurrences": 0, "short_text_share": None,
                "numeral_adjacency_share": None,
                "positional_entropy_bits": None}
    entropy = -sum(
        (c / occ) * math.log2(c / occ)
        for c in positions.values())
    return {
        "occurrences": occ,
        "short_text_share": round(short / occ, 6),
        "numeral_adjacency_share": round(adjacent / occ, 6),
        "positional_entropy_bits": round(entropy, 6),
    }


def _median(values: list[float]) -> float:
    s = sorted(values)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def _classify(target_m: dict, numeral_ms: list[dict],
              control_ms: list[dict]) -> dict:
    keys = ["short_text_share", "numeral_adjacency_share",
            "positional_entropy_bits"]
    per_measure = {}
    n_side = 0
    o_side = 0
    for k in keys:
        tv = target_m[k]
        nvals = [m[k] for m in numeral_ms if m[k] is not None]
        cvals = [m[k] for m in control_ms if m[k] is not None]
        n_med = _median(nvals)
        c_med = _median(cvals)
        numeral_side = (
            min(nvals) <= tv <= max(nvals)
            and tv != c_med
            and (tv - c_med) * (n_med - c_med) > 0)
        control_side = min(cvals) <= tv <= max(cvals)
        if numeral_side:
            n_side += 1
        if control_side:
            o_side += 1
        per_measure[k] = {
            "target": tv,
            "numeral_range": [min(nvals), max(nvals)],
            "numeral_median": round(n_med, 6),
            "control_range": [min(cvals), max(cvals)],
            "control_median": round(c_med, 6),
            "numeral_side": numeral_side,
            "control_side": control_side,
        }
    if n_side >= 2 and o_side < 2:
        outcome = "NUMERAL-LIKE"
    elif o_side >= 2 and n_side < 2:
        outcome = "NOT NUMERAL-LIKE"
    else:
        outcome = "MIXED"
    return {"per_measure": per_measure,
            "numeral_side_count": n_side,
            "control_side_count": o_side,
            "outcome": outcome}


def _control_set(counts: Counter, target_count: int,
                 excluded: set[str]) -> list[str]:
    ordinary = [s for s in counts if s not in excluded]
    ordinary.sort(key=lambda s: (abs(counts[s] - target_count),
                                 int(s)))
    return ordinary[:10]


def main() -> int:
    results: dict = {
        "phase": "Phase-414",
        "spec": "055",
        "claim_id": CLAIM_ID,
        "freeze_digest": FREEZE_DIGEST,
        "execution_date": EXECUTION_DATE,
        "executor": EXECUTOR,
        "base_commit": BASE_COMMIT,
        "osf_registration": "tbyqg (approved + public before the run)",
    }
    anchors_before = _sha256(_REPO / PINS["anchors"][0])

    recovery: dict = {
        "producer_spec": "055",
        "producer_claim_id": CLAIM_ID,
        "schema": "glossa.source-table-recovery/1",
        "source_document": {},
        "sign_list_naming": {"list_named": None,
                             "naming_statements": []},
        "recovered_material": [],
        "figure_refs": [],
        "target_sign": {
            "source_sign_no": "900",
            "drawn_sign_match_basis": None,
            "crosswalk_registry_id": None,
            "named_list_locator": None,
            "match_citation": None},
        "sign_700_material": {"present": False, "locators": []},
        "recovery_outcome": None,
    }

    def close(outcome: str, closure_class: str, wording: str) -> int:
        """Write the recovery record FIRST (gate 0.3), then
        the results record, on every closure outcome."""
        recovery["recovery_outcome"] = closure_class
        recovery["closure"] = {"class": closure_class,
                               "wording": wording}
        _write_json(_OUT_A, recovery)
        results["outcome"] = outcome
        results["closure_class"] = closure_class
        results["headline_wording"] = wording
        results["fence"] = FENCE
        results["chain_sentence"] = CHAIN
        results["anchors"] = {
            "file": PINS["anchors"][0],
            "sha256_before": anchors_before,
            "sha256_after": _sha256(_REPO / PINS["anchors"][0]),
            "byte_identical": (
                anchors_before == _sha256(_REPO / PINS["anchors"][0])),
        }
        _write_json(_OUT_B, results)
        _OUT_C.write_text(_render_report(results, recovery),
                          encoding="utf-8")
        print(f"OUTCOME: {closure_class}", flush=True)
        return 0

    # ── Step 0.1 — input integrity (fail-closed) ──────────
    pin_results = {}
    for name, (rel, want) in PINS.items():
        got = _sha256(_REPO / rel)
        pin_results[name] = {
            "file": rel, "expected_sha256": want,
            "observed_sha256": got, "match": got == want}
        if got != want:
            results["step0"] = {"gate_0_1": pin_results}
            return close(
                "CLOSED AT STEP 0",
                "CLOSED AT STEP 0 — INPUT PIN MISMATCH",
                "Spec 055 closed before identification: "
                f"input {name} did not hash to its frozen "
                "pin. No identification was recorded and "
                "no statement about the sign is made. The "
                "recovery record carries the closure.")
    results["step0"] = {"gate_0_1": pin_results,
                        "verdict": "PASS"}

    # ── Step 0.2 — source producible, material verbatim ──
    lit = json.loads((_REPO / PINS["literature_record"][0])
                     .read_text(encoding="utf-8"))
    recovery["source_document"] = {
        "document_id": lit["document_id"],
        "title": lit["detected_title"],
        "author": "Andreas Fuls (Technische Universität Berlin)",
        "held_text_ref": PINS["held_text"][0],
        "held_text_sha256": pin_results["held_text"]["observed_sha256"],
        "literature_record_ref": PINS["literature_record"][0],
        "original_file": {
            "name": lit["original_filename"],
            "size": lit["file_size_bytes"],
            "intake_checksum": lit["checksum_sha256"]},
    }
    text = (_REPO / PINS["held_text"][0]).read_text(encoding="utf-8")
    lines = text.splitlines()
    flat = _flat(text)

    def _line_exact(target: str) -> int | None:
        for i, line in enumerate(lines):
            if line.strip() == target:
                return i
        return None

    idx_sign900 = _line_exact("Sign 900")
    idx_numval = _line_exact("Numerical value of Sign 900")
    idx_summary = _line_exact("SUMMARY")
    idx_700 = _line_exact("SIGN 700 WITH NUMBERS")
    idx_listitems = _line_exact("List of items on a four-sided seal")
    table1_caption = None
    for i, line in enumerate(lines):
        if line.strip().startswith("T able 1:"):
            table1_caption = i
            break
    fig_caps = {}
    for fig in ("Figure 11:", "Figure 12:", "Figure 29:"):
        for i, line in enumerate(lines):
            if line.strip().startswith(fig):
                fig_caps[fig] = (i, line.strip())
                break
    required = [idx_sign900, idx_numval, idx_summary,
                table1_caption,
                fig_caps.get("Figure 11:"), fig_caps.get("Figure 12:"),
                fig_caps.get("Figure 29:")]
    if any(v is None for v in required):
        results["step0"]["gate_0_2"] = {
            "located_verbatim": False,
            "missing": [str(v) for v in required if v is None]}
        return close(
            "CLOSED AT STEP 0",
            "CLOSED AT STEP 0 — SOURCE NOT PRODUCIBLE",
            "Spec 055 closed before identification: the "
            "source document could not be produced from "
            "the program's held copy. No identification "
            "was recorded and no statement about the sign "
            "is made. The recovery record carries the "
            "closure.")
    results["step0"]["gate_0_2"] = {
        "source": PINS["held_text"][0],
        "located_verbatim": True,
        "sections_located": [
            "'Sign 900' section (printed p. 68)",
            "'Numerical value of Sign 900' section with "
            "its Table 1 caption (printed pp. 72–74)",
            "summary statement (printed p. 85)"],
    }
    results["step0"]["gate_0_3"] = {
        "recovery_before_verdict": True,
        "note": ("the recovery record (output A) is "
                 "written before the results record and "
                 "before any measure exists, on every "
                 "terminal outcome")}

    # ── Step 1.1 — name the sign list from the document ──
    q1 = _sentence(
        flat, "The signs are coded according to an extended "
        "sign list with 702 distinct signs", "(W ells 2015).")
    q2 = _sentence(
        flat, "The sign list by W ells (2011, 2015) has been "
        "extended to currently 702 distinct signs",
        "distinct signs")
    q3 = _sentence(
        flat, "They involve a sign list of about 702 "
        "distinct signs", "distinct signs")
    q4 = None
    for line in lines:
        if line.strip().startswith("APPENDIX A: SIGN LIST WITH"):
            q4 = line.strip()
            break
    naming = []
    if q1:
        naming.append({
            "quote": q1,
            "locator": "p. 57, opening section (introduction)"})
    if q2:
        naming.append({
            "quote": q2,
            "locator": "p. 59, 'SIGN LIST'"})
    if q3:
        naming.append({
            "quote": q3,
            "locator": "p. 85, 'SUMMARY'"})
    if q4:
        naming.append({
            "quote": q4,
            "locator": "p. 88, 'APPENDIX A'"})
    recovery["sign_list_naming"]["naming_statements"] = naming

    # ── Step 1 recovery material (verbatim, with locators) ─
    def _block(start_idx: int, end_idx: int) -> str:
        return "\n".join(lines[start_idx:end_idx + 1])

    recovery["recovered_material"] = [
        {"section_heading": "Sign 900",
         "locator": "p. 68, 'Sign 900' (SPECIAL NUMERICAL SIGNS)",
         "text_verbatim": _block(idx_sign900, idx_sign900 + 8)},
        {"section_heading": "Numerical value of Sign 900",
         "locator": ("pp. 72–74, 'Numerical value of Sign 900' "
                     "(NUMERICAL VALUES OF SIGNS)"),
         "text_verbatim": _block(idx_numval, idx_numval + 60),
         "table_1": {
             "caption_verbatim": _block(
                 table1_caption, table1_caption + 2),
             "locator": ("p. 72, 'Table 1' (NUMERICAL VALUES "
                         "OF SIGNS)"),
             "body_note": (
                 "the table's numeric grid did not survive "
                 "the held copy's text extraction: the held "
                 "cleaned text carries the caption and the "
                 "surrounding prose (both recovered above), "
                 "and no table body rows. Nothing was "
                 "reconstructed.")}},
        {"section_heading": "List of items on a four-sided seal",
         "locator": ("p. 74, 'List of items on a four-sided "
                     "seal' (NUMERICAL VALUES OF SIGNS) — "
                     "the Figure 18 continuation of the "
                     "Sign 900 value derivation"),
         "text_verbatim": _block(idx_listitems, idx_listitems + 24)},
        {"section_heading": "SUMMARY",
         "locator": "p. 85, 'SUMMARY'",
         "text_verbatim": _block(idx_summary + 5, idx_summary + 14)},
    ]
    recovery["figure_refs"] = [
        {"figure": "Figure 11",
         "caption_verbatim": fig_caps["Figure 11:"][1],
         "locator": "p. 68, 'Figure 11' (SPECIAL NUMERICAL SIGNS)"},
        {"figure": "Figure 12",
         "caption_verbatim": fig_caps["Figure 12:"][1],
         "locator": "p. 69, 'Figure 12'"},
        {"figure": "Figure 29",
         "caption_verbatim": fig_caps["Figure 29:"][1],
         "locator": "p. 85, 'Figure 29' (SUMMARY)"},
    ]
    if idx_700 is not None:
        recovery["sign_700_material"] = {
            "present": True,
            "locators": [
                "p. 70, 'SIGN 700 WITH NUMBERS'",
                ("pp. 72–74, 'Numerical value of Sign 900' "
                 "(NUMERICAL VALUES OF SIGNS) — Sign 700 "
                 "units are the counted objects of the "
                 "three two-sided tablets")],
        }

    if not q1 or not q2:
        recovery["recovery_outcome"] = (
            "IDENTIFICATION FAILED (list unnamed)")
        return close(
            "IDENTIFICATION FAILED",
            "IDENTIFICATION FAILED (list unnamed)",
            "The fragment 'sign 900 means six' cannot be "
            "carried to a behaviour test: the source "
            "document does not name its sign list from its "
            "own text. The record stays a stated gap — not "
            "a verdict on 'six', and not a verdict on the "
            "sign. Spec 055's recovery record preserves "
            "what the source does say, in full.")
    list_named = (
        "the extended Wells (2011, 2015) sign list of 702 "
        "distinct signs (Wells 2015; the ICIT database's "
        "sign list, Appendix A)")
    recovery["sign_list_naming"]["list_named"] = list_named

    # ── Step 1.2 — drawn-sign match, by drawn form only ──
    registry_path = _REPO / PINS["crosswalk_registry"][0]
    with registry_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    witness = json.loads((_REPO / WITNESS_FILE).read_text(
        encoding="utf-8"))
    witness_900 = [
        r for r in witness["rows"]
        if "900" in [g.strip() for g in
                     str(r.get("wells_graphemes", "")).split(";")]]
    plain_paren = [
        r for r in rows
        if re.fullmatch(
            r"Right parenthesis( \(perhaps with a backward "
            r"curve at the bottom\))?",
            r["description"].strip())]
    p154 = [r for r in rows if r["sign_id"] == "P154"]
    match_evidence = {
        "registry_rows": len(rows),
        "witness_rows_for_grapheme_900": [
            {"sign": r["sign"], "treatment": r["treatment"],
             "correspondence_method": r["correspondence_method"],
             "verification": r["verification"],
             "note": r["note"],
             "thesis_source": r["thesis_source"]}
            for r in witness_900],
        "plain_right_parenthesis_rows": [
            {"sign_id": r["sign_id"],
             "description": r["description"],
             "mahadevan_ids": r["mahadevan_ids"]}
            for r in plain_paren],
        "p154_row": (
            {"sign_id": p154[0]["sign_id"],
             "description": p154[0]["description"],
             "wells_ids": p154[0]["wells_ids"],
             "mahadevan_ids": p154[0]["mahadevan_ids"],
             "corpus_freq": p154[0]["corpus_freq"]}
            if p154 else None),
        "trap_note": (
            "the W900 value inside the wells_ids cell of "
            "the P154 row is recorded here as the frozen "
            "trap (F055-C07): it was NOT used as the "
            "identification, and its drawn description "
            "was NOT treated as a refutation; the match "
            "below rests on drawn-form descriptions only"),
    }
    matched = (
        len(witness_900) == 1
        and witness_900[0]["sign"] == "M287"
        and witness_900[0]["verification"] == "verified"
        and "single-arc grapheme" in witness_900[0]["note"]
        and len(plain_paren) == 1
        and plain_paren[0]["sign_id"] == "P154"
        and plain_paren[0]["mahadevan_ids"] == "M287")
    results["step1"] = {
        "list_named": list_named,
        "naming_statements": naming,
        "match_evidence": match_evidence,
        "drawn_sign_match": None,
    }
    if not matched:
        recovery["target_sign"] = {
            "source_sign_no": "900",
            "drawn_sign_match_basis": None,
            "crosswalk_registry_id": None,
            "named_list_locator": None,
            "match_citation": (
                "match attempted by drawn form and failed; "
                "evidence in the run's results record "
                "(step1.match_evidence)"),
            "failure_class": "IDENTIFICATION FAILED (sign unmatched)"}
        recovery["recovery_outcome"] = (
            "IDENTIFICATION FAILED (sign unmatched)")
        return close(
            "IDENTIFICATION FAILED",
            "IDENTIFICATION FAILED (sign unmatched)",
            "The fragment 'sign 900 means six' cannot be "
            "carried to a behaviour test: the drawn sign "
            "its number 900 labels could not be matched "
            "by drawn form to the crosswalk registry or "
            "to the named list's entry. The record stays "
            "a stated gap — not a verdict on 'six', and "
            "not a verdict on the sign. Spec 055's "
            "recovery record preserves what the source "
            "does say, in full.")
    target_corpus_id = "287"
    match_citation = (
        "Drawn-form match: the named list's sign 900 is "
        "the single-arc grapheme — the Phase-123 Wells "
        "segmentation witness (data/crosswalks/"
        "wells_segmentation_witness_v1.json, row M287; "
        "treatment SAME; verification: verified) records, "
        "from glyph inspection of Wells's PhD 2006 "
        "Figure 3.2 plates (thesis p. 92; numbering as "
        "cross-matched in the held canonical registry, "
        "the Wells 2015 form of the Wells/ICIT list): "
        "'W900 is the single-arc grapheme; thickness "
        "difference is font weight only', and its "
        "companion row records that the plates' arc signs "
        "(900–921) are all narrow parenthesis/C forms. In "
        "the crosswalk registry exactly one row's drawn "
        "description is a plain right parenthesis with no "
        "added element — P154, 'Right parenthesis "
        "(perhaps with a backward curve at the bottom)' "
        "(every neighbouring parenthesis row carries an "
        "addition — a line, stroke, tooth, leaf, outline, "
        "or a second parenthesis — or faces left). The "
        "two records agree on the pairing by drawn form: "
        "the witness row is the M287 row, and P154's "
        "Mahadevan crosswalk is M287. The identified "
        "sign's identifier in the pinned strict corpus "
        "is therefore Mahadevan 287. The registry's W900 "
        "cell on this row is consistent with the match "
        "but is not its basis (F055-C07). The source "
        "PDF's own figures (Figures 11, 12, 29) could not "
        "be produced from the held record — the original "
        "PDF is not held in the repository (the "
        "literature record's stored path is a workstation "
        "path) — so the drawn-form check rests on the "
        "witness's verified glyph inspection, stated "
        "openly here.")
    recovery["target_sign"] = {
        "source_sign_no": "900",
        "drawn_sign_match_basis": "crosswalk-registry",
        "crosswalk_registry_id": "P154",
        "named_list_locator": (
            "extended Wells (2011, 2015) list, sign 900 "
            "(Wells PhD 2006, Fig. 3.2, thesis p. 92, per "
            "the Phase-123 Wells segmentation witness)"),
        "match_citation": match_citation}
    recovery["recovery_outcome"] = "IDENTIFIED"
    results["step1"]["drawn_sign_match"] = {
        "crosswalk_registry_id": "P154",
        "corpus_identifier": "Mahadevan 287",
        "basis": "drawn form only (see recovery record)"}
    # Gate 0.3: the recovery record exists before any
    # identification wording is recorded anywhere else
    # and before any counting.
    _write_json(_OUT_A, recovery)

    # ── Gate 0.4 — corpus identified, exported, pinned ──
    corpus_path = _REPO / CORPUS_FILE
    if not corpus_path.exists():
        results["gate_0_4"] = {"verdict": "FAIL",
                               "reason": "corpus file absent"}
        return close(
            "CLOSED AT STEP 0",
            "CLOSED AT STEP 0 — CORPUS NOT PINNABLE",
            "Spec 055 closed before identification: the "
            "strict-corpus layer could not be identified "
            "and pinned. No identification was recorded "
            "and no statement about the sign is made. The "
            "recovery record carries the closure.")
    sequences: list[list[str]] = []
    record_ids: list[str] = []
    with corpus_path.open(encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("source_system") != "indusscript-m77":
                continue
            if rec.get("sign_id_scheme") != "Mahadevan1977":
                continue
            record_ids.append(rec["glossa_id"])
            sequences.append(
                _clean_tokens(rec.get("canonical_grapheme_ids")))
    with _OUT_D.open("w", encoding="utf-8") as fh:
        for rid, seq in zip(record_ids, sequences):
            fh.write(json.dumps(
                {"record_id": rid, "signs": seq},
                sort_keys=True) + "\n")
    export_sha = _sha256(_OUT_D)
    counts: Counter = Counter()
    for seq in sequences:
        counts.update(seq)
    target_count = counts.get(target_corpus_id, 0)
    results["gate_0_4"] = {
        "verdict": "PASS",
        "layer": (
            "the program's V3 / Mahadevan-lineage corpus "
            "as held in the database, in its held form: "
            "the records of the tracked primary corpus "
            "carrying source_system 'indusscript-m77' and "
            "sign scheme Mahadevan1977 (the executed "
            "Spec 033 precedent for this same layer; the "
            "V3 loader's own external Firestore export "
            "file is not present on disk, and CORPUS_"
            "VERSIONS.md records that the primary corpus "
            "already holds the same data in this form)"),
        "source_file": CORPUS_FILE,
        "source_file_sha256": _sha256(corpus_path),
        "export_file": (
            "specs/055-sign900-numeral/"
            "strict-corpus-export.jsonl"),
        "export_form": (
            "one JSON object per held record, in the "
            "source file's record order: {record_id, "
            "signs}, where signs is the record's "
            "canonical_grapheme_ids cleaned by the V3 "
            "loader's own rules (numeric Mahadevan ids "
            "only; '000'/'0' placeholders and '*'-prefixed "
            "supplementary tokens dropped), sequence "
            "order as stored"),
        "export_sha256": export_sha,
        "records_exported": len(sequences),
        "tokens_total": sum(counts.values()),
        "distinct_signs": len(counts),
        "target_corpus_identifier": "Mahadevan 287",
        "target_occurrences": target_count,
        "occurrence_floor": OCCURRENCE_FLOOR,
    }
    if target_count < OCCURRENCE_FLOOR:
        rep = ("not represented" if target_count == 0 else
               f"represented by {target_count} occurrences, "
               "below the frozen floor of 5")
        return close(
            "IDENTIFIED — TOO FEW OCCURRENCES TO TEST",
            "IDENTIFIED — TOO FEW OCCURRENCES TO TEST",
            "The sign that Fuls's paper numbers 900 is "
            "identified in Spec 055's recovery record as "
            "P154, and the fragment is thereby converted "
            "from a pointer into a claim. In the pinned "
            f"strict corpus the sign is {rep}, so the "
            "behaviour test cannot run as written. No "
            "measure was computed. The numeral question "
            "stands untested on this layer.")

    # ── Pre-counting record (spec 5.1; before any measure) ─
    by_id = {r["sign_id"]: r for r in rows}
    numeral_members = []
    numeral_ids: set[str] = set()
    for rid in STROKE_ROW_IDS:
        row = by_id[rid]
        assert _is_pure_stroke_description(row["description"]), (
            f"stroke-row description drift: {rid} "
            f"{row['description']}")
        for mid in [m.strip() for m in
                    row["mahadevan_ids"].split("|") if m.strip()]:
            token = str(int(mid[1:]))
            numeral_ids.add(token)
            numeral_members.append({
                "corpus_identifier": f"Mahadevan {token}",
                "registry_sign_id": rid,
                "wells_ids": row["wells_ids"],
                "drawn_description": row["description"],
                "published_source": (
                    "Fuls, 'Ancient Writing and Modern "
                    "Technologies', SPECIAL NUMERICAL "
                    "SIGNS: 'The numerical value of stroke "
                    "signs is most likely the number of "
                    "strokes' — the stroke signs are the "
                    "known numeral signs; this member is a "
                    "pure stroke group by its registry "
                    "drawn description")})
    hedged_members = []
    for h in HEDGED:
        wcell = f"W{int(h['source_sign_no']):03d}"
        row = next(
            r for r in rows
            if wcell in [t.strip() for t in
                         r["wells_ids"].split("|") if t.strip()])
        hedged_members.append({
            **h,
            "registry_sign_id": row["sign_id"],
            "corpus_identifier": (
                f"Mahadevan {int(row['mahadevan_ids'][1:])}"
                if row["mahadevan_ids"] else None),
            "status": ("EXCLUDED from the known-numeral "
                       "set under DD-055-14 (hedged "
                       "published identification)")})
    excluded = numeral_ids | {target_corpus_id}
    controls = _control_set(counts, target_count, excluded)
    # Dry-run (DD-055-16): the highest-count sign that is
    # neither the target nor a numeral-set member, ties by
    # corpus identifier ascending; machinery only.
    dry_sign = sorted(
        (s for s in counts if s not in excluded),
        key=lambda s: (-counts[s], int(s)))[0]
    dry_controls = _control_set(
        counts, counts[dry_sign], numeral_ids | {dry_sign})
    dry_numeral_ms = [
        _measures(sequences, s, numeral_ids)
        for s in sorted(numeral_ids, key=int)]
    dry_control_ms = [
        _measures(sequences, s, numeral_ids)
        for s in dry_controls]
    dry_run = {
        "sign": f"Mahadevan {dry_sign}",
        "occurrences": counts[dry_sign],
        "control_set": [f"Mahadevan {s}" for s in dry_controls],
        "measures": _measures(sequences, dry_sign, numeral_ids),
        "mapping": _classify(
            _measures(sequences, dry_sign, numeral_ids),
            dry_numeral_ms, dry_control_ms),
        "note": ("worked dry-run of the section 5 measures "
                 "and mapping on a non-target sign, as "
                 "DD-055-16 requires; it produces no "
                 "target quantity and no finding"),
    }
    pre_counting = {
        "known_numeral_set": {
            "rule": (
                "published identifications only: the "
                "source document's stroke-sign "
                "identification, entered through registry "
                "rows whose drawn description is a pure "
                "stroke group, crosswalked to Mahadevan "
                "corpus identifiers. The target sign is "
                "not a member (DD-055-3)."),
            "members": numeral_members,
            "corpus_identifiers": sorted(
                (f"Mahadevan {t}" for t in numeral_ids),
                key=lambda s: int(s.split()[1])),
        },
        "hedged_members_excluded": hedged_members,
        "target_census": {
            "corpus_identifier": "Mahadevan 287",
            "occurrences": target_count},
        "control_set": {
            "rule": (
                "the 10 ordinary signs (members of "
                "neither the numeral set nor the target) "
                "whose occurrence counts in the pinned "
                "layer are closest to the target's count, "
                "ties by corpus identifier ascending "
                "(DD-055-11)"),
            "members": [
                {"corpus_identifier": f"Mahadevan {s}",
                 "occurrences": counts[s]} for s in controls]},
        "dry_run": dry_run,
    }
    results["pre_counting"] = pre_counting

    # ── Step 2 — the three frozen measures ────────────────
    target_m = _measures(sequences, target_corpus_id, numeral_ids)
    numeral_ms = {s: _measures(sequences, s, numeral_ids)
                  for s in sorted(numeral_ids, key=int)}
    control_ms = {s: _measures(sequences, s, numeral_ids)
                  for s in controls}
    mapping = _classify(
        target_m, list(numeral_ms.values()),
        list(control_ms.values()))
    results["step2"] = {
        "target": {"corpus_identifier": "Mahadevan 287",
                   **target_m},
        "numeral_set": {
            f"Mahadevan {s}": m for s, m in numeral_ms.items()},
        "control_set": {
            f"Mahadevan {s}": m for s, m in control_ms.items()},
        "mapping": mapping,
    }
    outcome = mapping["outcome"]
    k_n = mapping["numeral_side_count"]
    k_o = mapping["control_side_count"]
    if outcome == "NUMERAL-LIKE":
        wording = (
            "The sign that Fuls's paper numbers 900 in "
            "the extended Wells (2011, 2015) sign list — "
            "matched by drawn form to P154 in Spec 055's "
            "recovery record — behaves as a numeral sign "
            "behaves in the pinned strict corpus: on "
            f"{k_n} of the three frozen measures it sits "
            "inside the known numeral signs' range and "
            "away from the frequency-matched ordinary "
            "signs' median (per-measure table in the "
            "run's results record). The recovered claim "
            "is checked on the numeral question: this "
            "sign is a numeral sign. This does not "
            "establish that its value is six; a "
            "distribution can support 'numeral', it "
            "cannot count.")
    elif outcome == "NOT NUMERAL-LIKE":
        wording = (
            "The sign that Fuls's paper numbers 900, "
            "identified in Spec 055's recovery record as "
            "P154, does not behave as a numeral sign "
            "behaves in the pinned strict corpus: on "
            f"{k_o} of the three frozen measures it sits "
            "inside the range of frequency-matched "
            "ordinary signs (per-measure table in the "
            "run's results record). The numeral reading "
            "the fragment carries is contradicted at the "
            "behaviour stage. The identification itself "
            "stands as recovered; what fails is the "
            "behaviour the reading predicts.")
    else:
        wording = (
            "The sign that Fuls's paper numbers 900, "
            "identified in Spec 055's recovery record as "
            "P154, splits the frozen measures in the "
            "pinned strict corpus (per-measure table in "
            "the run's results record): neither "
            "numeral-like nor ordinary-like on at least "
            "two. The numeral question is recorded as "
            "MIXED — the measures this design froze do "
            "not settle it, and no other measure may be "
            "substituted after the fact.")
    results["outcome"] = outcome
    results["headline_wording"] = wording
    results["fence"] = FENCE
    results["chain_sentence"] = CHAIN
    results["anchors"] = {
        "file": PINS["anchors"][0],
        "sha256_before": anchors_before,
        "sha256_after": _sha256(_REPO / PINS["anchors"][0]),
        "byte_identical": (
            anchors_before == _sha256(_REPO / PINS["anchors"][0])),
    }
    _write_json(_OUT_B, results)
    _OUT_C.write_text(_render_report(results, recovery),
                      encoding="utf-8")
    print(f"OUTCOME: {outcome} (numeral-side {k_n}, "
          f"control-side {k_o})", flush=True)
    return 0


def _render_report(r: dict, recovery: dict) -> str:
    outcome = r.get("outcome", "")
    wording = r.get("headline_wording", "")
    lines = [
        "# Phase-414 — Spec 055 sign-900 numeral test report",
        "",
        f"Executed {r['execution_date']} by {r['executor']}, "
        "under the frozen Spec 055 contract (freeze digest "
        f"`{r['freeze_digest']}`; OSF registration tbyqg, "
        "approved + public before the run).",
        "",
        "## Outcome",
        "",
        f"**{r.get('closure_class', outcome)}**",
        "",
        wording,
        "",
        r.get("fence", FENCE),
        "",
        r.get("chain_sentence", CHAIN),
        "",
        "## Identification (from the recovery record)",
        "",
        "Sign list named from the document's own text: "
        f"{recovery['sign_list_naming'].get('list_named')}",
        "",
    ]
    for s in recovery["sign_list_naming"]["naming_statements"]:
        lines.append(f"> \"{s['quote']}\" — {s['locator']}")
        lines.append("")
    ts = recovery["target_sign"]
    lines += [
        f"Target sign: source no. {ts['source_sign_no']}; "
        f"basis {ts['drawn_sign_match_basis']}; registry "
        f"id {ts['crosswalk_registry_id']}; named-list "
        f"locator {ts['named_list_locator']}.",
        "",
        "## Records",
        "",
        "- Recovery record: `specs/055-sign900-numeral/"
        "source-table-recovery.json` (schema "
        "glossa.source-table-recovery/1).",
        "- Results record: `reports/phase414_results.json`.",
    ]
    if "gate_0_4" in r:
        g = r["gate_0_4"]
        lines.append(
            f"- Corpus export: `{g['export_file']}` — "
            f"SHA-256 `{g['export_sha256']}` "
            f"({g['records_exported']} records, "
            f"{g['tokens_total']} tokens; target "
            f"{g['target_occurrences']} occurrences, "
            f"floor {g['occurrence_floor']}).")
    if "step2" in r:
        m = r["step2"]["mapping"]
        lines += ["", "## Per-measure table", "",
                  "| Measure | Target | Numeral range | "
                  "Control range | Numeral-side | "
                  "Control-side |",
                  "|---|---|---|---|---|---|"]
        for k, v in m["per_measure"].items():
            lines.append(
                f"| {k} | {v['target']} | "
                f"{v['numeral_range']} | "
                f"{v['control_range']} | "
                f"{v['numeral_side']} | {v['control_side']} |")
        lines += [
            "",
            f"Numeral-side {m['numeral_side_count']}, "
            f"control-side {m['control_side_count']} → "
            f"**{m['outcome']}** by the frozen section "
            "5.3 mapping alone.",
        ]
    lines += [
        "",
        "---",
        "",
        "*AI disclosure: executed by an AI agent (Muse "
        "Spark, via Muse) at the direction of Tristen "
        "Pierson, per constitution §VI.*",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
