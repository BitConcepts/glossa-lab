"""Spec 086 Stage 3 — the verification gate (T301–T305).

The teeth battery: one seeded divergence per check class,
each required to turn the gate red and name its check —
including the Atlas failure mode as a first-class case
(T304): Spec 054's 2026-10-24 closure (outcome `STRICT
CORPUS NOT PINNABLE` — the test did not execute) cited as
support for the Yadav claim must FAIL V4 while PASSING
V1–V3 in the same run.

Also pinned: the gate's registered definition copies agree
with the generator's (DEFINITIONS.md §12 same-motion
discipline); the recorded-source-hash arm (the Stage 1
gap); the numeric arm on fixtures (the live population
carries no measurement-with-bound citation, so the gate
states it unexercised and the battery exercises it here);
write-freedom (a red gate run leaves the published
artifacts byte-identical — Amendment 1, corollary 5); and
gated publication's negative control (T303).

Real-tree precondition: like the Stage 2 tests, the
clean-tree test builds over the committed tree, whose
source files the ledger mirrors by canonical hash; the
pre-existing test_indus_evidence_api.py rewrites those
files in-tree when it runs first in a suite process, in
which case the source-hash family fails by design. The
test verifies that precondition mechanically before the
full run — the gate's V1 recorded-source-hash arm alone —
and skips with the cause named only when that arm names
diverged files (assertions unchanged wherever the
precondition holds). The scratch-tree battery shares
that precondition through its fixture — its inputs link
the same source files — so the fixture applies the same
guard: in a polluted process the battery skips with the
cause named rather than failing on a precondition it
never stated.
"""

from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

import pytest

from glossa_lab import gated_publish as gp
from glossa_lab import ledger_gate as lg
from glossa_lab import ledger_intake as li
from glossa_lab import matrix_generate as mg

ROOT = Path(__file__).resolve().parents[2]
YADAV = "yadav_2009_arxiv_manual_002"
YADAV_FILE = "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json"
PTR_2024 = f"{YADAV_FILE}:{YADAV}#spec054_outcome_append_2026_10_24"
PTR_2025 = f"{YADAV_FILE}:{YADAV}#spec054_outcome_append_2026_10_25"


def _check(report: lg.GateReport, prefix: str) -> lg.Check:
    matches = [c for c in report.checks if c.name.startswith(prefix)]
    assert matches, f"no check named {prefix!r} in the gate output"
    return matches[0]


def _artifact_hashes(root: Path) -> dict[str, str]:
    out = {}
    for rel in (
        li.LEDGER_REL,
        "glossa-indus/matrix/matrix.json",
        "glossa-indus/matrix/matrix.md",
    ):
        target = root / rel
        out[rel] = li.canonical_sha256_bytes(target.read_bytes())
    return out


# ---------------------------------------------------------------------------
# The gate's registered copies agree with the generator's


def test_gate_definitions_match_the_generator_copies():
    assert lg.GATE_MATRIX_DEFS_VERSION == mg.MATRIX_DEFS_VERSION
    assert lg.RELATIONS == mg.RELATIONS
    assert lg.COLUMN_CLASSES == mg.COLUMN_CLASSES
    assert lg.DIRECTION_RELATIONS == mg.DIRECTION_RELATIONS
    assert lg.BEARING_OUTCOMES == mg.BEARING_OUTCOMES
    assert lg.VERDICT_RELATIONS == mg.VERDICT_RELATIONS
    assert lg.COOCCURRENCE_PARAMS == mg.COOCCURRENCE_PARAMS
    assert lg.ANCHORS_REL == mg.ANCHORS_REL
    assert lg.CORPUS_REL == mg.CORPUS_REL


# ---------------------------------------------------------------------------
# T301 — the gate passes a clean tree, enumerating every check


_DIVERGENCE_RE = re.compile(
    r"recorded (?:sidecar )?sha256 for (?P<hashed>\S+) does not match"
    r"|(?:source|sidecar) (?P<missing>\S+) not found"
)


def _recorded_source_hash_divergences(root: Path) -> list[str]:
    """The clean-tree test's precondition, checked
    mechanically: run the gate's V1 recorded-source-hash
    verification alone over ``root`` and return the source
    paths it names as diverged. An empty list means every
    recorded hash still verifies — the precondition holds.
    (If the arm fails without naming a path, the list is
    empty and the full gate below fails loudly instead:
    the skip is earned by a named divergence, never
    assumed.)"""
    report = lg.run_gate(root, scope={"V1"})
    arm = _check(report, "V1 recorded source hashes")
    if arm.status != "FAIL":
        return []
    paths: list[str] = []
    for ev in arm.evidence:
        match = _DIVERGENCE_RE.search(ev)
        if match:
            path = match.group("hashed") or match.group("missing")
            if path not in paths:
                paths.append(path)
    return paths


def _require_recorded_hashes(root: Path) -> None:
    """Skip-with-cause (the Stage 2 discipline) when the
    real-tree precondition is destroyed: the gate's
    recorded-source-hash arm refuses because an earlier
    suite test (tests/test_indus_evidence_api.py) rewrote
    the extracted-claims source files in-tree. Where the
    precondition holds this returns, and the full gate in
    the caller must pass exactly as before."""
    divergences = _recorded_source_hash_divergences(root)
    if divergences:
        shown = ", ".join(divergences[:3])
        more = (
            f" (+{len(divergences) - 3} more)"
            if len(divergences) > 3
            else ""
        )
        pytest.skip(
            "clean-tree precondition destroyed: the gate's "
            "check 'V1 recorded source hashes' fails — the "
            "tree no longer matches the ledger's recorded "
            "hashes because an earlier suite test "
            "(tests/test_indus_evidence_api.py) rewrote the "
            "extracted-claims source files in-tree; the "
            "gate's refusal is the designed behavior. "
            f"Diverged: {shown}{more}"
        )


def test_gate_passes_clean_tree():
    _require_recorded_hashes(ROOT)
    report = lg.run_gate(ROOT)
    assert report.ok, report.render()
    names = [c.name for c in report.checks]
    for cls in (
        "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
        "V11",
    ):
        assert any(n.startswith(cls) for n in names), cls
    v4 = _check(report, "V4 relation-carrying")
    assert v4.status == "PASS"
    assert "1436 matrix cells" in v4.evidence[0]


def test_precondition_names_an_altered_extracted_claims_file(scratch):
    """Teeth for the precondition itself: alter one
    extracted-claims source file in a scratch tree and the
    precondition must trip, naming that file — in the
    helper's divergence list and in the skip reason."""
    target = scratch / YADAV_FILE
    data = target.read_bytes()
    target.unlink()  # replace the fixture's symlink with a real file
    target.write_bytes(data + b"\n")
    divergences = _recorded_source_hash_divergences(scratch)
    assert YADAV_FILE in divergences
    with pytest.raises(pytest.skip.Exception) as excinfo:
        _require_recorded_hashes(scratch)
    reason = str(excinfo.value)
    assert "V1 recorded source hashes" in reason
    assert YADAV_FILE in reason


def test_precondition_holds_and_full_gate_passes_on_scratch(scratch):
    """The other direction: on a pristine tree the
    precondition does not trip, and the full gate passes
    through the same entry the real-tree test uses."""
    assert _recorded_source_hash_divergences(scratch) == []
    _require_recorded_hashes(scratch)  # must not skip
    report = lg.run_gate(scratch)
    assert report.ok, report.render()


# ---------------------------------------------------------------------------
# The scratch tree (a faithful copy of the chain's inputs)


