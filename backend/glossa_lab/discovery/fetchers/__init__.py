"""Fetcher registry + orchestration.

Public surface:
* :func:`available_fetchers` — return the list of all registered fetchers
  (configured or not), along with their disabled-reason if a key is missing.
* :func:`run_topic`          — fetch one topic across the requested sources
  and persist results via :mod:`glossa_lab.discovery.store`.
* :func:`run_all`            — fetch every topic profile shipped with the
  package across every configured source.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery import store
from glossa_lab.discovery.fetchers.arxiv import ArxivFetcher
from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    list_topics,
    load_topic,
    now_utc,
    to_iso,
)
from glossa_lab.discovery.fetchers.academia import AcademiaFetcher
from glossa_lab.discovery.fetchers.brave import BraveFetcher
from glossa_lab.discovery.fetchers.crossref import CrossrefFetcher
from glossa_lab.discovery.fetchers.doaj import DOAJFetcher
from glossa_lab.discovery.fetchers.europepmc import EuropePMCFetcher
from glossa_lab.discovery.fetchers.gdelt import GDELTFetcher
from glossa_lab.discovery.fetchers.newsapi import NewsAPIFetcher
from glossa_lab.discovery.fetchers.openalex import OpenAlexFetcher
from glossa_lab.discovery.fetchers.pubmed import PubMedFetcher
from glossa_lab.discovery.fetchers.rss import RSSFetcher
from glossa_lab.discovery.fetchers.semanticscholar import SemanticScholarFetcher
from glossa_lab.discovery.fetchers.serpapi import SerpAPIFetcher
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers")

# Order matters: API-key sources first (most authoritative for news/scholar),
# keyless academic sources after.
_REGISTRY: tuple[type[Fetcher], ...] = (
    # API-key sources first — most authoritative for news/scholar.
    NewsAPIFetcher,
    BraveFetcher,
    SerpAPIFetcher,
    # Keyless academic / scientific sources — always on.
    OpenAlexFetcher,
    ArxivFetcher,
    CrossrefFetcher,
    PubMedFetcher,
    EuropePMCFetcher,
    DOAJFetcher,
    SemanticScholarFetcher,
    # Keyless news + general sources.
    GDELTFetcher,
    RSSFetcher,
    # Academia.edu — keyless metadata search; auth-gated download requires
    # the user to paste a session cookie in Settings → Discovery.
    AcademiaFetcher,
)


def available_fetchers() -> list[dict[str, object]]:
    """Return a status snapshot for each registered fetcher, including rate-limit health."""
    from glossa_lab.discovery.fetchers.base import get_rate_tracker  # noqa: PLC0415
    from glossa_lab.api.settings import get_key  # noqa: PLC0415
    tracker = get_rate_tracker()
    out: list[dict[str, object]] = []
    for cls in _REGISTRY:
        f = cls()
        rate_status = tracker.status(f.source)
        has_upgrade_key = bool(f.upgrade_key and get_key(f.upgrade_key))
        entry: dict[str, object] = {
            "source": f.source,
            "requires": list(f.requires),
            "configured": f.is_configured(),
            "disabled_reason": f.disabled_reason(),
            "rate_limit": rate_status,
            "has_upgrade_key": has_upgrade_key,
        }
        # If rate-limited and no upgrade key, tell the user how to fix it.
        if rate_status.get("rate_limited") and f.upgrade_key and not has_upgrade_key:
            entry["upgrade_hint"] = (
                f"Set '{f.upgrade_key}' in Settings → Discovery to remove rate limits."
            )
            if f.upgrade_url:
                entry["upgrade_url"] = f.upgrade_url
        out.append(entry)
    return out


def _build_fetchers(only_sources: Iterable[str] | None) -> list[Fetcher]:
    wanted = {s.lower() for s in only_sources} if only_sources else None
    instances: list[Fetcher] = []
    for cls in _REGISTRY:
        f = cls()
        if wanted is not None and f.source not in wanted:
            continue
        if not f.is_configured():
            _log.info(
                "fetcher %s skipped (%s)",
                f.source,
                f.disabled_reason() or "not configured",
            )
            continue
        instances.append(f)
    return instances


async def run_topic(
    topic: TopicProfile | str,
    *,
    since: datetime | None = None,
    only_sources: Iterable[str] | None = None,
) -> dict[str, object]:
    """Fetch a topic across all configured sources and persist results.

    Returns an aggregate summary suitable for embedding in a CLI report or
    in a Job result row.
    """
    profile = load_topic(topic) if isinstance(topic, str) else topic
    fetchers = _build_fetchers(only_sources)
    if not fetchers:
        return {
            "topic": profile.id,
            "since": to_iso(since),
            "fetchers": [],
            "fetched": 0,
            "new": 0,
            "merged": 0,
            "errors": 0,
        }

    fetched_at = to_iso(now_utc())
    fetched_total = 0
    new_total = 0
    merged_total = 0
    errors = 0
    per_source: list[dict[str, object]] = []

    from glossa_lab.discovery.fetchers.base import get_rate_tracker  # noqa: PLC0415
    _tracker = get_rate_tracker()

    async def _one(f: Fetcher) -> None:
        nonlocal fetched_total, new_total, merged_total, errors
        s_fetched = 0
        s_new = 0
        s_merged = 0
        s_error: str | None = None
        was_429 = False
        try:
            items = list(await f.fetch(profile, since=since))
            for item in items:
                created = await store.upsert_raw(item, fetched_at=fetched_at)
                s_fetched += 1
                if created:
                    s_new += 1
                else:
                    s_merged += 1
        except FetcherError as exc:
            s_error = f"FetcherError: {exc}"
            was_429 = "429" in str(exc) or "Too Many Requests" in str(exc)
        except Exception as exc:  # noqa: BLE001 — keep one bad source from killing the run
            s_error = f"{type(exc).__name__}: {exc}"
            _log.warning("fetcher %s raised %s", f.source, exc)
        # Record in rate-limit tracker
        _tracker.record_request(
            f.source, ok=s_error is None, was_429=was_429,
        )

        fetched_total += s_fetched
        new_total += s_new
        merged_total += s_merged
        if s_error:
            errors += 1
        per_source.append(
            {
                "source": f.source,
                "fetched": s_fetched,
                "new": s_new,
                "merged": s_merged,
                "error": s_error,
            }
        )

    # Split fetchers into parallel (no rate limit) and sequential (rate-limited)
    # groups. Rate-limited fetchers are run one at a time with an inter-call
    # delay so they don't immediately 429 when multiple topics fire.
    parallel = [f for f in fetchers if getattr(f, "rate_delay", 0) <= 0]
    sequential = [f for f in fetchers if getattr(f, "rate_delay", 0) > 0]
    await asyncio.gather(*[_one(f) for f in parallel])
    for i, f in enumerate(sequential):
        if i > 0:
            await asyncio.sleep(f.rate_delay)
        await _one(f)

    return {
        "topic": profile.id,
        "since": to_iso(since),
        "fetched_at": fetched_at,
        "fetchers": per_source,
        "fetched": fetched_total,
        "new": new_total,
        "merged": merged_total,
        "errors": errors,
    }


async def run_all(
    *,
    since: datetime | None = None,
    only_sources: Iterable[str] | None = None,
    only_topics: Iterable[str] | None = None,
) -> dict[str, object]:
    """Fetch every topic profile shipped with the package."""
    topics = list_topics()
    if only_topics is not None:
        wanted = {t.lower() for t in only_topics}
        topics = [t for t in topics if t.id.lower() in wanted]
    # Collect rate-limited fetchers' delays so we can insert inter-topic
    # cooldowns. This prevents 429s when multiple topics are queued.
    max_rate_delay = 0.0
    for cls in _REGISTRY:
        d = getattr(cls, "rate_delay", 0) or 0
        if d > max_rate_delay:
            max_rate_delay = d
    summaries = []
    for i, t in enumerate(topics):
        if i > 0 and max_rate_delay > 0:
            await asyncio.sleep(max_rate_delay)
        summaries.append(await run_topic(t, since=since, only_sources=only_sources))
    agg = {
        "topics_run": [t.id for t in topics],
        "results": summaries,
        "fetched": sum(int(s.get("fetched", 0)) for s in summaries),
        "new": sum(int(s.get("new", 0)) for s in summaries),
        "merged": sum(int(s.get("merged", 0)) for s in summaries),
        "errors": sum(int(s.get("errors", 0)) for s in summaries),
    }
    return agg


__all__ = [
    "available_fetchers",
    "run_topic",
    "run_all",
    "Fetcher",
    "TopicProfile",
    "FetcherError",
    "RawItem",
    "load_topic",
    "list_topics",
]
