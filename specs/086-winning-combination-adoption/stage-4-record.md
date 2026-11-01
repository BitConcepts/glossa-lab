# Spec 086 — Stage 4 record (registration): settling semantics + hand-derived canonicals (T401–T402)

Date: 2026-11-01. Branch: `feat/086-settle-registration`
(off main `c93e2af4`, the Stage 3 merge; tasks.md names
the Stage 4 semantics PR `feat/086-settling-semantics` —
the branch name here follows the dispatching brief; the
difference is naming only). This record covers **T401
and T402 only**: the semantics registration and the
hand-derived canonicals. The engine (T403), its
exact-reproduction test and gate check V8 (T404), the
first interchangeability run as executed (T405), and the
stub's disposition (T406) are the next PR's work and
stay open below. Standing position, unchanged by
anything in this stage: **the Indus script is not
deciphered**; settling outputs are computations over
ledgered relations under registered semantics, labeled
as such, and no output of this stage is a reading or a
decipherment claim.

## What was registered

- `glossa-indus/ledger/SETTLING-SEMANTICS.md` —
  **glossa-settle-1** (T401): sign identity and frames
  (§2), candidates as data and the two assignment sets
  of record (§3), the context extraction rule (§4),
  rules S-R1–S-R4 in their registered forms (§5), the
  forced-consequence definition (§6 of the semantics),
  scenarios and the dual-run protocol (§7), confidence
  carriage (§8), the UNMEASURED register (§10 of the
  semantics), and the semantics' own falsifier (§11).
  It states expressly that the Atlas's settle-1
  constants are not lifted, and it names the layers
  distinction (computed settling outputs vs ledger
  verdicts are different layers; neither overrides the
  other) as binding.
- `glossa-indus/ledger/settling-canonical.json` —
  the canonicals (T402): five scenarios and one
  registered dual-run comparison, each with its prose
  derivation beside the expected output, in the Atlas's
  shape (inputs, derivation, expected). Provenance
  pinned at the head of the artifact: ledger canonical
  hash `c4e2326e…` (871 lines); anchors register raw
  SHA-256 `df0cf620…` (570,344 bytes; 287 records; 94
  strict = HIGH 90 + MEDIUM 4); strict rule
  `strict_sa_independent_hm` at its recorded version;
  `matrix-defs v1`; corpus snapshot `08fc96c8…`.
- A dated harmonization entry appended to
  `records/harmonization-2026-11-01.md` (see the
  harmonization section below).
- tasks.md: T401 and T402 ticked. LEDGER.md: the
  Stage 4 registration entry.

**No engine code exists in this PR, and none exists in
the tree**: `backend/glossa_lab/settling.py` does not
exist at this registration, and the gate's V9 audit
line on this tree still reports "no settling/scenario
package exists yet (Stage 4)" — the derive-before-build
order is a fact of the commit history, not an
intention.

## Registered readings (the choices that carry weight)

1. **Sign identity is by (frame, number).** The
   register keys its records `M` + zero-padded 3-digit
   number (all 287 keys match `^[A-Z]\d{3}$`, verified);
   the ledger stores refs unpadded (`mahadevan:64`).
   glossa-settle-1 resolves by number, so
   `mahadevan:64/70/72` resolve to M064/M070/M072.
   This **diverges in mechanics** from matrix-defs v1
   R4 (literal `M<n>` construction; R4 yields zero
   cells — Stage 2's recorded state of the matrix
   layer, which stands) and from the gate's V4 R4 tie
   conversion (padding kept). The divergence, its
   ground (the register's uniform key convention under
   the D-A declared schema), and its scope are recorded
   in the semantics (§2) and flagged here for the
   owner's oracle read: under the settling semantics
   the ledger's only sign refs name three real strict/
   non-strict anchors; under the matrix definitions as
   literally written they name none. Repair, if the
   owner wants one, is a matrix-defs amendment in both
   registered copies — deliberately **not** ridden in
   on this PR.
