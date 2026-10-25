# Spec 074 — Adjudication Record

> Draft record for Spec 074 (successor to
> Spec 070, design D-06), written 2026-10-24
> under the owner's order of the same date:
> re-freeze and execute Spec 070's question on
> the repaired surface. Sections 1–7 are the
> draft record; the freeze rulings are §8,
> added at the freeze act. Spec 070's
> adjudication record stands untouched; this
> record cites it, and edits none of it.

## 1. The adopted basis (operative substance)

- **The owner's order (2026-10-24).** Re-freeze
  and execute Spec 070 on the repaired
  surface. The act is a successor spec —
  Spec 070's closure (POPULATION NOT KEYED,
  Phase 433) stands unamended, and this
  spec's commission covers draft, freeze,
  and OSF filing; execution follows as a
  separate gated act.
- **Spec 070's outcome record (§3 of its
  outcome).** "A successor that wants this
  question answered must first repair the
  keying surface — a registry that carries
  Wells identities for these signs, or a
  different freeze-fixed route — and that is
  a new freeze decision, not a repair this
  execution was permitted to make at run
  time." This spec is that new freeze
  decision.
- **Spec 073's executed record (Phase 436,
  PR #354; outcome REPAIRED WITH NAMED
  SHORTFALL).** Registry v2 and Asset A v2
  are frozen products on the merged record;
  the 31-sign opening-strong set keys 31 of
  31 under them; the named shortfall (token
  999 without published identity; the
  celestial class empty) does not touch this
  spec's population or its animal class, and
  its token-999 consequence is carried in
  spec §7.
- **The carried design.** Spec 070's design
  is carried verbatim in substance — claim,
  falsifier, §2 battery, §4 test, §4.3
  precedence (from DD-049-3), sensitivities,
  grade discipline, reporting, limits — with
  the changes named in spec §1.3 and nowhere
  else.

## 2. Verification record at draft

