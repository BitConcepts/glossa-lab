"""Behavior tests for the tray supervisor (Spec 080 FR-006) and the
2026-10-29 UI-log audit fixes.

The tray module exits at import when pystray/Pillow are missing, so
these tests install minimal stubs into ``sys.modules`` first and
import the module fresh from its file path for each test (fresh
module globals per test). Everything is headless; Windows branches
are exercised by faking ``platform.system``.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import time
import types
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TRAY_MAIN = REPO / "tray" / "glossa_tray" / "main.py"


def _load_tray():
    """Import tray/glossa_tray/main.py fresh, with pystray/PIL stubbed."""
    if "pystray" not in sys.modules:
        sys.modules["pystray"] = types.ModuleType("pystray")
    if "PIL" not in sys.modules:
        pil = types.ModuleType("PIL")
        image = types.ModuleType("PIL.Image")
        draw = types.ModuleType("PIL.ImageDraw")
        pil.Image = image
        pil.ImageDraw = draw
        sys.modules["PIL"] = pil
        sys.modules["PIL.Image"] = image
        sys.modules["PIL.ImageDraw"] = draw
    spec = importlib.util.spec_from_file_location(
        "glossa_tray_main_under_test", TRAY_MAIN
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _instrument(mod, monkeypatch):
    """Route the tray log to a list; return the list."""
    lines: list[str] = []
    monkeypatch.setattr(mod, "_tray_log", lines.append)
    return lines


def _fake_windows(mod, monkeypatch):
    monkeypatch.setattr(mod.platform, "system", lambda: "Windows")


# ── Auto-restart supervision (FR-006) ─────────────────────


def test_auto_restart_never_duplicates_an_in_flight_start(monkeypatch):
    """A start still booting must not be restarted over: duplicate
    spawns race for the port (Errno 10048) and burn the restart cap."""
    mod = _load_tray()
    _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    starts: list[int] = []
    monkeypatch.setattr(mod, "_start_backend", lambda *a, **k: starts.append(1))
    mod._backend_starting = True
    mod._backend_start_mono = time.monotonic()

    assert mod._maybe_auto_restart() == "starting"
    assert starts == []


def test_auto_restart_resumes_after_start_grace_expires(monkeypatch):
    """A start that never came up within the grace window is treated
    as failed, logged, and supervision resumes."""
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    starts: list[int] = []
    monkeypatch.setattr(mod, "_start_backend", lambda *a, **k: starts.append(1))
    mod._backend_starting = True
    mod._backend_start_mono = time.monotonic() - (mod._START_GRACE_SEC + 5)

    assert mod._maybe_auto_restart() == "restarted"
    assert starts == [1]
    assert any("did not come up" in line for line in lines)


def test_auto_restart_cap_is_logged_once(monkeypatch):
    """Hitting the restart cap is recorded once, not once per poll."""
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    now = time.monotonic()
    mod._restart_times[:] = [now, now, now]

    assert mod._maybe_auto_restart() == "cap-reached"
    assert mod._maybe_auto_restart() == "cap-reached"
    cap_lines = [line for line in lines if "cap reached" in line]
    assert len(cap_lines) == 1


def test_user_stop_is_never_overridden(monkeypatch):
    mod = _load_tray()
    _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    starts: list[int] = []
    monkeypatch.setattr(mod, "_start_backend", lambda *a, **k: starts.append(1))
    mod._user_stopped = True

    assert mod._maybe_auto_restart() == "user-stopped"
    assert starts == []


# ── Poller liveness ───────────────────────────────────────


class _Sentinel(BaseException):
    """Breaks out of the poller's renewal loop in tests."""


def test_status_poller_renews_after_a_segment_failure(monkeypatch):
    """A crashed segment is logged and a fresh segment begins —
    supervision never ends silently (the old poller exited after
    ~24 h with only a print, invisible under pythonw)."""
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    calls: list[int] = []

    def fake_segment(_icon):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("boom")
        raise _Sentinel

    monkeypatch.setattr(mod, "_poll_segment", fake_segment)
    with pytest.raises(_Sentinel):
        mod._status_poller(object())
    assert len(calls) == 2
    assert any("segment 1 failed" in line for line in lines)


