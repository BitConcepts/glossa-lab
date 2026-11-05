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
`glossa-indus/ledger/assignment-sets.json`. Since Spec
089 Stage 2 it is a run: the artifact names its producing
run, a materialization run record lands in the run store,
and the store's run index gains the entry act.

`run` evaluates one candidate over one scope and writes
the run record to the run store; `--candidate` names a
set of record by id, or a path to a candidate record as
JSON. The record is also printed. The run id is minted
at execution start (run-defs v1, D-089-1); the record
lands under its run id, a same-basis rerun writes a NEW
record and appends a `supersedes` act naming the record
it re-derives (the superseded record stays in the store),
and an execution that refuses or crashes writes an
absence record stating the absence instead of a result.

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
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import run_records as rr
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


# ---------------------------------------------------------------------------
# Spec 089 Stage 2 — execution identity: minting, the index
# acts, and the absence record a no-result execution leaves.


def _code_version(root: Path) -> str:
    """The executed tree's git SHA — the key's
    code_version component. "unknown" where the tree is
    not a git checkout (a tmp mirror in a test): recorded
    as unknown, never invented."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    sha = proc.stdout.strip()
    return sha if proc.returncode == 0 and sha else "unknown"


def _append_entry(root: Path, record: dict) -> None:
    """The index `entry` act for a record just written."""
    header = record["run"]
    rr.append_act(
        st.run_index_path(root),
        {
            "act": "entry",
            "run_id": header["run_id"],
            "record": st.run_record_path(root, record).name,
            "key": header["key"],
            "legacy": False,
        },
    )


def _append_supersession(root: Path, record: dict) -> str | None:
    """A run that re-derives a stored record's basis
    supersedes it (Spec 089 Stage 2; the adoption-refresh
    relation of C089-2, as an index act — the superseded
    record stays in the store, byte-untouched). The basis
    is the record's (scenario, candidate, scope) — what
    the retired content-addressed filename hashed. The
    latest non-superseded predecessor with the same basis
    is the one superseded, so chains stay linear. Returns
    the superseded run id, or None."""
    basis = (
        record.get("scenario"),
        record.get("candidate"),
        tuple(record.get("scope") or ()),
    )
    if record.get("candidate") is None or "result" not in record:
        return None
    index_path = st.run_index_path(root)
    state = rr.fold_index(index_path)
    predecessor: str | None = None
    store = root / st.RUN_STORE_REL
    for prior_id in state.order:
        if prior_id == record["run"]["run_id"]:
            continue
        if prior_id in state.superseded_by:
            continue
        prior_path = store / state.entries[prior_id]["record"]
        if not prior_path.is_file():
            continue
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        if "result" not in prior or prior.get("candidate") is None:
            continue
        prior_basis = (
            prior.get("scenario"),
            prior.get("candidate"),
            tuple(prior.get("scope") or ()),
        )
        if prior_basis == basis:
            predecessor = prior_id
    if predecessor is None:
        return None
    rr.append_act(
        index_path,
        {
            "act": "supersedes",
            "run_id": record["run"]["run_id"],
            "supersedes": predecessor,
            "ref": (
                f"run_settling.py run {record['run']['run_id']} "
                "(same-basis re-derivation)"
            ),
        },
    )
    return predecessor


def _write_absence(
    root: Path,
    *,
    run_id: str,
    started: datetime,
    command: str,
    tool: str,
    pins: dict | None,
    envelope: dict,
    kind: str,
    detail: str,
    code_version: str,
) -> Path | None:
    """Write the absence record for a no-result execution
    (run-defs v1 §3.2) plus its index entry act: an
    execution that refuses or crashes leaves this record,
    not a half-written result and not silence (C089-1).
    Where the state never loaded, no pins exist to record
    — the key's input pins are the empty object and the
    absence detail says so. Returns the record's path, or
    None when even the absence write refused (named on
    stderr; the original refusal still governs)."""
    try:
        header = st.settling_run_header(
            pins if pins is not None else {},
            command=command,
            tool=tool,
            run_id=run_id,
            started=started,
            finished=datetime.now(UTC),
            code_version=code_version,
        )
        record: dict = {
            "run": header,
            "artifact": "settling run record",
            "label": st.SETTLING_LABEL,
            "semantics": st.SEMANTICS_VERSION,
        }
        record.update(envelope)
        if pins is not None:
            record["pins"] = pins
        record["absence"] = {"kind": kind, "detail": detail}
        path = st.write_run_record(root, record)
        _append_entry(root, record)
        return path
    except (st.SettlingError, rr.RunRecordError) as exc:
        print(
            f"absence record write also refused: {exc}",
            file=sys.stderr,
        )
        return None


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


def _execute_materialize_sets(root: Path) -> int:
    """materialize-sets as a run (Spec 089 Stage 2): mint
    at start, stamp the artifact with its producing run,
    write the materialization run record, append the
    entry act. A refusal leaves an absence record."""
    started = datetime.now(UTC)
    run_id = rr.mint_run_id("settling", now=started)
    command = "materialize-sets"
    code_version = _code_version(root)
    state: st.SettleState | None = None
    try:
        state = st.load_state(root)
        header = st.settling_run_header(
            state.pins,
            command=command,
            tool="run_settling.py materialize-sets",
            run_id=run_id,
            started=started,
            code_version=code_version,
        )
        artifact = st.stamp_assignment_sets_binding(
            st.build_assignment_sets(state), header
        )
        path = st.write_assignment_sets(root, artifact)
        payload = path.read_bytes()
        header["finished"] = rr.iso_stamp(datetime.now(UTC))
        record = st.materialization_record(
            state,
            artifact,
            header,
            artifact_sha256=hashlib.sha256(payload).hexdigest(),
        )
        record_path = st.write_run_record(root, record)
        _append_entry(root, record)
    except st.SettlingError as exc:
        _write_absence(
            root,
            run_id=run_id,
            started=started,
            command=command,
            tool="run_settling.py materialize-sets",
            pins=state.pins if state is not None else None,
            envelope={"materializes": st.ASSIGNMENT_SETS_REL},
            kind="refused",
            detail=str(exc),
            code_version=code_version,
        )
        print(f"SETTLING REFUSED: {exc}", file=sys.stderr)
        return 1
    data = json.loads(payload.decode("utf-8"))
    counts = ", ".join(
        f"{record['id']}: {len(record['assignments'])} assignments"
        for record in data["sets"]
    )
    print(
        f"wrote {path.relative_to(root)} ({len(payload)} bytes, "
        f"sha256 {hashlib.sha256(payload).hexdigest()})"
    )
    print(f"sets of record: {counts}")
    print(
        "out of frame (counted, assigned by no set): "
        + ", ".join(data["out_of_frame_records"])
    )
    print(
        f"run record {record_path.relative_to(root)} "
        f"(run {run_id})"
    )
    return 0


def _execute_run(root: Path, args: argparse.Namespace) -> int:
    """One settling run (Spec 089 Stage 2): the id is
    minted at execution start, before any results exist;
    the record lands under its run id; the index gains
    the entry act and, for a same-basis re-derivation, a
    supersedes act. A refusal or a crash leaves an
    absence record, never a half-written result."""
    started = datetime.now(UTC)
    run_id = rr.mint_run_id("settling", now=started)
    scope = [s.strip() for s in args.scope.split(",") if s.strip()]
    command = (
        f"run --candidate {args.candidate} --scope {args.scope}"
        + (f" --scenario {args.scenario}" if args.scenario else "")
    )
    code_version = _code_version(root)
    state: st.SettleState | None = None
    candidate: dict | None = None
    envelope = {
        "scenario": args.scenario,
        "candidate": args.candidate,
        "scope": scope,
    }
    try:
        state = st.load_state(root)
        candidate = _load_candidate(root, args.candidate, state)
        envelope["candidate"] = candidate["id"]
        header = st.settling_run_header(
            state.pins,
            command=command,
            tool="run_settling.py run",
            run_id=run_id,
            started=started,
            code_version=code_version,
        )
        record = st.run_record(
            state, candidate, scope,
            scenario=args.scenario, header=header,
        )
        header["finished"] = rr.iso_stamp(datetime.now(UTC))
        path = st.write_run_record(root, record)
    except st.SettlingError as exc:
        _write_absence(
            root,
            run_id=run_id,
            started=started,
            command=command,
            tool="run_settling.py run",
            pins=state.pins if state is not None else None,
            envelope=envelope,
            kind="refused",
            detail=str(exc),
            code_version=code_version,
        )
        print(f"SETTLING REFUSED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # a crash mid-execution
        _write_absence(
            root,
            run_id=run_id,
            started=started,
            command=command,
            tool="run_settling.py run",
            pins=state.pins if state is not None else None,
            envelope=envelope,
            kind="crashed",
            detail=f"{type(exc).__name__}: {exc}",
            code_version=code_version,
        )
        raise
    _append_entry(root, record)
    superseded = _append_supersession(root, record)
    print(f"wrote run record {path.relative_to(root)}")
    if superseded is not None:
        print(
            f"supersedes {superseded} (same-basis "
            "re-derivation; the superseded record remains "
            "in the store)"
        )
    sys.stdout.write(
        json.dumps(record, ensure_ascii=False, indent=1) + "\n"
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
    if args.command == "materialize-sets":
        return _execute_materialize_sets(root)
    if args.command == "run":
        return _execute_run(root, args)
    try:
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
