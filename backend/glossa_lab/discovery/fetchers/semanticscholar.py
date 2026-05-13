"""Semantic Scholar fetcher.

Uses the ``semanticscholar`` PyPI package (danielnsilva/semanticscholar) when
available, which supports automatic pagination beyond the 100-result-per-page
REST API limit.  Falls back to a direct HTTP call when the package is not
installed, which is capped at 100 results per request.

With an API key (``semantic_scholar_api_key`` in Settings) the rate limit
improves to 1 req/sec across all endpoints.  Without a key the free tier
is ~100 req/5 min, shared with all unauthenticated users.
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
_FIELDS_LIST = _FIELDS.split(",")


def _sdk_search(
    query: str,
    *,
    api_key: str | None,
    max_results: int,
    year_filter: str | None,
) -> list[dict]:
    """Search via the semanticscholar PyPI SDK (auto-paginates).

    Returns raw paper dicts compatible with the existing fetch() processing.
    Raises ImportError if the package is not installed.
    """
    from semanticscholar import SemanticScholar  # noqa: PLC0415
    sch = SemanticScholar(api_key=api_key or None, timeout=30)
    kw: dict = {"fields": _FIELDS_LIST, "limit": max_results}
    if year_filter:
        kw["year"] = year_filter
    results = sch.search_paper(query, **kw)
    out: list[dict] = []
    for p in results:
        if len(out) >= max_results:
            break
        ext = dict(getattr(p, "externalIds", None) or {})
        tldr = getattr(p, "tldr", None)
        tldr_text = ""
        if isinstance(tldr, dict):
            tldr_text = tldr.get("text") or ""
        elif hasattr(tldr, "text"):
            tldr_text = str(tldr.text or "")
        out.append({
            "paperId": str(getattr(p, "paperId", "") or ""),
            "title": str(getattr(p, "title", "") or ""),
            "url": str(getattr(p, "url", "") or ""),
            "abstract": str(getattr(p, "abstract", "") or ""),
            "authors": [
                {"name": a.name if hasattr(a, "name") else str(a)}
                for a in (getattr(p, "authors", None) or [])
            ],
            "year": getattr(p, "year", None),
            "citationCount": getattr(p, "citationCount", None),
            "externalIds": ext,
            "tldr": {"text": tldr_text},
            "publicationDate": str(getattr(p, "publicationDate", "") or ""),
        })
    return out


class SemanticScholarFetcher(Fetcher):
    source = "semanticscholar"
    requires = ()  # keyless (rate-limited)
    rate_delay: float = 6.0  # seconds between calls (conservative; 100 req/5 min)
    upgrade_key = "semantic_scholar_api_key"
    upgrade_url = "https://www.semanticscholar.org/product/api#api-key-form"

    # Track last request time class-wide so multiple instances share cooldown.
    # Initialised to now so the first call after a restart always waits the
    # full rate_delay — prevents 429s when the backend restarts quickly.
    import time as _time_init
    _last_request: float = _time_init.monotonic()

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        # With an API key the limit is 1 req/sec; without it use conservative 6s.
        from glossa_lab.api.settings import get_key as _gk  # noqa: PLC0415
        s2_key = _gk("semantic_scholar_api_key")
        effective_delay = 1.1 if s2_key else self.rate_delay
        import time as _time
        now = _time.monotonic()
        wait = effective_delay - (now - SemanticScholarFetcher._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        SemanticScholarFetcher._last_request = _time.monotonic()

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = " ".join(topic.keywords[:8]) or topic.label
        year_filter = f"{since.year}-" if since is not None else None

        # Try the PyPI SDK first — it handles pagination automatically, allowing
        # max_results > 100.  Fall back to a single-page REST call if the package
        # is not installed.
        papers: list[dict] = []
        try:
            papers = await run_in_thread(
                _sdk_search,
                query,
                api_key=s2_key,
                max_results=max_results,
                year_filter=year_filter,
            )
            _log.debug(
                "SemanticScholar SDK returned %d results for topic %s",
                len(papers), topic.id,
            )
        except ImportError:
            # semanticscholar package not installed — fall back to direct HTTP.
            _log.debug("semanticscholar PyPI package not found; using direct HTTP")

        except Exception as exc:  # noqa: BLE001
            # Network/connection errors from the SDK are transient — fall through
            # to the direct HTTP path instead of failing entirely.
            err_lower = str(exc).lower()
            is_network = any(k in err_lower for k in (
                "network", "connect", "timeout", "unreachable", "reset",
                "eof", "ssl", "socket", "host",
            ))
            if is_network:
                _log.info(
                    "SemanticScholar SDK network error for topic %s (%s: %s); "
                    "falling back to direct HTTP",
                    topic.id, type(exc).__name__, str(exc)[:120],
                )
                # papers stays [] — will trigger the HTTP fallback below
            else:
                _log.warning("SemanticScholar SDK error for topic %s: %s", topic.id, exc)
                return []

        # ── HTTP fallback (SDK not installed OR network error from SDK) ──
        if not papers:
            headers: dict[str, str] | None = None
            if s2_key:
                headers = {"x-api-key": s2_key}
            params: dict[str, object] = {
                "query": query,
                "limit": min(max_results, 100),
                "fields": _FIELDS,
            }
            if year_filter:
                params["year"] = year_filter
            try:
                data = await run_in_thread(
                    http_get_json, _ENDPOINT, params=params,
                    headers=headers, timeout=25.0,
                )
            except FetcherError as exc:
                _log.warning("SemanticScholar HTTP error for topic %s: %s", topic.id, exc)
                return []
            if not isinstance(data, dict):
                return []
            papers = data.get("data") or []

        items: list[RawItem] = []
        for p in papers:
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
