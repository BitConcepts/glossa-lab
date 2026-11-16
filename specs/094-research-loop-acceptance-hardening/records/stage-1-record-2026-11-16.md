# Spec 094 — Stage 1 record (record schema and the approval gate)

**Stage:** 1 — Record schema and the approval gate (C094-1..3)
**Date:** 2026-11-16
**Base:** `cc9f132a2eda8b11d3f3051f19c9516cbf5cd98c` (origin/main, the
Spec 092 Stage 2 merge)
**Branch:** `spec/094-s1-approval-gate`
**Tasks discharged:** T101, T102. **Also ticked:** T004 (evidence
below — the act was already of record; only the box was unticked).
**Claims discharged:** C094-1, C094-2, C094-3 (on the evidence named
per claim below).

Nothing in this stage touched the live backend or its stores: all
work ran in a fresh clone on the mini-server against synthetic
fixtures, the research loop was never run, and no live store was
read or written (C094-13 held throughout).

## What was built

### T101 — Candidate record fields (C094-3)

- `backend/glossa_lab/claim_stage.py` gains
  `CANDIDATE_GATE_FIELDS = ("falsifier", "approver", "evidence_ref")`:
  the gate inputs are named in one place, as first-class fields of
  the candidate record.
- The pipeline's staging write
  (`backend/glossa_lab/pipelines/research_loop.py::_save_staging`)
  is the carrier: every newly staged candidate record is written
  with all three fields present (`setdefault`, so a value a
  producer already set is carried, never overwritten). They start
  empty — the pipeline stages candidates, it does not adjudicate
  them — and a record carrying no falsifier or approver is
  unapprovable until adjudication records them.
- Records already in the staging file are not rewritten by the
  staging write, and nothing in this stage migrates existing
  records (C094-12): pre-gate records stay exactly as they are.

### T102 — Approve-route enforcement (C094-1, C094-2)

- The D-094-1 named-humans list lives in `claim_stage.py`, beside
  the actor rules' own allowlist (`AUTOMATED_ACTORS`), as
  `NAMED_HUMAN_APPROVERS = {"tristen_pierson"}` (normalized form;
  initially the owner alone, per D-094-1 as adopted). It is not a
  new registry: D-094-1 fixes the list's home as wherever the actor
  rules already read their allowlist from, or beside it.
  `is_listed_approver()` validates an actor as a named human under
  the existing `claim_stage` rules (`is_named_human`, reused, not
  redefined) AND requires list membership.
- `backend/glossa_lab/api/research_loop.py` gains
  `_approval_gate_refusal(candidate)`: the single gate check every
  route below shares. It reads only the candidate record and
  refuses when (a) the record's falsifier is missing or empty,
  (b) the record's approver is missing or empty, (c) the recorded
  approver is an automated identity under the `claim_stage` rules,
  or (d) the recorded approver does not validate as a listed named
  human.
- **Approve** (`staging_action`): after the existing state guard,
  the gate check runs on the matched record before any write; a
  refusal returns the endpoint's established shape
  (`{"ok": False, "error": ...}`) and changes nothing. The request
  body is never consulted for gate inputs — falsifier/approver keys
  in an approve request are ignored, so a gate decision taken from
  request-only data is refused by construction.
- **Verify** (`staging_verify_archive` and its deprecated
  `staging_verify_sa` alias; `cleanup_staging`'s approved→verified
  flip): records that fail the gate are not verified. They stay in
  staging with their status untouched and are reported in the new
  `blocked_no_approval_gate` response field; when every approved
  candidate is blocked, verify-archive refuses (`ok: False`) and
  writes nothing.
- **Promote** (`promote_to_anchors`): after the existing membership
  and H26 evidence gates, a record that fails the approval gate is
  refused and reported in the new `blocked_no_approval_gate`
  response field. This is the enforcement of C094-12/D-094-6 for
  the C094-1 fields: the pre-gate archive stock keeps its recorded
  status as history but cannot promote until its records carry the
  gate fields. (The C094-4/C094-5 evidence pin and class remain
  Stage 2's charge, untouched here.)

## Design choices taken inside the adopted decisions

1. **List placement (D-094-1).** The decision leaves the list's
   home to the stage record: it lives in `claim_stage.py` beside
   `AUTOMATED_ACTORS`, the allowlist the actor rules already read,
   with membership matched in the same normalized form.
2. **Verify/promote enforcement shape.** The verify and promote
   routes carry no actor of their own; the identity a transition is
   attributable to is the approver recorded on the candidate
   record. Stage 1 therefore enforces C094-2 on those routes at
   the record: a record whose recorded approver is automated (or
   absent, or unlisted) cannot be verified or promoted. This is
   the only reading under which "automated identities are refused
   for approve, verify, and promote" (T102) is enforceable on the
   built surface without inventing request-supplied actors — which
   C094-3 forbids as gate inputs.
3. **Gate order at promote.** The approval gate runs after the
   membership and H26 evidence gates, so the established blocked
   lists keep their meanings and the new list names exactly the
   records that passed every earlier gate and failed this one.
4. **Boundary with Stage 3.** `_run_anchor_lifecycle`'s
   flat-delta auto-verification is C094-7's object and is NOT
   touched here; it is removed at Stage 3 (T301). C094-2 is
   discharged on the endpoint surface — approve, verify, and
   promote are the routes an identity can drive — and C094-13
   keeps the loop off the live stores until closeout, so the
   lifecycle construction cannot reach a live verify transition
   in the interim.

## Test actuals

New battery: `backend/tests/test_spec094_stage1_approval_gate.py`
(15 tests) — actor-rule units (list shape, `is_listed_approver`
incl. normalization, allowlist/process-token and
`actor_kind="automated"` refusals); staging-write coverage (fields
carried on every newly staged record, producer values preserved,
pre-existing records not rewritten); probe (a) in its original
variant (no falsifier on the record: refused, file byte-identical)
and its automated-actor variant (recorded approver
`research_loop`: refused, file byte-identical); request-only gate
data refused by construction; unlisted named human refused;
missing approver refused; conforming approvals from `staged` and
`blocked` carry all three record fields; verify-archive refuses an
ungated record outright and partitions a mixed batch; cleanup does
not verify an ungated record; promote refuses an ungated record
and promotes a conforming one.

Targeted run (the new battery plus the three pre-existing
integrity batteries), CI invocation and environment, local:
**38 passed** (15 new + 7 staging-action + 11 promotion-integrity
+ 5 promotion-evidence).

Full backend suite, CI invocation (GPU files ignored) with the
one local deselect noted in Deviations — completed locally in two
parts (see Deviations for why):

- Part 1 (the whole suite as one run, stopped inside
  `tests/test_spec086_ledger_gate.py`): every file before that
  file completed (2,250 tests), plus ~50 tests into it — with no
  failure or error anywhere in the run's progress record (2,216
  passes and 84 skips counted from that record).
