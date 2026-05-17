"""Academia.edu RSS fetcher — topic-page RSS feeds (bypasses Cloudflare).

Academia.edu's public search page is protected by Cloudflare (HTTP 403).
However, the topic-category RSS feeds at:

    https://www.academia.edu/Documents/in/{Topic_Name}.rss

are served from a different path and bypass Cloudflare completely.
These feeds return the most recent papers uploaded to each topic category.

Topic names must match Academia.edu's URL slugs exactly (spaces → underscores
are fine, but capitalisation matters).  We map our topic keywords to a curated
list of known Academia.edu topic slugs, plus allow per-topic overrides in the
source_overrides.academia_rss section of a topic JSON.

Rate-limiting: Academia.edu has no documented rate limit for RSS feeds but we
use a conservative 30s inter-request delay to avoid any IP-level throttling.
"""

from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

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

_log = logging.getLogger("glossa_lab.discovery.fetchers.academia_rss")

_RSS_BASE = "https://www.academia.edu/Documents/in/{slug}.rss"

# ── Topic → Academia.edu slug map ─────────────────────────────────────────────
# Manually curated list matching Academia.edu's URL structure.
# Add more as needed; topic JSONs can override via source_overrides.academia_rss.slugs
_TOPIC_SLUG_MAP: dict[str, list[str]] = {
    "indus_script": [
        "Indus_Script",
        "Harappan_Civilization",
        "Indus_Valley_Civilization",
        "Indus_Valley_Script",
    ],
    "dravidian_linguistics": [
        "Dravidian_Languages",
        "Tamil_Linguistics",
        "Dravidian_Linguistics",
        "Old_Tamil",
    ],
    "ivc_archaeology": [
        "Indus_Valley_Civilization",
        "South_Asian_Archaeology",
        "Harappan_Civilization",
    ],
    "epigraphy": [
        "Epigraphy",
        "Ancient_Scripts",
        "Script_Decipherment",
    ],
    "ancient_near_east": [
        "Assyriology",
        "Ancient_Mesopotamia",
        "Cuneiform",
    ],
    "south_asian_archaeology": [
        "South_Asian_Archaeology",
        "Bronze_Age_South_Asia",
        "Harappan_Civilization",
    ],
}

_HEADERS = {
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "User-Agent": "Mozilla/5.0 (compatible; GlossaLab-RSS/0.1)",
}


def _parse_rss_items(xml_bytes: bytes, source_slug: str) -> list[dict]:
    """Parse an RSS 2.0/Atom feed and return a list of item dicts."""
    try:
        import feedparser  # noqa: PLC0415
        feed = feedparser.parse(xml_bytes)
        results = []
        for entry in feed.entries:
            title = (getattr(entry, "title", "") or "").strip()
            link = (getattr(entry, "link", "") or "").strip()
            if not title or not link:
                continue
            # Parse publication date
            pub_date = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    import time  # noqa: PLC0415
                    pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
                except Exception:  # noqa: BLE001
                    pass
            elif hasattr(entry, "published") and entry.published:
                try:
                    dt = parsedate_to_datetime(entry.published)
                    pub_date = dt.strftime("%Y-%m-%d")
                except Exception:  # noqa: BLE001
                    pass
            summary = (getattr(entry, "summary", "") or "").strip()
            # Extract authors — Academia RSS uses <author> or <dc:creator>
            authors: list[str] = []
            if hasattr(entry, "author"):
                authors = [entry.author.strip()] if entry.author.strip() else []
            elif hasattr(entry, "authors"):
                authors = [a.get("name", "").strip() for a in entry.authors if a.get("name")]
            results.append({
                "title": title,
                "url": link,
                "published": pub_date,
                "summary": summary[:1500],
                "authors": authors,
                "slug": source_slug,
            })
        return results
    except Exception as exc:  # noqa: BLE001
        _log.debug("RSS parse error for slug %s: %s", source_slug, exc)
        return []


class AcademiaRSSFetcher(Fetcher):
    """Academia.edu topic-category RSS fetcher.

    Uses the publicly accessible RSS feeds at academia.edu/Documents/in/<Topic>.rss
    which bypass the Cloudflare protection that blocks the search page.
    """
    source = "academia_rss"
    requires = ()  # keyless — RSS feeds are public
    rate_delay: float = 30.0  # conservative: 1 request / 30s per slug

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        import asyncio as _asyncio  # noqa: PLC0415

        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("academia_rss cooldown active — skipping (%.0fs remaining)", remaining)
            return []
        opts = topic.overrides_for(self.source)
        # Allow per-topic slug overrides
        slugs: list[str] = list(opts.get("slugs") or [])
        if not slugs:
            # Fall back to global map
            slugs = _TOPIC_SLUG_MAP.get(topic.id, [])
        if not slugs:
            # Construct a slug from the topic label as last resort
            slugs = [topic.label.replace(" ", "_")]

        max_per_slug = int(opts.get("max_per_slug", 15))
        all_items: list[RawItem] = []
        seen_urls: set[str] = set()

        for i, slug in enumerate(slugs[:4]):  # cap at 4 slugs per topic
            if i > 0:
                await _asyncio.sleep(self.rate_delay)  # polite delay between slugs
            url = _RSS_BASE.format(slug=slug)
            try:
                raw = await run_in_thread(
                    http_get_json, url, headers=_HEADERS, timeout=20.0,
                )
            except FetcherError as exc:
                _429_cooldown(str(exc), self.source)
                _log.debug("Academia RSS error for slug %s: %s", slug, exc)
                continue

            if not isinstance(raw, (bytes, bytearray)):
                _log.debug("Academia RSS: unexpected response type for slug %s", slug)
                continue

            entries = _parse_rss_items(raw, slug)
            for e in entries[:max_per_slug]:
                if e["url"] in seen_urls:
                    continue
                if not self._passes_exclusions(
                    f"{e['title']} {e['summary']}", topic.exclusions
                ):
                    continue
                if since is not None and e["published"]:
                    try:
                        pub_dt = datetime.strptime(e["published"][:10], "%Y-%m-%d")
                        if pub_dt < since.replace(tzinfo=None):
                            continue
                    except ValueError:
                        pass
                seen_urls.add(e["url"])
                all_items.append(RawItem(
                    title=e["title"],
                    url=e["url"],
                    source=self.source,
                    topic=topic.id,
                    published_at=e["published"],
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "summary": e["summary"],
                        "authors": e["authors"],
                        "academia_slug": e["slug"],
                    },
                ))

        return all_items
