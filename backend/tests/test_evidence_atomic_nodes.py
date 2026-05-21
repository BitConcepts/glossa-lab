"""Tests for the Evidence Graph atomic nodes (experiment_graph_indus_evidence.py).

Category: "Evidence Graph"
Nodes under test:
  IndusLiteratureLoader   TEST-EV-001..006
  IndusClaimsLoader       TEST-EV-007..013
  CrossHypothesisMatrix   TEST-EV-014..019
  HiddenHypothesisGen     TEST-EV-020..025
  IndusClaimTester        TEST-EV-026..030
  IndusNullModelTest      TEST-EV-031..034
  IndusIntakeRunner       TEST-EV-035..037
  Registration checks     TEST-EV-038..044
"""
from __future__ import annotations

import pytest

from glossa_lab.experiment_graph import ATOMIC_NODES


def _run(node_id: str, inputs: dict, params: dict) -> dict:
    """Helper: run an atomic node and return its result."""
    assert node_id in ATOMIC_NODES, f"Node '{node_id}' not registered in ATOMIC_NODES"
    return ATOMIC_NODES[node_id].fn(inputs, params)


# ── Registration checks ────────────────────────────────────────────────────────

_EVIDENCE_NODES = [
    "IndusLiteratureLoader",
    "IndusClaimsLoader",
    "CrossHypothesisMatrix",
    "HiddenHypothesisGen",
    "IndusClaimTester",
    "IndusNullModelTest",
    "IndusIntakeRunner",
]


def test_ev038_all_nodes_registered():
    """TEST-EV-038: All 7 Evidence Graph nodes are registered in ATOMIC_NODES."""
    missing = [n for n in _EVIDENCE_NODES if n not in ATOMIC_NODES]
    assert missing == [], f"Missing Evidence Graph nodes: {missing}"


def test_ev039_all_nodes_have_evidence_graph_category():
    """TEST-EV-039: All evidence nodes have category='Evidence Graph'."""
    for nid in _EVIDENCE_NODES:
        assert nid in ATOMIC_NODES, f"Node {nid} not registered"
        assert ATOMIC_NODES[nid].category == "Evidence Graph", (
            f"Node {nid} has category '{ATOMIC_NODES[nid].category}' instead of 'Evidence Graph'"
        )


def test_ev040_all_nodes_have_descriptions():
    """TEST-EV-040: All evidence nodes have non-empty descriptions."""
    for nid in _EVIDENCE_NODES:
        d = ATOMIC_NODES[nid].description
        assert d and len(d) > 10, f"Node {nid} has insufficient description: '{d}'"


def test_ev041_nodes_have_valid_port_types():
    """TEST-EV-041: All evidence node ports use known port types."""
    from glossa_lab.experiment_graph import PORT_COLORS
    for nid in _EVIDENCE_NODES:
        node = ATOMIC_NODES[nid]
        for port in node.inputs + node.outputs:
            assert port["type"] in PORT_COLORS, (
                f"Node {nid} port '{port['name']}' uses unknown type '{port['type']}'"
            )


def test_ev042_claims_port_color_defined():
    """TEST-EV-042: 'claims' port type has a color in PORT_COLORS."""
    from glossa_lab.experiment_graph import PORT_COLORS
    assert "claims" in PORT_COLORS
    assert PORT_COLORS["claims"].startswith("#")


def test_ev043_papers_port_color_defined():
    """TEST-EV-043: 'papers' port type has a color in PORT_COLORS."""
    from glossa_lab.experiment_graph import PORT_COLORS
    assert "papers" in PORT_COLORS
    assert PORT_COLORS["papers"].startswith("#")


def test_ev044_all_nodes_have_params_schema():
    """TEST-EV-044: All evidence nodes have a valid params_schema dict."""
    for nid in _EVIDENCE_NODES:
        schema = ATOMIC_NODES[nid].params_schema
        assert isinstance(schema, dict), f"Node {nid} params_schema is not a dict"
        assert schema.get("type") == "object", f"Node {nid} schema.type != 'object'"


# ── IndusLiteratureLoader ──────────────────────────────────────────────────────

def test_ev001_literature_loader_returns_papers():
    """TEST-EV-001: IndusLiteratureLoader returns papers list."""
    r = _run("IndusLiteratureLoader", {}, {})
    assert "papers" in r
    assert "total_papers" in r
    assert "text" in r
    assert isinstance(r["papers"], list)
    assert isinstance(r["total_papers"], int)
    assert r["total_papers"] >= 0


