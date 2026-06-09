"""Discovery API — list / classify / curate items surfaced by the engine.

Endpoints (mounted at ``/api/v1/discovery``):

* ``GET  /items``                     — paginated list with topic/kind/status/since filters
* ``GET  /items/{id}``                — fetch one item
* ``POST /items/{id}/status``         — mark reviewed / saved / dismissed (+ notes)
* ``GET  /topics``                    — list topic profiles shipped with the package
* ``GET  /sources``                   — fetcher status (configured? required key?)
* ``GET  /stats``                     — group counts (status / kind / topic / source)
* ``POST /fetch``                     — kick a fetch run as a background Job
* ``POST /mine``                      — kick a mining run as a background Job
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db
from glossa_lab.discovery import scheduler as _scheduler
from glossa_lab.discovery import store
from glossa_lab.discovery.fetchers import (
    available_fetchers,
    list_topics,
    run_all,
    run_topic,
)
from glossa_lab.discovery.llm import LLMClient
from glossa_lab.discovery.mine import mine_pending

router = APIRouter(prefix="/api/v1/discovery", tags=["discovery"])

_log = logging.getLogger("glossa_lab.api.discovery")


# ── Pydantic models ──────────────────────────────────────────────────────────


class StatusUpdate(BaseModel):
    status: str
    notes: str | None = None


class FetchRequest(BaseModel):
    topics: list[str] | None = None    # None = all
    sources: list[str] | None = None   # None = all configured
    since_iso: str | None = None       # ISO-8601; None = no since-filter


class MineRequest(BaseModel):
    topic: str | None = None
    limit: int = 20


class JobAck(BaseModel):
    job_id: str
    status: str
    message: str


# ── Helpers ─────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_since(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=f"since_iso must be ISO-8601 ({exc})"
        ) from exc


async def _create_bg_job(
    *,
    name: str,
    pipeline: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        return await db.create_job(
            name=name,
            pipeline=pipeline,
            params=params,
            created_at=_now_iso(),
            initial_status="running",
        )
    except (ValueError, Exception) as exc:
        # aiosqlite raises ValueError('no active connection') when the DB
        # connection has closed unexpectedly (e.g. after a long-running
        # background task crashes the internal worker).  Convert to 503 so
        # the frontend sees a clear, retryable error instead of an empty-body 500.
        _log.warning("_create_bg_job: DB error creating job '%s': %s", name, exc)
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable — {type(exc).__name__}: {exc}",
        ) from exc


async def _finish_job(
    job_id: str, *, status: str, result: dict[str, Any] | None = None,
) -> None:
    """Persist job completion to the DB.  Never raises — swallows DB errors so a
    broken connection does not produce an unhandled asyncio task exception."""
    db = get_db()
    if db is None:
        return
    try:
        if result is not None:
            await db.store_result(
                job_id=job_id, data=result, created_at=_now_iso(),
            )
        await db.update_job_status(job_id, status)
    except Exception as exc:  # noqa: BLE001
        # Log but never propagate — the background task is already finishing.
        _log.warning("_finish_job: could not persist job %s (%s): %s", job_id, status, exc)


# ── Items ────────────────────────────────────────────────────────────────────


@router.get("/items")
async def list_items(
    topic: str | None = None,
    kind: str | None = None,
    status: str | None = None,
    since: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    items = await store.list_items(
        topic=topic, kind=kind, status=status,
        since=since, limit=limit, offset=offset,
    )
    return {"items": [it.to_dict() for it in items], "limit": limit, "offset": offset}


@router.get("/items/{item_id}")
async def get_item(item_id: str) -> dict[str, Any]:
    item = await store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.to_dict()


@router.post("/items/{item_id}/status")
async def update_status(item_id: str, body: StatusUpdate) -> dict[str, Any]:
    item = await store.update_status(item_id, status=body.status, notes=body.notes)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.to_dict()


# ── Topics + sources ────────────────────────────────────────────────────────


@router.get("/topics")
async def list_topics_endpoint() -> dict[str, Any]:
    profiles = list_topics()
    return {
        "topics": [
            {
                "id": t.id,
                "label": t.label,
                "description": t.description,
                "keywords": t.keywords,
                "exclusions": t.exclusions,
                "languages": t.languages,
            }
            for t in profiles
        ],
    }


@router.get("/sources")
async def list_sources_endpoint() -> dict[str, Any]:
    return {"sources": available_fetchers()}


@router.get("/stats")
async def stats(group: str = "status") -> dict[str, Any]:
    counts = await store.count_by(group=group)
    return {"group": group, "counts": counts}


# ── Background runs ─────────────────────────────────────────────────────────


@router.post("/fetch")
async def fetch_endpoint(body: FetchRequest) -> JobAck:
    """Start a fetch in the background and return a Job id immediately."""
    since = _parse_since(body.since_iso)
    job = await _create_bg_job(
        name="Discovery: fetch  [API]",
        pipeline="discovery_fetch",
        params={
            "topics": body.topics,
            "sources": body.sources,
            "since_iso": body.since_iso,
        },
    )
    job_id = job["id"]

    async def _runner() -> None:
        try:
            if body.topics:
                summaries = []
                for tid in body.topics:
                    summaries.append(
                        await run_topic(tid, since=since, only_sources=body.sources)
                    )
                result = {
                    "topics_run": list(body.topics),
                    "results": summaries,
                    "fetched": sum(int(s.get("fetched", 0)) for s in summaries),
                    "new": sum(int(s.get("new", 0)) for s in summaries),
                    "merged": sum(int(s.get("merged", 0)) for s in summaries),
                    "errors": sum(int(s.get("errors", 0)) for s in summaries),
                }
            else:
                result = await run_all(since=since, only_sources=body.sources)
            await _finish_job(job_id, status="completed", result=result)
        except Exception as exc:  # noqa: BLE001
            _log.warning("discovery fetch job %s failed: %s", job_id, exc)
            await _finish_job(
                job_id,
                status="failed",
                result={"error": f"{type(exc).__name__}: {exc}"},
            )

    asyncio.create_task(_runner(), name=f"discovery_fetch_{job_id}")
    return JobAck(job_id=job_id, status="running", message="Fetch started")


@router.post("/mine")
async def mine_endpoint(body: MineRequest) -> JobAck:
    """Start a mining run in the background."""
    client = LLMClient()
    if not client.configured_providers():
        raise HTTPException(
            status_code=400,
            detail=(
                "No LLM provider configured. Set MISTRAL_API_KEY / OPENAI_API_KEY "
                "/ GOOGLE_API_KEY in Settings before mining."
            ),
        )
    job = await _create_bg_job(
        name="Discovery: mine  [API]",
        pipeline="discovery_mine",
        params={"topic": body.topic, "limit": body.limit},
    )
    job_id = job["id"]

    async def _runner() -> None:
        try:
            result = await mine_pending(
                client=client, topic=body.topic, limit=body.limit,
            )
            await _finish_job(job_id, status="completed", result=result)
        except Exception as exc:  # noqa: BLE001
            _log.warning("discovery mine job %s failed: %s", job_id, exc)
            # _finish_job now swallows its own exceptions, so this is safe
            # even when the DB connection has gone stale.
            await _finish_job(
                job_id,
                status="failed",
                result={"error": f"{type(exc).__name__}: {exc}"},
            )

    asyncio.create_task(_runner(), name=f"discovery_mine_{job_id}")
    return JobAck(job_id=job_id, status="running", message="Mine started")


# ── Manual import ────────────────────────────────────────────────────


class ImportPDFRequest(BaseModel):
    """Import a local PDF file as a discovery item."""
    file_path: str
    topic: str = "indus_script"
    source: str = "local_pdf"


class ImportBatchRequest(BaseModel):
    """Import multiple local PDF files."""
    file_paths: list[str]
    topic: str = "indus_script"
    source: str = "local_pdf"


def _extract_pdf_text(file_path: str, max_pages: int = 10) -> tuple[str, str]:
    """Extract title and text from a PDF. Returns (title, text)."""
    from pathlib import Path as _P  # noqa: PLC0415
    p = _P(file_path)
    if not p.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    title = p.stem.replace("_", " ").replace("  ", " ").strip()
    text = ""

    # Try pdfplumber first (better text extraction)
    try:
        import pdfplumber  # noqa: PLC0415
        with pdfplumber.open(str(p)) as pdf:
            pages = pdf.pages[:max_pages]
            chunks = []
            for page in pages:
                t = page.extract_text()
                if t:
                    chunks.append(t)
            text = "\n".join(chunks)
            # Try to extract title from first line
            if chunks and chunks[0].strip():
                first_lines = chunks[0].strip().split("\n")
                candidate = first_lines[0].strip()
                if 10 < len(candidate) < 200 and not candidate[0].isdigit():
                    title = candidate
        return title, text[:5000]  # cap at 5K chars
    except Exception:  # noqa: BLE001
        pass

    # Fallback: pymupdf
    try:
        import fitz  # noqa: PLC0415
        doc = fitz.open(str(p))
        chunks = []
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            t = page.get_text()
            if t:
                chunks.append(t)
        text = "\n".join(chunks)
        if chunks and chunks[0].strip():
            first_lines = chunks[0].strip().split("\n")
            candidate = first_lines[0].strip()
            if 10 < len(candidate) < 200 and not candidate[0].isdigit():
                title = candidate
        doc.close()
        return title, text[:5000]
    except Exception:  # noqa: BLE001
        pass

    return title, f"(PDF text extraction failed for {p.name})"


@router.post("/import-pdf")
async def import_pdf(body: ImportPDFRequest) -> dict[str, Any]:
    """Import a local PDF file as a discovery item.

    Extracts title and text from the PDF, creates a discovery item,
    and optionally classifies it. Returns the created item.
    """
    try:
        title, text = _extract_pdf_text(body.file_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {exc}") from exc

    from pathlib import Path as _P  # noqa: PLC0415
    filename = _P(body.file_path).name
    url = f"file:///{body.file_path.replace(chr(92), '/')}"

    # Create the discovery item
    raw_item = store.RawItem(
        title=title,
        url=url,
        source=body.source,
        topic=body.topic,
        published_at=_now_iso(),
        lang="en",
        raw={
            "filename": filename,
            "text_preview": text[:2000],
            "text_length": len(text),
            "import_method": "manual_pdf",
        },
    )
    is_new = await store.upsert_raw(raw_item)

    # Auto-classify with summary from extracted text
    summary = text[:500].replace("\n", " ").strip()
    if summary:
        await store.update_classification(
            raw_item.item_id,
            kind="paper",
            confidence=0.9,
            summary=summary,
        )

    item = await store.get(raw_item.item_id)
    return {
        "ok": True,
        "is_new": is_new,
        "item_id": raw_item.item_id,
        "title": title,
        "text_length": len(text),
        "item": item.to_dict() if item else None,
    }


@router.post("/import-batch")
async def import_batch(body: ImportBatchRequest) -> dict[str, Any]:
    """Import multiple local PDF files as discovery items."""
    results: list[dict[str, Any]] = []
    imported = 0
    errors = 0

    for fp in body.file_paths:
        try:
            title, text = _extract_pdf_text(fp)
        except Exception as exc:  # noqa: BLE001
            results.append({"file": fp, "ok": False, "error": str(exc)})
            errors += 1
            continue

        from pathlib import Path as _P  # noqa: PLC0415
        filename = _P(fp).name
        url = f"file:///{fp.replace(chr(92), '/')}"

        raw_item = store.RawItem(
            title=title,
            url=url,
            source=body.source,
            topic=body.topic,
            published_at=_now_iso(),
            lang="en",
            raw={
                "filename": filename,
                "text_preview": text[:2000],
                "text_length": len(text),
                "import_method": "manual_pdf",
            },
        )
        is_new = await store.upsert_raw(raw_item)

        summary = text[:500].replace("\n", " ").strip()
        if summary:
            await store.update_classification(
                raw_item.item_id,
                kind="paper",
                confidence=0.9,
                summary=summary,
            )

        results.append({
            "file": filename,
            "ok": True,
            "is_new": is_new,
            "item_id": raw_item.item_id,
            "title": title,
            "text_length": len(text),
        })
        imported += 1

    return {
        "ok": True,
        "imported": imported,
        "errors": errors,
        "total": len(body.file_paths),
        "results": results,
    }


# ── Scheduler runtime control ─────────────────────────────────────


@router.get("/scheduler/status")
async def scheduler_status() -> dict[str, Any]:
    """Snapshot of whether the auto-start scheduler is running + persisted on/off."""
    return {
        "running": _scheduler.is_running(),
        "enabled": _scheduler._enabled(),  # noqa: SLF001
        "interval_seconds": _scheduler._interval_seconds(),  # noqa: SLF001
    }


@router.post("/scheduler/start")
async def scheduler_start() -> dict[str, Any]:
    """Persist auto-start=on AND start the in-process task immediately."""
    started = await _scheduler.enable_at_runtime()
    return {
        "running": _scheduler.is_running(),
        "newly_started": started,
        "interval_seconds": _scheduler._interval_seconds(),  # noqa: SLF001
    }


@router.post("/scheduler/stop")
async def scheduler_stop() -> dict[str, Any]:
    """Persist auto-start=off AND cancel the running task."""
    stopped = await _scheduler.disable_at_runtime()
    return {"running": _scheduler.is_running(), "stopped": stopped}


__all__ = ["router"]
