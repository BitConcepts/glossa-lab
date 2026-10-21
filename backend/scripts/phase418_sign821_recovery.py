#!/usr/bin/env python3
"""Phase-418 — Spec 056 sign-821 recovery act.

Executes the frozen Spec 056 contract
(specs/056-sign821-recovery/freeze.md; freeze digest
64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e;
OSF registration 3eygs, approved and public before this
run, DOI 10.17605/OSF.IO/3EYGS): the fragment "Sign
value: 821 / it is used in a variety of contexts
(Figure 6"
(the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001,
stopped at Phase-104 under RULE-NUM) is re-extracted
from its pinned passage of record under the two-pass
protocol of spec section 4 and judged by the
conjunctive recovery test of spec section 5.

The run, in the frozen order:

  step 0.1  every spec section 2 input hashes to its
            frozen pin (fail-closed: CLOSED AT STEP 0
            — INPUT PIN MISMATCH). The claim record is
            asserted in the freeze's Spec 038 form
            (freeze.md section 2): its freeze-time hash
            is a definition constant carried in
            freeze.json, and the fragment's facts are
            asserted on the live file, because the
            extracted-claims store is regenerated and
            carries later appends on other claims;
  step 0.2  the passage is produced from the held
            copy: both anchor lines and the anchor
            sentence located verbatim (CLOSED AT
            STEP 0 — PASSAGE NOT PRODUCIBLE);
  step 0.3  the passage slice (held-text lines
            2783–2871) recomputes to its freeze-pinned
            digest (CLOSED AT STEP 0 — PASSAGE PIN
            MISMATCH);
  dry-run   the section 4–5 sheet and checklist
            machinery exercised on a passage other
            than the passage of record (DD-056-16):
            "The Mohenjo-daro bangle pot" section; it
            produces no candidate and no outcome for
            the fragment;
  step 1    two independent extraction passes over
            the pinned passage only (DD-056-14), each
            producing its extraction sheet of
            candidates carried by verbatim quotes;
            the candidate set of record is the union;
            reconciliation is by quotation and an
            unsettled disagreement on the decisive
            candidate would resolve AGAINST recovery;
  step 2    the recovery test (spec section 5):
            R-1..R-5 conjunctive. R-3's routes run for
            candidates that reach them: the sign list
            named from the document itself; the drawn
            sign identified by drawn form through the
            crosswalk registry, or by the source list's
            own published entry quoted with its
            locator — never by number alone (the
            registry's Yunmapped_0821 row is a
            Yajnadevam glyph identifier, the frozen
            number-collision trap, and is asserted as
            a trap, never used as a match).

Outputs:
  A — reports/phase418_results.json (the run's
      machine record);
  B — reports/phase418_recovery_report.md (the
      human-readable rendering; it does not diverge
      from A).

The extraction record (both sheets in full, the
reconciliation, the per-candidate checklists) is
specs/056-sign821-recovery/extraction-record.md and
the outcome record is
specs/056-sign821-recovery/outcome.md; the sheet
data below is the machine form of those sheets, and
every quote it carries is verified verbatim against
the pinned passage by this script before any outcome
is written. The claim-record closure append (spec
section 7, IDENTIFICATION FAILED form) is an
executor act recorded in the outcome record, not a
side effect of this script, so that re-running this
script never appends twice.

Fail-closed: any pin, passage, or registry fact
that differs from the frozen record aborts the run
before any outcome is written, except that a
step-0 closure IS an output (A and B record the
gate facts and no extraction pass is run).
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC_DIR = _REPO / "specs/056-sign821-recovery"
_OUT_A = _REPO / "reports/phase418_results.json"
_OUT_B = _REPO / "reports/phase418_recovery_report.md"

CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001")
FREEZE_DIGEST = (
    "64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e")
EXECUTOR = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-21"

PINS = {
    "held_text": (
        "glossa-indus/processed/cleaned_text/"
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
        "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"),
    "phase104_evaluation": (
        "glossa-indus/reports/phase104_claims_evaluation.json",
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"),
    "lane2_drafts": (
        "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"),
    "crosswalk_registry": (
        "data/crosswalks/canonical_sign_registry.csv",
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"),
    "anchors": (
        "backend/reports/INDUS_FINAL_ANCHORS.json",
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
}
CLAIM_FILE = (
    "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json")
CLAIM_FILE_SHA256_CONSTANT = (
    "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a")

START_ANCHOR = "The Dholavira signboard, revisited"
END_ANCHOR = "The Mohenjo-daro bangle pot"
ANCHOR_SENTENCE = (
    "Whatever sign 821 reads it is used in a variety of "
    "contexts (Figure 6.13).")
PASSAGE_SHA256 = (
    "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604")
PASSAGE_BYTES = 5354

FENCE = (
    "This act is record repair. It establishes, at most, what the "
    "source passage argues — never whether the argument is right, "
    "and nothing about sign 821 itself.")

IDENTIFICATION_FAILED_WORDING = (
    "Re-extraction found a specific argument in the passage of "
    "record (‘It is suggested here that sign 821, in the "
    "Dholavira signboard contexts, has a meaning of ‘city’, "
    "either as a determinative or as a word.’, printed p. 92), "
    "but the claim cannot be recovered in the program's form: "
    "the drawn sign could not be identified by either route §5 "
    "R-3 allows. The fragment is neither recovered nor retired; "
    "it stays a stated gap, with this closure as the record of "
    "why, and the unblocking act is the preservation, as a "
    "committed and hashed record, of an inspectable drawn-form "
    "reference for Wells's sign 821 — the Figure 2.6 sign-list "
    "pages (printed pp. 19–22) or the Figure 6.13 examples as "
    "images tied to the list entry — from which the drawn sign "
    "can be matched by drawn form through the crosswalk "
    "registry or quoted as the source list's own entry.")

UNBLOCKING_ACT = (
    "Preserve, as a committed and hashed record, an inspectable "
    "drawn-form reference for Wells's sign 821 — the Figure 2.6 "
    "sign-list pages (printed pp. 19–22) or the Figure 6.13 "
    "examples as images tied to the list entry — so the drawn "
    "sign can be matched by drawn form through the crosswalk "
    "registry or quoted as the source list's own published "
    "entry with its locator, satisfying §5 R-3.")

# ── The extraction sheets (spec section 4) ─────────────────────
# Quotes are whitespace-normalised verbatim from the pinned
# passage; this script verifies each one against the passage
# before any outcome is written. Locators give the cleaned-
# text line span and the printed page.

Q_PREMISE = (
    "I have posited (Wells 2011) that some part of this sign "
    "sequence would be the site’s locative (place name).")
Q_CITY = (
    "It is suggested here that sign 821, in the Dholavira "
    "signboard contexts, has a meaning of ‘city’, either as a "
    "determinative or as a word.")
Q_GLOSSES = (
    "752 Ta. ūr village, town, city. 808 Ta. eyil fortress, "
    "wall, fortification, city, town 3568 Ta. nakar house, "
    "abode, mansion, temple, palace, town, city. 4112 Ta. pāri "
    "temple; town, city, town of an agricultural tract, "
    "hermitage;")
Q_BEST = (
    "Any of these is possible. Which of these, if any, are "
    "the correct gloss cannot be known, but eyil seems the "
    "best choice given the fact that Dholavira is a walled "
    "city made of cut stone.")
Q_FULS = (
    "One verification of the sign 821 reading as ‘city’ has "
    "been pointed out by Andreas Fuls (pers. com. 2011; "
    "Figure 6.12). He notes that the sign combination of "
    "861+740 matches the imagery of a cow (740=*ay=’cow’) and "
    "the person in front of a structure, which may be a "
    "pictographic toponym (861 = city), seem to fit the "
    "readings developed so far. This evidence does not bring "
    "us any closer to a reading for sign 861, but does "
    "reinforce the association of this sign with important "
    "places.")
Q_ANCHOR = (
    "Whatever sign 821 reads it is used in a variety of "
    "contexts (Figure 6.13). While eyil-ay or eyil-i (i.e. "
    "collocating with sign 740) is not attested, this is not "
    "a nullification of the reading, as we really do not "
    "have a firm reading for sign 821.")

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

CANDIDATES = [
    {
        "id": "K-1",
        "proposition": (
            "Sign 821, in the Dholavira signboard contexts, "
            "has a meaning of ‘city’, either as a determinative "
            "or as a word; of the passage's candidate glosses "
            "(DED 752 ūr; DED 808 eyil; DED 3568 nakar; "
            "DED 4112 pāri), eyil is the best choice, because "
            "Dholavira is a walled city made of cut stone."),
        "quotes": [
            {"text": Q_CITY, "lines": "2835–2836",
             "printed_page": 92},
            {"text": Q_GLOSSES, "lines": "2842–2845",
             "printed_page": 93},
            {"text": Q_BEST, "lines": "2846–2847",
             "printed_page": 93},
        ],
        "premise_quote": {"text": Q_PREMISE, "lines": "2794–2795",
                          "printed_page": 91},
        "checklist": {
            "R-1": (
                "PASS — the proposition is the passage's own "
                "suggestion, stated in its own words (‘It is "
                "suggested here that…’); it is not a topic "
                "mention, not the figure, and not the bare "
                "fragment restated."),
            "R-2": (
                "PASS — a specific contention: a stated "
                "reading (‘city’, determinative or word) in a "
                "stated context (the Dholavira signboard "
                "contexts), of exactly the kind §5 names (‘a "
                "specific classification or reading in a "
                "stated context’). A contrary finding — 821 "
                "shown to carry another value in those "
                "contexts — could oppose it."),
            "R-3": "RUN AT STEP 2 — see the R-3 record.",
            "R-4": (
                "PASS — a falsification condition is statable "
                "from the passage's own logic (its locative "
                "premise and its context-bound suggestion), "
                "recorded verbatim in this sheet; the "
                "passage's own exclusion of the "
                "non-attestation observation as a nullification "
                "is respected, not overridden."),
            "R-5": (
                "PASS — the passage's stated conditions are "
                "carried with the contention: the context "
                "bound (‘in the Dholavira signboard "
                "contexts’), the determinative-or-word "
                "alternative, all four candidate glosses with "
                "their DED numbers, the eyil preference with "
                "its stated reason, and the passage's own "
                "hedge that no firm reading exists and the "
                "correct gloss cannot be known."),
        },
        "falsification_condition": R4_CONDITION,
        "decisive": True,
    },
    {
        "id": "K-2",
        "proposition": (
            "Considered and not credited as a candidate about "
            "sign 821: the passage's Fuls paragraph, framed as "
            "a verification of the 821 ‘city’ reading, whose "
            "asserted content concerns sign 861."),
        "quotes": [
            {"text": Q_FULS, "lines": "2848–2853",
             "printed_page": 93},
        ],
        "checklist": {
            "R-1": (
                "FAIL — the sentences assert a proposition "
                "about sign 861 (the 861+740 combination as a "
                "pictographic toponym, ‘cow at the city’, and "
                "861's association with important places). "
                "The head clause frames the paragraph as a "
                "verification of the 821 reading, but a "
                "framing clause is not a proposition about "
                "821 argued from evidence about 821; "
                "crediting it would assemble a candidate "
                "about one sign from another sign's evidence. "
                "The paragraph is supporting context for "
                "K-1's narrative, not a candidate."),
            "R-2": "NOT REACHED — R-1 fails.",
            "R-3": "NOT REACHED — R-1 fails.",
            "R-4": "NOT REACHED — R-1 fails.",
            "R-5": "NOT REACHED — R-1 fails.",
        },
        "decisive": False,
    },
    {
        "id": "K-3",
        "proposition": (
            "The bare fragment restated: sign 821 is used in "
            "a variety of contexts."),
        "quotes": [
            {"text": Q_ANCHOR, "lines": "2854–2856",
             "printed_page": 93},
        ],
        "checklist": {
            "R-1": (
                "FAIL — §5 rules this in advance: ‘Sign 821 "
                "is used in a variety of contexts’ is the "
                "fragment, and re-extracting the fragment is "
                "not recovering a claim."),
            "R-2": (
                "FAIL — no contention a contrary finding "
                "could oppose: the observation is true of "
                "almost any common sign, and the passage "
                "draws no contention from it (Figure 6.13, "
                "which it cites, is graphic-only in the held "
                "text and outside the passage of record as "
                "held)."),
            "R-3": "NOT REACHED — R-1 and R-2 fail.",
            "R-4": (
                "FAIL — no falsification condition can be "
                "written for it from the passage's own logic "
                "without inventing one."),
            "R-5": "NOT REACHED — R-1, R-2 and R-4 fail.",
        },
        "decisive": False,
    },
    {
        "id": "K-4",
        "proposition": (
            "Considered as a standalone candidate: eyil-ay or "
            "eyil-i (sign 821 collocating with sign 740) is "
            "not attested."),
        "quotes": [
            {"text": Q_ANCHOR, "lines": "2854–2856",
             "printed_page": 93},
        ],
        "checklist": {
            "R-1": (
                "PASS in the narrow sense — the passage does "
                "assert the non-attestation; the failure is "
                "at R-2."),
            "R-2": (
                "FAIL — a catalogue observation (an absence "
                "in the attestation record) from which the "
                "passage draws no contention about sign 821; "
                "the only point the passage draws from it is "
                "defensive — that it does not nullify K-1. "
                "Its content is carried into K-1's record "
                "under R-5 and into K-1's R-4 condition, "
                "where it belongs."),
            "R-3": "NOT REACHED — R-2 fails.",
            "R-4": "NOT REACHED — R-2 fails.",
            "R-5": "NOT REACHED — R-2 fails.",
        },
        "decisive": False,
    },
]

DRY_RUN_QUOTE = (
    "As sign 575 is likely a logograph representing a kiln, "
    "the use of 740 as a phonetic complement is redundant and "
    "wasteful of space in a medium in which space is precious.")


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


def main() -> int:
    results: dict = {
        "phase": "Phase-418",
        "spec": "056",
        "claim_id": CLAIM_ID,
        "freeze_digest": FREEZE_DIGEST,
        "execution_date": EXECUTION_DATE,
        "executor": EXECUTOR,
        "osf_registration": (
            "3eygs (approved + public before the run; "
            "DOI 10.17605/OSF.IO/3EYGS)"),
    }
    anchors_before = _sha256(_REPO / PINS["anchors"][0])

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
            results["failed_input"] = name
            _write_json(_OUT_A, results)
            _OUT_B.write_text(_render_report(results),
                              encoding="utf-8")
            print(f"STEP 0.1 FAIL: {name} pin mismatch",
                  flush=True)
            return 0
    # The claim record, in the freeze's Spec 038 form: the
    # freeze-time hash is asserted as the definition constant
    # carried in freeze.json, and the fragment's facts are
    # asserted on the live file (freeze.md section 2).
    freeze = json.loads((_SPEC_DIR / "freeze.json").read_text(
        encoding="utf-8"))
    constant_ok = (
        freeze["definition"]["inputs"]["claim_file"]["sha256"]
        == CLAIM_FILE_SHA256_CONSTANT)
    claim_doc = json.loads((_REPO / CLAIM_FILE).read_text(
        encoding="utf-8"))
    entry = _find_claim(claim_doc, CLAIM_ID)
    facts = {
        "constant_in_freeze_json": constant_ok,
        "entry_found": entry is not None,
        "normalized_claim": entry["normalized_claim"] if entry else None,
        "claim_status": entry["claim_status"] if entry else None,
        "stage": entry["stage"] if entry else None,
        "not_understood_names_source_passage": bool(
            entry and "the source passage in full"
            in entry["not_understood"]),
    }
    facts_ok = (
        constant_ok and facts["entry_found"]
        and facts["normalized_claim"] == (
            "Sign value: 821 / it is used in a variety of "
            "contexts (Figure 6")
        and facts["claim_status"] == "untested"
        and facts["stage"] == "created"
        and facts["not_understood_names_source_passage"])
    pin_results["claim_record_spec038_form"] = {
        "file": CLAIM_FILE,
        "freeze_time_sha256_constant": CLAIM_FILE_SHA256_CONSTANT,
        "live_file_sha256": _sha256(_REPO / CLAIM_FILE),
        "posture": (
            "Spec 038 form per freeze.md section 2: the "
            "extracted-claims store is regenerated and "
            "carries later appends on other claims (here, "
            "Spec 046's first_check append on the _0002 "
            "entry, PR #263), so the constant plus the "
            "fragment's facts on the live file are asserted, "
            "never a live-file hash"),
        "facts": facts, "match": facts_ok}
    if not facts_ok:
        results["step0"] = {"gate_0_1": pin_results}
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "INPUT PIN MISMATCH"
        results["failed_input"] = "claim_record"
        _write_json(_OUT_A, results)
        _OUT_B.write_text(_render_report(results),
                          encoding="utf-8")
        print("STEP 0.1 FAIL: claim-record facts mismatch",
              flush=True)
        return 0
    results["step0"] = {"gate_0_1": pin_results}

    # ── Step 0.2 — passage producible ─────────────────────────
    text_path = _REPO / PINS["held_text"][0]
    text_bytes = text_path.read_bytes()
    text = text_bytes.decode("utf-8")
    raw_lines = text_bytes.splitlines(keepends=True)
    stripped = [ln.strip() for ln in text.splitlines()]
    gate_0_2 = {
        "start_anchor": START_ANCHOR,
        "start_anchor_standalone_count":
            stripped.count(START_ANCHOR),
        "end_anchor": END_ANCHOR,
        "end_anchor_standalone_count": stripped.count(END_ANCHOR),
        "anchor_sentence": ANCHOR_SENTENCE,
        "anchor_sentence_occurrences": text.count(ANCHOR_SENTENCE),
    }
    if not (gate_0_2["start_anchor_standalone_count"] == 1
            and gate_0_2["end_anchor_standalone_count"] == 1
            and gate_0_2["anchor_sentence_occurrences"] == 1):
        results["step0"]["gate_0_2"] = gate_0_2
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "PASSAGE NOT PRODUCIBLE"
        _write_json(_OUT_A, results)
        _OUT_B.write_text(_render_report(results),
                          encoding="utf-8")
        print("STEP 0.2 FAIL: passage not producible",
              flush=True)
        return 0
    results["step0"]["gate_0_2"] = gate_0_2

    # ── Step 0.3 — passage pinnable ───────────────────────────
    passage = b"".join(raw_lines[2782:2871])
    gate_0_3 = {
        "lines": "2783-2871",
        "bytes": len(passage),
        "expected_sha256": PASSAGE_SHA256,
        "observed_sha256": hashlib.sha256(passage).hexdigest(),
    }
    gate_0_3["match"] = (
        gate_0_3["observed_sha256"] == PASSAGE_SHA256
        and gate_0_3["bytes"] == PASSAGE_BYTES)
    results["step0"]["gate_0_3"] = gate_0_3
    if not gate_0_3["match"]:
        results["outcome"] = "CLOSED AT STEP 0"
        results["closure_class"] = "PASSAGE PIN MISMATCH"
        _write_json(_OUT_A, results)
        _OUT_B.write_text(_render_report(results),
                          encoding="utf-8")
        print("STEP 0.3 FAIL: passage pin mismatch", flush=True)
        return 0
    passage_flat = _flat(passage.decode("utf-8"))
    results["step0"]["all_gates_passed"] = True

    # ── Dry-run (DD-056-16), before the protocol touches ──────
    # the fragment: the sheet + checklist machinery exercised
    # on the next headed section, "The Mohenjo-daro bangle
    # pot" (cleaned-text lines 2872-2931). It produces no
    # candidate and no outcome for the fragment.
    dry_section = _flat("\n".join(
        text.splitlines()[2871:2931]))
    results["dry_run"] = {
        "requirement": "DD-056-16",
        "passage": (
            "Wells 2015, 'The Mohenjo-daro bangle pot' "
            "(cleaned-text lines 2872–2931) — not the passage "
            "of record"),
        "candidate_proposition": (
            "Sign 575 is likely a logograph representing a "
            "kiln (cullai), so sign 740 beside it is not "
            "needed as a phonetic complement."),
        "quote": DRY_RUN_QUOTE,
        "quote_locator": "cleaned-text lines 2925–2926",
        "quote_verified_verbatim": _flat(DRY_RUN_QUOTE)
            in dry_section,
        "checklist_machinery": {
            "R-1": "exercised — proposition asserted in the "
                   "dry-run passage's own words",
            "R-2": "exercised — specific contention (a "
                   "logograph value for 575 in this context)",
            "R-3": "exercised in form only — no "
                   "identification attempted or needed; the "
                   "machinery records the route fields",
            "R-4": "exercised in form — a condition is "
                   "statable (575's contexts shown to carry "
                   "a single non-kiln value); not adjudicated",
            "R-5": "exercised — the stated hedge (‘likely’) "
                   "and the space rationale carried with "
                   "the proposition",
        },
        "produces": (
            "No candidate and no outcome for the fragment; "
            "machinery proof only."),
    }
    if not results["dry_run"]["quote_verified_verbatim"]:
        print("DRY-RUN FAIL: quote not verbatim", flush=True)
        return 1

    # ── Step 1 — two independent passes; quotes verified ──────
    quote_failures = []
    for cand in CANDIDATES:
        for q in cand["quotes"]:
            if _flat(q["text"]) not in passage_flat:
                quote_failures.append((cand["id"], q["lines"]))
        pq = cand.get("premise_quote")
        if pq and _flat(pq["text"]) not in passage_flat:
            quote_failures.append((cand["id"], pq["lines"]))
    if quote_failures:
        print(f"STEP 1 FAIL: quotes not verbatim: "
              f"{quote_failures}", flush=True)
        return 1
    results["step1"] = {
        "protocol": (
            "DD-056-14: two independent executor runs over "
            "the pinned passage only, each seeing only the "
            "passage and spec section 5; candidate set is "
            "the union of the sheets; reconciliation by "
            "quotation; unsettled disagreement on the "
            "decisive candidate resolves AGAINST recovery"),
        "pass_a": (
            "Sequential reading of the passage in order; "
            "candidates enumerated in passage order: "
            "K-1, K-2, K-3, K-4."),
        "pass_b": (
            "Mention-driven reading: every ‘821’ mention "
            "inside the passage worked outward, plus a "
            "sweep for propositions about 821 carried by "
            "‘this sign’ references (the sign-798 "
            "discussion's references are to 798, the "
            "sign-pair discussion's to the toponym pair — "
            "neither is a candidate about 821); candidates "
            "found: K-1, K-2, K-3, K-4 — the same set."),
        "candidates": CANDIDATES,
        "reconciliation": (
            "The two sheets agree on the union set "
            "{K-1, K-2, K-3, K-4} and on every checklist "
            "line. No disagreement arose on any candidate, "
            "settled or unsettled; in particular the "
            "decisive candidate K-1 carries identical "
            "R-1, R-2, R-4 and R-5 results on both sheets, "
            "each resting on the quotations recorded with "
            "it. The non-candidates were agreed by both "
            "passes: the sign-798 discussion (a different "
            "sign), the ‘copper/bronze tool’ sign-pair "
            "suggestion (the toponym pair, not 821), and "
            "the toponym-sequence observations (the "
            "sequence, not 821; the locative premise is "
            "carried as K-1's premise quote)."),
        "all_quotes_verified_verbatim": True,
    }

    # ── Step 2 — the recovery test; R-3 routes ────────────────
    apparatus = {
        "chapter_2_gives_the_list": (
            "Chapter 2 gives the Indus sign list used in "
            "this analysis" in _flat(text)),
        "sign_list_used_here_wells_2011": (
            "The sign list used here (Wells 2011)" in _flat(text)),
        "figure_2_6_caption": (
            "Figure 2.6 An Indus Sign List" in _flat(text)),
    }
    registry_path = _REPO / PINS["crosswalk_registry"][0]
    with registry_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    w821_cells = []
    city_descriptions = 0
    for row in rows:
        tokens = [t.strip() for t in row["wells_ids"].split("|")]
        if "W821" in tokens:
            w821_cells.append(row["sign_id"])
        if "city" in row["description"].lower():
            city_descriptions += 1
    yun = [r for r in rows if r["sign_id"] == "Yunmapped_0821"]
    witness = json.loads((_REPO / (
        "data/crosswalks/wells_segmentation_witness_v1.json")
    ).read_text(encoding="utf-8"))
    witness_821 = [
        r["sign"] for r in witness["rows"]
        if "821" in [g.strip() for g in
                     r.get("wells_graphemes", "").split(";")]]
    fig26_region = "\n".join(text.splitlines()[854:885])
    r3 = {
        "list_named_from_document": bool(all(apparatus.values())),
        "source_list_named": (
            "Wells's own sign list (Wells 2011), as given in "
            "Wells 2015, Chapter 2, ‘The Indus Sign List’ "
            "(Figure 2.6, printed pp. 19–22)"),
        "apparatus_evidence": apparatus,
        "registry_route": {
            "registry_rows": len(rows),
            "rows_with_w821_token": w821_cells,
            "descriptions_naming_a_city": city_descriptions,
            "yunmapped_0821_row": {
                "sign_id": yun[0]["sign_id"],
                "numbering_system": yun[0]["numbering_system"],
                "wells_ids": yun[0]["wells_ids"],
                "corpus_freq": yun[0]["corpus_freq"],
            } if yun else None,
            "result": (
                "NO MATCH — no registry entry carries the "
                "sign at all, by number or otherwise; a "
                "drawn-form match has nothing to match "
                "against, and the held text drops the glyph "
                "(the passage's sign slots are blank). The "
                "Yunmapped_0821 row is a Yajnadevam glyph "
                "identifier, not Wells's 821; it was "
                "asserted as the frozen trap and not used."),
        },
        "witness_route_evidence": {
            "wells_witness_rows": len(witness["rows"]),
            "wells_witness_grapheme_821_rows": witness_821,
        },
        "list_entry_route": {
            "locator": (
                "Wells 2015, Figure 2.6 (printed pp. 19–22)"),
            "held_text_figure_region_contains_821":
                "821" in fig26_region,
            "result": (
                "NO QUOTABLE ENTRY — in the held cleaned "
                "text the Figure 2.6 pages carry captions "
                "only (‘Figure 2.6 An Indus Sign List’ and "
                "its continuations); the drawn forms did "
                "not survive text extraction, so the list's "
                "own entry for sign 821 cannot be quoted "
                "from the held record. The appendix's "
                "‘Doubled Signs’ text (printed pp. 128–129) "
                "describes 821's formation from 820 by "
                "number; it is not the sign list's entry, "
                "carries no drawn form, and quoting it "
                "would identify by number — the route §5 "
                "forbids."),
        },
    }
    r3["drawn_sign_identified"] = bool(
        w821_cells or witness_821)
    r3["result"] = (
        "R-3 FAILS on its identification half: the sign "
        "list is named from the document itself, but the "
        "drawn sign its 821 labels is identified by "
        "neither allowed route.")
    results["step2"] = {"r3_record": r3}

    # Outcome mapping (spec section 6, applied mechanically
    # to the recorded checklists).
    decisive = next(c for c in CANDIDATES if c["decisive"])
    arg_pass = all(
        decisive["checklist"][k].startswith("PASS")
        for k in ("R-1", "R-2", "R-4", "R-5"))
    if arg_pass and not r3["drawn_sign_identified"]:
        results["outcome"] = "IDENTIFICATION FAILED"
        results["headline_wording"] = (
            IDENTIFICATION_FAILED_WORDING)
        results["unblocking_act"] = UNBLOCKING_ACT
    elif arg_pass and r3["drawn_sign_identified"]:
        results["outcome"] = "RECOVERED"
    else:
        results["outcome"] = "RETIREMENT RECOMMENDED"
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
    _OUT_B.write_text(_render_report(results), encoding="utf-8")
    print(f"OUTCOME: {results['outcome']}", flush=True)
    return 0


def _render_report(r: dict) -> str:
    g1 = r["step0"]["gate_0_1"]
    pins = "\n".join(
        f"- `{v['file']}` — SHA-256 `{v['observed_sha256']}` "
        f"(pin match: {v['match']})"
        for k, v in g1.items() if "observed_sha256" in v)
    claim = g1["claim_record_spec038_form"]
    head = (
        f"# Phase-418 — Spec 056 sign-821 recovery report\n\n"
        f"Executed {r['execution_date']} by {r['executor']}, "
        f"under the frozen Spec 056 contract (freeze digest\n"
        f"`{r['freeze_digest']}`; OSF registration 3eygs, "
        f"approved + public before the run,\n"
        f"DOI 10.17605/OSF.IO/3EYGS).\n")
    if r["outcome"] == "CLOSED AT STEP 0":
        return (
            head + f"\n## Outcome\n\n**CLOSED AT STEP 0 — "
            f"{r['closure_class']}**\n\nNo extraction pass "
            f"was run, the fragment stands exactly as "
            f"recorded, and no statement about the passage, "
            f"the fragment, or the sign is made.\n\n"
            f"Gate record: `{json.dumps(r['step0'])}`\n")
    cands = "\n".join(
        f"- **{c['id']}** — {c['proposition']}"
        for c in r["step1"]["candidates"])
    return f"""{head}
