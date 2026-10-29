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
    except Exception as exc:  # noqa: BLE001
        # A corrupt config silently defaulting the port made the tray
        # poll the wrong port and "restart" a second backend; the
        # failure is recorded in the tray log instead (audit 2026-10-29).
        _tray_log(
            f"config load failed ({type(exc).__name__}: {exc}); using defaults"
        )
    return {}


def _save_config(cfg: dict) -> None:
    try:
        _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        _tray_log(f"config save failed ({type(exc).__name__}: {exc})")


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

# ── Tray diagnostics log ─────────────────────────────────
#
# The tray runs under pythonw with stdout/stderr discarded, so
# print() goes nowhere: before this log existed, poller death,
# auto-restarts, failed stops and failed starts left no trace
# anywhere (2026-10-29 UI-log audit — the tray had no log file at
# all). logs/tray.log is the tray's durable diagnostic surface,
# rotated with the same discipline as the backend log.

_TRAY_LOG = _REPO_ROOT / "logs" / "tray.log"


def _rotate_log_file(path: Path) -> None:
    """Rotate ``path`` when it exceeds _MAX_LOG_BYTES.

    Keeps at most _LOG_BACKUPS numbered copies alongside the current
    log so total disk usage stays bounded (default: 4 × 10 MB max).
    """
    if not path.exists():
        return
    try:
        if path.stat().st_size < _MAX_LOG_BYTES:
            return
    except OSError:
        return
    # Shift existing numbered backups: .3 is dropped, .2 → .3, .1 → .2
    for n in range(_LOG_BACKUPS, 0, -1):
        src = path.with_suffix(f".{n}.log")
        dst = path.with_suffix(f".{n + 1}.log")
        try:
            if src.exists():
                src.replace(dst)
        except OSError:
            pass
    # Move current log to .1.log
    try:
        path.replace(path.with_suffix(".1.log"))
    except OSError:
        pass  # File may be locked — continue appending to it


def _tray_log(message: str) -> None:
    """Append one timestamped line to logs/tray.log.

    Best-effort by necessity — a diagnostics failure must never kill
    the tray — so OSError is swallowed here, and only here.
    """
    try:
        _TRAY_LOG.parent.mkdir(parents=True, exist_ok=True)
        _rotate_log_file(_TRAY_LOG)
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(_TRAY_LOG, "a", encoding="utf-8") as fh:
            fh.write(f"{stamp} {message}\n")
    except OSError:
        pass


# ── Spec 082: API token ──────────────────────────────────
#
# The backend requires a per-install API token (Spec 082). The tray
# resolves it the same way the backend's other consumers do: the
# GLOSSA_API_TOKEN environment value, then a token file named by
# GLOSSA_TOKEN_FILE, then this install's token file (the installed
# data dir; in a repo checkout, backend/data). Resolution runs per
# use — never cached — so a rotation applies on the next action
# without restarting the tray. The token value is never written to
# the tray log; a resolution miss is named, never silent (T009).


def _token_candidates() -> list[Path]:
    candidates: list[Path] = []
    named = os.environ.get("GLOSSA_TOKEN_FILE", "").strip()
    if named:
        candidates.append(Path(named).expanduser())
    system = platform.system()
    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            candidates.append(
                Path(local_app_data) / "GlossaLab" / "data" / "api_token"
            )
    elif system == "Darwin":
        candidates.append(
            Path.home()
            / "Library"
            / "Application Support"
            / "GlossaLab"
            / "data"
            / "api_token"
        )
    else:
        xdg_data = os.environ.get("XDG_DATA_HOME", "").strip()
        base = (
            Path(xdg_data).expanduser()
            if xdg_data
            else Path.home() / ".local" / "share"
        )
        candidates.append(base / "glossa-lab" / "api_token")
    candidates.append(_REPO_ROOT / "backend" / "data" / "api_token")
    return candidates


def _resolve_token() -> str | None:
    """Resolve this install's API token, or None when unresolvable."""
    env_token = os.environ.get("GLOSSA_API_TOKEN", "").strip()
    if env_token:
        return env_token
    for candidate in _token_candidates():
        try:
            if candidate.is_file():
                value = candidate.read_text(encoding="utf-8").strip()
                if value:
                    return value
        except OSError:
            continue
    return None


# Updated by the status poller; read by the dynamic menu item.
_status_text = "Backend: Checking..."
_status_error = False
_backend_starting = False  # set True while start is in progress, cleared by poller
_backend_start_mono = 0.0  # monotonic time of the latest start attempt
_START_GRACE_SEC = 120     # a start still not up after this is a failed start
_cap_notice_logged = False  # auto-restart cap notice written to tray log once

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


