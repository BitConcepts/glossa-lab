"""Brave Search fetcher (https://api.search.brave.com).

Supports both the ``/web/search`` and ``/news/search`` endpoints; the
``search_endpoint`` topic override (``"web"`` | ``"news"``) selects which.
Requires BRAVE_SEARCH_API_KEY.
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.brave")

_BASE = "https://api.search.brave.com/res/v1"


class BraveFetcher(Fetcher):
    source = "brave"
    requires = ("brave_search_api_key",)

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        from glossa_lab.api.settings import get_key

        api_key = get_key("brave_search_api_key")
        if not api_key:
            return []

        opts = topic.overrides_for(self.source)
        endpoint_kind = str(opts.get("search_endpoint", "news")).lower()
        endpoint = f"{_BASE}/news/search" if endpoint_kind == "news" else f"{_BASE}/web/search"
        params = {
            "q": build_query(topic),
            "count": int(opts.get("count", 20)),
            "country": opts.get("country", "us"),
            "search_lang": (topic.languages or ["en"])[0],
            "spellcheck": "0",
        }
        # Brave news: freshness window can be "pd","pw","pm","py" — mapped from since.
        if endpoint_kind == "news" and since is not None:
            delta_days = max(1, (datetime.utcnow().replace(tzinfo=since.tzinfo) - since).days or 1)
            if delta_days <= 1:
                params["freshness"] = "pd"
            elif delta_days <= 7:
                params["freshness"] = "pw"
            elif delta_days <= 31:
                params["freshness"] = "pm"
            else:
                params["freshness"] = "py"

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        }
        try:
            data = await run_in_thread(
                http_get_json, endpoint, params=params, headers=headers, timeout=20.0,
            )
        except FetcherError as exc:
            _log.warning("Brave error for topic %s: %s", topic.id, exc)
            return []

        results = []
        if endpoint_kind == "news":
            results = (data or {}).get("results") or []
        else:
            results = ((data or {}).get("web") or {}).get("results") or []

        items: list[RawItem] = []
        for r in results:
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            if not title or not url:
                continue
            description = r.get("description") or r.get("snippet") or ""
            if not self._passes_exclusions(f"{title} {description}", topic.exclusions):
                continue
            published = r.get("page_age") or r.get("age") or ""
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=str(published),
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "description": description,
                        "endpoint": endpoint_kind,
                        "meta_url": r.get("meta_url"),
                        "thumbnail": r.get("thumbnail"),
                    },
                )
            )
        return items
