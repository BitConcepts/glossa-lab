# Spec 040 — Freeze Record (D-25: G1 chronology-controlled rerun)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> This record is finalised at the freeze act.
> The digest in `freeze.json` at this draft is
> a **draft digest**, computed by
> `build_freeze.py` over this draft contract
> (register 0.5-draft) under the owner's draft
> order of 2026-10-20 (`adjudication.md`). At
> the freeze act — on the owner's freeze order,
> after spec §1's dependency gate is verified
> and the AEE lifecycle hooks pass over the
> recovered register — the digest is recomputed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 035
> ordering), with the Spec 039 assignment
> artifact's path, version, and SHA-256 named
> into the definition in the same act. The
> draft digest decides nothing and is not the
> freeze digest.

## 1. Basis

The contract implemented is design D-25 (PR
#195 portfolio) over the Spec 025 / Phase-140 /
Phase-385 record: G1 SUPPORTED under
composition and preservation control,
margin-completed at the governing basic
interval [0.1838, 0.2102] against the V = 0.10
floor, with the standing rider that chronology
is not controlled. The owner's 2026-10-20
bundle decision sequences the gazetteer act
(Spec 039, published determinations only)
before this spec, and spec §1 turns that
sequence into a fail-closed freeze gate: no
executed Spec 039 labels in the §4 form, no
freeze.

The freeze also decides the open design
proposals (`adjudication.md` §3): **DD-040-1**
(the interval-at-margin decision rule,
re-derived from Spec 025's p-only rule),
**DD-040-5** (the thinness closure's word:
NOT-YET-TESTABLE as drafted), **DD-040-6**
(the third margins arm: ≥ 1,000 permutable
inscriptions), and **DD-040-9** (filing the
frozen spec's own OSF registration). The
execution phase number is allocated in the
same act (DD-040-10).

## 2. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/040-d25-g1-chronology-controlled/freeze.md`
  (this document)
- `specs/040-d25-g1-chronology-controlled/spec.md`
- `specs/040-d25-g1-chronology-controlled/claims.json`
- `specs/040-d25-g1-chronology-controlled/adjudication.md`
- `specs/040-d25-g1-chronology-controlled/aee/freeze-aee-note.md`
- `specs/040-d25-g1-chronology-controlled/build_freeze.py`
- `backend/tests/test_spec040_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not
digest-covered (the house rule since Spec
026: plans change as work proceeds).

## 3. What the freeze would fix

- **The dependency** (spec §1 / F040-C02):
  the Spec 039 freeze digest, outcome, and
  assignment artifact (path, version,
  SHA-256) named in this record; a freeze
  without them is not a freeze of this
  contract.
- **The assignment discipline** (spec §4 /
  F040-C04): unique uncontested published-
  determination mappings at site-period
  resolution; everything else is UNASSIGNED
  in the primary; contested mappings enter
  only the labelled sensitivity under their
  frozen sensitivity labels.
- **The margins gate** (spec §5 / F040-C12):
  ≥ 5 sites in each coarse period, ≤ 40%
  unassigned, ≥ 1,000 permutable (third arm
  per DD-040-6); failure closes the execution
  NOT-YET-TESTABLE before any outcome
  quantity exists.
- **The primary test** (spec §6 /
  F040-C05…C08): the Phase-137 population and
  columns; strata composition × preservation
  × period; χ² with 9,999 permutations under
  seed 20261009; the Phase-385 v2 basic
  bootstrap interval (B = 4,999, seed
  20261012) governing against the V = 0.10
  margin.
- **The outcome mapping** (spec §6.4 /
  F040-C09…C11): interval entirely above the
  margin → SUPPORTED — CHRONOLOGY CONTROLLED
  (rider retired by append); straddling →
  WEAKENED — RIDER CONFIRMED AS MATERIAL (G1
  restated as a period-confounded
  association); entirely at or below →
  CONTRADICTED AT THE DECLARED MARGIN.
- **The record discipline** (spec §10 /
  F040-C15): dated appends only; the lineage
  label and assignment census on every
  headline; no frozen record edited; no
  anchor moved; no PRED contact.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
