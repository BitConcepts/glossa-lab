"""Statistical utilities for experiment analysis.

Provides bootstrap confidence intervals, empirical p-values, and z-scores
for use in the Linear A anti-circularity experiment suite.
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def bootstrap_ci(
    scores: Sequence[float],
    confidence: float = 0.95,
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Bootstrap confidence interval for the mean of scores.

    Args:
        scores: Sample of numerical scores.
        confidence: Confidence level (default 0.95 = 95% CI).
        n_bootstrap: Number of bootstrap resamples.
        seed: Random seed.

    Returns:
        (mean, lower_bound, upper_bound)
    """
    rng = random.Random(seed)
    n = len(scores)
    if n == 0:
        return 0.0, 0.0, 0.0

    mean = sum(scores) / n
    if n == 1:
        return mean, mean, mean

    # Bootstrap resampling
    boot_means: list[float] = []
    for _ in range(n_bootstrap):
        sample = [rng.choice(scores) for _ in range(n)]  # type: ignore[arg-type]
        boot_means.append(sum(sample) / n)

    boot_means.sort()
    alpha = 1.0 - confidence
    lo_idx = int(alpha / 2 * n_bootstrap)
    hi_idx = int((1 - alpha / 2) * n_bootstrap) - 1
    lo_idx = max(0, lo_idx)
    hi_idx = min(len(boot_means) - 1, hi_idx)

    return mean, boot_means[lo_idx], boot_means[hi_idx]


def empirical_p_value(
    real_score: float,
    null_scores: Sequence[float],
    tail: str = "right",
) -> float:
    """Empirical (permutation) p-value.

    Args:
        real_score: The observed score under the real mapping.
        null_scores: Distribution of scores under the null (random) mapping.
        tail: 'right' = fraction of null scores >= real (default),
              'left'  = fraction <= real,
              'two'   = 2 * min(left, right).

    Returns:
        p-value in [0, 1].
    """
    n = len(null_scores)
    if n == 0:
        return 1.0

    if tail == "right":
        count = sum(1 for s in null_scores if s >= real_score)
    elif tail == "left":
        count = sum(1 for s in null_scores if s <= real_score)
    else:
        right = sum(1 for s in null_scores if s >= real_score)
        left = sum(1 for s in null_scores if s <= real_score)
        count = 2 * min(right, left)

    return count / n


def z_score(
    real: float,
    null_scores: Sequence[float],
) -> float:
    """Z-score of the real result against the null distribution.

    Args:
        real: Observed value under the real mapping.
        null_scores: Distribution under the null.

    Returns:
        Z-score. Higher = more extreme relative to null mean.
    """
    n = len(null_scores)
    if n < 2:
        return 0.0
    mean = sum(null_scores) / n
    variance = sum((s - mean) ** 2 for s in null_scores) / (n - 1)
    std = math.sqrt(variance) if variance > 0 else 1.0
    return (real - mean) / std


def effect_size(
    real: float,
    null_scores: Sequence[float],
) -> float:
    """Cohen's d effect size: (real - null_mean) / null_std."""
    return z_score(real, null_scores)  # Same formula; Cohen's d = z for large n


def summarise(
    scores: Sequence[float],
    label: str = "",
) -> dict[str, float]:
    """Return descriptive statistics for a score list."""
    n = len(scores)
    if n == 0:
        return {"n": 0, "mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / max(n - 1, 1)
    std = math.sqrt(variance)
    sorted_s = sorted(scores)
    median = sorted_s[n // 2] if n % 2 == 1 else (sorted_s[n // 2 - 1] + sorted_s[n // 2]) / 2
    return {
        "label": label,
        "n": n,
        "mean": round(mean, 4),
        "std": round(std, 4),
        "min": round(min(scores), 4),
        "max": round(max(scores), 4),
        "median": round(median, 4),
    }
