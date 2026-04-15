"""User-definable Report Templates API.

All templates are stored in the database (not hardcoded in Python).
Users create templates from the Reports & Data UI, defining sections,
data sources, and chart types.  No Python file required to add a template.

Endpoints:
  GET    /report-templates               -- list all templates
  POST   /report-templates               -- create a new template
  GET    /report-templates/{id}          -- get one template
  PUT    /report-templates/{id}          -- update template
  DELETE /report-templates/{id}          -- delete template
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Schema ────────────────────────────────────────────────────────────────────

class SectionDef(BaseModel):
    """One section in a report template."""
    title: str = ""
    data_source: str = ""    # experiment ID or "upstream" for node-piped data
    data_key: str = ""       # key within the data_source JSON
    chart_type: str = "table"  # table | bar | line | text
    include_table: bool = True
    description: str = ""


class ReportTemplateCreate(BaseModel):
    name: str
    description: str = ""
    category: str = "General"
    sections: list[SectionDef] = []


class ReportTemplateUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    sections: list[SectionDef] | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/report-templates")
async def list_templates() -> list[dict[str, Any]]:
    """List all user-defined report templates."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return []
    return await db.list_report_templates()


@router.post("/report-templates", status_code=201)
async def create_template(body: ReportTemplateCreate) -> dict[str, Any]:
    """Create a new user-defined report template."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_report_template(
        name=body.name,
        description=body.description,
        category=body.category,
        sections=[s.model_dump() for s in body.sections],
        created_at=_now(),
    )


@router.get("/report-templates/{template_id}")
async def get_template(template_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    t = await db.get_report_template(template_id)
    if t is None:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return t


@router.put("/report-templates/{template_id}")
async def update_template(template_id: str, body: ReportTemplateUpdate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    fields: dict[str, Any] = {}
    if body.name is not None:        fields["name"] = body.name
    if body.description is not None: fields["description"] = body.description
    if body.category is not None:    fields["category"] = body.category
    if body.sections is not None:    fields["sections"] = [s.model_dump() for s in body.sections]
    result = await db.update_report_template(template_id, **fields)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return result


@router.delete("/report-templates/{template_id}")
async def delete_template(template_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.delete_report_template(template_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return {"deleted": True, "id": template_id}
