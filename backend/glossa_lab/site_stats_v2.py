"""Chi-square test of independence, done properly (repair WP3).

This module replaces ``chi2_test`` in the old Phase 69 script
(``phase69_site_stratification.py``). The old routine did not compute
the p-values it reported:

* If the statistic was greater than twice the degrees of freedom, it
  returned p = 0.0 exactly.
* If the statistic was below 0.5, it returned p = 1.0.
* Otherwise it was supposed to use the Wilson-Hilferty approximation,
  but that branch used ``math`` before a local ``import math``
  statement inside the same branch made ``math`` a local name, so it
  raised ``UnboundLocalError`` every time it ran. The surrounding
  ``except Exception`` then set p = 0.5. In other words, every
  statistic in the middle range was reported with p = 0.5 exactly,
  whatever its actual value was.
* A sign with too little data was assigned statistic 0.0 and p = 1.0
  as placeholder values in the output.
* A p-value at or above 0.05 was labeled "INVARIANT". Not detecting a
  difference is not evidence that two distributions are the same, so
  that label turned an absence of a detected difference into an
  established equivalence.

What this module does instead
-----------------------------
* Method: Pearson chi-square test of independence, WITHOUT the Yates
  continuity correction by default. Yates correction is available as
  an explicit option (``yates=True``) and is accepted only for 2x2
  tables. The choice is recorded in the result's ``method`` field.
* P-value: the survival function of the chi-square distribution,
  computed as the regularized upper incomplete gamma function
  Q(df/2, statistic/2), implemented here in pure standard library
  following Numerical Recipes (``gammq``: series representation when
  x < a + 1, continued fraction otherwise). The implementation is
  pinned by ``MODULE_VERSION`` and is cross-checked in the test suite
  against published reference values to a tolerance of 1e-6.
* Input validation: the table must be rectangular and every cell must
  be a nonnegative integer count. Booleans, floats (even whole-number
  floats), strings, ``None``, and negative values are rejected with
  status ERROR and no p-value. A numerical failure also returns status
  ERROR and no p-value. A p-value is never invented as a fallback.
* Zero margins -- the stated choice: a row or a column whose total is
  zero carries no information about independence, so it is DROPPED,
  and a note naming the dropped row or column is recorded in the
  result's ``notes``. If dropping (or the shape of the input) leaves
  fewer than two rows or two columns, or a grand total of zero, the
  result is status INSUFFICIENT_DATA with no statistic and no
  p-value. Insufficient data is explicit; it is never dressed up with
  placeholder numbers.
* Sparse tables: if any expected count is below 5, the result carries
  ``sparse_table_warning = True`` and a warning naming the smallest
  expected count. The asymptotic p-value is still reported, with that
  warning attached.
* No equivalence verdict: this module reports difference detection
  only. It produces no verdict that sites, signs, or distributions
  are the same, equal, or equivalent. See ``assess_equivalence``,
  which refuses to run without a prespecified design.

Result status values are ``OK``, ``INSUFFICIENT_DATA``, and ``ERROR``.

Pure standard library only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

__all__ = [
    "MODULE_VERSION",
    "STATUS_OK",
    "STATUS_INSUFFICIENT_DATA",
    "STATUS_ERROR",
    "STATUS_NOT_ASSESSED",
    "ChiSquareResult",
    "EquivalenceResult",
    "regularized_gamma_q",
    "gammq",
    "chi_square_independence",
    "chi2_independence",
    "assess_equivalence",
]

MODULE_VERSION = "site-stats-v2.0.0"

STATUS_OK = "OK"
STATUS_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
STATUS_ERROR = "ERROR"
STATUS_NOT_ASSESSED = "NOT_ASSESSED"

_METHOD_PEARSON = (
    "Pearson chi-square test of independence (no Yates correction); "
    "asymptotic p-value from the regularized upper incomplete gamma "
    "function"
)
_METHOD_YATES = (
    "Pearson chi-square test of independence with Yates continuity "
    "correction (2x2 only); asymptotic p-value from the regularized "
    "upper incomplete gamma function"
)

_SPARSE_THRESHOLD = 5.0


# ---------------------------------------------------------------- gamma

def regularized_gamma_q(a: float, x: float) -> float:
    """Regularized upper incomplete gamma function Q(a, x).

    Q(a, x) = Gamma(a, x) / Gamma(a), following Numerical Recipes
    (``gammq`` / ``gser`` / ``gcf``). Raises ValueError for arguments
    outside the domain and ArithmeticError if the series or the
    continued fraction does not converge, or if the computed value
    falls outside [0, 1] by more than rounding error. Callers must
    treat an exception as a numerical failure, never as a p-value.
    """
    if not (math.isfinite(a) and math.isfinite(x)):
        raise ArithmeticError(f"non-finite gamma argument: a={a!r}, x={x!r}")
    if a <= 0:
        raise ValueError(f"gamma shape a must be > 0, got {a!r}")
    if x < 0:
        raise ValueError(f"gamma x must be >= 0, got {x!r}")
    if x == 0:
        return 1.0

    eps = 3e-14
    max_iter = 1000
    log_factor = -x + a * math.log(x) - math.lgamma(a)

    if x < a + 1.0:
        # Series representation for P(a, x); Q = 1 - P.
        ap = a
        term = 1.0 / a
        total = term
        for _ in range(max_iter):
            ap += 1.0
            term *= x / ap
            total += term
            if abs(term) < abs(total) * eps:
                break
        else:
            raise ArithmeticError(
                f"gamma series did not converge for a={a!r}, x={x!r}"
            )
        q = 1.0 - total * math.exp(log_factor)
    else:
        # Continued fraction representation for Q(a, x) directly.
        tiny = 1e-300
        b = x + 1.0 - a
        c = 1.0 / tiny
        d = 1.0 / b if b != 0 else 1.0 / tiny
        h = d
        for i in range(1, max_iter + 1):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < tiny:
                d = tiny
            c = b + an / c
            if abs(c) < tiny:
                c = tiny
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < eps:
                break
        else:
            raise ArithmeticError(
                f"gamma continued fraction did not converge for a={a!r}, x={x!r}"
            )
        q = math.exp(log_factor) * h

    if not math.isfinite(q):
        raise ArithmeticError(f"gamma result is not finite for a={a!r}, x={x!r}")
    if q < 0.0 or q > 1.0:
        # Allow only rounding-level excursions.
        if -1e-12 <= q <= 1.0 + 1e-12:
            q = min(1.0, max(0.0, q))
        else:
            raise ArithmeticError(f"gamma result out of range: {q!r}")
    return q


# Short alias matching the Numerical Recipes name used in the docstring.
gammq = regularized_gamma_q


# ---------------------------------------------------------------- results

@dataclass
class ChiSquareResult:
    """One chi-square independence result.

    ``statistic``, ``df``, and ``p_value`` are None unless ``status``
    is OK. A result with status ERROR or INSUFFICIENT_DATA carries no
    numbers that could be mistaken for evidence.
    """

    status: str
    method: str = _METHOD_PEARSON
    statistic: float | None = None
    df: int | None = None
    p_value: float | None = None
    expected_counts: list[list[float]] | None = None
    min_expected_count: float | None = None
    sparse_table_warning: bool = False
    warnings: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    error: str | None = None
    n_rows: int | None = None
    n_cols: int | None = None
    grand_total: int | None = None
    module_version: str = MODULE_VERSION

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "method": self.method,
            "statistic": self.statistic,
            "df": self.df,
            "p_value": self.p_value,
            "expected_counts": self.expected_counts,
            "min_expected_count": self.min_expected_count,
            "sparse_table_warning": self.sparse_table_warning,
            "warnings": list(self.warnings),
            "notes": list(self.notes),
            "error": self.error,
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "grand_total": self.grand_total,
            "module_version": self.module_version,
        }


@dataclass
class EquivalenceResult:
    """Outcome of the equivalence gatekeeper. See assess_equivalence."""

    status: str = STATUS_NOT_ASSESSED
    reasons: tuple[str, ...] = ()
    module_version: str = MODULE_VERSION

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "reasons": list(self.reasons),
            "module_version": self.module_version,
        }


# ---------------------------------------------------------------- validation

def _validate_table(observed) -> tuple[list[list[int]] | None, str | None]:
    """Return (table, None) or (None, error_message).

    Only genuine integer counts pass. ``bool`` is rejected explicitly
    even though it is a subclass of ``int`` in Python. Floats are
    rejected even when they hold a whole number, because a float cell
    means the caller did not supply counts.
    """
    if isinstance(observed, (str, bytes)) or not isinstance(
        observed, (list, tuple)
    ):
        return None, (
            f"table must be a list of rows, got {type(observed).__name__}"
        )
    if len(observed) == 0:
        return [], None  # empty: caller maps this to INSUFFICIENT_DATA
    table: list[list[int]] = []
    width: int | None = None
    for i, row in enumerate(observed):
        if isinstance(row, (str, bytes)) or not isinstance(row, (list, tuple)):
            return None, f"row {i} is not a list of counts"
        if width is None:
            width = len(row)
        elif len(row) != width:
            return None, (
                f"table is not rectangular: row 0 has {width} cells, "
                f"row {i} has {len(row)}"
            )
        clean_row: list[int] = []
        for j, cell in enumerate(row):
            if isinstance(cell, bool):
                return None, f"cell ({i}, {j}) is a boolean, not a count"
            if not isinstance(cell, int):
                return None, (
                    f"cell ({i}, {j}) is not an integer count: {cell!r}"
                )
            if cell < 0:
                return None, f"cell ({i}, {j}) is negative: {cell}"
            clean_row.append(cell)
        table.append(clean_row)
    return table, None


# ---------------------------------------------------------------- main test

def chi_square_independence(observed, *, yates: bool = False) -> ChiSquareResult:
    """Pearson chi-square test of independence on a count table.

    Returns a ChiSquareResult. Invalid input gives status ERROR with
    no p-value; a table with too little usable data gives status
    INSUFFICIENT_DATA with no statistic and no p-value; a numerical
    failure gives status ERROR with no p-value. Zero-total rows and
    columns are dropped, with a note (see the module docstring).
    """
    method = _METHOD_YATES if yates else _METHOD_PEARSON

    table, error = _validate_table(observed)
    if error:
        return ChiSquareResult(status=STATUS_ERROR, method=method, error=error)
    assert table is not None
    if len(table) == 0 or (len(table) > 0 and len(table[0]) == 0):
        return ChiSquareResult(
            status=STATUS_INSUFFICIENT_DATA,
            method=method,
            notes=("empty table: no counts supplied",),
        )

    notes: list[str] = []

    # Drop zero-total rows, with a logged note for each.
    kept_rows: list[list[int]] = []
    for i, row in enumerate(table):
        if sum(row) == 0:
            notes.append(f"dropped row {i}: row total is zero")
        else:
            kept_rows.append(row)
    # Drop zero-total columns, with a logged note for each.
    if kept_rows:
        n_cols_in = len(kept_rows[0])
        keep_cols: list[int] = []
        for j in range(n_cols_in):
            if sum(row[j] for row in kept_rows) == 0:
                notes.append(f"dropped column {j}: column total is zero")
            else:
                keep_cols.append(j)
        kept_rows = [[row[j] for j in keep_cols] for row in kept_rows]

    n_rows = len(kept_rows)
    n_cols = len(kept_rows[0]) if kept_rows else 0
    grand = sum(sum(row) for row in kept_rows)
    if n_rows < 2 or n_cols < 2 or grand == 0:
        return ChiSquareResult(
            status=STATUS_INSUFFICIENT_DATA,
            method=method,
            notes=tuple(notes)
            + (
                "fewer than two usable rows or columns, or a grand "
                "total of zero, after zero-margin handling; a "
                "chi-square test of independence is not defined",
            ),
            n_rows=n_rows,
            n_cols=n_cols,
            grand_total=grand,
        )

    if yates and not (n_rows == 2 and n_cols == 2):
        return ChiSquareResult(
            status=STATUS_ERROR,
            method=method,
            error=(
                "Yates continuity correction was requested but the "
                f"usable table is {n_rows}x{n_cols}, not 2x2"
            ),
            notes=tuple(notes),
            n_rows=n_rows,
            n_cols=n_cols,
            grand_total=grand,
        )

    row_totals = [sum(row) for row in kept_rows]
    col_totals = [
        sum(kept_rows[i][j] for i in range(n_rows)) for j in range(n_cols)
    ]
    expected = [
        [row_totals[i] * col_totals[j] / grand for j in range(n_cols)]
        for i in range(n_rows)
    ]
    min_expected = min(min(row) for row in expected)

    warnings: list[str] = []
    sparse = min_expected < _SPARSE_THRESHOLD
    if sparse:
        warnings.append(
            f"sparse table: smallest expected count is "
            f"{min_expected:.4g} (< 5); the asymptotic p-value may be "
            "inaccurate for this table"
        )

    try:
        statistic = 0.0
        for i in range(n_rows):
            for j in range(n_cols):
                diff = abs(kept_rows[i][j] - expected[i][j])
                if yates:
                    diff = max(0.0, diff - 0.5)
                statistic += diff * diff / expected[i][j]
        df = (n_rows - 1) * (n_cols - 1)
        if df <= 0:
            raise ArithmeticError(f"degrees of freedom computed as {df}")
        p_value = regularized_gamma_q(df / 2.0, statistic / 2.0)
    except (ArithmeticError, ValueError, OverflowError) as exc:
        return ChiSquareResult(
            status=STATUS_ERROR,
            method=method,
            error=f"numerical failure: {exc}",
            notes=tuple(notes),
            warnings=tuple(warnings),
            n_rows=n_rows,
            n_cols=n_cols,
            grand_total=grand,
        )

    return ChiSquareResult(
        status=STATUS_OK,
        method=method,
        statistic=statistic,
        df=df,
        p_value=p_value,
        expected_counts=expected,
        min_expected_count=min_expected,
        sparse_table_warning=sparse,
        warnings=tuple(warnings),
        notes=tuple(notes),
        n_rows=n_rows,
        n_cols=n_cols,
        grand_total=grand,
    )


chi2_independence = chi_square_independence


# ---------------------------------------------------------------- equivalence

def assess_equivalence(
    observed=None,
    *,
    margin=None,
    effect_scale=None,
    procedure=None,
) -> EquivalenceResult:
    """Gatekeeper for any claim that two distributions are equivalent.

    Equivalence is a design decision, not a default, and a non-
    significant difference test is not evidence of equivalence. This
    helper therefore REFUSES to assess equivalence unless a design was
    prespecified, and in this version it returns NOT_ASSESSED in every
    case, naming what is missing:

    * ``margin`` -- a prespecified acceptable-difference margin, chosen
      before the outcomes were viewed. Without it, this helper returns
      NOT_ASSESSED on that ground alone.
    * ``effect_scale`` -- the scale on which the margin is expressed.
    * ``procedure`` -- a named, prespecified equivalence procedure
      (for example a confidence region that must lie entirely inside
      the margin). This module implements no such procedure, so even a
      call that supplies a margin is NOT_ASSESSED here, with the
      missing procedure named.

    Nothing returned by this helper can be used as evidence that two
    distributions are the same.
    """
    reasons: list[str] = []
    if margin is None:
        reasons.append(
            "no prespecified equivalence margin was supplied; "
            "equivalence cannot be assessed without a margin chosen "
            "before the outcomes were viewed"
        )
    else:
        if isinstance(margin, bool) or not isinstance(margin, (int, float)):
            reasons.append(f"margin is not a number: {margin!r}")
        elif not math.isfinite(margin) or margin <= 0:
            reasons.append(f"margin must be positive and finite, got {margin!r}")
    if effect_scale is None:
        reasons.append("no prespecified effect scale was supplied")
    if procedure is None:
        reasons.append(
            "no prespecified equivalence procedure was supplied; this "
            "module implements no equivalence procedure, so no "
            "equivalence assessment can be made here"
        )
    else:
        reasons.append(
            f"procedure {procedure!r} is not implemented in "
            f"{MODULE_VERSION}; no equivalence assessment can be made here"
        )
    reasons.append(
        "a non-significant difference test is not evidence of "
        "equivalence and is never reported as one by this module"
    )
    return EquivalenceResult(status=STATUS_NOT_ASSESSED, reasons=tuple(reasons))
