-- Spec 083 Step 2 (T015/T017): setup seed record + case-insensitive
-- username uniqueness.
--
-- setup_state gains the seed record the operator seed step writes
-- (scripts/seed-setup.mjs): the username and contact email of the
-- account /setup will create. The setup handler reads the username
-- and email ONLY from this record — they are never free input on the
-- setup request (Amendment 3 fixes the seed values; the seed step
-- writes them, this migration only adds the columns).
ALTER TABLE setup_state ADD COLUMN username TEXT;
ALTER TABLE setup_state ADD COLUMN email TEXT;

-- Username uniqueness is case-insensitive (T015): the base table's
-- UNIQUE is case-sensitive in SQLite, so a functional unique index
-- over lower(username) is the structural guarantee; the handlers
-- also normalize to lowercase before insert.
CREATE UNIQUE INDEX idx_users_username_lower ON users (lower(username));
