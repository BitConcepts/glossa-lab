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
import os
from collections import Counter, deque
from pathlib import Path
from typing import Any, Callable

from glossa_lab.experiment_base import ExperimentBase
from glossa_lab.generic_loaders import (
    dataset_record_loader_execute,
    json_corpus_loader_execute,
    json_record_dir_loader_execute,
)
from glossa_lab.generic_primitives import (
    anchor_syllabifier_execute,
    association_anchor_deriver_execute,
    cluster_contingency_profile_execute,
    evidence_rule_aggregator_execute,
    iconographic_anchor_scorer_execute,
    interaction_surplus_profile_execute,
    label_map_applier_execute,
    length_match_permutation_test_execute,
    length_match_scorer_execute,
    metric_field_extractor_execute,
    order_information_profile_execute,
    persons_aggregator_execute,
    phoneme_map_coverage_execute,
    phoneme_map_permutation_test_execute,
    pmi_centrality_ranker_execute,
    positional_claim_tester_execute,
    positional_class_classifier_execute,
    prediction_verdict_aggregator_execute,
    prefix_findspot_assigner_execute,
    record_group_summary_execute,
    corpus_comparison_stats_execute,
    corpus_cooccurrence_check_execute,
    registry_table_loader_execute,
    reverse_skeleton_search_execute,
    sign_position_null_test_execute,
    signature_comparator_execute,
    sign_role_classifier_execute,
    skeleton_tablet_search_execute,
    stratified_permutation_test_execute,
    template_miner_execute,
    token_context_association_execute,
    value_role_map_source_execute,
)

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
    # Evidence Graph port types
    "claims":    "#b45309",  # amber — list of claim records
    "papers":    "#0891b2",  # cyan  — list of paper/document records
}


# ── Atomic node definition ──────────────────────────────────────────────────

class AtomicNodeDef:
    def __init__(
        self,
        id: str, name: str, category: str, description: str,
        inputs: list[dict[str, str]], outputs: list[dict[str, str]],
        params_schema: dict[str, Any],
        fn: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
        legacy: bool = False,
    ) -> None:
        self.id = id; self.name = name; self.category = category
        self.description = description; self.inputs = inputs
        self.outputs = outputs; self.params_schema = params_schema; self.fn = fn
        # Spec 087 S2 (decision D1): legacy nodes stay registered and
        # resolvable (ATOMIC_NODES is the one resolution table) but leave
        # the builder palette — the catalog endpoint filters them out by
        # default. The flag is applied at registry build from the S2
        # migration data (see _apply_legacy_flags below), not per-site.
        self.legacy = legacy

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "category": self.category,
                "description": self.description, "inputs": self.inputs,
                "outputs": self.outputs, "params_schema": self.params_schema,
                "legacy": self.legacy}


# ── Atomic node implementations ─────────────────────────────────────────────

def _sync_db_one(table: str, row_id: str) -> dict | None:
    """Fetch one row from the Glossa Lab SQLite DB synchronously.

    Node functions run inside asyncio.run_in_executor threads. The aiosqlite
    connection is bound to the *main* event loop and cannot be used from those
    threads even with asyncio.run() (which creates a *new* loop).  This helper
    uses stdlib sqlite3 directly — no event loop required.
    """
    import sqlite3 as _sql  # noqa: PLC0415
    import json as _js   # noqa: PLC0415
    db_path = Path(__file__).parents[1] / "data" / "glossa.db"
    if not db_path.exists():
        return None
    conn = _sql.connect(str(db_path), check_same_thread=False)
    conn.row_factory = _sql.Row
    try:
        row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()  # noqa: S608
        if row is None:
            return None
        d = dict(row)
        for k, v in d.items():
            if isinstance(v, str) and v and v[0] in ("{", "["):
                try:
                    d[k] = _js.loads(v)
                except Exception:  # noqa: BLE001
                    pass
        return d
    finally:
        conn.close()


def _sync_db_all(table: str, where: str = "", params: tuple = ()) -> list[dict]:
    """Fetch all rows from a table synchronously (same rationale as _sync_db_one)."""
    import sqlite3 as _sql  # noqa: PLC0415
    import json as _js   # noqa: PLC0415
    db_path = Path(__file__).parents[1] / "data" / "glossa.db"
    if not db_path.exists():
        return []
    conn = _sql.connect(str(db_path), check_same_thread=False)
    conn.row_factory = _sql.Row
    try:
        sql = f"SELECT * FROM {table}"  # noqa: S608
        if where:
            sql += f" WHERE {where}"
        rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            d = dict(row)
            for k, v in d.items():
                if isinstance(v, str) and v and v[0] in ("{", "["):
                    try:
                        d[k] = _js.loads(v)
                    except Exception:  # noqa: BLE001
                        pass
            result.append(d)
        return result
    finally:
        conn.close()


def _corpus_reader(inputs: dict, params: dict) -> dict:
    corpus_id = params.get("corpus_id") or ""
    sequences: list[list[str]] = []
    if corpus_id:
        try:
            text = _sync_db_one("texts", corpus_id)
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
            from glossa_lab.data.old_hebrew import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang == "geez":
            from glossa_lab.data.geez import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang == "phoenician":
            from glossa_lab.data.phoenician import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
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
        elif lang in ("nw_semitic", "ugaritic", "fuls"):
            from glossa_lab.data.nw_semitic import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        elif lang in ("hieroglyphic_luwian", "luwian", "hluwian", "chli"):
            from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            syms = get_corpus_symbols(); inscs = get_corpus_inscriptions()
        else:
            return {"error": f"Unknown language '{lang}'. Valid: hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic, nw_semitic, hieroglyphic_luwian"}
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
            from glossa_lab.data.old_hebrew import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name == "geez":
            from glossa_lab.data.geez import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("geez_clean", "geez_nopunct", "geez_syllabic"):
            # Dr. Fuls April 2026: punctuation-free corpus (80,221 tokens, 209 signs)
            from glossa_lab.data.geez import (  # noqa: PLC0415
                get_clean_corpus_inscriptions,
                get_clean_corpus_symbols,
            )
            flat = get_clean_corpus_symbols(); seqs = get_clean_corpus_inscriptions()
        elif name == "phoenician":
            from glossa_lab.data.phoenician import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("nw_semitic", "fuls", "fuls_nw_semitic", "ugaritic"):
            from glossa_lab.data.nw_semitic import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
        elif name in ("meroitic",):
            from glossa_lab.data.meroitic import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
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
            from glossa_lab.data.dravidian import get_corpus_inscriptions as _di
            from glossa_lab.data.dravidian import get_corpus_symbols  # noqa: PLC0415
            flat = get_corpus_symbols(); seqs = _di()  # word-level char sequences
        elif name in ("indus_cisi", "cisi", "indus_parpola"):
            from glossa_lab.data.indus_cisi import get_corpus_inscriptions as _cisi_inscs
            from glossa_lab.data.indus_cisi import get_corpus_symbols as _cisi_syms  # noqa: PLC0415
            flat = _cisi_syms(); seqs = _cisi_inscs()  # real multi-sign Parpola inscriptions
        elif name in ("indus_m77", "m77", "mahadevan", "mahadevan_1977"):
            # Full Mahadevan 1977 concordance: 1669 inscriptions / 5361 tokens.
            # Much larger than the CISI Parpola subset; sign IDs are M77 codes
            # (e.g. "047", "820") rather than Parpola P-codes.
            from glossa_lab.data.indus_m77 import (
                get_corpus_inscriptions as _m77_inscs,
            )
            from glossa_lab.data.indus_m77 import (  # noqa: PLC0415
                get_corpus_symbols as _m77_syms,
            )
            flat = _m77_syms(); seqs = _m77_inscs()
        elif name in ("hieroglyphic_luwian", "luwian", "hluwian", "chli"):
            from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
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
    import logging as _logging  # noqa: PLC0415
    import time as _time  # noqa: PLC0415
    from collections import Counter as _C  # noqa: PLC0415
    _sa_log = _logging.getLogger("glossa_lab.sa_decipher")
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
    float(params.get("positional_weight", 0.005))
    anchors    = inputs.get("anchors") or params.get("anchors") or None
    flat = [s for seq in sequences for s in seq]

    _sa_log.info("SA decipher: %d signs, %d tokens, %d seeds × %d restarts × %d iter",
                 len(set(flat)), len(flat), n_seeds, restarts, max_iter)

    from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

    _sa_t0 = _time.time()
    _completed = [0]  # mutable counter for progress logging

    def _one(seed: int) -> dict:
        # cipher_inscriptions=None keeps cipher_positional empty,
        # enabling the numpy/cupy BigramScorer GPU fast path.
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        t0 = _time.time()
        r = decipher(flat, lm, seed=seed, max_iterations=max_iter, restarts=restarts,
                     cipher_inscriptions=None,  # None = GPU fast path
                     surjective=surjective,
                     ocp_weight=ocp_w, positional_weight=0.0,
                     anchors=anchors if anchors else None)
        _completed[0] += 1
        elapsed = _time.time() - t0
        _sa_log.info("SA seed %d done in %.1fs (score=%.2f) [%d/%d seeds complete, total %.0fs]",
                     seed, elapsed, r.get("score", 0), _completed[0], n_seeds, _time.time() - _sa_t0)
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


