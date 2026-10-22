"""Spec 029 Phase C — priority register and trails
(FR-029-11, FR-029-12; tasks C1–C3; claims F029-C08, F029-C09; OD-6).

Covers:
* C1  priority register: intake on record completeness alone —
      no score, stage, or verdict field exists on an entry;
      the public record is exactly claimant + server timestamp
      + SHA-256 of the reading; the content is stored sealed
      (no plaintext in the store record, no content on any
      public serialization); server-stamped timestamps (a
      claimant-asserted timestamp is ignored);
* C2  unseal rules: sealed before the reveal date; unseal on
      claimant publication (content presented whose hash
      matches); unseal at the claimant-chosen reveal date and
      at the default 24-month date; extension once only — a
      second extension is refused AND recorded; every
      transition is a dated, append-only history event, with
      an injectable clock throughout;
* C3  integrity: hash verification discriminates (a one-byte
      difference does not verify); a mismatched unseal
      presentation is refused and recorded; the sealed
      envelope fails closed on tampering; there is no
      edit/delete path; corrections are new entries that
      supersede; the credit display is invariant under a
      later program assessment of the reading;
* C2/C4 trail view: one serialized trail per claim assembling
      stage + stage history with a source pointer on every
      stage entry, verdicts and transitions alike carrying
      evidence refs with origin groups, falsifier state at
      decision time, actor, and timestamp; bundle + gate
      records when the claim is a bundle; anchor annotation
      (validation_status / strict_set) for anchors;
      evidence instances counted by origin group; priority
      entries filed against the claim ride the trail without
      leaking sealed content.

All fixtures are synthetic and obviously so: invented
claimant names marked SYNTHETIC, example.org references, and
synthetic readings. No real priority claim is filed by these
tests (Phase C hard limit) — the API tests run against a
temporary runtime store, never the live one.
"""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timedelta, timezone

import pytest

from glossa_lab import claim_trail as trail_mod
from glossa_lab.claim_trail import build_claim_trail
from glossa_lab.priority_register import (
    CANONICALIZATION,
    FORBIDDEN_ENTRY_FIELDS,
    PriorityRegister,
    PriorityRegisterError,
    add_months,
    canonical_content_bytes,
    content_hash,
    load_register,
    open_sealed,
    public_record,
    save_register,
    seal_content,
    serialize_entry,
    verify_content,
)

UTC = timezone.utc
T0 = datetime(2026, 10, 12, 12, 0, 0, tzinfo=UTC)

# Obviously-synthetic fixtures.
CLAIMANT = "SYNTHETIC Claimant (test fixture)"
CONTACT = "synthetic-claimant@example.org"
READING = "SYNTHETIC READING (test fixture): sign M000 reads as 'fixture-syllable'."
EVIDENCE = [
    "https://example.org/spec029/synthetic-priority-evidence-1",
    "synthetic fixture corpus notes, entry 1",
]
SEALED_MARKER = "fixture-syllable"
TEST_KEY = b"spec029-phase-c-test-seal-key-not-a-real-key"


def make_register(clock_time=T0):
    return PriorityRegister(seal_key=TEST_KEY, clock=lambda: clock_time)


def filed(register=None, **overrides):
    register = register or make_register()
    kwargs = dict(
        claimant=CLAIMANT, claimant_contact=CONTACT,
        reading=READING, evidence=EVIDENCE,
    )
    kwargs.update(overrides)
    entry = register.register(**kwargs)
    return register, entry


# ── C1: canonicalization + hash ──────────────────────────────────────────────

def test_canonicalization_is_defined_and_byte_exact():
    assert CANONICALIZATION == "spec029-priority-canonical-v1"
    blob = canonical_content_bytes(READING, EVIDENCE)
    payload = json.loads(blob.decode("utf-8"))
    assert payload == {"reading": READING, "evidence": EVIDENCE}
    assert content_hash(READING, EVIDENCE) == hashlib.sha256(blob).hexdigest()
    # Recomputing the same content hashes identically.
    assert content_hash(READING, list(EVIDENCE)) == content_hash(READING, EVIDENCE)


