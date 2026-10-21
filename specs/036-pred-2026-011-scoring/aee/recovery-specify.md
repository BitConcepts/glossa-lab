# AEE recovery — Spec 036 register (after_specify)

Register: `specs/036-pred-2026-011-scoring/claims.json`
(F036-C01…C15). The hooks ran at the freeze act
(the owner's do-all order of 2026-10-20), the gate
the draft deliberately deferred (tasks.md L3/L5).
Recovery follows the Spec 029/030/031/032/033/034
pattern: atomic rewrites, enumerations carried
into boundaries verbatim-in-substance, pairwise
boundary confirmations for every flagged pair.
Propositions, falsifiers, and verdict rules are
unchanged throughout (verified mechanically at
the freeze act: every claim field other than text
and boundary is identical to the draft register).
The passes were computed by the pinned AEE engine
(1.0.4) through the repo's own runner
(`run_aee.py assess`, the Glossa venv build); see
`freeze-aee-note.md`.

## Round 1 — 2026-10-20T19:57:47Z — iterate (10 failure modes)

Artifact: `aee-after_specify-20261020T195747Z.json`
(0 claims below the 0.70 threshold; minimum
confidence 0.845). Register 0.5-draft as drafted.

- **Irreducibility (6):** C03, C04, C06, C13,
  C14, C15 — texts carried second propositions,
  enumerations, or conditions.
- **Negation conflict (3):** C01↔C15, C04↔C09,
  C13↔C15.
- **Precision (1):** C08 — a term read as
  undefined or non-measurable.

**Recovery (register 0.5-draft → 0.6-draft).**
Five texts (C03, C04, C13, C14, C15) rewritten
as short single propositions; the enumerations
and second conditions were carried into the
boundaries verbatim-in-substance (the screened
set into C03's boundary, the byte-identity of
the predecessor entries into C14's, the
never-as-a-verdict clause into C15's). C06's
boundary was trimmed of its API read-back field
enumeration (the read-back stands in the claim's
evidence). C08's boundary was given the
operational definition of the conflict flag.
Pairwise boundary confirmations were added in
both claims of every flagged pair, stating the
two claims' different objects and their
consistency by construction.

## Round 2 — 2026-10-20T20:00:25Z — iterate (3 failure modes)

Artifact: `aee-after_specify-20261020T200025Z.json`.

- **Irreducibility (1):** C06 — its text still
  carried the two-predicate status form and its
  boundary still carried field detail.
- **Negation conflict (1):** C04↔C09.
- **Precision (1):** C08.

**Recovery (register 0.6-draft → 0.7-draft).**
C04's text was restated in the negation-first
form — its own gating negation made explicit,
aligning its polarity with C09's (the Spec 035
resolution of the same pair). C06's text was
restated as a single status predicate and its
boundary trimmed to the registration's identity
and verification points (the read-back stands in
`osf-registration.md` and the claim's evidence).
C08's text and boundary were restated in the
registered reading's own terms, with the mapping
file, its pin, and the operational definition of
the conflict flag carried in the boundary.

## Round 3 — 2026-10-20T20:01:42Z — iterate (1 failure mode)

Artifact: `aee-after_specify-20261020T200142Z.json`.

- **Negation conflict (1):** C03↔C04 — a new
  pairing from round 2's C04 text.

**Recovery (register 0.7-draft → 0.8-draft).**
Pairwise boundary confirmations were added in
both claims of the C03–C04 pair, stating the two
claims' different objects (the set and its
reproduction) and their consistency by
construction.

## Round 4 — 2026-10-20T20:02:20Z — iterate (1 failure mode)

Artifact: `aee-after_specify-20261020T200220Z.json`.

- **Negation conflict (1):** C03↔C04 — the pair
  persisted through the confirmations.

**Recovery (register 0.8-draft → 0.9-draft).**
The pair was separated by truthful phrasing, the
overlap removed: C03's text now states the set
itself in the unpunctuated form (the
screened-set definition stands in its boundary
and evidence), and C04's text takes the short
reproduction form (the screen step stands in its
boundary).

## Round 5 — 2026-10-20T20:03:01Z — pass (0 failure modes)

Artifact: `aee-after_specify-20261020T200301Z.json`
(0 claims below the 0.70 threshold; minimum
confidence 0.845). Register 0.9-draft.

The recovered register then passed at
after_plan (`aee-after_plan-20261020T200316Z.json`)
and after_tasks
(`aee-after_tasks-20261020T200318Z.json`) at the
first pass each, with their evaluator
counterparts. The register is frozen in this
form; the freeze digest covers it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
