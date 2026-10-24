"""Spec 054 freeze fences (Yadav opening/closing
signs: the amended falsifier act under NB-1).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the amended statement, battery
NB-1 (floor 20; bands 2/3 and 1/2), the two arms,
the decision procedure (per-class reappearance at
>= 1/2, DD-054-5 denominators, the 999-shuffle
label-permutation null at seed 44054, DD-054-2's
precedence in the amendment section 5.5 order),
the step-0 gate set, the falsifier append with its
exact text, Phase-437, and the unsatisfied
execution gate; (3) the governed claim register is
the frozen register (19 claims, integrity-clean,
recovered to 0.8-draft at the freeze gate) and the
three freeze-hook artifacts record the pass on the
DD-054-9 reading (zero correctness failure modes;
only FR-2.3 draft-cap records; no claim below the
0.70 threshold); (4) the cited records still carry
the facts the design rests on (the claim store at
its post-append pin, with the appended falsifier
verbatim and manual_001's condition intact; the
Phase-43 counts and its ten exhibited terminal
entries; the crosswalk pins and counts; the
anchors pin). These tests compute no positional
quantity, count no arm, and change no record.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/054-yadav-opening-closing"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CLAIM_STORE = (
    REPO
    / "glossa-indus/claims/extracted_claims"
    / "yadav_2009_arxiv.json"
)
PHASE43 = REPO / "outputs/phase43_all.json"
HUNT = (
    REPO
    / "glossa-indus/analysis/positional"
    / "hunt_tripartite_test.json"
)
CROSSWALK_JSON = (
    REPO / "data/crosswalks/parpola_mahadevan_crosswalk_v1.json"
)
CROSSWALK_CSV = (
    REPO / "data/crosswalks/parpola_mahadevan_crosswalk_v1.csv"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

CLAIM_STORE_SHA256_BEFORE = (
    "904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3"
)
CLAIM_STORE_SHA256_AFTER = (
    "dcbaf64a728bc4ff7a0a1f76f2c867f924734cbe7f9c8cab2554d131b22533d7"
)
PHASE43_SHA256 = (
    "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4"
)
HUNT_SHA256 = (
    "0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48"
)
CROSSWALK_JSON_SHA256 = (
    "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb"
)
CROSSWALK_CSV_SHA256 = (
    "3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
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
        "spec054-yadav-opening-closing"
    )
    assert definition["register"]["claims"] == 19
    assert definition["register"]["register_version"] == "0.8-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    assert "DD-054-9" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-437"
    # Battery NB-1, exactly as amended.
    battery = design["battery"]
    assert battery["name"] == "NB-1"
    assert battery["floor"] == 20
    assert battery["bands"] == {
        "STRONG": ">= 2/3",
        "MODERATE": ">= 1/2",
    }
    assert battery["opening_strong"] == "INITIAL_STRONG"
    assert battery["closing_strong"] == "TERMINAL_STRONG"
    assert "I + T + M = N" in battery["classes"]
    # The decision procedure.
    decision = design["decision"]
    assert ">= 1/2" in decision["reappearance"]
    assert "DD-054-5" in decision["denominators"]
    assert "TOO THIN / UNMAPPED / CONFLICT" in (
        decision["denominators"]
    )
    null = decision["null"]
    assert null["shuffles"] == 999
    assert null["seed"] == 44054
    assert "95th percentile" in null["chance_level"]
    assert "label permutation" in null["construction"]
    assert len(decision["precedence"]) == 3
    assert "NOT SUPPORTED" in decision["precedence"][0]
    assert "SUPPORTED" in decision["precedence"][1]
    assert "INCONCLUSIVE" in decision["precedence"][2]
    # The step-0 gates stand as a set.
    gates = design["step0_gates"]
    assert any("STRICT CORPUS NOT PINNABLE" in g for g in gates)
    assert any(g == "TOO THIN" for g in gates)
    assert any("SECOND ARM NOT RUNNABLE" in g for g in gates)
    assert any("determinism" in g for g in gates)
    # The falsifier append is registered with its pins.
    falsifier = design["falsifier"]
    assert falsifier["claim"] == "yadav_2009_arxiv_manual_002"
    inputs = definition["inputs"]
    store = inputs["claim_store"]
    assert store["sha256_before_append"] == CLAIM_STORE_SHA256_BEFORE
    assert store["sha256_after_append"] == CLAIM_STORE_SHA256_AFTER
    assert inputs["phase43"]["sha256"] == PHASE43_SHA256
    assert inputs["crosswalk"]["json_sha256"] == CROSSWALK_JSON_SHA256
    assert inputs["crosswalk"]["csv_sha256"] == CROSSWALK_CSV_SHA256
    assert inputs["crosswalk"]["mapped_pairs"] == 762
    assert inputs["crosswalk"]["conflict_pairs"] == 383
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    # No RE-EARNED survives in the amended wordings fence.
    assert "RE-EARNED" in design["verdict_wordings"]
    assert "appears in no amended wording" in (
        design["verdict_wordings"]
    )
    # The execution gate is not satisfied by the freeze.
    assert "NOT satisfied" in design["execution_gate"]
    assert "no execution order" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.8-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F054-C{i:02d}" for i in range(1, 20)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["observed_at"]
            assert item["independent_of"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_freeze_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase in ("after_specify", "after_plan", "after_tasks"):
        files = sorted(aee_dir.glob(f"evaluator-aee-{phase}-*.json"))
        assert len(files) == 1
        result = json.loads(files[0].read_text(encoding="utf-8"))
        assert "0 claim(s) below the 0.70" in result["summary"]
        assert all(
            "DRAFT-CAP" in f["id"] for f in result["findings"]
        )
        assert len(result["findings"]) == 19


def test_cited_records_carry_the_design_facts():
    # The claim store at its post-append pin, the
    # appended falsifier verbatim, the note present,
    # and manual_001's authored condition intact.
    store_bytes = CLAIM_STORE.read_bytes()
    assert hashlib.sha256(store_bytes).hexdigest() == (
        CLAIM_STORE_SHA256_AFTER
    )
    store = json.loads(store_bytes)
    by_id = {c["claim_id"]: c for c in store["claims"]}
    manual_002 = by_id["yadav_2009_arxiv_manual_002"]
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    frozen_text = record["definition"]["design"]["falsifier"]["text"]
    assert manual_002["falsification_condition"] == frozen_text
    assert "battery NB-1" in manual_002["falsification_condition"]
    assert "(§5.5)" in manual_002["falsification_condition"]
    note = manual_002["spec054_falsifier_append_2026_10_23"]
    assert note["date"] == "2026-10-23"
    assert "never appended" in note["note"]
    assert manual_002["claim_status"] == "strongly_supported"
    assert manual_002["stage"] == "explained"
    manual_001 = by_id["yadav_2009_arxiv_manual_001"]
    assert manual_001["falsification_condition"] == (
        "If frequency distribution deviates from "
        "Zipf-Mandelbrot law."
    )
    # The Phase-43 record at its pin, with the counts
    # and the ten exhibited terminal entries.
    phase43_bytes = PHASE43.read_bytes()
    assert hashlib.sha256(phase43_bytes).hexdigest() == PHASE43_SHA256
    phase43 = json.loads(phase43_bytes)
    t2 = phase43["T2_2_terminal_suffix_table"]
    assert t2["terminal_strong_count"] == 20
    assert t2["initial_strong_count"] == 40
    assert t2["medial_strong_count"] == 61
    assert t2["total_signs_profiled"] == 201
    assert len(t2["terminal_strong"]) == 10
    # The companion positional record at its pin.
    hunt_bytes = HUNT.read_bytes()
    assert hashlib.sha256(hunt_bytes).hexdigest() == HUNT_SHA256
    # The crosswalk at its pins, with its counts
    # re-derived from the pinned file.
    xw_bytes = CROSSWALK_JSON.read_bytes()
    assert hashlib.sha256(xw_bytes).hexdigest() == (
        CROSSWALK_JSON_SHA256
    )
    assert hashlib.sha256(CROSSWALK_CSV.read_bytes()).hexdigest() == (
        CROSSWALK_CSV_SHA256
    )
    rows = json.loads(xw_bytes)["rows"]
    assert len(rows) == 766
    mapped = [r for r in rows if r["relation_type"] != "unmapped"]
    assert len(mapped) == 762
    assert sum(1 for r in rows if r["conflict"] is True) == 383
    # The anchors file at its pin.
    anchors_bytes = ANCHORS.read_bytes()
    assert hashlib.sha256(anchors_bytes).hexdigest() == ANCHORS_SHA256
    assert len(anchors_bytes) == 570344


FREEZE_STAMPS = [
    "20261024T033510Z",
    "20261024T033516Z",
    "20261024T033520Z",
]
