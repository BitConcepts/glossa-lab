"""USPTO Patent Public Search (PPUBS) fetcher.

Uses the PPUBS internal search API at https://ppubs.uspto.gov to search
US patents and published applications by keyword.  No API key required.

PPUBS updates daily and covers all US patents from 1790 to present and
published applications from 2001 to present.

Rate limits are undocumented; this fetcher uses a conservative delay.
"""

from __future__ import annotations

import asyncio
import json
import logging
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any, Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.uspto")

_ENDPOINT = "https://ppubs.uspto.gov/dirsearch-public/searches/searchWithBeFamily"
_USER_AGENT = (
    "GlossaLab-DiscoveryEngine/0.1 (+https://github.com/layer1labs/glossa-lab)"
)


# ── PPUBS POST helper ───────────────────────────────────────────────────────

def _ppubs_search(
    query_text: str,
    *,
    start: int = 0,
    page_count: int = 25,
    timeout: float = 25.0,
) -> dict[str, Any]:
    """Synchronous POST to the PPUBS search API."""
    body = json.dumps({
        "searchText": query_text,
        "fpiOnly": False,
        "fl": "*",
        "facet": False,
        "sort": "date_publ desc",
        "start": start,
        "pageCount": page_count,
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": _USER_AGENT,
    }
    req = urllib.request.Request(_ENDPOINT, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        body_text = ""
        try:
            body_text = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:  # noqa: BLE001
            pass
        raise FetcherError(f"PPUBS HTTP {exc.code}: {body_text}") from exc
    except urllib.error.URLError as exc:
        raise FetcherError(f"PPUBS URLError: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise FetcherError(f"PPUBS bad JSON: {exc}") from exc


# ── Fetcher ──────────────────────────────────────────────────────────────────


class USPTOFetcher(Fetcher):
    source = "uspto"
    requires = ()  # keyless — PPUBS is open
    rate_delay: float = 3.0  # undocumented limits; be conservative
    upgrade_key = "uspto_api_key"
    upgrade_url = "https://developer.uspto.gov/"

    import time as _time_init
    _last_request: float = _time_init.monotonic()

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        import time as _time  # noqa: PLC0415
        now = _time.monotonic()
        wait = self.rate_delay - (now - USPTOFetcher._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        USPTOFetcher._last_request = _time.monotonic()

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))

        # Build PPUBS field-search query: title OR abstract
        keywords = topic.keywords[:10] or [topic.label]
        kw_part = " OR ".join(
            f'"{k}"' if " " in k else k for k in keywords
        )
        query_text = f"TTL/({kw_part}) OR ABST/({kw_part})"

        # Narrow by issue-date when a ``since`` cutoff is specified.
        if since is not None:
            date_str = since.strftime("%Y%m%d")
            query_text = f"({query_text}) AND ISD/{date_str}->"

        try:
            data = await run_in_thread(
                _ppubs_search,
                query_text,
                page_count=min(max_results, 50),
                timeout=25.0,
            )
        except FetcherError as exc:
            _log.warning("PPUBS error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for p in data.get("patents") or []:
            title = (
                p.get("inventionTitle")
                or p.get("title")
                or ""
            ).strip()
            if not title:
                continue

            doc_id = (
                p.get("documentId")
                or p.get("patentNumber")
                or p.get("guid")
                or ""
            )
            patent_num = p.get("patentNumber") or ""
            if patent_num:
                clean_num = patent_num.replace("-", "").replace("/", "")
                url = f"https://patents.google.com/patent/{clean_num}"
            elif doc_id:
                url = (
                    "https://ppubs.uspto.gov/pubwebapp/external.html"
                    f"?q={doc_id}"
                )
            else:
                continue

            abstract_parts = (
                p.get("abstractText") or p.get("abstract") or ""
            )
            if isinstance(abstract_parts, list):
                abstract = " ".join(str(x) for x in abstract_parts)[:1500]
            else:
                abstract = str(abstract_parts)[:1500]

            if not self._passes_exclusions(
                f"{title} {abstract}", topic.exclusions,
            ):
                continue

            pub_date = (
                p.get("publicationDate")
                or p.get("datePublished")
                or ""
            )
            if since is not None and pub_date:
                try:
                    clean_date = pub_date.replace("-", "")[:8]
                    pub_dt = datetime.strptime(clean_date, "%Y%m%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass

            # Inventors may arrive as "|"-delimited string or list.
            inventors_raw = (
                p.get("inventors") or p.get("inventorName") or ""
            )
            if isinstance(inventors_raw, str):
                inventors = [
                    i.strip() for i in inventors_raw.split("|") if i.strip()
                ]
            elif isinstance(inventors_raw, list):
                inventors = [str(i).strip() for i in inventors_raw if i]
            else:
                inventors = []

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
                        "patent_number": patent_num,
                    },
                )
            )
        return items
