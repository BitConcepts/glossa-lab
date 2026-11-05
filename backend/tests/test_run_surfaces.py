"""Spec 089 Stage 4 — the suite and experiment surfaces
(T401–T403).

The two surfaces' teeth, on tmp stores, tmp git trees,
and fake backends throughout (the one live-backend
exercise is the stage record's act, not a test — CI has
no backend):

Suite (T401, C089-6):

- the result block is parsed from the run's own output
  file: the counts follow the file's FINAL verdict line
  even when earlier text in the file presents different
  numbers, and the failed/errored test ids land in the
  Stage 3 fixture schema the junction matcher consumes
  ({test_id, phase, error} — phase from the ERRORS
  sections' own headers);
- a file with no verdict line refuses — there is no
  outcome to record;
- records the writer emits from REAL pytest runs (a tmp
  mini-suite, run by subprocess) validate, enter a
  store, and feed `compare_sides`: a divergent pair
  localizes into the result block's error paths;
- the PR #509 tray-flake pair, re-entered as output
  files in the CI logs' own format and bound by this
  stage's writer (the S3 worked example's fixture
  records were hand-built; these are writer-built),
  junctions to explained-by-named-difference citing the
  registered shape;
- the rewrite manifest over `glossa-indus/claims/` +
  `glossa-indus/reports/`: a dirty-tree fixture yields
  the manifest with HEAD/after hashes; a retained path
  without a reason refuses; an undisposed rewrite
  refuses; a disposition for an unrewritten path
  refuses; a restored path verifies byte-equal to HEAD.

Experiment (T403, C089-8):

- a completed job's citation record binds the job id
  and its recorded inputs (graph id + registered
  version, parameters verbatim), carries the results
  payload hash — re-derived identically from a second
  read of the same job (the T403 hash check) — and
  enters the store's index, so the citation resolves
  from the index alone;
- a graph carrying no version is pinned by its
  definition hash, recorded as such;
- a failed or cancelled job leaves an ABSENCE record
  (kind crashed), not a citable result; a completed job
  with no stored results leaves an empty absence; a
  running job refuses and writes nothing;
- a citation naming a quarantined run is detectable
  from the folded index state.

Store writer: a second write of one run id refuses (id
collision), with the store byte-unchanged.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from glossa_lab import run_junction as rj
from glossa_lab import run_records as rr

ROOT = Path(__file__).resolve().parents[2]
SUITE_CLI = ROOT / "tools" / "runs" / "suite_run_record.py"
CITATION_CLI = ROOT / "tools" / "runs" / "job_citation.py"

TRAY_TEST_ID = (
    "tests/test_tray_token_auth.py::"
    "test_copy_api_token_without_tkinter_is_named"
)
SQLITE_TEARDOWN_ERROR = (
    "sqlite3.ProgrammingError: Cannot operate on a "
    "closed database."
)

SUITE_COMMAND = (
    "python -m pytest tests/ --tb=short -q "
    "--ignore=tests/test_pipelines_gpu.py "
    "--ignore=tests/test_install_gpu.py -x"
)
SUITE_PINS = {
    "selection": ["tests/"],
    "ignore": [
        "tests/test_pipelines_gpu.py",
        "tests/test_install_gpu.py",
    ],
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stamp(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )


# ---------------------------------------------------------------------------
# T401 — pytest output parsing (the record follows the file)


def test_parse_follows_the_files_final_verdict_line():
    # A test inside the run presents its own numbers
    # (an echoed summary-shaped line, with a duration);
    # the run's outcome is the file's FINAL verdict line.
    text = (
        "tests/test_echo.py::test_echo PASSED\n"
        "3 passed, 9 failed in 0.50s\n"  # the echo, not the verdict
        "tests/test_real.py::test_real PASSED\n"
        "=========================== short test summary info "
        "============================\n"
        "FAILED tests/test_real.py::test_broken - AssertionError: no\n"
        "10 passed, 1 failed, 2 skipped in 12.50s\n"
    )
    result, duration = rr.parse_pytest_output(text)
    assert result["summary"] == {
        "passed": 10,
        "failed": 1,
        "errors": 0,
        "skipped": 2,
    }
    assert result["failures"] == ["tests/test_real.py::test_broken"]
    assert result["errors"] == []
    assert duration == 12.50


def test_parse_extracts_error_entries_in_the_fixture_schema():
    text = (
        "==================================== ERRORS "
        "====================================\n"
        "______ ERROR at teardown of "
        "test_copy_api_token_without_tkinter_is_named _______\n"
        "E   sqlite3.ProgrammingError: Cannot operate on a "
        "closed database.\n"
        "=========================== short test summary info "
        "============================\n"
        f"ERROR {TRAY_TEST_ID} - {SQLITE_TEARDOWN_ERROR}\n"
        "2549 passed, 98 skipped, 29 warnings, 1 error in "
        "242.98s (0:04:02)\n"
    )
    result, duration = rr.parse_pytest_output(text)
    assert result["summary"] == {
        "passed": 2549,
        "failed": 0,
        "errors": 1,
        "skipped": 98,
    }
    assert result["errors"] == [
        {
            "test_id": TRAY_TEST_ID,
            "phase": "teardown",
            "error": SQLITE_TEARDOWN_ERROR,
        }
    ]
    assert duration == 242.98


def test_parse_error_phase_is_unknown_without_a_section_header():
    text = (
        "=========================== short test summary info "
        "============================\n"
        "ERROR tests/test_x.py::test_y - RuntimeError: boom\n"
        "5 passed, 1 error in 3.25s\n"
    )
    result, _ = rr.parse_pytest_output(text)
    assert result["errors"] == [
        {"test_id": "tests/test_x.py::test_y", "phase": "unknown",
         "error": "RuntimeError: boom"}
    ]


def test_parse_refuses_a_file_with_no_verdict_line():
    with pytest.raises(rr.RunRecordError):
        rr.parse_pytest_output("tests ran, trust me\n")


# ---------------------------------------------------------------------------
# T401 — the writer over real pytest runs + the junction
# matcher consuming the emitted schema


def _run_mini_suite(tmp_path: Path, *, teardown_error: bool) -> Path:
    suite = tmp_path / ("suite_bad" if teardown_error else "suite_good")
    suite.mkdir()
    (suite / "test_alpha.py").write_text(
        "def test_one():\n    assert True\n\n"
        "def test_two():\n    assert True\n",
        encoding="utf-8",
    )
    fixture = (
        "import pytest\n\n"
        "@pytest.fixture\n"
        "def resource():\n"
        "    yield 1\n"
        "    raise RuntimeError('teardown boom')\n\n"
        "def test_uses(resource):\n    assert resource == 1\n"
        if teardown_error
        else "def test_uses():\n    assert True\n"
    )
    (suite / "test_beta.py").write_text(fixture, encoding="utf-8")
    output = tmp_path / ("out_bad.txt" if teardown_error else "out_good.txt")
    proc = subprocess.run(
        [
            sys.executable, "-m", "pytest", str(suite),
            "-q", "--tb=short", "-p", "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    output.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    return output


def _suite_record_from_output(
    output: Path, started: str, finished: str
) -> dict:
    result, _ = rr.parse_pytest_output(
        output.read_text(encoding="utf-8")
    )
    return rr.build_suite_record(
        command="python -m pytest <suite> -q --tb=short",
        tool_version="9.2.0",
        input_pins={"selection": ["<suite>"], "ignore": []},
        code_version="d" * 40,
        environment_class="vm/linux",
        started=_stamp(started),
        finished=_stamp(finished),
        result=result,
        tree={"sha": "d" * 40, "dirty": False, "rewrite_manifest": []},
    )


def test_writer_binds_a_real_pytest_run_and_the_matcher_consumes_it(
    tmp_path,
):
    bad = _run_mini_suite(tmp_path, teardown_error=True)
    good = _run_mini_suite(tmp_path, teardown_error=False)
    rec_bad = _suite_record_from_output(
        bad, "2026-11-04T10:00:00Z", "2026-11-04T10:00:05Z"
    )
    rec_good = _suite_record_from_output(
        good, "2026-11-04T10:05:00Z", "2026-11-04T10:05:05Z"
    )
    # The real run's own verdict, in the fixture schema.
    assert rec_bad["result"]["summary"] == {
        "passed": 3,
        "failed": 0,
        "errors": 1,
        "skipped": 0,
    }
    assert rec_bad["result"]["errors"][0]["phase"] == "teardown"
    assert rec_good["result"]["summary"]["errors"] == 0
    rr.validate_record(rec_bad)
    rr.validate_record(rec_good)
    store = tmp_path / "store"
    rr.write_run_record(store, rec_bad)
    rr.write_run_record(store, rec_good)
    state = rr.fold_index(store / "run-index.jsonl")
    side_a, _ = rj.load_side(
        store, state, rec_bad["run"]["run_id"]
    )
    side_b, _ = rj.load_side(
        store, state, rec_good["run"]["run_id"]
    )
    analysis = rj.compare_sides(side_a, side_b)
    # The error text is outside the registered family, so
    # the pair is unexplained — but the matcher READ the
    # writer's schema and localized the divergence into
    # the result block's error paths.
    assert analysis["disposition"] == "unexplained"
    assert any(
        path.startswith("result.errors")
        or path.startswith("result.summary.errors")
        for path in analysis["first_divergences"]
    )


def test_writer_built_flake_pair_junctions_to_explained(tmp_path):
    # The PR #509 pair, as output files in the CI logs'
    # own format (the S3 fixtures were hand-built
    # records; these records are built by this stage's
    # writer from output text).
    attempt_1 = (
        "==================================== ERRORS "
        "====================================\n"
        "______ ERROR at teardown of "
        "test_copy_api_token_without_tkinter_is_named _______\n"
        "E   sqlite3.ProgrammingError: Cannot operate on a "
        "closed database.\n"
        "=========================== short test summary info "
        "============================\n"
        f"ERROR {TRAY_TEST_ID} - {SQLITE_TEARDOWN_ERROR}\n"
        "2549 passed, 98 skipped, 29 warnings, 1 error in "
        "242.98s (0:04:02)\n"
    )
    attempt_2 = (
        "2549 passed, 98 skipped, 29 warnings in 275.20s "
        "(0:04:35)\n"
    )

    def record(text: str, started: str, finished: str) -> dict:
        result, _ = rr.parse_pytest_output(text)
        return rr.build_suite_record(
            command=SUITE_COMMAND,
            tool_version="pytest (CI; version not pinned in "
            "the job log)",
            input_pins=SUITE_PINS,
            code_version="a0fbdf97f726f56253e693c5eadcb740b416b74d",
            environment_class="ci/linux",
            started=_stamp(started),
            finished=_stamp(finished),
            result=result,
            tree={
                "sha": "a0fbdf97f726f56253e693c5eadcb740b416b74d",
                "dirty": False,
                "rewrite_manifest": [],
            },
        )

    rec_1 = record(attempt_1, "2026-11-04T13:35:31Z", "2026-11-04T13:40:13Z")
    rec_2 = record(attempt_2, "2026-11-04T13:40:45Z", "2026-11-04T13:44:39Z")
    store = tmp_path / "store"
    rr.write_run_record(store, rec_1)
    rr.write_run_record(store, rec_2)
    state = rr.fold_index(store / "run-index.jsonl")
    side_1, _ = rj.load_side(store, state, rec_1["run"]["run_id"])
    side_2, _ = rj.load_side(store, state, rec_2["run"]["run_id"])
    analysis = rj.compare_sides(side_1, side_2)
    assert analysis["disposition"] == "explained-by-named-difference"
    assert "tray-teardown-flake" in json.dumps(analysis)


# ---------------------------------------------------------------------------
# T401 — the rewrite manifest and its dispositions


def _git(root: Path, *args: str) -> None:
    proc = subprocess.run(
        [
            "git", "-C", str(root),
            "-c", "user.name=S089 S4 tests",
            "-c", "user.email=s089-tests@example.invalid",
            *args,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr


def _git_tree(tmp_path: Path) -> Path:
    root = tmp_path / "tree"
    (root / "glossa-indus" / "claims").mkdir(parents=True)
    (root / "glossa-indus" / "reports").mkdir(parents=True)
    (root / "glossa-indus" / "claims" / "a.json").write_text(
        '{"a": 1}\n', encoding="utf-8"
    )
    (root / "glossa-indus" / "reports" / "r.json").write_text(
        '{"r": 1}\n', encoding="utf-8"
    )
    (root / "other.txt").write_text("outside\n", encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "fixture")
    return root


def test_manifest_names_rewrites_with_head_and_after_hashes(tmp_path):
    root = _git_tree(tmp_path)
    claims = root / "glossa-indus" / "claims"
    (claims / "a.json").write_text('{"a": 2}\n', encoding="utf-8")
    (root / "glossa-indus" / "reports" / "r.json").unlink()
    (claims / "b.json").write_text('{"b": 1}\n', encoding="utf-8")
    manifest = rr.rewrite_manifest(root)
    by_path = {entry["path"]: entry for entry in manifest}
    assert set(by_path) == {
        "glossa-indus/claims/a.json",
        "glossa-indus/claims/b.json",
        "glossa-indus/reports/r.json",
    }
    assert by_path["glossa-indus/claims/a.json"]["head_sha256"] == (
        hashlib.sha256(b'{"a": 1}\n').hexdigest()
    )
    assert by_path["glossa-indus/claims/a.json"]["after_sha256"] == (
        hashlib.sha256(b'{"a": 2}\n').hexdigest()
    )
    assert by_path["glossa-indus/reports/r.json"]["after_sha256"] is None
    assert by_path["glossa-indus/claims/b.json"]["head_sha256"] is None


def test_clean_tree_manifest_is_empty(tmp_path):
    root = _git_tree(tmp_path)
    assert rr.rewrite_manifest(root) == []


def test_retained_without_a_reason_refuses(tmp_path):
    root = _git_tree(tmp_path)
    target = root / "glossa-indus" / "claims" / "a.json"
    target.write_text('{"a": 2}\n', encoding="utf-8")
    manifest = rr.rewrite_manifest(root)
    with pytest.raises(rr.RunRecordError):
        rr.apply_rewrite_dispositions(
            root,
            manifest,
            {"glossa-indus/claims/a.json": {"disposition": "retained"}},
        )
    # The refusal applied nothing.
    assert target.read_text(encoding="utf-8") == '{"a": 2}\n'


def test_undisposed_rewrite_refuses(tmp_path):
    root = _git_tree(tmp_path)
    (root / "glossa-indus" / "claims" / "a.json").write_text(
        '{"a": 2}\n', encoding="utf-8"
    )
    manifest = rr.rewrite_manifest(root)
    with pytest.raises(rr.RunRecordError):
        rr.apply_rewrite_dispositions(root, manifest, {})


def test_disposition_for_an_unrewritten_path_refuses(tmp_path):
    root = _git_tree(tmp_path)
    with pytest.raises(rr.RunRecordError):
        rr.apply_rewrite_dispositions(
            root,
            [],
            {
                "glossa-indus/claims/a.json": {
                    "disposition": "restored"
                }
            },
        )


def test_restored_rewrite_verifies_byte_equal_to_head(tmp_path):
    root = _git_tree(tmp_path)
    target = root / "glossa-indus" / "claims" / "a.json"
    target.write_text('{"a": 2}\n', encoding="utf-8")
    manifest = rr.rewrite_manifest(root)
    finalized = rr.apply_rewrite_dispositions(
        root,
        manifest,
        {"glossa-indus/claims/a.json": {"disposition": "restored"}},
    )
    assert target.read_bytes() == b'{"a": 1}\n'
    assert finalized[0]["disposition"] == "restored"
    assert rr.rewrite_manifest(root) == []


def test_retained_rewrite_carries_its_reason(tmp_path):
    root = _git_tree(tmp_path)
    (root / "glossa-indus" / "claims" / "a.json").write_text(
        '{"a": 2}\n', encoding="utf-8"
    )
    manifest = rr.rewrite_manifest(root)
    finalized = rr.apply_rewrite_dispositions(
        root,
        manifest,
        {
            "glossa-indus/claims/a.json": {
                "disposition": "retained",
                "reason": "the regeneration is the stage's object",
            }
        },
    )
    assert finalized[0]["disposition"] == "retained"
    assert finalized[0]["reason"] == (
        "the regeneration is the stage's object"
    )


# ---------------------------------------------------------------------------
# The store writer + quarantine detectability


def _one_suite_record() -> dict:
    result, _ = rr.parse_pytest_output("7 passed in 1.50s\n")
    return rr.build_suite_record(
        command="python -m pytest tests/ -q",
        tool_version="9.2.0",
        input_pins={"selection": ["tests/"], "ignore": []},
        code_version="e" * 40,
        environment_class="vm/linux",
        started=_stamp("2026-11-04T09:00:00Z"),
        finished=_stamp("2026-11-04T09:00:02Z"),
        result=result,
        tree={"sha": "e" * 40, "dirty": False, "rewrite_manifest": []},
    )


def test_write_run_record_enters_the_index_and_refuses_a_collision(
    tmp_path,
):
    store = tmp_path / "store"
    record = _one_suite_record()
    path = rr.write_run_record(store, record)
    assert path.is_file()
    state = rr.fold_index(store / "run-index.jsonl")
    run_id = record["run"]["run_id"]
    assert state.entries[run_id]["record"] == path.name
    assert state.entries[run_id]["key"] == record["run"]["key"]
    index_bytes = (store / "run-index.jsonl").read_bytes()
    with pytest.raises(rr.RunRecordError):
        rr.write_run_record(store, record)
    assert (store / "run-index.jsonl").read_bytes() == index_bytes
    assert _sha256_file(path) == _sha256_file(path)  # bytes stand


def test_a_quarantined_citation_is_detectable_from_the_index(tmp_path):
    store = tmp_path / "store"
    record = _one_suite_record()
    rr.write_run_record(store, record)
    run_id = record["run"]["run_id"]
    junction_id = rr.mint_junction_id(now=_stamp("2026-11-04T09:30:00Z"))
    rr.append_act(
        store / "run-index.jsonl",
        {
            "act": "quarantine",
            "junction_id": junction_id,
            "run_ids": [run_id],
        },
    )
    state = rr.fold_index(store / "run-index.jsonl")
    assert state.open_quarantine.get(run_id) == {junction_id}


# ---------------------------------------------------------------------------
# T403 — experiment citation records (fake backend)


JOB_ID = "abc123def456"
RESULTS_PAYLOAD = {
    "score": 0.5,
    "fetched": 12,
    "label": "run one",
    "rows": [1, 2, 3],
    "nested": {"a": 1},
}


def _job(**overrides) -> dict:
    job = {
        "id": JOB_ID,
        "name": "Exp run: fixture graph",
        "pipeline": "exp_run",
        "status": "completed",
        "params": {"exp_id": "graph_x", "iterations": 50},
        "created_at": "2026-11-02T07:38:47.261190+00:00",
        "updated_at": "2026-11-02 07:40:00",
        "created_by": None,
    }
    job.update(overrides)
    return job


def _reader(job, results, graph):
    def read(job_id: str):
        assert job_id == job["id"]
        return job, results, graph

    return read


def _cite(tmp_path, job, results, graph):
    return rr.cite_job(
        _reader(job, results, graph),
        job["id"],
        tmp_path / "store",
        code_version="0.1.0+dev",
        environment_class="desktop/windows",
        tool_version="0.1.0",
    )


def test_completed_job_citation_binds_job_inputs_and_payload_hash(
    tmp_path,
):
    graph = {"id": "graph_x", "version": "3", "nodes": []}
    path = _cite(tmp_path, _job(), RESULTS_PAYLOAD, graph)
    record = json.loads(path.read_text(encoding="utf-8"))
    rr.validate_record(record)
    header = record["run"]
    assert header["surface"] == "experiment"
    # The execution's own stamps, normalized from the
    # backend's mixed formats.
    assert header["started"] == "2026-11-02T07:38:47Z"
    assert header["finished"] == "2026-11-02T07:40:00Z"
    pins = header["key"]["input_pins"]
    assert pins["job_id"] == JOB_ID
    assert pins["graph_id"] == "graph_x"
    assert pins["graph_version"] == "3"
    assert pins["parameters"] == {"exp_id": "graph_x", "iterations": 50}
    assert record["job_id"] == JOB_ID
    assert record["result"]["job_id"] == JOB_ID
    # The T403 hash check: a second read of the same job
    # re-derives the recorded payload hash.
    _, results_again, _ = _reader(_job(), RESULTS_PAYLOAD, graph)(
        JOB_ID
    )
    assert record["result"]["results_sha256"] == (
        rr.canonical_payload_sha256(results_again)
    )
    # The citation resolves from the index alone.
    state = rr.fold_index(tmp_path / "store" / "run-index.jsonl")
    entry = state.entries[header["run_id"]]
    assert entry["record"] == path.name
    assert (tmp_path / "store" / entry["record"]).is_file()


def test_graph_without_a_version_is_pinned_by_its_definition_hash(
    tmp_path,
):
    graph = {"id": "graph_x", "nodes": [{"id": "n1"}]}
    path = _cite(tmp_path, _job(), RESULTS_PAYLOAD, graph)
    record = json.loads(path.read_text(encoding="utf-8"))
    pins = record["run"]["key"]["input_pins"]
    assert pins["graph_version"] is None
    assert pins["graph_definition_sha256"] == (
        rr.canonical_payload_sha256(graph)
    )


def test_failed_job_leaves_an_absence_record_not_a_result(tmp_path):
    path = _cite(
        tmp_path,
        _job(status="failed", updated_at="2026-11-02 07:39:00"),
        None,
        None,
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    assert "result" not in record
    assert record["absence"]["kind"] == "crashed"
    assert "failed" in record["absence"]["detail"]
    state = rr.fold_index(tmp_path / "store" / "run-index.jsonl")
    assert record["run"]["run_id"] in state.entries


def test_cancelled_job_leaves_an_absence_record(tmp_path):
    path = _cite(
        tmp_path,
        _job(status="cancelled", updated_at="2026-11-02 07:39:00"),
        None,
        None,
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["absence"]["kind"] == "crashed"
    assert "cancelled" in record["absence"]["detail"]


def test_completed_job_without_results_is_an_empty_absence(tmp_path):
    path = _cite(tmp_path, _job(), None, {"id": "graph_x", "version": "3"})
    record = json.loads(path.read_text(encoding="utf-8"))
    assert "result" not in record
    assert record["absence"]["kind"] == "empty"


def test_running_job_refuses_and_writes_nothing(tmp_path):
    with pytest.raises(rr.RunRecordError):
        _cite(tmp_path, _job(status="running"), None, None)
    assert not (tmp_path / "store").exists()


def test_mechanical_summary_quotes_scalars_and_sizes_the_rest():
    assert rr.mechanical_result_summary(RESULTS_PAYLOAD) == {
        "score": 0.5,
        "fetched": 12,
        "label": "run one",
        "rows": {"type": "list", "count": 3},
        "nested": {"type": "object", "count": 1},
    }


# ---------------------------------------------------------------------------
# CLI teeth (subprocess, the repo's convention)


def test_suite_cli_writes_a_record_from_an_output_file(tmp_path):
    root = _git_tree(tmp_path / "cli")
    (root / "glossa-indus" / "claims" / "a.json").write_text(
        '{"a": 2}\n', encoding="utf-8"
    )
    output = tmp_path / "cli" / "pytest-output.txt"
    output.write_text(
        "5 passed, 1 skipped in 2.50s\n", encoding="utf-8"
    )
    store = tmp_path / "cli" / "store"
    proc = subprocess.run(
        [
            sys.executable, str(SUITE_CLI),
            "--root", str(root),
            "--output", str(output),
            "--command", "python -m pytest tests/ -q",
            "--selection", "tests/",
            "--store", str(store),
            "--restore", "glossa-indus/claims/a.json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    records = list(store.glob("suite-*.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    rr.validate_record(record)
    assert record["result"]["summary"] == {
        "passed": 5,
        "failed": 0,
        "errors": 0,
        "skipped": 1,
    }
    manifest = record["tree"]["rewrite_manifest"]
    assert [entry["path"] for entry in manifest] == [
        "glossa-indus/claims/a.json"
    ]
    assert manifest[0]["disposition"] == "restored"
    assert (root / "glossa-indus" / "claims" / "a.json").read_bytes() == (
        b'{"a": 1}\n'
    )
    state = rr.fold_index(store / "run-index.jsonl")
    assert record["run"]["run_id"] in state.entries


def test_suite_cli_refuses_an_undisposed_rewrite(tmp_path):
    root = _git_tree(tmp_path / "cli2")
    (root / "glossa-indus" / "claims" / "a.json").write_text(
        '{"a": 2}\n', encoding="utf-8"
    )
    output = tmp_path / "cli2" / "pytest-output.txt"
    output.write_text("5 passed in 2.50s\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable, str(SUITE_CLI),
            "--root", str(root),
            "--output", str(output),
            "--command", "python -m pytest tests/ -q",
            "--selection", "tests/",
            "--store", str(tmp_path / "cli2" / "store"),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert proc.returncode == 1
    assert "refused" in proc.stderr
    assert "no disposition" in proc.stderr


def test_job_citation_cli_refuses_an_unreachable_backend(tmp_path):
    proc = subprocess.run(
        [
            sys.executable, str(CITATION_CLI), JOB_ID,
            "--store", str(tmp_path / "store"),
            "--base-url", "http://127.0.0.1:1",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert proc.returncode == 1
    assert "refused" in proc.stderr
    assert not (tmp_path / "store").exists()
