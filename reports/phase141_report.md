# Phase-141 Report — Spec 025: leave-one-site-out sensitivity of F1 — ICIT-lineage layer (horus84)

**Robustness outcome, as found: F1 is STABLE under
leave-one-site-out.** Every estimable subset's
Mantel–Haenszel common OR remains > 1 with its 95% CI
excluding 1, so **no single site is load-bearing** for
the F1 result. All three subsets were ESTIMABLE under
the Phase-136 §5 rule. This is a robustness statement
about the already-decided F1 result only (Spec 024,
Phase-136: CMH 47.0047, MH common OR 2.384, 95% CI
1.847–3.077, raw p 0.0001, verdict SUPPORTED after the
Spec 024 family BH correction). LOSO mints no verdicts,
carries raw p-values with **no q-values** (adjudication
Q4(b)), and cannot upgrade, downgrade, or replace the
F1 verdict — it qualifies F1's summary language only,
as Spec 025 §5 pre-specifies. The §8 limits bind the
reading throughout: co-occurrence in the recorded data
of this labeled lineage layer's joined subset; the
compilation-internal alternative (transcription and
object typing within one scholarly tradition) remains
live; no meaning claim is made or implied.

Design: `specs/025-stage2-controlled-followup/spec.md`
(§5), `phase139-freeze.md` §4, `phase141-freeze.md`.
Execution: `backend/scripts/phase141_loso.py`;
machine-readable results: `reports/phase141_results.json`.

## 1. Machinery and pre-run reproduction (freeze §2)

The Phase-136 test exactly as frozen — Phase-133
exact-string join, Seals/Tablets restriction,
TERMINAL14 outcome via the frozen mapping machinery
only, site strata with the Phase-136 eligibility
definition, CMH statistic, within-stratum permutation
(B = 9,999, seed 20261009) — with the stratum-drop
selector as the only added parameter; the Phase-136
pure functions are imported and reused, not
re-implemented. Before any subset was accepted, the
no-drop configuration **reproduced the committed
Phase-136 result exactly**: flow (5,679 layer rows;
2,895 matched; 2 ambiguous; 2,782 unmatched; 2,676
Seals/Tablets; 2,195 terminal-mapped; 2,062 in the
three eligible strata), per-stratum tables, CMH
47.004657020769315, 0 of 9,999 permutations ≥ observed,
raw p 0.0001, MH common OR 2.3839554105695653, 95% CI
[1.847164202454972, 3.076739681307485].

## 2. Subsets, as found

Each subset's remaining strata are the Phase-136
strata unchanged (asserted per subset against the
committed Phase-136 tables); estimability re-applied
mechanically per subset (≥ 2 eligible strata AND
pooled expected counts ≥ 5 in ≥ 80% of cells — every
subset's pooled fraction was 1.0).

| Subset | Remaining strata | CMH | Perms ≥ obs | Raw p | MH common OR | 95% CI (RBG) | Crude OR (uncontrolled) |
|---|---|---|---|---|---|---|---|
| L-MD (drop Mohenjo-daro) | Harappa, Kalibangan (n = 911) | 28.5198 | 0 / 9,999 | 0.0001 | **2.706** | 1.858–3.940 | 2.551 |
| L-HA (drop Harappa) | Mohenjo-daro, Kalibangan (n = 1,202) | 20.5927 | 1 / 9,999 | 0.0002 | **2.162** | 1.541–3.033 | 2.144 |
| L-KA (drop Kalibangan) | Mohenjo-daro, Harappa (n = 2,011) | 47.1515 | 0 / 9,999 | 0.0001 | **2.400** | 1.857–3.103 | 2.812 |

Per-stratum detail (descriptive; odds ratios are the
Phase-136 stratum ORs, unchanged in every subset —
Mohenjo-daro 2.182, Harappa 2.764, Kalibangan 1.429;
Fisher exact two-sided p per stratum: Mohenjo-daro
3.75×10⁻⁶, Harappa 2.60×10⁻⁷, Kalibangan 1.0 — the
Kalibangan table is the most probable table under its
own margins, so its stratum carries no independent
signal, as its n = 51 led us to expect). TERMINAL14
shares by type per stratum are as in Phase-136 (seals
28.1% vs tablets 12.5% pooled in the full population).

**Reading.** The criterion is met with room in every
subset. Dropping Harappa — the stratum with the largest
single-site OR — leaves the lowest subset estimate
(2.162, CI 1.541–3.033), still clearly above 1 with its
interval excluding 1; dropping Mohenjo-daro, the largest
stratum, leaves 2.706 (1.858–3.940); dropping
Kalibangan leaves 2.400 (1.857–3.103), essentially the
full-sample estimate, confirming that the small
Kalibangan stratum contributes precision neither way.
No site is load-bearing; the F1 summary language
stands unqualified ("supported") on this robustness
criterion, subject to the standing lineage-layer and
compilation-internal caveats that travel with F1
itself.

## 3. Process record

- Graph-first (H15/H23): node `IndusPhase141Loso`
  registered in `backend/glossa_lab/experiment_graph.py`
  (module `experiment_graph_phase141.py`) and verified
  before the run.
- Anchors asserted byte-identical before and after the
  run (sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`);
  all inputs consumed read-only and hash-recorded in
  the results JSON.
- Deviations: none in the execution. (Two pins in the
  phase's own test file were corrected during
  verification — a substring check that matched the
  results JSON's own "no q-values" declaration key and
  a case mismatch against that declaration; test code
  only, no quantity affected.)
- No anchor was minted, promoted, demoted, or
  validated; the frozen mapping machinery was imported
  for sign mapping only — no PRED scoring was imported
  or called, and no output of this phase is an input
  to PRED-2026-001/002/003; Class I fields entered
  nothing.

**AI disclosure:** produced by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.
