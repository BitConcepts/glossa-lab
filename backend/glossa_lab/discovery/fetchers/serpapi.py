"""SerpAPI fetcher (https://serpapi.com).

Two engines are supported via the ``engine`` topic override:
* ``google_news``    — News tab (default for news-y topics).
* ``google_scholar`` — Scholar (default for academic topics).

Requires SERP_API_KEY.
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
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.serpapi")

_ENDPOINT = "https://serpapi.com/search.json"


class SerpAPIFetcher(Fetcher):
    source = "serpapi"
    requires = ("serp_api_key",)

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        from glossa_lab.api.settings import get_key

        api_key = get_key("serp_api_key")
        if not api_key:
            return []
        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("serpapi cooldown active — skipping (%.0fs remaining)", remaining)
            return []

        opts = topic.overrides_for(self.source)
        engine = str(opts.get("engine", "google_news"))
        params: dict[str, object] = {
            "engine": engine,
            "q": build_query(topic),
            "num": int(opts.get("num", 20)),
            "hl": (topic.languages or ["en"])[0],
            "api_key": api_key,
        }
        # Scholar lets us pass year-low for the since window.
        if engine == "google_scholar" and since is not None:
            params["as_ylo"] = since.year

        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _429_cooldown(str(exc), self.source)
            _log.warning("SerpAPI error for topic %s (engine=%s): %s", topic.id, engine, exc)
            return []

        items: list[RawItem] = []
        if engine == "google_news":
            results = (data or {}).get("news_results") or []
            for r in results:
                title = (r.get("title") or "").strip()
                url = (r.get("link") or "").strip()
                if not title or not url:
                    continue
                snippet = r.get("snippet") or ""
                if not self._passes_exclusions(f"{title} {snippet}", topic.exclusions):
                    continue
                items.append(
                    RawItem(
                        title=title,
                        url=url,
                        source=self.source,
                        topic=topic.id,
                        published_at=r.get("date") or "",
                        lang=(topic.languages or ["en"])[0],
                        raw={
                            "snippet": snippet,
                            "source_name": r.get("source"),
                            "thumbnail": r.get("thumbnail"),
                            "engine": engine,
                        },
                    )
                )
        elif engine == "google_scholar":
            results = (data or {}).get("organic_results") or []
            for r in results:
                title = (r.get("title") or "").strip()
                url = (r.get("link") or "").strip()
                if not title or not url:
                    continue
                snippet = r.get("snippet") or ""
                if not self._passes_exclusions(f"{title} {snippet}", topic.exclusions):
                    continue
                pub_summary = (r.get("publication_info") or {}).get("summary") or ""
                items.append(
                    RawItem(
                        title=title,
                        url=url,
                        source=self.source,
                        topic=topic.id,
                        published_at="",  # Scholar gives a free-form string in publication_info
                        lang=(topic.languages or ["en"])[0],
                        raw={
                            "snippet": snippet,
                            "publication_summary": pub_summary,
                            "cited_by": (r.get("inline_links") or {}).get("cited_by"),
                            "engine": engine,
                        },
                    )
                )
        else:
            _log.warning("SerpAPI: unsupported engine %r", engine)
        return items
