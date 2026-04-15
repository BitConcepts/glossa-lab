"""Tests for graph experiment system (TEST-GE-001..016).

Graph experiment specs:
  TEST-GE-001  _build_proper_graph_specs() returns all expected experiments.
  TEST-GE-002  All graph specs have required keys: id, name, nodes, edges.
  TEST-GE-003  New ugaritic_sa_decipher spec has correct node types.
  TEST-GE-004  New fuls_rtl_decipher spec includes DirectionNormalizer node.
  TEST-GE-005  New geez_decipher spec includes CorpusSplitter and LMBuilder.
  TEST-GE-006  New kl_comparison spec includes two FreqCounter and KLDivergence.
  TEST-GE-007  New bigram_analysis spec includes two NgramCounter nodes.

Graph execution:
  TEST-GE-008  execute_graph on empty graph returns error.
  TEST-GE-009  execute_graph CorpusReader + EntropyCalc runs without crash.
  TEST-GE-010  execute_graph with unknown node type returns error in result.
  TEST-GE-011  Topological sort handles linear chain.
  TEST-GE-012  Topological sort handles diamond DAG.

ATOMIC_NODES registry:
  TEST-GE-013  All 24 expected nodes are registered.
  TEST-GE-014  Every node has id, name, category, fn defined.
  TEST-GE-015  Every node fn is callable.
  TEST-GE-016  Node categories include Decipherment (new).
"""
from __future__ import annotations

import pytest
from glossa_lab.experiment_graph import (
    ATOMIC_NODES, AtomicNodeDef,
    _build_proper_graph_specs, _topo_sort, execute_graph,
)


# ── Graph spec validation ─────────────────────────────────────────────────────

def test_all_expected_specs_present():
    """TEST-GE-001: _build_proper_graph_specs returns all expected experiments."""
    specs = _build_proper_graph_specs()
    expected = [
        "positional_profile_analysis", "symbol_clustering", "luwian_kl_scoring",
        "contact_zone", "indus_structural_atlas", "kandles_bias",
        "linear_a_circularity", "ocr_tables", "ocr_texts",
        # New specs:
        "ugaritic_sa_decipher", "fuls_rtl_decipher", "geez_decipher",
        "kl_comparison", "bigram_analysis",
    ]
    for exp_id in expected:
        assert exp_id in specs, f"Missing graph spec: {exp_id}"


def test_all_specs_have_required_keys():
    """TEST-GE-002: All graph specs have id, name, nodes, edges."""
    specs = _build_proper_graph_specs()
    for spec_id, spec in specs.items():
        assert "id"    in spec, f"{spec_id} missing 'id'"
        assert "name"  in spec, f"{spec_id} missing 'name'"
        assert "nodes" in spec, f"{spec_id} missing 'nodes'"
        assert "edges" in spec, f"{spec_id} missing 'edges'"
        assert len(spec["nodes"]) >= 1, f"{spec_id} has no nodes"


def _get_atomic_ids(spec: dict) -> set[str]:
    """Extract all atomicId values from a spec's nodes."""
    ids = set()
    for n in spec["nodes"]:
        data = n.get("data", {})
        ids.add(data.get("atomicId", n.get("type", "")))
    return ids


def test_ugaritic_sa_decipher_has_correct_nodes():
    """TEST-GE-003: ugaritic_sa_decipher uses BuiltinCorpus, CorpusSplitter, SADecipher."""
    spec = _build_proper_graph_specs()["ugaritic_sa_decipher"]
    ids  = _get_atomic_ids(spec)
    assert "BuiltinCorpus"   in ids
    assert "CorpusSplitter"  in ids
    assert "LMBuilder"       in ids
    assert "SADecipher"      in ids
    assert "ConsistencyScorer" in ids


def test_fuls_rtl_decipher_has_direction_normalizer():
    """TEST-GE-004: fuls_rtl_decipher includes DirectionNormalizer."""
    spec = _build_proper_graph_specs()["fuls_rtl_decipher"]
    ids  = _get_atomic_ids(spec)
    assert "DirectionNormalizer" in ids
    assert "BuiltinLM"           in ids
    assert "SADecipher"          in ids


def test_geez_decipher_has_splitter_and_lm_builder():
    """TEST-GE-005: geez_decipher includes CorpusSplitter and LMBuilder."""
    spec = _build_proper_graph_specs()["geez_decipher"]
    ids  = _get_atomic_ids(spec)
    assert "BuiltinCorpus"   in ids
    assert "CorpusSplitter"  in ids
    assert "LMBuilder"       in ids
    assert "SADecipher"      in ids


def test_kl_comparison_has_two_freq_counters():
    """TEST-GE-006: kl_comparison uses two FreqCounter and one KLDivergence node."""
    spec  = _build_proper_graph_specs()["kl_comparison"]
    nodes = spec["nodes"]
    freq_count = sum(1 for n in nodes
                     if (n.get("data", {}).get("atomicId") or n.get("type")) == "FreqCounter")
    kl_count   = sum(1 for n in nodes
                     if (n.get("data", {}).get("atomicId") or n.get("type")) == "KLDivergence")
    assert freq_count == 2
    assert kl_count == 1


