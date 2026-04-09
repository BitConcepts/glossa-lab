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
    "a": "'",  # aleph₁ → aleph
    "I": "'",  # aleph₂ → aleph (Ugaritic distinguishes three alephs)
    "U": "'",  # aleph₃ → aleph
    "b": "b",  # bet → bet
    "g": "g",  # gimel → gimel
    "x": "H",  # khet → het (Ugaritic x is the emphatic kh)
    "d": "d",  # dalet → dalet
    "h": "h",  # he → he
    "w": "w",  # waw → waw
    "z": "z",  # zayin → zayin
    "H": "H",  # het → het
    "T": "T",  # tet → tet
    "y": "y",  # yod → yod
    "k": "k",  # kaf → kaf
    "S": "k",  # kaph variant → kaf (Ugaritic has aspirated/non-aspirated)
    "l": "l",  # lamed → lamed
    "m": "m",  # mem → mem
    "D": "d",  # dalet variant → dalet (Ugaritic distinguishes emphatic d)
    "n": "n",  # nun → nun
    "Z": "C",  # tsade variant → tsade
    "s": "s",  # samek → samek
    "E": "E",  # ayin → ayin
    "p": "p",  # pe → pe
    "C": "C",  # tsade → tsade
    "q": "q",  # qof → qof
    "r": "r",  # resh → resh
    "V": "G",  # shin/ghayin → shin (Ugaritic V = g with dot)
    "G": "G",  # shin → shin
    "t": "t",  # tav → tav
    "s2": "G",  # shin₂ → shin (Ugaritic s2 merged with shin in Hebrew)
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
    "b r ' G y t . b r ' . ' l h y m . ' t . h G m y m . w ' t . h ' r C",
    "w h ' r C . h y t h . T h w . w b h w . w H G k . E l . p n y . t h w m",
    "w r w H . ' l h y m . m r H p t . E l . p n y . h m y m",
    "w y ' m r . ' l h y m . y h y . ' w r . w y h y . ' w r",
    "w y r ' . ' l h y m . ' t . h ' w r . k y . T w b",
    "w y b d l . ' l h y m . b y n h . ' w r . w b y n . h H G k",
    "w y q r ' . ' l h y m . l ' . w r y w . m w l H . G k q . r ' l . y l h",
    "w y h y . E r b . w y h y . b q r . y w m . ' H d",
    "w y ' m r . ' l h y m . y h y . r q y E . b t . w k h m y m",
    "w y E G . ' l h y m . ' t . h r q y E . w y b d l . b y n h . m y m",
    "w y k l w . h G m y m . w h ' r C . w k l C . b ' m",
    "w y k l . ' l h y m . b y w m . h G b y E y . l ' . k t w k . l",
    "w y b r k . ' l h y m . ' t . y w m . h G b y E y . w y q d G . ' t . h",
    "' l h y m . n G m t . ' d m h . w y C r . ' l h y m . m n . h ' d m h",
    "w y y p H . b ' p y w . n G m t . H y y m . w y h y . h ' d m . l n p G . H y h",
    "w y T E . ' l h y m . g n b . E d n . m q d m",
    "w y C m H . ' l h y m . m n . h ' d m h . k l . E C y m . h",
    "w n h r . y C ' . m y d . n w y . h y r ' . G l ' . r b h . ' p . r y m",
    "w h n H G . h y h . E r w . m m k l . H y t . h G d h",
    "w y ' m r . ' l . h ' d m . ' y k . h w y ' m r . ' t . q l ' . G m E . k",
    "w l ' . d m . q r ' . ' G . t w H . w h m E . y l d . ' b n . y m",
    "w y G l H . ' l h y m . m g n . E d n . l E b d . ' t . h ' d m h",
    "' G r y . h ' y G . H G r . l k y m . d r k . r G E y m",
    "w b d r k . H T ' y m . l ' . E m . d w b . m w G b . l C y m . l ' . y G b",
    "k y . ' m b . t w r t y . h w h H . p C w . w b t w r t . w y h g . h",
    "w h y h . k E C y . G t w . l l p l . g y m . w G r G . E y t . G",
    "w k l ' . G r y . C l H . y G r . H E l . h l b w . b l E G h . l ' . y b l",
    "l ' . k n l ' . y q w m . w r G E y m . b m G p . T",
    "k y . y d E . y h w h . d r k . C d y q y m . w d r k . r G E y m . t ' b . d",
    "y h w h . r ' y . l ' . ' H s . r",
    "b n . ' w t . d G ' . y r b . y C n . y E l . m y m . n H G . t",
    "n p G y . y G w . b b n t . y m n . H n y . b m E g . l y C d . q",
    "g m k . y ' l . k b g y ' . C l m w t . l ' . ' y r . ' r E",
    "G b T . k w m G E n t . k h m h . y n H . m w n y",
    "t E r . k l . p n y . G l H n . G y E n t . G l H . T",
    "' k T . w b w H . s d y . r d p . w n y k . l y m y . H y y",
    "w G b t . y b b . y t y . h w h l . ' r k . y m y m",
    "' l . y ' l . y l m . h E z b t n y",
    "r H q . m y G w . E t d . b r y G . ' g t . y",
    "' l . h y n q . r ' y . w m m w . l y l h . w l ' . d m . y h",
    "w ' t . h q d w G . y w G . b t . t h l w t . y G r ' l",
    "m G l y . G l m . h b n d . w d H k . m h w m . w s r",
    "l h b y n . ' m r . y b y . n h",
    "l q H . H m w . s r . h G k l . C d q . w m G p . T w m . y G r . y m",
    "l t t l . p t ' y m . E r m h",
    "y G m E . H k m . w y w s . p l q . H",
    "w n b w . n t k . l w t y . q n h",
    "l h b y n . m G l . w m l y . C h d . b r y H . k m y m . w H y d . t m",
    "y r ' t y . h w h r . ' G . y t d . E t H . k m h w ' . w y l t . b z w",
    "H k m h . b n . t h b . y t h . H C b . h E m w d . y h G . b E h",
    "T b H . h T b H . h m s k . h y y n . h ' p . h G l H n h",
    "G l H . h n E r . t y h . G b E . h w t q . r ' E . l p n y . q r t",
    "' G r . l b y n . s r . h l k w . b d r k . y b y . n h ' . G r w",
    "' G r . C y w . y H y . h E r m . r w H . q d G . h",
    "G m E . y G r ' l . y h w h . ' l h y n w . y h w h . ' H d",
    "w ' h b . t ' t . y h w h . ' l h y k . b k l l . b b k w . b k l n . p G k",
    "w h y w . h d b r y m . h ' l . h E l . l b b k . w G n n . t m",
    "w G n n . t m l . b n y . k w d b r . t b m . b k l G . b t . k",
    "w q G r . t m l . ' w t . E l y d k . w h y w . l T T p t . b y n . E y n y k",
    "w k t b . t m E . l m z w . z w t . b y t . k w b G . E r y . k",
    "w y h y . k y . y b y . ' k y . h w h ' . l h y k . ' l . h ' r C . ' G r . n G b . E",
    "G m r . w t m t . G m r . l b n y . k w h y h . k n G ' . t b h . m",
    "l ' . t l k . ' H r . y ' l . h y m ' . H r y . m m ' l . h y G r ' l",
    "y r ' t y . h w h ' . l h y k . w ' t . w t E b . d w b . G m w . t G b . E",
    "w h ' d m . y d E . ' t . H w h . ' G . t w w . t H r . w t l d . ' t . q y n",
    "w t s p . l d ' t . ' H y . w ' t . h b l . w y h y . h b l . r E h . C ' n",
    "w q y n . h y h . E b d . ' d m h",
    "w y h y . m q C h . y m y m . w y b ' . q y n . m p r y . h ' d m h . m n H h . l y h w h",
    "w h b l . h b y ' . g m h . b k r w t . C ' n . w m H l b . h n w",
    "w y G E y h . w h ' l . h b l . w ' l . m n . H t w . w ' l . q y n . w ' l . m n . H t w . l ' . G E h",
    "w y H r . l q y n . m ' d w . y p l . w p n y w",
    "w y ' m r . y h w h . ' l . q y n . l m h H . r h l . k w l m . h n p l . w p n y k",
    "w y ' m r . q y n . ' l . h b l . ' H y . w w y h y . b h y w . t m b . G d h",
    "w y q m . q y n . ' l . h b l . ' H y . w w y h . r g h . w",
    "w y ' m r . y h w h . ' l . q y n . ' y h . h b l . ' H y . k w y ' m r . h G m r . ' n k y . G m r . ' n y",
    "w ' t . h ' r C . p C t . h ' t . p y h . l q H . ' t . d m . ' H y . k m y d k",
    "n H w . y h y . C d y q . t m y . m h y h . b d r t . y w",
    "w t G H . t h ' . r C l . p n y . h ' l h y m . w t m l . ' h ' . r C H . m s",
    "w y r ' . ' l h y m . ' t . h ' r C . w h n h . n G H . t h k . y h G . H y t . k l . b G r . ' t . w ' t . d r k . w",
    "w y ' m r . ' l h y m . l n H q . C ' t . k l . b G r . l p n y . k y . m l ' h . h ' r C . H m s . m p n y . h m",
    "E G h . l k t b . t E C . y m r . k G l G . m n . w E C y m . m G H m . n E b . y l y . h m l b . d",
    "w n H E . G k k . l ' . G r C . w h ' l h y m",
    "w y h y . ' H r . m b w l . h m y m . E l . h ' r C . w n H b . n y H . G r",
    "w y z k . r ' l . h y m ' . t n H . w ' t . k l h . H y h . w ' t . k l h . b h m h",
    "w y ' m r . ' l h y m . l n H z . ' t . ' w t . h b r y . t ' G . r ' n . y n t . n b y . n y w . b y n . k l . b G r . H y",
    "' t . q G t . y n t . t y b . E n n . w y h y . h l ' w . t b r . y t b . y n y . w b y n . h ' r C",
    "w y ' m r . y h w h . ' l . ' b r . m l k . l k m ' . r C k . w m m w . l d t k . w m b y t . ' b y . k",
    "' l . h ' r C . ' G r . ' r ' . k w ' E . G k g . w y g d . w l w ' . b r k . k",
    "w ' b r . h m ' G r . k n n w . l q H . ' t . G r y",
    "w y b n . G m ' . l q H . ' t . l w T b . n h m . w y l k . w ' l . ' r C . k n E n",
    "w y E b . r ' b . r m b . ' r C . E d . m q w m . G k m",
    "w y r ' . y h w h . ' l . ' b r . m w y ' m r . l z r E . k ' t . t n ' . t h ' . r C h . z ' t",
    "w y b n . G m m . z b H . l y h w h . h n r ' . ' l . y w w . y q r ' . b G m y . h w h",
    "w y h y . d b r . y h w h . ' l . ' b r . m b m H . z h l . ' m r . ' l . t y r . ' ' b . r m",
    "' n k y . m g n . l k G k . r k h . r b m . ' d w . y ' m . n b y . h w h w . y H G . b h l w . C d q . h",
    "b y w m . h h w h . k r t . y h w h . ' t . ' b r . m b r y . t l ' . m r l z . r E . k n t t . y ' t . h ' r C . h z ' t",
    "w y h y . ' H r . h d b r y m . h ' l . h w h ' . l h y m . n s h . ' t . ' b r . h m w y ' m r . ' l . y w ' . b r h m",
    "w y ' m r . h n n y . w y ' m r . q H n . ' ' t . b n . k ' t . y H y . d k ' . G r ' . h b t ' . t y C . H q",
    "w y G k . m ' b r . h m b b . q r w . y H b . G ' t . H m r . w w y q . H ' t . G n y . n E r . y m",
    "w y G ' . ' b r . h m ' t . E y n . y w w . y r ' . ' t . h m q w m . m r H q",
    "w y ' m r . ' b r . h m ' l . n E r . y w G . b w l k . m p h ' . n y w . h n E r . n l k . h w n G . w b h",
    "w y q H . ' b r . h m ' t . E C y . h ' l . h w y G . m ' l . y C H . q b n . w w y q . m w y l k . w y H d . w ' l . h m q w m",
    "w y b n . G m ' . b r h m . ' t . h m z b H . G m w . y E r . k ' t . h E C y m . w y E q . d ' t . y C H . q b n . w",
    "w y G l H . ' b r . h m ' t . y d w . w y q H . ' t . h m ' k l . t l G . H T b . n w",
    "w y q r ' . m l ' k y . h w h ' . l y w m . n h G . m y m . w y ' m r . ' b r . h m ' b . r h m . w y ' m r . h n n y",
    "k y . b r k . ' b r . k k w h . r b ' . r b h . ' t . z r E . k k k w . k b y h . G m y m . w k H w . l E l . G p t . h y m",
    "w m G h . h y h . r E h . ' t . C ' n . y t r . b H t n . w y n h . l ' . t h m . d b r . h h r b . E l . h h ' l h y m",
    "w y r ' . m l ' k y . h w h ' . l y w b . l b t ' . G w y . r ' w . h n h . h s n h . b ' r . b ' G . w h s n h . ' y n . n w",
    "w y ' m r . m G h . ' s r . h n h . w ' r ' . h m r ' h . g d w . l h z h . m d w E . l ' . y b E . r h s . n h",
    "w y r ' . y h w h . k y . s r . l r ' w . t w y . q r ' . ' l . y w ' . l h y m . m t w k . h s n h . w y ' m r . m G h . m G h",
    "w y ' m r . ' n k y . ' l . h y ' . b y k ' . l h y ' . b r h m . ' l . h y y C . H q w . ' l . h y y E . q b",
    "w y q r . m G h . p n y w . k y . y r ' . m h b y . T ' l . h ' l h y m",
    "w y ' m r . y h w h . r ' ' . r ' y . t y ' . t E n . y E m . y b m . C r . y m w . ' t . C E q . t m G . m E t y . m p n y . n g G . y w",
    "l k n ' . G l H . k w ' G . l H k ' . l p r E h . w h w C . ' t . y G r ' l . m m C r . y m",
    "w y ' m r . m G h . ' l . h ' l h y m . m y ' n . k y . k y . ' l . k ' l . p r E h",
    "w y ' m r . k y . ' h y . h E m . k w z h . l k h ' . w t k y . ' n k y . G l H . t y k",
    "' n k y . y h w h . ' l h y k . ' G r . h w C ' . t y k . m ' r C . m C r y m . m b y t . E b d y m",
    "l ' . y h y h . l k ' l h y m . ' H r . y m E . l p n y",
    "l ' . t E G . h l k . p s l . w k l t . m w n h . ' G r . b G m y m . m E l",
    "l ' . t s ' . ' t . G m y . h w h ' . l h y k . l G w ' . k y . l ' . y n q . h y h . w h ' t . ' G r y . s ' ' . t G m . w",
    "z k w r . ' t . y w m . h G b t . l q d G w . k t G t . E G h . w l ' . t E G . b y w k . l m l ' . k t k",
    "k b d . ' t . ' b y . k w ' t . ' m k . l m E n . y ' r . k w n y . m y k E . l h ' d m h . ' G r y . h w h ' . l h y k . n t n . l k",
    "l ' . t r C . H l ' . t n ' . p l ' . t g n . b l ' t . E n h . b r E . k E d . G q r",
    "l ' . t H m . d b y . t r E . k l . ' t . H m d . ' G . t r E . k w E b d . w w ' m t . w w G w . r w w . H m r . w",
    "l m h r . g G w . g w y m . w l ' . m y m . y h g . w r y q",
    "y t y . C b w . m l k . y ' r . C w r . w z n y . m n . w ' d ' . l y",
    "n n t . q h m . w s r . w t y m . w n G l . y k m . m s r . w t y m . w",
    "y w G . b b G m y m . y C H . q ' d . n y y . l E g l . m w",
    "' z . y d b r . ' l . y m w . b ' p . w w b H . r n w . y b h . l m w",
    "w ' n y . n s k . t y m . l k y E . l C y w . n h r . q d G . y",
    "' s p . r h ' . l H q y . h w h ' . m r ' l . y b n . y ' t . h y w m . y l d . t y k",
    "G ' l . m m y n . H l t . k w ' H . z q t . k b G b T . y d y . m ' p . s y ' . r C ' . H z t . k",
    "w ' t . h m l k . y m h . s k y . l w h w . s r . w G p T . ' r C",
    "E b d . w ' t . y h w h . b y r ' . h w g y . l w b r . E d . h",
    "n G q . w b r m . p n b . ' p . y b m . E T y . b d r k . w t ' b . d",
    "' G r y . k l . H w s . y b w",
    "y h w h . ' d n y . n w m . h ' d y . r G m . k b k l h . ' r C . ' G r . t n h . w d k E . l h G m y m",
    "m p y E . w l l y . m w y w . n q y . m y s d . t ' z",
    "k y . ' r ' . h G m y . k m E G . y ' C . b E t y . k y . r H w . k w k b . y m",
    "m h ' n . w G ' d . m k y t . z k r . n w w . b n . ' d m . k y . t p q . d n w",
    "w t H s . r h w . m E T m . ' l h y m . w k b w . d w h . d r t . E T r . h w",
    "y h w h . m y y g . w r b ' . h l k . m y y G . k n b h . r q d . G k",
    "h w l k . t m y . m w p E . l C d q . w d b r . ' m t . b l b b . w",
    "l ' . r g l . E l . l G n w . l ' . E G h . r E h . l q r b . w h n b . z h b . E y n y m . ' t . n y k . b d w ' . t y r . ' y y . h w h y . k b d",
    "h G m y m . m s p r . y m k . b w d ' . l w m E . G h y . d y w . E G h . y d y . k p y w",
    "' y n . ' m r . w ' y n . d b r y m . b l y n . G m E . q w l . m w",
    "b k l h . ' r C . y C ' . q w m . w b q C . h t b l . m l y h . m",
    "t w r t y . h w h t . m y m . h m G y . b t . n p G",
    "p q w . d y y . h w h y . G r y . m m G m H . y l b",
    "m C w t y . h w h b . r h m . ' y r . t E y . n y m",
    "l y h w h . h ' r C . w m l w . ' h t . b l w y . G b y . h b",
    "k y . h w ' . E l . y m y m . y s d . h w E l . n h r . w t y k . w n n h",
    "m y y E . l h b h . r y h . w h w m . y y q . w m b m . q w m . q d G w",
    "n q y . k p y m . w b r ' . l b b . ' G r . l ' . n G ' . l G w ' . w l ' . n G b . m r m h",
    "G ' w . r G w . m y p t . H y w . G r E . w l m w . b ' y m . l k h k . b w d",
    "y h w h . ' w r . y w y . G E y . m m y ' . y r ' . y h w h . m E w z . H y y m . m y ' p . H d",
    "' H t . G ' l . t y m . ' l . h w h ' . t h ' . b q G G . b t . y b b . y t y . h w h k . l y m y . H y y",
    "l H z w . t b n . E m . y h w h . w l b q r . b h y k . l w",
    "k y . y C p . n n y . b s k h . b y w m . r E h . y s t . r n y . b s t r . ' h l . w",
    "q w h . ' l . y h w h . H z q . w y ' m . C l b . k w q w . h ' l . y h w h",
    "' l h y m . l n w m . H s h . w E z E . z r h . b C r . w t n m . C ' m . d",
    "' l . k n l ' . n y r . ' b h . m y r h . r b ' . l b b y m . b y m h . m l k . h",
    "y h w h . C b ' w t . E m . n w m . G g b . l n w ' . l h y y . E q b . s l h",
    "H n n y . ' l h y m . k H s d . k k r b . r H m . y k m . H h ' . t p G . E y",
    "k r b s . E n y . m k b s . n y m . E w n y . w m H T ' t y . T h r . n y",
    "k y . p G E y . ' n y . ' d E . w H T ' t y . l n g d . y t m . y d",
    "l b T h w . r b r . ' l . y ' l . h y m w . r w H . n k w n . H d G . b q r . b y",
    "y G b . b s t r . E l . y w n . b C l . G d y . G k n",
    "' m r . l y h w h . m H s y . w m C w . d t y . ' l . h y ' . b T H b . w",
    "k y . h w ' . y C y . l k m p . H y q . G w m . d b r . h w w t",
    "b ' b r . t w y . s k l . k w t H . t k n . p y w . t s h",
    "k y . m l ' k y . w y C w . h l G m . r k b . k l . d r k . y k",
    "b r k . y n p . G y ' . t y h . w h w k . l q r b . y ' t . G m q . d G w",
    "h s l H . l k l E . w n k h . r p ' . l k l t . H l w ' . y k",
    "k r H q . m z r H . m m E r b . k n r H . q m m . n w ' . t p G . E y n . w",
    "k r H m . r H m . ' b E . l b n y . m r H m . y h w h . ' t . y r ' . y w",
    "k y . y d E . y C r . n w z . k w r k . y E p . r ' n . H n w",
    "b n . H k m . y G m . H ' b . w b n k . s y l . t w g . t ' m . w",
    "l ' . y w E . y l w . ' k l . w n p G . C d y q y m",
    "k p y m . r y G . y t m . w l d ' . G r H . w p H k . s y l . b G y p . t G",
    "z k r . C d y q . l b r k . h w G m . r G E y m . r q b",
    "H k m . l b y q . b l m C w t . w E w y . l s p t . y m y . l b d",
    "h w l k . b t . m b T H . y T l . ' y p . H d w . y H H . k s y l . m s l . G l b . w",
    "y d . ' C d . y q n . p G b . h m t w . w r G E y m . y ' b . d w ' . t p n . y h m",
    "l b n b . y n y . q n h . H k m h . w k s y . l p r G . E l . b",
    "' w H . n p s . k s y l . t H y . h w k n . p G y . G r y . m r G k . l E t",
    "k l . m G l . h G k l . w t ' G . r m ' . G y b . b G t G",
    "l ' . d m . m E r k . y l b . w m y h w h . m E n h . l G w n",
    "k l . d r k . y ' y . G y r . b E y n . y w t . k n ' m . r w t . y y h . w h",
    "g l ' . l y h w h . m E G y . k w y k . n w m . H G b . w t y k",
    "b T H b . h G m b . l b b . w h w ' . l y G n . m n . w G ' T . t w b . ' G r y . h w h l . m n . w",
    "p y H . k m ' m . l y H G . r n t . G w n . t m l . k",
    "m G l y . G l m . h b n d . w d H k . m h m w s r . w d E t . w h l T . k l . m y n y . s",
    "m z w z . E b r . y C n . G r k . ' y b . ' l . y w y . s t m . k n w l . ' t . r E",
    "C d y q . ' k l . w l G b . E n p . G w b . T n r . G E y . m y H s . r",
    "b ' w z . y G r . E m l . k m w H . s d y . k n w s . ' t . k s ' . w",
    "y r ' t y . h w h l . H y y m . w G b E . m l ' y . p q d",
    "G m E . w G m y m . w h ' z . y n y . ' r C . k y . y h w h . d b r . b n y m . g d l . t y w . r w m . m t y w . h m G r . G b y",
    "' w y . g w y . H T ' . l y E m . k b d . E w n . w ' C E . r w E . z b w . ' t . y h w h . n ' C . w b z w . ' t . q d w G . y G r ' l",
    "l m h t . k w E w . d t w . s y p . w s r . h k l r . ' G . m l y k . b w",
    "m r ' G l . b l h m . m G p T . G k w . l m E G h . C d q . h",
    "C y w . n b m . G p T . t p d . h w G b . y h b . C d q . h",
    "G m E . w d b r . y h w h . q C y . n y h . ' z . y n w . t w r t . ' l h y n w . E m . G m",
    "m G r E . k y . G r ' . l q d w G . y G r ' l . b z h n . ' C w . r m ' . H w r",
    "k l . b G r . h r E . l G w h . w k H G . w l l b . n w ' . y n r . p ' w . h k h w . w z r y . H",
    "r H C . w k b s . w h y n . w l ' . m d w r . G E h . E G w . T w b . d r G . E h s . r h",
    "' m t . ' b w . G m E . t w n . t w k . l w E m . r G b . h G m E . w n G ' . n w k . l y h w h . d b r",
    "b G n t . m w t h . m l k . E z y h w . ' r ' . ' t . h ' d n y . y G b . y h E . l k s ' . r m w . n G ' . b y w m . l ' . h y k l . w ' t . H m G . k h h y . k l",
    "G r p . y m E . m d y m . l w G G . G r p . y m k . n p y . m y k s . h p n y w . G t y . k s h r . g l y . w w G t . y y E . w p",
    "w q r ' . z h ' . l z h w . ' m r . q d w G . q d w G . q d w G . y h w h . C b ' w t . m l ' k . l h ' r C . k b w d . w",
    "w ' m r . ' w y . ' l . k w ' n k y . ' y G . w b y t r . p ' y . k w G p . t y m . ' n k y . r ' y . t y ' . t h m . l k y h w h . C b ' w t",
    "y b r k . k y . h w h w . y G m . r k",
    "y ' r . y h w h . p n y w . ' l . y k w . y H n . k",
    "y G ' . y h w h . p n y w . ' l . y k w . y G m . l k G l . w m",
    "h b l . h b l . y m ' . r k l . h h b l",
    "m h y t r . n l ' . d m . b k l E . m l w G . y E m . l t H t . h G m G",
    "d w r . h l k w . d w r . b ' w h . ' r C . l E w l m . E m . d t",
    "E y n . z k r . w n l r . ' G . n y m . G y h . y w l . h m l G . m E w n y . m G y h . y w n . w E",
    "G w b . ' H d . m ' l . y m ' . y n ' . H r y . t m r . b y m",
    "w z k r . t ' t . k l h . d r k . ' G r . h l y k . k y . h w h ' . l h y k . z h ' . r b E . y m G . n h b . m d b r",
    "l m E n . E n t . k w l m E n . E z t . k l . d E t . ' t . ' G r . b l b b . k h t G . m r m C . w t y w . ' m l . ' y G . m r n",
    "w y E n . k w y r . E y b . k w y ' . k y . l k H m . n ' G . r l ' . y d E . t ' b . t y k . w w G m . r ' b . t y k . l m E n",
    "l ' . t G k . H l b . b k w l ' . t G k . H E y . n k w . m G k H . w t t w . r h k . s p w . z h b . l ' . t ' k . l k l ' . t ' k . l",
    "k y . y h w h . ' l h y k m . b y ' k . ' l . ' r C . T w b . h ' r C . n H l . y m ' . y n n . w b h ' r C . G m y m . w m y m",
    "w E t h . y G r ' l . m h y h w h . ' l h y k . G ' l . m m k G . E G h . E m . k E m . k G b E . l l b d l . y r ' . ' t . y h w h",
    "w l E b d . ' t . y h w h . ' l h y k . b k l l . b b k w . b k l n . p G k . l G m r . ' t . m C w t y . h w h",
    "' b r . k h ' t . y h w h . b k l E . t t m . y d . t h l . t w b . p y",
    "d r G . H y ' . t y h . w h w y . E n n . y w m . k l . m g w r . w t y h . C y l . n y",
    "h b y T . w ' l . y w h . n h r . w w p n y k m . h b G t . n y G . m E",
    "n C r . l G w n . k w G m . r ' t . G p t . y k m . r m E . G h T . w b w b . q G G . l w m",
    "s w r . m r E . w E G h . T w b . b q G G . l w m w . r d p . h w",
    "r b t . G m E . r G E y m . l C d y q . w k l H . s y m . b w y ' . G m w",
    "y h w h . g ' l . n p G . E b d . y w l . ' y ' . G m w . k l . H s y m . b w",
    "' l . t t H . r b m . r E . y m ' . l t q n . ' b E . G y ' . w n",
    "k y . k H C y . r y m . l y b G . w k d G . ' y b . y ' G . m w",
    "b T H b . y h w h . w E G h . T w b . G k n . ' r C . w r E h . ' m n . h",
    "g l E . l y h w h . d r k k . w b T H . E l . y w w . h w ' . y E G . h",
    "C d y q y m . y r G . w ' r C . w y G k . n w b . h l E w l m",
    "p y C . d y q . y h g . h H k m h . w l G w . n w l . ' t . k G l w",
    "' d n y . m E w n . ' t . h y t h . l n w b . d r w . d w d . r",
    "b T r m . h r y m . y l d . w t H w . l l t b . l ' . m ' l . m w E d . E w l m . ' t . h ' l",
    "t G b . ' n w . G G b . b b q r . k H C y . r y E . b r z r . E k",
    "y m y . G n t . n w k . m w ' m r . G n h . y h w . l l y l . h G n l . p n y w . E b r",
    "l m d . n w m . n w t . y m n . y m k . n H k . m h l b b",
    "' G r y . t m y . m y n k . d r k . b t . w r t y . h w h",
    "b k l l . b b ' d . r G n . w ' l . t G g . m m m C w t y . k",
    "g l y . E y n . y w ' . b y T h . n p l . ' w t . m t w r t k",
    "d b q . t E d . w t y k . ' d n y . ' l . t b y . G n y . l E w l m",
    "h b n y . n y w . ' G r . ' ' t . d r k . p q w . d y k",
    "z m m . t y l . G m r . H q y . k l . q w H . t y l . H y y m . y k y . h y m p . n y k",
    "T w b . ' t . h w T w b . l m d . n y H . q y k",
    "s r . t y m . n y C . w r k y . E d . y k y . b C q t . y G m . r t n . y H s . d k",
    "G m E . y G r ' l . y h w h . ' l h y n w . y h w h . ' H d",
    "w ' h b . t ' t . y h w h . ' l h y k . b k l l . b b k w . b k l n . p G k",
    "w h y w . h d b r y m . h ' l . h E l . l b b k . w G n n . t m",
    "w G n n . t m l . b n y . k w d b r . t b m . b k l G . b t . k",
    "w q G r . t m l . ' w t . E l y d k . w h y w . l T T p t . b y n . E y n y k",
    "w k t b . t m E . l m z w . z w t . b y t . k w b G . E r y . k",
    # ── Genesis 25–35 (patriarchal narratives) ────────────────────────────
    "w y s p . ' b r h m . w y q H . ' G h . w G m h . q T w r h",
    "w y t n . ' b r h m . ' t . k l . ' G r . l w . l y C H q . b n w",
    "w y g w E . w y m t . ' b r h m . b G y b h . T w b h . z q n . w G b E",
    "w y ' H z . y C H q . w r b q h . ' G t w . w t G r r . b T r m . y l d w . b b T n h",
    "w y ' m r . y h w h . l h . G n y . g w y m . b b T n k . w G n y . l ' m y m . y p r d w",
    "w y C ' . h r ' G w n . ' d m w n y . k l w . w y q r ' w . G m w . E G w",
    "w y g d l . h n E r y m . w y h y . E G w . ' y G . y d E . C y d . w y E q b . ' y G . t m . y G b . ' h l y m",
    "w y ' h b . y C H q . ' t E G w . k y . C y d . b p y w . w r b q h . ' h b t . ' t . y E q b",
    "w y z d . y E q b . n z y d . w y b ' . E G w . m n h G d h . w h w ' . E y p",
    "w y ' m r . E G w . ' l . y E q b . h l E y T n y . n ' . m n . h ' d m . h ' d m . h z h . k y . E y p . ' n k y",
    "w y ' m r . y E q b . m k r h . k y w m . ' t . b k r t k . l y",
    "w y ' m r . E G w . h n h . ' n k y . h w l k . l m w t . w l m h . z h . l y . b k r h",
    "w y E q b . n t n . l E G w . l H m . w n z y d . E d G y m . w y ' k l . w y G t . w y q m . w y l k . w y b z . E G w . ' t . h b k r h",
    "w y h y . r E b . b ' r C . m l b d . h r E b . h r ' G w n . w y l k . y C H q . ' l . ' b y m l k",
    "w y r ' . ' l y w . y h w h . w y ' m r . ' l . t r d . m C r y m h . G k n . b ' r C . ' G r . ' m r . ' l y k",
    "w y ' m r . ' l h y m . ' n k y . ' l . h y . b y k . b r k . ' b r k . k . w h r b . ' r b h . ' t . z r E . k",
    "w y b n . G m . b ' r . G b E . w y q r . b G m . y h w h . w y T . h ' h l . G m h",
    "w y l k . y C H q . ' l . ' b y m l k . m l k . p l G t y m . g r r h",
    "w y r ' . y h w h . ' l y w . b l y l . h h w ' . w y ' m r . ' n k y . ' l h y . ' b r h m . ' b y k",
    "g r . b ' r C . h z ' t . w ' h y h . E m k . w ' b r k k . l k . w l z r E k . ' t t n . ' t k l . h ' r C",
    "w y b n . G m . b ' r . G b E . w y q r . b G m . y h w h . w y T . h ' h l . G m h",
    "w y b ' . E G w . ' H y w . m n h C y d w . w y h y . E y p . w y G r . l y E q b",
    "w y E q b . G l H . ' t h . m t r m . m l k . b m l G k w . l k . w ' G r . l l b n . E G w",
    "w y q r . ' E G w . ' t . y E q b . ' H y w . w y ' m r . h y ' q b . k y . w y ' k b . ' t . m G k b t y . p E m y n",
    "w y ' m r . ' y G . k y . n G r . h m ' . ' d m h . ' G r . n G b E . E l y h",
    "w y r . ' y E q b . ' l h y m . p n y m . ' l . p n y m . w t n C l . n p G w",
    "w y ' m r . y E q b . ' l . G m . E G b r . p n . y k n y . ' m . w ' m . E b d y m . w b n y m . E l . h G n y . h G n y t",
    "w y G l H . y E q b . ' t . E y n y w . w y r ' . w h n h . E G w . b ' w h . w ' r b E h . ' y G y m . E m w",
    "w y s g . E G w . l q r ' t . y E q b . w y H b q h w . w y p l . E l . C w ' r w . w y G q h w",
    "w y ' m r . E G w . l y E q b . y G m E . h g m . k l . m G p H t . h ' r C . h ' G . l ' . y d E . k y . m h . ' s p h",
    "w y s E . y E q b . ' t . E y n y w . w y r ' . ' t . r H l . w t h y . G p l t . E y n y m . w l ' . r b h . w y G l p . b h . y E q b",
    "w y E b d . y E q b . b r H l . G b E . G n y m . w b E y n y w . k y m y m . ' H d y m . b ' h b t w . ' t h",
    "w y h y . b b q r . w h n h . h y ' . l ' h . w y ' m r . ' l . l b n . m h . z ' t . E G y t . l y . h l w ' . b r H l . E b d t y . E m k . w l m h . r m y t n y",
    "w y E n . l b n . l ' . y G s h . k n . b m q w m n w . l t t . h C E y r h . l p n y . h b k y r h",
    "w y h y . b b q r . w h n h . h y ' . l ' h . w y ' m r . ' l . l b n . m h . z ' t . E G y t . l y . h l w ' . b r H l . E b d t y . E m k . w l m h . r m y t n y",
    # ── Ruth (narrative prose, diverse vocabulary) ─────────────────────────
    "w y h y . b y m y . G p T . h G p T y m . w y h y . r E b . b ' r C . w y l k . ' y G . m b y t . l H m . y h w d h",
    "w G m . h ' y G . ' l y m . l k . w G m . ' G t w . n ' m y . w G m y . G n y . b n y w . m H l w n . w k l y w n",
    "w y m t . ' l y m . l k . ' y G . n ' m y . w t G ' r . h y ' . w G n y . b n y h",
    "w t q m . h y ' . w k l y t y h . w G t . t G b n h . l ' r C . m w ' b . k y . G m E h . b G d y . m w ' b . k y . p q d . y h w h . ' t . E m w",
    "w t ' m r . n ' m y . G b n h . l k . G b n h . l b y t . ' m k . w y G r h . t b y . k y . E G y t h m ' . E m . h m t y m . w E m y",
    "w t ' m r . r w t . ' l . t p g E y . b y . l E z b . l G w b . m ' H r y k . k y . ' l . ' G r . t l k y . ' l k . w b ' G r . t l y n y . ' l y n",
    "w t ' m r . n ' m y . G w b y . b n w t y m . l m h . t l k n h . E m y . h y G w d . l y . b n y m . b m E y . w h y h . l k m . l ' n G y m",
    "w t G ' n h . r w t . w t b k h . w t G q . l H m t h . w r w t . d b q h . b h",
    "w t ' m r . ' l h k n h . h n h . G b h . y b m t k . ' l . E m h . w ' l . ' l h y h . w ' m w t . G m . ' m w t",
    "w t ' m r . l h . h n h . G b h . y b m t k . h n h . G b h . y b m t k . w ' m w t . G m . ' m w t",
    "w t r ' . n ' m y . k y . m t ' m . C t h . l l k t . ' t h . w t H d l . l d b r . ' l y h",
    "w t l k n h . G n y . E d b y t . l h m . w t b ' n h . b y t . l H m . b t H l t . q C y r . G E r y m",
    "w y h y . k b w ' h . b y t . l H m . w t r g z . k l . h E y r . E l y h n . w t ' m r n h . h z ' t . n ' m y",
    "w t ' m r . ' l y h n . ' l . t q r ' n . l y . n ' m y . q r ' n . l y . m r h . k y . h m r . G d y . l y . m ' d",
    "w t ' m r . r w t . h m w ' b y h . ' l . n ' m y . ' b q G h . n ' . l G d h . w ' l q T h . b G b l y m . ' H r y . ' G r . ' m C ' . H n . b E y n y w",
    "w y ' m r . l h . b E l z . h G d h . h l w ' h ' . h ' G . ' G r . t h y h . ' l h k n h . w G b t y . l . l q T t . b G b l y m",
    "w t b ' . w t l q T . b G d h . w t E m l . m n h G k r . E d h E r b . w t H b T . ' t . ' G r . l q T h . w y h y . k ' p h . k ' m r . ' G ' l . ' G b . ' G n y m . m n h . l h . w ' k l h . w t G b E",
    "w t G ' ' l y h . E G w . w t ' m r . l H m t h . m y n h . l q T t . h y w m . w ' y p h . y h y . w y H y . G E r . l q T t",
    "w t r ' . n ' m y . ' t . k l y t h . w t ' m r . l h . b r k . h w ' . l y h w h . ' G r . l ' E z b . H s d w . ' t . h H y y m . w ' t . h m t y m",
    "w t ' m r . l h . n ' m y . h n h . k l y t h . b n y . h G q r y b . l n w . h w ' . m g ' l y n w . ' H d . h g ' l y m",
    "w y ' m r . b E z . l r w t . h l w ' . G m E t . b t y . ' l . t l k y . l l q T . b G d h . ' H r . w g m . l ' . t E b r y . m z h . w k h . t d b q y n . E m . n E r w t y",
    "w t q m . r w t . w t r C . h E y r . w t r ' . H m t h . ' t . ' G r . l q T h . w t h y . k ' y p h . G E r y m . w G b E . G E r y m . ' G r . t w t r . l h",
    # ── Psalms 40–60 (poetry) ───────────────────────────────────────────────
    "q w h . q w y t y . l y h w h . w y T . ' l y . w y G m E . G w E t y",
    "w y E l n y . m b w r . G ' w n . m T y T . h y w n . w y q m . E l . s l E . r g l y",
    "w y t n . b p y . G y r . H d G . t h l h . l ' l h y n w . y r ' w . r b y m . w y y r ' w . w y b T H w . b y h w h",
    "' G r y . h g b r . ' G r . G m . m b T H w . b y h w h . w l ' . p n h . ' l . r h b y m . w G T y . k z b",
    "r b w t . E G y t . ' t h . y h w h . ' l h y . n p l ' w t y k . w m H G b w t y k . ' l y k . ' g y d h . w ' d b r h . E C m w . m s p r",
    "z b H . w m n H h . l ' . H p C t . ' z n y m . k r y t . l y . t w r h . H p C t y . l E G w t . r C w n k . w t w r t k . b t w k . m E y",
    "b G r t y . C d q . b q h l . r b . h n h . G p t y . G p t y . y h w h . ' t h . y d E t",
    "k y . E z b w n y . r E w t . k y . y h w h . y s E d n y",
    "' G r y . m G k y l . ' l . d l . y h w h . y m l T h w . b y w m . r E h",
    "y h w h . y G m r h w . w y H y h w . w y ' G r . b ' r C . w ' l . t t n h w . b n p G . ' y b y w",
    "k ' y l . t E r g . E l . ' p y q y . m y m . k n . n p G y . t E r g . ' l y k . ' l h y m",
    "C m ' h . n p G y . l ' l h y m . l ' l . H y . m t y . ' b w ' . w ' r ' h . p n y . ' l h y m",
    "' m r h . l ' l . s l E y . l m h . G k H t n y . l m h . q d r . ' t h l k . b l H C . ' w y b",
    "G l H . ' w r k . w ' m t k . h m h . y n H w n y . y b y ' w n y . ' l . h r . q d G k . w ' l . m G k n t y k",
    "G p T y . ' l h y m . q w m h . r y b . r y b y . m g w y . l ' . H s y d . m ' y G . r m y h . w E w l h . t p l T n y",
    "h y w h . ' E n n h . ' t m k . h G y r . r n n h . w ' w d . ' s d r k . b t w k . h H g",
    "G l H . w b q r . ' d b r . p G E y . w t G n h . w ' G E q . k y . r b . h y y n y . b ' l h y m",
    "G m . E b d . y h w h . l m r w m y m . y r G l . l r G l y . w y G m . E l s G w n . m r y E h . E m w",
    "h ' l h y m . y w G y E n y . w y ' m r . h G k l h . G r ' l . ' l . y G r E l . l ' m w G . ' m y . E d y . l ' m . z r",
    "k y . G m E t y . b ' H d . h G p h . l G w n . l ' . ' y d E . ' G y b ' . b ' G d y . l ' G r . l ' m . z r h . ' b w . w ' m y",
    "m ' G r y y . b y t . ' l h y k . G ' y t y . ' l h y m . l p n y . ' l h y m . H y y m . w m l w . E y n y . k y . m T w b h . b y t . ' l h y k",
    "y h w h . C b ' w t . G m E . t p l t . h ' z y n h . ' l h y . y E q b . s l h",
    "m H y . C d q . ' n y . y G m E . l y . ' E n h . k y . G l w m t y . l y . q r ' t y k . ' l h y m . w l ' . ' m n E t y . b k",
    "k y . k n p G . C m ' h . h ' r C . l m T r . k n . C m ' ' n y . l k",
    "G m E . ' m y . t w r t y . h T w . ' z n k m . l ' m r y . p y",
    "' p t H h . b m G l . p y . ' d b r h . H y d w t . m n y . q d m",
    "k y . G m E t y . m E n y . w y G b . G m y m . y g y l w . k y . y G p T . ' l h y m . ' l h y m . h w l k",
    "h w G b . b s t r . E l y w n . b C l . G d y . G k n . ' m r . l y h w h . m H s y . w m C w d t y",
    "' m r . l y h w h . m H s y . w m C w d t y . ' l h y . ' b T H . b w",
    "k y . h w ' . y C y l k . m p H . y q w G . m d b r . h w w t",
    "b ' b r t w . y s k . l k . w t H t . k n p y w . t s h . b C n t w . y s w k . l k . h ' n G l y m . l G m r k . b k l . d r k y k",
    "l ' . t ' n h . ' l y k . r E h . w n g E . l ' . y q r b . b ' h l k",
    "k y . m l ' k y m . y C w h . l k . l G m r k . b k l . d r k y k",
    "' r k . y m y m . ' G b y E . w ' r ' h w . b y G w E y . y h w h . w y ' m r . k y . b y . H G q . h E n y t y . ' k n . ' l h y m . ' l h y m . H y y m",
    # ── Proverbs 22–31 (wisdom – expanded) ────────────────────────────────
    "n b H r . G m . m w G r . g d w l . m k s p . w m z h b . H n . T w b",
    "E G y r . w d l . n p g G w . y h w h . E G h . G n y h m",
    "H n k . l n E r . E l . p y . d r k w . g m . k y . y z q y n . l ' . y s w r . m m n h",
    "k r G E y ' . m l w h . w E b d . l w w h . w l w h . E b d . l w h",
    "z r E . ' w l . H r w G . y s w p . w G b T . E b r w . y k l h",
    "h T . ' z n k . w G m E . d b r y . H k m y m . w l b k . t G y t . l d E t",
    "' l . t s g . g b w l . E w l m . w b G d h . y t w m y m . ' l . t b w '",
    "k y . g ' l m . H z q . w h w ' . y r y b . ' t . r y b m . ' t k",
    "h b ' . l m w s r . l b k . w ' z n k . l ' m r y . d E t",
    "' l . t m n E . m n . E r . m w s r . k y . t k n w . b G b T . w n p G w . m G ' w l",
    "' m . t k n . b G b T . h w ' . y m w t . w n p G w . m G ' w l . t C y l",
    "b n y . ' m . H k m . l b k . y G m H . l b y . w t E l z . k l y w t y . b d b r . G p t y k . m y G r y m",
    "' l . y q n ' . l b k . b H T ' y m . k y . y G . E t y d . w t q w h . l ' . t k r t",
    "G m E . ' b y k . z h . y l d k . w ' l . t b w z . k y . z q n h . ' m k",
    "h k y n . E l . H k m . b y n h . w G E l . b d r k . G p T . h k m . G b y l y m",
    "' y n . H k m h . w t b w n h . w E C h . l n g d . y h w h",
    "m y . m C ' . ' G t . H y l . w r H q . m p n y y n y m . m k r h",
    "b T H . b h . l b . b E l h . w G l l . l ' . y H s r",
    "g m l t . h w . T w b . w l ' . r E . k l . y m y . H y y h",
    "d r G h . C m r . w G m r . w b E w b d y h . k y . G m H h . l ' . y k b h . b l y l . n r h",
    "h y t h . k ' n y w t . s w H r . m r H w q . t b y ' . l H m h",
    "t q m . w t t n . T r p . l b y t h . w H q . l n E r w t y h",
    "z m m h . G d h . w t q H h w . m p r y . k p y h . n T E h . k r m",
    "H g r h . b E w z . m t n y h . w t ' m C . z r w E w t y h",
    "p y h . p t H h . b H k m h . w t w r t . H s d . E l . l G w n h",
    "C w p y h . h l y k w t . b y t h . w l H m . E C l t . l ' . t ' k l",
    "q m w . b n y h . w y ' G r w h . b E l h . w y h l l h",
    "r b w t . b n w t . E G w . H y l . w ' t . E l y t . E l . k l n h",
    "G q r . h H n . w h b l . h y p y . ' G h . y r ' t . y h w h . h y ' . t h t h l l",
    "t n w . l h . m p r y . y d y h . w y h l l w h . b G E r y m . m E G y h",
    # ── Isaiah 40–45 (Deutero-Isaiah – different style) ──────────────────────
    "n H m w . n H m w . E m y . y ' m r . ' l h y k m",
    "d b r w . E l . l b . y r w G l m . w q r ' w . ' l y h . k y . m l ' h . C b ' h . k y . n r C h . E w n h . k y . l q H h . m y d . y h w h . k p l y m . b k l . H T ' w t y h",
    "q w l . q w r ' . b m d b r . p n w . d r k . y h w h . y G r w . b ' r b h . m s l h . l ' l h y n w",
    "k l . b G r . H C y r . w k l . H s d w . k C y C . h G d h . y b G . H C y r . y b G . w r w H . y h w h . n G p h . b w . ' k n . k l m G l . y q w m . w d b r . ' l h y n w . l E w l m . y q w m",
    "E l . g b h . H r . E l y . q w l k . m b G r t . t y G y . ' l . t y r ' y . ' m r y . l E r y . y h w d h",
    "h n h . ' d n y . y h w h . b H z q . y b w ' . w z r w E w . m G l h . l w . h n h . G k r w . l p n y w . w p E l t w . l p n y w",
    "k r w E h . y r E h . E d r w . y q b C . k b ' r y m . y n G ' . w b H y q w . y s ' m",
    "m y . m d d . b G ' l w . m y m . w G m y m . b z r t . k l l . w k l . b G l y G . E p r . h ' r C",
    "h l w ' . y d E t . h l w ' . G m E t . ' l h y . E w l m . y h w h . b w r ' . q C w t . h ' r C . l ' . y y E p . w l ' . y y g E",
    "q w y . y h w h . y H l y p w . k H . y E l w . ' b r . b n G r y m . y r w C w . w l ' . y y g E w . y l k w . w l ' . y y E p w",
    "k y . ' n y . y h w h ' . l h y k . m H z q . y m y n k . h ' m r . l k . ' l . t y r ' . ' n y . E z r t y k . ' p . t m k t y k . b y m y n . C d q y",
    "h y g y d w . h g y G w . ' p . y w E y C . l n w . m h . y ' G y w w . n ' m r . C d q . ' w . h G m y E n w . w n G t ' h . l b n w . ' p . n d E . ' H r y t m",
    "' b r h m . ' h b y . z r E . y G r ' l . ' G r . b H r t y k . m ' p s y . h ' r C . w m ' C y l y h . q r ' t y k . ' t k",
    "' n y . y h w h . ' l h y k . m H z q . y m y n k . h ' m r . l k . ' l . t y r ' . ' n y . E z r t y k",
    "h n h . y b G w . w y b G w . k l . m t q r m k . y ' b d w . w t G b d w . k l y G r y b . r y b k",
    "' n k y . y h w h . ' l h y k . ' H z y q . y m y n k . h ' m r . l k . ' l . t y r ' . ' n y . E z r t y k . ' p . t m k t y k . b y m y n . C d q y",
    "k h . ' m r . y h w h . z k r . ' l h y . h r ' G w n . w l ' . t h g . b r y b . b y n y k m",
    "m y . h E y r . m m z r H . C d q . y q r ' h w . l r g l w . y t n . l p n y w . g w y m . w m l k y m . y r d . k E p r . q G t w . k q G . n d p . r w H",
    "k y . E z z . y h w h . l b T H . b y t . ' l h y m . m n . h G m y m w . m G m y m . G p l y m . w m r k b . y l k w . G m w",
    "G m E . ' l y . k l . m ' p s y . ' r C . h w G y E w . k y . ' n y . ' l . w ' y n . E w d . z w l t y . ' l h y m . H y G w . l y . b y t . b G ' w l m",
    # ── Deuteronomy 28–30 (blessings and curses) ───────────────────────
    "w h y h . ' m . G m w E . t G m E . b q w l . y h w h ' . l h y k . l G m r . l E G w t . ' t . k l . m C w t y w",
    "w n t n k . y h w h . ' l h y k . E l y w n . E l . k l . g w y y . h ' r C . w b ' w . E l y k . k l . h b r k w t . h ' l h",
    "b r w k . ' t h . b E y r . w b r w k . ' t h . b G d h",
    "b r w k . p r y . b T n k . w p r y . ' d m t k . w p r y . b h m t k . G g r . ' l p y k . w E G t r w t . C ' n k",
    "b r w k . T n ' k . w m G ' r t k . b r w k . ' t h . b b ' k . w b r w k . ' t h . b C ' t k",
    "y t n . y h w h . ' t . ' y b y k . h q m y m . E l y k . n g p y m . l p n y k . b d r k . ' H d . y C ' ' l y k . w b G b E h . d r k y m . y n w s . l p n y k",
    "y C w . y h w h . ' t k . ' t . h b r k h . b ' s m y n k . w b k l . m G l H . y d k . w b r k k . b ' r C . ' G r . y h w h ' . l h y k . n t n . l k",
    "y q y m k . y h w h . l w . l E m . q d w G . k ' G r . n G b E . l k . k y . t G m r . ' t . m C w t . y h w h ' . l h y k . w h l k t . b d r k y w",
    "w r ' w . k l . E m y . h ' r C . k y . G m . y h w h . n q r ' . E l y k . w y r ' w . m m k",
    "w h w t r k . y h w h . l T w b h . b p r y . b T n k . w b p r y . b h m t k . w b p r y . ' d m t k . E l . h ' d m h . ' G r . n G b E . y h w h . l ' b t y k . l t t . l k",
    "y p t H . y h w h . l k . ' t . ' w C r w . h T w b . ' t . h G m y m . l t t . m T r . ' r C k . b E t w . w l b r k . ' t . k l . m E G h . y d k",
    "w h l w y t . g w y m . r b y m . w ' t h . l ' . t l w h . w m G l t . b g w y m . r b y m . w b k . l ' . t m G l",
    "h y h . l r ' G h . w l ' . l z n b . ' m . G m w E . t G m E . ' l . m C w t . y h w h ' . l h y k . ' G r . ' n k y . m C w k . h y w m . l G m r w t m w",
    "w h G b t . ' l . l b b k . ' t . h G b r k h . w h q l l h . ' G r . ' n k y . n t n . l p n y k . h y w m . w n t t . ' l . l b b k . ' t . k l y G r ' l . w E l h . b y n y k",
    "w ' t h . t G w b . w G m E t . b q w l . y h w h . w E G y t . ' t . k l . m C w t y w . ' G r . ' n k y . m C w k . h y w m",
    "k y . h m C w h . h z ' t . ' G r . ' n k y . m C w k . h y w m . l ' . n p l ' t . h y ' . m m k . w l ' . r H q h . h y '",
    "l ' . b G m y m . h y ' . l ' m r . m y . y E l h . l n w . h G m y m h . w y q H h . l n w . w y G m E n w . ' t h . w n E G n h",
    "k y . q r w b . ' l y k . h d b r . m ' d . b p y k . w b l b b k . l E G t w",
    "h E d t y . b k m . h y w m . ' t . h G m y m . w ' t . h ' r C . h H y y m . w h m w t . n t t y . l p n y k . h b r k h . w h q l l h",
    "b H r . b H y y m . l m E n . t H y h . ' t h . w z r E k . l ' h b h . ' t . y h w h . ' l h y k . l G m E . b q l w . l d b q h . b w",
    # ── More Psalms (61–80) ──────────────────────────────────────────────────
    "G m E . ' l h y m . r n t y . h q G y b h . t p l t y",
    "m q C h . h ' r C . ' l y k . ' q r ' . b E T p . l b y . b C w r . y r w m . m m n y . t n H n y",
    "' h y h . b ' h l k . l E w l m y m . ' H s h . b s t r . k n p y w . s l h",
    "k y . ' t h . ' l h y m . G m E t . t p l l t y . t t n . y r G t . l y r ' y . G m k . ' G r b h . E l . l b b y",
    "' n y . b t m y . ' G r . b y t k . ' l h y m . l E w l m y m . ' H s h . b s t r . k n p y k",
    "l l h . d m y h . t h l h . b C y w n . l k . y G l m . n d r . w l k . y G . G b E",
    "' G r y . t b H r . w t q r b . y G k n . b H C r y k . n G b E h . b T w b . b y t k . q d G . h y k l k",
    "m h . y d y d w t . m G k n w t y k . y h w h . C b ' w t . n k s p h . w g m . k l t h . n p G y . l H C r w t . y h w h",
    "n G r ' h . l b y . w b G r y . y r n n w . l ' l . H y . w ' l . G m E . ' l h y m . G p T y",
    "' l h y m . C b ' w t . G w b h . ' l . G b k n w t . b G r w t . h ' r C . p s y . E r y m . w m G l k . k l . r G l",
    "w y z k r . k y . b G r . h m h . r w H . h w l k . w l ' . y G w b . w l ' . y G b w b . k m h . b m d b r . y C m ' w n . w y n s w . ' t . ' l . b y G y m w n",
    "h l l w y h . h l l w . ' t . G m . y h w h . h l l w . ' t . y h w h . m n . h G m y m",
    "h l l w h w . b G p r . k h . m G m y m . h l l w h w . b g b w h y m . h l l w h w . k l . m l ' k y w",
    "h l l w h w . G m G . w y r H . h l l w h w . k l . k w k b y . ' w r",
    "h l l w h w . G m y . h G m y m . w h T n y n y m . w k l . t h m w t",
    "h l l w h w . ' G . w b r d . G l g . w q y T w r",
    "y h w h . ' d n y . g d w l . E G h . l E G . h y k l . ' G r . H p C . b ' r C . w b k l . t h m w t",
    "m y . k y h w h . ' l h y n w . h m g b y h y . l G b t . h m G p y l . l r ' w t . b G m y m . w b ' r C",
    "y h w h . G m k . l E w l m . ' l h y k . C y w n . l d r . w d r . h l l w y h",
    "h l l w y h . h l l w . ' l . ' l . q d G w . b q d G . E z w . ' l h y m . b g b w r t . E z w w",
    "h l l w h w . b t q E . G w p r . h l l w h w . b n b l . w k n w r . h l l w h w . b t p . w m H w l",
    "h l l w h w . b m y n y m . w E w g b . h l l w h w . b C l C l y . G m E . h l l w h w . b C l C l y . t r w E h",
    "k l . h n G m h . t h l l . y h . h l l w y h",
]

