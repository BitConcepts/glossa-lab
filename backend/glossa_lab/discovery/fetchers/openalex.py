"""OpenAlex fetcher (https://api.openalex.org/works).

Keyless. Uses the ``search`` parameter for keyword matching and
``from_publication_date`` for the since window.

When ``openalex_email`` is set in Settings, it is sent as a ``mailto``
query parameter, moving requests into OpenAlex's "polite pool" for
higher priority and faster responses.
"""

from __future__ import annotations

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

_log = logging.getLogger("glossa_lab.discovery.fetchers.openalex")

_ENDPOINT = "https://api.openalex.org/works"


def _reconstruct_abstract(inv_idx: dict[str, list[int]] | None) -> str:
    """OpenAlex stores abstracts as inverted indices; rebuild a plain string."""
    if not inv_idx:
        return ""
    positions: list[tuple[int, str]] = []
    for word, indices in inv_idx.items():
        for i in indices:
            positions.append((int(i), word))
    positions.sort()
    return " ".join(w for _, w in positions)


class OpenAlexFetcher(Fetcher):
    source = "openalex"
    requires = ()  # keyless
    upgrade_key = "openalex_email"
    upgrade_url = "https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication"

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        # OpenAlex's "search" param accepts free text — join keywords with spaces.
        query = " ".join(topic.keywords[:8]) or topic.label
        params: dict[str, object] = {
            "search": query,
            "per-page": int(opts.get("per_page", 25)),
            "sort": opts.get("sort", "publication_date:desc"),
        }
        if since is not None:
            params["filter"] = f"from_publication_date:{since.strftime('%Y-%m-%d')}"
        # Topic JSON can supply additional filters under source_overrides.openalex.filter.
        if opts.get("filter"):
            existing = params.get("filter", "")
            params["filter"] = (existing + "," + str(opts["filter"])).lstrip(",")

        # If the user has set an email for OpenAlex, include it as the
        # "mailto" param to join the polite pool (faster, priority access).
        from glossa_lab.api.settings import get_key  # noqa: PLC0415
        oa_email = get_key("openalex_email")
        if oa_email:
            params["mailto"] = oa_email
        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=15.0)
        except FetcherError as exc:
            _log.warning("OpenAlex error for topic %s: %s", topic.id, exc)
            return []

        items: list[RawItem] = []
        for w in (data or {}).get("results", []) or []:
            title = (w.get("title") or w.get("display_name") or "").strip()
            url = (w.get("doi") or w.get("id") or "").strip()
            if not title or not url:
                continue
            abstract = _reconstruct_abstract(w.get("abstract_inverted_index"))
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            authors = [
                (a.get("author") or {}).get("display_name", "")
                for a in (w.get("authorships") or [])
            ]
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=w.get("publication_date") or "",
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "abstract": abstract[:1500],  # truncate for storage size
                        "authors": [a for a in authors if a],
                        "cited_by_count": w.get("cited_by_count"),
                        "host_venue": (w.get("primary_location") or {}).get("source"),
                        "openalex_id": w.get("id"),
                    },
                )
            )
        return items
