"""Adversarial tests for the freeze gate (red-team finding D-1, 2026-10-25).

The 2026-10-25 programme red team demonstrated that a fully
fabricated freeze record set passed C4 with exit 0: a C1 record
claiming the opposite of the battery's determinations, a C2
record whose "agree" statuses were never compared against the
filed values (the one real gate-turning quantity relabelled and
unsampled), and a C3 record omitting the verdict-bearing claim
with an empty verifier and no evidence refs. Each fabrication
below must now FAIL, for the named reason. The honest fixture
must still pass (test_freeze_gate.py covers it).

Run: python -m pytest tools/freeze-gate/tests/ -q
"""

import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from check_freeze_gate import check_spec_dir  # noqa: E402

FIXTURES = HERE / "demo" / "fixtures"


def _copy(tmp_path):
    d = tmp_path / "spec"
    shutil.copytree(FIXTURES / "complete", d)
    return d


def _rewrite(spec_dir, name, mutate):
    path = spec_dir / "gate-records" / name
    rec = json.loads(path.read_text())
    mutate(rec)
    path.write_text(json.dumps(rec))
    return rec


def test_c1_claiming_opposite_determinations_fails(tmp_path):
    d = _copy(tmp_path)
    _rewrite(d, "c1-battery-result.json",
             lambda r: r["cases"][0].update({"flagged": True, "blind_spot": ""}))
    problems = check_spec_dir(d)
    assert any("canonical battery result" in p for p in problems), problems


def test_c2_agree_with_different_values_fails(tmp_path):
    d = _copy(tmp_path)
    _rewrite(d, "c2-spotcheck.json",
             lambda r: r["quantities"][0].update({"recomputed_value": 999999}))
    problems = check_spec_dir(d)
    assert any("does not equal pinned_value" in p for p in problems), problems


def test_c2_missing_recomputed_value_fails(tmp_path):
    d = _copy(tmp_path)
    _rewrite(d, "c2-spotcheck.json",
             lambda r: r["quantities"][0].pop("recomputed_value"))
    problems = check_spec_dir(d)
    assert any("recomputed_value is missing" in p for p in problems), problems


def test_c2_no_gate_turning_quantity_fails(tmp_path):
    d = _copy(tmp_path)

    def mutate(r):
        for q in r["quantities"]:
            q["gate_turning"] = False
        r["coverage"].update({"gate_turning_total": 0, "gate_turning_checked": 0,
                              "other_total": 2, "other_sampled": 2, "other_checked": 2})
    _rewrite(d, "c2-spotcheck.json", mutate)
    problems = check_spec_dir(d)
    assert any("no gate-turning quantity" in p for p in problems), problems


def test_c3_empty_verifier_and_refs_fail(tmp_path):
    d = _copy(tmp_path)

    def mutate(r):
        r["verifier"] = ""
        r["claims"][0]["evidence_refs_checked"] = []
    _rewrite(d, "c3-evidence-sample.json", mutate)
    problems = check_spec_dir(d)
    assert any("verifier is empty" in p for p in problems), problems
    assert any("evidence_refs_checked is empty" in p for p in problems), problems


def test_c3_verifier_equal_to_drafter_fails(tmp_path):
    d = _copy(tmp_path)
    _rewrite(d, "c3-evidence-sample.json",
             lambda r: r.update({"verifier": "fixture drafter"}))
    problems = check_spec_dir(d)
    assert any("same identity as the C2 drafter" in p for p in problems), problems


def test_c3_omitting_a_registered_claim_fails(tmp_path):
    d = _copy(tmp_path)
    # give the spec a register with both fixture claims, then drop
    # the verdict-bearing one from the record (the D-1 fabrication)
    (d / "claims.json").write_text(json.dumps(
        {"claims": [{"id": "FX-C01"}, {"id": "FX-C02"}]}))
    _rewrite(d, "c3-evidence-sample.json",
             lambda r: r.update({"claims": [c for c in r["claims"]
                                            if c["claim_id"] != "FX-C01"]}))
    problems = check_spec_dir(d)
    assert any("missing from the record" in p for p in problems), problems


def test_complete_fixture_with_register_still_passes(tmp_path):
    d = _copy(tmp_path)
    (d / "claims.json").write_text(json.dumps(
        {"claims": [{"id": "FX-C01"}, {"id": "FX-C02"}]}))
    assert check_spec_dir(d) == []
