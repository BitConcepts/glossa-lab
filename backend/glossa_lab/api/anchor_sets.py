"""User-definable Anchor Sets API.

Anchor sets store verified sign → reading mappings that users can
reuse across experiments without embedding them in Python files.

Endpoints:
  GET    /anchor-sets                    -- list all anchor sets
  POST   /anchor-sets                    -- create a new anchor set
  GET    /anchor-sets/{id}               -- get one anchor set
  PUT    /anchor-sets/{id}               -- update anchor set
  DELETE /anchor-sets/{id}               -- delete anchor set

Creation is fail-closed (acceptance-path defect 7, 2026-11-13): anchor
sets feed experiments as verified mappings, so a pair may only name a
grapheme that exists in the program's records, and its confidence must
be stated by the caller — an omitted confidence is refused, never
defaulted to "high".
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
_log = logging.getLogger("glossa_lab.api.anchor_sets")

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
# The two in-repo sources of record for which graphemes exist: the
# anchor register (the signs API's "authoritative anchor file") and the
# pinned corpus snapshot's canonical grapheme inventory (snapshot
# SHA-256 pinned by the Spec 090 G3 freeze).
_ANCHOR_REGISTER = _BACKEND_DIR / "reports" / "INDUS_FINAL_ANCHORS.json"
_CORPUS_SNAPSHOT = (
    _BACKEND_DIR.parent
    / "glossa-corpus" / "indus" / "exports" / "indus_research.jsonl"
)

_KNOWN_GRAPHEMES: frozenset[str] | None = None


def _load_known_graphemes() -> frozenset[str]:
    """Union of grapheme ids from the anchor register and the pinned
    corpus snapshot. Either source alone suffices for membership; an
    empty result means neither source could be read (the caller fails
    closed), so only a non-empty result is cached."""
    global _KNOWN_GRAPHEMES  # noqa: PLW0603
    if _KNOWN_GRAPHEMES is not None:
        return _KNOWN_GRAPHEMES
    known: set[str] = set()
    try:
        data = json.loads(_ANCHOR_REGISTER.read_text(encoding="utf-8"))
        known.update((data.get("anchors") or {}).keys())
    except Exception:  # noqa: BLE001
        _log.warning("Anchor register unavailable for grapheme validation", exc_info=True)
    try:
        with open(_CORPUS_SNAPSHOT, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                for grapheme in record.get("canonical_grapheme_ids") or []:
                    if isinstance(grapheme, str):
                        known.add(grapheme)
    except Exception:  # noqa: BLE001
        _log.warning("Corpus snapshot unavailable for grapheme validation", exc_info=True)
    if known:
        _KNOWN_GRAPHEMES = frozenset(known)
    return frozenset(known)


def _grapheme_exists(cipher: str) -> bool:
    """Membership test with the register's naming equivalence: the
    register names digit signs M-prefixed (M342) where the corpus
    inventory names the same signs bare (342); either form matches."""
    known = _load_known_graphemes()
    forms = {cipher}
    if cipher.isdigit():
        forms.add(f"M{cipher}")
    elif cipher.startswith("M") and cipher[1:].isdigit():
        forms.add(cipher[1:])
    return bool(forms & known)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AnchorPair(BaseModel):
    """One verified cipher→target sign pair."""
    cipher:     str               # cipher sign (as it appears in the undeciphered corpus)
    target:     str               # target reading (e.g. phoneme, syllable value)
    confidence: str               # high | medium | low — required, never defaulted:
                                  # an omitted value is refused (422), not stored as "high"
    note:       str = ""


class AnchorSetCreate(BaseModel):
    name:        str
    description: str = ""
    corpus_id:   str | None = None
    language:    str = ""
    pairs:       list[AnchorPair] = []


class AnchorSetUpdate(BaseModel):
    name:        str | None = None
    description: str | None = None
    corpus_id:   str | None = None
    language:    str | None = None
    pairs:       list[AnchorPair] | None = None


@router.get("/anchor-sets")
async def list_anchor_sets(corpus_id: str | None = None) -> list[dict[str, Any]]:
    """List all anchor sets, optionally filtered by corpus_id."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return []
    return await db.list_anchor_sets(corpus_id=corpus_id)


@router.post("/anchor-sets", status_code=201)
async def create_anchor_set(body: AnchorSetCreate) -> dict[str, Any]:
    if body.pairs:
        if not _load_known_graphemes():
            raise HTTPException(
                status_code=503,
                detail=(
                    "Cannot verify anchor-set graphemes: anchor register and "
                    "corpus sign inventory are unavailable"
                ),
            )
        for pair in body.pairs:
            if not _grapheme_exists(pair.cipher):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Unknown grapheme '{pair.cipher}': not present in the "
                        "anchor register or the pinned corpus sign inventory"
                    ),
                )
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_anchor_set(
        name=body.name,
        description=body.description,
        corpus_id=body.corpus_id,
        language=body.language,
        pairs=[p.model_dump() for p in body.pairs],
        created_at=_now(),
    )


@router.get("/anchor-sets/{anchor_set_id}")
async def get_anchor_set(anchor_set_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.get_anchor_set(anchor_set_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return result


@router.put("/anchor-sets/{anchor_set_id}")
async def update_anchor_set(anchor_set_id: str, body: AnchorSetUpdate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    fields: dict[str, Any] = {}
    if body.name is not None:        fields["name"] = body.name
    if body.description is not None: fields["description"] = body.description
    if body.corpus_id is not None:   fields["corpus_id"] = body.corpus_id
    if body.language is not None:    fields["language"] = body.language
    if body.pairs is not None:       fields["pairs"] = [p.model_dump() for p in body.pairs]
    result = await db.update_anchor_set(anchor_set_id, **fields)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return result


@router.delete("/anchor-sets/{anchor_set_id}")
async def delete_anchor_set(anchor_set_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.delete_anchor_set(anchor_set_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return {"deleted": True, "id": anchor_set_id}
