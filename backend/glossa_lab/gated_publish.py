"""Spec 086 Stage 3 — gated publication of the generated
artifacts (T303, C086-11).

The publish path for the generated artifacts (the matrix
since Stage 3; the map since Stage 5, T502 — `publish_map`
below runs the same mechanics over the map artifact):

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
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li
from glossa_lab import map_generate as mp
from glossa_lab import matrix_generate as mg
from glossa_lab.ledger_gate import run_gate

MATRIX_REL_DIR = "glossa-indus/matrix"
MAP_REL_DIR = "glossa-indus/map"
_CANDIDATE_DIRNAME = ".candidates"
_MATRIX_FILES = ("matrix.json", "matrix.md")
_MAP_FILES = ("map-data.json",)


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
