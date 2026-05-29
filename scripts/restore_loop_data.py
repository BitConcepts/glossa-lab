"""Check what's recoverable from old runs and optionally restore."""
import asyncio
from pathlib import Path

from glossa_lab.database import Database
from glossa_lab.pipelines.research_loop import _INSIGHT_KEYWORDS


async def main():
    db = Database(Path("backend/data/glossa.db"))
    await db.connect()

    # Check current state
    state = await db.load_research_loop_state()
    seen_count = len(state["all_seen"]) if state else 0
    hist_count = len(state["history"]) if state else 0
    print(f"Current state: {seen_count} seen, {hist_count} history")

    # Check both job results
    for jid in ["10344402cd37", "8ee8bdc6105e"]:
        result = await db.get_result_for_job(jid)
        if not result or not result.get("data"):
            print(f"Job {jid}: no result data")
            continue
        rd = result["data"]
        hist = rd.get("history", [])
        print(f"\nJob {jid}: {rd.get('cycles_run')} cycles, {rd.get('total_papers_mined')} papers")

        # Re-classify insights with new keywords
        reclassified = {}
        for entry in hist:
            verdict = entry.get("verdict", "")
            # Can't reclassify without original paper titles — they're not stored
            # But we can count what the old runs produced
            for t, c in (entry.get("insight_types") or {}).items():
                reclassified[t] = reclassified.get(t, 0) + c
        print(f"  Original insights: {reclassified}")
        print(f"  Experiments used: {set(e.get('experiment','') for e in hist)}")

    await db.close()
    print("\nNote: Paper titles are NOT stored in job results or history entries.")
    print("The all_seen set was the only place they existed, and it was reset.")
    print("Next run will re-mine papers from OpenAlex, which is actually beneficial")
    print("because the expanded keywords will now classify them properly.")


if __name__ == "__main__":
    asyncio.run(main())
