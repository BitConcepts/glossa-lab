"""Reports API backed by the repository reports directory.

Includes:
  GET  /reports                     -- list all reports
  GET  /reports/{name}              -- get one report (JSON)
  GET  /reports/{name}/download     -- download raw file
  POST /reports/{name}/open-folder  -- open folder in OS file manager
  DELETE /reports/{name}            -- delete a report
  GET  /reports/templates           -- list available PDF report templates
  POST /reports/generate            -- generate a PDF report from a template
"""
from __future__ import annotations

import asyncio
import json
import logging
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from glossa_lab.catalog import list_report_catalog

router = APIRouter()
logger = logging.getLogger("glossa_lab.api.reports")

_REPO_ROOT    = Path(__file__).resolve().parent.parent.parent.parent
_BACKEND_DIR  = _REPO_ROOT / "backend"
_REPORTS_DIR  = _REPO_ROOT / "reports"
_ALIASES      = {"indus": "real_indus_catalog_analysis.json"}


# ── Report template registry ──────────────────────────────────────────────────

# Each template defines a PDF report generator that reads from reports/
# and produces a PDF. These are selectable from the UI via the Generate Report modal.

_REPORT_TEMPLATES: dict[str, dict[str, Any]] = {
    "fuls_nw_semitic": {
        "id":          "fuls_nw_semitic",
        "name":        "Fuls NW Semitic Analysis Report",
        "description": (
            "Comprehensive PDF report for the Dr. Fuls NW Semitic test1 collaboration. "
            "Reads the latest fuls_rtl_corrected, fuls_nw_semitic_benchmark, "
            "fuls_writing_system_comparison, and fuls_constraint_space JSON results."
        ),
        "script":      "generate_fuls_nw_semitic_report.py",
        "output_glob": "fuls_nw_semitic_report*.pdf",
        "requires":    ["fuls_rtl_corrected*.json"],
        "category":    "Fuls Collaboration",
    },
    "geez_benchmark": {
        "id":          "geez_benchmark",
        "name":        "Geez Syllabic Anchor-Convergence Report",
        "description": (
            "Technical PDF report for the Geez anchor-convergence validation experiment. "
            "Reads the latest geez_syllabic_anchor_convergence JSON result. "
            "Includes anchor convergence curve, comparison with NW Semitic, and Dr. Fuls summary."
        ),
        "script":      "generate_geez_report.py",
        "output_glob": "geez_syllabic_anchor_convergence_report*.pdf",
        "requires":    ["geez_syllabic_anchor_convergence*.json"],
        "category":    "Fuls Collaboration",
    },
    "ugaritic_decipherment": {
        "id":          "ugaritic_decipherment",
        "name":        "Ugaritic Decipherment Report",
        "description": "PDF report for the Ugaritic anti-circularity and beam decipherment benchmarks.",
        "script":      "generate_decipherment_report.py",
        "output_glob": "decipherment_report*.pdf",
        "requires":    [],
        "category":    "Validation",
    },
    "linear_a": {
        "id":          "linear_a",
        "name":        "Linear A Anti-Circularity Report",
        "description": "PDF report for the Linear A phoneme hypothesis anti-circularity suite.",
        "script":      "generate_report_linear_a_circularity.py",
        "output_glob": "linear_a_circularity_report*.pdf",
        "requires":    [],
        "category":    "Validation",
    },
    "linear_b": {
        "id":          "linear_b",
        "name":        "Linear B / Ventris Grid Report",
        "description": "PDF report for the Ventris grid validation and Linear B beam decipherment.",
        "script":      "generate_report_linear_b.py",
        "output_glob": "linear_b_report*.pdf",
        "requires":    [],
        "category":    "Validation",
    },
}


@router.get("/reports/templates")
async def list_report_templates() -> list[dict[str, Any]]:
    """Return available PDF report templates."""
    return [
        {
            "id":          t["id"],
            "name":        t["name"],
            "description": t["description"],
            "category":    t["category"],
            "requires":    t["requires"],
            "ready":       all(
                bool(list(_REPORTS_DIR.glob(req)))
                for req in t["requires"]
            ),
        }
        for t in _REPORT_TEMPLATES.values()
    ]


class GenerateReportBody(BaseModel):
    template_id: str


