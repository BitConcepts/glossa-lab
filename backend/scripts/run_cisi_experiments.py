"""Run CISI corpus experiments: structural analysis + anchor estimation."""
import sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "tests"))

from glossa_lab.experiment_graph import get_graph_experiment, ATOMIC_NODES, _topo_sort, _node_type_and_params

REPORTS = Path(__file__).parent.parent / "reports"
REPORTS.mkdir(exist_ok=True)


def run_capture(exp_id):
    print(f"\n{'='*55}")
    print(f"  {exp_id}")
    print(f"{'='*55}")
    graph = get_graph_experiment(exp_id)
    nodes, edges = graph["nodes"], graph["edges"]
    ordered = _topo_sort(nodes, edges)
    res = {}
    t0 = time.time()
    for node in ordered:
        nid = node["id"]
        ntype, params = _node_type_and_params(node)
        node_inputs = {}
        for e in edges:
            if e.get("target") != nid:
                continue
            src, sp, tp = e.get("source",""), e.get("sourcePort",""), e.get("targetPort","")
            tp = tp or sp or "data"
            if src in res:
                if sp and sp in res[src]:
                    node_inputs[tp] = res[src][sp]
                else:
                    node_inputs.update(res[src])
        atomic = ATOMIC_NODES.get(ntype)
        if not atomic:
            res[nid] = {"error": f"Unknown: {ntype}"}
            print(f"  SKIP {nid} ({ntype})")
            continue
        try:
            r = atomic.fn(node_inputs, params) or {}
            res[nid] = r
            if "error" in r:
                print(f"  {nid}: ERROR {r['error']}")
        except Exception as exc:
            res[nid] = {"error": str(exc)}
            print(f"  {nid}: EXCEPTION {exc}")

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    # Find the Merger result
    for node in ordered:
        nid = node["id"]
        ntype, _ = _node_type_and_params(node)
        if ntype == "Merger":
            r = res[nid]
            inner = r.get("json", r)
            if isinstance(inner, dict):
                for k, v in inner.items():
                    if isinstance(v, (int, float, str, bool)):
                        print(f"  {k}: {v}")
                    elif isinstance(v, list):
                        print(f"  {k}: [list n={len(v)}] first={v[0] if v else None}")
                    elif isinstance(v, dict):
                        print(f"  {k}: {list(v.keys())[:5]}")
            # Save
            out = REPORTS / f"{exp_id}_results.json"
            out.write_text(json.dumps(r, indent=2, default=str))
            print(f"  -> saved {exp_id}_results.json")
    return res


if __name__ == "__main__":
    for eid in ["indus_cisi_structural", "indus_anchor_estimation"]:
        run_capture(eid)
    print("\nDone.")
