#!/usr/bin/env python3
"""Generate the Spec 087 S4 manual blocks (Stage S4, T401).

Runs the pure builder in `backend/glossa_lab/manual_generate.py`
over the live node registry and the graph files on disk, and
writes the three generated surfaces:

- the delimited Node Reference block in `docs/user-manual.md`,
- the HelpView data module
  `frontend/src/components/help/nodeReference.generated.ts`,
- the delimited active-experiments block in `docs/USER_GUIDE.md`.

One generation feeds all three — the manual's node reference is
the palette set (registered-minus-legacy) with each node's
category, ports, and params as the registry states them, and the
USER_GUIDE list is the graph files on disk, neither more nor
fewer. Delete-and-regenerate over an unchanged registry and
unchanged graph files reproduces the committed bytes exactly.

Usage (from the repo root):

    python3 tools/manual/generate_node_reference.py [--root PATH]
                                                    [--check]

`--check` builds without writing and exits 0 only if every
committed surface is byte-identical to the fresh build (the CI
conformance test in backend/tests/test_manual_conformance.py
runs the same check through the builder).

Exit code 0 on success, 1 on a named refusal (a missing or
duplicated delimiter, an unreadable graph file) — on a refusal
nothing is written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.manual_generate import (  # noqa: E402
    ManualBuildError,
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
        help="build only; exit 0 iff committed surfaces match the build",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.check:
            drifted = check_outputs(root)
            if drifted:
                print("DRIFT in generated manual surfaces:")
                for name in drifted:
                    print(f"  {name}")
                print(
                    "Regenerate with: "
                    "python3 tools/manual/generate_node_reference.py"
                )
                return 1
            print("OK: generated manual surfaces match the live registry")
            return 0
        written = write_outputs(root)
    except ManualBuildError as exc:
        print(f"REFUSED: {exc}")
        return 1
    for name in written:
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
