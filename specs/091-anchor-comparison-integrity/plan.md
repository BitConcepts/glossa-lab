# Spec 091 — implementation plan

**Date**: 2026-11-05. **Package branch**: `docs/091-wave1-draft` (this
package; repo home on adoption: `specs/091-anchor-comparison-integrity/`).
**Proposal basis**: the owner's wave-1 commission (2026-11-05;
`records/commission-and-grounding-2026-11-05.md`), carrying the Winning
Combination build order as its design rule: definitions before
machinery, in-house legs before the independence legs that need owner
acts, dispositions only from executions, the register amended last and
only to measured states.

Build order:

**definitions + protocols → locator pass ∥ corrected battery → the
independence legs (owner-gated) → dispositions in audit v2 → register
amendment + closeout.**

W1's in-house leg (the locator pass) and W3's in-house legs (battery
v2, the site-statistics arm) run in parallel after Stage 1; neither
waits for the other, and neither waits for the named-human acts. The
independence legs (W1 coding, W2 readers, W3 candidate 3) each start
only on the owner's D-091-1 act for that leg.

## Stage 0 — package adoption (precondition for every build stage)

- The package (spec.md, claims.md, aee-claims.json, plan.md, tasks.md,
  records/) lands in the repo as `specs/091-anchor-comparison-integrity/`
  on the package branch, PR'd as a draft for ratification and merged on
  the owner's block approval.
- **T002 (done at drafting, re-verified at adoption)** — the C091 bundle
  run through the pinned assessor in the CI-faithful venv, the Spec
  088/089 invocation:

  ```
  ~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
  ~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger \
      --input aee-claims.json --output records/t002-aee-assessment.json
  ```

  The verbatim outcome is recorded in `records/t002-note.md` at
  drafting; `iterate` is the expected outcome for a draft bundle on a
  single asserted source, and the owner's approval (T003) is the human
  act. The bundle is generated from claims.md by script and its set
  identity (15 ids, in order, one falsifier each) verified mechanically
  (t002-note.md).
- **Pre-append gate check (the freeze discipline)**: before the intake
  append, the adoption PR runs the gate CLI on the un-appended tree and
  records ALL PASS, so any post-append failure is attributable to the
  append and not to drift (the Spec 088/089 adoption shape).
- **T003 — owner block approval** of spec + 15 claims + this plan +
  decisions D-091-1..7. No build task starts before it.
- **T004 — adoption intake**: the claims enter the ledger through
  `tools/ledger/import_bundle.py --spec specs/091-anchor-comparison-integrity
  --date <adoption date>` — never a hand-edit of claims.jsonl —
  followed, in the same motion, by regeneration of the generated layers
  over the grown ledger and republication through gated publication,
  exactly the Spec 088/089 adoption shape. The spec's total ledger diff
  is this append.

## Dependencies