def test_bigram_analysis_has_two_ngram_nodes():
    """TEST-GE-007: bigram_analysis uses two NgramCounter nodes."""
    spec  = _build_proper_graph_specs()["bigram_analysis"]
    nodes = spec["nodes"]
    ngram_count = sum(1 for n in nodes
                      if (n.get("data", {}).get("atomicId") or n.get("type")) == "NgramCounter")
    assert ngram_count == 2


# ── Graph execution ───────────────────────────────────────────────────────────

def test_execute_graph_empty():
    """TEST-GE-008: execute_graph on empty graph returns error."""
    result = execute_graph({"nodes": [], "edges": []})
    assert "error" in result


def test_execute_graph_entropy_chain():
    """TEST-GE-009: CorpusReader -> EntropyCalc runs without crashing."""
    graph = {
        "nodes": [
            {"id": "n1", "type": "expNode",
             "data": {"atomicId": "FreqCounter", "label": "Freq",
                      "params": {"min_count": 1}}},
            {"id": "n2", "type": "expNode",
             "data": {"atomicId": "EntropyCalc", "label": "Entropy",
                      "params": {}}},
            {"id": "n3", "type": "expNode",
             "data": {"atomicId": "PassResult", "label": "Out",
                      "params": {}}},
        ],
        "edges": [
            {"id": "e1", "source": "n1", "target": "n2",
             "sourcePort": "freq_map", "targetPort": "freq_map"},
            {"id": "e2", "source": "n2", "target": "n3",
             "sourcePort": "h1", "targetPort": "data"},
        ],
    }
    # Pass sequences directly via kwargs (bypasses CorpusReader DB call)
    result = execute_graph(graph, {"sequences": [["a", "b", "a", "c", "b"]]})
    assert isinstance(result, dict)


def test_execute_graph_unknown_node_type():
    """TEST-GE-010: Unknown node type produces error in that node's result."""
    graph = {
        "nodes": [{"id": "n1", "type": "expNode",
                   "data": {"atomicId": "NonExistentNode_XYZ", "params": {}}}],
        "edges": [],
    }
    result = execute_graph(graph)
    # Either a top-level error or the node result has an error
    assert "error" in result or result == {}


# ── Topological sort ─────────────────────────────────────────────────────────

def _node(nid: str) -> dict:
    return {"id": nid}

def _edge(sid: str, tid: str) -> dict:
    return {"source": sid, "target": tid}


def test_topo_sort_linear_chain():
    """TEST-GE-011: Topological sort handles A -> B -> C correctly."""
    nodes = [_node("A"), _node("B"), _node("C")]
    edges = [_edge("A", "B"), _edge("B", "C")]
    order = _topo_sort(nodes, edges)
    ids   = [n["id"] for n in order]
    assert ids.index("A") < ids.index("B") < ids.index("C")


def test_topo_sort_diamond():
    """TEST-GE-012: Diamond DAG: A -> B, A -> C, B -> D, C -> D."""
    nodes = [_node("A"), _node("B"), _node("C"), _node("D")]
    edges = [_edge("A","B"), _edge("A","C"), _edge("B","D"), _edge("C","D")]
    order = _topo_sort(nodes, edges)
    ids   = [n["id"] for n in order]
    assert ids[0] == "A"
    assert ids[-1] == "D"


# ── ATOMIC_NODES registry ─────────────────────────────────────────────────────

def test_all_28_nodes_registered():
    """TEST-GE-013: All 28 expected atomic nodes are in the registry."""
    expected = {
        # Original (13)
        "CorpusReader", "StaticValue", "FreqCounter", "PositionalProfiler",
        "EntropyCalc", "Clusterer", "ZipfFitter", "Filter", "Merger",
        "JSONExport", "PassResult", "Comparator", "ExperimentWrapper",
        # Decipherment nodes (11)
        "LMBuilder", "BuiltinLM", "BuiltinCorpus", "CorpusSplitter",
        "DirectionNormalizer", "SADecipher", "ConsistencyScorer",
        "BenchmarkScorer", "KLDivergence", "NgramCounter", "AnchorGenerator",
        # H15 graph-first primitives (4)
        "WritingSystemClassifier", "BeamDecipher", "ShuffleControl", "ConstraintSweep",
    }
    assert expected == set(ATOMIC_NODES.keys()), (
        f"Registry mismatch. Extra: {set(ATOMIC_NODES.keys()) - expected}. "
        f"Missing: {expected - set(ATOMIC_NODES.keys())}"
    )


def test_every_node_has_required_fields():
    """TEST-GE-014: Every node definition has id, name, category, fn."""
    for nid, node in ATOMIC_NODES.items():
        assert node.id,       f"{nid} missing id"
        assert node.name,     f"{nid} missing name"
        assert node.category, f"{nid} missing category"
        assert node.fn,       f"{nid} missing fn"


def test_every_node_fn_is_callable():
    """TEST-GE-015: Every node's fn is callable."""
    for nid, node in ATOMIC_NODES.items():
        assert callable(node.fn), f"{nid}.fn is not callable"


def test_decipherment_category_exists():
    """TEST-GE-016: The 'Decipherment' category has at least 5 nodes."""
    decipher_nodes = [n for n in ATOMIC_NODES.values() if n.category == "Decipherment"]
    assert len(decipher_nodes) >= 5, (
        f"Expected >= 5 Decipherment nodes, found {len(decipher_nodes)}"
    )
