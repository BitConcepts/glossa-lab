# AEE recovery — Spec 038 register (after_specify)

Register: `specs/038-pred-2026-007-full-population/claims.json`
(F038-C01…C14). The hooks ran at the freeze act
(the owner's freeze-and-execute order of
2026-10-20), the gate the draft deliberately
deferred (DD-038-7). All passes were computed
under **aee 1.5.0** — the first freeze gate in
this programme run under the 1.5 engine — by the
engine's own CLI code path run in-process (this
VM's write restriction blocks the CLI's file
outputs; `aee/freeze-aee-note.md` records the
environment and the lenient loading). Recovery
follows the Spec 035/036 pattern: atomic
rewrites, enumerations carried into boundaries
verbatim-in-substance, pairwise boundary
confirmations completed in both claims of a
flagged pair. Propositions, falsifiers, and
verdict rules are unchanged throughout.

## Round 1 — 2026-10-20T22:40:23Z — iterate (24 failure modes)

Artifact: `aee-after_specify-20261020T224023Z.json`
(11 claims below the 0.70 threshold; every
claim's propagated score 0.695 or 0.8445).
Register 0.5-draft as drafted.

- **Irreducibility (9):** C02, C03, C04, C07,
  C10, C11, C12, C13, C14 — texts carried
  second propositions, enumerations, or
  conditions.
- **Counterexample challenge (1):** C05 —
  absolute language ("never edited") without a
  bounded domain (category
  assumption_unvalidated, severity high).
- **Draft-cap records (14):** one per claim
  (FR-2.3) — structural, see the gate reading
  below.
- **Scores:** the 11 claims below threshold sat
  at 0.695. Two aee 1.5.0 mechanics produce
  that figure: single-source claims carry
  independence 0.5, and every claim carried
  the FR-8.6 freshness penalty of 0.100,
  because no evidence item recorded an
  `observed_at` date and unknown freshness
  counts as stale.

**Recovery (register 0.5-draft → 0.6-draft).**
The nine flagged texts were restated as single
atomic propositions; enumerations and second
conditions were carried into the boundaries
verbatim-in-substance (the verdict mapping
into C02's boundary, the step-0 order and its
closure consequence into C04's, the coverage
rule's operative sentences into C07's, the
never-edited clause into C10's, the
scored-as-recorded clause into C11's, the
draft-stage triple into C13's). C05's text was
domain-bounded ("Under Spec 038, …") in place
of the unbounded absolute. Every evidence item
gained `observed_at` "2026-10-20" — the date
the draft's verification record
(`adjudication.md` §2) records the evidence was
verified first-hand. That is a factual
completion of the register in the engine's
native field, not a content change: refs,
kinds, directions, source qualities, and
descriptions are untouched, and the freshness
penalty it lifts was an artefact of the
unrecorded date, not of the evidence.

## Round 2 — 2026-10-20T22:40:34Z — iterate (20 failure modes)

Artifact: `aee-after_specify-20261020T224034Z.json`
(0 claims below the 0.70 threshold; minimum
propagated score 0.795).

- **Irreducibility (5):** C02 (the verbatim
  criterion's own colon and "or"), C05 (the
  two limbs joined by "and"), C12 (two "that"
  clauses), C13 (the compound subject
  "membership and size"), C14 (the two limbs
  joined by "and").
- **Negation conflict (1):** C04↔C14 — C04's
  boundary confirmation already spoke to the
  pair; C14's did not.
- **Draft-cap records (14).**

**Recovery (register 0.6-draft → 0.7-draft).**
The five still-flagged texts were shortened to
their head propositions, the carried clauses
moving into the boundaries verbatim-in-substance
(the registered criterion's verbatim sentence
into C02's boundary, where the claim's evidence
and spec §0.1 also carry it; the not-edited
clause into C05's; the clustering limb into
C12's; the size limb into C13's; the
not-a-verdict clause into C14's). C14's
pairwise boundary confirmation was extended to
the C04–C14 pair, so the confirmation stands in
both claims of the pair.

## Round 3 — 2026-10-20T22:41:01Z — gate met (14 failure modes, all structural)

Artifact: `aee-after_specify-20261020T224101Z.json`
(0 claims below the 0.70 threshold; minimum
propagated score 0.795). The only failure
records are the 14 FR-2.3 draft-cap records.
The recovered register then met the gate at
after_plan
(`aee-after_plan-20261020T224112Z.json`) and
after_tasks
(`aee-after_tasks-20261020T224122Z.json`) at the
first pass each, with their evaluator
counterparts — the same profile: 0 correctness
failure modes, 0 claims below threshold, the
14 draft-cap records alone. The register is
frozen in this form (0.7-draft); the freeze
digest covers it.

## The gate reading under aee 1.5.0 (DD-038-10)

Under aee 1.5.0 the engine's outcome word for
these passes is "iterate", for one stated
reason: FR-2.3 caps a bundle containing
draft-status claims at iterate, and R1.4
reserves "pass" to bundles whose claims stand
at stage explained or beyond. These claims
carry status draft and stand at stage created —
the state of every governed register at freeze
time in this programme (the frozen registers of
Specs 026–036 carry draft claims throughout;
statuses and lifecycle stages move at
evaluation, not at freeze, and no stage is
fabricated at a freeze act). The gate was
therefore applied in its substantive form —
zero correctness failure modes and zero claims
below the 0.70 threshold at all three lifecycle
phases — the form every prior freeze in this
programme was judged by, with the caps
disclosed rather than edited away. The freeze
adjudication records this reading as DD-038-10
(`adjudication.md` §6).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