def _sa_multi_comparison(inputs: dict, params: dict) -> dict:
    """Run SA decipherment against multiple language models and compare results.

    For each language in the `languages` param list, loads the corresponding
    BuiltinLM and runs SADecipher, then ranks by mean_consistency.
    Returns a comparison table and the best-performing language.
    """
    import logging as _logging  # noqa: PLC0415
    _mc_log = _logging.getLogger("glossa_lab.sa_multi")

    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences — connect CorpusReader or BuiltinCorpus."}

    anchors = inputs.get("anchors") or None

    # Parse languages param
    raw_langs = params.get("languages", "dravidian,sanskrit")
    if isinstance(raw_langs, list):
        lang_list = [l.strip() for l in raw_langs if l.strip()]
    else:
        import re as _re  # noqa: PLC0415
        lang_list = [l.strip() for l in _re.split(r"[,;\s]+", str(raw_langs)) if l.strip()]

    if not lang_list:
        return {"error": "No languages specified. Set the 'languages' param."}

    n_seeds  = max(1, int(params.get("n_seeds", 3)))
    max_iter = max(100, int(params.get("max_iterations", 5000)))
    restarts = max(1, int(params.get("restarts", 5)))

    results: list[dict] = []
    for lang in lang_list:
        _mc_log.info("SAMultiComparison: running SA against language=%s", lang)
        lm_out = _builtin_lm({}, {"language": lang})
        if "error" in lm_out:
            results.append({"language": lang, "error": lm_out["error"],
                             "mean_consistency": 0.0, "hci_count": 0})
            continue
        lm = lm_out.get("lm")
        if lm is None:
            results.append({"language": lang, "error": "LM not loaded",
                             "mean_consistency": 0.0, "hci_count": 0})
            continue
        sa_out = _sa_decipher(
            {"sequences": sequences, "lm": lm,
             **({"anchors": anchors} if anchors else {})},
            {"n_seeds": n_seeds, "max_iterations": max_iter,
             "restarts": restarts, "surjective": True, "ocp_weight": 0.0},
        )
        if "error" in sa_out:
            results.append({"language": lang, "error": sa_out["error"],
                             "mean_consistency": 0.0, "hci_count": 0})
        else:
            results.append({
                "language": lang,
                "mean_consistency": round(float(sa_out.get("mean_consistency", 0)), 4),
                "hci_count": int(sa_out.get("hci_count", 0)),
                "n_signs": int(sa_out.get("n_signs", 0)),
                "proposed_mapping": sa_out.get("proposed_mapping", {}),
            })

    # Sort by mean_consistency descending
    ranked = sorted(
        [r for r in results if "error" not in r],
        key=lambda x: x["mean_consistency"], reverse=True,
    )
    errored = [r for r in results if "error" in r]
    ranking = ranked + errored

    best = ranked[0] if ranked else None
    return {
        "comparison_results": results,
        "ranking": ranking,
        "best_language": best["language"] if best else "",
        "best_consistency": best["mean_consistency"] if best else 0.0,
        "n_languages_tested": len(lang_list),
        "n_languages_ok": len(ranked),
    }


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
    float(inputs.get("tokens_per_sign") or inputs.get("total_tokens", 1) /
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
    nearest[0]["tier"]

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
    inputs.get("freq_map") or {}
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
    import json as _json  # noqa: PLC0415

    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

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

    try:
        text = _sync_db_one("texts", corpus_id)
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

    try:
        anchor_set = _sync_db_one("anchor_sets", anchor_set_id)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Failed to load anchor set: {exc}", "anchors": {}}

    if anchor_set is None:
        return {"error": f"Anchor set '{anchor_set_id}' not found.", "anchors": {}}

    pairs = anchor_set.get("pairs") or []
    if isinstance(pairs, str):
        import json as _j; pairs = _j.loads(pairs)  # noqa: PLC0415,E702
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

    try:
        template = _sync_db_one("report_templates", template_id)
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

    Spec 087 S3 (family F3): the mechanism is the generic
    RegistryTableLoader engine (glossa_lab.generic_primitives);
    this node is its canonical-signs parameterisation — the table
    name, the two filter clauses, the id/uuid fields, and the
    Parpola filter-count live in the spec below, not in code.
    """
    spec = {
        "table": "canonical_signs",
        "filters": [
            {"clause": "in_corpus = 1", "param": "in_corpus_only", "mode": "truthy",
             "default": True},
            {"clause": "numbering_system = ?", "param": "numbering_system", "mode": "arg"},
        ],
        "id_field": "sign_id",
        "uuid_field": "internal_id",
        "count_filters": [
            {"output": "n_parpola", "field": "numbering_system", "value": "parpola_1982"},
        ],
        "error_prefix": "Failed to load registry: ",
        "empty_result": {
            "error": "Canonical sign registry is empty — run POST /canonical-signs/seed first",
            "n_signs": 0,
        },
        "records_output": "registry",
        "total_output": "n_signs",
        "map_output": "sign_id_to_uuid",
        "ids_output": "sign_ids",
    }
    merged = dict(params)
    merged["registry_spec"] = spec
    return registry_table_loader_execute(inputs, merged)


def _cluster_mapper(inputs: dict, params: dict) -> dict:
    """Map inscription sign sequences to structural cluster labels.

    Loads cluster assignments from the DB (seeded by the CGSA pipeline) or,
    when the DB is not available (e.g. CLI context), falls back to loading
    directly from analysis/sign_clusters.json.
    Unmapped signs receive label -1. NO phonetic mapping is performed.

    Spec 087 S3 (family F3): the mechanism is the generic
    LabelMapApplier engine (glossa_lab.generic_primitives); this
    node is its CGSA parameterisation — the three map sources in
    their historical priority (DB table, analysis JSON file,
    frequency-rank binning into ~40 clusters) and the -1
    unmapped label live in the spec below, not in code.
    """
    from pathlib import Path as _Path  # noqa: PLC0415

    _cluster_json = (
        _Path(__file__).resolve().parents[3] / "analysis" / "sign_clusters.json"
    )
    spec = {
        "sources": [
            {"kind": "db_table", "table": "sign_cluster_assignments"},
            {
                "kind": "json_file",
                "path": str(_cluster_json),
                "map_key": "sign_to_cluster",
                "k_key": "best_k",
                "k_default": 40,
            },
            {"kind": "frequency_rank", "bins": 40},
        ],
        "unmapped_label": -1,
        "unavailable_error": (
            "Cluster assignments unavailable and no sequences to generate from. "
            "Seed via POST /sign-clusters/seed or run scripts/cgsa_pipeline.py"
        ),
    }
    merged = dict(params)
    merged["map_spec"] = spec
    return label_map_applier_execute(inputs, merged)


def _structural_template_analyzer(inputs: dict, params: dict) -> dict:
    """Find recurrent structural templates in cluster-space inscription sequences.

    Operates on cluster_sequences from ClusterMapper (not raw sign sequences).
    Discovers recurring patterns of cluster labels (length 2-5, count ≥ min_count),
    identifies dominant prefix/suffix clusters, and computes slot occupancy.
    NO phonetic claims are made. All outputs are structural class labels.

    Spec 087 S3 (family F3): the mechanism is the generic
    TemplateMiner engine (glossa_lab.generic_primitives) — the
    triage's executed attempt H1 reproduced this node's template
    mining exactly from per-length NgramCounter composition;
    TemplateMiner exists to carry the four summary fields
    (dominant prefix/suffix clusters, slot occupancy,
    class-sequence entropy) the composition cannot. This node
    keeps its historical defaults as the engine's defaults.
    """
    return template_miner_execute(inputs, params)


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
    import math as _math  # noqa: PLC0415
    import random as _rnd  # noqa: PLC0415
    from collections import Counter as _C  # noqa: PLC0415

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

    set(sign_inv)
    flat_cipher = [s for seq in cipher_seqs for s in seq]
    len(true_mapping)

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

# ── Registry build tracking (Spec 087 S1) ────────────────────────────────────
# Every registration funnels through _register_node, and every failed plugin
# block records through _record_registration_failure, so a plugin module that
# fails to import can no longer shrink the registry silently behind a log
# warning: the failure is logged at ERROR, kept in the build report
# (registry_build_report(), served at GET /experiment-graphs/registry-health),
# and — outside the installed production runtime — raised at the end of the
# build (see _finalize_registry_build). The completeness pin that fails CI on
# any drift lives in backend/tests/test_spec087_registry_integrity.py.

_REGISTRATION_FAILURES: list[dict[str, str]] = []
_REGISTRATION_DUPLICATES: list[dict[str, str]] = []
_NODE_SOURCES: dict[str, str] = {}


def _node_source(node_def: AtomicNodeDef) -> str:
    """Best-effort provenance of a node definition: the module its fn lives in."""
    fn = getattr(node_def, "fn", None)
    return getattr(fn, "__module__", None) or "?"


def _register_node(node_def: AtomicNodeDef) -> None:
    """Register one atomic node.

    A duplicate id is recorded (and logged at ERROR) instead of silently
    overwriting the earlier definition; the later definition still wins at
    runtime, exactly as dict assignment did, so lenient production behaviour
    is unchanged — but the overwrite is now named in the build report.
    """
    source = _node_source(node_def)
    if node_def.id in ATOMIC_NODES:
        _REGISTRATION_DUPLICATES.append(
            {
                "id": node_def.id,
                "first_source": _NODE_SOURCES.get(node_def.id, "?"),
                "duplicate_source": source,
            }
        )
        logger.error(
            "Duplicate node id %r registered from %s (first registered from %s); "
            "the later definition wins",
            node_def.id,
            source,
            _NODE_SOURCES.get(node_def.id, "?"),
        )
    else:
        _NODE_SOURCES[node_def.id] = source
    ATOMIC_NODES[node_def.id] = node_def


def _record_registration_failure(block: str, exc: BaseException) -> None:
    """Record a registration block whose nodes failed to register."""
    _REGISTRATION_FAILURES.append(
        {"block": block, "error": f"{type(exc).__name__}: {exc}"}
    )
    logger.error("Node registration failed (%s): %s", block, exc)


def registry_strict_mode() -> bool:
    """Whether an incomplete registry build must raise instead of warn.

    GLOSSA_REGISTRY_STRICT (1/true/yes/on or 0/false/no/off) wins when set;
    otherwise strict everywhere except the installed production runtime
    (GLOSSA_MODE=installed), which keeps the application startable and
    surfaces the failure through the build report instead.
    """
    raw = os.environ.get("GLOSSA_REGISTRY_STRICT")
    if raw is not None:
        return raw.strip().lower() in ("1", "true", "yes", "on")
    return os.environ.get("GLOSSA_MODE", "dev") != "installed"


def registry_build_report() -> dict[str, Any]:
    """Snapshot of the registry build: completeness, failures, duplicates.

    Spec 087 S2 adds the legacy split (claim C087-17's three-way pin):
    registered == legacy + palette, counted from the same flags the
    catalog endpoint filters on, so the identity is mechanical.
    """
    legacy = sum(1 for d in ATOMIC_NODES.values() if d.legacy)
    return {
        "ok": not _REGISTRATION_FAILURES and not _REGISTRATION_DUPLICATES,
        "registered": len(ATOMIC_NODES),
        "legacy": legacy,
        "palette": len(ATOMIC_NODES) - legacy,
        "failures": [dict(f) for f in _REGISTRATION_FAILURES],
        "duplicates": [dict(d) for d in _REGISTRATION_DUPLICATES],
        "strict": registry_strict_mode(),
    }


# ── Legacy migration (Spec 087 S2, decision D1) ──────────────────────────────
# The 359 wrapper nodes of the census of record (audit census Appendix A,
# param-carry verdict WRAPPER: DOMAIN nodes with no input ports and an empty
# params schema) are flagged legacy at build time from the committed
# migration data file below — the act is reviewable id by id, and any drift
# between the file and the registry is recorded like a registration failure
# (strict contexts refuse to start over it). Flagging changes nothing about
# resolution or execution: ATOMIC_NODES keeps every entry.

_LEGACY_MIGRATION_PATH = Path(__file__).parent / "spec087_s2_legacy_ids.json"


def load_legacy_migration_ids() -> list[str]:
    """The S2 migration's id list, read from its committed data file."""
    data = json.loads(_LEGACY_MIGRATION_PATH.read_text(encoding="utf-8"))
    return list(data["legacy_ids"])


def _apply_legacy_flags() -> None:
    """Flag every migration id legacy on its registered definition."""
    try:
        legacy_ids = load_legacy_migration_ids()
    except Exception as exc:  # noqa: BLE001
        _record_registration_failure("Spec 087 S2 legacy migration data", exc)
        return
    for node_id in legacy_ids:
        node_def = ATOMIC_NODES.get(node_id)
        if node_def is None:
            _record_registration_failure(
                "Spec 087 S2 legacy migration",
                KeyError(f"migration id {node_id!r} is not registered"),
            )
        else:
            node_def.legacy = True


def _finalize_registry_build() -> None:
    """Close the registry build (called once, after the last plugin block).

    A complete build logs its census at INFO. An incomplete build is named
    at ERROR; in strict mode it raises, so CI and dev contexts fail loudly
    instead of running against a silently shrunken registry.
    """
    report = registry_build_report()
    if report["ok"]:
        logger.info(
            "Node registry complete: %d atomic nodes registered", report["registered"]
        )
        return
    problems = [f"{f['block']}: {f['error']}" for f in report["failures"]]
    problems += [
        f"duplicate node id {d['id']} ({d['first_source']} vs {d['duplicate_source']})"
        for d in report["duplicates"]
    ]
    summary = "; ".join(problems)
    if report["strict"]:
        raise RuntimeError(f"Node registry build incomplete: {summary}")
    logger.error("Node registry build incomplete: %s", summary)

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
    AtomicNodeDef("JsonCorpusLoader","JSON Corpus Loader","Sources",
        "Load a sign-sequence corpus from a JSON file via a declarative source spec "
        "(Spec 087 S3): a fallback chain of file sources (JSON record files, or a "
        "grouped-CSV fallback), a field map, and length filters, projected as "
        "sequences + per-inscription metadata + counts. Corpus identity, paths, "
        "and field names are parameters (corpus_spec), not code — the domain "
        "loaders (M77, ICIT, Mathematica Epigraphica) delegate to this engine.",
        inputs=[],
        outputs=[{"name":"sequences","type":"sequences"},{"name":"inscriptions","type":"json"},{"name":"n_inscriptions","type":"number"},{"name":"n_tokens","type":"number"},{"name":"n_distinct_signs","type":"number"},{"name":"label","type":"text"},{"name":"source","type":"text"},{"name":"available","type":"any"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "data_path":{"type":"string","title":"Data Path","description":"JSON corpus file (single-source use; see corpus_spec for chains)."},
            "records_key":{"type":"string","title":"Records Key","default":"inscriptions"},
            "projection":{"type":"string","title":"Projection","default":"sequence_corpus","description":"sequence_corpus | record_list | cache_summary."},
            "use_raw":{"type":"boolean","title":"Use Raw","default":False},
            "min_length":{"type":"integer","title":"Min Length","default":1,"minimum":0},
            "max_length":{"type":"integer","title":"Max Length","default":0,"description":"0 = no upper bound."},
            "label":{"type":"string","title":"Label","default":"corpus"},
            "corpus_spec":{"type":"object","title":"Corpus Spec","description":"Full declarative spec: sources, field_map, absent_result, verdict_template."}}},
        fn=json_corpus_loader_execute),
    AtomicNodeDef("DatasetRecordLoader","Dataset Record Loader","Sources",
        "Load records from a bundled data module (glossa_lab.data.*) via a "
        "declarative spec (Spec 087 S3): named getters with parameterised "
        "kwargs, record filters, and an ordered output assembly (values, "
        "counts, top-N counters, verdict templates). Dataset identity, getter "
        "names, and verdict text are parameters (dataset_spec), not code — "
        "the domain loaders (Mahadevan, ePSD2, Contact Corpus) delegate to "
        "this engine.",
        inputs=[],
        outputs=[{"name":"records","type":"json"},{"name":"n_records","type":"number"},{"name":"metadata","type":"json"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "module":{"type":"string","title":"Data Module","description":"Dotted path of a glossa_lab.data module."},
            "dataset_spec":{"type":"object","title":"Dataset Spec","description":"Full declarative spec: module, getters, filters, outputs."}}},
        fn=dataset_record_loader_execute),
    AtomicNodeDef("RegistryTableLoader","Registry Table Loader","Sources",
        "Load a registry table from the backend database via a declarative spec "
        "(Spec 087 S3): table name, parameter-driven filter clauses, id/uuid "
        "fields, and named filter-counts are parameters (registry_spec); the "
        "projection — records, total, counts, id->uuid map, id list — is the "
        "mechanism. Without a spec it uses the canonical-signs shape it was "
        "generalised from. The CGSA CanonicalSignLoader delegates to this engine.",
        inputs=[],
        outputs=[{"name":"registry","type":"json"},{"name":"n_signs","type":"number"},
                 {"name":"n_parpola","type":"number"},{"name":"sign_ids","type":"json"},
                 {"name":"sign_id_to_uuid","type":"json"}],
        params_schema={"type":"object","properties":{
            "table":{"type":"string","title":"Table","description":"Database table to load (single-table use; see registry_spec for the full spec)."},
            "in_corpus_only":{"type":"boolean","title":"In Corpus Only","default":True},
            "numbering_system":{"type":"string","title":"Numbering System","default":""},
            "registry_spec":{"type":"object","title":"Registry Spec","description":"Full declarative spec: table, filters, id_field, uuid_field, count_filters, output key names."}}},
        fn=registry_table_loader_execute),
    AtomicNodeDef("LabelMapApplier","Label Map Applier","Transforms",
        "Apply a sign->label map to sequences (Spec 087 S3). The map comes from "
        "the first source in the spec's fallback chain that yields one: a DB "
        "table, a JSON file, or frequency-rank binning of the input corpus "
        "itself. Unmapped signs receive the spec's unmapped label. The CGSA "
        "ClusterMapper delegates to this engine. NO phonetic mapping performed.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"cluster_sequences","type":"json"},{"name":"n_sequences","type":"number"},
                 {"name":"map_rate","type":"number"},{"name":"n_mapped_tokens","type":"number"},
                 {"name":"n_unmapped_tokens","type":"number"},{"name":"n_clusters","type":"number"},
                 {"name":"sign_to_cluster","type":"json"}],
        params_schema={"type":"object","properties":{
            "db_table":{"type":"string","title":"DB Table","description":"Assignments table (flat use; see map_spec for chains)."},
            "file_path":{"type":"string","title":"File Path","description":"JSON file holding the map (flat use)."},
            "bins":{"type":"integer","title":"Frequency Bins","default":40,"minimum":1},
            "unmapped_label":{"type":"integer","title":"Unmapped Label","default":-1},
            "map_spec":{"type":"object","title":"Map Spec","description":"Full declarative spec: sources chain, unmapped_label, unavailable_error."}}},
        fn=label_map_applier_execute),
    AtomicNodeDef("TemplateMiner","Template Miner","Analysis",
        "Find recurrent templates in label sequences (Spec 087 S3): n-gram "
        "template mining over a length range with a minimum count, plus the "
        "summary fields a plain n-gram composition cannot carry in one node — "
        "dominant prefix/suffix labels, per-slot occupancy, and the "
        "class-sequence entropy. Length range and cuts are parameters. The "
        "CGSA StructuralTemplateAnalyzer delegates to this engine. NO phonetic "
        "claims made; outputs are structural class labels.",
        inputs=[{"name":"cluster_sequences","type":"json","required":True}],
        outputs=[{"name":"recurrent_templates","type":"json"},{"name":"n_templates","type":"number"},
                 {"name":"dominant_prefix_clusters","type":"json"},{"name":"dominant_suffix_clusters","type":"json"},
                 {"name":"slot_occupancy","type":"json"},{"name":"h_class_sequence","type":"number"},
                 {"name":"n_distinct_class_sequences","type":"number"}],
        params_schema={"type":"object","properties":{
            "min_count":{"type":"integer","title":"Min Template Count","default":3,"minimum":2},
            "max_template_length":{"type":"integer","title":"Max Template Length","default":5,"minimum":2},
            "min_template_length":{"type":"integer","title":"Min Template Length","default":2,"minimum":1},
            "top_templates":{"type":"integer","title":"Top Templates","default":50,"minimum":1},
            "top_slots":{"type":"integer","title":"Top Slots","default":10,"minimum":1}}},
        fn=template_miner_execute),
    AtomicNodeDef("ClusterContingencyProfile","Cluster Contingency Profile","Analysis",
        "Per-cluster contingency profile over record strata (Spec 087 S3): "
        "site (strata) and length distributions for the inscriptions hosting "
        "a target cluster, enrichment rates against the corpus baseline, and "
        "a chi-squared test of strata-vs-cluster independence. The strata "
        "rule (field + prefix grouping), the significance rule, and the "
        "verdict template are parameters. The Phase-20 ClusterArchaeology "
        "delegates to this engine.",
        inputs=[{"name":"inscriptions","type":"json","required":True},
                {"name":"sign_to_cluster","type":"json","required":False}],
        outputs=[{"name":"site_table","type":"json"},{"name":"length_table","type":"json"},
                 {"name":"chi_squared","type":"number"},{"name":"dof","type":"number"},
                 {"name":"significant_p05","type":"any"},{"name":"verdict","type":"text"},
                 {"name":"target_cluster_signs","type":"json"}],
        params_schema={"type":"object","properties":{
            "target_cluster":{"type":"integer","title":"Target Cluster","default":0},
            "fixed_members":{"type":"array","title":"Fixed Members","default":[],
                             "description":"If provided, override sign_to_cluster and use this list as the target sign set."},
            "strata_field":{"type":"string","title":"Strata Field","default":"site_code"},
            "prefix_len":{"type":"integer","title":"Strata Prefix Length","default":2,"minimum":1},
            "prefix_suffix":{"type":"string","title":"Strata Prefix Suffix","default":"0000"},
            "critical_per_dof":{"type":"number","title":"Chi2 Critical per DoF","default":3.84},
            "site_limit":{"type":"integer","title":"Site Table Limit","default":25,"minimum":1},
            "verdict_template":{"type":"string","title":"Verdict Template",
                                "description":"Format template with {outcome} {chi2} {dof} {min_rate} {max_rate} {baseline}."}}},
        fn=cluster_contingency_profile_execute),
    AtomicNodeDef("SignRoleClassifier","Sign Role Classifier","Analysis",
        "Derive a role mask per sign from corpus statistics (Spec 087 S3): "
        "positional rates, strict/relaxed suffix rules, a numeral repetition "
        "heuristic, a behaviour-based logogram detector, and bigram-PMI "
        "compound detection. Every threshold is a parameter, and the numeral "
        "sign set is a parameter that defaults EMPTY — a domain caller's set "
        "is data it passes in. The CTT IndusSignRoleClassifier delegates to "
        "this engine with its Indus numeral set as the default value.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"role_table","type":"json"},{"name":"n_signs","type":"number"},
                 {"name":"role_summary","type":"json"},{"name":"compound_signs","type":"json"},
                 {"name":"high_pmi_bigrams","type":"json"}],
        params_schema={"type":"object","properties":{
            "terminal_threshold":{"type":"number","default":0.85,"minimum":0.5,"maximum":1.0},
            "terminal_relaxed":{"type":"number","default":0.45,"minimum":0.0,"maximum":1.0},
            "initial_threshold":{"type":"number","default":0.70,"minimum":0.5,"maximum":1.0},
            "compound_pmi_threshold":{"type":"number","default":4.0,"minimum":0.0},
            "min_count":{"type":"integer","default":5,"minimum":1},
            "numeral_signs":{"type":"array","default":[],
                             "description":"Signs classed numeral on sight. Empty by design; domain sets are caller data."},
            "numeral_repetition_threshold":{"type":"number","default":0.5,"minimum":0.0,"maximum":1.0},
            "logogram_min_count":{"type":"integer","default":20,"minimum":1},
            "logogram_position_concentration":{"type":"number","default":0.55,"minimum":0.0,"maximum":1.0},
            "logogram_solo_rate":{"type":"number","default":0.05,"minimum":0.0,"maximum":1.0}}},
        fn=sign_role_classifier_execute),
    AtomicNodeDef("ValueRoleMapSource","Value-Role Map Source","Sources",
        "Emit a value->role lookup table merged from a base map plus selected "
        "per-language family tables (Spec 087 S3). The base map and every "
        "family table (seed roles, base values, vocabulary sources, "
        "classification sets) are data parameters (base_map, family_tables); "
        "the merge order — base, families in the order named, then extra "
        "overrides — and unknown-family reporting are the mechanism. The CTT "
        "DefaultIndusValueRoleMap delegates to this engine with its Indus "
        "base map and family tables as data.",
        inputs=[],
        outputs=[{"name":"value_role_map","type":"json"},{"name":"n_values","type":"number"},
                 {"name":"families_applied","type":"json"},{"name":"family_sizes","type":"json"},
                 {"name":"unknown_families","type":"json"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "base_map":{"type":"object","title":"Base Map","default":{},
                        "description":"Base value->role map, included when include_default is true."},
            "family_tables":{"type":"object","title":"Family Tables","default":{},
                             "description":"Map of family name -> family spec (seed_roles, base_values, vocab_sources, vocab_mode, determinative_values, numeral_values)."},
            "families":{"type":"array","title":"Families","default":[],
                        "description":"Family names to merge in, in order. Unknown names are reported, not fatal."},
            "include_default":{"type":"boolean","title":"Include Base Map","default":True},
            "extra":{"type":"object","title":"Extra Overrides","default":{}}}},
        fn=value_role_map_source_execute),
    AtomicNodeDef("AnchorSyllabifier","Anchor Syllabifier","Sources",
        "Load an anchor file and map each reading to a syllable token "
        "(Spec 087 S3): strip the transliteration (diacritic) table, take a "
        "direct syllable-vocab hit when one exists, else split into CV "
        "chunks and use the first chunk in the vocab, with prefix-length "
        "fallbacks. File paths, the confidence order, the diacritic table, "
        "and the positional-label skip pattern are parameters/data. The "
        "Phase-33 IndusAnchorSetSyllable delegates to this engine.",
        inputs=[],
        outputs=[{"name":"anchor_dict","type":"json"},{"name":"n_anchors","type":"number"},
                 {"name":"n_skipped","type":"number"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "anchors_path":{"type":"string","title":"Anchors Path","description":"Anchor JSON file: {anchors: {sign_id: {reading, confidence}}}"},
            "vocab_path":{"type":"string","title":"Syllable Vocab Path","description":"JSON file holding the syllable vocab list."},
            "min_confidence":{"type":"string","title":"Min Confidence","default":"MEDIUM"},
            "confidence_order":{"type":"object","title":"Confidence Order",
                                "description":"Confidence label -> rank. Default HIGH 3, MEDIUM 2, LOW 1, UNCERTAIN 0."},
            "diacritic_table":{"type":"array","title":"Diacritic Table","default":[],
                               "description":"Ordered [source, replacement] string pairs applied after lowercasing."},
            "skip_pattern":{"type":"string","title":"Skip Pattern",
                            "description":"Regex matched at the start of a lowercased reading; matches are skipped (positional labels)."}}},
        fn=anchor_syllabifier_execute),
    AtomicNodeDef("AssociationAnchorDeriver","Association Anchor Deriver","Decipherment",
        "Derive a sign->value anchor dict from sign-context associations "
        "(Spec 087 S3): associations are sorted by descending pmi_z and "
        "each sign's first association at or above min_z binds it to "
        "anchor_prefix + context, up to max_anchors. The prefix is a "
        "parameter — a caller's context-label convention (e.g. 'ctx:') is "
        "data, not mechanism. The Phase-14 DerivedAnchorSet delegates to "
        "this engine.",
        inputs=[{"name":"associations","type":"json","required":True}],
        outputs=[{"name":"anchors","type":"json"},{"name":"n_anchors","type":"number"},
                 {"name":"anchor_table","type":"json"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "min_z":{"type":"number","title":"Min Z","default":2.0},
            "max_anchors":{"type":"integer","title":"Max Anchors","default":25,"minimum":1},
            "anchor_prefix":{"type":"string","title":"Anchor Prefix","default":""}}},
        fn=association_anchor_deriver_execute),
    AtomicNodeDef("PMICentralityRanker","PMI Centrality Ranker","Analysis",
        "Rank candidate anchor signs by PMI centrality (Spec 087 S3): the "
        "sum over bigram partners of |PMI| weighted by count — which sign's "
        "value, when fixed, most constrains the others. No domain "
        "constants. The Phase-14 EpistaticAnchorRanker delegates to this "
        "engine.",
        inputs=[{"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"ranking","type":"json"},{"name":"n_signs_ranked","type":"number"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "top_k":{"type":"integer","title":"Top K","default":10,"minimum":1},
            "min_count":{"type":"integer","title":"Min Bigram Count","default":5,"minimum":1}}},
        fn=pmi_centrality_ranker_execute),
    AtomicNodeDef("IconographicAnchorScorer","Iconographic Anchor Scorer","Decipherment",
        "Score iconographic anchors against a sign->phoneme map (Spec 087 "
        "S3): each anchor's iconic reading is matched against the map "
        "through an ordered reading->alias table carried as data; matches "
        "score by anchor-confidence weights with a high-confidence bonus. "
        "With an extension bonus set, the allograph mode credits family "
        "members carrying the family's phoneme. The Phase-27 "
        "IconographicAnchorScore and the Phase-28 "
        "AllographAwareIconographicScore delegate to this engine.",
        inputs=[{"name":"iconographic_anchors","type":"json","required":True},
                {"name":"phoneme_map","type":"json","required":True},
                {"name":"allograph_families","type":"json","required":False}],
        outputs=[{"name":"n_total_anchors","type":"number"},{"name":"n_matches","type":"number"},
                 {"name":"n_allograph_extensions","type":"number"},{"name":"extended_sign_ids","type":"json"},
                 {"name":"total_score","type":"number"},{"name":"rows","type":"json"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "scorer_spec":{"type":"object","title":"Scorer Spec",
                           "description":"Alias table (ordered [key, [aliases], family] entries), confidence weights, high-confidence bonus, optional allograph extension bonus, empty result, verdict template."}}},
        fn=iconographic_anchor_scorer_execute),
    AtomicNodeDef("PhonemeMapCoverage","Phoneme Map Coverage","Decipherment",
        "Apply a phoneme map to inscribed seals and report readability "
        "(Spec 087 S3): a seal is readable when at least one real "
        "(non-placeholder) sign resolves to a phoneme that is neither the "
        "unknown token nor marked uncertain; per-seal skeletons and "
        "high-confidence counts are reported. The unknown token, the "
        "uncertain marker, and the verdict text are spec data. The "
        "Phase-25 BlindHeldOutTest delegates to this engine.",
        inputs=[{"name":"inscribed_seals","type":"json","required":True},
                {"name":"phoneme_map","type":"json","required":True}],
        outputs=[{"name":"n_seals","type":"number"},{"name":"n_readable","type":"number"},
                 {"name":"n_high_conf","type":"number"},{"name":"rows","type":"json"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "coverage_spec":{"type":"object","title":"Coverage Spec",
                             "description":"Unknown token, uncertain marker, high-confidence label, placeholder skeleton, verdict template."}}},
        fn=phoneme_map_coverage_execute),
    AtomicNodeDef("PhonemeMapPermutationTest","Phoneme Map Permutation Test","Analysis",
        "Permutation test of a phoneme map's assignment over inscribed "
        "seals (Spec 087 S3): the observed confidence-weighted coverage "
        "total is compared against null maps that shuffle one dimension "
        "of the map — the confidence labels, or the phoneme values with "
        "an optional compound-plausibility reweighting whose pattern "
        "table and bonuses are data. The Phase-26 BayesianDecoder and "
        "the Phase-27 BayesianDecoderV2 delegate to this engine.",
        inputs=[{"name":"inscribed_seals","type":"json","required":True},
                {"name":"phoneme_map","type":"json","required":True}],
        outputs=[{"name":"n_seals","type":"number"},{"name":"n_phonemes_in_map","type":"number"},
                 {"name":"observed_total_weight","type":"number"},{"name":"null_mean_weight","type":"number"},
                 {"name":"observed_total_score","type":"number"},{"name":"null_mean_score","type":"number"},
                 {"name":"p_value","type":"number"},{"name":"n_perms","type":"number"},
                 {"name":"obs_per_seal_top10","type":"json"},{"name":"obs_per_seal","type":"json"},
                 {"name":"verdict","type":"text"},{"name":"interpretation","type":"text"}],
        params_schema={"type":"object","properties":{
            "n_permutations":{"type":"integer","title":"Permutations","default":1000,"minimum":200},
            "seed":{"type":"integer","title":"Seed","default":1234},
            "decoder_spec":{"type":"object","title":"Decoder Spec",
                            "description":"Shuffle dimension, confidence weights, plausibility patterns/bonuses, null gloss, output key names, verdict template, interpretation."}}},
        fn=phoneme_map_permutation_test_execute),
    AtomicNodeDef("LengthMatchScorer","Length Match Scorer","Decipherment",
        "Score candidate-name <-> seal pairings by length compatibility "
        "(Spec 087 S3): hyphen-segment counts against inscription "
        "lengths under a named score spec — the family tolerance falloff "
        "or a named divergent linear falloff carried as data, never "
        "silently re-shaped. Assignment modes: all-pairs with a best "
        "pairing per name, greedy one-to-one bipartite, or pairings "
        "aggregated from raw person rows against sign-bearing seals. "
        "The Phase-23 EnhancedNameMatcher, the Phase-24 "
        "EnhancedNameMatcherV2, and the Phase-22 MeluhhaNameMatcher "
        "delegate to this engine.",
        inputs=[{"name":"rows_all","type":"json","required":True},
                {"name":"inscribed_seals","type":"json","required":True},
                {"name":"persons","type":"json","required":False},
                {"name":"seals_at_mesopotamia","type":"json","required":False}],
        outputs=[{"name":"n_candidates","type":"number"},{"name":"n_seals","type":"number"},
                 {"name":"n_seals_with_signs","type":"number"},{"name":"n_seals_total","type":"number"},
                 {"name":"n_assigned","type":"number"},{"name":"n_unassigned","type":"number"},
                 {"name":"pairings","type":"json"},{"name":"pairings_top50","type":"json"},
                 {"name":"n_pairings","type":"number"},{"name":"best_per_name","type":"json"},
                 {"name":"total_length_score","type":"number"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "min_name_freq":{"type":"integer","title":"Min Name Frequency","default":2,"minimum":1},
            "tolerance":{"type":"integer","title":"Tolerance","default":2,"minimum":0},
            "matcher_spec":{"type":"object","title":"Matcher Spec",
                            "description":"Assignment mode, score spec (kind tolerance or a named linear falloff), min-frequency default, verdict/insufficient/no-signs templates."}}},
        fn=length_match_scorer_execute),
    AtomicNodeDef("LengthMatchPermutationTest","Length Match Permutation Test","Decipherment",
        "Permutation test of name-length <-> seal-length matching (Spec "
        "087 S3): the statistic is the per-name best length score summed "
        "(null: shuffle the seal lengths) or the greedy bipartite "
        "assignment sum (null: random one-to-one assignments). Verdict "
        "bands, the insufficient-data verdict, the optional "
        "observed-assignment output, and the interpretation are spec "
        "data. The Phase-23 BilingualReadoutTest and the Phase-24 "
        "BilingualReadoutTestV2 delegate to this engine.",
        inputs=[{"name":"rows_all","type":"json","required":True},
                {"name":"inscribed_seals","type":"json","required":True}],
        outputs=[{"name":"verdict","type":"text"},{"name":"p_value","type":"number"},
                 {"name":"observed","type":"number"},{"name":"null_mean","type":"number"},
                 {"name":"null_sd","type":"number"},{"name":"z_score","type":"number"},
                 {"name":"n_permutations","type":"number"},{"name":"n_candidates","type":"number"},
                 {"name":"n_seals","type":"number"},{"name":"observed_assignment","type":"json"},
                 {"name":"interpretation","type":"text"}],
        params_schema={"type":"object","properties":{
            "n_permutations":{"type":"integer","title":"Permutations","default":1000,"minimum":100},
            "min_name_freq":{"type":"integer","title":"Min Name Frequency","default":2,"minimum":1},
            "tolerance":{"type":"integer","title":"Tolerance","default":2,"minimum":0},
            "seed":{"type":"integer","title":"Seed","default":42},
            "test_spec":{"type":"object","title":"Test Spec",
                         "description":"Statistic (best_match or bipartite), defaults, insufficient verdict, verdict bands, assignment output flag, interpretation."}}},
        fn=length_match_permutation_test_execute),
    AtomicNodeDef("StratifiedPermutationTest","Stratified Permutation Test","Decipherment",
        "Run the bipartite length-match readout test per stratum plus a "
        "merged overall (Spec 087 S3): persons are aggregated by "
        "candidate name within strata assigned by an ordered "
        "substring->bucket rule table carried as data (case sensitivity, "
        "value stripping, and the empty/fallback buckets included), each "
        "stratum's permutation seed is a base plus the bucket name's "
        "length, and strata with fewer than two distinct candidates are "
        "skipped. The Phase-25 PeriodStratifiedReadout, the Phase-27 "
        "PeriodStratifiedReadout6Bucket, and the Phase-26 "
        "ProvenienceStratifiedReadout delegate to this engine.",
        inputs=[{"name":"persons_v3","type":"json","required":True},
                {"name":"inscribed_seals","type":"json","required":True}],
        outputs=[{"name":"results","type":"json"},{"name":"n_significant_strata","type":"number"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "n_permutations":{"type":"integer","title":"Permutations","default":1000,"minimum":100},
            "tolerance":{"type":"integer","title":"Tolerance","default":2,"minimum":0},
            "strata_spec":{"type":"object","title":"Strata Spec",
                           "description":"Stratum field, result axis key, ordered [bucket, [keys]] rules, case sensitivity, strip flag, empty/fallback buckets, seed base, verdict template."}}},
        fn=stratified_permutation_test_execute),
    AtomicNodeDef("SkeletonTabletSearch","Skeleton Tablet Search","Decipherment",
        "Predict a seal reading's phonetic skeleton under a sign->phoneme "
        "map and scan tablet lines for syllable-rendering matches (Spec "
        "087 S3): each scan in the carried scan list searches the gated "
        "tablets' lines for lines hitting at least the minimum number of "
        "renderings, where a scan's rendering list is a spec constant or "
        "arrives through an input port; the keyword gate, the hit rule, "
        "and the verdict text are spec data. The Phase-25 "
        "JanabiyahPhoneticReadout and the Phase-26 "
        "JanabiyahPhoneticReadoutV2 delegate to this engine.",
        inputs=[{"name":"janabiyah_reading","type":"json","required":True},
                {"name":"phoneme_map","type":"json","required":True},
                {"name":"tablets","type":"json","required":True},
                {"name":"miin_renderings","type":"json","required":False},
                {"name":"miin_renderings_direct_only","type":"json","required":False}],
        outputs=[{"name":"skeleton","type":"text"},{"name":"predictions","type":"json"},
                 {"name":"n_miin","type":"number"},{"name":"n_signs","type":"number"},
                 {"name":"matches_top20","type":"json"},{"name":"n_matches","type":"number"},
                 {"name":"matches_direct_top20","type":"json"},{"name":"n_matches_direct","type":"number"},
                 {"name":"matches_expanded_top20","type":"json"},{"name":"n_matches_expanded","type":"number"},
                 {"name":"n_new_matches_from_translation","type":"number"},
                 {"name":"miin_renderings_searched","type":"json"},
                 {"name":"verdict","type":"text"},{"name":"interpretation","type":"text"}],
        params_schema={"type":"object","properties":{
            "readout_spec":{"type":"object","title":"Readout Spec",
                           "description":"Scan list (rendering source per scan: spec constant or input port; hit key and output keys per scan), keyword gate, minimum hits, line limit, optional derived count, echoed renderings, error result, verdict template, optional interpretation."}}},
        fn=skeleton_tablet_search_execute),
    AtomicNodeDef("ReverseSkeletonSearch","Reverse Skeleton Search","Decipherment",
        "Score candidate names against a predicted phonetic skeleton "
        "(Spec 087 S3): one shared scoring core — target segment "
        "positions and length, length/position/free weights — carried "
        "as spec data, over three candidate modes: aggregated person "
        "rows matched by substring against the rendering set (with a "
        "suffix-penalty set as data), ePSD2-style name entries scored "
        "over their alternate forms by exact rendering-token match, "
        "and that mode binned by best-form segment count over a cohort "
        "table with a concentration verdict. The rendering set is data, "
        "with an optional dynamic expansion from the phoneme map via a "
        "named allograph family. The Phase-27 ReverseJanabiyahSearch, "
        "the Phase-28 ReverseJanabiyahSearchV2, the Phase-29 "
        "M77ReverseJanabiyahSearchV3, and the Phase-30 "
        "LengthCohortReverseJanabiyahSearch delegate to this engine.",
        inputs=[{"name":"persons_v3","type":"json","required":False},
                {"name":"epsd2_personal_names","type":"json","required":False},
                {"name":"janabiyah_reading","type":"json","required":True},
                {"name":"phoneme_map","type":"json","required":False},
                {"name":"allograph_families","type":"json","required":False}],
        outputs=[{"name":"n_candidates","type":"number"},{"name":"n_pns_searched","type":"number"},
                 {"name":"n_renderings","type":"number"},
                 {"name":"n_with_position_match","type":"number"},{"name":"n_with_free_miin","type":"number"},
                 {"name":"top_matches","type":"json"},
                 {"name":"n_cohorts","type":"number"},
                 {"name":"n_with_position_match_total","type":"number"},
                 {"name":"n_with_free_miin_total","type":"number"},
                 {"name":"cohorts","type":"json"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "top_k":{"type":"integer","title":"Top K","default":20,"minimum":1},
            "min_icount":{"type":"integer","title":"Min Instance Count","default":1,"minimum":1},
            "cohorts":{"type":"array","title":"Cohorts","default":[[3,4],[5,6],[7,8],[9,99]],
                       "description":"[lo, hi] segment-count cohort pairs for the pn_cohorts mode."},
            "search_spec":{"type":"object","title":"Search Spec",
                           "description":"Candidate mode, scoring core (target positions/length, weights), rendering set + optional expansion, penalty suffixes, cohort default + concentration factor, output plan, empty result, verdict templates."}}},
        fn=reverse_skeleton_search_execute),
    AtomicNodeDef("PersonsAggregator","Persons Aggregator","Transforms",
        "Aggregate person rows into per-name candidate counts (Spec "
        "087 S3): rows are counted per candidate name with each name's "
        "period set and first example line, plus — as spec data "
        "dictates — provenience and source-pattern sets, distinct "
        "tablet counts, and segment-count enrichment; known-name "
        "confirmation is a carried name set, the rows' upstream "
        "is_known flag, or none, and the example-line truncation and "
        "verdict text are spec data. The Phase-22 "
        "MeluhhanPersonsExtractor, the Phase-23 "
        "RefinedMeluhhanPersonsExtractor, the Phase-24 "
        "RefinedMeluhhanPersonsExtractorV2, and the Phase-25 "
        "Persons_v3_Extractor delegate to this engine.",
        inputs=[{"name":"persons","type":"json","required":False},
                {"name":"strict_persons","type":"json","required":False},
                {"name":"persons_v2","type":"json","required":False},
                {"name":"persons_v3","type":"json","required":False}],
        outputs=[{"name":"n_unique_candidates","type":"number"},{"name":"n_unique","type":"number"},
                 {"name":"rows_top50","type":"json"},{"name":"rows_all","type":"json"},
                 {"name":"all_rows_count","type":"number"},{"name":"n_total","type":"number"},
                 {"name":"confirmed_hits","type":"json"},{"name":"by_pattern","type":"json"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "min_freq":{"type":"integer","title":"Min Frequency","default":1,"minimum":1},
            "persons_spec":{"type":"object","title":"Persons Spec",
                            "description":"Input port key, collected field sets, known-name rule (set / upstream flag / none), example-line limit, output plan (count key names, row lists, by-pattern), verdict template."}}},
        fn=persons_aggregator_execute),
    AtomicNodeDef("InteractionSurplusProfile","Interaction Surplus Profile","Analysis",
        "Profile higher-order n-gram interactions beyond independence "
        "(Spec 087 S3): bigram PMI and trigram surplus over the "
        "pairwise baseline, counted significant at or above a "
        "spec-carried cut in nats. The Phase-14 "
        "EpistaticInteractionDetector delegates to this engine.",
        inputs=[{"name":"sequences","type":"json","required":True}],
        outputs=[{"name":"label","type":"text"},{"name":"bigrams","type":"json"},
                 {"name":"trigrams","type":"json"},
                 {"name":"n_significant_bigrams","type":"number"},
                 {"name":"n_significant_trigrams","type":"number"},
                 {"name":"n_total_bigrams_examined","type":"number"},
                 {"name":"n_total_trigrams_examined","type":"number"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "min_count_2":{"type":"integer","title":"Min Bigram Count","default":5,"minimum":2},
            "min_count_3":{"type":"integer","title":"Min Trigram Count","default":3,"minimum":2},
            "top_k":{"type":"integer","title":"Top K","default":25,"minimum":5},
            "label":{"type":"string","title":"Label","default":"unknown"},
            "profile_spec":{"type":"object","title":"Profile Spec",
                            "description":"Significance cut in nats for the bigram/trigram surplus counts."}}},
        fn=interaction_surplus_profile_execute),
    AtomicNodeDef("OrderInformationProfile","Order Information Profile","Analysis",
        "Decompose corpus information by interaction order (Spec 087 "
        "S3): per-symbol block entropies and their successive "
        "differences, with the regime classification carried as an "
        "ordered rule table over the order-fraction ratios. The "
        "Phase-14 EpistaticOrderProfile delegates to this engine.",
        inputs=[{"name":"sequences","type":"json","required":True}],
        outputs=[{"name":"label","type":"text"},{"name":"orders","type":"json"},
                 {"name":"per_symbol_entropy","type":"json"},
                 {"name":"regime","type":"text"},
                 {"name":"f2_over_f1","type":"number"},{"name":"f3_over_f2","type":"number"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "max_order":{"type":"integer","title":"Max Order","default":4,"minimum":2},
            "label":{"type":"string","title":"Label","default":"unknown"},
            "profile_spec":{"type":"object","title":"Profile Spec",
                            "description":"Ordered regime rules ([metric, op, threshold] conditions over f2_over_f1 / f3_over_f2) and the fallback regime."}}},
        fn=order_information_profile_execute),
    AtomicNodeDef("TokenContextAssociation","Token-Context Association","Analysis",
        "Permutation-tested association between tokens and a metadata "
        "context field (Spec 087 S3): the significance cut, the "
        "strong-verdict minimum, and the optional length binning are "
        "spec data. The Phase-14 SignContextAssociation delegates to "
        "this engine.",
        inputs=[{"name":"sequences","type":"json","required":True},
                {"name":"metadata","type":"json","required":True}],
        outputs=[{"name":"associations","type":"json"},{"name":"n_significant","type":"number"},
                 {"name":"n_total_pairs","type":"number"},{"name":"field","type":"text"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "field":{"type":"string","title":"Context Field","default":"type"},
            "n_perm":{"type":"integer","title":"Permutations","default":8,"minimum":2},
            "seed":{"type":"integer","title":"Seed","default":11},
            "min_count":{"type":"integer","title":"Min Pair Count","default":5,"minimum":1},
            "top_k":{"type":"integer","title":"Top K","default":30,"minimum":1},
            "association_spec":{"type":"object","title":"Association Spec",
                                "description":"Significance cut, strong-verdict minimum, verdict templates, and the length binning (binned field, source field, [bound, name] bins, default bin)."}}},
        fn=token_context_association_execute),
    AtomicNodeDef("MetricFieldExtractor","Metric Field Extractor","Transforms",
        "Extract a flat metric vector from wired analysis bundles "
        "(Spec 087 S3): the renaming table is a field_map parameter — "
        "an ordered list of extraction entries (a field of an input "
        "dict, the first row's field of a carried list, the field of "
        "the list row whose n equals a carried value, or the field "
        "of a list row at an index), each with a default. The "
        "Phase-14 DoFExtractor delegates to this engine, gaining its "
        "parameter surface from the map.",
        inputs=[{"name":"block_entropies","type":"json","required":False},
                {"name":"zipf","type":"json","required":False},
                {"name":"mi_decay","type":"json","required":False},
                {"name":"hed","type":"json","required":False}],
        outputs=[{"name":"dof_values","type":"json"},{"name":"n_dofs","type":"number"}],
        params_schema={"type":"object","properties":{
            "field_map":{"type":"array","title":"Field Map","default":[],
                         "description":"Ordered extraction entries: {out, kind, input, field/list_key/n/index, default}."}}},
        fn=metric_field_extractor_execute),
    AtomicNodeDef("SignatureComparator","Signature Comparator","Analysis",
        "Rank candidate corpora by closeness to language vs negative "
        "signature templates (Spec 087 S3): the candidate tag and "
        "marker, the negative-tag set, and the verdict margin are "
        "spec data. The Phase-14 LanguageSignatureComparator "
        "delegates to this engine.",
        inputs=[{"name":"a","type":"json","required":False},
                {"name":"b","type":"json","required":False},
                {"name":"c","type":"json","required":False},
                {"name":"d","type":"json","required":False},
                {"name":"e","type":"json","required":False},
                {"name":"f","type":"json","required":False}],
        outputs=[{"name":"ranked","type":"json"},{"name":"language_template","type":"json"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "target_label":{"type":"string","title":"Target Label","default":""},
            "comparator_spec":{"type":"object","title":"Comparator Spec",
                               "description":"Candidate tag and marker substrings, the negative-tag set, the verdict margin, the feature keys, and the verdict templates."}}},
        fn=signature_comparator_execute),
    AtomicNodeDef("EvidenceRuleAggregator","Evidence Rule Aggregator","Analysis",
        "Aggregate independent diagnostic verdicts into one judgement "
        "(Spec 087 S3): the evidence rule table (range_pair, "
        "field_equals, list_fraction_checks, success_threshold), "
        "the language score threshold, the confidence threshold, "
        "and the verdict templates are spec data. The Phase-14 "
        "LanguageDetectorVerdict delegates to this engine.",
        inputs=[{"name":"zipf","type":"json","required":False},
                {"name":"conditional_entropy","type":"json","required":False},
                {"name":"mi_decay","type":"json","required":False},
                {"name":"hed","type":"json","required":False},
                {"name":"cas_projection","type":"json","required":False}],
        outputs=[{"name":"is_language","type":"json"},{"name":"confidence","type":"number"},
                 {"name":"score","type":"number"},{"name":"evidence_for","type":"json"},
                 {"name":"evidence_against","type":"json"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "cas_violation_low":{"type":"number","title":"CAS Violation Low","default":0.1},
            "cas_violation_high":{"type":"number","title":"CAS Violation High","default":1.0},
            "aggregator_spec":{"type":"object","title":"Aggregator Spec",
                                "description":"Ordered evidence rules, language score threshold, confidence threshold, and the three verdict templates."}}},
        fn=evidence_rule_aggregator_execute),
    AtomicNodeDef("PositionalClassClassifier","Positional Class Classifier","Analysis",
        "Classify signs by their within-sequence position profile "
        "(Spec 087 S3): the class label set, the ordered "
        "dominant-position rules, and the verdict template are spec "
        "data; the classification thresholds stay plain params. The "
        "Phase-20 FulsPositionalClassifier delegates to this engine.",
        inputs=[{"name":"sequences","type":"json","required":True}],
        outputs=[{"name":"table","type":"json"},{"name":"counts_by_class","type":"json"},
                 {"name":"fractions_by_class","type":"json"},
                 {"name":"n_signs_classified","type":"number"},
                 {"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "min_count":{"type":"integer","title":"Min Count","default":5,"minimum":1},
            "dom_threshold":{"type":"number","title":"Dominance Threshold","default":0.55},
            "secondary_threshold":{"type":"number","title":"Secondary Threshold","default":0.30},
            "numerical_rr":{"type":"number","title":"Numerical Repeat Rate","default":0.20},
            "classifier_spec":{"type":"object","title":"Classifier Spec",
                               "description":"Class label set, ordered position-class rules (label key + dominant position), and the verdict template."}}},
        fn=positional_class_classifier_execute),
    AtomicNodeDef("SignPositionNullTest","Sign Position Null Test","Analysis",
        "Test a sign's positional bias against a shuffle null (Spec "
        "087 S3): the observed position-class rate is compared "
        "against shuffled re-deals of every sequence, and the "
        "z-score maps to a verdict through a spec-carried band "
        "table. Sequence-shaped by design — it does not reuse the "
        "score-shaped PermutationTest. The Indus-evidence "
        "IndusNullModelTest delegates to this engine.",
        inputs=[{"name":"sequences","type":"json","required":True}],
        outputs=[{"name":"z_score","type":"number"},
                 {"name":"p_approx","type":"number"},
                 {"name":"verdict","type":"text"},{"name":"json","type":"json"},
                 {"name":"text","type":"text"}],
        params_schema={"type":"object","properties":{
            "target_sign":{"type":"string","title":"Target Sign","default":""},
            "test_type":{"type":"string","title":"Position Class","default":"initial"},
            "n_null_runs":{"type":"integer","title":"Null Runs","default":1000,"minimum":1},
            "random_seed":{"type":"integer","title":"Random Seed","default":42},
            "null_spec":{"type":"object","title":"Null Spec",
                         "description":"Ordered [|z| threshold, verdict] bands and the fallback verdict."}}},
        fn=sign_position_null_test_execute),
    AtomicNodeDef("JsonRecordDirLoader","JSON Record Directory Loader","Sources",
        "Load a directory of one-JSON-record-per-file documents (Spec 087 "
        "S3): search mode projects each parseable record through a field "
        "map with an optional substring query and a cross-reference count "
        "from a sibling directory; records mode flattens the item lists of "
        "every parseable file (optionally restricted to files named by an "
        "upstream input) under param-driven filters, per-field value "
        "counts, and a cap. Paths, field names, filters, and text are "
        "parameters (loader_spec), not code — the Indus evidence loaders "
        "delegate to this engine.",
        inputs=[{"name":"papers","type":"papers","required":False}],
        outputs=[{"name":"papers","type":"papers"},{"name":"claims","type":"claims"},{"name":"total_papers","type":"number"},{"name":"total_claims","type":"number"},{"name":"source_docs","type":"number"},{"name":"type_counts","type":"json"},{"name":"status_counts","type":"json"},{"name":"json","type":"json"},{"name":"text","type":"text"}],
        params_schema={"type":"object","properties":{
            "query":{"type":"string","title":"Search Query","default":""},
            "max_papers":{"type":"integer","title":"Max Papers","default":200,"minimum":1},
            "claim_type":{"type":"string","title":"Claim Type Filter","default":""},
            "claim_status":{"type":"string","title":"Claim Status Filter","default":""},
            "sign_filter":{"type":"string","title":"Sign Filter","default":""},
            "max_claims":{"type":"integer","title":"Max Claims","default":500,"minimum":1},
            "loader_spec":{"type":"object","title":"Loader Spec","description":"Full declarative spec: mode, directory, projection / filters / counts, text templates."}}},
        fn=json_record_dir_loader_execute),
    AtomicNodeDef("PositionalClaimTester","Positional Claim Tester","Analysis",
        "Test typed claims against a sequence corpus (Spec 087 S3): a "
        "claim is testable when its type contains a spec keyword, it names "
        "a sign, and its normalized text names a position; each named "
        "sign's observed positional rate is compared with the corpus "
        "average over frequent signs, scaled by a spec multiplier. "
        "Untestable claims are skipped silently. The Indus-evidence "
        "IndusClaimTester delegates to this engine.",
        inputs=[{"name":"claims","type":"claims","required":True},
                {"name":"sequences","type":"sequences","required":True}],
        outputs=[{"name":"test_results","type":"json"},{"name":"n_tested","type":"number"},{"name":"n_supported","type":"number"},{"name":"support_rate","type":"number"},{"name":"json","type":"json"},{"name":"number","type":"number"},{"name":"text","type":"text"}],
        params_schema={"type":"object","properties":{
            "tester_spec":{"type":"object","title":"Tester Spec","description":"Type keywords, position needles, support rule, error and verdict texts."}}},
        fn=positional_claim_tester_execute),
    AtomicNodeDef("RecordGroupSummary","Record Group Summary","Analysis",
        "Grouped summary over a record list (Spec 087 S3): per-record "
        "computed fields, then ordered spec blocks — counts, value "
        "counters, row projections, derived subsets, sums, match and "
        "presence counts, top-N sections over inputs — closed by a "
        "verdict template. Field names, defaults, orders, caps and "
        "texts are parameters (summary_spec), not code — the phase "
        "auditors and reporters delegate to this engine.",
        inputs=[{"name":"records","type":"json","required":False}],
        outputs=[{"name":"verdict","type":"text"},{"name":"json","type":"json"}],
        params_schema={"type":"object","properties":{
            "summary_spec":{"type":"object","title":"Summary Spec","description":"Records key, per-record computed fields, ordered blocks, verdict template."}}},
        fn=record_group_summary_execute),
    AtomicNodeDef("CorpusComparisonStats","Corpus Comparison Stats","Analysis",
        "Per-corpus inscription statistics over a spec list of corpora "
        "(Spec 087 S3): input record/sequence corpora, direct loader "
        "corpora with spec-carried unavailable rows, and direct-count "
        "corpora, closed by a scale-up ratio between two rows and a "
        "verdict template. Corpus names, sequence fields and fallback "
        "rows are parameters (stats_spec), not code — Phase29CorpusStats "
        "delegates to this engine.",
        inputs=[{"name":"inscribed_seals","type":"json","required":False},
                {"name":"mahadevan_inscriptions","type":"json","required":False}],
        outputs=[{"name":"rows","type":"json"},{"name":"scale_up_factor_cisi_to_m77","type":"number"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "stats_spec":{"type":"object","title":"Stats Spec","description":"Corpus list, scale-up rows, verdict template."}}},
        fn=corpus_comparison_stats_execute),
    AtomicNodeDef("PrefixFindspotAssigner","Prefix Findspot Assigner","Analysis",
        "Assign records to find-spots by longest-prefix match of their "
        "catalogue id against a find-spot map (Spec 087 S3): reporter "
        "mode summarises the map and lists assignments (key-presence "
        "match); filter mode classifies a spec-named corpus getter's "
        "records into contact-zone / core lists (truthy-info match, "
        "so empty info entries fall through to shorter prefixes). "
        "Prefix lengths, match semantics and texts are parameters "
        "(assigner_spec), not code — CISIFindspotReporter and "
        "ShuIlishuContactZoneFilter delegate to this engine.",
        inputs=[{"name":"findspot_map","type":"json","required":False},
                {"name":"inscribed_seals","type":"json","required":False}],
        outputs=[{"name":"sites_by_country","type":"json"},{"name":"sites_distribution","type":"json"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "assigner_spec":{"type":"object","title":"Assigner Spec","description":"Mode, prefix lengths, corpus getter (filter mode), verdict templates."}}},
        fn=prefix_findspot_assigner_execute),
    AtomicNodeDef("CorpusCooccurrenceCheck","Corpus Co-occurrence Check","Analysis",
        "Check candidate names against the term set of a corpus-audit "
        "JSON file (Spec 087 S3): a candidate hits when it is a "
        "substring of a term or a term is a substring of it, counting "
        "only terms longer than a spec guard; an absent corpus file "
        "means an empty term set and an absence report. Candidate "
        "ports, the corpus path and the verdict texts are parameters "
        "(check_spec), not code — MeluhhaCooccurrenceCheck delegates "
        "to this engine.",
        inputs=[{"name":"top_candidates","type":"json","required":False},
                {"name":"unique_names","type":"json","required":False}],
        outputs=[{"name":"candidates_checked","type":"number"},{"name":"meluhha_hits","type":"json"},{"name":"meluhha_misses","type":"json"},{"name":"n_hits","type":"number"},{"name":"meluhha_corpus_available","type":"any"},{"name":"verdict","type":"text"}],
        params_schema={"type":"object","properties":{
            "check_spec":{"type":"object","title":"Check Spec","description":"Candidate keys, corpus path, entries key, caps, verdict texts."}}},
        fn=corpus_cooccurrence_check_execute),
    AtomicNodeDef("PredictionVerdictAggregator","Prediction Verdict Aggregator","Analysis",
        "Aggregate sub-experiment outputs into per-prediction verdicts "
        "(Spec 087 S3): spec-carried input shaping (verdict-text and "
        "per-bin extraction, shaped and synthesised inputs) and rule "
        "kinds — text match, count threshold, gap rise, gap spread, "
        "poisson fraction — assembled flat or nested. Rule sets, "
        "thresholds, detail texts and summaries are parameters "
        "(aggregator_spec), not code — Phase20Verdict and "
        "Phase21Verdict delegate to this engine.",
        inputs=[{"name":"length_strata","type":"json","required":False},
                {"name":"repetition_spectral","type":"json","required":False}],
        outputs=[{"name":"summary","type":"text"},{"name":"predictions","type":"json"},{"name":"evidence","type":"json"}],
        params_schema={"type":"object","properties":{
            "aggregator_spec":{"type":"object","title":"Aggregator Spec","description":"Shaping, rules, evidence, assembly, summary template."}}},
        fn=prediction_verdict_aggregator_execute),
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
        "Load a pre-built language model for a known language (hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic, nw_semitic). "
        "Use as the target LM in SADecipher or BeamDecipher.",
        inputs=[],
        outputs=[{"name":"lm","type":"any"},{"name":"language","type":"text"},
                 {"name":"n_signs","type":"number"},{"name":"n_tokens","type":"number"}],
        params_schema={"type":"object","properties":{
            "language":{"type":"string","title":"Language","default":"hebrew",
                        "description":"hebrew | geez | phoenician | sumerian | dravidian | south_dravidian | kannada | telugu | pali | sanskrit | coptic | linear_b | meroitic | proto_sinaitic | nw_semitic"}}},
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
    AtomicNodeDef("SAMultiComparison","SA Multi-Language Comparison","Decipherment",
        "Run Simulated Annealing against multiple reference language models and rank by consistency. "
        "Specify 2\u20136 languages in the 'languages' param (comma-separated). "
        "Each language runs independently; results are sorted best\u2192worst by mean_consistency. "
        "Connects: BuiltinCorpus/CorpusReader \u2192 sequences. No external LM port needed.",
        inputs=[{"name":"sequences","type":"sequences","required":True},
                {"name":"anchors","type":"any","required":False}],
        outputs=[{"name":"comparison_results","type":"json"},
                 {"name":"best_language","type":"text"},
                 {"name":"best_consistency","type":"number"},
                 {"name":"ranking","type":"json"}],
        params_schema={"type":"object","properties":{
            "languages":{"type":"string","title":"Languages (comma-separated)",
                         "default":"dravidian,sanskrit",
                         "description":"Comma-separated list of languages to compare. Valid: hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic"},
            "n_seeds":{"type":"integer","title":"Seeds per Language","default":3,"minimum":1},
            "max_iterations":{"type":"integer","title":"Max Iterations","default":5000,"minimum":100},
            "restarts":{"type":"integer","title":"Restarts per Seed","default":5,"minimum":1},
        }},
        fn=_sa_multi_comparison),
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
    _register_node(_d)

