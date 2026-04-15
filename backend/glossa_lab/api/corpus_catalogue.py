"""World Language Corpus Catalogue API.

Provides a browse-able catalogue of public-domain corpora spanning
ancient, modern, and undeciphered writing systems.  Users import
entries with one click; no Python file required to add a new language.

Endpoints:
  GET  /corpus-catalogue                -- browse the catalogue
  POST /corpus-catalogue/{id}/import    -- import a catalogue entry into the user's corpus DB
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = logging.getLogger("glossa_lab.api.corpus_catalogue")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/corpus-catalogue")
async def list_catalogue(
    script_type: str | None = None,
    undeciphered: bool | None = None,
) -> list[dict[str, Any]]:
    """Return the world language corpus catalogue, optionally filtered."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return []
    entries = await db.list_corpus_catalogue(
        script_type=script_type,
        is_undeciphered=undeciphered,
    )
    # Enrich with an `already_imported` flag by checking if a text with matching
    # name already exists in the user's corpus database.
    texts = await db.list_texts()
    existing_names = {t["name"] for t in texts}
    for e in entries:
        e["already_imported"] = e["name"] in existing_names
    return entries


@router.post("/corpus-catalogue/{catalogue_id}/import", status_code=201)
async def import_catalogue_entry(catalogue_id: str) -> dict[str, Any]:
    """Import a catalogue entry into the user's corpus database.

    If the catalogue entry has a `local_module` pointing to a bundled Python
    data module, the corpus is loaded immediately without a network call.
    Otherwise returns a 501 indicating external import is not yet supported.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    entry = await db.get_corpus_catalogue_entry(catalogue_id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Catalogue entry '{catalogue_id}' not found")

    local_module = entry.get("local_module", "")

    if not local_module:
        raise HTTPException(
            status_code=501,
            detail=(
                f"'{entry['name']}' does not have a bundled local module. "
                "Download the corpus from the source URL and upload it manually via + Upload / import corpus."
            ),
        )

    # Load via bundled data module
    try:
        import importlib  # noqa: PLC0415
        mod = importlib.import_module(f"glossa_lab.data.{local_module}")
        symbols: list[str] = mod.get_corpus_symbols()
        direction: str = "ltr"
        if hasattr(mod, "METADATA"):
            meta = mod.METADATA
            direction = meta.get("reading_direction", "ltr")
    except (ImportError, AttributeError) as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not load local module 'glossa_lab.data.{local_module}': {exc}",
        ) from exc

    # Check if already imported
    texts = await db.list_texts()
    existing = next((t for t in texts if t["name"] == entry["name"]), None)
    if existing:
        return {"imported": False, "reason": "already_exists", "corpus_id": existing["id"], "name": entry["name"]}

    text = await db.create_text(
        name=entry["name"],
        corpus_type="ancient" if entry.get("period", "") or entry.get("is_undeciphered") else "linguistic",
        content=symbols,
        metadata={
            "source": entry.get("source_url", ""),
            "language": entry.get("language", ""),
            "language_family": entry.get("language_family", ""),
            "script_type": entry.get("script_type", ""),
            "period": entry.get("period", ""),
            "license": entry.get("license", ""),
            "catalogue_id": catalogue_id,
        },
        reading_direction=direction,
        created_at=_now(),
    )
    logger.info("Imported corpus '%s' from catalogue (%d tokens)", entry["name"], len(symbols))
    return {"imported": True, "corpus_id": text["id"], "name": entry["name"], "tokens": len(symbols)}
