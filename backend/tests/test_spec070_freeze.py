"""Spec 070 freeze fences (Hunt opening signs successor on Shakti).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
design exactly - the Phase-43 battery applied new,
the documented-primary / S-C populations, the test
form and section 4.3 precedence, the keying route
(DD-070-9), the counting rule (DD-070-10), the
POPULATION NOT KEYED disposition (DD-070-11), the
outcome classes, the OSF filing (DD-070-12), and
Phase 433 (DD-070-13); (3) the governed claim
register is the frozen register (13 claims,
recovered to 0.9-frozen-candidate, integrity-clean)
and the three freeze-hook artifacts record the pass
on the DD-070-14 reading (zero failure modes; no
claim below the 0.70 threshold; minimum propagated
0.845); (4) the cited records still carry the facts
the design rests on - Asset A's digest and per-kind
counts in Spec 069's executed record, the intake
record's Shakti pins, and the registry, crosswalk
and anchors pins recomputing in the tree. These
tests enumerate no population, key no sign, and
compute no corpus quantity.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/070-hunt-opening-signs-successor"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
ASSET_FREEZE = (
    REPO / "specs/069-hunt-asset-a/asset-a/asset-a-freeze.json"
)
ASSET_CSV = (
    REPO / "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv"
)
INTAKE = REPO / "docs/decisions/2026-10-22-shakti-corpus-intake-record.md"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

ASSET_SHA256 = (
    "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
)
CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
REGISTRY_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
CROSSWALK_SHA256 = (
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
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
    assert definition["experiment_id"] == "spec070-hunt-opening-signs-successor"
    assert definition["register"]["claims"] == 13
    assert definition["register"]["register_version"] == "0.9-frozen-candidate"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "0.845" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase 433"
    assert "805/2,267" in design["battery"]
    assert "documented + corroborated" in design["populations"]
    assert "DD-049-3" in design["precedence"]
    assert "DD-070-9" in design["keying"]
    assert "DD-070-11" in design["disposition"]
    assert "POPULATION NOT KEYED" in design["disposition"]
    assert design["outcomes"] == [
        "SUPPORTED",
        "NOT SUPPORTED",
        "INCONCLUSIVE",
        "ASSET NOT FROZEN",
        "ASSET PIN MISMATCH",
        "SHAKTI INTAKE NOT REPRODUCED",
        "POPULATION NOT KEYED",
        "INVALID",
    ]
    assert "DD-070-12" in design["osf"]
    assert "Phase 433" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["asset_a"]["sha256"] == ASSET_SHA256
    assert inputs["asset_a"]["per_kind_counts"]["animal"] == 20
    assert inputs["asset_a"]["per_kind_counts"]["contested"] == 0
    assert inputs["shakti_corpus"]["corpus_sha256"] == CORPUS_SHA256
    assert inputs["shakti_corpus"]["row_grades_sha256"] == GRADES_SHA256
    assert inputs["canonical_registry"]["sha256"] == REGISTRY_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "6a981188" in inputs["pin_verification"]


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.9-frozen-candidate"
    claims = register["claims"]
    assert len(claims) == 13
    ids = [c["id"] for c in claims]
    assert ids == [f"F070-C{i:02d}" for i in range(1, 14)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert ASSET_SHA256 in by_id["F070-C05"]["boundary"]
    assert "DD-070-9" in by_id["F070-C08"]["boundary"]
    assert "DD-070-11" in by_id["F070-C08"]["boundary"]
    assert "DD-070-10" in by_id["F070-C11"]["boundary"]


def test_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase in ("after_specify", "after_plan", "after_tasks"):
        matches = sorted(aee_dir.glob(f"aee-{phase}-*.json"))
        assert len(matches) == 1, phase
        artifact = json.loads(matches[0].read_text(encoding="utf-8"))
        assert artifact["phase"] == phase
        assert artifact["outcome"] == "pass"
        failures = [
            f for claim in artifact["claims"] for f in claim["failures"]
        ]
        assert failures == []
        scores = artifact["scores"]
        assert min(s["propagated_score"] for s in scores.values()) >= 0.70
        ev = sorted(aee_dir.glob(f"evaluator-aee-{phase}-*.json"))
        assert len(ev) == 1, phase


def test_input_pins_recompute():
    assert _sha(ASSET_CSV) == ASSET_SHA256
    asset_freeze = json.loads(ASSET_FREEZE.read_text(encoding="utf-8"))
    assert asset_freeze["sha256"] == ASSET_SHA256
    assert asset_freeze["per_kind_counts"]["animal"] == 20
    assert asset_freeze["per_kind_counts"]["sky_cycle"] == 0
    assert _sha(REGISTRY) == REGISTRY_SHA256
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    intake_text = INTAKE.read_text(encoding="utf-8")
    assert CORPUS_SHA256 in intake_text
    assert GRADES_SHA256 in intake_text
