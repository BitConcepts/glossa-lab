"""Unit tests for the Phase-109 follow-through machinery (spec 007).

Decision rules are pure functions over assembled evidence dicts, so
they are tested on synthetic evidence — no repo data files involved.
Apply functions are tested on synthetic anchors mappings.
"""
from __future__ import annotations

import copy

from glossa_lab.pipelines import phase109_followthrough as p109


def _ev(**over):
    ev = {
        "sign": "M999",
        "current": {"reading": "min", "confidence": "MEDIUM",
                    "basis": "Promoted from anchor staging archive",
                    "source": "anchor_staging_archive:x"},
        "register_category": "GRAMMAR",
        "register_reasons": [],
        "snapshots": [],
        "latest_snapshot_entry": None,
        "crosswalk": None,
        "ledger_assignments": [],
        "archive_entries": [],
        "a1_crosswalk_match": False,
        "a2_snapshot_same": False,
        "a3_ledger_matches": [],
        "a1_crosswalk_exact": False,
        "a2_snapshot_exact": False,
        "a3_ledger_exact_matches": [],
        "prior_sa_origin": False,
        "snapshots_agree": False,
        "prior_differs": False,
    }
    ev.update(over)
    return ev


def _snap(reading="vaN", confidence="HIGH", file="INDUS_FINAL_ANCHORS.backup_20260523_181449.json"):
    return [{"file": file, "reading": reading, "confidence": confidence}]


# ── Step 1 decision rules ────────────────────────────────────────────

def test_rule_a_via_crosswalk():
    d = p109.decide_staging(_ev(a1_crosswalk_exact=True,
                                crosswalk={"reading": "min", "source": "Parpola 1994"}))
    assert d["rule"] == "a" and d["action"] == "keep"


def test_rule_a_via_snapshot_same():
    d = p109.decide_staging(_ev(a2_snapshot_exact=True, snapshots=_snap("min")))
    assert d["rule"] == "a"


def test_rule_a_via_ledger_flags_handcheck():
    m = [{"header": "Phase-X", "line": 1, "assigned_raw": "min",
          "assigned_norm": "min", "snippet": "M999=min"}]
    d = p109.decide_staging(_ev(a3_ledger_exact_matches=m))
    assert d["rule"] == "a" and d["needs_handcheck"] is True


def test_rule_b_restore_prior():
    prior_entry = {"reading": "vaN", "confidence": "HIGH",
                   "basis": "DEDR 5231", "source": "Phase-89"}
    d = p109.decide_staging(_ev(
        snapshots=_snap(), snapshots_agree=True, prior_differs=True,
        latest_snapshot_entry=prior_entry))
    assert d["rule"] == "b" and d["action"] == "restore"
    assert d["prior"]["reading"] == "vaN"
    assert d["prior"]["confidence"] == "HIGH"
    assert d["needs_handcheck"] is True  # HIGH restoration is hand-checked


def test_rule_b_low_prior_not_flagged():
    prior_entry = {"reading": "kol", "confidence": "LOW",
                   "basis": "distributional", "source": "Phase-40"}
    d = p109.decide_staging(_ev(
        snapshots=_snap("kol", "LOW"), snapshots_agree=True,
        prior_differs=True, latest_snapshot_entry=prior_entry))
    assert d["rule"] == "b" and d["needs_handcheck"] is False


def test_rule_c_when_no_support_no_prior():
    d = p109.decide_staging(_ev())
    assert d["rule"] == "c" and d["action"] == "demote"


def test_rule_c_when_snapshots_disagree():
    # snapshots that disagree with each other are not a restorable source
    prior_entry = {"reading": "x", "confidence": "LOW"}
    d = p109.decide_staging(_ev(
        snapshots=_snap("x", "LOW"), snapshots_agree=False,
        prior_differs=True, latest_snapshot_entry=prior_entry))
    assert d["rule"] == "c"


def test_rule_order_a_beats_b():
    prior_entry = {"reading": "vaN", "confidence": "HIGH"}
    d = p109.decide_staging(_ev(
        a1_crosswalk_exact=True,
        crosswalk={"reading": "min", "source": "Parpola 1994"},
        snapshots=_snap(), snapshots_agree=True, prior_differs=True,
        latest_snapshot_entry=prior_entry))
    assert d["rule"] == "a"


def test_normalised_only_match_does_not_fire_rule_a():
    # kaL vs kal: identical under Phase-108 normalisation, different
    # readings exactly (spec 007 addendum) — must NOT keep.
    d = p109.decide_staging(_ev(
        a1_crosswalk_match=True,
        crosswalk={"reading": "kaL", "source": "Parpola 1994 App. B"}))
    assert d["rule"] == "c"
    assert any("A1 not counted" in n for n in d["notes"])


def test_sa_origin_prior_is_not_restorable():
    prior_entry = {"reading": "kur", "confidence": "MEDIUM",
                   "basis": "Phase-122 syllabic LM SA: modal='kur'",
                   "source": "Phase-122"}
    d = p109.decide_staging(_ev(
        snapshots=_snap("kur", "MEDIUM"), snapshots_agree=True,
        prior_differs=True, latest_snapshot_entry=prior_entry,
        prior_sa_origin=True))
    assert d["rule"] == "c"
    assert any("SA run" in s for s in d["support"])


