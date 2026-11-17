"""Spec 095 Stage 2 — validator containment pinning tests (T201–T203).

Claim covered:
  C095-5  No v1 validator routine remains executable unguarded in a
          claim-bearing path of the live application: each of the
          four live v1 node paths of record is migrated, retired, or
          mechanically guarded, and a pinning test that plants a
          legacy-rule call in a claim-bearing path fails.

The four paths of record (Stage 0 census, completed at Stage 2):
  * IndusPhonologicalGap      — Phase-58 phonotactics v1 (script node)
  * IndusSiteStratification   — Phase-69 site-statistics v1 (script node)
  * IndusCisiCrosswalk116     — Phase-96 crosswalk v1 (script node)
  * IndusProvenanceRecompute  — Phase-108 recompute over the
    provenance_audit v1 library routines (phonotactic_check,
    site_invariance)

Disposition (Stage 2): mechanically guarded. The node functions
return the labelled refusal from glossa_lab.legacy_validator_guard;
the two provenance-audit v1 entry points raise LegacyValidatorRefused;
the three v1 scripts refuse direct execution from main().

The plants in this file are fixtures inside the tests — a temporary
node whose function calls a v1 routine, and a direct call through the
phase modules' own script runner. A plant "fails" when the guard
refuses it; that refusal is what these tests assert. No live code is
modified by a plant, and the temporary registry entry is removed
again (the registry is pinned by Spec 087's integrity tests).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg
from glossa_lab.legacy_validator_guard import (
    GUARDED_NODE_IDS,
    GUARDED_PATHS,
    LegacyValidatorRefused,
    refuse_legacy_validator,
    refusal_result,
)
from glossa_lab.pipelines import provenance_audit

BACKEND = Path(__file__).resolve().parents[1]
SCRIPTS = BACKEND / "scripts"

NODE_PATHS = {
    "IndusPhonologicalGap": "phonotactics_v1_node",
    "IndusSiteStratification": "site_stats_v1_node",
    "IndusCisiCrosswalk116": "crosswalk_v1_node",
    "IndusProvenanceRecompute": "provenance_recompute_v1_node",
}

# Keys a genuine v1 run would produce; a guarded node must produce none.
V1_OUTPUT_KEYS = {
    "IndusPhonologicalGap": {"n_valid", "n_invalid", "n_gap", "validity_rate"},
    "IndusSiteStratification": {"verdict", "chi2_p_value", "site_profiles",
                                "invariant_signs"},
    "IndusCisiCrosswalk116": {"crosswalk", "n_entries", "entries"},
    "IndusProvenanceRecompute": {"subsets", "phonotactics", "site_invariance"},
}


# ── The guard registry covers exactly the four paths of record ─────────────


def test_guard_registry_covers_the_four_node_paths():
    assert set(GUARDED_NODE_IDS) == set(NODE_PATHS)
    for node_id, path_id in NODE_PATHS.items():
        assert GUARDED_PATHS[path_id]["node_id"] == node_id


def test_guarded_nodes_remain_registered():
    """Guarded, not silently deregistered: the ids still resolve."""
    for node_id in NODE_PATHS:
        assert node_id in eg.ATOMIC_NODES


def test_refusal_result_is_labelled_and_carries_no_values():
    result = refusal_result("phonotactics_v1_node")
    refusal = result["legacy_validator_refusal"]
    assert refusal["claim"] == "C095-5"
    assert refusal["superseded_by"] == "glossa_lab.phonotactics_v2"
    assert "LegacyValidatorRefused" in result["error"]
    assert not ({"n_valid", "number", "json"} & set(result))


def test_refuse_raises_with_successor_named():
    with pytest.raises(LegacyValidatorRefused, match="site_stats_v2"):
        refuse_legacy_validator("provenance_audit_site_invariance")


# ── The four node paths refuse execution ────────────────────────────────────


@pytest.mark.parametrize("node_id,path_id", sorted(NODE_PATHS.items()))
def test_guarded_node_execution_returns_labelled_refusal(node_id, path_id):
    result = eg.ATOMIC_NODES[node_id].fn({}, {})
    refusal = result["legacy_validator_refusal"]
    assert refusal["path"] == path_id
    assert refusal["node_id"] == node_id
    assert "error" in result
    assert not (V1_OUTPUT_KEYS[node_id] & set(result))


# ── The provenance-audit v1 entry points refuse ─────────────────────────────


def test_provenance_audit_phonotactic_check_refuses():
    with pytest.raises(LegacyValidatorRefused, match="phonotactics_v2"):
        provenance_audit.phonotactic_check({})


def test_provenance_audit_site_invariance_refuses():
    with pytest.raises(LegacyValidatorRefused, match="site_stats_v2"):
        provenance_audit.site_invariance(set())


def test_provenance_audit_non_validator_surface_unaffected():
    """The guard covers the two v1 routines, not the whole library."""
    assert provenance_audit.normalize_reading("ay/ā") == "ay"
    assert provenance_audit.first_segment("kol/ka") == "kol"
    assert provenance_audit.token_coverage(["a"], {"a"})["coverage"] == 1.0


# ── T203: planted legacy-rule calls in claim-bearing paths fail ────────────


def test_planted_legacy_call_in_a_registered_node_fails():
    """Plant: a node whose fn calls the v1 phonotactic routine.

    Registered through the same funnel as every live node, then
    executed through the registry — the claim-bearing path. The plant
    fails: the guard raises before any v1 computation happens.
    """
    plant = eg.AtomicNodeDef(
        id="PlantedLegacyValidatorFixture095",
        name="Planted legacy validator (Spec 095 fixture)",
        category="Test Fixtures",
        description="Test plant: calls a superseded v1 validator routine.",
        inputs=[], outputs=[], params_schema={},
        fn=lambda inputs, params: provenance_audit.phonotactic_check({}),
    )
    eg._register_node(plant)
    try:
        with pytest.raises(LegacyValidatorRefused):
            eg.ATOMIC_NODES["PlantedLegacyValidatorFixture095"].fn({}, {})
    finally:
        eg.ATOMIC_NODES.pop("PlantedLegacyValidatorFixture095", None)
        eg._NODE_SOURCES.pop("PlantedLegacyValidatorFixture095", None)


def test_planted_legacy_call_through_script_runner_fails():
    """Plant: invoke the Phase-58 v1 script through the phase modules'
    own script runner, bypassing the guarded node function. The
    script itself refuses, so the runner surfaces a labelled error,
    never v1 output."""
    from glossa_lab.experiment_graph_phase56_61 import _run_phase_script

    result = _run_phase_script("phase58_phonological_gap.py")
    assert "error" in result
    assert "LegacyValidatorRefused" in result.get("stderr", "")


# ── The v1 scripts refuse direct execution ──────────────────────────────────


@pytest.mark.parametrize(
    "script,successor",
    [
        ("phase58_phonological_gap.py", "phonotactics_v2"),
        ("phase69_site_stratification.py", "site_stats_v2"),
        ("phase96_cisi_crosswalk.py", "crosswalk_provenance"),
    ],
)
def test_v1_scripts_refuse_direct_execution(script, successor):
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode != 0
    assert "LegacyValidatorRefused" in proc.stderr
    assert successor in proc.stderr
