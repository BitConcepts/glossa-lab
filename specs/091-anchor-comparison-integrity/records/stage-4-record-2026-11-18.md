# Spec 091 — Stage 4 record: the independence legs, not-started disposition

Stage 4 of Spec 091 (anchor-comparison integrity): tasks T401, T402,
T403. Record filed 2026-11-18 on branch `feat/091-stage4` from main
`6c89d0be8827b3d511c9b0b5cea6615b3a46be2e`.

**Disposition of the stage: no leg started.** Every Stage 4 leg is
gated on a named-human engagement that is the owner's act under
decision D-091-1, and no such act is on record for any leg. This
record files that disposition per leg, with the evidence for it, so
the legs are carried as *recorded not-started* — the state plan.md
prescribes for exactly this case — and never as silently pending.
No checkbox in tasks.md is ticked by this record: a tick asserts
execution, and no leg executed.

## 1. The governing gate

tasks.md, Stage 4 preamble: "Each leg starts only on the owner's
D-091-1 act for that leg (named humans engaged). A leg with no act
does not start and is reported not-started at Stage 6 — never
carried as silently pending."

spec.md, D-091-1: W1's independent coding, W2's external readers,
and W3 candidate 3's external sourcing "count as independent only
if the humans are outside the derivation lineage, and engaging
them is the owner's act."

spec.md, non-goals: "**No contact without the owner's act.** The
outside coder, the external readers, and candidate 3's external
sourcing are named-human engagements under the program's contact
rules; no stage initiates contact (D-091-1)."

plan.md, Stage 4: "A leg with no owner act does not start; the
stage is complete for closeout purposes when every leg has either
landed or been recorded not-started-by-owner-act at Stage 6 (the
register amendment then states the open state; nothing is carried
as silently pending)."

## 2. The search for a D-091-1 act

The following records were searched for any engagement, pick,
shortlist, or authorization naming humans for any Stage 4 leg:

- `records/ratification-2026-11-06.md` — ratifies D-091-1 with its
  recommendation (pattern (b): a shortlist prepared, contact only
  on the owner's pick) and states, of the adoption motion itself,
  that "the named-human engagements of D-091-1 remain the owner's
  acts." No human is named for any leg.
- `records/run-index.jsonl` — four entries, covering the Stage 2
  locator pass, its supplement, and the two Stage 3 runs. No
  Stage 4 run exists.
- The Stage 1, 2, and 3 records — no engagement is named in any of
  them. The Stage 1 record carries the position forward unchanged:
  "engagement is the owner's D-091-1 act."
- The program's current-state record (PROGRAM-STATE.md, maintained
  outside this repo) lists "D-091-1 independence-leg humans (the
  owner names them)" under owner-gated, open items.
- Git history (all branches, message search on the decision id and
  on engagement terms) — no engagement record for this spec.

**Finding: no D-091-1 act exists for T401, T402, or T403.** No
coder, reader, or sourcing engagement has been named, picked, or
authorized on any record available to this stage.

## 3. Per-leg dispositions

### T401 — W1 independent coding (claim C091-2): NOT STARTED

- Gate: no engaged coder. The blinding protocol (T102, filed
  Stage 1) requires a coder outside the derivation lineage
  (protocol clause P5; eligibility-defs v1 §7 excludes a coded
  value whose coder is in the lineage). This program's own
  machinery produced the project readings and their records; no
  in-house or agent substitution can satisfy the independence the
  leg exists to produce, and none was attempted.
- Inputs that exist and are ready: the located readings the coder
  would code — per the T202 artifact as amended by its supplement
  (the merge rule of `records/stage-2-supplement-delta.json`):
  phonetic 9 located / 175 not-found, semantic 0 located / 184
  not-found over the 184 crosswalk entries. The coding population
  is the 9 located phonetic fields.
- Unblocking act: the owner names and engages a coder (D-091-1
  pattern (a)), or picks from a shortlist (pattern (b)).
- *This does not establish:* that the coding is correct — only
  that it is independent evidence, produced blind by a named
  outside coder. (The task's line, carried as required; the leg
  produced no coding for it to apply to.)

### T402 — W2 outside reproduction over the 46 (claim C091-5): NOT STARTED

- Gate: no engaged readers. The reproduction protocol (T103,
  filed Stage 1) states the position in its own header: engaging
  the readers is the owner's D-091-1 act, outstanding.
- Inputs that exist and are ready: the protocol, and the
  population as the claim defines it — the WP5 audit's
  supported_internal_only class, 46 anchors.
- Unblocking act: the owner names and engages readers outside
  each anchor's derivation lineage (D-091-1).
- *This does not establish:* that any anchor's class changes —
  classes move at Stage 5's recomputation, and only on landed
  lines (C091-6). (The task's line, carried as required.)

### T403 — W3 candidate-3 sourcing for the 4 (claim C091-12): NOT STARTED

- Gate: claim C091-12 carries the dependency in its own text —
  the sourcing attempt is "(an owner act for the external
  engagement, D-091-1)". No such act is on record.
