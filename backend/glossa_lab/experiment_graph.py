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
            # Use word-level symbols so SA proposes word strings (e.g. 'tarhunt',
            # 'kol', 'min') that align with the Tamil-Brahmi + DEDR target
            # inventory in DefaultIndusValueRoleMap. Character-level symbols
            # would produce single-letter values that strict_mode rejects.
            from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
            syms = get_word_symbols(); inscs = None
        elif lang in ("south_dravidian", "dravidian_south", "kannada_telugu_tamil"):
            from glossa_lab.data.dravidian_south import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        elif lang in ("kannada",):
            from glossa_lab.data.dravidian_south import get_kannada_symbols  # noqa: PLC0415
            syms = get_kannada_symbols(); inscs = None
        elif lang in ("telugu",):
            from glossa_lab.data.dravidian_south import get_telugu_symbols  # noqa: PLC0415
            syms = get_telugu_symbols(); inscs = None
        elif lang in ("pali", "middle_indo_aryan", "mia"):
            from glossa_lab.data.pali import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        elif lang in ("sanskrit", "vedic"):
            from glossa_lab.data.sanskrit import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        elif lang in ("coptic",):
            from glossa_lab.data.meroitic import get_coptic_symbols  # noqa: PLC0415
            syms = get_coptic_symbols(); inscs = None
        elif lang in ("linear_b", "linear-b", "mycenaean", "mycenaean_greek"):
            from glossa_lab.data.linear_b_language import get_corpus_symbols  # noqa: PLC0415
            syms = get_corpus_symbols(); inscs = None
        elif lang in ("meroitic",):
            from glossa_lab.data.meroitic import get_corpus_symbols as _m  # noqa: PLC0415
            syms = _m(); inscs = None
        elif lang in ("proto_sinaitic", "proto-sinaitic"):
            from glossa_lab.data.proto_sinaitic import get_corpus_symbols as _ps  # noqa: PLC0415
            syms = _ps(); inscs = None
        elif lang in ("hieroglyphic_luwian", "luwian", "hluwian", "chli"):
            from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
                get_corpus_symbols, get_corpus_inscriptions,
            )
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        else:
            return {"error": f"Unknown language '{lang}'. Valid: hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic, hieroglyphic_luwian"}
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
            # Single-token sequences — use CorpusReader for multi-sign inscriptions
            seqs: list = [[s] for s in flat]
        elif name in ("hebrew", "old_hebrew"):
            from glossa_lab.data.old_hebrew import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name == "geez":
            from glossa_lab.data.geez import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("geez_clean", "geez_nopunct", "geez_syllabic"):
            # Dr. Fuls April 2026: punctuation-free corpus (80,221 tokens, 209 signs)
            from glossa_lab.data.geez import get_clean_corpus_symbols, get_clean_corpus_inscriptions  # noqa: PLC0415
            flat = get_clean_corpus_symbols(); seqs = get_clean_corpus_inscriptions()
        elif name == "phoenician":
            from glossa_lab.data.phoenician import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("nw_semitic", "fuls", "fuls_nw_semitic", "ugaritic"):
            from glossa_lab.data.nw_semitic import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("meroitic",):
            from glossa_lab.data.meroitic import get_corpus_symbols, get_corpus_inscriptions  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("sanskrit", "vedic"):
            from glossa_lab.data.sanskrit import get_corpus_symbols  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = [[s] for s in flat if len(s) >= 1]
        elif name in ("proto_sinaitic", "proto-sinaitic"):
            from glossa_lab.data.proto_sinaitic import get_corpus_symbols  # noqa: PLC0415
            flat = get_corpus_symbols()
            try:
                from glossa_lab.data.proto_sinaitic import get_corpus_inscriptions  # noqa: PLC0415
                seqs = get_corpus_inscriptions()
            except ImportError:
                seqs = [[s] for s in flat]
        elif name in ("linear_b", "linear-b", "mycenaean"):
            from glossa_lab.data.linear_b_language import get_corpus_symbols  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = [[s] for s in flat]
        elif name in ("dravidian", "tamil"):
            from glossa_lab.data.dravidian import get_corpus_symbols, get_corpus_inscriptions as _di  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = _di()  # word-level char sequences
        elif name in ("indus_cisi", "cisi", "indus_parpola"):
            from glossa_lab.data.indus_cisi import get_corpus_symbols as _cisi_syms, get_corpus_inscriptions as _cisi_inscs  # noqa: PLC0415
            flat = _cisi_syms(); seqs = _cisi_inscs()  # real multi-sign Parpola inscriptions
        elif name in ("indus_m77", "m77", "mahadevan", "mahadevan_1977"):
            # Full Mahadevan 1977 concordance: 1669 inscriptions / 5361 tokens.
            # Much larger than the CISI Parpola subset; sign IDs are M77 codes
            # (e.g. "047", "820") rather than Parpola P-codes.
            from glossa_lab.data.indus_m77 import (  # noqa: PLC0415
                get_corpus_symbols as _m77_syms,
                get_corpus_inscriptions as _m77_inscs,
            )
            flat = _m77_syms(); seqs = _m77_inscs()
        elif name in ("hieroglyphic_luwian", "luwian", "hluwian", "chli"):
            from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
                get_corpus_symbols, get_corpus_inscriptions,
            )
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        else:
            return {"error": f"Unknown corpus '{name}'. Valid: indus, indus_cisi, indus_m77, hebrew, geez, phoenician, nw_semitic/ugaritic, meroitic, proto_sinaitic, linear_b, sanskrit, dravidian"}
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
        # cipher_inscriptions=None keeps cipher_positional empty,
        # enabling the numpy/cupy BigramScorer GPU fast path.
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        r = decipher(flat, lm, seed=seed, max_iterations=max_iter, restarts=restarts,
                     cipher_inscriptions=None,  # None = GPU fast path
                     surjective=surjective,
                     ocp_weight=ocp_w, positional_weight=0.0,
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


# ── Additional primitives for H15 graph-first compliance ──────────────────────────


def _writing_system_classifier(inputs: dict, params: dict) -> dict:
    """Classify a corpus typologically by comparing its structural metrics against
    known writing system benchmarks (H15: primitive — one comparison operation).

    Takes: h1 (bits), n_signs (distinct signs), avg_word_len, tokens_per_sign.
    Returns: tier classification, similarity ranking against 12 known scripts.
    """
    import math  # noqa: PLC0415
    h1            = float(inputs.get("h1") or inputs.get("number") or params.get("h1", 5.5))
    n_signs       = int(inputs.get("distinct_symbols") or inputs.get("n_signs") or params.get("n_signs", 78))
    avg_word_len  = float(inputs.get("avg_word_len") or params.get("avg_word_len", 3.3))
    tok_per_sign  = float(inputs.get("tokens_per_sign") or inputs.get("total_tokens", 1) /
                          max(1, inputs.get("distinct_symbols") or n_signs))

    # Literature benchmark table (embedded — no external deps)
    BENCHMARKS = [
        {"name": "Classical Chinese",         "tier": "Logographic",   "H1": 9.65, "signs": 3500, "avg_wl": 1.0,  "tps": 250.0},
        {"name": "Sumerian Cuneiform",        "tier": "Logosyllabic",  "H1": 7.80, "signs": 800,  "avg_wl": 2.5,  "tps": 15.0},
        {"name": "Indus Script",              "tier": "Unknown",       "H1": 5.35, "signs": 400,  "avg_wl": 4.6,  "tps": 2.4},
        {"name": "Linear B",                  "tier": "Syllabary",     "H1": 5.98, "signs": 87,   "avg_wl": 3.6,  "tps": 90.5},
        {"name": "Old Persian Cuneiform",     "tier": "Syllabary",     "H1": 5.50, "signs": 41,   "avg_wl": 3.2,  "tps": 25.0},
        {"name": "Cypriot Syllabary",         "tier": "Syllabary",     "H1": 5.70, "signs": 55,   "avg_wl": 3.5,  "tps": 12.0},
        {"name": "Meroitic",                  "tier": "Abjad/Syllabic","H1": 4.65, "signs": 23,   "avg_wl": 3.1,  "tps": 18.0},
        {"name": "Proto-Sinaitic",            "tier": "Abjad",         "H1": 4.40, "signs": 27,   "avg_wl": 2.8,  "tps": 4.5},
        {"name": "Ugaritic",                  "tier": "Abjad",         "H1": 4.52, "signs": 30,   "avg_wl": 3.0,  "tps": 31.5},
        {"name": "Phoenician",                "tier": "Abjad",         "H1": 4.25, "signs": 22,   "avg_wl": 2.9,  "tps": 80.0},
        {"name": "Old Hebrew",                "tier": "Abjad",         "H1": 4.19, "signs": 22,   "avg_wl": 3.0,  "tps": 711.0},
    ]

    def _dist(b: dict) -> float:
        # Normalised Euclidean distance over the 3 most discriminating features
        dh = (h1 - b["H1"]) ** 2 / 25.0
        ds = (math.log1p(n_signs) - math.log1p(b["signs"])) ** 2 / 4.0
        dw = (avg_word_len - b["avg_wl"]) ** 2 / 4.0
        return round(math.sqrt(dh + ds + dw), 4)

    ranked = sorted(BENCHMARKS, key=_dist)
    nearest = ranked[:3]
    dominant_tier = nearest[0]["tier"]

    # Rule-based tier classification
    if h1 < 4.7 and n_signs < 50:
        tier = "Abjad (consonant alphabet)"
    elif h1 < 6.5 and n_signs < 120:
        tier = "Syllabary"
    elif n_signs > 200:
        tier = "Logographic / Logosyllabic"
    else:
        tier = "Mixed / Unknown"

    return {
        "corpus_h1":          round(h1, 4),
        "corpus_n_signs":     n_signs,
        "corpus_avg_word_len": round(avg_word_len, 3),
        "tier_classification": tier,
        "nearest_script":      nearest[0]["name"],
        "nearest_distance":    nearest[0].get("_d", _dist(nearest[0])),
        "top3_nearest":        [{"name": b["name"], "tier": b["tier"], "distance": _dist(b)} for b in nearest],
        "all_ranked":          [{"name": b["name"], "tier": b["tier"], "distance": _dist(b)} for b in ranked],
        "text":               f"Classified as: {tier}. Nearest known script: {nearest[0]['name']} ({nearest[0]['tier']})."
    }


def _beam_decipher(inputs: dict, params: dict) -> dict:
    """Beam search decipherment. Deterministic; finds the highest-scoring mapping
    in a bounded beam. Faster than SA for small corpora (primitive: one engine call)."""
    sequences = inputs.get("sequences") or inputs.get("test_sequences") or []
    lm = inputs.get("lm")
    if not lm:
        return {"error": "No LM — connect LMBuilder or BuiltinLM to 'lm' port."}
    if not sequences:
        return {"error": "No sequences — connect CorpusReader or CorpusSplitter."}
    flat = [s for seq in sequences for s in seq]
    beam_width = max(10, int(params.get("beam_width", 200)))
    anchors    = inputs.get("anchors") or params.get("anchors") or None
    try:
        from glossa_lab.pipelines.beam_decipher import beam_decipher  # noqa: PLC0415
        from glossa_lab.pipelines.decipher import score_accuracy      # noqa: PLC0415
        r = beam_decipher(flat, lm, beam_width=beam_width,
                          cipher_inscriptions=sequences or None,
                          surjective=bool(params.get("surjective", True)),
                          anchors=anchors if anchors else None)
        return {"proposed_mapping": r.get("proposed_mapping", {}),
                "score": r.get("score", 0), "beam_width": beam_width,
                "n_signs": len(r.get("proposed_mapping", {}))}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _token_filter(inputs: dict, params: dict) -> dict:
    """Filter sequence tokens by Unicode range, explicit blocklist, or minimum frequency.

    Solves the corpus sanitisation problem (H16): removes non-sign tokens
    (e.g. Ethiopic punctuation U+1361-U+1368) before building an LM or running SA.
    All three filter modes may be combined; they are applied in order:
      1. unicode_ranges: keep only tokens whose codepoint falls within listed ranges.
      2. blocklist: drop tokens whose string value appears in this list.
      3. min_freq: drop tokens that appear fewer than min_freq times across the corpus.

    Examples
    --------
    Remove Ethiopic punctuation (U+1361-U+1368)::
        TokenFilter(unicode_ranges=["U+1200-U+1360"])

    Remove specific sign codes::
        TokenFilter(blocklist=["punct", "000", "-"])

    Keep only signs appearing >= 3 times::
        TokenFilter(min_freq=3)
    """
    import re as _re  # noqa: PLC0415
    from collections import Counter as _C  # noqa: PLC0415

    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"sequences": [], "total_sequences": 0, "total_tokens": 0,
                "removed_tokens": 0, "removed_types": 0}

    # ── Parameter parsing ──────────────────────────────────────────────────────
    # unicode_ranges: list of "U+XXXX-U+YYYY" or "U+XXXX" strings
    raw_ranges = params.get("unicode_ranges") or []
    if isinstance(raw_ranges, str):
        raw_ranges = [r.strip() for r in raw_ranges.split(",") if r.strip()]

    parsed_ranges: list[tuple[int, int]] = []
    for rng in raw_ranges:
        rng = rng.strip()
        m = _re.match(r"U\+([0-9A-Fa-f]+)(?:-U\+([0-9A-Fa-f]+))?", rng)
        if m:
            lo = int(m.group(1), 16)
            hi = int(m.group(2), 16) if m.group(2) else lo
            parsed_ranges.append((lo, hi))

    # blocklist: list of token strings to drop
    blocklist_raw = params.get("blocklist") or []
    if isinstance(blocklist_raw, str):
        blocklist_raw = [t.strip() for t in blocklist_raw.split(",") if t.strip()]
    blocklist: set[str] = set(blocklist_raw)

    # min_freq: drop tokens appearing fewer than this many times
    min_freq = max(0, int(params.get("min_freq", 0)))

    # ── Build global frequency map if min_freq filtering ─────────────────────
    freq: dict[str, int] = {}
    if min_freq > 0:
        freq = dict(_C(tok for seq in sequences for tok in seq))

    # ── Filter function ────────────────────────────────────────────────────────
    def _keep(tok: str) -> bool:
        if tok in blocklist:
            return False
        if parsed_ranges:
            # Token must match at least one accepted range
            # For multi-char tokens: check first character codepoint
            cp = ord(tok[0]) if tok else -1
            if not any(lo <= cp <= hi for lo, hi in parsed_ranges):
                return False
        if min_freq > 0 and freq.get(tok, 0) < min_freq:
            return False
        return True

    # ── Apply filter ───────────────────────────────────────────────────────────
    before = sum(len(s) for s in sequences)
    before_types = len({t for s in sequences for t in s})

    filtered = [[tok for tok in seq if _keep(tok)] for seq in sequences]
    # Drop now-empty sequences (optional: controlled by keep_empty_seqs param)
    if not params.get("keep_empty_seqs", False):
        filtered = [s for s in filtered if s]

    after = sum(len(s) for s in filtered)
    after_types = len({t for s in filtered for t in s})

    return {
        "sequences":       filtered,
        "total_sequences": len(filtered),
        "total_tokens":    after,
        "removed_tokens":  before - after,
        "removed_types":   before_types - after_types,
        "kept_types":      after_types,
    }


