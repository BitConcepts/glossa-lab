"""Spec 087 Stage S2 — palette curation tests (T201–T203, T205).

Claims covered:
  C087-4  The palette is the registry minus legacy, mechanically: the
          catalog's default response is exactly the registered nodes not
          flagged legacy; the flag set is the census's WRAPPER set plus
          the ids recorded converted in the Stage S3 records, applied
          from the S2 migration data file (extended by recorded acts).
  C087-5  Legacy nodes stay resolvable; nothing stored dangles: every
          stored graph fixture still resolves every atomicId against the
          full registry, and a saved graph naming a legacy type still
          executes it.
  C087-17 The registry changes only by recorded acts: the census pin now
          reads three ways (registered 534 / legacy 387 / palette 147),
          per category, counted from the flags themselves.

S3 amendment (records/stage-s3-conversions.md, conversion contract
item 2): conversion PR-A registered two generic primitives
(JsonCorpusLoader, DatasetRecordLoader) and flagged the six converted
F1 domain loaders legacy in the same act; conversion PR-B registered
nine more generic primitives (the F3/F8 engines) and flagged the nine
converted F3/F8 domain nodes legacy in the same act; conversion PR-C
registered six more generic primitives (the F4/F5 engines) and flagged
the thirteen converted F4/F5 domain nodes legacy in the same act. The wrapper-rule
test below pins the amended identity: flagged == WRAPPER set ∪ {the
S3-converted ids}; the converted ids keep their parameterised defs,
so they no longer have the wrapper shape — the flag now records the
conversion, not the shape.

The migration data file (backend/glossa_lab/spec087_s2_legacy_ids.json)
was generated from the classification of record — the system-coupling
audit census (2026-11-02) Appendix A, whose WRAPPER verdict is the
two-stage rule: a DOMAIN node (census section 4.1) with no input ports
and an empty params schema (section 4.3). The one registered node with
the wrapper *shape* that the census classes GENERIC — ResearchLoopRunner,
a core node — is therefore not a wrapper and stays in the palette; the
rule test below pins that single named exception rather than absorbing
it silently.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from glossa_lab import experiment_graph as eg
from glossa_lab import registry_check

_PIN = json.loads(
    (Path(__file__).parent / "fixtures" / "spec087_registry_census.json").read_text(
        encoding="utf-8"
    )
)

_GRAPHS_DIR = Path(eg.__file__).parent / "experiments" / "graphs"

SHADOW_TRIO = [
    "IndusPhase254SemanticConstraint",
    "IndusPhase255CommodityPhonemes",
    "IndusPhase256LEExtension",
]

# The census's one GENERIC node with the wrapper shape (Appendix A row
# 490: class GENERIC). WRAPPER is a verdict over DOMAIN nodes, so this
# core node is not in the migration set and must stay unflagged.
WRAPPER_SHAPE_EXCEPTION = "ResearchLoopRunner"

# The S3 conversion ids (PR-A family F1; PR-B families F3 + F8;
# PR-C families F4 + F5): converted to delegate to a generic primitive
# and flagged legacy in the same act, per the S3 conversion contract.
# They are the only flagged ids without the wrapper shape. Later S3
# conversion PRs extend this set only by amending the S3 conversions
# record in the same PR.
S3_CONVERTED_FLAGGED = frozenset(
    {
        "M77InscriptionLoader",
        "ContactCorpusLoader",
        "MahadevanInscriptionLoader",
        "EPSD2NamesLoader",
        "ICITCorpusLoader",
        "MathematicaEpigraphicaLoader",
        "CanonicalSignLoader",
        "ClusterMapper",
        "StructuralTemplateAnalyzer",
        "ClusterArchaeology",
        "IndusSignRoleClassifier",
        "DefaultIndusValueRoleMap",
        "IndusAnchorSetSyllable",
        "DerivedAnchorSet",
        "EpistaticAnchorRanker",
        "IconographicAnchorScore",
        "AllographAwareIconographicScore",
        "BlindHeldOutTest",
        "BayesianDecoder",
        "BayesianDecoderV2",
        "EnhancedNameMatcher",
        "EnhancedNameMatcherV2",
        "MeluhhaNameMatcher",
        "BilingualReadoutTest",
        "BilingualReadoutTestV2",
        "PeriodStratifiedReadout",
        "PeriodStratifiedReadout6Bucket",
        "ProvenienceStratifiedReadout",
    }
)


def _flagged() -> set[str]:
    return {node_id for node_id, d in eg.ATOMIC_NODES.items() if d.legacy}


def _params_empty(params_schema: dict) -> bool:
    """The census's counting convention (section 4.3): a schema with no
    properties carries no editable parameters."""
    return not params_schema or not params_schema.get("properties")


# ── T201: the migration set is the census WRAPPER set ────────────────────────


def test_migration_data_matches_flagged_set_counted_both_ways():
    """Flagged set == migration data set, 387 ids each way (359 census
    WRAPPERs + the 28 S3 conversions recorded in the data file:
    6 in PR-A, 9 in PR-B, 13 in PR-C)."""
    migration = eg.load_legacy_migration_ids()
    assert len(migration) == 387
    assert len(set(migration)) == 387  # no duplicates in the data file
    flagged = _flagged()
    assert len(flagged) == 387
    assert flagged == set(migration)
    # Every migration id names a registered node (a missing id is recorded
    # as a build failure at import; this pins the same fact as a test).
    assert set(migration) <= set(eg.ATOMIC_NODES)


def test_flagged_set_matches_the_wrapper_rule():
    """Recompute the wrapper shape live and pin the S3-amended identity:
    flagged == wrapper-shaped set (minus the census's one named GENERIC
    exception) ∪ {the ids recorded converted in the S3 records}."""
    shape = {
        node_id
        for node_id, d in eg.ATOMIC_NODES.items()
        if not d.inputs and _params_empty(d.params_schema)
    }
    flagged = _flagged()
    assert flagged - shape == S3_CONVERTED_FLAGGED
    assert (flagged & shape) == shape - {WRAPPER_SHAPE_EXCEPTION}
    assert shape - flagged == {WRAPPER_SHAPE_EXCEPTION}
    assert not eg.ATOMIC_NODES[WRAPPER_SHAPE_EXCEPTION].legacy


def test_shadow_trio_flagged_legacy_like_every_wrapper():
    """The S1-kept misc_gaps definitions take the flag; S2 edits nothing
    about their definitions (provenance stays in misc_gaps)."""
    for node_id in SHADOW_TRIO:
        node_def = eg.ATOMIC_NODES[node_id]
        assert node_def.legacy
        assert node_def.fn.__module__ == "glossa_lab.experiment_graph_phase_misc_gaps"


# ── T202: catalog filtering, both directions ─────────────────────────────────


def test_catalog_default_response_is_exactly_the_palette(client):
    resp = client.get("/api/v1/experiment-graphs/catalog")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 147
    expected = {node_id for node_id, d in eg.ATOMIC_NODES.items() if not d.legacy}
    assert {entry["id"] for entry in body} == expected
    assert all(entry["legacy"] is False for entry in body)


def test_catalog_include_legacy_returns_the_full_registry(client):
    resp = client.get("/api/v1/experiment-graphs/catalog?include_legacy=true")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 534
    assert {entry["id"] for entry in body} == set(eg.ATOMIC_NODES)
    flagged_entries = {entry["id"] for entry in body if entry["legacy"]}
    assert flagged_entries == _flagged()
    assert len(flagged_entries) == 387


# ── T205: the three-way re-pin ───────────────────────────────────────────────


def test_three_way_census_pin():
    """Registered / legacy / palette counts, per category, from the flags."""
    assert _PIN["registered_total"] == 534
    assert _PIN["legacy_total"] == 387
    assert _PIN["palette_total"] == 147
    report = eg.registry_build_report()
    assert report["registered"] == 534
    assert report["legacy"] == 387
    assert report["palette"] == 147
    legacy_by_category = Counter(
        d.category for d in eg.ATOMIC_NODES.values() if d.legacy
    )
    palette_by_category = Counter(
        d.category for d in eg.ATOMIC_NODES.values() if not d.legacy
    )
    assert dict(legacy_by_category) == _PIN["by_category_legacy"]
    assert dict(palette_by_category) == _PIN["by_category_palette"]
    for category, total in _PIN["by_category"].items():
        assert (
            legacy_by_category.get(category, 0) + palette_by_category.get(category, 0)
            == total
        )


def test_registry_health_reports_the_split(client):
    resp = client.get("/api/v1/experiment-graphs/registry-health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["registered"] == 534
    assert body["legacy"] == 387
    assert body["palette"] == 147


def test_self_check_agrees_on_the_legacy_split():
    check = registry_check.registry_self_check()
    assert check["legacy_total"] == 387
    assert check["palette_total"] == 147
    assert check["legacy_mismatch"] == {
        "flagged_not_in_migration": [],
        "in_migration_not_flagged": [],
    }
    assert check["ok"]


# ── T203: resolution sweep over the stored graphs ────────────────────────────


def test_every_stored_graph_resolves_against_the_full_registry():
    """All 27 stored graph fixtures resolve every atomicId; SubExperiment
    targets resolve to a stored graph or a built-in spec the seeder
    materializes into the graph library."""
    graph_files = sorted(_GRAPHS_DIR.glob("*.json"))
    assert len(graph_files) == 27
    graph_ids = set()
    parsed = {}
    for path in graph_files:
        spec = json.loads(path.read_text(encoding="utf-8"))
        parsed[path.name] = spec
        graph_ids.add(spec["id"])
    builtin_ids = set(eg._build_proper_graph_specs())
    used: set[str] = set()
    for name, spec in parsed.items():
        for node in spec.get("nodes", []):
            atomic_id, params = eg._node_type_and_params(node)
            used.add(atomic_id)
            assert atomic_id in eg.ATOMIC_NODES, f"{name}: {atomic_id} unresolved"
            if atomic_id == "SubExperiment":
                target = params.get("experiment_id")
                assert target in graph_ids or target in builtin_ids, (
                    f"{name}: SubExperiment target {target!r} unresolved"
                )
    # The sweep covers the census's live working set size (36 atomicIds).
    assert len(used) == 36


# ── C087-5 execution leg: a stored-form graph naming a legacy type runs ─────


def test_saved_graph_referencing_a_legacy_type_still_executes():
    """ICITMetadataLoader is legacy (census WRAPPER); a graph built from
    it must still resolve and execute through execute_graph — the flag
    removes the palette offer, never the resolution."""
    legacy_id = "ICITMetadataLoader"
    assert eg.ATOMIC_NODES[legacy_id].legacy
    graph = {
        "id": "spec087_s2_legacy_execution_probe",
        "name": "Spec 087 S2 legacy execution probe",
        "nodes": [
            {
                "id": "loader",
                "type": "expNode",
                "data": {"atomicId": legacy_id, "label": "ICIT", "params": {}},
                "position": {"x": 0, "y": 0},
            }
        ],
        "edges": [],
    }
    result = eg.execute_graph(graph)
    assert "Unknown node type" not in json.dumps(result)
    assert result.get("n_sequences") == 0
    assert "metadata" in result
