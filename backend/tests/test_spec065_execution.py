"""Spec 065 execution tests (Phase-427).

The execution's terminal outcome is headline class
B — S-5 RESOLVED, S-1 STILL BLOCKED: S-5 resolves
HEADING ABSENT FROM DOCUMENT on the acquired file
(exactly one occurrence in its text layer,
extraction line 340, PDF page 9, sentence-initial
inside a running paragraph of section 5.5, not in
heading form), and S-1 resolves STILL UNLOCATED —
ACQUISITION BLOCKED under the frozen two-arm
contract (no intake-S1.json before the run; the
blocker record is the row's evidence). These tests
pin the delivered form: the step-0 gate verdicts in
frozen order, the two-row accounting, the S-5
extraction artifact and its judged occurrence, the
S-1 blocked-arm evidence, and the section 7.2
disposition (superseded-not-retired) as recorded in
the results record.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/065-s1-s5-heading-successor"
RESULTS = REPO / "reports/phase427_results.json"
CANON = (REPO / "glossa-indus/claims/extracted_claims"
         / "ancient_writing_and_modern_technologies"
           "_51831ac9.json")
CANON_ID = ("ancient_writing_and_modern_technologies"
            "_51831ac9_statisti_0004")
ACQUIRED_SHA256 = (
    "77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665"
)
EXTRACTION_SHA256 = (
    "74e42f8e3e4af6488c14540dd8c5b32e2cd5eed0cfdc03eaf82a7043dfcc155d"
)


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def _find_claim(node, claim_id):
    if isinstance(node, dict):
        if node.get("claim_id") == claim_id:
            return node
        for value in node.values():
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    return None


def test_step0_gates_passed_in_frozen_order():
    r = _results()
    gates = r["step0_gates"]
    assert [g["gate"] for g in gates] == [
        "0.1", "0.2", "0.3", "0.4"]
    assert all(g["verdict"] == "PASS" for g in gates)
    pins = gates[0]["pins"]
    assert set(pins) == {"S-1", "S-5"}
    for row in pins.values():
        assert row["cleaned_text_match"] is True
        assert row["registry_match"] is True
        assert row["claims_entry_facts_match"] is True
    for rec in gates[0]["record_inputs"].values():
        assert rec["match"] is True
    # Gate 0.2: the acquired file asserted by size,
    # SHA-256, and MD5.
    acq = gates[1]["acquired_file"]
    assert acq["present"] is True
    assert acq["size_bytes"] == 657863
    assert acq["sha256"] == ACQUIRED_SHA256
    assert acq["md5"] == "36616e20a2c62be106ebf9c3d4093fd6"
    # Gate 0.3: the blocked-arm determination and its
    # evidence.
    det = gates[2]["determination"]
    assert det["arm"] == "blocked arm"
    assert det["intake_record_exists"] is False
    ev = det["evidence"]
    assert ev["provenance_states_no_entry_taken"] is True
    assert ev["s1_download_folder_files"] == ["BLOCKED.md"]
    assert ev["delivered_s1_file_in_downloads_tree"] is False


def test_accounting_is_two_rows_one_outcome_each():
    r = _results()
    rows = r["accounting"]
    assert [row["source"] for row in rows] == ["S-1", "S-5"]
    assert rows[0]["outcome"] == (
        "STILL UNLOCATED — ACQUISITION BLOCKED")
    assert rows[1]["outcome"] == "HEADING ABSENT FROM DOCUMENT"
    assert r["headline_class"] == (
        "B — S-5 RESOLVED, S-1 STILL BLOCKED")
    assert "S-1 remains STILL UNLOCATED" in r["headline"]
    assert ACQUIRED_SHA256 in r["headline"]
    # S-1: no document searched; the blocker record is
    # the evidence.
    assert rows[0]["document_searched"] is None
    assert "BLOCKED.md" in rows[0]["blocker_ref"]
    assert "owner account act" in rows[0]["evidence_ref"] or (
        "blocker record" in rows[0]["evidence_ref"])


def test_s5_extraction_artifact_and_judged_occurrence():
    r = _results()
    s5 = {row["source"]: row for row in r["accounting"]}["S-5"]
    assert s5["document_searched"] == ACQUIRED_SHA256
    ext = s5["extraction"]
    artifact = SPEC_DIR / "extraction-S5.txt"
    data = artifact.read_bytes()
    assert hashlib.sha256(data).hexdigest() == (
        EXTRACTION_SHA256)
    assert ext["sha256"] == EXTRACTION_SHA256
    assert ext["bytes"] == 84672
    assert ext["lines"] == 2273
    # Exactly one occurrence in the whole text layer,
    # at the recorded locator, judged not heading form.
    text = data.decode("utf-8")
    assert text.lower().count("positional analysis") == 1
    occ = s5["occurrence_list"]
    assert len(occ) == 1
    assert occ[0]["extraction_line"] == 340
    assert occ[0]["page"] == 9
    assert occ[0]["heading_form"] is False
    assert "waterworks. Positional analysis" in occ[0][
        "line_text"]
    lines = text.split("\n")
    assert "Positional analysis" in lines[339]
    assert lines[340].strip().startswith(
        "shows a clear tripartite administrative grammar")
    assert "5.5 Governance and Civic Authority" in lines[335]


def test_disposition_and_anchors():
    # The disposition append itself is verified at the
    # act (outcome.md: removing the appended entry
    # reproduces the pre-act file byte-identically).
    # It is not asserted on the live claims file here:
    # the backend suite regenerates the extracted-claims
    # store during a full run (the freeze's Spec 038
    # posture), which can rewrite that file before this
    # test reads it. Pinned here: the frozen record's
    # own state, which regeneration preserves, and the
    # results record's disposition.
    r = _results()
    canon = _find_claim(
        json.loads(CANON.read_text(encoding="utf-8")),
        CANON_ID)
    assert canon["claim_status"] == "untested"
    assert canon["stage"] == "created"
    assert canon["proposition_fingerprint"] == (
        "a4874349e0cc0ba23b711f10c78f60372639c2dc6f352165b48"
        "d4a9e44272469")
    assert r["disposition"].startswith(
        "superseded-not-retired (class B)")
    assert "retirement is not available" in r["disposition"]
    assert r["anchors"]["byte_identical"] is True
    assert r["anchors"]["before_sha256"] == (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e608659"
        "2b32d34f569")
    assert r["fence"] == (
        "This act searched two documents for a heading. "
        "It checked nothing either passage states.")
    assert "unjudged as to S-1" in r["hypothesis_F065_C14"]
