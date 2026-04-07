"""Glossa Lab backend application entrypoint."""

import asyncio
import shutil
import subprocess
import sys
import time
import urllib.request
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from glossa_lab import __version__
from glossa_lab.api.ai_tools import router as ai_tools_router
from glossa_lab.api.analysis import router as analysis_router
from glossa_lab.api.env import router as env_router
from glossa_lab.api.catalog import router as catalog_router
from glossa_lab.api.experiments import router as experiments_router
from glossa_lab.api.health import router as health_router
from glossa_lab.api.jobs import router as jobs_router
from glossa_lab.api.ollama import router as ollama_router
from glossa_lab.api.pipelines import router as pipelines_router
from glossa_lab.api.presets import router as presets_router
from glossa_lab.api.reports import router as reports_router
from glossa_lab.api.research import router as research_router
from glossa_lab.api.results import router as results_router
from glossa_lab.api.settings import router as settings_router
from glossa_lab.api.shutdown import router as shutdown_router
from glossa_lab.api.status import router as status_router
from glossa_lab.api.studies import router as studies_router
from glossa_lab.api.system import router as system_router
from glossa_lab.api.terminal import router as terminal_router
from glossa_lab.api.texts import router as texts_router
from glossa_lab.config import get_settings
from glossa_lab.database import close_db, init_db
from glossa_lab.engine import run_engine_loop
from glossa_lab.logging import setup_logging

# Repo root is two levels above this file (backend/glossa_lab/main.py)
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_FRONTEND_DIST = _REPO_ROOT / "frontend" / "dist"

# ── Ollama lifecycle state ——————————————————————————————————————
_ollama_installed: bool = False
_ollama_started: bool = False


def get_ollama_state() -> dict[str, bool]:
    return {"installed": _ollama_installed, "started": _ollama_started}


def _try_start_ollama() -> None:
    """Start `ollama serve` in the background if Ollama is installed."""
    global _ollama_installed, _ollama_started  # noqa: PLW0603

    exe = shutil.which("ollama")
    if exe is None:
        # Also check common Windows install path
        win_path = Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"
        if win_path.exists():
            exe = str(win_path)

    if exe is None:
        _ollama_installed = False
        return

    _ollama_installed = True

    # Check if already running (quick probe)
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1)  # noqa: S310
        _ollama_started = True
        return  # already serving
    except Exception:  # noqa: BLE001
        pass

    # Not running — start it
    flags: dict = {}
    if sys.platform == "win32":
        flags["creationflags"] = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

    try:
        subprocess.Popen(  # noqa: S603
            [exe, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **flags,
        )
        _ollama_started = True
    except Exception:  # noqa: BLE001
        _ollama_started = False

_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    global _start_time  # noqa: PLW0603
    settings = get_settings()
    setup_logging(settings)

    # Initialize database
    await init_db(settings.data_dir)

    # Seed built-in corpora and pre-built studies on first run
    from glossa_lab.corpus_seeder import seed_corpora  # noqa: I001
    from glossa_lab.study_seeds import seed_studies  # noqa: I001
    from glossa_lab.database import get_db

    _db = get_db()
    if _db:
        await seed_corpora(_db)
        await seed_studies(_db)

    # Start Ollama in the background (no-op if not installed or already running)
    await asyncio.get_event_loop().run_in_executor(None, _try_start_ollama)

    # Start pipeline engine in background
    engine_task = asyncio.create_task(run_engine_loop())

    _start_time = time.time()
    yield
    # Shutdown: stop engine, close database, flush logs
    engine_task.cancel()
    try:
        await engine_task
    except asyncio.CancelledError:
        pass
    await close_db()
    _start_time = 0.0


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title="Glossa Lab",
        version=__version__,
        lifespan=lifespan,
    )

    # CORS — allow localhost origins in development mode
    if settings.dev_mode:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5174",
                "http://localhost:3000",
                "http://127.0.0.1:5174",
                "http://127.0.0.1:3000",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Register routers (must come before static-file mount so API takes priority)
    application.include_router(health_router, prefix="/api/v1")
    application.include_router(catalog_router, prefix="/api/v1")
    application.include_router(experiments_router, prefix="/api/v1")
    application.include_router(pipelines_router, prefix="/api/v1")
    application.include_router(status_router, prefix="/api/v1")
    application.include_router(jobs_router, prefix="/api/v1")
    application.include_router(results_router, prefix="/api/v1")
    application.include_router(texts_router, prefix="/api/v1")
    application.include_router(presets_router, prefix="/api/v1")
    application.include_router(reports_router, prefix="/api/v1")
    application.include_router(studies_router, prefix="/api/v1")
    application.include_router(analysis_router, prefix="/api/v1")
    application.include_router(research_router, prefix="/api/v1")
    application.include_router(ai_tools_router, prefix="/api/v1")
    application.include_router(system_router, prefix="/api/v1")
    application.include_router(ollama_router, prefix="/api/v1")
    application.include_router(terminal_router, prefix="/api/v1")
    application.include_router(settings_router)
    application.include_router(shutdown_router, prefix="/api/v1")
    application.include_router(env_router, prefix="/api/v1")

    # Serve built frontend at "/" — run 'npm run build' in frontend/ to populate.
    # Skipped silently in dev if the dist directory does not yet exist.
    if _FRONTEND_DIST.exists():
        application.mount(
            "/",
            StaticFiles(directory=str(_FRONTEND_DIST), html=True),
            name="frontend",
        )

    return application


def get_start_time() -> float:
    """Return the application start timestamp."""
    return _start_time


app = create_app()