@pytest.fixture(scope="module")
def pristine_scratch(tmp_path_factory) -> Path:
    """The chain's inputs, assembled once. Files a test can
    mutate (the ledger, the matrix artifacts, the anchors
    register) are real copies; everything else is a symlink
    to the real tree — the battery never writes through a
    symlinked path, and /tmp on this class of machine is a
    small tmpfs that full copies would fill."""
    base = tmp_path_factory.mktemp("gate-pristine")
    entries = li.read_ledger(ROOT / li.LEDGER_REL)
    real_copies = {
        li.LEDGER_REL,
        li.SCHEMA_REL,
        mg.ANCHORS_REL,
        lg.PROVENANCE_REGISTER_REL,
        "glossa-indus/matrix/matrix.json",
        "glossa-indus/matrix/matrix.md",
        "glossa-indus/matrix/DEFINITIONS.md",
        lg.SETTLING_CANONICAL_REL,
    }
    linked = {mg.CORPUS_REL}
    for entry in entries:
        for source in entry.get("sources", []):
            linked.add(source["path"])
        if entry.get("kind") == "annotation":
            sidecar = (entry.get("sidecar") or {}).get("path")
            if sidecar:
                linked.add(sidecar)
    linked -= real_copies
    for rel in sorted(real_copies):
        dst = base / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    for rel in sorted(linked):
        dst = base / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(ROOT / rel)
    (base / "backend" / "glossa_lab").mkdir(parents=True, exist_ok=True)
    # The settling layer's module, linked (never written
    # through): V8's separation arm scans it in the scratch
    # tree exactly as in the real one.
    (base / "backend" / "glossa_lab" / "settling.py").symlink_to(
        ROOT / "backend" / "glossa_lab" / "settling.py"
    )
    return base


@pytest.fixture()
def scratch(pristine_scratch: Path, tmp_path: Path) -> Path:
    dst = tmp_path / "tree"
    shutil.copytree(pristine_scratch, dst, symlinks=True)
    # The battery shares the clean-tree test's precondition:
    # the scratch tree links the real tree's source files,
    # so when an earlier suite test has rewritten them
    # in-tree, the battery's inputs no longer match the
    # ledger either. Every scratch test then skips with
    # the cause named (the Stage 2 discipline) instead of
    # failing on a precondition it never stated; the
    # assertions are unchanged wherever the precondition
    # holds.
    _require_recorded_hashes(dst)
    return dst


def _rewrite_ledger(root: Path, mutate) -> None:
    entries = li.read_ledger(root / li.LEDGER_REL)
    mutate(entries)
    (root / li.LEDGER_REL).write_bytes(
        b"".join(
            json.dumps(e, ensure_ascii=False).encode("utf-8") + b"\n"
            for e in entries
        )
    )


def _rewrite_matrix(root: Path, mutate) -> None:
    path = root / "glossa-indus" / "matrix" / "matrix.json"
    matrix = json.loads(path.read_text(encoding="utf-8"))
    mutate(matrix)
    path.write_bytes(
        json.dumps(matrix, ensure_ascii=False, indent=1).encode("utf-8")
        + b"\n"
    )


# ---------------------------------------------------------------------------
# T304 — the teeth battery, one seeded divergence per class


def test_teeth_v1_altered_source_hash_fails_by_name(scratch):
    def mutate(entries):
        entry = next(e for e in entries if e["id"] == YADAV)
        source = next(
            s for s in entry["sources"] if s["role"] == "source_of_record"
        )
        source["sha256"] = "0" * 64

    _rewrite_ledger(scratch, mutate)
    report = lg.run_gate(scratch, scope={"V1"})
    assert not report.ok
    arm = _check(report, "V1 recorded source hashes")
    assert arm.status == "FAIL"
    assert any(YADAV_FILE in ev for ev in arm.evidence)


def test_teeth_v2_flipped_matrix_status_fails(scratch):
    def mutate(matrix):
        row = next(r for r in matrix["rows"] if r["id"] == YADAV)
        row["status"] = "flipped-for-teeth"

    _rewrite_matrix(scratch, mutate)
    report = lg.run_gate(scratch, scope={"V2"})
    assert not report.ok
    assert _check(report, "V2 count equivalence — claims by status").status == "FAIL"


def test_teeth_v3_flipped_cell_relation_fails(scratch):
    def mutate(matrix):
        cell = next(
            c
            for c in matrix["cells"]
            if c["row"] == YADAV and c["column_class"] == "studies"
        )
        assert cell["relation"] == "opposes"
        cell["relation"] = "supports"

    _rewrite_matrix(scratch, mutate)
    report = lg.run_gate(scratch, scope={"V3"})
    assert not report.ok
    cells = _check(report, "V3 matrix recomputation — cells")
    assert cells.status == "FAIL"
    assert any(YADAV in ev for ev in cells.evidence)


def _candidate_map(root: Path, edges: list[dict]) -> dict:
    entries = li.read_ledger(root / li.LEDGER_REL)
    claims = [e for e in entries if e["kind"] == "claim"]
    yadav = next(e for e in claims if e["id"] == YADAV)
    matrix = json.loads(
        (root / "glossa-indus" / "matrix" / "matrix.json").read_text(
            encoding="utf-8"
        )
    )
    loads = {
        r["id"]: {"supports": 0, "opposes": 0, "constrains": 0}
        for r in matrix["rows"]
    }
    for cell in matrix["cells"]:
        loads[cell["row"]][cell["relation"]] += 1
    shares = lg._anchor_shares(root)
    return {
        "artifact": "glossa-indus map data (Stage 3 gate fixture)",
        "generated_from": "glossa-indus/matrix/matrix.json",
        "header": {
            "claims_by_status": dict(
                Counter(str(e.get("status")) for e in claims)
            ),
            "validated_anchor_share": shares["strict_share"],
            "strict_anchor_share": shares["strict_share"],
            "as_of": {
                "ledger_sha256": li.canonical_sha256_bytes(
                    (root / li.LEDGER_REL).read_bytes()
                )
            },
        },
        "elements": [
            {
                "id": yadav["id"],
                "kind": "claim",
                "statement": yadav["statement"],
                "status": yadav["status"],
                "stage": yadav["stage"],
                "population": yadav["population"],
            }
        ],
        "edges": edges,
        "loads": loads,
    }


def _write_candidate_map(root: Path, data: dict) -> Path:
    path = root / "candidate-map.json"
    path.write_bytes(json.dumps(data).encode("utf-8") + b"\n")
    return path


def test_teeth_v4_atlas_miscarriage_fails_v4_passing_v1_to_v3(scratch):
    """The named Atlas failure mode: Spec 054's 2026-10-24
    closure — outcome STRICT CORPUS NOT PINNABLE, the test
    did not execute (the task text's 'UNEXECUTED closure') —
    cited as support for the Yadav claim. The citation
    exists and is relevant; it carries no relation."""
    edge = {
        "from": "054",
        "to": YADAV,
        "rel": "supports",
        "citations": [YADAV, PTR_2024],
    }
    candidate = _write_candidate_map(scratch, _candidate_map(scratch, [edge]))
    report = lg.run_gate(
        scratch,
        scope={"V1", "V2", "V3", "V4", "V5", "V6"},
        candidate_map=candidate,
    )
    assert _check(report, "V1 ledger validity").status == "PASS"
    assert _check(report, "V1 recorded source hashes").status == "PASS"
    assert _check(report, "V2 count equivalence — claims by status").status == "PASS"
    assert _check(report, "V3 matrix recomputation — cells").status == "PASS"
    assert _check(report, "V5 map recomputation").status == "PASS"
    v4 = _check(report, "V4 relation-carrying")
    assert v4.status == "FAIL"
    text = "\n".join(v4.evidence)
    assert PTR_2024 in text
    assert "STRICT CORPUS NOT PINNABLE" in text
    assert "not carry the relation" in text


def test_v4_conforming_edges_pass(scratch):
    edges = [
        {
            "from": "054",
            "to": YADAV,
            "rel": "opposes",
            "citations": [YADAV, PTR_2025],
        },
        {
            "from": "yadav_2010_ngrams",
            "to": YADAV,
            "rel": "supports",
            "citations": [YADAV, "yadav_2010_ngrams_manual_002"],
        },
    ]
    candidate = _write_candidate_map(scratch, _candidate_map(scratch, edges))
    report = lg.run_gate(scratch, scope={"V4"}, candidate_map=candidate)
    v4 = _check(report, "V4 relation-carrying")
    assert v4.status == "PASS", report.render()


def test_teeth_v5_embedded_field_mismatch_fails(scratch):
    data = _candidate_map(scratch, [])
    data["elements"][0]["status"] = "not-the-ledger-status"
    candidate = _write_candidate_map(scratch, data)
    report = lg.run_gate(scratch, scope={"V5"}, candidate_map=candidate)
    assert not report.ok
    v5 = _check(report, "V5 map recomputation")
    assert v5.status == "FAIL"
    assert any(YADAV in ev for ev in v5.evidence)


