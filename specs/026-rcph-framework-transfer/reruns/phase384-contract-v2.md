# Rerun Contract v2 — Phase-384 (corrected interval procedure)

**Supersedes:** phase384-contract.md (v1) for the interval
computation only. The v1 margin (V = 0.10) and verdict rules
are unchanged — they were declared before any run.

## Why v2 (evidenced defect in v1, found by its own control)

The v1 procedure — parametric bootstrap over profile-table
cells, treating tokens as independent draws — was subjected to
the independence negative control the framework requires. On
an independence table with F2's exact margins (true V = 0) it
returned a 95% CI of [0.1115, 0.1242]; with F3's margins,
[0.0984, 0.1095]. A procedure that finds V ≈ 0.11 under exact
independence is non-discriminating at these table dimensions
(9 x 98 and 7 x 187; df 776 / 1116 against 7,002 / 17,257
tokens, with strong within-inscription dependence the cell
model ignores). Under Spec 026 principle 5 the v1 interval
adjudication is INVALID — recorded as such in the Phase-384
report, with the v1 numbers preserved verbatim.

## v2 computation (exactly this)

1. Rebuild each layer's population with the Phase-137 module's
   own loaders and frozen population rule (eligible sites;
   n_parsed_tokens >= 1; columns = signs with layer-wide count
   >= 10, remainder pooled as OTHER); assert the rebuilt
   profile table EQUALS the table recorded in
   reports/phase137_results.json, and chi2/V match the record.
2. Bootstrap over INSCRIPTIONS: resample with replacement
   within each site (site sizes fixed); rebuild the table;
   Cramer's V per replicate; B = 9,999; seed 20261012.
3. Intervals: percentile (reported) and BASIC bootstrap
   [2V - q97.5, 2V - q2.5] — the BASIC interval governs the
   margin adjudication (it corrects V's plug-in bias under
   resampling).

## Verdict rules (identical to v1)

- F3: SUPPORTED stands iff governing CI lower bound > 0.10;
  crossing -> INCONCLUSIVE at the declared margin.
- F2: governing CI upper bound < 0.10 -> CONTRADICTED at the
  declared margin; crossing -> INCONCLUSIVE.

Freeze record: phase384-freeze-v2.json (new digest over this
contract + the v2 script + the graph module; the v1 freeze is
untouched).
