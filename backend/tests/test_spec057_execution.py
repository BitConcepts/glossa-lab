"""Spec 057 execution tests (Phase-419).

The execution's terminal outcome is headline class C
— PARTIAL RECOVERY WITH UNLOCATED SOURCES (r=2, e=1,
u=2): S-3 and S-4 each state a checkable positional
classification finding, recovered at the created
stage; S-2's held chapter excerpt states the method
and no checkable finding (PASSAGE EMPTY); S-1 and
S-5 carry no heading-form occurrence in their held
texts (SOURCE UNLOCATED, sub-state HEADING NOT
PRESENT IN HELD TEXT, DD-057-10). These tests pin
the delivered form: the step-0 gate verdicts, the
five-row accounting, the passage artifacts as exact
byte slices of the pinned cleaned texts, the intake
records' lifecycle position, and the section 7.2
disposition append on the canonical record.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/057-five-sources-heading"
RESULTS = REPO / "reports/phase419_results.json"
CANON = (REPO / "glossa-indus/claims/extracted_claims"
         / "ancient_writing_and_modern_technologies"
           "_51831ac9.json")
CANON_ID = ("ancient_writing_and_modern_technologies"
            "_51831ac9_statisti_0004")

PASSAGES = {
    "S-2": ("fuls2023_catalog_of_indussigns_searchins"
            "_1dbdecdb", (536, 615)),
    "S-3": ("positional_analysis_of_indus_signs"
            "_a2bedc93", (54, 601)),
    "S-4": ("the_archaeology_and_epigraphy_of_indus_w"
            "_27f45a68", (3455, 3822)),
}


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


def test_step0_gates_passed_in_order():
    r = _results()
    gates = r["step0_gates"]
    assert [g["gate"] for g in gates] == ["0.1", "0.2", "0.3"]
    assert all(g["verdict"] == "PASS" for g in gates)
    pins = gates[0]["pins"]
    assert len(pins) == 5
    for row in pins.values():
        assert row["cleaned_text_match"] is True
        assert row["registry_match"] is True
        assert row["claims_entry_facts_match"] is True
    for rec in gates[0]["record_inputs"].values():
        assert rec["match"] is True
    assert gates[1]["evidence_instance_claim_ids"] == [
        "fuls2023_catalog_of_indussigns_searchins"
        "_1dbdecdb_statisti_0001",
        "positional_analysis_of_indus_signs_a2bedc93"
        "_statisti_0001",
        "the_archaeology_and_epigraphy_of_indus_w"
        "_27f45a68_statisti_0003",
        "without_kings_or_conquests_the_indus_scr"
        "_ce9d98cc_statisti_0002",
    ]


def test_accounting_is_complete_and_counts_match():
    r = _results()
    rows = r["accounting"]
    assert [row["source"] for row in rows] == [
        "S-1", "S-2", "S-3", "S-4", "S-5"]
    assert [row["outcome"] for row in rows] == [
        "SOURCE UNLOCATED", "PASSAGE EMPTY",
        "CLAIM RECOVERED", "CLAIM RECOVERED",
        "SOURCE UNLOCATED"]
    assert r["counts"] == {"r": 2, "e": 1, "u": 2}
    assert r["headline_class"] == (
        "C — PARTIAL RECOVERY WITH UNLOCATED SOURCES")
    for row in rows:
        if row["outcome"] == "SOURCE UNLOCATED":
            assert row["sub_state"] == (
                "HEADING NOT PRESENT IN HELD TEXT")
            log = row["search_log"]
            assert log["step_2_repository_search"][
                "cleaned_text_copies_found"]
            assert log["step_4_source_document"][
                "copies_of_original_filename_in_repo"] == []
            assert "unblocking" not in row or row[
                "unblocking_act"]
            assert "Re-acquisition" in row["unblocking_act"]


def test_passage_artifacts_are_exact_pinned_slices():
    r = _results()
    rows = {row["source"]: row for row in r["accounting"]}
    for sid, (doc_id, (start, end)) in PASSAGES.items():
        raw = (REPO / "glossa-indus/processed/cleaned_text"
               / f"{doc_id}.txt").read_bytes()
        kept = raw.decode("utf-8").splitlines(keepends=True)
        expected = b"".join(
            x.encode("utf-8") for x in kept[start - 1:end])
        artifact = (SPEC_DIR / "passages"
                    / f"passage-{sid}.txt").read_bytes()
        assert artifact == expected
        digest = hashlib.sha256(artifact).hexdigest()
        assert digest == rows[sid]["locator"]["passage_sha256"]
        assert rows[sid]["locator"]["cleaned_text_lines"] == [
            start, end]


def test_recovered_claims_enter_at_created_stage():
    r = _results()
    rows = {row["source"]: row for row in r["accounting"]}
    for sid, fname in [("S-3", "intake-S3.json"),
                       ("S-4", "intake-S4.json")]:
        intake = json.loads(
            (SPEC_DIR / fname).read_text(encoding="utf-8"))
        assert intake["stage"] == "created"
        assert intake["status"] == "unchecked"
        assert intake["claim_id"] == rows[sid][
            "recovered_claim_id"]
        assert intake["numbers"]
        assert "falsifier written" in intake[
            "falsifier_status"]
        assert "382, 790, 832, and 892" in intake[
            "proposition"]


def test_disposition_append_and_anchors():
    r = _results()
    canon = _find_claim(
        json.loads(CANON.read_text(encoding="utf-8")),
        CANON_ID)
    assert canon["claim_status"] == "untested"
    assert canon["stage"] == "created"
    disp = canon["disposition"]
    assert disp["form"] == "superseded"
    assert disp["phase"] == "Phase-419"
    for cid in ("fuls2013_positional_analysis"
                "_057_recovered_0001",
                "wells2015_appendix_ii_positional_analysis"
                "_057_recovered_0001"):
        assert cid in disp["wording"]
    assert r["anchors"]["byte_identical"] is True
    assert r["fence"] == (
        "This act recovered what five passages state. "
        "It checked none of it.")
