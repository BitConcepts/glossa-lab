"""GDELT DOC 2.0 API fetcher (https://api.gdeltproject.org/api/v2/doc/doc).

Keyless. Provides global news monitoring — articles from thousands of
worldwide news outlets, useful as a complement to the news-API-gated sources.
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.gdelt")

_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


class GDELTFetcher(Fetcher):
    source = "gdelt"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = build_query(topic, quote_phrases=True) or topic.label
        params: dict[str, object] = {
            "query": query,
            "mode": opts.get("mode", "ArtList"),
            "maxrecords": min(max_results, 250),
            "format": "json",
            "sort": opts.get("sort", "DateDesc"),
        }
        if since is not None:
            # GDELT accepts startdatetime as YYYYMMDDHHmmss
            params["startdatetime"] = since.strftime("%Y%m%d%H%M%S")
        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("GDELT error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for a in data.get("articles") or []:
            title = (a.get("title") or "").strip()
            url = (a.get("url") or "").strip()
            if not title or not url:
                continue
            if not self._passes_exclusions(title, topic.exclusions):
                continue
            # seendate is "YYYYMMDDTHHmmssZ"
            seen = a.get("seendate") or ""
            pub_date = ""
            if seen and len(seen) >= 8:
                try:
                    pub_date = datetime.strptime(seen[:8], "%Y%m%d").strftime("%Y-%m-%d")
                except ValueError:
                    pub_date = seen
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=a.get("language") or (topic.languages or ["en"])[0],
                    raw={
                        "domain": a.get("domain") or "",
                        "socialimage": a.get("socialimage") or "",
                        "seendate": seen,
                    },
                )
            )
        return items
