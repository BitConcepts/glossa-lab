# Feature Specification: Platform Hardening R4 — Credential Encryption at Rest, Verified Writes, and the Test-Harness Remainder

**Feature Branch**: `092-platform-hardening-r4` (build stages); this package
lands on `docs/092-r4-draft`
**Created**: 2026-11-05
**Status**: RATIFIED AS A BLOCK by the owner, Tristen Pierson,
2026-11-06 (decisions D-092-1..4 adopted as recommended; record:
`records/ratification-2026-11-06.md`). The claims intake was
executed at adoption through the ledger's own machinery
(T004): C092-1..14 stand in the claims ledger and the
generated layers are regenerated over the grown ledger.
**Nothing in this package is a result: no credential has
been encrypted, no verified-write library has been built,
and no harness leg has run. No build stage (Stage 1
onward) is started by this motion.**
**Input**: The owner's commission in this chat, 2026-11-05, from the
decision queue presented the same day (item 15: "Commission the R4
hardening spec," recommendation adopted as presented — commission, with
the `.keys.json` encryption first). The bundle is the standing audit-R4
remainder, carried since the password-hashing audit of 2026-10-30
recorded its single observation and the harness items accumulated
across Specs 087–089.
**Evidence of record**: the grounding record in
`records/commission-and-grounding-2026-11-05.md`, counted and read
first-hand from the repo at `27ce5550` on 2026-11-05: the settings
store (`backend/glossa_lab/api/settings.py` — `_keys_file` l.101,
`_load_keys` ll.106–113, `_save_keys` ll.116–124, `get_key`
ll.152–186, masked GET ll.489–505) and its consumer census; the
password-hashing audit of 2026-10-30 (§4, the observation; §7, no
defects besides); the fleet's safe-write tooling
(`~/workspace/system/safe-write/` — `safe_write.py`,
`safe-write.mjs`, `wave_probe.py`, the 14-check fault-injection
self-test); run-defs v1 §5 (suite divergence shape #1); Spec 089 S4's
rewrite-manifest machinery (`run_records.rewrite_manifest`,
`apply_rewrite_dispositions`); and the standing harness observations
(phase392 local stall; the 2026-11-01 unclassified notifications
ERROR).
**Predecessors**: Spec 082 (the token custody class this spec
explicitly does not touch), Spec 080 (the desktop topology the
production store lives under, and the data-dir copy shape C092-2 is
written against), Spec 089 (run-defs, the rewrite manifest, the V9
writer census this spec registers into), Spec 084 (the policy
fixtures — the privacy text's `.keys.json` disclosure stands as
written; this spec is the hardening it anticipated).

## Problem statement

Three places in the platform still tolerate a degraded state silently,
each small, each named before, none closed:

- **Credentials sit in plaintext behind a masked API.** The settings
  store keeps every outbound credential the backend must present —
  provider API keys, the SMTP password, and a long-lived Microsoft
  Graph refresh token — as plaintext JSON in `{data_dir}/.keys.json`.
  The file is chmod 0600 and the API never returns a value, which is
  exactly the custody the 2026-10-30 audit recorded, with its
  condition: *if the fleet standard requires encryption at rest for
  stored service credentials, this is the one place in Glossa that
  would not meet it.* The owner has now set that standard by
  commissioning this spec. The exposure is concrete in this program:
  its data dir is copied as a matter of routine (preservation
  snapshots, the Spec 080 migration), and every copy carries every
  credential in the clear.
- **The store's own write can destroy it.** `_save_keys` writes with a
  direct truncating `write_text`. The fleet's write-denial signature
  is proven at syscall level: open-with-truncate succeeds, the write
  itself is denied, and a file's content is gone before the error
  surfaces. The one file in the system whose loss is total (every
  stored credential at once) is written by the one pattern that can
  zero it. The verified-write construction that answers this exists
  and is proven — as agent tooling outside the repo. The shipped
  backend has no such path.
- **The harness absorbs noise instead of closing it.** A teardown
  ERROR family (sqlite closed-database, tray tests) has been
  rerun-managed through three specs and is registered as a known
  divergence shape — explained, never fixed. Suite runs still rewrite
  files inside the tree they measure; Spec 089 S4 made the rewrites
  visible and dispositioned, but restoration remains a manual
  post-run act and the run-scoped tests skip themselves on a dirty
  tree, so full-suite evidence about them is systematically absent. A
  determinism test stalls locally for tens of minutes and is
  deselected by hand from operator memory each enumeration. One ERROR
  from 2026-11-01 sits unclassified. None of these blocks a verdict
  today; all of them tax every future one, and each is the kind of
  known problem the program's standing rule says not to leave.

This spec closes the three, in the owner's priority order: the
credential store first, the write path second, the harness last.

## Scope — what this spec builds

- **S1 — Credential encryption at rest (C092-1..5, C092-7's store
  leg).** The settings store encrypts every credential-class value
  under the construction and key custody the owner selects at
  D-092-1, in the per-value format of D-092-2: a versioned store
  format in which credential entries carry ciphertext (AEAD, fresh
  nonce per value) and non-secret configuration stays readable. The
  save path writes through the verified-write construction (temp +
  fsync + atomic rename + read-back) from this stage — hand-rolled
  once here if the library has not yet landed, and refactored onto it
  in S2. Legacy plaintext stores migrate on first load, exactly once,
  verifiably (C092-4). A store that cannot be decrypted is a named
  error state, never an empty store (C092-3). No caller changes
  (C092-5): the stage's diff is the store's internals, the key-loading
  path, the dependency the selected construction requires, and tests.
- **S2 — The verified-write library (C092-6..8, C092-13).** The
  safe-write contract becomes a supported module in
  `backend/glossa_lab/`, documented as the way repo code writes state
  that matters, with the fault-injection battery running in CI. The
  keys store is refactored onto it as the first adopter of record;
  the store-writing modules this spec adds or moves are registered in
  the gate's V9 writer census.
- **S3 — The test-harness remainder (C092-9..12).** Four independent
  legs, each closing one standing item on evidence fixed in advance:
  the tray teardown ERROR root-caused, fixed at its source, and
  discharged against five named clean full-suite runs, with the
  run-defs shape registration amended on discharge; in-tree rewrites
  eliminated as a live-tree phenomenon (isolated copies or asserted
  temp-tree outputs), the post-run restore retired as a routine act,
  and the clean-tree guard skip count brought to zero; the phase392
  stall profiled and its local handling converted to a registered
  outcome (in-budget completion, or a named environment-scoped
  registration with CI as the authoritative runner); the unclassified
  notifications ERROR run through its stated battery and classified,
  or closed UNREPRODUCED on that battery with a self-reopening term.
- **Closeout.** Per-claim dispositions at stage-evidence strength,
  the standing gate profile restated from the gate's own output, and
  the boundary verification of C092-14 by diff census.

## Non-goals (explicit)

- **The Spec 082 install token.** `{data_dir}/api_token` is a bearer
  credential the local tooling must present; its 0600 file custody is
  by design (audit §6, listed, not graded). Untouched (C092-14).
- **User-account passwords.** There are none on the backend (the audit
  graded the edge's Argon2id sound; the desktop app is token-only).
  Nothing in this spec touches a password path.
- **The cloud edge's secret custody.** Worker secrets and D1 hashes
  are a different, already-sound custody class. Untouched.
- **A general secrets manager.** The store remains the app's own file
  in the operator's data dir; this spec changes its form, not its
  architecture. No external vault service is introduced.
- **Rewriting the agent-side safe-write tooling.** It stays the
  fleet's VM-side practice; S2 carries its *contract* into the repo,
  it does not import or replace the tooling.
- **New harness coverage.** S3 closes named standing items; it does
  not add new test areas, and it does not weaken any existing
  assertion to buy a pass (D-092-4 states the rule for the sharpest
  case).

## Decisions

- **D-092-1 — Key custody for the credential store (the owner's
  decision; the stage cannot build until it lands).** Options:
  (a) **Dedicated key file with separate custody** — a 32-byte key in
  a 0600 file *outside* `{data_dir}` (default: the per-user config
  location beside the data dir), loaded when the store opens; the
  construction is AES-256-GCM via the `cryptography` package (one
  added dependency), per-value random nonce, versioned envelope.
  (b) **OS keychain** — the key held in Windows Credential Manager
  (via the `keyring` package) on the desktop host. No key file to
  back up or lose; the OS brokers access.
  (c) **Windows DPAPI** (ctypes over crypt32, no new dependency) —
  ciphertext bound to the Windows user account; no separable key
  material exists at all.
  (d) **Environment-supplied key** — the key arrives in the process
  environment at start; nothing key-shaped rests on disk.
  *Recommendation: (a).* The deciding facts are this program's own.
  The store must work identically on the desktop host (Windows) and
  in the Linux VM/CI where the suite runs, because the fleet's rule
  is that the tested path is the production path — (b) exercises a
  different keyring backend (or none) under Linux CI than in
  production, (c) cannot run off Windows at all, so both make the
  battery prove a fallback instead of the construction. (d) fails on
  this host's topology: the backend starts unattended (Spec 080's
  logon task plus its 15-minute ensure tick), and an unattended
  starter has no channel for an env secret except a file or the task
  definition — a key file with worse custody and no rotation story.
  (a)'s custody argument is the Spec 080 lesson: this program copies
  its data dir (two preservation snapshots and a cross-machine
  migration on record), and a key outside the dir is the only option
  whose copies never travel with the ciphertext. Its cost is stated
  plainly: the key file is a second thing to preserve, and losing it
  loses the stored credentials to re-entry (C092-3 makes that loss
  loud, not silent). (b) is the runner-up if the owner prefers
  OS-brokered custody and accepts the Stage 1 proof duty named in the
  grounding record (starter-context reachability) plus the CI-path
  divergence.
- **D-092-2 — Encryption scope: per-value over the credential class.**
  Options: (a) per-value — credential-class entries encrypted,
  non-secret configuration and provider prefs remain readable in the
  same file; the encrypted set is a registered list the stage
  maintains (provider API keys, `smtp_password`,
  `ms_graph_refresh_token`, and any future key whose name joins the
  registered credential set). (b) whole-file — the entire dict
  encrypted as one blob.
  *Recommendation: (a).* It is the audit's smallest-fix shape
  ("encrypt `.keys.json` values"); it keeps the masked-status and
  scheduler reads of non-secret settings free of the key (a missing
  key then degrades exactly the credential class, under C092-3's
  named error, instead of taking the whole settings surface down);
  and it keeps the file inspectable for the non-secret state the
  operators legitimately read. (b)'s gain — hiding configuration
  metadata — is not a stated requirement, and its cost is coupling
  every settings read to key availability.
- **D-092-3 — Shape #1's registration on discharge: amend, never
  delete.** On C092-9's discharge, the run-defs v1 §5 registration is
  amended by act to record the mechanism and the fixing stage, and
  the shape stops matching as *explained*: a later teardown ERROR of
  the family is a new unexplained junction. Options: (a) amend as
  stated; (b) retire the shape from the registry entirely.
  *Recommendation: (a).* The registry is the program's memory of its
  divergence shapes; deleting the entry would make a recurrence
  indistinguishable from a first sighting, which is the state the
  program was in before Spec 089.
- **D-092-4 — The phase392 outcome branch, chosen in advance.** If
  the profile shows the stall's cost is intrinsic compute (the
  determinism check's own work at production scale), the stage
  registers the environment-scoped deselection (CI authoritative)
  rather than reducing the test's scale or weakening its assertion;
  if the profile shows a fixable pathology (an accidental quadratic,
  a retry loop, an unbounded wait), the stage fixes the pathology and
  the test runs locally in budget. *Recommendation: adopt this branch
  rule at ratification,* so the stage's outcome is decided by the
  evidence it gathers, not negotiated after it.

## Requirements (summary; the claims in claims.md are the normative text)

- **R1 (C092-1..5)** — the credential store encrypted at rest under
  D-092-1/D-092-2, migrating legacy stores verifiably, failing loudly
  and by name when it cannot decrypt, with every caller's contract
  unchanged.
- **R2 (C092-6..8, C092-13)** — a supported verified-write library in
  the backend carrying the safe-write contract, the keys store as its
  first adopter, the observed failure classes seeded in CI, and the
  new writers inside the gate's writer census.
- **R3 (C092-9..12)** — the four harness remainders closed on bars
  fixed at ratification: five named clean runs (tray), a clean tree
  and zero guard skips (rewrites), profile evidence plus a registered
  outcome (phase392), a stated battery and an honest end state
  (notifications ERROR).
- **R4 (C092-14)** — the boundary held: storage form and harness
  behaviour change; claim statuses, the token file, edge custody, and
  UI behaviour do not.

## Governance

- Stages land as separate PRs from the build clone, parent-gated on
  per-job CI green plus the delivery checker, per the standing seat
  discipline; each stage record cites the runs it relied on by the
  Spec 089 quadruple.
- The adoption intake (Stage 0, T004) appends the C092 bundle through
  `tools/ledger/import_bundle.py` only, regenerates the generated
  layers, and republishes through the gated path — the ledger grows
  by exactly this bundle.
- CI is green on the day's work or the work is not done; the backend
  CI job no longer stops at the first failure (the owner's `-x`
  removal, decided 2026-11-05 in the same queue as this commission),
  so stage enumerations cite full counts, not floors.
- No stage touches a credential value: fixtures carry synthetic
  values, stage records cite key names and counts, and the live
  migration's proof is a name census, never a value.
