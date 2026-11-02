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

---

## T403–T404 — the engine and the oracle test

### What was built

- `backend/glossa_lab/settling.py` — the settling engine.
  Pure builders plus thin write wrappers, mirroring the
  matrix generator's architecture (harmonization adoption
  3, item 5): `evaluate_candidate` / `run_record` /
  `compare_runs` / `build_assignment_sets` compute records
  in memory and write nothing; `write_assignment_sets` and
  `write_run_record` are the only writers, reached through
  the command. The module imports no intake/write entry
  point — it reads the ledger through `ledger_intake`'s
  read path only — and carries its own registered copies of
  the glossa-settle-1 constants (strict rule, outcome table,
  frame prefixes, tally keys); a test pins those copies
  equal to the gate's.
- `tools/ledger/run_settling.py` — the thin command:
  `materialize-sets`, `run`, `compare`, `verify-canonicals`.
- `glossa-indus/ledger/assignment-sets.json` — the
  assignment sets of record, materialized from the
  canonical anchors register at its pinned hash
  (26,287 bytes, sha256
  36bce404db20792826e7ffba220857c71d058423c8f8e47fca7aa900af27c5be;
  regeneration over the unchanged register is
  byte-identical): **incumbent 94 assignments** (the
  recomputed strict set read as assignments),
  **full-register 286 assignments** (every record of the
  mahadevan frame). Registered reading, carried from the
  registration record: tasks.md T403's "(287)" counts the
  register's records; the register holds 287 records, of
  which H003 belongs to a frame the anchors file does not
  name (UNMEASURED, SETTLING-SEMANTICS.md §2) and is out of
  v1 scope — the artifact counts it in
  `out_of_frame_records`, assigned by no set, never
  silently dropped.
- Run records are **not** published artifacts in v1's
  design and none are committed by this PR: a run writes
  its record only into the run store
  (`glossa-indus/ledger/runs/`, created on first use), and
  the canonical reproduction lives in the T404 test and in
  gate V8. T405 owns the first executed, stored dual run.

### Engine discipline (as registered, as built)

- Strictness is recomputed under the recorded D-A rule,
  never trusted from stored flags; `load_state` refuses
  when the recomputation disagrees with the stored
  `strict_set` flags, when the recorded strict count
  disagrees, or when the anchors file records a different
  rule id (semantics §1). Pinned in every run-record
  header: the ledger canonical hash + line count, the
  anchors register's raw-byte sha256 + byte/record/strict
  counts + rule id and version, the Phase-108 register's
  canonical hash, and the corpus snapshot's canonical
  hash (carried, per §7's dual-run protocol; settling does
  not read the corpus in v1).
- Sign identity is by (frame, number) — glossa-settle-1's
  rule, resolving mahadevan:64 → M064. The registered
  divergence from matrix-defs v1 R4's literal key
  construction stands as recorded at registration; the
  engine amends neither matrix-defs, the matrix, nor the
  semantics.
- S-R2 runs in its registered determinate v1 form and is
  value-independent; every run record carries the
  statement (`s_r2_value_independence`). S-R3 reports the
  determinate zero with `class_table: null` (UNMEASURED,
  §10). Confidences are carried verbatim from the register
  records into every context record.
- A candidate assigning one sign twice (by identity,
  padding included) is refused as malformed; a comparison
  whose two run records disagree on semantics version or
  on the ledger or corpus pins is refused (§7, C086-15's
  registered falsifier).
- Out-of-scope candidate assignments (§3) are enumerated
  on the run record at envelope level
  (`out_of_scope_assignments`), outside the S-R4 result
  block, whose field set stays exactly the registered one
  the canonicals pin.

### T404 — oracle reproduction (verbatim)

Filed at `records/stage-4-canonical-output.txt`: the
command's `verify-canonicals` output —

```
PASS null-over-subset
PASS incumbent-over-subset
PASS full-register-over-subset
PASS seeded-conflict-over-subset
PASS untouched-sign
PASS incumbent-vs-full-register-over-subset
  expectations note: absence clause reproduced exactly; the registered note's remainder is brief-specific prose (FINDING-S4-1, stage record)
verify-canonicals: 6/6 registered canonicals reproduce
```

