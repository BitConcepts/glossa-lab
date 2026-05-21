"""USPTO PPUBS patent search fetcher (keyless).

Uses the Patent Public Search (PPUBS) session-based API at
https://ppubs.uspto.gov to search US patents and published applications.
No API key required — PPUBS is open to the public.

The session flow follows the same pattern used by axiom's PatentsViewClient:
  1. GET /pubwebapp/  → acquire session cookies
  2. POST /api/users/me/session  → obtain caseId + access token
  3. POST /api/searches/searchWithBeFamily  → search with full query template

PatentsView (search.patentsview.org) migrated to the ODP in March 2026.
This fetcher replaces it with the PPUBS backend, keeping the same registry
slot so existing topic overrides for ``patentsview`` keep working.
"""

from __future__ import annotations

import asyncio
import copy
import http.cookiejar
import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    _429_cooldown,
    run_in_thread,
    source_is_cooling,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.patentsview")

_PPUBS_BASE = "https://ppubs.uspto.gov"
_UA = "GlossaLab-DiscoveryEngine/0.1 (+https://github.com/BitConcepts/glossa-lab)"

# Template derived from axiom's _PPUBS_QUERY_TEMPLATE (patent_mcp_server)
_QUERY_TEMPLATE: dict[str, Any] = {
    "start": 0,
    "pageCount": 25,
    "sort": "date_publ desc",
    "docFamilyFiltering": "familyIdFiltering",
    "searchType": 1,
    "familyIdEnglishOnly": True,
    "familyIdFirstPreferred": "US-PGPUB",
    "familyIdSecondPreferred": "USPAT",
    "familyIdThirdPreferred": "FPRS",
    "showDocPerFamilyPref": "showEnglish",
    "queryId": 0,
    "tagDocSearch": False,
    "query": {
        "caseId": None,
        "hl_snippets": "2",
        "op": "OR",
        "q": "",
        "queryName": "",
        "highlights": "1",
        "qt": "brs",
        "spellCheck": False,
        "viewName": "tile",
        "plurals": True,
        "britishEquivalents": True,
        "databaseFilters": [
            {"databaseName": "US-PGPUB", "countryCodes": []},
            {"databaseName": "USPAT", "countryCodes": []},
            {"databaseName": "USOCR", "countryCodes": []},
        ],
        "searchType": 1,
        "ignorePersist": True,
        "userEnteredQuery": "",
    },
}


# ── PPUBS session + search helpers ─────────────────────────────────────────

# Module-level session state (shared across calls)
_ppubs_case_id: int | None = None
_ppubs_token: str | None = None
_cookie_jar: http.cookiejar.CookieJar = http.cookiejar.CookieJar()
_opener: urllib.request.OpenerDirector | None = None

# Circuit breaker — disable PPUBS after consecutive session failures
import time as _time_cb  # noqa: E402
_ppubs_consecutive_fails: int = 0
_ppubs_skip_until: float = 0.0
_PPUBS_MAX_FAILS: int = 2
_PPUBS_COOLDOWN_SECS: float = 28800.0  # 8 h — PPUBS auth failures are persistent; avoid spam


def _ppubs_cb_record_failure() -> None:
    global _ppubs_consecutive_fails, _ppubs_skip_until  # noqa: PLW0603
    _ppubs_consecutive_fails += 1
    if _ppubs_consecutive_fails >= _PPUBS_MAX_FAILS:
        _ppubs_skip_until = _time_cb.monotonic() + _PPUBS_COOLDOWN_SECS
        _log.warning(
            "PPUBS circuit breaker OPEN (%d consecutive auth failures); "
            "disabling for %.0fs",
            _ppubs_consecutive_fails, _PPUBS_COOLDOWN_SECS,
        )


def _ppubs_cb_record_success() -> None:
    global _ppubs_consecutive_fails, _ppubs_skip_until  # noqa: PLW0603
    _ppubs_consecutive_fails = 0
    _ppubs_skip_until = 0.0


