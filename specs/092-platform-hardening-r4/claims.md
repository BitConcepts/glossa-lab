# Spec 092 — Claims

Every claim carries at least one falsifier (a concrete observation that
would show it false) and a "does not establish" line (the over-reading it
forbids), per the program's claims discipline. The security claims
(C092-1..4) carry attack-shaped falsifiers: each names the adversary's
position and the exact observation that would break the claim. The same
set, normalized into `aee-claims.json` without substantive change, is
validated under the pinned AEE (1.5.3) before any build task starts
(Stage 0, T002; `records/t002-aee-assessment.json`). Grounding for every
machinery statement below: `records/commission-and-grounding-2026-11-05.md`,
counted and read first-hand from the repo at `27ce5550` on 2026-11-05,
and the password-hashing audit of 2026-10-30 (goal workspace,
`hidden_files/password-audit-2026-10-30/AUDIT.md`, §4).

## Credential encryption at rest (Stage 1 — the owner's first priority)

**C092-1 — No stored credential value exists in plaintext at rest.**
Every credential-class value the settings store persists — the provider
API keys, the SMTP password, and the long-lived Microsoft Graph refresh
token (`ms_graph_refresh_token`), per the credential set the stage
registers — is encrypted under an authenticated-encryption construction
with a fresh random nonce per value before it is written. The store
file's bytes contain no stored credential value: not as a JSON string,
not base64- or hex-encoded, not as any contiguous substring.
*Falsifier:* take the `.keys.json` from a configured install, with full
knowledge of the format and the code, but without the key material, and
recover any one stored credential value from the file bytes alone
(substring search over the raw bytes, JSON parse, encoding-decode of
every field).
*Does not establish:* protection against an adversary who executes code
as the same OS user on the live host — the store must be decryptable by
the backend process, and that boundary is named, not hidden (the threat
this claim closes is the audit's: a reader of the data dir — a copy, a
snapshot, a backup, another user — holding the file but not the key).

**C092-2 — The encryption key never lives in the data dir it protects.**
The key is loaded from the custody location decision D-092-1 selects,
which is outside `{data_dir}`. No copy of the key material is written
into `{data_dir}`, into the repository, or into any artifact the data
dir's own copy path carries (the Spec 080 snapshot and migration shape:
this program copies its whole data dir, and a key inside it would
travel with every copy).
*Falsifier:* a copy of `{data_dir}` alone — the snapshot/migration
shape — suffices to decrypt a stored value; or key bytes found anywhere
under `{data_dir}` or in the repo tree.
*Does not establish:* protection against an operator who deliberately
exports both the data dir and the key — only that the program's own
copy paths never bundle them.