- Spec 088 complete + register v1 ratified (2026-11-04) — the entries
  this spec executes from. Spec 089 complete (2026-11-05) — run-defs v1
  governs every execution below. Spec 086 complete — the ledger, the
  gate, gated publication. The repair brief (PR #421) complete — WP4's
  classification, WP5's audit, the v2 checkers are this spec's inputs.
- The foundation check (constitution §III / H21) must PASS after any
  change touching anchor data — it gates Stages 3, 5, and 6 landings.
- GR-088-04 (the linguist leg) is a dependency of exactly one arm (W3
  candidate 2's phonotactic arm); it is not a dependency of any stage
  as a whole, and no stage waits for it (D-091-6).
- The owner's D-091-1 acts gate Stage 4 only, per leg.

## Stage 1 — Definitions and protocols

**PR**: `feat/091-s1-definitions` → one PR (three documents + the two
determinations).

- **Eligibility-defs v1** — the extension of WP4's classification rules
  to the locator + coding records: what a located reading is
  (entry-level, per reading field), what independently sourced means
  over a coding record, and the mechanical recomputation that produces
  the eligible set (C091-3's machinery). Behavior: given the two
  records, the recomputation is a pure function — same records, same
  eligible set, on any machine. Acceptance: **human-as-oracle** (the
  stage reviewer rules the document applies WP4's classes without
  redefining them; a redefinition returns to the owner, per the
  grounding record's gap 3).
- **The blinding protocol** (D-091-2) — the coder-facing document:
  inputs (primary sources + sign list), exclusions (project readings,
  WP4 classifications, audit dispositions), the filing act that ends
  the blind, and the deviation rule (C091-2). Acceptance:
  **human-as-oracle** (ratified in substance at T003 via D-091-2; the
  reviewer rules the filed protocol says what was ratified).
- **The W2 reproduction protocol** — attestation vs blind re-derivation
  per anchor, reader lineage exclusion, outcome vocabulary (landed /
  attempted-not-landed / not-attempted-with-reason). Acceptance:
  **human-as-oracle**, same basis.
- **T104 determination — the pass-by-default enumeration.** From the
  frozen battery code + the WP5 records' `phase48_reconstruction`
  fields: the enumerated list of pass-by-default paths in the
  historical battery, reconciled against the register's "four" (the
  grounding record's gap 2). Behavior: every credit kind in the WP5
  census is traced to the code path that awarded it. Acceptance:
  **test** (the enumeration is a generated record whose every entry
  names a code location and a census kind; a kind with no path, or a
  path with no kind, fails the determination).
- **T105 determination — the checker-arm split for the 5.** From the R5
  rule definitions and the full audit records: which of M042, M046,
  M108, M176, M342 require the phonotactic checker, which the
  site-statistics checker, which both (the grounding record's gap 1).
  Acceptance: **test** (a per-anchor determination record citing the
  rule text and record fields it rests on; an anchor whose arm cannot
  be determined is recorded as undetermined and treated as
  phonotactic-gated — the conservative direction).

*This stage does not establish:* that any protocol will be followed or
any definition is right in substance — it establishes that the rules
exist in writing before the executions they govern, so deviations are
findable.

## Stage 2 — W1 in-house leg: the locator pass

**PR**: `feat/091-s2-locator-pass` → one PR (the locator record + its
generator + tests).

- The locator record (a new versioned artifact beside the frozen
  provenance file): per entry, per reading field — locator
  (primary-source citation at entry level) or not-found with the
  documented search. The pass runs as a run under run-defs v1 and is
  cited by run id. Behavior: the record's census is mechanically
  184/184 examined; an entry cannot be filed with neither outcome.
  Claims: C091-1. Acceptance: **test** (census test over the record;
  sampled entries' locators resolve to the cited source text).
- The frozen WP4 provenance file is not edited; the locator record
  references its entries by sign id (C091-13).

*This stage does not establish:* independence or eligibility — it
establishes where each reading can be found in the primary literature,
which is the input the independence test consumes.

## Stage 3 — W3 in-house legs: battery v2 + the 28, the runnable arm of the 5

**PRs**: `feat/091-s3-battery-v2` (battery + fixtures + re-run +
dispositions), then `feat/091-s3-single-line` (the 5's runnable arms).

- **Battery v2** — a new versioned battery implementing the corrected
  checks with the Stage 1 enumeration's paths removed (D-091-4).
  Behavior: every credit traces to an executed check over present
  inputs; each removed path has a fixture in which the historical
  battery awarded credit and v2 returns not-run/fail. Claims: C091-8.
  Acceptance: **test** (the fixture battery) + **gate** (the foundation
  check passes over the touched anchor data before landing).
- **The re-run over the 28** — one run under run-defs v1 over the WP5
  Phase-48 subset's 28; dispositions follow the run (C091-9), filed as
  reclassification acts feeding audit v2 (Stage 5). Acceptance:
  **test** (disposition recomputation from the run record reproduces
  the filed dispositions exactly).
- **The 5's runnable arms** — `site_stats_v2`-lineage revalidation of
  the Stage 1 split's site-statistics subset, as runs; dispositions per
  C091-10; the phonotactic subset is recorded dependency-gated per
  C091-11 in the same motion (not skipped silently). Acceptance:
  **test**, same recomputation basis.

*This stage does not establish:* independent support for anything it
promotes or revalidates — these are internal validation events, and
audit v2 records them in the internal classes unless an external line
also exists.

## Stage 4 — The independence legs (each starts on its owner act)

**PRs**: one per leg — `feat/091-s4-coding` (W1), `feat/091-s4-readers`
(W2), `feat/091-s4-sourcing` (W3 candidate 3). A leg with no owner act
does not start; the stage is complete for closeout purposes when every
leg has either landed or been recorded not-started-by-owner-act at
Stage 6 (the register amendment then states the open state; nothing is
carried as silently pending).

- **W1 independent coding** — the engaged coder codes the located
  readings under the Stage 1 blinding protocol; the coding record is
  filed with the protocol-compliance record (C091-2). Acceptance:
  **human-as-oracle** (the owner, or his reviewer, rules the filed
  protocol was the executed protocol — the one judgment machinery
  cannot make) + **test** (the coding record covers every located
  entry, or names why not).
- **W2 outside reproduction** — the engaged readers execute the Stage 1
  protocol over the 46; per-anchor outcomes filed (C091-5). Acceptance:
  **human-as-oracle** on protocol compliance + **test** on the 46/46
  census.
- **W3 candidate-3 sourcing** — the documented sourcing attempt for
  M087, M165, M264, M311 outside the crosswalk lineage; landed lines or
  the structural record (C091-12). Acceptance: **human-as-oracle** on
  the attempt's adequacy (a search that found nothing must be shown to
  have looked in the places the record names).

*This stage does not establish:* the truth of any attestation or coding
— it establishes that the external evidence exists, was produced under
the filed protocols by the named humans, and is on record.

## Stage 5 — Dispositions: recomputation + audit v2

**PR**: `feat/091-s5-dispositions` → one PR (audit v2 + its generator +
the register-facing counts).

- The eligible set recomputed from Stage 2 + Stage 4 records under
  eligibility-defs v1 (C091-3); W2's support classes recomputed from
  Stage 4's filed lines (C091-6); all dispositions — W1 classes, W2
  classes, Stage 3's revalidations — assembled into **audit v2** by its
  versioned generator, every change carrying its act and its producing
  run id (C091-13). Behavior: audit v2's every count is reproducible
  from the named inputs by re-running the generator. Acceptance:
  **gate** (foundation check + gated publication for any generated
  layer the counts feed) + **test** (an independent recomputation in
  the stage's tests reproduces audit v2's census exactly).
- The citation consequences land per workstream as its dispositions
  land (D-091-5): eligibility classes on crosswalk citations (C091-4),
  internal-only labels and the measured supported mass (C091-7) —
  through gated publication; any preprint/site text change goes through
  the owner's approval of the actual text as its own act.

*This stage does not establish:* new evidence — it is arithmetic and
bookkeeping over the earlier stages' records, and its correctness is
exactly its reproducibility.

## Stage 6 — Register amendment + closeout

**PR**: `feat/091-s6-closeout` → one PR (register amendment + closeout
record).

- GR-088-01/02/03 amended append-only to their measured end states per
  C091-14: closed, re-registered structural, or open-with-blocking-fact
  (the phonotactic arm and any not-started independence leg are named
  here in their true state). Acceptance: **human-as-oracle** (the owner
  ratifies the register amendment as he ratified the register).
- The closeout record: per-claim dispositions C091-1..15 at
  stage-evidence strength with stage/PR pointers; the final counts
  (eligible set size; supported mass; the 37's end dispositions); every
  standing departure and unlanded leg named; the spec's "does not
  establish" summary. Acceptance: **gate** (CI green on the closeout PR;
  the register amendment and the closeout agree with audit v2's census).

*This stage does not establish:* that the program's anchor support is
strong — it establishes what the wave measured, and leaves the register
telling the truth about what remains.
