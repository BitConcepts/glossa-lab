"""Check the 30-cycle research loop results from DB."""
import asyncio
import json
from pathlib import Path

from glossa_lab.database import Database


async def main():
    db = Database(Path("data/glossa.db"))
    await db.connect()

    state = await db.load_research_loop_state()
    if not state:
        print("NO RESEARCH LOOP STATE IN DB")
        await db.close()
        return

    h = state["history"]
    seen = state["all_seen"]
    print("=== Research Loop State ===")
    print(f"Total cycles: {len(h)}")
    print(f"All seen papers: {len(seen)}")

    total_papers = sum(e.get("n_papers", 0) for e in h)
    total_insights = sum(e.get("n_insights", 0) for e in h)
    print(f"Total papers mined: {total_papers}")
    print(f"Total insights: {total_insights}")

    # Insight type distribution
    type_totals = {}
    for e in h:
        for t, c in (e.get("insight_types") or {}).items():
            type_totals[t] = type_totals.get(t, 0) + c
    print(f"\nInsight types:")
    for t, c in sorted(type_totals.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    # Selection methods
    methods = {}
    for e in h:
        m = e.get("selection_method", "unknown")
        methods[m] = methods.get(m, 0) + 1
    print(f"\nSelection methods: {methods}")

    # Experiments used
    exps = [e.get("experiment", "") for e in h]
    unique_exps = set(exps)
    print(f"\nUnique experiments run: {len(unique_exps)}")
    for exp in sorted(unique_exps):
        count = exps.count(exp)
        print(f"  {exp}: {count}x")

    # Verdicts classification
    real_runs = 0
    placeholder_runs = 0
    error_runs = 0
    for e in h:
        v = e.get("verdict", "")
        if "execution failed" in v or "no graph mapping" in v:
            error_runs += 1
        elif "Template " in v and "executed." in v:
            placeholder_runs += 1
        else:
            real_runs += 1
    print(f"\nVerdicts: {real_runs} real, {placeholder_runs} placeholder, {error_runs} errors")

    # Show ALL verdicts with cycle number
    print("\n=== All cycle verdicts ===")
    for e in h:
        sel = e.get("selection_method", "?")
        exp = e.get("experiment", "?")
        gap = e.get("gap_targeted", "?")
        np = e.get("n_papers", 0)
        ni = e.get("n_insights", 0)
        v = e.get("verdict", "")[:150]
        print(f"  C{e.get('cycle', '?'):>2} [{sel:>8}] {gap:>30} | {np:>3}p {ni:>2}i | {exp:>30} -> {v}")

    # Check job records
    jobs = await db.list_jobs()
    rl_jobs = [j for j in jobs if j.get("pipeline") == "research_loop"]
    print(f"\n=== Jobs Panel ===")
    print(f"Research Loop jobs: {len(rl_jobs)}")
    for j in rl_jobs[:5]:
        print(f"  {j['id']}: {j['name']} [{j['status']}] {j.get('created_at', '')}")
        # Check if job has results
        result = await db.get_result_for_job(j["id"])
        if result:
            rd = result.get("data", {})
            print(f"    -> cycles_run={rd.get('cycles_run')}, total_papers={rd.get('total_papers_mined')}")

    # Check for generated reports
    reports_dir = Path("reports")
    if reports_dir.exists():
        rl_reports = list(reports_dir.glob("*research*")) + list(reports_dir.glob("*loop*"))
        if rl_reports:
            print(f"\n=== Generated Reports ===")
            for r in rl_reports:
                print(f"  {r.name} ({r.stat().st_size} bytes)")

    # Check graph experiment outputs
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        recent = sorted(outputs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        if recent:
            print(f"\n=== Recent outputs (last 5) ===")
            for r in recent:
                import time
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(r.stat().st_mtime))
                print(f"  {r.name} ({r.stat().st_size} bytes, {mtime})")

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
