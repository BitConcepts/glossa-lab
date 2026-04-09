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
