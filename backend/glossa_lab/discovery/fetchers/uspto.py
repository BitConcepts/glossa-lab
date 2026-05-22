"""USPTO Open Data Portal (ODP) fetcher.

Uses the ODP REST API at https://api.uspto.gov to search US patent
applications by keyword.

Requires a USPTO API key (``uspto_api_key`` in Settings).
Register at: https://developer.uspto.gov/

Rate limits apply per-key; the default delay is conservative.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Iterable

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

_log = logging.getLogger("glossa_lab.discovery.fetchers.uspto")

_BASE = "https://api.uspto.gov/api/v1/patent/applications/search"


# ── Fetcher ──────────────────────────────────────────────────────────────────


import threading as _uspto_lock_mod  # noqa: E402
_uspto_rate_lock: _uspto_lock_mod.Lock = _uspto_lock_mod.Lock()


class USPTOFetcher(Fetcher):
    source = "uspto"
    requires = ("uspto_api_key",)
    rate_delay: float = 2.0
    upgrade_key = ""
    upgrade_url = ""

    import time as _time_init
    _last_request: float = _time_init.monotonic()

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        # Check cooldown BEFORE sleeping for rate_delay.
        from glossa_lab.api.settings import get_key  # noqa: PLC0415
        api_key = get_key("uspto_api_key")
        if not api_key:
            return []
        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("uspto cooldown active — skipping (%.0fs remaining)", remaining)
            return []

        # Atomically reserve the next request slot.
        import time as _time  # noqa: PLC0415
        with _uspto_rate_lock:
            now = _time.monotonic()
            wait = max(0.0, self.rate_delay - (now - USPTOFetcher._last_request))
            USPTOFetcher._last_request = now + wait
        if wait > 0:
            await asyncio.sleep(wait)

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))

        # Build keyword query for ODP searchText parameter
        keywords = topic.keywords[:10] or [topic.label]
        search_text = " OR ".join(
            f'"{k}"' if " " in k else k for k in keywords
        )

        params: dict[str, Any] = {
            "searchText": search_text,
            "rows": min(max_results, 50),
            "start": 0,
        }
        headers: dict[str, str] = {"X-API-KEY": api_key}

        try:
            data = await run_in_thread(
                http_get_json, _BASE, params=params, headers=headers,
                timeout=25.0,
            )
        except FetcherError as exc:
            _429_cooldown(str(exc), self.source)
            _log.warning("ODP error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for entry in data.get("patentFileWrapperDataBag") or []:
            meta = entry.get("applicationMetaData") or entry
            title = (meta.get("inventionTitle") or "").strip()
            if not title:
                continue

            app_num = meta.get("applicationNumberText") or ""
            pub_num = meta.get("earliestPublicationNumber") or ""

            # Build a Google Patents link from publication or application number
            if pub_num:
                clean = pub_num.replace("-", "").replace("/", "")
                url = f"https://patents.google.com/patent/US{clean}"
            elif app_num:
                clean = app_num.replace("-", "").replace("/", "")
                url = f"https://patents.google.com/patent/US{clean}"
            else:
                continue

            if not self._passes_exclusions(title, topic.exclusions):
                continue

            filing_date = meta.get("filingDate") or ""

            # Date filter using filing date
            if since is not None and filing_date:
                try:
                    clean_date = filing_date.replace("-", "")[:8]
                    pub_dt = datetime.strptime(clean_date, "%Y%m%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass

            # Inventors from inventorBag
            inventors: list[str] = []
            for inv in meta.get("inventorBag") or []:
                name = ""
                if isinstance(inv, dict):
                    name = (inv.get("inventorNameText") or "").strip()
                elif isinstance(inv, str):
                    name = inv.strip()
                if name:
                    inventors.append(name)

            applicant = (meta.get("firstApplicantName") or "").strip()
            status = (meta.get("applicationStatusDescriptionText") or "").strip()

            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=filing_date,
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "application_number": app_num,
                        "publication_number": pub_num,
                        "inventors": inventors,
                        "applicant": applicant,
                        "status": status,
                        "filing_date": filing_date,
                    },
                )
            )
        return items
