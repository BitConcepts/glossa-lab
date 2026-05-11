"""Common building blocks for discovery fetchers.

* :class:`TopicProfile` — typed view over the JSON files in
  ``glossa_lab/discovery/topics/``.
* :class:`Fetcher` — abstract base class every provider implements.
* :func:`http_get_json` — small synchronous JSON GET helper used by the
  fetchers; runs inside an executor when called from async code via
  :func:`run_in_thread`.
* :func:`build_query` — joins a topic's keywords into an OR-query usable by
  most search providers, with optional per-keyword quoting.
"""

from __future__ import annotations

import asyncio
import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers")

_TOPICS_DIR = Path(__file__).resolve().parent.parent / "topics"

# Default User-Agent — providers like CrossRef / arXiv prefer a contactable UA.
_USER_AGENT = "GlossaLab-DiscoveryEngine/0.1 (+https://github.com/layer1labs/glossa-lab)"


# ── Topic profiles ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class TopicProfile:
    """Declarative description of what a topic is interested in."""

    id: str
    label: str
    description: str
    keywords: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=lambda: ["en"])
    source_overrides: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TopicProfile":
        return cls(
            id=str(data["id"]),
            label=str(data.get("label", data["id"])),
            description=str(data.get("description", "")),
            keywords=list(data.get("keywords", [])),
            exclusions=list(data.get("exclusions", [])),
            languages=list(data.get("languages", ["en"])),
            source_overrides=dict(data.get("source_overrides", {}) or {}),
        )

    def overrides_for(self, source: str) -> dict[str, Any]:
        return dict(self.source_overrides.get(source, {}) or {})


def load_topic(topic_id: str) -> TopicProfile:
    """Load a single topic profile by id from the bundled JSON files."""
    path = _TOPICS_DIR / f"{topic_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Unknown topic id: {topic_id} (no file at {path})")
    return TopicProfile.from_dict(json.loads(path.read_text(encoding="utf-8")))


def list_topics() -> list[TopicProfile]:
    """Return every topic profile shipped with the package."""
    profiles: list[TopicProfile] = []
    if not _TOPICS_DIR.exists():
        return profiles
    for p in sorted(_TOPICS_DIR.glob("*.json")):
        try:
            profiles.append(TopicProfile.from_dict(json.loads(p.read_text(encoding="utf-8"))))
        except Exception as exc:  # noqa: BLE001
            _log.warning("Failed to load topic %s: %s", p.name, exc)
    return profiles


# ── Query helpers ───────────────────────────────────────────────────────────


def build_query(topic: TopicProfile, *, quote_phrases: bool = True) -> str:
    """Join topic keywords into a single OR-query string.

    Multi-word keywords are quoted by default so providers treat them as
    phrases. Exclusions are appended with `-`-prefix where the provider
    accepts that idiom (NewsAPI, Google variants).
    """
    def fmt(term: str, *, neg: bool = False) -> str:
        prefix = "-" if neg else ""
        if quote_phrases and " " in term:
            return f'{prefix}"{term}"'
        return f"{prefix}{term}"

    keyword_q = " OR ".join(fmt(k) for k in topic.keywords if k)
    if topic.exclusions:
        excl_q = " ".join(fmt(e, neg=True) for e in topic.exclusions if e)
        return f"({keyword_q}) {excl_q}".strip()
    return f"({keyword_q})" if keyword_q else ""


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def days_ago(days: int) -> datetime:
    return now_utc() - timedelta(days=days)


def to_iso(dt: datetime | None) -> str:
    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── HTTP ────────────────────────────────────────────────────────────────────


class FetcherError(RuntimeError):
    """Raised when a fetcher cannot complete a request."""


def _short_url(url: str) -> str:
    """Return just scheme+host+path, dropping query string (keeps logs readable)."""
    import re as _re  # noqa: PLC0415
    try:
        parsed = urllib.parse.urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    except Exception:  # noqa: BLE001
        return url[:80]


