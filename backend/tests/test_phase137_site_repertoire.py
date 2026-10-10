"""Phase-137 (spec 024, FROZEN Stage 2(c)) — site repertoire
differentiation consistency pins.

These tests validate the COMMITTED results JSON
(reports/phase137_results.json) for internal consistency, so
they pass in CI where the local store (the script's inputs)
does NOT exist. The one recomputation test skips cleanly when
the inputs are absent (Phase-133 pattern).

Frozen design pins: family members F2 (Holdat) and F3
(ICIT-lineage) tested separately, never pooled; B = 9,999,
seed 20261009, p = (1 + #{perm >= obs}) / (1 + B); sign
columns = layer-wide count >= 10 within the analysis
population, rarer signs in OTHER; site inclusion >= 30
inscriptions AND >= 100 tokens; mandatory sparsity
disclosure (freeze section 3).
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
_RESULTS = _REPO / "reports" / "phase137_results.json"
_SCRIPT = _REPO / "backend" / "scripts" / \
    "phase137_site_repertoire.py"
_ANCHORS = _REPO / "backend" / "reports" / \
    "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)

_spec = importlib.util.spec_from_file_location(
    "phase137_site_repertoire", _SCRIPT)
phase137 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase137)


def _results():
    return json.loads(_RESULTS.read_text("utf-8"))


def _layer(key):
    return _results()["layers"][key]


# ---------------------------------------------------------------------------
# Pure-function unit tests (no local store)
# ---------------------------------------------------------------------------

def test_chi_square_hand_checkable_table():
    # Perfectly separated 2x2: every expected count is 5,
    # chi-square = 4 * (5^2 / 5) = 20.
    assert phase137.chi_square([[10, 0], [0, 10]]) == 20.0
    # Independence table: observed == expected everywhere.
    assert phase137.chi_square([[5, 5], [5, 5]]) == 0.0
    # 2x3 hand-check: row totals 30/30, col totals 20/20/20,
    # expected 10 per cell; chi2 = 6 * (5^2 / 10) / ... each
    # cell deviates by 5 or 0: cells are (15,5,10),(5,15,10)
    # -> 4 cells * 25/10 = 10.
    assert phase137.chi_square(
        [[15, 5, 10], [5, 15, 10]]) == 10.0


def test_cramers_v_perfect_separation():
    table = [[10, 0], [0, 10]]
    v = phase137.cramers_v(table, phase137.chi_square(table))
    assert v == 1.0


def test_tv_distance_bounds():
    table = [[10, 0], [0, 10]]
    dists = phase137.tv_distances(table)
    assert dists == [0.5, 0.5]
    same = phase137.tv_distances([[5, 5], [5, 5]])
    assert same == [0.0, 0.0]


def test_site_inclusion_rule():
    assert phase137.site_eligible(30, 100)
    assert phase137.site_eligible(606, 2534)
    assert not phase137.site_eligible(29, 100000)
    assert not phase137.site_eligible(100000, 99)
    assert not phase137.site_eligible(28, 136)  # Unknown-like


def test_holdat_length_classes():
    assert phase137.holdat_length_class(2) == "2-3"
    assert phase137.holdat_length_class(3) == "2-3"
    assert phase137.holdat_length_class(4) == "4-5"
    assert phase137.holdat_length_class(5) == "4-5"
    assert phase137.holdat_length_class(6) == "6-8"
    assert phase137.holdat_length_class(8) == "6-8"


def test_horus_strata_classes():
    assert phase137.horus_length_class(1) == "1"
    assert phase137.horus_length_class(3) == "2-3"
    assert phase137.horus_length_class(5) == "4-5"
    assert phase137.horus_length_class(6) == "6+"
    assert phase137.horus_type_class("SEAL:u") == "SEAL"
    assert phase137.horus_type_class("TAB:pn") == "TAB"
    assert phase137.horus_type_class("POT:T:g") == "POT"
    for pooled in ("TAG:x", "MISC:x", "BNGL:x", "ROD:x",
                   "IMPL:x", "BEAD:x", "MDLN:x", "Unknown"):
        assert phase137.horus_type_class(pooled) == "OTHER"


def test_clean_value_strips_single_quotes():
    assert phase137.clean_value("'M391'") == "M391"
    assert phase137.clean_value("M391") == "M391"
    assert phase137.clean_value(" 'Harappa' ") == "Harappa"


def test_permutation_determinism_toy_population():
    # Two sites with disjoint sign use, one stratum.
    insc = []
    for _ in range(6):
        insc.append((0, "s", ((0, 2),)))
        insc.append((1, "s", ((1, 2),)))
    table = [[12, 0], [0, 12]]
    observed = phase137.chi_square(table)
    stats1, ge1 = phase137.run_permutation(
        insc, 2, 2, observed, b=99, seed=20261009,
        deadline_s=120, label="toy")
    stats2, ge2 = phase137.run_permutation(
        insc, 2, 2, observed, b=99, seed=20261009,
        deadline_s=120, label="toy")
    assert stats1 == stats2
    assert ge1 == ge2
    summary = phase137.permutation_summary(stats1, ge1, b=99)
    assert 0 < summary["p_value_raw"] <= 1
    # separated profiles: observed is the maximum attainable
    assert summary["permutation_median"] < observed


def test_permutation_respects_strata():
    # Site is perfectly confounded with stratum: within-stratum
    # shuffles can never move a token across sites, so every
    # permutation reproduces the observed statistic exactly.
    insc = ([(0, "a", ((0, 1),))] * 4
            + [(1, "b", ((1, 1),))] * 4)
    table = [[4, 0], [0, 4]]
    observed = phase137.chi_square(table)
    stats, ge = phase137.run_permutation(
        insc, 2, 2, observed, b=49, seed=20261009,
        deadline_s=120, label="toy-strata")
    assert all(s == observed for s in stats)
    assert ge == 49


# ---------------------------------------------------------------------------
# Committed-JSON consistency (CI-safe)
# ---------------------------------------------------------------------------

def test_results_exist_and_parameters_frozen():
    res = _results()
    assert res["phase"] == "Phase-137"
    params = res["parameters"]
    assert params["B_permutations"] == 9999
    assert params["seed"] == 20261009
    assert params["min_sign_count_for_column"] == 10
    assert params["site_inclusion"] == {
        "min_inscriptions": 30, "min_tokens": 100}
    assert res["anchors_sha256"] == _ANCHORS_SHA256
    # Class I fields are recorded as entering nothing
    used = res["fields_used"]
    assert used["holdat"] == ["letters", "position",
                              "seal_id", "site"]
    assert used["horus84"] == ["text", "site", "type"]
    class_i = used["class_i_fields_entering_nothing"]
    assert "noun" in class_i["holdat"]
    assert "upos" in class_i["holdat"]
    assert "sanskrit" in class_i["horus84"]
    assert "translation" in class_i["horus84"]


def test_f2_holdat_population_counts():
    layer = _layer("F2_holdat")
    assert layer["family_member"] == "F2"
    flow = layer["population_flow"]
    assert flow["inscriptions_parsed"] == 1670
    assert flow["token_rows_read"] == 7002
    assert flow["distinct_signs_native_full_layer"] == 390
    assert len(layer["eligible_sites"]) == 9
    assert layer["excluded_sites"] == []
    by_site = {s["site"]: s for s in layer["sites_all"]}
    assert by_site["Mohenjo-daro"]["inscriptions"] == 606
    assert by_site["Mohenjo-daro"]["parsed_tokens"] == 2534
    assert by_site["Harappa"]["inscriptions"] == 492
    assert by_site["Rakhigarhi"]["inscriptions"] == 33
    assert layer["analysis_population"]["inscriptions"] == 1670
    assert layer["analysis_population"]["profile_tokens"] == 7002
    # length-only strata (type control degenerates, stated)
    assert set(layer["strata_counts"]) == {"2-3", "4-5", "6-8"}
    assert sum(layer["strata_counts"].values()) == 1670


def test_f3_icit_population_counts():
    layer = _layer("F3_icit_lineage")
    assert layer["family_member"] == "F3"
    assert "ICIT-lineage" in layer["headline_label"]
    flow = layer["population_flow"]
    assert flow["rows_read"] == 5679
    assert flow["rows_with_ge1_parsed_token"] == 5679
    assert flow["distinct_signs_nonplaceholder_full_layer"] == 713
    assert flow["nonplaceholder_tokens_full_layer"] == 18047
    assert layer["eligible_sites"] == [
        "Chanhu-daro", "Dholavira", "Harappa", "Kalibangan",
        "Lothal", "Mohenjo-daro", "Nausharo"]
    assert layer["analysis_population"]["inscriptions"] == 5410
    by_site = {s["site"]: s for s in layer["sites_all"]}
    assert by_site["Harappa"]["inscriptions"] == 2717
    assert by_site["Harappa"]["parsed_tokens"] == 7975
    assert by_site["Mohenjo-daro"]["inscriptions"] == 1923
    assert by_site["Nausharo"]["inscriptions"] == 38
    # Unknown is a missing-value label, excluded and named
    excluded = {s["site"] for s in layer["excluded_sites"]}
    assert "Unknown" in excluded
    assert sum(layer["strata_counts"].values()) == 5410


@pytest.mark.parametrize("key", ["F2_holdat", "F3_icit_lineage"])
def test_table_margins_equal_token_totals(key):
    layer = _layer(key)
    table = layer["profile_table"]
    counts = table["counts"]
    assert table["sites"] == layer["eligible_sites"]
    assert len(counts) == len(table["sites"])
    for row, total in zip(counts, table["row_totals"]):
        assert sum(row) == total
        assert len(row) == len(table["columns"])
    for c, total in enumerate(table["column_totals"]):
        assert sum(row[c] for row in counts) == total
    assert sum(table["row_totals"]) == table["grand_total"]
    assert table["grand_total"] == \
        layer["analysis_population"]["profile_tokens"]
    # row totals are the per-site profile token counts
    by_site = {s["site"]: s for s in layer["sites_all"]}
    for site, total in zip(table["sites"], table["row_totals"]):
        assert by_site[site]["profile_tokens_nonplaceholder"] \
            == total
    assert layer["table_dimensions"] == [
        len(table["sites"]), len(table["columns"])]


@pytest.mark.parametrize("key", ["F2_holdat", "F3_icit_lineage"])
def test_p_value_and_sparsity_fields(key):
    layer = _layer(key)
    assert layer["estimable"] is True
    p = layer["p_value_raw"]
    assert 0 < p <= 1
    perm = layer["permutation"]
    assert perm["B"] == 9999
    assert perm["seed"] == 20261009
    assert perm["p_value_raw"] == p
    assert perm["permutation_median"] <= \
        perm["permutation_p95_nearest_rank"]
    assert layer["observed_chi_square"] > 0
    assert 0 <= layer["cramers_v_descriptive"] <= 1
    sparsity = layer["sparsity_disclosure"]
    for field in ("cells_total", "cells_expected_lt5",
                  "share_cells_expected_lt5",
                  "min_expected_count", "per_site_tokens"):
        assert field in sparsity, field
    assert sparsity["cells_total"] == \
        layer["table_dimensions"][0] * layer["table_dimensions"][1]
    assert 0.0 <= sparsity["share_cells_expected_lt5"] <= 1.0
    assert sparsity["min_expected_count"] > 0
    assert sparsity["per_site_tokens"] == \
        layer["profile_table"]["row_totals"]
    tv = layer["per_site_tv_distance_descriptive"]
    assert set(tv) == set(layer["eligible_sites"])
    assert all(0.0 <= v <= 1.0 for v in tv.values())


@pytest.mark.parametrize("key", ["F2_holdat", "F3_icit_lineage"])
def test_other_column_accounting(key):
    layer = _layer(key)
    sign_space = layer["sign_space"]
    table = layer["profile_table"]
    assert sign_space["other_column_present"] is True
    assert table["columns"][-1] == "OTHER"
    assert sign_space["n_sign_columns_kept"] == \
        len(table["columns"]) - 1
    other_total = sum(row[-1] for row in table["counts"])
    assert other_total == sign_space["other_tokens"]
    expected_share = (sign_space["other_tokens"]
                      / layer["analysis_population"]
                      ["profile_tokens"])
    assert abs(sign_space["other_share_of_profile_tokens"]
               - expected_share) < 1e-12


def test_inputs_recorded_with_sha256():
    for key in ("F2_holdat", "F3_icit_lineage"):
        inp = _layer(key)["input"]
        assert inp["path"]
        assert len(inp["sha256"]) == 64
        int(inp["sha256"], 16)


def test_anchors_sha256_unchanged():
    digest = hashlib.sha256(_ANCHORS.read_bytes()).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase137SiteRepertoire" in ATOMIC_NODES


def test_recomputation_skips_without_inputs():
    """Recompute into a temp file iff the local store exists."""
    holdat = Path.home() / "workspace" / "glossa-lab" / \
        "corpora" / "downloads" / "external_repos" / \
        "holdatllc_indus" / "indus_corpus 2.csv"
    horus = Path.home() / "workspace" / "research_notes" / \
        "indus-data-deep-sweep-20261008" / "downloads" / \
        "horus84-computational-linguistics" / "data" / \
        "inscriptions.csv"
    if not (holdat.exists() and horus.exists()):
        pytest.skip("local store absent (CI): script inputs "
                    "are local-only by design")
    out = Path("/tmp/phase137_recomputed.json")
    r = subprocess.run(
        [sys.executable, str(_SCRIPT), "--out", str(out)],
        capture_output=True, text=True, timeout=3600,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    committed = _results()
    for key in ("F2_holdat", "F3_icit_lineage"):
        new, old = recomputed["layers"][key], \
            committed["layers"][key]
        assert new["profile_table"] == old["profile_table"]
        assert new["observed_chi_square"] == \
            old["observed_chi_square"]
        assert new["p_value_raw"] == old["p_value_raw"]
        assert new["permutation"] == old["permutation"]
