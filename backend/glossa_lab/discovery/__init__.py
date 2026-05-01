"""Continuous Discovery Engine.

Subsystem responsible for fetching, deduplicating, classifying, and surfacing
new findings related to Indus script, Dravidian linguistics, and IVC
archaeology. The implementation is split into:

* ``store``      — typed wrappers around the ``discovery_items`` SQLite table
                   defined in ``glossa_lab.database`` (V13 schema). Provides
                   the canonical-URL hashing helper used as the primary key.
* ``fetchers/``  — one module per provider (Phase C — not yet implemented).
* ``mine``       — LLM-based classification + entity linking (Phase D).
* ``llm``        — thin client over the configured providers (Phase D).

The database schema and CRUD live in ``glossa_lab.database.Database`` to keep
the project's single migration ladder canonical; ``store`` only provides the
domain dataclasses, ID hashing, and convenience wrappers that operate against
the global ``Database`` singleton via ``get_db()``.
"""

from glossa_lab.discovery.store import (
    DiscoveryItem,
    RawItem,
    canonical_url,
    make_item_id,
)

__all__ = [
    "DiscoveryItem",
    "RawItem",
    "canonical_url",
    "make_item_id",
]
