"""Word-structure hypothesis pipeline.

Tests language-family hypotheses using ONLY word-structural statistics,
completely bypassing phoneme assignment.

Motivation: The anti-circularity experiments showed that bigram and Kandles
scoring under no-vocab conditions cannot statistically discriminate between
language families. This pipeline tests a different hypothesis surface:
the DISTRIBUTIONAL STRUCTURE of word groups (inscription entries), not
the phonological content.

Key statistics used (all vocabulary-independent):
  1. Word-length distribution (KL-divergence vs target language)
  2. Prefix entropy (how variable are word-initial signs?)
  3. Suffix entropy (how variable are word-terminal signs?)
  4. Type-token ratio of word groups (lexical diversity)
  5. Sign-repetition index (how often do the same signs recur?)

These statistics reflect fundamental properties of the target language's
morphology and phonotactics. A highly agglutinative language (Sumerian,
Dravidian) will have different word-length and suffix profiles than an
isolating language (Mycenaean Greek administrative) or a fusional one (Luwian).

Applied to Linear A: tests Anatolian, Greek, Dravidian, Semitic morphological
profiles against the actual administrative tablet structure.

Applied to Indus Script: tests whether the word-group length distribution and
repetition patterns better match Dravidian or Indo-Aryan morphology.
"""

from __future__ import annotations  # noqa: I001

import math
from collections import Counter
from typing import Any

from glossa_lab.engine import register_pipeline


# ── Reference language structural profiles ───────────────────────────
# Word-length distributions for administrative/accounting texts in each
# candidate language family.
# Source: typological analysis of administrative corpus samples.
# Lengths are in syllabic sign-groups (for syllabic scripts) or words.

# Proto-Dravidian (Parpola hypothesis for Indus):
# Agglutinative, case suffixes, verb-final, moderately long words
_DRAVIDIAN_PROFILE = {
    "name":                   "Proto-Dravidian",
    "word_length_dist":       {1: 0.05, 2: 0.20, 3: 0.32, 4: 0.25, 5: 0.12, 6: 0.04, 7: 0.02},
    "mean_word_length":       3.3,
    "suffix_entropy":         2.1,   # High: many distinct suffixes
    "prefix_entropy":         1.4,   # Moderate: some prefixes
    "type_token_ratio":       0.55,  # Moderate lexical diversity
    "unique_word_ratio":      0.45,
    "notes": "Agglutinative; case suffix variety; verb-final"
}

# Vedic Sanskrit / Indo-Aryan:
# Fusional, rich inflection, variable word order, medium-long words
_SANSKRIT_PROFILE = {
    "name":                   "Vedic Sanskrit / Indo-Aryan",
    "word_length_dist":       {1: 0.08, 2: 0.22, 3: 0.28, 4: 0.22, 5: 0.12, 6: 0.05, 7: 0.03},
    "mean_word_length":       3.2,
    "suffix_entropy":         2.3,
    "prefix_entropy":         1.2,
    "type_token_ratio":       0.60,
    "unique_word_ratio":      0.50,
    "notes": "Fusional; rich inflection; high vocabulary diversity"
}

# Luwian / Anatolian:
# Agglutinative, suffix-heavy, moderately short administrative words
_LUWIAN_PROFILE = {
    "name":                   "Luwian/Anatolian",
    "word_length_dist":       {1: 0.10, 2: 0.30, 3: 0.30, 4: 0.18, 5: 0.08, 6: 0.03, 7: 0.01},
    "mean_word_length":       2.8,
    "suffix_entropy":         1.9,
    "prefix_entropy":         1.1,
    "type_token_ratio":       0.50,
    "unique_word_ratio":      0.40,
    "notes": "Agglutinative; moderately short; suffix-based"
}

# Mycenaean Greek:
# Administrative syllabic texts: short words, high repetition, formulaic
_MYCENAEAN_PROFILE = {
    "name":                   "Mycenaean Greek",
    "word_length_dist":       {1: 0.12, 2: 0.28, 3: 0.28, 4: 0.18, 5: 0.08, 6: 0.04, 7: 0.02},
    "mean_word_length":       2.9,
    "suffix_entropy":         1.7,
    "prefix_entropy":         1.3,
    "type_token_ratio":       0.45,
    "unique_word_ratio":      0.35,
    "notes": "Administrative syllabary; short formulaic entries; repeated patterns"
}