def _ppubs_cb_is_open() -> bool:
    if _ppubs_skip_until <= 0.0:
        return False
    return _time_cb.monotonic() < _ppubs_skip_until


def _get_opener() -> urllib.request.OpenerDirector:
    global _opener  # noqa: PLW0603
    if _opener is None:
        _opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(_cookie_jar),
        )
    return _opener


def _ppubs_headers(token: str | None = None) -> dict[str, str]:
    return {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": _UA,
        "Origin": _PPUBS_BASE,
        "Referer": f"{_PPUBS_BASE}/pubwebapp/",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Access-Token": token or "null",
    }


def _establish_session(timeout: float = 15.0) -> tuple[int, str]:
    """3-step session handshake.  Returns (caseId, accessToken)."""
    global _ppubs_case_id, _ppubs_token  # noqa: PLW0603
    opener = _get_opener()

    # Step 1 — GET /pubwebapp/ to acquire cookies
    req1 = urllib.request.Request(
        f"{_PPUBS_BASE}/pubwebapp/",
        headers={"User-Agent": _UA, "Accept": "text/html"},
    )
    opener.open(req1, timeout=timeout)  # we only care about cookies

    # Step 2 — POST /api/users/me/session to get caseId + token.
    # Body: null (not -1) — USPTO changed their API; sending -1 returns 400.
    body = b"null"
    req2 = urllib.request.Request(
        f"{_PPUBS_BASE}/api/users/me/session",
        data=body,
        headers=_ppubs_headers(None),
        method="POST",
    )
    with opener.open(req2, timeout=timeout) as resp:
        token = resp.headers.get("X-Access-Token", "")
        data = json.loads(resp.read())
    case_id: int = data["userCase"]["caseId"]

    _ppubs_case_id = case_id
    _ppubs_token = token
    return case_id, token


def _ppubs_search(
    query_text: str,
    *,
    max_results: int = 25,
    timeout: float = 25.0,
) -> dict[str, Any]:
    """Synchronous PPUBS search.  Establishes session on first call."""
    global _ppubs_case_id, _ppubs_token  # noqa: PLW0603
    opener = _get_opener()

    if _ppubs_case_id is None:
        _establish_session(timeout=timeout)

    payload = copy.deepcopy(_QUERY_TEMPLATE)
    payload["pageCount"] = min(max_results, 500)
    payload["query"]["caseId"] = _ppubs_case_id
    payload["query"]["q"] = query_text
    payload["query"]["queryName"] = query_text
    payload["query"]["userEnteredQuery"] = query_text

    body = json.dumps(payload).encode("utf-8")
    url = f"{_PPUBS_BASE}/api/searches/searchWithBeFamily"

    def _do_post() -> dict[str, Any]:
        req = urllib.request.Request(
            url, data=body, headers=_ppubs_headers(_ppubs_token), method="POST",
        )
        with opener.open(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}

    try:
        return _do_post()
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            # Session expired or unauthorized — re-establish and retry once
            _ppubs_case_id = None
            _ppubs_token = None
            try:
                _establish_session(timeout=timeout)
                payload["query"]["caseId"] = _ppubs_case_id
                result = _do_post()
                _ppubs_cb_record_success()
                return result
            except Exception as retry_exc:  # noqa: BLE001
                _ppubs_cb_record_failure()
                raise FetcherError(f"PPUBS HTTP {exc.code}: session re-establish failed: {retry_exc}") from exc
        body_text = ""
        try:
            body_text = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:  # noqa: BLE001
            pass
        raise FetcherError(f"PPUBS HTTP {exc.code}: {body_text}") from exc
    except urllib.error.URLError as exc:
        raise FetcherError(f"PPUBS connection error: {exc.reason}") from exc
    except (json.JSONDecodeError, KeyError) as exc:
        raise FetcherError(f"PPUBS bad response: {exc}") from exc


# ── Fetcher ──────────────────────────────────────────────────────────────────


