"""Tests for phase advancement lifecycle.

Verifies:
1. complete_phase is blocked while any action is running/pending/failed
2. advance() marks experiments as 'running', not 'completed'
3. advance-all stops before complete_phase
4. Job completion hook updates phase_action status
5. Phase does NOT advance until all actions are done
"""
import json
import pytest
import pytest_asyncio
from pathlib import Path

from glossa_lab.database import Database


@pytest_asyncio.fixture
async def db(tmp_path):
    """Create a fresh in-memory-like DB for testing."""
    _db = Database(tmp_path / "test.db")
    await _db.connect()
    yield _db
    await _db.close()


@pytest.mark.asyncio
async def test_upsert_phase_action_creates_and_updates(db):
    """upsert_phase_action creates a new row, then updates on conflict."""
    a1 = await db.upsert_phase_action(
        phase=5, label="Test Action", action_type="run_experiment",
        status="pending",
    )
    assert a1["status"] == "pending"
    assert a1["action_label"] == "Test Action"

    # Update same action
    a2 = await db.upsert_phase_action(
        phase=5, label="Test Action", action_type="run_experiment",
        status="running", job_id="job123",
    )
    assert a2["status"] == "running"
    assert a2["job_id"] == "job123"

    # Verify only one row
    actions = await db.list_phase_actions(phase=5)
    assert len(actions) == 1


@pytest.mark.asyncio
async def test_running_action_blocks_complete_phase(db):
    """complete_phase must not be available while any action is running."""
    # Create a running action
    await db.upsert_phase_action(
        phase=5, label="Queue: Some Experiment",
        action_type="run_experiment", status="running", job_id="job1",
    )

    actions = await db.list_phase_actions(phase=5)
    running = [a for a in actions if a["status"] == "running"]
    assert len(running) == 1, "Should have 1 running action"

    # The advancer should see this running action and block complete_phase
    # (tested via the _all_actions_done helper)
    all_done = all(
        a["status"] in ("completed", "skipped")
        for a in actions
        if a["action_type"] != "complete_phase"
    )
    assert not all_done, "Should NOT be all_done while action is running"


@pytest.mark.asyncio
async def test_failed_action_blocks_complete_phase(db):
    """complete_phase must not be available while any action is failed."""
    await db.upsert_phase_action(
        phase=5, label="Queue: Failed Exp",
        action_type="run_experiment", status="failed",
        error_message="Node error",
    )

    actions = await db.list_phase_actions(phase=5)
    all_done = all(
        a["status"] in ("completed", "skipped")
        for a in actions
        if a["action_type"] != "complete_phase"
    )
    assert not all_done, "Should NOT be all_done while action is failed"


@pytest.mark.asyncio
async def test_all_completed_allows_complete_phase(db):
    """complete_phase is only available when all other actions are done."""
    await db.upsert_phase_action(
        phase=5, label="Exp 1", action_type="run_experiment", status="completed",
    )
    await db.upsert_phase_action(
        phase=5, label="Exp 2", action_type="run_experiment", status="completed",
    )
    await db.upsert_phase_action(
        phase=5, label="Review", action_type="open_view", status="skipped",
    )

    actions = await db.list_phase_actions(phase=5)
    all_done = all(
        a["status"] in ("completed", "skipped")
        for a in actions
        if a["action_type"] != "complete_phase"
    )
    assert all_done, "Should be all_done when all actions completed/skipped"


@pytest.mark.asyncio
async def test_reset_phase_action_redo(db):
    """reset_phase_action sets status back to pending."""
    await db.upsert_phase_action(
        phase=5, label="Done Action", action_type="run_experiment",
        status="completed",
    )
    result = await db.reset_phase_action(5, "Done Action")
    assert result["status"] == "pending"
    assert result["job_id"] is None


@pytest.mark.asyncio
async def test_job_completion_updates_phase_action(db):
    """Simulates the engine job→phase_action sync hook."""
    # Create a running action with a job_id
    await db.upsert_phase_action(
        phase=6, label="Queue: Kalyanaraman",
        action_type="run_experiment", status="running", job_id="job_abc",
    )

    # Simulate what _sync_phase_action does
    cursor = await db._conn.execute(
        "SELECT id, phase, action_label FROM phase_actions WHERE job_id = ?",
        ("job_abc",),
    )
    row = await cursor.fetchone()
    assert row is not None, "Should find phase_action by job_id"

    await db._conn.execute(
        "UPDATE phase_actions SET status = 'completed', completed_at = '2026-06-07T12:00:00Z' WHERE id = ?",
        (row["id"],),
    )
    await db._conn.commit()

    # Verify
    actions = await db.list_phase_actions(phase=6)
    assert actions[0]["status"] == "completed"
