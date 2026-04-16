"""
Run Geez anchor-convergence benchmark v2.

Changes from v1:
  - New punctuation-free corpus: 80,221 tokens, 209 signs (Dr. Fuls April 2026)
  - Word-final anchor priority: Set 0 = word-final ranked, Set 1 = frequency ranked
  - Compares both strategies at each anchor count

Expected improvements over v1 (153 signs):
  - More signs → more space to show anchor propagation
  - Word-final anchors may show better convergence than frequency alone
"""
import sys, os, json, datetime, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

_HERE = os.path.dirname(__file__)
_BACKEND = os.path.abspath(os.path.join(_HERE, ".."))
sys.path.insert(0, _BACKEND)

from glossa_lab.experiment_graph import get_graph_experiment, execute_graph
from glossa_lab.experiments._parallel import compute_device_label

REPORTS_DIR = os.path.abspath(os.path.join(_BACKEND, "..", "reports"))

def _pct(v):
    if v is None or (isinstance(v, float) and v != v): return "N/A"
    return f"{v * 100:.1f}%"

def run():
    device = compute_device_label()
    log.info("=== Geez Anchor Convergence v2 (clean corpus + word-final) ===")
    log.info("Device: %s | Corpus: 80,221 tokens, 209 signs", device)

    spec = get_graph_experiment("geez_anchor_convergence_v2")
    assert spec, "Spec not found"
    log.info("Spec: %s (%d nodes)", spec["id"], len(spec["nodes"]))

    t0 = datetime.datetime.utcnow()
    results = execute_graph(spec)
    elapsed = (datetime.datetime.utcnow() - t0).total_seconds()
    log.info("Completed in %.1f s (%.1f min)", elapsed, elapsed / 60)

    # Read saved results
    saved = os.path.join(REPORTS_DIR, "geez_anchor_convergence_v2.json")
    full = {}
    if os.path.exists(saved):
        with open(saved, encoding="utf-8") as f:
            d = json.load(f)
        full = d.get("data", d)

    table = full if isinstance(full, list) else full.get("summary_table", [])
    conc  = {} if isinstance(full, list) else full.get("conclusions", {})

    # Recompute verdict if missing
    if not conc and table:
        k0 = table[0]; km = table[-1]
        f0 = k0.get("struct_acc_free") or 0.0
        fm = km.get("struct_acc_free") or 0.0
        d0 = k0.get("struct_n_distinct") or 5.0
        dm = km.get("struct_n_distinct") or 5.0
        acc_rises = fm > f0 + 0.05
        clust_col = dm < d0 * 0.75
        conc = {
            "verdict": "SUCCESS" if acc_rises and clust_col else ("PARTIAL" if acc_rises or clust_col else "FAILURE"),
            "free_acc_at_0": f0, "free_acc_at_max": fm, "improvement": round(fm - f0, 4),
        }

    print(f"\n{'='*72}")
    print(f"GEEZ v2 — Clean Corpus + Word-Final Anchors")
    print(f"Corpus: 80,221 tokens, 209 signs | Device: {device} | Elapsed: {elapsed/60:.1f} min")
    print(f"{'='*72}")
    print(f"{'Anchors':>8} | {'StructAcc(free)':>16} | {'RandAcc(free)':>14} | {'StructConsist':>14} | {'HCI75':>8}")
    print("-" * 72)
    for row in table:
        print(f"{row.get('anchor_count', '?'):>8} | {_pct(row.get('struct_acc_free')):>16} | "
              f"{_pct(row.get('rand_acc_free')):>14} | "
              f"{_pct(row.get('struct_consistency')):>14} | "
              f"{_pct(row.get('struct_hci75')):>8}")
    print(f"{'='*72}")

    if conc:
        print(f"\nVERDICT: {conc.get('verdict', '?')}")
        print(f"Free-sign acc: {_pct(conc.get('free_acc_at_0'))} → {_pct(conc.get('free_acc_at_max'))} "
              f"(+{_pct(conc.get('improvement'))})")

    # Save timestamped
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    ts_path = os.path.join(REPORTS_DIR, f"geez_v2_{ts}.json")
    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump({"experiment": "geez_anchor_convergence_v2", "timestamp": ts,
                   "corpus": "geez_clean_nopunct_80221_209signs",
                   "word_final_anchors": True,
                   "compute_device": device, "elapsed_seconds": elapsed,
                   "conclusions": conc, "summary_table": table}, f, indent=2, default=str)
    log.info("Saved → %s", ts_path)
    return ts_path, conc

if __name__ == "__main__":
    run()
