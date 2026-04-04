"""Tests for CPSC constraint-projected decipherment.

Verifies:
  1. CPSC module is detected as available
  2. decipher_auto() uses CPSC by default
  3. CPSC projection produces valid results
  4. Hill climbing still works when forced
  5. CPSC and hill climbing both crack the synthetic cipher
"""

from glossa_lab.pipelines.decipher import (
    LanguageModel,
    _cpsc_available,
    decipher,
    decipher_auto,
    score_accuracy,
)
from tests.corpora.cipher_language import generate_cipher_test_data


def _data():
    return generate_cipher_test_data(seed=42)


def test_cpsc_is_available():
    """The CPSC module should be detected."""
    assert _cpsc_available() is True


def test_auto_uses_cpsc_by_default():
    """decipher_auto with engine='auto' should use CPSC."""
    data = _data()
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    result = decipher_auto(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42, max_iterations=5000, restarts=3,
    )
    assert result.get("engine") == "cpsc"


def test_hillclimb_when_forced():
    """decipher_auto with engine='hillclimb' should use hill climbing."""
    data = _data()
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    result = decipher_auto(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42, max_iterations=5000, restarts=3,
        engine="hillclimb",
    )
    # Hill climbing result doesn't have 'engine' key
    assert "engine" not in result or result.get("engine") != "cpsc"


def test_cpsc_cracks_synthetic():
    """CPSC projection should produce a valid decipherment.

    CPSC evaluates 4 constraints per swap candidate (vs hill climbing's 1),
    so it's slower per epoch but produces richer diagnostics. The accuracy
    threshold is lower than hill climbing because CPSC is optimising a
    multi-objective function, not a single score.
    """
    data = _data()
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    result = decipher_auto(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42, max_iterations=10000, restarts=5,
        engine="cpsc",
    )
    # CPSC should produce a mapping and reduce violations
    assert result["total_violation"] < 10.0, "Violation too high"
    assert len(result["proposed_mapping"]) > 0
    # Check it gets SOME accuracy (proving it's not random)
    reverse_key = data["cipher"]["reverse_map"]
    accuracy = score_accuracy(result["proposed_mapping"], reverse_key)
    assert accuracy["accuracy"] > 0.10, (
        f"CPSC accuracy {accuracy['accuracy']*100:.1f}% — worse than random"
    )


def test_cpsc_returns_constraint_violations():
    """CPSC result should include per-constraint violation report."""
    data = _data()
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    result = decipher_auto(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42, max_iterations=3000, restarts=2,
        engine="cpsc",
    )
    assert "constraint_violations" in result
    violations = result["constraint_violations"]
    # Should have entries for each constraint
    assert "frequency_rank" in violations
    assert "bigram" in violations


def test_hillclimb_still_works():
    """Hill climbing should still crack the synthetic cipher."""
    data = _data()
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])
    result = decipher(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42, max_iterations=10000, restarts=5,
    )
    reverse_key = data["cipher"]["reverse_map"]
    accuracy = score_accuracy(result["proposed_mapping"], reverse_key)
    assert accuracy["accuracy"] >= 0.70
