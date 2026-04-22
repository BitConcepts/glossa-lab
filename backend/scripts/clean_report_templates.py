"""List all report templates and delete test/placeholder ones.

Keeps only real-world useful templates. Runs against glossa.db directly.
Run: shell.cmd python backend/scripts/clean_report_templates.py
"""
import sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from glossa_lab.config import get_settings

# Templates to KEEP: real-world useful
# Templates to DELETE: test, example, placeholder, demo

KEEP_KEYWORDS = [
    "decipherment", "indus", "dravidian", "entropy", "corpus",
    "analysis", "benchmark", "sa ", "positional", "frequency",
    "bigram", "research", "sign", "language", "study", "experiment",
    "result", "finding", "hypothesis", "inscription", "concordance",
    "distribution", "comparison", "report", "pipeline",
]

# These match as whole-word patterns (space-bounded) to avoid false positives
# e.g. 'test' should NOT match 'hypothesis test data' used in descriptions
DELETE_NAMES_EXACT = [
    "get by id", "listed template", "minimal", "new name",
    "update sections", "with sections", "default template",
]
DELETE_NAME_CONTAINS = [
    "foo", "bar test", "demo template", "hello world", "e2e test",
    "placeholder", "dummy", "mock template",
]
DELETE_DESC_PHRASES = [
    # Only delete if description is clearly a test artifact
    "this is a test", "test template", "for testing", "used in tests",
    "e2e test", "created by playwright",
]


def should_delete(template: dict) -> bool:
    name = template.get("name", "").lower().strip()
    desc = template.get("description", "").lower().strip()

    # Exact name match (clearly test artifacts)
    if name in DELETE_NAMES_EXACT:
        return True
    # Name contains test-artifact phrases
    if any(kw in name for kw in DELETE_NAME_CONTAINS):
        return True
    # Description phrases that indicate pure test templates
    if any(phrase in desc for phrase in DELETE_DESC_PHRASES):
        return True

    # Has no research-relevant content in both name AND description
    has_keep_in_name = any(kw in name for kw in KEEP_KEYWORDS)
    has_keep_in_desc = any(kw in desc for kw in KEEP_KEYWORDS)
    if not has_keep_in_name and not has_keep_in_desc:
        return True

    return False


async def main():
    settings = get_settings()
    db_path = settings.data_dir / "glossa.db"
    if not db_path.exists():
        print(f"ERROR: DB not found at {db_path}"); sys.exit(1)

    from glossa_lab.database import Database
    db = Database(db_path)
    await db.connect()

    templates = await db.list_report_templates()
    print(f"Total report templates: {len(templates)}\n")

    to_keep = []
    to_delete = []

    for t in templates:
        if should_delete(t):
            to_delete.append(t)
        else:
            to_keep.append(t)

    print(f"KEEP ({len(to_keep)}):")
    for t in to_keep:
        print(f"  [KEEP]   {t['id'][:8]}  {t['name']}")

    print(f"\nDELETE ({len(to_delete)}):")
    for t in to_delete:
        print(f"  [DEL]    {t['id'][:8]}  {t['name']}")

    if not to_delete:
        print("\nNo templates to delete.")
        await db.close()
        return

    print(f"\nDeleting {len(to_delete)} test/placeholder templates...")
    deleted = 0
    for t in to_delete:
        try:
            await db._conn.execute("DELETE FROM report_templates WHERE id=?", (t["id"],))
            deleted += 1
            print(f"  Deleted: {t['name']}")
        except Exception as e:
            print(f"  ERROR deleting {t['name']}: {e}")

    await db._conn.commit()
    await db.close()

    remaining = len(to_keep)
    print(f"\nDone. Deleted {deleted}, kept {remaining} real-world templates.")


if __name__ == "__main__":
    asyncio.run(main())
