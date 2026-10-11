# Rerun Contract — Phase-383 (C4 rescoring: Phases 132/134/135)

**Correction type:** C4 (rescoring from complete on-disk records)
+ C1 interval completion for the pilots' agreement statistics.
**Register rows:** PHASE-132, PHASE-134, PHASE-135 (SPEC-023,
SPEC-024 in part). **Frozen:** at the S3 merge, before the
Phase-383 script runs. Freeze record: `phase383-freeze.json`
(framework026 canonical digest over this contract + the script +
the graph module).

## Inputs (registered/local stores, as used by the originals)

- Phase-132 store: `~/workspace/glossa-lab/corpora/downloads/
  cisi_image_layer/phase132_pilot/` (records per role per object).
- Phase-134 store: `.../phase134_pilot/`; Phase-135 store:
  `.../phase135_pilot/` (pass_a/pass_b/pass_gold/adjudication
  record dirs + frame.json in each store).
- Committed originals for comparison: `reports/
  phase132_pilot_metrics.json`, `reports/phase134_pilot_metrics
  .json`, `reports/phase135_pilot_metrics.json` (+ the three
  pilot reports). Input hashes are recorded in the freeze record
  where the store layout permits (frame.json + metrics JSONs);
  the stores are gitignored local research stores, so the run
  also records record-count assertions per role (132: 50 objects;
  134/135: 100 frame objects, 20 gold) and fails loudly on any
  mismatch.

## Computation (exactly this; nothing else)

1. Recompute each pilot's headline statistics FROM THE RECORDS
   using the original metrics modules' own loaders
   (phase132_metrics / phase134_metrics / phase135_metrics
   imported, not reimplemented): Phase-132 exact-sequence
   agreement (all-50) + per-token agreement + UNK share;
   Phase-134/135 exact agreement + Cohen's kappa + ILLEGIBLE
   per-category agreement. Assert equality with the committed
   metrics JSONs (tolerance 1e-9); any mismatch is reported as
   a finding, never silently absorbed.
2. Bootstrap intervals the originals lacked: resample OBJECTS
   with replacement (B = 9,999, seed 20261011), recompute each
   statistic per replicate, report percentile 95% CIs.
3. Origin-group audit: enumerate the coder origin groups behind
   the passes (per the pilots' own disclosure: all roles were
   one model family, Muse Spark) and state the
   effective number of independent coder origin groups (= 1).
   Agreement between two passes of one origin group is
   intra-origin consistency, not independent corroboration —
   this statement enters the verdict reasoning verbatim.

## Verdict rules (declared in advance)

- Each pilot's OWN frozen gates govern the bounded claim
  (132: release gates incl. exact-seq >= 0.80 floor; 134/135:
  proceed >= 0.85 AND kappa >= 0.75; stop < 0.70 OR kappa <
  0.50). Taxonomy: gates met -> SUPPORTED; stop rule fired with
  the recorded margin -> CONTRADICTED (bounded claim: this
  coding basis at this protocol); middle band -> INCONCLUSIVE.
- The 134 "missed by one object" characterization is adjudicated
  against the agreement CI: if the CI's upper bound < 0.85, the
  near-miss reading is NOT SUPPORTED as a sampling statement
  (reported as a finding about the original report's framing,
  not as a new verdict).

## Comparison reported

Original values (verbatim) vs recomputed values vs CIs vs
taxonomy verdict per pilot + the origin-group statement.
