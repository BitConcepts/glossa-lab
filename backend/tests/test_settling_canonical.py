"""Spec 086 Stage 4 — the settling engine (T403) and its
oracle (T404).

T404's acceptance: the engine reproduces every canonical
registered in `glossa-indus/ledger/settling-canonical.json`
exactly — the five scenarios' S-R4 result blocks
field-for-field, and the one comparison's mechanical fields
(coverage deltas, claims compared, per-claim divergences,
signs assigned by one only, expectations named). The
comparison's expectations note is the one registered field
whose text is not wholly mechanical: its first clause is the
derivable absence statement and is asserted verbatim; the
remainder is brief-specific prose from the T405 brief,
recorded as FINDING-S4-1 in the stage record, not silently
matched and not edited.

The canonicals are the oracle: a mismatch is an engine
defect, fixed in the engine — the expectations in the
registered artifact are never edited to fit.

Also pinned: the assignment sets of record (incumbent 94,
full-register 286 — the register's 287th record, H003,
belongs to a frame the anchors file does not name and is
out of v1 scope, counted not dropped); the engine's
refusals (a candidate assigning one sign twice; a register
whose stored strict flags disagree with the recomputation;
a comparison over two ledger builds); run-store discipline
(a run writes its run record and nothing else — T403's
acceptance); evaluation purity (the pure builders write
nothing); determinism (two evaluations of one scenario are
byte-identical); and the live V9 pass — the Stage 3 import
audit, armed before the engine existed, passes over the
real engine and names it in its scan count.

Real-tree precondition: like the Stage 2/3 tests, the
oracle builds over the committed tree, whose source files
the ledger mirrors by canonical hash; the pre-existing
test_indus_evidence_api.py rewrites those files in-tree
when it runs first in a suite process, in which case the
engine refuses by design. The tests verify that
precondition mechanically before running — the gate's V1
recorded-source-hash arm alone — and skip with the cause
named only when that arm names diverged files (assertions
unchanged wherever the precondition holds).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from glossa_lab import ledger_gate as lg
from glossa_lab import run_records as rr
from glossa_lab import settling as st

ROOT = Path(__file__).resolve().parents[2]
PARPOLA = "parpola_2010_dravidian_solution_manual_002"


def _check(report: lg.GateReport, prefix: str) -> lg.Check:
    matches = [c for c in report.checks if c.name.startswith(prefix)]
    assert matches, f"no check named {prefix!r} in the gate output"
    return matches[0]


_DIVERGENCE_RE = re.compile(
    r"recorded (?:sidecar )?sha256 for (?P<hashed>\S+) does not match"
    r"|(?:source|sidecar) (?P<missing>\S+) not found"
)


def _recorded_source_hash_divergences(root: Path) -> list[str]:
    report = lg.run_gate(root, scope={"V1"})
    arm = _check(report, "V1 recorded source hashes")
    if arm.status != "FAIL":
        return []
    paths: list[str] = []
    for ev in arm.evidence:
        for match in _DIVERGENCE_RE.finditer(ev):
            paths.append(match.group("hashed") or match.group("missing"))
    return paths


def _require_recorded_hashes(root: Path) -> None:
    diverged = _recorded_source_hash_divergences(root)
    if diverged:
        pytest.skip(
            "clean-tree precondition destroyed in this suite "
            "process: the evidence-API tests rewrote source "
            "files the ledger mirrors by hash ("
            + ", ".join(sorted(set(diverged))[:4])
            + "); the engine refuses over diverged sources "
            "by design"
        )


def _divergences(expected, actual, path: str, out: list[str]) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            if key not in actual:
                out.append(f"{path}.{key}: missing from engine output")
            else:
                _divergences(
                    expected[key], actual[key], f"{path}.{key}", out
                )
        for key in actual:
            if key not in expected:
                out.append(f"{path}.{key}: unexpected in engine output")
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            out.append(
                f"{path}: engine produced {len(actual)} item(s), "
                f"canonical registers {len(expected)}"
            )
        for i, (e_item, a_item) in enumerate(zip(expected, actual)):
            _divergences(e_item, a_item, f"{path}[{i}]", out)
    elif expected != actual:
        out.append(f"{path}: engine {actual!r} != canonical {expected!r}")


@pytest.fixture(scope="module")
def state() -> st.SettleState:
    _require_recorded_hashes(ROOT)
    return st.load_state(ROOT)


@pytest.fixture(scope="module")
def canonical() -> dict:
    return json.loads((ROOT / st.CANONICAL_REL).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# T404 — the oracle: every registered canonical reproduces exactly


def test_canonical_provenance_matches_the_tree(state, canonical):
    """The canonicals were derived against pinned inputs; the
    engine's pins over this tree must be the registered ones
    (a tree the canonicals do not describe is not an oracle
    discrepancy — it is a different build)."""
    prov = canonical["provenance"]
    assert state.pins["ledger"]["sha256"] == prov["ledger"]["sha256_canonical"]
    assert state.pins["ledger"]["lines"] == prov["ledger"]["lines"]
    anchors = prov["anchors_register"]
    pin = state.pins["anchors_register"]
    assert pin["sha256_raw_bytes"] == anchors["sha256_raw_bytes"]
    assert pin["bytes"] == anchors["bytes"]
    assert pin["records"] == anchors["records"]
    assert pin["strict"] == anchors["strict"]
    corpus = prov["corpus_snapshot"]
    assert state.pins["corpus_snapshot"]["sha256"] == corpus["sha256_canonical"]


def test_every_canonical_scenario_reproduces_exactly(state, canonical):
    for scenario in canonical["scenarios"]:
        record = st.run_record(
            state,
            scenario["inputs"]["candidate"],
            scenario["inputs"]["scope"],
            scenario=scenario["id"],
        )
        out: list[str] = []
        _divergences(
            scenario["expected"], record["result"], scenario["id"], out
        )
        assert not out, (
            f"scenario {scenario['id']} diverges from the "
            "registered canonical (an engine defect — the "
            "canonical is the oracle):\n" + "\n".join(out)
        )
        assert record["result"] == scenario["expected"]


def test_the_canonical_comparison_reproduces(state, canonical):
    comparison = canonical["comparisons"][0]
    by_id = {s["id"]: s for s in canonical["scenarios"]}
    records = {}
    for scenario_id in comparison["inputs"]["runs"]:
        scenario = by_id[scenario_id]
        records[scenario_id] = st.run_record(
            state,
            scenario["inputs"]["candidate"],
            scenario["inputs"]["scope"],
            scenario=scenario_id,
        )
    record = st.compare_runs(
        records[comparison["inputs"]["runs"][0]],
        records[comparison["inputs"]["runs"][1]],
    )
    expected = dict(comparison["expected"])
    registered_note = expected.pop("pre_registered_expectations_note")
    actual = dict(record["result"])
    engine_note = actual.pop("pre_registered_expectations_note")
    out: list[str] = []
    _divergences(expected, actual, comparison["id"], out)
    assert not out, (
        "the comparison's mechanical fields diverge from the "
        "registered canonical:\n" + "\n".join(out)
    )
    # FINDING-S4-1: the registered note's first clause is the
    # mechanically derivable absence statement; the engine
    # must reproduce it verbatim. The remainder names the
    # T405 brief's own expectation (Spec 074 / the Yadav
    # claim), which no registered rule derives — recorded in
    # the stage record, asserted here as exactly that split.
    assert engine_note == registered_note.split(";")[0] + "."
    assert "yadav_2009_arxiv_manual_002" in registered_note


def test_run_records_carry_the_label_and_the_value_independence_statement(
    state, canonical
):
    scenario = canonical["scenarios"][1]
    record = st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
    )
    assert record["label"] == st.SETTLING_LABEL
    assert record["semantics"] == "glossa-settle-1"
    assert "value-independent" in record["s_r2_value_independence"]


def test_evaluation_is_deterministic(state, canonical):
    # Spec 089 Stage 2: a run record carries its run-defs
    # header, whose id and stamps are execution facts —
    # determinism is asserted over identical inputs
    # INCLUDING the header (the same header heading two
    # evaluations of one scenario): byte-identical dumps.
    scenario = canonical["scenarios"][2]
    header = st.settling_run_header(
        state.pins,
        command="run_settling.py run --scenario determinism-fixture",
        tool="run_settling.py run",
        run_id="settling-20261104T000000Z-abcdef",
        started="2026-11-04T00:00:00Z",
        finished="2026-11-04T00:00:01Z",
    )
    first = st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
        header=header,
    )
    second = st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
        header=header,
    )
    assert st._dump(first) == st._dump(second)


# ---------------------------------------------------------------------------
# T403 — the assignment sets of record


def test_assignment_sets_of_record(state):
    artifact = st.build_assignment_sets(state)
    sets = {record["id"]: record for record in artifact["sets"]}
    assert len(sets["incumbent"]["assignments"]) == 94
    assert len(sets["full-register"]["assignments"]) == 286
    # The register's 287th record is out of frame and out of
    # every set — counted in the artifact, never dropped.
    assert artifact["register"]["records"] == 287
    assert artifact["out_of_frame_records"] == ["H003"]
    full_keys = {
        f"M{int(a['sign'].split(':')[1]):03d}"
        for a in sets["full-register"]["assignments"]
    }
    assert full_keys == {k for k in state.anchors if k.startswith("M")}
    # Every assignment carries the register's recorded
    # reading, verbatim; the incumbent set is exactly the
    # recomputed strict set.
    for record in sets.values():
        for assignment in record["assignments"]:
            number = int(assignment["sign"].split(":")[1])
            key = f"M{number:03d}"
            assert assignment["value"] == state.anchors[key]["reading"]
    incumbent_keys = {
        f"M{int(a['sign'].split(':')[1]):03d}"
        for a in sets["incumbent"]["assignments"]
    }
    assert incumbent_keys == state.strict
    # M070's recorded reading is carried verbatim.
    m70 = [
        a
        for a in sets["incumbent"]["assignments"]
        if a["sign"] == "mahadevan:70"
    ]
    assert m70 == [{"sign": "mahadevan:70", "value": "vēl"}]
    # Provenance is present on every set of record.
    for record in sets.values():
        assert record["provenance"]["register_sha256_raw_bytes"] == (
            state.pins["anchors_register"]["sha256_raw_bytes"]
        )


def test_assignment_sets_materialization_is_byte_deterministic(state):
    first = st._dump(st.build_assignment_sets(state))
    second = st._dump(st.build_assignment_sets(state))
    assert first == second
    on_disk = json.loads(
        (ROOT / st.ASSIGNMENT_SETS_REL).read_text(encoding="utf-8")
    )
    # Spec 089 Stage 2: a materialized artifact also names
    # its producing run (C089-7) — the binding is the one
    # execution-scoped part and is not content. The
    # standing artifact predates the binding and carries
    # none; the content comparison holds modulo it.
    on_disk.pop("producing_run", None)
    assert st._dump(on_disk) == first, (
        "the committed assignment-sets.json differs from a "
        "fresh build over the pinned register — regenerate "
        "with tools/ledger/run_settling.py materialize-sets"
    )


# ---------------------------------------------------------------------------
# Refusals — the engine names defects instead of settling
# over them


def test_a_candidate_assigning_one_sign_twice_is_refused(state):
    candidate = {
        "id": "test-double-assignment",
        "assignments": [
            {"sign": "mahadevan:70", "value": "vēl"},
            {"sign": "mahadevan:070", "value": "ka"},
        ],
    }
    with pytest.raises(st.SettlingError, match="twice"):
        st.run_record(state, candidate, ["mahadevan:70"])


def test_a_comparison_over_two_ledger_builds_is_refused(state, canonical):
    scenario = canonical["scenarios"][1]
    record = st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
    )
    other = json.loads(json.dumps(record))
    other["candidate"] = "someone-else"
    other["pins"] = json.loads(json.dumps(record["pins"]))
    other["pins"]["ledger"]["sha256"] = "0" * 64
    with pytest.raises(st.SettlingError, match="different ledger builds"):
        st.compare_runs(record, other)


def test_a_register_whose_stored_flags_disagree_is_refused(tmp_path):
    """A scratch tree whose anchors copy carries one flipped
    stored strict_set flag: recomputation and the stored
    flags disagree, and the run refuses (semantics §1)."""
    _require_recorded_hashes(ROOT)
    for name in ("glossa-indus", "glossa-corpus", "reports"):
        target = tmp_path / name
        if (ROOT / name).is_dir():
            target.symlink_to(ROOT / name, target_is_directory=True)
    reports_dir = tmp_path / "backend" / "reports"
    reports_dir.mkdir(parents=True)
    anchors = json.loads(
        (ROOT / st.ANCHORS_REL).read_text(encoding="utf-8")
    )
    assert anchors["anchors"]["M064"]["strict_set"] is False
    anchors["anchors"]["M064"]["strict_set"] = True
    (reports_dir / "INDUS_FINAL_ANCHORS.json").write_text(
        json.dumps(anchors, ensure_ascii=False), encoding="utf-8"
    )
    with pytest.raises(st.SettlingError, match="strict"):
        st.load_state(tmp_path)


# ---------------------------------------------------------------------------
# Store discipline and purity (T403's acceptance)


def _tree_hashes(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for base in ("glossa-indus/ledger",):
        for path in sorted((root / base).rglob("*")):
            if path.is_file():
                out[str(path.relative_to(root))] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
    return out


def test_evaluation_writes_nothing(state, canonical):
    # T405 stored the first run records in the run store,
    # so the store is populated by design from that task
    # on; the acceptance pinned here is purity — a pure
    # evaluation changes no hash anywhere under the
    # ledger tree, the populated run store included
    # (Spec 086 T405; stage-4-record.md, T405 section).
    before = _tree_hashes(ROOT)
    scenario = canonical["scenarios"][1]
    st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
    )
    st.build_assignment_sets(state)
    assert _tree_hashes(ROOT) == before


def test_a_run_writes_only_its_run_record(state, canonical, tmp_path):
    scenario = canonical["scenarios"][1]
    # Spec 089 Stage 2: a stored record carries a real
    # (non-ephemeral) run header and lands under its run
    # id; the write-surface acceptance is unchanged — one
    # record file, and nothing else.
    header = st.settling_run_header(
        state.pins,
        command="run_settling.py run --scenario write-surface-fixture",
        tool="run_settling.py run",
        run_id=rr.mint_run_id("settling"),
        started="2026-11-04T00:00:00Z",
        finished="2026-11-04T00:00:01Z",
    )
    record = st.run_record(
        state,
        scenario["inputs"]["candidate"],
        scenario["inputs"]["scope"],
        scenario=scenario["id"],
        header=header,
    )
    written = st.write_run_record(tmp_path, record)
    files = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert files == [written]
    assert written.parent == tmp_path / st.RUN_STORE_REL
    loaded = json.loads(written.read_text(encoding="utf-8"))
    assert loaded == record
    # The store-hash acceptance over the real tree: writing
    # into the real run store changes exactly one path.
    before = _tree_hashes(ROOT)
    real_written = st.write_run_record(ROOT, record)
    try:
        after = _tree_hashes(ROOT)
        changed = {
            path
            for path in set(before) | set(after)
            if before.get(path) != after.get(path)
        }
        assert changed == {str(real_written.relative_to(ROOT))}
    finally:
        real_written.unlink()
        runs_dir = ROOT / st.RUN_STORE_REL
        if runs_dir.exists() and not any(runs_dir.iterdir()):
            runs_dir.rmdir()


# ---------------------------------------------------------------------------
# The live V9 pass — the audit armed at Stage 3 passes over
# the real engine


def test_v9_settling_import_audit_passes_over_the_real_engine():
    _require_recorded_hashes(ROOT)
    report = lg.run_gate(ROOT, scope={"V9"})
    audit = _check(report, "V9 no write path — settling/scenario import audit")
    assert audit.status == "PASS", audit.evidence
    match = re.search(r"(\d+) settling/scenario module", audit.evidence[0])
    assert match and int(match.group(1)) >= 1, audit.evidence
    # And directly: the engine's own imports carry no write
    # entry point.
    import ast

    tree = ast.parse(
        (ROOT / "backend/glossa_lab/settling.py").read_text(encoding="utf-8")
    )
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
    assert not (imported & set(lg.WRITE_ENTRY_POINTS))
