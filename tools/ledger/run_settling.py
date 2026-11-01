#!/usr/bin/env python3
"""Run the Spec 086 settling engine (Stage 4, T403).

Drives `backend/glossa_lab/settling.py`, the pure evaluator
of glossa-settle-1 (registered in
`glossa-indus/ledger/SETTLING-SEMANTICS.md`). Settling
outputs are computations over ledgered relations — never
decipherment claims, never ledger verdicts — and a run
writes only run records, into the run store
(`glossa-indus/ledger/runs/`) and nowhere else (C086-16).

Usage (from the repo root):

    python3 tools/ledger/run_settling.py [--root PATH]
        materialize-sets
    python3 tools/ledger/run_settling.py [--root PATH]
        run --candidate ID_OR_JSON --scope sign[,sign...]
            [--scenario ID]
    python3 tools/ledger/run_settling.py [--root PATH]
        compare RUN_RECORD_A RUN_RECORD_B
    python3 tools/ledger/run_settling.py [--root PATH]
        verify-canonicals

`materialize-sets` writes the assignment sets of record
(the incumbent strict-94 set and the full-register set,
read off the canonical anchors register) to
`glossa-indus/ledger/assignment-sets.json`.

`run` evaluates one candidate over one scope and writes
the run record to the run store; `--candidate` names a
set of record by id, or a path to a candidate record as
JSON. The record is also printed.

`compare` prints the dual-run comparison record for two
stored run records (semantics §7); it writes nothing.

`verify-canonicals` evaluates every scenario and the one
comparison registered in
`glossa-indus/ledger/settling-canonical.json` and prints
a PASS/FAIL line per item. The comparison's expectations
note is checked on its mechanically derivable part (the
absence clause); the registered note's brief-specific
remainder is prose, recorded as FINDING-S4-1 in the
stage record. Exit code 0 only if every registered
canonical reproduces under that rule.

Exit code 0 on success, 1 on a named refusal (a source
whose hash does not match the ledger's record, a
malformed candidate, a register whose stored strict
flags disagree with the recomputation).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import settling as st  # noqa: E402


def _load_candidate(root: Path, name: str, state: st.SettleState) -> dict:
    candidate_path = Path(name)
    if candidate_path.is_file():
        return json.loads(candidate_path.read_text(encoding="utf-8"))
    sets = st.load_assignment_sets(root)
    if name in sets:
        return sets[name]
    raise st.SettlingError(
        f"candidate {name!r} is neither a file nor a set of "
        "record in glossa-indus/ledger/assignment-sets.json"
    )


def _first_divergences(expected, actual, path, out, limit=8):
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            if key not in actual:
                out.append(f"{path}.{key}: missing")
            else:
                _first_divergences(
                    expected[key], actual[key], f"{path}.{key}", out, limit
                )
            if len(out) >= limit:
                return
        for key in actual:
            if key not in expected:
                out.append(f"{path}.{key}: unexpected in recomputation")
            if len(out) >= limit:
                return
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            out.append(
                f"{path}: recomputed length {len(actual)}, "
                f"registered length {len(expected)}"
            )
        for i, (e_item, a_item) in enumerate(zip(expected, actual)):
            _first_divergences(e_item, a_item, f"{path}[{i}]", out, limit)
            if len(out) >= limit:
                return
    elif expected != actual:
        out.append(
            f"{path}: recomputed {actual!r}, registered {expected!r}"
        )


def _verify_canonicals(root: Path) -> int:
    state = st.load_state(root)
    canonical_path = root / st.CANONICAL_REL
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    failures = 0
    records: dict[str, dict] = {}
    for scenario in canonical["scenarios"]:
        record = st.run_record(
            state,
            scenario["inputs"]["candidate"],
            scenario["inputs"]["scope"],
            scenario=scenario["id"],
        )
        records[scenario["id"]] = record
        divergences: list[str] = []
        _first_divergences(
            scenario["expected"], record["result"], scenario["id"],
            divergences,
        )
        if divergences:
            failures += 1
            print(f"FAIL {scenario['id']}")
            for line in divergences:
                print(f"  {line}")
        else:
            print(f"PASS {scenario['id']}")
    for comparison in canonical["comparisons"]:
        run_a = records[comparison["inputs"]["runs"][0]]
        run_b = records[comparison["inputs"]["runs"][1]]
        record = st.compare_runs(run_a, run_b)
        expected = dict(comparison["expected"])
        registered_note = expected.pop("pre_registered_expectations_note")
        actual = dict(record["result"])
        engine_note = actual.pop("pre_registered_expectations_note")
        divergences = []
        _first_divergences(
            expected, actual, comparison["id"], divergences
        )
        note_ok = registered_note.split(";")[0] + "." == engine_note
        if divergences or not note_ok:
            failures += 1
            print(f"FAIL {comparison['id']}")
            for line in divergences:
                print(f"  {line}")
            if not note_ok:
                print(
                    "  pre_registered_expectations_note: the "
                    "engine's absence clause does not match the "
                    "registered note's first clause"
                )
        else:
            print(f"PASS {comparison['id']}")
            print(
                "  expectations note: absence clause reproduced "
                "exactly; the registered note's remainder is "
                "brief-specific prose (FINDING-S4-1, stage "
                "record)"
            )
    total = len(canonical["scenarios"]) + len(canonical["comparisons"])
    print(
        f"verify-canonicals: {total - failures}/{total} registered "
        "canonicals reproduce"
    )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("materialize-sets")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--candidate", required=True)
    run_parser.add_argument(
        "--scope",
        required=True,
        help="comma-separated frame-qualified signs",
    )
    run_parser.add_argument("--scenario", default=None)
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("run_a", type=Path)
    compare_parser.add_argument("run_b", type=Path)
    sub.add_parser("verify-canonicals")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == "materialize-sets":
            path = st.write_assignment_sets(root)
            payload = path.read_bytes()
            data = json.loads(payload.decode("utf-8"))
            counts = ", ".join(
                f"{record['id']}: {len(record['assignments'])} "
                "assignments"
                for record in data["sets"]
            )
            print(
                f"wrote {path.relative_to(root)} ({len(payload)} "
                f"bytes, sha256 "
                f"{hashlib.sha256(payload).hexdigest()})"
            )
            print(f"sets of record: {counts}")
            print(
                "out of frame (counted, assigned by no set): "
                + ", ".join(data["out_of_frame_records"])
            )
            return 0
        if args.command == "run":
            state = st.load_state(root)
            candidate = _load_candidate(root, args.candidate, state)
            scope = [s.strip() for s in args.scope.split(",") if s.strip()]
            record = st.run_record(
                state, candidate, scope, scenario=args.scenario
            )
            path = st.write_run_record(root, record)
            print(f"wrote run record {path.relative_to(root)}")
            sys.stdout.write(
                json.dumps(record, ensure_ascii=False, indent=1) + "\n"
            )
            return 0
        if args.command == "compare":
            run_a = json.loads(args.run_a.read_text(encoding="utf-8"))
            run_b = json.loads(args.run_b.read_text(encoding="utf-8"))
            record = st.compare_runs(run_a, run_b)
            sys.stdout.write(
                json.dumps(record, ensure_ascii=False, indent=1) + "\n"
            )
            return 0
        if args.command == "verify-canonicals":
            return _verify_canonicals(root)
    except st.SettlingError as exc:
        print(f"SETTLING REFUSED: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
