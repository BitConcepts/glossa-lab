"""Tests for Phase-122: Parpola<->Mahadevan crosswalk v1 + mayig layer.

Covers: crosswalk integrity (every pair row carries P, M,
relation, confidence, source; no forced 1:1 — splits/merges
present; conflicts kept on both sides and flagged; unmapped
rows honest), the frozen v1 headline counts, the mayig layer
(keyed by CISI object ID, provenance/MIT metadata, token
totals), and the through-crosswalk coverage figures recorded
in reports/phase122_crosswalk_mayig_results.json.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from glossa_lab.data import mayig_layer as ml
from glossa_lab.data import parpola_mahadevan_crosswalk_v1 as xw

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "reports" / "phase122_crosswalk_mayig_results.json"


def test_every_pair_row_carries_required_fields():
    for r in xw.load_crosswalk():
        assert r["parpola_id"].startswith("P")
        assert r["relation_type"] in {
            "1:1", "one-to-many", "many-to-one", "many-to-many",
            "unmapped"}
        assert r["confidence"] in {"high", "medium", "low", "none"}
        if r["relation_type"] != "unmapped":
            assert r["mahadevan_id"].startswith("M")
            assert r["sources"], "every mapping row carries a source"


def test_crosswalk_headline_counts():
    s = xw.crosswalk_stats()
    assert s["n_pairs"] == 762
    assert s["p_signs_covered"] == 412
    assert s["m_signs_covered"] == 412
    assert s["p_signs_unmapped"] == 4
    assert s["confidence_breakdown"] == {"high": 372, "low": 390}
    assert s["candidate_only_pairs"] == 219


def test_no_forced_one_to_one():
    rel = Counter(r["relation_type"] for r in xw.load_crosswalk())
    assert rel["one-to-many"] > 0 and rel["many-to-one"] > 0
    # a genuine split: some P sign asserts >1 M at high confidence
    assert any(len(xw.p_to_m(p, "high")) > 1
               for p in {r["parpola_id"] for r in xw.load_crosswalk()})


def test_conflicts_kept_both_sides_and_flagged():
    conf = xw.conflicts()
    assert len(conf) == 383
    assert all(c["conflict_detail"] for c in conf)
    # the documented v2 inversion: P001 is M012 in the canonical
    # registry/mayig maps and M001 in crosswalk_v2 — both kept
    assert xw.p_to_m("P001", "high") == ["M012"]
    assert "M001" in xw.p_to_m("P001", "low")


def test_unmapped_is_honest():
    assert xw.unmapped_p_signs() == ["P000", "P225", "P261", "P358"]
    assert xw.p_to_m("P000") == []  # damage marker: no M asserted


def test_mayig_layer_totals_and_keying():
    meta = ml.layer_metadata()
    assert meta["n_inscriptions"] == 179
    assert meta["n_sign_tokens"] == 1003
    assert meta["n_distinct_signs"] == 182
    assert meta["license"].startswith("MIT")
    assert meta["source_commit"] == \
        "ad2f1e218a34b8c33c57de0d6cb8d99272765bbb"
    inscs = ml.load_inscriptions()
    assert all(r["cisi_object_id"] for r in inscs)
    m1 = ml.get_by_object("M-1")
    assert m1 and m1[0]["side_id"] == "M-1A"
    assert m1[0]["tokens"] == ["P121", "P202", "P385", "P073", "P108"]
    assert len(ml.object_ids()) == 179


def test_coverage_figures_match_results():
    res = json.loads(RESULTS.read_text())
    assert res["coverage_tokens"] == {
        "clean": 768, "ambiguous": 202, "unmapped": 33}
    assert res["coverage_inscriptions"] == {"clean": 42, "partial": 137}
    # recompute token coverage through the loader (high+medium map)
    tok = Counter()
    for seq in ml.sequences():
        for t in seq:
            ms = xw.p_to_m(t, "medium")
            tok["clean" if len(ms) == 1 else
                "ambiguous" if len(ms) > 1 else "unmapped"] += 1
    assert dict(tok) == res["coverage_tokens"]


def test_cisi_overlap_recorded_with_basis():
    res = json.loads(RESULTS.read_text())
    ov = res["cisi_overlap"]
    # full overlap against the two obtainable structured ID lists
    assert ov["bhaskar2024_esm13"]["n_mayig_objects_in_set"] == 179
    assert ov["icit_keyed_layer"]["n_mayig_objects_in_set"] == 179
    assert ov["union_of_bases"]["mayig_coverage"] == 1.0
    assert "Phase E" in res["cisi_overlap_basis"]