- Population and current standing: M087, M165, M264, M311, each
  resting solely on a crosswalk or literature import (rule R5d).
  After the Stage 3 dispositions (T302, T303) these four are the
  remaining requires_revalidation pool.
- No sourcing search was run under this leg. A search executed
  without the owner act would not be the documented external
  sourcing attempt the claim specifies, and its negative result
  could not lawfully ground the structural outcome (the register
  falsifier's standard is a documented search of named sources
  under the engagement, ruled adequate by the reviewer).
- Unblocking act: the owner's D-091-1 act for candidate 3's
  external sourcing.
- *This does not establish:* that no outside source exists
  anywhere — only that the documented search of the named sources
  found none, which is the register falsifier's own standard for
  "structural." (The task's line, carried as required; no search
  has yet earned its application.)

## 4. The DEDR absence blocks no Stage 4 leg

The DEDR dataset is not held (it was lost with the former desktop;
restore-by-re-derivation is an open owner decision). Within this
spec its only consumer was the Stage 3 battery's DEDR leg, filed
not_run in the T302 run record for every sign. No Stage 4 leg's
inputs include DEDR: T401 consumes the locator records, T402 the
reproduction protocol and the anchor population, T403 an external
sourcing engagement. The absence is stated here so it is not
mistaken for a silent skip: the legs' sole blocker is the missing
D-091-1 act.

## 5. What was deliberately not done

- No contact of any kind was initiated toward any coder, reader,
  or source (spec non-goal).
- No coding, reading, or sourcing was simulated, substituted, or
  performed by the program's own machinery in the legs' names.
- No reclassification acts were filed; no anchor standing changes;
  no store or anchors file was touched by this stage.
- The per-leg branches named in plan.md (`feat/091-s4-coding`,
  `feat/091-s4-readers`, `feat/091-s4-sourcing`) were not created;
  they belong to legs that start. This disposition record rides
  `feat/091-stage4`.
- tasks.md Stage 4 checkboxes are unchanged (all unticked).

## 6. Judgment named

D-091-1 as ratified adopted pattern (b) — a shortlist prepared,
contact only on the owner's pick. No shortlist artifact exists in
this spec's records, and Stage 1's task list (T101–T105) carried
no shortlist task. Whether preparing a shortlist needs a further
owner authorization is the owner's call and this record takes no
position on it. The narrower fact decides this stage under every
reading of the decision: no engagement, pick, or authorization
naming humans for any leg is on record, so no leg's start
condition is met.

## 7. Verification of the tree this record rides

This stage changes no code, no data, and no generated layer: one
record file added under `specs/091-anchor-comparison-integrity/records/`.
The standing gates and the full test suite were run on the final
tree (bare checkout configuration, the configuration CI runs),
sequentially, and are cited exactly:

- Ledger gate, full mode: **29 PASS / 0 FAIL / 1 NOT-RUN**,
  RESULT: PASS, exit 0.
- Ledger gate, --regen mode: **32 PASS / 0 FAIL / 0 NOT-RUN**,
  RESULT: PASS, exit 0.
- Ledger gate, --contamination mode: **1,025 presentations
  scanned, 0 flags**, PASS, exit 0.
- Full test suite (CI invocation and environment; the two GPU
  files ignored as CI ignores them; the one documented local
  stall nodeid, `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`,
  deselected by its plain nodeid per standing local practice, CI
  authoritative for it), in two parts split at the ledger-gate
  test file: Part A (the suite minus
  `tests/test_spec086_ledger_gate.py`) **2,960 passed / 0 failed /
  66 skipped / 1 deselected**; Part B (that file alone) **67
  passed / 0 failed**. Union: **3,027 passed / 0 failed / 66
  skipped / 1 deselected**.

One environmental note, recorded rather than smoothed over: the
suite was first run with the Holdat corpus CSVs copied into the
clone at their gitignored paths (pins `62d14d2b…`, `eb6d3b6a…`,
the setup earlier stages' runners needed). That run failed
exactly two tests — `test_promotion_integrity.py::test_coverage_reported_unavailable_not_zero`
and `test_spec095_release_gate.py::test_real_tree_anchor_and_corpus_components_pass`
— both of which are written against the corpus layer's *absence*
(the first asserts coverage is reported unavailable rather than
zero; with the layer present, coverage computed to 0.0854; the
second asserts the layer is listed absent-by-design). The copies
were removed, the suite-dirtied files restored, and the full
suite re-run bare, producing the union cited above; the collected
count is identical in both runs (3,026 + 1 deselected in Part A),
and the arithmetic reconciles exactly (the two failures became
passes; six corpus-dependent tests that ran with the layer
present skip without it). The gates were likewise re-run bare
for the citations above. The suite's known in-tree side-effect
writes (four files) were restored before this record was
committed; the committed tree carries this record and nothing
else.

## 8. Claims

No claim is discharged by this record. C091-2, C091-5, and C091-12
remain open, each gated on its D-091-1 act. The not-started status
of all three legs is the input Stage 6's closeout record (T602)
carries, per plan.md; the register amendment (T601) then states
the open state for GR-088-01, GR-088-02, and GR-088-03 with the
blocking fact named — the same fact named here.
