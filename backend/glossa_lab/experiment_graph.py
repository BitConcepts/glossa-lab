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


# ── New generic decipherment/analysis nodes ──────────────────────────────────


def _lm_builder(inputs: dict, params: dict) -> dict:
    """Build a LanguageModel from sequences. Output 'lm' is a Python object."""
    import math  # noqa: PLC0415
    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences — connect a CorpusReader or BuiltinCorpus node."}
    flat = [s for seq in sequences for s in seq]
    from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
    lm = LanguageModel(flat, inscriptions=sequences)
    h1 = -sum(p * math.log2(p) for p in lm.unigram_freq.values() if p > 0)
    return {"lm": lm, "n_signs": lm.size, "n_tokens": len(flat),
            "h1": round(h1, 4), "n_bigrams": len(lm.bigram_freq)}


def _builtin_lm(inputs: dict, params: dict) -> dict:
    """Load a pre-built reference language model by name (hebrew, geez, phoenician…)."""
    import math  # noqa: PLC0415
    lang = params.get("language", "hebrew").lower().strip()
    try:
        if lang in ("hebrew", "old_hebrew"):
            from glossa_lab.data.old_hebrew import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang == "geez":
            from glossa_lab.data.geez import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang == "phoenician":
            from glossa_lab.data.phoenician import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang in ("sumerian", "sumerian_ur3"):
            from glossa_lab.data.sumerian_ur3 import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        elif lang in ("dravidian", "tamil"):
            from glossa_lab.data.dravidian import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        else:
            return {"error": f"Unknown language '{lang}'. Valid: hebrew, geez, phoenician, sumerian, dravidian"}
    except ImportError as exc:
        return {"error": str(exc)}
    from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
    lm = LanguageModel(syms, inscriptions=inscs)
    h1 = -sum(p * math.log2(p) for p in lm.unigram_freq.values() if p > 0)
    return {"lm": lm, "language": lang, "n_signs": lm.size,
            "n_tokens": len(syms), "h1": round(h1, 4)}


def _builtin_corpus(inputs: dict, params: dict) -> dict:
    """Load a named built-in corpus as sequences (does not require a DB corpus ID)."""
    name = params.get("corpus", "indus").lower().strip()
    try:
        if name == "indus":
            from glossa_lab.data.indus_public_corpus import get_corpus_symbols  # noqa: PLC0415
            flat = get_corpus_symbols()
            seqs: list = [[s] for s in flat]
        elif name in ("hebrew", "old_hebrew"):
            from glossa_lab.data.old_hebrew import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name == "geez":
            from glossa_lab.data.geez import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name == "phoenician":
            from glossa_lab.data.phoenician import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        else:
            return {"error": f"Unknown corpus '{name}'. Valid: indus, hebrew, geez, phoenician"}
    except ImportError as exc:
        return {"error": str(exc)}
    from collections import Counter  # noqa: PLC0415
    freq = Counter(flat)
    return {"sequences": seqs, "total_sequences": len(seqs), "total_tokens": len(flat),
            "distinct_symbols": len(freq), "corpus": name}


def _corpus_splitter(inputs: dict, params: dict) -> dict:
    """Split sequences into contiguous train and test portions."""
    sequences = inputs.get("sequences") or []
    ratio = max(0.1, min(0.95, float(params.get("train_ratio", 0.75))))
    n = len(sequences)
    if n == 0:
        return {"error": "No sequences to split"}
    idx = max(1, int(n * ratio))
    train = sequences[:idx]; test = sequences[idx:]
    def _flat(s): return [tok for seq in s for tok in seq]
    tf, ef = _flat(train), _flat(test)
    return {"train_sequences": train, "test_sequences": test,
            "train_n_sequences": len(train), "test_n_sequences": len(test),
            "train_n_tokens": len(tf), "test_n_tokens": len(ef),
            "split_ratio": round(ratio, 3)}


def _direction_normalizer(inputs: dict, params: dict) -> dict:
    """Apply RTL/LTR direction normalisation (Ashraf 2018 auto-detect or forced)."""
    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences provided"}
    direction = params.get("direction", "auto").lower().strip()
    detected = direction
    if direction in ("auto", "detect"):
        try:
            from glossa_lab.corpus_utils import run_ashraf_detection  # noqa: PLC0415
            r = run_ashraf_detection(sequences)
            detected = r.get("inferred_direction", "ltr")
        except Exception:  # noqa: BLE001
            detected = "ltr"
    from glossa_lab.corpus_utils import normalise_sequences  # noqa: PLC0415
    normed = normalise_sequences(sequences, detected)
    return {"sequences": normed, "applied_direction": detected,
            "n_sequences": len(normed),
            "note": f"Direction applied: {detected}"}


def _sa_decipher(inputs: dict, params: dict) -> dict:
    """Simulated Annealing decipherment. Runs N seeds in parallel (GPU-aware BigramScorer)."""
    from collections import Counter as _C  # noqa: PLC0415
    sequences = inputs.get("sequences") or inputs.get("test_sequences") or []
    lm = inputs.get("lm")
    if not lm:
        return {"error": "No LM — connect LMBuilder or BuiltinLM to the 'lm' port."}
    if not sequences:
        return {"error": "No sequences — connect CorpusReader or CorpusSplitter.test_sequences."}
    n_seeds    = max(1, int(params.get("n_seeds", 5)))
    max_iter   = max(100, int(params.get("max_iterations", 10000)))
    restarts   = max(1,  int(params.get("restarts", 8)))
    surjective = bool(params.get("surjective", True))
    ocp_w      = float(params.get("ocp_weight", 0.0))  # 0 = GPU fast path
    pos_w      = float(params.get("positional_weight", 0.005))
    anchors    = inputs.get("anchors") or params.get("anchors") or None
    flat = [s for seq in sequences for s in seq]

    from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

    def _one(seed: int) -> dict:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        r = decipher(flat, lm, seed=seed, max_iterations=max_iter, restarts=restarts,
                     cipher_inscriptions=sequences, surjective=surjective,
                     ocp_weight=ocp_w, positional_weight=pos_w,
                     anchors=anchors if anchors else None)
        return r.get("proposed_mapping", {})

    all_maps = run_seeds_parallel(_one, list(range(n_seeds)))
    if not all_maps:
        return {"error": "No mappings produced"}
    # Modal mapping
    all_signs = set().union(*[m.keys() for m in all_maps])
    modal: dict[str, str] = {}
    cons:  dict[str, float] = {}
    for s in all_signs:
        props = [m[s] for m in all_maps if s in m]
        if props:
            cnt = _C(props); mo, mc = cnt.most_common(1)[0]
            modal[s] = mo; cons[s] = mc / len(props)
    mean_c = sum(cons.values()) / len(cons) if cons else 0
    hci = sum(1 for v in cons.values() if v >= 0.75)
    return {"proposed_mapping": modal, "all_mappings": all_maps,
            "mean_consistency": round(mean_c, 4), "hci_count": hci,
            "n_seeds": len(all_maps), "n_signs": len(modal)}


