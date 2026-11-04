"""Spec 087 Stage S1 — registry integrity tests (T101–T105).

Claims covered:
  C087-1  Registry completeness is pinned, and a silent shrink fails CI.
  C087-2  No node id has two live definitions (the three shadowed classes
          of census Table 4 are resolved to the kept misc_gaps definitions).
  C087-16 The Study Builder's schema module no longer impersonates the
          node registry (node_registry.py -> study_node_registry.py; the
          /node-registry/ endpoint answers unchanged).
  C087-17 The registry changes only by recorded acts — the census pin in
          tests/fixtures/spec087_registry_census.json is the act's record.

The pin was generated from the live registry at stage start and matches
the census of record (specs/087-node-system-tightening/records/
census-evidence.md Table 1): 517 registered nodes, 66 categories,
144 plugin modules. Re-pinned by the recorded S3 conversion PR-A act
(records/stage-s3-conversions.md): 519 registered nodes (two new
generic primitives in the core list), 65 categories, core 44.
Re-pinned again by the recorded S3 conversion PR-B act (same record):
528 registered nodes (nine new generic primitives in the core list),
65 categories, core 53. Re-pinned again by the recorded S3 conversion
PR-C act (same record): 534 registered nodes (six new generic
primitives in the core list), 65 categories, core 59. Re-pinned again
by the recorded S3 conversion PR-D act (same record): 537 registered
nodes (three new generic primitives in the core list), 65 categories,
core 62. Re-pinned again by the recorded S3 conversion PR-E act (same
record): 545 registered nodes (eight new generic primitives in the
core list), 65 categories, core 70. Re-pinned again by the recorded
S3 conversion PR-F act (same record): 556 registered nodes (eleven
new generic primitives in the core list), 65 categories, core 81.
"""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg
from glossa_lab import registry_check

_PIN = json.loads(
    (Path(__file__).parent / "fixtures" / "spec087_registry_census.json").read_text(
        encoding="utf-8"
    )
)

SHADOWED_IDS = [
    "IndusPhase254SemanticConstraint",
    "IndusPhase255CommodityPhonemes",
    "IndusPhase256LEExtension",
]


# ── T102: completeness pin ───────────────────────────────────────────────────


def test_plugin_module_list_pinned():
    """The loader imports exactly the pinned 144 plugin modules."""
    expected = ["glossa_lab." + name for name in _PIN["plugin_modules"]]
    assert sorted(registry_check.expected_plugin_modules()) == sorted(expected)
    assert len(registry_check.expected_plugin_modules()) == 144


def test_registry_census_pinned():
    """Registered total and per-category counts match the pin exactly."""
    assert len(eg.ATOMIC_NODES) == _PIN["registered_total"] == 556
    census = Counter(d.category for d in eg.ATOMIC_NODES.values())
    assert dict(census) == _PIN["by_category"]
    assert len(census) == 65


def test_registry_self_check_passes():
    """The from-scratch recomputation agrees with the built registry."""
    check = registry_check.registry_self_check()
    assert check["plugin_module_errors"] == []
    assert check["duplicate_ids"] == []
    assert check["produced_not_registered"] == []
    assert check["core_registered"] == 81
    assert check["ok"]
    registry_check.assert_registry_complete(check)


def test_build_report_ok():
    """The runtime build recorded no failures and no duplicates."""
    report = eg.registry_build_report()
    assert report["ok"]
    assert report["registered"] == 556
    assert report["failures"] == []
    assert report["duplicates"] == []


# ── T101: strict build teeth (C087-1 falsifiers) ─────────────────────────────


