# Spec 034 — Why the Two Compilations Disagree: A Matched-Object Attribution

> ## DESIGN DRAFT — FOR FREEZE — 2026-10-13
>
> Written to carry design **D-20** of the
> experiment-design portfolio of 2026-10-13
> (`docs/research/experiment-designs-2026-10-13/
> 04-study-headlines.md` in draft PR #195) into a
> freezable contract, without deviation. The
> portfolio classified the underlying result
> **SETTLED** — the Phase-125 verdict stands — and
> this design attributes its unexplained residue.
> Adjudication: the design commission and the
> owner's freeze order of 2026-10-13 are recorded in
> `adjudication.md`. Execution is **Phase-398**; it
> runs after the OSF registration of this frozen
> contract verifies public. Nothing in this draft
> executes anything.

## 1. What this spec does, in plain words

Two standard compilations of the Indus inscriptions
— the CISI corpus (the Parpola side) and the ICIT
corpus (the Mahadevan side) — describe where signs
sit inside inscriptions very differently. Phase-125
measured that disagreement: of 286 sign pairs, only
16 could be judged at all, and their positional
profiles differed by a median distance of 0.637.
Phase-127 showed sampling noise alone produces only
0.083, so the disagreement is real. Phase-131 then
tried to attribute it to named causes and managed
6.1%, leaving 93.9% unexplained — because the two
digital layers shared **zero object keys**: there
was no way to ask, for *this same physical object*,
what each compilation says.

This spec builds that missing join — a bridge of
matched objects — and asks the question object by
object. Its step 0 is a feasibility gate fixed in
advance: if the bridge yields fewer than 150 matched
objects carrying texts of three or more signs in
both compilations, the study closes at step 0 as
**TOO THIN TO ATTRIBUTE**, with the bridge census
published as the finding. That outcome is a result,
not a failure: it converts "zero shared keys" from a
dead end into a measured quantity and names the
unblocking act precisely.

## 2. The result whose residue this attributes

**STUDY-SPEC-019/PHASE-125 — SETTLED: FAIL —
DISAGREEMENT** (`reports/
phase125_cross_compilation_summary.md`): 16
judgeable pairs of 286; median TV distance
0.636931; verdict FAIL / DISAGREEMENT stands.
Supporting record: Phase-127 (`reports/
phase127_cross_compilation_diagnostic.md`) — the
disagreement is not a sampling artefact (noise
alone: 0.083). Phase-131 (`reports/
phase131_attribution.md`) — 6.1% attributed to named
causes, 93.9% unexplained; its join attempts are
recorded there: the CISI-ID join was REJECTED
(Holdat `cisi_number` is internal sequential
numbering, not a CISI object ID — prohibited as a
join key), and shared artifact keys numbered **0**.

This spec does not re-judge the settled result. It
attributes the residue on it, and whichever way the
attribution falls, the Phase-125 verdict stands.

## 3. The study design (D-20, stated exactly)

**The question.** The disagreement might live in
the objects (the two compilations publish different
inscriptions), in the sign identities (the crosswalk
maps signs differently — 383 of its 762 pairs are
conflict pairs), or in segmentation (where each
compilation cuts texts into signs). Which of these
carries the 93.9%?

**Hypothesis.** On matched objects — the same
physical artefacts — the two compilations'
positional profiles agree far better than the
corpus-level 0.637 distance: most of the
disagreement is composition (different objects)
rather than transcription (different readings of
the same objects).

**Falsifier.** Matched-object disagreement remains
at or above half the corpus-level distance (0.32),
meaning the compilations genuinely transcribe the
same objects differently, and composition is
exonerated.

## 4. Step 0 — the bridge, and the gate

Object pairs (the same physical inscription in both
compilations) are constructed through the lawful
routes the programme holds:

- **(a)** the CISI catalogue layer — the 7,705-row
  catalogue built in the Phases 120–124 work (98.9%
  sample accuracy; `reports/
  phase124_cisi_image_layer.md`), which carries
  object identifiers on the Parpola/CISI side;
- **(b)** the Mahadevan side's published object
  references, joined through the **Phase-130 intake
  schema**, which exists precisely to admit
  object-level data with provenance;
- **(c)** the **44 Phase-128 evidence dossiers**
  (`reports/phase128_evidence_dossiers_44.csv`),
  which already assemble per-object evidence for
  the contested subset.

Every bridge pair enters as cited data with its
source. **Holdat `cisi_number` is never used as a
join key** (the Phase-131 prohibition stands).

**GATE, fixed in advance:** the bridge must yield
**at least 150 matched objects carrying texts of
three or more signs in both compilations**. Below
the gate, the study closes at step 0 as **TOO THIN
TO ATTRIBUTE**, with the bridge census published as
the finding: how many objects could be paired, by
which route, and where the join ran out — naming
the unblocking act (a published concordance or
object-level dataset entering through intake).

## 5. Method (step 1, if the gate passes)

For each matched object, extract each compilation's
sign sequence; compute the per-sign positional
profiles **on the matched-object subset only**, in
each compilation separately; measure the profile
distance **exactly as Phase-125 did — the same
distance (total variation) and the same count
floors**. Then decompose what disagreement remains:
align the two sequences per object and classify
every difference as

- **segmentation** — the same signs, different cuts;
- **substitution** — a sign mapped differently,
  checked against the crosswalk's conflict pairs;
- **composition residue** — objects present in one
  compilation's subset only.

The output is an attribution table in **Phase-131's
own categories**, so the 6.1% figure and this
study's figure are directly comparable. Profiles
are computed on the pooled matched subset, with
per-object distances reported as a distribution,
not averaged away.

## 6. Criteria (fixed in advance)

On the matched-object median distance:

- **ATTRIBUTED TO COMPOSITION:** at or below
  **0.20** — near Phase-127's noise band of 0.083,
  allowing for the smaller sample.
- **ATTRIBUTED TO TRANSCRIPTION:** at or above
  **0.32** — half the corpus-level 0.637 (the
  falsifier's line).
- **Between:** a split attribution, reported with
  the decomposition table as the result.

The design's success is a measured split, whichever
way it falls: "93.9% unexplained" is replaced with
named shares. Below the step-0 gate, no attribution
verdict exists — the census is the finding (§4).

## 7. Confounders (named in advance)

- **Bridge selection bias.** Objects that *can* be
  matched may be the better-published ones. The
  matched subset's site and object-type mix is
  reported against both compilations' full mixes,
  and any attribution verdict carries the subset's
  description with it.
- **Crosswalk circularity.** The substitution
  classification uses the crosswalk as a *record of
  disagreement*, never as ground truth (762 P↔M
  pairs; 383 conflict pairs).
- **Small samples per object.** Handled by the
  pooled profiles plus the per-object distance
  distribution (§5).

## 8. What this study would NOT establish

Which compilation is *right* where they differ.
Attribution explains disagreement; it does not
crown a winner. Nor does it re-open, soften, or
re-judge the settled Phase-125 verdict.

## 9. Execution shape (Phase-398; frozen here, performed later)

1. **Graph-first build** (H15/H23): script, graph
   module, registration, registration verification,
   then run.
2. **Step 0:** build the bridge through routes
   (a)–(c) as cited data; publish the bridge census;
   apply the §4 gate. Below the gate, close as TOO
   THIN TO ATTRIBUTE and stop.
3. **Step 1 (gate passed):** positional profiles on
   the matched subset under Phase-125's own distance
   and floors; the decomposition; the attribution
   under §6.
4. **Outcome:** recorded in this spec's directory
   and the root LEDGER, with the selection-bias
   report of §7 attached to the verdict. Nothing is
   written into the Phase-125/127/131 records,
   which stand as issued.

## 10. House notes

- **Claims first:** the governed register is
  `claims.json` (F034-C01…C14); every later
  artifact traces to it (H2).
- **Registration before execution:** this frozen
  contract is filed on OSF after the freeze merges
  and before Phase-398 runs (the Spec
  027/028/030/031/032 pattern).
- **Append-only:** outcomes append; the settled
  records are never edited (H1, H21 posture).

## 11. Claim register summary

- **C01** — scope: attributes the Phase-125 residue
  only; never which compilation is right.
- **C02** — the hypothesis (composition over
  transcription, on matched objects).
- **C03** — step 0 builds the bridge through the
  three named routes, as cited data.
- **C04** — the gate: at least 150 matched objects
  with texts of three or more signs in both
  compilations.
- **C05** — below the gate: TOO THIN TO ATTRIBUTE,
  with the census published as the finding.
- **C06** — Holdat `cisi_number` is never a join key.
- **C07** — the measurement repeats Phase-125's
  distance and count floors, on the matched subset
  only.
- **C08** — the decomposition uses Phase-131's own
  categories.
- **C09** — at or below 0.20: ATTRIBUTED TO
  COMPOSITION.
- **C10** — at or above 0.32: ATTRIBUTED TO
  TRANSCRIPTION.
- **C11** — between: a split attribution, with the
  decomposition table as the result.
- **C12** — the selection-bias report: mixes compared,
  and the verdict carries the subset's description.
- **C13** — the crosswalk is a record of
  disagreement, never ground truth.
- **C14** — the settled Phase-125 verdict stands
  untouched by this study.

## 12. Design decisions carried and recorded

- **DD-20-1 (bridge routes; the design's):** routes
  (a)–(c) only, every pair cited; the prohibited
  Holdat join stays prohibited.
- **DD-20-2 (the gate; the design's):** 150 matched
  objects with ≥3-sign texts in both compilations,
  fixed in advance; below it, the census is the
  finding and no attribution is attempted.
- **DD-20-3 (verdict lines; the design's):** 0.20
  and 0.32 on the matched-object median distance,
  with the split-attribution middle — stated before
  any object is matched.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
