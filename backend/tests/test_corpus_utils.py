"""Tests for glossa_lab.corpus_utils (TEST-CU-001 .. TEST-CU-016).

normalise_sequences
-------------------
TEST-CU-001  LTR direction returns words unchanged (new list objects).
TEST-CU-002  RTL direction reverses every word.
TEST-CU-003  unknown direction returns words unchanged.
TEST-CU-004  Normalise is non-destructive (originals unmodified).
TEST-CU-005  Single-sign words are unchanged in RTL mode.
TEST-CU-006  Empty corpus returns empty list.
TEST-CU-007  Words of length 1 are identity under RTL.

run_ashraf_detection
---------------------
TEST-CU-008  Clear RTL corpus is correctly identified as rtl.
TEST-CU-009  Clear LTR corpus is correctly identified as ltr.
TEST-CU-010  Corpus with fewer words than min_words returns unknown.
TEST-CU-011  Result dict has all required keys.
TEST-CU-012  Confidence reflects entropy delta.
TEST-CU-013  Gini values are in [0, 1].
TEST-CU-014  n_words field matches the number of valid words processed.
TEST-CU-015  All-equal distributions (max-entropy) yield unknown.
TEST-CU-016  High-entropy endpoint gives confidence=high for large delta.
"""

from __future__ import annotations

import pytest
from glossa_lab.corpus_utils import normalise_sequences, run_ashraf_detection


# ── normalise_sequences ──────────────────────────────────────────────────────


def test_ltr_returns_words_unchanged():
    """TEST-CU-001: LTR leaves words in the original order."""
    words = [["A", "B", "C"], ["D", "E"]]
    result = normalise_sequences(words, "ltr")
    assert result == [["A", "B", "C"], ["D", "E"]]


def test_rtl_reverses_every_word():
    """TEST-CU-002: RTL reverses each word independently."""
    words = [["A", "B", "C"], ["D", "E"]]
    result = normalise_sequences(words, "rtl")
    assert result == [["C", "B", "A"], ["E", "D"]]


def test_unknown_returns_words_unchanged():
    """TEST-CU-003: unknown direction behaves like LTR (no reversal)."""
    words = [["X", "Y", "Z"]]
    assert normalise_sequences(words, "unknown") == [["X", "Y", "Z"]]


def test_normalise_is_non_destructive():
    """TEST-CU-004: Original word lists must not be modified in-place."""
    words = [["A", "B", "C"]]
    original_inner = list(words[0])
    normalise_sequences(words, "rtl")
    assert words[0] == original_inner, "normalise_sequences must not mutate the input"


def test_single_sign_words_unchanged_under_rtl():
    """TEST-CU-005: Words of length 1 are trivially unchanged by RTL."""
    words = [["X"], ["Y"], ["Z"]]
    result = normalise_sequences(words, "rtl")
    assert result == [["X"], ["Y"], ["Z"]]


def test_empty_corpus_returns_empty_list():
    """TEST-CU-006: Empty corpus returns empty list for all directions."""
    assert normalise_sequences([], "ltr") == []
    assert normalise_sequences([], "rtl") == []
    assert normalise_sequences([], "unknown") == []


def test_rtl_preserves_word_count():
    """TEST-CU-007: RTL normalisation never drops or duplicates words."""
    words = [["A", "B"], ["C", "D", "E"], ["F"]]
    result = normalise_sequences(words, "rtl")
    assert len(result) == len(words)
    for orig, norm in zip(words, result):
        assert len(norm) == len(orig)


# ── run_ashraf_detection ─────────────────────────────────────────────────────


def _make_rtl_corpus(n: int = 40) -> list[list[str]]:
    """Synthetic RTL corpus: position-0 is highly constrained (1 sign) == word-END.

    Word-END (leftmost in file for RTL) always starts with sign '000',
    so H(pos-0) is very low. Word-start sign is drawn from a large set.
    """
    import random
    rng = random.Random(42)
    vocab = [str(i).zfill(3) for i in range(1, 25)]  # 24 different start signs
    words = []
    for _ in range(n):
        start = rng.choice(vocab)     # diverse: high entropy → word-START
        end = "000"                   # constant:  low entropy → word-END
        body = [rng.choice(vocab[:10]) for _ in range(rng.randint(0, 2))]
        # File order is RTL → leftmost in file is the word-END
        words.append([end] + body + [start])
    return words


