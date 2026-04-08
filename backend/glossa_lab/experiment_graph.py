"""Experiment Graph Engine.

Users compose custom experiments visually in the Experiment Builder by wiring
typed atomic computation nodes.  Each saved graph becomes a GraphExperiment
that ExperimentBase auto-discovers and surfaces in the Study Builder palette.

Hierarchy
---------
  Atomic node  (FreqCounter, PositionalProfiler, …)  ← lowest level
       ↓
  Experiment Graph  (JSON DAG of atomic nodes with typed ports)
       ↓
  GraphExperiment   (ExperimentBase subclass backed by the graph)
       ↓
  Study Builder     (composes GraphExperiments with other experiments)

Port types and colours (shared with the frontend)
-------------------------------------------------
  sequences   #059669   list of symbol sequences
  freq_map    #2563eb   {symbol: count}
  profiles    #7c3aed   [{symbol, t_rate, i_rate, m_rate, pos_class}]
  clusters    #d97706   [{label, count, members}]
  number      #dc2626   scalar int/float
  text        #0d9488   string
  json        #4f46e5   arbitrary dict/list
  any         #64748b   pass-through
"""
from __future__ import annotations

import json
import logging
from collections import Counter, deque
from pathlib import Path
from typing import Any, Callable

from glossa_lab.experiment_base import ExperimentBase

logger = logging.getLogger(__name__)

_GRAPHS_DIR = Path(__file__).parent / "experiments" / "graphs"

PORT_COLORS: dict[str, str] = {
    "sequences": "#059669",
    "freq_map":  "#2563eb",
    "profiles":  "#7c3aed",
    "clusters":  "#d97706",
    "number":    "#dc2626",
    "text":      "#0d9488",
    "json":      "#4f46e5",
    "any":       "#64748b",
}


# ── Atomic node definition ──────────────────────────────────────────────────

class AtomicNodeDef:
    def __init__(
        self,
        id: str, name: str, category: str, description: str,
        inputs: list[dict[str, str]], outputs: list[dict[str, str]],
        params_schema: dict[str, Any],
        fn: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    ) -> None:
        self.id = id; self.name = name; self.category = category
        self.description = description; self.inputs = inputs
        self.outputs = outputs; self.params_schema = params_schema; self.fn = fn

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "category": self.category,
                "description": self.description, "inputs": self.inputs,
                "outputs": self.outputs, "params_schema": self.params_schema}


# ── Atomic node implementations ─────────────────────────────────────────────

def _corpus_reader(inputs: dict, params: dict) -> dict:
    corpus_id = params.get("corpus_id") or ""
    sequences: list[list[str]] = []
    if corpus_id:
        from glossa_lab.database import get_db  # noqa: PLC0415
        import asyncio  # noqa: PLC0415
        db = get_db()
        if db:
            try:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete(db.get_text(corpus_id))
                if text and text.get("content"):
                    raw = text["content"]
                    sequences = raw if raw and isinstance(raw[0], list) else [raw]
            except Exception:  # noqa: BLE001
                pass
    if not sequences:
        icit = Path(__file__).parents[2] / "reports" / "icit_extracted_corpus.json"
        if icit.exists():
            data = json.loads(icit.read_text("utf-8"))
            sequences = [i["sequence"] for i in data.get("inscriptions", []) if i.get("sequence")]
    flat = [s for seq in sequences for s in seq]
    return {"sequences": sequences, "total_sequences": len(sequences),
            "total_tokens": len(flat), "distinct_symbols": len(set(flat))}


def _static_value(inputs: dict, params: dict) -> dict:
    val = params.get("value", "")
    try:
        parsed: Any = json.loads(val) if isinstance(val, str) and val.strip().startswith(("{", "[")) else val
    except Exception:  # noqa: BLE001
        parsed = val
    return {"value": parsed, "text": str(val)}