def test_ev002_literature_loader_total_matches_list():
    """TEST-EV-002: total_papers matches len(papers) when no limit exceeded."""
    r = _run("IndusLiteratureLoader", {}, {"max_papers": 200})
    assert r["total_papers"] == len(r["papers"])


def test_ev003_literature_loader_max_papers_respected():
    """TEST-EV-003: max_papers=1 returns at most 1 paper."""
    r = _run("IndusLiteratureLoader", {}, {"max_papers": 1})
    assert len(r["papers"]) <= 1


def test_ev004_literature_loader_query_filter():
    """TEST-EV-004: Empty query returns all; bogus query returns empty."""
    r_bogus = _run("IndusLiteratureLoader", {}, {"query": "zzz_no_such_paper_xyz"})
    assert r_bogus["papers"] == []
    assert r_bogus["total_papers"] == 0


def test_ev005_literature_loader_paper_keys():
    """TEST-EV-005: Paper records have required keys."""
    r = _run("IndusLiteratureLoader", {}, {})
    if not r["papers"]:
        pytest.skip("No papers registered")
    p = r["papers"][0]
    for k in ("document_id", "title", "authors", "year", "claim_count", "status"):
        assert k in p, f"Missing key '{k}' in paper record"


def test_ev006_literature_loader_text_output():
    """TEST-EV-006: text output is a non-empty string."""
    r = _run("IndusLiteratureLoader", {}, {})
    assert isinstance(r["text"], str)
    assert len(r["text"]) > 0


# ── IndusClaimsLoader ──────────────────────────────────────────────────────────

def test_ev007_claims_loader_returns_claims():
    """TEST-EV-007: IndusClaimsLoader returns claims list."""
    r = _run("IndusClaimsLoader", {}, {})
    assert "claims" in r
    assert "total_claims" in r
    assert "type_counts" in r
    assert "status_counts" in r
    assert isinstance(r["claims"], list)


def test_ev008_claims_loader_total_matches_list():
    """TEST-EV-008: total_claims matches len(claims) when no max exceeded."""
    r = _run("IndusClaimsLoader", {}, {"max_claims": 500})
    assert r["total_claims"] == len(r["claims"])


def test_ev009_claims_loader_type_filter():
    """TEST-EV-009: claim_type filter returns only matching claims."""
    r = _run("IndusClaimsLoader", {}, {"claim_type": "zzz_bogus_type_xyz"})
    assert r["claims"] == []
    assert r["total_claims"] == 0


def test_ev010_claims_loader_status_filter():
    """TEST-EV-010: claim_status filter returns only matching claims."""
    r = _run("IndusClaimsLoader", {}, {"claim_status": "zzz_bogus_status_xyz"})
    assert r["claims"] == []


def test_ev011_claims_loader_max_claims():
    """TEST-EV-011: max_claims=1 returns at most 1 claim."""
    r = _run("IndusClaimsLoader", {}, {"max_claims": 1})
    assert len(r["claims"]) <= 1


def test_ev012_claims_loader_upstream_papers_filter():
    """TEST-EV-012: If upstream papers given, only those doc_ids are searched."""
    fake_papers = [{"document_id": "zzz_nonexistent_doc_xyz"}]
    r = _run("IndusClaimsLoader", {"papers": fake_papers}, {})
    assert r["claims"] == []


def test_ev013_claims_loader_type_counts_are_dict():
    """TEST-EV-013: type_counts is a dict of {str: int}."""
    r = _run("IndusClaimsLoader", {}, {})
    assert isinstance(r["type_counts"], dict)
    for k, v in r["type_counts"].items():
        assert isinstance(k, str)
        assert isinstance(v, int)


# ── CrossHypothesisMatrix ──────────────────────────────────────────────────────

_SAMPLE_CLAIMS = [
    {
        "claim_id": "test_001",
        "source_document_id": "doc_a",
        "claim_type": "sign_value_claim",
        "normalized_claim": "fish sign means meen",
        "claim_status": "partially_supported",
        "signs_involved": ["fish"],
    },
    {
        "claim_id": "test_002",
        "source_document_id": "doc_b",
        "claim_type": "sign_value_claim",
        "normalized_claim": "fish sign means coastal guild",
        "claim_status": "partially_falsified",
        "signs_involved": ["fish"],
    },
    {
        "claim_id": "test_003",
        "source_document_id": "doc_c",
        "claim_type": "sign_position_claim",
        "normalized_claim": "fish sign is initial",
        "claim_status": "untested",
        "signs_involved": [],
    },
]


