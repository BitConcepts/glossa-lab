"""Seed the default research goal on first run.

Idempotent — if a goal with the default ID already exists, this is a no-op.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from glossa_lab.database import Database

_log = logging.getLogger("glossa_lab.goal_seeder")

_DEFAULT_GOAL_ID = "indus_decipherment"
_DEFAULT_GOAL = {
    "label": "Indus Script Decipherment",
    "description": (
        "Decipher the Indus / Harappan script using computational methods, "
        "comparative linguistics (Dravidian, NW Semitic), archaeological "
        "context, and statistical analysis of the M77 corpus."
    ),
    "prompt_context": (
        "You are a research-triage assistant for an Indus script decipherment "
        "project. The project uses simulated-annealing decipherment, bigram "
        "language models, anchor-convergence benchmarks, and a 14,000-token "
        "M77 Indus corpus. Related fields include Dravidian comparative "
        "linguistics (DEDR cognate sets, Proto-Dravidian reconstruction, "
        "Tamil-Brahmi epigraphy) and IVC archaeology (Mohenjo-daro, Harappa, "
        "Dholavira, Rakhigarhi). Classify items by how relevant they are to "
        "advancing or challenging this decipherment effort."
    ),
    "topic_ids": ["indus_script", "dravidian_linguistics", "ivc_archaeology"],
    "study_ids": [],
    "is_default": True,
}


async def seed_goals(db: Database) -> None:
    """Insert the default goal if no goals exist yet."""
    existing = await db.list_goals()
    if existing:
        _log.debug("Goals already seeded (%d goal(s)), skipping.", len(existing))
        return

    now = datetime.now(timezone.utc).isoformat()
    await db.upsert_goal(
        goal_id=_DEFAULT_GOAL_ID,
        label=_DEFAULT_GOAL["label"],
        description=_DEFAULT_GOAL["description"],
        prompt_context=_DEFAULT_GOAL["prompt_context"],
        topic_ids=_DEFAULT_GOAL["topic_ids"],
        study_ids=_DEFAULT_GOAL["study_ids"],
        is_default=_DEFAULT_GOAL["is_default"],
        created_at=now,
    )
    _log.info("Seeded default research goal: %s", _DEFAULT_GOAL_ID)