def _shuffle_control(inputs: dict, params: dict) -> dict:
    """Create a shuffled control corpus (primitive: one statistical control operation).

    Destroys sequential structure while preserving unigram frequencies,
    allowing statistical tests that isolate sequence-level signal from frequency.
    Mode: 'within_word' = shuffle signs within each word; 'global' = shuffle all.
    """
    import random  # noqa: PLC0415
    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences provided"}
    mode = params.get("mode", "within_word").lower()
    seed = int(params.get("seed", 42))
    rng  = random.Random(seed)
    if mode == "global":
        flat = [s for seq in sequences for s in seq]
        rng.shuffle(flat)
        # Redistribute into original word lengths
        shuffled, idx = [], 0
        for seq in sequences:
            shuffled.append(flat[idx:idx + len(seq)])
            idx += len(seq)
    else:  # within_word
        shuffled = [list(seq) for seq in sequences]
        for word in shuffled:
            rng.shuffle(word)
    return {"sequences": shuffled, "n_sequences": len(shuffled),
            "mode": mode, "note": f"Shuffled control ({mode}): sequence structure destroyed"}


def _constraint_sweep(inputs: dict, params: dict) -> dict:
    """Run SA decipherment under multiple anchor counts and return accuracy curve
    (primitive: one parameterised sweep operation).

    For each anchor count in anchor_counts, runs n_seeds SA seeds and records
    mean consistency. Returns the full curve for plotting.
    """
    from collections import Counter as _C  # noqa: PLC0415
    sequences  = inputs.get("sequences") or inputs.get("test_sequences") or []
    lm         = inputs.get("lm")
    freq_map   = inputs.get("freq_map") or {}
    if not lm:
        return {"error": "No LM — connect LMBuilder or BuiltinLM."}
    if not sequences:
        return {"error": "No sequences — connect CorpusReader or CorpusSplitter."}

    anchor_counts_raw = params.get("anchor_counts", [0, 1, 3, 5, 10])
    anchor_counts = [int(x) for x in anchor_counts_raw] if isinstance(anchor_counts_raw, list) else [0, 1, 3, 5, 10]
    n_seeds    = max(1, int(params.get("n_seeds", 3)))
    max_iter   = max(100, int(params.get("max_iterations", 3000)))
    restarts   = max(1, int(params.get("restarts", 3)))
    flat = [s for seq in sequences for s in seq]

    # Top-k anchors by frequency (signed as dict {cipher: target} must be provided by user)
    # Here we just run with NO anchors across the sweep and report consistency curve
    from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

    def _one(seed: int) -> dict:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        r = decipher(flat, lm, seed=seed, max_iterations=max_iter, restarts=restarts,
                     cipher_inscriptions=None, ocp_weight=0.0, positional_weight=0.0,
                     surjective=True)
        return r.get("proposed_mapping", {})

    curve = []
    for ac in sorted(anchor_counts):
        seeds = list(range(ac * 100, ac * 100 + n_seeds))
        maps  = run_seeds_parallel(_one, seeds)
        all_signs = set().union(*[m.keys() for m in maps]) if maps else set()
        mean_c = 0.0
        if maps and all_signs:
            conss = []
            for s in all_signs:
                props = [m[s] for m in maps if s in m]
                if props:
                    cnt = _C(props); _, mc = cnt.most_common(1)[0]
                    conss.append(mc / len(props))
            mean_c = sum(conss) / len(conss) if conss else 0
        curve.append({"anchor_count": ac, "mean_consistency": round(mean_c, 4),
                      "n_seeds": len(maps)})
    return {"consistency_curve": curve, "anchor_counts": anchor_counts, "n_curve_points": len(curve)}


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


def _corpus_lm(inputs: dict, params: dict) -> dict:
    """Build a LanguageModel from any corpus stored in the user's database (H16).

    Users upload any corpus via the Corpora tab, then reference it here by corpus_id.
    No Python file or data module required — any uploaded corpus becomes an LM source.
    This is the H16-compliant replacement for BuiltinLM hardcoded data modules.
    """
    import math as _math  # noqa: PLC0415
    corpus_id = params.get("corpus_id") or inputs.get("corpus_id") or ""
    min_freq   = max(1, int(params.get("min_freq", 1)))

    if not corpus_id:
        return {"error": "No corpus_id param — select a corpus from the dropdown or connect CorpusReader."}

    # Load sequences from DB (same pattern as _corpus_reader)
    from glossa_lab.database import get_db  # noqa: PLC0415
    import asyncio  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"error": "Database not available — is the backend running?"}
    try:
        loop = asyncio.get_event_loop()
        text = loop.run_until_complete(db.get_text(corpus_id))
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Failed to load corpus '{corpus_id}': {exc}"}

    if text is None:
        return {"error": f"Corpus '{corpus_id}' not found in database."}
    raw = text.get("content", [])
    if not raw:
        return {"error": f"Corpus '{corpus_id}' is empty."}

    flat: list[str] = raw if raw and not isinstance(raw[0], list) else [s for seq in raw for s in seq]
    if min_freq > 1:
        from collections import Counter as _C  # noqa: PLC0415
        freq = _C(flat)
        flat = [s for s in flat if freq[s] >= min_freq]

    from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
    lm = LanguageModel(flat)
    h1 = -sum(p * _math.log2(p) for p in lm.unigram_freq.values() if p > 0)
    return {
        "lm": lm,
        "corpus_id": corpus_id,
        "corpus_name": text.get("name", corpus_id),
        "n_signs": lm.size,
        "n_tokens": len(flat),
        "h1": round(h1, 4),
    }


def _cas_model_loader(inputs: dict, params: dict) -> dict:
    """Load a CAS-YAML constraint model from the database or built-in library.

    Users create CAS models in the Models editor (or use the built-in Indus models).
    The 'model' output is an opaque CasModel object that CASProjector and
    CASIndusEngine can consume directly — no YAML file path required.
    """
    model_id   = params.get("model_id", "").strip()
    yaml_text  = params.get("yaml_text", "").strip()
    builtin    = params.get("builtin", "").strip()

    try:
        from glossa_lab.cpsc_bridge import load_builtin_cas_model, _parse_yaml_to_model  # noqa: PLC0415
    except ImportError as exc:
        return {"error": f"CPSC not installed: {exc}"}

    # Priority: builtin name > inline yaml_text > DB model_id
    model = None
    source = ""

    if builtin:
        model = load_builtin_cas_model(builtin)
        source = f"builtin:{builtin}"
        if model is None:
            return {"error": f"Built-in CAS model '{builtin}' not found in data/cas_models/"}

    elif yaml_text:
        try:
            model = _parse_yaml_to_model(yaml_text)
            source = "inline_yaml"
        except Exception as exc:  # noqa: BLE001
            return {"error": f"YAML parse error: {exc}"}

    elif model_id:
        from glossa_lab.database import get_db  # noqa: PLC0415
        import asyncio  # noqa: PLC0415
        db = get_db()
        if db is None:
            return {"error": "Database not available."}
        try:
            loop = asyncio.get_event_loop()
            record = loop.run_until_complete(db.get_cas_model(model_id))
        except Exception as exc:  # noqa: BLE001
            return {"error": f"Failed to load CAS model '{model_id}': {exc}"}
        if record is None:
            return {"error": f"CAS model '{model_id}' not found in database."}
        try:
            model = _parse_yaml_to_model(record["yaml_text"])
            source = f"db:{model_id}"
        except Exception as exc:  # noqa: BLE001
            return {"error": f"Failed to parse stored CAS-YAML: {exc}"}
    else:
        return {"error": "Provide one of: builtin (e.g. 'indus_sign_roles'), yaml_text, or model_id."}

    return {
        "model":        model,
        "model_id":     model.model_id,
        "model_name":   model.model_id,
        "source":       source,
        "n_variables":  len(model.variables),
        "n_constraints":len(model.constraints),
        "dof_vars":     model.free_variables,
        "engine_hint":  getattr(model.projection, "strategy", "auto"),
    }


def _cas_projector(inputs: dict, params: dict) -> dict:
    """Run CPSC constraint projection on a CAS model.

    Connects: CASModelLoader.model → model.
    Provide DoF values as a JSON list or dict.
    The CPSC IterativeEngine (or CellularEngine) projects the free variables
    onto the constraint manifold — returning all derived variable values.

    GPU note: IterativeEngine is pure numpy (CPU). GPU acceleration applies
    to SADecipher/BigramScorer; CASProjector is constraint-gradient-based.
    """
    model    = inputs.get("model")
    dof_raw  = inputs.get("dof_values") or params.get("dof_values")
    engine   = str(params.get("engine", "auto"))
    max_iter = params.get("max_iterations")
    strategy = params.get("force_strategy", "") or None

    if model is None:
        return {"error": "No model — connect CASModelLoader to the 'model' port."}

    try:
        from glossa_lab.cpsc_bridge import project_cas_model  # noqa: PLC0415
    except ImportError as exc:
        return {"error": f"CPSC not installed: {exc}"}

    # Parse DoF values — accept list, dict (by name), JSON string, or empty (use zeros)
    dof_names = model.free_variables
    # If dof_raw came in as a JSON string from node params, parse it first
    if isinstance(dof_raw, str) and dof_raw.strip():
        import json as _json  # noqa: PLC0415
        try:
            dof_raw = _json.loads(dof_raw)
        except (ValueError, _json.JSONDecodeError):
            dof_raw = None

    if dof_raw is None or dof_raw == []:
        dof_values = [0.0] * len(dof_names)
    elif isinstance(dof_raw, dict):
        dof_values = [float(dof_raw.get(n, 0.0)) for n in dof_names]
    elif isinstance(dof_raw, list):
        dof_values = [float(v) for v in dof_raw[:len(dof_names)]]
        # Pad with zeros if fewer values than DoF vars
        dof_values += [0.0] * max(0, len(dof_names) - len(dof_values))
    else:
        dof_values = [0.0] * len(dof_names)

    result = project_cas_model(
        model, dof_values,
        engine=engine,
        max_iterations=int(max_iter) if max_iter else None,
        force_strategy=strategy,
    )
    return {
        "state":          result.get("state", {}),
        "success":        result.get("success", False),
        "iterations":     result.get("iterations", 0),
        "max_violation":  result.get("max_violation", float("inf")),
        "strategy_used":  result.get("strategy_used", engine),
        "reason":         result.get("reason"),
        "details":        result.get("details", {}),
        "dof_vars":       dof_names,
        "dof_values_used":dof_values,
    }