def test_hash_discriminates_one_byte_difference():
    base = content_hash(READING, EVIDENCE)
    assert content_hash(READING[:-1] + "!", EVIDENCE) != base  # one byte in reading
    assert content_hash(READING, [EVIDENCE[0][:-1] + "!", EVIDENCE[1]]) != base  # one byte in evidence
    assert content_hash(READING + " ", EVIDENCE) != base  # whitespace is content, not normalised away
    register, entry = filed()
    assert verify_content(entry, READING, EVIDENCE) is True
    assert verify_content(entry, READING[:-1] + "!", EVIDENCE) is False


# ── C1: intake ───────────────────────────────────────────────────────────────

def test_intake_public_record_is_exactly_claimant_timestamp_hash():
    _, entry = filed()
    record = public_record(entry)
    assert set(record) == {"claimant", "timestamp", "content_hash"}
    assert record["claimant"] == CLAIMANT
    assert record["timestamp"] == entry["registered_at"]
    assert record["content_hash"] == content_hash(READING, EVIDENCE)
    assert len(record["content_hash"]) == 64


def test_intake_no_score_stage_or_verdict_field_exists():
    _, entry = filed()
    serialized = serialize_entry(entry)
    for blob in (entry, serialized, public_record(entry)):
        for field in FORBIDDEN_ENTRY_FIELDS:
            assert field not in blob, field
    assert "score" not in json.dumps(serialized)
    assert "verdict" not in json.dumps(serialized)


def test_intake_timestamp_is_server_stamped_not_claimant_asserted():
    register = make_register()
    entry = register.register(
        claimant=CLAIMANT, claimant_contact=CONTACT, reading=READING,
        evidence=EVIDENCE, registered_at="1999-01-01T00:00:00+00:00",
        timestamp="1999-01-01T00:00:00+00:00",
    )
    assert entry["registered_at"] == T0.isoformat()


def test_intake_incomplete_record_is_refused_and_files_nothing():
    register = make_register()
    for kwargs in (
        dict(claimant="", claimant_contact=CONTACT, reading=READING, evidence=EVIDENCE),
        dict(claimant=CLAIMANT, claimant_contact="", reading=READING, evidence=EVIDENCE),
        dict(claimant=CLAIMANT, claimant_contact=CONTACT, reading="", evidence=EVIDENCE),
        dict(claimant=CLAIMANT, claimant_contact=CONTACT, reading=READING, evidence=[]),
    ):
        with pytest.raises(PriorityRegisterError):
            register.register(**kwargs)
    assert register.entries == []


def test_content_is_stored_sealed_not_plaintext():
    _, entry = filed()
    blob = json.dumps(entry)
    assert READING not in blob
    assert SEALED_MARKER not in blob
    assert CONTACT not in json.dumps(serialize_entry(entry))
    assert CONTACT not in json.dumps(public_record(entry))
    # The sealed envelope opens back to exactly the canonical content.
    opened = open_sealed(entry["sealed_content"], TEST_KEY)
    assert opened == canonical_content_bytes(READING, EVIDENCE)


def test_sealed_envelope_tamper_fails_closed():
    envelope = seal_content(b"synthetic sealed bytes", TEST_KEY)
    tampered = dict(envelope, ciphertext=envelope["ciphertext"][:-2] + "AA")
    with pytest.raises(PriorityRegisterError):
        open_sealed(tampered, TEST_KEY)
    with pytest.raises(PriorityRegisterError):
        open_sealed(envelope, b"a-different-key")


# ── C1/C2: seal holds before the date; the public surface leaks nothing ──────

def test_public_surface_leaks_no_sealed_content():
    register, entry = filed()
    surfaces = [
        json.dumps(public_record(entry)),
        json.dumps(serialize_entry(entry)),
        json.dumps(register.public_records()),
        json.dumps([serialize_entry(e) for e in register.entries]),
    ]
    for surface in surfaces:
        assert READING not in surface
        assert SEALED_MARKER not in surface
        assert CONTACT not in surface
    assert serialize_entry(entry)["content"] is None
    assert serialize_entry(entry)["sealed"] is True


def test_default_reveal_is_24_months_from_intake():
    _, entry = filed()
    assert entry["reveal_date"] == add_months(T0, 24).isoformat()
    assert entry["extended"] is False


