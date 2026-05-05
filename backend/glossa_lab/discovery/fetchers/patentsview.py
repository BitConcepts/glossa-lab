"""PatentsView PatentSearch API fetcher.

Uses the PatentsView v1 API at https://search.patentsview.org/api/v1/patent/
to search granted US patents by keyword.

Requires a PatentsView API key (``patentsview_api_key`` in Settings).
Request a key at: https://patentsview-support.atlassian.net/servicedesk/customer/portals

Rate limit: 45 requests per minute.
"""

from __future__ import annotations

import asyncio
import json
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.patentsview")

_ENDPOINT = "https://search.patentsview.org/api/v1/patent/"
_FIELDS = [
    "patent_id", "patent_title", "patent_abstract",
    "patent_date", "patent_type",
    "inventors", "assignees",
]


class PatentsViewFetcher(Fetcher):
    source = "patentsview"
    requires = ("patentsview_api_key",)
    rate_delay: float = 1.5  # 45 req/min → ~1.33s; be conservative
    upgrade_key = ""
    upgrade_url = ""

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

        from glossa_lab.api.settings import get_key  # noqa: PLC0415
        api_key = get_key("patentsview_api_key")
        if not api_key:
            return []

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))

        # Build keyword query — OR-search across title + abstract
        query_terms = " ".join(topic.keywords[:10]) or topic.label
        q_dict: dict = {
            "_or": [
                {"_text_any": {"patent_title": query_terms}},
                {"_text_any": {"patent_abstract": query_terms}},
            ]
        }
        if since is not None:
            q_dict = {
                "_and": [
                    q_dict,
                    {"_gte": {"patent_date": since.strftime("%Y-%m-%d")}},
                ]
            }

        params = {
            "q": json.dumps(q_dict),
            "f": json.dumps(_FIELDS),
            "o": json.dumps({"size": min(max_results, 1000)}),
        }
        headers: dict[str, str] = {"X-Api-Key": api_key}

        try:
            data = await run_in_thread(
                http_get_json, _ENDPOINT, params=params, headers=headers, timeout=30.0,
            )
        except FetcherError as exc:
            _log.warning("PatentsView error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict) or data.get("error"):
            return []

        items: list[RawItem] = []
        for p in data.get("patents") or []:
            title = (p.get("patent_title") or "").strip()
            if not title:
                continue
            patent_id = p.get("patent_id") or ""
            url = f"https://patents.google.com/patent/US{patent_id}" if patent_id else ""
            if not url:
                continue
            abstract = (p.get("patent_abstract") or "")[:1500]
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            pub_date = p.get("patent_date") or ""
            if since is not None and pub_date:
                try:
                    pub_dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass
            # Nested inventor objects → flat name list
            inventors: list[str] = []
            for inv in p.get("inventors") or []:
                if isinstance(inv, dict):
                    first = (inv.get("inventor_name_first") or "").strip()
                    last = (inv.get("inventor_name_last") or "").strip()
                    name = f"{first} {last}".strip()
                    if name:
                        inventors.append(name)
            # Nested assignee objects → org names
            assignees: list[str] = []
            for asg in p.get("assignees") or []:
                if isinstance(asg, dict):
                    org = (asg.get("assignee_organization") or "").strip()
                    if org:
                        assignees.append(org)
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "patent_id": patent_id,
                        "abstract": abstract,
                        "patent_type": p.get("patent_type") or "",
                        "inventors": inventors,
                        "assignees": assignees,
                    },
                )
            )
        return items
