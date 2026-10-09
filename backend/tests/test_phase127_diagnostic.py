"""Unit tests for the Phase-127 (spec 021) cross-compilation
disagreement diagnostic machinery.

Toy controls: class-label pools / profiles on hand-computed
inputs; split-half and matched-size nulls on degenerate pools
(exact values) plus determinism under the frozen seeds;
inscription bootstrap on identical toy compilations (all TVs
exactly 0); neighbourhood decomposition on synthetic
crosswalk rows (ambiguity share and attributable TV
hand-computed); composition-control evaluation on toy
contexts; power-grid machinery on a toy pool. Real-input
pins: the judgeable set is exactly Phase-125's 16 PRIMARY
pairs and the observed median TV of record is 0.636931;
the H23 graph registration is present. This phase issues
no verdict, and no test here applies one.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.phase113_battery import CorpusContext, positional_counts  # noqa: E402
from glossa_lab.phase127_diagnostic import (  # noqa: E402
    INITIAL, MEDIAL, TERMINAL, bootstrap_arm, class_labels,
    evaluate_pairs_on_contexts, inscription_count_vectors,
    matched_size_arm, neighbourhood_decomposition, power_grid,
    profile_from_labels, split_half_arm, split_half_replicates,
    subsample_remainder_tv, summary, tv_from_labels,
)
import random  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent.parent
_P125 = _REPO / "reports" / "phase125_cross_compilation_results.json"


# ── Pools / profiles ──────────────────────────────────────

def test_class_labels_convention():
    ins = [["A", "B", "C"], ["A", "B"], ["A"]]
    # A: initial (multi-sign), initial, sole-token medial
    assert class_labels(ins, "A") == [INITIAL, INITIAL, MEDIAL]
    # B: medial, terminal
    assert class_labels(ins, "B") == [MEDIAL, TERMINAL]
    assert class_labels(ins, "Z") == []


def test_class_labels_match_positional_counts():
    ins = [["X", "A", "Y", "A"], ["A"], ["B", "A", "B"]]
    labels = class_labels(ins, "A")
    counts = positional_counts(ins, "A")
    assert (labels.count(INITIAL), labels.count(MEDIAL),
            labels.count(TERMINAL)) == counts


def test_profile_and_tv_from_labels():
    assert profile_from_labels([]) is None
    assert profile_from_labels([INITIAL, MEDIAL]) == (0.5, 0.5, 0.0)
    assert tv_from_labels([INITIAL], [TERMINAL]) == 1.0
    assert tv_from_labels([INITIAL, MEDIAL], [INITIAL, MEDIAL]) == 0.0
    assert tv_from_labels([], [INITIAL]) is None


def test_summary_interval():
    s = summary([0.0, 1.0])
    assert s["median"] == 0.5 and s["n_replicates"] == 2
    assert summary([])["median"] is None


# ── Arm (a): split-half ───────────────────────────────────

def test_split_half_degenerate_pool_is_zero():
    rng = random.Random(127001)
    reps = split_half_replicates([MEDIAL] * 20, rng, b=25)
    assert reps == [0.0] * 25


def test_split_half_determinism_and_fullsize_scaling():
    pools = {"S1": [INITIAL] * 10 + [MEDIAL] * 20 + [TERMINAL] * 10}
    out1 = split_half_arm(pools, b=50)
    out2 = split_half_arm(pools, b=50)
    assert out1 == out2
    floor = out1["noise_floor_median_tv"]
    assert floor is not None and 0.0 < floor < 0.6
    # registered full-size estimate is floor / sqrt(2)
    import math
    assert out1["noise_floor_fullsize_est"] == pytest.approx(
        floor / math.sqrt(2), abs=1e-6)


def test_split_half_tiny_pool():
    assert split_half_replicates([INITIAL], random.Random(1), b=5) == []


# ── Arm (b): matched-size ─────────────────────────────────

def test_subsample_remainder_edges():
    rng = random.Random(3)
    assert subsample_remainder_tv([INITIAL] * 5, 5, rng) == (None, None)
    assert subsample_remainder_tv([INITIAL] * 5, 0, rng) == (None, None)
    tv_rem, tv_full = subsample_remainder_tv([MEDIAL] * 10, 4, rng)
    assert tv_rem == 0.0 and tv_full == 0.0


def test_matched_size_degenerate_and_deterministic():
    pools = {"S1": [INITIAL] * 30 + [TERMINAL] * 30}
    sizes = {"S1": 10}
    out1 = matched_size_arm(pools, sizes, b=40)
    out2 = matched_size_arm(pools, sizes, b=40)
    assert out1 == out2
    dist = out1["median_tv_distribution"]
    assert dist["median"] is not None and 0.0 <= dist["median"] <= 1.0
    assert dist["observed_median_tv"] == 0.636931
    per = out1["per_sign"]["S1"]
    assert per["n_tokens"] == 60 and per["target_size"] == 10
    assert per["n_skipped_replicates"] == 0


# ── Arm (c): bootstrap ────────────────────────────────────

def test_inscription_count_vectors():
    ins = [["A", "B"], ["A"]]
    vecs = inscription_count_vectors(ins, ["A", "B"])
    assert vecs[0]["A"] == (1, 0, 0)
    assert vecs[0]["B"] == (0, 0, 1)
    assert vecs[1]["A"] == (0, 1, 0)  # sole token is MEDIAL
    assert "B" not in vecs[1]


def test_bootstrap_identical_compilations_zero_tv():
    # Degenerate control: every inscription identical, so every
    # resample of either compilation gives A the same profile
    # (1, 0, 0) and TV is exactly 0 in every replicate. (Two
    # *independent* resamples of a varied corpus would NOT give
    # TV 0 — that difference is exactly what the bootstrap
    # prices.)
    ins = [["A", "B"] for _ in range(6)]
    vecs = inscription_count_vectors(ins, ["A"])
    out = bootstrap_arm(vecs, vecs, [("A", "A")], b=30)
    assert out["per_pair"]["A-A"]["median"] == 0.0
    assert out["median_tv"]["median"] == 0.0
    assert out["per_pair"]["A-A"]["n_excluded_replicates"] == 0


def test_bootstrap_determinism():
    ins_m = [["A", "B"], ["B", "A", "B"]]
    ins_h = [["A", "A", "B"], ["B"]]
    vm = inscription_count_vectors(ins_m, ["A"])
    vh = inscription_count_vectors(ins_h, ["A"])
    assert bootstrap_arm(vm, vh, [("A", "A")], b=20) == \
        bootstrap_arm(vm, vh, [("A", "A")], b=20)


# ── Arm (d): neighbourhood decomposition ──────────────────

def test_neighbourhood_decomposition_hand_computed():
    rows = [
        {"parpola_id": "P1", "mahadevan_id": "M1"},
        {"parpola_id": "P1", "mahadevan_id": "M2"},
        {"parpola_id": "P3", "mahadevan_id": "M1"},
        {"parpola_id": "P9", "mahadevan_id": "M9"},
    ]
    tvs = {("P1", "M1"): 0.8, ("P1", "M2"): 0.4, ("P3", "M1"): None}
    out = neighbourhood_decomposition(
        rows, {"parpola_id": "P1", "mahadevan_id": "M1"},
        lambda p, m: tvs.get((p, m)))
    assert out["k_p_rows"] == 2 and out["k_m_rows"] == 2
    assert out["neighbourhood_size"] == 3
    assert out["ambiguity_share"] == pytest.approx(2 / 3, abs=1e-6)
    # only (P1, M2) is a judgeable neighbourhood comparison
    assert out["n_neighbourhood_judgeable"] == 1
    assert out["neighbourhood_median_tv"] == pytest.approx(0.4)
    assert out["attributable_tv"] == pytest.approx(0.8 - 0.4)
    assert out["attributable_share"] == pytest.approx(0.5)


def test_neighbourhood_unambiguous_pair():
    rows = [{"parpola_id": "P1", "mahadevan_id": "M1"},
            {"parpola_id": "P2", "mahadevan_id": "M2"}]
    out = neighbourhood_decomposition(
        rows, {"parpola_id": "P1", "mahadevan_id": "M1"},
        lambda p, m: 0.3)
    assert out["ambiguity_share"] == 0.0
    assert out["neighbourhood_median_tv"] is None
    assert out["attributable_tv"] is None


# ── Arm (e): composition evaluation ───────────────────────

def test_evaluate_pairs_on_contexts_floor():
    mayig = CorpusContext([["P1", "X"] * 1 for _ in range(8)])
    holdat_full = CorpusContext([["M1", "Y"] for _ in range(8)])
    holdat_thin = CorpusContext([["M1", "Y"] for _ in range(3)])
    pairs = [{"parpola_id": "P1", "mahadevan_id": "M1"}]
    ev_full = evaluate_pairs_on_contexts(pairs, mayig, holdat_full)
    assert ev_full["n_judgeable"] == 1
    assert ev_full["records"][0]["tv"] == 0.0
    ev_thin = evaluate_pairs_on_contexts(pairs, mayig, holdat_thin)
    assert ev_thin["n_judgeable"] == 0  # restricted count below floor 8
    assert ev_thin["median_tv"] is None


# ── Arm (f): power grid ───────────────────────────────────

def test_power_grid_toy():
    pools = {"S1": [INITIAL] * 40 + [MEDIAL] * 40 + [TERMINAL] * 40}
    out = power_grid(pools, b=20, grid=(8, 32))
    assert [g["tokens_per_sign"] for g in out["grid"]] == [8, 32]
    # noise decreases with size: p95 at 32 <= p95 at 8 (degenerate-safe)
    assert out["grid"][1]["pooled_per_sign_tv_p95"] <= \
        out["grid"][0]["pooled_per_sign_tv_p95"] + 1e-9
    assert out["pass_bound"] == 0.35


# ── Real-input pins + H23 registration ────────────────────

def test_phase125_record_pins():
    p125 = json.loads(_P125.read_text(encoding="utf-8"))
    assert p125["verdict"]["verdict"] == "FAIL"
    stats = p125["arms"]["primary"]["stats"]
    assert stats["n_judgeable"] == 16
    assert stats["median_tv"] == 0.636931
    judged = [r for r in p125["arms"]["primary"]["records"] if r["judgeable"]]
    assert len(judged) == 16
    # primary pairs are unique on both sides (unambiguous by construction)
    assert len({r["parpola_id"] for r in judged}) == 16
    assert len({r["mahadevan_id"] for r in judged}) == 16


def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase127CrossCompilationDiagnostic" in ATOMIC_NODES
