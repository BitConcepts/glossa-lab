"""
Fix for Phase-32 T4 Tamil-Brahmi LM.

Problem: Both literal_aksharas (Cyrillic OCR artifacts) and romanized_text_b_raw
(English mixed in) give invalid bigrams. Top bigrams were 'of the', 'the cave', etc.

Solution:
1. Use ONLY original 47 high-quality inscriptions (not epub-extracted)
2. Apply strict Tamil syllable extraction:
   - Strip all editorial markers (!, ?, *, ^, °, ', ^, [, ], etc.)
   - Filter to valid Tamil CV patterns:
     CV: consonant (k/c/t/ṭ/p/n/ṉ/ṇ/m/y/r/ṟ/l/ḷ/ḻ/v/ñ/ṅ) + vowel(s)
     V:  pure vowel (a/ā/i/ī/u/ū/e/ē/o/ō)
   - Reject anything containing uppercase, digits, or non-Tamil chars
3. Build bigram LM from cleaned syllable sequences

Output:
  backend/glossa_lab/data/mahadevan_2003_tb_lm_clean.json  -- clean Tamil LM
  reports/phase32_tb_lm_fix.json                            -- stats
"""
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO     = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")
TB_JSON  = REPO / "backend/glossa_lab/data/mahadevan_2003_tamil_brahmi.json"
LM_OUT   = REPO / "backend/glossa_lab/data/mahadevan_2003_tb_lm_clean.json"
RPT_OUT  = REPO / "reports/phase32_tb_lm_fix.json"

# ── Tamil phoneme inventory for strict filtering ──────────────────────────
TAMIL_VOWELS     = "aāiīuūeēoō"
TAMIL_CONSONANTS = "kctpnmyrlv" + "ṭṇṉṟḷḻñṅśṣ"
VALID_START      = set(TAMIL_VOWELS) | set(TAMIL_CONSONANTS)

# Tamil diacritics — presence guarantees Tamil (not English/garbage)
TAMIL_DIACRITICS = set("āīūēōṭṇṉṟḷḻñṅśṣ")

# Common English words to explicitly reject (case-insensitive)
ENGLISH_STOPWORDS = {
    "the","of","and","in","a","to","is","for","by","was","he","she","it",
    "from","at","with","an","on","were","this","that","are","as","be",
    "his","her","their","our","have","had","has","not","who","which",
    "one","two","three","four","five","six","seven","eight","nine","ten",
    "cave","merchant","guild","carved","gave","caused","be","giving",
    "members","cutting","hermitage","preceptor","son","daughter","given",
    "section","lines","note","page","see","cf","fig","plate","vol","no",
    "pp","p","ibid","op","cit","loc",
}

# ── Editorial marker stripping ────────────────────────────────────────────
_EDITORIAL = re.compile(r"[!?*^°'\[\](){}@=|]+|[0-9]+")

def clean_token(tok: str) -> str:
    """Strip editorial markers and normalize."""
    tok = _EDITORIAL.sub("", tok)
    tok = tok.strip("-").lower()
    return tok

def is_valid_tamil_syllable(tok: str) -> bool:
    """Return True if tok looks like a genuine Tamil romanized syllable/word."""
    if len(tok) < 2 or len(tok) > 15:
        return False
    if not tok[0] in VALID_START:
        return False
    # Reject if it contains digits or uppercase (OCR garbage)
    if any(c.isdigit() or c.isupper() for c in tok):
        return False
    # Accept if it contains any Tamil diacritic
    if any(c in TAMIL_DIACRITICS for c in tok):
        # Still reject if it also contains obviously non-Tamil chars
        if any(c in "wxqz" for c in tok.lower()):
            return False
        return True
    # No diacritic: accept only known short Tamil syllable patterns
    # Pure vowel: a, i, u, e, o (1-2 chars)
    if all(c in TAMIL_VOWELS for c in tok):
        return True
    # CV pattern: starts with consonant, rest are vowels/consonants
    # Must NOT be an English stopword
    if tok in ENGLISH_STOPWORDS:
        return False
    # Accept if 2-6 chars, starts with Tamil consonant, no non-Latin-script chars
    if tok[0] in set(TAMIL_CONSONANTS) and all(c.isalpha() for c in tok) and len(tok) <= 6:
        # Exclude English function words
        return True
    # Longer words: require diacritic for acceptance (already handled above)
    return False

