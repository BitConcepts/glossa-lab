"""Terminal and log streaming API for the Glossa Lab IDE panel.

Endpoints:
  POST /terminal/run         -- run a command via GlossaShell, stream output via SSE
  GET  /terminal/log/stream  -- SSE: tail the backend log file in real time
  GET  /terminal/log         -- return last N lines of the backend log

GlossaShell handles cross-platform command dispatch with no visible window:
  - Common commands (ls, cat, grep, find, ...) run as Python builtins
  - Unknown commands fall back to OS subprocess with CREATE_NO_WINDOW
  - 'python' is automatically redirected to the Glossa Lab venv
"""

from __future__ import annotations

import asyncio
import json
import queue
import threading
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from glossa_lab.glossa_shell import GlossaShell

router = APIRouter(prefix="/terminal", tags=["terminal"])

_REPO_ROOT   = Path(__file__).resolve().parent.parent.parent.parent  # repo root
_BACKEND_DIR = _REPO_ROOT / "backend"


def _active_log_file() -> Path:
    """Return the most-recently-written glossa.log we can find.

    Selects the **most recently modified** candidate file, which is the
    one currently being written to.  Using file size was wrong: a stale
    rotated file from a previous run can be much larger than the new log.

    Search candidates (in priority order for fallback when none exists):
      1. settings.log_dir / glossa.log        — Python logging output (primary)
      2. {repo_root}/logs / glossa.log         — installed / tray mode
      3. {backend_dir}/logs / glossa.log       — dev mode launched from backend/
      4. {backend_dir}/logs / backend.log      — legacy stdout-redirect file
    """
    from glossa_lab.config import get_settings  # late import avoids circular dep

    candidates = [
        get_settings().log_dir / "glossa.log",
        _REPO_ROOT / "logs" / "glossa.log",
        _BACKEND_DIR / "logs" / "glossa.log",
        _BACKEND_DIR / "logs" / "backend.log",
    ]
    # Pick the most-recently modified file: newest mtime = actively written now.
    # (Size is NOT a valid proxy — a stale multi-MB rotated log beats a fresh
    # 10-line current log and causes the UI to show days-old entries.)
    existing = [(c.stat().st_mtime, c) for c in candidates if c.exists()]
    if existing:
        return max(existing)[1]
    # Nothing exists yet — return the primary path so it picks up when created
    return candidates[0]

# ── Persistent shell singleton ───────────────────────────────────────────
# Reusing one GlossaShell means:
# • Banner is shown once (on terminal open), not on every command
# • `cd` state persists across commands (real shell behaviour)
# • No per-request construction overhead

_shell: GlossaShell | None = None
_shell_lock = threading.Lock()


def _get_shell() -> GlossaShell:
    """Return the process-wide GlossaShell, creating it on first call."""
    global _shell  # noqa: PLW0603
    with _shell_lock:
        if _shell is None:
            _shell = GlossaShell(cwd=_REPO_ROOT, sandbox_root=_REPO_ROOT)
        return _shell


def _sse(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Command execution via GlossaShell ─────────────────────────────────────────


class RunRequest(BaseModel):
    command: str       # shell command to run
    cwd: str | None = None  # working dir relative to repo root; None = repo root
    use_venv: bool = True   # kept for API compatibility; GlossaShell handles this


async def _stream_command(command: str, cwd: Path) -> AsyncGenerator[str, None]:
    """Run *command* via GlossaShell in a daemon thread and stream SSE lines.

    GlossaShell handles all platform differences internally:
      - Common commands run as Python builtins (no subprocess at all)
      - Subprocess fallback uses CREATE_NO_WINDOW on Windows
      - 'python' is resolved to the venv Python automatically
    """
    yield _sse("started", {"command": command, "cwd": str(cwd)})

    q: queue.Queue[tuple[str, Any] | None] = queue.Queue()

    def _run() -> None:
        try:
            shell = _get_shell()
            for line in shell.run(command):
                q.put(("line", line))
            q.put(("done", 0))
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
    """Execute a command via GlossaShell and stream output as SSE.

    Output events: started, line (per line), done / error.
    """
    cwd = (_REPO_ROOT / body.cwd) if body.cwd else _REPO_ROOT
    if not cwd.exists():
        raise HTTPException(status_code=400, detail=f"Directory not found: {cwd}")

    return StreamingResponse(
        _stream_command(body.command, cwd),  # cwd arg kept for compat; shell owns cwd
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Log streaming ─────────────────────────────────────────────────────────────


@router.get("/log")
async def get_log(lines: int = 200) -> dict[str, Any]:
    """Return the last N lines of the backend log file."""
    log_file = _active_log_file()
    if not log_file.exists():
        return {"lines": [], "file": str(log_file), "exists": False}
    try:
        text = log_file.read_text(encoding="utf-8", errors="replace")
        all_lines = text.splitlines()
        tail = all_lines[-lines:] if len(all_lines) > lines else all_lines
        return {
            "lines": tail,
            "file": str(log_file),
            "exists": True,
            "total_lines": len(all_lines),
        }
    except Exception as exc:  # noqa: BLE001
        return {"lines": [], "file": str(log_file), "exists": True, "error": str(exc)}


async def _tail_log() -> AsyncGenerator[str, None]:
    """Yield new log lines as SSE events, then stream new additions in real time."""
    log_file = _active_log_file()

    # First: send last 100 lines (backfill)
    if log_file.exists():
        try:
            text = log_file.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines()[-100:]:
                if line.strip():
                    yield f"data: {json.dumps({'text': line, 'backfill': True})}\n\n"
        except Exception:  # noqa: BLE001
            pass

    # Then: watch for new content; also re-check log file path in case backend restarts
    offset = log_file.stat().st_size if log_file.exists() else 0
    try:
        while True:
            await asyncio.sleep(0.5)
            # Re-resolve the active log file each iteration (handles rotation / restart)
            log_file = _active_log_file()
            if not log_file.exists():
                continue
            size = log_file.stat().st_size
            if size > offset:
                try:
                    with open(str(log_file), encoding="utf-8", errors="replace") as f:
                        f.seek(offset)
                        new_text = f.read()
                    offset = size
                    for line in new_text.splitlines():
                        if line.strip():
                            yield f"data: {json.dumps({'text': line, 'backfill': False})}\n\n"
                except Exception:  # noqa: BLE001
                    pass
            elif size < offset:
                # Log was rotated — restart from beginning of new file
                offset = 0
    except asyncio.CancelledError:
        return


@router.post("/log/purge")
async def purge_log() -> dict:
    """Clear (truncate) the active backend log file. Returns bytes cleared."""
    log_file = _active_log_file()
    if not log_file.exists():
        return {"cleared": 0, "file": str(log_file)}
    try:
        size = log_file.stat().st_size
        log_file.write_text("", encoding="utf-8")
        return {"cleared": size, "file": str(log_file)}
    except Exception as exc:  # noqa: BLE001
        from fastapi import HTTPException  # noqa: PLC0415
        raise HTTPException(500, f"Could not purge log: {exc}") from exc


@router.get("/log/stream")
async def stream_log() -> StreamingResponse:
    """SSE: tail the backend log file (100-line backfill + live updates every 500ms)."""
    return StreamingResponse(
        _tail_log(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
