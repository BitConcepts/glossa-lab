# Spec 092 — Stage 2 record (2026-11-16)

Stage 2 (T201, T202, T203) of `specs/092-platform-hardening-r4/`. Branch
`spec/092-s2-verified-write` (the commissioning brief's name; the tasks.md
stage header says `feat/092-s2-verified-write` — the brief governed, noted
here as a deviation). Built and tested on the mini-server, the program's
execution home since 2026-11-16, in a fresh full clone at HEAD `d94197cc`
(= origin/main, the PR #571 merge), clean tree. The worker did not merge;
CI job conclusions are the parent's gate read, not claimed here.

## What was built

### T201 — `backend/glossa_lab/verified_write.py` (new)

The safe-write contract as a library:

- `write_file_verified(path, content, *, mode=None, retries=3)` returns a
  `WriteReceipt(path, sha256, attempts, via)`; `try_write_once` is the
  single-attempt leg; one typed error, `VerifiedWriteError`.
- Construction: temp file created by `mkstemp` in the target's own
  directory; the optional mode is applied to the temp file (`fchmod`)
  BEFORE write and rename, so the target never exists with wrong
  permissions; payload written, flushed, fsync'd; the TEMP file is read
  back and SHA-256-verified BEFORE the rename, so a silently truncated or
  0-byte land is caught while the previous target still stands;
  `os.replace`; best-effort directory fsync; the target is read back and
  SHA-256-verified after the rename.
- Empty content is refused before any attempt. Parent directories are
  never created implicitly — a missing parent is a typed failure and
  nothing is created.
- `VerifiedWriteError` subclasses `atomic_io.StateWriteError`, so the
  settings store's existing asserted error surface is preserved exactly.
- Bounded retry ladder: local attempts first; the fresh-subprocess child
  leg (`python -m glossa_lab.verified_write --child-write`, exit codes
  0/1/3/2) engages ONLY when the local failure carries the write-denial
  signature (EPERM/EACCES, or a read-back hash mismatch). Machine-state
  failures (ENOSPC and friends) exhaust the local ladder and raise: a
  fresh process cannot heal a full disk, and the program's disk-full
  fixtures patch `os.replace` in-process, so a child leg there would
  report a false heal. This refinement is documented in the module
  docstring.
- Provenance: the construction generalizes the verified-write pattern
  proven in the program's own store code in Stage 1.

### T202 — `backend/tests/test_verified_write.py` (new, 18 tests)

Fault cases enumerated:

1. Bytes round-trip with receipt assertions (path, sha256, attempts, via).
2. Str round-trip (UTF-8).
3. POSIX mode applied to the landed file.
4. Empty content refused — new target (nothing created).
5. Empty content refused — existing target (content preserved).
6. Missing parent directory — typed error, nothing created.
7. Parent path is a file — typed error.
8. Temp creation denied (mkstemp EPERM) — typed failure, previous content
   preserved (retries=0).
9. Temp creation denied — healed by the child leg (retries=1).
10. Silent 0-byte land (the fdopen wrapper drops the payload) — typed
    failure, preserved (retries=0).
11. Silent 0-byte land — healed by the child leg (retries=1).
12. Short write — typed failure, previous content preserved.
13. Rename ENOSPC — named in the error, preserved, no temp litter.
14. Rename EPERM — healed by the child leg.
15. Rename lands wrong bytes — detected by the post-rename read-back
    (retries=0); preservation is not asserted against this fault by
    design (the rename itself is the corruption).
16. Rename lands wrong bytes — healed by the child leg (retries=1).
17. `VerifiedWriteError` is a `StateWriteError` (the store's
    error-surface pin).
18. CLI round-trip; CLI missing-parent exits 3 with no traceback.

### T203 — settings save-path refactor + V9 writer census

- `api/settings.py`: Stage 1's in-module `_write_store_verified` is
  deleted; `_save_keys` now creates its own directory (the store owns its
  directory, as in Stage 1; the library never creates parents) and calls
  `write_file_verified(f, json.dumps(out, indent=2), mode=0o600)`; the
  post-write chmod discipline is kept. The store format is untouched: v2
  AES-256-GCM envelopes byte-compatible, non-credential entries
  untouched — proven by Stage 1's 23-test encryption battery passing
  UNCHANGED against the library path, together with the 7 F1 disk-full
  tests (48 targeted tests, all passing).
- Writer census, verified on this tree: `_save_keys` in
  `api/settings.py` is the ONLY function that writes the settings store
  (`.keys.json`). Its 7 call sites, in 5 modules:

  | # | Call site | Path |
  |---|-----------|------|
  | 1 | `settings.py:422` | `_migrate_store` |
  | 2 | `settings.py:929` | `update_settings` (PUT) |
  | 3 | `api/notifications.py:284` | Graph connect |
  | 4 | `api/notifications.py:297` | Graph disconnect |
  | 5 | `discovery/scheduler.py:164` | scheduler toggle |
  | 6 | `study_loop_scheduler.py:163` | scheduler toggle |
  | 7 | `notifications/smtp.py:250` | Graph token-refresh persistence |

  After the refactor, `settings.py` contains no direct write call (no
  `write_text` / `write_bytes` / `os.replace` / `mkstemp`). All 7 call
  sites reach the store through the single `_save_keys` choke point, so
  7 of 7 writers are on the library. Every other `.keys.json` mention in
  production code is a comment, docstring, or privacy text. Readers (not
  writers): `ai_utils.py` and `database.py`, via `_load_keys`.
- V9 census registration (`ledger_gate.py`): `REGISTERED_WRITERS` gains
  `backend/glossa_lab/verified_write.py` and
  `backend/glossa_lab/api/settings.py`. `ARTIFACT_PATH_PATTERNS` was
  deliberately NOT extended with a `.keys.json` pattern: that leg
  requires a write call in the same module, and unrelated modules that
  merely mention the string (`database.py`, `provider_registry.py`)
  would false-positive. The store's writers are covered by the
  registered-writer leg instead.

## Evidence (local, mini-server, venv glossa-ci, CI-identical env)

- Targeted run: **48 passed in 60.82s** — 18 new battery + 23 Stage 1
  encryption + 7 F1 disk-full, Stage 1's fixtures unchanged.
- Full backend suite (the CI invocation; GPU files ignored; the phase392
  deterministic test deselected by plain nodeid per the standing local
  rule — CI is authoritative for that test): attempt 1 was killed at
  ~77% by a mini-server reboot (a box event; the live backend unit
  returned to active on its own; no failures appeared in attempt 1's
  progress output up to the kill — partial evidence only, not a
  verdict). Attempt 2, the verdict run: **2779 passed, 108 skipped,
  29 warnings in 301.49s**.
- Ledger gate on the final tree: `--all` **29 PASS / 0 FAIL / 1 NOT-RUN**
  (RESULT: PASS); `--regen` **32 PASS / 0 FAIL / 0 NOT-RUN** (RESULT:
  PASS) — the standing profile in both modes. In-tree regenerations from
  the test runs (extracted claims, the batch report, the partial loop
  output) were restored before the gate runs and before the commit.
- Ruff 0.17.5: all checks passed on the four changed files.

## Claims discharged

C092-6, C092-7 (the library leg), C092-8, C092-13.

## Deviations and deferred items

- Branch name: the brief's `spec/092-s2-verified-write` over tasks.md's
  `feat/092-s2-verified-write`.
- Ladder refinement: the subprocess child leg engages only on the
  write-denial signature (reasoned under T201 above).
- `ARTIFACT_PATH_PATTERNS` not extended (reasoned under T203 above).
- Observed, out of scope, not touched: `privacy_statement.py` section 2
  still describes the settings store as "not encrypted" — stale since
  Stage 1 (2026-11-14). It is owner-approved policy text with its own
  change process (its section 7); correcting it is not Stage 2's to do
  (the C092-14 boundary).
- Nothing else deferred. Stage 3 (T301–T305) and closeout (T401) are
  separately commissioned.
