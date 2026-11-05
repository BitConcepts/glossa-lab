"""Primary-workspace scope reconciliation (Spec 083, T057).

Amendment 5 makes the desktop-resident dataset the hosted edition's
only dataset. Before go-live, the desktop dataset is reconciled
against the primary workspace (``indus-script`` /
``indus_decipherment``): every resource class is counted, per class,
against the dataset itself, and the check FAILS LOUDLY on any
unscoped or misassigned resource in a class the data model scopes
by project.

Class treatment is honest about the data model (the T019 coverage
table in ``glossa_lab/cloud_scope.py`` is the authority):

* **Scoped classes** — tables carrying a ``project_id`` column
  (notebooks, hypotheses, citations, correspondences, and any table
  that gains one): every row must name an existing project.
  ``project_id = ''`` is UNSCOPED and a non-empty id naming no
  project is MISASSIGNED (dangling); both are violations.
* **Experiments** — no experiments table exists; projects link
  experiments by id (``projects.experiment_ids``). The linkage is
  reported (ids linked, per project); there is no row set to audit.
* **Global classes** — tables with no project linkage (studies,
  jobs, anchor_sets, texts, discovery_items, research_loop_state,
  reports data, ...): counted and NAMED as global class, never
  silently passed. They gain true scope when their records gain a
  project linkage (the standing model gap, recorded at T019).
* **Evidence store** — claims/digestion/evidence live in the on-disk
  store owned by the primary program (Spec 081 ``_program_scope``
  semantics: ``_STORE_PROGRAM_ID`` in ``api/indus_evidence.py``).
  The check verifies the installed source still names the primary
  project as the store owner, consistent with the database.

The check is read-only: it opens the SQLite database with a
read-only URI and never writes. It runs against a data directory
(``glossa.db`` inside it) — on the desktop, in place; the dataset is
never copied anywhere for this check.
"""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

PRIMARY_PROJECT_ID = "indus_decipherment"
PRIMARY_WORKSPACE_SLUG = "indus-script"

_STORE_OWNER_RE = re.compile(r'_STORE_PROGRAM_ID\s*=\s*"([^"]+)"')

# Internal tables that are neither scoped nor global resource classes.
_INTERNAL_TABLES = {"_schema_version", "sqlite_sequence"}


@dataclass
class ClassLine:
    name: str
    kind: str  # "scoped" | "global" | "linkage" | "store" | "primary"
    detail: str
    violations: int = 0


@dataclass
class Report:
    lines: list[ClassLine] = field(default_factory=list)

    @property
    def violations(self) -> int:
        return sum(line.violations for line in self.lines)

    @property
    def verdict(self) -> str:
        return "PASS" if self.violations == 0 else "FAIL"

    def render(self) -> str:
        out = ["WORKSPACE-SCOPE RECONCILIATION (Spec 083 T057)"]
        out.extend(f"{line.kind.upper():8} {line.name}: {line.detail}" for line in self.lines)
        out.append(f"VERDICT: {self.verdict} violations={self.violations}")
        return "\n".join(out)