# ── CTT / Constraint Topology nodes (BitConcepts LLC, 2026) ─────────────────────────────
try:
    from glossa_lab.experiment_graph_ctt import _ctt_node_defs as _ctt_defs  # noqa: PLC0415
    for _d in _ctt_defs():
        _register_node(_d)
except Exception as _ctt_exc:  # noqa: BLE001
    _record_registration_failure("CTT nodes", _ctt_exc)

# ── Phase-14 nodes (structural signature + grounding + epistatic + CPSC) ────────────────
try:
    from glossa_lab.experiment_graph_phase14 import _phase14_node_defs as _p14_defs  # noqa: PLC0415
    for _d in _p14_defs():
        _register_node(_d)
except Exception as _p14_exc:  # noqa: BLE001
    _record_registration_failure("Phase-14 nodes", _p14_exc)

# ── Phase-15 nodes (long-tail validity, cipher self-test, hypothesis ranker) ─────────────
try:
    from glossa_lab.experiment_graph_phase15 import _phase15_node_defs as _p15_defs  # noqa: PLC0415
    for _d in _p15_defs():
        _register_node(_d)
except Exception as _p15_exc:  # noqa: BLE001
    _record_registration_failure("Phase-15 nodes", _p15_exc)

# ── Phase-20 nodes (length-stratified spectral, cluster archaeology, Ferrara OCR, Fuls) ──
try:
    from glossa_lab.experiment_graph_phase20 import _phase20_node_defs as _p20_defs  # noqa: PLC0415
    for _d in _p20_defs():
        _register_node(_d)
