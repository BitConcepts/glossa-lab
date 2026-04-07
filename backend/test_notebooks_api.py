"""Quick test to debug the notebooks 500 error."""
import asyncio
import traceback

import sys
sys.path.insert(0, ".")

from glossa_lab.database import Database, init_db, get_db
from pathlib import Path

async def main():
    await init_db(Path("data"))
    db = get_db()
    assert db, "DB not initialized"
    try:
        result = await db.list_notebooks()
        print("list_notebooks OK:", result)
    except Exception:
        traceback.print_exc()
    try:
        result = await db.create_notebook(
            title="test", content="hello", study_id=None, tags=[], created_at="2026-01-01T00:00:00"
        )
        print("create_notebook OK:", result)
    except Exception:
        traceback.print_exc()

asyncio.run(main())
