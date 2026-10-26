# Foundation Report — Red-Team Note (2026-10-25, findings E-6, E-7, E-10)

This note sits beside `foundation_check_report.json`. The
report's counts stand **as measured (39 passed / 0 failed / 9
warnings)** and its WITHDRAWN handling is correct: the Phase-169
aggregate confidence figure (79.8%) appears nowhere in
`passed[]`, and its warning text states the withdrawal
accurately. Three qualifications, verified by the 2026-10-25
programme red team, attach to the report as committed:

1. **P30-A1-A3 (the open half of RT-30).** The report carries
   the warning "Used hardcoded fallback candidates — live data
   not available" and, in the same file, lists P30-A1 in
   `solid_claims[]` with status "VERIFIED — but simulation used
   simplified model" (Enmenanak score 7.0 at the 100th
   percentile of the null, p<0.001). A claim whose data were
   hardcoded fallbacks should not sit in the solid-claims list
   on a "VERIFIED" status. Until the generator is corrected,
   read P30-A1's status as: **computed on fallback candidates;
   not a verification against live data.**
2. **"Decoded" labels.** `solid_claims[]` entries "Phase-53 16
   formulas decoded", "Phase-59 22 formulas decoded" and
   "Phase-68 formula type annotation" use "decoded" where every
   public surface of the programme says no reading is proven.
   Read "decoded" in these entries as "candidate readings
   assigned to ≥80% of slots under the phase's own rules" —
   an internal assignment statistic, not a decipherment claim.
3. **The 79.8 figure outside this report.** The withdrawal is
   correctly handled here, but `aggregate_confidence_pct: 79.8`
   still sits as a bare field in
   `backend/reports/phase169_master_synthesis.json` (and its
   research/indus copy). That field carries the same
   withdrawal: the figure has no recorded weighting rule and
   means nothing as a confidence value.

The generator corrections implied by (1) and (2) — the P30
claim's status carrying its fallback caveat in the claim
itself, and the "decoded" labels reworded — are named follow-up
work. This note is the record correction in the meantime; the
generated report itself is not hand-edited.

*This note establishes the qualifications a reader must carry
when citing the committed foundation report. It does not
establish any change to the measured counts.*

---

**Addendum (2026-10-26).** Items (1) and (2) are now fixed at
generation: `foundation_check.py` moves any claim whose inputs
fell back in the run out of `solid_claims` into
`caveated_claims` with a NOT VERIFIED fallback status (P30-A1 is
the current case), and the Phase-53/59/68 entries are worded as
candidate-reading assignments, not decipherment. The report was
regenerated with the fixed generator; counts unchanged
(39/0/9). Item (3): the Phase-169 generator now emits
`aggregate_confidence_pct_status` (WITHDRAWN) beside the value,
but the committed Phase-169 JSON files are **not yet
regenerated** — the generator needs PyTorch (absent from this
environment) and stamps its host's GPU state, and the current
canonical anchors have moved since Phase 169, so a regeneration
here would rewrite more than the annotation. Until that
regeneration runs in the right environment, item (3)'s
qualification above still applies to the committed JSON files.
