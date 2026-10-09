"""Tests for Phase-130 (spec 021) independent-data intake pack.

Covers: intake schema v1 <-> validator agreement; the
validator's structured verdicts incl. the hard license gate
(a license-missing dataset is a reject, not a warning),
sign-list declaration and duplicate-ID rejects, and
warning-only absences; the shared dedup module
(glossa_lab.dedup) reproducing the Phase-119 harness's
behaviour exactly — on the harness's own fixtures and, where
the converted layer file is present, on the spec 018
Appendix A.6 measured numbers (4,531 -> 2,446 kept, 46.02%
cumulative removal); spec 018 section 4 evaluability-class
assignment; the structural dry-run-only separation (the
intake module binds no scoring name; an intake report
carries the section 8 label and no verdict statistic); the
synthetic fixture end-to-end through every runbook stage
(docs/INTAKE_RUNBOOK.md) incl. its deliberate duplicate
cluster; and H23 graph registration.

All fixture data is synthetic: invented signs (P901-P905)
and invented sites. No real corpus data is used.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import glossa_lab.dedup as dedup_module
import glossa_lab.intake as intake
import glossa_lab.pred_harness as harness
from glossa_lab.intake import (
    SCHEMA_VERSION, assign_evaluability, run_intake, validate_dataset,
)
from glossa_lab.pred_harness import (
    DRY_RUN_LABEL, SignMapper, adapt_converted_layer, build_sign_maps,
    load_sign_classes,
)

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "intake"
HARNESS_FIXTURES = (Path(__file__).resolve().parent
                    / "fixtures" / "pred_harness")
SCHEMA_FILE = REPO / "data" / "intake" / "intake_dataset_schema_v1.json"
INVENTORY = REPO / "data" / "crosswalks" / "sign_inventory.csv"
REGISTRY = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"

EXPECTED_FIXTURE_DEDUP = {"input": 7, "stage_a_removed": 1,
                          "stage_b_removed": 1, "stage_c_removed": 1,
                          "kept": 4}
EXPECTED_LAYER_DEDUP = {"input": 4531, "stage_a_removed": 1468,
                        "stage_b_removed": 370, "stage_c_removed": 247,
                        "kept": 2446}


@pytest.fixture(scope="module")
def fixture_dataset():
    return json.loads((FIXTURES / "synthetic_dataset.json").read_text("utf-8"))


@pytest.fixture(scope="module")
def classes():
    return load_sign_classes(INVENTORY)


@pytest.fixture(scope="module")
def mapper():
    return SignMapper(build_sign_maps(REGISTRY))


def _codes(verdict, kind="errors"):
    return {e["code"] for e in verdict[kind]}


# ------------------------------------------------------------ schema v1

def test_schema_file_agrees_with_validator():
    schema = json.loads(SCHEMA_FILE.read_text("utf-8"))
    assert schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    assert set(schema["required"]) == set(intake.DATASET_REQUIRED)
    assert (set(schema["properties"]["source_class"]["enum"])
            == set(harness.SOURCE_CLASSES))
    ins = schema["$defs"]["inscription"]
    assert set(ins["required"]) == set(intake.INSCRIPTION_REQUIRED)
    assert set(ins["properties"]["sign_list"]["enum"]) == set(intake.SIGN_LISTS)
    lineage = schema["properties"]["upstream_lineage"]
    assert set(lineage["required"]) == set(intake.LINEAGE_REQUIRED)
    prov = ins["properties"]["provenance"]
    assert set(prov["required"]) == set(intake.PROVENANCE_REQUIRED)


# ------------------------------------------------------------- validator

def test_validator_passes_fixture(fixture_dataset):
    v = validate_dataset(fixture_dataset)
    assert v["verdict"] == "pass", v
    assert v["errors"] == [] and v["warnings"] == []
    assert v["summary"]["inscriptions"] == 7
    assert v["summary"]["sign_lists"] == ["parpola_1982"]


def test_validator_license_missing_is_reject_not_warning():
    ds = json.loads(
        (FIXTURES / "synthetic_dataset_no_license.json").read_text("utf-8"))
    v = validate_dataset(ds)
    assert v["verdict"] == "reject"
    assert "LICENSE_BASIS_MISSING" in _codes(v)
    # The license finding is an error, never a warning.
    assert "LICENSE_BASIS_MISSING" not in _codes(v, "warnings")
    ds2 = json.loads((FIXTURES / "synthetic_dataset.json").read_text("utf-8"))
    ds2["license_basis"] = "  "
    assert validate_dataset(ds2)["verdict"] == "reject"


def test_validator_rejects_duplicate_ids_signlist_and_class(fixture_dataset):
    ds = copy.deepcopy(fixture_dataset)
    ds["inscriptions"][4]["inscription_id"] = "SYN001"
    v = validate_dataset(ds)
    assert v["verdict"] == "reject"
    assert "DUPLICATE_INSCRIPTION_ID" in _codes(v)
    ds = copy.deepcopy(fixture_dataset)
    del ds["inscriptions"][0]["sign_list"]
    v = validate_dataset(ds)
    assert v["verdict"] == "reject"
    assert "SIGN_LIST_UNDECLARED" in _codes(v)
    ds = copy.deepcopy(fixture_dataset)
    ds["source_class"] = "some_new_class"
    v = validate_dataset(ds)
    assert v["verdict"] == "reject"
    assert "SOURCE_CLASS_INVALID" in _codes(v)


def test_validator_warnings_only_for_optional_absences(fixture_dataset):
    ds = copy.deepcopy(fixture_dataset)
    del ds["compiler"]
    del ds["inscriptions"][0]["object_type"]
    v = validate_dataset(ds)
    assert v["verdict"] == "pass-with-warnings"
    assert v["errors"] == []
    assert "RECOMMENDED_FIELD_MISSING" in _codes(v, "warnings")


# ------------------------------------------------------- dedup module

def test_harness_dedup_is_the_shared_module():
    assert harness.dedup is dedup_module.dedup


def _rec(tokens):
    return {"inscription_id": "x", "site": "s", "tokens": list(tokens)}


def test_dedup_module_stages():
    kept, counts = dedup_module.dedup(
        [_rec(["P001", "P009"]), _rec(["P001", "P009"]),
         _rec(["P009", "P001"])])
    assert counts == {"input": 3, "stage_a_removed": 1,
                      "stage_b_removed": 0, "stage_c_removed": 0,
                      "kept": 2} and len(kept) == 2
    a = _rec(["P001", "P002", "P003", "P004"])
    b = _rec(["P001", "P002", "P003", "P005"])
    c = _rec(["P001", "P002", "P006", "P005"])
    kept, counts = dedup_module.dedup([a, b, c])
    assert counts["stage_c_removed"] == 1 and kept == [a, c]  # no chaining


def test_dedup_module_matches_harness_on_harness_fixtures(mapper):
    ds = adapt_converted_layer(HARNESS_FIXTURES / "toy_layer.json",
                               mapper, "toy")
    kept_m, counts_m = dedup_module.dedup(ds.records)
    kept_h, counts_h = harness.dedup(ds.records)
    assert counts_m == counts_h == {"input": 4, "stage_a_removed": 1,
                                    "stage_b_removed": 0,
                                    "stage_c_removed": 0, "kept": 3}
    assert [r["inscription_id"] for r in kept_m] == \
        [r["inscription_id"] for r in kept_h]


def _layer_path():
    for cand in (REPO / "corpora" / "downloads",
                 Path.home() / "workspace" / "glossa-lab"
                 / "corpora" / "downloads"):
        p = cand / "icit_fieldcady" / "icit_converted_v2.json"
        if p.exists():
            return p
    return None


def test_dedup_module_reproduces_phase119_appendix_a6(mapper):
    """Spec 018 Appendix A.6 measured numbers through the shared
    module: 4,531 in; 1,468/370/247 removed; 2,446 kept;
    cumulative removal 46.02%."""
    path = _layer_path()
    if path is None:
        pytest.skip("icit_converted_v2.json not present in this checkout")
    ds = adapt_converted_layer(path, mapper, "layer")
    kept, counts = dedup_module.dedup(ds.records)
    assert counts == EXPECTED_LAYER_DEDUP
    assert len(kept) == 2446
    removed = counts["input"] - counts["kept"]
    assert round(100 * removed / counts["input"], 2) == 46.02
    kept_h, counts_h = harness.dedup(ds.records)
    assert counts_h == counts and len(kept_h) == len(kept)


# ---------------------------------------------------------- evaluability

def test_evaluability_assignment(fixture_dataset):
    ev = assign_evaluability(fixture_dataset)
    assert ev["source_class"] == "rmrl_concordance"
    assert ev["per_prediction"] == {"PRED-2026-001": "QUALIFIES",
                                    "PRED-2026-002": "QUALIFIES",
                                    "PRED-2026-003": "QUALIFIES"}
    assert ev["multi_site"] is True and ev["distinct_sites"] == 2
    assert ev["caveat_c1_required"] is False
    ds = copy.deepcopy(fixture_dataset)
    ds["source_class"] = "icit_lineage_derivative"
    ev = assign_evaluability(ds)
    assert set(ev["per_prediction"].values()) == {"NO"}
    ds["source_class"] = "icit_full"
    ev = assign_evaluability(ds)
    assert ev["caveat_c1_required"] is True
    assert set(ev["per_prediction"].values()) == {"QUALIFIES"}
    for ins in ds["inscriptions"]:
        ins["site"] = "only-site"
    ev = assign_evaluability(ds)
    assert ev["pred2026_003_site_input"] is False


# ------------------------------------------- structural dry-run-only rule

def test_intake_module_binds_no_scoring_path():
    assert not hasattr(intake, "evaluate")
    src = Path(intake.__file__).read_text("utf-8")
    assert "import evaluate" not in src and ", evaluate" not in src
    # The only harness names intake binds are the dry-run path,
    # the evaluability matrix and dataset containers.
    bound = {n for n in ("evaluate", "_score_rate", "_score_template")
             if hasattr(intake, n)}
    assert bound == set()


# ------------------------------------------------------------- end-to-end

def test_run_intake_end_to_end(fixture_dataset, classes):
    report = run_intake(fixture_dataset, classes)
    assert report["outcome"] == "intake-complete-dry-run-only"
    assert report["stages"]["license_gate"] == "pass"
    assert report["stages"]["validation"]["verdict"] == "pass"
    # The deliberate duplicate cluster is caught, one per stage.
    assert report["stages"]["dedup"] == EXPECTED_FIXTURE_DEDUP
    assert report["stages"]["evaluability"]["qualifies_any"] is True
    dr = report["stages"]["harness_dry_run"]
    assert dr["label"] == DRY_RUN_LABEL == report["label"]
    assert dr["dedup"] == EXPECTED_FIXTURE_DEDUP
    blob = json.dumps(dr)
    assert "verdict" not in blob and "meets_criterion" not in blob
    assert '"rate"' not in blob


def test_run_intake_rejects_no_license_variant(classes):
    ds = json.loads(
        (FIXTURES / "synthetic_dataset_no_license.json").read_text("utf-8"))
    report = run_intake(ds, classes)
    assert report["outcome"] == "rejected"
    assert report["stages"]["license_gate"] == "reject"
    assert "dedup" not in report["stages"]
    assert "harness_dry_run" not in report["stages"]


def test_run_intake_non_parpola_sign_list_skips_dry_run(fixture_dataset,
                                                        classes):
    ds = copy.deepcopy(fixture_dataset)
    for ins in ds["inscriptions"]:
        ins["sign_list"] = "mahadevan_1977"
        ins["tokens"] = ["M" + t[1:] for t in ins["tokens"]
                         if t != "UNK"] or ["M901"]
    report = run_intake(ds, classes)
    assert report["outcome"] == "intake-complete-dry-run-only"
    assert report["stages"]["harness_dry_run"]["status"] == "skipped"
    assert "adapter" in report["stages"]["harness_dry_run"]["reason"]


# ------------------------------------------------------------------- H23

def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase130IntakePack" in ATOMIC_NODES
