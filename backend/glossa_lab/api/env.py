"""Python environment management API.

Endpoints:
  GET  /env/status      -- venv path, Python version, package count
  POST /env/setup       -- SSE: create venv + pip install (idempotent)
  POST /env/rebuild     -- SSE: delete venv then run setup
  POST /env/upgrade     -- SSE: pip install --upgrade on all deps
  GET  /env/packages    -- list installed packages
"""
from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/env", tags=["env"])

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_REPO_ROOT   = _BACKEND_DIR.parent

# ── Helpers ───────────────────────────────────────────────────────────────────

def _venv_python() -> Path:
    if sys.platform == "win32":
        return _BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    return _BACKEND_DIR / "venv" / "bin" / "python"


def _venv_pip() -> Path:
    if sys.platform == "win32":
        return _BACKEND_DIR / "venv" / "Scripts" / "pip.exe"
    return _BACKEND_DIR / "venv" / "bin" / "pip"


def _popen_flags() -> dict[str, Any]:
    flags: dict[str, Any] = {}
    if sys.platform == "win32":
        flags["creationflags"] = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]
    return flags


def _system_python() -> str:
    """Return a system Python executable suitable for creating a new venv.

    Prefers python3 / python from PATH, avoiding our own venv interpreter
    (which may no longer exist after a rebuild).
    """
    for name in ("python3", "python"):
        found = shutil.which(name)
        if found:
            venv_dir = _BACKEND_DIR / "venv"
            try:
                if not Path(found).is_relative_to(venv_dir):
                    return found
            except (ValueError, AttributeError):
                return found  # Python < 3.9 fallback
    # Last resort: use sys.executable (may be stale after rebuild but worth trying)
    return sys.executable


def _get_python_version(py: Path) -> str:
    try:
        result = subprocess.run(  # noqa: S603
            [str(py), "--version"],
            capture_output=True, text=True, timeout=5,
            **_popen_flags(),
        )
        return (result.stdout or result.stderr).strip().replace("Python ", "")
    except Exception:  # noqa: BLE001
        return "unknown"


def _get_pkg_count(py: Path) -> int:
    try:
        result = subprocess.run(  # noqa: S603
            [str(py), "-m", "pip", "list", "--format=json"],
            capture_output=True, text=True, timeout=15,
            **_popen_flags(),
        )
        pkgs = json.loads(result.stdout or "[]")
        return len(pkgs)
    except Exception:  # noqa: BLE001
        return 0


