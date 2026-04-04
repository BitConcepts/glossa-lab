"""Glossa Lab backend application entrypoint."""

import asyncio
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from glossa_lab import __version__
from glossa_lab.api.catalog import router as catalog_router
from glossa_lab.api.health import router as health_router
from glossa_lab.api.jobs import router as jobs_router
from glossa_lab.api.presets import router as presets_router
from glossa_lab.api.reports import router as reports_router
from glossa_lab.api.results import router as results_router
from glossa_lab.api.settings import router as settings_router
from glossa_lab.api.shutdown import router as shutdown_router
from glossa_lab.api.status import router as status_router
from glossa_lab.api.texts import router as texts_router
from glossa_lab.config import get_settings
from glossa_lab.database import close_db, init_db
from glossa_lab.engine import run_engine_loop
from glossa_lab.logging import setup_logging

# Repo root is two levels above this file (backend/glossa_lab/main.py)
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_FRONTEND_DIST = _REPO_ROOT / "frontend" / "dist"

_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    global _start_time  # noqa: PLW0603
    settings = get_settings()
    setup_logging(settings)

    # Initialize database
    await init_db(settings.data_dir)

    # Seed built-in corpora (runs only if DB is empty or missing corpora)
    from glossa_lab.corpus_seeder import seed_corpora  # noqa: I001
    from glossa_lab.database import get_db

    _db = get_db()
    if _db:
        await seed_corpora(_db)

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
    application.include_router(status_router, prefix="/api/v1")
    application.include_router(jobs_router, prefix="/api/v1")
    application.include_router(results_router, prefix="/api/v1")
    application.include_router(texts_router, prefix="/api/v1")
    application.include_router(presets_router, prefix="/api/v1")
    application.include_router(reports_router, prefix="/api/v1")
    application.include_router(settings_router)
    application.include_router(shutdown_router, prefix="/api/v1")

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
