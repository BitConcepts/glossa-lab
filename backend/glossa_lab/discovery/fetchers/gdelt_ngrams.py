"""GDELT Web Ngrams fetcher — the DEFAULT GDELT source (replaces DOC API).

Per GDELT's guidance during its Spanner migration (Kalev Leetaru, GDELT
Project — see ``specs/002-gdelt-ngrams-and-frontier-methods/``), the
legacy DOC 2.0 API is strained and researchers should use the temporary
Web Ngrams dataset instead:

* Every minute GDELT publishes two gzipped files for the minute ~2
  minutes ago under ``https://data.gdeltproject.org/gdeltv5/weblegacy/ngrams/``:
    - ``<YYYYMMDDHHMM00>.ngrams.txt.gz`` — tab-delimited
      ``DOCID \\t QUADGRAM \\t COUNT`` (4-word phrases; NO full text);
    - ``<YYYYMMDDHHMM00>.toc.json.gz`` — DOCID → url / title / date /
      language / image.
* Workflows should request the file from ~5 minutes ago and must
  accommodate GDELT's 15-minute heartbeat: files may exist only at
  15-minute marks, with gaps in between. This fetcher therefore walks
  back over candidate marks (bounded: 24 marks ≈ 6 h) and processes the
  ones that exist and have not been processed before.
* A persistent watermark in ``.glossa-state/gdelt_ngrams.json`` records
  the newest processed file stem so scheduler runs never rescan the
  same minutes.

Matching: topic keywords of 1–4 words match as contiguous token
sequences inside a quadgram (a 1-word keyword matches any quadgram
containing the word; shorter phrases match via quadgram reduction to
tri/bi/unigrams). Keywords longer than 4 words match on any of their
constituent 4-gram windows, or on reduced trigram/bigram windows.
Topic exclusions are applied to matched titles/quadgrams exactly like
the other fetchers. The DOC-API fetcher (``gdelt.py``) remains in the
tree but is opt-in only while GDELT's migration is in progress.
"""

from __future__ import annotations

import gzip
import io
import json
import logging
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from glossa_lab.discovery.fetchers.base import (
    _USER_AGENT,
    Fetcher,
    TopicProfile,
    run_in_thread,
)
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.gdelt_ngrams")

_BASE_URL = "https://data.gdeltproject.org/gdeltv5/weblegacy/ngrams/"
_MAX_MARKS = 24          # bounded walk-back: 24 heartbeat marks ≈ 6 h
_LAG_MINUTES = 5         # request the file from ~5 minutes ago
_DOWNLOAD_TIMEOUT = 90.0

_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


# ── State (watermark) ────────────────────────────────────────────────────

def _state_path() -> Path:
    # gdelt_ngrams.py is at backend/glossa_lab/discovery/fetchers/ → repo root is 5 up.
    return Path(__file__).resolve().parents[4] / ".glossa-state" / "gdelt_ngrams.json"


def _load_watermark() -> str:
    try:
        data = json.loads(_state_path().read_text(encoding="utf-8"))
        return str(data.get("last_processed_stem") or "")
    except Exception:  # noqa: BLE001 — missing/corrupt state = start fresh
        return ""


def _save_watermark(stem: str) -> None:
    try:
        path = _state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"last_processed_stem": stem}, indent=2), encoding="utf-8",
        )
    except Exception as exc:  # noqa: BLE001
        _log.warning("gdelt_ngrams: could not persist watermark: %s", exc)


# ── Candidate marks ──────────────────────────────────────────────────────

def stem_for(dt: datetime) -> str:
    """File stem (``YYYYMMDDHHMM00``) for a UTC minute."""
    return dt.astimezone(timezone.utc).strftime("%Y%m%d%H%M") + "00"


