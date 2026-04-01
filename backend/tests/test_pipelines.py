"""Tests for Kandles, positional, sign clustering, paradigm, and co-occurrence pipelines."""

from glossa_lab.pipelines.kandles import (
    classify_word,
    color_code_text,
    compare_grids,
    generate_grid,
)
from glossa_lab.pipelines.positional import compute_positional_freq
from glossa_lab.pipelines.sign_cluster import compute_sign_clusters
from glossa_lab.pipelines.paradigm import detect_paradigms
from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network


# ── Kandles ───────────────────────────────────────────────────────


def test_kandles_k_group():
    """K, G, J, Ch → group 1 Yellow."""
    assert classify_word("cat")["group"] == 1
    assert classify_word("go")["group"] == 1
    assert classify_word("just")["group"] == 1
    assert classify_word("church")["group"] == 1  # CH digraph


def test_kandles_m_group():
    """M, N → group 2 Grey."""
    assert classify_word("moon")["group"] == 2
    assert classify_word("night")["group"] == 2


def test_kandles_t_group():
    """T, D, Th → group 3 Red."""
    assert classify_word("tree")["group"] == 3
    assert classify_word("day")["group"] == 3
    assert classify_word("the")["group"] == 3  # TH digraph


def test_kandles_r_group():
    """R, L → group 4 Blue."""
    assert classify_word("river")["group"] == 4
    assert classify_word("lake")["group"] == 4


def test_kandles_y_group():
    """Y, W, H → group 5 Green."""
    assert classify_word("water")["group"] == 5
    assert classify_word("year")["group"] == 5
    assert classify_word("house")["group"] == 5


def test_kandles_p_group():
    """P, B, F, V → group 6 Purple."""
    assert classify_word("fire")["group"] == 6
    assert classify_word("peace")["group"] == 6
    assert classify_word("bird")["group"] == 6
    assert classify_word("voice")["group"] == 6


def test_kandles_s_group():
    """S, Z, Sh → group 7 Brown."""
    assert classify_word("sun")["group"] == 7
    assert classify_word("zero")["group"] == 7
    assert classify_word("shine")["group"] == 7  # SH digraph


def test_kandles_vowel_group():
    """Vowel-initial → group 0 White."""
    assert classify_word("apple")["group"] == 0
    assert classify_word("earth")["group"] == 0
    assert classify_word("ice")["group"] == 0


def test_kandles_color_code_text():
    """Color-code produces correct length and groups."""
    words = ["The", "cat", "sat", "on", "the", "mat"]
    coded = color_code_text(words)
    assert len(coded) == 6
    assert coded[0]["group"] == 3  # The → T group (TH digraph → Red)
    assert coded[1]["group"] == 1  # cat → K group → Yellow


def test_kandles_grid_dimensions():
    """Grid should be square with ceil(sqrt(n)) sides."""
    words = ["a"] * 36
    grid = generate_grid(words)
    assert grid["grid_size"] == 6
    assert len(grid["grid"]) == 6
    assert len(grid["grid"][0]) == 6


def test_kandles_grid_small():
    """Small input produces valid grid."""
    words = ["cat", "dog", "sun"]
    grid = generate_grid(words)
    assert grid["grid_size"] == 2  # ceil(sqrt(3)) = 2
    assert grid["total_words"] == 3


def test_kandles_compare_same():
    """Comparing identical grids gives similarity ≈ 1.0."""
    words = ["cat", "dog", "sun", "moon"]
    ga = generate_grid(words)
    gb = generate_grid(words)
    result = compare_grids(ga, gb)
    assert result["similarity"] >= 0.99


def test_kandles_compare_different():
    """Comparing different texts gives similarity < 1.0."""
    ga = generate_grid(["cat", "cat", "cat", "cat"])
    gb = generate_grid(["sun", "sun", "sun", "sun"])
    result = compare_grids(ga, gb)
    assert result["similarity"] < 0.5


# ── Positional ───────────────────────────────────────────────────


def test_positional_basic():
    """Positional analysis produces correct counts."""
    inscriptions = [
        ["A", "B", "C"],
        ["A", "D", "C"],
        ["A", "E", "C"],
    ]
    result = compute_positional_freq(inscriptions)
    assert result["total_inscriptions"] == 3
    # A is always initial
    a_profile = next(p for p in result["profiles"] if p["sign"] == "A")
    assert a_profile["initial"] == 3
    assert a_profile["terminal"] == 0
    # C is always terminal
    c_profile = next(p for p in result["profiles"] if p["sign"] == "C")
    assert c_profile["terminal"] == 3
    assert c_profile["initial"] == 0


