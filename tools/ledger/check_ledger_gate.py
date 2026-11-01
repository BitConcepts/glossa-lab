#!/usr/bin/env python3
"""Run the Spec 086 verification gate (Stage 3, T301).

Recomputes the matrix (and, when present, the map) from the
ledger by the gate's own independent route and checks the
chain under classes V1–V9 of spec.md Point 4 (V8, the
settling canonicals, arrived with Stage 4). The gate never writes: bytecode
writing is disabled before any backend module is imported,
and the gate calls only pure builders and read paths
(parent-carried write-freedom requirement; V9 audits the
gate's own imports).

Usage (from the repo root):

    python3 tools/ledger/check_ledger_gate.py [--root PATH]
        [--all]                       full mode (default)
        [--pr-scope --base REF]       only the classes covering
                                      the layers the change touches
        [--regen]                     also run V7: hash,
                                      regenerate, byte-compare,
                                      classify any diff
        [--candidate PATH]            check a candidate
                                      matrix.json instead of the
                                      published artifact
        [--candidate-map PATH]        check a candidate map
                                      artifact (V2/V4/V5/V6 legs)
        [--intended-change NAME]      name an intended change
                                      for --regen classification

Exit code 0 iff no check FAILs. The printed output is the
gate output the stage records file verbatim.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.ledger_gate import run_gate  # noqa: E402

# PR-scope layer map: a changed path pulls in the check
# classes covering the layers it touches (spec.md Point 4:
# "--pr-scope on PRs (gate over the artifacts the change
# touches)"). Machinery changes run the full gate.
_LAYER_CLASSES = {
    "ledger": {"V1", "V2", "V3", "V4", "V8", "V9"},
    "matrix": {"V2", "V3", "V4"},
    "map": {"V2", "V4", "V5", "V6"},
    "anchors": {"V4", "V6", "V8"},
}
_MACHINERY = (
    "backend/glossa_lab/ledger_gate.py",
    "backend/glossa_lab/gated_publish.py",
    "backend/glossa_lab/settling.py",
    "tools/ledger/",
    ".github/workflows/ci.yml",
)


def _layer_of(path: str) -> str | None:
    if (
        path.startswith("glossa-indus/ledger/")
        or path == "backend/glossa_lab/ledger_intake.py"
        or path == "backend/glossa_lab/proposition_fingerprint.py"
    ):
        return "ledger"
    if path.startswith("glossa-indus/matrix/") or path == (
        "backend/glossa_lab/matrix_generate.py"
    ):
        return "matrix"
    if path.startswith("glossa-indus/map/"):
        return "map"
    if path in (
        "backend/reports/INDUS_FINAL_ANCHORS.json",
        "reports/phase108_provenance_register.json",
    ):
        return "anchors"
    return None


def pr_scope(root: Path, base: str) -> tuple[set[str] | None, str]:
    """The class set for a PR-scope run, and a note. A None
    set means 'run everything' (machinery touched, or the
    diff could not be taken — the gate falls back to full
    rather than silently passing)."""
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if diff.returncode != 0:
        return None, (
            f"git diff against {base} failed ({diff.stderr.strip()}); "
            "falling back to a full gate run"
        )
    changed = [line for line in diff.stdout.splitlines() if line.strip()]
    if any(
        path == m or (m.endswith("/") and path.startswith(m))
        for path in changed
        for m in _MACHINERY
    ):
        return None, (
            "gate machinery is touched by this change; full gate run"
        )
    layers: set[str] = set()
    classes: set[str] = set()
    for path in changed:
        layer = _layer_of(path)
        if layer:
            layers.add(layer)
            classes |= _LAYER_CLASSES[layer]
    if not layers:
        return set(), (
            "no ledger-chain artifacts touched by this change; "
            "every class enumerated NOT-RUN"
        )
    return classes, f"layers touched: {', '.join(sorted(layers))}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    parser.add_argument("--all", action="store_true",
                        help="full mode (the default)")
    parser.add_argument("--pr-scope", action="store_true",
                        help="gate only the classes covering the "
                        "layers this change touches")
    parser.add_argument("--base", default="origin/main",
                        help="base ref for --pr-scope diffs")
    parser.add_argument("--regen", action="store_true",
                        help="run V7 lossless regeneration")
    parser.add_argument("--candidate", type=Path, default=None,
                        help="candidate matrix.json to check "
                        "instead of the published artifact")
    parser.add_argument("--candidate-map", type=Path, default=None,
                        help="candidate map artifact to check")
    parser.add_argument("--intended-change", default=None,
                        help="name an intended change for "
                        "--regen diff classification")
    args = parser.parse_args()
    root = args.root.resolve()

    scope: set[str] | None = None
    mode = "full"
    note = None
    if args.pr_scope:
        mode = f"pr-scope (base {args.base})"
        scope, note = pr_scope(root, args.base)
    if args.regen:
        mode += " + regen"

    report = run_gate(
        root,
        mode=mode,
        scope=scope,
        candidate_matrix=args.candidate.resolve() if args.candidate else None,
        candidate_map=args.candidate_map.resolve() if args.candidate_map else None,
        regen=args.regen,
        intended_change=args.intended_change,
    )
    if note:
        report.header.append(f"scope note: {note}")
    sys.stdout.write(report.render())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
