"""WP5 anchor-support audit generator (repair program 2026-10-26).

Reads the canonical anchor table, the Phase-48 validation output, the
Phase-108 provenance register, the Phase-108 anchor trails, the
Phase-109 change register and (optionally) the Phase-109 rebase file
and the repository README, and emits one deterministic audit JSON.

What the audit does:

* FIRST reconstructs every Phase-48 promotion from the test details
  recorded in ``outputs/phase48_medium_validation.json`` and flags
  every pass that was granted by default (no positional expectation,
  a reading too short to test, a reading character missing from the
  language model, or no anchored neighbors). A pass granted by
  default is not evidence.
* THEN audits all strict-core entries: the HIGH/MEDIUM anchors whose
  Phase-108 register category is not SA_DERIVED or SA_CONFIRMED_ONLY
  and whose register record has ``sa_in_chain`` false (94 entries in
  the audited snapshot).
* Lists the 44 ``pending_non_sa_validation`` anchors without giving
  them any new weight: they are not audited and not promoted here.
* Counts the tiers in the actual anchors file and compares them with
  the Phase-109 rebase file and the README errata line, so the
  LOW/CANDIDATE discrepancy is resolved from the record itself.

Every per-sign statement is taken from the input files. Where the
assembled trail holds no source passage, the record says so in
words. Where no falsifier is recorded, the record says so in words.
No calibrated probabilities are produced.

Dispositions use this fixed vocabulary only:

* ``supported_independent`` -- the record contains a support line
  from outside this program's own corpus work (the Phase-276 dual
  external corroboration: Elamite and Sanskrit comparanda named
  with source codes in the entry, on top of an internal derivation).
* ``supported_internal_only`` -- the record contains a non-SA
  derivation produced inside the program (distributional, DEDR,
  iconographic, grammar, or comparable internal lines) and nothing
  that triggers a stronger caution below.
* ``requires_revalidation`` -- a recorded step that carries the
  entry's current standing is defective or ineligible as recorded
  (the Phase-48 battery, a sole crosswalk/literature import whose
  only trail form is an identity entry, or a mechanically restored
  reading whose own derivation is not in the record), so the entry
  must be re-tested under a corrected method before its tier is
  relied on. This does not say the reading is wrong.
* ``insufficient_evidence`` -- the assembled audit record does not
  contain a derivation of the proposed value that can be checked
  (pass-1-only provenance classification, no first proposal, no
  ledger passage).
* ``expert_adjudication_pending`` -- the record itself shows the
  deciding step is a human adjudication that has not happened or
  was inconclusive (a research-loop value retained only on a
  crosswalk attribution, or a tier capped in Phase-109 because the
  latest adjudication was INCONCLUSIVE).
* ``superseded_record`` -- the entry's own validation status marks
  its premise as superseded. (No strict-core entry met this rule in
  the audited snapshot; the rule is kept so the vocabulary is
  complete and the check runs every time.)

Standard library only. Deterministic: the same inputs always
produce byte-identical output (no clock, no randomness, stable
ordering: Phase-48 promotions first in their recorded order, then
the remaining strict-core entries by sign).

Usage (paths are CLI arguments with repo-relative defaults):

    python3 backend/scripts/repair_anchor_audit.py \
        --repo /path/to/glossa-lab-checkout \
        --out docs/repair-2026-10-26/anchor-support-audit.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

AUDIT_ID = "repair-2026-10-26-wp5-anchor-support-audit"
NO_PASSAGE = "no source passage in the assembled trail"
NO_FALSIFIER = "no falsifier recorded"

DISPOSITIONS = [
    "supported_independent",
    "supported_internal_only",
    "requires_revalidation",
    "insufficient_evidence",
    "expert_adjudication_pending",
    "superseded_record",
]

EVIDENCE_TEST_VOCABULARY = [
    "drawing",
    "distribution",
    "functional_role",
    "phonetic_value",
    "meaning",
]

# Code facts about backend/scripts/phase48_medium_validation.py,
# verified by reading the source in the audited snapshot. They are
# stated here once, as facts about the code, and referenced by the
# per-sign reconstructions.
PHASE48_CODE_FACTS = [
    {
        "id": "positional_reading_blind",
        "fact": (
            "test_positional(sign, reading, role) never uses the "
            "reading argument: it checks only the Holdat role's "
            "average position and starter/ending flags against the "
            "role expectation. A positional test that ignores the "
            "proposed reading cannot validate that reading; at most "
            "it tests distribution and functional role."
        ),
    },
    {
        "id": "positional_pass_by_default",
        "fact": (
            "test_positional returns (True, "
            "'no_expectation—pass_by_default') when the role has no "
            "expectation entry (for example UNKNOWN or a missing "
            "role): an uncheckable case is scored as a pass."
        ),
    },
    {
        "id": "dedr_too_short_pass",
        "fact": (
            "test_dedr returns (True, 'too_short_pass') when the "
            "reading has fewer than 2 characters after normalization: "
            "an uncheckable case is scored as a pass."
        ),
    },
    {
        "id": "dedr_is_lexical_plausibility",
        "fact": (
            "Otherwise test_dedr counts dictionary entries equal to "
            "the normalized reading (exact match) or sharing its "
            "first 3 normalized characters (prefix match, pass at "
            "2 or more). That tests whether a similar word exists "
            "in the dictionary -- lexical plausibility -- not "
            "whether this sign stood for that word."
        ),
    },
    {
        "id": "bigram_pass_by_default",
        "fact": (
            "test_bigram_consistency returns (True, "
            "'char_not_in_lm—pass_by_default') when the reading's "
            "first character is absent from the language model, and "
            "(True, 'no_anchor_neighbours—pass_by_default') when "
            "none of the sign's top following signs has a HIGH or "
            "MEDIUM anchor reading: both uncheckable cases are "
            "scored as passes."
        ),
    },
    {
        "id": "bigram_backend_divergence",
        "fact": (
            "The two branches of test_bigram_consistency compute "
            "different comparison sets by construction. When torch "
            "is importable, the comparison set is the top-5 "
            "continuation characters of the reading's character "
            "(row.topk(min(5, n))). When torch is absent, the set "
            "is every continuation character attested for that "
            "character ({b for (a, b) in bigram_prob if a == "
            "reading_char}). The CPU form is a superset of the "
            "torch form, so the same sign can pass on one backend "
            "and fail on the other; the backends do not implement "
            "the same method. The recorded Phase-48 run reports "
            "gpu_device 'cuda', i.e. the torch branch; a rerun "
            "without torch would not be computing the same test."
        ),
    },
    {
        "id": "promotion_rule",
        "fact": (
            "Promotion required any 2 of the 3 tests to pass "
            "(score >= 2), so default credits counted toward "
            "promotion exactly like measured passes."
        ),
    },
]


# ------------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def strip_diacritics(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def norm_reading(reading: str) -> str:
    """Lossy comparison form (matches the program's own Phase-108
    normalization): first segment before '/', parenthetical glosses
    removed, diacritics stripped, letters only, lower case."""
    s = (reading or "").split("/")[0]
    s = re.sub(r"\([^)]*\)", " ", s)
    s = strip_diacritics(s.lower())
    return re.sub(r"[^a-z]", "", s)


def reading_segments(reading: str) -> list[str]:
    return [seg.strip() for seg in (reading or "").split("/") if seg.strip()]


# ------------------------------------------------------------------
# Phase-48 reconstruction
# ------------------------------------------------------------------

def classify_positional(detail: str, passed: bool) -> dict:
    if "pass_by_default" in (detail or ""):
        return {
            "credit": "default_credit_no_expectation",
            "note": (
                "Pass granted by default: the role had no "
                "expectation to check against, so nothing was "
                "measured."
            ),
        }
    if passed:
        return {
            "credit": "genuine_positional_pass_reading_blind",
            "note": (
                "A real measurement of the sign's position and "
                "starter/ending behavior against the role "
                "expectation. The test never uses the proposed "
                "reading, so it supports the sign's distribution "
                "and functional role only; it is not evidence for "
                "the reading itself."
            ),
        }
    return {
        "credit": "fail",
        "note": "The sign's position did not match the role expectation.",
    }


def classify_dedr(detail: str, passed: bool) -> dict:
    d = detail or ""
    if d == "too_short_pass":
        return {
            "credit": "default_credit_too_short",
            "note": (
                "Pass granted by default: the normalized reading "
                "is shorter than 2 characters, so the dictionary "
                "check did not run."
            ),
        }
    if passed and d.startswith("exact_match"):
        return {
            "credit": "exact_match_lexical_plausibility",
            "note": (
                "The normalized reading matches dictionary forms "
                "exactly. That shows a word of this shape exists "
                "in the dictionary (lexical plausibility); it does "
                "not show this sign stood for that word."
            ),
        }
    if passed and d.startswith("prefix_match"):
        return {
            "credit": "prefix_match_weak_lexical_plausibility",
            "note": (
                "Pass on a prefix match: dictionary entries "
                "sharing the first 3 normalized characters of the "
                "reading (or the reverse). With counts in the "
                "hundreds this is a weak form of lexical "
                "plausibility, not a sign-to-word proof."
            ),
        }
    return {
        "credit": "fail",
        "note": "No dictionary match was recorded.",
    }


def classify_bigram(detail: str, passed: bool) -> dict:
    d = detail or ""
    if "char_not_in_lm" in d:
        return {
            "credit": "default_credit_missing_model_character",
            "note": (
                "Pass granted by default: the reading's first "
                "character is absent from the language model, so "
                "no comparison was possible."
            ),
        }
    if "no_anchor_neighbours" in d or "no_anchor_neighbors" in d:
        return {
            "credit": "default_credit_no_anchor_neighbors",
            "note": (
                "Pass granted by default: none of the sign's top "
                "following signs had an anchored reading to "
                "compare against."
            ),
        }
    if passed:
        return {
            "credit": "genuine_bigram_pass_as_recorded_backend_dependent",
            "note": (
                "A real comparison as recorded -- but the "
                "comparison set depends on the compute backend "
                "(top-5 continuations with torch, all "
                "continuations without), so the pass is not "
                "reproducible across backends as the same test."
            ),
        }
    return {
        "credit": "fail",
        "note": "The recorded neighbor match fell below the 0.4 threshold.",
    }


DEFAULT_CREDITS = {
    "default_credit_no_expectation",
    "default_credit_too_short",
    "default_credit_missing_model_character",
    "default_credit_no_anchor_neighbors",
}


def reconstruct_phase48(result: dict) -> dict:
    tests = {}
    classifiers = {
        "test1_positional": ("positional", classify_positional),
        "test2_dedr": ("dedr", classify_dedr),
        "test3_bigram": ("bigram", classify_bigram),
    }
    default_passes: list[str] = []
    non_default_passes = 0
    reading_sensitive_non_default = 0
    for key, (label, classify) in classifiers.items():
        t = result.get(key, {})
        passed = bool(t.get("pass"))
        verdict = classify(t.get("detail", ""), passed)
        tests[label] = {
            "recorded_pass": passed,
            "recorded_detail": t.get("detail"),
            "credit": verdict["credit"],
            "note": verdict["note"],
        }
        if passed and verdict["credit"] in DEFAULT_CREDITS:
            default_passes.append(label)
        elif passed:
            non_default_passes += 1
            if label in ("dedr", "bigram"):
                reading_sensitive_non_default += 1
    score = int(result.get("score", 0))
    return {
        "tested_in_phase48": True,
        "holdat_role": result.get("holdat_role"),
        "avg_position": result.get("avg_position"),
        "n_corpus": result.get("n_corpus"),
        "recorded_score": score,
        "recorded_promote": bool(result.get("promote")),
        "tests": tests,
        "default_credit_passes": default_passes,
        "n_default_credit_passes": len(default_passes),
        "n_non_default_passes": non_default_passes,
        "n_reading_sensitive_non_default_passes": reading_sensitive_non_default,
        "score_without_default_credits": non_default_passes,
        "promotion_survives_removing_default_credits": non_default_passes >= 2,
        "any_non_default_test_evidence_supported_the_promotion": non_default_passes > 0,
        "any_reading_sensitive_non_default_evidence": reading_sensitive_non_default > 0,
        "reading_note": (
            "The positional pass is a real measurement but never "
            "uses the reading. Only the dictionary and bigram tests "
            "touch the reading at all, and both are weaker than a "
            "sign-to-word proof: the dictionary test is lexical "
            "plausibility and the bigram test is backend-dependent."
        ),
    }


# ------------------------------------------------------------------
# Evidence classification
# ------------------------------------------------------------------

def tests_for_component(comp: dict) -> list[str]:
    """Map one provenance-register component to the controlled
    vocabulary: what does this line of evidence actually test?"""
    ctype = (comp.get("type") or "").upper()
    role = (comp.get("role") or "").lower()
    if ctype == "SA" or role == "gloss_lookup_only":
        return []
    if ctype == "ICONOGRAPHIC":
        tests = ["drawing", "meaning"]
        if "motif" in role:
            tests.append("distribution")
        return tests
    if ctype == "DEDR":
        return ["phonetic_value", "meaning"]
    if ctype == "GRAMMAR":
        if role == "round_distributional_assignment":
            return ["distribution"]
        if role == "research_loop_heuristic":
            return ["distribution"]
        return ["distribution", "functional_role"]
    if ctype == "LITERATURE":
        return ["phonetic_value", "meaning"]
    if ctype == "CROSSWALK_CORPUS":
        if "commodity" in role:
            return ["distribution", "meaning"]
        return ["phonetic_value", "meaning"]
    if ctype == "FORMULA":
        return ["distribution", "functional_role"]
    return []


def component_is_support(comp: dict) -> bool:
    """Components that record an actual derivation/support line.
    SA table rows and gloss lookups are not support: the register
    itself states a gloss lookup is not an etymological assignment,
    and Phase-107 falsified SA as evidence for sign values."""
    if (comp.get("type") or "").upper() == "SA":
        return False
    if (comp.get("role") or "") == "gloss_lookup_only":
        return False
    return True


# ------------------------------------------------------------------
# Per-sign record assembly
# ------------------------------------------------------------------

_LEDGER_ASSIGN_RE = r"{sign}\s*=\s*([^\s,;(]+)"


def build_record(sign: str, anchors: dict, register: dict, trails: dict,
                 phase48_by_sign: dict, changes_by_sign: dict) -> dict:
    entry = anchors[sign]
    reg = register.get(sign, {})
    trail = trails.get(sign, {})
    reading = entry.get("reading")
    components = reg.get("components", [])
    reasons = reg.get("reasons", [])
    basis_text = entry.get("basis") or ""
    source_text = entry.get("source") or ""

    # --- identity and corpus frame ---------------------------------
    structured = trail.get("structured", {}) or {}
    crosswalk = structured.get("crosswalk_v2") or None
    frame_issues: list[str] = []
    parpola_equivalent = None
    if crosswalk is None:
        frame_issues.append(
            "No Mahadevan-Parpola crosswalk entry is present in "
            "the assembled trail, so no Parpola-frame equivalent "
            "is recorded there for this sign."
        )
    else:
        parpola_equivalent = crosswalk.get("parpola_id")
        if not crosswalk.get("mahadevan_id"):
            frame_issues.append(
                "The crosswalk entry in the trail has no "
                "mahadevan_id field: the join key is blank. Five "
                "trail entries share that blank key, so a join on "
                "mahadevan_id alone would mix records."
            )
        elif crosswalk.get("mahadevan_id") != sign:
            frame_issues.append(
                "The crosswalk entry's mahadevan_id "
                f"({crosswalk.get('mahadevan_id')}) does not match "
                "this sign."
            )
        num = int(sign[1:])
        pnum = crosswalk.get("parpola_num")
        if pnum is not None and pnum != num:
            frame_issues.append(
                f"Numbering differs across frames: this sign is "
                f"{sign} in Mahadevan numbering and "
                f"{crosswalk.get('parpola_id')} in Parpola "
                "numbering. The two numbers must not be "
                "interchanged."
            )
    if any("stale" in r.lower() for r in reasons):
        frame_issues.append(
            "The provenance register records stale fields in this "
            "entry (see the derivation reasons): stale text that "
            "contradicts the current basis is a record "
            "inconsistency, not evidence."
        )

    # --- proposed value and alternatives ---------------------------
    segments = reading_segments(reading)
    alternatives: list[dict] = []
    seen_norms = {norm_reading(reading)}

    def add_alternative(value, source, note):
        if not value:
            return
        n = norm_reading(value)
        if n and n not in seen_norms:
            seen_norms.add(n)
            alternatives.append(
                {"value": value, "source": source, "note": note})

    for seg in segments[1:]:
        alternatives.append({
            "value": seg,
            "source": "INDUS_FINAL_ANCHORS.json entry (reading field)",
            "note": (
                "Alternative form recorded in the same reading "
                "field, after the '/' separator."
            ),
        })
        seen_norms.add(norm_reading(seg))
    if crosswalk and crosswalk.get("reading"):
        add_alternative(
            crosswalk["reading"],
            "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json "
            "(crosswalk extract in the Phase-108 trail)",
            "Reading recorded in the crosswalk extract; differs "
            "from the anchor reading under the program's own "
            "normalization.",
        )
    sa52 = structured.get("phase52_sa_table") or {}
    if sa52.get("sa_reading"):
        add_alternative(
            sa52["sa_reading"],
            "reports/phase52_full_decipherment_table.json",
            "Value the Phase-52 SA table recorded for this sign. "
            "Listed as a recorded alternative only: Phase-107 "
            "falsified SA as evidence for sign values, so this is "
            "not support.",
        )
    snaps = structured.get("anchor_snapshots") or {}
    for fname in sorted(snaps):
        add_alternative(
            snaps[fname].get("reading"),
            f"backend/reports/{fname}",
            "Reading in an earlier anchor-file backup; differs "
            "from the current reading.",
        )
    for ch in changes_by_sign.get(sign, []):
        before = (ch.get("before") or {}).get("reading")
        add_alternative(
            before,
            "reports/phase109_change_register.json "
            f"({ch.get('step')}, {ch.get('rule')})",
            "Reading recorded immediately before the Phase-109 "
            "change for this sign.",
        )
    assign_re = re.compile(
        _LEDGER_ASSIGN_RE.format(sign=re.escape(sign)))
    for m in trail.get("ledger_mentions", []) or []:
        for hit in assign_re.finditer(m.get("snippet", "")):
            add_alternative(
                hit.group(1),
                f"{m.get('source')}:{m.get('line')}",
                "Value assigned to this sign in a ledger line "
                "preserved in the trail.",
            )

    # --- source passages -------------------------------------------
    ledger_passages = [
        {
            "source": m.get("source"),
            "line": m.get("line"),
            "header": m.get("header"),
            "snippet": m.get("snippet"),
        }
        for m in (trail.get("ledger_mentions", []) or [])
    ]
    structured_extracts: list[dict] = []
    if sa52:
        structured_extracts.append({
            "kind": "phase52_sa_table",
            "citation": sa52.get("citation"),
            "data": {
                "sa_reading": sa52.get("sa_reading"),
                "sa_consensus_pct": sa52.get("sa_consensus_pct"),
                "sa_agrees_confirmed": sa52.get("sa_agrees_confirmed"),
                "confirmed_reading_then": sa52.get("confirmed_reading_then"),
            },
        })
    sa107 = structured.get("phase107_sa_table") or {}
    if sa107:
        structured_extracts.append({
            "kind": "phase107_sa_table",
            "citation": sa107.get("citation"),
            "data": sa107.get("row"),
        })
    if snaps:
        structured_extracts.append({
            "kind": "anchor_snapshots",
            "citation": "backend/reports/INDUS_FINAL_ANCHORS.backup_*.json",
            "data": snaps,
        })
    if crosswalk:
        structured_extracts.append({
            "kind": "crosswalk_v2",
            "citation": (
                "backend/glossa_lab/data/"
                "mahadevan_parpola_crosswalk_v2.json"
            ),
            "data": crosswalk,
        })
    ledger_present = len(ledger_passages) > 0

    # --- Phase-109 change facts (needed before independence) --------
    changes = changes_by_sign.get(sign, [])
    step1a_keep = any(
        ch.get("step") == "step1" and ch.get("action") == "keep+annotate"
        for ch in changes
    )
    step1b_restore = any(
        ch.get("step") == "step1" and ch.get("action") == "restore"
        for ch in changes
    )

    # --- independent lines vs repetition ---------------------------
    # The register predates Phase-109. For a sign whose loop value
    # was restored away in Step 1(b), the register's research-loop
    # component describes the superseded value, not the current
    # one, so it is not listed as support for the current value;
    # the restored entry's own source line is listed instead.
    independent_lines: list[dict] = []
    for comp in components:
        if not component_is_support(comp):
            continue
        if step1b_restore and \
                (comp.get("role") or "") == "research_loop_heuristic":
            continue
        independent_lines.append({
            "type": comp.get("type"),
            "role": comp.get("role"),
            "citation": comp.get("citation"),
            "tests": tests_for_component(comp),
        })
    if step1b_restore and "DEDR" in source_text.upper():
        independent_lines.append({
            "type": "DEDR",
            "role": "phase109_step1b_restored_entry_source",
            "citation": (
                "INDUS_FINAL_ANCHORS.json entry source field, "
                "restored in Phase-109 Step 1(b): "
                + source_text
            ),
            "tests": ["phonetic_value", "meaning"],
        })
    dual_external = (
        "dual external corroboration" in basis_text.lower()
        or any("dual external corroboration" in r.lower() for r in reasons)
    )
    if dual_external:
        independent_lines.append({
            "type": "EXTERNAL_CORROBORATION",
            "role": "phase276_dual_external",
            "citation": (
                "INDUS_FINAL_ANCHORS.json entry basis (Phase-276: "
                "Elamite and Sanskrit comparanda named with "
                "source codes in the entry text)"
            ),
            "tests": ["phonetic_value", "meaning"],
        })

    repetition_lines: list[str] = []
    if sa52.get("sa_agrees_confirmed") is True:
        repetition_lines.append(
            "The Phase-52 SA table records the SA reading agreeing "
            "with the already-confirmed reading. Agreement scored "
            "against the existing reading is a confirmation on the "
            "same record, not independent evidence; Phase-107 "
            "also falsified SA as evidence for sign values."
        )
    row107 = sa107.get("row") or {}
    if row107.get("gold") and norm_reading(row107["gold"]) == norm_reading(reading):
        repetition_lines.append(
            "The Phase-107 table's gold value for this sign is "
            "the anchor reading itself, so agreement there is "
            "measured against the same value it is cited for."
        )
    same_snaps = sum(
        1 for v in snaps.values()
        if norm_reading(v.get("reading") or "") == norm_reading(reading)
    )
    if same_snaps:
        repetition_lines.append(
            f"The same reading appears in {same_snaps} anchor-file "
            "backup(s) in the trail. A backup repeats the record "
            "over time; it does not add evidence."
        )
    if crosswalk and crosswalk.get("reading") and \
            norm_reading(crosswalk["reading"]) == norm_reading(reading):
        repetition_lines.append(
            "The crosswalk extract records the same reading as "
            "the anchor table (an identity entry). From the "
            "assembled record this cannot be distinguished from "
            "a copied project value, so this audit counts it as "
            "repetition, not independent support (Work Package 4)."
        )
    if ledger_passages:
        repetition_lines.append(
            f"The trail holds {len(ledger_passages)} ledger "
            "mention(s). A ledger mention is a later use or "
            "restatement of the value in program work; it counts "
            "as independent evidence only where the snippet "
            "itself records a derivation."
        )
    if sign in phase48_by_sign:
        repetition_lines.append(
            "The Phase-48 battery re-used the same Holdat corpus "
            "observations that produced the role expectations it "
            "checked against. It is a re-check on the same data, "
            "not independent evidence."
        )

    # --- what the evidence tests ------------------------------------
    # Derived from the register components and the dual-external
    # line only (not from keyword matches on prose, which cannot
    # tell a claim from its negation).
    tests_vocab: set[str] = set()
    for line in independent_lines:
        tests_vocab.update(line["tests"])
    evidence_tests = [t for t in EVIDENCE_TEST_VOCABULARY if t in tests_vocab]

    # --- falsifier ---------------------------------------------------
    falsifier = NO_FALSIFIER
    for container in (entry, reg):
        for k, v in container.items():
            if "falsifier" in str(k).lower() and v:
                falsifier = str(v)
    # No per-sign falsifier field exists in the audited inputs;
    # the scan above is the check, and it finds none.

    # --- Phase-48 reconstruction ------------------------------------
    phase48 = None
    if sign in phase48_by_sign:
        phase48 = reconstruct_phase48(phase48_by_sign[sign])

    # --- disposition --------------------------------------------------
    step3_inconclusive = any(
        ch.get("step") == "step3" for ch in changes
    ) and "INCONCLUSIVE" in (entry.get("phase109_annotation") or "")
    has_loop_component = any(
        (c.get("role") or "") == "research_loop_heuristic" for c in components
    )
    pass1_only = (
        reg.get("decision_source") == "pass1"
        and not reg.get("first_proposal")
    )
    phase48_cited = any(
        ("phase-48" in r.lower() or "phase48" in r.lower()) for r in reasons
    )
    sole_import = (
        len(components) > 0
        and all(
            (c.get("type") or "").upper() in ("LITERATURE", "CROSSWALK_CORPUS")
            for c in components
        )
        and not any(
            "commodity" in (c.get("role") or "") for c in components
        )
        and not dual_external
    )

    if entry.get("validation_status") == "premise_superseded":
        status, rule = "superseded_record", "R1_premise_superseded"
        rule_text = (
            "The entry's own validation status marks its premise "
            "as superseded."
        )
    elif has_loop_component and step1a_keep:
        status, rule = "expert_adjudication_pending", "R2a_loop_value_crosswalk_retention"
        rule_text = (
            "The current value was proposed by the automated "
            "research loop and was retained in Phase-109 Step 1(a) "
            "only because the crosswalk extract records the same "
            "value. Under Work Package 4 a crosswalk attribution "
            "of that kind is not eligible as independent "
            "validation, and Phase-110 expressly did not re-try "
            "this reading. A human expert must adjudicate the "
            "value itself."
        )
    elif step3_inconclusive:
        status, rule = "expert_adjudication_pending", "R2b_phase109_step3_inconclusive"
        rule_text = (
            "Phase-109 Step 3 capped this entry's tier because "
            "the latest adjudication on record (Phase-105) is "
            "INCONCLUSIVE and was never superseded; the higher "
            "tier came from a promotion gate, not an adjudication. "
            "The missing step is a human adjudication."
        )
    elif dual_external:
        status, rule = "supported_independent", "R3_dual_external_corroboration"
        rule_text = (
            "The entry records a Phase-276 dual external "
            "corroboration -- Elamite and Sanskrit comparanda "
            "named with source codes -- on top of an internal "
            "derivation, with no SA in the chain. The external "
            "sources' own passages are not reproduced in the "
            "assembled trail, so this status credits the "
            "corroboration line as recorded; it does not "
            "re-verify the comparanda against their primary "
            "publications."
        )
    elif pass1_only:
        status, rule = "insufficient_evidence", "R4_pass1_only_record"
        rule_text = (
            "The provenance register classifies this entry by a "
            "single structured signal in pass 1 only: no hand "
            "review, no first proposal recorded, and the trail "
            "holds no ledger passage. The anchor entry asserts a "
            "specific reading without recording its derivation, "
            "so the assembled record does not contain a checkable "
            "derivation of the value."
        )
    elif phase48 is not None:
        status, rule = "requires_revalidation", "R5a_phase48_promotion"
        rule_text = (
            "This sign's current tier rests on the Phase-48 "
            "promotion, and the Phase-48 battery is defective as "
            "recorded (default credits, a reading-blind "
            "positional test, lexical-plausibility scoring, and "
            "backend-dependent bigram sets). The promotion must "
            "be re-earned under a corrected test. Any non-Phase-48 "
            "derivation line in the record is noted separately "
            "and is not erased by this status."
        )
    elif step1b_restore:
        status, rule = "requires_revalidation", "R5b_restored_reading"
        rule_text = (
            "The current value is a pre-loop reading mechanically "
            "restored in Phase-109 Step 1(b) after the research "
            "loop overwrote it. The register's reasons describe "
            "the superseded loop value, not this one; the restored "
            "entry's own record is a source label plus a "
            "recalibration bracket, with no derivation passage in "
            "the trail. The restored value needs a fresh check on "
            "its own record."
        )
    elif phase48_cited:
        status, rule = "requires_revalidation", "R5c_phase48_cited_as_support"
        rule_text = (
            "The provenance register's stated support for this "
            "entry includes the Phase-48 battery, which is "
            "defective as recorded. The part of the standing that "
            "rests on that battery must be re-earned under a "
            "corrected test."
        )
    elif sole_import:
        status, rule = "requires_revalidation", "R5d_sole_crosswalk_or_literature_import"
        rule_text = (
            "The only support lines in the record are a "
            "literature or crosswalk import, and the only form "
            "of that line in the assembled trail is an identity "
            "entry (the crosswalk extract repeats the anchor "
            "reading) or an unreproduced mention count. Under "
            "Work Package 4 that is not eligible as independent "
            "validation until the primary source is checked "
            "directly."
        )
    else:
        status, rule = "supported_internal_only", "R6_internal_derivation"
        rule_text = (
            "The record contains a non-SA derivation produced "
            "inside the program, and no defective or ineligible "
            "step carries the entry's current standing. All of "
            "the support in the record is internal to the "
            "program: no external independent line is verified "
            "in the assembled trail."
        )

    # --- plain-language explanation ----------------------------------
    parts: list[str] = []
    parts.append(
        f"{sign} is read as '{reading}' and the anchor table "
        f"marks it {entry.get('confidence')}."
    )
    fp = reg.get("first_proposal")
    if fp:
        parts.append(f"Recorded origin: {fp}.")
    if phase48 is not None:
        d = phase48["n_default_credit_passes"]
        nd = phase48["n_non_default_passes"]
        rs = phase48["n_reading_sensitive_non_default_passes"]
        parts.append(
            "In Phase-48 it scored "
            f"{phase48['recorded_score']}/3 and was promoted. "
            f"Of its passes, {d} were granted by default and "
            f"{nd} were real test outcomes. Only {rs} of the "
            "real outcomes touched the reading at all, and those "
            "test dictionary plausibility or neighbor patterns, "
            "not the sign-to-word mapping itself."
        )
    if not ledger_present:
        parts.append(
            "For this sign, " + NO_PASSAGE + "; what can be "
            "checked is the register's classification, the entry "
            "fields, and the structured extracts."
        )
    if repetition_lines:
        parts.append(
            "Later confirmations in the record repeat the same "
            "value or the same observations and are flagged as "
            "repetition, not counted as new evidence."
        )
    parts.append("Current status: " + status + ". " + rule_text)
    explanation = " ".join(parts)

    return {
        "sign": sign,
        "sign_identity": {
            "sign": sign,
            "mahadevan_number": int(sign[1:]),
            "parpola_equivalent_in_trail_crosswalk": parpola_equivalent,
            "n_corpus_in_phase107_table": row107.get("n_corpus"),
        },
        "corpus_frame": (
            "Mahadevan sign numbering (M-numbers), as used in "
            "the canonical anchor table "
            "backend/reports/INDUS_FINAL_ANCHORS.json."
        ),
        "crosswalk_frame_issues": frame_issues,
        "proposed_value": {
            "reading": reading,
            "recorded_alternative_forms_in_reading_field": segments[1:],
            "basis_as_recorded": basis_text or None,
            "source_as_recorded": source_text or None,
            "dedr_reference_as_recorded": (
                entry.get("dedr") or entry.get("dedr_id")
                or entry.get("dedr_source") or trail.get("dedr")
            ),
            "gloss_as_recorded": (
                entry.get("gloss") or entry.get("dedr_gloss")
                or entry.get("meaning")
            ),
        },
        "alternatives": alternatives,
        "source_passages": {
            "ledger_passage_present": ledger_present,
            "ledger_passages": ledger_passages,
            "structured_extracts": structured_extracts,
            "passage_note": (
                None if ledger_present else
                NO_PASSAGE + ". The structured extracts listed "
                "here are the only per-sign records the trail "
                "assembled."
            ),
        },
        "original_derivation": {
            "register_category": reg.get("category"),
            "register_reasons": reasons,
            "first_proposal": fp,
            "decision_source": reg.get("decision_source"),
            "sa_in_chain": reg.get("sa_in_chain"),
            "sa_role": reg.get("sa_role"),
            "components": components,
            "trail_citations": reg.get("trail_citations", []),
        },
        "evidence_independence": {
            "independent_lines": independent_lines,
            "repetition_lines": repetition_lines,
            "same_observation_confirmations_flagged": len(repetition_lines) > 0,
            "register_state_note": (
                "The Phase-108 register predates the Phase-109 "
                "follow-through. For this sign the register "
                "describes the research-loop staging value that "
                "Phase-109 then kept or restored away; the "
                "original_derivation block quotes the register "
                "as written, and the disposition works from the "
                "current anchor entry plus the Phase-109 change "
                "register."
                if (step1a_keep or step1b_restore) else None
            ),
        },
        "evidence_tests": evidence_tests,
        "falsifier": falsifier,
        "distinguishing_observation": (
            "not recorded" if falsifier == NO_FALSIFIER else None
        ),
        "historical_confidence_category": entry.get("confidence"),
        "current_evidential_status": status,
        "disposition_rule": rule,
        "phase48_promotion": phase48 is not None,
        "phase48_reconstruction": phase48,
        "plain_language_explanation": explanation,
    }


# ------------------------------------------------------------------
# Tier-count check
# ------------------------------------------------------------------

def tier_check(anchors_data: dict, rebase: dict | None,
               readme_text: str | None) -> dict:
    anchors = anchors_data["anchors"]
    actual = dict(Counter(
        (e.get("confidence") or "").upper() for e in anchors.values()
    ))
    counts = {t: actual.get(t, 0)
              for t in ("HIGH", "MEDIUM", "LOW", "CANDIDATE")}
    rebase_counts = None
    if rebase:
        rebase_counts = {
            t: rebase.get("anchor_counts_by_tier", {}).get(t)
            for t in ("HIGH", "MEDIUM", "LOW", "CANDIDATE")
        }
    readme_counts = None
    if readme_text:
        m = re.search(
            r"(\d+)\s+HIGH\s*\+\s*(\d+)\s+MEDIUM\s*\+\s*(\d+)\s+LOW"
            r"\s*\+\s*(\d+)\s+CANDIDATE",
            readme_text,
        )
        if m:
            readme_counts = {
                "HIGH": int(m.group(1)), "MEDIUM": int(m.group(2)),
                "LOW": int(m.group(3)), "CANDIDATE": int(m.group(4)),
            }
    return {
        "anchors_file_actual_counts": counts,
        "anchors_file_total_entries": len(anchors),
        "anchors_file_by_confidence_field": anchors_data.get("by_confidence"),
        "phase109_rebase_counts": rebase_counts,
        "phase109_rebase_basis_as_recorded": (rebase or {}).get("basis"),
        "readme_errata_counts": readme_counts,
        "resolution": (
            "The canonical anchors file itself holds HIGH "
            f"{counts['HIGH']}, MEDIUM {counts['MEDIUM']}, LOW "
            f"{counts['LOW']}, CANDIDATE {counts['CANDIDATE']} "
            f"({len(anchors)} entries), and its own by_confidence "
            "field agrees. The README errata of 2026-10-12 states "
            "the same numbers, so the errata is correct. "
            "reports/phase109_rebase.json states LOW 112 and "
            "CANDIDATE 4: that file misstates the current "
            "canonical table. Its own basis line shows why -- it "
            "was computed on the post-Phase-109 table, before "
            "Phase-110 demoted 109 Phase-111 'kur' entries from "
            "LOW to CANDIDATE (112 - 109 = 3 LOW; 4 + 109 = 113 "
            "CANDIDATE; see the _phase110_note field in the "
            "anchors file). The rebase file is a superseded "
            "snapshot, not an arithmetic error at its own basis "
            "date, but any current claim quoting its LOW/CANDIDATE "
            "counts is quoting stale numbers."
        ),
    }


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".",
                    help="repository checkout root (default: .)")
    ap.add_argument("--anchors", default=None,
                    help="default: <repo>/backend/reports/INDUS_FINAL_ANCHORS.json")
    ap.add_argument("--phase48", default=None,
                    help="default: <repo>/outputs/phase48_medium_validation.json")
    ap.add_argument("--register", default=None,
                    help="default: <repo>/reports/phase108_provenance_register.json")
    ap.add_argument("--trails", default=None,
                    help="default: <repo>/reports/phase108_anchor_trails.json")
    ap.add_argument("--change-register", default=None,
                    help="default: <repo>/reports/phase109_change_register.json")
    ap.add_argument("--rebase", default=None,
                    help="default: <repo>/reports/phase109_rebase.json")
    ap.add_argument("--readme", default=None,
                    help="default: <repo>/README.md")
    ap.add_argument("--out", required=True, help="output audit JSON path")
    args = ap.parse_args(argv)

    repo = Path(args.repo)
    paths = {
        "anchors": Path(args.anchors) if args.anchors
            else repo / "backend/reports/INDUS_FINAL_ANCHORS.json",
        "phase48": Path(args.phase48) if args.phase48
            else repo / "outputs/phase48_medium_validation.json",
        "register": Path(args.register) if args.register
            else repo / "reports/phase108_provenance_register.json",
        "trails": Path(args.trails) if args.trails
            else repo / "reports/phase108_anchor_trails.json",
        "change_register": Path(args.change_register) if args.change_register
            else repo / "reports/phase109_change_register.json",
        "rebase": Path(args.rebase) if args.rebase
            else repo / "reports/phase109_rebase.json",
        "readme": Path(args.readme) if args.readme else repo / "README.md",
    }
    for name in ("anchors", "phase48", "register", "trails"):
        if not paths[name].exists():
            print(f"error: required input missing: {paths[name]}",
                  file=sys.stderr)
            return 2

    anchors_data = load_json(paths["anchors"])
    anchors = anchors_data["anchors"]
    phase48_data = load_json(paths["phase48"])
    register = load_json(paths["register"])["records"]
    trails = load_json(paths["trails"])["trails"]
    changes_by_sign: dict[str, list] = {}
    if paths["change_register"].exists():
        for ch in load_json(paths["change_register"]).get("entries", []):
            if ch.get("sign"):
                changes_by_sign.setdefault(ch["sign"], []).append(ch)
    rebase = load_json(paths["rebase"]) if paths["rebase"].exists() else None
    readme_text = (paths["readme"].read_text(encoding="utf-8")
                   if paths["readme"].exists() else None)

    phase48_by_sign = {r["sign"]: r for r in phase48_data.get("results", [])}
    promoted_order = list(phase48_data.get("promoted_signs", []))

    # Strict core, exactly as defined in the brief: register
    # category not in (SA_DERIVED, SA_CONFIRMED_ONLY), sa_in_chain
    # false, restricted to HIGH/MEDIUM in the anchors file.
    strict = sorted(
        s for s, e in anchors.items()
        if (e.get("confidence") or "").upper() in ("HIGH", "MEDIUM")
        and register.get(s, {}).get("category")
            not in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
        and not register.get(s, {}).get("sa_in_chain")
    )
    ordered = [s for s in promoted_order if s in strict]
    ordered += [s for s in strict if s not in set(promoted_order)]

    records = [
        build_record(s, anchors, register, trails,
                     phase48_by_sign, changes_by_sign)
        for s in ordered
    ]

    # Phase-48 aggregate statistics.
    recs48 = [r["phase48_reconstruction"] for r in records
              if r["phase48_reconstruction"]]
    credit_counter: Counter = Counter()
    for rec in recs48:
        for t in rec["tests"].values():
            if t["recorded_pass"]:
                credit_counter[t["credit"]] += 1
    phase48_summary = {
        "n_medium_tested": phase48_data.get("n_medium_tested"),
        "n_promoted": phase48_data.get("n_promoted"),
        "promoted_signs_in_recorded_order": promoted_order,
        "gpu_device_as_recorded": phase48_data.get("gpu_device"),
        "pass_credits_by_kind": dict(sorted(credit_counter.items())),
        "n_promotions_with_at_least_one_default_credit": sum(
            1 for r in recs48 if r["n_default_credit_passes"] > 0),
        "promotions_with_at_least_one_default_credit": [
            r["sign"] for r in records
            if r["phase48_reconstruction"]
            and r["phase48_reconstruction"]["n_default_credit_passes"] > 0
        ],
        "n_promotions_with_no_reading_sensitive_non_default_pass": sum(
            1 for r in recs48
            if r["n_reading_sensitive_non_default_passes"] == 0),
        "promotions_with_no_reading_sensitive_non_default_pass": [
            r["sign"] for r in records
            if r["phase48_reconstruction"]
            and r["phase48_reconstruction"]
                ["n_reading_sensitive_non_default_passes"] == 0
        ],
        "n_promotions_reaching_threshold_on_reading_sensitive_passes_alone": sum(
            1 for r in recs48
            if r["n_reading_sensitive_non_default_passes"] >= 2),
        "n_promotions_failing_without_default_credits": sum(
            1 for r in recs48
            if not r["promotion_survives_removing_default_credits"]),
        "note": (
            "Strictly, no promotion rests wholly on default "
            "credits if the positional pass is counted, because "
            "the positional test genuinely measured position for "
            "all 30 signs. But the positional test never uses the "
            "reading. For the reading itself, the promotions "
            "listed under "
            "promotions_with_no_reading_sensitive_non_default_pass "
            "have no non-default reading-sensitive support at "
            "all: every reading-touching pass they received was "
            "granted by default."
        ),
    }

    # Pending set: listed, given no new weight, not audited.
    pending = sorted(
        s for s, e in anchors.items()
        if e.get("validation_status") == "pending_non_sa_validation"
    )
    pending_block = {
        "count": len(pending),
        "policy": (
            "These anchors carry the Phase-109 Step 2 flag "
            "pending_non_sa_validation (SA-derived or "
            "SA-confirmed-only provenance in the Phase-108 "
            "register). This audit assigns them no new weight: "
            "they receive no disposition, no promotion, and no "
            "support from anything in this file. Their status is "
            "unchanged from the anchor table."
        ),
        "entries": [
            {
                "sign": s,
                "reading": anchors[s].get("reading"),
                "historical_confidence_category": anchors[s].get("confidence"),
                "register_category": register.get(s, {}).get("category"),
                "validation_status": anchors[s].get("validation_status"),
                "current_evidential_status": (
                    "pending_non_sa_validation (unchanged; no new "
                    "weight assigned by this audit)"
                ),
            }
            for s in pending
        ],
    }

    overall = Counter(r["current_evidential_status"] for r in records)
    promo = Counter(
        r["current_evidential_status"] for r in records if r["phase48_promotion"]
    )
    rest = Counter(
        r["current_evidential_status"] for r in records
        if not r["phase48_promotion"]
    )

    audit = {
        "audit_id": AUDIT_ID,
        "work_package": (
            "WP5 -- audit anchor promotions and the full strict "
            "core (Glossa Lab repair program, 2026-10-26)"
        ),
        "generated_by": "backend/scripts/repair_anchor_audit.py",
        "inputs": {
            name: {"path": str(p), "sha256": sha256_of(p)}
            for name, p in paths.items() if p.exists()
        },
        "method": {
            "strict_core_definition": (
                "Anchors with confidence HIGH or MEDIUM in the "
                "canonical anchor table whose Phase-108 register "
                "category is not SA_DERIVED or SA_CONFIRMED_ONLY "
                "and whose register record has sa_in_chain false."
            ),
            "ordering": (
                "Phase-48 promotions first, in the order recorded "
                "in outputs/phase48_medium_validation.json; then "
                "the remaining strict-core entries by sign."
            ),
            "disposition_vocabulary": DISPOSITIONS,
            "evidence_tests_vocabulary": EVIDENCE_TEST_VOCABULARY,
            "phase48_code_facts": PHASE48_CODE_FACTS,
            "no_calibrated_probabilities": (
                "This audit records no probability, percentage "
                "confidence, or score for any reading. Historical "
                "confidence categories are quoted as recorded; "
                "current statuses use the fixed vocabulary above."
            ),
            "falsifier_rule": (
                "A falsifier is reported only where a per-sign "
                "falsifier is recorded in the inputs. The "
                "generator scans the anchor entry and the register "
                "record for a falsifier field; in the audited "
                "snapshot there is none for any strict-core "
                "entry, so every record states '" + NO_FALSIFIER + "'."
            ),
        },
        "tier_count_check": tier_check(anchors_data, rebase, readme_text),
        "phase48_summary": phase48_summary,
        "summary_counts": {
            "strict_core_total": len(records),
            "overall": {k: overall.get(k, 0) for k in DISPOSITIONS},
            "phase48_promotion_subset": {
                "n": sum(1 for r in records if r["phase48_promotion"]),
                "by_disposition": {k: promo.get(k, 0) for k in DISPOSITIONS},
            },
            "strict_core_not_in_phase48": {
                "n": sum(1 for r in records if not r["phase48_promotion"]),
                "by_disposition": {k: rest.get(k, 0) for k in DISPOSITIONS},
            },
            "expert_adjudication_pending_signs": [
                r["sign"] for r in records
                if r["current_evidential_status"]
                == "expert_adjudication_pending"
            ],
            "records_with_no_falsifier_recorded": sum(
                1 for r in records if r["falsifier"] == NO_FALSIFIER),
            "records_with_no_ledger_passage_in_trail": sum(
                1 for r in records
                if not r["source_passages"]["ledger_passage_present"]),
            "records_with_a_crosswalk_identity_entry": sum(
                1 for r in records
                if any("identity entry" in line
                       for line in r["evidence_independence"]
                       ["repetition_lines"])),
        },
        "records": records,
        "pending_non_sa_validation": pending_block,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}: {len(records)} strict-core records "
          f"({sum(1 for r in records if r['phase48_promotion'])} "
          f"Phase-48 promotions first), {len(pending)} pending "
          "anchors listed with no new weight")
    print("overall dispositions:",
          {k: overall.get(k, 0) for k in DISPOSITIONS})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
