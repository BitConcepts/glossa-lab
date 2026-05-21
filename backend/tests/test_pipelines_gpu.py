"""Tests for pipeline GPU/parallel compliance (TEST-PL-001..010).

TEST-PL-001  block_entropy compute_block_entropies returns N entries.
TEST-PL-002  block_entropy entries are sorted by n ascending.
TEST-PL-003  block_entropy entropy is non-negative.
TEST-PL-004  block_entropy normalized value in [0, 1].
TEST-PL-005  block_entropy parallel execution produces same result as sequential.
TEST-PL-006  cooccurrence build_cooccurrence_network returns nodes and edges.
TEST-PL-007  cooccurrence numpy path matches Python path for same input.
TEST-PL-008  cooccurrence returns community structure.
TEST-PL-009  _parallel.parallel_map runs all tasks and returns results.
TEST-PL-010  _parallel.parallel_map handles empty list.
"""
from __future__ import annotations

from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network

_SYMBOLS = list("abcdeabcdeabcde" * 30)   # 450 symbols
_LONG    = list("abcdeabcdeabcde" * 100)  # 1500 symbols (triggers numpy path)


# ── block_entropy ─────────────────────────────────────────────────────────────

def test_block_entropy_count():
    """TEST-PL-001: compute_block_entropies returns max_n entries."""
    r = compute_block_entropies(_SYMBOLS, max_n=4)
    assert len(r["block_entropies"]) == 4


def test_block_entropy_sorted():
    """TEST-PL-002: Entries are sorted by n ascending (parallel results reordered)."""
    r = compute_block_entropies(_SYMBOLS, max_n=4)
    ns = [e["n"] for e in r["block_entropies"]]
    assert ns == sorted(ns)


def test_block_entropy_non_negative():
    """TEST-PL-003: All entropy values are non-negative."""
    r = compute_block_entropies(_SYMBOLS, max_n=4)
    for e in r["block_entropies"]:
        assert e["raw_nats"] >= 0.0


def test_block_entropy_normalized_in_range():
    """TEST-PL-004: Normalized entropy is in [0, 1]."""
    r = compute_block_entropies(_SYMBOLS, max_n=3)
    for e in r["block_entropies"]:
        assert 0.0 <= e["normalized"] <= 1.01  # slight tolerance for float rounding


def test_block_entropy_parallel_matches_sequential():
    """TEST-PL-005: Parallel and sequential (fallback) produce identical results."""
    r1 = compute_block_entropies(_SYMBOLS, max_n=3)
    # Force sequential by patching parallel_map temporarily
    orig = None
    try:
        import glossa_lab.experiments._parallel as _pm
        orig = _pm.parallel_map

        def _seq_map(fn, args_list, max_workers=None):
            return [fn(*a) for a in args_list]

        _pm.parallel_map = _seq_map
        r2 = compute_block_entropies(_SYMBOLS, max_n=3)
    finally:
        if orig is not None:
            _pm.parallel_map = orig

    for e1, e2 in zip(r1["block_entropies"], r2["block_entropies"]):
        assert e1["n"] == e2["n"]
        assert abs(e1["raw_nats"] - e2["raw_nats"]) < 1e-9


# ── cooccurrence ──────────────────────────────────────────────────────────────

def test_cooccurrence_basic():
    """TEST-PL-006: build_cooccurrence_network returns nodes, edges, communities."""
    r = build_cooccurrence_network(_SYMBOLS, window=2, min_freq=2)
    assert "nodes" in r
    assert "edges" in r
    assert "communities" in r
    assert r["node_count"] > 0


def test_cooccurrence_numpy_matches_python():
    """TEST-PL-007: Numpy path and Python path produce same edge counts."""
    import glossa_lab.pipelines.cooccurrence as _co

    # Force Python path
    orig = _co._HAS_NUMPY
    try:
        _co._HAS_NUMPY = False
        r_py = build_cooccurrence_network(_LONG, window=2, min_freq=3)
    finally:
        _co._HAS_NUMPY = orig

    # Numpy path (if available)
    if orig:
        r_np = build_cooccurrence_network(_LONG, window=2, min_freq=3)
        assert r_np["edge_count"] == r_py["edge_count"]
        assert r_np["node_count"] == r_py["node_count"]
    else:
        # Can't test numpy path without numpy — just verify python path worked
        assert r_py["node_count"] > 0


def test_cooccurrence_community_count():
    """TEST-PL-008: Community detection returns at least 1 community."""
    r = build_cooccurrence_network(_SYMBOLS, window=2, min_freq=2)
    assert r["community_count"] >= 1
    assert len(r["communities"]) >= 1


# ── _parallel.parallel_map ────────────────────────────────────────────────────

def test_parallel_map_all_tasks():
    """TEST-PL-009: parallel_map runs all tasks and returns results."""
    from glossa_lab.experiments._parallel import parallel_map

    def _square(x: int) -> int:
        return x * x

    results = parallel_map(_square, [(1,), (2,), (3,), (4,)])
    assert sorted(results) == [1, 4, 9, 16]


def test_parallel_map_empty():
    """TEST-PL-010: parallel_map with empty list returns empty list."""
    from glossa_lab.experiments._parallel import parallel_map
    assert parallel_map(lambda x: x, []) == []