def test_broken_plugin_module_fails_the_check(tmp_path, monkeypatch):
    """A plugin module that fails to import is named by the self-check."""
    (tmp_path / "broken_plugin_fixture_087.py").write_text(
        'raise ImportError("seeded break for Spec 087 teeth")\n', encoding="utf-8"
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    imports = registry_check.loader_plugin_imports()
    imports.append(("broken_plugin_fixture_087", ["_broken_node_defs"]))
    _, errors = registry_check.collect_plugin_nodes(imports)
    assert len(errors) == 1
    assert errors[0]["module"] == "broken_plugin_fixture_087"
    assert "seeded break" in errors[0]["error"]
    # And the verdict path refuses it: a check carrying this error raises.
    check = registry_check.registry_self_check()
    assert check["ok"]
    check["plugin_module_errors"] = errors
    check["ok"] = False
    with pytest.raises(RuntimeError, match="broken_plugin_fixture_087"):
        registry_check.assert_registry_complete(check)


def test_raising_defs_function_fails_the_check(tmp_path, monkeypatch):
    """A defs function that raises mid-registration is named, not swallowed."""
    (tmp_path / "raising_plugin_fixture_087.py").write_text(
        "def _raising_node_defs():\n    raise RuntimeError('seeded defs failure')\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    _, errors = registry_check.collect_plugin_nodes(
        [("raising_plugin_fixture_087", ["_raising_node_defs"])]
    )
    assert len(errors) == 1
    assert "seeded defs failure" in errors[0]["error"]


def test_duplicate_production_fails_the_check(tmp_path, monkeypatch):
    """A second producer of an existing id is a duplicate, named by the check."""
    (tmp_path / "dup_plugin_fixture_087.py").write_text(
        "from glossa_lab.experiment_graph import AtomicNodeDef\n"
        "def _dup_node_defs():\n"
        "    return [AtomicNodeDef('IndusPhase248CeilingMine', 'Dup', 'X', 'dup',\n"
        "            [], [], {}, lambda inputs, params: {})]\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    imports = registry_check.loader_plugin_imports()
    imports.append(("dup_plugin_fixture_087", ["_dup_node_defs"]))
    sources, errors = registry_check.collect_plugin_nodes(imports)
    assert errors == []
    assert len(sources["IndusPhase248CeilingMine"]) == 2
    check = registry_check.registry_self_check()
    check["duplicate_ids"] = [
        {"id": "IndusPhase248CeilingMine", "sources": sources["IndusPhase248CeilingMine"]}
    ]
    check["ok"] = False
    with pytest.raises(RuntimeError, match="IndusPhase248CeilingMine"):
        registry_check.assert_registry_complete(check)


def test_strict_finalize_raises_on_recorded_failure(monkeypatch):
    """In strict mode the build close refuses a recorded registration failure."""
    monkeypatch.setattr(
        eg,
        "_REGISTRATION_FAILURES",
        [{"block": "Phase-999 nodes", "error": "ImportError: seeded"}],
    )
    monkeypatch.setenv("GLOSSA_REGISTRY_STRICT", "1")
    with pytest.raises(RuntimeError, match="Phase-999 nodes"):
        eg._finalize_registry_build()


def test_lenient_finalize_records_without_raising(monkeypatch):
    """With strict mode off, the same failure is reported, not raised."""
    monkeypatch.setattr(
        eg,
        "_REGISTRATION_FAILURES",
        [{"block": "Phase-999 nodes", "error": "ImportError: seeded"}],
    )
    monkeypatch.setenv("GLOSSA_REGISTRY_STRICT", "0")
    eg._finalize_registry_build()  # must not raise
    assert not eg.registry_build_report()["ok"]


def test_strict_gate_env_semantics(monkeypatch):
    """GLOSSA_REGISTRY_STRICT wins; otherwise strict except installed mode."""
    monkeypatch.setenv("GLOSSA_REGISTRY_STRICT", "1")
    monkeypatch.setenv("GLOSSA_MODE", "installed")
    assert eg.registry_strict_mode() is True
    monkeypatch.setenv("GLOSSA_REGISTRY_STRICT", "0")
    monkeypatch.setenv("GLOSSA_MODE", "dev")
    assert eg.registry_strict_mode() is False
    monkeypatch.delenv("GLOSSA_REGISTRY_STRICT")
    monkeypatch.setenv("GLOSSA_MODE", "installed")
    assert eg.registry_strict_mode() is False
    monkeypatch.setenv("GLOSSA_MODE", "dev")
    assert eg.registry_strict_mode() is True


# ── T103: shadow resolution guards (C087-2) ──────────────────────────────────


def test_no_duplicate_node_id_literals_in_source():
    """AST scan: no AtomicNodeDef id literal is defined in more than one place."""
    assert registry_check.duplicate_node_id_literals() == {}


def test_shadowed_ids_resolve_to_the_kept_definitions():
    """The three formerly shadowed ids live in misc_gaps only."""
    for node_id in SHADOWED_IDS:
        node_def = eg.ATOMIC_NODES[node_id]
        assert node_def.fn.__module__ == "glossa_lab.experiment_graph_phase_misc_gaps"
    sources, errors = registry_check.collect_plugin_nodes(
        [
            (
                "glossa_lab.experiment_graph_phase248_253",
                ["_phase248_254_node_defs"],
            )
        ]
    )
    assert errors == []
    for node_id in SHADOWED_IDS:
        assert node_id not in sources
    # The module's own five nodes (phases 248-253) still register from it.
    assert len(sources) == 5


# ── T105: rename (C087-16) ───────────────────────────────────────────────────


def test_old_module_name_is_gone():
    assert importlib.util.find_spec("glossa_lab.node_registry") is None
    assert importlib.util.find_spec("glossa_lab.study_node_registry") is not None


def test_both_registries_import_in_one_process():
    from glossa_lab.study_node_registry import router as study_router

    assert study_router is not None
    assert len(eg.ATOMIC_NODES) == 556


def test_node_registry_endpoint_unchanged(client):
    """GET /node-registry/{node_type}/{ref_id} answers as before the rename."""
    resp = client.get("/api/v1/node-registry/corpus/any")
    assert resp.status_code == 200
    body = resp.json()
    assert body["type"] == "object"
    assert "corpus_id" in body["properties"]


def test_registry_health_endpoint(client):
    """GET /experiment-graphs/registry-health exposes the build report."""
    resp = client.get("/api/v1/experiment-graphs/registry-health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["registered"] == 556
    assert body["failures"] == []
    assert body["duplicates"] == []
