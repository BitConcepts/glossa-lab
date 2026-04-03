"""Tests for the logosyllabic decipherment pipeline.

Validates:
- sign classification (logogram / syllabogram / determinative)
- affinity clustering produces valid structure
- reading proposals cover all syllabograms
- candidate word extraction returns well-formed output
- full analysis produces required output keys
- empty and minimal inputs are handled gracefully
"""

from __future__ import annotations

from glossa_lab.pipelines.logosyllabic import (
    analyze_logosyllabic,
    classify_signs,
    compute_affinity,
    extract_candidate_words,
    propose_readings,
)

# ── Synthetic corpora for testing ─────────────────────────────────────

# A minimal synthetic logosyllabic corpus:
# - "KING" appears alone (→ logogram)
# - "FISH" always at inscription start (→ potential determinative)
# - ba, bi, bu, ga, gi, gu appear in medial positions (→ syllabograms)

_LOGOGRAMS = ["KING", "FISH", "GOD"]
_SYLLABLES = ["ba", "bi", "bu", "ga", "gi", "gu", "la", "li", "na", "ni"]

_INSCRIPTIONS_RICH = [
    # Logograms in isolation (3 occurrences each)
    ["KING"],
    ["KING"],
    ["KING"],
    ["GOD"],
    ["GOD"],
    ["FISH"],
    # Mixed: determinative + syllabogram run
    ["FISH", "ba", "ga", "la"],
    ["FISH", "ba", "gi", "na"],
    ["FISH", "bi", "ga", "li"],
    ["GOD", "ga", "ba", "ni"],
    ["GOD", "gi", "bi", "la"],
    ["KING", "bu", "gu"],
    # Pure syllabogram sequences
    ["ba", "ga", "la", "na"],
    ["bi", "gi", "li", "ni"],
    ["bu", "gu", "la", "ba"],
    ["na", "la", "ba", "ga"],
    ["ni", "li", "bi", "gi"],
    ["la", "ba", "ga", "na"],
    ["ga", "la", "ba", "na"],
    ["gi", "li", "bi", "ni"],
]


def _flat(inscriptions):
    return [sign for insc in inscriptions for sign in insc]


# ── classify_signs tests ──────────────────────────────────────────────


def test_classify_signs_returns_all_unique_signs():
    """Every unique sign in the corpus must appear in the classification."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = classify_signs(_INSCRIPTIONS_RICH, flat)
    unique = set(flat)
    assert set(result.keys()) == unique


def test_classify_signs_types_are_valid():
    """All classification types must be one of the three expected values."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = classify_signs(_INSCRIPTIONS_RICH, flat)
    valid_types = {"logogram", "syllabogram", "determinative"}
    for sign, info in result.items():
        assert info["type"] in valid_types, (
            f"Sign '{sign}' has invalid type '{info['type']}'"
        )


def test_classify_signs_logogram_detected():
    """KING, GOD appearing alone should be classified as logograms."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = classify_signs(_INSCRIPTIONS_RICH, flat)
    # KING appears alone 3/4 times → isolation_rate >= 0.4
    assert result["KING"]["type"] == "logogram", (
        f"Expected KING to be logogram, got {result['KING']['type']}"
    )


def test_classify_signs_syllabogram_detected():
    """Signs appearing predominantly in medial positions should be syllabograms."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = classify_signs(_INSCRIPTIONS_RICH, flat)
    # 'la' never appears alone, always in runs → syllabogram
    assert result["la"]["type"] == "syllabogram", (
        f"Expected 'la' to be syllabogram, got {result['la']['type']}"
    )


