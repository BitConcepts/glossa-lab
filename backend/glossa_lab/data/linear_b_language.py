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

# ── Extended Pylos / Knossos vocabulary (Ventris-Chadwick 1973, Aura Jorro) ──────────
# Source: Aura Jorro, *Diccionario Micénico* (1985–1993), and the index of
# Ventris-Chadwick *Documents in Mycenaean Greek* (2nd ed. 1973). Tokens are
# spelled in CIPEM hyphenated transcription so they round-trip through the
# `get_corpus_symbols` tokenizer (each hyphen-separated piece becomes one
# syllabic-sign token).

# Occupations and craft titles (Pylos Pn / Eb / Jn series)
OCCUPATION_VOCAB: dict[str, str] = {
    "a-mo-te": "chariot-fitter (harmoster)",
    "a-pi-qo-i-ta": "cattle-herder",
    "a-ke-ro": "messenger (angelos)",
    "a-ke-ti-ri-ja": "decorator-women (askentriai)",
    "a-ra-ka-te-ja": "spinning-women (alakatesiai)",
    "a-ze-ti-ri-ja": "dyer-women",
    "da-mi-jo": "of the people (damios)",
    "e-pi-ko-wo": "watchmen (epikowoi)",
    "i-je-re-u": "priest (hiereus)",
    "ka-ke-u": "smith (khalkeus)",
    "ka-na-pe-u": "fuller (knapheus)",
    "ke-ra-me-u": "potter (kerameus)",
    "ke-ri-mi-ja": "gold-women (chrysoumiai)",
    "ko-ki-da": "shell-purple-dyer",
    "ku-pi-ri-jo": "Cypriot (kypriois)",
    "me-ri-da-ma-te": "honey-controllers",
    "mi-ka-ta": "mixer (miktas)",
    "o-pi-su-ko": "fig-overseer",
    "pa-ra-jo": "old / former",
    "po-me": "shepherd (poimen)",
    "ra-pi-ti-ra": "sewing-women (rhaptirai)",
    "ra-pte": "tailor (rhapter)",
    "to-ko-do-mo": "wall-builder (toikhodomos)",
    "to-ko-so-wo-ko": "bow-maker (toxoworgos)",
    "u-po-jo": "upholder / vassal",
    "wi-ri-ki-ni-jo": "of the workshop",
}

# Weapons, chariots, military gear (Knossos R, Sc, So series)
MILITARY_VOCAB: dict[str, str] = {
    "a-no-no": "reins",
    "e-ke-a": "spears (enkhea)",
    "i-qi-ja": "chariot-frame (hippiai)",
    "ka-ru-ke": "helmet (karyx)",
    "ki-to": "tunic / chiton",
    "ko-ru": "helmet (korys)",
    "o-pa": "workshop unit / order",
    "o-pi-ko-ru-si-ja": "helmet-fittings",
    "pa-we-a": "cloths / robes",
    "qe-ro": "target / shield (qerwos)",
    "qe-ro2": "shield (variant)",
    "ra-pi-ti-ra2": "sewers of harness",
    "ru-ka": "belt / strap",
    "to-ra-ke": "breastplate / corselet",
    "to-ko-so": "bow (toxon)",
    "wi-ri-no": "leather (rhinos)",
    "za-mi-jo": "penalty / fine (zamion)",
}

# Vessels, textiles, furniture (Pylos Tn, Ta series)
VESSEL_VOCAB: dict[str, str] = {
    "a-pi-qo-to": "two-handled (cup)",
    "di-pa": "cup / depas",
    "e-ko-me-no": "having handles",
    "ka-ko-de-ta": "bronze-bound",
    "ka-ra-re-we": "jars (klareus)",
    "ke-ra-ja-pi": "with horns (instr.)",
    "ki-ti-je-si": "in the household (loc.pl.)",
    "ku-wa-no": "blue-glass (kyanos)",
    "o-da-tu-we-ta": "toothed / dentated",
    "o-no-ke": "in the (foot)stool (dat.)",
    "pa-ka-na": "swords (phasgana)",
    "pa-sa-ro": "all (panta)",
    "po-ka": "fleece",
    "po-ni-ki-ja": "red / phoenician (poinikia)",
    "qe-to": "jar / pithos",
    "ra-e-ja": "linen (raeia)",
    "ri-no": "linen (linon)",
    "ta-ra-nu": "footstool (thranus)",
    "to-no": "throne (thronos)",
    "we-a2-no": "clothing",
    "wo-ko": "unguent / oil (worgon)",
}