2. **S-R2 is registered in a determinate v1 form, and
   the spec sketch's value-keyed test is a named gap
   (GAP-S2), not an implementation.** Spec.md's sketch
   ("a claim whose recorded outcome or falsifier bears
   against the assigned value's reading family") is not
   mechanically determinate over the current record:
   the counter-decomposition search (semantics §10)
   found exactly one sign_refs-bearing claim in the
   whole ledger; its `proposed_value` is one prose
   string for a sign family, its falsifier a prose
   corpus-statistical condition, and it carries no
   governing outcome blocks (its one outcome-shaped
   append names Spec 072, carries no outcome string,
   and stands redacted under the Roif gate — Spec 086
   §9 name-only discipline; it was not read). S-R2 v1
   therefore enumerates touched claims and tallies only
   registered machine-readable bearings (governing
   outcome blocks under the matrix-defs v1 outcome
   table), counts falsifiers present vs evaluable (1
   vs 0 for the one touchable claim), and states its
   **value-independence** plainly: in v1 a touched
   claim's tallies depend on which signs are assigned,
   never on the values. Implementing the sketch
   literally would require judging prose — the practice
   Spec 085 retired.
3. **S-R3 is registered but inert: its class table is
   UNMEASURED.** The five-artifact search is recorded
   in semantics §10 (anchors file; `canonical_signs`
   schema — continuous rates in a live DB, not classes
   in a repo record; the Parpola-frame crosswalk CSV;
   the Soviet positional dataset — a different
   numbering tradition, self-registered
   descriptive-only; the Hunt tripartite test output).
   Every run under v1 reports
   `s_r3: {class_table: null, violations: []}` — a
   determinate zero.
4. **The forced-consequence computation collapses in
   v1, and the registration says so.** Under S-R1 the
   only signs with a unique consistent value are the
   strict-anchored ones, so forced = the strict
   register restated for the scope's unassigned signs
   (semantics §6, with the full-frame corollary: 94
   pairs). It becomes informative only when a
   registered rule couples signs. Reported as computed,
   never narrated as a discovery.
5. **Contexts are the canonical register's records —
   one per sign — and the pair-list shape is out of
   scope, on the record.** The register's field census
   (40 distinct fields over 287 records) contains no
   `pairs` field and no pair-set field of any name.
   The pair-list shape (`{cipher, target, confidence,
   note}`) exists only in the live DB's `anchor_sets`
   table — the user-built sets Spec 086 §8 (Spec 085
   Q2, answered in drafting) excludes as settling
   contexts in v1, with the canonical anchors file as
   the operative source. The semantics (§4) reconciles
   this openly and pre-registers what "pair" and
   "context" will mean if a future version settles over
   such sets. This also corrects, on the record, the
   premise the stage was dispatched under (that
   single-inscription anchor records carry pair-sets
   under their own field): in this tree they do not;
   the tree governed, per the brief's own
   derive-from-the-tree instruction.
6. **M222's registered reading is `min`, and it is
   strict.** An easy fact to get wrong from the
   program's narrative memory (the Phase-110 'kur'
   cohort story): M222's current record reads `min`
   (MEDIUM, category GRAMMAR, sa_in_chain false →
   strict). The canonicals derive from the record as
   stored, and the derivation shows the register facts
   for all four subset signs, including the two
   non-strict ones (M064 fails on `sa_in_chain: true`;
   M072 on category SA_DERIVED) — each derived from the
   Phase-108 register, and each agreeing with the
   stored `strict_set` flag and `validation_status`.
7. **Bearing tallies are 0/0/0 everywhere in the
   canonicals, and that is the record, not a gap in
   the derivation.** The only touchable claim's matrix
   row is empty and it carries no governing outcome
   blocks, so every scenario's S-R2 tallies are zero
   and the dual-run divergence list is empty (the runs
   diverge in coverage only). A canonical set that
   manufactured a non-zero tally would be inventing a
   relation the record does not carry.
