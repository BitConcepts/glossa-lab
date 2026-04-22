"""List all current report templates."""
import sys, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from glossa_lab.config import get_settings

async def main():
    settings = get_settings()
    from glossa_lab.database import Database
    db = Database(settings.data_dir / "glossa.db")
    await db.connect()
    templates = await db.list_report_templates()
    print(f"Report templates ({len(templates)} total):")
    for t in sorted(templates, key=lambda x: x.get("category","") + x.get("name","")):
        cat = t.get("category","?")
        n_sections = len(t.get("sections", []))
        print(f"  [{cat:15s}] {t['name']}  ({n_sections} sections)")
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())