def _sse(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Status ────────────────────────────────────────────────────────────────────

@router.get("/status")
async def env_status() -> dict[str, Any]:
    """Return Python venv status."""
    py = _venv_python()
    venv_exists = py.exists()
    version = _get_python_version(py) if venv_exists else None
    pkg_count = _get_pkg_count(py) if venv_exists else 0

    return {
        "venv_exists": venv_exists,
        "venv_path": str(_BACKEND_DIR / "venv"),
        "python_path": str(py) if venv_exists else None,
        "python_version": version,
        "pkg_count": pkg_count,
        "backend_dir": str(_BACKEND_DIR),
    }


# ── SSE stream helper ─────────────────────────────────────────────────────────

async def _stream_setup(rebuild: bool = False) -> AsyncGenerator[str, None]:
    """Run venv setup and stream SSE output lines."""
    import queue  # noqa: PLC0415
    import threading  # noqa: PLC0415

    yield _sse("started", {"rebuild": rebuild})

    q: queue.Queue[tuple[str, str] | None] = queue.Queue()

    def _run() -> None:
        try:
            py = _venv_python()
            venv_dir = _BACKEND_DIR / "venv"

            # --- Step 1: optionally remove old venv ---
            if rebuild and venv_dir.exists():
                q.put(("line", "Removing existing venv…"))
                shutil.rmtree(venv_dir)
                q.put(("line", "✓ Removed."))

            # --- Step 2: create venv if missing ---
            if not py.exists():
                q.put(("line", f"Creating venv at {venv_dir}…"))
                base_py = _system_python()
                q.put(("line", f"  Using system Python: {base_py}"))
                proc = subprocess.run(  # noqa: S603
                    [base_py, "-m", "venv", str(venv_dir)],
                    capture_output=True, text=True, cwd=str(_BACKEND_DIR),
                    **_popen_flags(),
                )
                if proc.returncode != 0:
                    q.put(("error", f"venv creation failed: {proc.stderr[:300]}"))
                    q.put(None)
                    return
                q.put(("line", "✓ venv created."))
            else:
                q.put(("line", "venv already exists — skipping creation."))

            # --- Step 3: upgrade pip ---
            q.put(("line", "Upgrading pip…"))
            subprocess.run(  # noqa: S603
                [str(py), "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                cwd=str(_BACKEND_DIR), **_popen_flags(),
            )

            # --- Step 4: install project deps ---
            q.put(("line", "Installing dependencies (pyproject.toml [dev])…"))
            proc2 = subprocess.Popen(  # noqa: S603
                [str(py), "-m", "pip", "install", "-e", ".[dev]"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, cwd=str(_BACKEND_DIR), **_popen_flags(),
            )
            assert proc2.stdout is not None
            for line in proc2.stdout:
                line = line.rstrip()
                if line:
                    q.put(("line", line))
            proc2.wait()
            if proc2.returncode == 0:
                q.put(("done", "✓ Environment ready."))
            else:
                q.put(("error", f"pip install failed (exit {proc2.returncode})"))
        except Exception as exc:  # noqa: BLE001
            q.put(("error", str(exc)))
        finally:
            q.put(None)

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    loop = asyncio.get_event_loop()
    try:
        while True:
            item = await loop.run_in_executor(None, q.get)
            if item is None:
                break
            event_type, data = item
            yield _sse(event_type, {"text": data})
    except asyncio.CancelledError:
        return


async def _stream_upgrade() -> AsyncGenerator[str, None]:
    """Upgrade all project dependencies."""
    import queue  # noqa: PLC0415
    import threading  # noqa: PLC0415

    yield _sse("started", {"action": "upgrade"})
    q: queue.Queue[tuple[str, str] | None] = queue.Queue()

    def _run() -> None:
        try:
            py = _venv_python()
            if not py.exists():
                q.put(("error", "No venv found. Run setup first."))
                q.put(None)
                return
            q.put(("line", "Upgrading dependencies…"))
            proc = subprocess.Popen(  # noqa: S603
                [str(py), "-m", "pip", "install", "--upgrade", "-e", ".[dev]"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, cwd=str(_BACKEND_DIR), **_popen_flags(),
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                line = line.rstrip()
                if line:
                    q.put(("line", line))
            proc.wait()
            if proc.returncode == 0:
                q.put(("done", "✓ Dependencies upgraded."))
            else:
                q.put(("error", f"Upgrade failed (exit {proc.returncode})"))
        except Exception as exc:  # noqa: BLE001
            q.put(("error", str(exc)))
        finally:
            q.put(None)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    loop = asyncio.get_event_loop()
    try:
        while True:
            item = await loop.run_in_executor(None, q.get)
            if item is None:
                break
            event_type, data = item
            yield _sse(event_type, {"text": data})
    except asyncio.CancelledError:
        return


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/setup")
async def env_setup() -> StreamingResponse:
    """Create venv (if missing) and install all dependencies. SSE stream."""
    return StreamingResponse(
        _stream_setup(rebuild=False),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/rebuild")
async def env_rebuild() -> StreamingResponse:
    """Delete existing venv and recreate from scratch. SSE stream."""
    return StreamingResponse(
        _stream_setup(rebuild=True),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/upgrade")
async def env_upgrade() -> StreamingResponse:
    """Upgrade all dependencies in existing venv. SSE stream."""
    return StreamingResponse(
        _stream_upgrade(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/packages")
async def env_packages() -> dict[str, Any]:
    """List all installed packages in the venv."""
    py = _venv_python()
    if not py.exists():
        return {"packages": [], "count": 0, "venv_exists": False}
    try:
        result = subprocess.run(  # noqa: S603
            [str(py), "-m", "pip", "list", "--format=json"],
            capture_output=True, text=True, timeout=15,
            **_popen_flags(),
        )
        pkgs = json.loads(result.stdout or "[]")
        return {"packages": pkgs, "count": len(pkgs), "venv_exists": True}
    except Exception as exc:  # noqa: BLE001
        return {"packages": [], "count": 0, "venv_exists": True, "error": str(exc)}