def _set_autostart(enabled: bool) -> bool:
    """Install or remove the OS autostart registration for the tray.

    Returns True on success. Failures are written to the tray log:
    previously the result was discarded entirely, so a failed install
    was invisible and retried silently on every launch.
    """
    action = "install" if enabled else "uninstall"
    if platform.system() == "Windows":
        setup = str(_REPO_ROOT / "setup-os.cmd")
        result = subprocess.run(
            ["cmd.exe", "/c", setup, action],
            capture_output=True,
            creationflags=_WIN_HIDDEN,
            check=False,
        )
        if result.returncode != 0:
            err = (result.stderr or b"").decode(errors="replace").strip()[:200]
            _tray_log(
                f"autostart {action} failed (exit {result.returncode}): {err}"
            )
            return False
        return True
    if platform.system() == "Linux":
        if enabled:
            # The Linux installer is the single install path: a
            # render-only run (re)writes the tray autostart entry,
            # the icon, and the backend unit without touching the
            # service manager.
            installer = _REPO_ROOT / "services" / "linux" / "install.sh"
            result = subprocess.run(
                ["bash", str(installer), "--render-only", "--skip-dependencies"],
                capture_output=True,
                timeout=30,
                check=False,
            )
            if result.returncode != 0:
                err = (result.stderr or b"").decode(errors="replace").strip()[:200]
                _tray_log(
                    f"autostart install failed (exit {result.returncode}): {err}"
                )
                return False
            return True
        try:
            _LINUX_AUTOSTART_DESKTOP.unlink(missing_ok=True)
        except OSError as exc:
            _tray_log(f"autostart uninstall failed: {exc}")
            return False
        return True
    return False


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
    """Open the frontend in the default browser.

    Spec 082: the resolved token rides in a URL fragment
    (``#token=...``) — fragments are never sent to the server or
    written to access logs, and the SPA moves the value into
    session storage and strips it from the address bar
    (ui-contract.md). When no token resolves, the UI opens bare
    and the miss is named in the tray log; a fragment is never
    fabricated.
    """
    token = _resolve_token()
    if token:
        webbrowser.open(f"{FRONTEND_URL}#token={token}")
        return
    _tray_log(
        "open UI: no API token resolved (checked GLOSSA_API_TOKEN, "
        "GLOSSA_TOKEN_FILE, the installed data dir, backend/data); "
        "opening the UI without the token handoff"
    )
    webbrowser.open(FRONTEND_URL)


def _copy_api_token(_icon=None, _item=None) -> None:
    """Copy the install's API token to the clipboard (Spec 082 T009).

    Uses tkinter, the same toolkit as the Change Port dialog. Every
    failure is named in the tray log — an unresolvable token, a
    missing tkinter, a clipboard error — and the token value itself
    is never logged.
    """
    token = _resolve_token()
    if not token:
        _tray_log(
            "copy API token: no token resolved (checked "
            "GLOSSA_API_TOKEN, GLOSSA_TOKEN_FILE, the installed "
            "data dir, backend/data)"
        )
        return
    try:
        import tkinter as tk  # noqa: PLC0415
    except ImportError:
        _tray_log("copy API token failed: tkinter is not available")
        return
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(token)
        root.update()  # settle clipboard ownership before destroying
        root.destroy()
        _tray_log("API token copied to the clipboard")
    except Exception as exc:  # noqa: BLE001
        _tray_log(f"copy API token failed: {type(exc).__name__}: {exc}")


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
    """Rotate backend.log when it exceeds _MAX_LOG_BYTES."""
    _rotate_log_file(_BACKEND_LOG)


def _start_backend(_icon=None, _item=None) -> bool:
    """Start the backend by launching Python directly — zero visible windows.

    Spawns the venv Python executable with CREATE_NO_WINDOW | DETACHED_PROCESS
    so no cmd shell or console ever appears. uvicorn stdout/stderr are appended
    to logs/backend.log alongside the app's structured logs.

    Records the start as in-flight (``_backend_starting``) so the
    supervisor never spawns a duplicate while this one is still
    booting. A spawn failure is written to the tray log and reported
    in the tray status instead of propagating: previously a Popen
    failure (e.g. a missing venv pythonw) killed the tray silently
    before its icon ever appeared. Returns True when the spawn was
    issued.
    """
    global _user_stopped, _backend_starting, _backend_start_mono  # noqa: PLW0603
    global _status_text, _status_error, _cap_notice_logged  # noqa: PLW0603
    _user_stopped = False  # any start clears a prior user stop (Spec 080)
    _backend_starting = True
    _backend_start_mono = time.monotonic()
    _cap_notice_logged = False  # a fresh start re-arms the cap notice
    _rotate_backend_log()   # ensure log file stays bounded before appending
    try:
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
    except Exception as exc:  # noqa: BLE001
        _backend_starting = False
        _status_text = "Backend: Start failed  (click to view log)"
        _status_error = True
        _tray_log(f"backend start failed: {type(exc).__name__}: {exc}")
        return False
    _tray_log("backend start issued")
    return True


