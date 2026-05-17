"""Indus Evidence Graph API.

Mounted at ``/api/v1/indus-evidence``.

Endpoints
---------
GET  /library                   List registered literature documents
GET  /claims                    List extracted claims (with filters)
GET  /hypotheses                List hypothesis model summaries

POST /upload                    Upload a PDF → run intake
POST /import-url                Import a paper from a URL → run intake
POST /intake/run                Re-run claims extraction pipeline on all registered docs

GET  /sweep/config              Read project sweep.yaml
PUT  /sweep/config              Save project sweep.yaml
POST /sweep/run                 Run sweep using sweep.yaml → background job
GET  /sweep/candidates          Read latest sweep candidates file
POST /sweep/intake              Intake a single sweep candidate (by URL / doi / title)

All filesystem operations target the ``glossa-indus/`` directory which lives two
levels above this file's package root (alongside ``backend/``).
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

_log = logging.getLogger("glossa_lab.api.indus_evidence")
router = APIRouter(prefix="/api/v1/indus-evidence", tags=["indus-evidence"])

# ── Path constants ────────────────────────────────────────────────────────────

_REPO_ROOT    = Path(__file__).resolve().parent.parent.parent.parent
_EVIDENCE_BASE = _REPO_ROOT / "glossa-indus"
_LIT_DOCS     = _EVIDENCE_BASE / "literature" / "documents"
_CLAIMS_DIR   = _EVIDENCE_BASE / "claims" / "extracted_claims"
_HYPO_MODELS  = _EVIDENCE_BASE / "hypotheses" / "models"
_SWEEP_CFG    = _EVIDENCE_BASE / "config" / "sweep.yaml"
_SWEEP_CANDS  = _EVIDENCE_BASE / "logs" / "sweep_candidates_latest.json"
_RAW_UPLOADS  = _EVIDENCE_BASE / "raw" / "user_uploads"
_SCRIPTS      = _EVIDENCE_BASE / "scripts"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── YAML helper (stdlib-only fallback, optional PyYAML) ───────────────────────

def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file. Falls back to a minimal line-parser if PyYAML is absent."""
    try:
        import yaml  # noqa: PLC0415
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Minimal fallback: parse only simple key: value lines
        data: dict = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and ":" in stripped:
                    k, _, v = stripped.partition(":")
                    data[k.strip()] = v.strip()
        return data


def _dump_yaml(data: dict[str, Any], path: Path) -> None:
    try:
        import yaml  # noqa: PLC0415
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    except ImportError:
        # Minimal fallback: write as JSON inside a YAML comment block
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# Auto-saved by Glossa-Lab (PyYAML not installed — JSON fallback)\n"
            + json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


# ── Library ───────────────────────────────────────────────────────────────────

