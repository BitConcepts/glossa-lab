#!/usr/bin/env python3
"""The composed release gate CLI (Spec 095 Stage 4, T405).

Usage:
    python tools/release-gate/check_release_gate.py --root <candidate> \
        [--evidence evidence.json] [--exceptions exceptions.json] \
        [--surface rel/path ...] [--out record.json]

Exit 0 iff the candidate's verdict is PASS. The per-component
results record is printed and, with --out, written as JSON: the
record of record for the candidate.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.release_gate import format_summary, run_release_gate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="candidate tree (default: cwd)")
    parser.add_argument("--evidence", type=Path, default=None, help="evidence manifest JSON")
    parser.add_argument(
        "--exceptions",
        type=Path,
        default=Path(__file__).resolve().parent / "exceptions.json",
        help="recorded owner-approved exceptions (default: this tool's exceptions.json)",
    )
    parser.add_argument("--surface", action="append", default=None, help="public surface to scan (repeatable)")
    parser.add_argument("--out", type=Path, default=None, help="write the results record JSON here")
    args = parser.parse_args()

    evidence = None
    if args.evidence is not None:
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    exceptions = None
    if args.exceptions is not None and args.exceptions.is_file():
        exceptions = json.loads(args.exceptions.read_text(encoding="utf-8"))

    record = run_release_gate(
        args.root.resolve(),
        evidence=evidence,
        exceptions=exceptions,
        surfaces=args.surface,
    )
    print(format_summary(record))
    if args.out is not None:
        args.out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