— and the T404 test file's run: **13 passed**. All five
scenarios reproduce field-for-field; the comparison
reproduces on every mechanical field. One registered field
is not wholly mechanical — see FINDING-S4-1.

### FINDING-S4-1 — the comparison's expectations note is
### not fully derivable

The canonical comparison's expected
`pre_registered_expectations_note` reads: "No
pre-registered expectation exists in the program's record
for the one touched claim; Spec 074's outcome record
concerns yadav_2009_arxiv_manual_002, touched by neither
run." The first clause is the absence statement semantics
§7 requires, and it is mechanically derivable: no
expectations register exists in v1's record, so the
comparison states the absence for the touched claim(s).
The second clause is prose from the T405 brief (which
names Spec 074's outcome record as the expectation to
check); no registered rule derives *which* untouched
claim's record to name — an exhaustive census of
outcome-carrying claims would name dozens. The engine
therefore takes expectations (and, where a caller carries
one, an expectations note) as comparison **input data**,
generates the absence statement itself, and the T404 test
and gate V8 both assert the generated clause equals the
registered note's first clause verbatim and record the
remainder as registered prose. Nothing in the canonical
artifact was edited; the engine was not bent to
regurgitate the clause. If the program wants the clause
mechanical, the route is a registered expectations
register in a future semantics version — an owner's oracle
call, not this PR's.

### Tally-key reading (an engine defect found and fixed in
### the open, per T404's rule)

The engine's first oracle run mismatched on exactly one
thing: the S-R2 tally keys. The first build keyed tallies
by the matrix's cell relation values (supports / opposes /
constrains); SETTLING-SEMANTICS.md §5 registers the tally
keys as `supporting`, `opposing`, `constraining` (and the
canonicals carry them). The engine was fixed to the
registration; the canonicals were not touched. Recorded
here because T404's acceptance is that mismatches are
fixed in the open.

### Gate V8 (T404's wiring)

`backend/glossa_lab/ledger_gate.py` gains V8 in three
checks, in the Stage 3 idiom — the gate recomputes by its
own route from its own registered copies of glossa-settle-1
(`SETTLE_*` constants, `_gate_settle`, `_gate_compare`),
never importing the engine:

1. **Scenarios reproduce** — the canonical artifact's
   provenance pins are verified against the tree first
   (ledger canonical hash + lines; anchors raw-byte
   sha256; corpus canonical hash; strict rule id; stored
   vs recomputed strict set; source-hash verification of
   the records S-R2 reads). A pin failure FAILs naming the
   pin. Then each scenario is settled by the gate's route
   and divergences are named by scenario and field path.
