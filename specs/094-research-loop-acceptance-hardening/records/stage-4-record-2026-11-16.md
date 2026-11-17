# Spec 094 — Stage 4 record (lifecycle routing and atomic stores)

- **Stage:** 4 — lifecycle routing and atomic stores (T401, T402, T403)
- **Date:** 2026-11-16
- **Base:** `98559bfe51da5a3bfc61b38e651f5b1a4e316f52` (Stage 3 merge, PR #575)
- **Branch:** `spec/094-s4-lifecycle-routing`
- **Tasks discharged:** T401, T402, T403
- **Claims discharged:** C094-10, C094-11, and the D-094-5 stage-4 exit
  gate (the storage-edit probe re-run, filed here). This record does
  not establish the Stage 5 closeout (T501/T502) and lifts no part of
  C094-13.

## What was built

**T401 — the gated transition service** (`backend/glossa_lab/
anchor_transition.py`, new). One module is now the only writer of
`review_status` on anchor-path records. It carries the same
guarantees `claim_stage.transition_stage` carries for the claims
ledger, restated for the anchor path's own vocabulary (the mapping
answer is §1 below):

- **Legality first.** A transition outside the allowed table does not
  exist to attempt: it is refused before any other consideration,
  and the refusal changes nothing and appends nothing.
- **One-step moves only.** The table advances a record one named
  stage at a time along the spine; there is no direct
  staged→promoted move for code to request.
- **Actor validation with the automated ceiling.** Actor
  classification is `claim_stage`'s own (`is_automated_actor`,
  reused, not redefined — C094-12's rule against a second actor
  vocabulary). An automated actor may only effect transitions whose
  mapped stages are both at or below the checked rank; any
  transition touching a stage above checked requires a named human.
- **Reasons.** A backward (demotion) move requires a recorded
  reason, and so does a lateral move into a terminal status
  (rejection, expiry).
- **Evidence.** Advancing into a stage above checked requires
  non-empty evidence references.
- **Trail.** Every transition appends one entry to the record's
  append-only `review_history` (from/to status, from/to stage,
  actor, timestamp, evidence refs, reason). The trail field is new
  on transitioned records; records that never transition carry none,
  and the service never stamps claim-stage cache fields onto anchor
  records — the mapping is the service's rule parameter, not record
  state (C094-12).

The routes now call the service, passing the most truthful actor
identity each route holds: approve and promote pass the record's
recorded `approver` (the identity the Stage 1 gate admitted);
verify (verify-archive, cleanup) passes the record's recorded
`verification_evaluator` (the Stage 3 evaluation's author); reject
and re-stage pass `staging_action`; the manual archive passes
`staging_archive`; lifecycle expiry passes `research_loop` — an
automated actor admitted for exactly that move because expiry is
created-rank on both sides of the mapping. Archival bookkeeping
(`archived_at` / `archived_reason`) is a stamp the service performs
after validating the record is archivable and the actor may stamp
at that record's rank, and it leaves its own trail entry; a
verify-then-archive therefore carries two entries (the transition
and the stamp), which the tests assert exactly.

Creation and removal are not transitions and do not pass through
the service, stated plainly so the closure's scope is exact: the
pipeline's staging write creates new records (staged, or blocked
when the candidate cannot be scored) and carries existing records
verbatim — it never rewrites a status; delete and prune remove
records outright.

**T402 — the stores move to the verified-write library.** Every
write of the three anchor-path stores now goes through
`glossa_lab.verified_write.write_file_verified` (Spec 092 Stage
2's library — landed, so the task's successor clause applies and
the older `atomic_io` path was not used): `api/research_loop.py`
gained `_write_staging` / `_write_archive` / `_write_anchors`
helpers over one `_write_store`, and the pipeline's `_save_staging`
writes through the library directly. What the library gives, stated
precisely: the payload is written to a temporary file in the
target's own directory, the target's mode is applied to the temp
file before rename, the write is flushed and fsynced, the temp
file is read back and its SHA-256 verified **before** the rename,
the rename is `os.replace` (atomic on the same filesystem), the
directory is fsynced best-effort, and the renamed file is read back
again; empty content is refused, parent directories are never
created, transient failures retry on a bounded ladder whose
fresh-subprocess leg engages only on the write-denial signature
(EPERM/EACCES or read-back mismatch), and every failure surfaces as
the one typed error `VerifiedWriteError`. What C094-11 does **not**
add: no read-back hash verification of the stores beyond what the
library itself performs — the claim is the move onto the library,
not a new verification layer.