- Part 2 (the 35 files from `test_spec086_ledger_gate.py` onward,
  same invocation and environment): **650 tests — 585 passed, 65
  skipped, 0 failed** (697.10s). A parallel re-run of the 29
  non-Spec-086 files among them independently returned 519
  passed, 1 skipped, 0 failed.

Ruff on all changed files: clean.

## Existing-test fixture updates (named, per the stage's effect)

The gate changes what a conforming candidate record is, so three
pre-existing fixtures were updated to the conforming adjudicated
shape (recorded falsifier + approver "Tristen Pierson"); no
assertion in them was weakened and their defect coverage is
unchanged:

- `tests/test_staging_action_integrity.py` — `_candidate()` gains
  falsifier/approver/evidence_ref (its approve legs now approve a
  gate-carrying record; the state-guard and rejection-history
  assertions are untouched).
- `tests/test_promotion_integrity.py` — `_candidate()` gains
  falsifier/approver (its refusal tests still refuse on their own
  earlier gates: skip, membership, mismatch).
- `tests/test_staging_promotion_evidence.py` — `_candidate()` and
  the verify-archive test's inline candidate gain
  falsifier/approver, so the H26 evidence gate remains the
  deciding gate in those tests.

## Ledger gate (this tree, before push)

- `tools/ledger/check_ledger_gate.py --all`:
  `summary: 29 PASS / 0 FAIL / 1 NOT-RUN` — `RESULT: PASS`
- `tools/ledger/check_ledger_gate.py --regen`:
  `summary: 32 PASS / 0 FAIL / 0 NOT-RUN` — `RESULT: PASS`

Both hold the standing profile exactly. (Local gate runs are
recorded here as stage evidence; no CI claim is made from them —
the PR's CI read is the parent's gate.)

## T004 — ticked on evidence already of record

T004's act was executed 2026-11-13 as intake PR #567, separate
from the adoption PR, exactly as the task prescribes; the box was
simply never ticked. Verified on this tree (base `cc9f132a`):

- `glossa-indus/map/program-map-taxonomy.json` assigns
  `094-research-loop-acceptance-hardening` (spec_dir entry).
- `glossa-indus/ledger/claims.jsonl` carries all 13 claims as
  `094-research-loop-acceptance-hardening/C094-1` …
  `/C094-13`, and the generated layers were regenerated over the
  grown ledger in that act (the ledger gate above passes on the
  result).

## Claims discharged

- **C094-1** — approval requires a recorded non-empty falsifier
  and a listed named-human approver: enforced at `staging_action`
  and proven by probe (a)'s original variant, the unlisted-human
  and missing-approver refusals, and the conforming approvals.
- **C094-2** — automated identities refused for approve, verify,
  and promote: probe (a)'s automated-actor variant at approve;
  record-level refusal at verify-archive, verify-sa, cleanup, and
  promote. Boundary stated in design choice 4.
- **C094-3** — gate inputs live on the record: the fields are
  first-class and carried by the staging write; the
  request-only-data test shows a decision offered only in the
  request is refused by construction.

## Deviations

- The full local suite deselects
  `tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  by its plain nodeid, per the standing local-run discipline for
  that environment-sensitive test; CI is authoritative for it. No
  CI claim is made from any local run in this record.
- The local full-suite evidence was gathered in two parts: as one
  run, the suite crawls inside `tests/test_spec086_ledger_gate.py`
  on this box (its tests re-run the ledger gate machinery against
  the real tree; a single standalone full-mode gate pass takes
  ~2.5 minutes here) and was stopped after completing every
  earlier file with no failure or error in its progress record;
  the remaining 35 files were then run as a second invocation
  with an identical environment. The union covers all 2,900
  collected tests. This is a local-hardware artifact of the Spec
  086 gate tests, not a finding about this stage's changes (which
  do not touch the ledger machinery, and whose own gate runs
  above pass with the standing profile).
- No other deviations. Scope held to T101 + T102 exactly: no
  Stage 2–5 work, no change to `_run_anchor_lifecycle`, no change
  to the anchor-set surface, no live-store access.
