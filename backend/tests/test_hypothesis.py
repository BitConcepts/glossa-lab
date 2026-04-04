"""Tests for the hypothesis-driven decipherment engine."""

from glossa_lab.pipelines.decipher import LanguageModel
from glossa_lab.pipelines.hypothesis import (
    Hypothesis,
    HypothesisEngine,
    score_internal_consistency,
    score_paradigm_regularity,
    score_word_matches,
)
from tests.corpora.cipher_language import generate_cipher_test_data


def _data():
    return generate_cipher_test_data(seed=42)


def test_hypothesis_engine_runs():
    """Engine should complete an iteration and return results."""
    data = _data()
    engine = HypothesisEngine(data["cipher"]["flat_signs"])

    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    hyp = Hypothesis(
        id="test-h1",
        name="Test hypothesis",
        target_language="test",
    )

    result = engine.test_hypothesis(
        hyp, target_model, max_iterations=3000, restarts=2,
    )
    assert result.hypothesis_id == "test-h1"
    assert result.total_score > 0
    assert len(result.mapping) > 0
    assert "bigram_ll" in result.scores


def test_hypothesis_tracks_history():
    """Engine should track hypothesis history."""
    data = _data()
    engine = HypothesisEngine(data["cipher"]["flat_signs"])
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    for i in range(3):
        hyp = Hypothesis(id=f"h{i}", name=f"Hyp {i}", target_language="test")
        engine.test_hypothesis(hyp, target_model, max_iterations=1000, restarts=1)

    assert engine.iteration == 3
    assert len(engine.history) == 3


def test_hypothesis_with_vocabulary():
    """Engine should score word matches against a vocabulary."""
    data = _data()
    engine = HypothesisEngine(data["cipher"]["flat_signs"])
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    # Create a vocabulary from the plaintext words
    vocab = {}
    for insc in data["plaintext"]["inscriptions"][:10]:
        for word in insc:
            vocab[word] = f"meaning of {word}"

    hyp = Hypothesis(id="h-vocab", name="Vocab test", target_language="test")
    result = engine.test_hypothesis(
        hyp, target_model, vocabulary=vocab,
        max_iterations=5000, restarts=3,
    )

    # Should have word match score
    assert "word_matches" in result.scores


def test_hypothesis_suggests_next():
    """Engine should generate suggestions for next hypotheses."""
    data = _data()
    engine = HypothesisEngine(data["cipher"]["flat_signs"])
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    hyp = Hypothesis(id="h-suggest", name="Suggest test", target_language="test")
    result = engine.test_hypothesis(
        hyp, target_model, max_iterations=3000, restarts=2,
    )
    assert len(result.suggested_next) > 0


def test_hypothesis_run_iteration():
    """run_iteration should test multiple hypotheses and rank them."""
    data = _data()
    engine = HypothesisEngine(data["cipher"]["flat_signs"])
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    hypotheses = [
        Hypothesis(id="h1", name="Hyp 1", target_language="test"),
        Hypothesis(id="h2", name="Hyp 2", target_language="test"),
    ]
    results = engine.run_iteration(
        hypotheses,
        {"test": target_model},
        max_iterations=2000,
    )
    assert len(results) == 2
    # Results should be sorted by score (best first)
    assert results[0].total_score >= results[1].total_score


def test_word_matches_scoring():
    """Word match scorer should find matches in vocabulary."""
    decoded = list("thecat")
    vocab = {"the": "article", "cat": "animal", "at": "preposition"}
    result = score_word_matches(decoded, vocab)
    assert result["match_count"] >= 1


def test_consistency_scoring():
    """Consistency scorer should return 1.0 for deterministic mappings."""
    mapping = {"A": "x", "B": "y", "C": "z"}
    signs = ["A", "B", "C", "A", "B", "C"]
    score = score_internal_consistency(mapping, signs)
    assert score == 1.0


def test_paradigm_regularity():
    """Paradigm regularity should be positive for structured data."""
    mapping = {"A": "x", "B": "x", "C": "x"}  # All map to same = very regular
    signs = ["A", "B", "C"] * 10
    score = score_paradigm_regularity(mapping, signs)
    assert score > 0
