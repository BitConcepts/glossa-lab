# Spec 092 — Commission and grounding record (2026-11-05)

**Commission.** The owner commissioned the Audit R4 hardening spec
from the decision queue presented in the Glossa-Lab chat on
2026-11-05 (item 15, "Commission the R4 hardening spec"; the
recommendation was adopted as presented: commission, with the
`.keys.json` encryption first). The bundle is the standing audit-R4
remainder: (a) encryption at rest for stored outbound service
credentials; (b) a verified-write helper as a supported library path;
(c) test-harness hardening — the tray-teardown ERROR family, the
in-tree rewrite precondition class's remainder, the phase392 local
stall, and the one unclassified notifications ERROR. This record is
the package's grounding: everything below was read first-hand at
drafting, from the repo at `origin/main` = `27ce5550` (2026-11-05)
and from the audit file of record. No credential value was read,
copied, or recorded at any point in this grounding — key names,
counts, and mechanisms only.

## 1. The `.keys.json` mechanism, as found (item a)

Source of record for the finding: the password-hashing audit of
2026-10-30 (goal workspace
`hidden_files/password-audit-2026-10-30/AUDIT.md`, §4 and §7), which
graded the codebase's password handling SOUND in every user-password
path and recorded exactly one observation: outbound service
credentials stored in plaintext JSON. The audit read `main` at
`d3dcebd9`; the mechanism was re-verified at drafting against `main`
at `27ce5550` and is unchanged.

- **The store.** `backend/glossa_lab/api/settings.py` (547 lines):
  `_keys_file()` (l.101) resolves `{data_dir}/.keys.json`;
  `_load_keys()` (ll.106–113) returns the parsed JSON dict, and
  returns `{}` on *any* exception (a corrupt or unreadable store is
  indistinguishable from an unconfigured one — the behaviour C092-3
  retires for the encrypted path); `_save_keys()` (ll.116–124) writes
  with a direct `Path.write_text` followed by a best-effort
  `chmod 0o600`. The write is neither atomic nor verified — under the
  fleet's documented write-denial signature (open-with-truncate
  succeeds, the write is denied; evidence note of 2026-10-30), that
  call can destroy the only copy of every stored credential before
  failing. This is the concrete joint between items (a) and (b).
- **What the store holds.** One JSON dict mixing three classes:
  credential values (the `KNOWN_KEYS` provider API keys;
  `smtp_password` and the SMTP settings block, ll.59–66 region;
  and — found at drafting, beyond the audit's enumeration — the
  long-lived Microsoft Graph refresh token, saved as
  `ms_graph_refresh_token` by the notifications API's Graph connect
  path, `backend/glossa_lab/api/notifications.py` ll.282–284, and
  consumed by `backend/glossa_lab/notifications/graph.py`); non-secret
  configuration (`smtp_host`, `smtp_port`, `smtp_from`,
  `openalex_email`, the schedulers' `discovery_daily` /
  `study_loop_daily` toggles and intervals); and provider preferences
  under `_provider_prefs`. The mixed dict is the factual basis for
  decision D-092-2 (per-value encryption of the credential class).
- **Access funnels through one module.** Every reader and writer
  reaches the file through `api/settings.py`'s `_load_keys` /
  `_save_keys` / `get_key` (code census at drafting: direct importers
  of the private helpers are `api/notifications.py`,
  `discovery/scheduler.py`, `study_loop_scheduler.py`, and
  `database.py` l.731 — the last a one-time Ollama-prefs migration
  read at database init; `get_key` consumers include
  `notifications/smtp.py` l.58, which takes `smtp_password` to the
  SMTP `login`). No module reads or writes the file directly. This is
  what makes C092-5 (internals-only change) a claim that can hold.
- **Resolution and masking.** `get_key` (ll.152–186): process env
  (uppercased name) wins over the stored value; placeholder values are
  filtered as unconfigured. The GET settings endpoint returns masked
  set/unset status only (ll.489–505); values are never returned. The
  PUT endpoint (ll.512–547) writes through `_save_keys` and also sets
  the value into the process environment.
- **No crypto dependency exists.** `backend/pyproject.toml` and
  `backend/requirements.txt` at `27ce5550` carry no `cryptography`,
  no `pynacl`, no `keyring`. Any construction the owner selects under
  D-092-1 either adds one dependency deliberately or uses the
  platform's own facility (DPAPI via ctypes). The audit's own smallest
  fix (§4) frames the shape: "encrypt `.keys.json` values under a
  machine-local key (OS-keychain-backed or a 0600 key file beside
  it) — a storage change in `_load_keys`/`_save_keys` only; callers
  unchanged."
- **Explicitly out of scope.** The Spec 082 install token
  (`{data_dir}/api_token`, a 0600 bearer-credential file by design —
  audit §6, listed and not graded) and the cloud edge's custody
  (Worker secrets; SHA-256 hashes in D1) are different custody classes
  and are not touched (C092-14).

## 2. The verified-write practice, as found (item b)

The fleet's existing practice lives outside the repo at
`~/workspace/system/safe-write/` (built 2026-10-28; README + sources
read at drafting):

- **Python entry:** `safe_write.py` — `write_file_verified(path,
  content)` returns `{ok, via, attempts, sha256}` and raises
  `SafeWriteError` on total failure. Construction: temp file in the
  target's directory (mkstemp inside the guarded region — the
  2026-10-28 retrofit fix), write + flush + fsync, atomic
  `os.replace`, directory fsync, read-back SHA-256 verification.
  Retry ladder: local attempt, then alternating fresh-subprocess
  attempts (`--child-write`, because write denial is sticky per
  process lineage) and local retries, bounded (default 3 retries).
  Empty content is refused outright.