# Place names (Pylos PY An / Knossos KN B series)
PLACE_NAME_VOCAB: dict[str, str] = {
    "a-ka-na": "Akhana (Pylian town)",
    "a-mi-ni-so": "Amnisos",
    "a-ka-wi-ja-de": "to Achaea (allative)",
    "a-pi-no-e-wi-jo": "Aphinoean (place adj.)",
    "a-pu-ne-we": "Apunew (locale)",
    "a-pu2-de": "to Aipy (allative)",
    "da-mi-ni-jo": "of Damnia",
    "e-na-po-ro": "Enaporo",
    "e-ra": "Hera-temple-region",
    "i-te-re-wa": "Iterewa (Pylian)",
    "ka-ra-do-ro": "Charadros",
    "ko-no-so": "Knossos",
    "ku-do-ni-ja": "Kydonia",
    "me-ta-pa": "Metapa",
    "mu-ti-ri-jo": "of Myrtilo",
    "o-ru-ma-to": "Olympus / Orumantos",
    "pa-ki-ja-na": "Pa-ki-ja-ne (Pylos sanctuary)",
    "pi-sa-wa": "Pisawa",
    "ra-su-to": "Lasynthos",
    "re-u-ko-to-ro": "Leuktron",
    "ro-u-so": "Lousoi",
    "sa-ma-ri-jo": "Samarion",
    "se-do": "Sedô (settlement)",
    "so-ja": "Soja (Knossian)",
    "ti-mi-to-a-ke-i": "in the temple (loc.)",
    "u-pa-ra-ki-ri-ja": "of the highland",
    "we-da-ne-u": "Wedaneu (PN/place)",
}

# Personal names (high-frequency, Pylos roster)
PERSONAL_NAME_VOCAB: dict[str, str] = {
    "a-ke-u": "Akhaeus (PN)",
    "a-ki-ja": "Akhya (PN)",
    "a-pi-mi-jo": "Aphimios (PN)",
    "da-i-pi-ta": "Daiphita (PN)",
    "di-ko-na": "Dikona (PN)",
    "e-ke-ra-wo": "Ekheraon (PN)",
    "e-ke-da-mo": "Ekhedamos (PN)",
    "e-u-me-de": "Eumedes (PN)",
    "ka-ko-de-ta-ra": "Khalkodontas (PN)",
    "ka-pa": "Karpa (PN)",
    "ku-ru-me-no": "Klymenos (PN)",
    "ne-da-wa-ta": "Nedwatas (PN)",
    "o-pe-re-ta": "Opheltas (PN)",
    "pa-ko": "Pakos (PN)",
    "pi-ra-ka-ra": "Philagra (PN)",
    "po-ki-ro": "Poikilos (PN)",
    "ra-pa-sa-ko": "Rapsakos (PN)",
    "ru-ko": "Lykos (PN)",
    "si-mi": "Simi (PN)",
    "te-se-u": "Theseus (PN)",
    "te-tu-ro": "Teturos (PN)",
    "ti-ri-jo": "Trios (PN)",
    "u-ru-pi-ja-jo": "Olympia-man (PN)",
    "we-we-si-jo": "Wewesios (PN)",
    "wi-pi-no-o": "Wiphinoos (PN)",
    "za-ku-si-jo": "Zakynthian (PN)",
}

# Numbers / measurements / quantities
QUANTITY_VOCAB: dict[str, str] = {
    "e-ne-ka": "because (heneka)",
    "e-pi-de-da-to": "distributed",
    "e-ra-pe-me-na": "sewn together",
    "e-re-pa": "ivory (elephas)",
    "e-ru-ta-ra": "red (eruthra)",
    "ke-ka-u-me-no": "burnt / kiln-dried",
    "ko-wo": "young man (koros)",
    "ko-wa": "young woman (kore)",
    "me-zo-e": "more / greater (meizos)",
    "o-u-di-do-si": "they do not give",
    "o-u-qe": "and not (oude)",
    "pa-si-te-o-i": "to all the gods",
    "pe-ru-si-nu-wo": "of last year",
    "po-ro": "first (proton)",
    "qe-te-jo": "that must be paid",
    "qe-te-o": "to be paid (gerund)",
    "re-ke-to-ro-te-ri-jo": "festival of bed-spreading",
    "si-a2-ro": "hog / boar (sialos)",
    "to-pe-za": "table (trapeza)",
    "u-de-wi-ne": "watery / aquatic",
    "wo-no": "wine (oinos)",
    "za-we-te": "this year (zawetes)",
}

# Complete vocabulary merged
VOCABULARY: dict[str, str] = {
    **ADMIN_VOCAB,
    **DIVINE_VOCAB,
    **COMMODITY_VOCAB,
    **OCCUPATION_VOCAB,
    **MILITARY_VOCAB,
    **VESSEL_VOCAB,
    **PLACE_NAME_VOCAB,
    **PERSONAL_NAME_VOCAB,
    **QUANTITY_VOCAB,
}


