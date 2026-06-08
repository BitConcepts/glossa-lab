"""Semantic Scholar fetcher.

Uses the S2AG (Semantic Scholar Academic Graph) API and S2ORC (Open Research
Corpus) fields to discover and expand the academic literature corpus relevant
to Indus script decipherment.

API surfaces used
-----------------
S2AG endpoints:
  /graph/v1/paper/search          — keyword search (primary discovery)
  /graph/v1/paper/{id}/citations  — find papers that CITE a key paper
  /graph/v1/paper/{id}/references — find papers a key paper REFERENCES
  /graph/v1/paper/batch           — bulk detail fetch for multiple paper IDs
  /recommendations/v1/papers/     — seed-based paper recommendations

S2ORC fields (via S2AG graph API):
  openAccessPdf      — URL to open-access full PDF (S2ORC provenance)
  s2FieldsOfStudy    — S2ORC field-of-study taxonomy classifications
  isOpenAccess       — whether the paper has an OA version

These fields are requested in every search so the discovery pipeline can:
  * surface open-access PDFs for deep-evidence extraction
  * filter / weight by academic field (Linguistics, History, CompSci, etc.)
  * use highly-cited papers as seeds for citation-graph expansion

Rate limits
-----------
With an API key: 1 req/sec.  Without: ~100 req/5 min (shared / IP-level).
Exponential backoff + global cooldown protect against 429s.
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
    http_get_json,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.semanticscholar")

_BASE    = "https://api.semanticscholar.org"
_ENDPOINT = f"{_BASE}/graph/v1/paper/search"
_BATCH_ENDPOINT = f"{_BASE}/graph/v1/paper/batch"
_RECOM_ENDPOINT = f"{_BASE}/recommendations/v1/papers/"

# ── S2AG + S2ORC field sets ──────────────────────────────────────────────────
# Core search fields (kept lean to stay within S2 response-size limits)
_SEARCH_FIELDS = (
    "paperId,title,url,abstract,authors,year,citationCount,"
    "externalIds,tldr,publicationDate,"
    # S2ORC provenance fields:
    "isOpenAccess,openAccessPdf,s2FieldsOfStudy"
)
_FIELDS = _SEARCH_FIELDS  # backwards-compat alias
_FIELDS_LIST = _SEARCH_FIELDS.split(",")

# Citation / reference expansion fields (minimal — we only need identity + abstract)
_EXPAND_FIELDS = (
    "paperId,title,url,abstract,authors,year,citationCount,"
    "externalIds,tldr,publicationDate,isOpenAccess,openAccessPdf,s2FieldsOfStudy"
)
_EXPAND_FIELDS_LIST = _EXPAND_FIELDS.split(",")

# ── SDK circuit breaker ─────────────────────────────────────────────────
# After _SDK_MAX_CONSECUTIVE_FAILS consecutive network errors, skip the
# SDK entirely and go straight to HTTP for _SDK_COOLDOWN_SECS seconds.
# Resets on any SDK success.
_sdk_consecutive_fails: int = 0
_sdk_skip_until: float = 0.0
_SDK_MAX_CONSECUTIVE_FAILS: int = 1  # open circuit after one timeout/hang
_SDK_COOLDOWN_SECS: float = 3600.0  # 60 minutes

# ── Global S2 endpoint cooldown (mirrors arXiv pattern) ─────────────────
# Rate limits are per-IP and global — a 429 from ANY task/topic blocks ALL
# future S2 requests until the window resets.  This prevents the pattern
# where the SDK exhausts the budget, then the HTTP fallback immediately
# fires and also gets 429.
_s2_cooldown_until: float = 0.0
_S2_DEFAULT_COOLDOWN: float = 900.0  # 15 min default when no Retry-After header
_S2_TIMEOUT_COOLDOWN: float = 600.0  # 10 min cooldown after read/network timeouts

import threading as _s2_lock_mod  # noqa: E402
import time as _time_sdk  # noqa: E402

# Protects _last_request so concurrent topic fetches can't both bypass the
# inter-request delay.  Pattern mirrors arXiv: atomically reserve the next
# request slot inside the lock, sleep *outside* it.
_s2_rate_lock: _s2_lock_mod.Lock = _s2_lock_mod.Lock()


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

    Requests S2AG core fields plus S2ORC provenance fields (openAccessPdf,
    s2FieldsOfStudy, isOpenAccess).  Returns raw paper dicts compatible with
    the existing fetch() processing.
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
        # S2ORC fields
        oap = getattr(p, "openAccessPdf", None)
        oa_pdf = ""
        if isinstance(oap, dict):
            oa_pdf = oap.get("url") or ""
        elif isinstance(oap, str):
            oa_pdf = oap
        fos_raw = getattr(p, "s2FieldsOfStudy", None) or []
        fields_of_study = [
            (f.get("category") if isinstance(f, dict) else str(f))
            for f in fos_raw
        ]
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
            # S2ORC provenance
            "isOpenAccess": bool(getattr(p, "isOpenAccess", False)),
            "openAccessPdf": oa_pdf,
            "s2FieldsOfStudy": [f for f in fields_of_study if f],
        })
    return out


def _http_get_json_sync(
    url: str,
    *,
    params: dict | None = None,
    headers: dict | None = None,
    json_body: dict | None = None,
    timeout: float = 15.0,
) -> dict:
    """Synchronous HTTP GET or POST (for use inside run_in_thread)."""
    import json as _json  # noqa: PLC0415
    import urllib.error  # noqa: PLC0415
    import urllib.parse  # noqa: PLC0415
    import urllib.request  # noqa: PLC0415

    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    hdrs = {"Accept": "application/json", "User-Agent": "GlossaLab/0.9"}
    if headers:
        hdrs.update(headers)
    if json_body is not None:
        data = _json.dumps(json_body).encode()
        hdrs["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    else:
        req = urllib.request.Request(url, headers=hdrs, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return _json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        raise FetcherError(f"{exc.code}: {exc.reason}") from exc
    except Exception as exc:  # noqa: BLE001
        raise FetcherError(str(exc)) from exc


class SemanticScholarFetcher(Fetcher):
    source = "semanticscholar"
    requires = ()  # keyless (rate-limited)
    rate_delay: float = 10.0  # seconds between calls (very conservative; keyless S2 is shared)
    upgrade_key = "semantic_scholar_api_key"
    upgrade_url = "https://www.semanticscholar.org/product/api#api-key-form"

    # Track last request time class-wide so multiple instances share cooldown.
    # Initialised to now so the first call after a restart always waits the
    # full rate_delay — prevents 429s when the backend restarts quickly.
    import time as _time_init
    _last_request: float = _time_init.monotonic()

    # ── S2AG: citation / reference graph expansion ──────────────────────

    async def _expand_via_citations(
        self,
        paper_id: str,
        *,
        headers: dict | None,
        limit: int = 15,
        direction: str = "citations",   # "citations" | "references"
    ) -> list[dict]:
        """Fetch papers that CITE or are REFERENCED BY a seed paper.

        direction="citations"  → papers that cited this paper (follow-on work)
        direction="references" → papers this paper cited (foundational work)

        Both use the S2AG /graph/v1/paper/{id}/{direction} endpoint.
        Results are deduplicated against the main search results by the caller.
        """
        cooling, _ = _s2_is_cooling()
        if cooling:
            return []
        url = f"{_BASE}/graph/v1/paper/{paper_id}/{direction}"
        params: dict[str, object] = {
            "fields": _EXPAND_FIELDS,
            "limit": min(limit, 50),
        }
        try:
            data = await run_in_thread(
                _http_get_json_sync, url,
                params=params, headers=headers, timeout=12.0,
            )
            if not isinstance(data, dict):
                return []
            # The response shape is {"data": [{"citingPaper": {...}}, ...]}
            # for citations and {"data": [{"citedPaper": {...}}, ...]} for
            # references.  Extract the nested paper object.
            key = "citingPaper" if direction == "citations" else "citedPaper"
            return [
                entry[key] for entry in (data.get("data") or [])
                if isinstance(entry, dict) and key in entry
            ]
        except FetcherError as exc:
            if "429" in str(exc):
                _s2_cooldown_trip(_S2_DEFAULT_COOLDOWN)
            _log.debug("S2AG %s expansion failed for %s: %s", direction, paper_id, exc)
            return []

    # ── S2AG: seed-based paper recommendations ───────────────────────────

    async def _fetch_recommendations(
        self,
        positive_ids: list[str],
        *,
        headers: dict | None,
        limit: int = 20,
    ) -> list[dict]:
        """Use S2AG recommendations API to find related papers.

        Sends a POST to /recommendations/v1/papers/ with a list of
        positive paper IDs (found by search) as seeds.  Returns papers
        that are semantically close but would not appear in a keyword search.
        Requires an API key for higher rate limits but works keyless too.
        """
        if not positive_ids:
            return []
        cooling, _ = _s2_is_cooling()
        if cooling:
            return []
        body: dict = {
            "positivePaperIds": positive_ids[:5],  # S2AG cap is ~5 positive seeds
            "negativePaperIds": [],
        }
        params: dict[str, object] = {
            "fields": _EXPAND_FIELDS,
            "limit": min(limit, 100),
        }
        try:
            data = await run_in_thread(
                _http_get_json_sync, _RECOM_ENDPOINT,
                params=params, headers=headers,
                json_body=body, timeout=15.0,
            )
            if not isinstance(data, dict):
                return []
            return data.get("recommendedPapers") or []
        except FetcherError as exc:
            if "429" in str(exc):
                _s2_cooldown_trip(_S2_DEFAULT_COOLDOWN)
            _log.debug("S2AG recommendations failed: %s", exc)
            return []

    # ── Main fetch ───────────────────────────────────────────────────────

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

        # With an API key the limit is 1 req/sec; without it use conservative 15s
        # (the free tier is ~100 req/5 min shared across all IPs — stay well clear).
        from glossa_lab.api.settings import get_key as _gk  # noqa: PLC0415
        s2_key = _gk("semantic_scholar_api_key")
        effective_delay = 1.2 if s2_key else self.rate_delay
        import time as _time
        # Atomically reserve the next request slot inside the lock, then sleep
        # outside — mirrors arXiv pattern to prevent concurrent topics from both
        # reading the same _last_request value and bypassing the delay.
        with _s2_rate_lock:
            now = _time.monotonic()
            wait = max(0.0, effective_delay - (now - SemanticScholarFetcher._last_request))
            SemanticScholarFetcher._last_request = now + wait  # reserve slot
        if wait > 0:
            await asyncio.sleep(wait)

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = " ".join(topic.keywords[:8]) or topic.label
        year_filter = f"{since.year}-" if since is not None else None

        # Prefer the bounded direct HTTP endpoint.  The PyPI SDK auto-paginates
        # internally and has repeatedly hung for ~90s in the scheduler; only use
        # it when a topic explicitly opts in with {"use_sdk": true}.
        papers: list[dict] = []
        _sdk_used = False
        use_sdk = bool(opts.get("use_sdk", False))

        if use_sdk and _sdk_is_bypassed():
            _log.debug(
                "SemanticScholar SDK bypassed (circuit open, %d consecutive failures); "
                "using direct HTTP for topic %s",
                _sdk_consecutive_fails, topic.id,
            )
        elif use_sdk:
            # Cap total SDK time — the SDK auto-paginates and can hang for many
            # minutes when the S2 API is slow or returning 5xx errors.
            _SDK_TOTAL_TIMEOUT = 30.0
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
                _log.warning(
                    "SemanticScholar SDK timeout (>%.0fs) for topic %s; "
                    "tripping circuit breaker + %.0fs global cooldown (consecutive: %d)",
                    _SDK_TOTAL_TIMEOUT, topic.id, _S2_TIMEOUT_COOLDOWN, _sdk_consecutive_fails,
                )
                _s2_cooldown_trip(_S2_TIMEOUT_COOLDOWN)
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
        headers: dict[str, str] | None = None
        if s2_key:
            headers = {"x-api-key": s2_key}

        if not papers:
            params: dict[str, object] = {
                "query": query,
                "limit": min(max_results, 100),
                "fields": _SEARCH_FIELDS,
            }
            if year_filter:
                params["year"] = year_filter
            try:
                data = await run_in_thread(
                    http_get_json, _ENDPOINT, params=params,
                    headers=headers, timeout=15.0,
                )
            except FetcherError as exc:
                err_str = str(exc)
                is_429 = "429" in err_str
                is_timeout = "timed out" in err_str.lower() or "timeout" in err_str.lower()
                if is_429:
                    import re as _re  # noqa: PLC0415
                    ra_match = _re.search(r"Retry-After:\s*(\d+)", err_str)
                    cooldown = int(ra_match.group(1)) + 5 if ra_match else _S2_DEFAULT_COOLDOWN
                    _s2_cooldown_trip(cooldown)
                elif is_timeout:
                    _s2_cooldown_trip(_S2_TIMEOUT_COOLDOWN)
                    _log.warning(
                        "SemanticScholar HTTP timeout for topic %s — global cooldown set to %.0fs",
                        topic.id, _S2_TIMEOUT_COOLDOWN,
                    )
                _log.warning("SemanticScholar HTTP error for topic %s: %s", topic.id, exc)
                return []
            if not isinstance(data, dict):
                return []
            papers = data.get("data") or []

        # ── S2AG expansion: citations + recommendations (API-key only to
        # protect the shared IP-wide rate limit; skipped when keyless). ──
        # Elect the top-2 papers by citation count as seeds.
        # With an API key we can afford up to 3 extra requests per topic
        # (1 citations, 1 references, 1 recommendations).  Without a key
        # the base search already consumes most of the budget.
        if s2_key and papers and not _s2_is_cooling()[0]:
            do_expand = bool(opts.get("expand", True))  # opt-out with {"expand": false}
            if do_expand:
                sorted_by_cit = sorted(
                    [p for p in papers if p.get("paperId")],
                    key=lambda p: int(p.get("citationCount") or 0),
                    reverse=True,
                )
                seed_ids = [p["paperId"] for p in sorted_by_cit[:2]]

                expand_limit = int(opts.get("expand_limit", 15))

                # 1. Citing papers (follow-on work in the same area)
                if seed_ids:
                    extra_cit = await self._expand_via_citations(
                        seed_ids[0], headers=headers,
                        limit=expand_limit, direction="citations",
                    )
                    papers.extend(extra_cit)
                    _log.debug(
                        "S2AG citation expansion for topic %s: +%d papers from citing %s",
                        topic.id, len(extra_cit), seed_ids[0],
                    )

                # 2. Recommendations seeded from top search results
                recom = await self._fetch_recommendations(
                    seed_ids, headers=headers, limit=expand_limit,
                )
                papers.extend(recom)
                _log.debug(
                    "S2AG recommendations for topic %s: +%d papers",
                    topic.id, len(recom),
                )

        # ── Deduplicate by paperId, then convert to RawItems ─────────
        seen_ids: set[str] = set()
        items: list[RawItem] = []
        for p in papers:
            title = (p.get("title") or "").strip()
            if not title:
                continue
            paper_id = p.get("paperId") or ""
            if paper_id and paper_id in seen_ids:
                continue
            if paper_id:
                seen_ids.add(paper_id)

            ext = p.get("externalIds") or {}
            doi = ext.get("DOI") or ""
            url = (
                p.get("url")
                or (f"https://doi.org/{doi}" if doi else "")
                or (f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else "")
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

            # ── S2ORC provenance fields ────────────────────────────────
            # openAccessPdf: {"url": "...", "status": "GREEN"} or None
            oap = p.get("openAccessPdf")
            oa_pdf_url = ""
            if isinstance(oap, dict):
                oa_pdf_url = oap.get("url") or ""
            elif isinstance(oap, str):
                oa_pdf_url = oap
            is_oa = bool(p.get("isOpenAccess", False))
            # s2FieldsOfStudy: [{"category": "Linguistics", "source": "s2-fos-model"}, ...]
            fos_raw = p.get("s2FieldsOfStudy") or []
            fields_of_study = [
                f.get("category", "") if isinstance(f, dict) else str(f)
                for f in fos_raw
            ]

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
                        "paper_id": paper_id,
                        # S2ORC provenance
                        "open_access": is_oa,
                        "open_access_pdf": oa_pdf_url,
                        "fields_of_study": [f for f in fields_of_study if f],
                    },
                )
            )
        return items