def test_teeth_v6_flipped_strict_flag_fails(scratch):
    anchors_path = scratch / mg.ANCHORS_REL
    data = json.loads(anchors_path.read_text(encoding="utf-8"))
    sign = next(s for s, r in data["anchors"].items() if r.get("strict_set"))
    data["anchors"][sign]["strict_set"] = False
    anchors_path.write_bytes(json.dumps(data).encode("utf-8") + b"\n")
    report = lg.run_gate(scratch, scope={"V6"})
    assert not report.ok
    assert _check(report, "V6 anchor shares — strict set").status == "FAIL"


def test_teeth_v7_hand_edited_artifact_is_a_named_defect(scratch):
    md = scratch / "glossa-indus" / "matrix" / "matrix.md"
    md.write_bytes(md.read_bytes() + b"hand edit\n")
    report = lg.run_gate(scratch, scope={"V7"}, regen=True)
    assert not report.ok
    defect = _check(report, "V7 lossless regeneration — matrix.md")
    assert defect.status == "FAIL"
    assert any("downstream-defect" in ev for ev in defect.evidence)
    # The same diff, named as an intended change, classifies
    # as intended-change-named (C086-12).
    named = lg.run_gate(
        scratch, scope={"V7"}, regen=True, intended_change="teeth-fixture"
    )
    classified = _check(named, "V7 lossless regeneration — matrix.md")
    assert classified.status == "PASS"
    assert any("intended-change-named" in ev for ev in classified.evidence)
    assert _check(named, "V7 lossless regeneration — matrix.json").status == "PASS"


def test_teeth_v9_settling_module_importing_a_write_path_fails(scratch):
    module = scratch / "backend" / "glossa_lab" / "settling_fixture.py"
    module.write_text(
        "from glossa_lab.ledger_intake import append_entry\n",
        encoding="utf-8",
    )
    report = lg.run_gate(scratch, scope={"V9"})
    assert not report.ok
    audit = _check(report, "V9 no write path — settling/scenario")
    assert audit.status == "FAIL"
    assert any("settling_fixture" in ev for ev in audit.evidence)


def test_teeth_v9_unregistered_writer_fails(scratch):
    module = scratch / "backend" / "glossa_lab" / "rogue_writer.py"
    module.write_text(
        'TARGET = "glossa-indus/matrix/matrix.json"\n'
        "from pathlib import Path\n"
        "Path(TARGET).write_bytes(b'x')\n",
        encoding="utf-8",
    )
    report = lg.run_gate(scratch, scope={"V9"})
    assert not report.ok
    census = _check(report, "V9 no write path — matrix/map writer census")
    assert census.status == "FAIL"
    assert any("rogue_writer" in ev for ev in census.evidence)


# ---------------------------------------------------------------------------
# The numeric arm (adoption 3, item 2) — exercised on
# fixtures; the live population carries no such citation


def test_numeric_arm_refuses_a_violating_supports_citation():
    assert lg.numeric_arm_check("supports", 0.87, "<=", 0.8) is not None
    assert lg.numeric_arm_check("supports", 0.72, "<=", 0.8) is None
    assert lg.numeric_arm_check("opposes", 0.72, "<=", 0.8) is not None
    assert lg.numeric_arm_check("opposes", 0.87, "<=", 0.8) is None
    assert lg.numeric_arm_check("supports", 3.5, "in", [3.0, 4.0]) is None
    assert lg.numeric_arm_check("supports", 4.5, "in", [3.0, 4.0]) is not None


def test_numeric_arm_fires_through_the_v4_evaluator(scratch):
    ctx = lg._TieContext(scratch, li.read_ledger(scratch / li.LEDGER_REL))
    ctx.entries["fixture-measurement"] = {
        "id": "fixture-measurement",
        "kind": "measurement",
        "value": 0.87,
    }
    claim = {
        "id": "fixture-claim",
        "measurement": {"comparator": "<=", "bound": 0.8},
    }
    failures = lg._numeric_arm_failures(
        ctx, claim, "supports", ["fixture-measurement"]
    )
    assert failures and "violates the claim's bound" in failures[0]
    assert ctx.numeric_exercised == 1
    assert (
        lg._numeric_arm_failures(ctx, claim, "opposes", ["fixture-measurement"])
        == []
    )


# ---------------------------------------------------------------------------
# Write-freedom (parent-carried; Amendment 1 corollary 5):
# a RED gate run mutates nothing it checks


def test_red_gate_run_leaves_published_artifacts_byte_identical(scratch):
    before = _artifact_hashes(scratch)

    def mutate(entries):
        entry = next(e for e in entries if e["id"] == YADAV)
        entry["status"] = "flipped-for-teeth"

    _rewrite_ledger(scratch, mutate)
    # The ledger itself is the seeded input; the published
    # artifacts downstream of it must not move.
    report = lg.run_gate(scratch, scope={"V2", "V3", "V4"})
    assert not report.ok
    after = _artifact_hashes(scratch)
    assert after["glossa-indus/matrix/matrix.json"] == before[
        "glossa-indus/matrix/matrix.json"
    ]
    assert after["glossa-indus/matrix/matrix.md"] == before[
        "glossa-indus/matrix/matrix.md"
    ]


def test_cli_disables_bytecode_before_importing_the_backend():
    text = (ROOT / "tools" / "ledger" / "check_ledger_gate.py").read_text(
        encoding="utf-8"
    )
    assert text.index("sys.dont_write_bytecode = True") < text.index(
        "from glossa_lab.ledger_gate import"
    )


# ---------------------------------------------------------------------------
# T303 — gated publication: candidate -> gate -> replace
# only on ALL PASS; the negative control


def test_gated_publication_publishes_on_a_clean_tree(scratch):
    result = gp.publish_matrix(scratch)
    assert result["published"], result["gate"].render()
    matrix = scratch / "glossa-indus" / "matrix" / "matrix.json"
    assert (
        li.canonical_sha256_bytes(matrix.read_bytes())
        == result["written"]["matrix.json"]["sha256"]
    )
    assert not (scratch / "glossa-indus" / "matrix" / ".candidates").exists()


def test_gated_publication_negative_control(scratch, tmp_path):
    """T303's negative control, mechanically: the ledger
    status is flipped and the matrix a builder produced
    from the pre-flip ledger (the stale published bytes) is
    presented as the candidate. Publication must refuse,
    name the diverged checks, and leave the published
    artifact byte-identical to its pre-run hash."""
    before = _artifact_hashes(scratch)
    stale = tmp_path / "stale-candidate"
    stale.mkdir()
    for name in ("matrix.json", "matrix.md"):
        shutil.copyfile(
            scratch / "glossa-indus" / "matrix" / name, stale / name
        )

    def mutate(entries):
        entry = next(e for e in entries if e["id"] == YADAV)
        entry["status"] = "flipped-for-teeth"

    _rewrite_ledger(scratch, mutate)
    result = gp.publish_matrix(scratch, candidate_dir=stale)
    assert not result["published"]
    gate = result["gate"]
    assert not gate.ok
    failing_names = [c.name for c in gate.checks if c.status == "FAIL"]
    assert any(n.startswith("V2") for n in failing_names), gate.render()
    after = _artifact_hashes(scratch)
    assert after["glossa-indus/matrix/matrix.json"] == before[
        "glossa-indus/matrix/matrix.json"
    ]
    assert after["glossa-indus/matrix/matrix.md"] == before[
        "glossa-indus/matrix/matrix.md"
    ]
    assert not (scratch / "glossa-indus" / "matrix" / ".candidates").exists()


# ---------------------------------------------------------------------------
# T305 — PR-scope selection


def test_pr_scope_diff_fallback_is_full_not_silent():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_ledger_gate",
        ROOT / "tools" / "ledger" / "check_ledger_gate.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    classes, note = module.pr_scope(ROOT, "refs/does-not-exist")
    assert classes is None  # full run
    assert "falling back to a full gate run" in note
    assert module._layer_of("glossa-indus/ledger/claims.jsonl") == "ledger"
    assert module._layer_of("glossa-indus/matrix/matrix.json") == "matrix"
    assert module._layer_of("glossa-indus/map/map-data.json") == "map"
    assert (
        module._layer_of("backend/reports/INDUS_FINAL_ANCHORS.json")
        == "anchors"
    )
    assert module._layer_of("frontend/src/App.tsx") is None


