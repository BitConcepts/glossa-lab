"""Tests for the Phase-121 Soviet positional dataset.

Descriptive dataset only: provenance completeness, table shapes,
spot values read from the printed pages, and the printed-anomaly
checks (anomalies are asserted AS PRINTED, never repaired).
"""
from __future__ import annotations

import pytest

from glossa_lab.soviet_positional import (
    load_dataset, load_table_csv, provenance_gaps, table4_checks)

EXPECTED_TABLES = {
    "K1965-T1": 56, "K1965-T2": 11, "K1965-T3": 21, "K1965-T4": 9,
    "PI73-V1": 4, "PI73-V2": 3, "PI73-V3": 5,
}


@pytest.fixture(scope="module")
def dataset():
    return load_dataset()


def test_tables_and_row_counts(dataset):
    got = {t["table_id"]: t["n_rows"] for t in dataset["tables"]}
    assert got == EXPECTED_TABLES
    for t in dataset["tables"]:
        assert len(t["records"]) == t["n_rows"]


def test_provenance_complete(dataset):
    assert provenance_gaps(dataset) == []


def test_non_claims_present(dataset):
    assert dataset["descriptive_only"] is True
    assert "open question" in dataset["non_claims"]
    ids = {t["id"] for t in dataset["tables_not_extracted"]}
    assert ids == {"KN1968", "PI73-G1", "PI73-G2", "PI73-K"}


def test_table1_spot_values():
    rows = load_table_csv("kondratov1965_table1_new_sign_emergence.csv")
    by_n = {int(r["number_of_signs"]): r for r in rows}
    assert (by_n[25]["egypt_new_signs"], by_n[25]["india_new_signs"]) == ("13", "20")
    assert by_n[400]["india_new_signs"] == "6"
    assert by_n[1125]["egypt_new_signs"] == "1"  # text layer reads 'X'; page shows 1
    assert by_n[1400]["india_new_signs"] == "2"


def test_table2_totals():
    rows = load_table_csv("kondratov1965_table2_sign_classes.csv")
    total = rows[-1]
    assert total["frequency_class_pct"] == "TOTAL"
    assert total["egypt_n_signs"] == "195"
    assert total["india_n_signs"] == "315"


def test_table4_printed_anomaly_preserved():
    rows = load_table_csv("kondratov1965_table4_stable_initials_finals.csv")
    checks = table4_checks(rows)
    assert checks["row_totals_match_cells"] is True
    assert checks["computed_grand_total"] == 160
    assert checks["printed_grand_total"] == 171
    assert checks["columns_disagreeing"] == ["final_87", "final_124", "final_66"]


def test_pi73_yuga_durations():
    rows = load_table_csv("protoindica1973_volchok_yuga_durations.csv")
    maha = rows[-1]
    assert maha["duration_divine_years"] == "12000"
    assert maha["duration_human_years"] == "4320000"
    assert sum(int(r["duration_divine_years"]) for r in rows[:4]) == 12000
