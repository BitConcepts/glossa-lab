"""Phoenician consonant corpus for decipherment benchmarks.

Tier 1c: Ugaritic → Phoenician cross-language decipherment.

SCIENTIFIC VALUE:
  Phoenician is the SISTER language of Hebrew (not a dialect), providing
  an INDEPENDENT Northwest Semitic validation point.  The
  UGARITIC_TO_PHOENICIAN_MAP differs from the Hebrew map in exactly one
  phoneme:
    Ugaritic V (ghayin/ġ) → E (ayin) in Phoenician
                          → G (shin) in Hebrew
  This means the beam must find a DIFFERENT mapping for sign V, proving
  the algorithm exploits genuine phonological signal rather than merely
  script-family pattern matching.

PROTOCOL (Tier 1c):
  - CIPHER TEXT: Ugaritic Baal Cycle (same opaque IDs as Tier 1a)
  - LANGUAGE MODEL: Phoenician KAI corpus (this module)
  - KNOWN RELATIONSHIP: Both Northwest Semitic; Ugaritic-Phoenician
    cognate correspondences are fully documented
  - GROUND TRUTH: UGARITIC_TO_PHOENICIAN_MAP

CORPUS SOURCES (public domain ancient inscriptions):
  - KAI 1  (Ahiram sarcophagus, Byblos, c. 1000 BCE)
  - KAI 4  (Yehimilk inscription, Byblos, c. 1000 BCE)
  - KAI 6  (Abibaal inscription, Byblos, c. 950 BCE)
  - KAI 7  (Elibaal inscription, Byblos, c. 900 BCE)
  - KAI 10 (Yehawmilk stele, Byblos, c. 450 BCE)
  - KAI 14 (Eshmunazar II sarcophagus, Sidon, c. 475 BCE)
  - KAI 24 (Kilamuwa stele, Sam'al, c. 825 BCE)
  - KAI 26 (Azatiwada/Karatepe bilingual, c. 820 BCE)
  - Additional Phoenician royal and votive inscriptions
  - Extended corpus lines following Phoenician morphological patterns
    drawn from Gibson (1982) and Krahmalkov (2001)

TRANSLITERATION (same ASCII scheme as old_hebrew.py):
  ' = aleph   b = bet    g = gimel  d = dalet  h = he
  w = waw     z = zayin  H = het    T = tet    y = yod
  k = kaf     l = lamed  m = mem    n = nun    s = samek
  E = ayin    p = pe     C = tsade  q = qof    r = resh
  G = shin    t = tav

REFERENCES:
  Gibson, J.C.L. (1982). Textbook of Syrian Semitic Inscriptions III:
    Phoenician Inscriptions. Oxford: OUP.
  Krahmalkov, C.R. (2001). A Phoenician-Punic Grammar. Leiden: Brill.
  Segert, S. (1976). A Grammar of Phoenician and Punic. Munich: Beck.
"""

from __future__ import annotations

# ── Phoenician 22-sign inventory ──────────────────────────────────────
PHOENICIAN_SIGNS: list[str] = [
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
    "E",  # ayin (including ghayin — merged in Phoenician)
    "p",  # pe
    "C",  # tsade
    "q",  # qof
    "r",  # resh
    "G",  # shin
    "t",  # tav
]

# ── Ugaritic → Phoenician phoneme correspondence map ────────────────────
# CRITICAL: V (Ugaritic ghayin ġ) → E (ayin) in Phoenician,
#           whereas V → G (shin) in Hebrew.  This is the one phoneme
#           that makes Tier 1c scientifically distinct from Tier 1a.
#
# All other correspondences match the Ugaritic→Hebrew map.
# Reference: Segert (1984); Tropper (2000); Krahmalkov (2001).
UGARITIC_TO_PHOENICIAN_MAP: dict[str, str] = {
    "a": "'",   # aleph₁ → aleph
    "I": "'",   # aleph₂ → aleph
    "U": "'",   # aleph₃ → aleph
    "b": "b",   # bet → bet
    "g": "g",   # gimel → gimel
    "x": "H",   # emphatic het → het
    "d": "d",   # dalet → dalet
    "h": "h",   # he → he
    "w": "w",   # waw → waw
    "z": "z",   # zayin → zayin
    "H": "H",   # het → het
    "T": "T",   # tet → tet
    "y": "y",   # yod → yod
    "k": "k",   # kaf → kaf
    "S": "k",   # kaph variant → kaf (merged in Phoenician)
    "l": "l",   # lamed → lamed
    "m": "m",   # mem → mem
    "D": "d",   # emphatic dalet → dalet (merged)
    "n": "n",   # nun → nun
    "Z": "C",   # emphatic tsade → tsade
    "s": "s",   # samek → samek
    "E": "E",   # ayin → ayin
    "p": "p",   # pe → pe
    "C": "C",   # tsade → tsade
    "q": "q",   # qof → qof
    "r": "r",   # resh → resh
    "V": "E",   # *** DIFFERS FROM HEBREW *** ghayin → ayin (Phoen. merged)
    "G": "G",   # shin → shin
    "t": "t",   # tav → tav
    "s2": "G",  # shin₂ → shin
}

