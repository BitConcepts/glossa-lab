-- Spec 083 Step 1 (T010): D1 identity schema — core tables.
--
-- Identity lives in D1 at the edge so authentication never depends on
-- the container being awake (plan Step 1). All timestamps are ISO-8601
-- UTC text. Secrets are stored ONLY as hashes: password_hash holds the
-- Argon2id hash produced at setup/registration (Phase 2); the setup
-- code is stored only as a SHA-256 hash.

CREATE TABLE users (
  id            TEXT PRIMARY KEY,
  username      TEXT NOT NULL UNIQUE,
  email         TEXT,
  password_hash TEXT NOT NULL,
  -- Global user type (Amendment 1): owner is singular (the glassbreak
  -- account); guests are capped at Viewer in every workspace.
  global_type   TEXT NOT NULL DEFAULT 'member'
                CHECK (global_type IN ('owner', 'admin', 'member', 'guest')),
  -- Removal is expressed by removed_at (attribution on past work is
  -- preserved, FR via Story 4); status carries the live disable flag.
  status        TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'disabled')),
  created_at    TEXT NOT NULL,
  removed_at    TEXT
);

CREATE INDEX idx_users_status ON users (status);

-- setup_state: exactly one row (id is constrained to 'singleton').
-- Holds the glassbreak first-run setup state (FR-003): while
-- completed_at IS NULL and setup_code_expires_at is in the future, the
-- /setup path may redeem setup_code_hash exactly once; the moment
-- setup completes, completed_at is set and the path closes forever.
CREATE TABLE setup_state (
  id                    TEXT PRIMARY KEY CHECK (id = 'singleton'),
  setup_code_hash       TEXT,
  setup_code_expires_at TEXT,
  completed_at          TEXT
);

INSERT INTO setup_state (id) VALUES ('singleton');