def test_add_months_calendar_arithmetic():
    assert add_months(datetime(2026, 1, 31, tzinfo=UTC), 24) == datetime(2028, 1, 31, tzinfo=UTC)
    assert add_months(datetime(2026, 10, 12, tzinfo=UTC), 24) == datetime(2028, 10, 12, tzinfo=UTC)
    assert add_months(datetime(2025, 1, 31, tzinfo=UTC), 1) == datetime(2025, 2, 28, tzinfo=UTC)


def test_seal_holds_before_reveal_date():
    register, entry = filed()
    unsealed = register.unseal_due(now=T0 + timedelta(days=364 * 2 - 1))
    assert unsealed == []
    assert entry["status"] == "sealed"
    assert serialize_entry(entry)["content"] is None


# ── C2: unseal triggers ──────────────────────────────────────────────────────

def test_unseal_at_chosen_reveal_date():
    register, entry = filed(reveal_date="2027-01-01")
    assert entry["reveal_date"].startswith("2027-01-01")
    assert register.unseal_due(now=datetime(2026, 12, 31, tzinfo=UTC)) == []
    unsealed = register.unseal_due(now=datetime(2027, 1, 1, tzinfo=UTC))
    assert [e["entry_id"] for e in unsealed] == [entry["entry_id"]]
    assert entry["status"] == "unsealed"
    assert entry["unseal_trigger"] == "reveal_date"
    shown = serialize_entry(entry)
    assert shown["sealed"] is False
    assert shown["content"] == {"reading": READING, "evidence": EVIDENCE}
    last = entry["history"][-1]
    assert last["event"] == "unsealed" and last["trigger"] == "reveal_date"
    assert last["timestamp"] == datetime(2027, 1, 1, tzinfo=UTC).isoformat()
    # Idempotent: a second sweep changes nothing.
    assert register.unseal_due(now=datetime(2027, 1, 2, tzinfo=UTC)) == []


def test_unseal_at_default_24_month_date():
    register, entry = filed()
    unsealed = register.unseal_due(now=add_months(T0, 24))
    assert [e["entry_id"] for e in unsealed] == [entry["entry_id"]]


def test_unseal_by_claimant_publication_matching_content():
    register, entry = filed()
    out = register.unseal_by_publication(
        entry["entry_id"], reading=READING, evidence=EVIDENCE, now=T0 + timedelta(days=3),
    )
    assert out["status"] == "unsealed"
    assert out["unseal_trigger"] == "claimant_publication"
    assert serialize_entry(out)["content"]["reading"] == READING
    last = out["history"][-1]
    assert last["event"] == "unsealed" and last["trigger"] == "claimant_publication"
    assert last["presented_content_hash"] == content_hash(READING, EVIDENCE)


def test_unseal_by_publication_hash_mismatch_refused_and_recorded():
    register, entry = filed()
    before = len(entry["history"])
    with pytest.raises(PriorityRegisterError):
        register.unseal_by_publication(
            entry["entry_id"], reading=READING[:-1] + "!", evidence=EVIDENCE,
            now=T0 + timedelta(days=1),
        )
    assert entry["status"] == "sealed"
    assert serialize_entry(entry)["content"] is None
    assert len(entry["history"]) == before + 1
    refusal = entry["history"][-1]
    assert refusal["event"] == "unseal_refused"
    assert refusal["timestamp"] == (T0 + timedelta(days=1)).isoformat()


# ── C2: extension, once only ─────────────────────────────────────────────────

def test_extension_once_succeeds_as_dated_record():
    register, entry = filed()
    new_date = add_months(T0, 36)
    register.extend_reveal_date(entry["entry_id"], new_date, now=T0 + timedelta(days=10))
    assert entry["extended"] is True
    assert entry["reveal_date"] == new_date.isoformat()
    event = entry["history"][-1]
    assert event["event"] == "reveal_extended"
    assert event["previous_reveal_date"] == add_months(T0, 24).isoformat()
    assert event["new_reveal_date"] == new_date.isoformat()
    assert event["timestamp"] == (T0 + timedelta(days=10)).isoformat()
    # The extended date governs: sealed the day before, unsealed on it.
    assert register.unseal_due(now=new_date - timedelta(days=1)) == []
    assert register.unseal_due(now=new_date)