def stem_datetime(stem: str) -> datetime | None:
    try:
        return datetime.strptime(stem, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def candidate_stems(now: datetime, *, max_marks: int = _MAX_MARKS) -> list[str]:
    """Candidate file stems to try, newest first.

    Starts at ``now - 5 min`` (the exact minute, in case per-minute
    publishing is live), then walks the 15-minute heartbeat marks
    backwards, bounded at ``max_marks`` marks (≈6 h).
    """
    start = (now - timedelta(minutes=_LAG_MINUTES)).astimezone(timezone.utc)
    stems: list[str] = [stem_for(start)]
    mark = start.replace(minute=(start.minute // 15) * 15, second=0, microsecond=0)
    for _ in range(max_marks):
        s = stem_for(mark)
        if s not in stems:
            stems.append(s)
        mark -= timedelta(minutes=15)
    return stems


# ── Keyword → ngram patterns ─────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def build_patterns(topic: TopicProfile) -> dict[tuple[str, ...], str]:
    """Map matchable token n-grams → originating topic keyword.

    * 1–4-word keywords contribute their full token tuple (contiguous
      subsequence match inside a quadgram covers reduction to
      uni/bi/trigrams).
    * >4-word keywords contribute every constituent 4-gram window plus
      reduced trigram and bigram windows.
    """
    patterns: dict[tuple[str, ...], str] = {}
    for keyword in topic.keywords:
        words = tokenize(keyword)
        if not words:
            continue
        if len(words) <= 4:
            patterns.setdefault(tuple(words), keyword)
        else:
            for size in (4, 3, 2):
                for i in range(len(words) - size + 1):
                    patterns.setdefault(tuple(words[i:i + size]), keyword)
    return patterns


def match_keywords(tokens: list[str], patterns: dict[tuple[str, ...], str]) -> set[str]:
    """Return the topic keywords whose pattern occurs in *tokens*."""
    hits: set[str] = set()
    n = len(tokens)
    for size in (4, 3, 2, 1):
        if size > n:
            continue
        for i in range(n - size + 1):
            kw = patterns.get(tuple(tokens[i:i + size]))
            if kw:
                hits.add(kw)
    return hits


# ── File parsing ─────────────────────────────────────────────────────────

def parse_ngrams(text: str) -> Iterable[tuple[str, str, int]]:
    """Yield ``(docid, quadgram, count)`` from ngrams file text."""
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        docid, quadgram = parts[0].strip(), parts[1].strip()
        if not docid or not quadgram:
            continue
        try:
            count = int(parts[2])
        except ValueError:
            count = 1
        yield docid, quadgram, count


def _toc_field(entry: dict[str, Any], *names: str) -> str:
    lowered = {str(k).lower(): v for k, v in entry.items()}
    for name in names:
        value = lowered.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def parse_toc(text: str) -> dict[str, dict[str, str]]:
    """Parse toc.json content into ``{docid: {url,title,date,lang,img}}``.

    Accepts a JSON array, a JSON object keyed by docid, or JSON-lines —
    the field lookup is case-insensitive and tolerant of naming variants.
    """
    entries: list[tuple[str, dict[str, Any]]] = []
    stripped = text.strip()
    parsed: Any = None
    if stripped:
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            parsed = None
    if isinstance(parsed, list):
        for entry in parsed:
            if isinstance(entry, dict):
                entries.append((_toc_field(entry, "docid", "id", "doc_id"), entry))
    elif isinstance(parsed, dict):
        for docid, entry in parsed.items():
            if isinstance(entry, dict):
                entries.append((str(docid), entry))
    else:  # JSON-lines fallback
        for line in stripped.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict):
                entries.append((_toc_field(entry, "docid", "id", "doc_id"), entry))
    out: dict[str, dict[str, str]] = {}
    for docid, entry in entries:
        if not docid:
            docid = _toc_field(entry, "docid", "id", "doc_id")
        if not docid:
            continue
        out[docid] = {
            "url": _toc_field(entry, "url", "link"),
            "title": _toc_field(entry, "title", "headline"),
            "date": _toc_field(entry, "date", "published", "published_at", "datetime"),
            "lang": _toc_field(entry, "lang", "language"),
            "img": _toc_field(entry, "img", "image", "socialimage"),
        }
    return out


def _normalize_date(raw: str) -> str:
    """Best-effort normalize a TOC date to ``YYYY-MM-DD`` ('' if unknown)."""
    raw = (raw or "").strip()
    if not raw:
        return ""
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw[: len(fmt) + 2], fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    if len(raw) >= 10 and raw[4] == "-" and raw[7] == "-":
        return raw[:10]
    if len(raw) >= 8 and raw[:8].isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return raw


def items_from_pair(
    ngrams_text: str,
    toc: dict[str, dict[str, str]],
    topic: TopicProfile,
    *,
    stem: str = "",
) -> list[RawItem]:
    """Match one ngrams file against *topic* and build RawItems via the TOC."""
    patterns = build_patterns(topic)
    if not patterns:
        return []
    matched: dict[str, dict[str, Any]] = {}
    for docid, quadgram, count in parse_ngrams(ngrams_text):
        hits = match_keywords(tokenize(quadgram), patterns)
        if not hits:
            continue
        slot = matched.setdefault(
            docid, {"keywords": set(), "count": 0, "quadgrams": []},
        )
        slot["keywords"].update(hits)
        slot["count"] += count
        if len(slot["quadgrams"]) < 3:
            slot["quadgrams"].append(quadgram)

    items: list[RawItem] = []
    for docid, slot in matched.items():
        meta = toc.get(docid)
        if not meta:
            continue  # cannot build an item without url/title from the TOC
        title = (meta.get("title") or "").strip()
        url = (meta.get("url") or "").strip()
        if not title or not url:
            continue
        haystack = f"{title} {' '.join(slot['quadgrams'])}"
        if not Fetcher._passes_exclusions(haystack, topic.exclusions):
            continue
        items.append(
            RawItem(
                title=title,
                url=url,
                source="gdelt_ngrams",
                topic=topic.id,
                published_at=_normalize_date(meta.get("date", "")),
                lang=meta.get("lang") or (topic.languages or ["en"])[0],
                raw={
                    "docid": docid,
                    "matched_keywords": sorted(slot["keywords"]),
                    "match_count": slot["count"],
                    "quadgrams": slot["quadgrams"],
                    "ngrams_file": stem,
                    "img": meta.get("img", ""),
                },
            )
        )
    return items


# ── Download ─────────────────────────────────────────────────────────────

def _download_gz_text(url: str) -> str | None:
    """Download + gunzip *url*; None when the file does not exist (404)."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=_DOWNLOAD_TIMEOUT) as resp:
            payload = resp.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        _log.warning("gdelt_ngrams: HTTP %s for %s", exc.code, url)
        return None
    except Exception as exc:  # noqa: BLE001
        _log.warning("gdelt_ngrams: download failed for %s: %s", url, exc)
        return None
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload)) as gz:
            return gz.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        _log.warning("gdelt_ngrams: gunzip failed for %s: %s", url, exc)
        return None


def download_pair(stem: str) -> tuple[str, str] | None:
    """Download the (ngrams, toc) text pair for *stem*; None if absent."""
    ngrams = _download_gz_text(f"{_BASE_URL}{stem}.ngrams.txt.gz")
    if ngrams is None:
        return None
    toc = _download_gz_text(f"{_BASE_URL}{stem}.toc.json.gz")
    if toc is None:
        _log.warning("gdelt_ngrams: %s ngrams present but TOC missing", stem)
        return None
    return ngrams, toc


# ── Fetcher ──────────────────────────────────────────────────────────────

class GDELTNgramsFetcher(Fetcher):
    source = "gdelt_ngrams"
    requires = ()  # keyless
    rate_delay: float = 0.0

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_marks = int(opts.get("max_marks", _MAX_MARKS))
        now = datetime.now(timezone.utc)
        watermark = _load_watermark()
        since_floor = since.astimezone(timezone.utc) if since else None

        stems = [
            s for s in candidate_stems(now, max_marks=max_marks)
            if s > watermark
            and (since_floor is None or (stem_datetime(s) or now) >= since_floor)
        ]
        if not stems:
            _log.debug("gdelt_ngrams: nothing new since watermark %s", watermark)
            return []

        items: list[RawItem] = []
        # Oldest first so the watermark advances monotonically.
        for stem in reversed(stems):
            pair = await run_in_thread(download_pair, stem)
            if pair is None:
                continue  # heartbeat gap / not yet published — try next run
            ngrams_text, toc_text = pair
            toc = parse_toc(toc_text)
            items.extend(items_from_pair(ngrams_text, toc, topic, stem=stem))
            _save_watermark(stem)
            _log.info(
                "gdelt_ngrams: processed %s (%d TOC entries)", stem, len(toc),
            )
        return items