@router.get("/library")
async def list_library(
    q: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List all registered literature documents."""
    _LIT_DOCS.mkdir(parents=True, exist_ok=True)
    docs: list[dict[str, Any]] = []
    for f in sorted(_LIT_DOCS.glob("*.json")):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        if q:
            haystack = (
                (d.get("detected_title") or "")
                + " "
                + " ".join(d.get("detected_authors") or [])
            ).lower()
            if q.lower() not in haystack:
                continue
        if status and d.get("processing_status") != status:
            continue

        # Attach claim count from extracted_claims if available
        claim_file = _CLAIMS_DIR / f"{d.get('document_id', f.stem)}.json"
        claim_count = 0
        if claim_file.exists():
            try:
                cd = json.loads(claim_file.read_text("utf-8"))
                claim_count = cd.get("total_claims", 0)
            except Exception:
                pass

        docs.append({
            "document_id":        d.get("document_id", f.stem),
            "title":              d.get("detected_title", ""),
            "authors":            d.get("detected_authors", []),
            "year":               d.get("detected_year"),
            "doi":                d.get("detected_doi"),
            "file_size_bytes":    d.get("file_size_bytes", 0),
            "access_type":        d.get("access_type", ""),
            "license_status":     d.get("license_status", ""),
            "processing_status":  d.get("processing_status", ""),
            "ocr_required":       d.get("ocr_required", False),
            "intake_date":        d.get("intake_date", ""),
            "claim_count":        claim_count,
            "claim_extraction_status": d.get("claim_extraction_status", ""),
        })

    total = len(docs)
    return {"documents": docs[offset: offset + limit], "total": total, "limit": limit, "offset": offset}


# ── Claims ────────────────────────────────────────────────────────────────────

@router.get("/claims")
async def list_claims(
    q: str | None = None,
    claim_type: str | None = None,
    claim_status: str | None = None,
    doc_id: str | None = None,
    sign: str | None = None,
    limit: int = 200,
    offset: int = 0,
) -> dict[str, Any]:
    """List all extracted claims across all registered documents."""
    _CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    all_claims: list[dict[str, Any]] = []
    for f in sorted(_CLAIMS_DIR.glob("*.json")):
        if doc_id and f.stem != doc_id:
            continue
        try:
            record = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        for claim in record.get("claims", []):
            if claim_type and claim.get("claim_type") != claim_type:
                continue
            if claim_status and claim.get("claim_status") != claim_status:
                continue
            if q and q.lower() not in (claim.get("normalized_claim") or "").lower():
                continue
            if sign:
                signs_involved = " ".join(claim.get("signs_involved") or [])
                if sign.lower() not in signs_involved.lower():
                    continue
            all_claims.append({
                **claim,
                "_source_file": f.stem,
            })

    total = len(all_claims)
    return {
        "claims": all_claims[offset: offset + limit],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


# ── Hypotheses ────────────────────────────────────────────────────────────────

@router.get("/hypotheses")
async def list_hypotheses() -> dict[str, Any]:
    """List hypothesis model summaries from YAML files."""
    _HYPO_MODELS.mkdir(parents=True, exist_ok=True)
    models: list[dict[str, Any]] = []
    for f in sorted(_HYPO_MODELS.glob("*.yaml")):
        try:
            d = _load_yaml(f)
        except Exception:
            d = {}
        models.append({
            "file": f.name,
            "model_id":   d.get("model_id", f.stem),
            "model_name": d.get("model_name", ""),
            "status":     d.get("status", ""),
            "model_type": d.get("model_type", ""),
            "n_claims":   len(d.get("core_claims") or []),
            "n_tests":    len(d.get("tests_planned") or []),
        })
    return {"models": models}


# ── Upload PDF ────────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_paper(
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Upload a PDF and queue it for intake."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / file.filename
    content = await file.read()
    dest.write_bytes(content)
    _log.info("uploaded: %s (%d bytes)", dest.name, len(content))

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "uploaded",
        "filename": file.filename,
        "size_bytes": len(content),
        "message": "Intake queued — document will be processed in the background.",
    }


def _run_intake_on_file(file_path: str) -> None:
    import subprocess  # noqa: PLC0415
    intake_script = _SCRIPTS / "indus_intake.py"
    try:
        subprocess.run(
            [sys.executable, str(intake_script), "--file", file_path],
            capture_output=True, text=True, timeout=120,
        )
    except Exception as exc:
        _log.warning("intake failed for %s: %s", file_path, exc)


# ── Import from URL ───────────────────────────────────────────────────────────

class ImportUrlBody(BaseModel):
    url: str
    title: str = ""
    doi: str = ""
    authors: list[str] = []
    year: int | None = None


@router.post("/import-url")
async def import_url(body: ImportUrlBody, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Download a PDF from a URL and queue it for intake."""
    url = body.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")

    # Derive a safe filename from the URL
    parsed  = urllib.parse.urlparse(url)
    fname   = Path(parsed.path).name or "paper.pdf"
    if not fname.lower().endswith(".pdf"):
        fname += ".pdf"
    # Sanitize
    fname = re.sub(r"[^A-Za-z0-9._\-]", "_", fname)[:120]

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / fname

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            content = resp.read()
        dest.write_bytes(content)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to download: {exc}") from exc

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "downloaded",
        "filename": fname,
        "size_bytes": len(content),
        "source_url": url,
        "message": "Download complete — intake queued.",
    }


# ── Intake pipeline runner ────────────────────────────────────────────────────

