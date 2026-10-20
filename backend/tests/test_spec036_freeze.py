"""Spec 036 freeze fences (PRED-2026-011 scoring).

Pins: (1) the machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the registered
criterion, the screened trained set, the step-0
closures, and the unmappable cap exactly as
registered (70% of trained signs at start rate 0.40
or above, which with 2 signs passes only at 2 of 2;
any unmappable trained sign closes the scoring as
CANNOT BE RUN AS WRITTEN); (3) the governed claim
register is the recovered register (15 claims,
integrity-clean, hooks passed at the freeze act); (4) the cited records still carry
the facts the design rests on (the derivation
record's screened and unscreened sets, censuses,
and pins; the PRED register entry; the crosswalk
coverage expectation: P217 -> Y0520 and P324 ->
Y0740 as best matches, P000 best-match absent).
These tests score nothing, open no withheld
content, and compute no start rate.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/036-pred-2026-011-scoring"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
DERIVATION = (
    REPO
    / "docs/research/pred-2026-011-registration/"
    "derivation-record.json"
)
PRED_REGISTER = REPO / "docs/PREDICTION_REGISTER.md"
CROSSWALK = (
    REPO / "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv"
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
        "spec036-pred-2026-011-scoring"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.9-draft"
    assert "PASS" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-400"
    assert design["trained_initial_set"] == ["P217", "P324"]
    crit = design["criterion"]
    assert crit["share_min"] == 0.7
    assert crit["start_rate_min"] == 0.4
    assert crit["trained_signs"] == 2
    assert "2 of 2" in crit["pass_structure"]
    # The closures and the cap must be carried, not softened.
    assert "CANNOT BE RUN AS WRITTEN" in (
        design["step0"]["failure_closure"])
    assert design["unmappable"]["cap"] == 0.2
    assert "CANNOT BE RUN AS WRITTEN" in (
        design["unmappable"]["over_cap_closure"])
    assert "not analyst blindness" in design["disclosure"]
    assert "execution order" in design["execution_gate"]
    assert design["mappability_screen"]["retained"] == ["P217", "P324"]
    assert design["osf_registration"]["id"] == "t6whq"
    assert design["osf_registration"]["doi"] == (
        "10.17605/OSF.IO/T6WHQ"
    )
    inputs = definition["inputs"]
    assert inputs["training_pool"]["sha256"] == (
        "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
    )
    assert inputs["training_pool"][
        "filtered_pool_manifest_sha256"
    ] == "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
    assert inputs["crosswalk"]["sha256"] == (
        "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
    )
    assert inputs["withheld"]["sha256"] == (
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
    )


def _claim_from_register(raw_claim: dict):
    """Load one frozen-register claim under aee >= 1.5.

    The frozen registers store ``boundary`` as a plain string (the
    pre-1.5 serialization). aee 1.5.0's strict bundle loader refuses
    a scalar where the model declares a list of strings, so the
    string is wrapped at load time; the frozen register bytes are
    never modified.
    """
    from aee.model import Claim

    claim = dict(raw_claim)
    if isinstance(claim.get("boundary"), str):
        claim["boundary"] = [claim["boundary"]]
    return Claim.from_dict(claim)


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.9-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F036-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [_claim_from_register(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_facts():
    derivation = json.loads(
        DERIVATION.read_text(encoding="utf-8"))
    assert derivation["mappability_screen"][
        "trained_initial_set"] == ["P217", "P324"]
    assert derivation["underlying_classification"][
        "unscreened_initial_set"] == ["P000", "P217", "P324"]
    assert derivation["underlying_classification"][
        "class_counts"] == {
        "INITIAL": 3, "MEDIAL": 19, "MIXED": 3, "TERMINAL": 3}
    assert derivation["training_pool"]["pool_rows"] == 179
    assert derivation["training_pool"][
        "yajnadevam_rows_in_pool"] == 0
    assert derivation["training_pool"]["file_sha256"] == (
        "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
    )
    assert derivation["training_pool"][
        "pool_manifest_sha256"
    ] == "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
    assert derivation["crosswalk_fixed_by_reference"][
        "file_sha256"
    ] == "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
    assert derivation["withheld_data_fixed_by_reference"][
        "file_sha256"
    ] == "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
    register = PRED_REGISTER.read_text(encoding="utf-8")
    assert "PRED-2026-011" in register
    assert "P217, P324" in register
    assert (
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
        in register
    )
    # The coverage expectation the design rests on
    # (spec section 0.4): best-match counterparts
    # for P217 and P324; P000 best-match absent.
    best: dict[str, list[str]] = {}
    rows = list(csv.DictReader(CROSSWALK.open(encoding="utf-8")))
    for row in rows:
        best.setdefault(row["best_parpola_match"], []).append(
            row["registry_sign_id_yajnadevam"])
    assert best.get("P217") == ["Y0520"]
    assert best.get("P324") == ["Y0740"]
    assert "P000" not in best
