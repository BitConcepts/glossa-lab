"""RAG (Retrieval-Augmented Generation) API endpoints.

Endpoints:
  POST /rag/index   -- rebuild the TF-IDF index from all sources
  POST /rag/query   -- run a semantic search against the index
  GET  /rag/status  -- return index size and age
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

import glossa_lab.rag as _rag
from glossa_lab.database import get_db

router = APIRouter(prefix="/rag", tags=["rag"])


class RagQueryRequest(BaseModel):
    query: str
    top_k: int = 5


@router.get("/status")
async def rag_status() -> dict[str, Any]:
    """Return current index size and staleness."""
    return {
        "index_size": _rag.index_size(),
        "index_age_seconds": _rag.index_age_seconds(),
        "ready": _rag.index_size() > 0,
    }


@router.post("/index")
async def rag_index() -> dict[str, Any]:
    """Rebuild the RAG index from all available sources."""
    db = get_db()
    count = await _rag.build_index(db)
    return {
        "indexed_chunks": count,
        "ready": count > 0,
    }


@router.post("/query")
async def rag_query(body: RagQueryRequest) -> dict[str, Any]:
    """Run a semantic search and return the top-k most relevant chunks."""
    # Auto-build the index on first query if not yet built
    if _rag.index_size() == 0:
        db = get_db()
        await _rag.build_index(db)

    results = _rag.query(body.query, top_k=body.top_k)
    return {
        "query": body.query,
        "results": results,
        "total": len(results),
    }
