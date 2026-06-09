import sqlite3
import json

conn = sqlite3.connect(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\data\glossa.db", timeout=3)
conn.row_factory = sqlite3.Row

# Find research loop jobs
rows = conn.execute(
    "SELECT id, name, pipeline, status, params, updated_at FROM jobs "
    "WHERE name LIKE '%esearch%' OR pipeline LIKE '%esearch%' "
    "ORDER BY updated_at DESC LIMIT 5"
).fetchall()

if not rows:
    # Try all recent failed jobs
    rows = conn.execute(
        "SELECT id, name, pipeline, status, params, updated_at FROM jobs "
        "WHERE status = 'failed' ORDER BY updated_at DESC LIMIT 5"
    ).fetchall()

for r in rows:
    print(f"ID: {r['id'][:12]}  status: {r['status']}  pipeline: {r['pipeline']}")
    print(f"  name: {r['name']}  updated: {r['updated_at']}")
    p = json.loads(r["params"]) if r["params"] else {}
    # Print all keys
    print(f"  param keys: {list(p.keys())}")
    # Print error-related fields
    for k in p:
        if "error" in k.lower() or "fail" in k.lower() or "traceback" in k.lower():
            val = str(p[k])[:500]
            print(f"  {k}: {val}")
    if "cycles_completed" in p:
        print(f"  cycles_completed: {p['cycles_completed']}")
    print()

conn.close()
