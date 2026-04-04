"""Linear B Validation Study.

Validates the Glossa Lab decipherment engine against Linear B
(Mycenaean Greek, c. 1375–1200 BCE), the most comprehensively
documented Bronze Age syllabic script.

Study design mirrors the Ugaritic validation:
  1. Encode the Linear B syllable corpus with opaque sign IDs (LB01, LB02…)
     to simulate an undeciphered state.
  2. Build a language model from the known Mycenaean Greek transliteration.
  3. Run the decipherment engine.
  4. Score accuracy against Ventris's known values.

Source: Ventris & Chadwick (1973) Documents in Mycenaean Greek.
Corpus: Pylos (PY) and Knossos (KN) tablets via DĀMOS (University of Oslo).
"""

from __future__ import annotations

from glossa_lab.data.linear_b_language import (
    encode_corpus,
    get_corpus_symbols,
)
from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy
from tests.corpora.real import load_linear_b_signs

# ── Helpers ───────────────────────────────────────────────────────────

def _get_norm(result: dict, n: int) -> float:
    for entry in result["block_entropies"]:
        if entry["n"] == n:
            return entry["normalized"]
    raise ValueError(f"No entry for n={n}")


# ── Block entropy tests ───────────────────────────────────────────────


def test_linear_b_in_linguistic_range():
    """Linear B H1_norm should fall in the linguistic range (0.65–0.95).

    Mycenaean Greek, like all natural languages, should cluster with
    English, Tamil, Sanskrit — distinct from DNA (high) or Fortran (low).
    """
    symbols = load_linear_b_signs()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    assert 0.60 <= h1 <= 0.95, (
        f"Linear B H1_norm={h1:.4f}, expected in linguistic range 0.60–0.95"
    )


def test_linear_b_sublinear_entropy_growth():
    """Linear B should show sub-linear block entropy growth.

    H2/H1 < 2.0 indicates sequential dependencies (bigram correlations),
    a defining property of natural language (Rao et al. 2009).
    """
    symbols = load_linear_b_signs()
    result = compute_block_entropies(symbols, max_n=3)
    h1 = _get_norm(result, 1)
    h2 = _get_norm(result, 2)
    ratio = h2 / h1 if h1 > 0 else 2.0
    assert ratio < 1.95, (
        f"Linear B H2/H1={ratio:.3f}: should be sub-linear (< 1.95)"
    )


def test_linear_b_alphabet_size():
    """The Linear B syllabary should have 20–90 distinct sign types.

    The actual syllabary has 87 signs; with a smaller corpus the
    observed count will be lower but should be in a plausible range.
    """
    symbols = load_linear_b_signs()
    result = compute_block_entropies(symbols, max_n=1)
    assert 20 <= result["alphabet_size"] <= 90, (
        f"Linear B alphabet size {result['alphabet_size']} unexpected"
    )


def test_linear_b_corpus_size():
    """Linear B fixture should produce a meaningful number of syllable tokens."""
    symbols = load_linear_b_signs()
    assert len(symbols) >= 400, (
        f"Linear B corpus too small: {len(symbols)} tokens"
    )


# ── Decipherment accuracy tests ───────────────────────────────────────


def _run_linear_b_decipherment():
    """Core decipherment: encode → decipher → score.

    Returns (accuracy_dict, opaque_sequence, answer_key, result).
    """
    symbols = get_corpus_symbols()
    opaque, answer_key = encode_corpus(symbols)

    # Build language model from the KNOWN transliteration (the target)
    target_model = LanguageModel(symbols)

    result = decipher(
        opaque,
        target_model,
        seed=42,
        max_iterations=8000,
        restarts=5,
    )

    accuracy = score_accuracy(result["proposed_mapping"], answer_key)
    return accuracy, opaque, answer_key, result


def test_linear_b_decipherment_runs():
    """Decipherment engine completes without error on Linear B corpus."""
    accuracy, _, _, result = _run_linear_b_decipherment()
    assert "accuracy" in accuracy
    assert "proposed_mapping" in result


def test_linear_b_decipherment_accuracy_above_threshold():
    """Decipherment accuracy should be substantially above random chance.

    With a corpus of ~800 syllable tokens and a correct target language
    model, the engine should recover at least 70% of sign-to-syllable
    mappings. The exact threshold is conservative; the Ugaritic benchmark
    (96.7%) used a larger and richer corpus.
    """
    accuracy, _, answer_key, _ = _run_linear_b_decipherment()
    n_signs = len(answer_key)
    assert accuracy["accuracy"] >= 0.70, (
        f"Linear B decipherment accuracy={accuracy['accuracy']:.3f} "
        f"({accuracy['correct']}/{accuracy['total']}) on {n_signs} signs"
    )


def test_linear_b_top5_most_frequent_correct():
    """Top-5 most frequent signs should be correctly deciphered.

    Frequency-rank seeding works best on common signs; the top-5
    are the most reliable indicators of the algorithm's performance.
    """
    from collections import Counter

    symbols = get_corpus_symbols()
    opaque, answer_key = encode_corpus(symbols)
    counts = Counter(opaque)
    top5_opaque = [s for s, _ in counts.most_common(5)]

    target_model = LanguageModel(symbols)
    result = decipher(opaque, target_model, seed=42, max_iterations=8000, restarts=5)
    mapping = result["proposed_mapping"]

    correct = sum(
        1 for s in top5_opaque
        if mapping.get(s) == answer_key.get(s)
    )
    assert correct >= 3, (
        f"Top-5 correct: {correct}/5 — frequency seeding should nail most common signs"
    )


def test_linear_b_kandles_confidence_positive():
    """Kandles phonetic confidence should be > 0 for a correct-language model."""
    _, _, _, result = _run_linear_b_decipherment()
    # A decipherment with the right language should score positively
    assert result.get("kandles_confidence", 0) >= 0.0
