"""System status endpoint (REQ-API-002)."""

import platform
import time
from datetime import datetime, timezone

from fastapi import APIRouter

from glossa_lab import __version__
from glossa_lab.catalog import get_catalog_summary
from glossa_lab.database import get_db
from glossa_lab.engine import get_registered_pipelines

router = APIRouter()


@router.get("/status")
async def status():
    """Return detailed system status including job counts and pipeline states.

    Satisfies REQ-API-002.

    Spec 081 (FR-007): status surfaces show identity — what is
    serving, where, and since when — not liveness alone. The identity
    block lives here rather than on /health, whose key set is pinned
    minimal by TEST-SEC-002.
    """
    from glossa_lab.main import get_ollama_state, get_start_time  # noqa: PLC0415

    start = get_start_time()
    uptime = time.time() - start if start > 0 else 0.0

    data_dir = ""
    try:
        from glossa_lab.config import get_settings

        data_dir = str(get_settings().data_dir)
    except Exception:  # noqa: BLE001 — identity is best-effort
        data_dir = ""

    db = get_db()
    job_counts = (
        await db.get_job_counts()
        if db
        else {
            "total": 0,
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
        }
    )
    pipelines = get_registered_pipelines()

    # Spec 083 (T027): the dataset identity the shell's dataset chip
    # renders — the bundle currently in place (C083-13), or None when
    # no bundle has been hydrated into this data dir. Best-effort,
    # like the rest of the identity block: a missing or unreadable
    # manifest means "no bundle identity to state", never an error.
    dataset = None
    if data_dir:
        try:
            import os

            from glossa_lab.cloud_bundles import MANIFEST_NAME, served_manifest

            manifest = served_manifest(data_dir)
            if manifest is not None:
                hydrated_at = ""
                try:
                    mtime = os.path.getmtime(os.path.join(data_dir, MANIFEST_NAME))
                    hydrated_at = datetime.fromtimestamp(
                        mtime, tz=timezone.utc
                    ).isoformat()
                except Exception:  # noqa: BLE001 — mtime is best-effort
                    hydrated_at = ""
                dataset = {
                    "bundle_id": manifest.bundle_id,
                    "source_commit": manifest.source_commit,
                    "built_at": manifest.built_at,
                    "hydrated_at": hydrated_at,
                }
        except Exception:  # noqa: BLE001 — identity is best-effort
            dataset = None

    ollama = get_ollama_state()
    return {
        "status": "healthy",
        "version": __version__,
        "uptime_seconds": round(uptime, 1),
        # ── Spec 081 identity block (FR-007) ─────────────────────────
        "app": "Glossa Lab",
        "host": platform.node(),
        "started_at": (
            datetime.fromtimestamp(start, tz=timezone.utc).isoformat()
            if start > 0
            else ""
        ),
        "data_dir": data_dir,
        "dataset": dataset,
        "db_ready": db is not None,
        "jobs": job_counts,
        "job_counts": job_counts,
        "pipelines": pipelines,
        "pipeline_count": len(pipelines),
        "catalog_counts": get_catalog_summary(),
        "ollama_installed": ollama["installed"],
        "ollama_running": ollama["started"],
    }
