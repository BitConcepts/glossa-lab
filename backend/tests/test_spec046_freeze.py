"""Spec 046 freeze fences (horned-tiger concordance).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, with the covered-source set exact);
(2) the definition carries the frozen contract
exactly - Phase-405, the four lists of record
named at the freeze (DD-046-10 to DD-046-12),
Wells scored as SOURCE and never counted toward
CONSENSUS (DD-046-2), the total outcome mapping
with the freeze-confirmed PARTIAL CONCURRENCE
word (DD-046-9), the delivery and closure form
(DD-046-1), and the Spec 045 cross-check finding
recorded for Spec 045's freeze (DD-046-14);
(3) the governed claim register is the frozen
register (15 claims, integrity-clean, recovered
to 0.7-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-046-16 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited records
still carry the facts the design rests on (the
section 2 pins asserted as freeze-time facts
against the definition; the live records checked
for their design facts, the registry census of 803 rows, and
the two registry traps of spec section 4.3:
Parpola P297 the Ladder motif, and W297 inside
the multi-value wells_ids cell on the P205 row);
(5) the section 5.2 outcome mapping is total over
every score pattern. These tests open no list
for scoring, match no drawn sign, and change no
record.
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/046-horned-tiger-concordance"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CLAIM_RECORD = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json"
)
SOURCE_TEXT = (
    REPO / "glossa-indus/processed/cleaned_text/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt"
)
PHASE104 = REPO / "glossa-indus/reports/phase104_claims_evaluation.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
LANE2 = REPO / "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json"

PINS = {
    CLAIM_RECORD: (
        "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a"
    ),
    SOURCE_TEXT: (
        "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"
    ),
    PHASE104: (
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"
    ),
    REGISTRY: (
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
    ),
    LANE2: (
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"
    ),
}

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []
    # The covered-source set is exact: nothing else
    # decides the question (prefix integrity of the
    # freeze payload - the digest covers precisely
    # these sources, no more, no fewer).
    assert set(record["sources"]) == {
        "specs/046-horned-tiger-concordance/freeze.md",
        "specs/046-horned-tiger-concordance/spec.md",
        "specs/046-horned-tiger-concordance/claims.json",
        "specs/046-horned-tiger-concordance/adjudication.md",
        "specs/046-horned-tiger-concordance/aee/freeze-aee-note.md",
        "specs/046-horned-tiger-concordance/build_freeze.py",
        "backend/tests/test_spec046_freeze.py",
    }


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec046-horned-tiger-concordance"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-405"
    assert design["claim_id"] == (
        "the_archaeology_and_epigraphy_of_"
        "indus_w_27f45a68_sign_val_0002"
    )
    # Wells never counts toward CONSENSUS (DD-046-2).
    assert "never counts toward CONSENSUS" in design["source_role"]
    assert "Wells (2015) itself" in design["source_role"]
    # The lists of record, named at the freeze.
    lists = design["lists_of_record"]
    assert "Chapter 2" in lists["WELLS"]
    assert "978 1 78491 046 4" in lists["WELLS"]
    assert "Vol. 1" in lists["CISI"] and "Vol. 2" in lists["CISI"]
    assert "MASI 86" in lists["CISI"]
    assert "Deciphering the Indus Script" in lists["PARPOLA"]
    assert "1994" in lists["PARPOLA"]
    assert "No. 77, 1977" in lists["MAHADEVAN"]
    assert "M77" in lists["MAHADEVAN"]
    # The outcome mapping is the frozen, total one.
    mapping = design["outcome_mapping"]
    assert mapping["CONSENSUS"] == "A >= 2 and D = 0"
    assert mapping["CONTESTED"] == "D >= 1, whatever A is"
    assert mapping["PARTIAL CONCURRENCE"] == "A = 1 and D = 0"
    assert mapping["SINGLE-SOURCE"] == "A = 0 and D = 0"
    # The delivery and closure form (DD-046-1).
    delivery = design["delivery"]
    assert "concordance-297.json" in delivery["file"]
    assert "empty array" in delivery["closure_form"]
    assert "closure block" in delivery["closure_form"] or (
        "closure {class, wording}" in delivery["closure_form"]
    )
    assert "flagged_disputed" in delivery["asset_a_feed"]
    # The OPEN-6 finding is on the frozen record.
    assert "PARTIAL CONCURRENCE" in design["open6_finding"]
    assert "Spec 045" in design["open6_finding"]
    # Inputs: the five section 2 pins.
    inputs = definition["inputs"]
    assert inputs["claim_record"]["sha256"] == PINS[CLAIM_RECORD]
    assert inputs["source_book_held_text"]["sha256"] == PINS[SOURCE_TEXT]
    assert inputs["phase104_evaluation"]["sha256"] == PINS[PHASE104]
    assert inputs["crosswalk_registry"]["sha256"] == PINS[REGISTRY]
    assert inputs["crosswalk_registry"]["rows"] == 803
    assert inputs["lane2_drafts"]["sha256"] == PINS[LANE2]
    # The execution gate is NOT satisfied at the freeze.
    assert "NOT satisfied at the freeze" in design["execution_gate"]
    assert "no concordance row exists" in design["execution_gate"]


def _outcome(a_independent_agree: int, d_disagree: int) -> str:
    """The spec section 5.2 mapping, restated for the totality check."""
    if d_disagree >= 1:
        return "CONTESTED"
    if a_independent_agree >= 2:
        return "CONSENSUS"
    if a_independent_agree == 1:
        return "PARTIAL CONCURRENCE"
    return "SINGLE-SOURCE"


def test_outcome_mapping_is_total():
    outcomes = {
        _outcome(a, d) for a in range(4) for d in range(5)
    }
    assert outcomes == {
        "CONSENSUS",
        "CONTESTED",
        "PARTIAL CONCURRENCE",
        "SINGLE-SOURCE",
    }
    assert _outcome(2, 0) == "CONSENSUS"
    assert _outcome(3, 0) == "CONSENSUS"
    assert _outcome(1, 0) == "PARTIAL CONCURRENCE"
    assert _outcome(0, 0) == "SINGLE-SOURCE"
    assert _outcome(0, 1) == "CONTESTED"
    assert _outcome(3, 2) == "CONTESTED"


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F046-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert item["observed_at"] == "2026-10-21"
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The section 2 pins are freeze-time facts: they are
    # asserted against freeze.json's definition in
    # test_freeze_definition_constants, and the step-0
    # pin check is an execution-time act over a pristine
    # checkout (spec section 5.1). Live byte equality is
    # NOT asserted here for the claim-lifecycle records
    # (claim record, Phase-104 evaluation, lane-2
    # drafts): the suite's own Spec 029 regeneration
    # tests rewrite those records in the working tree
    # before this test runs, with fresh extracted_at
    # timestamps (observed in CI run 39581775853, where
    # the claim record's live hash differed from its
    # committed bytes for exactly that reason; the
    # amendment is recorded in freeze.md). What this
    # test asserts live is that every cited record is
    # present and still carries the design facts the
    # freeze rests on.
    for path in PINS:
        assert path.is_file(), path
    # The registry census and the two traps of spec section 4.3.
    rows = list(
        csv.DictReader(io.StringIO(REGISTRY.read_text(encoding="utf-8")))
    )
    assert len(rows) == 803
    p297 = [r for r in rows if r["parpola_id"] == "P297"]
    assert len(p297) == 1
    assert "Ladder motif" in p297[0]["description"]
    p205 = [r for r in rows if r["parpola_id"] == "P205"]
    assert len(p205) == 1
    assert "W297" in p205[0]["wells_ids"].split("|")
    # The claim record carries the fragment as stated.
    claim_doc = json.loads(CLAIM_RECORD.read_text(encoding="utf-8"))
    entry = next(
        c
        for c in claim_doc["claims"]
        if c["claim_id"]
        == (
            "the_archaeology_and_epigraphy_of_indus_w_"
            "27f45a68_sign_val_0002"
        )
    )
    assert entry["claim_status"] == "untested"
    assert "horned tiger" in entry["normalized_claim"]
    # The source text carries the passage verbatim.
    source_text = SOURCE_TEXT.read_text(encoding="utf-8")
    assert "sign 297 represents the horned tiger" in source_text
    # The Phase-104 record carries the RULE-NUM stop for this claim.
    evaluation = json.loads(PHASE104.read_text(encoding="utf-8"))
    found = []

    def _walk(node):
        if isinstance(node, dict):
            if node.get("claim_id") == entry["claim_id"]:
                found.append(node)
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for value in node:
                _walk(value)

    _walk(evaluation)
    assert found and found[0]["rule"] == "RULE-NUM"
    assert found[0]["verdict"] == "stays_untested"
    # The lane-2 drafts carry the adopted draft for this claim.
    assert entry["claim_id"] in LANE2.read_text(encoding="utf-8")


FREEZE_STAMPS = [
    "20261021T095612Z",
    "20261021T095616Z",
    "20261021T095619Z",
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
                encoding="utf-8"
            )
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