def test_ev014_cross_matrix_requires_claims():
    """TEST-EV-014: CrossHypothesisMatrix returns error with no claims."""
    r = _run("CrossHypothesisMatrix", {}, {})
    assert "error" in r


def test_ev015_cross_matrix_returns_matrix():
    """TEST-EV-015: CrossHypothesisMatrix returns matrix list."""
    r = _run("CrossHypothesisMatrix", {"claims": _SAMPLE_CLAIMS}, {})
    assert "matrix" in r
    assert isinstance(r["matrix"], list)
    assert len(r["matrix"]) > 0


def test_ev016_cross_matrix_conflict_detection():
    """TEST-EV-016: Fish sign should be a conflict (supported + falsified)."""
    r = _run("CrossHypothesisMatrix", {"claims": _SAMPLE_CLAIMS}, {"group_by": "sign"})
    matrix = r["matrix"]
    fish_row = next((m for m in matrix if m["group"] == "fish"), None)
    assert fish_row is not None, "Expected 'fish' group in matrix"
    assert fish_row["verdict"] == "conflict"
    assert fish_row["n_supported"] >= 1
    assert fish_row["n_falsified"] >= 1


def test_ev017_cross_matrix_n_conflicts():
    """TEST-EV-017: n_conflicts is >= 0 and <= len(matrix)."""
    r = _run("CrossHypothesisMatrix", {"claims": _SAMPLE_CLAIMS}, {})
    assert 0 <= r["n_conflicts"] <= r["n_groups"]


def test_ev018_cross_matrix_group_by_claim_type():
    """TEST-EV-018: group_by='claim_type' groups by claim_type correctly."""
    r = _run("CrossHypothesisMatrix", {"claims": _SAMPLE_CLAIMS}, {"group_by": "claim_type"})
    groups = {m["group"] for m in r["matrix"]}
    assert "sign_value_claim" in groups


def test_ev019_cross_matrix_json_output():
    """TEST-EV-019: json output contains matrix and n_conflicts."""
    r = _run("CrossHypothesisMatrix", {"claims": _SAMPLE_CLAIMS}, {})
    assert "json" in r
    assert "matrix" in r["json"]


# ── HiddenHypothesisGen ───────────────────────────────────────────────────────

_CLAIMS_FOR_HYPO = [
    {
        "claim_id": "h_001",
        "source_document_id": "parpola_paper",
        "claim_type": "sign_value_claim",
        "normalized_claim": "fish sign means meen",
        "claim_status": "partially_supported",
        "signs_involved": ["fish"],
        "proposed_value": "meen (Proto-Dravidian)",
    },
    {
        "claim_id": "h_002",
        "source_document_id": "yadav_paper",
        "claim_type": "sign_position_claim",
        "normalized_claim": "initial signs function as titles",
        "claim_status": "strongly_supported",
        "signs_involved": [],
    },
    {
        "claim_id": "h_003",
        "source_document_id": "hunt_paper",
        "claim_type": "sign_function_claim",
        "normalized_claim": "faunal signs are initial prefixes",
        "claim_status": "partially_supported",
        "signs_involved": ["fish", "unicorn"],
    },
]


def test_ev020_hypo_gen_requires_claims():
    """TEST-EV-020: HiddenHypothesisGen returns error with no claims."""
    r = _run("HiddenHypothesisGen", {}, {})
    assert "error" in r


def test_ev021_hypo_gen_returns_hypotheses():
    """TEST-EV-021: HiddenHypothesisGen returns hypotheses list."""
    r = _run("HiddenHypothesisGen", {"claims": _CLAIMS_FOR_HYPO}, {})
    assert "hypotheses" in r
    assert "total_hypotheses" in r
    assert isinstance(r["hypotheses"], list)
    assert isinstance(r["total_hypotheses"], int)
    assert r["total_hypotheses"] >= 0


def test_ev022_hypo_gen_cross_paper():
    """TEST-EV-022: All generated hypotheses draw from >= 2 papers."""
    r = _run("HiddenHypothesisGen", {"claims": _CLAIMS_FOR_HYPO},
             {"min_sources_per_hypothesis": 2})
    for h in r["hypotheses"]:
        assert h["n_sources"] >= 2, (
            f"Hypothesis {h['hypothesis_id']} has only {h['n_sources']} sources"
        )


def test_ev023_hypo_gen_hypothesis_keys():
    """TEST-EV-023: Hypothesis records have required keys."""
    r = _run("HiddenHypothesisGen", {"claims": _CLAIMS_FOR_HYPO}, {})
    if not r["hypotheses"]:
        pytest.skip("No hypotheses generated from sample claims")
    h = r["hypotheses"][0]
    for k in ("hypothesis_id", "derived_from", "n_sources",
              "hypothesis_text", "testability"):
        assert k in h, f"Missing key '{k}' in hypothesis"


