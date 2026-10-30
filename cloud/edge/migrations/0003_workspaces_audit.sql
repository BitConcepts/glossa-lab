-- Spec 083 Step 1 (T010): workspaces, per-workspace roles, audit log.
--
-- The workspace is the tenancy unit (Amendment 1, FR-015..FR-017): the
-- existing Program/projects entity, carried at the edge as the identity
-- side of the scope boundary. workspace_roles is read by the edge on
-- every authenticated request and injected as X-Glossa-Workspace-Roles;
-- the container API remains the enforcement point for workspace scope.

CREATE TABLE workspaces (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  slug        TEXT NOT NULL UNIQUE,
  -- An archived workspace serves nothing (FR-016).
  archived_at TEXT,
  created_by  TEXT NOT NULL REFERENCES users (id),
  created_at  TEXT NOT NULL
);

CREATE TABLE workspace_roles (
  user_id      TEXT NOT NULL REFERENCES users (id),
  workspace_id TEXT NOT NULL REFERENCES workspaces (id),
  role         TEXT NOT NULL
               CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
  granted_by   TEXT REFERENCES users (id),
  granted_at   TEXT NOT NULL,
  PRIMARY KEY (user_id, workspace_id)
);

CREATE INDEX idx_workspace_roles_workspace ON workspace_roles (workspace_id);

-- audit_log: APPEND-ONLY (FR-012, C083-12). No code path in any phase
-- issues UPDATE or DELETE against this table — the only writes are
-- INSERTs — and the triggers below make that structural rather than
-- conventional: even a future bug cannot rewrite history through D1.
CREATE TABLE audit_log (
  id          TEXT PRIMARY KEY,
  ts          TEXT NOT NULL,
  actor_id    TEXT REFERENCES users (id),
  -- Human-readable actor snapshot (username at event time), so the log
  -- stays legible after an account is removed.
  actor_label TEXT NOT NULL,
  event       TEXT NOT NULL,
  target      TEXT,
  detail      TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_audit_log_ts ON audit_log (ts);
CREATE INDEX idx_audit_log_actor ON audit_log (actor_id);
CREATE INDEX idx_audit_log_event ON audit_log (event);

CREATE TRIGGER audit_log_no_update
BEFORE UPDATE ON audit_log
BEGIN
  SELECT RAISE(ABORT, 'audit_log is append-only');
END;

CREATE TRIGGER audit_log_no_delete
BEFORE DELETE ON audit_log
BEGIN
  SELECT RAISE(ABORT, 'audit_log is append-only');
END;