# ---------------------------------------------------------------------------
# Stage 4 (T404) — V8 teeth: the settling canonicals under
# the gate's own route, and the separation arm's
# reachability extension.


def test_v8_passes_on_pristine_scratch(scratch):
    report = lg.run_gate(scratch, scope={"V8"})
    checks = [c for c in report.checks if c.name.startswith("V8")]
    assert len(checks) == 3
    for check in checks:
        assert check.status == "PASS", (check.name, check.evidence)


def test_teeth_v8_seeded_canonical_error_fails_naming_scenario_and_field(
    scratch,
):
    """Flip one registered expectation in the scratch copy
    of the canonical artifact (incumbent `consistent` 2→3):
    V8 must FAIL, naming the scenario and the field. The
    canonical in the real tree is untouched — the teeth
    bite the copy."""
    target = scratch / lg.SETTLING_CANONICAL_REL
    canonical = json.loads(target.read_text(encoding="utf-8"))
    scenario = next(
        s for s in canonical["scenarios"] if s["id"] == "incumbent-over-subset"
    )
    assert scenario["expected"]["consistent"] == 2
    scenario["expected"]["consistent"] = 3
    target.write_text(
        json.dumps(canonical, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    report = lg.run_gate(scratch, scope={"V8"})
    check = _check(report, "V8 settling canonicals — scenarios")
    assert check.status == "FAIL"
    named = "\n".join(check.evidence)
    assert "incumbent-over-subset" in named
    assert "consistent" in named


def test_teeth_v8_module_reaching_a_write_path_fails_where_v9_passes(
    scratch,
):
    """The separation arm's extension over V9.2: a settling
    module that imports only the intake *module* and reaches
    the write entry point as an attribute (`li.append_entry`)
    passes V9.2's import-only audit — and must FAIL V8,
    naming the module. Scenario/verdict separation is by
    reachability, not by import style."""
    module = scratch / "backend" / "glossa_lab" / "settling_fixture.py"
    module.write_text(
        "from glossa_lab import ledger_intake as li\n"
        "\n"
        "\n"
        "def smuggle(entry):\n"
        "    return li.append_entry(entry)\n",
        encoding="utf-8",
    )
    v9 = lg.run_gate(scratch, scope={"V9"})
    audit = _check(v9, "V9 no write path — settling/scenario import audit")
    assert audit.status == "PASS", audit.evidence
    report = lg.run_gate(scratch, scope={"V8"})
    check = _check(report, "V8 scenario/verdict separation")
    assert check.status == "FAIL"
    named = "\n".join(check.evidence)
    assert "settling_fixture.py" in named
    assert "append_entry" in named


def test_teeth_v8_module_importing_a_write_path_fails(scratch):
    """The import form, for completeness: a settling module
    importing a write entry point directly fails V8's
    separation arm, naming the module (V9.2's own teeth
    cover the same seed under V9's name; this pins V8's)."""
    module = scratch / "backend" / "glossa_lab" / "settling_fixture.py"
    module.write_text(
        "from glossa_lab.ledger_intake import write_ledger\n",
        encoding="utf-8",
    )
    report = lg.run_gate(scratch, scope={"V8"})
    check = _check(report, "V8 scenario/verdict separation")
    assert check.status == "FAIL"
    named = "\n".join(check.evidence)
    assert "settling_fixture.py" in named
    assert "write_ledger" in named


def test_gate_settle_copies_agree_with_the_engine_copies():
    """Same-motion discipline for the settle definitions:
    the gate's registered copies of glossa-settle-1 agree
    with the engine's (the DEFINITIONS.md §12 pattern,
    carried to the settling layer)."""
    from glossa_lab import settling as st

    assert lg.SETTLE_SEMANTICS_VERSION == st.SEMANTICS_VERSION
    assert lg.SETTLE_TALLY_KEYS == st.TALLY_KEYS
    assert lg.SETTLE_BEARING_OUTCOMES == st.BEARING_OUTCOMES
    assert lg.SETTLE_FRAME_PREFIXES == st.FRAME_PREFIXES
    assert lg.SETTLING_CANONICAL_REL == st.CANONICAL_REL
    assert lg.STRICT_RULE_ID == st.STRICT_RULE_ID


# ---------------------------------------------------------------------------
# Stage 5 (T502) — the map legs are live: agreement of the
# registered copies, the census on the clean tree, and teeth
# per map class (a seeded divergence per class, named).


PARPOLA = "parpola_2010_dravidian_solution_manual_002"
SUPERSEDED_PTR = (
    "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json:"
    "yadav_2009_arxiv_manual_002#spec054_outcome_append_2026_10_24"
)


@pytest.fixture()
def map_scratch(scratch: Path) -> Path:
    """The scratch tree plus the map chain's records of
    record (the published map, its definitions, the
    assignment sets, the stored runs, the filed comparison)
    as real copies a test can mutate."""
    root = scratch
    for rel in (
        "glossa-indus/map/DEFINITIONS.md",
        lg.MAP_REL,
        lg.ASSIGNMENT_SETS_REL,
        lg.COMPARISON_REL,
    ):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    runs_dst = root / lg.RUNS_REL_DIR
    runs_dst.mkdir(parents=True, exist_ok=True)
    # The whole store closure, not just its *.json records:
    # this fixture predates Spec 089 S2, which added
    # run-index.jsonl to the store, and the *.json glob was
    # never widened — so the scratch tree carried the run
    # records without the index that enters them. No gate
    # leg read the index in a scratch tree until V11
    # (Spec 089 S5), whose legs (a) and (c) failed on
    # exactly that omission (PR #521, CI run 41957645343).
    # The gate is right — a store whose records stand
    # without their covering index is non-conforming — so
    # the copy is repaired, not the legs.
    for f in sorted((ROOT / lg.RUNS_REL_DIR).iterdir()):
        if f.is_file():
            shutil.copyfile(f, runs_dst / f.name)
    # The junction store likewise, when the real tree has
    # one (it comes into existence with the first filed
    # report): leg (d) reads it from the tree root, and a
    # records-only copy would lose it the same way.
    junctions_src = ROOT / lg.RUN_JUNCTIONS_REL
    if junctions_src.is_dir():
        junctions_dst = root / lg.RUN_JUNCTIONS_REL
        junctions_dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(junctions_src.iterdir()):
            if f.is_file():
                shutil.copyfile(f, junctions_dst / f.name)
    return root


def _checks(report: lg.GateReport, prefix: str) -> list[lg.Check]:
    return [c for c in report.checks if c.name.startswith(prefix)]


def _rewrite_map(root: Path, mutate) -> None:
    path = root / lg.MAP_REL
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_bytes(
        json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")
        + b"\n"
    )


def test_map_definitions_copies_agree_with_the_builder_copies():
    """Same-motion discipline for map-defs v1: the gate's
    registered copies agree with the builder's, field for
    field (the DEFINITIONS.md §11 pattern)."""
    from glossa_lab import map_generate as mp

    assert lg.GATE_MAP_DEFS_VERSION == mp.MAP_DEFS_VERSION
    assert lg.PENDING_VALIDATIONS_REASON == mp.PENDING_VALIDATIONS_REASON
    assert lg.SETTLING_LABEL == mp.SETTLING_LABEL
    assert lg.MAP_S_R3_NOTE == mp.S_R3_NOTE
    assert lg.MAP_RUN_RESULT_FIELDS == mp.RUN_RESULT_FIELDS
    assert lg.ASSIGNMENT_SETS_REL == mp.ASSIGNMENT_SETS_REL
    assert lg.RUNS_REL_DIR == mp.RUNS_REL_DIR
    assert lg.COMPARISON_REL == mp.COMPARISON_REL
    assert lg.PENDING_VALIDATION_STATUS == "pending_non_sa_validation"


def test_map_legs_live_and_pass_on_a_clean_map_tree(map_scratch):
    report = lg.run_gate(map_scratch)
    assert report.ok, report.render()
    v2 = _check(report, "V2 count equivalence — claims by status: ledger == map header")
    assert v2.status == "PASS"
    assert "913 claims counted across 8 statuses" in "\n".join(v2.evidence)
    v5_full = _checks(report, "V5 map recomputation")[1]
    assert v5_full.name.endswith("(map-defs v1 copies)")
    assert v5_full.status == "PASS"
    census = "\n".join(v5_full.evidence)
    assert "1436 map edges by relation" in census
    assert "UNPROVEN on the live population: corpus_texts" in census
    assert "UNPROVEN on the live population: constrains" in census
    v6 = _check(report, "V6 anchor shares — map header leg")
    assert v6.status == "PASS"
    assert "287 register records, 94 of them strict" in "\n".join(v6.evidence)
    v4 = _check(report, "V4 relation-carrying citations")
    assert "map edge census: supports 1429, opposes 7, constrains 0" in (
        "\n".join(v4.evidence)
    )


def test_v9_census_names_the_map_writer_on_the_real_tree():
    report = lg.run_gate(ROOT, scope={"V9"})
    v9 = _check(report, "V9 no write path — matrix/map writer census")
    assert v9.status == "PASS"
    assert "map_generate.py" in "\n".join(v9.evidence)


def test_teeth_v2_map_header_count_flip_fails(map_scratch):
    def mutate(data):
        data["header"]["claims_by_status"]["draft"] -= 1

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, scope={"V2"})
    check = _check(
        report, "V2 count equivalence — claims by status: ledger == map header"
    )
    assert check.status == "FAIL"


def test_teeth_v5_map_claims_section_divergence_is_named(map_scratch):
    def mutate(data):
        data["claims"][PARPOLA]["does_not_establish"] = "tampered"

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, scope={"V5"})
    check = _checks(report, "V5 map recomputation")[1]
    assert check.status == "FAIL"
    named = "\n".join(check.evidence)
    assert PARPOLA in named
    assert "does_not_establish" in named


