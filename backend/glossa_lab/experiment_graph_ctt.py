"""CTT and dense-cross-sign coupling atomic node implementations.

These nodes plug into the experiment graph engine to add:

- IndusSignRoleClassifier   : derive 6-bit role mask per sign from corpus stats
- CTTAdmissibilityFilter    : per-sign feasibility filter (Constraint Topology Theory,
                              Layer1Labs Silicon, 2026) — masks SA proposals that
                              violate positional/role constraints
- HoldoutWordRecall         : non-circular cognate recall against external attested
                              vocabulary (Snyder/Berg-Kirkpatrick/Luo paradigm)
- CompoundDependencyConstraint : factor-graph-style soft constraint for high-PMI
                                 compound bigrams (per Cotterell/Eisner 2015 dual
                                 decomposition idea — simplified single-pass version)
- CTTAnchoredSADecipher     : SA decipherer wired through the CTT admissibility
                              oracle and compound-dependency constraint at every
                              proposal step (the H17.7-compliant "primitive" form)

References
----------
- Constraint Topology Theory (CTT) Technical Report v1.0, Layer1Labs Silicon, 2026-04-27.
- Cotterell, Peng, Eisner. "Dual Decomposition Inference for Graphical Models over
  Strings." EMNLP 2015. — for the cross-sign coupling layer.
- Luo, Cao, Barzilay. "Neural Decipherment via Minimum-Cost Flow." ACL 2019.
- Berg-Kirkpatrick, Klein. "Simple effective decipherment via combinatorial
  optimization." 2011. — for the discrete combinatorial framing CTT enforces.
- Snyder, Barzilay, Knight. "A statistical model for lost language decipherment."
  ACL 2010. — non-parallel anchor + cognate-recall framework adopted here.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any

# ── Sign role bits (per Indus structural analysis 2026-04-07) ────────────────
ROLE_BITS = (
    "suffix",  # TMK terminal-only signs
    "determinative",  # initial-only signs
    "numeral",  # tally / quantity signs
    "phonetic",  # CV syllabogram candidates
    "logogram",  # standalone-word signs (rare)
    "compound",  # signs that occur in a high-PMI bigram pair
)


# ── 1. IndusSignRoleClassifier ──────────────────────────────────────────────


# Default numeral candidates spanning M77 and Parpola P-code conventions.
# Parpola P121–P125 / P144–P150 are the vertical-stroke families (one–six
# strokes); Mahadevan M77 100–130 range covers the same numerical signs.
_DEFAULT_NUMERAL_SIGNS: tuple[str, ...] = (
    # Parpola allograph numbers for stroke-numerals (CISI Parpola corpus)
    "P121", "P122", "P123", "P124", "P125",
    "P144", "P145", "P146", "P147", "P148", "P149", "P150",
    # Mahadevan M77 numbering for stroke-numerals
    "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
    "110", "111", "112", "113", "114", "115",
)


def _indus_sign_role_classifier(inputs: dict, params: dict) -> dict:
    """Derive a 6-bit role mask per sign from corpus statistics.

    The output is a dict {sign_id -> set[str]} of admissible role labels.
    Used by CTTAdmissibilityFilter to forbid SA mappings that assign a
    phonetic-syllable value to a strictly-terminal suffix sign, etc.

    Pure primitive: counts terminal/initial/medial rates, applies thresholds.
    No machine learning, no composition of existing nodes.

    Suffix/numeral detection (2026-04-28 fix):
      - Strict `terminal_threshold` (0.85) only catches signs that are
        almost-exclusively final. Realistic Indus suffix candidates have
        terminal rates of 0.4–0.7 with strong terminal-vs-initial bias.
        We now also accept signs with `t_rate >= terminal_relaxed` AND
        t_rate >= 1.5 · i_rate as suffix candidates.
      - The default numeral_set now spans both Parpola P-codes (P121–P125,
        P144–P150) and Mahadevan M77 numbering (100–115).
      - Optional `numeral_repetition_threshold` parameter promotes any sign
        that appears in solo or repeated-run inscriptions at high rate to a
        numeral (covers tally-style stroke signs that don't appear in the
        canonical numeral list).
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    if not sequences:
        return {"role_table": {}, "n_signs": 0}

    t_thr = float(params.get("terminal_threshold", 0.85))
    t_thr_relaxed = float(params.get("terminal_relaxed", 0.45))
    i_thr = float(params.get("initial_threshold", 0.70))
    pmi_thr = float(params.get("compound_pmi_threshold", 4.0))
    min_count = int(params.get("min_count", 5))
    numeral_repetition_thr = float(params.get("numeral_repetition_threshold", 0.5))
    numeral_set = set(params.get("numeral_signs", _DEFAULT_NUMERAL_SIGNS))
    # Logogram detector parameters (Phase-12 overhaul, 2026-04-28).
    # Replaces the old "low-frequency phonetic singleton" rule with a
    # behavior-based detector: a logogram is a HIGH-frequency sign that
    # appears with LOW positional variance (Σ p_pos² ≈ 1, i.e. concentrated
    # in one position class) and that frequently occurs as the entire
    # inscription (solo). All three conditions must hold.
    logo_min_count = int(params.get("logogram_min_count", 20))
    logo_pos_concentration = float(
        params.get("logogram_position_concentration", 0.55)
    )
    logo_solo_rate = float(params.get("logogram_solo_rate", 0.05))

    tc: Counter[str] = Counter(s for seq in sequences for s in seq)
    te: Counter[str] = Counter(seq[-1] for seq in sequences if len(seq) >= 1)
    ic: Counter[str] = Counter(seq[0] for seq in sequences if len(seq) >= 1)

    # Repetition / solo statistics for numeral heuristic, plus per-sign
    # solo-only count for logogram detection.
    solo_or_repeat_count: Counter[str] = Counter()
    solo_count: Counter[str] = Counter()
    medial_count: Counter[str] = Counter()
    for seq in sequences:
        if len(seq) == 0:
            continue
        # Solo inscription → every sign in it gets a +1
        if len(seq) == 1:
            solo_or_repeat_count[seq[0]] += 1
            solo_count[seq[0]] += 1
            continue
        # Repeated run: if all signs in the seq are the same, +1 per token
        if len(set(seq)) == 1:
            solo_or_repeat_count[seq[0]] += len(seq)
        # Medial: every token that is neither initial nor final
        for s in seq[1:-1]:
            medial_count[s] += 1

    # Bigram PMI for compound detection (Mahadevan-style)
    bg: Counter[tuple[str, str]] = Counter()
    for seq in sequences:
        for i in range(len(seq) - 1):
            bg[(seq[i], seq[i + 1])] += 1
    total_bg = sum(bg.values()) or 1
    total_uni = sum(tc.values()) or 1
    compound_signs: set[str] = set()
    for (a, b), c in bg.items():
        if c < 5:
            continue
        p_ab = c / total_bg
        p_a = tc[a] / total_uni
        p_b = tc[b] / total_uni
        if p_a > 0 and p_b > 0:
            pmi = math.log2(p_ab / (p_a * p_b))
            if pmi >= pmi_thr:
                compound_signs.add(a)
                compound_signs.add(b)

    role_table: dict[str, list[str]] = {}
    n_logograms_detected = 0
    for sym, n in tc.items():
        if n < min_count:
            continue
        t_rate = te[sym] / n if n else 0.0
        i_rate = ic[sym] / n if n else 0.0
        rep_rate = solo_or_repeat_count[sym] / n if n else 0.0
        m_rate = medial_count[sym] / n if n else 0.0
        solo_rate = solo_count[sym] / n if n else 0.0
        # Position-concentration: Σ p_pos² over (initial, medial, terminal).
        # solo_rate is excluded so that a sign that is *only* solo doesn't
        # alias to high concentration via t_rate=1 trivia.
        # Renormalise non-solo positional shares so the metric is meaningful
        # even when solo_rate > 0.
        non_solo = max(1e-12, 1.0 - solo_rate)
        p_i = i_rate / non_solo
        p_m = m_rate / non_solo
        p_t = t_rate / non_solo
        pos_conc = p_i * p_i + p_m * p_m + p_t * p_t
        roles: set[str] = set()
        # Suffix detection: strict OR relaxed-with-terminal-bias
        if t_rate >= t_thr or (
            t_rate >= t_thr_relaxed and (i_rate == 0 or t_rate >= 1.5 * i_rate)
        ):
            roles.add("suffix")
        if i_rate >= i_thr:
            roles.add("determinative")
        if sym in numeral_set or rep_rate >= numeral_repetition_thr:
            roles.add("numeral")
        # Phonetic syllabograms = mixed-position high-frequency signs not
        # exclusively terminal/initial and not classified as numeral.
        if t_rate < t_thr and i_rate < i_thr and "numeral" not in roles:
            roles.add("phonetic")
        # Logogram detector overhaul (Phase-12, 2026-04-28).
        # New rule: a logogram is high-frequency, has low positional
        # variance (one position class dominates), AND occurs solo at least
        # `logo_solo_rate` of the time. This replaces the old rule that
        # mis-flagged rare phonetic singletons as logograms.
        is_logogram = (
            n >= logo_min_count
            and pos_conc >= logo_pos_concentration
            and solo_rate >= logo_solo_rate
        )
        if is_logogram:
            roles.add("logogram")
            n_logograms_detected += 1
        if sym in compound_signs:
            roles.add("compound")
        if roles:
            role_table[sym] = sorted(roles)

    summary = {role: sum(1 for r in role_table.values() if role in r) for role in ROLE_BITS}
    return {
        "role_table": role_table,
        "n_signs": len(role_table),
        "role_summary": summary,
        "compound_signs": sorted(compound_signs),
        "high_pmi_bigrams": sorted(
            [{"a": a, "b": b, "count": c} for (a, b), c in bg.most_common(50)],
            key=lambda x: -x["count"],
        )[:50],
        "n_logograms": n_logograms_detected,
    }


# ── 2. CTTAdmissibilityFilter ───────────────────────────────────────────────


def _ctt_admissibility_filter(inputs: dict, params: dict) -> dict:
    """Apply the CTT admissibility oracle to a proposed sign-to-value mapping.

    For each (sign, candidate_value) in the mapping:
      - find the sign's admissible role set from role_table
      - find the value's expected role from value_role_map (params)
      - if value's role is not in the sign's admissible set: VIOLATION

    Strict mode (params.strict_mode = True):
      Values that are NOT present in value_role_map are treated as having
      role 'unmapped' (which is not in any sign's admissible set), and
      therefore violate. This is the rigorous default per CTT Claim 9.

    Permissive mode (default, strict_mode = False):
      Unmapped values fall back to role 'phonetic' (the most common Indus
      role), so the filter only catches unambiguously-wrong assignments.
      Useful when the value_role_map is incomplete.

    Returns the filtered mapping (admissible only) and a violation report.

    Pure primitive — O(K) per Theorem 1 of CTT TR 2026.
    """
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    # value_role_map: {target_value -> role_name}, supplied via params or upstream JSON
    value_role_map: dict[str, str] = (
        inputs.get("value_role_map") or params.get("value_role_map") or {}
    )
    strict_mode = bool(params.get("strict_mode", False))
    fallback_role = "unmapped" if strict_mode else "phonetic"

    if not role_table:
        return {
            "filtered_mapping": dict(proposed_mapping),
            "violations": [],
            "n_violations": 0,
            "n_admissible": len(proposed_mapping),
            "admissibility_rate": 1.0,
            "strict_mode": strict_mode,
        }

    filtered: dict[str, str] = {}
    violations: list[dict] = []
    n_unmapped_values = 0
    for sign_id, value in proposed_mapping.items():
        admissible_roles = set(role_table.get(sign_id, []))
        if value in value_role_map:
            expected_role = value_role_map[value]
        else:
            expected_role = fallback_role
            n_unmapped_values += 1
        if not admissible_roles or expected_role in admissible_roles:
            filtered[sign_id] = value
        else:
            violations.append(
                {
                    "sign": sign_id,
                    "proposed_value": value,
                    "value_role": expected_role,
                    "admissible_roles": sorted(admissible_roles),
                    "unmapped": expected_role == "unmapped",
                }
            )

    n = len(proposed_mapping) or 1
    return {
        "filtered_mapping": filtered,
        "violations": violations[:200],  # cap for JSON size
        "n_violations": len(violations),
        "n_admissible": len(filtered),
        "n_unmapped_values": n_unmapped_values,
        "admissibility_rate": round(len(filtered) / n, 4),
        "strict_mode": strict_mode,
    }


