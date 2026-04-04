"""Small-sample entropy estimators.

Implements bias-corrected entropy estimators for small corpora where the
naive maximum-likelihood estimator (MLE) systematically underestimates
entropy due to unobserved symbols ("missing mass").

Two estimators are provided:

Miller-Madow (1955)
  H_MM = H_MLE + (K - 1) / (2 * N)
  where K = number of observed distinct symbols, N = total symbol count.
  Simple additive correction. Works best when N >> K.

Chao-Shen (2003)
  Uses Good-Turing coverage estimation C = 1 - f1/N (f1 = singleton count)
  to adjust probabilities before computing entropy, then divides each term
  by the inclusion probability to account for unseen symbols.

  H_CS = -sum_i [ p̂_i * log(p̂_i) / (1 - (1 - p̂_i)^N) ]
  where p̂_i = C * x_i / N

  Significantly better than Miller-Madow for small or sparse corpora.

References:
  Miller, G. A. (1955). Note on the bias of information estimates.
    In H. Quastler (Ed.), Information Theory in Psychology, pp. 95–100.
  Chao, A., & Shen, T-J. (2003). Nonparametric estimation of Shannon's
    index of diversity when there are unseen species in sample.
    Environmental and Ecological Statistics 10(4), 429-443.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any


def miller_madow_entropy(counts: Counter) -> float:
    """Miller-Madow bias-corrected entropy estimator.

    Args:
        counts: Counter mapping symbol (or n-gram) to its count.

    Returns:
        Estimated entropy in nats.
    """
    N = sum(counts.values())
    if N == 0:
        return 0.0

    K = len(counts)  # number of observed distinct symbols

    # MLE entropy
    h_mle = 0.0
    for c in counts.values():
        p = c / N
        if p > 0:
            h_mle -= p * math.log(p)

    # Miller-Madow correction
    correction = (K - 1) / (2 * N)
    return h_mle + correction


def chao_shen_entropy(counts: Counter) -> float:
    """Chao-Shen coverage-adjusted entropy estimator.

    Uses Good-Turing coverage C = 1 - f1/N as a shrinkage factor,
    then applies an inclusion-probability correction to each term.

    Args:
        counts: Counter mapping symbol (or n-gram) to its count.

    Returns:
        Estimated entropy in nats.
    """
    N = sum(counts.values())
    if N == 0:
        return 0.0

    # Good-Turing coverage estimate
    f1 = sum(1 for c in counts.values() if c == 1)  # singletons
    coverage = 1.0 - f1 / N
    # Clamp coverage to avoid degenerate cases
    coverage = max(coverage, 1e-8)

    h_cs = 0.0
    for c in counts.values():
        p_hat = c / N  # MLE probability
        p_adj = coverage * p_hat  # coverage-adjusted

        if p_adj <= 0:
            continue

        # Inclusion probability: P(symbol observed at least once in N draws)
        # For large N * p_adj this approaches 1; avoids log(0) issues.
        inclusion = 1.0 - (1.0 - p_adj) ** N
        if inclusion <= 0:
            continue

        h_cs -= (p_adj * math.log(p_adj)) / inclusion

    return h_cs


def estimate_entropy(
    symbols: list[str],
    n: int = 1,
    estimator: str = "mle",
) -> float:
    """Compute entropy for n-grams of size n using the specified estimator.

    Args:
        symbols: flat list of symbols.
        n: n-gram size (1 = unigram, 2 = bigram, etc.).
        estimator: one of "mle", "miller_madow", "chao_shen".

    Returns:
        Estimated entropy in nats.

    Raises:
        ValueError: if estimator name is unknown.
    """
    if len(symbols) < n:
        return 0.0

    counts: Counter = Counter()
    for i in range(len(symbols) - n + 1):
        ngram = tuple(symbols[i : i + n])
        counts[ngram] += 1

    if estimator == "mle":
        N = sum(counts.values())
        if N == 0:
            return 0.0
        h = 0.0
        for c in counts.values():
            p = c / N
            if p > 0:
                h -= p * math.log(p)
        return h
    elif estimator == "miller_madow":
        return miller_madow_entropy(counts)
    elif estimator == "chao_shen":
        return chao_shen_entropy(counts)
    else:
        raise ValueError(
            f"Unknown estimator: {estimator!r}. Choose from: 'mle', 'miller_madow', 'chao_shen'."
        )


def compare_estimators(
    symbols: list[str],
    max_n: int = 6,
) -> dict[str, Any]:
    """Run all three estimators and return a comparison.

    Useful for diagnostics: shows how much the MLE underestimates
    relative to the bias-corrected estimators for each n-gram order.

    Args:
        symbols: flat list of symbols.
        max_n: maximum n-gram size.

    Returns:
        dict with keys 'mle', 'miller_madow', 'chao_shen', each a list
        of dicts {n, raw_nats, normalized}.
    """
    alphabet_size = len(set(symbols))
    ln_L = math.log(alphabet_size) if alphabet_size > 1 else 1.0

    result: dict[str, Any] = {
        "alphabet_size": alphabet_size,
        "symbol_count": len(symbols),
    }
    for name in ("mle", "miller_madow", "chao_shen"):
        entries = []
        for n in range(1, max_n + 1):
            raw = estimate_entropy(symbols, n=n, estimator=name)
            normalized = raw / ln_L if ln_L > 0 else 0.0
            entries.append(
                {
                    "n": n,
                    "raw_nats": round(raw, 6),
                    "normalized": round(normalized, 6),
                }
            )
        result[name] = entries

    return result
