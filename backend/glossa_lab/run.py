"""CLI runner for Glossa Lab experiments with full UI integration.

Usage:
    python -m glossa_lab.run <experiment_id> [--param key=value ...]
    python -m glossa_lab.run beam_decipher_benchmark
    python -m glossa_lab.run tier5_indus_decipherment
    python -m glossa_lab.run --list

When the Glossa Lab backend is running you will see:
  - A job appear in the Jobs panel (auto-removed on completion)
  - The result JSON saved in the Reports catalog
  - Log entries in the Logs panel

When the backend is NOT running the experiment still executes normally
and the result is saved to reports/ for when the UI starts.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

# Ensure the backend package is on the path when running as a script
_BACKEND = Path(__file__).resolve().parent.parent
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

# Basic stdout logging so CLI users see structured progress
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
_log = logging.getLogger("glossa_lab.run")


def _list_experiments() -> None:
    from glossa_lab.experiment_base import discover_experiments
    exps = discover_experiments()
    print(f"\n  {'ID':<42} {'Category':<14} {'~Time':<14} Name")
    print("  " + "-" * 100)
    by_cat: dict[str, list] = {}
    for eid, cls in exps.items():
        cat = getattr(cls, "category", "?")
        by_cat.setdefault(cat, []).append((eid, cls))
    for cat in sorted(by_cat):
        for eid, cls in sorted(by_cat[cat]):
            est  = getattr(cls, "estimated_time", "?")
            name = getattr(cls, "name", eid)
            print(f"  {eid:<42} {cat:<14} {est:<14} {name}")
    print(f"\n  Total: {len(exps)} experiments\n")


def _parse_kwarg(s: str) -> tuple[str, object]:
    """Parse 'key=value' into (key, value), auto-converting types."""
    if "=" not in s:
        raise argparse.ArgumentTypeError(f"Expected key=value, got: {s!r}")
    k, v = s.split("=", 1)
    # Type coercion: bool → int → float → str
    if v.lower() in ("true", "false"):
        return k, v.lower() == "true"
    try:
        return k, int(v)
    except ValueError:
        pass
    try:
        return k, float(v)
    except ValueError:
        pass
    return k, v


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m glossa_lab.run",
        description="Run a Glossa Lab experiment with full UI integration.",
    )
    parser.add_argument(
        "experiment_id",
        nargs="?",
        help="Experiment ID to run (e.g. beam_decipher_benchmark).",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available experiments and exit.",
    )
    parser.add_argument(
        "--param", "-p",
        action="append",
        type=_parse_kwarg,
        metavar="key=value",
        default=[],
        help="Pass a parameter to the experiment (repeatable).",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip saving result to reports/ (still registers job).",
    )

    args = parser.parse_args(argv)

    if args.list:
        _list_experiments()
        return 0

    if not args.experiment_id:
        parser.print_help()
        return 1

    # Discover experiment
    from glossa_lab.experiment_base import get_experiment, discover_experiments
    discover_experiments()   # warm cache with all files
    cls = get_experiment(args.experiment_id)
    if cls is None:
        _log.error("Unknown experiment: %s", args.experiment_id)
        print(f"\n  ERROR: experiment '{args.experiment_id}' not found.")
        print("  Run with --list to see all available experiments.\n")
        return 1

    kwargs = dict(args.param)
    exp_name = getattr(cls, "name", args.experiment_id)
    est_time = getattr(cls, "estimated_time", "unknown")

    print(f"\n  Glossa Lab — running experiment via CLI")
    print(f"  ID:           {args.experiment_id}")
    print(f"  Name:         {exp_name}")
    print(f"  Est. time:    {est_time}")
    if kwargs:
        print(f"  Params:       {kwargs}")
    print()

    from glossa_lab.cli_bridge import CliReporter, _api_running
    if _api_running():
        print("  Backend detected — job will appear in the UI Jobs panel.")
    else:
        print("  Backend not detected — results will be saved to reports/ for later.")
    print()

    t0 = time.time()
    with CliReporter(args.experiment_id, exp_name) as rep:
        instance = cls()
        result   = instance.run(**kwargs)

        if isinstance(result, dict) and not args.no_report:
            path = rep.save_result(result)
            if path:
                print(f"\n  Report saved: {path.name}")

    elapsed = round(time.time() - t0, 1)
    print(f"\n  Done in {elapsed}s.")

    # Pretty-print a summary of the result dict
    if isinstance(result, dict):
        print("\n  Result summary:")
        for k, v in list(result.items())[:12]:
            v_str = json.dumps(v, default=str)
            if len(v_str) > 80:
                v_str = v_str[:77] + "..."
            print(f"    {k}: {v_str}")
        if len(result) > 12:
            print(f"    ... ({len(result) - 12} more keys)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
