"""Pre-built study workflow seeds.

Called once at startup (idempotent) to populate the studies table with
curated research workflows so the Study Builder has useful starting points.

Each seed is a named graph of experiment nodes connected by data-flow edges.
These represent the research workflows we have already built and validated.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

# ── Node / edge helpers ────────────────────────────────────────────────


def _node(
    node_id: str,
    exp_id: str,
    label: str,
    x: float,
    y: float,
    node_type: str = "experiment",
) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": node_type,
        "ref_id": exp_id,
        "label": label,
        "params": {},
        "position": {"x": x, "y": y},
    }


def _edge(edge_id: str, src: str, tgt: str) -> dict[str, Any]:
    return {"id": edge_id, "source": src, "target": tgt}


# ── Study definitions ──────────────────────────────────────────────────

_SEEDS: list[dict[str, Any]] = [
    {
        "name": "Indus Structural Atlas",
        "description": (
            "Full structural analysis of the Indus script corpus. "
            "Runs real-catalog positional analysis → structural atlas → "
            "TMK cross-validation. Produces the baseline Fuls (2023) findings."
        ),
        "graph": {
            "nodes": [
                _node("n1", "real_catalog",   "Real Catalog Analysis",    100, 100),
                _node("n2", "indus_atlas",    "Indus Structural Atlas",   400, 100),
                _node("n3", "kandles_bias",   "Kandles Bias Comparison",  700, 100),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "n3"),
            ],
        },
    },
    {
        "name": "Ugaritic Anti-Circularity Benchmark",
        "description": (
            "Validates decipherment accuracy using proper train/test splits. "
            "Runs Ugaritic vs Hebrew (hill-climbing) then the proper benchmark "
            "to quantify circularity inflation (+76.7pp)."
        ),
        "graph": {
            "nodes": [
                _node("n1", "ugaritic_vs_hebrew",       "Ugaritic vs Hebrew",          100, 100),
                _node("n2", "ugaritic_proper_benchmark", "Ugaritic Proper Benchmark",   450, 100),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
            ],
        },
    },
    {
        "name": "Kandles Bias Analysis",
        "description": (
            "Tests whether Luwian's Kandles advantage is an artefact of the "
            "Greek-calibrated phoneme mapping. Runs the 30-trial Monte Carlo "
            "suite with and without language-specific bias profiles."
        ),
        "graph": {
            "nodes": [
                _node("n1", "kandles_bias", "Kandles Bias Comparison (30 trials)", 100, 100),
            ],
            "edges": [],
        },
    },
    {
        "name": "Writing System Progression",
        "description": (
            "Validates the Fuls progression hypothesis: "
            "Ugaritic → Hebrew → Linear B → Sumerian → Indus. "
            "Runs the full 5-tier progression benchmark."
        ),
        "graph": {
            "nodes": [
                _node("n1", "progression",               "Fuls Progression Benchmark", 100, 100),
                _node("n2", "writing_system_progression", "Writing System Progression",  450, 100),
                _node("n3", "ventris_validation",         "Ventris Grid (Linear B)",      800, 100),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "n3"),
            ],
        },
    },
    {
        "name": "Linear A Full Study",
        "description": (
            "Complete Linear A analysis pipeline: OCR data prep → "
            "structural analysis → anti-circularity → Kandles bias → "
            "final hypothesis ranking."
        ),
        "graph": {
            "nodes": [
                _node("n1", "indus_atlas",    "Structural Atlas",          100,  80),
                _node("n2", "kandles_bias",   "Kandles Bias (30 trials)",  500,  80),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
            ],
        },
    },
    {
        "name": "OCR Pipeline (requires Mistral key)",
        "description": (
            "Runs Mahadevan (1977) OCR to extract bigram tables and "
            "inscription sequences. Requires mistral_api_key in Settings."
        ),
        "graph": {
            "nodes": [
                _node("n1", "ocr_tables", "OCR — Bigram & Frequency Tables", 100, 100),
                _node("n2", "ocr_texts",  "OCR — Inscription Sequences",     100, 280),
                _node("n3", "real_catalog", "Real Catalog Analysis",          450, 190),
            ],
            "edges": [
                _edge("e1", "n1", "n3"),
                _edge("e2", "n2", "n3"),
            ],
        },
    },
]


# ── Seed function ──────────────────────────────────────────────────────


async def seed_studies(db: Any) -> None:  # noqa: ANN401
    """Insert pre-built studies if the studies table is empty (idempotent)."""
    existing = await db.list_studies()
    if existing:
        return  # Already seeded; respect any user modifications

    now = datetime.now(timezone.utc).isoformat()
    logger.info("Seeding %d pre-built studies into the database", len(_SEEDS))

    for seed in _SEEDS:
        graph_json = json.dumps(seed["graph"])
        await db._conn.execute(  # noqa: SLF001 — direct insert for seeding
            """INSERT INTO studies (id, name, description, graph_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                _slug(seed["name"]),
                seed["name"],
                seed["description"],
                graph_json,
                now,
                now,
            ),
        )
    await db._conn.commit()  # noqa: SLF001
    logger.info("Study seeds inserted successfully")


def _slug(name: str) -> str:
    """Turn a study name into a stable short ID."""
    import re
    return re.sub(r"[^a-z0-9]+", "_", name.lower())[:20].strip("_")
