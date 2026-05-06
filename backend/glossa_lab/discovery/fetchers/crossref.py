"""Crossref fetcher (https://api.crossref.org/works).

Keyless. Provides DOI-anchored bibliographic metadata.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    http_get_json,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.crossref")

_ENDPOINT = "https://api.crossref.org/works"


_RE_TAG = re.compile(r"<[^>]+>")
_RE_WHITESPACE = re.compile(r"\s{2,}")


def _strip_markup(text: str) -> str:
    """Remove HTML/XML/MathML tags, Unicode replacement chars, and collapse whitespace."""
    cleaned = _RE_TAG.sub(" ", text)
    # Strip Unicode replacement characters (�) that appear when source
    # data has encoding issues (common in Crossref metadata).
    cleaned = cleaned.replace("\uFFFD", "").replace("\uFFFE", "").replace("\uFFFF", "")
    cleaned = _RE_WHITESPACE.sub(" ", cleaned)
    return cleaned.strip()


def _join_title(parts: list[str] | None) -> str:
    if not parts:
        return ""
    raw = " ".join(p for p in parts if p).strip()
    return _strip_markup(raw)


def _published_iso(item: dict) -> str:
    pub = item.get("issued") or item.get("published-print") or item.get("published-online") or {}
    parts = pub.get("date-parts") or []
    if parts and parts[0]:
        bits = parts[0]
        y = bits[0] if len(bits) >= 1 else None
        m = bits[1] if len(bits) >= 2 else 1
        d = bits[2] if len(bits) >= 3 else 1
        if y:
            try:
                return datetime(int(y), int(m or 1), int(d or 1)).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                return str(y)
    return ""


class CrossrefFetcher(Fetcher):
    source = "crossref"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        params: dict[str, object] = {
            "query.bibliographic": " ".join(topic.keywords[:6]) or topic.label,
            "rows": int(opts.get("rows", 25)),
            "sort": opts.get("sort", "issued"),
            "order": opts.get("order", "desc"),
        }
        if since is not None:
            params["filter"] = f"from-pub-date:{since.strftime('%Y-%m-%d')}"

        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("Crossref error for topic %s: %s", topic.id, exc)
            return []

        items_in = (((data or {}).get("message") or {}).get("items")) or []
        items: list[RawItem] = []
        for it in items_in:
            title = _join_title(it.get("title"))
            url = (it.get("URL") or "").strip()
            doi = (it.get("DOI") or "").strip()
            if not title:
                continue
            # Prefer DOI URL form (canonical, deduplicates across mirrors).
            if doi and not url:
                url = f"https://doi.org/{doi}"
            if not url:
                continue
            abstract = _strip_markup(it.get("abstract") or "")
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            authors = [
                f"{(a.get('given') or '').strip()} {(a.get('family') or '').strip()}".strip()
                for a in (it.get("author") or [])
            ]
            container = (it.get("container-title") or [""])
            venue = container[0] if isinstance(container, list) and container else ""
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=_published_iso(it),
                    lang=(it.get("language") or (topic.languages or ["en"])[0]) or "en",
                    raw={
                        "doi": doi,
                        "abstract": abstract[:1500] if isinstance(abstract, str) else "",
                        "authors": [a for a in authors if a],
                        "venue": venue,
                        "type": it.get("type"),
                    },
                )
            )
        return items
