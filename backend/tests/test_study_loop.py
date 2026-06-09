"""Tests for the Autonomous Study Loop pipeline.

TEST-SL-001  Direct analysis: every template runs and returns a non-empty verdict.
TEST-SL-002  Proposals always execute: 3-cycle loop produces zero gap_skipped events.
TEST-SL-003  Iterations meaning: max_cycles=3 produces exactly 3 node_complete events.
TEST-SL-004  Verify fallback: all proposals return 'skip' → experiments still run.
TEST-SL-005  Verify abort: all proposals return 'abort' → gap is skipped.
TEST-SL-006  Rotation fallback: empty proposals list → still reaches execution.
TEST-SL-007  Cycle logging: verify that cycle-start log entries are emitted.
"""
from __future__ import annotations

import logging
from unittest.mock import MagicMock, patch


from glossa_lab.loop_proposal import (
    VerificationResult,
)
from glossa_lab.pipelines.research_loop import (
    EXPERIMENT_NAMES,
    ResearchLoop,
)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_loop(*, max_cycles: int = 3) -> ResearchLoop:
    """Create a ResearchLoop with mocked external I/O (no network, no files)."""
    with patch.object(ResearchLoop, "_load_corpus"), \
         patch.object(ResearchLoop, "_load_anchors"):
        loop = ResearchLoop(max_cycles=max_cycles)
    # Provide minimal corpus data so direct_analysis works
    loop.corpus_seqs = [["H001", "H002", "H003"]] * 50
    loop.corpus_sites = ["Mohenjo-daro"] * 50
    loop.corpus_motifs = ["unicorn"] * 50
    loop.anchors = {
        "H001": {"reading": "ko", "confidence": "HIGH", "basis": "positional"},
        "H002": {"reading": "an", "confidence": "MEDIUM", "basis": "DEDR"},
        "H003": {"reading": "", "confidence": "LOW", "basis": ""},
    }
    loop.high_signs = {"H001", "H002"}
    loop.low_signs = {"H003"}
    loop.blocker_signs = {"H003"}
    return loop


def _collect_events(loop: ResearchLoop) -> list[dict]:
    """Run the loop with mocked mining and collect all yielded events."""
    with patch.object(loop, "_blitz_mine", return_value=([], [], {"reading": 0.5})), \
         patch.object(loop, "_mine", return_value=(
             [{"title": "Test paper", "abstract": "Indus script sign reading"}],
             [{"type": "reading", "title": "Test"}],
         )):
        return list(loop.run())


# ── TEST-SL-001 ──────────────────────────────────────────────────────────────


def test_direct_analysis_all_templates():
    """TEST-SL-001: Every template in EXPERIMENT_NAMES runs without error
    and returns a non-empty verdict string."""
    loop = _make_loop(max_cycles=1)
    for template in EXPERIMENT_NAMES:
        verdict, output = loop._direct_analysis(template)
        assert isinstance(verdict, str), f"{template}: verdict is not a string"
        assert len(verdict) > 0, f"{template}: verdict is empty"
        assert isinstance(output, dict), f"{template}: output is not a dict"


# ── TEST-SL-002 ──────────────────────────────────────────────────────────────


def test_proposals_always_execute():
    """TEST-SL-002: A 3-cycle loop produces zero gap_skipped events.

    With corpus available (50 seqs, 3 anchors), verify_before_run should
    return 'pass' or at worst 'skip' — never triggering gap_skipped.
    """
    loop = _make_loop(max_cycles=3)
    events = _collect_events(loop)

    gap_skipped = [e for e in events if e.get("type") == "gap_skipped"]
    assert len(gap_skipped) == 0, (
        f"Expected 0 gap_skipped events, got {len(gap_skipped)}: "
        f"{[e.get('reason') for e in gap_skipped]}"
    )

    node_complete = [e for e in events if e.get("type") == "node_complete"]
    assert len(node_complete) > 0, "Expected at least one node_complete event"


# ── TEST-SL-003 ──────────────────────────────────────────────────────────────


def test_iterations_meaning():
    """TEST-SL-003: max_cycles=3 produces exactly 3 node_complete events.

    Each experiment cycle emits exactly one node_complete event, so
    the count of node_complete events must equal max_cycles.
    """
    loop = _make_loop(max_cycles=3)
    events = _collect_events(loop)

    node_complete = [e for e in events if e.get("type") == "node_complete"]
    assert len(node_complete) == 3, (
        f"Expected exactly 3 node_complete events for max_cycles=3, "
        f"got {len(node_complete)}"
    )


