"""Spec 073 freeze fences (keying-surface repair).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the governing source list and
hierarchy confirmed at the freeze (OPEN-073-1:
CISI governing first, Fuls 2023 Catalog second,
Parpola 1994 third in held form, Fuls 2023 Corpus
corroborating; Mahadevan 1977 and Wells 1998
struck from this study's ruled list for
non-exhibition; Yajnadevam, the Fuls OCR texts
and the ICIT documentation locators only),
Registry v2's form and the icit_wells value
(OPEN-073-2), the attested frame (OPEN-073-3:
documented + corroborated rows), the row_origin
field (OPEN-073-4), two-pass entry checking with
no added spot check (OPEN-073-5), direct entry
with d18_input = none (OPEN-073-6), the OSF
contract registration filed at the freeze
(OPEN-073-7), Phase-436 (OPEN-073-8), the
baselines A-D and the outcome classes of spec
section 7; (3) the governed claim register is
the frozen register (16 claims, integrity-clean,
recovered at 0.9-draft in four rounds) and the
three freeze-hook artifacts record the pass on
the DD-038-10 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited records
still carry the facts the design rests on (the
section 2 pins live in the tree; the registry's
498-id Wells map and the five codes' absence;
Asset A v1's census; the Phase 433/434 machine
records' baselines and closures). The
restricted-local corpus and row-grades files are
asserted as definition constants only, in the
Spec 038 form: they are never committed, so no
live-file hash is asserted on them in the suite;
execution gate 0.1 recomputes them. These tests
add no registry row, classify no sign, and
compute no coverage figure.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/073-keying-surface-repair"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
MASTER = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ASSET_A = REPO / "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv"
PHASE433 = REPO / "reports/phase433_results.json"
PHASE434 = REPO / "reports/phase434_results.json"

REGISTRY_SHA256 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
MASTER_SHA256 = "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
ASSET_A_SHA256 = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
SPEC045_DIGEST = "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
SPEC070_DIGEST = "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
SPEC071_DIGEST = "c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478"
PHASE433_SHA256 = "667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214"
PHASE434_SHA256 = "7158f79ce416e5e01fee041e6e97df827d3a048f9c1c178a8200bd79f68bbda7"
CORPUS_SHA256 = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
GRADES_SHA256 = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"

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
    assert definition["experiment_id"] == "spec073-keying-surface-repair"
    assert definition["register"]["claims"] == 16
    assert definition["register"]["register_version"] == "0.9-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.795" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-436"
    served = design["claims_served"]
    assert "manual_003" in served["manual_003"]
    assert "IN QUESTION" in served["manual_003"]
    assert "manual_004" in served["manual_004"]
    assert "UNTESTED" in served["manual_004"]
    # The hierarchy and the strikes (OPEN-073-1).
    hier = design["hierarchy"]
    assert "CISI" in hier["ruling"]
    assert "Catalog of Indus Signs" in hier["ruling"]
    assert "Parpola 1994" in hier["ruling"]
    assert "locators only" in hier["ruling"].lower()
    struck = hier["struck_at_the_freeze"]
    assert "10.11575/PRISM/23641" in struck["wells_1998"]
    assert "403" in struck["wells_1998"]
    assert "introduction" in struck["mahadevan_1977"]
    assert "ad2f1e218a34b8c33c57de0d6cb8d99272765bbb" in hier["exhibits"]
    # Registry v2 (OPEN-073-2, DD-073-2/3).
    reg = design["registry_v2"]
    assert reg["path"] == "data/crosswalks/canonical_sign_registry_v2.csv"
    assert "icit_wells" in reg["ruling"]
    assert "CONTESTED IDENTITY" in reg["ruling"]
    assert "no-published-identity.json" in reg["ruling"]
    # The frame (OPEN-073-3) and the asset (OPEN-073-4/5/6).
    assert "documented and corroborated" in design["frame"]
    asset = design["asset_a_v2"]
    assert "carried_v1" in asset["ruling"]
    assert "new_entry" in asset["ruling"]
    assert "two passes" in asset["entry"]
    assert "d18_input = none" in asset["entry"]
    assert "unidentified" in asset["entry"]
    # Baselines, measures, outcomes.
    base = design["baselines"]
    assert "31 signs" in base["A"]
    assert "617 (56)" in base["A"]
    assert "557 distinct signs" in base["B"]
    assert "285" in base["B"] and "134" in base["B"] and "138" in base["B"]
    assert "498 distinct Wells ids" in base["C"]
    assert "sky_cycle 0" in base["D"]
    assert "M5" in design["measures"]
    assert "floor of 30" in design["measures"]
    assert design["outcomes"] == [
        "KEYING SURFACE REPAIRED",
        "REPAIRED WITH NAMED SHORTFALL",
        "INPUT PIN MISMATCH",
        "SHAKTI INTAKE NOT REPRODUCED",
        "BASELINE NOT REPRODUCED",
        "SOURCE NOT IN HAND",
        "ENTRY DISCIPLINE FAILED",
        "ASSET FAILED (gate named)",
        "FROZEN INPUT MUTATED",
    ]
    assert "adds no registry row" in design["freeze_does_not"]
    assert "Phase-436" in design["execution_gate"]
    # Inputs: the pins as asserted at the freeze.
    inputs = definition["inputs"]
    assert inputs["registry_v1"]["sha256"] == REGISTRY_SHA256
    assert inputs["registry_v1"]["rows"] == 803
    assert inputs["registry_v1"]["wells_map_distinct_ids"] == 498
    assert inputs["registry_v1"]["five_codes_absent"] == [
        "W136", "W298", "W401", "W617", "W824",
    ]
    assert inputs["crosswalk"]["sha256"] == MASTER_SHA256
    assert inputs["asset_a_v1"]["csv_sha256"] == ASSET_A_SHA256
    assert inputs["asset_a_v1"]["census"]["sky_cycle"] == 0
    assert SPEC045_DIGEST in inputs["asset_a_v1"]["contract"]
    assert inputs["spec_070_record"]["freeze_digest"] == SPEC070_DIGEST
    assert inputs["spec_070_record"]["machine_record"]["sha256"] == PHASE433_SHA256
    assert inputs["spec_071_record"]["freeze_digest"] == SPEC071_DIGEST
    assert inputs["spec_071_record"]["machine_record"]["sha256"] == PHASE434_SHA256
    assert inputs["shakti_corpus"]["sha256"] == CORPUS_SHA256
    assert inputs["row_grades"]["sha256"] == GRADES_SHA256
    assert "bfc811df" in inputs["intake_record"]["merged"]
    assert "31729a4f" in inputs["fuls_volumes"]["catalog_pdf_sha256"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.9-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F073-C{i:02d}" for i in range(1, 17)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The section 2 pins, live in the tree.
    assert _sha(REGISTRY) == REGISTRY_SHA256
    assert _sha(MASTER) == MASTER_SHA256
    assert _sha(ASSET_A) == ASSET_A_SHA256
    assert _sha(PHASE433) == PHASE433_SHA256
    assert _sha(PHASE434) == PHASE434_SHA256
    # The cited freezes still carry their digests.
    for spec_dir, digest in (
        ("045-hunt-depicted-kinds", SPEC045_DIGEST),
        ("070-hunt-opening-signs-successor", SPEC070_DIGEST),
        ("071-hunt-sky-signs-successor", SPEC071_DIGEST),
    ):
        rec = json.loads(
            (REPO / "specs" / spec_dir / "freeze.json").read_text(
                encoding="utf-8")
        )
        assert rec["digest"] == digest
    # The registry facts the repair starts from (Baseline C + Break 1).
    rows = list(csv.DictReader(REGISTRY.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 803
    wells_ids = set()
    for r in rows:
        if r["numbering_system"] == "parpola_1982":
            wells_ids.update(t for t in r["wells_ids"].split("|") if t)
    assert len(wells_ids) == 498
    all_wells = set()
    for r in rows:
        all_wells.update(t for t in r["wells_ids"].split("|") if t)
    assert not {"W136", "W298", "W401", "W617", "W824"} & all_wells
    # Asset A v1's census (Baseline D).
    asset_rows = list(csv.DictReader(ASSET_A.read_text(encoding="utf-8").splitlines()))
    assert len(asset_rows) == 187
    census = {}
    for r in asset_rows:
        census[r["depicted_kind"]] = census.get(r["depicted_kind"], 0) + 1
    assert all(
        census.get(k, 0) == v
        for k, v in {
            "animal": 20, "sky_cycle": 0, "object_goods": 14, "human": 25,
            "other": 127, "contested": 0, "unidentified": 1,
        }.items()
    )
    # The Phase 433 record (Baseline A): closure, set size, the five codes.
    p433 = json.loads(PHASE433.read_text(encoding="utf-8"))
    assert p433["outcome"] == "POPULATION NOT KEYED"
    assert p433["spec_freeze_digest"] == SPEC070_DIGEST
    assert p433["O_size"] == 31
    assert [u["wells_code"] for u in p433["unkeyable_O_signs"]] == [
        "136", "298", "401", "617", "824",
    ]
    counts = {
        e["wells_code"]: e["total"]
        for e in p433["population"]["O_enumeration_wells_space"]
    }
    assert counts["136"] == 6
    assert counts["298"] == 7
    assert counts["401"] == 5
    assert counts["617"] == 56
    assert counts["824"] == 16
    # The Phase 434 record (Baseline B): closure and the coverage census.
    p434 = json.loads(PHASE434.read_text(encoding="utf-8"))
    assert p434["outcome"] == "INVALID"
    assert p434["spec_freeze_digest"] == SPEC071_DIGEST
    cov = p434["gate_0_3_coverage"]
    assert cov["signs_occurring_in_primary_population"] == 557
    assert cov["signs_carrying_an_asset_row"] == 285
    assert cov["sky_cycle_rows_in_asset"] == 0


FREEZE_STAMPS = [
    "20261023T131036Z",
    "20261023T131041Z",
    "20261023T131046Z",
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