def test_teeth_v5_map_settling_section_divergence_is_named(map_scratch):
    def mutate(data):
        data["settling"]["runs"][0]["assigned_count"] = 95

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, scope={"V5"})
    check = _checks(report, "V5 map recomputation")[1]
    assert check.status == "FAIL"
    assert "assigned_count" in "\n".join(check.evidence)


def test_teeth_v5_partial_candidate_map_fails_naming_the_section(
    map_scratch, tmp_path
):
    data = json.loads((ROOT / lg.MAP_REL).read_text(encoding="utf-8"))
    del data["settling"]
    candidate = tmp_path / "candidate-map.json"
    candidate.write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    report = lg.run_gate(map_scratch, candidate_map=candidate)
    check = _checks(report, "V5 map recomputation")[1]
    assert check.status == "FAIL"
    assert "settling" in "\n".join(check.evidence)


def test_teeth_v6_map_header_share_flip_fails(map_scratch):
    def mutate(data):
        data["header"]["validated_anchor_share"] = 0.5

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, scope={"V6"})
    check = _check(report, "V6 anchor shares — map header leg")
    assert check.status == "FAIL"


def test_teeth_v4_map_edge_citation_must_carry_its_relation(map_scratch):
    def mutate(data):
        edge = next(
            e
            for e in data["edges"]
            if e["to"] == YADAV and e["column_class"] == "studies"
        )
        edge["citations"] = [YADAV, SUPERSEDED_PTR]

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, scope={"V4"})
    check = _check(report, "V4 relation-carrying citations")
    assert check.status == "FAIL"
    assert SUPERSEDED_PTR in "\n".join(check.evidence)


def test_teeth_v7_map_hand_edit_is_a_downstream_defect(map_scratch):
    def mutate(data):
        data["claims"][PARPOLA]["status"] = "strongly_supported"

    _rewrite_map(map_scratch, mutate)
    report = lg.run_gate(map_scratch, regen=True, scope={"V7"})
    check = _check(report, "V7 lossless regeneration — map data")
    assert check.status == "FAIL"
    assert "downstream-defect" in "\n".join(check.evidence)
    named = lg.run_gate(
        map_scratch,
        regen=True,
        scope={"V7"},
        intended_change="test-named map change",
    )
    check = _check(named, "V7 lossless regeneration — map data")
    assert check.status == "PASS"
    assert "intended-change-named" in "\n".join(check.evidence)


