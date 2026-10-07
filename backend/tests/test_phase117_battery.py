"""Tests for Phase-117 (spec 016) within-compilation battery.

Covers: the frozen partition on the real Holdat corpus (seed
117; halves asserted at A = 3,531 / B = 3,471 tokens, with
Appendix A.5 per-sign spot counts), W1 direction state machine
and combination rule, W3 junction floor / donor-band guard /
score machinery, phi percentile, W4 strata rules, the section-8
decision rule, set recomputation against the real repo files
(44 / 94 / 113), graph registration (H23), and toy end-to-end
controls (a synthetic core-coherent reading validates; a
synthetic incoherent reading does not).
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from glossa_lab.phase113_battery import CorpusContext
from glossa_lab.phase113_run import compute_sets
from glossa_lab.phase117_battery import (
    FAIL, INDETERMINATE, PASS, build_partition, decide,
    evaluate_anchor, percentile, phonemes_of, site_profiles,
    w3_self_score,
)
from glossa_lab.phase117_battery import test_w1 as battery_w1
from glossa_lab.phase117_battery import test_w3 as battery_w3
from glossa_lab.phase117_battery import test_w4 as battery_w4

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent


def _holdat_csv():
    rel = Path("corpora/downloads/external_repos/holdatllc_indus/"
               "indus_corpus 2.csv")
    for cand in (REPO / rel, Path.home() / "workspace/glossa-lab" / rel):
        if cand.exists():
            return cand
    return None


# ── Phonemes / percentile ──────────────────────────────────────

def test_phonemes_of():
    assert phonemes_of("ka") == ("k", "a")
    assert phonemes_of("nal") == ("n", "l")
    assert phonemes_of("ai") == ("ai", "ai")
    assert phonemes_of("kaḷiṟu") == ("k", "u")


def test_percentile_type7():
    assert percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == \
        pytest.approx(1.9)
    assert percentile([5.0], 10) == 5.0
    assert percentile([1.0, 3.0], 10) == pytest.approx(1.2)


# ── Decision rule (spec section 8) ─────────────────────────────

@pytest.mark.parametrize("w1,w3,w4,out", [
    (PASS, PASS, PASS, "VALIDATED"),
    (PASS, PASS, INDETERMINATE, "VALIDATED"),
    (INDETERMINATE, PASS, PASS, "VALIDATED"),
    (INDETERMINATE, PASS, INDETERMINATE, "UNRESOLVED"),
    (PASS, INDETERMINATE, PASS, "UNRESOLVED"),
    (INDETERMINATE, INDETERMINATE, INDETERMINATE, "UNRESOLVED"),
    (FAIL, PASS, PASS, "DEMOTE"),
    (PASS, FAIL, PASS, "DEMOTE"),
    (PASS, PASS, FAIL, "DEMOTE"),
])
def test_decide(w1, w3, w4, out):
    assert decide(w1, w3, w4) == out


# ── W1 state machine ───────────────────────────────────────────

def test_w1_direction_below_floor():
    ctx_a = CorpusContext([["S", "A"]] * 6 + [["A", "B"]] * 6)
    ctx_b = CorpusContext([["S", "A"]] * 3 + [["A", "B"]] * 6)
    out = battery_w1("S", ctx_a, ctx_b, {"A", "B"})
    # Scoring on B: S has 3 tokens < 4 -> that direction is
    # INDETERMINATE; W1 cannot PASS.
    assert out["directions"]["modelA_scoreB"]["state"] == INDETERMINATE
    assert out["directions"]["modelA_scoreB"]["reason"] == \
        "half_count_below_floor"
    assert out["state"] != PASS


def test_w1_centroid_undefined():
    # Core signs are INITIAL- or TERMINAL-modal only; S is
    # MEDIAL-modal on the scoring half -> no centroid exists.
    half = ([["A", "B"]] * 8 + [["X", "S", "B"]] * 6)
    ctx_a, ctx_b = CorpusContext(half), CorpusContext(half)
    out = battery_w1("S", ctx_a, ctx_b, {"A", "B", "X"})
    assert out["directions"]["modelA_scoreB"]["reason"] == \
        "centroid_undefined"
    assert out["state"] == INDETERMINATE


# ── W3 guards ──────────────────────────────────────────────────

def _w3_world(sign_ins, anchors_extra=None):
    ins = ([["A", "B"]] * 30 + [["A", "C"]] * 20 + [["C", "B"]] * 30
           + sign_ins)
    anchors = {"A": "ka", "B": "nal", "C": "ta"}
    if anchors_extra:
        anchors.update(anchors_extra)
    phon = {s: phonemes_of(r) for s, r in anchors.items()}
    ctx = CorpusContext(ins)
    counts = dict(ctx.token_counts)
    return ins, anchors, phon, ctx, counts


def test_w3_junction_floor():
    ins, anchors, phon, ctx, counts = _w3_world(
        [["A", "S"]] * 3 + [["S", "B"]] * 2, {"S": "na"})  # n_j = 5
    out = battery_w3("S", "na", ins, {"A", "B", "C"}, phon, anchors,
                  ctx, counts, sorted(anchors), phi=-3.0,
                  rng=random.Random(117))
    assert out["state"] == INDETERMINATE
    assert out["reason"] == "junction_floor"
    assert out["n_junctions"] == 5


def test_w3_donor_band_empty():
    # S attested 6 times; every other anchored sign is far
    # outside the [ceil(6/3), 18] donor band.
    ins, anchors, phon, ctx, counts = _w3_world(
        [["A", "S"]] * 6, {"S": "na"})
    out = battery_w3("S", "na", ins, {"A", "B", "C"}, phon, anchors,
                  ctx, counts, sorted(anchors), phi=-3.0,
                  rng=random.Random(117))
    assert out["n_junctions"] == 6
    assert out["state"] == INDETERMINATE
    assert out["reason"] == "donor_band_empty"


# ── W4 strata rules ────────────────────────────────────────────

def _profiles(rows):
    return site_profiles([(toks, site) for toks, site in rows])


def test_w4_pass_same_modal_low_tv():
    rows = ([(["S", "A"], "X1")] * 6 + [(["S", "A"], "X2")] * 5
            + [(["A", "B"], "X1")] * 4)
    out = battery_w4("S", _profiles(rows))
    assert out["state"] == PASS


def test_w4_fail_modal_flip_at_attestation():
    rows = ([(["S", "A"], "X1")] * 8 + [(["A", "S"], "X2")] * 8)
    out = battery_w4("S", _profiles(rows))
    assert out["state"] == FAIL


def test_w4_indeterminate_thin_disagreement():
    rows = ([(["S", "A"], "X1")] * 5 + [(["A", "S"], "X2")] * 5)
    out = battery_w4("S", _profiles(rows))
    assert out["state"] == INDETERMINATE
    assert out["reason"] == "modal_disagreement_below_fail_bar"


def test_w4_indeterminate_single_stratum():
    out = battery_w4("S", _profiles([(["S", "A"], "X1")] * 9))
    assert out["state"] == INDETERMINATE
    assert out["reason"] == "strata_below_two"


# ── Toy end-to-end controls (spec section 11 step 2) ───────────

def _toy():
    """Core A 'ka' (initial-leaning), B 'nal' (terminal), C 'ta';
    candidate X 'na' sits in the core's favored junctions
    (final a -> initial n/t) with an initial-consistent profile;
    candidate Y 'li' sits in identical positions with phonemes
    the junction model never predicts."""
    half = ([["A", "B"]] * 15 + [["A", "C"]] * 10 + [["C", "B"]] * 15
            + [["A", "X"]] * 10 + [["C", "X"]] * 5
            + [["X", "B"]] * 10 + [["X", "C"]] * 5
            + [["A", "Y"]] * 10 + [["C", "Y"]] * 5
            + [["Y", "B"]] * 10 + [["Y", "C"]] * 5)
    donor_ins = [[f"D{i}", f"D{i}"] for i in range(1, 5)
                 for _ in range(30)]
    full = half * 2 + donor_ins
    anchors = {"A": "ka", "B": "nal", "C": "ta", "X": "na",
               "Y": "li", "D1": "lu", "D2": "ri", "D3": "vu",
               "D4": "mi"}
    phon = {s: phonemes_of(r) for s, r in anchors.items()}
    ctx_full = CorpusContext(full)
    ctx_a, ctx_b = CorpusContext(half), CorpusContext(half)
    ins_sites = [(t, "S1") for t in full]
    core = {"A", "B", "C"}
    scores = [w3_self_score(s, full, core - {s}, phon) for s in core]
    phi = percentile([s for s in scores if s is not None], 10)
    return {"anchors": anchors, "phon": phon, "full": full,
            "ins_sites": ins_sites, "ctx_full": ctx_full,
            "ctx_a": ctx_a, "ctx_b": ctx_b,
            "profiles": site_profiles(ins_sites),
            "counts": dict(ctx_full.token_counts), "core": core,
            "phi": phi}


def _toy_eval(toy, sign):
    return evaluate_anchor(
        sign, toy["anchors"][sign], toy["core"], toy["phon"],
        toy["anchors"], toy["full"], toy["ins_sites"],
        toy["ctx_full"], toy["ctx_a"], toy["ctx_b"],
        toy["profiles"], toy["counts"], sorted(toy["anchors"]),
        toy["phi"], random.Random(117))


def test_toy_core_coherent_reading_validates():
    toy = _toy()
    r = _toy_eval(toy, "X")
    assert r["w3"]["state"] == PASS
    assert r["w3"]["p_value"] <= 0.05
    assert r["w3"]["score"] >= r["w3"]["phi"]
    assert r["w1"]["state"] == PASS
    assert r["outcome"] == "VALIDATED"


def test_toy_incoherent_reading_does_not_validate():
    toy = _toy()
    r = _toy_eval(toy, "Y")
    assert r["w3"]["state"] == FAIL
    assert r["outcome"] == "DEMOTE"


# ── Frozen partition on the real corpus ────────────────────────

def test_real_partition_totals():
    csv_path = _holdat_csv()
    if csv_path is None:
        pytest.skip("Holdat CSV not present (gitignored downloads)")
    from glossa_lab.phase117_run import load_holdat_with_sites
    ins_sites = load_holdat_with_sites(csv_path)
    assert len(ins_sites) == 1670
    assert sum(len(t) for t, _ in ins_sites) == 7002
    half1 = build_partition(ins_sites)
    half2 = build_partition(ins_sites)
    assert half1 == half2                       # deterministic
    tok_a = sum(len(t) for (t, _), h in zip(ins_sites, half1)
                if h == "A")
    tok_b = sum(len(t) for (t, _), h in zip(ins_sites, half1)
                if h == "B")
    assert (tok_a, tok_b) == (3531, 3471)       # spec section 3
    per = {}
    for (toks, _), h in zip(ins_sites, half1):
        for t in toks:
            a, b = per.get(t, (0, 0))
            per[t] = (a + (h == "A"), b + (h == "B"))
    # Appendix A.5 spot counts
    assert per["M293"] == (124, 108)
    assert per["M011"] == (10, 5)
    assert per["M024"] == (12, 1)
    assert per["M177"] == (5, 0)


# ── Real set recomputation (spec section 2) ────────────────────

def test_real_sets():
    anchors = json.loads(
        (BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json")
        .read_text("utf-8"))["anchors"]
    register = json.loads(
        (REPO / "reports" / "phase108_provenance_register.json")
        .read_text("utf-8"))
    sets = compute_sets(anchors, register)
    assert len(sets["flagged44"]) == 44
    assert len(sets["strict94"]) == 94
    assert len(sets["kur113"]) == 113
    assert "M293" in sets["flagged44"]
    assert anchors["M293"]["confidence"] == "MEDIUM"
    for s in ("M235", "M254", "M402"):
        assert s in sets["flagged44"]


# ── H23 registration ───────────────────────────────────────────

def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase117WithinCompilationValidation" in ATOMIC_NODES
