"""Quick diagnostic: dump all jobs and identify issues."""
import sqlite3, json, sys
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "glossa.db"
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row

rows = conn.execute(
    "SELECT id, name, status, pipeline, created_at, updated_at, params "
    "FROM jobs ORDER BY created_at DESC"
).fetchall()

print(f"=== {len(rows)} jobs in DB ===\n")
by_status = {}
for r in rows:
    s = r["status"]
    by_status[s] = by_status.get(s, 0) + 1
    params = json.loads(r["params"]) if r["params"] else {}
    stall = params.get("stall_reason", "")
    exp_id = params.get("exp_id", "")
    print(f"  {s:12} {r['pipeline']:18} {r['name'][:45]:45} {r['id']}"
          f"{'  STALL:'+stall if stall else ''}"
          f"{'  exp:'+exp_id if exp_id else ''}")

print(f"\nBy status: {by_status}")

# Check for stuck running jobs
stuck = [r for r in rows if r["status"] == "running"]
if stuck:
    print(f"\n⚠ {len(stuck)} STUCK running job(s):")
    for r in stuck:
        print(f"  {r['id']} {r['name']}")

# Check for results
for r in rows:
    if r["status"] == "failed":
        result = conn.execute(
            "SELECT data FROM job_results WHERE job_id = ?", (r["id"],)
        ).fetchone()
        if result:
            data = json.loads(result["data"])
            err = data.get("error", "")[:120]
            print(f"\n  Failed job {r['id']}: {err}")
        else:
            print(f"\n  Failed job {r['id']}: NO RESULT STORED")

conn.close()
