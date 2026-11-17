# Spec 094 — Stage 5 closeout record (full battery, register
amendment, boundary verification; C094-12..13)

- **Stage:** 5 — Closeout (T501, T502)
- **Date:** 2026-11-16
- **Base:** `251423ee6bdf9bd502a417cfb88ca0de1e6981f6` (origin/main,
  the Spec 094 Stage 4 merge, PR #576)
- **Branch:** `spec/094-s5-closeout`
- **Tasks discharged:** T501, T502
- **Claims discharged:** C094-1..13 — every claim, per claim on its
  evidence (§4). On that full discharge, C094-13's loop-off
  protection is lifted by name (§5).

Nothing in this stage touched the live backend or its stores: the
battery re-ran against the built system on scratch stores
(synthetic fixtures, the pattern every stage used), the boundary
verification read the clone's files and the stage PRs' records,
and no loop run of any kind was made against the live stores. The
C094-13 lift in §5 is a governance record in this PR; the first
real loop run after it is a separate operation this stage does
not perform.

## §1 — The full policy probe battery, re-run end to end (T501)

The battery is the union of the four stage probe batteries and
the integrity batteries they build on, run in one invocation
against the built system at this branch's base (CI invocation and
environment; GPU files are not part of this battery; the run's
stores are the batteries' synthetic scratch stores):

| Battery | Tests | Result |
|---|---|---|
| `test_spec094_stage1_approval_gate.py` | 15 | passed |
| `test_spec094_stage2_evidence_standard.py` | 19 | passed |
| `test_spec094_stage3_verification.py` | 18 | passed |
| `test_spec094_stage4_lifecycle_routing.py` | 19 | passed |
| `test_staging_action_integrity.py` | 7 | passed |
| `test_promotion_integrity.py` | 11 | passed |
| `test_staging_promotion_evidence.py` | 5 | passed |
| `test_verified_write.py` | 18 | passed |
| **Union (one invocation)** | **112** | **112 passed, 0 failed** (27.65s, exit 0) |

Per-file counts were read from individual runs of the same
invocation; they sum to the union run exactly. Probes (a) and (b)
in all their variants, the approval/evidence/verification gate
refusals, the lifecycle flip test, both Stage 4 censuses, and the
per-store write-failure byte-identity tests all refuse or hold
exactly as their stage records describe. The storage-edit probe
re-run is not repeated here: it was filed at Stage 4 (that
record's §4, readings reproduced exactly in both gate modes) and
is incorporated by reference, as plan.md's Stage 5 work list
provides.

## §2 — C094-12 boundary verification (T501)

Method: byte-level comparison of the three stores' repo copies
against the adoption-day state in Stage 0's record (read at main
`4d08788f`, 2026-11-13), a census re-read, the ledger state read
from the clone, and a file-list census of every diff this spec
has landed. No live store was read or written for this check.

- **Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
  SHA-256 at the Stage 0 base commit `4d08788f`:
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.
  SHA-256 at this branch's base `251423ee`: the identical digest.
  The file is byte-identical to adoption day. Census re-read:
  **287 anchors** (the file's own `total` field agrees), HIGH
  166 · MEDIUM 5 · LOW 3 · CANDIDATE 113 — Stage 0's census
  exactly. No pre-existing anchor's reading or confidence moved.
- **Staging (repo copy).** SHA-256
  `42456ef9bf0e54590c17501f07c652557c733b9f9b0102967883b5040bb0aabe`,
  **52 items** — byte-identical to Stage 0's recorded value.
- **Archive (repo copy).** SHA-256
  `5450df76735a77e86e4b682189bf209fcc1f7df38e9e1a9a88109e51fc6c6283`,
  **1,047 entries** — byte-identical to Stage 0's recorded value.
- **Stage-diff census.** The file lists of the four stage PRs
  (#573, #574, #575, #576) contain only backend code
  (`api/research_loop.py`, `claim_stage.py`,
  `pipelines/research_loop.py`, `evidence_standard.py`,
  `verification.py`, `anchor_transition.py`), backend tests, and
  this spec's own records and tasks file. No store path, no
  ledger path, no generated-layer path, and no claim-record path
  appears in any stage diff; this closeout's own diff (the
  register amendment, this record, the tasks ticks) adds none
  either.
- **Ledger.** `glossa-indus/ledger/claims.jsonl` stands at 1,025
  lines; C094-1..13 are all present and every one stands at stage
  `created`, status `draft` — exactly as the T004 intake appended
  them, unmoved by any act under this spec. The ledger gate holds
  its standing profile on this tree (§6).
- **Pre-gate stock, restated with its suspension in force**
  (Stage 0's inventory, unchanged by any stage): live archive
  1,107 entries (58 `approved` · 1,025 `verified` · 24
  `promoted`), repo archive 1,047; the endpoint-promotable pool
  is 104 distinct signs. Under D-094-6 every pre-gate entry keeps
  its recorded status as history and **cannot promote until
  re-evidenced onto the Stage 1–2 record fields** — and the
  battery (§1) re-proves the built gates enforce exactly that:
  ungated records refuse at approve, verify, and promote, and a
  bare `verified` status with no recorded evaluation caps at LOW.

## §3 — GR-088-05 amendment (T501)

Appended to the GR-088-05 entry in
`glossa-indus/map/gap-register.md`, in the register's own
amendment style (a bold-headed paragraph at the entry's end; the
original entry text is untouched — the diff is 29 insertions,
0 deletions; the register file's SHA-256 after amendment is
`ec7cf3bb86501385cd1120a42e8c1bbacab67dc3324f32c6ed9ee34a62685fb3`).
The amendment records that the cross-cutting spec the entry
called for exists as this spec, and that it closes the gap **for
the anchor path only**: transitions there route through the
gated transition service and the three stores are written only
through the verified-write path. It states the remainder
plainly — the claims ledger and every other writer remain as
they were, resting on writer discipline backed by post-hoc
cross-store divergence detection — and it carries the required
cap verbatim: *"This amendment does not establish closure of
GR-088-05 beyond the anchor path."*

## §4 — Per-claim discharge (T502)

- **C094-1 — DISCHARGED** (Stage 1, PR #573). Approval requires a
  recorded non-empty falsifier and a listed named-human approver,
  enforced at `staging_action`; probe (a)'s variants refuse and
  conforming approvals carry the fields. Battery re-run at
  closeout: the Stage 1 battery (15) passes.
- **C094-2 — DISCHARGED** (Stage 1, PR #573). Automated
  identities are refused for approve, verify, and promote —
  at approve directly, at verify and promote at the record.
  Battery re-run: Stage 1 battery passes.
- **C094-3 — DISCHARGED** (Stage 1, PR #573). Falsifier, approver,
  and evidence are first-class record fields carried by the
  staging write; a gate decision offered only in the request is
  refused by construction. Battery re-run: Stage 1 battery passes.
- **C094-4 — DISCHARGED** (Stage 2, PR #574). Promotion evidence
  is pinned by SHA-256 on the record at pin time; promotion
  verifies the bytes and refuses on absence, mismatch, or a pin
  created by the promote request itself. Battery re-run: the
  Stage 2 battery (19) passes.
- **C094-5 — DISCHARGED** (Stage 2, PR #574). The registered
  class list is landed with its four ratified classes; loop or
  anchor-path output about the candidate refuses as a class at
  registration, at pin time, and at promotion. Battery re-run:
  Stage 2 battery passes.
- **C094-6 — DISCHARGED** (Stage 3, PR #575). "Verified" is a
  recorded per-candidate evaluation by a named human, citing
  per-candidate evidence; run-level citations refuse at recording
  and at every gate. Battery re-run: the Stage 3 battery (18)
  passes.
- **C094-7 — DISCHARGED** (Stage 3, PR #575). The `sa_delta = 0.1`
  construction and the approved → verified flip are removed from
  `_run_anchor_lifecycle`, demonstrated from the code before and
  after; a lifecycle run over approved candidates under a clean
  foundation check flips nothing, and the expiry duty is
  unchanged. Battery re-run: Stage 3 battery passes.
- **C094-8 — DISCHARGED** (Stage 3, PR #575). Promotion confers
  MEDIUM exactly on candidates verified under C094-6; unverified
  caps at LOW at score 0.99, and a `verified` record carrying no
  evaluation caps at LOW. Battery re-run: Stage 3 battery passes.
- **C094-9 — DISCHARGED** (Stage 3, PR #575). The fabricated
  fallback was demonstrated from the code (score 0.9 → `sa_delta`
  0.108) and removed; no surface carries an `sa_delta` for a
  candidate with no recorded comparison, and a recorded delta is
  carried as recorded. Battery re-run: Stage 3 battery passes.
- **C094-10 — DISCHARGED** (Stage 4, PR #576). Every anchor-path
  status transition routes through the single gated transition
  service; the census proves zero direct `review_status` writes
  remain outside it. The closure is path-scoped, as the claim
  states. Battery re-run: the Stage 4 battery (19) passes.
- **C094-11 — DISCHARGED** (Stage 4, PR #576). The three
  anchor-path stores are written only through the verified-write
  library; every drafting-census write site is re-proven absent,
  and a simulated write failure leaves each store byte-identical
  under `VerifiedWriteError`. Battery re-run: Stage 4 battery and
  the verified-write battery (18) pass.
- **C094-12 — DISCHARGED** (Stage 5, this record §2). No diff
  under this spec altered any pre-existing anchor entry, claim
  record, or ledger entry — proven byte-for-byte against the
  adoption-day state — and the pre-gate stock's promotability
  suspension stands in force until re-evidenced.
- **C094-13 — DISCHARGED** (Stage 5, this record §5). The bar
  held for the spec's whole life: Stage 0 observed the live loop
  off with 0 cycles, and every stage record states no loop run
  touched the live stores (scratch instances only). On the full
  discharge of C094-1..12 above, the protection is lifted by name
  in §5.

## §5 — C094-13 lifted by name (T502)

On the full discharge of C094-1..13 recorded in §4, **the
loop-off protection of C094-13 is lifted by name**: the research
loop may run against the live anchor-path stores under the
landed gates, as ordinary operations. This record performs no
loop run and approves none: any later loop run is ordinary
operations under the landed gates, judged on its own record
(T502's own cap).

## §6 — Verification (this worker's runs, on the mini-server)

- Full policy probe battery (§1): **112 passed, 0 failed** in one
  invocation (27.65s, exit 0); per-file counts sum to the union
  exactly.
- Full backend suite, CI invocation (GPU files ignored; the
  phase392 deterministic test deselected locally by its plain
  nodeid — CI is authoritative for it), two parts split at
  `tests/test_spec086_ledger_gate.py`:
  - part 1: `2826 passed, 64 skipped, 1 deselected` in 611.56s
    (exit 0)
  - part 2: `23 passed, 44 skipped` in 578.26s (exit 0)
  - union: 2,958 collected — **2,849 passed, 108 skipped,
    1 deselected, 0 failed** — Stage 4's union exactly, as
    expected: this stage changes no code.
- Ledger gate from this clone, run sequentially on a quiet tree
  with the register amendment in place:
  - `--all`: `summary: 29 PASS / 0 FAIL / 1 NOT-RUN` — `RESULT: PASS`
  - `--regen`: `summary: 32 PASS / 0 FAIL / 0 NOT-RUN` — `RESULT: PASS`
  Both hold the standing profile exactly; the register amendment
  did not move either mode's numbers.
- Ruff: this stage's diff changes no Python file (the register
  amendment, this record, and the tasks ticks are the whole
  diff), so there is no changed Python file for ruff to check;
  the ruff claim is vacuous, stated rather than skipped silently.

## Deviations and notes

- The register amendment was applied on the box by a
  self-verifying insertion (anchor asserted to occur exactly
  once, the result proven purely additive, written via temp file
  and `os.replace`, hash read back on both sides) instead of the
  fetch-edit-return route: a VM write wave (the standing EPERM
  defect; the wave probe read WAVE at the time) blocked the local
  download the fetch route needs. The resulting `git diff` —
  29 insertions, 0 deletions, in the GR-088-05 entry only — is
  the verification of record.
- The full local suite ran in two parts split at
  `test_spec086_ledger_gate.py`, and deselects the phase392
  deterministic test by its plain nodeid, per the standing
  local-run discipline; CI is authoritative for it. No CI claim
  is made from any local run in this record.
- No other deviations. Scope held to T501 + T502 exactly: no code
  change, no live-store access, no loop run, no backend restart.
