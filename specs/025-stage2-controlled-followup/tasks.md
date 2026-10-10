# Spec 025 — Tasks

> ## FROZEN — OWNER-ADJUDICATED 2026-10-10 (spec.md §11)
>
> Phase-139 is authorized by the adjudication. Phase-140
> tasks stay gated on the Phase-139 freeze record (T6);
> Phase-141 proceeds under the same record.

## Adjudication

- [x] T0 — Owner answers §11 Q1–Q6; answers recorded in a dated
      decision entry appended to spec.md (append-only).
      **Done 2026-10-10:** all six answered with the
      recommended answers; record at spec.md §11.

## Phase-139 — Covariate audit + harmonization

- [x] T1 — Recompute spec §3 fill-rate tables from the layer
      file (hash-asserted); file the audit script + tables.
      **Done 2026-10-10 (Phase-139):** counts reproduce §3
      exactly; three printed percentages carry documented
      deltas (reports/phase139_report.md §2).
- [x] T2 — Covariate-eligibility audit vs the frozen gate
      (coverage, per-site counts, permutable-N projections;
      margins only — no repertoire outcome computed).
      **Done 2026-10-10:** chron_band SENSITIVITY (41.9%),
      depth_band SENSITIVITY (51.1%), preservation PRIMARY
      CONTROL (99.9%).
- [x] T3 — Q2(a) approved: `chron_band` mapping table with per-cell
      published-stratigraphy citations; Class C grading.
      **Done 2026-10-10:** 35 mapped cells, 7 citations;
      register at data/evidence_integration/
      phase139_citation_register.json.
- [x] T4 — Q3(a) approved: `depth_band` construction (within-site
      tertiles + UNRECORDED) with parse rules documented.
      **Done 2026-10-10:** 2,765 banded (51.1%); parse
      categories and 145 boundary-tie rows disclosed.
- [x] T5 — Phase-139 audit report + freeze recommendation
      (or G1 NOT ESTIMABLE record under §4.3 F-c).
      **Done 2026-10-10:** reports/phase139_report.md —
      verdict ESTIMABLE (primary = composition ×
      preservation); sensitivities routed per §4.2.
- [x] T6 — Freeze record committed + merged (spec-before-code).
      **Done 2026-10-10:** phase139-freeze.md (this PR) —
      final strata, seed 20261009, thresholds (BH over G1
      alone) named for Phase-140/141.

## Phase-140 — G1 controlled re-test

- [x] T7 — Graph module/node registered + verified; unit tests
      incl. uncontrolled-configuration regression vs Phase-137.
- [x] T8 — Run under frozen strata (B = 9,999); anchors and
      layer hash asserted before/after.
- [x] T9 — Results JSON + phase report (lineage headline;
      coverage statement in the headline paragraph).

## Phase-141 — F1 LOSO sensitivity

- [x] T10 — Stratum-drop parameter + tests incl. exact
      reproduction of Phase-136 in the no-drop configuration.
- [x] T11 — Run L-MD / L-HA / L-KA; per-subset estimability
      rule applied mechanically.
- [x] T12 — Phase report: robustness-criterion outcome;
      load-bearing site named if any.

## Close-out

- [ ] T13 — BH correction (per Q4) + combined Spec 025 report.
- [ ] T14 — Foundation check 0 failures; anchors re-asserted.
- [ ] T15 — Publication per Q6; ledgers updated (Spec 024
      records untouched).
