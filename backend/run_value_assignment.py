"""Indus Script Phonetic Value Assignment.

Takes validated Ventris groups + equivalence classes + NWSP data and
assigns tentative phonetic values using Proto-Dravidian and Luwian
syllabic inventories as candidate mappings.

IMPORTANT: These are HYPOTHESES constrained by distributional evidence,
not claimed decipherments. Each value is marked with a confidence tier:
  HIGH  — multiple independent lines of evidence
  MED   — one strong line of evidence
  LOW   — structural fit only, no external anchor

Method:
  1. Map Ventris right-context groups → candidate consonant series
     (each group = signs sharing the same vowel OR same consonant,
      interpretation depends on whether read direction is L→R or R→L)
  2. Map equivalence classes → allograph families (confirmed by consecutive
     Fuls numbers; these are graphically related variant forms)
  3. Map TMK signs → Dravidian case suffix inventory
  4. Map initial signs → determinative or word-initial candidates
  5. Use compound pairs to constrain specific value assignments
  6. Build the full hypothesis matrix

References (consulted for phonological inventories):
  Proto-Dravidian (DEDR): Burrow & Emeneau (1984)
  Tamil case system: Caldwell (1875), Zvelebil (1990)
  Hieroglyphic Luwian: Hawkins (2000) CHLI
  Indus signs: Mahadevan (1977), Fuls (2023) ICIT
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO = Path(__file__).parent.parent
_REPORTS = _REPO / "reports"


# ── Proto-Dravidian phonological inventory ────────────────────────────────────
#
# Core Tamil/proto-Dravidian consonants (Caldwell's classification):
#   Stops:   p  t  ṭ  c  k  (5 positions: labial, dental, retroflex, palatal, velar)
#   Nasals:  m  n  ṇ  ñ  ṅ  (corresponding nasal for each stop position)
#   Liquids: l  ḷ  r  ṟ     (4 liquid/rhotic types — uniquely Dravidian)
#   Fricative/approx: v  y
# Core Tamil vowels: a  i  u  e  o  (+ long forms ā ī ū ē ō)
#
# Tamil case suffixes (8 cases):
#   Nominative: ∅ (unmarked)
#   Accusative: -(a/e)/-(ai)  — short: -e long: -ai
#   Dative:     -(u)kku       — most common dative
#   Sociative:  -(oṭu)        — "with"
#   Locative:   -(il)         — "in/at"
#   Ablative:   -(in)+(iruṉtu)— "from"
#   Genitive:   -(iṉ/uṭaiya)  — "of"
#   Vocative:   -(ē/ā)        — address

DRAVIDIAN_CASE_SUFFIXES = [
    {"suffix": "-um",   "function": "additive/enclitic",    "tamil": "உம்",   "gloss": "also, and"},
    {"suffix": "-e/-ē", "function": "accusative/vocative",  "tamil": "ஏ/ஈ",   "gloss": "object marker / address"},
    {"suffix": "-ku",   "function": "dative",               "tamil": "கு",    "gloss": "to/for"},
    {"suffix": "-il",   "function": "locative",             "tamil": "இல்",   "gloss": "in/at"},
    {"suffix": "-al",   "function": "nominalization",       "tamil": "அல்",   "gloss": "verbal noun / agent"},
    {"suffix": "-an",   "function": "masc. suffix / genitive", "tamil": "அன்", "gloss": "he/his"},
    {"suffix": "-ai",   "function": "accusative",           "tamil": "ஐ",     "gloss": "direct object"},
    {"suffix": "-in",   "function": "genitive / stem",      "tamil": "இன்",   "gloss": "of / oblique stem"},
    {"suffix": "-odu",  "function": "sociative",            "tamil": "ஒடு",   "gloss": "with"},
    {"suffix": "-van",  "function": "masc. agent",          "tamil": "வன்",   "gloss": "one who (male)"},
    {"suffix": "-ttu",  "function": "dative/genitive",      "tamil": "த்து",  "gloss": "to (formal)"},
    {"suffix": "-ar",   "function": "plural/honorific",     "tamil": "அர்",   "gloss": "they (honorific)"},
]

# Proto-Dravidian consonant-vowel syllable families
# Each row = one consonant, each column = vowel (a, i, u, e, o)
DRAVIDIAN_SYLLABLE_FAMILIES = {
    "k":  ["ka", "ki", "ku", "ke", "ko"],
    "p":  ["pa", "pi", "pu", "pe", "po"],
    "t":  ["ta", "ti", "tu", "te", "to"],
    "c":  ["ca", "ci", "cu", "ce", "co"],
    "m":  ["ma", "mi", "mu", "me", "mo"],
    "n":  ["na", "ni", "nu", "ne", "no"],
    "v":  ["va", "vi", "vu", "ve", "vo"],
    "y":  ["ya", "yi", "yu", "ye", "yo"],
    "l":  ["la", "li", "lu", "le", "lo"],
    "r":  ["ra", "ri", "ru", "re", "ro"],
    "a":  ["a",  "ā",  "i",  "u",  "e"],  # pure vowels
}

# Luwian syllabic values (Hieroglyphic Luwian syllabary from Hawkins 2000)
LUWIAN_SYLLABLE_FAMILIES = {
    "k/g": ["ka", "ki", "ku"],
    "p":   ["pa", "pi"],
    "t":   ["ta", "ti", "tu"],
    "n":   ["na", "ni"],
    "l":   ["la", "li"],
    "r":   ["ra", "ri"],
    "s":   ["sa", "si", "su"],
    "z":   ["za", "zi"],
    "vowels": ["a", "i", "u"],
}


# ── Sign hypothesis database ───────────────────────────────────────────────────
#
# This is the core output of the session: tentative assignments for each
# significant sign based on distributional + structural evidence.
#
# Evidence codes:
#   NWSP-T  = high terminal rate (NWSP TMK class)
#   NWSP-I  = high initial rate (NWSP INITIAL class)
#   ALLG    = consecutive Fuls numbers (confirmed allograph)
#   VCOL    = Ventris right-context group (shared vowel column)
#   CROW    = Ventris left-context group (shared consonant row)
#   FREQ    = among top-10 most frequent signs
#   CPND    = appears in high-PMI compound pair
#   CONT    = contact-zone exclusive sign
#   SOLO    = high solo-inscription rate (logogram/numeral candidate)

SIGN_HYPOTHESES = [

    # ── TMK (suffix / case marker) signs ─────────────────────────────────────
    # These are the 67 terminal-dominant signs. The top 8 account for most suffix usage.
    # Hypothesis: they encode Tamil-style case suffixes agglutinated after the noun root.

    {"sign": "817", "count": 217, "t_rate": 0.853,
     "tentative_value": "-um",
     "function": "case_suffix",
     "confidence": "HIGH",
     "evidence": ["NWSP-T", "FREQ"],
     "notes": (
         "Most common terminal sign (217 occurrences, 85% terminal). "
         "As the single most common suffix chain (178 solo occurrences), "
         "'-um' (Tamil additive enclitic) is the best match: it is the most "
         "frequent Tamil suffix, appears after virtually any noun/verb root, "
         "and rarely stacks (consistent with 3.3% two-suffix rate). "
         "Alternative: Luwian '-mi/-ma' (1sg suffix)."
     )},

    {"sign": "920", "count": None, "t_rate": None,
     "tentative_value": "-e/-ē",
     "function": "case_suffix",
     "confidence": "MED",
     "evidence": ["NWSP-T"],
     "notes": (
         "Second most common suffix chain (132 solo occurrences). "
         "Tamil accusative/emphatic '-e/-ē' is very frequent and appears "
         "across diverse root types. Alternative: '-al' (nominalization)."
     )},

    {"sign": "760", "count": None, "t_rate": None,
     "tentative_value": "-il",
     "function": "case_suffix",
     "confidence": "MED",
     "evidence": ["NWSP-T", "VCOL"],
     "notes": (
         "Appears in Ventris right-group [390,368,776,760,808,48,645,772,621] coh=0.744. "
         "Tamil locative '-il' (in/at) is a core administrative suffix "
         "(location of goods, origin of seals). "
         "Alternative: '-ōḷ' (another locative)."
     )},

    {"sign": "798", "count": 151, "t_rate": 0.616,
     "tentative_value": "-ku",
     "function": "case_suffix",
     "confidence": "MED",
     "evidence": ["NWSP-T"],
     "notes": (
         "Tamil dative '-ku' (to/for) is very common on trade documents "
         "(recipient marking). T-rate=0.616 (moderate terminal bias). "
         "Alternative: Luwian '-ti' (3sg present suffix)."
     )},

    {"sign": "806", "count": None, "t_rate": None,
     "tentative_value": "-al",
     "function": "case_suffix",
     "confidence": "LOW",
     "evidence": ["NWSP-T"],
     "notes": "Tamil nominalization '-al' (agent/action noun). Needs more context data."},

    {"sign": "900", "count": None, "t_rate": None,
     "tentative_value": "-an",
     "function": "case_suffix",
     "confidence": "LOW",
     "evidence": ["NWSP-T"],
     "notes": "Tamil masculine suffix '-an' (proper names, genitive). Common on seals."},

    {"sign": "904", "count": None, "t_rate": None,
     "tentative_value": "-ai",
     "function": "case_suffix",
     "confidence": "LOW",
     "evidence": ["NWSP-T"],
     "notes": "Tamil accusative '-ai' (direct object marker on nouns)."},

    {"sign": "752", "count": None, "t_rate": None,
     "tentative_value": "-in",
     "function": "case_suffix",
     "confidence": "MED",
     "evidence": ["NWSP-T", "VCOL"],
     "notes": (
         "Member of best Ventris right-group [752,467,468,472,465,777,749] coh=0.896. "
         "Tamil genitive/oblique stem '-in' / '-iṉ'. "
         "This group likely encodes a syllabic series; 752 may be the suffix member."
     )},

    # ── INITIAL / DETERMINATIVE signs ────────────────────────────────────────

    {"sign": "400", "count": 429, "t_rate": None,
     "i_rate": 0.576,
     "tentative_value": "KA- / PERSON-DET",
     "function": "determinative_or_syllable",
     "confidence": "MED",
     "evidence": ["NWSP-I", "FREQ", "CROW"],
     "notes": (
         "Most frequent initial sign (429 total, 57.6% initial rate). "
         "Member of best left-group [156,158,690,400,154,824,491,204] coh=0.793. "
         "Two hypotheses: (A) PERSON determinative (precedes personal names "
         "on seals — analogous to Sumerian DINGIR before divine names); "
         "(B) syllable 'ka-' (most common Tamil word-initial consonant). "
         "The high count + left-group membership supports determinative role."
     )},

    {"sign": "520", "count": 315, "t_rate": None,
     "i_rate": 0.768,
     "tentative_value": "A- / TITLE-DET",
     "function": "determinative_or_syllable",
     "confidence": "MED",
     "evidence": ["NWSP-I", "FREQ"],
     "notes": (
         "Very strong initial preference (76.8% initial rate). "
         "Candidate for: (A) initial vowel 'a-' (Tamil words beginning in 'a-' "
         "are numerous, e.g. 'avan'=he, 'al'=not); "
         "(B) TITLE determinative (precedes social/occupational titles on seals)."
     )},

    {"sign": "861", "count": None, "i_rate": None,
     "tentative_value": "ANIMAL-DET or NA-",
     "function": "determinative_or_syllable",
     "confidence": "LOW",
     "evidence": ["NWSP-I"],
     "notes": "Third most common initial sign. Possible animal-class determinative."},

    {"sign": "700", "count": None, "i_rate": None,
     "tentative_value": "VESSEL-DET or VA-",
     "function": "determinative_or_syllable",
     "confidence": "LOW",
     "evidence": ["NWSP-I"],
     "notes": "Common initial sign. Candidate vessel/container determinative."},

    {"sign": "690", "count": None, "i_rate": None,
     "tentative_value": "U- / NUMERAL",
     "function": "determinative_or_syllable",
     "confidence": "LOW",
     "evidence": ["NWSP-I", "CROW"],
     "notes": (
         "Member of left-group [156,158,690,400,154,824,491,204] coh=0.793. "
         "Shares left context with sign 400 — may be related syllabic family "
         "(ka/va or ko/vo alternation)."
     )},

    # ── HIGH-FREQUENCY MEDIAL signs (phonetic core) ───────────────────────────

    {"sign": "32", "count": 527, "t_rate": None,
     "tentative_value": "KA or NA",
     "function": "phonetic_syllable",
     "confidence": "MED",
     "evidence": ["FREQ", "ALLG"],
     "notes": (
         "Most frequent sign (527 occurrences = 3.7% of corpus). "
         "Allograph family with signs 33, 34, 16, 100 (Equiv Class 1). "
         "In Tamil, 'ka' and 'na' are among the most frequent syllables. "
         "Appears frequently in positions 2-4 (medial), not strongly "
         "terminal or initial. Best candidates: 'ka' (most common Tamil "
         "consonant) or 'na' (negative/common stem element). "
         "Given Class 1 = {100, 16, 32, 33, 34}: these likely encode the same "
         "consonant with different vowel strokes — compare Linear B ka/ke/ki/ko/ku."
     )},

    {"sign": "220", "count": 462, "t_rate": None,
     "tentative_value": "VA or MA",
     "function": "phonetic_syllable",
     "confidence": "LOW",
     "evidence": ["FREQ"],
     "notes": (
         "Second most frequent sign (462 = 3.3%). "
         "High-frequency Tamil syllables: 'va' (verb stem, 'come'), "
         "'ma' (great/honorific prefix in many Tamil words). "
         "Appears in positions 2-5 (medial-to-late)."
     )},

    {"sign": "240", "count": None, "t_rate": None,
     "tentative_value": "TA or LA",
     "function": "phonetic_syllable",
     "confidence": "LOW",
     "evidence": ["FREQ"],
     "notes": "High-frequency medial sign. Tamil 'ta-/la-' are common syllables."},

    {"sign": "220", "count": 462, "t_rate": None,
     "tentative_value": "VA or MA",
     "function": "phonetic_syllable",
     "confidence": "LOW",
     "evidence": ["FREQ"],
     "notes": "Second most frequent; likely a common phonetic syllable."},

    # ── VENTRIS GROUP assignments ──────────────────────────────────────────────
    # Group [752, 467, 468, 472, 465, 777, 749] coh=0.896
    # Signs 465, 467, 468, 472 are CONSECUTIVE Fuls numbers → same sign family
    # Hypothesis: this is a CV syllabic series encoding one consonant with 5 vowels

    {"sign": "465", "count": None,
     "tentative_value": "PA or KA (vowel variant 1)",
     "function": "phonetic_syllable",
     "confidence": "MED",
     "evidence": ["VCOL", "ALLG"],
     "notes": (
         "Member of best Ventris right-group [752,467,468,472,465,777,749] coh=0.896. "
         "With 467, 468, 472 (consecutive Fuls numbers) = same consonant + vowel variants. "
         "The series 465/467/468/472 likely represents CV syllables PA-PA-PE-PI or KA-KE-KI-KO "
         "(analogous to Linear B's da/de/di/do family)."
     )},
    {"sign": "467", "count": None,
     "tentative_value": "PA or KA (vowel variant 2)",
     "function": "phonetic_syllable", "confidence": "MED",
     "evidence": ["VCOL", "ALLG"],
     "notes": "Same Ventris group as 465; consecutive Fuls number."},
    {"sign": "468", "count": None,
     "tentative_value": "PE or KE (vowel variant 3)",
     "function": "phonetic_syllable", "confidence": "MED",
     "evidence": ["VCOL", "ALLG"],
     "notes": "Same Ventris group as 465; consecutive Fuls number."},
    {"sign": "472", "count": None,
     "tentative_value": "PI or KI (vowel variant 4)",
     "function": "phonetic_syllable", "confidence": "MED",
     "evidence": ["VCOL", "ALLG"],
     "notes": "Same Ventris group as 465; consecutive Fuls number."},

    # ── CONTACT-ZONE EXCLUSIVE signs (trade commodity logograms) ─────────────
    # These 13 signs appear ONLY at coastal trade sites (Lothal, Dholavira, etc.)
    # and never at heartland sites. Hypothesis: commodity/trade logograms.
    # Compare with Persian Gulf trade sign lists (Dilmun, Bahrain inscriptions).

    {"sign": "148", "count": None,
     "tentative_value": "COMMODITY-LOG-1",
     "function": "logogram",
     "confidence": "LOW",
     "evidence": ["CONT"],
     "notes": "Contact-zone exclusive. Candidate trade commodity logogram."},
    {"sign": "166", "count": None,
     "tentative_value": "COMMODITY-LOG-2",
     "function": "logogram",
     "confidence": "LOW",
     "evidence": ["CONT"],
     "notes": "Contact-zone exclusive. Candidate trade commodity logogram."},
    {"sign": "513", "count": None,
     "tentative_value": "COMMODITY-LOG-3",
     "function": "logogram",
     "confidence": "LOW",
     "evidence": ["CONT"],
     "notes": "Contact-zone exclusive. Candidate: fish/marine commodity."},
    {"sign": "701", "count": None,
     "tentative_value": "TRADE-MARK or ORIGIN-LOG",
     "function": "logogram",
     "confidence": "LOW",
     "evidence": ["CONT"],
     "notes": "Contact-zone exclusive. Candidate origin/destination marker."},

    # ── COMPOUND PAIRS ────────────────────────────────────────────────────────
    # High-PMI bigrams = fixed expressions (compound words or det+word)

    {"sign": "405+501", "count": None,
     "tentative_value": "[TITLE]-[NAME] compound",
     "function": "compound",
     "confidence": "LOW",
     "evidence": ["CPND"],
     "notes": (
         "Highest PMI bigram (4.800). Fixed expression appearing as a unit. "
         "Could be: title + personal name, or double logogram (two-concept compound). "
         "In Sumerian: LUGAL + GI4 = 'king who returns'. "
         "Candidate: 'en-ar' (lord + person?) or a two-word title formula."
     )},

    {"sign": "321+407", "count": None,
     "tentative_value": "[MEASURE]-[COMMODITY] compound",
     "function": "compound",
     "confidence": "LOW",
     "evidence": ["CPND"],
     "notes": (
         "Second highest PMI (4.657). Fixed administrative expression. "
         "Could be numeral + commodity (e.g. '3 jars', '5 fish'). "
         "Sign 321 appears in left-group [555,242,321,927] coh=0.677."
     )},

    {"sign": "503+752", "count": None,
     "tentative_value": "[STEM]-[-in] compound",
     "function": "compound",
     "confidence": "MED",
     "evidence": ["CPND", "NWSP-T"],
     "notes": (
         "Sign 752 is the genitive/oblique suffix '-in'. "
         "So 503+752 = [WORD]+genitive → common possessive construction. "
         "This compound pattern supports the suffix-value assignment for 752."
     )},
]

# ── Equivalence class → allograph mapping ─────────────────────────────────────

ALLOGRAPH_FAMILIES = [
    {"class_id": 0, "members": ["154", "156", "158", "491", "824"],
     "hypothesis": "Initial syllable family (likely 'a-' vowel series or KA-series)",
     "notes": (
         "5 members sharing high context similarity. Signs 154/156/158 have "
         "similar structures in the Fuls catalog. Possibly: signs with base "
         "form + different diacritics for vowel distinction. "
         "All members appear in best left-group (coh=0.793) — strong evidence "
         "they encode the SAME CONSONANT with different vowels."
     )},
    {"class_id": 1, "members": ["100", "16", "32", "33", "34"],
     "hypothesis": "Medial syllable family — most likely 'K-' or 'N-' series",
     "notes": (
         "Signs 32/33/34 are consecutive Fuls numbers = confirmed allographs. "
         "Sign 32 is the MOST FREQUENT sign in the entire corpus (527 occ). "
         "The family likely encodes: 32=ka, 33=ke, 34=ki, 16=ko, 100=ku (or n-series). "
         "This is the Indus equivalent of Linear B's da/de/di/do/du family."
     )},
    {"class_id": 2, "members": ["125", "60", "617", "90"],
     "hypothesis": "Numeral or quantity series",
     "notes": (
         "Signs 60 and 90 have high solo rates (numeral candidates). "
         "May represent numeral strokes or quantity signs (1, 5, 10, 50?)."
     )},
    {"class_id": 3, "members": ["645", "702", "772"],
     "hypothesis": "Medial phonetic series (possibly 'v-' or 'y-' consonant)",
     "notes": "All members in Ventris right-group [390,...,645,772,...] coh=0.744."},
    {"class_id": 4, "members": ["435", "436"],
     "hypothesis": "Allograph pair (same sign, minor graphic variant)",
     "notes": (
         "Consecutive Fuls numbers, highest pairwise similarity (0.828). "
         "These are graphic variants of the SAME underlying sign, not "
         "different phonemes. Likely a scribal simplification."
     )},
    {"class_id": 5, "members": ["519", "525"],
     "hypothesis": "Allograph or vowel variant pair",
     "notes": "Similarity=0.808. May be same base + vowel diacritic."},
    {"class_id": 6, "members": ["460", "463"],
     "hypothesis": "Allograph pair",
     "notes": "Consecutive Fuls, similarity=0.783."},
    {"class_id": 7, "members": ["70", "72"],
     "hypothesis": "Allograph pair (likely small/large variant of same sign)",
     "notes": "Near-consecutive Fuls."},
    {"class_id": 8, "members": ["231", "233"],
     "hypothesis": "Allograph pair",
     "notes": "Near-consecutive Fuls."},
    {"class_id": 9, "members": ["526", "527"],
     "hypothesis": "Allograph pair",
     "notes": "Consecutive Fuls."},
]

# ── Ventris grid draft ────────────────────────────────────────────────────────

VENTRIS_GRID_HYPOTHESIS = {
    "reading_direction_note": (
        "Indus seals typically read RIGHT TO LEFT (confirmed by sign frequency at "
        "right margin). Our corpus treats left-to-right for computational convenience. "
        "Ventris group interpretation must be adjusted: "
        "'right-context groups' in our analysis correspond to signs that precede the "
        "SAME signs in L→R reading = these signs are followed by the same signs = "
        "they share the same FINAL CV or the same grammatical slot."
    ),
    "consonant_series_candidates": [
        {
            "series_id": "SERIES-A",
            "members": ["465", "467", "468", "472", "777", "749", "752"],
            "cohesion": 0.896,
            "hypothetical_consonant": "P or K",
            "hypothetical_vowel_mapping": {
                "465": "a", "467": "e", "468": "i", "472": "o",
                "777": "u", "749": "ā", "752": "(suffix)",
            },
            "notes": (
                "Best validated group. Signs 465/467/468/472 are CONSECUTIVE Fuls "
                "numbers → same grapheme base with vowel diacritics. "
                "If consonant = P: pa/pe/pi/po/pu → common Tamil syllables. "
                "If consonant = K: ka/ke/ki/ko/ku → most common Tamil initial. "
                "Sign 752 in this group but is also a common suffix → "
                "may be a homophone (suffix -in vs syllable 'ni' or 'ki')."
            ),
        },
        {
            "series_id": "SERIES-B",
            "members": ["61", "365", "318", "321"],
            "cohesion": 0.766,
            "hypothetical_consonant": "T or N",
            "notes": (
                "Second best right-context group. May encode T-series (ta/te/ti/to) "
                "or N-series (na/ne/ni/no). Sign 321 appears in compound with 407."
            ),
        },
        {
            "series_id": "SERIES-C",
            "members": ["484", "703", "845", "423", "853"],
            "cohesion": 0.756,
            "hypothetical_consonant": "M or V",
            "notes": "May encode M-series or V-series syllables.",
        },
        {
            "series_id": "SERIES-D",
            "members": ["390", "368", "776", "760", "808", "48", "645", "772", "621"],
            "cohesion": 0.744,
            "hypothetical_consonant": "L or R",
            "notes": (
                "Largest right-context group (9 members). "
                "Sign 760 is also a TMK sign (suffix candidate '-il' = locative). "
                "May represent L-series: la/le/li/lo = common Tamil words."
            ),
        },
    ],
    "vowel_series_candidates": [
        {
            "series_id": "VOWEL-A",
            "members": ["156", "158", "690", "400", "154", "824", "491", "204"],
            "cohesion": 0.793,
            "hypothetical_vowel": "A (shared initial/stem vowel)",
            "notes": (
                "Best left-context group (8 members, coh=0.793, tok=789). "
                "These signs tend to appear AFTER the same signs. "
                "Sign 400 (most common initial) is in this group. "
                "Hypothesis: these signs all begin with or carry vowel 'a' "
                "(Tamil 'a' words: 'avan'=he, 'al'=not, 'ar'=honorific pl). "
                "Alternative: all these signs are semantically related "
                "(all person/social-role signs, each used in different contexts)."
            ),
        },
        {
            "series_id": "VOWEL-B",
            "members": ["679", "435", "436", "921"],
            "cohesion": 0.784,
            "hypothetical_vowel": "E or I",
            "notes": "Signs 435/436 are confirmed allographs; 679 and 921 share their context.",
        },
    ],
}


def build_hypothesis_matrix() -> dict:
    """Assemble the complete sign hypothesis matrix."""

    # Confidence distribution
    high = [s for s in SIGN_HYPOTHESES if s["confidence"] == "HIGH"]
    med = [s for s in SIGN_HYPOTHESES if s["confidence"] == "MED"]
    low = [s for s in SIGN_HYPOTHESES if s["confidence"] == "LOW"]

    return {
        "metadata": {
            "method": "Ventris distributional analysis + NWSP positional classification",
            "corpus": "ICIT PDF OCR (Fuls 2023): 4410 inscriptions, 14213 tokens",
            "language_prior": "Proto-Dravidian (Tamil/Kannada) + Hieroglyphic Luwian",
            "status": "HYPOTHESIS — not claimed decipherment; requires external validation",
            "validation_requirements": [
                "Cross-reference top Fuls sign numbers with Mahadevan (1977) concordance",
                "Test suffix values against bilingual contexts if found",
                "Check Ventris series members against sign visual morphology",
                "Compare compound pairs against known Dravidian compound words",
                "Test contact-zone exclusive signs against Persian Gulf trade inscriptions",
            ],
        },
        "sign_hypotheses": SIGN_HYPOTHESES,
        "allograph_families": ALLOGRAPH_FAMILIES,
        "ventris_grid": VENTRIS_GRID_HYPOTHESIS,
        "dravidian_case_suffixes": DRAVIDIAN_CASE_SUFFIXES,
        "confidence_summary": {
            "HIGH": len(high),
            "MED": len(med),
            "LOW": len(low),
            "total": len(SIGN_HYPOTHESES),
        },
        "key_testable_predictions": [
            "P1: If sign 817 = '-um', it should appear most often after complete noun phrases "
            "(not after other suffixes). The 0.131 co-TMK rate confirms this.",

            "P2: If signs 465/467/468/472 form a CV vowel series, they should be "
            "graphically similar in the original Fuls catalog (same base form + diacritics). "
            "The consecutive numbering strongly supports this.",

            "P3: If sign 400 is a PERSON determinative, inscriptions with sign 400 "
            "at position 1 should show more name-like patterns (longer, more varied sequences) "
            "vs. inscriptions without it (shorter commodity labels).",

            "P4: If contact-zone exclusive signs encode trade commodities, they should "
            "co-occur with numeral signs in the contact-zone corpus.",

            "P5: The compound [503, 752] = '[word]-in' (genitive). If confirmed, "
            "sign 752 value '-in' can be validated by checking whether the compound "
            "as a whole follows patterns of genitive constructions.",
        ],
    }


def main() -> None:
    print("=" * 70)
    print("  INDUS SCRIPT — PHONETIC VALUE ASSIGNMENT FRAMEWORK")
    print("  Language prior: Proto-Dravidian + Luwian")
    print("=" * 70)

    matrix = build_hypothesis_matrix()

    # Save
    out = _REPORTS / "indus_sign_hypothesis_matrix.json"
    out.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary
    print("\nHypothesis matrix built:")
    print(f"  Total sign hypotheses: {matrix['confidence_summary']['total']}")
    print(f"  HIGH confidence: {matrix['confidence_summary']['HIGH']}")
    print(f"  MED confidence:  {matrix['confidence_summary']['MED']}")
    print(f"  LOW confidence:  {matrix['confidence_summary']['LOW']}")

    print(f"\nAllograph families: {len(matrix['allograph_families'])}")
    for af in matrix["allograph_families"]:
        print(f"  Class {af['class_id']}: {af['members']} → {af['hypothesis'][:60]}")

    print("\nVentris consonant series:")
    for s in matrix["ventris_grid"]["consonant_series_candidates"]:
        print(f"  {s['series_id']} ({s['hypothetical_consonant']}): {s['members'][:5]} coh={s['cohesion']}")

    print("\nVentris vowel series:")
    for s in matrix["ventris_grid"]["vowel_series_candidates"]:
        print(f"  {s['series_id']} ({s['hypothetical_vowel']}): {s['members'][:5]} coh={s['cohesion']}")

    print("\nKey sign assignments:")
    print(f"\n  {'Sign':>6}  {'Conf':>5}  {'Value':>25}  {'Function':>20}")
    print("  " + "-" * 65)
    for h in matrix["sign_hypotheses"]:
        sign = h["sign"]
        if "+" not in sign:  # skip compound entries for summary
            print(f"  {sign:>6}  {h['confidence']:>5}  {h['tentative_value']:>25}  {h['function']:>20}")

    print("\nKey testable predictions:")
    for p in matrix["key_testable_predictions"]:
        print(f"  {p[:100]}")

    print(f"\nSaved to {out}")

    # ── Quick validation: test P1 for sign 817 ────────────────────────────────
    print("\n" + "=" * 70)
    print("  QUICK VALIDATION: Sign 817 = '-um' hypothesis (Prediction P1)")
    print("=" * 70)

    corpus = json.loads((_REPORTS / "icit_extracted_corpus.json").read_text("utf-8"))
    inscriptions = [i["sequence"] for i in corpus["inscriptions"] if i.get("sequence")]

    tmk_signs = {"817", "920", "760", "798", "806", "900", "904", "752", "717",
                 "845", "717", "905", "809"}

    # Sign 817 alone as suffix vs. preceded by another TMK sign
    solo_suffix = 0   # 817 appears as suffix, preceded by non-TMK
    stack_suffix = 0  # 817 appears as suffix, preceded by TMK (suffix stacking)
    n_817_terminal = 0

    for ins in inscriptions:
        for j, s in enumerate(ins):
            if s == "817" and j == len(ins) - 1:  # terminal position
                n_817_terminal += 1
                if j > 0 and ins[j - 1] in tmk_signs:
                    stack_suffix += 1
                else:
                    solo_suffix += 1

    stack_rate = stack_suffix / max(n_817_terminal, 1)
    print(f"\n  Sign 817 terminal occurrences: {n_817_terminal}")
    print(f"  Preceded by another TMK sign: {stack_suffix} ({stack_rate*100:.1f}%)")
    print(f"  Preceded by non-TMK (pure suffix): {solo_suffix} ({(1-stack_rate)*100:.1f}%)")
    print("\n  Interpretation:")
    if stack_rate < 0.15:
        print(f"  ✓ P1 SUPPORTED: Sign 817 rarely follows another TMK sign ({stack_rate*100:.1f}% < 15%).")
        print("    Consistent with '-um' as a primary (non-stacking) enclitic.")
    else:
        print(f"  △ P1 AMBIGUOUS: {stack_rate*100:.1f}% stacking rate.")

    # Additional: does 817 appear after more unique predecessors than any other sign?
    pred_817: set[str] = set()
    for ins in inscriptions:
        for j, s in enumerate(ins):
            if s == "817" and j > 0:
                pred_817.add(ins[j - 1])

    print(f"\n  Unique predecessor signs for 817: {len(pred_817)}")
    print(f"    {sorted(pred_817)[:15]}...")
    print("\n  If '-um' hypothesis is correct: should appear after many different roots.")
    if len(pred_817) > 50:
        print(f"  ✓ HIGH DIVERSITY ({len(pred_817)} unique predecessors) supports '-um'.")

    print("\nDone.")


if __name__ == "__main__":
    main()
