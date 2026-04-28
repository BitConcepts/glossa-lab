"""Quick inspector for recent backend jobs.

Reads /api/v1/jobs and prints the most recent N jobs with status,
pipeline, created/updated timestamps, and any error message.

Usage:
    shell.cmd python backend/scripts/inspect_jobs.py [N]
"""

from __future__ import annotations

import json
import sys
import urllib.request


def main(n: int = 25) -> int:
    url = "http://127.0.0.1:8001/api/v1/jobs"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"ERROR: cannot reach backend at {url}: {e}")
        return 1
    jobs = data if isinstance(data, list) else data.get("jobs", [])
    jobs.sort(key=lambda j: j.get("created_at", ""), reverse=True)
    recent = jobs[:n]

    fmt = "{status:<12} {pipeline:<32} {created:<20} {jid:<10} {exp}"
    print(
        fmt.format(
            status="STATUS", pipeline="PIPELINE", created="CREATED", jid="JOB_ID", exp="EXTRA"
        )
    )
    print("-" * 110)
    for j in recent:
        params = j.get("params") or {}
        exp = params.get("experiment_id") or params.get("graph_id") or params.get("name") or ""
        print(
            fmt.format(
                status=str(j.get("status", "?"))[:12],
                pipeline=str(j.get("pipeline", "?"))[:32],
                created=str(j.get("created_at", "?"))[:19],
                jid=str(j.get("id", "?"))[:10],
                exp=str(exp)[:60],
            )
        )
        if j.get("error"):
            print(f"   ERROR: {str(j.get('error'))[:200]}")

    statuses = {}
    for j in recent:
        s = j.get("status", "?")
        statuses[s] = statuses.get(s, 0) + 1
    print("\nSummary of last", len(recent), "jobs:")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {s:<12} {c}")
    return 0


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    sys.exit(main(n))
