"""Seed the default research project on first run.

Idempotent — if a project with the default ID already exists, this is a no-op.
Links all registered graph experiments to the project so the Indus project
starts fully populated.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from glossa_lab.database import Database

_log = logging.getLogger("glossa_lab.project_seeder")

_DEFAULT_PROJECT_ID = "indus_decipherment"
_DEFAULT_PROJECT = {
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
}


async def seed_projects(db: Database) -> None:
    """Insert the default project if no projects exist yet."""
    existing = await db.list_projects()
    if existing:
        _log.debug("Projects already seeded (%d project(s)), skipping.", len(existing))
        return

    # Discover all registered graph experiments to link to the project.
    experiment_ids: list[str] = []
    try:
        from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415
        experiment_ids = sorted(discover_experiments().keys())
    except Exception:  # noqa: BLE001
        pass

    now = datetime.now(timezone.utc).isoformat()
    await db.upsert_project(
        project_id=_DEFAULT_PROJECT_ID,
        label=_DEFAULT_PROJECT["label"],
        description=_DEFAULT_PROJECT["description"],
        prompt_context=_DEFAULT_PROJECT["prompt_context"],
        topic_ids=_DEFAULT_PROJECT["topic_ids"],
        experiment_ids=experiment_ids,
        corpus_ids=[],
        is_active=True,
        created_at=now,
    )
    _log.info(
        "Seeded default project: %s (%d experiments linked)",
        _DEFAULT_PROJECT_ID, len(experiment_ids),
    )
