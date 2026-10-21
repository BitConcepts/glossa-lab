# Spec 060 — The Holdat Site Effect: Margin Curve and Shared Population (a Residue Study of Spec 024 F2)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments campaign
> approved by the owner on 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4; member 17 of the twenty), and the
> portfolio triage of the same date
> (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`),
> which found design D-23 RIPE and recorded the
> drafting correction this draft carries in §2.2
> and claim F060-C05. **The freeze and the
> execution of Spec 060 are separate later owner
> acts.** No AEE lifecycle hooks have run on this
> draft; they are a freeze gate. Nothing in this
> draft has been run, frozen, registered, or
> computed.
>
> The execution phase number is **unassigned**
> at this draft. It is allocated at the freeze
> act, from the merged record as it then stands
> (DD-060-5).

**Design source:** D-23 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-23, read in full at this draft).

**Claim under test:** `STUDY-SPEC-024/F2-HOLDAT` —
the site-repertoire effect on the Holdat
compilation layer, standing **SETTLED —
CONTRADICTED at the declared margin**: the
Phase-384 rerun's governing interval for the
effect is [0.059, 0.078], entirely below the
0.10 margin fixed in advance; the descriptive
value in this layer had been 0.1154.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Spec 024's family asked, in two compilation
layers, whether different sites use different
sign repertoires. In the ICIT lineage (F3) the
answer came out one way; in the Holdat layer
(F2) the other. Phase-137 (Spec 024) measured
both layers with one design; Phase-384
(Spec 026's rerun, corrected procedure v2)
then put a bias-corrected interval on each
layer's effect size, judged against the margin
the family had declared in advance — Cramér's
V = 0.10, the size the program agreed to care
about. The record of that rerun
(`reports/phase384_results.json`) is:

- **F2, Holdat layer:** 1,670 analysis
  inscriptions; point V **0.1154**; governing
  (basic bootstrap) interval **[0.0589,
  0.0778]** — its upper bound below 0.10, so
  the bounded claim is **CONTRADICTED at the
  declared margin**. The original
  composition-controlled permutation on this
  layer (Phase-137) had already returned NOT
  SUPPORTED (raw p = 0.7354); the two routes
  converge and neither is edited here.
- **F3, ICIT lineage:** 5,410 analysis
  inscriptions; point V **0.2190**; governing
  interval **[0.1823, 0.2104]** — entirely
  above 0.10, so **SUPPORTED stands at the
  declared margin**.

The same question, answered in two layers,
produced intervals that do not come near each
other. Two residues from that record are this
spec's whole subject, and both are stated in
the design before any method:

1. **Margin-dependence.** The F2 verdict is
   "contradicted *at 0.10*" — an honest
   verdict, but what anyone citing F2 can
   use depends on how the answer moves with
   the margin, and that curve has never been
   published as the primary object.
2. **The layer disagreement.** Phase-125
   showed the compilations themselves
   disagree beyond noise, so the Holdat
   result may be a fact about the Holdat
   compilation rather than about ancient
   cities.

### 1.1 The question, in plain words

First: show the F2 verdict as a function of
the margin, on a grid fixed in advance, so
the verdict's shape is on the record where
anyone citing F2 will meet it. Second: put
both layers on the population they share —
the same sites, the same object types — and
ask whether their effect sizes then move
toward each other. If they do, the layer
disagreement is substantially a difference
in what the two layers contain. If they do
not, the disagreement lives in how the
compilations treat signs, and §2.2 states —
against the finished record, not against a
pending study — what that outcome means.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** On the population the two
layers share (same sites, same object types),
the Holdat effect and the ICIT effect move
toward each other — that is, the layer
disagreement is substantially a composition
difference.

**Falsifier.** On the shared population the
two layers' effect intervals still exclude
each other — the disagreement then lives in
the compilations' sign treatment, not in
their composition.

The design as written in the packet routed
that falsifier outcome to a next step that
no longer exists in the form the design
assumed. §2.2 records the correction; the
falsifier itself is unchanged.

## 2. The corrected hand-off (read before the method)

### 2.1 What the design said

Design D-23's falsifier paragraph ends: "the
disagreement then lives in the compilations'
sign treatment, and D-20's attribution becomes
the governing next step (the design says so in
advance, so the hand-off is pre-registered,
not improvised)."

### 2.2 What the record now is

D-20 is **complete**. It was executed as
**Spec 034** (Phase-398, 2026-10-13) and its
verdict is **ATTRIBUTED TO COMPOSITION**: on
169 matched objects — the same physical
objects read in
 both compilations,
carrying texts of three or more signs in both
— the two compilations' positional profiles
agree almost exactly (median distance
**0.025694**, at or below the frozen 0.20
composition line; the 0.32 transcription
falsifier nowhere near firing), leaving a
residual of **0.0403** of the corpus-level
disagreement where Phase-131 had left 93.9%
unexplained. The caveat the design required
travels with the answer: the 169 matched
objects are **all Mohenjo-daro seals**.

### 2.3 What this draft does about it

Arm 2 (§5) is written **against that finished
record**, in three ways:

1. Arm 2 does not wait for, cite as pending,
   or re-run any part of D-20. Spec 034's
   verdict is an input to this spec's
   reasoning, pinned in §3 like any other
   input.
2. If arm 2's falsifier fires (COMPOSITION
   DOES NOT, §5.2), the outcome is stated as
   a measured tension **alongside** Spec
   034's finished attribution, in the
   pre-written wording of §6.3: on matched
   objects the compilations agree and the
   Phase-125 disagreement is composition;
   on the shared site-and-type population the
   two layers' site effects still exclude
   each other. Both statements stand; neither
   edits the other. What the tension points
   to — the layers' site-effect estimation,
   their sign treatment at repertoire level,
   or selection beyond the matched slice —
   is **not** adjudicated by this spec, and
   no output may present a new attribution
   study as already designed or already
   governing. Any successor is a new design
   through its own planning gate.
3. If arm 2 finds COMPOSITION EXPLAINS THE
   GAP, that result is consonant with Spec
   034's attribution and is reported as a
   second, independent composition finding —
   on a different question (site effects, not
   positional profiles) and a different
   population (six shared sites, not one
   site's seals). It does not extend Spec
   034's slice, and no output may cite it as
   widening the matched-object result.

This correction is recorded openly here and
in `adjudication.md` §2, as the campaign plan
(Part 3) and the triage both require. The
design governs this spec's substance in every
other respect.

## 3. Inputs (pinned at this draft; re-asserted at the freeze)

The two corpus layers are **not in this
repository**: they are held files, named in
the Phase-137 record by the paths its loaders
used. Their pins below are the SHA-256 values
**recorded in that record** — the only pins
that exist for them — and step 0 (§4) requires
the execution venue's copies to hash to
exactly those values before anything is
computed. Every other pin was recomputed
first-hand at this draft from `main` (commit
`83b6a563…`, 2026-10-21) through the
repository's own records.

| Input | Pin / state |
|---|---|
| Holdat layer (`indus_corpus 2.csv`, holdatllc_indus export as held at Phase-137) — 7,002 token rows, 1,670 inscriptions | SHA-256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e` **as recorded in** `reports/phase137_results.json` (F2 `input.sha256`); re-asserted against the held file at step 0 |
| ICIT-lineage layer (`inscriptions.csv`, horus84 as held at Phase-137) — 5,679 rows, 5,410 analysis inscriptions | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef` **as recorded in** `reports/phase137_results.json` (F3 `input.sha256`); re-asserted against the held file at step 0 |
| Phase-137 results (`reports/phase137_results.json`) | SHA-256 `18f86f45892526b947a4a7447201be9d69584ec96d33a1d18139309b9dc2a7a1` (recomputed at this draft) |
| Phase-137 machinery (`backend/scripts/phase137_site_repertoire.py`) — the loaders and the frozen population rule | SHA-256 `e00dacf4df8f52871b482e36ca0a37f66503c5f1b107ee835ac99fa21dfc8c86` (recomputed at this draft) |
| Phase-384 results (`reports/phase384_results.json`) | SHA-256 `dda6092d9f4d368869a6e3a590948dfa97d02c5db50bf75868d6e055f0896aad` (recomputed at this draft) |
| Phase-384 estimator, v2 (`backend/scripts/phase384_stage2_margins_v2.py`) | SHA-256 `3313394e6a716898cdfd440a46333ebd2b9136b77306413ed1514eab322a72a5` (recomputed at this draft; **matches** the Phase-384 freeze-v2 sources record) |
| Phase-384 contract v2 (`specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md`) | SHA-256 `f0a67bd766ae28a33edc33553613bf9c50cc933df1bfbe2b5e1192d6571bbc75` (recomputed at this draft; **matches** the freeze-v2 sources record) |
| Phase-384 freeze v2 (`specs/026-rcph-framework-transfer/reruns/phase384-freeze-v2.json`) | File SHA-256 `5749c6b89ac26be6333e0c20457bc320ca624c15f5ca65e689c107aa12b7b8e9`; freeze digest recorded inside it `4e6c78bc917c96a3…` |
| Spec 034 outcome (`specs/034-matched-object-attribution/outcome.md`) — the finished D-20 record §2.2 rests on | SHA-256 `c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175` (recomputed at this draft); Spec 034 freeze digest `696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a` |
| Spec 024 specification (`specs/024-evidence-integration/spec.md`) — the family record F2 belongs to | SHA-256 `a817f698fd5f2dd0a2d324d580d25cba41fc989762b20e0b77a4144a02d3ee25` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

The populations of record (Phases 137/384,
frozen): **Holdat** — 7,002 token rows →
1,670 inscriptions → analysis population
1,670 at **9 eligible sites** (Banawali,
Chanhu-daro, Dholavira, Harappa, Kalibangan,
Lothal, Mohenjo-daro, Rakhigarhi, Surkotada),
profile table 9 × 98, χ² 745.953, V 0.1154.
**ICIT lineage** — 5,679 rows → analysis
population 5,410 at **7 eligible sites**
(Chanhu-daro, Dholavira, Harappa, Kalibangan,
Lothal, Mohenjo-daro, Nausharo), profile table
7 × 187, χ² 4966.362, V 0.2190. Site
eligibility is the frozen Phase-137 rule
(at least 30 inscriptions and at least 100
parsed tokens at a site).

## 4. Step 0 — gates before any quantity (fail-closed)

Execution runs these checks in order, before
any margin-curve cell or shared-population
quantity is computed. A failure stops the
execution in the class named; nothing is
repaired at run time.

- **0.1 Input integrity.** Every §3 input
  hashes to its stated value — the repository
  files to their recomputed pins, and the two
  held layer files to the values recorded in
  the Phase-137 results. A mismatch stops
  the run as **INVALID**.
- **0.2 Population reproduction, both
  layers.** The Phase-137 module's own
  loaders and frozen population rule, re-run
  on the pinned layers, reproduce each
  layer's recorded profile table **exactly**
  (the Phase-384 v2 contract's own first
  step), with the recorded counts, table
  dimensions, χ², and V: Holdat 1,670
  inscriptions, 9 × 98, χ² 745.953, V 0.1154;
  ICIT 5,410 inscriptions, 7 × 187, χ²
  4966.362, V 0.2190. A mismatch in either
  layer stops the run as **INVALID**.
- **0.3 Estimator regression.** The Phase-384
  v2 estimator, run unchanged on the two
  full-layer populations, reproduces the
  recorded governing intervals exactly:
  F2 basic interval [0.058939204306206666,
  0.0777941604081594], percentile interval
  [0.15300258989494483, 0.17185754599689756],
  bootstrap median 0.16180470665653984; F3
  basic interval [0.18229651053139323,
  0.21036863506165235]. Any mismatch stops
  the run as **INVALID** — neither arm
  proceeds on machinery that cannot first
  reproduce its own frozen result.
- **0.4 Shared-population census (arm 2's
  gate; margins and counts only).** The
  shared population of §5.2 is constructed
  and censused: the sites in both layers,
  per layer the inscription count on the
  shared population, and the per-site
  counts. If the shared population retains
  **fewer than 5 sites or fewer than 500
  inscriptions in either layer**, arm 2
  closes as **TOO THIN** with the counts
  stated (§5.2). Arm 1 is independent of
  this census and is not closed by it
  (DD-060-2).

## 5. The two arms

### 5.1 Arm 1 — the margin curve (a sensitivity display, never a verdict)

Recompute the bounded interval estimate for
F2 — the Phase-384 v2 method, **unchanged**:
inscription-level
bootstrap within site, site sizes fixed,
B = 9,999, seed 20261012, the **basic**
bootstrap interval governing) — and report
the verdict as a function of the margin
across the design's pre-registered grid:
**0.05, 0.075, 0.10, 0.125, 0.15**. At each
grid margin *m*, the cell word follows the
family's frozen rule applied to the governing
interval: **CONTRADICTED AT m** if the
interval's upper bound is below *m*;
**SUPPORTED AT m** if its lower bound is
above *m*; **STRADDLES m** otherwise. The
curve — the governing interval, the point
estimate, and the five cell words together —
is the arm's product. It is labelled
**sensitivity** in every output. The recorded
verdict at 0.10 stands (§7, limit 1): no cell
of this curve replaces it, and the margin at
which the cell word flips may never be quoted
as if it were the verdict.

### 5.2 Arm 2 — the shared population

**Construction (fixed in advance).** Start
from each layer's Phase-137 analysis
population (§3). Restrict both layers to the
**sites present in both layers' analysis
populations** — on the record at this draft,
the intersection of the two eligible-site
lists is six sites: Chanhu-daro, Dholavira,
Harappa, Kalibangan, Lothal, Mohenjo-daro;
the census at gate 0.4 re-derives the
intersection from the pinned layers rather
than trusting this list. Restrict by **object
type present in both**: the Holdat layer
carries **no object-type field** — its
inscriptions are seal texts, a constant, as
the Phase-137 record itself states — so the
type present in both layers is **SEAL**, the
Holdat side enters whole, and the ICIT side
is restricted to its recorded `SEAL` type
class (the Phase-137 loader's type class,
taken from the recorded `type` field).
No inscription is re-typed, and no other
type class enters. This reading of the
design's "same object types" is DD-060-3,
recorded in `adjudication.md`; the freeze
may overturn it openly.

**Measurement.** On that shared population,
compute the site-effect size **in each layer
separately**, with **identical code** — the
Phase-384 v2 estimator (§5.1), each layer in
its own sign numbering. The two layers' signs
are **never pooled, mapped, or harmonised**
under this spec: the comparison is of the two
governing intervals, nothing else. Period mix
is described per layer on the shared
population **insofar as the layers as held
carry the fields for it**; where a layer
carries no period field in the fields its
loader uses, the outcome states that plainly
(period mix NOT DESCRIBED FOR THIS LAYER —
FIELD NOT CARRIED) rather than importing a
period assignment from another source
(DD-060-4).

**Criteria fixed in advance (the design's
own words).**

- **COMPOSITION EXPLAINS THE GAP** — on the
  shared population, the two layers'
  governing intervals **overlap**.
- **COMPOSITION DOES NOT** — on the shared
  population, the two layers' governing
  intervals **still exclude each other**.
  This is the falsifier's outcome, stated
  under the corrected hand-off of §2.3.
- **TOO THIN** — the gate-0.4 census fails
  its floors; arm 2 computes nothing and
  closes with the counts stated.

## 6. Pre-written outcome wordings

The outcome record's headline paragraphs use
these forms, with the bracketed quantities
filled from the run. The full outcome set is
the two arm outcomes together, plus the stop
classes of §8.

### 6.1 Arm 1 (always reported, in this shape)

"Margin curve for STUDY-SPEC-024/F2-HOLDAT
(sensitivity display — the recorded verdict
at the declared margin 0.10 stands,
CONTRADICTED, and is not moved by this
curve): governing basic-bootstrap interval
[lo, hi], point V [v], on the Holdat layer's
1,670-inscription analysis population,
recomputed under the Phase-384 v2 estimator.
At margin 0.05: [cell word]. At 0.075: [cell
word]. At 0.10: [cell word]. At 0.125: [cell
word]. At 0.15: [cell word]."

### 6.2 Arm 2 — COMPOSITION EXPLAINS THE GAP

"On the population the two layers share —
[sites] sites, object type SEAL (the Holdat
layer's constant type), [nH] Holdat
inscriptions and [nI] ICIT inscriptions —
the Holdat governing interval [loH, hiH] and
the ICIT governing interval [loI, hiI]
overlap. The layer disagreement recorded
between F2 and F3 is substantially a
composition difference on this population:
put on the same sites and the same object
type, the two layers' site effects move
toward each other. This is consonant with
Spec 034's matched-object attribution
(ATTRIBUTED TO COMPOSITION) and independent
of it — a different question on a different
population. No verdict moves: F2 stands
CONTRADICTED at 0.10 and F3 stands SUPPORTED
at 0.10, exactly as recorded."

### 6.3 Arm 2 — COMPOSITION DOES NOT (the falsifier)

"On the population the two layers share —
[sites] sites, object type SEAL, [nH] Holdat
inscriptions and [nI] ICIT inscriptions —
the Holdat governing interval [loH, hiH] and
the ICIT governing interval [loI, hiI] still
exclude each other. Composition, in the form
of site and object-type mix, does not explain
the layer disagreement on this population.
This outcome stands **alongside** the
finished record of Spec 034 (design D-20,
complete): on 169 matched objects — all
Mohenjo-daro seals — the two compilations'
positional profiles agree (median distance
0.025694; ATTRIBUTED TO COMPOSITION). Both
statements stand; neither edits the other.
What carries the remaining disagreement —
the layers' site-effect estimation, their
sign treatment at repertoire level, or
selection beyond the matched slice — is not
adjudicated by this spec, and no successor
study is designed, registered, or implied by
this outcome; any successor enters through
its own planning gate. No verdict moves:
F2 stands CONTRADICTED at 0.10 and F3 stands
SUPPORTED at 0.10, exactly as recorded."

### 6.4 Arm 2 — TOO THIN

"The shared population cannot carry arm 2
as designed: it retains [s] sites and [nH]
Holdat / [nI] ICIT inscriptions, against the
frozen floors of 5 sites and 500 inscriptions
in either layer. No shared-population
quantity was computed. Arm 1's margin curve
stands as this spec's product, and the
settled F2 and F3 verdicts stand exactly as
recorded."

### 6.5 Stop wordings

- INVALID: "Execution stopped at step 0,
  gate [gate]: [observed values]. No arm
  quantity was computed. Spec 024's F2 and F3
  records stand exactly as recorded."
- A stop is a statement about runnability
  under the frozen contract, not about the
  claim.

## 7. Controls and named confounders

- **Site mix and object-type mix** are what
  arm 2 controls, by restriction to the
  shared population; the census of gate 0.4
  is published with the result so the
  restriction's size is never hidden.
- **Period mix** is described per layer on
  the shared population insofar as the
  layers carry it (§5.2), never silently
  treated as controlled: description is not
  control, and the outcome wording says
  which layers, if any, it could not be
  described for.
- **Sign numbering** is the named third
  confounder, and it is exactly what the
  falsifier routes to. The two layers number
  signs in different systems (the Holdat
  layer's native signs; the ICIT layer's
  three-digit codes). This spec never maps
  one system onto the other: each layer's
  effect is computed inside its own
  numbering, and only the two intervals are
  compared. A COMPOSITION DOES NOT outcome
  is therefore a statement that a gap
  survives sharing sites and types — with
  sign treatment among its named, unseparated
  candidate carriers (§2.3).
- **Margin shopping** is controlled by the
  fixed grid of §5.1 and the sensitivity
  label: the grid was written here, before
  any recomputation, and includes the
  declared margin 0.10 as one cell among
  five.
- **Selection in the shared population.**
  Restricting the ICIT layer to SEAL texts
  and to six sites changes that layer's mix
  (its full population is Harappa-heavy and
  tablet-rich); the per-site census and each
  layer's full-population interval (§4,
  gate 0.3) are reported beside the shared
  intervals so the restriction's effect on
  the inputs is visible, not just its effect
  on the answer.

## 8. Reporting obligations

Every product of an execution carries:

1. both corpus labels — the Holdat
   compilation layer and the ICIT-lineage
   layer (horus84), each with its §3 pin and
   its lineage posture as recorded in
   Spec 024 / Phase-137;
2. the step-0 record: every gate's verdict,
   in order, before any arm quantity;
3. arm 1's full curve in the §6.1 shape —
   governing interval, point estimate, all
   five cell words, the sensitivity label;
4. arm 2's census (sites, per-layer and
   per-site counts), the two governing
   intervals on the shared population, the
   period-mix description or its stated
   unavailability per layer, and the outcome
   word of §5.2 in the §6 wording that
   matches it;
5. the no-verdict-moves sentence: "No
   verdict moves under this spec: F2 stands
   CONTRADICTED at the declared margin 0.10
   and F3 stands SUPPORTED at the declared
   margin 0.10, exactly as recorded."

Deliverables at execution: a results JSON
(gate record, margin curve, shared census,
per-layer intervals full and shared, period
descriptions), a report under these headline
rules, the experiment-graph node (H15/H23,
registered and verified before the run), the
outcome append in this directory, and the
LEDGER entry (H1). Foundation check (H21)
after the execution phase: 0 failures, or the
outcome record says why not. Anchors asserted
byte-identical before and after.

## 9. Epistemic limits (binding on all outputs)

1. **No verdict moves under this design.**
   By the design's own terms: the settled F2
   verdict (CONTRADICTED at 0.10) and the F3
   verdict (SUPPORTED at 0.10) stand exactly
   as recorded, whatever either arm finds.
   This spec publishes the margin-dependence
   and tests convergence on a shared
   population; it re-adjudicates nothing.
2. **This does not establish that there is
   no site effect in Holdat.** The settled
   verdict already says the effect, if
   present, is below the size the program
   agreed to care about; this spec explains
   the verdict's shape, not its replacement.
3. **This does not establish which
   compilation is right.** Neither arm crowns
   a winner; arm 2 locates a disagreement —
   in composition, or surviving it — and
   location is not correctness.
4. **Arm 1 is sensitivity, in every output.**
   A cell word at any margin other than the
   declared 0.10 is a statement about that
   margin, never a verdict, and may not be
   quoted as one.
5. **Spec 034's slice travels with its
   verdict** wherever §2 or a COMPOSITION
   DOES NOT outcome cites it: 169 matched
   objects, all Mohenjo-daro seals. This
   spec neither widens nor narrows it.
6. Negative, thin, and invalid outcomes
   publish with the same prominence as a
   composition finding.

## 10. Risks and honest weaknesses

- **The layers are held files, not
  repository files.** Their pins are the
  values the Phase-137 record carries; if
  the execution venue cannot produce copies
  hashing to those values, gate 0.1 closes
  the run INVALID. That is the gate working,
  and it is a real risk: the Phase-137
  loaders' default paths point at checkouts
  outside this repository.
- **The shared population may be thin on
  the ICIT side.** The ICIT SEAL stratum on
  six sites has never been censused; gate
  0.4 exists because arm 2 may honestly
  close TOO THIN, and this draft does not
  pre-compute the census to find out
  (adjudication §2).
- **Interval overlap is a coarse
  convergence test.** Two wide intervals can
  overlap without the effects being close,
  and two narrow ones can exclude each other
  over a small gap. The design fixed this
  criterion; the outcome reports both
  intervals and both point estimates so a
  reader can see the sizes, not just the
  word.
- **The Holdat type restriction is a
  reading, not a quotation.** The design
  says "same object types"; the Holdat layer
  carries no type field. DD-060-3 records
  the reading and the freeze may overturn
  it — but any other reading must also say
  what it does with a layer whose type is a
  constant.

## 11. Stop conditions and outcome classes

Execution ends in exactly one of:

- **INVALID** — a §3 hash mismatches (0.1);
  either layer's population does not
  reproduce (0.2); or the estimator
  regression fails (0.3). No arm quantity
  is computed.
- **Arm outcomes** (after all gates pass) —
  arm 1 always reports its curve; arm 2
  reports exactly one of **COMPOSITION
  EXPLAINS THE GAP**, **COMPOSITION DOES
  NOT**, or **TOO THIN** (gate 0.4).

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§4) — integrity, both layers'
   population reproduction, estimator
   regression, shared-population census.
3. **Arm 1** (§5.1) — the margin curve on
   the full Holdat population.
4. **Arm 2** (§5.2) — per-layer intervals on
   the shared population, if its gate
   passed.
5. **Outcome** (§8) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 13. What this spec is not

Not a re-run or re-adjudication of Spec 024
or of Phase-384, not a new attribution study
(D-20 is complete; §2), not a sign-mapping
or crosswalk exercise, not a new corpus, not
a PRED evaluation, and not an authorisation
to execute. It is the margin curve of one
settled verdict and one convergence test on
the population two layers share, designed so
that its honest outcomes — including closing
thin at its own gate — are written down
before any quantity is computed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