def test_gated_publication_of_the_map_and_its_negative_control(
    map_scratch, tmp_path
):
    before = (map_scratch / lg.MAP_REL).read_bytes()
    result = gp.publish_map(map_scratch)
    assert result["published"] is True
    assert (map_scratch / lg.MAP_REL).read_bytes() == before

    # Negative control: a candidate whose header count is
    # flipped is refused by the gate, and the previously
    # published artifact stays byte-untouched (Amendment 1).
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    data = json.loads(before.decode("utf-8"))
    data["header"]["claims_by_status"]["draft"] -= 1
    (candidate_dir / "map-data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    refused = gp.publish_map(map_scratch, candidate_dir=candidate_dir)
    assert refused["published"] is False
    assert refused["gate"].ok is False
    assert (map_scratch / lg.MAP_REL).read_bytes() == before


# ---------------------------------------------------------------------------
# Spec 088 Stage 3 (T301–T303) — V10 program-map equivalence:
# agreement of the registered copies, the legs live on a
# program-map tree, the NOT-RUN posture where the layer has
# not landed, and teeth per seeded divergence — each fails
# by name and leaves the seeded tree byte-untouched.
# Stage 4 (T401/T403) adds: the page in the agreement test
# and the legs (five legs), page teeth (chrome edit, payload
# edit, missing page), and the gated-publication pair for
# publish_program_map.


@pytest.fixture()
def pm_scratch(scratch: Path) -> Path:
    """The scratch tree plus the program-map layer's records
    of record (the taxonomy and the published artifacts —
    both data artifacts and, since Stage 4, the page) as
    real copies a test can mutate, and the spec-directory
    names the derivation reads (names only — empty dirs;
    the derivation reads no spec content)."""
    root = scratch
    for rel in (
        lg.PROGRAM_MAP_TAXONOMY_REL,
        lg.PROGRAM_MAP_REL,
        lg.PROGRAM_MAP_FINDS_REL,
        lg.PROGRAM_MAP_HTML_REL,
    ):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    specs = root / "specs"
    specs.mkdir(exist_ok=True)
    for d in sorted((ROOT / "specs").iterdir()):
        if d.is_dir():
            (specs / d.name).mkdir(exist_ok=True)
    return root


def _rewrite_program_map(root: Path, mutate) -> None:
    path = root / lg.PROGRAM_MAP_REL
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_bytes(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )


def _pm_hashes(root: Path) -> dict[str, str]:
    import hashlib

    return {
        rel: hashlib.sha256((root / rel).read_bytes()).hexdigest()
        for rel in (
            lg.PROGRAM_MAP_REL,
            lg.PROGRAM_MAP_FINDS_REL,
            lg.PROGRAM_MAP_HTML_REL,
            lg.PROGRAM_MAP_TAXONOMY_REL,
            li.LEDGER_REL,
        )
    }


def test_program_map_definitions_copies_agree_with_the_builder_copies():
    """Same-motion discipline for program-map-defs v1: the
    gate's registered copies agree with the builder's, field
    for field (PROGRAM-MAP-DEFINITIONS.md §12)."""
    from glossa_lab import program_map_generate as pm

    assert lg.GATE_PROGRAM_MAP_DEFS_VERSION == pm.DEFS_VERSION
    assert lg.PROGRAM_MAP_TAXONOMY_VERSION == pm.TAXONOMY_VERSION
    assert lg.PROGRAM_MAP_REL == pm.MAP_REL
    assert lg.PROGRAM_MAP_FINDS_REL == pm.FINDS_REL
    assert lg.PROGRAM_MAP_TAXONOMY_REL == pm.TAXONOMY_REL
    assert lg.PROGRAM_MAP_SPECS_REL == pm.SPECS_REL
    assert lg.PM_STATUS_TO_CLASS == pm.STATUS_TO_CLASS
    assert lg.PM_CLAIM_CLASSES == pm.CLAIM_CLASSES
    assert lg.PM_STUDY_CLASSES == pm.STUDY_CLASSES
    assert lg.PM_IN_FLIGHT == pm.IN_FLIGHT
    assert lg.PM_STANDING_TEMPLATE == pm._STANDING_TEMPLATE
    assert lg.PM_RESTRICTED_NAME_ONLY == pm.RESTRICTED_NAME_ONLY
    assert lg.PM_FORBIDDEN_TAXONOMY_KEYS == pm.FORBIDDEN_TAXONOMY_KEYS
    assert set(lg.PM_FIND_KINDS) == {
        pm.FIND_BUNDLE_LESS_STUDY,
        pm.FIND_JUDGMENT_CALL,
        pm.FIND_EXTRACTED_NULL_FALSIFIER,
        pm.FIND_RESTRICTED_NODE,
    }
    # Stage 4: the page joins the registered copies — its
    # artifact path and the three template pieces agree with
    # the builder's, byte for byte.
    assert lg.PROGRAM_MAP_HTML_REL == pm.PAGE_REL
    assert lg.PM_PAGE_HEAD == pm._PAGE_HEAD
    assert lg.PM_PAGE_MID == pm._PAGE_MID
    assert lg.PM_PAGE_TAIL == pm._PAGE_TAIL


def test_v10_legs_live_and_pass_on_a_program_map_tree(pm_scratch):
    report = lg.run_gate(pm_scratch, scope={"V10"})
    assert report.ok, report.render()
    checks = _checks(report, "V10 program-map equivalence")
    assert len(checks) == 5
    assert all(c.status == "PASS" for c in checks)
    census = "\n".join(checks[1].evidence)
    assert "913 claim nodes" in census
    assert "91 study nodes" in census
    finds_evidence = "\n".join(checks[2].evidence)
    assert "bundle_less_study 28" in finds_evidence
    assert "restricted_node 1" in finds_evidence
    # Stage 4's fifth leg: the page, byte-equal to the
    # gate's recomputation under its template copies.
    page_check = _check(report, "V10 program-map equivalence — program-map.html")
    assert page_check.status == "PASS"
    assert "verbatim" in "\n".join(page_check.evidence)


def test_v10_not_run_where_the_layer_has_not_landed(scratch):
    """The V5 posture toward a layer that did not exist yet:
    a tree with no taxonomy and no published program-map
    artifacts enumerates one NOT-RUN and the gate stays
    green (the pre-088 scratch battery depends on it)."""
    report = lg.run_gate(scratch, scope={"V10"})
    assert report.ok, report.render()
    checks = _checks(report, "V10 program-map equivalence")
    assert len(checks) == 1
    assert checks[0].status == "NOT-RUN"


def test_teeth_v10_hand_edited_program_map_fails(pm_scratch):
    before = _pm_hashes(pm_scratch)

    def mutate(data):
        data["nodes"]["claims"][0]["standing"] = "tampered"

    _rewrite_program_map(pm_scratch, mutate)
    seeded = _pm_hashes(pm_scratch)
    assert seeded != before  # the seed itself landed
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _checks(
        report, "V10 program-map equivalence — program-map.json"
    )[0]
    assert check.status == "FAIL"
    assert "standing" in "\n".join(check.evidence)
    assert _pm_hashes(pm_scratch) == seeded  # the gate wrote nothing


def test_teeth_v10_dropped_claim_node_fails(pm_scratch):
    def mutate(data):
        data["nodes"]["claims"] = data["nodes"]["claims"][1:]

    _rewrite_program_map(pm_scratch, mutate)
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _checks(
        report, "V10 program-map equivalence — program-map.json"
    )[0]
    assert check.status == "FAIL"
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_dropped_find_fails(pm_scratch):
    path = pm_scratch / lg.PROGRAM_MAP_FINDS_REL
    data = json.loads(path.read_text(encoding="utf-8"))
    data["finds"] = data["finds"][1:]
    path.write_bytes(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — program-map-finds.json"
    )
    assert check.status == "FAIL"
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_defs_copy_drift_fails(pm_scratch, monkeypatch):
    """A one-copy definitions change (the builder's table
    drifts from the gate's registered copies): artifacts
    built under the drifted table fail V10 — never silent
    agreement."""
    from glossa_lab import program_map_generate as pm

    monkeypatch.setitem(pm.STATUS_TO_CLASS, "draft", "closed_other")
    for rel, text in pm.build_artifacts(pm_scratch).items():
        (pm_scratch / rel).write_text(text, encoding="utf-8")
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _checks(
        report, "V10 program-map equivalence — program-map.json"
    )[0]
    assert check.status == "FAIL"
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_stale_stamp_fails(pm_scratch):
    def mutate(data):
        data["stamp"]["ledger_lines"] += 1

    _rewrite_program_map(pm_scratch, mutate)
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — stamp freshness"
    )
    assert check.status == "FAIL"
    assert "ledger_lines" in "\n".join(check.evidence)
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_dropped_taxonomy_assignment_fails(pm_scratch):
    tax_path = pm_scratch / lg.PROGRAM_MAP_TAXONOMY_REL
    tax = json.loads(tax_path.read_text(encoding="utf-8"))
    dropped = tax["studies"][0]["spec_dir"]
    tax["studies"] = tax["studies"][1:]
    tax_path.write_bytes(
        json.dumps(tax, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — taxonomy coverage"
    )
    assert check.status == "FAIL"
    assert dropped in "\n".join(check.evidence)
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_hand_edited_page_fails(pm_scratch):
    """Stage 4 (T401): a hand-touched page — one word of
    chrome changed, data untouched — fails the page leg by
    name, and the gate writes nothing."""
    path = pm_scratch / lg.PROGRAM_MAP_HTML_REL
    page = path.read_text(encoding="utf-8")
    path.write_text(
        page.replace("<title>Program map", "<title>Program map, edited"),
        encoding="utf-8",
    )
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — program-map.html"
    )
    assert check.status == "FAIL"
    assert "chrome" in "\n".join(check.evidence)
    assert _pm_hashes(pm_scratch) == seeded  # the gate wrote nothing


def test_teeth_v10_page_with_tampered_embedded_data_fails(pm_scratch):
    """A page whose embedded payload was edited (the data
    artifacts on disk left clean) fails the page leg naming
    the payload, not the chrome."""
    path = pm_scratch / lg.PROGRAM_MAP_HTML_REL
    page = path.read_text(encoding="utf-8")
    marker = 'id="program-map-data">\n'
    head, rest = page.split(marker, 1)
    payload, tail = rest.split("</script>", 1)
    tampered = payload.replace(
        '"status": "draft"', '"status": "untested"', 1
    )
    assert tampered != payload
    path.write_text(
        head + marker + tampered + "</script>" + tail, encoding="utf-8"
    )
    seeded = _pm_hashes(pm_scratch)
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — program-map.html"
    )
    assert check.status == "FAIL"
    assert "embedded program-map payload" in "\n".join(check.evidence)
    assert _pm_hashes(pm_scratch) == seeded


def test_teeth_v10_missing_page_fails_by_name(pm_scratch):
    (pm_scratch / lg.PROGRAM_MAP_HTML_REL).unlink()
    report = lg.run_gate(pm_scratch, scope={"V10"})
    check = _check(
        report, "V10 program-map equivalence — program-map.html"
    )
    assert check.status == "FAIL"
    assert "missing" in "\n".join(check.evidence)


def test_publish_program_map_through_the_gate(pm_scratch):
    """T403's mechanics: candidates built by the pure
    builder are gated by V10 (against the candidates, not
    the published bytes) and land byte-identical."""
    from glossa_lab import program_map_generate as pm

    expected = pm.build_artifacts(pm_scratch)
    result = gp.publish_program_map(pm_scratch)
    assert result["published"] is True, result["gate"].render()
    assert result["gate"].ok
    for rel, text in expected.items():
        assert (pm_scratch / rel).read_bytes() == text.encode("utf-8")


def test_publish_program_map_refuses_a_tampered_candidate(
    pm_scratch, tmp_path
):
    """A candidate set whose page was hand-edited is refused:
    nothing is published and the published artifacts keep
    their prior bytes."""
    from glossa_lab import program_map_generate as pm

    before = _pm_hashes(pm_scratch)
    candidate_dir = tmp_path / "candidates"
    candidate_dir.mkdir()
    for rel, text in pm.build_artifacts(pm_scratch).items():
        (candidate_dir / Path(rel).name).write_text(
            text, encoding="utf-8"
        )
    page_path = candidate_dir / "program-map.html"
    page_path.write_bytes(page_path.read_bytes() + b"<!-- hand edit -->")
    result = gp.publish_program_map(
        pm_scratch, candidate_dir=candidate_dir
    )
    assert result["published"] is False
    assert result["gate"].ok is False
    assert _pm_hashes(pm_scratch) == before


