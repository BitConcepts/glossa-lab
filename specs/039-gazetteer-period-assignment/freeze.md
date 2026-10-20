# Spec 039 — Freeze Record (Gazetteer Period Assignment: the Spec 027 §6.2 Act)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> This record is finalised at the freeze act.
> The digest in `freeze.json` at this draft is a
> **draft digest**, computed by `build_freeze.py`
> over this draft contract (register 0.5-draft)
> under the owner's decisions of 2026-10-20
> (`adjudication.md`). At the freeze act — in the
> bundle sequence (`plan.md`) — the AEE lifecycle
> hooks run over the register first, and the
> digest is recomputed **exactly once** over the
> recovered register and the finalised freeze
> texts (the Spec 035 ordering). The draft digest
> decides nothing and is not the freeze digest.

## 1. Basis

The contract implements the Spec 027 §6.2
gazetteer period-assignment act under the owner's
decisions of 2026-10-20: the act authorised and
bundled with the D-25 chronology test, and the
evidence standard fixed at **Option 1 — published
period determinations only** (no program-derived
assignments). Both decisions stand recorded as
DECIDED in `adjudication.md` §1; the freeze does
not re-ask them.

The design's factual basis is the gazetteer as it
stands on `main` (`data/movement/gazetteer_rows.jsonl`,
SHA-256
`5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`;
36 rows, 30 sites, `program_period_assignment`
null on all 36 rows), Spec 031's frozen period
rule (F031-C10), and the Phase-395 margins record
(0 eligible sites; in-universe link mass 2 sites /
1 pair against floors of 8 / 10) — all verified
first-hand at this draft (`adjudication.md` §3).

The freeze also decides the open points
(`adjudication.md` §4): **DD-039-1** (the label
set; recommended: Early / Mature / Late Harappan),
**DD-039-2** (the source hierarchy; recommended:
four citation tiers, never a resolution rule),
**DD-039-3** (when a TwoRains determination counts
as published; recommended: journal articles,
their published supplements, and published report
series, with a locator — theses, project datasets,
and deposits do not count, and doubtful venues
default to not counting), **DD-039-4** (Masudpur
establishment; recommended default: not in this
act), **DD-039-5** (the margins re-run as this
act's verification step; recommended: yes,
confined to the period-eligibility gate), and
**DD-039-6** (the spec's own OSF contract
registration; proposal: yes, per the DD-035-4 /
DD-036-4 precedent).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/039-gazetteer-period-assignment/freeze.md` (this document)
- `specs/039-gazetteer-period-assignment/spec.md`
- `specs/039-gazetteer-period-assignment/claims.json`
- `specs/039-gazetteer-period-assignment/adjudication.md`
- `specs/039-gazetteer-period-assignment/aee/freeze-aee-note.md`
- `specs/039-gazetteer-period-assignment/build_freeze.py`
- `backend/tests/test_spec039_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds).

## 3. What the freeze would fix

- **The evidence standard** (spec §3 / F039-C02,
  C03): published period determinations only,
  each cited with its locator; no label from
  spine dates, analogy, or unpublished material.
- **The label set and mapping discipline**
  (spec §4 / F039-C05): the DD-039-1 set;
  scheme-aware mapping under a table frozen
  before any assignment; unmapped values yield
  blanks with reason codes, never improvised
  mappings.
- **The disagreement posture** (spec §5 /
  F039-C09, C10): contested assignments flagged
  and carried verbatim; no majority vote; no
  hierarchy resolution; both-ways reporting
  downstream. Spec 030 Ask 2 stays reserved and
  is not decided.
- **The record's shape** (spec §6 / F039-C06–C08,
  C11, C12): site-level assignments carried on
  every row, each with its mapping rule, reviewer,
  and per-determination citations; the pre-act
  gazetteer preserved byte-identically outside
  the assignment field; the Stage 0 Zenodo
  deposit superseded only by a new version.
- **The fences** (spec §§1, 8, 10 / F039-C01,
  C13–C15): assignments are published-record
  statements, not dating evidence; no study
  verdict changes; the verification step re-runs
  only the period-eligibility gate and states the
  unchanged link mass (2 sites / 1 pair) against
  its floors.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
