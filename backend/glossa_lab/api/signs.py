"""Signs API — unified sign index with anchored cross-references.

Data sources (merged on startup):
  1. ``INDUS_FINAL_ANCHORS.json`` — the authoritative anchor file
  2. ``anchor_sets`` DB table    — user-created named anchor sets
  3. ``anchor_staging.json`` / ``anchor_staging_archive.json`` — staging pipeline

Endpoints (mounted at ``/api/v1/signs``):
  GET  /signs          — paginated, filterable sign list
  GET  /signs/summary  — aggregate counts
  GET  /signs/{sign_id} — full detail for one sign
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/v1/signs", tags=["signs"])
_log = logging.getLogger("glossa_lab.api.signs")

# ── In-memory sign index ──────────────────────────────────────────────────
# Built lazily on first request from all available sources.

_SIGNS_INDEX: dict[str, dict[str, Any]] = {}
_INDEX_BUILT = False

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
_REPORTS_DIR = _BACKEND_DIR / "reports"
_OUTPUTS_DIR = _BACKEND_DIR / "outputs"
_STATIC_SIGNS_DIR = _BACKEND_DIR / "static" / "signs"


def _parse_phase(source_exp: str) -> int | None:
    """Extract phase number from an experiment id like 'indus_anchored_sa_dravidian_p257'."""
    m = re.search(r"[_pP](\d+)", source_exp or "")
    return int(m.group(1)) if m else None


def _build_sign_entry(
    sign_id: str,
    reading: str,
    confidence: str,
    *,
    basis: str = "",
    source_experiment: str = "",
    evidence_score: float = 0.0,
    evidence_type: str = "",
    dedr: str = "",
    dedr_source: str = "",
    phase_upgraded: int | None = None,
    corpus_freq: int = 0,
    in_corpus: bool = True,
    wells_ids: list[str] | None = None,
    mahadevan_ids: list[str] | None = None,
    numbering_system: str = "wells",
    gloss: str = "",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    phase = phase_upgraded or _parse_phase(source_experiment)
    _img_path = _STATIC_SIGNS_DIR / f"{sign_id}.png"
    return {
        "sign_id": sign_id,
        "reading": reading,
        "confidence": confidence.upper(),
        "image_url": f"/static/signs/{sign_id}.png" if _img_path.exists() else None,
        "in_corpus": in_corpus,
        "corpus_freq": corpus_freq,
        "evidence_type": evidence_type,
        "evidence_score": evidence_score,
        "basis": basis,
        "gloss": gloss,
        "source": {
            "experiment": source_experiment,
            "phase": phase,
            "job_id": None,
            "report_ref": f"Phase {phase} Anchored SA" if phase else "",
            "staging_entry": None,
            "dedr_ref": f"DEDR {dedr}" if dedr else "",
            "dedr_source": dedr_source,
        },
        "wells_ids": wells_ids or [],
        "mahadevan_ids": mahadevan_ids or [],
        "numbering_system": numbering_system,
        **(extra or {}),
    }


def _load_final_anchors() -> None:
    """Load INDUS_FINAL_ANCHORS.json into the index."""
    path = _REPORTS_DIR / "INDUS_FINAL_ANCHORS.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        anchors = data.get("anchors") or {}
        for sid, info in anchors.items():
            reading = info.get("reading", "")
            confidence = (info.get("confidence") or "LOW").upper()
            source = info.get("source", "")
            dedr = info.get("dedr", "")
            dedr_source = info.get("dedr_source", "")
            phase_upgraded = info.get("phase_upgraded")
            gloss = info.get("gloss", "")
            basis = info.get("basis", "")

            entry = _build_sign_entry(
                sign_id=sid,
                reading=reading,
                confidence=confidence,
                basis=basis,
                source_experiment=source,
                dedr=str(dedr) if dedr else "",
                dedr_source=dedr_source,
                phase_upgraded=int(phase_upgraded) if phase_upgraded else None,
                gloss=gloss,
            )
            _SIGNS_INDEX[sid] = entry
        _log.info("Loaded %d signs from INDUS_FINAL_ANCHORS.json", len(anchors))
    except Exception:  # noqa: BLE001
        _log.warning("Failed to load INDUS_FINAL_ANCHORS.json", exc_info=True)


def _load_staging_files() -> None:
    """Load anchor_staging.json and anchor_staging_archive.json if present."""
    for fname in ("anchor_staging.json", "anchor_staging_archive.json"):
        path = _OUTPUTS_DIR / fname
        if not path.exists():
            continue
        try:
            items = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(items, list):
                continue
            count = 0
            for item in items:
                sid = item.get("sign") or item.get("sign_id", "")
                if not sid or sid in _SIGNS_INDEX:
                    continue
                status = (item.get("review_status") or "").lower()
                if status not in ("approved", "verified", "accepted"):
                    continue
                entry = _build_sign_entry(
                    sign_id=sid,
                    reading=item.get("proposed_reading", ""),
                    confidence=(item.get("confidence") or "LOW").upper(),
                    evidence_type=item.get("evidence_type", ""),
                    evidence_score=float(item.get("evidence_score", 0)),
                    source_experiment=item.get("source_experiment", ""),
                )
                entry["staging_source"] = fname
                _SIGNS_INDEX[sid] = entry
                count += 1
            if count:
                _log.info("Loaded %d signs from %s", count, fname)
        except Exception:  # noqa: BLE001
            _log.warning("Failed to load %s", fname, exc_info=True)


async def _load_anchor_sets() -> None:
    """Load pairs from the anchor_sets DB table."""
    try:
        from glossa_lab.database import get_db  # noqa: PLC0415

        db = get_db()
        if db is None:
            return
        sets = await db.list_anchor_sets()
        count = 0
        for aset in sets:
            pairs = aset.get("pairs")
            if isinstance(pairs, str):
                try:
                    pairs = json.loads(pairs)
                except Exception:  # noqa: BLE001
                    continue
            if not isinstance(pairs, list):
                continue
            for pair in pairs:
                cipher = pair.get("cipher", "")
                target = pair.get("target", "")
                if not cipher or cipher in _SIGNS_INDEX:
                    continue
                conf = (pair.get("confidence") or "medium").upper()
                entry = _build_sign_entry(
                    sign_id=cipher,
                    reading=target,
                    confidence=conf,
                    source_experiment=f"anchor_set:{aset.get('id', '')}",
                )
                entry["anchor_set_name"] = aset.get("name", "")
                _SIGNS_INDEX[cipher] = entry
                count += 1
        if count:
            _log.info("Loaded %d signs from anchor_sets table", count)
    except Exception:  # noqa: BLE001
        _log.warning("Failed to load anchor_sets", exc_info=True)


async def _ensure_index() -> None:
    """Build the index once on first access."""
    global _INDEX_BUILT  # noqa: PLW0603
    if _INDEX_BUILT:
        return
    _load_final_anchors()
    _load_staging_files()
    await _load_anchor_sets()
    _INDEX_BUILT = True
    _log.info("Signs index ready: %d total entries", len(_SIGNS_INDEX))


# ── Endpoints ─────────────────────────────────────────────────────────────


@router.get("/summary")
async def signs_summary() -> dict[str, Any]:
    """Aggregate counts: total, deciphered, undeciphered, by confidence, etc."""
    await _ensure_index()
    signs = list(_SIGNS_INDEX.values())
    total = len(signs)
    high = sum(1 for s in signs if s["confidence"] == "HIGH")
    medium = sum(1 for s in signs if s["confidence"] == "MEDIUM")
    low = sum(1 for s in signs if s["confidence"] == "LOW")
    in_corpus = sum(1 for s in signs if s.get("in_corpus"))
    deciphered = high + medium + low  # all with readings
    # ICIT reference: 713 known signs total
    icit_total = 713
    undeciphered = max(0, icit_total - deciphered)
    return {
        "total": total,
        "deciphered": deciphered,
        "undeciphered": undeciphered,
        "icit_total": icit_total,
        "high": high,
        "medium": medium,
        "low": low,
        "in_corpus": in_corpus,
    }


@router.get("")
async def list_signs(
    deciphered: bool | None = Query(None),
    confidence: str | None = Query(None),
    in_corpus: bool | None = Query(None),
    search: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> dict[str, Any]:
    """Paginated, filterable sign list."""
    await _ensure_index()
    results = list(_SIGNS_INDEX.values())

    # Filters
    if confidence and confidence.upper() != "ANY":
        conf_set = {c.strip().upper() for c in confidence.split(",")}
        results = [s for s in results if s["confidence"] in conf_set]

    if in_corpus is not None:
        results = [s for s in results if s.get("in_corpus") == in_corpus]

    if deciphered is not None:
        if deciphered:
            results = [s for s in results if s.get("reading")]
        else:
            results = [s for s in results if not s.get("reading")]

    if search:
        q = search.lower()
        results = [
            s for s in results
            if q in s["sign_id"].lower()
            or q in (s.get("reading") or "").lower()
            or q in (s.get("basis") or "").lower()
        ]

    # Sort by confidence rank then sign_id
    conf_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "UNCERTAIN": 3}
    results.sort(key=lambda s: (conf_rank.get(s["confidence"], 9), s["sign_id"]))

    total = len(results)
    page = results[offset: offset + limit]
    return {
        "items": page,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{sign_id}")
async def get_sign(sign_id: str) -> dict[str, Any]:
    """Full detail for one sign including cross-references."""
    await _ensure_index()
    entry = _SIGNS_INDEX.get(sign_id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Sign '{sign_id}' not found")
    return entry
