"""RSS / Atom feed fetcher.

Keyless. Topic profiles can specify a list of feed URLs under
``source_overrides.rss.feeds`` — each is fetched and parsed with stdlib
``xml.etree.ElementTree``.  If no feeds are specified for a topic the
fetcher returns an empty result without error.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.rss")

_ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def _parse_rfc2822(s: str) -> datetime | None:
    """Try to parse an RFC 2822 date (common in RSS <pubDate>)."""
    try:
        return parsedate_to_datetime(s)
    except Exception:  # noqa: BLE001
        return None


def _parse_iso(s: str) -> datetime | None:
    """Try to parse an ISO-8601 / Atom date."""
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:  # noqa: BLE001
        return None


def _parse_feed(raw: bytes, *, source_label: str) -> list[dict[str, str]]:
    """Parse an RSS 2.0 or Atom feed into a flat list of dicts."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _log.warning("RSS: XML parse error from %s: %s", source_label, exc)
        return []
    entries: list[dict[str, str]] = []

    # RSS 2.0: <channel><item>…</item></channel>
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = (item.findtext("description") or "").strip()
        if title and link:
            entries.append({"title": title, "url": link, "date": pub_date, "summary": description})

    # Atom: <entry>…</entry>
    for entry in root.findall("a:entry", _ATOM_NS):
        title = (entry.findtext("a:title", default="", namespaces=_ATOM_NS) or "").strip()
        link_el = entry.find("a:link[@rel='alternate']", _ATOM_NS) or entry.find("a:link", _ATOM_NS)
        link = (link_el.get("href") or "").strip() if link_el is not None else ""
        pub = (entry.findtext("a:published", default="", namespaces=_ATOM_NS)
               or entry.findtext("a:updated", default="", namespaces=_ATOM_NS) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=_ATOM_NS) or "").strip()
        if title and link:
            entries.append({"title": title, "url": link, "date": pub, "summary": summary})

    return entries


class RSSFetcher(Fetcher):
    source = "rss"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        feeds: list[str] = opts.get("feeds") or []
        if not feeds:
            return []

        cooling, remaining = source_is_cooling(self.source)
        if cooling:
            _log.debug("rss cooldown active — skipping (%.0fs remaining)", remaining)
            return []

        items: list[RawItem] = []
        for feed_url in feeds:
            try:
                raw = await run_in_thread(http_get_json, feed_url, timeout=20.0)
            except FetcherError as exc:
                err_str = str(exc)
                if _429_cooldown(err_str, self.source):
                    # Rate-limited — stop processing remaining feeds for this topic.
                    break
                _log.warning("RSS: error fetching %s for topic %s: %s", feed_url, topic.id, exc)
                continue
            if not isinstance(raw, (bytes, bytearray)):
                _log.debug("RSS: non-bytes payload from %s (type=%s)", feed_url, type(raw).__name__)
                continue
            for e in _parse_feed(raw, source_label=feed_url):
                title = e["title"]
                url = e["url"]
                date_str = e.get("date") or ""
                summary = e.get("summary") or ""
                if not self._passes_exclusions(f"{title} {summary}", topic.exclusions):
                    continue
                # Filter by since
                if since is not None and date_str:
                    dt = _parse_rfc2822(date_str) or _parse_iso(date_str)
                    if dt is not None and dt.replace(tzinfo=None) < since.replace(tzinfo=None):
                        continue
                # Normalise date to ISO
                pub_iso = ""
                if date_str:
                    dt = _parse_rfc2822(date_str) or _parse_iso(date_str)
                    if dt is not None:
                        pub_iso = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    else:
                        pub_iso = date_str
                items.append(
                    RawItem(
                        title=title,
                        url=url,
                        source=self.source,
                        topic=topic.id,
                        published_at=pub_iso,
                        lang=(topic.languages or ["en"])[0],
                        raw={
                            "feed_url": feed_url,
                            "summary": summary[:1500],
                        },
                    )
                )
        return items
