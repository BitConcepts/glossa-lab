#!/usr/bin/env python3
"""Primary-workspace scope reconciliation CLI (Spec 083, T057).

Usage:
    python tools/workspace-scope/check_workspace_scope.py \
        --data-dir <desktop data dir> --repo-root <install tree>

Runs the reconciliation from ``glossa_lab.workspace_scope_check``
against the dataset IN PLACE (the database is opened read-only; the
dataset is never copied). Prints the per-class report and one
citable verdict line; exits 0 only on ``VERDICT: PASS``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.workspace_scope_check import run_check


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    args = parser.parse_args(argv)
    report = run_check(args.data_dir, args.repo_root)
    print(report.render())
    return 0 if report.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
