"""Probabilistic sign function estimator.

Assigns probability distributions over functional types to each sign in a
corpus, without assuming any knowledge of the language.

THE CENTRAL QUESTION FOR INDUS:
  "How many of the ~400 Indus signs are phonetic (syllabograms) vs
   logographic vs determinatives?  What fraction encode sound?"

This question is critical because:
  - If most signs are phonetic → the script is primarily a syllabary,
    total sound-sign count may be 40-80, rest are logograms/determinatives
  - If most signs are logograms → a Sumerian-type system, most signs
    encode meaning, far fewer encode sound
  - This determines which decipherment strategy is appropriate

FUNCTIONAL TYPE DEFINITIONS:
  numeral         : Signs encoding quantities (strokes, circles, fractions).
                    Appear in specific positions relative to commodity signs.
                    High frequency, appear before/after object signs.
  determinative   : Silent semantic classifiers. Appear in consistent
                    positional relationships (always before or always after
                    a semantic cluster). Never appear alone. Strong boundary bias.
  logogram        : One sign = one morpheme/word. Can appear alone (isolation
                    rate > 0.3). Tend to be high frequency for common words.
  phonetic        : Encode sound (phonemes, syllables, consonants). Appear in
                    varied positions, many bigram partners, lower boundary bias.
  boundary_marker : Phrase-boundary or text-section markers. Appear at
                    inscription edges with very high regularity.

ALGORITHM:
  For each sign, compute a feature vector:
    f1: isolation_rate          — appears alone in X% of occurrences
    f2: initial_rate            — appears at inscription start
    f3: terminal_rate           — appears at inscription end
    f4: boundary_bias           — f2 + f3 (total edge concentration)
    f5: log_frequency           — log of total count (normalized)
    f6: bigram_diversity        — number of distinct left + right neighbors
    f7: positional_entropy      — entropy of positional distribution
    f8: same_context_rate       — appears in same contexts as other signs
    f9: polyvalence_score       — bimodality of positional distribution

  Then apply a scoring function calibrated against known signs in
  deciphered scripts (Linear B and Ugaritic).

CROSS-VALIDATION (Linear B ground truth):
  Linear B logograms: *100 (VIR man), *105 (FEMINA woman), *120 (wheat)…
    Expected: high isolation_rate, high frequency, moderate boundary_bias
  Linear B phonetics: a, e, i, o, u, da, de, di…
    Expected: low isolation_rate, moderate frequency, diverse contexts
  Ugaritic determinatives: none (abjad has no determinatives)
    → Ugaritic should show near-zero determinative scores

USAGE:
    from glossa_lab.pipelines.sign_function_estimator import estimate_sign_functions
    result = estimate_sign_functions(inscriptions)
    # result['signs']: list of dicts with P(numeral), P(logogram), etc.
    # result['system_summary']: estimated fraction of each type
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline  # noqa: I001

# ── Feature extraction ─────────────────────────────────────────────────


def _extract_features(
    inscriptions: list[list[str]],
    flat: list[str],
) -> dict[str, dict[str, float]]:
    """Compute the 9-feature vector for each sign.

    Returns dict mapping sign → feature dict.
    """
    freq: Counter[str] = Counter(flat)

    initial_c: Counter[str] = Counter()
    terminal_c: Counter[str] = Counter()
    alone_c: Counter[str] = Counter()
    insc_c: Counter[str] = Counter()  # inscriptions containing this sign

    # Left and right neighbors
    left_nbrs: dict[str, set[str]] = defaultdict(set)
    right_nbrs: dict[str, set[str]] = defaultdict(set)

    for insc in inscriptions:
        if not insc:
            continue
        seen_in_insc: set[str] = set()
        for sign in insc:
            seen_in_insc.add(sign)
        for sign in seen_in_insc:
            insc_c[sign] += 1
        if len(insc) == 1:
            alone_c[insc[0]] += 1
        else:
            initial_c[insc[0]] += 1
            terminal_c[insc[-1]] += 1

        for i, sign in enumerate(insc):
            if i > 0:
                left_nbrs[sign].add(insc[i - 1])
            if i < len(insc) - 1:
                right_nbrs[sign].add(insc[i + 1])

    # Positional entropy
    from glossa_lab.pipelines.sign_polyvalence import (
        _fractional_positions,
        _positional_histogram,
    )

    frac_pos = _fractional_positions(inscriptions)
    pos_entropy: dict[str, float] = {}
    bins = 10
    ln_bins = math.log(bins)
    for sign, positions in frac_pos.items():
        if len(positions) < 2:
            pos_entropy[sign] = 0.5
            continue
        hist = _positional_histogram(positions, bins)
        pe = -sum(p * math.log(p) for p in hist if p > 0) / ln_bins
        pos_entropy[sign] = pe

    # Polyvalence score
    from glossa_lab.pipelines.sign_polyvalence import (
        _bimodality_score,
        _detect_peaks,
    )

    poly_score: dict[str, float] = {}
    for sign, positions in frac_pos.items():
        if len(positions) < 3:
            poly_score[sign] = 0.0
            continue
        hist = _positional_histogram(positions, bins)
        peaks = _detect_peaks(hist, min_prominence=0.05)
        poly_score[sign] = _bimodality_score(peaks, hist)

    # Build feature vectors
    log_max = math.log(max(freq.values())) if freq else 1.0
    features: dict[str, dict[str, float]] = {}

    for sign, count in freq.items():
        occ = max(insc_c.get(sign, 1), 1)
        isolation = alone_c.get(sign, 0) / occ
        init_rate = initial_c.get(sign, 0) / occ
        term_rate = terminal_c.get(sign, 0) / occ
        boundary = init_rate + term_rate
        log_freq = math.log(count) / log_max if log_max > 0 else 0.0
        bigram_div = (len(left_nbrs.get(sign, set())) + len(right_nbrs.get(sign, set()))) / max(
            2 * (count**0.5), 1
        )
        pos_ent = pos_entropy.get(sign, 0.5)
        # "same context rate" = fraction of inscriptions where this sign
        # co-occurs with the most frequent sign (proxy for semantic grouping)
        most_freq_sign = freq.most_common(1)[0][0]
        same_ctx = sum(1 for insc in inscriptions if sign in insc and most_freq_sign in insc) / max(
            insc_c.get(sign, 1), 1
        )
        poly = min(poly_score.get(sign, 0.0), 1.0)

        features[sign] = {
            "isolation_rate": round(isolation, 4),
            "initial_rate": round(init_rate, 4),
            "terminal_rate": round(term_rate, 4),
            "boundary_bias": round(boundary, 4),
            "log_frequency": round(log_freq, 4),
            "bigram_diversity": round(min(bigram_div, 1.0), 4),
            "positional_entropy": round(pos_ent, 4),
            "same_context_rate": round(same_ctx, 4),
            "polyvalence_score": round(poly, 4),
        }

    return features


# ── Probability scoring functions ──────────────────────────────────────
# These scoring functions are calibrated heuristics based on patterns
# observed in deciphered scripts (Linear B, Ugaritic, Sumerian).
# Each outputs a raw score in [0,∞]; these are normalized to probabilities.


def _score_numeral(f: dict[str, float]) -> float:
    """Numerals: high frequency, very specific positional context, low diversity."""
    score = 0.0
    # Very high frequency sign
    if f["log_frequency"] > 0.80:
        score += 0.4
    # Low bigram diversity (only appears with commodity signs)
    if f["bigram_diversity"] < 0.20:
        score += 0.3
    # Moderate boundary bias (often at end, tallying counts)
    if 0.2 < f["boundary_bias"] < 0.8:
        score += 0.2
    # Rarely appears alone
    if f["isolation_rate"] < 0.05:
        score += 0.1
    return score


def _score_determinative(f: dict[str, float]) -> float:
    """Determinatives: STRONG positional bias, never alone, modest frequency."""
    score = 0.0
    # Very strong initial or terminal bias (>0.7 on one side)
    if f["initial_rate"] > 0.70 or f["terminal_rate"] > 0.70:
        score += 0.5
    # Never appears alone
    if f["isolation_rate"] < 0.02:
        score += 0.2
    # Not the most common sign (determinatives are moderately frequent)
    if 0.2 < f["log_frequency"] < 0.85:
        score += 0.2
    # Low positional entropy (appears in very specific positions)
    if f["positional_entropy"] < 0.35:
        score += 0.1
    return score


def _score_logogram(f: dict[str, float]) -> float:
    """Logograms: can appear alone, high frequency, moderate position variety."""
    score = 0.0
    # Can appear alone (word = one sign)
    if f["isolation_rate"] > 0.15:
        score += 0.4
    # High or moderate frequency (common words)
    if f["log_frequency"] > 0.50:
        score += 0.2
    # Not strongly tied to one position
    if 0.30 < f["positional_entropy"] < 0.75:
        score += 0.2
    # Moderate bigram diversity (appears with varied neighbors but not hugely)
    if 0.15 < f["bigram_diversity"] < 0.60:
        score += 0.2
    return score


def _score_phonetic(f: dict[str, float]) -> float:
    """Phonetic signs (syllabograms/letters): diverse contexts, medial position."""
    score = 0.0
    # Low boundary bias (appears throughout words)
    if f["boundary_bias"] < 0.35:
        score += 0.3
    # High bigram diversity (appears with many different neighbors)
    if f["bigram_diversity"] > 0.40:
        score += 0.3
    # High positional entropy (not stuck at one position)
    if f["positional_entropy"] > 0.55:
        score += 0.2
    # Rarely appears alone
    if f["isolation_rate"] < 0.05:
        score += 0.2
    return score


def _score_boundary_marker(f: dict[str, float]) -> float:
    """Boundary markers: extreme boundary bias, appears in nearly all inscriptions."""
    score = 0.0
    # Extremely high boundary bias (>1.2 = appears at both ends)
    if f["boundary_bias"] > 1.2:
        score += 0.5
    # High frequency (appears in most inscriptions)
    if f["log_frequency"] > 0.70:
        score += 0.3
    # Bimodal positional distribution (initial AND terminal)
    if f["polyvalence_score"] > 0.15:
        score += 0.2
    return score


def _normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Convert raw scores to a probability distribution."""
    total = sum(scores.values())
    if total <= 0:
        n = len(scores)
        return {k: 1.0 / n for k in scores}
    return {k: round(v / total, 4) for k, v in scores.items()}


