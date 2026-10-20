"""Spec 038 draft freeze fences (PRED-2026-007 full-population census, D-31).

Pins: (1) the draft machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the registered
criterion verbatim, the mechanical verdict rule
with no pre-written outcome, the population frame
(NOT enumerated at draft), the named primary /
cross-check sources with their hashes and the
conflict rule, the DD-038-9 cluster-class
operationalisation, the coverage rule, and the
step-0 closures exactly as designed; (3) the
governed claim register is the draft register
(14 claims, integrity-clean, hooks not run — the
hooks are a freeze gate under aee 1.5.0); (4) the
cited records still carry the facts the design
rests on (the PRED register entry; the primary
source's FORM — 611 per-sign records carrying an
icit_function field, values never inspected; the
cross-check's header; the recorded Phase 5
output's three named assignments; the
characterisation's classes for those clusters;
the parser's Wells lineage; the mayig feature
files' lack of any function field).
These tests enumerate nothing, score nothing,
and compute no share.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/038-pred-2026-007-full-population"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
PRED_REGISTER = REPO / "docs/PREDICTION_REGISTER.md"
PRIMARY = REPO / "reports/indus_cgsa_cluster_analysis.json"
CROSS_CHECK = REPO / "data/crosswalks/canonical_sign_registry.csv"
SIGN_CLUSTERS = REPO / "outputs/analysis/sign_clusters.json"
CHARACTERIZATION = REPO / "reports/cluster_characterization.md"
FULS_PARSER = REPO / "backend/glossa_lab/data/fuls_parser.py"
MAYIG_DIR = REPO / "data/raw/other_sites/mayig_features"

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
        "spec038-pred-2026-007-full-population"
    )
    assert definition["register"]["claims"] == 14
    assert definition["register"]["register_version"] == "0.5-draft"
    assert "NOT RUN" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert "Phase-401" in design["phase"]
    crit = design["criterion"]
    assert crit["share_min"] == 0.7
    assert "ITM-coded signs are TERMINAL" in crit["verbatim"]
    # The verdict rule is mechanical and no outcome
    # is pre-written for any branch (DD-038-1).
    assert "mechanical" in crit["verdict_rule"]
    assert "no pre-written outcome" in crit["verdict_rule"]
    assert "mixed in a non-ITM sign" in crit["recorded_partial_test"]
    pop = design["population"]
    assert "NOT enumerated" in pop["status_at_draft"]
    assert "P098 (LOG)" in pop["excluded_by_rule"]
    srcs = design["sources"]
    primary = srcs["primary_function_code"]
    assert primary["file"] == (
        "reports/indus_cgsa_cluster_analysis.json")
    assert primary["records"] == 611
    assert primary["sha256"] == (
        "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3"
    )
    assert srcs["cross_check_function_code"]["sha256"] == (
        "228a4e138c7fdb9016dae50e24db8d96767620825da7959d30963b4dd0bcee035"
    )
    assert "primary governs" in srcs["conflict_rule"]
    assert "DD-038-5" in srcs["conflict_rule"]
    p5 = design["phase5_output"]
    assert p5["assignment"]["sha256"] == (
        "27ed99060f6f6d2e3332e070a74c9b43848c1c8cd0dfd2e6abab2f48f6fa55a1"
    )
    assert p5["assignment"]["best_k"] == 40
    assert p5["assignment"]["signs_clustered"] == 160
    assert "DD-038-9" in p5["cluster_class_rule"]
    assert p5["sanity_anchor"] == {
        "P385": 21, "P378": 39, "P098": 10}
    assert "CANNOT BE RUN AS WRITTEN" in (
        design["step0"]["failure_closure"])
    assert design["coverage_rule"]["floor"] == 0.8
    assert "no outcome is pre-written" in design["census_branch"]
    assert "no freeze order" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["pred_register"]["sha256"] == (
        "425cf07b7532d4ef8baab7a81463502650b59ba54ea98f6ee34ee11e48ce8829"
    )


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.5-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F038-C{i:02d}" for i in range(1, 15)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    register = PRED_REGISTER.read_text(encoding="utf-8")
    assert "PRED-2026-007" in register
    assert (
        "≥ 70% of ITM-coded signs are TERMINAL or "
        "cluster in TERMINAL clusters" in register
    )
    assert "PARTIALLY CONFIRMED" in register
    assert "P098 (LOG) is Cluster 10 INITIAL" in register
    # Primary source FORM only: 611 per-sign records
    # carrying an icit_function field. The values
    # are never inspected here — reading them
    # across signs would be the enumeration.
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    records = primary["data"]["a"]
    assert len(records) == 611
    for rec in records[:5]:
        assert "icit_function" in rec
        assert "sign_id" in rec
    # Cross-check header carries the field.
    with CROSS_CHECK.open(encoding="utf-8") as fh:
        header = next(csv.reader(fh))
    assert "icit_function" in header
    # The recorded Phase 5 output survives and
    # reproduces the register's named assignments.
    clusters = json.loads(
        SIGN_CLUSTERS.read_text(encoding="utf-8"))
    assert clusters["best_k"] == 40
    s2c = clusters["sign_to_cluster"]
    assert len(s2c) == 160
    assert s2c["P385"] == 21
    assert s2c["P378"] == 39
    assert s2c["P098"] == 10
    # The characterisation records the classes the
    # registered partial test used (DD-038-9).
    characterization = CHARACTERIZATION.read_text(
        encoding="utf-8")
    assert "Cluster 21 — TERMINAL" in characterization
    assert "Cluster 39 — TERMINAL" in characterization
    assert "Cluster 10 — INITIAL" in characterization
    # The codes' lineage is Wells-derived, and the
    # mayig feature files carry no function field.
    parser = FULS_PARSER.read_text(encoding="utf-8")
    assert "(from Wells)" in parser
    assert '"ITM"' in parser
    feature_files = sorted(MAYIG_DIR.glob("*.json"))
    assert len(feature_files) >= 396
    for path in feature_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert not any(
            "function" in key.lower() for key in data
        ), path
