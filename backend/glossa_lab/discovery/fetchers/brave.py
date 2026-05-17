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
    _429_cooldown,
    http_get_json,
    run_in_thread,
    source_is_cooling,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.brave")

_BASE = "https://api.search.brave.com/res/v1"

# Brave Search rejects queries longer than 50 whitespace-separated words. We
# stay 2 words below the cap to leave room for quote marks / safe overhead.
_BRAVE_MAX_WORDS = 48


def _word_count(s: str) -> int:
    """Count whitespace-separated tokens (matches Brave's word definition)."""
    return len(s.split())


def _build_brave_query(topic: TopicProfile, *, max_words: int = _BRAVE_MAX_WORDS) -> str:
    """Build a Brave-friendly OR-query that fits inside Brave's word limit.

    Strategy: format each keyword (quoting multi-word phrases), greedily add
    keywords from highest-priority (first in the topic file) to lowest until
    the next addition would push us over the cap. Then append exclusions in
    the same greedy fashion using the remaining headroom.
    """
    def fmt(term: str, *, neg: bool = False) -> str:
        prefix = "-" if neg else ""
        if " " in term:
            return f'{prefix}"{term}"'
        return f"{prefix}{term}"

    kept: list[str] = []
    used = 1  # the wrapping parens count as 0 tokens, but "OR" between adds 1 each
    for k in topic.keywords:
        if not k:
            continue
        token = fmt(k)
        # Adding this keyword costs (token words) + 1 for the OR connector
        cost = _word_count(token) + (1 if kept else 0)
        if used + cost > max_words:
            continue  # try the next, smaller keyword
        kept.append(token)
        used += cost
    if not kept:
        return ""
    keyword_q = " OR ".join(kept)
    body = f"({keyword_q})"
    used = _word_count(body)

    excl_kept: list[str] = []
    for e in topic.exclusions:
        if not e:
            continue
        token = fmt(e, neg=True)
        cost = _word_count(token) + 1  # space separator
        if used + cost > max_words:
            continue
        excl_kept.append(token)
        used += cost
    if excl_kept:
        body = f"{body} {' '.join(excl_kept)}"
    return body


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
        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("brave cooldown active — skipping (%.0fs remaining)", remaining)
            return []

        opts = topic.overrides_for(self.source)
        endpoint_kind = str(opts.get("search_endpoint", "news")).lower()
        endpoint = f"{_BASE}/news/search" if endpoint_kind == "news" else f"{_BASE}/web/search"
        # Brave-specific query (Brave’s 50-word cap is much tighter than other
        # providers). Other fetchers continue using the full ``build_query``.
        q = _build_brave_query(topic)
        if not q:
            return []
        params = {
            "q": q,
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
            _429_cooldown(str(exc), self.source)
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
