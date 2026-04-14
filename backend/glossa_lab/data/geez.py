"""Geʽez Genesis corpus data module for Glossa Lab.

Provides access to Dr. Fuls' Geʽez Genesis corpus and sign list,
pre-processed into the standard Glossa Lab data module interface.

The Geʽez script is an abugida (alphasyllabary) used to write
several Afro-Asiatic languages of Ethiopia and Eritrea. It is fully
deciphered, making it an ideal controlled benchmark for evaluating
syllabic decipherment methods.

Corpus: Book of Genesis in Ethiopic script (Tigrinya)
Sign list: 26 consonant rows × 7-8 vowel orders ≈ 200 syllabic signs

This module is used by:
  - geez_syllabic_anchor_convergence.py  (anchor validation experiment)
  - The Glossa Lab corpus registry (auto-seeded on first run)

Geographic / temporal metadata:
  Geʽez script: 1st century CE → present
  Ge'ez language: liturgical language of Ethiopian/Eritrean Orthodox Church
  Genesis source: Tigrinya Bible (uses Geʽez abugida)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_HERE     = Path(os.path.abspath(__file__)).parent
_DATA_DIR = _HERE / "geez"
_GENESIS  = _DATA_DIR / "Geez_Genesis.txt"
_SIGNLIST = _DATA_DIR / "Geez_signlist.txt"

# ── Metadata ──────────────────────────────────────────────────────────────────

METADATA: dict[str, Any] = {
    "name":          "Geʽez Genesis (Tigrinya Bible)",
    "language":      "Tigrinya / Geʽez",
    "script":        "Geʽez (Ethiopic Abugida)",
    "writing_type":  "abugida-syllabic",
    "reading_direction": "ltr",
    "status":        "fully_deciphered",
    "period":        "Modern (Tigrinya Bible translation)",
    "source":        "Book of Genesis in Ethiopic script",
    "geo_centroid":  [15.0, 39.0],   # Eritrea / Northern Ethiopia
    "date_range_bce": [-30, -2026],  # Geʽez script ~1st CE to present
    "language_family": "Afro-Asiatic / Semitic / Ethiosemitic",
    "sign_inventory_size": "~200 syllabic signs",
    "corpus_size":   "~85,000 Ethiopic syllabic tokens",
    "provided_by":   "Dr. Andreas Fuls",
    "note": (
        "The Geʽez script (fidäl) has 26 consonant base characters, "
        "each with 7 vowel-order forms (plus labialized 8th forms for some). "
        "This corpus is used as a fully-known benchmark for the "
        "anchor-convergence validation experiment."
    ),
}

# ── Ethiopic Unicode ranges ───────────────────────────────────────────────────

_ETHIOPIC_PUNCT = {
    '\u1361', '\u1362', '\u1363', '\u1364',
    '\u1365', '\u1366', '\u1367', '\u1368',
}

def _is_ethiopic(c: str) -> bool:
    cp = ord(c)
    return (
        0x1200 <= cp <= 0x137F or
        0x1380 <= cp <= 0x139F or
        0x2D80 <= cp <= 0x2DDF or
        0xAB00 <= cp <= 0xAB2F
    )

def _is_syllabic(c: str) -> bool:
    return _is_ethiopic(c) and c not in _ETHIOPIC_PUNCT


# ── Core data accessors ───────────────────────────────────────────────────────

def get_sign_inventory() -> dict[str, dict[str, Any]]:
    """Return the full sign inventory from the Geʽez sign list.

    Returns a dict mapping Unicode character → metadata dict with keys:
      char, codepoint, name, romanization, order (1-8), row_idx, col_idx,
      is_syllabic, is_punctuation
    """
    if not _SIGNLIST.exists():
        return {}
    inventory: dict[str, dict[str, Any]] = {}
    row_idx = 0
    with open(_SIGNLIST, encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            name  = parts[0].strip()
            roman = parts[1].strip()
            order = 1
            for part in parts[2:]:
                for c in part:
                    if not _is_ethiopic(c):
                        continue
                    inventory[c] = {
                        "char":           c,
                        "codepoint":      f"U+{ord(c):04X}",
                        "name":           name,
                        "romanization":   roman,
                        "order":          order,
                        "row_idx":        row_idx,
                        "col_idx":        order - 1,
                        "is_syllabic":    c not in _ETHIOPIC_PUNCT,
                        "is_punctuation": c in _ETHIOPIC_PUNCT,
                    }
                    order += 1
            row_idx += 1
    return inventory


def get_corpus_symbols() -> list[str]:
    """Return a flat list of all syllabic Ethiopic tokens from Genesis.

    Each element is a single Geʽez Unicode character (one syllabic sign).
    Verse numbers, whitespace, and Ethiopic punctuation are excluded.
    """
    if not _GENESIS.exists():
        return []
    sign_inv = get_sign_inventory()
    known_syllabic = {c for c, m in sign_inv.items() if m["is_syllabic"]}
    tokens: list[str] = []
    with open(_GENESIS, encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            stripped = line.replace("-", "").replace(" ", "")
            if stripped.isdigit():
                continue
            for chunk in line.split():
                for c in chunk:
                    if c in known_syllabic:
                        tokens.append(c)
    return tokens


def get_corpus_inscriptions() -> list[list[str]]:
    """Return word-level inscriptions (lists of syllabic sign tokens).

    Each inner list is one whitespace-delimited word from the Genesis text,
    containing only syllabic Ethiopic characters.  Words of length < 2
    are excluded (single-character words provide no bigram information).
    """
    if not _GENESIS.exists():
        return []
    sign_inv = get_sign_inventory()
    known_syllabic = {c for c, m in sign_inv.items() if m["is_syllabic"]}
    words: list[list[str]] = []
    with open(_GENESIS, encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            stripped = line.replace("-", "").replace(" ", "")
            if stripped.isdigit():
                continue
            for chunk in line.split():
                word_signs = [c for c in chunk if c in known_syllabic]
                if len(word_signs) >= 2:
                    words.append(word_signs)
    return words


def get_syllabic_inventory_filtered(min_freq: int = 3) -> list[str]:
    """Return the filtered syllabic inventory (signs appearing >= min_freq times).

    Signs are ordered by consonant row × vowel order (canonical Geʽez order).
    """
    from collections import Counter
    tokens = get_corpus_symbols()
    sign_inv = get_sign_inventory()
    freq = Counter(tokens)
    return sorted(
        [c for c, n in freq.items()
         if n >= min_freq and c in sign_inv and sign_inv[c]["is_syllabic"]],
        key=lambda c: sign_inv[c].get("row_idx", 999) * 10 + sign_inv[c].get("col_idx", 0)
    )


def corpus_statistics() -> dict[str, Any]:
    """Return summary statistics for the Geʽez Genesis corpus."""
    from collections import Counter
    tokens = get_corpus_symbols()
    inscriptions = get_corpus_inscriptions()
    sign_inv = get_sign_inventory()
    freq = Counter(tokens)
    syllabic_inv = get_syllabic_inventory_filtered()
    return {
        "n_tokens":             len(tokens),
        "n_words":              len(inscriptions),
        "n_unique_signs_raw":   len(freq),
        "inventory_size":       len(syllabic_inv),
        "n_consonant_rows":     len(set(sign_inv[c]["name"] for c in syllabic_inv if c in sign_inv)),
        "mean_word_length":     sum(len(w) for w in inscriptions) / max(1, len(inscriptions)),
        "mean_tokens_per_sign": len(tokens) / max(1, len(syllabic_inv)),
        "script_type":          "abugida-syllabic",
        "reading_direction":    "ltr",
    }