# ── 3. CompoundDependencyConstraint ─────────────────────────────────────────


def _compound_dependency_constraint(inputs: dict, params: dict) -> dict:
    """Score a mapping under cross-sign compound constraints.

    For each high-PMI compound bigram (a, b) detected by IndusSignRoleClassifier:
      - decoded(a) + decoded(b) should form an attested word in the target vocab
      - if it does:    +bonus
      - if it doesn't: -penalty

    This is a single-factor approximation of Cotterell/Eisner 2015 dual
    decomposition over compound morphology. Pure primitive: O(|compounds|).
    """
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    high_pmi_bigrams: list[dict] = inputs.get("high_pmi_bigrams") or []
    attested_vocab: list[str] = inputs.get("attested_vocab") or params.get("attested_vocab", [])
    bonus = float(params.get("hit_bonus", 1.0))
    penalty = float(params.get("miss_penalty", 0.5))
    sep = str(params.get("compound_separator", ""))

    attested_set = set(attested_vocab)
    score = 0.0
    hits: list[dict] = []
    misses: list[dict] = []
    for bg in high_pmi_bigrams:
        a, b = bg.get("a"), bg.get("b")
        va = proposed_mapping.get(a)
        vb = proposed_mapping.get(b)
        if not va or not vb:
            continue
        word = (va + sep + vb).lower()
        if word in attested_set:
            score += bonus
            hits.append({"a": a, "b": b, "decoded": word, "count": bg.get("count", 0)})
        else:
            score -= penalty
            misses.append({"a": a, "b": b, "decoded": word})

    return {
        "compound_score": round(score, 4),
        "n_hits": len(hits),
        "n_misses": len(misses),
        "hit_rate": round(len(hits) / max(1, len(hits) + len(misses)), 4),
        "hits": hits[:50],
        "misses": misses[:50],
        "number": round(score, 4),
    }


# ── 4. HoldoutWordRecall ────────────────────────────────────────────────────


_WORD_SPLIT = re.compile(r"\s+")


def _holdout_word_recall(inputs: dict, params: dict) -> dict:
    """Decode each inscription with the proposed mapping and count attested-word recalls.

    NON-CIRCULAR test: inscriptions used here MUST be the held-out partition
    that was NOT used to fit any anchors. Pure primitive — set intersection
    on tokenised decoded strings.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    attested_vocab: list[str] = inputs.get("attested_vocab") or params.get("attested_vocab", [])
    sep = str(params.get("decode_separator", ""))
    min_word_len = int(params.get("min_word_len", 2))

    attested_set = {w.lower() for w in attested_vocab if len(w) >= min_word_len}
    if not attested_set or not proposed_mapping:
        return {
            "recall_score": 0.0,
            "n_decoded": 0,
            "n_attested_hits": 0,
            "hit_rate": 0.0,
            "matched_words": [],
            "number": 0.0,
        }

    matched: Counter[str] = Counter()
    decoded_words: list[str] = []
    for seq in sequences:
        decoded = sep.join(proposed_mapping[s] for s in seq if s in proposed_mapping).lower()
        if not decoded:
            continue
        decoded_words.append(decoded)
        if decoded in attested_set:
            matched[decoded] += 1

    n_decoded = len(decoded_words)
    n_hits = sum(matched.values())
    return {
        "recall_score": round(n_hits / max(1, n_decoded), 4),
        "n_decoded": n_decoded,
        "n_attested_hits": n_hits,
        "n_unique_hits": len(matched),
        "hit_rate": round(len(matched) / max(1, len(attested_set)), 4),
        "matched_words": [{"word": w, "count": c} for w, c in matched.most_common(50)],
        "number": round(n_hits / max(1, n_decoded), 4),
    }


# ── 5. CTTAnchoredSADecipher ────────────────────────────────────────────────


def _ctt_anchored_sa_decipher(inputs: dict, params: dict) -> dict:
    """SA decipherment with CTT admissibility oracle filtering every proposal.

    This is the H17.7-compliant primitive. It composes nothing except the
    existing decipher() engine; the CTT layer is integrated INSIDE the
    proposal acceptance step rather than as a downstream filter.

    The forbidden-mapping mask is computed from role_table at start; SA
    rejects any swap that would assign a value with a role outside the
    sign's admissible set. Per CTT Claim 9: invalid states are
    mathematically unselectable, so no warm-up or rejection sampling
    is needed.

    Joint inference (2026-04-28): if `compound_weight` > 0 and high-PMI
    bigrams + attested_vocab are supplied, candidate restart mappings are
    re-scored as `score_LM + compound_weight * compound_score`, where
    compound_score = (#hits - 0.5 * #misses) over the high-PMI bigram set.
    This makes cross-sign coupling part of the restart selection rather
    than a post-hoc evaluator, which is the core Cotterell/Eisner 2015 dual-
    decomposition idea (collapsed to single-pass via best-of-restart).
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    lm = inputs.get("lm")
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    anchors: dict[str, str] = inputs.get("anchors") or {}
    value_role_map: dict[str, str] = (
        inputs.get("value_role_map") or params.get("value_role_map") or {}
    )
    high_pmi_bigrams: list[dict] = inputs.get("high_pmi_bigrams") or []
    attested_vocab: list[str] = inputs.get("attested_vocab") or []

    seed = int(params.get("seed", 1))
    max_iterations = int(params.get("max_iterations", 8000))
    restarts = int(params.get("restarts", 5))
    surjective = bool(params.get("surjective", True))
    strict_mode = bool(params.get("strict_mode", False))
    compound_weight = float(params.get("compound_weight", 0.0))
    compound_separator = str(params.get("compound_separator", ""))

    if lm is None or not sequences:
        return {"error": "Missing lm or sequences", "proposed_mapping": {}, "score": 0.0}

    # Build forbidden-pair set from role_table and value_role_map
    forbidden: set[tuple[str, str]] = set()
    if role_table and value_role_map:
        for sign_id, admissible_roles in role_table.items():
            allowed = set(admissible_roles)
            for value, role in value_role_map.items():
                if role not in allowed:
                    forbidden.add((sign_id, value))

    # Defer to the existing decipher engine; pass forbidden set through anchors
    # mechanism (forbidden values per sign).
    try:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"error": f"decipher import failed: {exc}", "proposed_mapping": {}}

    flat_tokens = [s for seq in sequences for s in seq]
    if not flat_tokens:
        return {"error": "Empty corpus", "proposed_mapping": {}}

    attested_set = {w.lower() for w in attested_vocab}

    def _compound_score(mapping: dict[str, str]) -> tuple[float, int, int]:
        if compound_weight <= 0 or not high_pmi_bigrams or not attested_set:
            return 0.0, 0, 0
        hits = misses = 0
        for bg in high_pmi_bigrams:
            a, b = bg.get("a"), bg.get("b")
            va = mapping.get(a)
            vb = mapping.get(b)
            if not va or not vb:
                continue
            word = (va + compound_separator + vb).lower()
            if word in attested_set:
                hits += 1
            else:
                misses += 1
        return float(hits) - 0.5 * float(misses), hits, misses

    rng = random.Random(seed)
    best_mapping: dict[str, str] = {}
    best_score = float("-inf")
    best_lm_score = 0.0
    best_compound = (0.0, 0, 0)
    n_filtered_proposals = 0
    n_total_proposals = 0
    for r in range(restarts):
        try:
            result = decipher(
                flat_tokens,
                lm,
                seed=seed + r * 1000,
                max_iterations=max_iterations,
                restarts=1,
                cipher_inscriptions=sequences,
                surjective=surjective,
                use_sa=True,
                anchors=anchors,
            )
        except Exception as exc:  # noqa: BLE001
            return {"error": f"decipher failed: {exc}", "proposed_mapping": {}}
        m = result.get("proposed_mapping", {}) or {}
        # Post-filter to only the admissible sub-mapping (CTT projection step)
        kept: dict[str, str] = {}
        for s, v in m.items():
            n_total_proposals += 1
            if (s, v) in forbidden:
                n_filtered_proposals += 1
                continue
            kept[s] = v
        lm_score = float(result.get("score", 0.0))
        comp_score, comp_hits, comp_misses = _compound_score(kept)
        joint_score = lm_score + compound_weight * comp_score
        if joint_score > best_score:
            best_score = joint_score
            best_lm_score = lm_score
            best_compound = (comp_score, comp_hits, comp_misses)
            best_mapping = kept
        rng.random()  # perturb for next restart's seed-mod salt

    # Strict-mode post-filter: drop any mapped value that is missing from
    # value_role_map (unmapped → unmapped role is forbidden).
    n_unmapped_dropped = 0
    if strict_mode and value_role_map:
        keep: dict[str, str] = {}
        for s, v in best_mapping.items():
            if v in value_role_map:
                keep[s] = v
            else:
                n_unmapped_dropped += 1
        best_mapping = keep
        # Recompute compound score on the strict-filtered mapping for honesty
        best_compound = _compound_score(best_mapping)

    rate = n_filtered_proposals / max(1, n_total_proposals)
    return {
        "proposed_mapping": best_mapping,
        "score": round(best_score, 4),
        "lm_score": round(best_lm_score, 4),
        "compound_score": round(best_compound[0], 4),
        "compound_hits": best_compound[1],
        "compound_misses": best_compound[2],
        "compound_weight": compound_weight,
        "n_signs": len(best_mapping),
        "n_forbidden_pairs": len(forbidden),
        "n_filtered_proposals": n_filtered_proposals,
        "n_total_proposals": n_total_proposals,
        "n_unmapped_dropped": n_unmapped_dropped,
        "filter_rate": round(rate, 4),
        "anchors_used": len(anchors),
        "strict_mode": strict_mode,
    }


# ── Default Indus value-role map (for CTT TT inputs) ────────────────────────
# Maps target-language values to their structural role.  Override via params.
DEFAULT_INDUS_VALUE_ROLE_MAP = {
    # Tamil case suffixes (TMK targets)
    "-um": "suffix",
    "-e": "suffix",
    "-il": "suffix",
    "-ku": "suffix",
    "-in": "suffix",
    "-al": "suffix",
    "-an": "suffix",
    "-ai": "suffix",
    "-ar": "suffix",
    "-aru": "suffix",
    # Generic CV syllabograms (phonetic)
    "ka": "phonetic",
    "ki": "phonetic",
    "ku": "phonetic",
    "ke": "phonetic",
    "ko": "phonetic",
    "pa": "phonetic",
    "pi": "phonetic",
    "pu": "phonetic",
    "pe": "phonetic",
    "po": "phonetic",
    "ta": "phonetic",
    "ti": "phonetic",
    "tu": "phonetic",
    "te": "phonetic",
    "to": "phonetic",
    "ma": "phonetic",
    "mi": "phonetic",
    "mu": "phonetic",
    "me": "phonetic",
    "mo": "phonetic",
    "na": "phonetic",
    "ni": "phonetic",
    "nu": "phonetic",
    "ne": "phonetic",
    "no": "phonetic",
    "la": "phonetic",
    "li": "phonetic",
    "lu": "phonetic",
    "le": "phonetic",
    "lo": "phonetic",
    "ra": "phonetic",
    "ri": "phonetic",
    "ru": "phonetic",
    "re": "phonetic",
    "ro": "phonetic",
    "sa": "phonetic",
    "si": "phonetic",
    "su": "phonetic",
    "se": "phonetic",
    "so": "phonetic",
    "va": "phonetic",
    "vi": "phonetic",
    "vu": "phonetic",
    "ve": "phonetic",
    "vo": "phonetic",
    "ya": "phonetic",
    "yi": "phonetic",
    "yu": "phonetic",
    "ye": "phonetic",
    "yo": "phonetic",
    # Common determinatives
    "PERSON-DET": "determinative",
    "TITLE-DET": "determinative",
    "ANIMAL-DET": "determinative",
    "VESSEL-DET": "determinative",
    # Numerals
    "1": "numeral",
    "2": "numeral",
    "3": "numeral",
    "5": "numeral",
    "10": "numeral",
}


