#!/usr/bin/env python3
"""Generate the Spec 086 claims×evidence matrix (Stage 2, T202).

Runs the pure builder in `backend/glossa_lab/matrix_generate.py`
over the ledger and its registers and writes the two generated
artifacts (`glossa-indus/matrix/matrix.json`, `matrix.md`).
The matrix is generated, never made: these artifacts are
produced only here, and delete-and-regenerate over an
unchanged ledger reproduces them byte-for-byte (C086-7).

Usage (from the repo root):

    python3 tools/ledger/generate_matrix.py [--root PATH]
                                            [--out-dir PATH]
                                            [--check]
                                            [--gated]

`--check` builds without writing and exits 0 only if the
committed artifacts are byte-identical to the fresh build.

`--gated` (Spec 086 Stage 3, T303) publishes through the
verification gate: the build is written as a candidate, the
gate runs against the candidate, and the published artifacts
are replaced only on ALL PASS — on a red gate the published
files are byte-untouched and the command exits 1 with the
gate output.

Exit code 0 on success, 1 on a named refusal (a source whose
hash does not match the ledger's record, an unregistered
direction, a conflicting derivation). The printed output is
the generator output Stage 2 files verbatim in its stage
record.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.matrix_generate import (  # noqa: E402
    MatrixBuildError,
    build_matrix,
    write_matrix,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="artifact directory (default: <root>/glossa-indus/matrix)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="build only; exit 0 iff committed artifacts match the build",
    )
    parser.add_argument(
        "--gated",
        action="store_true",
        help="publish through the Stage 3 verification gate "
        "(candidate -> gate -> replace only on ALL PASS)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    out_dir = (
        args.out_dir.resolve()
        if args.out_dir
        else (root / "glossa-indus" / "matrix")
    )
    try:
        if args.gated:
            from glossa_lab.gated_publish import publish_matrix

            result = publish_matrix(root, out_dir)
            gate = result["gate"]
            sys.stdout.write(gate.render())
            if not result["published"]:
                print(
                    "PUBLICATION REFUSED: the gate is red; the "
                    "published artifacts are byte-untouched.",
                    file=sys.stderr,
                )
                return 1
            for name, info in result["written"].items():
                print(f"published {info['path']} ({info['bytes']} bytes, "
                      f"sha256 {info['sha256']})")
            return 0
        if args.check:
            build = build_matrix(root)
            ok = True
            for name, data in (
                ("matrix.json", build.json_bytes),
                ("matrix.md", build.md_bytes),
            ):
                target = out_dir / name
                if not target.is_file() or target.read_bytes() != data:
                    print(f"STALE: {target} differs from the fresh build")
                    ok = False
            sys.stdout.write(build.output)
            print("CHECK: " + ("MATCH" if ok else "STALE"))
            return 0 if ok else 1
        result = write_matrix(root, out_dir)
        build = result["build"]
        sys.stdout.write(build.output)
        for name, info in result["written"].items():
            print(f"wrote {info['path']} ({info['bytes']} bytes, "
                  f"sha256 {info['sha256']})")
        return 0
    except MatrixBuildError as exc:
        print(f"GENERATION REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
