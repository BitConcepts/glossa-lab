"""Tests for the correctness-bearing freeze gate machinery (C1–C5).

Run: python -m pytest tools/freeze-gate/tests/ -q
Stdlib + pytest only; no corpus, no network, no evaluator binary
needed (the battery runner is exercised through its result schema,
not by running the evaluator).
"""

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from check_freeze_gate import check_spec_dir  # noqa: E402
from freeze_records import scaffold_c2, scaffold_c3, validate_c2, validate_c3  # noqa: E402

FIXTURES = HERE / "demo" / "fixtures"


def test_complete_fixture_passes():
    assert check_spec_dir(FIXTURES / "complete") == []


def test_missing_c1_fails():
    problems = check_spec_dir(FIXTURES / "missing-c1")
    assert any("C1" in p and "missing" in p for p in problems)


def test_missing_c2_fails():
    problems = check_spec_dir(FIXTURES / "missing-c2")
    assert any("C2" in p and "missing" in p for p in problems)


def test_missing_c3_fails():
    problems = check_spec_dir(FIXTURES / "missing-c3")
    assert any("C3" in p and "missing" in p for p in problems)


def test_unresolved_gate_turning_mismatch_fails():
    problems = check_spec_dir(FIXTURES / "unresolved-c2")
    assert any("UNRESOLVED MISMATCH" in p for p in problems)


def test_unverified_verdict_bearing_claim_fails():
    problems = check_spec_dir(FIXTURES / "unverified-c3")
    assert any("UNVERIFIED verdict-bearing" in p for p in problems)


def test_stale_evaluator_battery_fails(tmp_path):
    import shutil
    d = tmp_path / "spec"
    shutil.copytree(FIXTURES / "complete", d)
    rec_path = d / "gate-records" / "c1-battery-result.json"
    rec = json.loads(rec_path.read_text())
    rec["evaluator_version"] = "0.0.0"
    rec_path.write_text(json.dumps(rec))
    problems = check_spec_dir(d)
    assert any("not the current evaluator" in p for p in problems)


def test_unflagged_case_without_blind_spot_fails(tmp_path):
    import shutil
    d = tmp_path / "spec"
    shutil.copytree(FIXTURES / "complete", d)
    rec_path = d / "gate-records" / "c1-battery-result.json"
    rec = json.loads(rec_path.read_text())
    rec["cases"][0]["blind_spot"] = ""
    rec_path.write_text(json.dumps(rec))
    problems = check_spec_dir(d)
    assert any("names no blind spot" in p for p in problems)


def test_c2_scaffold_samples_gate_turning_and_quarter_of_rest():
    quantities = [{"name": f"g{i}", "source_in_spec": "§1", "gate_turning": True, "pinned_value": i} for i in range(2)]
    quantities += [{"name": f"r{i}", "source_in_spec": "§2", "gate_turning": False, "pinned_value": i} for i in range(20)]
    rec = scaffold_c2("specs/x", "drafter", "recomputer", quantities, seed=7)
    sampled_rest = [q for q in rec["quantities"] if not q["gate_turning"] and q["sampled"]]
    assert all(q["sampled"] for q in rec["quantities"] if q["gate_turning"])
    assert len(sampled_rest) == 5  # 25% of 20, above the minimum of 3
    assert rec["outcome"] == "INCOMPLETE"
    # an untouched scaffold must NOT validate as a passing record
    assert validate_c2(rec) != []


def test_c2_scaffold_minimum_three():
    quantities = [{"name": "g", "source_in_spec": "§1", "gate_turning": True, "pinned_value": 1}]
    quantities += [{"name": f"r{i}", "source_in_spec": "§2", "gate_turning": False, "pinned_value": i} for i in range(4)]
    rec = scaffold_c2("specs/x", "d", "r", quantities, seed=7)
    sampled_rest = [q for q in rec["quantities"] if not q["gate_turning"] and q["sampled"]]
    assert len(sampled_rest) == 3  # minimum 3 governs over 25% of 4 = 1


def test_c3_scaffold_marks_verdict_bearing_and_sample(tmp_path):
    bundle = {"claims": [{"id": f"C{i}"} for i in range(1, 12)]}
    claims_path = tmp_path / "claims.json"
    claims_path.write_text(json.dumps(bundle))
    rec = scaffold_c3("specs/x", str(claims_path), ["C1", "C2"], seed=7)
    by_id = {c["claim_id"]: c for c in rec["claims"]}
    assert by_id["C1"]["sampled"] and by_id["C2"]["sampled"]
    sampled_rest = [c for c in rec["claims"] if not c["verdict_bearing"] and c["sampled"]]
    assert len(sampled_rest) >= 2  # at least 20% of the 9 remaining
    assert rec["verification_mode"] == "on"
    assert validate_c3(rec) != []  # pending verifications do not validate


def test_battery_manifest_covers_four_cases():
    manifest = json.loads((HERE / "battery" / "cases.json").read_text())
    assert {c["id"] for c in manifest["cases"]} == {"i", "ii", "iii", "iv"}
    for c in manifest["cases"]:
        assert (HERE / "battery" / c["dir"] / c["input"]).exists()
        assert (HERE / "battery" / c["dir"] / "DEFECT.md").exists()
        assert c["blind_spot_if_unflagged"].strip()
