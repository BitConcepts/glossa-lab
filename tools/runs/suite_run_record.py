#!/usr/bin/env python3
"""Write the suite light record for one local evidence run
(Spec 089 Stage 4, T401; C089-6, D-089-6).

A suite run cited as evidence is bound by a lightweight
run record written from the run's OWN output file — the
counts and the failed/errored test ids are parsed from
that file, never from a presentation of the run — plus
the tree state the run measured (tree SHA + dirty flag)
and the rewrite manifest: the paths under
`glossa-indus/claims/` and `glossa-indus/reports/` whose
bytes differ from HEAD after the run, each with its
disposition. A rewritten path the caller does not
dispose refuses the record: an undisposed rewrite is
exactly the contamination C089-6 names. The dirty flag
records the tree as the run left it, observed before
this writer applies any restore.

Usage (from the repo root):

    python3 tools/runs/suite_run_record.py \
        --output pytest-output.txt \
        --command "python -m pytest tests/ -q" \
        --selection tests/ \
        --store specs/<spec>/records \
        [--ignore tests/test_gpu.py] \
        [--restore glossa-indus/claims/extracted_claims/x.json] \
        [--retain glossa-indus/reports/y.json="reason..."]

`--restore` paths are put back to their HEAD bytes and
verified hash-for-hash; `--retain PATH=REASON` paths are
left as the run left them, with the reason recorded.
The record lands in the store under its run id and the
store's run index gains the `entry` act. Exit code 0 on
success, 1 on a named refusal.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import run_records as rr
from glossa_lab import settling as st


def _pytest_version() -> str:
    """The suite tool's version, from the installed
    package metadata (governance H10). "unknown" where
    the metadata is unavailable; recorded, never
    invented."""
    try:
        return importlib.metadata.version("pytest")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _git_head(root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    sha = proc.stdout.strip()
    return sha if proc.returncode == 0 and sha else "unknown"


def _tree_dirty(root: Path) -> bool:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return True  # unmeasurable is not clean
    if proc.returncode != 0:
        return True
    return bool(proc.stdout.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the suite light record for one "
        "local evidence run (Spec 089, T401)."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="the tree the suite measured (default: this repo)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="the pytest invocation's own output file",
    )
    parser.add_argument(
        "--command",
        required=True,
        help="the invocation, verbatim (the key's command "
        "component)",
    )
    parser.add_argument(
        "--selection",
        action="append",
        default=[],
        help="a test path / node id the invocation selected "
        "(repeatable; the key's input pins)",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="an --ignore path of the invocation (repeatable)",
    )
    parser.add_argument(
        "--store",
        type=Path,
        required=True,
        help="the citing stage's records directory (the "
        "suite surface's store of record)",
    )
    parser.add_argument(
        "--restore",
        action="append",
        default=[],
        metavar="PATH",
        help="a rewritten path to restore to its HEAD bytes "
        "(repeatable)",
    )
    parser.add_argument(
        "--retain",
        action="append",
        default=[],
        metavar="PATH=REASON",
        help="a rewritten path to retain, with its reason "
        "(repeatable)",
    )
    parser.add_argument(
        "--environment-class",
        default=None,
        help="venue class token (default: this venue's "
        "registered default)",
    )
    parser.add_argument(
        "--tool-version",
        default=None,
        help="the executing pytest's version (default: the "
        "installed pytest metadata)",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    try:
        output_text = args.output.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"refused: cannot read output file: {exc}", file=sys.stderr)
        return 1
    try:
        result, duration = rr.parse_pytest_output(output_text)
        finished = datetime.fromtimestamp(
            args.output.stat().st_mtime, tz=timezone.utc
        ).replace(microsecond=0)
        started = (
            finished - timedelta(seconds=duration)
            if duration is not None
            else finished
        )
        manifest = rr.rewrite_manifest(root)
        # The tree state as the run left it, observed
        # before this writer applies any disposition.
        tree_sha = _git_head(root)
        tree_dirty = _tree_dirty(root)
        dispositions: dict[str, dict[str, str]] = {
            path: {"disposition": "restored"} for path in args.restore
        }
        for item in args.retain:
            path, sep, reason = item.partition("=")
            if not sep:
                raise rr.RunRecordError(
                    f"--retain expects PATH=REASON, got {item!r}"
                )
            dispositions[path] = {
                "disposition": "retained",
                "reason": reason,
            }
        manifest = rr.apply_rewrite_dispositions(
            root, manifest, dispositions
        )
        record = rr.build_suite_record(
            command=args.command,
            tool_version=args.tool_version or _pytest_version(),
            input_pins={
                "selection": args.selection,
                "ignore": args.ignore,
            },
            code_version=tree_sha,
            environment_class=(
                args.environment_class or st.default_environment_class()
            ),
            started=started,
            finished=finished,
            result=result,
            tree={
                "sha": tree_sha,
                "dirty": tree_dirty,
                "rewrite_manifest": manifest,
            },
        )
        path = rr.write_run_record(args.store, record)
    except rr.RunRecordError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print(f"suite run record: {path}")
    print(json.dumps(record, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