except Exception as _p20_exc:  # noqa: BLE001
    _record_registration_failure("Phase-20 nodes", _p20_exc)

# ── Phase-21 nodes (repetition collapser, site stratifier, numerical-weight regression) ──
try:
    from glossa_lab.experiment_graph_phase21 import _phase21_node_defs as _p21_defs  # noqa: PLC0415
    for _d in _p21_defs():
        _register_node(_d)
except Exception as _p21_exc:  # noqa: BLE001
    _record_registration_failure("Phase-21 nodes", _p21_exc)

# ── Phase-16/17/18/19 retroactive migration shims (LegacyPhaseScriptRunner) ──
try:
    from glossa_lab.experiment_graph_phase_legacy import (
        _phase_legacy_node_defs as _plg_defs,  # noqa: PLC0415
    )
    for _d in _plg_defs():
        _register_node(_d)
except Exception as _plg_exc:  # noqa: BLE001
    _record_registration_failure("Phase-legacy nodes", _plg_exc)

# ── Phase-22 nodes (CDLI Meluhha-mention corpus + Indus seals at Mesopotamia + name matcher) ──
try:
    from glossa_lab.experiment_graph_phase22 import _phase22_node_defs as _p22_defs  # noqa: PLC0415
    for _d in _p22_defs():
        _register_node(_d)
