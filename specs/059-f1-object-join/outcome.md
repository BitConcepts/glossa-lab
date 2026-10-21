# Spec 059 / Phase-421 — Outcome record (EXECUTED 2026-10-21 — CLOSED AT STEP 0 — JOIN GATE NOT MET)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 059 contract
> (freeze digest
> `bba1caca1885c2146515b437963619dff6737b4fc321a683f0dce9a56b5aed58`),
> as **Phase-421**, in Wave 3 group 2 of the
> runnable-experiments campaign (plan approved
> AS WRITTEN on 2026-10-21). The execution gate
> was satisfied before the run: OSF registration
> **yfw7h** is APPROVED + PUBLIC (DOI
> 10.17605/OSF.IO/YFW7H; verified by API
> read-back at the run: `reviews_state`
> accepted, `public` true). Outcome: **CLOSED
> AT STEP 0 — JOIN GATE NOT MET** — gate 0.4
> failed on observed counts. No F1 quantity was
> computed, no verdict under this spec exists,
> and `STUDY-SPEC-024/F1` stands exactly as
> recorded.

## Headline (spec §3.5 wording, filled from the census)

> "CLOSED AT STEP 0 — JOIN GATE NOT MET. The
> object-identifier join joined 2899 of 5,679
> lineage rows (51.05%), against the original
> concordance join's 51.0% and the gate fixed
> in advance at 61.0% or more. The enlarged
> joined set this design required does not
> exist on the available catalogue data, so no
> F1 quantity was computed and
> `STUDY-SPEC-024/F1` stands exactly as
> recorded — SUPPORTED on its original joined
> subset, its 'on the joined subset' scope
> unchanged. The unjoined share is a measured
> property of the available catalogue data,
> not an oversight. The unblocking act is a
> more complete published object catalogue
> entering through Phase-130 intake."

Claim: `STUDY-SPEC-024/F1` — SETTLED —
SUPPORTED on its original joined subset
(Mantel–Haenszel odds ratio 2.384, 95% CI
[1.847, 3.077], family q = 0.00015), unchanged.
This record is the claim's dated replication
record under spec §7.2: it appends beside the
frozen record and edits nothing in it. No
"on the joined subset" re-statement arises:
§5 provides for one only in a gate-passed
outcome, and the §3.5 wording above states
the scope is unchanged.

What this closure means, in plain words: the
original test could only reach the half of
the lineage layer whose catalogue references
matched the printed catalogue by exact string.
This spec asked whether routing the same rows
through object identifiers — the catalogue's
own object IDs, carried as provenance data —
would reach materially more of the layer. It
reaches four more rows. The better join the
design required does not exist on the
catalogue data the programme holds, so the
replication test was not run, by the frozen
design's own rule, written before any row was
joined.

## 1. What was executed

Step 0 only (spec §3, gates in frozen order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase421_f1_object_join.py`;
graph module
`backend/glossa_lab/experiment_graph_phase421.py`
(node `IndusPhase421F1ObjectJoin`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The script carries
the §4 machinery (the pinned Phase-136
builder's own statistic functions, imported
from its pinned file) behind the gate check;
that machinery was not reached and did not
run. The run's base was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`.
The run's records:

- `reports/phase421_results.json` — SHA-256
  `3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f`
- `reports/phase421_join_census.json` — SHA-256
  `952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8`
  (the per-row gate census: identifier
  provenance and resolution class for all
  5,679 layer rows — the join's audit under
  DD-059-11)
- `reports/phase421_report.md` — SHA-256
  `167584e18284667715b7aea31d111bd7185c11f8f86aac9b425f964f6553b064`

Each digest was derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced all
three output files byte-identically.

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every spec
  §2 input and every object-identifier source
  named and pinned at DD-059-9 recomputes to
  its freeze-record value, in the foreground
  by two independent routes (the GitHub
  contents API and the git-blob route, both at
  the run's base commit, for the twelve
  committed pins; Python `hashlib` and
  `sha256sum` for the four local-store pins):
  Phase-136 results `11a07413…`, Stage 2(a)
  freeze `c65a4b9b…`, Phase-136 builder
  `d5ceec46…`, Phase-141 report `d442f8d2…`,
  combined Stage 2 report `6a4f5d26…`,
  canonical sign registry `8a0b2a82…`, Spec
  034 outcome `c0cc615d…`, Spec 037 outcome
  `28e444f2…`, anchors `df0cf620…`, intake
  schema `b94d03ad…` (6,197 bytes), Phase-398
  builder `278f16b0…` (40,104 bytes), intake
  validator `02b24e33…` (18,867 bytes); horus84
  layer `c368f290…` (1,190,884 bytes), CISI
  vol. 1 `e0d698f9…` (804,665 bytes), vol. 2
  `e751244e…` (1,431,631 bytes), ICIT
  converted keyed layer v2 `bbfdbcd5…`
  (1,586,137 bytes). The phase machinery
  re-asserted the same pins in the worktree
  during the run. The schema-validation half
  of this gate is recorded at gate 0.3, where
  the dataset is built: verdict **pass**
  (below).
- **0.2 Original-join reproduction — PASS.**
  The original concordance join, re-run under
  its frozen exact-string rule, reproduces
  the recorded census exactly: 5,679 layer
  rows; 2,895 matched; 2 ambiguous; 2,782
  unmatched. The gate's baseline (51.0%,
  50.977% unrounded) is the recorded one.
