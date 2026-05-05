"""GDELT DOC 2.0 API fetcher (https://api.gdeltproject.org/api/v2/doc/doc).

Keyless. Provides global news monitoring — articles from thousands of
worldwide news outlets, useful as a complement to the news-API-gated sources.
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.gdelt")

_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


class GDELTFetcher(Fetcher):
    source = "gdelt"
    requires = ()  # keyless
    rate_delay: float = 12.0  # GDELT enforces 1 req/5s; 12s avoids 429 under load
    # GDELT has no API key option — rate limit is fixed at 1 req/5s.
    _MAX_RETRIES: int = 2
    _RETRY_BACKOFF: float = 8.0  # seconds extra wait on 429

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
        wait = self.rate_delay - (now - GDELTFetcher._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        GDELTFetcher._last_request = _time.monotonic()

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
        # Retry loop for 429 / SSL-timeout / connection errors
        data: dict | None = None
        for attempt in range(1 + self._MAX_RETRIES):
            try:
                data = await run_in_thread(
                    http_get_json, _ENDPOINT, params=params, timeout=30.0,
                )
                break
            except FetcherError as exc:
                err_str = str(exc)
                is_retryable = (
                    "429" in err_str
                    or "timed out" in err_str.lower()
                    or "ssl" in err_str.lower()
                    or "urlopen error" in err_str.lower()
                )
                if is_retryable and attempt < self._MAX_RETRIES:
                    backoff = self._RETRY_BACKOFF * (attempt + 1)
                    _log.info(
                        "GDELT error for topic %s (attempt %d/%d), "
                        "retrying in %.0fs: %s",
                        topic.id, attempt + 1, self._MAX_RETRIES,
                        backoff, err_str[:120],
                    )
                    await asyncio.sleep(backoff)
                    GDELTFetcher._last_request = _time.monotonic()
                    continue
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
