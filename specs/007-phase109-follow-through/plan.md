# Plan 007 — Phase-109 Follow-Through (executing the Phase-108 recommendations)

## Branch / commits

Branch `feat/phase109-follow-through` from main (1d25d01d). One
commit per step, plus this proposal commit and a close-out commit.
Commit after every step (a predecessor package lost its coordinator
to a runtime restart; banked commits are the recovery mechanism).
PR to main via `gh pr create`; NOT merged (owner review).

## Shared machinery

Library: `backend/glossa_lab/pipelines/phase109_followthrough.py`
- Loaders: anchors file (current + the three backup snapshots),
  Phase-108 register + trails, crosswalk v2.1, staging archive.
- Evidence assembly per cohort anchor (Step 1): current entry,
  register components, snapshot readings/confidences/full entries,
  crosswalk record, ledger mentions, archive entries.
- Decision rules (spec 007 Step 1 (a)/(b)/(c); Step 3 caps) as
  pure functions over the assembled evidence — unit-tested on
  synthetic records (`backend/tests/test_phase109_followthrough
  .py`), reusing `provenance_audit.normalize_reading` /
  `first_segment` for the A1 match.
- Change application: deterministic rewrite of the anchors file
  (entries in file order preserved; only named entries touched),
  `phase109_annotation` stamping, cumulative change-register
  read/append/write (`reports/phase109_change_register.json`).
- Recomputation (Step 5): Phase-108 methods reused via
  `pipelines/provenance_audit.py` (`token_coverage`,
  `phonotactic_check`, `parpola_agreement`, `site_invariance`,
  `load_holdat_tokens`) over the post-change file + register
  classes; bookkeeping regeneration per spec 004 WS3.

Scripts (H23: written + graph-registered BEFORE first run). Each
has `decide` (default) and `apply` modes:
- `backend/scripts/phase109_step1_staging_review.py` — Step 1
  decisions → `reports/phase109_step1_decisions.json`; apply →
  anchors + change register.
- `backend/scripts/phase109_step2_sa_flags.py` — Step 2 flags →
  `reports/phase109_step2_flags.json`; apply likewise.
- `backend/scripts/phase109_step3_rereviews.py` — Step 3 dossiers
  → `reports/phase109_dossier_M293.json` / `_M362.json` /
  `_M398.json`; apply likewise.
- `backend/scripts/phase109_step5_rebase.py` — Step 5(a)
  recomputation → `reports/phase109_rebase.json`; Step 5(b)
  bookkeeping regeneration in `apply` mode.

Graph: `backend/glossa_lab/experiment_graph_phase109.py`, nodes
`IndusPhase109StagingReview`, `IndusPhase109SaFlags`,
`IndusPhase109Rereviews`, `IndusPhase109Rebase` (subprocess
pattern per the phase108 module, `decide` mode); registered in
`experiment_graph.py` try/except; verified in ATOMIC_NODES before
any script runs.

## Compute budget (H9/H11)

All steps are deterministic text/count work: evidence assembly is
bounded file reads; recomputation is single passes over a
7,002-row CSV plus the Phase-69 χ² machinery on ≤275 signs.
Every script run carries a shell timeout; no unbounded loops.

## Step procedures

### Step 0
Spec + plan + tasks (this commit). No anchor is touched before
the spec lands.

### Step 1
1. Build library + unit tests; scripts + graph + registration in
   the machinery commit, before any run (H23).
2. `decide` run → decisions artifact with per-anchor evidence
   summary + rule fired. Hand-check: every (a), every (c), every
   (b) with snapshot confidence HIGH/MEDIUM, 10 sampled
   (b)-to-LOW. Log any rule/evidence conflict as an edge case in
   the artifact (decided by rule order, cited).
3. `apply` run → anchors file updated; change register updated.
4. Foundation check (H21 — anchor data changed): 0 failures
   required before the step commit.

### Step 2
1. `decide` → flags artifact (44 signs, register citations).
2. `apply` → `validation_status` + `provenance_class` fields on
   the 44; assert no reading/confidence changed (diff check in
   the script).
3. Foundation check; commit.

### Step 3
1. Assemble dossiers (script gathers: anchor entry, register
   record, trail, Phase-116 eval/recal records for M293,
   Phase-101 ledger section, Phase-105 results for M362/M398,
   May-backup tiers, and a post-Phase-105 adjudication search
   over ledgers + reports/ + outputs/ for M362/M398).
2. Apply the registered caps: M293 → highest non-SA-supported
   tier; M362/M398 → at most MEDIUM absent a superseding
   adjudication.
3. `apply` → tier changes + annotations; foundation check;
   commit.

### Step 4
1. API: rename `/staging/verify-sa` handler to
   `/staging/verify-archive`; keep `/staging/verify-sa` as a
   deprecated alias (docstring + log warning) delegating to the
   same function. Update `frontend/src/components/
   ResearchLoopPanel.tsx` to the new path.
2. `/staging/promote`: evidence gate (`evidence_ref` on the
   candidate or `evidence_refs` in the body; blocked candidates
   reported as `blocked_no_evidence`, never written); remove the
   post-promote SA auto-queue block; keep `sa_validation_jobs`
   in the response (always []).
3. Regression tests: `backend/tests/
   test_staging_promotion_evidence.py` — TestClient with the
   module's staging/archive/anchors paths monkeypatched to tmp
   files: promotion without a ref promotes nothing and reports
   the block; with a ref promotes; the new route exists and the
   deprecated alias still responds.
4. Governance: H26 appended to `docs/governance/rules.md`.
5. Foundation texts: the Step-4(c) reframes in
   `backend/scripts/foundation_check.py` (text only; verify by
   diff that no CHECK/WARN logic changed); run the foundation
   check — 0 failures.
6. Commit.

### Step 5
1. `decide` (recompute) → `reports/phase109_rebase.json`:
   post-change sets (full H+M; strict SA-independent H+M) with
   counts by tier, token coverage, phonotactics, Parpola
   (Phase-108 method + caveat), site invariance.
2. README edits (status block, §Indus Script Decipherment,
   Current research status) from the artifact's numbers + the
   dated re-base note.
3. `apply` (bookkeeping) → anchors summary fields regenerated;
   `_phase109_note` added; foundation check.
4. Preprint addendum draft (`glossa-corpus/indus/pierson_2026_
   indus_decipherment_addendum_v5.md`, DRAFT banner) +
   PREPRINT_VERSIONING.md draft row.
5. Commit.

### Step 6
1. Full backend suite (exact counts vs 586/9 baseline); ruff on
   changed Python.
2. Final foundation check (0 failures; exact totals).
3. Change-register completeness check: diff the anchors file
   against main and assert every differing entry/field is in
   the register.
4. Ledgers (glossa-indus Phase-109 per-step entries appended in
   each step commit; root summary at close-out), tasks.md
   checked off.
5. Push; `gh pr create` (change-register summary in body);
   report. No merge.

## Verification (constitution §VIII)

- Exact test counts vs baseline (586 passed / 9 skipped).
- Foundation check 0 failures at every anchor-touching step and
  at close-out (H21); exact pass/warn totals reported.
- Every number in the README re-base, the rebase artifact, and
  the PR body traces to `reports/phase109_*` artifacts computed
  from the post-change anchors file.
- Change register ↔ anchors diff completeness (Step 6.3).
