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
"""

from __future__ import annotations

import asyncio

import pytest

import glossa_lab.database as _database
import glossa_lab.engine as _engine
from glossa_lab.database import Database
from glossa_lab.engine import run_engine_loop


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
