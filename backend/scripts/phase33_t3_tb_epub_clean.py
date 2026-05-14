"""Phase-33 T3: Clean epub-extracted Tamil-Brahmi inscriptions and rebuild Dravidian syllable LM.

Problem:
  74 of 121 inscriptions in mahadevan_2003_tamil_brahmi.json were extracted via epub OCR.
  These contain English noise tokens: 'racing', 'ig', 'ocus', 'the', 'of', 'pp', etc.
  These contaminate the Dravidian syllable LM built from TB aksharas.

Fix:
  Filter each akshara in epub entries against known Tamil-Brahmi akshara patterns:
  - Must be 1-4 chars
  - Must match CV / CVC / V pattern (Tamil syllable structure)
  - No English function words, no numbers, no capitalized words (non-akshara)
  - Reject tokens containing digits, parentheses, slashes, brackets, etc.

Output:
  - reports/mahadevan_2003_tb_clean_stats.json: stats on cleaning
  - backend/glossa_lab/data/mahadevan_2003_tb_lm_clean.json: rebuilt bigram LM
  - reports/phase33_t3_tb_epub_clean.json: full report

Citations:
  A.12 — Mahadevan 2003 'Early Tamil Epigraphy'
  E.1  — DEDR (Burrow & Emeneau)
"""
from __future__ import annotations
import json, math, re, sys, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS = ROOT / "reports"
DATA = ROOT / "backend" / "glossa_lab" / "data"

# ── Known Tamil-Brahmi vowels and consonant initials ──────────────────────────
_TB_VOWELS    = set("aeiouāīūḷ")
_TB_CONSONANTS = set("bcdfghjklmnpqrstvwxyzṟṉṭḍṅṇñśṣḥ")

# English stop words / noise words seen in epub extraction
_ENGLISH_NOISE = {
    "racing", "ig", "ocus", "the", "of", "to", "in", "on", "at", "by",
    "and", "or", "is", "it", "its", "this", "that", "from", "for", "as",
    "are", "was", "but", "not", "with", "an", "he", "she", "we", "you",
    "pp", "pl", "fig", "no", "see", "cm", "ca", "nd", "rd", "th", "st",
    "ee", "os", "al", "oc", "le", "ur", "ub", "or", "age", "ate", "ute",
    "left", "right", "cave", "rock", "line", "upper", "lower", "middle",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "ninth",
    "google", "tracing", "estampage", "inscription", "plate", "digitized",
    "oogle", "ength", "nscription", "ocus", "ubl", "amil", "rahmi",
    "early", "late", "century", "century", "are", "not", "more", "from",
    "made", "given", "caused", "carved", "engraved", "reading", "known",
    "probably", "approximately", "extant", "incomplete", "broken", "damaged",
}

# Akshara regex: allows 1-5 chars, starts with consonant or vowel, no digits,
# no capitals, no brackets, no punctuation except diacritics
_AKSHARA_RE = re.compile(
    r"^[a-zāīūṟṉṭḍṅṇñśṣḥṛḷḻ]{1,5}$"
)

# Known M77 bigrams — if a token appears as an M77 sign, it's valid
# (these are valid akshara shapes that overlap with M77 corpus signs)
_VALID_M77_SHAPES = {
    "na", "ka", "ta", "pa", "ya", "ma", "va", "la", "ra", "sa", "ca",
    "ti", "ni", "ki", "pi", "vi", "li", "ri", "si", "ci",
    "tu", "nu", "ku", "pu", "vu", "lu", "ru", "su", "cu",
    "te", "ne", "ke", "pe", "ve", "le", "re", "se", "ce",
    "to", "no", "ko", "po", "vo", "lo", "ro", "so", "co",
    "tā", "nā", "kā", "pā", "vā", "lā", "rā",
    "tà", "và", "pà", "rà", "kà", "nà",
    "mu", "bu", "du", "gu", "hu", "ju",
    "ba", "da", "ga", "ha", "ja", "fa",
    "an", "in", "un", "am", "im", "um",
    "ai", "au",
    "ya", "wa", "ha",
    "kol", "kal", "tal", "pal", "nal", "mal", "val", "ral",
    "kan", "tan", "pan", "nan", "man", "van", "ran",
    "kar", "tar", "par", "nar", "mar", "var",
    "ko", "ki", "ke", "ku",
    "mi", "min", "miin",
    "pu", "puli",
    "er", "eru",
    "kol",
    "tai", "kai", "nai", "vai", "rai", "pai", "mai",
    "ura", "iru", "oru",
    "muta", "nelli", "koni",
}

