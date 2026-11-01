"""Spec 075 freeze fences (depicted-kind endings atlas).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
design exactly - the atlas's own claim family (not
Spec 071's, not Hunt's), the documented-lineage
population reproduced at 3,045 / 557 / 550, the
two-leg keying route adopted from DD-074-8
(DD-075-5), the comparison class excluding the
unidentified signs (design R8, DD-075-4), the
floors of 20 signs / 30 occurrences, the per-kind
verdict bands with no pooled verdict, the celestial
arm pre-registered EMPTY, the outcome classes, the
OSF filing, and Phase 441; (3) the governed claim
register is the frozen register (13 claims, drafted
directly in the recovered 0.7-draft form,
integrity-clean) and the three freeze-hook
artifacts record the pass as it ran: 22 findings
per artifact - the 13 FR-2.3 draft caps plus the 9
named advisory challenges (7 irreducibility, 2
counterexample), zero findings of contradiction,
independence, ambiguity, or evidence-resolution
kind, no claim below the 0.70 threshold (minimum
propagated 0.8695); (4) the cited records still
carry the facts the design rests on - Asset A v2's
and Registry v2's digests, row counts, per-kind
and dispute counts in Spec 073's executed record
and recomputed from the canonical CSVs, the intake
record's Shakti pins, the registry v1, crosswalk
and anchors pins recomputing in the tree, and the
keying surface fact the route rests on: the
combined Wells map over Registry v2 carries 708
distinct ids with zero ambiguous. The corpus
itself is restricted-local and never in git; its
pins are asserted against the intake record's
text, and its population figures are gate 0.4's
to reproduce at an execution. These tests run no
arm, compute no final-position quantity, and
measure no test quantity.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/075-depicted-kind-endings-atlas"
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
        == "spec075-depicted-kind-endings-atlas"
    )
    assert definition["register"]["claims"] == 13
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "aee 1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.8695" in definition["register"]["aee_hook_pass"]
    assert "DD-075-6" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase 441"
    assert "3,045" in design["populations"]
    assert "5,131" in design["populations"]
    assert "EMPTY" in design["classes"]
    assert "token 999" in design["classes"]
    assert "DD-074-8" in design["keying"]
    assert "POPULATION NOT KEYED" in design["keying"]
    assert "20" in design["floors"] and "30" in design["floors"]
    assert "no pooled depicted-kinds verdict" in design["verdicts"]
    assert "S2" in design["sensitivities"]
    assert design["outcomes"] == [
        "SUPPORTED",
        "NOT SUPPORTED",
        "INCONCLUSIVE",
        "TOO THIN",
        "ASSET NOT FROZEN",
        "ASSET PIN MISMATCH",
        "SHAKTI INTAKE NOT REPRODUCED",
        "POPULATION NOT REPRODUCED",
        "POPULATION NOT KEYED",
        "INVALID",
        "NOT-RUN",
    ]
    assert "osf-spec-registration.md" in design["osf"]
    assert "Phase 441" in design["execution_gate"]
    assert "replay/drift gate" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["asset_a_v2"]["sha256"] == ASSET_V2_SHA256
    assert inputs["asset_a_v2"]["rows"] == 552
    assert inputs["asset_a_v2"]["per_kind_counts"]["animal"] == 30
    assert inputs["asset_a_v2"]["per_kind_counts"]["sky_cycle"] == 0
    assert inputs["asset_a_v2"]["dispute_status_counts"]["borderline"] == 4
    assert inputs["asset_a_v2"]["dispute_status_counts"]["contested"] == 0
    assert inputs["registry_v2"]["sha256"] == REGISTRY_V2_SHA256
    assert inputs["registry_v2"]["rows"] == 1013
    assert inputs["shakti_corpus"]["corpus_sha256"] == CORPUS_SHA256
    assert inputs["shakti_corpus"]["row_grades_sha256"] == GRADES_SHA256
    assert inputs["shakti_corpus"]["grades"]["documented-lineage"] == 3212
    pop = inputs["shakti_corpus"]["population"]
    assert pop["primary_rows"] == 3045
    assert pop["distinct_signs"] == 557
    assert pop["signs_in_sequences_ge2"] == 550
    assert pop["corroborated_rows"] == 5131
    assert pop["token_999_primary_rows"] == 2
    assert inputs["canonical_registry_v1"]["sha256"] == REGISTRY_V1_SHA256
    assert inputs["crosswalk"]["sha256"] == CROSSWALK_SHA256
    assert inputs["crosswalk"]["rows"] == 205
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "379a9fc3" in inputs["pin_verification"]


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.7-draft"
    claims = register["claims"]
    assert len(claims) == 13
    ids = [c["id"] for c in claims]
    assert ids == [f"F075-C{i:02d}" for i in range(1, 14)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert ASSET_V2_SHA256 in by_id["F075-C05"]["boundary"]
    assert REGISTRY_V2_SHA256 in by_id["F075-C05"]["boundary"]
    assert "icit_wells" in by_id["F075-C08"]["boundary"]
    assert "DD-074-8" in by_id["F075-C08"]["boundary"]
    assert "POPULATION NOT KEYED" in by_id["F075-C08"]["boundary"]
    assert "999" in by_id["F075-C08"]["boundary"]
    assert "1.5" in by_id["F075-C11"]["boundary"]
    assert "UNTESTED" in by_id["F075-C02"]["boundary"]


FREEZE_STAMPS = [
    "20261025T161923Z",
    "20261025T161923Z",
    "20261025T161923Z",
]

CHALLENGE_IDS = {
    "AEE-F075-C06-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C07-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C08-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C09-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C09-COUNTEREXAMPLE-CHALLENGE",
    "AEE-F075-C10-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C12-IRREDUCIBILITY-CHALLENGE",
    "AEE-F075-C12-COUNTEREXAMPLE-CHALLENGE",
    "AEE-F075-C13-IRREDUCIBILITY-CHALLENGE",
}

FORBIDDEN_CATEGORIES = {
    "contradiction",
    "independence_unmodeled",
    "ambiguous_requirement",
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
        assert not [
            f for f in failures if f["category"] in FORBIDDEN_CATEGORIES
        ], phase
        non_cap = [f for f in failures if f["category"] != "draft_cap"]
        assert {f["id"] for f in non_cap} == CHALLENGE_IDS, phase
        assert all(f["id"].endswith("-CHALLENGE") for f in non_cap), phase
        caps = [f for f in failures if f["category"] == "draft_cap"]
        assert len(caps) == 13, phase
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
        "unidentified": 211,
    }
    assert {k: per_kind.get(k, 0) for k in expected_kinds} == expected_kinds
    assert set(per_kind) <= set(expected_kinds)
    disputes = Counter(r["dispute_status"] for r in asset_rows)
    assert disputes.get("borderline", 0) == 4
    assert disputes.get("contested", 0) == 0
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
    with REGISTRY_V1.open(encoding="utf-8") as fh:
        assert len(list(csv.DictReader(fh))) == 803
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    with CROSSWALK.open(encoding="utf-8") as fh:
        assert len(list(csv.DictReader(fh))) == 205
    assert _sha(ANCHORS) == ANCHORS_SHA256
    intake_text = INTAKE.read_text(encoding="utf-8")
    assert CORPUS_SHA256 in intake_text
    assert GRADES_SHA256 in intake_text
    # The keying surface fact the two-leg route rests on,
    # recomputed over Registry v2 (the Spec 074 test's fact,
    # unchanged surface): leg 1 the parpola_1982 rows' wells_ids;
    # leg 2 the icit_wells rows, whose sign_id is the Wells id
    # itself; the combined map is unambiguous.
    asset_keys = {r["sign_key"] for r in asset_rows}
    assert len(asset_keys) == 552
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
