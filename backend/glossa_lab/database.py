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

# Increment this when adding a new _SCHEMA_Vn block below.
# _apply_schema will raise if the DB is somehow ahead of the code.
_SCHEMA_VERSION = 5

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

_SCHEMA_V3 = """
CREATE TABLE IF NOT EXISTS studies (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    graph_json  TEXT NOT NULL DEFAULT '{"nodes":[],"edges":[]}',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

_SCHEMA_V4 = """
CREATE TABLE IF NOT EXISTS hypotheses (
    id           TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    statement    TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL DEFAULT 'active',
    evidence     TEXT NOT NULL DEFAULT '[]',
    study_ids    TEXT NOT NULL DEFAULT '[]',
    exp_ids      TEXT NOT NULL DEFAULT '[]',
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notebooks (
    id           TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    content      TEXT NOT NULL DEFAULT '',
    study_id     TEXT,
    tags         TEXT NOT NULL DEFAULT '[]',
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS citations (
    id           TEXT PRIMARY KEY,
    key          TEXT NOT NULL UNIQUE,
    title        TEXT NOT NULL DEFAULT '',
    authors      TEXT NOT NULL DEFAULT '',
    year         TEXT NOT NULL DEFAULT '',
    venue        TEXT NOT NULL DEFAULT '',
    doi          TEXT NOT NULL DEFAULT '',
    url          TEXT NOT NULL DEFAULT '',
    bibtex       TEXT NOT NULL DEFAULT '',
    exp_ids      TEXT NOT NULL DEFAULT '[]',
    study_ids    TEXT NOT NULL DEFAULT '[]',
    notes        TEXT NOT NULL DEFAULT '',
    created_at   TEXT NOT NULL
);
"""

_SCHEMA_V5 = """
CREATE TABLE IF NOT EXISTS collab_messages (
    id         TEXT PRIMARY KEY,
    study_id   TEXT NOT NULL,
    author     TEXT NOT NULL DEFAULT '',
    message    TEXT NOT NULL,
    pinned     INTEGER NOT NULL DEFAULT 0,
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
            await self._conn.execute("INSERT INTO _schema_version (version) VALUES (?)", (1,))
            current_version = 1

        if current_version < 2:
            await self._conn.executescript(_SCHEMA_V2)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (2,))
            current_version = 2

        if current_version < 3:
            await self._conn.executescript(_SCHEMA_V3)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (3,))
            current_version = 3

        if current_version < 4:
            await self._conn.executescript(_SCHEMA_V4)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (4,))
            current_version = 4

        if current_version < 5:
            await self._conn.executescript(_SCHEMA_V5)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (5,))

        if current_version > _SCHEMA_VERSION:
            logger.warning(
                "DB schema version %s is ahead of code version %s",
                current_version,
                _SCHEMA_VERSION,
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
        cursor = await self._conn.execute("SELECT * FROM jobs ORDER BY created_at DESC")
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

    async def clear_finished_jobs(self) -> int:
        """Delete only completed and cancelled jobs (leaves pending/running)."""
        assert self._conn
        statuses = ("completed", "cancelled", "failed")
        placeholders = ",".join("?" * len(statuses))
        # Remove results for finished jobs first
        await self._conn.execute(
            f"DELETE FROM job_results WHERE job_id IN "
            f"(SELECT id FROM jobs WHERE status IN ({placeholders}))",
            statuses,
        )
        cursor = await self._conn.execute(
            f"DELETE FROM jobs WHERE status IN ({placeholders}) RETURNING id",
            statuses,
        )
        rows = await cursor.fetchall()
        await self._conn.commit()
        return len(rows)

    async def get_job_counts(self) -> dict[str, int]:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT status, COUNT(*) as cnt FROM jobs GROUP BY status"
        )
        rows = await cursor.fetchall()
        counts = {
            "total": 0,
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
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
                text_id,
                name,
                corpus_type,
                json.dumps(content),
                alphabet_size,
                json.dumps(symbol_set),
                json.dumps(metadata or {}),
                created_at,
            ),
        )
        await self._conn.commit()
        return await self.get_text(text_id)  # type: ignore[return-value]

    async def list_texts(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM texts ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        return [self._row_to_dict(r) for r in rows]

    async def get_text(self, text_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM texts WHERE id = ?", (text_id,))
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
        self,
        *,
        job_id: str,
        data: dict[str, Any],
        created_at: str,
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
        self,
        job_id: str,
    ) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM job_results WHERE job_id = ?", (job_id,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_job_status(
        self,
        job_id: str,
        status: str,
    ) -> None:
        assert self._conn
        await self._conn.execute(
            "UPDATE jobs SET status = ?, updated_at = datetime('now') WHERE id = ?",
            (status, job_id),
        )
        await self._conn.commit()

    async def claim_pending_job(self) -> dict[str, Any] | None:
        """Atomically claim the oldest pending job."""
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM jobs WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        job = self._row_to_dict(row)
        await self.update_job_status(job["id"], "running")
        return job

    # ── Studies ────────────────────────────────────────────────

    async def create_study(
        self,
        *,
        name: str,
        description: str = "",
        graph: dict[str, Any] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        study_id = uuid.uuid4().hex[:12]
        graph_json = json.dumps(graph or {"nodes": [], "edges": []})
        await self._conn.execute(
            """INSERT INTO studies (id, name, description, graph_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (study_id, name, description, graph_json, created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_study(study_id)  # type: ignore[return-value]

    async def list_studies(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM studies ORDER BY updated_at DESC")
        rows = await cursor.fetchall()
        return [self._row_to_dict(r) for r in rows]

    async def get_study(self, study_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM studies WHERE id = ?", (study_id,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_study(
        self,
        study_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        graph: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_study(study_id)
        if existing is None:
            return None
        next_name = name if name is not None else existing["name"]
        next_desc = description if description is not None else existing["description"]
        next_graph = json.dumps(graph) if graph is not None else json.dumps(existing["graph"])
        await self._conn.execute(
            """UPDATE studies
               SET name = ?, description = ?, graph_json = ?,
                   updated_at = datetime('now')
               WHERE id = ?""",
            (next_name, next_desc, next_graph, study_id),
        )
        await self._conn.commit()
        return await self.get_study(study_id)

    async def delete_study(self, study_id: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_study(study_id)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM studies WHERE id = ?", (study_id,))
        await self._conn.commit()
        return existing

    # ── Hypotheses ─────────────────────────────────────────────────

    async def create_hypothesis(
        self,
        *,
        title: str,
        statement: str = "",
        status: str = "active",
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        hid = uuid.uuid4().hex[:12]
        await self._conn.execute(  # noqa: E501
            """INSERT INTO hypotheses
               (id,title,statement,status,evidence,study_ids,exp_ids,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (hid, title, statement, status, "[]", "[]", "[]", created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_hypothesis(hid)  # type: ignore[return-value]

    async def list_hypotheses(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM hypotheses ORDER BY updated_at DESC")
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_hypothesis(self, hid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM hypotheses WHERE id=?", (hid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_hypothesis(self, hid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_hypothesis(hid)
        if existing is None:
            return None
        title = fields.get("title", existing["title"])
        statement = fields.get("statement", existing["statement"])
        status = fields.get("status", existing["status"])
        evidence = (
            json.dumps(fields["evidence"])
            if "evidence" in fields
            else json.dumps(existing["evidence"])
        )
        study_ids = (
            json.dumps(fields["study_ids"])
            if "study_ids" in fields
            else json.dumps(existing["study_ids"])
        )
        exp_ids = (
            json.dumps(fields["exp_ids"])
            if "exp_ids" in fields
            else json.dumps(existing["exp_ids"])
        )
        await self._conn.execute(
            """UPDATE hypotheses SET title=?,statement=?,status=?,evidence=?,study_ids=?,exp_ids=?,
               updated_at=datetime('now') WHERE id=?""",
            (title, statement, status, evidence, study_ids, exp_ids, hid),
        )
        await self._conn.commit()
        return await self.get_hypothesis(hid)

    async def delete_hypothesis(self, hid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_hypothesis(hid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM hypotheses WHERE id=?", (hid,))
        await self._conn.commit()
        return existing

    # ── Notebooks ─────────────────────────────────────────────────

    async def create_notebook(
        self,
        *,
        title: str,
        content: str = "",
        study_id: str | None = None,
        tags: list[str] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        nid = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO notebooks (id,title,content,study_id,tags,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?)""",
            (nid, title, content, study_id, json.dumps(tags or []), created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_notebook(nid)  # type: ignore[return-value]

    async def list_notebooks(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM notebooks ORDER BY updated_at DESC")
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_notebook(self, nid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM notebooks WHERE id=?", (nid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_notebook(self, nid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_notebook(nid)
        if existing is None:
            return None
        title = fields.get("title", existing["title"])
        content = fields.get("content", existing["content"])
        study_id = fields.get("study_id", existing.get("study_id"))
        tags = (
            json.dumps(fields["tags"]) if "tags" in fields else json.dumps(existing.get("tags", []))
        )
        await self._conn.execute(
            """UPDATE notebooks SET title=?,content=?,study_id=?,tags=?,
               updated_at=datetime('now') WHERE id=?""",
            (title, content, study_id, tags, nid),
        )
        await self._conn.commit()
        return await self.get_notebook(nid)

    async def delete_notebook(self, nid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_notebook(nid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM notebooks WHERE id=?", (nid,))
        await self._conn.commit()
        return existing

    # ── Citations ─────────────────────────────────────────────────

    async def create_citation(
        self,
        *,
        key: str,
        title: str = "",
        authors: str = "",
        year: str = "",
        venue: str = "",
        doi: str = "",
        url: str = "",
        bibtex: str = "",
        notes: str = "",
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        cid = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO citations
               (id,key,title,authors,year,venue,doi,url,bibtex,exp_ids,study_ids,notes,created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                cid,
                key,
                title,
                authors,
                year,
                venue,
                doi,
                url,
                bibtex,
                "[]",
                "[]",
                notes,
                created_at,
            ),
        )
        await self._conn.commit()
        return await self.get_citation(cid)  # type: ignore[return-value]

    async def list_citations(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM citations ORDER BY year DESC, key ASC")
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_citation(self, cid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM citations WHERE id=?", (cid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_citation(self, cid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_citation(cid)
        if existing is None:
            return None
        for f in ("title", "authors", "year", "venue", "doi", "url", "bibtex", "notes"):
            existing[f] = fields.get(f, existing[f])
        exp_ids = (
            json.dumps(fields["exp_ids"])
            if "exp_ids" in fields
            else json.dumps(existing["exp_ids"])
        )
        study_ids = (
            json.dumps(fields["study_ids"])
            if "study_ids" in fields
            else json.dumps(existing["study_ids"])
        )
        await self._conn.execute(
            """UPDATE citations SET title=?,authors=?,year=?,venue=?,doi=?,url=?,bibtex=?,
               exp_ids=?,study_ids=?,notes=? WHERE id=?""",
            (
                existing["title"],
                existing["authors"],
                existing["year"],
                existing["venue"],
                existing["doi"],
                existing["url"],
                existing["bibtex"],
                exp_ids,
                study_ids,
                existing["notes"],
                cid,
            ),
        )
        await self._conn.commit()
        return await self.get_citation(cid)

    async def delete_citation(self, cid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_citation(cid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM citations WHERE id=?", (cid,))
        await self._conn.commit()
        return existing

    # ── Collaboration Messages ────────────────────────────────────────────

    async def list_collab_messages(self, study_id: str) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM collab_messages WHERE study_id=? ORDER BY pinned DESC, created_at ASC",
            (study_id,),
        )
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def create_collab_message(
        self,
        *,
        study_id: str,
        author: str = "",
        message: str,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        mid = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO collab_messages (id,study_id,author,message,pinned,created_at)
               VALUES (?,?,?,?,0,?)""",
            (mid, study_id, author, message, created_at),
        )
        await self._conn.commit()
        return await self.get_collab_message(mid)  # type: ignore[return-value]

    async def get_collab_message(self, mid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM collab_messages WHERE id=?", (mid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def update_collab_message(
        self, mid: str, *, pinned: int | None = None, message: str | None = None, author: str | None = None  # noqa: E501
    ) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_collab_message(mid)
        if existing is None:
            return None
        next_pinned  = pinned  if pinned  is not None else existing["pinned"]
        next_message = message if message is not None else existing["message"]
        next_author  = author  if author  is not None else existing["author"]
        await self._conn.execute(
            "UPDATE collab_messages SET pinned=?,message=?,author=? WHERE id=?",
            (next_pinned, next_message, next_author, mid),
        )
        await self._conn.commit()
        return await self.get_collab_message(mid)

    async def delete_collab_message(self, mid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_collab_message(mid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM collab_messages WHERE id=?", (mid,))
        await self._conn.commit()
        return existing

    # ── Helpers ──────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(row: aiosqlite.Row) -> dict[str, Any]:
        d = dict(row)
        # Deserialise JSON columns — use try/except so plain-text fields
        # (e.g. notebooks.content = markdown) pass through unchanged.
        for field in (
            "params",
            "content",
            "symbol_set",
            "metadata",
            "data",
            "evidence",
            "study_ids",
            "exp_ids",
            "tags",
        ):
            if field in d and isinstance(d[field], str):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, ValueError):
                    pass  # plain-text field — keep as-is
        # graph_json → graph (studies)
        if "graph_json" in d and isinstance(d["graph_json"], str):
            d["graph"] = json.loads(d["graph_json"])
            del d["graph_json"]
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
