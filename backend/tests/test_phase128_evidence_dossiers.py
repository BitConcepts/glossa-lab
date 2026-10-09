"""Unit tests for the Phase-128 integrated evidence dossiers.

Join integrity: 44 pending anchors in = 44 dossiers out; every
source field traceable (each dossier block carries a provenance
pointer naming its source file and row key); missing join keys
are recorded NOT-COVERED, never inferred. Bucket rules are
tested as pure predicates, including edge cases (residual
exclusivity, multi-membership of buckets 1-4, the discrepancy
route into segmentation-contested, the not-covered conjunction).
Real-input pins: Bhaskar CONTESTED is exactly {M402}; exactly
one pending anchor (M072) is Phase-125 judgeable / Phase-127
per-pair; M281 has no crosswalk row; the anchors file sha256 is
the frozen baseline. This phase is descriptive only — no test
here issues or implies a verdict on any anchor.
"""
import csv
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.phase128_dossiers import (  # noqa: E402
    EXPECTED_ANCHORS_SHA256,
    NOT_COVERED,
    build_dossiers,
    classify_buckets,
    pending_anchor_ids,
    phase126_class,
)
from glossa_lab.phase128_run import dossier_csv_rows, render_csv  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent.parent


def _doc():
    return build_dossiers(_REPO)


def _fields(**over):
    base = {
        "bhaskar_classification": "NOT-COVERED",
        "wells_treatment": "SAME",
        "wells_determinate": True,
        "wells_contested": False,
        "cw_present": True,
        "cw_conflict": False,
        "p125_present": True,
        "p127_present": False,
    }
    base.update(over)
    return base


# ── Bucket-rule unit tests (pure predicates) ─────────────────

def test_bucket_evidence_complete_requires_all_four():
    assert classify_buckets(_fields(p127_present=True)) == [
        "evidence-complete"
    ]
    # dropping any one leg removes it (falls to the residual)
    assert classify_buckets(_fields(wells_determinate=False)) == [
        "evidence-thin"
    ]
    assert classify_buckets(_fields(cw_present=False)) == ["evidence-thin"]
    assert classify_buckets(_fields(p125_present=False)) == ["evidence-thin"]


def test_bucket_segmentation_contested_via_split_and_via_discrepancy():
    assert "segmentation-contested" in classify_buckets(
        _fields(wells_treatment="SPLIT", wells_contested=True)
    )
    # discrepancy route: treatment SAME but verification discrepancy
    # is encoded upstream in wells_contested
    assert "segmentation-contested" in classify_buckets(
        _fields(wells_contested=True)
    )


def test_bucket_crosswalk_contested():
    assert "crosswalk-contested" in classify_buckets(
        _fields(cw_conflict=True)
    )
    assert "crosswalk-contested" not in classify_buckets(_fields())


def test_bucket_not_covered_conjunction():
    f = _fields(
        wells_treatment="INDETERMINATE",
        wells_determinate=False,
        p125_present=False,
    )
    assert classify_buckets(f) == ["not-covered"]
    # Bhaskar CONTESTED breaks the conjunction -> residual
    f2 = _fields(
        bhaskar_classification="CONTESTED",
        wells_treatment="INDETERMINATE",
        wells_determinate=False,
        p125_present=False,
    )
    assert classify_buckets(f2) == ["evidence-thin"]
    # a Phase-125 record breaks it too
    f3 = _fields(
        wells_treatment="NOT-COVERED",
        wells_determinate=False,
        p125_present=True,
    )
    assert classify_buckets(f3) == ["evidence-thin"]


def test_bucket_multi_membership_and_residual_exclusivity():
    f = _fields(
        wells_treatment="SPLIT",
        wells_contested=True,
        cw_conflict=True,
        p127_present=True,
    )
    out = classify_buckets(f)
    assert "evidence-complete" in out
    assert "segmentation-contested" in out
    assert "crosswalk-contested" in out
    assert "evidence-thin" not in out


def test_phase126_class_map():
    assert phase126_class("SAME") == "unit-same"
    assert phase126_class("SPLIT") == "split"
    assert phase126_class("MERGE") == "merge"
    assert phase126_class("NOT-COVERED") == "not-covered"
    assert phase126_class("INDETERMINATE") == "indeterminate"
    assert phase126_class(None) is None


# ── Real-input join integrity ────────────────────────────────

