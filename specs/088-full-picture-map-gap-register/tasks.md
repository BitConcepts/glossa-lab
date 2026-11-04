# Spec 088 — Tasks

Acceptance modes per the Autonomous Execution Doctrine: **test** (a named
automated check decides), **gate** (the Spec 086 gate / CI decides),
**human-as-oracle** (a named human reads a named artifact and rules).
Every task carries the *This does not establish* line that must survive
into its stage report.

## Stage 0 — Package adoption

- [x] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (adoption record, taxonomy v0 draft, scan
  plan, T002 assessment + note) committed as
  `specs/088-program-map-gap-register/` on `feat/088-spec-package`.
  Claims: package-level. Acceptance: **test** (the package verification
  of record: aee-claims.json parses; claims.md and aee-claims.json carry
  the same 19 claim ids; every claim has a falsifier and a DNE line; the
  taxonomy draft's assignment table counts to the spec-tree census, 88).
  *This does not establish:* that the package is approved — only that it
  is complete and internally consistent.
  **Completed 2026-11-04** (ticked at Stage S6; the work was
  executed at adoption): the package landed byte-identical
  under the adopted names `specs/088-full-picture-map-gap-register/`
  on `feat/088-adoption` (PR #504) — the directory/branch
  naming departure from this task's draft text is recorded
  in `records/ratification-2026-11-04.md` and named again
  as departure (c) in `records/stage-s6-record.md`. The
  package verification of record stands (19/19 claim ids
  identical across claims.md and aee-claims.json; every
  claim carries a falsifier and a DNE line).
- [x] **T002 — AEE verification of the claims.** The C088 bundle run
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
  **Completed 2026-11-04** (ticked at Stage S6; executed at
  package build): `aee validate` → `valid: 19 claim(s)`;
  `aee assess --no-ledger` → **outcome: iterate**, 80
  failure modes, recorded verbatim in `records/t002-note.md`
  with the assessment at `records/t002-aee-assessment.json`.
  **Closeout correction 2026-11-04 (T701):** the S6 stage
  recorded this completion but left the box unticked; the
  box is flipped at closeout against the evidence of record
  above. No work was re-executed.
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

- [x] **T201 — First committed artifacts.** `program-map.json` +
  `program-map-finds.json` generated over the live ledger and taxonomy
  v1 and committed. Claims: C088-3, C088-5, C088-6. Acceptance: **test**
  (`--check` exits 0 on the committed artifacts).
  *This does not establish:* that the standings are true — only that they
  are the defs' outputs over the current ledger.
  **Completed 2026-11-04:** generated by the builder CLI over the
  live inputs and committed in this stage's PR — the first committed
  landing (S1 generated in scratch only). SHA-256:
  `program-map.json` `672cfb78…` (byte-identical to the S1 scratch
  build's hash), `program-map-finds.json` `7a6cd137…`; `--check`
  exits 0 on the real root; the S1 conformance module now exercises
  check semantics against the real root
  (`test_committed_artifacts_match_fresh_build`). Record:
  `records/stage-s2-record.md`.
- [x] **T202 — Derivation census in the stage record.** Per-domain counts
  quoted from the coverage block; the judgment-call list with member
  counts; the unjudged list; falsifier coverage as recomputed (expected
  848/857; the 9 extracted nulls enumerated in the find list). Claims:
  C088-4, C088-5, C088-14. Acceptance: **test** (every number in the
  record is the coverage block's or the find list's, matched 1:1 by a
  checker or a named reviewer reading both).
  *This does not establish:* a health verdict for any domain — counts by
  class are counts, and there is no cross-domain aggregate (C088-14).
  **Completed 2026-11-04:** the census is quoted 1:1 from the
  committed coverage block in `records/stage-s2-record.md` — claims
  876 by class (positive 2 / negative 6 / open 867 / closed_other 1);
  studies 89 (open 60 / unjudged 28 / restricted 1); judgment calls
  **0** on the live ledger (empty population, mechanism stated in
  the record — the emission path is fixture-proven); falsifier
  coverage recomputed **867/876**, the 9 nulls enumerated in the
  find list (the 848/857 expectation above predates the T004
  intake — departure (a) in the record).
- [x] **T203 — Determinism proof.** Delete the artifacts, regenerate,
  byte-compare; hashes recorded in the stage record. Claims: C088-13.
  Acceptance: **test** (byte-identity across the delete-and-regenerate
  cycle, twice).
  *This does not establish:* determinism under changed inputs — only that
  the build is a pure function of the inputs it declares.
  **Completed 2026-11-04:** two delete-and-regenerate cycles over
  the real root, byte-identical both times (sha256 listings diffed
  empty); the hashes equal the S1 scratch build's, so the committed
  bytes are the same bytes S1 proved. Record:
  `records/stage-s2-record.md`.

## Stage 3 — Gate extension (PR: feat/088-s3-gate-v10)

- [x] **T301 — Gate class V10.** `ledger_gate.py` gains V10
  (program-map equivalence) with the gate's own registered copies of
  program-map-defs v1 (not imported from the builder): recompute the map
  by an independent route; check artifact byte-equality, exact coverage,
  citation resolution, stamp freshness against the current ledger, and
  find-list equality. Claims: C088-7. Acceptance: **gate** (the gate CLI
  over the real tree reports ALL PASS with V10 in the per-class list).
  *This does not establish:* that the derivation is correct — two routes
  agreeing is consistency; the defs' semantics were the owner's call at
  T003/T101.
  **Completed 2026-11-04:** V10 landed as four legs (taxonomy coverage
  and format, bidirectional; program-map.json byte-equality; finds
  byte-equality; stamp freshness) over the gate's own registered
  program-map-defs v1 copies and an independently coded recomputation
  route (`_derive_program_map`; no builder import). Gate CLI over the
  real tree: full **24 PASS / 0 FAIL / 1 NOT-RUN**, `--regen` **27 PASS /
  0 FAIL / 0 NOT-RUN**, both ALL PASS with V10 in the per-class list —
  verbatim outputs in `records/stage-s3-record.md`. Where the layer has
  not landed at all (no taxonomy, no artifacts) V10 enumerates a single
  NOT-RUN, the V5 posture; the PR-scope CLI routes the program-map
  paths and the builder to a `program_map` layer carrying V10.
- [x] **T302 — V10 teeth.** Seeded-divergence tests on tmp copies: a
  mutated program-map.json fails V10 and the report names it; a
  builder-vs-gate defs divergence fails; a stale stamp fails; a dropped
  node fails. Claims: C088-7. Acceptance: **test** (each seeded case
  fails the gate for the stated reason).
  *This does not establish:* that no unseeded divergence can pass — only
  that the named failure modes are caught, which is what teeth means.
  **Completed 2026-11-04:** six seeded cases in
  `backend/tests/test_spec086_ledger_gate.py`, each FAILing by name —
  hand-edited standing, dropped claim node, dropped find, builder-vs-gate
  defs drift (artifacts rebuilt under a drifted derivation table), stale
  stamp (`ledger_lines`), dropped taxonomy assignment — and each
  asserting the seeded tree's hashes are identical before and after the
  gate run (the gate wrote nothing). Results in
  `records/stage-s3-record.md`.
- [x] **T303 — V9 registration for the map artifacts.**
  `program_map_generate` joins the registered-writer list; the map
  artifact paths join the artifact patterns, so unregistered writes to
  them are gate failures. Claims: C088-7, C088-1. Acceptance: **gate**
  (gate suite green incl. a negative case: an unregistered-path write
  pattern is refused).
  *This does not establish:* protection against a writer added by a
  future amendment — amendments are acts, reviewed as such.
  **Completed 2026-11-04:** the writer registration landed at S1
  (departure (d) there: V9's census required it once the builder
  existed). S3 confirmed the artifact-pattern side — the existing
  `glossa-indus/map` prefix pattern in `ARTIFACT_PATH_PATTERNS` covers
  the program-map paths, and the V9 census on the clean tree names
  `program_map_generate.py` among the registered writers — and added
  the negative case: a seeded unregistered writer of
  `program-map.json` fails the V9 census by name
  (`test_teeth_v9_census_catches_an_unregistered_program_map_writer`).

## Stage 4 — The page (PR: feat/088-s4-page)

- [x] **T401 — Page rendering in the builder.** `program-map.html`: data
  embedded verbatim; collapsible domains/subdomains; class chips; filters
  and search over generated fields only; stamp + per-domain counts in the
  header; restricted studies name-only. The gate's V10 artifact list is
  amended in the same PR to include the page (defs discipline; recorded
  in the stage record). Claims: C088-8, C088-14, C088-19. Acceptance:
  **test** (conformance: page bytes regenerate identically; a source scan
  shows no standing logic beyond filtering/searching generated fields).
  *This does not establish:* that the page reads well — that is T402's
  rendered evidence and the reader's judgment.
  **Completed 2026-11-04:** the builder emits `program-map.html` as
  exactly the registered template (`_PAGE_HEAD`/`_PAGE_MID`/`_PAGE_TAIL`)
  wrapped around the two data artifacts embedded verbatim, with a
  fail-closed guard against a script-close sequence in the data;
  `--check` covers all three artifacts. The amendment to V10's artifact
  list landed in the same PR: the gate carries its own registered copies
  of the three template pieces (the agreement test pins them byte-equal
  to the builder's) and a fifth V10 leg byte-compares the page against
  the gate's recomputation from its recomputed data. Conformance: the
  committed page is template + verbatim data by construction and by
  test; the template source scan finds none of the eight registered
  statuses and no standing logic. Record:
  `records/stage-s4-record.md`.
- [x] **T402 — Playwright render verification.** The generated page
  rendered at desktop (1440×900) and mobile (390×844); screenshots kept
  with the stage record; checked: sections collapse, filters change the
  visible set correctly, search narrows to generated-field matches,
  counts match the coverage block, the restricted node shows no standing.
  Claims: C088-8. Acceptance: **human-as-oracle** (a named reviewer rules
  on the screenshots against the design points; per the standing rule,
  source checks alone never support a verified claim about a page).
  *This does not establish:* usability for every reader or device — two
  widths and the named checks are the evidence, no more.
  **Completed 2026-11-04:** `records/stage-s4-evidence/verify_page.py`
  (Playwright, Chromium) ran **14/14 checks passed** over the committed
  page at both widths — 876 claim rows and 89 study groups in the DOM,
  header stamp and per-domain counts equal to the coverage block, a
  domain section collapsing and reopening, the Negative filter showing
  exactly the 6 negative claims, search narrowing to generated-field
  matches, the restricted node name-only, the finds panel rendering all
  four kinds with the judgment-call kind's empty state shown as empty.
  Five screenshots in `records/stage-s4-evidence/`, read by the stage
  worker before any claim here: `desktop.png`, `desktop-study.png`,
  `desktop-filtered.png`, `desktop-restricted.png`, `mobile.png`;
  results in the same directory's `results.txt`.
- [x] **T403 — Publication through the gate.** The page + JSON + finds
  republished via `gated_publish.py`; the stage record cites the V10 gate
  output over these artifacts. Claims: C088-16. Acceptance: **gate**
  (ALL PASS incl. V10, quoted in the stage record).
  *This does not establish:* that publishing was wise — only that C1's
  order was kept: the verification existed before the surface did.
  **Completed 2026-11-04:** `gated_publish.py` gains
  `publish_program_map` (the T303 mechanics over the program map: the
  candidates are gated by a V10-scoped gate run over a scratch root
  carrying the candidates, never the published bytes; atomic replace
  only on ALL PASS). Publication run of record: published, candidate
  gate **5 PASS / 0 FAIL / 10 NOT-RUN** (the five V10 legs; the
  NOT-RUNs are the out-of-scope classes). The full gate over the real
  tree with the page landed: **25 PASS / 0 FAIL / 1 NOT-RUN** full,
  **28 PASS / 0 FAIL / 0 NOT-RUN** `--regen` — V10 section quoted
  verbatim in `records/stage-s4-record.md`. The two JSON artifacts
  republished byte-identical (SHA-256 unchanged from the S2/S3
  records); the page's SHA-256 is `b99d636e…`.

## Stage 5 — Gap scans (PRs: feat/088-s5a / s5b / s5c)

- [x] **T501 — Cluster A scan: corpus + anchors.** Domains: Sign
  inventory & corpus; Anchors & readings. Inputs: find list + coverage
  block for those domains; pre-answered legs per the scan plan (incl.
  the falsifier census). Output: `records/scan-corpus-anchors.md`,
  four-kind finds only, every candidate falsifier-carrying and typed
  (C088-12). Claims: C088-10, C088-12. Acceptance: **human-as-oracle**
  (classification review) + **test** (template conformance: kinds,
  falsifiers, types present on every line that needs them).
  *This does not establish:* that these are all the gaps in those domains
  — only that every find recorded is in the registered shape.
  **Completed 2026-11-04:** `records/scan-corpus-anchors.md` — 12
  finds (missing node 2, missing edge 3, thin evidence 5, stale
  bookkeeping 2), 14 candidates (A-06 carries three, one per
  revalidation route). The WP5 census was verified against the audit
  record itself (`anchor-support-audit.json` summary_counts:
  6/46/37/3/2) and the 37 requires-revalidation anchors routed from
  the audit's own fields (28 Phase-48 promotions / 5 single-line /
  4 sole crosswalk-literature imports). Consumes 20 of the 28
  `bundle_less_study` finds. Template conformance is T504's
  mechanical pass. Record: `records/stage-s5-record.md`.
- [x] **T502 — Cluster B scan: claim families + contact zone.** Domains:
  Claim families by study line; Contact zone & external corpora.
  Pre-answered legs: WP5 census (6/46/37/3/2), WP4 (0 of 184), WP2/WP3
  blockers. Output: `records/scan-families-contact.md`. Claims: C088-10,
  C088-12. Acceptance: **human-as-oracle** + **test** (as T501).
  *This does not establish:* that thin evidence means wrong — the census
  counts support classes; what they mean is the register's judgment,
  reviewed by the owner at T603.
  **Completed 2026-11-04:** `records/scan-families-contact.md` — 12
  finds (missing node 3, missing edge 3, thin evidence 3, stale
  bookkeeping 3), 12 candidates. Domain 4's thinness classified on
  the records as **not** honest smallness (B-09/B-10/B-12: the
  Laursen catalog leg has zero ledger claims — counted this scan —
  the sequence study is gated on the CISI Vol. 3 transcription, and
  the attestation study is bundle-less). Consumes 11 find-list
  items (9 `extracted_null_falsifier`, 2 `bundle_less_study`); the
  `restricted_node` find is explicitly carried to S6 (owner
  restriction by design, not a gap). Record:
  `records/stage-s5-record.md`.
- [x] **T503 — Cluster C scan: infrastructure + bookkeeping.** Domain:
  Program infrastructure, plus cross-cutting bookkeeping (the adoption
  record's §4 items: llms.txt staleness, desktop-clone sync, data-lineage
  question; the missing-directory finds for spec numbers 049 and 085).
  Output: `records/scan-infra-bookkeeping.md`. Claims: C088-10.
  Acceptance: **human-as-oracle** + **test** (as T501).
  *This does not establish:* that infrastructure gaps matter less — the
  register ranks; the scan only records.
  **Completed 2026-11-04:** `records/scan-infra-bookkeeping.md` —
  11 finds (missing node 2, missing edge 2, thin evidence 0, stale
  bookkeeping 7), 11 candidates. GAP-C12's legacy rule verified in
  the current tree (`experiment_graph_phase20.py` lines 462/474);
  the Spec 086 residuals recounted from the current matrix
  (dependency pairs 793; the join's population still 1 of 876); the
  desktop-sync find states the precision the records support
  (`309ea63c` is PR #472's merge commit and is in main's history —
  the desktop **checkout** stands 118 commits behind, per the
  GitHub compare read this scan). Consumes Domain 5's 6
  `bundle_less_study` finds. Record: `records/stage-s5-record.md`.
- [x] **T504 — Scan consolidation check.** Every find in the three scan
  records is exactly one of the four kinds; every candidate has a
  falsifier and an honesty-rule type; every find-list item from S2 is
  consumed by a scan or explicitly carried to S6. Claims: C088-10.
  Acceptance: **test** (the mechanical pass over the three records +
  find list).
  *This does not establish:* scan quality — shape only; quality is the
  oracle's and, finally, the owner's at ratification.
  **Completed 2026-11-04:** the mechanical pass over the three
  records + the find list (script run this stage; output quoted in
  `records/stage-s5-record.md`): 35 finds, each carrying exactly one
  kind line from the four registered kinds (missing node 7, missing
  edge 8, thin evidence 8, stale bookkeeping 12); 37 candidates,
  each with a falsifier line and an honesty-rule type line (counts
  equal per cluster: A 14/14, B 12/12, C 11/11); find-list
  consumption complete — all 28 `bundle_less_study` subjects named
  in a scan record (A 20, B 2, C 6), all 9
  `extracted_null_falsifier` claims' documents covered by B-05,
  the 1 `restricted_node` item explicitly carried to S6, and 0
  `judgment_call` items exist to consume.

## Stage 6 — Gap register v1 (PR: feat/088-s6-register)

- [x] **T601 — Register v1 drafted.** `glossa-indus/map/gap-register.md`
  in RCPH's format: ranked headline list; `GR-088-NN` entries with status
  words; each entry names the missing node/edge, why its absence blocks
  convergence, the candidate with its falsifier and type, and owner
  gates; closing owner-decisions section; ratification block. Claims:
  C088-11, C088-12. Acceptance: **human-as-oracle** (drafting review
  against the scan records: every scan find is in an entry or
  dispositioned).
  *This does not establish:* the ranking — ranking is judgment, and the
  owner's ratification (T603) is where it settles.
  **Completed 2026-11-04:** register v1 drafted — 37 entries
  (GR-088-01…37) consolidating the S5 scans' 35 finds and
  37 candidates, the carried `restricted_node` find
  (GR-088-37, restriction stated, no candidate), and one
  entry added at consolidation from its source record
  (GR-088-26, S-R3; departure (a) in
  `records/stage-s6-record.md`). Candidates 38, each with
  a falsifier and an honesty-rule type (mechanically
  counted 38/38). No two finds were merged (the
  deduplication analysis is in the register's census
  section). Drafting review: every scan find is in an
  entry — script-verified 35/35 with kinds matching.
- [x] **T602 — Completeness check against the source lists.** The
  source-coverage annex: every C088-11 source-list item mapped to entry
  id(s) or a recorded not-a-gap disposition. Mechanical legs (find-list
  items, the 28 unjudged studies, the 9 null-falsifier claims) checked by
  script; prose legs (GAP-C07, GAP-C12 remnant, WP2/WP3/WP5 items, Spec
  086 residuals, T201) checked against the annex by a named reviewer.
  Claims: C088-11. Acceptance: **test** (mechanical legs) +
  **human-as-oracle** (prose legs, reading the annex).
  *This does not establish:* completeness in nature — only completeness
  against the program's own named lists, which is the claim.
  **Completed 2026-11-04:** the source-coverage annex is
  `records/stage-s6-record.md` § "Source-coverage annex
  (T602)". Mechanical legs by script, all PASS (51 checks,
  0 failures): find-list items consumed (28/28
  bundle-less studies named, 9/9 null-falsifier claims
  dispositioned to GR-088-21, 1/1 restricted item carried
  to GR-088-37, 0 judgment-call items exist); entry
  structure and censuses recounted from the register's
  own text. Prose legs ruled against the annex by the
  stage worker (oracle sign-off line in the record).
  **Verdict: COMPLETE against the named lists** — every
  C088-11 item and every further named list item is
  represented in an entry or carries a recorded not-a-gap
  disposition with its reason; no unmapped item, so
  C088-11's falsifier does not fire.
  **Closeout correction 2026-11-04 (T701):** as T002 — the
  S6 stage recorded this completion but left the box
  unticked; flipped at closeout against the annex evidence
  of record. No work was re-executed.
- [x] **T603 — Owner block ratification of register v1.** The owner
  ratifies the register as a block (entries, ranking, dispositions, and
  the owner-decisions section). This act ends the spec; first waves are
  commissioned separately, from the ratified register, by a later owner
  act. Claims: C088-11. Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* that any register entry's candidate will
  succeed — only that the program's gap picture is now the ratified one
  work is commissioned from.
  **Status at S6 (2026-11-04): OPEN, by design.** This is
  the owner's act on the merged register; register v1 is
  presented for it with the S6 PR (its ratification block
  stands PENDING in `glossa-indus/map/gap-register.md`).
  It is the only task besides T701 left unticked, and it
  cannot be executed by a build stage.
  **Completed 2026-11-04:** ratified as a block by
  Tristen Pierson (option tap, "Ratify register v1 as a
  block", with confirming words, in the Glossa-Lab chat)
  — entries, ranking, dispositions, and the
  owner-decisions section, with GR-088-26 standing as a
  ratified entry (no strike recorded). The register's
  Ratification block is completed in the closeout PR.
  Record:
  `records/register-ratification-2026-11-04.md`.

## Closeout

- [x] **T701 — Closeout record.** Per-claim dispositions for C088-1..19
  (discharged / carried, with the evidence pointer for each); the final
  census quoted from the coverage block; the register's entry count and
  ratification reference; the explicit statement that no wave is
  commissioned by this spec and no claim's standing was changed by it.
  Acceptance: **human-as-oracle** (the stage reviewer against the stage
  records).
  *This does not establish:* program health — it establishes that the
  spec's own claims were each answered with evidence, which is the only
  closeout a spec can honestly give.
  **Status at S6 (2026-11-04): OPEN, by dependency.** The
  closeout requires the ratification reference, which
  exists only after T603; T701 follows T603 in the
  closeout act.
  **Completed 2026-11-04:** the closeout record is
  `records/stage-t701-closeout-record.md` — per-claim
  dispositions for C088-1..19 (all discharged, with
  evidence pointers and scope notes), the final census,
  the register's ratification reference (T603 above),
  and the explicit statement that no wave is commissioned
  by this spec and no claim's standing was changed by
  it. With this tick, tasks.md carries zero unticked
  tasks (verified mechanically at closeout).
