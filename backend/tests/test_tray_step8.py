"""Spec 081 step 8 (T020) — tray amendments, headless.

Mirrors tests/test_tray_token_auth.py's loader: pystray/Pillow are
stubbed in ``sys.modules`` and the tray module is imported fresh
from its file path. Covers wireframe 15's contract: humanized
uptime, status lines that name the open program (and say which
kind of stop a stop is), the single-instance lock (acquire / deny
+ focus marker / stale takeover / release), the focus hand-off's
poller half, the active-program read (label / 404 / transport
failure), and the "View status & session log" URL shapes.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import time
import types
import urllib.error

import pytest

REPO = None  # set below (kept import-order simple)
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TRAY_MAIN = REPO / "tray" / "glossa_tray" / "main.py"
TOKEN = "step8-token"


def _load_tray():
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
        "glossa_tray_main_step8", TRAY_MAIN
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def tray(monkeypatch):
    mod = _load_tray()
    log_lines: list[str] = []
    monkeypatch.setattr(mod, "_tray_log", log_lines.append)
    # Icon pixels are not under test; the PIL stub has no real
    # imaging calls (the supervision suite stubs the module the
    # same way and likewise never renders an icon).
    monkeypatch.setattr(mod, "_create_icon_image", lambda colour="grey": object())
    mod._test_log_lines = log_lines
    return mod


class FakeIcon:
    def __init__(self):
        self.icon = None
        self.title = ""
        self.visible = False
        self.menu_updates = 0

    def update_menu(self):
        self.menu_updates += 1


# ── Humanized uptime ─────────────────────────────────────────────


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "under a minute"),
        (59, "under a minute"),
        (60, "1 m"),
        (2100, "35 m"),
        (3600, "1 h"),
        (21000, "5 h 50 m"),
        (86400, "1 d"),
        (90000, "1 d 1 h"),
        (176400, "2 d 1 h"),
    ],
)
def test_humanize_uptime(tray, seconds, expected):
    assert tray._humanize_uptime(seconds) == expected


def test_humanize_uptime_never_raw_seconds(tray):
    # The wireframe's specimen: 1803 s is "30 m", never "1803s".
    assert tray._humanize_uptime(1803) == "30 m"


# ── Status lines (wireframe 15) ──────────────────────────────────


def _poll_with_health(tray, monkeypatch, health, program=None, fetch_raises=False):
    monkeypatch.setattr(tray, "_check_health", lambda: health)
    if fetch_raises:
        def _boom():
            raise OSError("backend hiccup")
        monkeypatch.setattr(tray, "_fetch_active_program_label", _boom)
    else:
        monkeypatch.setattr(tray, "_fetch_active_program_label", lambda: program)
    icon = FakeIcon()
    tray._poll_once(icon)
    return icon


def test_status_line_names_program_and_humanizes(tray, monkeypatch):
    icon = _poll_with_health(
        tray,
        monkeypatch,
        {"status": "healthy", "version": "0.1.0", "uptime_seconds": 21000},
        program="Indus Script Decipherment",
    )
    assert tray._status_text == (
        "Indus Script Decipherment — backend healthy · v0.1.0 · up 5 h 50 m"
    )
    assert icon.title == "Glossa Lab — Healthy (v0.1.0) · Indus Script Decipherment"
    assert "s" not in tray._status_text.rsplit("up ", 1)[1].replace(" m", "").replace(" h", "")


def test_status_line_without_program_omits_the_segment(tray, monkeypatch):
    _poll_with_health(
        tray,
        monkeypatch,
        {"status": "healthy", "version": "0.1.0", "uptime_seconds": 120},
        program=None,
    )
    assert tray._status_text == "Backend healthy · v0.1.0 · up 2 m"


def test_status_line_keeps_last_program_on_a_failed_read(tray, monkeypatch):
    tray._program_label = "Indus Script Decipherment"
    _poll_with_health(
        tray,
        monkeypatch,
        {"status": "healthy", "version": "0.1.0", "uptime_seconds": 120},
        fetch_raises=True,
    )
    assert tray._program_label == "Indus Script Decipherment"
    assert tray._status_text.startswith("Indus Script Decipherment — backend healthy")


def test_status_line_user_stopped_in_words(tray, monkeypatch):
    monkeypatch.setattr(tray, "_check_health", lambda: None)
    monkeypatch.setattr(tray, "_maybe_auto_restart", lambda: "user-stopped")
    icon = FakeIcon()
    tray._poll_once(icon)
    assert tray._status_text == "Backend stopped by you — it will not restart itself."
    assert icon.title == "Glossa Lab — Backend stopped"


def test_status_line_cap_reached_names_the_limit(tray, monkeypatch):
    monkeypatch.setattr(tray, "_check_health", lambda: None)
    monkeypatch.setattr(tray, "_maybe_auto_restart", lambda: "cap-reached")
    tray._poll_once(FakeIcon())
    assert tray._status_text == (
        "Backend stopped — auto-restart limit reached (3 in the last hour)."
    )


def test_status_line_starting_is_one_bounded_state(tray, monkeypatch):
    monkeypatch.setattr(tray, "_check_health", lambda: None)
    monkeypatch.setattr(tray, "_maybe_auto_restart", lambda: "starting")
    tray._poll_once(FakeIcon())
    assert tray._status_text == "Backend starting…"


def test_status_line_degraded_names_the_check_when_payload_does(tray, monkeypatch):
    _poll_with_health(
        tray,
        monkeypatch,
        {"status": "degraded", "version": "0.1.0", "detail": "database read-only"},
    )
    assert tray._status_text == "Backend degraded — database read-only."


def test_status_line_degraded_without_detail_points_at_status(tray, monkeypatch):
    _poll_with_health(tray, monkeypatch, {"status": "degraded", "version": "0.1.0"})
    assert "Status screen names the failing check" in tray._status_text


# ── Active-program read ──────────────────────────────────────────


class _FakeResp:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode()

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_fetch_program_label_reads_the_active_record(tray, monkeypatch):
    monkeypatch.setattr(tray, "_resolve_token", lambda: TOKEN)
    seen = {}

    def fake_urlopen(req, timeout=0):
        seen["auth"] = req.headers.get("Authorization")
        seen["url"] = req.full_url
        return _FakeResp({"id": "p1", "label": "Indus Script Decipherment"})

    monkeypatch.setattr(tray.urllib.request, "urlopen", fake_urlopen)
    assert tray._fetch_active_program_label() == "Indus Script Decipherment"
    assert seen["auth"] == f"Bearer {TOKEN}"
    assert seen["url"].endswith("/api/v1/projects/active")


def test_fetch_program_label_404_means_no_program_open(tray, monkeypatch):
    def fake_urlopen(req, timeout=0):
        raise urllib.error.HTTPError(req.full_url, 404, "no active", {}, None)

    monkeypatch.setattr(tray.urllib.request, "urlopen", fake_urlopen)
    assert tray._fetch_active_program_label() is None


def test_fetch_program_label_transport_failure_raises(tray, monkeypatch):
    def fake_urlopen(req, timeout=0):
        raise urllib.error.URLError("down")

    monkeypatch.setattr(tray.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(urllib.error.URLError):
        tray._fetch_active_program_label()


# ── Single instance ──────────────────────────────────────────────


@pytest.fixture()
def lock_paths(tray, monkeypatch, tmp_path):
    lock = tmp_path / "tray-instance.lock"
    marker = tmp_path / "tray-focus-request"
    monkeypatch.setattr(tray, "_INSTANCE_LOCK", lock)
    monkeypatch.setattr(tray, "_FOCUS_MARKER", marker)
    return lock, marker


def test_instance_lock_acquire_on_fresh_dir(tray, lock_paths):
    lock, _marker = lock_paths
    assert tray._acquire_instance_lock() is True
    assert lock.read_text(encoding="utf-8") == str(os.getpid())


def test_instance_lock_denies_a_second_live_tray(tray, lock_paths):
    lock, marker = lock_paths
    sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        lock.write_text(str(sleeper.pid), encoding="utf-8")
        assert tray._acquire_instance_lock() is False
        # The running tray is asked for focus; the lock is untouched.
        assert marker.exists()
        assert lock.read_text(encoding="utf-8") == str(sleeper.pid)
        assert any("already running" in line for line in tray._test_log_lines)
    finally:
        sleeper.terminate()
        sleeper.wait(timeout=5)


def test_instance_lock_takes_over_a_stale_lock(tray, lock_paths):
    lock, _marker = lock_paths
    done = subprocess.Popen([sys.executable, "-c", "pass"])
    done.wait(timeout=5)
    lock.write_text(str(done.pid), encoding="utf-8")
    assert tray._acquire_instance_lock() is True
    assert lock.read_text(encoding="utf-8") == str(os.getpid())


def test_instance_lock_release_only_our_own(tray, lock_paths):
    lock, _marker = lock_paths
    lock.write_text("999999", encoding="utf-8")
    tray._release_instance_lock()
    assert lock.exists()  # someone else's lock is not ours to drop
    lock.write_text(str(os.getpid()), encoding="utf-8")
    tray._release_instance_lock()
    assert not lock.exists()


def test_focus_request_is_consumed_by_the_poller(tray, lock_paths):
    _lock, marker = lock_paths
    marker.write_text(f"{time.time():.0f}", encoding="utf-8")
    icon = FakeIcon()
    tray._consume_focus_request(icon)
    assert not marker.exists()
    assert icon.visible is True
    assert any("remains the single instance" in line for line in tray._test_log_lines)


# ── View status & session log ────────────────────────────────────


def test_open_status_screen_uses_the_routed_token_fragment(tray, monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr(tray, "_resolve_token", lambda: TOKEN)
    monkeypatch.setattr(tray.webbrowser, "open", opened.append)
    tray._open_status_screen()
    assert opened == [f"{tray.FRONTEND_URL}#/status#token={TOKEN}"]


def test_open_status_screen_without_a_token_opens_bare_and_logs(tray, monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr(tray, "_resolve_token", lambda: None)
    monkeypatch.setattr(tray.webbrowser, "open", opened.append)
    tray._open_status_screen()
    assert opened == [f"{tray.FRONTEND_URL}#/status"]
    assert any("no API token resolved" in line for line in tray._test_log_lines)


def test_status_click_opens_the_status_screen_not_the_raw_log(tray, monkeypatch):
    calls: list[str] = []
    monkeypatch.setattr(tray, "_open_status_screen", lambda: calls.append("status"))
    tray._on_status_click()
    assert calls == ["status"]