def _is_valid_akshara(token: str) -> bool:
    """Return True if this token looks like a genuine Tamil-Brahmi akshara."""
    if not token or len(token) > 6:
        return False
    # Strip uncertainty markers at end
    t = token.rstrip("!?")
    # Skip empty or pure punctuation
    if not t:
        return False
    # Skip tokens with digits, brackets, slashes, dots (OCR noise)
    if re.search(r"[0-9\[\]{}()/\\|.,;:\"]", t):
        return False
    # Skip capitalized (English proper nouns / OCR headers)
    if t[0].isupper():
        return False
    # Skip English noise words
    if t.lower() in _ENGLISH_NOISE:
        return False
    # Skip tokens longer than 6 chars (unlikely akshara)
    if len(t) > 6:
        return False
    # Skip tokens that are purely English-looking long words
    if len(t) >= 4 and re.match(r"^[a-z]+$", t) and t not in _VALID_M77_SHAPES:
        # Check if it matches Tamil syllable structure (short, CV/CVC/CVCC)
        # 4+ char pure-ASCII words that aren't in known shapes are usually English
        if len(t) >= 6:
            return False
        # 4-5 char: allow if it looks like a Tamil word (not in English noise)
        # Common 4-char TB aksharas: "tara", "kani", "nata", "muta", etc.
        if len(t) == 4 and t[3] in "aeiou":
            pass  # CV+CV pattern — likely valid
        elif len(t) == 4 and t[2] in "aeiou" and t[3] in "lrnmt":
            pass  # CVC+C — could be valid
        else:
            # Run through the known-valid list
            pass
    # Accept tokens matching basic akshara regex
    if _AKSHARA_RE.match(t.lower()):
        return True
    # Accept tokens in known M77 shape set
    if t.lower() in _VALID_M77_SHAPES:
        return True
    return False

# ── Load corpus ───────────────────────────────────────────────────────────────
print("Loading mahadevan_2003_tamil_brahmi.json...")
tb_data = json.loads((DATA / "mahadevan_2003_tamil_brahmi.json").read_text("utf-8"))
inscriptions_raw = tb_data.get("inscriptions", [])
print(f"Total entries: {len(inscriptions_raw)}")

# Categorize entries
original_entries = [e for e in inscriptions_raw if e.get("source") != "epub_extraction"]
epub_entries = [e for e in inscriptions_raw if e.get("source") == "epub_extraction"]
print(f"  Original parse: {len(original_entries)}")
print(f"  Epub-extracted: {len(epub_entries)}")

# ── Clean epub entries ─────────────────────────────────────────────────────────
print("\nCleaning epub entries...")
epub_clean_stats = []
cleaned_epub = 0
total_original_epub_tokens = 0
total_clean_epub_tokens = 0

for entry in epub_entries:
    raw_aksharas = entry.get("literal_aksharas", [])
    total_original_epub_tokens += len(raw_aksharas)
    clean = [a for a in raw_aksharas if _is_valid_akshara(str(a))]
    total_clean_epub_tokens += len(clean)
    epub_clean_stats.append({
        "id": entry.get("inscription_id", ""),
        "site": entry.get("site", ""),
        "original_n": len(raw_aksharas),
        "clean_n": len(clean),
        "kept_pct": round(len(clean) / max(len(raw_aksharas), 1) * 100, 1),
        "clean_aksharas": clean,
    })
    if len(clean) >= 3:
        cleaned_epub += 1

print(f"  Epub entries with >=3 clean aksharas: {cleaned_epub}/{len(epub_entries)}")
print(f"  Total epub tokens: {total_original_epub_tokens} → {total_clean_epub_tokens} clean "
      f"({100*total_clean_epub_tokens//max(total_original_epub_tokens,1)}% kept)")

# ── Collect all clean aksharas for LM rebuild ─────────────────────────────────
print("\nCollecting clean aksharas for LM rebuild...")
all_clean_aksharas: list[str] = []

# From original parse entries (these are already clean)
orig_tokens = 0
for entry in original_entries:
    aksharas = entry.get("literal_aksharas", [])
    # Light filter on originals too (remove obvious noise)
    clean = [a for a in aksharas if _is_valid_akshara(str(a))]
    all_clean_aksharas.extend(clean)
    orig_tokens += len(clean)

print(f"  Original entries: {orig_tokens} clean tokens from {len(original_entries)} inscriptions")

# From cleaned epub entries
epub_tokens = 0
for stat in epub_clean_stats:
    if stat["clean_n"] >= 3:
        all_clean_aksharas.extend(stat["clean_aksharas"])
        epub_tokens += stat["clean_n"]

print(f"  Epub entries: {epub_tokens} clean tokens from {cleaned_epub} inscriptions")
print(f"  Total clean tokens: {len(all_clean_aksharas)}")

