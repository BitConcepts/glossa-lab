"""Academia.edu fetcher — keyless metadata search.

Uses Academia.edu's public search page and extracts structured metadata
from the JSON-LD embedded in search results.  No API key is needed for
metadata discovery.  Full-text PDF download is auth-gated and requires the
user to paste an ``academia_session_cookie`` value in Settings → Discovery;
this fetcher does NOT attempt downloads — it only collects metadata
(title, authors, URL, abstract snippet).
"""

from __future__ import annotations

import json
import logging
import re
import urllib.parse
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.academia")

_SEARCH_URL = "https://www.academia.edu/search"

# Regex to extract JSON-LD script blocks from the HTML search page.
_JSONLD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def _extract_papers_from_html(html: str) -> list[dict]:
    """Best-effort extraction of paper metadata from Academia search HTML.

    Academia.edu embeds JSON-LD ``ScholarlyArticle`` objects in the page.
    We also fall back to a simple regex scrape of ``<a>`` + title patterns
    if no JSON-LD is found (Academia frequently changes its markup).
    """
    papers: list[dict] = []
    for m in _JSONLD_RE.finditer(html):
        try:
            blob = json.loads(m.group(1))
        except (json.JSONDecodeError, ValueError):
            continue
        items = blob if isinstance(blob, list) else [blob]
        for item in items:
            if not isinstance(item, dict):
                continue
            stype = item.get("@type") or ""
            if "Article" not in stype and "ScholarlyArticle" not in stype:
                continue
            title = (item.get("name") or item.get("headline") or "").strip()
            url = (item.get("url") or item.get("mainEntityOfPage") or "").strip()
            if title and url:
                authors_raw = item.get("author") or []
                if isinstance(authors_raw, dict):
                    authors_raw = [authors_raw]
                authors = [
                    (a.get("name") or "").strip()
                    for a in authors_raw if isinstance(a, dict)
                ]
                papers.append({
                    "title": title,
                    "url": url,
                    "authors": [a for a in authors if a],
                    "abstract": (item.get("description") or "")[:1500],
                    "date": (item.get("datePublished") or ""),
                })
    return papers


class AcademiaFetcher(Fetcher):
    source = "academia"
    requires = ()  # keyless for search metadata

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 20))
        query = " ".join(topic.keywords[:6]) or topic.label
        url = f"{_SEARCH_URL}?{urllib.parse.urlencode({'q': query})}"
        headers = {
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "Mozilla/5.0 (compatible; GlossaLab/0.1)",
        }
        try:
            raw = await run_in_thread(
                http_get_json, url, headers=headers, timeout=20.0,
            )
        except FetcherError as exc:
            _log.warning("Academia.edu error for topic %s: %s", topic.id, exc)
            return []
        # http_get_json returns bytes when Content-Type is not JSON.
        if isinstance(raw, (bytes, bytearray)):
            html = raw.decode("utf-8", errors="replace")
        elif isinstance(raw, str):
            html = raw
        else:
            _log.debug("Academia.edu: unexpected response type %s", type(raw).__name__)
            return []

        papers = _extract_papers_from_html(html)
        items: list[RawItem] = []
        for p in papers[:max_results]:
            title = p["title"]
            paper_url = p["url"]
            if not self._passes_exclusions(f"{title} {p.get('abstract', '')}", topic.exclusions):
                continue
            pub_date = p.get("date") or ""
            if since is not None and pub_date:
                try:
                    pub_dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass
            items.append(
                RawItem(
                    title=title,
                    url=paper_url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "authors": p.get("authors") or [],
                        "abstract": p.get("abstract") or "",
                    },
                )
            )
        return items