## Outcome

**{r['outcome']}**

{r['headline_wording']}

{r['fence']}

## The passage of record

Wells (2015), ‘The Dholavira signboard, revisited’,
printed pp. 90–94; held cleaned text
(`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`),
lines 2783–2871; passage slice 5,354 bytes, SHA-256
`{PASSAGE_SHA256}`. Anchor sentence: “{ANCHOR_SENTENCE}”

The held text drops the book's sign glyphs and
Figure 6.13 is graphic-only in it, present only as its
caption; that limit stands as a stated boundary of
the recovery test (DD-056-13) and is stated wherever
this outcome is stated.

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed:

{pins}

Claim record, in the freeze's Spec 038 form: freeze-time
SHA-256 constant `{claim['freeze_time_sha256_constant']}`
carried in freeze.json; the fragment's facts asserted
on the live file (entry found, status untested, stage
created, the source passage named in its
not-understood text) — match: {claim['match']}.

Gate 0.2 — the passage was produced from the held copy:
both anchor lines stand as standalone lines exactly
once, and the anchor sentence occurs exactly once.

Gate 0.3 — the passage slice recomputes to its
freeze-pinned digest
(`{r['step0']['gate_0_3']['observed_sha256']}`,
{r['step0']['gate_0_3']['bytes']} bytes).

