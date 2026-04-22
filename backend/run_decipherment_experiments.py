"""Run all 4 decipherment experiments toward Indus script reading."""
import sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from glossa_lab.experiment_graph import get_graph_experiment, ATOMIC_NODES, _topo_sort, _node_type_and_params

REPORTS = Path(__file__).parent.parent / "reports"
REPORTS.mkdir(exist_ok=True)


def run(exp_id, label=""):
    print(f"\n{'='*60}")
    print(f"  {label or exp_id}")
    print(f"{'='*60}")
    graph = get_graph_experiment(exp_id)
    if graph is None:
        print(f"  ERROR: graph '{exp_id}' not found"); return {}
    nodes, edges = graph["nodes"], graph["edges"]
    ordered = _topo_sort(nodes, edges)
    res = {}
    t0 = time.time()
    for node in ordered:
        nid = node["id"]
        ntype, params = _node_type_and_params(node)
        node_inputs = {}
        for e in edges:
            if e.get("target") != nid: continue
            src, sp, tp = e.get("source",""), e.get("sourcePort",""), e.get("targetPort","")
            tp = tp or sp or "data"
            if src in res:
                if sp and sp in res[src]: node_inputs[tp] = res[src][sp]
                else: node_inputs.update(res[src])
        atomic = ATOMIC_NODES.get(ntype)
        if not atomic:
            res[nid] = {"error": f"Unknown: {ntype}"}; print(f"  SKIP {nid}")
            continue
        try:
            r = atomic.fn(node_inputs, params) or {}
            res[nid] = r
            if "error" in r:
                print(f"  {nid}: ERROR {str(r['error'])[:100]}")
        except Exception as exc:
            res[nid] = {"error": str(exc)}; print(f"  {nid}: EXCEPTION {str(exc)[:100]}")

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    # Find Merger output
    data = {}
    for node in ordered:
        nid = node["id"]
        ntype, _ = _node_type_and_params(node)
        if ntype == "Merger":
            data = res.get(nid, {})
            inner = data.get("json", data)
            if isinstance(inner, dict):
                for k, v in list(inner.items())[:12]:
                    if isinstance(v, (str, int, float, bool)):
                        print(f"  {k}: {v}")
                    elif isinstance(v, dict):
                        print(f"  {k}: {list(v.keys())[:6]}")
                    elif isinstance(v, list) and v:
                        print(f"  {k}: [n={len(v)}] first={str(v[0])[:80]}")
            out = REPORTS / f"{exp_id}_results.json"
            out.write_text(json.dumps(data, indent=2, default=str))
            print(f"  -> saved reports/{exp_id}_results.json")
    return data


if __name__ == "__main__":
    # 1. Fast: CAS bigram phoneme projection
    run("indus_cas_bigram_phoneme", "CAS Bigram Phoneme (P122→P385 genitive)")

    # 2. SA A/B on real CISI (most important - real bigrams)
    run("indus_cisi_dravidian_vs_sanskrit", "SA A/B Dravidian vs Sanskrit on CISI")

    # 3. Anchored 2 (P385=n, P324=k)
    run("indus_cisi_anchored_2", "Anchored SA 2 (P385=n, P324=k)")

    # 4. Anchored 5 (extended)
    run("indus_cisi_anchored_5", "Anchored SA 5 (P385=n,P324=k,P122=a,P086=m,P060=i)")

    print("\n" + "="*60 + "\nAll experiments complete.\n" + "="*60)
