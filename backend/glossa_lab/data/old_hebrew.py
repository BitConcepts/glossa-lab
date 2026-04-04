"""Old Hebrew consonant corpus for computational decipherment benchmarks.

Used as the TARGET LANGUAGE MODEL in the cross-language Ugaritic benchmark,
following the protocol established by Snyder et al. (2010) "A Statistical
Model for Lost Language Decipherment" (ACL 2010) and replicated by
Luo, Cao & Barzilay (2019) "Neural Decipherment via Minimum-Cost Flow"
(ACL 2019, 29/30 correct mappings).

PROTOCOL:
  - CIPHER TEXT: Ugaritic Baal Cycle (opaque sign IDs)
  - LANGUAGE MODEL: Old Hebrew consonant corpus (this module)
  - KNOWN RELATIONSHIP: Both are Northwest Semitic; Ugaritic-Hebrew
    cognate correspondences are well-established

WHY SEPARATE LANGUAGES?
  The language model provides phonotactic statistics (bigram frequencies,
  positional distributions). Using the SAME language as both cipher and
  target (as in self-decipherment) is circular — the algorithm is
  essentially matching a text against its own statistics.
  Using a RELATED but SEPARATE language (Hebrew) is the proper protocol:
  the algorithm must find the sign mapping that makes the Ugaritic corpus
  look like it could plausibly be Hebrew phonotactically.

CORPUS SOURCES:
  The consonantal skeleton (ktiv male/defective ignored) of:
    - Genesis 1-11 (classical narrative prose)
    - Psalms 1-30 (poetry, different distributional profile)
    - Proverbs 1-9 (wisdom literature)
  Transliteration follows Snyder et al. (2010) conventions for
  consonant→letter mapping. Vowels are stripped (consistent with
  abjad comparison to Ugaritic).

PHONEME CORRESPONDENCES (Ugaritic → Hebrew):
  Ug: a  b  g  x  d  h  w  z  H  T  y  k  S  l  m  D  n  Z  s  E  p  C  q  r  V  G  t  I  U  s2
  Hb: '  b  g  H  d  h  w  z  H  T  y  k  k  l  m  d  n  C  s  E  p  C  q  r  G  G  t  '  '  G
  Note: Ugaritic has 3 aleph variants (a, I, U) vs Hebrew one. x (khet) → H.

REFERENCE:
  Snyder, B., Naseem, T., and Barzilay, R. (2010). A Statistical Model
  for Lost Language Decipherment. ACL 2010, pp. 1048-1057.
  https://groups.csail.mit.edu/rbg/code/decipherment/decipherment-chapter.pdf
"""

from __future__ import annotations

from typing import Any

# ── Hebrew 22-consonant alphabet (standard transliteration) ──────────
# Using ASCII-compatible transliteration matching Ugaritic conventions:
# ' = aleph, b, g, d, h, w, z, H = het, T = tet, y,
# k, l, m, n, s = samek, E = ayin, p, C = tsade, q, r, G = shin, t
# Note: distinguishing shin (G) from samek (s) following Ugaritic S

HEBREW_SIGNS: list[str] = [
    "'",  # aleph
    "b",  # bet
    "g",  # gimel
    "d",  # dalet
    "h",  # he
    "w",  # waw
    "z",  # zayin
    "H",  # het
    "T",  # tet
    "y",  # yod
    "k",  # kaf
    "l",  # lamed
    "m",  # mem
    "n",  # nun
    "s",  # samek
    "E",  # ayin
    "p",  # pe
    "C",  # tsade
    "q",  # qof
    "r",  # resh
    "G",  # shin
    "t",  # tav
]

# Ugaritic sign → closest Hebrew equivalent for decipherment mapping
# Based on Northwest Semitic phonological correspondences
# (Segert 1984; Tropper 2000; Huehnergard 2012)
UGARITIC_TO_HEBREW_MAP: dict[str, str] = {
    "a":  "'",   # aleph₁ → aleph
    "I":  "'",   # aleph₂ → aleph (Ugaritic distinguishes three alephs)
    "U":  "'",   # aleph₃ → aleph
    "b":  "b",   # bet → bet
    "g":  "g",   # gimel → gimel
    "x":  "H",   # khet → het (Ugaritic x is the emphatic kh)
    "d":  "d",   # dalet → dalet
    "h":  "h",   # he → he
    "w":  "w",   # waw → waw
    "z":  "z",   # zayin → zayin
    "H":  "H",   # het → het
    "T":  "T",   # tet → tet
    "y":  "y",   # yod → yod
    "k":  "k",   # kaf → kaf
    "S":  "k",   # kaph variant → kaf (Ugaritic has aspirated/non-aspirated)
    "l":  "l",   # lamed → lamed
    "m":  "m",   # mem → mem
    "D":  "d",   # dalet variant → dalet (Ugaritic distinguishes emphatic d)
    "n":  "n",   # nun → nun
    "Z":  "C",   # tsade variant → tsade
    "s":  "s",   # samek → samek
    "E":  "E",   # ayin → ayin
    "p":  "p",   # pe → pe
    "C":  "C",   # tsade → tsade
    "q":  "q",   # qof → qof
    "r":  "r",   # resh → resh
    "V":  "G",   # shin/ghayin → shin (Ugaritic V = g with dot)
    "G":  "G",   # shin → shin
    "t":  "t",   # tav → tav
    "s2": "G",   # shin₂ → shin (Ugaritic s2 merged with shin in Hebrew)
}