All facts below were verified first-hand at
drafting, on the merged tree at `1978a4a6`
(main after PR #367) or at the files'
restricted-local paths:

- **Pins recomputed in the tree.** Registry
  v2 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`
  (1,013 rows); Asset A v2
  `681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`
  (552 rows); Registry v1 `8a0b2a82…` and
  Asset A v1 `95231935…` still recompute to
  their own pins (the v2 products' carried
  rows are what Spec 073's record says they
  are); crosswalk `4ace1a61…`; anchors
  `df0cf620…`; `reports/phase433_results.json`
  `667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214`.
- **Shakti files hashed at their
  restricted-local paths** (never in git):
  corpus `345241b1…` and row-grades
  `02394241…` equal the intake record's pins.
- **Asset A v2 census counted from the
  file:** other 246, unidentified 211,
  human 43, animal 30, object_goods 22 —
  agreeing with Spec 073's
  `asset-a-v2-freeze.json`; contested rows 0
  and sky_cycle rows 0 (the freeze record's
  per-kind map omits both keys; the file
  itself was counted, so the zeroes are
  observed, not inferred from an absence).
- **Keying simulation over the pinned
  files.** Spec 070's recorded 31 Wells
  codes were resolved against Registry v2
  (`parpola_1982` rows' `wells_ids`, split
  on `|`; plus the `icit_wells` rows) and
  the resolutions checked against Asset A
  v2's `sign_key` set: all 31 resolve to
  exactly one Asset A v2 row. The combined
  Wells map carries 708 distinct Wells ids,
  zero resolving to more than one sign —
  agreeing with Spec 073's M1 accounting
  (498 carried + 210 new = 708). The five
  formerly unkeyable signs resolve through
  the `icit_wells` leg to their own W-keyed
  Asset A v2 rows, each classified
  `unidentified` in the asset (a fact Spec
  073's outcome record states per sign).
  No test quantity was computed: no
  inventory, share, ratio, or p was derived
  at drafting, and the simulation recorded
  resolutions only.
- **Census arithmetic.** Spec 070's recorded
  class census sums as recorded:
  42 + 81 + 37 + 6 + 23 + 31 = 220 signs at
  the floor.

## 3. Double derivation of acceptance tests (doctrine requirement)

The freeze's acceptance tests were derived
twice — once from the commissioning order
and the predecessor records, once from the
programme's standing freeze pattern (Specs
052/054/040) — and the two derivations
agree on: (a) the freeze gate is the AEE
lifecycle hooks in the DD-038-10 form (zero
correctness failure modes; no claim below
0.70 propagated confidence); (b) the digest
is computed exactly once, after the gate
passes, over the recovered register and the
final texts; (c) the freeze tests replay
the record and are proven able to fail by a
one-place mutation before the digest is
relied on; (d) the PR merges only on
genuine CI green read from the run's own
job conclusions; (e) the OSF registration is
filed at the freeze and its approval is the
owner's act, never the filing worker's.
Two points where the derivations differed,
resolved here: (i) **the population
reproduction assertion** — the commission
requires a keying gate that reproduces
31/31; the standing pattern adds that a
successor on identical pinned inputs asserts
the enumeration itself, so gate 0.4 asserts
both (spec §1.3, change 3), with its own
closure class; (ii) **the phase number** —
both derivations allocate it mechanically
at the freeze from the merged record; the
highest phase there is Phase-439 (Spec
040), so this freeze allocates the next.

## 4. What the freeze decision is asked to decide

1. **OPEN-074-1 (the v2 digests).** Copy
   Registry v2's and Asset A v2's SHA-256
   values from Spec 073's executed record
   (its two freeze records) into this spec's
   freeze record, character for character,
   with Asset A v2's per-kind counts.
   Mechanical, but stated as a freeze item
   so it cannot be finessed: gate 0.1
   asserts exactly these values.
2. **OPEN-074-2 (the keying route, two
   legs).** Fix the exact route of §4.1:
   the `parpola_1982` leg of DD-070-9 over
   Registry v2 first; the `icit_wells` leg
   for signs the first leg cannot resolve;
   zero or multiple resolutions across both
   legs is unkeyable. This is the
   successor's one genuine design decision —
   the "different freeze-fixed route" Spec
   070's outcome record contemplated,
   stated as a route over the repaired
   registry rather than a new invention.
3. **OPEN-074-3 (the reproduction
   assertion and its closure class).**
   Confirm gate 0.4's assertion — enumerated
   set and per-sign counts equal to Spec
   070's recorded 31, and the class census
   equal to Spec 070's recorded census —
   and the closure class POPULATION NOT
   REPRODUCED for a difference.
4. **OPEN-074-4 (the unkeyable-sign
   disposition).** Decide, in advance, the
   disposition of a named unkeyable sign at
   gate 0.4. The draft proposes carrying
   DD-070-11 unchanged: closure as
   POPULATION NOT KEYED. The alternative —
   a stated continuation — was the branch
   Spec 070's freeze rejected, for the
   recorded reason; a successor that
   reverses it must say so openly and say
   why the reason no longer holds.
5. **OPEN-074-5 (OSF).** Whether this spec
   files its own OSF contract registration
   at its freeze, as a new registration for
   a new spec, per the programme's standing
   pattern (Specs 069/070/071 and the
   2026-10-23/24 freezes all filed their
   own).
6. **OPEN-074-6 (phase number).** Allocate
   the execution phase number at the
   freeze, mechanically, from the merged
   record as it then stands.

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

- **DD-074-1 — Same question, same
  discipline.** The claim, its falsifier,
  the §2 battery, the §4 test form, the
  §4.3 precedence, and the sensitivities
  are Spec 070's, carried; the successor's
  novelty is confined to the keying surface
  and the reproduction assertion (spec
  §1.3).
- **DD-074-2 — Spec 070's closure stands.**
  No outcome of this spec amends, reopens,
  or completes Spec 070; the claim's record
  carries both attempts under their own
  specs (§8, limit 6).
- **DD-074-3 — Keying is not
  classification.** The five formerly
  unkeyable signs enter the primary's
  tallies exactly as Asset A v2 classes
  them — `unidentified`: counted, listed,
  excluded from numerator and denominator
  (§4.1). Their keying is never reported
  as a depiction.
- **DD-074-4 — No phase at draft.** The
  execution phase is allocated at the
  freeze act (OPEN-074-6).
- **DD-074-5 — Evidence observed_at of the
  draft.** Evidence items carry the draft
  date because the cited facts were
  verified first-hand at drafting (§2).
- **DD-074-6 — The AEE freeze gate in the
  DD-038-10 form.** The gate is tasks L4:
  the lifecycle hooks at after_specify,
  after_plan, and after_tasks, with zero
  correctness failure modes and no claim
  below the 0.70 threshold; the digest is
  computed over the recovered register
  exactly once, after the gate passes.

## 6. Design defects and ambiguities found at drafting

- **Spec 070 §4.1's "no recorded count
  stands as its check" vs this spec's
  reproduction assertion.** Not a conflict:
  Spec 070's rule governed its own first
  measurement against *other* counts (40;
  Phase-43 counts). This spec's assertion
  runs against Spec 070's own recorded
  measurement on identical pinned inputs,
  and is named as a change (spec §1.3,
  change 3) rather than read into Spec
  070's text.
- **Asset A v2's freeze record omits the
  zero kinds.** Its `per_kind_counts` map
  has no `sky_cycle` or `contested` key.
  Resolved at drafting by counting the
  canonical CSV directly (§2): both are 0,
  and the freeze record quotes the counts
  as counted from the file.
- **DD-070-9's trailing sentence** ("The
  resolved sign must also carry an Asset A
  row; gate 0.5's coverage scope check
  applies") is carried into this spec's
  gates 0.4/0.5 without change of substance:
  resolution to a `sign_key` with no Asset
  A v2 row is a coverage failure at gate
  0.5 (INVALID), not a keying success.
- **The unicorn's label under Asset A v2**
  is an execution-time naming (gate 0.5),
  as it was under Spec 070; nothing at
  drafting turns on it, and S-B's
  not-applicable branch is carried.

## 7. Bottom line

Spec 070 asked the right question on a
surface that could not carry it, and closed
honestly at its own gate. Spec 073 repaired
the surface and named its shortfall. This
successor changes nothing about the question
and exactly the things the repair requires —
the registry and asset it consumes, one
added keying leg, and a reproduction
assertion that exists because the population
is now a recorded measurement — and it
carries the predecessor's conservative
dispositions unless the freeze overturns
them openly. If the join is ever run, its
verdict will be the first verdict the
claim's animal half has had, in either
direction.

## 8. Freeze rulings (2026-10-24)

*(Freeze act under the owner's order of 2026-10-24,
"Shouldn't we do all three of these?", covering the
re-freeze of Spec 070's question on the repaired
surface; executed by the freeze worker per the standing
freeze pattern (Spec 040's §5.6 precedent): every open
item is ruled per the draft's stated default; a
predecessor record's decided position stands; a genuine
unresolved choice takes the more conservative option
and is recorded and flagged as such. §1–§7 above are
unchanged; the DD-074-1 to DD-074-6 readings stand as
drafted. The rulings below were already carried in the
frozen register's claim boundaries (F074-C05, F074-C08,
F074-C11), this draft having been written against the
decided positions they record; the hooks' final round
ran over the register with the rulings in place (see
aee/freeze-aee-note.md).)*

**DD-074-7 — OPEN-074-1: the v2 digests are copied, and
re-verified.** The two frozen pins are copied character
for character from Spec 073's executed record
(`specs/073-keying-surface-repair/registry-v2/registry-v2-freeze.json`
and
`specs/073-keying-surface-repair/asset-a-v2/asset-a-v2-freeze.json`
on the merged tree) and were re-verified by
recomputation on the merged tree at this freeze:
canonical registry v2 SHA-256
`42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`
(1,013 rows) and Asset A v2 SHA-256
`681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`
(552 rows; per-kind counts animal 30, sky_cycle 0,
object_goods 22, human 43, other 246, contested 0,
unidentified 211 — the two zero kinds counted from the
canonical CSV itself at this freeze, Spec 073's per-kind
map in the freeze record omitting both keys).

**DD-074-8 — OPEN-074-2: the two-leg keying route.**
The step-0 keying route of spec §4.1 is ruled in the
form recorded in the boundary of F074-C08: leg 1 is
DD-070-9's rule carried (an attested opening-strong
sign keys by its Phase-433 recorded Wells code when the
canonical registry v2 carries a row for that code under
any numbering); leg 2, for a sign with no attested Wells
code in the Phase-433 record, is that the canonical
registry v2 rows built by Spec 073 from the ICIT Wells
catalogue (source system `icit_wells`) are consulted,
the sign ID of the row being the sign's own Wells code,
and the sign keys to the Asset A v2 row of that sign
key; zero matches across both legs, or multiple Asset A
v2 rows under the resolved key, make the sign unkeyable
under this freeze, with no further search admitted.
The population-side counting rule — an attested sign
with no keyable row is unkeyable however many times it
occurs, and multiplicity in the corpus never repairs a
missing key — is carried from DD-070-10 and stands as a
standing rule of this test, not re-opened.

**DD-074-9 — OPEN-074-3: the reproduction assertion and
POPULATION NOT REPRODUCED. (Conservative; flagged.)**
Upheld in the drafted form: gate 0.4's pinned
recomputation of the Phase-433 battery, which is this
test's claim that the population it keys is the
population Spec 070 meant, is part of the frozen
contract, and a mismatch closes the run **POPULATION
NOT REPRODUCED** with the discrepancy stated and no arm
counting.

**DD-074-10 — OPEN-074-4: DD-070-11 carried unchanged.
(Conservative; flagged.)** The recorded headline claim's
frozen dispute is closed as **POPULATION NOT KEYED**
rather than TEST UNRUNNABLE: Spec 070's own outcome
record names POPULATION NOT KEYED as its outcome class
(spec §1) and its claim-dispute closure line carries the
exact wording (spec §4.6), so the successor inherits
the predecessor's recorded disposition without
amendment. That Spec 070's precedence put POPULATION
NOT KEYED at step 0 while TEST UNRUNNABLE belongs to
the gate-0.1 kind of failure is recorded in the draft
(spec §7) and does not change the carried disposition.

**DD-074-11 — OPEN-074-5: an own OSF registration.**
A new OSF registration is filed for this freeze at the
freeze act, as Spec 070 filed its own; the record is
`osf-spec-registration.md` in this directory.

**DD-074-12 — OPEN-074-6: Phase 440.** The highest
phase on the merged record at the freeze act is
Phase-439 (Spec 040). Graph and experiment modules
exist only to Phase-438 (Spec 040 is frozen, not yet
executed), so allocation rests on the frozen record,
not on module filenames: the run this freeze freezes
is **Phase 440**.

**DD-074-13 — the AEE gate reading.** The gate reading
of the predecessor line (DD-038-10 via DD-070-14)
governs: zero correctness failure modes and no claim
below the 0.70 threshold pass the freeze gate; the
engine's "iterate" word following from FR-2.3
draft-cap records alone does not block the freeze. The
gate passed in that form over register 0.7-draft
(aee/freeze-aee-note.md).

*— adjudication record §8, the freeze rulings,
2026-10-24. This section is append-only from here.*

## 9. Addendum — 2026-10-25 (red-team finding RT-19): the S-B sensitivity is vacuous, and a standing rule for future asset rebuilds

Recorded by dated append; §§1–8 above are unchanged and no
ruling, verdict, or frozen text is altered by this addendum.

**The vacuity.** The frozen sensitivity arm S-B (the primary
arm rerun without the unicorn sign(s)) is recorded in the
execution record as not applicable: no Asset A v2 verbatim
label identifies a unicorn (outcome.md: S-B is not applicable
— "no Asset A v2 verbatim label identifies a unicorn"; the
step-0 unicorn naming scan at gate 0.5 returns no sign).
Spec 069's attestation had recorded a "unicorn" verbatim
label, but Asset A v2's rebuilt table never carried that
label into its columns, so the arm could never run on the
repaired surface: it is vacuous by construction, not by
measurement. The drafting record (§6 above) had already
noted that nothing at drafting turned on the unicorn's label
under Asset A v2 and that S-B's not-applicable branch was
carried; the red-team finding (RT-19, 2026-10-24/25) is
that a frozen sensitivity which structurally cannot execute
should have been caught at Spec 073's asset build or at
this spec's freeze, rather than only disclosed in the
results. That criticism stands. The outcome does not turn
on S-B: the verdict rests on the primary arm and is stated
with its containment in the outcome record, and the other
sensitivity arms (S-A, S-C) ran as frozen.

**Standing rule (adopted by this addendum).** At any future
asset rebuild — any new version of the depicted-kind asset
or of any classification table a frozen sensitivity names —
the build must assert, before freeze, that every frozen
sensitivity label exists in the new table's vocabulary:
each label a sensitivity arm would scan for is checked
against the rebuilt table's actual labels/columns, and the
assertion's result is recorded in the build record. A label
absent from the new vocabulary is named at the build, not
discovered at execution; a sensitivity that cannot run on
the rebuilt table is dispositioned openly at that point
(carried as not-applicable by design, re-scoped, or the
arm is dropped by a recorded ruling), never frozen in a
form that can only return "not applicable."

*— adjudication record §9, addendum of 2026-10-25
(red-team finding RT-19 disposition, road-to-decipherment
plan Step 7).*
