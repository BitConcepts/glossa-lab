"""Tests for database initialisation (TEST-BE-004)."""

import asyncio
import tempfile
from pathlib import Path

import pytest

from glossa_lab.database import Database


@pytest.fixture()
def tmp_db_path(tmp_path: Path) -> Path:
    return tmp_path / "test.db"


def test_database_creates_file(tmp_db_path: Path):
    """Database file is created on connect."""

    async def _run():
        db = Database(tmp_db_path)
        await db.connect()
        assert tmp_db_path.exists()
        await db.close()

    asyncio.get_event_loop().run_until_complete(_run())


def test_schema_tables_exist(tmp_db_path: Path):
    """Schema creates _schema_version and jobs tables."""

    async def _run():
        db = Database(tmp_db_path)
        await db.connect()

        # Verify tables
        import aiosqlite

        async with aiosqlite.connect(str(tmp_db_path)) as conn:
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = {row[0] for row in await cursor.fetchall()}
        assert "_schema_version" in tables
        assert "jobs" in tables

        await db.close()

    asyncio.get_event_loop().run_until_complete(_run())


def test_job_crud_roundtrip(tmp_db_path: Path):
    """Create, read, list, cancel a job."""

    async def _run():
        db = Database(tmp_db_path)
        await db.connect()

        # Create
        job = await db.create_job(name="test", created_at="2026-01-01T00:00:00Z")
        assert job["name"] == "test"
        assert job["status"] == "pending"
        job_id = job["id"]

        # Read
        fetched = await db.get_job(job_id)
        assert fetched is not None
        assert fetched["id"] == job_id

        # List
        jobs = await db.list_jobs()
        assert len(jobs) == 1

        # Cancel
        cancelled = await db.cancel_job(job_id)
        assert cancelled["status"] == "cancelled"

        # Counts
        counts = await db.get_job_counts()
        assert counts["total"] == 1
        assert counts["cancelled"] == 1

        await db.close()

    asyncio.get_event_loop().run_until_complete(_run())