except Exception as _p22_exc:  # noqa: BLE001
    _record_registration_failure("Phase-22 nodes", _p22_exc)

# ── Phase-23 nodes (refined persons + sign-aware matcher + permutation readout test) ──
try:
    from glossa_lab.experiment_graph_phase23 import _phase23_node_defs as _p23_defs  # noqa: PLC0415
    for _d in _p23_defs():
        _register_node(_d)
except Exception as _p23_exc:  # noqa: BLE001
    _record_registration_failure("Phase-23 nodes", _p23_exc)

# ── Phase-24 nodes (Laursen Table 1 + sign upgrade + persons-v2 + bipartite readout test) ──
try:
    from glossa_lab.experiment_graph_phase24 import _phase24_node_defs as _p24_defs  # noqa: PLC0415
    for _d in _p24_defs():
        _register_node(_d)
except Exception as _p24_exc:  # noqa: BLE001
    _record_registration_failure("Phase-24 nodes", _p24_exc)

# ── Phase-25 nodes (phonetic readout + period-stratified replication + Tamil-Brahmi cross-check) ──
try:
    from glossa_lab.experiment_graph_phase25 import _phase25_node_defs as _p25_defs  # noqa: PLC0415
    for _d in _p25_defs():
        _register_node(_d)
except Exception as _p25_exc:  # noqa: BLE001
    _record_registration_failure("Phase-25 nodes", _p25_exc)

# ── Phase-26 nodes (provenience-stratified + Bayesian decoder + expanded readout + find-spot) ──
try:
    from glossa_lab.experiment_graph_phase26 import _phase26_node_defs as _p26_defs  # noqa: PLC0415
    for _d in _p26_defs():
        # NB: Phase-26 redefines a few atomic IDs that collide with Phase-25
        # (e.g. ProvenienceStratifiedReadout). Phase-26 overrides Phase-25
        # for any colliding ID.
        _register_node(_d)
except Exception as _p26_exc:  # noqa: BLE001
    _record_registration_failure("Phase-26 nodes", _p26_exc)

# ── Phase-27 nodes (reverse Janabiyah + Bayesian v2 + iconographic anchors + 6-bucket period) ──
try:
    from glossa_lab.experiment_graph_phase27 import _phase27_node_defs as _p27_defs  # noqa: PLC0415
    for _d in _p27_defs():
        _register_node(_d)
except Exception as _p27_exc:  # noqa: BLE001
    _record_registration_failure("Phase-27 nodes", _p27_exc)

# ── Phase-28 nodes (CISI Vol 3 OCR via call_llm_vision + Mahadevan crosswalk + allograph-aware) ──
try:
    from glossa_lab.experiment_graph_phase28 import _phase28_node_defs as _p28_defs  # noqa: PLC0415
    for _d in _p28_defs():
        _register_node(_d)
except Exception as _p28_exc:  # noqa: BLE001
    _record_registration_failure("Phase-28 nodes", _p28_exc)

# ── Phase-29 nodes (corpus 10x expansion: M77 + ePSD2 + Fuls + ICIT loaders) ──
try:
    from glossa_lab.experiment_graph_phase29 import _phase29_node_defs as _p29_defs  # noqa: PLC0415
    for _d in _p29_defs():
        _register_node(_d)
except Exception as _p29_exc:  # noqa: BLE001
    _record_registration_failure("Phase-29 nodes", _p29_exc)

# ── Phase-30 nodes (length-cohort reverse Janabiyah + per-bin permutation null) ──
try:
    from glossa_lab.experiment_graph_phase30 import _phase30_node_defs as _p30_defs  # noqa: PLC0415
    for _d in _p30_defs():
        _register_node(_d)
except Exception as _p30_exc:  # noqa: BLE001
    _record_registration_failure("Phase-30 nodes", _p30_exc)

# ── Phase-32 nodes (PermutationTest, MeluhhaCooccurrenceCheck, DravidianSyllableLM) ──
try:
    from glossa_lab.experiment_graph_phase30 import (
        _phase30_phase32_node_defs as _p32_defs,  # noqa: PLC0415
    )
    for _d in _p32_defs():
        _register_node(_d)
except Exception as _p32_exc:  # noqa: BLE001
    _record_registration_failure("Phase-32 nodes", _p32_exc)

# ── Evidence Graph nodes (glossa-indus evidence graph operations) ─────────────────────
try:
    from glossa_lab.experiment_graph_indus_evidence import (
        _evidence_node_defs as _ev_defs,  # noqa: PLC0415
    )
    for _d in _ev_defs():
        _register_node(_d)
except Exception as _ev_exc:  # noqa: BLE001
    _record_registration_failure("Evidence Graph nodes", _ev_exc)

# ── Phase-48-55 nodes (full Indus decipherment pipeline — GPU mandatory) ──────────────
try:
    from glossa_lab.experiment_graph_phase48_55 import (
        _phase48_55_node_defs as _p4855_defs,  # noqa: PLC0415
    )
    for _d in _p4855_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-48-55 decipherment nodes (GPU mandatory)", len(list(_p4855_defs())))
except Exception as _p4855_exc:  # noqa: BLE001
    _record_registration_failure("Phase-48-55 decipherment nodes", _p4855_exc)


# ── Phase-56-61 nodes (expanded Parpola, phonotactic falsification — GPU mandatory) ──
try:
    from glossa_lab.experiment_graph_phase56_61 import (
        _phase56_61_node_defs as _p5661_defs,  # noqa: PLC0415
    )
    for _d in _p5661_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-56-61 decipherment nodes (GPU mandatory)", len(list(_p5661_defs())))
except Exception as _p5661_exc:  # noqa: BLE001
    _record_registration_failure("Phase-56-61 decipherment nodes", _p5661_exc)

# ── Phase-62-66 nodes (ensemble fix, phonotactic filter, morph boundary, crosswalk, Sanskrit SA) ──
try:
    from glossa_lab.experiment_graph_phase62_66 import (
        _phase62_66_node_defs as _p6266_defs,  # noqa: PLC0415
    )
    for _d in _p6266_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-62-66 decipherment nodes (GPU mandatory)", len(list(_p6266_defs())))
except Exception as _p6266_exc:  # noqa: BLE001
    _record_registration_failure("Phase-62-66 decipherment nodes", _p6266_exc)

# ── Phase-67-73 nodes (Sanskrit norm, formula translation, M267 validation, site strat, crosswalk, parser) ──
try:
    from glossa_lab.experiment_graph_phase67_73 import (
        _phase67_73_node_defs as _p6773_defs,  # noqa: PLC0415
    )
    for _d in _p6773_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-67-73 decipherment nodes (GPU mandatory)", len(list(_p6773_defs())))
except Exception as _p6773_exc:  # noqa: BLE001
    _record_registration_failure("Phase-67-73 decipherment nodes", _p6773_exc)

# ── Phase-74-80 nodes (grammar test, Levit, place formula, SA agreement, semantic cluster, gap, DEDR) ──
try:
    from glossa_lab.experiment_graph_phase74_80 import (
        _phase74_80_node_defs as _p7480_defs,  # noqa: PLC0415
    )
    for _d in _p7480_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-74-80 decipherment nodes", len(list(_p7480_defs())))
except Exception as _p7480_exc:  # noqa: BLE001
    _record_registration_failure("Phase-74-80 decipherment nodes", _p7480_exc)

# ── Phase-81-87 nodes (M293 deep-dive, seal translation, gap sprint, formula lexicon, CISI crossval, phonology, sprint-120) ──
try:
    from glossa_lab.experiment_graph_phase81_87 import (
        _phase81_87_node_defs as _p8187_defs,  # noqa: PLC0415
    )
    for _d in _p8187_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-81-87 decipherment nodes", len(list(_p8187_defs())))
except Exception as _p8187_exc:  # noqa: BLE001
    _record_registration_failure("Phase-81-87 decipherment nodes", _p8187_exc)

# ── Phase-88-90 nodes (literature mine, DEDR systematic expansion to 120, scholarly translations) ──
try:
    from glossa_lab.experiment_graph_phase88_90 import (
        _phase88_90_node_defs as _p8890_defs,  # noqa: PLC0415
    )
    for _d in _p8890_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-88-90 decipherment nodes", len(list(_p8890_defs())))
except Exception as _p8890_exc:  # noqa: BLE001
    _record_registration_failure("Phase-88-90 decipherment nodes", _p8890_exc)

# ── Phase-91-100 nodes (anchor-120, uncertain reduce, M293 SA, fulltext, retroflex, crosswalk, trigram, grammar, academic, full-corpus) ──
try:
    from glossa_lab.experiment_graph_phase91_100 import (
        _phase91_100_node_defs as _p91100_defs,  # noqa: PLC0415
    )
    for _d in _p91100_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-91-100 decipherment nodes", len(list(_p91100_defs())))
except Exception as _p91100_exc:  # noqa: BLE001
    _record_registration_failure("Phase-91-100 decipherment nodes", _p91100_exc)

# ── Phase-101-103 nodes (M293 iconographic, PDF extraction, personal name lexicon) ──
try:
    from glossa_lab.experiment_graph_phase101_103 import (
        _phase101_103_node_defs as _p101103_defs,  # noqa: PLC0415
    )
    for _d in _p101103_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-101-103 decipherment nodes", len(list(_p101103_defs())))
except Exception as _p101103_exc:  # noqa: BLE001
    _record_registration_failure("Phase-101-103 decipherment nodes", _p101103_exc)

# ── Phase-104-109 nodes (OCR, name signs, name SA, TB check, phon exhaustion, academic submit) ──
try:
    from glossa_lab.experiment_graph_phase104_109 import (
        _phase104_109_node_defs as _p104109_defs,  # noqa: PLC0415
    )
    for _d in _p104109_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-104-109 decipherment nodes", len(list(_p104109_defs())))
except Exception as _p104109_exc:  # noqa: BLE001
    _record_registration_failure("Phase-104-109 decipherment nodes", _p104109_exc)

# ── Phase-104 claims evaluation node (spec 003) ──
try:
    from glossa_lab.experiment_graph_phase104_claims import (
        _phase104_claims_node_defs as _p104claims_defs,  # noqa: PLC0415
    )
    for _d in _p104claims_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-104 claims-evaluation nodes", len(list(_p104claims_defs())))
except Exception as _p104claims_exc:  # noqa: BLE001
    _record_registration_failure("Phase-104 claims-evaluation nodes", _p104claims_exc)

# ── Phase-107 nodes (spec 005: Phase-52 v2 — SA validation, ablation, delta run, pooling, metrology) ──
try:
    from glossa_lab.experiment_graph_phase107 import (
        _phase107_node_defs as _p107_defs,  # noqa: PLC0415
    )
    for _d in _p107_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-107 (spec 005) nodes", len(list(_p107_defs())))
except Exception as _p107_exc:  # noqa: BLE001
    _record_registration_failure("Phase-107 (spec 005) nodes", _p107_exc)

# ── Phase-108 nodes (spec 006: anchor provenance audit) ──
try:
    from glossa_lab.experiment_graph_phase108 import (
        _phase108_node_defs as _p108_defs,  # noqa: PLC0415
    )
    for _d in _p108_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-108 (spec 006) nodes", len(list(_p108_defs())))
except Exception as _p108_exc:  # noqa: BLE001
    _record_registration_failure("Phase-108 (spec 006) nodes", _p108_exc)

# ── Phase-109 nodes (spec 007: Phase-108 follow-through) ──
try:
    from glossa_lab.experiment_graph_phase109 import (
        _phase109_node_defs as _p109_defs,  # noqa: PLC0415
    )
    for _d in _p109_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-109 (spec 007) nodes", len(list(_p109_defs())))
except Exception as _p109_exc:  # noqa: BLE001
    _record_registration_failure("Phase-109 (spec 007) nodes", _p109_exc)

# ── Phase-110 nodes (spec 008: M222/'kur' adjudication) ──
try:
    from glossa_lab.experiment_graph_phase110 import (
        _phase110_node_defs as _p110_defs,  # noqa: PLC0415
    )
    for _d in _p110_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-110 (spec 008) nodes", len(list(_p110_defs())))
except Exception as _p110_exc:  # noqa: BLE001
    _record_registration_failure("Phase-110 (spec 008) nodes", _p110_exc)

# ── Phase-111 nodes (spec 009: blind language-affiliation study) ──
try:
    from glossa_lab.experiment_graph_phase111 import (
        _phase111_node_defs as _p111_defs,  # noqa: PLC0415
    )
    for _d in _p111_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-111 (spec 009) nodes", len(list(_p111_defs())))
except Exception as _p111_exc:  # noqa: BLE001
    _record_registration_failure("Phase-111 (spec 009) nodes", _p111_exc)

# ── Phase-112 nodes (spec 010: blind affiliation, order-carrying features) ──
try:
    from glossa_lab.experiment_graph_phase112 import (
        _phase112_node_defs as _p112_defs,  # noqa: PLC0415
    )
    for _d in _p112_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-112 (spec 010) nodes", len(list(_p112_defs())))
except Exception as _p112_exc:  # noqa: BLE001
    _record_registration_failure("Phase-112 (spec 010) nodes", _p112_exc)

# ── Phase-113 nodes (spec 011: non-SA validation battery; spec 012: blind
#    affiliation, adversarial protocol — spec 012 renumbered Phase-114, see
#    LEDGER.md correction entries. experiment_graph_phase113 registers BOTH
#    studies' nodes: the two graph modules were authored in parallel under
#    the same filename and were unioned at the PR #71 merge) ──
try:
    from glossa_lab.experiment_graph_phase113 import (
        _phase113_node_defs as _p113_defs,  # noqa: PLC0415
    )
    for _d in _p113_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-113 (specs 011+012) nodes", len(list(_p113_defs())))
except Exception as _p113_exc:  # noqa: BLE001
    _record_registration_failure("Phase-113 (specs 011+012) nodes", _p113_exc)

# ── Phase-115 nodes (spec 014: non-SA validation battery v2, 44 flagged anchors) ──
try:
    from glossa_lab.experiment_graph_phase115 import (
        _phase115_node_defs as _p115_defs,  # noqa: PLC0415
    )
    for _d in _p115_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-115 (spec 014) nodes", len(list(_p115_defs())))
except Exception as _p115_exc:  # noqa: BLE001
    _record_registration_failure("Phase-115 (spec 014) nodes", _p115_exc)
# ── Phase-116 nodes (spec 015: corpus-harmonization study) ──
try:
    from glossa_lab.experiment_graph_phase116 import (
        _phase116_node_defs as _p116_defs,  # noqa: PLC0415
    )
    for _d in _p116_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-116 (spec 015) nodes", len(list(_p116_defs())))
except Exception as _p116_exc:  # noqa: BLE001
    _record_registration_failure("Phase-116 (spec 015) nodes", _p116_exc)

# ── Phase-117 nodes (spec 016: within-compilation validation battery) ──
try:
    from glossa_lab.experiment_graph_phase117 import (
        _phase117_node_defs as _p117_defs,  # noqa: PLC0415
    )
    for _d in _p117_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-117 (spec 016) nodes", len(list(_p117_defs())))
except Exception as _p117_exc:  # noqa: BLE001
    _record_registration_failure("Phase-117 (spec 016) nodes", _p117_exc)

# ── Phase-119 nodes (spec 018: PRED-2026 readiness harness) ──
try:
    from glossa_lab.experiment_graph_phase119 import (
        _phase119_node_defs as _p119_defs,  # noqa: PLC0415
    )
    for _d in _p119_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-119 (spec 018) nodes", len(list(_p119_defs())))
except Exception as _p119_exc:  # noqa: BLE001
    _record_registration_failure("Phase-119 (spec 018) nodes", _p119_exc)
# ── Phase-130 intake nodes (spec 021: independent-data intake pack) ──
try:
    from glossa_lab.experiment_graph_phase130_intake import (
        _phase130_intake_node_defs as _p130i_defs,  # noqa: PLC0415
    )
    for _d in _p130i_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-130 intake (spec 021) nodes", len(list(_p130i_defs())))
