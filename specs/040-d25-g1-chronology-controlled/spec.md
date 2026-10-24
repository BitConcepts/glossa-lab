# Spec 040 — D-25: G1 With Time Held Fixed (Chronology-Controlled Site-Repertoire Test)

> ## FROZEN — 2026-10-24
>
> Drafted under the owner's 2026-10-20 bundle
> decision: the gazetteer period-assignment act
> (Spec 039) runs first, under the published-
> determinations-only evidence standard, and
> D-25 follows it. **Spec 040 cannot be
> frozen until Spec 039 has executed and its
> period labels are frozen in a form this spec
> can consume (§1).** At the freeze act of
> 2026-10-24, §1 was judged satisfied by the
> openly recorded successor-artifact
> substitution of Spec 041's artifact
> (`adjudication.md` §5.1; `freeze.md` §1–§2):
> Spec 039's own artifact did not satisfy §1,
> and that finding stands. The AEE lifecycle
> hooks ran at the freeze gate over the
> recovered register (0.7-draft) and passed
> (`aee/freeze-aee-note.md`). **This freeze
> executes nothing.** Execution is a separate
> later owner act.
>
> The execution phase number, unassigned at
> draft, is allocated at this freeze act under
> DD-040-10: **Phase-439** (the highest phase
> on the merged record at the act is
> Phase-438, Spec 054's).

**Design source:** D-25 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-25, read in full at this draft).

**Claim under test:** `STUDY-SPEC-025/G1` —
site-repertoire differentiation on the
ICIT-lineage layer, SUPPORTED under composition
and preservation control, with the standing
rider that **chronology is not controlled**.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The dependency gate — stated first, because it governs the freeze

D-25 asks whether the G1 site association
survives when inscriptions are compared only
within the same coarse period. That question
cannot be asked until every G1 inscription can
be placed — or honestly left unplaced — in a
period stratum. The placement evidence does
not yet exist in usable form:

- The Stage 0 gazetteer's
  `program_period_assignment` column is empty
  on every row. Spec 027 §6.2 reserved filling
  it to a separate owner act.
- The owner authorised that act on 2026-10-20
  (Spec 039, bundled with this design), with
  the evidence standard fixed as **published
  period determinations only**: a label must
  trace to a publication's own period
  determination for the site or site-period,
  never to a program inference from dates.
- The 205-row extended chronology spine
  (Spec 030 / Phase-394) exists and is pinned
  (§3), but a spine row is a dated
  sample/context assertion about a site. It is
  **not** a period label for any inscription,
  and no inscription inherits a period merely
  because its site has dated contexts.

**Freeze gate (fail-closed).** Spec 040 may be
frozen only when all of the following are on
record:

1. Spec 039 has **executed** — not merely
   frozen — and its outcome record and freeze
   digest are merged and named in Spec 040's
   freeze record.
2. Spec 039's product includes a frozen,
   machine-readable **period-assignment
   artifact**, pinned by SHA-256 in Spec 040's
   freeze record, that resolves the
   chronological placement of G1 inscriptions
   at **site-period resolution** (§4): for
   each inscription, its site and its recorded
   local chronological label(s) map to exactly
   one coarse period (`EARLY`, `MATURE`,
   `LATE`), to `UNASSIGNED`, or to a flagged
   contested assignment with a frozen
   sensitivity label.
3. Every non-`UNASSIGNED` assignment in that
   artifact carries its published source
   citation and locator, the mapping rule
   applied, and its contested flag. An
   assignment resting on a program-derived
   dates-to-period inference fails this gate:
   that is the evidence standard the owner
   excluded.
4. The artifact's join key covers the G1
   population's inscription identifiers
   exactly (§3). A site-level occupation label
   by itself does **not** satisfy this gate:
   the G1 sites were occupied across more than
   one coarse period, so a single label per
   site cannot place its inscriptions, and
   borrowing the site label for every
   inscription is forbidden (§4.3).

