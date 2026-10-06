"""Unit tests for the Phase-107 SA validation harness (spec 005)."""
from __future__ import annotations

import math
import random

import pytest

from glossa_lab.pipelines import sa_validation as sv


# ── gold extraction ──────────────────────────────────────────────────────

def test_gold_high_syllabic_precedence():
    anchors = {"M006": {"confidence": "HIGH", "reading": "puli"}}
    gold = sv.extract_gold(anchors, ["ka", "ko", "pu", "ya"])
    assert gold["M006"] == "pu"  # HIGH_SYLLABIC, not 'pu' from 'puli' by luck


def test_gold_medium_normalisation_and_fallback():
    anchors = {
        "M100": {"confidence": "MEDIUM", "reading": "Kal/ir"},   # -> 'kal' -> prefix 'ka'
        "M101": {"confidence": "MEDIUM", "reading": "zz top"},   # no vocab match
        "M102": {"confidence": "LOW", "reading": "ka"},          # excluded
        "M103": {"confidence": "HIGH", "reading": ""},           # no reading
    }
    gold = sv.extract_gold(anchors, ["ka", "ki"])
    assert gold["M100"] == "ka"
    assert gold["M101"] is None
    assert "M102" not in gold
    assert gold["M103"] is None


# ── folds ────────────────────────────────────────────────────────────────

def test_folds_disjoint_and_cover():
    pins = {f"M{i:03d}": "ka" for i in range(50)}
    anchors = {s: {"confidence": "HIGH" if i < 20 else "MEDIUM"}
               for i, s in enumerate(sorted(pins))}
    folds = sv.make_folds(pins, anchors, k=5, seed=107)
    flat = [s for f in folds for s in f]
    assert sorted(flat) == sorted(pins)
    assert len(flat) == len(set(flat)) == 50
    # stratified: every fold holds both confidences
    for f in folds:
        confs = {anchors[s]["confidence"] for s in f}
        assert confs == {"HIGH", "MEDIUM"}


def test_pin_budget_priority():
    pins = {"M006": "pu", "M500": "ka", "M501": "ki"}
    flat = ["M500"] * 10 + ["M501"] * 5 + ["M006"]
    sel = sv.select_pin_budget(pins, 2, flat)
    assert set(sel) == {"M006", "M500"}  # HIGH_SYLLABIC first, then frequency


# ── scrambled LM ─────────────────────────────────────────────────────────

def test_scramble_preserves_probability_multiset():
    prob = {("ka", "ki"): 0.5, ("ki", "ka"): 0.3, ("ka", "ka"): 0.2}
    vocab = ["ka", "ki"]
    sp, svoc = sv.scramble_lm(prob, vocab, seed=3)
    assert sorted(sp.values()) == sorted(prob.values())
    assert svoc == vocab
    assert set(sp) != set(prob) or len(vocab) < 2  # labels actually moved (2-vocab swap)


# ── objective terms on a toy corpus ──────────────────────────────────────

TOY_INSC = [["A", "B"], ["A", "C", "B"], ["D", "A"]]
TOY_FLAT = [s for insc in TOY_INSC for s in insc]
TOY_PROB = {("wa", "xa"): 0.4, ("xa", "wa"): 0.3, ("wa", "ya"): 0.2, ("ya", "za"): 0.1}


def _toy_objective(terms=(), logp=None):
    return sv.Objective(TOY_PROB, TOY_FLAT, TOY_INSC, terms=terms,
                        positional_logp=logp)


def test_phono_penalty_counts_initial_inscriptions():
    obj = _toy_objective(terms=("phono",))
    # A is initial in 2 inscriptions, D in 1; 'xa'/'wa' have invalid
    # initials ('x'/'w' in Phase-61 PD_INVALID_INITIALS); 'ya' is valid.
    mapping = {"A": "xa", "B": "wa", "C": "ya", "D": "wa"}
    assert obj.phono_penalty(mapping) == 3
    mapping["A"] = "ya"
    mapping["D"] = "ya"
    assert obj.phono_penalty(mapping) == 0


def test_harmony_penalty_front_back_mix():
    prob = {("ki", "ku"): 0.4, ("ku", "ka"): 0.3, ("ka", "ki"): 0.3}
    obj = sv.Objective(prob, TOY_FLAT, TOY_INSC, terms=("harmony",))
    # 'ki' front, 'ku' back, 'ka' neutral: insc 1 (ki,ku) mixes; insc 2
    # (ki,ka,ku) mixes; insc 3 (ka,ki) front-only -> no violation.
    mapping = {"A": "ki", "B": "ku", "C": "ka", "D": "ka"}
    assert obj.harmony_penalty(mapping) == 2


def test_positional_profile_normalises():
    logp = sv.build_positional_logp({"A": "wa"}, TOY_FLAT, TOY_INSC, ["wa", "xa"])
    for k in range(3):
        s = sum(math.exp(logp[v][k]) for v in ("wa", "xa"))
        assert s == pytest.approx(1.0)


# ── delta scorer equivalence on the toy corpus ───────────────────────────

def test_delta_swap_matches_total_difference():
    logp = sv.build_positional_logp({"A": "wa", "B": "xa"}, TOY_FLAT, TOY_INSC,
                                    ["wa", "xa", "ya", "za"])
    obj = _toy_objective(terms=("phono", "harmony", "positional"), logp=logp)
    delta = sv.DeltaObjective(obj, TOY_INSC)
    rng = random.Random(0)
    signs = ["A", "B", "C", "D"]
    vals = ["wa", "xa", "ya", "za"]
    for _ in range(60):
        mapping = {s: rng.choice(vals) for s in signs}
        delta.set_mapping(mapping)
        before = delta.total()
        ci, cj = rng.sample(range(4), 2)
        d = delta.delta_swap(ci, cj)
        delta.apply_swap(ci, cj)
        after = delta.total()
        assert after - before == pytest.approx(d, abs=1e-6)


def test_delta_total_close_to_objective_score():
    logp = sv.build_positional_logp({"A": "wa"}, TOY_FLAT, TOY_INSC,
                                    ["wa", "xa", "ya", "za"])
    obj = _toy_objective(terms=("phono", "harmony", "positional"), logp=logp)
    delta = sv.DeltaObjective(obj, TOY_INSC)
    mapping = {"A": "wa", "B": "xa", "C": "ya", "D": "za"}
    delta.set_mapping(mapping)
    # float32 (BigramScorer) vs float64 (delta) summation noise only
    assert delta.total() == pytest.approx(obj.score(mapping), rel=1e-4)
