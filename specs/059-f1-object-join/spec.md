# Spec 059 — The Seal/Tablet Difference on a Better Join (Spec 024 F1 Rebuilt Through Object Identifiers)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the approved runnable-experiments
> campaign (owner approval 2026-10-21 of the campaign
> plan as written; campaign member 16 of 20). This
> draft is a drafting act only: **no freeze, no OSF
> filing, no execution, and no computation of any
> new quantity has been performed.** The freeze and
> the execution of Spec 059 are separate later acts
> under the campaign's freeze wave. No AEE lifecycle
> hooks have run on this draft; they are a freeze
> gate.
>
> The execution phase number is **unassigned** at
> this draft. It is allocated at the freeze act,
> from the merged record as it then stands
> (DD-059-6).

**Design source:** D-22 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-22, read in full at this draft), as triaged
RIPE on 2026-10-21
(`design-portfolio-triage-2026-10-21.md`, entry
D-22: "RUNNABLE-TODAY, step-0 gate").

**Claim under test:** `STUDY-SPEC-024/F1` —
within sites, a text's final sign falls in the
frozen TERMINAL14 class at different rates on
seals than on tablets; standing **SETTLED —
SUPPORTED** on the joined subset of one lineage
layer (odds ratio 2.384, interval [1.847, 3.077],
family q = 0.00015; stable under
leave-one-site-out in Phase-141).

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Spec 024's family member F1 (Stage 2(a),
Phase-136) asked whether the closing-sign
behaviour of inscriptions differs between seals
and tablets, once site is controlled within
site strata. Its frozen protocol
(`specs/024-evidence-integration/stage2a-freeze.md`)
joined the ICIT-lineage (horus84) layer to the
CISI catalogue by **catalogue concordance**: a
row joined if and only if its `cisi` value was
a printed catalogue ID in exactly one volume,
matched as an exact string.

The recorded flow (`reports/phase136_results.json`):

| Step | Count |
|---|---|
| ICIT-lineage layer rows | 5,679 |
| Matched (cisi in exactly one volume) | 2,895 |
| Ambiguous (value `H-311`, in both volumes) | 2 |
| Unmatched | 2,782 |
| Unjoinable-or-ambiguous share | **49.0%** (2,784 of 5,679) |
| Typed (catalogue object_type filled) | 2,752 — Seals 1,588; Tablets 1,088; Graffiti 69; Objects 7 |
| Restricted to {Seals, Tablets} | 2,676 |
| Terminal mapped (W→P, frozen machinery) | 2,195 |
| Analysis population in eligible strata | 2,062 |

The joined share of the original join is
therefore 2,895 / 5,679 = **51.0%** (50.977%
unrounded) — the figure design D-22 and this
spec's gate are stated against.

On that joined subset the test returned:
Cochran–Mantel–Haenszel chi-square 47.0047;
permutation raw p = 0.0001 (B = 9,999, seed
20261009); Mantel–Haenszel common odds ratio
**2.384**, 95% CI **[1.847, 3.077]**; verdict
**SUPPORTED** after the Spec 024 family
Benjamini–Hochberg correction (family
**q = 0.00015**, combined Stage 2 report).
Phase-141's leave-one-site-out rerun found F1
**STABLE**: every dropped-site subset remained
estimable with its odds-ratio interval
excluding 1 (drop Mohenjo-daro 2.706
[1.858–3.940]; drop Harappa 2.162 [1.541–3.033];
drop Kalibangan 2.400 [1.857–3.103]). Phase-141
minted no verdict; it qualified F1's summary
language only, and it does the same here (§4.4).

### 1.1 The question, in plain words

The result above describes only the joined
subset: 49.0% of the lineage layer's rows
could not be joined to the catalogue at all,
so half the corpus is silent in the program's
cleanest positive result. The claim's
not-understood text names the fix, and design
D-22 registers it: **the same test on a corpus
joined through object identifiers rather than
catalogue concordance** — but only if the
better join is in fact better. That condition
is this spec's step-0 gate, and it is the
spec's defining feature: if the object-ID join
does not beat the original joined share by the
design's stated margin, the design closes at
its gate, unscored, and that closure is a
pre-registered outcome of this spec, not a
failure of it.

