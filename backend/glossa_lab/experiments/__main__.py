"""Universal CLI entry point for Glossa Lab experiments.

Usage:
    python -m glossa_lab.experiments <experiment_id> [--list]

This routes through ExperimentBase.run_cli() so the run is always
registered as a job in the UI, the result is saved to reports/, and
log entries appear in the backend log — regardless of whether the
experiment was triggered from the terminal or from within the Glossa Lab UI.

Examples:
    python -m glossa_lab.experiments beam_decipher_benchmark
    python -m glossa_lab.experiments fuls_nw_semitic_benchmark
    python -m glossa_lab.experiments --list
"""

from __future__ import annotations

import sys
import os

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _list_experiments() -> None:
    from glossa_lab.experiment_graph import register_graph_experiments  # noqa: PLC0415
    register_graph_experiments()
    from glossa_lab.experiment_base import list_discovered_experiments
    exps = list_discovered_experiments()
    print(f"\n  {len(exps)} experiments registered:\n")
    for e in sorted(exps, key=lambda x: (x["category"], x["id"])):
        print(f"  [{e['category']:20s}]  {e['id']:<45}  {e['estimated_time']}")
    print()


def _run(experiment_id: str) -> None:
    # Register graph experiments (JSON files) into the discovery registry
    # before looking up the experiment by ID.
    from glossa_lab.experiment_graph import register_graph_experiments  # noqa: PLC0415
    register_graph_experiments()
    from glossa_lab.experiment_base import get_experiment
    cls = get_experiment(experiment_id)
    if cls is None:
        print(f"  ERROR: experiment '{experiment_id}' not found.", file=sys.stderr)
        print("  Run with --list to see all registered experiments.", file=sys.stderr)
        sys.exit(1)
    # Strip surrogate/emoji chars that can crash Windows console
    safe_name = cls.name.encode("ascii", errors="replace").decode("ascii")
    print(f"\n  Running: {safe_name}  [{cls.estimated_time}]")
    print(f"  This run is registered as a Job in the Glossa Lab UI.\n")
    result = cls().run_cli()
    print(f"\n  Done. Result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("__")]  # filter pyc artefacts
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)
    if "--list" in args or args[0] == "list":
        _list_experiments()
        sys.exit(0)
    _run(args[0])


if __name__ == "__main__":
    main()
