"""GDELT DOC 2.0 API fetcher (https://api.gdeltproject.org/api/v2/doc/doc).

Keyless. Provides global news monitoring — articles from thousands of
worldwide news outlets, useful as a complement to the news-API-gated sources.

Rate-limiting strategy:
  • Global ``asyncio.Lock`` so only one coroutine hits GDELT at a time.
  • 60 s inter-request delay (12× the documented 5 s minimum).
  • **Circuit breaker**: if GDELT returns 429, all requests are skipped for
    an escalating cooldown (1 h → 2 h → 4 h → 8 h, max 24 h).  A successful
    request resets the breaker.  This prevents retry storms from worsening
    an IP-level penalty that GDELT applies after sustained over-use.
"""

from __future__ import annotations

import asyncio
import logging
import time as _time_mod
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery.fetchers.base import (
    Fetcher,
    FetcherError,
    TopicProfile,
    build_query,
    http_get_json,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.gdelt")

_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"

# ── Global GDELT serialisation ──────────────────────────────────────────────
_gdelt_lock = asyncio.Lock()
_last_request_mono: float = _time_mod.monotonic()


def _update_last_request() -> None:
    global _last_request_mono  # noqa: PLW0603
    _last_request_mono = _time_mod.monotonic()


async def _wait_for_rate_delay(delay: float) -> None:
    elapsed = _time_mod.monotonic() - _last_request_mono
    remaining = delay - elapsed
    if remaining > 0:
        _log.debug("GDELT rate-delay: sleeping %.1fs", remaining)
        await asyncio.sleep(remaining)


# ── Circuit breaker ───────────────────────────────────────────────────
# After a 429, all GDELT requests are skipped for ``_cb_cooldown_secs``.
# Each consecutive 429 doubles the cooldown (1 h → 2 h → … → 24 h max).
# A successful request resets everything.
_CB_INITIAL: float = 3600.0       # 1 hour
_CB_MAX: float = 86400.0          # 24 hours
_cb_cooldown_secs: float = 0.0    # 0 = breaker closed (healthy)
_cb_tripped_at: float = 0.0       # monotonic time of last trip
_cb_consecutive_429: int = 0


def _cb_is_open() -> bool:
    """True when the circuit breaker is open (requests should be skipped)."""
    if _cb_cooldown_secs <= 0:
        return False
    elapsed = _time_mod.monotonic() - _cb_tripped_at
    if elapsed >= _cb_cooldown_secs:
        # Cooldown expired — allow one probe request.
        return False
    return True


def _cb_trip() -> None:
    """Record a 429 and escalate the cooldown."""
    global _cb_cooldown_secs, _cb_tripped_at, _cb_consecutive_429  # noqa: PLW0603
    _cb_consecutive_429 += 1
    _cb_cooldown_secs = min(_CB_MAX, _CB_INITIAL * (2 ** (_cb_consecutive_429 - 1)))
    _cb_tripped_at = _time_mod.monotonic()
    _log.warning(
        "GDELT circuit breaker OPEN — skipping all requests for %.0f s "
        "(consecutive 429s: %d)",
        _cb_cooldown_secs, _cb_consecutive_429,
    )


def _cb_reset() -> None:
    """A successful request resets the breaker."""
    global _cb_cooldown_secs, _cb_tripped_at, _cb_consecutive_429  # noqa: PLW0603
    if _cb_consecutive_429 > 0:
        _log.info("GDELT circuit breaker CLOSED — successful request after %d consecutive 429s", _cb_consecutive_429)
    _cb_cooldown_secs = 0.0
    _cb_tripped_at = 0.0
    _cb_consecutive_429 = 0


class GDELTFetcher(Fetcher):
    source = "gdelt"
    requires = ()  # keyless
    rate_delay: float = 60.0
    _MAX_RETRIES: int = 3  # retry up to 3 times with exponential backoff before tripping
    # GDELT explicitly requires ≥5s between requests; we use 12s to be safe.
    # Exponential: 12s → 24s → 48s (all well above the 5s minimum).
    _RETRY_BASE: float = 12.0

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        # ── Circuit breaker check ─────────────────────────────────────
        if _cb_is_open():
            remaining = _cb_cooldown_secs - (_time_mod.monotonic() - _cb_tripped_at)
            _log.debug(
                "GDELT circuit breaker open — skipping topic %s (%.0fs remaining)",
                topic.id, remaining,
            )
            return []

        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = build_query(topic, quote_phrases=True) or topic.label
        params: dict[str, object] = {
            "query": query,
            "mode": opts.get("mode", "ArtList"),
            "maxrecords": min(max_results, 250),
            "format": "json",
            "sort": opts.get("sort", "DateDesc"),
        }
        if since is not None:
            params["startdatetime"] = since.strftime("%Y%m%d%H%M%S")

        data: dict | None = None
        for attempt in range(1 + self._MAX_RETRIES):
            async with _gdelt_lock:
                await _wait_for_rate_delay(self.rate_delay)
                _update_last_request()
                try:
                    data = await run_in_thread(
                        http_get_json, _ENDPOINT, params=params, timeout=30.0,
                    )
                    _cb_reset()  # success — reset breaker
                    break
                except FetcherError as exc:
                    err_str = str(exc)
                    is_429 = "429" in err_str
                    is_retryable = (
                        is_429
                        or "timed out" in err_str.lower()
                        or "ssl" in err_str.lower()
                        or "urlopen error" in err_str.lower()
                        or "urlerror" in err_str.lower()
                        or "winerror" in err_str.lower()
                        or "connection" in err_str.lower()
                    )
                    if is_retryable and attempt < self._MAX_RETRIES:
                        backoff = self._RETRY_BASE * (2 ** attempt)  # 12s → 24s → 48s
                        # Log 429 retries at DEBUG — they are managed by the
                        # rate-delay + circuit breaker and are not errors.
                        _log.debug(
                            "GDELT %s for topic %s (attempt %d/%d), "
                            "retrying in %.1fs",
                            "429" if is_429 else "transient-error", topic.id,
                            attempt + 1, self._MAX_RETRIES, backoff,
                        )
                        _update_last_request()
                        # Release lock, backoff, then loop to retry.
                        break  # exits the `async with _gdelt_lock` block
                    elif is_429 or is_retryable:
                        # Exhausted retries — trip the circuit breaker.
                        _cb_trip()
                        _log.warning(
                            "GDELT %s for topic %s — exhausted %d retries, breaker tripped",
                            "429" if is_429 else "error", topic.id, self._MAX_RETRIES,
                        )
                        return []
                    else:
                        _log.warning("GDELT non-retryable error for topic %s: %s", topic.id, exc)
                        return []
            # Backoff sleep outside lock (only for non-429 retryable errors).
            if data is None and attempt < self._MAX_RETRIES:
                backoff = self._RETRY_BASE * (attempt + 1)
                await asyncio.sleep(backoff)
                _update_last_request()

        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for a in data.get("articles") or []:
            title = (a.get("title") or "").strip()
            url = (a.get("url") or "").strip()
            if not title or not url:
                continue
            if not self._passes_exclusions(title, topic.exclusions):
                continue
            # seendate is "YYYYMMDDTHHmmssZ"
            seen = a.get("seendate") or ""
            pub_date = ""
            if seen and len(seen) >= 8:
                try:
                    pub_date = datetime.strptime(seen[:8], "%Y%m%d").strftime("%Y-%m-%d")
                except ValueError:
                    pub_date = seen
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=pub_date,
                    lang=a.get("language") or (topic.languages or ["en"])[0],
                    raw={
                        "domain": a.get("domain") or "",
                        "socialimage": a.get("socialimage") or "",
                        "seendate": seen,
                    },
                )
            )
        return items
