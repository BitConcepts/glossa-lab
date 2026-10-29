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

_CONFIG_FILE = Path.home() / ".glossa-lab" / "config.json"


def _load_config() -> dict:
    try:
        if _CONFIG_FILE.exists():
            return json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_config(cfg: dict) -> None:
    try:
        _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    except Exception:
        pass


def _current_port() -> int:
    """Return the configured backend port (default 8001)."""
    return int(_load_config().get("port", 8001))


# Dynamically resolved so port changes take effect immediately.
def _make_urls(port: int) -> tuple[str, str, str]:
    base     = f"http://127.0.0.1:{port}"
    health   = f"{base}/api/v1/health"
    frontend = f"http://localhost:{port}"
    return base, health, frontend


BACKEND_URL, HEALTH_URL, FRONTEND_URL = _make_urls(_current_port())
POLL_INTERVAL = 3  # seconds

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

# Spec 080 (Windows host supervision): the tray owns backend liveness on
# Windows — there is no service manager underneath it. A backend that
# dies without a user stop is restarted automatically, capped so a
# crash loop cannot spin forever (H11). A user-initiated stop is never
# overridden.
_MAX_AUTO_RESTARTS = 3
_RESTART_WINDOW_SEC = 3600
_restart_times: list[float] = []
_user_stopped = False

# Label for the autostart toggle, varies by OS
_AUTOSTART_LABEL = (
    "Run at Windows startup" if platform.system() == "Windows"
    else "Start at login" if platform.system() == "Darwin"
    else "Enable autostart"
)


# ── Icon: the Glossa Lab brand tile + a status badge ────────────────
#
# The base image is the project's own application mark (the blue
# gradient tile with a white "G" used in the web UI), shipped as a
# packaged asset — NOT a plain coloured circle and NOT another
# project's mark. Status is shown as a small badge dot in the lower
# right corner, the same treatment the Syncyard tray uses.

_ASSETS_DIR = Path(__file__).resolve().parent / "assets"
_BRAND_ICON_PATH = _ASSETS_DIR / "glossa-lab.png"
_brand_image: Image.Image | None = None


def _load_brand_image() -> Image.Image | None:
    """Load (and cache) the packaged Glossa Lab brand tile."""
    global _brand_image
    if _brand_image is None and _BRAND_ICON_PATH.exists():
        try:
            _brand_image = Image.open(_BRAND_ICON_PATH).convert("RGBA")
        except (OSError, ValueError):
            _brand_image = None
    return _brand_image


