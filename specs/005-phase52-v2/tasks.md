# Tasks 005 — Phase-52 v2 (Phase-107)

## Proposal
- [x] T001 Read AGENTS.md, constitution, governance rules, spec-004 shape
- [x] T002 Read program-analysis audit + Phase-52/57/58/61/133 sources
- [x] T003 Create branch `feat/phase52-v2` from main ad6de412
- [x] T004 Write specs/005 (spec / plan / tasks) with pre-registered protocol

## Step 1 — Validation harness (current objective)
- [x] T010 Build `pipelines/sa_validation.py` (loaders, gold, folds, SA, terms interface)
- [x] T011 Unit tests `tests/test_sa_validation.py`
- [x] T012 Write phase107 scripts + graph module + registration; verify ATOMIC_NODES (H23)
- [x] T013 Run 1a: 5-fold primary + secondary held-out metrics (baseline)
- [x] T014 Run 1b: pin-count sweep {0, 53, 90, all} on fold 0
- [x] T015 Run 1c: blind controls (Sanskrit, Ge'ez, scrambled) × 5 folds
- [x] T016 Aggregate step1 artifact; discrimination verdict per pre-registered rule

## Step 2 — Constraint ablation
- [ ] T020 Implement phonotactic term (Phase-58/61 rules)
- [ ] T021 Implement vowel-harmony term (Phase-61 definition)
- [ ] T022 Implement positional-grammar term (Phase-133b classes, per-fold profiles)
- [ ] T023 Run ablations in order + combined kept-terms config
- [ ] T024 Aggregate step2 artifact; kept/dropped verdicts per keep rule

## Step 3 — Delta scoring + scaled run
- [ ] T030 Implement delta scorer (LM + kept terms)
- [ ] T031 Equivalence test full vs delta (Claim D criteria)
- [ ] T032 Scaled run 10×10×100K; stability selection (≥0.80 / ≥0.60 tiers)
- [ ] T033 Final consensus decipherment table artifact

## Step 4 — Corpus pooling + acquisition hunt
- [ ] T040 Audit CITATIONS.md ingested sources (no re-fetch list)
- [ ] T041 Convert in-repo CISI subset via crosswalk v2.1; dedupe vs Holdat; pool
- [ ] T042 Hunt: RMRL Mahadevan concordance (download attempt, outcome logged)
- [ ] T043 Hunt: ICIT / CISID / CDLI / Harappa.com / Wells / code hosts / Zenodo-Figshare-OSF / 2025-conference + Dixit datasets / Dilmun-Gulf
- [ ] T044 Ingest obtained corpora as flagged layers + CITATIONS.md entries
- [ ] T045 Re-run Step-1a primary metric on enlarged pool (best objective)
- [ ] T046 Step4 artifact: ingested / not-obtained (blocker) / not-found lists

## Step 5 — Numerals/metrology
- [ ] T050 Extract stroke-numeral family + C3 pattern from named artifacts
- [ ] T051 Evaluate C1 distinctness, C2 order, C3 positional (pass/fail + counts)
- [ ] T052 Step5 artifact

## Step 6 — Close-out
- [ ] T060 Foundation check (0 failures; H21)
- [ ] T061 Full backend test suite (exact counts)
- [ ] T062 Ruff on changed Python files
- [ ] T063 glossa-indus LEDGER Phase-107 entries (per step, AI disclosure)
- [ ] T064 Root LEDGER.md summary entry (AI disclosure)
- [ ] T065 Push branch, open PR (do NOT merge)
