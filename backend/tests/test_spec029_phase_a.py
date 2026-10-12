"""Spec 029 Phase A — stage axis core (FR-029-01…03; tasks A1–A5).

Covers:
* A1  record shapes: stage defaults are unstamped (never invented),
      stamped values carry through verbatim, serialization carries
      provenance + history summary;
* A2  AEE mapping: the stage axis maps as a distinct object in
      ``Claim.metadata``, never into ``ClaimStatus`` / confidence,
      and score propagation over the current claim set is
      byte-identical to the pre-change behaviour — the expected
      scores in ``fixtures/spec029_pre_change_aee_scores.json`` were
      captured from the code at main ``a38cf92e`` (pre-Phase-A)
      before any Phase A edit;
* A3  transition service: one-step-forward legality, reasoned
      demotion, automated allowlist fail-closed above ``checked``
      (discriminating control), named-human requirement above
      ``checked`` (a process name never validates), atomic
      stage/source/as_of writes with an appended history entry;
* A4  endpoint serialization: ``GET /claims``,
      ``GET /claims/aee-scores`` and the anchor (signs) surface
      serialize stage and lane-1 score as distinct objects;
* A5  risk flag: the audit's flagged shapes (the 8 supported-class
      extracted-claim records at band ``high`` staged below
      ``explained``, and the partially_falsified record at band
      ``high``) are flagged; explained-and-above and non-supported,
      non-high shapes are not; a confidence tier alone never fires
      the flag.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from aee.model import ClaimStatus

from glossa_lab.aee_core import assessment_summary, claim_from_glossa
from glossa_lab.claim_stage import (
    STAGES,
    StageTransitionError,
    compute_verified_unexplained,
    is_named_human,
    serialize_stage,
    stage_defaults,
    transition_stage,
    with_stage_defaults,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REAL_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_ANCHORS_FILE = _REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_PRE_CHANGE_SCORES = (
    Path(__file__).resolve().parent / "fixtures" / "spec029_pre_change_aee_scores.json"
)

HUMAN = "Tristen Pierson"
TS = "2026-10-12T12:00:00+00:00"


def _record(stage=None, **extra):
    rec: dict = {"claim_id": "t_stage_001"}
    if stage is not None:
        rec.update({
            "stage": stage,
            "stage_source": "test-fixture",
            "stage_as_of": "2026-10-12T00:00:00+00:00",
            "stage_history": [],
        })
    rec.update(extra)
    return rec


# ── A1: record shapes ────────────────────────────────────────────────────

def test_stage_vocabulary_is_tao_verbatim_in_order():
    assert STAGES == ("created", "checked", "explained", "accepted", "digested")


def test_stage_defaults_are_unstamped_never_invented():
    d = stage_defaults()
    assert d == {"stage": None, "stage_source": None, "stage_as_of": None,
                 "stage_history": []}
    out = with_stage_defaults({"claim_id": "x", "claim_status": "untested"})
    assert out["stage"] is None and out["stage_source"] is None
    assert out["stage_history"] == []
    assert out["claim_status"] == "untested"  # existing fields untouched


def test_with_stage_defaults_preserves_stamped_values():
    stamped = _record("checked", stage_history=[{"from_stage": "created",
                                                 "to_stage": "checked",
                                                 "actor": "extraction",
                                                 "timestamp": TS,
                                                 "evidence_refs": [],
                                                 "reason": ""}])
    out = with_stage_defaults(stamped)
    assert out["stage"] == "checked"
    assert out["stage_source"] == "test-fixture"
    assert len(out["stage_history"]) == 1


def test_serialize_stage_unstamped_and_stamped():
    unstamped = serialize_stage({"claim_id": "x"})
    assert unstamped["stage"] is None
    assert unstamped["stamped"] is False
    assert unstamped["stage_history_count"] == 0
    assert unstamped["latest_transition"] is None

    stamped = serialize_stage(_record("created", stage_history=[
        {"from_stage": None, "to_stage": "created", "actor": "extraction",
         "timestamp": TS, "evidence_refs": ["doc:1"], "reason": ""},
    ]))
    assert stamped["stage"] == "created"
    assert stamped["stamped"] is True
    assert stamped["stage_source"] == "test-fixture"
    assert stamped["stage_as_of"] == "2026-10-12T00:00:00+00:00"
    assert stamped["stage_history_count"] == 1
    assert stamped["latest_transition"]["to_stage"] == "created"


def test_serialize_stage_rejects_unknown_stage():
    with pytest.raises(ValueError):
        serialize_stage({"stage": "settled"})


# ── A2: AEE mapping + byte-identical score propagation ───────────────────

def test_stage_maps_as_distinct_object_not_status_or_confidence():
    raw = {
        "claim_id": "t_stage_a2",
        "source_document_id": "doc_a2",
        "claim_type": "language_claim",
        "normalized_claim": "A claim with a stamped stage.",
        "claim_status": "supported",
        "confidence_in_source": 0.5,
        "stage": "checked",
        "stage_source": "test-fixture",
        "stage_as_of": "2026-10-12T00:00:00+00:00",
        "stage_history": [],
    }
    claim = claim_from_glossa(raw)
    # Stage is its own object in metadata …
    assert claim.metadata["glossa_stage"]["stage"] == "checked"
    assert claim.metadata["glossa_stage"]["stage_source"] == "test-fixture"
    # … never folded into ClaimStatus (that still maps claim_status) …
    assert claim.status is ClaimStatus.SUPPORTED
    # … and never into confidence (still confidence_in_source here).
    assert claim.confidence == 0.5


def test_stage_absent_maps_to_none_not_invented():
    claim = claim_from_glossa({
        "claim_id": "t_stage_a2b",
        "normalized_claim": "No stage on this record.",
        "claim_status": "untested",
    })
    assert claim.metadata["glossa_stage"]["stage"] is None
    assert claim.metadata["glossa_stage"]["stamped"] is False
    assert claim.status is ClaimStatus.DRAFT


def test_score_propagation_byte_identical_to_pre_change():
    """A2 regression: every current claim's AEE score dict equals the
    score captured from the pre-change code (main a38cf92e)."""
    if not _REAL_CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    expected = json.loads(_PRE_CHANGE_SCORES.read_text(encoding="utf-8"))
    summary = assessment_summary(_REAL_CLAIMS_DIR)
    assert summary["total_claims"] == len(expected)
    for entry in summary["claims"]:
        want = expected[entry["claim_id"]]
        got = entry["aee_score"]
        assert got == want, entry["claim_id"]
        # Byte-identical under the canonical serialization.
        assert json.dumps(got, sort_keys=True) == json.dumps(want, sort_keys=True)
        # The lane-1 alias carries the same score, as a distinct key.
        assert entry["lane1_score"] == want
    assert summary["mean_propagated_score"] == 0.484903


# ── A3: transition service ───────────────────────────────────────────────

def test_forward_one_step_by_automated_actor():
    rec = _record()
    entry = transition_stage(rec, "created", actor="extraction", timestamp=TS)
    assert rec["stage"] == "created"
    assert entry["from_stage"] is None and entry["to_stage"] == "created"
    entry2 = transition_stage(rec, "checked", actor="scoring", timestamp=TS)
    assert rec["stage"] == "checked"
    assert entry2["from_stage"] == "created"
    # Every write updates stage, stage_source, stage_as_of together …
    assert rec["stage_as_of"] == TS
    assert rec["stage_source"] == "transition-service:stage_history[1]"
    # … and appends (never rewrites) history.
    assert [h["to_stage"] for h in rec["stage_history"]] == ["created", "checked"]


def test_forward_skip_is_illegal():
    rec = _record("created")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "explained", actor=HUMAN, timestamp=TS,
                         evidence_refs=["explanation:1"])
    assert rec["stage"] == "created"  # refused writes change nothing
    assert rec["stage_history"] == []


def test_unstamped_record_first_transition_is_created_only():
    rec = _record()
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "checked", actor="extraction", timestamp=TS)


def test_automated_actor_fail_closed_above_checked():
    """Discriminating control (plan §2.4): an automated actor attempting
    an ``explained`` transition must fail."""
    rec = _record("checked")
    for actor in ("extraction", "scoring", "research_loop", "batch_job"):
        with pytest.raises(StageTransitionError):
            transition_stage(rec, "explained", actor=actor, timestamp=TS,
                             evidence_refs=["explanation:1"])
    assert rec["stage"] == "checked"
    assert rec["stage_history"] == []


def test_automated_actor_cannot_touch_records_above_checked():
    rec = _record("explained")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "checked", actor="extraction", timestamp=TS,
                         reason="automated demotion attempt")


def test_named_human_can_advance_above_checked_with_evidence():
    rec = _record("checked")
    entry = transition_stage(rec, "explained", actor=HUMAN, timestamp=TS,
                             evidence_refs=["explanation:artifact-1"])
    assert rec["stage"] == "explained"
    assert entry["actor"] == HUMAN
    assert entry["evidence_refs"] == ["explanation:artifact-1"]


def test_process_name_never_validates_as_human():
    assert not is_named_human("research_loop")
    assert not is_named_human("Glossa Lab pipeline")
    assert not is_named_human("batch job")
    assert not is_named_human("")
    assert is_named_human(HUMAN)
    rec = _record("checked")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "explained", actor="research_loop", timestamp=TS,
                         evidence_refs=["explanation:1"])
    # An explicit automated kind fails closed even under a human name.
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "explained", actor=HUMAN, actor_kind="automated",
                         timestamp=TS, evidence_refs=["explanation:1"])


def test_human_transition_above_checked_requires_evidence_refs():
    rec = _record("checked")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "explained", actor=HUMAN, timestamp=TS)


def test_backward_move_requires_recorded_reason():
    rec = _record("explained")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "created", actor=HUMAN, timestamp=TS)
    entry = transition_stage(rec, "created", actor=HUMAN, timestamp=TS,
                             reason="explanation withdrawn by its author")
    assert rec["stage"] == "created"
    assert entry["from_stage"] == "explained"
    assert entry["reason"] == "explanation withdrawn by its author"
    assert rec["stage_source"] == "transition-service:stage_history[0]"


def test_backward_move_by_automated_actor_within_allowlist():
    rec = _record("checked")
    transition_stage(rec, "created", actor="extraction", timestamp=TS,
                     reason="extraction batch regenerated")
    assert rec["stage"] == "created"


def test_noop_and_unknown_stage_rejected():
    rec = _record("created")
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "created", actor="extraction", timestamp=TS)
    with pytest.raises(StageTransitionError):
        transition_stage(rec, "settled", actor=HUMAN, timestamp=TS)


# ── A5: risk flag ────────────────────────────────────────────────────────

def test_flag_supported_class_below_explained():
    for status in ("supported", "strongly_supported", "partially_supported"):
        assert compute_verified_unexplained(
            {"stage": "checked", "claim_status": status})
        assert compute_verified_unexplained(
            {"stage": "created", "claim_status": status})
        assert compute_verified_unexplained(
            {"stage": None, "claim_status": status})


def test_flag_high_band_below_explained_even_without_supported_status():
    # The audit's partially_falsified shape: status is not supported-class,
    # but the AEE band is high → flagged while below explained.
    assert compute_verified_unexplained(
        {"stage": "checked", "claim_status": "partially_falsified"},
        score={"band": "high"})


def test_flag_not_fired_at_or_above_explained():
    for stage in ("explained", "accepted", "digested"):
        assert not compute_verified_unexplained(
            {"stage": stage, "claim_status": "strongly_supported"},
            score={"band": "high"})


def test_flag_not_fired_for_weak_lane1_state():
    assert not compute_verified_unexplained(
        {"stage": "created", "claim_status": "untested"}, score={"band": "low"})
    assert not compute_verified_unexplained(
        {"stage": "checked", "claim_status": "contradicted"},
        score={"band": "unknown"})


def test_flag_supported_verdict_vocabulary():
    assert compute_verified_unexplained({"stage": "checked", "verdict": "SUPPORTED"})


def test_flag_confidence_tier_alone_never_fires():
    # Anchors carry a confidence tier, not a lane-1 verdict/band: the
    # tier alone must not fire the flag (Phase D stamps the audit's
    # strict-set flags from the ledger, not from tiers).
    assert not compute_verified_unexplained({"stage": "created", "confidence": "HIGH"})
    assert not compute_verified_unexplained({"stage": None, "confidence": "HIGH"})


def test_flag_on_current_claim_set_matches_audit_shapes():
    """The audit flagged the 8 supported-class extracted-claim records;
    with scores in hand the high-band partially_falsified record is
    flagged too (FR-029-03's high-band disjunct) — 9 in total, and no
    untested/contradicted record is flagged."""
    if not _REAL_CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    summary = assessment_summary(_REAL_CLAIMS_DIR)
    flagged = {e["claim_id"] for e in summary["claims"] if e["verified_unexplained"]}
    supported_class = {
        e["claim_id"] for e in summary["claims"]
        if e["glossa_claim_status"] in
        ("supported", "strongly_supported", "partially_supported")
    }
    assert len(supported_class) == 8
    assert supported_class <= flagged
    assert flagged == supported_class | {
        "indus_valley_script_deciphered_from_myth_65ff0a26_manual_002",
    }
    assert len(flagged) == 9


# ── A4: endpoint serialization ───────────────────────────────────────────

def test_claims_endpoint_serializes_stage_object_and_flag(client):
    r = client.get("/api/v1/indus-evidence/claims?limit=5")
    assert r.status_code == 200, r.text
    claims = r.json()["claims"]
    if not claims:
        pytest.skip("No extracted claims in evidence base")
    for c in claims:
        stage = c["stage"]
        assert isinstance(stage, dict)
        # Phase D (OD-1) has stamped the live records from the frozen
        # reclassification ledger: stamped, with ledger provenance.
        assert stage["stage"] in STAGES
        assert stage["stamped"] is True
        assert stage["stage_source"].startswith(
            "specs/029-tao-claim-lifecycle/reclassification-ledger.json:")
        assert stage["stage_as_of"] == "2026-10-12"
        assert "stage_source" in stage and "stage_history_count" in stage
        assert isinstance(c["verified_unexplained"], bool)
        # Lane separation: no lane-1 score is folded into the stage object.
        assert "aee_score" not in stage and "propagated_score" not in stage


def test_claims_endpoint_flag_filter(client):
    r = client.get("/api/v1/indus-evidence/claims?verified_unexplained=true")
    assert r.status_code == 200, r.text
    d = r.json()
    # Status-based flag (no scores requested): exactly the audit's
    # 8 supported-class records.
    assert d["total"] == 8
    assert all(c["verified_unexplained"] for c in d["claims"])


def test_claims_endpoint_aee_scores_are_distinct_lane1_object(client):
    r = client.get("/api/v1/indus-evidence/claims?aee=true&limit=5")
    assert r.status_code == 200, r.text
    for c in r.json()["claims"]:
        assert isinstance(c["stage"], dict)
        assert c["lane1_score"] == c["aee_score"]
        assert "stage" not in (c["aee_score"] or {})


def test_aee_scores_endpoint_serializes_stage_and_lane1_distinctly(client):
    r = client.get("/api/v1/indus-evidence/claims/aee-scores")
    assert r.status_code == 200, r.text
    d = r.json()
    if not d["claims"]:
        pytest.skip("No extracted claims in evidence base")
    for entry in d["claims"]:
        assert isinstance(entry["stage"], dict)
        # Phase D (OD-1) stamped every live claim from the ledger.
        assert entry["stage"]["stage"] in STAGES
        assert entry["stage"]["stamped"] is True
        assert entry["lane1_score"] == entry["aee_score"]
        assert isinstance(entry["verified_unexplained"], bool)
    flagged = [e for e in d["claims"] if e["verified_unexplained"]]
    assert len(flagged) == 9  # 8 supported-class + 1 high-band (see A5 test)


def test_anchor_surface_serializes_stage_object(client):
    # Every entry on the surface — final anchors and any staging /
    # anchor-set entries sharing the index — must carry the stage
    # object; check a full page, not a sample that could miss a
    # non-anchor entry source.
    r = client.get("/api/v1/signs?limit=500")
    assert r.status_code == 200, r.text
    items = r.json()["items"]
    if not items:
        pytest.skip("No signs in index")
    anchors_doc = json.loads(_ANCHORS_FILE.read_text("utf-8"))["anchors"]
    for item in items:
        assert isinstance(item["stage"], dict)
        if item["sign_id"] in anchors_doc:
            # Final anchors: Phase D (OD-1) stamped them from the ledger.
            assert item["stage"]["stage"] == anchors_doc[item["sign_id"]]["stage"]
            assert item["stage"]["stamped"] is True
            assert item["stage"]["stage_as_of"] == "2026-10-12"
        else:
            # Staging / anchor-set entries are not ledger records:
            # they stay unstamped — a stage is never invented.
            assert item["stage"]["stage"] is None
            assert item["stage"]["stamped"] is False
        assert isinstance(item["verified_unexplained"], bool)
        # The lane-1 confidence tier stays its own field, not a stage:
        # it is a tier string (HIGH/MEDIUM/LOW/UNCERTAIN/CANDIDATE),
        # never one of the lane-2 stage names.
        assert isinstance(item["confidence"], str) and item["confidence"]
        assert item["confidence"].lower() not in STAGES
    flagged = [i for i in items if i["verified_unexplained"]]
    assert len(flagged) == 94  # the audit's strict-set anchor flags (Phase D)