# ── Main estimator ─────────────────────────────────────────────────────


def estimate_sign_functions(
    inscriptions: list[list[str]],
    min_freq: int = 3,
) -> dict[str, Any]:
    """Estimate functional type probabilities for each sign in a corpus.

    Args:
        inscriptions: List of inscriptions, each a list of sign strings.
        min_freq:     Minimum occurrences required to classify a sign.

    Returns:
        dict with:
            signs:         List of per-sign classification dicts
            system_summary: Estimated fraction of each type across corpus
            high_confidence: Signs with P(type) > 0.6 for some type
            likely_phonetics: Signs most likely to be phonetic
            likely_determinatives: Signs most likely to be determinatives
    """
    flat = [s for insc in inscriptions for s in insc]
    freq: Counter[str] = Counter(flat)
    features = _extract_features(inscriptions, flat)

    signs: list[dict[str, Any]] = []
    type_accumulator: Counter[str] = Counter()

    for sign, feats in sorted(features.items()):
        if freq[sign] < min_freq:
            continue

        raw = {
            "numeral": _score_numeral(feats),
            "determinative": _score_determinative(feats),
            "logogram": _score_logogram(feats),
            "phonetic": _score_phonetic(feats),
            "boundary_marker": _score_boundary_marker(feats),
        }
        probs = _normalize_scores(raw)
        dominant_type = max(probs, key=lambda k: probs[k])
        confidence = probs[dominant_type]

        type_accumulator[dominant_type] += 1

        entry: dict[str, Any] = {
            "sign": sign,
            "frequency": freq[sign],
            "dominant_type": dominant_type,
            "confidence": confidence,
            "probabilities": probs,
            "features": {k: round(v, 3) for k, v in feats.items()},
        }
        signs.append(entry)

    signs.sort(key=lambda s: s["confidence"], reverse=True)

    total_classified = sum(type_accumulator.values()) or 1
    system_summary = {t: round(c / total_classified, 3) for t, c in type_accumulator.most_common()}

    high_confidence = [s for s in signs if s["confidence"] >= 0.60]
    likely_phonetics = sorted(
        [s for s in signs if s["dominant_type"] == "phonetic"],
        key=lambda s: s["probabilities"]["phonetic"],
        reverse=True,
    )
    likely_determinatives = sorted(
        [s for s in signs if s["dominant_type"] == "determinative"],
        key=lambda s: s["probabilities"]["determinative"],
        reverse=True,
    )
    likely_numerals = sorted(
        [s for s in signs if s["dominant_type"] == "numeral"],
        key=lambda s: s["probabilities"]["numeral"],
        reverse=True,
    )

    # Estimated phonetic sign inventory (for a syllabary: usually 40-90 unique CV values)
    phonetic_count = type_accumulator.get("phonetic", 0)

    return {
        "total_signs_classified": total_classified,
        "signs": signs,
        "system_summary": system_summary,
        "type_counts": dict(type_accumulator),
        "phonetic_inventory_estimate": phonetic_count,
        "high_confidence": high_confidence[:20],
        "likely_phonetics": likely_phonetics[:20],
        "likely_determinatives": likely_determinatives[:10],
        "likely_numerals": likely_numerals[:10],
        "interpretation": _interpret(system_summary, phonetic_count, total_classified),
    }