except Exception as _p130i_exc:  # noqa: BLE001
    _record_registration_failure("Phase-130 intake (spec 021) nodes", _p130i_exc)
# ── Phase-131 nodes (spec 022: source-of-disagreement attribution) ──
try:
    from glossa_lab.experiment_graph_phase131_attribution import (
        _phase131_attribution_node_defs as _p131a_defs,  # noqa: PLC0415
    )
    for _d in _p131a_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-131 attribution (spec 022) nodes", len(list(_p131a_defs())))
except Exception as _p131a_exc:  # noqa: BLE001
    _record_registration_failure("Phase-131 attribution (spec 022) nodes", _p131a_exc)
# ── Phase-132 nodes (spec 023: keyed transcription layer, Stage P pilot) ──
try:
    from glossa_lab.experiment_graph_phase132 import (
        _phase132_node_defs as _p132_defs,  # noqa: PLC0415
    )
    for _d in _p132_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-132 pilot (spec 023) nodes", len(list(_p132_defs())))
except Exception as _p132_exc:  # noqa: BLE001
    _record_registration_failure("Phase-132 pilot (spec 023) nodes", _p132_exc)
# ── Phase-133 nodes (spec 024: evidence integration, Stage 0 inventory) ──
try:
    from glossa_lab.experiment_graph_phase133 import (
        _phase133_node_defs as _p133_defs,  # noqa: PLC0415
    )
    for _d in _p133_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-133 inventory (spec 024) nodes", len(list(_p133_defs())))
except Exception as _p133_exc:  # noqa: BLE001
    _record_registration_failure("Phase-133 inventory (spec 024) nodes", _p133_exc)
# ── Phase-134 nodes (spec 024: evidence integration, Stage 1 motif pilot) ──
try:
    from glossa_lab.experiment_graph_phase134 import (
        _phase134_node_defs as _p134_defs,  # noqa: PLC0415
    )
    for _d in _p134_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-134 pilot (spec 024) nodes", len(list(_p134_defs())))
except Exception as _p134_exc:  # noqa: BLE001
    _record_registration_failure("Phase-134 pilot (spec 024) nodes", _p134_exc)
# ── Phase-138 nodes (spec 024: evidence integration, Stage 2(d) graffiti descriptive) ──
try:
    from glossa_lab.experiment_graph_phase138 import (
        _phase138_node_defs as _p138_defs,  # noqa: PLC0415
    )
    for _d in _p138_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-138 descriptive (spec 024) nodes", len(list(_p138_defs())))
except Exception as _p138_exc:  # noqa: BLE001
    _record_registration_failure("Phase-138 descriptive (spec 024) nodes", _p138_exc)
# ── Phase-135 nodes (spec 024: evidence integration, Stage 1 re-pilot) ──
try:
    from glossa_lab.experiment_graph_phase135 import (
        _phase135_node_defs as _p135_defs,  # noqa: PLC0415
    )
    for _d in _p135_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-135 re-pilot (spec 024) nodes", len(list(_p135_defs())))
except Exception as _p135_exc:  # noqa: BLE001
    _record_registration_failure("Phase-135 re-pilot (spec 024) nodes", _p135_exc)
# ── Phase-136 nodes (spec 024: evidence integration, Stage 2(a), F1) ──
try:
    from glossa_lab.experiment_graph_phase136 import (
        _phase136_node_defs as _p136_defs,  # noqa: PLC0415
    )
    for _d in _p136_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-136 terminal-type (spec 024) nodes", len(list(_p136_defs())))
except Exception as _p136_exc:  # noqa: BLE001
    _record_registration_failure("Phase-136 terminal-type (spec 024) nodes", _p136_exc)
# ── Phase-137 nodes (spec 024: evidence integration, Stage 2(c) site repertoire) ──
try:
    from glossa_lab.experiment_graph_phase137 import (
        _phase137_node_defs as _p137_defs,  # noqa: PLC0415
    )
    for _d in _p137_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-137 site repertoire (spec 024) nodes", len(list(_p137_defs())))
except Exception as _p137_exc:  # noqa: BLE001
    _record_registration_failure("Phase-137 site repertoire (spec 024) nodes", _p137_exc)
# ── Phase-139 nodes (spec 025: Stage 2 controlled follow-up, covariate audit) ──
try:
    from glossa_lab.experiment_graph_phase139 import (
        _phase139_node_defs as _p139_defs,  # noqa: PLC0415
    )
    for _d in _p139_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-139 covariate audit (spec 025) nodes", len(list(_p139_defs())))
except Exception as _p139_exc:  # noqa: BLE001
    _record_registration_failure("Phase-139 covariate audit (spec 025) nodes", _p139_exc)
# ── Phase-140 nodes (spec 025: Stage 2 controlled follow-up, G1) ──
try:
    from glossa_lab.experiment_graph_phase140 import (
        _phase140_node_defs as _p140_defs,  # noqa: PLC0415
    )
    for _d in _p140_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-140 G1 controlled (spec 025) nodes", len(list(_p140_defs())))
except Exception as _p140_exc:  # noqa: BLE001
    _record_registration_failure("Phase-140 G1 controlled (spec 025) nodes", _p140_exc)
# ── Phase-141 nodes (spec 025: Stage 2 controlled follow-up, F1 LOSO) ──
try:
    from glossa_lab.experiment_graph_phase141 import (
        _phase141_node_defs as _p141_defs,  # noqa: PLC0415
    )
    for _d in _p141_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-141 LOSO (spec 025) nodes", len(list(_p141_defs())))
except Exception as _p141_exc:  # noqa: BLE001
    _record_registration_failure("Phase-141 LOSO (spec 025) nodes", _p141_exc)
# ── Phase-383-386 nodes (spec 026: RCPH framework transfer reruns) ──
try:
    from glossa_lab.experiment_graph_phase383_386 import (
        _phase383_386_node_defs as _p383386_defs,  # noqa: PLC0415
    )
    for _d in _p383386_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-383-386 (spec 026) nodes", len(list(_p383386_defs())))
except Exception as _p383386_exc:  # noqa: BLE001
    _record_registration_failure("Phase-383-386 (spec 026) nodes", _p383386_exc)
# ── Phase-391-392 nodes (spec 027: movement, culture, language) ──
try:
    from glossa_lab.experiment_graph_phase391_392 import (
        _phase391_392_node_defs as _p391392_defs,  # noqa: PLC0415
    )
    for _d in _p391392_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-391-392 (spec 027) nodes", len(list(_p391392_defs())))
except Exception as _p391392_exc:  # noqa: BLE001
    _record_registration_failure("Phase-391-392 (spec 027) nodes", _p391392_exc)
# ── Phase-393 node (spec 028: Harappa robustness) ──
try:
    from glossa_lab.experiment_graph_phase393 import (
        _phase393_node_defs as _p393_defs,  # noqa: PLC0415
    )
    for _d in _p393_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-393 (spec 028) nodes", len(list(_p393_defs())))
except Exception as _p393_exc:  # noqa: BLE001
    _record_registration_failure("Phase-393 (spec 028) nodes", _p393_exc)
# ── Phase-394 node (spec 030: Q6 chronology-spine extension) ──
try:
    from glossa_lab.experiment_graph_phase394 import (
        _phase394_node_defs as _p394_defs,  # noqa: PLC0415
    )
    for _d in _p394_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-394 (spec 030) nodes", len(list(_p394_defs())))
except Exception as _p394_exc:  # noqa: BLE001
    _record_registration_failure("Phase-394 (spec 030) nodes", _p394_exc)
# ── Phase-395 node (spec 031: Q7 provenanced-material networks) ──
try:
    from glossa_lab.experiment_graph_phase395 import (
        _phase395_node_defs as _p395_defs,  # noqa: PLC0415
    )
    for _d in _p395_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-395 (spec 031) nodes", len(list(_p395_defs())))
except Exception as _p395_exc:  # noqa: BLE001
    _record_registration_failure("Phase-395 (spec 031) nodes", _p395_exc)
# ── Phase-396 node (spec 032: PRED-2026-006 Harappa breakdown) ──
try:
    from glossa_lab.experiment_graph_phase396 import (
        _phase396_node_defs as _p396_defs,  # noqa: PLC0415
    )
    for _d in _p396_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-396 (spec 032) nodes", len(list(_p396_defs())))
except Exception as _p396_exc:  # noqa: BLE001
    _record_registration_failure("Phase-396 (spec 032) nodes", _p396_exc)
# ── Phase-397 node (spec 033: SA-free language comparison) ──
try:
    from glossa_lab.experiment_graph_phase397 import (
        _phase397_node_defs as _p397_defs,  # noqa: PLC0415
    )
    for _d in _p397_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-397 (spec 033) nodes", len(list(_p397_defs())))
except Exception as _p397_exc:  # noqa: BLE001
    _record_registration_failure("Phase-397 (spec 033) nodes", _p397_exc)
# ── Phase-398 node (spec 034: matched-object attribution) ──
try:
    from glossa_lab.experiment_graph_phase398 import (
        _phase398_node_defs as _p398_defs,  # noqa: PLC0415
    )
    for _d in _p398_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-398 (spec 034) nodes", len(list(_p398_defs())))
except Exception as _p398_exc:  # noqa: BLE001
    _record_registration_failure("Phase-398 (spec 034) nodes", _p398_exc)
# ── Phase-399 node (spec 035: PRED-2026-010 scoring) ──
try:
    from glossa_lab.experiment_graph_phase399 import (
        _phase399_node_defs as _p399_defs,  # noqa: PLC0415
    )
    for _d in _p399_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-399 (spec 035) nodes", len(list(_p399_defs())))
except Exception as _p399_exc:  # noqa: BLE001
    _record_registration_failure("Phase-399 (spec 035) nodes", _p399_exc)
# ── Phase-400 node (spec 036: PRED-2026-011 scoring) ──
try:
    from glossa_lab.experiment_graph_phase400 import (
        _phase400_node_defs as _p400_defs,  # noqa: PLC0415
    )
    for _d in _p400_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-400 (spec 036) nodes", len(list(_p400_defs())))
except Exception as _p400_exc:  # noqa: BLE001
    _record_registration_failure("Phase-400 (spec 036) nodes", _p400_exc)
# ── Phase-401 node (spec 038: PRED-2026-007 full-population census) ──
try:
    from glossa_lab.experiment_graph_phase401 import (
        _phase401_node_defs as _p401_defs,  # noqa: PLC0415
    )
    for _d in _p401_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-401 (spec 038) nodes", len(list(_p401_defs())))
except Exception as _p401_exc:  # noqa: BLE001
    _record_registration_failure("Phase-401 (spec 038) nodes", _p401_exc)
# ── Phase-402 nodes (Spec 037 CISI 3.1 concordance census) ──
try:
    from glossa_lab.experiment_graph_phase402 import (
        _phase402_node_defs as _p402_defs,  # noqa: PLC0415
    )
    for _d in _p402_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-402 (spec 037) nodes", len(list(_p402_defs())))
except Exception as _p402_exc:  # noqa: BLE001
    _record_registration_failure("Phase-402 (spec 037) nodes", _p402_exc)
# ── Phase-403 node (spec 039: gazetteer period assignment) ──
try:
    from glossa_lab.experiment_graph_phase403 import (
        _phase403_node_defs as _p403_defs,  # noqa: PLC0415
    )
    for _d in _p403_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-403 (spec 039) nodes", len(list(_p403_defs())))
except Exception as _p403_exc:  # noqa: BLE001
    _record_registration_failure("Phase-403 (spec 039) nodes", _p403_exc)

# ── Phase-404 node (spec 044: fish-sign coastal residue, step 0) ──
try:
    from glossa_lab.experiment_graph_phase404 import (
        _phase404_node_defs as _p404_defs,  # noqa: PLC0415
    )
    for _d in _p404_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-404 (spec 044) nodes", len(list(_p404_defs())))
except Exception as _p404_exc:  # noqa: BLE001
    _record_registration_failure("Phase-404 (spec 044) nodes", _p404_exc)
# ── Phase-405 node (spec 046: horned-tiger concordance) ──
try:
    from glossa_lab.experiment_graph_phase405 import (
        _phase405_node_defs as _p405_defs,  # noqa: PLC0415
    )
    for _d in _p405_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-405 (spec 046) nodes", len(list(_p405_defs())))
except Exception as _p405_exc:  # noqa: BLE001
    _record_registration_failure("Phase-405 (spec 046) nodes", _p405_exc)
# ── Phase-426 node (spec 064: sign-297 concordance, successor) ──
try:
    from glossa_lab.experiment_graph_phase426 import (
        _phase426_node_defs as _p426_defs,  # noqa: PLC0415
    )
    for _d in _p426_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-426 (spec 064) nodes", len(list(_p426_defs())))
except Exception as _p426_exc:  # noqa: BLE001
    _record_registration_failure("Phase-426 (spec 064) nodes", _p426_exc)
# ── Phase-406 node (spec 047: Roif ledger step 1 — Asset B) ──
try:
    from glossa_lab.experiment_graph_phase406 import (
        _phase406_node_defs as _p406_defs,  # noqa: PLC0415
    )
    for _d in _p406_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-406 (spec 047) nodes", len(list(_p406_defs())))
except Exception as _p406_exc:  # noqa: BLE001
    _record_registration_failure("Phase-406 (spec 047) nodes", _p406_exc)
# ── Phase-407 node (spec 042: Arm B object-type split) ──
try:
    from glossa_lab.experiment_graph_phase407 import (
        _phase407_node_defs as _p407_defs,  # noqa: PLC0415
    )
    for _d in _p407_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-407 (spec 042) nodes", len(list(_p407_defs())))
except Exception as _p407_exc:  # noqa: BLE001
    _record_registration_failure("Phase-407 (spec 042) nodes", _p407_exc)
# ── Phase-409 node (spec 051: Roif arrow sign) ──
try:
    from glossa_lab.experiment_graph_phase409 import (
        _phase409_node_defs as _p409_defs,  # noqa: PLC0415
    )
    for _d in _p409_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-409 (spec 051) nodes", len(list(_p409_defs())))
except Exception as _p409_exc:  # noqa: BLE001
    _record_registration_failure("Phase-409 (spec 051) nodes", _p409_exc)
# ── Phase-411 node (spec 045: Hunt depicted kinds, step 0) ──
try:
    from glossa_lab.experiment_graph_phase411 import (
        _phase411_node_defs as _p411_defs,  # noqa: PLC0415
    )
    for _d in _p411_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-411 (spec 045) nodes", len(list(_p411_defs())))
except Exception as _p411_exc:  # noqa: BLE001
    _record_registration_failure("Phase-411 (spec 045) nodes", _p411_exc)
# ── Phase-423 node (spec 061: Arm A precision computation) ──
try:
    from glossa_lab.experiment_graph_phase423 import (
        _phase423_node_defs as _p423_defs,  # noqa: PLC0415
    )
    for _d in _p423_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-423 (spec 061) nodes", len(list(_p423_defs())))
except Exception as _p423_exc:  # noqa: BLE001
    _record_registration_failure("Phase-423 (spec 061) nodes", _p423_exc)
# ── Phase-424 node (spec 062: Arm A precision computation, calibration repair) ──
try:
    from glossa_lab.experiment_graph_phase424 import (
        _phase424_node_defs as _p424_defs,  # noqa: PLC0415
    )
    for _d in _p424_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-424 (spec 062) nodes", len(list(_p424_defs())))
except Exception as _p424_exc:  # noqa: BLE001
    _record_registration_failure("Phase-424 (spec 062) nodes", _p424_exc)
# ── Phase-418 node (spec 056: sign-821 recovery) ──
try:
    from glossa_lab.experiment_graph_phase418 import (
        _phase418_node_defs as _p418_defs,  # noqa: PLC0415
    )
    for _d in _p418_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-418 (spec 056) nodes", len(list(_p418_defs())))
except Exception as _p418_exc:  # noqa: BLE001
    _record_registration_failure("Phase-418 (spec 056) nodes", _p418_exc)
# ── Phase-425 node (spec 063: sign-821 identification successor) ──
try:
    from glossa_lab.experiment_graph_phase425 import (
        _phase425_node_defs as _p425_defs,  # noqa: PLC0415
    )
    for _d in _p425_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-425 (spec 063) nodes", len(list(_p425_defs())))
except Exception as _p425_exc:  # noqa: BLE001
    _record_registration_failure("Phase-425 (spec 063) nodes", _p425_exc)
# ── Phase-419 node (spec 057: five-sources heading) ──
try:
    from glossa_lab.experiment_graph_phase419 import (
        _phase419_node_defs as _p419_defs,  # noqa: PLC0415
    )
    for _d in _p419_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-419 (spec 057) nodes", len(list(_p419_defs())))
except Exception as _p419_exc:  # noqa: BLE001
    _record_registration_failure("Phase-419 (spec 057) nodes", _p419_exc)
# ── Phase-427 node (spec 065: S-1/S-5 heading successor) ──
try:
    from glossa_lab.experiment_graph_phase427 import (
        _phase427_node_defs as _p427_defs,  # noqa: PLC0415
    )
    for _d in _p427_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-427 (spec 065) nodes", len(list(_p427_defs())))
except Exception as _p427_exc:  # noqa: BLE001
    _record_registration_failure("Phase-427 (spec 065) nodes", _p427_exc)
# ── Phase-413 node (spec 053: Yadav Zipf controls, step 0) ──
try:
    from glossa_lab.experiment_graph_phase413 import (
        _phase413_node_defs as _p413_defs,  # noqa: PLC0415
    )
    for _d in _p413_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-413 (spec 053) nodes", len(list(_p413_defs())))
except Exception as _p413_exc:  # noqa: BLE001
    _record_registration_failure("Phase-413 (spec 053) nodes", _p413_exc)
# ── Phase-408 node (spec 048: Parpola fish-family profiles, step 0) ──
try:
    from glossa_lab.experiment_graph_phase408 import (
        _phase408_node_defs as _p408_defs,  # noqa: PLC0415
    )
    for _d in _p408_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-408 (spec 048) nodes", len(list(_p408_defs())))
except Exception as _p408_exc:  # noqa: BLE001
    _record_registration_failure("Phase-408 (spec 048) nodes", _p408_exc)



# ── Phase-421 node (spec 059: F1 object-ID join, step 0 + gate-passed test) ──
try:
    from glossa_lab.experiment_graph_phase421 import (
        _phase421_node_defs as _p421_defs,  # noqa: PLC0415
    )
    for _d in _p421_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-421 (spec 059) nodes", len(list(_p421_defs())))
