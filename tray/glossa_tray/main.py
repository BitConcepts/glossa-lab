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

_SCHTASK_NAME = "GlossaLab"  # single task that owns tray + backend

BACKEND_URL = "http://127.0.0.1:8001"
HEALTH_URL = f"{BACKEND_URL}/api/v1/health"
FRONTEND_URL = "http://localhost:8001"  # backend serves built frontend
POLL_INTERVAL = 3  # seconds — fast enough to feel live

# Determine repo root and shell wrapper
_TRAY_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _TRAY_DIR.parent.parent
if platform.system() == "Windows":
    _SHELL = str(_REPO_ROOT / "shell.cmd")
else:
    _SHELL = str(_REPO_ROOT / "shell.sh")

_BACKEND_LOG     = _REPO_ROOT / "logs" / "backend.log"
_BACKEND_DIR     = str(_REPO_ROOT / "backend")
_MAX_LOG_BYTES   = 10 * 1024 * 1024   # 10 MB per file
_LOG_BACKUPS     = 3                   # keep 3 rotated copies alongside the current log

# Use pythonw.exe on Windows: it is the *windowless* Python launcher —
# identical to python.exe but compiled as a GUI subsystem app, so Windows
# never allocates a console window for it under any circumstances.
_VENV_PYTHON = str(
    _REPO_ROOT / "backend" / "venv" / "Scripts" / "pythonw.exe"
    if platform.system() == "Windows"
    else _REPO_ROOT / "backend" / "venv" / "bin" / "python"
)

# Updated by the status poller; read by the dynamic menu item.
_status_text = "Backend: Checking..."
_status_error = False
_backend_starting = False  # set True while start is in progress, cleared by poller

# Label for the autostart toggle, varies by OS
_AUTOSTART_LABEL = (
    "Run at Windows startup" if platform.system() == "Windows"
    else "Start at login" if platform.system() == "Darwin"
    else "Enable autostart"
)


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
    """Check if the GlossaLab scheduled task exists (Windows) or launchd entry (macOS)."""
    if platform.system() == "Windows":
        result = subprocess.run(
            ["schtasks", "/query", "/tn", _SCHTASK_NAME],
            capture_output=True, creationflags=_WIN_HIDDEN,
        )
        return result.returncode == 0
    return False


def _set_autostart(enabled: bool) -> None:
    """Install or remove the GlossaLab scheduled task."""
    setup = str(_REPO_ROOT / "setup-os.cmd")
    if platform.system() == "Windows":
        cmd = "install" if enabled else "uninstall"
        subprocess.run(
            ["cmd.exe", "/c", setup, cmd],
            capture_output=True,
            creationflags=_WIN_HIDDEN,
        )


def _toggle_autostart(_icon=None, _item=None) -> None:
    """Toggle the Windows startup task."""
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


# Windows process-creation flags (no console window, detached, new group)
_WIN_DETACHED     = 0x00000008  # DETACHED_PROCESS
_WIN_NO_WINDOW    = 0x08000000  # CREATE_NO_WINDOW — suppresses any cmd flash
_WIN_NEW_PG       = 0x00000200  # CREATE_NEW_PROCESS_GROUP
_WIN_HIDDEN       = _WIN_DETACHED | _WIN_NO_WINDOW | _WIN_NEW_PG



def _run_silent(*cmd: str) -> None:
    """Run a command fully detached with no visible window (Windows) or in
    a new session (Linux/macOS). Used for service management only."""
    if platform.system() == "Windows":
        subprocess.Popen(
            list(cmd),
            creationflags=_WIN_HIDDEN,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            list(cmd),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )


def _start_or_stop_service(_icon=None, _item=None) -> None:
    """Single toggle: starts the backend if stopped, stops it if running."""
    global _backend_starting  # noqa: PLW0603
    if _backend_running():
        _stop_backend()
    else:
        _backend_starting = True
        _start_backend()


def _service_label(_item) -> str:
    return "Stop Service" if _backend_running() else "Start Service"


def _service_enabled(_item) -> bool:
    """Gray out while a start is in flight (backend not yet up)."""
    return not _backend_starting or _backend_running()


def _restart_service(_icon=None, _item=None) -> None:
    """Stop the backend then restart it. Runs in a background thread."""
    def _do() -> None:
        global _backend_starting  # noqa: PLW0603
        _stop_backend()
        for _ in range(20):  # wait up to 10 s for shutdown
            time.sleep(0.5)
            if not _backend_running():
                break
        time.sleep(0.5)
        _backend_starting = True
        _start_backend()
    threading.Thread(target=_do, daemon=True).start()


def _rotate_backend_log() -> None:
    """Rotate backend.log when it exceeds _MAX_LOG_BYTES.

    Keeps at most _LOG_BACKUPS numbered copies alongside the current log
    so total disk usage stays bounded (default: 4 × 10 MB = 40 MB max).
    """
    if not _BACKEND_LOG.exists():
        return
    try:
        if _BACKEND_LOG.stat().st_size < _MAX_LOG_BYTES:
            return
    except OSError:
        return
    # Shift existing numbered backups: .3.log is dropped, .2 → .3, .1 → .2
    for n in range(_LOG_BACKUPS, 0, -1):
        src = _BACKEND_LOG.with_suffix(f".{n}.log")
        dst = _BACKEND_LOG.with_suffix(f".{n + 1}.log")
        try:
            if src.exists():
                src.replace(dst)
        except OSError:
            pass
    # Move current log to .1.log
    try:
        _BACKEND_LOG.replace(_BACKEND_LOG.with_suffix(".1.log"))
    except OSError:
        pass  # File may be locked — continue appending to it


