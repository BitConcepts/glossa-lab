"""Spec 029 — Phase-104 carry-over correction (2026-10-13).

The Phase-104 evaluation of untested extracted claims
(``glossa-indus/reports/phase104_claims_evaluation.json``) returned
``status_changed`` -> ``contradicted`` under RULE-DUP for five
records, each "restating the proposition already adjudicated as
farmer_sproat_witzel_2004_manual_001 … Verdict carries over." The
carry-over was never written into the live records: the three
canonical claims among the five still read ``untested`` at stage
``created``. The correction (owner's order, 2026-10-13; record:
``specs/029-tao-claim-lifecycle/phase104-carryover-correction-record.md``;
tool: ``correct_phase104_carryover.py`` in the same directory)
wrote the verdict and its evidence into the three canonical
records and moved their stage to ``checked`` through the single
stage writer, preserving the previous status in an additive
``status_correction`` field and the Phase D stamp as
``stage_history[0]``.

These tests pin the corrected state, its basis, and its exact
blast radius:

* the Phase-104 record supports the carry-over for all three;
* each corrected record carries Phase-104's evidence verbatim,
  the dated correction note, and a recompute-clean stage;
* the canonical claim is unchanged;
* the only AEE score movement in the whole scored set is the
  three corrected claims', each the engine's contradiction
  penalty applying to evidence the record now honestly carries;
* the named residual stands deliberately: the two Phase-104
  records Phase I merged as evidence instances
  (``..._critique_0003`` / ``..._critique_0004``) keep their
  preserved pre-correction stamps — they are sightings of the
  two corrected canonicals, not separate live claims, and this
  correction did not rewrite preserved instance records.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

from glossa_lab import spec029_gates as gates
from glossa_lab.aee_core import assessment_summary

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC_DIR = _REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_PHASE104 = json.loads(
    (_REPO_ROOT / "glossa-indus" / "reports" / "phase104_claims_evaluation.json")
    .read_text("utf-8"))
_FIXTURES = Path(__file__).resolve().parent / "fixtures"
# aee 1.5.0 adoption supersession (2026-10-20): both score
# fixtures were regenerated under the adopted engine (the
# post-merge one from the pre-correction store bytes, the
# post-correction one from the live store), so the movement
# comparison below stays within one engine's semantics; the
# pre-1.5 fixtures are preserved untouched.
_POST_MERGE_SCORES = json.loads(
    (_FIXTURES / "spec029_post_merge_aee150_scores.json").read_text("utf-8"))
_POST_CORRECTION_SCORES = json.loads(
    (_FIXTURES / "spec029_post_phase104_correction_aee150_scores.json").read_text("utf-8"))

CANONICAL = "farmer_sproat_witzel_2004_manual_001"
CORRECTED = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
}
#: Proposition fingerprints of the corrected records, as extracted —
#: the correction changes no identity field.
FINGERPRINTS = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001":
        "defa7480501b2b457f4c0316d28d0801e91496b385ba99f5d62b90ae7bc74630",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002":
        "d7e4efd6b7748029e58d6480d5d227e7556e648007cc0e6cd43d2f5ad96b33e6",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001":
        "16fa1b2e8d294dcbd855ffe6ab4bbabc4fb24b2b3f3d4cb1ecd3b9bdb7d285f6",
}
_BASE_KEYS = {
    "claim_id", "source_document_id", "claim_type", "normalized_claim",
    "quote_fragment", "claim_status", "testability", "confidence_in_source",
    "extracted_at", "stage", "stage_source", "stage_as_of", "stage_history",
    "verified_unexplained", "proposition_fingerprint",
}


def _load_store() -> dict[str, dict]:
    records = {}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            records[claim["claim_id"]] = claim
    return records


def _phase104_entry(claim_id: str) -> dict:
    return next(r for r in _PHASE104["results"] if r["claim_id"] == claim_id)


# ── The basis: Phase-104 says what the correction says it says ───────────

def test_phase104_record_supports_the_carryover_for_all_three():
    assert _PHASE104["rules"]["RULE-DUP"] == (
        "verdict carried over from an already-adjudicated identical proposition")
    for claim_id in CORRECTED:
        entry = _phase104_entry(claim_id)
        assert entry["verdict"] == "status_changed", claim_id
        assert entry["new_status"] == "contradicted", claim_id
        assert entry["rule"] == "RULE-DUP", claim_id
        assert CANONICAL in entry["reason"], claim_id
        assert "Verdict carries over" in entry["reason"], claim_id
        assert len(entry["evidence"]) == 4, claim_id


# ── The corrected records ────────────────────────────────────────────────

def test_corrected_records_carry_the_phase104_outcome():
    records = _load_store()
    for claim_id in CORRECTED:
        rec = records[claim_id]
        entry = _phase104_entry(claim_id)
        # The verdict Phase-104 prescribed, with its evidence verbatim.
        assert rec["claim_status"] == "contradicted", claim_id
        assert rec["contradicting_evidence"] == entry["evidence"], claim_id
        # Nothing else about the proposition changed; no falsifier
        # was invented (Phase-104 carried over none, and the
        # fragments' falsifier gap stays visible on their trails).
        assert rec["proposition_fingerprint"] == FINGERPRINTS[claim_id]
        assert "falsification_condition" not in rec, claim_id
        # The correction's two fields on top of the base keys —
        # plus the two authored lane-2 fields (``not_understood`` /
        # ``explanation_record``) the lane-2 adoption ingestion
        # (PR #197, merged from main after this correction was
        # written) placed on every adopted record, these three
        # included. The correction neither wrote nor removed them;
        # their coexistence with the correction is pinned by
        # test_carryover_and_lane2_fields_coexist below.
        want_keys = _BASE_KEYS | {"contradicting_evidence", "status_correction",
                                  "not_understood", "explanation_record"}
        if claim_id.endswith(("critique_0001", "critique_0002")):
            want_keys |= {"evidence_instances"}
        # Amendment (Spec 052 execution, 2026-10-24): the frozen
        # Spec 052 section 4.2 appends a dated outcome entry to
        # each of these three records — as the 2026-10-22 Spec 025
        # audit appended one to the parent record. Dated appends
        # (keys carrying a trailing _YYYY_MM_DD date) are
        # append-only records under the program's discipline, not
        # changes to the proposition or to this correction, so
        # the exact-shape pin covers every non-append key and any
        # extra key must be a dated append. The generator's
        # dated-append carry-over (indus_claims.py) preserves
        # them across regeneration under the same rule.
        extra = set(rec) - want_keys
        assert all(
            re.search(r"_\d{4}_\d{2}_\d{2}$", k) for k in extra
        ), claim_id
        assert set(rec) - extra == want_keys, claim_id
        # The previous status is preserved on the record itself.
        corr = rec["status_correction"]
        assert corr["kind"] == "phase104-carryover-correction"
        assert corr["date"] == "2026-10-13"
        assert corr["previous_claim_status"] == "untested"
        assert corr["new_claim_status"] == "contradicted"
        assert corr["rule"] == "RULE-DUP"
        assert corr["basis"] == (
            f"glossa-indus/reports/phase104_claims_evaluation.json:{claim_id}")
        # Stage: the Phase D entry stands; the correction appended
        # the transition-service tail the stored stage derives from.
        (h0, h1) = rec["stage_history"]
        assert h0["actor"] == "spec029-phase-d-restaging-migration"
        assert h0["to_stage"] == "created" and h0["timestamp"] == "2026-10-12"
        assert h1["from_stage"] == "created" and h1["to_stage"] == "checked"
        assert h1["actor"] == "spec029-phase104-carryover-migration"
        assert h1["evidence_refs"][0] == corr["basis"]
        assert "Phase-104 carry-over correction" in h1["reason"]
        assert rec["stage"] == "checked"
        assert rec["stage_source"] == "transition-service:stage_history[1]"
        assert rec["stage_as_of"] == h1["timestamp"]
        assert rec["verified_unexplained"] is False


def test_corrected_records_pass_the_phase_g_gates():
    records = _load_store()
    ctx = gates.load_context(_REPO_ROOT)
    for claim_id in CORRECTED:
        rec = records[claim_id]
        assert gates.audit_stage_cache(rec, ctx) == [], claim_id
        assert gates.audit_trail_record(rec, ctx, record_kind="claim") == [], claim_id
        # The gap profile did not grow: still exactly the recorded
        # baseline family for these records (no verdict actor was
        # invented; no falsifier was invented).
        profile = gates.trail_gap_profile(rec, record_kind="claim")
        assert profile <= {"actor", "falsifier_state"}, claim_id


def test_canonical_claim_unchanged_by_the_correction():
    rec = _load_store()[CANONICAL]
    assert rec["claim_status"] == "contradicted"
    assert "status_correction" not in rec
    assert rec["contradicting_evidence"] == [
        "Rao et al. 2009: conditional entropy falls in linguistic range",
        "Phase-43: 20 TERMINAL_STRONG signs consistent with morphological suffixes",
        "Phase-43: [M77/267][M77/99] = fixed title formula at inscription start",
    ]
    # The correction appended nothing to the canonical claim. Its
    # one post-Phase-D movement is the lane-2 adoption's
    # checked -> explained transition (PR #197, a separate owner
    # act merged from main after this correction was written;
    # the advanced shape is pinned by the Phase D tests). Here we
    # pin that no correction entry exists anywhere in its history.
    assert all(h["actor"] != "spec029-phase104-carryover-migration"
               for h in rec["stage_history"])
    assert rec["stage"] == "explained"
    assert len(rec["stage_history"]) == 2


def test_carryover_and_lane2_fields_coexist_on_the_corrected_records():
    # The reconciliation requirement of the merge with main: each
    # corrected record carries BOTH the Phase-104 carry-over
    # correction (this act) AND the authored lane-2 fields (the
    # adoption ingestion, PR #197) — neither act's fields dropped.
    records = _load_store()
    for claim_id in CORRECTED:
        rec = records[claim_id]
        assert rec["status_correction"]["kind"] == (
            "phase104-carryover-correction"), claim_id
        assert rec["claim_status"] == "contradicted", claim_id
        assert rec["stage"] == "checked", claim_id
        assert isinstance(rec["not_understood"], str), claim_id
        assert rec["not_understood"].strip(), claim_id
        explanation = rec["explanation_record"]
        assert explanation["author"] == "Tristen Pierson", claim_id
        assert explanation["author_kind"] == "human", claim_id


# ── Blast radius: scores move only where the record changed ─────────────

def test_score_movement_is_exactly_the_three_corrected_claims():
    summary = assessment_summary(_CLAIMS_DIR)
    assert summary["total_claims"] == len(_POST_MERGE_SCORES) == 23
    moved = set()
    for entry in summary["claims"]:
        cid = entry["claim_id"]
        assert entry["aee_score"] == _POST_CORRECTION_SCORES[cid], cid
        if entry["aee_score"] != _POST_MERGE_SCORES[cid]:
            moved.add(cid)
    assert moved == CORRECTED
    for cid in CORRECTED:
        before, after = _POST_MERGE_SCORES[cid], _POST_CORRECTION_SCORES[cid]
        # The movement is the contradiction penalty, and only that:
        # the record now carries the contradicting evidence, exactly
        # as the canonical claim's record always did.
        assert before["band"] == "low" and after["band"] == "unknown", cid
        assert before["propagated_score"] == 0.139375, cid
        assert after["propagated_score"] == 0.0, cid
        assert after["components"]["contradiction_penalty"] == 0.75, cid
        assert "Contradiction penalty 0.750" in after["notes"], cid


# ── The named residual: preserved instances were not rewritten ──────────

def test_merged_instance_records_keep_their_preserved_stamps():
    records = _load_store()
    pairs = {
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003":
            "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004":
            "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    }
    for instance_id, canonical_id in pairs.items():
        rec = records[instance_id]
        # Phase I's disposition stands: merged into the canonical
        # (now-corrected) claim; the preserved record itself was
        # not rewritten by this correction.
        assert rec["merged_into"] == canonical_id
        assert rec["claim_status"] == "untested"
        assert rec["stage"] == "created"
        assert len(rec["stage_history"]) == 1
        assert "status_correction" not in rec
        # The embedded copy on the canonical is the same record
        # (Phase I's invariant; ``extracted_at`` excluded, as there).
        embedded = next(
            i["record"] for i in records[canonical_id]["evidence_instances"]
            if i["claim_id"] == instance_id)
        kept = {k: v for k, v in embedded.items() if k != "extracted_at"}
        live = {k: v for k, v in rec.items() if k != "extracted_at"}
        assert kept == live


# ── The correction tool: verify mode passes, re-apply fails closed ──────

def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "correct_phase104_carryover", _SPEC_DIR / "correct_phase104_carryover.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_correction_tool_verifies_and_refuses_to_reapply():
    tool = _load_tool()
    assert tool.main(["correct_phase104_carryover.py", "--verify"]) == 0
    with pytest.raises(tool.CorrectionError):
        tool.main(["correct_phase104_carryover.py", "--apply"])


# ── Regeneration must not un-correct a record ───────────────────────────
#
# The extracted-claims store is regenerated wholesale by
# indus_claims.py (a suite test exercising the refresh path does
# exactly this — the first CI run of this correction failed when a
# regeneration reset the three records to the extraction default).
# The Phase D / Phase I carry-overs already preserve stage fields
# and merge state by claim identity; the correction added the same
# never-drop rule for a status_correction's outcome fields. This
# test pins it on a synthetic store, in the Phase D pattern.

def _regenerate_with_prior(tmp_path: Path, prior_claim: dict | None) -> dict:
    spec = importlib.util.spec_from_file_location(
        "indus_claims", _REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tmp_path.mkdir(parents=True, exist_ok=True)
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "demo_doc.json").write_text(json.dumps({"title": "Demo"}), "utf-8")
    (processed / "demo_doc.txt").write_text(
        "The Indus script encodes Proto-Dravidian language.", "utf-8")
    if prior_claim is not None:
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
    return claim


def test_regeneration_preserves_a_status_correction(tmp_path):
    correction = {
        "kind": "phase104-carryover-correction",
        "date": "2026-10-13",
        "previous_claim_status": "untested",
        "new_claim_status": "contradicted",
        "basis": "glossa-indus/reports/phase104_claims_evaluation.json:demo",
        "rule": "RULE-DUP",
        "note": "Synthetic correction for the regeneration control.",
    }
    prior = {
        "claim_id": "demo_doc_language_0001",
        "claim_status": "contradicted",
        "contradicting_evidence": ["Synthetic contradicting evidence"],
        "status_correction": correction,
    }
    claim = _regenerate_with_prior(tmp_path / "corrected", prior)
    assert claim["claim_status"] == "contradicted"
    assert claim["contradicting_evidence"] == ["Synthetic contradicting evidence"]
    assert claim["status_correction"] == correction


def test_regeneration_without_a_correction_keeps_extraction_status(tmp_path):
    # Control: with no status_correction on the prior record, the
    # extraction-assigned status stands — the carry-over is keyed
    # on the correction field, never on the claim's identity.
    claim = _regenerate_with_prior(tmp_path / "plain", None)
    assert claim["claim_status"] == "untested"
    assert "status_correction" not in claim