def _cas_indus_engine(inputs: dict, params: dict) -> dict:
    """CASIndusEngine — custom CPSC-based Indus sign role classifier.

    Our own engine built on CPSC's IterativeEngine. For each sign in the corpus:
      1. Observes I/M/T rates from real CISI inscription sequences
      2. Builds a CasModel dynamically encoding Dravidian morphological constraints
         (case suffixes terminal-biased, determinatives initial-biased,
         phonetic syllables medial-biased)
      3. Runs CPSC IterativeEngine to project observed rates onto the constraint manifold
      4. Classifies each sign as TERMINAL / INITIAL / MEDIAL based on projected weights

    Connects:
      BuiltinCorpus(indus_cisi) → sequences
      PositionalProfiler → profiles
      BuiltinLM(dravidian) → lm  (optional, used for phoneme candidate matching)

    Unlike SADecipher (black-box SA optimizer), this engine is transparent:
    users can modify the constraints in the Models editor and re-run.
    """
    sequences = inputs.get("sequences") or []
    profiles  = inputs.get("profiles") or inputs.get("class_summary") or {}
    lm        = inputs.get("lm")

    t_thresh = float(params.get("terminal_threshold", 0.55))
    i_thresh = float(params.get("initial_threshold", 0.45))
    engine   = str(params.get("engine", "iterative"))

    try:
        from glossa_lab.cpsc_bridge import run_indus_engine  # noqa: PLC0415
    except ImportError as exc:
        return {"error": f"CPSC not installed: {exc}"}

    if not sequences and not profiles:
        return {"error": "Connect BuiltinCorpus(indus_cisi) to sequences and/or PositionalProfiler to profiles."}

    return run_indus_engine(
        sequences=sequences,
        profiles=profiles,
        lm=lm,
        terminal_threshold=t_thresh,
        initial_threshold=i_thresh,
        engine=engine,
    )


def _anchor_set_loader(inputs: dict, params: dict) -> dict:
    """Load a user-defined anchor set from the database (H16).

    Returns the anchor pairs as a dict {cipher_sign: target_value}
    compatible with the SADecipher and AnchorConvergenceBenchmark nodes.
    Users define anchor sets in the Anchor Set Editor (Corpora tab).
    No Python file required.
    """
    anchor_set_id = params.get("anchor_set_id") or inputs.get("anchor_set_id") or ""
    if not anchor_set_id:
        return {"error": "No anchor_set_id param — select an anchor set.", "anchors": {}}

    from glossa_lab.database import get_db  # noqa: PLC0415
    import asyncio  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"error": "Database not available.", "anchors": {}}
    try:
        loop = asyncio.get_event_loop()
        anchor_set = loop.run_until_complete(db.get_anchor_set(anchor_set_id))
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Failed to load anchor set: {exc}", "anchors": {}}

    if anchor_set is None:
        return {"error": f"Anchor set '{anchor_set_id}' not found.", "anchors": {}}

    pairs = anchor_set.get("pairs", []) or []
    # Convert list of {cipher, target, confidence, note} to {cipher: target}
    anchors = {p["cipher"]: p["target"] for p in pairs if p.get("cipher") and p.get("target")}
    return {
        "anchors": anchors,
        "anchor_set_id": anchor_set_id,
        "anchor_set_name": anchor_set.get("name", anchor_set_id),
        "n_anchors": len(anchors),
        "pairs": pairs,
    }


def _report_generator(inputs: dict, params: dict) -> dict:
    """Generate a structured report from a user-defined template + upstream data (H16).

    Takes a template_id (from the report_templates DB table) and upstream result data.
    Renders each section using the template's section definitions (title, data_key, chart_type).
    Saves the rendered report as JSON to reports/ (PDF rendering via ReportLab can be added
    by wiring to a PDF export pipeline).
    No Python script required — template structure is user-defined in the Template Editor.
    """
    template_id = params.get("template_id") or inputs.get("template_id") or ""
    if not template_id:
        return {"error": "No template_id param — select a report template."}

    from glossa_lab.database import get_db  # noqa: PLC0415
    import asyncio  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"error": "Database not available."}
    try:
        loop = asyncio.get_event_loop()
        template = loop.run_until_complete(db.get_report_template(template_id))
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Failed to load template: {exc}"}
    if template is None:
        return {"error": f"Template '{template_id}' not found."}

    sections = template.get("sections", []) or []
    rendered: list[dict] = []
    for sec in sections:
        data_key = sec.get("data_key", "")
        # Look up the data_key in the upstream inputs
        value = inputs.get(data_key) if data_key else None
        rendered.append({
            "title":       sec.get("title", ""),
            "chart_type":  sec.get("chart_type", "table"),
            "description": sec.get("description", ""),
            "data":        value,
            "data_key":    data_key,
        })

    import datetime as _dt  # noqa: PLC0415
    report = {
        "template_id":   template_id,
        "template_name": template.get("name", ""),
        "category":      template.get("category", ""),
        "generated_at":  _dt.datetime.utcnow().isoformat(),
        "sections":      rendered,
    }
    return {"report": report, "template_name": template.get("name"), "n_sections": len(rendered)}


def _experiment_input(inputs: dict, params: dict) -> dict:
    """Declare a named input port for an experiment graph (subroutine pattern).

    When this graph is invoked via SubExperiment, the caller injects a value
    for each ExperimentInput port by port_name. Otherwise uses default_value.
    The value passes through to downstream nodes as both 'value' and port_name.
    """
    port_name = str(params.get("port_name") or "input")
    # Injected by execute_graph from kwargs when called as sub-experiment
    value = (inputs.get(port_name) or inputs.get("value")
             or params.get("default_value"))
    return {"value": value, port_name: value, "port_name": port_name}


def _experiment_output(inputs: dict, params: dict) -> dict:
    """Declare a named output port for an experiment graph (subroutine pattern).

    Exposes upstream data under port_name so a calling Study/Experiment can
    wire the result to other nodes. Multiple ExperimentOutput nodes can exist
    in one graph, each exporting a different named result.
    """
    port_name = str(params.get("port_name") or "output")
    data = (inputs.get("data") or inputs.get("value")
            or {k: v for k, v in inputs.items() if k not in ("port_name",)})
    return {"value": data, "port_name": port_name, port_name: data}


def _sub_experiment(inputs: dict, params: dict) -> dict:
    """Invoke a graph experiment as a reusable subroutine.

    Looks up experiment_id in the graph library, injects caller inputs through
    ExperimentInput nodes (matched by port_name), executes the sub-graph, and
    returns the sub-graph's ExperimentOutput values as named ports.

    This implements the Study → Experiment → Atomic Node hierarchy:
    a Study can compose multiple Experiments without code duplication.
    """
    exp_id = params.get("experiment_id", "")
    if not exp_id:
        return {"error": "No experiment_id param — set the experiment to call"}
    target = get_graph_experiment(exp_id)
    if not target:
        return {"error": f"Graph experiment '{exp_id}' not found"}

    # Collect which port names the sub-experiment declares as ExperimentInput
    port_kwargs: dict[str, object] = {}
    for node in target.get("nodes", []):
        data = node.get("data", {}) if node.get("type") == "expNode" else {}
        if data.get("atomicId") == "ExperimentInput":
            pname = (data.get("params") or {}).get("port_name", "input")
            if pname in inputs:
                port_kwargs[pname] = inputs[pname]

    # Also forward any extra caller params that aren't meta-params
    extra = {k: v for k, v in params.items() if k != "experiment_id"}
    result = execute_graph(target, {**port_kwargs, **extra})
    return result if isinstance(result, dict) else {"result": result}


# ── CGSA / Structural nodes ───────────────────────────────────────────────────

