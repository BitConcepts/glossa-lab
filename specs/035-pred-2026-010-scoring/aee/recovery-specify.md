# AEE recovery — Spec 035 register (after_specify)

Register: `specs/035-pred-2026-010-scoring/claims.json`
(F035-C01…C15). The hooks ran at the freeze act
(the owner's freeze-and-execute order of
2026-10-20), the gate the draft deliberately
deferred (tasks.md L3/L5). Recovery follows the
Spec 029/030/031/032/033/034 pattern: atomic
rewrites, enumerations carried into boundaries
verbatim-in-substance, pairwise boundary
confirmations for every flagged pair.
Propositions, falsifiers, and verdict rules are
unchanged throughout. The passes were computed
by the pinned AEE engine (1.0.4) in-process —
this VM's write restriction blocks the CLI's
file outputs; see `freeze-aee-note.md`.

## Round 1 — 2026-10-20T12:09:31Z — iterate (30 failure modes)

Artifact: `aee-after_specify-20261020T120931Z.json`
(0 claims below the 0.70 threshold; minimum
confidence 0.845). Register 0.5-draft as drafted.

- **Irreducibility (15):** every claim
  (C01–C15) — texts carried second propositions,
  enumerations, or conditions.
- **Negation conflict (15):** C02↔C04, C02↔C11,
  C02↔C12, C03↔C04, C03↔C05, C03↔C12, C04↔C06,
  C04↔C08, C04↔C10, C05↔C08, C08↔C09, C08↔C12,
  C09↔C10, C10↔C11, C10↔C12.

**Recovery (register 0.5-draft → 0.6-draft).**
Texts rewritten as short single propositions;
the enumerations and second conditions were
carried into the boundaries verbatim-in-substance
(the four pins into C05's boundary, the
start-rate definition into C10's, the table's
columns into C12's, the register-handling
clauses into C14's). Pairwise boundary
confirmations were added in both claims of every
flagged pair, stating the two claims' different
objects and their consistency by construction.

## Round 2 — 2026-10-20T12:12:03Z — iterate (9 failure modes)

Artifact: `aee-after_specify-20261020T121203Z.json`.

- **Irreducibility (7):** C03, C04, C06, C07,
  C08, C12, C15 — their boundaries still carried
  detail beyond scope (derivation facts, API
  read-back fields, the draft-stage observation
  in full).
- **Negation conflict (2):** C04↔C09, C08↔C09.

**Recovery (register 0.6-draft → 0.7-draft).**
The still-flagged claims' boundaries were
trimmed to scope and exclusions (the detail
stands in the claims' evidence, the spec, and
the derivation record; C09's boundary keeps the
draft-stage observation in one sentence, the
form its falsification test cites). Three texts
(C04, C06, C12) were shortened to single
propositions. Both-claims confirmations were
added for the C04–C09 and C08–C09 pairs.

## Round 3 — 2026-10-20T12:13:11Z — iterate (8 failure modes)

Artifact: `aee-after_specify-20261020T121311Z.json`.

- **Irreducibility (5):** C03 (the set's commas),
  C06 ("and"), C07 (a comma), C08 ("and" in the
  two-pool phrase), C15 (a comma).
- **Negation conflict (3):** C04↔C09, C08↔C09,
  C11↔C12 (a new pairing from round 2's C12
  text).

**Recovery (register 0.7-draft → 0.8-draft).**
The seven flagged texts were restated as single
propositions without compound markers, keeping
each proposition whole (C03's set stands in its
boundary and evidence in punctuated form; C08's
text takes the short form and its boundary
takes up the two-pool relation in its first
sentence). The flagged pairs were separated by
truthful phrasing: overlaps removed (C08–C09,
C11–C12) and C04's own gating negation made
explicit, aligning its polarity with C09's.

## Round 4 — 2026-10-20T12:14:31Z — pass (0 failure modes)

Artifact: `aee-after_specify-20261020T121431Z.json`
(0 claims below the 0.70 threshold; minimum
confidence 0.845). Register 0.8-draft.

The recovered register then passed at
after_plan (`aee-after_plan-20261020T121443Z.json`)
and after_tasks
(`aee-after_tasks-20261020T121452Z.json`) at the
first pass each, with their evaluator
counterparts. The register is frozen in this
form; the freeze digest covers it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