**T403 — the storage-edit probe re-run.** §4 below; the original
verdict reproduces exactly against the built shape, and the outcome
is handled per C094-10 as designed in Stage 0.

## §1 — The stage-vocabulary mapping (T401's question, answered)

The anchor path's statuses map onto the claim-stage ranks as
follows (pinned as data in `anchor_transition.ANCHOR_STAGE_MAP`
and asserted exactly by test):

| anchor status | claim stage | why |
|---|---|---|
| `staged` | created | proposed, not yet examined |
| `blocked` | created | proposed and unscorable — still unexamined |
| `approved` | checked | a named human examined it and passed the Stage 1 gate |
| `verified` | explained | the Stage 3 evaluation gives the grounds |
| `promoted` | accepted | entered the anchors register |
| `rejected` | created | examined and refused; nothing accepted stands behind it |
| `expired` | created | a stale rejection aged out; nothing accepted stands behind it |

`digested` is **deliberately unmapped**. Digestion is independent
scholarly engagement with a claim — the anchor path never performs
it, and promotion is acceptance into the register, not digestion.
Mapping `promoted` to `digested` would let an anchor-path act claim
a scholarly act it did not perform, so no anchor status maps there,
and the automated ceiling therefore binds at the explained rank on
this path.

The allowed transition table (one-step moves; terminal statuses
have no outgoing moves): staged/blocked → {approved, rejected};
approved → {verified, promoted, rejected, staged};
verified → {promoted, rejected, staged, verified};
rejected → {staged, expired}; promoted/expired → {}. The single
same-status move, verified → verified, exists for the cleanup
route's archival bookkeeping on already-verified records and is
admitted explicitly, not by a general no-op rule.

## §2 — T401 census (no direct writes remain)

Method: package-wide greps over `backend/glossa_lab/` on the built
tree, plus two census tests in the new battery that re-run the same
censuses mechanically.

- `record["review_status"] = …` assignments outside
  `anchor_transition.py`: **zero**.
- `"review_status":` literals (record creation) occur only in
  `pipelines/research_loop.py` — the four creation sites of new
  staging records (each creating its record as staged, or blocked
  on a reading conflict). Creation is not a transition
  (§"What was built").
- Every route that changed a status before this stage
  (`staging_action`, `_run_anchor_lifecycle`, `archive_staging`,
  `cleanup_staging`, `staging_verify_archive`,
  `promote_to_anchors`) now routes through the service; the route
  tests assert the trail entries each route leaves.

The closure is **path-scoped**, as C094-10 states: it binds the
routes by which a staged candidate becomes, or fails to become, an
anchor. Writers of the anchors file that are not on that path were
not changed and are named here so the scope is auditable:
`api/foundation_check.py`'s M267 auto-fix (rewrites one anchor's
confidence in place; no status, no lifecycle act);
`pipelines/phase109_followthrough.py`'s `write_anchors_file` and
the `phase113/115/117/118` run scripts' direct anchors writes
(historical phase-run machinery, not routes a candidate travels);
`backend/scripts/_cleanup_stale.py` (a standalone operator script
that filters staging entries; changes no status). None of these is
a route by which a staged candidate becomes an anchor.

## §3 — T402 census (every drafting-census write site re-proven)

The drafting census (`records/commission-and-grounding-2026-11-13.md`
§3) counted 12 truncating `Path.write_text` sites in
`api/research_loop.py`: six staging writes (staging_action,
lifecycle, archive_staging, prune, cleanup, verify_archive), five
archive writes (lifecycle, archive_staging, cleanup,
verify_archive, promote), one anchors write (promote). A thirteenth
anchor-path site sits outside that file: the pipeline's
`_save_staging` staging write.

Exit census on the built tree: `write_text` against any of the
three stores (`_STAGING_JSON`, `_ARCHIVE_JSON`, `_FA_PATH`,
`_STAGING_ARCHIVE_JSON`) occurs **nowhere** in the package, and
`api/research_loop.py` contains no `.write_text(` call at all. (The
pipeline module retains a `write_text` for
`outputs/partial_loop_result.json`, which is not one of the three
stores.) The write-failure behaviour is proven by test per store: a
simulated `os.replace` failure (ENOSPC, so the denial-signature
subprocess leg does not engage) raises `VerifiedWriteError` and
leaves the store byte-identical, and a route-level write failure
surfaces as HTTP 500 with the staging file unchanged.