def _listener_pid(port: int) -> int | None:
    """PID of the process LISTENING on ``port`` (Windows, via netstat).

    Used only as the stop path's last resort. Returns None when no
    listener is found or netstat cannot be run.
    """
    if platform.system() != "Windows":
        return None
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=5,
            creationflags=_WIN_HIDDEN, check=False,
        )
    except Exception:  # noqa: BLE001
        return None
    for line in result.stdout.splitlines():
        parts = line.split()
        if (
            len(parts) >= 5
            and parts[0].upper() == "TCP"
            and parts[1].endswith(f":{port}")
            and parts[3].upper() == "LISTENING"
        ):
            try:
                return int(parts[4])
            except ValueError:
                return None
    return None


def _wait_until_stopped(attempts: int = 10, interval: float = 0.5) -> bool:
    """Bounded wait (H11) for the backend to stop answering health."""
    for _ in range(attempts):
        if not _backend_running():
            return True
        time.sleep(interval)
    return not _backend_running()


def _stop_backend(_icon=None, _item=None) -> None:
    """Stop the backend gracefully via HTTP, then kill if still running.

    Windows: after the shutdown request, wait (bounded) for the
    backend to actually go away; if it is still answering, kill the
    process listening on the backend port as the documented last
    resort. Every failure is written to the tray log — previously the
    shutdown request's failure was swallowed and the promised kill
    did not exist, so a stop could silently not happen while the
    tray reported the backend as stopped by the user.
    Linux: also tells systemd to stop the unit.
    A user stop is remembered so the Windows auto-restart (Spec 080)
    never overrides it.
    """
    global _user_stopped  # noqa: PLW0603
    _user_stopped = True
    try:
        # Spec 082: the shutdown route is token-gated. Present the
        # resolved token when one is available; without one the
        # request is refused (401, logged below) and the bounded
        # kill fallback behind this block remains the last resort,
        # exactly as before.
        headers = {}
        token = _resolve_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(
            f"{BACKEND_URL}/api/v1/shutdown", method="POST", headers=headers
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception as exc:  # noqa: BLE001
        _tray_log(f"shutdown request failed: {type(exc).__name__}: {exc}")
    if platform.system() != "Windows":
        _run_silent("systemctl", "--user", "stop", "glossa-lab-backend")
        _tray_log("backend stop requested (systemd)")
        return
    if _wait_until_stopped():
        _tray_log("backend stopped")
        return
    pid = _listener_pid(_current_port())
    if pid is not None:
        _tray_log(
            "backend still running after the shutdown request; "
            f"killing listener pid {pid}"
        )
        try:
            subprocess.run(
                ["taskkill", "/F", "/PID", str(pid), "/T"],
                capture_output=True, timeout=10,
                creationflags=_WIN_HIDDEN, check=False,
            )
        except Exception as exc:  # noqa: BLE001
            _tray_log(f"taskkill failed: {type(exc).__name__}: {exc}")
        if _wait_until_stopped():
            _tray_log("backend stopped (via kill fallback)")
            return
    _tray_log(
        "backend stop FAILED: still responding after the shutdown "
        "request and the kill fallback"
    )


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

    Returns "restarted", "user-stopped", "cap-reached", "starting",
    or "not-windows". Bounded at _MAX_AUTO_RESTARTS restarts per
    _RESTART_WINDOW_SEC window (H11); the caller surfaces
    "cap-reached" in the tray status so a crash loop is visible
    instead of silent. Linux is supervised by systemd and never
    auto-restarts from the tray.

    A start already in flight is never duplicated: the poller runs
    every POLL_INTERVAL seconds while a real start can take much
    longer to answer health, and restarting over an in-flight start
    spawned duplicate backends racing for the port (Errno 10048 in
    the backend log, 2026-10-29) and burned the whole restart cap on
    a single slow start. A start that has not come up within
    _START_GRACE_SEC is treated as failed and supervision resumes.
    """
    global _backend_starting, _cap_notice_logged  # noqa: PLW0603
    if platform.system() != "Windows":
        return "not-windows"
    if _user_stopped:
        return "user-stopped"
    if _backend_starting:
        if time.monotonic() - _backend_start_mono < _START_GRACE_SEC:
            return "starting"
        _backend_starting = False
        _tray_log(
            f"backend start did not come up within {_START_GRACE_SEC}s; "
            "treating the start as failed"
        )
    now = time.monotonic()
    _restart_times[:] = [t for t in _restart_times if now - t < _RESTART_WINDOW_SEC]
    if len(_restart_times) >= _MAX_AUTO_RESTARTS:
        if not _cap_notice_logged:
            _cap_notice_logged = True
            _tray_log(
                f"auto-restart cap reached ({_MAX_AUTO_RESTARTS} restarts "
                f"per {_RESTART_WINDOW_SEC}s); supervision is holding"
            )
        return "cap-reached"
    _restart_times.append(now)
    _tray_log(
        f"auto-restart {len(_restart_times)}/{_MAX_AUTO_RESTARTS} "
        f"(window {_RESTART_WINDOW_SEC}s)"
    )
    _start_backend()
    return "restarted"


def _quit(icon, _item=None):
    """Exit the tray application."""
    icon.stop()


# ── Status polling thread ────────────────────────────────────────────

_MAX_POLL_ITERATIONS = 86400 // POLL_INTERVAL  # one ~24 h bounded segment (H11)


def _poll_once(icon: pystray.Icon) -> None:
    """One health poll: refresh the icon/status and supervise."""
    global _status_text, _status_error, _backend_starting  # noqa: PLW0603
    health = _check_health()
    if health is None:
        # Spec 080: on Windows the tray is the supervisor — a
        # backend that died on its own is restarted (capped); a
        # user stop is left alone and labelled as such; a start
        # already in flight is left to finish booting.
        outcome = _maybe_auto_restart()
        if outcome == "starting":
            icon.icon = _create_icon_image("yellow")
            icon.title = "Glossa Lab - Starting..."
            _status_text = "Backend: Starting..."
            _status_error = False
        elif outcome == "user-stopped":
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab - Backend stopped"
            _status_text = "Backend: Stopped by user"
            _status_error = True
        elif outcome == "cap-reached":
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab - Backend stopped"
            _status_text = (
                "Backend: Stopped - auto-restart limit reached "
                "(click to view log)"
            )
            _status_error = True
        elif outcome == "restarted":
            icon.icon = _create_icon_image("yellow")
            icon.title = "Glossa Lab - Starting..."
            _status_text = "Backend: Restarting..."
            _status_error = False
        else:  # "not-windows" — systemd supervises; the tray only reports
            icon.icon = _create_icon_image("red")
            icon.title = "Glossa Lab - Backend stopped"
            _status_text = "Backend: Stopped  (click to view log)"
            _status_error = True
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


def _poll_segment(icon: pystray.Icon) -> None:
    """One bounded polling segment: _MAX_POLL_ITERATIONS polls (H11).

    A single failed poll is written to the tray log and polling
    continues; one bad poll must never end supervision.
    """
    for _poll_iter in range(_MAX_POLL_ITERATIONS):
        try:
            _poll_once(icon)
        except Exception as exc:  # noqa: BLE001
            _tray_log(f"status poll failed: {type(exc).__name__}: {exc}")
        time.sleep(POLL_INTERVAL)


def _status_poller(icon: pystray.Icon):
    """Background thread: polls health every POLL_INTERVAL seconds.

    Started via icon.run(setup=…) so icon.visible is already True.
    Runs as a daemon thread and is killed automatically on exit.

    Polling runs in bounded segments of _MAX_POLL_ITERATIONS polls
    (H11: every loop bounded, expiry diagnosed). When a segment
    ends — by reaching its bound or by an unexpected failure — the
    renewal is written to the tray log and a fresh segment begins.
    The previous design let the thread END at the bound with only a
    print (invisible under pythonw): after ~24 h the tray kept
    showing its last status forever with supervision silently over.
    """
    _tray_log("status poller started")
    segment = 0
    while True:
        segment += 1
        try:
            _poll_segment(icon)
        except Exception as exc:  # noqa: BLE001
            _tray_log(
                f"status poller segment {segment} failed: "
                f"{type(exc).__name__}: {exc}; renewing"
            )
        else:
            _tray_log(
                f"status poller segment {segment} reached the "
                f"{_MAX_POLL_ITERATIONS}-poll bound; renewing"
            )


# ── Entry point ──────────────────────────────────────────────────────

def main():
    """Launch the Glossa Lab system tray icon."""
    _tray_log("tray starting")
    menu = pystray.Menu(
        pystray.MenuItem("Open UI", _open_ui, default=True),
        pystray.MenuItem("Copy API Token", _copy_api_token),
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

    # Ensure autostart is registered on first launch (idempotent).
    # A failed install is written to the tray log by _set_autostart
    # instead of being silently retried on every launch.
    if not _is_autostart_enabled():
        _set_autostart(True)

    def _on_setup(ic: pystray.Icon) -> None:
        """Called by pystray after the icon is displayed and the event loop running.
        Only here is ic.visible reliably True and the menu repaint safe.
        """
        ic.visible = True
        poller = threading.Thread(target=_status_poller, args=(ic,), daemon=True)
        poller.start()
        _tray_log("tray icon visible; status poller running")

    icon.run(setup=_on_setup)


if __name__ == "__main__":
    main()
