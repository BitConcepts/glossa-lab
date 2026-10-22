"""Spec 029 Phase B — bundles, attribution, explanation, digestion
(FR-029-04…07; tasks B1–B5; OD-2, OD-3, OD-5).

Covers:
* B1  bundle representation: exactly the four governed sub-claim
      kinds, each a first-class record with evidence list, its own
      falsifier, and its own Phase A stage; the parent stage is
      computed as the minimum of sub-claim stages and stored as
      that computation's cache — never directly assignable,
      through either the Phase A service or the Phase B gate layer;
* B2  attribution template: prior readings with resolvable
      citations + a completeness basis (search record); OD-3 —
      contested caps the parent at ``checked``, unexamined carries
      no cap, and a durable adjudication record resolving the
      contest lifts the cap;
* B3  explanation record: named accountable human, artifact URI +
      stored content hash, challenge venue, AI-assistance
      disclosure; AI / process actors rejected as the named human
      (an AI drafter is permitted and recorded); the ``accepted``
      transition fails closed without a valid record and writes
      nothing;
* B4  digestion record: the three OD-5 classes, each with
      resolvable references and a validated program-independence
      field; the ``digested`` transition fails closed without
      independent engagement; adverse digestion (an unanswered
      refutation) flags the claim contested, blocks advance above
      ``checked``, and pulls the claim back by a recorded demotion;
* B5  discriminating controls (plan §2.4): every gate above is
      paired with a must-fail control whose positive twin passes —
      automated actor → ``explained``; human transition without an
      explanation record → ``accepted``; ``digested`` without
      independent engagement; a contested bundle rendering above
      ``checked``. If a control could not fail, the gate would be
      non-differential and the run INVALID.

All fixtures are synthetic: invented names, example.org
references, and a hash of a synthetic artifact string. No live
claim or anchor is promoted, decomposed, or given a gate record
by these tests (Phase B hard limit).
"""
from __future__ import annotations

import copy
import hashlib

import pytest

from glossa_lab.claim_bundle import (
    DIGESTION_CLASSES,
    PARENT_STAGE_SOURCE,
    SUBCLAIM_KINDS,
    BundleGateError,
    BundleValidationError,
    answer_adverse_digestion,
    attribution_is_contested,
    compute_parent_stage,
    contest_is_resolved,
    gated_transition_stage,
    get_subclaim,
    has_unanswered_refutation,
    is_valid_digestion_record,
    is_valid_explanation_record,
    make_adverse_digestion_record,
    make_attribution_subclaim,
    make_bundle,
    make_subclaim,
    record_adverse_digestion,
    serialize_bundle,
    sync_parent_stage,
    validate_attribution_subclaim,
)
from glossa_lab.claim_stage import (
    StageTransitionError,
    transition_stage,
    with_stage_defaults,
)

TS = "2026-10-12T12:00:00+00:00"

# Synthetic fixture persons (invented for these tests; not real scholars).
EXPLAINER = "Nadia Rahman"
CLAIM_AUTHOR = "Tomas Weber"
SCHOLAR = "Marcus Feld"
REVIEWER = "Priya Nair"
REFUTER = "Jonas Lindqvist"
SEARCHER = "Nadia Rahman"

ARTIFACT_HASH = hashlib.sha256(b"synthetic explanation artifact (test fixture)").hexdigest()
EXPLANATION_URI = "https://example.org/spec029/synthetic-explanation"
REFS = ["https://example.org/spec029/evidence-1"]


def valid_explanation_record(**overrides):
    rec = {
        "author": EXPLAINER,
        "artifact_uri": EXPLANATION_URI,
        "content_hash": ARTIFACT_HASH,
        "challenge_venue": "https://example.org/spec029/challenges",
        "ai_assistance_disclosure": (
            "Drafted with AI assistance; the named human author reviewed "
            "the account and takes responsibility for it."
        ),
        # An AI system recorded as drafter is permitted (OD-2) — it is
        # the named-human slot it may never occupy.
        "drafter": "Muse Spark (AI system)",
    }
    rec.update(overrides)
    return rec


