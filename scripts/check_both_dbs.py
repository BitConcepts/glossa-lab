"""Check both glossa.db files for research loop state + jobs."""
import asyncio
import json
from pathlib import Path

from glossa_lab.database import Database


async def check_db(label: str, dbpath: Path):
    print(f"\n{'='*60}")
    print(f"DB: {label} ({dbpath}, {dbpath.stat().st_size:,} bytes)")
    print("="*60)

    db = Database(dbpath)
    await db.connect()

    # Schema version
    cur = await db._conn.execute("SELECT version FROM _schema_version")
    row = await cur.fetchone()
    print(f"Schema version: {row['version'] if row else '?'}")

    # Check if research_loop_state table exists
    cur = await db._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='research_loop_state'"
    )
    has_table = await cur.fetchone()
    print(f"research_loop_state table: {'YES' if has_table else 'NO'}")

    if has_table:
        state = await db.load_research_loop_state()
        if state:
            h = state["history"]
            seen = state["all_seen"]
            print(f"Cycles stored: {len(h)}")
            print(f"Papers seen: {len(seen)}")

            # Insight types
            types = {}
            for e in h:
                for t, c in (e.get("insight_types") or {}).items():
                    types[t] = types.get(t, 0) + c
            if types:
                print(f"Insight types: {types}")

            # Verdict classification
            real = sum(1 for e in h if e.get("verdict","") and "Template " not in e.get("verdict","") and "failed" not in e.get("verdict",""))
            placeholder = sum(1 for e in h if "Template " in e.get("verdict","") and "executed." in e.get("verdict",""))
            print(f"Verdicts: {real} real, {placeholder} placeholder")

            # Show first and last 3 cycles
            print("\nFirst 3 cycles:")
            for e in h[:3]:
                print(f"  C{e.get('cycle','?')}: {e.get('experiment','?')} [{e.get('selection_method','?')}] -> {e.get('verdict','')[:100]}")
            if len(h) > 6:
                print("  ...")
            print("Last 3 cycles:")
            for e in h[-3:]:
                print(f"  C{e.get('cycle','?')}: {e.get('experiment','?')} [{e.get('selection_method','?')}] -> {e.get('verdict','')[:100]}")
        else:
            print("No research_loop_state row found")

    # Jobs
    jobs = await db.list_jobs()
    rl_jobs = [j for j in jobs if "research" in j.get("name","").lower() or j.get("pipeline","") == "research_loop"]
    print(f"\nResearch Loop jobs: {len(rl_jobs)}")
    for j in rl_jobs:
        print(f"  {j['id']}: [{j['status']}] {j['name']} ({j.get('created_at','')})")
        result = await db.get_result_for_job(j["id"])
        if result and result.get("data"):
            rd = result["data"]
            print(f"    results: cycles={rd.get('cycles_run')}, papers={rd.get('total_papers_mined')}, insights={rd.get('total_insights')}")

    # All jobs count
    all_jobs = await db.list_jobs()
    statuses = {}
    for j in all_jobs:
        s = j.get("status","?")
        statuses[s] = statuses.get(s, 0) + 1
    print(f"\nAll jobs: {len(all_jobs)} total — {statuses}")

    await db.close()


async def main():
    paths = [
        ("data/glossa.db (root)", Path("data/glossa.db")),
        ("backend/data/glossa.db", Path("backend/data/glossa.db")),
    ]
    for label, p in paths:
        if p.exists():
            await check_db(label, p)
        else:
            print(f"\n{label}: NOT FOUND")


if __name__ == "__main__":
    asyncio.run(main())
