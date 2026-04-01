"""SQLite database layer for Glossa Lab (REQ-BE-004).

Uses aiosqlite for async access. Initialises schema automatically
on first startup. Simple version-based migration support.
"""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Any

import aiosqlite

logger = logging.getLogger(__name__)

_SCHEMA_VERSION = 1

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS _schema_version (
    version INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id         TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    pipeline   TEXT NOT NULL DEFAULT 'default',
    status     TEXT NOT NULL DEFAULT 'pending',
    params     TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

# Module-level singleton
_db: Database | None = None


def get_db() -> Database | None:
    """Return the current database instance (may be None before startup)."""
    return _db


class Database:
    """Thin async wrapper around an SQLite database."""

    def __init__(self, db_path: Path) -> None:
        self._path = db_path
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        """Open the database and ensure the schema exists."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(str(self._path))
        self._conn.row_factory = aiosqlite.Row
        await self._apply_schema()
        logger.info("Database ready", extra={"path": str(self._path)})

    async def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    # ── Schema / migrations ──────────────────────────────────────────

    async def _apply_schema(self) -> None:
        assert self._conn
        await self._conn.executescript(_SCHEMA_SQL)

        cursor = await self._conn.execute("SELECT version FROM _schema_version")
        row = await cursor.fetchone()
        if row is None:
            await self._conn.execute(
                "INSERT INTO _schema_version (version) VALUES (?)", (_SCHEMA_VERSION,)
            )
            await self._conn.commit()
        # Future migrations would go here: if row["version"] < 2: ...

    # ── Jobs ─────────────────────────────────────────────────────────

    async def create_job(
        self,
        *,
        name: str,
        pipeline: str = "default",
        params: dict[str, Any] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        job_id = uuid.uuid4().hex[:12]
        params_json = json.dumps(params or {})
        await self._conn.execute(
            """INSERT INTO jobs (id, name, pipeline, status, params, created_at, updated_at)
               VALUES (?, ?, ?, 'pending', ?, ?, ?)""",
            (job_id, name, pipeline, params_json, created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_job(job_id)  # type: ignore[return-value]

    async def list_jobs(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [self._row_to_dict(r) for r in rows]

    async def get_job(self, job_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def cancel_job(self, job_id: str) -> dict[str, Any] | None:
        assert self._conn
        job = await self.get_job(job_id)
        if job is None:
            return None
        await self._conn.execute(
            "UPDATE jobs SET status = 'cancelled', updated_at = datetime('now') WHERE id = ?",
            (job_id,),
        )
        await self._conn.commit()
        return await self.get_job(job_id)

    async def get_job_counts(self) -> dict[str, int]:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT status, COUNT(*) as cnt FROM jobs GROUP BY status"
        )
        rows = await cursor.fetchall()
        counts = {
            "total": 0, "pending": 0, "running": 0,
            "completed": 0, "failed": 0, "cancelled": 0,
        }
        for row in rows:
            s = row["status"]
            c = row["cnt"]
            if s in counts:
                counts[s] = c
            counts["total"] += c
        return counts

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(row: aiosqlite.Row) -> dict[str, Any]:
        d = dict(row)
        # Deserialise JSON params
        if "params" in d and isinstance(d["params"], str):
            d["params"] = json.loads(d["params"])
        return d


async def init_db(data_dir: Path) -> Database:
    """Create and connect the global database singleton."""
    global _db  # noqa: PLW0603
    db_path = data_dir / "glossa.db"
    _db = Database(db_path)
    await _db.connect()
    return _db


async def close_db() -> None:
    """Close the global database connection."""
    global _db  # noqa: PLW0603
    if _db:
        await _db.close()
        _db = None
