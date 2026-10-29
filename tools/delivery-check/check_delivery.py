#!/usr/bin/env python3
"""Delivery-integrity checker CLI (Leg C finding C-15).

Usage:
    python tools/delivery-check/check_delivery.py <run_id> <expected_sha>

Prints exactly one citable verdict line and exits 0 only when the
run RESOLVES against the GitHub API (exists, head_sha matches, all
jobs' conclusions are success). Any other outcome prints
``UNRESOLVED: <reason>`` and exits 1. Watchers, crons, and reporting
templates must paste this line — never a watcher's prose summary.
See backend/glossa_lab/delivery_check.py for the rule ("No
resolution, no report").
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.delivery_check import check_delivery  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_delivery.py <run_id> <expected_sha>")
        return 2
    ok, verdict = check_delivery(argv[1], argv[2])
    print(verdict)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
