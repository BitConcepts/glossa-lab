"""Unit tests for the Phase-118 (spec 017) battery machinery.

Toy controls mirror the Phase-117 fixture: a synthetic sign
whose reading fits the core's junction + positional fabric
must VALIDATE (W1 PASS and cross-fit W3 PASS); an incoherent
one must DEMOTE (W3 FAIL in both cross-fit directions). The
partition and set tests pin spec 017 sections 2-3 against the
real frozen data; the judgeability test recomputes J94/JKUR
on the real inputs and asserts the frozen counts of section
2.1 (67 / 29).
"""
import json
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.phase113_battery import (  # noqa: E402
    FAIL, INDETERMINATE, PASS, CorpusContext,
)
from glossa_lab.phase113_run import compute_sets  # noqa: E402
from glossa_lab.phase117_run import load_holdat_with_sites  # noqa: E402
from glossa_lab.phase118_battery import (  # noqa: E402
    build_partition, decide, donor_pool, evaluate_anchor,
    percentile, phonemes_of, site_profiles,
    test_w1 as battery_test_w1, test_w3x as battery_test_w3x,
    w3x_self_score,
)

_REPO = Path(__file__).resolve().parent.parent.parent
_HOLDAT = _REPO / "corpora" / "downloads" / "external_repos" \
    / "holdatllc_indus" / "indus_corpus 2.csv"
_MAIN_HOLDAT = Path.home() / "workspace" / "glossa-lab" / "corpora" \
    / "downloads" / "external_repos" / "holdatllc_indus" \
    / "indus_corpus 2.csv"


def _holdat_path():
    for cand in (_HOLDAT, _MAIN_HOLDAT):
        if cand.exists():
            return cand
    return None


def test_phonemes():
    assert phonemes_of("ka") == ("k", "a")
    assert phonemes_of("nal") == ("n", "l")
    assert phonemes_of("vēḷ") == ("v", "ḷ")
    assert phonemes_of("") is None
    assert phonemes_of("M293") is None


def test_percentile_type7():
    vals = [float(i) for i in range(11)]  # 0..10
    assert percentile(vals, 10) == pytest.approx(1.0)
    assert percentile(vals, 50) == pytest.approx(5.0)
    assert percentile([3.0], 10) == 3.0


def test_decide_w1_primary_rule():
    cases = [
        # (w1, w3, w4) -> outcome; W1 PASS and W3 PASS are BOTH
        # mandatory; W4's PASS cannot substitute for W1's.
        ((PASS, PASS, PASS), "VALIDATED"),
        ((PASS, PASS, INDETERMINATE), "VALIDATED"),
        ((PASS, PASS, FAIL), "DEMOTE"),
        ((INDETERMINATE, PASS, PASS), "UNRESOLVED"),
        ((PASS, INDETERMINATE, PASS), "UNRESOLVED"),
        ((INDETERMINATE, INDETERMINATE, INDETERMINATE), "UNRESOLVED"),
        ((FAIL, PASS, PASS), "DEMOTE"),
        ((PASS, FAIL, INDETERMINATE), "DEMOTE"),
        ((INDETERMINATE, FAIL, INDETERMINATE), "DEMOTE"),
        ((INDETERMINATE, INDETERMINATE, FAIL), "DEMOTE"),
    ]
    for states, want in cases:
        assert decide(*states) == want, states


