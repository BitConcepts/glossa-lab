"""CORE.ac.uk fetcher — 449M+ open access research papers.

API docs: https://api.core.ac.uk/docs/v3
Auth:     Bearer token via Authorization header (optional but recommended)
Rate limits:
  Unauthenticated:  100 requests/day, 10 req/min
  Personal key:     1,000 tokens/day, 25 req/min
  Academic key:     5,000 tokens/day, 10 req/min
Obtain a free key at: https://core.ac.uk/services/api
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    build_query,
    http_get_json,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.core_ac")

# Trailing slash is required — the API 301-redirects the slash-less URL
# and Python's urllib drops the Authorization header on the redirect.
_ENDPOINT = "https://api.core.ac.uk/v3/search/works/"


class COREFetcher(Fetcher):
    source = "core"
    requires = ()  # keyless — optional core_api_key for higher limits
    upgrade_key = "core_api_key"
    upgrade_url = "https://core.ac.uk/services/api"
    # Free tier: 10 req/min → 6s gap. Keyed personal: 25 req/min → 2.5s gap.
    # We default to the conservative free-tier value; fetch() tightens it
    # at runtime when a key is present.
    rate_delay = 6.0

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        from glossa_lab.api.settings import get_key  # noqa: PLC0415

        api_key = get_key("core_api_key") or ""
        # Honour faster rate for authenticated requests.
        if api_key:
            self.__class__.rate_delay = 2.5  # 25 req/min personal tier
        opts = topic.overrides_for(self.source)
        limit = int(opts.get("limit", 25))

        params: dict[str, object] = {
            "q": build_query(topic),
            "limit": limit,
        }
        if since:
            params["createdDate"] = f">={since.strftime('%Y-%m-%d')}"

        headers: dict[str, str] = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            data = await run_in_thread(
                http_get_json, _ENDPOINT, params=params,
                headers=headers if headers else None, timeout=20.0,
            )
        except FetcherError as exc:
            _log.warning("CORE error for topic %s: %s", topic.id, exc)
            return []

        results = (data or {}).get("results") or []
        items: list[RawItem] = []
        for r in results:
            title = (r.get("title") or "").strip()
            if not title:
                continue
            url = ""
            for link in (r.get("links") or []):
                if link.get("type") == "display":
                    url = link.get("url", "")
                    break
            if not url:
                url = r.get("downloadUrl") or r.get("sourceFulltextUrls", [""])[0] if r.get("sourceFulltextUrls") else ""
            if not url:
                url = f"https://core.ac.uk/works/{r.get('id', '')}"

            snippet = (r.get("abstract") or "")[:500]
            if not self._passes_exclusions(f"{title} {snippet}", topic.exclusions):
                continue

            authors = ", ".join(
                a.get("name", "") for a in (r.get("authors") or [])
            )
            items.append(RawItem(
                title=title,
                url=url,
                source=self.source,
                topic=topic.id,
                published_at=r.get("publishedDate") or r.get("createdDate") or "",
                lang=(topic.languages or ["en"])[0],
                raw={
                    "abstract": snippet,
                    "authors": authors,
                    "doi": r.get("doi") or "",
                    "year": r.get("yearPublished"),
                    "journal": (r.get("journals") or [{}])[0].get("title", "") if r.get("journals") else "",
                    "oa_status": "open_access",
                },
            ))
        return items
