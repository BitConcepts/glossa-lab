"""Regression tests for glossa_lab.site_stats_v2 (repair WP3).

Reference values are the ones named in the repair brief for
uncorrected Pearson chi-square with df = 1. The hand-computed 3x3
statistic is worked out in the test itself from the table margins.

The old Phase 69 routine, run from the inspect copy on the two
reference tables, returns (1.6, 0.5) and (3.6, 0.0): the middle-range
p-value is the except-branch fallback 0.5, and the larger statistic
hits the fabricated p = 0.0 branch. Neither is the correct p-value.
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.site_stats_v2 import (  # noqa: E402
    MODULE_VERSION,
    assess_equivalence,
    chi_square_independence,
    regularized_gamma_q,
)

TOL = 1e-6


# ---- reference tables from the brief -----------------------------------

def test_reference_table_1_statistic_and_p_value():
    result = chi_square_independence([[12, 8], [8, 12]])
    assert result.status == "OK"
    assert result.statistic == pytest.approx(1.6, abs=1e-12)
    assert result.df == 1
    assert result.p_value == pytest.approx(0.2059032107, abs=TOL)
    # The old routine's fingerprint values must not appear.
    assert result.p_value != 0.5
    assert result.p_value != 0.0
    assert result.module_version == MODULE_VERSION
    assert "Yates" in result.method  # the method names the Yates choice
    assert result.expected_counts == [[10.0, 10.0], [10.0, 10.0]]
    assert result.min_expected_count == 10.0
    assert result.sparse_table_warning is False


def test_reference_table_2_statistic_and_p_value():
    result = chi_square_independence([[13, 7], [7, 13]])
    assert result.status == "OK"
    assert result.statistic == pytest.approx(3.6, abs=1e-12)
    assert result.df == 1
    assert result.p_value == pytest.approx(0.0577795711, abs=TOL)
    # chi2 > 2*df made the old routine fabricate p = 0.0 exactly.
    assert result.p_value != 0.0
    assert result.p_value > 0.05


def test_gamma_function_matches_closed_forms():
    # Q(1, x) = exp(-x); Q(2, x) = exp(-x) * (1 + x).
    assert regularized_gamma_q(1.0, 2.0) == pytest.approx(math.exp(-2.0), abs=1e-12)
    assert regularized_gamma_q(2.0, 7.5) == pytest.approx(
        math.exp(-7.5) * 8.5, abs=1e-12
    )
    assert regularized_gamma_q(0.5, 0.0) == 1.0


def test_gamma_function_rejects_bad_arguments():
    with pytest.raises((ValueError, ArithmeticError)):
        regularized_gamma_q(0.0, 1.0)
    with pytest.raises((ValueError, ArithmeticError)):
        regularized_gamma_q(1.0, -1.0)


# ---- multidimensional table, hand-computed ------------------------------

def test_3x3_table_against_hand_computed_statistic():
    # Table [[20,10,10],[10,20,10],[10,10,20]]:
    # every row total and every column total is 40, grand total 120,
    # so every expected count is 40*40/120 = 13.333...
    # Each row contributes (20-13.333)^2/13.333 + 2*(10-13.333)^2/13.333
    # = 3.333... + 2*0.8333... = 5.0. Three rows give 15.0 in total.
    # df = (3-1)*(3-1) = 4, and for df = 4 the survival function is
    # Q(2, 15/2) = exp(-7.5) * (1 + 7.5).
    result = chi_square_independence([[20, 10, 10], [10, 20, 10], [10, 10, 20]])
    assert result.status == "OK"
    assert result.statistic == pytest.approx(15.0, abs=1e-9)
    assert result.df == 4
    assert result.p_value == pytest.approx(math.exp(-7.5) * 8.5, abs=1e-9)
    assert result.min_expected_count == pytest.approx(40 * 40 / 120)
    assert result.sparse_table_warning is False


# ---- Yates option --------------------------------------------------------

def test_yates_is_an_explicit_option_for_2x2_only():
    plain = chi_square_independence([[12, 8], [8, 12]])
    corrected = chi_square_independence([[12, 8], [8, 12]], yates=True)
    assert corrected.status == "OK"
    # |2| - 0.5 = 1.5 per cell; 1.5^2 / 10 * 4 cells = 0.9.
    assert corrected.statistic == pytest.approx(0.9, abs=1e-12)
    assert corrected.p_value == pytest.approx(0.3427817111, abs=TOL)
    assert corrected.statistic != plain.statistic
    assert "Yates continuity correction" in corrected.method

    not_2x2 = chi_square_independence(
        [[20, 10, 10], [10, 20, 10], [10, 10, 20]], yates=True
    )
    assert not_2x2.status == "ERROR"
    assert not_2x2.p_value is None


# ---- zero margins, all-zero, single row, one eligible dimension ---------

def test_zero_margin_row_is_dropped_with_a_logged_note():
    result = chi_square_independence([[0, 0], [10, 10], [10, 10]])
    assert result.status == "OK"
    assert any("dropped row 0" in note for note in result.notes)
    assert result.n_rows == 2
    assert result.statistic == pytest.approx(0.0, abs=1e-12)
    # Statistic 0 legitimately gives p = 1.0 from the gamma function;
    # it is a computed value on a real table, not a placeholder: the
    # status is OK and the expected counts are present.
    assert result.p_value == pytest.approx(1.0, abs=1e-12)
    assert result.expected_counts is not None


def test_zero_margin_column_leaving_one_column_is_insufficient_data():
    result = chi_square_independence([[0, 10], [0, 10]])
    assert result.status == "INSUFFICIENT_DATA"
    assert any("dropped column 0" in note for note in result.notes)
    assert result.statistic is None
    assert result.p_value is None


def test_all_zero_input_is_insufficient_data_with_no_placeholder_numbers():
    result = chi_square_independence([[0, 0], [0, 0]])
    assert result.status == "INSUFFICIENT_DATA"
    # The old code assigned chi2 = 0.0 / p = 1.0 placeholders here.
    assert result.statistic is None
    assert result.p_value is None
    assert result.df is None


def test_single_row_table_is_insufficient_data():
    result = chi_square_independence([[5, 5, 5]])
    assert result.status == "INSUFFICIENT_DATA"
    assert result.statistic is None
    assert result.p_value is None


def test_single_column_table_is_insufficient_data():
    result = chi_square_independence([[5], [5]])
    assert result.status == "INSUFFICIENT_DATA"
    assert result.p_value is None


def test_empty_table_is_insufficient_data():
    assert chi_square_independence([]).status == "INSUFFICIENT_DATA"
    assert chi_square_independence([[]]).status == "INSUFFICIENT_DATA"
    assert chi_square_independence([]).p_value is None


# ---- sparse counts and large effects -------------------------------------

def test_sparse_counts_carry_a_warning():
    result = chi_square_independence([[2, 1], [1, 2]])
    assert result.status == "OK"
    assert result.sparse_table_warning is True
    assert result.min_expected_count == pytest.approx(1.5)
    assert any("sparse" in w.lower() for w in result.warnings)
    assert result.statistic == pytest.approx(2 / 3, abs=1e-9)
    assert result.p_value == pytest.approx(0.4142161782, abs=TOL)


def test_large_effect_gives_a_small_computed_p_value_not_zero():
    result = chi_square_independence([[50, 0], [0, 50]])
    assert result.status == "OK"
    assert result.statistic == pytest.approx(100.0, abs=1e-9)
    assert result.df == 1
    assert result.p_value is not None
    assert 0.0 < result.p_value < 1e-20
    assert result.sparse_table_warning is False


def test_identical_distributions_give_statistic_zero():
    result = chi_square_independence([[10, 10], [10, 10]])
    assert result.status == "OK"
    assert result.statistic == pytest.approx(0.0, abs=1e-12)
    assert result.p_value == pytest.approx(1.0, abs=1e-12)
    # A p-value of 1.0 here must not be turned into any verdict by
    # this module: the result object carries no verdict field at all.
    assert not hasattr(result, "verdict")


# ---- invalid input: ERROR status, never a p-value ------------------------

@pytest.mark.parametrize(
    "table",
    [
        [[1.5, 2], [3, 4]],        # float cell
        [[2.0, 2], [3, 4]],        # whole-number float is still not a count
        [[True, 2], [3, 4]],       # boolean cell
        [[-1, 2], [3, 4]],         # negative cell
        [["3", 2], [3, 4]],        # string cell
        [[None, 2], [3, 4]],       # missing cell
        [[1, 2], [3]],             # not rectangular
        [[1, 2], "not a row"],     # row is not a list of counts
        "not a table",
        None,
        42,
    ],
)
def test_invalid_input_returns_error_status_and_never_a_p_value(table):
    result = chi_square_independence(table)
    assert result.status == "ERROR"
    assert result.error
    # A numerical or input failure must never become a p-value
    # (the old routine's except branch produced p = 0.5).
    assert result.p_value is None
    assert result.statistic is None
    assert result.p_value != 0.5


# ---- no equivalence verdict anywhere --------------------------------------

def test_no_result_carries_an_equivalence_style_verdict():
    for table in ([[12, 8], [8, 12]], [[10, 10], [10, 10]], [[50, 0], [0, 50]]):
        result = chi_square_independence(table)
        as_dict = result.to_dict()
        assert "verdict" not in as_dict
        blob = str(as_dict).upper()
        assert "INVARIANT" not in blob
        assert "EQUIVALENT" not in blob


def test_equivalence_helper_refuses_without_a_prespecified_margin():
    result = assess_equivalence([[12, 8], [8, 12]])
    assert result.status == "NOT_ASSESSED"
    assert any("margin" in reason for reason in result.reasons)


def test_equivalence_helper_does_not_run_on_margin_alone():
    # A margin is necessary but not sufficient: an effect scale and a
    # prespecified procedure are also design decisions, and this
    # module implements no equivalence procedure.
    result = assess_equivalence([[12, 8], [8, 12]], margin=0.1)
    assert result.status == "NOT_ASSESSED"

    bad_margin = assess_equivalence([[12, 8], [8, 12]], margin=-1)
    assert bad_margin.status == "NOT_ASSESSED"
    assert any("margin" in reason for reason in bad_margin.reasons)