def valid_digestion_record(cls="independent_reuse", **overrides):
    rec = {
        "digestion_class": cls,
        "independent_scholar": SCHOLAR,
        "scholar_is_claim_author": False,
        "scholar_is_program_staff": False,
        "references": ["https://doi.org/10.0000/synthetic-reuse"],
    }
    if cls == "independent_reuse":
        rec["reuse_reference"] = "https://doi.org/10.0000/synthetic-reuse"
    elif cls == "published_challenge_answered":
        rec["challenge_reference"] = "https://doi.org/10.0000/synthetic-challenge"
        rec["response_reference"] = "https://doi.org/10.0000/synthetic-response"
    elif cls == "mechanism_engaging_citation":
        rec["intake_reviewer"] = REVIEWER
        rec["intake_rationale"] = (
            "The citation works through the reading's mechanism, not a passing mention."
        )
    rec.update(overrides)
    return rec


def plain_claim(claim_id="synthetic-claim-001"):
    return with_stage_defaults({
        "claim_id": claim_id,
        "normalized_claim": "A synthetic claim used only as a Phase B test fixture.",
        "claim_status": "supported",
        "claim_authors": [CLAIM_AUTHOR],
    })


def advance(record, to_stage, **kwargs):
    kwargs.setdefault("actor", EXPLAINER)
    kwargs.setdefault("evidence_refs", REFS)
    kwargs.setdefault("timestamp", TS)
    return gated_transition_stage(record, to_stage, **kwargs)


def claim_at_accepted():
    rec = plain_claim()
    advance(rec, "created", actor="extraction", evidence_refs=[])
    advance(rec, "checked", actor="scoring", evidence_refs=[])
    advance(rec, "explained")
    advance(rec, "accepted", explanation_record=valid_explanation_record())
    return rec


def search_record():
    return {
        "corpora_searched": ["synthetic-corpus-a"],
        "literature_searched": ["synthetic-bibliography-b"],
        "searched_on": "2026-10-01",
        "searcher": SEARCHER,
    }


def attribution_subclaim(stage=None, contest_state="unexamined", contest_record=None):
    kwargs = {}
    if contest_state != "unexamined":
        kwargs = {
            "prior_readings": [{"citation": "https://doi.org/10.0000/prior-reading"}],
            "search_record": search_record(),
        }
    return make_attribution_subclaim(
        "synthetic-sub-attribution",
        proposition="All prior readings of this synthetic sign are accounted for.",
        evidence=REFS,
        falsification_condition="A prior reading absent from prior_readings defeats it.",
        contest_state=contest_state,
        contest_record=contest_record,
        stage=stage,
        timestamp=TS,
        **kwargs,
    )


def contest_record(**overrides):
    rec = {
        "contested_by": "Helena Brooks",
        "evidence": ["https://doi.org/10.0000/rival-attribution"],
        "contested_on": "2026-10-05",
    }
    rec.update(overrides)
    return rec


def bundle_parent(stages, contest_state="unexamined", contest=None, **parent_extra):
    """A synthetic bundle parent; *stages* maps kind -> stamped stage."""
    subs = []
    for kind in SUBCLAIM_KINDS:
        if kind == "attribution":
            subs.append(attribution_subclaim(
                stage=stages.get(kind), contest_state=contest_state, contest_record=contest))
        else:
            subs.append(make_subclaim(
                kind, f"synthetic-sub-{kind}",
                proposition=f"Synthetic proposition for {kind}.",
                evidence=REFS,
                falsification_condition=f"A synthetic falsifier for {kind}.",
                stage=stages.get(kind), timestamp=TS,
            ))
    parent = with_stage_defaults({"claim_id": "synthetic-bundle-001", **parent_extra})
    return make_bundle(parent, subs, timestamp=TS)


ALL_EXPLAINED = {kind: "explained" for kind in SUBCLAIM_KINDS}


# ── B1: bundle representation ────────────────────────────────────────────

def test_bundle_has_exactly_the_four_governed_kinds():
    parent = bundle_parent(ALL_EXPLAINED)
    assert [s["kind"] for s in parent["sub_claims"]] == list(SUBCLAIM_KINDS)
    for sub in parent["sub_claims"]:
        assert isinstance(sub["evidence"], list)
        assert sub["falsification_condition"]
        assert sub["stage"] == "explained"