def _start_backend(_icon=None, _item=None) -> None:
    """Start the backend by launching Python directly — zero visible windows.

    Spawns the venv Python executable with CREATE_NO_WINDOW | DETACHED_PROCESS
    so no cmd shell or console ever appears. uvicorn stdout/stderr are appended
    to logs/backend.log alongside the app's structured logs.
    """
    _rotate_backend_log()   # ensure log file stays bounded before appending
    if platform.system() == "Windows":
        _BACKEND_LOG.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(str(_BACKEND_LOG), "ab")  # noqa: SIM115
        env = os.environ.copy()
        env["PYTHONPATH"] = _BACKEND_DIR
        subprocess.Popen(
            [
                _VENV_PYTHON, "-m", "uvicorn", "glossa_lab.main:app",
                "--host", "0.0.0.0", "--port", "8001",
                "--app-dir", _BACKEND_DIR,
            ],
            cwd=_BACKEND_DIR,
            creationflags=_WIN_HIDDEN,
            env=env,
            stdout=log_fh,
            stderr=log_fh,
            stdin=subprocess.DEVNULL,
        )
        log_fh.close()  # parent closes; child keeps its inherited fd
    else:
        _run_silent("systemctl", "--user", "start", "glossa-lab-backend")


def _stop_backend(_icon=None, _item=None) -> None:
    """Stop the backend gracefully via HTTP, then kill if still running.

    Linux: also tells systemd to stop the unit.
    """
    try:
        req = urllib.request.Request(f"{BACKEND_URL}/api/v1/shutdown", method="POST")
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass
    if platform.system() != "Windows":
        _run_silent("systemctl", "--user", "stop", "glossa-lab-backend")


def _open_log(_icon=None, _item=None) -> None:
    """Open the backend log file in the default text editor."""
    log = _BACKEND_LOG
    if not log.exists():
        return
    try:
        if platform.system() == "Windows":
            os.startfile(str(log))  # type: ignore[attr-defined]
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(log)])
        else:
            subprocess.Popen(["xdg-open", str(log)])
    except Exception:
        pass


def _on_status_click(_icon=None, _item=None) -> None:
    """Click the status item: open log when backend is stopped/errored."""
    if _status_error:
        _open_log()


def _ensure_backend_running() -> None:
    """Start the backend if it is not already responding. Called at tray startup."""
    if not _backend_running():
        _start_backend()


def _quit(icon, _item=None):
    """Exit the tray application."""
    icon.stop()


# ── Status polling thread ────────────────────────────────────────────

def _status_poller(icon: pystray.Icon):
    """Background thread: polls health every POLL_INTERVAL seconds.

    Started via icon.run(setup=…) so icon.visible is already True.
    Runs as a daemon thread and is killed automatically on exit.
    """
    global _status_text, _status_error, _backend_starting  # noqa: PLW0603
    while True:
        health = _check_health()
        if health is None:
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab — Backend stopped"
            _status_text = "Backend: Stopped  (click to view log)"
            _status_error = True
        elif health.get("status") in ("healthy", "degraded"):
            _backend_starting = False  # clear the starting flag once we see it's up
            if health.get("status") == "healthy":
                icon.icon = _create_icon_image("green")
                ver = health.get('version', '?')
                uptime = int(health.get('uptime_seconds', 0))
                icon.title = f"Glossa Lab — Healthy (v{ver})"
                _status_text = f"Backend: Healthy  v{ver}  up {uptime}s"
                _status_error = False
            else:
                icon.icon = _create_icon_image("yellow")
                icon.title = "Glossa Lab — Degraded"
                _status_text = "Backend: Degraded  (click to view log)"
                _status_error = True
        else:
            icon.icon = _create_icon_image("grey")
            icon.title = "Glossa Lab — Unknown"
            _status_text = "Backend: Unknown  (click to view log)"
            _status_error = True
        try:
            icon.update_menu()  # Force pystray to re-evaluate dynamic labels
        except Exception:  # noqa: BLE001
            pass
        time.sleep(POLL_INTERVAL)


# ── Entry point ──────────────────────────────────────────────────────

def main():
    """Launch the Glossa Lab system tray icon."""
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", _open_ui, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(lambda _: _status_text, _on_status_click),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(_service_label, _start_or_stop_service, enabled=_service_enabled),
        pystray.MenuItem("Restart Service", _restart_service),
        pystray.MenuItem("View Log", _open_log),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            _AUTOSTART_LABEL,
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

    # Start backend immediately if not running — tray is the single entry point
    _ensure_backend_running()

    # Ensure autostart is registered on first launch (idempotent)
    if not _is_autostart_enabled():
        _set_autostart(True)

    def _on_setup(ic: pystray.Icon) -> None:
        """Called by pystray after the icon is displayed and the event loop running.
        Only here is ic.visible reliably True and the menu repaint safe.
        """
        ic.visible = True
        poller = threading.Thread(target=_status_poller, args=(ic,), daemon=True)
        poller.start()

    icon.run(setup=_on_setup)


if __name__ == "__main__":
    main()
