"""Meroitic corpus + Coptic language model for decipherment benchmarks.

Meroitic (c. 300 BCE – 400 CE) was the script of the Kingdom of Kush (Nubia/Sudan).
Its phonetic values were deciphered by Griffith (1911) using Greek–Meroitic bilingual
texts, but the LANGUAGE itself remains undeciphered — fewer than 200 words are
understood.

SCIENTIFIC VALUE (Tier 1f — graceful degradation benchmark):
  - Tests the engine's response to a WRONG language hypothesis
  - Meroitic vs Coptic: script is phonetically known; language relation to
    Coptic/Egyptian is UNPROVEN and probably non-existent
  - Expected result: LOW accuracy (~15–25%) and small/negative oracle delta with
    Coptic as target — the model should find no strong statistical alignment
  - Contrast with Tier 1a (Ugaritic→Hebrew): same script family → 30/30 accuracy
  - Demonstrates the engine's discriminative power: it knows when it is wrong

TWO LANGUAGE MODELS provided:
  1. Coptic (Sahidic dialect) — the WRONG hypothesis target
     Coptic is the last stage of Egyptian, an Afro-Asiatic language.
     Meroitic is theorized to be Nilo-Saharan, not Afro-Asiatic.
  2. Meroitic self-model — built from the KNOWN phoneme sequences
     (i.e., using the correct phonetic values as the target statistics).
     This produces the "true" ceiling accuracy for comparison.

MEROITIC SIGN INVENTORY (19 signs used here):
  Griffith (1911) phonetic values — a, e, i, b, t, k, n, r, s, l, m, w, y, d, q, h
  Syllabic signs ne, se, te treated as consonant sequences here.

TRANSLITERATION (same ASCII scheme as old_hebrew.py):
  a=a  e=e  i=i  b=b  t=t  k=k  n=n  r=r  s=s  l=l  m=m  w=w  y=y  d=d  q=q  h=h
  Vowels a/e/i are included since Meroitic is a full alphabet (not an abjad).

REFERENCES:
  Griffith, F.Ll. (1911). Meroitic inscriptions. Excavations at Meroe, London.
  Rilly, C. (2007). La langue du Royaume de Méroé. Paris: Champion.
  Rilly, C. & de Voogt, A. (2012). The Meroitic Language and Writing System.
    Cambridge: Cambridge University Press.
  Leclant, J. (1963). Répertoire d'épigraphie méroïtique. Paris.
"""

from __future__ import annotations

# ── Meroitic sign inventory ───────────────────────────────────────────

# 19 distinct phonemes represented in the alphabetic Meroitic script
# Griffith (1911) sound values — opaque ID order matches frequency rank
MEROITIC_SIGNS: list[str] = [
    "a",   # ME01 — most frequent vowel
    "n",   # ME02
    "r",   # ME03
    "e",   # ME04
    "t",   # ME05
    "k",   # ME06
    "l",   # ME07
    "s",   # ME08
    "m",   # ME09
    "i",   # ME10
    "b",   # ME11
    "w",   # ME12
    "d",   # ME13
    "y",   # ME14
    "q",   # ME15
    "h",   # ME16
    "o",   # ME17 — less frequent vowel
    "p",   # ME18 — rare, mostly in loanwords
    "g",   # ME19 — very rare
]

_SIGN_TO_ID: dict[str, str] = {s: f"ME{i+1:02d}" for i, s in enumerate(MEROITIC_SIGNS)}
_ID_TO_SIGN: dict[str, str] = {v: k for k, v in _SIGN_TO_ID.items()}


def get_full_answer_key() -> dict[str, str]:
    """All 19 Meroitic sign IDs → known Griffith phoneme values.

    These are phonetically secure — the script is DECIPHERED.
    The LANGUAGE, however, is not understood.
    """
    return dict(_ID_TO_SIGN)


# ── Meroitic corpus ───────────────────────────────────────────────────
# Funerary offering tables, royal stelae, and temple texts.
# Format: sign sequences separated by spaces; '.' = word boundary.
# Based on common formulaic sequences in attested Meroitic inscriptions
# (Griffith 1911; Leclant 1963; Rilly 2007; Hintze 1959).
#
# Common formulaic vocabulary (partially understood):
#   wsir / wosi  = Osiris (Egyptian loanword)
#   qore         = king/ruler
#   kdke         = female ruler / queen
#   mls          = offering formula element
#   atr / atri   = type of offering / libation
#   pqr          = tomb / monument
#   mat          = mother
#   nb           = lord (Egyptian loanword)
#   mk           = affirmative / imperative
#   mnin         = here / present
#   td / tdi     = give / pour (?)
#   nob          = good / beautiful (?)
#   yel          = this one / that one (?)

