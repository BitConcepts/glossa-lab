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
    for cls in ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"):
        assert any(n.startswith(cls) for n in names), cls
    v4 = _check(report, "V4 relation-carrying")
    assert v4.status == "PASS"
    assert "1363 matrix cells" in v4.evidence[0]


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
