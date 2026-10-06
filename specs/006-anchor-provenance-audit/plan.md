# Plan 006 — Anchor Provenance Audit (Phase-108)

## Branch / commits

Branch `feat/anchor-provenance-audit` from main (6a46809e). One
commit per step, plus this proposal commit and a close-out commit.
Commit after every step (a predecessor package lost its coordinator
to a runtime restart; banked commits are the recovery mechanism).
PR to main via `gh pr create`; NOT merged (owner review).

## Shared machinery

Library: `backend/glossa_lab/pipelines/provenance_audit.py`
- Anchor loading + field normalisation (diacritic stripping, first
  segment extraction — same conventions as spec 005's gold extraction
  where applicable).
- Trail assembly: anchor-entry fields; ledger section index
  (phase → text span) over `glossa-indus/LEDGER.md` and `LEDGER.md`;
  artifact index over `reports/` + `outputs/` (filename phase tags +
  per-sign mention scan for SA artifacts); claims index.
- SA-lineage tables: the enumerated SA phases/artifacts from spec
  006, as data (phase number → role: origin-capable | agreement-only
  | falsification-only | validation-only).
- Pass-1 classifier implementing the pre-registered rules.
- Recomputations: coverage (Holdat CSV), phonotactics (imports
  Phase-58 functions by file path), Parpola agreement (crosswalk
  v2.1), site invariance (imports Phase-69 `chi2_test` by file path;
  I/M/T counting replicated from its code with the eligibility rule
  quoted in the artifact).
- Unit tests: `backend/tests/test_provenance_audit.py`
  (normalisation, match rule, pass-1 rules on synthetic trails,
  coverage counting on a toy corpus).

Scripts (H23: written + graph-registered BEFORE first run):
- `backend/scripts/phase108_provenance_extract.py` — Step 1 →
  `reports/phase108_anchor_trails.json`.
- `backend/scripts/phase108_provenance_classify.py` — Step 2:
  pass 1 → draft register; `--finalize` merges
  `reports/phase108_review_decisions.json` (hand-review, authored
  between the two runs) → `reports/phase108_provenance_register.json`
  + `reports/phase108_provenance_summary.md`.
- `backend/scripts/phase108_provenance_recompute.py` — Step 3 →
  `reports/phase108_subset_recomputation.json`.
- `backend/scripts/phase108_provenance_impact.py` — Step 4 →
  `reports/phase108_impact_map.json` (+ summary MD section appended
  by the close-out edit, or a companion
  `reports/phase108_impact_summary.md`).

Graph: `backend/glossa_lab/experiment_graph_phase108.py` with nodes
`IndusProvenanceExtract`, `IndusProvenanceClassify`,
`IndusProvenanceRecompute`, `IndusProvenanceImpact` (subprocess
pattern per the phase107 module); registered in
`experiment_graph.py` try/except; verified in ATOMIC_NODES before
any script runs.

## Compute budget (H9/H11)

All steps are deterministic text/count work: extraction scans are
bounded file reads over `reports/` + `outputs/` (mention scans capped
per file); recomputations are single passes over a 7,002-row CSV.
Every script run carries a shell timeout; no unbounded loops.

## Step procedures

### Step 1
1. Build library + tests; scripts + graph + registration in the
   same commit, before any run (H23).
2. Run extraction → trails artifact. Spot-check 5 anchors by hand
   against the raw sources before proceeding (M267 must show its
   Phase-273 promotion with grammar/χ²/DEDR/Elamite lines and no
   SA origin; M047 must show the crosswalk/Parpola trail).

### Step 2
1. Pass 1 classify → draft register with per-anchor decision basis
   (`explicit` vs `needs_review`).
2. Hand-review every `needs_review` anchor by reading its trail;
   write review_decisions.json (category + rationale + citations
   per anchor; edge cases and pass disagreements logged).
3. Finalize → register + summary MD with the registered headline
   counts (overall, by tier, three-way SA-independent number).

### Step 3
1. Implement recomputations in the library against the final
   register's sets.
2. Run → recomputation artifact: (a) coverage, (b) phonotactics,
   (c) Parpola agreement (+ Phase-159 cross-check), (d) site
   invariance (full-set replication first, then subset; divergence
   reported if any). Each with method note + old-vs-subset numbers.

### Step 4
1. Circular-chain detection: for each anchor, if it appears as a pin
   in a Phase-52/57 (or re-run) decipherment table AND a later
   promotion/claim cites SA agreement — emit the chain with both
   citations. Supplement with the ledger's injection→re-run cycles.
2. Claims map: parse the 31 extracted claims + Phase-104 evaluation;
   per claim, list cited signs (M-numbers / values in claim text)
   intersected with the SA-lineage anchor set.
3. Headline-number map: 161 / 90.96% / 59% — source artifact for
   each, the set it was computed on, SA-lineage share of that set
   per the register.
4. Foundation-check map: grep + read `foundation_check.py` for every
   claim text citing an SA phase; record text, location, and
   post-Phase-107 status (falsified / caveated / unaffected).
5. Aggregate → impact artifact + summary.

### Step 5
1. Recommendations authored into the summary MD + PR body (not
   executed): surviving numbers, numbers to retire/re-base, the
   honest programme statement.
2. Foundation check (0 failures; H21), full backend suite, ruff.
3. Ledgers (glossa-indus Phase-108 per-step entries appended in each
   step commit; root summary at close-out), tasks.md checked off.
4. Push; `gh pr create`; report. No merge.

## Verification (constitution §VIII)

- Exact test counts vs baseline (576 passed / 9 skipped).
- Foundation check exact result vs baseline (40/0/8), 0 failures.
- Every number in the register/summary/PR traces to a trail or
  recomputation artifact under `reports/phase108_*`.
- `INDUS_FINAL_ANCHORS.json` byte-identical to main at close-out
  (audit-only guarantee, verified by hash).
