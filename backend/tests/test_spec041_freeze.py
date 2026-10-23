"""Spec 041 freeze fences (site x local-label period mapping).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the carried DD-039-3 evidence
standard (published determinations only, venue and
locator test, verification bar), the four-code value
vocabulary, the five enumerated unassigned reasons,
the step-0 gate set, the freeze rulings (DD-041-10
no single sensitivity label; DD-041-11 scope (a);
DD-041-12 OSF filed at the freeze; DD-041-13
reserved), Phase-435, and the unsatisfied execution
gate; (3) the governed claim register is the frozen
register (15 claims, integrity-clean, recovered to
0.8-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-041-15 reading (zero correctness failure modes;
only FR-2.3 draft-cap records; no claim below the
0.70 threshold); (4) the cited records still carry
the facts the design rests on (the anchors pin at
its refreshed value; the Phase-139 covariates pin;
the Phase-139 census tables; Spec 040's closure
record of conditions 2 and 4 FAILED and its
section 3 gate statement; DD-039-3's venue test).
These tests construct no cell, compute no census,
and change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/041-site-local-label-period-mapping"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
COVARIATES = (
    REPO / "data/evidence_integration"
    / "phase139_harmonized_covariates.json"
)
PHASE139_REPORT = REPO / "reports/phase139_report.md"
SPEC040_OUTCOME = (
    REPO / "specs/040-d25-g1-chronology-controlled/outcome.md"
)
SPEC039_ADJUDICATION = (
    REPO / "specs/039-gazetteer-period-assignment/adjudication.md"
)

ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
COVARIATES_SHA256 = (
    "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
)
LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
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
        "spec041-site-local-label-period-mapping"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    assert "DD-041-15" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-435"
    # The carried evidence standard, not softened.
    std = design["evidence_standard"]
    assert "published period determinations" in std["source"]
    assert "locator" in std["venue_locator_test"]
    assert "never grounds a cell" in std["verification_bar"]
    assert "chron_band" in " ".join(std["forbidden"])
    # The frozen schema.
    cell = design["cell_schema"]
    assert cell["values"] == ["EARLY", "MATURE", "LATE", "UNASSIGNED"]
    assert cell["statuses"] == ["MAPPED", "CONTESTED", "UNASSIGNED"]
    assert cell["unassigned_reasons"] == [
        "NO_PUBLISHED_DETERMINATION",
        "DETERMINATION_UNVERIFIED",
        "SPANS_COARSE_BOUNDARY",
        "NOT_IN_PUBLISHED_SCHEME",
        "LABEL_UNCERTAIN_IN_LAYER",
    ]
    # The freeze rulings.
    assert "DD-041-10" in cell["sensitivity_label"]
    assert "no single label frozen" in cell["sensitivity_label"]
    assert "DD-041-11" in design["construction"]["acquisition_scope"]
    assert "RESERVED" in design["row_derivation"]
    assert "DD-041-13" in design["row_derivation"]
    # The step-0 gates stand as a set.
    assert set(design["step0_gates"]) == {
        "G0.1", "G0.2", "G0.3", "G0.4", "G0.5", "G0.6",
    }
    # Inputs and their pins.
    inputs = definition["inputs"]
    assert inputs["layer"]["sha256"] == LAYER_SHA256
    assert inputs["layer"]["rows"] == 5679
    assert inputs["covariates"]["sha256"] == COVARIATES_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    pop = inputs["population"]
    assert pop["rows"] == 5410
    assert pop["label_coverage"] == {
        "period": 2266,
        "phase": 2638,
        "both": 1788,
        "either": 3116,
        "neither": 2294,
    }
    assert len(pop["eligible_sites"]) == 7
    # The execution gate is not satisfied by the freeze.
    assert "NOT satisfied" in design["execution_gate"]
    assert "no execution order" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F041-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["observed_at"] == "2026-10-21"
            assert item["independent_of"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_freeze_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase in ("after_specify", "after_plan", "after_tasks"):
        files = sorted(aee_dir.glob(f"evaluator-aee-{phase}-*.json"))
        assert len(files) == 1
        result = json.loads(files[0].read_text(encoding="utf-8"))
        assert "0 claim(s) below the 0.70" in result["summary"]
        assert all(
            "DRAFT-CAP" in f["id"] for f in result["findings"]
        )
        assert len(result["findings"]) == 15


def test_cited_records_carry_the_design_facts():
    # The anchors file at its refreshed pin.
    raw_bytes = ANCHORS.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == ANCHORS_SHA256
    assert len(raw_bytes) == 570344
    # The Phase-139 covariates at their pin.
    cov_bytes = COVARIATES.read_bytes()
    assert hashlib.sha256(cov_bytes).hexdigest() == COVARIATES_SHA256
    # The Phase-139 report carries the census the gates reproduce.
    report = PHASE139_REPORT.read_text(encoding="utf-8")
    for figure in ("2,266", "2,638", "1,788", "3,116"):
        assert figure in report
    # Spec 040's closure: conditions 2 and 4 failed, and
    # section 3 states what would satisfy the gate.
    outcome = SPEC040_OUTCOME.read_text(encoding="utf-8")
    assert "What would satisfy the gate" in outcome
    assert "NOT-YET-TESTABLE" in outcome
    # DD-039-3's venue-and-locator test stands in Spec 039's
    # adjudication.
    adj = SPEC039_ADJUDICATION.read_text(encoding="utf-8")
    assert "DD-039-3" in adj


FREEZE_STAMPS = [
    "20261022T230644Z",
    "20261022T230647Z",
    "20261022T230650Z",
]
