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
from glossa_lab.api.ag2_chat import router as ag2_chat_router
from glossa_lab.api.ai_endpoints import router as ai_endpoints_router
from glossa_lab.api.ai_profiles import router as ai_profiles_router
from glossa_lab.api.ai_tools import router as ai_tools_router
from glossa_lab.api.analysis import router as analysis_router
from glossa_lab.api.anchor_sets import router as anchor_sets_router
from glossa_lab.api.cas_models import router as cas_models_router
from glossa_lab.api.catalog import router as catalog_router
from glossa_lab.api.cgsa import router as cgsa_router
from glossa_lab.api.collab import router as collab_router
from glossa_lab.api.corpus_catalogue import router as corpus_catalogue_router
from glossa_lab.api.dashboard import router as dashboard_router
from glossa_lab.api.discovery import router as discovery_router
from glossa_lab.api.notifications import router as notifications_router
from glossa_lab.api.env import router as env_router
from glossa_lab.api.experiment_graphs import router as experiment_graphs_router
from glossa_lab.api.experiments import router as experiments_router
from glossa_lab.api.health import router as health_router
from glossa_lab.api.jobs import router as jobs_router
from glossa_lab.api.ollama import router as ollama_router
from glossa_lab.api.pipelines import router as pipelines_router
from glossa_lab.api.presets import router as presets_router
from glossa_lab.api.rag import router as rag_router
from glossa_lab.api.report_templates import router as report_templates_router
from glossa_lab.api.reports import router as reports_router
from glossa_lab.api.research import router as research_router
from glossa_lab.api.foundation_check import router as foundation_check_router
from glossa_lab.api.results import router as results_router
from glossa_lab.api.settings import router as settings_router
from glossa_lab.api.shutdown import router as shutdown_router
from glossa_lab.api.status import router as status_router
from glossa_lab.api.studies import router as studies_router
from glossa_lab.api.system import router as system_router
from glossa_lab.api.terminal import router as terminal_router
from glossa_lab.api.projects import router as projects_router
from glossa_lab.api.correspondences import router as correspondences_router
from glossa_lab.api.model_assignments import router as model_assignments_router
from glossa_lab.api.provider_registry import router as provider_registry_router
from glossa_lab.model_intelligence import router as model_intelligence_router
from glossa_lab.api.texts import router as texts_router
from glossa_lab.config import get_settings
from glossa_lab.database import close_db, init_db
from glossa_lab.engine import run_engine_loop
from glossa_lab.log_setup import setup_logging
from glossa_lab.node_registry import router as node_registry_router

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

    # Seed world language corpus catalogue (idempotent upserts)
    from glossa_lab.corpus_catalogue_seeder import seed_corpus_catalogue  # noqa: PLC0415

    await seed_corpus_catalogue()

    # Seed default report templates (idempotent — skips existing IDs)
    from glossa_lab.report_template_seeder import seed_report_templates  # noqa: PLC0415

    await seed_report_templates()

    # Seed default research project (idempotent — skips if projects exist)
    from glossa_lab.project_seeder import seed_projects  # noqa: PLC0415

    if _db:
        await seed_projects(_db)

    # Seed built-in CAS-YAML constraint models into DB (idempotent)
    from glossa_lab.cas_model_seeder import seed_cas_models  # noqa: PLC0415

    if _db:
        await seed_cas_models(_db)

    # Start Ollama in the background (no-op if not installed or already running)
    await asyncio.get_event_loop().run_in_executor(None, _try_start_ollama)

    # Build RAG index in the background (non-blocking — completes while app starts)
    from glossa_lab.rag import build_index as _rag_build  # noqa: PLC0415

    asyncio.create_task(_rag_build(_db))  # fire and forget

    # Register graph experiments into the ExperimentBase discovery registry
    from glossa_lab.experiment_graph import (  # noqa: PLC0415
        auto_migrate_hardcoded_experiments,
        register_graph_experiments,
    )

    register_graph_experiments()
    # Migrate any Python experiments not yet represented as graph files (idempotent)
    auto_migrate_hardcoded_experiments()

    # Start pipeline engine in background
    engine_task = asyncio.create_task(run_engine_loop())

    # Optional: start the discovery scheduler when GLOSSA_DISCOVERY_DAILY=1.
    from glossa_lab.discovery.scheduler import start_scheduler  # noqa: PLC0415

    discovery_task = start_scheduler()

    # Probe all enabled providers to refresh available_models (non-blocking)
    async def _probe_all_providers() -> None:
        from glossa_lab.api.provider_registry import probe_provider  # noqa: PLC0415
        _pdb = get_db()
        if _pdb is None:
            return
        try:
            provs = await _pdb.list_providers(enabled_only=True)
            for prov in provs:
                try:
                    result = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda p=prov: probe_provider(
                            p["provider_type"], p.get("provider_id", ""),
                            p["base_url"], p["api_key"], p.get("headers"),
                        ),
                    )
                    from datetime import datetime as _dt, timezone as _tz  # noqa: PLC0415
                    await _pdb.update_provider(
                        prov["id"],
                        status="reachable" if result["valid"] else "unreachable",
                        available_models=result.get("models", []),
                        last_probed_at=_dt.now(_tz.utc).isoformat(),
                    )
                except Exception:  # noqa: BLE001
                    pass
        except Exception:  # noqa: BLE001
            pass
    asyncio.create_task(_probe_all_providers())

    # Start model intelligence sync (HF leaderboard → model_scores)
    from glossa_lab.model_intelligence import start_intelligence_sync  # noqa: PLC0415
    intel_task = asyncio.create_task(start_intelligence_sync())

    _start_time = time.time()
    yield
    # Shutdown: stop engine + scheduler, close database, flush logs
    engine_task.cancel()
    try:
        await engine_task
    except asyncio.CancelledError:
        pass
    if discovery_task is not None:
        discovery_task.cancel()
        try:
            await discovery_task
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
    application.include_router(collab_router, prefix="/api/v1")
    application.include_router(analysis_router, prefix="/api/v1")
    application.include_router(research_router, prefix="/api/v1")
    application.include_router(foundation_check_router, prefix="/api/v1/research")
    application.include_router(ai_tools_router, prefix="/api/v1")
    application.include_router(system_router, prefix="/api/v1")
    application.include_router(ollama_router, prefix="/api/v1")
    application.include_router(terminal_router, prefix="/api/v1")
    application.include_router(settings_router)
    application.include_router(shutdown_router, prefix="/api/v1")
    application.include_router(env_router, prefix="/api/v1")
    application.include_router(node_registry_router, prefix="/api/v1")
    application.include_router(rag_router, prefix="/api/v1")
    application.include_router(experiment_graphs_router, prefix="/api/v1")
    application.include_router(report_templates_router, prefix="/api/v1")
    application.include_router(anchor_sets_router, prefix="/api/v1")
    application.include_router(corpus_catalogue_router, prefix="/api/v1")
    application.include_router(cas_models_router, prefix="/api/v1")
    application.include_router(ag2_chat_router, prefix="/api/v1")
    application.include_router(cgsa_router, prefix="/api/v1")
    application.include_router(discovery_router)  # already prefixed at /api/v1/discovery
    application.include_router(dashboard_router)   # already prefixed at /api/v1/dashboard
    application.include_router(notifications_router)  # already prefixed at /api/v1/notifications
    application.include_router(ai_endpoints_router)  # already prefixed at /api/v1/ai-endpoints
    application.include_router(ai_profiles_router)   # already prefixed at /api/v1/ai-profiles
    application.include_router(projects_router)        # already prefixed at /api/v1/projects
    application.include_router(correspondences_router)  # already prefixed at /api/v1/correspondences
    application.include_router(provider_registry_router)  # /api/v1/providers
    application.include_router(model_assignments_router)  # /api/v1/model-assignments
    application.include_router(model_intelligence_router)  # /api/v1/model-intelligence

    # Serve built frontend
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