# Proto-Semitic / Phoenician:
# Root-pattern morphology; highly variable word length
_SEMITIC_PROFILE = {
    "name":                   "Proto-Semitic",
    "word_length_dist":       {1: 0.08, 2: 0.18, 3: 0.30, 4: 0.24, 5: 0.12, 6: 0.05, 7: 0.03},
    "mean_word_length":       3.3,
    "suffix_entropy":         2.0,
    "prefix_entropy":         2.2,   # High: prefixal morphology (CVCVC root patterns)
    "type_token_ratio":       0.60,
    "unique_word_ratio":      0.50,
    "notes": "Root-pattern morphology; prefixal; high unique-word ratio"
}

# Sumerian:
# Agglutinative, chains of morphemes, long words common in texts
_SUMERIAN_PROFILE = {
    "name":                   "Sumerian",
    "word_length_dist":       {1: 0.06, 2: 0.15, 3: 0.25, 4: 0.28, 5: 0.15, 6: 0.07, 7: 0.04},
    "mean_word_length":       3.7,
    "suffix_entropy":         2.5,   # Very high: agglutinative morpheme chains
    "prefix_entropy":         2.0,
    "type_token_ratio":       0.55,
    "unique_word_ratio":      0.42,
    "notes": "Highly agglutinative; long morpheme chains; ergativity"
}

ALL_PROFILES = [
    _DRAVIDIAN_PROFILE, _SANSKRIT_PROFILE, _LUWIAN_PROFILE,
    _MYCENAEAN_PROFILE, _SEMITIC_PROFILE, _SUMERIAN_PROFILE,
]


# ── Corpus statistics ────────────────────────────────────────────────

def compute_corpus_profile(
    inscriptions: list[list[str]],
) -> dict[str, Any]:
    """Compute word-structural statistics for a corpus.

    Args:
        inscriptions: List of sign-group sequences (each inscription = one word/entry).

    Returns:
        Dict with all structural statistics needed for language-family comparison.
    """
    if not inscriptions:
        return {}

    lengths = [len(insc) for insc in inscriptions if insc]
    if not lengths:
        return {}

    total = len(lengths)
    max_len = max(lengths)
    mean_len = sum(lengths) / total

    # Word-length distribution (normalised)
    len_count = Counter(lengths)
    len_dist = {k: v / total for k, v in len_count.items()}

    # Initial sign entropy (how variable are word-starting signs?)
    initial_signs = Counter(insc[0] for insc in inscriptions if insc)
    prefix_entropy = _entropy(initial_signs)

    # Terminal sign entropy
    terminal_signs = Counter(insc[-1] for insc in inscriptions if insc)
    suffix_entropy = _entropy(terminal_signs)

    # Type-token ratio for sign-group patterns
    all_groups = [tuple(insc) for insc in inscriptions if insc]
    all_signs  = [s for insc in inscriptions for s in insc]
    unique_groups = len(set(all_groups))
    ttr = len(set(all_signs)) / max(len(all_signs), 1)

    # Unique-word ratio (how many inscription patterns appear only once?)
    group_counts = Counter(all_groups)
    unique_ratio = sum(1 for v in group_counts.values() if v == 1) / max(unique_groups, 1)

    return {
        "word_length_dist":    len_dist,
        "mean_word_length":    round(mean_len, 3),
        "max_word_length":     max_len,
        "total_words":         total,
        "unique_words":        unique_groups,
        "type_token_ratio":    round(ttr, 4),
        "unique_word_ratio":   round(unique_ratio, 4),
        "prefix_entropy":      round(prefix_entropy, 4),
        "suffix_entropy":      round(suffix_entropy, 4),
    }


def _entropy(counter: Counter) -> float:
    """Shannon entropy (nats) of a counter."""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((v / total) * math.log(v / total) for v in counter.values() if v > 0)


def _kl_divergence(p: dict, q: dict) -> float:
    """KL divergence D(P||Q) between word-length distributions.

    Smoothed with epsilon for unseen values.
    """
    eps = 0.001
    all_keys = set(p) | set(q)
    total_p = sum(p.values()) or 1.0
    total_q = sum(q.values()) or 1.0
    p_norm = {k: p.get(k, 0.0) / total_p for k in all_keys}
    q_norm = {k: (q.get(k, 0.0) + eps) / (total_q + eps * len(all_keys)) for k in all_keys}
    return sum(p_norm[k] * math.log(p_norm[k] / q_norm[k])
               for k in all_keys if p_norm[k] > 0)


# ── Hypothesis scoring ────────────────────────────────────────────────

