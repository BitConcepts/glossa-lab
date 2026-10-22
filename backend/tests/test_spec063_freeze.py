"""Spec 063 freeze fences (sign-821 identification successor).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, including the preserved drawn-form
reference); (2) the definition carries the frozen
contract exactly - Spec 056's executed record as
predecessor (freeze digest 64c28ce1..., outcome
IDENTIFICATION FAILED at R-3, Phase-418), candidate
K-1 with its argument conditions of record, the
preservation act (drawn-form-reference-821.json,
schema glossa.drawn-form-reference/1, SHA-256
695dd35d..., no images), the step-0 gates in their
three named classes (including the thesis file
asserted on the local file before any plate read),
the identification protocol (step D double
derivation without sight of the drafted wording,
unsettled disagreement resolving AGAINST
identification; step C continuity on the anchors'
agreement; step M routes 1-3 with route 3, the NEW
composition route, carrying its justification -
every step is a drawn form and the number only
locates them), the traps (Yunmapped_0821; sign 861;
P378 as the target), the total three-word outcome
mapping (no retirement word), the recovered
claim's lifecycle position (created, untested,
designed-never-run test note, the DD-056-6 /
DD-056-17 pattern), and Phase-425; (3) the
governed claim register is the frozen register
(15 claims, integrity-clean, recovered to
0.6-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-063-15 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited records
still carry the facts the design rests on (every
spec section 2 pin, verified at the freeze by two
independent routes; the registry's 803 rows, no
W821, its P378 base-sign anchor and Yunmapped_0821
trap; the witness's 157 rows with no grapheme 821;
the held text's locators for the list naming, the
K-1 suggestion, the Figure 2.6 / 6.13 captions,
and the Doubled Signs formation passage; the
passage slice digest; the fragment's live facts
in the Spec 038 form, including its
spec056_closure append). The thesis PDF is a
local file, not a repository file: its digest is
asserted as a definition constant and on the
preserved reference, never on a live repo file.
These tests perform no derivation, no plate read,
and no identification.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/063-sign821-identification-successor"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
REFERENCE = SPEC / "drawn-form-reference-821.json"
SPEC056 = REPO / "specs/056-sign821-recovery"
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json"
)
HELD_TEXT = (
    REPO / "glossa-indus/processed/cleaned_text/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt"
)
PHASE104 = REPO / "glossa-indus/reports/phase104_claims_evaluation.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
WITNESS = REPO / "data/crosswalks/wells_segmentation_witness_v1.csv"
LANE2 = REPO / "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

HELD_TEXT_SHA256 = (
    "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e"
)
REGISTRY_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
WITNESS_SHA256 = (
    "ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da"
)
PHASE104_SHA256 = (
    "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"
)
LANE2_SHA256 = (
    "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
CLAIM_FILE_SHA256 = (
    "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a"
)
PASSAGE_SHA256 = (
    "51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604"
)
SPEC056_FREEZE_DIGEST = (
    "64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e"
)
SPEC056_OUTCOME_SHA256 = (
    "ff16184aa265b68358865c51e8f43dc9c9ec40688a53614792640f1d2e2d844e"
)
SPEC056_EXTRACTION_SHA256 = (
    "ad4a3f747d6ae4e0f13ae984c1169bd4a94570625e7dcc199146ff2ef73fb6ab"
)
REFERENCE_SHA256 = (
    "695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999"
)
THESIS_SHA256 = (
    "4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e"
)
CLAIM_ID = "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001"

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec063-sign821-identification-successor"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.6-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-425"
    # The predecessor record (never patched).
    pred = design["predecessor"]
    assert pred["phase"] == "Phase-418"
    assert pred["freeze_digest"] == SPEC056_FREEZE_DIGEST
    assert pred["outcome"] == "IDENTIFICATION FAILED"
    assert "never edited" in pred["posture"]
    # Candidate K-1, of record.
    cand = design["candidate"]
    assert cand["id"] == CLAIM_ID
    assert cand["candidate"] == "K-1"
    assert "city" in cand["proposition"]
    assert "Dholavira signboard" in cand["proposition"]
    assert "R-1" in cand["record"] and "R-3" in cand["record"]
    # The preservation act: the reference, pinned, no images.
    pres = design["preservation"]
    assert pres["file"] == (
        "specs/063-sign821-identification-successor/"
        "drawn-form-reference-821.json"
    )
    assert pres["sha256"] == REFERENCE_SHA256
    assert pres["schema"] == "glossa.drawn-form-reference/1"
    assert "no image" in pres["posture"]
    # Step 0 gates, in their named classes.
    gates = design["protocol"]["step0_gates"]
    assert "INPUT PIN MISMATCH" in gates
    assert "THESIS FILE PIN MISMATCH" in gates
    assert "REFERENCE NOT PRODUCIBLE" in gates
    assert "before any plate is read" in gates
    assert THESIS_SHA256 in gates
    # Step D: twice, blind, disagreement against identification.
    step_d = design["protocol"]["step_d"]
    assert "two independent derivations" in step_d
    assert "without sight" in step_d
    assert "AGAINST identification" in step_d
    assert "reference not sustained" in step_d
    # Step C: continuity on the anchors' agreement.
    step_c = design["protocol"]["step_c"]
    assert "anchors" in step_c
    assert "formation passage" in step_c
    assert "P378" in step_c
    # Step M: routes 1-3, route 3 new, with its justification.
    step_m = design["protocol"]["step_m"]
    assert "Route 1" in step_m and "Route 2" in step_m
    assert "Route 3" in step_m and "composition" in step_m
    assert "every step is a drawn form" in step_m
    assert "the number is used only to locate them" in step_m
    assert "does not fall back to P378" in step_m
    traps = design["protocol"]["traps"]
    assert "Yunmapped_0821" in traps
    assert "861" in traps
    # Outcomes are total: exactly three words, no retirement.
    assert design["outcomes"] == [
        "RECOVERED",
        "IDENTIFICATION FAILED",
        "CLOSED AT STEP 0",
    ]
    # A recovered claim: created, untested, designed-never-run note.
    rec = design["recovered_claim"]
    assert "created" in rec["lifecycle"]
    assert "untested" in rec["lifecycle"]
    assert "DD-056-6" in rec["lifecycle"]
    assert "appended" in rec["placement"]
    assert "no test is executed" in rec["test_note"]
    assert "DD-056-17" in rec["test_note"]
    # What the freeze does not do, and the execution gate.
    assert "does not establish that sign 821 is identified" in (
        design["freeze_does_not"]
    )
    assert "has not run" in design["freeze_does_not"]
    assert "Not satisfied at the freeze" in design["execution_gate"]
    assert "approval" in design["execution_gate"]
    assert "Phase-425" in design["execution_gate"]
    # Inputs: every section 2 pin, as verified two-route at freeze.
    inputs = definition["inputs"]
    assert inputs["held_text"]["sha256"] == HELD_TEXT_SHA256
    assert inputs["registry"]["sha256"] == REGISTRY_SHA256
    assert inputs["registry"]["rows"] == 803
    assert inputs["registry"]["w821_entries"] == 0
    assert inputs["witness"]["sha256"] == WITNESS_SHA256
    assert inputs["witness"]["rows"] == 157
    assert inputs["spec056_freeze"]["digest"] == SPEC056_FREEZE_DIGEST
    assert inputs["spec056_outcome"]["sha256"] == SPEC056_OUTCOME_SHA256
    assert inputs["spec056_extraction"]["sha256"] == (
        SPEC056_EXTRACTION_SHA256
    )
    assert inputs["claim_file"]["sha256"] == CLAIM_FILE_SHA256
    assert inputs["claim_file"]["claim_id"] == CLAIM_ID
    assert inputs["phase104_evaluation"]["sha256"] == PHASE104_SHA256
    assert inputs["lane2_drafts"]["sha256"] == LANE2_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["passage"]["sha256"] == PASSAGE_SHA256
    assert inputs["reference"]["sha256"] == REFERENCE_SHA256
    assert inputs["thesis_pdf"]["sha256"] == THESIS_SHA256
    assert "two independent routes" in inputs["pin_verification"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.6-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F063-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


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


def test_cited_records_carry_the_design_facts():
    # The preserved reference: pin, schema, and section 6.1 contents.
    reference_bytes = REFERENCE.read_bytes()
    assert hashlib.sha256(reference_bytes).hexdigest() == REFERENCE_SHA256
    reference = json.loads(reference_bytes)
    assert reference["schema"] == "glossa.drawn-form-reference/1"
    assert reference["target"]["sign_number"] == 821
    assert "Figure 2.6" in reference["target"]["list"]
    assert reference["base_sign_registry_anchor"]["row"] == "P378"
    assert reference["base_sign_registry_anchor"]["wells_ids"] == "W820"
    assert reference["base_sign_registry_anchor"]["mahadevan_ids"] == "M391"
    assert reference["base_sign_registry_anchor"]["description"] == (
        "Wheel with 6 spokes with even angles"
    )
    assert "doubled form of sign 820" in reference["descriptor"]
    assert "six sectors" in reference["descriptor"]
    plate = reference["plate_confirmation"]
    assert plate["thesis_page"] == 92
    assert plate["pdf_page"] == 104
    assert plate["file_sha256"] == THESIS_SHA256
    assert "sign 820 doubles to form sign 821" in (
        reference["formation_reference"]["passage_verbatim"]
    )
    trap_names = [t["trap"] for t in reference["traps_named"]]
    assert "Yunmapped_0821" in trap_names
    assert "sign 861" in trap_names
    assert "no image" in reference["license_position"]
    # The predecessor records: freeze digest and outcome hashes.
    spec056_freeze = json.loads(
        (SPEC056 / "freeze.json").read_text(encoding="utf-8")
    )
    assert spec056_freeze["digest"] == SPEC056_FREEZE_DIGEST
    assert (
        hashlib.sha256((SPEC056 / "outcome.md").read_bytes()).hexdigest()
        == SPEC056_OUTCOME_SHA256
    )
    assert (
        hashlib.sha256(
            (SPEC056 / "extraction-record.md").read_bytes()
        ).hexdigest()
        == SPEC056_EXTRACTION_SHA256
    )
    # The claim file: facts on the live file (Spec 038 form).
    claim_doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))
    entry = _find_claim(claim_doc, CLAIM_ID)
    assert entry is not None
    assert entry["normalized_claim"] == (
        "Sign value: 821 / it is used in a variety of contexts (Figure 6"
    )
    assert entry["claim_status"] == "untested"
    assert entry["stage"] == "created"
    assert entry["spec056_closure"]["outcome"] == "IDENTIFICATION FAILED"
    assert entry["spec056_closure"]["phase"] == "Phase-418"
    # The Phase-104 record: UNTESTED under RULE-NUM.
    p104_bytes = PHASE104.read_bytes()
    assert hashlib.sha256(p104_bytes).hexdigest() == PHASE104_SHA256
    p104_entry = _find_claim(json.loads(p104_bytes), CLAIM_ID)
    assert p104_entry is not None
    assert p104_entry["verdict"] == "stays_untested"
    assert p104_entry["rule"] == "RULE-NUM"
    # The registry: pin, 803 rows, no W821, P378 anchor, the trap.
    registry_bytes = REGISTRY.read_bytes()
    assert hashlib.sha256(registry_bytes).hexdigest() == REGISTRY_SHA256
    rows = list(csv.DictReader(registry_bytes.decode("utf-8").splitlines()))
    assert len(rows) == 803
    assert all(
        "W821" not in (r["wells_ids"] or "").split("|") for r in rows
    )
    assert all("W821" not in (r["wells_ids"] or "") for r in rows)
    p378 = [r for r in rows if r["sign_id"] == "P378"][0]
    assert p378["wells_ids"] == "W820"
    assert p378["mahadevan_ids"] == "M391"
    assert p378["description"] == "Wheel with 6 spokes with even angles"
    yun = [r for r in rows if r["sign_id"] == "Yunmapped_0821"][0]
    assert yun["numbering_system"] == "yajnadevam_glyphid"
    assert yun["wells_ids"] == ""
    # The witness: pin, 157 rows, no grapheme 821.
    witness_bytes = WITNESS.read_bytes()
    assert hashlib.sha256(witness_bytes).hexdigest() == WITNESS_SHA256
    wrows = list(
        csv.DictReader(witness_bytes.decode("utf-8").splitlines())
    )
    assert len(wrows) == 157
    assert all(
        "821" not in (r["wells_graphemes"] or "") for r in wrows
    )
    # The held text: pin, locators, and the passage slice.
    text_bytes = HELD_TEXT.read_bytes()
    assert hashlib.sha256(text_bytes).hexdigest() == HELD_TEXT_SHA256
    lines = text_bytes.decode("utf-8").splitlines()
    assert lines[413].startswith(
        "Chapter 2 gives the Indus sign list used in this analysis"
    )
    assert lines[664].startswith("The sign list used here (Wells 2011)")
    assert lines[867].strip() == "Figure 2.6 An Indus Sign List"
    assert lines[871].strip() == "Figure 2.6 An Indus Sign List (Continued)"
    assert lines[875].strip() == "Figure 2.6 An Indus Sign List (Continued)"
    assert lines[879].strip() == "Figure 2.6 An Indus Sign List (Continued)"
    assert "Figure 6.13" in lines[175]
    assert lines[2859].strip().startswith(
        "Figure 6.13. Examples of the various contexts of sign 821."
    )
    assert "It is suggested here that sign 821" in lines[2834]
    assert "city" in lines[2835]
    assert "determinative or as a word" in lines[2835]
    assert lines[3690].strip() == "Doubled Signs"
    formation = " ".join(
        ln.strip() for ln in lines[3691:3694]
    )
    assert "sign 820 doubles to form sign 821" in formation
    assert lines[3705].strip() == (
        "Table AII.4 Comparison of signs and their doubled graphem"
    )
    raw_lines = text_bytes.splitlines(keepends=True)
    passage = b"".join(raw_lines[2782:2871])
    assert len(passage) == 5354
    assert hashlib.sha256(passage).hexdigest() == PASSAGE_SHA256
    # The lane-2 drafts and anchors files: pins only.
    assert hashlib.sha256(LANE2.read_bytes()).hexdigest() == LANE2_SHA256
    assert hashlib.sha256(ANCHORS.read_bytes()).hexdigest() == ANCHORS_SHA256


FREEZE_STAMPS = [
    "20261022T014746Z",
    "20261022T014749Z",
    "20261022T014751Z",
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