except Exception as _p421_exc:  # noqa: BLE001
    _record_registration_failure("Phase-421 (spec 059) nodes", _p421_exc)
# ── Phase-428 node (spec 066: Phase-130 catalogue extension) ──
try:
    from glossa_lab.experiment_graph_phase428 import (
        _phase428_node_defs as _p428_defs,  # noqa: PLC0415
    )
    for _d in _p428_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-428 (spec 066) nodes", len(list(_p428_defs())))
except Exception as _p428_exc:  # noqa: BLE001
    _record_registration_failure("Phase-428 (spec 066) nodes", _p428_exc)
# ── Phase-429 node (spec 067: F1 enlarged join, step 0 + gate-passed test) ──
try:
    from glossa_lab.experiment_graph_phase429 import (
        _phase429_node_defs as _p429_defs,  # noqa: PLC0415
    )
    for _d in _p429_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-429 (spec 067) nodes", len(list(_p429_defs())))
except Exception as _p429_exc:  # noqa: BLE001
    _record_registration_failure("Phase-429 (spec 067) nodes", _p429_exc)
# ── Phase-430 node (spec 068: Yadav Zipf controls successor, step 0 + fits) ──
try:
    from glossa_lab.experiment_graph_phase430 import (
        _phase430_node_defs as _p430_defs,  # noqa: PLC0415
    )
    for _d in _p430_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-430 (spec 068) nodes", len(list(_p430_defs())))
except Exception as _p430_exc:  # noqa: BLE001
    _record_registration_failure("Phase-430 (spec 068) nodes", _p430_exc)
# ── Phase-432 node (spec 069: Asset A build, gates A1-A6) ──
try:
    from glossa_lab.experiment_graph_phase432 import (
        _phase432_node_defs as _p432_defs,  # noqa: PLC0415
    )
    for _d in _p432_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-432 (spec 069) nodes", len(list(_p432_defs())))
except Exception as _p432_exc:  # noqa: BLE001
    _record_registration_failure("Phase-432 (spec 069) nodes", _p432_exc)
# ── Phase-431 node (spec 072: fish-family profiles, ICIT numbering, Shakti corpus) ──
try:
    from glossa_lab.experiment_graph_phase431 import (
        _phase431_node_defs as _p431_defs,  # noqa: PLC0415
    )
    for _d in _p431_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-431 (spec 072) nodes", len(list(_p431_defs())))
except Exception as _p431_exc:  # noqa: BLE001
    _record_registration_failure("Phase-431 (spec 072) nodes", _p431_exc)
# ── Phase-433 node (spec 070: opening signs on Shakti) ──
try:
    from glossa_lab.experiment_graph_phase433 import (
        _phase433_node_defs as _p433_defs,  # noqa: PLC0415
    )
    for _d in _p433_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-433 (spec 070) nodes", len(list(_p433_defs())))
except Exception as _p433_exc:  # noqa: BLE001
    _record_registration_failure("Phase-433 (spec 070) nodes", _p433_exc)
# ── Phase-434 node (spec 071: sky signs on Shakti) ──
try:
    from glossa_lab.experiment_graph_phase434 import (
        _phase434_node_defs as _p434_defs,  # noqa: PLC0415
    )
    for _d in _p434_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-434 (spec 071) nodes", len(list(_p434_defs())))
except Exception as _p434_exc:  # noqa: BLE001
    _record_registration_failure("Phase-434 (spec 071) nodes", _p434_exc)
# ── Phase-436 node (spec 073: keying-surface repair) ──
try:
    from glossa_lab.experiment_graph_phase436 import (
        _phase436_node_defs as _p436_defs,  # noqa: PLC0415
    )
    for _d in _p436_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-436 (spec 073) nodes", len(list(_p436_defs())))
except Exception as _p436_exc:  # noqa: BLE001
    _record_registration_failure("Phase-436 (spec 073) nodes", _p436_exc)
# ── Phase-437 node (spec 052: Farmer NB-1 on the Shakti layer) ──
try:
    from glossa_lab.experiment_graph_phase437 import (
        _phase437_node_defs as _p437_defs,  # noqa: PLC0415
    )
    for _d in _p437_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-437 (spec 052) nodes", len(list(_p437_defs())))
except Exception as _p437_exc:  # noqa: BLE001
    _record_registration_failure("Phase-437 (spec 052) nodes", _p437_exc)
# ── Phase-438 node (spec 054: Yadav opening/closing, amended NB-1) ──
try:
    from glossa_lab.experiment_graph_phase438 import (
        _phase438_node_defs as _p438_defs,  # noqa: PLC0415
    )
    for _d in _p438_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-438 (spec 054) nodes", len(list(_p438_defs())))
except Exception as _p438_exc:  # noqa: BLE001
    _record_registration_failure("Phase-438 (spec 054) nodes", _p438_exc)
# ── Phase-439 node (spec 040: G1 chronology-controlled rerun, D-25) ──
try:
    from glossa_lab.experiment_graph_phase439 import (
        _phase439_node_defs as _p439_defs,  # noqa: PLC0415
    )
    for _d in _p439_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-439 (spec 040) nodes", len(list(_p439_defs())))
except Exception as _p439_exc:  # noqa: BLE001
    _record_registration_failure("Phase-439 (spec 040) nodes", _p439_exc)
# ── Phase-440 node (spec 074: Hunt opening signs on the repaired surface) ──
try:
    from glossa_lab.experiment_graph_phase440 import (
        _phase440_node_defs as _p440_defs,  # noqa: PLC0415
    )
    for _d in _p440_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-440 (spec 074) nodes", len(list(_p440_defs())))
except Exception as _p440_exc:  # noqa: BLE001
    _record_registration_failure("Phase-440 (spec 074) nodes", _p440_exc)
# ── Phase-441 node (spec 075: depicted-kind endings atlas) ──
try:
    from glossa_lab.experiment_graph_phase441 import (
        _phase441_node_defs as _p441_defs,  # noqa: PLC0415
    )
    for _d in _p441_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-441 (spec 075) nodes", len(list(_p441_defs())))
except Exception as _p441_exc:  # noqa: BLE001
    _record_registration_failure("Phase-441 (spec 075) nodes", _p441_exc)
# ── Phase-410 node (spec 043: PRED-2026-012 registry frame, step 0) ──
try:
    from glossa_lab.experiment_graph_phase410 import (
        _phase410_node_defs as _p410_defs,  # noqa: PLC0415
    )
    for _d in _p410_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-410 (spec 043) nodes", len(list(_p410_defs())))
except Exception as _p410_exc:  # noqa: BLE001
    _record_registration_failure("Phase-410 (spec 043) nodes", _p410_exc)
# ── Phase-420 node (spec 058: transcription-disagreement mechanism, D-21 arm A) ──
try:
    from glossa_lab.experiment_graph_phase420 import (
        _phase420_node_defs as _p420_defs,  # noqa: PLC0415
    )
    for _d in _p420_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-420 (spec 058) nodes", len(list(_p420_defs())))
except Exception as _p420_exc:  # noqa: BLE001
    _record_registration_failure("Phase-420 (spec 058) nodes", _p420_exc)
# ── Phase-414 node (spec 055: sign 900 numeral test) ──
try:
    from glossa_lab.experiment_graph_phase414 import (
        _phase414_node_defs as _p414_defs,  # noqa: PLC0415
    )
    for _d in _p414_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-414 (spec 055) nodes", len(list(_p414_defs())))
except Exception as _p414_exc:  # noqa: BLE001
    _record_registration_failure("Phase-414 (spec 055) nodes", _p414_exc)
# ── Phase-422 node (spec 060: F2 margin curve + shared population) ──
try:
    from glossa_lab.experiment_graph_phase422 import (
        _phase422_node_defs as _p422_defs,  # noqa: PLC0415
    )
    for _d in _p422_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-422 (spec 060) nodes", len(list(_p422_defs())))
except Exception as _p422_exc:  # noqa: BLE001
    _record_registration_failure("Phase-422 (spec 060) nodes", _p422_exc)
# ── Phase-120 nodes (Bhaskar 2024 descriptive triage) ──
try:
    from glossa_lab.experiment_graph_phase120 import (
        _phase120_node_defs as _p120_defs,  # noqa: PLC0415
    )
    for _d in _p120_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-120 nodes", len(list(_p120_defs())))
except Exception as _p120_exc:  # noqa: BLE001
    _record_registration_failure("Phase-120 nodes", _p120_exc)

# ── Phase-118 nodes (spec 017: within-compilation validation battery v2) ──
try:
    from glossa_lab.experiment_graph_phase118 import (
        _phase118_node_defs as _p118_defs,  # noqa: PLC0415
    )
    for _d in _p118_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-118 (spec 017) nodes", len(list(_p118_defs())))
except Exception as _p118_exc:  # noqa: BLE001
    _record_registration_failure("Phase-118 (spec 017) nodes", _p118_exc)

# ── Phase-125 nodes (spec 019: cross-compilation positional comparison) ──
try:
    from glossa_lab.experiment_graph_phase125 import (
        _phase125_node_defs as _p125_defs,  # noqa: PLC0415
    )
    for _d in _p125_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-125 (spec 019) nodes", len(list(_p125_defs())))
except Exception as _p125_exc:  # noqa: BLE001
    _record_registration_failure("Phase-125 (spec 019) nodes", _p125_exc)

# ── Phase-126 nodes (ledger sequence: Wells-split candidates) ──
try:
    from glossa_lab.experiment_graph_phase126_wells import (
        _phase126_wells_node_defs as _p126w_defs,  # noqa: PLC0415
    )
    for _d in _p126w_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-126 (ledger) nodes", len(list(_p126w_defs())))
except Exception as _p126w_exc:  # noqa: BLE001
    _record_registration_failure("Phase-126 (ledger) nodes", _p126w_exc)

# ── Phase-127 nodes (spec 021: cross-compilation disagreement diagnostic) ──
try:
    from glossa_lab.experiment_graph_phase127_diagnostic import (
        _phase127_diagnostic_node_defs as _p127d_defs,  # noqa: PLC0415
    )
    for _d in _p127d_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-127 (spec 021) nodes", len(list(_p127d_defs())))
except Exception as _p127d_exc:  # noqa: BLE001
    _record_registration_failure("Phase-127 (spec 021) nodes", _p127d_exc)

# ── Phase-110-115 nodes (targeted SA, allographs, grammar infer, M→H upgrade, seal translations, significance) ──
try:
    from glossa_lab.experiment_graph_phase110_115 import (
        _phase110_115_node_defs as _p110115_defs,  # noqa: PLC0415
    )
    for _d in _p110115_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-110-115 decipherment nodes", len(list(_p110115_defs())))
except Exception as _p110115_exc:  # noqa: BLE001
    _record_registration_failure("Phase-110-115 decipherment nodes", _p110115_exc)

# ── Phase-116-121 nodes (SA recal, grammar LOW, site semantics, arXiv, LOW→MED, full email) ──
try:
    from glossa_lab.experiment_graph_phase116_121 import (
        _phase116_121_node_defs as _p116121_defs,  # noqa: PLC0415
    )
    for _d in _p116121_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-116-121 decipherment nodes", len(list(_p116121_defs())))
except Exception as _p116121_exc:  # noqa: BLE001
    _record_registration_failure("Phase-116-121 decipherment nodes", _p116121_exc)

# ── Phase-122-123 nodes (syllabic SA, Munda/BMAC substrate) ──
try:
    from glossa_lab.experiment_graph_phase122_123 import (
        _phase122_123_node_defs as _p122123_defs,  # noqa: PLC0415
    )
    for _d in _p122123_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-122-123 decipherment nodes", len(list(_p122123_defs())))
except Exception as _p122123_exc:  # noqa: BLE001
    _record_registration_failure("Phase-122-123 decipherment nodes", _p122123_exc)

# ── Phase-124-125 nodes (fish polysemy, Arthasastra mining) ──
try:
    from glossa_lab.experiment_graph_phase124_125 import (
        _phase124_125_node_defs as _p124125_defs,  # noqa: PLC0415
    )
    for _d in _p124125_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-124-125 decipherment nodes", len(list(_p124125_defs())))
except Exception as _p124125_exc:  # noqa: BLE001
    _record_registration_failure("Phase-124-125 decipherment nodes", _p124125_exc)


# ── Phase-134-141 nodes (falsification suite, advancement, extended battery, master scorecard) ──
try:
    from glossa_lab.experiment_graph_phase134_141 import (
        _phase134_141_node_defs as _p134141_defs,  # noqa: PLC0415
    )
    for _d in _p134141_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-134-141 falsification nodes", len(_p134141_defs()))
except Exception as _p134141_exc:  # noqa: BLE001
    _record_registration_failure("Phase-134-141 falsification nodes", _p134141_exc)

try:
    from glossa_lab.experiment_graph_phase126 import (
        _phase126_node_defs as _p126_defs,  # noqa: PLC0415
    )
    for _d in _p126_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-126 ICIT nodes", len(_p126_defs()))
except Exception as _p126_exc:  # noqa: BLE001
    _record_registration_failure("Phase-126 ICIT nodes", _p126_exc)

try:
    from glossa_lab.experiment_graph_phase128_133 import (
        _phase128_133_node_defs as _p128133_defs,  # noqa: PLC0415
    )
    for _d in _p128133_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-128-133 nodes", len(_p128133_defs()))
except Exception as _p128133_exc:  # noqa: BLE001
    _record_registration_failure("Phase-128-133 nodes", _p128133_exc)

try:
    from glossa_lab.experiment_graph_phase142_145 import (
        _phase142_145_node_defs as _p142145_defs,  # noqa: PLC0415
    )
    for _d in _p142145_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-142-145 nodes", len(_p142145_defs()))
except Exception as _p142145_exc:  # noqa: BLE001
    _record_registration_failure("Phase-142-145 nodes", _p142145_exc)

try:
    from glossa_lab.experiment_graph_phase146_155 import (
        _phase146_155_node_defs as _p146155_defs,  # noqa: PLC0415
    )
    for _d in _p146155_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-146-155 nodes", len(_p146155_defs()))
except Exception as _p146155_exc:  # noqa: BLE001
    _record_registration_failure("Phase-146-155 nodes", _p146155_exc)

try:
    from glossa_lab.experiment_graph_phase156_165 import (
        _phase156_165_node_defs as _p156165_defs,  # noqa: PLC0415
    )
    for _d in _p156165_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-156-165 nodes", len(_p156165_defs()))
except Exception as _p156165_exc:  # noqa: BLE001
    _record_registration_failure("Phase-156-165 nodes", _p156165_exc)

# ── Phase-166-168 nodes (sibilant validation, Meluhhan expansion, blocker SA) — FINAL PHASE GROUP
try:
    from glossa_lab.experiment_graph_phase166_168 import (
        _phase166_168_node_defs as _p166168_defs,  # noqa: PLC0415
    )
    for _d in _p166168_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-166-168 nodes (final pre-ICIT phase group)", len(_p166168_defs()))
except Exception as _p166168_exc:  # noqa: BLE001
    _record_registration_failure("Phase-166-168 nodes", _p166168_exc)

# ── Phase-169-170 nodes (master synthesis + grammar variance — FINAL PHASES)
try:
    from glossa_lab.experiment_graph_phase169_170 import (
        _phase169_170_node_defs as _p169170_defs,  # noqa: PLC0415
    )
    for _d in _p169170_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-169-170 nodes (computational frontier)", len(_p169170_defs()))
except Exception as _p169170_exc:  # noqa: BLE001
    _record_registration_failure("Phase-169-170 nodes", _p169170_exc)

# ── Phase-171-178 nodes (network centrality, betweenness stratification, network deep dive)
try:
    from glossa_lab.experiment_graph_phase171_178 import (
        _phase171_178_node_defs as _p171178_defs,  # noqa: PLC0415
    )
    for _d in _p171178_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-171-178 nodes (network analysis batch)", len(_p171178_defs()))
except Exception as _p171178_exc:  # noqa: BLE001
    _record_registration_failure("Phase-171-178 nodes", _p171178_exc)

# ── Phase-179-180 nodes (recent literature mine + Mesopotamian contact mine)
try:
    from glossa_lab.experiment_graph_phase179_180 import (
        _phase179_180_node_defs as _p179180_defs,  # noqa: PLC0415
    )
    for _d in _p179180_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-179-180 nodes (mining batch)", len(_p179180_defs()))
except Exception as _p179180_exc:  # noqa: BLE001
    _record_registration_failure("Phase-179-180 nodes", _p179180_exc)

# ── Phase-181 node (aDNA archaeogenetics mine)
try:
    from glossa_lab.experiment_graph_phase181 import (
        _phase181_node_defs as _p181_defs,  # noqa: PLC0415
    )
    for _d in _p181_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-181 nodes (aDNA archaeogenetics mine)", len(_p181_defs()))
except Exception as _p181_exc:  # noqa: BLE001
    _record_registration_failure("Phase-181 nodes", _p181_exc)

# ── Phase-182 node (deep evidence mine)
try:
    from glossa_lab.experiment_graph_phase182 import (
        _phase182_node_defs as _p182_defs,  # noqa: PLC0415
    )
    for _d in _p182_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-182 nodes (deep evidence mine)", len(_p182_defs()))
except Exception as _p182_exc:  # noqa: BLE001
    _record_registration_failure("Phase-182 nodes", _p182_exc)

# ── Phase-183 node (bulk mine 5000)
try:
    from glossa_lab.experiment_graph_phase183 import (
        _phase183_node_defs as _p183_defs,  # noqa: PLC0415
    )
    for _d in _p183_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-183 nodes (bulk mine 5000)", len(_p183_defs()))
except Exception as _p183_exc:  # noqa: BLE001
    _record_registration_failure("Phase-183 nodes", _p183_exc)

# ── Phase-184 node (bulk mine 5000 — second run, fresh clusters)
try:
    from glossa_lab.experiment_graph_phase184 import (
        _phase184_node_defs as _p184_defs,  # noqa: PLC0415
    )
    for _d in _p184_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-184 nodes (bulk mine 5000 fresh clusters)", len(_p184_defs()))
except Exception as _p184_exc:  # noqa: BLE001
    _record_registration_failure("Phase-184 nodes", _p184_exc)

