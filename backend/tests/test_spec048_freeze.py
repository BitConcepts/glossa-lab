"""Spec 048 freeze fences (Parpola fish-family profiles).

Pins: (1) the freeze machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the Asset F pin-timing ruling
(DD-048-9: Spec 044's freeze digest quoted as the
contract anchor, the pin source fixed as Spec
044's step-0 outcome record, gate 0.1 asserting
the byte-digest at execution step 0), the strict
corpus reading confirmed (DD-048-10: the Spec 033
section 4 V3 / Mahadevan-lineage corpus with the
gate-0.3 T2.4 reproduction), the join via
mahadevan_number with the UNMAPPED disposition
(DD-048-15), the 20% member bar, the nine-class
outcome set, the control rules, the OSF decision
under campaign E-1, and Phase-408; (3) the governed
claim register is the frozen register (15 claims,
integrity-clean, recovered to 0.7-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-048-17 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (manual_002's state and sign_ids,
the Phase-43 T2.4 reference points, the anchors
census with M072's corrected status, the
crosswalk's Parpola citation, the Spec 033 corpus
statement). These tests count no fish sign, build
no asset, and change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/048-parpola-fish-family-profiles"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "parpola_2010_dravidian_solution.json"
)
PHASE43 = REPO / "outputs/phase43_all.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
CROSSWALK = (
    REPO / "backend/glossa_lab/data/"
    "mahadevan_parpola_crosswalk.json"
)
SPEC033 = (
    REPO / "specs/033-sa-free-language-comparison/spec.md"
)

CLAIM_SHA256 = (
    "3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba"
    "20d06c1b22810dfb000c"
)
PHASE43_SHA256 = (
    "78a6c21908b9362854c54dd3d820d717be22feab3af"
    "11135663fa14aaf554fe4"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580"
    "088e6086592b32d34f569"
)
CROSSWALK_SHA256 = (
    "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8"
    "ed28ccc6e06444a2dc69b"
)
SPEC033_SHA256 = (
    "eaea0e2e4f288e199acfa56cc401b80b5939175578"
    "ccb5f52c87adddf2f15ca9"
)
SPEC044_FREEZE_DIGEST = (
    "6851f943d196fa389e48b67cb5161b90daa1180d8a3"
    "e1cf3f020fcf25691d9c8"
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
        "spec048-parpola-fish-family-profiles"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-408"
    # The claim and its standing state.
    claim = design["claim"]
    assert claim["id"] == (
        "parpola_2010_dravidian_solution_manual_002"
    )
    assert "IN QUESTION" in claim["state"]
    assert "partially supported" in claim["state"]
    # Asset F: the pin-timing ruling (DD-048-9).
    asset = design["asset_f"]
    assert asset["contract_anchor"]["freeze_digest"] == (
        SPEC044_FREEZE_DIGEST
    )
    assert "PR #243" in asset["contract_anchor"]["source"]
    assert "not yet merged" in asset["contract_anchor"]["source"]
    assert asset["pin_source"]["record"] == (
        "Spec 044's step-0 outcome record"
    )
    assert asset["pin_source"]["asset_file"] == (
        "specs/044-fish-sign-coastal-residue/"
        "asset-f-fish-family.json"
    )
    gate = asset["gate_0_1"]
    assert "EXECUTION step 0" in gate
    assert "ASSET F NOT AVAILABLE" in gate
    assert "ASSET F DIGEST MISMATCH" in gate
    assert "digest field excluded" in gate
    # The join: mahadevan_number, UNMAPPED (DD-048-15).
    join = design["join"]
    assert "mahadevan_number" in join["via"]
    assert "UNMAPPED" in join["unmapped"]
    assert "never counted as TOO THIN" in join["unmapped"]
    # The strict corpus reading (DD-048-10).
    corpus = design["strict_corpus"]
    assert "V3 / Mahadevan-lineage" in corpus["reading"]
    assert "Spec 033" in corpus["reading"]
    assert "not a restriction" in corpus["reading"]
    repro = corpus["reproduction"]
    assert repro["sign_72"] == {
        "occurrences": 181, "terminal_frac": 0.259,
        "supported": True,
    }
    assert repro["sign_267"] == {
        "occurrences": 356, "terminal_frac": 0.038,
        "supported": False,
    }
    assert repro["candidates"] == [267, 72, 65, 59, 60, 70]
    # The test form.
    test = design["test"]
    assert "T2.4" in test["measure"]
    assert test["member_bar"] == 0.20
    assert test["family_lines"] == {"supported": 0.70, "not_supported": 0.30}
    assert test["floor"] == 30
    assert "integral" in test["second_arm"]
    assert design["outcomes"] == [
        "FAMILY SUPPORTED",
        "FAMILY NOT SUPPORTED",
        "INCONCLUSIVE",
        "TOO THIN",
        "ASSET F NOT AVAILABLE",
        "ASSET F DIGEST MISMATCH",
        "STRICT CORPUS NOT PINNABLE",
        "SECOND ARM NOT RUNNABLE",
        "INVALID",
    ]
    # The controls (DD-048-13).
    controls = design["controls"]
    assert "at or above" in controls["comparison"]
    assert "half the smallest" in controls["matching_rule"]
    assert "twice the largest" in controls["matching_rule"]
    # The fences and the execution gate.
    assert "Roif hold" in design["fences"]
    assert "awaits the verified approval" in (
        design["execution_gate"]
    )
    assert "no count was made at the freeze" in (
        design["execution_gate"]
    )
    # Inputs: hashes as definition constants.
    inputs = definition["inputs"]
    assert inputs["claim_file"]["sha256"] == CLAIM_SHA256
    assert inputs["claim_file"]["claim_status"] == (
        "partially_supported"
    )
    assert inputs["phase43"]["sha256"] == PHASE43_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["anchors"]["total"] == 287
    assert inputs["anchors"]["strict_sa_independent"] == 94
    assert inputs["crosswalk"]["sha256"] == CROSSWALK_SHA256


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F048-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The claim file: entry and standing state,
    # asserted on the live file. Its whole-file
    # hash is not asserted here, by the Spec 038
    # form. The extracted-claims store is
    # regenerated wholesale by the backend suite
    # itself (its scripts rewrite extraction_date),
    # so by the time this test runs in the full
    # suite the working-tree file may hash
    # differently from its committed bytes. The
    # freeze-time hash (3202aeca...) remains
    # asserted as a definition constant
    # (test_freeze_definition_constants) and in
    # the freeze record, and manual_002's facts
    # are asserted on the live file below.
    claim_doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))
    entries = [
        c for c in claim_doc["claims"]
        if c["claim_id"] == (
            "parpola_2010_dravidian_solution_manual_002"
        )
    ]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["claim_status"] == "partially_supported"
    assert entry["stage"] == "explained"
    assert entry["sign_ids"]["mahadevan"] == ["72", "64", "70"]
    assert "run sign by sign across the whole fish family" in (
        entry["not_understood"]
    )
    assert "on the strict corpus" in entry["not_understood"]
    # The Phase-43 record: pin and T2.4 reference points.
    assert _sha(PHASE43) == PHASE43_SHA256
    phase43 = json.loads(PHASE43.read_text(encoding="utf-8"))
    t24 = phase43["T2_4_fish_rebus"]
    assert t24["fish_sign_candidates_tested"] == [
        267, 72, 65, 59, 60, 70
    ]
    assert t24["primary_fish_72"]["total"] == 181
    assert t24["primary_fish_72"]["terminal_frac"] == 0.259
    assert t24["primary_fish_72"]["supported"] is True
    assert t24["primary_fish_267"]["total"] == 356
    assert t24["primary_fish_267"]["terminal_frac"] == 0.038
    assert t24["primary_fish_267"]["supported"] is False
    # The anchors file: pin, census, and the
    # corrected M072 fact (DD-048-18).
    assert _sha(ANCHORS) == ANCHORS_SHA256
    anchors_doc = json.loads(ANCHORS.read_text(encoding="utf-8"))
    anchors = anchors_doc["anchors"]
    assert len(anchors) == 287
    strict = [
        k for k, v in anchors.items()
        if v.get("validation_status") == "strict_sa_independent"
    ]
    assert len(strict) == 94
    assert "M072" in anchors
    assert anchors["M072"]["validation_status"] == (
        "pending_non_sa_validation"
    )
    assert "M072" not in strict
    # The crosswalk: pin and the Parpola citation.
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    refs = " ".join(crosswalk["_citation"]["full_references"])
    assert "fig. 5.1, pp. 70-78" in refs
    # Spec 033's corpus statement (DD-048-10's basis).
    assert _sha(SPEC033) == SPEC033_SHA256
    spec033 = SPEC033.read_text(encoding="utf-8")
    flat = " ".join(spec033.split())
    assert (
        "the program's V3/Mahadevan-lineage corpus as "
        "held in the database" in flat
    )
    assert "94 readings carrying validation status" in flat


FREEZE_STAMPS = [
    "20261021T102254Z",
    "20261021T102256Z",
    "20261021T102259Z",
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
