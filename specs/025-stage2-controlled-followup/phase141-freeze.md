# Spec 025 — Phase-141 Freeze Record (F1 leave-one-site-out)

> ## FROZEN 2026-10-10 — before any Phase-141 code runs
>
> This record freezes the Phase-141 (LOSO) design at
> execution level, under Spec 025 §5 and the Phase-139
> freeze record (`phase139-freeze.md` §4). It adds no
> design choice those documents do not already
> determine. Amendments append-only, dated, and
> committed before the execution they affect.

## 1. Basis

- Spec 025 §5 (frozen 2026-10-10; PR #129): the design,
  the estimability rule, and the robustness criterion,
  verbatim.
- Phase-139 freeze record §4: LOSO members L-MD / L-HA /
  L-KA in the §5 configuration, verdict-relevant only
  through the §5 robustness criterion; raw permutation
  p-values reported; **no q-values computed for LOSO
  members** (adjudication Q4(b)).
- Phase-136 execution (Spec 024 Stage 2(a), family
  member F1): the machinery and frozen definitions
  reused unchanged (`backend/scripts/
  phase136_terminal_type.py`, freeze
  `specs/024-evidence-integration/stage2a-freeze.md`,
  results `reports/phase136_results.json`). F1 as
  executed: eligible strata Mohenjo-daro (n = 1,151),
  Harappa (n = 860), Kalibangan (n = 51); CMH 47.0047;
  MH common OR 2.384 (95% CI 1.847–3.077); raw
  p = 0.0001; verdict SUPPORTED (Spec 024 family BH).

## 2. The one permitted change

Phase-141 is the Phase-136 test exactly as frozen —
same joined-subset construction (Phase-133 exact-string
join), same TERMINAL14 outcome via the same frozen
mapping machinery, same catalogue object type, same
stratum eligibility definition, same CMH statistic,
same within-stratum permutation (B = 9,999, seed
20261009, `random.Random(20261009)`, p = (1 +
#{perm ≥ obs}) / (1 + B)) — with **one** added
parameter: a stratum-drop selector naming one eligible
stratum to remove before the test is computed.

**Pre-run reproduction requirement.** Before any subset
is accepted, the Phase-141 machinery in the no-drop
configuration must reproduce the committed Phase-136
result **exactly** (population flow, eligible strata,
per-stratum tables, CMH statistic, MH common OR and
95% CI, permutation count and raw p) from
`reports/phase136_results.json`. Any mismatch is a
stop condition, recorded here as a dated amendment
before subsets proceed.

## 3. Subsets

- **L-MD:** drop Mohenjo-daro; Harappa + Kalibangan
  remain.
- **L-HA:** drop Harappa; Mohenjo-daro + Kalibangan
  remain.
- **L-KA:** drop Kalibangan; Mohenjo-daro + Harappa
  remain.

The dropped stratum is removed from the eligible set;
the remaining strata are **not** re-derived — their
eligibility, tables, and outcome vectors are exactly
their Phase-136 values (asserted per subset against
the committed Phase-136 results).

## 4. Estimability (per subset, mechanical)

The Phase-136 §5 rule, re-applied to each subset
verbatim: **≥ 2 eligible strata AND the pooled 2×2
expected counts ≥ 5 in at least 80% of its 4 cells.**
A subset failing it is reported **NOT ESTIMABLE** as
a sensitivity — a designed outcome (spec §5),
especially possible where Kalibangan (n = 51) is one
of two remaining strata. A NOT ESTIMABLE subset mints
no statistic, no p-value, and no robustness reading.

## 5. Per-subset outputs (estimable subsets)

- Per-stratum 2×2 tables and odds ratios (descriptive),
  with Fisher exact two-sided p-values per stratum as
  descriptive stratum detail (the Phase-139 freeze
  record's §4 parenthetical; descriptive only — they
  enter no criterion and mint nothing).
- CMH statistic and within-stratum permutation raw
  p (B = 9,999, seed 20261009; fresh stream per
  subset, exactly as the Phase-136 machinery seeds
  each call).
- Mantel–Haenszel common OR with Robins–Breslow–
  Greenland 95% CI — the quantity the §6 criterion
  reads.
- TERMINAL14 shares by type, per stratum and pooled
  (descriptive).

## 6. Robustness criterion (spec §5, verbatim)

F1 is reported **stable** iff every estimable subset's
Mantel–Haenszel common OR remains **> 1 with its 95%
CI excluding 1**. If any estimable subset's CI
includes 1 or its OR ≤ 1, the report names the dropped
site as **load-bearing** and downgrades the F1 summary
language accordingly ("supported, concentrated
in …"). A NOT ESTIMABLE subset neither confirms nor
breaks stability; if any subset is NOT ESTIMABLE, the
robustness statement says so and scopes itself to the
estimable subsets. The criterion is on effect
estimates deliberately: these are sensitivity analyses
of an already-decided test, **not new tests**; they
mint no verdicts of their own, carry raw p-values with
**no q-values** (Q4(b)), and cannot upgrade, downgrade,
or replace the Spec 024 F1 verdict — they qualify its
summary language only, as §5 pre-specifies.

## 7. Execution and reporting obligations

- Graph-first (H15/H23): the Phase-141 experiment-graph
  node is registered and verified before the run;
  foundation check (H21) 0 failures after the phase.
- Anchors asserted byte-identical (sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`)
  before and after; all inputs consumed read-only and
  hash-recorded.
- Deliverables: `reports/phase141_results.json` and
  `reports/phase141_report.md` under the mandatory
  **ICIT-lineage layer (horus84)** headline. The
  report states the §6 robustness-criterion outcome
  and names any load-bearing site.
- Expected precision, stated in advance (spec §5):
  the three Phase-136 stratum ORs were 2.18
  (Mohenjo-daro), 2.76 (Harappa), 1.43 (Kalibangan,
  n = 51) — all in the same direction, with
  Kalibangan's precision low by construction. Wide
  intervals in L-MD and L-HA are expected and are
  reported, not smoothed.
- §8's epistemic limits bind every output:
  co-occurrence in a labeled lineage layer's joined
  subset; no meaning claims; no PRED contact; no
  anchor movement.

*Freeze record ends. Amendments append-only, dated,
and committed before the execution they affect.*
