"""Europe PMC fetcher (https://www.ebi.ac.uk/europepmc/webservices/rest/search).

Keyless. Returns bibliographic metadata for biomedical and life-science
literature — complements PubMed with European and preprint sources.
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

_log = logging.getLogger("glossa_lab.discovery.fetchers.europepmc")

_ENDPOINT = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


class EuropePMCFetcher(Fetcher):
    source = "europepmc"
    requires = ()  # keyless

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        opts = topic.overrides_for(self.source)
        max_results = int(opts.get("max_results", 25))
        query = build_query(topic, quote_phrases=True) or topic.label
        if since is not None:
            query = f"({query}) AND (FIRST_PDATE:[{since.strftime('%Y-%m-%d')} TO *])"
        params = {
            "query": query,
            "pageSize": min(max_results, 100),
            "resultType": "lite",
            "format": "json",
            "sort": opts.get("sort", "DATE_DESC"),
        }
        try:
            data = await run_in_thread(http_get_json, _ENDPOINT, params=params, timeout=25.0)
        except FetcherError as exc:
            _log.warning("EuropePMC error for topic %s: %s", topic.id, exc)
            return []
        if not isinstance(data, dict):
            return []

        items: list[RawItem] = []
        for r in (data.get("resultList") or {}).get("result") or []:
            title = (r.get("title") or "").strip()
            pmid = r.get("pmid") or ""
            doi = (r.get("doi") or "").strip()
            epmc_id = r.get("id") or ""
            url = (
                f"https://doi.org/{doi}" if doi
                else f"https://europepmc.org/article/MED/{pmid}" if pmid
                else f"https://europepmc.org/article/{r.get('source','')}/{epmc_id}" if epmc_id
                else ""
            )
            if not title or not url:
                continue
            abstract = (r.get("abstractText") or "")[:1500]
            if not self._passes_exclusions(f"{title} {abstract}", topic.exclusions):
                continue
            authors = (r.get("authorString") or "").strip()
            items.append(
                RawItem(
                    title=title,
                    url=url,
                    source=self.source,
                    topic=topic.id,
                    published_at=r.get("firstPublicationDate") or "",
                    lang=(topic.languages or ["en"])[0],
                    raw={
                        "pmid": pmid,
                        "doi": doi,
                        "abstract": abstract,
                        "authors": authors,
                        "journal": r.get("journalTitle") or "",
                        "cited_by": r.get("citedByCount"),
                    },
                )
            )
        return items