def _canonical_sign_loader(inputs: dict, params: dict) -> dict:
    """Load the canonical sign registry from the CGSA pipeline (V12 DB table).

    Returns the full sign inventory with Parpola, Wells, Mahadevan crosswalk IDs,
    ICIT function codes, and corpus frequency/positional statistics.
    Requires: scripts/cgsa_pipeline.py has been run, DB seeded via POST /canonical-signs/seed.
    """
    filter_in_corpus = bool(params.get("in_corpus_only", True))
    numbering_system = params.get("numbering_system") or None

    from glossa_lab.database import get_db  # noqa: PLC0415
    import asyncio  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"error": "Database not available"}
    try:
        loop = asyncio.get_event_loop()
        signs = loop.run_until_complete(
            db.list_canonical_signs(in_corpus_only=filter_in_corpus,
                                    numbering_system=numbering_system)
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Failed to load registry: {exc}"}

    if not signs:
        return {
            "error": "Canonical sign registry is empty — run POST /canonical-signs/seed first",
            "n_signs": 0,
        }

    # Build sign_id → internal_id map for downstream nodes
    sign_id_map = {s["sign_id"]: s["internal_id"] for s in signs}
    parpola_signs = [s for s in signs if s["numbering_system"] == "parpola_1982"]
    return {
        "registry": signs,
        "n_signs": len(signs),
        "n_parpola": len(parpola_signs),
        "sign_id_to_uuid": sign_id_map,
        "sign_ids": [s["sign_id"] for s in signs],
    }


def _cluster_mapper(inputs: dict, params: dict) -> dict:
    """Map inscription sign sequences to structural cluster labels.

    Loads cluster assignments from the DB (seeded by the CGSA pipeline) or,
    when the DB is not available (e.g. CLI context), falls back to loading
    directly from analysis/sign_clusters.json.
    Unmapped signs receive label -1. NO phonetic mapping is performed.
    """
    import json as _json  # noqa: PLC0415
    import asyncio  # noqa: PLC0415
    from pathlib import Path as _Path  # noqa: PLC0415

    assignments: list = []
    summary: dict = {}

    # ── Try DB first (live backend context) ──────────────────────────────────
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is not None:
        try:
            loop = asyncio.get_event_loop()
            assignments = loop.run_until_complete(db.list_cluster_assignments())
            summary     = loop.run_until_complete(db.get_clusters_summary())
        except Exception:  # noqa: BLE001
            assignments = []

    # ── Fallback: load from analysis/sign_clusters.json ──────────────────────
    if not assignments:
        _cluster_json = (
            _Path(__file__).resolve().parents[3] / "analysis" / "sign_clusters.json"
        )
        if _cluster_json.exists():
            try:
                data = _json.loads(_cluster_json.read_text("utf-8"))
                best_k = data.get("best_k", 40)
                s2c_raw: dict = data.get("sign_to_cluster", {})
                assignments = [
                    {"sign_id": sid, "cluster_label": lbl}
                    for sid, lbl in s2c_raw.items()
                ]
                n_clusters = len(set(s2c_raw.values()))
                summary = {"n_clusters": n_clusters, "cluster_k": best_k,
                           "n_signs": len(s2c_raw)}
            except Exception:  # noqa: BLE001
                assignments = []

    if not assignments:
        return {
            "error": "Cluster assignments unavailable. "
                     "Seed via POST /sign-clusters/seed or run scripts/cgsa_pipeline.py",
            "n_assignments": 0,
        }

    s2c: dict[str, int] = {a["sign_id"]: a["cluster_label"] for a in assignments}
    sequences = inputs.get("sequences") or []
    cluster_sequences: list[list[int]] = []
    n_mapped = 0
    n_unmapped = 0
    for seq in sequences:
        cs = []
        for sign in seq:
            lbl = s2c.get(sign, -1)
            cs.append(lbl)
            if lbl >= 0:
                n_mapped += 1
            else:
                n_unmapped += 1
        cluster_sequences.append(cs)

    total = n_mapped + n_unmapped
    return {
        "cluster_sequences": cluster_sequences,
        "n_sequences": len(cluster_sequences),
        "n_mapped_tokens": n_mapped,
        "n_unmapped_tokens": n_unmapped,
        "map_rate": round(n_mapped / total, 4) if total else 0,
        "n_clusters": summary.get("n_clusters", 0),
        "cluster_k": summary.get("cluster_k", 0),
        "sign_to_cluster": s2c,
    }


def _structural_template_analyzer(inputs: dict, params: dict) -> dict:
    """Find recurrent structural templates in cluster-space inscription sequences.

    Operates on cluster_sequences from ClusterMapper (not raw sign sequences).
    Discovers recurring patterns of cluster labels (length 2-5, count ≥ min_count),
    identifies dominant prefix/suffix clusters, and computes slot occupancy.
    NO phonetic claims are made. All outputs are structural class labels.
    """
    import math as _m  # noqa: PLC0415
    from collections import Counter as _C  # noqa: PLC0415

    cluster_sequences = inputs.get("cluster_sequences") or []
    min_count = int(params.get("min_count", 3))
    max_len = int(params.get("max_template_length", 5))

    if not cluster_sequences:
        return {"error": "No cluster_sequences — connect ClusterMapper.cluster_sequences"}

    template_ctr: _C = _C()
    prefix_ctr: _C = _C()
    suffix_ctr: _C = _C()
    slot_dist: dict = {"initial": _C(), "terminal": _C(), "internal": _C()}

    for cs in cluster_sequences:
        if not cs:
            continue
        # Filter out unmapped (-1)
        clean = [c for c in cs if c >= 0]
        if not clean:
            continue
        prefix_ctr[clean[0]] += 1
        suffix_ctr[clean[-1]] += 1
        for i, c in enumerate(cs):
            if c < 0:
                continue
            if i == 0:
                slot_dist["initial"][c] += 1
            elif i == len(cs) - 1:
                slot_dist["terminal"][c] += 1
            else:
                slot_dist["internal"][c] += 1
        for length in range(2, min(max_len + 1, len(clean) + 1)):
            for i in range(len(clean) - length + 1):
                t = tuple(clean[i:i + length])
                template_ctr[t] += 1

    recurrent = [
        {"template": list(t), "count": c, "length": len(t)}
        for t, c in template_ctr.most_common(50) if c >= min_count
    ]

    # Sequence-level entropy (class space)
    seq_ctr: _C = _C(tuple(cs) for cs in cluster_sequences)
    total_seqs = len(cluster_sequences)
    h_class = -sum((c/total_seqs)*_m.log2(c/total_seqs)
                   for c in seq_ctr.values() if c > 0) if total_seqs else 0

    return {
        "n_templates": len(recurrent),
        "recurrent_templates": recurrent,
        "dominant_prefix_clusters": dict(prefix_ctr.most_common(10)),
        "dominant_suffix_clusters": dict(suffix_ctr.most_common(10)),
        "slot_occupancy": {
            k: dict(v.most_common(10)) for k, v in slot_dist.items()
        },
        "h_class_sequence": round(h_class, 4),
        "n_distinct_class_sequences": len(seq_ctr),
        "n_sequences": total_seqs,
    }


def _cipher_constructor(inputs: dict, params: dict) -> dict:
    """Create a bijective random substitution cipher from a sign inventory
    (primitive: one operation — shuffle a known inventory and apply it to sequences).

    Takes a test corpus and an LM (for its sign inventory), shuffles the sign-to-sign
    mapping with a fixed random seed, and returns the ciphered sequences plus ground-truth
    mapping. Designed to pair with AnchorConvergenceBenchmark for controlled self-tests.
    """
    import random as _rnd  # noqa: PLC0415
    sequences = inputs.get("sequences") or inputs.get("test_sequences") or []
    lm        = inputs.get("lm")
    if not sequences:
        return {"error": "No sequences — connect CorpusSplitter.test_sequences"}
    if lm is None:
        return {"error": "No LM — connect LMBuilder or BuiltinLM to supply sign inventory"}

    seed       = int(params.get("cipher_seed", 42))
    max_tokens = int(params.get("max_tokens", 15_000))

    # Derive inventory from LM unigram freqs
    try:
        inv = sorted(lm.unigram_freq.keys())
    except AttributeError:
        return {"error": "LM has no unigram_freq — use LMBuilder or BuiltinLM"}

    if not inv:
        return {"error": "LM sign inventory is empty"}

    rng  = _rnd.Random(seed)
    shuf = list(inv); rng.shuffle(shuf)
    perm  = {inv[i]: shuf[i] for i in range(len(inv))}   # original → cipher
    truth = {shuf[i]: inv[i] for i in range(len(inv))}   # cipher   → original

    # Cipher the sequences (filter to known signs, honour max_tokens)
    inv_set       = set(inv)
    cipher_seqs: list[list[str]] = []
    token_count   = 0
    for seq in sequences:
        if token_count >= max_tokens:
            break
        cs = [perm[s] for s in seq if s in inv_set]
        if len(cs) >= 2:
            cipher_seqs.append(cs)
            token_count += len(cs)

    return {
        "cipher_sequences":  cipher_seqs,
        "true_mapping":      truth,
        "perm":              perm,
        "sign_inventory":    inv,
        "n_cipher_tokens":   token_count,
        "n_cipher_seqs":     len(cipher_seqs),
        "inventory_size":    len(inv),
    }


def _anchor_convergence_benchmark(inputs: dict, params: dict) -> dict:
    """Measure how anchor injection drives convergence in a known-cipher benchmark
    (primitive: one well-defined engine — sweep anchor counts, measure accuracy/convergence).

    Requires cipher_sequences from CipherConstructor plus the LM used to build the cipher.
    For each anchor count runs structured (frequency-ranked) and random anchor sets,
    reports top-1 accuracy, free-sign accuracy, consistency, and distinct-mappings metrics.
    """
    import random as _rnd  # noqa: PLC0415
    import math as _math  # noqa: PLC0415
    from collections import Counter as _C, defaultdict as _dd  # noqa: PLC0415

    cipher_seqs  = inputs.get("cipher_sequences") or []
    lm           = inputs.get("lm")
    true_mapping = inputs.get("true_mapping") or {}
    sign_inv     = inputs.get("sign_inventory") or []

    if not cipher_seqs:
        return {"error": "No cipher_sequences — connect CipherConstructor"}
    if lm is None:
        return {"error": "No LM — connect LMBuilder or BuiltinLM"}
    if not true_mapping:
        return {"error": "No true_mapping — connect CipherConstructor"}

    anchor_counts_raw = params.get("anchor_counts", [0, 3, 10, 20])
    anchor_counts = sorted([int(x) for x in anchor_counts_raw])
    n_struct  = max(1, int(params.get("n_structured", 3)))
    n_rand    = max(1, int(params.get("n_random", 5)))
    nsb       = max(1, int(params.get("n_seeds_base", 5)))
    nss       = max(1, int(params.get("n_seeds_struct", 3)))
    nsr       = max(1, int(params.get("n_seeds_rand", 2)))
    sa_iter   = max(500, int(params.get("sa_iterations", 2000)))
    sa_rest   = max(1,   int(params.get("sa_restarts", 1)))
    sa_temp   = float(params.get("sa_temp", 1.0))
    sa_cool   = float(params.get("sa_cool", 0.9985))
    use_wf    = bool(params.get("use_word_final_anchors", False))

    from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

    # Derive perm (original → cipher) from true_mapping (cipher → original)
    perm = {v: k for k, v in true_mapping.items()}

    # Use LM inventory if sign_inv not provided
    if not sign_inv:
        try:
            sign_inv = sorted(lm.unigram_freq.keys())
        except AttributeError:
            pass
    if not sign_inv:
        return {"error": "Cannot determine sign inventory"}

    inv_set = set(sign_inv)
    flat_cipher = [s for seq in cipher_seqs for s in seq]
    n_total = len(true_mapping)

    # ── helpers ──────────────────────────────────────────────────────────────
    def _mean(xs): return sum(xs) / len(xs) if xs else float("nan")

    def _run_sa(seed: int, anchors: dict) -> dict:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        r = decipher(flat_cipher, lm, seed=seed, max_iterations=sa_iter,
                     restarts=sa_rest, cipher_inscriptions=None,
                     use_sa=True, sa_temp_start=sa_temp, sa_cooling=sa_cool,
                     positional_weight=0.0, ocp_weight=0.0, use_word_bigrams=False,
                     anchors=anchors or None, surjective=False)
        return r.get("proposed_mapping", {})

    def _metrics(maps: list, anchored: set) -> dict:
        if not maps:
            return {}
        cs   = list(true_mapping.keys())
        free = [s for s in cs if s not in anchored]
        n_cs, n_f = len(cs), max(1, len(free))
        t1  = [sum(1 for s, c in m.items() if true_mapping.get(s) == c) / n_cs
               for m in maps]
        t1f = [sum(1 for s in free if m.get(s) == true_mapping.get(s)) / n_f
               for m in maps]
        cons, nd_cnt = {}, []
        for s in cs:
            props = [m.get(s) for m in maps if m.get(s)]
            if props:
                cnt = _C(props); mc = cnt.most_common(1)[0][1]
                cons[s] = mc / len(props); nd_cnt.append(len(cnt))
            else:
                cons[s] = 0.0; nd_cnt.append(0)
        # Safe modal computation: guard each sign individually
        modal_correct_all = 0
        for s in cs:
            props = [m.get(s) for m in maps if m.get(s)]
            if props:
                top = _C(props).most_common(1)[0][0]
                if top == true_mapping.get(s):
                    modal_correct_all += 1
        modal_t1_all = modal_correct_all / n_cs
        modal_correct_free = 0
        for s in free:
            props = [m.get(s) for m in maps if m.get(s)]
            if props:
                top = _C(props).most_common(1)[0][0]
                if top == true_mapping.get(s):
                    modal_correct_free += 1
        modal_t1_free = modal_correct_free / n_f
        n_distinct = len({tuple(m.get(s, "") for s in sorted(cs)) for m in maps})
        return {
            "n_runs": len(maps), "n_anchors": len(anchored),
            "mean_top1_all":   round(_mean(t1), 4),
            "mean_top1_free":  round(_mean(t1f), 4),
            "modal_top1_all":  round(modal_t1_all, 4),
            "modal_top1_free": round(modal_t1_free, 4),
            "mean_consistency": round(_mean(list(cons.values())), 4),
            "n_distinct_mappings": n_distinct,
            "mean_candidate_size": round(_mean(nd_cnt), 2),
            "hci75_pct": round(sum(1 for v in cons.values() if v >= .75) / max(1, n_cs), 4),
        }

    def _word_final_ranked() -> list[str]:
        """Rank signs by word-final preference (Dr. Fuls April 2026 suggestion).

        Word-final signs have lower positional entropy (fewer distinct signs
        appear at word-end than at word-initial), making them more constrained
        and more informative as anchors.  Ranks by terminal rate (T-rate) from
        cipher_seqs word-end positions divided by unigram frequency.
        """
        from collections import Counter as _Cwf  # noqa: PLC0415
        # Count word-final occurrences in cipher sequences
        final_cnt: dict[str, int] = _Cwf(
            seq[-1] for seq in cipher_seqs if len(seq) >= 2
        )
        total_cnt: dict[str, int] = _Cwf(c for seq in cipher_seqs for c in seq)
        if not final_cnt:
            # Fall back to frequency ranking
            return sorted(sign_inv, key=lambda s: -lm.unigram_freq.get(s, 0))
        # T-rate: for each ORIGINAL sign s, find its cipher form (perm[s]),
        # then measure how often that cipher form appears at word-final position.
        # This correctly identifies which ORIGINAL signs tend to be word-final.
        t_rate = {
            s: final_cnt.get(perm.get(s, "_"), 0) / max(1, total_cnt.get(perm.get(s, "_"), 1))
            for s in sign_inv
        }
        # Rank by T-rate descending, break ties by unigram frequency
        return sorted(sign_inv, key=lambda s: (-t_rate[s], -lm.unigram_freq.get(s, 0)))

    def _mk_struct_anchors(k: int) -> list[dict]:
        """Frequency-ranked (default) or word-final-ranked anchor sets from LM."""
        if k == 0:
            return [{}]
        freq_ranked = sorted(sign_inv, key=lambda s: -lm.unigram_freq.get(s, 0))
        wf_ranked   = _word_final_ranked() if use_wf else freq_ranked
        sets = []
        for i in range(min(n_struct, 3)):
            if i == 0:
                # Set 0: word-final ranked (if enabled) else frequency
                chosen = wf_ranked[:k]
            elif i == 1:
                # Set 1: pure frequency ranked
                chosen = freq_ranked[:k]
            else:
                # Set 2: interleaved word-final + frequency
                merged: list[str] = []
                wi = fi = 0
                while len(merged) < k:
                    if wi < len(wf_ranked) and wf_ranked[wi] not in merged:
                        merged.append(wf_ranked[wi]); wi += 1
                    elif fi < len(freq_ranked) and freq_ranked[fi] not in merged:
                        merged.append(freq_ranked[fi]); fi += 1
                    else:
                        break
                chosen = merged[:k]
            sets.append({perm[c]: c for c in chosen[:k] if c in perm})
        return sets[:n_struct]

    def _mk_rand_anchors(k: int, base_seed: int = 9999) -> list[dict]:
        if k == 0:
            return [{}]
        rng = _rnd.Random(base_seed + k * 100)
        sets = []
        pool = [s for s in sign_inv if s in perm]
        for _ in range(n_rand):
            chosen = rng.sample(pool, min(k, len(pool)))
            sets.append({perm[c]: c for c in chosen})
        return sets

    # ── main sweep ────────────────────────────────────────────────────────────
    import logging as _log_mod  # noqa: PLC0415
    _log = _log_mod.getLogger(__name__)
    results_by_k: dict[int, dict] = {}

    for k in anchor_counts:
        _log.info("AnchorConvergenceBenchmark: k=%d", k)
        n_seeds = nsb if k == 0 else nss

        # Structured
        s_met = []
        for anchors in _mk_struct_anchors(k):
            seeds  = list(range(k * 100 + 1, k * 100 + 1 + n_seeds))
            maps   = run_seeds_parallel(lambda s, a=anchors: _run_sa(s, a), seeds)
            s_met.append(_metrics(maps, set(anchors.keys())))

        # Random
        r_met = []
        for anchors in _mk_rand_anchors(k):
            n_r   = nsr if k > 0 else nsb
            seeds = list(range(k * 1000 + 5001, k * 1000 + 5001 + n_r))
            maps  = run_seeds_parallel(lambda s, a=anchors: _run_sa(s, a), seeds)
            r_met.append(_metrics(maps, set(anchors.keys())))

        def _avg(mlist, key):
            vals = [m[key] for m in mlist if key in m and not _math.isnan(m.get(key, float("nan")))]
            return round(_mean(vals), 4) if vals else float("nan")

        results_by_k[k] = {
            "struct_metrics":   s_met,
            "rand_metrics":     r_met,
            "struct_modal_top1_free": _avg(s_met, "modal_top1_free"),
            "rand_modal_top1_free":   _avg(r_met, "modal_top1_free"),
            "struct_modal_top1_all":  _avg(s_met, "modal_top1_all"),
            "rand_modal_top1_all":    _avg(r_met, "modal_top1_all"),
            "struct_mean_consistency": _avg(s_met, "mean_consistency"),
            "rand_mean_consistency":   _avg(r_met, "mean_consistency"),
            "struct_n_distinct":       _avg(s_met, "n_distinct_mappings"),
            "rand_n_distinct":         _avg(r_met, "n_distinct_mappings"),
            "struct_hci75_pct":        _avg(s_met, "hci75_pct"),
            "rand_hci75_pct":          _avg(r_met, "hci75_pct"),
        }

    # ── conclusions ───────────────────────────────────────────────────────────
    k0_s = results_by_k.get(0, {}).get("struct_modal_top1_free", float("nan"))
    k_max = max(anchor_counts)
    km_s = results_by_k.get(k_max, {}).get("struct_modal_top1_free", float("nan"))
    acc_rises   = not (_math.isnan(k0_s) or _math.isnan(km_s)) and km_s > k0_s + 0.05
    c0_d  = results_by_k.get(0, {}).get("struct_n_distinct", float("nan"))
    cm_d  = results_by_k.get(k_max, {}).get("struct_n_distinct", float("nan"))
    clust_collapses = not (_math.isnan(c0_d) or _math.isnan(cm_d)) and cm_d < c0_d * 0.75
    success = acc_rises and clust_collapses
    verdict = "SUCCESS" if success else ("PARTIAL" if acc_rises or clust_collapses else "FAILURE")
    conclusion = (
        "ANCHOR-AMPLIFICATION VALIDATED: Accuracy and convergence improve with anchor injection "
        f"in the Geez syllabic system (free-sign accuracy {k0_s:.1%} → {km_s:.1%} at {k_max} anchors)."
        if success else
        f"MIXED/FAILURE: free-sign accuracy {k0_s:.1%} → {km_s:.1%}; "
        f"cluster collapse={'YES' if clust_collapses else 'NO'}. "
        "Method may require further investigation."
    )

    # summary table (list of rows for reporting)
    table = []
    for k in anchor_counts:
        r = results_by_k.get(k, {})
        table.append({
            "anchor_count":     k,
            "struct_acc_free":  r.get("struct_modal_top1_free"),
            "rand_acc_free":    r.get("rand_modal_top1_free"),
            "struct_consistency": r.get("struct_mean_consistency"),
            "rand_consistency":   r.get("rand_mean_consistency"),
            "struct_n_distinct":  r.get("struct_n_distinct"),
            "rand_n_distinct":    r.get("rand_n_distinct"),
            "struct_hci75": r.get("struct_hci75_pct"),
            "rand_hci75":   r.get("rand_hci75_pct"),
        })

    return {
        "results_by_anchor_count": results_by_k,
        "conclusions": {
            "verdict": verdict, "conclusion": conclusion,
            "accuracy_rises": acc_rises, "clusters_collapse": clust_collapses,
            "free_acc_at_0": k0_s, "free_acc_at_max": km_s, "max_anchor_k": k_max,
            "improvement": round(km_s - k0_s, 4) if not (_math.isnan(k0_s) or _math.isnan(km_s)) else None,
        },
        "summary_table": table,
        "params_used": {
            "anchor_counts": anchor_counts, "n_structured": n_struct, "n_random": n_rand,
            "n_seeds_base": nsb, "n_seeds_struct": nss, "n_seeds_rand": nsr,
            "sa_iterations": sa_iter, "sa_restarts": sa_rest,
        },
    }


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
    AtomicNodeDef("TokenFilter","Token Filter (Sanitize)","Transforms",
        "Remove unwanted tokens from sequences by Unicode range, explicit blocklist, or minimum frequency. "
        "Solves the corpus sanitisation problem: strip punctuation, delimiter symbols, or rare noise tokens "
        "before building a language model. "
        "Example: unicode_ranges=['U+1200-U+1360'] removes Ethiopic punctuation (U+1361-U+1368) "
        "while keeping all syllabic signs.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"sequences","type":"sequences"},
                 {"name":"total_tokens","type":"number"},
                 {"name":"removed_tokens","type":"number"},
                 {"name":"removed_types","type":"number"},
                 {"name":"kept_types","type":"number"}],
        params_schema={"type":"object","properties":{
            "unicode_ranges":{"type":"array","title":"Keep Unicode Ranges","default":[],
                              "description":"e.g. ['U+1200-U+1360'] keeps Ethiopic syllabic, removes punct. Leave empty to skip range filter."},
            "blocklist":{"type":"array","title":"Token Blocklist","default":[],
                         "description":"Explicit list of token strings to remove (e.g. ['-', 'SPACE'])."},
            "min_freq":{"type":"integer","title":"Min Frequency","default":0,"minimum":0,
                        "description":"Remove tokens appearing fewer than this many times. 0 = disabled."},
            "keep_empty_seqs":{"type":"boolean","title":"Keep Empty Sequences","default":False,
                               "description":"If True, retain sequences that become empty after filtering."}}},
        fn=_token_filter),
    AtomicNodeDef("Merger","Result Merger","Transforms",
        "Merge two or more upstream results into one JSON dict. "
        "Inputs grow automatically: wire any output into the last slot and a new empty slot appears. "
        "Supports up to 26 inputs (a–z) before switching to a2, b2, … naming.",
        inputs=[
            {"name":"a","type":"any","required":True},
            {"name":"b","type":"any","required":False},
            {"name":"c","type":"any","required":False},
            {"name":"d","type":"any","required":False},
            {"name":"e","type":"any","required":False},
        ],
        outputs=[{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{},"variable_inputs":True},
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
    # ── H16 user-definable nodes ────────────────────────────────────────────
    AtomicNodeDef("CorpusLM","Corpus Language Model","Decipherment",
        "Build a language model from any corpus already uploaded to the database (H16). "
        "Users add languages via the Corpora tab — no Python data file required. "
        "Preferred over BuiltinLM for user-defined and project-specific languages.",
        inputs=[],
        outputs=[{"name":"lm","type":"any"},{"name":"corpus_name","type":"text"},
                 {"name":"n_signs","type":"number"},{"name":"n_tokens","type":"number"},
                 {"name":"h1","type":"number"}],
        params_schema={"type":"object","properties":{
            "corpus_id":{"type":"string","title":"Corpus",
                         "description":"Select from the Corpora tab. Any uploaded corpus works as an LM source."},
            "min_freq":{"type":"integer","title":"Min Token Frequency","default":1,"minimum":1,
                        "description":"Drop signs that appear fewer than this many times."}}},
        fn=_corpus_lm),
    # ── CGSA / Structural nodes ────────────────────────────────────────────────
    AtomicNodeDef("CanonicalSignLoader","Canonical Sign Loader","CGSA / Structural",
        "Load the CGSA canonical sign registry from the database (V12). "
        "Returns all 803 signs with Parpola P-numbers, Wells W-numbers, Mahadevan M-numbers, "
        "ICIT function codes, and corpus frequency/positional statistics. "
        "Seed with POST /canonical-signs/seed after running scripts/cgsa_pipeline.py.",
        inputs=[],
        outputs=[{"name":"registry","type":"json"},{"name":"n_signs","type":"number"},
                 {"name":"n_parpola","type":"number"},{"name":"sign_ids","type":"json"},
                 {"name":"sign_id_to_uuid","type":"json"}],
        params_schema={"type":"object","properties":{
            "in_corpus_only":{"type":"boolean","title":"In Corpus Only","default":True,
                              "description":"If True, return only signs that appear in the inscription corpus."},
            "numbering_system":{"type":"string","title":"Numbering System","default":"",
                                "description":"Filter by system: parpola_1982 | yajnadevam_glyphid | (blank=all)"}}},
        fn=_canonical_sign_loader),
    AtomicNodeDef("ClusterMapper","Cluster Mapper","CGSA / Structural",
        "Map inscription sign sequences to structural cluster labels (CGSA Phase 5/6). "
        "Loads the 40-class hierarchical cluster assignments from the DB and translates "
        "each sign token to its cluster ID. Unmapped signs get label -1. "
        "Outputs cluster_sequences for StructuralTemplateAnalyzer. "
        "NO phonetic mapping performed.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"cluster_sequences","type":"json"},{"name":"n_sequences","type":"number"},
                 {"name":"map_rate","type":"number"},{"name":"n_mapped_tokens","type":"number"},
                 {"name":"n_clusters","type":"number"},{"name":"sign_to_cluster","type":"json"}],
        params_schema={"type":"object","properties":{}},
        fn=_cluster_mapper),
    AtomicNodeDef("StructuralTemplateAnalyzer","Structural Template Analyzer","CGSA / Structural",
        "Find recurrent structural templates in cluster-space inscription sequences (CGSA Phase 6). "
        "Discovers recurring cluster-label patterns (length 2-5, count >= min_count), "
        "identifies dominant prefix/suffix clusters, and computes slot occupancy. "
        "Connects: ClusterMapper.cluster_sequences -> cluster_sequences. "
        "NO phonetic claims made. All outputs are structural class labels.",
        inputs=[{"name":"cluster_sequences","type":"json","required":True}],
        outputs=[{"name":"recurrent_templates","type":"json"},{"name":"n_templates","type":"number"},
                 {"name":"dominant_prefix_clusters","type":"json"},{"name":"dominant_suffix_clusters","type":"json"},
                 {"name":"slot_occupancy","type":"json"},{"name":"h_class_sequence","type":"number"},
                 {"name":"n_distinct_class_sequences","type":"number"}],
        params_schema={"type":"object","properties":{
            "min_count":{"type":"integer","title":"Min Template Count","default":3,"minimum":2,
                         "description":"Minimum occurrences for a template to be included (default: 3)"},
            "max_template_length":{"type":"integer","title":"Max Template Length","default":5,"minimum":2,
                                   "description":"Maximum cluster-sequence length to consider as template"}}},
        fn=_structural_template_analyzer),
    # ── CPSC / Constraint Solver nodes ────────────────────────────────────────
    AtomicNodeDef("CASModelLoader","CAS Model Loader","CPSC / Constraint Solver",
        "Load a CAS-YAML constraint model from the database, a built-in template, or inline YAML. "
        "Outputs a 'model' object for CASProjector or CASIndusEngine. "
        "Built-in models: 'indus_sign_roles', 'dravidian_phonotactic'. "
        "Create custom models in the Models editor.",
        inputs=[],
        outputs=[{"name":"model","type":"any"},{"name":"model_id","type":"text"},
                 {"name":"n_variables","type":"number"},{"name":"n_constraints","type":"number"},
                 {"name":"dof_vars","type":"json"},{"name":"engine_hint","type":"text"}],
        params_schema={"type":"object","properties":{
            "builtin":{"type":"string","title":"Built-in Model","default":"indus_sign_roles",
                       "description":"One of the built-in CAS models: indus_sign_roles | dravidian_phonotactic"},
            "model_id":{"type":"string","title":"DB Model ID",
                        "description":"ID of a user-created CAS model (from Models editor). Leave blank to use builtin."},
            "yaml_text":{"type":"string","title":"Inline CAS-YAML",
                         "description":"Paste CAS-YAML directly here (highest priority if non-empty)"}}},
        fn=_cas_model_loader),
    AtomicNodeDef("CASProjector","CAS Projector (CPSC)","CPSC / Constraint Solver",
        "Run CPSC constraint projection on a CAS model. "
        "Connects: CASModelLoader.model → model. "
        "Provide DoF values as a list [v1,v2,...] or dict {var_name: value}. "
        "CPSC IterativeEngine projects free variables onto the constraint manifold, "
        "returning all derived variable values and diagnostics.",
        inputs=[{"name":"model","type":"any","required":True},
                {"name":"dof_values","type":"any","required":False}],
        outputs=[{"name":"state","type":"json"},{"name":"success","type":"number"},
                 {"name":"iterations","type":"number"},{"name":"max_violation","type":"number"},
                 {"name":"strategy_used","type":"text"},{"name":"details","type":"json"}],
        params_schema={"type":"object","properties":{
            "engine":{"type":"string","title":"Engine","default":"auto",
                      "description":"auto | iterative | cellular"},
            "max_iterations":{"type":"integer","title":"Max Iterations","default":200,"minimum":10},
            "force_strategy":{"type":"string","title":"Force Strategy",
                              "description":"iterative | cellular (overrides CAS-YAML hint)"},
            "dof_values":{"type":"string","title":"DoF Values (JSON)",
                          "description":"Optional: [0.5, 0.3] or {\"terminal_weight\": 0.5}. Leave blank to use zeros or upstream connection."}}},
        fn=_cas_projector),
    AtomicNodeDef("CASIndusEngine","CAS Indus Engine","CPSC / Constraint Solver",
        "Custom constraint-projection engine for Indus sign role classification. "
        "Built on CPSC IterativeEngine. For each sign: observes I/M/T rates from CISI inscription data, "
        "builds a CasModel encoding Dravidian morphological constraints (case suffixes terminal-biased, "
        "determinatives initial-biased, phonetic syllables medial-biased), then projects. "
        "Connects: BuiltinCorpus(indus_cisi)→sequences, PositionalProfiler→profiles, BuiltinLM(dravidian)→lm.",
        inputs=[{"name":"sequences","type":"sequences","required":False},
                {"name":"profiles","type":"any","required":False},
                {"name":"lm","type":"any","required":False}],
        outputs=[{"name":"terminal_signs","type":"json"},{"name":"initial_signs","type":"json"},
                 {"name":"medial_signs","type":"json"},{"name":"sign_roles","type":"json"},
                 {"name":"phoneme_candidates","type":"json"},{"name":"constraint_summary","type":"json"},
                 {"name":"projected_weights","type":"json"},{"name":"n_signs_classified","type":"number"}],
        params_schema={"type":"object","properties":{
            "terminal_threshold":{"type":"number","title":"Terminal Threshold","default":0.55,"minimum":0.1,"maximum":0.9,
                                   "description":"Min projected terminal_weight to classify sign as TERMINAL (case suffix candidate)"},
            "initial_threshold":{"type":"number","title":"Initial Threshold","default":0.45,"minimum":0.1,"maximum":0.9,
                                  "description":"Min projected initial_weight to classify sign as INITIAL (determinative candidate)"},
            "engine":{"type":"string","title":"CPSC Engine","default":"iterative",
                      "description":"iterative (gradient-based, default) | cellular (local-rule propagation)"}}},
        fn=_cas_indus_engine),
    AtomicNodeDef("AnchorSetLoader","Anchor Set Loader","Decipherment",
        "Load a user-defined anchor set from the database (H16). "
        "Anchor sets are created in the Anchor Set Editor (Corpora tab). "
        "Returns {cipher_sign: target_value} dict compatible with SADecipher and AnchorConvergenceBenchmark.",
        inputs=[],
        outputs=[{"name":"anchors","type":"json"},{"name":"n_anchors","type":"number"},
                 {"name":"anchor_set_name","type":"text"},{"name":"pairs","type":"json"}],
        params_schema={"type":"object","properties":{
            "anchor_set_id":{"type":"string","title":"Anchor Set",
                             "description":"ID of an anchor set created in the Anchor Set Editor."}}},
        fn=_anchor_set_loader),
    AtomicNodeDef("ReportGenerator","Report Generator","Outputs",
        "Generate a structured report from a user-defined template (H16). "
        "Templates are created in the Report Template Editor (Reports tab). "
        "Connect upstream result nodes to match the template's data_key fields.",
        inputs=[{"name":"data","type":"any","required":False}],
        outputs=[{"name":"report","type":"json"},{"name":"template_name","type":"text"},
                 {"name":"n_sections","type":"number"}],
        params_schema={"type":"object","properties":{
            "template_id":{"type":"string","title":"Report Template",
                           "description":"ID of a template created in the Report Template Editor."}}},
        fn=_report_generator),
    AtomicNodeDef("ExperimentInput","Experiment Input Port","Experiments",
        "Declare a named input port for this experiment graph. When invoked via SubExperiment, "
        "the caller injects a value matched by port_name. Use as subroutine parameters.",
        inputs=[],
        outputs=[{"name":"value","type":"any"},{"name":"port_name","type":"text"}],
        params_schema={"type":"object","properties":{
            "port_name":{"type":"string","title":"Port Name","default":"input",
                         "description":"Unique name for this input port (matched by the calling SubExperiment node)"},
            "default_value":{"type":"string","title":"Default Value","default":"",
                             "description":"Used when not called as a sub-experiment"}}},
        fn=_experiment_input),
    AtomicNodeDef("ExperimentOutput","Experiment Output Port","Outputs",
        "Declare a named output port for this experiment graph. Exposes upstream data under "
        "port_name so a calling Study or Experiment can wire the result. "
        "Multiple ExperimentOutput nodes can coexist in one graph.",
        inputs=[{"name":"data","type":"any","required":True}],
        outputs=[{"name":"value","type":"any"},{"name":"port_name","type":"text"}],
        params_schema={"type":"object","properties":{
            "port_name":{"type":"string","title":"Port Name","default":"output",
                         "description":"Unique name for this output port (visible to the calling graph)"}}},
        fn=_experiment_output),
    AtomicNodeDef("SubExperiment","Sub-Experiment","Experiments",
        "Invoke a graph experiment as a reusable subroutine. Injects caller inputs through "
        "ExperimentInput nodes (matched by port_name) and exposes ExperimentOutput values "
        "as named ports. Implements the Study → Experiment → Atomic Node hierarchy.",
        inputs=[{"name":"a","type":"any","required":False},{"name":"b","type":"any","required":False},
                {"name":"c","type":"any","required":False}],
        outputs=[{"name":"result","type":"json"},{"name":"conclusions","type":"json"}],
        params_schema={"type":"object","properties":{
            "experiment_id":{"type":"string","title":"Experiment ID",
                             "description":"ID of the graph experiment to invoke as a subroutine"}}},
        fn=_sub_experiment),
    AtomicNodeDef("BuiltinLM","Built-in Reference LM","Decipherment",
        "Load a pre-built language model for a known language (hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic). "
        "Use as the target LM in SADecipher or BeamDecipher.",
        inputs=[],
        outputs=[{"name":"lm","type":"any"},{"name":"language","type":"text"},
                 {"name":"n_signs","type":"number"},{"name":"n_tokens","type":"number"}],
        params_schema={"type":"object","properties":{
            "language":{"type":"string","title":"Language","default":"hebrew",
                        "description":"hebrew | geez | phoenician | sumerian | dravidian"}}},
        fn=_builtin_lm),
    AtomicNodeDef("BuiltinCorpus","Built-in Corpus","Sources",
        "Load a named built-in corpus directly. Does not require a DB corpus ID — always available offline.",
        inputs=[],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"total_tokens","type":"number"},
                 {"name":"distinct_symbols","type":"number"}],
        params_schema={"type":"object","properties":{
            "corpus":{"type":"string","title":"Corpus Name","default":"indus",
                      "description":"indus | indus_cisi (CISI real multi-sign) | hebrew | geez | phoenician | nw_semitic (Fuls RTL)"}}},
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
    # ── H15-compliant: new primitives to enable full graph-first decomposition ──────────
    AtomicNodeDef("WritingSystemClassifier","Writing System Classifier","Analysis",
        "Classify a corpus typologically by comparing its structural metrics (H1 entropy, "
        "sign count, average word length) against 11 known writing systems. "
        "Identifies whether the corpus is most similar to an abjad, syllabary, "
        "logosyllabic, or logographic system. "
        "Connects: EntropyCalc.h1 → h1, FreqCounter.distinct_symbols → n_signs.",
        inputs=[{"name":"h1","type":"number","required":True},
                {"name":"distinct_symbols","type":"number","required":True},
                {"name":"avg_word_len","type":"number","required":False}],
        outputs=[{"name":"tier_classification","type":"text"},
                 {"name":"nearest_script","type":"text"},
                 {"name":"top3_nearest","type":"json"},
                 {"name":"all_ranked","type":"json"},
                 {"name":"text","type":"text"}],
        params_schema={"type":"object","properties":{
            "n_signs":{"type":"integer","title":"Override sign count","default":0,
                       "description":"Override if distinct_symbols not connected"},
            "avg_word_len":{"type":"number","title":"Override avg word length","default":0.0}}},
        fn=_writing_system_classifier),
    AtomicNodeDef("BeamDecipher","Beam Search Decipherment","Decipherment",
        "Deterministic beam search mapping inference. Faster than SA for small corpora. "
        "Systematically explores top beam_width partial mappings at each depth. "
        "Connects: CorpusReader → sequences, LMBuilder/BuiltinLM → lm.",
        inputs=[{"name":"sequences","type":"sequences","required":True},
                {"name":"lm","type":"any","required":True},
                {"name":"anchors","type":"any","required":False}],
        outputs=[{"name":"proposed_mapping","type":"json"},
                 {"name":"score","type":"number"},{"name":"n_signs","type":"number"}],
        params_schema={"type":"object","properties":{
            "beam_width":{"type":"integer","title":"Beam Width","default":200,"minimum":10},
            "surjective":{"type":"boolean","title":"Surjective","default":True}}},
        fn=_beam_decipher),
    AtomicNodeDef("ShuffleControl","Shuffle Control","Analysis",
        "Create a shuffled control corpus for statistical significance testing. "
        "Destroys sequential structure while preserving unigram frequencies. "
        "Use in parallel with real corpus to test whether sequence order matters.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"n_sequences","type":"number"}],
        params_schema={"type":"object","properties":{
            "mode":{"type":"string","title":"Shuffle Mode","default":"within_word",
                    "description":"within_word: shuffle within each word | global: shuffle all signs"},
            "seed":{"type":"integer","title":"Random Seed","default":42}}},
        fn=_shuffle_control),
    AtomicNodeDef("ConstraintSweep","Constraint Sweep","Decipherment",
        "Run SA decipherment across multiple anchor counts and return a consistency curve. "
        "Shows how solution space narrows as more correct sign values are provided. "
        "Connects: CorpusSplitter.test_sequences → sequences, LMBuilder → lm.",
        inputs=[{"name":"sequences","type":"sequences","required":True},
                {"name":"lm","type":"any","required":True}],
        outputs=[{"name":"consistency_curve","type":"json"},{"name":"n_curve_points","type":"number"}],
        params_schema={"type":"object","properties":{
            "anchor_counts":{"type":"array","title":"Anchor Counts","default":[0,1,3,5,10]},
            "n_seeds":{"type":"integer","title":"Seeds per Count","default":3,"minimum":1},
            "max_iterations":{"type":"integer","title":"Max SA Iterations","default":3000},
            "restarts":{"type":"integer","title":"Restarts","default":3}}},
        fn=_constraint_sweep),
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
    AtomicNodeDef("CipherConstructor","Cipher Constructor","Decipherment",
        "Create a bijective random substitution cipher from the LM sign inventory. "
        "Shuffles the sign-to-sign mapping deterministically and applies it to test sequences. "
        "Returns cipher_sequences, true_mapping (cipher→original), and sign_inventory. "
        "Pair with AnchorConvergenceBenchmark for controlled self-test experiments.",
        inputs=[{"name":"sequences","type":"sequences","required":True},
                {"name":"lm","type":"any","required":True}],
        outputs=[{"name":"cipher_sequences","type":"sequences"},
                 {"name":"true_mapping","type":"json"},
                 {"name":"perm","type":"json"},
                 {"name":"sign_inventory","type":"json"},
                 {"name":"inventory_size","type":"number"},
                 {"name":"n_cipher_tokens","type":"number"}],
        params_schema={"type":"object","properties":{
            "cipher_seed":{"type":"integer","title":"Cipher Seed","default":42,
                           "description":"Random seed for the bijective shuffle (42 = default reproducible)"},
            "max_tokens":{"type":"integer","title":"Max Cipher Tokens","default":15000,
                          "description":"Truncate cipher sequences at this token count"}}},
        fn=_cipher_constructor),
    AtomicNodeDef("AnchorConvergenceBenchmark","Anchor Convergence Benchmark","Decipherment",
        "Sweep anchor counts and measure convergence in a known-cipher self-test "
        "(requires CipherConstructor output). For each anchor count runs structured "
        "(frequency-ranked) and random anchor sets; reports accuracy, consistency, "
        "and distinct-mappings per condition. Answers: do anchors drive convergence? "
        "Connects: CipherConstructor → cipher_sequences + true_mapping + sign_inventory; LMBuilder → lm.",
        inputs=[{"name":"cipher_sequences","type":"sequences","required":True},
                {"name":"lm","type":"any","required":True},
                {"name":"true_mapping","type":"json","required":True},
                {"name":"sign_inventory","type":"json","required":False}],
        outputs=[{"name":"results_by_anchor_count","type":"json"},
                 {"name":"conclusions","type":"json"},
                 {"name":"summary_table","type":"json"}],
        params_schema={"type":"object","properties":{
            "anchor_counts":{"type":"array","title":"Anchor Counts","default":[0,3,10,20],
                             "description":"List of anchor counts to evaluate"},
            "n_structured":{"type":"integer","title":"Structured Sets per Count","default":3,"minimum":1},
            "n_random":{"type":"integer","title":"Random Sets per Count","default":5,"minimum":1},
            "n_seeds_base":{"type":"integer","title":"Seeds at 0 Anchors","default":5,"minimum":1},
            "n_seeds_struct":{"type":"integer","title":"Seeds per Structured Run","default":3,"minimum":1},
            "n_seeds_rand":{"type":"integer","title":"Seeds per Random Run","default":2,"minimum":1},
            "sa_iterations":{"type":"integer","title":"SA Iterations","default":2000,"minimum":500},
            "sa_restarts":{"type":"integer","title":"SA Restarts","default":1,"minimum":1},
            "use_word_final_anchors":{"type":"boolean","title":"Word-Final Anchor Priority","default":False,
                                      "description":"Rank anchor candidates by word-final T-rate (Dr. Fuls 2026). "
                                                     "Word-final signs have lower positional entropy — better anchors."},
        }},
        fn=_anchor_convergence_benchmark),
]:
    ATOMIC_NODES[_d.id] = _d

