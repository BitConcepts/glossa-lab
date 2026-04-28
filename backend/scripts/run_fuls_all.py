"""Run all key Fuls Python experiments via ExperimentBase.run_cli().

Each experiment is invoked through run_cli() so it:
  - Registers a Job in the backend Jobs panel
  - Streams structured log output to backend.log
  - Saves the JSON result to reports/<id>_<timestamp>.json
  - PATCHes the Job to 'completed' or 'failed' on exit

Per H17.1: After every batch we query /api/v1/jobs and report which jobs
completed and which failed.

Usage:
    shell.cmd python backend/scripts/run_fuls_all.py [--quick]

    --quick   skip the slow validation_suite + independence_suite (~20 min total)
"""

from __future__ import annotations

import argparse
import io
import os
import sys
import time
import traceback
from pathlib import Path

# Force UTF-8 stdout on Windows so emoji / dashes don't crash print()
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)
ROOT = Path(_BACKEND).parent

for _p in (_BACKEND, os.path.join(_BACKEND, "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def run_one(label: str, exp_cls):
    """Run one ExperimentBase subclass via run_cli(); capture status."""
    print(f"\n{'=' * 78}\n  {label}\n{'=' * 78}", flush=True)
    t0 = time.time()
    exp_id = getattr(exp_cls, "id", "?")
    try:
        exp = exp_cls()
        result = exp.run_cli()
        elapsed = time.time() - t0
        ok = isinstance(result, dict) and "error" not in result
        marker = "[OK]" if ok else "[WARN]"
        print(f"\n{marker} {label} finished in {elapsed:.1f}s (exp_id={exp.id})", flush=True)
        return ok, exp.id
    except Exception as e:  # noqa: BLE001
        elapsed = time.time() - t0
        print(f"\n[FAIL] {label} crashed after {elapsed:.1f}s: {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
        return False, exp_id


def main(quick: bool = False) -> int:
    from glossa_lab.experiments._legacy.fuls_independence_suite import (
        FulsIndependenceSuite,
    )
    from glossa_lab.experiments._legacy.fuls_nw_semitic_ngram import FulsNWSemiticNgram
    from glossa_lab.experiments._legacy.fuls_rtl_corrected import FulsRTLCorrected
    from glossa_lab.experiments._legacy.fuls_sequence_information_test import (
        FulsSequenceInformationTest,
    )
    from glossa_lab.experiments._legacy.fuls_validation_suite import FulsValidationSuite
    from glossa_lab.experiments._legacy.fuls_writing_system_comparison import (
        FulsWritingSystemComparison,
    )

    plan: list[tuple[str, type]] = [
        ("Writing System Comparison", FulsWritingSystemComparison),
        ("NW Semitic N-gram", FulsNWSemiticNgram),
        ("Sequence Information Test", FulsSequenceInformationTest),
        ("RTL Corrected", FulsRTLCorrected),
    ]
    if not quick:
        plan += [
            ("Independence Suite", FulsIndependenceSuite),
            ("Validation Suite", FulsValidationSuite),
        ]

    print(f"Plan: {len(plan)} Fuls experiments  (quick={quick})")
    for label, _ in plan:
        print(f"  - {label}")

    results: list[tuple[str, str, bool]] = []
    for label, cls in plan:
        ok, exp_id = run_one(label, cls)
        results.append((label, exp_id, ok))

    print("\n" + "=" * 78)
    print("  BATCH SUMMARY (per H17.5)")
    print("=" * 78)
    n_ok = sum(1 for _, _, ok in results if ok)
    print(f"  Submitted: {len(results)}")
    print(f"  Succeeded: {n_ok}")
    print(f"  Failed:    {len(results) - n_ok}")
    for label, exp_id, ok in results:
        marker = "[OK]   " if ok else "[FAIL] "
        print(f"  {marker}{exp_id:<40} {label}")

    print("\nVerify Job registry with:  shell.cmd python backend/scripts/inspect_jobs.py 20")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="skip the two ~5min suites")
    args = parser.parse_args()
    sys.exit(main(quick=args.quick))