def _freq_counter(inputs: dict, params: dict) -> dict:
    sequences = inputs.get("sequences") or []
    min_count = int(params.get("min_count", 1))
    top_n = int(params.get("top_n", 0))
    flat = [s for seq in sequences for s in seq]
    freq = {k: v for k, v in Counter(flat).items() if v >= min_count}
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    if top_n > 0:
        ranked = ranked[:top_n]
        freq = dict(ranked)
    return {"freq_map": freq, "total_tokens": len(flat), "distinct_symbols": len(freq),
            "top_10": [{"symbol": k, "count": v} for k, v in ranked[:10]]}


def _positional_profiler(inputs: dict, params: dict) -> dict:
    sequences = inputs.get("sequences") or []
    mc = int(params.get("min_count", 3))
    tc = Counter(s for seq in sequences for s in seq)
    te = Counter(seq[-1] for seq in sequences if len(seq) > 1)
    ic = Counter(seq[0]  for seq in sequences if len(seq) > 1)
    mc2 = Counter(s for seq in sequences for s in seq[1:-1])
    profiles = []
    for sym, n in tc.items():
        if n < mc:
            continue
        t, i, m = te[sym]/n, ic[sym]/n, mc2[sym]/n
        pos = "TERMINAL" if t >= 0.60 else ("INITIAL" if i >= 0.50 else ("MEDIAL" if m >= 0.65 else "MIXED"))
        profiles.append({"symbol": sym, "count": n,
                          "t_rate": round(t,4), "i_rate": round(i,4), "m_rate": round(m,4), "pos_class": pos})
    profiles.sort(key=lambda x: x["count"], reverse=True)
    summary = {cls: sum(1 for p in profiles if p["pos_class"] == cls) for cls in ("TERMINAL","INITIAL","MEDIAL","MIXED")}
    return {"profiles": profiles, "class_summary": summary}


def _entropy_calc(inputs: dict, params: dict) -> dict:
    import math  # noqa: PLC0415
    freq_map = inputs.get("freq_map") or {}
    if not freq_map:
        freq_map = dict(Counter(s for seq in (inputs.get("sequences") or []) for s in seq))
    total = sum(freq_map.values())
    if not total:
        return {"h1": 0.0, "h1_normalized": 0.0, "vocab_size": 0, "number": 0.0}
    h1 = -sum((c/total)*math.log2(c/total) for c in freq_map.values() if c > 0)
    v = len(freq_map)
    h1n = round(h1/math.log2(v), 4) if v > 1 else 0.0
    return {"h1": round(h1,4), "h1_normalized": h1n, "vocab_size": v, "total_tokens": total, "number": h1n}


def _clusterer(inputs: dict, params: dict) -> dict:
    profiles = inputs.get("profiles") or []
    buckets: dict[str, list] = {}
    for p in profiles:
        buckets.setdefault(p.get("pos_class","MIXED"), []).append(p)
    clusters = [{"label": k, "count": len(v), "members": [m["symbol"] for m in v[:25]]}
                for k, v in buckets.items() if v]
    return {"clusters": clusters, "n_clusters": len(clusters)}


def _zipf_fitter(inputs: dict, params: dict) -> dict:
    import math  # noqa: PLC0415
    ranked = sorted((inputs.get("freq_map") or {}).values(), reverse=True)
    n = len(ranked)
    if n < 2:
        return {"zipf_exponent": 0.0, "number": 0.0}
    lrs = [math.log(r+1) for r in range(n)]
    lfs = [math.log(f) if f > 0 else 0 for f in ranked]
    mr, mf = sum(lrs)/n, sum(lfs)/n
    num = sum((lrs[i]-mr)*(lfs[i]-mf) for i in range(n))
    den = sum((lr-mr)**2 for lr in lrs)
    alpha = round(-num/den, 4) if den else 0.0
    return {"zipf_exponent": alpha, "number": alpha}


def _filter_seqs(inputs: dict, params: dict) -> dict:
    seqs = inputs.get("sequences") or []
    mn, mx = int(params.get("min_length",1)), int(params.get("max_length",999))
    out = [s for s in seqs if mn <= len(s) <= mx]
    return {"sequences": out, "total_sequences": len(out)}


