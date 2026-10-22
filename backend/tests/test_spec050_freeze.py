"""Spec 050 freeze fences (Hunt sky signs' endings).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, with the covered-source set exact);
(2) the definition carries the frozen contract
exactly - Phase-416, the celestial class as Asset
A's sky_cycle kind exactly (DD-050-1, frozen at
DD-050-13) with the broader closing notion as a
stated untested boundary, Asset A consumed under
Spec 045's contract with its pin timing ruled at
the freeze (DD-050-11: Spec 045's freeze digest
5d8254dd... as contract anchor, Spec 045's
asset-a-freeze.json as the fixed pin source, gate
0.1 asserting the SHA-256 at execution step 0 -
mismatch ASSET PIN MISMATCH, unfrozen ASSET NOT
FROZEN, exactly as drafted), the DD-045-18
coverage consequence (DD-050-12: gate 0.3 does
not close INVALID for want of corpus-wide
coverage on that ground), the step-0 gates, and
the pre-registered test (frequency band of
DD-050-2, Fisher's exact test two-sided of
DD-050-4, the 1.5 / 1.0 criteria, the symmetric
30-occurrence TOO THIN floor of DD-050-3, the
two sensitivity arms); (3) the governed claim
register is the frozen register (15 claims,
integrity-clean, recovered to 0.8-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-050-9 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (the section 6 pins asserted as
freeze-time facts against the definition; the
live records checked for their design facts -
the positional quantities, the Phase-43 class
counts, the crosswalk census of 205 rows and
187 distinct sign keys, the corpus row count,
the anchors census, the Phase-104 UNTESTED /
RULE-CLASS entry, and Spec 045's frozen digest
with its DD-045-18 consequence). No live-file
hash is asserted on any cited record: the
section 6 pins are freeze-time facts asserted
against the definition, and the step-0 pin
check is an execution-time act over a pristine
checkout (the Spec 038 form). These tests
classify no sign, take no census, join nothing,
and compute no final-position quantity.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/050-hunt-sky-signs-endings"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
POSITIONAL = (
    REPO / "glossa-indus/analysis/positional/hunt_tripartite_test.json"
)
PHASE43 = REPO / "outputs/phase43_all.json"
CORPUS = REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
PHASE104 = REPO / "glossa-indus/reports/phase104_claims_evaluation.json"
SPEC045 = REPO / "specs/045-hunt-depicted-kinds"
SPEC045_FREEZE = SPEC045 / "freeze.json"

PINS = {
    POSITIONAL: (
        "0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48"
    ),
    PHASE43: (
        "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4"
    ),
    CORPUS: (
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
    ),
    CROSSWALK: (
        "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
    ),
    ANCHORS: (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
    ),
    PHASE104: (
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"
    ),
}
SPEC045_FREEZE_DIGEST = (
    "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
)
CLAIM_ID = "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004"

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []
    # The covered-source set is exact: nothing else
    # decides the question (prefix integrity of the
    # freeze payload - the digest covers precisely
    # these sources, no more, no fewer).
    assert set(record["sources"]) == {
        "specs/050-hunt-sky-signs-endings/freeze.md",
        "specs/050-hunt-sky-signs-endings/spec.md",
        "specs/050-hunt-sky-signs-endings/claims.json",
        "specs/050-hunt-sky-signs-endings/adjudication.md",
        "specs/050-hunt-sky-signs-endings/aee/freeze-aee-note.md",
        "specs/050-hunt-sky-signs-endings/build_freeze.py",
        "backend/tests/test_spec050_freeze.py",
    }


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == "spec050-hunt-sky-signs-endings"
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-416"
    assert design["claim_id"] == CLAIM_ID
    assert "stays_untested" in design["claim_status"]
    assert "RULE-CLASS" in design["claim_status"]
    # Asset A is a contract at the freeze, not a built asset.
    asset = design["asset_a"]
    assert "NOT built at this freeze" in asset["form"]
    assert "NOT in existence at this freeze" in asset["form"]
    # The pin-timing ruling (DD-050-11): contract anchor,
    # fixed pin source, gate 0.1 assertion at step 0.
    anchor = asset["contract_anchor"]
    assert anchor["freeze_digest"] == SPEC045_FREEZE_DIGEST
    assert anchor["freeze_record"] == (
        "specs/045-hunt-depicted-kinds/freeze.json"
    )
    assert asset["pin_source"] == (
        "specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json"
    )
    assert "DD-050-11" in asset["pin_timing"]
    assert "does not exist yet" in asset["pin_timing"]
    assert "ASSET PIN MISMATCH" in asset["gate_0_1"]
    assert "ASSET NOT FROZEN" in asset["gate_0_1"]
    assert "exactly as drafted" in asset["gate_0_1"]
    # The celestial class is sky_cycle exactly (DD-050-1),
    # with the broader notion an untested boundary.
    assert "exactly the set of signs" in asset["celestial_class"]
    assert "sky_cycle" in asset["celestial_class"]
    assert "DD-050-1" in asset["celestial_class"]
    assert "NOT tested" in asset["untested_boundary"]
    assert "never silently widened" in asset["untested_boundary"]
    # The Spec 050 coverage consequence (DD-045-18 via DD-050-12).
    assert "does not close INVALID" in design["coverage_consequence"]
    assert "187" in design["coverage_consequence"]
    assert "DD-045-18" in design["coverage_consequence"]
    # The frozen test form.
    test = design["test"]
    assert "DD-050-2" in test["comparison_class"]
    assert "two-sided" in test["fisher_exact"]
    assert "DD-050-4" in test["fisher_exact"]
    crit = test["criteria"]
    assert ">= 1.5" in crit["supported"]
    assert "p < 0.05" in crit["supported"]
    assert "at least half" in crit["supported"]
    assert crit["not_supported"] == "enrichment ratio <= 1.0"
    assert "DD-050-3" in crit["too_thin"]
    assert test["thin_floor"] == 30
    assert "S1" in test["sensitivities"]
    assert "S2" in test["sensitivities"]
    assert "DD-050-15" in design["step0_gates"]
    # Inputs: the section 6 pins plus the claim-status record
    # and the Spec 045 anchor, as freeze-time facts.
    inputs = definition["inputs"]
    assert inputs["corpus_layer"]["sha256"] == PINS[CORPUS]
    assert inputs["corpus_layer"]["rows"] == 5679
    assert inputs["positional_record"]["sha256"] == PINS[POSITIONAL]
    assert inputs["phase43_record"]["sha256"] == PINS[PHASE43]
    assert inputs["crosswalk_master"]["sha256"] == PINS[CROSSWALK]
    assert inputs["crosswalk_master"]["rows"] == 205
    assert inputs["crosswalk_master"]["distinct_sign_keys"] == 187
    assert inputs["anchors"]["sha256"] == PINS[ANCHORS]
    assert inputs["anchors"]["anchors"] == 287
    assert inputs["phase104_record"]["sha256"] == PINS[PHASE104]
    assert inputs["phase104_record"]["verdict"] == "stays_untested"
    assert inputs["phase104_record"]["rule"] == "RULE-CLASS"
    assert inputs["phase104_record"]["claim_id"] == CLAIM_ID
    assert inputs["spec045_freeze"]["digest"] == SPEC045_FREEZE_DIGEST
    assert "two routes" in inputs["pins_reasserted"]
    # The execution gate is NOT satisfied at the freeze.
    assert "NOT satisfied at the freeze" in design["execution_gate"]
    assert "Asset A does not exist" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F050-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert item["observed_at"] == "2026-10-21"
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def _find_claim(node, claim_id):
    if isinstance(node, dict):
        if node.get("claim_id") == claim_id:
            return node
        for value in node.values():
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    return None


def test_cited_records_carry_the_design_facts():
    # The section 6 pins are freeze-time facts: they are
    # asserted against freeze.json's definition in
    # test_freeze_definition_constants, and the step-0
    # pin check is an execution-time act over a pristine
    # checkout (spec section 3, gate 0.2). Live byte
    # equality is NOT asserted here for any cited record:
    # the suite's own regeneration tests rewrite records
    # in the working tree before a freeze test runs
    # (the extracted-claims store precedent that turned
    # Specs 044's and 046's first freeze CI runs red;
    # the Spec 038 form). What this test asserts live is
    # that every cited record is present and still
    # carries the design facts the freeze rests on.
    for path in PINS:
        assert path.is_file(), path
    assert SPEC045_FREEZE.is_file()
    # The positional record carries the premise quantities
    # and its own two-accounts verdict.
    positional = json.loads(POSITIONAL.read_text(encoding="utf-8"))
    formula = positional["formula_test"]
    assert formula["inscriptions_with_imit_structure"] == 805
    assert formula["total_inscriptions_len3plus"] == 2267
    assert formula["formula_rate"] == 0.355
    assert formula["null_expected_rate"] == 0.006
    structural = positional["structural_test"]
    assert structural["initial_strong_signs"] == 40
    assert structural["medial_strong_signs"] == 61
    assert structural["terminal_strong_signs"] == 20
    assert "Consistent with BOTH Hunt model" in positional["verdict"]
    # The Phase-43 record carries the same class counts.
    phase43 = json.loads(PHASE43.read_text(encoding="utf-8"))
    table = phase43["T2_2_terminal_suffix_table"]
    assert table["initial_strong_count"] == 40
    assert table["medial_strong_count"] == 61
    assert table["terminal_strong_count"] == 20
    assert table["total_signs_profiled"] == 201
    assert len(table["terminal_strong"]) == 10
    # The crosswalk census: 205 rows, 187 distinct sign
    # keys - the full sign universe of DD-045-18.
    with CROSSWALK.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 205
    assert len({r["registry_sign_id"] for r in rows}) == 187
    # The corpus layer carries its recorded row count.
    with CORPUS.open(encoding="utf-8") as fh:
        corpus_rows = list(csv.DictReader(fh))
    assert len(corpus_rows) == 5679
    # The anchors file carries its recorded census.
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    assert anchors["total"] == 287
    assert len(anchors["anchors"]) == 287
    # The Phase-104 record: UNTESTED under RULE-CLASS.
    phase104 = json.loads(PHASE104.read_text(encoding="utf-8"))
    entry = _find_claim(phase104, CLAIM_ID)
    assert entry is not None
    assert entry["verdict"] == "stays_untested"
    assert entry["rule"] == "RULE-CLASS"
    assert "Celestial signs" in entry["normalized_claim"]
    assert "celestial sign class" in entry["reason"]
    # Spec 045's frozen record: the contract anchor replays,
    # and its coverage ruling carries the consequence for
    # this spec's gate 0.3.
    spec045_freeze = json.loads(
        SPEC045_FREEZE.read_text(encoding="utf-8")
    )
    assert spec045_freeze["digest"] == SPEC045_FREEZE_DIGEST
    assert "does not close INVALID" in (
        spec045_freeze["definition"]["design"][
            "coverage_consequence_for_spec050"
        ]
    )


def _verdict(ratio: float, fisher_pass: bool, half_met: bool) -> str:
    """The spec section 4.3 mapping, restated for the totality check."""
    if ratio <= 1.0:
        return "NOT SUPPORTED"
    if ratio >= 1.5 and fisher_pass and half_met:
        return "SUPPORTED"
    return "INCONCLUSIVE"


def test_verdict_mapping_is_total():
    outcomes = {
        _verdict(r, f, h)
        for r in (0.9, 1.0, 1.2, 1.5, 1.6)
        for f in (True, False)
        for h in (True, False)
    }
    assert outcomes == {"SUPPORTED", "NOT SUPPORTED", "INCONCLUSIVE"}
    assert _verdict(1.6, True, True) == "SUPPORTED"
    assert _verdict(1.5, True, True) == "SUPPORTED"
    assert _verdict(1.0, True, True) == "NOT SUPPORTED"
    assert _verdict(0.9, True, True) == "NOT SUPPORTED"
    assert _verdict(1.2, True, True) == "INCONCLUSIVE"
    assert _verdict(1.6, False, True) == "INCONCLUSIVE"
    assert _verdict(1.6, True, False) == "INCONCLUSIVE"


FREEZE_STAMPS = [
    "20261021T110847Z",
    "20261021T110850Z",
    "20261021T110852Z",
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
                encoding="utf-8"
            )
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
