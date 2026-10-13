# Spec 033 — The Language Comparison Rerun Without the Falsified Method (D-03)

> ## DESIGN — FOR FREEZE — 2026-10-13
>
> This spec freezes design **D-03** of the experiment-design
> portfolio of 2026-10-13 (`docs/research/
> experiment-designs-2026-10-13/`, draft PR #195),
> commissioned by the owner's order of 2026-10-13
> ("Design experiments for all of the 35 that remain in
> question or inconclusive") and adjudicated for freeze by
> the owner's order of 2026-10-13 06:39 EDT ("Freeze
> D-30, D-03, and D-20 for execution"). The adjudication
> is recorded in `adjudication.md`. Execution
> (**Phase-397**) runs only after this freeze merges and
> the OSF registration of this frozen contract verifies
> public; no execution is performed by this spec.

## 1. Purpose

The claim `parpola_2010_dravidian_solution_manual_001` —
Parpola's proposal that the script writes an early form
of the Dravidian language family, by the rebus method —
stands at *partially supported*. The support on the record
comes from two comparisons the program ran with its
semantic-anchoring (SA) machinery: Phase-41 (a likelihood
ratio of **1.0566 to 1** for Dravidian anchors over
Sanskrit anchors, on the Mahadevan corpus) and Phase-43
(**0.484 log units per sign** for Dravidian, on a
1,500-sequence sample of the V3 corpus). The program
later falsified that method on held-out data (Phase-107:
its predictions scored **0.000, 0 of 115**). No rerun of
this comparison with a method that survived testing
exists in the record, so the claim's checked status has
never been re-earned without the falsified machinery.
This spec freezes the SA-free rerun the portfolio design
prescribes, so the claim's status can be re-earned — or
replaced — under a method the program trusts.

## 2. The question in plain words

Forget the old machinery. Take the signs whose values
are not in dispute, and ask a narrower question that a
sound method can answer: when each candidate language
family's word-values are assigned to a small set of
anchor signs, which family's assignments make the actual
inscription sequences look most probable — and does the
winner beat not just the other families but also the
result of assigning values at random?

## 3. Hypothesis and falsifier

**Hypothesis.** Proto-Dravidian assignments produce
inscription sequences with higher probability than
Indo-Aryan (Sanskrit), Munda, and isolate-baseline
assignments, by the margin fixed in §6, and beat the
random-assignment control.

**Falsifier.** The hypothesis fails if any rival family
matches or beats the Dravidian assignments, or if
Dravidian's margin over the best rival falls below the
fixed margin, or if random assignments reach the same
range — any of which means the comparison carries no
information about language family.

## 4. Data

- **The strict sign set**: the 94 readings carrying
  validation status `strict_sa_independent` in
  `backend/reports/INDUS_FINAL_ANCHORS.json` (287
  anchors in total; census pinned by the freeze tests).
- **The corpus**: the program's V3/Mahadevan-lineage
  corpus as held in the database — the same corpus
  family the original comparisons used, so the rerun is
  comparable to them.
- **Anchor candidate values, from published sources
  only**: the Dravidian Etymological Dictionary
  tradition for Dravidian; standard Sanskrit lexicon
  values for Indo-Aryan; published Munda reconstructions
  for Munda.

All data in hand; all published; derived statistics
publishable.

## 5. Method (SA-free by construction)

No semantic anchoring and no anchor promotion anywhere
in this design (H26). For each family: fix the same
small set of anchor signs (the five-per-language pattern
of the original Phase-41 comparison, with the anchor
list frozen before any run); assign that family's
published word-values to them; score every inscription
sequence under a simple counted model — sign-sequence
probabilities estimated from the corpus itself, with the
assigned values contributing only through the phoneme
sequences they imply.

**The exact estimator, fixed at this freeze** (the
design prescribes that the estimator is fixed at freeze
time and is the same for every family): the scored unit
is one inscription sequence over the strict sign set.
Under a family's assignment, each anchor sign contributes
the phoneme sequence its assigned value implies; every
non-anchor strict sign contributes its own sign identity
as a single value-free unit. The model is the counted
conditional distribution of each unit given the
preceding unit, estimated from the corpus itself under
that family's mapping, with add-one (Laplace) smoothing.
A sequence's score is its mean log probability per sign;
a family's score is the mean over all scored sequences.
The identical pipeline — same sequences, same smoothing,
same scoring — runs for every family and every control.

**Controls, run in the same pass:** (a) **999 random
assignments** of the same values to the same anchor
signs, giving the no-information distribution; (b) a
**no-language baseline** in which anchor signs carry no
values at all.

**Sensitivity, pre-registered:** the comparison is
reported a second time with Harappa's inscriptions
removed. The verdict rests on the primary run only; the
sensitivity carries the one verdict consequence §6
states.

**Robustness arm, pre-registered:** a second anchor list
(the next five published candidates per family) is run
under the identical pipeline.

## 6. Criteria fixed in advance

The margins are set from the original results so the
rerun can fail the claim, not just re-confirm it: the
original Phase-41 margin was a likelihood ratio of
1.0566 to 1 and Phase-43's was 0.484 log units per sign.

- **SUPPORTED** (for the bounded claim "Dravidian
  assignments fit better than the named rivals under
  this method"): Dravidian beats the best rival by at
  least **0.10 log units per sign** on the primary run
  **and** sits above the **99th percentile** of the
  random-assignment distribution.
- **NOT SUPPORTED**: any rival at or above Dravidian,
  or Dravidian inside the random distribution's range.
- **INCONCLUSIVE**: Dravidian first but by less than
  0.10 log units per sign, or the Harappa-removed
  sensitivity reverses the ranking.

**Status handling.** The claim's status after the run
is re-earned under this method or it is not: if the
result is NOT SUPPORTED, the inherited partial support
is replaced by the new record in an appended, dated
entry — the old SA-based numbers stay in history,
labelled as produced by a falsified method. This freeze
changes no claim record; the adopted explanation and
not-understood texts of the lane-2 record stand as they
are until the execution's appended entry.

## 7. Controls and named confounders

- **Only-two-families bias** (the original defect):
  three families plus two controls, all named in
  advance (§§3, 5).
- **Anchor-picking bias**: the anchor list is frozen
  before any family is scored, and the second
  pre-registered anchor list is run as a robustness arm
  (§5).
- **Within-lineage corpus**: named in the verdict
  wording — a win is a win inside the Mahadevan lineage,
  and designs D-01/D-24 are the ones that speak to other
  lineages. This design claims no cross-lineage
  independence.

## 8. What this design would move, and what it would NOT establish

**What it would move.** The claim from IN QUESTION (the
portfolio's classification) to a re-earned checked
status (supported, not supported, or inconclusive)
under a method the program trusts — the first time its
status would rest on post-falsification evidence.

**What it would NOT establish.** Not the rebus method
itself, not any single sign's reading, not a
decipherment. A statistical fit between one family's
word-values and the sign sequences is one kind of
evidence, and the design says so in its own verdict
wording.

## 9. Execution shape (Phase-397 — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment script,
   graph module, registration, registration
   verification, then run.
2. **Anchor freeze**: both pre-registered anchor lists
   written as cited data (family, sign, published
   value, source) and hashed before any scoring.
3. **Scoring**: the frozen pipeline (§5) over the
   families, both controls, the robustness arm, and
   the Harappa-removed sensitivity.
4. **Outcome**: the verdict under §6, recorded in this
   spec's directory and the root LEDGER, with the
   claim-status consequence of §6 appended as a dated
   entry to the claim's record; nothing written into
   any frozen record.

## 10. What this spec does not do

- It does not execute anything. Execution (Phase-397)
  follows the verified OSF approval of this frozen
  contract under the owner's order of 2026-10-13.
- It uses no semantic-anchoring machinery, no anchor
  promotion, and no SA-derived quantity anywhere —
  including in its controls (H26).
- It does not score the sibling fish-sign claim
  (`parpola_2010_dravidian_solution_manual_002`, design
  D-04) or any other claim.
- It changes no claim record, no anchor, and no frozen
  Spec 026–032 record at freeze time.

## 11. Governed claims (summary)

The governed register is `claims.json` (F033-C01…C15):

- **C01** — verdicts concern the bounded comparison
  only.
- **C02** — the hypothesis: Dravidian assignments fit
  better than the named rivals under the frozen model.
- **C03** — the pipeline contains no semantic anchoring
  and no anchor promotion.
- **C04** — scoring uses the strict sign set.
- **C05** — the corpus is the V3/Mahadevan-lineage
  corpus as held.
- **C06** — each family's anchor signs are the same
  frozen five-sign set.
- **C07** — anchor values come from published sources
  only.
- **C08** — every family and control is scored by the
  identical counted-model pipeline.
- **C09** — the controls are 999 random assignments and
  a no-language baseline, in the same pass.
- **C10** — the SUPPORTED margin: at least 0.10 log
  units per sign over the highest-scoring rival.
- **C15** — the SUPPORTED percentile bar: the 99th
  percentile of the random-assignment distribution.
- **C11** — any rival at or above Dravidian, or
  Dravidian inside the random range, yields NOT
  SUPPORTED.
- **C12** — a sub-margin win, or a ranking reversal in
  the Harappa-removed sensitivity, yields INCONCLUSIVE.
- **C13** — the second pre-registered anchor list runs
  as a robustness arm.
- **C14** — the verdict wording names the within-lineage
  limit.

## 12. Design decisions

The portfolio design D-03 is carried into this freeze
without deviation. Its own decisions, recorded here as
the design states them:

- **DD-03-1 — Margins set from the originals.** The
  0.10-log-unit bar and the 99th-percentile rule are
  fixed from the Phase-41/43 results so the rerun can
  fail the claim (§6).
- **DD-03-2 — Verdict on the primary run only.** The
  Harappa-removed reporting is a sensitivity whose sole
  verdict consequence is the INCONCLUSIVE rule of §6.
- **DD-03-3 — Status is re-earned or replaced.** The
  inherited SA-based partial support does not survive a
  NOT SUPPORTED outcome; the replacement is an appended,
  dated entry, never an edit (§6).

At freeze time one design-internal point is fixed, as
the design itself prescribes ("the exact estimator is
fixed at freeze time"): the estimator of §5 (counted
conditional model over phoneme-sequence and sign-identity
units, add-one smoothing, mean log probability per sign),
identical for every family and control.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
