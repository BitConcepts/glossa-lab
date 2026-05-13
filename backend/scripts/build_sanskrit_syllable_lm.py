"""Build a syllable-level Sanskrit bigram LM for Phase-32 T7 redo.

Creates a Sanskrit LM at the same granularity as dravidian_syllable_lm.json
(CV syllable tokens, 2-3 chars) so that T7 (Sanskrit falsification) can be
compared fairly against T4 (Dravidian) at the same token level.

Sources:
  1. VOCABULARY from backend/glossa_lab/data/sanskrit.py (~150 words)
  2. RIGVEDA_TEXT embedded in sanskrit.py (sample Vedic hymns)

Output: backend/glossa_lab/data/sanskrit_syllable_lm.json
Citations: Sanskrit Vedic sources (Monier-Williams, Rigveda)
"""
from __future__ import annotations
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "backend"))

OUT_PATH = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"

from glossa_lab.data.sanskrit import VOCABULARY, RIGVEDA_TEXT  # noqa: E402


# ── Sanskrit CV syllable splitter ─────────────────────────────────────────────
# Sanskrit syllable structure: (C*)V(C) where C is a consonant, V is a vowel
# We use the same greedy CV chunking as the Dravidian splitter.

VOWELS = set("aeiouāīū")
CONSONANTS = set("bcdfghjklmnpqrstvwxyzñśṣṭḍṇṝṃḥ")


def split_to_syllables(word: str) -> list[str]:
    """Split a Sanskrit word into CV syllables using greedy chunking."""
    word = word.lower().strip()
    # Normalize long vowels and aspirates to basic forms for LM building
    word = word.replace("ā", "a").replace("ī", "i").replace("ū", "u")
    word = word.replace("ṭ", "t").replace("ḍ", "d").replace("ṇ", "n")
    word = word.replace("ś", "s").replace("ṣ", "s").replace("ñ", "n")
    word = word.replace("ṝ", "r").replace("ṃ", "m").replace("ḥ", "h")
    # Remove non-alpha
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return []

    syllables: list[str] = []
    i = 0
    current = ""

    while i < len(word):
        c = word[i]
        current += c
        if c in VOWELS:
            # Include a following consonant if it's CVC-pattern
            if (i + 1 < len(word) and word[i + 1] in CONSONANTS and
                    (i + 2 >= len(word) or word[i + 2] in VOWELS)):
                i += 1
                current += word[i]
            syllables.append(current)
            current = ""
        elif len(current) >= 3:
            syllables.append(current)
            current = ""
        i += 1

    if current:
        if syllables:
            syllables[-1] += current
        else:
            syllables.append(current)

    return [s for s in syllables if len(s) >= 1 and any(c in VOWELS for c in s)]


def tokenize_rigveda(text: str) -> list[list[str]]:
    """Convert Rigveda text to syllable sequences (list of words, each a list of syllables)."""
    sequences = []
    words = text.lower().split()
    for word in words:
        # Clean word
        word = re.sub(r"[^a-z]", "", word)
        if not word:
            continue
        sylls = split_to_syllables(word)
        if len(sylls) >= 2:
            sequences.append(sylls)
        elif len(sylls) == 1 and len(sylls[0]) >= 2:
            sequences.append(sylls)
    return sequences


# ── Collect bigrams ───────────────────────────────────────────────────────────

bigram_counts: Counter = Counter()
unigram_counts: Counter = Counter()

# 1. Sanskrit vocabulary words
for word in VOCABULARY.keys():
    sylls = split_to_syllables(word)
    if not sylls:
        continue
    for s in sylls:
        unigram_counts[s] += 1
    for j in range(len(sylls) - 1):
        bigram_counts[(sylls[j], sylls[j + 1])] += 2  # weight vocabulary

print(f"Vocabulary: {len(VOCABULARY)} words processed")

# 2. Rigveda text
rigveda_sequences = tokenize_rigveda(RIGVEDA_TEXT)
for seq in rigveda_sequences:
    for s in seq:
        unigram_counts[s] += 1
    for j in range(len(seq) - 1):
        bigram_counts[(seq[j], seq[j + 1])] += 1

print(f"Rigveda: {len(rigveda_sequences)} syllable sequences")
print(f"Total bigrams: {sum(bigram_counts.values())}")

# ── Build log-prob LM ─────────────────────────────────────────────────────────

vocab = sorted(unigram_counts.keys())
V = len(vocab)

lm: dict[str, float] = {}
for (a, b), cnt in bigram_counts.items():
    denom = unigram_counts.get(a, 0) + V + 1
    prob = (cnt + 1) / denom
    lm[f"{a}|{b}"] = round(math.log(prob), 6)

print(f"\nSanskrit Syllable LM: {V} unique syllables, {len(lm)} bigrams")

print("Top 10 bigrams by count:")
for (a, b), cnt in bigram_counts.most_common(10):
    print(f"  {a}|{b}: {cnt}")

print("\nSample syllables:", sorted(vocab)[:20])

# ── Save ──────────────────────────────────────────────────────────────────────

output = {
    "_citation": {
        "primary_sources": ["Sanskrit vocabulary", "Rigveda ITRANS text"],
        "derivation": (
            "Sanskrit syllable-level bigram LM at the same granularity as "
            "dravidian_syllable_lm.json (CV tokens, 2-3 chars). "
            "Built from Monier-Williams Sanskrit vocabulary (~150 Vedic roots) + "
            "embedded Rigveda text sample (hymns). Bigrams counted within words; "
            "Laplace smoothed. Used for Phase-32 T7 redo (Sanskrit falsification "
            "at proper syllable level, not character level)."
        ),
        "see_also": "CITATIONS.md, Rigveda ITRANS e-texts (Sanskritdocuments.org)",
    },
    "version": "sanskrit-syllable-v1 (2026-05-13)",
    "n_syllables": V,
    "n_bigrams": len(lm),
    "vocab": vocab,
    "bigrams": lm,
}

OUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved to {OUT_PATH}")
