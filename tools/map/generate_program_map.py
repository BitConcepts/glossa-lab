#!/usr/bin/env python3
"""Generate the Spec 088 program map (Stage S1, T103).

Runs the pure builder in `backend/glossa_lab/program_map_generate.py`
over the ledger, the curated taxonomy, and the spec tree, and
writes the two generated artifacts:

- `glossa-indus/map/program-map.json` — one node per claim and
  per study, standings derived under program-map-defs v1;
- `glossa-indus/map/program-map-finds.json` — the machine find
  list (bundle-less studies, judgment calls, extracted claims
  with null falsifiers, restricted nodes).

Delete-and-regenerate over unchanged inputs reproduces the
committed bytes exactly; the stamp carries only input-derived
values (the ledger's canonical hash, its line count, its own
latest entry date, and the defs/taxonomy versions) — no wall
clock.

Usage (from the repo root):

    python3 tools/map/generate_program_map.py [--root PATH]
                                              [--check]

`--check` builds without writing and exits 0 only if every
committed artifact is byte-identical to the fresh build.

Exit code 0 on success, 1 on a named refusal (a coverage gap,
an unknown id, an unregistered status, a taxonomy carrying a
standing-shaped key) — on a refusal nothing is written.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.program_map_generate import (  # noqa: E402
    ProgramMapBuildError,
    build_artifacts,
    check_outputs,
    write_outputs,
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
        "--check",
        action="store_true",
        help="build only; exit 0 iff committed artifacts match the build",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.check:
            drifted = check_outputs(root)
            if drifted:
                print("DRIFT in generated program-map artifacts:")
                for name in drifted:
                    print(f"  {name}")
                print(
                    "Regenerate with: "
                    "python3 tools/map/generate_program_map.py"
                )
                return 1
            print("OK: generated program-map artifacts match the inputs")
            return 0
        written = write_outputs(root)
    except ProgramMapBuildError as exc:
        print(f"REFUSED: {exc}")
        return 1
    for name in written:
        print(f"wrote {name}")
    artifacts = build_artifacts(root)
    program_map = artifacts["glossa-indus/map/program-map.json"]
    coverage = json.loads(program_map)["coverage"]
    print(
        "claims: {claims} · studies: {studies} · unjudged studies: "
        "{unjudged} · judgment calls: {judgments}".format(
            claims=coverage["claims"]["total"],
            studies=coverage["studies"]["total"],
            unjudged=len(coverage["unjudged_studies"]),
            judgments=len(coverage["judgment_call_studies"]),
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
