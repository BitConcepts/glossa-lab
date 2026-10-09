"""Tests for Phase-132 (spec 023, FROZEN) metrics machinery.

Covers backend/scripts/phase132_metrics.py: the minimum-edit
alignment (determinism + substitution preference at equal
cost), the agreement / gold-estimator formulas on toy
sequences, and the crosswalk-v1 primary-map derivation
(highest confidence, tie -> lowest P number; conflict flag
carried; UNK stays UNK; an M with no crosswalk row is
crosswalk_unmapped) — on synthetic rows and on known rows of
the real crosswalk of record.
"""

import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "phase132_metrics.py"
CROSSWALK = REPO / "data" / "crosswalks" / \
    "parpola_mahadevan_crosswalk_v1.json"

spec = importlib.util.spec_from_file_location("phase132_metrics", SCRIPT)
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)


def _row(m, p, conf, conflict=False):
    return {"mahadevan_id": m, "parpola_id": p, "confidence": conf,
            "conflict": conflict}


# ── Alignment ───────────────────────────────────────────────

def test_alignment_substitution_preferred_over_indel_pair():
    # One substitution (cost 1) must win over delete+insert
    # (cost 2), and over the equal-cost alternatives the
    # diagonal is chosen deterministically.
    assert pm.align(["P001"], ["P002"]) == [("P001", "P002")]
    assert pm.alignment_matches(["P001"], ["P002"]) == 0
    assert pm.alignment_differing(["P001"], ["P002"]) == 1


def test_alignment_deterministic_and_optimal():
    a = ["P001", "P002", "P003", "P004"]
    b = ["P001", "P009", "P003"]
    first = pm.align(a, b)
    for _ in range(5):
        assert pm.align(a, b) == first
    # Optimal: 1 substitution + 1 deletion = edit distance 2.
    assert sum(1 for x, y in first if x != y) == 2
    assert pm.alignment_matches(a, b) == 2


def test_alignment_indel_columns():
    cols = pm.align(["P001", "P002"], ["P001"])
    assert cols == [("P001", "P001"), ("P002", None)]
    cols = pm.align(["P001"], ["P001", "P002"])
    assert cols == [("P001", "P001"), (None, "P002")]
    assert pm.align([], []) == []
    assert pm.alignment_matches([], []) == 0


# ── Agreement / estimator formulas ──────────────────────────

def test_exact_sequence_agreement_toy():
    pairs = [(["P001", "P002"], ["P001", "P002"]),
             (["P001"], ["P002"]),
             (["UNK"], ["UNK"])]
    out = pm.exact_sequence_agreement(pairs)
    assert out["n_objects"] == 3 and out["n_exact"] == 2
    assert out["rate"] == round(2 / 3, 6)


def test_per_token_agreement_toy():
    # Object 1: 2/2 matches. Object 2: align [P001,P002,P003]
    # to [P001,P003] -> 2 matches, denominator max(3,2)=3.
    pairs = [(["P001", "P002"], ["P001", "P002"]),
             (["P001", "P002", "P003"], ["P001", "P003"])]
    out = pm.per_token_agreement(pairs)
    assert out["matches"] == 4 and out["denominator"] == 5
    assert out["rate"] == 0.8


def test_error_estimator_toy():
    # S2 vs S3: position 2 differs (substitution), plus one
    # token present only in S3 -> 2 differing positions,
    # denominator max(3,4)=4.
    pairs = [(["P001", "P002", "P003"], ["P001", "P009", "P003", "P004"]),
             (["UNK", "P005"], ["UNK", "P005"])]
    out = pm.error_estimator(pairs)
    assert out["differing_positions"] == 2
    assert out["denominator"] == 6
    assert out["rate"] == round(2 / 6, 6)


# ── Primary-map derivation ──────────────────────────────────

def test_primary_map_synthetic_tiebreak_and_conflict():
    rows = [_row("M900", "P900", "low"),
            _row("M900", "P902", "high", conflict=True),
            _row("M900", "P901", "high"),
            _row("M901", "P910", "medium"),
            _row("M901", "P911", "low"),
            # P-side unmapped marker rows carry no M and are
            # ignored by the M -> P derivation.
            _row("", "P000", "none")]
    m2p = pm.build_m_to_p(rows)
    # High-confidence tie between P901/P902 -> lowest P number.
    assert m2p["M900"]["primary"] == "P901"
    # All candidate rows carried, in frozen sort order.
    assert [c["parpola_id"] for c in m2p["M900"]["candidates"]] == \
        ["P901", "P902", "P900"]
    # The conflict flag is the PRIMARY row's flag (P901: False),
    # even though a sibling candidate row conflicts.
    assert m2p["M900"]["conflict"] is False
    assert m2p["M900"]["any_conflict"] is True
    # Medium outranks low.
    assert m2p["M901"]["primary"] == "P910"
    assert "P000" not in m2p and "" not in m2p


def test_primary_map_real_crosswalk_rows():
    rows = json.loads(CROSSWALK.read_text("utf-8"))["rows"]
    m2p = pm.build_m_to_p(rows)
    # M002: high tie P015/P016 (+ low P002) -> P015; its
    # primary row is one of the 383 conflict pairs.
    assert m2p["M002"]["primary"] == "P015"
    assert m2p["M002"]["conflict"] is True
    assert len(m2p["M002"]["candidates"]) == 3
    # M001: high P013 beats low P001; primary row conflicts.
    assert m2p["M001"]["primary"] == "P013"
    assert m2p["M001"]["conflict"] is True
    # M341: high P320 beats the same-number low P341.
    assert m2p["M341"]["primary"] == "P320"
    assert m2p["M341"]["conflict"] is False
    # M054 -> P076 (the attestation sign), high + conflict.
    assert m2p["M054"]["primary"] == "P076"


def test_derive_token_unk_and_unmapped():
    rows = json.loads(CROSSWALK.read_text("utf-8"))["rows"]
    m2p = pm.build_m_to_p(rows)
    unk = pm.derive_token("UNK", m2p)
    assert unk["p_value"] == "UNK" and unk["p_id"] is None
    assert unk["crosswalk_unmapped"] is False
    # M817 was matched by transcribers but has NO crosswalk
    # row in v1: crosswalk_unmapped, placeholder P value,
    # never equal to another unmapped sign's value.
    unm = pm.derive_token("M817", m2p)
    assert unm["crosswalk_unmapped"] is True
    assert unm["p_id"] is None
    assert unm["p_value"] == "UNMAPPED:M817"
    # M705 likewise has no row in crosswalk v1; its placeholder
    # is a different value, so distinct unmapped signs never
    # compare equal in P space.
    assert "M705" not in m2p
    assert pm.derive_token("M705", m2p)["p_value"] == "UNMAPPED:M705"
    mapped = pm.derive_token("M212", m2p)
    assert mapped["p_value"] == "P212" and mapped["p_id"] == "P212"


def test_distribution_stats():
    out = pm.distribution([10, 20, 30, 40])
    assert out == {"n": 4, "mean": 25.0, "median": 25.0,
                   "min": 10, "max": 40, "total": 100}
    assert pm.distribution([])["n"] == 0
