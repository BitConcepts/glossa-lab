"""Numeral identification pipeline.

Detects signs that are likely numerals based on:
  1. Positional behavior: numerals cluster in specific positions
  2. Frequency patterns: numerals follow different distributions
  3. Co-occurrence: numerals appear with specific neighboring signs
  4. Combinatorial: stroked signs (1 stroke, 2 strokes...) are numeric

For the Indus script, scholars broadly agree that certain signs
represent numerals (single strokes, multiple strokes, etc.). If we
can identify and remove numerals from the phonetic search space,
we reduce the problem significantly.

References:
  - Fuls (2023): "Corpus of Indus Inscriptions" — numeral sign functions
  - Wells (2006): sign function classifications (NUM, SHN, LON, SPN)
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from glossa_lab.engine import register_pipeline


def identify_numerals(
    inscriptions: list[list[str]],
    min_freq: int = 3,
) -> dict[str, Any]:
    """Identify likely numeral signs based on distributional properties.

    Numeral signs typically:
      - Appear in clusters (consecutive numeral signs)
      - Have high frequency but limited positional range
      - Co-occur with specific "counter" signs
      - Follow a combinatorial pattern (1, 2, 3... strokes)

    Returns dict with candidate numerals and their evidence.
    """
    freq: Counter[str] = Counter()
    # Track which signs appear adjacent to each other
    adjacency: dict[str, Counter[str]] = {}
    # Track positional patterns
    positions: dict[str, list[float]] = {}

    for insc in inscriptions:
        for i, sign in enumerate(insc):
            freq[sign] += 1
            # Relative position (0=initial, 1=terminal)
            if len(insc) > 1:
                rel_pos = i / (len(insc) - 1)
            else:
                rel_pos = 0.5
            positions.setdefault(sign, []).append(rel_pos)

            # Adjacency
            if i > 0:
                adjacency.setdefault(sign, Counter())[insc[i - 1]] += 1
            if i < len(insc) - 1:
                adjacency.setdefault(sign, Counter())[insc[i + 1]] += 1

    candidates = []
    for sign, count in freq.most_common():
        if count < min_freq:
            continue

        pos_list = positions.get(sign, [])
        avg_pos = sum(pos_list) / len(pos_list) if pos_list else 0.5
        pos_std = (
            (sum((p - avg_pos) ** 2 for p in pos_list) / len(pos_list)) ** 0.5
            if len(pos_list) > 1
            else 0
        )

        # Numeral heuristics
        evidence = []
        numeral_score = 0.0

        # 1. Numerals often cluster in specific positions (not spread evenly)
        if pos_std < 0.25:
            evidence.append("concentrated_position")
            numeral_score += 0.3

        # 2. Numerals often appear together (self-adjacency)
        adj = adjacency.get(sign, Counter())
        if sign in adj and adj[sign] > count * 0.1:
            evidence.append("self_adjacent")
            numeral_score += 0.3

        # 3. Signs that co-occur with very few distinct neighbors
        # (numerals pair with specific "unit" signs)
        if len(adj) < 10 and count > 10:
            evidence.append("limited_neighbors")
            numeral_score += 0.2

        # 4. High frequency relative to distinct-neighbor count
        neighbor_ratio = len(adj) / max(count, 1)
        if neighbor_ratio < 0.3:
            evidence.append("high_freq_low_diversity")
            numeral_score += 0.2

        if numeral_score >= 0.3:
            candidates.append({
                "sign": sign,
                "frequency": count,
                "numeral_score": round(numeral_score, 2),
                "avg_position": round(avg_pos, 3),
                "position_std": round(pos_std, 3),
                "distinct_neighbors": len(adj),
                "evidence": evidence,
            })

    candidates.sort(key=lambda c: c["numeral_score"], reverse=True)

    # Classify top candidates
    likely_numerals = [c["sign"] for c in candidates if c["numeral_score"] >= 0.5]
    possible_numerals = [
        c["sign"] for c in candidates
        if 0.3 <= c["numeral_score"] < 0.5
    ]

    return {
        "total_signs_analysed": len(freq),
        "likely_numerals": likely_numerals[:20],
        "possible_numerals": possible_numerals[:20],
        "candidates": candidates[:30],
        "non_numeral_count": len(freq) - len(likely_numerals) - len(possible_numerals),
    }


@register_pipeline("numerals")
async def run_numerals(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point."""
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    # Reconstruct inscriptions from flat list
    symbols = text["content"]
    metadata = text.get("metadata", {})
    if isinstance(metadata, dict) and "inscription_lengths" in metadata:
        inscriptions = []
        idx = 0
        for length in metadata["inscription_lengths"]:
            inscriptions.append(symbols[idx:idx + length])
            idx += length
    else:
        inscriptions = [symbols]

    result = identify_numerals(inscriptions, min_freq=params.get("min_freq", 3))
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    return result
