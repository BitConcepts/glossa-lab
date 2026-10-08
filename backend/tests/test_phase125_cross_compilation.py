"""Unit tests for the Phase-125 (spec 019) cross-compilation
positional comparison machinery.

Toy controls: profiles/TV/W1/Spearman on hand-computed
inputs; arm construction on synthetic crosswalk rows
(ambiguity excluded from PRIMARY, included pair-by-pair in
arm B; unmapped rows in no arm); end-to-end verdict
controls through the real section-6 rule — a synthetic
agreeing pair-set PASSes, a synthetic disagreeing and
uninformative pair-set FAILs, a 5-pair set is
NULL-STARVED. Real-input tests pin the frozen counts of
spec Appendix A (372 high / 286 primary / 762 all pairs;
judgeable at floor 8: PRIMARY 16, arm B 28) and the H23
graph registration.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.data import parpola_mahadevan_crosswalk_v1 as xw  # noqa: E402
from glossa_lab.phase113_battery import CorpusContext  # noqa: E402
from glossa_lab.phase125_cross_compilation import (  # noqa: E402
    ARM_PRIMARY, ARM_SENSITIVITY_A, ARM_SENSITIVITY_B,
    build_arms, classify, evaluate_arm, median, sign_profile,
    spearman, w1_distance,
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


# ── Profiles / distances ──────────────────────────────────

def test_sign_profile_convention():
    ins = [["A", "B", "C"], ["A", "B"], ["X"]]
    prof_a, n_a, _ = sign_profile(ins, "A")
    assert n_a == 2 and prof_a == (1.0, 0.0, 0.0)
    prof_b, _, _ = sign_profile(ins, "B")
    assert prof_b == (0.0, 0.5, 0.5)  # medial, then terminal
    prof_x, _, _ = sign_profile(ins, "X")
    assert prof_x == (0.0, 1.0, 0.0)  # sole token is MEDIAL
    prof_z, n_z, _ = sign_profile(ins, "Z")
    assert prof_z is None and n_z == 0


def test_w1_distance():
    assert w1_distance((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)) == 2.0
    assert w1_distance((0.5, 0.5, 0.0), (0.5, 0.0, 0.5)) == 0.5
    assert w1_distance((0.2, 0.3, 0.5), (0.2, 0.3, 0.5)) == 0.0


def test_median():
    assert median([3.0, 1.0, 2.0]) == 2.0
    assert median([1.0, 2.0, 3.0, 4.0]) == 2.5
    assert median([]) is None


def test_spearman():
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)
    # ties get average ranks
    assert spearman([1, 1, 2, 3], [1, 2, 3, 4]) == pytest.approx(
        0.948683, abs=1e-5)
    # a constant vector has no rho (spec section 5)
    assert spearman([1, 1, 1, 1], [1, 2, 3, 4]) is None
    assert spearman([1, 2], [1, 2]) is None


# ── Arms on synthetic rows ────────────────────────────────

def _row(p, m, conf, rel="1:1"):
    return {"parpola_id": p, "mahadevan_id": m, "confidence": conf,
            "relation_type": rel}


def test_build_arms_gating():
    rows = [
        _row("P001", "M001", "high"),
        _row("P002", "M002", "high"),
        _row("P002", "M003", "high"),   # P002 ambiguous within high
        _row("P003", "M004", "low"),
        _row("P004", None, "none", rel="unmapped"),
    ]
    arms = build_arms(rows)
    # PRIMARY: only the unambiguous high pair survives
    assert [(p["parpola_id"], p["mahadevan_id"]) for p in arms[ARM_PRIMARY]] \
        == [("P001", "M001")]
    # arm A = high+medium unique; no medium rows here -> same as PRIMARY
    assert arms[ARM_SENSITIVITY_A] == arms[ARM_PRIMARY]
    # arm B: every pair row, pair-by-pair, incl. ambiguous and low
    assert len(arms[ARM_SENSITIVITY_B]) == 4


# ── Verdict rule (classify) ───────────────────────────────

def _stats(n, med, rho_i, rho_t, p_null):
    return {"n_judgeable": n, "median_tv": med, "spearman_initial": rho_i,
            "spearman_terminal": rho_t,
            "null": ({"p_null": p_null} if p_null is not None else None)}


def test_classify_patterns():
    assert classify(_stats(16, 0.20, 0.9, 0.8, 0.001))["verdict"] == "PASS"
    assert classify(_stats(16, 0.70, 0.1, 0.0, 0.90))["verdict"] == "FAIL"
    # large but informative: not FAIL (spec section 6.3 note)
    out = classify(_stats(16, 0.70, 0.1, 0.0, 0.001))
    assert out["verdict"] == "NULL" and out["substate"] == "INCONCLUSIVE"
    # small distances but a rho leg missed: inconclusive, not pass
    out = classify(_stats(16, 0.20, 0.9, 0.2, 0.001))
    assert out["verdict"] == "NULL" and out["substate"] == "INCONCLUSIVE"
    # starved beats every other pattern
    out = classify(_stats(5, 0.0, 1.0, 1.0, 0.001))
    assert out["verdict"] == "NULL" and out["substate"] == "STARVED"


# ── Toy end-to-end verdicts through evaluate_arm ─────────

def _ctx_from_profiles(profiles: dict, n_per: int = 20):
    """Build a toy inscription list whose per-sign positional
    counts realize the given (I, M, T) share triples at
    n_per tokens per sign (counts rounded to integers that
    sum to n_per). Each sign gets its own inscriptions:
    initial tokens open a 2-token inscription, terminal
    tokens close one, medial tokens are sole tokens."""
    inscriptions = []
    for sign, (pi, pm, pt) in profiles.items():
        ni = round(pi * n_per)
        nt = round(pt * n_per)
        nm = n_per - ni - nt
        assert nm >= 0
        inscriptions += [[sign, "FILL"]] * ni
        inscriptions += [["FILL", sign]] * nt
        inscriptions += [[sign]] * nm
    return CorpusContext(inscriptions)


def _pairs(signs):
    return [{"parpola_id": f"P{i:03d}", "mahadevan_id": f"M{i:03d}",
             "confidence": "high"} for i in range(len(signs))]


def test_toy_end_to_end_pass():
    # 12 pairs; gradient profiles, identical in both compilations
    grads = []
    for k in range(12):
        pi = 1.0 - k / 11.0
        grads.append((round(pi, 4), 0.0, round(1.0 - pi, 4)))
    mayig = {f"P{i:03d}": g for i, g in enumerate(grads)}
    holdat = {f"M{i:03d}": g for i, g in enumerate(grads)}
    ev = evaluate_arm(_pairs(grads), _ctx_from_profiles(mayig),
                      _ctx_from_profiles(holdat))
    assert ev["stats"]["n_judgeable"] == 12
    assert ev["stats"]["median_tv"] == pytest.approx(0.0, abs=0.06)
    out = classify(ev["stats"])
    assert out["verdict"] == "PASS", ev["stats"]


def test_toy_end_to_end_fail():
    # 12 pairs; one-hot profiles, exactly reversed across compilations
    mayig = {}
    holdat = {}
    for i in range(12):
        mayig[f"P{i:03d}"] = (1.0, 0.0, 0.0) if i < 6 else (0.0, 0.0, 1.0)
        holdat[f"M{i:03d}"] = (0.0, 0.0, 1.0) if i < 6 else (1.0, 0.0, 0.0)
    ev = evaluate_arm(_pairs(list(range(12))), _ctx_from_profiles(mayig),
                      _ctx_from_profiles(holdat))
    assert ev["stats"]["n_judgeable"] == 12
    assert ev["stats"]["median_tv"] == pytest.approx(1.0)
    out = classify(ev["stats"])
    assert out["verdict"] == "FAIL", ev["stats"]


def test_toy_end_to_end_starved():
    grads = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
             (0.5, 0.0, 0.5), (0.5, 0.5, 0.0)]
    mayig = {f"P{i:03d}": g for i, g in enumerate(grads)}
    holdat = {f"M{i:03d}": g for i, g in enumerate(grads)}
    ev = evaluate_arm(_pairs(grads), _ctx_from_profiles(mayig),
                      _ctx_from_profiles(holdat))
    assert ev["stats"]["n_judgeable"] == 5
    out = classify(ev["stats"])
    assert out["verdict"] == "NULL" and out["substate"] == "STARVED"


def test_below_floor_pairs_are_counted_not_scored():
    # both signs attested only 3 times (< floor 8)
    mayig = CorpusContext([["P001", "FILL"]] * 3)
    holdat = CorpusContext([["M001", "FILL"]] * 3)
    pairs = [{"parpola_id": "P001", "mahadevan_id": "M001",
              "confidence": "high"}]
    ev = evaluate_arm(pairs, mayig, holdat)
    assert ev["stats"]["n_pairs"] == 1
    assert ev["stats"]["n_judgeable"] == 0
    assert ev["stats"]["n_below_floor"] == 1
    assert ev["records"][0]["tv"] is None  # excluded, never imputed


# ── Real inputs: frozen Appendix A counts ────────────────

def test_real_crosswalk_arm_counts():
    arms = build_arms(xw.load_crosswalk())
    assert len(arms[ARM_PRIMARY]) == 286
    # v1 has zero medium pairs: arm A coincides with PRIMARY
    assert arms[ARM_SENSITIVITY_A] == arms[ARM_PRIMARY]
    assert len(arms[ARM_SENSITIVITY_B]) == 762
    stats = xw.crosswalk_stats()
    assert stats["confidence_breakdown"] == {"high": 372, "low": 390}
    assert xw.unmapped_p_signs() == ["P000", "P225", "P261", "P358"]


def test_real_judgeability_counts():
    hp = _holdat_path()
    if hp is None:
        pytest.skip("Holdat CSV not present")
    from glossa_lab.data import mayig_layer as ml
    from glossa_lab.phase113_run import load_holdat_inscriptions

    mayig_ctx = CorpusContext([list(r["tokens"])
                               for r in ml.load_inscriptions()])
    holdat_ctx = CorpusContext(load_holdat_inscriptions(hp))
    assert mayig_ctx.n_tokens == 1003 and holdat_ctx.n_tokens == 7002
    arms = build_arms(xw.load_crosswalk())
    ev_p = evaluate_arm(arms[ARM_PRIMARY], mayig_ctx, holdat_ctx)
    assert ev_p["stats"]["n_judgeable"] == 16
    assert ev_p["stats"]["n_below_floor"] == 286 - 16
    ev_b = evaluate_arm(arms[ARM_SENSITIVITY_B], mayig_ctx, holdat_ctx)
    assert ev_b["stats"]["n_judgeable"] == 28


def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase125CrossCompilationPositional" in ATOMIC_NODES
