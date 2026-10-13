"""Spec 029 Phase I — D-B proposition deduplication (tasks I1–I5).

Pins:

* the frozen proposition fingerprint (normalisation rules in
  ``glossa_lab.proposition_fingerprint``): case / whitespace /
  punctuation variants of one proposition collide; materially
  different propositions do not;
* the merged live store: all 31 records of the 2026-10-09 batch
  still present (merge, never delete), exactly 5 duplicate
  groups, every instance carrying ``merged_into`` and preserved
  verbatim on its canonical record, Phase D stage stamps
  untouched everywhere, falsifiers preserved where either
  instance carried one and never invented;
* origin-group counting in the AEE wiring (I3): the scored set
  is the 23 canonical claims; a merged proposition's evidence is
  counted once; every surviving claim's score is byte-identical
  to the Phase A pre-change fixture, and the mean movement
  (0.484903 → 0.497641) is composition only;
* the intake fingerprint gate (I4): a planted duplicate is
  refused loudly, naming both records; a distinct proposition
  is accepted; a regeneration recreating known claim ids is
  not a collision; regeneration preserves the merge state.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from glossa_lab.aee_core import assessment_summary, load_claims_from_dir
from glossa_lab.proposition_fingerprint import (
    DuplicatePropositionError,
    claim_fingerprint,
    normalize_proposition_text,
    proposition_fingerprint,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC_DIR = _REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_FIXTURES = Path(__file__).resolve().parent / "fixtures"
_PRE_CHANGE = _FIXTURES / "spec029_pre_change_aee_scores.json"
_POST_MERGE = _FIXTURES / "spec029_post_merge_aee_scores.json"
_LEDGER = json.loads((_SPEC_DIR / "reclassification-ledger.json").read_text("utf-8"))

ZIPF_2009 = "yadav_2009_arxiv_manual_001"
ZIPF_2010 = "yadav_2010_ngrams_manual_001"
BEGIN_2009 = "yadav_2009_arxiv_manual_002"
BEGIN_2010 = "yadav_2010_ngrams_manual_002"

EXPECTED_GROUPS = {
    ZIPF_2009: {ZIPF_2010},
    BEGIN_2009: {BEGIN_2010},
    "ancient_writing_and_modern_technologies_51831ac9_statisti_0004": {
        "fuls2023_catalog_of_indussigns_searchins_1dbdecdb_statisti_0001",
        "positional_analysis_of_indus_signs_a2bedc93_statisti_0001",
        "the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003",
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002",
    },
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001": {
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003",
    },
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002": {
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004",
    },
}
ALL_INSTANCES = set().union(*EXPECTED_GROUPS.values())


def _load_store() -> dict[str, dict]:
    records = {}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            records[claim["claim_id"]] = claim
    return records


def _load_merge_tool():
    spec = importlib.util.spec_from_file_location(
        "merge_phase_i_dedupe", _SPEC_DIR / "merge_phase_i_dedupe.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_indus_claims():
    spec = importlib.util.spec_from_file_location(
        "indus_claims", _REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── I1: fingerprint definition ───────────────────────────────────────────

def test_normalization_rules():
    assert normalize_proposition_text("  Zipf-Mandelbrot   LAW. ") == \
        normalize_proposition_text("zipf mandelbrot law")
    # Newlines (extraction snippets carry them mid-phrase) and
    # whitespace runs normalise identically.
    assert normalize_proposition_text("myth of a\nliterate Harappan") == \
        normalize_proposition_text("Myth of a  Literate   Harappan")
    assert normalize_proposition_text("Collapse of the Indus-Script Thesis") == \
        normalize_proposition_text("collapse of the indus script thesis")


def test_fingerprint_is_text_only_and_discriminating():
    zipf = "Indus script sign frequencies follow a Zipf-Mandelbrot distribution."
    assert proposition_fingerprint(zipf) == proposition_fingerprint(zipf.upper())
    # A materially different proposition does not collide.
    assert proposition_fingerprint(zipf) != proposition_fingerprint(
        "Sign value: 700 / a volumetric system with a unit of 40")
    assert proposition_fingerprint(
        "Sign value: 700 / a volumetric system with a unit of 40") != \
        proposition_fingerprint("Sign value: 700 / a unit of 4")


# ── I1/I2: the merged live store ─────────────────────────────────────────

def test_store_holds_all_31_records_nothing_deleted():
    records = _load_store()
    assert len(records) == 31
    ledger_ids = {e["item_id"] for e in _LEDGER["entries"]
                  if e["class"] == "extracted_claim"}
    assert set(records) == ledger_ids


def test_every_record_carries_its_correct_fingerprint():
    for claim_id, record in _load_store().items():
        assert record["proposition_fingerprint"] == claim_fingerprint(record), claim_id


def test_duplicate_groups_are_exactly_the_five_expected():
    records = _load_store()
    actual = {}
    for canonical, instances in EXPECTED_GROUPS.items():
        assert records[canonical].get("merged_into") is None
        embedded = records[canonical].get("evidence_instances") or []
        assert {e["claim_id"] for e in embedded} == instances, canonical
        actual[canonical] = instances
    pointed = {cid for cid, r in records.items() if r.get("merged_into")}
    assert pointed == ALL_INSTANCES
    for cid in ALL_INSTANCES:
        canonical = records[cid]["merged_into"]
        assert cid in EXPECTED_GROUPS[canonical]
        assert records[cid]["proposition_fingerprint"] == \
            records[canonical]["proposition_fingerprint"]


def test_instances_preserved_verbatim_on_canonical():
    records = _load_store()
    for canonical, instances in EXPECTED_GROUPS.items():
        embedded = {e["claim_id"]: e for e in records[canonical]["evidence_instances"]}
        for cid in instances:
            entry = embedded[cid]
            # The embedded copy is the record as merged; the
            # store's one volatile field, ``extracted_at``, is
            # refreshed on the live record by later extraction
            # regenerations (pre-existing behaviour) and is the
            # only field excluded from the comparison.
            kept = {k: v for k, v in entry["record"].items() if k != "extracted_at"}
            live = {k: v for k, v in records[cid].items() if k != "extracted_at"}
            assert kept == live
            assert entry["source_document_id"] == records[cid]["source_document_id"]


def test_phase_d_stage_stamps_untouched_by_merge():
    records = _load_store()
    entries = {e["item_id"]: e for e in _LEDGER["entries"]
               if e["class"] == "extracted_claim"}
    for claim_id, record in records.items():
        entry = entries[claim_id]
        assert record["stage"] == entry["honest_stage"], claim_id
        assert record["stage_source"].endswith(f":{claim_id}"), claim_id
        assert record["stage_as_of"] == "2026-10-12"
        assert len(record["stage_history"]) == 1
        assert record["verified_unexplained"] is (
            "verified_unexplained" in (entry.get("flags") or []))


def test_falsifiers_preserved_and_never_invented():
    records = _load_store()
    # Zipf: both instances carried the same falsifier; the
    # canonical keeps it.
    assert records[ZIPF_2009]["falsification_condition"] == \
        "If frequency distribution deviates from Zipf-Mandelbrot law."
    # Text-begin/end: NEITHER instance carried a falsifier, so the
    # canonical honestly carries none (audit finding; not repaired
    # by inventing one).
    assert "falsification_condition" not in records[BEGIN_2009]
    assert "falsification_condition" not in records[BEGIN_2010]


def test_merge_tool_verify_and_idempotency():
    tool = _load_merge_tool()
    files = tool.load_store()
    plan = tool.plan_merges(files)
    assert {p["canonical_claim_id"] for p in plan} == set(EXPECTED_GROUPS)
    assert tool.store_state(files, plan) == "merged"
    assert tool.verify_store(files, plan)["ok"]


# ── I3: origin-group counting + score movement ───────────────────────────

def test_scored_set_is_the_23_canonical_claims():
    claims = load_claims_from_dir(_CLAIMS_DIR)
    assert len(claims) == 23
    ids = {c.id for c in claims}
    assert not (ids & ALL_INSTANCES)
    assert set(EXPECTED_GROUPS) <= ids


def test_merged_proposition_evidence_counted_once():
    claims = {c.id: c for c in load_claims_from_dir(_CLAIMS_DIR)}
    zipf = claims[ZIPF_2009]
    # Source assertion (Yadav 2009) + Glossa's Phase-43 test — the
    # identical Phase-43 evidence the 2010 instance carried is NOT
    # counted a second time, although the instance is preserved on
    # the record and named in metadata.
    assert len(zipf.evidence) == 2
    assert sum(1 for e in zipf.evidence if e.source_id == "glossa-lab") == 1
    assert zipf.metadata["evidence_instance_claim_ids"] == [ZIPF_2010]


def test_every_surviving_score_identical_to_pre_change_fixture():
    pre = json.loads(_PRE_CHANGE.read_text("utf-8"))
    post = json.loads(_POST_MERGE.read_text("utf-8"))
    assert set(post) == set(pre) - ALL_INSTANCES
    for claim_id, want in post.items():
        assert want == pre[claim_id], claim_id
    summary = assessment_summary(_CLAIMS_DIR)
    assert summary["total_claims"] == 23
    # Spec 029 Phase E1 (E1.3): the summary-position mean was
    # withdrawn (FR-029-08). The composition-only mean movement
    # this test formerly pinned (0.497641) is superseded by the
    # withdrawal; the per-claim fixture identity above stands.
    assert "mean_propagated_score" not in summary


# ── I4: intake fingerprint gate ──────────────────────────────────────────

def _plant_store(tmp_path: Path) -> Path:
    store = tmp_path / "extracted"
    store.mkdir(parents=True, exist_ok=True)
    (store / "existing_doc.json").write_text(json.dumps({
        "document_id": "existing_doc",
        "claims": [{
            "claim_id": "existing_doc_manual_001",
            "source_document_id": "existing_doc",
            "claim_type": "statistical_claim",
            "normalized_claim":
                "Indus script sign frequencies follow a Zipf-Mandelbrot distribution.",
            "claim_status": "strongly_supported",
            "testability": "directly_testable",
        }],
    }), "utf-8")
    return store


def test_gate_rejects_planted_duplicate_naming_both_records(tmp_path):
    mod = _load_indus_claims()
    store = _plant_store(tmp_path)
    incoming = [{
        "claim_id": "new_doc_manual_001",
        "source_document_id": "new_doc",
        "normalized_claim":
            "Indus script sign frequencies follow a Zipf Mandelbrot distribution!",
    }]
    with pytest.raises(DuplicatePropositionError) as excinfo:
        mod.assert_no_duplicate_propositions(incoming, store)
    message = str(excinfo.value)
    assert "new_doc_manual_001" in message
    assert "existing_doc_manual_001" in message


def test_gate_accepts_distinct_proposition(tmp_path):
    mod = _load_indus_claims()
    store = _plant_store(tmp_path)
    incoming = [{
        "claim_id": "new_doc_manual_009",
        "source_document_id": "new_doc",
        "normalized_claim": "Celestial signs function as suffix markers.",
    }]
    mod.assert_no_duplicate_propositions(incoming, store)  # no raise


def test_gate_allows_known_group_members_regeneration(tmp_path):
    mod = _load_indus_claims()
    store = _plant_store(tmp_path)
    # Wholesale regeneration recreates the same claim id for the
    # same proposition: a member, not a collision.
    incoming = [{
        "claim_id": "existing_doc_manual_001",
        "source_document_id": "existing_doc",
        "normalized_claim":
            "Indus script sign frequencies follow a Zipf-Mandelbrot distribution.",
    }]
    mod.assert_no_duplicate_propositions(incoming, store)  # no raise


def test_process_document_stops_on_planted_duplicate(tmp_path):
    mod = _load_indus_claims()
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "yadav_2009_arxiv.json").write_text(json.dumps({"title": "Y"}), "utf-8")
    _plant_store(tmp_path)  # writes tmp_path/extracted/existing_doc.json
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    with pytest.raises(DuplicatePropositionError):
        mod.process_document("yadav_2009_arxiv")
    # Intake stopped: nothing was written for the duplicate doc.
    assert not (out_dir / "yadav_2009_arxiv.json").exists()


def test_process_document_accepts_distinct_proposition(tmp_path):
    mod = _load_indus_claims()
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "farmer_sproat_witzel_2004.json").write_text(
        json.dumps({"title": "F"}), "utf-8")
    _plant_store(tmp_path)
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document("farmer_sproat_witzel_2004")
    assert result["status"] == "extracted"
    assert (out_dir / "farmer_sproat_witzel_2004.json").exists()


def test_regeneration_preserves_merge_state(tmp_path):
    mod = _load_indus_claims()
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "demo_doc.json").write_text(json.dumps({"title": "Demo"}), "utf-8")
    (processed / "demo_doc.txt").write_text(
        "The Indus script encodes Proto-Dravidian language.", "utf-8")
    prior_claim = {
        "claim_id": "demo_doc_language_0001",
        "proposition_fingerprint": "f" * 64,
        "merged_into": "some_canonical_001",
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
    assert claim["merged_into"] == "some_canonical_001"
    assert claim["proposition_fingerprint"] == "f" * 64


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
