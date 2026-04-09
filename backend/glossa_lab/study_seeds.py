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


def _report(
    node_id: str,
    label: str,
    x: float,
    y: float,
    filename: str = "",
) -> dict[str, Any]:
    """A report node that compiles upstream results and saves to reports/."""
    return {
        "id": node_id,
        "type": "report",
        "ref_id": "",
        "label": label,
        "params": {"report_name": filename or ""},
        "position": {"x": x, "y": y},
    }


# ── Study definitions ──────────────────────────────────────────────────

# ── IMPORTANT ──────────────────────────────────────────────────────────
# All ref_id values MUST match experiment ids registered via ExperimentBase
# subclasses discovered from backend/glossa_lab/experiments/.
# Run: python -c "from glossa_lab.experiment_base import discover_experiments; print(list(discover_experiments()))"
# to verify registered ids before adding seeds.
# ───────────────────────────────────────────────────────────────────────

_SEEDS: list[dict[str, Any]] = [
    # ── General-purpose (corpus-agnostic) ──────────────────────────────
    {
        "name": "Positional Profile Analysis",
        "description": (
            "Run Positional Profile Analysis on any uploaded corpus. "
            "Add a 📚 Corpus node and connect it to set corpus_id, or leave blank to use the default Indus corpus. "
            "Results are compiled and saved to reports/ by the Report node."
        ),
        "graph": {
            "nodes": [
                _node("n1", "positional_profile_analysis", "Positional Profile Analysis", 100, 100),
                _report("r1", "Positional Profile Report", 450, 100, "positional_profile_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "r1"),
            ],
        },
    },
    {
        "name": "Symbol Clustering",
        "description": (
            "Cluster symbols by positional behaviour (I/M/T rates) using L1 distance. "
            "Works on any corpus — upload one in the Corpora tab and set corpus_id in the Inspector."
        ),
        "graph": {
            "nodes": [
                _node("n1", "positional_profile_analysis", "Positional Profile Analysis",  100, 100),
                _node("n2", "symbol_clustering",           "Symbol Clustering",            450, 100),
                _report("r1", "Clustering Report", 800, 100, "symbol_clustering_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "r1"),
            ],
        },
    },
    # ── Indus Script research workflows ───────────────────────────────
    {
        "name": "Indus Contact Zone & KL Scoring",
        "description": (
            "Three parallel Indus analyses compiled into one report: "
            "(1) Contact zone vs heartland sign-usage (Lothal, Dholavira vs Harappa, Mohenjo-daro). "
            "(2) Inscription-length KL scoring against 10 language profiles. "
            "(3) Indus Structural Atlas (entropy, Zipf, NWSP, clustering). "
            "All three require icit_extracted_corpus.json in reports/."
        ),
        "graph": {
            "nodes": [
                _node("n1", "contact_zone",          "Contact Zone Analysis",   100, 100),
                _node("n2", "luwian_kl_scoring",     "Luwian/Greek KL Scoring", 100, 260),
                _node("n3", "indus_structural_atlas", "Indus Structural Atlas",  100, 420),
                _report("r1", "Indus Analysis Report", 550, 260, "indus_contact_kl_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "r1"),
                _edge("e2", "n2", "r1"),
                _edge("e3", "n3", "r1"),
            ],
        },
    },
    {
        "name": "Indus Structural Atlas",
        "description": (
            "Full structural analysis of the Indus script: entropy, Zipf, NWSP positional "
            "profiling, and symbol clustering. Followed by a Kandles bias comparison to "
            "validate phonological hypothesis independence. Both run from the graph builder "
            "(use Inspector to set n_mc_trials for Kandles Bias; default=3 quick, 30 full)."
        ),
        "graph": {
            "nodes": [
                _node("n1", "indus_structural_atlas", "Indus Structural Atlas",  100, 100),
                _node("n2", "kandles_bias",           "Kandles Bias Comparison", 500, 100),
                _report("r1", "Indus Atlas Report",   900, 100, "indus_atlas_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "r1"),
            ],
        },
    },
    # ── Validation workflows ───────────────────────────────────────────
    {
        "name": "Ugaritic Anti-Circularity Benchmark",
        "description": (
            "Validates decipherment accuracy using proper train/test splits. "
            "Runs Ugaritic vs Hebrew (hill-climbing bigram) then the proper 75/25 split "
            "benchmark to quantify circularity inflation (+76.7pp)."
        ),
        "graph": {
            "nodes": [
                _node("n1", "ugaritic_vs_hebrew",       "Ugaritic vs Hebrew",       100, 100),
                _node("n2", "ugaritic_proper_benchmark", "Proper Benchmark (75/25)", 450, 100),
                _report("r1", "Decipherment Report",     800, 100, "ugaritic_decipherment_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "r1"),
            ],
        },
    },
    {
        "name": "Writing System Progression",
        "description": (
            "Validates the Fuls progression hypothesis: abjad → syllabary → logo-syllabic. "
            "Runs the 5-tier progression benchmark, writing-system comparisons, and "
            "Ventris grid validation on Linear B."
        ),
        "graph": {
            "nodes": [
                _node("n1", "progression",               "Fuls Progression Benchmark",  100, 100),
                _node("n2", "writing_system_progression", "Writing System Progression",  450, 100),
                _node("n3", "ventris_validation",          "Ventris Grid (Linear B)",     800, 100),
                _report("r1", "Progression Report",        1150, 100, "writing_progression_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "n3"),
                _edge("e3", "n3", "r1"),
            ],
        },
    },
    {
        "name": "Linear A Anti-Circularity Suite",
        "description": (
            "7-experiment anti-circularity suite: Greek-dominant Linear A result vs null "
            "mappings, ablations, and corpus shuffles. Followed by a Kandles bias comparison. "
            "Both run from the graph builder (3 MC trials default). Set n_mc_trials=30 in the "
            "Inspector for the full scientifically-valid analysis."
        ),
        "graph": {
            "nodes": [
                _node("n1", "linear_a_circularity", "Linear A Circularity Suite",  100, 100),
                _node("n2", "kandles_bias",          "Kandles Bias Comparison",     500, 100),
                _report("r1", "Linear A Report",      900, 100, "linear_a_circularity_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "n2"),
                _edge("e2", "n2", "r1"),
            ],
        },
    },
    {
        "name": "Dr. Fuls Tier Validation Progression",
        "description": (
            "Systematic validation of the decipherment pipeline following the tier "
            "progression proposed by Dr. Andreas Fuls (Catalog of Indus Signs, p.105). "
            "Each experiment must be validated before proceeding to the next. "
            "IMPORTANT: Run these in order and share results with Dr. Fuls at each step. "
            "\n\nTier 1a: Ugaritic cross-language (Hebrew LM → Ugaritic cipher). "
            "Honest result: ~6.7% with our hill-climbing bigram (vs HMM 76.7%, neural 96.7%). "
            "\nTier 1a-B: Anti-circularity — proves our original 96.7% claim was circular. "
            "\nTier 1b: Hebrew self-decipherment (75/25 split). "
            "\nTier 4: Linear B Ventris grid recovery (F1 at 100%/75%/50% corpus). "
            "\n\nTier 5a (Sumerian) and Tier 5b (Indus) follow once these pass."
        ),
        "graph": {
            "nodes": [
                _node("n1", "ugaritic_vs_hebrew",        "Tier 1a: Ugaritic vs Hebrew",         100, 100),
                _node("n2", "ugaritic_proper_benchmark",  "Tier 1a-B: Anti-Circularity Proof",   100, 260),
                _node("n3", "old_hebrew_self_benchmark",  "Tier 1b: Hebrew Self-Decipherment",   100, 420),
                _node("n4", "ventris_validation",         "Tier 4: Linear B / Ventris",          100, 580),
                _report("r1", "Fuls Tier Validation Report", 600, 340,
                        "fuls_tier_validation_report.json"),
            ],
            "edges": [
                _edge("e1", "n1", "r1"),
                _edge("e2", "n2", "r1"),
                _edge("e3", "n3", "r1"),
                _edge("e4", "n4", "r1"),
            ],
        },
    },
    {
        "name": "OCR Pipeline (requires Mistral key)",
        "description": (
            "Extracts Mahadevan (1977) bigram tables and inscription sequences via Mistral OCR. "
            "IMPORTANT: Both experiments are CLI-only \u2014 they cannot run from this graph. "
            "Open a Terminal and run the command shown on each node. "
            "Requires: (1) mistral_api_key set in Settings, (2) Mahadevan PDF files on disk."
        ),
        "graph": {
            "nodes": [
                _node("n1", "ocr_tables", "OCR \u2014 Bigram & Frequency Tables", 100, 100),
                _node("n2", "ocr_texts",  "OCR \u2014 Inscription Sequences",      100, 320),
            ],
            "edges": [],  # parallel independent CLI operations — no data flow between them
        },
    },
]


# ── Seed function ──────────────────────────────────────────────────────


async def seed_studies(db: Any) -> None:  # noqa: ANN401
    """Upsert pre-built studies into the database (idempotent).

    Uses INSERT OR REPLACE so that fixing a seed's graph in code
    immediately updates it on next server restart. User-created studies
    (with non-seed IDs) are never touched.
    """
    now = datetime.now(timezone.utc).isoformat()
    seed_ids = {_slug(s["name"]) for s in _SEEDS}

    logger.info("Upserting %d pre-built study seeds", len(_SEEDS))

    for seed in _SEEDS:
        sid = _slug(seed["name"])
        graph_json = json.dumps(seed["graph"])
        await db._conn.execute(  # noqa: SLF001
            """INSERT INTO studies (id, name, description, graph_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   name        = excluded.name,
                   description = excluded.description,
                   -- graph_json intentionally NOT updated: preserve any user modifications.
                   -- To reset a study to its seed graph, delete it and restart the server.
                   updated_at  = excluded.updated_at""",
            (
                sid,
                seed["name"],
                seed["description"],
                graph_json,
                now,
                now,
            ),
        )
    await db._conn.commit()  # noqa: SLF001
    logger.info("Study seeds upserted (seed ids: %s)", sorted(seed_ids))


def _slug(name: str) -> str:
    """Turn a study name into a stable short ID."""
    import re

    return re.sub(r"[^a-z0-9]+", "_", name.lower())[:20].strip("_")
