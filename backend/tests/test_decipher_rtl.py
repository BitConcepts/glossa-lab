"""Tests for reading_direction parameter in the decipher pipeline (TEST-DR-001..008).

TEST-DR-001  LTR: cipher_inscriptions passed unchanged to pipeline.
TEST-DR-002  RTL: cipher_inscriptions reversed before processing.
TEST-DR-003  unknown: cipher_inscriptions passed unchanged (same as LTR).
TEST-DR-004  RTL: decipher() returns a proposed_mapping dict.
TEST-DR-005  RTL: proposed_mapping contains entries for all cipher signs.
TEST-DR-006  normalise_sequences is idempotent (normalise twice == normalise once).
TEST-DR-007  RTL with no cipher_inscriptions: does not crash.
TEST-DR-008  decipher reading_direction param accepts 'ltr', 'rtl', 'unknown'.
"""

from __future__ import annotations

import pytest
from glossa_lab.corpus_utils import normalise_sequences
from glossa_lab.pipelines.decipher import LanguageModel, decipher


# ── Helpers ──────────────────────────────────────────────────────────────────


def _small_lm() -> LanguageModel:
    """Build a minimal Hebrew-like language model for fast tests."""
    # 5 consonants, repeated to give meaningful bigram statistics
    symbols = list("abcdeabcdeabcde" * 20)
    inscriptions = [list(w) for w in ["abc", "bcd", "cde", "dea", "eab"] * 10]
    return LanguageModel(symbols, inscriptions=inscriptions)


def _cipher_words() -> list[list[str]]:
    """Small corpus of cipher words (sign IDs)."""
    return [
        ["001", "002", "003"],
        ["002", "004"],
        ["003", "001", "005"],
        ["004", "003", "002", "001"],
        ["005", "002"],
    ]


# ── normalise_sequences unit tests ───────────────────────────────────────────


def test_ltr_leaves_words_unchanged():
    """TEST-DR-001: LTR direction does not alter word order."""
    words = _cipher_words()
    normed = normalise_sequences(words, "ltr")
    for orig, norm in zip(words, normed):
        assert norm == orig


def test_rtl_reverses_word_order():
    """TEST-DR-002: RTL direction reverses each word."""
    words = [["001", "002", "003"], ["004", "005"]]
    normed = normalise_sequences(words, "rtl")
    assert normed[0] == ["003", "002", "001"]
    assert normed[1] == ["005", "004"]


def test_unknown_direction_same_as_ltr():
    """TEST-DR-003: unknown direction behaves identically to ltr."""
    words = _cipher_words()
    assert normalise_sequences(words, "unknown") == normalise_sequences(words, "ltr")


def test_normalise_rtl_idempotent_double_reversal():
    """TEST-DR-006: Normalising RTL twice (ltr then rtl) restores original."""
    words = _cipher_words()
    once = normalise_sequences(words, "rtl")
    twice = normalise_sequences(once, "rtl")
    for orig, final in zip(words, twice):
        assert final == orig


# ── decipher() integration tests ─────────────────────────────────────────────


def test_rtl_decipher_returns_mapping():
    """TEST-DR-004: decipher() with reading_direction='rtl' returns a mapping dict."""
    lm = _small_lm()
    cipher_words = _cipher_words()
    flat = [s for w in cipher_words for s in w]

    result = decipher(
        flat,
        lm,
        seed=1,
        max_iterations=500,
        restarts=2,
        cipher_inscriptions=cipher_words,
        surjective=True,
        reading_direction="rtl",
    )
    assert "proposed_mapping" in result
    assert isinstance(result["proposed_mapping"], dict)
    assert len(result["proposed_mapping"]) > 0


def test_rtl_decipher_maps_all_cipher_signs():
    """TEST-DR-005: Every distinct cipher sign appears in proposed_mapping."""
    lm = _small_lm()
    cipher_words = _cipher_words()
    flat = [s for w in cipher_words for s in w]
    signs = set(flat)

    result = decipher(
        flat,
        lm,
        seed=2,
        max_iterations=500,
        restarts=2,
        cipher_inscriptions=cipher_words,
        surjective=True,
        reading_direction="rtl",
    )
    mapping = result["proposed_mapping"]
    for sign in signs:
        assert sign in mapping, f"Sign {sign!r} missing from proposed_mapping"


def test_rtl_decipher_without_inscriptions_does_not_crash():
    """TEST-DR-007: reading_direction='rtl' with no cipher_inscriptions does not crash."""
    lm = _small_lm()
    flat = ["001", "002", "003", "001", "002"]
    # No cipher_inscriptions — RTL normalisation is a no-op
    result = decipher(
        flat,
        lm,
        seed=3,
        max_iterations=300,
        restarts=1,
        cipher_inscriptions=None,
        surjective=True,
        reading_direction="rtl",
    )
    assert "proposed_mapping" in result


@pytest.mark.parametrize("direction", ["ltr", "rtl", "unknown"])
def test_decipher_accepts_all_direction_values(direction):
    """TEST-DR-008: decipher() accepts ltr, rtl, and unknown without error."""
    lm = _small_lm()
    cipher_words = [["001", "002"], ["002", "003"]]
    flat = [s for w in cipher_words for s in w]

    result = decipher(
        flat,
        lm,
        seed=4,
        max_iterations=200,
        restarts=1,
        cipher_inscriptions=cipher_words,
        surjective=True,
        reading_direction=direction,
    )
    assert "proposed_mapping" in result
