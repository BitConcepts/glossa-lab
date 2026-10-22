"""Spec 039 freeze fences (gazetteer period assignment).

Pins: (1) the draft machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the decided
contract exactly - the owner's Option 1 evidence
standard (published period determinations only, no
program-derived assignments), the recommended label
set (Early / Mature / Late Harappan, DD-039-1), the
no-majority-vote posture with Spec 030 Ask 2
RESERVED, the append-only outputs, the margins
verification step confined to the period-eligibility
gate, the D-25 bundle, and the Masudpur recommended
default (DD-039-4: not in this act); (3) the governed
claim register is the frozen register (15 claims,
integrity-clean, recovered to 0.7-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-039-8 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold); (4) the cited records still carry the
facts the design rests on (the gazetteer census and
pin; Spec 027's field contract and no-majority-vote
rule; Spec 031's frozen period rule F031-C10; the
Phase-395 margins record: 0 eligible sites, floors
8 / 10, in-universe link mass 2 sites / 1 pair).
These tests assign no period label, open no
restricted source, and change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/039-gazetteer-period-assignment"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
GAZETTEER = REPO / "data/movement/gazetteer_rows.jsonl"
SPEC027 = REPO / "specs/027-movement-culture-language/spec.md"
SPEC031 = REPO / "specs/031-stage2-q7-provenance-networks/spec.md"
PHASE395 = REPO / "reports/phase395_results.json"

GAZETTEER_SHA256 = (
    "5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6"
)

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
        "spec039-gazetteer-period-assignment"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-403"
    # The decided evidence standard, carried not softened.
    std = design["evidence_standard"]
    assert std["option"].startswith("Option 1")
    assert "Option 2" in std["no_program_derived"]
    assert "locator" in std["admissible"]
    # The decided label set (DD-039-1).
    assert design["label_set"]["labels"] == [
        "Early Harappan",
        "Mature Harappan",
        "Late Harappan",
    ]
    # The disagreement posture and the reserved question.
    dis = design["disagreement"]
    assert "no majority vote" in dis["posture"]
    assert "RESERVED" in dis["ask2_reserved"]
    assert "NOT DECIDED" in dis["ask2_reserved"]
    # The margins verification step's confinement.
    mv = design["margins_verification"]
    assert "only the period-eligibility" in mv["scope"]
    assert "not as a Q7 verdict" in mv["then_stated"]
    assert "NOT-YET-TESTABLE" in mv["never_reopened"]
    # The Masudpur recommended default (DD-039-4).
    assert "establishes no new sites" in design["masudpur"]["default"]
    assert "28" in design["masudpur"]["state"]
    # Inputs.
    inputs = definition["inputs"]
    gaz = inputs["gazetteer"]
    assert gaz["sha256"] == GAZETTEER_SHA256
    assert gaz["rows"] == 36
    assert gaz["program_sites"] == 30
    assert gaz["program_period_assignment_null_rows"] == 36
    p395 = inputs["phase395_margins"]
    assert p395["eligible_sites_at_margins"] == 0
    assert p395["floors"] == {
        "eligible_sites_min": 8,
        "linked_pairs_min": 10,
    }
    assert p395["linked_pairs_in_universe"] == 1
    assert len(p395["link_eligible_sites_in_gazetteer"]) == 2
    assert inputs["stage0_deposit"]["doi"] == "10.5281/zenodo.23300361"
    # The mapping table is frozen, with no other entries.
    entries = design["mapping_rule"]["entries"]
    assert set(entries) == {
        "MAP-EXPLICIT-EARLY", "MAP-EXPLICIT-MATURE",
        "MAP-EXPLICIT-LATE", "MAP-EXPLICIT-MULTI",
        "MAP-RANGE-EARLY-MATURE", "MAP-RANGE-MATURE-LATE",
        "MAP-RANGE-EARLY-LATE", "MAP-HARP-RAVI",
        "MAP-HARP-KOTDIJI", "MAP-HARP-HARAPPAN",
        "MAP-HARP-CEMETERY-H", "MAP-JHUKAR",
        "MAP-CEMETERY-H",
    }
    assert "Muse" in design["mapping_rule"]["reviewer"]
    # The execution gate is satisfied at the freeze;
    # no assignment was made by the freeze itself.
    assert "Satisfied at the freeze" in design["execution_gate"]
    assert "no period assignment was made" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F039-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # The gazetteer as it stands: pin, census, empty fields.
    raw_bytes = GAZETTEER.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == GAZETTEER_SHA256
    rows = [
        json.loads(line)
        for line in raw_bytes.decode("utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 36
    assert len({r["program_site_id"] for r in rows}) == 30
    assert all(
        r["program_period_assignment"] is None for r in rows
    )
    published = [r["period_label_as_published"] for r in rows]
    assert sum(1 for v in published if v is None) == 33
    assert sum(
        1 for v in published if v == ["PN", "Neo.?"]
    ) == 2
    assert sum(
        1 for v in published if v == ["PN", "Neo."]
    ) == 1
    # Spec 027's field contract and conflict rules.
    spec027 = " ".join(
        SPEC027.read_text(encoding="utf-8").split()
    )
    assert "program_period_assignment" in spec027
    assert "mapping rule and reviewer recorded" in spec027
    assert "No majority vote" in spec027
    # Spec 031's frozen period rule (F031-C10).
    spec031 = SPEC031.read_text(encoding="utf-8")
    assert "period-eligible iff" in spec031
    assert "Mature Harappan" in spec031
    assert "No finer temporal slicing" in spec031
    # The Phase-395 margins record: pin, floors, link mass.
    p395 = json.loads(PHASE395.read_text(encoding="utf-8"))
    assert (
        p395["input_hashes"]["data/movement/gazetteer_rows.jsonl"]
        == GAZETTEER_SHA256
    )
    pop = p395["population_record"]
    assert pop["link_eligible_sites_in_gazetteer"] == 2
    assert pop["linked_pairs_in_gazetteer"] == 1
    assert pop["arms"]["bead_craft"]["eligible_sites"] == 0
    assert pop["arms"]["ceramic"]["eligible_sites"] == 0


FREEZE_STAMPS = [
    "20261021T015329Z",
    "20261021T015331Z",
    "20261021T015334Z",
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
