"""Phase-121 validation run: load the Soviet positional dataset,
check provenance, report printed anomalies, write results JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.soviet_positional import (  # noqa: E402
    load_dataset, load_table_csv, provenance_gaps, table4_checks)

REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    dataset = load_dataset()
    t4 = table4_checks(load_table_csv(
        "kondratov1965_table4_stable_initials_finals.csv"))
    results = {
        "phase": 121,
        "dataset": "phase121_soviet_positional",
        "descriptive_only": True,
        "tables": {t["table_id"]: t["n_rows"] for t in dataset["tables"]},
        "total_records": sum(t["n_rows"] for t in dataset["tables"]),
        "provenance_gaps": provenance_gaps(dataset),
        "tables_not_extracted": [t["id"] for t in dataset["tables_not_extracted"]],
        "table4_checks": t4,
        "printed_anomalies": dataset["printed_anomalies"],
    }
    out = REPO / "reports" / "phase121_soviet_positional_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1))
    print(json.dumps(results, indent=1))
    return 0 if not results["provenance_gaps"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