def test_bundle_rejects_missing_duplicate_and_unknown_kinds():
    good = [make_subclaim(k, f"s-{k}", proposition="p", evidence=[],
                           falsification_condition="f") for k in SUBCLAIM_KINDS]
    parent = with_stage_defaults({"claim_id": "b-x"})
    with pytest.raises(BundleValidationError):
        make_bundle(parent, good[:3], timestamp=TS)  # one kind missing
    with pytest.raises(BundleValidationError):
        make_bundle(parent, good + [good[0]], timestamp=TS)  # duplicate kind
    with pytest.raises(BundleValidationError):
        make_subclaim("significance", "s-x", proposition="p", evidence=[],
                      falsification_condition="f")  # not a governed kind


def test_subclaim_requires_its_own_falsifier():
    with pytest.raises(BundleValidationError):
        make_subclaim("reading_soundness", "s-x", proposition="p", evidence=[],
                      falsification_condition="  ")


def test_parent_stage_is_the_minimum_of_subclaim_stages():
    parent = bundle_parent({
        "reading_soundness": "digested",
        "scholarship_accounting": "checked",
        "attribution": "accepted",
        "explanation_intelligibility": "explained",
    })
    assert compute_parent_stage(parent) == "checked"
    assert parent["stage"] == "checked"


def test_parent_stage_unstamped_subclaim_makes_parent_unstamped():
    stages = dict(ALL_EXPLAINED)
    stages["scholarship_accounting"] = None
    parent = bundle_parent(stages)
    assert compute_parent_stage(parent) is None
    assert parent["stage"] is None
    detail = parent["stage_computation"]
    assert detail["unstamped_subclaims"] == ["scholarship_accounting"]


def test_parent_stage_is_stored_as_the_computations_cache():
    parent = bundle_parent(ALL_EXPLAINED)
    assert parent["stage"] == "explained"
    assert parent["stage_source"] == PARENT_STAGE_SOURCE
    assert parent["stage_as_of"] == TS


def test_parent_stage_is_never_directly_assignable():
    parent = bundle_parent(ALL_EXPLAINED)
    before = copy.deepcopy(parent)
    with pytest.raises(StageTransitionError):
        transition_stage(parent, "accepted", actor=EXPLAINER, evidence_refs=REFS,
                         timestamp=TS)
    with pytest.raises(BundleGateError):
        gated_transition_stage(parent, "accepted", actor=EXPLAINER, evidence_refs=REFS,
                               timestamp=TS)
    assert parent == before  # refused transitions wrote nothing


def test_subclaim_stages_move_through_the_phase_a_service():
    parent = bundle_parent({k: "created" for k in SUBCLAIM_KINDS})
    assert parent["stage"] == "created"
    for sub in parent["sub_claims"]:
        transition_stage(sub, "checked", actor="scoring", timestamp=TS)
    assert sync_parent_stage(parent, timestamp=TS) == "checked"
    assert parent["stage"] == "checked"


def test_sync_records_a_computation_demotion_in_history():
    parent = bundle_parent(ALL_EXPLAINED)
    entries_before = len(parent["stage_history"])
    # A sub-claim is demoted (its own recorded transition, Phase A service).
    sub = get_subclaim(parent, "reading_soundness")
    transition_stage(sub, "created", actor=EXPLAINER, reason="synthetic demotion",
                     evidence_refs=REFS, timestamp=TS)
    sync_parent_stage(parent, timestamp=TS)
    assert parent["stage"] == "created"
    new_entries = parent["stage_history"][entries_before:]
    assert any(e["from_stage"] == "explained" and e["to_stage"] == "created"
               and e["actor"] == "bundle-minimum-computation" for e in new_entries)


def test_bundle_machinery_does_not_touch_lane1_fields():
    parent = bundle_parent(ALL_EXPLAINED, claim_status="supported", confidence=0.5)
    assert parent["claim_status"] == "supported"
    assert parent["confidence"] == 0.5


# ── B2: attribution template + OD-3 cap ──────────────────────────────────

def test_attribution_template_validates_when_complete_and_uncontested():
    sub = attribution_subclaim(stage="checked", contest_state="uncontested")
    validate_attribution_subclaim(sub)  # no raise
    assert not attribution_is_contested(sub)