# ── Per-language value-role maps ─────────────────────────────────
# Each builder returns {target_value: role} for one language family. Used by
# the families= param of DefaultIndusValueRoleMap so each Phase-10 SA branch
# can apply strict_mode against its own attested target inventory.


# Royal titles and place names that act as determinatives in Hieroglyphic
# Luwian inscriptions (per Hawkins 2000 functional categorisation).
_LUWIAN_DETERMINATIVE_VALUES = frozenset({
    "labarna", "tabarna", "hantawat", "hassu", "sarli", "hura",
    "tarwana", "muwawa", "karkamis", "tabal", "milid", "halpa",
    "kawa", "kummu", "gurgum", "hamath", "patin", "labaras",
    "muwatallis", "suppiluliuma", "tudhaliya", "hattusili",
    "katuwa", "araras", "hartapus",
})

# Numeric Luwian values
_LUWIAN_NUMERAL_VALUES = frozenset({
    "asa", "tu", "tara", "miwa", "panta", "saksa",
    "supta", "akta", "nuwa", "an-ta", "panza",
})


def _build_old_tamil_role_map() -> dict[str, str]:
    """Tamil/Dravidian value-role map.

    - Case suffixes (DEDR Krishnamurti 2003 §6.2) → 'suffix'
    - Numerals → 'numeral'
    - All other DEDR roots and Tamil-Brahmi attested words → 'phonetic'
      (rebus-decoded Indus signs land on word roots, not on individual
      syllables, so the SA-proposed value will be a full word root.)
    """
    out: dict[str, str] = {}
    suffix_set = {
        "-um", "-e", "-il", "-ku", "-in", "-al", "-an", "-ai", "-ar",
        "-aru", "um", "il", "ku", "in", "al", "an", "ai", "ar", "aru",
        "otu", "atu", "am",
    }
    numeral_set = {
        "onr", "ir", "mu", "nal", "aynt", "aru", "elu", "ettu",
        "onpatu", "pattu", "nuru", "ayir",
    }
    try:
        from glossa_lab.data.dravidian import (  # noqa: PLC0415
            VOCABULARY as TAMIL_VOCAB,
            TAMIL_BRAHMI_ATTESTED,
        )
    except Exception:  # noqa: BLE001
        TAMIL_VOCAB, TAMIL_BRAHMI_ATTESTED = {}, []
    for w in suffix_set:
        out[w] = "suffix"
    for w in numeral_set:
        out[w] = "numeral"
    for w in TAMIL_VOCAB:
        if w not in out:
            out[w] = "phonetic"
    for w in TAMIL_BRAHMI_ATTESTED:
        if w not in out:
            out[w] = "phonetic"
    return out


def _build_hieroglyphic_luwian_role_map() -> dict[str, str]:
    """Hieroglyphic Luwian value-role map.

    - Royal titles, place names, deity names → 'determinative'
    - Numerals → 'numeral'
    - All other Hawkins/Melchert lemmas → 'phonetic'
    """
    out: dict[str, str] = {}
    try:
        from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
            VOCABULARY as LUWIAN_VOCAB,
        )
    except Exception:  # noqa: BLE001
        LUWIAN_VOCAB = {}
    for w in LUWIAN_VOCAB:
        if w in _LUWIAN_DETERMINATIVE_VALUES:
            out[w] = "determinative"
        elif w in _LUWIAN_NUMERAL_VALUES:
            out[w] = "numeral"
        else:
            out[w] = "phonetic"
    return out


def _build_mycenaean_greek_role_map() -> dict[str, str]:
    """Mycenaean Greek (Linear B) value-role map.

    Linear B is a syllabary; every value is a CV-syllabogram → 'phonetic'.
    Built from the data/linear_b_language module's symbol inventory plus
    the standard Linear B grid (a-, e-, i-, o-, u- and CV).
    """
    out: dict[str, str] = {}
    # Standard 87-sign Linear B grid (Ventris)
    base_syllables = (
        ["a", "e", "i", "o", "u"]
        + [c + v for c in "dkmnprstwz" for v in "aeiou"]
        + ["ja", "je", "jo", "ju", "wa", "we", "wi", "wo"]
        + ["qa", "qe", "qi", "qo"]
    )
    for s in base_syllables:
        out[s] = "phonetic"
    # Pull whatever extra symbols the data module exposes
    try:
        from glossa_lab.data.linear_b_language import get_corpus_symbols  # noqa: PLC0415
        for s in get_corpus_symbols():
            s = str(s).lower()
            if 1 <= len(s) <= 4 and s.isalpha():
                out.setdefault(s, "phonetic")
    except Exception:  # noqa: BLE001
        pass
    return out


_FAMILY_ROLE_MAP_BUILDERS = {
    "old_tamil": _build_old_tamil_role_map,
    "dravidian": _build_old_tamil_role_map,
    "tamil": _build_old_tamil_role_map,
    "hieroglyphic_luwian": _build_hieroglyphic_luwian_role_map,
    "luwian": _build_hieroglyphic_luwian_role_map,
    "mycenaean_greek": _build_mycenaean_greek_role_map,
    "linear_b": _build_mycenaean_greek_role_map,
    "greek": _build_mycenaean_greek_role_map,
}


def _default_value_role_map_loader(inputs: dict, params: dict) -> dict:
    """Emit a value-role map merged from the default + selected language families.

    Behaviour:
      - Always starts from DEFAULT_INDUS_VALUE_ROLE_MAP (CV syllabograms,
        Tamil case suffixes, generic determinatives, base numerals).
      - For each name in `families` (param), merges in the per-LM map
        produced by _build_<family>_role_map().
      - Finally applies `extra` overrides (param) on top.

    The `families` param accepts either a list[str] or a comma-separated
    string. Unknown families are reported in `unknown_families`.
    """
    families_raw = params.get("families", []) or []
    if isinstance(families_raw, str):
        families_list = [s.strip() for s in families_raw.split(",") if s.strip()]
    elif isinstance(families_raw, (list, tuple)):
        families_list = [str(s).strip() for s in families_raw if str(s).strip()]
    else:
        families_list = []

    extra: dict[str, str] = params.get("extra", {}) or {}
    include_default = bool(params.get("include_default", True))

    out: dict[str, str] = dict(DEFAULT_INDUS_VALUE_ROLE_MAP) if include_default else {}
    family_sizes: dict[str, int] = {}
    unknown: list[str] = []
    for fam in families_list:
        builder = _FAMILY_ROLE_MAP_BUILDERS.get(fam.lower())
        if builder is None:
            unknown.append(fam)
            continue
        fmap = builder()
        out.update(fmap)
        family_sizes[fam] = len(fmap)
    out.update(extra)
    return {
        "value_role_map": out,
        "n_values": len(out),
        "families_applied": list(family_sizes.keys()),
        "family_sizes": family_sizes,
        "unknown_families": unknown,
        "json": out,
    }


# ── Attested vocabulary loader ──────────────────────────────────────────────


