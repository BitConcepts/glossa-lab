# Spec 042 — Arm B Split by Object Type (a Registered Primary Variant of Spec 028 Arm B)

> ## FROZEN — 2026-10-21
>
> Drafted under the owner's 2026-10-21 order
> ("address all these remaining items now") and
> the portfolio triage of the same date
> (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`),
> which found design D-28 RIPE and the
> highest-ranked design in the PR #195 packet
> never yet taken up. **Frozen on 2026-10-21**
> under the campaign plan approved as written
> (authorisation E-1): the AEE lifecycle hooks
> passed over the recovered register
> (0.7-draft) on the DD-042-9 gate reading,
> every §2 pin was re-derived by two routes,
> and the freeze digest was computed exactly
> once over the frozen contract (`freeze.md` /
> `freeze.json`). The freeze decisions
> (DD-042-6…9) stand in `adjudication.md` §6.
> Nothing has been computed under this spec:
> the stratum census appears nowhere in the
> frozen record, by design.
>
> The execution phase is **Phase-407**,
> allocated at the freeze (DD-042-5
> discharged). Phase-400 is Spec 036's,
> Phase-401 Spec 038's, Phase-402 Spec 037's,
> and Phase-403 Spec 039's. Execution is a
> separate owner act, gated on the OSF
> registration's approval (DD-042-6).

**Design source:** D-28 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-28, read in full at this draft).

**Claim under test:** `STUDY-SPEC-028/ARM-B` —
the equal-site-weights similarity–distance
association of Spec 028's Arm B, standing
**INCONCLUSIVE**: above the margin in its
primary estimate, failed by the frozen
jackknife clause on the drop-Harappa cell.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Spec 027's Stage 1 (Phase-392) asked whether
sites' sign repertoires resemble each other
more when the sites are closer, and returned
INCONCLUSIVE: median adjusted R² 0.01677,
interval [0.01032, 0.02397], above the family's
0.01 margin — but dropping Harappa pulled the
median to 0.00928, below the margin, and the
frozen SUPPORTED rule's jackknife clause
failed. Spec 028 (Phase-393) attacked the
Harappa question directly with two
pre-registered arms:

- **Arm A** (Harappa removed entirely):
  INCONCLUSIVE — median adjusted R² 0.0087839,
  interval [0.00463, 0.01297], rejection share
  0.6231. Arm A is not this spec's subject.
- **Arm B** (equal site weights): the claim
  under this spec. Its recorded primary
  (`reports/phase393_results.json`, SHA-256
  `0a1657a8…`): 3,030 analysis records; median
  adjusted R² **0.0223721**, percentile
  interval **[0.0122174, 0.0333271]**, median
  raw R² 0.0380896, share of draws rejecting
  **0.9548**, median p 0.004. Leave-one-site-out
  medians: dropping Harappa **0.0066068** —
  the cell that failed the SUPPORTED rule's
  every-cell-above-the-margin clause — while
  the other recorded cells stand above the
  margin (Mohenjo-daro 0.0237627, Dholavira
  0.0243568, Lothal 0.0247476). Verdict:
  **INCONCLUSIVE**.

Spec 028 also ran an **exploratory** Arm C,
which produced the clue this design exists to
test: Harappa's repertoire profile differs
from the pooled other sites far more among
**tablets** (dissimilarity 0.4952733) than
among **seals** (0.1113521). Arm C was
exploratory description, not a registered
test; its numbers are a hypothesis source,
nothing more, and this spec does not promote
them by citing them.

### 1.1 The question, in plain words

Arm B's pooled test may be mixing two
different stories: a seal story, in which
sites look alike and Harappa is unexceptional,
and a tablet story, in which Harappa genuinely
differs. Split the primary test by object
type — seals alone, tablets alone, each under
the frozen rules — and find out which story,
if either, the data tell. This is a new
pre-registered variant of a frozen test; the
frozen Arm B outcome stands untouched beside
whatever this spec finds.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The similarity–distance
association, equally weighted, differs by
object type: the seal stratum survives the
full site jackknife including drop-Harappa;
the tablet stratum is where the Harappa
dependence concentrates.

**Falsifier.** The strata behave alike — both
survive or both fail the jackknife the same
way — in which case object type is exonerated
and the Harappa dependence is a whole-corpus
property, stated as such.

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the Phase-393 layer, 5,679 records | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft from `main`) |
| Phase-393 results (`reports/phase393_results.json`) | SHA-256 `0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607` (recomputed at this draft) |
| Phase-393 machinery (`specs/028-harappa-robustness/pipeline393.py`) | SHA-256 `6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e` (recomputed at this draft) |
| Spec 028 margins audit (`specs/028-harappa-robustness/margins-audit.json`) | SHA-256 `15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d` (recomputed at this draft) |
| Spec 028 freeze record (`specs/028-harappa-robustness/freeze.json`) | SHA-256 `376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. The pin is stated from a fresh recompute because the last draft to carry one (Spec 040's) was found stale at its gate — its `eccea6d5…` no longer recomputes. |

The population flow of record (Phase-393,
frozen): 5,679 layer records → 4,531 after
dedup → 4,505 provenanced → 3,605 seal/tablet
records → 3,144 eligible primary → **3,030
analysis records** at 6 sites (Chanhu-daro,
Dholavira, Harappa, Kalibangan, Lothal,
Mohenjo-daro). The Arm B analysis population
is those 3,030 records; every one of them is
recorded as object type SEAL or TAB by the
frozen flow's construction.

## 3. Step 0 — gates before any stratum quantity (fail-closed)

Execution runs these checks in order, before
any repertoire quantity is computed for either
stratum. A failure stops the execution in the
class named; nothing is repaired at run time.

- **0.1 Input integrity.** Every §2 input
  hashes to its freeze-record value. A
  mismatch stops the run as **INVALID**.
- **0.2 Population reproduction.** The frozen
  population flow, re-run on the pinned layer,
  reproduces the recorded flow counts exactly
  (5,679 / 4,531 / 4,505 / 3,605 / 3,144 /
  3,030) and the recorded Arm B analysis set.
  A mismatch stops the run as **INVALID**.
- **0.3 Partition census.** The analysis
  population is partitioned by recorded object
  type. The census reports, per stratum and
  per site, the inscription counts, and asserts
  the two strata's counts sum to 3,030. A
  record whose type is neither SEAL nor TAB
  stops the run as **INVALID** — the frozen
  flow admits none, so one appearing is a
  machinery finding, never a silent drop.
- **0.4 Stratum floors (margins only).** A
  stratum enters the test only if at least
  **6 sites** each carry at least **20
  inscriptions** of its type. A stratum below
  the floor is recorded **TOO THIN** with its
  counts. If either stratum is TOO THIN, the
  execution closes at this gate with headline
  **THIN** and neither stratum is computed:
  the headline under this spec is the pattern
  across strata, and a one-stratum result
  quoted alone would misstate the test
  (DD-042-2).
- **0.5 Pooled regression.** The un-split Arm B
  machinery, run on the full analysis
  population under the recorded design and
  seed (20261012), reproduces the recorded
  primary quantities exactly: median adjusted
  R² 0.0223721, interval [0.0122174, 0.0333271],
  rejection share 0.9548, and every recorded
  leave-one-site-out median, including
  drop-Harappa's 0.0066068. Any mismatch stops
  the run as **INVALID** — the primary does
  not proceed on machinery that cannot first
  reproduce its own frozen result.

## 4. The primary test

For each stratum separately, Phase-393's
Arm B machinery runs **unchanged**: the same
similarity–distance estimator (adjusted
PERMANOVA-style R² over repertoire profiles
against geographic distance), the same equal
site weights with the recorded quota scheme,
the same draw design and seed, the same
negative and positive controls, and the same
practical margin — adjusted R² **0.01**. The
only change from the frozen Arm B run is the
population: the stratum's records only.
Object types are as recorded in the corpus;
no record is re-typed, and the two strata are
computed independently, each with its own
full site jackknife (every site dropped in
turn, drop-Harappa named in advance in both).

### 4.1 Per-stratum verdicts (the frozen family's rules, verbatim)

Within a stratum whose controls pass:

- **SUPPORTED** iff the stratum's primary
  median adjusted R² is > 0.01 **and** every
  leave-one-site-out median adjusted R² of
  that stratum is > 0.01.
- **CONTRADICTED** iff (≥ 95% of the stratum's
  primary draws fail to reject **or** the
  stratum's adjusted R² percentile interval
  lies entirely at or below 0.01).
- **INCONCLUSIVE** iff neither fires.

If a stratum's controls fail, that stratum is
**NOT ADJUDICATED** — a machinery finding,
not a verdict — and the headline is NOT
ADJUDICATED with the failing control named
(DD-042-3).

### 4.2 The headline pattern (fixed in advance)

The execution's headline outcome is exactly
one of:

- **SPLIT** — one stratum SUPPORTED and the
  other not SUPPORTED (CONTRADICTED or
  INCONCLUSIVE). A SPLIT is reported with its
  direction: **SPLIT AS PREDICTED** (seal
  stratum SUPPORTED, tablet stratum not) or
  **SPLIT REVERSED** (tablet SUPPORTED, seal
  not). A reversed split defeats the
  falsifier's "alike" but does **not** support
  the §1.2 hypothesis as stated; the outcome
  record says so in its first paragraph.
- **UNIFORM-PASS** — both strata SUPPORTED.
- **UNIFORM-FAIL** — neither stratum
  SUPPORTED, in any combination of CONTRADICTED
  and INCONCLUSIVE.
- **THIN** — closed at gate 0.4.

UNIFORM-PASS and UNIFORM-FAIL are the
falsifier's outcomes: the strata behaved
alike, and object type stands exonerated as
the locus of the Harappa dependence — which
is itself a finding the claim's record needs,
stated with the same prominence as a split.

### 4.3 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- SPLIT AS PREDICTED: "Split by object type,
  the Arm B association survives the full site
  jackknife on seals (median adjusted R²
  [x], every leave-one-site-out median above
  0.01) and does not survive it on tablets
  (median adjusted R² [y]; the failing
  jackknife cell is [site], median [z]). The
  Harappa dependence in Spec 028's Arm B is
  localised to the tablet stratum of this
  corpus layer. This is a statement about
  where an association sits, not about why,
  and not about movement of people."
- SPLIT REVERSED: "Split by object type, the
  strata diverge against the direction the
  exploratory Arm C clue suggested: the tablet
  stratum is SUPPORTED and the seal stratum is
  not. The hypothesis as stated in Spec 042
  §1.2 is not supported. [Quantities.]"
- UNIFORM-PASS: "Split by object type, both
  strata are SUPPORTED under the frozen rules.
  Object type is exonerated as the locus of
  the Harappa dependence: the dependence
  recorded in pooled Arm B does not reproduce
  as a stratum property under this test.
  [Quantities.]"
- UNIFORM-FAIL: "Split by object type,
  neither stratum is SUPPORTED (seals:
  [verdict]; tablets: [verdict]). Object type
  is exonerated as the locus of the Harappa
  dependence; the dependence is a whole-corpus
  property of this layer under this test.
  [Quantities.]"
- THIN: "The object-type split cannot be run
  as designed: the [seal/tablet] stratum
  carries fewer than six sites with at least
  twenty inscriptions of its type ([census]).
  No stratum quantity was computed. Spec 028
  Arm B stands exactly as recorded."

## 5. Controls and named confounders

- **Object-type mix is site-dependent.** That
  is the confounder that motivates the design;
  stratification is the control, and each
  stratum's site census is published with its
  result.
- **Harappa's weight in the tablet stratum.**
  Harappa carries the largest tablet share in
  this layer (in Arm B's recorded per-draw
  quotas, 39 of 59 tablet allocations). Equal
  site weights are the machinery's mitigation,
  not a cure; the stratum census and the
  drop-Harappa cell are reported where a
  reader cannot miss them.
- **Preservation differences between seals
  and tablets** are described per stratum in
  every outcome product (the recorded
  preservation distribution over each
  stratum's records), never adjusted away
  silently.
- **Period mix** is likewise described per
  stratum and carried in the outcome wording.
  Period is **not** controlled under this
  spec: the period-controlled variant of the
  movement test is design D-26, which is
  blocked on a site × local-label → coarse-
  period mapping that does not exist (Spec 040
  dependency-gate record). The two designs are
  complementary and are not merged.
- **Object type is one compilation's
  recording.** Spec 037's census found the
  CISI volumes and the program's corpus
  classify matched objects' types differently
  in 49% of cases. This test uses type only
  as recorded *within* the Phase-393 layer,
  consistently for both strata; the limit is
  stated wherever the result is stated.

## 6. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the corpus label — the Phase-393 layer
   (the Yajnadevam-compiled inscription file
   as held by the program), with its lineage
   posture as recorded in Specs 027/028;
2. the stratum census of gate 0.3/0.4;
3. per stratum: median adjusted R², the
   percentile interval, the rejection share,
   the minimum leave-one-site-out median and
   the site that produced it, and the
   per-stratum verdict word;
4. the headline pattern word of §4.2 (with
   direction, for a SPLIT);
5. the fence sentence: "This result is about
   repertoire association in recorded data. It
   is not evidence that any population moved."

Deliverables at execution: a results JSON
(censuses, per-stratum primaries and
jackknives, control outcomes, the regression
record of gate 0.5), a report under these
headline rules, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 7. Epistemic limits (binding on all outputs)

1. **No movement conclusion.** Even a clean,
   stratum-resolved association is consistent
   with goods and habits moving without
   populations moving; Spec 027's
   ecological-fallacy fence binds this spec's
   wording exactly as it bound the
   originals'.
2. **No mechanism conclusion.** The test
   localises a dependence; it does not say
   why tablets would differ. Genre,
   administration, and chronology all remain
   live explanations, named as such.
3. **The frozen outcome stands.** Spec 028's
   Arm B INCONCLUSIVE verdict on the pooled
   population is a record of its own design
   and is not edited, superseded, or
   re-adjudicated by anything this spec finds.
   This spec's outcome appends to the claim
   `STUDY-SPEC-028/ARM-B` as a dated,
   stratum-resolved record beside it.
4. **The Arm C clue stays exploratory.** A
   SPLIT AS PREDICTED would make the split a
   registered finding; it would not
   retroactively make Arm C's description a
   test, and no output may cite the 0.4953 /
   0.1114 figures as evidence — only as the
   hypothesis's source.
5. Negative, uniform, thin, and
   not-adjudicated outcomes publish with the
   same prominence as a split.

## 8. Risks and honest weaknesses

- **The tablet stratum may be thin or
  Harappa-bound.** The floor at gate 0.4
  exists because this design may honestly
  close unrun, and if it runs, the tablet
  stratum's site balance is Harappa-heavy by
  construction of the surviving record.
- **Six sites is few.** Each jackknife cell
  is load-bearing; that is inherited from the
  family design (Phases 392/393) and is
  stated, not repaired.
- **Type labels are compilation-relative**
  (§5). Within one layer the split is
  well-defined; across compilations it is
  not claimed to be.
- **A reversed split is a real possibility**
  the design must not bury: Arm C's clue is
  one exploratory description, and §4.2
  pre-writes the reversed wording so it
  cannot be softened after the fact.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **THIN** — gate 0.4 fails for either
  stratum. No stratum quantity is computed.
- **INVALID** — a §2 hash mismatches; the
  population does not reproduce (0.2); the
  partition census fails (0.3); or the pooled
  regression fails (0.5).
- **NOT ADJUDICATED** — a stratum's controls
  fail at the primary.
- **SPLIT** (AS PREDICTED or REVERSED),
  **UNIFORM-PASS**, or **UNIFORM-FAIL** —
  per §4, after all gates pass.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — integrity, population
   reproduction, partition census, stratum
   floors, pooled regression.
3. **Primaries** (§4) — seal stratum, tablet
   stratum, each with controls and the full
   jackknife.
4. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 11. What this spec is not

Not a re-run or re-adjudication of Spec 028,
not a period control (that is D-26, blocked),
not a new corpus, not a PRED evaluation, and
not an authorisation to execute. It is the
object-type split of one recorded test,
designed so that its honest outcomes —
including closing thin at its own gate — are
written down before any stratum is computed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