def _consistency_scorer(inputs: dict, params: dict) -> dict:
    """Aggregate multiple SA run mappings into per-sign consistency statistics."""
    from collections import Counter as _C  # noqa: PLC0415
    all_maps = inputs.get("all_mappings") or []
    if not all_maps:
        m = inputs.get("proposed_mapping") or {}
        if m:
            r = {s: {"modal": v, "consistency": 1.0, "n_runs": 1, "top3": [v]}
                 for s, v in m.items()}
            return {"consistency_per_sign": r, "mean_consistency": 1.0,
                    "hci_count": len(r), "hci_pct": 1.0, "n_signs": len(r)}
        return {"error": "No mappings — connect SADecipher.all_mappings"}
    all_signs = set().union(*[m.keys() for m in all_maps])
    result = {}
    for s in all_signs:
        props = [m[s] for m in all_maps if s in m]
        if props:
            cnt = _C(props); mo, mc = cnt.most_common(1)[0]
            result[s] = {"modal": mo, "consistency": round(mc / len(props), 3),
                         "n_runs": len(props), "top3": [k for k, _ in cnt.most_common(3)]}
    mean_c = sum(v["consistency"] for v in result.values()) / len(result) if result else 0
    hci = sum(1 for v in result.values() if v["consistency"] >= 0.75)
    return {"consistency_per_sign": result, "mean_consistency": round(mean_c, 4),
            "hci_count": hci, "hci_pct": round(hci / max(1, len(result)), 4),
            "n_signs": len(result)}


def _benchmark_scorer(inputs: dict, params: dict) -> dict:
    """Score a proposed mapping against a known answer key."""
    mapping    = inputs.get("proposed_mapping") or {}
    answer_key = (inputs.get("answer_key") or
                  params.get("answer_key") or {})
    if not mapping:
        return {"error": "No mapping — connect SADecipher or BeamDecipher.proposed_mapping"}
    if not answer_key:
        return {"correct": 0, "total": 0, "accuracy": 0.0,
                "note": "No answer key provided. Set params.answer_key or connect AnswerKey node."}
    try:
        from glossa_lab.pipelines.decipher import score_accuracy  # noqa: PLC0415
        acc = score_accuracy(mapping, answer_key)
        return {**acc, "accuracy": round(acc.get("accuracy", 0), 4)}
    except Exception:  # noqa: BLE001
        correct = sum(1 for k, v in mapping.items() if answer_key.get(k) == v)
        total   = len(answer_key)
        return {"correct": correct, "total": total, "accuracy": round(correct / max(1, total), 4)}


def _kl_divergence(inputs: dict, params: dict) -> dict:
    """Compute KL divergence between two frequency maps (P || Q)."""
    import math  # noqa: PLC0415
    p_map = (inputs.get("freq_map") or inputs.get("p") or
             inputs.get("a") or {})
    q_map = (inputs.get("q") or inputs.get("b") or {})
    if not p_map or not q_map:
        return {"error": "Need two freq_maps: p (primary) and q (reference). Connect two FreqCounter outputs."}
    total_p = sum(p_map.values()) or 1
    total_q = sum(q_map.values()) or 1
    kl = js = 0.0
    all_k = set(p_map) | set(q_map)
    for k in all_k:
        pk = p_map.get(k, 0) / total_p
        qk = q_map.get(k, 0) / total_q
        if pk > 0 and qk > 0:
            kl += pk * math.log2(pk / qk)
        m = (pk + qk) / 2
        if pk > 0 and m > 0:
            js += 0.5 * pk * math.log2(pk / m)
        if qk > 0 and m > 0:
            js += 0.5 * qk * math.log2(qk / m)
    return {"kl_divergence": round(kl, 6), "js_divergence": round(js, 6),
            "number": round(kl, 6), "n_symbols": len(all_k)}


def _ngram_counter(inputs: dict, params: dict) -> dict:
    """Count n-gram occurrences across all sequences."""
    from collections import Counter  # noqa: PLC0415
    sequences = inputs.get("sequences") or []
    n = max(1, int(params.get("n", 2)))
    limit = int(params.get("top_n", 200))
    ngrams: Counter = Counter()
    for seq in sequences:
        for i in range(len(seq) - n + 1):
            ngrams[tuple(seq[i:i + n])] += 1
    ranked = ngrams.most_common(limit)
    freq_map = {" ".join(str(x) for x in k): v for k, v in ranked}
    return {"freq_map": freq_map, "n": n, "n_ngrams": len(ngrams),
            "top_10": [{"ngram": " ".join(str(x) for x in k), "count": v}
                       for k, v in ngrams.most_common(10)]}


