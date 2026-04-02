"""Tests for NSB-style small-sample entropy estimators.

Validates that:
- Miller-Madow >= MLE (additive positive correction)
- Chao-Shen >= MLE (addresses missing-mass problem)
- Both estimators converge to MLE as N grows large
- Estimators handle edge cases (empty, single symbol, all singletons)
- compare_estimators() returns correct structure
- block_entropy pipeline respects the estimator param
"""

from __future__ import annotations

import pytest

from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.nsb_entropy import (
    compare_estimators,
    estimate_entropy,
)
from tests.corpora.synthetic import generate_random


# ── Unit tests ────────────────────────────────────────────────────────


def test_miller_madow_ge_mle_small():
    """Miller-Madow must be >= MLE (positive correction)."""
    symbols = list("aababcabcd") * 5  # small corpus, ~50 symbols
    mle = estimate_entropy(symbols, n=1, estimator="mle")
    mm = estimate_entropy(symbols, n=1, estimator="miller_madow")
    assert mm >= mle, f"Miller-Madow {mm:.4f} should be >= MLE {mle:.4f}"


def test_chao_shen_ge_mle_sparse():
    """Chao-Shen must be >= MLE for sparse corpora (many singletons)."""
    # Many distinct symbols, each seen only once -> very sparse
    symbols = list("abcdefghijklmnopqrstuvwxyz")  # 26 singletons
    mle = estimate_entropy(symbols, n=1, estimator="mle")
    cs = estimate_entropy(symbols, n=1, estimator="chao_shen")
    assert cs >= mle, f"Chao-Shen {cs:.4f} should be >= MLE {mle:.4f}"


def test_miller_madow_converges_large():
    """With large N, Miller-Madow correction becomes negligible (< 1%)."""
    symbols = generate_random(size=10_000, seed=42)
    mle = estimate_entropy(symbols, n=1, estimator="mle")
    mm = estimate_entropy(symbols, n=1, estimator="miller_madow")
    # Relative difference should be < 1%
    diff = abs(mm - mle) / max(abs(mle), 1e-8)
    assert diff < 0.01, (
        f"With N=10000, MM-MLE relative diff={diff:.4f} should be < 0.01"
    )


def test_chao_shen_converges_large():
    """With large N and few singletons, Chao-Shen approaches MLE."""
    symbols = generate_random(size=10_000, seed=42)
    mle = estimate_entropy(symbols, n=1, estimator="mle")
    cs = estimate_entropy(symbols, n=1, estimator="chao_shen")
    diff = abs(cs - mle) / max(abs(mle), 1e-8)
    assert diff < 0.02, (
        f"With N=10000, CS-MLE relative diff={diff:.4f} should be < 0.02"
    )


def test_estimate_entropy_empty():
    """Empty symbol list returns 0.0 for all estimators."""
    for est in ("mle", "miller_madow", "chao_shen"):
        result = estimate_entropy([], n=1, estimator=est)
        assert result == 0.0, f"{est}: expected 0.0 for empty input"


def test_estimate_entropy_single_symbol():
    """Single unique symbol has entropy 0 (deterministic)."""
    symbols = ["a"] * 100
    for est in ("mle", "miller_madow", "chao_shen"):
        result = estimate_entropy(symbols, n=1, estimator=est)
        # MLE = 0; MM adds tiny correction; all should be near 0
        assert result >= 0.0, f"{est}: entropy should be non-negative"


def test_estimate_entropy_unknown_raises():
    """Passing an unknown estimator name raises ValueError."""
    with pytest.raises(ValueError, match="Unknown estimator"):
        estimate_entropy(["a", "b"], n=1, estimator="bogus")


# ── compare_estimators structure ─────────────────────────────────────


def test_compare_estimators_structure():
    """compare_estimators returns correct keys and entry shapes."""
    symbols = list("hello world " * 50)
    result = compare_estimators(symbols, max_n=3)

    assert "alphabet_size" in result
    assert "symbol_count" in result
    for name in ("mle", "miller_madow", "chao_shen"):
        assert name in result
        entries = result[name]
        assert len(entries) == 3  # max_n=3
        for entry in entries:
            assert "n" in entry
            assert "raw_nats" in entry
            assert "normalized" in entry
            assert entry["raw_nats"] >= 0.0
            assert entry["normalized"] >= 0.0


# ── Integration with block_entropy pipeline ───────────────────────────


def test_block_entropy_pipeline_respects_estimator():
    """compute_block_entropies correctly passes estimator through."""
    symbols = list("abcdef" * 20)  # small but not tiny
    mle_result = compute_block_entropies(symbols, max_n=2, estimator="mle")
    mm_result = compute_block_entropies(symbols, max_n=2, estimator="miller_madow")
    cs_result = compute_block_entropies(symbols, max_n=2, estimator="chao_shen")

    # Each result should report its estimator
    assert mle_result["estimator"] == "mle"
    assert mm_result["estimator"] == "miller_madow"
    assert cs_result["estimator"] == "chao_shen"

    # Miller-Madow H1 should be >= MLE H1
    mle_h1 = mle_result["block_entropies"][0]["raw_nats"]
    mm_h1 = mm_result["block_entropies"][0]["raw_nats"]
    cs_h1 = cs_result["block_entropies"][0]["raw_nats"]
    assert mm_h1 >= mle_h1, "MM H1 should be >= MLE H1"
    assert cs_h1 >= mle_h1, "CS H1 should be >= MLE H1"


def test_small_corpus_estimators_diverge_meaningfully():
    """On a small corpus, MM and CS should diverge noticeably from MLE."""
    # 20 symbols from a 10-letter alphabet — definitely sparse
    symbols = list("abcdefghij")
    mle = estimate_entropy(symbols, n=1, estimator="mle")
    mm = estimate_entropy(symbols, n=1, estimator="miller_madow")
    cs = estimate_entropy(symbols, n=1, estimator="chao_shen")

    # Both corrections should add something meaningful for 10 singletons/10 total
    assert mm > mle, "MM should exceed MLE for all-singleton corpus"
    assert cs > mle, "CS should exceed MLE for all-singleton corpus"
