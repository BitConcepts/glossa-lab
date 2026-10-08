"""Phase-120 unit tests: Bhaskar disagreement register + classifier.

Descriptive triage only. These tests pin the register's integrity
(unique ids, valid kinds, resolvable locations), the classifier's
contract (CONTESTED only from a documented dispute naming the
sign; ALL-AGREE never inferred), and the real 44-anchor outcome
(44 rows; counts 0 / 1 / 43) against the anchors file of record.
"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from glossa_lab.phase120_bhaskar import (
    ALL_CASES,
    DISAGREEMENT_CASES,
    DISPUTE_KINDS,
    FORM_REANALYSIS_NOTES,
    MENTION_SOURCES,
    cases_for,
    classify_anchor,
    count_labelled_e1,
    disagreement_csv,
    disagreement_table_rows,
    load_flagged44,
    mentions_for,
    triage_all,
)

REPO = Path(__file__).resolve().parents[2]
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"


# -- register integrity -----------------------------------------------------

def test_case_ids_unique_and_prefixed():
    ids = [c.case_id for c in ALL_CASES]
    assert len(ids) == len(set(ids))
    assert all(i.startswith("BH-") for i in ids)


def test_kinds_valid():
    for c in DISAGREEMENT_CASES:
        assert c.kind in DISPUTE_KINDS, c.case_id
    for c in FORM_REANALYSIS_NOTES:
        assert c.kind == "form_reanalysis"


def test_every_case_has_location_and_summary():
    for c in ALL_CASES:
        assert c.location and "ESM" in c.location or "Article" in c.location
        assert len(c.summary) > 40


def test_cases_for_402_is_the_coverage_gap():
    hits = cases_for(402)
    assert [c.case_id for c in hits] == ["BH-D10"]
    assert hits[0].kind == "coverage_gap"


def test_cases_for_267_excludes_reanalysis_by_default():
    assert [c.case_id for c in cases_for(267)] == ["BH-D01"]
    assert cases_for(59) == []  # fish family is reanalysis, not a dispute
    assert [c.case_id for c in cases_for(59, include_reanalysis=True)] == ["BH-R01"]


def test_context_signs_are_not_involved_signs():
    d12 = next(c for c in ALL_CASES if c.case_id == "BH-D12")
    assert d12.signs_involved == ()
    assert 28 in d12.context_signs  # M028 must NOT become CONTESTED via context


# -- mention index ----------------------------------------------------------

def test_mention_sources_are_sign_numbers():
    for name, signs in MENTION_SOURCES.items():
        assert signs, name
        assert all(1 <= s <= 999 for s in signs), name


def test_mentions_for_known_signs():
    assert "ESM1_list1_frontal" in mentions_for(402)
    assert "ESM3_list1_base_of_99" in mentions_for(293)
    assert mentions_for(11) == []


# -- classifier contract ----------------------------------------------------

def test_classifier_contested_only_for_402_among_probed():
    assert classify_anchor("M402", "vēḷ", "HIGH").classification == "CONTESTED"
    # 267 is contested in the register but is not one of the 44;
    # the classifier itself must still report it faithfully.
    assert classify_anchor("M267", "iN/in", "MEDIUM").classification == "CONTESTED"


def test_classifier_never_infers_all_agree():
    # Signs Bhaskar uses heavily and silently (e.g. 155, 293) are
    # NOT-COVERED, never ALL-AGREE: silent use is not concordance.
    for key in ("M155", "M293", "M011", "M035"):
        row = classify_anchor(key, "x", "HIGH")
        assert row.classification == "NOT-COVERED", key


def test_classifier_subflags():
    assert classify_anchor("M293", "ta", "MEDIUM").subflag == (
        "mentioned_behaviourally")
    assert classify_anchor("M011", "kaḷiṟu", "HIGH").subflag == "not_mentioned"


# -- the real 44 ------------------------------------------------------------

def test_flagged44_loads_exactly_44():
    flagged = load_flagged44(ANCHORS)
    assert len(flagged) == 44
    keys = [k for k, _, _ in flagged]
    assert keys == sorted(keys)
    assert "M293" in keys and "M402" in keys


def test_triage_counts_on_real_anchors():
    rows = triage_all(ANCHORS)
    assert len(rows) == 44
    counts = {}
    for r in rows:
        counts[r.classification] = counts.get(r.classification, 0) + 1
    assert counts == {"CONTESTED": 1, "NOT-COVERED": 43}
    contested = [r.sign for r in rows if r.classification == "CONTESTED"]
    assert contested == ["M402"]
    sub = {}
    for r in rows:
        sub[r.subflag] = sub.get(r.subflag, 0) + 1
    assert sub["not_mentioned"] + sub["mentioned_behaviourally"] == 43


def test_triage_rows_carry_readings_from_anchors():
    data = json.loads(ANCHORS.read_text("utf-8"))
    for r in triage_all(ANCHORS):
        assert r.reading == data["anchors"][r.sign]["reading"]


# -- disagreement table serialisation ---------------------------------------

def test_disagreement_table_rows_and_csv_roundtrip():
    rows = disagreement_table_rows()
    assert len(rows) == len(ALL_CASES)
    text = disagreement_csv()
    parsed = list(csv.DictReader(io.StringIO(text)))
    assert len(parsed) == len(rows)
    assert {p["case_id"] for p in parsed} == {r["case_id"] for r in rows}
    d10 = next(p for p in parsed if p["case_id"] == "BH-D10")
    assert d10["signs_involved"] == "M402"
    assert d10["is_dispute"] == "true"
    r01 = next(p for p in parsed if p["case_id"] == "BH-R01")
    assert r01["is_dispute"] == "false"


def test_count_labelled_e1():
    assert count_labelled_e1("x E1 (1): foo\nE1 (12): bar") == 2
    assert count_labelled_e1("no labels here") == 0


# -- H23 graph registration ---------------------------------------------------

def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase120BhaskarTriage" in ATOMIC_NODES


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
