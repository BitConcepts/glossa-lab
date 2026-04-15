"""
Run the geez_decipher graph experiment (anchor-convergence study).

Usage:
    shell.cmd python backend/scripts/run_geez_decipher.py

Runs the graph experiment: BuiltinCorpus → CorpusSplitter → LMBuilder + SADecipher (5 seeds GPU)
→ ConsistencyScorer → JSONExport

Output saved to: reports/geez_decipher_graph_<timestamp>.json
"""
import json
import sys
import os
import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Ensure backend on path
_HERE = os.path.dirname(__file__)
_BACKEND = os.path.abspath(os.path.join(_HERE, ".."))
sys.path.insert(0, _BACKEND)

from glossa_lab.experiment_graph import get_graph_experiment, execute_graph
from glossa_lab.experiments._parallel import compute_device_label, gpu_available

REPORTS_DIR = os.path.join(_BACKEND, "..", "reports")


def run():
    device = compute_device_label()
    log.info("=== Geez Syllabic Anchor-Convergence (graph experiment) ===")
    log.info("Compute device: %s", device)

    spec = get_graph_experiment("geez_decipher")
    log.info("Loaded graph spec: %s (%d nodes)", spec["id"], len(spec["nodes"]))

    log.info("Executing graph …  (SA 5 seeds, expect ~2 min GPU / ~8 min CPU)")
    t0 = datetime.datetime.utcnow()
    results = execute_graph(spec)
    elapsed = (datetime.datetime.utcnow() - t0).total_seconds()
    log.info("Graph execution complete in %.1f s", elapsed)

    # Summarise ConsistencyScorer output
    cons = results.get("cons", {})
    per_sign = cons.get("consistency_per_sign", {})
    overall = cons.get("overall_consistency")
    hci = cons.get("signs_above_75pct")
    total_signs = cons.get("total_signs")

    log.info("Overall consistency: %.1f%%", (overall or 0) * 100)
    if hci is not None and total_signs:
        log.info("HCI (≥75%%): %d/%d", hci, total_signs)

    # Save timestamped results
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_path = os.path.join(REPORTS_DIR, f"geez_decipher_graph_{ts}.json")
    payload = {
        "experiment": "geez_decipher",
        "timestamp": ts,
        "compute_device": device,
        "elapsed_seconds": elapsed,
        "overall_consistency": overall,
        "signs_above_75pct": hci,
        "total_signs": total_signs,
        "consistency_per_sign": per_sign,
        "raw_results": {k: v for k, v in results.items() if k != "cons"},
    }
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    log.info("Results saved → %s", out_path)

    print("\n--- SUMMARY ---")
    print(f"Compute device : {device}")
    print(f"Elapsed        : {elapsed:.1f} s")
    print(f"Overall consist: {(overall or 0)*100:.1f}%")
    if hci is not None:
        print(f"HCI (≥75%)     : {hci}/{total_signs}")
    print(f"Output         : {out_path}")
    return out_path


if __name__ == "__main__":
    run()