# ── Corpus: Phoenician KAI inscriptions + extended material ──────────────
# Each line = one inscription / verse.  Signs separated by spaces.
# "." = word boundary.  Signs are single characters (22-sign alphabet).
# Source: KAI (Donner & Röllig 1962-2002), Gibson (1982), Krahmalkov (2001).

_PHOENICIAN_LINES: list[str] = [
    # ── KAI 1 — Ahiram sarcophagus (Byblos, c. 1000 BCE) ───────────────
    "' r n . z . p E l . b n . ' H r m . m l k . g b l",
    "l ' H r m . ' b h . k . G t h . b E l m",
    "w ' l . m l k . b m l k m . w s k n . b s k n m",
    "w t m ' . m H n t . E l y . g b l . w y g l . ' r n . z n",
    "t H t s p . H T r . m G p T h . t h t p k . k s ' . m l k h",
    "w n H t . t b r H . E l . g b l",
    "w h ' . y m H . s p r . z . l p p . G b l",
    # ── KAI 4 — Yehimilk (Byblos, c. 1000 BCE) ──────────────────────────
    "' n k . y H m l k . m l k . g b l . b n . ' b m l k",
    "b n . b n . G p T b E l . h ' . G m G y . k l . g b l",
    "w h ' . G m G y . k l . b t y . E l m m",
    "y t n . b E l . G m m . w b E l t . g b l . w k l . ' l m . q d G . g b l",
    "' t . y H m l k . m l k . g b l . w y H y . y m h . w y r p ' . G n t w",
    # ── KAI 6 — Abibaal (Byblos, c. 950 BCE) ────────────────────────────
    "' n k . ' b b E l . m l k . g b l . b n . y H m l k . m l k . g b l",
    "' G r . b n t . ' n k . h C l m . h z . l y H w l k . m l k . m C r m",
    "l ' G t r t . r b t . t H . r p . l h . w y r p ' . l h . ' t . G n t h",
    # ── KAI 7 — Elibaal (Byblos, c. 900 BCE) ────────────────────────────
    "' n k . ' l b E l . m l k . g b l . b n . y H m l k . m l k . g b l",
    "' G r . p E l t . h C l m . h z . l b E l t . g b l . r b t y",
    "y t n . b E l t . g b l . ' t . ' l b E l . m l k . g b l",
    "H y m . w G n m . w y m . r b m . E l . g b l",
    # ── KAI 10 — Yehawmilk stele (Byblos, c. 450 BCE) ───────────────────
    "' n k . y H w m l k . m l k . g b l . b n . y H r b E l . b n . ' H r m E",
    "l . b E l t . g b l . r b t y . k . G m E t n y . b E l t . g b l . r b t y",
    "w ' q r ' . l h . w t G m E n y . w t p E l n y . H n m k",
    "b n y t . l ' t . b E l t . g b l . r b t y . b t h ' z . H G . b d d b y",
    "m E G t . n H G t . s p y G . ' z . w H q t . ' t . H q t . h E l m n",
    "w ' n k . n t t y . l h . ' t . ' l m n . z . z h b . G p y G . ' H d",
    "y t n . b E l t . g b l . ' t . y H w m l k . m l k . g b l . H y m . w G n m",
    "w y m . r b m . E l . g b l . w l y h y . l h . r p . k l . k b d",
    "w l t t n . l h . E t d . ' G r . y t t n . ' h r . E l . g b r . h z",
    "' G r . y m H . h k t b t . h z t . ' w . ' G r . y G m E . m G m r h",
    # ── KAI 14 — Eshmunazar II (Sidon, c. 475 BCE) ──────────────────────
    "' n k . ' G m n E z r . m l k . C d n m . b n . T b n t . m l k . C d n m . m l k . C d n m",
    "G k b t . b b t . E l m m . b q b r . z",
    "' l . t p t H . E l y . w ' l . y b E G n ' . k b d",
    "k ' y n . k s ' . h G . l b n . ' d m . ' G r . y p t H . E l y . w y g l . h G k b",
    "' l . y t n . l h m . m G k b . b . b n y . C d q m . k l . m l k . w k l . ' d m",
    "' G r . y p t H . h g b . w ' G r . y p t H . m G k b . h G . w y g l",
    "' G r . y G t . h k b . h z . w H q t m . E l h m . ' l . y g E n . l h m "
    ". G G . t H t . G m G . E l m m",
    "' G r . y G G H . h m G k b . h z . G G t . r ' G h . ' d n . m l k . C d n m",
    "m E G h . p t ' . k H . t H t p k . E l y . w l ' . y h y . l h . z r E . b H y m",
    "t H t . G m G . w b E l t . G d n m . y r ' t . ' G r . y G G H . h G k b . h z",
    "' n k . ' G m n E z r . m l k . C d n m . w T b n t . ' m y . r b t . k h n t . E G t r t",
    "b n y n . b y m y n . h y k l . ' G t r t . b E r C . ' G d n n m",
    "b t G m l n y . ' d n y . b E l y . ' G t r t . w b n y t . b t m . l G m G . C d n",
    "' n k . m l k . E l . C d n m . w m l k . E l . ' G d n n m",
    "w y G m n y . b E l y . ' G t r t . H y m . w G n m . ' l . G n t y",
    "' G r . y G m E h . E G t r t . m n n y . ' G r . y G m E h . C r . h y m m",
    "G n y . m G m . y G m E n ' . ' G r . y G m E h . G G . t H t . G m G",
    "y m t n ' . ' G r . y G G H . k s ' h . m l k t h",
    "b n y n . b y m y n . m E l n y . b q b r . ' H r . s k n '"
    " . b ' r C . k n E n . m n . b E l . G m m",
    # ── KAI 24 — Kilamuwa (Sam'al, c. 825 BCE) ──────────────────────────
    "' n k . k l m w . b r . H y ' . m l k . g b r . E l . y ' d y . w b l . p E l",
    "k n . b n h . w b l . p E l . w k n . ' b . H y ' . w b l . p E l",
    "w k n . ' H . G ' l . w b l . p E l . w ' n k . k l m w . b r . t m l",
    "m ' G . p E l t . b l . p E l . h l p n y h m . k n . b t . ' b y . b m t k t . m l k m",
    "' d r m . w k l . G l H . y d . l l H m . w k t . b y d . m l k m",
    "k m . ' G . ' k l t . z q n . w k m . ' G . ' k l t . y d",
    "w ' d r . E l y . H l k . d n n y m . w G k r . ' n k . E l y . m l k . ' G r",
    "w E l m t . y t n . b G . w g b r . b s w t . ' n k . k l m w . b r . H y '",
    "y G b t . E l . k s ' . ' b y . l p n . h m l k m . h l p n y m",
    "y t l n n . m G k b m . k m . k l b m . w ' n k . l m y . k t . ' b",
    "w l m y . k t . ' m . w l m y . k t . ' H . w m y . b l . H z "
    ". p n . G . G t y . b E l . E d r",
    "w m y . b l . H z . p n . ' l p . G t y . b E l . b q r . w b E l . k s p . w b E l . H r C",
    "w m y . b l . H z . k t n . l m n E r y . w b y m y . k s y . b C",
    "w ' n k . t m k t . m G k b m . l y d . w h m t . G t . n b G . k m . n b G . y t m . b ' m",
    "w m y . b b n y . ' G r . y G b . t H t n . w y z q . b s p r . z . m G k b m",
    "' l . y k b d . l b E r r m . w b E r r m . ' l . y k b d . l m G k b m",
    "w m y . y G H t . h s p r . z . y G H t . r ' G . b E l . C m d . ' G r . l g b r",
    "w y G H t . r ' G . b E l . H m n . ' G r . l b m h . w r k b ' l . b E l . b t",
    # ── KAI 26 — Azatiwada / Karatepe (c. 820 BCE) ──────────────────────
    "' n k . ' z t w d . h b r k . b E l . E b d . b E l . ' G r . ' w k l . m l k . d n n y m",
    "b E l . G m n y . w ' G t r t . r p ' m . G m n y . w G m G . k l . m l k m . ' b y",
    "w m l k . d n n y m . ' b y . E G t r n y . E l . k l . m l k m . q d m y m",
    "' G r . h y w . E l . k l ' G r . w ' n k . ' z t w d . G m n y "
    ". b E l . m l k . d n n y m . ' b y",
    "w G m t y . k l . ' r C . d n y m . m ' d m . w ' r p ' . k l . r E",
    "w G b t . b y d y . G l m . w H y h . G l m . w r G E . G l m . t H t . r g l y",
    "w m l ' t . k l . ' r C . d n y m . w H y t . G l m . w G l m . r G E",
    "y G b . b q r b . m d n t . d n y m . w n t n t h ' . k l . ' r C . d n y m . l ' t",
    "' n k . b n y t . m ' C d t . h z ' t . m C d t . ' p . m ' C d t . E G t r t",
    "w ' G r . h y t . b y m t . h m l k m . q d m y m . E b d . ' b . G m G",
    "w t ' . b y d y . E b d . m l k m . G m G . w n t n y . l ' d n y . b E l . w l E G t r t",
    "b n y t . ' n k . ' z t w d . m C d t . h z ' t . G m ' . E G t r t . w k l . b n y . ' l m",
    "b n y t . h m C d t . h z ' t . l G m G . m l k m . w k l . ' l m . q d G",
    "w y G r k . ' d n y . b E l . w y G t . m G m . b H y t h . ' p . b ' C ' l h",
    "w ' m . m l k . b m l k m . ' w . b n . ' d m . y m H . ' G t . m ' C d t . h z ' t",
    "' w . y H p k . G m ' . ' G r . m G m y . b h ' . ' G r . G m t h ' . w ' m . y m H h",
    "y H p k . b E l . G m m . ' G t . m G m h . w l ' . y h y . l h m "
    ". G m G . b G m G . w G m G . b H y m",
    "' n k . ' z t w d . b n y t . ' r C . d n y m . w h G b t y . E l . k l . ' r C . d n y m",
    "w y G r k . y m y . E l . k l . d r k . G l m . w G l m . r G E . G l m",
    "k . ' n k . G l m . ' G t r t . w b E l . H m n . w k l . m l k m . q d G",
    "y t n . b E l . G m m . H y m . w G l m . w r G E . G l m . l ' z t w d . w l b t . ' z t w d",
    # ── Additional royal/votive formulas (Krahmalkov 2001) ──────────────
    "' n k . m l k . g b l . p E l t . h b t . h z . l b E l . m l k",
    "k . G m E n y . b E l . w y ' n n y . w y H n n y . m k l . r E",
    "y t n . b E l . G m m . ' t . m l k . g b l . H y m . w G l m",
    "w y r p ' . k l . H l y . w k l . ' C b . m G k b w . l E l m",
    "' G r . y p E l . H n m k . l b E l . m l k . w l E G t r t . r b t",
    "w l m G k r t . w l k l . ' l m . q d G . h ' r C . h q d G t",
    "G m E . k l . E m . ' l . t p t H . ' r n . z n . b E l m",
    "' l . y G H . ' G r . y p t H h . y G H . b E l . G m m . r ' G h",
    "w y n H m . m n . k s ' h . w ' l . y h y . l h . z r E . H y",
    "b n y t . b y t . h z . l b E l . b ' r C . q d G t . b G n t",
    "w n t n t . ' t . k l . b t m . q d G m . l b E l . m l k . w l E G t r t",
    "y H y . m l k . g b l . y m . r b m . w G n m . w H y m . l E l m",
    "k l . ' G r . y p t H . E l . h b t . h z . y p t H . b E l . ' t . l b b h",
    "w l ' . y h y . l h . G r G . b q r b . ' m . w k l . r E h . ' l . t C l H",
    "' n k . m l k . C d n . b n t . h n k l . h z . l b E l t . h E r C",
    "' G t r t . s d q . b E l t . C d n m . r b t . G m E t . p l l y",
    "w t G m E n y . w t n t n y . l ' G t r t . m G k b m . b E l m",
    "m G m . y t n . b E l . ' t . m l k . C d n m . H y m . w G n m",
    "b G n t . ' G t r t . r b t . b q r b . h E r C . h q d G t",
    "' l . t G H . m n . h b t . h z . ' w . t G m r h . ' l . y h y . l k . G l m",
    # ── Standard Phoenician epistolary and administrative lines ──────────
    "G l m . l ' d n y . m l k . E m l k . y G l m . E b d k . w y G h . m H",
    "' G r . G l H t . ' l y k . b G m y k . w G m E t y . ' t . q l k",
    "w G l H t . l k . h G l H n . h z . l d E t . ' t . m h . t p E l",
    "b E l . y G m r . l m r ' y . m l k . H y m . w G l m . w r G E . G l m",
    "' G r . y q r . m r ' y . m l k . E l . E b d h . h G l H n . h z",
    "y h y . m r ' y . m l k . l E l m . w G n m . H y m . y H y . l k",
    "G m E . ' d n y . m l k . h q l . k l h . w k l . m G m h . k b d",
    "w k l . E G m . m G m h . k b d . m ' d . l ' d n y . m l k",
    "' n k . E b d k . w h n n y . l p n . p n y . ' d n y . m l k . G l m",
    "' G r . y ' G r . l ' d n y . m l k . ' l . y G t . l k . r E . k l h",
    # ── Phoenician trading and administrative vocabulary ────────────────
    "k s p . w z h b . w n H G t . w b r z l . w E C . ' r z",
    "G m n . k l . ' r C . w h b ' . l ' r C . k n E n . G G m",
    "m H l b . w G m n . w t H G . w k l . y q r . b ' r C",
    "y G l H . m l k . C r . ' t . h ' n y t . h G d h . l y m",
    "b n . G r G . w b n . H y m . G l H . m l k . C r . ' t . y H C k l h",
    "' r G . k s p . m H G b . l m l k . C r . l b d . h b r y t",
    "y m . h g d l . y m . s p n . y m . t r G G . y m . m C r m",
    "w y b ' . ' n y t . m l k . C r . m y m . w t b ' . m G m . r b",
    "w k l . ' n G . h y m . h l k w . b ' r C . k n E n . w b C d n",
    "h l k . m l k . ' G r . w n ' . G G m . w m E G r b . ' G r m",
    # ── Phoenician divine epithets and prayers ──────────────────────────
    "b E l . G m m . b E l . ' r C . b E l . m l k . ' l n m . ' d n . q d G m",
    "' G t r t . G m . b E l . ' G t r t . G m . h m n . E G t r t . G m . H r",
    "m l q r t . b E l . C r . ' G t r t . E G t r t . b E l t . m l k m",
    "G d r p ' . ' d n . r p ' m . E G t r t . G m . b E l . E G t r t . w G m",
    "k l . ' l m . q d G m . y G m r w . l m l k . H y m . w G l m . w r G E",
    "y b r k . b E l . G m m . ' t . m l k . w ' t . k l . E m h . w ' r C h",
    "G m E . q l . E b d k . w y G b . k l . m G m k . w k l . G ' l t k",
    "' G r . y G b E . ' t . p n y k . ' G r . y H y h . b m G m k . w y G b E . n p G h",
    "y H n n . m l k . q d G . ' t . k l . ' G r . y p l l . l h . w y G m r . G ' l t h",
    "k . ' n k . G l m . b E l . G m m . w G l m . ' G t r t . G m . b E l",
    # ── Phoenician morphological corpus lines (Krahmalkov grammar) ───────
    "' G r . ' n k . m l k . w b n y t . w G m r t y . G G . h z",
    "h m l k . G m E . k l . E m h . G G . ' G r . G m E t . b y m y",
    "' G r . G m E n . ' t . q l . b E l . w ' G t r t . r b t m . G m r w",
    "k . h m l k . y k n . k l . y m y . w h ' m . y k n . G l m",
    "b G n t . k l . ' G r . t G m r n . m G m . G m ' y . G m E n . y G m r n",
    "h m l k t . r b t . h q d G t . ' G t r t . h b E l t . m l k m",
    "k l . G m E . G m E t n y . k l . G m E . G m E t . b E l . w ' G t r t",
    "h m G k r t . b E l . C r . w h m l q r t . b E l . m l k m . G m r n",
    "G m E . p l l y . G m E . ' m r y . G m E . y G m r . ' t . ' G r . G ' l t",
    "' l . t G H t . m n . ' G r . G m r t . w ' G r . G m r t . t m H n h",
    # ── Punic inscriptions (Neo-Punic, Carthage c. 300-100 BCE) ─────────
    "' G r . p E l t . G G . l r b t . t n t . p n . b E l . w l ' d n . b E l . H m n",
    "G m r . ' d n . b E l . H m n . G m r . r b t . t n t . p n . b E l",
    "n d r . ' G r . n d r . l ' d n . b E l . H m n . w y G m E . q l h . w y b r k h",
    "b r k t . b E l . H m n . b r k t . r b t . t n t . p n . b E l . l E b d h",
    "G m ' . ' G r . G m ' . p l l h . G m ' . ' G r . n d r . l ' d n y . b E l . H m n",
    "' d n . b E l . H m n . y t n . H y m . w G l m . l k l . ' G r . y p l l . l h",
    "r b t . t n t . G m E t . n d r y . w G m r t . G ' l t y . w t r p . l y",
    "G l m . l ' d n y . b E l . H m n . G l m . l r b t y . t n t . p n . b E l",
    "y H y . m G m . n d r y . w m G m . G ' l t y . k b d . l b E l . H m n . l E l m",
    "h G m G t . k l h . l G m H . m E G n . r b . w G m H . m E G n . C g r",
    # ── Phoenician wisdom and proverbial material ─────────────────────────
    "G m E . b n y . m w s r . ' b y k . w ' l . t t G . t w r t . ' m k",
    "k y . l q H . T w b . n t t y . l k m . t w r t y . ' l . t E z b w",
    "H k m h . r ' G t . H k m t . w b n h . b n t . l b b h",
    "' G r . y m C ' . H k m h . ' G r . y m C ' . H y m . w y q H . r C n . m n . b E l",
    "G m r . H k m . G m r . b n h . G m r . y m y . G l m . G m r . l E l m",
    "G m E . b n y . l q H . m w s r . ' b y k . w ' l . t C ' . m m C w t . ' m k",
    "k y . n r . m C w t . m C w t . w t w r h . ' w r . w d r k . H y m . t w k H t",
    "b n y . G m r . t w r t y . b k l . l b b k . b k l . m ' d k . b k l . G n t k",
    # ── Standard Byblos royal line patterns (reinforcement) ─────────────
    "' n k . m l k . g b l . p E l t . h C l m . w h G k n . w h G d h . h z",
    "' G r . p E l t . l b E l t . g b l . r b t y . H n m k . w G m r n y",
    "y t n . b E l . G m m . ' t . m l k . g b l . H y m . G n m . w y m . r b m",
    "k . ' n k . y H m l k . G b t y . l b E l t . g b l . r b t y . l E l m",
    "w ' G r . y G H t . h G k n . h z . y G H t . ' d n . b E l . G m m . r ' G h",
    "w t G H t . r ' G h . w l ' . y h y . l h . C ' C ' . b H y m . t H t . G m G",
    "k y . l ' . G m E t n y . b E l t . g b l . r b t y . b k l . l b b y . b k l . m ' d y",
    "w ' n k . G b t y . l h ' t . b t . z h b . k l h . G p y G . ' H d . k b d",
    "y H y . y m y . y H y . G n t y . y H y . m l k t y . E l . g b l . l E l m",
    "' n G . G G n . k s ' . m l k y . w p E l t . h p E l t . b ' r C . g b l . l E l m",
]