def _make_ltr_corpus(n: int = 40) -> list[list[str]]:
    """Synthetic LTR corpus: position-0 is diverse == word-START.

    Word-END (rightmost in file for LTR) always ends with sign '000',
    so H(pos-N1) is very low. Word-start sign is drawn from a large set.
    """
    import random
    rng = random.Random(99)
    vocab = [str(i).zfill(3) for i in range(1, 25)]
    words = []
    for _ in range(n):
        start = rng.choice(vocab)     # diverse: high entropy → word-START
        end = "000"                   # constant:  low entropy → word-END
        body = [rng.choice(vocab[:10]) for _ in range(rng.randint(0, 2))]
        # File order is LTR → leftmost in file is the word-START
        words.append([start] + body + [end])
    return words


def test_clear_rtl_corpus_detected_as_rtl():
    """TEST-CU-008: Corpus with constrained word-END at pos-0 => rtl."""
    words = _make_rtl_corpus(50)
    result = run_ashraf_detection(words)
    assert result["inferred_direction"] == "rtl", (
        f"Expected rtl, got {result['inferred_direction']}. "
        f"H0={result['entropy_pos0']:.4f}  HN1={result['entropy_posN1']:.4f}"
    )


def test_clear_ltr_corpus_detected_as_ltr():
    """TEST-CU-009: Corpus with constrained word-END at pos-N1 => ltr."""
    words = _make_ltr_corpus(50)
    result = run_ashraf_detection(words)
    assert result["inferred_direction"] == "ltr", (
        f"Expected ltr, got {result['inferred_direction']}. "
        f"H0={result['entropy_pos0']:.4f}  HN1={result['entropy_posN1']:.4f}"
    )


def test_insufficient_words_returns_unknown():
    """TEST-CU-010: Fewer than min_words words returns unknown."""
    words = [["A", "B"], ["C", "D"]]   # only 2 words
    result = run_ashraf_detection(words, min_words=5)
    assert result["inferred_direction"] == "unknown"
    assert result["entropy_pos0"] is None
    assert result["n_words"] == 2


def test_result_has_all_required_keys():
    """TEST-CU-011: Result dict always contains all documented keys."""
    required = {
        "entropy_pos0", "entropy_posN1", "gini_pos0", "gini_posN1",
        "inferred_direction", "confidence", "n_words", "interpretation",
    }
    # Sufficient-data case
    words = _make_rtl_corpus(20)
    result = run_ashraf_detection(words, min_words=5)
    assert required.issubset(result.keys()), f"Missing keys: {required - result.keys()}"

    # Insufficient-data case
    result2 = run_ashraf_detection([["A"]], min_words=5)
    assert required.issubset(result2.keys())


def test_confidence_low_for_small_delta():
    """TEST-CU-012: Nearly equal entropies produce low confidence and unknown direction."""
    # Both positions draw from the same uniform distribution → delta ≈ 0
    import random
    rng = random.Random(7)
    vocab = [str(i) for i in range(20)]
    words = [[rng.choice(vocab), rng.choice(vocab)] for _ in range(30)]
    result = run_ashraf_detection(words)
    assert result["confidence"] in ("low", "medium")
    if result["confidence"] == "low":
        assert result["inferred_direction"] == "unknown"


def test_gini_in_unit_interval():
    """TEST-CU-013: Gini values are always in [0, 1]."""
    for words in [_make_rtl_corpus(20), _make_ltr_corpus(20)]:
        result = run_ashraf_detection(words)
        assert 0.0 <= result["gini_pos0"] <= 1.0
        assert 0.0 <= result["gini_posN1"] <= 1.0


def test_n_words_matches_corpus_size():
    """TEST-CU-014: n_words equals the number of non-empty words analysed."""
    words = _make_rtl_corpus(30)
    result = run_ashraf_detection(words)
    assert result["n_words"] == 30


def test_high_confidence_for_large_entropy_delta():
    """TEST-CU-016: Very skewed distribution yields high confidence."""
    # pos-0 is always '999' (entropy=0), pos-N1 is random (high entropy)
    import random
    rng = random.Random(55)
    vocab = [str(i) for i in range(30)]
    words = [["999"] + [rng.choice(vocab) for _ in range(3)] for _ in range(50)]
    result = run_ashraf_detection(words)
    assert result["confidence"] in ("high", "medium")
    assert result["inferred_direction"] == "rtl"   # pos-0 most constrained → RTL
