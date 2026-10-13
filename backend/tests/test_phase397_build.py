"""Phase-397 (Spec 033) build-machinery fences.

Pins: (1) the frozen estimator (counted conditional model,
add-one smoothing, mean log probability per sign) reproduces
hand-computed values on synthetic fixtures, including a
multi-unit anchor expansion; (2) the value-to-units folding rule
reproduces every unit sequence frozen in the anchor record;
(3) every anchor-freeze sign is in the strict set as stamped,
the strict census is 287/94, and the random pool is the frozen
15 values; (4) the frozen verdict procedure maps score patterns
to verdicts exactly as claims F033-C10/C11/C12/C15 and plan
section 4 define them; (5) sequence construction applies the
V3 cleaning rules and the strict filter.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "backend" / "scripts"
sys.path.insert(0, str(REPO / "backend"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p397 = _load("phase397_sa_free_language_comparison")

FREEZE = json.loads(
    (REPO / "specs" / "033-sa-free-language-comparison"
     / "anchors-phase397.json").read_text("utf-8"))


def test_estimator_hand_computed():
    seqs = [["1", "2"], ["1", "2"]]
    score = p397.score_sequences(seqs, {"1": ["a"], "2": ["b"]})
    # P(a|BOS) = P(b|a) = (2+1)/(2+2); score per sequence = ln(3/4)
    assert abs(score - math.log(0.75)) < 1e-12


def test_estimator_multi_unit_expansion():
    seqs = [["1", "2"]]
    score = p397.score_sequences(seqs, {"1": ["a", "a"], "2": ["b"]})
    # units [a,a,b]: P(a|BOS)=2/3, P(a|a)=1/2, P(b|a)=1/2; /2 signs
    expected = (math.log(2 / 3) + math.log(0.5) + math.log(0.5)) / 2
    assert abs(score - expected) < 1e-12


def test_estimator_identity_mapping_matches():
    seqs = [["1", "2"], ["1", "2"]]
    assert abs(p397.score_sequences(seqs, {})
               - math.log(0.75)) < 1e-12


def test_fold_rule_reproduces_frozen_units():
    for entry in FREEZE["primary_list"]:
        for family in ("dravidian", "sanskrit", "munda"):
            got = p397.fold_value(entry[family]["value_as_published"])
            assert got == entry[family]["units"], (entry["sign"], family)
    for family in ("dravidian", "sanskrit", "munda"):
        for entry in FREEZE["robustness_lists"][family]["signs"]:
            got = p397.fold_value(entry["value_as_published"])
            assert got == entry["units"], (family, entry["sign"])


def test_anchor_freeze_signs_are_strict():
    strict, census = p397.load_strict_signs()
    assert census == {"anchors_total": 287, "strict": 94}
    for entry in FREEZE["primary_list"]:
        assert str(entry["sign"]) in strict
    for family in ("dravidian", "sanskrit", "munda"):
        for entry in FREEZE["robustness_lists"][family]["signs"]:
            assert str(entry["sign"]) in strict


def test_primary_order_and_random_pool():
    signs = [str(e["sign"]) for e in FREEZE["primary_list"]]
    assert signs == ["99", "87", "124", "60", "47"]
    pool = []
    for fam in ("dravidian", "sanskrit", "munda"):
        for e in FREEZE["primary_list"]:
            pool.append(e[fam]["units"])
    assert len(pool) == 15


def test_sequence_construction_rules():
    records = [["1", "000", "2", "*3", "x"], ["4"], ["5", "6", "4"]]
    strict = {"1", "2", "5", "6"}
    seqs = p397.build_sequences(records, strict)
    assert seqs == [["1", "2"], ["5", "6"]]


def test_verdict_procedure_frozen_rules():
    v, _ = p397.decide_verdict(0.0, 0.1, -5.0, False)
    assert v == "NOT SUPPORTED"          # rival at/above (C11)
    v, _ = p397.decide_verdict(1.0, 0.5, 1.2, False)
    assert v == "NOT SUPPORTED"          # inside random range (C11)
    v, _ = p397.decide_verdict(1.0, 0.95, 0.5, False)
    assert v == "INCONCLUSIVE"           # margin < 0.10 (C12)
    v, _ = p397.decide_verdict(1.0, 0.8, 0.5, True)
    assert v == "INCONCLUSIVE"           # sensitivity reversal (C12)
    v, _ = p397.decide_verdict(1.0, 0.8, 0.5, False)
    assert v == "SUPPORTED"              # both bars met (C10, C15)
    v, _ = p397.decide_verdict(1.0, 0.91, 0.5, False)
    assert v == "INCONCLUSIVE"           # margin 0.09, just below the bar


def test_percentile_helpers():
    s = [float(i) for i in range(100)]
    assert p397.percentile_rank(s, 50.0) == 50.0
    assert abs(p397.percentile_value(s, 99) - 98.01) < 1e-9
    assert p397.percentile_value(s, 50) == 49.5
