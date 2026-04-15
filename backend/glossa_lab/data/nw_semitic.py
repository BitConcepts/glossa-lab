"""NW Semitic Test1 corpus data module — Dr. Andreas Fuls.

This is the undeciphered NW Semitic corpus provided by Dr. Fuls for
collaborative decipherment research. Each sign is identified by a
3-digit numeric code (e.g. '004', '066', '208').

Properties:
  - 78 distinct signs
  - ~450 tokens across ~143 words
  - Reading direction: RIGHT-TO-LEFT (confirmed by Dr. Fuls 2026-04)
  - Writing system: syllabic (consonant + vowel), NOT consonantal-only
  - Verified anchor signs (Dr. Fuls): 004=T, 066=M, 208=N, 133=ayin, 128=L, 080=W

Note: The corpus file is read LEFT-TO-RIGHT as stored, but each word
must be reversed for phonetically correct order (RTL reading direction).
The reading_direction field is set to 'rtl' so the DirectionNormalizer
atomic node and decipher pipeline normalise automatically.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).parent
_CORPUS_FILE = _DATA_DIR / "fuls_nw_semitic_test1.txt"

# Verified anchor assignments from Dr. Fuls (2026-04)
FULS_ANCHORS: dict[str, str] = {
    "004": "T",   # tet
    "066": "m",   # mem
    "208": "n",   # nun
    "133": "E",   # ayin (transliterated as 'E' matching Hebrew corpus)
    "128": "l",   # lamed
    "080": "w",   # waw (also U vowel in syllabic context)
}

METADATA: dict[str, Any] = {
    "name":            "NW Semitic Test1 (Dr. Fuls)",
    "language":        "Unknown NW Semitic",
    "script":          "Undeciphered syllabic",
    "writing_type":    "syllabic (CV — consonant + vowel)",
    "reading_direction": "rtl",
    "status":          "undeciphered",
    "source":          "Provided by Dr. Andreas Fuls for collaborative decipherment",
    "n_signs":         78,
    "tokens_per_sign": 4.2,
    "provided_by":     "Dr. Andreas Fuls",
    "anchors":         FULS_ANCHORS,
    "note": (
        "Reading direction is RIGHT-TO-LEFT (confirmed by Dr. Fuls, Apr 2026). "
        "File stores words left-to-right; each word must be reversed for correct "
        "phonological order. Writing system is syllabic (CV), not consonantal. "
        "Use DirectionNormalizer(rtl) or reading_direction='rtl' in all analyses."
    ),
}


def get_corpus_words() -> list[list[str]]:
    """Return the raw word list as stored in the file (LEFT-TO-RIGHT order).

    Each inner list is one word (sequence of sign codes separated by '-').
    To get phonetically correct RTL order, reverse each inner list.
    """
    if not _CORPUS_FILE.exists():
        return []
    words: list[list[str]] = []
    with open(_CORPUS_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = [s.strip() for s in line.split("-") if s.strip()]
            if parts:
                words.append(parts)
    return words


def get_corpus_inscriptions() -> list[list[str]]:
    """Return word-level inscriptions normalised to RTL phonological order.

    Each word is REVERSED so that the phonetically first sign is at index 0,
    matching the convention used by LanguageModel and all decipherment nodes.
    This is what DirectionNormalizer(rtl) would produce.
    """
    return [list(reversed(w)) for w in get_corpus_words()]


def get_corpus_symbols() -> list[str]:
    """Return flat list of all sign tokens (RTL-normalised order)."""
    return [s for word in get_corpus_inscriptions() for s in word]


def corpus_statistics() -> dict[str, Any]:
    """Return summary statistics."""
    words = get_corpus_inscriptions()
    flat  = [s for w in words for s in w]
    from collections import Counter
    freq = Counter(flat)
    return {
        "n_tokens":   len(flat),
        "n_words":    len(words),
        "n_distinct": len(freq),
        "tokens_per_sign": round(len(flat) / max(1, len(freq)), 2),
        "reading_direction": "rtl",
        "top_signs": [s for s, _ in freq.most_common(10)],
    }
