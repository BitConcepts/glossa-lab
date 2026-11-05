"""Spec 083 (T057) — workspace-scope reconciliation checker tests.

Fixture SQLite datasets pin the checker's contract: scoped classes
fail loudly on unscoped ('') or misassigned (dangling) project ids,
global classes are counted and named (never silently passed), the
experiments linkage is reported, a missing primary workspace fails,
and the evidence-store ownership must name the primary program.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from glossa_lab.workspace_scope_check import (
    check_database,
    check_store_ownership,
    run_check,
)


def _make_db(path: Path, *, notebooks: list[str], primary: bool = True) -> Path:
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "CREATE TABLE projects (id TEXT PRIMARY KEY, label TEXT,"
            " experiment_ids TEXT NOT NULL DEFAULT '[]')"
        )
        if primary:
            conn.execute(
                "INSERT INTO projects VALUES ('indus_decipherment', 'Indus', ?)",
                (json.dumps(["exp-1", "exp-2"]),),
            )
        conn.execute(
            "INSERT INTO projects VALUES ('other-proj', 'Other', '[]')"
        )
        conn.execute(
            "CREATE TABLE notebooks (id TEXT PRIMARY KEY,"
            " project_id TEXT NOT NULL DEFAULT '')"
        )
        for i, pid in enumerate(notebooks):
            conn.execute(
                "INSERT INTO notebooks VALUES (?, ?)", (f"nb-{i}", pid)
            )
        conn.execute("CREATE TABLE studies (id TEXT PRIMARY KEY)")
        conn.execute("INSERT INTO studies VALUES ('st-1')")
        conn.execute("INSERT INTO studies VALUES ('st-2')")
        conn.commit()
    finally:
        conn.close()
    return path


def _lines_by_name(lines):
    return {line.name: line for line in lines}


def test_clean_dataset_passes(tmp_path):
    db = _make_db(
        tmp_path / "glossa.db",
        notebooks=["indus_decipherment", "other-proj"],
    )
    lines = _lines_by_name(check_database(db))
    assert lines["projects"].violations == 0
    nb = lines["notebooks"]
    assert nb.kind == "scoped" and nb.violations == 0
    assert "total=2" in nb.detail and "primary=1" in nb.detail
    assert "other-workspace=1" in nb.detail
    studies = lines["studies"]
    assert studies.kind == "global" and "count=2" in studies.detail
    exp = lines["experiments"]
    assert exp.kind == "linkage" and "linked_ids=2" in exp.detail


def test_unscoped_and_misassigned_fail_loudly(tmp_path):
    db = _make_db(
        tmp_path / "glossa.db",
        notebooks=["indus_decipherment", "", "ghost-project"],
    )
    lines = _lines_by_name(check_database(db))
    nb = lines["notebooks"]
    assert nb.violations == 2
    assert "unscoped=1" in nb.detail and "misassigned=1" in nb.detail


def test_missing_primary_workspace_fails(tmp_path):
    db = _make_db(tmp_path / "glossa.db", notebooks=[], primary=False)
    lines = _lines_by_name(check_database(db))
    assert lines["projects"].violations == 1
    assert "present=NO" in lines["projects"].detail


def test_store_ownership_must_name_the_primary(tmp_path):
    source = tmp_path / "backend" / "glossa_lab" / "api" / "indus_evidence.py"
    source.parent.mkdir(parents=True)
    source.write_text('_STORE_PROGRAM_ID = "indus_decipherment"\n', encoding="utf-8")
    line = check_store_ownership(tmp_path)
    assert line.violations == 0 and "consistent=yes" in line.detail

    source.write_text('_STORE_PROGRAM_ID = "someone-else"\n', encoding="utf-8")
    line = check_store_ownership(tmp_path)
    assert line.violations == 1 and "consistent=NO" in line.detail

    line = check_store_ownership(tmp_path / "nonexistent")
    assert line.violations == 1 and "UNVERIFIABLE" in line.detail


def test_run_check_verdict_and_missing_db(tmp_path):
    repo = tmp_path / "repo"
    source = repo / "backend" / "glossa_lab" / "api" / "indus_evidence.py"
    source.parent.mkdir(parents=True)
    source.write_text('_STORE_PROGRAM_ID = "indus_decipherment"\n', encoding="utf-8")
    data = tmp_path / "data"
    data.mkdir()
    _make_db(data / "glossa.db", notebooks=["indus_decipherment"])
    report = run_check(data, repo)
    assert report.verdict == "PASS" and report.violations == 0
    assert "VERDICT: PASS" in report.render()

    empty = tmp_path / "empty"
    empty.mkdir()
    report = run_check(empty, repo)
    assert report.verdict == "FAIL"
    assert "MISSING" in report.render()
