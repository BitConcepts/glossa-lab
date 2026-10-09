"""Tests for backend/scripts/release_gate.py — the release hash gate.

TEST-RG-001  A staged set byte-identical to its named repo sources
             passes (exit 0, every entry MATCH).
TEST-RG-002  A one-byte mutation of a staged file fails (exit 1,
             that entry MISMATCH) — the v4.2.0 failure class.
TEST-RG-003  A missing repo source fails (exit 1, MISSING-SOURCE).
TEST-RG-004  A missing staged file fails (exit 1, MISSING-STAGED).
TEST-RG-005  An external-source entry behaves as specified: no repo
             source is consulted; a present staged file passes as
             EXTERNAL (exit 0) and its hash is reported; a missing
             staged external file fails (exit 1).
TEST-RG-006  A malformed manifest (entry with both / neither of
             source and external_source) is a usage error (exit 2).
TEST-RG-007  CRLF drift fails: the same parsed JSON re-serialised
             with CRLF line endings is a MISMATCH on raw bytes —
             the exact v4.2.0 anchors divergence (audit §3).

The gate module is loaded from its script path (it is a script, not
a package module); the CLI is exercised via subprocess.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "release_gate.py"


def _load_gate():
    spec = importlib.util.spec_from_file_location("release_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GATE = _load_gate()


def _setup(tmp_path: Path, staged_bytes: bytes = b'{"a": 1}\n',
           source_bytes: bytes | None = b'{"a": 1}\n'):
    """Build repo/ + staging/ + manifest in tmp_path; return paths."""
    repo = tmp_path / "repo"
    staging = tmp_path / "staging"
    (repo / "data").mkdir(parents=True)
    staging.mkdir()
    if source_bytes is not None:
        (repo / "data" / "anchors.json").write_bytes(source_bytes)
    (staging / "anchors.json").write_bytes(staged_bytes)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"files": [
        {"deposit_name": "anchors.json", "source": "data/anchors.json"},
    ]}), encoding="utf-8")
    return repo, staging, manifest


def _run_cli(manifest: Path, staging: Path, repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest),
         "--staging-dir", str(staging), "--repo-root", str(repo)],
        capture_output=True, text=True, timeout=60,
    )


def test_matching_set_passes(tmp_path):
    repo, staging, manifest = _setup(tmp_path)
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 0
    assert [r["status"] for r in results] == ["MATCH"]
    assert results[0]["staged_sha256"] == results[0]["source_sha256"]
    proc = _run_cli(manifest, staging, repo)
    assert proc.returncode == 0, proc.stderr
    assert "MATCH" in proc.stdout and "PASS" in proc.stdout


def test_one_byte_mutation_fails(tmp_path):
    repo, staging, manifest = _setup(tmp_path, staged_bytes=b'{"a": 2}\n')
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 1
    assert results[0]["status"] == "MISMATCH"
    proc = _run_cli(manifest, staging, repo)
    assert proc.returncode == 1
    assert "MISMATCH" in proc.stdout and "FAIL" in proc.stdout


def test_missing_source_fails(tmp_path):
    repo, staging, manifest = _setup(tmp_path, source_bytes=None)
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 1
    assert results[0]["status"] == "MISSING-SOURCE"
    assert _run_cli(manifest, staging, repo).returncode == 1


def test_missing_staged_fails(tmp_path):
    repo, staging, manifest = _setup(tmp_path)
    (staging / "anchors.json").unlink()
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 1
    assert results[0]["status"] == "MISSING-STAGED"


def test_external_source_entry(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "note.md").write_bytes(b"supplementary note\n")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"files": [
        {"deposit_name": "note.md",
         "external_source": "Authored outside the repo; reviewed by owner"},
    ]}), encoding="utf-8")

    # Present staged external file: passes as EXTERNAL, hash reported,
    # no repo source consulted (repo is empty).
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 0
    assert results[0]["status"] == "EXTERNAL"
    assert results[0]["source"] is None
    assert results[0]["staged_sha256"] is not None
    assert _run_cli(manifest, staging, repo).returncode == 0

    # Missing staged external file: fails.
    (staging / "note.md").unlink()
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 1
    assert results[0]["status"] == "MISSING-STAGED"


def test_malformed_manifest_is_usage_error(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"files": [
        {"deposit_name": "x.json", "source": "a.json",
         "external_source": "both set — invalid"},
    ]}), encoding="utf-8")
    proc = _run_cli(manifest, staging, tmp_path)
    assert proc.returncode == 2


def test_crlf_drift_fails(tmp_path):
    lf = b'{\n  "a": 1\n}\n'
    crlf = lf.replace(b"\n", b"\r\n")
    repo, staging, manifest = _setup(
        tmp_path, staged_bytes=crlf, source_bytes=lf)
    # Same parsed JSON, different bytes: the gate hashes raw bytes,
    # so this must fail — it is the v4.2.0 anchors divergence.
    assert json.loads(crlf) == json.loads(lf)
    results, code = GATE.run_gate(manifest, staging, repo)
    assert code == 1
    assert results[0]["status"] == "MISMATCH"
