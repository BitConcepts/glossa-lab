"""Regression test: engine loop exits cleanly when its DB closes mid-run.

CI teardown flake, 2026-11-06/07 (runs 42220891977, 42245110090, 42250965563,
42251859916, 42258269523): the session TestClient teardown awaited the engine
task while the loop was mid-iteration against a database closed by another
TestClient lifespan's shutdown — `sqlite3.ProgrammingError: Cannot operate on
a closed database`, `AssertionError` from `assert self._conn`, or aiosqlite
`ValueError: no active connection` when the close lands between a query and
its fetch — reported as "ERROR at teardown of
test_run_check_verdict_and_missing_db". The loop must stop cleanly when its
database is verifiably gone instead of failing the session teardown.

The test installs a throwaway database as the engine's global, starts the
loop, closes the database under it (the shutdown race), and asserts the loop
task ends without raising. On the unfixed code the task raises AssertionError
(the next iteration trips `assert self._conn` in peek_next_pending_job).

Second face, 2026-11-10 (runs 42729580150 on main and 42731318567, same
teardown ERROR): PR #541's loop-level handler judged "database gone" by the
GLOBAL singleton (`get_db()`), but `_process_one` claims through the
Database instance it captured at iteration start. When the close lands
between peek and claim AND another lifespan has already installed a fresh,
connected singleton (its `init_db`), the handler reads the new singleton as
connected and re-raises — the AssertionError from `claim_pending_job`
escapes anyway. The second test below drives exactly that interleaving
deterministically: peek a real pending job, close the captured database,
replace the global singleton with a fresh connected one, then let the
iteration reach the claim. The fix judges the signal against the captured
instance and converts it to a clean loop stop; a third test pins the
opposite boundary — a claim AssertionError raised while the captured
database is still connected is NOT swallowed.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

import glossa_lab.database as _database
import glossa_lab.engine as _engine
from glossa_lab.database import Database
from glossa_lab.engine import _process_one, run_engine_loop


@pytest.mark.asyncio
async def test_engine_loop_stops_cleanly_when_db_closes(tmp_path):
    """Closing the database under a running loop ends the loop, not the test."""
    db = Database(tmp_path / "engine-race.db")
    await db.connect()
    saved_db = _database._db
    _database._db = db
    try:
        loop_task = asyncio.create_task(run_engine_loop(poll_interval=0.05))
        # Wait until the loop is past startup (pipelines loaded) so the close
        # lands on a live iteration, not on startup imports. Bounded wait.
        deadline = asyncio.get_running_loop().time() + 15
        while not _engine._PIPELINE_MODULES_LOADED:
            if asyncio.get_running_loop().time() > deadline:
                pytest.fail("engine loop did not reach startup within 15s")
            await asyncio.sleep(0.05)
        # Let the orphan sweep and first peek complete.
        await asyncio.sleep(0.3)
        assert not loop_task.done()
        # Simulate the shutdown race: another lifespan closes the shared DB.
        await db.close()
        # The loop must exit on its own (next iteration finds the DB gone),
        # not raise the closed-database error out of the task.
        await asyncio.wait_for(loop_task, timeout=10)
        assert loop_task.done() and not loop_task.cancelled()
        assert loop_task.exception() is None
    finally:
        _database._db = saved_db


@pytest.mark.asyncio
async def test_engine_loop_stops_cleanly_when_db_closed_and_singleton_replaced(
    tmp_path, monkeypatch
):
    """Close between peek and claim, with a fresh singleton already installed.

    Deterministic form of the 2026-11-10 CI failure: the loop peeks a real
    pending job on DB-A; DB-A is closed and the global singleton is replaced
    by a fresh, connected DB-B (another lifespan's init_db) before the
    iteration reaches claim_pending_job. On the PR #541 code the claim's
    AssertionError escapes the loop, because the handler consults get_db()
    (DB-B, connected) instead of the captured DB-A. With the fix the loop
    task ends without raising.
    """
    db_old = Database(tmp_path / "old.db")
    await db_old.connect()
    await db_old.create_job(
        name="race-job",
        pipeline="default",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db_new = Database(tmp_path / "new.db")
    await db_new.connect()

    # Deterministic resources so the iteration always proceeds to the claim.
    monkeypatch.setattr(_engine, "_get_system_resources", lambda: (0.0, 999.0, None))

    saved_db = _database._db
    _database._db = db_old
    original_peek = db_old.peek_next_pending_job

    async def peek_then_close_and_replace():
        row = await original_peek()
        await db_old.close()
        _database._db = db_new  # another lifespan's init_db lands here
        return row

    db_old.peek_next_pending_job = peek_then_close_and_replace
    loop_task = asyncio.create_task(run_engine_loop(poll_interval=0.05))
    try:
        await asyncio.wait_for(loop_task, timeout=30)
        assert loop_task.done() and not loop_task.cancelled()
        assert loop_task.exception() is None
    finally:
        if not loop_task.done():
            loop_task.cancel()
        _database._db = saved_db
        await db_new.close()


@pytest.mark.asyncio
async def test_process_one_reraises_claim_assertion_while_db_connected(tmp_path, monkeypatch):
    """The tolerance is scoped: a claim AssertionError on a LIVE database
    must still fail loudly, not be converted into a clean stop."""
    db = Database(tmp_path / "live.db")
    await db.connect()
    await db.create_job(
        name="live-job",
        pipeline="default",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    monkeypatch.setattr(_engine, "_get_system_resources", lambda: (0.0, 999.0, None))

    async def asserting_claim():
        raise AssertionError("boom: real claim defect")

    db.claim_pending_job = asserting_claim
    saved_db = _database._db
    _database._db = db
    try:
        with pytest.raises(AssertionError, match="real claim defect"):
            await _process_one()
    finally:
        _database._db = saved_db
        await db.close()
