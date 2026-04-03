"""Sign polyvalence detection pipeline.

Detects signs that exhibit bimodal or multimodal positional distributions,
which is a strong indicator of sign polyvalence — the same graphic sign
serving more than one linguistic function.

BACKGROUND (Fuls 2014, A Catalog of Indus Signs, p.105):
  In logo-syllabic writing systems a single sign may carry:
    (a) a logographic function (word or morpheme level), AND
    (b) a phonetic / syllabic function (sound level)
  A purely phonetic sign in an abjad or syllabary typically has a
  unimodal positional distribution (it occupies a consistent role in the
  word/inscription).  A polyvalent sign shows multiple concentration peaks —
  for example appearing frequently at inscription-initial position (as a
  logogram for a word-class like numerals or titles) AND at medial position
  (as a phonetic complement).

  The canonical example: Indus sign 550 (Fuls' numbering) has a bimodal
  positional histogram with peaks at initial and terminal positions,
  suggesting it functions as both a noun-class marker and a phonetic sign.

ALGORITHM:
  For each sign occurring ≥ min_freq times across all inscriptions:
    1. Compute a 3-bin positional histogram: [initial%, medial%, terminal%]
    2. Compute a finer within-word position histogram (fractional position 0→1)
    3. Detect multiple peaks using a simple prominence-threshold algorithm
    4. Compute a bimodality score B = (peak_count - 1) × peak_prominence
    5. Flag signs with B > bimodal_threshold as polyvalence candidates

USAGE:
    from glossa_lab.pipelines.sign_polyvalence import detect_polyvalent_signs
    result = detect_polyvalent_signs(inscriptions, min_freq=5)
    # result['candidates']: list of polyvalent sign dicts, sorted by B score
"""

from __future__ import annotations  # noqa: I001

import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline


# ── Core algorithm ────────────────────────────────────────────────────

def _fractional_positions(inscriptions: list[list[str]]) -> dict[str, list[float]]:
    """For each sign, collect fractional within-inscription positions.

    Position 0.0 = first slot, 1.0 = last slot.
    Single-sign inscriptions produce position 0.5.
    """
    positions: dict[str, list[float]] = defaultdict(list)
    for insc in inscriptions:
        L = len(insc)
        if L == 0:
            continue
        for i, sign in enumerate(insc):
            frac = i / (L - 1) if L > 1 else 0.5
            positions[sign].append(frac)
    return dict(positions)


def _positional_histogram(positions: list[float], bins: int = 10) -> list[float]:
    """Convert fractional positions to a normalised histogram.

    bins: number of equal-width bins over [0, 1].
    Returns a list of `bins` floats summing to 1.0.
    """
    counts = [0] * bins
    for p in positions:
        idx = min(int(p * bins), bins - 1)
        counts[idx] += 1
    total = sum(counts) or 1
    return [c / total for c in counts]


def _detect_peaks(hist: list[float], min_prominence: float = 0.05) -> list[int]:
    """Return indices of local maxima in hist with prominence ≥ min_prominence.

    Prominence = value at peak minus the highest valley between the peak
    and the nearest higher peak (simplified: value minus local minimum).
    """
    n = len(hist)
    peaks = []
    for i in range(1, n - 1):
        if hist[i] > hist[i - 1] and hist[i] > hist[i + 1]:
            # Compute prominence: min valley depth on each side
            left_min = min(hist[:i]) if i > 0 else hist[i]
            right_min = min(hist[i + 1 :]) if i < n - 1 else hist[i]
            prominence = hist[i] - max(left_min, right_min)
            if prominence >= min_prominence:
                peaks.append(i)
    # Also check endpoints
    if len(hist) >= 2:
        if hist[0] > hist[1]:
            right_min = min(hist[1:])
            if hist[0] - right_min >= min_prominence:
                peaks.append(0)
        if hist[-1] > hist[-2]:
            left_min = min(hist[:-1])
            if hist[-1] - left_min >= min_prominence:
                peaks.append(n - 1)
    return sorted(set(peaks))


def _bimodality_score(peaks: list[int], hist: list[float]) -> float:
    """Quantify how bimodal/multimodal the histogram is.

    Score = sum of peak prominences weighted by distance from each other.
    A perfectly bimodal distribution (two equal peaks at opposite ends)
    gives a high score; a unimodal distribution gives 0.
    """
    if len(peaks) < 2:
        return 0.0
    prominences = [hist[p] for p in peaks]
    # Weight by spread: distance between outer peaks normalised to [0,1]
    spread = (max(peaks) - min(peaks)) / max(len(hist) - 1, 1)
    return sum(prominences) * spread


def _coarse_positional(positions: list[float]) -> dict[str, float]:
    """3-bin coarse histogram: initial (0-0.25), medial (0.25-0.75), terminal (0.75-1)."""
    initial  = sum(1 for p in positions if p <= 0.25)
    terminal = sum(1 for p in positions if p >= 0.75)
    medial   = len(positions) - initial - terminal
    total = len(positions) or 1
    return {
        "initial_pct":  round(initial  / total, 4),
        "medial_pct":   round(medial   / total, 4),
        "terminal_pct": round(terminal / total, 4),
        "dominant":     "initial"  if initial > medial and initial > terminal
                        else "terminal" if terminal > medial
                        else "medial",
    }


