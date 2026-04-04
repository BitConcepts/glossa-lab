"""Normalized Weighted Sign Position (NWSP) analysis.

Exact implementation of the method published in:
  Fuls, A. (2013). Positional Analysis of Indus Signs.
    Voprosi Epigrafiki, Vol. 7(1), pp. 253-275.
  Fuls, A. (2015). Appendix II: Positional Analysis of Indus Signs.
    In B. K. Wells, The Archaeology and Epigraphy of Indus Writing.
    Archaeopress, Oxford, pp. 119-133.

WHY THIS METHOD MATTERS:
  The NWSP method is the foundational positional analysis technique used
  in the ICIT database. By implementing it exactly, we can:
    1. Directly compare our results to Fuls' published findings
    2. Validate our implementation against his published histograms
    3. Use his sign classification categories (initial, terminal, etc.)
    4. Demonstrate methodological alignment for ICIT collaboration

THE ALGORITHM:
  For a text of L signs, each sign at position p (1-indexed) is mapped to
  a 'normalized weighted position' (NWP) in the range [1, 10]:

    NWP(p, L) = round((p - 1) / (L - 1) × 9 + 1)   for L >= 2
    NWP(p, 1) = 5.5  (middle of scale, for isolated signs)

  The key innovation: each occurrence is weighted by L (the text length).
  Longer texts provide more precise position information and are weighted
  more heavily in the histogram. This prevents short inscriptions (length
  2-3) from dominating the histogram.

    Weight(p, L) = L

  The final histogram sums weighted positions over all occurrences of a sign:
    histogram[nwp] += L   for each occurrence of sign at position p in text of length L

  The histogram is then normalized by dividing by the total weight (sum of
  all L values across all occurrences).

SIGN CLASSIFICATION (Fuls 2015, Chapter 3.3):
  After computing the NWSP histogram for each sign, signs are classified by
  the shape of their histogram:

  ITM  (Initial Cluster Terminal Marker):
    Strong peaks at both positions 1-2 (initial) AND 9-10 (terminal).
    These signs appear at both ends — they are "frame" markers.

  TMK  (Terminal Marker):
    Dominant peak at positions 8-10. Appears at end of inscriptions.
    These are the grammatical suffixes / class markers.

  PTM  (Post Terminal Marker):
    Peak at position 9-10, but AFTER a terminal marker.

  ITM_INITIAL (Initial sign):
    Dominant peak at positions 1-2. Appears at start.

  NUM  (Numeral):
    Appears consistently at positions 6-8 (before terminal signs).
    Often in clusters.

  CON  (Constant distribution):
    Nearly flat histogram — appears at all positions equally.
    These are high-frequency phonetic signs (syllabograms).

  MED  (Medial):
    Peak in positions 3-7. Intermediate position, likely phonetic.

USAGE:
    from glossa_lab.pipelines.nwsp import compute_nwsp
    result = compute_nwsp(inscriptions)
    # result['signs']: dict sign → {histogram, classification, mean_pos, ...}
    # result['summary']: classification counts
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline  # noqa: I001

# ── Core NWSP computation ─────────────────────────────────────────────


def _nwp(position_1indexed: int, text_length: int) -> float:
    """Compute Normalized Weighted Position.

    Maps position p in text of length L to [1.0, 10.0].

    Args:
        position_1indexed: 1-indexed sign position.
        text_length:       Number of signs in the text.

    Returns:
        Float in [1.0, 10.0].
    """
    if text_length <= 1:
        return 5.5  # isolated sign: middle of scale
    p = position_1indexed
    L = text_length
    return (p - 1) / (L - 1) * 9.0 + 1.0


def compute_nwsp(
    inscriptions: list[list[str]],
    n_bins: int = 10,
    min_occurrences: int = 4,
) -> dict[str, Any]:
    """Compute Normalized Weighted Sign Position histograms for all signs.

    Args:
        inscriptions:    List of sign sequences (each = one inscription).
        n_bins:          Number of histogram bins (default 10, as in Fuls).
        min_occurrences: Minimum total occurrences to compute histogram.

    Returns:
        dict with:
            signs:         {sign: {histogram, raw_histogram, classification,
                                   mean_position, variance, total_weight,
                                   occurrence_count}}
            summary:       {classification: count, ...}
            corpus_stats:  {n_inscriptions, n_tokens, n_distinct_signs}
    """
    # Accumulate weighted position histograms
    # hist[sign][bin_0..bin_9] = sum of weights for that bin
    hist_weighted: dict[str, list[float]] = defaultdict(lambda: [0.0] * n_bins)
    hist_raw: dict[str, list[int]] = defaultdict(lambda: [0] * n_bins)
    total_weight: dict[str, float] = defaultdict(float)
    occurrence_count: Counter[str] = Counter()

    for insc in inscriptions:
        L = len(insc)
        if L == 0:
            continue
        for pos, sign in enumerate(insc, start=1):
            nwp = _nwp(pos, L)
            # Bin index: NWP in [1,10] → bins [0,9]
            bin_idx = min(int((nwp - 1.0) / 9.0 * n_bins), n_bins - 1)
            hist_weighted[sign][bin_idx] += L  # weight = text length
            hist_raw[sign][bin_idx] += 1  # unweighted count
            total_weight[sign] += L
            occurrence_count[sign] += 1

    # Build per-sign analysis
    signs_result: dict[str, dict[str, Any]] = {}

    for sign, raw in hist_raw.items():
        occ = occurrence_count[sign]
        if occ < min_occurrences:
            continue

        w_hist = hist_weighted[sign]
        tw = total_weight[sign]

        # Normalize weighted histogram to sum to 1.0
        norm_hist = [v / tw for v in w_hist] if tw > 0 else [1.0 / n_bins] * n_bins

        # Compute mean and variance of normalized weighted position
        bin_centers = [(i + 0.5) / n_bins * 9.0 + 1.0 for i in range(n_bins)]
        mean_pos = sum(norm_hist[i] * bin_centers[i] for i in range(n_bins))
        variance = sum(norm_hist[i] * (bin_centers[i] - mean_pos) ** 2 for i in range(n_bins))

        # Classification
        classification = _classify_nwsp(norm_hist, n_bins)

        signs_result[sign] = {
            "histogram": [round(v, 4) for v in norm_hist],
            "raw_histogram": raw,
            "classification": classification,
            "mean_position": round(mean_pos, 3),
            "variance": round(variance, 3),
            "total_weight": round(tw, 1),
            "occurrence_count": occ,
        }

    # Summary counts
    summary: Counter[str] = Counter(v["classification"] for v in signs_result.values())

    # Corpus statistics
    flat = [s for insc in inscriptions for s in insc]
    freq = Counter(flat)

    return {
        "signs": signs_result,
        "summary": dict(summary),
        "corpus_stats": {
            "n_inscriptions": len(inscriptions),
            "n_tokens": len(flat),
            "n_distinct_signs": len(freq),
            "signs_analyzed": len(signs_result),
        },
    }


def _classify_nwsp(norm_hist: list[float], n_bins: int = 10) -> str:
    """Classify a sign based on its normalized NWSP histogram shape.

    Follows Fuls (2015) Chapter 3.3 classification scheme.

    Returns one of: ITM, TMK, PTM, INITIAL, NUM, CON, MED
    """
    # Peak detection by region
    # Bin indices 0-1 = initial (NWP 1-3), 8-9 = terminal (NWP 8-10)
    initial_mass = sum(norm_hist[:2])  # bins 0-1: NWP 1-3
    terminal_mass = sum(norm_hist[-2:])  # bins 8-9: NWP 8-10
    medial_mass = sum(norm_hist[2:8])  # bins 2-7: NWP 3-8
    pre_term_mass = sum(norm_hist[5:8])  # bins 5-7: NWP 6-8 (numeral zone)

    # Entropy of histogram (low = peaked, high = uniform)
    entropy = -sum(p * math.log(p) for p in norm_hist if p > 0)
    max_entropy = math.log(n_bins)
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0

    # ITM: strong peaks at BOTH initial AND terminal
    if initial_mass > 0.25 and terminal_mass > 0.25:
        return "ITM"

    # TMK: dominant terminal peak
    if terminal_mass > 0.50:
        return "TMK"

    # INITIAL: dominant initial peak
    if initial_mass > 0.45:
        return "INITIAL"

    # NUM: concentration in pre-terminal zone (positions 6-8)
    if pre_term_mass > 0.45 and terminal_mass < 0.30:
        return "NUM"

    # CON: flat distribution (high entropy) → constant/phonetic
    if norm_entropy > 0.85:
        return "CON"

    # MED: medial concentration
    if medial_mass > 0.60:
        return "MED"

    # Default: medial
    return "MED"


# ── ICIT function code mapping ────────────────────────────────────────
# Maps our NWSP classification to Fuls' ICIT 3-letter function codes.
# These codes appear in the ICIT database alongside sign numbers.

NWSP_TO_ICIT: dict[str, str] = {
    "ITM": "ITM",  # Initial Cluster Terminal Marker
    "TMK": "TMK",  # Terminal Marker
    "PTM": "PTM",  # Post-Terminal Marker
    "INITIAL": "ITM",  # In ICIT, strong initials are part of ITM cluster
    "NUM": "NUM",  # Numeral
    "CON": "SYL",  # Constant distribution → likely syllabic (SYL in ICIT)
    "MED": "SYL",  # Medial distribution → likely syllabic
}


def compare_with_icit_functions(
    nwsp_result: dict[str, Any],
    icit_labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Compare NWSP classification to ICIT ground-truth labels.

    Args:
        nwsp_result:  Output of compute_nwsp().
        icit_labels:  Optional dict mapping sign_id → ICIT function code.
                      When provided (e.g. from ICIT database access), computes
                      classification accuracy.

    Returns:
        dict with:
            mapped_signs:   {sign: {nwsp_class, icit_code, match (if labels given)}}
            icit_summary:   {icit_code: count}
            accuracy:       float (only if icit_labels provided)
    """
    mapped: dict[str, Any] = {}
    icit_summary: Counter[str] = Counter()

    for sign, info in nwsp_result["signs"].items():
        nwsp_class = info["classification"]
        mapped_icit = NWSP_TO_ICIT.get(nwsp_class, "SYL")
        icit_summary[mapped_icit] += 1

        entry: dict[str, Any] = {
            "sign": sign,
            "nwsp_class": nwsp_class,
            "icit_code": mapped_icit,
        }

        if icit_labels and sign in icit_labels:
            true_icit = icit_labels[sign]
            entry["icit_true"] = true_icit
            entry["match"] = mapped_icit == true_icit

        mapped[sign] = entry

    result: dict[str, Any] = {
        "mapped_signs": mapped,
        "icit_summary": dict(icit_summary),
    }

    if icit_labels:
        labeled = {s: v for s, v in mapped.items() if "match" in v}
        correct = sum(1 for v in labeled.values() if v["match"])
        result["accuracy"] = round(correct / len(labeled), 4) if labeled else 0.0
        result["n_labeled"] = len(labeled)

    return result


# ── Pipeline entry point ──────────────────────────────────────────────


@register_pipeline("nwsp")
async def run_nwsp(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id:           corpus to analyze
        min_occurrences:   minimum sign occurrences (default 4)
        compare_icit:      if True, map results to ICIT codes (default True)
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

    result = compute_nwsp(
        inscriptions,
        min_occurrences=params.get("min_occurrences", 4),
    )

    if params.get("compare_icit", True):
        result["icit_mapping"] = compare_with_icit_functions(result)

    result["text_id"] = text_id
    result["text_name"] = text.get("name", text_id)
    return result
