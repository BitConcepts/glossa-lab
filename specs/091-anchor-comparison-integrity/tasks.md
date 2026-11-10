# Spec 091 — Tasks

Acceptance modes per the Autonomous Execution Doctrine: **test** (a named
automated check decides), **gate** (the Spec 086 gate / foundation check /
CI decides), **human-as-oracle** (a named human reads a named artifact and
rules). Every task carries the *This does not establish* line that must
survive into its stage report.

## Stage 0 — Package adoption

- [x] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (commission-and-grounding record, T002
  assessment + note) committed as `specs/091-anchor-comparison-integrity/`
  on `docs/091-wave1-draft`, opened as a draft PR for ratification.
  Claims: package-level. Acceptance: **test** (the package verification
  of record: aee-claims.json parses; claims.md and aee-claims.json carry
  the same 15 claim ids; every claim has a falsifier and a DNE line; the
  grounding record's census numbers are reproducible from the repo at
  the package's base commit).
  *This does not establish:* that the package is approved — only that it
  is complete and internally consistent.
- [x] **T002 — AEE verification of the claims.** The C091 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv), exactly as
  Spec 088/089's T002: `aee validate` and `aee assess --no-ledger`,
  outcome recorded verbatim in `records/t002-note.md`, assessment of
  record `records/t002-aee-assessment.json`. Acceptance: **test** (the
  assessor ran and its outcome is recorded verbatim).
  *This does not establish:* claim quality — `iterate` is the expected
  reading for a draft bundle on one asserted source; the owner's approval
  is the human act (T003).
- [ ] **T003 — Owner block approval.** The owner ratifies the package as
  a block: spec, 15 claims, plan, and decisions D-091-1..7 (including
  the full-blind protocol D-091-2 and the dependency-gated phonotactic
  arm D-091-6). Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output, or of
  any named-human engagement — each D-091-1 engagement is its own act.
- [ ] **T004 — Adoption intake + generated-layer regeneration.** After
  T003: (a) record the pre-append gate run (gate CLI on the un-appended
  tree, ALL PASS); (b) append the C091 bundle through
  `tools/ledger/import_bundle.py --spec specs/091-anchor-comparison-integrity
  --date <adoption date>` — the only sanctioned path, never a hand-edit;
  (c) regenerate the generated layers over the grown ledger and republish
  through `tools/ledger/gated_publish.py`; (d) the bundle-reconciliation
  test passes. Claims: package-level (the spec's total ledger diff is
  this append). Acceptance: **gate** (the ledger-gate job green incl.
  the reconciliation test).
  *This does not establish:* anything about the appended claims' truth —
  only that the ledger grew by the sanctioned path and the generated
  layers match it.

## Stage 1 — Definitions and protocols (PR: feat/091-s1-definitions)

- [ ] **T101 — Eligibility-defs v1.** The extension of WP4's
  classification rules to the locator + coding records: the entry-level
  locator definition per reading field, "independently sourced" over a
  coding record, and the mechanical recomputation of the eligible set.
  Claims: C091-3 (defs side). Acceptance: **human-as-oracle** (the stage
  reviewer rules the document applies WP4's classes without redefining
  them; a redefinition returns to the owner).
  *This does not establish:* that the eligible set is non-empty, or that
  WP4's classes are the right classes — only that the recomputation is
  defined before it is run.
- [ ] **T102 — The blinding protocol filed.** The coder-facing protocol
  of D-091-2: inputs, exclusions, the filing act that ends the blind,
  the deviation rule. Claims: C091-2 (protocol side). Acceptance:
  **human-as-oracle** (the reviewer rules the filed protocol says what
  T003 ratified).
  *This does not establish:* that any coder will follow it — compliance
  is Stage 4's oracle act; this establishes the standard it is judged
  against.
- [ ] **T103 — The W2 reproduction protocol filed.** Attestation vs
  blind re-derivation per anchor; reader lineage exclusion; the outcome
  vocabulary. Claims: C091-5 (protocol side). Acceptance:
  **human-as-oracle**, same basis as T102.
  *This does not establish:* that readers exist or will be engaged —
  engagement is the owner's D-091-1 act.
