"""Unpaywall fetcher — find open access versions of papers by DOI.

API docs: https://unpaywall.org/products/api
Free tier: 100K req/day with email as key. No API key needed.
Pass your email as UNPAYWALL_EMAIL in Settings → Discovery.
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.unpaywall")

_ENDPOINT = "https://api.unpaywall.org/v2/search"


class UnpaywallFetcher(Fetcher):
    source = "unpaywall"
    requires = ("unpaywall_email",)
    rate_delay = 0.2  # polite rate

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        from glossa_lab.api.settings import get_key  # noqa: PLC0415

        email = get_key("unpaywall_email")
        if not email:
            return []

        opts = topic.overrides_for(self.source)
        limit = int(opts.get("limit", 25))
        query = build_query(topic)

        params: dict[str, object] = {
            "query": query,
            "is_oa": "true",
            "email": email,
        }

        try:
            data = await run_in_thread(
                http_get_json, _ENDPOINT, params=params, timeout=20.0,
            )
        except FetcherError as exc:
            _log.warning("Unpaywall error for topic %s: %s", topic.id, exc)
            return []

        results = (data or {}).get("results") or []
        items: list[RawItem] = []
        for r in results[:limit]:
            resp = r.get("response") or r
            title = (resp.get("title") or "").strip()
            doi = resp.get("doi") or ""
            if not title:
                continue

            # Best OA location
            best_oa = resp.get("best_oa_location") or {}
            url = best_oa.get("url") or best_oa.get("url_for_pdf") or ""
            if not url and doi:
                url = f"https://doi.org/{doi}"

            snippet = ""
            if not self._passes_exclusions(title, topic.exclusions):
                continue

            authors_list = resp.get("z_authors") or []
            authors = ", ".join(
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in authors_list[:5]
            )
            items.append(RawItem(
                title=title,
                url=url,
                source=self.source,
                topic=topic.id,
                published_at=resp.get("published_date") or "",
                lang=(topic.languages or ["en"])[0],
                raw={
                    "doi": doi,
                    "authors": authors,
                    "journal": resp.get("journal_name") or "",
                    "year": resp.get("year"),
                    "oa_status": resp.get("oa_status") or "unknown",
                    "is_oa": resp.get("is_oa", False),
                    "publisher": resp.get("publisher") or "",
                    "best_oa_url": best_oa.get("url") or "",
                    "pdf_url": best_oa.get("url_for_pdf") or "",
                },
            ))
        return items
