# Spec 067 / Phase-429 — Outcome record (EXECUTED 2026-10-22 — REPLICATED)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 067 contract
> (freeze digest
> `73463ab949f65ecf620a9f4544b9a84fe18f72056a86c48ce9d5d0164f3d41db`),
> as **Phase-429**, under the owner's approval
> of 2026-10-21 (amendment package Item 7 §6)
> and the separate execution order given after
> OSF registration **qsthg** was approved and
> API-verified by the parent on 2026-10-22
> (public true, pending false, withdrawn false,
> reviews_state accepted). Outcome:
> **REPLICATED** — all step-0 gates passed, the
> enlarged set was estimable, and the frozen
> §5 mapping assigns REPLICATED on the run's
> own quantities. `STUDY-SPEC-024/F1`'s frozen
> record is not edited; this record appends
> beside it and beside Spec 059's record, and
> carries the §5 re-statement the gate-passed
> REPLICATED outcome earns (§1).

## Headline (spec §5 REPLICATED wording, filled from the run)

> "On the enlarged object-ID-joined
> set (4676 of 5,679 lineage rows, 82.34%, against
> the original join's 51.0%), the seal/tablet
> difference in TERMINAL14 endings replicates
> within sites: Mantel–Haenszel odds ratio
> 2.452, 95% CI [1.965–3.058], entirely above 1.5,
> family-adjusted q = 0.0001. The original F1
> result was not an artefact of which rows the
> concordance join could reach, at this test's
> resolution. Leave-one-site-out: every dropped-site subset remained
> estimable with its interval excluding 1; no site is
> load-bearing. This is a
> statement about recorded use in this lineage
> layer, not about what the difference means."

**The §5 re-statement (appended record only).**
REPLICATED on a materially enlarged set is the
outcome under which the claim's "on the joined
subset" scope is re-stated, and this record
re-states it: `STUDY-SPEC-024/F1`'s seal/tablet
TERMINAL14 difference is now recorded on the
enlarged object-ID-joined subset actually
joined under this spec — **4,676 of 5,679
lineage rows (82.34%)**, joined through object
identifiers against the merged catalogue layer
v2 — in place of the original joined subset's
51.0% scope, by this appended record only. The
frozen Spec 024 record itself, its verdict
(SUPPORTED, odds ratio 2.384, interval
[1.847, 3.077], family q = 0.00015), and Spec
059's JOIN GATE NOT MET closure stand exactly
as recorded and are not edited, superseded, or
re-adjudicated by this append.

What this means, in plain words: the original
test could reach only the half of the lineage
layer whose catalogue references matched the
printed catalogue by exact string, and Spec
059 showed that routing the same rows through
object identifiers reached no more of it on the
catalogue the programme then held. The fuller
catalogue Spec 066 built through Phase-130
intake changed that: the same object-identifier
route now reaches more than four-fifths of the
layer, and on that much larger joined set the
seal/tablet difference in closing signs is
still there, at much the same size (odds ratio
2.452 against the original 2.384), within the
same three sites. The original result was not
an artefact of which rows could be joined, at
this test's resolution.

## 1. What was executed

The full frozen contract (spec §§3–4), under
the graph-first build (H15/H23): experiment
script `backend/scripts/phase429_f1_enlarged_join.py`;
graph module
`backend/glossa_lab/experiment_graph_phase429.py`
(node `IndusPhase429F1EnlargedJoin`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The primary test
reuses the pinned Phase-136 builder's own
statistic functions, imported from its pinned
file after its hash was asserted at gate 0.1.
The run's base was `main` at `689a5499`. The
run's committed records:

- `reports/phase429_results.json` — SHA-256
  `f08d469b95a3c72048d217965720cf2fbbab828f43ec6f6572889f80fdaf06af`
- `reports/phase429_report.md` — SHA-256
  `8cc2c154e315da0631a185f7471d3cf5dbb4aa330e1747a0f95d2f78cb821477`

Each digest was derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced the
results JSON, the report, and the
restricted-local per-row census byte-identically.

Restricted-local product (spec §7.3, named by
filename and count only): `phase429_join_census.json`
— the per-row join census against layer v2,
5,679 rows — held beside the merged catalogue
layer v2 in the restricted local store (the
main checkout's
`corpora/downloads/cisi_image_layer/catalogue/`),
never committed. No row-level merged-layer
data, and no CISI source row, enters any
committed product of this execution; the
committed products are aggregates, the gate
and type-fill censuses in aggregate form, and
this record.

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every spec
  §2 input and every source named and pinned
  at DD-067-9 recomputes to its freeze-record
  value: the committed pins (Phase-136 results
  `11a07413…`, Stage 2(a) freeze `c65a4b9b…`,
  Phase-136 builder `d5ceec46…`, Phase-141
  report `d442f8d2…`, combined Stage 2 report
  `6a4f5d26…`, canonical sign registry
  `8a0b2a82…`, Spec 034 outcome `c0cc615d…`,
  Spec 037 outcome `28e444f2…`, anchors
  `df0cf620…`, intake schema `b94d03ad…`
  (6,197 bytes), Phase-398 builder `278f16b0…`
  (40,104 bytes), intake validator
  `02b24e33…` (18,867 bytes), Phase-421 census
  `95282931…`, Phase-421 results `3948cd01…`,
  Spec 066 extension index `be20439a…`
  (78,531 bytes, 2,101 rows)), the Spec 066
  freeze digest asserted from its record
  (`0b81d842…`), and the local-store pins
  (horus84 layer `c368f290…` (1,190,884 bytes),
  CISI vol. 1 `e0d698f9…` (804,665 bytes),
  vol. 2 `e751244e…` (1,431,631 bytes), ICIT
  converted keyed layer v2 `bbfdbcd5…`
  (1,586,137 bytes)). **The merged catalogue
  layer v2 was asserted on the local file
  first, before any join work**: SHA-256
  `cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad`,
  2,655,958 bytes, and its rows and distinct
  objects counted from the file — 9,741 rows,
  5,529 distinct objects — equal to Spec 066's
  outcome pin. No INVALID class fired.
- **0.2 Original-join reproduction — PASS.**
  The original concordance join, re-run under
  its frozen exact-string rule against the
  vols. 1–2 layer, reproduces the recorded
  census **exactly**: 5,679 layer rows; 2,895
  matched; 2 ambiguous; 2,782 unmatched. It
  contributed no row to the enlarged set.
- **0.3 Object-ID join census — PASS (built
  and censused).** The join dataset was built
  by the pinned route-(b) construction itself
  (`build_intake_dataset` in the pinned
  Phase-398 module) from the pinned converted
  keyed layer: 5,018 records carrying a CISI
  object reference as `provenance.object_id`.
  The pinned Phase-130 validator returns
  verdict **pass**, 0 errors, 0 warnings.
  Resolution was against the pinned merged
  catalogue layer v2's distinct objects
  (9,741 rows; 5,529 distinct objects; by
  volume: vol. 1: 3,320 rows, vol. 2: 4,385
  rows, 3.1-portion: 2,036 rows). The census:

  | Class | Rows |
  |---|---|
  | Layer rows | 5,679 |
  | Joined (identifier resolves to exactly one distinct object in layer v2) | **4,676** |
  | Unjoined — no identifier carried | 661 |
  | Unjoined — identifier resolves to zero objects in layer v2 | 342 |
  | Ambiguous — resolves to more than one distinct object | 0 |
  | Distinct catalogue objects joined to | 3,763 |

  The more-than-one class is structurally
  empty on this layer and is reported as
  observed: resolution is against distinct
  catalogue objects keyed by their own ID
  (DD-067-9), so one identifier can resolve to
  at most one distinct object. The joined set's
  object-type mix (rows): Seals 1,969; Tablets
  2,108; Graffiti 214; Objects 53; Seal
  impressions 15; unfilled 317. The census was
  derived twice — through the intake dataset
  and directly from the lineage layer's own
  `cisi` field with the same strip the
  construction applies — and every row's joined
  classification agrees between the routes.
  Five raw-value discrepancies between the
  lineage layer and its converted form were
  found, the same five Spec 059 recorded (none
  changes any row's joined classification);
  their per-row detail is in the
  restricted-local census. The object-ID join
  adds 1,781 rows over the original concordance
  join and loses none of its rows.
- **0.4 Type-fill census — PASS (taken, before
  any F1 quantity existed).** On the **newly
  joined objects** — the 1,777 joined rows the
  Phase-421 census recorded as unjoined
  (identifier resolving to zero objects in the
  vols. 1–2 layer), resolving to 1,284 distinct
  objects in layer v2: type **filled** on 1,152
  distinct objects (1,603 rows); type
  **unfilled** on 132 distinct objects (174
  rows). Their type mix (rows): Tablets 1,018;
  Seals 379; Graffiti 145; Objects 46; Seal
  impressions 15; unfilled 174. On the **whole
  joined set** (4,676 rows, 3,763 distinct
  objects): type filled on 3,511 distinct
  objects (4,359 rows); type unfilled on 252
  distinct objects (317 rows). Restricted to
  {Seals, Tablets}: 4,077 rows. The resulting
  eligible seal/tablet strata in census form
  (restriction, then N ≥ 20 with ≥5 Seals and
  ≥5 Tablets, before any terminal mapping):
  **Harappa** (2,140 restricted rows; 431
  Seals, 1,709 Tablets), **Kalibangan** (68;
  53, 15), **Mohenjo-daro** (1,701; 1,324,
  377) — the same three sites the primary's
  own eligibility rule returns in §3. The
  intake record's expectations (126 unfilled-
  heading overlap numbers; 143 previously
  unfilled objects) were expectations, not
  results; the measured figures above are this
  census's own.
- **0.5 Gate comparison — PASS.** The bar
  adopted at DD-067-7 is joined share
  ≥ 61.0%, i.e. ≥ 3,465 of 5,679 joined rows
  (0.61 × 5,679 = 3,464.19; 3,464 rows =
  60.997% and fails), carried from Spec 059
  with no bar derived from Spec 066's
  projection. Observed: **4,676 joined rows =
  82.3384%** — 1,211 rows above the bar. The
  gate is judged on this execution's own
  census; the projection is not cited as a
  result anywhere in this record (§5).

## 3. The primary test (spec §4, frozen Phase-136 flow)

The flow on the enlarged set, unchanged in
every particular:

| Step | Count |
|---|---|
| Joined rows | 4,676 |
| Typed (catalogue object_type filled) | 4,359 — Seals 1,969; Tablets 2,108; Graffiti 214; Objects 53; Seal impressions 15 |
| Unfilled type, excluded and counted | 317 |
| Restricted to {Seals, Tablets} | 4,077 |
| Terminal mapped (W→P, frozen machinery) | 3,315 |
| Terminal UNK, excluded and counted | 762 |
| Analysis population in eligible strata | 3,181 |

Eligible strata (analysis-population rule,
mechanically: N ≥ 20, ≥5 Seals, ≥5 Tablets):
Harappa, Mohenjo-daro, Kalibangan — the
original run's three strata. Estimability
(mechanically): **estimable** — 3 eligible
strata (≥2 required) and pooled expected
counts ≥ 5 in 4 of 4 cells (100% ≥ the 80%
required); pooled 2×2 table a=432, b=1,061,
c=204, d=1,484; pooled expected counts
[298.51, 1,194.49, 337.49, 1,350.51]. No NOT
ESTIMABLE clause fired.

Per-stratum tables (a = Seals & TERMINAL14,
b = Seals & not, c = Tablets & TERMINAL14,
d = Tablets & not):

| Site | N | Seals | Tablets | a | b | c | d | Odds ratio | TERMINAL14 share, Seals | Tablets |
|---|---|---|---|---|---|---|---|---|---|---|
| Harappa | 1,695 | 340 | 1,355 | 87 | 253 | 150 | 1,205 | 2.762 | 0.256 | 0.111 |
| Mohenjo-daro | 1,435 | 1,113 | 322 | 340 | 773 | 53 | 269 | 2.232 | 0.305 | 0.165 |
| Kalibangan | 51 | 40 | 11 | 5 | 35 | 1 | 10 | 1.429 | 0.125 | 0.091 |

The test: Cochran–Mantel–Haenszel chi-square
**67.3998** (no continuity correction);
permutation raw **p = 0.0001** (B = 9,999,
seed 20261009; 0 of 9,999 permutations reached
the observed statistic); family-adjusted
**q = 0.0001** (single-test family, DD-067-8:
adjusted q equals the raw p). Mantel–Haenszel
common odds ratio **2.452**, 95% CI
**[1.965, 3.058]** (Robins–Breslow–Greenland).
Crude odds ratio 2.962 [2.464, 3.561],
labelled uncontrolled.

**Verdict mapping (§5, mechanically):** q =
0.0001 is below 0.05 and the interval
[1.965, 3.058] lies entirely above 1.5 — the
outcome is **REPLICATED**. DD-067-12's
precedence was not needed: the interval does
not include 1.0.

**Leave-one-site-out (descriptive; mints no
verdict):**

| Dropped site | Estimable | MH odds ratio | 95% CI |
|---|---|---|---|
| Harappa | yes | 2.214 | [1.611, 3.042] |
| Mohenjo-daro | yes | 2.723 | [2.026, 3.659] |
| Kalibangan | yes | 2.465 | [1.974, 3.079] |

Every dropped-site subset remained estimable
with its interval excluding 1; **no site is
load-bearing**.

**Covariate comparisons (§4.5, reported either
way; full tables in the machine record).**
Joined vs unjoined rows: joined rows are
longer on average (mean 3.64 parsed codes,
median 3, against unjoined 2.92, median 2);
preservation differs (joined: complete 2,812
of 4,676, fragment 1,320; unjoined: complete
368 of 1,003, fragment 547 — the still-silent
share is more fragmentary and shorter);
unjoined rows concentrate at Dholavira (236
of its 238 layer rows unjoined) and
Kalibangan (116 of 212), while Harappa and
Mohenjo-daro are now mostly joined (2,475 of
2,717; 1,821 of 1,923). Object type for
unjoined rows is not carried — unjoined rows
have no catalogue object — and is named as
not carried, never reconstructed. Original
joined set vs added rows: the 1,781 rows the
layer-v2 join adds over the concordance join
are shorter (mean 3.01 codes against the
original set's 4.03) and are mostly Harappa
rows (1,371 of 1,781; the original set was
mostly Mohenjo-daro, 1,412 of 2,895), with
preservation complete 1,004 / fragment 596.
Phase-421 joined set vs newly joined rows
(1,777 rows): the same picture (mean 3.01
codes; Harappa 1,369, Mohenjo-daro 408). What
the enlargement changed is therefore on
record: it chiefly brought in Harappa's
tablet-heavy rows that the vols. 1–2 catalogue
did not contain.

## 4. Claim consequences (register F067-C01…C15)

- **C01 — stands as scoped.** The outcome
  states only whether F1 replicates on the
  enlarged object-ID-joined set; it states
  nothing about meaning, sign meanings, or
  any other corpus.
- **C02 — untouched.** F1's recorded numbers
  stand exactly as cited in the headline.
- **C03 — reproduced.** The original joined
  share (2,895 of 5,679, 51.0%) was re-derived
  exactly at gate 0.2.
- **C04 — applied as ruled.** The bar was
  DD-067-7's carried 61.0% / 3,465 rows; the
  observed 4,676 rows (82.34%) clears it.
- **C05 — executed as ruled.** The join was
  built through object identifiers only, from
  the DD-067-9 sources, resolving against the
  pinned merged layer v2, and censused.
- **C06 — held.** String identity was never a
  join key: identifiers entered only as
  `provenance.object_id` provenance data; the
  gate 0.2 concordance re-run contributed no
  row to the enlarged set.
- **C07 — held in order.** Every step-0 gate's
  verdict was recorded, in order, before the
  first enlarged-set quantity; no gate failed.
- **C08 — SUPPORTED.** The replication
  hypothesis (gate-passed case) is supported:
  the outcome is REPLICATED under C11.
- **C09 — did not fire.** The enlarged set's
  interval [1.965, 3.058] does not include
  1.0, the point estimate 2.452 is not below
  1.5, and q is below 0.05.
- **C10 — executed unchanged.** The frozen
  Phase-136 flow, TERMINAL14, eligibility,
  estimability, CMH, B = 9,999, seed 20261009,
  and the MH interval were applied with the
  joined set as the only changed input.
- **C11 — applied mechanically.** REPLICATED
  by the §5 mapping alone (q < 0.05, interval
  entirely above 1.5); DD-067-12's precedence
  was not invoked.
- **C12 — not reached.** The enlarged set was
  estimable (§3); no NOT ESTIMABLE clause
  fired, on the primary's own counts or on
  the gate-0.4 census's.
- **C13 — applied as ruled.** The single-test
  family (DD-067-8): adjusted q = raw
  p = 0.0001. The closed Spec 024 family was
  not re-opened.
- **C14 — reported.** The LOSO rerun
  (descriptive; no site load-bearing) and
  both covariate comparisons are in §3 and
  in the machine record.
- **C15 — held, with the §5 re-statement
  earned.** Spec 024's and Spec 059's frozen
  records stand unedited; this outcome
  appends beside them and carries the
  re-statement §5 provides for (headline
  block). Anchors asserted byte-identical
  before and after (`df0cf620…` at both
  readings).

## 5. What this outcome does not establish

Per spec §7.4: it does not establish what the
difference means — genre, habit, and survival
remain live explanations, named as such, and
this test adjudicates nothing among them. It
says nothing about corpora outside this
lineage: results describe this lineage layer,
and its object-ID-joined subset, not the
Indus corpus in general. It says nothing
about sign meanings: TERMINAL14 is a frozen
descriptive class, and membership in it is a
fact about use, prior to any reading. And
Spec 066's projection establishes nothing
here: the gate was judged on this execution's
own census (4,676 joined rows, measured at
gate 0.3), not on any projection over grades.

Foundation check (H21) is reported at the
merge of this record, as measured, in the
landing append to this file (run on this
execution tree before the outcome commit:
**40 checks passed, 0 failed, 8 warnings** —
the standing figure; the two Holdat CSVs
were copied from the existing local downloads
for the run, the corpus CSV's SHA-256
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
verified first, and the CSVs were never
committed).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
