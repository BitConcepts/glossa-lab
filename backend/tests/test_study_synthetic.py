"""Synthetic study — regression test for block entropy pipeline.

Uses deterministic synthetic corpora (seed=42) with known statistical
properties. Expected entropy ranges are fixed; any drift indicates a
bug in the entropy computation.
"""

from tests.corpora.synthetic import generate_markov, generate_ordered, generate_random

from glossa_lab.pipelines.block_entropy import compute_block_entropies


def _get_norm(result: dict, n: int) -> float:
    """Extract normalized entropy for block size n."""
    for entry in result["block_entropies"]:
        if entry["n"] == n:
            return entry["normalized"]
    raise ValueError(f"No entry for n={n}")


# ── Random (Max Entropy baseline) ────────────────────────────────────


def test_random_h1_near_maximum():
    """Random uniform sequence should have H1_norm ≈ 1.0."""
    symbols = generate_random()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    # Uniform over 26 symbols → H1 ≈ ln(26), normalized ≈ 1.0
    assert 0.98 <= h1 <= 1.02, f"H1_norm={h1}, expected ≈1.0"


def test_random_h2_near_maximum():
    """Random sequence: H2_norm should also be near maximum (~2.0)."""
    symbols = generate_random()
    result = compute_block_entropies(symbols, max_n=3)
    h2 = _get_norm(result, 2)
    # For independent uniform, H2 ≈ 2 * H1 → normalized ≈ 2.0
    assert 1.90 <= h2 <= 2.05, f"H2_norm={h2}, expected ≈2.0"


# ── Ordered (Min Entropy baseline) ───────────────────────────────────


def test_ordered_h1_uniform():
    """Ordered cycle uses all 26 symbols equally → H1_norm ≈ 1.0."""
    symbols = generate_ordered()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    # Cycle visits each letter equally
    assert 0.98 <= h1 <= 1.02, f"H1_norm={h1}, expected ≈1.0"


def test_ordered_h2_much_lower():
    """Ordered cycle: H2_norm << 2*H1 because bigrams are deterministic."""
    symbols = generate_ordered()
    result = compute_block_entropies(symbols, max_n=3)
    h2 = _get_norm(result, 2)
    # Only 26 distinct bigrams (AB, BC, ..., ZA) out of 676 possible
    # H2 = ln(26) → normalized = ln(26)/ln(26) = 1.0
    # This is much less than 2.0 (what random would give)
    assert h2 < 1.5, f"H2_norm={h2}, expected < 1.5 (deterministic bigrams)"


# ── Markov (Linguistic-like baseline) ────────────────────────────────


def test_markov_h1_mid_range():
    """Markov chain: H1_norm should be < 1.0 (non-uniform distribution)."""
    symbols = generate_markov()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    # Non-uniform due to biased transitions → some letters more frequent
    assert 0.85 <= h1 <= 1.0, f"H1_norm={h1}, expected 0.85-1.0"


def test_markov_sublinear_growth():
    """Markov chain: H2 < 2*H1 (sub-linear growth = linguistic signature)."""
    symbols = generate_markov()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    h2 = _get_norm(result, 2)
    ratio = h2 / h1
    # For independent symbols, ratio = 2.0. For correlated, ratio < 2.0.
    assert ratio < 1.95, f"H2/H1 ratio={ratio:.3f}, expected < 1.95"


def test_markov_deterministic():
    """Markov results must be identical across runs (seed=42)."""
    r1 = compute_block_entropies(generate_markov(), max_n=6)
    r2 = compute_block_entropies(generate_markov(), max_n=6)
    for e1, e2 in zip(r1["block_entropies"], r2["block_entropies"]):
        assert e1["normalized"] == e2["normalized"], "Non-deterministic!"
