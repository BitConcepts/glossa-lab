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


def http_get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: float = 15.0,
) -> Any:
    """Make a synchronous JSON GET request and return the parsed body.

    Raises :class:`FetcherError` on any HTTP / decode failure so callers can
    handle individual provider failures without crashing the whole run.
    """
    full_url = url
    if params:
        # Drop None values so callers can skip optional params idiomatically.
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            sep = "&" if "?" in full_url else "?"
            full_url = f"{full_url}{sep}{urllib.parse.urlencode(clean, doseq=True)}"
    hdrs = {"Accept": "application/json", "User-Agent": _USER_AGENT}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(full_url, headers=hdrs, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return {}
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "json" in ctype or raw[:1] in (b"{", b"["):
                return json.loads(raw)
            # Some providers (arXiv) return XML; let the caller decide.
            return raw
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:  # noqa: BLE001
            pass
        raise FetcherError(f"HTTP {exc.code} from {full_url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise FetcherError(f"URLError from {full_url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise FetcherError(f"Bad JSON from {full_url}: {exc}") from exc


async def run_in_thread(fn, *args, **kwargs):
    """Run a blocking callable in the default thread executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))


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