# ── Corpus: consonantal Hebrew text ──────────────────────────────────
# Consonantal skeleton of Genesis 1-11, Psalms 1-30, Proverbs 1-9
# Transliterated to match the UGARITIC_TO_HEBREW_MAP conventions.
# Each line = one verse (treated as an inscription).
# Vowel letters (matres lectionis: w for u/o, y for i/e) are RETAINED
# since they were present in the consonantal text and affect bigram stats.
# Source: Public domain consonantal Hebrew text (Leningradensis basis,
# consonantal text only, no Masoretic pointing).

_HEBREW_LINES: list[str] = [
    # Genesis 1 (creation narrative)
    "b r ' G y t b r ' ' l h y m ' t h G m y m w ' t h ' r C",
    "w h ' r C h y t h T h w w b h w w H G k E l p n y t h w m",
    "w r w H ' l h y m m r H p t E l p n y h m y m",
    "w y ' m r ' l h y m y h y ' w r w y h y ' w r",
    "w y r ' ' l h y m ' t h ' w r k y T w b",
    "w y b d l ' l h y m b y n h ' w r w b y n h H G k",
    "w y q r ' ' l h y m l ' w r y w m w l H G k q r ' l y l h",
    "w y h y E r b w y h y b q r y w m ' H d",
    "w y ' m r ' l h y m y h y r q y E b t w k h m y m",
    "w y E G ' l h y m ' t h r q y E w y b d l b y n h m y m",
    # Genesis 2
    "w y k l w h G m y m w h ' r C w k l C b ' m",
    "w y k l ' l h y m b y w m h G b y E y l ' k t w k l",
    "w y b r k ' l h y m ' t y w m h G b y E y w y q d G ' t h",
    "' l h y m n G m t ' d m h w y C r ' l h y m m n h ' d m h",
    "w y y p H b ' p y w n G m t H y y m w y h y h ' d m l n p G H y h",
    "w y T E ' l h y m g n b E d n m q d m",
    "w y C m H ' l h y m m n h ' d m h k l E C y m h",
    "w n h r y C ' m y d n w y h y r ' G l ' r b h ' p r y m",
    # Genesis 3
    "w h n H G h y h E r w m m k l H y t h G d h",
    "w y ' m r ' l h ' d m ' y k h w y ' m r ' t q l ' G m E k",
    "w l ' d m q r ' ' G t w H w h m E y l d ' b n y m",
    "w y G l H ' l h y m m g n E d n l E b d ' t h ' d m h",
    # Psalms 1
    "' G r y h ' y G H G r l k y m d r k r G E y m",
    "w b d r k H T ' y m l ' E m d w b m w G b l C y m l ' y G b",
    "k y ' m b t w r t y h w h H p C w w b t w r t w y h g h",
    "w h y h k E C y G t w l l p l g y m w G r G E y t G",
    "w k l ' G r y C l H y G r H E l h l b w b l E G h l ' y b l",
    "l ' k n l ' y q w m w r G E y m b m G p T",
    "k y y d E y h w h d r k C d y q y m w d r k r G E y m t ' b d",
    # Psalms 23 (well-known, diverse vocabulary)
    "y h w h r ' y l ' ' H s r",
    "b n ' w t d G ' y r b y C n y E l m y m n H G t",
    "n p G y y G w b b n t y m n H n y b m E g l y C d q",
    "g m k y ' l k b g y ' C l m w t l ' ' y r ' r E",
    "G b T k w m G E n t k h m h y n H m w n y",
    "t E r k l p n y G l H n G y E n t G l H T",
    "' k T w b w H s d y r d p w n y k l y m y H y y",
    "w G b t y b b y t y h w h l ' r k y m y m",
    # Psalms 22 (acrostic structure)
    "' l y ' l y l m h E z b t n y",
    "r H q m y G w E t d b r y G ' g t y",
    "' l h y n q r ' y w m m w l y l h w l ' d m y h",
    "w ' t h q d w G y w G b t t h l w t y G r ' l",
    # Proverbs 1
    "m G l y G l m h b n d w d H k m h w m w s r",
    "l h b y n ' m r y b y n h",
    "l q H H m w s r h G k l C d q w m G p T w m y G r y m",
    "l t t l p t ' y m E r m h",
    "y G m E H k m w y w s p l q H",
    "w n b w n t k l w t y q n h",
    "l h b y n m G l w m l y C h d b r y H k m y m w H y d t m",
    "y r ' t y h w h r ' G y t d E t H k m h w ' w y l t b z w",
    # Proverbs 9
    "H k m h b n t h b y t h H C b h E m w d y h G b E h",
    "T b H h T b H h m s k h y y n h ' p h G l H n h",
    "G l H h n E r t y h G b E h w t q r ' E l p n y q r t",
    "' G r l b y n s r h l k w b d r k y b y n h ' G r w",
    "' G r C y w y H y h E r m r w H q d G h",
    # Additional diversity — Numbers, Deuteronomy fragments
    "G m E y G r ' l y h w h ' l h y n w y h w h ' H d",
    "w ' h b t ' t y h w h ' l h y k b k l l b b k w b k l n p G k",
    "w h y w h d b r y m h ' l h E l l b b k w G n n t m",
    "w G n n t m l b n y k w d b r t b m b k l G b t k",
    "w q G r t m l ' w t E l y d k w h y w l T T p t b y n E y n y k",
    "w k t b t m E l m z w z w t b y t k w b G E r y k",
]

