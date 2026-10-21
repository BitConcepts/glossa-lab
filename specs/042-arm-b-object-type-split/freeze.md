# Spec 042 — Freeze Record (Arm B Object-Type Split, Design D-28)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the campaign plan approved as written on
> 2026-10-21 (authorisation E-1; campaign
> Wave 2). The AEE lifecycle hooks ran over
> the register first (register recovered to
> 0.7-draft; `aee/freeze-aee-note.md`), and
> the digest in `freeze.json` was then
> computed over the recovered register and
> the finalised freeze texts (the Spec 035
> ordering; §6 records the one correction
> made before filing). Every spec §2
> input pin was re-derived in the foreground
> by two independent routes before digesting
> (§2 below). The freeze also files this
> spec's own OSF contract registration
> (DD-042-6; `osf-registration.md`, completed
> by append after filing). Execution runs as
> **Phase-407** under this frozen contract,
> on a separate execution order, and awaits
> the registration's approval.

## 1. Basis

The contract registers design D-28 from the
PR #195 experiment-design packet as a primary
test: Spec 028's Arm B (equal site weights),
machinery unchanged, run separately on the
seal-only and tablet-only sets of the
Phase-393 analysis population, each stratum
under the frozen family verdict rules, the
headline pre-registered as one of SPLIT /
UNIFORM-PASS / UNIFORM-FAIL / THIN. The claim
under test is `STUDY-SPEC-028/ARM-B`,
standing INCONCLUSIVE on its recorded
numbers (spec §1); this variant appends to
its record and never edits it (DD-042-1).

The freeze decided the draft's open items
(`adjudication.md` §6): **DD-042-6** (this
spec files its own OSF contract registration
at the freeze), **DD-042-7** (a fresh
synthetic calibration is **declined** — the
machinery is byte-identical to Spec 028's
calibrated pipeline of record, and gate 0.5's
exact reproduction of the recorded pooled
quantities is the variant's machinery check),
**DD-042-8** (no separate margins audit —
the gate-0.3/0.4 census is this variant's
margins instrument, as the draft proposed),
and **DD-042-9** (the DD-038-10 AEE gate
reading adopted). **DD-042-2** (THIN closes
the whole execution) and **DD-042-3** (NOT
ADJUDICATED is the control-failure class)
are **confirmed** as drafted. **DD-042-5**
is discharged: the execution phase is
**Phase-407**, allocated at this freeze
in the campaign allocation (the draft
recorded Phase-400 through Phase-403
already taken).

## 2. Pin verification at the freeze

Every §2 pin was re-derived in the
foreground at this freeze, by two routes —
(route 1) the contents API raw download
hashed with `sha256sum`; (route 2) the
contents API payload decoded and hashed
with Python `hashlib` (the corpus layer,
over the API's 1 MB content limit, streamed
through `hashlib` as route 2) — and both
routes agreed with the draft's pins and
with each other on all six inputs:

- corpus layer `c02e3d7b…` (full:
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`)
- Phase-393 results `0a1657a8…`
  (`0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607`)
- pipeline393.py `6c2ff91c…`
  (`6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e`)
- Spec 028 margins audit `15ae0281…`
  (`15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d`)
- Spec 028 freeze record `376cd8e7…`
  (`376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc`)
- anchors file `df0cf620…`
  (`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`)

No pin moved between the draft and the
freeze. The stratum census (gates 0.3/0.4)
was **not** computed at the freeze: it
appears nowhere in the frozen record, by
design.

## 3. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/042-arm-b-object-type-split/freeze.md` (this
  document)
- `specs/042-arm-b-object-type-split/spec.md`
- `specs/042-arm-b-object-type-split/claims.json`
- `specs/042-arm-b-object-type-split/adjudication.md`
- `specs/042-arm-b-object-type-split/aee/freeze-aee-note.md`
- `specs/042-arm-b-object-type-split/build_freeze.py`
- `backend/tests/test_spec042_freeze.py`

`tasks.md` and `osf-registration.md` are
lifecycle bookkeeping and are not
digest-covered (the house rule since
Spec 026: plans change as work proceeds;
the OSF record is completed by append after
filing).

## 4. What the freeze fixes

- **The gates** (spec §3 / F042-C09): five
  step-0 gates, in order, fail-closed —
  input integrity, population reproduction,
  partition census, stratum floors, exact
  pooled regression — before any stratum
  quantity is computed.
- **The floors and the THIN closure**
  (spec §3 gate 0.4 / F042-C08): at least 6
  sites carrying at least 20 inscriptions of
  the type, per stratum; either stratum
  below its floor closes the execution with
  headline THIN and neither stratum is
  computed (DD-042-2).
- **The verdict rules** (spec §4.1 /
  F042-C10): Spec 028's frozen family rules
  carried verbatim — margin 0.01, seed
  20261012, SUPPORTED / CONTRADICTED /
  INCONCLUSIVE as written there; the freeze
  alters none of them. Control failure is
  NOT ADJUDICATED (DD-042-3).
- **The headline pattern** (spec §4.2 /
  F042-C11, C12): exactly one of SPLIT (with
  direction: AS PREDICTED or REVERSED),
  UNIFORM-PASS, UNIFORM-FAIL, THIN, under
  the pre-written wordings of spec §4.3.
- **The machinery evidence posture**
  (DD-042-7, DD-042-8): no fresh synthetic
  calibration and no separate margins audit
  stand between this freeze and execution;
  gate 0.5's exact reproduction and the
  gate-0.3 census carry those checks, at
  execution, fail-closed.
- **The fences** (spec §7 / F042-C01, C14,
  C15): no movement conclusion, no
  mechanism conclusion, period described
  not controlled, Arm C's figures cited as
  the hypothesis's source only.

## 5. What the freeze does not do

It computes nothing: no census, no stratum
quantity, no repertoire statistic. It does
not execute Phase-407 (a separate order),
does not approve the OSF registration
(approval proceeds by the standing OSF
route; execution awaits it), and does not
touch Spec 028's files, the anchors file,
or any other spec's record.

## 6. Freeze-test able-to-fail proof

`backend/tests/test_spec042_freeze.py` was
proven able to fail before the digest was
computed: with the completed test in place,
one covered source (this file's §1 phase
line, mutated in a scratch copy of the tree)
made `test_freeze_record_replays` fail on
the digest/source-hash check; the mutation
was then removed and the suite re-ran green
over the unmutated tree. The proof ran in
the freeze scratch tree, never against the
merged record.

One correction before filing, recorded
openly: a first builder run over the
near-final texts exposed two mismatches in
the new test file's constants (a
header-inclusive line count for the corpus
layer; one wording assertion) and a
strict-loader call where the family loads
its registers leniently. The test file was
corrected, and the digest of record is the
recomputation over the corrected, finalised
texts — made before the OSF filing and
before any push, and not repeated after.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