- **0.3 Object-ID join census — PASS (built
  and censused).** The join dataset was built
  by the pinned route-(b) construction itself
  (`build_intake_dataset` in the pinned
  Phase-398 module) from the pinned converted
  keyed layer: 5,018 records carrying a CISI
  object reference as `provenance.object_id`.
  The pinned Phase-130 validator returns
  verdict **pass**, 0 errors, 0 warnings —
  the same verdict Spec 034's route (b)
  recorded for its dataset. Resolution was
  against the pinned catalogue layer's
  distinct objects in the merged vols 1–2
  layer (7,705 rows; 3,493 distinct objects;
  vol. 1: 3,320 rows / 1,475 distinct IDs;
  vol. 2: 4,385 rows / 2,019 distinct IDs; one
  ID, `H-311`, in both volumes — one distinct
  object in the merged layer). The census:

  | Class | Rows |
  |---|---|
  | Layer rows | 5,679 |
  | Joined (identifier resolves to exactly one distinct object) | **2,899** |
  | Unjoined — no identifier carried | 661 |
  | Unjoined — identifier resolves to zero objects | 2,119 |
  | Ambiguous — resolves to more than one distinct object | 0 |
  | Distinct catalogue objects joined to | 2,479 |

  The more-than-one class is structurally
  empty on this layer and is reported as
  observed: resolution is against distinct
  catalogue objects keyed by their own ID
  (DD-059-9), so one identifier can resolve
  to at most one distinct object. The joined
  set's object-type mix (the joined catalogue
  objects' recorded types): Seals 1,590;
  Tablets 1,090; Graffiti 69; Objects 7;
  unfilled 143. The joined set's site mix and
  the full by-site table are in the machine
  record. The census was derived twice —
  through the intake dataset and directly
  from the lineage layer's own `cisi` field
  with the same strip the construction
  applies — and every row's joined
  classification agrees between the routes.
  Five raw-value discrepancies between the
  lineage layer and its converted form were
  found and are recorded per row in the
  census (none changes any row's joined
  classification): a trailing tab on
  `H-1734` (row 967; resolves zero either
  way), trailing spaces on `L-78` (row 2793)
  and `M-929` (row 4177), leading spaces on
  the inscription ID at row 3079 (its
  identifier `M-1917` resolves zero either
  way), and row 4861, where the lineage layer
  carries `-` (no reference) and the
  converted form carries `W-1` (resolves zero
  either way; this one row is why the
  no-identifier count is 661 on the dataset
  route and 662 on the lineage-direct route,
  with the zero-resolution count 2,119 /
  2,118 — the joined and unjoined totals are
  identical).