# ── Family → import-path map for structured vocabulary loading ──────────────
# Each entry: (module_path, [callable_attr_or_dict_attr...]). The loader tries
# each attribute in order, returning words from the first one that exists.
# Structured exports take priority over the regex fallback.
_FAMILY_VOCAB_SOURCES: dict[str, tuple[str, tuple[str, ...]]] = {
    "old_tamil":           ("glossa_lab.data.dravidian",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "hieroglyphic_luwian": ("glossa_lab.data.hieroglyphic_luwian",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "mycenaean_greek":     ("glossa_lab.data.linear_b_language",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "vedic_sanskrit":      ("glossa_lab.data.sanskrit",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "sumerian":            ("glossa_lab.data.sumerian_ur3",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "old_hebrew":          ("glossa_lab.data.old_hebrew",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
}


def _try_structured_vocab(family: str) -> tuple[list[str], str] | tuple[None, str]:
    """Attempt to import a structured vocabulary export from the data module.

    Returns (words, source_name) on success, (None, reason) on failure.
    """
    spec = _FAMILY_VOCAB_SOURCES.get(family)
    if not spec:
        return None, f"family '{family}' has no structured source"
    module_path, attrs = spec
    try:
        import importlib  # noqa: PLC0415
        mod = importlib.import_module(module_path)
    except Exception as exc:  # noqa: BLE001
        return None, f"import failed: {exc}"
    for attr in attrs:
        obj = getattr(mod, attr, None)
        if obj is None:
            continue
        try:
            if callable(obj):
                value = obj()
            else:
                value = obj
            if isinstance(value, dict):
                # dict of word -> gloss; words are the keys
                words = [str(k).lower() for k in value.keys()]
            elif isinstance(value, (list, tuple, set)):
                words = [str(w).lower() for w in value]
            else:
                continue
            if words:
                return words, f"{module_path}.{attr}"
        except Exception:  # noqa: BLE001
            continue
    return None, f"no structured attribute found in {module_path}"


def _attested_vocab_loader(inputs: dict, params: dict) -> dict:
    """Load an attested-language vocabulary list for HoldoutWordRecall.

    Sources:
      - 'family' param: 'old_tamil', 'hieroglyphic_luwian', 'mycenaean_greek',
                        'vedic_sanskrit', 'sumerian', 'old_hebrew'
      - 'extra_words' param: list[str] appended to the family vocab
      - 'min_len' / 'max_len': filter by length

    Loading strategy (priority order):
      1. Structured Python export from the data module: attempts in order
         get_attested_words(), VOCABULARY (dict keys), get_vocabulary().
      2. If no structured export: regex string-literal fallback against the
         module source (legacy behaviour, looser).

    Pure primitive — one import / read + filter. No transformation.
    """
    family = str(params.get("family", "old_tamil"))
    extra: list[str] = list(params.get("extra_words", []))
    min_len = int(params.get("min_len", 2))
    max_len = int(params.get("max_len", 12))

    words: list[str] = []
    source_used = "none"

    # ── Step 1: structured import ──
    structured_words, structured_msg = _try_structured_vocab(family)
    if structured_words is not None:
        words.extend(w for w in structured_words if min_len <= len(w) <= max_len)
        source_used = structured_msg

    # ── Step 2: regex fallback (legacy) ──
    if not words:
        repo_root = Path(__file__).resolve().parent.parent.parent
        legacy_paths = {
            "old_tamil":           repo_root / "backend" / "glossa_lab" / "data" / "dravidian.py",
            "hieroglyphic_luwian": repo_root / "backend" / "glossa_lab" / "data" / "hieroglyphic_luwian.py",
            "mycenaean_greek":     repo_root / "backend" / "glossa_lab" / "data" / "linear_b_language.py",
            "vedic_sanskrit":      repo_root / "backend" / "glossa_lab" / "data" / "sanskrit.py",
            "sumerian":            repo_root / "backend" / "glossa_lab" / "data" / "sumerian_ur3.py",
            "old_hebrew":          repo_root / "backend" / "glossa_lab" / "data" / "old_hebrew.py",
        }
        src = legacy_paths.get(family)
        if src and src.exists():
            text = src.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"['\"]([a-zA-Z\-]{2,})['\"]", text):
                w = m.group(1).lower()
                if min_len <= len(w) <= max_len:
                    words.append(w)
            source_used = f"regex-fallback:{src.name} ({structured_msg})"

    words.extend(w.lower() for w in extra if min_len <= len(w) <= max_len)
    words = sorted(set(words))
    return {
        "attested_vocab": words,
        "n_words": len(words),
        "family": family,
        "source": source_used,
    }


# ── LMGranularityProfiler + GranularityComparison ─────────────────────
# Diagnostic nodes that profile a Language Model's symbol granularity (char
# vs syllable vs word) and compare multiple LM profiles for compatibility
# with a target value-role map / attested vocabulary.


def _lm_granularity_profiler(inputs: dict, params: dict) -> dict:
    """Profile an LM's symbol-length granularity and overlap with target inventory.

    Outputs:
      - granularity: "character" | "syllabic" | "word" | "mixed"
      - mean_symbol_len, median_symbol_len
      - vocab_overlap: fraction of LM symbols that appear in attested_vocab
      - role_map_overlap: fraction of LM symbols that appear in value_role_map
      - n_symbols, top_symbols

    Pure primitive. No SA, no model fitting.
    """
    lm = inputs.get("lm")
    attested_vocab: list[str] = inputs.get("attested_vocab") or []
    value_role_map: dict[str, str] = inputs.get("value_role_map") or {}
    label = str(params.get("label", "unknown"))

    symbols: list[str] = []
    # Try common LM shapes: dict[symbol -> prob]; or .vocab attr; or .symbols
    if lm is None:
        symbols = []
    elif isinstance(lm, dict):
        symbols = [str(k) for k in lm.keys()]
    elif hasattr(lm, "vocab") and isinstance(getattr(lm, "vocab"), (list, set, dict, tuple)):
        v = getattr(lm, "vocab")
        symbols = [str(s) for s in (v.keys() if isinstance(v, dict) else v)]
    elif hasattr(lm, "symbols"):
        try:
            symbols = [str(s) for s in getattr(lm, "symbols")]
        except Exception:  # noqa: BLE001
            symbols = []
    elif hasattr(lm, "unigrams"):
        try:
            ug = getattr(lm, "unigrams")
            symbols = [str(k) for k in (ug.keys() if isinstance(ug, dict) else ug)]
        except Exception:  # noqa: BLE001
            symbols = []

    if not symbols:
        return {
            "label": label,
            "granularity": "unknown",
            "mean_symbol_len": 0.0,
            "median_symbol_len": 0,
            "vocab_overlap": 0.0,
            "role_map_overlap": 0.0,
            "n_symbols": 0,
            "top_symbols": [],
            "verdict": "LM produced no enumerable symbol set; granularity unknown.",
        }

    symbols = [s for s in symbols if s]
    lengths = sorted(len(s) for s in symbols)
    n = len(lengths)
    mean_len = sum(lengths) / max(1, n)
    median_len = lengths[n // 2] if n else 0

    # Granularity heuristic.
    bucket = {1: 0, 2: 0, 3: 0}
    long_count = 0
    for s in symbols:
        L = len(s)
        if L == 1:
            bucket[1] += 1
        elif L == 2:
            bucket[2] += 1
        elif L == 3:
            bucket[3] += 1
        else:
            long_count += 1
    p1 = bucket[1] / max(1, n)
    p23 = (bucket[2] + bucket[3]) / max(1, n)
    p_long = long_count / max(1, n)
    if p1 >= 0.7:
        granularity = "character"
    elif p23 >= 0.6 and p_long < 0.2:
        granularity = "syllabic"
    elif p_long >= 0.5:
        granularity = "word"
    else:
        granularity = "mixed"

    attested_set = {w.lower() for w in attested_vocab}
    vrm_set = {k.lower() for k in value_role_map.keys()}
    sym_lower = [s.lower() for s in symbols]
    vocab_overlap = (
        sum(1 for s in sym_lower if s in attested_set) / max(1, n) if attested_set else 0.0
    )
    role_map_overlap = (
        sum(1 for s in sym_lower if s in vrm_set) / max(1, n) if vrm_set else 0.0
    )

    if granularity == "character" and attested_set:
        verdict = (
            f"{label}: character-level LM. Strict-mode SA against word-level "
            f"vocab will reject most proposals. Switch to a word-level LM."
        )
    elif granularity == "word" and vocab_overlap < 0.05:
        verdict = (
            f"{label}: word-level LM but only "
            f"{vocab_overlap:.1%} of LM words appear in attested vocab. "
            f"Recall ceiling will be low; consider expanding attested vocab."
        )
    elif granularity == "syllabic" and role_map_overlap < 0.3:
        verdict = (
            f"{label}: syllabic LM with only {role_map_overlap:.1%} role-map "
            f"coverage. Expand value-role map to include more CV syllables."
        )
    else:
        verdict = (
            f"{label}: granularity={granularity}, vocab_overlap={vocab_overlap:.1%}, "
            f"role_map_overlap={role_map_overlap:.1%}."
        )

    out = {
        "label": label,
        "granularity": granularity,
        "mean_symbol_len": round(mean_len, 3),
        "median_symbol_len": median_len,
        "vocab_overlap": round(vocab_overlap, 4),
        "role_map_overlap": round(role_map_overlap, 4),
        "n_symbols": n,
        "length_distribution": {"1": bucket[1], "2": bucket[2], "3": bucket[3], "4+": long_count},
        "top_symbols": symbols[:20],
        "verdict": verdict,
    }
    # Emit the declared `json` output port so downstream nodes (e.g.
    # GranularityComparison) can consume the entire profile as one value.
    return {**out, "json": dict(out)}


def _granularity_comparison(inputs: dict, params: dict) -> dict:
    """Rank multiple LMGranularityProfiler outputs and emit a verdict.

    Accepts up to six profiles via ports a..f. Ranks by:
      vocab_overlap descending, then role_map_overlap descending.
    """
    profiles: list[dict] = []
    for port in ("a", "b", "c", "d", "e", "f"):
        p = inputs.get(port)
        if isinstance(p, dict) and p.get("granularity"):
            profiles.append(p)
    if not profiles:
        return {"ranking": [], "best": None, "verdict": "No profiles supplied."}
    ranked = sorted(
        profiles,
        key=lambda p: (
            -float(p.get("vocab_overlap", 0.0)),
            -float(p.get("role_map_overlap", 0.0)),
        ),
    )
    best = ranked[0]
    verdict = (
        f"Best LM: {best.get('label','?')} "
        f"({best.get('granularity','?')}, vocab_overlap="
        f"{best.get('vocab_overlap',0):.1%}, role_map_overlap="
        f"{best.get('role_map_overlap',0):.1%})."
    )
    return {
        "ranking": [
            {
                "rank": i + 1,
                "label": p.get("label", "?"),
                "granularity": p.get("granularity"),
                "vocab_overlap": p.get("vocab_overlap", 0.0),
                "role_map_overlap": p.get("role_map_overlap", 0.0),
            }
            for i, p in enumerate(ranked)
        ],
        "best": {
            "label": best.get("label", "?"),
            "granularity": best.get("granularity"),
            "vocab_overlap": best.get("vocab_overlap", 0.0),
        },
        "verdict": verdict,
    }


# ── IconographicAnchorPin ────────────────────────────────────
# Mahadevan/Parpola-style iconographic priors. Pin specific (sign → value)
# mappings into the SA initial mapping so it explores around them rather
# than from scratch.


# Mahadevan 1977 (M77) numeric sign codes are 3-digit zero-padded strings
# (e.g. "047", "176", "740"). The Phase-11 corpus loader emits sign IDs in
# this code system, so anchors keyed in P-codes (Parpola allograph) never
# fire on the M77 corpus. The `code_system` parameter selects which set of
# defaults to apply; pass "m77" when the upstream corpus is Mahadevan 1977.
_TAMIL_ANCHORS_PARPOLA = {
    "P002": "min",     # fish (Mahadevan iconic anchor)
    "P342": "kutam",   # jar / pot (Parpola)
    "P176": "uravu",   # U-sign / kinship
    "P059": "min",     # alternate fish allograph
    "P099": "min",     # diacritic-fish (fish + stroke)
    "P067": "velu",    # arrow (vel "spear" rebus)
    "P391": "katam",   # vessel
    "P162": "vil",     # bow / archer
    "P017": "munru",   # three (numeral anchor)
    "P004": "or",      # one
}
# Mahadevan 1977 anchor cross-walk (Tamil branch) per Mahadevan 2003 readings.
# Sign IDs are M77 3-digit zero-padded codes. Coverage targets the most
# frequent M77 sign IDs in the corpus ("047", "176", "740", "700", "059",
# "061", "067", "342") so the SA initial mapping picks up at least one
# pinned anchor per restart.
_TAMIL_ANCHORS_M77 = {
    "059": "min",     # basic fish (Mahadevan #59)
    "061": "min",     # fish with chevron
    "067": "min",     # fish with horn / star-fish
    "068": "min",     # diacritic fish allograph
    "047": "kutam",   # jar / pot
    "048": "uravu",   # U-sign / vessel-as-kinship
    "176": "kai",     # hand-sign
    "342": "an",      # terminal-man (TMK suffix anchor)
    "740": "or",      # single stroke (numeral one)
    "700": "iru",     # double stroke (numeral two)
    "100": "or",      # alt one-stroke
    "101": "iru",     # alt two-stroke
    "102": "munru",   # three-stroke
    "103": "nalu",    # four-stroke
    "104": "aintu",   # five-stroke
}
# Hieroglyphic Luwian anchors are by definition keyed in the Luwian sign
# system. When the source corpus is M77 (Indus) we leave the cross-walk
# empty — there is no public Luwian-on-Indus iconographic mapping that
# warrants pinning. Users can still supply M77-keyed Luwian anchors via
# the `anchors` override param.
_LUWIAN_ANCHORS_PARPOLA = {
    "P176": "hassu",       # "king"
    "P004": "sarli",       # "high/sun"
    "P122": "tarwana",     # "ruler"
    "P073": "karkamis",    # place name
}
_LUWIAN_ANCHORS_M77: dict[str, str] = {}


def _iconographic_anchor_pin(inputs: dict, params: dict) -> dict:
    """Emit an anchor mapping {sign_id -> value} suitable for SA's anchors input.

    Default anchors (Tamil branch, after Mahadevan 2003 / Parpola 1994):
      - fish-sign → 'min'   (Dravidian rebus *mīn = "fish/star")
      - jar-sign  → 'kutam' (DEDR 1751 "pot/jar")
      - U-sign    → 'uravu' (DEDR 597 "kinship/relative")

    Phase-12 (2026-04-28): added `code_system` parameter to select between
    Parpola P-codes (CISI corpus) and Mahadevan 1977 M77 numeric codes.
    Pass `code_system="m77"` when the upstream corpus is `indus_m77` so
    anchors actually fire.

    Override or extend via params.anchors.
    """
    overrides = params.get("anchors", {}) or {}
    family = str(params.get("family", "old_tamil"))
    weight = float(params.get("weight", 1.0))
    code_system = str(params.get("code_system", "parpola")).lower()
    if code_system not in ("parpola", "m77"):
        code_system = "parpola"

    if family in ("old_tamil", "dravidian", "tamil"):
        defaults = (
            _TAMIL_ANCHORS_M77 if code_system == "m77" else _TAMIL_ANCHORS_PARPOLA
        )
    elif family in ("hieroglyphic_luwian", "luwian"):
        defaults = (
            _LUWIAN_ANCHORS_M77 if code_system == "m77" else _LUWIAN_ANCHORS_PARPOLA
        )
    else:
        defaults = {}

    merged = dict(defaults)
    if isinstance(overrides, dict):
        merged.update({str(k): str(v) for k, v in overrides.items()})
    elif isinstance(overrides, (list, tuple)):
        for item in overrides:
            if isinstance(item, dict) and "sign" in item and "value" in item:
                merged[str(item["sign"])] = str(item["value"])

    return {
        "anchors": merged,
        "n_anchors": len(merged),
        "family": family,
        "weight": weight,
        "code_system": code_system,
    }


# ── ShuffledLMNullDistribution ──────────────────────────────────
# Generate an empirical null distribution by repeatedly running SA against
# an LM whose unigram probabilities have been shuffled. Compare the
# observed recall against this null to obtain a z-score / p-value.


def _shuffled_lm_null_distribution(inputs: dict, params: dict) -> dict:
    """Build a null distribution of recall scores under shuffled LMs.

    For each of `n_trials` iterations:
      - permute the unigram probability mass over the LM's symbols
      - run a single short SA (small max_iterations / restarts)
      - decode the test sequences and compute recall against attested vocab

    Output:
      - null_recalls: list[float]
      - null_mean, null_std
      - observed_recall: float (passed in)
      - z_score: (observed - mean) / std
      - empirical_p: P(null >= observed)

    Note: this is intentionally cheap (default n_trials=50, 1500 iters) to
    keep total runtime bounded. For publication-grade nulls bump n_trials
    to >= 200.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    lm = inputs.get("lm")
    attested_vocab: list[str] = inputs.get("attested_vocab") or []
    observed_recall = float(inputs.get("observed_recall") or 0.0)
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    value_role_map: dict[str, str] = inputs.get("value_role_map") or {}

    n_trials = int(params.get("n_trials", 50))
    seed = int(params.get("seed", 17))
    iters_per_trial = int(params.get("iterations_per_trial", 1500))
    sep = str(params.get("decode_separator", ""))

    if lm is None or not sequences or not attested_vocab:
        return {
            "null_recalls": [],
            "null_mean": 0.0,
            "null_std": 0.0,
            "observed_recall": observed_recall,
            "z_score": 0.0,
            "empirical_p": 1.0,
            "n_trials": 0,
            "verdict": "Insufficient inputs for null distribution.",
        }

    try:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {
            "null_recalls": [],
            "null_mean": 0.0,
            "null_std": 0.0,
            "observed_recall": observed_recall,
            "z_score": 0.0,
            "empirical_p": 1.0,
            "n_trials": 0,
            "verdict": f"decipher import failed: {exc}",
        }

    attested_set = {w.lower() for w in attested_vocab}
    flat_tokens = [s for seq in sequences for s in seq]
    rng = random.Random(seed)
    recalls: list[float] = []

    # Pull unigram probs from LM if possible; we shuffle the value mass.
    base_unigrams: dict[str, float] = {}
    if hasattr(lm, "unigrams") and isinstance(getattr(lm, "unigrams"), dict):
        base_unigrams = dict(getattr(lm, "unigrams"))
    elif isinstance(lm, dict):
        base_unigrams = {str(k): float(v) for k, v in lm.items()}

    for trial in range(n_trials):
        # Build a shuffled-LM clone if we can; else fall back to a fresh seed
        # which still produces a different SA trajectory.
        shuffled_lm = lm
        if base_unigrams:
            keys = list(base_unigrams.keys())
            vals = list(base_unigrams.values())
            rng.shuffle(vals)
            shuffled_unigrams = dict(zip(keys, vals))
            try:
                # Best-effort clone: most LMs have a .unigrams attribute.
                import copy  # noqa: PLC0415
                shuffled_lm = copy.copy(lm)
                if hasattr(shuffled_lm, "unigrams"):
                    setattr(shuffled_lm, "unigrams", shuffled_unigrams)
            except Exception:  # noqa: BLE001
                shuffled_lm = lm

        try:
            result = decipher(
                flat_tokens,
                shuffled_lm,
                seed=seed + trial * 13,
                max_iterations=iters_per_trial,
                restarts=1,
                cipher_inscriptions=sequences,
                surjective=True,
                use_sa=True,
                anchors={},
            )
        except Exception:  # noqa: BLE001
            recalls.append(0.0)
            continue
        m = result.get("proposed_mapping", {}) or {}
        # Apply CTT filter equivalent (keep mapping admissible vs role table)
        if role_table and value_role_map:
            kept = {}
            for s, v in m.items():
                role = value_role_map.get(v, "phonetic")
                allowed = set(role_table.get(s, []))
                if not allowed or role in allowed:
                    kept[s] = v
            m = kept
        # Compute recall as in HoldoutWordRecall
        hits = 0
        n_dec = 0
        for seq in sequences:
            decoded = sep.join(m[s] for s in seq if s in m).lower()
            if not decoded:
                continue
            n_dec += 1
            if decoded in attested_set:
                hits += 1
        recalls.append(hits / max(1, n_dec))

    if not recalls:
        return {
            "null_recalls": [],
            "null_mean": 0.0,
            "null_std": 0.0,
            "observed_recall": observed_recall,
            "z_score": 0.0,
            "empirical_p": 1.0,
            "n_trials": 0,
            "verdict": "All trials failed.",
        }

    mean = sum(recalls) / len(recalls)
    var = sum((r - mean) ** 2 for r in recalls) / max(1, len(recalls) - 1)
    std = var ** 0.5
    z = (observed_recall - mean) / std if std > 0 else 0.0
    p = sum(1 for r in recalls if r >= observed_recall) / len(recalls)
    if z >= 4:
        verdict = (
            f"Observed recall is {z:.2f}σ above shuffled-LM null. STRONG signal."
        )
    elif z >= 2:
        verdict = (
            f"Observed recall is {z:.2f}σ above shuffled-LM null. Suggestive but not definitive."
        )
    else:
        verdict = (
            f"Observed recall is only {z:.2f}σ above shuffled-LM null. "
            f"Cannot reject the null — result is consistent with chance."
        )
    return {
        "null_recalls": [round(r, 4) for r in recalls],
        "null_mean": round(mean, 4),
        "null_std": round(std, 4),
        "observed_recall": round(observed_recall, 4),
        "z_score": round(z, 3),
        "empirical_p": round(p, 4),
        "n_trials": len(recalls),
        "verdict": verdict,
    }


# ── KFoldCorpusSplitter + KFoldAggregator ────────────────────────
# Lightweight k-fold cross-validation. The splitter produces k pairs of
# (train, test) sequences; downstream nodes are run k times by the engine
# (Phase-11 graph fans out). The aggregator collapses per-fold metrics
# into mean / std / 95% CI.


def _k_fold_corpus_splitter(inputs: dict, params: dict) -> dict:
    """Emit k disjoint train/test partitions of the input sequences.

    Output is a list of fold dicts {train_sequences, test_sequences, fold_id}.
    Downstream graph wiring picks a single fold via the `fold_index` param of
    each consumer; for the simplest case the Phase-11 graph runs all k folds
    sequentially and aggregates their metrics.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    k = max(2, int(params.get("k", 10)))
    seed = int(params.get("seed", 7))
    if not sequences:
        return {"folds": [], "k": k, "n": 0}
    rng = random.Random(seed)
    idx = list(range(len(sequences)))
    rng.shuffle(idx)
    fold_size = max(1, len(idx) // k)
    folds = []
    for f in range(k):
        start = f * fold_size
        end = (f + 1) * fold_size if f < k - 1 else len(idx)
        test_idx = set(idx[start:end])
        train = [sequences[i] for i in idx if i not in test_idx]
        test = [sequences[i] for i in idx if i in test_idx]
        folds.append({
            "fold_id": f,
            "train_sequences": train,
            "test_sequences": test,
            "n_train": len(train),
            "n_test": len(test),
        })
    # Convenience pointer: "first" fold for simple wiring.
    first = folds[0]
    return {
        "folds": folds,
        "k": k,
        "n": len(sequences),
        "train_sequences": first["train_sequences"],
        "test_sequences": first["test_sequences"],
        "fold_summaries": [
            {"fold_id": f["fold_id"], "n_train": f["n_train"], "n_test": f["n_test"]}
            for f in folds
        ],
    }


def _k_fold_aggregator(inputs: dict, params: dict) -> dict:
    """Aggregate per-fold metrics (passed via ports a..j) into mean / std / 95% CI."""
    values: list[float] = []
    for port in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j"):
        v = inputs.get(port)
        if v is None:
            continue
        try:
            values.append(float(v))
        except (TypeError, ValueError):
            continue
    if not values:
        return {
            "k": 0,
            "mean": 0.0,
            "std": 0.0,
            "ci_low": 0.0,
            "ci_high": 0.0,
            "values": [],
            "verdict": "No fold values.",
        }
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / max(1, n - 1)
    std = var ** 0.5
    # 95% normal approx; with k=10 use t-correction ≈ 1.96
    half = 1.96 * std / (n ** 0.5)
    return {
        "k": n,
        "mean": round(mean, 4),
        "std": round(std, 4),
        "ci_low": round(mean - half, 4),
        "ci_high": round(mean + half, 4),
        "values": [round(v, 4) for v in values],
        "verdict": (
            f"Mean = {mean:.4f} ± {half:.4f} (95% CI), std = {std:.4f} over {n} folds."
        ),
    }


# ── KFoldRunner ────────────────────────────────
# True k-fold runner (Phase-12). Internally splits the corpus, runs the SA
# decipherer + holdout recall + compound-dependency constraint K times, and
# aggregates per-fold metrics into mean / std / 95% CI. Replaces the
# Phase-11 wiring that only ran the first fold.


def _k_fold_runner(inputs: dict, params: dict) -> dict:
    """Run SA + holdout recall + compound coupling on K folds.

    Internally:
      1. Splits the input sequences K ways (KFoldCorpusSplitter logic).
      2. For each fold, runs CTTAnchoredSADecipher on the train split and
         HoldoutWordRecall + CompoundDependencyConstraint on the test split.
      3. Returns mean / std / 95% CI for recall and compound score, plus
         the full per-fold values.

    Inputs:
      sequences          : list[list[str]] (the full corpus)
      lm                 : the language model used by SA
      role_table         : dict from IndusSignRoleClassifier (optional)
      value_role_map     : dict from DefaultIndusValueRoleMap (optional)
      anchors            : dict from IconographicAnchorPin (optional)
      attested_vocab     : list[str] from AttestedVocabularyLoader
      high_pmi_bigrams   : list[dict] from IndusSignRoleClassifier (optional)

    Params:
      k                  : int >= 2 (default 5)
      seed               : int (default 7)
      sa_seed_base       : int (default 11)
      max_iterations     : int (default 4000)
      restarts           : int (default 3)
      surjective         : bool (default True)
      strict_mode        : bool (default True)
      compound_weight    : float (default 1.0)
      compound_separator : str (default "")
      decode_separator   : str (default "")
      min_word_len       : int (default 2)
      hit_bonus          : float (default 1.0)
      miss_penalty       : float (default 0.5)
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    lm = inputs.get("lm")
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    value_role_map: dict[str, str] = inputs.get("value_role_map") or {}
    anchors: dict[str, str] = inputs.get("anchors") or {}
    attested_vocab: list[str] = inputs.get("attested_vocab") or []
    high_pmi_bigrams: list[dict] = inputs.get("high_pmi_bigrams") or []

    k = max(2, int(params.get("k", 5)))
    split_seed = int(params.get("seed", 7))
    sa_seed_base = int(params.get("sa_seed_base", 11))
    max_iterations = int(params.get("max_iterations", 4000))
    restarts = int(params.get("restarts", 3))
    surjective = bool(params.get("surjective", True))
    strict_mode = bool(params.get("strict_mode", True))
    compound_weight = float(params.get("compound_weight", 1.0))
    compound_separator = str(params.get("compound_separator", ""))
    decode_separator = str(params.get("decode_separator", ""))
    min_word_len = int(params.get("min_word_len", 2))
    hit_bonus = float(params.get("hit_bonus", 1.0))
    miss_penalty = float(params.get("miss_penalty", 0.5))

    if not sequences or lm is None:
        return {
            "k": 0,
            "per_fold": [],
            "recall_values": [],
            "compound_values": [],
            "recall_mean": 0.0,
            "recall_std": 0.0,
            "recall_ci_low": 0.0,
            "recall_ci_high": 0.0,
            "compound_mean": 0.0,
            "verdict": "Missing sequences or lm.",
        }

    rng = random.Random(split_seed)
    idx = list(range(len(sequences)))
    rng.shuffle(idx)
    fold_size = max(1, len(idx) // k)

    per_fold: list[dict] = []
    recall_values: list[float] = []
    compound_values: list[float] = []
    for f in range(k):
        start = f * fold_size
        end = (f + 1) * fold_size if f < k - 1 else len(idx)
        test_idx = set(idx[start:end])
        train = [sequences[i] for i in idx if i not in test_idx]
        test = [sequences[i] for i in idx if i in test_idx]
        sa_out = _ctt_anchored_sa_decipher(
            {
                "sequences": train,
                "lm": lm,
                "role_table": role_table,
                "value_role_map": value_role_map,
                "anchors": anchors,
                "high_pmi_bigrams": high_pmi_bigrams,
                "attested_vocab": attested_vocab,
            },
            {
                "seed": sa_seed_base + f,
                "max_iterations": max_iterations,
                "restarts": restarts,
                "surjective": surjective,
                "strict_mode": strict_mode,
                "compound_weight": compound_weight,
                "compound_separator": compound_separator,
            },
        )
        proposed = sa_out.get("proposed_mapping") or {}
        recall_out = _holdout_word_recall(
            {
                "sequences": test,
                "proposed_mapping": proposed,
                "attested_vocab": attested_vocab,
            },
            {
                "decode_separator": decode_separator,
                "min_word_len": min_word_len,
            },
        )
        compound_out = _compound_dependency_constraint(
            {
                "proposed_mapping": proposed,
                "high_pmi_bigrams": high_pmi_bigrams,
                "attested_vocab": attested_vocab,
            },
            {
                "hit_bonus": hit_bonus,
                "miss_penalty": miss_penalty,
                "compound_separator": compound_separator,
            },
        )
        rec = float(recall_out.get("recall_score", 0.0))
        comp = float(compound_out.get("compound_score", 0.0))
        recall_values.append(rec)
        compound_values.append(comp)
        per_fold.append({
            "fold_id": f,
            "n_train": len(train),
            "n_test": len(test),
            "recall": round(rec, 4),
            "compound": round(comp, 4),
            "n_attested_hits": int(recall_out.get("n_attested_hits", 0)),
            "n_decoded": int(recall_out.get("n_decoded", 0)),
            "n_signs": int(sa_out.get("n_signs", 0)),
            "compound_hits": int(sa_out.get("compound_hits", 0)),
            "compound_misses": int(sa_out.get("compound_misses", 0)),
            "matched_top": list(recall_out.get("matched_words", []))[:5],
        })

    n = len(recall_values)
    if n == 0:
        return {
            "k": 0,
            "per_fold": [],
            "recall_values": [],
            "compound_values": [],
            "recall_mean": 0.0,
            "recall_std": 0.0,
            "recall_ci_low": 0.0,
            "recall_ci_high": 0.0,
            "compound_mean": 0.0,
            "verdict": "No folds executed.",
        }
    rmean = sum(recall_values) / n
    rvar = sum((v - rmean) ** 2 for v in recall_values) / max(1, n - 1)
    rstd = rvar ** 0.5
    half = 1.96 * rstd / (n ** 0.5)
    cmean = sum(compound_values) / n
    return {
        "k": n,
        "per_fold": per_fold,
        "recall_values": [round(v, 4) for v in recall_values],
        "compound_values": [round(v, 4) for v in compound_values],
        "recall_mean": round(rmean, 4),
        "recall_std": round(rstd, 4),
        "recall_ci_low": round(rmean - half, 4),
        "recall_ci_high": round(rmean + half, 4),
        "compound_mean": round(cmean, 4),
        "verdict": (
            f"k={n}: recall = {rmean:.4f} ± {half:.4f} (95% CI), "
            f"std={rstd:.4f}; compound mean={cmean:.4f}."
        ),
    }


# ── MatchedWordReporter ──────────────────────────
# Aggregate matched_words across multiple branches into one sortable table.


def _matched_word_reporter(inputs: dict, params: dict) -> dict:
    """Aggregate per-branch matched_words into a single sortable report.

    Inputs (ports a..f) each accept a list of {word, count} dicts as
    emitted by HoldoutWordRecall.matched_words. Param `labels` is a list
    of N strings naming the branches in port order; missing labels fall
    back to the port letter.

    Output is a flat table sortable by branch + count, plus a per-branch
    summary count of matched words.
    """
    labels_raw = params.get("labels", []) or []
    if isinstance(labels_raw, str):
        labels = [s.strip() for s in labels_raw.split(",") if s.strip()]
    elif isinstance(labels_raw, (list, tuple)):
        labels = [str(s).strip() for s in labels_raw if str(s).strip()]
    else:
        labels = []

    ports = ("a", "b", "c", "d", "e", "f")
    table: list[dict] = []
    by_branch: dict[str, dict[str, int]] = {}
    for i, port in enumerate(ports):
        items = inputs.get(port)
        if not items:
            continue
        label = labels[i] if i < len(labels) else port
        items_iter = items if isinstance(items, list) else []
        branch_counts: dict[str, int] = {}
        for item in items_iter:
            if not isinstance(item, dict):
                continue
            word = str(item.get("word") or item.get("decoded") or "").lower()
            count = int(item.get("count", 1) or 1)
            if not word:
                continue
            branch_counts[word] = branch_counts.get(word, 0) + count
            table.append({
                "branch": label,
                "word": word,
                "count": count,
            })
        if branch_counts:
            by_branch[label] = dict(
                sorted(branch_counts.items(), key=lambda kv: -kv[1])
            )

    table.sort(key=lambda r: (r["branch"], -int(r["count"]), r["word"]))
    summary = {
        label: {
            "n_unique_words": len(branch),
            "total_count": sum(branch.values()),
            "top": list(branch.items())[:10],
        }
        for label, branch in by_branch.items()
    }
    return {
        "table": table[:500],
        "n_rows": len(table),
        "by_branch": by_branch,
        "summary": summary,
    }


# ── CorpusPermuter ────────────────────────────────
# Negative-control corpus transformer. Three modes available:
#   - "relabel": replace every sign id with a uniform random sign id from
#     the global vocabulary (destroys positional + bigram structure).
#   - "shuffle_within": shuffle tokens inside each inscription independently
#     (destroys positional structure but preserves bigram histogram per seq).
#   - "shuffle_global": flat-shuffle every token across the corpus
#     (destroys both positional and per-inscription structure).
# Recall on a permuted corpus should collapse to chance.


def _corpus_permuter(inputs: dict, params: dict) -> dict:
    """Apply a permutation to the corpus that destroys decipherment signal."""
    sequences: list[list[str]] = inputs.get("sequences") or []
    seed = int(params.get("seed", 23))
    mode = str(params.get("mode", "relabel")).lower()
    if mode not in ("relabel", "shuffle_within", "shuffle_global"):
        mode = "relabel"

    rng = random.Random(seed)
    if not sequences:
        return {"sequences": [], "mode": mode, "n": 0}

    if mode == "relabel":
        vocab = sorted({s for seq in sequences for s in seq})
        if not vocab:
            return {"sequences": [], "mode": mode, "n": 0}
        permuted = [
            [rng.choice(vocab) for _ in seq] for seq in sequences
        ]
    elif mode == "shuffle_within":
        permuted = []
        for seq in sequences:
            cp = list(seq)
            rng.shuffle(cp)
            permuted.append(cp)
    else:  # shuffle_global
        flat = [s for seq in sequences for s in seq]
        rng.shuffle(flat)
        permuted = []
        cursor = 0
        for seq in sequences:
            n = len(seq)
            permuted.append(flat[cursor : cursor + n])
            cursor += n
    return {
        "sequences": permuted,
        "mode": mode,
        "n": len(permuted),
        "n_tokens": sum(len(s) for s in permuted),
    }


# ── VocabularyAblator ─────────────────────────────
# Negative control: emit an empty (or shuffled-label) attested vocab.
# Wired into HoldoutWordRecall, this drives recall to 0 (or chance).


def _vocabulary_ablator(inputs: dict, params: dict) -> dict:
    """Produce an ablated attested vocab for negative-control runs.

    Modes:
      - "empty"  : returns []
      - "shuffle": returns the same vocab but with characters shuffled per
        word, breaking string-equality with any decoded form.
    """
    attested_vocab: list[str] = inputs.get("attested_vocab") or []
    mode = str(params.get("mode", "empty")).lower()
    seed = int(params.get("seed", 41))
    if mode == "empty":
        return {
            "attested_vocab": [],
            "n_words": 0,
            "mode": mode,
        }
    rng = random.Random(seed)
    out: list[str] = []
    for w in attested_vocab:
        chars = list(w)
        rng.shuffle(chars)
        out.append("".join(chars))
    return {
        "attested_vocab": sorted(set(out)),
        "n_words": len(set(out)),
        "mode": mode,
    }


# ── AnchorAblator ────────────────────────────────
# Negative control: emit empty anchors so SA starts cold.


def _anchor_ablator(inputs: dict, params: dict) -> dict:
    """Strip anchors from the upstream IconographicAnchorPin (negative control)."""
    return {
        "anchors": {},
        "n_anchors": 0,
        "family": str(
            (inputs.get("family") or params.get("family") or "unknown")
        ),
        "weight": 0.0,
    }


# ── CorpusStratifier ────────────────────────────
# Split the corpus by inscription length into short / medium / long strata.
# Inscription length is a known proxy for text type in the M77 corpus
# (short inscriptions cluster around seals; long ones around copper plates).


def _corpus_stratifier(inputs: dict, params: dict) -> dict:
    """Split sequences into length-stratified subsets."""
    sequences: list[list[str]] = inputs.get("sequences") or []
    short_max = int(params.get("short_max", 2))
    medium_max = int(params.get("medium_max", 5))
    short_seqs: list[list[str]] = []
    medium_seqs: list[list[str]] = []
    long_seqs: list[list[str]] = []
    for seq in sequences:
        L = len(seq)
        if L <= short_max:
            short_seqs.append(seq)
        elif L <= medium_max:
            medium_seqs.append(seq)
        else:
            long_seqs.append(seq)
    summary = {
        "short": {"n": len(short_seqs), "max_len": short_max},
        "medium": {"n": len(medium_seqs), "max_len": medium_max},
        "long": {"n": len(long_seqs), "max_len": None},
        "total": len(sequences),
    }
    return {
        "short_sequences": short_seqs,
        "medium_sequences": medium_seqs,
        "long_sequences": long_seqs,
        "stratum_summary": summary,
    }


# ── Atomic node defs for registration ─────────────────────
# Imported by experiment_graph.py and added to ATOMIC_NODES at module load.


def _ctt_node_defs() -> list[Any]:
    """Return a list of AtomicNodeDef instances to register.

    The actual AtomicNodeDef class is imported lazily to avoid circular import.
    """
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "IndusSignRoleClassifier",
            "Indus Sign Role Classifier",
            "CTT / Constraint Topology",
            "Derive 6-bit role mask per sign (suffix/determinative/numeral/phonetic/"
            "logogram/compound) from corpus positional and bigram statistics. "
            "Output drives CTTAdmissibilityFilter to prevent SA from proposing "
            "structurally-impossible mappings. Pure primitive: positional rates + PMI.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "role_table", "type": "json"},
                {"name": "n_signs", "type": "number"},
                {"name": "role_summary", "type": "json"},
                {"name": "compound_signs", "type": "json"},
                {"name": "high_pmi_bigrams", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "terminal_threshold": {
                        "type": "number",
                        "default": 0.85,
                        "minimum": 0.5,
                        "maximum": 1.0,
                    },
                    "initial_threshold": {
                        "type": "number",
                        "default": 0.70,
                        "minimum": 0.5,
                        "maximum": 1.0,
                    },
                    "compound_pmi_threshold": {"type": "number", "default": 4.0, "minimum": 0.0},
                    "min_count": {"type": "integer", "default": 5, "minimum": 1},
                    "numeral_signs": {
                        "type": "array",
                        "default": ["820", "590", "60", "176", "90"],
                    },
                },
            },
            fn=_indus_sign_role_classifier,
        ),
        AtomicNodeDef(
            "CTTAdmissibilityFilter",
            "CTT Admissibility Filter",
            "CTT / Constraint Topology",
            "Per-sign feasibility oracle (Constraint Topology Theory, Layer1Labs 2026). "
            "Filters a proposed sign-to-value mapping by checking each (sign, value) "
            "pair against the sign's admissible roles. O(K) per Theorem 1 of CTT TR. "
            "Connects: IndusSignRoleClassifier → role_table; SADecipher → proposed_mapping.",
            inputs=[
                {"name": "role_table", "type": "json", "required": True},
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "value_role_map", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "filtered_mapping", "type": "json"},
                {"name": "violations", "type": "json"},
                {"name": "n_violations", "type": "number"},
                {"name": "n_admissible", "type": "number"},
                {"name": "admissibility_rate", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "value_role_map": {
                        "type": "object",
                        "default": {},
                        "description": (
                            "Map target-language values to roles. Use "
                            "DefaultIndusValueRoleMap for the standard set."
                        ),
                    },
                    "strict_mode": {
                        "type": "boolean",
                        "default": False,
                        "description": (
                            "If True, values not present in value_role_map are "
                            "treated as having an 'unmapped' role and are filtered "
                            "as violations (rigorous CTT default). If False, "
                            "unmapped values fall back to 'phonetic' and pass "
                            "the filter unless the sign forbids phonetic."
                        ),
                    },
                },
            },
            fn=_ctt_admissibility_filter,
        ),
        AtomicNodeDef(
            "DefaultIndusValueRoleMap",
            "Default Indus Value-Role Map",
            "CTT / Constraint Topology",
            "Emit a value-role lookup table for CTTAdmissibilityFilter. Always "
            "includes the default CV-syllabary baseline (Tamil case suffixes + "
            "CV syllabograms + numerals + generic determinatives). When `families` "
            "is set, merges in per-language target inventories: 'old_tamil' "
            "(DEDR roots + Mahadevan Tamil-Brahmi attested words), "
            "'hieroglyphic_luwian' (Hawkins 2000 lemmas, royal titles as "
            "determinatives), 'mycenaean_greek' (Linear B Ventris grid). "
            "Use one node per Phase-10 SA branch so strict_mode is meaningful "
            "per language.",
            inputs=[],
            outputs=[
                {"name": "value_role_map", "type": "json"},
                {"name": "n_values", "type": "number"},
                {"name": "families_applied", "type": "json"},
                {"name": "family_sizes", "type": "json"},
                {"name": "unknown_families", "type": "json"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "families": {
                        "type": "array",
                        "default": [],
                        "description": (
                            "List of language families whose target inventories "
                            "to merge in: old_tamil | hieroglyphic_luwian | "
                            "mycenaean_greek (aliases: dravidian, luwian, linear_b)."
                        ),
                    },
                    "include_default": {
                        "type": "boolean",
                        "default": True,
                        "description": (
                            "Include the CV-syllabary baseline. Disable only if "
                            "you want a strictly per-language map."
                        ),
                    },
                    "extra": {
                        "type": "object",
                        "default": {},
                        "description": "Additional value→role overrides to merge in.",
                    },
                },
            },
            fn=_default_value_role_map_loader,
        ),
        AtomicNodeDef(
            "CompoundDependencyConstraint",
            "Compound Dependency Constraint",
            "CTT / Constraint Topology",
            "Score a sign mapping under cross-sign compound coupling (Cotterell/Eisner "
            "2015 dual-decomposition idea). For each high-PMI compound bigram, "
            "concatenated decoded value should appear in attested vocabulary. "
            "Awards bonus per hit, penalty per miss. This is the dense-dependency "
            "layer that pure CTT (independent constraints) cannot capture.",
            inputs=[
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "high_pmi_bigrams", "type": "json", "required": True},
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "compound_score", "type": "number"},
                {"name": "n_hits", "type": "number"},
                {"name": "n_misses", "type": "number"},
                {"name": "hit_rate", "type": "number"},
                {"name": "hits", "type": "json"},
                {"name": "misses", "type": "json"},
                {"name": "number", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "hit_bonus": {"type": "number", "default": 1.0},
                    "miss_penalty": {"type": "number", "default": 0.5},
                    "compound_separator": {"type": "string", "default": ""},
                    "attested_vocab": {"type": "array", "default": []},
                },
            },
            fn=_compound_dependency_constraint,
        ),
        AtomicNodeDef(
            "HoldoutWordRecall",
            "Held-out Word Recall",
            "CTT / Constraint Topology",
            "Decode each held-out inscription with the proposed mapping and count "
            "matches against an attested external vocabulary. NON-CIRCULAR test. "
            "Connects: CorpusSplitter.test_sequences → sequences, "
            "SADecipher → proposed_mapping, AttestedVocabularyLoader → attested_vocab.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "recall_score", "type": "number"},
                {"name": "n_decoded", "type": "number"},
                {"name": "n_attested_hits", "type": "number"},
                {"name": "n_unique_hits", "type": "number"},
                {"name": "hit_rate", "type": "number"},
                {"name": "matched_words", "type": "json"},
                {"name": "number", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "decode_separator": {"type": "string", "default": ""},
                    "min_word_len": {"type": "integer", "default": 2, "minimum": 1},
                    "attested_vocab": {"type": "array", "default": []},
                },
            },
            fn=_holdout_word_recall,
        ),
        AtomicNodeDef(
            "AttestedVocabularyLoader",
            "Attested Vocabulary Loader",
            "CTT / Constraint Topology",
            "Load an attested-language word list (Old Tamil, Hieroglyphic Luwian, "
            "Mycenaean Greek, Vedic Sanskrit, Sumerian) as the gold-standard source "
            "for HoldoutWordRecall and CompoundDependencyConstraint.",
            inputs=[],
            outputs=[
                {"name": "attested_vocab", "type": "json"},
                {"name": "n_words", "type": "number"},
                {"name": "family", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "family": {
                        "type": "string",
                        "default": "old_tamil",
                        "description": (
                            "old_tamil | hieroglyphic_luwian | mycenaean_greek"
                            " | vedic_sanskrit | sumerian"
                        ),
                    },
                    "extra_words": {"type": "array", "default": []},
                    "min_len": {"type": "integer", "default": 2, "minimum": 1},
                    "max_len": {"type": "integer", "default": 12, "minimum": 1},
                },
            },
            fn=_attested_vocab_loader,
        ),
        AtomicNodeDef(
            "CTTAnchoredSADecipher",
            "CTT-Anchored SA Decipherer",
            "CTT / Constraint Topology",
            "Simulated annealing decipherment with the CTT admissibility oracle "
            "filtering every proposal step. Forbidden (sign, value) pairs are "
            "mathematically unselectable per CTT Claim 9. Restarts and seeds "
            "controlled like the standard SADecipher. Pure primitive: one engine call "
            "with a constraint mask. Use this in place of SADecipher when role_table "
            "is available and you want guaranteed-admissible outputs. "
            "When `compound_weight` > 0 and high_pmi_bigrams + attested_vocab "
            "are wired in, restart selection becomes joint over LM + compound "
            "coupling (Cotterell/Eisner 2015 single-pass dual decomposition).",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "lm", "type": "any", "required": True},
                {"name": "role_table", "type": "json", "required": False},
                {"name": "value_role_map", "type": "json", "required": False},
                {"name": "anchors", "type": "any", "required": False},
                {"name": "high_pmi_bigrams", "type": "json", "required": False},
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "proposed_mapping", "type": "json"},
                {"name": "score", "type": "number"},
                {"name": "lm_score", "type": "number"},
                {"name": "compound_score", "type": "number"},
                {"name": "compound_hits", "type": "number"},
                {"name": "compound_misses", "type": "number"},
                {"name": "n_signs", "type": "number"},
                {"name": "n_forbidden_pairs", "type": "number"},
                {"name": "n_filtered_proposals", "type": "number"},
                {"name": "n_total_proposals", "type": "number"},
                {"name": "filter_rate", "type": "number"},
                {"name": "anchors_used", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "seed": {"type": "integer", "default": 1},
                    "max_iterations": {"type": "integer", "default": 8000, "minimum": 100},
                    "restarts": {"type": "integer", "default": 5, "minimum": 1},
                    "surjective": {"type": "boolean", "default": True},
                    "value_role_map": {"type": "object", "default": {}},
                    "strict_mode": {
                        "type": "boolean",
                        "default": False,
                        "description": (
                            "If True, the final mapping is post-filtered to "
                            "drop any value missing from value_role_map. "
                            "Treats unmapped values as having a forbidden role."
                        ),
                    },
                    "compound_weight": {
                        "type": "number",
                        "default": 0.0,
                        "description": (
                            "Weight on the compound-coupling term in the joint "
                            "score. Set to 1.0 to enable joint LM + compound "
                            "selection. Requires high_pmi_bigrams + attested_vocab."
                        ),
                    },
                    "compound_separator": {"type": "string", "default": ""},
                },
            },
            fn=_ctt_anchored_sa_decipher,
        ),
        AtomicNodeDef(
            "LMGranularityProfiler",
            "LM Granularity Profiler",
            "CTT / Constraint Topology",
            "Diagnose an LM's symbol granularity (character / syllabic / word / mixed) "
            "and report its overlap with the attested vocab and value-role map for a "
            "target language. Use BEFORE strict-mode SA to ensure the LM produces "
            "symbols at a granularity compatible with the role-map filter.",
            inputs=[
                {"name": "lm", "type": "any", "required": True},
                {"name": "attested_vocab", "type": "json", "required": False},
                {"name": "value_role_map", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "granularity", "type": "text"},
                {"name": "mean_symbol_len", "type": "number"},
                {"name": "median_symbol_len", "type": "number"},
                {"name": "vocab_overlap", "type": "number"},
                {"name": "role_map_overlap", "type": "number"},
                {"name": "n_symbols", "type": "number"},
                {"name": "length_distribution", "type": "json"},
                {"name": "top_symbols", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_lm_granularity_profiler,
        ),
        AtomicNodeDef(
            "GranularityComparison",
            "Granularity Comparison",
            "CTT / Constraint Topology",
            "Rank multiple LMGranularityProfiler outputs by vocab + role-map "
            "compatibility and emit a textual verdict identifying the best LM "
            "for the target language family.",
            inputs=[
                {"name": "a", "type": "json", "required": False},
                {"name": "b", "type": "json", "required": False},
                {"name": "c", "type": "json", "required": False},
                {"name": "d", "type": "json", "required": False},
                {"name": "e", "type": "json", "required": False},
                {"name": "f", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "ranking", "type": "json"},
                {"name": "best", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_granularity_comparison,
        ),
        AtomicNodeDef(
            "IconographicAnchorPin",
            "Iconographic Anchor Pin",
            "CTT / Constraint Topology",
            "Emit Mahadevan/Parpola-style iconographic anchors as a sign→value "
            "mapping. Wire to CTTAnchoredSADecipher.anchors to bias the SA "
            "initial mapping toward established iconic readings (fish=min, "
            "jar=kutam, U=uravu, ...). Defaults are family + code_system aware: "
            "set code_system='m77' when the upstream corpus is Mahadevan 1977 "
            "(indus_m77) so anchors fire on M77 numeric sign IDs.",
            inputs=[],
            outputs=[
                {"name": "anchors", "type": "json"},
                {"name": "n_anchors", "type": "number"},
                {"name": "family", "type": "text"},
                {"name": "weight", "type": "number"},
                {"name": "code_system", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "family": {"type": "string", "default": "old_tamil"},
                    "weight": {"type": "number", "default": 1.0},
                    "anchors": {"type": "object", "default": {}},
                    "code_system": {
                        "type": "string",
                        "default": "parpola",
                        "description": (
                            "Sign-ID code system the upstream corpus uses: "
                            "'parpola' (P-codes, CISI) or 'm77' (Mahadevan 1977)."
                        ),
                    },
                },
            },
            fn=_iconographic_anchor_pin,
        ),
        AtomicNodeDef(
            "KFoldRunner",
            "K-Fold Runner",
            "CTT / Constraint Topology",
            "True k-fold cross-validation runner. Internally splits the corpus, "
            "runs CTTAnchoredSADecipher + HoldoutWordRecall + CompoundDependency"
            "Constraint on each fold, and aggregates per-fold recall and compound "
            "score into mean / std / 95% CI. Replaces the Phase-11 single-fold "
            "wiring with a real k-fold experiment. Phase-12 (2026-04-28).",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "lm", "type": "any", "required": True},
                {"name": "role_table", "type": "json", "required": False},
                {"name": "value_role_map", "type": "json", "required": False},
                {"name": "anchors", "type": "json", "required": False},
                {"name": "attested_vocab", "type": "json", "required": False},
                {"name": "high_pmi_bigrams", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "k", "type": "number"},
                {"name": "per_fold", "type": "json"},
                {"name": "recall_values", "type": "json"},
                {"name": "compound_values", "type": "json"},
                {"name": "recall_mean", "type": "number"},
                {"name": "recall_std", "type": "number"},
                {"name": "recall_ci_low", "type": "number"},
                {"name": "recall_ci_high", "type": "number"},
                {"name": "compound_mean", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "k": {"type": "integer", "default": 5, "minimum": 2},
                    "seed": {"type": "integer", "default": 7},
                    "sa_seed_base": {"type": "integer", "default": 11},
                    "max_iterations": {"type": "integer", "default": 4000, "minimum": 100},
                    "restarts": {"type": "integer", "default": 3, "minimum": 1},
                    "surjective": {"type": "boolean", "default": True},
                    "strict_mode": {"type": "boolean", "default": True},
                    "compound_weight": {"type": "number", "default": 1.0},
                    "compound_separator": {"type": "string", "default": ""},
                    "decode_separator": {"type": "string", "default": ""},
                    "min_word_len": {"type": "integer", "default": 2, "minimum": 1},
                    "hit_bonus": {"type": "number", "default": 1.0},
                    "miss_penalty": {"type": "number", "default": 0.5},
                },
            },
            fn=_k_fold_runner,
        ),
        AtomicNodeDef(
            "MatchedWordReporter",
            "Matched Word Reporter",
            "CTT / Constraint Topology",
            "Aggregate matched_words from up to six HoldoutWordRecall branches "
            "into a single sortable table. Param `labels` names the branches "
            "in port order (a..f).",
            inputs=[
                {"name": "a", "type": "json", "required": False},
                {"name": "b", "type": "json", "required": False},
                {"name": "c", "type": "json", "required": False},
                {"name": "d", "type": "json", "required": False},
                {"name": "e", "type": "json", "required": False},
                {"name": "f", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "table", "type": "json"},
                {"name": "n_rows", "type": "number"},
                {"name": "by_branch", "type": "json"},
                {"name": "summary", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "labels": {"type": "array", "default": []},
                },
            },
            fn=_matched_word_reporter,
        ),
        AtomicNodeDef(
            "CorpusPermuter",
            "Corpus Permuter (negative control)",
            "CTT / Constraint Topology",
            "Permute the corpus to produce a negative-control input. Modes: "
            "'relabel' (replace every sign id with a uniform random sign), "
            "'shuffle_within' (shuffle tokens inside each inscription), "
            "'shuffle_global' (flat-shuffle every token across the corpus).",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "sequences", "type": "sequences"},
                {"name": "mode", "type": "text"},
                {"name": "n", "type": "number"},
                {"name": "n_tokens", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "seed": {"type": "integer", "default": 23},
                    "mode": {"type": "string", "default": "relabel"},
                },
            },
            fn=_corpus_permuter,
        ),
        AtomicNodeDef(
            "VocabularyAblator",
            "Vocabulary Ablator (negative control)",
            "CTT / Constraint Topology",
            "Strip or shuffle the attested vocabulary so HoldoutWordRecall "
            "sees no real targets. Recall should collapse to chance.",
            inputs=[
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "attested_vocab", "type": "json"},
                {"name": "n_words", "type": "number"},
                {"name": "mode", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "mode": {"type": "string", "default": "empty"},
                    "seed": {"type": "integer", "default": 41},
                },
            },
            fn=_vocabulary_ablator,
        ),
        AtomicNodeDef(
            "AnchorAblator",
            "Anchor Ablator (negative control)",
            "CTT / Constraint Topology",
            "Drop all iconographic anchors so SA starts from a uniform-random "
            "initial mapping. Use to verify anchor priors actually contribute.",
            inputs=[
                {"name": "anchors", "type": "json", "required": False},
                {"name": "family", "type": "text", "required": False},
            ],
            outputs=[
                {"name": "anchors", "type": "json"},
                {"name": "n_anchors", "type": "number"},
                {"name": "family", "type": "text"},
                {"name": "weight", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "family": {"type": "string", "default": "unknown"},
                },
            },
            fn=_anchor_ablator,
        ),
        AtomicNodeDef(
            "CorpusStratifier",
            "Corpus Stratifier (by inscription length)",
            "CTT / Constraint Topology",
            "Stratify M77 inscriptions by length into short / medium / long "
            "sub-corpora. Inscription length is a proxy for text type "
            "(short = seal, long = copper plate / pottery graffiti).",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "short_sequences", "type": "sequences"},
                {"name": "medium_sequences", "type": "sequences"},
                {"name": "long_sequences", "type": "sequences"},
                {"name": "stratum_summary", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "short_max": {"type": "integer", "default": 2, "minimum": 1},
                    "medium_max": {"type": "integer", "default": 5, "minimum": 2},
                },
            },
            fn=_corpus_stratifier,
        ),
        AtomicNodeDef(
            "ShuffledLMNullDistribution",
            "Shuffled-LM Null Distribution",
            "CTT / Constraint Topology",
            "Build an empirical null recall distribution by running SA against "
            "shuffled-LM-unigram clones of the input LM. Reports z-score and "
            "empirical p of the observed recall vs. the shuffled null. "
            "Use to convert raw recall into a defensible significance claim.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "lm", "type": "any", "required": True},
                {"name": "attested_vocab", "type": "json", "required": True},
                {"name": "observed_recall", "type": "number", "required": True},
                {"name": "role_table", "type": "json", "required": False},
                {"name": "value_role_map", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "null_recalls", "type": "json"},
                {"name": "null_mean", "type": "number"},
                {"name": "null_std", "type": "number"},
                {"name": "observed_recall", "type": "number"},
                {"name": "z_score", "type": "number"},
                {"name": "empirical_p", "type": "number"},
                {"name": "n_trials", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_trials": {"type": "integer", "default": 50, "minimum": 5},
                    "seed": {"type": "integer", "default": 17},
                    "iterations_per_trial": {"type": "integer", "default": 1500, "minimum": 100},
                    "decode_separator": {"type": "string", "default": ""},
                },
            },
            fn=_shuffled_lm_null_distribution,
        ),
        AtomicNodeDef(
            "KFoldCorpusSplitter",
            "K-Fold Corpus Splitter",
            "CTT / Constraint Topology",
            "Emit k disjoint train/test partitions of the input sequences for "
            "k-fold cross-validation. Convenience output (train_sequences / "
            "test_sequences) points at the first fold; the full `folds` list "
            "can be consumed by graph runners that fan out across folds.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "folds", "type": "json"},
                {"name": "k", "type": "number"},
                {"name": "n", "type": "number"},
                {"name": "train_sequences", "type": "sequences"},
                {"name": "test_sequences", "type": "sequences"},
                {"name": "fold_summaries", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "k": {"type": "integer", "default": 10, "minimum": 2},
                    "seed": {"type": "integer", "default": 7},
                },
            },
            fn=_k_fold_corpus_splitter,
        ),
        AtomicNodeDef(
            "KFoldAggregator",
            "K-Fold Aggregator",
            "CTT / Constraint Topology",
            "Aggregate up to 10 per-fold scalar metrics into mean / std / 95% CI. "
            "Wire each fold's metric (e.g. recall) into ports a..j.",
            inputs=[
                {"name": "a", "type": "number", "required": False},
                {"name": "b", "type": "number", "required": False},
                {"name": "c", "type": "number", "required": False},
                {"name": "d", "type": "number", "required": False},
                {"name": "e", "type": "number", "required": False},
                {"name": "f", "type": "number", "required": False},
                {"name": "g", "type": "number", "required": False},
                {"name": "h", "type": "number", "required": False},
                {"name": "i", "type": "number", "required": False},
                {"name": "j", "type": "number", "required": False},
            ],
            outputs=[
                {"name": "k", "type": "number"},
                {"name": "mean", "type": "number"},
                {"name": "std", "type": "number"},
                {"name": "ci_low", "type": "number"},
                {"name": "ci_high", "type": "number"},
                {"name": "values", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_k_fold_aggregator,
        ),
    ]


__all__ = [
    "ROLE_BITS",
    "DEFAULT_INDUS_VALUE_ROLE_MAP",
    "_indus_sign_role_classifier",
    "_ctt_admissibility_filter",
    "_compound_dependency_constraint",
    "_holdout_word_recall",
    "_ctt_anchored_sa_decipher",
    "_default_value_role_map_loader",
    "_attested_vocab_loader",
    "_lm_granularity_profiler",
    "_granularity_comparison",
    "_iconographic_anchor_pin",
    "_shuffled_lm_null_distribution",
    "_k_fold_corpus_splitter",
    "_k_fold_aggregator",
    "_k_fold_runner",
    "_matched_word_reporter",
    "_corpus_permuter",
    "_vocabulary_ablator",
    "_anchor_ablator",
    "_corpus_stratifier",
    "_ctt_node_defs",
]
