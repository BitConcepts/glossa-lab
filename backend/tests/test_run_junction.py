"""Spec 089 Stage 3 — the junction tool (T301–T303).

The comparator's teeth, on tmp stores throughout (the
standing stores gain nothing in this stage — the last
test reads the standing settling store's records into a
tmp copy, read-only):

- an identical pair is listed identical: no report is
  written and the index is byte-unchanged;
- a divergent deterministic pair files a report whose
  first divergence is the seeded path, carries the
  red-team section with its six causes unmarked, and
  quarantines both runs by index act;
- a one-side-empty pair (result vs absence) localizes
  the divergence as the absence plus the first result
  present on the non-empty side;
- a constitutive-diff pair is not-comparable, with the
  differing component named, and writes nothing;
- the suite's registered shape #1 explains only with
  its evidence present: a teardown ERROR outside the
  sqlite family, a non-tray test id, or unequal pass
  counts each refuse the explained classification and
  the pair goes unexplained + quarantined;
- a presentation-only divergence over byte-stable,
  outcome-equal records dispositions identical-after-
  all and names the presentation artifact;
- adjudication lifts one quarantine and confirms
  another, as acts, with every run record's hash
  unchanged across the whole sequence, and an
  adjudication naming an unknown junction refuses with
  the index byte-unchanged;
- the standing T405 legacy pair pairs with nothing
  under a scan (key-partial sides) and junctions to
  not-comparable with the unrecoverable components
  named;
- the PR #509 tray-flake pair, replayed as a worked
  example from the CI job logs of record, junctions to
  explained-by-named-difference citing the registered
  shape — the manual adjudication of 2026-11-04,
  reproduced mechanically;
- the settling CLI's automatic trigger (T303): a
  divergent rerun seeded against a stored comparable
  record produces its junction + quarantine in the
  same invocation that created the run; an identical
  rerun produces neither.

The trigger tests use tmp mirror trees in the shape of
test_settling_run_scoped.py's precedent (symlinked
read-only inputs, a real tmp run store) and carry the
same clean-tree precondition guard.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from glossa_lab import ledger_gate as lg
from glossa_lab import run_junction as rj
from glossa_lab import run_records as rr
from glossa_lab import settling as st

ROOT = Path(__file__).resolve().parents[2]
JUNCTION_CLI = ROOT / "tools" / "ledger" / "run_junction.py"
SETTLING_CLI = ROOT / "tools" / "ledger" / "run_settling.py"
CANONICAL = json.loads((ROOT / st.CANONICAL_REL).read_text(encoding="utf-8"))
SCENARIO = next(
    s for s in CANONICAL["scenarios"] if s["id"] == "incumbent-over-subset"
)
SCOPE_ARG = ",".join(SCENARIO["inputs"]["scope"])

TRAY_TEST_ID = (
    "tests/test_tray_token_auth.py::"
    "test_copy_api_token_without_tkinter_is_named"
)
SQLITE_TEARDOWN_ERROR = (
    "sqlite3.ProgrammingError: Cannot operate on a "
    "closed database."
)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Fixture stores: settling records and suite records,
# entered under index acts


def _settling_record(run_id: str, started: str, *,
                     result=None, absence=None,
                     pins=None, command="run --candidate "
                     "incumbent --scope M001"):
    start = datetime.strptime(
        started, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    header = rr.build_header(
        surface="settling",
        tool="run_settling.py run",
        tool_version="0.1.0",
        command=command,
        code_version="c0ffee1234567890",
        input_pins=pins if pins is not None else {
            "ledger": {"sha256": "a" * 64, "lines": 943}
        },
        seed=rr.NO_SEED,
        environment_class="vm/linux",
        started=start,
        finished=start,
        run_id=run_id,
    )
    kwargs = {}
    if absence is not None:
        kwargs["absence"] = absence
    else:
        kwargs["result"] = result
    return rr.build_record(header, **kwargs)


def _enter(store: Path, record: dict) -> str:
    header = record["run"]
    name = f"{header['run_id']}.json"
    path = store / name
    path.write_text(
        json.dumps(record, ensure_ascii=False), encoding="utf-8"
    )
    rr.append_act(
        store / "run-index.jsonl",
        {
            "act": "entry",
            "run_id": header["run_id"],
            "record": name,
            "key": header["key"],
            "legacy": False,
        },
    )
    return header["run_id"]


def _store(tmp_path: Path) -> tuple[Path, Path]:
    store = tmp_path / "runs"
    store.mkdir(parents=True)
    return store, tmp_path / "junctions"


def _suite_record(run_id: str, started: str, finished: str,
                  summary: dict, errors: list, *, ci: dict):
    start = datetime.strptime(
        started, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    finish = datetime.strptime(
        finished, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    header = rr.build_header(
        surface="suite",
        tool="pytest (GitHub Actions: Backend tests (pytest))",
        tool_version="pytest (CI; version not pinned in "
        "the job log)",
        command=(
            "python -m pytest tests/ --tb=short -q "
            "--ignore=tests/test_pipelines_gpu.py "
            "--ignore=tests/test_install_gpu.py -x"
        ),
        code_version="a0fbdf97f726f56253e693c5eadcb740b416b74d",
        input_pins={
            "selection": ["tests/"],
            "ignore": [
                "tests/test_pipelines_gpu.py",
                "tests/test_install_gpu.py",
            ],
        },
        seed=rr.NO_SEED,
        environment_class="ci/linux",
        started=start,
        finished=finish,
        run_id=run_id,
    )
    record = rr.build_record(
        header,
        result={
            "summary": summary,
            "failures": [],
            "errors": errors,
        },
    )
    record["ci"] = ci
    return record


# ---------------------------------------------------------------------------
# T302 — the fixture-pair teeth


def test_identical_pair_writes_nothing(tmp_path):
    store, junctions = _store(tmp_path)
    _enter(store, _settling_record(
        "settling-20261104T070000Z-aa0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS", "counts": {"a": 1}},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070100Z-aa0002", "2026-11-04T07:01:00Z",
        result={"verdict": "PASS", "counts": {"a": 1}},
    ))
    index_before = (store / "run-index.jsonl").read_bytes()
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-aa0001",
        "settling-20261104T070100Z-aa0002",
    )
    assert outcome["disposition"] == "identical"
    assert outcome["junction_id"] is None
    assert not junctions.exists()
    assert (store / "run-index.jsonl").read_bytes() == index_before


def test_divergent_deterministic_pair_quarantines(tmp_path):
    store, junctions = _store(tmp_path)
    _enter(store, _settling_record(
        "settling-20261104T070000Z-bb0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS", "counts": {"a": 1}},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070100Z-bb0002", "2026-11-04T07:01:00Z",
        result={"verdict": "FAIL", "counts": {"a": 1}},
    ))
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-bb0001",
        "settling-20261104T070100Z-bb0002",
    )
    assert outcome["disposition"] == "unexplained"
    assert outcome["quarantined"] is True
    # The first divergence is the seeded path.
    assert outcome["first_divergences"][0].startswith(
        "result.verdict:"
    )
    assert "'FAIL' in run B" in outcome["first_divergences"][0]
    # The report is filed, immutable-shaped, and carries
    # the red-team section with its six causes unmarked.
    report = json.loads(
        Path(outcome["report_path"]).read_text(encoding="utf-8")
    )
    assert report["junction_id"] == outcome["junction_id"]
    assert report["disposition"] == "unexplained"
    assert [
        c["cause"] for c in report["red_team"]["causes"]
    ] == list(rj.RED_TEAM_CAUSES)
    assert all(
        c["marking"] is None for c in report["red_team"]["causes"]
    )
    assert report["red_team"]["junction_id"] == outcome[
        "junction_id"
    ]
    # Both runs stand quarantined in the folded index.
    state = rr.fold_index(store / "run-index.jsonl")
    assert set(state.open_quarantine) == {
        "settling-20261104T070000Z-bb0001",
        "settling-20261104T070100Z-bb0002",
    }


def test_one_side_empty_pair_localizes_first_result(tmp_path):
    store, junctions = _store(tmp_path)
    _enter(store, _settling_record(
        "settling-20261104T070000Z-cc0001", "2026-11-04T07:00:00Z",
        result={"assignments": [{"sign": "M001"}], "total": 1},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070100Z-cc0002", "2026-11-04T07:01:00Z",
        absence={
            "kind": "crashed",
            "detail": "RuntimeError: fixture crash",
        },
    ))
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-cc0001",
        "settling-20261104T070100Z-cc0002",
    )
    assert outcome["disposition"] == "unexplained"
    assert outcome["quarantined"] is True
    first, second = outcome["first_divergences"]
    assert "recorded an absence (crashed" in first
    assert "run B" in first and "run A" in second
    assert second.startswith("result.assignments[0].sign:")
    assert "'M001'" in second


def test_constitutive_diff_pair_is_not_comparable(tmp_path):
    store, junctions = _store(tmp_path)
    _enter(store, _settling_record(
        "settling-20261104T070000Z-dd0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070100Z-dd0002", "2026-11-04T07:01:00Z",
        result={"verdict": "FAIL"},
        pins={"ledger": {"sha256": "b" * 64, "lines": 944}},
    ))
    index_before = (store / "run-index.jsonl").read_bytes()
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-dd0001",
        "settling-20261104T070100Z-dd0002",
    )
    assert outcome["disposition"] == "not-comparable"
    assert outcome["differing_components"] == ["input_pins"]
    pins_entry = next(
        e for e in outcome["key_diff"]
        if e["component"] == "input_pins"
    )
    assert pins_entry["constitutive"] is True
    assert pins_entry["divergent_paths"]
    assert not junctions.exists()
    assert (store / "run-index.jsonl").read_bytes() == index_before


def test_code_version_difference_does_not_break_comparability(
    tmp_path,
):
    store, junctions = _store(tmp_path)
    rec_a = _settling_record(
        "settling-20261104T070000Z-ee0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    )
    rec_b = _settling_record(
        "settling-20261104T070100Z-ee0002", "2026-11-04T07:01:00Z",
        result={"verdict": "PASS"},
    )
    rec_b["run"]["key"]["code_version"] = "d15c0de123456789"
    _enter(store, rec_a)
    _enter(store, rec_b)
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-ee0001",
        "settling-20261104T070100Z-ee0002",
    )
    # Recorded-and-diffed, never constitutive (D-089-4):
    # equal results over differing code versions are an
    # identical pair, with the difference on the record.
    assert outcome["disposition"] == "identical"
    assert outcome["environment_diff"]["code_version"] == {
        "a": "c0ffee1234567890",
        "b": "d15c0de123456789",
        "differ": True,
    }


# ---------------------------------------------------------------------------
# T302 — the tray-flake worked example (PR #509) and the
# shape's evidence bar

# The recorded summaries of record: CI run 41839490370
# (PR #509, Spec 088 S5, head a0fbdf97), Backend tests
# (pytest) job — attempt 1 (job 126606956437): "2549
# passed, 98 skipped, 29 warnings, 1 error" with the
# single mark "ERROR at teardown of
# test_copy_api_token_without_tkinter_is_named ...
# sqlite3.ProgrammingError: Cannot operate on a closed
# database."; attempt 2 (job 126609751508, the
# failed-jobs rerun): "2549 passed, 98 skipped, 29
# warnings", no error. Job stamps from the job records;
# the stage closeout record (Spec 088,
# stage-t701-closeout-record.md) carries the same
# summary. The fixture records carry the outcome fields
# the registered shape is stated over — the counts and
# the error entries; durations and warning counts are
# log presentation, not result content.


def _pr509_pair(store: Path) -> tuple[str, str]:
    attempt_1 = _suite_record(
        "suite-20261104T133531Z-a11001",
        "2026-11-04T13:35:31Z", "2026-11-04T13:40:13Z",
        {"passed": 2549, "failed": 0, "errors": 1,
         "skipped": 98},
        [{
            "test_id": TRAY_TEST_ID,
            "phase": "teardown",
            "error": SQLITE_TEARDOWN_ERROR,
        }],
        ci={
            "github_run_id": 41839490370,
            "attempt": 1,
            "job": "Backend tests (pytest)",
            "job_id": 126606956437,
            "head_sha": "a0fbdf97f726f56253e693c5eadcb740b416b74d",
            "conclusion": "failure",
        },
    )
    attempt_2 = _suite_record(
        "suite-20261104T134045Z-a22002",
        "2026-11-04T13:40:45Z", "2026-11-04T13:44:39Z",
        {"passed": 2549, "failed": 0, "errors": 0,
         "skipped": 98},
        [],
        ci={
            "github_run_id": 41839490370,
            "attempt": 2,
            "job": "Backend tests (pytest)",
            "job_id": 126609751508,
            "head_sha": "a0fbdf97f726f56253e693c5eadcb740b416b74d",
            "conclusion": "success",
        },
    )
    return _enter(store, attempt_1), _enter(store, attempt_2)


def test_pr509_worked_example_explained_by_shape(tmp_path):
    store, junctions = _store(tmp_path)
    run_a, run_b = _pr509_pair(store)
    outcome = rj.analyze_pair(store, junctions, run_a, run_b)
    assert outcome["disposition"] == (
        "explained-by-named-difference"
    )
    shape = outcome["shape"]
    assert shape["shape"] == "tray-teardown-flake"
    assert any(
        "pass counts equal: 2549" in line
        for line in shape["evidence"]
    )
    assert any(
        TRAY_TEST_ID in line for line in shape["evidence"]
    )
    assert any(
        line.startswith("result.errors")
        or line.startswith("result.summary")
        for line in shape["divergent_lines"]
    )
    # Explained pairs are filed but never quarantined.
    report = json.loads(
        Path(outcome["report_path"]).read_text(encoding="utf-8")
    )
    assert report["disposition"] == (
        "explained-by-named-difference"
    )
    state = rr.fold_index(store / "run-index.jsonl")
    assert state.open_quarantine == {}
    assert state.junctions == {}


@pytest.mark.parametrize(
    "mutate,why",
    [
        ("error-text", "no sqlite closed-database family"),
        ("counts", "pass counts unequal"),
        ("test-id", "not a tray test id"),
        ("phase", "not a teardown error"),
    ],
)
def test_shape_evidence_absent_refuses_explained(
    tmp_path, mutate, why
):
    """The mechanical explained case cannot be asserted
    without its evidence: each mutation removes one
    registered element of the shape, and the pair goes
    unexplained + quarantined instead (the shape's
    evidence bar)."""
    store, junctions = _store(tmp_path)
    summary_1 = {"passed": 2549, "failed": 0, "errors": 1,
                 "skipped": 98}
    entry = {
        "test_id": TRAY_TEST_ID,
        "phase": "teardown",
        "error": SQLITE_TEARDOWN_ERROR,
    }
    if mutate == "error-text":
        entry["error"] = "AssertionError: assert 1 == 2"
    elif mutate == "counts":
        summary_1["passed"] = 2548
    elif mutate == "test-id":
        entry["test_id"] = (
            "tests/test_auth_api.py::"
            "test_copy_api_token_without_tkinter_is_named"
        )
    elif mutate == "phase":
        entry["phase"] = "call"
    run_a = _enter(store, _suite_record(
        "suite-20261104T133531Z-a11001",
        "2026-11-04T13:35:31Z", "2026-11-04T13:40:13Z",
        summary_1, [entry], ci={"attempt": 1},
    ))
    run_b = _enter(store, _suite_record(
        "suite-20261104T134045Z-a22002",
        "2026-11-04T13:40:45Z", "2026-11-04T13:44:39Z",
        {"passed": 2549, "failed": 0, "errors": 0,
         "skipped": 98},
        [], ci={"attempt": 2},
    ))
    outcome = rj.analyze_pair(store, junctions, run_a, run_b)
    assert outcome["disposition"] == "unexplained", why
    assert outcome["quarantined"] is True
    causes = {
        c["cause"]: c
        for c in outcome["red_team"]["causes"]
    }
    nondeterminism = " ".join(
        causes["nondeterminism"]["evidence"]
    )
    assert "tray-teardown-flake" in nondeterminism
    assert "not matched" in nondeterminism


# ---------------------------------------------------------------------------
# T302 — identical-after-all, adjudication, the legacy
# pair, and the scan


def test_presentation_only_divergence_identical_after_all(
    tmp_path,
):
    store, junctions = _store(tmp_path)
    _enter(store, _settling_record(
        "settling-20261104T070000Z-ff0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070100Z-ff0002", "2026-11-04T07:01:00Z",
        result={"verdict": "PASS"},
    ))
    # Without a presentation claim the pair is simply
    # identical and nothing is filed.
    plain = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-ff0001",
        "settling-20261104T070100Z-ff0002",
    )
    assert plain["disposition"] == "identical"
    assert not junctions.exists()
    # With one, and the records byte-stable and equal,
    # the disposition is identical-after-all and the
    # report names the presentation artifact.
    outcome = rj.analyze_pair(
        store, junctions,
        "settling-20261104T070000Z-ff0001",
        "settling-20261104T070100Z-ff0002",
        presented_artifact=(
            "background-delivery summary of 2026-11-04 "
            "(presented verdicts PASS / FAIL)"
        ),
    )
    assert outcome["disposition"] == "identical-after-all"
    report = json.loads(
        Path(outcome["report_path"]).read_text(encoding="utf-8")
    )
    assert report["presentation_artifact"].startswith(
        "background-delivery summary"
    )
    state = rr.fold_index(store / "run-index.jsonl")
    assert state.open_quarantine == {}


def test_adjudication_lifts_and_confirms_records_untouched(
    tmp_path,
):
    store, junctions = _store(tmp_path)
    ids = []
    for i, verdict in enumerate(("PASS", "FAIL", "PASS", "FAIL")):
        ids.append(_enter(store, _settling_record(
            f"settling-20261104T070{i}00Z-ab000{i + 1}",
            f"2026-11-04T07:0{i}:00Z",
            result={"verdict": verdict},
        )))
    hashes_before = {
        p.name: _sha256_file(p) for p in store.glob("*.json")
    }
    first = rj.analyze_pair(store, junctions, ids[0], ids[1])
    second = rj.analyze_pair(store, junctions, ids[2], ids[3])
    assert first["quarantined"] and second["quarantined"]
    # Lift the first quarantine; confirm the second.
    rj.adjudicate(
        store, first["junction_id"],
        ruling="fixture ruling: the divergence is a "
        "seeded test artifact",
        actor="test-suite (T302)",
        resulting_state="quarantine-lifted",
    )
    rj.adjudicate(
        store, second["junction_id"],
        ruling="fixture ruling: divergence stands "
        "unexplained on re-examination",
        actor="test-suite (T302)",
        resulting_state="quarantine-confirmed",
    )
    state = rr.fold_index(store / "run-index.jsonl")
    assert set(state.open_quarantine) == {ids[2], ids[3]}
    assert state.junctions[first["junction_id"]]["lifted"] is True
    assert state.junctions[second["junction_id"]]["lifted"] is False
    # An adjudication naming an unknown junction refuses,
    # and the index is byte-unchanged by the refusal.
    index_before = (store / "run-index.jsonl").read_bytes()
    with pytest.raises(rr.RunRecordError):
        rj.adjudicate(
            store, "junction-20261104T070000Z-000000",
            ruling="fixture ruling",
            actor="test-suite (T302)",
            resulting_state="quarantine-lifted",
        )
    assert (store / "run-index.jsonl").read_bytes() == index_before
    # No run record's bytes moved across the whole
    # sequence.
    assert {
        p.name: _sha256_file(p) for p in store.glob("*.json")
    } == hashes_before


def test_scan_lists_identical_and_skips_the_rest(tmp_path):
    store, junctions = _store(tmp_path)
    same_a = _enter(store, _settling_record(
        "settling-20261104T070000Z-ac0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    ))
    same_b = _enter(store, _settling_record(
        "settling-20261104T070100Z-ac0002", "2026-11-04T07:01:00Z",
        result={"verdict": "PASS"},
    ))
    divergent = _enter(store, _settling_record(
        "settling-20261104T070200Z-ac0003", "2026-11-04T07:02:00Z",
        result={"verdict": "FAIL"},
    ))
    _enter(store, _settling_record(
        "settling-20261104T070300Z-ac0004", "2026-11-04T07:03:00Z",
        result={"verdict": "PASS"},
        pins={"ledger": {"sha256": "b" * 64, "lines": 944}},
    ))
    outcome = rj.scan_store(store, junctions)
    assert outcome["counts"] == {"identical": 1, "unexplained": 2}
    assert len(outcome["skipped"]) == 3
    assert all(
        "input_pins" in skipped["reason"]
        for skipped in outcome["skipped"]
    )
    state = rr.fold_index(store / "run-index.jsonl")
    # Pairs (a, c) and (b, c) are unexplained: all three
    # comparable runs stand quarantined.
    assert set(state.open_quarantine) == {same_a, same_b, divergent}


def test_legacy_pair_is_not_comparable(tmp_path):
    """The T405 pair, copied read-only into a
    tmp store under its legacy entries: a scan pairs it
    with nothing, and a direct compare dispositions
    not-comparable naming the unrecoverable constitutive
    components — the legacy label's honesty, mechanized
    (C089-17)."""
    store, junctions = _store(tmp_path)
    # The pair departed the standing store at the Spec 093
    # intake replay (2026-11-05); its bytes stand preserved
    # as fixtures at the departure acts' blob hashes
    # (tests/fixtures/legacy_t405_pair/).
    fixtures = (
        Path(__file__).resolve().parent / "fixtures" / "legacy_t405_pair"
    )
    for name in (
        "t405-incumbent-over-full-frame--d9f73e4c4e4e.json",
        "t405-full-register-over-full-frame--f8c86443e924.json",
    ):
        (store / name).write_bytes((fixtures / name).read_bytes())
    for act in rr.enumerate_legacy_entries(store):
        rr.append_act(store / "run-index.jsonl", act)
    scan = rj.scan_store(store, junctions)
    assert scan["pairs"] == []
    assert len(scan["skipped"]) == 1
    assert "legacy" in scan["skipped"][0]["reason"]
    outcome = rj.analyze_pair(
        store, junctions,
        "legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e",
        "legacy:t405-full-register-over-full-frame--f8c86443e924",
    )
    assert outcome["disposition"] == "not-comparable"
    assert set(outcome["differing_components"]) == {
        "command", "tool_version", "seed",
    }
    assert not junctions.exists()


# ---------------------------------------------------------------------------
# T301/T302 — the CLI, over a seeded tmp store


def _junction_cli(store: Path, junctions: Path, *args: str):
    return subprocess.run(
        [
            sys.executable, str(JUNCTION_CLI),
            "--root", str(ROOT),
            "--store", str(store),
            "--junctions", str(junctions),
            *args,
        ],
        capture_output=True, text=True, timeout=120,
    )


def test_cli_compare_scan_adjudicate(tmp_path):
    store, junctions = _store(tmp_path)
    run_a = _enter(store, _settling_record(
        "settling-20261104T070000Z-ad0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    ))
    run_b = _enter(store, _settling_record(
        "settling-20261104T070100Z-ad0002", "2026-11-04T07:01:00Z",
        result={"verdict": "FAIL"},
    ))
    compared = _junction_cli(store, junctions, "compare", run_a, run_b)
    assert compared.returncode == 0, compared.stderr
    assert "unexplained" in compared.stdout
    assert "QUARANTINED" in compared.stdout
    assert "may be cited as verdict support" in compared.stdout
    reports = list(junctions.glob("*.json"))
    assert len(reports) == 1
    junction_id = reports[0].stem
    adjudicated = _junction_cli(
        store, junctions, "adjudicate", junction_id,
        "--ruling", "fixture ruling via CLI",
        "--actor", "test-suite (T302)",
    )
    assert adjudicated.returncode == 0, adjudicated.stderr
    state = rr.fold_index(store / "run-index.jsonl")
    assert state.open_quarantine == {}
    scanned = _junction_cli(store, junctions, "scan")
    assert scanned.returncode == 0, scanned.stderr
    assert "1 comparable pair(s) analyzed" in scanned.stdout


def test_cli_refusals_are_named(tmp_path):
    store, junctions = _store(tmp_path)
    run_a = _enter(store, _settling_record(
        "settling-20261104T070000Z-ae0001", "2026-11-04T07:00:00Z",
        result={"verdict": "PASS"},
    ))
    unknown = _junction_cli(
        store, junctions, "compare", run_a,
        "settling-20261104T070100Z-ae0002",
    )
    assert unknown.returncode == 1
    assert "JUNCTION REFUSED" in unknown.stderr
    bogus = _junction_cli(
        store, junctions, "adjudicate",
        "junction-20261104T070000Z-000000",
        "--ruling", "fixture", "--actor", "test-suite",
    )
    assert bogus.returncode == 1
    assert "JUNCTION REFUSED" in bogus.stderr


# ---------------------------------------------------------------------------
# T303 — the automatic trigger on the settling surface
#
# Mirror trees in test_settling_run_scoped.py's shape,
# with the same clean-tree precondition guard: the
# engine refuses over diverged sources by design, so a
# suite process whose earlier tests rewrote mirrored
# sources in-tree skips these with the cause named.


_DIVERGENCE_RE = re.compile(
    r"recorded (?:sidecar )?sha256 for (?P<hashed>\S+) does not match"
    r"|(?:source|sidecar) (?P<missing>\S+) not found"
)


def _require_recorded_hashes(root: Path) -> None:
    report = lg.run_gate(root, scope={"V1"})
    arm = next(
        c for c in report.checks if c.name.startswith("V1 recorded")
    )
    if arm.status != "FAIL":
        return
    paths: list[str] = []
    for ev in arm.evidence:
        for match in _DIVERGENCE_RE.finditer(ev):
            paths.append(match.group("hashed") or match.group("missing"))
    pytest.skip(
        "clean-tree precondition destroyed in this suite "
        "process: the evidence-API tests rewrote source "
        "files the ledger mirrors by hash ("
        + ", ".join(sorted(set(paths))[:4])
        + "); the engine refuses over diverged sources "
        "by design"
    )


def _mirror_root(tmp_path: Path) -> Path:
    _require_recorded_hashes(ROOT)
    root = tmp_path / "root"
    root.mkdir(parents=True)
    for name in ("specs", "glossa-corpus", "reports"):
        (root / name).symlink_to(ROOT / name, target_is_directory=True)
    reports_dir = root / "backend" / "reports"
    reports_dir.mkdir(parents=True)
    (reports_dir / "INDUS_FINAL_ANCHORS.json").symlink_to(
        ROOT / st.ANCHORS_REL
    )
    indus = root / "glossa-indus"
    indus.mkdir()
    for child in sorted((ROOT / "glossa-indus").iterdir()):
        if child.name == "ledger":
            continue
        (indus / child.name).symlink_to(
            child, target_is_directory=child.is_dir()
        )
    ledger = indus / "ledger"
    ledger.mkdir()
    for child in sorted((ROOT / "glossa-indus" / "ledger").iterdir()):
        if child.name in ("runs", "assignment-sets.json", "claims.jsonl"):
            continue
        (ledger / child.name).symlink_to(
            child, target_is_directory=child.is_dir()
        )
    (ledger / "claims.jsonl").symlink_to(
        ROOT / "glossa-indus" / "ledger" / "claims.jsonl"
    )
    (ledger / "assignment-sets.json").symlink_to(
        ROOT / st.ASSIGNMENT_SETS_REL
    )
    (ledger / "runs").mkdir()
    return root


def _settling_cli(root: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(SETTLING_CLI), "--root", str(root), *args],
        capture_output=True, text=True, timeout=300,
    )


def _run_scenario(root: Path):
    return _settling_cli(
        root, "run",
        "--candidate", "incumbent",
        "--scope", SCOPE_ARG,
        "--scenario", SCENARIO["id"],
    )


def _first_leaf(value, path):
    if isinstance(value, dict):
        for key, item in value.items():
            return _first_leaf(item, f"{path}.{key}")
        return path, value
    if isinstance(value, list):
        for i, item in enumerate(value):
            return _first_leaf(item, f"{path}[{i}]")
        return path, value
    return path, value


def _mutated_copy(record):
    """A deep copy of a run record with the first scalar
    leaf of its result block (in the localizer's
    traversal order) changed; the leaf's path in
    localizer format comes back with it."""
    import copy

    mutated = copy.deepcopy(record)
    leaf_path, leaf = _first_leaf(mutated["result"], "result")
    keys: list = []
    rest = leaf_path[len("result"):]
    for token in re.findall(r"\.([^.\[\]]+)|\[(\d+)\]", rest):
        keys.append(token[0] if token[0] else int(token[1]))
    if isinstance(leaf, bool):
        replacement = not leaf
    elif isinstance(leaf, int):
        replacement = leaf + 1
    elif isinstance(leaf, float):
        replacement = leaf + 1.0
    elif isinstance(leaf, str):
        replacement = leaf + " (fixture mutation)"
    else:
        replacement = "fixture-mutation"
    if not keys:
        mutated["result"] = replacement
        return mutated, leaf_path
    parent = mutated["result"]
    for key in keys[:-1]:
        parent = parent[key]
    parent[keys[-1]] = replacement
    return mutated, leaf_path


def test_trigger_identical_rerun_writes_no_junction(tmp_path):
    root = _mirror_root(tmp_path)
    first = _run_scenario(root)
    assert first.returncode == 0, first.stderr
    second = _run_scenario(root)
    assert second.returncode == 0, second.stderr
    assert "junction scan:" in second.stdout
    assert "identical" in second.stdout
    junctions = root / "glossa-indus" / "ledger" / "junctions"
    assert not junctions.exists()
    state = rr.fold_index(root / st.RUN_STORE_REL / "run-index.jsonl")
    assert state.open_quarantine == {}
    assert state.junctions == {}


def test_trigger_divergent_rerun_junctions_in_same_invocation(
    tmp_path,
):
    root = _mirror_root(tmp_path)
    # Seed the store with a comparable record whose
    # result is the genuine evaluation's, mutated at
    # exactly one leaf — the divergent-rerun raw
    # material, built from the engine's own output.
    state = st.load_state(root)
    command = (
        f"run --candidate incumbent --scope {SCOPE_ARG} "
        f"--scenario {SCENARIO['id']}"
    )
    fixture_id = rr.mint_run_id(
        "settling",
        now=datetime(2026, 11, 4, 6, 0, 0, tzinfo=timezone.utc),
    )
    header = st.settling_run_header(
        state.pins,
        command=command,
        tool="run_settling.py run",
        run_id=fixture_id,
        started=datetime(2026, 11, 4, 6, 0, 0, tzinfo=timezone.utc),
        code_version="fixture",
    )
    genuine = st.run_record(
        state, SCENARIO["inputs"]["candidate"],
        SCENARIO["inputs"]["scope"],
        scenario=SCENARIO["id"], header=header,
    )
    seeded, leaf_path = _mutated_copy(genuine)
    st.write_run_record(root, seeded)
    rr.append_act(
        st.run_index_path(root),
        {
            "act": "entry",
            "run_id": fixture_id,
            "record": st.run_record_path(root, seeded).name,
            "key": header["key"],
            "legacy": False,
        },
    )
    # The rerun: the trigger must junction the pair in
    # this same invocation — no further command.
    rerun = _run_scenario(root)
    assert rerun.returncode == 0, rerun.stderr
    assert "UNEXPLAINED" in rerun.stdout
    junctions = root / "glossa-indus" / "ledger" / "junctions"
    reports = list(junctions.glob("*.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["disposition"] == "unexplained"
    report_run_ids = {run["run_id"] for run in report["runs"]}
    assert fixture_id in report_run_ids
    assert len(report_run_ids) == 2
    assert report["first_divergences"][0].startswith(
        leaf_path + ":"
    )
    state_after = rr.fold_index(st.run_index_path(root))
    assert fixture_id in state_after.open_quarantine
    assert len(state_after.open_quarantine) == 2
