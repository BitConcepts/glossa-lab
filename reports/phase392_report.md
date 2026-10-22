# Phase-392 — Spec 027 Stage 1 (Q2 repertoire gate)

**Verdict: INCONCLUSIVE** — controls pass; neither the SUPPORTED nor the CONTRADICTED rule fires (or the LOSO range crosses the margin).

Bounded claim (stage1-freeze.md section 1, as amended): in the named corpus, under M77, after rarefaction to a common cell size and stratification by object type, site explains more recorded sign-repertoire variation than expected under permuted site labels, at the declared practical margin (adjusted R^2 = 0.01). The claim concerns recorded repertoires in this corpus only; no outcome identifies a dialect or a language.

## Primary

- Population reproduced: True (eligible 3144; analysis 3030 at 6 sites; cells included 8; excluded cells {'Chanhu-daro|TAB': 2, 'Dholavira|TAB': 15, 'Kalibangan|TAB': 3, 'Lothal|TAB': 2}).
- Median adjusted PERMANOVA R^2 over 199 rarefaction draws: 0.0168; 95% percentile interval [0.0103, 0.0240]; median raw R^2 0.0293 (reported for transparency; all rules use the adjusted scale); share of draws rejecting at alpha 0.05: 1.000.

## Jackknife (leave-one-site-out, median adjusted R^2)

- Drop Harappa: 0.0093
- Drop Mohenjo-daro: 0.0181
- Drop Dholavira: 0.0186
- Drop Lothal: 0.0169
- Drop Chanhu-daro: 0.0168
- Drop Kalibangan: 0.0171

## Controls (failure = INVALID)

- Negative (pooled composition, no site structure): median adjusted R^2 0.0002, share rejecting 0.005 — PASS.
- Positive (planted site effect, 10 signs x3 per site): median adjusted R^2 0.0212, interval [0.0158, 0.0276], share rejecting 1.000 — PASS.

## Labelled sensitivity (no verdict)

- S-complete (complete='N' excluded; 2564 records): median adjusted R^2 0.0179, share rejecting 1.0.

## Boundaries

- Period is not controlled (layer period field 59.2% uninformative; Phase-139 finding, frozen as a stated limitation).
- Multi-line status is not recorded in this layer; eligibility ran on the frozen legible-token rule.
- The Parpola/CISI sensitivity is NOT ESTIMABLE at the frozen crosswalk rule (freeze-time margins determination) and was not run.
- Anchors and PRED untouched by this phase.