def test_attribution_template_rejects_incomplete_accounting():
    base = attribution_subclaim(stage="checked", contest_state="uncontested")
    for defect in (
        {"prior_readings": []},
        {"prior_readings": [{"citation": "an unresolvable bare title"}]},
        {"search_record": None},
        {"search_record": {**search_record(), "searcher": "extraction pipeline"}},
        {"search_record": {**search_record(), "corpora_searched": []}},
    ):
        broken = copy.deepcopy(base)
        broken.update(defect)
        with pytest.raises(BundleValidationError):
            validate_attribution_subclaim(broken)


def test_contested_attribution_requires_a_contest_record():
    with pytest.raises(BundleValidationError):
        attribution_subclaim(stage="checked", contest_state="contested", contest_record=None)
    broken = contest_record(evidence=["not a resolvable reference"])
    with pytest.raises(BundleValidationError):
        attribution_subclaim(stage="checked", contest_state="contested", contest_record=broken)


def test_contested_attribution_caps_parent_at_checked():
    # Differential pair: identical sub-claim stages; only the contest
    # state differs. Uncontested computes to the minimum; contested
    # is capped at checked (OD-3).
    free = bundle_parent(ALL_EXPLAINED, contest_state="uncontested")
    assert compute_parent_stage(free) == "explained"
    capped = bundle_parent(ALL_EXPLAINED, contest_state="contested",
                           contest=contest_record())
    assert compute_parent_stage(capped) == "checked"
    assert capped["stage"] == "checked"
    assert capped["stage_computation"]["attribution_contested"] is True
    assert capped["stage_computation"]["caps_applied"]


def test_unexamined_attribution_carries_no_cap():
    parent = bundle_parent(ALL_EXPLAINED, contest_state="unexamined")
    attribution = get_subclaim(parent, "attribution")
    assert attribution["prior_readings"] == []  # honestly unexamined
    assert not attribution_is_contested(attribution)
    # The bundle minimum rule alone applies: no OD-3 cap.
    assert compute_parent_stage(parent) == "explained"


def test_resolved_contest_lifts_the_cap():
    resolved = contest_record(resolution={
        "adjudication_ref": "https://example.org/spec029/adjudication-1",
        "resolved_on": "2026-10-10",
        "resolved_by": REVIEWER,
    })
    parent = bundle_parent(ALL_EXPLAINED, contest_state="contested", contest=resolved)
    attribution = get_subclaim(parent, "attribution")
    assert contest_is_resolved(attribution)
    assert not attribution_is_contested(attribution)
    assert compute_parent_stage(parent) == "explained"


def test_unresolvable_resolution_does_not_lift_the_cap():
    # A resolution whose adjudication reference does not resolve is
    # rejected at record creation (the template validator) …
    fake = contest_record(resolution={
        "adjudication_ref": "a note somewhere, trust me",
        "resolved_on": "2026-10-10",
        "resolved_by": REVIEWER,
    })
    with pytest.raises(BundleValidationError):
        attribution_subclaim(stage="checked", contest_state="contested",
                             contest_record=fake)
    # … and if such a defective resolution reaches the computation
    # on a stored record anyway, the computation fails closed too:
    # the cap stays on.
    resolved = contest_record(resolution={
        "adjudication_ref": "https://example.org/spec029/adjudication-1",
        "resolved_on": "2026-10-10",
        "resolved_by": REVIEWER,
    })
    parent = bundle_parent(ALL_EXPLAINED, contest_state="contested", contest=resolved)
    attribution = get_subclaim(parent, "attribution")
    attribution["contest_record"]["resolution"]["adjudication_ref"] = \
        "a note somewhere, trust me"
    assert attribution_is_contested(attribution)
    assert compute_parent_stage(parent) == "checked"


# ── B3: explanation record + the accepted gate ───────────────────────────

def test_explanation_record_valid_with_ai_drafter_recorded():
    # Positive control: an AI drafter is permitted; the named human
    # is accountable.
    assert is_valid_explanation_record(valid_explanation_record())


@pytest.mark.parametrize("author", [
    "Muse Spark",            # an AI system named as the human
    "GPT-4",                   # an AI system named as the human
    "AI Assistant",            # an AI role named as the human
    "extraction pipeline",     # a process name
    "",                        # missing
    None,                      # missing
    ["Nadia Rahman", "Tomas Weber"],  # not ONE accountable human
])
def test_explanation_record_rejects_non_human_authors(author):
    assert not is_valid_explanation_record(valid_explanation_record(author=author))


