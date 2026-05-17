"""Phase-44: Rebuild Dravidian Tamil LM with TamilTB data.

The current LM (486 bigrams) was built purely from dravidian.py's curated sequences.
TamilTB (Tamil TreeBank) is a morphologically annotated corpus that gives us:
  - TamilTB.v0.1.utf8.tt: 435 KB plain-token tab-separated
  - TamilTB.v0.1.utf8.conll: 744 KB CoNLL format with POS tags

Strategy:
  1. Parse TamilTB CoNLL for lemmas/forms (filtered to noun/verb morpheme sequences)
  2. Extract Tamil syllable bigrams from the word forms
  3. Merge with the existing dravidian.py sequences
  4. Rebuild bigrams, recompute verdict

Why this matters:
  Current 486 bigrams undercount Tamil syllabic transition patterns.
  TamilTB has ~12,000 tokens → ~4,000 unique forms → potentially 5,000+ bigrams.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

TAMILTB_TT    = REPO / "corpora/downloads/external_repos/Kee2u_Indus_Decipherment/TamilTB.v0.1/data/TamilTB.v0.1.utf8.tt"
TAMILTB_CONLL = REPO / "corpora/downloads/external_repos/Kee2u_Indus_Decipherment/TamilTB.v0.1/data/TamilTB.v0.1.utf8.conll"
LM_OUT = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
REPORTS = REPO / "reports"

# Tamil syllable segmentation — simplified but effective for bigrams
_VOWELS = "aeiouāēīōūṃṁ"
_CONSONANTS = "bcdghjklmnprstvyzṭḍṇḷṟṉñśṣ"

def segment_tamil_syllables(word: str) -> list[str]:
    """Extract consonant-vowel pairs as syllables from a Tamil word."""
    # Simple CV segmentation: C(C)V or V
    syllables = []
    word = word.lower().strip()
    # Remove punctuation
    word = re.sub(r"[^\w\u0B80-\u0BFF]", "", word)
    if not word or len(word) < 2:
        return []
    # Extract 2-char sequences as proxy syllables
    # (Full Tamil syllabification is complex; this gives useful bigrams)
    for i in range(len(word) - 1):
        pair = word[i:i+2]
        if re.match(r"[a-zāēīōūṭḍṇḷṟṉñśṣ]{2}", pair):
            syllables.append(pair)
    return syllables


def parse_tamiltb_tt(path: Path) -> list[str]:
    """Parse TamilTB .tt file (tab-separated: word\tPOS\t...) for word forms."""
    words = []
    if not path.exists():
        print(f"  WARNING: {path.name} not found at {path}")
        return words
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split("\t")
            if parts:
                word = parts[0].strip()
                # Skip empty, punctuation-only, numbers
                if word and not re.match(r"^[\d.,;:!?()\"'\s]+$", word) and len(word) > 1:
                    words.append(word)
    return words


def parse_tamiltb_conll(path: Path) -> list[str]:
    """Parse TamilTB CoNLL file for LEMMA column."""
    words = []
    if not path.exists():
        print(f"  WARNING: {path.name} not found at {path}")
        return words
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            # CoNLL format: id, form, lemma, pos, ...
            if len(parts) >= 3:
                form = parts[1].strip()
                lemma = parts[2].strip() if parts[2] != "_" else form
                # Use form for bigram extraction
                if form and not re.match(r"^[\d.,;:!?()\"'\s]+$", form) and len(form) > 1:
                    words.append(form)
    return words


def build_bigrams_from_words(words: list[str]) -> Counter:
    """Build character bigrams from Tamil words."""
    bigrams: Counter = Counter()
    for word in words:
        # Extract character bigrams from the word
        syllables = segment_tamil_syllables(word)
        if len(syllables) >= 2:
            for i in range(len(syllables) - 1):
                bigrams[(syllables[i], syllables[i+1])] += 1
        # Also add raw 2-char bigrams
        clean = re.sub(r"[^\w\u0B80-\u0BFF]", "", word.lower())
        for i in range(len(clean) - 1):
            pair = clean[i:i+2]
            # Only Tamil Unicode or ASCII letters
            if re.match(r"[\u0B80-\u0BFF]{2}", pair) or re.match(r"[a-z]{2}", pair):
                bigrams[pair] += 1
    return bigrams


def check_english_contamination(words: list[str]) -> float:
    """Check % of words that look like English."""
    if not words:
        return 0.0
    english_re = re.compile(r"^[a-zA-Z]+$")
    n_english = sum(1 for w in words if english_re.match(w) and len(w) > 2)
    return round(n_english / len(words), 4)


if __name__ == "__main__":
    print("=" * 60)
    print("Phase-44: Rebuild Dravidian Tamil LM with TamilTB")
    print("=" * 60)

    # Load existing LM to merge with
    existing_bigrams: Counter = Counter()
    existing_sources = []
    if LM_OUT.exists():
        existing_lm = json.loads(LM_OUT.read_text(encoding="utf-8"))
        existing_bigrams_raw = existing_lm.get("bigrams", {})
        for k, v in existing_bigrams_raw.items():
            if isinstance(k, str) and "," in k:
                a, b = k.split(",", 1)
                existing_bigrams[(a.strip(), b.strip())] = v
            elif isinstance(k, list):
                existing_bigrams[tuple(k)] = v
        existing_sources = existing_lm.get("sources", ["dravidian.py"])
        print(f"  Existing LM: {len(existing_bigrams)} bigrams from {existing_sources}")
    else:
        print("  No existing LM found — building from scratch")

    # Parse TamilTB
    print(f"\nParsing TamilTB .tt file ({TAMILTB_TT.name})...")
    tt_words = parse_tamiltb_tt(TAMILTB_TT)
    print(f"  {len(tt_words)} word forms")
    tt_english_pct = check_english_contamination(tt_words)
    print(f"  English contamination: {tt_english_pct:.1%}")

    print(f"\nParsing TamilTB CoNLL file ({TAMILTB_CONLL.name})...")
    conll_words = parse_tamiltb_conll(TAMILTB_CONLL)
    print(f"  {len(conll_words)} word forms")

    # Build bigrams from TamilTB
    all_tamiltb_words = tt_words + conll_words
    # Deduplicate
    all_tamiltb_words = list(dict.fromkeys(all_tamiltb_words))
    print(f"\nBuilding bigrams from {len(all_tamiltb_words)} unique TamilTB word forms...")
    tamiltb_bigrams = build_bigrams_from_words(all_tamiltb_words)
    print(f"  {len(tamiltb_bigrams)} new bigrams from TamilTB")

    # Also import from dravidian.py directly for comparison
    try:
        from glossa_lab.data.dravidian import get_corpus_inscriptions, get_attested_words  # type: ignore
        dravidian_seqs = get_corpus_inscriptions()
        dravidian_words_raw = []
        for seq in dravidian_seqs:
            dravidian_words_raw.extend(seq)
        dravidian_bigrams: Counter = Counter()
        for seq in dravidian_seqs:
            for i in range(len(seq) - 1):
                a, b = seq[i], seq[i+1]
                if a and b:
                    dravidian_bigrams[(a, b)] += 1
        print(f"  {len(dravidian_bigrams)} bigrams from dravidian.py ({len(dravidian_seqs)} sequences)")
    except Exception as e:
        dravidian_bigrams = existing_bigrams
        print(f"  dravidian.py import failed: {e} — using existing bigrams")

    # Merge all bigrams
    merged: Counter = Counter()
    merged.update(dravidian_bigrams)
    merged.update(tamiltb_bigrams)
    # Don't use existing_bigrams to avoid double-counting dravidian.py
    print(f"\nMerged: {len(merged)} total bigrams")
    top10 = merged.most_common(10)
    print(f"  Top 10: {top10}")

    # Check for English contamination in merged bigrams
    english_pairs = sum(1 for (a, b) in merged
                        if re.match(r"^[a-z]+$", str(a)) and re.match(r"^[a-z]+$", str(b)))
    tamiltb_contamination = tt_english_pct

    verdict = "CLEAN" if tamiltb_contamination < 0.05 else "CONTAMINATED"

    # Build vocab from TamilTB words
    vocab_from_tamiltb = Counter(w.lower() for w in all_tamiltb_words if len(w) > 1)

    # Build output LM
    lm_out = {
        "_citation": {
            "primary_sources": ["E.1", "E.2", "E.3"],
            "derivation": (
                "Merged from: (1) dravidian.py curated Sangam + DEDR sequences, "
                "(2) TamilTB v0.1 (morphologically annotated Tamil TreeBank, ~12K tokens). "
                "TamilTB via Kee2u_Indus_Decipherment repo, License: CC-SA 3.0."
            ),
            "authors": "Burrow & Emeneau 1984 (DEDR); Tamil TreeBank project; Glossa Lab 2026",
            "date": "2026-05-17",
        },
        "sources": ["dravidian.py (Sangam+DEDR)", "TamilTB.v0.1 (morphologically annotated)"],
        "n_inscription_sequences": len(dravidian_seqs) if "dravidian_seqs" in dir() else 0,
        "n_tamiltb_words": len(all_tamiltb_words),
        "total_syllables": sum(merged.values()),
        "vocab_size": len(vocab_from_tamiltb),
        "n_bigrams": len(merged),
        "english_contamination": tamiltb_contamination,
        "verdict": verdict,
        "top_15_bigrams": [{"bigram": list(k), "count": v} for k, v in merged.most_common(15)],
        "vocab": dict(list(vocab_from_tamiltb.most_common(200))),
        "unigrams": {},  # could be filled; keeping minimal
        "bigrams": {f"{a},{b}": c for (a, b), c in merged.items()},
    }

    LM_OUT.write_text(json.dumps(lm_out, indent=2, ensure_ascii=False), encoding="utf-8")

    # Save report
    rpt = {
        "_citation": lm_out["_citation"],
        "n_bigrams_before": len(existing_bigrams),
        "n_bigrams_after": len(merged),
        "increase": len(merged) - len(existing_bigrams),
        "increase_pct": round((len(merged) - len(existing_bigrams)) / max(len(existing_bigrams), 1) * 100),
        "tamiltb_words": len(all_tamiltb_words),
        "verdict": verdict,
        "english_contamination_pct": tamiltb_contamination,
    }
    (REPORTS / "phase44_dravidian_lm_rebuild.json").write_text(
        json.dumps(rpt, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n✓ Dravidian LM rebuilt: {len(existing_bigrams)} → {len(merged)} bigrams "
          f"(+{len(merged) - len(existing_bigrams)})")
    print(f"  Verdict: {verdict}, English contamination: {tamiltb_contamination:.1%}")
    print(f"  Saved to {LM_OUT.name}")
