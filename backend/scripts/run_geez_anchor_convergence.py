"""
Run the geez_anchor_convergence graph experiment.

Graph: BuiltinCorpus(geez) -> CorpusSplitter(75/25) -> LMBuilder + CipherConstructor
       -> AnchorConvergenceBenchmark([0,3,10,20]) -> JSONExport

Estimated runtime: ~25-45 min on GPU (RTX 4070 SUPER, CUDA 13).

Output files:
  reports/geez_anchor_convergence.json       -- main results (per-condition table)
  reports/geez_anchor_convergence_<ts>.json  -- full timestamped run
"""
import json
import sys
import os
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

_HERE = os.path.dirname(__file__)
_BACKEND = os.path.abspath(os.path.join(_HERE, ".."))
sys.path.insert(0, _BACKEND)

from glossa_lab.experiment_graph import get_graph_experiment, execute_graph
from glossa_lab.experiments._parallel import compute_device_label

REPORTS_DIR = os.path.abspath(os.path.join(_BACKEND, "..", "reports"))


def _pct(v):
    if v is None or v != v:  # NaN check
        return "N/A"
    return f"{v * 100:.1f}%"


def run():
    device = compute_device_label()
    log.info("=== Geez Anchor-Convergence Benchmark (graph experiment) ===")
    log.info("Compute device: %s", device)
    log.info("Settings: 4 anchor conditions [0,3,10,20], 3 structured + 5 random sets each")
    log.info("SA: 2000 iterations, 1 restart per seed")

    spec = get_graph_experiment("geez_anchor_convergence")
    assert spec is not None, "Graph spec 'geez_anchor_convergence' not found"
    log.info("Spec loaded: %s (%d nodes, %d edges)", spec["id"], len(spec["nodes"]), len(spec["edges"]))

    t0 = datetime.datetime.utcnow()
    log.info("Starting graph execution ...")

    results = execute_graph(spec)

    elapsed = (datetime.datetime.utcnow() - t0).total_seconds()
    log.info("Graph execution complete in %.1f s (%.1f min)", elapsed, elapsed / 60)

    # The JSONExport node saved summary_table; retrieve full results from the saved file
    saved_path = os.path.join(REPORTS_DIR, "geez_anchor_convergence.json")
    full_results = {}
    if os.path.exists(saved_path):
        with open(saved_path, encoding="utf-8") as f:
            saved = json.load(f)
        # JSONExport wraps in {"data": ...} if passed summary_table
        full_results = saved.get("data", saved)

    # The execute_graph returns the output node result which may not have full benchmark data
    # Check if we need to re-read from reports/
    conclusions = {}
    summary_table = []

    if isinstance(full_results, list):
        summary_table = full_results
    elif isinstance(full_results, dict):
        summary_table = full_results.get("summary_table", [])
        conclusions = full_results.get("conclusions", {})

    # Print summary table
    print("\n" + "=" * 72)
    print("GEEZ SYLLABIC ANCHOR-CONVERGENCE BENCHMARK")
    print(f"Corpus: Geez Genesis (Dr. Fuls) | Device: {device} | Elapsed: {elapsed / 60:.1f} min")
    print("=" * 72)
    print(f"{'Anchors':>8} | {'StructAcc(free)':>16} | {'RandAcc(free)':>14} | "
          f"{'StructConsist':>14} | {'StructNDistinct':>15} | {'StructHCI75':>12}")
    print("-" * 90)
    for row in summary_table:
        k = row.get("anchor_count", "?")
        print(
            f"{k:>8} | {_pct(row.get('struct_acc_free')):>16} | "
            f"{_pct(row.get('rand_acc_free')):>14} | "
            f"{_pct(row.get('struct_consistency')):>14} | "
            f"{str(row.get('struct_n_distinct', 'N/A')):>15} | "
            f"{_pct(row.get('struct_hci75')):>12}"
        )
    print("=" * 72)

    if conclusions:
        print(f"\nVERDICT: {conclusions.get('verdict', '?')}")
        print(f"{conclusions.get('conclusion', '')}")
        print(f"\nFree-sign accuracy: {_pct(conclusions.get('free_acc_at_0'))} "
              f"→ {_pct(conclusions.get('free_acc_at_max'))} "
              f"(+{_pct(conclusions.get('improvement'))})")
        print(f"Accuracy rises: {conclusions.get('accuracy_rises')}")
        print(f"Clusters collapse: {conclusions.get('clusters_collapse')}")

    # Save full timestamped result
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    ts_path = os.path.join(REPORTS_DIR, f"geez_anchor_convergence_{ts}.json")
    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump({
            "experiment": "geez_anchor_convergence",
            "timestamp": ts,
            "compute_device": device,
            "elapsed_seconds": elapsed,
            "conclusions": conclusions,
            "summary_table": summary_table,
            "raw_graph_output": {k: str(v)[:200] for k, v in results.items()}
        }, f, indent=2, ensure_ascii=False, default=str)
    log.info("Timestamped results saved -> %s", ts_path)

    return ts_path, conclusions


if __name__ == "__main__":
    run()
