"""Spec 045 freeze fences (Hunt depicted kinds; builder of Asset A).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source, with the covered-source set exact);
(2) the definition carries the frozen contract
exactly - Phase-411, the fit form with the
0.05 margin and its recorded derivation
(DD-045-11), the AUC comparison rule
(DD-045-12), the pooling threshold of 5
(DD-045-13), the jurisdiction coding rule
(DD-045-14), the D-18 consumption repair
(DD-045-17: the total frozen vocabulary with
PARTIAL CONCURRENCE, the CLOSED AT STEP 0
closure delivery, and the null-key
disposition), Spec 046's two producer
digests (DD-045-21), the full-crosswalk
coverage scope with its census and the
Spec 050 consequence (DD-045-18), and the
two distinctly named closing measures
(DD-045-19); (3) the governed claim register
is the frozen register (17 claims,
integrity-clean, recovered to 0.8-draft at
the freeze gate) and the three freeze-hook
artifacts record the pass on the DD-045-9
reading (zero correctness failure modes;
only FR-2.3 draft-cap records; no claim
below the 0.70 threshold); (4) the cited
records still carry the facts the design
rests on (the section 4 pins asserted as
freeze-time facts against the definition;
the live records checked for their design
facts - the positional quantities, the
Phase-43 class counts, the crosswalk census
of 205 rows and 187 distinct sign keys, the
corpus row count, and the anchors census);
(5) the section 5.4 verdict mapping is total
over every comparison pattern. These tests
classify no sign, build no part of Asset A,
fit no model, and change no record.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/045-hunt-depicted-kinds"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
POSITIONAL = (
    REPO / "glossa-indus/analysis/positional/hunt_tripartite_test.json"
)
PHASE43 = REPO / "outputs/phase43_all.json"
CORPUS = REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

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
}

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
        "specs/045-hunt-depicted-kinds/freeze.md",
        "specs/045-hunt-depicted-kinds/spec.md",
        "specs/045-hunt-depicted-kinds/claims.json",
        "specs/045-hunt-depicted-kinds/adjudication.md",
        "specs/045-hunt-depicted-kinds/aee/freeze-aee-note.md",
        "specs/045-hunt-depicted-kinds/build_freeze.py",
        "backend/tests/test_spec045_freeze.py",
    }


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == "spec045-hunt-depicted-kinds"
    assert definition["register"]["claims"] == 17
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-411"
    assert design["claim_id"] == (
        "without_kings_or_conquests_the_indus_scr_"
        "ce9d98cc_manual_001"
    )
    # Asset A is a contract at the freeze, not a built asset.
    asset = design["asset_a"]
    assert "187" in asset["form"] and "205" in asset["form"]
    assert "NOT built at this freeze" in asset["form"]
    # The D-18 consumption repair (DD-045-17) and the
    # producer digests (DD-045-21).
    d18 = design["d18_consumption"]
    assert "PARTIAL CONCURRENCE" in d18["vocabulary"]
    assert "not changed" in d18["vocabulary"]
    assert "never presented as consensus" in d18["partial_concurrence"]
    assert "CLOSED AT STEP 0" in d18["closures"]
    assert "empty signs array" in d18["closures"]
    assert "not rejected" in d18["null_key_disposition"]
    assert "unattached D-18 input" in d18["null_key_disposition"]
    digests = d18["producer_digests"]
    assert digests["freeze_act"] == (
        "80c3be31e5af5236f71cb2c1894b2946f9b8ad47b"
        "12bdeab9d03cd76468af405"
    )
    assert digests["successor"] == (
        "e0d7add84b9d28ae5f6a6b392dca578b727ad4d99"
        "a117360a57d39f3b94b01c6"
    )
    assert "osf.io/dnts8" in digests["note"]
    # The frozen test form (DD-045-11 to DD-045-14).
    test = design["test"]
    assert test["fit_margin"] == 0.05
    assert "0.506" in test["margin_derivation"]
    assert "0.757" in test["margin_derivation"]
    assert "AUC" in test["comparison_rule"]
    assert "strictly greater" in test["comparison_rule"]
    assert test["pooling_threshold"] == 5
    assert "verbatim label alone" in test["jurisdiction_rule"]
    # The two closing measures are different and distinctly
    # named (DD-045-19; Spec 054's OPEN-054-6 mirror).
    assert "closing distinct-predecessor rate" in (
        test["closing_measure_spec045"]
    )
    assert "Phase-43 terminal-strong set membership" in (
        test["closing_measure_spec054"]
    )
    assert "DIFFERENT measure" in test["closing_measure_spec054"]
    assert "OPEN-054-6" in test["closing_measure_spec054"]
    # The Spec 050 coverage consequence (DD-045-18).
    assert "does not close INVALID" in (
        design["coverage_consequence_for_spec050"]
    )
    assert "DD-045-16" in design["spot_check"]
    # Inputs: the five section 4 pins.
    inputs = definition["inputs"]
    assert inputs["positional_record"]["sha256"] == PINS[POSITIONAL]
    assert inputs["phase43_record"]["sha256"] == PINS[PHASE43]
    assert inputs["corpus_layer"]["sha256"] == PINS[CORPUS]
    assert inputs["corpus_layer"]["rows"] == 5679
    assert inputs["crosswalk_master"]["sha256"] == PINS[CROSSWALK]
    assert inputs["crosswalk_master"]["rows"] == 205
    assert inputs["crosswalk_master"]["distinct_sign_keys"] == 187
    assert inputs["anchors"]["sha256"] == PINS[ANCHORS]
    assert inputs["anchors"]["anchors"] == 287
    # The execution gate is NOT satisfied at the freeze.
    assert "NOT satisfied at the freeze" in design["execution_gate"]
    assert "Asset A does not exist" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F045-C{i:02d}" for i in range(1, 18)
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


def test_cited_records_carry_the_design_facts():
    # The section 4 pins are freeze-time facts: they are
    # asserted against freeze.json's definition in
    # test_freeze_definition_constants, and the step-0
    # pin check is an execution-time act over a pristine
    # checkout (spec section 6, gate 0.1). Live byte
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
    assert structural["mean_i_rate_of_initial_signs"] == 0.757
    assert structural["expected_i_by_chance"] == 0.251
    # The margin derivation recomputes from these live
    # facts: 0.757 - 0.251 = 0.506, one tenth 0.0506,
    # frozen as 0.05 (DD-045-11).
    advantage = (
        structural["mean_i_rate_of_initial_signs"]
        - structural["expected_i_by_chance"]
    )
    assert abs(advantage - 0.506) < 1e-9
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
    # keys - the full sign universe of gate A3 (DD-045-18).
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


def _verdict(margin_met: bool, kind_beats_suffix: bool) -> str:
    """The spec section 5.4 mapping, restated for the totality check."""
    if margin_met and kind_beats_suffix:
        return "DISCRIMINATED FOR HUNT"
    if not margin_met and not kind_beats_suffix:
        return "DISCRIMINATED FOR THE GRAMMAR ACCOUNT"
    return "NOT DISCRIMINATED"


def test_verdict_mapping_is_total():
    outcomes = {
        _verdict(m, k) for m in (True, False) for k in (True, False)
    }
    assert outcomes == {
        "DISCRIMINATED FOR HUNT",
        "DISCRIMINATED FOR THE GRAMMAR ACCOUNT",
        "NOT DISCRIMINATED",
    }
    assert _verdict(True, True) == "DISCRIMINATED FOR HUNT"
    assert _verdict(False, False) == (
        "DISCRIMINATED FOR THE GRAMMAR ACCOUNT"
    )
    assert _verdict(True, False) == "NOT DISCRIMINATED"
    assert _verdict(False, True) == "NOT DISCRIMINATED"


FREEZE_STAMPS = [
    "20261021T104300Z",
    "20261021T104303Z",
    "20261021T104305Z",
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
