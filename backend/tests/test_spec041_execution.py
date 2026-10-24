"""Spec 041 / Phase-435 execution acceptance tests.

Pins the executed act's own record: the frozen step-0
gates all passed; the committed census's headline
counts are the frozen ones; the artifact's cell set is
provably the census set; the artifact obeys the frozen
schema discipline; the four §8 derivations account for
the whole population and respect the 57.6% ceiling; the
artifact's SHA-256 pin in the outcome record matches the
file; and no G1 quantity was computed (DD-041 / §5.5
fence; Spec 040's closure is not amended by this act).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports" / \
    "phase435_results.json"
CENSUS = REPO_ROOT / "specs" / \
    "041-site-local-label-period-mapping" / \
    "step0-census.json"
ARTIFACT = REPO_ROOT / "data" / "evidence_integration" / \
    "site_period_mapping.jsonl"
META = REPO_ROOT / "data" / "evidence_integration" / \
    "site_period_mapping_meta.json"
OUTCOME = REPO_ROOT / "specs" / \
    "041-site-local-label-period-mapping" / "outcome.md"

LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef")
FREEZE_DIGEST = (
    "fe6188864d5ff497fed5e3e89456d0499987c2c"
    "bc8ada5997920e864360dfdc7")
POPULATION_ROWS = 5410
CENSUS_CELLS = 78
CEILING = 3116
EXPECTED_MARGINS = {"period": 2266, "phase": 2638,
                    "both": 1788, "union": 3116,
                    "neither": 2294}
KEY_ORDER = ["site", "field", "local_label",
             "coarse_period", "status", "determinations",
             "contested", "sensitivity_label",
             "unassigned_reason", "attested_rows"]
VALUES = {"EARLY", "MATURE", "LATE", "UNASSIGNED"}
REASONS = {"NO_PUBLISHED_DETERMINATION",
           "DETERMINATION_UNVERIFIED",
           "SPANS_COARSE_BOUNDARY",
           "NOT_IN_PUBLISHED_SCHEME",
           "LABEL_UNCERTAIN_IN_LAYER"}


@pytest.fixture(scope="module")
def results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def artifact() -> list[dict]:
    return [json.loads(line) for line in
            ARTIFACT.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def test_step0_gates_all_pass(results):
    assert results["step0_verdict"] == "STEP 0 PASSED"
    gates = {g["gate"]: g["verdict"]
             for g in results["gates"]}
    assert set(gates) == {"G0.1", "G0.2", "G0.3", "G0.4",
                          "G0.5", "G0.6"}
    assert all(v == "PASS" for v in gates.values())


def test_no_g1_quantity_computed(results):
    assert results["g1_quantity_computed"] is False


def test_census_headline_reproduced(results):
    assert results["population_rows"] == POPULATION_ROWS
    assert results["census_headline"] == EXPECTED_MARGINS
    assert results["census_cells"] == CENSUS_CELLS
    committed = json.loads(
        CENSUS.read_text(encoding="utf-8"))
    assert committed["margins"] == EXPECTED_MARGINS
    assert len(committed["cells"]) == CENSUS_CELLS


def test_artifact_cell_set_equals_census(artifact):
    committed = json.loads(
        CENSUS.read_text(encoding="utf-8"))
    census_set = {(c["site"], c["field"], c["local_label"])
                  for c in committed["cells"]}
    artifact_set = {(r["site"], r["field"], r["local_label"])
                    for r in artifact}
    assert artifact_set == census_set
    assert len(artifact) == CENSUS_CELLS
    census_rows = {(c["site"], c["field"], c["local_label"]):
                   c["rows"] for c in committed["cells"]}
    for r in artifact:
        key = (r["site"], r["field"], r["local_label"])
        assert r["attested_rows"] == census_rows[key]


def test_artifact_schema_discipline(artifact):
    for r in artifact:
        assert list(r.keys()) == KEY_ORDER
        assert r["coarse_period"] in VALUES
        assert r["status"] in {"MAPPED", "CONTESTED",
                               "UNASSIGNED"}
        # DD-041-10: no sensitivity label on any cell.
        assert r["sensitivity_label"] is None
        if r["status"] == "MAPPED":
            assert r["coarse_period"] != "UNASSIGNED"
            assert len(r["determinations"]) == 1
            assert r["contested"] is False
            assert r["unassigned_reason"] is None
        elif r["status"] == "CONTESTED":
            assert r["coarse_period"] == "UNASSIGNED"
            assert r["contested"] is True
            assert len(r["determinations"]) >= 2
        else:
            assert r["coarse_period"] == "UNASSIGNED"
            assert r["determinations"] == []
            assert r["unassigned_reason"] in REASONS
            assert r["contested"] is False
        for d in r["determinations"]:
            assert d["verification"] in {
                "OWN_TEXT", "PAGINATED_RESTATEMENT"}
            assert d["citation"] and d["locator"] \
                and d["mapping_rule"]
            assert set(d.keys()) == {"citation", "locator",
                "mapping_rule", "verification"}


def test_derivations_account_for_population(results):
    for name in ("A1", "A2", "B", "C"):
        d = results["derivations"][name]
        assert d["placed_total"] + d["unplaced_total"] \
            == POPULATION_ROWS
        assert d["placed_total"] <= CEILING
        assert sum(d["unplaced_by_cause"].values()) == \
            d["unplaced_total"]
        assert sum(d["placed_by_period"].values()) == \
            d["placed_total"]


def test_meta_consistency(artifact):
    meta = json.loads(META.read_text(encoding="utf-8"))
    assert meta["layer_sha256"] == LAYER_SHA256
    assert meta["freeze_digest"] == FREEZE_DIGEST
    counts = {}
    for r in artifact:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    assert meta["cells_by_status"] == counts
    assert meta["cells_total"] == CENSUS_CELLS


def test_artifact_pin_matches_outcome_record():
    text = OUTCOME.read_text(encoding="utf-8")
    m = re.search(r"Artifact SHA-256: `([0-9a-f]{64})`",
                  text)
    assert m, "outcome record carries no artifact pin"
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
    assert m.group(1) == digest
