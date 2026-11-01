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
    # Spec 081 Amendment 2 (D2.2 refinement): the program's standing
    # position is program data, carried on this record and rendered as
    # the lead line of the program home. The text is Spec 029 Phase
    # E2's standing position, verbatim in substance — the two
    # panel-relative phrases of the panel rendering ("lane 2, below";
    # "on this panel") are carried in surface-neutral form here,
    # because the record is not a panel.
    "standing_position": (
        "The Indus script is not deciphered. The readings this program records are "
        "candidate readings, each one a claim standing at a stage of the claim "
        "lifecycle. A reading is not settled by being recorded and checked, and "
        "no count in this program is a measure of decipherment."
    ),
    "topic_ids": ["indus_script", "dravidian_linguistics", "ivc_archaeology"],
}


async def seed_projects(db: Database) -> None:
    """Insert the default project if no projects exist yet."""
    existing = await db.list_projects()
    if existing:
        _log.debug("Projects already seeded (%d project(s)), skipping.", len(existing))
        await _backfill_default_standing_position(db, existing)
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
        standing_position=_DEFAULT_PROJECT["standing_position"],
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


async def _backfill_default_standing_position(
    db: Database, existing: list[dict],
) -> None:
    """Fill the default program's standing position where it is empty.

    Existing installs predate the ``standing_position`` column (schema
    v25), so their default record carries ''. The position must not go
    silently missing from the program home on those installs — that is
    the loss the Spec 029 guards exist to prevent — so an EMPTY default
    record is backfilled from the seed text. A position the owner has
    edited (any non-empty value) is never overwritten, and no other
    field of the record is changed.
    """
    for proj in existing:
        if proj.get("id") != _DEFAULT_PROJECT_ID:
            continue
        if (proj.get("standing_position") or "").strip():
            return
        await db.upsert_project(
            project_id=proj["id"],
            label=proj["label"],
            description=proj.get("description", ""),
            prompt_context=proj.get("prompt_context", ""),
            question=proj.get("question", ""),
            standing_position=_DEFAULT_PROJECT["standing_position"],
            topic_ids=proj.get("topic_ids", []),
            experiment_ids=proj.get("experiment_ids", []),
            corpus_ids=proj.get("corpus_ids", []),
            is_active=bool(proj.get("is_active")),
            created_at=proj.get("created_at") or datetime.now(timezone.utc).isoformat(),
        )
        _log.info(
            "Backfilled standing position on default project: %s",
            _DEFAULT_PROJECT_ID,
        )
        return
