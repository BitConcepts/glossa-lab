#!/usr/bin/env python3
"""Generate the Spec 086 layered map data (Stage 5, T502).

Runs the pure builder in `backend/glossa_lab/map_generate.py`
over the ledger through the gated matrix and the settling
records of record, and writes the generated artifact
(`glossa-indus/map/map-data.json`). The map is generated,
never made: the artifact is produced only here, and
delete-and-regenerate over unchanged inputs reproduces it
byte-for-byte (map-defs v1, DEFINITIONS.md §2).

Usage (from the repo root):

    python3 tools/ledger/generate_map.py [--root PATH]
                                         [--out-dir PATH]
                                         [--check]
                                         [--gated]

`--check` builds without writing and exits 0 only if the
committed artifact is byte-identical to the fresh build.

`--gated` (Stage 3's gated publication, extended to the map
in Stage 5) publishes through the verification gate: the
build is written as a candidate, the gate runs against the
candidate, and the published artifact is replaced only on
ALL PASS — on a red gate the published file is
byte-untouched and the command exits 1 with the gate output.

Exit code 0 on success, 1 on a named refusal (a source whose
hash does not match the ledger's record, a stale matrix, a
settling record pinned to another build). The printed
output is the generator output the stage record files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.map_generate import (  # noqa: E402
    MapBuildError,
    build_map,
    write_map,
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
        help="artifact directory (default: <root>/glossa-indus/map)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="build only; exit 0 iff the committed artifact "
        "matches the build",
    )
    parser.add_argument(
        "--gated",
        action="store_true",
        help="publish through the verification gate "
        "(candidate -> gate -> replace only on ALL PASS)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    out_dir = (
        args.out_dir.resolve()
        if args.out_dir
        else (root / "glossa-indus" / "map")
    )
    try:
        if args.gated:
            from glossa_lab.gated_publish import publish_map

            result = publish_map(root, out_dir)
            gate = result["gate"]
            sys.stdout.write(gate.render())
            if not result["published"]:
                print(
                    "PUBLICATION REFUSED: the gate is red; the "
                    "published artifact is byte-untouched.",
                    file=sys.stderr,
                )
                return 1
            for name, info in result["written"].items():
                print(f"published {info['path']} ({info['bytes']} bytes, "
                      f"sha256 {info['sha256']})")
            return 0
        if args.check:
            build = build_map(root)
            target = out_dir / "map-data.json"
            ok = (
                target.is_file()
                and target.read_bytes() == build.json_bytes
            )
            sys.stdout.write(build.output)
            print("CHECK: " + ("MATCH" if ok else "STALE"))
            return 0 if ok else 1
        result = write_map(root, out_dir)
        build = result["build"]
        sys.stdout.write(build.output)
        for name, info in result["written"].items():
            print(f"wrote {info['path']} ({info['bytes']} bytes, "
                  f"sha256 {info['sha256']})")
        return 0
    except MapBuildError as exc:
        print(f"GENERATION REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
