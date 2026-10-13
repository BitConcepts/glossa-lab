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
_POST_MERGE_SCORES = json.loads(
    (_FIXTURES / "spec029_post_merge_aee_scores.json").read_text("utf-8"))
_POST_CORRECTION_SCORES = json.loads(
    (_FIXTURES / "spec029_post_phase104_correction_aee_scores.json").read_text("utf-8"))

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
        want_keys = _BASE_KEYS | {"contradicting_evidence", "status_correction"}
        if claim_id.endswith(("critique_0001", "critique_0002")):
            want_keys |= {"evidence_instances"}
        assert set(rec) == want_keys, claim_id
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


def test_canonical_claim_unchanged():
    rec = _load_store()[CANONICAL]
    assert rec["claim_status"] == "contradicted"
    assert rec["stage"] == "checked"
    assert len(rec["stage_history"]) == 1
    assert rec["stage_source"].endswith(f":{CANONICAL}")
    assert "status_correction" not in rec
    assert rec["contradicting_evidence"] == [
        "Rao et al. 2009: conditional entropy falls in linguistic range",
        "Phase-43: 20 TERMINAL_STRONG signs consistent with morphological suffixes",
        "Phase-43: [M77/267][M77/99] = fixed title formula at inscription start",
    ]


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
        assert before["propagated_score"] == 0.289375, cid
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
