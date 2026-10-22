"""Spec 072 freeze fences (fish-family profiles, ICIT-native).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the verdict line derived at
the freeze (L = 0.765, OPEN-072-1: the 95th
percentile, nearest-rank rank 82 of 86, of the
reference distribution of non-fish signs clearing
total >= 20 on the primary population, recorded
in reference-distribution.json, sha256
55d266b3...; the Phase-43 points and Spec 048's
20 percent bar excluded as inputs), the
concordance act (OPEN-072-2: the two pinned basis
files and the unique-intersection rule; M048 to
243, M050 to 220, M060 to 235, M145 to 032, M147
to 033; M047 and M052 UNIDENTIFIED IN ICIT under
the confirmed DD-072-5 disposition, with the
depiction divergence named), the populations and
the carried measure with its confirmed readings
(OPEN-072-3, OPEN-072-4), the majority partition
(OPEN-072-5), the grade-flip headline rule
(OPEN-072-6), the step-0 gates with gates 0.1 and
0.2 PASS at the freeze, the outcome set, the Roif
gate (OPEN-072-10), and Phase-431; (3) the
governed claim register is the frozen register
(15 claims, integrity-clean, recovered at
0.8-draft in three rounds) and the three
freeze-hook artifacts record the pass on the
DD-038-10 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited records
still carry the facts the design rests on (Asset
F's digest recomputed under Spec 044 section
4.2's exclusion rule; the crosswalk pins; the
registry and crosswalk entries the concordance
was read from; the Phase-43 pin). The
restricted-local corpus and row-grades files are
asserted as definition constants only, in the
Spec 038 form: they are never committed, so no
live-file hash is asserted on them in the suite;
gate 0.1 at execution recomputes them. These
tests compute no member fraction and no census.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/072-fish-family-profiles-redesign"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
REF_DIST = SPEC / "reference-distribution.json"
ASSET_F = REPO / "specs/044-fish-sign-coastal-residue/asset-f-fish-family.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
YAJNADEVAM = REPO / "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv"
MASTER = REPO / "data/crosswalks/sign_crosswalk_master.csv"
MP_CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk.json"
PHASE43 = REPO / "outputs/phase43_all.json"

ASSET_F_DIGEST = "ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3"
REGISTRY_SHA256 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
YAJNADEVAM_SHA256 = "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
MASTER_SHA256 = "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
MP_SHA256 = "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b"
PHASE43_SHA256 = "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4"
REF_DIST_SHA256 = "55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5"
CORPUS_SHA256 = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
GRADES_SHA256 = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"

IDENTIFIED = {"M048": "243", "M050": "220", "M060": "235", "M145": "032", "M147": "033"}

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
    assert definition["experiment_id"] == "spec072-fish-family-profiles-redesign"
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-431"
    claim = design["claim_under_test"]
    assert claim["id"] == "parpola_2010_dravidian_solution_manual_002"
    assert "IN QUESTION" in claim["record"]
    # The derived verdict line (OPEN-072-1).
    line = design["verdict_line"]
    assert line["L"] == 0.765
    assert line["reference_record"]["sha256"] == REF_DIST_SHA256
    assert line["reference_record"]["sign_count"] == 86
    assert line["reference_record"]["nearest_rank_index_1based"] == 82
    assert abs(line["reference_record"]["p95_fraction"] - 0.7647058823529411) < 1e-12
    assert "VERDICT LINE NOT DERIVABLE" in line["degeneracy_rule"]
    assert "25.9" in line["excluded_inputs"]
    assert "20 percent" in line["excluded_inputs"]
    # The concordance (OPEN-072-2).
    conc = design["concordance"]
    assert conc["identified"] == IDENTIFIED
    assert conc["unidentified"] == ["M047", "M052"]
    assert conc["basis"]["registry"]["sha256"] == REGISTRY_SHA256
    assert conc["basis"]["yajnadevam_crosswalk"]["sha256"] == YAJNADEVAM_SHA256
    assert "UNIDENTIFIED IN ICIT" in conc["disposition"]
    assert "depiction" in conc["divergence_named"]
    # Populations, measure, partition, grade-flip, gates, Roif.
    assert "3,212" in design["populations"]
    assert "5,299" in design["populations"]
    assert "TERMINAL_STRONG" in design["measure"]
    assert "no chance-baseline" in design["measure"]
    assert "50 percent" in design["partition"]
    assert "70 percent" in design["partition"]
    assert "GRADE-SENSITIVE" in design["grade_flip"]
    assert "SHAKTI INTAKE NOT REPRODUCED" in design["step0_gates"]
    assert "L = 0.765" in design["step0_gates"]
    assert design["outcomes"] == [
        "FAMILY SUPPORTED",
        "FAMILY NOT SUPPORTED",
        "INCONCLUSIVE",
        "TOO THIN",
        "SHAKTI INTAKE NOT REPRODUCED",
        "ASSET F DIGEST MISMATCH",
        "ASSET F NOT AVAILABLE",
        "CONCORDANCE FAILED",
        "INVALID",
    ]
    assert "Roif 2025a" in design["roif_gate"]
    assert "143222807" in design["roif_gate"]
    assert "does not itself score any member" in design["freeze_does_not"]
    assert "Phase-431" in design["execution_gate"]
    # Inputs: the pins as asserted at the freeze.
    inputs = definition["inputs"]
    assert inputs["asset_f"]["digest"] == ASSET_F_DIGEST
    assert inputs["asset_f"]["member_count"] == 7
    assert inputs["shakti_corpus"]["sha256"] == CORPUS_SHA256
    assert inputs["row_grades"]["sha256"] == GRADES_SHA256
    assert inputs["phase43_results"]["sha256"] == PHASE43_SHA256
    assert inputs["mahadevan_parpola_crosswalk"]["sha256"] == MP_SHA256
    assert "bfc811df" in inputs["intake_record"]["merged"]
    assert "5,704" in inputs["intake_record"]["census"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F072-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_reference_distribution_record():
    assert _sha(REF_DIST) == REF_DIST_SHA256
    rec = json.loads(REF_DIST.read_text(encoding="utf-8"))
    assert rec["sign_count"] == 86
    entries = rec["entries"]
    assert len(entries) == 86
    fracs = [e["fraction"] for e in entries]
    assert fracs == sorted(fracs)
    # The family codes are excluded (non-members only).
    assert not {e["sign"] for e in entries} & set(IDENTIFIED.values())
    # Every entry clears the carried supported floor.
    assert all(e["total"] >= 20 for e in entries)
    # Nearest-rank 95th percentile and the recorded line.
    rank = rec["derivation"]["nearest_rank_index_1based"]
    assert rank == 82
    assert abs(entries[rank - 1]["fraction"] - rec["derivation"]["p95_fraction"]) < 1e-12
    assert entries[rank - 1]["sign"] == "226"
    assert rec["derivation"]["verdict_line_L"] == 0.765


def test_cited_records_carry_the_design_facts():
    # Asset F: digest recomputed under Spec 044 section 4.2's rule.
    asset = json.loads(ASSET_F.read_text(encoding="utf-8"))
    assert asset["digest"] == ASSET_F_DIGEST
    assert asset["member_count"] == 7
    assert [m["sign_key"] for m in asset["members"]] == [
        "M047", "M048", "M050", "M052", "M060", "M145", "M147",
    ]
    body = {k: v for k, v in asset.items() if k != "digest"}
    canonical = json.dumps(
        body, indent=2, sort_keys=True, ensure_ascii=False
    ) + "\n"
    assert hashlib.sha256(canonical.encode("utf-8")).hexdigest() == ASSET_F_DIGEST
    # The crosswalk pins, live in the tree.
    assert _sha(REGISTRY) == REGISTRY_SHA256
    assert _sha(YAJNADEVAM) == YAJNADEVAM_SHA256
    assert _sha(MASTER) == MASTER_SHA256
    assert _sha(MP_CROSSWALK) == MP_SHA256
    assert _sha(PHASE43) == PHASE43_SHA256
    # The concordance entries, read from the pinned bases.
    registry = {
        r["parpola_id"]: r
        for r in csv.DictReader(REGISTRY.read_text(encoding="utf-8").splitlines())
    }
    assert registry["P047"]["wells_ids"] == "W517|W518"
    assert registry["P048"]["wells_ids"] == "W243"
    assert registry["P050"]["wells_ids"] == "W220"
    assert registry["P052"]["wells_ids"] == "W944"
    assert registry["P060"]["wells_ids"] == "W235"
    assert registry["P145"]["wells_ids"] == "W032"
    assert registry["P147"]["wells_ids"] == "W033"
    cross = list(csv.DictReader(YAJNADEVAM.read_text(encoding="utf-8").splitlines()))
    confirmed = {}
    for r in cross:
        if r["review_status"] == "confirmed":
            confirmed.setdefault(r["best_parpola_match"], set()).add(
                r["yajnadevam_glyph_id"].zfill(3)
            )
    assert confirmed.get("P047", set()) == set()
    assert confirmed.get("P052", set()) == set()
    assert "243" in confirmed["P048"]
    assert "220" in confirmed["P050"]
    assert "235" in confirmed["P060"]
    assert "032" in confirmed["P145"]
    assert "033" in confirmed["P147"]
    # The Phase-43 record: the split this question starts from.
    phase43 = json.loads(PHASE43.read_text(encoding="utf-8"))
    t24 = phase43["T2_4_fish_rebus"]
    assert t24["fish_sign_candidates_tested"] == [267, 72, 65, 59, 60, 70]
    assert t24["primary_fish_72"]["terminal_frac"] == 0.259
    assert t24["primary_fish_267"]["terminal_frac"] == 0.038


FREEZE_STAMPS = [
    "20261022T225508Z",
    "20261022T225511Z",
    "20261022T225514Z",
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
