"""Tests for backend/scripts/foundation_check.py repo-root resolution.

TEST-FCS-001  resolve_repo_root honours the GLOSSA_REPO_ROOT env override.
TEST-FCS-002  resolve_repo_root defaults to the script-location-derived root
              (backend/scripts/ -> repo root), with no hardcoded user path.
TEST-FCS-003  The script source contains no hardcoded Windows user path.
TEST-FCS-004  Integration: the script runs end-to-end against the real repo
              (skipped when the gitignored Holdat corpus is not downloaded)
              and reports 0 failures.

The resolver is extracted from the script source via ``ast`` so importing it
does not execute the (module-level) check body.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "foundation_check.py"
HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"


def _load_resolver(script_file: Path):
    """Exec only resolve_repo_root() from the script, in isolation."""
    tree = ast.parse(script_file.read_text(encoding="utf-8"))
    fn = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "resolve_repo_root"
    )
    ns: dict = {"os": os, "Path": Path, "__file__": str(script_file)}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(script_file), "exec"), ns)
    return ns["resolve_repo_root"]


def test_resolver_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("GLOSSA_REPO_ROOT", str(tmp_path))
    resolve = _load_resolver(SCRIPT)
    assert resolve() == tmp_path


def test_resolver_default_from_script_location(monkeypatch, tmp_path):
    monkeypatch.delenv("GLOSSA_REPO_ROOT", raising=False)
    fake_script = tmp_path / "repo" / "backend" / "scripts" / "foundation_check.py"
    fake_script.parent.mkdir(parents=True)
    fake_script.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    resolve = _load_resolver(fake_script)
    assert resolve() == tmp_path / "repo"


def test_resolver_default_matches_this_repo(monkeypatch):
    monkeypatch.delenv("GLOSSA_REPO_ROOT", raising=False)
    resolve = _load_resolver(SCRIPT)
    assert resolve() == REPO


def test_no_hardcoded_windows_user_path():
    src = SCRIPT.read_text(encoding="utf-8")
    assert "C:\\Users" not in src
    assert "C:/Users" not in src


def _load_fallback_fn(script_file: Path):
    """Exec only apply_fallback_caveats() from the script, in isolation."""
    tree = ast.parse(script_file.read_text(encoding="utf-8"))
    fn = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "apply_fallback_caveats"
    )
    ns: dict = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(script_file), "exec"), ns)
    return ns["apply_fallback_caveats"]


def test_fallback_claim_cannot_stay_solid():
    """E-6: a claim generated from fallback inputs cannot come out VERIFIED-solid."""
    apply_fn = _load_fallback_fn(SCRIPT)
    solid = [("P30-A1 permutation null", "score 7.0", "VERIFIED — but simplified"),
             ("Other claim", "d", "VERIFIED")]
    solid_out, caveated_out = apply_fn(
        solid, [], {"P30-A1 permutation null": "NOT VERIFIED — fallback"})
    assert [c[0] for c in solid_out] == ["Other claim"]
    assert caveated_out == [("P30-A1 permutation null", "score 7.0",
                             "NOT VERIFIED — fallback")]


def test_fallback_noop_without_fallbacks():
    apply_fn = _load_fallback_fn(SCRIPT)
    solid = [("A", "d", "VERIFIED")]
    caveated = [("B", "d", "NEEDS CAVEAT")]
    assert apply_fn(solid, caveated, {}) == (solid, caveated)


def test_committed_report_carries_e6_and_e10_fixes():
    """The committed (regenerated) report: P30-A1 caveated, no 'decoded' solids."""
    report = json.loads((REPO / "reports" / "foundation_check_report.json")
                        .read_text("utf-8"))
    assert (report["n_ok"], report["n_fail"], report["n_warn"]) == (39, 0, 9)
    solid_names = [c["claim"] for c in report["solid_claims"]]
    assert "P30-A1 permutation null" not in solid_names
    p30 = [c for c in report["caveated_claims"]
           if c["claim"] == "P30-A1 permutation null"]
    assert len(p30) == 1
    assert "NOT VERIFIED" in p30[0]["status"]
    assert "fallback" in p30[0]["status"]
    for entry in report["solid_claims"]:
        assert "decoded" not in entry["claim"].lower()
        assert "decoded" not in entry["detail"].lower()


def test_phase169_generator_annotates_withdrawn_figure():
    """E-7 residual: the phase169 generator emits the WITHDRAWN status sibling."""
    src = (REPO / "backend" / "scripts" / "phase169_master_synthesis.py") \
        .read_text(encoding="utf-8")
    assert '"aggregate_confidence_pct_status"' in src
    assert "WITHDRAWN 2026-10-23" in src


@pytest.mark.skipif(not HOLDAT.exists(), reason="Holdat corpus not downloaded (gitignored corpora/)")
def test_foundation_check_script_runs_clean():
    env = dict(os.environ, GLOSSA_REPO_ROOT=str(REPO))
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=600, env=env,
        cwd=str(REPO),
    )
    assert proc.returncode == 0, proc.stderr[-500:]
    assert "0 failed" in proc.stdout
    report = json.loads((REPO / "reports" / "foundation_check_report.json").read_text("utf-8"))
    assert report["n_fail"] == 0