def get_attested_words() -> list[str]:
    """Return the sorted list of attested Mycenaean Greek words (full forms).

    Each entry is the original CIPEM hyphenated transcription (e.g. ``wa-na-ka``).
    Used by `AttestedVocabularyLoader(family='linear_b')` for HoldoutWordRecall
    and CompoundDependencyConstraint scoring against word-level mappings.
    """
    return sorted(VOCABULARY.keys())


def get_attested_word_tokens() -> list[str]:
    """Return the deduplicated set of *syllabic tokens* attested across the
    expanded Mycenaean Greek vocabulary.

    Each hyphen-separated piece (e.g. ``wa``, ``na``, ``ka`` from ``wa-na-ka``)
    becomes one syllabic-sign token. Useful for sign-level decipherment
    inventories (``CipherConstructor`` / role-mapping diagnostics).
    """
    tokens: set[str] = set()
    for word in VOCABULARY.keys():
        for piece in word.replace("3", "").split("-"):
            cleaned = piece.strip().lower()
            if cleaned and cleaned.replace("*", "").replace("2", "").isalpha():
                tokens.add(cleaned)
    return sorted(tokens)


def get_corpus_inscriptions() -> list[list[str]]:
    """Return representative Linear B "inscriptions" (lemma sequences).

    Each list is one synthetic clause that strings together attested forms
    in plausible Mycenaean phrase order, suitable for bigram LM seeding and
    `CompoundDependencyConstraint` scoring.
    """
    return [
        ["wa-na-ka", "e-qe-ta", "do-ra", "pa-si-te-o-i"],
        ["ra-wa-ke-ta", "i-je-re-u", "ke-ra-me-u", "ka-ke-u"],
        ["po-me", "o-wi-de", "ko-no-so", "a-mi-ni-so"],
        ["da-mo", "ko-to-na", "ke-ke-me-na", "ki-ti-me-na"],
        ["e-ke-ra-wo", "o-pa", "i-qi-ja", "to-ko-so"],
        ["po-ti-ni-ja", "do-ra", "po-re-na-qe", "a-ke"],
        ["di-wi-jo", "di-u-ja", "a-ta-na", "po-se-da-o"],
        ["ko-re-te", "a-pu-do-si", "ta-ra-si-ja", "ka-ko"],
        ["po-me", "a-ko-ro", "e-pi", "pa-ro"],
        ["wa-na-ka", "i-je-re-u", "e-ke-ra-wo", "do-ra"],
        ["ra-pte", "pa-we-a", "ri-no", "po-ka"],
        ["ka-ke-u", "ka-ko", "to-ra-ke", "ka-ru-ke"],
        ["e-pi-ko-wo", "ka-ra-do-ro", "e-ra", "me-ta-pa"],
        ["u-ru-pi-ja-jo", "ne-da-wa-ta", "ku-ru-me-no", "ru-ko"],
        ["po-ti-ni-ja", "a-ta-na", "e-ra", "di-wi-jo"],
        ["qe-to", "di-pa", "to-no", "ta-ra-nu"],
        ["a-pi-qo-to", "ku-wa-no", "po-ni-ki-ja", "e-re-pa"],
        ["a-pi-mi-jo", "e-u-me-de", "ka-pa", "ti-ri-jo"],
        ["to-ko-so-wo-ko", "to-ko-so", "e-ke-a", "o-pi-ko-ru-si-ja"],
        ["ko-no-so", "ku-do-ni-ja", "ko-wa", "ko-wo"],
        ["po-me", "si-a2-ro", "o-wi-de", "i-qo-qe"],
        ["o-da-tu-we-ta", "qe-ro", "to-ra-ke", "za-mi-jo"],
        ["a-ke-ti-ri-ja", "a-ra-ka-te-ja", "a-ze-ti-ri-ja", "ra-pi-ti-ra"],
        ["o-u-di-do-si", "o-u-qe", "qe-te-jo", "qe-te-o"],
        ["po-ro", "za-we-te", "pe-ru-si-nu-wo", "e-ne-ka"],
    ]

# ── Answer key: opaque ID → true phonetic value ─────────────────────────


def build_answer_key(opaque_sequence: list[str]) -> dict[str, str]:
    """Build an answer key mapping opaque sign IDs to true syllable values.

    Used for validation: after the decipherment engine proposes a mapping,
    we compare it against this key.

    The opaque IDs are in the form 'LB_01', 'LB_02', etc., assigned in
    the order the syllables appear in the corpus (most frequent first).
    """
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
