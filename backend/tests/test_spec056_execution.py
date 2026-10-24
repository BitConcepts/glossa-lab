"""Spec 056 execution tests (Phase-418).

The execution's terminal outcome is IDENTIFICATION
FAILED: step 0 passed in full, two independent
extraction passes recovered a specific argument
from the pinned passage (K-1, the 'city' reading
in Dholavira signboard contexts, passing R-1,
R-2, R-4 and R-5), the sign list was named from
the document itself, and the drawn sign could not
be identified by either route spec section 5 R-3
allows. These tests pin the delivered form: the
results record's gate and R-3 facts, the frozen
traps asserted as traps (a W821 match, or the
Yunmapped_0821 number collision used as an
identification, would fail here), and the
claim-record closure append in the section 7
form with the fragment's status and stage
unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO / "specs/056-sign821-recovery"
RESULTS = REPO / "reports/phase418_results.json"
EXTRACTION = SPEC_DIR / "extraction-record.md"
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json"
)
CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001")
PASSAGE_SHA256 = (
    "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604")


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def _claim_entry() -> dict:
    doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))

    def find(node):
        if isinstance(node, dict):
            if node.get("claim_id") == CLAIM_ID:
                return node
            for value in node.values():
                hit = find(value)
                if hit is not None:
                    return hit
        elif isinstance(node, list):
            for value in node:
                hit = find(value)
                if hit is not None:
                    return hit
        return None

    entry = find(doc)
    assert entry is not None
    return entry


def test_results_record_outcome_and_step0():
    r = _results()
    assert r["phase"] == "Phase-418"
    assert r["spec"] == "056"
    assert r["claim_id"] == CLAIM_ID
    assert r["outcome"] == "IDENTIFICATION FAILED"
    assert "the drawn sign could not be identified" in (
        r["headline_wording"])
    g1 = r["step0"]["gate_0_1"]
    for name, pin in g1.items():
        assert pin["match"] is True, name
    assert g1["claim_record_spec038_form"][
        "freeze_time_sha256_constant"] == (
        "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a")
    g2 = r["step0"]["gate_0_2"]
    assert g2["start_anchor_standalone_count"] == 1
    assert g2["end_anchor_standalone_count"] == 1
    assert g2["anchor_sentence_occurrences"] == 1
    g3 = r["step0"]["gate_0_3"]
    assert g3["match"] is True
    assert g3["observed_sha256"] == PASSAGE_SHA256
    assert g3["bytes"] == 5354
    assert r["step0"]["all_gates_passed"] is True
    assert r["anchors"]["byte_identical"] is True


def test_dry_run_recorded_and_outcome_free():
    r = _results()
    d = r["dry_run"]
    assert d["requirement"] == "DD-056-16"
    assert d["quote_verified_verbatim"] is True
    assert "no candidate and no outcome" in d["produces"].lower()


def test_step1_candidates_and_checklists():
    r = _results()
    cands = {c["id"]: c for c in r["step1"]["candidates"]}
    assert set(cands) == {"K-1", "K-2", "K-3", "K-4"}
    assert r["step1"]["all_quotes_verified_verbatim"] is True
    k1 = cands["K-1"]
    assert k1["decisive"] is True
    for cond in ("R-1", "R-2", "R-4", "R-5"):
        assert k1["checklist"][cond].startswith("PASS"), cond
    assert "signboard contexts" in k1["falsification_condition"]
    assert "not a nullification" in k1["falsification_condition"]
    assert cands["K-2"]["checklist"]["R-1"].startswith("FAIL")
    assert cands["K-3"]["checklist"]["R-1"].startswith("FAIL")
    assert cands["K-3"]["checklist"]["R-2"].startswith("FAIL")
    assert cands["K-4"]["checklist"]["R-2"].startswith("FAIL")


def test_step2_r3_record_and_traps():
    r = _results()
    r3 = r["step2"]["r3_record"]
    assert r3["list_named_from_document"] is True
    assert "Wells's own sign list" in r3["source_list_named"]
    assert r3["drawn_sign_identified"] is False
    reg = r3["registry_route"]
    assert reg["registry_rows"] == 803
    assert reg["rows_with_w821_token"] == []
    assert reg["descriptions_naming_a_city"] == 0
    trap = reg["yunmapped_0821_row"]
    assert trap["numbering_system"] == "yajnadevam_glyphid"
    assert trap["wells_ids"] == ""
    wit = r3["witness_route_evidence"]
    assert wit["wells_witness_grapheme_821_rows"] == []
    assert r3["list_entry_route"][
        "held_text_figure_region_contains_821"] is False


def test_extraction_record_carries_the_sheets():
    text = EXTRACTION.read_text(encoding="utf-8")
    for needle in (
        "Pass A — extraction sheet",
        "Pass B — extraction sheet",
        "Reconciliation",
        "Dry-run of the machinery",
        PASSAGE_SHA256,
        "IDENTIFICATION FAILED",
        "Yunmapped_0821",
        "Fence sentence (spec §8)",
        "record repair. It establishes, at most",
    ):
        assert needle in text, needle


def test_claim_record_closure_append_form():
    # The fragment's own facts on the live file stand
    # unedited (the Spec 038 form: this store is
    # regenerated by the backend suite, so facts —
    # never a live-file hash or a mid-suite append —
    # are asserted on it).
    entry = _claim_entry()
    assert entry["normalized_claim"] == (
        "Sign value: 821 / it is used in a variety of "
        "contexts (Figure 6")
    assert entry["claim_status"] == "untested"
    assert entry["stage"] == "created"
    # The section 7 closure append, in its prescribed
    # form as recorded in the run's machine record.
    # The append itself was verified at the act:
    # removing it reproduces the pre-act claim file
    # byte-identically (outcome.md, F056-C15).
    append = _results()["claim_closure_append"]
    assert append["key"] == "spec056_closure"
    assert append["spec"] == "056"
    assert append["phase"] == "Phase-418"
    assert append["date"] == "2026-10-21"
    assert append["outcome"] == "IDENTIFICATION FAILED"
    assert append["wording"] == _results()["headline_wording"]
    assert append["record"] == (
        "specs/056-sign821-recovery/outcome.md")
    assert append["extraction_record"] == (
        "specs/056-sign821-recovery/extraction-record.md")
    # No retirement was recorded and no restatement
    # arises: the recorded append is a closure.
    assert "disposition" not in append["kind"]
    outcome_text = (SPEC_DIR / "outcome.md").read_text(
        encoding="utf-8")
    assert "spec056_closure" in outcome_text
    assert "byte-identically" in outcome_text