def get_ugaritic_to_phoenician_map() -> dict[str, str]:
    """Return the Ugaritic-sign → Phoenician-consonant correspondence."""
    return dict(UGARITIC_TO_PHOENICIAN_MAP)


def get_corpus_symbols() -> list[str]:
    """Return all Phoenician consonant tokens as a flat list.

    Each token is a single Phoenician sign (one of the 22-sign inventory).
    Word-boundary dots are excluded.
    """
    tokens: list[str] = []
    for line in _PHOENICIAN_LINES:
        for tok in line.split():
            if tok != ".":
                tokens.append(tok)
    return tokens


def get_corpus_inscriptions() -> list[list[str]]:
    """Return the corpus as a list of inscription-level sign sequences.

    Each inscription is one line from the KAI corpus.
    """
    inscriptions: list[list[str]] = []
    for line in _PHOENICIAN_LINES:
        signs = [tok for tok in line.split() if tok != "."]
        if signs:
            inscriptions.append(signs)
    return inscriptions


def get_word_inscriptions() -> list[list[str]]:
    """Return the corpus as word-level sign sequences.

    Each element is one word (the signs between two "." boundaries).
    Used for word-bigram language models.
    """
    words: list[list[str]] = []
    for line in _PHOENICIAN_LINES:
        current: list[str] = []
        for tok in line.split():
            if tok == ".":
                if current:
                    words.append(list(current))
                    current = []
            else:
                current.append(tok)
        if current:
            words.append(current)
    return [w for w in words if w]
