"""Spec 059 freeze fences (F1 object-ID join replication).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the gate bar adopted at
DD-059-7 (joined share at least 61.0 percent, at
least 3,465 of 5,679 rows; the exact-points and
relative readings refused on the record), the
object-identifier sources named and pinned at
DD-059-9 (the lineage layer's cisi field carried
as provenance.object_id under the pinned
Phase-130 schema, per the pinned Spec 034
route-(b) construction, resolving against the
pinned catalogue layer's 3,493 distinct
objects), the string-identity boundary
(F059-C06; Spec 037's census), the identical
Phase-136 machinery (TERMINAL14, CMH, B = 9,999,
seed 20261009), the single-test correction
family confirmed at DD-059-8, the verdict
mapping with DD-059-3's precedence confirmed at
DD-059-12, the total outcome set, the step-0
gates, and Phase-421; (3) the governed claim
register is the frozen register (15 claims,
integrity-clean, recovered to 0.8-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-059-14 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (every spec section 2 pin,
verified at the freeze by two independent
routes; the Phase-136 flow and parameters and
its recorded local-store pins; the combined
report's family table; Phase-141's LOSO
stability; Spec 034 route (b)'s provenance
join; Spec 037's census; the registry's 803
rows; the Phase-130 schema's provenance
object_id field; the Phase-398 construction).
The local-store files' freeze-time hashes are
asserted as definition constants only, in the
Spec 038 form: they are not committed, so no
live-file hash is asserted on them in the suite;
their recorded values inside the committed
Phase-136 results file are asserted instead.
These tests build no join, compute no census,
and run no F1 quantity.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/059-f1-object-join"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
RESULTS136 = REPO / "reports/phase136_results.json"
STAGE2A = REPO / "specs/024-evidence-integration/stage2a-freeze.md"
BUILDER136 = REPO / "backend/scripts/phase136_terminal_type.py"
PHASE141 = REPO / "reports/phase141_report.md"
STAGE2_REPORT = REPO / "reports/phase136_137_138_stage2_report.md"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
SPEC034_OUTCOME = REPO / "specs/034-matched-object-attribution/outcome.md"
SPEC037_OUTCOME = REPO / "specs/037-cisi31-concordance-spine/outcome.md"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
SCHEMA = REPO / "data/intake/intake_dataset_schema_v1.json"
PHASE398 = REPO / "backend/glossa_lab/phase398_matched_object.py"
INTAKE = REPO / "backend/glossa_lab/intake.py"

RESULTS136_SHA256 = (
    "11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022"
)
STAGE2A_SHA256 = (
    "c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c"
)
BUILDER136_SHA256 = (
    "d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871"
)
PHASE141_SHA256 = (
    "d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347"
)
STAGE2_REPORT_SHA256 = (
    "6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062"
)
REGISTRY_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
SPEC034_SHA256 = (
    "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175"
)
SPEC037_SHA256 = (
    "28e444f20e698b3533559aac3a4bc3efcbc50440e79427ae58f656642886a02a"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
SCHEMA_SHA256 = (
    "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b"
)
PHASE398_SHA256 = (
    "278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0"
)
INTAKE_SHA256 = (
    "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03"
)
HORUS84_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
)
CAT1_SHA256 = (
    "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e"
)
CAT2_SHA256 = (
    "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9"
)
KEYED_SHA256 = (
    "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8"
)
TERMINAL14 = [
    "P020", "P076", "P095", "P099", "P108", "P125", "P210",
    "P226", "P256", "P346", "P359", "P378", "P384", "P385",
]

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
    assert definition["experiment_id"] == "spec059-f1-object-join"
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-421"
    claim = design["claim_under_test"]
    assert claim["id"] == "STUDY-SPEC-024/F1"
    assert "2.384" in claim["record"]
    assert "0.00015" in claim["record"]
    assert "STABLE" in claim["record"]
    # The gate bar, adopted with its arithmetic (DD-059-7).
    gate = design["gate"]
    assert "DD-059-7" in gate["ruling"]
    assert "61.0" in gate["ruling"]
    assert "3,465" in gate["ruling"]
    assert "50.977" in gate["baseline"]
    assert "3,463" in gate["refused_readings"]
    assert "3,186" in gate["refused_readings"]
    assert "JOIN GATE NOT MET" in gate["closure"]
    # The join: sources named and pinned (DD-059-9).
    join = design["join"]
    assert "DD-059-9" in join["ruling"]
    assert "exactly one distinct object" in join["construction"]
    assert "provenance.object_id" in join["construction"]
    assert join["lineage_source"]["sha256"] == HORUS84_SHA256
    assert join["lineage_source"]["bytes"] == 1190884
    assert join["converted_form"]["sha256"] == KEYED_SHA256
    assert join["converted_form"]["bytes"] == 1586137
    assert "5,018" in join["converted_form"]["posture"]
    assert join["catalogue_source"]["object_key"] == "cisi_id"
    assert join["catalogue_source"]["rows"] == 7705
    assert join["catalogue_source"]["distinct_objects"] == 3493
    assert join["schema"]["sha256"] == SCHEMA_SHA256
    assert join["schema"]["validator_sha256"] == INTAKE_SHA256
    assert join["construction_precedent"]["sha256"] == PHASE398_SHA256
    assert "DD-059-11" in join["audit"]
    # The string-identity boundary, with Spec 037's census.
    boundary = design["string_boundary"]
    assert "F059-C06" in boundary
    assert "49.21" in boundary
    assert "provenance.object_id" in boundary
    assert "gate 0.2" in boundary
    # The machinery: identical Phase-136, unchanged.
    machinery = design["machinery"]
    for sign in TERMINAL14:
        assert sign in machinery
    assert "B = 9,999" in machinery
    assert "seed 20261009" in machinery
    assert "Cochran-Mantel-Haenszel" in machinery
    assert "Robins-Breslow-Greenland" in machinery
    # The correction: single-test family confirmed (DD-059-8).
    assert "DD-059-8" in design["correction"]
    assert "single primary test" in design["correction"]
    assert "closed" in design["correction"]
    # Verdicts and their precedence (DD-059-12 confirming DD-059-3).
    assert "REPLICATED" in design["verdicts"]["mapping"]
    assert "WEAKENED" in design["verdicts"]["mapping"]
    assert "NOT REPLICATED" in design["verdicts"]["mapping"]
    assert "DD-059-12" in design["verdicts"]["precedence"]
    assert "DD-059-3" in design["verdicts"]["precedence"]
    # Reporting, outcomes, gates, and the execution gate.
    assert "leave-one-site-out" in design["reporting"]
    assert "mints no verdict" in design["reporting"]
    assert design["outcomes"] == [
        "INVALID",
        "CLOSED AT STEP 0 - JOIN GATE NOT MET",
        "NOT ESTIMABLE",
        "REPLICATED",
        "WEAKENED",
        "NOT REPLICATED",
    ]
    gates = design["step0_gates"]
    assert "5,679" in gates and "2,895" in gates
    assert "2,782" in gates
    assert "DD-059-7" in gates
    assert "does not itself join anything" in design["freeze_does_not"]
    assert "Not satisfied at the freeze" in design["execution_gate"]
    assert "Phase-421" in design["execution_gate"]
    # Inputs: every section 2 pin, as verified two-route at the freeze.
    inputs = definition["inputs"]
    assert inputs["phase136_results"]["sha256"] == RESULTS136_SHA256
    assert inputs["stage2a_freeze"]["sha256"] == STAGE2A_SHA256
    assert inputs["phase136_builder"]["sha256"] == BUILDER136_SHA256
    assert inputs["phase141_report"]["sha256"] == PHASE141_SHA256
    assert inputs["stage2_report"]["sha256"] == STAGE2_REPORT_SHA256
    assert inputs["registry"]["sha256"] == REGISTRY_SHA256
    assert inputs["registry"]["rows"] == 803
    assert inputs["spec034_outcome"]["sha256"] == SPEC034_SHA256
    assert inputs["spec037_outcome"]["sha256"] == SPEC037_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["local_store"]["catalogue_vol1_sha256"] == CAT1_SHA256
    assert inputs["local_store"]["catalogue_vol2_sha256"] == CAT2_SHA256
    assert "two independent routes" in inputs["pin_verification"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F059-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # Every committed spec section 2 pin, live in the repo.
    assert _sha(RESULTS136) == RESULTS136_SHA256
    assert _sha(STAGE2A) == STAGE2A_SHA256
    assert _sha(BUILDER136) == BUILDER136_SHA256
    assert _sha(PHASE141) == PHASE141_SHA256
    assert _sha(STAGE2_REPORT) == STAGE2_REPORT_SHA256
    assert _sha(REGISTRY) == REGISTRY_SHA256
    assert _sha(SPEC034_OUTCOME) == SPEC034_SHA256
    assert _sha(SPEC037_OUTCOME) == SPEC037_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    assert _sha(SCHEMA) == SCHEMA_SHA256
    assert _sha(PHASE398) == PHASE398_SHA256
    assert _sha(INTAKE) == INTAKE_SHA256
    # The Phase-136 record: the flow, the parameters, and the
    # local-store pins it recorded (asserted in-repo, Spec 038 form).
    results = json.loads(RESULTS136.read_text(encoding="utf-8"))
    flow = results["flow"]
    assert flow["layer_rows"] == 5679
    assert flow["matched_single_volume"] == 2895
    assert flow["ambiguous"] == 2
    assert flow["unmatched"] == 2782
    assert flow["typed_filled"] == 2752
    assert flow["restricted_seals_tablets"] == 2676
    assert flow["terminal_mapped"] == 2195
    assert flow["analysis_population_eligible_strata"] == 2062
    params = results["parameters"]
    assert params["B"] == 9999
    assert params["seed"] == 20261009
    assert params["terminal14"] == TERMINAL14
    recorded = results["inputs"]
    assert recorded["horus84_inscriptions"]["sha256"] == HORUS84_SHA256
    assert recorded["horus84_inscriptions"]["bytes"] == 1190884
    assert recorded["cisi_vol1_catalogue"]["sha256"] == CAT1_SHA256
    assert recorded["cisi_vol2_catalogue"]["sha256"] == CAT2_SHA256
    assert recorded["canonical_sign_registry"]["sha256"] == REGISTRY_SHA256
    # The combined report's family table: F1 SUPPORTED at q 0.00015.
    report_text = STAGE2_REPORT.read_text(encoding="utf-8")
    assert "| **F1** |" in report_text
    assert "0.00015" in report_text
    assert "**SUPPORTED**" in report_text
    # Phase-141: F1 STABLE under LOSO, intervals excluding 1.
    phase141_text = PHASE141.read_text(encoding="utf-8")
    assert "STABLE" in phase141_text
    assert "2.706" in phase141_text
    # Spec 034 route (b): the provenance.object_id join precedent.
    outcome034 = SPEC034_OUTCOME.read_text(encoding="utf-8")
    assert "5,018" in outcome034
    assert "provenance.object_id" in outcome034
    assert "pass" in outcome034
    # Spec 037's census: the string-identity boundary's ground.
    outcome037 = SPEC037_OUTCOME.read_text(encoding="utf-8")
    assert "693" in outcome037
    assert "CONFLICT 341 (49.21%)" in outcome037
    # The registry: pin and 803 rows.
    rows = list(csv.DictReader(
        REGISTRY.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 803
    # The Phase-130 schema: provenance carries the object_id field.
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    inscription = schema["$defs"]["inscription"]
    provenance = inscription["properties"]["provenance"]
    assert "object_id" in provenance["properties"]
    assert "source_reference" in provenance["properties"]
    # The Phase-398 construction: object_id carried from cisi.
    phase398_text = PHASE398.read_text(encoding="utf-8")
    assert "def build_intake_dataset" in phase398_text
    assert '"object_id": cisi' in phase398_text
    # The Stage 2(a) freeze: TERMINAL14 as frozen there.
    stage2a_text = STAGE2A.read_text(encoding="utf-8")
    for sign in TERMINAL14:
        assert sign in stage2a_text


FREEZE_STAMPS = [
    "20261021T115324Z",
    "20261021T115324Z",
    "20261021T115324Z",
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