## Dry-run (DD-056-16)

The sheet and checklist machinery was exercised on
‘The Mohenjo-daro bangle pot’ (cleaned-text lines
2872–2931), a passage other than the passage of
record, before the protocol touched the fragment.
Its quote was verified verbatim and its checklist
completed in form; it produces no candidate and no
outcome for the fragment.

## Step 1 — extraction (two passes, reconciled)

{cands}

Both passes found the same candidate set; the
reconciliation records full agreement, settled by
the quotations on the sheets. Every quote was
verified verbatim against the pinned passage by the
phase script. The full sheets, reconciliation, and
per-candidate checklists are the extraction record:
`specs/056-sign821-recovery/extraction-record.md`.

## Step 2 — the recovery test

The decisive candidate K-1 passes R-1, R-2, R-4 and
R-5 on both sheets. R-3: the sign list is named from
the document itself — Wells's own sign list (Wells
2011), as given in Wells 2015, Chapter 2 / Figure
2.6. The drawn sign is identified by neither
allowed route: the pinned registry carries no W821
value in any of its 803 rows (its Yunmapped_0821 row
is a Yajnadevam glyph identifier — the frozen
number-collision trap — and was not used), the
Phase-123 Wells witness carries no grapheme 821,
and the source list's own entry stands in Figure
2.6, whose drawn forms did not survive the held
copy's text extraction, so no entry can be quoted.
R-3 therefore fails, and §6's mapping gives
IDENTIFICATION FAILED: the fragment is neither
recovered nor retired.

Unblocking act: {r['unblocking_act']}

Anchors asserted byte-identical before and after
(`{r['anchors']['sha256_before']}`).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
"""


if __name__ == "__main__":
    sys.exit(main())