### 1.2 The hypothesis and its falsifier

**Hypothesis (gate-passed case only).** The
seal/tablet difference in TERMINAL14 endings,
within sites, replicates on the enlarged
object-ID-joined set at comparable size.

**Falsifier.** On the enlarged set, the
within-site test's interval for the odds ratio
includes 1.0, or the point estimate falls
below 1.5 — meaning the original result was
partly an artefact of which rows could be
joined.

The hypothesis is specified **only** for the
case in which the step-0 gate passes. If the
gate fails, no hypothesis under this spec is
tested, no F1 quantity is computed on the new
join, and the claim's record gains the gate
closure and nothing else (§3.3).

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Phase-136 results (`reports/phase136_results.json`) | SHA-256 `11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022` (recomputed at this draft from `main` at `83b6a563`) |
| Spec 024 Stage 2(a) freeze (`specs/024-evidence-integration/stage2a-freeze.md`) | SHA-256 `c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c` (recomputed at this draft) |
| Phase-136 builder (`backend/scripts/phase136_terminal_type.py`) | SHA-256 `d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871` (recomputed at this draft) |
| Phase-141 report (`reports/phase141_report.md`) | SHA-256 `d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347` (recomputed at this draft) |
| Combined Stage 2 report (`reports/phase136_137_138_stage2_report.md`) | SHA-256 `6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062` (recomputed at this draft) |
| Canonical sign registry (`data/crosswalks/canonical_sign_registry.csv`) — the frozen W→P mapping substrate | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed at this draft; equals the value Phase-136 recorded for it) |
| ICIT-lineage (horus84) inscription layer (5,679 rows; local store, as at Phase-136) | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`, 1,190,884 bytes — **as recorded in `reports/phase136_results.json`**; re-asserted by recompute at the freeze |
| CISI catalogue layer, vol. 1 (`cisi_vol1_catalogue.csv`; local store, gitignored) | SHA-256 `e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e`, 804,665 bytes — **as recorded in `reports/phase136_results.json`**; re-asserted at the freeze |
| CISI catalogue layer, vol. 2 (`cisi_vol2_catalogue.csv`; local store, gitignored) | SHA-256 `e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9`, 1,431,631 bytes — **as recorded**; re-asserted at the freeze |
| Phase-130 intake schema (`data/intake/intake_dataset_schema_v1.json`, schema_version `1.0`; Spec 021) | The join route of record (§3.2). Its validator is `glossa_lab/intake.py`. The schema file's hash is asserted at the freeze from the merged record. |
| Spec 034 outcome (`specs/034-matched-object-attribution/outcome.md`) — the object-ID join precedent | SHA-256 `c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175` (recomputed at this draft) |
| Spec 037 outcome (`specs/037-cisi31-concordance-spine/outcome.md`) — the string-identity census | SHA-256 `28e444f20e698b3533559aac3a4bc3efcbc50440e79427ae58f656642886a02a` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft, fresh — not inherited from any earlier draft's pin). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**The object-ID mapping artifact is not pinned
at this draft, because it does not yet exist as
a single artifact.** Step 0 builds it (§3.2)
under the Phase-130 schema from held sources,
following Spec 034's route-(b) precedent; the
freeze names and pins the exact held source
(or sources) from which each row's object
identifier is taken, before any execution
(OPEN item OF-059-3, adjudication §5). A draft
that invented that source would be stating a
fact not on record; this draft states the
requirement instead.

## 3. Step 0 — the join gate (fail-closed, gate-first)

Execution runs these checks **in order**. The
gate is decided on census counts alone, before
any F1 quantity exists on the new join. No
failure is repaired at run time.

### 3.1 Gate 0.1 — input integrity

Every §2 input hashes to its freeze-record
value, and the Phase-130 schema validates the
join dataset built at gate 0.3 (verdict
`pass`, as Spec 034's route (b) recorded for
its dataset). A mismatch or a validation
failure stops the run as **INVALID**.

### 3.2 Gate 0.2 — original-join reproduction

The original concordance join is re-run on the
pinned layer and catalogue under its frozen
rule (exact string; a row joins iff its `cisi`
value is a printed catalogue ID in exactly one
volume), and must reproduce the recorded
census **exactly**: 5,679 layer rows; 2,895
matched; 2 ambiguous; 2,782 unmatched. A
mismatch stops the run as **INVALID** — the
gate's baseline (51.0%) is the recorded one,
and a run that cannot reproduce it has no
baseline to beat.

### 3.3 Gate 0.3 — the object-identifier join census

The join is rebuilt **through object
identifiers only**:

- Each lineage row's object identifier is
  carried as cited provenance data under the
  Phase-130 intake schema — the route Spec 034
  proved at scale (5,018 ICIT inscriptions
  admitted through the schema, validation
  verdict pass, joined on `provenance.object_id`
  only).
- A row is **joined** iff its object
  identifier resolves to **exactly one** object
  in the CISI catalogue layer. Rows resolving
  to zero catalogue objects are **unjoined**;
  rows resolving to more than one are
  **ambiguous**; both classes are counted and
  neither enters the joined set.
- **String identity is never a join key.**
  No name string, number string, `cisi` field
  string, or `cisi_number` string is matched
  as identity at any point in this join (§7.1
  states the boundary and its ground: Spec
  037's census).
- The unit of the census is the **layer row**,
  as in the original flow; if two joined rows
  resolve to the same catalogue object, both
  count as joined rows, and the distinct-object
  count is reported descriptively alongside
  (DD-059-2).
- The census reports: layer rows; joined rows
  and share; unjoined rows; ambiguous rows;
  distinct catalogue objects joined to; and
  the joined set's site and object-type mix.

### 3.4 Gate 0.4 — the gate comparison

**The bar, exactly as design D-22 states it:**
the object-ID join must raise the joined share
**above the original 51.0% by at least 10
points — to 61.0% or more.**

- Operative arithmetic at this draft: joined
  share = joined rows / 5,679, and the gate
  passes iff the share is **≥ 61.0%**, which
  on the reproduced denominator is **≥ 3,465
  joined rows** (3,464 rows = 60.997% and
  fails).
- The comparison is like-for-like: the
  original 51.0% is the matched share *before*
  any object-type restriction or terminal
  mapping (2,895 of 5,679), and the new share
  is taken at the same point in the flow —
  joined to the catalogue, before typing,
  restriction, or mapping (§4.1 then applies
  the frozen flow to the joined set).
- **Ambiguity, recorded — not silently
  resolved (OPEN item OF-059-1).** The design's
  words "by at least 10 points (to 61% or
  more)" state the percentage-points reading
  in the design's own parenthetical, and this
  draft carries that reading as operative.
  Two other readings exist and are recorded
  here so the freeze rules on them openly:
  (i) *exact-points* — original share unrounded
  (50.977%) + 10 points = 60.977%, i.e.
  ≥ 3,463 joined rows; (ii) *relative* — a 10%
  relative rise on 51.0% = 56.1%, i.e.
  ≥ 3,186 joined rows (≥ 3,185 on the unrounded
  base). The freeze confirms the operative
  reading or replaces it; until it does, the
  draft's operative bar is the design's stated
  **61.0% / 3,465 rows**, the strictest of the
  three.

### 3.5 The gate closure (pre-written)

If gate 0.4 fails, the execution **closes at
step 0, unscored**, with this wording (the
bracketed quantities filled from the census):

> "CLOSED AT STEP 0 — JOIN GATE NOT MET. The
> object-identifier join joined [n] of 5,679
> lineage rows ([x]%), against the original
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

The gate census itself is published as the
closure's finding, whichever way the gate
falls (joined / unjoined / ambiguous counts,
by route and by site), exactly as Spec 034's
gate census was published when its gate
passed.

## 4. The primary test (gate-passed case only)

Nothing in this section runs unless gate 0.4
passes. If it passes, the frozen Phase-136
flow is applied to the enlarged joined set,
**unchanged in every particular**:

### 4.1 The frozen flow on the enlarged set

1. The joined object's catalogue `object_type`
   (Class O), as in the original flow: filled /
   unfilled counted; unfilled excluded, counted.
2. Restriction to object types {Seals, Tablets};
   Graffiti and Objects excluded and reported
   descriptively, as frozen.
3. Sequence parse by the established convention
   (`re.findall(r"\d{3}", text)` in recorded
   reading order; terminal sign = last parsed
   code).
4. Terminal mapping by the frozen Spec 018 §3
   canonical map (Wells → Parpola) via the
   frozen machinery (`build_sign_maps` /
   `SignMapper.map_w` over the pinned registry,
   its frozen conflict rule); UNK terminals
   excluded, counted.
5. Stratum eligibility, mechanically: a site
   stratum enters iff its analysis-population
   N ≥ 20 and it contains ≥5 Seals and ≥5
   Tablets (the original run's eligible strata
   were Mohenjo-daro, Harappa, Kalibangan; the
   enlarged set's strata are whatever the rule
   returns, reported in full).
6. Estimability, mechanically (the frozen
   rule): the test executes iff, on the
   eligible-strata population, (i) ≥2 eligible
   strata, and (ii) the pooled 2×2 table's
   expected counts are ≥5 in at least 80% of
   its 4 cells. Failure → **NOT ESTIMABLE**,
   cell counts shown, no p-value (§5).

### 4.2 The test statistic and effect sizes

- **Statistic:** Cochran–Mantel–Haenszel
  chi-square (no continuity correction) over
  the eligible strata's 2×2 (type × outcome)
  tables; outcome = terminal mapped P sign ∈
  **TERMINAL14** = {P020, P076, P095, P099,
  P108, P125, P210, P226, P256, P346, P359,
  P378, P384, P385} (frozen, Spec 018 §3).
- **Null distribution:** permutation — within
  each stratum, object-type labels shuffled;
  B = 9,999; seed 20261009; p = (1 + #{perm ≥
  obs}) / (1 + B); Python stdlib
  `random.Random(20261009)`. No asymptotic
  p-value is reported as a result.
- **Effect sizes (reported regardless of
  verdict):** Mantel–Haenszel common odds
  ratio with 95% CI (Robins–Breslow–Greenland);
  the crude odds ratio, labelled uncontrolled;
  per-stratum odds ratios and observed
  TERMINAL14 shares by type (descriptive).

### 4.3 The family correction

The design carries the test "with the same
family correction across the Spec 024 family."
The Spec 024 family (F1/F2/F3) was corrected
once, in its combined report, and is closed;
it cannot be re-opened by this spec. This
draft therefore proposes (DD-059-4, **OPEN
item OF-059-2** for the freeze to confirm or
replace): the confirmatory family under this
spec is its single primary test, so the
Benjamini–Hochberg adjustment at q = 0.05 is
over one p-value and the adjusted q equals
the raw p. Every verdict wording in §5 is
stated in terms of that adjusted q. If the
freeze declares a wider family, the wordings
stand and the family's membership is recorded
in the freeze record before execution.

### 4.4 Leave-one-site-out (descriptive)

The Phase-141 leave-one-site-out rerun is
repeated on the enlarged set with the same
machinery and parameters, and reported
descriptively with the outcome: each
dropped-site subset's estimability, odds
ratio, and interval. As in Phase-141, LOSO
**mints no verdict** and changes no verdict
word; it qualifies the outcome's summary
language only, and the outcome record says
which sites, if any, are load-bearing.

### 4.5 The covariate comparison (reported either way)

Whether or not the test replicates, the
execution reports a stated comparison of the
**joined and unjoined rows** on every
covariate the data carries — site, object
type (for rows the catalogue types), text
length, and preservation as recorded — so the
still-silent share is at least described; and
the same comparison between the original
joined set and the rows the object-ID join
adds, so what the enlargement changed is on
record. A covariate the data does not carry
is named as not carried, never reconstructed.

## 5. Criteria fixed in advance, and pre-written verdict wordings

After all gates pass and the test is
estimable, the outcome is exactly one of
**REPLICATED**, **WEAKENED**, or **NOT
REPLICATED**, by these rules (design D-22's,
carried verbatim; precedence per DD-059-3):

- **REPLICATED:** adjusted q below 0.05 **and**
  the odds-ratio interval entirely above 1.5.
- **WEAKENED:** adjusted q below 0.05, the
  interval does **not** include 1.0, but it
  reaches below 1.5.
- **NOT REPLICATED:** adjusted q at or above
  0.05, **or** the odds-ratio interval includes
  1.0. (An interval including 1.0 is NOT
  REPLICATED even if q is below 0.05 — the
  design's falsifier names inclusion of 1.0
  first; DD-059-3.)

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- REPLICATED: "On the enlarged object-ID-joined
  set ([n] of 5,679 lineage rows, [x]%, against
  the original join's 51.0%), the seal/tablet
  difference in TERMINAL14 endings replicates
  within sites: Mantel–Haenszel odds ratio
  [r], 95% CI [lo–hi], entirely above 1.5,
  family-adjusted q = [q]. The original F1
  result was not an artefact of which rows the
  concordance join could reach, at this test's
  resolution. [LOSO sentence.] This is a
  statement about recorded use in this lineage
  layer, not about what the difference means."
- WEAKENED: "On the enlarged object-ID-joined
  set ([n] of 5,679 rows, [x]%), the seal/tablet
  difference in TERMINAL14 endings remains
  detectable within sites (family-adjusted
  q = [q]) but smaller than the original
  estimate: Mantel–Haenszel odds ratio [r],
  95% CI [lo–hi], reaching below 1.5 (original:
  2.384 [1.847–3.077] on 51.0% joined). Part of
  the original result's size was a property of
  which rows could be joined. [LOSO sentence.]"
- NOT REPLICATED: "On the enlarged
  object-ID-joined set ([n] of 5,679 rows,
  [x]%), the seal/tablet difference in
  TERMINAL14 endings does not replicate within
  sites: [family-adjusted q = [q] at or above
  0.05 / the odds-ratio interval [lo–hi]
  includes 1.0], point estimate [r] (original:
  2.384 [1.847–3.077] on 51.0% joined). The
  design's falsifier has fired: the original
  result was partly an artefact of which rows
  could be joined. The original verdict stands
  as recorded on its subset; this outcome is
  appended as its replication record.
  [LOSO sentence.]"
- NOT ESTIMABLE: "The object-ID join passed
  its gate ([n] of 5,679 rows, [x]%), but the
  enlarged set fails the frozen estimability
  rule ([failed clause]; cell counts shown in
  the record). No p-value was computed and no
  verdict under this spec exists.
  `STUDY-SPEC-024/F1` stands exactly as
  recorded."

In every gate-passed outcome, the claim's
wording gains or loses the phrase "on the
joined subset" as the evidence dictates, by
appended record only (§7.2): REPLICATED on a
materially enlarged set is the outcome under
which the phrase's scope is re-stated to the
enlarged share actually joined; WEAKENED and
NOT REPLICATED keep the phrase and add the
enlarged-set result beside it. The exact
re-statement sentence is part of the outcome
record, written from the frozen wordings
above, not improvised.

## 6. Controls and named confounders

- **Join-selection bias** is the confounder
  that motivates the design; the §4.5 covariate
  comparison is its control, and it is reported
  whether or not the test replicates. The gate
  itself is the prior control: an enlargement
  too small to change the selection is closed
  at step 0 rather than run.
- **Genre differences** (ownership marks versus
  accounts) and **preservation differences**
  between object types: the within-site design
  controls place, not kind. This limit is
  stated in the verdict wording's scope, as
  the original report stated it.
- **Compilation-internal association:** the
  lineage's transcriptions and the catalogue's
  typing were both made within one scholarly
  tradition (Phase-136's adversarial note). The
  within-site control does not imply more
  independence than exists; no output may
  present the enlarged join as independent
  corroboration of the catalogue's typing.
- **Object-type disagreement across
  compilations** (Spec 037: object type is the
  dominant conflict axis in its census). Type
  under this spec is the joined catalogue
  object's recorded type, as in the original
  test; the limit travels with the result.

## 7. Epistemic limits (binding on all outputs)

### 7.1 The string-identity boundary

This design joins on **object IDs, never on
string identity**. The ground is Spec 037's
census: of 693 CISI↔corpus exact-string
matches, 269 verified as same-object joins
under the frozen grading ladder, 341 were
CONFLICT (49.21% — mostly on object type), and
83 were UNRESOLVED. A string match is a
candidate, never an identity. Accordingly: no
step of this spec's join, census, or test may
treat equality of any string (a catalogue
number string, a name, the layer's `cisi`
field, a `cisi_number`) as evidence that two
records concern the same physical object. The
original concordance join is re-run at gate
0.2 **only** to reproduce the recorded
baseline the gate is stated against; it
contributes no row to the enlarged set.

### 7.2 The frozen outcome stands

Spec 024 F1's SUPPORTED verdict on its joined
subset is a record of its own frozen design
and is **not edited, superseded, or
re-adjudicated** by anything this spec finds.
This spec's outcome — gate closure, NOT
ESTIMABLE, or a §5 verdict — appends to the
claim `STUDY-SPEC-024/F1` as a dated
replication record beside it.

### 7.3 What no outcome establishes

- **Not what the difference means.** Genre,
  habit, and survival remain live explanations,
  named as such; this test re-measures an
  association on a larger joined share and
  adjudicates nothing among them.
- **Nothing about corpora outside this
  lineage.** Every output carries the lineage
  label and the sentence: results describe
  this lineage layer, and (gate-passed) its
  object-ID-joined subset, not the Indus
  corpus in general.
- **Nothing about sign meanings.** TERMINAL14
  is a frozen descriptive class; membership in
  it is a fact about use, prior to any reading.
- **A gate closure establishes nothing about
  the claim.** It is a statement about the
  available catalogue data's joinability
  (§3.5), and the record says so.

## 8. Risks and honest weaknesses

- **The gate may honestly fail.** The original
  join reached 51.0% by string concordance;
  whether object identifiers cover materially
  more of *this layer's* rows is exactly what
  the census measures, and a closure at step 0
  is a realistic, pre-registered outcome of
  this spec — under the campaign plan, a pass
  in which members close at step 0 with honest
  closures is a completed pass.
- **The object-ID source for this layer is
  the draft's one unpinned input** (§2,
  OF-059-3). Spec 034 proves the route at
  scale on ICIT inscriptions; it does not by
  itself prove coverage of every row of this
  layer, and the freeze must name the source
  before execution. If no held source supplies
  identifiers for this layer, the honest act
  is a drafting-stage report, not a weaker
  join.
- **Enlargement changes the strata.** Sites
  thin in the original joined set may become
  eligible, and the eligible-strata population
  will differ from the original 2,062; the
  comparison to the original result is
  therefore a replication on an enlarged set,
  not a paired re-measurement of identical
  rows — except for the §4.5 added-rows
  comparison, which is descriptive.
- **Three sites carried the original test.**
  If the enlarged set's eligibility returns
  the same three strata, the replication
  inherits that thinness; it is stated, not
  repaired.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **INVALID** — a §2 hash mismatches; the
  Phase-130 validation of the join dataset
  fails; or the original-join reproduction
  (gate 0.2) does not reproduce the recorded
  census exactly.
- **CLOSED AT STEP 0 — JOIN GATE NOT MET** —
  gate 0.4 fails: the object-ID joined share
  is below the §3.4 bar. Unscored; the §3.5
  wording is the outcome; the census is its
  finding.
- **NOT ESTIMABLE** — the gate passes but the
  enlarged set fails the frozen estimability
  rule (§4.1 step 6). Cell counts shown; no
  p-value.
- **REPLICATED**, **WEAKENED**, or **NOT
  REPLICATED** — per §5, after all gates pass
  and the test is estimable.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — integrity, original-join
   reproduction, object-ID join census, gate
   comparison. A gate failure ends the
   execution here, with the census and the
   §3.5 closure as its complete record.
3. **Primary** (§4, gate-passed only) — the
   frozen flow on the enlarged set, the test,
   LOSO, and the covariate comparisons.
4. **Outcome** (§5) — appended records only;
   anchors asserted byte-identical;
   foundation check (H21) reported as
   measured.

## 11. What this spec is not

Not a re-run or re-adjudication of Spec 024,
not a new corpus, not a string-identity join
under any relabelling, not a PRED evaluation,
and not an authorisation to execute. It is
the gate-first replication of one recorded
test on a better join — designed so that its
most likely honest outcome, closing at its
own gate, is written down before any row is
joined.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