def _toy():
    """Synthetic world: core signs A 'ka', B 'nal', C 'ta'; the
    junction fabric makes (a -> n) and (a -> t) the coherent
    pairs. Candidate X 'na' continues the fabric; candidate Y
    'li' contradicts it. Two disjoint halves carry identical
    pattern proportions (cross-fit directions see the same
    fabric); donor self-pairs sit in both halves so donor
    token counts land in the frozen band."""
    pattern = (
        [["A", "B"] for _ in range(15)]
        + [["A", "C"] for _ in range(10)]
        + [["C", "B"] for _ in range(15)]
        + [["A", "X"] for _ in range(10)]
        + [["C", "X"] for _ in range(5)]
        + [["X", "B"] for _ in range(10)]
        + [["X", "C"] for _ in range(5)]
        + [["A", "Y"] for _ in range(10)]
        + [["C", "Y"] for _ in range(5)]
        + [["Y", "B"] for _ in range(10)]
        + [["Y", "C"] for _ in range(5)]
        + [[f"D{i}", f"D{i}"] for i in range(1, 5)
           for _ in range(15)]
    )
    ins_a = [list(t) for t in pattern]
    ins_b = [list(t) for t in pattern]
    full = ins_a + ins_b
    readings = {"A": "ka", "B": "nal", "C": "ta",
                "X": "na", "Y": "li",
                "D1": "lu", "D2": "ri", "D3": "vu", "D4": "mi"}
    phon = {s: phonemes_of(r) for s, r in readings.items()}
    ctx_full = CorpusContext(full)
    core = {"A", "B", "C"}
    phi = {}
    for name, mi, si in (("modelA_scoreB", ins_a, ins_b),
                         ("modelB_scoreA", ins_b, ins_a)):
        scores = [w3x_self_score(t, mi, si, core - {t}, phon)
                  for t in sorted(core)]
        phi[name] = percentile(
            [s for s in scores if s is not None], 10)
    return {
        "ins_a": ins_a, "ins_b": ins_b, "full": full,
        "readings": readings, "phon": phon,
        "ctx_full": ctx_full,
        "ctx_a": CorpusContext(ins_a),
        "ctx_b": CorpusContext(ins_b),
        "ins_sites": [(t, "S1") for t in full],
        "profiles": site_profiles([(t, "S1") for t in full]),
        "counts": dict(ctx_full.token_counts),
        "anchors": sorted(readings),
        "core": core, "phi": phi,
    }


def _evaluate_toy(toy, sign):
    return evaluate_anchor(
        sign, toy["readings"][sign], toy["core"], toy["phon"],
        toy["readings"], toy["ins_a"], toy["ins_b"],
        toy["ins_sites"], toy["ctx_full"], toy["ctx_a"],
        toy["ctx_b"], toy["profiles"], toy["counts"],
        toy["anchors"], toy["phi"], random.Random(118))


def test_toy_coherent_sign_validates():
    toy = _toy()
    res = _evaluate_toy(toy, "X")
    assert res["w1"]["state"] == PASS
    assert res["w3"]["state"] == PASS
    for d in res["w3"]["directions"].values():
        assert d["state"] == PASS
        assert d["score"] >= d["phi"]
        assert d["p_value"] <= 0.50
    assert res["outcome"] == "VALIDATED"


def test_toy_incoherent_sign_demotes():
    toy = _toy()
    res = _evaluate_toy(toy, "Y")
    for d in res["w3"]["directions"].values():
        assert d["state"] == FAIL
        assert d["score"] < d["phi"]
        assert d["p_value"] >= 0.50
    assert res["w3"]["state"] == FAIL
    assert res["outcome"] == "DEMOTE"


def test_w1_direction_below_floor_is_indeterminate():
    toy = _toy()
    # Z appears once on half B: the modelA_scoreB direction
    # cannot judge it.
    ins_a = toy["ins_a"] + [["A", "Z"] for _ in range(8)]
    ins_b = toy["ins_b"] + [["A", "Z"]]
    res = battery_test_w1("Z", CorpusContext(ins_a), CorpusContext(ins_b),
                  toy["core"])
    d = res["directions"]["modelA_scoreB"]
    assert d["state"] == INDETERMINATE
    assert d["reason"] == "half_count_below_floor"
    assert res["state"] != PASS


