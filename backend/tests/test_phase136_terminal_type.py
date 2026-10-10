"""Phase-136 (spec 024, FROZEN Stage 2(a); family member F1) —
results consistency pins + statistic unit tests.

The committed-JSON tests validate reports/phase136_results.json
for internal consistency, so they pass in CI where the local
store (the builder's inputs) does NOT exist. The recomputation
test skips cleanly when those inputs are absent (Phase-133
pattern).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_RESULTS = _REPO / "reports" / "phase136_results.json"
_REPORT = _REPO / "reports" / "phase136_report.md"
_BUILDER = _REPO / "backend" / "scripts" / "phase136_terminal_type.py"
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)

_spec = importlib.util.spec_from_file_location(
    "phase136_terminal_type", _BUILDER)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _res():
    return json.loads(_RESULTS.read_text("utf-8"))


def test_results_exist_and_carry_lineage_label():
    res = _res()
    assert res["phase"] == "Phase-136"
    assert res["family_member"] == "F1"
    assert res["lineage_label"] == "ICIT-lineage (horus84)"
    assert "not the Indus corpus in general" in res["lineage_sentence"]
    for entry in res["inputs"].values():
        assert entry["sha256"], "every input needs a recorded sha256"


def test_flow_counts_sum():
    f = _res()["flow"]
    assert (f["matched_single_volume"] + f["ambiguous"]
            + f["unmatched"]) == f["layer_rows"] == 5679
    assert f["unjoinable_or_ambiguous"] == 2784
    assert abs(f["unjoinable_or_ambiguous_share"] - 2784 / 5679) < 1e-12
    assert f["typed_filled"] + f["untyped"] == f["matched_single_volume"]
    assert sum(f["typed_by_type"].values()) == f["typed_filled"]
    assert f["restricted_seals_tablets"] == (
        f["typed_by_type"]["Seals"] + f["typed_by_type"]["Tablets"])
    assert (f["terminal_mapped"] + f["terminal_unk"]
            + f["terminal_no_codes"]) == f["restricted_seals_tablets"]
    assert f["analysis_population_all_strata"] == f["terminal_mapped"]
    eligible_n = sum(s["n"] for s in _res()["strata"] if s["eligible"])
    assert eligible_n == f["analysis_population_eligible_strata"]


def test_design_audit_counts_reproduced():
    f = _res()["flow"]
    assert (f["matched_single_volume"], f["ambiguous"],
            f["unmatched"]) == (2895, 2, 2782)
    assert f["typed_by_type"] == {"Seals": 1588, "Tablets": 1088,
                                  "Graffiti": 69, "Objects": 7}
    assert f["untyped"] == 143
    assert f["restricted_seals_tablets"] == 2676
    assert (f["terminal_mapped"], f["terminal_unk"]) == (2195, 481)
    assert f["terminal14_margin_among_mapped"] == 475


def test_strata_tables_and_eligibility():
    res = _res()
    assert res["eligible_strata"] == [
        "Mohenjo-daro", "Harappa", "Kalibangan"]
    for s in res["strata"]:
        t = s["table"]
        assert t["a"] + t["b"] == s["n_seals"]
        assert t["c"] + t["d"] == s["n_tablets"]
        assert s["n"] == s["n_seals"] + s["n_tablets"]
        expected_elig = (s["n"] >= 20 and s["n_seals"] >= 5
                         and s["n_tablets"] >= 5)
        assert s["eligible"] == expected_elig
    pooled = res["pooled_table_eligible"]
    for k in "abcd":
        assert pooled[k] == sum(s["table"][k] for s in res["strata"]
                                if s["eligible"])


def test_estimability_and_p_value():
    res = _res()
    est = res["estimability"]
    assert est["estimable"] is True and est["verdict"] == "ESTIMABLE"
    assert est["n_eligible_strata"] >= 2
    assert est["fraction_expected_ge_5"] >= 0.8
    assert all(e >= 5 for e in res["pooled_expected_counts"])
    test = res["test"]
    assert test["B"] == 9999 and test["seed"] == 20261009
    assert 0 < test["raw_p"] <= 1.0
    assert test["raw_p"] == (1 + test["n_perm_ge_observed"]) / (1 + 9999)
    assert test["statistic_observed"] > test["perm_stat_p95"]


def test_effect_sizes_consistency():
    es = _res()["effect_sizes"]
    or_mh, ci = es["mh_common_odds_ratio"], es["mh_ci95"]
    assert ci[0] < or_mh < ci[1]
    assert abs(es["mh_log_or"] - math.log(or_mh)) < 1e-9
    crude = es["crude_odds_ratio_uncontrolled"]
    assert crude["label"].startswith("uncontrolled")
    pooled = _res()["pooled_table_eligible"]
    assert abs(crude["odds_ratio"]
               - (pooled["a"] * pooled["d"])
               / (pooled["b"] * pooled["c"])) < 1e-9
    shares = es["pooled_terminal14_shares"]
    assert abs(shares["seals"] - pooled["a"]
               / (pooled["a"] + pooled["b"])) < 1e-12
    assert abs(shares["tablets"] - pooled["c"]
               / (pooled["c"] + pooled["d"])) < 1e-12


def test_cmh_hand_checkable_table():
    # Single stratum a=10,b=5,c=3,d=12 (N=30): E[a]=6.5,
    # Var = 15*15*13*17/(30^2*29) = 1.905172..., CMH = 3.5^2/Var.
    table = [{"a": 10, "b": 5, "c": 3, "d": 12}]
    var = 15 * 15 * 13 * 17 / (30 * 30 * 29)
    assert abs(_mod.cmh_statistic(table) - 12.25 / var) < 1e-9
    # MH OR for one stratum equals its plain OR = (10*12)/(5*3) = 8.
    mh = _mod.mh_odds_ratio(table)
    assert abs(mh["common_odds_ratio"] - 8.0) < 1e-12
    assert mh["ci95"][0] < 8.0 < mh["ci95"][1]
    assert abs(_mod.odds_ratio(10, 5, 3, 12) - 8.0) < 1e-12


def test_cmh_no_association_table_is_zero():
    # a exactly at its expectation in every stratum -> statistic 0.
    tables = [{"a": 5, "b": 5, "c": 5, "d": 5},
              {"a": 2, "b": 6, "c": 3, "d": 9}]
    assert _mod.cmh_statistic(tables) == 0.0
    assert abs(_mod.mh_odds_ratio(tables)["common_odds_ratio"]
               - 1.0) < 1e-12


def test_permutation_determinism_toy():
    strata = [{"site": "Toy", "n_seals": 10,
               "outcomes": [True] * 6 + [False] * 4
               + [True] * 2 + [False] * 8}]
    r1 = _mod.permutation_test(strata, b_perm=99, seed=20261009,
                               deadline_seconds=600)
    r2 = _mod.permutation_test(strata, b_perm=99, seed=20261009,
                               deadline_seconds=600)
    assert r1["p_value"] == r2["p_value"]
    assert r1["perm_stat_median"] == r2["perm_stat_median"]
    assert 0 < r1["p_value"] <= 1.0


def test_anchors_sha256_unchanged():
    digest = hashlib.sha256(_ANCHORS.read_bytes()).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_report_exists_with_lineage_headline():
    text = _REPORT.read_text("utf-8")
    assert "ICIT-lineage" in text
    assert "49.0%" in text
    assert _ANCHORS_SHA256 in text


def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase136TerminalType" in ATOMIC_NODES


def test_builder_recomputation_skips_without_inputs():
    """Recompute into a temp file iff the local store exists."""
    store = (Path.home() / "workspace" / "glossa-lab" / "corpora"
             / "downloads" / "cisi_image_layer" / "catalogue"
             / "cisi_vol1_catalogue.csv")
    horus = (Path.home() / "workspace" / "research_notes"
             / "indus-data-deep-sweep-20261008" / "downloads"
             / "horus84-computational-linguistics" / "data"
             / "inscriptions.csv")
    if not (store.exists() and horus.exists()):
        pytest.skip("local store absent (CI): builder inputs "
                    "are local-only by design")
    out = Path("/tmp/phase136_recomputed.json")
    r = subprocess.run(
        [sys.executable, str(_BUILDER), "--out", str(out)],
        capture_output=True, text=True, timeout=1200,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    committed = _res()
    assert recomputed["flow"] == committed["flow"]
    assert recomputed["test"] == committed["test"]
    assert recomputed["effect_sizes"] == committed["effect_sizes"]
