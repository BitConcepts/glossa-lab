# Phase-115 — Non-SA Validation Battery v2 for the 44 SA-Lineage Anchors

**Spec:** specs/014-phase115-nonsa44-validation-v2 (frozen before any results) · **Date:** 2026-10-07 · **GPU device:** cpu (torch absent)

## What changed vs Phase-113 (spec 014 sections 1-2, 4)

Phase-113's battery was rejected at calibration (STRICT94 validated 3/94) because T1 starved on the Phase-107 ICIT layer. Diagnosis: a leading-zero key mismatch cost 4,014 source tokens and the all-or-nothing inscription rule discarded the rest. Battery v2 rebuilds the layer and scales T1's attestation floor to each sign's measured opportunity; T2/T3, the gates, and the decision rule are spec 011 unchanged.

- v2 layer: 4531 inscriptions / 13492 mapped tokens (+ 2388 sentinel positions); token-map coverage excl. placeholders 0.9155 (v1: 0.693); sampling ratio r = 1.926878.

## Verdict

**BATTERY REJECTED at calibration.** The frozen gates of spec 014 section 5 were not both met, so FLAGGED44 was never run and the anchors file was not modified. The battery may not be re-tuned under this spec.

## Calibration (executed before the 44; reported whatever it showed)

| Set | n | VALIDATED | DEMOTE | UNRESOLVED | Gate |
|---|---|---|---|---|---|
| STRICT94 (positive, leave-one-out) | 94 | 1 | 57 | 36 | >= 57 required: **FAIL** |
| KUR113 (negative control) | 113 | 0 | 23 | 90 | <= 5 required: **PASS** |

Per-test states (calibration):

| Set | Test | PASS | FAIL | NOT_ATTESTED | INDETERMINATE |
|---|---|---|---|---|---|
| STRICT94 | T1 | 8 | 43 | 43 | 0 |
| STRICT94 | T2 | 60 | 13 | 0 | 21 |
| STRICT94 | T3 | 34 | 19 | 0 | 41 |
| KUR113 | T1 | 26 | 23 | 64 | 0 |
| KUR113 | T2 | 0 | 0 | 0 | 113 |
| KUR113 | T3 | 0 | 0 | 0 | 113 |

## Sets and corpora (recomputed; assertions in spec section 3)

- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).
- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token coverage 0.7368 (5,159 / 7,002).
- KUR113: 113 premise-superseded anchors, all reading `kur`.
- Holdat: 1670 inscriptions / 7002 tokens. ICIT v2 layer: 4531 inscriptions / 13492 mapped tokens (local restricted data; statistics only).

## Limitations (registered in spec section 8)

A PASS certifies distributional and compositional survival under independent non-SA tests; it does not prove the phonetic value. A FAIL demotes to CANDIDATE; it does not declare the reading false. Holdat and the ICIT layer are independent compilations of the same published catalogues, not independent archaeology; sentinel positions preserve positional geometry but the v2 layer measures a broader inscription population than v1.

## Calibration diagnosis (post-hoc, descriptive — no re-tuning performed or permitted)

Appended after the run, from `phase115_nonsa44v2_results.json`
(the generated record above is unaltered):

- **The layer expansion worked as engineered; the battery
  still fails, now on agreement rather than attestation.**
  T1 judged 51/94 strict signs (Phase-113: 33/94), and the
  NOT_ATTESTED count fell from 61 to 43 — but 25/94 strict
  signs still have **zero** tokens in the v2 layer (the ICIT
  corpus's artifact coverage simply does not include them),
  and 42/94 remain below their opportunity floor.
- **Of the 51 judged strict signs, 43 FAIL T1** — 40 on
  modal-class disagreement, median TV 0.79 (not borderline).
  Modal-pair decomposition (Holdat → ICIT): INITIAL→MEDIAL
  18, INITIAL→TERMINAL 7, TERMINAL→MEDIAL 7, MEDIAL→INITIAL
  3, MEDIAL→TERMINAL 4, same-modal TV-only 3. An
  INITIAL↔TERMINAL reading-direction swap accounts for only
  8 — the dominant pattern is Holdat-initial signs appearing
  medial-modal in the ICIT population. Whatever its cause
  (segmentation, inscription-population, or conversion
  differences between the two compilations), positional
  profiles do **not** transfer between Holdat and the ICIT
  layer at the frozen tolerance for most strict-core signs.
- **T2 and T3 tallies are identical to Phase-113's**
  (T2 60/13/21, T3 34/19/41) — the reused machinery is
  unchanged and was never the problem, in either phase.
- **KUR113:** 0 validated (gate passed). Its T2/T3 remain
  INDETERMINATE wholesale (the frequency guard), so the
  negative control confirms — again — only that the battery
  does not validate known-bad readings through the grammar
  tests; T1 alone passes 26 kur signs and fails 23, i.e. T1
  does not discriminate the negative control either.
- **Conclusion recorded:** two independently frozen batteries
  have now been rejected at the same gate for disjoint
  reasons — v1 could not attest the core, v2 attests it and
  finds cross-corpus positional disagreement. The honest
  reading is that a conjunctive cross-corpus gate on this
  pair of compilations is not a validation instrument for
  these anchors. Any further successor would first have to
  establish, as its own pre-registered question, *why*
  Holdat and ICIT positional profiles disagree — a
  corpus-harmonization study, not another battery — and
  requires a new spec and the owner's direction. The 44
  anchors remain `pending_non_sa_validation`; their status
  is unchanged and the question stays open.

## Verification

Recorded in the phase ledger entries and the PR body (full backend suite; foundation check per H21; ruff).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.
