# Plan 005 — Phase-52 v2 (Phase-107)

## Branch / commits

Branch `feat/phase52-v2` from main (ad6de412). One commit per step,
plus this proposal commit and a close-out commit. PR to main via
`gh pr create`; NOT merged (owner review).

## Shared machinery (built in Step 1, reused throughout)

Library: `backend/glossa_lab/pipelines/sa_validation.py`
- Corpus/LM loaders (Holdat CSV; syllabic LM JSON in both in-repo
  formats — Dravidian `syllable_freq`+`a,b` bigrams, Sanskrit
  `vocab`+`a|b` bigrams; Ge'ez LM builder from the Fuls syllabic text).
- Gold extraction (spec: Phase-52 procedure generalised to H+M).
- Fold construction (k=5, stratified, seed 107) + pin-budget selection.
- SA runner wrapping `BigramScorer` with pluggable objective terms
  (full-rescoring path; terms: LM, phonotactic, harmony, positional).
- Delta scorer (Step 3) in the same module, same objective interface.
- Unit tests: `backend/tests/test_sa_validation.py` (gold extraction,
  fold disjointness, delta-vs-full score equality on a toy corpus,
  scrambled-LM construction).

Scripts (H23: written + graph-registered BEFORE first run):
- `backend/scripts/phase107_sa_validation.py` — Steps 1–3 driver;
  subcommands per step; checkpoint JSON per (step, config, fold) under
  `reports/phase107_checkpoints/` (gitignored scratch) and a summary
  artifact per step: `reports/phase107_step1_validation.json`,
  `reports/phase107_step2_ablation.json`,
  `reports/phase107_step3_scaled.json` (incl. the final consensus
  decipherment table `reports/phase107_decipherment_table.json`).
- `backend/scripts/phase107_corpus_pool.py` — Step 4:
  `reports/phase107_step4_pooling.json` (+ acquisition log in the
  glossa-indus ledger entry; downloads land in `corpora/downloads/`,
  gitignored; provenance in CITATIONS.md).
- `backend/scripts/phase107_metrology_check.py` — Step 5:
  `reports/phase107_step5_metrology.json`.

Graph: `backend/glossa_lab/experiment_graph_phase107.py` with nodes
`IndusSAHeldOutValidation`, `IndusSAAblation`, `IndusSAScaledRun`,
`IndusSACorpusPool`, `IndusSAMetrologyCheck` (subprocess pattern per
the phase104_109 module); registered in `experiment_graph.py`
try/except; verified: node IDs present in ATOMIC_NODES.

## Compute budget (H9/H11 — every run timeout-bounded)

Measured: score_full ≈ 0.211 ms → harness run (3 seeds × 5 restarts ×
10K iters) ≈ 32 s LM-only; constraint terms add ≤ ~2× worst case.
- Step 1: 5 folds baseline + 3 sweep runs (fold 0; the 4th budget
  reuses fold-0 baseline) + 3 controls × 5 folds ≈ 23 runs ≈ ≤ 25 min.
- Step 2: 3 terms × 5 folds + 1 combined × 5 folds = 20 runs ≈ ≤ 25 min.
- Step 3: equivalence 2 × 5 seeds short runs (minutes); scaled run
  10 × 10 × 100K delta iterations (delta ≈ 10–50× cheaper/iter;
  hard timeout 30 min, checkpoint per seed).
- Step 4: pooled headline = 5 folds at harness config ≈ ≤ 5 min.
- Step 5: analysis only, seconds.
All SA drivers run detached with logs (VM can die); every run writes
its checkpoint JSON before printing, so partial progress is banked.
Folds run across 2 worker processes (nproc = 2).

## Step procedures

### Step 1
1. Build library + tests; commit is Step-1's (scripts + graph +
   registration land in the same commit, before any run — H23).
2. Run harness: baseline folds; sweep; controls. Each (config, fold)
   checkpointed. Aggregate → step1 artifact.
3. Report: primary mean±SD, secondary metric, sweep table, control
   table (z + held-out agreement + stability per LM incl. scrambled),
   discrimination verdict per the pre-registered rule.

### Step 2
1. Implement the three terms in the library (rules imported/copied
   from phase58/phase61 code with source comments; positional profile
   builder per fold).
2. Run ablations in the pre-registered order; aggregate → step2
   artifact with per-term kept/dropped verdicts by the keep rule.

### Step 3
1. Implement delta scorer; toy + real equivalence runs → step3
   artifact (equivalence numbers first).
2. Scaled run with kept-terms objective; stability selection at the
   pre-registered thresholds; final consensus table artifact.

### Step 4
1. CITATIONS.md audit of already-ingested sources (no re-fetch).
2. Web hunt per spec candidate list (public downloads only);
   download attempts logged with URLs and outcomes.
3. CISI conversion + dedupe + pooling; other obtained corpora
   converted where legitimate; headline metric re-run on the pool.
4. CITATIONS.md entries for every ingested source; step4 artifact
   with found/ingested, found/not-obtained (exact blocker), and
   searched/not-found lists.

### Step 5
1. Extract the stroke-numeral family + metrological pattern from the
   named artifacts; copy the C3 pattern statement verbatim into the
   script header.
2. Evaluate C1–C3 against the Step-3 consensus mapping → step5
   artifact, pass/fail with counts.

### Step 6
1. Foundation check after phase artifacts land (H21, 0 failures).
2. Full backend suite + ruff on changed Python.
3. Ledgers (glossa-indus per-step Phase-107 entries were appended in
   each step commit; root summary at close-out), tasks.md checked off.
4. Push; `gh pr create`; report. No merge.

## Verification (constitution §VIII)

- Exact test counts vs baseline (564 passed / 9 skipped).
- Foundation check exact result vs baseline (40/0/8), 0 failures.
- Every number in the PR/ledger traces to an artifact path under
  `reports/phase107_*`.