def test_second_extension_refused_and_recorded():
    register, entry = filed()
    register.extend_reveal_date(entry["entry_id"], add_months(T0, 36), now=T0)
    before = len(entry["history"])
    with pytest.raises(PriorityRegisterError):
        register.extend_reveal_date(entry["entry_id"], add_months(T0, 48), now=T0 + timedelta(days=1))
    assert entry["reveal_date"] == add_months(T0, 36).isoformat()
    assert len(entry["history"]) == before + 1
    refusal = entry["history"][-1]
    assert refusal["event"] == "extension_refused"
    assert "already been extended once" in refusal["reason"]


def test_extension_that_does_not_move_reveal_later_is_refused_and_recorded():
    register, entry = filed()
    with pytest.raises(PriorityRegisterError):
        register.extend_reveal_date(entry["entry_id"], add_months(T0, 12), now=T0)
    assert entry["extended"] is False
    assert entry["history"][-1]["event"] == "extension_refused"


def test_extension_after_unseal_is_refused_and_recorded():
    register, entry = filed()
    register.unseal_by_publication(entry["entry_id"], reading=READING, evidence=EVIDENCE, now=T0)
    with pytest.raises(PriorityRegisterError):
        register.extend_reveal_date(entry["entry_id"], add_months(T0, 48), now=T0)
    assert entry["history"][-1]["event"] == "extension_refused"


# ── C3: append-only, corrections, credit invariant ───────────────────────────

def test_no_edit_or_delete_path_exists():
    register, _ = filed()
    for name in ("delete", "remove", "edit", "update_entry", "delete_entry", "edit_entry"):
        assert not hasattr(register, name), name
    import glossa_lab.api.indus_evidence as api

    routes = {(r.path, tuple(sorted(r.methods or ()))) for r in api.router.routes}
    delete_routes = [p for p, methods in routes if "DELETE" in methods and "priority" in p]
    put_routes = [p for p, methods in routes if "PUT" in methods and "priority" in p]
    assert delete_routes == [] and put_routes == []


def test_correction_is_a_new_entry_superseding_the_old():
    register, old = filed()
    old_public = public_record(old)
    _, new = filed(
        register=register, reading=READING + " Corrected synthetic sentence.",
        supersedes=old["entry_id"],
    )
    assert new["supersedes"] == old["entry_id"]
    assert old["superseded_by"] == new["entry_id"]
    assert old["history"][-1]["event"] == "superseded"
    # The superseded entry's own content, hash, and credit are untouched.
    assert public_record(old) == old_public
    assert old["content_hash"] == content_hash(READING, EVIDENCE)
    assert len(register.entries) == 2


def test_credit_display_invariant_under_later_assessment():
    register, entry = filed()
    before = public_record(entry)
    # Simulate every later event the program can record: an
    # assessment living on a *separate* claim record, an
    # extension, a refused unseal, and the eventual unseal.
    assessed_claim = {"claim_id": "synthetic-claim", "claim_status": "contradicted",
                      "aee_score": {"propagated_score": 0.01, "band": "low"}}
    register.extend_reveal_date(entry["entry_id"], add_months(T0, 30), now=T0)
    with pytest.raises(PriorityRegisterError):
        register.unseal_by_publication(entry["entry_id"], reading="wrong", evidence=EVIDENCE, now=T0)
    register.unseal_by_publication(entry["entry_id"], reading=READING, evidence=EVIDENCE, now=T0)
    assert assessed_claim["claim_status"] == "contradicted"  # assessment happened elsewhere
    assert public_record(entry) == before


def test_every_transition_is_a_dated_history_event():
    register, entry = filed()
    register.extend_reveal_date(entry["entry_id"], add_months(T0, 30), now=T0)
    register.unseal_due(now=add_months(T0, 30))
    events = [h["event"] for h in entry["history"]]
    assert events == ["registered", "reveal_extended", "unsealed"]
    for event in entry["history"]:
        assert event["timestamp"]  # every event is dated