def _clean_body(raw: str) -> str:
    """Extract a terse human-readable string from an HTTP error body.

    Priority:
    1. HTML <title> tag (e.g. "504 Gateway Time-out")
    2. Strip all HTML tags, collapse whitespace
    3. Truncate to 120 chars
    """
    import re as _re  # noqa: PLC0415
    if not raw:
        return ""
    # Try HTML <title>
    m = _re.search(r"<title[^>]*>([^<]{1,120})</title>", raw, _re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Strip tags and collapse whitespace
    no_tags = _re.sub(r"<[^>]+>", " ", raw)
    clean = " ".join(no_tags.split())
    return clean[:120] if clean else raw[:120]


# Thread-local storage for rate-limit headers captured from the last response.
# Fetchers can read this after http_get_json returns to feed the tracker.
import threading as _threading
_last_rate_headers = _threading.local()


def get_last_rate_limit_info() -> dict[str, object] | None:
    """Return rate-limit info parsed from the last http_get_json response, if any."""
    return getattr(_last_rate_headers, "info", None)


def _parse_rate_headers(resp_headers: Any) -> dict[str, object] | None:
    """Extract X-RateLimit-* / RateLimit-* headers from an HTTP response."""
    limit = (
        resp_headers.get("X-RateLimit-Limit")
        or resp_headers.get("RateLimit-Limit")
        or resp_headers.get("x-ratelimit-limit")
    )
    remaining = (
        resp_headers.get("X-RateLimit-Remaining")
        or resp_headers.get("RateLimit-Remaining")
        or resp_headers.get("x-ratelimit-remaining")
    )
    reset = (
        resp_headers.get("X-RateLimit-Reset")
        or resp_headers.get("RateLimit-Reset")
        or resp_headers.get("Retry-After")
        or resp_headers.get("x-ratelimit-reset")
    )
    if limit is None and remaining is None and reset is None:
        return None
    info: dict[str, object] = {}
    if limit is not None:
        try: info["limit"] = int(limit)
        except (ValueError, TypeError): info["limit"] = str(limit)
    if remaining is not None:
        try: info["remaining"] = int(remaining)
        except (ValueError, TypeError): info["remaining"] = str(remaining)
    if reset is not None:
        try: info["reset"] = int(reset)
        except (ValueError, TypeError): info["reset"] = str(reset)
    return info


def http_get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: float = 15.0,
) -> Any:
    """Make a synchronous JSON GET request and return the parsed body.

    Also captures X-RateLimit-* headers from the response into thread-local
    storage; callers can read them via :func:`get_last_rate_limit_info`.

    Raises :class:`FetcherError` on any HTTP / decode failure so callers can
    handle individual provider failures without crashing the whole run.
    """
    _last_rate_headers.info = None  # reset
    full_url = url
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            sep = "&" if "?" in full_url else "?"
            full_url = f"{full_url}{sep}{urllib.parse.urlencode(clean, doseq=True)}"
    hdrs = {"Accept": "application/json", "User-Agent": _USER_AGENT}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(full_url, headers=hdrs, method="GET")
    # Allow disabling SSL verification via env var (for corporate proxies/VPNs)
    import os as _os, ssl as _ssl  # noqa: PLC0415,E401
    ssl_ctx: _ssl.SSLContext | None = None
    if _os.environ.get("GLOSSA_SSL_VERIFY", "1").strip() in ("0", "false", "no"):
        ssl_ctx = _ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = _ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            # Capture rate-limit headers before reading body.
            _last_rate_headers.info = _parse_rate_headers(resp.headers)
            raw = resp.read()
            if not raw:
                return {}
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "json" in ctype or raw[:1] in (b"{", b"["):
                return json.loads(raw)
            return raw
    except urllib.error.HTTPError as exc:
        # Still try to capture rate-limit headers from error responses.
        try:
            _last_rate_headers.info = _parse_rate_headers(exc.headers)
        except Exception:  # noqa: BLE001
            pass
        raw_body = ""
        try:
            raw_body = exc.read().decode("utf-8", errors="replace")[:2000]
        except Exception:  # noqa: BLE001
            pass
        clean = _clean_body(raw_body)
        short = _short_url(full_url)
        raise FetcherError(
            f"HTTP {exc.code} ({exc.reason or 'error'}) from {short}"
            + (f": {clean}" if clean else "")
        ) from exc
    except urllib.error.URLError as exc:
        reason = str(exc.reason) if exc.reason else "network error"
        raise FetcherError(f"{reason} — {_short_url(full_url)}") from exc
    except json.JSONDecodeError as exc:
        raise FetcherError(f"Invalid JSON from {_short_url(full_url)}: {exc.msg}") from exc


