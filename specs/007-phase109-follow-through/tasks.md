# Tasks 007 — Phase-109 Follow-Through (Phase-108 recommendations, executed)

## Proposal
- [x] T001 Read AGENTS.md, constitution, governance rules, Phase-108 summary/register/impact map
- [x] T002 Survey evidence landscape (anchors + backups, staging archive, endpoint code, README/preprint surfaces, foundation texts)
- [x] T003 Create branch `feat/phase109-follow-through` from main 1d25d01d
- [x] T004 Write specs/007 (spec / plan / tasks) with pre-registered decision rules (Steps 1–4), re-base targets (Step 5), acceptance checks (Step 6)

## Machinery (H23 — before any script runs)
- [x] T010 Build `pipelines/phase109_followthrough.py` (loaders, evidence assembly, decision rules, change application, register)
- [x] T011 Unit tests `tests/test_phase109_followthrough.py`
- [x] T012 Write phase109 scripts (step1/step2/step3/step5) + graph module + registration; verify ATOMIC_NODES

## Step 1 — Staging-cohort re-review (116)
- [x] T013 Decide run → `reports/phase109_step1_decisions.json` ((a)/(b)/(c) per anchor with evidence)
- [x] T014 Hand-check every (a) and (c), every (b) at HIGH/MEDIUM snapshot confidence, 10 sampled (b)-to-LOW
- [x] T015 Apply → anchors + change register; list every (b) restoration
- [x] T016 Foundation check (0 failures; H21)

## Step 2 — SA-lineage HIGH flags (44)
- [x] T020 Decide run → `reports/phase109_step2_flags.json`
- [x] T021 Apply → `validation_status` + `provenance_class` on the 44; assert no value/tier change
- [x] T022 Foundation check

## Step 3 — Individual re-reviews (M293, M362, M398)
- [x] T030 Dossiers → `reports/phase109_dossier_M293.json` / `_M362.json` / `_M398.json` (incl. post-Phase-105 adjudication search for M362/M398)
- [x] T031 Apply registered caps (M293 → highest non-SA-supported tier; M362/M398 → at most MEDIUM)
- [x] T032 Foundation check

## Step 4 — Promotion-path + governance fixes
- [ ] T040 Rename `/staging/verify-sa` → `/staging/verify-archive` (+ deprecated alias); frontend/src updated
- [ ] T041 `/staging/promote` evidence gate (`evidence_ref` / `evidence_refs`); remove post-promote SA auto-queue
- [ ] T042 Regression tests `tests/test_staging_promotion_evidence.py` (no-ref fails, with-ref succeeds, routes)
- [ ] T043 H26 added to `docs/governance/rules.md`
- [ ] T044 Foundation-check text retirements (Phase-52/57/67/73 + Phase-44 mislabel; text only); foundation check 0 failures

## Step 5 — Headline re-base
- [ ] T050 Recompute → `reports/phase109_rebase.json` (post-change sets: counts, coverage, phonotactics, Parpola + caveat, site invariance)
- [ ] T051 README re-base (status block, §Indus Script Decipherment, Current research status) + dated re-base note
- [ ] T052 Anchors bookkeeping regenerated (spec 004 WS3 method) + `_phase109_note`; foundation check
- [ ] T053 Preprint addendum v5 DRAFT in-repo + PREPRINT_VERSIONING.md draft row (no submission)

## Step 6 — Close-out
- [ ] T060 Full backend test suite (exact counts vs 586/9 baseline)
- [ ] T061 Ruff on changed Python files
- [ ] T062 Change-register completeness vs anchors diff to main
- [ ] T063 glossa-indus LEDGER Phase-109 entries (per step, AI disclosure)
- [ ] T064 Root LEDGER.md summary entry (AI disclosure)
- [ ] T065 Push branch, open PR with change-register summary (do NOT merge)