If any condition fails, Spec 040 is **not
frozen** and its state is recorded as
**NOT-YET-TESTABLE — dependency gate**. That
is a designed closure of the freeze step, not
a verdict on G1: G1 and its rider stand exactly
as Spec 025 and Phase-385 left them.

A second, execution-stage thinness gate (§5)
applies the same closure word after the labels
exist, if they leave too few sites or rows in
the controlled strata.

## 2. The claim and the record it stands on

### 2.1 What G1 is

Spec 025's G1 (Phase-140) re-tested the
Phase-137 site-repertoire association on the
ICIT-lineage layer (horus84), permuting site
labels within composition × preservation
strata. The recorded result
(`reports/phase140_results.json`):

- Population: **5,410 inscriptions** at 7
  eligible sites (Chanhu-daro, Dholavira,
  Harappa, Kalibangan, Lothal, Mohenjo-daro,
  Nausharo), reproduced exactly from the
  Phase-137 rule.
- Observed χ² = **4966.362228365138**;
  permutations ≥ observed: **0 of 9,999**;
  raw permutation p = **0.0001**; verdict
  **SUPPORTED under control** under Spec 025's
  rule (raw p ≤ 0.05, BH over G1 alone).
- Cramér's V (descriptive) = **0.2190**.

Phase-385 (Spec 026 margin completion) added
the interval Spec 025 had not reported: a
stratified basic bootstrap 95% CI for V of
**[0.1838, 0.2102]** (governing; B = 4,999,
seed 20261012), entirely above the declared
V = 0.10 practical floor
(`reports/phase385_results.json`).

### 2.2 The rider

Every G1 statement carries it, and this spec
exists because of it: **chronology is NOT
controlled in the primary test** — period/phase
remain uncontrolled confounders. The sites'
period mixes differ, so part of the apparent
site effect may be a time effect. Spec 025's
own chronology sensitivity (S-chron, strata =
composition × Phase-139 `chron_band`) was
EXPLORATORY, rested on a harmonization that
covered only 41.9% of rows, and could not
retire the rider.

### 2.3 The question, in plain words

When inscriptions are compared only against
inscriptions from the same coarse period —
with composition and preservation still held
fixed, as before — does the site association
stay clearly above the program's practical
margin? If it does, the rider is retired. If
the effect shrinks to or below the margin
once period is held fixed, the honest reading
changes: what looked like "cities wrote
differently" may be "times wrote differently."

### 2.4 A tension in the design source, recorded openly

D-25's feasibility line says the missing asset
"now exists": the 205-row spine, "on top of
the Stage 0 gazetteer's period labels." The
spine exists; the gazetteer labels did not —
the assignment column was empty when the
design was written and is empty still. The
owner's 2026-10-20 bundle decision is what
makes the second half true: Spec 039 first,
this spec after it. This draft does not
harmonise the tension away; §1 is its
consequence.

## 3. Inputs (pinned or to be pinned at the freeze)

