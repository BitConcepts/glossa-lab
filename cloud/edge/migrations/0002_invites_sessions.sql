-- Spec 083 Step 1 (T010): invites + sessions.
--
-- HASH ONLY, in both tables: an invite code (>=128-bit CSPRNG, FR-002)
-- and a session token (>=256-bit opaque, FR-004) are stored exclusively
-- as SHA-256 hashes. No plaintext code or token column exists anywhere
-- in this schema, so the identity database alone yields no credential.

CREATE TABLE invites (
  id               TEXT PRIMARY KEY,
  code_hash        TEXT NOT NULL UNIQUE,
  created_by       TEXT NOT NULL REFERENCES users (id),
  -- Optional email binding (FR-002 / D-2): when set, only that email's
  -- redemption is accepted (enforced in Phase 2, T014).
  email            TEXT,
  -- JSON object: { "<workspace_id>": "<role>", ... } — the grants that
  -- become the redeeming user's initial workspace_roles rows.
  workspace_grants TEXT NOT NULL DEFAULT '{}',
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  revoked_at       TEXT,
  redeemed_by      TEXT REFERENCES users (id),
  redeemed_at      TEXT
);

CREATE INDEX idx_invites_created_by ON invites (created_by);

CREATE TABLE sessions (
  id           TEXT PRIMARY KEY,
  token_hash   TEXT NOT NULL UNIQUE,
  user_id      TEXT NOT NULL REFERENCES users (id),
  created_at   TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  expires_at   TEXT NOT NULL,
  revoked_at   TEXT
);

CREATE INDEX idx_sessions_user ON sessions (user_id);
CREATE INDEX idx_sessions_expires ON sessions (expires_at);
