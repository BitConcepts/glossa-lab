"""Reseed the 3 templates that were incorrectly deleted by the cleaner.

The templates 'Indus Script Complete Analysis', 'Writing System Fingerprint Report',
and 'Writing System Tier Progression Report' were deleted because their descriptions
contained the word 'test' in context ('hypothesis test', 'benchmark test').
This script restores them directly.

Run: shell.cmd python backend/scripts/reseed_templates.py
"""
import sys, asyncio
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).parent.parent))
from glossa_lab.config import get_settings

TEMPLATES = [
    {
        "id": "tmpl-indus-complete",
        "name": "Indus Script Complete Analysis",
        "description": (
            "Full Tier 5 research report: structural fingerprint -> phonogram filter -> "
            "Dravidian vs Sumerian decipherment hypothesis comparison. "
            "Combines tier5_indus_readings and tier5_indus_decipherment results."
        ),
        "category": "Indus Script",
        "sections": [
            {"title": "Writing System Tier",     "data_source": "tier5_indus_readings",     "data_key": "b", "chart_type": "text",  "include_table": False, "description": "Full-corpus tier classification (expected: Logographic / Logosyllabic)."},
            {"title": "Phonogram Tier (filtered)","data_source": "tier5_indus_decipherment","data_key": "a", "chart_type": "text",  "include_table": False, "description": "Tier of the high-frequency phonogram subset (expected: Syllabary)."},
            {"title": "Dravidian Consistency",    "data_source": "tier5_indus_decipherment","data_key": "b", "chart_type": "text",  "include_table": False, "description": "SA mean consistency vs Dravidian LM. Higher = stronger structural match."},
            {"title": "Sumerian Consistency",     "data_source": "tier5_indus_decipherment","data_key": "c", "chart_type": "text",  "include_table": False, "description": "SA mean consistency vs Sumerian LM (comparator)."},
            {"title": "Symbol Clusters",          "data_source": "tier5_indus_readings",     "data_key": "a", "chart_type": "table", "include_table": True,  "description": "Positional clustering of high-frequency Indus signs."},
        ],
    },
    {
        "id": "tmpl-writing-system-fingerprint",
        "name": "Writing System Fingerprint Report",
        "description": (
            "10-dimensional structural fingerprint: H1, H2/H1, Zipf-alpha, V/N, hapax%, "
            "mean positional entropy, polyvalence%, inscription length, boundary-bias variance, "
            "paradigmatic rate. Compares corpus against known writing systems database."
        ),
        "category": "Analysis",
        "sections": [
            {"title": "Structural Vector",   "data_source": "experiment", "data_key": "vector",           "chart_type": "table", "include_table": True,  "description": "10D fingerprint vector for the corpus."},
            {"title": "Nearest Scripts",     "data_source": "experiment", "data_key": "nearest_scripts",  "chart_type": "table", "include_table": True,  "description": "Top-3 nearest known writing systems by Euclidean distance."},
            {"title": "Classification",      "data_source": "experiment", "data_key": "interpretation",   "chart_type": "text",  "include_table": False, "description": "Inferred script class (abjad / syllabary / logosyllabic / logographic)."},
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
            {"title": "NW Semitic Classification","data_source": "writing_system_progression","data_key": "a", "chart_type": "text","include_table": False,"description": "Tier classification for NW Semitic (abjad reference)."},
            {"title": "Meroitic Classification", "data_source": "writing_system_progression","data_key": "b", "chart_type": "text","include_table": False,"description": "Tier classification for Meroitic."},
            {"title": "Ge'ez Classification",    "data_source": "writing_system_progression","data_key": "c", "chart_type": "text","include_table": False,"description": "Tier classification for Ge'ez syllabary."},
            {"title": "Indus Classification",    "data_source": "writing_system_progression","data_key": "d", "chart_type": "text","include_table": False,"description": "Tier classification for the Indus Script."},
        ],
    },
]


async def main():
    settings = get_settings()
    db_path = settings.data_dir / "glossa.db"
    if not db_path.exists():
        print(f"ERROR: DB not found at {db_path}"); sys.exit(1)

    from glossa_lab.database import Database
    import json
    db = Database(db_path)
    await db.connect()
    now = datetime.now(timezone.utc).isoformat()

    for tmpl in TEMPLATES:
        # Check if already exists
        cur = await db._conn.execute("SELECT id FROM report_templates WHERE id=?", (tmpl["id"],))
        row = await cur.fetchone()
        if row:
            print(f"  Already exists: {tmpl['name']}")
            continue

        await db._conn.execute(
            """INSERT INTO report_templates (id, name, description, category, sections, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?)""",
            (tmpl["id"], tmpl["name"], tmpl["description"], tmpl["category"],
             json.dumps(tmpl["sections"]), now, now),
        )
        print(f"  Restored: {tmpl['name']}")

    await db._conn.commit()
    await db.close()
    print("\nDone. Verify in UI: Reports -> Generate Report to see available templates.")


if __name__ == "__main__":
    asyncio.run(main())
