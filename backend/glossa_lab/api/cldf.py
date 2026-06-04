"""CLDF data API — read-only access to JAMBU DEDR wordlist data.

No database dependency; all data is loaded from CSV via
:mod:`glossa_lab.data.cldf_loader`.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Query

from glossa_lab.data.cldf_loader import (
    get_cldf_summary,
    get_forms_by_language,
    get_forms_by_parameter,
    load_forms,
    load_languages,
    load_parameters,
)

_log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/cldf", tags=["cldf"])


@router.get("/summary")
def cldf_summary() -> dict:
    """High-level counts and family distribution."""
    try:
        return get_cldf_summary()
    except Exception:
        _log.warning("CLDF summary failed", exc_info=True)
        return {"n_forms": 0, "n_languages": 0, "n_parameters": 0, "families": {}}


@router.get("/forms")
def cldf_forms(
    language_id: Optional[str] = Query(None),
    parameter_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=5000),
    offset: int = Query(0, ge=0),
) -> dict:
    """Paginated form list with optional filters."""
    try:
        forms = load_forms()
    except Exception:
        _log.warning("CLDF forms load failed", exc_info=True)
        return {"items": [], "total": 0, "limit": limit, "offset": offset}

    if language_id:
        forms = [f for f in forms if f.get("language_id") == language_id]
    if parameter_id:
        forms = [f for f in forms if f.get("parameter_id") == parameter_id]
    if search:
        s = search.lower()
        forms = [
            f for f in forms
            if s in (f.get("form") or "").lower()
            or s in (f.get("gloss") or "").lower()
        ]

    total = len(forms)
    return {
        "items": forms[offset : offset + limit],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/languages")
def cldf_languages(
    family: Optional[str] = Query(None),
) -> list[dict]:
    """Language list, optionally filtered by family substring."""
    try:
        langs = load_languages()
    except Exception:
        _log.warning("CLDF languages load failed", exc_info=True)
        return []

    if family:
        fam_lower = family.lower()
        langs = [l for l in langs if fam_lower in (l.get("family") or "").lower()]
    return langs


@router.get("/cognate-set/{parameter_id}")
def cldf_cognate_set(parameter_id: str) -> dict:
    """All forms for a given parameter_id (cognate set)."""
    try:
        params = load_parameters()
    except Exception:
        _log.warning("CLDF parameters load failed", exc_info=True)
        params = []

    headword = ""
    for p in params:
        if p.get("parameter_id") == parameter_id:
            headword = p.get("name", "")
            break

    try:
        forms = get_forms_by_parameter(parameter_id)
    except Exception:
        _log.warning("CLDF cognate-set forms load failed", exc_info=True)
        forms = []

    return {
        "parameter_id": parameter_id,
        "headword": headword,
        "forms": forms,
    }