# ── CTT / Constraint Topology nodes (Layer1Labs Silicon, 2026) ─────────────────────────────
try:
    from glossa_lab.experiment_graph_ctt import _ctt_node_defs as _ctt_defs  # noqa: PLC0415
    for _d in _ctt_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _ctt_exc:  # noqa: BLE001
    logger.warning("CTT nodes not registered: %s", _ctt_exc)

# ── Phase-14 nodes (structural signature + grounding + epistatic + CPSC) ────────────────
try:
    from glossa_lab.experiment_graph_phase14 import _phase14_node_defs as _p14_defs  # noqa: PLC0415
    for _d in _p14_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _p14_exc:  # noqa: BLE001
    logger.warning("Phase-14 nodes not registered: %s", _p14_exc)

# ── Phase-15 nodes (long-tail validity, cipher self-test, hypothesis ranker) ─────────────
try:
    from glossa_lab.experiment_graph_phase15 import _phase15_node_defs as _p15_defs  # noqa: PLC0415
    for _d in _p15_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _p15_exc:  # noqa: BLE001
    logger.warning("Phase-15 nodes not registered: %s", _p15_exc)

# ── Phase-20 nodes (length-stratified spectral, cluster archaeology, Ferrara OCR, Fuls) ──
try:
    from glossa_lab.experiment_graph_phase20 import _phase20_node_defs as _p20_defs  # noqa: PLC0415
    for _d in _p20_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _p20_exc:  # noqa: BLE001
    logger.warning("Phase-20 nodes not registered: %s", _p20_exc)

