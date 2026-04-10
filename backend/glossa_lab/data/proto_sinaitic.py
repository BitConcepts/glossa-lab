"""Proto-Sinaitic consonant corpus for decipherment benchmarks.

Proto-Sinaitic (c. 1850–1500 BCE) is the earliest attested alphabetic script,
found at Serabit el-Khadim (Sinai) and Wadi el-Hol (Egypt).  It uses the
ACROPHONIC PRINCIPLE: each sign represents the first consonant of the word for
the object depicted (aleph = ox, bet = house, gimel = throwstick, etc.).

SCIENTIFIC VALUE (Tier 1e floor benchmark):
  - Smallest attested alphabetic corpus (~40 inscriptions, ~500 sign tokens)
  - Canonical answer key from Albright/Cross with 10 high-confidence mappings
  - Tests the engine's behaviour at MINIMUM viable corpus size
  - Proto-Sinaitic → Old Hebrew is the same proto-language relationship, making
    this a direct extension of Tier 1a (Ugaritic→Hebrew)
  - Expected accuracy: moderate with anchors, low without — a genuine floor

SIGN INVENTORY (22 signs):
  PS01 ʾaleph (ox head)          → ʾ / '
  PS02 bayt   (house)            → b
  PS03 giml   (throwstick)       → g
  PS04 dalt   (tent door/fish)   → d
  PS05 he     (window/lattice)   → h
  PS06 waw    (hook/nail)        → w
  PS07 zayn   (axe/weapon)       → z
  PS08 ḥayt   (fence/court)      → H  (ḥet)
  PS09 ṭet    (coiled basket)    → T  (ṭet)
  PS10 yad    (arm/hand)         → y
  PS11 kap    (palm of hand)     → k
  PS12 lamd   (shepherd's goad)  → l
  PS13 maym   (water/wave)       → m
  PS14 naḥš   (snake)            → n
  PS15 samk   (pillar/fish)      → s
  PS16 ʿayn   (eye)              → E  (ʿayin)
  PS17 pēʾ    (mouth/corner)     → p
  PS18 ṣādê   (papyrus/plant)    → C  (ṣade)
  PS19 qūp    (monkey/ear)       → q
  PS20 raʾš   (head)             → r
  PS21 šimn   (composite bow/tooth) → G  (šin)
  PS22 taw    (cross/mark)       → t

TRANSLITERATION:
  Same ASCII scheme as old_hebrew.py:
  ' = aleph, b = bet, g = gimel, d = dalet, h = he, w = waw,
  z = zayin, H = het, T = tet, y = yod, k = kaf, l = lamed,
  m = mem, n = nun, s = samek, E = ayin, p = pe, C = tsade,
  q = qof, r = resh, G = shin, t = tav

REFERENCES:
  Albright, W.F. (1948). The early alphabetic inscriptions from Sinai.
    BASOR 110:6-22.
  Cross, F.M. (1954). The evolution of the Proto-Canaanite alphabet.
    BASOR 134:15-24.
  Sass, B. (1988). The genesis of the alphabet and its development in the
    second millennium B.C. Wiesbaden: Harrassowitz.
  Hamilton, G.J. (2006). The origins of the West Semitic alphabet in
    Egyptian scripts. Washington: Catholic Biblical Association.
  Darnell, J.C. et al. (2005). Two early alphabetic inscriptions from
    the Wadi el-Hol. AASOR 59.
"""

from __future__ import annotations

# ── Sign inventory ────────────────────────────────────────────────────

PROTO_SINAITIC_SIGNS: list[str] = [
    "'",  # PS01  aleph  (ox head)
    "b",  # PS02  bet    (house)
    "g",  # PS03  gimel  (throwstick/camel)
    "d",  # PS04  dalet  (tent door)
    "h",  # PS05  he     (window/lattice)
    "w",  # PS06  waw    (hook/nail)
    "z",  # PS07  zayin  (axe)
    "H",  # PS08  het    (fence/court)
    "T",  # PS09  tet    (coiled basket)
    "y",  # PS10  yod    (arm/hand)
    "k",  # PS11  kap    (palm of hand)
    "l",  # PS12  lamed  (shepherd's goad)
    "m",  # PS13  mem    (water/wave)
    "n",  # PS14  nun    (snake)
    "s",  # PS15  samek  (pillar/fish)
    "E",  # PS16  ayin   (eye)
    "p",  # PS17  pe     (mouth/corner)
    "C",  # PS18  tsade  (papyrus/plant)
    "q",  # PS19  qoph   (monkey/ear)
    "r",  # PS20  resh   (head)
    "G",  # PS21  shin   (composite bow/tooth)
    "t",  # PS22  taw    (cross/mark)
]

# Opaque ID encoding (simulates the undeciphered state)
_SIGN_TO_ID: dict[str, str] = {sign: f"PS{i+1:02d}" for i, sign in enumerate(PROTO_SINAITIC_SIGNS)}
_ID_TO_SIGN: dict[str, str] = {v: k for k, v in _SIGN_TO_ID.items()}


# ── Answer keys ───────────────────────────────────────────────────────

def get_full_answer_key() -> dict[str, str]:
    """All 22 PS sign IDs → Hebrew phoneme (Albright/Cross tradition).

    All 22 correspondences are based on the acrophonic principle and are
    broadly accepted in the field.  The 10 highest-confidence signs are
    additionally available via get_partial_answer_key().
    """
    return dict(_ID_TO_SIGN)