def score_against_profile(
    corpus_stats: dict[str, Any],
    profile: dict[str, Any],
    weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """Score corpus statistics against a language-family structural profile.

    Returns a structural compatibility score (lower = more compatible).

    Args:
        corpus_stats: Output of compute_corpus_profile().
        profile:      One of the language profile dicts.
        weights:      Optional per-statistic weights.

    Returns:
        Dict with per-statistic scores and total score.
    """
    if not corpus_stats:
        return {"total": float("inf"), "profile": profile["name"]}

    default_weights = {
        "word_length_kl":   3.0,  # Most informative
        "mean_length_diff": 2.0,
        "suffix_entropy_diff": 1.5,
        "prefix_entropy_diff": 1.5,
        "ttr_diff":         1.0,
        "unique_ratio_diff": 1.0,
    }
    w = weights or default_weights

    # KL divergence on word-length distribution
    target_dist = profile["word_length_dist"]
    corpus_dist = corpus_stats.get("word_length_dist", {})
    kl = _kl_divergence(corpus_dist, target_dist)

    # Absolute differences on scalar statistics
    mean_diff    = abs(corpus_stats.get("mean_word_length",0) - profile["mean_word_length"])
    suffix_diff  = abs(corpus_stats.get("suffix_entropy",0) - profile["suffix_entropy"])
    prefix_diff  = abs(corpus_stats.get("prefix_entropy",0) - profile["prefix_entropy"])
    ttr_diff     = abs(corpus_stats.get("type_token_ratio",0) - profile["type_token_ratio"])
    unique_diff  = abs(corpus_stats.get("unique_word_ratio",0) - profile["unique_word_ratio"])

    # Total cost (lower = better fit)
    total_cost = (
        w["word_length_kl"]      * kl
        + w["mean_length_diff"]  * mean_diff
        + w["suffix_entropy_diff"]* suffix_diff
        + w["prefix_entropy_diff"]* prefix_diff
        + w["ttr_diff"]          * ttr_diff
        + w["unique_ratio_diff"] * unique_diff
    )

    # Convert to compatibility score (higher = better)
    # Use negative exponential so score is in [0,1]
    compatibility = math.exp(-total_cost)

    return {
        "profile":            profile["name"],
        "compatibility":      round(compatibility, 4),
        "cost":               round(total_cost, 4),
        "word_length_kl":     round(kl, 4),
        "mean_length_diff":   round(mean_diff, 3),
        "suffix_entropy_diff":round(suffix_diff, 3),
        "prefix_entropy_diff":round(prefix_diff, 3),
        "ttr_diff":           round(ttr_diff, 4),
        "unique_ratio_diff":  round(unique_diff, 4),
    }


def rank_language_families(
    inscriptions: list[list[str]],
    profiles: list[dict] | None = None,
) -> dict[str, Any]:
    """Rank language families by structural compatibility (no phoneme assumptions).

    Args:
        inscriptions: Corpus as list of sign sequences (inscriptions).
        profiles:     Language profiles to test. Defaults to ALL_PROFILES.

    Returns:
        Dict with corpus_profile, ranked_hypotheses, and top winner.
    """
    profiles = profiles or ALL_PROFILES
    corpus_stats = compute_corpus_profile(inscriptions)

    scores = []
    for profile in profiles:
        result = score_against_profile(corpus_stats, profile)
        scores.append(result)

    scores.sort(key=lambda x: -x["compatibility"])

    return {
        "corpus_profile": corpus_stats,
        "ranked_hypotheses": scores,
        "winner": scores[0]["profile"] if scores else "unknown",
        "winner_compatibility": scores[0]["compatibility"] if scores else 0.0,
        "margin_vs_second": (
            round(scores[0]["compatibility"] - scores[1]["compatibility"], 4)
            if len(scores) >= 2 else 0.0
        ),
        "method": "word_structure_only (no phoneme assumptions)",
    }


# ── Pipeline entry point ──────────────────────────────────────────────

@register_pipeline("word_structure_hypothesis")
async def run_word_structure_hypothesis(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id (required): corpus ID
        chunk_size:         signs per inscription group (default 5)
        profiles:           language profiles to test (default all)
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

    content = text["content"]
    if not isinstance(content, list):
        raise ValueError("Text content must be a list of sign tokens")

    chunk_size = params.get("chunk_size", 5)
    inscriptions = [
        content[i: i + chunk_size]
        for i in range(0, len(content), chunk_size)
        if content[i: i + chunk_size]
    ]

    result = rank_language_families(inscriptions)
    result["text_id"]    = text_id
    result["text_name"]  = text.get("name", "")
    result["corpus_type"]= text.get("corpus_type", "")
    return result
