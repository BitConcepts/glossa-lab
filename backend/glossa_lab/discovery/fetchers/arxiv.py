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


# ── Global arXiv rate tracking ────────────────────────────────────────────────
# arXiv enforces a per-IP rate limit across ALL requests (not just per topic).
# After a 429 we back off the ENTIRE arXiv pipeline for a cooling period.
import threading as _threading  # noqa: E402
import time as _time_mod  # noqa: E402

_arxiv_lock = _threading.Lock()
# Initialised to now() so the FIRST request after any process restart waits the
# full inter-request delay.  A restart resets the in-memory cooldown state but
# arXiv's servers still remember our IP from the previous session.  Forcing a
# delay on the first post-restart request avoids immediately tripping any
# lingering IP-level ban from the previous run.
_arxiv_last_attempt_mono: float = _time_mod.monotonic()
_arxiv_cooldown_until: float = 0.0
_ARXIV_INTER_REQUEST_SECS: float = 30.0   # 30s between requests — arXiv enforces 3s but shared IPs need far more margin


def _arxiv_cb_trip(cooldown: float) -> None:
    global _arxiv_cooldown_until  # noqa: PLW0603
    _arxiv_cooldown_until = _time_mod.monotonic() + cooldown
    _log.warning(
        "arXiv rate-limit cooldown: pausing all arXiv requests for %.0fs", cooldown
    )


def _arxiv_cb_is_cooling() -> tuple[bool, float]:
    """Returns (is_cooling, seconds_remaining)."""
    remaining = _arxiv_cooldown_until - _time_mod.monotonic()
    return remaining > 0, max(0.0, remaining)


class ArxivFetcher(Fetcher):
    source = "arxiv"
    requires = ()  # keyless
    # arXiv policy (2024-2025): no more than 1 request per 3 seconds.
    # We use 20s as our polite inter-request delay to avoid IP-level bans.
    rate_delay: float = 15.0
    _MAX_RETRIES: int = 0     # do not retry inside a scheduler tick; cooldown skips later topics
    _RETRY_BASE: float = 900.0  # 15m cooldown on 429 when no Retry-After is available
    _TIMEOUT_COOLDOWN: float = 300.0  # 5m cooldown on network/read timeouts (was 10m — too long)

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        global _arxiv_last_attempt_mono  # noqa: PLW0603 — must be declared before first read
        import asyncio as _asyncio  # noqa: PLC0415

        # Check global cooldown before attempting anything
        cooling, remaining = _arxiv_cb_is_cooling()
        if cooling:
            _log.debug(
                "arXiv cooldown active for topic %s — skipping (%.0fs remaining)",
                topic.id, remaining,
            )
            return []

        opts = topic.overrides_for(self.source)
        params = {
            "search_query": _build_search_query(topic, str(opts.get("search_query_extra", ""))),
            "max_results": int(opts.get("max_results", 25)),
            "sortBy": opts.get("sort_by", "submittedDate"),
            "sortOrder": opts.get("sort_order", "descending"),
        }
        raw = None
        for attempt in range(1 + self._MAX_RETRIES):
            # Reserve a request slot and sleep asynchronously outside the lock.
            with _arxiv_lock:
                now_mono = _time_mod.monotonic()
                elapsed = now_mono - _arxiv_last_attempt_mono
                wait_secs = max(0.0, _ARXIV_INTER_REQUEST_SECS - elapsed)
                _arxiv_last_attempt_mono = now_mono + wait_secs
            if wait_secs > 0:
                await _asyncio.sleep(wait_secs)

            try:
                raw = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=30.0)
                break
            except FetcherError as exc:
                err_str = str(exc)
                is_429 = "429" in err_str or "rate exceeded" in err_str.lower()
                is_timeout = "timed out" in err_str.lower() or "timeout" in err_str.lower()
                is_retryable = (is_429 or is_timeout) and attempt < self._MAX_RETRIES
                if is_429:
                    # Trip the global cooldown immediately — ALL topics must back off
                    import re as _re  # noqa: PLC0415
                    ra_match = _re.search(r"Retry-After:\s*(\d+)", err_str)
                    backoff = int(ra_match.group(1)) + 5 if ra_match else self._RETRY_BASE
                    _arxiv_cb_trip(backoff)
                    _log.warning(
                        "arXiv 429 for topic %s (attempt %d/%d) — "
                        "global cooldown set to %.0fs",
                        topic.id, attempt + 1, self._MAX_RETRIES + 1, backoff,
                    )
                    if is_retryable:
                        await _asyncio.sleep(backoff)
                        continue
                    return []
                if is_timeout:
                    _arxiv_cb_trip(self._TIMEOUT_COOLDOWN)
                    _log.warning(
                        "arXiv timeout for topic %s — global cooldown set to %.0fs",
                        topic.id, self._TIMEOUT_COOLDOWN,
                    )
                    return []
                if is_retryable:
                    await _asyncio.sleep(15.0)
                    continue
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
