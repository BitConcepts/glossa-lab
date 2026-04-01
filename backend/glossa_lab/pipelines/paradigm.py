"""Paradigm detection pipeline.

Finds sets of inscriptions that share a common stem but differ in
one position — likely grammatical inflections (e.g. verb conjugations,
noun declensions, case markers).

For example, if we find:
  [A B C D]
  [A B E D]
  [A B F D]

Then signs C, E, F may form an inflectional paradigm at position 3,
with [A B _ D] as the stem template.

This is a direct computational implementation of the morphological
analysis that Ventris and Kober used to crack Linear B.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline


def detect_paradigms(
    inscriptions: list[list[str]],
    min_stem_freq: int = 2,
    min_variants: int = 2,
) -> dict[str, Any]:
    """Detect inflectional paradigms in a set of inscriptions.

    For each possible slot position in inscriptions of a given length,
    creates a stem template (inscription with that slot wildcarded)
    and groups inscriptions by stem.

    Args:
        inscriptions: list of inscriptions, each a list of sign IDs.
        min_stem_freq: minimum number of inscriptions sharing a stem.
        min_variants: minimum unique values in the varying slot.
    """
    # Group inscriptions by length
    by_length: dict[int, list[list[str]]] = defaultdict(list)
    for insc in inscriptions:
        if len(insc) >= 2:
            by_length[len(insc)].append(insc)

    paradigms = []

    for length, group in sorted(by_length.items()):
        if len(group) < min_stem_freq:
            continue

        # For each possible varying position
        for slot in range(length):
            # Build stem templates: replace slot with wildcard
            stems: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(
                list
            )
            for insc in group:
                stem = tuple(
                    "_" if i == slot else insc[i] for i in range(length)
                )
                stems[stem].append({
                    "inscription": insc,
                    "variant_sign": insc[slot],
                })

            # Find stems with multiple variants
            for stem, variants in stems.items():
                unique_variants = set(v["variant_sign"] for v in variants)
                if (
                    len(variants) >= min_stem_freq
                    and len(unique_variants) >= min_variants
                ):
                    paradigms.append({
                        "stem_template": list(stem),
                        "length": length,
                        "slot_position": slot,
                        "variant_count": len(unique_variants),
                        "occurrence_count": len(variants),
                        "variants": sorted(unique_variants),
                        "examples": [
                            v["inscription"] for v in variants[:10]
                        ],
                    })

    # Sort by number of variants (most interesting first)
    paradigms.sort(key=lambda p: p["variant_count"], reverse=True)

    return {
        "total_inscriptions": sum(len(g) for g in by_length.values()),
        "length_distribution": {
            str(k): len(v) for k, v in sorted(by_length.items())
        },
        "paradigm_count": len(paradigms),
        "paradigms": paradigms[:50],  # Top 50
    }


@register_pipeline("paradigm")
async def run_paradigm(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id, min_stem_freq, min_variants}."""
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    # For Indus corpus: reconstruct inscriptions from flat list
    # using the corpus generator's structure
    symbols = text["content"]

    # Split into inscription-like chunks by a separator or fixed window
    # For now, use windowed approach with common inscription lengths (3-7)
    inscriptions: list[list[str]] = []

    # Try to use metadata for inscription boundaries
    metadata = text.get("metadata", {})
    if isinstance(metadata, dict) and "inscription_lengths" in metadata:
        idx = 0
        for length in metadata["inscription_lengths"]:
            inscriptions.append(symbols[idx : idx + length])
            idx += length
    else:
        # Default: treat entire content as one inscription
        inscriptions = [symbols]

    result = detect_paradigms(
        inscriptions,
        min_stem_freq=params.get("min_stem_freq", 2),
        min_variants=params.get("min_variants", 2),
    )
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    return result
