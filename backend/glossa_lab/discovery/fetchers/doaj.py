"""DOAJ fetcher (https://doaj.org/api/search/articles/).

Keyless. Searches the Directory of Open Access Journals for articles
matching the topic profile. All results are open-access by definition.
"""

from __future__ import annotations

import logging
import urllib.parse
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.doaj")

_ENDPOINT = "https://doaj.org/api/search/articles"


class DOAJFetcher(Fetcher):
    source = "doaj"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = build_query(topic, quote_phrases=True) or topic.label
        # DOAJ search endpoint uses path-based query: /api/search/articles/{query}
        # The query goes into the URL *path* — it MUST be percent-encoded so
        # special chars (spaces, parens, quotes) don't break urllib.
        url = f"{_ENDPOINT}/{urllib.parse.quote(query, safe='')}"
        params = {
            "pageSize": min(max_results, 100),
            "sort": opts.get("sort", "last_updated:desc"),
        }
        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("doaj cooldown active — skipping (%.0fs remaining)", remaining)
            return []
        try:
            data = await run_in_thread(http_get_json, url, params=params, timeout=25.0)
        except FetcherError as exc:
            _429_cooldown(str(exc), self.source)
            _log.warning("DOAJ error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for r in data.get("results") or []:
            bibjson = r.get("bibjson") or {}
            title = (bibjson.get("title") or "").strip()
            if not title:
                continue
            # Build URL from identifiers
            doi = ""
            article_url = ""
            for ident in bibjson.get("identifier") or []:
                if ident.get("type") == "doi":
                    doi = (ident.get("id") or "").strip()
            for link in bibjson.get("link") or []:
                if link.get("type") == "fulltext":
                    article_url = (link.get("url") or "").strip()
                    break
            url_final = (
                f"https://doi.org/{doi}" if doi
                else article_url
                or f"https://doaj.org/article/{r.get('id', '')}"
            )
            if not url_final:
                continue
            abstract = (bibjson.get("abstract") or "")[:1500]
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            # Date: year + month if available
            year = bibjson.get("year") or ""
            month = bibjson.get("month") or ""
            pub_date = f"{year}-{month.zfill(2)}-01" if year and month else (year or "")
            if since is not None and pub_date and len(pub_date) >= 10:
                try:
                    pub_dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass
            authors = [
                (a.get("name") or "").strip()
                for a in (bibjson.get("author") or [])
                if isinstance(a, dict)
            ]
            journal = (bibjson.get("journal") or {}).get("title") or ""
            items.append(
                RawItem(
                    title=title,
                    url=url_final,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "doi": doi,
                        "abstract": abstract,
                        "authors": [a for a in authors if a],
                        "journal": journal,
                        "doaj_id": r.get("id") or "",
                    },
                )
            )
        return items
