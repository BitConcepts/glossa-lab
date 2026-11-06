"""Spec 089 Stage 2 — settling surface adoption (T201–T203).

The write path's teeth, on tmp mirror trees throughout
(the standing store gains only its run index in this
stage — covered by the last test, read-only):

- the same basis run twice produces two records with
  distinct execution-minted ids and byte-equal result
  blocks; the first record's bytes are identical after
  the second run; the index folds both entries plus
  exactly one supersedes act (the second run supersedes
  the first) and the census is monotonic;
- a run over a mutated pin produces a record whose
  constitutive key diff against the unmutated run is
  exactly the input pins, and within them exactly the
  ledger pin;
- a write whose target already exists refuses — a
  minted-id write repeated, and a hand-placed colliding
  file — and the existing bytes are untouched;
- ephemeral (in-memory) and headerless records are
  refused by the write path and never land;
- a refused execution and a crashed execution each
  leave the absence record run-defs v2 §3.2 prescribes
  (kind refused / crashed), with an index entry, and no
  result block;
- materialize-sets is a run: the artifact names its
  producing run, a materialization run record lands in
  the store naming the artifact and its bytes' hash,
  and an unbound artifact write refuses;
- verify-canonicals still reproduces 6/6 through the
  CLI (its in-memory records carry ephemeral headers
  and are never written).

The mirror trees symlink the real tree's read-only
inputs and give the store (and, where a test needs it,
the ledger or the assignment-sets artifact) a real tmp
home, in the shape of test_settling_canonical.py's
scratch-tree precedent. The clean-tree precondition is
the same one the canonical oracle states: if another
suite process rewrote the ledger's mirrored sources
in-tree, the V1 arm names them and these tests skip
with the cause named.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from glossa_lab import ledger_gate as lg
from glossa_lab import run_records as rr
from glossa_lab import settling as st

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "ledger" / "run_settling.py"
CANONICAL = json.loads((ROOT / st.CANONICAL_REL).read_text(encoding="utf-8"))
SCENARIO = next(
    s for s in CANONICAL["scenarios"] if s["id"] == "incumbent-over-subset"
)
SCOPE_ARG = ",".join(SCENARIO["inputs"]["scope"])


# ---------------------------------------------------------------------------
# The clean-tree precondition (the canonical oracle's own)


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


# ---------------------------------------------------------------------------
# Mirror trees + the CLI


def _mirror_root(
    tmp_path: Path,
    *,
    ledger_writable: bool = False,
    assignment_sets_writable: bool = False,
    corrupt_anchors: bool = False,
) -> Path:
    """A tmp root over the real tree's inputs: read-only
    inputs are symlinks; the run store is a real empty
    directory; the ledger / assignment-sets artifact are
    real copies where a test must write them."""
    _require_recorded_hashes(ROOT)
    root = tmp_path / "root"
    root.mkdir(parents=True)
    for name in ("specs", "glossa-corpus", "reports"):
        (root / name).symlink_to(ROOT / name, target_is_directory=True)
    reports_dir = root / "backend" / "reports"
    reports_dir.mkdir(parents=True)
    anchors_src = ROOT / st.ANCHORS_REL
    if corrupt_anchors:
        anchors = json.loads(anchors_src.read_text(encoding="utf-8"))
        assert anchors["anchors"]["M064"]["strict_set"] is False
        anchors["anchors"]["M064"]["strict_set"] = True
        (reports_dir / "INDUS_FINAL_ANCHORS.json").write_text(
            json.dumps(anchors, ensure_ascii=False), encoding="utf-8"
        )
    else:
        (reports_dir / "INDUS_FINAL_ANCHORS.json").symlink_to(anchors_src)
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
    if ledger_writable:
        shutil.copyfile(
            ROOT / "glossa-indus" / "ledger" / "claims.jsonl",
            ledger / "claims.jsonl",
        )
    else:
        (ledger / "claims.jsonl").symlink_to(
            ROOT / "glossa-indus" / "ledger" / "claims.jsonl"
        )
    if assignment_sets_writable:
        shutil.copyfile(
            ROOT / st.ASSIGNMENT_SETS_REL, ledger / "assignment-sets.json"
        )
    else:
        (ledger / "assignment-sets.json").symlink_to(
            ROOT / st.ASSIGNMENT_SETS_REL
        )
    (ledger / "runs").mkdir()
    return root


def _cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), "--root", str(root), *args],
        capture_output=True,
        text=True,
        timeout=300,
    )


def _run_scenario(root: Path) -> subprocess.CompletedProcess:
    return _cli(
        root,
        "run",
        "--candidate", "incumbent",
        "--scope", SCOPE_ARG,
        "--scenario", SCENARIO["id"],
    )


def _store_records(root: Path) -> list[Path]:
    return sorted((root / st.RUN_STORE_REL).glob("*.json"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# T201/T203 — the same basis twice: two records, one
# supersession, monotonic census, no overwrite


def test_same_basis_twice_two_records_one_supersession(tmp_path):
    root = _mirror_root(tmp_path)
    index_path = st.run_index_path(root)

    first = _run_scenario(root)
    assert first.returncode == 0, first.stderr
    records = _store_records(root)
    assert len(records) == 1
    first_path = records[0]
    first_hash = _sha256(first_path)
    first_record = json.loads(first_path.read_text(encoding="utf-8"))
    state1 = rr.fold_index(index_path)
    assert state1.census == 1

    second = _run_scenario(root)
    assert second.returncode == 0, second.stderr
    records = _store_records(root)
    assert len(records) == 2
    # The first record is preserved byte-untouched.
    assert _sha256(first_path) == first_hash
    second_path = next(p for p in records if p != first_path)
    second_record = json.loads(second_path.read_text(encoding="utf-8"))

    # Identity: distinct execution-minted ids, filenames
    # derived from them; byte-equal result blocks.
    first_id = first_record["run"]["run_id"]
    second_id = second_record["run"]["run_id"]
    assert first_id != second_id
    assert first_path.name == f"{first_id}.json"
    assert second_path.name == f"{second_id}.json"
    assert first_record["result"] == second_record["result"]
    assert (
        json.dumps(first_record["result"], sort_keys=True)
        == json.dumps(second_record["result"], sort_keys=True)
    )

    # The header: key pins are the record's pins block
    # verbatim; the seed is the registered no-seed marker.
    for record in (first_record, second_record):
        header = record["run"]
        assert header["surface"] == "settling"
        assert header["determinism_class"] == "deterministic"
        assert header["key"]["input_pins"] == record["pins"]
        assert header["key"]["seed"] == rr.NO_SEED
        assert "ephemeral" not in header

    # The index folds both entries and exactly one
    # supersession — the second run supersedes the first —
    # and the census only grew.
    state2 = rr.fold_index(index_path)
    assert state2.census == 2
    assert set(state2.entries) == {first_id, second_id}
    assert state2.superseded_by == {first_id: second_id}


def test_a_third_run_supersedes_the_second_not_the_first(tmp_path):
    root = _mirror_root(tmp_path)
    ids = []
    for _ in range(3):
        proc = _run_scenario(root)
        assert proc.returncode == 0, proc.stderr
        state = rr.fold_index(st.run_index_path(root))
        ids.append(state.order[-1])
    state = rr.fold_index(st.run_index_path(root))
    assert state.census == 3
    # Linear chain: run 2 supersedes run 1, run 3 run 2 —
    # the fold's single-successor rule is never refused.
    assert state.superseded_by == {ids[0]: ids[1], ids[1]: ids[2]}
    assert len(_store_records(root)) == 3


# ---------------------------------------------------------------------------
# T203 — a mutated pin: the key diff is exactly the pin


def test_mutated_pin_key_diff_is_exactly_the_pin(tmp_path):
    base_root = _mirror_root(tmp_path / "base")
    proc = _run_scenario(base_root)
    assert proc.returncode == 0, proc.stderr
    base_record = json.loads(
        _store_records(base_root)[0].read_text(encoding="utf-8")
    )

    mutated_root = _mirror_root(
        tmp_path / "mutated", ledger_writable=True
    )
    ledger_path = mutated_root / "glossa-indus" / "ledger" / "claims.jsonl"
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {"id": "spec089-s2-mutation-probe", "kind": "claim"}
            )
            + "\n"
        )
    proc = _run_scenario(mutated_root)
    assert proc.returncode == 0, proc.stderr
    mutated_record = json.loads(
        _store_records(mutated_root)[0].read_text(encoding="utf-8")
    )

    diff = rr.constitutive_diff(
        base_record["run"]["key"], mutated_record["run"]["key"]
    )
    assert diff == ["input_pins"]
    base_pins = base_record["pins"]
    mutated_pins = mutated_record["pins"]
    assert mutated_pins["ledger"]["sha256"] != base_pins["ledger"]["sha256"]
    assert mutated_pins["ledger"]["lines"] == base_pins["ledger"]["lines"] + 1
    for component in ("anchors_register", "phase108_register",
                      "corpus_snapshot"):
        assert mutated_pins[component] == base_pins[component]


# ---------------------------------------------------------------------------
# T201 — collision refusal at the write path


def _fixture_record(run_id: str, finished: str) -> dict:
    header = st.settling_run_header(
        {"ledger": {"sha256": "0" * 64, "lines": 1}},
        command="run_settling.py run --scenario collision-fixture",
        tool="run_settling.py run",
        run_id=run_id,
        started="2026-11-04T00:00:00Z",
        finished=finished,
    )
    return {"run": header, "result": {"fixture": True}}


def test_a_colliding_write_refuses_and_preserves_bytes(tmp_path):
    run_id = "settling-20261104T000000Z-c01115"
    record = _fixture_record(run_id, "2026-11-04T00:00:01Z")
    written = st.write_run_record(tmp_path, record)
    before = written.read_bytes()
    replay = _fixture_record(run_id, "2026-11-04T00:00:02Z")
    with pytest.raises(st.SettlingError, match="already exists"):
        st.write_run_record(tmp_path, replay)
    assert written.read_bytes() == before


def test_a_hand_placed_colliding_file_is_refused_not_overwritten(tmp_path):
    run_id = "settling-20261104T000000Z-beef42"
    store = tmp_path / st.RUN_STORE_REL
    store.mkdir(parents=True)
    target = store / f"{run_id}.json"
    target.write_bytes(b"hand-placed, not a run record\n")
    record = _fixture_record(run_id, "2026-11-04T00:00:01Z")
    with pytest.raises(st.SettlingError, match="already exists"):
        st.write_run_record(tmp_path, record)
    assert target.read_bytes() == b"hand-placed, not a run record\n"


def test_ephemeral_and_headerless_records_are_never_written(tmp_path):
    pins = {"ledger": {"sha256": "0" * 64, "lines": 1}}
    ephemeral_header = st.settling_run_header(
        pins,
        command="in-memory recomputation (fixture)",
        tool="glossa_lab.settling",
        ephemeral=True,
    )
    with pytest.raises(st.SettlingError, match="ephemeral"):
        st.write_run_record(
            tmp_path, {"run": ephemeral_header, "result": {}}
        )
    with pytest.raises(st.SettlingError, match="no run header"):
        st.write_run_record(tmp_path, {"result": {}})
    assert not list(tmp_path.rglob("*.json"))


# ---------------------------------------------------------------------------
# T201 — no-result executions leave absence records


def test_a_refusal_before_state_load_leaves_an_absence_record(tmp_path):
    root = _mirror_root(tmp_path, corrupt_anchors=True)
    proc = _run_scenario(root)
    assert proc.returncode == 1
    assert "SETTLING REFUSED" in proc.stderr
    records = _store_records(root)
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert "result" not in record
    assert record["absence"]["kind"] == "refused"
    assert "strict" in record["absence"]["detail"]
    # The state never loaded: no pins exist to record.
    assert "pins" not in record
    assert record["run"]["key"]["input_pins"] == {}
    state = rr.fold_index(st.run_index_path(root))
    assert set(state.entries) == {record["run"]["run_id"]}


def test_a_refusal_after_state_load_leaves_an_absence_record(tmp_path):
    root = _mirror_root(tmp_path)
    candidate_path = tmp_path / "double-assignment.json"
    candidate_path.write_text(
        json.dumps(
            {
                "id": "s2-double-assignment",
                "assignments": [
                    {"sign": "mahadevan:70", "value": "vēl"},
                    {"sign": "mahadevan:070", "value": "ka"},
                ],
            }
        ),
        encoding="utf-8",
    )
    proc = _cli(
        root, "run",
        "--candidate", str(candidate_path),
        "--scope", "mahadevan:70",
        "--scenario", "s2-refusal-fixture",
    )
    assert proc.returncode == 1
    assert "SETTLING REFUSED" in proc.stderr
    records = _store_records(root)
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert "result" not in record
    assert record["absence"]["kind"] == "refused"
    assert "twice" in record["absence"]["detail"]
    # The state loaded before the refusal: its pins are
    # the record's, and the key carries them verbatim.
    assert record["run"]["key"]["input_pins"] == record["pins"]


def test_a_crash_leaves_an_absence_record_not_a_half_result(tmp_path):
    root = _mirror_root(tmp_path)
    candidate_path = tmp_path / "malformed.json"
    candidate_path.write_text("{not json", encoding="utf-8")
    proc = _cli(
        root, "run",
        "--candidate", str(candidate_path),
        "--scope", "mahadevan:70",
        "--scenario", "s2-crash-fixture",
    )
    assert proc.returncode != 0
    records = _store_records(root)
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert "result" not in record
    assert record["absence"]["kind"] == "crashed"
    assert record["absence"]["detail"].startswith("JSONDecodeError")
    state = rr.fold_index(st.run_index_path(root))
    assert set(state.entries) == {record["run"]["run_id"]}


# ---------------------------------------------------------------------------
# T203 — materialize-sets is a run; the artifact names it


def test_materialize_sets_becomes_a_run(tmp_path):
    root = _mirror_root(tmp_path, assignment_sets_writable=True)
    artifact_path = root / st.ASSIGNMENT_SETS_REL
    before = json.loads(artifact_path.read_text(encoding="utf-8"))
    # The mirror's artifact is the standing one. Until
    # Spec 089 Stage 5 it stood unbound, and this test
    # asserted that premise; Stage 5 executed the binding
    # materialize-sets run over it (the act V11's leg (a)
    # verifies), so the invariant is restated to what it
    # always meant: a materialize-sets execution (re)binds
    # the artifact to ITS OWN run, and the content modulo
    # the binding is the pure build's, unchanged.
    before_unbound = dict(before)
    before_unbound.pop("producing_run", None)
    prior_run = (before.get("producing_run") or {}).get("run_id")

    proc = _cli(root, "materialize-sets")
    assert proc.returncode == 0, proc.stderr

    after = json.loads(artifact_path.read_text(encoding="utf-8"))
    run_id = after["producing_run"]["run_id"]
    assert run_id != prior_run
    assert after["producing_run"]["surface"] == "settling"
    # Content is the pure build's; only the binding moved.
    stripped = dict(after)
    del stripped["producing_run"]
    assert stripped == before_unbound

    records = _store_records(root)
    assert [p.name for p in records] == [f"{run_id}.json"]
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert record["artifact"] == "settling materialization record"
    assert record["result"]["materialized"] == st.ASSIGNMENT_SETS_REL
    assert record["result"]["artifact_sha256"] == _sha256(artifact_path)
    assert record["result"]["producing_run"] == run_id
    assert record["run"]["key"]["input_pins"] == record["pins"]
    state = rr.fold_index(st.run_index_path(root))
    assert set(state.entries) == {run_id}
    # The artifact still loads as the sets of record.
    assert set(st.load_assignment_sets(root)) == {
        "incumbent",
        "full-register",
    }


def test_an_unbound_assignment_sets_write_refuses(tmp_path):
    state_free_artifact = {"sets": [], "register": {}}
    with pytest.raises(st.SettlingError, match="producing-run binding"):
        st.write_assignment_sets(tmp_path, state_free_artifact)
    assert not (tmp_path / st.ASSIGNMENT_SETS_REL).exists()


# ---------------------------------------------------------------------------
# T202 — canonicals through the CLI, 6/6, nothing written


def test_verify_canonicals_reproduces_six_of_six_and_writes_nothing():
    _require_recorded_hashes(ROOT)
    store = ROOT / st.RUN_STORE_REL
    before = {p.name: _sha256(p) for p in store.glob("*") if p.is_file()}
    proc = _cli(ROOT, "verify-canonicals")
    assert proc.returncode == 0, proc.stderr
    assert "6/6 registered canonicals reproduce" in proc.stdout
    after = {p.name: _sha256(p) for p in store.glob("*") if p.is_file()}
    assert after == before


# ---------------------------------------------------------------------------
# T202 — the standing store's index (built by this stage)


def test_the_standing_store_index_covers_the_pair_by_legacy_entries():
    store = ROOT / st.RUN_STORE_REL
    index_path = st.run_index_path(ROOT)
    assert index_path.is_file(), (
        "the settling store carries no run index — Stage 2 "
        "builds it over the standing pair"
    )
    state = rr.fold_index(index_path)
    record_files = sorted(store.glob("*.json"))
    # The folded census covers every standing record
    # file (each is named by an entry act). Until Stage 5
    # the census equaled the file count exactly; T501's
    # legacy completion also enters the store's
    # superseded generations and the canonical
    # re-derivation events, so the census now exceeds the
    # standing files — coverage, not equality, is the
    # invariant (restated at Stage 5).
    entered_records = {
        entry["record"]
        for entry in state.entries.values()
        if "event" not in entry
    }
    assert {p.name for p in record_files} <= entered_records
    # The legacy assertions below govern the pre-spec
    # pair (the headerless records); post-spec records
    # stand entered under their own minted ids. The pair
    # departed the standing store at the Spec 093 intake
    # replay (2026-11-05): its entries stand in the folded
    # index, and its departure is accounted by departure
    # acts (run-defs v2 §7.1) whose blob hashes name the
    # pair's preserved fixture bytes
    # (tests/fixtures/legacy_t405_pair/).
    fixtures = (
        Path(__file__).resolve().parent / "fixtures" / "legacy_t405_pair"
    )
    for name in (
        "t405-incumbent-over-full-frame--d9f73e4c4e4e.json",
        "t405-full-register-over-full-frame--f8c86443e924.json",
    ):
        assert not (store / name).exists(), (
            "the departed pair's records must not stand in the store"
        )
        legacy_id = rr.legacy_run_id(name)
        assert legacy_id in state.entries
        entry = state.entries[legacy_id]
        assert entry["legacy"] is True
        assert entry["label"] == rr.LEGACY_LABEL
        assert entry["key_partial"] is True
        assert entry["record"] == name
        # The departure accounting resolves against the
        # preserved bytes: the act's blob hash is the
        # record's hash, and its git blob is named.
        assert legacy_id in state.departed
        departure = state.departed[legacy_id]
        assert departure["record"] == name
        record_bytes = (fixtures / name).read_bytes()
        assert (
            hashlib.sha256(record_bytes).hexdigest()
            == departure["blob_sha256"]
        )
        assert departure["git_blob"]
        assert departure["superseded_by_commit"]
        # The retired filename function still resolves the
        # legacy record's standing path from its content.
        record = json.loads(record_bytes.decode("utf-8"))
        assert "run" not in record  # pre-spec bytes, untouched
        assert st.run_record_filename(record) == name