def test_w3x_direction_below_junction_floor():
    toy = _toy()
    readings = dict(toy["readings"])
    readings["Z"] = "za"
    phon = dict(toy["phon"])
    phon["Z"] = phonemes_of("za")
    ins_a = toy["ins_a"] + [["A", "Z"] for _ in range(6)]
    ins_b = toy["ins_b"] + [["A", "Z"]]  # one junction on B
    full = ins_a + ins_b
    counts = dict(CorpusContext(full).token_counts)
    res = battery_test_w3x("Z", "za", ins_a, ins_b, toy["core"], phon,
                   readings, CorpusContext(full), counts,
                   sorted(readings), toy["phi"], random.Random(118))
    d = res["directions"]["modelA_scoreB"]
    assert d["state"] == INDETERMINATE
    assert d["reason"] == "junction_floor_half"
    assert res["state"] != PASS


def test_w3x_donor_band_empty_is_indeterminate():
    # S is junction-scorable in both directions, but every
    # other anchor sits far outside [ceil(6/3), 18].
    big = [["A", "B"] for _ in range(60)] \
        + [["B", "C"] for _ in range(60)]
    ins_a = big + [["A", "S"] for _ in range(3)]
    ins_b = big + [["A", "S"] for _ in range(3)]
    full = ins_a + ins_b
    readings = {"A": "ka", "B": "nal", "C": "ta", "S": "sa"}
    phon = {s: phonemes_of(r) for s, r in readings.items()}
    counts = dict(CorpusContext(full).token_counts)
    assert donor_pool("S", counts, sorted(readings)) == []
    res = battery_test_w3x("S", "sa", ins_a, ins_b, {"A", "B", "C"}, phon,
                   readings, CorpusContext(full), counts,
                   sorted(readings),
                   {"modelA_scoreB": -2.0, "modelB_scoreA": -2.0},
                   random.Random(118))
    for d in res["directions"].values():
        assert d["state"] == INDETERMINATE
        assert d["reason"] == "donor_band_empty"
    assert res["state"] == INDETERMINATE


def test_w3x_donor_pool_band():
    counts = {"S": 12, "T1": 4, "T2": 36, "T3": 3, "T4": 37,
              "T5": 12}
    assert donor_pool("S", counts, sorted(counts)) == ["T1", "T2", "T5"]


@pytest.mark.skipif(_holdat_path() is None,
                    reason="Holdat CSV not available")
def test_real_partition_totals():
    ins_sites = load_holdat_with_sites(_holdat_path())
    assert sum(len(t) for t, _ in ins_sites) == 7002
    half = build_partition(ins_sites)
    toks = {"A": 0, "B": 0}
    for (toks_list, _), h in zip(ins_sites, half):
        toks[h] += len(toks_list)
    assert toks == {"A": 3531, "B": 3471}


@pytest.mark.skipif(_holdat_path() is None,
                    reason="Holdat CSV not available")
def test_real_sets_and_judgeability():
    from glossa_lab.phase118_run import (
        BatteryInputs, compute_judgeability,
    )
    anchors = json.loads(
        (_REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json")
        .read_text("utf-8"))["anchors"]
    register = json.loads(
        (_REPO / "reports" / "phase108_provenance_register.json")
        .read_text("utf-8"))
    sets = compute_sets(anchors, register)
    assert len(sets["flagged44"]) == 44
    assert len(sets["strict94"]) == 94
    assert len(sets["kur113"]) == 113
    inputs = BatteryInputs(anchors)
    judge = compute_judgeability(inputs, sets)
    assert judge["counts"] == {"J94": 67, "JKUR": 29}
    # The three by-construction signs (spec section 5) are
    # judgeable by no instrument: not W1-scorable (a half below
    # 4 tokens) and not W3-scorable (a direction below 2
    # junction observations) — Appendix A.2 counts.
    from glossa_lab.phase118_battery import w3x_scorable
    strict = set(sets["strict94"])
    for s in ("M235", "M254", "M402"):
        assert not (inputs.ctx_a.token_count(s) >= 4
                    and inputs.ctx_b.token_count(s) >= 4)
        assert not w3x_scorable(s, inputs.ins_a, inputs.ins_b,
                                strict, inputs.holdat_counts,
                                inputs.anchor_signs)


def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase118WithinCompilationValidation" in ATOMIC_NODES
