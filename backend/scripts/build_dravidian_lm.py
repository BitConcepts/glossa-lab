"""
Build a clean Tamil-Brahmi bigram language model from dravidian.py.

Sources (all authors credited per CITATIONS.md):
  E.1: Burrow, T. & Emeneau, M.B. 1984. DEDR (Revised). Oxford: Clarendon.
  E.2: Krishnamurti, B. 2003. The Dravidian Languages. Cambridge: CUP.
  E.3: Sangam Tamil Literature, ~300 BCE-300 CE.
  C.1: Parpola, A. 1994. Deciphering the Indus Script. Cambridge: CUP.
  C.2: Parpola, A. 2010. A Dravidian Solution... World Classical Tamil Conference.
  E.6: Glossa Lab 2026 (derived corpus from above; dravidian.py).

Why dravidian.py and not the Mahadevan 2003 epub:
  The epub/djvu.txt OCR is contaminated with English commentary and Cyrillic artifacts.
  dravidian.py's get_corpus_inscriptions() provides 1,297 curated Old Tamil inscription
  sequences from the Sangam corpus and DEDR — these are clean syllabic sequences.

Output:
  backend/glossa_lab/data/dravidian_tamil_lm.json   -- cited Tamil bigram LM
  reports/dravidian_lm_build.json                    -- build stats
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.data.dravidian import (  # type: ignore[import]
    get_vocabulary,
    get_attested_words,
    get_corpus_inscriptions,
)

LM_OUT  = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
RPT_OUT = REPO / "reports/dravidian_lm_build.json"

# ── Tamil phoneme inventory ────────────────────────────────────────────────────
# Source: Krishnamurti 2003 (E.2) Table 1.1 Tamil consonant/vowel inventory
TAMIL_CONSONANTS = set("kctpnmyrlv") | {"ṭ", "ṇ", "ṉ", "ṟ", "ḷ", "ḻ", "ñ", "ṅ", "ś", "ṣ"}
TAMIL_VOWELS     = set("aāiīuūeēoō")
TAMIL_CHARS      = TAMIL_CONSONANTS | TAMIL_VOWELS


def syllabify_tamil(char_seq: list[str]) -> list[str]:
    """
    Convert a character-level Tamil sequence into CV syllables.

    Algorithm (simplified Krishnamurti 2003 syllabification):
    - Vowel-initial: V → standalone syllable
    - Consonant+Vowel: CV → single syllable
    - Consonant at end (no following vowel): coda, attach to previous or standalone

    Returns list of syllable strings.
    """
    syllables: list[str] = []
    i = 0
    while i < len(char_seq):
        ch = char_seq[i].lower() if char_seq[i] else ""
        if not ch or ch not in TAMIL_CHARS:
            i += 1
            continue
        if ch in TAMIL_VOWELS:
            # Standalone vowel syllable
            syllables.append(ch)
            i += 1
        elif ch in TAMIL_CONSONANTS:
            # Consume consonant + optional following vowel
            syl = ch
            if i + 1 < len(char_seq):
                nxt = char_seq[i + 1].lower() if char_seq[i + 1] else ""
                if nxt in TAMIL_VOWELS:
                    syl += nxt
                    i += 2
                    syllables.append(syl)
                    continue
            # Consonant with no following vowel → add short 'a' (implicit vowel in Tamil)
            syl += "a"
            syllables.append(syl)
            i += 1
        else:
            i += 1
    return syllables


def is_valid_tamil_syllable(tok: str) -> bool:
    """Basic Tamil syllable validity check."""
    if len(tok) < 1 or len(tok) > 8:
        return False
    if not tok[0].lower() in TAMIL_CHARS:
        return False
    # Reject if contains non-Tamil characters
    for ch in tok.lower():
        if ch not in TAMIL_CHARS and ch not in "-":
            return False
    return True


# ── Load sources ────────────────────────────────────────────────────────────────
print("Loading dravidian.py corpus (sources: DEDR, Parpola, Sangam) …")
vocab       = get_vocabulary()          # 1,740 Tamil word → gloss entries
attested    = get_attested_words()      # 2,155 attested Tamil forms
inscriptions = get_corpus_inscriptions()  # 1,297 Old Tamil inscription sequences

print(f"  Vocabulary entries:   {len(vocab)}")
print(f"  Attested word forms:  {len(attested)}")
print(f"  Inscription sequences: {len(inscriptions)}")

# ── Build syllable sequences from inscription corpus ──────────────────────────
print("\nSyllabifying inscription sequences …")
syllable_seqs: list[list[str]] = []
total_chars  = 0
total_sylls  = 0

for insc in inscriptions:
    if not isinstance(insc, list):
        continue
    total_chars += len(insc)
    seq = syllabify_tamil([str(c) for c in insc])
    seq = [s for s in seq if is_valid_tamil_syllable(s)]
    if len(seq) >= 2:
        syllable_seqs.append(seq)
        total_sylls += len(seq)

print(f"  Sequences with ≥2 syllables: {len(syllable_seqs)}")
print(f"  Total input characters: {total_chars}")
print(f"  Total syllables extracted: {total_sylls}")

# Also use attested word forms: treat each word as a 1-element sequence
# and extract bigrams from compound names (words with internal hyphens)
compound_seqs: list[list[str]] = []
for w in attested:
    if not isinstance(w, str):
        continue
    parts = w.lower().strip().split("-")
    parts = [p for p in parts if p and is_valid_tamil_syllable(p)]
    if len(parts) >= 2:
        compound_seqs.append(parts)

print(f"  Compound name sequences: {len(compound_seqs)}")
all_seqs = syllable_seqs + compound_seqs

# ── Build bigram counts ─────────────────────────────────────────────────────────
unigram: Counter = Counter()
bigram_counts: Counter = Counter()

for seq in all_seqs:
    for s in seq:
        unigram[s] += 1
    for i in range(len(seq) - 1):
        bigram_counts[(seq[i], seq[i + 1])] += 1

vocab_list = list(unigram.keys())
V          = len(vocab_list)
total_bi   = len(bigram_counts)

print(f"\nVocabulary: {V} distinct syllables/forms")
print(f"Bigrams:    {total_bi} distinct bigram types")
print(f"Top 15 bigrams: {bigram_counts.most_common(15)}")

# Verify: check top bigrams are Tamil (not English)
# NOTE: Single chars 'a', 'i', 'u' are valid Tamil vowel syllables, not English.
# Only check multi-character English function words.
ENGLISH_WORDS = {"the", "of", "and", "in", "to", "is", "for", "by",
                 "was", "on", "this", "that", "are", "be",
                 "cave", "line", "cm", "lower", "ledge", "racing",
                 "left", "tracing", "estampage", "plate", "fig"}
contamination = sum(
    1 for (a, b), _ in bigram_counts.most_common(15)
    if a in ENGLISH_WORDS or b in ENGLISH_WORDS
)
print(f"English contamination in top 15: {contamination}/15")
verdict = "CLEAN" if contamination == 0 else f"MINOR ({contamination}/15)"
print(f"LM verdict: {verdict}")

# ── Build log-probability LM ────────────────────────────────────────────────────
lm: dict[str, float] = {}
for (a, b), cnt in bigram_counts.items():
    prob     = (cnt + 1) / (unigram.get(a, 0) + V + 1)
    lm[f"{a}|{b}"] = round(math.log(prob), 6)

# ── Save ────────────────────────────────────────────────────────────────────────
lm_data = {
    "_citation": {
        "primary_sources": ["E.1", "E.2", "E.3", "C.1", "C.2", "E.6"],
        "derivation": (
            "Tamil bigram LM built from dravidian.py get_corpus_inscriptions() "
            "(1,297 Old Tamil Sangam inscription sequences) + get_attested_words() "
            "(compound name parsing). Syllabification: simplified Krishnamurti 2003 "
            "CV algorithm with implicit vowel insertion."
        ),
        "authors_credited": [
            "Burrow, Thomas & Emeneau, Murray Barnson (1984) — DEDR lexical base",
            "Krishnamurti, Bhadriraju (2003) — syllabification rules",
            "Sangam poets (~300 BCE–300 CE) — inscription corpus",
            "Parpola, Asko (1994, 2010) — phoneme assignments",
            "Glossa Lab contributors (2026) — dravidian.py compilation",
        ],
        "see_also": "CITATIONS.md sections E.1, E.2, E.3, C.1, C.2, E.6",
        "license": (
            "Derived from public domain + CC-licensed sources. "
            "DEDR: Oxford Clarendon (reference only). Sangam corpus: public domain. "
            "Parpola 2010: open conference paper."
        ),
        "caveat": (
            "This LM uses Classical Old Tamil forms (not Proto-Dravidian reconstructions). "
            "Label as 'Old Tamil LM (Sangam period, ~300 BCE–300 CE)' in publications. "
            "Syllabification is approximate (CV algorithm, not full morphological parse)."
        ),
    },
    "n_inscription_sequences": len(syllable_seqs),
    "n_compound_seqs":         len(compound_seqs),
    "total_syllables":         total_sylls,
    "vocab_size":              V,
    "n_bigrams":               total_bi,
    "english_contamination":   contamination,
    "verdict":                 verdict,
    "top_15_bigrams":          [(list(k), v) for k, v in bigram_counts.most_common(15)],
    "vocab":                   vocab_list,
    "unigrams":                {k: v for k, v in unigram.most_common()},
    "bigrams":                 lm,
}

LM_OUT.write_text(json.dumps(lm_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved: {LM_OUT.name}")

# ── Save build report ──────────────────────────────────────────────────────────
RPT_OUT.write_text(json.dumps({
    "title":                   "Dravidian Tamil LM build from dravidian.py",
    "timestamp":               __import__("datetime").datetime.now(
                                   __import__("datetime").timezone.utc).isoformat(),
    "sources":                 ["E.1 DEDR", "E.2 Krishnamurti 2003", "E.3 Sangam",
                                "C.1 Parpola 1994", "C.2 Parpola 2010"],
    "n_inscription_seqs":      len(syllable_seqs),
    "n_compound_seqs":         len(compound_seqs),
    "n_bigrams":               total_bi,
    "vocab_size":              V,
    "english_contamination":   contamination,
    "verdict":                 verdict,
    "top_15_bigrams":          [(list(k), v) for k, v in bigram_counts.most_common(15)],
    "citations": ["E.1", "E.2", "E.3", "C.1", "C.2", "E.6"],
}, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Report saved: {RPT_OUT.name}")
print(f"\nLM STATUS: {verdict} — {'ready for Phase-32 T4 SA experiment' if contamination == 0 else 'review top bigrams before use'}")
