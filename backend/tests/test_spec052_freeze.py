"""Spec 052 freeze fences (Farmer 'not writing' —
the amended NB-1 design on the Shakti corpus layer).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly — battery NB-1 as specified in
the amendment (position classes and the partition
property, the N(s) >= 20 floor, the 2/3 and 1/2
strength bands, opening bigrams over B, the
within-sequence permutation null of 999
permutations at seed 43052 with the nearest-rank
95th-percentile chance level, conditions F and O,
the NB-1.9 thinness gate), the two populations
with their freeze-recorded counts (primary 3,045
rows / 11,805 tokens / 557 signs; sensitivity
5,131 / 17,216 / 707), step-0 gates A–D with
BATTERY NOT PINNABLE retired and NOT ADJUDICATED
retained, the re-pointed outcome semantics of
amendment section 6, Phase-437, and the claims
served (the parent claim SETTLED — contradicted,
its status unmoved by any outcome; the three
restatement fragments); (3) the governed claim
register is the frozen register (19 claims,
integrity-clean, recovered at 0.8-draft in three
rounds) and the three freeze-hook artifacts
record the pass on the DD-038-10 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold,
minimum 0.72); (4) the cited records still carry
the facts the design rests on (the intake record
at its pin; the Phase-43 record at its pin with
its anchor facts — 201 signs, 3,137 sequences, 20
TERMINAL_STRONG, the ten exhibited rates
0.683–0.892 with smallest total 22, the (267, 99)
candidate at 251 / 0.74; the parent claim's
record at its freeze hash — moved from the
draft's pin by the dated 2026-10-22 Spec 025
audit note — with its status, stage and three
contradicting-evidence entries; the fragments'
records; Spec 068's freeze digest). The
restricted-local corpus and row-grades files are
asserted as definition constants only, in the
Spec 038 form: they are never committed, so no
live-file hash is asserted on them in the suite;
execution gates A and B recompute them. These
tests compute no positional quantity, classify
no sign, and assign no outcome word.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/052-farmer-not-writing-soviet"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
INTAKE = REPO / "docs/decisions/2026-10-22-shakti-corpus-intake-record.md"
PHASE43 = REPO / "outputs/phase43_all.json"
FARMER = (
    REPO
    / "glossa-indus/claims/extracted_claims/"
    "farmer_sproat_witzel_2004.json"
)
FRAGMENTS_A = (
    REPO
    / "glossa-indus/claims/extracted_claims/"
    "indus_valley_script_deciphered_from_myth_65ff0a26.json"
)
FRAGMENTS_B = (
    REPO
    / "glossa-indus/claims/extracted_claims/"
    "without_kings_or_conquests_the_indus_scr_ce9d98cc.json"
)
SPEC068_FREEZE = (
    REPO / "specs/068-yadav-zipf-controls-successor/freeze.json"
)

CORPUS_SHA256 = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
GRADES_SHA256 = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
INTAKE_SHA256 = "bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d"
SPEC068_DIGEST = "ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d"
PHASE43_SHA256 = "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4"
FARMER_SHA256 = "41a855c9a79845206d7e63ed6fd835ef60f3611f3e825de5d73615ffba85425e"

sys.path.insert(0, str(REPO / "backend"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == "spec052-farmer-not-writing-soviet"
    assert definition["register"]["claims"] == 19
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.72" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-437"
    # Battery NB-1.
    batt = design["battery"]
    assert "partition property" in batt["NB-1.2"]
    assert "length 1" in batt["NB-1.2"]
    assert "N(s) >= 20" in batt["NB-1.4"]
    assert "smallest total" in batt["NB-1.4"]
    assert "2/3" in batt["NB-1.5"] and "0.683" in batt["NB-1.5"]
    assert "B = the number of sequences of length >= 2" in batt["NB-1.6"]
    assert "999 permutations" in batt["NB-1.7"]
    assert "seed 43052" in batt["NB-1.7"]
    assert "950th" in batt["NB-1.7"]
    assert "condition F" in batt["NB-1.8"] and "Condition O" in batt["NB-1.8"]
    assert "30 sequences of length" in batt["NB-1.9"]
    assert "10 classifiable signs" in batt["NB-1.9"]
    # Populations.
    pops = design["populations"]
    assert "3,045" in pops["primary"] and "11,805" in pops["primary"]
    assert "557 distinct signs" in pops["primary"]
    assert "90 classifiable" in pops["primary"]
    assert "5,131" in pops["sensitivity"] and "17,216" in pops["sensitivity"]
    assert "707 distinct signs" in pops["sensitivity"]
    assert "never enter git" in pops["venue"]
    assert "not" in pops["lineage_limit"] and "independent discovery" in pops[
        "lineage_limit"
    ]
    # Gates.
    gates = design["gates"]
    assert "INVALID" in gates["A"] and "INVALID" in gates["B"]
    assert "seed 43052" in gates["C"]
    assert "TOO THIN" in gates["D"]
    assert "BATTERY NOT PINNABLE cannot occur" in gates["retired"]
    assert "NOT ADJUDICATED is retained" in gates["retained"]
    # Outcomes and the claims served.
    assert design["outcomes"] == [
        "CONSISTENT",
        "INCONSISTENT",
        "PARTIAL",
        "TOO THIN",
    ]
    assert "re-pointed" in design["outcome_semantics"]
    assert "neither condition F nor condition O" in design["outcome_semantics"]
    served = design["claims_served"]
    assert "contradicted" in served["farmer_sproat_witzel_2004_manual_001"]
    assert "no outcome of the amended run moves it" in served[
        "farmer_sproat_witzel_2004_manual_001"
    ]
    assert "critique_0001" in served["fragments"]
    assert "critique_0002" in served["fragments"]
    assert "ce9d98cc_language_0001" in served["fragments"]
    assert "Phase-437" in design["execution_gate"]
    assert "separate" in design["execution_gate"]
    assert "does not execute" in design["freeze_does_not"] or (
        "execute the study" in design["freeze_does_not"]
    )
    # Inputs: the pins as asserted at the freeze.
    inputs = definition["inputs"]
    assert inputs["shakti_corpus"]["sha256"] == CORPUS_SHA256
    assert inputs["shakti_corpus"]["census"]["rows"] == 5704
    assert inputs["shakti_corpus"]["census"]["analyzable"] == 5536
    assert inputs["shakti_corpus"]["census"]["grades"] == {
        "documented-lineage": 3212,
        "undocumented-corroborated": 2087,
        "undocumented-uncorroborated": 405,
    }
    assert inputs["row_grades"]["sha256"] == GRADES_SHA256
    assert inputs["intake_record"]["sha256"] == INTAKE_SHA256
    assert "bfc811df" in inputs["intake_record"]["merged"]
    assert inputs["spec_068_record"]["freeze_digest"] == SPEC068_DIGEST
    assert inputs["phase43_record"]["sha256"] == PHASE43_SHA256
    assert inputs["phase43_record"]["facts"]["terminal_strong_count"] == 20
    assert inputs["phase43_record"]["facts"]["exhibited_smallest_total"] == 22
    assert inputs["farmer_claim_record"]["sha256"] == FARMER_SHA256
    assert "51cf8b3c" in inputs["farmer_claim_record"]["note"]
    assert "retired" in inputs["soviet_tables"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F052-C{i:02d}" for i in range(1, 20)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The cited records, live in the tree, at their pins.
    assert _sha(INTAKE) == INTAKE_SHA256
    assert _sha(PHASE43) == PHASE43_SHA256
    assert _sha(FARMER) == FARMER_SHA256
    rec068 = json.loads(SPEC068_FREEZE.read_text(encoding="utf-8"))
    assert rec068["digest"] == SPEC068_DIGEST
    # The Phase-43 record's anchor facts.
    p43 = json.loads(PHASE43.read_text(encoding="utf-8"))
    assert p43["T1_1_corpus_v3"]["total_sequences"] == 3137
    t22 = p43["T2_2_terminal_suffix_table"]
    assert t22["terminal_strong_count"] == 20
    assert t22["initial_strong_count"] == 40
    assert t22["total_signs_profiled"] == 201
    exhibited = t22["terminal_strong"]
    assert len(exhibited) == 10
    rates = [x["t_rate"] for x in exhibited]
    assert min(rates) == 0.683 and max(rates) == 0.892
    assert min(x["total"] for x in exhibited) == 22
    cand = p43["T2_3_cv_pair"]["m77_candidate"]
    assert (cand["a"], cand["b"]) == (267, 99)
    assert cand["bigram_count"] == 251
    assert cand["dominance"] == 0.74
    # The parent claim's record: status, stage, contradicting items.
    farmer_doc = json.loads(FARMER.read_text(encoding="utf-8"))
    parent = farmer_doc["claims"][0]
    assert parent["claim_id"] == "farmer_sproat_witzel_2004_manual_001"
    assert parent["claim_status"] == "contradicted"
    assert parent["stage"] == "explained"
    assert len(parent["contradicting_evidence"]) == 3
    # The three fragments: present, settled as restatements.
    frag_a = json.loads(FRAGMENTS_A.read_text(encoding="utf-8"))
    frag_b = json.loads(FRAGMENTS_B.read_text(encoding="utf-8"))
    by_id = {
        c["claim_id"]: c for c in frag_a["claims"] + frag_b["claims"]
    }
    for fid in (
        "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
        "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
        "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
    ):
        assert by_id[fid]["claim_status"] == "contradicted"


FREEZE_STAMPS = [
    "20261024T032847Z",
    "20261024T032850Z",
    "20261024T032853Z",
]

CORRECTNESS_CATEGORIES = {
    "coverage_gap",
    "contradiction",
    "assumption_unvalidated",
    "ambiguous_requirement",
    "independence_unmodeled",
}


def test_freeze_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase, stamp in zip(
        ("after_specify", "after_plan", "after_tasks"),
        FREEZE_STAMPS,
    ):
        record = json.loads(
            (aee_dir / f"aee-{phase}-{stamp}.json").read_text(
                encoding="utf-8")
        )
        failures = [
            f for c in record["claims"] for f in c["failures"]
        ]
        assert failures, phase
        assert {f["category"] for f in failures} <= {"draft_cap"}, phase
        assert not [
            f for f in failures
            if f["category"] in CORRECTNESS_CATEGORIES
        ], phase
        confidences = [c["confidence"] for c in record["claims"]]
        assert min(confidences) >= 0.70, phase
