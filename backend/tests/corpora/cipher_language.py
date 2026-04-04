"""Synthetic cipher language for decipherment testing.

Creates a toy language with KNOWN grammar and vocabulary, then
encrypts it with a random substitution cipher. The answer key
is preserved so tests can verify that our analysis tools recover
the correct linguistic structure.

Language design:
  - 15 consonants + 5 vowels = 20 phonemes
  - Words are CV or CVC syllables (1-2 syllables per word)
  - 3 noun cases: nominative (-a), accusative (-o), genitive (-u)
  - 2 verb tenses: present (ka-), past (ti-)
  - Word order: Subject-Object-Verb (SOV)
  - ~40 root words, ~500 inscriptions of 3-5 words

The cipher applies a random 1:1 substitution: each phoneme is
mapped to an arbitrary sign ID (S01..S20). The test must recover
the structure WITHOUT knowing the mapping.
"""

from __future__ import annotations

import random
from typing import Any

# ── Language definition ───────────────────────────────────────────

VOWELS = list("aeiou")
CONSONANTS = list("bdfghjklmnprstvz")  # 16 consonants
PHONEMES = VOWELS + CONSONANTS  # 21 total

# Case suffixes (nouns)
CASES = {"nom": "a", "acc": "o", "gen": "u"}

# Tense prefixes (verbs)
TENSES = {"pres": "ka", "past": "ti"}

# Root vocabulary: (root, part_of_speech)
ROOTS = [
    "bal",
    "kin",
    "mar",
    "sur",
    "den",
    "pol",
    "hir",
    "vam",
    "zel",
    "tuk",
    "fas",
    "gim",
    "nar",
    "bes",
    "dul",
    "rem",
    "fol",
    "kaz",
    "mil",
    "pun",
    "sil",
    "var",
    "hep",
    "zon",
    "bet",
    "gal",
    "lim",
    "rav",
    "dak",
    "jom",
]

NOUN_ROOTS = ROOTS[:20]
VERB_ROOTS = ROOTS[15:]


def _make_noun(root: str, case: str, rng: random.Random) -> str:
    """Generate an inflected noun: root + case suffix."""
    return root + CASES[case]


def _make_verb(root: str, tense: str, rng: random.Random) -> str:
    """Generate an inflected verb: tense prefix + root."""
    return TENSES[tense] + root


def generate_language_corpus(
    seed: int = 42,
    num_inscriptions: int = 500,
) -> dict[str, Any]:
    """Generate the plaintext corpus with known grammar.

    Returns:
        dict with:
          - inscriptions: list of inscriptions (lists of words)
          - flat_phonemes: flat list of all phonemes (characters)
          - vocabulary: all unique words
          - grammar: description of the grammar rules
    """
    rng = random.Random(seed)
    inscriptions = []
    tenses = list(TENSES.keys())

    for _ in range(num_inscriptions):
        # SOV: Subject(nom) Object(acc) Verb
        # Sometimes add genitive modifier: Subject Gen-noun Object Verb
        subj = _make_noun(rng.choice(NOUN_ROOTS), "nom", rng)
        obj = _make_noun(rng.choice(NOUN_ROOTS), "acc", rng)
        verb = _make_verb(rng.choice(VERB_ROOTS), rng.choice(tenses), rng)

        if rng.random() < 0.3:
            # Add genitive modifier
            gen = _make_noun(rng.choice(NOUN_ROOTS), "gen", rng)
            inscriptions.append([subj, gen, obj, verb])
        else:
            inscriptions.append([subj, obj, verb])

    flat_phonemes = []
    for insc in inscriptions:
        for word in insc:
            flat_phonemes.extend(list(word))

    return {
        "inscriptions": inscriptions,
        "flat_phonemes": flat_phonemes,
        "vocabulary": sorted(set(w for insc in inscriptions for w in insc)),
        "grammar": {
            "word_order": "SOV",
            "case_suffixes": CASES,
            "tense_prefixes": TENSES,
            "noun_roots": NOUN_ROOTS,
            "verb_roots": VERB_ROOTS,
        },
    }


def apply_cipher(
    corpus: dict[str, Any],
    seed: int = 99,
) -> dict[str, Any]:
    """Apply a random substitution cipher to the corpus.

    Each phoneme is mapped to a sign ID (S01..S20).
    Returns the ciphered corpus + the answer key.
    """
    rng = random.Random(seed)

    # Create random 1:1 mapping
    sign_ids = [f"S{i:02d}" for i in range(1, len(PHONEMES) + 1)]
    shuffled = list(sign_ids)
    rng.shuffle(shuffled)
    cipher_map = dict(zip(PHONEMES, shuffled))
    reverse_map = {v: k for k, v in cipher_map.items()}

    # Apply cipher to inscriptions
    ciphered_inscriptions = []
    for insc in corpus["inscriptions"]:
        ciphered_insc = []
        for word in insc:
            ciphered_word = "".join(cipher_map[ch] for ch in word)
            ciphered_insc.append(ciphered_word)
        ciphered_inscriptions.append(ciphered_insc)

    # Flat sign sequence (individual sign IDs, not concatenated words)
    flat_signs = []
    for insc in ciphered_inscriptions:
        for word in insc:
            # Split into sign IDs (every 3 chars = one sign)
            for i in range(0, len(word), 3):
                flat_signs.append(word[i : i + 3])

    return {
        "ciphered_inscriptions": ciphered_inscriptions,
        "flat_signs": flat_signs,
        "cipher_map": cipher_map,
        "reverse_map": reverse_map,
        "alphabet_size": len(sign_ids),
    }


def generate_cipher_test_data(
    seed: int = 42,
) -> dict[str, Any]:
    """Generate complete test data: plaintext + cipher + answer key."""
    corpus = generate_language_corpus(seed=seed)
    cipher = apply_cipher(corpus, seed=99)
    return {
        "plaintext": corpus,
        "cipher": cipher,
        "answer_key": {
            "cipher_map": cipher["cipher_map"],
            "reverse_map": cipher["reverse_map"],
            "grammar": corpus["grammar"],
        },
    }
