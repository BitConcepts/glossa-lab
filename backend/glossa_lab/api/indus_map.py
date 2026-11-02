"""Indus layered-map API (Spec 086 Stage 5, T503).

Mounted at ``/api/v1/indus-map``. Serves the published,
gate-verified map artifact (``glossa-indus/map/map-data.json``)
exactly as published: the surface renders the gated artifact
(C086-17) — no recomputation here, no hand-tuned counts, no
client-side drift. The only value computed at serve time is the
stale flag (C086-18): whether the artifact's as-of ledger hash
still matches the ledger's current hash.

Scoping (C086-19): the map belongs to the primary workspace
(indus-script). ``cloud_scope`` resolves the indus-map resource
to that workspace, so a cloud actor without an indus-script
role receives the scoped 404, and a response never contains an
element outside the actor's scope.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from glossa_lab import ledger_intake as li

router = APIRouter(prefix="/api/v1/indus-map", tags=["indus-map"])

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MAP_PATH = _REPO_ROOT / "glossa-indus" / "map" / "map-data.json"
_LEDGER_PATH = _REPO_ROOT / li.LEDGER_REL

_cache: dict[str, Any] = {"key": None, "data": None}


def _load_artifact() -> dict[str, Any]:
    if not _MAP_PATH.is_file():
        raise HTTPException(
            status_code=404, detail="map artifact is not published"
        )
    stat = _MAP_PATH.stat()
    key = (stat.st_mtime_ns, stat.st_size)
    if _cache["key"] != key:
        _cache["data"] = json.loads(_MAP_PATH.read_text(encoding="utf-8"))
        _cache["key"] = key
    return _cache["data"]


def _stamp(artifact: dict[str, Any]) -> dict[str, Any]:
    as_of = artifact["header"]["as_of"]
    stale = True
    if _LEDGER_PATH.is_file():
        stale = li.sha256_file(_LEDGER_PATH) != as_of["ledger_sha256"]
    return {
        "map": "glossa-indus/map/map-data.json",
        "map_sha256": hashlib.sha256(_MAP_PATH.read_bytes()).hexdigest(),
        "map_defs": as_of["map_defs"],
        "generated_by": artifact["generated_by"],
        "as_of": as_of,
        "stale": stale,
    }


def _envelope(artifact: dict[str, Any], **sections: Any) -> dict[str, Any]:
    return {
        "header": artifact["header"],
        "stamp": _stamp(artifact),
        **sections,
    }


@router.get("/header")
def get_header() -> dict[str, Any]:
    artifact = _load_artifact()
    return _envelope(artifact)


@router.get("/system")
def get_system() -> dict[str, Any]:
    artifact = _load_artifact()
    return _envelope(artifact, system=artifact["system"])


@router.get("/matrix")
def get_matrix() -> dict[str, Any]:
    artifact = _load_artifact()
    return _envelope(artifact, matrix=artifact["matrix"])


@router.get("/settling")
def get_settling() -> dict[str, Any]:
    artifact = _load_artifact()
    return _envelope(artifact, settling=artifact["settling"])


@router.get("/claims/{claim_id}")
def get_claim(claim_id: str) -> dict[str, Any]:
    artifact = _load_artifact()
    record = artifact["claims"].get(claim_id)
    if record is None:
        raise HTTPException(status_code=404, detail="claim not in the map")
    return _envelope(artifact, claim=record)


@router.get("/claims/{claim_id}/evidence")
def get_claim_evidence(claim_id: str) -> dict[str, Any]:
    artifact = _load_artifact()
    record = artifact["claims"].get(claim_id)
    if record is None:
        raise HTTPException(status_code=404, detail="claim not in the map")
    return _envelope(artifact, evidence=record["evidence"])