@router.post("/reports/generate")
async def generate_report(body: GenerateReportBody) -> dict[str, Any]:
    """Generate a PDF report from a registered template.

    Runs the corresponding generate_*.py script as a background job.
    The job appears in the Jobs panel with progress updates.
    Returns immediately with a job_id; poll GET /jobs/{id} for completion.
    """
    tmpl = _REPORT_TEMPLATES.get(body.template_id)
    if tmpl is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown template '{body.template_id}'. "
                   f"Valid: {list(_REPORT_TEMPLATES)}"
        )

    script_path = _BACKEND_DIR / tmpl["script"]
    if not script_path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Report generator script not found: {tmpl['script']}"
        )

    # Check that required input JSON files exist
    missing = [
        req for req in tmpl["requires"]
        if not list(_REPORTS_DIR.glob(req))
    ]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Cannot generate report: missing required result files: {missing}. "
                f"Run the corresponding experiment first, then generate the report."
            )
        )

    # Create a Job record so the run appears in the Jobs panel
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    job_id: str | None = None
    if db:
        try:
            job = await db.create_job(
                name=f"Generate Report: {tmpl['name']}",
                pipeline="report_generator",
                params={
                    "template_id": body.template_id,
                    "script":      tmpl["script"],
                    "source":      "ui",
                },
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            job_id = job["id"]
            await db.update_job_status(job_id, "running")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not create job record: %s", exc)

    # Run the generator in a background thread (non-blocking)
    loop = asyncio.get_event_loop()

    async def _run_generator() -> None:
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, str(script_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(_BACKEND_DIR),
            )
            stdout, _ = await proc.communicate()
            output = stdout.decode("utf-8", errors="replace") if stdout else ""
            if proc.returncode == 0:
                logger.info("Report generated: %s\n%s", tmpl["name"], output[-500:])
                if job_id and db:
                    await db.update_job_status(job_id, "completed")
            else:
                logger.error("Report generation failed (rc=%d): %s", proc.returncode, output[-500:])
                if job_id and db:
                    await db.update_job_status(job_id, "failed")
        except Exception as exc:  # noqa: BLE001
            logger.error("Report generation exception: %s", exc)
            if job_id and db:
                try:
                    await db.update_job_status(job_id, "failed")
                except Exception:  # noqa: BLE001
                    pass

    asyncio.create_task(_run_generator())

    return {
        "started":     True,
        "job_id":      job_id,
        "template_id": body.template_id,
        "template_name": tmpl["name"],
        "script":      tmpl["script"],
        "message":     (
            f"Generating '{tmpl['name']}'. "
            f"The report will appear in the Reports list when complete. "
            f"Job ID: {job_id}"
        ),
    }


@router.get("/reports")
async def list_reports() -> list[dict[str, Any]]:
    return list_report_catalog()


@router.get("/reports/{report_name}")
async def get_report(report_name: str) -> dict[str, Any]:
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "name": path.name,
        "relative_path": path.relative_to(_REPO_ROOT).as_posix(),
        "content": path.read_text(encoding="utf-8"),
    }


@router.get("/reports/{report_name}/download")
async def download_report(report_name: str) -> FileResponse:
    """Serve the raw file for direct download or inline browser viewing."""
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    suffix = path.suffix.lower()
    media_types = {
        ".pdf": "application/pdf",
        ".json": "application/json",
        ".csv": "text/csv",
        ".md": "text/markdown",
        ".txt": "text/plain",
    }
    media_type = media_types.get(suffix, "application/octet-stream")
    return FileResponse(
        path=str(path),
        media_type=media_type,
        filename=path.name,
        headers={"Content-Disposition": f'inline; filename="{path.name}"'},
    )


@router.post("/reports/{report_name}/open-folder")
async def open_report_folder(report_name: str) -> dict[str, Any]:
    """Open the folder containing the report in the OS file manager."""
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    folder = str(path.parent)
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["explorer", folder])
        elif system == "Darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"opened": True, "folder": folder}


@router.delete("/reports/{report_name}")
async def delete_report(report_name: str) -> dict[str, Any]:
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    relative_path = path.relative_to(_REPO_ROOT).as_posix()
    path.unlink()
    return {"deleted": True, "relative_path": relative_path}


def _resolve(report_name: str) -> Path | None:
    name = _ALIASES.get(report_name, report_name)
    for path in _REPORTS_DIR.rglob("*"):
        if path.is_file() and (path.name == name or path.stem == name):
            return path
    return None