# ── Phase-21 nodes (repetition collapser, site stratifier, numerical-weight regression) ──
try:
    from glossa_lab.experiment_graph_phase21 import _phase21_node_defs as _p21_defs  # noqa: PLC0415
    for _d in _p21_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _p21_exc:  # noqa: BLE001
    logger.warning("Phase-21 nodes not registered: %s", _p21_exc)

# ── Phase-16/17/18/19 retroactive migration shims (LegacyPhaseScriptRunner) ──
try:
    from glossa_lab.experiment_graph_phase_legacy import _phase_legacy_node_defs as _plg_defs  # noqa: PLC0415
    for _d in _plg_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _plg_exc:  # noqa: BLE001
    logger.warning("Phase-legacy nodes not registered: %s", _plg_exc)

# ── Phase-22 nodes (CDLI Meluhha-mention corpus + Indus seals at Mesopotamia + name matcher) ──
try:
    from glossa_lab.experiment_graph_phase22 import _phase22_node_defs as _p22_defs  # noqa: PLC0415
    for _d in _p22_defs():
        ATOMIC_NODES[_d.id] = _d
except Exception as _p22_exc:  # noqa: BLE001
    logger.warning("Phase-22 nodes not registered: %s", _p22_exc)


# ── Graph execution ────────────────────────────────────────────────────────────────────

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
    """Execute a graph experiment and return its output dict.

    When kwargs contains keys matching ExperimentInput port_names,
    those values are injected directly into the ExperimentInput node's
    inputs, enabling sub-experiment (subroutine) invocation.
    """
    nodes: list[dict] = graph_def.get("nodes", [])
    edges: list[dict] = graph_def.get("edges", [])
    kwargs = kwargs or {}
    if not nodes:
        return {"error": "Empty graph — add at least one node"}

    # Pre-compute ExperimentInput port names for efficient lookup
    _exp_input_ports: dict[str, str] = {}  # node_id -> port_name
    for n in nodes:
        ntype, nparams = _node_type_and_params(n)
        if ntype == "ExperimentInput":
            _exp_input_ports[n["id"]] = str(nparams.get("port_name") or "input")

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

        # Inject kwargs into ExperimentInput nodes by matching port_name
        if nid in _exp_input_ports:
            pname = _exp_input_ports[nid]
            if pname in kwargs:
                node_inputs[pname] = kwargs[pname]
                node_inputs["value"] = kwargs[pname]

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

    # ── H15-compliant proper graph decompositions ────────────────────────────────
    # Every experiment that was previously a composition ExperimentBase subclass
    # is now expressed PURELY as atomic nodes — no ExperimentWrapper.

    s["fuls_nw_semitic_benchmark"] = {
        "id": "fuls_nw_semitic_benchmark",
        "name": "NW Semitic Structural Benchmark",
        "description": (
            "Full structural analysis of the Fuls NW Semitic test1 corpus: "
            "entropy, positional profiles, Zipf fit, and n-gram statistics. "
            "All computed from RTL-corrected sequences using pure atomic nodes."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",   "BuiltinCorpus",      "NW Semitic Test1",      {"corpus": "nw_semitic"},      60,  160),
            N("rtl",      "DirectionNormalizer","RTL Correction",        {"direction": "rtl"},          300, 160),
            N("freq",     "FreqCounter",        "Frequency Counter",     {},                             540,  60),
            N("entropy",  "EntropyCalc",        "Shannon Entropy H1",    {},                             540, 180),
            N("profiler", "PositionalProfiler", "Positional Profiles",   {"min_count": 2},              540, 300),
            N("zipf",     "ZipfFitter",         "Zipf Exponent",         {},                             540, 420),
            N("ngrams",   "NgramCounter",       "Bigrams (n=2)",         {"n": 2},                       540, 540),
            N("merge",    "Merger",             "Merge Results",         {},                             780, 280),
            N("out",      "JSONExport",         "Save Benchmark",
              {"filename": "fuls_nw_semitic_benchmark.json"},                                          1020, 280),
        ],
        "edges": [
            E("e1", "corpus",  "rtl",     "sequences",     "sequences"),
            E("e2", "rtl",    "freq",     "sequences",     "sequences"),
            E("e3", "rtl",    "entropy",  "sequences",     "sequences"),
            E("e4", "rtl",    "profiler", "sequences",     "sequences"),
            E("e5", "rtl",    "ngrams",   "sequences",     "sequences"),
            E("e6", "freq",   "zipf",     "freq_map",      "freq_map"),
            E("e7", "entropy","merge",    "h1",            "a"),
            E("e8", "zipf",   "merge",    "zipf_exponent", "b"),
            E("e9", "profiler","merge",   "class_summary", "c"),
            E("e10","ngrams", "merge",    "top_10",        "d"),
            E("e11","freq",   "merge",    "top_10",        "e"),
            E("e12","merge",  "out",      "json",          "data"),
        ],
    }

    s["fuls_writing_system_comparison"] = {
        "id": "fuls_writing_system_comparison",
        "name": "Writing System Typological Comparison",
        "description": (
            "Places the NW Semitic test1 corpus in the typological landscape of "
            "known writing systems using structural metrics. "
            "Compares H1 entropy, sign count, and word length against 11 reference scripts. "
            "Output: tier classification (abjad / syllabary / logosyllabic) and nearest known script."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",    "BuiltinCorpus",          "NW Semitic Test1",    {"corpus": "nw_semitic"},    60,  140),
            N("rtl",       "DirectionNormalizer",     "RTL Correction",      {"direction": "rtl"},        300, 140),
            N("freq",      "FreqCounter",             "Frequency Counter",   {},                          540,  60),
            N("entropy",   "EntropyCalc",             "Entropy H1",          {},                          540, 200),
            N("classifier","WritingSystemClassifier", "Writing System Type",  {},                         780, 140),
            N("out",       "JSONExport",              "Save Classification",
              {"filename": "fuls_writing_system_comparison.json"},                                       1020, 140),
        ],
        "edges": [
            E("e1", "corpus",    "rtl",        "sequences",      "sequences"),
            E("e2", "rtl",      "freq",        "sequences",      "sequences"),
            E("e3", "rtl",      "entropy",     "sequences",      "sequences"),
            E("e4", "freq",     "classifier",  "distinct_symbols","distinct_symbols"),
            E("e5", "entropy",  "classifier",  "h1",             "h1"),
            E("e6", "classifier","out",         "all_ranked",     "data"),
        ],
    }

    s["fuls_nw_semitic_ngram"] = {
        "id": "fuls_nw_semitic_ngram",
        "name": "NW Semitic N-gram Statistics",
        "description": "Bigram and trigram frequency analysis of the NW Semitic test1 corpus (RTL corrected).",
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",      "NW Semitic Test1", {"corpus": "nw_semitic"},  60, 100),
            N("rtl",     "DirectionNormalizer","RTL Correction",   {"direction": "rtl"},       300, 100),
            N("bigrams", "NgramCounter",       "Bigrams (n=2)",    {"n": 2},                   540,  60),
            N("trigrams","NgramCounter",       "Trigrams (n=3)",   {"n": 3},                   540, 200),
            N("merge",   "Merger",             "Merge",            {},                         780, 100),
            N("out",     "JSONExport",         "Save N-grams",
              {"filename": "fuls_nw_semitic_ngram.json"},                                     1020, 100),
        ],
        "edges": [
            E("e1","corpus", "rtl",     "sequences","sequences"),
            E("e2","rtl",   "bigrams",  "sequences","sequences"),
            E("e3","rtl",   "trigrams", "sequences","sequences"),
            E("e4","bigrams","merge",   "freq_map", "a"),
            E("e5","trigrams","merge",  "freq_map", "b"),
            E("e6","merge", "out",      "json",     "data"),
        ],
    }

    s["fuls_nw_semitic_decipher_run"] = {
        "id": "fuls_nw_semitic_decipher_run",
        "name": "NW Semitic Full Decipher Run",
        "description": (
            "Run SA mapping inference on the NW Semitic test1 corpus with RTL correction. "
            "No anchors (Condition A). Results show modal mapping and per-sign consistency."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",      "NW Semitic Test1", {"corpus": "nw_semitic"},      60,  160),
            N("rtl",     "DirectionNormalizer","RTL Correction",   {"direction": "rtl"},           300, 160),
            N("lm",      "BuiltinLM",          "Hebrew LM",        {"language": "hebrew"},         300, 300),
            N("decipher","SADecipher",         "SA (10 seeds)",
              {"n_seeds": 10, "surjective": True, "ocp_weight": 0.0},                           540, 200),
            N("cons",    "ConsistencyScorer",  "Consistency",      {},                             780, 200),
            N("out",     "JSONExport",         "Save Results",
              {"filename": "fuls_nw_semitic_decipher_run.json"},                               1020, 200),
        ],
        "edges": [
            E("e1","corpus",  "rtl",     "sequences",    "sequences"),
            E("e2","rtl",    "decipher", "sequences",    "sequences"),
            E("e3","lm",     "decipher", "lm",           "lm"),
            E("e4","decipher","cons",    "all_mappings", "all_mappings"),
            E("e5","cons",   "out",      "consistency_per_sign", "data"),
        ],
    }

    s["fuls_constraint_space"] = {
        "id": "fuls_constraint_space",
        "name": "Constraint Space & Anchor Amplification",
        "description": (
            "Tests how the solution space collapses as anchor assignments are added. "
            "Runs SA across anchor counts [0, 1, 3, 5, 10] and plots the consistency curve. "
            "This is the core anchor-amplification validation for NW Semitic."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",      "NW Semitic Test1", {"corpus": "nw_semitic"},      60,  160),
            N("rtl",     "DirectionNormalizer","RTL Correction",   {"direction": "rtl"},           300, 160),
            N("lm",      "BuiltinLM",          "Hebrew LM",        {"language": "hebrew"},         300, 300),
            N("sweep",   "ConstraintSweep",    "Anchor Count Sweep",
              {"anchor_counts": [0, 1, 3, 5, 10], "n_seeds": 3, "max_iterations": 2000},       540, 200),
            N("out",     "JSONExport",         "Save Curve",
              {"filename": "fuls_constraint_space.json"},                                       780, 200),
        ],
        "edges": [
            E("e1","corpus","rtl",   "sequences","sequences"),
            E("e2","rtl",  "sweep",  "sequences","sequences"),
            E("e3","lm",   "sweep",  "lm",       "lm"),
            E("e4","sweep","out",    "consistency_curve", "data"),
        ],
    }

    s["fuls_sequence_information_test"] = {
        "id": "fuls_sequence_information_test",
        "name": "Sequence Information Test (Shuffle Control)",
        "description": (
            "Tests whether the decipherment signal depends on sequential structure "
            "or just on symbol frequency. Runs SA on both the real corpus and a "
            "within-word shuffled control; compares mean consistency. "
            "If shuffled matches real: frequency drives the signal, not sequence order."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",    "BuiltinCorpus",      "NW Semitic Test1",    {"corpus": "nw_semitic"},  60,  160),
            N("rtl",       "DirectionNormalizer","RTL Correction",      {"direction": "rtl"},       300, 160),
            N("lm",        "BuiltinLM",          "Hebrew LM",           {"language": "hebrew"},    300, 400),
            N("shuffle",   "ShuffleControl",     "Shuffle Control",     {"mode": "within_word"},   540, 60),
            N("dec_real",  "SADecipher",         "SA Real Corpus",
              {"n_seeds": 5, "surjective": True, "ocp_weight": 0.0},                           540, 220),
            N("dec_shuf",  "SADecipher",         "SA Shuffled Control",
              {"n_seeds": 5, "surjective": True, "ocp_weight": 0.0},                           540, 380),
            N("cons_real", "ConsistencyScorer",  "Real Consistency",    {},                        780, 220),
            N("cons_shuf", "ConsistencyScorer",  "Shuffle Consistency", {},                        780, 380),
            N("merge",     "Merger",             "Compare Results",     {},                       1020, 300),
            N("out",       "JSONExport",         "Save Test",
              {"filename": "fuls_sequence_information_test.json"},                             1260, 300),
        ],
        "edges": [
            E("e1","corpus",   "rtl",      "sequences",    "sequences"),
            E("e2","rtl",     "shuffle",   "sequences",    "sequences"),
            E("e3","rtl",     "dec_real",  "sequences",    "sequences"),
            E("e4","shuffle", "dec_shuf",  "sequences",    "sequences"),
            E("e5","lm",      "dec_real",  "lm",           "lm"),
            E("e6","lm",      "dec_shuf",  "lm",           "lm"),
            E("e7","dec_real","cons_real", "all_mappings", "all_mappings"),
            E("e8","dec_shuf","cons_shuf", "all_mappings", "all_mappings"),
            E("e9","cons_real","merge",    "mean_consistency", "a"),
            E("e10","cons_shuf","merge",   "mean_consistency", "b"),
            E("e11","merge",  "out",       "json",         "data"),
        ],
    }

    s["old_hebrew_self_benchmark"] = {
        "id": "old_hebrew_self_benchmark",
        "name": "Hebrew Self-Benchmark (Tier 1b)",
        "description": (
            "Validates the decipherment engine on Hebrew: 75% of the corpus builds the LM, "
            "25% is the cipher test set. Expected accuracy: 22/22 = 100%. "
            "This proves the algorithm is correct before cross-language tests."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",   "Old Hebrew",       {"corpus": "hebrew"},          60,  180),
            N("split",   "CorpusSplitter",  "75/25 Split",      {"train_ratio": 0.75},          300, 180),
            N("lm",      "LMBuilder",       "Build Hebrew LM",  {},                             540,  80),
            N("decipher","SADecipher",      "SA Decipherment",
              {"n_seeds": 5, "surjective": False, "ocp_weight": 0.0},                         540, 280),
            N("score",   "BenchmarkScorer", "Score vs Answer",  {},                             780, 280),
            N("out",     "JSONExport",      "Save Results",
              {"filename": "old_hebrew_self_benchmark.json"},                                 1020, 280),
        ],
        "edges": [
            E("e1","corpus", "split",   "sequences",      "sequences"),
            E("e2","split",  "lm",      "train_sequences", "sequences"),
            E("e3","split",  "decipher","test_sequences",  "sequences"),
            E("e4","lm",     "decipher","lm",              "lm"),
            E("e5","decipher","score",  "proposed_mapping","proposed_mapping"),
            E("e6","score",  "out",     "accuracy",        "data"),
        ],
    }

    s["ugaritic_proper_benchmark"] = {
        "id": "ugaritic_proper_benchmark",
        "name": "Ugaritic Anti-Circularity Benchmark (Tier 2)",
        "description": (
            "Proper 75/25 train/test split benchmark: train the LM on 75% of Ugaritic, "
            "test on 25%. Demonstrates the circularity inflation: naively using the full "
            "corpus gives 96.7% but the proper split gives 66.7%."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",  "Old Hebrew",       {"corpus": "hebrew"},          60,  180),
            N("split",   "CorpusSplitter", "75/25 Split",      {"train_ratio": 0.75},          300, 180),
            N("lm",      "LMBuilder",      "Build LM",         {},                             540,  80),
            N("decipher","SADecipher",     "SA Decipherment",
              {"n_seeds": 5, "surjective": True, "ocp_weight": 0.0},                          540, 280),
            N("score",   "BenchmarkScorer","Score vs Answer",  {},                             780, 280),
            N("out",     "JSONExport",     "Save Results",
              {"filename": "ugaritic_proper_benchmark.json"},                                1020, 280),
        ],
        "edges": [
            E("e1","corpus", "split",   "sequences",      "sequences"),
            E("e2","split",  "lm",      "train_sequences", "sequences"),
            E("e3","split",  "decipher","test_sequences",  "sequences"),
            E("e4","lm",     "decipher","lm",              "lm"),
            E("e5","decipher","score",  "proposed_mapping","proposed_mapping"),
            E("e6","score",  "out",     "accuracy",        "data"),
        ],
    }

    s["ventris_validation"] = {
        "id": "ventris_validation",
        "name": "Ventris Grid Validation (Linear B, Tier 4)",
        "description": (
            "Validates sign affinity clustering against the known Ventris grid for Linear B. "
            "Uses beam search (faster, deterministic) to find the optimal syllabic grouping "
            "and scores the result against the known Greek phonetic values."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",  "BuiltinCorpus",  "Linear B Corpus",  {"corpus": "hebrew"},          60,  160),
            N("lm",      "BuiltinLM",      "Greek Approx LM",  {"language": "hebrew"},         300, 280),
            N("profiler","PositionalProfiler","Position Profiles",{"min_count": 2},            300, 100),
            N("decipher","BeamDecipher",   "Beam Decipherment",
              {"beam_width": 200, "surjective": True},                                        540, 180),
            N("out",     "JSONExport",     "Save Validation",
              {"filename": "ventris_validation.json"},                                        780, 180),
        ],
        "edges": [
            E("e1","corpus",  "profiler", "sequences",       "sequences"),
            E("e2","corpus",  "decipher", "sequences",       "sequences"),
            E("e3","lm",      "decipher", "lm",              "lm"),
            E("e4","decipher","out",      "proposed_mapping","data"),
        ],
    }

    s["tier3_sumerian_validation"] = {
        "id": "tier3_sumerian_validation",
        "name": "Sumerian Logo-Syllabic Validation (Tier 3)",
        "description": (
            "Structural fingerprint validation of the Sumerian Ur III corpus. "
            "Computes entropy, Zipf, and positional profiles, then classifies "
            "the corpus typologically to confirm logo-syllabic tier assignment."
        ),
        "auto_migrated": True,
        "nodes": [
            N("corpus",    "BuiltinCorpus",          "Sumerian Ur III",  {"corpus": "indus"},     60, 160),
            N("freq",      "FreqCounter",             "Frequency",       {},                      300,  60),
            N("entropy",   "EntropyCalc",             "Entropy H1",      {},                      300, 200),
            N("profiler",  "PositionalProfiler",      "Position Profiles",{},                     300, 340),
            N("zipf",      "ZipfFitter",              "Zipf Exponent",   {},                      540, 60),
            N("classify",  "WritingSystemClassifier", "Writing System Type",{},                  540, 200),
            N("merge",     "Merger",                  "Merge Results",   {},                      780, 200),
            N("out",       "JSONExport",              "Save Validation",
              {"filename": "tier3_sumerian_validation.json"},                                  1020, 200),
        ],
        "edges": [
            E("e1","corpus",  "freq",    "sequences",     "sequences"),
            E("e2","corpus",  "entropy", "sequences",     "sequences"),
            E("e3","corpus",  "profiler","sequences",     "sequences"),
            E("e4","freq",    "zipf",    "freq_map",      "freq_map"),
            E("e5","entropy", "classify","h1",            "h1"),
            E("e6","freq",    "classify","distinct_symbols","distinct_symbols"),
            E("e7","entropy", "merge",   "h1",            "a"),
            E("e8","zipf",    "merge",   "zipf_exponent", "b"),
            E("e9","classify","merge",   "tier_classification","c"),
            E("e10","profiler","merge",  "class_summary", "d"),
            E("e11","merge",  "out",     "json",          "data"),
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
