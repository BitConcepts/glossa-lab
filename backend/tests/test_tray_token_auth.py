"""Spec 082 (T009) — tray token behavior, headless.

Mirrors tests/test_tray_supervision.py's loader: pystray/Pillow are
stubbed in ``sys.modules`` and the tray module is imported fresh
from its file path per test. Covers the token resolution order,
per-use re-resolution (rotation pickup), the authenticated
shutdown request, the Open UI fragment handoff (+ the named tray
log line when no token resolves), and Copy API Token (clipboard
success via a fake tkinter; named failures otherwise).
"""

from __future__ import annotations

import importlib.util
import sys
import types
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TRAY_MAIN = REPO / "tray" / "glossa_tray" / "main.py"
TOKEN = "tray-test-token-082"


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


@pytest.fixture()
def tray(monkeypatch, tmp_path):
    """A fresh tray module with every token source controlled."""
    mod = _load_tray()
    log_lines: list[str] = []
    monkeypatch.setattr(mod, "_tray_log", log_lines.append)
    monkeypatch.delenv("GLOSSA_API_TOKEN", raising=False)
    monkeypatch.delenv("GLOSSA_TOKEN_FILE", raising=False)
    # Point the platform data-dir candidate and the repo fallback
    # at empty tmp dirs so only a test's own plants can resolve.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr(mod, "_REPO_ROOT", tmp_path / "repo")
    # Hermeticity on an INSTALLED host (T020 host run, 2026-10-30):
    # the resolver's Windows candidate reads LOCALAPPDATA, which the
    # lines above do not touch — on the desktop install the REAL
    # api_token resolved inside tests that planted elsewhere or
    # expected none (and assertion output carried the live value
    # into the job log). Pin the platform branch to the XDG form
    # this fixture controls, and point LOCALAPPDATA at an empty tmp
    # dir as well; the Windows-specific test re-patches both itself.
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    monkeypatch.setattr(mod.platform, "system", lambda: "Linux")
    mod._test_log_lines = log_lines
    mod._test_tmp = tmp_path
    return mod


def _plant(path: Path, value: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value + "\n", encoding="utf-8")
    return path


# ── Resolution order ──────────────────────────────────────


def test_env_token_wins(tray, monkeypatch):
    _plant(tray._test_tmp / "xdg" / "glossa-lab" / "api_token", "file-token")
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    assert tray._resolve_token() == TOKEN


def test_token_file_env_is_next(tray, monkeypatch):
    named = _plant(tray._test_tmp / "named.txt", "named-token")
    monkeypatch.setenv("GLOSSA_TOKEN_FILE", str(named))
    assert tray._resolve_token() == "named-token"


def test_installed_data_dir_candidate(tray):
    _plant(tray._test_tmp / "xdg" / "glossa-lab" / "api_token", "xdg-token")
    assert tray._resolve_token() == "xdg-token"


def test_installed_data_dir_candidate_windows(tray, monkeypatch):
    monkeypatch.setattr(tray.platform, "system", lambda: "Windows")
    monkeypatch.setenv("LOCALAPPDATA", str(tray._test_tmp / "localappdata"))
    _plant(
        tray._test_tmp / "localappdata" / "GlossaLab" / "data" / "api_token",
        "win-token",
    )
    assert tray._resolve_token() == "win-token"


def test_repo_fallback_candidate(tray):
    _plant(
        tray._test_tmp / "repo" / "backend" / "data" / "api_token",
        "repo-token",
    )
    assert tray._resolve_token() == "repo-token"


def test_unresolvable_returns_none(tray):
    assert tray._resolve_token() is None


def test_resolution_is_per_use_so_rotation_applies(tray):
    token_file = _plant(
        tray._test_tmp / "xdg" / "glossa-lab" / "api_token", "before-rotation"
    )
    assert tray._resolve_token() == "before-rotation"
    token_file.write_text("after-rotation\n", encoding="utf-8")
    assert tray._resolve_token() == "after-rotation"


# ── Shutdown request carries the token ────────────────────


def _capture_shutdown(tray, monkeypatch):
    captured: list = []

    def fake_urlopen(req, timeout=None):  # noqa: ANN001, ANN202
        captured.append(req)
        return object()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(tray, "_run_silent", lambda *a, **k: None)
    tray._stop_backend()
    assert captured, "the tray issued no shutdown request"
    return captured[0]


def test_shutdown_sends_the_bearer_token(tray, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    request = _capture_shutdown(tray, monkeypatch)
    assert request.full_url.endswith("/api/v1/shutdown")
    assert request.get_header("Authorization") == f"Bearer {TOKEN}"


def test_shutdown_without_a_token_sends_no_header(tray, monkeypatch):
    request = _capture_shutdown(tray, monkeypatch)
    assert request.get_header("Authorization") is None


# ── Open UI fragment handoff ──────────────────────────────


def test_open_ui_hands_off_the_token_fragment(tray, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    opened: list[str] = []
    monkeypatch.setattr(tray.webbrowser, "open", opened.append)
    tray._open_ui()
    assert opened == [f"{tray.FRONTEND_URL}#token={TOKEN}"]


def test_open_ui_without_a_token_logs_the_miss(tray, monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr(tray.webbrowser, "open", opened.append)
    tray._open_ui()
    assert opened == [tray.FRONTEND_URL]  # bare: no fabricated fragment
    assert any(
        "no API token resolved" in line for line in tray._test_log_lines
    )


# ── Copy API Token ────────────────────────────────────────


class _FakeTk:
    appended: list[str] = []

    def withdraw(self):
        pass

    def clipboard_clear(self):
        pass

    def clipboard_append(self, value):
        _FakeTk.appended.append(value)

    def update(self):
        pass

    def destroy(self):
        pass


def test_copy_api_token_copies_and_never_logs_the_value(tray, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    _FakeTk.appended = []
    fake_tk = types.ModuleType("tkinter")
    fake_tk.Tk = _FakeTk
    monkeypatch.setitem(sys.modules, "tkinter", fake_tk)
    tray._copy_api_token()
    assert _FakeTk.appended == [TOKEN]
    assert any("copied" in line for line in tray._test_log_lines)
    assert all(TOKEN not in line for line in tray._test_log_lines)


def test_copy_api_token_without_a_token_is_named(tray, monkeypatch):
    _FakeTk.appended = []
    fake_tk = types.ModuleType("tkinter")
    fake_tk.Tk = _FakeTk
    monkeypatch.setitem(sys.modules, "tkinter", fake_tk)
    tray._copy_api_token()
    assert _FakeTk.appended == []
    assert any(
        "no token resolved" in line for line in tray._test_log_lines
    )


def test_copy_api_token_without_tkinter_is_named(tray, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    monkeypatch.setitem(sys.modules, "tkinter", None)  # import fails
    tray._copy_api_token()
    assert any(
        "tkinter is not available" in line for line in tray._test_log_lines
    )
