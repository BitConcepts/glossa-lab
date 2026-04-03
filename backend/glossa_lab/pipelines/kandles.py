"""Kandles phonetic color-coding pipeline.

Implements the Kandles system from [REDACTED-PATENT-PUB] (Merkur):
  - Maps first-consonant sounds to 7 color groups
  - Generates color-coded text and grid representations
  - Enables cross-language phonetic fingerprint comparison

Kandles groups (derived from extended Soundex):
  0: Vowel-initial (A, E, I, O, U)       → White
  1: K, G, J, Ch                         → Yellow (Sun)
  2: M, N                                → Grey   (Moon)
  3: T, D, Th                            → Red    (Fire)
  4: R, L                                → Blue   (Water)
  5: Y, W, H, Kh                         → Green  (Tree)
  6: P, B, F, V                          → Purple (Flower)
  7: S, Z, Sh                            → Brown  (Soil)

Language-specific bias profiles are defined in kandles_profiles.py.
Pass a KandlesProfile (or profile name string) to any function to use
a language-appropriate phoneme→color mapping instead of the default.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING, Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline

if TYPE_CHECKING:
    from glossa_lab.pipelines.kandles_profiles import KandlesProfile

# ── Kandles mapping ───────────────────────────────────────────────

KANDLES_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White", "hex": "#FFFFFF",
        "nature": "Vowel", "kanji": ""},
    1: {"letters": {"K", "G", "J", "C", "Q"}, "color": "Yellow", "hex": "#EAB308",
        "nature": "Sun", "kanji": "日", "digraphs": {"CH"}},
    2: {"letters": {"M", "N"}, "color": "Grey", "hex": "#9CA3AF",
        "nature": "Moon", "kanji": "月", "digraphs": set()},
    3: {"letters": {"T", "D"}, "color": "Red", "hex": "#DC2626",
        "nature": "Fire", "kanji": "火", "digraphs": {"TH"}},
    4: {"letters": {"R", "L"}, "color": "Blue", "hex": "#2563EB",
        "nature": "Water", "kanji": "水", "digraphs": set()},
    5: {"letters": {"Y", "W", "H"}, "color": "Green", "hex": "#16A34A",
        "nature": "Tree", "kanji": "木", "digraphs": {"KH"}},
    6: {"letters": {"P", "B", "F", "V"}, "color": "Purple", "hex": "#9333EA",
        "nature": "Flower", "kanji": "花", "digraphs": set()},
    7: {"letters": {"S", "Z", "X"}, "color": "Brown", "hex": "#92400E",
        "nature": "Soil", "kanji": "土", "digraphs": {"SH"}},
}

# Build fast lookup: letter → group number
_LETTER_TO_GROUP: dict[str, int] = {}
for gnum, ginfo in KANDLES_GROUPS.items():
    for letter in ginfo["letters"]:
        _LETTER_TO_GROUP[letter] = gnum

# Digraph lookup: digraph → group number
_DIGRAPH_TO_GROUP: dict[str, int] = {}
for gnum, ginfo in KANDLES_GROUPS.items():
    for dg in ginfo.get("digraphs", set()):
        _DIGRAPH_TO_GROUP[dg] = gnum


def _resolve_profile(
    profile: "KandlesProfile | str | None",
) -> "KandlesProfile | None":
    """Resolve profile argument to a KandlesProfile object (or None for default)."""
    if profile is None:
        return None
    if isinstance(profile, str):
        if profile in ("default", "greek", "mycenaean"):
            return None  # use built-in globals for the default case
        from glossa_lab.pipelines.kandles_profiles import get_profile
        return get_profile(profile)
    return profile  # already a KandlesProfile


def classify_word(
    word: str,
    profile: "KandlesProfile | str | None" = None,
) -> dict[str, Any]:
    """Classify a word into its Kandles group based on initial sound.

    Args:
        word:    The word/syllable to classify.
        profile: Optional language-specific bias profile. When None the
                 default Greek/English Kandles mapping is used.
    """
    if not word:
        return {"group": -1, "color": "None", "hex": "#000000"}

    p = _resolve_profile(profile)
    letter_to_group = p.letter_to_group if p else _LETTER_TO_GROUP
    digraph_to_group = p.digraph_to_group if p else _DIGRAPH_TO_GROUP
    groups_map = p.groups if p else KANDLES_GROUPS

    upper = word.upper()

    # Check digraphs first (CH, TH, SH, KH, KW, NG, …)
    if len(upper) >= 2:
        digraph = upper[:2]
        if digraph in digraph_to_group:
            gnum = digraph_to_group[digraph]
            g = groups_map.get(gnum, {})
            return {
                "group": gnum,
                "color": g.get("color", f"Group{gnum}"),
                "hex":   KANDLES_GROUPS.get(gnum, {}).get("hex", "#888888"),
                "nature": g.get("nature", ""),
                "word": word,
            }

    # Single letter lookup
    first = upper[0]
    gnum = letter_to_group.get(first, -1)
    if gnum >= 0:
        g = groups_map.get(gnum, {})
        return {
            "group": gnum,
            "color": g.get("color", f"Group{gnum}"),
            "hex":   KANDLES_GROUPS.get(gnum, {}).get("hex", "#888888"),
            "nature": g.get("nature", ""),
            "word": word,
        }

    return {"group": -1, "color": "Unknown", "hex": "#666666",
            "nature": "Unknown", "word": word}


def color_code_text(
    words: list[str],
    profile: "KandlesProfile | str | None" = None,
) -> list[dict[str, Any]]:
    """Color-code a list of words using the Kandles system.

    Args:
        words:   List of word/syllable strings.
        profile: Optional language-specific bias profile.
    """
    p = _resolve_profile(profile)  # resolve once, reuse
    return [classify_word(w, profile=p) for w in words]


def generate_grid(
    words: list[str],
    size: int | None = None,
    profile: "KandlesProfile | str | None" = None,
) -> dict[str, Any]:
    """Generate a Kandles color-coded grid.

    Grid has equal rows and columns. Words are laid out left-to-right,
    top-to-bottom. Empty cells are padded.

    Args:
        words:   Words/syllables to lay out.
        size:    Force grid size (auto-computed if None).
        profile: Optional language-specific bias profile.
    """
    n = len(words)
    if size is None:
        size = math.ceil(math.sqrt(n))
    if size < 1:
        size = 1

    p = _resolve_profile(profile)
    coded = color_code_text(words, profile=p)
    groups_map = p.groups if p else KANDLES_GROUPS

    rows = []
    for r in range(size):
        row = []
        for c in range(size):
            idx = r * size + c
            if idx < len(coded):
                cell = coded[idx].copy()
                cell["row"] = r
                cell["col"] = c
            else:
                cell = {
                    "group": -1, "color": "Empty", "hex": "#000000",
                    "nature": "Empty", "word": "", "row": r, "col": c,
                }
            row.append(cell)
        rows.append(row)

    # Color distribution summary
    dist = Counter(c["group"] for c in coded if c["group"] >= 0)
    color_dist = {}
    for gnum, count in sorted(dist.items()):
        g = groups_map.get(gnum, {})
        color_dist[g.get("color", f"Group {gnum}")] = count

    return {
        "grid_size": size,
        "total_words": n,
        "grid": rows,
        "color_distribution": color_dist,
        "profile": (p.name if p else "default"),
    }


def compare_grids(
    grid_a: dict[str, Any],
    grid_b: dict[str, Any],
) -> dict[str, Any]:
    """Compare two Kandles grids by color distribution similarity.

    Uses cosine similarity on the 8-dimensional color distribution vectors.
    Both grids must have been generated with the SAME profile for the
    comparison to be linguistically meaningful.
    """
    groups = list(range(8))

    def to_vec(grid_result: dict) -> list[float]:
        dist: dict[int, int] = {}
        for row in grid_result["grid"]:
            for cell in row:
                g = cell.get("group", -1)
                if g >= 0:
                    dist[g] = dist.get(g, 0) + 1
        total = sum(dist.values()) or 1
        return [dist.get(g, 0) / total for g in groups]

    va = to_vec(grid_a)
    vb = to_vec(grid_b)

    dot = sum(a * b for a, b in zip(va, vb))
    mag_a = math.sqrt(sum(a * a for a in va))
    mag_b = math.sqrt(sum(b * b for b in vb))
    similarity = dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0.0

    # Use label from grid_a's profile (both should match)
    profile_name = grid_a.get("profile", "default")

    return {
        "similarity": round(similarity, 4),
        "profile": profile_name,
        "distribution_a": {f"G{g}": round(va[g], 4) for g in groups},
        "distribution_b": {f"G{g}": round(vb[g], 4) for g in groups},
    }


@register_pipeline("kandles")
async def run_kandles(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id: str, mode: str}.

    Modes: "color_code" (default), "grid", "compare" (needs text_id_b).
    """
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    mode = params.get("mode", "grid")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    words = text["content"]

    if mode == "color_code":
        coded = color_code_text(words)
        return {"text_id": text_id, "text_name": text["name"],
                "mode": mode, "coded_words": coded}

    if mode == "grid":
        grid = generate_grid(words)
        return {"text_id": text_id, "text_name": text["name"],
                "mode": mode, **grid}

    if mode == "compare":
        text_id_b = params.get("text_id_b")
        if not text_id_b:
            raise ValueError("compare mode requires text_id_b")
        text_b = await db.get_text(text_id_b)
        if text_b is None:
            raise ValueError(f"Text not found: {text_id_b}")

        grid_a = generate_grid(words)
        grid_b = generate_grid(text_b["content"])
        comparison = compare_grids(grid_a, grid_b)
        return {"text_id_a": text_id, "text_id_b": text_id_b,
                "mode": mode, **comparison}

    raise ValueError(f"Unknown mode: {mode}")