def _table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return [r[0] for r in rows if r[0] not in _INTERNAL_TABLES]


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def _count(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> int:
    return int(conn.execute(sql, params).fetchone()[0])


def check_database(db_path: Path) -> list[ClassLine]:
    """Per-class counts against the dataset at ``db_path`` (read-only)."""
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        lines: list[ClassLine] = []
        tables = _table_names(conn)

        # ── Primary workspace presence ──────────────────────────────
        project_ids: set[str] = set()
        if "projects" in tables:
            project_ids = {
                r[0] for r in conn.execute("SELECT id FROM projects").fetchall()
            }
        primary_present = PRIMARY_PROJECT_ID in project_ids
        lines.append(
            ClassLine(
                name="projects",
                kind="primary",
                detail=(
                    f"workspaces={len(project_ids)} "
                    f"primary[{PRIMARY_PROJECT_ID}] "
                    f"present={'yes' if primary_present else 'NO'}"
                ),
                violations=0 if primary_present else 1,
            )
        )

        # ── Scoped + global classes ─────────────────────────────────
        for table in tables:
            if table == "projects":
                continue
            columns = _columns(conn, table)
            total = _count(conn, f"SELECT COUNT(*) FROM {table}")
            if "project_id" not in columns:
                lines.append(
                    ClassLine(
                        name=table,
                        kind="global",
                        detail=f"count={total} (no project linkage in the model)",
                    )
                )
                continue
            primary = _count(
                conn,
                f"SELECT COUNT(*) FROM {table} WHERE project_id = ?",
                (PRIMARY_PROJECT_ID,),
            )
            unscoped = _count(
                conn,
                f"SELECT COUNT(*) FROM {table} "
                "WHERE project_id IS NULL OR project_id = ''",
            )
            dangling = 0
            scoped_other = 0
            for (pid,) in conn.execute(
                f"SELECT DISTINCT project_id FROM {table} "
                "WHERE project_id IS NOT NULL AND project_id != ''"
            ).fetchall():
                n = _count(
                    conn,
                    f"SELECT COUNT(*) FROM {table} WHERE project_id = ?",
                    (pid,),
                )
                if pid in project_ids:
                    if pid != PRIMARY_PROJECT_ID:
                        scoped_other += n
                else:
                    dangling += n
            violations = unscoped + dangling
            lines.append(
                ClassLine(
                    name=table,
                    kind="scoped",
                    detail=(
                        f"total={total} primary={primary} "
                        f"other-workspace={scoped_other} "
                        f"unscoped={unscoped} misassigned={dangling}"
                    ),
                    violations=violations,
                )
            )

        # ── Experiments linkage (no experiments table exists) ───────
        linked: set[str] = set()
        linking_projects = 0
        if "projects" in tables:
            for (raw,) in conn.execute(
                "SELECT experiment_ids FROM projects"
            ).fetchall():
                try:
                    ids = json.loads(raw or "[]")
                except (TypeError, ValueError):
                    ids = []
                if ids:
                    linking_projects += 1
                    linked.update(str(i) for i in ids)
        lines.append(
            ClassLine(
                name="experiments",
                kind="linkage",
                detail=(
                    f"linked_ids={len(linked)} "
                    f"projects_linking={linking_projects} "
                    "(projects link experiments by id; no row set to audit)"
                ),
            )
        )
        return lines
    finally:
        conn.close()


def check_store_ownership(repo_root: Path) -> ClassLine:
    """The on-disk evidence store must belong to the primary program."""
    source = repo_root / "backend" / "glossa_lab" / "api" / "indus_evidence.py"
    if not source.exists():
        return ClassLine(
            name="evidence-store",
            kind="store",
            detail=f"UNVERIFIABLE: {source} not found",
            violations=1,
        )
    match = _STORE_OWNER_RE.search(source.read_text(encoding="utf-8"))
    owner = match.group(1) if match else None
    consistent = owner == PRIMARY_PROJECT_ID
    return ClassLine(
        name="evidence-store",
        kind="store",
        detail=(
            f"owner={owner!r} primary={PRIMARY_PROJECT_ID!r} "
            f"consistent={'yes' if consistent else 'NO'} "
            "(claims/digestion/evidence store, Spec 081 _program_scope)"
        ),
        violations=0 if consistent else 1,
    )


def run_check(data_dir: Path, repo_root: Path) -> Report:
    """Full T057 reconciliation for one desktop install."""
    report = Report()
    db_path = data_dir / "glossa.db"
    if not db_path.exists():
        report.lines.append(
            ClassLine(
                name="database",
                kind="primary",
                detail=f"MISSING: {db_path} not found",
                violations=1,
            )
        )
    else:
        report.lines.extend(check_database(db_path))
    report.lines.append(check_store_ownership(repo_root))
    return report
