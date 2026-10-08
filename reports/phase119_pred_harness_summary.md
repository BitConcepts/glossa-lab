# Phase-119 — PRED-2026 Readiness Harness: Summary

**HARNESS DRY RUN — NOT A PRED EVALUATION**

Spec: `specs/018-phase119-pred2026-readiness/` (frozen in its
own commit before any code). Date: 2026-10-07. No
PRED-2026 prediction was evaluated by this phase; no
qualifying dataset exists yet (spec §10).

## What was built

The machine that fires the day independent data lands:

- `backend/glossa_lab/pred_harness.py` — frozen sign sets +
  canonical map loaded from the registry files (hashes
  asserted in tests); dedup stages A/B/C; three ingestion
  adapters (`rmrl_concordance`, `image_transcription`,
  `future_concordance`) plus the dry-run-only
  `converted_layer` adapter, each emitting the Phase-107/111
  provenance-log entry; §6.1 gating (qualifying class,
  provenance completeness, ≤ 25% unmapped+ambiguous token
  share, verdict lock, multi-site input for 003) enforced
  **before** any criterion statistic can exist; mechanical
  scorers implementing the registered criteria verbatim;
  a `dry_run` path that shares ingestion/dedup only and
  cannot produce a rate, conformance fraction, or verdict.
- `backend/scripts/phase119_pred_harness.py` — fixture
  self-checks + the §8 dry run; asserts its outputs against
  spec Appendix A and exits nonzero on mismatch.
- `backend/glossa_lab/experiment_graph_phase119.py` — node
  `IndusPhase119PredHarness`, registered per H23 and asserted
  in `ATOMIC_NODES` before the script was run.
- Synthetic fixtures + 21 unit tests
  (`backend/tests/test_phase119_pred_harness.py`), including
  a toy prediction evaluated end-to-end through the real
  gating/scoring code in **both** verdict directions, the
  real PRED-2026-003 scorer on toy future-concordance
  fixtures (0.80 CONFIRMED / 0.40 REFUTED), gate refusals,
  and the verdict lock.

Machine: gpu_device = cpu (no experiment run; harness only).

## The registered criteria (verbatim, docs/PREDICTION_REGISTER.md §2)

- **PRED-2026-001:** "Signs classified as TERMINAL by the
  CGSA model will have end_rate ≥ 0.45 in the ICIT full
  corpus (6,800 inscriptions) when it becomes available." —
  criterion: "≥ 10 of the 14 current TERMINAL signs show
  end_rate ≥ 0.45 in ICIT data".
- **PRED-2026-002:** "Signs classified as INITIAL by the CGSA
  model will have start_rate ≥ 0.45 in the ICIT full corpus."
  — criterion: "≥ 8 of the 12 current INITIAL signs show
  start_rate ≥ 0.45 in ICIT data".
- **PRED-2026-003:** "The 3-slot INITIAL-MEDIAL-TERMINAL
  template structure will account for ≥ 70% of inscription
  templates in any newly acquired multi-site dataset." —
  criterion: "Template coverage ≥ 70% in held-out corpus".

## Evaluability matrix (spec §4, frozen)

| Class | 001 | 002 | 003 |
|---|---|---|---|
| rmrl_concordance | QUALIFIES | QUALIFIES | QUALIFIES |
| image_transcription | QUALIFIES | QUALIFIES | only if ≥ 2 sites |
| future_concordance | QUALIFIES | QUALIFIES | QUALIFIES |
| icit_full | QUALIFIES (C1) | QUALIFIES (C1) | QUALIFIES (C1) |
| icit_lineage_derivative | dry-run only | dry-run only | dry-run only |
| derivation_corpus | NO | NO | NO |

C1 (verbatim): "Class features derive in part from a mayig
ICIT feature extract; this corpus is the registered withheld
data but is derivation-adjacent in part." **Nothing
qualifying is in hand today**; the acquisition log
(`reports/phase119_acquisition_log.json`) records the three
awaited sources as GAPs.

## Dry-run headline numbers (non-independent layer; spec App. A)

Population: Phase-115 expanded ICIT converted layer,
4,531 inscriptions / 15,880 tokens (class
`icit_lineage_derivative`). Dedup (§5, P-space):

| Stage | Kept | Removed (stage) | Cumulative |
|---|---|---|---|
| input | 4,531 | — | — |
| A exact | 3,063 | 1,468 (32.40%) | 32.40% |
| B sentinel-normalized | 2,693 | 370 | 40.79% |
| C near-dup ≤ 1, len ≥ 4 | 2,446 | 247 | 46.02% |

Sign-set coverage (what the eventual test could judge):
TERMINAL attested **12/14** (unattested P076, P125); INITIAL
**11/12** (unattested P000); MEDIAL **38/46**; unmapped
47 tokens (9 unmapped + 38 ambiguous, incl. M002 → UNK).
PRED-003 classifiability coverage: 2,544/4,531 (56.15%)
pre-dedup; 1,045/2,446 (42.72%) post-dedup. Per-prediction
judgeability on a future corpus equals attestation of the
frozen sets in that corpus; on this lineage the ceiling for
001 is 12 of the 14 TERMINAL signs and for 002 is 11 of 12
INITIAL signs — with unattested signs counting as NOT
meeting the criterion (§6.2), the registered bars (≥ 10,
≥ 8) remain reachable on attestation like this layer's, but
no rate was or may be computed here.

One process note: Appendix A's prototype dedup figures were
measured on raw M-space sequences; §5 as frozen operates on
P-space sequences. The correction is recorded additively as
spec Appendix A.6; the harness asserts the corrected
(P-space) values, and reproduced every other Appendix A
figure exactly.

## Verification

21 new unit tests pass. Full suite + foundation check +
ruff: recorded in the Phase-119 ledger entries at close-out.
