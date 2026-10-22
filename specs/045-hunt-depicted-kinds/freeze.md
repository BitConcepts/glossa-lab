# Spec 045 — Freeze Record (Hunt's Three Parts: Pattern, or Meanings? — Design D-05; Builder of Asset A)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on
> 2026-10-21 (campaign Wave 2; `adjudication.md`
> §7). The AEE lifecycle hooks ran over the
> register first (register recovered to
> 0.8-draft; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 039
> ordering). The freeze also files this spec's
> own OSF contract registration under campaign
> decision E-1 (DD-045-20;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-411** under this frozen contract, as
> a separate later act: it awaits the
> registration's approval and the campaign's
> execution pass (Wave 3), and no sign was
> classified at the freeze.

## 1. Basis

The contract implements design D-05 (PR #195
packet, §D-05) over the claim
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
— Hunt's three-part account of inscription
structure, standing IN QUESTION, partially
supported for position only — and builds
Asset A, the depicted-kind sign
classification three Hunt designs share
(campaign decision E-6). Its factual basis
is the §4 input set as pinned at draft and
**re-asserted at this freeze against `main`
at `881947a0` by two routes** (contents API
and git-data blob API; every pin recomputed
in the foreground and matched): the
positional record (`0e546962…`: 805/2,267,
rate 0.355 against null 0.006; 40/61/20
strong-sign classes), the Phase-43 battery
record (`78a6c219…`), the corpus layer
(`c02e3d7b…`), the crosswalk master
(`4ace1a61…`: 205 rows, 187 distinct
`registry_sign_id` values), and the anchors
file (`df0cf620…`, 287 anchors).

The freeze decided every open point
(`adjudication.md` §7): **DD-045-9** (the
DD-038-10 AEE gate reading adopted),
**DD-045-10** (Phase-411 allocated),
**DD-045-11** (the fit form fixed as
out-of-sample predictive accuracy and the
fit margin frozen at **0.05**, derived from
the recorded positional advantage of 0.506 —
mean initial rate 0.757 against 0.251 by
chance — as one tenth of that advantage),
**DD-045-12** (the §5.2 comparison rule
frozen as the AUC rule), **DD-045-13** (the
pooling threshold frozen at 5 signs),
**DD-045-14** (entry-time jurisdiction
coding confirmed, its rule stated from the
verbatim label alone), **DD-045-15**
(DD-045-2 and DD-045-3 confirmed as drafted),
**DD-045-16** (no second-enterer spot check
added, decided on the record), **DD-045-17**
(the D-18 consumption repair answering Spec
046's DD-046-14: PARTIAL CONCURRENCE given a
consumption rule, CLOSED AT STEP 0 named an
acceptable terminal delivery, and the
null-key disposition stated instead of
rejection — Spec 046's vocabulary unchanged),
**DD-045-18** (coverage restated to the full
pinned-crosswalk sign universe, answering
Spec 050's draft defect 1), **DD-045-19**
(the closing measures disambiguated: this
spec's **closing distinct-predecessor rate**
versus Spec 054's **Phase-43 terminal-strong
set membership** — different measures,
neither adopting the other's form),
**DD-045-20** (the OSF registration filed at
the freeze; execution awaits its approval),
and **DD-045-21** (Spec 046's two digests
quoted in spec §§2.7 and 4 as its record
presents them: freeze-act `80c3be31…`,
successor `e0d7add8…`).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/045-hunt-depicted-kinds/freeze.md` (this
  document)
- `specs/045-hunt-depicted-kinds/spec.md`
- `specs/045-hunt-depicted-kinds/claims.json`
- `specs/045-hunt-depicted-kinds/adjudication.md`
- `specs/045-hunt-depicted-kinds/aee/freeze-aee-note.md`
- `specs/045-hunt-depicted-kinds/build_freeze.py`
- `backend/tests/test_spec045_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds). This spec has no separate
`plan.md`; `tasks.md` carries the plan.

## 3. What the freeze fixes

- **Asset A's contract** (spec §2 / F045-C06
  to C11): one row per sign over the **full
  pinned-crosswalk sign universe** (187
  distinct sign keys; DD-045-18), the §2.2
  field set and no others, labels only from
  the §2.3 held published sources, blind
  entry and freeze before any join, disputes
  coded contested by rule, and dependents
  pinning the asset by digest.
- **The D-18 consumption form** (spec §2.6 /
  F045-C10; DD-045-17): Spec 046's frozen
  `concordance-297.json` delivery consumed
  under its total outcome vocabulary —
  CONSENSUS / PARTIAL CONCURRENCE /
  SINGLE-SOURCE as corroboration (partial
  concurrence counting exactly the one
  independent corroboration it carries),
  CONTESTED as a forced dispute, closure
  files (IDENTIFICATION FAILED, CLOSED AT
  STEP 0) as stated no-input deliveries, and
  null-key records carried under their
  Wells-list-entry reference, never rejected
  and never re-keyed by hand.
- **The test** (spec §5 / F045-C03 to C05,
  C13 to C15): models P and PH on the
  odd/even split, fit as out-of-sample
  predictive accuracy with the frozen margin
  **0.05** (DD-045-11); the closing head-on
  comparison under the frozen **AUC rule**
  (DD-045-12) between depicted-kind
  membership (cycle/sky plus the
  jurisdiction-coded subset, DD-045-14) and
  the **closing distinct-predecessor rate**;
  the one pre-registered sensitivity; and
  the three verdict words of §5.4 with their
  pre-written wordings.
- **The gates** (spec §§3, 6 / F045-C12):
  build gates A1–A6 (A3 at the restated
  full-universe scope) and step-0 gates
  0.1–0.4, fail-closed, before any model
  quantity — including the freeze-order
  proof that the margin and the comparison
  rule were recorded before the first join.
- **The fences** (spec §8 / F045-C01, C16,
  C17): no gloss is established by any
  outcome; depiction is the published
  identification layer, not ground truth;
  Spec 037's 49% census caution travels with
  the asset and every verdict.

## 4. What this freeze does not do

It does not build Asset A (the asset is
BUILT at execution step 1, under the §3
gates, after Spec 046's concordance lands),
classify any sign, open any source volume
for entry, fit any model, join the
classification to the corpus, or file any
outcome on the claim's record. It does not
amend design D-05, Spec 046's frozen record,
or Spec 054's draft. Execution (Phase-411)
is a separate act, gated as stated in the
header above.

## 5. Tooling pins

- AEE package **1.5.0** (pin `>=1.5.0,<1.6`),
  run from the venv `glossa-aee150`.
- specify CLI **1.0.10**; Python **3.12.3**.
- Freeze test: `backend/tests/test_spec045_freeze.py`
  (6 tests), proven able to fail at this
  freeze, before the final digest was
  computed: with a provisional digest in
  place, all 6 tests passed; a scratch
  mutation (one appended line,
  `MUTATION-PROBE`, in the covered source
  `spec.md`) turned `test_freeze_record_replays`
  red (1 failure, the other 5 still passing);
  restoring `spec.md` byte-identically
  returned all 6 tests to green. The mutation
  was a scratch probe only and is not part of
  the frozen tree.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