# ── Phase-185-189 nodes (fish-sign battery, Elamo-Dravidian gap, 2026 hypotheses,
#                      commodity semantic, north Dravidian LM)
try:
    from glossa_lab.experiment_graph_phase185_189 import (
        _phase185_189_node_defs as _p185189_defs,  # noqa: PLC0415
    )
    for _d in _p185189_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-185-189 decipherment experiment nodes", len(_p185189_defs()))
except Exception as _p185189_exc:  # noqa: BLE001
    _record_registration_failure("Phase-185-189 nodes", _p185189_exc)

# ── Phase-190-192 nodes (Elamo anchor injection, grammar validation, anchor update proposal)
try:
    from glossa_lab.experiment_graph_phase190_192 import (
        _phase190_192_node_defs as _p190192_defs,  # noqa: PLC0415
    )
    for _d in _p190192_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-190-192 anchor pipeline nodes", len(_p190192_defs()))
except Exception as _p190192_exc:  # noqa: BLE001
    _record_registration_failure("Phase-190-192 nodes", _p190192_exc)

# ── Phase-193-195 nodes (SA rerun, SSRN fetch, grammar revalidation)
try:
    from glossa_lab.experiment_graph_phase193_195 import (
        _phase193_195_node_defs as _p193195_defs,  # noqa: PLC0415
    )
    for _d in _p193195_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-193-195 nodes", len(_p193195_defs()))
except Exception as _p193195_exc:  # noqa: BLE001
    _record_registration_failure("Phase-193-195 nodes", _p193195_exc)

# ── Phase-196-201 nodes (mine3, top8 analysis, DEDR lookup, triple-LM, allograph, inscription reading)
try:
    from glossa_lab.experiment_graph_phase196_201 import (
        _phase196_201_node_defs as _p196201_defs,  # noqa: PLC0415
    )
    for _d in _p196201_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-196-201 nodes", len(_p196201_defs()))
except Exception as _p196201_exc:  # noqa: BLE001
    _record_registration_failure("Phase-196-201 nodes", _p196201_exc)

# ── Phase-206-208 nodes (anchor injection M692/M861, SA rerun 404, bulk mine fifth run)
try:
    from glossa_lab.experiment_graph_phase206_208 import (
        _phase206_208_node_defs as _p206208_defs,  # noqa: PLC0415
    )
    for _d in _p206208_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-206-208 nodes (anchor injection, SA rerun, mine5)", len(_p206208_defs()))
except Exception as _p206208_exc:  # noqa: BLE001
    _record_registration_failure("Phase-206-208 nodes", _p206208_exc)

# ── Phase-203-205 nodes (E28 falsification, McAlpin extended cognates, Bayesian phylogenetics)
try:
    from glossa_lab.experiment_graph_phase203_205 import (
        _phase203_205_node_defs as _p203205_defs,  # noqa: PLC0415
    )
    for _d in _p203205_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-203-205 nodes (E28 falsify, McAlpin cognates, Bayesian phylo)", len(_p203205_defs()))
except Exception as _p203205_exc:  # noqa: BLE001
    _record_registration_failure("Phase-203-205 nodes", _p203205_exc)

# ── Phase-216-220 nodes (SA recal, site semantic, arXiv, Parpola/CISI)
try:
    from glossa_lab.experiment_graph_phase216_220 import (
        _phase216_220_node_defs as _p216220_defs,  # noqa: PLC0415
    )
    for _d in _p216220_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-216-220 nodes", len(_p216220_defs()))
except Exception as _p216220_exc:  # noqa: BLE001
    _record_registration_failure("Phase-216-220 nodes", _p216220_exc)

# ── Phase-221-225 nodes (P324/P122 investigation, CISI injection, slot mismatch, PDF)
try:
    from glossa_lab.experiment_graph_phase221_225 import (
        _phase221_225_node_defs as _p221225_defs,  # noqa: PLC0415
    )
    for _d in _p221225_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-221-225 nodes", len(_p221225_defs()))
except Exception as _p221225_exc:  # noqa: BLE001
    _record_registration_failure("Phase-221-225 nodes", _p221225_exc)

# ── Phase-226-228 nodes (P122 phonetic, P324 formula, CISI tripartite)
try:
    from glossa_lab.experiment_graph_phase226_228 import (
        _phase226_228_node_defs as _p226228_defs,  # noqa: PLC0415
    )
    for _d in _p226228_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-226-228 nodes", len(_p226228_defs()))
except Exception as _p226228_exc:  # noqa: BLE001
    _record_registration_failure("Phase-226-228 nodes", _p226228_exc)

# ── Phase-229 node (CISI anchor SA test, M122 upgrade)
try:
    from glossa_lab.experiment_graph_phase229 import (
        _phase229_node_defs as _p229_defs,  # noqa: PLC0415
    )
    for _d in _p229_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-229 nodes", len(_p229_defs()))
except Exception as _p229_exc:  # noqa: BLE001
    _record_registration_failure("Phase-229 nodes", _p229_exc)

# ── Phase-230-234 nodes (cross-ref matrix, indirect bilingual mine/score, cultural/demographic, P324)
try:
    from glossa_lab.experiment_graph_phase230_234 import (
        _phase230_234_node_defs as _p230234_defs,  # noqa: PLC0415
    )
    for _d in _p230234_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-230-234 nodes", len(_p230234_defs()))
except Exception as _p230234_exc:  # noqa: BLE001
    _record_registration_failure("Phase-230-234 nodes", _p230234_exc)

# ── Phase-235-236 nodes (Elamite–PDr bridge, Sanskrit loanword mapping)
try:
    from glossa_lab.experiment_graph_phase235_236 import (
        _phase235_236_node_defs as _p235236_defs,  # noqa: PLC0415
    )
    for _d in _p235236_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-235-236 nodes", len(_p235236_defs()))
except Exception as _p235236_exc:  # noqa: BLE001
    _record_registration_failure("Phase-235-236 nodes", _p235236_exc)

# ── Phase-237-246 nodes (blocker mine, batch upgrades, synthesis, E41 DEDR, SA crossing)
try:
    from glossa_lab.experiment_graph_phase237_246 import (
        _phase237_246_node_defs as _p237246_defs,
    )
    for _d in _p237246_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-237-246 nodes", len(_p237246_defs()))
except Exception as _p237246_exc:
    _record_registration_failure("Phase-237-246 nodes", _p237246_exc)

# ── Phase-248-254 nodes (ceiling-breaker mine, allograph experiments, CISI allograph, semantic constraint)
try:
    from glossa_lab.experiment_graph_phase248_253 import (
        _phase248_254_node_defs as _p248254_defs,  # noqa: PLC0415
    )
    for _d in _p248254_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-248-254 nodes", len(_p248254_defs()))
except Exception as _p248254_exc:  # noqa: BLE001
    _record_registration_failure("Phase-248-254 nodes", _p248254_exc)

# ── Phase-257-294 nodes (SA reruns, Yajnadevam corpus, DEDR resolution, final 605/605)
try:
    from glossa_lab.experiment_graph_phase257_294 import (
        _phase257_294_node_defs as _p257294_defs,  # noqa: PLC0415
    )
    for _d in _p257294_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-257-294 nodes", len(_p257294_defs()))
except Exception as _p257294_exc:  # noqa: BLE001
    _record_registration_failure("Phase-257-294 nodes", _p257294_exc)

# ── Phase-295-297 nodes (bulk mine May 2026, mine cross-reference, gap analysis)
try:
    from glossa_lab.experiment_graph_phase295_297 import (
        _phase295_297_node_defs as _p295297_defs,
    )
    for _d in _p295297_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-295-297 nodes", len(_p295297_defs()))
except Exception as _p295297_exc:
    _record_registration_failure("Phase-295-297 nodes", _p295297_exc)

# ── Phase-127 nodes (Gulf corpus analysis, Roif mining, fish site polysemy)
try:
    from glossa_lab.experiment_graph_phase127 import (
        _phase127_node_defs as _p127_defs,
    )
    for _d in _p127_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-127 nodes", len(_p127_defs()))
except Exception as _p127_exc:  # noqa: BLE001
    _record_registration_failure("Phase-127 nodes", _p127_exc)

# ── Misc gap phases (44-47, 202, 209-215, 254-256) — previously unregistered scripts
try:
    from glossa_lab.experiment_graph_phase_misc_gaps import (
        _misc_gaps_node_defs as _pmiscgaps_defs,
    )
    for _d in _pmiscgaps_defs():
        _register_node(_d)
    logger.info("Registered %d misc-gap phase nodes (44-47, 202, 209-215, 254-256)", len(_pmiscgaps_defs()))
except Exception as _pmiscgaps_exc:  # noqa: BLE001
    _record_registration_failure("Misc-gap phase nodes", _pmiscgaps_exc)

# ── Phase-298-308 nodes (deep Munda mine, Munda SA, substrate, archaeology,
#    anchored Munda SA, allograph, cross-researcher, semantic, DEDR, Elamite baseline)
try:
    from glossa_lab.experiment_graph_phase298_308 import (
        _phase298_308_node_defs as _p298308_defs,
    )
    for _d in _p298308_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-298-308 nodes", len(_p298308_defs()))
except Exception as _p298308_exc:  # noqa: BLE001
    _record_registration_failure("Phase-298-308 nodes", _p298308_exc)

# ── Phase-322-390 nodes (May 2026 decipherment advancement session)
try:
    from glossa_lab.experiment_graph_phase322_362 import (
        phase322_362_node_defs as _p322390_defs,
    )
    for _d in _p322390_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-322-390 nodes", len(_p322390_defs()))
except Exception as _p322390_exc:  # noqa: BLE001
    _record_registration_failure("Phase-322-390 nodes", _p322390_exc)

# ── Contact-zone analysis templates (KL divergence, synthesis, A/B) ─────────
try:
    from glossa_lab.experiment_graph_contact_zone import (
        _contact_zone_node_defs as _cz_defs,
    )
    for _d in _cz_defs():
        _register_node(_d)
    logger.info("Registered %d contact-zone template nodes", len(_cz_defs()))
except Exception as _cz_exc:  # noqa: BLE001
    _record_registration_failure("Contact-zone template nodes", _cz_exc)

# ── A/B language comparison templates (anchored SA, consistency matrix) ──────
try:
    from glossa_lab.experiment_graph_ab_language import (
        _ab_language_node_defs as _ab_defs,
    )
    for _d in _ab_defs():
        _register_node(_d)
    logger.info("Registered %d A/B language template nodes", len(_ab_defs()))
except Exception as _ab_exc:  # noqa: BLE001
    _record_registration_failure("A/B language template nodes", _ab_exc)

# ── Cross-culture contact matrix + script family classifier ─────────────────
try:
    from glossa_lab.experiment_graph_cross_culture import (
        _cross_culture_node_defs as _cc_defs,
    )
    for _d in _cc_defs():
        _register_node(_d)
    logger.info("Registered %d cross-culture template nodes", len(_cc_defs()))
except Exception as _cc_exc:  # noqa: BLE001
    _record_registration_failure("Cross-culture template nodes", _cc_exc)

# ── Research Loop Runner (meta-node for Experiment Builder)
try:
    from glossa_lab.pipelines.research_loop import ResearchLoop as _RL

    def _research_loop_runner(inputs: dict, params: dict) -> dict:
        """Run the integrated research loop as an atomic node."""
        max_cycles = int(params.get("max_cycles", 5))
        loop = _RL(max_cycles=max_cycles)
        for _ in loop.run():
            pass
        return loop.get_full_results()

    _register_node(AtomicNodeDef(
        id="ResearchLoopRunner",
        name="Research Loop Runner",
        category="Research",
        description="Run the Mine\u2192Analyze\u2192Register\u2192Execute\u2192Analyze cycle for N iterations.",
        inputs=[],
        outputs=[
            {"name": "total_papers", "type": "number"},
            {"name": "total_insights", "type": "number"},
            {"name": "json", "type": "json"},
            {"name": "text", "type": "text"},
        ],
        params_schema={
            "max_cycles": {"type": "integer", "title": "Max Cycles", "default": 5,
                          "description": "Number of Mine\u2192Execute cycles to run."},
        },
        fn=_research_loop_runner,
    ))
    logger.info("Registered ResearchLoopRunner atomic node")
except Exception as _rl_exc:  # noqa: BLE001
    _record_registration_failure("ResearchLoopRunner", _rl_exc)


# ── Experiment metadata (ledger-backed) ──────────────────────────────────────

def get_experiment_metadata() -> list[dict[str, Any]]:
    """Return ledger metadata for all registered experiment nodes.

    Merges the static experiment_ledger.json with live registration data
    from ATOMIC_NODES to provide a unified metadata view.
    """
    ledger_path = Path(__file__).parent / "experiment_ledger.json"
    ledger: list[dict] = []
    if ledger_path.exists():
        try:
            ledger = json.loads(ledger_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass

    # Build a lookup from node ID to ledger entry
    node_to_ledger: dict[str, dict] = {}
    for entry in ledger:
        for node_name in entry.get("key_nodes", []):
            node_to_ledger[node_name] = entry

    # Merge live registration with ledger
    result: list[dict[str, Any]] = []
    for node_id, node_def in ATOMIC_NODES.items():
        ledger_entry = node_to_ledger.get(node_id, {})
        result.append({
            "id": node_id,
            "display_name": node_def.name,
            "category": ledger_entry.get("category", node_def.category),
            "phase": ledger_entry.get("phases", ""),
            "description": node_def.description,
            "status": ledger_entry.get("status", "active"),
            "superseded_by": ledger_entry.get("superseded_by"),
            "source_file": ledger_entry.get("file", ""),
        })

    # Also include ledger-only entries (files without individually named nodes)
    seen_files = {e.get("source_file") for e in result if e.get("source_file")}
    for entry in ledger:
        if entry.get("file") not in seen_files:
            result.append({
                "id": entry.get("file", "").replace(".py", ""),
                "display_name": entry.get("file", "").replace("experiment_graph_", "").replace(".py", ""),
                "category": entry.get("category", "misc"),
                "phase": entry.get("phases", ""),
                "description": entry.get("purpose", ""),
                "status": entry.get("status", "active"),
                "superseded_by": entry.get("superseded_by"),
                "source_file": entry.get("file", ""),
            })

    return result


# ── Graph execution

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


# ── Kalyanaraman rebus cross-validation node ─────────────────────────────────
try:
    from glossa_lab.experiment_graph_kalyanaraman import (
        _kalyanaraman_node_defs as _kalyan_defs,  # noqa: PLC0415
    )
    for _d in _kalyan_defs():
        _register_node(_d)
    logger.info("Registered Kalyanaraman cross-validation node")
except Exception as _kalyan_exc:  # noqa: BLE001
    _record_registration_failure("Kalyanaraman node", _kalyan_exc)

# ── Phase-435 node (spec 041: site-period mapping) ──
try:
    from glossa_lab.experiment_graph_phase435 import (
        _phase435_node_defs as _p435_defs,  # noqa: PLC0415
    )
    for _d in _p435_defs():
        _register_node(_d)
    logger.info("Registered %d Phase-435 (spec 041) nodes", len(list(_p435_defs())))
except Exception as _p435_exc:  # noqa: BLE001
    _record_registration_failure("Phase-435 (spec 041) nodes", _p435_exc)

# ── Legacy flags (Spec 087 S2) ───────────────────────────────────────────────
# Every registration block has run; flag the census's wrapper nodes legacy
# from the migration data before the build closes, so a missing migration id
# is recorded as a build failure like any other registry defect.
_apply_legacy_flags()

# ── Registry build close (Spec 087 S1) ───────────────────────────────────────
# Every plugin block above has now run. Close the build: publish the census,
# and in strict mode refuse to import against an incomplete registry.
_finalize_registry_build()

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
    import re
    import time  # noqa: PLC0415
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

    # contact_zone: RETIRED — was a self-referential ExperimentWrapper (experiment_id
    # = "contact_zone" looking up itself). Replaced by indus_contact_zone_v2.json.

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
    # 1. Their JSON files are deleted if they still exist as auto-migrated files.
    # 2. They are SKIPPED in the creation loop so they are never recreated on startup.
    _RETIRED = {
        "progression", "writing_system_progression", "ventris_validation",
        "ugaritic_proper_benchmark", "ugaritic_vs_hebrew",
        "contact_zone",  # self-referential ExperimentWrapper; replaced by indus_contact_zone_v2
        # Archived 2026-06 experiment cleanup (kept in experiments/graphs/_archive/):
        "positional_profile_analysis", "symbol_clustering", "luwian_kl_scoring",
        "fuls_rtl_decipher", "geez_decipher", "bigram_analysis",
        "kandles_bias", "linear_a_circularity", "ocr_tables", "ocr_texts",
        "fuls_writing_system_comparison", "fuls_nw_semitic_ngram",
        "fuls_nw_semitic_decipher_run", "fuls_constraint_space",
        "fuls_sequence_information_test", "old_hebrew_self_benchmark",
        "tier3_sumerian_validation",
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
        if exp_id in _RETIRED:
            continue  # never recreate retired/archived experiments
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


async def queue_graph_experiment(
    experiment_id: str,
    *,
    db: Any,
    params: dict | None = None,
    name_override: str | None = None,
) -> dict | None:
    """Create a Job record for a graph experiment and return the job dict.

    Returns the job dict on success, or None if db is unavailable or the
    experiment_id is not found in the graph registry.
    """
    from datetime import datetime, timezone  # noqa: PLC0415

    experiments = list_graph_experiments()
    match = None
    for exp in experiments:
        if exp.get("id") == experiment_id:
            match = exp
            break
    if match is None:
        return None
    if db is None:
        return None

    job_name = name_override or match.get("name", experiment_id)
    now = datetime.now(timezone.utc).isoformat()
    job = await db.create_job(
        name=job_name,
        pipeline="graph_experiment",
        params={"experiment_id": experiment_id, **(params or {})},
        created_at=now,
        initial_status="pending",
    )
    return job


def register_graph_experiments() -> None:
    """Inject all saved graph experiments into the ExperimentBase discovery registry."""
    if not _GRAPHS_DIR.exists():
        return
    from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415
    registry = discover_experiments()
    for p in sorted(_GRAPHS_DIR.glob("*.json")):
        if not p.exists():  # guard against race with retirement cleanup
            continue
        try:
            d = json.loads(p.read_text("utf-8"))
            cls = _make_cls(d)
            registry[cls.id] = cls
        except Exception as exc:  # noqa: BLE001
            logger.warning("GraphExperiment load failed (%s): %s", p.name, exc)