- **Node twin:** `safe-write.mjs` — `writeFileVerified(path, content)`
  → `{ok, via, attempts, error}`, same construction. (Repo scope for
  this spec is the Python path; the backend is Python.)
- **Wave probe:** `wave_probe.py` — one verified write of a probe
  file; exit 0 CLEAR / exit 3 WAVE.
- **Fault-injection self-test:** `self-test.mjs`, 14 checks (empty
  write, 0-byte detection, parent-failure classes incl. regression
  checks 13–14) — the model for C092-8's in-CI battery.
- **Why a library path, not an import of the tooling:** the safe-write
  directory is agent tooling on this VM, not a shipped dependency of
  the backend (the production backend runs on TRISTEN-DESKTOP under
  the Spec 080 topology). Item (b) carries the contract into the repo
  as a supported module so the shipped product owns its write
  discipline; the tooling remains the agent-side practice.

## 3. The harness items, as found (item c)

- **Tray teardown flake (suite divergence shape #1).** Registered in
  run-defs v1 §5 (`glossa-indus/ledger/RUN-DEFINITIONS.md`, Spec 089
  S1): a divergence between two suite runs is inside the shape iff it
  is confined to teardown ERROR entries of the sqlite
  closed-database family on tray test ids (first registered instance:
  `test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`),
  with pass and fail counts otherwise equal. The family has recurred
  across Specs 087–089 enumerations and CI attempts (five hand
  adjudications in three days during Spec 089's grounding alone) and
  is currently *managed* — rerun, junction-explained — never
  root-caused. C092-9 requires the mechanism and the fix.
- **In-tree rewrite remainder.** Settled behaviour (Spec 089
  grounding): tests regenerate `glossa-indus/claims/extracted_claims/*.json`
  (and occasionally claim_reports, and the repo-root
  `outputs/partial_loop_result.json`) inside the tree they run in.
  Spec 089 S4 (PR #520) discharged the visibility half:
  `run_records.rewrite_manifest` + `apply_rewrite_dispositions`
  enumerate every rewritten path under the watched roots with
  head/worktree hashes, enforce dispositions before any byte moves,
  and restore HEAD bytes hash-verified. The remainder S4 did not
  close, and C092-10 scopes exactly it: the rewrites still happen in
  the live tree, restoration is still a routine post-run act, and the
  run-scoped tests carry a clean-tree precondition guard that skipped
  8 of S2's 13 new tests (and 2 of S3's) inside full-suite runs —
  they pass standalone, so the suite's own evidence about them is
  systematically the skipped kind.
- **phase392 local stall.**
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  stalls for tens of minutes on this VM, equally on pristine
  `origin/main` (so not a regression of any branch), and every Spec
  089 stage enumeration deselected exactly this one test by hand and
  said so. CI is its de-facto authoritative runner. No profile of the
  stall exists; C092-11 requires the evidence before the disposition.
- **Unclassified notifications ERROR.**
  `test_notifications_api.py::test_mask_email_redacts_local_part`
  produced one ERROR in the 2026-11-01 enumerations, was recorded
  UNCLASSIFIED with no second sighting, and has sat there since.
  C092-12 fixes the battery (50 module repetitions + 3 suite-order
  runs) and the two honest end states in advance.

## 4. Grounding gaps — what this drafting did not establish

1. **The live desktop store's contents were not inspected.** The
   desktop install's `.keys.json` (which credentials are actually
   configured, whether the Graph token is present) was not read — by
   design (no credential values), and per the audit's own coverage
   note (it graded code, not any install's data files). C092-4's
   migration is therefore written against fixture stores; the live
   proof (key-name census before/after, never values) belongs to
   Stage 1's deployment record.
2. **The tray flake's root cause is unknown at drafting.** The
   fixture/connection-lifecycle reading is a hypothesis shape, not a
   finding; C092-9 is written so the stage must produce the mechanism
   with evidence, and its discharge bar (five named clean runs) is
   fixed before the answer is known.
3. **The notifications ERROR has never reproduced.** One sighting,
   2026-11-01. The battery sizes in C092-12 are a judgment, stated in
   the claim so the owner ratifies the bar, not just the outcome.
4. **No profile of the phase392 stall exists.** The environmental
   reading (shared VM, ~7.9 GB RAM, no swap) is consistent with the
   pristine-main observation but is not evidence; C092-11 requires
   the profile first.
5. **Keychain reachability from the desktop starter's context is
   untested.** If the owner selects D-092-1 option B, whether the
   Spec 080 starter's logon task and 15-minute ensure tick can reach
   the interactive user's Credential Manager store must be proven in
   Stage 1 before the construction is adopted — it is an open risk
   of that option, named in the decision.
6. **Whether `cryptography` is present transitively in the desktop
   runtime was not verified** — it is absent from the repo's declared
   dependencies (§1); Stage 1 adds it explicitly if D-092-1 selects
   the key-file option, and the addition is part of that stage's diff,
   not an assumption.

## 5. Format and numbering

Package format follows Specs 089/090: `spec.md`, `claims.md`,
`aee-claims.json` (normalized from claims.md), `plan.md`, `tasks.md`,
`records/`. The spec number is **092**: `specs/` on `main` at
`27ce5550` ends at `090-projected-constraints-generalization-study`;
no 091 or 092 directory exists. Claim ids are C092-1..14; decisions
D-092-1..4. Stage order follows the owner's stated priority —
encryption first (Stage 1), verified writes second (Stage 2), harness
remainder third (Stage 3) — with Stage 0 (adoption) before them and
the closeout after, per the house pattern.