def test_teeth_v9_census_catches_an_unregistered_program_map_writer(
    scratch,
):
    """T303's negative case: the program-map artifacts ride
    the existing gated-artifact census (the glossa-indus/map
    pattern), so a writer that is not the registered builder
    fails V9 by name."""
    rogue = scratch / "backend" / "glossa_lab" / "rogue_pm_writer.py"
    rogue.write_text(
        '"""Seeded: an unregistered writer of the program map."""\n'
        "from pathlib import Path\n\n"
        "TARGET = Path('glossa-indus/map/program-map.json')\n\n\n"
        "def go():\n"
        "    TARGET.write_text('{}')\n",
        encoding="utf-8",
    )
    report = lg.run_gate(scratch, scope={"V9"})
    assert not report.ok
    census = _check(report, "V9 no write path — matrix/map writer census")
    assert census.status == "FAIL"
    assert "rogue_pm_writer.py" in "\n".join(census.evidence)


# ---------------------------------------------------------------------------
# Spec 089 Stage 5 — V11 (run-binding) teeth (T502, T503)
#
# The fixture is a self-contained run layer on a tmp root:
# a settling store holding two comparable scenario runs
# and one materialization run, the assignment-sets
# artifact bound to the materialization run, and a spec
# records directory (the citation store) whose stage
# record cites the first run. Seeded means seeded: each
# case mutates its own copy of the fixture, never the
# tree, and each failure must name its V11 leg while the
# other legs stay green.

import hashlib  # noqa: E402

from glossa_lab import run_records as rr  # noqa: E402

_V11_RUN_A = "settling-20261105T000000Z-aaaaaa"
_V11_RUN_B = "settling-20261105T010000Z-bbbbbb"
_V11_MAT = "settling-20261105T020000Z-cccccc"
_V11_JUNCTION = "junction-20261105T030000Z-dddd44"


def _v11_key(command: str) -> dict:
    return {
        "surface": "settling",
        "command": command,
        "tool_version": "1",
        "input_pins": {"ledger": "fixture-pin"},
        "seed": "no-seed",
        "code_version": "fixture-sha",
        "environment_class": "vm/linux",
    }


def _v11_record(run_id: str, command: str, result: dict) -> dict:
    return {
        "run": {
            "run_id": run_id,
            "surface": "settling",
            "tool": "fixture tool",
            "tool_version": "1",
            "started": "2026-11-05T00:00:00Z",
            "finished": "2026-11-05T00:00:01Z",
            "key": _v11_key(command),
            "determinism_class": "deterministic",
        },
        "result": result,
    }


def _v11_write(path: Path, payload: dict) -> bytes:
    data = (
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def _v11_tree(tmp_path: Path, *, divergent: bool = False) -> Path:
    """The conforming fixture. With `divergent`, the two
    scenario runs' result blocks differ (a comparable
    divergent pair with no junction report yet)."""
    root = tmp_path / "v11-tree"
    store = root / "glossa-indus" / "ledger" / "runs"
    store.mkdir(parents=True)
    result_a = {"verdict": "same", "assignments": [1, 2]}
    result_b = (
        {"verdict": "DIFFERENT", "assignments": [1, 2]}
        if divergent
        else {"verdict": "same", "assignments": [1, 2]}
    )
    _v11_write(store / f"{_V11_RUN_A}.json", _v11_record(_V11_RUN_A, "run t405", result_a))
    _v11_write(store / f"{_V11_RUN_B}.json", _v11_record(_V11_RUN_B, "run t405", result_b))
    artifact = {
        "artifact": "glossa-settle-1 assignment sets of record",
        "producing_run": {
            "run_id": _V11_MAT,
            "surface": "settling",
            "command": "materialize-sets",
        },
        "sets": [],
    }
    artifact_bytes = _v11_write(
        root / "glossa-indus" / "ledger" / "assignment-sets.json",
        artifact,
    )
    mat_record = _v11_record(
        _V11_MAT,
        "materialize-sets",
        {
            "materialized": "glossa-indus/ledger/assignment-sets.json",
            "artifact_sha256": hashlib.sha256(artifact_bytes).hexdigest(),
            "producing_run": _V11_MAT,
        },
    )
    _v11_write(store / f"{_V11_MAT}.json", mat_record)
    acts = [
        {
            "act": "entry",
            "run_id": run_id,
            "record": f"{run_id}.json",
            "key": _v11_key(command),
        }
        for run_id, command in (
            (_V11_RUN_A, "run t405"),
            (_V11_RUN_B, "run t405"),
            (_V11_MAT, "materialize-sets"),
        )
    ]
    (store / "run-index.jsonl").write_text(
        "".join(
            json.dumps(act, sort_keys=True) + "\n" for act in acts
        ),
        encoding="utf-8",
    )
    _v11_write(
        root / "glossa-indus" / "ledger" / "settling-canonical.json",
        {"artifact": "settling canonicals", "re_derivations": []},
    )
    records = root / "specs" / "900-fixture" / "records"
    records.mkdir(parents=True)
    (records / "stage-record.md").write_text(
        f"# Fixture stage record\n\nSuite evidence: run {_V11_RUN_A}.\n",
        encoding="utf-8",
    )
    return root


def _v11_legs(report: lg.GateReport) -> dict[str, lg.Check]:
    return {
        c.name.split("—")[1].strip().split(" (")[0]: c
        for c in report.checks
        if c.name.startswith("V11 run-binding —")
    }


def _v11_assert_only_leg_fails(report: lg.GateReport, leg: str) -> None:
    legs = _v11_legs(report)
    assert set(legs) == {
        "producing bindings resolve",
        "no quarantined citation as verdict support",
        "store census and index integrity",
        "junction completeness",
    }
    for name, check in legs.items():
        if name == leg:
            assert check.status == "FAIL", f"{leg} should fail"
        else:
            assert check.status == "PASS", (
                f"{name} should stay green: {check.evidence}"
            )
    assert not report.ok


def test_v11_passes_a_conforming_run_layer(tmp_path):
    root = _v11_tree(tmp_path)
    report = lg.run_gate(root, scope={"V11"})
    assert report.ok, report.render()
    legs = _v11_legs(report)
    assert all(c.status == "PASS" for c in legs.values())


def test_v11_run_defs_copies_agree_with_the_library_copies():
    """The same-motion discipline, pinned: the gate's
    registered run-defs copies equal the tooling's."""
    assert lg.GATE_RUN_DEFS_VERSION == rr.RUN_DEFS_VERSION
    assert lg.RUN_DISPOSITIONS == rr.DISPOSITIONS
    assert lg.RUN_CONSTITUTIVE_COMPONENTS == rr.CONSTITUTIVE_COMPONENTS
    assert lg.RUN_KEY_COMPONENTS == rr.KEY_COMPONENTS
    assert lg.RUN_ABSENCE_KINDS == rr.ABSENCE_KINDS
    assert lg.RUN_ADJUDICATION_STATES == rr.ADJUDICATION_STATES
    assert lg.RUN_LEGACY_LABEL == rr.LEGACY_LABEL
    assert set(lg.RUN_SURFACES) == set(rr.SURFACES)
    assert tuple(lg.RUN_ACT_KINDS) == tuple(rr.ACT_KINDS)


def test_teeth_v11a_unbound_artifact_fails(tmp_path):
    root = _v11_tree(tmp_path)
    artifact_path = root / "glossa-indus" / "ledger" / "assignment-sets.json"
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    del artifact["producing_run"]
    artifact_path.write_text(
        json.dumps(artifact, indent=1) + "\n", encoding="utf-8"
    )
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "producing bindings resolve")
    leg = _v11_legs(report)["producing bindings resolve"]
    assert "no producing-run binding" in "\n".join(leg.evidence)


def test_teeth_v11a_binding_naming_an_unknown_run_fails(tmp_path):
    root = _v11_tree(tmp_path)
    artifact_path = root / "glossa-indus" / "ledger" / "assignment-sets.json"
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    artifact["producing_run"]["run_id"] = "settling-20261105T090000Z-ffffff"
    artifact_path.write_text(
        json.dumps(artifact, indent=1) + "\n", encoding="utf-8"
    )
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "producing bindings resolve")
    leg = _v11_legs(report)["producing bindings resolve"]
    assert "does not resolve" in "\n".join(leg.evidence)