8. **Share conventions are registered, not chosen per
   run**: an undefined share is null with a gloss
   ("no strict contexts touched" / "no assignments in
   scope"), never 0 or 1 by convention; assignment
   share and contexted share are separate counts, and
   the untouched-sign canonical exists to keep them
   distinct (assigned_share 1.0 with contexted_share
   0.0).

## The canonical cases (T402)

Scope for scenarios 1–4: **canonical-subset-1** =
[mahadevan:64, mahadevan:70, mahadevan:72,
mahadevan:222] — the three signs the ledger's only
sign_refs claim names, plus M222, a strict MEDIUM
anchor no claim names (selection rationale recorded in
the artifact). Each expected output below was derived
by hand from the register, the Phase-108 register, and
the claim's record; the full prose derivations stand
in `settling-canonical.json` beside the expectations.

| Scenario | Contexts | Strict ctx | Consistent | Conflicts | Claims touched | Forced |
|---|---|---|---|---|---|---|
| null-over-subset | 0 | 0 | 0 | 0 | 0 | (70, vēl), (222, min) |
| incumbent-over-subset | 2 | 2 | 2 | 0 | 1 (parpola…, via 70) | — |
| full-register-over-subset | 4 | 2 | 2 | 0 | 1 (parpola…, via 72/64/70) | — |
| seeded-conflict-over-subset | 1 | 1 | 0 | 1: (70, M070, ka ≠ vēl) | 1 (via 70) | (222, min) |
| untouched-sign (scope {417}) | 0 | 0 | 0 | 0 | 0 | — |

Plus the registered comparison
**incumbent-vs-full-register-over-subset**: identical
input pins; per-claim divergence list **empty** (the
one touched claim tallies 0/0/0 under both);
coverage deltas assigned 2→4, contexts 2→4, strict
contexts 2→2, conflicts 0→0, forced 0→0; signs
assigned by one only: mahadevan:64, mahadevan:72
(full-register only); pre-registered expectations:
**none exists for the touched claim** — Spec 074's
outcome record concerns `yadav_2009_arxiv_manual_002`,
which carries no sign_refs and is touched by neither
run; the absence is recorded in the artifact, not
omitted.

**Derivation check, disclosed.** The derivations are
hand derivations and stand as the review surface
(T402's acceptance is human-as-oracle). As a
transcription guard only, a one-off scratch script
recomputed every scenario's expected object from the
source artifacts under the registered rules and
compared it field-for-field with the registered JSON:
5 of 5 scenarios and the comparison's deltas agree.
That script is not the engine, is not in the tree, and
proves nothing about the semantics — it guards against
transcription slips between the derivations and the
artifact. The engine's independent reproduction is
T404's bar.

## UNMEASURED and gap findings

All three are registered in semantics §10 with their
search records; stated here so the stage report
carries them:

1. **S-R3 positional-class table — UNMEASURED** (no
   registered class table over the mahadevan frame
   exists in the record; S-R3 inert in v1).
2. **GAP-S2 — value-keyed claim bearing** (spec.md's
   S-R2 sketch is not mechanically determinate over
   the current record; closes when per-sign proposed
   values are intaken in identifier-bearing form).
3. **The H-prefix frame name — UNMEASURED** (the
   anchors file does not name H003's frame; nothing in
   v1 depends on it).

No canonical case had to be stopped on an
indeterminacy: every scenario above produces a
determinate expected output under the semantics as
registered (S-R2 and S-R3 enter their expectations
through their registered v1 forms — tallies from
machine-readable bearings only, and the inert-rule
zero — not through forced numbers).

## Harmonization entry (records addition)

Appended to `records/harmonization-2026-11-01.md`, a
dated entry recording the **Breaking-Point Atlas's
adoption of Glossa's falsifier-gap census pattern
note**, delivered and adopted the same day
(2026-11-01; their record:
`~/workspace/breaking-point-atlas/scenarios/PATTERN-NOTE-ADOPTION-2026-11-01-falsifier-gap-census.md`):
their mechanism already stood from their Amendment 3
build; their prospective rule binds harder than the
note requires (falsifier required and non-null at
intake, control-tested); their gap is zero (0 of 541),
so the census proves a negative; the one element they
lacked — per-population naming — was built the same
day (13 populations; check totals unchanged at 206
PASS plain / 207 with regen; a temp-copy failure-path
control moved the header to 540/541 and the HIND line
to 37/38 with the SCHEMA check failing on the named
entry; the real ledger untouched). The **named
divergence** is recorded in full: the Atlas schema
forbids null falsifiers outright while Glossa stores
legacy nulls as counted nulls — consistent today only
because the Atlas has no gap population; their recorded
forward disposition is a counted-null class by schema
amendment when a genuine gap population arrives, which
is Glossa's existing mechanism. **Glossa's
disposition: no conflict with any ratified Glossa
decision; no Glossa change follows** (our census
already names its populations: bundle 817/817,
extracted 14/23). Location of the entry:
`records/harmonization-2026-11-01.md`, final section,
"2026-11-01 — The Atlas adopted Glossa's
falsifier-gap census note".

## Local checks (this tree, before pushing)

Ledger validator (`tools/ledger/validate_ledger.py`),
tail verbatim:

```text
falsifier coverage: 831 of 840 claim entries carry a falsifier
falsifier coverage by population: bundle 817/817, extracted 14/23
does_not_establish coverage: 755 of 840 claim entries
aee_state present: 0 of 840 claim entries
errors: none
RESULT: PASS
```

Gate, full mode (`tools/ledger/check_ledger_gate.py`),
summary verbatim: **13 PASS / 0 FAIL / 5 NOT-RUN —
RESULT: PASS** (the five NOT-RUN legs are the Stage 5
map legs, V7's regen-only mode, and V8, which arrives
with the engine at T404 and is correctly still NOT-RUN
for this registration PR). The new files under
`glossa-indus/ledger/` enter the gate's PR-scope path
by its path rule; no check was loosened and no existing
artifact was modified.

Tests (CI-faithful venv): freeze family
(`-k freeze`): **263 passed, 1 skipped** — the
established count. Spec 086 family (`-k spec086`):
**62 passed, 1 skipped**. Records-only changes; no
test was touched.

## Claim assessments (T401/T402 legs only)

- **C086-13 (settling is derive-before-build)** —
  SUPPORTED at registration scope. The semantics
  (glossa-settle-1) and the hand-derived canonicals,
  with prose derivations, are registered in git in
  this PR, and no settling engine module exists in
  the tree at this registration — the claim's first
  falsifier clause (commit order showing the engine
  predating the registration) is now permanently
  unsatisfiable. The claim's second leg — every
  canonical reproduced exactly by the engine, test
  green — is T404's and stays open.
- **C086-14 (settling is mechanical, labeled, and
  read-only against the ledger)** — the contract leg
  is registered: the semantics fixes the run-record
  header pins, the verbatim label every output
  surface must carry, and the no-write-path rule the
  gate's V9 will audit. The claim itself is **not
  assessed as supported at this stage**: its
  falsifier (a reported settling number with no run
  record; a surface missing the label; a settling
  module importing a write path) becomes testable
  only when the engine exists (T403/T404).
- C086-15 and C086-16 are T403–T405 scope and are not
  assessed here; the registered comparison above is
  T405's expectation, not its execution.

## What this stage does not establish

Per tasks.md, carried with the tasks they belong to:
T401 — *the rules are the right rules* (each carries
its grounding so a reviewer can disagree in the open).
T402 — *the derivations are error-free* (they exist in
prose, where an error can be found by reading, before
any code depends on them).

## Cleanup determination

Nothing spawned remains: the clone
(`~/workspace/glossa-run/spec086-stage4-reg`) is kept,
as the seat discipline requires, for the parent's
merge motion — it carries this PR's branch and a clean
working tree apart from the PR's own files. The
derivation scratch scripts live under `/tmp/s086s4/`
(ephemeral, outside the repo; nothing in the tree
depends on them). No background processes, containers,
worktrees, or venvs were created. No branch was merged
or deleted by this worker; main was not touched.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
