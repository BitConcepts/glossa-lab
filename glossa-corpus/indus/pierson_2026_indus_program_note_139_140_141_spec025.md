# Indus Program Note — Spec 025: Stage 2 Controlled Follow-Up (Phases 139–141)

**Tristen Kyle Pierson / BitConcepts LLC** · 2026-10-10
**Release:** Glossa-Lab v4.9.0 · **Repository:**
github.com/BitConcepts/glossa-lab · **Anchors:**
`INDUS_FINAL_ANCHORS.json` sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
(287 anchors; unchanged by this program)

**AI disclosure:** the work recorded here was
executed by AI agents (Muse Spark, via Muse) at
the direction of the author, per the project
constitution §VI. All quantities are computed by
script from the data files and are reproducible
from the repository at the commits named below.

---

## 1. What this note reports

Spec 024 Stage 2 (v4.8.0) reported a genuinely mixed
family of context-association tests. One member —
F3, site repertoire differentiation on the
ICIT-lineage layer (horus84) — was SUPPORTED under a
composition-only control, with period, preservation,
and excavation history named in the same breath as
uncontrolled confounders. Spec 025 is the disciplined
follow-up the program owed that result: audit what
the layer can actually support as covariates, re-test
F3 under the one control the data can bear, bound the
rest through a pre-declared sensitivity panel, and
stress F1 — the family's other positive — by
leave-one-site-out sensitivity. The design was frozen
before execution (spec PR #129; Phase-139 freeze
record PR #130; Phase-140/141 freeze records PR #131),
after an owner adjudication that answered six design
questions (spec §11). Combined report:
`reports/phase139_140_141_spec025_report.md`.

The fence is unchanged and binds everything below:
associations describe **use and co-occurrence in
recorded data, not meaning**; no result obtainable
under this spec can mint, promote, demote, or
validate any sign reading, change any anchor's
status, or move the registered predictions
PRED-2026-001/002/003 in either direction. Spec 024's
records are unedited; every Spec 025 result stands
alongside them, never instead of them.

## 2. Phase-139 — the audit, and a finding about the sketch

Before any test could be designed, Phase-139 audited
the candidate covariates on the exact F3 population
(5,410 inscriptions, 7 sites) — margins only; no
association statistic was computed. It reproduced
the spec's fill tables exactly from the layer file,
and found the spec **as sketched not freezable**: the
layer's `unit` field is a locus label, not an
excavation unit; `depth` is recorded on 51.1% of rows
in mixed units and incommensurable zero-points;
`context` is empty on all 5,679 rows; no
surface-collection rows exist; per-phase site
chronology exists only as published-stratigraphy
compilations. The frozen replacements: chronology
harmonized from published stratigraphies to ≤ 3 bands
with per-cell citations (constructed context,
Class C; 41.9% recorded); depth as within-site
relative tertiles (51.1% recorded); preservation by a
mechanical collapse (99.9% recorded). The frozen
eligibility gate (≥ 70% recorded; ≥ 3 sites at ≥ 30
recorded; ≥ 1,000 permutable) then classified
preservation as the sole PRIMARY CONTROL and routed
the other two to the sensitivity panel; G1 was
declared ESTIMABLE with primary strata = composition
(Phase-137 type class × length class) × preservation.

## 3. Phase-140 — G1, the controlled re-test

**Headline (with its mandatory rider):** on the
**ICIT-lineage layer (horus84)**, preservation
recorded coverage **99.9%**, **G1 is SUPPORTED under
control** — and **chronology is NOT controlled in the
primary test**: period/phase remain uncontrolled
confounders, bounded by the sensitivity panel below.

The population was reproduced by rule and asserted
against the committed F3 record; the covariate join
covered 5,410 of 5,410 rows; and the uncontrolled
configuration first reproduced Phase-137's F3 result
exactly (χ² 4,966.36; 0/9,999 permutations ≥ observed;
null median 2,667.87), so comparability is mechanical.
Under permutation within composition × preservation
strata (53 strata; permutable 5,404 of 5,410;
B = 9,999; seed 20261009): observed χ² 4,966.36 vs
controlled null median 2,684.74 (95th percentile
2,859.30); **0 of 9,999 permutations reached the
observed statistic; raw p = 0.0001**. Benjamini–Hochberg
was applied over G1 alone at q = 0.05 (adjudication
Q4(b)); with a family of one the adjusted value is the
raw p, and it is stated that plainly everywhere — it
is not a family correction across the sensitivity
analyses. Cramér's V is 0.2190 (descriptive); sparsity
is disclosed (67.8% of profile-table cells have
expected counts < 5; inference is by permutation
only). Differential preservation, as recorded, does
not account for the site-repertoire association on
this layer.

**Sensitivity panel (EXPLORATORY — bounds, never the
verdict):** S-chron (permutation within composition ×
chron_band strata; coverage 41.9%): null median
2,809.53, 0 of 9,999 ≥ observed, raw p = 0.0001.
S-depth (composition × depth_band strata; coverage
51.1%): null median 2,682.78, 0 of 9,999, raw
p = 0.0001. The association is not an artifact of the
recorded parts of either covariate under their
strata; neither bound converts chronology into a
controlled variable.

## 4. Phase-141 — leave-one-site-out for F1

The Phase-136 machinery, unchanged, plus a
stratum-drop parameter; the no-drop configuration
reproduced Phase-136 exactly (CMH 47.0047; MH common
OR 2.384, 95% CI 1.847–3.077; raw p 0.0001) before any
subset was accepted. All three subsets were estimable
under the §5 rule:

| Subset | MH common OR | 95% CI | Raw p |
|---|---|---|---|
| L-MD (drop Mohenjo-daro) | 2.706 | 1.858–3.940 | 0.0001 |
| L-HA (drop Harappa) | 2.162 | 1.541–3.033 | 0.0002 |
| L-KA (drop Kalibangan) | 2.400 | 1.857–3.103 | 0.0001 |

**Robustness statement (the pre-specified criterion,
its outcome verbatim): F1 is STABLE under
leave-one-site-out** — every estimable subset's
Mantel–Haenszel common OR remains > 1 with its 95% CI
excluding 1, so no single site is load-bearing for
the F1 result. Raw p-values only; no q-values; the
LOSO panel minted no verdicts and changed no Spec 024
record.

## 5. What did not change, and what would change our mind

The strict core (94 readings / 73.68% coverage) stands
exactly as before, as a hypothesis. The anchors file
is byte-identical (sha256 above); PRED-2026-001/002/
003 remain pending and untouched — nothing in this
program is an input to them. The Holdat layer's F2
null stands beside these positives; the cross-layer
contrast is not itself a test. Compilation-internal
explanations — transcription and compilation practice
within one scholarly tradition — remain live
alternatives for every quantity in this note, and
chronology remains an uncontrolled confounder of the
primary result, addressed only by a partial-coverage
exploratory bound. A keyed, independently provenanced
corpus — the trigger the program's data watch is
waiting for — remains the thing that could move any
of this from structure-within-a-lineage to evidence
about the script itself.

## 6. Files in this deposit

The v4.8.0 file set, carried forward unchanged, plus:
this note; `phase139_results.json` (the covariate
audit, gate, and verdict); `phase140_results.json`
(G1, the regression record, and the sensitivity
panel, machine-readable); `phase141_results.json`
(the LOSO subsets and the robustness outcome); and an
updated `RELEASE_VALIDATION.json` recording this
release. Source commit and release-gate record:
`RELEASE_VALIDATION.json`, entry `release_v4_9_0`.
License: CC BY 4.0.
