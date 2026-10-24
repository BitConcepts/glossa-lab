"""Spec 074 freeze fences (Hunt opening signs on the repaired surface).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
design exactly - Spec 070's test carried with the
five named changes of spec section 1.3: the
repaired surface (Registry v2 / Asset A v2), the
two-leg keying route (DD-074-8), the reproduction
assertion and POPULATION NOT REPRODUCED closure
(DD-074-9), DD-070-11's disposition carried
(DD-074-10), the outcome classes, the OSF filing
(DD-074-11), and Phase 440 (DD-074-12); (3) the
governed claim register is the frozen register (13
claims, recovered to 0.7-draft, integrity-clean) and
the three freeze-hook artifacts record the pass on
the DD-074-13 reading (DD-038-10 form: failures all
FR-2.3 draft-cap records, zero correctness modes,
no claim below the 0.70 threshold, minimum
propagated 0.795); (4) the cited records still
carry the facts the design rests on - Asset A v2's
and Registry v2's digests, row counts and per-kind
counts in Spec 073's executed record and recomputed
from the canonical CSVs, the intake record's Shakti
pins, the registry v1, crosswalk and anchors pins
recomputing in the tree, the Phase-433 record's
facts (Spec 070's freeze digest, its POPULATION NOT
KEYED outcome, its 31-sign enumeration and class
census), and the two-leg keyability fact this
successor exists on: all 31 of Spec 070's recorded
opening-strong signs resolve to exactly one Asset A
v2 row each, over a combined Wells map of 708
distinct ids with zero ambiguous. These tests run
no arm, compute no depicted-kind share, and measure
no test quantity.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/074-hunt-opening-signs-repaired-surface"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
ASSET_CSV = (
    REPO
    / "specs/073-keying-surface-repair/asset-a-v2/depicted-kind-classification.csv"
)
ASSET_FREEZE = (
    REPO
    / "specs/073-keying-surface-repair/asset-a-v2/asset-a-v2-freeze.json"
)
REGISTRY_V2 = REPO / "data/crosswalks/canonical_sign_registry_v2.csv"
REGISTRY_V2_FREEZE = (
    REPO
    / "specs/073-keying-surface-repair/registry-v2/registry-v2-freeze.json"
)
INTAKE = REPO / "docs/decisions/2026-10-22-shakti-corpus-intake-record.md"
REGISTRY_V1 = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
PHASE433 = REPO / "reports/phase433_results.json"

ASSET_V2_SHA256 = (
    "681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193"
)
REGISTRY_V2_SHA256 = (
    "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"
)
REGISTRY_V1_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
CROSSWALK_SHA256 = (
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
PHASE433_SHA256 = (
    "667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214"
)
SPEC070_FREEZE_DIGEST = (
    "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
)

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
    assert (
        definition["experiment_id"]
        == "spec074-hunt-opening-signs-repaired-surface"
    )
    assert definition["register"]["claims"] == 13
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "0.795" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase 440"
    assert "805/2,267" in design["battery"]
    assert "documented + corroborated" in design["populations"]
    assert "DD-049-3" in design["precedence"]
    assert "DD-074-8" in design["keying"]
    assert "DD-074-10" in design["disposition"]
    assert "POPULATION NOT KEYED" in design["disposition"]
    assert design["outcomes"] == [
        "SUPPORTED",
        "NOT SUPPORTED",
        "INCONCLUSIVE",
        "ASSET NOT FROZEN",
        "ASSET PIN MISMATCH",
        "SHAKTI INTAKE NOT REPRODUCED",
        "POPULATION NOT REPRODUCED",
        "POPULATION NOT KEYED",
        "INVALID",
    ]
    assert "DD-074-11" in design["osf"]
    assert "Phase 440" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["asset_a_v2"]["sha256"] == ASSET_V2_SHA256
    assert inputs["asset_a_v2"]["per_kind_counts"]["animal"] == 30
    assert inputs["asset_a_v2"]["per_kind_counts"]["contested"] == 0
    assert inputs["registry_v2"]["sha256"] == REGISTRY_V2_SHA256
    assert inputs["registry_v2"]["rows"] == 1013
    assert (
        inputs["spec070_record"]["freeze_digest"] == SPEC070_FREEZE_DIGEST
    )
    assert (
        inputs["spec070_record"]["phase433_results"]["sha256"]
        == PHASE433_SHA256
    )
    assert inputs["shakti_corpus"]["corpus_sha256"] == CORPUS_SHA256
    assert inputs["shakti_corpus"]["row_grades_sha256"] == GRADES_SHA256
    assert inputs["canonical_registry_v1"]["sha256"] == REGISTRY_V1_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "33e49b65" in inputs["pin_verification"]
    assert "708" in inputs["pin_verification"]


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.7-draft"
    claims = register["claims"]
    assert len(claims) == 13
    ids = [c["id"] for c in claims]
    assert ids == [f"F074-C{i:02d}" for i in range(1, 14)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert ASSET_V2_SHA256 in by_id["F074-C05"]["boundary"]
    assert REGISTRY_V2_SHA256 in by_id["F074-C05"]["boundary"]
    assert "icit_wells" in by_id["F074-C08"]["boundary"]
    assert "DD-070-9" in by_id["F074-C08"]["boundary"]
    assert "DD-070-11" in by_id["F074-C08"]["boundary"]
    assert "POPULATION NOT KEYED" in by_id["F074-C08"]["boundary"]
    assert "DD-070-10" in by_id["F074-C11"]["boundary"]


FREEZE_STAMPS = [
    "20261024T232206Z",
    "20261024T232209Z",
    "20261024T232212Z",
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
        assert record["phase"] == phase
        failures = [
            f for c in record["claims"] for f in c["failures"]
        ]
        assert failures, phase
        assert {f["category"] for f in failures} <= {"draft_cap"}, phase
        assert not [
            f
            for f in failures
            if f["category"] in CORRECTNESS_CATEGORIES
        ], phase
        confidences = [c["confidence"] for c in record["claims"]]
        assert min(confidences) >= 0.70, phase
        scores = record["scores"]
        assert (
            min(s["propagated_score"] for s in scores.values()) >= 0.70
        ), phase
        evaluator = (
            aee_dir / f"evaluator-aee-{phase}-{stamp}.json"
        )
        assert evaluator.exists(), phase


def test_input_pins_recompute():
    assert _sha(ASSET_CSV) == ASSET_V2_SHA256
    asset_freeze = json.loads(ASSET_FREEZE.read_text(encoding="utf-8"))
    assert asset_freeze["sha256"] == ASSET_V2_SHA256
    assert asset_freeze["row_count"] == 552
    assert asset_freeze["per_kind_counts"]["animal"] == 30
    with ASSET_CSV.open(encoding="utf-8") as fh:
        asset_rows = list(csv.DictReader(fh))
    assert len(asset_rows) == 552
    per_kind = Counter(r["depicted_kind"] for r in asset_rows)
    expected_kinds = {
        "animal": 30,
        "sky_cycle": 0,
        "object_goods": 22,
        "human": 43,
        "other": 246,
        "contested": 0,
        "unidentified": 211,
    }
    assert {k: per_kind.get(k, 0) for k in expected_kinds} == expected_kinds
    assert set(per_kind) <= set(expected_kinds)
    assert _sha(REGISTRY_V2) == REGISTRY_V2_SHA256
    registry_freeze = json.loads(
        REGISTRY_V2_FREEZE.read_text(encoding="utf-8")
    )
    assert registry_freeze["sha256"] == REGISTRY_V2_SHA256
    assert registry_freeze["rows_total"] == 1013
    assert registry_freeze["base_v1_sha256"] == REGISTRY_V1_SHA256
    with REGISTRY_V2.open(encoding="utf-8") as fh:
        registry_rows = list(csv.DictReader(fh))
    assert len(registry_rows) == 1013
    assert _sha(REGISTRY_V1) == REGISTRY_V1_SHA256
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    intake_text = INTAKE.read_text(encoding="utf-8")
    assert CORPUS_SHA256 in intake_text
    assert GRADES_SHA256 in intake_text
    # The Phase-433 record still carries the facts gate 0.4
    # reproduces against.
    assert _sha(PHASE433) == PHASE433_SHA256
    phase433 = json.loads(PHASE433.read_text(encoding="utf-8"))
    assert phase433["spec_freeze_digest"] == SPEC070_FREEZE_DIGEST
    assert phase433["outcome"] == "POPULATION NOT KEYED"
    assert phase433["O_size"] == 31
    assert {
        u["wells_code"] for u in phase433["unkeyable_O_signs"]
    } == {"136", "298", "401", "617", "824"}
    census = phase433["population"]["battery_class_counts_primary"]
    assert census == {
        "TERMINAL_STRONG": 42,
        "MEDIAL_STRONG": 81,
        "TERMINAL_MODERATE": 37,
        "INITIAL_MODERATE": 6,
        "MIXED": 23,
        "INITIAL_STRONG": 31,
    }
    # The keyability fact this successor exists on, recomputed
    # under the frozen two-leg route (DD-074-8): leg 1 the
    # parpola_1982 rows' wells_ids; leg 2 the icit_wells rows,
    # whose sign_id is the Wells id itself.
    asset_keys = {r["sign_key"] for r in asset_rows}
    leg1: dict[str, set[str]] = {}
    leg2: dict[str, str] = {}
    for row in registry_rows:
        if row["numbering_system"] == "parpola_1982":
            for wells in (row["wells_ids"] or "").split("|"):
                if wells:
                    leg1.setdefault(wells, set()).add(row["sign_id"])
        elif row["numbering_system"] == "icit_wells":
            leg2[row["sign_id"]] = row["sign_id"]
    assert not [w for w, keys in leg1.items() if len(keys) > 1]
    assert len(set(leg1) | set(leg2)) == 708
    enumeration = phase433["population"]["O_enumeration_wells_space"]
    assert len(enumeration) == 31
    for entry in enumeration:
        wells = "W" + entry["wells_code"]
        resolved = set()
        if wells in leg1:
            resolved |= leg1[wells]
        if wells in leg2:
            resolved.add(leg2[wells])
        hits = [k for k in resolved if k in asset_keys]
        assert len(hits) == 1, entry["wells_code"]
