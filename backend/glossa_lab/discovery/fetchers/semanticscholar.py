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

# ── SDK circuit breaker ─────────────────────────────────────────────────
# After _SDK_MAX_CONSECUTIVE_FAILS consecutive network errors, skip the
# SDK entirely and go straight to HTTP for _SDK_COOLDOWN_SECS seconds.
# Resets on any SDK success.
_sdk_consecutive_fails: int = 0
_sdk_skip_until: float = 0.0
_SDK_MAX_CONSECUTIVE_FAILS: int = 2  # open circuit after 2 consecutive timeouts
_SDK_COOLDOWN_SECS: float = 900.0  # 15 minutes

# ── Global S2 endpoint cooldown (mirrors arXiv pattern) ─────────────────
# Rate limits are per-IP and global — a 429 from ANY task/topic blocks ALL
# future S2 requests until the window resets.  This prevents the pattern
# where the SDK exhausts the budget, then the HTTP fallback immediately
# fires and also gets 429.
_s2_cooldown_until: float = 0.0
_S2_DEFAULT_COOLDOWN: float = 120.0  # 2 min default when no Retry-After header

import time as _time_sdk  # noqa: E402


def _s2_cooldown_trip(secs: float) -> None:
    """Set the global S2 cooldown.  All fetches check this before starting."""
    global _s2_cooldown_until  # noqa: PLW0603
    _s2_cooldown_until = _time_sdk.monotonic() + secs
    _log.warning(
        "SemanticScholar global cooldown: pausing ALL S2 requests for %.0fs", secs
    )


def _s2_is_cooling() -> tuple[bool, float]:
    """Returns (is_cooling, seconds_remaining)."""
    remaining = _s2_cooldown_until - _time_sdk.monotonic()
    return remaining > 0, max(0.0, remaining)


def _sdk_record_success() -> None:
    global _sdk_consecutive_fails, _sdk_skip_until  # noqa: PLW0603
    _sdk_consecutive_fails = 0
    _sdk_skip_until = 0.0


def _sdk_record_failure() -> None:
    global _sdk_consecutive_fails, _sdk_skip_until  # noqa: PLW0603
    _sdk_consecutive_fails += 1
    if _sdk_consecutive_fails >= _SDK_MAX_CONSECUTIVE_FAILS:
        _sdk_skip_until = _time_sdk.monotonic() + _SDK_COOLDOWN_SECS
        _log.info(
            "SemanticScholar SDK circuit breaker OPEN (%d consecutive network errors); "
            "using direct HTTP for %.0fs",
            _sdk_consecutive_fails, _SDK_COOLDOWN_SECS,
        )


def _sdk_is_bypassed() -> bool:
    """True when the circuit breaker is open — skip SDK, go to HTTP."""
    if _sdk_skip_until <= 0.0:
        return False
    if _time_sdk.monotonic() >= _sdk_skip_until:
        # Cooldown expired — allow one probe attempt
        return False
    return True


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
        # Check global S2 cooldown first — rate limits are per-IP, shared across
        # all tasks and topics.  If any previous call was 429'd, skip entirely.
        cooling, remaining = _s2_is_cooling()
        if cooling:
            _log.debug(
                "SemanticScholar global cooldown active for topic %s — skipping (%.0fs remaining)",
                topic.id, remaining,
            )
            return []

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
        # is not installed or the SDK circuit breaker is open.
        papers: list[dict] = []
        _sdk_used = False

        if _sdk_is_bypassed():
            _log.debug(
                "SemanticScholar SDK bypassed (circuit open, %d consecutive failures); "
                "using direct HTTP for topic %s",
                _sdk_consecutive_fails, topic.id,
            )
        else:
            # Cap total SDK time — the SDK auto-paginates and can hang for many
            # minutes when the S2 API is slow or returning 5xx errors.
            _SDK_TOTAL_TIMEOUT = 90.0  # increased from 45s — S2 can be legitimately slow
            try:
                papers = await asyncio.wait_for(
                    run_in_thread(
                        _sdk_search,
                        query,
                        api_key=s2_key,
                        max_results=max_results,
                        year_filter=year_filter,
                    ),
                    timeout=_SDK_TOTAL_TIMEOUT,
                )
                _sdk_record_success()
                _sdk_used = True
                _log.debug(
                    "SemanticScholar SDK returned %d results for topic %s",
                    len(papers), topic.id,
                )
            except ImportError:
                # semanticscholar package not installed — fall back to direct HTTP.
                _log.debug("semanticscholar PyPI package not found; using direct HTTP")

            except asyncio.TimeoutError:
                # SDK took too long — the SDK made multiple paginated requests
                # internally while timing out, which consumed the rate limit budget.
                # Trip circuit breaker AND set a global cooldown before HTTP fallback
                # so we don't immediately fire another request into a depleted window.
                _sdk_record_failure()
                _s2_cooldown_trip(60.0)  # 60s: let the per-IP window partially reset
                _log.warning(
                    "SemanticScholar SDK timeout (>%.0fs) for topic %s; "
                    "tripping circuit breaker + 60s global cooldown (consecutive: %d)",
                    _SDK_TOTAL_TIMEOUT, topic.id, _sdk_consecutive_fails,
                )
                # papers stays [] — HTTP fallback is SKIPPED because cooldown is now active;
                # subsequent topics will also skip via the cooldown check at fetch() start.
                return []

            except Exception as exc:  # noqa: BLE001
                err_lower = str(exc).lower()
                is_circuit_breaker = any(k in err_lower for k in (
                    "network", "connect", "timeout", "unreachable", "reset",
                    "eof", "ssl", "socket", "host", "gateway",
                    # S2 server errors also warrant circuit-breaker + HTTP fallback
                    "server error", "internal server", "bad gateway", "service unavailable",
                ))
                if is_circuit_breaker:
                    _sdk_record_failure()
                    _log.debug(
                        "SemanticScholar SDK error for topic %s (%s); "
                        "falling back to direct HTTP (consecutive failures: %d)",
                        topic.id, type(exc).__name__, _sdk_consecutive_fails,
                    )
                    # papers stays [] — HTTP fallback below
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
                err_str = str(exc)
                is_429 = "429" in err_str
                if is_429:
                    # 429 on HTTP fallback — trip global cooldown so all parallel
                    # and subsequent tasks know the IP-wide budget is exhausted.
                    import re as _re  # noqa: PLC0415
                    ra_match = _re.search(r"Retry-After:\s*(\d+)", err_str)
                    cooldown = int(ra_match.group(1)) + 5 if ra_match else _S2_DEFAULT_COOLDOWN
                    _s2_cooldown_trip(cooldown)
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
