"""List all available corpora in the database."""
import asyncio
import sys
sys.path.insert(0, ".")
from glossa_lab.database import init_db, get_db
from pathlib import Path

async def main():
    await init_db(Path("data"))
    db = get_db()
    texts = await db.list_texts()
    print(f"\n{'ID':12} {'Tokens':>8} {'Type':12} Name")
    print("-" * 70)
    for t in texts:
        print(f"{t['id']:12} {len(t['content']):>8} {t['corpus_type']:12} {t['name'][:40]}")
    print(f"\nTotal: {len(texts)} corpora")

asyncio.run(main())
