"""Compute entropy and Zipf metrics for the IVS corpus.

Computes unigram entropy H0, bigram conditional entropy H1,
and Zipf slope for all IVS inscriptions in the translation corpus.
"""
import json
import math
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]


def load_ivs_sequences() -> list[list[str]]:
    """Load sign sequences from the translation corpus."""
    corpus_path = ROOT / "outputs" / "seal_translations.json"
    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    return [t["signs"] for t in data["translations"] if t["signs"]]


def unigram_entropy(sequences: list[list[str]]) -> float:
    """H0: Shannon entropy of unigram distribution."""
    counts: Counter[str] = Counter()
    for seq in sequences:
        counts.update(seq)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum(
        (c / total) * math.log2(c / total) for c in counts.values() if c > 0
    )


def bigram_conditional_entropy(sequences: list[list[str]]) -> float:
    """H1: conditional entropy H(Y|X) over bigrams."""
    bigram_counts: Counter[tuple[str, str]] = Counter()
    unigram_counts: Counter[str] = Counter()
    for seq in sequences:
        for i in range(len(seq) - 1):
            bigram_counts[(seq[i], seq[i + 1])] += 1
            unigram_counts[seq[i]] += 1
    total_bigrams = sum(bigram_counts.values())
    if total_bigrams == 0:
        return 0.0
    # H(X,Y) - H(X)
    joint = -sum(
        (c / total_bigrams) * math.log2(c / total_bigrams)
        for c in bigram_counts.values()
        if c > 0
    )
    total_uni = sum(unigram_counts.values())
    marginal = -sum(
        (c / total_uni) * math.log2(c / total_uni)
        for c in unigram_counts.values()
        if c > 0
    )
    return joint - marginal


def zipf_slope(sequences: list[list[str]]) -> float:
    """Compute Zipf exponent via least-squares log-log fit."""
    counts: Counter[str] = Counter()
    for seq in sequences:
        counts.update(seq)
    freqs = sorted(counts.values(), reverse=True)
    n = len(freqs)
    if n < 2:
        return 0.0
    log_ranks = [math.log(i + 1) for i in range(n)]
    log_freqs = [math.log(f) for f in freqs]
    mean_x = sum(log_ranks) / n
    mean_y = sum(log_freqs) / n
    num = sum((log_ranks[i] - mean_x) * (log_freqs[i] - mean_y) for i in range(n))
    den = sum((log_ranks[i] - mean_x) ** 2 for i in range(n))
    return num / den if den != 0 else 0.0


def compute_all() -> dict:
    """Compute all entropy metrics for IVS."""
    seqs = load_ivs_sequences()
    all_tokens = sum(len(s) for s in seqs)
    all_types = len({sign for seq in seqs for sign in seq})
    mean_len = all_tokens / len(seqs) if seqs else 0

    h0 = unigram_entropy(seqs)
    h1 = bigram_conditional_entropy(seqs)
    alpha = zipf_slope(seqs)

    result = {
        "system": "Indus Valley Script (IVS)",
        "n_texts": len(seqs),
        "n_tokens": all_tokens,
        "n_types": all_types,
        "mean_text_length": round(mean_len, 2),
        "H0_unigram_entropy": round(h0, 4),
        "H1_conditional_entropy": round(h1, 4),
        "zipf_slope": round(alpha, 4),
    }
    return result


if __name__ == "__main__":
    result = compute_all()
    print(json.dumps(result, indent=2))
    out = ROOT / "outputs" / "benchmarks"
    out.mkdir(parents=True, exist_ok=True)
    (out / "ivs_entropy_metrics.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(f"\nSaved to {out / 'ivs_entropy_metrics.json'}")