@pytest.mark.parametrize("defect", [
    {"artifact_uri": None},
    {"artifact_uri": "a bare title, not a reference"},
    {"content_hash": None},
    {"content_hash": "not-a-sha256-hash"},
    {"challenge_venue": ""},
    {"ai_assistance_disclosure": ""},
    {"ai_assistance_disclosure": None},
])
def test_explanation_record_rejects_missing_artifact_fields(defect):
    assert not is_valid_explanation_record(valid_explanation_record(**defect))


def test_control_accepted_without_explanation_record_fails_closed():
    # B5 must-fail control: a named-human transition to accepted
    # with no explanation record is refused and writes nothing.
    rec = plain_claim()
    advance(rec, "created", actor="extraction", evidence_refs=[])
    advance(rec, "checked", actor="scoring", evidence_refs=[])
    advance(rec, "explained")
    before = copy.deepcopy(rec)
    with pytest.raises(BundleGateError):
        advance(rec, "accepted")
    assert rec == before
    # An invalid record (AI as the named human) fails the same way.
    with pytest.raises(BundleGateError):
        advance(rec, "accepted",
                explanation_record=valid_explanation_record(author="Muse Spark"))
    assert rec == before


def test_accepted_with_valid_explanation_record_passes():
    rec = claim_at_accepted()
    assert rec["stage"] == "accepted"
    assert rec["explanation_record"]["author"] == EXPLAINER
    assert rec["stage_history"][-1]["to_stage"] == "accepted"


# ── B4: digestion record + the digested gate ─────────────────────────────

@pytest.mark.parametrize("cls", list(DIGESTION_CLASSES))
def test_each_digestion_class_validates(cls):
    assert is_valid_digestion_record(
        valid_digestion_record(cls), claim_authors=[CLAIM_AUTHOR])


@pytest.mark.parametrize("cls", list(DIGESTION_CLASSES))
def test_digested_transition_passes_for_each_class(cls):
    rec = claim_at_accepted()
    advance(rec, "digested", digestion_record=valid_digestion_record(cls),
            claim_authors=[CLAIM_AUTHOR])
    assert rec["stage"] == "digested"
    assert rec["digestion_record"]["digestion_class"] == cls


def test_control_digested_without_digestion_record_fails_closed():
    rec = claim_at_accepted()
    before = copy.deepcopy(rec)
    with pytest.raises(BundleGateError):
        advance(rec, "digested", claim_authors=[CLAIM_AUTHOR])
    assert rec == before


@pytest.mark.parametrize("defect", [
    {"scholar_is_claim_author": True},       # the scholar authored the claim
    {"scholar_is_program_staff": True},      # program staff, not independent
    {"independent_scholar": CLAIM_AUTHOR},   # cross-check against the author list
    {"independent_scholar": "Muse Spark"},  # not a human scholar
    {"references": []},                      # no engagement reference
    {"references": ["a bare title"]},        # unresolvable reference
])
def test_digestion_record_rejects_non_independent_or_unreferenced(defect):
    assert not is_valid_digestion_record(
        valid_digestion_record(**defect), claim_authors=[CLAIM_AUTHOR])


def test_digestion_record_rejects_missing_independence_fields():
    rec = valid_digestion_record()
    del rec["scholar_is_claim_author"]  # missing is a failure, fail-closed
    assert not is_valid_digestion_record(rec, claim_authors=[CLAIM_AUTHOR])
    rec = valid_digestion_record()
    del rec["scholar_is_program_staff"]
    assert not is_valid_digestion_record(rec, claim_authors=[CLAIM_AUTHOR])


@pytest.mark.parametrize("cls,defect", [
    ("independent_reuse", {"reuse_reference": None}),
    ("published_challenge_answered", {"response_reference": None}),
    ("published_challenge_answered", {"challenge_reference": "not resolvable"}),
    ("mechanism_engaging_citation", {"intake_reviewer": None}),
    ("mechanism_engaging_citation", {"intake_reviewer": "scoring service"}),
    ("mechanism_engaging_citation", {"intake_rationale": ""}),
])
def test_digestion_record_rejects_class_specific_defects(cls, defect):
    assert not is_valid_digestion_record(
        valid_digestion_record(cls, **defect), claim_authors=[CLAIM_AUTHOR])


