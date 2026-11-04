"""Spec 086 Stage 3 — gated publication of the generated
artifacts (T303, C086-11).

The publish path for the generated artifacts (the matrix
since Stage 3; the map since Stage 5, T502 — `publish_map`
below runs the same mechanics over the map artifact; the
Spec 088 program map since its Stage 4, T403 —
`publish_program_map` runs them over its three artifacts
under the program map's own gate class, V10):

1. a candidate exists — either built here by the pure
   builder from the current ledger, or presented by a
   builder elsewhere (the app-bundle / local build shape
   spec.md Point 4 names: the same candidate → gate →
   replace mechanics apply);
2. the candidate files are staged beside the published
   artifacts;
3. the verification gate (`ledger_gate.run_gate`) runs
   against the candidates — never against the published
   bytes;
4. only on ALL PASS are the presented files replaced
   (atomic `os.replace` per file); on a red gate the
   staging directory is removed and the previously
   published artifacts are byte-untouched.

This module is one of the registered writers of the gated
artifacts (gate check V9's census). The gate itself
(`ledger_gate.py`) contains no write path.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li
from glossa_lab import map_generate as mp
from glossa_lab import matrix_generate as mg
from glossa_lab import program_map_generate as pm
from glossa_lab.ledger_gate import run_gate

MATRIX_REL_DIR = "glossa-indus/matrix"
MAP_REL_DIR = "glossa-indus/map"
_CANDIDATE_DIRNAME = ".candidates"
_MATRIX_FILES = ("matrix.json", "matrix.md")
_MAP_FILES = ("map-data.json",)
_PROGRAM_MAP_FILES = (
    "program-map.json",
    "program-map-finds.json",
    "program-map.html",
)


def publish_matrix(
    root: Path,
    out_dir: Optional[Path] = None,
    *,
    candidate_dir: Optional[Path] = None,
) -> dict[str, Any]:
    """Publish the matrix artifacts through the gate.

    With no ``candidate_dir``, the candidate is built from
    the current ledger by the pure builder. With one, the
    candidate files it holds (matrix.json, and matrix.md
    when present) are the candidate a builder elsewhere
    produced. Returns {"published": bool, "gate":
    GateReport, "written": {...}} — on a red gate,
    "published" is False and the previously published
    artifacts are untouched.
    """
    root = Path(root)
    out = Path(out_dir) if out_dir else (root / MATRIX_REL_DIR)
    if candidate_dir is not None:
        source = Path(candidate_dir)
        candidates = {
            name: (source / name).read_bytes()
            for name in _MATRIX_FILES
            if (source / name).is_file()
        }
        if "matrix.json" not in candidates:
            raise ValueError(
                f"candidate dir {source} holds no matrix.json"
            )
    else:
        build = mg.build_matrix(root)
        candidates = {
            "matrix.json": build.json_bytes,
            "matrix.md": build.md_bytes,
        }
    staging = out / _CANDIDATE_DIRNAME
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        for name, data in candidates.items():
            (staging / name).write_bytes(data)
        report = run_gate(
            root,
            mode="gated publication (candidate)",
            candidate_matrix=staging / "matrix.json",
        )
        if not report.ok:
            return {"published": False, "gate": report, "written": {}}
        written: dict[str, Any] = {}
        for name, data in candidates.items():
            target = out / name
            # Atomic replace: the published file is never
            # observed half-written, and it changes only now
            # that the gate has passed.
            (staging / name).replace(target)
            read_back = target.read_bytes()
            if read_back != data:
                raise RuntimeError(
                    f"publish verification failed for {target}: "
                    "read-back bytes differ from the gated "
                    "candidate bytes"
                )
            written[name] = {
                "path": str(target),
                "sha256": li.canonical_sha256_bytes(read_back),
                "bytes": len(read_back),
            }
        return {"published": True, "gate": report, "written": written}
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def publish_program_map(
    root: Path,
    *,
    candidate_dir: Optional[Path] = None,
) -> dict[str, Any]:
    """Publish the Spec 088 program-map artifacts through
    the gate (Stage 4, T403 — the T303 mechanics over the
    program map's three artifacts).

    With no ``candidate_dir``, the candidates are built from
    the current inputs by the pure builder. With one, the
    candidate files it holds (all three of
    ``_PROGRAM_MAP_FILES``) are the candidates a builder
    elsewhere produced.

    The program map's gate class is V10, which recomputes
    the artifacts from the tree it is run over — so the
    gate runs over a scratch root whose records of record
    are the real tree's (the ledger directory, the taxonomy,
    and the spec tree, by symlink) and whose program-map
    artifacts are the candidates as real files: the verdict
    is over the candidate bytes, never the published ones.
    Only on ALL PASS are the presented files replaced
    (atomic `os.replace` per file); on a red gate the
    previously published artifacts are byte-untouched.
    Returns {"published": bool, "gate": GateReport,
    "written": {...}}.
    """
    # Resolved absolute: the gate scratch root links the
    # records of record, and a relative target would resolve
    # against the scratch root, not this tree.
    root = Path(root).resolve()
    out = root / MAP_REL_DIR
    if candidate_dir is not None:
        source = Path(candidate_dir)
        candidates = {
            name: (source / name).read_bytes()
            for name in _PROGRAM_MAP_FILES
            if (source / name).is_file()
        }
        missing = [
            name for name in _PROGRAM_MAP_FILES if name not in candidates
        ]
        if missing:
            raise ValueError(
                f"candidate dir {source} is missing program-map "
                f"artifact(s): {', '.join(missing)}"
            )
    else:
        candidates = {
            Path(rel).name: text.encode("utf-8")
            for rel, text in pm.build_artifacts(root).items()
        }
    with tempfile.TemporaryDirectory(
        prefix="glossa-program-map-gate-"
    ) as td:
        gate_root = Path(td)
        (gate_root / "glossa-indus").mkdir(parents=True)
        (gate_root / "glossa-indus" / "ledger").symlink_to(
            root / "glossa-indus" / "ledger"
        )
        gate_map_dir = gate_root / MAP_REL_DIR
        gate_map_dir.mkdir(parents=True)
        (gate_map_dir / "program-map-taxonomy.json").symlink_to(
            root / pm.TAXONOMY_REL
        )
        (gate_root / pm.SPECS_REL).symlink_to(root / pm.SPECS_REL)
        for name, data in candidates.items():
            (gate_map_dir / name).write_bytes(data)
        report = run_gate(
            gate_root,
            mode="gated publication (candidate)",
            scope={"V10"},
        )
    if not report.ok:
        return {"published": False, "gate": report, "written": {}}
    staging = out / _CANDIDATE_DIRNAME
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        for name, data in candidates.items():
            (staging / name).write_bytes(data)
        written: dict[str, Any] = {}
        for name, data in candidates.items():
            target = out / name
            (staging / name).replace(target)
            read_back = target.read_bytes()
            if read_back != data:
                raise RuntimeError(
                    f"publish verification failed for {target}: "
                    "read-back bytes differ from the gated "
                    "candidate bytes"
                )
            written[name] = {
                "path": str(target),
                "sha256": li.canonical_sha256_bytes(read_back),
                "bytes": len(read_back),
            }
        return {"published": True, "gate": report, "written": written}
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def publish_map(
    root: Path,
    out_dir: Optional[Path] = None,
    *,
    candidate_dir: Optional[Path] = None,
) -> dict[str, Any]:
    """Publish the map artifact through the gate (Stage 5,
    T502 — the T303 mechanics over the map).

    With no ``candidate_dir``, the candidate is built from
    the current ledger by the pure map builder. With one,
    the candidate file it holds (map-data.json) is the
    candidate a builder elsewhere produced. Returns
    {"published": bool, "gate": GateReport, "written":
    {...}} — on a red gate, "published" is False and the
    previously published artifact is untouched.
    """
    root = Path(root)
    out = Path(out_dir) if out_dir else (root / MAP_REL_DIR)
    if candidate_dir is not None:
        source = Path(candidate_dir)
        candidates = {
            name: (source / name).read_bytes()
            for name in _MAP_FILES
            if (source / name).is_file()
        }
        if "map-data.json" not in candidates:
            raise ValueError(
                f"candidate dir {source} holds no map-data.json"
            )
    else:
        build = mp.build_map(root)
        candidates = {"map-data.json": build.json_bytes}
    staging = out / _CANDIDATE_DIRNAME
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        for name, data in candidates.items():
            (staging / name).write_bytes(data)
        report = run_gate(
            root,
            mode="gated publication (candidate)",
            candidate_map=staging / "map-data.json",
        )
        if not report.ok:
            return {"published": False, "gate": report, "written": {}}
        written: dict[str, Any] = {}
        for name, data in candidates.items():
            target = out / name
            # Atomic replace: the published file is never
            # observed half-written, and it changes only now
            # that the gate has passed.
            (staging / name).replace(target)
            read_back = target.read_bytes()
            if read_back != data:
                raise RuntimeError(
                    f"publish verification failed for {target}: "
                    "read-back bytes differ from the gated "
                    "candidate bytes"
                )
            written[name] = {
                "path": str(target),
                "sha256": li.canonical_sha256_bytes(read_back),
                "bytes": len(read_back),
            }
        return {"published": True, "gate": report, "written": written}
    finally:
        if staging.exists():
            shutil.rmtree(staging)