def _merger(inputs: dict, params: dict) -> dict:
    result: dict[str, Any] = {}
    for k, v in inputs.items():
        if isinstance(v, dict):
            result.update({f"{k}__{ik}": iv for ik, iv in v.items()})
        else:
            result[k] = v
    return {"json": result}


def _json_export(inputs: dict, params: dict) -> dict:
    fn = (params.get("filename") or "graph_experiment_output.json").strip()
    if not fn.endswith(".json"):
        fn += ".json"
    rep = Path(__file__).parents[2] / "reports"
    rep.mkdir(exist_ok=True)
    out = rep / fn
    out.write_text(json.dumps(dict(inputs), indent=2, default=str), encoding="utf-8")
    return {"saved": True, "path": str(out), "filename": fn}


def _pass_result(inputs: dict, params: dict) -> dict:
    return dict(inputs)


def _comparator_ai(inputs: dict, params: dict) -> dict:
    """Compare two upstream result dicts using Glossa AI."""
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415
    import json as _json  # noqa: PLC0415

    a = inputs.get("a") or inputs.get(list(inputs.keys())[0] if inputs else "a", {})
    b = inputs.get("b") or (list(inputs.values())[1] if len(inputs) > 1 else {})
    prompt = params.get("comparison_prompt", "Compare these two analysis results and highlight key differences, insights, and which approach is preferable.")

    try:
        raw = call_llm(
            [{"role": "system", "content": "You are a scientific comparator. Return a concise comparison as a JSON dict with keys: summary, a_strengths, b_strengths, key_differences, recommendation."},
             {"role": "user", "content": f"{prompt}\n\nResult A:\n{_json.dumps(a)[:800]}\n\nResult B:\n{_json.dumps(b)[:800]}"}],
            json_mode=True, max_tokens=600, temperature=0.3,
        )
        return {"comparison": _json.loads(raw), "a_summarized": str(a)[:200], "b_summarized": str(b)[:200]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc), "comparison": {}}


def _experiment_wrapper(inputs: dict, params: dict) -> dict:
    """Delegate to any registered ExperimentBase subclass."""
    from glossa_lab.experiment_base import get_experiment  # noqa: PLC0415
    exp_id = params.get("experiment_id", "")
    cls = get_experiment(exp_id)
    if cls is None:
        return {"error": f"Experiment '{exp_id}' not found"}
    # Merge node params (minus meta) + upstream inputs as kwargs
    kwargs = {**inputs}
    for k, v in params.items():
        if k not in ("experiment_id",):
            kwargs[k] = v
    try:
        instance = cls()
        result = instance.run(**kwargs)
        return result if isinstance(result, dict) else {"result": result}
    except NotImplementedError:
        return {"error": f"'{exp_id}' is CLI-only; use the terminal command.", "cli_only": True}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ── Registry ────────────────────────────────────────────────────────────────

ATOMIC_NODES: dict[str, AtomicNodeDef] = {}

