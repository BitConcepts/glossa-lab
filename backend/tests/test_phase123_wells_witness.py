"""Tests for Phase-123: Wells segmentation witness table.

Covers: the witness table covers exactly the 113 CANDIDATE + 44
pending_non_sa_validation anchor signs (157, disjoint); every row
carries a treatment in the closed vocabulary; every non-INDETERMINATE
row carries Wells graphemes and a thesis source; every INDETERMINATE
row carries a reason and no graphemes; the frozen headline counts;
the hand-verification record (>=10 rows, outcomes in the closed
vocabulary, the M293 discrepancy preserved); CSV/JSON agreement;
and the witness framing (no adoption recommendation anywhere).
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CSV_PATH = REPO / "data" / "crosswalks" / "wells_segmentation_witness_v1.csv"
JSON_PATH = REPO / "data" / "crosswalks" / "wells_segmentation_witness_v1.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"

TREATMENTS = {"SPLIT", "MERGE", "SAME", "NOT-COVERED", "INDETERMINATE"}
VERIF_OUTCOMES = {"verified", "verified_with_conflict", "partial", "discrepancy"}


def _rows() -> list[dict]:
    return json.loads(JSON_PATH.read_text())["rows"]


def test_covers_exactly_the_157_anchor_signs():
    anchors = json.loads(ANCHORS.read_text())["anchors"]
    cand = {k for k, v in anchors.items() if v.get("confidence") == "CANDIDATE"}
    pend = {k for k, v in anchors.items()
            if v.get("validation_status") == "pending_non_sa_validation"}
    assert len(cand) == 113 and len(pend) == 44 and not (cand & pend)
    rows = _rows()
    assert {r["sign"] for r in rows} == cand | pend
    assert len(rows) == 157
    for r in rows:
        expected = "pending_non_sa_validation" if r["sign"] in pend else "CANDIDATE"
        assert r["anchor_set"] == expected


def test_treatment_vocabulary_and_required_fields():
    for r in _rows():
        assert r["treatment"] in TREATMENTS
        assert r["implication_note"]
        if r["treatment"] == "INDETERMINATE":
            assert not r["wells_graphemes"]
            assert r["note"], "indeterminate rows must state the reason"
        else:
            assert r["thesis_source"], "determinate rows must cite a thesis source"
        if r["treatment"] in {"SPLIT", "MERGE", "SAME"}:
            assert r["wells_graphemes"], "SPLIT/MERGE/SAME rows must name Wells graphemes"


def test_headline_counts_frozen():
    counts = Counter(r["treatment"] for r in _rows())
    assert counts == {"SAME": 87, "SPLIT": 40, "MERGE": 5,
                      "NOT-COVERED": 2, "INDETERMINATE": 23}


def test_hand_verification_record():
    ver = {r["sign"]: r["verification"] for r in _rows() if r["verification"]}
    assert len(ver) >= 10
    assert set(ver.values()) <= VERIF_OUTCOMES
    assert ver["M293"] == "discrepancy"
    assert ver["M389"] == "verified_with_conflict"
    outcomes = Counter(ver.values())
    assert len(ver) == 20
    assert outcomes["verified"] + outcomes["verified_with_conflict"] == 17
    assert outcomes["partial"] == 2 and outcomes["discrepancy"] == 1


def test_csv_json_agree():
    doc = json.loads(JSON_PATH.read_text())
    with CSV_PATH.open(newline="") as fh:
        csv_rows = list(csv.DictReader(fh))
    assert len(csv_rows) == len(doc["rows"]) == 157
    for jr, cr in zip(doc["rows"], csv_rows, strict=True):
        assert jr["sign"] == cr["sign"]
        assert jr["treatment"] == cr["treatment"]
        assert jr["wells_graphemes"] == cr["wells_graphemes"]


def test_witness_framing_no_adoption_language():
    doc = json.loads(JSON_PATH.read_text())
    assert "Witness statement only" in doc["_witness_framing"]
    blob = JSON_PATH.read_text().lower()
    for banned in ("recommend adopting", "should adopt", "we adopt",
                   "anchor should be upgraded", "anchor should be downgraded"):
        assert banned not in blob
    for r in doc["rows"]:
        if r["treatment"] in {"SPLIT", "MERGE", "NOT-COVERED"}:
            assert "if wells's segmentation were adopted" in r["implication_note"].lower()
