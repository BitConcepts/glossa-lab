"""Default report template seeder.

Seeds six research-grade report templates into the database on startup.
All templates are idempotent — they only insert if the ID is absent,
so existing user edits are never overwritten.

Templates use data_key values that match the output keys produced by
standard experiment graph nodes (JSONExport, ConsistencyScorer, etc.)
so the ReportGenerator atomic node can auto-populate sections.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("glossa_lab.report_template_seeder")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Default template definitions ─────────────────────────────────────────────
# Each entry has a stable id so upserts are safe.
# `sections` follow the SectionDef schema:
#   title, data_source, data_key, chart_type, include_table, description

DEFAULT_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "tmpl-structural-analysis",
        "name": "Structural Analysis Report",
        "description": (
            "Summarises the structural fingerprint of any corpus: H1 entropy, "
            "Zipf exponent, positional profiles (I/M/T), symbol clustering, and "
            "WritingSystemClassifier tier. Works for any script."
        ),
        "category": "Structural Analysis",
        "sections": [
            {
                "title": "Writing System Classification",
                "data_source": "experiment",
                "data_key": "tier_classification",
                "chart_type": "text",
                "include_table": False,
                "description": (
                    "Tier label from WritingSystemClassifier: "
                    "Abjad / Syllabary / Logographic / Logosyllabic."
                ),
            },
            {
                "title": "Nearest Known Script",
                "data_source": "experiment",
                "data_key": "nearest_script",
                "chart_type": "text",
                "include_table": False,
                "description": "Closest match from the benchmark script database.",
            },
            {
                "title": "H1 Entropy",
                "data_source": "experiment",
                "data_key": "h1",
                "chart_type": "bar",
                "include_table": True,
                "description": "Shannon H1 entropy in bits/token.",
            },
            {
                "title": "Zipf Exponent",
                "data_source": "experiment",
                "data_key": "zipf_exponent",
                "chart_type": "text",
                "include_table": False,
                "description": "Slope of log-rank vs log-frequency. ~1.0 = ideal Zipf.",
            },
            {
                "title": "Positional Profiles (I/M/T)",
                "data_source": "experiment",
                "data_key": "profiles",
                "chart_type": "table",
                "include_table": True,
                "description": "Per-sign initial / medial / terminal rates and dominant position class.",
            },
            {
                "title": "Symbol Clusters",
                "data_source": "experiment",
                "data_key": "clusters",
                "chart_type": "table",
                "include_table": True,
                "description": "Positional cluster groups with member signs.",
            },
        ],
    },
    {
        "id": "tmpl-decipherment-benchmark",
        "name": "Decipherment Benchmark Report",
        "description": (
            "Standard benchmark report for SA or Beam decipherment experiments: "
            "consistency scores, accuracy (if answer key present), "
            "mean HCI ≥75% fraction, and proposed mapping top-N."
        ),
        "category": "Decipherment",
        "sections": [
            {
                "title": "Mean Consistency",
                "data_source": "experiment",
                "data_key": "mean_consistency",
                "chart_type": "text",
                "include_table": False,
                "description": "Fraction of SA seeds agreeing on modal assignment (0–1).",
            },
            {
                "title": "HCI ≥ 75% Signs",
                "data_source": "experiment",
                "data_key": "hci_count",
                "chart_type": "text",
                "include_table": False,
                "description": "Number of signs with consistency ≥ 75% across seeds.",
            },
            {
                "title": "Proposed Sign Mapping",
                "data_source": "experiment",
                "data_key": "proposed_mapping",
                "chart_type": "table",
                "include_table": True,
                "description": "Modal cipher→target mapping for all signs.",
            },
            {
                "title": "Per-Sign Consistency",
                "data_source": "experiment",
                "data_key": "consistency_per_sign",
                "chart_type": "table",
                "include_table": True,
                "description": "Consistency score, modal assignment and top-3 candidates per sign.",
            },
        ],
    },
    {
        "id": "tmpl-indus-complete",
        "name": "Indus Script Complete Analysis",
        "description": (
            "Full Tier 5 research report: structural fingerprint → phonogram filter → "
            "Dravidian vs Sumerian decipherment hypothesis test. "
            "Combines tier5_indus_readings and tier5_indus_decipherment results."
        ),
        "category": "Indus Script",
        "sections": [
            {
                "title": "Writing System Tier",
                "data_source": "tier5_indus_readings",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "Full-corpus tier classification (expected: Logographic / Logosyllabic).",
            },
            {
                "title": "Phonogram Tier (after hapax filter)",
                "data_source": "tier5_indus_decipherment",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier of the high-frequency phonogram subset (expected: Syllabary).",
            },
            {
                "title": "Dravidian Consistency",
                "data_source": "tier5_indus_decipherment",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "SA mean consistency vs Dravidian LM. Higher = stronger structural match.",
            },
            {
                "title": "Sumerian Consistency",
                "data_source": "tier5_indus_decipherment",
                "data_key": "c",
                "chart_type": "text",
                "include_table": False,
                "description": "SA mean consistency vs Sumerian LM (comparator).",
            },
            {
                "title": "Symbol Clusters (phonograms)",
                "data_source": "tier5_indus_readings",
                "data_key": "a",
                "chart_type": "table",
                "include_table": True,
                "description": "Positional clustering of high-frequency Indus signs.",
            },
        ],
    },
    {
        "id": "tmpl-nw-semitic",
        "name": "NW Semitic Study Report (Fuls Method)",
        "description": (
            "Decipherment benchmark following the Fuls (2013) / Snyder (2010) protocol: "
            "RTL-corrected NW Semitic corpus → SA vs Hebrew LM → consistency + accuracy. "
            "Primary validation suite for the Glossa Lab pipeline."
        ),
        "category": "NW Semitic",
        "sections": [
            {
                "title": "SA Consistency (5 seeds)",
                "data_source": "ugaritic_vs_hebrew",
                "data_key": "mean_consistency",
                "chart_type": "text",
                "include_table": False,
                "description": "Mean SA seed consistency for Ugaritic → Hebrew.",
            },
            {
                "title": "Proposed Sign Mapping",
                "data_source": "ugaritic_vs_hebrew",
                "data_key": "proposed_mapping",
                "chart_type": "table",
                "include_table": True,
                "description": "Modal Ugaritic→Hebrew mapping from SA decipherment.",
            },
            {
                "title": "Fuls Split Sensitivity",
                "data_source": "fuls_split_sensitivity",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Consistency at 50/50 split vs 75/25 split — answers Fuls question.",
            },
        ],
    },
    {
        "id": "tmpl-writing-system-progression",
        "name": "Writing System Tier Progression Report",
        "description": (
            "Multi-tier benchmark: NW Semitic (abjad Tier 1), Meroitic (Tier 1/2), "
            "Ge'ez (syllabary Tier 4), Indus (logo-syllabic Tier 5). "
            "Quantifies the research challenge at each tier."
        ),
        "category": "Comparison",
        "sections": [
            {
                "title": "NW Semitic Classification",
                "data_source": "writing_system_progression",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for NW Semitic (abjad reference).",
            },
            {
                "title": "Meroitic Classification",
                "data_source": "writing_system_progression",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for Meroitic.",
            },
            {
                "title": "Ge'ez Classification",
                "data_source": "writing_system_progression",
                "data_key": "c",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for Ge'ez syllabary.",
            },
            {
                "title": "Indus Classification",
                "data_source": "writing_system_progression",
                "data_key": "d",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for the Indus Script.",
            },
        ],
    },
    {
        "id": "tmpl-geez-benchmark",
        "name": "Ge'ez Syllabic Anchor Convergence Report",
        "description": (
            "Anchor amplification benchmark on the Ge'ez syllabic corpus (Dr. Fuls 2026): "
            "sweep k = 0, 3, 10, 20 anchors and record StructAcc (free signs), "
            "consistency, and HCI ≥ 75%. Validates the anchor-amplification hypothesis."
        ),
        "category": "Geez / Ethiopic",
        "sections": [
            {
                "title": "Summary Table",
                "data_source": "geez_anchor_convergence_v2",
                "data_key": "summary_table",
                "chart_type": "table",
                "include_table": True,
                "description": (
                    "Columns: anchor_count, struct_acc_free, rand_acc_free, "
                    "struct_consistency, rand_consistency, struct_hci75."
                ),
            },
            {
                "title": "Conclusions",
                "data_source": "geez_anchor_convergence_v2",
                "data_key": "conclusions",
                "chart_type": "text",
                "include_table": False,
                "description": "Verdict: anchor-amplification VALIDATED / PARTIAL / FAILURE.",
            },
        ],
    },
]


async def seed_report_templates() -> int:
    """Seed default report templates (idempotent — skips existing IDs).

    Returns the number of templates inserted (0 if all already present).
    """
    from glossa_lab.database import get_db  # noqa: PLC0415

    db = get_db()
    if db is None:
        logger.warning("report_template_seeder: database not available")
        return 0

    assert db._conn  # noqa: SLF001
    inserted = 0
    for tmpl in DEFAULT_TEMPLATES:
        # Check if already present
        cursor = await db._conn.execute(  # noqa: SLF001
            "SELECT id FROM report_templates WHERE id = ?", (tmpl["id"],)
        )
        row = await cursor.fetchone()
        if row:
            continue  # already seeded — never overwrite user edits
        import json  # noqa: PLC0415
        await db._conn.execute(  # noqa: SLF001
            """INSERT INTO report_templates
               (id, name, description, category, sections, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                tmpl["id"],
                tmpl["name"],
                tmpl["description"],
                tmpl["category"],
                json.dumps(tmpl["sections"]),
                _now(),
                _now(),
            ),
        )
        inserted += 1

    if inserted:
        await db._conn.commit()  # noqa: SLF001
        logger.info("Report template seeder: inserted %d default templates", inserted)
    return inserted
