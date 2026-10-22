"""Phase-139 (spec 025, FROZEN 2026-10-10) — covariate audit
+ harmonization consistency pins.

These tests validate the COMMITTED results JSON
(reports/phase139_results.json), the harmonized dataset, and
the citation register for internal consistency, so they pass
in CI where the local store (the script's input layer) does
NOT exist. The one recomputation test skips cleanly when the
input is absent (Phase-133 pattern).

Frozen design pins: Phase-137 F3 population (5,410
inscriptions, 7 eligible sites); gate thresholds >= 70%
recorded / >= 3 sites at >= 30 recorded / >= 1,000
permutable (spec sec.4.2 step 3, adjudication Q5); routing
rule (gate-fail -> SENSITIVITY; sole passer forms the
primary strata). MARGINS ONLY: the results JSON must carry
no association quantity of any kind.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_RESULTS = _REPO / "reports" / "phase139_results.json"
_DATASET = (_REPO / "data" / "evidence_integration"
            / "phase139_harmonized_covariates.json")
_REGISTER = (_REPO / "data" / "evidence_integration"
             / "phase139_citation_register.json")
_SCRIPT = _REPO / "backend" / "scripts" / \
    "phase139_covariate_audit.py"
_ANCHORS = _REPO / "backend" / "reports" / \
    "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
_LAYER = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")

_spec = importlib.util.spec_from_file_location(
    "phase139_covariate_audit", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


@pytest.fixture(scope="module")
def results():
    return json.loads(_RESULTS.read_text("utf-8"))


@pytest.fixture(scope="module")
def dataset():
    return json.loads(_DATASET.read_text("utf-8"))


# ---------------------------------------------------------------------------
# Pure-helper pins
# ---------------------------------------------------------------------------

def test_gate_thresholds_are_the_frozen_ones():
    assert _mod.GATE_MIN_COVERAGE == 0.70
    assert _mod.GATE_MIN_SITES == 3
    assert _mod.GATE_MIN_SITE_RECORDED == 30
    assert _mod.GATE_MIN_PERMUTABLE == 1000


def test_apply_gate_arms():
    g = _mod.apply_gate(700, 1000, 3, 1000)
    assert g["passes"] is True
    g = _mod.apply_gate(699, 1000, 3, 1000)
    assert g["passes"] is False
    assert g["arms"]["i_recorded_coverage_ge_0.70"] is False
    g = _mod.apply_gate(900, 1000, 2, 5000)
    assert g["arms"]["ii_sites_with_ge30_recorded_ge_3"] is False
    g = _mod.apply_gate(900, 1000, 5, 999)
    assert g["arms"]["iii_permutable_ge_1000"] is False


def test_chron_mapping_cells():
    assert _mod.map_chron_cell("Harappa", "period", "3") == (
        "middle", "KENOYER2008")
    assert _mod.map_chron_cell("Harappa", "phase", "B/C") == (
        "middle", "KENOYER2008")
    assert _mod.map_chron_cell("Dholavira", "period", "6") == (
        "late", "BISHT_DHOLAVIRA")
    assert _mod.map_chron_cell("Nausharo", "period", "3") == (
        "late", "JARRIGE1993_NAUSHARO")
    # Unmapped cells stay UNRECORDED with a reason.
    band, reason = _mod.map_chron_cell("Harappa", "period", "2/3")
    assert band is None and "boundary" in reason
    band, reason = _mod.map_chron_cell(
        "Harappa", "phase", "Stratum II")
    assert band is None and "Vats" in reason
    band, reason = _mod.map_chron_cell(
        "Lothal", "period", "Layer 7")
    assert band is None and "layer" in reason.lower()
    band, reason = _mod.map_chron_cell(
        "Nausharo", "period", "4")
    assert band is None and "Period IV" in reason
    band, reason = _mod.map_chron_cell(
        "Mohenjo-daro", "phase", "II")
    assert band is None


def test_chron_precedence_period_wins():
    band, source, _cite, conflict = _mod.harmonize_chron(
        "Mohenjo-daro", "Late", "II")
    assert (band, source, conflict) == ("late", "period", False)
    band, source, _cite, conflict = _mod.harmonize_chron(
        "Harappa", "-", "B")
    assert (band, source) == ("middle", "phase")
    band, source, _cite, _c = _mod.harmonize_chron(
        "Chanhu-daro", "-", "-")
    assert band == _mod.UNRECORDED and source is None


def test_preservation_collapse():
    assert _mod.collapse_preservation("complete") == "complete"
    assert _mod.collapse_preservation("fragment") == "fragment"
    assert _mod.collapse_preservation("chipped") == "damaged"
    assert _mod.collapse_preservation(
        "slightly chipped") == "damaged"
    assert _mod.collapse_preservation(
        "partly damaged") == "damaged"
    assert _mod.collapse_preservation("-") == _mod.UNRECORDED


def test_parse_depth_categories():
    assert _mod.parse_depth("- -") == ("MISSING", None, None)
    assert _mod.parse_depth("+10.8 ft") == ("VALUE", 10.8, "ft")
    assert _mod.parse_depth("surface -")[0] == "SURFACE"
    cat, val, unit = _mod.parse_depth("97-110 cm")
    assert cat == "RANGE" and val == 103.5 and unit == "cm"
    cat, val, unit = _mod.parse_depth("-7..75 ft")
    assert cat == "DECIMAL_DOTDOT" and val == -7.75
    cat, val, unit = _mod.parse_depth("-4:0 ft")
    assert cat == "COLON_FT_IN" and val == -4.0
    cat, val, unit = _mod.parse_depth("0 -")
    assert cat == "UNITLESS" and val == 0.0
    assert _mod.parse_depth("- ft")[0] == "UNPARSED"


def test_depth_banding_tertiles_and_small_groups():
    rows = []
    for i in range(9):
        rows.append({"id": str(i), "site": "S",
                     "depth_category": "VALUE",
                     "depth_value": float(i),
                     "depth_unit": "ft"})
    rows.append({"id": "x", "site": "T",
                 "depth_category": "VALUE", "depth_value": 1.0,
                 "depth_unit": "ft"})
    _mod.assign_depth_bands(rows)
    bands = [r["depth_band"] for r in rows[:9]]
    assert bands == ["shallow"] * 3 + ["middle"] * 3 \
        + ["deep"] * 3
    assert rows[9]["depth_band"] == _mod.UNRECORDED  # group n=1


# ---------------------------------------------------------------------------
# Committed-artifact pins
# ---------------------------------------------------------------------------

def test_population_and_anchors(results):
    assert results["population"]["inscriptions"] == 5410
    assert len(results["population"]["eligible_sites"]) == 7
    assert results["anchors_sha256"] == _ANCHORS_SHA256
    assert results["input"]["sha256"] == (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef")


def test_sec3_reproduction(results):
    repro = results["spec_sec3_reproduction"]
    assert repro["count_fields_match_spec_sec3"] is True
    assert repro["f3_population"]["period_informative"] == 2266
    assert repro["f3_population"]["phase_informative"] == 2638
    assert len(repro["deltas"]) == 3  # documented, bounded


def test_gate_application_verbatim(results):
    gates = results["gate"]["per_covariate"]
    assert gates["chron_band"]["recorded"] == 2267
    assert gates["chron_band"]["passes"] is False
    assert gates["chron_band"]["arms"][
        "i_recorded_coverage_ge_0.70"] is False
    assert gates["depth_band"]["recorded"] == 2765
    assert gates["depth_band"]["passes"] is False
    assert gates["preservation"]["recorded"] == 5404
    assert gates["preservation"]["passes"] is True
    assert results["gate"]["classifications"] == {
        "chron_band": "SENSITIVITY",
        "depth_band": "SENSITIVITY",
        "preservation": "PRIMARY CONTROL",
    }


def test_verdict(results):
    v = results["verdict"]
    assert v["word"] == "ESTIMABLE"
    assert v["primary_control_set"] == ["preservation"]
    assert "preservation" in v["primary_strata"]
    assert sorted(v["sensitivity_panel"]) == [
        "chron_band", "depth_band"]


def test_margins_sum_to_population(results):
    for section, key in (("chron_band", "margins"),
                         ("depth_band", "margins"),
                         ("preservation", "margins")):
        levels = results[section][key]["levels"]
        assert sum(levels.values()) == 5410, section
        for site, per in results[section][key][
                "per_site"].items():
            assert sum(per["levels"].values()) == per["n"]


def test_dataset_rows_and_no_text_field(dataset):
    assert len(dataset) == 5410
    for row in dataset:
        assert "text" not in row
        assert row["chron_band"] in (
            "early", "middle", "late", "UNRECORDED")
        assert row["depth_band"] in (
            "shallow", "middle", "deep", "UNRECORDED")
        if row["chron_band"] != "UNRECORDED":
            assert row["chron_citation"]
            assert row["chron_source_field"] in (
                "period", "phase")


def test_register_every_mapped_cell_cited():
    register = json.loads(_REGISTER.read_text("utf-8"))
    assert len(register["mapped_cells"]) == len(_mod.CHRON_MAP)
    for cell in register["mapped_cells"]:
        assert cell["citation"] in register["citations"]
        assert cell["band"] in ("early", "middle", "late")
    assert len(register["citations"]) == 7


def _all_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k).lower()
            yield from _all_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _all_keys(v)


def test_fence_no_association_quantities(results):
    # No computed association quantity may exist under any key.
    # (Prose fields — e.g. the fence statement itself — name the
    # forbidden quantities; the invariant is about keys/values
    # computed, so keys are what is pinned.)
    for key in _all_keys(results):
        for forbidden in ("chi_square", "chi-square",
                          "odds_ratio", "p_value", "cramers",
                          "permutation", "observed_statistic"):
            assert forbidden not in key, (key, forbidden)
    assert "association quantity was computed" in \
        results["fence"]


def test_graph_node_registered():
    import sys
    sys.path.insert(0, str(_REPO / "backend"))
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase139CovariateAudit" in ATOMIC_NODES


# ---------------------------------------------------------------------------
# Recomputation (skips in CI — the layer lives in the local store)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _LAYER.exists(),
                    reason="local-store layer not present")
def test_recomputation_matches_committed(results, tmp_path):
    out = tmp_path / "results.json"
    ds = tmp_path / "dataset.json"
    reg = tmp_path / "register.json"
    rc = _mod.main(["--layer", str(_LAYER), "--out", str(out),
                    "--dataset", str(ds), "--register", str(reg)])
    assert rc == 0
    fresh = json.loads(out.read_text("utf-8"))
    assert fresh["gate"] == results["gate"]
    assert fresh["verdict"] == results["verdict"]
    assert fresh["population"] == results["population"]
