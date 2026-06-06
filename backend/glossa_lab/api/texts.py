"""Text corpus management endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.corpus_utils import run_ashraf_detection
from glossa_lab.database import get_db

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


class DetectDirectionRawRequest(BaseModel):
    """Detect reading direction from raw word data without requiring a DB corpus."""
    words: list[list[str]] | None = None
    corpus_file: str | None = None  # e.g. "holdat" or path to a JSON corpus file


@router.post("/texts/detect-direction")
async def detect_direction_raw(
    body: DetectDirectionRawRequest | None = None,
) -> dict[str, Any]:
    """Run Ashraf & Sinha (2018) direction detection on raw data or a named corpus.

    Accepts either:
      - ``words``: explicit list of word token lists
      - ``corpus_file``: one of 'holdat', 'icit', 'cisi', or a relative path
        under backend/reports/ to a JSON file with an 'inscriptions' array

    Returns entropy analysis, inferred direction ('ltr'|'rtl'|'unknown'),
    confidence level, and human-readable interpretation.
    """
    import csv  # noqa: PLC0415
    import json as _json  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    from glossa_lab.corpus_utils import run_ashraf_detection  # noqa: PLC0415

    backend_dir = Path(__file__).resolve().parent.parent.parent
    words: list[list[str]] | None = None
    source = "caller_supplied"

    if body and body.words:
        words = body.words
        source = "caller_supplied"
    elif body and body.corpus_file:
        cf = body.corpus_file.lower().strip()
        if cf in ("holdat", "icit"):
            # Load Holdat CSV — group by seal, build word = sign sequence per seal
            holdat_path = backend_dir / "data" / "holdat_latest.csv"
            if not holdat_path.exists():
                holdat_path = backend_dir.parent / "data" / "holdat_latest.csv"
            if holdat_path.exists():
                seals: dict[str, list[tuple[int, str]]] = {}
                with open(holdat_path, encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        sid = r.get("cisi_number", "")
                        pos = int(r.get("position", 0))
                        sign = r.get("letters", "")
                        if sid and sign:
                            seals.setdefault(sid, []).append((pos, sign))
                words = []
                for sid in sorted(seals):
                    signs = seals[sid]
                    signs.sort(key=lambda x: x[0])
                    words.append([s for _, s in signs])
                source = f"holdat ({len(words)} seals)"
            else:
                raise HTTPException(404, "holdat_latest.csv not found")
        elif cf == "cisi":
            cisi_path = backend_dir.parent / "data" / "indus_cisi_corpus.json"
            if cisi_path.exists():
                cisi = _json.loads(cisi_path.read_text(encoding="utf-8"))
                if isinstance(cisi, list):
                    words = [item.get("sequence", []) for item in cisi if item.get("sequence")]
                else:
                    words = [item.get("sequence", []) for item in cisi.get("inscriptions", []) if item.get("sequence")]
                source = f"cisi ({len(words)} inscriptions)"
            else:
                raise HTTPException(404, "indus_cisi_corpus.json not found")
        else:
            # Try as a reports/ path
            report_path = backend_dir / "reports" / cf
            if not report_path.exists() and not cf.endswith(".json"):
                report_path = backend_dir / "reports" / f"{cf}.json"
            if report_path.exists():
                rdata = _json.loads(report_path.read_text(encoding="utf-8"))
                inscriptions = rdata.get("inscriptions", [])
                if inscriptions and isinstance(inscriptions[0], dict):
                    words = [i.get("sequence", []) for i in inscriptions if i.get("sequence")]
                elif inscriptions and isinstance(inscriptions[0], list):
                    words = inscriptions
                source = f"report:{cf} ({len(words or [])} inscriptions)"
            else:
                raise HTTPException(404, f"Corpus file '{cf}' not found")
    else:
        raise HTTPException(400, "Provide either 'words' or 'corpus_file' (holdat/icit/cisi/report_name)")

    if not words or len(words) < 2:
        return {
            "source": source,
            "inferred_direction": "unknown",
            "confidence": "low",
            "interpretation": "Insufficient data for direction detection.",
            "n_words": len(words or []),
        }

    result = run_ashraf_detection(words)
    return {"source": source, **result}


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