def test_store_roundtrip_persists_sealed_only(tmp_path):
    register, entry = filed()
    store = tmp_path / "priority_register.json"
    key = tmp_path / "priority_register.key"
    key.write_bytes(TEST_KEY)
    save_register(register, store)
    blob = store.read_text("utf-8")
    # Sealed content is never plaintext, even at rest in the store.
    # (The contact does live in this internal store file — it is
    # correspondence data per plan §5/§V — but in no serialization.)
    assert READING not in blob and SEALED_MARKER not in blob
    loaded = load_register(store, key, clock=lambda: T0)
    assert public_record(loaded.entries[0]) == public_record(entry)
    unsealed = loaded.unseal_due(now=add_months(T0, 24))
    assert unsealed and unsealed[0]["revealed_content"]["reading"] == READING


# ── Trail view: synthetic claim with a full record ───────────────────────────

def full_claim():
    return {
        "claim_id": "synthetic_claim_0001",
        "source_document_id": "synthetic_source_doc",
        "normalized_claim": "SYNTHETIC claim (test fixture).",
        "claim_status": "supported",
        "extracted_at": "2026-10-09T00:00:00+00:00",
        "falsification_condition": "If the synthetic fixture fails, this claim falls.",
        "glossa_lab_evidence": ["synthetic phase-test result"],
        "contradicting_evidence": [],
        "stage": "checked",
        "stage_source": "specs/029-tao-claim-lifecycle/reclassification-ledger.json:synthetic_claim_0001",
        "stage_as_of": "2026-10-12",
        "stage_history": [{
            "from_stage": None, "to_stage": "created",
            "actor": "spec029-phase-d-restaging-migration", "timestamp": "2026-10-12",
            "evidence_refs": ["specs/029-tao-claim-lifecycle/reclassification-ledger.json:synthetic_claim_0001"],
            "reason": "synthetic migration entry",
        }, {
            "from_stage": "created", "to_stage": "checked",
            "actor": "SYNTHETIC Checker (test fixture)", "timestamp": "2026-10-12",
            "evidence_refs": ["https://example.org/spec029/synthetic-check"],
            "reason": "synthetic check",
        }],
        "evidence_instances": [{
            "claim_id": "synthetic_claim_0001_dup",
            "source_document_id": "synthetic_source_doc",
            "record": {"claim_id": "synthetic_claim_0001_dup",
                       "source_document_id": "synthetic_source_doc",
                       "stage": "created", "stage_source": "ledger:dup",
                       "stage_as_of": "2026-10-12", "stage_history": []},
        }, {
            "claim_id": "synthetic_claim_0001_other",
            "source_document_id": "synthetic_other_doc",
            "record": {"claim_id": "synthetic_claim_0001_other",
                       "source_document_id": "synthetic_other_doc",
                       "stage": "created", "stage_source": "ledger:other",
                       "stage_as_of": "2026-10-12", "stage_history": []},
        }],
    }


def test_trail_assembles_stage_history_with_source_pointers():
    view = build_claim_trail(full_claim())
    assert view["claim_id"] == "synthetic_claim_0001"
    assert view["stage"]["stage"] == "checked"
    assert len(view["stage_transitions"]) == 2
    for event in view["stage_transitions"]:
        assert event["source_pointer"] == full_claim()["stage_source"]
        assert event["actor"] and event["timestamp"]
        assert event["falsifier_state_at_decision"] == "stated"
        assert event["evidence_refs"] and all("origin_group" in r for r in event["evidence_refs"])
    ledger_ref = view["stage_transitions"][0]["evidence_refs"][0]
    assert ledger_ref["origin_group"] == "spec029-reclassification-ledger"


def test_trail_verdict_carries_fr029_12_fields():
    view = build_claim_trail(full_claim())
    assert len(view["verdicts"]) == 1
    verdict = view["verdicts"][0]
    assert verdict["verdict"] == "supported"
    assert verdict["timestamp"] == "2026-10-09T00:00:00+00:00"
    assert verdict["falsifier_state_at_decision"] == "stated"
    assert verdict["evidence_refs"]
    assert all("origin_group" in r for r in verdict["evidence_refs"])
    # The extraction-era actor gap is stated, never invented.
    assert verdict["actor_recorded"] is False
    assert view["completeness"]["missing"] == ["actor"]


def test_trail_origin_groups_count_instances_once_per_group():
    view = build_claim_trail(full_claim())
    # Two instances, but one shares the canonical claim's origin
    # group: distinct groups are {canonical doc, other doc,
    # glossa evidence} + the ledger-free set below.
    assert view["evidence_instances"][0]["origin_group"] == "synthetic_source_doc"
    groups = view["origin_groups"]
    assert "synthetic_source_doc" in groups and "synthetic_other_doc" in groups
    assert view["origin_group_count"] == len(set(groups))
    assert view["falsifier"]["state"] == "stated"


