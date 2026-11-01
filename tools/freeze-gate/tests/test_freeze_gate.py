"""Tests for the correctness-bearing freeze gate machinery (C1–C5).

Run: python -m pytest tools/freeze-gate/tests/ -q
Stdlib + pytest only; no corpus, no network, no evaluator binary
needed (the battery runner is exercised through its result schema,
not by running the evaluator).
"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import check_freeze_gate  # noqa: E402
from check_freeze_gate import check_spec_dir, pr_scope_dirs  # noqa: E402
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


# --- --pr-scope population (gate-records regime) -------------------
# pr_scope_dirs shells to git, so these tests build temp git repos
# and point check_freeze_gate.REPO_ROOT at them.


def _git(repo, *args):
    subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    )


def _write(repo, rel, content):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _commit_all(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    out = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo,
        check=True, capture_output=True, text=True,
    )
    return out.stdout.strip()


def _spec_repo(tmp_path, monkeypatch, base_files):
    """Temp git repo with one base commit carrying base_files;
    returns (repo, base_sha) with REPO_ROOT pointed at the repo."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "freeze-gate-tests@example.invalid")
    _git(repo, "config", "user.name", "Freeze Gate Tests")
    _git(repo, "config", "commit.gpgsign", "false")
    for rel, content in base_files.items():
        _write(repo, rel, content)
    base = _commit_all(repo, "base")
    monkeypatch.setattr(check_freeze_gate, "REPO_ROOT", repo)
    return repo, base


def test_pr_scope_skips_pre_regime_freeze_change(tmp_path, monkeypatch):
    # framework026-regime shape: freeze.json, no gate-records/ at
    # base or in the tree. A freeze.json recompute must NOT select
    # the dir (the PR #477 false positive).
    repo, base = _spec_repo(tmp_path, monkeypatch, {
        "specs/054-pre-regime/freeze.json": "{}\n",
        "specs/054-pre-regime/adjudication.md": "record\n",
    })
    _write(repo, "specs/054-pre-regime/freeze.json", '{"recomputed": true}\n')
    _commit_all(repo, "recompute freeze")
    assert pr_scope_dirs(base) == []


def test_pr_scope_selects_regime_freeze_change(tmp_path, monkeypatch):
    repo, base = _spec_repo(tmp_path, monkeypatch, {
        "specs/075-regime/freeze.json": "{}\n",
        "specs/075-regime/gate-records/c2-spotcheck.json": "{}\n",
    })
    _write(repo, "specs/075-regime/freeze.json", '{"recomputed": true}\n')
    _commit_all(repo, "recompute freeze")
    assert pr_scope_dirs(base) == [repo / "specs/075-regime"]


def test_pr_scope_selects_regime_gate_records_deletion(tmp_path, monkeypatch):
    # Deleting a regime spec's gate-records/ must stay in scope so
    # check_spec_dir fails it — the base-ref arm of the regime
    # test carries this case (the dir is gone from the tree).
    repo, base = _spec_repo(tmp_path, monkeypatch, {
        "specs/075-regime/freeze.json": "{}\n",
        "specs/075-regime/gate-records/c2-spotcheck.json": "{}\n",
    })
    records = repo / "specs/075-regime/gate-records"
    (records / "c2-spotcheck.json").unlink()
    records.rmdir()
    _commit_all(repo, "delete gate-records")
    assert not records.exists()
    assert pr_scope_dirs(base) == [repo / "specs/075-regime"]


def test_pr_scope_ignores_non_trigger_change(tmp_path, monkeypatch):
    repo, base = _spec_repo(tmp_path, monkeypatch, {
        "specs/075-regime/freeze.json": "{}\n",
        "specs/075-regime/gate-records/c2-spotcheck.json": "{}\n",
        "specs/075-regime/adjudication.md": "record\n",
    })
    _write(repo, "specs/075-regime/adjudication.md", "record, appended\n")
    _commit_all(repo, "append adjudication")
    assert pr_scope_dirs(base) == []


def test_pr_scope_477_shape_selects_nothing(tmp_path, monkeypatch):
    # The PR #477 shape end to end: freeze.json recomputed for two
    # pre-regime specs (054/074-style append acts), nothing else.
    repo, base = _spec_repo(tmp_path, monkeypatch, {
        "specs/054-a/freeze.json": "{}\n",
        "specs/074-b/freeze.json": "{}\n",
    })
    _write(repo, "specs/054-a/freeze.json", '{"recomputed": true}\n')
    _write(repo, "specs/074-b/freeze.json", '{"recomputed": true}\n')
    _commit_all(repo, "recompute freezes")
    assert pr_scope_dirs(base) == []
