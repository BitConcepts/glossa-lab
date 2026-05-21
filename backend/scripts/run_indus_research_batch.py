"""Batch runner for Indus Script Research priorities 1-4 (April 22 2026).

Runs the following graph experiments in order:
  1. indus_fish_sign               (P3 — fast, no SA)
  2. indus_sign_function_dravidian (P2 — SA 1 arm, GPU)
  3. indus_dravidian_vs_pali       (P1b — SA 2 arms, GPU)
  4. indus_south_dravidian_vs_sanskrit (P1a — SA 2 arms, GPU)
  5. geez_anchor_convergence_v2    (P4 calibration)

Each result is saved to reports/ and printed to stdout.
Run: python backend/run_indus_research_batch.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
_HERE    = Path(__file__).resolve().parent
_BACKEND = _HERE
_REPO    = _HERE.parent
_TESTS   = _BACKEND / "tests"
for _p in (str(_BACKEND), str(_TESTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

REPORTS_DIR = _REPO / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ── Import graph runner ───────────────────────────────────────────────────────
from glossa_lab.experiment_graph import get_graph_experiment, execute_graph  # noqa: E402


def run_experiment(exp_id: str) -> dict:
    """Load and execute a graph experiment, save result to reports/."""
    print(f"\n{'='*60}")
    print(f"  Running: {exp_id}")
    print(f"{'='*60}")
    graph = get_graph_experiment(exp_id)
    if graph is None:
        print(f"  ERROR: graph '{exp_id}' not found")
        return {"error": f"graph '{exp_id}' not found"}
    t0 = time.time()
    result = execute_graph(graph)
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")
    # Print key metrics
    for key in ("mean_consistency", "h1", "tier_classification",
                "zipf_exponent", "accuracy", "b", "c", "json"):
        if key in result:
            val = result[key]
            if key == "json" and isinstance(val, dict):
                for k2, v2 in val.items():
                    if k2 not in ("a", "b", "c", "d", "e", "f"):
                        continue
                    print(f"    {k2}: {v2}")
            else:
                print(f"    {key}: {val}")
    # Save
    out_path = REPORTS_DIR / f"{exp_id}.json"
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"  Saved → reports/{exp_id}.json")
    return result


def main() -> None:
    experiments = [
        "indus_fish_sign",
        "indus_sign_function_dravidian",
        "indus_dravidian_vs_pali",
        "indus_south_dravidian_vs_sanskrit",
        "geez_anchor_convergence_v2",
    ]

    results: dict[str, dict] = {}
    t_total = time.time()
    for exp_id in experiments:
        try:
            results[exp_id] = run_experiment(exp_id)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED: {exc}")
            results[exp_id] = {"error": str(exc)}

    print(f"\n{'='*60}")
    print(f"  All {len(experiments)} experiments complete in {time.time()-t_total:.1f}s")
    print(f"{'='*60}\n")

    # Summary table
    print("SUMMARY:")
    for exp_id, r in results.items():
        if "error" in r:
            print(f"  {exp_id:<45} ERROR: {r['error']}")
        else:
            # Extract the merged JSON blob to find consistency values
            merged = r.get("json") or r
            b = merged.get("b", "?")
            c = merged.get("c", "?")
            print(f"  {exp_id:<45} b={b}  c={c}")


if __name__ == "__main__":
    main()
