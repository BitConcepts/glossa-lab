"""Spec 060 freeze fences (F2 margin curve + shared population).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the settled F2/F3 record, the
D-20 correction (Spec 034 finished, never a
pending next step), the Phase-384 v2 estimator
identity with gate 0.3 as its check (DD-060-14),
the fixed margin grid labelled sensitivity, the
shared-population construction with the SEAL
reading confirmed (DD-060-12: the Holdat layer
carries no object-type field, its type a
constant), the period stated-unavailability
wording confirmed with no imported assignment
(DD-060-13), the venue ruling (DD-060-15), the
total arm-2 outcome mapping with TOO THIN
closing arm 2 only (DD-060-11), the step-0
gates, and Phase-422; (3) the governed claim
register is the frozen register (15 claims,
integrity-clean, recovered to 0.7-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-060-17 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (every spec section 3 pin,
verified at the freeze by two independent
routes; the Phase-137 populations, site lists,
type and period facts; the Phase-384 v2
intervals; the freeze-v2 sources record matching
the estimator and contract pins; Spec 034's
finished attribution and its slice). The two
held layers are not repository files: their
pins are asserted as definition constants (the
values the pinned Phase-137 results record),
and the results record's own input entries are
asserted on the live file. These tests compute
no margin-curve cell, no shared-population
quantity, and not the gate-0.4 census.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/060-f2-margin-curve"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
PHASE137_RESULTS = REPO / "reports/phase137_results.json"
PHASE137_SCRIPT = REPO / "backend/scripts/phase137_site_repertoire.py"
PHASE384_RESULTS = REPO / "reports/phase384_results.json"
PHASE384_ESTIMATOR = (
    REPO / "backend/scripts/phase384_stage2_margins_v2.py"
)
PHASE384_CONTRACT = (
    REPO / "specs/026-rcph-framework-transfer/reruns/"
    "phase384-contract-v2.md"
)
PHASE384_FREEZE = (
    REPO / "specs/026-rcph-framework-transfer/reruns/"
    "phase384-freeze-v2.json"
)
SPEC034_OUTCOME = (
    REPO / "specs/034-matched-object-attribution/outcome.md"
)
SPEC024_SPEC = REPO / "specs/024-evidence-integration/spec.md"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

PHASE137_RESULTS_SHA256 = (
    "18f86f45892526b947a4a7447201be9d69584ec96d33a1d18139309b9dc2a7a1"
)
PHASE137_SCRIPT_SHA256 = (
    "e00dacf4df8f52871b482e36ca0a37f66503c5f1b107ee835ac99fa21dfc8c86"
)
PHASE384_RESULTS_SHA256 = (
    "dda6092d9f4d368869a6e3a590948dfa97d02c5db50bf75868d6e055f0896aad"
)
PHASE384_ESTIMATOR_SHA256 = (
    "3313394e6a716898cdfd440a46333ebd2b9136b77306413ed1514eab322a72a5"
)
PHASE384_CONTRACT_SHA256 = (
    "f0a67bd766ae28a33edc33553613bf9c50cc933df1bfbe2b5e1192d6571bbc75"
)
PHASE384_FREEZE_SHA256 = (
    "5749c6b89ac26be6333e0c20457bc320ca624c15f5ca65e689c107aa12b7b8e9"
)
SPEC034_OUTCOME_SHA256 = (
    "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175"
)
SPEC024_SPEC_SHA256 = (
    "a817f698fd5f2dd0a2d324d580d25cba41fc989762b20e0b77a4144a02d3ee25"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
HOLDAT_LAYER_SHA256 = (
    "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e"
)
ICIT_LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
)
PHASE384_FREEZE_DIGEST = (
    "4e6c78bc917c96a3eeb80fc09e3345073dbaf38e809171f1f59041778784b28e"
)
SPEC034_FREEZE_DIGEST = (
    "696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a"
)
SHARED_SITES = [
    "Chanhu-daro",
    "Dholavira",
    "Harappa",
    "Kalibangan",
    "Lothal",
    "Mohenjo-daro",
]
F2_BASIC = [0.058939204306206666, 0.0777941604081594]
F2_PERCENTILE = [0.15300258989494483, 0.17185754599689756]
F2_MEDIAN = 0.16180470665653984
F3_BASIC = [0.18229651053139323, 0.21036863506165235]

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == "spec060-f2-margin-curve"
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-422"
    claim = design["claim_under_test"]
    assert claim["id"] == "STUDY-SPEC-024/F2-HOLDAT"
    assert "CONTRADICTED" in claim["record"]
    assert "0.058939204306206666" in claim["record"]
    # The falsifier is stated under the corrected hand-off:
    # Spec 034 is finished, and no successor is implied.
    falsifier = design["falsifier"]
    assert "COMPOSITION DOES NOT" in falsifier
    assert "ATTRIBUTED TO COMPOSITION" in falsifier
    assert "169 matched objects" in falsifier
    assert "Mohenjo-daro seals" in falsifier
    assert "no successor study" in falsifier
    # Arm 1: the fixed grid, the frozen rule, the sensitivity label.
    arm1 = design["arm1_margin_curve"]
    for margin in ("0.05", "0.075", "0.10", "0.125", "0.15"):
        assert margin in arm1
    assert "CONTRADICTED AT m" in arm1
    assert "SUPPORTED AT m" in arm1
    assert "STRADDLES m" in arm1
    assert "sensitivity" in arm1
    assert "B = 9,999" in arm1
    assert "seed 20261012" in arm1
    # The shared population: SEAL confirmed; signs never pooled.
    shared = design["shared_population"]
    assert "DD-060-12" in shared["type_ruling"]
    assert "CONFIRMED" in shared["type_ruling"]
    assert "carries no object-type field" in shared["type_ruling"]
    assert "SEAL" in shared["type_ruling"]
    for site in SHARED_SITES:
        assert site in shared["sites"]
    assert "never pooled, mapped, or harmonised" in shared["measurement"]
    # Period: stated unavailability confirmed; nothing imported.
    period = design["period_ruling"]
    assert "DD-060-13" in period
    assert "CONFIRMED" in period
    assert "PERIOD MIX NOT DESCRIBED FOR THIS LAYER" in period
    assert "Spec 041-style" in period
    assert "never treated as controlled" in period
    # Calibration and venue rulings.
    assert "DD-060-14" in design["calibration_ruling"]
    assert "gate 0.3" in design["calibration_ruling"]
    assert "no fresh synthetic calibration" in design["calibration_ruling"]
    assert "DD-060-15" in design["venue_ruling"]
    assert "default paths" in design["venue_ruling"]
    # Outcomes and TOO THIN's scope: arm 2 only.
    assert design["outcomes_arm2"] == [
        "COMPOSITION EXPLAINS THE GAP",
        "COMPOSITION DOES NOT",
        "TOO THIN",
    ]
    assert "DD-060-11" in design["too_thin_ruling"]
    assert "arm 2 only" in design["too_thin_ruling"]
    assert "arm 1 is independent" in design["too_thin_ruling"]
    # Gates are total, ordered, and fail-closed as INVALID.
    gates = design["step0_gates"]
    assert "gate 0.1" in gates and "gate 0.4" in gates
    assert "INVALID" in gates
    assert "TOO THIN" in gates
    # What the freeze does not do, and the execution gate.
    assert "does not itself compute anything" in design["freeze_does_not"]
    assert "not the gate-0.4 census" in design["freeze_does_not"]
    assert "moves no verdict" in design["freeze_does_not"]
    assert "Not satisfied at the freeze" in design["execution_gate"]
    assert "approval" in design["execution_gate"]
    # Inputs: every section 3 pin, as verified two-route at the freeze.
    inputs = definition["inputs"]
    assert inputs["holdat_layer"]["sha256"] == HOLDAT_LAYER_SHA256
    assert inputs["icit_layer"]["sha256"] == ICIT_LAYER_SHA256
    assert inputs["phase137_results"]["sha256"] == PHASE137_RESULTS_SHA256
    assert inputs["phase137_machinery"]["sha256"] == PHASE137_SCRIPT_SHA256
    assert inputs["phase384_results"]["sha256"] == PHASE384_RESULTS_SHA256
    assert inputs["phase384_results"]["f2_basic_ci95"] == F2_BASIC
    assert inputs["phase384_results"]["f3_basic_ci95"] == F3_BASIC
    assert inputs["phase384_estimator"]["sha256"] == PHASE384_ESTIMATOR_SHA256
    assert inputs["phase384_estimator"]["freeze_v2_sources_match"] is True
    assert inputs["phase384_contract"]["sha256"] == PHASE384_CONTRACT_SHA256
    assert inputs["phase384_freeze_v2"]["sha256"] == PHASE384_FREEZE_SHA256
    assert (
        inputs["phase384_freeze_v2"]["recorded_digest"]
        == PHASE384_FREEZE_DIGEST
    )
    spec034 = inputs["spec034_outcome"]
    assert spec034["sha256"] == SPEC034_OUTCOME_SHA256
    assert spec034["verdict"] == "ATTRIBUTED TO COMPOSITION"
    assert spec034["matched_objects"] == 169
    assert spec034["median_distance"] == 0.025694
    assert spec034["freeze_digest"] == SPEC034_FREEZE_DIGEST
    assert inputs["spec024_spec"]["sha256"] == SPEC024_SPEC_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "two independent routes" in inputs["pin_verification"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F060-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # Phase-137 results: pin, populations, sites, type and
    # period facts, and the held layers' recorded input pins.
    p137_bytes = PHASE137_RESULTS.read_bytes()
    assert hashlib.sha256(p137_bytes).hexdigest() == PHASE137_RESULTS_SHA256
    p137 = json.loads(p137_bytes)
    assert p137["fields_used"]["holdat"] == [
        "letters",
        "position",
        "seal_id",
        "site",
    ]
    assert p137["fields_used"]["horus84"] == ["text", "site", "type"]
    assert "period" in p137["uncontrolled_confounders_statement"]
    assert "not available in these layers" in (
        p137["uncontrolled_confounders_statement"]
    )
    f2 = p137["layers"]["F2_holdat"]
    f3 = p137["layers"]["F3_icit_lineage"]
    assert f2["input"]["sha256"] == HOLDAT_LAYER_SHA256
    assert f3["input"]["sha256"] == ICIT_LAYER_SHA256
    assert f2["analysis_population"]["inscriptions"] == 1670
    assert f3["analysis_population"]["inscriptions"] == 5410
    assert f2["table_dimensions"] == [9, 98]
    assert f3["table_dimensions"] == [7, 187]
    assert abs(f2["observed_chi_square"] - 745.953) < 0.001
    assert abs(f3["observed_chi_square"] - 4966.362) < 0.001
    assert abs(f2["cramers_v_descriptive"] - 0.11539837515155221) < 1e-12
    assert abs(f3["cramers_v_descriptive"] - 0.2190084751289231) < 1e-12
    assert f2["p_value_raw"] == 0.7354
    assert "carries no object-type field" in f2["strata_definition"]
    assert "seal texts" in f2["strata_definition"]
    assert any(k.startswith("SEAL|") for k in f3["strata_counts"])
    shared = set(f2["eligible_sites"]) & set(f3["eligible_sites"])
    assert sorted(shared) == sorted(SHARED_SITES)
    # Phase-137 machinery: pin, loader fields, SEAL type class.
    script_bytes = PHASE137_SCRIPT.read_bytes()
    assert hashlib.sha256(script_bytes).hexdigest() == PHASE137_SCRIPT_SHA256
    script = script_bytes.decode("utf-8")
    assert "horus_type_class" in script
    assert '"SEAL", "TAB", "POT"' in script
    # Phase-384 results: pin and the recorded intervals exactly.
    p384_bytes = PHASE384_RESULTS.read_bytes()
    assert hashlib.sha256(p384_bytes).hexdigest() == PHASE384_RESULTS_SHA256
    p384 = json.loads(p384_bytes)
    assert p384["parameters"]["B_bootstrap"] == 9999
    assert p384["parameters"]["seed"] == 20261012
    assert p384["parameters"]["governing_interval"] == "basic bootstrap"
    m2 = p384["members"]["F2_holdat"]
    m3 = p384["members"]["F3_icit_lineage"]
    assert m2["basic_ci95"] == F2_BASIC
    assert m2["percentile_ci95"] == F2_PERCENTILE
    assert m2["bootstrap_median"] == F2_MEDIAN
    assert m3["basic_ci95"] == F3_BASIC
    assert m2["n_analysis_inscriptions"] == 1670
    assert m3["n_analysis_inscriptions"] == 5410
    # Estimator and contract: pins, and the freeze-v2 sources
    # record inside the pinned freeze-v2 file matches both.
    assert (
        hashlib.sha256(PHASE384_ESTIMATOR.read_bytes()).hexdigest()
        == PHASE384_ESTIMATOR_SHA256
    )
    estimator = PHASE384_ESTIMATOR.read_text(encoding="utf-8")
    assert "SEED = 20261012" in estimator
    assert "B_BOOT = 9999" in estimator
    assert (
        hashlib.sha256(PHASE384_CONTRACT.read_bytes()).hexdigest()
        == PHASE384_CONTRACT_SHA256
    )
    freeze_bytes = PHASE384_FREEZE.read_bytes()
    assert hashlib.sha256(freeze_bytes).hexdigest() == PHASE384_FREEZE_SHA256
    freeze384 = json.loads(freeze_bytes)
    assert freeze384["digest"] == PHASE384_FREEZE_DIGEST
    sources = freeze384["sources"]
    assert (
        sources["backend/scripts/phase384_stage2_margins_v2.py"]
        == PHASE384_ESTIMATOR_SHA256
    )
    assert (
        sources[
            "specs/026-rcph-framework-transfer/reruns/"
            "phase384-contract-v2.md"
        ]
        == PHASE384_CONTRACT_SHA256
    )
    # Spec 034's outcome: pin and the finished attribution's facts.
    outcome_bytes = SPEC034_OUTCOME.read_bytes()
    assert hashlib.sha256(outcome_bytes).hexdigest() == SPEC034_OUTCOME_SHA256
    outcome = outcome_bytes.decode("utf-8")
    assert "ATTRIBUTED TO COMPOSITION" in outcome
    assert SPEC034_FREEZE_DIGEST in outcome
    assert "0.025694" in outcome
    assert "0.040340" in outcome
    assert "all Mohenjo-daro" in outcome
    # Spec 024's specification and the anchors file: pins only.
    assert (
        hashlib.sha256(SPEC024_SPEC.read_bytes()).hexdigest()
        == SPEC024_SPEC_SHA256
    )
    assert (
        hashlib.sha256(ANCHORS.read_bytes()).hexdigest() == ANCHORS_SHA256
    )


FREEZE_STAMPS = [
    "20261021T115413Z",
    "20261021T115413Z",
    "20261021T115413Z",
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