def test_teeth_v11b_quarantined_citation_fails(tmp_path):
    root = _v11_tree(tmp_path)
    index_path = root / "glossa-indus" / "ledger" / "runs" / "run-index.jsonl"
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "act": "quarantine",
                    "junction_id": _V11_JUNCTION,
                    "run_ids": [_V11_RUN_A, _V11_RUN_B],
                },
                sort_keys=True,
            )
            + "\n"
        )
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(
        report, "no quarantined citation as verdict support"
    )
    leg = _v11_legs(report)["no quarantined citation as verdict support"]
    assert _V11_RUN_A in "\n".join(leg.evidence)


def test_teeth_v11c_dropped_record_fails_census(tmp_path):
    root = _v11_tree(tmp_path)
    (root / "glossa-indus" / "ledger" / "runs" / f"{_V11_RUN_B}.json").unlink()
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "store census and index integrity")
    leg = _v11_legs(report)["store census and index integrity"]
    assert "neither stands in the store" in "\n".join(leg.evidence)


_V11_LEGACY_NAME = "t405-incumbent-over-full-frame--aaaaaaaaaaaa.json"
_V11_LEGACY_ID = "legacy:t405-incumbent-over-full-frame--aaaaaaaaaaaa"


def _v11_tree_with_legacy_generation(tmp_path) -> Path:
    """The conforming fixture plus one legacy generation
    entered standing (its entry carries no accounting
    fields — the run-defs v1 shape that stranded the
    2026-11-05 intakes)."""
    root = _v11_tree(tmp_path)
    store = root / "glossa-indus" / "ledger" / "runs"
    _v11_write(
        store / _V11_LEGACY_NAME,
        {
            "artifact": "settling run record",
            "semantics": "glossa-settle-1",
            "candidate": "incumbent",
            "scenario": "t405-incumbent-over-full-frame",
            "pins": {"ledger": {"sha256": "a" * 64}},
            "result": {"assignments": []},
        },
    )
    index_path = store / "run-index.jsonl"
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "act": "entry",
                    "run_id": _V11_LEGACY_ID,
                    "record": _V11_LEGACY_NAME,
                    "key": {
                        "surface": "settling",
                        "semantics": "glossa-settle-1",
                        "candidate": "incumbent",
                        "input_pins": {"ledger": {"sha256": "a" * 64}},
                    },
                    "legacy": True,
                    "key_partial": True,
                    "label": lg.RUN_LEGACY_LABEL,
                    "missing": ["command", "tool_version"],
                },
                sort_keys=True,
            )
            + "\n"
        )
    return root


def _v11_append_departure(root: Path, **overrides) -> None:
    store = root / "glossa-indus" / "ledger" / "runs"
    act = {
        "act": "departure",
        "run_id": _V11_LEGACY_ID,
        "record": _V11_LEGACY_NAME,
        "superseded_by_commit": "c" * 40,
        "git_blob": "d" * 40,
        "blob_sha256": "e" * 64,
        "ref": "teeth fixture",
    }
    act.update(overrides)
    with (store / "run-index.jsonl").open(
        "a", encoding="utf-8"
    ) as handle:
        handle.write(json.dumps(act, sort_keys=True) + "\n")


def test_teeth_v11c_dropped_legacy_generation_unaccounted_fails(tmp_path):
    """A legacy generation that entered standing and then
    departed, with no accounting anywhere, is exactly the
    seeded unaccounted run: leg (c) still fails."""
    root = _v11_tree_with_legacy_generation(tmp_path)
    (root / "glossa-indus" / "ledger" / "runs" / _V11_LEGACY_NAME).unlink()
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "store census and index integrity")
    leg = _v11_legs(report)["store census and index integrity"]
    assert "neither stands in the store" in "\n".join(leg.evidence)


def test_v11c_departure_act_accounts_a_dropped_legacy_generation(tmp_path):
    """The run-defs v2 accounting: the same dropped
    generation, with a folded departure act carrying the
    superseding commit, the git blob, and the blob hash,
    passes every leg — the entry itself unedited."""
    root = _v11_tree_with_legacy_generation(tmp_path)
    (root / "glossa-indus" / "ledger" / "runs" / _V11_LEGACY_NAME).unlink()
    _v11_append_departure(root)
    report = lg.run_gate(root, scope={"V11"})
    assert report.ok, report.render()
    leg = _v11_legs(report)["store census and index integrity"]
    assert "accounted by departure act" in "\n".join(leg.evidence)


def test_teeth_v11c_departure_naming_an_unknown_run_fails(tmp_path):
    root = _v11_tree_with_legacy_generation(tmp_path)
    _v11_append_departure(
        root, run_id="legacy:t405-incumbent-over-full-frame--zzzzzzzzzzzz"
    )
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "store census and index integrity")
    leg = _v11_legs(report)["store census and index integrity"]
    assert "unknown run id" in "\n".join(leg.evidence)


def test_teeth_v11c_dangling_supersedes_link_fails(tmp_path):
    root = _v11_tree(tmp_path)
    index_path = root / "glossa-indus" / "ledger" / "runs" / "run-index.jsonl"
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "act": "supersedes",
                    "run_id": _V11_RUN_A,
                    "supersedes": "settling-20261105T090000Z-ffffff",
                    "ref": "teeth fixture",
                },
                sort_keys=True,
            )
            + "\n"
        )
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "store census and index integrity")
    leg = _v11_legs(report)["store census and index integrity"]
    assert "unknown run id" in "\n".join(leg.evidence)


def _v11_junction_report(
    root: Path, disposition: str, *, quarantine: bool = False
) -> None:
    junctions = root / "glossa-indus" / "ledger" / "junctions"
    _v11_write(
        junctions / f"{_V11_JUNCTION}.json",
        {
            "junction_id": _V11_JUNCTION,
            "kind": "junction report",
            "runs": [
                {"run_id": _V11_RUN_A},
                {"run_id": _V11_RUN_B},
            ],
            "disposition": disposition,
        },
    )
    if quarantine:
        index_path = (
            root / "glossa-indus" / "ledger" / "runs" / "run-index.jsonl"
        )
        with index_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "act": "quarantine",
                        "junction_id": _V11_JUNCTION,
                        "run_ids": [_V11_RUN_A, _V11_RUN_B],
                    },
                    sort_keys=True,
                )
                + "\n"
            )


def test_teeth_v11d_divergent_pair_without_a_report_fails(tmp_path):
    root = _v11_tree(tmp_path, divergent=True)
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "junction completeness")
    leg = _v11_legs(report)["junction completeness"]
    assert "no junction report" in "\n".join(leg.evidence)


def test_teeth_v11d_out_of_vocabulary_disposition_fails(tmp_path):
    root = _v11_tree(tmp_path, divergent=True)
    _v11_junction_report(root, "benign-variation")
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "junction completeness")
    leg = _v11_legs(report)["junction completeness"]
    assert "outside the registered vocabulary" in "\n".join(leg.evidence)


def test_teeth_v11d_unexplained_without_quarantine_fails(tmp_path):
    root = _v11_tree(tmp_path, divergent=True)
    _v11_junction_report(root, "unexplained")
    report = lg.run_gate(root, scope={"V11"})
    _v11_assert_only_leg_fails(report, "junction completeness")
    leg = _v11_legs(report)["junction completeness"]
    assert "not quarantined" in "\n".join(leg.evidence)


def test_v11d_explained_report_satisfies_a_divergent_pair(tmp_path):
    root = _v11_tree(tmp_path, divergent=True)
    _v11_junction_report(root, "explained-by-named-difference")
    report = lg.run_gate(root, scope={"V11"})
    assert report.ok, report.render()


def test_v11d_unexplained_with_quarantine_passes_d_but_fails_b(tmp_path):
    """The two legs look at the same junction from their
    own sides: with the quarantine act appended, leg (d)
    is satisfied — and the fixture's stage record, which
    cites run A, now fails leg (b) for exactly that
    reason. Both readings are the design working."""
    root = _v11_tree(tmp_path, divergent=True)
    _v11_junction_report(root, "unexplained", quarantine=True)
    report = lg.run_gate(root, scope={"V11"})
    legs = _v11_legs(report)
    assert legs["junction completeness"].status == "PASS"
    assert (
        legs["no quarantined citation as verdict support"].status
        == "FAIL"
    )
