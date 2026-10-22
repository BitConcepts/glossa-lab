"""Spec 064 freeze fences (sign 297 concordance, successor).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, with the covered-source set exact - the
preserved drawn-form reference is a covered
source); (2) the definition carries the frozen
contract exactly - Phase-426, the predecessor
fence (Spec 046 closed IDENTIFICATION FAILED at
step 1.2, its closure delivery standing
unedited), the preserved reference at its pinned
digest with continuity_status QUALIFIED, the
identification protocol (step D twice-derived,
step C mandatory with its pre-registered
closure, step M routes 1 and 2 only), Wells
scored as SOURCE and never counted toward
CONSENSUS, the total outcome mapping carried
from Spec 046, the lists of record as Spec
046's freeze named them, and the delivery in
this spec's own directory; (3) the governed
claim register is the frozen register (15
claims, integrity-clean, recovered to 0.7-draft
at the freeze gate) and the three freeze-hook
artifacts record the pass on the DD-064-18
reading (zero correctness failure modes; only
FR-2.3 draft-cap records; no claim below the
0.70 threshold); (4) the cited records still
carry the facts the design rests on (the
section 2 pins asserted as freeze-time facts
against the definition; the live records
checked for their design facts - the registry
census and traps, the witness M297 caution,
the passage and Figure 2.6 captions in the
held text, the reference record's descriptor,
family anchor, traps, and QUALIFIED status);
(5) the section 5.2 outcome mapping is total
over every score pattern. These tests open no
list for scoring, derive no descriptor, run no
step C, and change no record.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/064-sign297-concordance-successor"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
REFERENCE = SPEC / "drawn-form-reference-297.json"
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
WITNESS = REPO / "data/crosswalks/wells_segmentation_witness_v1.csv"
LANE2 = REPO / "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json"
CONC046 = REPO / "specs/046-horned-tiger-concordance/concordance-297.json"

PINS = {
    CLAIM_RECORD: (
        "997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031"
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
    WITNESS: (
        "ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da"
    ),
    LANE2: (
        "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"
    ),
    CONC046: (
        "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"
    ),
    REFERENCE: (
        "33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4"
    ),
}

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []
    # The covered-source set is exact: nothing else
    # decides the question.
    assert set(record["sources"]) == {
        "specs/064-sign297-concordance-successor/freeze.md",
        "specs/064-sign297-concordance-successor/spec.md",
        "specs/064-sign297-concordance-successor/claims.json",
        "specs/064-sign297-concordance-successor/adjudication.md",
        "specs/064-sign297-concordance-successor/aee/freeze-aee-note.md",
        "specs/064-sign297-concordance-successor/build_freeze.py",
        "specs/064-sign297-concordance-successor/drawn-form-reference-297.json",
        "backend/tests/test_spec064_freeze.py",
    }


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec064-sign297-concordance-successor"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-426"
    assert design["claim_id"] == (
        "the_archaeology_and_epigraphy_of_"
        "indus_w_27f45a68_sign_val_0002"
    )
    # The predecessor fence (DD-064-9).
    pred = design["predecessor"]
    assert pred["phase"] == "Phase-405"
    assert "IDENTIFICATION FAILED" in pred["outcome"]
    assert "step 1.2" in pred["outcome"]
    assert "772db4df" in pred["closure_delivery_sha256"]
    assert "unedited" in pred["posture"]
    # Wells never counts toward CONSENSUS (DD-064-2).
    assert "never counts toward CONSENSUS" in design["source_role"]
    assert "Wells (2015) itself" in design["source_role"]
    # The preserved reference and its qualification.
    proto = design["identification_protocol"]
    ref = proto["reference"]
    assert ref["sha256"] == PINS[REFERENCE]
    assert ref["schema"] == "glossa.drawn-form-reference/1"
    assert ref["continuity_status"] == "QUALIFIED"
    assert "family level only" in ref["qualification"]
    assert "MANDATORY" in proto["step_c"]
    assert "continuity/discrimination not sustained" in proto["step_c"]
    assert "pre-registered" in proto["step_c"]
    assert "twice" in proto["step_d"]
    assert "reference not sustained" in proto["step_d"]
    assert "Route 1" in proto["step_m"]
    assert "Route 2" in proto["step_m"]
    assert "821" in proto["step_m"]
    # The lists of record, as Spec 046's freeze named them.
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
    # The delivery: this successor's own directory (DD-064-1).
    delivery = design["delivery"]
    assert "concordance-297.json" in delivery["file"]
    assert "064-sign297-concordance-successor" in delivery["file"]
    assert "producer_spec" in delivery["file"]
    assert "empty array" in delivery["closure_form"]
    assert "flagged_disputed" in delivery["asset_a_feed"]
    assert "only this successor's delivery" in delivery["asset_a_feed"]
    # Inputs: every section 2 pin, as verified two routes.
    inputs = definition["inputs"]
    assert inputs["claim_record"]["sha256"] == PINS[CLAIM_RECORD]
    assert inputs["source_book_held_text"]["sha256"] == PINS[SOURCE_TEXT]
    assert inputs["phase104_evaluation"]["sha256"] == PINS[PHASE104]
    assert inputs["crosswalk_registry"]["sha256"] == PINS[REGISTRY]
    assert inputs["crosswalk_registry"]["rows"] == 803
    assert inputs["wells_witness"]["sha256"] == PINS[WITNESS]
    assert inputs["lane2_drafts"]["sha256"] == PINS[LANE2]
    assert inputs["spec046_closure_delivery"]["sha256"] == PINS[CONC046]
    assert inputs["drawn_form_reference"]["sha256"] == PINS[REFERENCE]
    assert inputs["thesis_pdf"]["sha256"].startswith("4b39330c")
    assert "not committed" in inputs["thesis_pdf"]["posture"]
    assert "two independent routes" in inputs["pin_verification"]
    # The execution gate is NOT satisfied at the freeze.
    assert "NOT satisfied at the freeze" in design["execution_gate"]
    assert "no concordance row exists" in design["execution_gate"]
    assert "does not establish" in design["freeze_does_not"]
    assert "step C" in design["freeze_does_not"]


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
        f"F064-C{i:02d}" for i in range(1, 16)
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
    # checkout. Live byte equality is NOT asserted here
    # for the claim-lifecycle records (claim record,
    # Phase-104 evaluation, lane-2 drafts): the suite's
    # own Spec 029 regeneration tests rewrite those
    # records in the working tree before this test runs
    # (the Spec 046 freeze amendment, freeze.md section
    # 6 of that spec). What this test asserts live is
    # that every cited record is present and still
    # carries the design facts the freeze rests on.
    for path in PINS:
        assert path.is_file(), path
    # The Spec 046 closure delivery: a frozen file in a
    # frozen directory, asserted byte-exact.
    assert hashlib.sha256(CONC046.read_bytes()).hexdigest() == PINS[CONC046]
    closure = json.loads(CONC046.read_text(encoding="utf-8"))
    assert closure["producer_spec"] == "046"
    assert closure["schema"] == "glossa.concordance/1"
    assert closure["signs"] == []
    assert "IDENTIFICATION FAILED" in closure["closure"]["class"]
    # The preserved reference: byte-exact at its pin, and
    # carrying the section 6.2 record's facts.
    assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest() == PINS[REFERENCE]
    ref = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert ref["schema"] == "glossa.drawn-form-reference/1"
    assert ref["target"]["sign_number"] == 297
    assert "four long parallel strokes bent once" in ref["descriptor"]["text"]
    assert "289-308" in ref["descriptor"]["text"]
    assert ref["plate_reference"]["thesis_page"] == 90
    assert ref["plate_reference"]["pdf_page"] == 102
    assert ref["plate_reference"]["file_sha256"].startswith("4b39330c")
    anchor = ref["family_anchor_2015"]
    assert anchor["row"] == "P205"
    assert "W297" in anchor["wells_ids"].split("|")
    assert anchor["mahadevan_ids"] == "M180"
    assert "NOT an identification" in anchor["status"]
    assert ref["continuity_status"]["status"] == "QUALIFIED"
    traps = " ".join(ref["traps_named"])
    assert "Ladder motif" in traps
    assert "924" in traps
    assert "M180" in traps
    # The registry census and the traps of spec section 4.5.
    rows = list(
        csv.DictReader(io.StringIO(REGISTRY.read_text(encoding="utf-8")))
    )
    assert len(rows) == 803
    p297 = [r for r in rows if r["parpola_id"] == "P297"]
    assert len(p297) == 1
    assert "Ladder motif" in p297[0]["description"]
    assert p297[0]["wells_ids"] == ""
    p205 = [r for r in rows if r["parpola_id"] == "P205"]
    assert len(p205) == 1
    assert "W297" in p205[0]["wells_ids"].split("|")
    assert p205[0]["mahadevan_ids"] == "M180"
    assert not any("tiger" in r["description"].lower() for r in rows)
    # The witness: no grapheme 297; M297's grapheme is 924.
    wrows = list(
        csv.DictReader(io.StringIO(WITNESS.read_text(encoding="utf-8")))
    )
    assert len(wrows) == 157
    graphemes = set()
    for r in wrows:
        graphemes.update(
            g.strip() for g in r["wells_graphemes"].split(";") if g.strip()
        )
    assert "297" not in graphemes
    m297 = [r for r in wrows if r["sign"] == "M297"]
    assert len(m297) == 1
    assert m297[0]["wells_graphemes"] == "924"
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
    # The source text carries the passage and captions.
    source_text = SOURCE_TEXT.read_text(encoding="utf-8")
    assert "sign 297 represents the horned tiger" in source_text
    assert source_text.count("Figure 2.6 An Indus Sign List") >= 4
    assert "The sign list used here (Wells 2011)" in source_text
    # The Phase-104 record carries the RULE-NUM stop.
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
    "20261022T015228Z",
    "20261022T015229Z",
    "20261022T015230Z",
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