# ── TEST-SL-004 ──────────────────────────────────────────────────────────────


def test_loop_verify_fallback_skip():
    """TEST-SL-004: When all proposals return 'skip', experiments still run.

    'skip' is a warning, not a hard block. The loop should use the
    best-scoring skip proposal and continue to execution.
    """
    loop = _make_loop(max_cycles=1)

    # Mock verify_before_run to always return "skip"
    skip_vr = VerificationResult(
        ok=False,
        issues=["Very small corpus (3 sequences)"],
        recommendation="skip",
    )

    with patch.object(loop, "_blitz_mine", return_value=([], [], {"reading": 0.5})), \
         patch.object(loop, "_mine", return_value=(
             [{"title": "Test paper", "abstract": "Indus script"}],
             [{"type": "reading", "title": "Test"}],
         )), \
         patch(
             "glossa_lab.loop_proposal.verify_before_run",
             return_value=skip_vr,
         ):
        events = list(loop.run())

    gap_skipped = [e for e in events if e.get("type") == "gap_skipped"]
    node_complete = [e for e in events if e.get("type") == "node_complete"]

    assert len(gap_skipped) == 0, (
        f"Skip proposals should not cause gap_skipped, got {len(gap_skipped)}"
    )
    assert len(node_complete) == 1, (
        f"Expected 1 node_complete with skip fallback, got {len(node_complete)}"
    )


# ── TEST-SL-005 ──────────────────────────────────────────────────────────────


def test_loop_verify_abort_skips_gap():
    """TEST-SL-005: When ALL proposals return 'abort', the gap is skipped."""
    loop = _make_loop(max_cycles=1)

    abort_vr = VerificationResult(
        ok=False,
        issues=["No corpus data available for this experiment"],
        recommendation="abort",
    )

    with patch.object(loop, "_blitz_mine", return_value=([], [], {"reading": 0.5})), \
         patch.object(loop, "_mine", return_value=(
             [{"title": "Test paper", "abstract": "Indus script"}],
             [{"type": "reading", "title": "Test"}],
         )), \
         patch(
             "glossa_lab.loop_proposal.verify_before_run",
             return_value=abort_vr,
         ):
        events = list(loop.run())

    gap_skipped = [e for e in events if e.get("type") == "gap_skipped"]
    assert len(gap_skipped) == 1, (
        f"Expected 1 gap_skipped when all abort, got {len(gap_skipped)}"
    )


# ── TEST-SL-006 ──────────────────────────────────────────────────────────────


def test_rotation_fallback_executes():
    """TEST-SL-006: When ProposalEngine returns [], the rotation fallback
    still reaches experiment execution and produces a node_complete."""
    loop = _make_loop(max_cycles=1)

    # Force ProposalEngine to return empty list
    loop._proposal_engine.propose = MagicMock(return_value=[])

    with patch.object(loop, "_blitz_mine", return_value=([], [], {})), \
         patch.object(loop, "_mine", return_value=(
             [{"title": "Test paper", "abstract": "Formula"}],
             [{"type": "formula", "title": "Test"}],
         )):
        events = list(loop.run())

    node_complete = [e for e in events if e.get("type") == "node_complete"]
    assert len(node_complete) == 1, (
        f"Rotation fallback should produce 1 node_complete, got {len(node_complete)}"
    )

    # Verify it used "rotation" selection method
    assert node_complete[0]["selection_method"] == "rotation"


# ── TEST-SL-007 ──────────────────────────────────────────────────────────────


def test_cycle_logging(caplog):
    """TEST-SL-007: Cycle-start log entries are emitted for each cycle."""
    loop = _make_loop(max_cycles=2)

    with caplog.at_level(logging.INFO, logger="glossa_lab.pipelines.research_loop"):
        _collect_events(loop)

    cycle_logs = [r for r in caplog.records if "=== Cycle" in r.message]
    assert len(cycle_logs) >= 2, (
        f"Expected at least 2 cycle-start log lines, got {len(cycle_logs)}"
    )

    template_logs = [r for r in caplog.records if "template=" in r.message]
    assert len(template_logs) >= 2, (
        f"Expected at least 2 template-selection logs, got {len(template_logs)}"
    )
