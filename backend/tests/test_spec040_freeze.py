"""Spec 040 freeze fences (D-25: G1 chronology-controlled).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the dependency gate satisfied
by the openly recorded successor-artifact
substitution (Spec 039 executed and named, its
artifact at its pin and recorded as not
satisfying section 1; Spec 041's artifact
accepted as the successor dependency artifact at
its pin), derivation A1 with the counts
reproduced at the freeze, the margins gate's
three arms all retained (DD-040-6) with the
NOT-YET-TESTABLE closure word (DD-040-5) and the
known margins consequence stated, the
interval-at-margin decision rule (DD-040-1
adopted), section 8.1 NOT APPLICABLE on the
zero-contested-cell record, Phase-439, and the
Phase-140 / Phase-385 machinery constants;
(3) the governed claim register is the frozen
register (15 claims, integrity-clean, recovered
at 0.7-draft in two rounds) and the three
freeze-hook artifacts record the pass on the
DD-038-10 reading (zero correctness failure
modes; only FR-2.3 draft-cap records; no claim
below the 0.70 threshold, minimum 0.8445);
(4) the section 1 verification the freeze rests
on, recomputed here from the pinned records:
the accepted artifact hashes to its pin and
validates against its schema, the cell census
built from the pinned Phase-139 covariates
equals the artifact's 78 triples exactly, and
the section 4.1 join under A1 yields exactly
one assignment row for each of the 5,410
population inscription IDs, reproducing the
published A1 counts; (5) the cited in-repo
records still carry the facts the design rests
on (the Phase-140 and Phase-385 quantities, the
spine and covariate pins, the Spec 025 rider,
the Spec 027 section 6.2 assignment field). The
anchors pin stands as a definition constant
only: this spec asserts anchors byte-identical
before and after any execution, at execution.
These tests join no label for outcome purposes,
run no margin, and calculate no repertoire
quantity - the A1 join below is the freeze
record's own verification, reproduced.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
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
ARTIFACT = (
    REPO / "data/evidence_integration/site_period_mapping.jsonl"
)
ARTIFACT_META = (
    REPO / "data/evidence_integration/site_period_mapping_meta.json"
)
SPEC039_ARTIFACT = (
    REPO / "data/movement/gazetteer_rows_assigned.jsonl"
)
SPEC039_FREEZE = (
    REPO / "specs/039-gazetteer-period-assignment/freeze.json"
)
SPEC041_FREEZE = (
    REPO / "specs/041-site-local-label-period-mapping/freeze.json"
)
SPEC041_CENSUS = (
    REPO
    / "specs/041-site-local-label-period-mapping/step0-census.json"
)
SPEC025 = REPO / "specs/025-stage2-controlled-followup/spec.md"
SPEC027 = REPO / "specs/027-movement-culture-language/spec.md"
SPEC030_OUTCOME = (
    REPO / "specs/030-q6-chronology-spine-extension/outcome.md"
)

SPEC039_DIGEST = "ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742"
SPEC039_ARTIFACT_SHA256 = "64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4"
SPEC041_DIGEST = "fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7"
SPEC041_ARTIFACT_SHA256 = "1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67"
SPEC041_META_SHA256 = "bda1017dd88da0b14efaa3ffc5ff280b09818349bda4de1ed20f8c60d42864a9"
SPEC041_CENSUS_SHA256 = "b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be"
COVARIATES_SHA256 = "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
SPINE_SHA256 = "9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93"
ANCHORS_SHA256 = "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"

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
        "spec040-d25-g1-chronology-controlled"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.8445" in definition["register"]["aee_hook_pass"]
    assert "Approve as specified" in definition["basis"]["decisions"]
    design = definition["design"]
    assert "Phase-439" in design["phase"]
    assert "Phase-438" in design["phase"]
    assert design["claim_under_test"] == "STUDY-SPEC-025/G1"
    # The dependency gate: satisfied by substitution,
    # both artifacts named, the 039 finding unamended.
    gate = design["dependency_gate"]
    assert "SATISFIED" in gate["state_at_freeze"]
    assert "successor-artifact substitution" in (
        gate["state_at_freeze"])
    a039 = gate["spec039_artifact"]
    assert a039["sha256"] == SPEC039_ARTIFACT_SHA256
    assert a039["spec039_freeze_digest"] == SPEC039_DIGEST
    assert "did NOT satisfy" in a039["standing"]
    a041 = gate["spec041_artifact"]
    assert a041["sha256"] == SPEC041_ARTIFACT_SHA256
    assert a041["spec041_freeze_digest"] == SPEC041_DIGEST
    assert a041["meta_sha256"] == SPEC041_META_SHA256
    assert a041["step0_census_sha256"] == SPEC041_CENSUS_SHA256
    assert "ACCEPTED" in a041["standing"]
    assert "24 MAPPED" in a041["standing"]
    assert "0 CONTESTED" in a041["standing"]
    assert "published period determinations only" in (
        " ".join(gate["requires"]))
    # The assignment discipline and derivation A1.
    assignment = design["period_assignment"]
    assert assignment["labels"] == ["EARLY", "MATURE", "LATE"]
    assert "UNASSIGNED" in assignment["primary_rule"]
    assert "site-level occupation label inheritance" in (
        assignment["forbidden_placements"])
    deriv = assignment["derivation"]
    assert "A1" in deriv["name"]
    assert "does not veto" in deriv["rule"]
    assert "No field precedence" in deriv["rule"] or (
        "no field precedence" in deriv["rule"])
    assert "not silently substituted" in deriv["not_chosen"]
    assert "1,457 placed" in deriv["reproduced_at_freeze"]
    assert "EARLY 32" in deriv["reproduced_at_freeze"]
    assert "MATURE 1,386" in deriv["reproduced_at_freeze"]
    assert "LATE 39" in deriv["reproduced_at_freeze"]
    assert "Mohenjo-daro 0" in deriv["reproduced_at_freeze"]
    assert "NOT APPLICABLE" in assignment["contested"]
    assert "zero" in assignment["contested"]
    # The margins gate's three arms, all retained,
    # and the known consequence stated.
    margins = design["margins_gate"]
    assert margins["sites_per_period_min"] == 5
    assert margins["periods_required"] == ["EARLY", "MATURE", "LATE"]
    assert margins["unassigned_share_max"] == 0.4
    assert margins["permutable_min"] == 1000
    assert "RETAINED" in margins["permutable_arm_status"]
    assert "NOT-YET-TESTABLE" in margins["failure_state"]
    assert "DD-040-5" in margins["failure_state"]
    consequence = margins["known_consequence"]
    assert "73.1%" in consequence
    assert "85.6%" in consequence
    assert "0 of its 1,923" in consequence
    assert "settlement and closure act" in consequence
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
    # The decision rule: DD-040-1 adopted; the three
    # outcome mappings, none softened.
    rules = design["decision_rules"]
    assert "ADOPTED" in rules["rule_source"]
    assert "DD-040-1" in rules["rule_source"]
    assert "SUPPORTED - CHRONOLOGY CONTROLLED" in rules["supported"]
    assert "WEAKENED - RIDER CONFIRMED AS MATERIAL" in (
        rules["weakened"])
    assert "period-confounded" in rules["weakened"]
    assert "CONTRADICTED AT THE DECLARED MARGIN" in (
        rules["contradicted"])
    assert "NOT APPLICABLE" in design["sensitivities"][0]
    assert "separate owner order" in design["execution_gate"]
    assert "Phase-439" in design["execution_gate"]
    # The pinned inputs.
    inputs = definition["inputs"]
    assert inputs["layer"]["sha256"] == (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
    )
    assert inputs["layer"]["population_rows"] == 5410
    assert inputs["covariates"]["sha256"] == COVARIATES_SHA256
    assert inputs["spine"]["sha256"] == SPINE_SHA256
    assert inputs["spine"]["rows"] == 205
    assert inputs["recorded_results"]["phase385"][
        "governing_basic_ci95"] == [
            0.1837750116366994, 0.2102434435947284]
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "refreshed at the freeze" in inputs["anchors"]["note"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F040-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["independent_of"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def _informative(value: str) -> bool:
    return value is not None and value.strip() not in ("", "-")


def test_dependency_artifact_and_a1_join():
    # The accepted artifact, live in the tree, at its pin.
    assert _sha(ARTIFACT) == SPEC041_ARTIFACT_SHA256
    assert _sha(ARTIFACT_META) == SPEC041_META_SHA256
    assert _sha(SPEC041_CENSUS) == SPEC041_CENSUS_SHA256
    # The two dependency records' freeze digests.
    rec039 = json.loads(SPEC039_FREEZE.read_text(encoding="utf-8"))
    assert rec039["digest"] == SPEC039_DIGEST
    assert _sha(SPEC039_ARTIFACT) == SPEC039_ARTIFACT_SHA256
    rec041 = json.loads(SPEC041_FREEZE.read_text(encoding="utf-8"))
    assert rec041["digest"] == SPEC041_DIGEST
    cells = [
        json.loads(ln)
        for ln in ARTIFACT.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert len(cells) == 78
    cellmap = {
        (c["site"], c["field"], c["local_label"]): c for c in cells
    }
    assert len(cellmap) == 78
    reasons = Counter()
    for c in cells:
        assert c["contested"] is False
        assert c["sensitivity_label"] is None
        if c["status"] == "MAPPED":
            assert c["coarse_period"] in ("EARLY", "MATURE", "LATE")
            assert len(c["determinations"]) == 1
            det = c["determinations"][0]
            assert det["verification"] == "OWN_TEXT"
            assert det["citation"] and det["locator"]
            assert det["mapping_rule"]
            assert c["unassigned_reason"] is None
        else:
            assert c["status"] == "UNASSIGNED"
            assert c["coarse_period"] == "UNASSIGNED"
            assert c["determinations"] == []
            reasons[c["unassigned_reason"]] += 1
    assert Counter(
        c["coarse_period"] for c in cells if c["status"] == "MAPPED"
    ) == {"EARLY": 4, "MATURE": 18, "LATE": 2}
    assert reasons == {
        "NO_PUBLISHED_DETERMINATION": 35,
        "DETERMINATION_UNVERIFIED": 10,
        "SPANS_COARSE_BOUNDARY": 4,
        "LABEL_UNCERTAIN_IN_LAYER": 3,
        "NOT_IN_PUBLISHED_SCHEME": 2,
    }
    # The population, from the pinned covariates; the
    # census triples equal the artifact's exactly.
    assert _sha(COVARIATES) == COVARIATES_SHA256
    covariates = json.loads(COVARIATES.read_text(encoding="utf-8"))
    assert len(covariates) == 5410
    population = [
        {
            "id": r["id"].strip(),
            "site": r["site"].strip(),
            "period": (r["period_raw"] or "").strip(),
            "phase": (r["phase_raw"] or "").strip(),
        }
        for r in covariates
    ]
    assert len({r["id"] for r in population}) == 5410
    margins = Counter()
    census = Counter()
    for row in population:
        p_inf = _informative(row["period"])
        f_inf = _informative(row["phase"])
        margins["period"] += p_inf
        margins["phase"] += f_inf
        margins["both"] += p_inf and f_inf
        margins["union"] += p_inf or f_inf
        margins["neither"] += (not p_inf) and (not f_inf)
        for field in ("period", "phase"):
            if _informative(row[field]):
                census[(row["site"], field, row[field])] += 1
    assert margins == {
        "period": 2266, "phase": 2638, "both": 1788,
        "union": 3116, "neither": 2294,
    }
    assert set(census) == set(cellmap)
    for key, n in census.items():
        assert cellmap[key]["attested_rows"] == n
    # The section 4.1 join under A1: exactly one
    # assignment row per population inscription ID,
    # reproducing Spec 041's published A1 counts.
    placed = Counter()
    placed_by_site = defaultdict(Counter)
    unplaced = Counter()
    assignments = {}
    for row in population:
        row_cells = [
            cellmap[(row["site"], field, row[field])]
            for field in ("period", "phase")
            if _informative(row[field])
        ]
        period = None
        if not row_cells:
            unplaced["no_informative_label"] += 1
        else:
            mapped = [
                c for c in row_cells if c["status"] == "MAPPED"
            ]
            if mapped:
                values = {c["coarse_period"] for c in mapped}
                if len(values) == 1:
                    period = mapped[0]["coarse_period"]
                else:
                    unplaced["disagreement"] += 1
            elif any(
                c["status"] == "CONTESTED" for c in row_cells
            ):
                unplaced["contested_only"] += 1
            else:
                unplaced["all_unassigned"] += 1
        assignments[row["id"]] = period or "UNASSIGNED"
        if period is not None:
            placed[period] += 1
            placed_by_site[row["site"]][period] += 1
    assert len(assignments) == 5410
    assert set(assignments.values()) <= {
        "EARLY", "MATURE", "LATE", "UNASSIGNED"}
    assert placed == {"EARLY": 32, "MATURE": 1386, "LATE": 39}
    assert sum(placed.values()) == 1457
    assert unplaced == {
        "no_informative_label": 2294,
        "all_unassigned": 1658,
        "disagreement": 1,
    }
    assert {
        s: sum(c.values()) for s, c in placed_by_site.items()
    } == {
        "Dholavira": 133, "Harappa": 1021, "Kalibangan": 157,
        "Lothal": 108, "Nausharo": 38,
    }


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
    assert _sha(SPINE) == SPINE_SHA256
    spine_lines = [
        ln for ln in SPINE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert len(spine_lines) == 205
    assert _sha(COVARIATES) == COVARIATES_SHA256
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


FREEZE_STAMPS = [
    "20261024T150459Z",
    "20261024T150502Z",
    "20261024T150506Z",
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
