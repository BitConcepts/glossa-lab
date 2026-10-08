"""Unit tests for the Phase-126 Wells-split descriptive
analysis of the 113 CANDIDATE anchors.

Covers: the analysis set is exactly the 113 CANDIDATE anchors
(disjoint from the 44 pending_non_sa_validation anchors,
which are excluded); the frozen headline counts (split 27 /
merge 4 / unit-same 62 / not-covered 1 / indeterminate 19);
every CANDIDATE gets exactly one record and none is dropped
(a sign absent from the witness table is recorded
not-covered); split components are recorded from the witness
table; the `basis` parser reads freq and the positional
profile; every cross-tab sums to 113; the build is
deterministic; the committed results JSON agrees with a
fresh build; the descriptive framing carries no adjudication
language; and the H23 graph registration.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.phase126_run import build_results  # noqa: E402
from glossa_lab.phase126_wells_split import (  # noqa: E402
    TREATMENT_ORDER, build_records, candidate_signs,
    headline_counts, parse_basis, pending_signs,
)

_REPO = Path(__file__).resolve().parent.parent.parent
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_RESULTS = _REPO / "reports" \
    / "phase126_wells_split_candidates_results.json"
_MEMO = _REPO / "reports" / "phase126_wells_split_candidates.md"
_ANCHORS_SHA256 = ("eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c8"
                   "6ebb1fa3b602cfaed")


def _anchors_doc():
    return json.loads(_ANCHORS.read_text("utf-8"))


# ── Analysis set ──────────────────────────────────────────

def test_candidate_set_exactly_113_disjoint_from_pending():
    doc = _anchors_doc()
    cand = candidate_signs(doc)
    pend = pending_signs(doc)
    assert len(cand) == 113
    assert len(pend) == 44
    assert not (set(cand) & pend)
    assert all(v["confidence"] == "CANDIDATE" for v in cand.values())


def test_every_candidate_recorded_none_dropped():
    results = build_results()
    assert len(results["records"]) == 113
    signs = [r["sign"] for r in results["records"]]
    assert len(set(signs)) == 113
    assert set(signs) == set(candidate_signs(_anchors_doc()))


def test_missing_witness_sign_recorded_not_covered():
    cand = {"M999": {"reading": "x", "confidence": "CANDIDATE",
                     "basis": "freq=2. I=0.000 T=0.000 M=1.000.",
                     "source": "Phase-111"}}
    records = build_records(cand, [])
    assert len(records) == 1
    assert records[0]["wells_treatment"] == "not-covered"
    assert records[0]["witness_present"] is False


# ── Headline counts / treatments ──────────────────────────

def test_headline_counts_frozen():
    results = build_results()
    assert results["headline_counts"] == {
        "split": 27, "merge": 4, "unit-same": 62,
        "not-covered": 1, "indeterminate": 19}
    assert sum(results["headline_counts"].values()) == 113


def test_treatment_vocabulary_closed():
    results = build_results()
    for r in results["records"]:
        assert r["wells_treatment"] in TREATMENT_ORDER


def test_split_components_recorded():
    results = build_results()
    splits = [r for r in results["records"]
              if r["wells_treatment"] == "split"]
    assert len(splits) == 27
    for r in splits:
        assert r["n_wells_graphemes"] >= 2
        assert len(r["wells_graphemes"]) == r["n_wells_graphemes"]
    m120 = next(r for r in splits if r["sign"] == "M120")
    assert m120["wells_graphemes"] == ["025", "026", "027", "028", "029"]
    assert results["split_size_distribution"] == {"2": 20, "3": 6, "5": 1}


def test_not_covered_and_indeterminate_listed():
    results = build_results()
    notcov = [r["sign"] for r in results["records"]
              if r["wells_treatment"] == "not-covered"]
    assert notcov == ["M312"]
    indet = [r for r in results["records"]
             if r["wells_treatment"] == "indeterminate"]
    assert len(indet) == 19
    for r in indet:
        assert r["witness_note"], "indeterminate rows state the reason"


# ── Basis parsing / anchor features ───────────────────────

def test_parse_basis():
    parsed = parse_basis(
        "Phase-111 allograph resolution: positional profile "
        "L1=0.000 matches M222 ('kur', MEDIUM). "
        "I=0.000 T=0.000 M=1.000. freq=4.")
    assert parsed["freq"] == 4
    assert parsed["profile"] == (0.0, 0.0, 1.0)
    assert parse_basis("") == {"freq": None, "profile": None}


def test_anchor_features_as_recorded():
    results = build_results()
    for r in results["records"]:
        assert r["reading"] == "kur"
        assert r["source"] == "Phase-111"
        assert r["validation_status"] == "premise_superseded"
        assert r["basis_profile"] == [0.0, 0.0, 1.0]
        assert r["basis_freq"] in (1, 2, 3, 4)
    freq_tab = results["cross_tabs"]["by_basis_freq"]
    assert {k: sum(v.values()) for k, v in freq_tab.items()} == {
        "1": 17, "2": 26, "3": 34, "4": 36}


def test_every_cross_tab_sums_to_113():
    results = build_results()
    for name, tab in results["cross_tabs"].items():
        for key, counts in tab.items():
            assert sum(counts.values()) <= 113, (name, key)
        assert sum(sum(c.values()) for c in tab.values()) == 113, name


def test_phase252_cohort_all_unit_same():
    results = build_results()
    cohort = [r for r in results["records"] if r["phase_upgraded"]]
    assert len(cohort) == 4
    assert all(r["wells_treatment"] == "unit-same" for r in cohort)
    assert all(r["has_dedr"] for r in cohort)


# ── Determinism / committed artifacts / guards ────────────

def test_build_is_deterministic():
    assert build_results() == build_results()


def test_committed_results_agree_with_fresh_build():
    committed = json.loads(_RESULTS.read_text("utf-8"))
    fresh = build_results()
    assert committed["headline_counts"] == fresh["headline_counts"]
    assert committed["records"] == fresh["records"]
    assert committed["cross_tabs"] == fresh["cross_tabs"]


def test_anchors_hash_unchanged():
    digest = hashlib.sha256(_ANCHORS.read_bytes()).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_no_adjudication_language():
    blob = (_RESULTS.read_text("utf-8") + _MEMO.read_text("utf-8")).lower()
    for banned in ("should be promoted", "should be demoted",
                   "we recommend promoting", "we recommend demoting",
                   "promote m", "demote m", "upgrade to medium",
                   "downgrade to low"):
        assert banned not in blob


def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase126WellsSplitCandidates" in ATOMIC_NODES
    # headline_counts helper agrees with the built records
    results = build_results()
    assert headline_counts(results["records"]) \
        == results["headline_counts"]
