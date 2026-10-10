"""Phase-140 (spec 025, FROZEN 2026-10-10) — G1 controlled
F3 re-test consistency pins.

These tests validate the COMMITTED results JSON
(reports/phase140_results.json) for internal consistency,
so they pass in CI where the local store (the script's
layer input) does NOT exist. The recomputation test skips
cleanly when the input is absent (Phase-133 pattern).

Frozen design pins (phase140-freeze.md, under the
Phase-139 freeze record): population = Phase-137 F3
population reproduced by rule (5,410 inscriptions, 7
sites, ICIT-lineage layer horus84); statistic family =
Phase-137 F3 exactly; primary strata = composition x
preservation with UNRECORDED as a level, primary-
control set exactly {preservation}; B = 9,999, seed
20261009; verdict per Q4(b) — BH over G1 alone (m = 1),
SUPPORTED under control iff raw p <= 0.05; chronology
NOT controlled (rider mandatory); S-chron / S-depth are
EXPLORATORY bounds with coverage stated; the
uncontrolled configuration must reproduce the committed
Phase-137 F3 result exactly (regression).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_RESULTS = _REPO / "reports" / "phase140_results.json"
_RESULTS137 = _REPO / "reports" / "phase137_results.json"
_SCRIPT = _REPO / "backend" / "scripts" / \
    "phase140_g1_controlled.py"
_ANCHORS = _REPO / "backend" / "reports" / \
    "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
_LAYER = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")
_LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
)

_spec = importlib.util.spec_from_file_location(
    "phase140_g1_controlled", _SCRIPT)
phase140 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase140)


def _results():
    return json.loads(_RESULTS.read_text("utf-8"))


@pytest.fixture(scope="module")
def results():
    return _results()


# ---------------------------------------------------------------------------
# Pure-function unit tests (no local store)
# ---------------------------------------------------------------------------

def test_permutable_inscriptions_counts_multistrata():
    analysis = [
        {"site": "A", "stratum": "SEAL|1"},
        {"site": "B", "stratum": "SEAL|1"},
        {"site": "A", "stratum": "SEAL|2-3"},
        {"site": "A", "stratum": "SEAL|2-3"},
    ]
    n, table = phase140.permutable_inscriptions(
        analysis, lambda i: i["stratum"])
    # SEAL|1 spans 2 sites (permutable); SEAL|2-3 is
    # single-site (constant under permutation).
    assert n == 2
    by_key = {t["stratum"]: t for t in table}
    assert by_key["SEAL|1"]["permutable_inscriptions"] == 2
    assert by_key["SEAL|2-3"]["permutable_inscriptions"] == 0
    assert by_key["SEAL|2-3"]["n_sites"] == 1


def test_frozen_parameters():
    assert phase140.B_PERM == 9999
    assert phase140.SEED == 20261009
    assert phase140.MIN_SIGN_COUNT == 10
    assert phase140.PLACEHOLDERS == {"000", "999"}


# ---------------------------------------------------------------------------
# Committed-results consistency pins
# ---------------------------------------------------------------------------

def test_population_and_anchors(results):
    assert results["population"]["inscriptions"] == 5410
    assert results["population"]["eligible_sites"] == [
        "Chanhu-daro", "Dholavira", "Harappa", "Kalibangan",
        "Lothal", "Mohenjo-daro", "Nausharo"]
    assert results["population"][
        "matches_committed_phase137_f3"] is True
    assert results["table_dimensions"] == [7, 187]
    assert results["input"]["sha256"] == _LAYER_SHA256
    assert results["anchors_sha256"] == _ANCHORS_SHA256
    assert hashlib.sha256(
        _ANCHORS.read_bytes()).hexdigest() == _ANCHORS_SHA256


def test_regression_reproduces_phase137_f3_exactly(results):
    reg = results["regression_composition_only"]
    f3 = json.loads(_RESULTS137.read_text("utf-8"))[
        "layers"]["F3_icit_lineage"]
    assert reg["matches_committed_phase137_f3_exactly"] is True
    assert reg["observed_chi_square"] == \
        f3["observed_chi_square"]
    assert reg["permutation"] == f3["permutation"]


def test_g1_design_pins(results):
    g1 = results["g1_primary"]
    assert g1["primary_control_set"] == ["preservation"]
    assert g1["permutation"]["B"] == 9999
    assert g1["permutation"]["seed"] == 20261009
    assert g1["nominal_inscriptions"] == 5410
    # Phase-139 projection for the primary strata.
    assert g1["permutable_inscriptions"] == 5404
    # Strata keys are composition x preservation with
    # UNRECORDED retained as a level.
    levels = {t["stratum"].rsplit("|", 1)[1]
              for t in g1["strata"]["table"]}
    assert levels <= {"complete", "fragment", "damaged",
                      "UNRECORDED"}
    assert "UNRECORDED" in levels


def test_g1_verdict_rule_q4b(results):
    g1 = results["g1_primary"]
    bh = g1["benjamini_hochberg"]
    assert bh["m"] == 1 and bh["q"] == 0.05
    assert bh["adjusted_value"] == g1["p_value_raw"]
    expected = ("SUPPORTED under control"
                if g1["p_value_raw"] <= 0.05
                else "NOT SUPPORTED under control")
    assert g1["verdict"] == expected
    assert "NOT a family correction" in bh["statement"]


def test_chronology_rider_present(results):
    rider = results["headline_rider"]
    assert "Chronology is NOT controlled" in rider
    assert results["lineage_label"] == \
        "ICIT-lineage layer (horus84)"
    assert "Chronology is NOT controlled" in \
        results["g1_primary"]["verdict_statement"]
    assert "99.9%" in results["g1_primary"][
        "verdict_statement"]


def test_sensitivity_panel_is_exploratory(results):
    panel = results["sensitivity_panel_exploratory"]
    for name, cov in (("S_chron", 2267 / 5410),
                      ("S_depth", 2765 / 5410)):
        s = panel[name]
        assert "EXPLORATORY" in s["role"]
        assert s["recorded_coverage"] == cov
        assert "verdict" not in s
        assert s["nominal_inscriptions"] == 5410
        assert s["permutation"]["B"] == 9999
        assert s["permutation"]["seed"] == 20261009


def test_sparsity_disclosed(results):
    for cfg in (results["g1_primary"],
                *results["sensitivity_panel_exploratory"]
                .values()):
        sp = cfg["sparsity_disclosure"]
        assert sp["cells_total"] == 7 * 187
        assert "share_cells_expected_lt5" in sp
        assert "min_expected_count" in sp


def test_graph_node_registered():
    sys.path.insert(0, str(_REPO / "backend"))
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase140G1Controlled" in ATOMIC_NODES


# ---------------------------------------------------------------------------
# Recomputation (skips in CI — the layer lives in the local store)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _LAYER.exists(),
                    reason="local-store layer not present")
def test_recomputation_matches_committed(results, tmp_path):
    out = tmp_path / "phase140_recomputed.json"
    r = subprocess.run(
        [sys.executable, str(_SCRIPT), "--out", str(out)],
        capture_output=True, text=True, timeout=3600,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    for key in ("population", "table_dimensions"):
        assert recomputed[key] == results[key]
    assert recomputed["regression_composition_only"][
        "permutation"] == results[
            "regression_composition_only"]["permutation"]
    assert recomputed["g1_primary"]["permutation"] == \
        results["g1_primary"]["permutation"]
    assert recomputed["g1_primary"]["verdict"] == \
        results["g1_primary"]["verdict"]
    for name in ("S_chron", "S_depth"):
        assert recomputed["sensitivity_panel_exploratory"][
            name]["permutation"] == results[
                "sensitivity_panel_exploratory"][name][
                    "permutation"]
