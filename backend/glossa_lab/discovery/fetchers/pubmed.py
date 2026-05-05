"""PubMed E-utilities fetcher (https://eutils.ncbi.nlm.nih.gov/entrez/eutils/).

Keyless. Two-step protocol:
  1. esearch.fcgi  → list of PMIDs matching the topic.
  2. esummary.fcgi → metadata for each PMID (title, authors, journal, date).
We assemble RawItems pointing at the canonical pubmed.ncbi.nlm.nih.gov URL.
"""

from __future__ import annotations

import logging
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.pubmed")

_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


class PubMedFetcher(Fetcher):
    source = "pubmed"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        # PubMed's relevance ranking does well with simple OR-keyword queries.
        query = build_query(topic, quote_phrases=True) or topic.label
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": opts.get("sort", "date"),
        }
        try:
            search = await run_in_thread(http_get_json, _ESEARCH, params=params, timeout=20.0)
        except FetcherError as exc:
            _log.warning("PubMed esearch error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(search, dict):
            return []
        ids = ((search.get("esearchresult") or {}).get("idlist") or [])
        if not ids:
            return []

        sum_params = {
            "db": "pubmed",
            "id": ",".join(str(i) for i in ids),
            "retmode": "json",
        }
        try:
            summary = await run_in_thread(http_get_json, _ESUMMARY, params=sum_params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("PubMed esummary error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(summary, dict):
            return []
        result = summary.get("result") or {}

        items: list[RawItem] = []
        for pmid in ids:
            entry = result.get(str(pmid))
            if not isinstance(entry, dict):
                continue
            title = (entry.get("title") or "").strip()
            if not title:
                continue
            published = (entry.get("pubdate") or entry.get("epubdate") or "").strip()
            # Filter by `since` when we can parse a year-month-day prefix.
            if since is not None and published:
                try:
                    pub_dt = datetime.strptime(published[:10], "%Y-%m-%d")
                    if pub_dt < since.replace(tzinfo=None):
                        continue
                except ValueError:
                    pass  # ambiguous date format → keep
            authors_raw = entry.get("authors") or []
            authors = [
                (a.get("name") or "").strip()
                for a in authors_raw if isinstance(a, dict)
            ]
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            if not self._passes_exclusions(title, topic.exclusions):
                continue
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=published,
                    lang=(entry.get("lang") or ["en"])[0] if isinstance(entry.get("lang"), list) else "en",
                    raw={
                        "pmid": pmid,
                        "journal": entry.get("fulljournalname") or entry.get("source") or "",
                        "authors": [a for a in authors if a],
                    },
                )
            )
        return items
