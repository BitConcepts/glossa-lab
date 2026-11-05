#!/usr/bin/env python3
"""The Spec 089 junction tool CLI (Stage 3, T301).

Drives `backend/glossa_lab/run_junction.py`, the
comparator of run-defs v1 §6
(`glossa-indus/ledger/RUN-DEFINITIONS.md`): two run
records from one store, compared mechanically — key
diff (constitutive components marked), environment
diff, first divergent output localized, and exactly
one disposition. The tool is standalone (D-089-2): it
originates no explanation beyond the registered
mechanical cases (a divergence wholly inside a
registered nondeterminism shape; a divergence that
exists only in a presentation of the records). An
unexplained junction quarantines both runs by index
act and carries the red-team section — the report, the
evidence pack, and the quarantine exist without anyone
having to remember to ask (C089-14).

Usage (from the repo root):

    python3 tools/ledger/run_junction.py [--root PATH]
        [--store PATH] [--junctions PATH]
        compare RUN_A RUN_B [--presented-artifact NAME]
    python3 tools/ledger/run_junction.py [--root PATH]
        [--store PATH] [--junctions PATH]
        scan [--run RUN_ID]
    python3 tools/ledger/run_junction.py [--root PATH]
        [--store PATH]
        adjudicate JUNCTION_ID --ruling TEXT --actor NAME
            [--resulting-state quarantine-lifted |
                               quarantine-confirmed]

`compare` names two runs by run id or by store-relative
record filename. Dispositions: identical (listed, no
report written) / not-comparable (the pair is refused
as a junction; the differing constitutive components
are named) / explained-by-named-difference /
identical-after-all (the last two file a report in the
junction store) / unexplained (report filed; both runs
quarantined by index act — while the quarantine stands
open, neither run's results may be cited as verdict
support, C089-13).

`scan` analyzes every comparable pair in the store's
index (identical pairs listed, triggering pairs
reported + written); `--run` restricts the scan to the
pairs involving one run — the form the settling
surface's automatic trigger uses at run completion
(T303).

`adjudicate` appends the adjudication act for a
junction: a named actor's ruling, lifting or
confirming its quarantine. It never edits the junction
report or the run records.

Exit code 0 on success — an unexplained disposition is
a first-class outcome of the tool, not a failure of it.
Exit code 1 on a named refusal (an unknown run id, a
record that fails validation, an act the fold refuses).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import run_junction as rj
from glossa_lab import run_records as rr


def _pair_line(outcome: dict) -> str:
    runs = outcome["runs"]
    pair = f"{runs[0]['run_id']} vs {runs[1]['run_id']}"
    disposition = outcome["disposition"]
    if disposition == "identical":
        return f"{pair}: identical"
    if disposition == "not-comparable":
        return (
            f"{pair}: not-comparable — constitutive "
            f"components differ: "
            f"{outcome['differing_components']} "
            "(different experiments, C089-10; no report, "
            "no quarantine)"
        )
    line = (
        f"{pair}: {disposition} — junction "
        f"{outcome['junction_id']}, report "
        f"{outcome['report_path']}"
    )
    if outcome.get("quarantined"):
        line += (
            "; both runs QUARANTINED by index act — "
            "neither run's results may be cited as "
            "verdict support while the quarantine stands "
            "open (C089-13)"
        )
    return line


def _resolve_run_id(store: Path, state: rr.IndexState,
                    name: str) -> str:
    """A run named on the command line, by run id or by
    store-relative record filename."""
    if name in state.entries:
        return name
    for run_id in state.order:
        if state.entries[run_id]["record"] == name:
            return run_id
    raise rr.RunRecordError(
        f"run {name!r} is neither a run id in the index "
        f"of store {store} nor one of its record "
        "filenames"
    )


def _execute_compare(args: argparse.Namespace, store: Path,
                     junctions: Path) -> int:
    state = rr.fold_index(store / "run-index.jsonl")
    run_id_a = _resolve_run_id(store, state, args.run_a)
    run_id_b = _resolve_run_id(store, state, args.run_b)
    outcome = rj.analyze_pair(
        store, junctions, run_id_a, run_id_b,
        presented_artifact=args.presented_artifact,
    )
    print(_pair_line(outcome))
    if outcome["report_path"] is not None:
        report = json.loads(
            Path(outcome["report_path"]).read_text(
                encoding="utf-8"
            )
        )
        sys.stdout.write(
            json.dumps(report, ensure_ascii=False, indent=1)
            + "\n"
        )
    return 0


def _execute_scan(args: argparse.Namespace, store: Path,
                  junctions: Path) -> int:
    outcome = rj.scan_store(
        store, junctions, only_run_id=args.run,
    )
    for pair in outcome["pairs"]:
        print(_pair_line(pair))
    for skipped in outcome["skipped"]:
        runs = skipped["runs"]
        print(
            f"{runs[0]} vs {runs[1]}: not paired — "
            f"{skipped['reason']}"
        )
    counts = outcome["counts"]
    summary = ", ".join(
        f"{disposition} {n}"
        for disposition, n in sorted(counts.items())
    )
    print(
        f"scan: {len(outcome['pairs'])} comparable "
        f"pair(s) analyzed ({summary or 'none'}), "
        f"{len(outcome['skipped'])} pair(s) not paired"
    )
    return 0


def _execute_adjudicate(args: argparse.Namespace,
                        store: Path) -> int:
    state = rj.adjudicate(
        store,
        args.junction_id,
        ruling=args.ruling,
        actor=args.actor,
        resulting_state=args.resulting_state,
    )
    junction = state.junctions[args.junction_id]
    print(
        f"adjudication appended for junction "
        f"{args.junction_id}: {args.resulting_state} "
        f"(actor {args.actor}); runs "
        f"{junction['run_ids']} — open quarantine now: "
        f"{sorted(state.open_quarantine)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=None,
        help="run store directory (default: the settling "
        "store, <root>/glossa-indus/ledger/runs)",
    )
    parser.add_argument(
        "--junctions",
        type=Path,
        default=None,
        help="junction store directory (default: "
        "<root>/glossa-indus/ledger/junctions)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("run_a")
    compare_parser.add_argument("run_b")
    compare_parser.add_argument(
        "--presented-artifact",
        default=None,
        help="name a presentation of the pair that "
        "asserted a divergence (a summary, a delivery, a "
        "dashboard); consulted only when the records "
        "themselves agree — the identical-after-all case",
    )
    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument(
        "--run",
        default=None,
        help="restrict the scan to pairs involving this "
        "run id",
    )
    adjudicate_parser = sub.add_parser("adjudicate")
    adjudicate_parser.add_argument("junction_id")
    adjudicate_parser.add_argument("--ruling", required=True)
    adjudicate_parser.add_argument("--actor", required=True)
    adjudicate_parser.add_argument(
        "--resulting-state",
        default="quarantine-lifted",
        choices=list(rr.ADJUDICATION_STATES),
        help="the ruling's effect on the quarantine "
        "(default: quarantine-lifted)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    store = (
        args.store.resolve()
        if args.store is not None
        else root / rj.RUNS_REL
    )
    junctions = (
        args.junctions.resolve()
        if args.junctions is not None
        else rj.junctions_path(root)
    )
    try:
        if args.command == "compare":
            return _execute_compare(args, store, junctions)
        if args.command == "scan":
            return _execute_scan(args, store, junctions)
        if args.command == "adjudicate":
            return _execute_adjudicate(args, store)
    except rr.RunRecordError as exc:
        print(f"JUNCTION REFUSED: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(
            f"JUNCTION REFUSED: a record in store {store} "
            f"is not valid JSON: {exc}",
            file=sys.stderr,
        )
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
