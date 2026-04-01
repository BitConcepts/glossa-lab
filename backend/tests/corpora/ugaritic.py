"""Ugaritic corpus for decipherment benchmarking.

Ugaritic (c. 1400-1190 BCE) is a Northwest Semitic language written
in a cuneiform alphabet of 30 signs. It was deciphered in the 1930s.
The decipherment is well-established, making it an ideal benchmark.

We encode excerpts from the Baal Cycle in two forms:
  1. "Undeciphered" — using opaque sign IDs (U01..U30)
  2. "Deciphered" — the known transliteration values

The test verifies that our structural analysis of the undeciphered
form reveals patterns consistent with the known linguistic structure.

Ugaritic alphabet (30 signs, North Semitic order):
  a b g x d h w z H T y k S l m D n Z s E p C q r V G t I U s2
  (simplified ASCII transliteration)
"""

from __future__ import annotations

import random
from typing import Any

# ── Ugaritic sign inventory ────────────────────────────────────────

# 30 signs in traditional order, with opaque IDs
UGARITIC_SIGNS = [
    "a", "b", "g", "x", "d", "h", "w", "z", "H", "T",
    "y", "k", "S", "l", "m", "D", "n", "Z", "s", "E",
    "p", "C", "q", "r", "V", "G", "t", "I", "U", "s2",
]

# Map: real transliteration → opaque sign ID
_SIGN_TO_ID = {sign: f"U{i + 1:02d}" for i, sign in enumerate(UGARITIC_SIGNS)}
_ID_TO_SIGN = {v: k for k, v in _SIGN_TO_ID.items()}

# ── Corpus: Baal Cycle excerpts (simplified transliteration) ──────
# Words separated by dots in original; we use space here.
# These are representative phrases from KTU 1.1-1.6

_BAAL_CYCLE_LINES = [
    # KTU 1.1-1.2: Yamm's demand and El's council
    "y m l k . b E l",
    "w y E n . b E l . a l I y n",
    "h l m . t m x S . a r S",
    "a l . t S t . b n . I l m",
    "k . y r d . b E l . b a r S",
    "y s a . G l m . b E l",
    "t s p r . I l . d . p I d",
    "a n k . b E l . s p n",
    "w y E n . k V r t . m l k",
    "S m E . l . b t l t . E n t",
    "y p E . I l . d . p I d",
    "k . m l a k . y m",
    "b n . d g n . y d E . a r S",
    "t E d b . d b H . l . I l m",
    "h m . m t . a l I y n . b E l",
    "w y E n . l p n . I l . d . p I d",
    "I l . y t b . b m r z H",
    "S m . b n y . b n w t . h k l",
    "m l k . E l . d r k t",
    "y d E . k s a . I l",
    "b y m . S b E . n q m d",
    "a l . t q r b . b n . I l m",
    "k t r . w x s s . y b a",
    "y s q . k s . b y d h",
    "a n t . t s p r . m l a k t",
    "b E l . y m l k . E l . a r S",
    "w t E n . b t l t . E n t",
    "y r d . l a r S . b E l",
    "t E d b . d b H . S l m m",
    "a l . y m t . b E l . a l I y n",
    # KTU 1.3-1.4: Baal's palace and battles
    "t b n . b t . l . b E l",
    "k . y b n . h k l . k s p",
    "w y s U . b E l . E n t . E n t",
    "b n . I l m . y S t H w n",
    "h l m . y m x S . m t . b E l",
    "w y S l H . m l a k m . b n . y m",
    "k t r . w x s s . y T b x . b E l",
    "a l . y r d . b n . I l m . l a r S",
    "y s a . q r n . b E l . G z r",
    "l . y t n . b E l . q l h",
    "t E d b . Z b H . l . I l m",
    "b D . g p n . w . U g r",
    "S m E . a n t . b t l t . E n t",
    "t s U . k s . b y d . b E l",
    "w t E n . r b t . a V r t . y m",
    "y S t . b E l . k s I h . b y d h",
    "h m . t m x S . a r S . w S m m",
    "y d E . k l . b n . I l m . s p r",
    "m l k . E l m . b E l . y m l k",
    # KTU 1.5-1.6: Baal's death and resurrection
    "m t . y s U . n p S h . l . S a l",
    "a l . y m t . b E l . b n . d g n",
    "w y r d . b E l . b a r S",
    "E n t . t b k y . l . b E l",
    "t S a . G l m . I l . l . m t",
    "h l m . S m S . t Z H r",
    "y q m . b E l . a l I y n",
    "w y t b . l . k s I . m l k",
    "y C E . V D . m t . l . I l",
    "t E n . a n t . l . b E l . a l I y n",
    "S b E . S n t . y t b . m t",
    "b V m n . S n t . y q m . b E l",
    "k . y t b . l . k s I . m l k h",
    "a l . t S t . b n . I l m . b a r S",
    "h m . y r d . a l I y n . b E l",
    "t q l . S m m . S m n . l . a r S",
    "w y E n . l T p n . I l . d . p I d",
    "k . m l k . b E l . y m l k",
    "a n k . S p S . b E l . a l I y n",
    "w y s a . l . k s I . m l k h",
    "d b H . y E S . l . I l m",
    "b E l . t E z . w t E D d",
    "D . m t . b n . I l m . y m t",
    "S m E . l . b t l t . E n t . a n t",
    # KTU 1.6: Final restoration
    "t g r S . m t . l . k s I",
    "m l k . E l . y S b . k s I h",
    "w y d E . b E l . a l I y n . k l . a r S",
    "a n t . t E D d . l . b E l",
    "S l m . d b H . l . I l m . r b m",
    "y T b . b E l . b h k l h",
    "b n . d g n . y t b . l . k s I . m l k h",
    "w y S t H w n . I l m . l . b E l",
    "S m E . q l . b E l . b S m m",
]


