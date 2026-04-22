"""CGSA API — Canonical Sign Registry and Cluster Assignments (V12).

Endpoints:
  GET  /canonical-signs              -- list all canonical signs
  GET  /canonical-signs/{sign_id}    -- get one sign by sign_id or internal_id
  POST /canonical-signs/seed         -- seed registry from CGSA pipeline CSVs
  GET  /sign-clusters                -- list all cluster assignments
  GET  /sign-clusters/summary        -- cluster count, k value, sign count
  POST /sign-clusters/seed           -- seed clusters from CGSA pipeline JSON
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter()

_ROOT = Path(__file__).resolve().parents[4]  # glossa-lab/


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _db():
    from glossa_lab.database import get_db  # noqa: PLC0415
    return get_db()


# ── Canonical Signs ──────────────────────────────────────────────────────────

@router.get("/canonical-signs")
async def list_canonical_signs(
    in_corpus_only: bool = False,
    numbering_system: str | None = None,
) -> list[dict[str, Any]]:
    db = _db()
    if db is None:
        return []
    return await db.list_canonical_signs(
        in_corpus_only=in_corpus_only,
        numbering_system=numbering_system,
    )


@router.get("/canonical-signs/{sign_id}")
async def get_canonical_sign(sign_id: str) -> dict[str, Any]:
    db = _db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.get_canonical_sign(sign_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sign '{sign_id}' not found")
    return result


@router.post("/canonical-signs/seed", status_code=201)
async def seed_canonical_signs() -> dict[str, Any]:
    """Seed the canonical_signs table from crosswalks/canonical_sign_registry.csv."""
    db = _db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    csv_path = _ROOT / "crosswalks" / "canonical_sign_registry.csv"
    if not csv_path.exists():
        raise HTTPException(
            status_code=404,
            detail="canonical_sign_registry.csv not found — run scripts/cgsa_pipeline.py first"
        )
    with open(csv_path, newline="", encoding="utf-8") as f:
        signs = list(csv.DictReader(f))
    # Convert bool-like fields
    for s in signs:
        s["in_corpus"] = s.get("in_corpus", "False").lower() in ("true", "1", "yes")
    n = await db.seed_canonical_signs(signs)
    return {"seeded": n, "source": str(csv_path)}


# ── Sign Clusters ─────────────────────────────────────────────────────────────

@router.get("/sign-clusters/summary")
async def get_clusters_summary() -> dict[str, Any]:
    db = _db()
    if db is None:
        return {"n_clusters": 0, "cluster_k": 0, "n_signs": 0}
    return await db.get_clusters_summary()


@router.get("/sign-clusters")
async def list_cluster_assignments(cluster_k: int | None = None) -> list[dict[str, Any]]:
    db = _db()
    if db is None:
        return []
    return await db.list_cluster_assignments(cluster_k=cluster_k)


@router.post("/sign-clusters/seed", status_code=201)
async def seed_cluster_assignments() -> dict[str, Any]:
    """Seed sign_cluster_assignments from analysis/sign_clusters.json."""
    db = _db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    json_path = _ROOT / "analysis" / "sign_clusters.json"
    if not json_path.exists():
        raise HTTPException(
            status_code=404,
            detail="sign_clusters.json not found — run scripts/cgsa_pipeline.py first"
        )
    cluster_data = json.loads(json_path.read_text("utf-8"))
    best_k = cluster_data.get("best_k", 40)
    sil = cluster_data.get("k_results", {}).get(str(best_k), {}).get("silhouette", 0.0)
    s2c: dict[str, int] = cluster_data.get("sign_to_cluster", {})

    assignments = [
        {
            "sign_id": sign_id,
            "cluster_label": label,
            "cluster_k": best_k,
            "method": "hierarchical_ward",
            "silhouette": sil,
            "dominant_pos": "",
        }
        for sign_id, label in s2c.items()
    ]
    n = await db.seed_cluster_assignments(assignments, created_at=_now())
    return {"seeded": n, "best_k": best_k, "silhouette": sil, "source": str(json_path)}
