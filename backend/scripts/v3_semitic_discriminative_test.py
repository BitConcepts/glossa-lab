"""V3 Preprint — Discriminative LM Test: Hebrew vs Dravidian on the Indus corpus.

Addresses Fuls' implicit question: "How do you KNOW it's Dravidian and not something else?"

This script builds two language models — Dravidian (from DEDR/TamilTB) and
NW Semitic (from Old Hebrew consonantal corpus) — and scores the same Indus
corpus against both. If Dravidian is the correct language family, the
Dravidian LM should produce a significantly better bigram log-likelihood
score per token than the Hebrew LM.

Output: reports/v3_semitic_discriminative_test.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

_BACKEND = str(Path(__file__).resolve().parent.parent)
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)


def _build_hebrew_lm():
    """Build a LanguageModel from the Old Hebrew consonantal corpus."""
    from glossa_lab.data.old_hebrew import _HEBREW_LINES  # noqa: PLC2701

    # Parse lines: split on whitespace, skip '.' separators
    symbols: list[str] = []
    inscriptions: list[list[str]] = []
    for line in _HEBREW_LINES:
        word_signs = [s for s in line.split() if s != "."]
        if word_signs:
            symbols.extend(word_signs)
            inscriptions.append(word_signs)

    from glossa_lab.pipelines.decipher import LanguageModel

    return LanguageModel(symbols, inscriptions)


def _build_dravidian_lm():
    """Build a LanguageModel from the Dravidian TamilTB LM."""
    lm_path = Path(_BACKEND) / "glossa_lab" / "data" / "dravidian_tamil_lm.json"
    if not lm_path.exists():
        print(f"ERROR: {lm_path} not found")
        sys.exit(1)
    lm_data = json.loads(lm_path.read_text(encoding="utf-8"))

    # The LM JSON has "bigrams" as a dict of {"a,k": count, ...}
    bigrams_raw = lm_data.get("bigrams", {})

    # Build a flat symbol stream by expanding bigram counts
    symbols: list[str] = []
    for key, count in bigrams_raw.items():
        # Try comma, pipe, underscore as separators
        for sep in (",", "|", "_"):
            if sep in key:
                parts = key.split(sep)
                break
        else:
            continue
        if len(parts) == 2:
            for _ in range(max(1, int(count))):
                symbols.extend(parts)

    if not symbols:
        print(f"ERROR: Could not parse any bigrams from {lm_path}")
        sys.exit(1)

    from glossa_lab.pipelines.decipher import LanguageModel

    return LanguageModel(symbols)


def _load_indus_corpus():
    """Load the Holdat V1 Indus corpus (indus_research.jsonl-based)."""
    # Try V2 loader (the primary corpus)
    try:
        from glossa_lab.data.indus_corpus_v2 import load_corpus

        seqs = load_corpus()
        flat = [s for seq in seqs for s in seq]
        return flat, seqs
    except Exception:
        pass

    # Fallback: try Firestore
    try:
        from glossa_lab.data.indus_corpus_firestore import load_corpus

        seqs = load_corpus()
        flat = [s for seq in seqs for s in seq]
        return flat, seqs
    except Exception:
        pass

    print("ERROR: No Indus corpus loader found")
    sys.exit(1)


def _score_corpus_against_lm(corpus_flat, lm):
    """Compute bigram log-likelihood score per token."""
    smoothing = 1e-8
    ll = 0.0
    n_pairs = 0
    for i in range(len(corpus_flat) - 1):
        a, b = corpus_flat[i], corpus_flat[i + 1]
        p = lm.bigram_freq.get((a, b), smoothing)
        ll += math.log(p)
        n_pairs += 1

    return {
        "total_log_likelihood": round(ll, 4),
        "n_pairs": n_pairs,
        "n_tokens": len(corpus_flat),
        "score_per_token": round(ll / max(1, len(corpus_flat)), 4),
        "score_per_pair": round(ll / max(1, n_pairs), 4),
    }


def main():
    print("=" * 68)
    print("  Discriminative LM Test: Hebrew vs Dravidian on Indus Corpus")
    print("=" * 68)

    # Build LMs
    print("\n[1] Building Hebrew LM...")
    heb_lm = _build_hebrew_lm()
    print(f"    Hebrew LM: {len(heb_lm.alphabet)} symbols, "
          f"{len(heb_lm.bigram_freq)} bigrams")

    print("\n[2] Building Dravidian LM...")
    drav_lm = _build_dravidian_lm()
    print(f"    Dravidian LM: {len(drav_lm.alphabet)} symbols, "
          f"{len(drav_lm.bigram_freq)} bigrams")

    # Load Indus corpus
    print("\n[3] Loading Indus corpus...")
    flat, seqs = _load_indus_corpus()
    n_distinct = len(set(flat))
    print(f"    Corpus: {len(flat)} tokens, {len(seqs)} inscriptions, "
          f"{n_distinct} distinct signs")

    # Score against both LMs
    # For fair comparison, we need to map Indus signs to each LM's alphabet.
    # Since neither LM knows Indus sign codes, we use frequency-rank mapping:
    # most frequent Indus sign -> most frequent LM symbol, etc.

    # Frequency-rank map: Indus -> Hebrew
    indus_ranked = [s for s, _ in Counter(flat).most_common()]
    heb_ranked = heb_lm.ranked
    drav_ranked = drav_lm.ranked

    # Build frequency-rank mappings
    heb_map = {}
    for i, isign in enumerate(indus_ranked):
        heb_map[isign] = heb_ranked[i % len(heb_ranked)]

    drav_map = {}
    for i, isign in enumerate(indus_ranked):
        drav_map[isign] = drav_ranked[i % len(drav_ranked)]

    # Apply mappings and score
    print("\n[4] Scoring Indus corpus against Hebrew LM (frequency-rank mapping)...")
    heb_decoded = [heb_map.get(s, heb_ranked[0]) for s in flat]
    heb_score = heb_lm.score_text(heb_decoded)
    heb_spt = heb_score / max(1, len(flat))

    print(f"    Hebrew LM score/token: {heb_spt:.4f}")

    print("\n[5] Scoring Indus corpus against Dravidian LM (frequency-rank mapping)...")
    drav_decoded = [drav_map.get(s, drav_ranked[0]) for s in flat]
    drav_score = drav_lm.score_text(drav_decoded)
    drav_spt = drav_score / max(1, len(flat))

    print(f"    Dravidian LM score/token: {drav_spt:.4f}")

    # Compare
    delta = drav_spt - heb_spt
    winner = "Dravidian" if delta > 0 else "Hebrew" if delta < 0 else "TIE"
    ratio = abs(drav_spt / heb_spt) if heb_spt != 0 else float("inf")

    print(f"\n{'=' * 68}")
    print(f"  RESULT: {winner} wins")
    print(f"  Dravidian score/token: {drav_spt:.4f}")
    print(f"  Hebrew score/token:    {heb_spt:.4f}")
    print(f"  Delta (Drav - Heb):    {delta:+.4f}")
    print(f"  Ratio (Drav/Heb):      {ratio:.4f}")
    print(f"{'=' * 68}")

    result = {
        "test": "Discriminative LM: Hebrew vs Dravidian on Indus corpus",
        "method": "Frequency-rank mapping (most frequent Indus sign -> most frequent LM symbol)",
        "corpus": {
            "tokens": len(flat),
            "inscriptions": len(seqs),
            "distinct_signs": n_distinct,
        },
        "hebrew_lm": {
            "alphabet_size": len(heb_lm.alphabet),
            "n_bigrams": len(heb_lm.bigram_freq),
            "score_per_token": round(heb_spt, 4),
            "total_score": round(heb_score, 4),
        },
        "dravidian_lm": {
            "alphabet_size": len(drav_lm.alphabet),
            "n_bigrams": len(drav_lm.bigram_freq),
            "score_per_token": round(drav_spt, 4),
            "total_score": round(drav_score, 4),
        },
        "comparison": {
            "winner": winner,
            "delta_score_per_token": round(delta, 4),
            "ratio": round(ratio, 4),
        },
    }

    out_path = Path(_BACKEND).parent / "reports" / "v3_semitic_discriminative_test.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
