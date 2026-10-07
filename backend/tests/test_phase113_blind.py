"""Tests for Phase-113 (design stage) new candidate features.

Design-stage tests (pre-freeze): the mechanical permutation-
sensitivity verification — every new candidate must change
materially under within-text permutation on structured toy
corpora — plus hand-computed values, determinism, and
degenerate-input guards.

Note on toy choice: toy_a / toy_b are the Phase-112 toy
constructions, copied verbatim. On those two small-vocabulary
toys alone, shared_bigram_type_frac (token-weighted, per its
definition) cannot move by more than 0.0016 under any within-text
permutation (its original value is 1.0 and every permuted bigram
type still recurs across texts), so a third toy with a larger
vocabulary and cross-text bigram structure (toy_c) is included
for the cross-text family; every candidate must move on at least
one of the three toys.
"""
from __future__ import annotations

import numpy as np
import pytest

from glossa_lab.phase112_features import CANDIDATE_FEATURES as CANDIDATES112
from glossa_lab.phase112_features import FEATURE_NAMES as FEATURE_NAMES112
from glossa_lab.phase113_features import (
    LADDER_A,
    NEW_CANDIDATES,
    NEW_CANDIDATES_B,
    NEW_CANDIDATES_C,
    extract_all113,
    extract_new_candidates,
)

# ---------------------------------------------------------------------------
# Structured toy corpora (deterministic; no RNG in construction)
# ---------------------------------------------------------------------------


def toy_a() -> list[list[int]]:
    """Positional + Markov toy: fixed start tokens, a period-4 body
    cycle with an adjacent-double motif, one fixed end token."""
    texts = []
    for i in range(120):
        length = 5 + (i % 4)
        start = 90 + (i % 2)
        body_len = length - 2
        s = i % 4
        seq = [(s + j) % 4 for j in range(body_len)]
        if body_len >= 2:
            seq[1] = seq[0]
        texts.append([start] + seq + [80])
    return texts


def toy_b() -> list[list[int]]:
    """Period-3 repetition toy: distance-3 pairs are always equal."""
    return [[(j + i) % 3 for j in range(6 + (i % 3))] for i in range(90)]


def toy_c() -> list[list[int]]:
    """Cross-text toy: overlapping windows over a 40-token cycle,
    so most bigram types are shared across many texts."""
    return [[(i + j) % 40 for j in range(6)] for i in range(80)]


def _permute(texts: list[list[int]], seed: int = 999) -> list[list[int]]:
    rng = np.random.default_rng(np.random.SeedSequence([seed]))
    out = []
    for t in texts:
        arr = list(t)
        rng.shuffle(arr)
        out.append(arr)
    return out


# ---------------------------------------------------------------------------
# Mechanical permutation-sensitivity
# ---------------------------------------------------------------------------


def test_all_new_candidates_permutation_sensitive_on_toys():
    """Each new candidate must move by > 0.002 under permutation
    on at least one structured toy."""
    toys = [toy_a(), toy_b(), toy_c()]
    originals = [extract_new_candidates(t, draw_index=0) for t in toys]
    permuted = [extract_new_candidates(_permute(t), draw_index=0) for t in toys]
    for name in NEW_CANDIDATES:
        delta = max(abs(o[name] - p[name]) for o, p in zip(originals, permuted))
        assert delta > 0.002, f"{name} is permutation-insensitive on toys (delta={delta})"


def test_candidate_lists_disjoint_and_complete():
    assert NEW_CANDIDATES == NEW_CANDIDATES_B + NEW_CANDIDATES_C
    assert len(NEW_CANDIDATES) == len(set(NEW_CANDIDATES))
    assert not set(NEW_CANDIDATES) & set(CANDIDATES112)


def test_ladder_a_is_phase112_feature_names():
    assert LADDER_A == FEATURE_NAMES112
    assert len(LADDER_A) == 16


# ---------------------------------------------------------------------------
# Hand-computed values
# ---------------------------------------------------------------------------


def test_dup_features_hand_values():
    f = extract_new_candidates([[0, 1, 2], [0, 1, 2], [3], [4, 5]], draw_index=0)
    # [0,1,2] occurs twice; the other two texts are unique.
    assert f["dup_text_frac"] == pytest.approx(2 / 4)
    # duplicated texts hold 6 of the 9 tokens
    assert f["dup_token_coverage"] == pytest.approx(6 / 9)


def test_dup_features_all_identical():
    f = extract_new_candidates([[1, 2], [1, 2], [1, 2]], draw_index=0)
    assert f["dup_text_frac"] == pytest.approx(1.0)
    assert f["dup_token_coverage"] == pytest.approx(1.0)


