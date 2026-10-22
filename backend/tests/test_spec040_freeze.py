"""Spec 040 draft freeze fences (D-25: G1 chronology-controlled).

Pins: (1) the draft machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the design
constants exactly as drafted (the dependency gate
unsatisfied and fail-closed, the assignment
discipline, the margins gate's three arms, the
Phase-140 permutation and Phase-385 interval
constants, the V = 0.10 margin, and the three
outcome mappings); (3) the governed claim register
is the draft register (15 claims, integrity-clean,
hooks not run - the hooks are a freeze gate);
(4) the cited in-repo records still carry the
facts the design rests on (the Phase-140 and
Phase-385 quantities, the spine and covariate
pins, the Spec 025 rider, the Spec 027 section
6.2 assignment field). These tests join no label,
compute no margin, and calculate no repertoire
quantity.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/040-d25-g1-chronology-controlled"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
R140 = REPO / "reports/phase140_results.json"
R385 = REPO / "reports/phase385_results.json"
SPINE = REPO / "data/movement/chronology_rows_phase394.jsonl"
COVARIATES = (
    REPO
    / "data/evidence_integration/phase139_harmonized_covariates.json"
)
SPEC025 = REPO / "specs/025-stage2-controlled-followup/spec.md"
SPEC027 = REPO / "specs/027-movement-culture-language/spec.md"
SPEC030_OUTCOME = (
    REPO / "specs/030-q6-chronology-spine-extension/outcome.md"
)

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
        "spec040-d25-g1-chronology-controlled"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.5-draft"
    assert "NOT RUN" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["claim_under_test"] == "STUDY-SPEC-025/G1"
    # The dependency gate is unsatisfied at draft
    # and fails closed.
    gate = design["dependency_gate"]
    assert "NOT SATISFIED" in gate["state_at_draft"]
    assert "NOT-YET-TESTABLE" in gate["failure_state"]
    assert "PENDING" in gate["spec039_artifact"]["sha256"]
    assert "published period determinations only" in (
        " ".join(gate["requires"]))
    # The assignment discipline.
    assignment = design["period_assignment"]
    assert assignment["labels"] == ["EARLY", "MATURE", "LATE"]
    assert "UNASSIGNED" in assignment["primary_rule"]
    assert "site-level occupation label inheritance" in (
        assignment["forbidden_placements"])
    # The margins gate's three arms.
    margins = design["margins_gate"]
    assert margins["sites_per_period_min"] == 5
    assert margins["periods_required"] == ["EARLY", "MATURE", "LATE"]
    assert margins["unassigned_share_max"] == 0.4
    assert margins["permutable_min"] == 1000
    assert "NOT-YET-TESTABLE" in margins["failure_state"]
    # The primary test's carried constants.
    primary = design["primary_test"]
    assert primary["permutation"]["B"] == 9999
    assert primary["permutation"]["seed"] == 20261009
    assert primary["interval"]["B"] == 4999
    assert primary["interval"]["seed"] == 20261012
    assert "basic bootstrap" in primary["interval"]["governing"]
    assert primary["margin_v"] == 0.1
    assert "composition_stratum | preservation_class" in (
        primary["strata"])
    # The three outcome mappings, none softened.
    rules = design["decision_rules"]
    assert "SUPPORTED - CHRONOLOGY CONTROLLED" in rules["supported"]
    assert "WEAKENED - RIDER CONFIRMED AS MATERIAL" in (
        rules["weakened"])
    assert "period-confounded" in rules["weakened"]
    assert "CONTRADICTED AT THE DECLARED MARGIN" in (
        rules["contradicted"])
    assert "no freeze order" in design["execution_gate"]
    # The pinned inputs.
    inputs = definition["inputs"]
    assert inputs["layer"]["sha256"] == (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
    )
    assert inputs["layer"]["population_rows"] == 5410
    assert inputs["covariates"]["sha256"] == (
        "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
    )
    assert inputs["spine"]["sha256"] == (
        "9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93"
    )
    assert inputs["spine"]["rows"] == 205
    assert inputs["recorded_results"]["phase385"][
        "governing_basic_ci95"] == [
            0.1837750116366994, 0.2102434435947284]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.5-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F040-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    r140 = json.loads(R140.read_text(encoding="utf-8"))
    assert r140["population"]["inscriptions"] == 5410
    assert r140["g1_primary"]["observed_chi_square"] == (
        4966.362228365138)
    assert r140["g1_primary"]["permutation"]["p_value_raw"] == 0.0001
    assert "Chronology is NOT controlled" in r140["headline_rider"]
    r385 = json.loads(R385.read_text(encoding="utf-8"))
    assert r385["parameters"]["margin_v"] == 0.1
    assert r385["parameters"]["B_bootstrap"] == 4999
    assert r385["parameters"]["seed"] == 20261012
    assert r385["g1_primary"]["bootstrap_v_intervals"][
        "basic_ci95"] == [
            0.1837750116366994, 0.2102434435947284]
    # The spine and covariate pins, as pinned.
    assert hashlib.sha256(SPINE.read_bytes()).hexdigest() == (
        "9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93"
    )
    spine_lines = [
        ln for ln in SPINE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert len(spine_lines) == 205
    assert hashlib.sha256(COVARIATES.read_bytes()).hexdigest() == (
        "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
    )
    covariates = json.loads(COVARIATES.read_text(encoding="utf-8"))
    assert len(covariates) == 5410
    # The rider and the assignment field the
    # dependency rests on.
    spec025 = SPEC025.read_text(encoding="utf-8")
    assert "NOT controlled" in spec025
    f140 = (
        REPO / "specs/025-stage2-controlled-followup/phase140-freeze.md"
    ).read_text(encoding="utf-8")
    assert "chronology is NOT controlled in the\n  primary test" in (
        f140.replace("**", ""))
    spec027 = SPEC027.read_text(encoding="utf-8")
    assert "program_period_assignment" in spec027
    outcome030 = SPEC030_OUTCOME.read_text(encoding="utf-8")
    assert "NOT-YET-TESTABLE" in outcome030
    assert "205 rows" in outcome030
