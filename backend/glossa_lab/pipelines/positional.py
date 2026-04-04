"""Positional frequency analysis pipeline.

Computes position-specific frequencies for each sign in a corpus
of inscriptions. Reveals which signs are exclusively initial,
medial, or terminal — critical for identifying grammatical
structure in undeciphered scripts.

For the Indus script, strong positional constraints are well
documented: sign 342 is overwhelmingly terminal, certain signs
are exclusively initial (Mahadevan 1977, Yadav et al. 2010).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline


def compute_positional_freq(
    inscriptions: list[list[str]],
) -> dict[str, Any]:
    """Compute positional frequency distribution for each sign.

    Args:
        inscriptions: list of inscriptions, each a list of sign IDs.

    Returns dict with per-sign positional profiles and summary stats.
    """
    sign_positions: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0, "singleton": 0}
    )
    total_by_position: dict[str, int] = {
        "initial": 0,
        "medial": 0,
        "terminal": 0,
        "singleton": 0,
    }
    total_signs = 0
    total_inscriptions = len(inscriptions)

    for insc in inscriptions:
        if not insc:
            continue
        if len(insc) == 1:
            sign_positions[insc[0]]["singleton"] += 1
            total_by_position["singleton"] += 1
            total_signs += 1
        else:
            # Initial
            sign_positions[insc[0]]["initial"] += 1
            total_by_position["initial"] += 1
            # Terminal
            sign_positions[insc[-1]]["terminal"] += 1
            total_by_position["terminal"] += 1
            # Medial
            for s in insc[1:-1]:
                sign_positions[s]["medial"] += 1
                total_by_position["medial"] += 1
            total_signs += len(insc)

    # Compute per-sign profiles with dominance classification
    profiles = []
    for sign, pos_counts in sorted(
        sign_positions.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True,
    ):
        total = sum(pos_counts.values())
        profile = {
            "sign": sign,
            "total": total,
            "initial": pos_counts["initial"],
            "medial": pos_counts["medial"],
            "terminal": pos_counts["terminal"],
            "singleton": pos_counts["singleton"],
        }
        # Classify dominant position
        active = {k: v for k, v in pos_counts.items() if k != "singleton" and v > 0}
        if active:
            dom_pos = max(active, key=active.get)  # type: ignore[arg-type]
            dom_pct = active[dom_pos] / total if total > 0 else 0
            profile["dominant_position"] = dom_pos
            profile["dominant_pct"] = round(dom_pct, 3)
            profile["exclusive"] = len(active) == 1
        else:
            profile["dominant_position"] = "singleton"
            profile["dominant_pct"] = 1.0
            profile["exclusive"] = True

        profiles.append(profile)

    # Find exclusively positional signs
    exclusively_initial = [
        p["sign"]
        for p in profiles
        if p.get("exclusive") and p.get("dominant_position") == "initial" and p["total"] >= 3
    ]
    exclusively_terminal = [
        p["sign"]
        for p in profiles
        if p.get("exclusive") and p.get("dominant_position") == "terminal" and p["total"] >= 3
    ]

    return {
        "total_signs": total_signs,
        "total_inscriptions": total_inscriptions,
        "unique_signs": len(sign_positions),
        "position_totals": total_by_position,
        "exclusively_initial": exclusively_initial[:20],
        "exclusively_terminal": exclusively_terminal[:20],
        "profiles": profiles[:100],  # Top 100 by frequency
    }


@register_pipeline("positional")
async def run_positional(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params: {text_id: str, delimiter: str (default " ")}.
    Text content is split into inscriptions by newline, then by delimiter.
    """
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    # For Indus-style corpora, content is a flat list of signs.
    # We treat each contiguous sequence as one inscription.
    # If the corpus has metadata about inscription boundaries,
    # use that; otherwise treat entire content as one inscription.
    symbols = text["content"]

    # Heuristic: if symbols contain spaces or look like multi-sign
    # inscriptions encoded as space-separated strings, split them.
    delimiter = params.get("delimiter", None)
    if delimiter:
        # Content is a flat list; group into chunks
        inscriptions = []
        current: list[str] = []
        for s in symbols:
            if s == delimiter:
                if current:
                    inscriptions.append(current)
                    current = []
            else:
                current.append(s)
        if current:
            inscriptions.append(current)
    else:
        # Treat entire content as one inscription
        inscriptions = [symbols]

    result = compute_positional_freq(inscriptions)
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    return result