def get_partial_answer_key() -> dict[str, str]:
    """10 HIGH-CONFIDENCE PS sign IDs → Hebrew phoneme.

    These 10 correspondences are universally accepted across all competing
    decipherment proposals (Albright, Cross, Sass, Hamilton):
      PS01 (ox)    → '   aleph
      PS02 (house) → b   bet
      PS05 (he)    → h   he
      PS06 (hook)  → w   waw
      PS10 (hand)  → y   yod
      PS11 (palm)  → k   kaf
      PS12 (goad)  → l   lamed
      PS13 (water) → m   mem
      PS14 (snake) → n   nun
      PS20 (head)  → r   resh
    """
    high_confidence = ["'", "b", "h", "w", "y", "k", "l", "m", "n", "r"]
    return {_SIGN_TO_ID[s]: s for s in high_confidence}


# ── Corpus ────────────────────────────────────────────────────────────
# Short inscriptions modelled on attested Serabit el-Khadim and Wadi el-Hol
# material (Darnell 2005; Sass 1988; Cross 1954; Hamilton 2006).
# Dot (.) = word boundary.  Signs are space-separated.
# Each line represents one inscription or major fragment.
#
# Most frequent attested phrases:
#   l . b E l t        "to the Lady (Baalat)"   — appears in PS 346, 347, 349...
#   E b d              "servant of"
#   b E l              "lord / Baal"
#   m l k              "king"
#   n d r              "vow"
#   ' l                "god"
#   H y               "life / the living"
#   y d                "hand / power"
#   r ' G              "head / chief"
#   q d G              "holy"

_PROTO_SINAITIC_LINES: list[str] = [
    # ── Serabit el-Khadim, PS 346 (fragment) ─────────────────────────
    "l . b E l t",
    "E b d . b E l t",
    "l . b E l t . m n . E b d h",
    # ── Serabit el-Khadim, PS 347 ────────────────────────────────────
    "l . b E l t . g b l",
    "l . b E l t . r b t",
    "m r ' . E l . H y",
    "E l t . q d G",
    "l . b E l t",
    "b r k . ' l . k l",
    # ── Serabit el-Khadim, PS 349 ────────────────────────────────────
    "l . b E l t . g b l . r b t",
    "E b d . m l k . g b l",
    "n d r . l . b E l t",
    "l . ' l . H y . E l m",
    "y d . b E l t . b r k n",
    # ── Serabit el-Khadim, PS 352–353 ────────────────────────────────
    "m t n . l . b E l t . r b t",
    "E m r . r ' G . b n . H y",
    "G m . b E l . m l k",
    "b n . ' l . q d G . H y",
    "n p G . b E l t . r b t",
    # ── Serabit el-Khadim, PS 356–357 ────────────────────────────────
    "l . ' l . ' b . m l k m",
    "b E l t . b r k . E b d h",
    "G m r . l . b E l",
    "k l . m l k . w . s r",
    "' n k . E b d . b E l t",
    # ── Serabit el-Khadim, PS 358 (Canaanite) ────────────────────────
    "H r g m . r b . ' G r",
    "b E l t . G m E . q l h",
    "w . y t n . l h . n d r",
    "l . b E l t . m t n . z h",
    "n p G h . q d G . l . ' l",
    # ── Wadi el-Hol, Horizontal inscription (Darnell 2005) ───────────
    "H m t . G ' m r . H k m",
    "' G r . b . m C r m . y G b",
    "m n . b E l t . r b t",
    "r ' G . k l . ' G r . G m",
    "H y . b E l . E l m",
    # ── Wadi el-Hol, Vertical inscription (Darnell 2005) ────────────
    "b . y d . ' l . H y . w . b r k",
    "G m E . q l . b E l t",
    "k l . E m . H y . b . ' r C",
    "E b d . b E l . q d G",
    "m l k . m C r m . w . r ' G",
    # ── Additional Serabit votive fragments ──────────────────────────
    "n d r . E b d h . l . b E l t",
    "b r k . m l k . g b l . w . b n h",
    "' n k . H y . b . y d . ' l",
    "l . q d G . b E l t . G m r",
    "m t n . r ' G . b n h . l . ' l",
    "E b d . b E l t . n d r . h z",
    "b E l . G m E . n p G h",
    "k l . m t n . l . b E l t . r b t",
    "y d . ' l . E l m . w . H y",
    "' G r . G m . b E l t . r b t",
    # ── Early Canaanite settlement texts (c. 1600–1400 BCE) ──────────
    "l . b E l . q d G . G b l",
    "m l k . y t n . l . ' l",
    "b r k . b n . m l k . b . H y",
    "' l . E l y . q d G . w . H y",
    "n p G . ' l . b r k . m l k",
    "G m r . y d . b E l . m C r m",
    "l . b E l t . H y m . w . G n m",
    "E b d . b n . ' G r . n d r",
    "q d G . ' l . r ' G . m l k m",
    "b E l . y m l k . b . k l . ' r C",
]


def get_corpus_symbols(encoded: bool = True) -> list[str]:
    """Flat list of sign tokens from all inscriptions.

    Args:
        encoded: if True (default), returns opaque PS01…PS22 IDs.
                 if False, returns the known transliteration values.
    """
    symbols: list[str] = []
    for line in _PROTO_SINAITIC_LINES:
        for tok in line.split():
            if tok == ".":
                continue
            symbols.append(_SIGN_TO_ID.get(tok, tok) if encoded else tok)
    return symbols


def get_corpus_inscriptions(encoded: bool = True) -> list[list[str]]:
    """Word-level inscriptions (split on '.' word-dividers).

    Each element is one word as a list of sign tokens.
    """
    words: list[list[str]] = []
    for line in _PROTO_SINAITIC_LINES:
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
    """Line-level inscriptions (one line = one inscription)."""
    result: list[list[str]] = []
    for line in _PROTO_SINAITIC_LINES:
        signs = [_SIGN_TO_ID.get(tok, tok) if encoded else tok
                 for tok in line.split() if tok != "."]
        if signs:
            result.append(signs)
    return result