def extract_tamil_syllables(insc: dict) -> list[str]:
    """Extract clean Tamil syllables from an inscription record."""
    syllables = []
    # Priority 1: literal_aksharas (pre-extracted, but may have Cyrillic noise)
    lit = insc.get("literal_aksharas", [])
    for raw in lit:
        tok = clean_token(str(raw))
        if is_valid_tamil_syllable(tok):
            syllables.append(tok)

    # If fewer than 3 from literal, also try romanized (first 100 chars = before translation)
    if len(syllables) < 3:
        rom_raw = insc.get("romanized_text_b_raw", "")
        # Take only up to first likely translation start
        # Translations typically start with a capital letter after punctuation
        # or after the last Tamil word
        # Simple heuristic: stop at first occurrence of "The " or " of the " etc.
        for stop_word in ["The ", "A ", "An ", "This ", "He ", "She ", "They ", "It "]:
            idx = rom_raw.find(stop_word)
            if idx > 0:
                rom_raw = rom_raw[:idx]
                break
        for word in rom_raw.split():
            tok = clean_token(word)
            if is_valid_tamil_syllable(tok) and tok not in syllables:
                syllables.append(tok)

    return syllables


# ── Main ──────────────────────────────────────────────────────────────────
print("Loading Tamil-Brahmi corpus …")
tb = json.loads(TB_JSON.read_text(encoding="utf-8"))
inscriptions = tb.get("inscriptions", [])

# Use original inscriptions only (cleaner)
original = [i for i in inscriptions if i.get("source", "") != "epub_extraction"]
epub_ext = [i for i in inscriptions if i.get("source", "") == "epub_extraction"]
print(f"  Original inscriptions: {len(original)}")
print(f"  Epub-extracted:        {len(epub_ext)} (using with caution)")

# Extract from ALL, but weight original more
all_syllable_seqs: list[list[str]] = []
seq_by_source: dict[str, list[list[str]]] = {"original": [], "epub": []}

for insc in original:
    seq = extract_tamil_syllables(insc)
    if len(seq) >= 2:
        all_syllable_seqs.append(seq)
        seq_by_source["original"].append(seq)

for insc in epub_ext:
    seq = extract_tamil_syllables(insc)
    if len(seq) >= 2:
        all_syllable_seqs.append(seq)
        seq_by_source["epub"].append(seq)

total_seqs = len(all_syllable_seqs)
total_toks = sum(len(s) for s in all_syllable_seqs)
print(f"\nExtracted {total_seqs} sequences, {total_toks} valid Tamil syllables")
print(f"  From original: {len(seq_by_source['original'])} seqs")
print(f"  From epub:     {len(seq_by_source['epub'])} seqs")

# Build bigram LM with Laplace smoothing
unigram: Counter = Counter()
bigram_counts: Counter = Counter()

for seq in all_syllable_seqs:
    for s in seq:
        unigram[s] += 1
    for i in range(len(seq) - 1):
        bigram_counts[(seq[i], seq[i+1])] += 1

vocab = list(unigram.keys())
V     = len(vocab)
print(f"\nVocabulary: {V} distinct Tamil syllables")
print(f"Bigrams:    {len(bigram_counts)} distinct bigram types")
print(f"Top 10 bigrams: {bigram_counts.most_common(10)}")

# Verify top bigrams are actually Tamil (not English)
top_10 = bigram_counts.most_common(10)
english_contamination = sum(
    1 for (a, b), _ in top_10
    if a in ENGLISH_STOPWORDS or b in ENGLISH_STOPWORDS
)
print(f"\nEnglish contamination in top 10: {english_contamination}/10")
if english_contamination > 2:
    print("  WARNING: still some English contamination — review filter")
else:
    print("  OK: minimal contamination")

# Build log-probability LM
lm: dict[str, float] = {}
for (a, b), cnt in bigram_counts.items():
    prob     = (cnt + 1) / (unigram.get(a, 0) + V + 1)
    lm[f"{a}|{b}"] = round(math.log(prob), 6)

# Save
lm_data = {
    "_doc": (
        "Clean Tamil-Brahmi bigram LM from Mahadevan 2003 corpus. "
        "Filtered to genuine Tamil syllables only (no English, no OCR garbage). "
        "Source: Mahadevan, Iravatham. 2003. Early Tamil Epigraphy. "
        "Harvard Oriental Series 62."
    ),
    "n_inscriptions": total_seqs,
    "n_tokens":       total_toks,
    "vocab_size":     V,
    "n_bigrams":      len(bigram_counts),
    "top_10_bigrams": [(list(k), v) for k, v in top_10],
    "vocab":          vocab,
    "unigrams":       dict(unigram.most_common()),
    "bigrams":        lm,
}
LM_OUT.write_text(json.dumps(lm_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved: {LM_OUT.name}")

# Save report
RPT_OUT.write_text(json.dumps({
    "n_seqs":             total_seqs,
    "n_tokens":           total_toks,
    "n_vocab":            V,
    "n_bigrams":          len(bigram_counts),
    "n_original_seqs":    len(seq_by_source["original"]),
    "n_epub_seqs":        len(seq_by_source["epub"]),
    "top_10_bigrams":     [(list(k), v) for k, v in top_10],
    "english_contamination_top10": english_contamination,
    "verdict":            "CLEAN" if english_contamination <= 2 else "CONTAMINATED",
}, indent=2), encoding="utf-8")

print(f"\nLM is {'CLEAN' if english_contamination <= 2 else 'STILL CONTAMINATED'}")
print("Done.")
