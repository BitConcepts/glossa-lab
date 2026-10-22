# Spec 033 — Adjudication Record

> ## ADJUDICATED INPUT — 2026-10-13
>
> This spec has two adjudication inputs, recorded here
> so the freeze's basis is inspectable:
>
> 1. **The design commission of 2026-10-13** (owner
>    order, 06:13 EDT): "Design experiments for all of
>    the 35 that remain in question or inconclusive."
>    The commission produced the experiment-design
>    portfolio (`docs/research/
>    experiment-designs-2026-10-13/`, draft PR #195),
>    in which design **D-03** specifies this study and
>    classifies `parpola_2010_dravidian_solution_
>    manual_001` as IN QUESTION. The portfolio's own
>    recommendation ranked D-03 second of the 31
>    designs.
> 2. **The freeze order of 2026-10-13** (owner order,
>    06:39 EDT), verbatim: **"Freeze D-30, D-03, and
>    D-20 for execution"**. That order is the
>    adjudicating act for this freeze. It adopts
>    design D-03 as written; no design point was
>    reopened, added, or removed by it.

## 1. The adopted design (operative substance)

Design D-03, as frozen in `spec.md`:

- **The question, narrowed to what a sound method can
  answer:** which family's published word-values,
  assigned to a small frozen set of anchor signs, make
  the inscription sequences most probable — and does
  the winner beat the other families and the
  random-assignment control.
- **Hypothesis and falsifier, as designed:** Proto-
  Dravidian assignments beat Indo-Aryan (Sanskrit),
  Munda, and isolate-baseline assignments by the fixed
  margin and beat the random control; the hypothesis
  fails if any rival matches or beats Dravidian, if
  the margin falls below the fixed bar, or if random
  assignments reach the same range.
- **SA-free by construction (H26):** no semantic
  anchoring, no anchor promotion, and no SA-derived
  quantity anywhere in the pipeline. The prior support
  for the claim (Phase-41: ratio 1.0566 to 1; Phase-43:
  0.484 log units per sign) was produced by the SA
  machinery Phase-107 falsified (held-out 0.000,
  0 of 115); it is the reason for the rerun, not an
  input to it.
- **Data, as designed:** the strict sign set (94
  readings, validation status `strict_sa_independent`)
  and the V3/Mahadevan-lineage corpus as held — the
  same corpus family the originals used. Anchor values
  from published sources only.
- **Criteria, as designed, with margins set from the
  originals so the rerun can fail:** SUPPORTED at a
  margin of at least 0.10 log units per sign over the
  best rival **and** above the 99th percentile of the
  999-assignment random distribution; NOT SUPPORTED on
  a rival at or above Dravidian or Dravidian inside
  the random range; INCONCLUSIVE on a sub-margin win
  or a ranking reversal in the Harappa-removed
  sensitivity. The verdict rests on the primary run.
- **Status consequence, as designed:** the claim's
  status is re-earned under this method or replaced by
  an appended, dated entry; the old SA-based numbers
  stay in history, labelled as produced by a falsified
  method.

## 2. The freeze-time fixing the design prescribes

The design states that "the exact estimator is fixed
at freeze time and is the same for every family." This
freeze fixes it (spec §5): the scored unit is one
inscription sequence over the strict sign set; under a
family's assignment each anchor sign contributes the
phoneme sequence its assigned value implies, and every
non-anchor strict sign contributes its own sign
identity as a single value-free unit; the model is the
counted conditional distribution of each unit given
the preceding unit, estimated from the corpus itself
under that family's mapping, with add-one (Laplace)
smoothing; a sequence's score is its mean log
probability per sign, and a family's score is the mean
over all scored sequences. This is a fixing of the
design's "simple counted model", not a change to it:
every criterion, control, and verdict rule is the
design's own.

## 3. Sequencing adopted with the freeze

Mirroring the program's registration-before-execution
precedent (Spec 027 Stage 1 `pnqrx`; Spec 028 `7m35w`;
Spec 030 `bge3k`; Spec 031 `jtwvc`; Spec 032): the
frozen contract is filed on OSF after this freeze
merges and before any execution. Execution
(**Phase-397**) runs under the owner's order of
2026-10-13 once the registration's approval verifies
public. No execution is performed by the freeze.

## 4. What was NOT decided here

- No score exists. No family has been run under the
  frozen pipeline.
- The claim's current record — partially supported,
  with the owner's adopted explanation and
  not-understood texts — stands untouched until the
  execution's appended entry.
- The sibling fish-sign claim
  (`parpola_2010_dravidian_solution_manual_002`,
  design D-04) is not scored or altered by this
  freeze.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
