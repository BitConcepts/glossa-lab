"""NewsAPI fetcher (https://newsapi.org/).

Reads items from the ``/v2/everything`` endpoint, scoped by topic keywords
and (optionally) since-window. Requires NEWS_API_KEY.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    _429_cooldown,
    build_query,
    http_get_json,
    run_in_thread,
    source_is_cooling,
    to_iso,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.newsapi")

_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsAPIFetcher(Fetcher):
    source = "newsapi"
    requires = ("news_api_key",)

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        from glossa_lab.api.settings import get_key

        api_key = get_key("news_api_key")
        if not api_key:
            return []
        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("newsapi cooldown active — skipping (%.0fs remaining)", remaining)
            return []

        opts = topic.overrides_for(self.source)
        params = {
            "q": build_query(topic),
            "pageSize": int(opts.get("page_size", 50)),
            "sortBy": opts.get("sort_by", "publishedAt"),
            "language": (topic.languages or ["en"])[0],
            "apiKey": api_key,
        }
        if since is not None:
            params["from"] = to_iso(since)
        if "search_in" in opts:
            params["searchIn"] = opts["search_in"]

        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=20.0)
        except FetcherError as exc:
            _429_cooldown(str(exc), self.source)
            _log.warning("NewsAPI error for topic %s: %s", topic.id, exc)
            return []

        articles = (data or {}).get("articles") or []
        items: list[RawItem] = []
        for art in articles:
            title = (art.get("title") or "").strip()
            url = (art.get("url") or "").strip()
            if not title or not url:
                continue
            description = art.get("description") or ""
            if not self._passes_exclusions(f"{title} {description}", topic.exclusions):
                continue
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=art.get("publishedAt") or "",
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "description": description,
                        "author": art.get("author"),
                        "source_name": (art.get("source") or {}).get("name"),
                        "url_to_image": art.get("urlToImage"),
                    },
                )
            )
        return items
