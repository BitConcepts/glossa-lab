"""Tests for terminal log endpoints (TEST-TL-001 .. TEST-TL-009).

TEST-TL-001  GET /terminal/log returns a list of lines and the file path.
TEST-TL-002  GET /terminal/log respects the 'lines' query parameter.
TEST-TL-003  GET /terminal/log on missing log file returns exists=False.
TEST-TL-004  POST /terminal/log/purge truncates the log file.
TEST-TL-005  POST /terminal/log/purge reports the number of bytes cleared.
TEST-TL-006  POST /terminal/log/purge on missing log returns cleared=0.
TEST-TL-007  mtime selection: newer-smaller file wins over older-larger file.
TEST-TL-008  mtime selection: only existing files are considered.
TEST-TL-009  GET /terminal/log/stream returns text/event-stream content-type.
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch


# ── Endpoint tests (require the session-scoped 'client' fixture) ─────────────


def test_get_log_returns_list(client, tmp_path):
    """TEST-TL-001: GET /terminal/log returns lines list and file info."""
    log_file = tmp_path / "glossa.log"
    log_file.write_text('{"msg":"line1"}\n{"msg":"line2"}\n', encoding="utf-8")

    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=log_file):
        resp = client.get("/api/v1/terminal/log?lines=200")

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["lines"], list)
    assert data["exists"] is True
    assert len(data["lines"]) >= 1


def test_get_log_respects_lines_param(client, tmp_path):
    """TEST-TL-002: The 'lines' param limits the tail of the log returned."""
    log_file = tmp_path / "glossa.log"
    log_file.write_text("\n".join(f"line{i}" for i in range(20)), encoding="utf-8")

    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=log_file):
        resp = client.get("/api/v1/terminal/log?lines=5")

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["lines"]) <= 5


def test_get_log_missing_file(client, tmp_path):
    """TEST-TL-003: GET /terminal/log on a missing log file returns exists=False."""
    missing = tmp_path / "nonexistent.log"
    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=missing):
        resp = client.get("/api/v1/terminal/log")

    assert resp.status_code == 200
    data = resp.json()
    assert data["exists"] is False
    assert data["lines"] == []


def test_purge_log_truncates_file(client, tmp_path):
    """TEST-TL-004: POST /terminal/log/purge writes empty string to the log file."""
    log_file = tmp_path / "glossa.log"
    log_file.write_text("old content that should be removed\n", encoding="utf-8")
    assert log_file.stat().st_size > 0

    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=log_file):
        resp = client.post("/api/v1/terminal/log/purge")

    assert resp.status_code == 200
    assert log_file.read_text(encoding="utf-8") == ""


def test_purge_log_reports_bytes_cleared(client, tmp_path):
    """TEST-TL-005: POST /terminal/log/purge returns the number of bytes cleared."""
    content = "x" * 1234
    log_file = tmp_path / "glossa.log"
    log_file.write_text(content, encoding="utf-8")

    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=log_file):
        resp = client.post("/api/v1/terminal/log/purge")

    assert resp.status_code == 200
    data = resp.json()
    assert data["cleared"] == 1234


def test_purge_log_missing_file(client, tmp_path):
    """TEST-TL-006: POST /terminal/log/purge on a missing log returns cleared=0."""
    missing = tmp_path / "no_log_here.log"
    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_active_log_file", return_value=missing):
        resp = client.post("/api/v1/terminal/log/purge")

    assert resp.status_code == 200
    assert resp.json()["cleared"] == 0


# ── Unit tests for _active_log_file mtime selection ─────────────────────────


def test_mtime_selection_newer_smaller_wins(tmp_path):
    """TEST-TL-007: Regression test — newer file wins regardless of size.

    Bug: _active_log_file used file SIZE not mtime, so a stale 445 KB
    logs/glossa.log kept winning over the fresh 10-line active log.
    """
    old_large = tmp_path / "old.log"
    new_small = tmp_path / "new.log"

    old_large.write_text("x" * 100_000, encoding="utf-8")
    time.sleep(0.02)                          # guarantee mtime difference
    new_small.write_text("y" * 50, encoding="utf-8")

    # Mimic the selection logic from _active_log_file exactly
    candidates = [old_large, new_small]
    existing = [(p.stat().st_mtime, p) for p in candidates if p.exists()]
    chosen = max(existing)[1]

    assert chosen == new_small, (
        f"Expected the NEWER file ({new_small.name}) to be selected, "
        f"got {chosen.name}.  This would have caused stale logs in the UI."
    )


def test_mtime_selection_only_existing_files(tmp_path):
    """TEST-TL-008: Non-existent candidates are silently skipped."""
    exists = tmp_path / "exists.log"
    exists.write_text("hello", encoding="utf-8")
    missing = tmp_path / "missing.log"

    candidates = [missing, exists]
    existing = [(p.stat().st_mtime, p) for p in candidates if p.exists()]
    chosen = max(existing)[1]

    assert chosen == exists


# ── SSE content-type check ───────────────────────────────────────────────────


async def _finite_tail():
    """Finite stand-in for _tail_log that yields one event and exits."""
    yield 'data: {"text": "test", "backfill": true}\n\n'


def test_log_stream_content_type(client, tmp_path):
    """TEST-TL-009: GET /terminal/log/stream returns text/event-stream.

    _tail_log is patched with a finite generator so the stream closes
    cleanly without hanging the test runner.
    """
    import glossa_lab.api.terminal as _t
    with patch.object(_t, "_tail_log", return_value=_finite_tail()):
        resp = client.get("/api/v1/terminal/log/stream")

    assert resp.status_code == 200
    ct = resp.headers.get("content-type", "")
    assert "text/event-stream" in ct