def test_pending_universe_is_exactly_44():
    anchors = json.loads(
        (_REPO / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text(
            encoding="utf-8"
        )
    )
    ids = pending_anchor_ids(anchors)
    assert len(ids) == 44
    assert ids == sorted(ids)


def test_join_integrity_44_in_44_out():
    doc = _doc()
    assert doc["n_dossiers"] == 44
    assert [d["anchor_id"] for d in doc["dossiers"]] == pending_anchor_ids(
        json.loads(
            (_REPO / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text(
                encoding="utf-8"
            )
        )
    )
    # buckets partition-cover: every anchor in >= 1 bucket, and
    # bucket membership lists match per-dossier buckets exactly
    seen = [s for members in doc["buckets"].values() for s in members]
    for d in doc["dossiers"]:
        assert d["buckets"], d["anchor_id"]
        for b in d["buckets"]:
            assert d["anchor_id"] in doc["buckets"][b]
    assert set(seen) == {d["anchor_id"] for d in doc["dossiers"]}


def test_anchors_hash_frozen_and_unchanged():
    doc = _doc()
    assert doc["anchors_sha256_before"] == EXPECTED_ANCHORS_SHA256
    assert doc["anchors_unchanged"] is True


def test_every_block_has_provenance():
    doc = _doc()
    for d in doc["dossiers"]:
        for key in (
            "anchor",
            "bhaskar_phase120",
            "wells_phase123",
            "wells_phase126_class",
            "crosswalk_phase122",
            "phase125_cross_compilation",
            "phase127_diagnostic",
            "soviet_spec020_limitation",
        ):
            assert d[key].get("provenance"), (d["anchor_id"], key)


def test_bhaskar_contested_is_exactly_m402():
    doc = _doc()
    contested = [
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["bhaskar_phase120"].get("classification") == "CONTESTED"
    ]
    assert contested == ["M402"]
    nc = [
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["bhaskar_phase120"].get("classification") == NOT_COVERED
    ]
    assert len(nc) == 43


def test_phase125_and_127_coverage_pins():
    doc = _doc()
    judgeable = [
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["phase125_cross_compilation"].get("judgeable")
    ]
    assert judgeable == ["M072"]
    p127 = [
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["phase127_diagnostic"].get("status")
        == "in_judgeable_pair_set"
    ]
    assert p127 == ["M072"]
    m072 = next(d for d in doc["dossiers"] if d["anchor_id"] == "M072")
    assert m072["phase127_diagnostic"]["pair_key"] == "P058-M072"
    assert m072["phase127_diagnostic"]["bootstrap_ci"]["median"] == 1.0
    present125 = [
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["phase125_cross_compilation"]["status"]
        == "in_primary_records"
    ]
    assert len(present125) == 36


def test_missing_joins_recorded_not_covered():
    doc = _doc()
    m281 = next(d for d in doc["dossiers"] if d["anchor_id"] == "M281")
    assert m281["crosswalk_phase122"]["status"] == NOT_COVERED
    assert m281["crosswalk_phase122"]["n_rows"] == 0
    assert m281["phase125_cross_compilation"]["status"] == NOT_COVERED
    assert "not-covered" in m281["buckets"]
    # every dossier carries the uniform spec-020 limitation
    for d in doc["dossiers"]:
        assert d["soviet_spec020_limitation"]["value"] == (
            "NOT-EVALUABLE-VIA-SOVIET-DATASET"
        )


def test_wells_pending_breakdown_matches_phase123_memo():
    doc = _doc()
    from collections import Counter

    treatments = Counter(
        d["wells_phase123"]["treatment"] for d in doc["dossiers"]
    )
    assert treatments == {
        "SAME": 25,
        "SPLIT": 13,
        "MERGE": 1,
        "NOT-COVERED": 1,
        "INDETERMINATE": 4,
    }


def test_csv_rendering_is_flat_44_rows():
    doc = _doc()
    rows = dossier_csv_rows(doc)
    assert len(rows) == 44
    parsed = list(csv.DictReader(io.StringIO(render_csv(doc))))
    assert len(parsed) == 44
    assert {r["anchor_id"] for r in parsed} == {
        d["anchor_id"] for d in doc["dossiers"]
    }


def test_bucket_counts_sum_consistency():
    doc = _doc()
    counts = doc["bucket_counts"]
    # buckets 1-4 may overlap; evidence-thin is the residual, so
    # thin + (anchors in >=1 of buckets 1-4) == 44
    non_thin = {
        d["anchor_id"]
        for d in doc["dossiers"]
        if d["buckets"] != ["evidence-thin"]
    }
    assert counts["evidence-thin"] + len(non_thin) == 44
    assert counts["not-covered"] == 3
