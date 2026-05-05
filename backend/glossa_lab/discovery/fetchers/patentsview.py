"""PatentsView fetcher — DISABLED.

The PatentsView API at search.patentsview.org was shut down and migrated
to the USPTO Open Data Portal (api.uspto.gov) in March 2026.

This fetcher is retained as a placeholder.  Use the ``uspto`` source
(which uses the ODP API) for US patent search instead.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from glossa_lab.discovery.fetchers.base import Fetcher, TopicProfile
from glossa_lab.discovery.store import RawItem

_log = logging.getLogger("glossa_lab.discovery.fetchers.patentsview")


class PatentsViewFetcher(Fetcher):
    source = "patentsview"
    requires = ("patentsview_api_key",)
    rate_delay: float = 0

    def is_configured(self) -> bool:
        # PatentsView API has been shut down — always disabled.
        return False

    def disabled_reason(self) -> str:
        return (
            "PatentsView API (search.patentsview.org) shut down March 2026. "
            "Use the USPTO (ODP) source instead."
        )

    async def fetch(
        self, topic: TopicProfile, *, since: datetime | None = None,
    ) -> Iterable[RawItem]:
        return []