def detect_polyvalent_signs(
    inscriptions: list[list[str]],
    min_freq: int = 5,
    bins: int = 10,
    min_prominence: float = 0.05,
    bimodal_threshold: float = 0.08,
) -> dict[str, Any]:
    """Detect signs with bimodal/multimodal positional distributions.

    Args:
        inscriptions:      List of inscriptions, each a list of sign strings.
        min_freq:          Minimum total occurrences to analyse a sign.
        bins:              Histogram bin count (finer = more sensitive).
        min_prominence:    Minimum peak prominence to count as a true peak.
        bimodal_threshold: Minimum bimodality score to flag as candidate.

    Returns dict with:
        candidates:   List of polyvalence candidates sorted by bimodality score.
        all_signs:    Full analysis for every sign meeting min_freq.
        summary:      High-level counts and corpus statistics.
    """
    frac_positions = _fractional_positions(inscriptions)
    freq: Counter[str] = Counter(
        sign for insc in inscriptions for sign in insc
    )

    candidates: list[dict[str, Any]] = []
    all_signs: list[dict[str, Any]] = []

    for sign, positions in sorted(frac_positions.items()):
        if freq[sign] < min_freq:
            continue

        hist = _positional_histogram(positions, bins)
        peaks = _detect_peaks(hist, min_prominence)
        b_score = _bimodality_score(peaks, hist)
        coarse = _coarse_positional(positions)

        # Entropy of the positional distribution (higher → more spread)
        pos_entropy = -sum(
            p * math.log2(p) for p in hist if p > 0
        ) / math.log2(bins)  # normalised to [0,1]

        entry: dict[str, Any] = {
            "sign":          sign,
            "frequency":     freq[sign],
            "peak_count":    len(peaks),
            "bimodality_score": round(b_score, 4),
            "positional_entropy": round(pos_entropy, 4),
            "histogram":     [round(v, 4) for v in hist],
            "peaks":         peaks,
            **coarse,
        }
        all_signs.append(entry)

        if b_score >= bimodal_threshold:
            entry["polyvalence_candidate"] = True
            candidates.append(entry)

    candidates.sort(key=lambda x: x["bimodality_score"], reverse=True)
    all_signs.sort(key=lambda x: x["bimodality_score"], reverse=True)

    total_signs = len(all_signs)
    n_candidates = len(candidates)

    return {
        "candidates":    candidates,
        "all_signs":     all_signs,
        "summary": {
            "total_signs_analysed": total_signs,
            "polyvalence_candidates": n_candidates,
            "candidate_fraction": round(n_candidates / total_signs, 3) if total_signs else 0,
            "parameters": {
                "min_freq":          min_freq,
                "bins":              bins,
                "min_prominence":    min_prominence,
                "bimodal_threshold": bimodal_threshold,
            },
        },
    }


def compare_across_systems(
    systems: dict[str, list[list[str]]],
    min_freq: int = 3,
) -> dict[str, Any]:
    """Run polyvalence detection across multiple writing system corpora.

    Args:
        systems: {system_name: inscriptions_list}
        min_freq: minimum frequency threshold

    Returns comparative dict showing how polyvalence candidate rate
    scales with writing system complexity.
    """
    comparison: dict[str, Any] = {}
    for name, inscriptions in systems.items():
        result = detect_polyvalent_signs(inscriptions, min_freq=min_freq)
        freq: Counter[str] = Counter(
            s for insc in inscriptions for s in insc
        )
        comparison[name] = {
            "total_tokens":        sum(freq.values()),
            "distinct_signs":      len(freq),
            "type_token_ratio":    round(len(freq) / max(sum(freq.values()), 1), 4),
            "hapax_count":         sum(1 for v in freq.values() if v == 1),
            "polyvalence_candidates": result["summary"]["polyvalence_candidates"],
            "total_analysed":      result["summary"]["total_signs_analysed"],
            "candidate_fraction":  result["summary"]["candidate_fraction"],
            "top_candidates":      [
                {"sign": c["sign"], "score": c["bimodality_score"]}
                for c in result["candidates"][:5]
            ],
        }
    return comparison


# ── Pipeline entry point ──────────────────────────────────────────────

@register_pipeline("sign_polyvalence")
async def run_sign_polyvalence(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id:          corpus to analyse
        min_freq:         minimum sign frequency (default 5)
        bins:             histogram bins (default 10)
        min_prominence:   peak prominence threshold (default 0.05)
        bimodal_threshold: score threshold for candidates (default 0.08)
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

    # Use inscription-level structure if available, else treat as one inscription
    content = text.get("content", [])
    if content and isinstance(content[0], list):
        inscriptions = content
    else:
        inscriptions = [content]

    result = detect_polyvalent_signs(
        inscriptions,
        min_freq=params.get("min_freq", 5),
        bins=params.get("bins", 10),
        min_prominence=params.get("min_prominence", 0.05),
        bimodal_threshold=params.get("bimodal_threshold", 0.08),
    )
    result["text_id"] = text_id
    result["text_name"] = text.get("name", text_id)
    return result