- **0.4 Gate comparison — FAIL (the execution
  closes here).** The bar adopted at DD-059-7
  is joined share ≥ 61.0%, i.e. ≥ 3,465 of
  5,679 joined rows (0.61 × 5,679 = 3,464.19;
  3,464 rows = 60.997% and fails). Observed:
  **2,899 joined rows = 51.0477%** — a
  shortfall of **566 rows** (9.95 points)
  against the bar. The refused exact-points
  (≥ 3,463) and relative (≥ 3,186 / ≥ 3,185)
  readings were not revived; the observed
  count falls below every one of the three
  readings, so no reading of the bar changes
  this closure. The object-ID join adds
  exactly **4 rows** over the original join
  and loses none: the two `H-311` rows
  (1333.1, 1333.2 — ambiguous under the
  per-volume concordance rule, exactly one
  distinct object in the merged layer) and
  the two rows whose references carry
  trailing spaces in the lineage layer
  (`L-78`, row 2793; `M-929`, row 4177),
  which the route-(b) construction's strip
  carries cleanly. Every other row the
  concordance join could not reach carries
  either no reference at all (661 rows) or a
  reference to an object the available
  catalogue does not contain (2,119 rows) —
  a property of the available catalogue
  data, measured here for the first time
  under this join route.

## 3. What was not done

The §4 primary test did not run: no terminal
mapping, no eligibility or estimability
computation on an enlarged set, no CMH
statistic, no permutation, no p-value or
q-value, no odds ratio, no leave-one-site-out
rerun, and no covariate comparison under
§4.5 (that section belongs to the gate-passed
case; the gate census above is this closure's
complete finding, and its by-site and
object-type tables describe the joined and
unjoined shares as far as the frozen closure
provides). No Spec 024 record was edited;
the family correction of DD-059-8 had no
p-value to adjust. The claim's record gains
this gate closure and nothing else (§1.2).

## 4. Claim consequences (register F059-C01…C15)

- **C01 — stands as scoped.** The outcome
  states only the gate result; it states
  nothing about whether F1 replicates,
  because no replication was run.
- **C02 — untouched.** F1's recorded numbers
  stand exactly as cited in the headline.
- **C03 — reproduced.** The original joined
  share (2,895 of 5,679, 51.0%) was
  re-derived exactly at gate 0.2.
- **C04 — applied as ruled.** The bar was
  DD-059-7's adopted 61.0% / 3,465 rows; the
  observed 2,899 rows fall below it (and
  below both refused readings).
- **C05 — executed as ruled.** The join was
  built through object identifiers only,
  from the DD-059-9 sources, and censused.
- **C06 — held.** String identity was never
  a join key: identifiers entered only as
  `provenance.object_id` provenance data;
  the gate 0.2 concordance re-run
  contributed no row to the joined set (its
  2,895 rows are a baseline, and the joined
  set was counted independently — the 4
  added rows are precisely rows the
  concordance rule did not join).
- **C07 — fired as designed.** The execution
  stopped at the step-0 gate failure before
  any enlarged-set quantity was computed.
- **C08 — unjudged.** The replication
  hypothesis is specified only for the
  gate-passed case (§1.2); the gate failed,
  so it was not tested — neither supported
  nor falsified by this execution.
- **C09 — not reached.** No interval exists
  on an enlarged set; the falsifier did not
  fire and could not.
- **C10 — not run.** The frozen Phase-136
  test was not applied to any enlarged set.
- **C11 / C13 — not reached.** No verdict
  mapping was applied and no q exists; the
  single-test family (DD-059-8) is recorded
  in the freeze and stands for any later
  act, not used here.
- **C12 — not reached.** NOT ESTIMABLE
  belongs to the gate-passed case; this
  execution closed one gate earlier.
- **C14 — not reached.** The LOSO rerun and
  covariate comparisons are gate-passed
  reporting obligations (§§4.4–4.5).
- **C15 — held.** Spec 024's frozen verdict
  and records stand unedited; this outcome
  appends beside them. Anchors asserted
  byte-identical before and after
  (`df0cf620…` at both readings).

## 5. What this outcome does not establish

Per spec §7.3: a gate closure establishes
nothing about the claim. It does not show
the seal/tablet difference is or is not
real beyond its original joined subset; it
does not say what the difference means
(genre, habit, and survival remain live
explanations); it says nothing about corpora
outside this lineage layer; and it says
nothing about sign meanings. It establishes
one measured fact: on the catalogue data
available to the programme, routing this
layer's rows through object identifiers
joins 2,899 of 5,679 rows (51.05%) — four
more than catalogue concordance joined —
which is below the enlargement the design
required before re-testing. The unblocking
act named in the frozen wording is a more
complete published object catalogue entering
through Phase-130 intake.

Foundation check (H21) is reported at the
merge of this record, as measured, in the
landing append to this file.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
