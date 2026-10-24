"""Tests for the Spec 052 execution records.

Phase-437 (Farmer NB-1 on the Shakti layer)
executed under the frozen amended contract:
the step-0 gates passed, the battery produced
the INCONSISTENT outcome on the primary
population with the sensitivity run agreeing,
and the outcome was appended in the same words
to the parent claim's record and to each of
the three fragments' records, as the frozen
spec section 4.2 requires. These tests pin the
recorded facts: a gate figure, a census
number, a condition value, or an append that
drifts from the executed run fails here.

Author: Spec 052 (Phase-437), 2026-10-24.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports/phase437_results.json"
SPEC_DIR = (
    REPO_ROOT / "specs/052-farmer-not-writing-soviet"
)
APPEND_KEY = "spec052_outcome_append_2026_10_24"

FRAGMENTS = {
    "glossa-indus/claims/extracted_claims/"
    "farmer_sproat_witzel_2004.json": [
        "farmer_sproat_witzel_2004_manual_001",
    ],
    "glossa-indus/claims/extracted_claims/"
    "indus_valley_script_deciphered_from_myth_65ff0a26.json": [
        "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
        "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    ],
    "glossa-indus/claims/extracted_claims/"
    "without_kings_or_conquests_the_indus_scr_ce9d98cc.json": [
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
    ],
}


def _results() -> dict:
    return json.loads(RESULTS.read_text("utf-8"))


def test_phase437_results_record_complete():
    r = _results()
    text = RESULTS.read_text("utf-8")
    assert r["spec"] == "052"
    assert r["phase"] == 437
    assert r["contract"]["freeze_digest"] == (
        "83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019"
    )
    assert r["contract"]["osf_registration"] == "7cu23"
    assert "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68" in text
    assert "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739" in text


def test_step0_gates_all_passed_in_order():
    r = _results()
    verdicts = [g["verdict"] for g in r["gates"]]
    assert verdicts == ["PASS", "PASS", "PASS", "PASS"]
    assert r["closure"] is None


def test_census_reproduces_the_freeze_counts():
    r = _results()
    p = r["census"]["primary"]
    assert p["rows"] == 3045
    assert p["tokens"] == 11805
    assert p["distinct_signs"] == 557
    assert p["len_1"] == 103
    assert p["len_ge_2"] == 2942
    assert p["len_ge_3"] == 2068
    assert p["classifiable"] == 90
    s = r["census"]["sensitivity"]
    assert s["rows"] == 5131
    assert s["tokens"] == 17216
    assert s["distinct_signs"] == 707
    assert s["len_ge_3"] == 2889
    # NB-1 classifiability counts occurrences in
    # sequences of length >= 2 (sign 540 carries
    # its remaining occurrences as single-sign
    # inscriptions); the freeze census's 112
    # counted total occurrences. See
    # step0-record.md's census note.
    assert s["classifiable"] == 111
    assert any(
        "540" in n for n in r["census_notes"]
    )


def test_outcome_inconsistent_with_conditions():
    r = _results()
    assert r["outcome"] == "INCONSISTENT"
    b = r["battery_primary"]
    assert b["conditions"]["F"]["holds"] is True
    assert b["conditions"]["O"]["holds"] is True
    assert b["terminal_strong_count"] == 7
    assert b["strong_sets"]["terminal"] == [
        "034", "413", "501", "503", "692", "817",
        "820",
    ]
    assert b["null"]["terminal_strong_count"][
        "chance_level_950th"
    ] == 0
    assert b["opening"]["top_bigram"] == [
        "400", "740"
    ]
    assert b["opening"]["top_count"] == 179
    assert b["opening"]["B"] == 2942
    assert b["null"]["max_opening_bigram_count"][
        "chance_level_950th"
    ] == 76
    assert r["sensitivity_outcome"] == "INCONSISTENT"
    bs = r["battery_sensitivity"]
    assert bs["conditions"]["F"]["holds"] is True
    assert bs["conditions"]["O"]["holds"] is True
    assert bs["terminal_strong_count"] == 9
    assert bs["opening"]["top_count"] == 235


def test_anchors_byte_identical_after_run():
    r = _results()
    assert r["anchors"]["byte_identical"] is True
    assert r["anchors"]["before"] == (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
    )
    assert r["anchors"]["after"] == r["anchors"]["before"]


def test_outcome_appended_in_same_words_everywhere():
    r = _results()
    text = r["outcome_append_text"]
    seen = 0
    for rel, ids in FRAGMENTS.items():
        d = json.loads(
            (REPO_ROOT / rel).read_text("utf-8")
        )
        for c in d["claims"]:
            if c["claim_id"] not in ids:
                continue
            seen += 1
            entry = c.get(APPEND_KEY)
            assert entry is not None, c["claim_id"]
            assert entry["note"] == text
            assert entry["outcome"] == "INCONSISTENT"
            assert entry["date"] == "2026-10-24"
            assert c["claim_status"] == "contradicted"
    assert seen == 4


def test_regeneration_preserves_the_outcome_append(tmp_path):
    """The extracted-claims generator regenerates the store
    wholesale (the Spec 029 tests do it in-tree); the dated
    section 4.2 outcome append is a record, not extraction
    output, and the generator's dated-append carry-over must
    preserve it — and the 2026-10-22 audit note — verbatim.
    (CI on this spec's execution PR caught the append being
    stripped in-tree before the carry-over existed.)"""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "indus_claims",
        REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lit = tmp_path / "documents"
    lit.mkdir()
    processed = tmp_path / "cleaned"
    processed.mkdir()
    out_dir = tmp_path / "extracted"
    out_dir.mkdir()
    prior_text = (
        REPO_ROOT
        / "glossa-indus/claims/extracted_claims/"
        "farmer_sproat_witzel_2004.json"
    ).read_text("utf-8")
    prior = json.loads(prior_text)
    (lit / "farmer_sproat_witzel_2004.json").write_text(
        json.dumps({"title": prior["title"]}), "utf-8"
    )
    (out_dir / "farmer_sproat_witzel_2004.json").write_text(
        prior_text, "utf-8"
    )
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document(
        "farmer_sproat_witzel_2004"
    )
    assert result["status"] == "extracted"
    regenerated = json.loads(
        (out_dir / "farmer_sproat_witzel_2004.json").read_text(
            "utf-8"
        )
    )
    (claim,) = [
        c
        for c in regenerated["claims"]
        if c["claim_id"]
        == "farmer_sproat_witzel_2004_manual_001"
    ]
    prior_claim = prior["claims"][0]
    assert claim[APPEND_KEY] == prior_claim[APPEND_KEY]
    assert (
        claim["audit_note_2026_10_22"]
        == prior_claim["audit_note_2026_10_22"]
    )
    assert claim["claim_status"] == "contradicted"


def test_outcome_record_carries_the_result():
    outcome = (SPEC_DIR / "outcome.md").read_text(
        "utf-8"
    )
    step0 = (SPEC_DIR / "step0-record.md").read_text(
        "utf-8"
    )
    assert "INCONSISTENT" in outcome
    assert "400, 740" in outcome
    assert "7cu23" in outcome
    assert "PASS" in step0
