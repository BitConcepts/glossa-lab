"""Spec 042 freeze fences (Arm B object-type split, D-28).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - Phase-407, the step-0 gates
fail-closed, the per-stratum verdict rules carried
verbatim from Spec 028 (margin 0.01, seed 20261012),
the four-word headline pattern set, the stratum
floors (6 sites / 20 inscriptions), and the freeze
decisions (DD-042-6 OSF registration filed at the
freeze; DD-042-7 fresh synthetic calibration
declined, gate 0.5 exact reproduction standing as
the machinery check; DD-042-8 the gate-0.3/0.4
census standing as the margins instrument);
(3) the governed claim register is the frozen
register (15 claims, integrity-clean, recovered to
0.7-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-042-9 gate reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited records
still carry the facts the design rests on (the
six section 2 input pins re-derived from the
files themselves; the Phase-393 population flow;
Arm B's recorded primary quantities and its
drop-Harappa jackknife cell; Arm C's exploratory
dissimilarities; Spec 028's frozen verdict rules
as written in its spec). These tests compute no
stratum quantity, run no repertoire machinery,
and change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/042-arm-b-object-type-split"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
LAYER = REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
RESULTS393 = REPO / "reports/phase393_results.json"
SPEC028 = REPO / "specs/028-harappa-robustness"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

LAYER_SHA256 = (
    "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
)
RESULTS_SHA256 = (
    "0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607"
)
PIPELINE_SHA256 = (
    "6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e"
)
MARGINS_SHA256 = (
    "15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d"
)
FREEZE028_SHA256 = (
    "376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc"
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
    assert definition["experiment_id"] == (
        "spec042-arm-b-object-type-split"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-407"
    # The frozen verdict rules, carried verbatim from Spec 028.
    rules = design["verdict_rules"]
    assert rules["margin_adjusted_r2"] == 0.01
    assert rules["seed"] == 20261012
    assert "every leave-one-site-out median" in rules["supported"]
    assert "95%" in rules["contradicted"]
    assert "NOT ADJUDICATED" in rules["control_failure"]
    # The headline pattern set is exactly D-28's four words.
    assert design["headline_patterns"] == [
        "SPLIT",
        "UNIFORM-PASS",
        "UNIFORM-FAIL",
        "THIN",
    ]
    # The stratum floors (gate 0.4) and the THIN closure (DD-042-2).
    floors = design["stratum_floors"]
    assert floors["min_sites"] == 6
    assert floors["min_inscriptions_per_site"] == 20
    assert "neither stratum is computed" in floors["on_failure"]
    # The step-0 gates are fail-closed, in order.
    gates = design["step0_gates"]
    assert [g["id"] for g in gates] == ["0.1", "0.2", "0.3", "0.4", "0.5"]
    assert "INVALID" in gates[0]["failure_class"]
    assert "exactly" in gates[4]["check"]
    # The freeze decisions.
    dec = definition["decisions"]
    assert "DD-042-6" in dec["osf_registration"]
    assert "files its own OSF contract registration" in dec["osf_registration"]
    assert "DECLINED" in dec["synthetic_calibration"]
    assert "0.5" in dec["synthetic_calibration"]
    assert "census" in dec["margins_audit"]
    assert "CONFIRMED" in dec["dd_042_2"]
    assert "CONFIRMED" in dec["dd_042_3"]
    # Inputs: every section 2 pin, as re-derived at the freeze.
    inputs = definition["inputs"]
    assert inputs["corpus_layer"]["sha256"] == LAYER_SHA256
    assert inputs["phase393_results"]["sha256"] == RESULTS_SHA256
    assert inputs["pipeline393"]["sha256"] == PIPELINE_SHA256
    assert inputs["spec028_margins_audit"]["sha256"] == MARGINS_SHA256
    assert inputs["spec028_freeze"]["sha256"] == FREEZE028_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["population"]["analysis_records"] == 3030
    assert inputs["population"]["analysis_sites"] == 6
    # The execution gate: frozen, not executed, by this act.
    assert "Phase-407" in design["execution_gate"]
    assert "no stratum quantity was computed" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F042-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["observed_at"] == "2026-10-21"
    report = check_dependency_integrity(
        [Claim.from_dict(c, strict=False) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # Every section 2 pin re-derived from the file itself.
    assert _sha(LAYER) == LAYER_SHA256
    assert _sha(RESULTS393) == RESULTS_SHA256
    assert _sha(SPEC028 / "pipeline393.py") == PIPELINE_SHA256
    assert _sha(SPEC028 / "margins-audit.json") == MARGINS_SHA256
    assert _sha(SPEC028 / "freeze.json") == FREEZE028_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    # The corpus layer holds the frozen flow's 5,679 records
    # (5,680 lines: one header row plus the records).
    lines = [
        line
        for line in LAYER.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert lines[0].startswith("id,")
    assert len(lines) == 5680
    # The Phase-393 record: flow, Arm B primary, jackknife, Arm C.
    res = json.loads(RESULTS393.read_text(encoding="utf-8"))
    assert res["verdicts"]["arm_b"] == "INCONCLUSIVE"
    flow = res["population"]["flow"]
    assert flow["layer_records"] == 5679
    assert flow["after_dedup_kept"] == 4531
    assert flow["provenanced"] == 4505
    assert flow["seal_tab"] == 3605
    assert flow["eligible_primary"] == 3144
    assert res["population"]["analysis"] == 3030
    arm_b = res["arm_b"]
    assert arm_b["records"] == 3030
    primary = arm_b["primary"]
    assert round(primary["median_adj_r2"], 7) == 0.0223721
    assert [round(v, 7) for v in primary["adj_r2_interval_95"]] == [
        0.0122174,
        0.0333271,
    ]
    assert round(primary["share_draws_rejecting"], 4) == 0.9548
    harappa = arm_b["loso"]["Harappa"]
    loso_median = (
        harappa["median_adj_r2"]
        if "median_adj_r2" in harappa
        else harappa["primary"]["median_adj_r2"]
    )
    assert round(loso_median, 7) == 0.0066068
    assert arm_b["controls_pass"] is True
    within = res["arm_c"]["within_type"]
    assert round(within["TAB"], 7) == 0.4952733
    assert round(within["SEAL"], 7) == 0.1113521
    assert res["provenance"]["seed"] == 20261012
    assert res["provenance"]["freeze_digest"] == (
        "619ab0c30048b934a14f2f2e7583a1a2e93c25c0599488f97165c285cd38bb61"
    )
    # Spec 028's frozen rules as written in its spec.
    spec028 = " ".join(
        (SPEC028 / "spec.md").read_text(encoding="utf-8").split()
    )
    assert "SUPPORTED" in spec028
    assert "0.01" in spec028
    assert "20261012" in spec028


FREEZE_STAMPS = [
    "20261021T095618Z",
    "20261021T095624Z",
    "20261021T095628Z",
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