def _create_icon_image(colour: str = "green") -> Image.Image:
    """Brand tile with a status badge; falls back to the tile alone."""
    colours = {"green": "#22c55e", "red": "#dc2626", "yellow": "#eab308", "grey": "#9ca3af"}
    fill = colours.get(colour, colours["grey"])
    brand = _load_brand_image()
    if brand is None:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([4, 4, 60, 60], radius=14, fill="#2563eb")
        draw.ellipse([40, 40, 58, 58], fill=fill, outline="white", width=2)
        return img
    img = brand.copy().resize((64, 64), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    draw.ellipse([42, 42, 60, 60], fill=fill, outline="white", width=2)
    return img


# ── Autostart management ───────────────────────────────────────

_LINUX_AUTOSTART_DESKTOP = (
    Path.home() / ".config" / "autostart" / "glossa-lab-tray.desktop"
)


def _is_autostart_enabled() -> bool:
    """Windows: GlossaLab scheduled task. Linux: tray autostart entry."""
    if platform.system() == "Windows":
        result = subprocess.run(
            ["schtasks", "/query", "/tn", _SCHTASK_NAME],
            capture_output=True, creationflags=_WIN_HIDDEN, check=False,
        )
        return result.returncode == 0
    if platform.system() == "Linux":
        return _LINUX_AUTOSTART_DESKTOP.exists()
    return False


def _set_autostart(enabled: bool) -> None:
    """Install or remove the OS autostart registration for the tray."""
    if platform.system() == "Windows":
        setup = str(_REPO_ROOT / "setup-os.cmd")
        cmd = "install" if enabled else "uninstall"
        subprocess.run(
            ["cmd.exe", "/c", setup, cmd],
            capture_output=True,
            creationflags=_WIN_HIDDEN,
            check=False,
        )
    elif platform.system() == "Linux":
        if enabled:
            # The Linux installer is the single install path: a
            # render-only run (re)writes the tray autostart entry,
            # the icon, and the backend unit without touching the
            # service manager.
            installer = _REPO_ROOT / "services" / "linux" / "install.sh"
            subprocess.run(
                ["bash", str(installer), "--render-only", "--skip-dependencies"],
                capture_output=True,
                timeout=30,
                check=False,
            )
        else:
            _LINUX_AUTOSTART_DESKTOP.unlink(missing_ok=True)


def _toggle_autostart(_icon=None, _item=None) -> None:
    """Toggle the Windows autostart entry."""
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
    global _user_stopped  # noqa: PLW0603
    _user_stopped = False  # any start clears a prior user stop (Spec 080)
    _rotate_backend_log()   # ensure log file stays bounded before appending
    if platform.system() == "Windows":
        _BACKEND_LOG.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(str(_BACKEND_LOG), "ab")  # noqa: SIM115
        env = os.environ.copy()
        env["PYTHONPATH"] = _BACKEND_DIR
        # Installed mode: the database lives under
        # %LOCALAPPDATA%\GlossaLab\data regardless of the caller's cwd
        # (Spec 080 FR-005).
        env["GLOSSA_MODE"] = "installed"
        port = str(_current_port())
        subprocess.Popen(
            [
                _VENV_PYTHON, "-m", "uvicorn", "glossa_lab.main:create_app",
                "--factory", "--host", "127.0.0.1", "--port", port,
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
    A user stop is remembered so the Windows auto-restart (Spec 080)
    never overrides it.
    """
    global _user_stopped  # noqa: PLW0603
    _user_stopped = True
    try:
        req = urllib.request.Request(f"{BACKEND_URL}/api/v1/shutdown", method="POST")
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass
    if platform.system() != "Windows":
        _run_silent("systemctl", "--user", "stop", "glossa-lab-backend")


def _change_port(_icon=None, _item=None) -> None:
    """Ask the user for a new port via a simple tkinter dialog.

    Saves the new port to ~/.glossa-lab/config.json and offers to restart
    the backend so the change takes effect immediately.
    """
    global BACKEND_URL, HEALTH_URL, FRONTEND_URL  # noqa: PLW0603
    try:
        import tkinter as tk  # noqa: PLC0415
        from tkinter import simpledialog, messagebox  # noqa: PLC0415
    except ImportError:
        return  # tkinter not available — skip

    root = tk.Tk()
    root.withdraw()  # hide root window
    root.attributes("-topmost", True)
    current = _current_port()
    answer = simpledialog.askstring(
        "Glossa Lab - Change Port",
        f"Enter new backend port (current: {current}):\n"
        "Common choices: 8001 (default), 8000, 5000, 3000",
        initialvalue=str(current),
        parent=root,
    )
    root.destroy()
    if not answer:
        return
    try:
        new_port = int(answer.strip())
        if not (1 <= new_port <= 65535):
            raise ValueError("Port out of range")
    except ValueError:
        return

    if new_port == current:
        return

    # Save and rebuild URLs
    cfg = _load_config()
    cfg["port"] = new_port
    _save_config(cfg)
    BACKEND_URL, HEALTH_URL, FRONTEND_URL = _make_urls(new_port)

    # Ask whether to restart now
    root2 = tk.Tk()
    root2.withdraw()
    root2.attributes("-topmost", True)
    if messagebox.askyesno(
        "Restart backend?",
        f"Port changed to {new_port}.\nRestart the backend now to apply the change?",
        parent=root2,
    ):
        threading.Thread(target=_restart_service, daemon=True).start()
    root2.destroy()


def _port_label(_item) -> str:
    return f"Port: {_current_port()}"


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


def _maybe_auto_restart() -> str:
    """Windows tray supervision (Spec 080 FR-006): restart a backend
    that died without a user stop.

    Returns "restarted", "user-stopped", "cap-reached", or
    "not-windows". Bounded at _MAX_AUTO_RESTARTS restarts per
    _RESTART_WINDOW_SEC window (H11); the caller surfaces
    "cap-reached" in the tray status so a crash loop is visible
    instead of silent. Linux is supervised by systemd and never
    auto-restarts from the tray.
    """
    if platform.system() != "Windows":
        return "not-windows"
    if _user_stopped:
        return "user-stopped"
    now = time.monotonic()
    _restart_times[:] = [t for t in _restart_times if now - t < _RESTART_WINDOW_SEC]
    if len(_restart_times) >= _MAX_AUTO_RESTARTS:
        return "cap-reached"
    _restart_times.append(now)
    _start_backend()
    return "restarted"


def _quit(icon, _item=None):
    """Exit the tray application."""
    icon.stop()


# ── Status polling thread ────────────────────────────────────────────

_MAX_POLL_ITERATIONS = 86400 // POLL_INTERVAL  # ~24 hours of polling before self-stop


def _status_poller(icon: pystray.Icon):
    """Background thread: polls health every POLL_INTERVAL seconds.

    Started via icon.run(setup=…) so icon.visible is already True.
    Runs as a daemon thread and is killed automatically on exit.
    H11 compliant: bounded by _MAX_POLL_ITERATIONS (~24 h at POLL_INTERVAL).
    """
    global _status_text, _status_error, _backend_starting  # noqa: PLW0603
    for _poll_iter in range(_MAX_POLL_ITERATIONS):
        health = _check_health()
        if health is None:
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab - Backend stopped"
            _status_text = "Backend: Stopped  (click to view log)"
            _status_error = True
            # Spec 080: on Windows the tray is the supervisor — a
            # backend that died on its own is restarted (capped); a
            # user stop is left alone and labelled as such.
            outcome = _maybe_auto_restart()
            if outcome == "user-stopped":
                _status_text = "Backend: Stopped by user"
            elif outcome == "cap-reached":
                _status_text = (
                    "Backend: Stopped - auto-restart limit reached "
                    "(click to view log)"
                )
        elif health.get("status") in ("healthy", "degraded"):
            _backend_starting = False  # clear the starting flag once we see it's up
            if health.get("status") == "healthy":
                icon.icon = _create_icon_image("green")
                ver = health.get('version', '?')
                uptime = int(health.get('uptime_seconds', 0))
                icon.title = f"Glossa Lab - Healthy (v{ver})"
                _status_text = f"Backend: Healthy  v{ver}  up {uptime}s"
                _status_error = False
            else:
                icon.icon = _create_icon_image("yellow")
                icon.title = "Glossa Lab - Degraded"
                _status_text = "Backend: Degraded  (click to view log)"
                _status_error = True
        else:
            icon.icon = _create_icon_image("grey")
            icon.title = "Glossa Lab - Unknown"
            _status_text = "Backend: Unknown  (click to view log)"
            _status_error = True
        try:
            icon.update_menu()  # Force pystray to re-evaluate dynamic labels
        except Exception:  # noqa: BLE001
            pass
        time.sleep(POLL_INTERVAL)
    # H11: deadline reached — log and exit polling
    print(f"[WARN] _status_poller: reached {_MAX_POLL_ITERATIONS} iterations "
          f"({_MAX_POLL_ITERATIONS * POLL_INTERVAL}s). Stopping poller. "
          "Restart tray to resume.")


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
        pystray.MenuItem(_port_label, None, enabled=False),  # display-only
        pystray.MenuItem("Change Port...", _change_port),
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
        title="Glossa Lab - Starting...",
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
