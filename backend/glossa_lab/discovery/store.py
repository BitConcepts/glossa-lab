"""Discovery item store — domain types + thin wrappers over the DB layer.

The actual SQL schema (``discovery_items``) and CRUD live on the
``glossa_lab.database.Database`` class (V13 migration). This module exposes:

* ``RawItem``       — the dataclass produced by fetchers (Phase C).
* ``DiscoveryItem`` — the persisted shape returned by the store.
* ``canonical_url`` — URL normalisation used for deduplication.
* ``make_item_id``  — sha256(canonical_url + '|' + title) primary key.
* Async helper functions (``upsert``, ``get``, ``list_items``, etc.) that
  resolve the DB singleton at call-time so callers don't have to.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from glossa_lab.database import Database, get_db

# ── URL canonicalisation ─────────────────────────────────────────────────────

# Tracking parameters that should never affect dedupe identity.
_TRACKING_PARAMS = frozenset(
    {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src",
        "yclid", "dclid", "msclkid", "_hsenc", "_hsmi",
        "igshid", "trk", "trkCampaign",
    }
)


def canonical_url(url: str) -> str:
    """Return a normalised form of *url* suitable for deduplication.

    * Lowercases scheme and host.
    * Drops the fragment.
    * Strips well-known tracking query parameters.
    * Sorts the remaining query parameters for stable hashing.
    * Strips a trailing slash from the path (except for the root '/').
    """
    if not url:
        return ""
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower() or "http"
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    # Drop tracking params, sort the rest
    query_pairs = [
        (k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in _TRACKING_PARAMS
    ]
    query_pairs.sort()
    query = urlencode(query_pairs, doseq=True)
    return urlunsplit((scheme, netloc, path, query, ""))


def make_item_id(url: str, title: str) -> str:
    """Return the sha256 primary key for a discovery item."""
    cu = canonical_url(url)
    payload = f"{cu}|{(title or '').strip().lower()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ── Domain types ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class RawItem:
    """Producer-side record from a fetcher.

    Each fetcher in ``glossa_lab.discovery.fetchers`` yields ``RawItem``
    instances which are persisted via :func:`upsert_raw`.
    """

    title: str
    url: str
    source: str                # e.g. "newsapi", "brave", "openalex"
    topic: str                 # comma-separated topic ids the item matched
    published_at: str = ""     # ISO 8601, may be empty if provider omits it
    lang: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def item_id(self) -> str:
        return make_item_id(self.url, self.title)


@dataclass(slots=True)
class DiscoveryItem:
    """Persisted shape of a discovery item, hydrated from the DB."""

    id: str
    title: str
    url: str
    source: str
    topic: str
    published_at: str
    fetched_at: str
    lang: str
    raw_json: dict[str, Any]
    summary: str
    kind: str
    confidence: float
    links: list[dict[str, Any]]
    status: str
    notes: str

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "DiscoveryItem":
        # ``Database._row_to_dict`` already json-decodes raw_json + links.
        raw = row.get("raw_json")
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                raw = {}
        links = row.get("links")
        if isinstance(links, str):
            try:
                links = json.loads(links)
            except (json.JSONDecodeError, ValueError):
                links = []
        return cls(
            id=row["id"],
            title=row.get("title", ""),
            url=row.get("url", ""),
            source=row.get("source", ""),
            topic=row.get("topic", ""),
            published_at=row.get("published_at", ""),
            fetched_at=row.get("fetched_at", ""),
            lang=row.get("lang", ""),
            raw_json=raw or {},
            summary=row.get("summary", ""),
            kind=row.get("kind", "other"),
            confidence=float(row.get("confidence", 0.0) or 0.0),
            links=links or [],
            status=row.get("status", "new"),
            notes=row.get("notes", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _require_db() -> Database:
    db = get_db()
    if db is None:
        raise RuntimeError(
            "Glossa Lab database is not initialised. "
            "Discovery store calls require an active app lifespan."
        )
    return db


# ── Async wrappers around the Database CRUD ─────────────────────────────────


async def upsert_raw(item: RawItem, *, fetched_at: str | None = None) -> bool:
    """Persist a fetched ``RawItem``. Returns True if newly created."""
    db = _require_db()
    return await db.upsert_discovery_item(
        item_id=item.item_id,
        title=item.title,
        url=item.url,
        source=item.source,
        topic=item.topic,
        published_at=item.published_at,
        fetched_at=fetched_at or _now_iso(),
        lang=item.lang,
        raw=item.raw,
    )


async def update_classification(
    item_id: str,
    *,
    kind: str,
    confidence: float,
    summary: str,
    links: list[dict[str, Any]] | None = None,
) -> DiscoveryItem | None:
    db = _require_db()
    row = await db.update_discovery_classification(
        item_id,
        kind=kind,
        confidence=confidence,
        summary=summary,
        links=links,
    )
    return DiscoveryItem.from_row(row) if row else None


async def update_status(
    item_id: str, *, status: str, notes: str | None = None,
) -> DiscoveryItem | None:
    db = _require_db()
    row = await db.update_discovery_status(item_id, status=status, notes=notes)
    return DiscoveryItem.from_row(row) if row else None


async def get(item_id: str) -> DiscoveryItem | None:
    db = _require_db()
    row = await db.get_discovery_item(item_id)
    return DiscoveryItem.from_row(row) if row else None


async def list_items(
    *,
    topic: str | None = None,
    kind: str | None = None,
    status: str | None = None,
    since: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[DiscoveryItem]:
    db = _require_db()
    rows = await db.list_discovery_items(
        topic=topic, kind=kind, status=status,
        since=since, limit=limit, offset=offset,
    )
    return [DiscoveryItem.from_row(r) for r in rows]


async def count_by(group: str = "status") -> dict[str, int]:
    db = _require_db()
    return await db.count_discovery_by(group=group)


async def delete(item_id: str) -> bool:
    db = _require_db()
    res = await db.delete_discovery_item(item_id)
    return res is not None
