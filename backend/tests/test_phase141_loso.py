"""Phase-141 (spec 025, FROZEN 2026-10-10) — F1
leave-one-site-out (LOSO) consistency pins.

These tests validate the COMMITTED results JSON
(reports/phase141_results.json) for internal
consistency, so they pass in CI where the local store
(the script's inputs) does NOT exist. The recomputation
test skips cleanly when the inputs are absent
(Phase-133 pattern).

Frozen design pins (phase141-freeze.md, under spec
sec.5 and the Phase-139 freeze record sec.4):
Phase-136 machinery unchanged + stratum-drop parameter
only; the no-drop configuration must reproduce the
committed Phase-136 result exactly; subsets L-MD /
L-HA / L-KA; estimability per subset by the Phase-136
sec.5 rule; robustness criterion verbatim (every
estimable subset's MH OR > 1 with 95% CI excluding 1,
else the dropped site is LOAD-BEARING); raw p reported;
NO q-values (Q4(b)); no verdicts minted.
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
_RESULTS = _REPO / "reports" / "phase141_results.json"
_RESULTS136 = _REPO / "reports" / "phase136_results.json"
_SCRIPT = _REPO / "backend" / "scripts" / "phase141_loso.py"
_ANCHORS = _REPO / "backend" / "reports" / \
    "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8b"
    "e1f282c86ebb1fa3b602cfaed"
)
_LAYER = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")

_spec = importlib.util.spec_from_file_location(
    "phase141_loso", _SCRIPT)
phase141 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase141)


def _results():
    return json.loads(_RESULTS.read_text("utf-8"))


@pytest.fixture(scope="module")
def results():
    return _results()


# ---------------------------------------------------------------------------
# Pure-function unit tests (no local store)
# ---------------------------------------------------------------------------

def test_fisher_exact_known_tables():
    # Perfectly separated 2x2 with margins 10/10, 10/10:
    # only the two extreme tables are as or less probable;
    # p = 2 / C(20, 10).
    p = phase141.fisher_exact_two_sided(10, 0, 0, 10)
    assert abs(p - 2 / 184756) < 1e-12
    # A table at the exact centre of its margin class has
    # p = 1 (every table is at most as probable... the
    # observed table is the MOST probable, so all tables
    # count): [[5,5],[5,5]].
    assert phase141.fisher_exact_two_sided(5, 5, 5, 5) == 1.0


def test_estimability_rule():
    good = [{"a": 50, "b": 50, "c": 50, "d": 50},
            {"a": 40, "b": 60, "c": 30, "d": 70}]
    est = phase141.estimability(good)
    assert est["estimable"] is True
    # One stratum only -> NOT ESTIMABLE (>= 2 required).
    assert phase141.estimability(good[:1])["estimable"] is False
    # Tiny pooled counts -> expected < 5 in most cells.
    tiny = [{"a": 1, "b": 1, "c": 0, "d": 1},
            {"a": 0, "b": 1, "c": 1, "d": 0}]
    assert phase141.estimability(tiny)["estimable"] is False


def test_frozen_parameters():
    assert phase141.B_PERM == 9999
    assert phase141.SEED == 20261009
    assert phase141.DROP_LABELS == {
        "Mohenjo-daro": "L-MD", "Harappa": "L-HA",
        "Kalibangan": "L-KA"}


# ---------------------------------------------------------------------------
# Committed-results consistency pins
# ---------------------------------------------------------------------------

def test_anchors(results):
    assert results["anchors_sha256"] == _ANCHORS_SHA256
    assert hashlib.sha256(
        _ANCHORS.read_bytes()).hexdigest() == _ANCHORS_SHA256


def test_reproduction_reproduces_phase136_exactly(results):
    rep = results["reproduction_no_drop"]
    c136 = json.loads(_RESULTS136.read_text("utf-8"))
    assert rep["matches_committed_phase136_exactly"] is True
    assert rep["test"]["statistic_observed"] == \
        c136["test"]["statistic_observed"]
    assert rep["test"]["n_perm_ge_observed"] == \
        c136["test"]["n_perm_ge_observed"]
    assert rep["test"]["raw_p"] == c136["test"]["raw_p"]
    assert rep["effect_sizes"]["mh_common_odds_ratio"] == \
        c136["effect_sizes"]["mh_common_odds_ratio"]
    assert rep["effect_sizes"]["mh_ci95"] == \
        c136["effect_sizes"]["mh_ci95"]
    # Per-stratum tables equal the committed eligible tables.
    committed_tables = {s["site"]: s["table"]
                        for s in c136["strata"] if s["eligible"]}
    for row in rep["per_stratum"]:
        assert row["table"] == committed_tables[row["site"]]


def test_subset_strata_are_phase136_strata_minus_drop(results):
    c136 = json.loads(_RESULTS136.read_text("utf-8"))
    committed_tables = {s["site"]: s["table"]
                        for s in c136["strata"] if s["eligible"]}
    for label, drop in (("L-MD", "Mohenjo-daro"),
                        ("L-HA", "Harappa"),
                        ("L-KA", "Kalibangan")):
        cfg = results["subsets"][label]
        assert cfg["dropped_site"] == drop
        expected_sites = [s for s in
                          ("Mohenjo-daro", "Harappa", "Kalibangan")
                          if s != drop]
        assert cfg["strata_sites"] == expected_sites
        for row in cfg["per_stratum"]:
            assert row["table"] == committed_tables[row["site"]]
            assert row["fisher_exact_two_sided_p_descriptive"] \
                is not None


def test_no_q_values_anywhere(results):
    keys = set()

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(k)
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(results)
    assert "q_value" not in keys and "bh_q" not in keys
    assert "adjusted_p" not in keys and "q" not in keys
    assert "no q-values are computed" in \
        results["parameters"]["q_values"]


def test_robustness_outcome_matches_criterion(results):
    outcome = results["robustness_outcome"]
    load_bearing = []
    not_estimable = []
    for label, cfg in results["subsets"].items():
        if not cfg["estimability"]["estimable"]:
            not_estimable.append(label)
            continue
        fx = cfg["effect_sizes"]
        passes = (fx["mh_common_odds_ratio"] > 1
                  and fx["mh_ci95"][0] > 1)
        assert cfg["criterion_reading"]["passes"] == passes
        if not passes:
            load_bearing.append(cfg["dropped_site"])
    assert outcome["load_bearing_sites"] == load_bearing
    assert outcome["not_estimable_subsets"] == not_estimable
    assert outcome["stable"] == (not load_bearing
                                 and len(not_estimable) < 3)
    if load_bearing:
        for site in load_bearing:
            assert site in outcome["statement"]
            assert "LOAD-BEARING" in outcome["statement"]
    else:
        assert "STABLE" in outcome["statement"]


def test_graph_node_registered():
    sys.path.insert(0, str(_REPO / "backend"))
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase141Loso" in ATOMIC_NODES


# ---------------------------------------------------------------------------
# Recomputation (skips in CI — inputs live in the local store)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _LAYER.exists(),
                    reason="local-store inputs not present")
def test_recomputation_matches_committed(results, tmp_path):
    out = tmp_path / "phase141_recomputed.json"
    r = subprocess.run(
        [sys.executable, str(_SCRIPT), "--out", str(out)],
        capture_output=True, text=True, timeout=1800,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    assert recomputed["robustness_outcome"] == \
        results["robustness_outcome"]
    for label in ("L-MD", "L-HA", "L-KA"):
        assert recomputed["subsets"][label]["test"] == \
            results["subsets"][label]["test"]
        assert recomputed["subsets"][label]["effect_sizes"] == \
            results["subsets"][label]["effect_sizes"]
