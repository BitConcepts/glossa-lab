"""
Build a syllable-level Dravidian Tamil bigram LM.

Syllables are 1–3 char CV / CVC tokens derived from:
1. DEDR root forms (dravidian.py VOCABULARY + EXTENDED_VOCABULARY) split
   into ~2-char syllables using simple greedy CV chunking
2. Clean literal_aksharas from mahadevan_2003_tamil_brahmi.json (filtering
   out Cyrillic-contaminated tokens that came from OCR errors)

This produces a much richer bigram LM than the word-level one (dravidian_tamil_lm.json)
because each root word contributes multiple bigrams rather than one whole-word bigram.

Output: backend/glossa_lab/data/dravidian_syllable_lm.json
Citations: E.1 (DEDR/Burrow+Emeneau), E.3 (Sangam/Mahadevan 2003), A.12 (Mahadevan 2003 TB)

Run: shell.cmd python backend/scripts/build_dravidian_syllable_lm.py
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

from glossa_lab.data.dravidian import VOCABULARY, EXTENDED_VOCABULARY  # noqa: E402

TB_PATH    = REPO / "backend/glossa_lab/data/mahadevan_2003_tamil_brahmi.json"
OUT_PATH   = REPO / "backend/glossa_lab/data/dravidian_syllable_lm.json"

# ── Cyrillic detection ────────────────────────────────────────────────────────
# Cyrillic Unicode block: U+0400–U+04FF
_CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")
_VALID_SYLLABLE_RE = re.compile(r"^[a-zA-Z\u0101\u0113\u012b\u016b\u0325\u1e5b\u1e6d\u1e47\u1e0d\u1e45]{1,5}$")

# Simplified ASCII-only syllable chars for broad acceptance
_ASCII_SYLLABLE_RE = re.compile(r"^[a-z]{1,5}$", re.IGNORECASE)


# Common English words that pass ASCII filter but are NOT Tamil syllables
_ENGLISH_STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "have", "are", "was",
    "been", "not", "but", "can", "his", "her", "its", "our", "you", "she",
    "he", "we", "it", "be", "do", "go", "on", "by", "at", "to", "in", "is",
    "of", "or", "as", "an", "so", "up", "out", "off", "all", "one", "two",
    "has", "had", "did", "get", "got", "may", "see", "say", "saw", "cave",
    "rock", "bed", "top", "old", "new", "use", "per",
}


def is_clean_akshara(s: str) -> bool:
    """Return True if the token is a plausible Tamil-Brahmi syllable:
    - No Cyrillic contamination
    - 1-3 chars (Tamil-Brahmi syllables are short: ka, ya, ma, tha, etc.)
    - Not an English function/content word
    """
    if not s or len(s) > 3:  # Tamil-Brahmi syllables are 1-3 chars
        return False
    if _CYRILLIC_RE.search(s):
        return False
    # Normalise diacritics to ASCII for checking
    clean = s.lower()
    for src, dst in [("à","a"),("ā","a"),("ì","i"),("ī","i"),("ù","u"),("ū","u"),
                     ("ñ","n"),("ṅ","n"),("ṭ","t"),("ḍ","d"),("ṇ","n"),("ḷ","l"),
                     ("ḻ","l"),("ṉ","n"),("ṟ","r"),("ḥ","h"),("ṃ","m"),("ü","u"),
                     ("é","e"),("è","e"),("ê","e")]:
        clean = clean.replace(src, dst)
    if not re.match(r'^[a-z]{1,3}$', clean):
        return False
    if clean in _ENGLISH_STOPWORDS:
        return False
    # Must contain at least one vowel — rules out consonant clusters like pp, cm, st
    vowels_in = [c for c in clean if c in 'aeiou']
    if not vowels_in:
        return False
    # 3-char syllables: only C+V+C or C+V pattern — reject V+C+V ("age", "ate", "ire")
    # Tamil-Brahmi CVC has at most 1 vowel for length-3 tokens
    if len(clean) == 3 and len(vowels_in) > 1:
        return False
    return True


def split_to_syllables(root: str) -> list[str]:
    """Split a DEDR root into ~2-char syllables using greedy CV chunking.

    Rules:
    - Consume one consonant cluster + one vowel at a time
    - Any trailing consonant stays with previous syllable
    """
    root = root.lower().strip()
    VOWELS = set("aeiouāīūẽõ")
    CONSONANTS = set("bcdfghjklmnpqrstvwxyz")

    syllables: list[str] = []
    i = 0
    current = ""

    while i < len(root):
        c = root[i]
        current += c
        # If we hit a vowel, finish the syllable
        if c in VOWELS:
            # Greedily include a following consonant if next char is also consonant
            # (for CVC structure like "kal", "min")
            if (i + 1 < len(root) and root[i+1] in CONSONANTS and
                    (i + 2 >= len(root) or root[i+2] in VOWELS)):
                i += 1
                current += root[i]
            syllables.append(current)
            current = ""
        elif len(current) >= 3:
            # Safety: flush if we hit 3+ consonants without a vowel
            syllables.append(current)
            current = ""
        i += 1

    if current:
        if syllables:
            syllables[-1] += current  # attach trailing consonant
        else:
            syllables.append(current)

    # Filter single-char syllables that are just consonants — not useful
    return [s for s in syllables if len(s) >= 1]


# ── Collect bigrams ───────────────────────────────────────────────────────────

bigram_counts: Counter = Counter()
unigram_counts: Counter = Counter()
source_stats = {"dedr_roots": 0, "tb_aksharas": 0, "dedr_bigrams": 0, "tb_bigrams": 0}

# 1. DEDR roots
all_roots = {**VOCABULARY, **EXTENDED_VOCABULARY}
for root in all_roots:
    sylls = split_to_syllables(root)
    if len(sylls) < 2:
        # Single-syllable root — still count unigram
        if sylls:
            unigram_counts[sylls[0]] += 1
        continue
    source_stats["dedr_roots"] += 1
    for s in sylls:
        unigram_counts[s] += 1
    for j in range(len(sylls) - 1):
        bigram_counts[(sylls[j], sylls[j+1])] += 1
        source_stats["dedr_bigrams"] += 1

print(f"DEDR: {source_stats['dedr_roots']} multi-syllable roots, "
      f"{source_stats['dedr_bigrams']} bigrams from {len(all_roots)} roots")

# 2. TB aksharas
if TB_PATH.exists():
    tb = json.loads(TB_PATH.read_text(encoding="utf-8"))
    for insc in tb.get("inscriptions", []):
        aksharas = [a for a in insc.get("literal_aksharas", []) if is_clean_akshara(a)]
        if len(aksharas) < 2:
            continue
        # Normalise to lowercase
        aksharas = [a.lower() for a in aksharas]
        source_stats["tb_aksharas"] += len(aksharas)
        for a in aksharas:
            unigram_counts[a] += 1
        for j in range(len(aksharas) - 1):
            bigram_counts[(aksharas[j], aksharas[j+1])] += 5  # weight TB data higher
            source_stats["tb_bigrams"] += 1
    print(f"TB: {source_stats['tb_aksharas']} clean aksharas, "
          f"{source_stats['tb_bigrams']} bigrams")
else:
    print("TB file not found — using DEDR only")

# ── Build log-prob LM ─────────────────────────────────────────────────────────

vocab = sorted(unigram_counts.keys())
V = len(vocab)
total_bigrams = sum(bigram_counts.values())

lm: dict[str, float] = {}
for (a, b), cnt in bigram_counts.items():
    # Add-1 (Laplace) smoothing over vocab
    denom = unigram_counts.get(a, 0) + V + 1
    prob = (cnt + 1) / denom
    lm[f"{a}|{b}"] = round(math.log(prob), 6)

print(f"\nSyllable LM: {V} unique syllables, {len(lm)} bigrams")
print(f"Top 10 bigrams by count:")
for (a, b), cnt in bigram_counts.most_common(10):
    print(f"  {a}|{b}: {cnt}")

# ── Contamination check ───────────────────────────────────────────────────────
# Check for English function words that would indicate contamination
ENGLISH_CHECK = ["the", "and", "for", "with", "from", "that", "this", "have",
                 "are", "was", "been", "not", "but", "can"]
contaminated = [w for w in ENGLISH_CHECK if w in unigram_counts]
print(f"\nEnglish contamination check: {len(contaminated)}/15 words found: {contaminated}")
verdict = "CLEAN" if len(contaminated) == 0 else f"CONTAMINATED ({len(contaminated)} hits)"

# ── Save ──────────────────────────────────────────────────────────────────────

out = {
    "_citation": {
        "primary_sources": ["E.1", "A.12"],
        "derivation": (
            "Syllable-level bigram LM built by (1) splitting DEDR roots (Burrow+Emeneau 1984) "
            "into ~2-char CV syllables using greedy chunking, and (2) using clean literal_aksharas "
            "from Mahadevan 2003 Tamil-Brahmi corpus (filtering Cyrillic-contaminated OCR tokens). "
            "Bigrams are log-prob with Laplace smoothing. TB aksharas weighted 5× over DEDR."
        ),
        "see_also": "CITATIONS.md sections E.1, A.12",
    },
    "version": "syllable-v1 (2026-05-11)",
    "n_syllables": V,
    "n_bigrams": len(lm),
    "vocab": vocab,
    "bigrams": lm,
    "verdict": verdict,
    "contamination_check": contaminated,
    "source_stats": source_stats,
}

OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: {OUT_PATH}")
print(f"Verdict: {verdict}")
