"""Spec 058 freeze fences (transcription-disagreement mechanism).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - Phase-420, the CONTRADICTED
claim of record and its residue question, the
hypothesis and its falsifier, the store ruling
(DD-058-15: the Phase-132 store survives complete,
proven at the freeze by inventory and exact
reproduction, production deferred to execution
gate 0.2 with no store bytes pinned), the step-0
gates 0.1-0.6 fail-closed in order with their two
stop classes, the frozen machinery imported
unchanged, the event definitions, the T1-T3
tabulations with the UNK handling, the three locus
rules with their confirmed draft readings
(DD-058-3, DD-058-6, DD-058-8), the total headline
mapping including MULTIPLE LOCI (DD-058-9), arm B
blocked with no AI substitution, and the execution
gate; (3) the governed claim register is the frozen
register (16 claims, integrity-clean, recovered to
0.8-draft at the freeze gate) and the three
freeze-hook artifacts record the pass on the
DD-058-18 reading (zero correctness failure modes;
only FR-2.3 draft-cap records; no claim below the
0.70 threshold); (4) the cited records still carry
the facts the design rests on (every spec section
2.1 pin, verified at the freeze by two independent
routes; the pilot's recorded numbers; the
Phase-383 interval, verdict, and origin audit; the
frame census; the dataset meta's content hash of
record). These tests run no alignment, tabulate
no event, and compute no localisation quantity.
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/058-transcription-disagreement-mechanism"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
SPEC023 = REPO / "specs/023-keyed-transcription-layer/spec.md"
METRICS = REPO / "reports/phase132_pilot_metrics.json"
PILOT_REPORT = REPO / "reports/phase132_pilot_report.md"
FRAME = REPO / "data/keyed_transcription/phase132_pilot_frame.json"
DATASET = REPO / "data/keyed_transcription/phase132_pilot_dataset_v1.json"
DATASET_META = (
    REPO / "data/keyed_transcription/phase132_pilot_dataset_v1_meta.json"
)
R383_RESULTS = REPO / "reports/phase383_results.json"
R383_REPORT = REPO / "reports/phase383_report.md"
METRICS_MODULE = REPO / "backend/scripts/phase132_metrics.py"
RESCORING_MODULE = REPO / "backend/scripts/phase383_pilot_rescoring.py"
CROSSWALK = REPO / "data/crosswalks/parpola_mahadevan_crosswalk_v1.json"
LANE2 = REPO / "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

PINS = {
    SPEC023: "c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2",
    METRICS: "e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554",
    PILOT_REPORT: "e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00",
    FRAME: "a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea",
    DATASET: "adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400",
    DATASET_META: "b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4",
    R383_RESULTS: "4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334",
    R383_REPORT: "9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca",
    METRICS_MODULE: "238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984",
    RESCORING_MODULE: "b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec",
    CROSSWALK: "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb",
    LANE2: "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb",
    ANCHORS: "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
}
CLAIM_ID = "STUDY-SPEC-023/PHASE-132+383"

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
        "spec058-transcription-disagreement-mechanism"
    )
    assert definition["register"]["claims"] == 16
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-420"
    claim = design["claim_under_test"]
    assert claim["id"] == CLAIM_ID
    assert "CONTRADICTED" in claim["record"]
    assert "0.20" in claim["record"]
    assert "[0.10, 0.32]" in claim["record"]
    assert "origin groups = 1" in claim["record"]
    assert "not understood" in claim["residue"]
    assert "concentrated, not uniform" in design["hypothesis"]
    assert "NOT LOCALISED" in design["falsifier"]
    # The store ruling: survival proven at the freeze,
    # production deferred to gate 0.2, no bytes pinned.
    store = design["store"]
    assert "DD-058-15" in store["ruling"]
    assert "survives complete" in store["ruling"]
    assert "320 events" in store["ruling"]
    assert "deferred to execution gate 0.2" in store["production"]
    assert "no store bytes" in store["production"]
    assert "pass_gold" in store["layout"]
    # Step-0 gates: ordered, fail-closed, two stop classes.
    gates = design["step0_gates"]
    assert "PILOT-PASS RECORDS NOT PRODUCIBLE" in gates
    assert "INVALID" in gates
    assert "0.4-0.6 suffice" in gates
    assert "DD-058-16" in gates
    # Machinery and events: frozen module, P primary.
    assert "imported unchanged" in design["machinery"]
    assert "UNMAPPED:<M_ID>" in design["machinery"]
    assert "SUBSTITUTION" in design["events"]
    assert "INDEL" in design["events"]
    assert "first divergence" in design["events"]
    # Tabulations and UNK handling.
    assert "DD-058-6" in design["tabulations"]
    assert "381 tokens" in design["tabulations"]
    assert "never carries the headline" in design["unk_handling"]
    assert "illegibility" in design["unk_handling"]
    # Locus rules with their confirmed readings.
    loci = design["locus_rules"]
    assert "at least 50%" in loci["signs"]
    assert "UNIFORM" in loci["signs"]
    assert "DD-058-8" in loci["object_types"]
    assert "10 points" in loci["object_types"]
    assert "DD-058-3" in loci["segmentation"]
    # Outcomes and headline mapping are total.
    assert design["outcomes"] == [
        "LOCALISED TO SIGNS",
        "LOCALISED TO OBJECT TYPES",
        "LOCALISED TO SEGMENTATION",
        "LOCALISED TO MULTIPLE LOCI",
        "NOT LOCALISED",
        "PILOT-PASS RECORDS NOT PRODUCIBLE",
        "INVALID",
    ]
    assert "DD-058-9" in design["headline_mapping"]
    assert "MULTIPLE LOCI" in design["headline_mapping"]
    # Arm B: blocked, no substitution.
    assert "blocked and out of scope" in design["arm_b"]
    assert "no AI substitution" in design["arm_b"]
    # What the freeze does not do, and the execution gate.
    assert "does not itself localise" in design["freeze_does_not"]
    assert "Not satisfied at the freeze" in design["execution_gate"]
    assert "approval" in design["execution_gate"]
    # Inputs: every section 2.1 pin, as verified two-route.
    inputs = definition["inputs"]
    assert inputs["spec023"]["sha256"] == PINS[SPEC023]
    assert inputs["pilot_metrics"]["sha256"] == PINS[METRICS]
    assert inputs["pilot_report"]["sha256"] == PINS[PILOT_REPORT]
    assert inputs["pilot_frame"]["sha256"] == PINS[FRAME]
    assert inputs["pilot_dataset"]["sha256"] == PINS[DATASET]
    assert inputs["pilot_dataset_meta"]["sha256"] == PINS[DATASET_META]
    assert inputs["phase383_results"]["sha256"] == PINS[R383_RESULTS]
    assert inputs["phase383_report"]["sha256"] == PINS[R383_REPORT]
    assert inputs["metrics_module"]["sha256"] == PINS[METRICS_MODULE]
    assert inputs["rescoring_module"]["sha256"] == PINS[RESCORING_MODULE]
    assert inputs["crosswalk"]["sha256"] == PINS[CROSSWALK]
    assert inputs["lane2_drafts"]["sha256"] == PINS[LANE2]
    assert inputs["lane2_drafts"]["claim_id"] == CLAIM_ID
    assert inputs["anchors"]["sha256"] == PINS[ANCHORS]
    assert "two" in inputs["pin_verification"]
    assert "independent routes" in inputs["pin_verification"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F058-C{i:02d}" for i in range(1, 17)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # Every section 2.1 pin, on the live files.
    for path, sha in PINS.items():
        assert _sha(path) == sha, path
    # The pilot's recorded numbers.
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    exact = metrics["exact_sequence_agreement"]
    assert exact["all_50"]["p"]["rate"] == 0.2
    assert exact["all_50"]["m"]["rate"] == 0.2
    assert exact["all_50"]["p"]["n_exact"] == 10
    per_token = metrics["per_token_agreement"]
    assert per_token["all_50"]["p"]["matches"] == 95
    assert per_token["all_50"]["p"]["denominator"] == 198
    assert per_token["gold_sample"]["p"]["matches"] == 18
    assert per_token["gold_sample"]["p"]["denominator"] == 42
    estimator = metrics["gold_error_estimator"]
    assert estimator["p"]["rate"] == 0.05
    assert estimator["p"]["differing_positions"] == 2
    assert estimator["p"]["denominator"] == 40
    counts = metrics["counts"]
    assert counts["n_objects"] == 50
    assert counts["n_gold_objects"] == 10
    assert counts["total_tokens_pass_a"] == 191
    assert counts["total_tokens_pass_b"] == 190
    assert counts["total_tokens_pass_gold"] == 40
    assert counts["total_tokens_adjudicated_final"] == 189
    assert metrics["verdicts"]["stop_rule"]["stop_rule_fired"] is True
    # The Phase-383 record: interval, verdict, origin audit.
    r383 = json.loads(R383_RESULTS.read_text(encoding="utf-8"))
    assert r383["parameters"]["B_bootstrap"] == 9999
    assert r383["parameters"]["seed"] == 20261011
    pilot = r383["pilots"]["phase132"]
    assert pilot["bootstrap_exact_seq_ci95"] == [0.1, 0.32]
    assert pilot["recomputed_exact_sequence_agreement_all50_p"] == 0.2
    assert "CONTRADICTED" in pilot["taxonomy_verdict"]
    assert "ONE model family" in r383["origin_group_audit"]
    # The frame census, as recorded.
    frame_doc = json.loads(FRAME.read_text(encoding="utf-8"))
    frame = frame_doc["frame"]
    assert len(frame) == 50
    sites = collections.Counter(e["site"] for e in frame)
    assert sites == {
        "Mohenjo-Daro": 25,
        "Harappa": 15,
        "Lothal": 6,
        "Kalibangan": 4,
    }
    types = collections.Counter(e["object_type"] for e in frame)
    assert types["Seals"] == 34
    assert types["Tablets"] == 11
    assert types[""] == 5
    assert sum(1 for e in frame if e["gold"]) == 10
    # The dataset meta carries the content hash of record and
    # the pinned crosswalk hash.
    meta = json.loads(DATASET_META.read_text(encoding="utf-8"))
    assert meta["dataset_content_hash"] == (
        "7bdc73f5e0f6a959f8d94a4317c642ebe36638e841f7bb80bae97c75477f224a"
    )
    assert meta["crosswalk"]["sha256"] == PINS[CROSSWALK]
    # The crosswalk carries the rows the metrics record states.
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    assert len(crosswalk["rows"]) == 766
    # The lane-2 record of the claim under test.
    lane2 = json.loads(LANE2.read_text(encoding="utf-8"))
    entry = [
        d for d in lane2["drafts"] if d["claim_id"] == CLAIM_ID
    ]
    assert len(entry) == 1
    assert "CONTRADICTED" in entry[0]["lane1_status"]
    assert "not understood" in json.dumps(entry[0]).lower()


FREEZE_STAMPS = [
    "20261021T114007Z",
    "20261021T114007Z",
    "20261021T114007Z",
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
