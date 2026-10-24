"""Spec 066 freeze fences (Phase-130 catalogue extension).

Pins: (1) the freeze machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the design
constants exactly as frozen (the 2,101-candidate
census and its set split, the ladder's outcome
classes and reason codes, the 20 percent halt rule
over all graded candidates with the
true-non-identity tripwire, the stratum seed, the
Phase-130 gate pins, the portion / table / layer /
census / schema / validator hashes); (3) the
governed claim register is the frozen register
(15 claims, integrity-clean, recovered to
0.6-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-066-10 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited in-repo
records still carry the facts the design rests on
(the Phase-421 census and results pins and the
Spec 059 closure figures; the intake schema and
validator pins). The restricted material itself is
NOT in the repository and is never read by these
tests: the gate and census facts about it are
pinned through the definition constants, not
through the portion. These tests grade no
candidate, build no layer, and extract nothing.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/066-phase130-catalogue-extension"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CENSUS = REPO / "reports/phase421_join_census.json"
RESULTS421 = REPO / "reports/phase421_results.json"
SCHEMA = REPO / "data/intake/intake_dataset_schema_v1.json"
VALIDATOR = REPO / "backend/glossa_lab/intake.py"
SPEC059_OUTCOME = REPO / "specs/059-f1-object-join/outcome.md"

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
        "spec066-phase130-catalogue-extension"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.6-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-428"
    cand = design["candidates"]
    assert cand["total"] == 2101
    assert cand["referenced"] == 1341
    assert cand["referenced_zero_resolution"] == 1293
    assert cand["referenced_already_joined"] == 48
    assert cand["unreferenced"] == 760
    assert design["outcome_classes"] == [
        "VERIFIED", "CONFLICT", "UNRESOLVED",
    ]
    assert "NUMBER-AMBIGUOUS" in design["conflict_reason_codes"]
    assert design["halt_rule"]["conflict_share_cap"] == 0.2
    assert design["halt_rule"]["base"] == (
        "all 2101 graded candidates")
    assert "non-identity" in design["halt_rule"]["tripwire"]
    assert "EXTENSION HALTED" in design["halt_rule"]["on_halt"]
    assert "20261021" in design["hand_check_stratum"]
    fences = design["fences"]
    assert "never a catalogue object" in fences["string_match"]
    assert "not a verified join" in fences["verified_object"]
    assert "no OSF registration" in fences["no_osf"]
    assert "Satisfied at the freeze" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["portion_pdf"]["sha256"] == (
        "514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a"
    )
    assert inputs["portion_pdf"]["bytes"] == 8206446
    assert inputs["local_table"]["sha256"] == (
        "7179858d9b2bc18b480ba092a08ea2ee021ce569fcaceb5b992d22c541d333c8"
    )
    assert inputs["local_table"]["records"] == 2123
    assert inputs["local_table"][
        "distinct_wellformed_numbers"] == 2101
    assert inputs["local_table"]["sections"] == {
        "mohenjo_daro": 519,
        "harappa_old": 510,
        "harappa_harp": 1094,
    }
    assert inputs["catalogue_layer_base"]["vol1"]["sha256"] == (
        "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e"
    )
    assert inputs["catalogue_layer_base"]["vol2"]["sha256"] == (
        "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9"
    )
    assert inputs["catalogue_layer_base"][
        "merged_distinct_objects"] == 3493
    assert inputs["lineage_layer"]["sha256"] == (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
    )
    assert inputs["phase421_census"]["sha256"] == (
        "952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8"
    )
    assert inputs["phase421_results"]["sha256"] == (
        "3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f"
    )
    assert inputs["intake_schema"]["sha256"] == (
        "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b"
    )
    assert inputs["intake_validator"]["sha256"] == (
        "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03"
    )
    assert "entry 22" in inputs["gate"]["record"]
    assert "section 4 line stays restricted-local" in (
        inputs["gate"]["classification"])


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.6-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F066-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The committed pins the candidate sets and the
    # validator discipline rest on.
    for path, pin in (
        (CENSUS,
         "952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8"),
        (RESULTS421,
         "3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f"),
        (SCHEMA,
         "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b"),
        (VALIDATOR,
         "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03"),
    ):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == pin
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    summary = census["summary"]
    assert summary["layer_rows"] == 5679
    assert summary["joined_rows"] == 2899
    assert summary["unjoined_with_identifier_resolving_zero"] == 2119
    assert census["gate_bar"]["joined_rows_min"] == 3465
    # The Spec 059 record the fences cite: closed at
    # step 0, F1 standing as recorded.
    outcome059 = SPEC059_OUTCOME.read_text(encoding="utf-8")
    assert "JOIN GATE NOT MET" in outcome059
    assert "STUDY-SPEC-024/F1" in outcome059


FREEZE_STAMPS = [
    "20261022T030515Z",
    "20261022T030556Z",
    "20261022T030558Z",
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
