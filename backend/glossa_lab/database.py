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

_SCHEMA_VERSION = 2

_SCHEMA_V1 = """
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

_SCHEMA_V2 = """
CREATE TABLE IF NOT EXISTS texts (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    corpus_type   TEXT NOT NULL DEFAULT 'linguistic',
    content       TEXT NOT NULL,
    alphabet_size INTEGER NOT NULL DEFAULT 0,
    symbol_set    TEXT NOT NULL DEFAULT '[]',
    metadata      TEXT NOT NULL DEFAULT '{}',
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS job_results (
    id         TEXT PRIMARY KEY,
    job_id     TEXT NOT NULL REFERENCES jobs(id),
    data       TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
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
        # Always apply v1 (uses IF NOT EXISTS)
        await self._conn.executescript(_SCHEMA_V1)

        cursor = await self._conn.execute("SELECT version FROM _schema_version")
        row = await cursor.fetchone()
        current_version = row["version"] if row else 0

        if current_version < 1:
            await self._conn.execute(
                "INSERT INTO _schema_version (version) VALUES (?)", (1,)
            )
            current_version = 1

        if current_version < 2:
            await self._conn.executescript(_SCHEMA_V2)
            await self._conn.execute(
                "UPDATE _schema_version SET version = ?", (2,)
            )

        await self._conn.commit()

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

    async def clear_jobs(self) -> int:
        """Delete all jobs and job results, returning the number of jobs removed."""
        assert self._conn
        cursor = await self._conn.execute("SELECT COUNT(*) AS cnt FROM jobs")
        row = await cursor.fetchone()
        cleared = int(row["cnt"]) if row else 0
        await self._conn.execute("DELETE FROM job_results")
        await self._conn.execute("DELETE FROM jobs")
        await self._conn.commit()
        return cleared

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

    # ── Texts ─────────────────────────────────────────────────────────

    async def create_text(
        self,
        *,
        name: str,
        corpus_type: str = "linguistic",
        content: list[str],
        metadata: dict[str, Any] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        text_id = uuid.uuid4().hex[:12]
        symbol_set = sorted(set(content))
        alphabet_size = len(symbol_set)
        await self._conn.execute(
            """INSERT INTO texts
               (id, name, corpus_type, content, alphabet_size,
                symbol_set, metadata, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                text_id, name, corpus_type,
                json.dumps(content), alphabet_size,
                json.dumps(symbol_set),
                json.dumps(metadata or {}), created_at,
            ),
        )
        await self._conn.commit()
        return await self.get_text(text_id)  # type: ignore[return-value]

    async def list_texts(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM texts ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [self._row_to_dict(r) for r in rows]

    async def get_text(self, text_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM texts WHERE id = ?", (text_id,)
        )
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_text(
        self,
        text_id: str,
        *,
        name: str | None = None,
        corpus_type: str | None = None,
        content: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Update a text corpus and recompute derived fields when content changes."""
        assert self._conn
        existing = await self.get_text(text_id)
        if existing is None:
            return None

        next_name = name if name is not None else existing["name"]
        next_corpus_type = corpus_type if corpus_type is not None else existing["corpus_type"]
        next_content = content if content is not None else existing["content"]
        next_metadata = metadata if metadata is not None else existing["metadata"]
        next_symbol_set = sorted(set(next_content))
        next_alphabet_size = len(next_symbol_set)

        await self._conn.execute(
            """UPDATE texts
               SET name = ?, corpus_type = ?, content = ?, alphabet_size = ?,
                   symbol_set = ?, metadata = ?
               WHERE id = ?""",
            (
                next_name,
                next_corpus_type,
                json.dumps(next_content),
                next_alphabet_size,
                json.dumps(next_symbol_set),
                json.dumps(next_metadata),
                text_id,
            ),
        )
        await self._conn.commit()
        return await self.get_text(text_id)

    async def delete_text(self, text_id: str) -> dict[str, Any] | None:
        """Delete a text corpus and return the deleted record."""
        assert self._conn
        existing = await self.get_text(text_id)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM texts WHERE id = ?", (text_id,))
        await self._conn.commit()
        return existing

    # ── Job results ──────────────────────────────────────────────────

    async def store_result(
        self, *, job_id: str, data: dict[str, Any], created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        result_id = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO job_results (id, job_id, data, created_at)
               VALUES (?, ?, ?, ?)""",
            (result_id, job_id, json.dumps(data), created_at),
        )
        await self._conn.commit()
        return {"id": result_id, "job_id": job_id, "data": data}

    async def get_result_for_job(
        self, job_id: str,
    ) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM job_results WHERE job_id = ?", (job_id,)
        )
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_job_status(
        self, job_id: str, status: str,
    ) -> None:
        assert self._conn
        await self._conn.execute(
            "UPDATE jobs SET status = ?, updated_at = datetime('now') "
            "WHERE id = ?",
            (status, job_id),
        )
        await self._conn.commit()

    async def claim_pending_job(self) -> dict[str, Any] | None:
        """Atomically claim the oldest pending job."""
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM jobs WHERE status = 'pending' "
            "ORDER BY created_at ASC LIMIT 1"
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        job = self._row_to_dict(row)
        await self.update_job_status(job["id"], "running")
        return job

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(row: aiosqlite.Row) -> dict[str, Any]:
        d = dict(row)
        # Deserialise JSON columns
        for field in ("params", "content", "symbol_set", "metadata", "data"):
            if field in d and isinstance(d[field], str):
                d[field] = json.loads(d[field])
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