- [ ] **T104 — The pass-by-default enumeration.** Every credit kind in
  the WP5 census traced to the code path in the frozen battery that
  awarded it; the register's "four pass-by-default paths" reconciled
  against the enumeration (grounding gap 2). Claims: C091-8 (enumeration
  side). Acceptance: **test** (the generated enumeration record names a
  code location and a census kind per entry; an untraced kind or path
  fails it). If the enumeration contradicts the register's count, the
  correction is filed as a register amendment in Stage 6, not edited
  into the register here.
  *This does not establish:* the corrected battery's behavior — only
  where the defaults live, which is what battery v2 must remove.
- [ ] **T105 — The checker-arm split for the 5.** Per-anchor
  determination for M042, M046, M108, M176, M342 from the R5 rule
  definitions and the full audit records: phonotactic arm,
  site-statistics arm, or both; undeterminable anchors recorded as
  phonotactic-gated (grounding gap 1). Claims: C091-10, C091-11
  (determination side). Acceptance: **test** (the determination record
  cites the rule text and record fields per anchor).
  *This does not establish:* any revalidation outcome — only which
  checker may lawfully produce one for each anchor.

## Stage 2 — W1 in-house leg: the locator pass (PR: feat/091-s2-locator-pass)

- [ ] **T201 — The locator record artifact + generator.** A new
  versioned artifact beside the frozen provenance file: per entry, per
  reading field, a locator or a documented not-found; entries referenced
  by sign id. Claims: C091-1 (artifact side), C091-13. Acceptance:
  **test** (schema + census-shape tests on fixtures; the generator
  refuses an entry filed with neither outcome).
  *This does not establish:* that the searches behind not-found outcomes
  were adequate — adequacy is sampled under T202.
- [ ] **T202 — The locator pass executed.** The full pass over all 184
  entries as a run under run-defs v1, cited by run id in the stage
  record; sampled locators verified against the cited source text.
  Claims: C091-1. Acceptance: **test** (the record's census is 184/184;
  the sample verification passes) + **human-as-oracle** on the sample's
  not-found searches (the reviewer rules the documented searches were
  real searches of the named sources).
  *This does not establish:* eligibility — located readings still need
  independent coding (T401) before any class moves.

## Stage 3 — W3 in-house legs (PRs: feat/091-s3-battery-v2, feat/091-s3-single-line)

- [ ] **T301 — Battery v2, no pass-by-default.** A new versioned battery
  (the historical script frozen, D-091-4) with every path enumerated in
  T104 removed; per removed path, a fixture in which the historical
  battery awarded credit and v2 returns not-run/fail. Claims: C091-8.
  Acceptance: **test** (the fixture battery, all paths) + **gate**
  (foundation check over the battery's code landing).
  *This does not establish:* that v2's genuine checks are well-calibrated
  — only that its credits are earned by checks that ran over present
  inputs.
- [ ] **T302 — The re-run over the 28 + dispositions.** One run under
  run-defs v1 over the WP5 Phase-48 subset's 28; dispositions filed as
  reclassification acts per the run's output; the historical output
  retired as evidence for all 28 in the same motion. Claims: C091-9,
  C091-13. Acceptance: **test** (dispositions recomputed from the run
  record match the filed acts exactly) + **gate** (foundation check
  passes over the touched anchor data).
  *This does not establish:* independent support for any promotion that
  survives — a battery promotion is an internal validation event.
- [ ] **T303 — The 5's runnable arms; the gated arm recorded.** The
  site-statistics-arm revalidations of T105's split, as runs, with
  dispositions per the checkers' outputs; the phonotactic-arm anchors
  recorded at requires-revalidation with the GR-088-04 dependency named,
  in the same motion. Claims: C091-10, C091-11, C091-13. Acceptance:
  **test** (dispositions recomputed from the run records match) +
  **gate** (foundation check).
  *This does not establish:* a phonotactic verdict in either direction,
  or that the gated anchors are permanently blocked — only that they
  wait, named, on a named dependency.

## Stage 4 — The independence legs (PRs: feat/091-s4-coding, feat/091-s4-readers, feat/091-s4-sourcing)

Each leg starts only on the owner's D-091-1 act for that leg (named
humans engaged). A leg with no act does not start and is reported
not-started at Stage 6 — never carried as silently pending.

