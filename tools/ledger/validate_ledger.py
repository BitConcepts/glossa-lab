#!/usr/bin/env python3
"""Validate the Spec 086 claims ledger (Stage 1, T102).

Runs the full intake validation over
``glossa-indus/ledger/claims.jsonl``: pinned-schema validation,
proposition-fingerprint recomputation and uniqueness (D-B),
field-provenance checks (C086-5, C086-6), pointer resolution,
and the falsifier-coverage counts every run must publish.

Usage (from the repo root):

    python3 tools/ledger/validate_ledger.py [--ledger PATH]

Exit code 0 on PASS, 1 on FAIL. The printed report is the
gate output Stage 1 files verbatim in its stage record.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.ledger_intake import validate_ledger  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=None)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    report = validate_ledger(root, args.ledger)
    report.path = str(args.ledger or (root / "glossa-indus" / "ledger" / "claims.jsonl"))
    sys.stdout.write(report.render())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
