"""Semantic Scholar fetcher (https://api.semanticscholar.org/graph/v1/paper/search).

Keyless (rate-limited to ~100 req/5 min without a key). Returns academic
paper metadata with citation counts and TLDRs when available.
"""

from __future__ import annotations

import asyncio
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.semanticscholar")

_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search"
_FIELDS = "paperId,title,url,abstract,authors,year,citationCount,externalIds,tldr,publicationDate"


class SemanticScholarFetcher(Fetcher):
    source = "semanticscholar"
    requires = ()  # keyless (rate-limited)
    rate_delay: float = 6.0  # seconds between calls (conservative; 100 req/5 min)

    # Track last request time class-wide so multiple instances share cooldown.
    # Initialised to now so the first call after a restart always waits the
    # full rate_delay — prevents 429s when the backend restarts quickly.
    import time as _time_init
    _last_request: float = _time_init.monotonic()

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        # Enforce per-class rate limit before every request.
        import time as _time
        now = _time.monotonic()
        wait = self.rate_delay - (now - SemanticScholarFetcher._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        SemanticScholarFetcher._last_request = _time.monotonic()

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = " ".join(topic.keywords[:8]) or topic.label
        params: dict[str, object] = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": _FIELDS,
        }
        if since is not None:
            params["year"] = f"{since.year}-"
        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("SemanticScholar error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for p in data.get("data") or []:
            title = (p.get("title") or "").strip()
            if not title:
                continue
            ext = p.get("externalIds") or {}
            doi = ext.get("DOI") or ""
            url = (
                p.get("url")
                or (f"https://doi.org/{doi}" if doi else "")
                or f"https://www.semanticscholar.org/paper/{p.get('paperId', '')}"
            )
            if not url:
                continue
            abstract = (p.get("abstract") or "")[:1500]
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            pub_date = p.get("publicationDate") or ""
            if since is not None and pub_date:
                try:
                    pub_dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass
            authors = [
                (a.get("name") or "").strip()
                for a in (p.get("authors") or [])
                if isinstance(a, dict)
            ]
            tldr = (p.get("tldr") or {}).get("text") or ""
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date or str(p.get("year") or ""),
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "doi": doi,
                        "abstract": abstract,
                        "authors": [a for a in authors if a],
                        "citation_count": p.get("citationCount"),
                        "tldr": tldr[:500],
                        "paper_id": p.get("paperId") or "",
                    },
                )
            )
        return items