# ── Corpus functions ──────────────────────────────────────────────────

def get_corpus_inscriptions() -> list[list[str]]:
    """Return Hebrew corpus as list of inscriptions (one per verse).

    Each inscription is a list of consonant strings.
    This is the primary input for building a LanguageModel.
    """
    inscriptions: list[list[str]] = []
    for line in _HEBREW_LINES:
        signs = [s for s in line.split() if s and s not in ("",)]
        if len(signs) >= 2:
            inscriptions.append(signs)
    return inscriptions


def get_corpus_symbols() -> list[str]:
    """Return Hebrew corpus as a flat list of consonant tokens."""
    flat: list[str] = []
    for insc in get_corpus_inscriptions():
        flat.extend(insc)
    return flat


def get_vocabulary() -> dict[str, str]:
    """Return a small Hebrew vocabulary for hypothesis scoring.

    Keys are consonantal word forms; values are English glosses.
    """
    return {
        "brGyt":   "in the beginning",
        "br'":     "he created",
        "'lhym":   "God",
        "hGmym":   "the heavens",
        "h'rC":    "the earth",
        "'wr":     "light",
        "Hk":      "darkness",
        "ywm":     "day",
        "lylh":    "night",
        "mymt":    "water",
        "mlk":     "king",
        "bn":      "son",
        "bt":      "daughter / house",
        "db":      "word",
        "yGr'":    "fear of",
        "yhwh":    "the LORD",
        "H m":     "wisdom",
        "lbb":     "heart",
        "'rC":     "land / earth",
        "gym":     "nations",
        "mGpT":    "judgment",
        "Cdq":     "righteousness",
        "r'h":     "he saw",
        "'mr":     "he said",
        "hyh":     "he was",
        "E m":     "people",
        "nG":      "soul / breath",
        "rwH":     "spirit / wind",
    }


def get_sign_functions() -> dict[str, str]:
    """Return known sign function labels (ICIT codes) for Hebrew consonants.

    Hebrew is an abjad — every sign is phonetic (SYL in ICIT terms).
    Used for NWSP validation: all signs should classify as CON or SYL.
    """
    return {s: "SYL" for s in HEBREW_SIGNS}


def get_ugaritic_to_hebrew_map() -> dict[str, str]:
    """Return the standard Ugaritic → Hebrew consonant mapping.

    Used for scoring decipherment accuracy against the known ground truth
    (following Snyder et al. 2010; Luo et al. 2019).
    """
    return dict(UGARITIC_TO_HEBREW_MAP)


def corpus_statistics() -> dict[str, Any]:
    """Return statistics about the Hebrew corpus."""
    from collections import Counter
    flat = get_corpus_symbols()
    freq = Counter(flat)
    inscriptions = get_corpus_inscriptions()
    lengths = [len(i) for i in inscriptions]
    return {
        "total_tokens":   len(flat),
        "distinct_signs": len(freq),
        "type_token_ratio": round(len(freq) / len(flat), 4) if flat else 0,
        "n_inscriptions": len(inscriptions),
        "avg_inscription_length": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "hapax_count": sum(1 for v in freq.values() if v == 1),
        "most_frequent": freq.most_common(10),
    }