def test_ev024_hypo_gen_testability_values():
    """TEST-EV-024: All hypotheses have valid testability values."""
    r = _run("HiddenHypothesisGen", {"claims": _CLAIMS_FOR_HYPO}, {})
    valid = {"directly_testable", "indirectly_testable"}
    for h in r["hypotheses"]:
        assert h["testability"] in valid, (
            f"Hypothesis {h['hypothesis_id']} has invalid testability '{h['testability']}'"
        )


def test_ev025_hypo_gen_total_matches_list():
    """TEST-EV-025: total_hypotheses matches len(hypotheses)."""
    r = _run("HiddenHypothesisGen", {"claims": _CLAIMS_FOR_HYPO}, {})
    assert r["total_hypotheses"] == len(r["hypotheses"])


# ── IndusClaimTester (real corpus integration) ───────────────────────────────

def test_ev_claim_tester_real_indus_cisi_corpus():
    """TEST-EV-REAL-01: IndusClaimTester against the actual indus_cisi corpus.

    Tests the gap identified in gap analysis: bridge synthetic fixture tests
    to real corpus behaviour. Uses the built-in CISI corpus for positional
    claim testing, which provides genuine Parpola-concordance sequences.
    """
    import pytest  # noqa: PLC0415

    # Load real sequences from the built-in indus_cisi corpus
    try:
        from glossa_lab.data.indus_cisi import get_corpus_inscriptions  # noqa: PLC0415
        real_sequences = get_corpus_inscriptions()
    except Exception:  # noqa: BLE001
        pytest.skip("indus_cisi corpus not available in this environment")

    if len(real_sequences) < 10:
        pytest.skip("indus_cisi corpus too small for meaningful test")

    # Craft a claim using an actual Parpola sign code from the corpus
    # P1 (unicorn seal composite sign) is one of the most common initial signs
    from collections import Counter  # noqa: PLC0415
    flat = [s for seq in real_sequences for s in seq]
    freq = Counter(flat)
    top_signs = [s for s, _ in freq.most_common(10)]

    if not top_signs:
        pytest.skip("No signs found in corpus")

    most_common = top_signs[0]
    test_claim = [
        {
            "claim_id": "real_corpus_test_001",
            "source_document_id": "parpola_test_source",
            "claim_type": "sign_position_claim",
            "normalized_claim": f"{most_common} sign is initial",
            "claim_status": "untested",
            "signs_involved": [most_common],
        }
    ]

    r = _run("IndusClaimTester",
             {"claims": test_claim, "sequences": real_sequences}, {})

    # Core assertions — should run without error on real data
    assert "test_results" in r, f"Missing test_results key. Got: {list(r.keys())}"
    assert "n_tested" in r
    assert "support_rate" in r
    assert 0.0 <= r["support_rate"] <= 1.0

    # The most-common sign in the real corpus should have enough occurrences
    # to register at least one testable result
    assert r["n_tested"] >= 1, (
        f"Expected at least 1 testable result on real corpus sign '{most_common}', "
        f"got {r['n_tested']}. Corpus size: {len(real_sequences)} sequences, "
        f"{len(flat)} tokens."
    )

    # Verify result keys are complete
    if r["test_results"]:
        result = r["test_results"][0]
        for key in ("sign", "predicted_pos", "observed_rate", "corpus_avg_rate",
                     "lift", "test_verdict"):
            assert key in result, f"Missing key '{key}' in real-corpus test result"
        assert result["test_verdict"] in ("supported", "not_supported")


# ── IndusClaimTester (synthetic fixture) ─────────────────────────────────────

# Original synthetic tests below

_TEST_SEQUENCES = [
    ["fish", "jar", "unicorn"], ["fish", "arrow"], ["unicorn", "fish", "jar"],
    ["fish", "cattle", "grid"], ["arrow", "fish"], ["jar", "unicorn", "fish"],
    ["fish", "plough"], ["unicorn", "jar"], ["fish", "boat", "jar"],
    ["arrow", "cattle", "fish"],
]

_POSITIONAL_CLAIMS = [
    {
        "claim_id": "pos_001",
        "source_document_id": "test_doc",
        "claim_type": "sign_position_claim",
        "normalized_claim": "fish sign is initial",
        "claim_status": "untested",
        "signs_involved": ["fish"],
    }
]