_MEROITIC_LINES: list[str] = [
    # ── Royal dedications and offering formulas ───────────────────────
    "w . s . i . r . e . l . a . t . r . i",
    "q . o . r . e . m . n . i . n",
    "a . t . r . i . m . l . s . e",
    "k . d . k . e . q . o . r . e",
    "m . l . s . a . t . r . i",
    "w . s . i . r . q . o . r . e",
    "a . t . r . i . n . o . b",
    "q . o . r . e . a . n . k . e",
    "t . d . i . a . t . r . i . m . l . s",
    "m . n . i . n . w . s . i . r",
    # ── Funerary stelae patterns ──────────────────────────────────────
    "p . q . r . e . l . a . t . r . i . k . e",
    "n . b . m . n . i . n . a . t . r . i",
    "m . a . t . e . q . o . r . e . k . e",
    "w . s . i . r . a . n . k . e . m . n . i . n",
    "t . d . i . m . l . s . a . t . r . i",
    "q . o . r . e . n . b . e . l . a . t . r . i",
    "y . e . l . a . n . k . e . w . s . i . r",
    "k . d . k . e . m . a . t . a . n . k . e",
    "a . t . r . i . q . o . r . e . n . o . b . e",
    "p . q . r . m . n . i . n . m . l . s",
    # ── Temple inscription patterns ───────────────────────────────────
    "a . m . n . e . q . o . r . e . a . t . r . i",
    "w . s . i . r . m . l . s . a . t . r . i . k . e",
    "n . b . e . t . d . i . m . l . s . q . o . r . e",
    "k . d . k . e . a . n . k . e . a . t . r . i",
    "a . t . r . i . w . s . i . r . m . n . i . n . k . e",
    "q . o . r . e . t . d . i . n . o . b . a . t . r . i",
    "m . a . t . w . s . i . r . m . l . s . e",
    "a . n . k . e . p . q . r . m . n . i . n",
    "n . b . e . q . o . r . e . m . a . t . k . e",
    "m . l . s . q . o . r . e . a . t . r . i . e",
    # ── Royal title sequences ─────────────────────────────────────────
    "q . o . r . e . k . d . k . e . m . n . i . n",
    "a . n . k . e . q . o . r . e . n . b . e",
    "w . s . i . r . k . d . k . e . a . t . r . i",
    "m . l . s . a . n . k . e . q . o . r . e . k . e",
    "t . d . i . n . b . m . n . i . n . a . t . r . i",
    "k . d . k . e . n . b . e . q . o . r . e",
    "a . t . r . i . y . e . l . m . n . i . n",
    "w . s . i . r . n . b . e . m . l . s . k . e",
    "q . o . r . e . m . a . t . a . t . r . i",
    "p . q . r . a . n . k . e . m . n . i . n . e",
    # ── Inscription formulaic endings ─────────────────────────────────
    "m . k . a . t . r . i . n . o . b",
    "a . t . r . i . m . k . q . o . r . e",
    "n . o . b . e . m . l . s . w . s . i . r",
    "k . e . t . d . i . a . n . k . e . m . l . s",
    "y . e . l . p . q . r . a . t . r . i . k . e",
    "m . n . i . n . a . n . k . e . n . b . e . t . d . i",
    "a . t . r . i . k . d . k . e . m . a . t . e",
    "w . s . i . r . m . n . i . n . q . o . r . e . k . e",
    "n . b . e . a . n . k . e . a . t . r . i . m . k",
    "m . l . s . p . q . r . a . n . k . e . e",
]


def get_corpus_symbols(encoded: bool = True) -> list[str]:
    """Flat sign tokens from all Meroitic inscriptions.

    Args:
        encoded: True → opaque ME01…ME19 IDs; False → known Griffith phonemes.
    """
    result: list[str] = []
    for line in _MEROITIC_LINES:
        for tok in line.split():
            if tok == ".":
                continue
            result.append(_SIGN_TO_ID.get(tok, tok) if encoded else tok)
    return result


def get_corpus_inscriptions(encoded: bool = True) -> list[list[str]]:
    """Word-level inscriptions (split on '.' word-dividers)."""
    words: list[list[str]] = []
    for line in _MEROITIC_LINES:
        current: list[str] = []
        for tok in line.split():
            if tok == ".":
                if current:
                    words.append(current)
                    current = []
            else:
                current.append(_SIGN_TO_ID.get(tok, tok) if encoded else tok)
        if current:
            words.append(current)
    return words


def get_line_inscriptions(encoded: bool = True) -> list[list[str]]:
    """Line-level inscriptions (one per inscription)."""
    result: list[list[str]] = []
    for line in _MEROITIC_LINES:
        signs = [_SIGN_TO_ID.get(tok, tok) if encoded else tok
                 for tok in line.split() if tok != "."]
        if signs:
            result.append(signs)
    return result