def test_poll_segment_survives_one_bad_poll(monkeypatch):
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    monkeypatch.setattr(mod, "_MAX_POLL_ITERATIONS", 3)
    monkeypatch.setattr(mod, "POLL_INTERVAL", 0)
    calls: list[int] = []

    def fake_poll_once(_icon):
        calls.append(1)
        if len(calls) == 2:
            raise RuntimeError("transient")

    monkeypatch.setattr(mod, "_poll_once", fake_poll_once)
    mod._poll_segment(object())
    assert len(calls) == 3
    assert any("status poll failed" in line for line in lines)


# ── Tray log ──────────────────────────────────────────────


def test_tray_log_writes_timestamped_lines(tmp_path, monkeypatch):
    mod = _load_tray()
    log = tmp_path / "tray.log"
    monkeypatch.setattr(mod, "_TRAY_LOG", log)
    mod._tray_log("hello tray")
    text = log.read_text(encoding="utf-8")
    assert re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} hello tray$", text, re.M)


def test_tray_log_rotates_when_oversized(tmp_path, monkeypatch):
    mod = _load_tray()
    log = tmp_path / "tray.log"
    log.write_text("x" * 500, encoding="utf-8")
    monkeypatch.setattr(mod, "_TRAY_LOG", log)
    monkeypatch.setattr(mod, "_MAX_LOG_BYTES", 100)
    mod._tray_log("fresh line")
    assert (tmp_path / "tray.1.log").exists()
    assert "fresh line" in log.read_text(encoding="utf-8")


# ── Config honesty ────────────────────────────────────────


def test_config_load_failure_is_logged_not_silent(tmp_path, monkeypatch):
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    bad = tmp_path / "config.json"
    bad.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(mod, "_CONFIG_FILE", bad)
    assert mod._load_config() == {}
    assert any("config load failed" in line for line in lines)


# ── Start / stop honesty ──────────────────────────────────


def test_start_backend_spawn_failure_is_logged_not_raised(tmp_path, monkeypatch):
    """A Popen failure (missing venv pythonw) must not kill the tray;
    it is logged, the starting flag cleared, and False returned."""
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    monkeypatch.setattr(mod, "_BACKEND_LOG", tmp_path / "backend.log")

    def boom(*_a, **_k):
        raise OSError("pythonw missing")

    monkeypatch.setattr(mod.subprocess, "Popen", boom)
    assert mod._start_backend() is False
    assert mod._backend_starting is False
    assert mod._status_error is True
    assert any("backend start failed" in line for line in lines)


class _Resp:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False

    def read(self) -> bytes:
        return self._body


def test_stop_backend_kills_listener_when_shutdown_request_fails(monkeypatch):
    """The documented stop fallback is real: when the shutdown POST
    fails and the backend keeps answering, the listener is killed
    and the outcome is logged."""
    mod = _load_tray()
    lines = _instrument(mod, monkeypatch)
    _fake_windows(mod, monkeypatch)
    monkeypatch.setattr(mod.time, "sleep", lambda *_a: None)
    state = {"killed": False}

    def fake_urlopen(req, timeout=0):  # noqa: ARG001
        url = req.full_url
        if "shutdown" in url or state["killed"]:
            raise OSError("connection refused")
        return _Resp(b'{"status": "healthy", "version": "0.1.0", "uptime_seconds": 7}')

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(mod, "_listener_pid", lambda _port: 4242)
    killed: list[list[str]] = []

    def fake_run(cmd, **_k):
        killed.append(list(cmd))
        state["killed"] = True
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(mod.subprocess, "run", fake_run)
    mod._stop_backend()

    assert killed and "4242" in killed[0]
    assert any("shutdown request failed" in line for line in lines)
    assert any("via kill fallback" in line for line in lines)