- [ ] **T401 — W1 independent coding.** The engaged coder codes the
  located readings under T102's protocol; the coding record + the
  protocol-compliance record filed. Claims: C091-2. Acceptance:
  **human-as-oracle** (the owner or his reviewer rules the filed
  protocol was the executed protocol) + **test** (the coding record
  covers every located entry or names why not).
  *This does not establish:* that the coding is correct — only that it
  is independent evidence, produced blind by a named outside coder.
- [ ] **T402 — W2 outside reproduction over the 46.** The engaged
  readers execute T103's protocol; per-anchor outcomes filed, census
  46/46. Claims: C091-5. Acceptance: **human-as-oracle** (protocol
  compliance) + **test** (the census and outcome vocabulary validate
  over the filed records).
  *This does not establish:* that any anchor's class changes — classes
  move at Stage 5's recomputation, and only on landed lines (C091-6).
- [ ] **T403 — W3 candidate-3 sourcing for the 4.** The documented
  sourcing attempt for M087, M165, M264, M311 outside the crosswalk
  lineage; landed lines filed, or the search record that grounds the
  structural outcome. Claims: C091-12. Acceptance: **human-as-oracle**
  (the reviewer rules the attempt adequate: the named sources were
  actually searched).
  *This does not establish:* that no outside source exists anywhere —
  only that the documented search of the named sources found none,
  which is the register falsifier's own standard for "structural."

## Stage 5 — Dispositions: recomputation + audit v2 (PR: feat/091-s5-dispositions)

- [ ] **T501 — The recomputations.** The eligible set recomputed under
  eligibility-defs v1 from the T202 + T401 records; W2's support classes
  recomputed from T402's filed lines; both as runs under run-defs v1.
  Claims: C091-3, C091-6. Acceptance: **test** (an independent
  recomputation in the stage's tests reproduces both results exactly).
  *This does not establish:* new evidence — this is arithmetic over
  earlier records, and its whole virtue is reproducibility.
- [ ] **T502 — Audit v2.** The new versioned anchor-support audit,
  generated from the named inputs (WP5 audit, T302/T303 acts, T501
  recomputations), every disposition change carrying its act and
  producing run id; frozen records byte-untouched. Claims: C091-13.
  Acceptance: **gate** (foundation check passes; any generated layer the
  counts feed republishes through gated publication) + **test** (audit
  v2's census reproduces from its named inputs).
  *This does not establish:* that audit v2 is the final word — it is the
  current word, with the same amendment discipline as v1.
- [ ] **T503 — The citation consequences.** Per workstream as its
  dispositions land (D-091-5): crosswalk citations carry eligibility
  classes (C091-4); the 46 cited as internal-only and the supported mass
  stated as measured (C091-7) — through gated publication; any
  preprint/site text change is the owner's own approval act on the
  actual text. Claims: C091-4, C091-7. Acceptance: **gate** (gated
  publication's own checks over the republished layers).
  *This does not establish:* that every historical document is rewritten
  — historical records stand; the obligation binds published current
  layers.

## Stage 6 — Register amendment + closeout (PR: feat/091-s6-closeout)

- [ ] **T601 — The register amendment.** GR-088-01/02/03 amended
  append-only to their measured end states (closed / structural / open
  with the blocking fact named), including the T104 count correction if
  one is owed. Claims: C091-14. Acceptance: **human-as-oracle** (the
  owner ratifies the amendment).
  *This does not establish:* that the gaps are gone — only that the
  register now states, per entry, what the wave measured and what
  remains.
- [ ] **T602 — The closeout record.** Per-claim dispositions C091-1..15
  at stage-evidence strength with stage/PR pointers; the final counts
  (eligible set; supported mass; the 37's end dispositions); every
  unlanded leg and dependency named (the phonotactic arm; any
  not-started Stage 4 leg); the spec's "does not establish" summary.
  Claims: all. Acceptance: **gate** (CI green on the closeout PR; the
  closeout and the register amendment agree with audit v2's census).
  *This does not establish:* that the program's anchor support is strong
  — the closeout reports the measured state, whatever it is.