| Input | Pin / state |
|---|---|
| ICIT-lineage layer (horus84 `inscriptions.csv`) | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef` (the Phase-137/139/140 file) |
| Phase-139 harmonized covariates (`data/evidence_integration/phase139_harmonized_covariates.json`) | SHA-256 `a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413`; 5,410 rows; supplies `preservation_class` and `composition_stratum` per inscription id |
| Phase-140 results (`reports/phase140_results.json`) | The regression target of §7 |
| Phase-385 results (`reports/phase385_results.json`) | The interval precedent of §6.3 |
| Extended chronology spine (`data/movement/chronology_rows_phase394.jsonl`) | 205 rows; SHA-256 `9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93` |
| Period-assignment artifact (the §1 dependency) | **Spec 041's artifact, accepted at the 2026-10-24 freeze by successor-artifact substitution** (`adjudication.md` §5.1): `data/evidence_integration/site_period_mapping.jsonl`, SHA-256 `1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67`. Spec 039's own artifact (`data/movement/gazetteer_rows_assigned.jsonl`, SHA-256 `64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`) did not satisfy §1 and is not the consumed artifact |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (refreshed at the freeze from the draft's stale `eccea6d5…` pin); asserted byte-identical before and after any execution; this spec moves no anchor |

The spine's role is bounded: its rows may be
cited inside Spec 039's published-determination
record as the traced location of a published
assertion, and its contested flags travel with
any assignment that rests on a contested
assertion. The spine is **not** recomputed,
extended, or re-graded under this spec, and
its dates never assign an inscription's period
directly.

## 4. Period assignment — how period enters

Period enters as a **stratification variable**
(the design's method: shuffling inside groups
matched for composition, preservation, and
period). It is not a regression covariate and
not a matching score. This section fixes the
assignment discipline the primary test consumes.

### 4.1 The assignment interface

Execution joins three records on the layer's
unique inscription `id`:

1. the layer row (site; its recorded local
   `period` / `phase` values exactly as
   published in the layer);
2. the Phase-139 covariate row
   (`composition_stratum`, `preservation_class`);
3. the Spec 039 assignment artifact, keyed at
   site-period resolution: site × the recorded
   local chronological label(s) → one of
   `EARLY` / `MATURE` / `LATE` / `UNASSIGNED`,
   with citation, mapping rule, and contested
   flag per mapping.

The join must produce exactly one assignment
row per population inscription (5,410).
A missing join row, a duplicate, or a site
mismatch is a stop condition (§9), never a
repair opportunity.

### 4.2 Assignment rules (primary)

An inscription's primary `period_stratum` is:

- the unique coarse label its site × local
  chronological label maps to under Spec 039's
  frozen artifact, **only if** that mapping is
  uncontested;
- `UNASSIGNED` if it has no recorded local
  chronological label, if its label maps to no
  coarse period, if it maps to more than one
  coarse period (transitional or mixed labels
  such as `2/3` are not split by guesswork), or
  if its only mapping is contested.

`UNASSIGNED` inscriptions are **excluded from
the primary test and counted** — never assigned
by site reputation, by majority, or by the
spine's dates. The excluded count and share
are headline quantities (§5, §10).

### 4.3 What may not place an inscription

- A site-level occupation label alone (a site
  occupied in the Mature period also has Early
  and Late material; the label does not date
  the object).
- A radiocarbon determination for the site
  (a dated context is not this inscription's
  context).
- The Phase-139 `chron_band` harmonization
  (it is Spec 025's constructed context; D-25
  replaces it as the primary period source —
  it survives only as the recorded S-chron
  companion in §8.4).
- Analyst judgement at execution time. Every
  placement traces to the frozen artifact or
  does not happen.

### 4.4 Contested assignments

Following Spec 030's two-computation posture:
contested mappings are **excluded from the
primary** (the inscription is `UNASSIGNED`
there) and **included in the §8.1 sensitivity**
under the sensitivity label Spec 039 froze for
that mapping. If Spec 039 froze no unique
sensitivity label for a contested mapping, the
sensitivity is reported NOT ESTIMABLE for the
affected mappings; execution does not choose a
label.

## 5. The margins gate (execution stage 1 — margins only, no outcome)

Before any repertoire quantity is computed,
execution reports assignment margins only:

- assigned / unassigned counts and shares,
  overall and by site and by coarse period;
- distinct sites with ≥ 1 assigned inscription
  in each coarse period;
- contested-excluded count;
- permutable inscriptions under the §6 primary
  strata (rows in strata containing ≥ 2
  distinct sites).

**Gate (all three must hold):**

1. **Each** of `EARLY`, `MATURE`, and `LATE`
   retains assigned inscriptions from at
   least **5 distinct sites** (D-25's rule,
   carried verbatim).
2. The unassigned share is **≤ 40%** of the
   5,410-row population (D-25's rule: *more
   than* 40% unassignable closes the design;
   exactly 2,164 of 5,410 is 40.0% and passes).
3. Permutable inscriptions under the primary
   strata number **≥ 1,000** (proposed at this
   draft, DD-040-6: Spec 025's covariate-gate
   floor, carried to the combined strata so a
   technically non-empty but practically
   singleton-fragmented design cannot proceed).

If any arm fails, execution closes as
**NOT-YET-TESTABLE** with the margins stated:
no profile table outcome, no permutation, no
interval is computed, and G1 stands unchanged
with its rider. (D-25's source wording for
this closure is "INCONCLUSIVE-BY-DESIGN"; this
spec governs it as NOT-YET-TESTABLE, the
program's word for a test the data cannot yet
support — the terminology decision is recorded
as DD-040-5, not made silently.)

## 6. The primary test

### 6.1 Population and profile table

- **Base population:** the Phase-137 F3
  population, reproduced by rule from the
  pinned layer (7 eligible sites, 5,410
  inscriptions, ≥ 1 parsed token), asserted
  against `reports/phase137_results.json` and
  `reports/phase140_results.json` before
  anything else runs (§7).
- **Analysis population:** the base
  population's inscriptions with an uncontested
  unique primary `period_stratum` (§4.2).
  Analysis sites are the sites retaining ≥ 1
  assigned inscription; sites dropping out
  are named in the report.
- **Profile table:** site × sign, on the
  analysis population, with the sign columns
  fixed from the **full base population**
  exactly as Phase-137/140 built them (signs
  with layer-wide count ≥ 10 within the base
  population; rarer signs pooled to `OTHER`;
  placeholders `000` / `999` excluded) — the
  column set is not re-derived on the assigned
  subset (DD-040-4), so the new table is
  directly comparable to the recorded ones.
- **Statistic:** Pearson χ² of the site × sign
  profile table as the divergence statistic;
  Cramér's V and per-site total-variation
  distances as descriptive effects; sparsity
  disclosure mandatory (cells, expected < 5
  share, minimum expected, per-site tokens),
  carried from Phase-137/140 practice.

### 6.2 Permutation inference

Site labels are permuted at inscription level
**within strata** keyed
`{composition_stratum} | {preservation_class} | {period_stratum}`,
holding each inscription's token vector,
composition, preservation, and period fixed.
B = 9,999; `random.Random(20261009)` (the
Phase-136/137/140 seed); Fisher–Yates via
`shuffle`; p = (1 + #{χ²_perm ≥ χ²_obs}) /
(1 + B). Rows in single-site strata are
constant under permutation: counted as
non-permutable, reported, never silently
dropped. No asymptotic p-value is reported
anywhere. The permutation p is **reported**
with the result; under this spec's re-derived
decision rule (§6.4, DD-040-1) it does not by
itself mint the verdict.

### 6.3 The effect interval (governing quantity)

The interval follows the Phase-385 v2
estimator, carried exactly:

- Stratified bootstrap of **inscriptions
  within the §6.2 primary strata** (resample
  with replacement, stratum sizes preserved),
  over the analysis population;
- B = 4,999, seed 20261012;
- report both the percentile interval and the
  **basic bootstrap interval**
  [2V − q97.5, 2V − q2.5] for Cramér's V;
- **the basic interval governs** the margin
  adjudication, as it governed Phase-385's.

### 6.4 Decision rules and claim consequences (fixed in advance)

The practical margin is **V = 0.10**, carried
from the Spec 026 / Phase-385 declaration for
this result family. Let [lo, hi] be the
governing basic interval of §6.3.

- **SUPPORTED — CHRONOLOGY CONTROLLED**
  (lo > 0.10): the period-controlled effect
  lies entirely above the margin. Consequence
  (appended record only): G1's statement
  becomes "SUPPORTED under control, chronology
  included," and the chronology rider is
  retired from that date. Historical statements
  carrying the rider are not edited; the
  retirement is a dated append, as every
  correction in this program is.
- **WEAKENED — RIDER CONFIRMED AS MATERIAL**
  (lo ≤ 0.10 < hi): the interval straddles the
  margin, so the chronology-controlled effect
  is not shown to clear it. Consequence
  (appended record only): G1 is restated as a
  **period-confounded association** — supported
  under composition and preservation control,
  not established under chronology control —
  with the size of the drop from the
  Phase-385 interval reported beside it.
- **CONTRADICTED AT THE DECLARED MARGIN**
  (hi ≤ 0.10): the period-controlled effect
  lies entirely at or below the practical
  floor. Consequence (appended record only):
  the chronology-controlled form of G1 is
  recorded CONTRADICTED at the declared margin.
  This defeats the claim that the site
  association survives holding time fixed; it
  does not assert that no site association
  exists in any form, and it does not alter
  Phase-140's differently-controlled result,
  which stands as the record of its own design.

No other verdict words exist under this spec.
A result is never rounded up: an interval that
straddles the margin is WEAKENED, not
"supported with a caveat."

## 7. Comparability regression (stop condition, before the primary)

Before the primary run is accepted, the
execution machinery must reproduce, on the
full base population:

1. the Phase-137 composition-only configuration
   **exactly** (observed χ², count of
   permutations ≥ observed, null median and
   95th percentile, raw p, from
   `reports/phase137_results.json`); and
2. the Phase-140 composition × preservation
   configuration **exactly** (the same
   quantities, from
   `reports/phase140_results.json`).

Any mismatch is a stop condition: the run is
recorded **INVALID — regression failure**, the
primary does not proceed, and the cause is
found and recorded before any renewed attempt.
An INVALID run is a machinery finding, not a
verdict on G1 and not a NOT-YET-TESTABLE
closure.

## 8. Sensitivity computations (labelled; none mints a verdict)

All sensitivities use the §6 statistic and
estimators unless stated, are labelled
**SENSITIVITY** in every artifact, and are
reported as bounds on the primary result.
None can upgrade, downgrade, or replace the
§6.4 outcome.

### 8.1 Contested-included

§4.4's sensitivity: contested mappings enter
under their frozen sensitivity labels; all
other rules unchanged. Report assigned N,
unassigned share, χ², permutation p, V, and
the basic interval beside the primary's.

### 8.2 Leave-one-site-out

For every analysis site in turn: drop the
site, re-form the strata on the remaining
assigned inscriptions, and recompute χ²,
permutation p, V, and the basic interval.
Report per dropped site, with the period-site
census of each subset. A subset whose table
cannot support V (fewer than 2 sites) is
reported NOT ESTIMABLE for that subset. These
are stability readings of an already-decided
test, not new tests.

### 8.3 Drop-Harappa

The Harappa member of §8.2, named in advance
because Harappa is corpus-dominant in this
layer: reported in the headline sensitivity
paragraph, not buried in the LOSO table. If
Harappa is not an analysis site, this
sensitivity is recorded NOT APPLICABLE with
the reason.

### 8.4 Recorded companions (not recomputed)

Reported alongside, as recorded: the
Phase-140 primary result and the Phase-385
governing interval [0.1838, 0.2102]; Spec 025's
EXPLORATORY S-chron interval [0.1848, 0.2098]
(composition × Phase-139 `chron_band`). These
are context for the size of any change, and
are labelled with their own designs wherever
they appear.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **NOT-YET-TESTABLE** — the §1 dependency
  gate (at freeze) or the §5 margins gate (at
  execution) fails. No outcome quantity is
  computed past the failed gate.
- **INVALID** — an input hash mismatches; the
  §4.1 join does not cover the population
  exactly; the §7 regression fails; or a frozen
  rule would have to change to proceed.
- **SUPPORTED — CHRONOLOGY CONTROLLED**,
  **WEAKENED — RIDER CONFIRMED AS MATERIAL**,
  or **CONTRADICTED AT THE DECLARED MARGIN**
  — per §6.4, after all gates pass.

## 10. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the lineage label **"ICIT-lineage layer
   (horus84)"**;
2. the assignment census: assigned and
   unassigned counts and shares, the
   contested-excluded count, and the Spec 039
   artifact's identity (version + SHA-256);
3. the outcome word of §9 and, for a §6.4
   outcome, the governing basic interval and
   the margin;
4. for any pre-execution G1 quotation, the
   standing rider verbatim — until and unless
   a SUPPORTED outcome retires it by append.

Deliverables at execution: results JSON
(margins, strata tables, permutable N,
observed vs null distribution, V and both
intervals, sparsity disclosures, regression
record, sensitivity panel), a report under the
§10 headline rules, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not.

## 11. Epistemic limits (binding on all outputs)

1. Every result describes **the ICIT-lineage
   layer** — a derivative compilation, not an
   independent witness — never "the Indus
   corpus" in general.
2. Associations describe **co-occurrence** in
   recorded data. A chronology-controlled
   repertoire association is not evidence for
   regional dialects as linguistic entities,
   for any reading of any sign, or for any
   decipherment claim.
3. **No movement conclusion.** Even a clean
   period-controlled association is consistent
   with goods and habits moving without
   populations moving; Spec 027's
   ecological-fallacy fence binds this spec's
   wording exactly as it bound the original's.
4. **No mechanism conclusion.** The test does
   not distinguish local repertoires from
   genre mixes, workshop habits, or recording
   traditions.
5. **No PRED contact, no anchor movement.** No
   output feeds PRED-2026 scoring; no anchor
   is minted, promoted, demoted, or validated.
6. Period assignment is **constructed
   context**: its published sources, mapping
   rules, coverage, and contested exclusions
   travel with every number that uses it. A
   result quoted without its assignment census
   is a misquote of this spec.
7. Negative, weakened, and NOT-YET-TESTABLE
   outcomes publish with the same prominence
   as supported ones.

## 12. Risks and honest weaknesses

- **Assignment sparsity is the expected
  failure mode.** Local chronological labels
  are recorded for a minority of layer rows
  and are structurally missing by site
  (Spec 025 §3.2). The §5 gate exists because
  this design may honestly close unrun.
- **Coarse strata only.** Early / Mature /
  Late is the finest resolution the published
  record supports for this test. Spec 030
  closed the fine timing question
  NOT-YET-TESTABLE (C1 1 FAIL, C2 6 FAIL,
  C3 0.0 FAIL, C4 PASS); nothing here reopens
  it or claims finer control.
- **Period mixes within a label remain.**
  Stratification holds the coarse label fixed;
  it does not make two inscriptions
  contemporary.
- **Bootstrap behaviour.** Cramér's V carries
  plug-in bias under resampling (the Phase-385
  v1 lesson); the basic interval governs for
  exactly that reason, and the percentile
  interval is never substituted for it.
- **Harappa concentration.** The layer is
  dominated by two sites' token counts;
  §8.2/§8.3 exist so that dependence is
  measured, not asserted away.

## 13. Execution shape (gated; NOT run by this draft)

1. **Dependency verification** — §1's gate,
   re-checked against the merged Spec 039
   record and the pinned artifact.
2. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
3. **Margins gate** (§5) — margins only.
4. **Regression** (§7) — exact reproduction or
   INVALID.
5. **Primary** (§6) and **sensitivities** (§8).
6. **Outcome** (§10) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured.

## 14. What this spec is not

Not a reopening of Spec 024 or Spec 027, not
a new corpus, not a re-adjudication of Q6 or
Q7, not a PRED evaluation, and not an
authorisation to execute. It is the
chronology-controlled rerun of one recorded
test, designed so that its most likely honest
outcomes — including closing unrun — are
written down before any label is joined.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
