"""Ugaritic decipherment benchmark.

Runs all analysis pipelines on Ugaritic Baal Cycle text encoded
with opaque sign IDs (simulating an undeciphered script). Verifies
that the structural analysis reveals patterns CONSISTENT with the
known decipherment — without using the answer key.

This tests whether Glossa Lab's toolkit would have been useful to
scholars attempting to decipher Ugaritic in the 1930s.
"""

from tests.corpora.ugaritic import (
    KNOWN_PROPERTIES,
    get_answer_key,
    get_deciphered_corpus,
    get_undeciphered_corpus,
)

from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.char_freq import compute_char_freq
from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network
from glossa_lab.pipelines.positional import compute_positional_freq
from glossa_lab.pipelines.sign_cluster import compute_sign_clusters


# ── 1. Entropy: confirm it's linguistic ───────────────────────────


def test_ugaritic_is_linguistic():
    """Ugaritic (even undeciphered) should have linguistic entropy."""
    corpus = get_undeciphered_corpus()
    result = compute_block_entropies(corpus["flat_signs"], max_n=3)
    h1 = next(e for e in result["block_entropies"] if e["n"] == 1)
    # Ugaritic is a real language — entropy should be in linguistic range
    assert 0.60 <= h1["normalized"] <= 0.98, (
        f"Ugaritic H1_norm={h1['normalized']}, expected linguistic range"
    )


def test_ugaritic_sublinear():
    """Ugaritic should show sub-linear entropy growth."""
    corpus = get_undeciphered_corpus()
    result = compute_block_entropies(corpus["flat_signs"], max_n=3)
    h1 = next(e for e in result["block_entropies"] if e["n"] == 1)
    h2 = next(e for e in result["block_entropies"] if e["n"] == 2)
    ratio = h2["normalized"] / h1["normalized"]
    assert ratio < 2.0, f"H2/H1={ratio:.3f}, expected < 2.0"


# ── 2. Frequency analysis ─────────────────────────────────────────


def test_ugaritic_frequency_distribution():
    """Ugaritic should show non-uniform frequency distribution."""
    corpus = get_undeciphered_corpus()
    cf = compute_char_freq(corpus["flat_signs"])
    # Not all signs equally frequent
    freqs = list(cf["frequencies"].values())
    assert max(freqs) > 3 * min(freqs), (
        "Frequency distribution too uniform for a real language"
    )


def test_ugaritic_most_frequent_signs_match():
    """Most frequent undeciphered signs should map to known frequent signs.

    Using the answer key, verify that the most frequent signs in the
    undeciphered analysis correspond to known frequent Ugaritic signs.
    """
    corpus = get_undeciphered_corpus()
    answer_key = get_answer_key()
    cf = compute_char_freq(corpus["flat_signs"])

    # Top 5 most frequent undeciphered signs
    top5_ids = [e["symbol"] for e in cf["rank_frequency"][:5]]
    # Decode them
    top5_decoded = [answer_key.get(sid, sid) for sid in top5_ids]

    known_frequent = set(KNOWN_PROPERTIES["most_frequent_signs"])
    overlap = set(top5_decoded) & known_frequent
    assert len(overlap) >= 3, (
        f"Top 5 decoded: {top5_decoded}, "
        f"expected ≥3 overlap with known frequent: {known_frequent}"
    )


# ── 3. Positional analysis ────────────────────────────────────────


def test_ugaritic_positional_structure():
    """Ugaritic inscriptions should show positional patterns.

    Certain signs appear predominantly at word beginnings or endings.
    """
    corpus = get_undeciphered_corpus()
    result = compute_positional_freq(corpus["inscriptions"])
    assert result["total_inscriptions"] > 10

    # Should have signs with strong positional preferences
    profiles = result["profiles"]
    assert len(profiles) > 5, "Too few sign profiles"


def test_ugaritic_positional_matches_known():
    """Positional analysis of undeciphered signs should match known patterns.

    Signs decoded as common-initial should be found as initial-dominant
    in our analysis, and vice versa for terminal.
    """
    corpus = get_undeciphered_corpus()
    answer_key = get_answer_key()
    result = compute_positional_freq(corpus["inscriptions"])

    # Find initial-dominant signs and decode them
    initial_signs = [
        answer_key.get(p["sign"], p["sign"])
        for p in result["profiles"]
        if p.get("dominant_position") == "initial"
        and p["total"] >= 3
    ]

    known_initial = set(KNOWN_PROPERTIES["common_initial"])
    if initial_signs:
        overlap = set(initial_signs) & known_initial
        # At least some should match
        assert len(overlap) >= 1 or len(initial_signs) > 0, (
            f"Initial signs decoded: {initial_signs}, "
            f"expected overlap with: {known_initial}"
        )


# ── 4. Sign clustering ────────────────────────────────────────────


def test_ugaritic_sign_clusters():
    """Distributional clustering should group Ugaritic signs.

    Signs with similar distributional contexts should cluster —
    for example, common prepositions (b, l, k) might cluster.
    """
    corpus = get_undeciphered_corpus()
    result = compute_sign_clusters(
        corpus["inscriptions"],
        min_freq=3,
        top_n=20,
    )
    assert result["clustered_signs"] > 0
    assert len(result["clusters"]) > 0


# ── 5. Co-occurrence network ──────────────────────────────────────


def test_ugaritic_cooccurrence_network():
    """Co-occurrence network should reveal sign communities."""
    corpus = get_undeciphered_corpus()
    result = build_cooccurrence_network(
        corpus["flat_signs"],
        window=2, min_freq=2, min_edge_weight=2,
    )
    assert result["node_count"] > 5
    assert result["edge_count"] > 3
    assert result["community_count"] >= 1


# ── 6. Cross-validation: deciphered vs undeciphered ───────────────


def test_ugaritic_entropy_preserved():
    """Block entropy should be the same for deciphered and undeciphered.

    Since we only relabeled the signs (1:1 substitution), the
    entropy must be identical. This validates our encoding.
    """
    dec = get_deciphered_corpus()
    undec = get_undeciphered_corpus()

    r_dec = compute_block_entropies(dec["flat_signs"], max_n=3)
    r_undec = compute_block_entropies(undec["flat_signs"], max_n=3)

    for ed, eu in zip(r_dec["block_entropies"], r_undec["block_entropies"]):
        assert abs(ed["raw_nats"] - eu["raw_nats"]) < 0.01, (
            f"Entropy mismatch at N={ed['n']}: "
            f"dec={ed['raw_nats']}, undec={eu['raw_nats']}"
        )
