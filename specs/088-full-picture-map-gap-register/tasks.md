# Spec 088 — Tasks

Acceptance modes per the Autonomous Execution Doctrine: **test** (a named
automated check decides), **gate** (the Spec 086 gate / CI decides),
**human-as-oracle** (a named human reads a named artifact and rules).
Every task carries the *This does not establish* line that must survive
into its stage report.

## Stage 0 — Package adoption

- [ ] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (adoption record, taxonomy v0 draft, scan
  plan, T002 assessment + note) committed as
  `specs/088-program-map-gap-register/` on `feat/088-spec-package`.
  Claims: package-level. Acceptance: **test** (the package verification
  of record: aee-claims.json parses; claims.md and aee-claims.json carry
  the same 19 claim ids; every claim has a falsifier and a DNE line; the
  taxonomy draft's assignment table counts to the spec-tree census, 88).
  *This does not establish:* that the package is approved — only that it
  is complete and internally consistent.
- [ ] **T002 — AEE verification of the claims.** The C088 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv), exactly as
  Spec 087's T002: `aee validate` → `valid: 19 claim(s)`; `aee assess
  --no-ledger` → **outcome: iterate** (80 failure modes; draft cap and
  stage cap binding by construction). Assessment of record:
  `records/t002-aee-assessment.json`; commands and verbatim outcome:
  `records/t002-note.md`. Acceptance: **test** (the assessor ran and its
  outcome is recorded verbatim).
  *This does not establish:* claim quality — `iterate` is the expected
  reading for a draft bundle on one asserted source; the owner's approval
  is the human act (T003).
- [x] **T003 — Owner block approval.** The owner ratifies the package as
  a block: spec, 19 claims, plan, the taxonomy v0 draft
  (`records/taxonomy-v0-draft.md`), and decisions D-088-1..6 (including
  the derivation table's judgment rows and the empty in_flight
  population). Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output — each
  lands on its own evidence; and the register is ratified separately at
  T603.
  **Completed 2026-11-04:** ratified as a block by Tristen Pierson by
  option tap in the Glossa-Lab chat ("Ratify the package as a block") —
  spec, 19 claims, plan, taxonomy v0 draft (incl. its two judgment
  calls), and D-088-1..6 as recommended, including the derivation
  table's judgment rows (partially_supported → open) and the empty
  in_flight population. Record:
  `records/ratification-2026-11-04.md`.
- [x] **T004 — Adoption intake + generated-layer regeneration.** After
  T003: (a) record the pre-append gate run (gate CLI on the un-appended
  tree, ALL PASS); (b) append the C088 bundle through
  `tools/ledger/import_bundle.py --spec specs/088-program-map-gap-register
  --date <adoption date>` — the only sanctioned path, never a hand-edit;
  (c) regenerate the matrix and map over the grown ledger and republish
  through `tools/ledger/gated_publish.py`, recording the gate output;
  (d) the bundle-reconciliation test passes (ledger bundle population ==
  bundles on disk). Claims: C088-15. Acceptance: **gate** (the
  ledger-gate job green incl. the reconciliation test; the ledger diff is
  exactly the append).
  *This does not establish:* anything about the appended claims' truth —
  only that the ledger grew by the sanctioned path and the generated
  layers match it.
  **Completed 2026-11-04:** (a) pre-append gate run recorded (full
  20 PASS / 0 FAIL / 1 NOT-RUN; --regen 23 PASS / 0 FAIL / 0 NOT-RUN);
  (b) intake via `tools/ledger/import_bundle.py --spec
  specs/088-full-picture-map-gap-register --date 2026-11-04` — 19
  appended, 0 already canonical, 0 refusals; ledger 888 →
  907 lines, SHA-256 `f988ed61…` → `9f8144c3…`, append-only
  byte-verified; validator PASS (876 claims, bundle 853/853 falsifier
  coverage); (c) matrix + map regenerated and republished through the
  gated route (gate of record: full 20 PASS / 0 FAIL / 1 NOT-RUN,
  --regen 23 PASS / 0 FAIL / 0 NOT-RUN), with the settling chain
  refresh executed per the Spec 087 adoption precedent (canonicals
  6/6 reproduce before the pin refresh; T405 records re-run, result
  blocks byte-equal; comparison re-filed, per_claim_divergences []);
  (d) `test_p2_reconciliation` passes in the targeted batch (108
  tests, six ledger/gate files, all passing). Record:
  `records/ratification-2026-11-04.md`.

## Stage 1 — Definitions, taxonomy, builder core (PR: feat/088-s1-defs-builder)

- [x] **T101 — program-map-defs v1 registered.**
  `glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md`: closed input list;
  reclassification-chain resolution; the status→class derivation table
  (D-088-3); standing-text template; study membership rule; roll-up
  precedence incl. the judgment-call rule; find kinds; coverage block;
  stamp contents; in_flight registered with no rule. Claims: C088-3,
  C088-4, C088-18 (defs side). Acceptance: **human-as-oracle** (the owner
  settled the judgment rows at T003; the stage reviewer rules the
  document says exactly what T003 approved — any deviation returns to the
  owner).
  *This does not establish:* that the derivation semantics are right —
  only that they are the ratified ones, registered where amendments must
  go.
  **Completed 2026-11-04:** `PROGRAM-MAP-DEFINITIONS.md` filed as
  written, incl. the membership clarification recorded as departure (a)
  in `records/stage-s1-record.md` (membership = the source-of-record
  spec; the draft's "any sources[]" phrasing would double-count 44
  claims — the fork is named in the record for the stage review).
- [x] **T102 — program-map-taxonomy v1 filed.** The taxonomy JSON per
  `records/taxonomy-v0-draft.md`: declared domains/subdomains, the 88
  study assignments, the extracted-claim document assignments, the
  restricted list (Spec 072). No standing/status field exists in the
  format. Claims: C088-9, C088-17, C088-19 (format side). Acceptance:
  **test** (schema check: every spec directory assigned exactly once;
  every domain/subdomain declared; no standing-shaped key anywhere in
  the file).
  *This does not establish:* that the groupings are the best ones — only
  that they are total, singular, and carry no standings.
  **Completed 2026-11-04:** filed with **89** study assignments (the
  ratified 88 + Spec 088's own directory, per the draft's advance
  record; coverage is over the live tree) and 7 extracted-document
  assignments; verified set-equal against the live tree and ledger at
  filing, and continuously by the conformance test.
- [x] **T103 — Pure builder + CLI.** `program_map_generate.py` (pure;
  reads only the defs' inputs) + `tools/map/generate_program_map.py` with
  `--check` (builds without writing; byte-identity or a named refusal).
  Fail-closed on: coverage gaps/duplicates, unknown ids, undeclared
  domains/subdomains, unregistered status strings, in-flight emission,
  unresolvable citations. Claims: C088-1, C088-2, C088-6 (build side),
  C088-13. Acceptance: **test** (builder test module incl. the seeded
  failure cases of T104; `--check` on a clean tree exits 0 and writes
  nothing).
  *This does not establish:* that the outputs over the real ledger are
  correct — that is T104's census and S3's independent route.
  **Completed 2026-11-04:** builder + CLI as written (CLI at the plan's
  `tools/map/` path). One anticipation: T303's registered-writer line
  for this module was pulled forward — without it the V9 census fails
  the gate from the moment the builder exists; departure (d) in
  `records/stage-s1-record.md`.
- [x] **T104 — Builder teeth + first-build census.** Tests: derivation
  table per status; roll-up per rule incl. judgment call; dropped-id,
  duplicated-assignment, unknown-id, unregistered-status fixtures all
  fail; two builds byte-identical. Then a first real build reproduces the
  census of record (857 claim nodes / 88 study nodes / 28 unjudged),
  recomputed from the inputs at test time. Claims: C088-1, C088-2,
  C088-13. Acceptance: **test**.
  *This does not establish:* coverage of inputs nobody has built yet —
  the census binds to today's ledger and tree, and moves with them under
  the same rules.
  **Completed 2026-11-04:** 30 targeted tests green (25 builder teeth +
  5 conformance); the first real build's census, recomputed from the
  live post-adoption inputs per this task's own instruction, is **876
  claim nodes / 89 study nodes / 28 unjudged** (the 857/88 figures above
  predate the T004 intake — departure (b) in the stage record).
  Determinism: two CLI runs byte-identical (hashes in the stage
  record); `--check` clean on the produced artifacts in the scratch
  verification root — the committed artifacts themselves land at T201,
  per the plan's staging.

## Stage 2 — Standing derivation (PR: feat/088-s2-derivation)

- [ ] **T201 — First committed artifacts.** `program-map.json` +
  `program-map-finds.json` generated over the live ledger and taxonomy
  v1 and committed. Claims: C088-3, C088-5, C088-6. Acceptance: **test**
  (`--check` exits 0 on the committed artifacts).
  *This does not establish:* that the standings are true — only that they
  are the defs' outputs over the current ledger.
- [ ] **T202 — Derivation census in the stage record.** Per-domain counts
  quoted from the coverage block; the judgment-call list with member
  counts; the unjudged list; falsifier coverage as recomputed (expected
  848/857; the 9 extracted nulls enumerated in the find list). Claims:
  C088-4, C088-5, C088-14. Acceptance: **test** (every number in the
  record is the coverage block's or the find list's, matched 1:1 by a
  checker or a named reviewer reading both).
  *This does not establish:* a health verdict for any domain — counts by
  class are counts, and there is no cross-domain aggregate (C088-14).
- [ ] **T203 — Determinism proof.** Delete the artifacts, regenerate,
  byte-compare; hashes recorded in the stage record. Claims: C088-13.
  Acceptance: **test** (byte-identity across the delete-and-regenerate
  cycle, twice).
  *This does not establish:* determinism under changed inputs — only that
  the build is a pure function of the inputs it declares.

## Stage 3 — Gate extension (PR: feat/088-s3-gate-v10)

- [ ] **T301 — Gate class V10.** `ledger_gate.py` gains V10
  (program-map equivalence) with the gate's own registered copies of
  program-map-defs v1 (not imported from the builder): recompute the map
  by an independent route; check artifact byte-equality, exact coverage,
  citation resolution, stamp freshness against the current ledger, and
  find-list equality. Claims: C088-7. Acceptance: **gate** (the gate CLI
  over the real tree reports ALL PASS with V10 in the per-class list).
  *This does not establish:* that the derivation is correct — two routes
  agreeing is consistency; the defs' semantics were the owner's call at
  T003/T101.
- [ ] **T302 — V10 teeth.** Seeded-divergence tests on tmp copies: a
  mutated program-map.json fails V10 and the report names it; a
  builder-vs-gate defs divergence fails; a stale stamp fails; a dropped
  node fails. Claims: C088-7. Acceptance: **test** (each seeded case
  fails the gate for the stated reason).
  *This does not establish:* that no unseeded divergence can pass — only
  that the named failure modes are caught, which is what teeth means.
- [ ] **T303 — V9 registration for the map artifacts.**
  `program_map_generate` joins the registered-writer list; the map
  artifact paths join the artifact patterns, so unregistered writes to
  them are gate failures. Claims: C088-7, C088-1. Acceptance: **gate**
  (gate suite green incl. a negative case: an unregistered-path write
  pattern is refused).
  *This does not establish:* protection against a writer added by a
  future amendment — amendments are acts, reviewed as such.

## Stage 4 — The page (PR: feat/088-s4-page)

- [ ] **T401 — Page rendering in the builder.** `program-map.html`: data
  embedded verbatim; collapsible domains/subdomains; class chips; filters
  and search over generated fields only; stamp + per-domain counts in the
  header; restricted studies name-only. The gate's V10 artifact list is
  amended in the same PR to include the page (defs discipline; recorded
  in the stage record). Claims: C088-8, C088-14, C088-19. Acceptance:
  **test** (conformance: page bytes regenerate identically; a source scan
  shows no standing logic beyond filtering/searching generated fields).
  *This does not establish:* that the page reads well — that is T402's
  rendered evidence and the reader's judgment.
- [ ] **T402 — Playwright render verification.** The generated page
  rendered at desktop (1440×900) and mobile (390×844); screenshots kept
  with the stage record; checked: sections collapse, filters change the
  visible set correctly, search narrows to generated-field matches,
  counts match the coverage block, the restricted node shows no standing.
  Claims: C088-8. Acceptance: **human-as-oracle** (a named reviewer rules
  on the screenshots against the design points; per the standing rule,
  source checks alone never support a verified claim about a page).
  *This does not establish:* usability for every reader or device — two
  widths and the named checks are the evidence, no more.
- [ ] **T403 — Publication through the gate.** The page + JSON + finds
  republished via `gated_publish.py`; the stage record cites the V10 gate
  output over these artifacts. Claims: C088-16. Acceptance: **gate**
  (ALL PASS incl. V10, quoted in the stage record).
  *This does not establish:* that publishing was wise — only that C1's
  order was kept: the verification existed before the surface did.

## Stage 5 — Gap scans (PRs: feat/088-s5a / s5b / s5c)

- [ ] **T501 — Cluster A scan: corpus + anchors.** Domains: Sign
  inventory & corpus; Anchors & readings. Inputs: find list + coverage
  block for those domains; pre-answered legs per the scan plan (incl.
  the falsifier census). Output: `records/scan-corpus-anchors.md`,
  four-kind finds only, every candidate falsifier-carrying and typed
  (C088-12). Claims: C088-10, C088-12. Acceptance: **human-as-oracle**
  (classification review) + **test** (template conformance: kinds,
  falsifiers, types present on every line that needs them).
  *This does not establish:* that these are all the gaps in those domains
  — only that every find recorded is in the registered shape.
- [ ] **T502 — Cluster B scan: claim families + contact zone.** Domains:
  Claim families by study line; Contact zone & external corpora.
  Pre-answered legs: WP5 census (6/46/37/3/2), WP4 (0 of 184), WP2/WP3
  blockers. Output: `records/scan-families-contact.md`. Claims: C088-10,
  C088-12. Acceptance: **human-as-oracle** + **test** (as T501).
  *This does not establish:* that thin evidence means wrong — the census
  counts support classes; what they mean is the register's judgment,
  reviewed by the owner at T603.
- [ ] **T503 — Cluster C scan: infrastructure + bookkeeping.** Domain:
  Program infrastructure, plus cross-cutting bookkeeping (the adoption
  record's §4 items: llms.txt staleness, desktop-clone sync, data-lineage
  question; the missing-directory finds for spec numbers 049 and 085).
  Output: `records/scan-infra-bookkeeping.md`. Claims: C088-10.
  Acceptance: **human-as-oracle** + **test** (as T501).
  *This does not establish:* that infrastructure gaps matter less — the
  register ranks; the scan only records.
- [ ] **T504 — Scan consolidation check.** Every find in the three scan
  records is exactly one of the four kinds; every candidate has a
  falsifier and an honesty-rule type; every find-list item from S2 is
  consumed by a scan or explicitly carried to S6. Claims: C088-10.
  Acceptance: **test** (the mechanical pass over the three records +
  find list).
  *This does not establish:* scan quality — shape only; quality is the
  oracle's and, finally, the owner's at ratification.

## Stage 6 — Gap register v1 (PR: feat/088-s6-register)

- [ ] **T601 — Register v1 drafted.** `glossa-indus/map/gap-register.md`
  in RCPH's format: ranked headline list; `GR-088-NN` entries with status
  words; each entry names the missing node/edge, why its absence blocks
  convergence, the candidate with its falsifier and type, and owner
  gates; closing owner-decisions section; ratification block. Claims:
  C088-11, C088-12. Acceptance: **human-as-oracle** (drafting review
  against the scan records: every scan find is in an entry or
  dispositioned).
  *This does not establish:* the ranking — ranking is judgment, and the
  owner's ratification (T603) is where it settles.
- [ ] **T602 — Completeness check against the source lists.** The
  source-coverage annex: every C088-11 source-list item mapped to entry
  id(s) or a recorded not-a-gap disposition. Mechanical legs (find-list
  items, the 28 unjudged studies, the 9 null-falsifier claims) checked by
  script; prose legs (GAP-C07, GAP-C12 remnant, WP2/WP3/WP5 items, Spec
  086 residuals, T201) checked against the annex by a named reviewer.
  Claims: C088-11. Acceptance: **test** (mechanical legs) +
  **human-as-oracle** (prose legs, reading the annex).
  *This does not establish:* completeness in nature — only completeness
  against the program's own named lists, which is the claim.
- [ ] **T603 — Owner block ratification of register v1.** The owner
  ratifies the register as a block (entries, ranking, dispositions, and
  the owner-decisions section). This act ends the spec; first waves are
  commissioned separately, from the ratified register, by a later owner
  act. Claims: C088-11. Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* that any register entry's candidate will
  succeed — only that the program's gap picture is now the ratified one
  work is commissioned from.

## Closeout

- [ ] **T701 — Closeout record.** Per-claim dispositions for C088-1..19
  (discharged / carried, with the evidence pointer for each); the final
  census quoted from the coverage block; the register's entry count and
  ratification reference; the explicit statement that no wave is
  commissioned by this spec and no claim's standing was changed by it.
  Acceptance: **human-as-oracle** (the stage reviewer against the stage
  records).
  *This does not establish:* program health — it establishes that the
  spec's own claims were each answered with evidence, which is the only
  closeout a spec can honestly give.