class PatentsViewFetcher(Fetcher):
    """Keyless US patent search via PPUBS.

    Replaces the dead PatentsView API. Source name kept as ``patentsview``
    for backward compat with existing topic overrides.
    """

    source = "patentsview"
    requires = ()  # keyless — PPUBS is open
    rate_delay: float = 5.0  # PPUBS has no documented limit; be conservative
    upgrade_key = "patentsview_api_key"
    upgrade_url = "https://patentsview-support.atlassian.net/servicedesk/customer/portals"

    import time as _time_init
    _last_request: float = _time_init.monotonic()

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        import time as _time  # noqa: PLC0415
        now = _time.monotonic()
        wait = self.rate_delay - (now - PatentsViewFetcher._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        PatentsViewFetcher._last_request = _time.monotonic()

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))

        # Build PPUBS field-search query: title OR abstract
        keywords = topic.keywords[:10] or [topic.label]
        kw_part = " OR ".join(
            f'"{k}"' if " " in k else k for k in keywords
        )
        query_text = f"({kw_part})"

        # Narrow by publication date when a ``since`` cutoff is given.
        if since is not None:
            date_str = since.strftime("%Y%m%d")
            query_text = f"({query_text}) AND ISD/{date_str}->"

        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("patentsview cooldown active — skipping (%.0fs remaining)", remaining)
            return []
        # Skip if circuit breaker is open
        if _ppubs_cb_is_open():
            _log.debug("PPUBS circuit breaker open — skipping topic %s", topic.id)
            return []

        try:
            data = await run_in_thread(
                _ppubs_search, query_text,
                max_results=min(max_results, 50),
                timeout=25.0,
            )
            _ppubs_cb_record_success()
        except FetcherError as exc:
            _429_cooldown(str(exc), self.source)
            _log.warning("PPUBS error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        # Check for API-level error
        if data.get("error"):
            err = data["error"]
            msg = err.get("errorMessage", str(err)) if isinstance(err, dict) else str(err)
            _log.warning("PPUBS error for topic %s: %s", topic.id, msg)
            return []

        items: list[RawItem] = []
        for p in data.get("patents") or []:
            title = (p.get("inventionTitle") or p.get("title") or "").strip()
            if not title:
                continue

            guid = p.get("guid") or ""
            doc_id = guid.replace("-", "").replace(" ", "")
            if not doc_id:
                continue

            url = f"https://patents.google.com/patent/{doc_id}"

            # Exclusions check
            abstract_html = p.get("abstractHtml") or p.get("abstract") or ""
            if isinstance(abstract_html, str):
                abstract = abstract_html[:1500]
            else:
                abstract = str(abstract_html)[:1500]

            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue

            pub_date = (p.get("datePublished") or "")[:10]
            if since is not None and pub_date:
                try:
                    clean_date = pub_date.replace("-", "")[:8]
                    pub_dt = datetime.strptime(clean_date, "%Y%m%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass

            # Inventors
            inv_short = str(p.get("inventorsShort", ""))
            inv_list = p.get("inventors", [])
            if isinstance(inv_list, list):
                inventors = [str(i).strip() for i in inv_list if i]
            elif inv_short:
                inventors = [i.strip() for i in inv_short.split(",") if i.strip()]
            else:
                inventors = []

            # Assignee
            assignee_raw = p.get("assigneeName") or p.get("assignees") or ""
            if isinstance(assignee_raw, list):
                assignee = ", ".join(str(a) for a in assignee_raw[:5])
            else:
                assignee = str(assignee_raw)

            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "document_id": doc_id,
                        "abstract": abstract,
                        "inventors": inventors,
                        "assignee": assignee,
                        "application_number": str(
                            p.get("applicationNumber") or p.get("appNumber") or ""
                        ),
                        "cpc_codes": str(
                            p.get("cpcInventiveFlattened")
                            or p.get("cpcClassification")
                            or ""
                        ),
                    },
                )
            )
        return items