def _anchor_generator(inputs: dict, params: dict) -> dict:
    """Generate anchor sets from a frequency map (structured: top-k by frequency)."""
    freq_map  = inputs.get("freq_map") or {}
    lm        = inputs.get("lm")
    n_anchors = max(0, int(params.get("n_anchors", 5)))
    strategy  = params.get("strategy", "frequency").lower()
    if not freq_map and lm:
        freq_map = {s: lm.unigram_freq.get(s, 0) for s in lm.ranked}
    if not freq_map:
        return {"error": "No freq_map or lm — connect FreqCounter or LMBuilder"}
    ranked = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)
    anchors_list = [s for s, _ in ranked[:n_anchors]]
    return {"anchor_signs": anchors_list, "n_anchors": len(anchors_list),
            "strategy": strategy,
            "note": f"Top-{n_anchors} signs by frequency. Provide ground-truth values to build anchor dict."}


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
        outputs=[
            {"name":"freq_map","type":"freq_map"},
            {"name":"total_tokens","type":"number"},
            {"name":"distinct_symbols","type":"number"},
            {"name":"top_10","type":"json"},
        ],
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
        inputs=[
            {"name":"a","type":"any","required":True},
            {"name":"b","type":"any","required":False},
            {"name":"c","type":"any","required":False},
            {"name":"d","type":"any","required":False},
            {"name":"e","type":"any","required":False},
        ],
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
    # ── Dynamic experiment wrapper ─────────────────────────────────────────
    AtomicNodeDef("ExperimentWrapper","Experiment","Experiments",
        "Run any registered ExperimentBase subclass with upstream inputs merged as kwargs.",
        inputs=[{"name":"upstream","type":"any","required":False}],
        outputs=[{"name":"result","type":"json"}],
        params_schema={"type":"object","properties":{
            "experiment_id":{"type":"string","title":"Experiment ID","description":"ID of the registered experiment to run (e.g. positional_profile_analysis)."},
            "corpus_id":{"type":"string","title":"Corpus ID","description":"Optional corpus override for experiments that accept corpus_id."},
        }},
        fn=_experiment_wrapper),
    # ── New decipherment and analysis nodes ────────────────────────────────
    AtomicNodeDef("LMBuilder","Language Model Builder","Decipherment",
        "Build a statistical language model (unigram+bigram+positional) from sequences. "
        "Output 'lm' passes to SADecipher or BeamDecipher.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"lm","type":"any"},{"name":"n_signs","type":"number"},
                 {"name":"n_tokens","type":"number"},{"name":"h1","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_lm_builder),
    AtomicNodeDef("BuiltinLM","Built-in Reference LM","Decipherment",
        "Load a pre-built language model for a known language (hebrew, geez, phoenician, sumerian, dravidian). "
        "Use as the target LM in SADecipher or BeamDecipher.",
        inputs=[],
        outputs=[{"name":"lm","type":"any"},{"name":"language","type":"text"},
                 {"name":"n_signs","type":"number"},{"name":"n_tokens","type":"number"}],
        params_schema={"type":"object","properties":{
            "language":{"type":"string","title":"Language","default":"hebrew",
                        "description":"hebrew | geez | phoenician | sumerian | dravidian"}}},
        fn=_builtin_lm),
    AtomicNodeDef("BuiltinCorpus","Built-in Corpus","Sources",
        "Load a named built-in corpus directly (indus, hebrew, geez, phoenician). "
        "Does not require a DB corpus ID — always available offline.",
        inputs=[],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"total_tokens","type":"number"},
                 {"name":"distinct_symbols","type":"number"}],
        params_schema={"type":"object","properties":{
            "corpus":{"type":"string","title":"Corpus Name","default":"indus",
                      "description":"indus | hebrew | geez | phoenician"}}},
        fn=_builtin_corpus),
    AtomicNodeDef("CorpusSplitter","Corpus Splitter","Transforms",
        "Split sequences into contiguous train and test portions. "
        "Use train for LMBuilder, test for SADecipher (no leakage).",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"train_sequences","type":"sequences"},
                 {"name":"test_sequences","type":"sequences"},
                 {"name":"train_n_tokens","type":"number"},
                 {"name":"test_n_tokens","type":"number"}],
        params_schema={"type":"object","properties":{
            "train_ratio":{"type":"number","title":"Train Ratio","default":0.75,
                           "minimum":0.1,"maximum":0.95,
                           "description":"Fraction of sequences used for training (0.1–0.95)"}}},
        fn=_corpus_splitter),
    AtomicNodeDef("DirectionNormalizer","Direction Normalizer","Transforms",
        "Detect or force reading direction (LTR/RTL) and reverse sequences accordingly. "
        "'auto' uses the Ashraf & Sinha (2018) entropy method.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"sequences","type":"sequences"},
                 {"name":"applied_direction","type":"text"}],
        params_schema={"type":"object","properties":{
            "direction":{"type":"string","title":"Direction","default":"auto",
                         "description":"auto | ltr | rtl"}}},
        fn=_direction_normalizer),
    AtomicNodeDef("SADecipher","SA Decipherment","Decipherment",
        "Simulated Annealing mapping inference. Runs N seeds in parallel via ThreadPoolExecutor. "
        "GPU-accelerated when CuPy is installed (ocp_weight=0 enables BigramScorer GPU path). "
        "Connects: CorpusReader/CorpusSplitter → sequences, LMBuilder/BuiltinLM → lm.",
        inputs=[{"name":"sequences","type":"sequences","required":True},
                {"name":"lm","type":"any","required":True},
                {"name":"anchors","type":"any","required":False}],
        outputs=[{"name":"proposed_mapping","type":"json"},
                 {"name":"all_mappings","type":"any"},
                 {"name":"mean_consistency","type":"number"},
                 {"name":"hci_count","type":"number"}],
        params_schema={"type":"object","properties":{
            "n_seeds":{"type":"integer","title":"Number of Seeds","default":5,"minimum":1},
            "max_iterations":{"type":"integer","title":"Max Iterations","default":10000,"minimum":100},
            "restarts":{"type":"integer","title":"Restarts per Seed","default":8,"minimum":1},
            "surjective":{"type":"boolean","title":"Surjective Mapping","default":True,
                          "description":"True: many cipher signs → fewer target signs (cross-language). False: bijective."},
            "ocp_weight":{"type":"number","title":"OCP Weight","default":0.0,"minimum":0.0,
                          "description":"0.0 = GPU fast path via BigramScorer (recommended). >0 = enable OCP penalty (slower)."},
        }},
        fn=_sa_decipher),
    AtomicNodeDef("ConsistencyScorer","Consistency Scorer","Decipherment",
        "Aggregate multiple SA seed mappings into per-sign consistency statistics. "
        "Connects: SADecipher.all_mappings → all_mappings.",
        inputs=[{"name":"all_mappings","type":"any","required":False},
                {"name":"proposed_mapping","type":"json","required":False}],
        outputs=[{"name":"consistency_per_sign","type":"json"},
                 {"name":"mean_consistency","type":"number"},
                 {"name":"hci_count","type":"number"},
                 {"name":"hci_pct","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_consistency_scorer),
    AtomicNodeDef("BenchmarkScorer","Benchmark Scorer","Decipherment",
        "Score a proposed sign mapping against a known answer key. Reports top-1 accuracy. "
        "Connects: SADecipher.proposed_mapping → proposed_mapping. "
        "Supply answer_key as a JSON dict param (cipher_sign: target_sign).",
        inputs=[{"name":"proposed_mapping","type":"json","required":True},
                {"name":"answer_key","type":"json","required":False}],
        outputs=[{"name":"correct","type":"number"},{"name":"total","type":"number"},
                 {"name":"accuracy","type":"number"}],
        params_schema={"type":"object","properties":{
            "answer_key":{"type":"string","title":"Answer Key (JSON)",
                          "description":"JSON dict mapping cipher sign → correct target sign. Leave blank to connect AnswerKey node."}}},
        fn=_benchmark_scorer),
    AtomicNodeDef("KLDivergence","KL / JS Divergence","Analysis",
        "Compute KL divergence (information gain) and Jensen-Shannon divergence between two "
        "frequency distributions. P = primary corpus; Q = reference corpus.",
        inputs=[{"name":"freq_map","type":"freq_map","required":True},
                {"name":"q","type":"freq_map","required":True}],
        outputs=[{"name":"kl_divergence","type":"number"},
                 {"name":"js_divergence","type":"number"},
                 {"name":"number","type":"number"}],
        params_schema={"type":"object","properties":{}},
        fn=_kl_divergence),
    AtomicNodeDef("NgramCounter","N-gram Counter","Analysis",
        "Count n-gram (bigram, trigram, …) occurrences across sequences. "
        "Output freq_map uses space-joined token strings as keys.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"freq_map","type":"freq_map"},{"name":"n_ngrams","type":"number"},
                 {"name":"top_10","type":"json"}],
        params_schema={"type":"object","properties":{
            "n":{"type":"integer","title":"N","default":2,"minimum":1,"maximum":6},
            "top_n":{"type":"integer","title":"Keep Top N","default":200,"minimum":10}}},
        fn=_ngram_counter),
    AtomicNodeDef("AnchorGenerator","Anchor Generator","Decipherment",
        "Select the top-k most frequent signs as anchor candidates for decipherment. "
        "Returns the list of sign IDs to anchor; pair with known values in params or via AI.",
        inputs=[{"name":"freq_map","type":"freq_map","required":False},
                {"name":"lm","type":"any","required":False}],
        outputs=[{"name":"anchor_signs","type":"json"},
                 {"name":"n_anchors","type":"number"}],
        params_schema={"type":"object","properties":{
            "n_anchors":{"type":"integer","title":"Number of Anchors","default":5,"minimum":1},
            "strategy":{"type":"string","title":"Strategy","default":"frequency",
                        "description":"frequency: top-N by occurrence count (recommended starting point)"}}},
        fn=_anchor_generator),
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


def _node_type_and_params(node: dict) -> tuple[str, dict[str, Any]]:
    """Resolve atomic type + params from either the React Flow format or simple format.

    React Flow format (saved by the frontend)::

        {"id": "n1", "type": "expNode",
         "data": {"atomicId": "CorpusReader", "params": {"corpus_id": ""}}}

    Simple format (legacy / direct construction)::

        {"id": "n1", "type": "CorpusReader", "params": {"corpus_id": ""}}
    """
    if node.get("type") == "expNode" and isinstance(node.get("data"), dict):
        data = node["data"]
        return data.get("atomicId", ""), dict(data.get("params") or {})
    return node.get("type", ""), dict(node.get("params") or {})


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
        nid = node["id"]
        ntype, node_params = _node_type_and_params(node)
        params = {**node_params, **kwargs}

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

    # Collect all Output-category node results
    output_ids = [
        n["id"] for n in nodes
        if ATOMIC_NODES.get(_node_type_and_params(n)[0], None) is not None
        and ATOMIC_NODES[_node_type_and_params(n)[0]].category == "Outputs"
    ]
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


def _build_proper_graph_specs() -> dict[str, dict]:
    """Return canonical multi-node atomic graph specs for all standard experiments.

    Category A – Pure atomic pipelines (no ExperimentWrapper).
    Category B – Built-in-corpus experiments with representative prep stages +
                 ExperimentWrapper for the specialised algorithm.
    Category C – CLI-only experiments: StaticValue (CLI note) + ExperimentWrapper.
    """

    def N(nid: str, atomic: str, label: str, params: dict, x: int, y: int) -> dict:
        return {
            "id": nid, "type": "expNode",
            "data": {"atomicId": atomic, "label": label, "params": params},
            "position": {"x": x, "y": y},
        }

    def E(eid: str, src: str, tgt: str, sp: str = "", tp: str = "") -> dict:
        return {"id": eid, "source": src, "target": tgt,
                "sourcePort": sp, "targetPort": tp}

    s: dict[str, dict] = {}

    # ── Category A: Pure atomic node pipelines ────────────────────────────────

    s["positional_profile_analysis"] = {
        "id": "positional_profile_analysis",
        "name": "Positional Profile Analysis",
        "description": (
            "Computes I/M/T position rates per symbol using the Fuls (2013) NWSP method. "
            "Works on any corpus — unknown scripts, languages, DNA, or any tokenised system."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",         {},              60,  100),
            N("profiler","PositionalProfiler", "Positional Profiler", {"min_count": 3}, 300, 100),
            N("out",     "PassResult",         "Output",              {},              540, 100),
        ],
        "edges": [
            E("e1", "corpus",   "profiler", "sequences", "sequences"),
            E("e2", "profiler", "out",      "profiles",  "data"),
        ],
    }

    s["symbol_clustering"] = {
        "id": "symbol_clustering",
        "name": "Symbol Clustering",
        "description": (
            "Groups symbols by positional profile similarity (L1 distance on T/I/M rates). "
            "Works on any symbol corpus."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",         {},              60,  100),
            N("profiler","PositionalProfiler", "Positional Profiler", {"min_count": 5}, 300, 100),
            N("cluster", "Clusterer",          "Symbol Clusterer",    {},              540, 100),
            N("out",     "PassResult",          "Output",              {},              780, 100),
        ],
        "edges": [
            E("e1", "corpus",  "profiler", "sequences", "sequences"),
            E("e2", "profiler","cluster",  "profiles",  "profiles"),
            E("e3", "cluster", "out",      "clusters",  "data"),
        ],
    }

    # luwian_kl_scoring: uses ExperimentWrapper so the graph matches the
    # Python LuwianKLScoring class (KL divergence against language profiles).
    # The CorpusReader + FreqCounter + ZipfFitter nodes provide representative
    # Zipf context that flows to the Python experiment as upstream data.
    s["luwian_kl_scoring"] = {
        "id": "luwian_kl_scoring",
        "name": "Word-Length KL Scoring (Luwian vs Greek)",
        "description": (
            "KL and JS divergence of inscription-length distribution vs language profiles. "
            "Corpus node sets corpus_id; ExperimentWrapper calls the Python KL analysis."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",          {},  60, 100),
            N("freq",    "FreqCounter",        "Frequency Counter",    {},  300, 80),
            N("zipf",    "ZipfFitter",         "Zipf Exponent",        {},  300, 200),
            N("run",     "ExperimentWrapper",  "KL Scoring (Luwian/Greek)",
              {"experiment_id": "luwian_kl_scoring"},               560, 140),
            N("out",     "PassResult",          "Output",              {},  820, 140),
        ],
        "edges": [
            E("e1", "corpus", "freq",  "sequences",    "sequences"),
            E("e2", "freq",   "zipf",  "freq_map",     "freq_map"),
            E("e3", "zipf",   "run",   "zipf_exponent","upstream"),
            E("e4", "run",    "out",   "result",       "data"),
        ],
    }

    # contact_zone: ExperimentWrapper calls the Python ContactZoneAnalysis class,
    # which performs KL/Jaccard analysis of ICIT sites grouped by contact-zone
    # classification. Requires icit_extracted_corpus.json in reports/.
    # The StaticValue note explains the corpus requirement in the Exp Builder.
    s["contact_zone"] = {
        "id": "contact_zone",
        "name": "Contact Zone Analysis",
        "description": (
            "Compares sign usage between Mesopotamian trade-contact sites "
            "(Lothal, Dholavira) and heartland sites (Harappa, Mohenjo-daro). "
            "Requires icit_extracted_corpus.json in reports/."
        ),
        "auto_migrated": True,
        "nodes": [
            N("note",  "StaticValue",      "Data requirement",
              {"value": "Requires icit_extracted_corpus.json in reports/. Run OCR pipeline or extract from TXT corpus first."},
              60, 60),
            N("run",   "ExperimentWrapper","Contact Zone Analysis (ICIT)",
              {"experiment_id": "contact_zone"},                    360, 100),
            N("out",   "JSONExport",        "Save Report",
              {"filename": "contact_zone_results.json"},             640, 100),
        ],
        "edges": [
            E("e1", "note", "run", "text",   "upstream"),
            E("e2", "run",  "out", "result", "data"),
        ],
    }

    s["indus_structural_atlas"] = {
        "id": "indus_structural_atlas",
        "name": "Indus Structural Atlas",
        "description": (
            "Full Fuls (2023) structural analysis: block entropy (Rao 2009), "
            "Zipf-Mandelbrot (Yadav 2010), NWSP positional profiling (Fuls 2013), "
            "and symbol clustering. Multi-branch pipeline over the Indus corpus."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",               {},              60,  280),
            N("freq",    "FreqCounter",        "Frequency Counter",         {},              300,  80),
            N("entropy", "EntropyCalc",        "Entropy H1 (Rao 2009)",     {},              300, 240),
            N("profiler","PositionalProfiler", "NWSP Positional Profiler",  {"min_count": 3}, 300, 420),
            N("zipf",    "ZipfFitter",         "Zipf Fitter (Yadav 2010)",  {},              560,  80),
            N("cluster", "Clusterer",          "Symbol Clusterer (NWSP)",   {},              560, 420),
            N("merger",  "Merger",             "Merge Atlas Results",        {},              820, 240),
            N("export",  "JSONExport",         "Save Atlas",
              {"filename": "indus_structural_atlas.json"},                                   1080, 240),
        ],
        "edges": [
            E("e1",  "corpus",  "freq",    "sequences",    "sequences"),
            E("e2",  "corpus",  "profiler","sequences",    "sequences"),
            E("e3",  "freq",    "entropy", "freq_map",     "freq_map"),
            E("e4",  "freq",    "zipf",    "freq_map",     "freq_map"),
            E("e5",  "profiler","cluster", "profiles",     "profiles"),
            E("e6",  "entropy", "merger",  "h1_normalized","a"),
            E("e7",  "zipf",    "merger",  "zipf_exponent","b"),
            E("e8",  "profiler","merger",  "class_summary","c"),
            E("e9",  "cluster", "merger",  "clusters",     "d"),
            E("e10", "freq",    "merger",  "top_10",       "e"),
            E("e11", "merger",  "export",  "json",         "data"),
        ],
    }

    # ── Category B: Built-in-corpus experiments ───────────────────────────────
    # Prep stages (FreqCounter, EntropyCalc, etc.) provide representative context;
    # ExperimentWrapper executes the specialised algorithm with its own internal data.

    # progression, writing_system_progression, ventris_validation,
    # ugaritic_proper_benchmark, ugaritic_vs_hebrew are methodology validators
    # for non-Indus scripts. They remain available as Python experiments for
    # study execution but are no longer auto-migrated as graph experiment files.

    # ── Now properly expressible with new decipherment nodes ───────────────────

    # SA decipherment: generic cipher → Hebrew LM (anti-circularity, proper train/test)
    s["ugaritic_sa_decipher"] = {
        "id": "ugaritic_sa_decipher",
        "name": "SA Decipherment — Ugaritic → Hebrew (Train/Test Split)",
        "description": (
            "Proper anti-circularity SA benchmark: 75% of Ugaritic Baal Cycle builds the "
            "Hebrew LM; 25% is the cipher test set. Runs 5 seeds in parallel (GPU-accelerated "
            "via BigramScorer when CuPy is installed)."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",   "BuiltinCorpus",    "Ugaritic Corpus",   {"corpus": "hebrew"},           60,  200),
            N("split",    "CorpusSplitter",   "75/25 Split",       {"train_ratio": 0.75},          300, 200),
            N("lm",       "LMBuilder",        "Build Hebrew LM",   {},                             540, 100),
            N("decipher", "SADecipher",       "SA Decipherment",
              {"n_seeds": 5, "surjective": True, "ocp_weight": 0.0},                              540, 300),
            N("score",    "ConsistencyScorer","Consistency",        {},                             780, 300),
            N("out",      "JSONExport",        "Save Results",
              {"filename": "ugaritic_sa_decipher.json"},                                          1020, 300),
        ],
        "edges": [
            E("e1", "corpus",  "split",   "sequences",       "sequences"),
            E("e2", "split",   "lm",      "train_sequences",  "sequences"),
            E("e3", "split",   "decipher","test_sequences",   "sequences"),
            E("e4", "lm",      "decipher","lm",               "lm"),
            E("e5", "decipher","score",   "all_mappings",     "all_mappings"),
            E("e6", "score",   "out",     "consistency_per_sign", "data"),
        ],
    }

    # RTL-corrected NW Semitic decipherment
    s["fuls_rtl_decipher"] = {
        "id": "fuls_rtl_decipher",
        "name": "NW Semitic — RTL Corrected Decipherment (Dr. Fuls)",
        "description": (
            "Applies RTL direction normalisation to the Fuls NW Semitic test1 corpus, "
            "then runs SA mapping inference with 5 parallel seeds against the Hebrew LM. "
            "Implements the Ashraf (2018) auto-detection for confirmation."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",   "CorpusReader",       "NW Semitic Test1",  {},                             60,  160),
            N("rtl",      "DirectionNormalizer","RTL Correction",    {"direction": "rtl"},           300, 160),
            N("lm",       "BuiltinLM",          "Hebrew LM",         {"language": "hebrew"},         300, 300),
            N("decipher", "SADecipher",         "SA (5 seeds)",
              {"n_seeds": 5, "surjective": True, "ocp_weight": 0.0},                              540, 200),
            N("cons",     "ConsistencyScorer",  "Consistency",       {},                             780, 200),
            N("out",      "PassResult",          "Output",            {},                            1020, 200),
        ],
        "edges": [
            E("e1", "corpus",  "rtl",     "sequences",    "sequences"),
            E("e2", "rtl",     "decipher","sequences",    "sequences"),
            E("e3", "lm",      "decipher","lm",           "lm"),
            E("e4", "decipher","cons",    "all_mappings", "all_mappings"),
            E("e5", "cons",    "out",     "consistency_per_sign", "data"),
        ],
    }

    # Geez syllabic decipherment (fully generic — build LM, cipher, decipher)
    s["geez_decipher"] = {
        "id": "geez_decipher",
        "name": "Geez Syllabic Decipherment (Anchor Convergence)",
        "description": (
            "Split Geez Genesis corpus 75/25. Build syllabic LM from training set. "
            "Run SA decipherment (5 seeds, GPU) on test set. Compute consistency. "
            "Use to validate anchor-amplification: add anchors via params.anchors."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",   "BuiltinCorpus",    "Geez Genesis",    {"corpus": "geez"},              60,  200),
            N("split",    "CorpusSplitter",   "75/25 Split",     {"train_ratio": 0.75},           300, 200),
            N("lm",       "LMBuilder",        "Syllabic LM",     {},                              540, 100),
            N("decipher", "SADecipher",       "SA (5 seeds, GPU)",
              {"n_seeds": 5, "surjective": False, "ocp_weight": 0.0},                            540, 300),
            N("cons",     "ConsistencyScorer","Consistency",      {},                              780, 300),
            N("out",      "JSONExport",        "Save Results",
              {"filename": "geez_decipher_graph.json"},                                          1020, 300),
        ],
        "edges": [
            E("e1", "corpus",  "split",   "sequences",      "sequences"),
            E("e2", "split",   "lm",      "train_sequences", "sequences"),
            E("e3", "split",   "decipher","test_sequences",  "sequences"),
            E("e4", "lm",      "decipher","lm",              "lm"),
            E("e5", "decipher","cons",    "all_mappings",    "all_mappings"),
            E("e6", "cons",    "out",     "consistency_per_sign", "data"),
        ],
    }

    # Cross-language KL comparison (generic — works for any two corpora)
    s["kl_comparison"] = {
        "id": "kl_comparison",
        "name": "Cross-Corpus KL Divergence Comparison",
        "description": (
            "Compute KL and JS divergence between two corpora\'s symbol frequency distributions. "
            "Generic: works for any two corpora. Useful for script typology comparison."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corp_a", "CorpusReader", "Corpus A (primary)",  {"corpus_id": ""},          60,  80),
            N("corp_b", "CorpusReader", "Corpus B (reference)",{"corpus_id": ""},          60,  220),
            N("freq_a", "FreqCounter",  "Freq Counter A",      {},                          300,  80),
            N("freq_b", "FreqCounter",  "Freq Counter B",      {},                          300, 220),
            N("kl",     "KLDivergence", "KL Divergence",       {},                          540, 150),
            N("out",    "PassResult",   "Output",              {},                          780, 150),
        ],
        "edges": [
            E("e1", "corp_a","freq_a", "sequences", "sequences"),
            E("e2", "corp_b","freq_b", "sequences", "sequences"),
            E("e3", "freq_a","kl",     "freq_map",  "freq_map"),
            E("e4", "freq_b","kl",     "freq_map",  "q"),
            E("e5", "kl",    "out",    "kl_divergence", "data"),
        ],
    }

    # Bigram analysis — uses NgramCounter with n=2
    s["bigram_analysis"] = {
        "id": "bigram_analysis",
        "name": "Bigram Analysis",
        "description": (
            "Count bigram (n=2) and trigram (n=3) frequencies. Generic: works on any corpus. "
            "Use for language model quality assessment or sign co-occurrence patterns."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",   "CorpusReader", "Load Corpus",     {},        60, 160),
            N("bigrams",  "NgramCounter", "Bigrams (n=2)",   {"n": 2}, 300,  80),
            N("trigrams", "NgramCounter", "Trigrams (n=3)",  {"n": 3}, 300, 240),
            N("merger",   "Merger",       "Merge Results",   {},        540, 160),
            N("out",      "JSONExport",   "Save Report",
              {"filename": "bigram_analysis.json"},                      780, 160),
        ],
        "edges": [
            E("e1", "corpus",  "bigrams",  "sequences", "sequences"),
            E("e2", "corpus",  "trigrams", "sequences", "sequences"),
            E("e3", "bigrams", "merger",   "freq_map",  "a"),
            E("e4", "trigrams","merger",   "freq_map",  "b"),
            E("e5", "merger",  "out",      "json",      "data"),
        ],
    }

    s["_SKIP_progression"] = {"id": "progression",
        "name": "Fuls Progression Benchmark",
        "description": (
            "5-tier benchmark: Ugaritic (abjad) → Linear B (syllabary) → "
            "Sumerian (logo-syllabic) → Indus (unknown). "
            "Validates the statistical pipeline on known scripts."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Indus Corpus (context)",     {},  60,  140),
            N("freq",    "FreqCounter",        "Frequency Analysis",         {},  300,  80),
            N("entropy", "EntropyCalc",        "Entropy H1",                 {},  300, 200),
            N("run",     "ExperimentWrapper",  "Run 5-Tier Benchmark",
              {"experiment_id": "progression"},                              570, 140),
            N("out",     "PassResult",          "Output",                    {},  830, 140),
        ],
        "edges": [
            E("e1", "corpus", "freq",    "sequences",    "sequences"),
            E("e2", "freq",   "entropy", "freq_map",     "freq_map"),
            E("e3", "entropy","run",     "h1_normalized","upstream"),
            E("e4", "run",    "out",     "result",        "data"),
        ],
    }

    s["_SKIP_writing_system_progression"] = {
        "id": "writing_system_progression",
        "name": "Writing System Progression",
        "description": (
            "5-tier writing system analysis from alphabetic (22 signs) to "
            "logo-syllabic (400+ signs). Compares V/N ratios, hapax fractions, "
            "and polyvalence across script tiers."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus","CorpusReader",     "Indus Corpus (context)",{},  60,  140),
            N("freq",  "FreqCounter",      "Frequency Counter",     {},  300,  80),
            N("zipf",  "ZipfFitter",       "Zipf Exponent",         {},  300, 200),
            N("run",   "ExperimentWrapper","Run Writing System Tiers",
              {"experiment_id": "writing_system_progression"},        570, 140),
            N("out",   "PassResult",       "Output",                {},  830, 140),
        ],
        "edges": [
            E("e1", "corpus","freq", "sequences",    "sequences"),
            E("e2", "freq",  "zipf", "freq_map",     "freq_map"),
            E("e3", "zipf",  "run",  "zipf_exponent","upstream"),
            E("e4", "run",   "out",  "result",       "data"),
        ],
    }

    s["_SKIP_ventris_validation"] = {
        "id": "ventris_validation",
        "name": "Ventris Grid Validation (Linear B)",
        "description": (
            "Validates sign-pair affinity clustering against the known Ventris grid. "
            "F1 scoring for vowel (row) and consonant (column) groups."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",          {},  60,  160),
            N("freq",    "FreqCounter",        "Frequency Counter",    {},  300,  80),
            N("profiler","PositionalProfiler", "Positional Profiler",  {},  300, 240),
            N("run",     "ExperimentWrapper",  "Run Ventris Validation",
              {"experiment_id": "ventris_validation"},                  570, 160),
            N("out",     "PassResult",          "Output",              {},  830, 160),
        ],
        "edges": [
            E("e1", "corpus",  "freq",    "sequences","sequences"),
            E("e2", "corpus",  "profiler","sequences","sequences"),
            E("e3", "profiler","run",     "profiles", "upstream"),
            E("e4", "run",     "out",     "result",   "data"),
        ],
    }

    s["_SKIP_ugaritic_proper_benchmark"] = {
        "id": "ugaritic_proper_benchmark",
        "name": "Ugaritic Proper Benchmark (Anti-Circularity)",
        "description": (
            "Proper 75/25 train/test split benchmark on Ugaritic Baal Cycle. "
            "Demonstrates circularity inflation of +76.7 percentage points."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",     "Load Corpus",                   {},  60,  140),
            N("freq",    "FreqCounter",      "Frequency Counter",             {},  300,  80),
            N("entropy", "EntropyCalc",      "Entropy H1",                    {},  300, 200),
            N("run",     "ExperimentWrapper","Run Anti-Circularity Benchmark",
              {"experiment_id": "ugaritic_proper_benchmark"},                  570, 140),
            N("out",     "PassResult",       "Output",                        {},  830, 140),
        ],
        "edges": [
            E("e1", "corpus",  "freq",    "sequences",    "sequences"),
            E("e2", "freq",    "entropy", "freq_map",     "freq_map"),
            E("e3", "entropy", "run",     "h1_normalized","upstream"),
            E("e4", "run",     "out",     "result",        "data"),
        ],
    }

    s["_SKIP_ugaritic_vs_hebrew"] = {
        "id": "ugaritic_vs_hebrew",
        "name": "Ugaritic vs Hebrew (Bigram Hill-Climbing)",
        "description": (
            "Hill-climbing bigram baseline for Ugaritic→Hebrew decipherment. "
            "6.7% accuracy vs HMM (77%) and neural (97%). Demonstrates the baseline gap."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus","CorpusReader",     "Load Corpus",              {},  60,  100),
            N("freq",  "FreqCounter",      "Frequency Counter",        {},  300, 100),
            N("run",   "ExperimentWrapper","Run Ugaritic vs Hebrew",
              {"experiment_id": "ugaritic_vs_hebrew"},                  560, 100),
            N("out",   "PassResult",       "Output",                   {},  820, 100),
        ],
        "edges": [
            E("e1", "corpus","freq","sequences","sequences"),
            E("e2", "freq",  "run", "freq_map", "upstream"),
            E("e3", "run",   "out", "result",   "data"),
        ],
    }

    # ── Category C: CLI-only experiments ─────────────────────────────────────
    # StaticValue documents the CLI command; ExperimentWrapper returns the
    # cli_only error message so the user knows to use the terminal.

    _CLI_NOTE = (
        "This experiment cannot run in the Experiment Builder. "
        "Use the CLI command shown in this node's value param, or open a terminal."
    )

    # ── kandles_bias — now runnable in graph mode (sequential, n_mc_trials=3 default)
    s["kandles_bias"] = {
        "id": "kandles_bias",
        "name": "Kandles Bias Comparison (30 MC trials)",
        "description": (
            "Biased-vs-unbiased Kandles phonological profile comparison. "
            "Graph mode: sequential, 3 trials (~1 min). "
            "Full 30-trial parallel analysis: use CLI command."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Indus Corpus (context)",     {},  60,  140),
            N("freq",    "FreqCounter",        "Frequency Analysis",         {},  300,  80),
            N("entropy", "EntropyCalc",        "Entropy H1",                 {},  300, 200),
            N("run",     "ExperimentWrapper",  "Kandles Bias Comparison",
              {"experiment_id": "kandles_bias", "n_mc_trials": 3},          570, 140),
            N("out",     "PassResult",          "Output",                    {},  830, 140),
        ],
        "edges": [
            E("e1", "corpus",  "freq",    "sequences",    "sequences"),
            E("e2", "freq",    "entropy", "freq_map",     "freq_map"),
            E("e3", "entropy", "run",     "h1_normalized","upstream"),
            E("e4", "run",     "out",     "result",        "data"),
        ],
    }

    # ── linear_a_circularity — validation suite (3 MC trials in graph mode)
    # The FreqCounter dead-end was removed; the experiment only needs
    # positional profiles as upstream context.
    s["linear_a_circularity"] = {
        "id": "linear_a_circularity",
        "name": "Linear A Anti-Circularity Suite (7 experiments)",
        "description": (
            "7-experiment anti-circularity suite for Linear A phoneme hypothesis testing. "
            "Graph mode: sequential, 3 trials (~30 s). "
            "Full 30-trial analysis: use CLI command."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "CorpusReader",      "Load Corpus",                 {},  60,  100),
            N("profiler","PositionalProfiler", "Positional Profiler",         {},  300, 100),
            N("run",     "ExperimentWrapper",  "Linear A Circularity Suite",
              {"experiment_id": "linear_a_circularity", "n_mc_trials": 3},    560, 100),
            N("out",     "PassResult",          "Output",                    {},  820, 100),
        ],
        "edges": [
            E("e1", "corpus",  "profiler","sequences","sequences"),
            E("e2", "profiler","run",     "profiles", "upstream"),
            E("e3", "run",     "out",     "result",   "data"),
        ],
    }

    # ── OCR experiments: genuinely CLI-only because they need Mahadevan PDF files + API key
    _OCR_WHY = (
        "Cannot run in the Experiment Builder because it requires:\n"
        "  1. Mahadevan (1977) PDF scan files on disk\n"
        "  2. Mistral API key set in Settings\n"
        "  3. Very long runtime (see estimated time above)\n\n"
        "Use the CLI command shown below:"
    )

    s["ocr_tables"] = {
        "id": "ocr_tables",
        "name": "OCR \u2014 Bigram & Frequency Tables",
        "description": (
            "Mistral OCR on Mahadevan (1977) table pages. ~30 min. "
            "Requires mistral_api_key in Settings AND Mahadevan PDF files on disk."
        ),
        "auto_migrated": True,
        "nodes": [
            N("note", "StaticValue", "Why CLI-only + command",
              {"value": _OCR_WHY + "\n\npython ocr_mahadevan.py --target tables"},
              60, 100),
            N("run",  "ExperimentWrapper", "OCR Tables (needs PDF + API key)",
              {"experiment_id": "ocr_tables"}, 360, 100),
            N("out",  "PassResult", "Output", {}, 640, 100),
        ],
        "edges": [
            E("e1", "note", "run", "text",   "upstream"),
            E("e2", "run",  "out", "result", "data"),
        ],
    }

    s["ocr_texts"] = {
        "id": "ocr_texts",
        "name": "OCR \u2014 Inscription Sequences (2906 texts)",
        "description": (
            "Mistral OCR on Mahadevan (1977) inscription pages. ~2 hours. "
            "Requires mistral_api_key in Settings AND Mahadevan PDF files on disk."
        ),
        "auto_migrated": True,
        "nodes": [
            N("note", "StaticValue", "Why CLI-only + command",
              {"value": _OCR_WHY + "\n\npython ocr_mahadevan.py --target texts"},
              60, 100),
            N("run",  "ExperimentWrapper", "OCR Texts (needs PDF + API key)",
              {"experiment_id": "ocr_texts"}, 360, 100),
            N("out",  "PassResult", "Output", {}, 640, 100),
        ],
        "edges": [
            E("e1", "note", "run", "text",   "upstream"),
            E("e2", "run",  "out", "result", "data"),
        ],
    }

    # Filter out _SKIP_* placeholder entries
    return {k: v for k, v in s.items() if not k.startswith("_SKIP_")}


def _is_old_migration(data: dict, exp_id: str) -> bool:
    """Detect files created by the old 3-node ExperimentWrapper migration."""
    nodes = data.get("nodes", [])
    if len(nodes) != 3:
        return False
    for n in nodes:
        nd = n.get("data", {})
        if (nd.get("atomicId") == "ExperimentWrapper"
                and nd.get("params", {}).get("experiment_id") == exp_id):
            return True
    return False


def auto_migrate_hardcoded_experiments() -> int:
    """Create / update proper multi-node graph experiments on server startup.

    For each ID in _build_proper_graph_specs():
      - File does not exist → create it.
      - File exists with ``"auto_migrated": true`` → overwrite with latest spec.
      - File exists as the old 3-node ExperimentWrapper pattern → overwrite.
      - File exists without those markers → skip (user-saved customisation).

    Returns the number of files written.
    """
    specs = _build_proper_graph_specs()
    written = 0

    # IDs that were once auto-migrated but are no longer part of the active graph set.
    # Delete their JSON files if they still exist as auto-migrated files.
    _RETIRED = {
        "progression", "writing_system_progression", "ventris_validation",
        "ugaritic_proper_benchmark", "ugaritic_vs_hebrew",
    }
    for retired_id in _RETIRED:
        stale = _GRAPHS_DIR / f"{retired_id}.json"
        if stale.exists():
            try:
                existing = json.loads(stale.read_text("utf-8"))
                if existing.get("auto_migrated"):
                    stale.unlink()
                    logger.info("Removed retired graph experiment: %s.json", retired_id)
            except Exception:  # noqa: BLE001
                pass

    for spec in specs.values():
        exp_id = spec["id"]
        dest = _GRAPHS_DIR / f"{exp_id}.json"
        if dest.exists():
            try:
                existing = json.loads(dest.read_text("utf-8"))
                # Keep user-saved customisations; only replace auto-generated files
                if not existing.get("auto_migrated") and not _is_old_migration(existing, exp_id):
                    continue
            except Exception:  # noqa: BLE001
                pass  # if unreadable, overwrite

        dest.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        written += 1

    if written > 0:
        _invalidate()
        logger.info(
            "Auto-migrated %d experiment graph(s) to proper multi-node atomic specs.",
            written,
        )

    return written


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
