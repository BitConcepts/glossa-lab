"""Text corpus management endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db
from glossa_lab.corpus_utils import run_ashraf_detection

router = APIRouter()


class TextCreate(BaseModel):
    """Request body for uploading a text corpus."""

    name: str
    corpus_type: str = "linguistic"
    content: list[str]
    metadata: dict[str, Any] = {}
    reading_direction: str = "unknown"


class TextResponse(BaseModel):
    """Serialised text returned by the API."""

    id: str
    name: str
    corpus_type: str
    content: list[str]
    alphabet_size: int
    symbol_set: list[str]
    metadata: dict[str, Any]
    reading_direction: str
    created_at: str


class TextUpdate(BaseModel):
    """Request body for updating corpus metadata/content."""

    name: str | None = None
    corpus_type: str | None = None
    content: list[str] | None = None
    metadata: dict[str, Any] | None = None
    reading_direction: str | None = None


class DetectDirectionRequest(BaseModel):
    """Optional request body for the detect-direction endpoint.

    *words* overrides the word structure derived from metadata; each
    inner list is a sequence of sign tokens forming one word.
    If omitted, the endpoint attempts to derive word structure from
    ``metadata.inscriptions`` or ``metadata.words``, and falls back to
    treating consecutive 4-token windows of *content* as pseudo-words.
    """

    words: list[list[str]] | None = None
    update_field: bool = True   # if True, persist the inferred direction to DB


@router.post("/texts", status_code=201)
async def create_text(body: TextCreate) -> TextResponse:
    """Upload a new text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    now = datetime.now(timezone.utc).isoformat()
    text = await db.create_text(
        name=body.name,
        corpus_type=body.corpus_type,
        content=body.content,
        metadata=body.metadata,
        reading_direction=body.reading_direction,
        created_at=now,
    )
    return TextResponse(**text)


@router.get("/texts")
async def list_texts() -> list[TextResponse]:
    """List all text corpora."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    rows = await db.list_texts()
    return [TextResponse(**r) for r in rows]


@router.get("/texts/{text_id}")
async def get_text(text_id: str) -> TextResponse:
    """Get a single text corpus by ID."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)


@router.put("/texts/{text_id}")
async def update_text(text_id: str, body: TextUpdate) -> TextResponse:
    """Update a text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.update_text(
        text_id,
        name=body.name,
        corpus_type=body.corpus_type,
        content=body.content,
        metadata=body.metadata,
        reading_direction=body.reading_direction,
    )
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)


@router.post("/texts/{text_id}/detect-direction")
async def detect_direction(
    text_id: str,
    body: DetectDirectionRequest | None = None,
) -> dict[str, Any]:
    """Run the Ashraf & Sinha (2018) handedness test on this corpus.

    Returns entropy values, inferred direction, and confidence score.
    If *update_field* is True (default), the detected direction is
    persisted to the corpus record so it can be used by downstream
    experiments automatically.

    Word structure resolution priority:
      1. ``body.words`` (caller-supplied explicit word list)
      2. ``metadata.inscriptions`` (list of lists stored at upload time)
      3. ``metadata.words`` (same format, alternative key)
      4. Fallback: sliding 4-token windows over flat content (coarse proxy)
    """
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    corpus = await db.get_text(text_id)
    if corpus is None:
        raise HTTPException(status_code=404, detail="Text not found")

    # --- Resolve word structure ---
    words: list[list[str]] | None = None

    if body is not None and body.words:
        words = body.words
    else:
        meta = corpus.get("metadata") or {}
        for key in ("inscriptions", "words"):
            if key in meta and isinstance(meta[key], list):
                candidate = meta[key]
                # Accept both list[list[str]] and list[str]
                if candidate and isinstance(candidate[0], list):
                    words = candidate
                    break
                elif candidate and isinstance(candidate[0], str):
                    # Each string is a space-separated word
                    words = [w.split() for w in candidate if w.strip()]
                    break

    if words is None:
        # Last-resort fallback: 4-token sliding windows over flat content
        content: list[str] = corpus.get("content") or []
        window = 4
        words = [
            content[i : i + window]
            for i in range(0, len(content) - window + 1, window)
        ]

    ashraf = run_ashraf_detection(words)

    update_body = body if body is not None else DetectDirectionRequest()
    if update_body.update_field and ashraf["inferred_direction"] in ("ltr", "rtl"):
        await db.update_text(text_id, reading_direction=ashraf["inferred_direction"])

    return {
        "text_id": text_id,
        "word_source": (
            "caller_supplied" if (body and body.words) else
            "metadata" if any(
                k in (corpus.get("metadata") or {}) for k in ("inscriptions", "words")
            ) else "sliding_window_fallback"
        ),
        **ashraf,
    }


@router.delete("/texts/{text_id}")
async def delete_text(text_id: str) -> TextResponse:
    """Delete a text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.delete_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)