def test_sa_origin_detection():
    assert p109._sa_origin({"source": "Phase-122",
                            "basis": "Phase-122 syllabic LM SA: modal"})
    assert p109._sa_origin({"source": "x", "basis": "CGSA run"})
    # A DEDR-sourced reading with a later SA-cons recal bracket is
    # NOT SA-origin (M042/M108 pattern).
    assert not p109._sa_origin({
        "source": "Phase-89 systematic DEDR (ICON, MEDIUM)",
        "basis": " [Phase-116 recal: SA-cons=0.62✓ DEDR✓]"})
    assert not p109._sa_origin(None)


def test_exact_segment_is_case_and_diacritic_sensitive():
    assert p109._exact_segment("kaL") != p109._exact_segment("kal")
    assert p109._exact_segment("vaN") == "vaN"
    assert p109._exact_segment("min (fish)") == "min"


# ── Apply functions ──────────────────────────────────────────────────

def _anchors_data():
    return {"anchors": {
        "M999": {"reading": "min", "confidence": "MEDIUM",
                 "basis": "Promoted from anchor staging archive",
                 "source": "anchor_staging_archive:x"},
        "M111": {"reading": "ta", "confidence": "HIGH",
                 "basis": "b", "source": "s"},
    }}


def test_apply_demote_one_tier():
    data = _anchors_data()
    ev = {"M999": _ev()}
    d = [p109.decide_staging(ev["M999"])]
    changes = p109.apply_staging_decisions(data, d, ev)
    assert data["anchors"]["M999"]["confidence"] == "LOW"
    assert "staging-heuristic origin, unvalidated" in \
        data["anchors"]["M999"]["phase109_annotation"]
    assert changes[0]["before"]["confidence"] == "MEDIUM"
    assert changes[0]["after"]["confidence"] == "LOW"


def test_apply_restore_replaces_entry_and_annotates():
    data = _anchors_data()
    prior_entry = {"reading": "vaN", "confidence": "HIGH",
                   "basis": "DEDR 5231", "source": "Phase-89"}
    ev = {"M999": _ev(snapshots=_snap(), snapshots_agree=True,
                      prior_differs=True, latest_snapshot_entry=prior_entry)}
    d = [p109.decide_staging(ev["M999"])]
    changes = p109.apply_staging_decisions(data, d, ev)
    e = data["anchors"]["M999"]
    assert e["reading"] == "vaN" and e["confidence"] == "HIGH"
    assert e["basis"] == "DEDR 5231"
    assert "RESTORED" in e["phase109_annotation"]
    assert changes[0]["action"] == "restore"


def test_apply_keep_annotates_only():
    data = _anchors_data()
    before = copy.deepcopy(data["anchors"]["M999"])
    ev = {"M999": _ev(a1_crosswalk_exact=True,
                      crosswalk={"reading": "min", "source": "Parpola 1994"})}
    d = [p109.decide_staging(ev["M999"])]
    p109.apply_staging_decisions(data, d, ev)
    e = data["anchors"]["M999"]
    assert e["reading"] == before["reading"]
    assert e["confidence"] == before["confidence"]
    assert "RETAINED" in e["phase109_annotation"]


def test_apply_sa_flags_never_touch_value_or_tier():
    data = _anchors_data()
    changes = p109.apply_sa_flags(data, {"M111": "SA_DERIVED"})
    e = data["anchors"]["M111"]
    assert e["reading"] == "ta" and e["confidence"] == "HIGH"
    assert e["validation_status"] == "pending_non_sa_validation"
    assert e["provenance_class"] == "SA_DERIVED"
    assert changes[0]["action"] == "flag"


def test_demote_map_edges():
    assert p109.DEMOTE == {"HIGH": "MEDIUM", "MEDIUM": "LOW",
                           "LOW": "CANDIDATE", "CANDIDATE": "CANDIDATE"}


def test_strict_subset_definition():
    anchors = {
        "M1": {"confidence": "HIGH"},     # clean
        "M2": {"confidence": "HIGH"},     # SA-derived
        "M3": {"confidence": "MEDIUM"},   # SA in chain (component)
        "M4": {"confidence": "LOW"},      # not H+M
        "M5": {"confidence": "MEDIUM"},   # clean
    }
    records = {
        "M1": {"category": "DEDR", "sa_in_chain": False},
        "M2": {"category": "SA_DERIVED", "sa_in_chain": True},
        "M3": {"category": "MIXED", "sa_in_chain": True},
        "M4": {"category": "GRAMMAR", "sa_in_chain": False},
        "M5": {"category": "GRAMMAR", "sa_in_chain": False},
    }
    assert p109.strict_sa_independent_hm(anchors, records) == {"M1", "M5"}


def test_regenerate_bookkeeping_counts():
    data = {"anchors": {
        "M1": {"confidence": "HIGH"}, "M2": {"confidence": "HIGH"},
        "M3": {"confidence": "MEDIUM"}, "M4": {"confidence": "LOW"},
        "M5": {"confidence": "CANDIDATE"}},
        "total": 999, "metadata": {}}
    out = p109.regenerate_bookkeeping(data, 0.5)
    assert out["total"] == 5 and out["hm"] == 3
    assert data["by_confidence"] == {"HIGH": 2, "MEDIUM": 1,
                                     "LOW": 1, "CANDIDATE": 1}
    assert data["metadata"]["hm_confirmed_count"] == 3
    assert data["corpus_token_coverage"] == 0.5
