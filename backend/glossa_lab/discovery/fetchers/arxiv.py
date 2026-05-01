"""arXiv fetcher (https://export.arxiv.org/api/query).

Keyless. arXiv returns Atom XML; we parse it with the stdlib ElementTree.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.arxiv")

_ENDPOINT = "https://export.arxiv.org/api/query"
_ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def _build_search_query(topic: TopicProfile, extra: str = "") -> str:
    """Compose an arXiv `search_query` from topic keywords."""
    # arXiv supports OR over title-search clauses; quote multi-word phrases.
    clauses = []
    for kw in topic.keywords[:6]:
        if " " in kw:
            clauses.append(f'ti:"{kw}"')
        else:
            clauses.append(f"ti:{kw}")
    base = " OR ".join(clauses) if clauses else f"all:{topic.label}"
    if extra:
        base = f"({base}) AND ({extra})"
    return base


class ArxivFetcher(Fetcher):
    source = "arxiv"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        params = {
            "search_query": _build_search_query(topic, str(opts.get("search_query_extra", ""))),
            "max_results": int(opts.get("max_results", 25)),
            "sortBy": opts.get("sort_by", "submittedDate"),
            "sortOrder": opts.get("sort_order", "descending"),
        }
        try:
            raw = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("arXiv error for topic %s: %s", topic.id, exc)
            return []

        if not isinstance(raw, (bytes, bytearray)):
            _log.warning("arXiv: unexpected payload type %s", type(raw).__name__)
            return []

        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            _log.warning("arXiv: XML parse error: %s", exc)
            return []

        items: list[RawItem] = []
        for entry in root.findall("a:entry", _ATOM_NS):
            title_el = entry.find("a:title", _ATOM_NS)
            link_el = entry.find("a:id", _ATOM_NS)
            published_el = entry.find("a:published", _ATOM_NS)
            summary_el = entry.find("a:summary", _ATOM_NS)
            title = (title_el.text or "").strip() if title_el is not None else ""
            url = (link_el.text or "").strip() if link_el is not None else ""
            if not title or not url:
                continue
            published = (published_el.text or "").strip() if published_el is not None else ""
            if since is not None and published:
                try:
                    pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    if pub_dt < since:
                        continue
                except ValueError:
                    pass
            summary = (summary_el.text or "").strip() if summary_el is not None else ""
            if not self._passes_exclusions(f"{title} {summary}", topic.exclusions):
                continue
            authors = [
                (a.findtext("a:name", default="", namespaces=_ATOM_NS) or "").strip()
                for a in entry.findall("a:author", _ATOM_NS)
            ]
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=published,
                    lang="en",
                    raw={
                        "summary": summary[:1500],
                        "authors": [a for a in authors if a],
                    },
                )
            )
        return items
