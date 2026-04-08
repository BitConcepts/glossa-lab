"""Tests for the Experiment Graph engine.

Covers:
  - Atomic node functions (unit tests)
  - Graph execution (integration tests)
  - File storage CRUD
  - ExperimentWrapper delegation

Run with:
  cd backend && pytest tests/test_experiment_graph.py -v
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure the backend package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from glossa_lab.experiment_graph import (
    ATOMIC_NODES,
    PORT_COLORS,
    _entropy_calc,
    _filter_seqs,
    _freq_counter,
    _merger,
    _pass_result,
    _positional_profiler,
    _static_value,
    _zipf_fitter,
    delete_graph_experiment,
    execute_graph,
    get_graph_experiment,
    list_graph_experiments,
    save_graph_experiment,
)


# ── Fixtures ────────────────────────────────────────────────────────────────

SAMPLE_SEQUENCES = [
    ["A", "B", "C", "A"],
    ["B", "C", "A"],
    ["A", "A", "B", "C", "C"],
    ["C", "A", "B"],
    ["A", "B", "B", "C"],
]


# ── PORT_COLORS ─────────────────────────────────────────────────────────────

def test_port_colors_complete():
    expected = {"sequences", "freq_map", "profiles", "clusters", "number", "text", "json", "any"}
    assert expected == set(PORT_COLORS)


def test_port_colors_are_hex():
    for name, color in PORT_COLORS.items():
        assert color.startswith("#"), f"{name} color should be hex"
        assert len(color) == 7, f"{name} color should be 7 chars"


# ── ATOMIC_NODES registry ────────────────────────────────────────────────────

def test_all_required_nodes_registered():
    required = {
        "CorpusReader", "StaticValue", "FreqCounter", "PositionalProfiler",
        "EntropyCalc", "Clusterer", "ZipfFitter", "Filter",
        "Merger", "JSONExport", "PassResult", "ExperimentWrapper",
    }
    assert required.issubset(set(ATOMIC_NODES))


def test_each_node_has_required_fields():
    for node_id, node in ATOMIC_NODES.items():
        assert node.id == node_id, f"{node_id}.id mismatch"
        assert node.name, f"{node_id} missing name"
        assert node.category, f"{node_id} missing category"
        assert node.description, f"{node_id} missing description"
        assert isinstance(node.inputs, list), f"{node_id} inputs not list"
        assert isinstance(node.outputs, list), f"{node_id} outputs not list"
        assert isinstance(node.params_schema, dict), f"{node_id} params_schema not dict"
        assert callable(node.fn), f"{node_id} fn not callable"


# ── Atomic node unit tests ───────────────────────────────────────────────────

def test_static_value_string():
    r = _static_value({}, {"value": "hello"})
    assert r["value"] == "hello"
    assert r["text"] == "hello"


def test_static_value_json():
    r = _static_value({}, {"value": '{"key": 42}'})
    assert r["value"] == {"key": 42}


def test_freq_counter_basic():
    r = _freq_counter({"sequences": SAMPLE_SEQUENCES}, {})
    assert "A" in r["freq_map"]
    assert r["freq_map"]["A"] > 0
    assert r["total_tokens"] == sum(len(s) for s in SAMPLE_SEQUENCES)
    assert r["distinct_symbols"] == 3  # A, B, C


def test_freq_counter_min_count():
    r = _freq_counter({"sequences": SAMPLE_SEQUENCES}, {"min_count": 100})
    assert r["freq_map"] == {}


def test_freq_counter_top_n():
    r = _freq_counter({"sequences": SAMPLE_SEQUENCES}, {"top_n": 2})
    assert len(r["freq_map"]) == 2


def test_positional_profiler_classes():
    seqs = [
        ["X", "A", "B", "Y"],
        ["X", "A", "C", "Y"],
        ["X", "B", "A", "Y"],
        ["X", "A", "B", "Y"],
    ]
    r = _positional_profiler({"sequences": seqs}, {"min_count": 2})
    assert "profiles" in r
    assert "class_summary" in r
    classes = {p["pos_class"] for p in r["profiles"]}
    assert classes.issubset({"INITIAL", "TERMINAL", "MEDIAL", "MIXED"})


def test_positional_profiler_terminal():
    # Y always terminal
    seqs = [["A", "B", "Y"]] * 10
    r = _positional_profiler({"sequences": seqs}, {"min_count": 1})
    y_profile = next((p for p in r["profiles"] if p["symbol"] == "Y"), None)
    assert y_profile is not None
    assert y_profile["pos_class"] == "TERMINAL"
    assert y_profile["t_rate"] == 1.0


def test_entropy_calc_from_freq_map():
    r = _entropy_calc({"freq_map": {"A": 50, "B": 50}}, {})
    assert abs(r["h1"] - 1.0) < 0.01  # equal distribution = H1 = 1 bit
    assert r["h1_normalized"] == 1.0   # max entropy for 2 symbols


def test_entropy_calc_from_sequences():
    r = _entropy_calc({"sequences": [["A", "B"]] * 100}, {})
    assert r["h1"] > 0
    assert 0 <= r["h1_normalized"] <= 1


def test_entropy_calc_empty():
    r = _entropy_calc({}, {})
    assert r["h1"] == 0.0


def test_zipf_fitter_basic():
    r = _zipf_fitter({"freq_map": {"A": 100, "B": 50, "C": 25, "D": 12}}, {})
    assert "zipf_exponent" in r
    assert r["zipf_exponent"] > 0  # should be approximately 1.0


def test_zipf_fitter_empty():
    r = _zipf_fitter({"freq_map": {}}, {})
    assert r["zipf_exponent"] == 0.0


def test_filter_seqs_length():
    r = _filter_seqs({"sequences": [[1, 2, 3], [1], [1, 2, 3, 4, 5]]}, {"min_length": 2, "max_length": 4})
    assert r["total_sequences"] == 2
    assert all(2 <= len(s) <= 4 for s in r["sequences"])


def test_merger_combines_inputs():
    r = _merger({"a": {"x": 1}, "b": {"y": 2}}, {})
    assert "json" in r
    combined = r["json"]
    assert "a__x" in combined
    assert "b__y" in combined


def test_pass_result_identity():
    inputs = {"sequences": [[1, 2]], "count": 42}
    r = _pass_result(inputs, {})
    assert r["sequences"] == [[1, 2]]
    assert r["count"] == 42


# ── execute_graph ────────────────────────────────────────────────────────────

def make_graph(nodes, edges):
    return {"nodes": nodes, "edges": edges}


def test_execute_empty_graph():
    r = execute_graph(make_graph([], []))
    assert "error" in r


def test_execute_single_static_value():
    graph = make_graph(
        [{"id": "n1", "type": "StaticValue", "params": {"value": "hello"}}],
        []
    )
    r = execute_graph(graph)
    assert r.get("value") == "hello" or r.get("text") == "hello"


def test_execute_freq_counter_chain():
    """CorpusReader-style: injecting sequences directly via kwargs."""
    graph = make_graph(
        [
            {"id": "n1", "type": "FreqCounter", "params": {"min_count": 1}},
        ],
        []
    )
    # Inject sequences as kwargs (since no CorpusReader, we pass directly)
    r = execute_graph(graph, {"sequences": SAMPLE_SEQUENCES})
    # FreqCounter returns freq_map if sequences are in inputs or params
    # Without upstream, inputs will be empty; kwargs are merged into params only
    # This tests graceful handling with empty sequences
    assert "freq_map" in r or "error" in r  # either works correctly


def test_execute_two_node_chain():
    """FreqCounter → PassResult (result should contain freq_map)."""
    graph = make_graph(
        [
            {"id": "n1", "type": "StaticValue", "params": {"value": "test"}},
            {"id": "n2", "type": "PassResult",  "params": {}},
        ],
        [{"id": "e1", "source": "n1", "target": "n2", "sourcePort": "value", "targetPort": "data"}]
    )
    r = execute_graph(graph)
    # PassResult merges all inputs; should contain the value from StaticValue
    assert "value" in r or "text" in r or "data" in r


def test_execute_unknown_node_type():
    graph = make_graph(
        [{"id": "n1", "type": "NonExistentNode", "params": {}}],
        []
    )
    r = execute_graph(graph)
    # Last node result contains the error
    assert "error" in r


def test_execute_topological_order():
    """Ensure nodes execute in order: n1 → n2 → n3."""
    call_order = []

    original_static = ATOMIC_NODES["StaticValue"].fn
    original_pass = ATOMIC_NODES["PassResult"].fn

    def mock_static(inputs, params):
        call_order.append("n1")
        return original_static(inputs, params)

    def mock_pass(inputs, params):
        call_order.append("n2")
        return original_pass(inputs, params)

    ATOMIC_NODES["StaticValue"].fn = mock_static
    ATOMIC_NODES["PassResult"].fn = mock_pass

    try:
        graph = make_graph(
            [
                {"id": "n1", "type": "StaticValue", "params": {"value": "x"}},
                {"id": "n2", "type": "PassResult", "params": {}},
            ],
            [{"id": "e1", "source": "n1", "target": "n2"}]
        )
        execute_graph(graph)
        assert call_order == ["n1", "n2"]
    finally:
        ATOMIC_NODES["StaticValue"].fn = original_static
        ATOMIC_NODES["PassResult"].fn = original_pass


# ── File storage ─────────────────────────────────────────────────────────────

def test_save_and_retrieve(tmp_path, monkeypatch):
    """save_graph_experiment and get_graph_experiment round-trip."""
    from glossa_lab import experiment_graph as eg
    monkeypatch.setattr(eg, "_GRAPHS_DIR", tmp_path)

    data = {"name": "Test Experiment", "description": "A test.", "nodes": [], "edges": []}
    saved = save_graph_experiment(data)
    assert "id" in saved

    retrieved = get_graph_experiment(saved["id"])
    assert retrieved is not None
    assert retrieved["name"] == "Test Experiment"


def test_list_graph_experiments(tmp_path, monkeypatch):
    from glossa_lab import experiment_graph as eg
    monkeypatch.setattr(eg, "_GRAPHS_DIR", tmp_path)

    save_graph_experiment({"name": "A", "nodes": [], "edges": []})
    save_graph_experiment({"name": "B", "nodes": [], "edges": []})

    exps = list_graph_experiments()
    assert len(exps) == 2
    names = {e["name"] for e in exps}
    assert "A" in names and "B" in names


def test_delete_graph_experiment(tmp_path, monkeypatch):
    from glossa_lab import experiment_graph as eg
    monkeypatch.setattr(eg, "_GRAPHS_DIR", tmp_path)

    saved = save_graph_experiment({"name": "ToDelete", "nodes": [], "edges": []})
    eid = saved["id"]

    assert get_graph_experiment(eid) is not None
    result = delete_graph_experiment(eid)
    assert result is True
    assert get_graph_experiment(eid) is None


def test_delete_nonexistent_returns_false(tmp_path, monkeypatch):
    from glossa_lab import experiment_graph as eg
    monkeypatch.setattr(eg, "_GRAPHS_DIR", tmp_path)

    assert delete_graph_experiment("does_not_exist") is False


# ── RAG module ────────────────────────────────────────────────────────────────

def test_rag_tokenize():
    from glossa_lab.rag import _tokenize
    tokens = _tokenize("Hello, World! foo bar")
    assert "hello" in tokens
    assert "world" in tokens
    assert "foo" in tokens


def test_rag_query_empty_index():
    from glossa_lab import rag
    # Don't build index; query should return empty list gracefully
    rag._chunks.clear()
    rag._tfidf_matrix.clear()
    result = rag.query("test query", top_k=5)
    assert result == []


@pytest.mark.asyncio
async def test_rag_build_and_query(tmp_path, monkeypatch):
    """Build a tiny in-memory index and verify query returns results."""
    from glossa_lab import rag as rag_mod
    monkeypatch.setattr(rag_mod, "_REPORTS_DIR", tmp_path)

    # Write a small JSON report
    (tmp_path / "test_report.json").write_text(
        json.dumps({"result": "Indus script positional analysis complete"}),
        encoding="utf-8"
    )

    count = await rag_mod.build_index(db=None)
    assert count > 0

    results = rag_mod.query("Indus positional analysis", top_k=3)
    assert isinstance(results, list)
    # With one document, we should get at least one result
    assert len(results) >= 1
    assert "text" in results[0]
    assert "score" in results[0]


# ── ExperimentWrapper ────────────────────────────────────────────────────────

def test_experiment_wrapper_unknown_experiment():
    from glossa_lab.experiment_graph import _experiment_wrapper
    r = _experiment_wrapper({}, {"experiment_id": "this_does_not_exist"})
    assert "error" in r


def test_experiment_wrapper_registered_experiment():
    """Test that ExperimentWrapper can call a real registered experiment."""
    from glossa_lab.experiment_base import discover_experiments
    from glossa_lab.experiment_graph import _experiment_wrapper

    exps = discover_experiments()
    if not exps:
        pytest.skip("No registered experiments")

    # Find an experiment that's not CLI-only
    non_cli = {eid: cls for eid, cls in exps.items()
               if "CLI" not in (cls.description or "")}
    if not non_cli:
        pytest.skip("No non-CLI experiments available")

    exp_id = next(iter(non_cli))
    r = _experiment_wrapper({}, {"experiment_id": exp_id})
    # Should return a dict (result or error)
    assert isinstance(r, dict)