def get_deciphered_corpus() -> dict[str, Any]:
    """Return the corpus in known transliteration (the 'answer')."""
    inscriptions = []
    for line in _BAAL_CYCLE_LINES:
        # Remove word dividers and split into signs
        signs = [ch for ch in line.split() if ch != "."]
        inscriptions.append(signs)

    flat = [s for insc in inscriptions for s in insc]
    return {
        "inscriptions": inscriptions,
        "flat_signs": flat,
        "sign_inventory": UGARITIC_SIGNS,
        "alphabet_size": len(UGARITIC_SIGNS),
    }


def get_undeciphered_corpus() -> dict[str, Any]:
    """Return the corpus with opaque sign IDs (simulating undeciphered state)."""
    deciphered = get_deciphered_corpus()
    inscriptions = []
    for insc in deciphered["inscriptions"]:
        inscriptions.append([_SIGN_TO_ID.get(s, s) for s in insc])

    flat = [s for insc in inscriptions for s in insc]
    return {
        "inscriptions": inscriptions,
        "flat_signs": flat,
        "alphabet_size": deciphered["alphabet_size"],
    }


def get_answer_key() -> dict[str, str]:
    """Return the mapping from opaque IDs to real transliterations."""
    return dict(_ID_TO_SIGN)


# ── Known linguistic properties (for test assertions) ─────────────

KNOWN_PROPERTIES = {
    # Most common signs in Ugaritic texts
    "most_frequent_signs": ["l", "b", "E", "y", "m", "n", "I", "a", "k", "d"],
    # Signs that frequently appear at word-initial position
    "common_initial": ["b", "y", "w", "t", "k", "l", "a", "m"],
    # Signs that frequently appear at word-final position
    "common_final": ["l", "m", "n", "t", "k", "d", "S", "H"],
    # The language is clearly linguistic (entropy in linguistic range)
    "expected_linguistic": True,
    # Known word patterns (common Ugaritic words)
    "known_words": {
        "bEl": "Baal (the god)",
        "mlk": "king",
        "Il": "El (the god)",
        "bn": "son",
        "arS": "earth",
        "Sm": "name",
        "dbH": "sacrifice",
        "bt": "house",
    },
}
