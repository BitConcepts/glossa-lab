"""Spec 065 freeze fences (S-1/S-5 heading successor).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, with the covered-source set exact); (2) the
definition carries the frozen contract exactly -
Phase-427, the predecessor fence (Spec 057 closed
class C with S-1 and S-5 SOURCE UNLOCATED, its
freeze digest standing), the two rows at their
pins, the acquired S-5 file at its pinned hashes
with its CC-BY-4.0 licence and established edition
relationship, the frozen S-1 two-arm contract with
its no-contact fence, the frozen outcome set, the
headline classes, and the retirement rule (retires
only when both sources resolve); (3) the governed
claim register is the frozen register (15 claims,
integrity-clean, recovered to 0.6-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-065-14 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (the section 2 pins asserted as
freeze-time facts against the definition; the live
records checked for their design facts - the two
rows' entries and quote fragments, the Spec 057
outcome postures, and the anchors pin). These
tests search no text layer, judge no heading, and
change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/065-s1-s5-heading-successor"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
SPEC057 = REPO / "specs/057-five-sources-heading"

S1_TEXT = (
    REPO / "glossa-indus/processed/cleaned_text/"
    "ancient_writing_and_modern_technologies_51831ac9.txt"
)
S1_CLAIMS = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "ancient_writing_and_modern_technologies_51831ac9.json"
)
S1_REGISTRY = (
    REPO / "glossa-indus/literature/documents/"
    "ancient_writing_and_modern_technologies_51831ac9.json"
)
S5_TEXT = (
    REPO / "glossa-indus/processed/cleaned_text/"
    "without_kings_or_conquests_the_indus_scr_ce9d98cc.txt"
)
S5_CLAIMS = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "without_kings_or_conquests_the_indus_scr_ce9d98cc.json"
)
S5_REGISTRY = (
    REPO / "glossa-indus/literature/documents/"
    "without_kings_or_conquests_the_indus_scr_ce9d98cc.json"
)
FREEZE057 = SPEC057 / "freeze.json"
OUTCOME057 = SPEC057 / "outcome.md"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

PINS = {
    S1_TEXT: (
        "1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4"
    ),
    S1_REGISTRY: (
        "92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c"
    ),
    S5_TEXT: (
        "dd58497528db89fe75111d2431b9611aebd4a5a9715a4ecceb012d9d1538029e"
    ),
    S5_REGISTRY: (
        "38122256305b8451e49e4ef4d56df7399363bdc3c57052b10f9165ab593261a7"
    ),
    FREEZE057: (
        "3cc68c372790d6bd62d9ab1bb43b15ec2f43502dd614150d660d33b4c452d8af"
    ),
    OUTCOME057: (
        "d3ae1325bdba52295bd44990db024957c1d3aceeb462ddbf60af73b512834a58"
    ),
    ANCHORS: (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
    ),
}

CLAIMS_CONSTANTS = {
    S1_CLAIMS: (
        "e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8"
    ),
    S5_CLAIMS: (
        "c1a433d539a0ed899fe7ab11af2be0c608cb85d9f0fc99b2ccfefdb6e866262a"
    ),
}

FINGERPRINT = (
    "a4874349e0cc0ba23b711f10c78f60372639c2dc6f352165b48d4a9e44272469"
)
DIGEST057 = (
    "237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9"
)
ACQUIRED_S5_SHA256 = (
    "77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665"
)

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []
    # The covered-source set is exact: nothing else
    # decides the question.
    assert set(record["sources"]) == {
        "specs/065-s1-s5-heading-successor/freeze.md",
        "specs/065-s1-s5-heading-successor/spec.md",
        "specs/065-s1-s5-heading-successor/claims.json",
        "specs/065-s1-s5-heading-successor/adjudication.md",
        "specs/065-s1-s5-heading-successor/aee/freeze-aee-note.md",
        "specs/065-s1-s5-heading-successor/build_freeze.py",
        "backend/tests/test_spec065_freeze.py",
    }


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec065-s1-s5-heading-successor"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.6-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-427"
    assert design["claim_under_test"]["id"] == (
        "ancient_writing_and_modern_"
        "technologies_51831ac9_statisti_0004"
    )
    assert design["claim_under_test"]["fingerprint"] == FINGERPRINT
    # The predecessor fence (DD-065-1).
    pred = design["predecessor"]
    assert pred["phase"] == "Phase-419"
    assert "class C" in pred["outcome"]
    assert "HEADING NOT PRESENT IN HELD TEXT" in pred["outcome"]
    assert pred["freeze_digest"] == DIGEST057
    assert "unedited" in pred["posture"]
    assert "superseded-not-retired" in pred["posture"]
    # The two rows, at their pins.
    rows = {r["source"]: r for r in design["rows"]}
    assert set(rows) == {"S-1", "S-5"}
    assert rows["S-1"]["cleaned_text_sha256"] == PINS[S1_TEXT]
    assert rows["S-1"]["registry_file_sha256"] == PINS[S1_REGISTRY]
    assert rows["S-1"]["claims_file_freeze_constant"] == (
        CLAIMS_CONSTANTS[S1_CLAIMS]
    )
    assert rows["S-1"]["quote_fragment"] == "positional analysis"
    assert "NOT ACQUIRED" in rows["S-1"]["acquisition"]
    assert rows["S-5"]["cleaned_text_sha256"] == PINS[S5_TEXT]
    assert rows["S-5"]["registry_file_sha256"] == PINS[S5_REGISTRY]
    assert rows["S-5"]["claims_file_freeze_constant"] == (
        CLAIMS_CONSTANTS[S5_CLAIMS]
    )
    assert rows["S-5"]["quote_fragment"] == "Positional analysis"
    assert "ACQUIRED" in rows["S-5"]["acquisition"]
    # The acquired S-5 file, its licence, its edition.
    acq = design["acquired_s5"]
    assert acq["sha256"] == ACQUIRED_S5_SHA256
    assert acq["md5"] == "36616e20a2c62be106ebf9c3d4093fd6"
    assert acq["size_bytes"] == 657863
    assert "CC-BY-4.0" in acq["licence"]
    assert "supersedes" in acq["licence"]
    assert "ESTABLISHED" in acq["edition_relationship"]
    assert "acquired file, not the held cleaned text" in (
        acq["edition_relationship"]
    )
    assert "gate 0.2" in acq["posture"]
    # The frozen S-1 contract and its fence.
    s1 = design["s1_contract"]
    assert "intake-S1.json" in s1["search_arm"]
    assert "ACQUISITION BLOCKED" in s1["blocked_arm"]
    assert "owner account act" in s1["blocked_arm"]
    assert "never contacts Fuls" in s1["fence"]
    assert "never creates an account" in s1["fence"]
    # The frozen outcome set and headline classes.
    outcomes = design["outcome_set"]
    assert "document-level finding" in outcomes[
        "HEADING ABSENT FROM DOCUMENT"
    ]
    assert "S-1 only" in outcomes[
        "STILL UNLOCATED - ACQUISITION BLOCKED"
    ]
    assert design["headline_classes"] == {
        "A": "BOTH SOURCES RESOLVED",
        "B": "S-5 RESOLVED, S-1 STILL BLOCKED",
    }
    # The retirement rule, carried verbatim.
    assert "retires only when both sources resolve" in (
        design["retirement_rule"]
    )
    assert "superseded-not-retired" in design["retirement_rule"]
    # Prior assessments carry no standing.
    assert "no standing" in design["prior_assessments"]
    assert "Spec 055 rule" in design["prior_assessments"]
    # Inputs: every section 2 pin, as verified two routes.
    inputs = design["inputs"]
    assert inputs["s1_cleaned_text"]["sha256"] == PINS[S1_TEXT]
    assert inputs["s1_registry"]["sha256"] == PINS[S1_REGISTRY]
    assert inputs["s5_cleaned_text"]["sha256"] == PINS[S5_TEXT]
    assert inputs["s5_registry"]["sha256"] == PINS[S5_REGISTRY]
    assert inputs["spec057_freeze_record"]["sha256"] == PINS[FREEZE057]
    assert inputs["spec057_freeze_record"]["digest"] == DIGEST057
    assert inputs["spec057_outcome"]["sha256"] == PINS[OUTCOME057]
    assert inputs["anchors"]["sha256"] == PINS[ANCHORS]
    assert "two independent routes" in inputs["pin_verification"]
    # The execution gate is NOT satisfied at the freeze.
    assert "NOT satisfied at the freeze" in design["execution_gate"]
    assert "no outcome row exists" in design["execution_gate"]
    assert "does not establish" in design["freeze_does_not"]
    assert "has not run" in design["freeze_does_not"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.6-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F065-C{i:02d}" for i in range(1, 16)
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
    # checkout. Live byte equality IS asserted here for
    # the frozen predecessor records and the held texts
    # and registries (files no suite regenerates).
    for path, pin in PINS.items():
        assert path.is_file(), path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == pin, path
    # Spec 057's freeze digest recomputes as recorded.
    freeze057 = json.loads(FREEZE057.read_text(encoding="utf-8"))
    assert freeze057["digest"] == DIGEST057
    # Spec 057's outcome carries the two rows' postures.
    outcome = OUTCOME057.read_text(encoding="utf-8")
    assert "PARTIAL RECOVERY WITH UNLOCATED" in outcome
    assert "S-1" in outcome and "S-5" in outcome
    assert "HEADING NOT PRESENT IN HELD TEXT" in outcome
    assert "not retired while a source remains unlocated" in outcome
    # The two rows' extracted-claims entries carry their
    # facts (the store is regenerated by the suite, so
    # entry facts - never live hashes - are asserted,
    # the Spec 057 convention).
    s1 = json.loads(S1_CLAIMS.read_text(encoding="utf-8"))
    e1 = next(
        c for c in s1["claims"]
        if c["claim_id"] == (
            "ancient_writing_and_modern_"
            "technologies_51831ac9_statisti_0004"
        )
    )
    assert e1["claim_status"] == "untested"
    assert e1["quote_fragment"] == "positional analysis"
    s5 = json.loads(S5_CLAIMS.read_text(encoding="utf-8"))
    e5 = next(
        c for c in s5["claims"]
        if c["claim_id"] == (
            "without_kings_or_conquests_the_indus_scr_"
            "ce9d98cc_statisti_0002"
        )
    )
    assert e5["claim_status"] == "untested"
    assert e5["quote_fragment"] == "Positional analysis"
    # The fingerprint stands on both files' entries.
    blob = S1_CLAIMS.read_text(encoding="utf-8") + S5_CLAIMS.read_text(
        encoding="utf-8"
    )
    assert blob.count(FINGERPRINT) >= 2
    # The held texts carry the postures Spec 057 recorded
    # (string occurrences only - no heading is judged here).
    t1 = S1_TEXT.read_text(encoding="utf-8").lower()
    assert t1.count("positional analysis") == 2
    t5 = S5_TEXT.read_text(encoding="utf-8").lower()
    assert t5.count("positional analysis") == 1


FREEZE_STAMPS = [
    "20261022T031035Z",
    "20261022T031035Z",
    "20261022T031035Z",
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
