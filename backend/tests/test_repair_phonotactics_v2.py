"""Regression tests for glossa_lab.phonotactics_v2 (repair WP2).

Each test names the old Phase 58 / provenance_audit defect it guards
against. The old defects were verified first-hand against the inspect
copies before these tests were written:

* the cleanup regex [^a-zāīūēō] deleted every retroflex, so "ṭa"
  became "a" and passed;
* uncheckable input returned True (PASS);
* slash alternatives were collapsed to the first segment;
* normalize_reading stripped all diacritics, collapsing ṭ/t, ḍ/d,
  ś/s and ṣ/s;
* an initials-only check fed a "VALID / 0 violations" headline.
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phonotactics_v2 import (  # noqa: E402
    PARSER_VERSION,
    RULES,
    SCOPE,
    AggregateResult,
    Outcome,
    check_reading,
    check_readings,
)

FORBIDDEN_READINGS = ["ṭa", "ḍa", "ṇa", "ḷa", "ṟa", "ṉa"]


# ---- declared prohibited-initial rule --------------------------------

@pytest.mark.parametrize("reading", FORBIDDEN_READINGS)
def test_each_prohibited_initial_triggers_the_declared_rule(reading):
    result = check_reading(reading)
    assert result.outcome is Outcome.VIOLATION
    assert len(result.alternatives) == 1
    alt = result.alternatives[0]
    assert alt.outcome is Outcome.VIOLATION
    assert "prohibited-initial-retroflex" in alt.rules_violated
    # The retroflex itself, not a stripped substitute, is the initial.
    assert alt.initial == reading[0]
    assert alt.normalized == reading


@pytest.mark.parametrize("reading", FORBIDDEN_READINGS)
def test_prohibited_initial_single_character_also_violates(reading):
    # The single retroflex alone is a complete (checkable) initial.
    single = reading[0]
    assert check_reading(single).outcome is Outcome.VIOLATION


def test_rule_set_is_data_with_id_description_and_enabled_flag():
    assert PARSER_VERSION
    assert RULES, "the declared rule set must not be empty"
    for rule in RULES:
        assert rule.id
        assert rule.description
        assert isinstance(rule.enabled, bool)
    enabled_ids = [r.id for r in RULES if r.enabled]
    assert "prohibited-initial-retroflex" in enabled_ids


def test_disabling_the_rule_as_data_changes_the_outcome():
    disabled = tuple(
        type(r)(
            id=r.id,
            description=r.description,
            enabled=False,
            forbidden_initials=r.forbidden_initials,
        )
        for r in RULES
    )
    result = check_reading("ṭa", rules=disabled)
    assert result.outcome is Outcome.PASS
    assert result.alternatives[0].rules_checked == ()


# ---- permitted examples pass only the specified rule ------------------

def test_permitted_example_passes_only_the_specified_rule():
    result = check_reading("ka")
    assert result.outcome is Outcome.PASS
    alt = result.alternatives[0]
    assert alt.outcome is Outcome.PASS
    assert alt.rules_checked == ("prohibited-initial-retroflex",)
    assert alt.rules_violated == ()
    # The reason must bound the pass to the specified rule and scope.
    reason_text = " ".join(alt.reasons)
    assert "only the specified rule" in reason_text


def test_vowel_initial_passes_the_declared_rule():
    assert check_reading("a").outcome is Outcome.PASS
    assert check_reading("ā").outcome is Outcome.PASS


def test_plain_t_is_not_the_retroflex():
    # Diacritics are not stripped: t-initial is a different initial
    # from ṭ-initial and does not break the retroflex rule.
    assert check_reading("ta").outcome is Outcome.PASS
    assert check_reading("ṭa").outcome is Outcome.VIOLATION
    assert check_reading("da").outcome is Outcome.PASS
    assert check_reading("ḍa").outcome is Outcome.VIOLATION


# ---- uncheckable input is never PASS ----------------------------------

@pytest.mark.parametrize(
    "reading",
    [
        "",
        "   ",
        "!!!",
        "123",
        "(fish)",          # annotation-only
        "(a gloss)",       # annotation-only, with a space
        "k*a",             # unrecognized character in the middle
        "ča",              # letter outside the recognized inventory
        "ṛa",              # letter outside the declared inventory
        "ka-",             # punctuation is not deleted to force a pass
        "ka/",             # empty second alternative
        "/ka",             # empty first alternative
        "ka//ki",          # empty middle alternative
        "(unclosed ka",    # malformed annotation
        "()",              # empty annotation, no reading
    ],
)
def test_uncheckable_input_is_never_pass(reading):
    result = check_reading(reading)
    assert result.outcome is not Outcome.PASS
    assert result.outcome is Outcome.UNCHECKABLE or any(
        a.outcome is Outcome.UNCHECKABLE for a in result.alternatives
    )
    assert all(a.reasons for a in result.alternatives)


@pytest.mark.parametrize("reading", [None, 42, 3.5, ["ka"], {"reading": "ka"}])
def test_non_text_input_is_uncheckable_not_pass(reading):
    result = check_reading(reading)
    assert result.outcome is Outcome.UNCHECKABLE


def test_annotation_only_records_the_annotation():
    result = check_reading("(fish)")
    assert result.outcome is Outcome.UNCHECKABLE
    assert result.annotations == ("fish",)
    assert result.alternatives[0].annotations == ("fish",)


# ---- Unicode: composed and decomposed behave identically --------------

@pytest.mark.parametrize("reading", FORBIDDEN_READINGS + ["ka", "ā", "śa", "ṇi"])
def test_composed_and_decomposed_forms_behave_identically(reading):
    composed = unicodedata.normalize("NFC", reading)
    decomposed = unicodedata.normalize("NFD", reading)
    r_composed = check_reading(composed)
    r_decomposed = check_reading(decomposed)
    assert r_composed.outcome is r_decomposed.outcome
    assert [a.normalized for a in r_composed.alternatives] == [
        a.normalized for a in r_decomposed.alternatives
    ]
    assert [a.outcome for a in r_composed.alternatives] == [
        a.outcome for a in r_decomposed.alternatives
    ]


def test_uppercase_input_is_checked_as_its_lowercase_initial():
    assert check_reading("ṬA").outcome is Outcome.VIOLATION
    assert check_reading("KA").outcome is Outcome.PASS


# ---- slash alternatives keep distinct outcomes -------------------------

def test_alternative_readings_retain_distinct_outcomes():
    result = check_reading("ṭa/ka")
    assert len(result.alternatives) == 2
    first, second = result.alternatives
    assert first.alternative.strip() == "ṭa"
    assert first.outcome is Outcome.VIOLATION
    assert second.alternative.strip() == "ka"
    assert second.outcome is Outcome.PASS
    # The whole reading is not collapsed to the first segment, and the
    # first segment's violation is not hidden by the second's pass.
    assert result.outcome is Outcome.VIOLATION


def test_alternative_order_does_not_change_individual_outcomes():
    result = check_reading("ka/ṭa")
    assert [a.outcome for a in result.alternatives] == [
        Outcome.PASS,
        Outcome.VIOLATION,
    ]


def test_uncheckable_alternative_does_not_hide_a_violation():
    result = check_reading("ṭa/*")
    assert [a.outcome for a in result.alternatives] == [
        Outcome.VIOLATION,
        Outcome.UNCHECKABLE,
    ]
    assert result.outcome is Outcome.VIOLATION


# ---- annotations are recorded, not silently dropped --------------------

def test_annotation_is_recorded_and_the_reading_is_still_checked():
    result = check_reading("ka (fish)")
    assert result.annotations == ("fish",)
    assert result.alternatives[0].annotations == ("fish",)
    assert result.outcome is Outcome.PASS

    violating = check_reading("ṭa (a gloss)")
    assert violating.annotations == ("a gloss",)
    assert violating.outcome is Outcome.VIOLATION


# ---- initials-only scope labeling ---------------------------------------

def test_every_result_is_labeled_initials_only():
    for reading in ["ka", "ṭa", "", "ṭa/ka", "(fish)"]:
        result = check_reading(reading)
        assert result.scope == "INITIALS-ONLY"
        assert result.scope == SCOPE
        assert "not" in result.scope_note.lower()
        assert "complete phonotactic" in result.scope_note
        for alt in result.alternatives:
            assert alt.scope == "INITIALS-ONLY"
            assert alt.parser_version == PARSER_VERSION
        as_dict = result.to_dict()
        assert as_dict["scope"] == "INITIALS-ONLY"


def test_no_result_claims_a_complete_phonotactic_assessment():
    result = check_reading("ka")
    text = str(result.to_dict()).lower()
    assert "initials-only" in text
    # A PASS here must not be worded as a complete assessment verdict.
    assert "complete phonotactic assessment: pass" not in text


# ---- denominator-preserving aggregate -----------------------------------

def test_aggregate_reports_checked_violations_and_uncheckable():
    agg = check_readings(["ṭa", "ka", "", "ki", "ča"])
    assert isinstance(agg, AggregateResult)
    assert agg.n_readings == 5
    assert agg.total == 5
    assert agg.violations == 1
    assert agg.passed == 2
    assert agg.uncheckable == 2
    # Checked excludes the uncheckable; nothing is silently dropped
    # and uncheckable items are not folded into PASS.
    assert agg.checked == agg.passed + agg.violations == 3
    assert agg.checked + agg.uncheckable == agg.total
    assert agg.scope == "INITIALS-ONLY"
    as_dict = agg.to_dict()
    for key in ("total", "checked", "passed", "violations", "uncheckable"):
        assert key in as_dict


def test_aggregate_counts_alternatives_individually():
    agg = check_readings(["ṭa/ka", "a"])
    assert agg.total == 3
    assert agg.violations == 1
    assert agg.passed == 2
    assert agg.uncheckable == 0


def test_aggregate_with_no_violations_still_reports_uncheckable():
    # The old headline pattern was "0 violations" presented as VALID.
    # Here a zero violation count is only meaningful alongside the
    # uncheckable count and the initials-only scope.
    agg = check_readings(["ka", ""])
    assert agg.violations == 0
    assert agg.uncheckable == 1
    assert agg.scope == "INITIALS-ONLY"