def _interpret(
    summary: dict[str, float],
    phonetic_count: int,
    total: int,
) -> str:
    """Generate a one-paragraph interpretation of the sign function distribution."""
    pho_frac = summary.get("phonetic", 0)
    det_frac = summary.get("determinative", 0)
    log_frac = summary.get("logogram", 0)
    num_frac = summary.get("numeral", 0)

    if pho_frac >= 0.50:
        base = (
            f"The corpus is dominated by phonetic signs ({pho_frac:.0%}). "
            f"This profile resembles an abjad or syllabary. "
            f"Estimated phonetic sign inventory: ~{phonetic_count} signs."
        )
    elif log_frac >= 0.40:
        base = (
            f"Logograms dominate ({log_frac:.0%}). "
            f"This profile resembles a logo-syllabic system (Sumerian/Egyptian). "
            f"Only ~{phonetic_count}/{total} signs are likely phonetic."
        )
    else:
        base = (
            f"Mixed sign functions: phonetic {pho_frac:.0%}, "
            f"logographic {log_frac:.0%}, determinatives {det_frac:.0%}. "
            f"Consistent with a logo-syllabic system."
        )

    if det_frac > 0.10:
        base += (
            f" A significant determinative component ({det_frac:.0%}) "
            f"suggests semantic classification markers — a key feature of "
            f"Sumerian and Egyptian but not of Northwest Semitic abjads."
        )
    if num_frac > 0.05:
        base += (
            f" Numeral signs ({num_frac:.0%}) are identifiable by their "
            f"specific distributional context."
        )
    return base


# ── Pipeline entry point ──────────────────────────────────────────────


@register_pipeline("sign_function_estimator")
async def run_sign_function_estimator(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id:   corpus to analyze
        min_freq:  minimum sign frequency (default 3)
    """
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    content = text.get("content", [])
    if content and isinstance(content[0], list):
        inscriptions = content
    else:
        inscriptions = [content]

    result = estimate_sign_functions(
        inscriptions,
        min_freq=params.get("min_freq", 3),
    )
    result["text_id"] = text_id
    result["text_name"] = text.get("name", text_id)
    return result