2. **The registered comparison reproduces** — same
   treatment; the expectations note is checked per
   FINDING-S4-1 (absence clause verbatim; remainder named
   as brief-specific prose in the check's evidence).
3. **Scenario/verdict separation** — every settling/
   scenario module under `backend/glossa_lab` is audited
   for imports of **and reachability to** a ledger write
   entry point: attribute uses (`li.append_entry(...)`)
   and bare name references count, extending V9.2's
   import-only audit rather than duplicating it. Where
   the canonical artifact is present but no settling
   module exists, the arm FAILs (the layer the canonicals
   govern is missing); where the settling layer is absent
   from a tree entirely, all three V8 checks enumerate
   NOT-RUN with the absent inputs named.

The gate's header now states the settling semantics
version and the canonical path on every run. The CLI's
PR-scope map gains V8 for the ledger and anchors layers,
and `backend/glossa_lab/settling.py` joins the machinery
list (an engine change runs the full gate).

Gate output, verbatim: `records/stage-4-gate-output.txt`
(full: **16 PASS / 0 FAIL / 4 NOT-RUN, RESULT PASS**) and
`records/stage-4-regen-output.txt` (--regen: **18 PASS /
0 FAIL / 4 NOT-RUN, RESULT PASS**). The remaining NOT-RUNs
are the Stage 5 map legs (V2 map leg, V5, V6 map leg) and
V7 in non-regen mode. V8 was the last NOT-RUN besides the
map legs; it now PASSes on the clean tree.

### Teeth (each seeded in a scratch copy; the real tree
### untouched)

- Canonical flip: incumbent `consistent` 2→3 in the
  scratch canonical copy → V8 FAILs, naming scenario
  `incumbent-over-subset` and field `consistent`.
- Reachability seed: a scratch settling module importing
  only the intake module and calling `li.append_entry(...)`
  → V9.2's import audit PASSes it; V8's separation arm
  FAILs, naming the module and `append_entry` (the
  extension, proven distinct).
- Import seed: a scratch settling module importing
  `write_ledger` directly → V8's separation arm FAILs,
  naming the module.
- Engine refusals (`test_settling_canonical.py`): a
  duplicate assignment by identity (mahadevan:70 and
  mahadevan:070); a flipped stored strict flag in a
  scratch anchors copy; a comparison over two ledger
  builds.
- Store discipline (T403's acceptance): the pure builders
  write nothing (tree hashes identical across an
  evaluation); `write_run_record` adds exactly one file,
  under the run store, and changes no other hash;
  evaluation is byte-deterministic across runs.
- The live V9 pass: with the real engine in the tree,
  V9.2's audit scans 1 settling module and PASSes — the
  audit armed at Stage 3 over a then-absent layer now has
  its live subject.

### Local checks

- Spec 086 family (gate battery incl. the V8 teeth, the
  canonical tests, intake, migration, matrix): **107
  passed**. Freeze family: green inside the full
  enumeration below.
- Full backend suite, no `-x`, enumerated in five chunks
  (2,273 tests): **2,205 passed / 67 skipped / 1 failed** —
  the one failure is the known environmental baseline,
  `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
  (it needs a download this environment lacks; it fails
  identically on main). In-tree rewrites the suite causes
  (the evidence-API tests' extracted-claims rewrites and
  two report files) were restored before committing;
  `git status` at commit time shows only this PR's files.
- Ledger validator: **PASS**. Gate full + --regen: PASS
  (above).

### CI repair addendum (2026-11-01, post-push)

PR #483's first CI run (41359909760) failed the three
Shell wrappers jobs (macOS / Ubuntu / Windows) at the
step "shell.sh lint — backend passes ruff". The defect
class is unused-import / unused-variable hygiene in the
two files this PR introduced. Running the invocation
shell.sh defines (`ruff check backend/`, config from
backend/pyproject.toml; run with the CI venv's python,
as this clone carries no backend/venv for shell.sh to
resolve) surfaced five findings, each verified unused
by grep before removal:

- F401 `dataclasses.field` imported but unused —
  settling.py:66 (the finding quoted from the CI log);
  `field` is never called or referenced in the module.
- F841 `scope_ids` assigned but never used —
  settling.py:486 (a pure comprehension; the evaluator
  recomputes the intersection inline).
- F841 `assignments` assigned but never used —
  settling.py:639; the `_validate_candidate(candidate)`
  call is kept as a bare call, preserving its validation
  side effect.
- F401 `shutil` imported but unused —
  test_settling_canonical.py:52.
- F401 `glossa_lab.ledger_intake` imported but unused —
  test_settling_canonical.py:58.

Scope note, stated plainly: the repair brief named
settling.py plus this record as the commit set. The two
test-file findings are the same defect class in the
PR's other new file and block the same lint step, so
they were fixed in the same motion rather than left to
fail the next run; no other file was touched.

Local lint proof after the fix (verbatim):

```text
$ python -m ruff check backend/
All checks passed!
```

(exit 0). Re-runs on the repaired tree:
test_settling_canonical.py **13 passed**; the ledger
gate in full mode **16 PASS / 0 FAIL / 4 NOT-RUN,
RESULT: PASS** (the same counts as at the PR head);
the remaining Spec 086 family files (ledger gate,
intake, migration, matrix) **67 passed**. The test
runs left no in-tree rewrites to restore — `git status`
shows only the two repaired files plus this record.

The same CI run's Backend job failure is a different
animal: the teardown ERROR on
`test_copy_api_token_without_tkinter_is_named`
(sqlite3 "Cannot operate on a closed database" exiting
the conftest TestClient) — the known tray teardown
flake, fourth sighting (cf. PR #477 run 41319020208
attempt 1). It is remedied by rerun at the parent's
gate, not by this change; nothing in this repair
touches it.

### Claim assessments (engine scope only)

- **C086-13 (canonical cases reproduce exactly)** —
  SUPPORTED at engine scope: every registered scenario and
  the comparison's mechanical content reproduce exactly,
  in the T404 test and under the gate's independent route
  (V8). The one registered field not reproduced verbatim
  is the comparison note's brief-specific remainder —
  FINDING-S4-1, named above, not silently matched.
- **C086-14 (settling is mechanical, labeled, and
  read-only against the ledger)** — SUPPORTED at engine
  scope: the engine computes run records mechanically from
  pinned inputs; every run record and the assignment sets
  carry the verbatim glossa-settle-1 label; the engine
  imports no write path, writes only run records into the
  run store, and the gate's V9 audit passes over it live.
  The Experiment Builder surface leg is T406's, still open.
- **C086-16** — its T403 leg is established (a run creates
  only run records; the store-hash diff across a run is
  empty outside the run store, tested). The claim as a
  whole also carries T405/T406 legs and is not closed here.
- C086-15 (the dual run) is T405's and is **not** executed
  by this PR: the registered comparison remains its
  expectation, now with an engine and a gate that both
  reproduce it.

### Still open in Stage 4

T405 (first interchangeability run, executed and stored),
T406 (Experiment Builder stub disposition), T407 (stage
closeout — its canonical-reproduction leg is filed here;
the dual-run leg lands with T405).

## Cleanup determination (T403–T404)

The clone (`~/workspace/glossa-run/spec086-stage4-engine`)
is kept on the PR branch with a clean tree apart from the
PR's own files, as the seat discipline requires, for the
parent's merge motion. One full-suite run was lost to a
VM replacement mid-flight (its log sat in /tmp); the
suite was re-run in five chunks with logs in durable
storage (`~/workspace/glossa-run/stage4-suite-logs/`,
outside the repo, retained as this stage's working
record). The smoke-test run records written during
development were removed; the run store does not exist in
the committed tree. No background processes, containers,
worktrees, or venvs were created by this worker. No branch
was merged or deleted by this worker; main was not
touched.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.

---

## T405–T407 — the first interchangeability run, the stub's disposition, stage closeout

Date: 2026-11-01. Branch: `feat/086-stage4-closeout`
(off main `b0528198`, the Stage 4 engine merge). This
section closes Stage 4: T405 executes and stores the
first dual run, T406 disposes of the Experiment Builder
constraint-projection stub, and T407 files the closeout
artifacts. Standing position, unchanged: **the Indus
script is not deciphered**; everything below is
computation over ledgered relations under
glossa-settle-1, labeled as such.

### T405 — the first interchangeability run (executed and stored)

**Protocol (semantics §7).** Both runs were executed
through the engine's command
(`tools/ledger/run_settling.py run`) over the **same
ledger build and the same corpus snapshot**, over the
**same scope**: the full mahadevan frame inventory —
286 signs, in the register's own order (the
full-register assignment set's sign order). Scenario
ids: `t405-incumbent-over-full-frame` and
`t405-full-register-over-full-frame`. Before running,
the assignment sets of record were regenerated in
memory and compared: byte-identical to the committed
`assignment-sets.json` (sha256 `36bce404…`), so both
candidates are exactly the sets of record — incumbent
94 assignments, full-register 286, H003 the one
out-of-frame record, assigned by neither.

**The two runs (headline numbers, from the stored
records).**

| | incumbent | full-register |
|---|---|---|
| scope signs | 286 | 286 |
| assigned | 94 (share 0.3287) | 286 (share 1.0) |
| contexts touched | 94 | 286 |
| strict contexts | 94 | 94 |
| consistent | 94 | 94 |
| non-strict contexts | 0 | 192 |
| conflicts | 0 | 0 |
| strict agreement share | 1.0 | 1.0 |
| contexted share | 1.0 | 1.0 |
| uncontexted assignments | 0 | 0 |
| claims touched | 1 | 1 |
| forced | 0 | 0 |
| out-of-scope assignments | 0 | 0 |

Both candidates assign every sign its own recorded
reading, so zero conflicts and full strict agreement
are the mechanical consequence of what the sets of
record *are* — reported as computed, not as a result
about the script. The runs diverge in coverage only:
the full-register run adds 192 non-strict contexts and
no claim's tallies move (below).

**Pins (T405's test acceptance: input hashes equal
across the run records).** Both records carry,
identically: ledger canonical sha256
`c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf`
(871 lines); anchors register raw-byte sha256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
(287 records, 94 strict, rule `strict_sa_independent_hm`);
Phase-108 register sha256 `2b04fed4…`; corpus snapshot
sha256 `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`;
semantics `glossa-settle-1`. The comparison route
itself refuses on any pin disagreement; none occurred.

**Stored run records (the run store's first records).**

| record | bytes | sha256 |
|---|---|---|
| `glossa-indus/ledger/runs/t405-incumbent-over-full-frame--b262d06655a4.json` | 37,957 | `45cde1d3ff19df193953d84e812810b18ebfe674879d6fbba81db4a0a85826ea` |
| `glossa-indus/ledger/runs/t405-full-register-over-full-frame--e0892157556b.json` | 87,209 | `2c483f0d0eb9b962e6d46bd374d7ebcc62ca05a6af9282fccf5c3171a2e0b5fd` |

**The comparison and the per-claim divergence list.**
Produced by the engine's `compare` route over the two
stored records and filed verbatim at
`records/stage-4-dual-run-comparison.json` (6,296
bytes, sha256
`ae83e71b6153c4ffde7caa75f7a8a3160a9f95e7f62e367f85f63bd19c74e2c8`
— the filed copy is byte-identical to the command's
output). Its decisive content:

- Claims compared: exactly one — the ledger's only
  sign_refs-bearing claim,
  `parpola_2010_dravidian_solution_manual_002`. The
  incumbent touches it via `mahadevan:70`; the
  full-register run via all three stored refs
  (`mahadevan:72`, `mahadevan:64`, `mahadevan:70`).
  Its tallies are 0 supporting / 0 opposing /
  0 constraining under **both** runs (it carries no
  governing outcome blocks; falsifiers 1 present /
  0 evaluable), so it is compared and **not
  divergent**.
- `per_claim_divergences`: **empty**. The divergence
  list is the coverage deltas: assigned 94 → 286,
  contexts 94 → 286, strict contexts 94 → 94,
  consistent 94 → 94, conflicts 0 → 0, forced 0 → 0;
  signs assigned by one candidate only: 192 by
  full-register, 0 by incumbent.
- The S-R2 value-independence registered at T401 is
  what this shape means: tallies move only when a
  newly assigned sign newly *touches* a claim, and
  the one touchable claim was already touched by the
  incumbent. A fuller divergence awaits a ledger whose
  claims carry per-sign references in more than one
  place — the record's true state, stated, not a
  defect of the run.

**Pre-registered expectations — derived afresh, with
a correction to FINDING-S4-1's prose.** Per
FINDING-S4-1's method, expectations are comparison
input data taken from the record; the census was
re-derived for this run by the engine's own S-R2
route (governing outcome blocks over every claim's
records of record). The record carries 13 governing
(claim, study) pairs: Spec 047 → the
indus_valley…manual_001 claim (INCONCLUSIVE);
Spec 051 → indus_valley…manual_003 (INCONCLUSIVE);
Spec 052 → four claims (INCONSISTENT ×4: farmer…,
indus_valley…critique_0001, indus_valley…critique_0002,
without_kings…language_0001); Spec 054 →
`yadav_2009_arxiv_manual_002` (NOT SUPPORTED,
governing block dated 2026-10-25, 2 blocks);
Spec 055 → ancient_writing…sign_val_0001
(NOT NUMERAL-LIKE); Spec 056 → archaeology…
sign_val_0001 (IDENTIFICATION FAILED); Spec 063 →
the same claim (RECOVERED); Spec 046 →
archaeology…sign_val_0002 (IDENTIFICATION FAILED);
Spec 064 → the same claim (IDENTIFICATION FAILED);
and **Spec 074 → `without_kings_or_conquests_the_
indus_scr_ce9d98cc_manual_003` (NOT SUPPORTED, dated
2026-10-24, pointer `…#spec074_outcome_append_
2026_10_24`)**.

Two dispositions follow. (1) **No expectation concerns
a touched claim**: none of the 13 claims carries
sign_refs, and the one touched claim carries no
governing outcome block at all — so the comparison
was executed with an empty expectations input and the
engine generated its absence statement itself, which
stands verbatim in the filed comparison: *"No
pre-registered expectation exists in the program's
record for the one touched claim."* C086-15's
falsifier leg (a touched claim with an expectation the
report neither names nor scores) is not met: there is
no such claim. (2) **Correction, in the open:**
FINDING-S4-1's prose remainder (in the T403–T404
section above) names Spec 074's outcome record as
concerning `yadav_2009_arxiv_manual_002`. The census
shows that attribution is wrong: Spec 074's outcome
record concerns the without-kings (Hunt) manual_003
claim — as this program's own PR #477 record also
states — and the yadav claim's governing record is
Spec **054**'s. FINDING-S4-1 had already flagged its
second clause as brief-specific prose rather than
derivation; the clause's substance (no expectation
exists for the touched claim) is unaffected, and the
registration record above is not edited — the
correction stands here, where the afresh derivation
was made.

*This does not establish either reading — it
establishes exactly where they diverge, claim by
claim, which is the thing narration cannot do.*
(tasks.md T405, carried verbatim.)

### The T404 store test's precondition, adapted in the open

`test_evaluation_writes_nothing` (T404) asserted the
run store was empty before and after a pure
evaluation — a scaffold from when no stored runs
existed. T405 by design populates the store, so the
assertion's precondition is false on any tree carrying
this task's own output. The test is adapted in this
PR: the two store-emptiness assertions are removed
and the purity assertion — no hash anywhere under
`glossa-indus/ledger` changes across an evaluation,
the populated run store included — stands as the
test's whole content, which is T403's acceptance
stated more strongly, not a loosening. No canonical
expectation was touched; the companion test
(`test_a_run_writes_only_its_run_record`, changed-set
== exactly one new run-store path) passes unmodified
against the populated store.

### T406 — the stub's disposition: removed from the palette, with a pointer

**What the stub was.** `_cas_hypothesis_projector` in
`backend/glossa_lab/experiment_graph_phase14.py` — the
Experiment Builder node function for
`CASHypothesisProjector`, which projected a corpus's
measured degrees of freedom through a CAS-YAML
constraint model via the CPSC IterativeEngine /
CellularEngine and returned `max_violation` with a
per-constraint breakdown. Its history in git: the node
arrived with Phase-14 (49b0cf69); the CPSC module was
deleted for IP contamination (b96b7fbd); the owner
then removed the CAS-YAML UI/API and the node's
AtomicNodeDef registration (60faf1c3, 2026-05-21,
"all CAS nodes errored on every run — dead UI"); the
stub function was re-added in the final IP sweep
(57139e3a) as a tombstone returning
`{"error": "Constraint projection engine not
available.", "success": False, "max_violation": 1e9}`
to any caller.

**State found.** The node is already absent from the
palette: `_phase14_node_defs()` registers 14 nodes,
none of them the projector; the function is not in the
module's `__all__`, is called from nowhere in backend
or frontend, and the frontend carries no reference to
it. Its downstream consumer, LanguageDetectorVerdict,
takes `cas_projection` as an *optional* input and
scores nothing when it is absent. What remained was
exactly two things: an error-returning orphan function
one re-registration away from being a trap again, and
the stub error string in the codebase path (Spec 085
T017's acceptance names its absence).

**Decision: removal with a pointer** (the disposition
Spec 085 C085-15 and Spec 086 T406 both offer second),
on these grounds:

1. **The node's contract presupposes machinery that
   does not exist and must not be resurrected.** Its
   inputs are measured DoF values plus a CAS-YAML
   model; its engine was a continuous constraint
   projector deleted deliberately, in part for IP
   contamination. glossa-settle-1 consumes sign→value
   assignment sets against anchor records and computes
   enumerated contexts, conflicts, and tallies; it has
   no DoF projection, no YAML model, and no
   `max_violation`. Wiring the node to it would require
   inventing a mapping from settling outputs to the
   dead contract's fields — new semantics invented to
   fit a removed engine, barred by the semantics'
   amendment discipline (§12: a rule change is a new
   registered version, derived first) and by this
   task's own decision rule.
2. **There is no settling service surface to wire to.**
   In v1's registered design the engine's surfaces are
   the library, its command, and the gate (T403
   record: run records are not published artifacts; no
   API route exists). A graph node calling the library
   would still need the invented contract of ground 1.
3. **The palette absence is already the lived state**
   (since 2026-05-21) and no rendered surface changes:
   removing an unregistered backend function touches
   no UI. The wireframe gate is therefore not
   triggered by this disposition; had the disposition
   altered a rendered surface, this task would have
   stopped instead, per its brief.

**The change.** The stub function is deleted; at its
site a pointer comment names the capability's
successor (the glossa-settle-1 settling engine —
`backend/glossa_lab/settling.py`, operated via
`tools/ledger/run_settling.py`) and records that no
Builder node projects constraints in v1 and that the
consumer's optional input has no in-tree producer.
The consumer itself is untouched — its input is
optional, inert unconnected, and editing another
node's contract was not this task's to do.
`backend/tests/test_spec086_stub_disposition.py`
(5 tests) pins the disposition: the stub error string
is absent from the codebase path (the backend package
source; it survives only in records quoting the audit
— Spec 086 spec.md's current-state text and the new
test's own constant — which are not an invocable
path); the stub symbol and node are absent, the
palette enumerated in full via `ATOMIC_NODES`; the
pointer's target is real (the settling module and its
command); and the consumer returns well-formed
verdicts unfed and fed a well-formed projection-shaped
input (C085-15's second falsifier leg).

*This does not establish experiment authors should
settle inside pipelines — only that the named
capability is no longer a trap.* (tasks.md T406,
carried verbatim; the same sentence Spec 085 T017
carried.)

### T407 — closeout filings

Filed in `specs/086-winning-combination-adoption/records/`:

- `stage-4-closeout-canonical-output.txt` — the
  canonical reproduction regenerated fresh on this
  tree: `verify-canonicals` 6/6 PASS, and the T404
  test file **13 passed**.
- `stage-4-dual-run-comparison.json` — the first
  dual-run divergence list, verbatim engine output
  (above; sha256 `ae83e71b…`).
- The two run records themselves — stored in the run
  store (T405 table above) and cited there; T407's
  "filed verbatim" is satisfied by the stored
  artifacts plus the verbatim comparison filing.
- `stage-4-closeout-gate-output.txt` and
  `stage-4-closeout-regen-output.txt` — the gate on
  this tree: full **16 PASS / 0 FAIL / 4 NOT-RUN,
  RESULT PASS**; --regen **18 PASS / 0 FAIL /
  4 NOT-RUN, RESULT PASS**. The counts hold at the
  engine PR's exactly: the stored run records enter
  no check's inputs (V8's inputs are the canonicals;
  the run store is an output the gate does not read),
  and the phase14 removal touches no gated artifact.

### Local checks (this PR's tree)

- Ruff (`python -m ruff check backend/`, the CI
  shell-wrapper invocation): **All checks passed!**
- Ledger validator: **PASS** (falsifier coverage
  831 of 840 claim entries; errors: none).
- Gate: full 16 PASS, --regen 18 PASS (above).
- Spec 086 + settling families (the six subject
  files: ledger gate, ledger intake, ledger
  migration, matrix, stub disposition, settling
  canonical): **85 passed**; under `-k "spec086 or
  settling"` across the whole suite: 85 passed,
  1 skipped (an OpenCV-availability skip in
  test_sign_images.py, matched by the -k filter).
  Freeze family (`-k freeze`): **263 passed,
  1 skipped** — the established count.
- Full backend enumeration without `-x`, five chunks
  over 214 test files (2,279 tests): **2,210 passed /
  67 skipped / 1 failed / 1 error**. The failure is
  the known environmental baseline,
  `test_phase133_stage0_inventory.py::
  test_builder_recomputation_skips_without_inputs`
  (needs a download this environment lacks; fails
  identically on main). The error is a one-off
  suite-interaction ERROR in
  `test_notifications_api.py::
  test_mask_email_redacts_local_part` (chunk 1 of 5),
  not reproduced standalone (1 passed), in-file
  (9 passed), or in the chunk's API-file subset
  (75 passed); it is not the tray teardown test, its
  error text was not captured beyond the summary
  line, and this PR touches no notifications code —
  recorded as an unclassified one-off, with the three
  green re-runs as its evidence. The tray teardown
  flake did not appear in this enumeration.
- In-tree rewrites the suite caused (the evidence-API
  family's extracted-claims rewrites: 10 files under
  `glossa-indus/claims/extracted_claims/`, one claim
  report, `outputs/partial_loop_result.json`) were
  restored before committing; `git status` at commit
  time shows only this PR's files.

### Claim assessments (closeout scope)

- **C086-13 (canonical cases reproduce exactly)** —
  SUPPORTED, unchanged from engine scope; the
  closeout adds this tree's fresh reproduction filing.
  FINDING-S4-1's named exception (the comparison
  note's brief-specific remainder) stands exactly as
  recorded at T404.
- **C086-14 (settling is mechanical, labeled, and
  read-only against the ledger)** — SUPPORTED at
  closeout scope. The Experiment Builder leg left open
  at engine scope is closed by T406: the Builder
  surface no longer carries a node that returns the
  "engine removed" error; it carries a pointer to the
  settling engine in the removed stub's place, pinned
  by test. The claim's falsifier legs (a reported
  settling number with no run record; a surface
  missing the label; a settling module importing a
  write path) — none is met on this tree: every number
  in this section traces to a stored run record or a
  filed verbatim output, and V8/V9 pass live.
- **C086-15 (interchangeability discipline)** —
  SUPPORTED. The first dual run is executed and
  stored: identical ledger and corpus pins across both
  run records (the claim's first falsifier leg —
  different input hashes — checked and absent); the
  per-claim divergence list is emitted with both
  tallies per claim (second leg — narration without
  the list — absent: the list is the filed artifact);
  for the one touched claim, no pre-registered
  expectation exists in the program's record, and the
  report says so in the engine's own generated words,
  with the record's 13 governing outcome records
  censused and named above, Spec 074's among them
  (third leg — an expectation neither named nor
  scored — absent: no touched claim carries one).
- **C086-16 (settling moves nothing)** — SUPPORTED
  at Stage 4 scope. This PR's runs created only run
  records: the tree diff attributable to settling is
  exactly the two files under
  `glossa-indus/ledger/runs/`; the store-discipline
  tests pass against the populated store. The claim's
  remaining leg — a *displayed* score differing from
  an independent ScoringEngine execution — is a
  property of the Stage 5 surface, which does not
  exist yet; the settling layer computes no displayed
  score, and the leg is carried to Stage 5 unnamed
  nowhere and dropped nowhere.

### What this stage does not establish

*This does not establish any decipherment consequence
— settling outputs are computations over ledgered
relations, labeled as such, and enter the research
record only through intake.* (tasks.md T407, carried
verbatim.) Stage 4 is closed; Stage 5 (the layered
map, wireframes first, the owner's approval by name)
is the remaining stage of Spec 086.

## Cleanup determination (T405–T407)

The clone (`~/workspace/glossa-run/spec086-stage4-closeout`)
is kept on the PR branch with a clean tree apart from
this PR's own files, as the seat discipline requires,
for the parent's merge motion. Scratch lives under
`/tmp/s086s4/` (the census script, the scope list, run
and comparison captures, suite chunk lists) — ephemeral,
outside the repo; nothing in the tree depends on it.
Chunk suite outputs live in this session's process
records; their summaries are transcribed above. No
background processes, containers, worktrees, or venvs
were created by this worker, and none are left running.
No branch was merged or deleted by this worker; main
was not touched.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