@router.post("/intake/run")
async def run_intake_pipeline(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Re-run indus_intake.py (scan) + indus_claims.py on all registered docs."""
    background_tasks.add_task(_run_full_intake)
    return {"status": "queued", "message": "Full intake + claim extraction pipeline queued."}


def _run_full_intake() -> None:
    import subprocess  # noqa: PLC0415
    intake = _SCRIPTS / "indus_intake.py"
    claims = _SCRIPTS / "indus_claims.py"
    for script in (intake, claims):
        if not script.exists():
            continue
        try:
            args = [sys.executable, str(script)]
            if script.name == "indus_intake.py":
                args += ["--scan", str(_RAW_UPLOADS)]
            subprocess.run(args, capture_output=True, text=True, timeout=300)
        except Exception as exc:
            _log.warning("pipeline script %s failed: %s", script.name, exc)


# ── Sweep: read / write config ────────────────────────────────────────────────

@router.get("/sweep/config")
async def get_sweep_config() -> dict[str, Any]:
    """Read the project sweep.yaml configuration."""
    if not _SWEEP_CFG.exists():
        raise HTTPException(status_code=404, detail="sweep.yaml not found — create it via PUT /sweep/config")
    try:
        return _load_yaml(_SWEEP_CFG)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not parse sweep.yaml: {exc}") from exc


class SweepConfigBody(BaseModel):
    schema_version: str = "1.0"
    sweep: dict[str, Any] = {}


@router.put("/sweep/config")
async def save_sweep_config(body: SweepConfigBody) -> dict[str, Any]:
    """Save a new sweep.yaml configuration."""
    try:
        _dump_yaml(body.model_dump(), _SWEEP_CFG)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not write sweep.yaml: {exc}") from exc
    return {"status": "saved", "path": str(_SWEEP_CFG)}


# ── Sweep: run ────────────────────────────────────────────────────────────────

@router.post("/sweep/run")
async def run_sweep(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Run the sweep in the background using sweep.yaml. Returns a job ack."""
    if not _SWEEP_CFG.exists():
        raise HTTPException(status_code=404, detail="sweep.yaml not found — configure it first")

    background_tasks.add_task(_bg_sweep)
    return {
        "status": "running",
        "message": "Sweep started in background. Poll GET /sweep/candidates for results.",
    }


async def _bg_sweep() -> None:
    """Background task: build a TopicProfile from sweep.yaml and run the fetchers."""
    try:
        cfg = _load_yaml(_SWEEP_CFG)
        sweep = cfg.get("sweep", {})

        from glossa_lab.discovery.fetchers.base import TopicProfile  # noqa: PLC0415
        from glossa_lab.discovery.fetchers import _build_fetchers, to_iso, now_utc  # noqa: PLC0415
        from glossa_lab.discovery import store  # noqa: PLC0415

        # Flatten keywords into one list for TopicProfile
        kw_block = sweep.get("keywords", {})
        all_kws: list[str] = (
            list(kw_block.get("primary", []))
            + list(kw_block.get("secondary", []))
        )
        # Only add expansions if total is still < 30
        if len(all_kws) < 30:
            all_kws += list(kw_block.get("expansions", []))

        source_overrides: dict[str, dict] = {}
        sources_cfg = sweep.get("sources", {})
        for src, opts in sources_cfg.items():
            if not isinstance(opts, dict) or not opts.get("enabled", True):
                continue
            ovr: dict = {}
            mr = opts.get("max_results")
            if mr:
                ovr["per_page"] = mr
                ovr["max_results"] = mr
                ovr["rows"] = mr
            cats = opts.get("categories")
            if cats:
                ovr["search_query_extra"] = " OR ".join(f"cat:{c}" for c in cats)
            if ovr:
                source_overrides[src] = ovr

        profile = TopicProfile(
            id="evidence_sweep",
            label=sweep.get("name", "Evidence Sweep"),
            description=sweep.get("description", ""),
            keywords=all_kws,
            exclusions=list(sweep.get("exclusions", [])),
            languages=list((sweep.get("filters") or {}).get("languages") or ["en"]),
            source_overrides=source_overrides,
        )

        # Only enabled sources
        enabled_sources = [
            src for src, opts in sources_cfg.items()
            if isinstance(opts, dict) and opts.get("enabled", True)
        ]

        fetchers = _build_fetchers(enabled_sources if enabled_sources else None)
        fetched_at = to_iso(now_utc())
        raw_items: list[dict[str, Any]] = []

        async def _one(f) -> None:
            try:
                items = list(await f.fetch(profile))
                for item in items:
                    raw_items.append({
                        "source":        f.source,
                        "title":         item.title or "",
                        "url":           item.url or "",
                        "doi":           item.doi or "",
                        "authors":       list(item.authors or []),
                        "published_at":  item.published_at or "",
                        "summary":       (item.summary or "")[:400],
                        "pdf_url":       item.pdf_url or "",
                        "open_access":   bool(item.pdf_url),
                        "kind":          item.kind or "study",
                        "fetched_at":    fetched_at,
                    })
            except Exception as exc:  # noqa: BLE001
                _log.warning("sweep fetcher %s: %s", f.source, exc)

        # Split into parallel and sequential (rate-limited)
        parallel   = [f for f in fetchers if getattr(f, "rate_delay", 0) <= 0]
        sequential = [f for f in fetchers if getattr(f, "rate_delay", 0) > 0]
        await asyncio.gather(*[_one(f) for f in parallel])
        for f in sequential:
            await _one(f)

        # De-duplicate by normalized title + doi
        seen: set[str] = set()
        unique_items: list[dict] = []
        for it in raw_items:
            key = _normalize_title(it["title"]) or it["doi"] or it["url"]
            if key and key not in seen:
                seen.add(key)
                unique_items.append(it)

        # Filter against already-registered papers
        registered_keys = _registered_paper_keys()
        candidates = [
            it for it in unique_items
            if not _is_registered(it, registered_keys)
        ]

        # Apply max_candidates cap
        max_cands = int((sweep.get("output") or {}).get("max_candidates", 200))
        candidates = candidates[:max_cands]

        # Save to log
        _SWEEP_CANDS.parent.mkdir(parents=True, exist_ok=True)
        _SWEEP_CANDS.write_text(
            json.dumps({
                "sweep_date": _now_iso(),
                "total_fetched": len(raw_items),
                "total_unique": len(unique_items),
                "total_new":    len(candidates),
                "candidates":   candidates,
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        _log.info(
            "sweep complete: fetched=%d unique=%d new=%d",
            len(raw_items), len(unique_items), len(candidates),
        )
    except Exception as exc:  # noqa: BLE001
        _log.error("sweep background task failed: %s", exc)
        _SWEEP_CANDS.parent.mkdir(parents=True, exist_ok=True)
        _SWEEP_CANDS.write_text(
            json.dumps({"sweep_date": _now_iso(), "error": str(exc), "candidates": []}),
            encoding="utf-8",
        )


def _normalize_title(t: str) -> str:
    return re.sub(r"\W+", " ", (t or "").lower()).strip()[:120]


def _registered_paper_keys() -> set[str]:
    keys: set[str] = set()
    if not _LIT_DOCS.exists():
        return keys
    for f in _LIT_DOCS.glob("*.json"):
        try:
            d = json.loads(f.read_text("utf-8"))
            if d.get("detected_title"):
                keys.add(_normalize_title(d["detected_title"]))
            if d.get("detected_doi"):
                keys.add(str(d["detected_doi"]).lower().strip())
        except Exception:
            pass
    return keys


def _is_registered(item: dict[str, Any], registered_keys: set[str]) -> bool:
    title_key = _normalize_title(item.get("title", ""))
    doi_key   = str(item.get("doi", "") or "").lower().strip()
    return bool(
        (title_key and title_key in registered_keys)
        or (doi_key and doi_key in registered_keys)
    )


# ── Sweep: get candidates ─────────────────────────────────────────────────────

@router.get("/sweep/candidates")
async def get_sweep_candidates() -> dict[str, Any]:
    """Return the latest sweep candidate list."""
    if not _SWEEP_CANDS.exists():
        return {"candidates": [], "total_new": 0, "sweep_date": None}
    try:
        return json.loads(_SWEEP_CANDS.read_text("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not read candidates: {exc}") from exc


# ── Sweep: intake a candidate ─────────────────────────────────────────────────

class IntakeCandidateBody(BaseModel):
    url: str = ""
    pdf_url: str = ""
    title: str = ""
    doi: str = ""
    authors: list[str] = []
    year: int | None = None
    source: str = ""


@router.post("/sweep/intake")
async def intake_sweep_candidate(
    body: IntakeCandidateBody,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Download a sweep candidate and queue it for intake."""
    target_url = body.pdf_url or body.url
    if not target_url:
        raise HTTPException(status_code=400, detail="url or pdf_url required")

    # Generate filename from title or URL
    if body.title:
        fname = re.sub(r"[^A-Za-z0-9_\-]", "_", body.title[:60]) + ".pdf"
    else:
        parsed = urllib.parse.urlparse(target_url)
        fname  = Path(parsed.path).name or "paper.pdf"
        if not fname.lower().endswith(".pdf"):
            fname += ".pdf"
    fname = re.sub(r"_+", "_", fname).strip("_")

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / fname

    # If the target doesn't look like a direct PDF, just register the URL
    if not (target_url.endswith(".pdf") or "pdf" in target_url.lower()):
        # Write a placeholder JSON stub the user can replace with a manual upload
        stub = {
            "source_url": target_url,
            "title": body.title,
            "doi": body.doi,
            "authors": body.authors,
            "year": body.year,
            "note": "Non-PDF URL — please upload the PDF manually to raw/user_uploads/",
        }
        stub_path = _EVIDENCE_BASE / "logs" / "pending_imports.jsonl"
        stub_path.parent.mkdir(parents=True, exist_ok=True)
        with open(stub_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(stub, ensure_ascii=False) + "\n")
        return {
            "status": "pending_manual",
            "message": "URL is not a direct PDF. Logged to logs/pending_imports.jsonl — upload manually.",
            "url": target_url,
        }

    try:
        req = urllib.request.Request(target_url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            content = resp.read()
        dest.write_bytes(content)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Download failed: {exc}") from exc

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "downloaded",
        "filename": fname,
        "size_bytes": len(content),
        "message": "Downloaded and intake queued.",
    }
