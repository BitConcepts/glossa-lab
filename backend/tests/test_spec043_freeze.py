"""Spec 043 freeze fences (PRED-2026-012 registry frame).

Pins: (1) the machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the registered criterion
verbatim with its mechanical verdict rule, the
registry-primary population frame with the
population listed at draft (P056, P324, P378,
P385) and its census, the re-derivation rule,
the provenance gate (evidence set D1-D4, three
limbs, the PROVENANCE closure name, the
DD-043-10 borderline standard adopted at the
freeze), the LOG class enumerated-only
(DD-043-12), the recorded Phase 5 output with
the DD-043-7 cluster-class rule and the sanity
anchor, the coverage rule, the foreclosed
census branch, Phase-410, and the
campaign-approval execution citation; (3) the
governed claim register is the recovered register
(16 claims, integrity-clean, hooks passed at the
freeze act under aee 1.5.0); (4) the cited
records still carry the facts the design rests
on (the PRED register's PRED-2026-012 entry, in
the Spec 038 form - facts on the live file, the
freeze-time hash asserted as a definition
constant, because the register is this
contract's own append target; the registry's
census and the exact re-derivation of its
icit_function column from the pinned builder
rule; the builder's and parser's pins and the
Wells lineage; the cross-check's FORM - 611
per-sign records carrying an icit_function
field, values never inspected here; the recorded
Phase 5 output's three named assignments; the
characterisation's classes for those clusters).
These tests compute no share, run no provenance
gate, and look up no Phase 5 assignment beyond
the register's own three named signs.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/043-pred-2026-007-registry-frame"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
PRED_REGISTER = REPO / "docs/PREDICTION_REGISTER.md"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSS_CHECK = REPO / "reports/indus_cgsa_cluster_analysis.json"
BUILDER = REPO / "scripts/cgsa_pipeline.py"
FULS_PARSER = REPO / "backend/glossa_lab/data/fuls_parser.py"
SIGN_CLUSTERS = REPO / "outputs/analysis/sign_clusters.json"
CHARACTERIZATION = REPO / "reports/cluster_characterization.md"

REGISTRY_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
CROSS_CHECK_SHA256 = (
    "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3"
)
BUILDER_SHA256 = (
    "4af822f1ad5c924defed7852df967f8633899b27a27fdaea84e2cdad8744efb0"
)
PARSER_SHA256 = (
    "9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615"
)
SIGN_CLUSTERS_SHA256 = (
    "623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a"
)
CHARACTERIZATION_SHA256 = (
    "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476"
)
PRED_REGISTER_SHA256 = (
    "254ccf039cf04cf2882e04c8658381cc05573163651ed5d478697058aa424984"
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
        "spec043-pred-2026-007-registry-frame"
    )
    assert definition["register"]["claims"] == 16
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-410"
    crit = design["criterion"]
    assert crit["share_min"] == 0.7
    assert "ITM-coded signs are TERMINAL" in crit["verbatim"]
    assert "mechanical" in crit["verdict_rule"]
    assert "no pre-written outcome" in crit["verdict_rule"]
    assert "mixed in a non-ITM sign" in crit["recorded_partial_test"]
    pop = design["population"]
    assert pop["listed_at_draft"] == ["P056", "P324", "P378", "P385"]
    assert pop["size"] == 4
    assert pop["census"] == {
        "rows": 803,
        "uncoded": 791,
        "coded": 12,
        "coded_counts": {
            "ITM": 4, "LOG": 2, "NUM": 2,
            "TMK": 2, "SHN": 1, "SYL": 1,
        },
    }
    assert "P098" in pop["excluded_by_rule"]
    assert pop["log_set"]["members"] == ["P217", "P310"]
    assert "enumerated-only" in pop["log_set"]["role"]
    assert "DD-043-12" in pop["log_set"]["role"]
    srcs = design["sources"]
    primary = srcs["primary_function_code"]
    assert primary["file"] == (
        "data/crosswalks/canonical_sign_registry.csv")
    assert primary["rows"] == 803
    assert primary["sha256"] == REGISTRY_SHA256
    cross = srcs["cross_check_function_code"]
    assert cross["records"] == 611
    assert cross["sha256"] == CROSS_CHECK_SHA256
    assert srcs["builder"]["sha256"] == BUILDER_SHA256
    assert srcs["parser"]["sha256"] == PARSER_SHA256
    assert "primary governs" in srcs["conflict_rule"]
    gate = design["provenance_gate"]
    assert "check 0.3" in gate["position"]
    assert set(gate["evidence_set"]) == {"D1", "D2", "D3", "D4"}
    assert len(gate["limbs"]) == 3
    assert "PROVENANCE" in gate["failure_closure"]
    assert "CANNOT BE RUN AS WRITTEN" in gate["failure_closure"]
    assert "no subset verdict" in gate["failure_closure"]
    assert "DD-043-10" in gate["borderline_standard"]
    assert "in words, with a locator" in gate["borderline_standard"]
    p5 = design["phase5_output"]
    assert p5["assignment"]["sha256"] == SIGN_CLUSTERS_SHA256
    assert p5["assignment"]["best_k"] == 40
    assert p5["assignment"]["signs_clustered"] == 160
    assert "DD-043-7" in p5["cluster_class_rule"]
    assert CHARACTERIZATION_SHA256 in p5["cluster_class_rule"]
    assert p5["sanity_anchor"] == {
        "P385": 21, "P378": 39, "P098": 10}
    assert len(design["step0"]["order"]) == 4
    assert "PROVENANCE" in design["step0"]["failure_closures"]
    assert design["coverage_rule"]["floor"] == 0.8
    assert "foreclosed" in design["census_branch"]
    # The execution gate carries the campaign
    # citation answering the register's line.
    gate_text = design["execution_gate"]
    assert "Phase-410" in gate_text
    assert "AS WRITTEN on 2026-10-21" in gate_text
    assert "Wave 3" in gate_text
    assert "does not run the provenance adjudication" in gate_text
    inputs = definition["inputs"]
    assert inputs["pred_register"]["sha256"] == PRED_REGISTER_SHA256
    assert "PRED-2026-012" in inputs["pred_register"]["entry"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F043-C{i:02d}" for i in range(1, 17)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The PRED register's PRED-2026-012 entry, in
    # the Spec 038 form: the freeze-time whole-file
    # hash is asserted as a definition constant
    # (test_freeze_definition_constants); the live
    # file is this contract's own append target at
    # execution, so its facts - not its hash - are
    # asserted here.
    register = PRED_REGISTER.read_text(encoding="utf-8")
    assert "PRED-2026-012" in register
    assert (
        "≥ 70% of ITM-coded signs are TERMINAL or "
        "cluster in TERMINAL clusters" in register
    )
    assert (
        "registration alone is not a scoring order" in register
    )
    assert "PARTIALLY CONFIRMED" in register
    # The primary source: pin, census, and the
    # exact re-derivation of the column that
    # defines the population (a population-side
    # read, disclosed in the design).
    assert _sha(REGISTRY) == REGISTRY_SHA256
    with REGISTRY.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 803
    coded = [r for r in rows if r["icit_function"]]
    assert len(coded) == 12
    assert sum(1 for r in rows if not r["icit_function"]) == 791
    itm = sorted(
        r["parpola_id"] for r in coded
        if r["icit_function"] == "ITM"
    )
    assert itm == ["P056", "P324", "P378", "P385"]
    log = sorted(
        r["parpola_id"] for r in coded
        if r["icit_function"] == "LOG"
    )
    assert log == ["P217", "P310"]
    p098 = [r for r in rows if r["parpola_id"] == "P098"]
    assert len(p098) == 1
    assert p098[0]["icit_function"] == ""
    assert p098[0]["wells_ids"] == "W400|W402"
    # The builder: pin, and its rule reproduces
    # every recorded value exactly.
    assert _sha(BUILDER) == BUILDER_SHA256
    tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
    table = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "_WELLS_FUNCTIONS"
            for t in node.targets
        ):
            table = ast.literal_eval(node.value)
    assert table is not None
    assert len(table) == 14
    assert table["W740"] == "ITM"
    for row in rows:
        wells = [
            w.strip()
            for w in (row["wells_ids"] or "").split("|")
            if w.strip()
        ]
        derived = ""
        for key, value in table.items():
            if key in wells:
                derived = value
                break
        assert derived == row["icit_function"], row["parpola_id"]
    # The parser: pin and Wells lineage.
    assert _sha(FULS_PARSER) == PARSER_SHA256
    parser = FULS_PARSER.read_text(encoding="utf-8")
    assert "(from Wells)" in parser
    assert '"ITM"' in parser
    # Cross-check FORM only: 611 per-sign records
    # carrying an icit_function field. The values
    # are never inspected here - the file's known
    # uncoded state is taken from Spec 038's
    # execution record, as the design states.
    assert _sha(CROSS_CHECK) == CROSS_CHECK_SHA256
    primary = json.loads(CROSS_CHECK.read_text(encoding="utf-8"))
    records = primary["data"]["a"]
    assert len(records) == 611
    for rec in records[:5]:
        assert "icit_function" in rec
        assert "sign_id" in rec
    # The recorded Phase 5 output survives and
    # reproduces the register's named assignments
    # (the sanity anchor - the only Phase 5 read
    # this test makes, as at the draft).
    assert _sha(SIGN_CLUSTERS) == SIGN_CLUSTERS_SHA256
    clusters = json.loads(
        SIGN_CLUSTERS.read_text(encoding="utf-8"))
    assert clusters["best_k"] == 40
    s2c = clusters["sign_to_cluster"]
    assert len(s2c) == 160
    assert s2c["P385"] == 21
    assert s2c["P378"] == 39
    assert s2c["P098"] == 10
    assert _sha(CHARACTERIZATION) == CHARACTERIZATION_SHA256
    characterization = CHARACTERIZATION.read_text(
        encoding="utf-8")
    assert "Cluster 21 — TERMINAL" in characterization
    assert "Cluster 39 — TERMINAL" in characterization
    assert "Cluster 10 — INITIAL" in characterization


FREEZE_STAMPS = [
    "20261021T102815Z",
    "20261021T102818Z",
    "20261021T102820Z",
]

CORRECTNESS_CATEGORIES = {
    "coverage_gap",
    "contradiction",
    "assumption_unvalidated",
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
