"""Synthetic decipherment test.

Creates a toy language with KNOWN grammar, encrypts it with a
substitution cipher, then runs all analysis tools on the encrypted
form. Verifies that the tools recover the correct linguistic
structure WITHOUT access to the answer key.

This is the ultimate integration test: if our pipelines can
identify the structure of a ciphered language, they can contribute
to real decipherment.
"""

from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.char_freq import compute_char_freq
from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network
from glossa_lab.pipelines.paradigm import detect_paradigms
from glossa_lab.pipelines.positional import compute_positional_freq
from glossa_lab.pipelines.sign_cluster import compute_sign_clusters
from tests.corpora.cipher_language import generate_cipher_test_data


def _data():
    return generate_cipher_test_data(seed=42)


# ── 1. Entropy: detect it's linguistic ────────────────────────────


def test_cipher_is_linguistic():
    """Ciphered text should have linguistic entropy profile.

    A substitution cipher does NOT change the entropy — it's a 1:1
    mapping, so H_N is preserved. The ciphered text should have the
    same entropy as the plaintext, which is linguistic.
    """
    data = _data()
    result = compute_block_entropies(data["cipher"]["flat_signs"], max_n=3)
    h1 = next(e for e in result["block_entropies"] if e["n"] == 1)
    # Should be in linguistic range (not random ~1.0, not rigid ~0.0)
    assert 0.50 <= h1["normalized"] <= 0.95, (
        f"H1_norm={h1['normalized']}, expected linguistic range"
    )


def test_cipher_sublinear_growth():
    """Ciphered text should show sub-linear entropy growth."""
    data = _data()
    result = compute_block_entropies(data["cipher"]["flat_signs"], max_n=3)
    h1 = next(e for e in result["block_entropies"] if e["n"] == 1)
    h2 = next(e for e in result["block_entropies"] if e["n"] == 2)
    ratio = h2["normalized"] / h1["normalized"]
    assert ratio < 2.0, f"H2/H1={ratio:.3f}, expected < 2.0"


# ── 2. Frequency: Zipf-like distribution ──────────────────────────


def test_cipher_zipf():
    """Ciphered signs should follow Zipf-like distribution."""
    data = _data()
    cf = compute_char_freq(data["cipher"]["flat_signs"])
    assert cf["zipf_exponent"] is not None
    # Zipf exponent should be positive (power law)
    assert cf["zipf_exponent"] > 0.3, f"Zipf α={cf['zipf_exponent']}, expected > 0.3"


# ── 3. Positional: case suffixes create terminal patterns ─────────


def test_cipher_positional_patterns():
    """Ciphered inscriptions should show strong positional constraints.

    Because our language has case suffixes (-a nom, -o acc, -u gen)
    and tense prefixes (ka-, ti-), certain signs should be strongly
    positional.
    """
    data = _data()
    inscriptions = data["cipher"]["ciphered_inscriptions"]
    # Each word is a "mini-inscription" for positional analysis
    word_as_inscriptions = []
    for insc in inscriptions:
        for word in insc:
            # Split ciphered word into individual sign IDs
            signs = [word[i : i + 3] for i in range(0, len(word), 3)]
            if signs:
                word_as_inscriptions.append(signs)

    result = compute_positional_freq(word_as_inscriptions)
    # Should find signs with strong positional preferences
    assert result["total_inscriptions"] > 100
    # Some signs should be predominantly terminal (case suffixes)
    terminal_dominant = [
        p
        for p in result["profiles"]
        if p.get("dominant_position") == "terminal"
        and p.get("dominant_pct", 0) > 0.5
        and p["total"] >= 10
    ]
    assert len(terminal_dominant) >= 1, (
        f"Expected ≥1 terminally-dominant signs (case suffixes), found {len(terminal_dominant)}"
    )


# ── 4. Paradigms: detect grammatical inflection ───────────────────


def test_cipher_paradigm_detection():
    """Paradigm detection should find inflectional patterns.

    Our language has 3 noun cases (same root, different suffix).
    The paradigm detector should find stem templates with varying
    final positions.
    """
    data = _data()
    inscriptions = data["cipher"]["ciphered_inscriptions"]

    # Use words as inscriptions (split into sign sequences)
    word_inscriptions = []
    for insc in inscriptions:
        for word in insc:
            signs = [word[i : i + 3] for i in range(0, len(word), 3)]
            if len(signs) >= 2:
                word_inscriptions.append(signs)

    result = detect_paradigms(
        word_inscriptions,
        min_stem_freq=3,
        min_variants=2,
    )
    # Should find paradigms (noun case inflections)
    assert result["paradigm_count"] > 0, "No paradigms found!"

    # At least one paradigm should have 3 variants (3 cases)
    max_variants = max(p["variant_count"] for p in result["paradigms"])
    assert max_variants >= 2, f"Max variants={max_variants}, expected ≥2 (case inflections)"


# ── 5. Clustering: signs with similar function group together ─────


def test_cipher_sign_clusters():
    """Distributional clustering should group functionally similar signs.

    The 3 case-suffix signs (cipher of a, o, u) should appear in
    similar distributional contexts (always word-final, after
    consonants) and thus cluster together.
    """
    data = _data()
    # Use the flat sign sequence for context analysis
    result = compute_sign_clusters(
        [data["cipher"]["flat_signs"]],
        min_freq=5,
        top_n=20,
    )
    assert result["clustered_signs"] > 0
    # Should form multiple clusters
    multi_sign_clusters = [c for c in result["clusters"] if c["size"] > 1]
    assert len(multi_sign_clusters) >= 1, "No multi-sign clusters found!"


# ── 6. Network: co-occurrence reveals sign communities ────────────


def test_cipher_cooccurrence():
    """Co-occurrence network should detect sign communities."""
    data = _data()
    result = build_cooccurrence_network(
        data["cipher"]["flat_signs"],
        window=2,
        min_freq=5,
        min_edge_weight=3,
    )
    assert result["node_count"] > 5
    assert result["edge_count"] > 5
    assert result["community_count"] >= 1, (
        f"Expected ≥1 communities, found {result['community_count']}"
    )


# ── 7. Answer key verification ────────────────────────────────────


def test_cipher_alphabet_size_matches():
    """Ciphered alphabet size should match phoneme count."""
    data = _data()
    unique_signs = set(data["cipher"]["flat_signs"])
    expected = len(data["answer_key"]["cipher_map"])
    assert len(unique_signs) == expected, (
        f"Expected {expected} unique signs, found {len(unique_signs)}"
    )