def test_mi_lag2_zero_when_lag2_token_constant():
    # Lag-2 pairs are (0, 5) and (1, 5): the lag-2 token is constant,
    # so H(py) = 0 and H(pxy) = H(px) exactly (same counts, same
    # Miller-Madow correction), giving MI = 0.
    draw = [[0, 9, 5], [1, 8, 5], [0, 7, 5], [1, 6, 5]] * 20
    f = extract_new_candidates(draw, draw_index=0)
    assert f["mi_lag2"] == pytest.approx(0.0, abs=1e-9)


def test_mi_lag2_near_zero_for_independent_lag2_pairs():
    # All four lag-2 combinations occur equally often, so the
    # plug-in MI is 0 up to the (small) Miller-Madow corrections.
    draw = [[0, 9, 0], [0, 9, 1], [1, 9, 0], [1, 9, 1]] * 50
    f = extract_new_candidates(draw, draw_index=0)
    assert abs(f["mi_lag2"]) < 0.01


def test_block_h5_constant_text_is_zero():
    # A constant text has exactly one 5-gram type, so the plug-in
    # entropy is 0 and the Miller-Madow term (m - 1) is also 0.
    f = extract_new_candidates([[7] * 10] * 5, draw_index=0)
    assert f["blockH5"] == pytest.approx(0.0)
    assert f["blockH6"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Determinism and degenerate inputs
# ---------------------------------------------------------------------------


def test_extraction_deterministic():
    draw = [[3, 1, 4, 1, 5], [9, 2, 6], [5, 3, 5]]
    assert extract_new_candidates(draw, draw_index=7) == extract_new_candidates(draw, draw_index=7)
    assert extract_all113(draw, draw_index=7) == extract_all113(draw, draw_index=7)


def test_extract_all113_merges_phase112_and_new():
    f = extract_all113([[0, 1, 0], [1, 0, 1], [0, 1, 0]], draw_index=0)
    assert set(f.keys()) == set(CANDIDATES112) | set(NEW_CANDIDATES)
    assert np.isfinite(list(f.values())).all()


def test_empty_draw_guards():
    f = extract_new_candidates([], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()
    assert f["pp_ratio_ord3"] == pytest.approx(1.0)


def test_single_token_texts_guards():
    f = extract_new_candidates([[5], [5], [9]], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()


def test_two_identical_texts_guards():
    f = extract_new_candidates([[0, 1], [0, 1]], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()
    assert f["dup_text_frac"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Pipeline: ladder, blinding, adversarial generator, optimizer,
# control shares, verdict branches, classify guard (spec 012)
# ---------------------------------------------------------------------------

import inspect  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from glossa_lab import phase112_custodian as custodian112  # noqa: E402
from glossa_lab import phase113_analyst as analyst113  # noqa: E402
from glossa_lab import phase113_custodian as custodian113  # noqa: E402
from glossa_lab import phase114_run as run113  # noqa: E402

_AUDIT_PATH = Path(__file__).resolve().parents[2] / "reports" / "phase113_feature_audit.json"


def test_ladder_matches_audit():
    audit = json.loads(_AUDIT_PATH.read_text(encoding="utf-8"))
    admitted = audit["admitted_new_features"]
    admitted_b = [n for n in NEW_CANDIDATES_B if n in set(admitted["B"])]
    admitted_c = [n for n in NEW_CANDIDATES_C if n in set(admitted["C"])]
    assert admitted_b == admitted["B"]
    assert admitted_c == admitted["C"]
    assert custodian113.LADDER_L1 == FEATURE_NAMES112
    assert custodian113.LADDER_L2 == custodian113.LADDER_L1 + admitted_b
    assert custodian113.LADDER_L3 == custodian113.LADDER_L2 + admitted_c
    assert len(custodian113.LADDER_L1) == 16
    assert len(custodian113.LADDER_L2) == 24
    assert len(custodian113.LADDER_L3) == 30
    assert custodian113.FEATURE_NAMES == custodian113.LADDER_L3


def test_blinding_invariant():
    import ast

    src = inspect.getsource(analyst113)
    tree = ast.parse(src)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert imported, "analyst should have imports to inspect"
    assert all("custodian" not in name for name in imported)
    assert "phase113_custodian" not in imported
    assert "phase111_custodian" not in imported


def test_extract_ladder_features_order_and_shape():
    draw = [[0, 1, 2, 0], [1, 2, 0, 1], [2, 0, 1, 2, 0]] * 5
    row = custodian113.extract_ladder_features(draw, draw_index=0)
    assert len(row) == 30
    feats = extract_all113(draw, draw_index=0)
    assert row == [feats[name] for name in custodian113.LADDER_L3]
    assert np.isfinite(row).all()


def test_final_training_rows_slice_dict_gen_train():
    n_feat = len(custodian113.LADDER_L3)

    def _rows(value, n=4):
        return [[value] * n_feat for _ in range(n)]

    panel = {
        "feature_names": custodian113.LADDER_L3,
        "known_ids": ["C01", "C02"],
        "blind_ids": [],
        "members": {
            "C01": {"label": "dravidian", "features_primary": _rows(1.0)},
            "C02": {"label": "non_linguistic", "features_primary": _rows(2.0)},
        },
        "gen_train": {
            "rows": [{name: 3.0 for name in custodian113.LADDER_L3}],
            "labels": ["gen_heraldic"],
        },
    }
    X, y = analyst113.final_training_rows(panel, custodian113.LADDER_L1)
    assert X.shape == (9, 16)
    assert list(y).count("gen_heraldic") == 1
    model = analyst113.train_final_model(panel, custodian113.LADDER_L1)
    assert "gen_heraldic" in model.classes_
    assert model.posterior(X).shape == (9, len(model.classes_))


# -- Adversarial generator ---------------------------------------------------


def _synthetic_r1(n_texts: int = 40, vocab: int = 12) -> list[list[int]]:
    texts = []
    for i in range(n_texts):
        length = 3 + (i % 5)
        texts.append([(i + j) % vocab for j in range(length)])
    return texts


@pytest.mark.skipif(
    not (custodian113.SOURCES / "holdat_indus_corpus.csv").exists(),
    reason="phase113 staging not present in this environment",
)
def test_theta_s5_reproduces_s5():
    # NOTE on the reference corpus: c112.s5_generator must be fed
    # R1's SOURCE-TOKEN (string) texts. Feeding it the int-mapped
    # texts silently degenerates it — its str() coercion makes the
    # successor lookups miss every count, collapsing it to a
    # positional-unigram sampler. So S5 is generated in string space
    # and mapped into R1's int space through the token-by-token
    # correspondence between the loader texts and r1_texts_int().
    r1_str = custodian113.LOADERS[custodian113.R1_CODE][1]()[0]
    r1_int = custodian113.r1_texts_int()
    mapping: dict = {}
    for str_text, int_text in zip(r1_str, r1_int):
        for str_tok, int_tok in zip(str_text, int_text):
            mapping[str_tok] = int_tok
    s5_str, _stats = custodian112.s5_generator(r1_str)
    s5_int = [[mapping[tok] for tok in t] for t in s5_str]
    assert sum(len(t) for t in s5_int) >= 20_000
    # The frozen S5 sample's recorded unigram fidelity (spec 010/012:
    # TV = 0.0419) reproduces exactly in this mapping.
    assert custodian113.unigram_tv(s5_int, r1_int) == pytest.approx(0.0419, abs=0.002)

    advgen = custodian113.AdvGen(r1_int)
    gen = advgen.generate(custodian113.THETA_S5, [20261030, 1, 0])
    gen_alt = advgen.generate(custodian113.THETA_S5, [20261030, 1, 1])
    assert sum(len(t) for t in gen) >= 20_000
    assert custodian113.unigram_tv(gen, r1_int) < 0.10
    # Positional-bigram fidelity: the per-context empirical TV
    # statistic has a sampling-noise floor of ~0.25 at 55k tokens —
    # two corpora from the IDENTICAL model differ by that much — so
    # the spec section 6 anchor (< 0.10 between the two generators'
    # distributions) is checked as: no systematic excess over the
    # same-model noise floor, and an absolute bound well under the
    # degenerate (positional-unigram) mismatch of ~0.61.
    tv_vs_s5 = custodian113.positional_bigram_tv(gen, s5_int)
    tv_noise_floor = custodian113.positional_bigram_tv(gen, gen_alt)
    assert tv_vs_s5 < 0.30
    assert tv_vs_s5 <= tv_noise_floor + 0.05


def test_generator_determinism():
    advgen = custodian113.AdvGen(_synthetic_r1())
    theta = (0.2, 0.2, 0.2, 0.2, 0.2, 1.0, 0.3, 3.0, 1.0, 0.1, 0.1)
    first = advgen.generate(theta, [7, 8, 9])
    second = advgen.generate(theta, [7, 8, 9])
    assert first == second
    assert sum(len(t) for t in first) >= 55_000


def test_generator_copy_burst_extremes():
    advgen = custodian113.AdvGen(_synthetic_r1())
    theta_copy = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0)
    copied = advgen.generate(theta_copy, [11, 12])
    assert len(copied) > 1
    assert all(t == copied[0] for t in copied[1:])

    theta_burst = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0)
    bursted = advgen.generate(theta_burst, [13, 14])
    assert all(all(tok == t[0] for tok in t[1:]) for t in bursted if len(t) > 1)


# -- Optimizer ----------------------------------------------------------------


def _stub_eval(theta, eval_index):
    feasible = theta[9] <= 0.05
    return float(theta[1]), feasible, 0 if feasible else 1, {"w_P2": float(theta[1])}


def test_optimizer_determinism_and_ranking(tmp_path):
    theta_a, trace_a = custodian113.run_search(1, _stub_eval, tmp_path / "trace_a.jsonl")
    theta_b, trace_b = custodian113.run_search(1, _stub_eval, tmp_path / "trace_b.jsonl")
    assert theta_a == theta_b
    assert [r["objective"] for r in trace_a] == [r["objective"] for r in trace_b]
    assert len(trace_a) == 200
    # round 1 candidate 0 is the forced theta_S5 (spec section 7)
    assert trace_a[0]["theta"] == [float(v) for v in custodian113.THETA_S5]
    lines_a = (tmp_path / "trace_a.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines_a) == 200
    assert json.loads(lines_a[0])["eval_index"] == 0

    # feasible outranks infeasible regardless of objective
    assert custodian113.rank_key(True, 3, -1.0, 199) > custodian113.rank_key(False, 0, 999.0, 0)
    # among infeasible, fewer violations wins over higher objective
    assert custodian113.rank_key(False, 1, 0.0, 5) > custodian113.rank_key(False, 2, 100.0, 0)
    # among feasible, higher objective wins; ties break to lower index
    assert custodian113.rank_key(True, 0, 2.0, 9) > custodian113.rank_key(True, 0, 1.0, 0)
    assert custodian113.rank_key(True, 0, 1.0, 3) > custodian113.rank_key(True, 0, 1.0, 4)


# -- Control share + verdict ----------------------------------------------------

_CLASSES113 = analyst113.FAMILIES + [analyst113.NONLING] + analyst113.GEN_CLASSES


def _post_row(**masses) -> np.ndarray:
    row = np.zeros(len(_CLASSES113))
    for name, value in masses.items():
        row[_CLASSES113.index(name)] = value
    return row


def test_control_share_math():
    post = np.array([
        _post_row(non_linguistic=0.6, dravidian=0.4),          # counted
        _post_row(non_linguistic=0.3, dravidian=0.7),          # not counted
        _post_row(gen_heraldic=0.5, dravidian=0.5),            # counted (>=)
        _post_row(gen_administrative=0.2, non_linguistic=0.2,
                  dravidian=0.6),                              # not counted
    ])
    assert analyst113.control_share(post, _CLASSES113) == pytest.approx(0.5)


def test_verdict_invalid_on_adversarial_share():
    posteriors: dict[str, np.ndarray] = {}
    roles: dict[str, str] = {}
    synth_codes = ["S1_permutation", "S2_iid_zipf", "S3_heraldic_gen",
                   "S4_admin_gen", "S5_positional_bigram_gen"]
    for i, code in enumerate(synth_codes):
        cid = f"C{i + 1:02d}"
        posteriors[cid] = np.tile(_post_row(non_linguistic=1.0), (20, 1))
        roles[cid] = code
    for i, code in enumerate(["R1_indus_holdat_m77", "R2_indus_icit_wells",
                              "R3_indus_mixed"]):
        cid = f"C{i + 6:02d}"
        posteriors[cid] = np.tile(_post_row(dravidian=1.0), (20, 1))
        roles[cid] = code
    verdict = analyst113.compute_verdict(
        posteriors, _CLASSES113, roles, {}, {},
        control_shares_extra={"A1": 1.0, "A2": 0.50, "A3": 0.97})
    assert verdict["verdict"] == "INVALID RUN — CONTROL VALIDITY FAILED"
    assert "A2" in verdict["failing_controls"]
    assert verdict["control_validity_shares"]["A2"] == pytest.approx(0.50)
    assert verdict["control_validity_shares"]["S1_permutation"] == pytest.approx(1.0)


# -- Classify guard --------------------------------------------------------------


def test_classify_guard(tmp_path, monkeypatch):
    fake = tmp_path / "phase113_blind_affiliation_results.json"
    fake.write_text(json.dumps({
        "verdict": "INVALID RUN — CONTROL VALIDITY FAILED",
        "stop_stage": "rounds_control",
        "status": "stopped_at_rounds_control",
        "rounds": {"1": {}},
    }), encoding="utf-8")
    monkeypatch.setattr(run113, "RESULTS_PATH", fake)
    with pytest.raises(RuntimeError):
        run113.stage_classify()


def test_classify_guard_incomplete_rounds(tmp_path, monkeypatch):
    fake = tmp_path / "phase113_blind_affiliation_results.json"
    fake.write_text(json.dumps({
        "verdict": None, "stop_stage": None,
        "status": "rounds_running", "rounds": {},
    }), encoding="utf-8")
    monkeypatch.setattr(run113, "RESULTS_PATH", fake)
    with pytest.raises(RuntimeError):
        run113.stage_classify()