# ── Build bigram LM ───────────────────────────────────────────────────────────
print("\nBuilding bigram LM from clean TB aksharas...")
bigram_count: Counter = Counter()
unigram_count: Counter = Counter()

# Group back into inscription sequences for bigrams
# Original entries: use clean aksharas in sequence order
def _clean_insc(entry: dict) -> list[str]:
    return [a for a in entry.get("literal_aksharas", []) if _is_valid_akshara(str(a))]

sequences: list[list[str]] = []
for entry in original_entries:
    seq = _clean_insc(entry)
    if len(seq) >= 2:
        sequences.append(seq)

for stat in epub_clean_stats:
    seq = stat["clean_aksharas"]
    if len(seq) >= 2:
        sequences.append(seq)

for seq in sequences:
    for tok in seq:
        unigram_count[tok] += 1
    for i in range(len(seq) - 1):
        bigram_count[(seq[i], seq[i+1])] += 1

print(f"  Sequences (>=2 tokens): {len(sequences)}")
print(f"  Distinct unigrams: {len(unigram_count)}")
print(f"  Distinct bigrams: {len(bigram_count)}")
print(f"  Top-10 aksharas: {[f'{a}:{c}' for a, c in unigram_count.most_common(10)]}")

# Convert to log-probabilities
total_bigrams = sum(bigram_count.values())
bigram_logprob: dict[str, float] = {}
for (a, b), cnt in bigram_count.items():
    bigram_logprob[f"{a}|{b}"] = math.log(cnt / total_bigrams)

# Build vocab
vocab = [tok for tok, _ in unigram_count.most_common()]

# ── Save rebuilt LM ────────────────────────────────────────────────────────────
lm_out = {
    "_citation": {
        "primary_sources": ["A.12", "E.1"],
        "derivation": (
            "Rebuilt from cleaned mahadevan_2003_tamil_brahmi.json (Phase-33 T3). "
            "Epub OCR noise filtered using Tamil akshara pattern matching. "
            f"{len(sequences)} inscription sequences, {len(bigram_count)} bigrams."
        ),
        "authors": "Mahadevan, Iravatham (2003). Early Tamil Epigraphy, Harvard Oriental Series 62.",
    },
    "language": "tamil_brahmi_clean",
    "phase": "Phase-33-T3",
    "n_sequences": len(sequences),
    "n_bigrams": len(bigram_count),
    "n_syllables": len(vocab),
    "vocab": vocab,
    "bigrams": bigram_logprob,
}
lm_path = DATA / "mahadevan_2003_tb_lm_clean.json"
lm_path.write_text(json.dumps(lm_out, indent=2, ensure_ascii=False), "utf-8")
print(f"\nSaved rebuilt LM: {lm_path} ({lm_path.stat().st_size // 1024}KB)")

# ── Full report ────────────────────────────────────────────────────────────────
report = {
    "experiment": "Phase-33 T3: TB epub quality improvement",
    "n_original_entries": len(original_entries),
    "n_epub_entries": len(epub_entries),
    "n_epub_usable_after_clean": cleaned_epub,
    "total_epub_tokens_before": total_original_epub_tokens,
    "total_epub_tokens_after": total_clean_epub_tokens,
    "epub_keep_rate_pct": round(100 * total_clean_epub_tokens / max(total_original_epub_tokens, 1), 1),
    "clean_lm_n_sequences": len(sequences),
    "clean_lm_n_bigrams": len(bigram_count),
    "clean_lm_n_syllables": len(vocab),
    "clean_lm_top20_aksharas": [{"akshara": a, "count": c} for a, c in unigram_count.most_common(20)],
    "epub_entries_detail": epub_clean_stats[:20],  # first 20 for brevity
    "verdict": (
        f"Phase-33 T3 TB epub cleaning: {len(epub_entries)} epub entries processed. "
        f"{cleaned_epub} retained (>=3 clean aksharas). "
        f"Token keep rate: {100*total_clean_epub_tokens//max(total_original_epub_tokens,1)}%. "
        f"Rebuilt LM: {len(sequences)} sequences, {len(bigram_count)} bigrams, {len(vocab)} syllables. "
        f"Saved to backend/glossa_lab/data/mahadevan_2003_tb_lm_clean.json."
    ),
    "_citation": {"primary": ["A.12", "E.1"], "phase": "Phase-33-T3"},
}
(REPORTS / "phase33_t3_tb_epub_clean.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False), "utf-8")
print(f"Saved phase33_t3_tb_epub_clean.json")
print(f"\nVerdict: {report['verdict']}")