def test_trail_missing_falsifier_is_visible_never_invented():
    claim = full_claim()
    del claim["falsification_condition"]
    view = build_claim_trail(claim)
    assert view["falsifier"]["state"] == "absent"
    assert view["falsifier"]["falsification_condition"] is None
    assert "falsifier_state" in view["completeness"]["missing"]


def test_trail_bundle_and_gate_records():
    from glossa_lab.claim_bundle import make_attribution_subclaim, make_bundle, make_subclaim

    subs = []
    for kind in ("reading_soundness", "scholarship_accounting", "explanation_intelligibility"):
        subs.append(make_subclaim(
            kind, f"synthetic-{kind}", proposition=f"SYNTHETIC {kind} proposition.",
            evidence=["https://example.org/spec029/synthetic-evidence"],
            falsification_condition="Synthetic falsifier.", stage="checked",
            stage_source="test", timestamp=T0.isoformat(),
        ))
    subs.append(make_attribution_subclaim(
        "synthetic-attribution", proposition="SYNTHETIC attribution proposition.",
        evidence=[], falsification_condition="Synthetic falsifier.", stage="checked",
        stage_source="test", timestamp=T0.isoformat(),
    ))
    parent = make_bundle(
        {"claim_id": "synthetic_bundle_0001", "claim_status": "supported"}, subs,
        timestamp=T0.isoformat(),
    )
    parent["explanation_record"] = {"author": "SYNTHETIC Explainer (test fixture)"}
    view = build_claim_trail(parent)
    assert view["bundle"] is not None
    assert len(view["bundle"]["sub_claims"]) == 4
    assert view["bundle"]["stage_computation"]["minimum_stage"] == "checked"
    assert view["gate_records"]["explanation_record"]["author"].startswith("SYNTHETIC")
    assert view["falsifier"]["sub_claims"]["attribution"]["state"] == "stated"


def test_trail_anchor_annotation():
    anchor = {
        "claim_id": "M000", "reading": "synthetic", "confidence": "HIGH",
        "basis": "Synthetic basis.", "stage": "checked",
        "stage_source": "specs/029-tao-claim-lifecycle/reclassification-ledger.json:ANCHOR-M000",
        "stage_as_of": "2026-10-12",
        "stage_history": [{
            "from_stage": None, "to_stage": "checked", "actor": "migration",
            "timestamp": "2026-10-12",
            "evidence_refs": ["specs/029-tao-claim-lifecycle/reclassification-ledger.json:ANCHOR-M000"],
            "reason": "synthetic",
        }],
        "validation_status": "strict_sa_independent", "strict_set": True,
        "verified_unexplained": True,
    }
    rule = {"rule_id": "strict_sa_independent_hm", "rule_version": "synthetic"}
    view = build_claim_trail(anchor, record_kind="anchor", strict_set_rule=rule)
    assert view["record_kind"] == "anchor"
    assert view["anchor_annotation"]["validation_status"] == "strict_sa_independent"
    assert view["anchor_annotation"]["strict_set"] is True
    assert view["anchor_annotation"]["strict_set_rule"] == rule


def test_trail_priority_entries_ride_without_leaking_sealed_content():
    register, entry = filed(claim_id="synthetic_claim_0001")
    view = build_claim_trail(full_claim(), priority_entries=register.entries)
    assert len(view["priority_entries"]) == 1
    shown = view["priority_entries"][0]
    assert shown["public_record"] == public_record(entry)
    assert shown["content"] is None
    blob = json.dumps(view)
    assert SEALED_MARKER not in blob and CONTACT not in blob
    # After unseal the trail shows the revealed content.
    register.unseal_by_publication(entry["entry_id"], reading=READING, evidence=EVIDENCE, now=T0)
    view2 = build_claim_trail(full_claim(), priority_entries=register.entries)
    assert view2["priority_entries"][0]["content"]["reading"] == READING