## §4 — T403 probe outcome (verbatim summaries)

The probe of record (Stage 0 record §6) re-ran against the built
shape, in a disposable copy of this branch's tree (never the live
stores): one ledger claim
(`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`,
line 1 of `glossa-indus/ledger/claims.jsonl`) flipped by bare file
edit from stage `created` to `digested` — no stage_history entry,
no named human, no evidence; the edit touched exactly that one
line. The ledger gate then read:

- `--all`: `summary: 18 PASS / 10 FAIL / 2 NOT-RUN` — `RESULT: FAIL`
- `--regen`: `summary: 18 PASS / 13 FAIL / 1 NOT-RUN` — `RESULT: FAIL`

These are the original probe's readings exactly, in both modes.
Every failing check is a cross-store consistency check — V2 count
equivalence, V3 matrix recomputation, V5 map recomputation (×2),
V7 lossless regeneration (×3, regen mode), V8 settling canonicals,
V10 program-map equivalence (×4), V11 run-binding. No check
validates the transition itself; none was added by this stage.

Handling, per C094-10 as designed in Stage 0: the outcome is filed
here and the path-scoped cap applies. The claims ledger's
protection remains post-hoc divergence detection — unchanged by
this spec, by design — while the anchor path's transitions, which
had neither gate nor net, are now closed at the code-path level by
T401. A bare file edit bypasses any code-path service by
construction; that is exactly why C094-10 binds code paths and
claims nothing more. The full battery re-run is Stage 5's act
(T501), not this stage's.

## Verification (this worker's runs, on the mini-server)

- New battery `tests/test_spec094_stage4_lifecycle_routing.py`:
  **19 passed** (mapping pinned as data; the forward spine one step
  at a time with its trail; outside-table transitions do not exist;
  the automated ceiling both ways; reason requirements; the
  evidence requirement; refusals change nothing; archive-stamp
  rules; route-level trails for approve, reject-refusal,
  verify-archive, cleanup, lifecycle expiry, promote, manual
  archive; per-store write-failure byte-identity; the route-level
  500; both censuses).
- Targeted batteries (Stage 1 + Stage 2 + Stage 3 +
  staging-action integrity + promotion integrity + promotion
  evidence + verified-write): **93 passed**. No existing fixture
  needed conforming this stage — the transitioned records gain a
  trail field and nothing existing changed shape.
- Full backend suite, CI invocation (GPU files ignored; the
  phase392 deterministic test deselected locally by its plain
  nodeid — CI is authoritative for it), two parts split at
  `tests/test_spec086_ledger_gate.py`:
  - part 1: `2826 passed, 64 skipped, 1 deselected` in 200.22s
  - part 2: `23 passed, 44 skipped` in 35.39s
  - union: 2,958 collected — **2,849 passed, 108 skipped,
    1 deselected, 0 failed**.
- Ledger gate from this clone, run sequentially on a quiet tree:
  - `--all`: `summary: 29 PASS / 0 FAIL / 1 NOT-RUN` — `RESULT: PASS`
  - `--regen`: `summary: 32 PASS / 0 FAIL / 0 NOT-RUN` — `RESULT: PASS`
- Ruff on all changed files: clean.

## Claims discharged by this stage

- **C094-10** — anchor-path status transitions route through the
  single gated service of §1–§2, carrying the transition
  guarantees; direct writes are removed and the removal is
  census-proven. The closure is path-scoped, as the claim states.
- **C094-11** — the three anchor-path stores are written only
  through the verified-write library (§3); every drafting-census
  site is re-proven absent, and a simulated write failure leaves
  each store byte-identical under `VerifiedWriteError`.
- **D-094-5 (stage-4 exit gate)** — the storage-edit probe re-ran
  against the built shape and its outcome is filed at §4, handled
  per C094-10.

## Deviations and notes

- No existing-test fixtures were updated (Stages 1–3 each conformed
  fixtures; Stage 4 changes no existing record shape — transitioned
  records gain `review_history`, an additive field).
- The out-of-path anchors writers named in §2 were left unchanged
  by design; the stage record names them rather than widening the
  closure past the claim's scope.
- The ssh route to the mini-server dropped mid-command several
  times during this stage; every long run (gate modes, suite parts)
  ran detached with a log file and was read back from its log, so
  no reading rests on a dropped connection.
