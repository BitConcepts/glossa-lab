"""Character frequency analysis pipeline.

Computes symbol frequencies, rank-frequency distribution, and
an approximate Zipf's law exponent.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline


def compute_char_freq(symbols: list[str]) -> dict[str, Any]:
    """Compute character frequency statistics for a symbol sequence."""
    counts = Counter(symbols)
    total = len(symbols)
    unique = len(counts)

    # Sort by frequency descending
    ranked = counts.most_common()
    frequencies = {sym: cnt for sym, cnt in ranked}

    # Zipf's law fit: log(freq) ≈ -α * log(rank) + C
    # Simple least-squares on log-log scale
    zipf_exponent = _fit_zipf(ranked)

    return {
        "total_symbols": total,
        "unique_symbols": unique,
        "frequencies": frequencies,
        "rank_frequency": [
            {"rank": i + 1, "symbol": sym, "count": cnt, "freq": round(cnt / total, 6)}
            for i, (sym, cnt) in enumerate(ranked)
        ],
        "zipf_exponent": round(zipf_exponent, 4) if zipf_exponent else None,
    }


def _fit_zipf(ranked: list[tuple[str, int]]) -> float | None:
    """Fit Zipf exponent via log-log linear regression."""
    if len(ranked) < 3:
        return None

    n = len(ranked)
    sum_x = sum_y = sum_xy = sum_x2 = 0.0
    for i, (_, cnt) in enumerate(ranked):
        if cnt == 0:
            continue
        x = math.log(i + 1)
        y = math.log(cnt)
        sum_x += x
        sum_y += y
        sum_xy += x * y
        sum_x2 += x * x

    denom = n * sum_x2 - sum_x * sum_x
    if abs(denom) < 1e-12:
        return None

    slope = (n * sum_xy - sum_x * sum_y) / denom
    return -slope  # Zipf exponent is the negative slope


@register_pipeline("char_freq")
async def run_char_freq(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id: str}."""
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    symbols = text["content"]
    if not isinstance(symbols, list):
        raise ValueError("Text content must be a list of symbols")

    result = compute_char_freq(symbols)
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    result["corpus_type"] = text["corpus_type"]
    return result
