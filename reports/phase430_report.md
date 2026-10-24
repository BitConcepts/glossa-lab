# Phase-430 — Spec 068 report

Claim: `yadav_2009_arxiv_manual_001` — standing strongly
supported, stage explained, exactly as recorded.
Execution date: 2026-10-22. Freeze digest:
`ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d`. OSF registration 3pbwe (filed
2026-10-22; pending approval at execution, recorded as
it stands).

## Outcome: COMPARISON UNINFORMATIVE

## Headline (spec section 7 wording, filled from the run)

> This corpus is an ICIT-lineage corpus. Agreement between it and the program's earlier ICIT-lineage layer is consistency within one tradition, not independent corroboration. The comparison cannot judge the script: the linguistic positive control, Linear B sign frequencies (fit error 0.9229), does not fit strictly better than every non-linguistic control (Mesopotamian numerical signs 0.5335; heraldic charges 0.1839; the synthetic emblem process, median 0.2405), so the measures used here do not separate the one certain writing system in the set from systems that are not writing. The Indus quantities on the Shakti restricted corpus (0.1584, exponent 2.004) are reported for the record as a new baseline and support no separability conclusion either way. The claim stands exactly as recorded, with no strength label added.

## Fit table (spec section 10, item 3)

| System | V | N | alpha | q | NRMSE_log | R2_log | gap Delta |
|---|---|---|---|---|---|---|---|
| Indus primary (documented-lineage) | 557 | 11805 | 2.004 | 19.9 | 0.1584 | 0.9892 | — |
| N1 Mesopotamian numerical signs | 12 | 1981 | 3.0 | 0.66 | 0.5335 | 0.9312 | 0.3752 |
| N2 Heraldic charges (Dering Roll) | 57 | 825 | 2.878 | 20.0 | 0.1839 | 0.9704 | 0.0255 |
| N3 Synthetic emblem inventory (median of 99) | 1181.0 | 11805 | 1.16 | 0.0 | 0.2405 | — | 0.0821 |
| P1 Linear B (positive control) | 89 | 47292 | 3.0 | 17.45 | 0.9229 | 0.7658 | 0.7646 |

N3 replicate distribution: alpha median 1.16, NRMSE_log median 0.2405, central 90% interval [0.20345467653345492, 0.28685523446752004]; as-well share 0.00. NEAR MISS (0 < Delta <= 0.02): none.

Positive-control condition (P1 strictly better than every non-linguistic control): NOT MET.

## Sensitivity fit (spec section 6.1, in full)

| Indus sensitivity (documented + corroborated) | 707 | 17216 | 1.96 | 20.0 | 0.1544 | 0.9901 | — |

Grade-sensitive: False. The verdict-relevant ordering does not change between the grade sets.

## Subsampling (spec section 6.2; median [central 90% interval])

- primary half: alpha 1.823 [1.7728, 1.8735]; NRMSE_log 0.1739 [0.1589, 0.1874] (1522 inscriptions x 99 replicates)
- primary quarter: alpha 1.632 [1.5391000000000001, 1.7328999999999999]; NRMSE_log 0.1884 [0.1763, 0.2131] (761 inscriptions x 99 replicates)
- sensitivity half: alpha 1.793 [1.7599, 1.842]; NRMSE_log 0.1687 [0.1592, 0.1793] (2565 inscriptions x 99 replicates)
- sensitivity quarter: alpha 1.619 [1.5589, 1.6925]; NRMSE_log 0.1867 [0.1703, 0.2067] (1282 inscriptions x 99 replicates)

Section 6.3: no separate full-inventory fit exists under limb B — the primary already is that fit.

## Gates, in frozen order

- **Gate 0.1 — Input integrity: PASS**
- **Gate 0.2 — Estimator self-test: PASS**
- **Gate 0.3 — Shakti intake identity (P-F1 S1): PASS**
- **Gate 0.4 — Shakti intake census (P-F1 S2) + restricted census: PASS**
- **Gate 0.5 — Population act (OPEN-068-1, DD-068-7): PASS**
- **Gate 0.6 — Control set freeze (cited data): PASS**
- **Gate 0.7 — Census floors: PASS**

This result is a strength label for a recorded curve fit, measured as a new baseline on the Shakti corpus. It is not evidence that the script encodes language, it changes no verdict, and it neither confirms nor corrects any Phase-43 quantity.

Anchors asserted byte-identical before and after: `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.*
