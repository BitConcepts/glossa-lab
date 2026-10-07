"""Tests for Phase-115 (spec 014) non-SA validation battery v2.

Covers: the opportunity-scaled attestation floor (band
boundaries), the T1 v2 state machine (opportunity floor,
stability guard, absent-from-Holdat), sentinel-position profile
geometry, the v2 layer-builder policy on toy rows (key
normalization, placeholders, partial retention, both dedupe
rules), set recomputation against the real repo files
(44 / 94 / 113), graph registration (H23), and a toy end-to-end
through evaluate_anchor_v2.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from glossa_lab.phase113_battery import (
    FAIL, NOT_ATTESTED, PASS, CorpusContext, CoreGrammar,
)
from glossa_lab.phase113_run import compute_sets
from glossa_lab.phase115_battery import (
    attestation_floor, evaluate_anchor_v2, opportunity,
)
from glossa_lab.phase115_battery import test_t1_v2 as t1_v2

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALID_INITIAL = _load(
    "phase58_phonological_gap",
    BACKEND / "scripts" / "phase58_phonological_gap.py",
).is_valid_dravidian_initial

BUILDER = _load(
    "phase115_build_layer_v2",
    BACKEND / "scripts" / "phase115_build_layer_v2.py")


# ── Opportunity + floor bands (spec 014 section 4) ─────────────

def test_opportunity_arithmetic():
    assert opportunity(10, 1.5) == 15.0
    assert opportunity(0, 1.926877) == 0.0
    assert opportunity(3, 0.5) == 1.5


@pytest.mark.parametrize("opp,floor", [
    (0.0, 1), (1.5, 1), (2.999, 1),
    (3.0, 2), (5.0, 2), (8.999, 2),
    (9.0, 3), (15.4, 3), (500.0, 3),
])
def test_attestation_floor_bands(opp, floor):
    assert attestation_floor(opp) == floor


# ── T1 v2 state machine ────────────────────────────────────────

def test_t1_v2_sign_absent_holdat():
    h = CorpusContext([["A", "B"]])
    i = CorpusContext([["S", "B"]] * 5)
    out = t1_v2("S", h, i, 2.0)
    assert out["state"] == NOT_ATTESTED
    assert out["reason"] == "sign_absent_holdat"


def test_t1_v2_below_opportunity_floor():
    h = CorpusContext([["S", "A"]] * 10)          # n_H = 10
    i = CorpusContext([["S", "A"]] * 2)           # n_I = 2 < floor 3
    out = t1_v2("S", h, i, 2.0)              # O = 20 -> floor 3
    assert out["floor"] == 3
    assert out["state"] == NOT_ATTESTED
    assert out["reason"] == "below_opportunity_floor"


def test_t1_v2_pass_on_single_token_at_scaled_floor():
    # Holdat profile (2/3 INITIAL, 1/3 TERMINAL); one ICIT token,
    # INITIAL; O = 1.5 -> floor 1; TV = 1/3 <= 0.40 -> PASS.
    h = CorpusContext([["S", "A"], ["S", "B"], ["A", "S"]])
    i = CorpusContext([["S", "A"]])
    out = t1_v2("S", h, i, 0.5)
    assert out["floor"] == 1
    assert out["n_icit_tokens"] == 1
    assert out["state"] == PASS


def test_t1_v2_disagreement_below_stability_is_not_a_fail():
    h = CorpusContext([["S", "A"], ["S", "B"], ["A", "S"]])
    i = CorpusContext([["A", "S"], ["B", "S"]])   # 2 tokens, all TERMINAL
    out = t1_v2("S", h, i, 0.5)
    assert out["state"] == NOT_ATTESTED
    assert out["reason"] == "below_stability_floor"


def test_t1_v2_disagreement_at_stability_fails():
    h = CorpusContext([["S", "A"], ["S", "B"], ["A", "S"]])
    i = CorpusContext([["A", "S"]] * 3)           # 3 tokens, all TERMINAL
    out = t1_v2("S", h, i, 0.5)
    assert out["state"] == FAIL


def test_t1_v2_tv_beyond_tolerance_fails_same_modal():
    h = CorpusContext([["S", "A"]] * 10)          # profile (1, 0, 0)
    i = CorpusContext([["S", "A"]] * 11 + [["A", "S"]] * 9)
    out = t1_v2("S", h, i, 2.0)              # profile (.55, 0, .45)
    assert out["modal_holdat"] == out["modal_icit"] == "INITIAL"
    assert out["tv"] == pytest.approx(0.45)
    assert out["state"] == FAIL


# ── Sentinel geometry (v2 layer profiles) ──────────────────────

def test_sentinel_occupies_its_position():
    ctx = CorpusContext([["M001", "UNK", "M002"]])
    assert ctx.profile("M001") == (1.0, 0.0, 0.0)   # INITIAL
    assert ctx.profile("M002") == (0.0, 0.0, 1.0)   # TERMINAL
    assert ctx.profile("UNK") == (0.0, 1.0, 0.0)    # MEDIAL
    assert ctx.token_count("UNK") == 1
    ctx2 = CorpusContext([["UNK", "M002"]])
    assert ctx2.profile("M002") == (0.0, 0.0, 1.0)  # still TERMINAL


# ── Layer builder policy (toy rows) ────────────────────────────

W2M = {"2": "M002", "3": "M003"}
W2P = {"7": "P007"}
P2M = {"P007": "M007"}


def test_builder_code_conversion():
    assert BUILDER.normalize_code("002") == "2"
    assert BUILDER.normalize_code("410") == "410"
    assert BUILDER.convert_code("002", W2M, W2P, P2M) == ("M002", "direct")
    assert BUILDER.convert_code("007", W2M, W2P, P2M) == ("M007", "chain")
    assert BUILDER.convert_code("000", W2M, W2P, P2M) == ("UNK", "placeholder")
    assert BUILDER.convert_code("999", W2M, W2P, P2M) == ("UNK", "placeholder")
    assert BUILDER.convert_code("555", W2M, W2P, P2M) == ("UNK", "unmapped")


def test_builder_partial_retention_and_dedupe():
    rows = [
        {"text": "+002-000-007+"},   # -> [M002, UNK, M007] kept
        {"text": "+002-000-007+"},   # exact duplicate -> dropped (intra)
        {"text": "+002-003-007+"},   # -> [M002, M003, M007] kept:
                                     # intra-layer dedupe is exact-only,
                                     # wildcard is NOT applied intra-layer
        {"text": "+555-556+"},       # zero mapped -> dropped
        {"text": "+002-555+"},       # partial len 2 -> kept (below
                                     # dedupe thresholds)
    ]
    kept, stats = BUILDER.build_layer(rows, [], W2M, W2P, P2M)
    assert kept == [["M002", "UNK", "M007"],
                    ["M002", "M003", "M007"],
                    ["M002", "UNK"]]
    assert stats["dropped_dedupe_intra"] == 1
    assert stats["dropped_zero_mapped"] == 1
    assert stats["kept_inscriptions"] == 3
    assert stats["kept_mapped_tokens"] == 6
    assert stats["token_map_coverage_excl_placeholders"] == \
        pytest.approx(8 / 11)


def test_builder_holdat_wildcard_dedupe():
    rows = [{"text": "+002-555-007+"}]            # [M002, UNK, M007]
    kept, stats = BUILDER.build_layer(
        rows, [["M002", "M003", "M007"]], W2M, W2P, P2M)
    assert kept == []
    assert stats["dropped_dedupe_holdat"] == 1


# ── Toy end-to-end (evaluate_anchor_v2) ────────────────────────

def _toy():
    """Same toy world as the Phase-113 tests: core A 'ka'
    (initial), B 'nal' (terminal), C 'ay' (medial); candidate X
    'ka' behaves like a core sign."""
    holdat = ([["A", "B"]] * 10 + [["A", "C", "B"]] * 10
              + [["X", "B"]] * 12 + [["A", "X", "B"]] * 4
              + [["X", "C", "B"]] * 4
              + [["Z", "B"]] * 10)
    icit = ([["A", "B"]] * 6 + [["X", "B"]] * 4
            + [["X", "C", "B"]] * 2
            + [["B", "Z"]] * 4)
    readings = {"A": "ka", "B": "nal", "C": "ay"}
    core = {"A", "B", "C"}
    grammar = CoreGrammar(core, readings, CorpusContext(holdat))
    return (CorpusContext(holdat), CorpusContext(icit), grammar,
            readings)


def test_toy_v2_core_consistent_anchor_validates():
    h, i, g, readings = _toy()
    r = evaluate_anchor_v2("X", "ka", g, readings, h, i,
                           VALID_INITIAL, 2.0)
    assert r["t1"]["state"] == PASS
    assert r["t1"]["floor"] == 3            # O = 2.0 * 20 = 40
    assert r["t2"]["state"] == PASS
    assert r["t3"]["state"] == PASS
    assert r["outcome"] == "VALIDATED_NON_SA"


def test_toy_v2_cross_corpus_contradiction_demotes():
    h, i, g, readings = _toy()
    # Z is INITIAL-only in Holdat (10 tokens) but TERMINAL-only
    # in the ICIT layer (4 tokens >= stability minimum) -> T1 FAIL.
    r = evaluate_anchor_v2("Z", "ka", g, readings, h, i,
                           VALID_INITIAL, 2.0)
    assert r["t1"]["state"] == FAIL
    assert r["outcome"] == "DEMOTE"


# ── Real set recomputation (spec 014 section 3) ───────────────

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


# ── H23 registration ───────────────────────────────────────────

def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase115NonSaValidation" in ATOMIC_NODES