def test_ev026_claim_tester_requires_sequences():
    """TEST-EV-026: IndusClaimTester returns error without sequences."""
    r = _run("IndusClaimTester", {"claims": _POSITIONAL_CLAIMS, "sequences": []}, {})
    assert "error" in r


def test_ev027_claim_tester_requires_claims():
    """TEST-EV-027: IndusClaimTester returns error without claims."""
    r = _run("IndusClaimTester", {"claims": [], "sequences": _TEST_SEQUENCES}, {})
    assert "error" in r


def test_ev028_claim_tester_returns_results():
    """TEST-EV-028: IndusClaimTester returns test_results list."""
    r = _run("IndusClaimTester",
             {"claims": _POSITIONAL_CLAIMS, "sequences": _TEST_SEQUENCES}, {})
    assert "test_results" in r
    assert "n_tested" in r
    assert "support_rate" in r
    assert isinstance(r["test_results"], list)
    assert 0.0 <= r["support_rate"] <= 1.0


def test_ev029_claim_tester_result_keys():
    """TEST-EV-029: Each test result has required keys."""
    r = _run("IndusClaimTester",
             {"claims": _POSITIONAL_CLAIMS, "sequences": _TEST_SEQUENCES}, {})
    if not r["test_results"]:
        pytest.skip("No testable claims matched corpus signs")
    result = r["test_results"][0]
    for k in ("sign", "predicted_pos", "observed_rate", "corpus_avg_rate",
              "lift", "test_verdict"):
        assert k in result, f"Missing key '{k}' in test result"


def test_ev030_claim_tester_verdict_values():
    """TEST-EV-030: test_verdict is 'supported' or 'not_supported'."""
    r = _run("IndusClaimTester",
             {"claims": _POSITIONAL_CLAIMS, "sequences": _TEST_SEQUENCES}, {})
    for res in r["test_results"]:
        assert res["test_verdict"] in ("supported", "not_supported"), (
            f"Invalid verdict '{res['test_verdict']}'"
        )


# ── IndusNullModelTest ────────────────────────────────────────────────────────

def test_ev031_null_model_requires_sequences():
    """TEST-EV-031: IndusNullModelTest returns error without sequences."""
    r = _run("IndusNullModelTest", {}, {"target_sign": "fish", "n_null_runs": 10})
    assert "error" in r


def test_ev032_null_model_requires_target_sign():
    """TEST-EV-032: IndusNullModelTest returns error without target_sign."""
    r = _run("IndusNullModelTest",
             {"sequences": _TEST_SEQUENCES}, {"n_null_runs": 10})
    assert "error" in r


def test_ev033_null_model_returns_z_score():
    """TEST-EV-033: IndusNullModelTest returns z_score and verdict."""
    r = _run("IndusNullModelTest",
             {"sequences": _TEST_SEQUENCES},
             {"target_sign": "fish", "n_null_runs": 100,
              "test_type": "initial", "random_seed": 42})
    assert "z_score" in r
    assert "p_approx" in r
    assert "verdict" in r
    assert "observed_rate" in r
    assert isinstance(r["z_score"], float)
    assert 0.0 <= r["p_approx"] <= 1.0


def test_ev034_null_model_verdict_values():
    """TEST-EV-034: verdict is one of the four defined levels."""
    r = _run("IndusNullModelTest",
             {"sequences": _TEST_SEQUENCES},
             {"target_sign": "fish", "n_null_runs": 50,
              "test_type": "initial", "random_seed": 42})
    valid = {"STRONGLY_SIGNIFICANT", "SIGNIFICANT",
             "BORDERLINE", "NOT_SIGNIFICANT"}
    assert r["verdict"] in valid, f"Unknown verdict: {r['verdict']}"


# ── IndusIntakeRunner ──────────────────────────────────────────────────────────

def test_ev035_intake_runner_returns_pipeline_results():
    """TEST-EV-035: IndusIntakeRunner returns pipeline_results list."""
    r = _run("IndusIntakeRunner", {}, {})
    assert "pipeline_results" in r
    assert "all_ok" in r
    assert "text" in r
    assert isinstance(r["pipeline_results"], list)


def test_ev036_intake_runner_result_shape():
    """TEST-EV-036: Each pipeline result has script and status keys."""
    r = _run("IndusIntakeRunner", {}, {})
    for res in r["pipeline_results"]:
        assert "script" in res
        assert "status" in res


def test_ev037_intake_runner_text_is_string():
    """TEST-EV-037: text output is a meaningful string."""
    r = _run("IndusIntakeRunner", {}, {})
    assert isinstance(r["text"], str)
    assert len(r["text"]) > 5
