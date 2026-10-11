# Rerun Contract v2 — Phase-385 (governing interval correction)

**Supersedes:** phase385-contract.md (v1) for the interval
reporting only. Margin (V = 0.10), strata, population, and
verification steps are unchanged from v1.

## Why v2

The v1 design resampled the correct unit (inscriptions within
the frozen composition x preservation strata) but reported
only the PERCENTILE bootstrap interval for Cramer's V, whose
plug-in bias grows under resampling: the v1 percentile CI
[0.2282, 0.2537] excluded the point estimate 0.2190 it was
meant to bracket. The v1 execution is preserved in the
Phase-385 report.

## v2 computation (exactly this)

Identical rebuild + verification + stratified bootstrap as v1,
with B = 4,999 and seed 20261012, reporting BOTH the percentile
interval and the BASIC bootstrap interval
[2V - q97.5, 2V - q2.5]. **The basic interval governs the
margin adjudication.** Sensitivity designs (composition x
chron_band / x depth_band) remain EXPLORATORY, intervals only.
The chronology rider is unchanged and mandatory.

Freeze record: phase385-freeze-v2.json (new digest; v1 freeze
untouched).