**C092-3 — A store that cannot be decrypted is a named error, never an
empty store.** When a store file exists but cannot be decrypted —
missing key, wrong key, corrupt or tampered ciphertext — the settings
surface reports a named error state that distinguishes it from "no keys
configured," and no credential is served from it. The loader never
falls back to parsing an encrypted store as plaintext, and never
presents an undecryptable store as empty (the current loader's
silent-`{}`-on-any-error behaviour is retired for the encrypted path).
A startup-path reader that cannot tolerate the failure (the database
init's one-time prefs migration) must skip with a logged reason, never
crash the backend and never silently proceed as if unconfigured.
*Falsifier:* replace or remove the key on a configured install and
observe the settings API report the keys as simply unset, or observe
any credential value served; or remove the key and observe the backend
fail to start without a named store error in its log.
*Does not establish:* availability — a lost key still loses the stored
credentials, and re-entry is the recovery; the claim is that the loss
is loud and named, never silent.

**C092-4 — A legacy plaintext store migrates exactly once, verifiably,
or not at all.** On the first load after the upgrade, a store in the
legacy plaintext format is read, rewritten in the encrypted format
through the verified-write construction (C092-7), and proven by
re-reading: every value present before migration is returned
identically by `get_key` after it, and the credential set encrypted is
exactly the registered set. An absent or credential-free store is a
no-op, not a migration. A failed migration leaves the original file
byte-untouched and the failure named — there is no half-migrated state.
*Falsifier:* a legacy fixture store whose post-migration `get_key`
results differ from its pre-migration results for any key; or a
migration failure (key absent, write denied) after which the original
file's bytes changed.
*Does not establish:* migration of any particular live install — the
desktop install's store is migrated when Stage 1 deploys there, and
its proof is that stage's record against the live store's key census
(names and counts, never values).

**C092-5 — Encryption changes the store's internals only; every
caller's contract is unchanged.** `get_key`'s resolution order (process
env over stored), the placeholder filtering, the masked GET status
shape, the PUT semantics (including the process-env side effect), and
every consumer — the settings API, `notifications/smtp.py`,
`notifications/graph.py`, the notifications API's Graph save/disconnect
path, the discovery and study-loop schedulers, and the database init's
prefs migration — behave identically to the pre-stage code. All access
continues to funnel through `api/settings.py`'s store functions; no
consumer gains a direct file read.
*Falsifier:* a diff in any consumer module required by the stage; or a
behavioural difference in the masked status surface or `get_key`
results over a fixture store, before versus after the stage, for the
same inputs.
*Does not establish:* that the consumers are themselves secure — only
that this stage does not move their contract while it changes the
storage form underneath them.

## Verified writes (Stage 2; the store-path leg lands in Stage 1)

**C092-6 — The repo carries a verified-write library path with the
fleet's proven contract.** `backend/glossa_lab/` gains a supported
module implementing the safe-write contract the fleet's tooling
(`~/workspace/system/safe-write/`) already proves: temp file in the
target's own directory, fsync, atomic rename, read-back hash
verification, a bounded retry ladder that includes a fresh-subprocess
attempt (write denial is sticky per process lineage), refusal of empty
content, parents never created implicitly, and a typed error — never a
bare `OSError` — when every path fails. The module is the documented
way repo code writes state that matters; the keys store is its first
adopter of record.
*Falsifier:* a caller of the helper observes a reported success whose
on-disk bytes differ from the content written; or a write-path failure
(a denied write, a missing or non-directory parent) escaping the
helper as an untyped exception; or an empty write landing through it.
*Does not establish:* durability against a storage stack that lies
below fsync — the contract is verification against read-back, which is
the failure class the fleet actually met (denied writes and silent
0-byte landings), named as such.

**C092-7 — A failed write never destroys the previous good target.**
Because a verified write lands by renaming a fully written temp file,
any failure before the rename leaves the prior target byte-identical.
The keys store's save path writes through this construction from
Stage 1 (retiring the direct `write_text`, whose truncating open can
destroy the only copy of every stored credential before a denied write
lands — the write-denial evidence of 2026-10-30), and its library
form from Stage 2.
*Falsifier:* under fault injection — write denied at open, write
landing 0 bytes, rename-time failure — the target's bytes after the
failed call differ from its bytes before it, on either the helper path
or the keys-store path.
*Does not establish:* protection against deletion or corruption of the
file by means outside the write path.

**C092-8 — The write failure classes the fleet actually met are seeded
in CI.** The fault-injection battery modelled on the safe-write
self-test (14 checks there) runs in the repo's CI: permission-denied
writes, silent 0-byte landings, short writes, and missing or
non-directory parents each surface as the typed error with the target
preserved. The construction production runs is the construction the
battery exercises, on the CI runners as well as locally.
*Falsifier:* a seeded class that escapes the battery as an untyped
error, lands silently, or is exercised only on a developer machine and
not in CI.
*Does not establish:* that real write-denial waves behave exactly like
the seeds — the classes are the observed ones, and the claim covers
exactly those.

## Test-harness remainder (Stage 3)

**C092-9 — The tray teardown ERROR is root-caused and eliminated, not
rerun-managed.** The mechanism behind suite divergence shape #1
(run-defs v1 §5: teardown ERROR entries of the sqlite closed-database
family on tray test ids, first instance
`test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`)
is identified in the stage record with its evidence, and the defect is
fixed at its source in the fixture/connection lifecycle. Discharge
requires five consecutive full-suite runs, named by run id (CI runs or
bound local light records), with zero teardown ERRORs on tray tests;
on discharge the shape's run-defs registration is amended by act
(D-092-3) to record the fix, so a recurrence is a new unexplained
junction, not a known shape to rerun away.
*Falsifier:* a teardown ERROR of that family on any suite run after
the fix lands; or a discharge claimed on fewer than the five named
runs, or on runs not named.
*Does not establish:* that no other teardown flake exists — only that
this family's mechanism is found, fixed, and watched by a stated bar.

**C092-10 — A full-suite run leaves the working tree clean; the
clean-tree guard skip is retired.** Spec 089 S4 made in-tree rewrites
visible (the rewrite manifest over the watched roots
`glossa-indus/claims/`, `glossa-indus/reports/`) and dispositioned;
this claim closes the remainder: after a full-suite run, `git status`
under the watched roots and the repo-root `outputs/` path is empty
with no restore step — tests that regenerate artifacts write to
isolated copies, or the regeneration is the test's own asserted output
in a temp tree. The manifest remains as the detection instrument, but
restoration stops being a routine post-run act, and the count of
run-scoped tests skipped by the clean-tree precondition guard in a
full-suite run is zero (S2's enumeration skipped 8 of 13 that way; the
guard, not the tests, is what retires).
*Falsifier:* a full-suite run after this stage whose post-run
`git status` under a watched root is non-empty absent a recorded
disposition for that run, or whose suite light record shows a
guard-skipped test.
*Does not establish:* that tests never write files — only that they
never write the live tree they are measuring.

**C092-11 — The phase392 local stall is explained, and its handling is
registered machinery.** A stage record states where the stall's time
goes, from profile evidence gathered on this VM, for
`test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
(which stalls for tens of minutes locally, equally on pristine
`origin/main` — environmental in shape, unexplained in fact). The
local path then takes exactly one of the two registered outcomes: the
test completes within a stated budget on the VM, or its deselection
becomes a named, environment-scoped registration (run-defs entry or
the suite-runner configuration of record) with the CI backend job as
its authoritative runner. No later enumeration depends on an operator
remembering to deselect it by hand.
*Falsifier:* a local full-suite enumeration after this stage that
stalls on the test, or deselects it by an unregistered manual act; or
a stall explanation asserted in the record without profile evidence.
*Does not establish:* that the test becomes fast, or that its
determinism assertion may be weakened — D-092-4 forbids buying the
budget by weakening what the test asserts.

**C092-12 — The unclassified notifications ERROR is classified, or
closed on a stated battery.**
`test_notifications_api.py::test_mask_email_redacts_local_part`
carries one ERROR sighting (2026-11-01) and no classification. The
stage runs a stated battery — 50 repetitions of the notifications
module standalone plus 3 full-suite-order runs — and the item ends in
exactly one state: reproduced, and then classified (a named flake
family, or a defect fixed at its source under C092-9's pattern); or
not reproduced anywhere in the battery, and closed UNREPRODUCED with
the battery as the evidence of record. The closure record carries its
own reopening term: a later sighting reopens the item automatically.
*Falsifier:* the ERROR recurring after an UNREPRODUCED closure without
the item reopening; or a closure asserted on less than the stated
battery.
*Does not establish:* that the test is correct — only that its error
state no longer sits unclassified, which is the defect this item
carries.

## Census and boundary

**C092-13 — Every writer this spec adds or moves stands in the gate's
writer census.** The writers Stage 1 and Stage 2 create or move (the
encrypted store's save path, the verified-write module's adopters of
record) are registered under the V9 writer-census discipline Spec 089
S5 established, so the census the gate computes finds exactly the
registered set. The standing gate profile after this spec is whatever
the gate's own output states on the final tree, recorded verbatim in
the closeout.
*Falsifier:* a store-writing module in the tree that the census does
not name, found by the gate or by audit.
*Does not establish:* that unregistered writers are impossible — only
that this spec's surface is fully inside the census the gate runs.

**C092-14 — Boundary: this spec changes storage form and harness
behaviour, and nothing else.** No claim's status, stage, or score
moves under this spec; no settling verdict is re-adjudicated; the
Spec 082 install-token file is untouched (a bearer credential by
design — password audit §6, a different custody class, listed and not
graded there); the cloud edge's secret custody (Worker secrets, D1
hashes) is untouched; no wireframe-gated UI surface changes (the
settings surface's behaviour is contract-identical under C092-5).
*Falsifier:* a diff in this spec's stages that moves a claim status,
alters the token file's handling, touches edge secret handling, or
changes a UI surface's behaviour.
*Does not establish:* that the out-of-scope surfaces are sound — only
that they are out of this spec's scope, each with its own record.
