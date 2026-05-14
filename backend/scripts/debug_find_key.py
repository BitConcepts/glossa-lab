import sqlite3
from pathlib import Path
ROOT = Path(__file__).parents[2]
for p in ROOT.rglob("*.db"):
    try:
        c = sqlite3.connect(str(p))
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        print(f"{p}: {tables}")
        if "settings" in tables:
            keys = [r[0] for r in c.execute("SELECT key FROM settings").fetchall()]
            print(f"  settings keys: {keys}")
        c.close()
    except Exception as e:
        print(f"{p}: ERROR {e}")