async def run_in_thread(fn, *args, **kwargs):
    """Run a blocking callable in the default thread executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))


# ── Rate-limit tracker ──────────────────────────────────────────────────────


class RateLimitTracker:
    """Per-source request counter and 429 tracker.

    Tracks total requests, successes, 429 errors, and last-request timestamp
    for each source. Exposed via ``/api/v1/discovery/sources`` so the frontend
    can show rate-limit health and suggest API key setup when needed.
    """

    def __init__(self) -> None:
        self._data: dict[str, dict[str, object]] = {}

    def record_request(
        self, source: str, *, ok: bool = True, was_429: bool = False,
        rate_limit_info: dict[str, object] | None = None,
    ) -> None:
        import time  # noqa: PLC0415
        if source not in self._data:
            self._data[source] = {
                "requests": 0, "success": 0, "errors_429": 0,
                "errors_other": 0, "last_request": 0.0,
                "limit": None, "remaining": None, "reset": None,
            }
        d = self._data[source]
        d["requests"] = int(d["requests"]) + 1  # type: ignore[arg-type]
        d["last_request"] = time.time()
        if was_429:
            d["errors_429"] = int(d["errors_429"]) + 1  # type: ignore[arg-type]
        elif not ok:
            d["errors_other"] = int(d["errors_other"]) + 1  # type: ignore[arg-type]
        else:
            d["success"] = int(d["success"]) + 1  # type: ignore[arg-type]
        # Persist rate-limit headers when the provider returns them.
        if rate_limit_info:
            if rate_limit_info.get("limit") is not None:
                d["limit"] = rate_limit_info["limit"]
            if rate_limit_info.get("remaining") is not None:
                d["remaining"] = rate_limit_info["remaining"]
            if rate_limit_info.get("reset") is not None:
                d["reset"] = rate_limit_info["reset"]

    def status(self, source: str) -> dict[str, object]:
        d = self._data.get(source, {})
        reqs = int(d.get("requests", 0))
        n429 = int(d.get("errors_429", 0))
        return {
            "requests": reqs,
            "success": int(d.get("success", 0)),
            "errors_429": n429,
            "errors_other": int(d.get("errors_other", 0)),
            "rate_limited": n429 > 0 and n429 >= reqs * 0.3,  # >30% of requests are 429
            "last_request": d.get("last_request", 0),
            # Provider-reported limits (from X-RateLimit-* headers)
            "limit": d.get("limit"),
            "remaining": d.get("remaining"),
            "reset": d.get("reset"),
        }

    def all_statuses(self) -> dict[str, dict[str, object]]:
        return {s: self.status(s) for s in self._data}


# Module-level singleton — shared across all fetcher instances.
_rate_tracker = RateLimitTracker()


def get_rate_tracker() -> RateLimitTracker:
    return _rate_tracker


# ── Fetcher contract ────────────────────────────────────────────────────────


class Fetcher(ABC):
    """Provider-specific fetcher.

    Subclasses must define :attr:`source` and may declare :attr:`requires`,
    a tuple of API-key names (matching :data:`KNOWN_KEYS` in the settings
    router) that must resolve to a non-empty value via
    ``glossa_lab.api.settings.get_key``.
    """

    source: str = ""
    requires: tuple[str, ...] = ()
    rate_delay: float = 0  # seconds to wait between successive calls across topics
    # Optional key name that upgrades rate limits when set.
    upgrade_key: str = ""
    upgrade_url: str = ""  # URL where users can get the key

    def __init__(self) -> None:
        if not self.source:
            raise TypeError(f"{type(self).__name__}.source must be set")

    # ── lifecycle ──
    def is_configured(self) -> bool:
        """Return True when every required API key resolves to a value."""
        # Local import keeps this module importable in stub-only test contexts.
        from glossa_lab.api.settings import get_key

        for key_name in self.requires:
            if not get_key(key_name):
                return False
        return True

    def disabled_reason(self) -> str:
        from glossa_lab.api.settings import get_key

        missing = [k for k in self.requires if not get_key(k)]
        if missing:
            return f"missing key(s): {', '.join(missing)}"
        return ""

    # ── work ──
    @abstractmethod
    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        """Fetch items matching *topic* published since *since*."""

    # ── helpers for subclasses ──
    @staticmethod
    def _passes_exclusions(text: str, exclusions: list[str]) -> bool:
        if not exclusions or not text:
            return True
        haystack = text.lower()
        return not any(e.lower() in haystack for e in exclusions if e)
