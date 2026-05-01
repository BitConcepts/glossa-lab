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
_SCHEMA_VERSION = 13

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

_SCHEMA_V6 = """
ALTER TABLE texts ADD COLUMN reading_direction TEXT NOT NULL DEFAULT 'unknown';
"""

_SCHEMA_V7 = """
CREATE TABLE IF NOT EXISTS report_templates (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category    TEXT NOT NULL DEFAULT 'General',
    sections    TEXT NOT NULL DEFAULT '[]',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

_SCHEMA_V8 = """
CREATE TABLE IF NOT EXISTS anchor_sets (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    corpus_id   TEXT,
    language    TEXT NOT NULL DEFAULT '',
    pairs       TEXT NOT NULL DEFAULT '[]',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

_SCHEMA_V9 = """
CREATE TABLE IF NOT EXISTS corpus_catalogue (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    language        TEXT NOT NULL DEFAULT '',
    language_family TEXT NOT NULL DEFAULT '',
    script_type     TEXT NOT NULL DEFAULT '',
    period          TEXT NOT NULL DEFAULT '',
    tokens_approx   INTEGER NOT NULL DEFAULT 0,
    source_url      TEXT NOT NULL DEFAULT '',
    license         TEXT NOT NULL DEFAULT '',
    description     TEXT NOT NULL DEFAULT '',
    local_module    TEXT NOT NULL DEFAULT '',
    is_undeciphered INTEGER NOT NULL DEFAULT 0
);
"""

_SCHEMA_V11 = """
ALTER TABLE corpus_catalogue ADD COLUMN reading_direction TEXT NOT NULL DEFAULT 'unknown';
"""

_SCHEMA_V10 = """
CREATE TABLE IF NOT EXISTS cas_models (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    yaml_text   TEXT NOT NULL DEFAULT '',
    engine_hint TEXT NOT NULL DEFAULT 'auto',
    is_builtin  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

_SCHEMA_V13 = """
CREATE TABLE IF NOT EXISTS discovery_items (
    id            TEXT PRIMARY KEY,
    title         TEXT NOT NULL DEFAULT '',
    url           TEXT NOT NULL DEFAULT '',
    source        TEXT NOT NULL DEFAULT '',
    topic         TEXT NOT NULL DEFAULT '',
    published_at  TEXT NOT NULL DEFAULT '',
    fetched_at    TEXT NOT NULL,
    lang          TEXT NOT NULL DEFAULT '',
    raw_json      TEXT NOT NULL DEFAULT '{}',
    summary       TEXT NOT NULL DEFAULT '',
    kind          TEXT NOT NULL DEFAULT 'other',
    confidence    REAL NOT NULL DEFAULT 0.0,
    links         TEXT NOT NULL DEFAULT '[]',
    status        TEXT NOT NULL DEFAULT 'new',
    notes         TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_discovery_topic_fetched
    ON discovery_items(topic, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_discovery_status_fetched
    ON discovery_items(status, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_discovery_kind_fetched
    ON discovery_items(kind, fetched_at DESC);
"""

_SCHEMA_V12 = """
CREATE TABLE IF NOT EXISTS canonical_signs (
    internal_id        TEXT PRIMARY KEY,
    sign_id            TEXT NOT NULL,
    numbering_system   TEXT NOT NULL DEFAULT 'parpola_1982',
    description        TEXT NOT NULL DEFAULT '',
    wells_ids          TEXT NOT NULL DEFAULT '',
    mahadevan_ids      TEXT NOT NULL DEFAULT '',
    parpola_allographs TEXT NOT NULL DEFAULT '',
    icit_function      TEXT NOT NULL DEFAULT '',
    corpus_freq        INTEGER NOT NULL DEFAULT 0,
    start_rate         REAL NOT NULL DEFAULT 0.0,
    end_rate           REAL NOT NULL DEFAULT 0.0,
    internal_rate      REAL NOT NULL DEFAULT 0.0,
    in_corpus          INTEGER NOT NULL DEFAULT 0,
    n_feature_dims     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sign_cluster_assignments (
    id             TEXT PRIMARY KEY,
    sign_id        TEXT NOT NULL,
    cluster_label  INTEGER NOT NULL,
    cluster_k      INTEGER NOT NULL DEFAULT 40,
    method         TEXT NOT NULL DEFAULT 'hierarchical_ward',
    silhouette     REAL NOT NULL DEFAULT 0.0,
    dominant_pos   TEXT NOT NULL DEFAULT '',
    created_at     TEXT NOT NULL
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
            current_version = 5

        if current_version < 6:
            # ALTER TABLE is not transactional in SQLite but is safe here
            try:
                await self._conn.execute(
                    "ALTER TABLE texts ADD COLUMN reading_direction TEXT NOT NULL DEFAULT 'unknown'"
                )
            except Exception:  # noqa: BLE001
                pass  # Column already exists (idempotent)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (6,))

        if current_version < 7:
            await self._conn.executescript(_SCHEMA_V7)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (7,))
            current_version = 7

        if current_version < 8:
            await self._conn.executescript(_SCHEMA_V8)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (8,))
            current_version = 8

        if current_version < 9:
            await self._conn.executescript(_SCHEMA_V9)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (9,))
            current_version = 9

        if current_version < 10:
            await self._conn.executescript(_SCHEMA_V10)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (10,))
            current_version = 10

        if current_version < 11:
            try:
                await self._conn.execute(
                    "ALTER TABLE corpus_catalogue ADD COLUMN reading_direction TEXT NOT NULL DEFAULT 'unknown'"
                )
            except Exception:  # noqa: BLE001
                pass  # column already exists
            await self._conn.execute("UPDATE _schema_version SET version = ?", (11,))
            current_version = 11

        if current_version < 12:
            await self._conn.executescript(_SCHEMA_V12)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (12,))
            current_version = 12

        if current_version < 13:
            await self._conn.executescript(_SCHEMA_V13)
            await self._conn.execute("UPDATE _schema_version SET version = ?", (13,))
            current_version = 13

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
        initial_status: str = "pending",
    ) -> dict[str, Any]:
        assert self._conn
        job_id = uuid.uuid4().hex[:12]
        params_json = json.dumps(params or {})
        safe_status = initial_status if initial_status in (
            "pending", "running", "completed", "failed", "cancelled"
        ) else "pending"
        await self._conn.execute(
            """INSERT INTO jobs (id, name, pipeline, status, params, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (job_id, name, pipeline, safe_status, params_json, created_at, created_at),
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
        reading_direction: str = "unknown",
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        text_id = uuid.uuid4().hex[:12]
        symbol_set = sorted(set(content))
        alphabet_size = len(symbol_set)
        safe_dir = reading_direction if reading_direction in ("ltr", "rtl", "unknown") else "unknown"
        await self._conn.execute(
            """INSERT INTO texts
               (id, name, corpus_type, content, alphabet_size,
                symbol_set, metadata, reading_direction, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                text_id,
                name,
                corpus_type,
                json.dumps(content),
                alphabet_size,
                json.dumps(symbol_set),
                json.dumps(metadata or {}),
                safe_dir,
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
        reading_direction: str | None = None,
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
        raw_dir = reading_direction if reading_direction is not None else existing.get("reading_direction", "unknown")
        next_direction = raw_dir if raw_dir in ("ltr", "rtl", "unknown") else "unknown"

        await self._conn.execute(
            """UPDATE texts
               SET name = ?, corpus_type = ?, content = ?, alphabet_size = ?,
                   symbol_set = ?, metadata = ?, reading_direction = ?
               WHERE id = ?""",
            (
                next_name,
                next_corpus_type,
                json.dumps(next_content),
                next_alphabet_size,
                json.dumps(next_symbol_set),
                json.dumps(next_metadata),
                next_direction,
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

    # ── Report Templates (V7) ────────────────────────────────────────────

    async def list_report_templates(self) -> list[dict[str, Any]]:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM report_templates ORDER BY name ASC")
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_report_template(self, tid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM report_templates WHERE id=?", (tid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def create_report_template(
        self,
        *,
        name: str,
        description: str = "",
        category: str = "General",
        sections: list[dict] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        tid = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO report_templates (id,name,description,category,sections,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?)""",
            (tid, name, description, category, json.dumps(sections or []), created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_report_template(tid)  # type: ignore[return-value]

    async def update_report_template(self, tid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_report_template(tid)
        if existing is None:
            return None
        name = fields.get("name", existing["name"])
        description = fields.get("description", existing["description"])
        category = fields.get("category", existing["category"])
        sections = json.dumps(fields["sections"]) if "sections" in fields else json.dumps(existing["sections"])
        await self._conn.execute(
            """UPDATE report_templates SET name=?,description=?,category=?,sections=?,
               updated_at=datetime('now') WHERE id=?""",
            (name, description, category, sections, tid),
        )
        await self._conn.commit()
        return await self.get_report_template(tid)

    async def delete_report_template(self, tid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_report_template(tid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM report_templates WHERE id=?", (tid,))
        await self._conn.commit()
        return existing

    # ── Anchor Sets (V8) ─────────────────────────────────────────────────

    async def list_anchor_sets(self, corpus_id: str | None = None) -> list[dict[str, Any]]:
        assert self._conn
        if corpus_id:
            cursor = await self._conn.execute(
                "SELECT * FROM anchor_sets WHERE corpus_id=? ORDER BY name ASC", (corpus_id,)
            )
        else:
            cursor = await self._conn.execute("SELECT * FROM anchor_sets ORDER BY name ASC")
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_anchor_set(self, aid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM anchor_sets WHERE id=?", (aid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def create_anchor_set(
        self,
        *,
        name: str,
        description: str = "",
        corpus_id: str | None = None,
        language: str = "",
        pairs: list[dict] | None = None,
        created_at: str,
    ) -> dict[str, Any]:
        assert self._conn
        aid = uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT INTO anchor_sets (id,name,description,corpus_id,language,pairs,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (aid, name, description, corpus_id, language, json.dumps(pairs or []), created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_anchor_set(aid)  # type: ignore[return-value]

    async def update_anchor_set(self, aid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_anchor_set(aid)
        if existing is None:
            return None
        name = fields.get("name", existing["name"])
        description = fields.get("description", existing["description"])
        corpus_id = fields.get("corpus_id", existing.get("corpus_id"))
        language = fields.get("language", existing["language"])
        pairs = json.dumps(fields["pairs"]) if "pairs" in fields else json.dumps(existing["pairs"])
        await self._conn.execute(
            """UPDATE anchor_sets SET name=?,description=?,corpus_id=?,language=?,pairs=?,
               updated_at=datetime('now') WHERE id=?""",
            (name, description, corpus_id, language, pairs, aid),
        )
        await self._conn.commit()
        return await self.get_anchor_set(aid)

    async def delete_anchor_set(self, aid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_anchor_set(aid)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM anchor_sets WHERE id=?", (aid,))
        await self._conn.commit()
        return existing

    # ── Corpus Catalogue (V9) ─────────────────────────────────────────────

    async def list_corpus_catalogue(
        self,
        script_type: str | None = None,
        is_undeciphered: bool | None = None,
    ) -> list[dict[str, Any]]:
        assert self._conn
        q = "SELECT * FROM corpus_catalogue WHERE 1=1"
        args: list = []
        if script_type:
            q += " AND script_type=?"; args.append(script_type)
        if is_undeciphered is not None:
            q += " AND is_undeciphered=?"; args.append(1 if is_undeciphered else 0)
        q += " ORDER BY language_family ASC, name ASC"
        cursor = await self._conn.execute(q, args)
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_corpus_catalogue_entry(self, cid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM corpus_catalogue WHERE id=?", (cid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def upsert_corpus_catalogue_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Insert or replace a catalogue entry (used by the seeder)."""
        assert self._conn
        await self._conn.execute(
            """INSERT OR REPLACE INTO corpus_catalogue
               (id,name,language,language_family,script_type,period,
                tokens_approx,source_url,license,description,local_module,is_undeciphered,reading_direction)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                entry["id"], entry["name"], entry.get("language", ""),
                entry.get("language_family", ""), entry.get("script_type", ""),
                entry.get("period", ""), entry.get("tokens_approx", 0),
                entry.get("source_url", ""), entry.get("license", ""),
                entry.get("description", ""), entry.get("local_module", ""),
                1 if entry.get("is_undeciphered") else 0,
                entry.get("reading_direction", "unknown"),
            ),
        )
        await self._conn.commit()
        return await self.get_corpus_catalogue_entry(entry["id"])  # type: ignore[return-value]

    # ── CAS Models (V10) ─────────────────────────────────────────────

    async def list_cas_models(self, builtin_only: bool = False) -> list[dict[str, Any]]:
        assert self._conn
        q = "SELECT * FROM cas_models"
        if builtin_only:
            q += " WHERE is_builtin=1"
        q += " ORDER BY name ASC"
        cursor = await self._conn.execute(q)
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_cas_model(self, mid: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute("SELECT * FROM cas_models WHERE id=?", (mid,))
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def create_cas_model(
        self,
        *,
        name: str,
        description: str = "",
        yaml_text: str = "",
        engine_hint: str = "auto",
        is_builtin: bool = False,
        created_at: str,
        model_id: str | None = None,
    ) -> dict[str, Any]:
        assert self._conn
        mid = model_id or uuid.uuid4().hex[:12]
        await self._conn.execute(
            """INSERT OR REPLACE INTO cas_models
               (id,name,description,yaml_text,engine_hint,is_builtin,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (mid, name, description, yaml_text, engine_hint,
             1 if is_builtin else 0, created_at, created_at),
        )
        await self._conn.commit()
        return await self.get_cas_model(mid)  # type: ignore[return-value]

    async def update_cas_model(self, mid: str, **fields: Any) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_cas_model(mid)
        if existing is None:
            return None
        name        = fields.get("name",        existing["name"])
        description = fields.get("description", existing["description"])
        yaml_text   = fields.get("yaml_text",   existing["yaml_text"])
        engine_hint = fields.get("engine_hint", existing["engine_hint"])
        await self._conn.execute(
            """UPDATE cas_models SET name=?,description=?,yaml_text=?,engine_hint=?,
               updated_at=datetime('now') WHERE id=?""",
            (name, description, yaml_text, engine_hint, mid),
        )
        await self._conn.commit()
        return await self.get_cas_model(mid)

    async def delete_cas_model(self, mid: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_cas_model(mid)
        if existing is None:
            return None
        if existing.get("is_builtin"):
            return None  # protect built-in models
        await self._conn.execute("DELETE FROM cas_models WHERE id=?", (mid,))
        await self._conn.commit()
        return existing

    # ── Canonical Sign Registry (V12) ────────────────────────────────────

    async def seed_canonical_signs(self, signs: list[dict[str, Any]]) -> int:
        """Bulk-insert canonical signs from the CGSA pipeline output."""
        assert self._conn
        await self._conn.execute("DELETE FROM canonical_signs")
        for s in signs:
            await self._conn.execute(
                """INSERT OR REPLACE INTO canonical_signs
                   (internal_id,sign_id,numbering_system,description,wells_ids,mahadevan_ids,
                    parpola_allographs,icit_function,corpus_freq,start_rate,end_rate,internal_rate,
                    in_corpus,n_feature_dims)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    s["internal_id"], s["sign_id"], s.get("numbering_system", "parpola_1982"),
                    s.get("description", ""), s.get("wells_ids", ""), s.get("mahadevan_ids", ""),
                    s.get("parpola_allographs", ""), s.get("icit_function", ""),
                    int(s.get("corpus_freq", 0)), float(s.get("start_rate", 0)),
                    float(s.get("end_rate", 0)), float(s.get("internal_rate", 0)),
                    1 if s.get("in_corpus") else 0, int(s.get("n_feature_dims", 0)),
                )
            )
        await self._conn.commit()
        return len(signs)

    async def list_canonical_signs(
        self,
        in_corpus_only: bool = False,
        numbering_system: str | None = None,
    ) -> list[dict[str, Any]]:
        assert self._conn
        q = "SELECT * FROM canonical_signs WHERE 1=1"
        args: list = []
        if in_corpus_only:
            q += " AND in_corpus=1"
        if numbering_system:
            q += " AND numbering_system=?"; args.append(numbering_system)
        q += " ORDER BY sign_id ASC"
        cursor = await self._conn.execute(q, args)
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_canonical_sign(self, sign_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM canonical_signs WHERE sign_id=? OR internal_id=? LIMIT 1",
            (sign_id, sign_id)
        )
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def seed_cluster_assignments(
        self, assignments: list[dict[str, Any]], created_at: str
    ) -> int:
        """Bulk-insert cluster assignments from the CGSA pipeline."""
        assert self._conn
        await self._conn.execute("DELETE FROM sign_cluster_assignments")
        for a in assignments:
            aid = uuid.uuid4().hex[:12]
            await self._conn.execute(
                """INSERT INTO sign_cluster_assignments
                   (id,sign_id,cluster_label,cluster_k,method,silhouette,dominant_pos,created_at)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (
                    aid, a["sign_id"], int(a["cluster_label"]),
                    int(a.get("cluster_k", 40)), a.get("method", "hierarchical_ward"),
                    float(a.get("silhouette", 0)), a.get("dominant_pos", ""), created_at,
                )
            )
        await self._conn.commit()
        return len(assignments)

    async def list_cluster_assignments(
        self, cluster_k: int | None = None
    ) -> list[dict[str, Any]]:
        assert self._conn
        q = "SELECT * FROM sign_cluster_assignments WHERE 1=1"
        args: list = []
        if cluster_k:
            q += " AND cluster_k=?"; args.append(cluster_k)
        q += " ORDER BY cluster_label ASC, sign_id ASC"
        cursor = await self._conn.execute(q, args)
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def get_clusters_summary(self) -> dict[str, Any]:
        """Return cluster count, k value, and top cluster sizes."""
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT cluster_k, COUNT(DISTINCT cluster_label) as n_clusters, "
            "COUNT(*) as n_signs FROM sign_cluster_assignments LIMIT 1"
        )
        row = await cursor.fetchone()
        if not row:
            return {"n_clusters": 0, "cluster_k": 0, "n_signs": 0}
        return dict(row)

    # ── Discovery Items (V13) ────────────────────────────────────────────

    async def upsert_discovery_item(
        self,
        *,
        item_id: str,
        title: str,
        url: str,
        source: str,
        topic: str,
        published_at: str,
        fetched_at: str,
        lang: str = "",
        raw: dict[str, Any] | None = None,
    ) -> bool:
        """Insert a new item, or merge ``topic`` if the id already exists.

        Returns True if a new row was created, False if the existing row was
        only updated (topic-merge / latest-fetched_at).

        The insert path uses ``INSERT OR IGNORE`` so concurrent fetchers cannot
        race on the check-then-insert pattern — SQLite resolves the conflict
        atomically and the caller falls through to the merge path on collision.
        """
        assert self._conn
        cursor = await self._conn.execute(
            """INSERT OR IGNORE INTO discovery_items
               (id,title,url,source,topic,published_at,fetched_at,lang,raw_json)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                item_id, title, url, source, topic, published_at,
                fetched_at, lang, json.dumps(raw or {}),
            ),
        )
        if cursor.rowcount == 1:
            await self._conn.commit()
            return True
        # Existing row — read its current topic CSV so we can merge with set
        # semantics (and a stable sort order) and bump fetched_at.
        sel = await self._conn.execute(
            "SELECT topic FROM discovery_items WHERE id=?", (item_id,)
        )
        row = await sel.fetchone()
        existing_topics = (
            {t for t in (row["topic"] or "").split(",") if t} if row else set()
        )
        new_topics = {t for t in (topic or "").split(",") if t}
        merged = ",".join(sorted(existing_topics | new_topics))
        await self._conn.execute(
            "UPDATE discovery_items SET topic=?, fetched_at=? WHERE id=?",
            (merged, fetched_at, item_id),
        )
        await self._conn.commit()
        return False

    async def update_discovery_classification(
        self,
        item_id: str,
        *,
        kind: str,
        confidence: float,
        summary: str,
        links: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        assert self._conn
        await self._conn.execute(
            """UPDATE discovery_items
               SET kind=?, confidence=?, summary=?, links=?
               WHERE id=?""",
            (kind, float(confidence), summary, json.dumps(links or []), item_id),
        )
        await self._conn.commit()
        return await self.get_discovery_item(item_id)

    async def update_discovery_status(
        self,
        item_id: str,
        *,
        status: str,
        notes: str | None = None,
    ) -> dict[str, Any] | None:
        assert self._conn
        safe_status = status if status in ("new", "reviewed", "dismissed", "saved") else "new"
        if notes is None:
            await self._conn.execute(
                "UPDATE discovery_items SET status=? WHERE id=?",
                (safe_status, item_id),
            )
        else:
            await self._conn.execute(
                "UPDATE discovery_items SET status=?, notes=? WHERE id=?",
                (safe_status, notes, item_id),
            )
        await self._conn.commit()
        return await self.get_discovery_item(item_id)

    async def get_discovery_item(self, item_id: str) -> dict[str, Any] | None:
        assert self._conn
        cursor = await self._conn.execute(
            "SELECT * FROM discovery_items WHERE id=?", (item_id,)
        )
        row = await cursor.fetchone()
        return self._row_to_dict(row) if row else None

    async def list_discovery_items(
        self,
        *,
        topic: str | None = None,
        kind: str | None = None,
        status: str | None = None,
        since: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        assert self._conn
        q = "SELECT * FROM discovery_items WHERE 1=1"
        args: list[Any] = []
        if topic:
            # CSV match — items whose topic column contains this id
            q += " AND (',' || topic || ',') LIKE ?"
            args.append(f"%,{topic},%")
        if kind:
            q += " AND kind=?"
            args.append(kind)
        if status:
            q += " AND status=?"
            args.append(status)
        if since:
            q += " AND fetched_at >= ?"
            args.append(since)
        q += " ORDER BY fetched_at DESC LIMIT ? OFFSET ?"
        args.extend([int(limit), int(offset)])
        cursor = await self._conn.execute(q, args)
        return [self._row_to_dict(r) for r in await cursor.fetchall()]

    async def count_discovery_by(
        self,
        *,
        group: str = "status",
    ) -> dict[str, int]:
        """Group counts by one of: status, kind, topic, source."""
        assert self._conn
        if group not in ("status", "kind", "topic", "source"):
            return {}
        cursor = await self._conn.execute(
            f"SELECT {group} AS g, COUNT(*) AS cnt FROM discovery_items GROUP BY {group}"
        )
        rows = await cursor.fetchall()
        return {(r["g"] or ""): int(r["cnt"]) for r in rows}

    async def delete_discovery_item(self, item_id: str) -> dict[str, Any] | None:
        assert self._conn
        existing = await self.get_discovery_item(item_id)
        if existing is None:
            return None
        await self._conn.execute("DELETE FROM discovery_items WHERE id=?", (item_id,))
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
            "sections",   # report_templates
            "pairs",      # anchor_sets
            "raw_json",   # discovery_items
            "links",      # discovery_items
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