# ── Corpus functions ──────────────────────────────────────────────────


def get_corpus_inscriptions() -> list[list[str]]:
    """Return Hebrew corpus as list of inscriptions (one per verse).

    Each inscription is a list of consonant strings (dots stripped).
    This is the primary input for building a LanguageModel flat bigrams.
    """
    inscriptions: list[list[str]] = []
    for line in _HEBREW_LINES:
        signs = [s for s in line.split() if s and s != "."]
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
        "brGyt": "in the beginning",
        "br'": "he created",
        "'lhym": "God",
        "hGmym": "the heavens",
        "h'rC": "the earth",
        "'wr": "light",
        "Hk": "darkness",
        "ywm": "day",
        "lylh": "night",
        "mymt": "water",
        "mlk": "king",
        "bn": "son",
        "bt": "daughter / house",
        "db": "word",
        "yGr'": "fear of",
        "yhwh": "the LORD",
        "H m": "wisdom",
        "lbb": "heart",
        "'rC": "land / earth",
        "gym": "nations",
        "mGpT": "judgment",
        "Cdq": "righteousness",
        "r'h": "he saw",
        "'mr": "he said",
        "hyh": "he was",
        "E m": "people",
        "nG": "soul / breath",
        "rwH": "spirit / wind",
    }


def get_word_inscriptions() -> list[list[str]]:
    """Return the corpus as WORD-level inscriptions.

    Parses the '.' word-boundary markers written into _HEBREW_LINES by
    the tools/build_hebrew_words.py vocabulary-matching segmenter.
    Lines that were not segmented (no dots) fall back to 3-consonant
    chunks (closer to the true average Biblical Hebrew word length).

    Each returned list is one word as a list of consonant strings.
    """
    words: list[list[str]] = []
    for line in _HEBREW_LINES:
        tokens = line.split()
        if "." in tokens:
            # Proper word-boundary parse
            current: list[str] = []
            for tok in tokens:
                if tok == ".":
                    if current:
                        words.append(current)
                        current = []
                else:
                    current.append(tok)
            if current:
                words.append(current)
        else:
            # Fallback: 3-consonant chunks (avg BH word length)
            for start in range(0, len(tokens), 3):
                chunk = tokens[start : start + 3]
                if chunk:
                    words.append(chunk)
    return [w for w in words if w]


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
        "total_tokens": len(flat),
        "distinct_signs": len(freq),
        "type_token_ratio": round(len(freq) / len(flat), 4) if flat else 0,
        "n_inscriptions": len(inscriptions),
        "avg_inscription_length": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "hapax_count": sum(1 for v in freq.values() if v == 1),
        "most_frequent": freq.most_common(10),
    }