def test_trail_module_does_not_mutate_the_record():
    claim = full_claim()
    snapshot = copy.deepcopy(claim)
    build_claim_trail(claim)
    assert claim == snapshot
    assert trail_mod.ANCHORS_SOURCE.endswith("INDUS_FINAL_ANCHORS.json")


# ── API surface (temporary runtime store; never the live one) ────────────────

@pytest.fixture()
def api_store(tmp_path, monkeypatch):
    import glossa_lab.api.indus_evidence as api

    monkeypatch.setattr(api, "_PRIORITY_STORE", tmp_path / "priority_register.json")
    monkeypatch.setattr(api, "_PRIORITY_KEY", tmp_path / "priority_register.key")
    (tmp_path / "priority_register.key").write_bytes(TEST_KEY)
    return tmp_path


def test_api_intake_public_and_unseal_flow(client, api_store):
    r = client.post("/api/v1/indus-evidence/priority-register", json={
        "claimant": CLAIMANT, "claimant_contact": CONTACT,
        "reading": READING, "evidence": EVIDENCE, "claim_id": "synthetic_claim_api",
    })
    assert r.status_code == 200, r.text
    body = r.json()
    entry_id = body["entry_id"]
    assert set(body["public_record"]) == {"claimant", "timestamp", "content_hash"}
    assert SEALED_MARKER not in r.text and CONTACT not in r.text

    listing = client.get("/api/v1/indus-evidence/priority-register")
    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    assert SEALED_MARKER not in listing.text

    # A one-byte-different presentation is refused; the refusal is recorded.
    bad = client.post(f"/api/v1/indus-evidence/priority-register/{entry_id}/unseal", json={
        "reading": READING[:-1] + "!", "evidence": EVIDENCE,
    })
    assert bad.status_code == 400
    got = client.get(f"/api/v1/indus-evidence/priority-register/{entry_id}")
    events = [h["event"] for h in got.json()["entry"]["history"]]
    assert "unseal_refused" in events
    assert got.json()["entry"]["content"] is None

    ok = client.post(f"/api/v1/indus-evidence/priority-register/{entry_id}/unseal", json={
        "reading": READING, "evidence": EVIDENCE,
    })
    assert ok.status_code == 200, ok.text
    assert ok.json()["entry"]["content"]["reading"] == READING


def test_api_extension_once_only(client, api_store):
    r = client.post("/api/v1/indus-evidence/priority-register", json={
        "claimant": CLAIMANT, "claimant_contact": CONTACT,
        "reading": READING, "evidence": EVIDENCE,
    })
    entry_id = r.json()["entry_id"]
    first = client.post(f"/api/v1/indus-evidence/priority-register/{entry_id}/extend",
                        json={"new_reveal_date": "2030-01-01"})
    assert first.status_code == 200, first.text
    second = client.post(f"/api/v1/indus-evidence/priority-register/{entry_id}/extend",
                         json={"new_reveal_date": "2031-01-01"})
    assert second.status_code == 400
    got = client.get(f"/api/v1/indus-evidence/priority-register/{entry_id}")
    events = [h["event"] for h in got.json()["entry"]["history"]]
    assert events.count("reveal_extended") == 1 and "extension_refused" in events


def test_api_trail_for_live_claim_and_anchor(client, api_store):
    claims = client.get("/api/v1/indus-evidence/claims?limit=1")
    assert claims.status_code == 200
    claim_id = claims.json()["claims"][0]["claim_id"]
    r = client.get(f"/api/v1/indus-evidence/claims/{claim_id}/trail")
    assert r.status_code == 200, r.text
    view = r.json()
    assert view["claim_id"] == claim_id
    assert view["stage"]["stage"] in ("created", "checked")
    assert view["stage_transitions"], "Phase D stamped a stage history on live claims"
    assert view["stage_transitions"][0]["source_pointer"]
    anchor = client.get("/api/v1/indus-evidence/claims/M342/trail")
    assert anchor.status_code == 200, anchor.text
    aview = anchor.json()
    assert aview["record_kind"] == "anchor"
    assert aview["anchor_annotation"]["validation_status"] == "strict_sa_independent"
    assert aview["anchor_annotation"]["strict_set"] is True
    missing = client.get("/api/v1/indus-evidence/claims/no-such-claim-zzz/trail")
    assert missing.status_code == 404