def test_digested_also_requires_the_explanation_record_to_still_validate():
    rec = claim_at_accepted()
    rec["explanation_record"] = valid_explanation_record(author="Muse Spark")
    with pytest.raises(BundleGateError):
        advance(rec, "digested", digestion_record=valid_digestion_record(),
                claim_authors=[CLAIM_AUTHOR])
    assert rec["stage"] == "accepted"


# ── B4 continued: adverse digestion ──────────────────────────────────────

def adverse_record():
    return make_adverse_digestion_record(
        refuted_by=REFUTER,
        reference="https://doi.org/10.0000/synthetic-refutation",
        recorded_on="2026-10-11",
        summary="A synthetic substantive refutation, unanswered.",
    )


def test_adverse_digestion_flags_and_pulls_back_a_plain_claim():
    rec = claim_at_accepted()
    record_adverse_digestion(rec, adverse_record(), actor=EXPLAINER, timestamp=TS)
    assert rec["contested"] is True
    assert has_unanswered_refutation(rec)
    assert rec["stage"] == "checked"  # pulled back from accepted
    demotion = rec["stage_history"][-1]
    assert demotion["from_stage"] == "accepted" and demotion["to_stage"] == "checked"
    assert "adverse digestion" in demotion["reason"]


def test_adverse_digestion_blocks_advance_until_answered():
    rec = claim_at_accepted()
    record_adverse_digestion(rec, adverse_record(), actor=EXPLAINER, timestamp=TS)
    with pytest.raises(BundleGateError):
        advance(rec, "explained")
    answer_adverse_digestion(
        rec, response_reference="https://doi.org/10.0000/synthetic-answer",
        answered_by=EXPLAINER, timestamp=TS)
    assert rec["contested"] is False
    assert not has_unanswered_refutation(rec)
    advance(rec, "explained")  # the block is lifted
    assert rec["stage"] == "explained"


def test_adverse_digestion_pulls_back_a_bundle_parent():
    stages = {kind: "accepted" for kind in SUBCLAIM_KINDS}
    parent = bundle_parent(stages, contest_state="uncontested")
    assert parent["stage"] == "accepted"
    record_adverse_digestion(parent, adverse_record(), actor=EXPLAINER, timestamp=TS)
    assert parent["contested"] is True
    assert parent["stage"] == "checked"  # the computation's adverse cap
    rendered = serialize_bundle(parent)
    assert rendered["contested"] is True
    assert rendered["stage"]["stage"] == "checked"


# ── B5: discriminating controls ──────────────────────────────────────────

def test_control_automated_actor_cannot_reach_explained():
    rec = plain_claim()
    advance(rec, "created", actor="extraction", evidence_refs=[])
    advance(rec, "checked", actor="scoring", evidence_refs=[])
    before = copy.deepcopy(rec)
    with pytest.raises(StageTransitionError):
        gated_transition_stage(rec, "explained", actor="scoring",
                               evidence_refs=REFS, timestamp=TS)
    with pytest.raises(StageTransitionError):
        gated_transition_stage(rec, "explained", actor=EXPLAINER,
                               actor_kind="automated", evidence_refs=REFS, timestamp=TS)
    assert rec == before
    # Positive twin: the same move by a named human passes.
    advance(rec, "explained")
    assert rec["stage"] == "explained"


def test_control_contested_bundle_never_renders_above_checked():
    parent = bundle_parent(
        {kind: "digested" for kind in SUBCLAIM_KINDS},
        contest_state="contested", contest=contest_record())
    rendered = serialize_bundle(parent)
    # Even with every sub-claim stamped digested, the contested
    # parent's computed and rendered stage is capped at checked,
    # and the contest itself renders with the parent.
    assert rendered["stage"]["stage"] == "checked"
    assert rendered["attribution_contested"] is True
    assert rendered["contest_record"]["contested_by"] == "Helena Brooks"
    sub_stages = {s["kind"]: s["stage"]["stage"] for s in rendered["sub_claims"]}
    assert sub_stages["attribution"] == "digested"  # the cap, not the minimum, binds