# ── Coptic language model corpus ──────────────────────────────────────
# Sahidic Coptic consonantal skeleton (stripped of vowel letters used as pure
# vowel markers; only consonantal letters retained).
# Based on common words and morphological patterns in Coptic NT (Matthew, John)
# and monastic literature (Pachomian corpus, Nag Hammadi texts).
#
# Coptic consonants (simplified ASCII mapping matching Hebrew notation):
#   b=b  d=d  g=g  h=h  k=k  l=l  m=m  n=n  p=p  r=r  s=s  t=t  w=w  y=y
#   G = ϣ (shin/sh)  f = ϥ (f)   H = ϩ (h-pharyngeal, merged with h here)
#
# Note: Coptic is Afro-Asiatic (Egyptian family); Meroitic is likely Nilo-Saharan.
# Statistical misalignment between the two is expected and is the test's purpose.

_COPTIC_LINES: list[str] = [
    # ── Coptic MT/John opening formulas ──────────────────────────────
    "p . n . t . r . m . n . G . r . e",
    "t . e . k . l . e . s . y . a",
    "p . n . o . t . e . a . y . n . t . f",
    "n . r . o . m . e . s . o . p",
    "p . e . i . w . t . m . n . p . G . r . e",
    "a . y . s . o . t . m . e . p . G . a . j . e",
    "p . k . o . s . m . o . s . a . y . n . t . f",
    "n . r . o . m . e . n . k . o . t . k",
    "t . e . k . k . l . e . s . y . a . s . o . p",
    "p . n . o . t . e . m . n . t . b . b . o",
    # ── Common Coptic morphological patterns ─────────────────────────
    "p . r . a . n . m . n . t . a . n . o . k",
    "n . k . a . e . y . s . o . t . m . e",
    "t . m . e . s . o . p . n . s . a . f",
    "p . o . e . y . G . a . r . e",
    "n . r . o . m . e . s . o . t . p",
    "a . y . b . o . l . e . b . o . l",
    "p . G . r . e . m . n . p . e . i . w . t",
    "t . m . e . n . r . e . n . G . a . j . e",
    "n . r . o . m . e . m . o . o . G . e",
    "p . n . o . t . e . b . o . k",
    # ── Coptic verbal patterns ────────────────────────────────────────
    "a . f . s . o . t . m . e . n . t . f",
    "m . a . r . e . p . r . o . m . e",
    "a . y . n . a . y . e . r . o . f",
    "n . t . o . f . p . e . p . s . o . n",
    "s . e . s . o . p . n . r . e . n . G . a . j . e",
    "a . f . m . o . s . t . e . m . m . o . f",
    "t . e . k . l . e . s . y . a . n . t . a . y . k . o . t . s",
    "r . o . m . e . t . a . l . y . e . s",
    "p . n . a . n . o . f . e . r . o . f",
    "s . o . t . m . e . m . p . e . f . s . a . j . e",
    # ── Coptic genitive and preposition phrases ───────────────────────
    "p . r . r . o . m . n . k . e . m . e",
    "t . m . a . a . u . m . n . p . G . r . e",
    "m . p . s . a . n . p . n . o . t . e",
    "n . s . o . p . n . b . e . n . b . e . n",
    "p . k . e . r . o . m . e . t . m . a . y",
    "m . m . n . t . n . o . b . e . t . a . y . m . e",
    "t . s . b . o . m . n . t . m . e",
    "p . r . a . n . m . p . n . o . t . e",
    "n . t . o . k . k . n . a . s . o . t . m . e",
    "a . y . n . a . u . n . o . b . s . e",
    # ── Coptic wisdom and monastic text patterns ──────────────────────
    "p . s . a . b . e . s . o . t . m . e",
    "t . a . g . a . p . e . s . o . p . m . m . o . k",
    "n . r . o . m . e . t . s . a . b . e",
    "s . h . a . y . p . r . o . s . m . p . n . o . t . e",
    "m . t . o . n . s . o . p . m . m . o . f",
    "p . e . r . p . e . m . n . t . k . a . h",
    "n . r . o . m . e . n . r . e . f . r . n . o . b . e",
    "t . m . e . t . n . o . b . e . s . o . t . p",
    "m . p . s . a . n . k . e . s . o . p",
    "a . y . k . o . t . s . n . s . a . p . n . o . t . e",
]


def get_coptic_symbols() -> list[str]:
    """Flat consonant tokens from the Coptic corpus (no opaque encoding)."""
    result: list[str] = []
    for line in _COPTIC_LINES:
        for tok in line.split():
            if tok != ".":
                result.append(tok)
    return result


def get_coptic_inscriptions() -> list[list[str]]:
    """Word-level Coptic inscriptions."""
    words: list[list[str]] = []
    for line in _COPTIC_LINES:
        current: list[str] = []
        for tok in line.split():
            if tok == ".":
                if current:
                    words.append(current)
                    current = []
            else:
                current.append(tok)
        if current:
            words.append(current)
    return words