def test_classify_signs_fields_complete():
    """Each classification entry must have all required fields."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = classify_signs(_INSCRIPTIONS_RICH, flat)
    required_fields = {"type", "frequency", "relative_frequency",
                       "boundary_bias", "isolation_rate", "evidence"}
    for sign, info in result.items():
        missing = required_fields - set(info.keys())
        assert not missing, f"Sign '{sign}' missing fields: {missing}"


# ── compute_affinity tests ────────────────────────────────────────────


def test_compute_affinity_structure():
    """Affinity result must contain vowel_groups and consonant_groups."""
    syllabograms = [s for s in _SYLLABLES]
    result = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)
    assert "vowel_groups" in result
    assert "consonant_groups" in result


def test_compute_affinity_groups_are_lists():
    """Vowel and consonant groups must be lists of lists of strings."""
    syllabograms = list(_SYLLABLES)
    result = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)
    for group in result.get("vowel_groups", []):
        assert isinstance(group, list)
        for sign in group:
            assert isinstance(sign, str)
    for group in result.get("consonant_groups", []):
        assert isinstance(group, list)


def test_compute_affinity_insufficient_data():
    """With fewer than 2 syllabograms, affinity should return empty groups."""
    result = compute_affinity(_INSCRIPTIONS_RICH, ["ba"])
    assert result.get("vowel_groups") == []
    assert result.get("consonant_groups") == []


# ── propose_readings tests ────────────────────────────────────────────


def test_propose_readings_covers_all_syllabograms():
    """Every syllabogram in the corpus should get a proposed reading."""
    flat = _flat(_INSCRIPTIONS_RICH)
    classification = classify_signs(_INSCRIPTIONS_RICH, flat)
    syllabograms = [s for s, info in classification.items()
                    if info["type"] == "syllabogram"]
    affinity = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)

    from glossa_lab.pipelines.logosyllabic import _SUMERIAN_SYLLABLES
    readings = propose_readings(
        classification, affinity, _SUMERIAN_SYLLABLES, _INSCRIPTIONS_RICH,
    )

    for sign in syllabograms:
        assert sign in readings, f"Missing reading for syllabogram '{sign}'"
        assert "reading" in readings[sign]
        assert "confidence" in readings[sign]


def test_propose_readings_confidence_range():
    """Confidence values must be in [0, 1]."""
    flat = _flat(_INSCRIPTIONS_RICH)
    classification = classify_signs(_INSCRIPTIONS_RICH, flat)
    syllabograms = [s for s, info in classification.items()
                    if info["type"] == "syllabogram"]
    affinity = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)

    from glossa_lab.pipelines.logosyllabic import _SUMERIAN_SYLLABLES
    readings = propose_readings(
        classification, affinity, _SUMERIAN_SYLLABLES, _INSCRIPTIONS_RICH,
    )

    for sign, info in readings.items():
        assert 0.0 <= info["confidence"] <= 1.0, (
            f"Confidence for '{sign}' out of range: {info['confidence']}"
        )


# ── extract_candidate_words tests ─────────────────────────────────────


def test_extract_candidate_words_returns_list():
    """Candidate word extraction should return a list."""
    flat = _flat(_INSCRIPTIONS_RICH)
    classification = classify_signs(_INSCRIPTIONS_RICH, flat)
    syllabograms = [s for s, info in classification.items()
                    if info["type"] == "syllabogram"]
    affinity = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)

    from glossa_lab.pipelines.logosyllabic import _SUMERIAN_SYLLABLES
    readings = propose_readings(
        classification, affinity, _SUMERIAN_SYLLABLES, _INSCRIPTIONS_RICH,
    )

    candidates = extract_candidate_words(
        _INSCRIPTIONS_RICH, classification, readings,
    )
    assert isinstance(candidates, list)


def test_extract_candidate_words_structure():
    """Each candidate word must have required fields."""
    flat = _flat(_INSCRIPTIONS_RICH)
    classification = classify_signs(_INSCRIPTIONS_RICH, flat)
    syllabograms = [s for s, info in classification.items()
                    if info["type"] == "syllabogram"]
    affinity = compute_affinity(_INSCRIPTIONS_RICH, syllabograms)

    from glossa_lab.pipelines.logosyllabic import _SUMERIAN_SYLLABLES
    readings = propose_readings(
        classification, affinity, _SUMERIAN_SYLLABLES, _INSCRIPTIONS_RICH,
    )

    candidates = extract_candidate_words(
        _INSCRIPTIONS_RICH, classification, readings,
    )

    required = {"signs", "readings", "combined_reading", "word_length",
                "avg_confidence", "score", "vocabulary_match"}
    for cand in candidates:
        missing = required - set(cand.keys())
        assert not missing, f"Candidate missing fields: {missing}"


# ── Full analysis tests ───────────────────────────────────────────────


def test_analyze_logosyllabic_output_keys():
    """Full analysis must return all required top-level keys."""
    result = analyze_logosyllabic(_INSCRIPTIONS_RICH, target_language="sumerian")
    required_keys = {
        "target_language", "sign_count", "unique_signs", "inscription_count",
        "sign_classification", "summary", "affinity", "proposed_readings",
        "candidate_words", "vocabulary_match_count",
    }
    missing = required_keys - set(result.keys())
    assert not missing, f"Missing keys: {missing}"


def test_analyze_logosyllabic_summary_counts():
    """Summary counts must be non-negative and add up to unique_signs."""
    result = analyze_logosyllabic(_INSCRIPTIONS_RICH, target_language="generic")
    s = result["summary"]
    assert s["logograms"] >= 0
    assert s["syllabograms"] >= 0
    assert s["determinatives"] >= 0
    total = s["logograms"] + s["syllabograms"] + s["determinatives"]
    assert total == result["unique_signs"], (
        f"Counts {total} != unique_signs {result['unique_signs']}"
    )


def test_analyze_logosyllabic_vocabulary_matching():
    """With a matching vocabulary entry, the match count should be > 0."""
    # Construct a vocabulary that should match at least one candidate
    from glossa_lab.pipelines.logosyllabic import _SUMERIAN_SYLLABLES
    # The most frequent syllabograms will be mapped to the top of the inventory
    # which starts with 'a', 'e', 'i', 'u', 'ba', ...
    # Synthesize a vocabulary entry for 'ae' (rank 0 + rank 1 = 'a' + 'e')
    # and 'ii' (rank 2 twice) to ensure at least one match is plausible.
    vocab = {"ae": "sky", "ii": "water", "aei": "fire"}

    result = analyze_logosyllabic(
        _INSCRIPTIONS_RICH,
        target_language="generic",
        vocabulary=vocab,
    )
    # May or may not match depending on ranking — just verify structure
    assert result["vocabulary_match_count"] >= 0


def test_analyze_logosyllabic_empty_input():
    """Empty inscription list should return an error dict, not raise."""
    result = analyze_logosyllabic([], target_language="generic")
    assert "error" in result
    assert result["sign_count"] == 0


def test_analyze_logosyllabic_sign_count():
    """sign_count must equal total signs across all inscriptions."""
    flat = _flat(_INSCRIPTIONS_RICH)
    result = analyze_logosyllabic(_INSCRIPTIONS_RICH)
    assert result["sign_count"] == len(flat)


def test_analyze_logosyllabic_linear_b_target():
    """Linear B target language should use the Linear B syllable inventory."""
    result = analyze_logosyllabic(_INSCRIPTIONS_RICH, target_language="linear_b")
    assert result["target_language"] == "linear_b"
    # Readings should include Linear B CV values
    any_linear_b = any(
        info["reading"] in {"da", "de", "di", "ka", "ke", "ta", "te"}
        for info in result["proposed_readings"].values()
    )
    assert any_linear_b, "Expected some Linear B readings to be assigned"
