"""Spec 026 Stage S2 — register completeness + drift tests (FR-026-5)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / "specs" / "026-rcph-framework-transfer"

EXPECTED_RERUN_REQUIRED = {
    "SPEC-023", "SPEC-024", "SPEC-025",
    "PHASE-132", "PHASE-134", "PHASE-135", "PHASE-137", "PHASE-140",
}


def _register() -> list[dict]:
    return json.loads((SPEC_DIR / "impact-register.json").read_text())["register"]


def test_register_covers_inventory_exactly() -> None:
    inventory = json.loads((SPEC_DIR / "working" / "inventory.json").read_text())
    rows = _register()
    assert len(rows) == len(inventory)
    assert {r["item_id"] for r in rows} == {i["item_id"] for i in inventory}


def test_register_classes_valid_and_rerun_set_exact() -> None:
    rows = _register()
    classes = {"RERUN-REQUIRED", "REPRODUCE-ONLY", "REINTERPRET-ONLY",
               "UNAFFECTED", "NOT-RERUNNABLE"}
    assert all(r["classification"] in classes for r in rows)
    assert all(r["rationale"] for r in rows)
    rerun = {r["item_id"] for r in rows if r["classification"] == "RERUN-REQUIRED"}
    assert rerun == EXPECTED_RERUN_REQUIRED
    assert all(r["rerun_spec"] for r in rows if r["classification"] == "RERUN-REQUIRED")


def test_register_files_do_not_drift() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "backend" / "scripts" / "spec026_register_build.py"), "--check"],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
