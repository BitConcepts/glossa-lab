# Spec 074 — Execution outcome

**Date:** 2026-10-24
**Execution:** Phase-440, two runs, byte-identical results
(`reports/phase440_results.json`, SHA-256
`d539519d6949d6ce73654290a49a0e629141a89082f7034e201135e9af1c3bc1`)
**Freeze:** digest `5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c`
(contract-level recompute, freeze PR #368, merged `c561f293`)
**Registration:** OSF cfe7z (submitted 2026-10-24; approved by the owner and
public — the approval completed before this execution opened), DOI
10.17605/OSF.IO/CFE7Z
**Owner's order:** 2026-10-24 19:04 EDT — "Shouldn't we do all three of
these?" — Spec 070 re-frozen as this successor AND executed; the OSF approval
completed before the run.

## Outcome: NOT SUPPORTED

The frozen question — *are Shakti's opening signs the animal signs?* — is
answered **no, not in the re-scoped form the freeze states**. All six step-0
gates passed, including gate 0.4's reproduction assertion: the enumerated
population reproduces Spec 070's recorded measurement **exactly** — the
canonical publication hash of the executed enumeration is identical to Spec
070's recorded hash (`30092b6f…`), the 31 signs and their per-sign I/M/T
counts are equal, and the full battery census (220 signs at the floor) is
equal. Every one of the 31 signs then keyed to exactly one Asset A v2 row
under the frozen two-leg route (DD-074-8): 26 under leg 1 (parpola_1982
wells_ids), and the five signs Spec 070 could not key — 136, 298, 401, 617,
824 — under leg 2 (Registry v2's icit_wells rows), to their own W-keyed rows,
each classified `unidentified` in the frozen asset. No POPULATION NOT KEYED
closure applied; keying is not classification, and the five enter the counts
as unidentified — counted, listed, excluded from the primary's numerator and
denominator.

Measured on the graded ICIT corpus, of the 31 opening-strong signs Shakti's
own battery returns, **2 are animal signs** under the frozen classification
(226 and 241, both fish signs) — a share of 0.0769 (2 of 26 classified
members) against the animal share 0.0889 (8 of 90) over the disjoint table's
classified universe: **enrichment ratio R1 = 0.8654, Fisher exact one-sided
p = 0.7345** (two-sided p = 1.0). Animal signs appear among the opening-strong
signs at no better than the base rate. The precedence of section 4.3 gives
**NOT SUPPORTED** on rule 1's first ground alone (R1 ≤ 1.0), and on its
second ground independently (p ≥ 0.05). The frozen falsifier of section 1.2
fires. The reversed arm agrees in direction, so no rule-1 asymmetry arises:
within the comparison inventory, **none** of its six animal signs is
opening-strong (R2 = 0.0; the population's two animal signs occur 21 and 10
times, below the inventory's 30-occurrence floor). The sensitivity arms agree:
S-A equals the primary (Asset A v2 carries zero contested rows); S-B is not
applicable (no Asset A v2 verbatim label identifies a unicorn); S-C, on the
documented + corroborated population (O = 35, U = 89), returns the same word
— R1 = 0.8929, p = 0.7140 — so the result is **not grade-sensitive**.

This is the first verdict the claim's animal half has had, in either
direction: Spec 070 closed before scoring; this successor scores. The
headline wording of section 4.6 (NOT SUPPORTED form) is recorded verbatim in
`reports/phase440_results.json` and `reports/phase440_report.md`, and the
dated append `spec074_outcome_append_2026_10_24` carries it onto the claim's
record. The claim
(`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`) stands
partially supported on its positional half alone, stage explained,
falsification condition unchanged. **Spec 070's closure stands unamended
beside this outcome; the claim's record carries both attempts, each under its
own spec.**

**Honesty fence (spec section 6.2).** This test measures Hunt's claim
against a positional framework measured on the graded ICIT corpus (the
Shakti corpus). It does not test it against the Phase-43 framework. The
recorded Phase-43 quantities — 805/2,267 and the 40/61/20 strong-sign
classes — are never this spec's basis.

**Lineage (P-F1 S3, verbatim).** This corpus is an ICIT-lineage corpus.
Agreement between it and the program's earlier ICIT-lineage layer is
consistency within one tradition, not independent corroboration.

**Classification (spec section 6.4).** Asset A v2 — SHA-256
`681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`; 552 rows;
per-kind counts: animal 30, sky_cycle 0, object_goods 22, human 43,
other 246, contested 0, unidentified 211.

**Fence sentence (spec section 6.9).** This result is about depiction and
position in recorded data. It is not evidence that any sign marked identity,
a guild, or goods.

**Cross-compilation caution (spec section 8, limit 3).** Spec 037's census
records object-type labels diverging in 49% of matched cases between
compilations. Depiction in Asset A v2 is the field's published identification
for this compilation — and the 49% fact travels with this result as its
standing caution.

## What was executed

1. **Step-0 gates (spec section 5), fail-closed, in order — all PASS.**
   Gate 0.1: Spec 073's executed record shows both products frozen; Registry
   v2 and Asset A v2 recompute to their digests; Asset A v2's per-kind
   counts match the freeze record. Gate 0.2: the Shakti corpus and the
   row-grade file hash to their pins; the census reproduces (5,704 rows;
   5,536 analyzable; grades 3,212 / 2,087 / 405; 4,904 CISI-carrying).
   Gate 0.3: the Phase-433 record, Registry v1, the crosswalk, and the
   anchors hash to their freeze values; this spec's own freeze record
   carries digest `5416a0d3…`. Gate 0.4: the population reproduced exactly
   (above) and keyed 31/31 under the two-leg route. Gate 0.5: the comparison
   inventory enumerated — 76 signs at total ≥ 30 under DD-070-10's counting
   rule (73 classified: 6 animal, 67 non-animal; 0 contested; 3 unidentified
   — 501, 585, 617); every O and U sign carries an Asset A v2 row; the S-B
   unicorn naming scan returns no sign. Gate 0.6: the order stands recorded
   in the machine record — v2 digests from Spec 073's executed record and
   the recorded enumeration from Spec 070's at the freeze; the population
   hashed at gate 0.4 before any join was computed.
2. **The frozen section 4 test, exactly.** The opening-strong set was
   enumerated in Wells space before any join (its hash published before the
   join's result could exist, in-spec section 4.1's sense); the disjoint
   2×2 over classified members is [[2, 24], [6, 58]]; the reversed arm's
   table is [[0, 6], [9, 58]]; both arms' exact tests and all three
   sensitivities ran as frozen. The full counts — every cell, both sets'
   sizes, the contested and unidentified tallies, and the per-sign
   classification tables for O and for U — are published in
   `reports/phase440_report.md` and the machine record.
3. **Scored only in the frozen section 4.6 wordings**, as re-pointed by this
   spec (section 4.6's NOT SUPPORTED form, quoted in the report).

A note on the ratio's denominator, for the reader recounting from the
published tables: the carried instrument computes the baseline share over
the disjoint table's classified universe (O together with U∖O: 8 animal of
90), as Spec 070's frozen machinery defines it; the animal share of the
inventory's own classified members is 6 of 73 (0.0822), published beside it
in the report. The headline word is the same under either denominator —
section 4.3 rule 1 fires on R1 ≤ 1.0 and on p ≥ 0.05 independently, and the
exact test's p is a property of the table under both readings.

## What this does NOT establish (spec section 8, binding)

- **No meaning conclusion.** Depiction and position coincide or fail to
  coincide in recorded data; that animal signs marked identity, a guild, or
  goods remains Hunt's reading of the coincidence, not a measurement of this
  test — and its absence here is not a measurement against the reading
  either: the test answers the re-scoped enrichment question and nothing
  more.
- **Depiction is not ground truth.** Asset A v2 is the field's published
  identification layer, with citations; the verdict is a statement about
  that layer, carrying Spec 037's 49% cross-compilation caution.
- **Nothing about the Phase-43 framework, in either direction** (the honesty
  fence above is a limit, not a preface).
- **Nothing about any other book's claims, and nothing about Spec 070's
  record** — its POPULATION NOT KEYED closure stands exactly as recorded;
  this successor amends no predecessor record.
- **No claim status or stage change.** The animal half is recorded as not
  supported *in its re-scoped form*; the claim's record is amended only by
  the dated append carrying this outcome.

## Landing

[To be completed by the landing record: execution PR, CI run, merge commit,
foundation posture.]

## Records

- `reports/phase440_results.json` — the machine record (contract, gates, the
  gate 0.4 reproduction record, the keyed population, both classification
  tables, both arms, all sensitivities, the headline wording, the anchors
  assertion; SHA-256
  `d539519d6949d6ce73654290a49a0e629141a89082f7034e201135e9af1c3bc1`,
  byte-identical across the two runs).
- `reports/phase440_report.md` — the plain-language report carrying the
  section 6 headline items and the full section 4.2 counts.
- `specs/074-hunt-opening-signs-repaired-surface/step0-record.md` — the
  step-0 record.
- The claim's dated append
  `spec074_outcome_append_2026_10_24` (store SHA-256 before the append
  `4e0822ad…`, after `e78ecba1…`; append-only diff — status, stage, and
  falsification condition untouched).
- Anchors asserted byte-identical before and after
  (`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both
  readings).

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.*
