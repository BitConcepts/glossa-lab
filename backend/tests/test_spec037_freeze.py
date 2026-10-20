"""Spec 037 draft freeze fences (CISI 3.1 concordance).

Pins: (1) the draft machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the design
constants exactly as drafted (the 693-candidate
census and its section split, the ladder's outcome
classes and reason codes, the 20 percent halt
rule, the Phase-130 gate pins, the portion and
corpus_master hashes); (3) the governed claim
register is the draft register (15 claims,
integrity-clean, hooks not run - the hooks are a
freeze gate); (4) the cited in-repo records still
carry the facts the design rests on (the
corpus_master pin and census; the Spec 031 outcome
record's Q7 closure figures the annex fence
cites). The restricted material itself is NOT in
the repository and is never read by these tests:
the gate and census facts about it are pinned
through the definition constants, not through the
portion. These tests build no join, grade no
candidate, and extract nothing.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/037-cisi31-concordance-spine"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CORPUS_MASTER = REPO / "data/normalized/corpus_master.csv"
SPEC031_OUTCOME = (
    REPO
    / "specs/031-stage2-q7-provenance-networks/outcome.md"
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
        "spec037-cisi31-concordance-spine"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.5-draft"
    assert "NOT RUN" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-401"
    pilot = design["pilot"]
    assert pilot["candidates"] == 693
    assert pilot["candidate_split_by_section"] == {
        "mohenjo_daro": 289,
        "harappa_old": 102,
        "harappa_harp": 302,
    }
    assert pilot["outcome_classes"] == [
        "VERIFIED", "CONFLICT", "UNRESOLVED",
    ]
    assert "NUMBER-AMBIGUOUS" in pilot["conflict_reason_codes"]
    assert pilot["halt_rule"]["conflict_share_cap"] == 0.2
    assert "SPINE HALTED" in pilot["halt_rule"]["on_halt"]
    fences = design["fences"]
    assert "never a join" in fences["string_match"]
    assert "no sign transcriptions" in fences["no_pred_scoring"]
    assert "NOT-YET-TESTABLE" in fences["q7"]
    assert "no execution order" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["portion_pdf"]["sha256"] == (
        "514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a"
    )
    assert inputs["portion_pdf"]["bytes"] == 8206446
    assert inputs["local_table"]["records"] == 2123
    assert inputs["local_table"][
        "distinct_catalogue_numbers"] == 2101
    assert inputs["local_table"]["sections"] == {
        "mohenjo_daro": 519,
        "harappa_old": 510,
        "harappa_harp": 1094,
    }
    assert inputs["corpus_master"]["sha256"] == (
        "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
    )
    assert "entry 22" in inputs["gate"]["record"]
    assert "nothing derived enters git" in (
        inputs["gate"]["classification"])


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.5-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F037-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    # corpus_master: the pin and census the key
    # inventory and the candidate count rest on.
    digest = hashlib.sha256(
        CORPUS_MASTER.read_bytes()).hexdigest()
    assert digest == (
        "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
    )
    lines = CORPUS_MASTER.read_text(
        encoding="utf-8").splitlines()
    assert len(lines) == 2723  # header + 2,722 rows
    header = lines[0].split(",")
    for key in (
        "source_object_id", "site", "artifact_type",
        "source_name",
    ):
        assert key in header
    # The Spec 031 record the annex fence cites:
    # Q7 closed at the margins step, both arms'
    # verdicts as the fence states them.
    outcome031 = SPEC031_OUTCOME.read_text(encoding="utf-8")
    assert "NOT-YET-TESTABLE" in outcome031
    assert "NOT ESTIMABLE" in outcome031
