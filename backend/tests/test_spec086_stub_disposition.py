"""Spec 086 T406 — the constraint-projection stub's
disposition (Spec 085 C085-15, carried in).

Disposition: REMOVED FROM THE PALETTE WITH A POINTER.
The CASHypothesisProjector node's registration left the
palette with the CPSC engine in May 2026 (commit
60faf1c3) and was never restored; what remained was the
orphan stub function `_cas_hypothesis_projector` in
experiment_graph_phase14.py, returning the "engine
removed" error dict to any caller. T406 removes the
stub from the codebase path and leaves a pointer at its
site to the capability's successor, the glossa-settle-1
settling engine (backend/glossa_lab/settling.py,
operated via tools/ledger/run_settling.py). Wiring was
rejected on the record: the node's contract presupposed
the deleted CAS-YAML/CPSC machinery (a continuous
max_violation over measured DoF values), which the
settling semantics do not compute and must not be made
to imitate. Grounds in full: stage-4-record.md (T406).

These tests pin the disposition:
- the stub error string is absent from the codebase
  path (Spec 085 T017's acceptance);
- the stub function and its node are absent;
- the pointer's target (the settling engine) is real;
- the downstream consumer (LanguageDetectorVerdict)
  works unfed and accepts a well-formed input shape
  without erroring (C085-15's falsifier, second leg).
"""

from __future__ import annotations

from pathlib import Path

from glossa_lab import experiment_graph_phase14 as phase14
from glossa_lab.experiment_graph import ATOMIC_NODES

BACKEND = Path(__file__).resolve().parents[1]
STUB_ERROR = "Constraint projection engine not available."


def test_stub_error_string_absent_from_codebase_path() -> None:
    """Spec 085 T017: the stub error string is absent
    from the codebase path (the backend package source;
    spec documents quoting the audit finding are records,
    not the code path)."""
    offenders = []
    for path in sorted((BACKEND / "glossa_lab").rglob("*.py")):
        if STUB_ERROR in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(BACKEND)))
    assert offenders == [], (
        f"stub error string still present in: {offenders}"
    )


def test_stub_function_removed() -> None:
    assert not hasattr(phase14, "_cas_hypothesis_projector")


def test_palette_has_no_constraint_projection_node() -> None:
    assert "CASHypothesisProjector" not in ATOMIC_NODES
    for node_id, node in ATOMIC_NODES.items():
        assert getattr(node.fn, "__name__", "") != (
            "_cas_hypothesis_projector"
        ), f"node {node_id} is backed by the removed stub"


def test_pointer_target_is_the_real_settling_engine() -> None:
    """The pointer at the stub's former site names the
    glossa-settle-1 settling engine; that target exists
    and exposes the run/comparison builders."""
    from glossa_lab import settling

    assert settling.SEMANTICS_VERSION == "glossa-settle-1"
    assert callable(settling.run_record)
    assert callable(settling.compare_runs)
    cli = BACKEND.parent / "tools" / "ledger" / "run_settling.py"
    assert cli.is_file()


def test_downstream_consumer_unfed_and_wellformed_fed() -> None:
    """LanguageDetectorVerdict consumes cas_projection
    optionally: unfed it returns a well-formed verdict;
    fed a well-formed projection-shaped input it does
    not error (C085-15's falsifier, second leg)."""
    unfed = phase14._language_detector_verdict({}, {})
    assert "error" not in unfed
    assert isinstance(unfed["is_language"], bool)
    assert isinstance(unfed["verdict"], str)

    fed = phase14._language_detector_verdict(
        {"cas_projection": {"success": True, "max_violation": 0.0}},
        {},
    )
    assert "error" not in fed
    assert any(
        "CAS projection succeeded" in line
        for line in fed["evidence_for"]
    )
