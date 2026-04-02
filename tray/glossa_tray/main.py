"""Glossa Lab system tray application.

Uses pystray for cross-platform tray icon.
Communicates with the backend exclusively via HTTP API and CLI commands.
Satisfies REQ-TRAY-001 (display backend status) and REQ-TRAY-002 (no backend logic).
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print(
        "[ERROR] pystray and Pillow are required.\n"
        "Install them: pip install pystray Pillow\n"
        "Or run: shell.cmd setup / shell.sh setup"
    )
    sys.exit(1)

try:
    import urllib.request
    import json
except ImportError:
    pass  # stdlib, always available

# ── Constants ────────────────────────────────────

_AUTOSTART_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_AUTOSTART_NAME = "GlossaLabTray"

BACKEND_URL = "http://127.0.0.1:8001"
HEALTH_URL = f"{BACKEND_URL}/api/v1/health"
FRONTEND_URL = "http://localhost:5174"
POLL_INTERVAL = 5  # seconds

# Determine repo root and shell wrapper
_TRAY_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _TRAY_DIR.parent.parent
if platform.system() == "Windows":
    _SHELL = str(_REPO_ROOT / "shell.cmd")
else:
    _SHELL = str(_REPO_ROOT / "shell.sh")


# ── Icon generation ──────────────────────────────────────────────────

def _create_icon_image(colour: str = "green") -> Image.Image:
    """Generate a simple coloured circle icon."""
    colours = {"green": "#22c55e", "red": "#dc2626", "yellow": "#eab308", "grey": "#9ca3af"}
    fill = colours.get(colour, colours["grey"])
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=fill)
    return img


# ── Autostart management ───────────────────────────────────────

def _is_autostart_enabled() -> bool:
    """Check if tray autostart is registered in HKCU Run (Windows only)."""
    if platform.system() != "Windows":
        return False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _AUTOSTART_REG_KEY) as key:
            winreg.QueryValueEx(key, _AUTOSTART_NAME)
            return True
    except (FileNotFoundError, OSError):
        return False


def _set_autostart(enabled: bool) -> None:
    """Add or remove the tray HKCU Run entry (Windows only)."""
    if platform.system() != "Windows":
        return
    tray_svc = str(_REPO_ROOT / "scripts" / "run-tray-svc.cmd")
    try:
        import winreg
        if enabled:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, _AUTOSTART_REG_KEY,
                0, winreg.KEY_SET_VALUE,
            ) as key:
                winreg.SetValueEx(
                    key, _AUTOSTART_NAME, 0, winreg.REG_SZ,
                    f'"{tray_svc}"',
                )
        else:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, _AUTOSTART_REG_KEY,
                0, winreg.KEY_SET_VALUE,
            ) as key:
                winreg.DeleteValue(key, _AUTOSTART_NAME)
    except OSError:
        pass


def _toggle_autostart(_icon=None, _item=None) -> None:
    """Toggle the Start on login setting."""
    _set_autostart(not _is_autostart_enabled())


# ── Backend interaction (HTTP only — no backend logic) ───────────

def _check_health() -> dict | None:
    """Poll the backend health endpoint. Returns JSON dict or None on failure."""
    try:
        req = urllib.request.Request(HEALTH_URL, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def _backend_running() -> bool:
    return _check_health() is not None


# ── Actions (all via CLI or browser — no backend logic) ──────────────

def _open_ui(_icon=None, _item=None):
    """Open the frontend in the default browser."""
    webbrowser.open(FRONTEND_URL)


def _start_backend(_icon=None, _item=None):
    """Start the backend via shell wrapper (detached)."""
    if platform.system() == "Windows":
        subprocess.Popen(
            [_SHELL, "run"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            [_SHELL, "run"],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def _stop_backend(_icon=None, _item=None):
    """Request a clean backend shutdown via the /api/v1/shutdown endpoint."""
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{BACKEND_URL}/api/v1/shutdown", method="POST"
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass


def _quit(icon, _item=None):
    """Exit the tray application."""
    icon.stop()


# ── Status polling thread ────────────────────────────────────────────

def _status_poller(icon: pystray.Icon):
    """Background thread that polls backend health and updates the icon."""
    while icon.visible:
        health = _check_health()
        if health is None:
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab — Backend stopped"
        elif health.get("status") == "healthy":
            icon.icon = _create_icon_image("green")
            icon.title = f"Glossa Lab — Healthy (v{health.get('version', '?')})"
        elif health.get("status") == "degraded":
            icon.icon = _create_icon_image("yellow")
            icon.title = "Glossa Lab — Degraded"
        else:
            icon.icon = _create_icon_image("grey")
            icon.title = "Glossa Lab — Unknown"
        time.sleep(POLL_INTERVAL)


# ── Entry point ──────────────────────────────────────────────────────

def main():
    """Launch the Glossa Lab system tray icon."""
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", _open_ui, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Start Backend", _start_backend),
        pystray.MenuItem("Stop Backend", _stop_backend),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            "Start on login",
            _toggle_autostart,
            checked=lambda item: _is_autostart_enabled(),
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", _quit),
    )

    icon = pystray.Icon(
        name="glossa-lab",
        icon=_create_icon_image("grey"),
        title="Glossa Lab — Starting...",
        menu=menu,
    )

    # Ensure autostart is registered on first launch (idempotent)
    if not _is_autostart_enabled():
        _set_autostart(True)

    # Start poller thread
    poller = threading.Thread(target=_status_poller, args=(icon,), daemon=True)
    poller.start()

    icon.run()


if __name__ == "__main__":
    main()
