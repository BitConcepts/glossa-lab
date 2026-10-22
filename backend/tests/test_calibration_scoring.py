"""Calibration scoring machinery tests.

All coder records in this file are synthetic fixtures fabricated for
the machinery. They are not transcriptions of any object, human or
machine, and no calibration object is coded here.
"""

from glossa_lab.calibration_scoring import Crosswalk, score_calibration


def _row(m_sign, p_sign, confidence="high", conflict="False",
         candidate_only="False"):
    return {
        "mahadevan_id": m_sign,
        "parpola_id": p_sign,
        "confidence": confidence,
        "conflict": conflict,
        "candidate_only": candidate_only,
    }


CROSSWALK = Crosswalk.from_rows(
    [
        _row("M342", "P324"),
        _row("M135", "P197"),
        _row("M161", "P085"),
        _row("M161", "P086"),
        _row("M050", "P043"),
        _row("M050", "P044"),
        _row("M006", "P013", confidence="low", conflict="True"),
        _row("M001", "P013", confidence="low", conflict="True"),
    ]
)

CALIBRATION = {
    "entries": [
        {
            "canonical_key": "fixture:clean",
            "reference_p_sequence": ["P324", "P197"],
        },
        {
            "canonical_key": "fixture:ambiguous",
            "reference_p_sequence": ["P086"],
        },
        {
            "canonical_key": "fixture:conflict-only",
            "reference_p_sequence": ["P013"],
        },
        {
            "canonical_key": "fixture:error",
            "reference_p_sequence": ["P324"],
        },
        {
            "canonical_key": "fixture:split",
            "reference_p_sequence": ["P043", "P044"],
        },
        {
            "canonical_key": "fixture:merge",
            "reference_p_sequence": ["P324"],
        },
    ]
}

CODER = {
    "records": [
        {"canonical_key": "fixture:clean", "m77_sequence": ["M342", "M135"]},
        {"canonical_key": "fixture:ambiguous", "m77_sequence": ["M161"]},
        {"canonical_key": "fixture:conflict-only", "m77_sequence": ["M006"]},
        {"canonical_key": "fixture:error", "m77_sequence": ["M135"]},
        {"canonical_key": "fixture:split", "m77_sequence": ["M050"]},
        {"canonical_key": "fixture:merge", "m77_sequence": ["M342", "M342"]},
    ]
}


def _by_key(report):
    return {row["canonical_key"]: row for row in report["objects"]}


def test_crosswalk_core_and_conflict_classification():
    assert CROSSWALK.core_candidates["M342"] == ("P324",)
    assert CROSSWALK.core_candidates["M161"] == ("P085", "P086")
    assert "M006" not in CROSSWALK.core_candidates
    assert CROSSWALK.mapping_for("M006")["reason"] == "conflict_register_only"
    assert CROSSWALK.mapping_for("M999")["reason"] == "unmapped_sign"


def test_clean_fixture_scores_as_exact_agreement():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:clean"
    ]
    assert row["agreements"] == 2
    assert row["errors"] == 0
    assert row["ambiguous_tokens"] == 0
    assert row["per_token_agreement"] == 1.0
    assert row["exact_sequence"] is True


def test_ambiguous_fixture_is_neither_agreement_nor_error():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:ambiguous"
    ]
    assert row["agreements"] == 0
    assert row["errors"] == 0
    assert row["ambiguous_tokens"] == 1
    assert row["per_token_agreement"] is None
    assert row["exact_sequence"] is False
    assert row["segments"][0]["reason"] == "core_one_to_many"


def test_conflict_only_fixture_is_ambiguous_not_a_silent_pick():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:conflict-only"
    ]
    assert row["agreements"] == 0
    assert row["errors"] == 0
    assert row["ambiguous_tokens"] == 1
    assert row["segments"][0]["reason"] == "conflict_register_only"


def test_error_fixture_scores_as_error():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:error"
    ]
    assert row["agreements"] == 0
    assert row["errors"] == 1
    assert row["ambiguous_tokens"] == 0
    assert row["per_token_agreement"] == 0.0
    assert row["exact_sequence"] is False


def test_split_segment_is_reported_ambiguous_at_the_mapping_layer():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:split"
    ]
    assert row["agreements"] == 0
    assert row["errors"] == 0
    assert row["ambiguous_tokens"] == 2
    assert row["segments"][0]["operation"] == "split"


def test_merge_segment_contracts_two_m_tokens_to_one_reference_sign():
    row = _by_key(score_calibration(CALIBRATION, CODER, CROSSWALK))[
        "fixture:merge"
    ]
    assert row["agreements"] == 1
    assert row["errors"] == 0
    assert row["ambiguous_tokens"] == 0
    assert row["segments"][0]["operation"] == "merge"
    assert row["exact_sequence"] is True


def test_aggregate_excludes_ambiguous_tokens_from_rate_denominator():
    report = score_calibration(CALIBRATION, CODER, CROSSWALK)
    aggregate = report["aggregate"]
    # Clean 2 + merge 1 agreements; one planted error. Ambiguous
    # reference tokens: 1 (one-to-many) + 1 (conflict-only) + 2 (split).
    assert aggregate["agreements"] == 3
    assert aggregate["errors"] == 1
    assert aggregate["ambiguous_tokens"] == 4
    assert aggregate["scored_tokens"] == 4
    assert aggregate["per_token_agreement"] == 0.75
    assert aggregate["exact_sequence_objects"] == 2


def test_record_set_mismatch_fails_loudly():
    incomplete = {"records": CODER["records"][:-1]}
    try:
        score_calibration(CALIBRATION, incomplete, CROSSWALK)
    except ValueError as exc:
        assert "missing=['fixture:merge']" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("mismatched record set was accepted")