for _d in [
    AtomicNodeDef("CorpusReader","Corpus Reader","Sources",
        "Load sequences from a corpus (falls back to ICIT Indus corpus if no ID).",
        inputs=[],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"total_sequences","type":"number"},{"name":"total_tokens","type":"number"}],
        params_schema={"type":"object","properties":{"corpus_id":{"type":"string","title":"Corpus ID","description":"UUID from Corpora tab. Leave blank for default ICIT corpus."}}},
        fn=_corpus_reader),
    AtomicNodeDef("StaticValue","Static Value","Sources",
        "Emit a constant string, number, or JSON value as a node output.",
        inputs=[],
        outputs=[{"name":"value","type":"any"},{"name":"text","type":"text"}],
        params_schema={"type":"object","properties":{"value":{"type":"string","title":"Value"}}},
        fn=_static_value),
    AtomicNodeDef("FreqCounter","Frequency Counter","Transforms",
        "Count symbol occurrences across all sequences.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"freq_map","type":"freq_map"},{"name":"total_tokens","type":"number"},{"name":"distinct_symbols","type":"number"}],
        params_schema={"type":"object","properties":{"min_count":{"type":"integer","title":"Min Count","default":1,"minimum":1},"top_n":{"type":"integer","title":"Top N (0=all)","default":0,"minimum":0}}},
        fn=_freq_counter),
    AtomicNodeDef("PositionalProfiler","Positional Profiler","Analysis",
        "Compute I/M/T position rates per symbol (Fuls 2013 NWSP method).",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"profiles","type":"profiles"},{"name":"class_summary","type":"json"}],
        params_schema={"type":"object","properties":{"min_count":{"type":"integer","title":"Min Count","default":3,"minimum":1}}},
        fn=_positional_profiler),
    AtomicNodeDef("EntropyCalc","Entropy Calculator","Analysis",
        "Compute Shannon H1 and normalised H1 (Rao 2009 method).",
        inputs=[{"name":"sequences","type":"sequences","required":False},{"name":"freq_map","type":"freq_map","required":False}],
        outputs=[{"name":"h1","type":"number"},{"name":"h1_normalized","type":"number"},{"name":"number","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_entropy_calc),
    AtomicNodeDef("Clusterer","Symbol Clusterer","Analysis",
        "Group symbols into positional classes via L1 distance on I/M/T profiles.",
        inputs=[{"name":"profiles","type":"profiles","required":True}],
        outputs=[{"name":"clusters","type":"clusters"},{"name":"n_clusters","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_clusterer),
    AtomicNodeDef("ZipfFitter","Zipf Fitter","Analysis",
        "Estimate the Zipf exponent via log-rank regression (Yadav 2010).",
        inputs=[{"name":"freq_map","type":"freq_map","required":True}],
        outputs=[{"name":"zipf_exponent","type":"number"},{"name":"number","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_zipf_fitter),
    AtomicNodeDef("Filter","Sequence Filter","Transforms",
        "Filter sequences by min/max length.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"total_sequences","type":"number"}],
        params_schema={"type":"object","properties":{"min_length":{"type":"integer","title":"Min Length","default":1,"minimum":1},"max_length":{"type":"integer","title":"Max Length","default":50,"minimum":1}}},
        fn=_filter_seqs),
    AtomicNodeDef("Merger","Result Merger","Transforms",
        "Merge two or more upstream results into one JSON dict.",
        inputs=[{"name":"a","type":"any","required":True},{"name":"b","type":"any","required":False}],
        outputs=[{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{}},
        fn=_merger),
    AtomicNodeDef("JSONExport","JSON Export","Outputs",
        "Save result to a JSON file in reports/.",
        inputs=[{"name":"data","type":"any","required":True}],
        outputs=[{"name":"saved","type":"any"},{"name":"path","type":"text"}],
        params_schema={"type":"object","properties":{"filename":{"type":"string","title":"Filename","default":"graph_experiment_output.json"}}},
        fn=_json_export),
    AtomicNodeDef("PassResult","Pass Result","Outputs",
        "Return all upstream inputs as the final experiment result (used in Study Builder).",
        inputs=[{"name":"data","type":"any","required":True}],
        outputs=[{"name":"result","type":"json"}],
        params_schema={"type":"object","properties":{}},
        fn=_pass_result),
    # ── AI comparator ────────────────────────────────────────────────────
    AtomicNodeDef("Comparator","AI Comparator","Analysis",
        "Use Glossa AI to compare two upstream results and generate structured insights.",
        inputs=[{"name":"a","type":"json","required":True},{"name":"b","type":"json","required":True}],
        outputs=[{"name":"comparison","type":"json"}],
        params_schema={"type":"object","properties":{
            "comparison_prompt":{"type":"string","title":"Comparison Prompt","description":"Guide the AI comparison. Leave blank for default."},
        }},
        fn=_comparator_ai),
    # ── Dynamic experiment wrapper ───────────────────────────────────────────
    AtomicNodeDef("ExperimentWrapper","Experiment","Experiments",
        "Run any registered ExperimentBase subclass with upstream inputs merged as kwargs.",
        inputs=[{"name":"upstream","type":"any","required":False}],
        outputs=[{"name":"result","type":"json"}],
        params_schema={"type":"object","properties":{
            "experiment_id":{"type":"string","title":"Experiment ID","description":"ID of the registered experiment to run (e.g. positional_profile_analysis)."},
            "corpus_id":{"type":"string","title":"Corpus ID","description":"Optional corpus override for experiments that accept corpus_id."},
        }},
        fn=_experiment_wrapper),
]:
    ATOMIC_NODES[_d.id] = _d


# ── Graph execution ──────────────────────────────────────────────────────────

def _topo_sort(nodes: list[dict], edges: list[dict]) -> list[dict]:
    id2n = {n["id"]: n for n in nodes}
    in_d = {n["id"]: 0 for n in nodes}
    succ: dict[str, list[str]] = {n["id"]: [] for n in nodes}
    for e in edges:
        s, t = e.get("source",""), e.get("target","")
        if s in in_d and t in in_d:
            in_d[t] += 1
            succ[s].append(t)
    q = deque(nid for nid, d in in_d.items() if d == 0)
    order: list[dict] = []
    while q:
        nid = q.popleft()
        order.append(id2n[nid])
        for s in succ[nid]:
            in_d[s] -= 1
            if in_d[s] == 0:
                q.append(s)
    done = {n["id"] for n in order}
    order.extend(n for n in nodes if n["id"] not in done)
    return order


def execute_graph(graph_def: dict[str, Any], kwargs: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a graph experiment and return its output dict."""
    nodes: list[dict] = graph_def.get("nodes", [])
    edges: list[dict] = graph_def.get("edges", [])
    kwargs = kwargs or {}
    if not nodes:
        return {"error": "Empty graph — add at least one node"}

    ordered = _topo_sort(nodes, edges)
    res: dict[str, dict] = {}

    for node in ordered:
        nid, ntype = node["id"], node.get("type","")
        params = {**node.get("params",{}), **kwargs}

        node_inputs: dict[str, Any] = {}
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
            res[nid] = {"error": f"Unknown node type: '{ntype}'"}
            continue
        try:
            res[nid] = atomic.fn(node_inputs, params) or {}
        except Exception as exc:  # noqa: BLE001
            res[nid] = {"error": str(exc)}

    output_ids = [n["id"] for n in nodes
                  if (a := ATOMIC_NODES.get(n.get("type",""))) and a.category == "Outputs"]
    if output_ids:
        merged: dict[str, Any] = {}
        for oid in output_ids:
            merged.update(res.get(oid, {}))
        return merged
    return res.get(ordered[-1]["id"], {}) if ordered else {}


# ── Graph experiment file storage ────────────────────────────────────────────

_GRAPHS_DIR.mkdir(parents=True, exist_ok=True)


def list_graph_experiments() -> list[dict[str, Any]]:
    out = []
    for p in sorted(_GRAPHS_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text("utf-8"))
            out.append({"id": d.get("id", p.stem), "name": d.get("name", p.stem),
                        "description": d.get("description",""),
                        "node_count": len(d.get("nodes",[])),
                        "edge_count": len(d.get("edges",[]))})
        except Exception:  # noqa: BLE001
            pass
    return out


def get_graph_experiment(exp_id: str) -> dict[str, Any] | None:
    p = _GRAPHS_DIR / f"{exp_id}.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else None


def save_graph_experiment(data: dict[str, Any]) -> dict[str, Any]:
    import re, time  # noqa: PLC0415
    eid = data.get("id") or (
        re.sub(r"[^a-z0-9_]","_",(data.get("name") or "exp").lower())[:24]
        + f"_{int(time.time())%100000}"
    )
    data["id"] = eid
    (_GRAPHS_DIR / f"{eid}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    _invalidate()
    return data


def delete_graph_experiment(exp_id: str) -> bool:
    p = _GRAPHS_DIR / f"{exp_id}.json"
    if not p.exists():
        return False
    p.unlink(); _invalidate(); return True


def _invalidate() -> None:
    try:
        from glossa_lab.experiment_base import invalidate_cache  # noqa: PLC0415
        invalidate_cache()
    except Exception:  # noqa: BLE001
        pass


# ── Auto-discovery ───────────────────────────────────────────────────────────

def _make_cls(gd: dict[str, Any]) -> type:
    gid, gname, gdesc = gd.get("id","gexp"), gd.get("name","Graph Exp"), gd.get("description","")
    def run(self: Any, **kw: Any) -> dict[str, Any]:  # noqa: ANN401
        return execute_graph(gd, kw)
    return type(f"GraphExp_{gid}", (ExperimentBase,), {
        "id": gid, "name": f"\ud83d\udd00 {gname}", "category": "Graph Experiments",
        "description": gdesc or "Experiment composed in the Experiment Builder.",
        "estimated_time": "varies",
        "params_schema": {"type":"object","properties":{"corpus_id":{"type":"string","title":"Corpus ID","description":"Override corpus in CorpusReader nodes."}}},
        "run": run,
    })


def auto_migrate_hardcoded_experiments() -> int:
    """Convert every registered Python ExperimentBase subclass into a graph experiment JSON.

    Each Python experiment gets a minimal editable graph:
      [CorpusReader] → [ExperimentWrapper] → [PassResult]

    This makes all experiments visible and composable in the Experiment Builder.
    Only creates files that do not already exist (fully idempotent).
    Returns the number of new files created.
    """
    from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415

    existing_ids = {p.stem for p in _GRAPHS_DIR.glob("*.json")}
    created = 0

    for exp_id, cls in discover_experiments().items():
        if exp_id in existing_ids:
            continue  # already has a graph experiment file
        if cls.category == "Graph Experiments":
            continue  # already IS a graph experiment; skip

        clean_name = cls.name.replace("\ud83d\udd00 ", "")
        graph_data: dict = {
            "id": exp_id,
            "name": clean_name,
            "description": cls.description or f"Graph wrapper for {clean_name}.",
            "nodes": [
                {
                    "id": "corpus", "type": "expNode",
                    "data": {"atomicId": "CorpusReader", "label": "Load Corpus", "params": {}},
                    "position": {"x": 60, "y": 80},
                },
                {
                    "id": "wrap", "type": "expNode",
                    "data": {
                        "atomicId": "ExperimentWrapper",
                        "label": clean_name,
                        "params": {"experiment_id": exp_id, "corpus_id": ""},
                    },
                    "position": {"x": 320, "y": 80},
                },
                {
                    "id": "out", "type": "expNode",
                    "data": {"atomicId": "PassResult", "label": "Output", "params": {}},
                    "position": {"x": 570, "y": 80},
                },
            ],
            "edges": [
                {"id": "e1", "source": "corpus", "target": "wrap",
                 "sourcePort": "sequences", "targetPort": "upstream"},
                {"id": "e2", "source": "wrap", "target": "out",
                 "sourcePort": "result", "targetPort": "data"},
            ],
        }
        # Write directly (bypass save_graph_experiment to avoid cache invalidation per file)
        dest = _GRAPHS_DIR / f"{exp_id}.json"
        dest.write_text(__import__("json").dumps(graph_data, indent=2), encoding="utf-8")
        existing_ids.add(exp_id)
        created += 1

    if created > 0:
        _invalidate()
        logger.info("Migrated %d hardcoded experiments to graph experiment files", created)

    return created


def register_graph_experiments() -> None:
    """Inject all saved graph experiments into the ExperimentBase discovery registry."""
    if not _GRAPHS_DIR.exists():
        return
    from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415
    registry = discover_experiments()
    for p in sorted(_GRAPHS_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text("utf-8"))
            cls = _make_cls(d)
            registry[cls.id] = cls
        except Exception as exc:  # noqa: BLE001
            logger.warning("GraphExperiment load failed (%s): %s", p.name, exc)
