"""Phase-121: Soviet positional dataset loader / validator.

Descriptive dataset only (see reports/phase121_soviet_positional_dataset.md).
It scores no prediction and validates no anchor. The loader checks
provenance completeness (every record traces to source, printed page
and table id) and reports — never repairs — internal inconsistencies
in the printed tables.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA_DIR = REPO / "data" / "soviet_positional"
DATASET_JSON = DATA_DIR / "phase121_soviet_positional_dataset.json"


def load_dataset(path: Path = DATASET_JSON) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_table_csv(name: str, data_dir: Path = DATA_DIR) -> list[dict]:
    with open(Path(data_dir) / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def provenance_gaps(dataset: dict) -> list[str]:
    """Every record must trace to (source, printed page, table id)."""
    gaps = []
    for table in dataset["tables"]:
        for i, rec in enumerate(table["records"]):
            for key in ("source", "printed_page", "table_id"):
                if rec.get(key) in (None, ""):
                    gaps.append(f"{table['table_id']} record {i}: missing {key}")
            if str(rec.get("table_id")) != table["table_id"]:
                gaps.append(f"{table['table_id']} record {i}: table_id mismatch")
    return gaps


def table4_checks(rows: list[dict]) -> dict:
    """Arithmetic checks on K1965-T4, reported as printed (no repair)."""
    finals = ["final_87", "final_124", "final_68", "final_96",
              "final_97", "final_87_dash", "final_66"]
    body = [r for r in rows if r["initial_sign_1"] != "PRINTED_TOTAL"]
    printed = next(r for r in rows if r["initial_sign_1"] == "PRINTED_TOTAL")
    row_totals_match = all(
        sum(int(r[c]) for c in finals) == int(r["row_total_printed"])
        for r in body)
    computed = {c: sum(int(r[c]) for r in body) for c in finals}
    printed_totals = {c: int(printed[c]) for c in finals}
    return {
        "row_totals_match_cells": row_totals_match,
        "computed_column_totals": computed,
        "printed_column_totals": printed_totals,
        "computed_grand_total": sum(computed.values()),
        "printed_grand_total": int(printed["row_total_printed"]),
        "columns_disagreeing": [c for c in finals
                                if computed[c] != printed_totals[c]],
    }