def test_positional_exclusive():
    """Exclusively terminal signs are identified."""
    inscriptions = [
        ["X", "Y", "Z"],
        ["A", "B", "Z"],
        ["C", "D", "Z"],
    ]
    result = compute_positional_freq(inscriptions)
    assert "Z" in result["exclusively_terminal"]


# ── Sign clustering ──────────────────────────────────────────────


def test_sign_cluster_basic():
    """Sign clustering produces clusters."""
    # A and B always appear in same context (before C)
    inscriptions = [
        ["A", "C", "D", "E"],
        ["B", "C", "D", "E"],
        ["A", "C", "F", "E"],
        ["B", "C", "F", "E"],
    ] * 5  # Repeat for frequency
    result = compute_sign_clusters(inscriptions, min_freq=2, top_n=10)
    assert result["clustered_signs"] > 0
    assert len(result["clusters"]) > 0


def test_sign_cluster_similarity():
    """Similar signs should have high similarity."""
    inscriptions = [
        ["X", "A", "Y"],
        ["X", "B", "Y"],
    ] * 10
    result = compute_sign_clusters(inscriptions, min_freq=2, top_n=10)
    # A and B appear in identical contexts → should be similar
    pairs = result["similarity_pairs"]
    ab_pair = next(
        (p for p in pairs
         if {p["sign_a"], p["sign_b"]} == {"A", "B"}),
        None,
    )
    assert ab_pair is not None
    assert ab_pair["similarity"] > 0.5


# ── Paradigm detection ───────────────────────────────────────────


def test_paradigm_basic():
    """Paradigm detection finds inflectional patterns."""
    inscriptions = [
        ["A", "B", "C"],
        ["A", "B", "D"],
        ["A", "B", "E"],
    ]
    result = detect_paradigms(inscriptions, min_stem_freq=2, min_variants=2)
    assert result["paradigm_count"] > 0
    # Should find paradigm with stem [A, B, _] at position 2
    p = result["paradigms"][0]
    assert p["slot_position"] == 2
    assert set(p["variants"]) >= {"C", "D", "E"}


def test_paradigm_multiple_slots():
    """Paradigm detection works for different slot positions."""
    inscriptions = [
        ["X", "A", "Z"],
        ["X", "B", "Z"],
        ["X", "C", "Z"],
        ["Y", "A", "Z"],
        ["Y", "B", "Z"],
    ]
    result = detect_paradigms(inscriptions, min_stem_freq=2, min_variants=2)
    assert result["paradigm_count"] >= 2  # Slot 0 and slot 1 both vary


# ── Co-occurrence network ────────────────────────────────────────


def test_cooccurrence_basic():
    """Co-occurrence network produces nodes and edges."""
    symbols = ["A", "B", "C", "A", "B", "C", "A", "B"] * 10
    result = build_cooccurrence_network(
        symbols, window=2, min_freq=2, min_edge_weight=2,
    )
    assert result["node_count"] > 0
    assert result["edge_count"] > 0


def test_cooccurrence_communities():
    """Community detection groups co-occurring signs."""
    # Two clusters: (A,B,C) co-occur together, (X,Y,Z) co-occur together
    symbols = (
        ["A", "B", "C"] * 20 + ["X", "Y", "Z"] * 20
    )
    result = build_cooccurrence_network(
        symbols, window=2, min_freq=2, min_edge_weight=2,
    )
    assert result["community_count"] >= 2


def test_cooccurrence_edge_weights():
    """More frequent co-occurrences have higher edge weights."""
    symbols = ["A", "B"] * 50 + ["A", "C"] * 5
    result = build_cooccurrence_network(
        symbols, window=2, min_freq=2, min_edge_weight=2,
    )
    ab_edge = next(
        (e for e in result["edges"]
         if {e["source"], e["target"]} == {"A", "B"}),
        None,
    )
    ac_edge = next(
        (e for e in result["edges"]
         if {e["source"], e["target"]} == {"A", "C"}),
        None,
    )
    if ab_edge and ac_edge:
        assert ab_edge["weight"] > ac_edge["weight"]
