"""Terminal and log streaming API for the Glossa Lab IDE panel.

Endpoints:
  POST /terminal/run         -- run a command in the Glossa-Lab venv, stream output via SSE
  GET  /terminal/log/stream  -- SSE: tail the backend log file in real time
  GET  /terminal/log         -- return last N lines of the backend log
"""

from __future__ import annotations

import asyncio
import json
import os
import queue
import subprocess
import sys
import threading
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/terminal", tags=["terminal"])

_REPO_ROOT = (
    Path(__file__).resolve().parent.parent.parent.parent
)  # backend/glossa_lab/api -> repo root
_BACKEND_DIR = _REPO_ROOT / "backend"
_LOG_FILE = _BACKEND_DIR / "logs" / "backend.log"
_VENV_PYTHON = str(
    _BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    if sys.platform == "win32"
    else _BACKEND_DIR / "venv" / "bin" / "python"
)


def _sse(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Command execution ─────────────────────────────────────────────────────────


class RunRequest(BaseModel):
    command: str  # shell command to run
    cwd: str | None = None  # working dir relative to repo root; None = backend/
    use_venv: bool = True  # if True, prepend venv python path


async def _stream_command(command: str, cwd: Path) -> AsyncGenerator[str, None]:
    """Run a shell command in a daemon thread and stream output lines as SSE.

    Uses cmd.exe on Windows and /bin/sh on Unix/macOS.
    This avoids asyncio subprocess issues on Windows (ProactorEventLoop required).
    """
    yield _sse("started", {"command": command, "cwd": str(cwd)})

    env = os.environ.copy()
    env["PYTHONPATH"] = str(_BACKEND_DIR)

    # cmd.exe on Windows, sh on Unix
    if sys.platform == "win32":
        shell_args = ["cmd.exe", "/c", command]
    else:
        shell_args = ["/bin/sh", "-c", command]

    q: queue.Queue[tuple[str, Any] | None] = queue.Queue()

    def _run() -> None:
        try:
            proc = subprocess.Popen(
                shell_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=str(cwd),
                env=env,
            )
            assert proc.stdout is not None
            for raw_line in proc.stdout:
                q.put(("line", raw_line.decode(errors="replace").rstrip("\r\n")))
            proc.wait()
            q.put(("done", proc.returncode))
        except Exception as exc:  # noqa: BLE001
            q.put(("error", str(exc)))
        finally:
            q.put(None)  # sentinel

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    loop = asyncio.get_event_loop()
    try:
        while True:
            item = await loop.run_in_executor(None, q.get)
            if item is None:
                break
            event_type, data = item
            if event_type == "line":
                yield _sse("line", {"text": data})
            elif event_type == "done":
                yield _sse("done", {"return_code": data})
            elif event_type == "error":
                yield _sse("error", {"message": data})
    except asyncio.CancelledError:
        return


@router.post("/run")
async def run_command(body: RunRequest) -> StreamingResponse:
    """Execute a command in the Glossa-Lab environment and stream output.

    Output is streamed as SSE events: started, line (per line), done / error.
    """
    # Determine working directory
    if body.cwd:
        cwd = _REPO_ROOT / body.cwd
    else:
        cwd = _BACKEND_DIR

    if not cwd.exists():
        raise HTTPException(status_code=400, detail=f"Working directory not found: {cwd}")

    command = body.command

    # Prefix 'python' commands with the venv python path for convenience
    if body.use_venv and (command.startswith("python ") or command == "python"):
        command = f'"{_VENV_PYTHON}" {command[7:]}'

    return StreamingResponse(
        _stream_command(command, cwd),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Log streaming ─────────────────────────────────────────────────────────────


@router.get("/log")
async def get_log(lines: int = 200) -> dict[str, Any]:
    """Return the last N lines of the backend log file."""
    if not _LOG_FILE.exists():
        return {"lines": [], "file": str(_LOG_FILE), "exists": False}
    try:
        text = _LOG_FILE.read_text(encoding="utf-8", errors="replace")
        all_lines = text.splitlines()
        tail = all_lines[-lines:] if len(all_lines) > lines else all_lines
        return {
            "lines": tail,
            "file": str(_LOG_FILE),
            "exists": True,
            "total_lines": len(all_lines),
        }
    except Exception as exc:  # noqa: BLE001
        return {"lines": [], "file": str(_LOG_FILE), "exists": True, "error": str(exc)}


async def _tail_log() -> AsyncGenerator[str, None]:
    """Yield new log lines as SSE events, then stream new additions in real time."""
    # First: send last 100 lines
    if _LOG_FILE.exists():
        try:
            text = _LOG_FILE.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines()[-100:]:
                yield f"data: {json.dumps({'text': line, 'backfill': True})}\n\n"
        except Exception:  # noqa: BLE001
            pass

    # Then: watch for new content
    offset = _LOG_FILE.stat().st_size if _LOG_FILE.exists() else 0
    try:
        while True:
            await asyncio.sleep(0.5)
            if not _LOG_FILE.exists():
                continue
            size = _LOG_FILE.stat().st_size
            if size > offset:
                try:
                    with open(str(_LOG_FILE), encoding="utf-8", errors="replace") as f:
                        f.seek(offset)
                        new_text = f.read()
                    offset = size
                    for line in new_text.splitlines():
                        if line.strip():
                            yield f"data: {json.dumps({'text': line, 'backfill': False})}\n\n"
                except Exception:  # noqa: BLE001
                    pass
    except asyncio.CancelledError:
        return


@router.get("/log/stream")
async def stream_log() -> StreamingResponse:
    """SSE: tail the backend log file (100-line backfill + live updates every 500ms)."""
    return StreamingResponse(
        _tail_log(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
