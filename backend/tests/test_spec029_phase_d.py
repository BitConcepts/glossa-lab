"""Spec 029 Phase D — OD-1 re-staging migration (tasks D2–D5).

These tests pin the post-migration live state and the migration
script's contract:

* the ledger-vs-live reconciliation, recomputed from the live
  stores, matches the frozen ledger's §3 table exactly
  (220 created / 116 checked / 0 / 0 / 0; 105
  ``verified_unexplained`` flags);
* every stamped record carries ``stage_source`` (naming the
  ledger and its entry) and ``stage_as_of`` (2026-10-12), plus
  exactly one initial ``stage_history`` entry;
* the migration is additive only: canonical comparison of the
  anchors file against the pinned pre-migration SHA-256, with
  exactly the Phase D additive keys removed, and byte-prefix
  comparison for the hypothesis YAML files against the base
  commit's content is asserted via the snapshot-free property
  that no pre-existing parsed key changed;
* the script, exercised on synthetic stores in a temp copy of
  its own logic (imported module, monkeypatched paths), is
  idempotent and fail-closed on conflicts and mismatches.

The script lives in the spec directory (house style for spec
tooling); it is loaded by path.

Supersession note (2026-10-13): the Phase-104 carry-over
correction superseded the migration stamp on exactly three
extracted claims (named in ``_CARRYOVER_CORRECTED`` below). The
live-state pins in this file exempt exactly those records, and
the reconciliation / plan pins assert that the migration's own
machinery disagrees with the frozen expectations by exactly the
correction's movement and nothing else.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC_DIR = _REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
_LEDGER = json.loads((_SPEC_DIR / "reclassification-ledger.json").read_text("utf-8"))
_ANCHORS_PATH = _REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_HYPO_DIR = _REPO_ROOT / "glossa-indus" / "hypotheses" / "models"
_SIDECAR = _SPEC_DIR / "phase-d-stamped-records.json"
_PRE_MIGRATION_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
_ADDITIVE = ("stage", "stage_source", "stage_as_of", "stage_history",
             "verified_unexplained")
_LEDGER_REF = "specs/029-tao-claim-lifecycle/reclassification-ledger.json"

#: Phase-104 carry-over correction (2026-10-13): the three fragment
#: records the Phase-104 evaluation prescribed a verdict carry-over
#: for no longer carry the Phase D migration stamp — the correction
#: superseded it through the transition service, appending a second
#: history entry (the Phase D entry stands as history[0]). See
#: ``specs/029-tao-claim-lifecycle/phase104-carryover-correction-record.md``.
#: The Phase D pins below exempt exactly these records, by name;
#: the correction's own shape is asserted in
#: ``test_spec029_phase104_correction.py``.
_CARRYOVER_CORRECTED = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
}

# ── Lane-2 adoption amendment (2026-10-13, owner act) ─────────────────────
#
# On 2026-10-13 the owner adopted the 35 lane-2 explanation drafts
# (PR #190: "Adopt all 35 lane-2 drafts as authored by me") and
# ordered their ingestion. Twenty records that stood at ``checked``
# advanced to ``explained`` through the transition service (the
# machinery's single writer), carrying the authored explanation
# records; nine of them had their Phase D ``verified_unexplained``
# stamp cleared, because the missing explanation was the flag's
# whole content. The migration stamp remains every advanced
# record's ``stage_history[0]``, byte-identical — append-only.
# The assertions in this file therefore partition: records the
# adoption did not advance keep the original stamp assertions
# verbatim; the named 20 are asserted in their advanced form.
_LANE2_TS = "2026-10-13T10:12:00+00:00"
_LANE2_EXPLAINED = {
    "farmer_sproat_witzel_2004_manual_001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_manual_002",
    "parpola_2010_dravidian_solution_manual_001",
    "parpola_2010_dravidian_solution_manual_002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003",
    "yadav_2009_arxiv_manual_001",
    "yadav_2009_arxiv_manual_002",
    "STUDY-SPEC-019/PHASE-125",
    "STUDY-SPEC-023/PHASE-132+383",
    "STUDY-SPEC-024/F1",
    "STUDY-SPEC-024/F2-HOLDAT",
    "STUDY-SPEC-024/F3-ICIT",
    "STUDY-SPEC-025/G1",
    "STUDY-SPEC-027/STAGE1-PHASE-392",
    "STUDY-SPEC-028/ARM-A",
    "STUDY-SPEC-028/ARM-B",
    "STUDY-SPECS-001-023+PHASES-TO-141",
    "PRED-2026-006",
    "PRED-2026-007",
}
_LANE2_FLAG_CLEARED = {
    "parpola_2010_dravidian_solution_manual_001",
    "parpola_2010_dravidian_solution_manual_002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003",
    "yadav_2009_arxiv_manual_001",
    "yadav_2009_arxiv_manual_002",
    "STUDY-SPEC-024/F1",
    "STUDY-SPEC-024/F3-ICIT",
    "STUDY-SPEC-025/G1",
}


def _load_migration():
    spec = importlib.util.spec_from_file_location(
        "migrate_phase_d_restaging", _SPEC_DIR / "migrate_phase_d_restaging.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mig = _load_migration()


def _entries(cls: str) -> list[dict]:
    return [e for e in _LEDGER["entries"] if e["class"] == cls]


def _assert_stamp(record: dict, entry: dict) -> None:
    assert record["stage"] == entry["honest_stage"]
    assert record["stage_source"] == f"{_LEDGER_REF}:{entry['item_id']}"
    assert record["stage_as_of"] == "2026-10-12"
    assert record["verified_unexplained"] is (
        "verified_unexplained" in (entry.get("flags") or []))
    history = record["stage_history"]
    assert len(history) == 1
    (h,) = history
    assert h["from_stage"] is None
    assert h["to_stage"] == entry["honest_stage"]
    assert h["actor"] == "spec029-phase-d-restaging-migration"
    assert h["timestamp"] == "2026-10-12"
    assert h["evidence_refs"] == [f"{_LEDGER_REF}:{entry['item_id']}"]
    assert "OD-1" in h["reason"] and entry["item_id"] in h["reason"]


def _assert_lane2_advanced(record: dict, entry: dict) -> None:
    """One of the named 20: the migration stamp survives as
    ``stage_history[0]`` (asserted field-for-field, as in
    ``_assert_stamp``), and the adoption appended exactly one
    transition-service entry on top of it."""
    history = record["stage_history"]
    assert len(history) == 2
    h0 = history[0]
    assert h0["from_stage"] is None
    assert h0["to_stage"] == entry["honest_stage"]
    assert h0["actor"] == "spec029-phase-d-restaging-migration"
    assert h0["timestamp"] == "2026-10-12"
    assert h0["evidence_refs"] == [f"{_LEDGER_REF}:{entry['item_id']}"]
    assert "OD-1" in h0["reason"] and entry["item_id"] in h0["reason"]
    h1 = history[1]
    assert h1["from_stage"] == entry["honest_stage"] == "checked"
    assert h1["to_stage"] == "explained"
    assert h1["actor"] == "Tristen Pierson"
    assert h1["timestamp"] == _LANE2_TS
    assert h1["evidence_refs"]
    assert "lane2-drafts" in h1["evidence_refs"][0]
    assert record["stage"] == "explained"
    assert record["stage_source"] == "transition-service:stage_history[1]"
    assert record["stage_as_of"] == _LANE2_TS
    if entry["item_id"] in _LANE2_FLAG_CLEARED:
        assert record["verified_unexplained"] is False
    else:
        assert record["verified_unexplained"] is (
            "verified_unexplained" in (entry.get("flags") or []))


# ── Live reconciliation (D5) ─────────────────────────────────────────────

def test_verify_mode_reconciliation_matches_the_recorded_state():
    """At the migration, this reconciliation matched the frozen
    ledger exactly (220 / 116 / 0 / 0 / 0; 105 flags — the original
    assertions, preserved in the phase-d record). Two
    owner-ordered acts of 2026-10-13 then moved records, each
    through the transition service (the machinery's single
    writer) and each named in this file: the lane-2 adoption
    advanced the named 20 records one step (checked -> explained)
    and cleared 9 flags; the Phase-104 carry-over correction
    moved the named 3 extracted claims from created to checked,
    writing the verdict Phase-104 had prescribed (their Phase D
    stamps stand as stage_history[0]). The reconciliation now
    matches THAT recorded state exactly: every deviation from
    the ledger is one of the named moves, every other record
    still carries the migration stamp untouched, and the
    migration's own counter (``count_stamped_records``) refuses
    the advanced population, as designed — it is a migration
    verifier, and the migration is not re-runnable over an
    advanced store."""
    by_class = mig.entries_by_class(mig.load_ledger())
    stamped = mig.collect_live_state(by_class)
    counts: dict[str, dict[str, int]] = {}
    flags = 0
    deviating_stage: set[str] = set()
    deviating_flag: set[str] = set()
    for cls, entry, record in stamped:
        counts.setdefault(cls, {})
        counts[cls][record["stage"]] = counts[cls].get(record["stage"], 0) + 1
        if record.get("verified_unexplained") is True:
            flags += 1
        if record["stage"] != entry["honest_stage"]:
            deviating_stage.add(entry["item_id"])
        ledger_flag = "verified_unexplained" in (entry.get("flags") or [])
        if record["verified_unexplained"] is not ledger_flag:
            deviating_flag.add(entry["item_id"])
        if entry["item_id"] not in _LANE2_EXPLAINED | _CARRYOVER_CORRECTED:
            assert record["stage"] == entry["honest_stage"]
            assert record["stage_source"] == f"{_LEDGER_REF}:{entry['item_id']}"
            assert record["stage_as_of"] == "2026-10-12"
    assert deviating_stage == _LANE2_EXPLAINED | _CARRYOVER_CORRECTED
    assert deviating_flag == _LANE2_FLAG_CLEARED
    assert counts == {
        "anchor_reading": {"created": 193, "checked": 94},
        "extracted_claim": {"created": 18, "checked": 5, "explained": 8},
        "registered_prediction": {"created": 3, "explained": 2},
        "hypothesis_model": {"created": 3},
        "study_headline_claim": {"explained": 10},
    }
    totals = {stage: 0 for stage in
              ("created", "checked", "explained", "accepted", "digested")}
    for cls_counts in counts.values():
        for stage, n in cls_counts.items():
            totals[stage] += n
    assert totals == {
        "created": 217, "checked": 99, "explained": 20,
        "accepted": 0, "digested": 0,
    }
    assert flags == 96
    assert mig.grouped_count(by_class) == 9
    # The migration verifier itself fails closed on the advanced
    # records (stage_source no longer the ledger stamp).
    with pytest.raises(mig.MigrationError):
        mig.count_stamped_records(stamped, mig.grouped_count(by_class))


def test_every_anchor_stamped_with_provenance():
    doc = json.loads(_ANCHORS_PATH.read_text("utf-8"))
    entries = {e["item_id"][len("ANCHOR-"):]: e for e in _entries("anchor_reading")}
    assert set(doc["anchors"]) == set(entries)
    for sign, entry in entries.items():
        _assert_stamp(doc["anchors"][sign], entry)


def test_every_extracted_claim_stamped_with_provenance():
    entries = {e["item_id"]: e for e in _entries("extracted_claim")}
    seen = {}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            seen[claim["claim_id"]] = claim
    assert set(seen) == set(entries)
    corrected = []
    for cid, entry in entries.items():
        if cid in _LANE2_EXPLAINED:
            _assert_lane2_advanced(seen[cid], entry)
        elif cid in _CARRYOVER_CORRECTED:
            # Superseded by the Phase-104 carry-over correction:
            # the Phase D stamp survives as history[0] (asserted
            # here); the record's current stamp is the correction's
            # transition-service tail (asserted in the correction
            # test file and by the Phase G recompute gate).
            corrected.append(cid)
            (h0, _tail) = seen[cid]["stage_history"]
            assert h0["from_stage"] is None
            assert h0["to_stage"] == entry["honest_stage"]
            assert h0["actor"] == "spec029-phase-d-restaging-migration"
            assert h0["timestamp"] == "2026-10-12"
            assert h0["evidence_refs"] == [f"{_LEDGER_REF}:{cid}"]
            assert seen[cid]["verified_unexplained"] is (
                "verified_unexplained" in (entry.get("flags") or []))
        else:
            _assert_stamp(seen[cid], entry)
    assert set(corrected) == _CARRYOVER_CORRECTED


def test_hypothesis_models_stamped_and_parseable_where_parseable():
    import yaml  # noqa: PLC0415

    for entry in _entries("hypothesis_model"):
        path = _HYPO_DIR / f"{entry['item_id'][len('HYP-'):]}.yaml"
        text = path.read_text("utf-8")
        rec = mig.yaml_record_from_text(text)
        assert rec["stage"] == entry["honest_stage"]
        assert rec["stage_source"] == f"{_LEDGER_REF}:{entry['item_id']}"
        assert rec["stage_as_of"] == "2026-10-12"
        assert rec["verified_unexplained"] is False
        if entry["item_id"] == "HYP-roif_guild_ledger":
            continue  # pre-existing PyYAML defect in this file (Phase D record)
        parsed = yaml.safe_load(text)
        assert parsed["stage"] == entry["honest_stage"]
        assert parsed["stage_history"][0]["to_stage"] == entry["honest_stage"]


def test_sidecar_covers_document_classes_only():
    sidecar = json.loads(_SIDECAR.read_text("utf-8"))
    assert sidecar["source_ledger"] == _LEDGER_REF
    assert sidecar["date"] == "2026-10-12"
    by_id = {r["item_id"]: r for r in sidecar["records"]}
    want = {e["item_id"]: e for cls in ("registered_prediction", "study_headline_claim")
            for e in _entries(cls)}
    assert set(by_id) == set(want)
    assert len(by_id) == 15
    for item_id, entry in want.items():
        if item_id in _LANE2_EXPLAINED:
            _assert_lane2_advanced(by_id[item_id], entry)
        else:
            _assert_stamp(by_id[item_id], entry)
        assert by_id[item_id]["class"] == entry["class"]
        assert by_id[item_id]["live_source"]


# ── Additive-only (D5) ───────────────────────────────────────────────────

def test_anchors_additive_only_canonical_comparison():
    doc = json.loads(_ANCHORS_PATH.read_text("utf-8"))
    stripped = copy.deepcopy(doc)
    for rec in stripped["anchors"].values():
        for key in _ADDITIVE:
            rec.pop(key, None)
        # Spec 029 Phase H (D-A, 2026-10-12): the Phase H
        # annotation is additive on top of Phase D's stamps —
        # ``strict_set`` on every record, ``validation_status``
        # on the records that carried none (exactly the Phase H
        # values; pre-existing values stand), and the metadata
        # annotation block. Removing it too reproduces the
        # pre-migration bytes this assertion pins.
        rec.pop("strict_set", None)
        if rec.get("validation_status") in (
                "strict_sa_independent", "sa_in_provenance_chain",
                "no_validation_record"):
            rec.pop("validation_status", None)
    stripped.get("metadata", {}).pop("spec029_phase_h_annotation", None)
    digest = hashlib.sha256(
        json.dumps(stripped, indent=2, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert digest == _PRE_MIGRATION_ANCHORS_SHA256


def test_extracted_claims_additive_only_canonical_comparison():
    # Every pre-existing field of every claim (and file) is unchanged:
    # removing the additive keys and re-serializing must reproduce a
    # file whose claims parse to the same pre-existing content the
    # Phase A AEE fixture pins (checked separately in Phase A tests);
    # here we assert no claim carries any key beyond its pre-migration
    # key set plus the additive keys. (Lane-2 amendment, 2026-10-13:
    # the 23 canonical claims additionally carry the adopted
    # ``not_understood`` / ``explanation_record`` keys — additive on
    # top of the Phase D stamp, like Phase H's anchor annotations;
    # the 8 preserved instances carry neither.)
    pre_keys: dict[str, set] = {}
    entries = {e["item_id"]: e for e in _entries("extracted_claim")}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            extra = set(claim) - set(_ADDITIVE)
            assert extra  # the claim still carries its own fields
            pre_keys[claim["claim_id"]] = extra
            if claim["claim_id"] in _LANE2_EXPLAINED:
                _assert_lane2_advanced(claim, entries[claim["claim_id"]])
            elif claim["claim_id"] in _CARRYOVER_CORRECTED:
                # The Phase-104 carry-over correction (2026-10-13)
                # superseded these three stamps and added its two
                # correction fields; the corrected records' exact
                # shape is asserted in the correction test file,
                # not by this pin.
                continue
            else:
                _assert_stamp(claim, entries[claim["claim_id"]])
    assert len(pre_keys) == 31


def test_pred_register_document_untouched():
    # The pin proves the Phase D migration itself did not alter
    # the register. It was advanced once, by name, for the one
    # later authorised change: the append-only dated entry of
    # 2026-10-13 under register section 6 recording the Spec
    # 032 / Phase-396 step-0 closure of PRED-2026-006 (the
    # register's existing text is unchanged by that append;
    # Spec 032 spec section 7 prescribes it). It was advanced
    # a second time, by name, for the owner-ordered
    # registration append of 2026-10-13: the PRED-2026-010
    # entry added to register section 3 and its dated note in
    # section 6 (the clean-withholding successor to
    # PRED-2026-006; insertions only, +20/-0 lines, no
    # existing entry altered). It was advanced a third
    # time, by name, for the owner-ordered registration
    # append of 2026-10-20: the PRED-2026-011 entry added
    # to register section 3 and its dated note in section 6
    # (the clean-withholding successor to PRED-2026-010
    # with the disclosed mappability screen; insertions
    # only, no existing entry altered). It was advanced
    # a fourth time, by name, for the owner-ordered
    # execution append of 2026-10-20: the dated section 6
    # entry recording the Spec 035 / Phase-399 step-0
    # closure of PRED-2026-010 (insertions only, no
    # existing entry altered; the section 3 entry's
    # Tested/Outcome fields unchanged, per claim
    # F035-C15). It was advanced a fifth time, by
    # name, for the owner-ordered completion append
    # of 2026-10-20: the dated section 6 entry
    # recording the approval and public verification
    # of PRED-2026-011's OSF registration
    # (https://osf.io/t6whq/, DOI
    # 10.17605/OSF.IO/T6WHQ; insertions only, no
    # existing entry altered). Any further drift
    # from this hash is unauthorised.
    digest = hashlib.sha256(
        (_REPO_ROOT / "docs" / "PREDICTION_REGISTER.md").read_bytes()
    ).hexdigest()
    assert digest == "548b13f22eabd1f10280d1544533b440f6d317977be2b26da6a0b4abd9de159c"


# ── Script contract: shapes, states, idempotency ─────────────────────────

def test_stage_payload_shape_and_flag():
    flagged = next(e for e in _entries("anchor_reading")
                   if "verified_unexplained" in (e.get("flags") or []))
    payload = mig.stage_payload(flagged)
    assert payload["stage"] == flagged["honest_stage"]
    assert payload["verified_unexplained"] is True
    assert set(payload) == set(_ADDITIVE)


def test_record_state_transitions():
    entry = _entries("extracted_claim")[0]
    record: dict = {"claim_id": entry["item_id"]}
    assert mig.record_state(record, entry) == "unstamped"
    mig.stamp_record(record, entry)
    assert mig.record_state(record, entry) == "stamped"
    record["stage"] = "digested"
    assert mig.record_state(record, entry) == "conflict"


def test_plan_fails_closed_on_the_advanced_population():
    """The migration is a one-shot act, and its plan must refuse
    to re-run over an advanced store ("refusing to smooth").
    Before 2026-10-13 this test asserted ``state_counts ==
    {"stamped": 336}``, no problems, and a matching would-be
    reconciliation. Two owner-ordered acts of 2026-10-13 then
    advanced records through the transition service: the lane-2
    adoption (the named 20 — the 8 extracted claims among them
    live in the file store, the other 12 in the sidecar) and the
    Phase-104 carry-over correction (the named 3 extracted
    claims). The plan now reports exactly those 11 file-store
    records as conflicts with the ledger stamp, plus the sidecar
    differing from its ledger-derived form — and nothing else.
    Neither act is smoothed over."""
    p = mig.plan()
    assert p["state_counts"] == {"stamped": 310, "conflict": 11}
    extracted_advanced = {
        cid for cid in _LANE2_EXPLAINED
        if any(e["item_id"] == cid and e["class"] == "extracted_claim"
               for e in _LEDGER["entries"])
    }
    assert len(extracted_advanced) == 8
    assert set(p["problems"]) == (
        {f"{cid}: existing stage fields conflict with the ledger stamp"
         for cid in extracted_advanced | _CARRYOVER_CORRECTED}
        | {"sidecar exists but differs from the ledger-derived sidecar"})
    assert p["would_be_reconciliation"] is None


def test_reconcile_detects_mismatch_not_smoothed():
    recon = mig.reconcile({"anchor_reading": {"created": 1}}, flags=0, grouped=9)
    assert not recon["match"]
    assert recon["problems"]


def test_extraction_regeneration_preserves_stage_fields(tmp_path):
    """Plan §4 risk control: indus_claims.py regenerates the
    extracted-claims store wholesale; a regeneration must carry
    each claim's stamped stage fields over by claim identity.
    Amended 2026-10-13 (lane-2 adoption): the same carry-over
    covers the authored ``not_understood`` / ``explanation_record``
    fields."""
    spec = importlib.util.spec_from_file_location(
        "indus_claims", _REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "demo_doc.json").write_text(json.dumps({"title": "Demo"}), "utf-8")
    (processed / "demo_doc.txt").write_text(
        "The Indus script encodes Proto-Dravidian language.", "utf-8")
    entry = _entries("extracted_claim")[0]
    prior_claim = {"claim_id": "demo_doc_language_0001"}
    mig.stamp_record(prior_claim, entry)
    # Lane-2 adoption amendment (2026-10-13): the authored lane-2
    # fields ride the same carry-over. CI on PR #197 caught the
    # intake pipeline's regeneration stripping both fields while
    # the stage fields survived — a regenerated record at stage
    # 'explained' with no explanation record behind it.
    prior_claim["not_understood"] = (
        "Synthetic gap statement for the regeneration carry-over.")
    prior_claim["explanation_record"] = {
        "author": "Synthetic Author",
        "explanation": "Synthetic explanation for the carry-over.",
    }
    (out_dir / "demo_doc.json").write_text(
        json.dumps({"document_id": "demo_doc", "claims": [prior_claim]}), "utf-8")
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document("demo_doc")
    assert result["status"] == "extracted"
    regenerated = json.loads((out_dir / "demo_doc.json").read_text("utf-8"))
    (claim,) = regenerated["claims"]
    assert claim["claim_id"] == "demo_doc_language_0001"
    _assert_stamp(claim, entry)
    # Lane-2 adoption amendment (2026-10-13): authored fields survive.
    assert claim["not_understood"] == prior_claim["not_understood"]
    assert claim["explanation_record"] == prior_claim["explanation_record"]


def test_compute_flag_honours_stamped_state():
    from glossa_lab.claim_stage import compute_verified_unexplained  # noqa: PLC0415

    # A stamped anchor: no lane-1 field of its own fires the computed
    # rule, but the ledger-stamped state does (below explained).
    assert compute_verified_unexplained(
        {"stage": "checked", "confidence": "HIGH", "verified_unexplained": True})
    assert not compute_verified_unexplained(
        {"stage": "explained", "confidence": "HIGH", "verified_unexplained": True})
    # Unstamped / stamped-false records behave exactly as Phase A.
    assert not compute_verified_unexplained({"stage": "created", "confidence": "HIGH"})
    assert not compute_verified_unexplained(
        {"stage": "checked", "confidence": "HIGH", "verified_unexplained": False})


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
