"""Mycenaean Greek language data for Linear B studies.

Provides the syllable inventory, vocabulary, and corpus symbols
used to build language models for:
  1. Linear B decipherment validation (comparing engine output against
     known Ventris values)
  2. Linear A hypothesis testing (testing whether Mycenaean Greek
     phonetic values applied to Linear A signs produce recognisable Greek)

Sign values follow the CIPEM conventions established in Ventris & Chadwick
(1973) Documents in Mycenaean Greek (2nd ed.).

Reference corpus: Pylos tablets (PY series, c. 1200 BCE) and
Knossos tablets (KN series, c. 1375 BCE).
"""

from __future__ import annotations

from pathlib import Path

# ── Syllable inventory (87 signs with known values) ──────────────────

# Core CV syllables organized by row (same vowel = same row)
SYLLABARY: list[str] = [
    # Vowels
    "a",
    "e",
    "i",
    "o",
    "u",
    # d-row
    "da",
    "de",
    "di",
    "do",
    "du",
    # j-row
    "ja",
    "je",
    "jo",
    # k-row (including labiovelar)
    "ka",
    "ke",
    "ki",
    "ko",
    "ku",
    "qa",
    "qe",
    "qi",
    "qo",
    # m-row
    "ma",
    "me",
    "mi",
    "mo",
    "mu",
    # n-row
    "na",
    "ne",
    "ni",
    "no",
    "nu",
    # p-row
    "pa",
    "pe",
    "pi",
    "po",
    "pu",
    # r-row
    "ra",
    "re",
    "ri",
    "ro",
    "ru",
    # s-row
    "sa",
    "se",
    "si",
    "so",
    "su",
    # t-row
    "ta",
    "te",
    "ti",
    "to",
    "tu",
    # w-row
    "wa",
    "we",
    "wi",
    "wo",
    # z-row
    "za",
    "ze",
    "zo",
    # Special signs
    "nwa",
    "pte",
    "dwo",
    "dwe",
    "two",
    "twe",
    # Rare signs
    "rai",
    "rja",
    "rjo",
    # a2 / a3 variants
    "a2",
    "a3",
    "ra2",
    "ra3",
    "ta2",
]

# ── Vocabulary (Mycenaean Greek word forms) ───────────────────────────

# Administration and social terms
ADMIN_VOCAB: dict[str, str] = {
    "wa-na-ka": "king (wanax)",
    "ra-wa-ke-ta": "leader of the host (lawagetas)",
    "te-re-ta": "obligation-holders (telestai)",
    "e-qe-ta": "followers, companions (hekwetai)",
    "ko-re-te": "mayor/official (koreter)",
    "da-mo": "people, community (damos)",
    "do-e-ro": "slave, servant (doelos)",
    "do-e-ra": "female slave (doelra)",
    "ko-to-na": "plot of land (khtoina)",
    "ke-ke-me-na": "communal (gegeimena)",
    "ki-ti-me-na": "individual (ktimena)",
    "a-ko-ro": "field (agros)",
    "ka-ma": "land parcel (kama)",
    "o-na-to": "lease, usufruct (onaston)",
    "e-to-ni-jo": "without payment (etonion)",
    "a-pu-do-si": "delivery, payment (apudosis)",
    "ta-ra-si-ja": "allocations, bronze rations (talasia)",
    "pa-ro": "from, beside (para)",
    "e-pi": "on, for (epi)",
    "to-so": "so much, this many (toson)",
    "to-so-de": "and so many (tosonde)",
}

# Religious and divine terms
DIVINE_VOCAB: dict[str, str] = {
    "po-ti-ni-ja": "mistress, lady (Potnia)",
    "di-wi-jo": "of Zeus (Diwios)",
    "di-u-ja": "of Zeus (Diuia)",
    "te-o-jo": "of the god (theojo)",
    "do-ra": "gifts (dora)",
    "po-re-na-qe": "and offerings (porena-que)",
    "a-ke": "lead, bring (agein)",
    "pe-re": "carry, bring (pherein)",
    "i-je-re-ja": "priestess (hiereia)",
    "e-ri-ta": "priestess (name: Erita)",
    "a-ta-na": "Athena",
    "a-re-i": "of Ares (Arewi)",
    "po-se-da-o": "Poseidon (Poseidaon)",
}

# Livestock and commodities
COMMODITY_VOCAB: dict[str, str] = {
    "o-wi-de": "sheep (owis, plural)",
    "ka-ko": "bronze, copper (khalkos)",
    "o-li-wa": "olive oil (elaiwa)",
    "e-ra-wo": "olive (elaion)",
    "ka-po": "fruit (karpos)",
    "me-ri-to": "of honey (melitos)",
    "pe-ma": "seed, sowing (sperma)",
    "a-re-pa": "ointment (aleiphar)",
    "a-ni-ja": "reins, bridle (hania)",
    "i-qo-qe": "and horse(s) (hippos-que)",
    "wi-ri-ne-jo": "of leather (rhineos)",
}

# Complete vocabulary merged
VOCABULARY: dict[str, str] = {
    **ADMIN_VOCAB,
    **DIVINE_VOCAB,
    **COMMODITY_VOCAB,
}

# ── Answer key: opaque ID → true phonetic value ──────────────────────


def build_answer_key(opaque_sequence: list[str]) -> dict[str, str]:
    """Build an answer key mapping opaque sign IDs to true syllable values.

    Used for validation: after the decipherment engine proposes a mapping,
    we compare it against this key.

    The opaque IDs are in the form 'LB_01', 'LB_02', etc., assigned in
    the order the syllables appear in the corpus (most frequent first).
    """
    from collections import Counter

    counts = Counter(opaque_sequence)
    # Map by frequency rank — LB_01 = most frequent sign
    # Reverse-lookup: opaque_id → true_syllable
    # This is built when the corpus is encoded
    return {}  # populated by encode_corpus()


def encode_corpus(signs: list[str]) -> tuple[list[str], dict[str, str]]:
    """Encode a syllable sequence with opaque sign IDs.

    Returns:
        (opaque_sequence, answer_key)
        where answer_key maps opaque_id → true_syllable
    """
    from collections import Counter

    # Sort by frequency (most common gets lowest ID number)
    counts = Counter(signs)
    ranked = [s for s, _ in counts.most_common()]
    mapping = {syl: f"LB{str(i + 1).zfill(2)}" for i, syl in enumerate(ranked)}
    answer_key = {v: k for k, v in mapping.items()}
    opaque = [mapping[s] for s in signs]
    return opaque, answer_key


# ── Corpus symbols ────────────────────────────────────────────────────


def get_corpus_symbols() -> list[str]:
    """Load the Linear B fixture and return syllable-level tokens."""
    fixture = (
        Path(__file__).resolve().parent.parent.parent
        / "tests"
        / "corpora"
        / "fixtures"
        / "linear_b.txt"
    )
    text = fixture.read_text(encoding="utf-8")
    tokens: list[str] = []
    for line in text.splitlines():
        for word in line.strip().split():
            # Each word is hyphen-separated syllables: wa-na-ka → [wa, na, ka]
            parts = word.replace("3", "").split("-")
            for p in parts:
                cleaned = p.strip()
                if cleaned and cleaned.replace("*", "").replace("2", "").isalpha():
                    tokens.append(cleaned.lower())
    return tokens


def get_vocabulary() -> dict[str, str]:
    """Return the Mycenaean Greek vocabulary for hypothesis scoring."""
    return VOCABULARY
