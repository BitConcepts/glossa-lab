# Spec 095 — tasks

## Adoption (this PR)

- [x] **T001 — the package lands.** spec.md, claims.md,
  aee-claims.json (C095-1..C095-17, each with a falsifier), plan.md,
  tasks.md, and the records (commission and grounding, Stage 0
  record) on branch `adopt/095-red-team-remediation`.
- [x] **T002 — AEE assessment of the package.** The bundle is
  validated and assessed under the pinned assessor (aee 1.5.3);
  the output is filed verbatim at
  `records/adoption-aee-assessment.json` and read in the
  ratification record, never edited.
- [x] **T003 — owner approval.** The owner adopted the package as
  Spec 095 on 2026-11-15 (22:29 ET, "Adopt it as Spec 095,
  reconciliation first, as recommended"), with D-095-1..D-095-6 as
  adopted. `records/ratification-2026-11-15.md`.
- [x] **T004 — claims-ledger intake, inside this PR (D-095-6).**
  The clean Spec 092 pattern (PR #548), explicitly not the Spec 094
  #566 exception: (a) the program-map assignment is entered in
  `glossa-indus/map/program-map-taxonomy.json` (Program
  infrastructure / Governance, lifecycle & generated layers — the
  subdomain of Specs 088-092 and 094; 095 is a governance and
  remediation spec binding the program's evidence machinery across
  domains, which is the family that subdomain holds); (b) C095-1..17
  are appended to `glossa-indus/ledger/claims.jsonl` through
  `tools/ledger/import_bundle.py`, the only sanctioned path, never a
  hand-edit; (c) the settling chain is refreshed in the standing
  precedent order (verify-canonicals before any pin moves; the T405
  pair re-executed with byte-equal result blocks; the comparison
  re-filed; sets re-materialized; the pin refreshed with the
  re-derivation recorded; the superseded pair departed under
  run-defs v2); (d) the generated layers are regenerated with the
  plain generators in dependency order (the Spec 093 Appendix A
  procedure); (e) the ledger gate's summaries in both modes on the
  final tree are recorded in the root LEDGER.md entry; (f) every
  census re-pin is re-set from the regenerated artifacts' actuals,
  with expected counts derived independently before acceptance.

## Stage 0 — Reconciliation and register (complete at adoption)

- [x] **T010 — the register.** Every row of the external red-team
  review dispositioned against the program's records: 43 rows
  (RT-01..RT-43); 23 DUPLICATE-OF-RECORD mapped to their owning
  vehicles (RT-06 among them, classified a security risk
  requiring verification under Spec 083); 18 rows carrying the
  14 NEW items isolated in register section N (RT-03 among them:
  the one confirmed defect, a micro-task on a duplicate family);
  two FACT-DISPUTED rows closed with the
  record governing (RT-42: 977 claims / 95 studies at 1,008 lines,
  not 912/91; RT-43: mini-server residency since 2026-11-09, not
  desktop). Deliverable: `register-draft.md` in the goal workspace's
  `hidden_files/red-team-2026-11-15/` (SHA-256 in the Stage 0
  record).
- [x] **T011 — the pinnability pass.** Priority 0 settled: the
  missing corpus and the missing loader are the same artifact
  (`firestore_indusarrays_full.jsonl`, the V3 loader's sole data
  file); the file is intake-pinned of record (PR #393) and its
  absence from checkouts is a placement defect (the raw subtree is
  gitignored by design); the remediation is prescribed fail-closed
  (locate, verify against the pin, place read-only, reproduce,
  then re-execute under a new order). Deliverable:
  `pinnability-p0.md`, same directory and citation.
- [x] **T012 — the public-surfaces pass.** RT-03 CONFIRMED (the
  anchor-model README presents the v2-era 161-anchor package as
  current, with no supersession notice); the tracker matches the
  record except one stale ledger sentence (quoted verbatim in the
  pass); the review's app claim is its tool limit, not a defect
  (edge serves, backend health verified by identity); accessibility
  is covered by no program record. Deliverable:
  `public-surfaces.md`, same directory and citation.
- [x] **T013 — the validator census.** At the census clone's HEAD:
  every corrected v2 module's only consumers are its own repair
  tests; the four v1 node paths stand registered in the live app
  with no guard of any kind (phonotactics Phase-58 and Phase-108
  nodes; site-statistics Phase-69 node and provenance recompute;
  crosswalk Phase-96 node); no current evidence path computes with
  v1; exposure is prospective. Deliverable: `validator-census.md`,
  same directory and citation.
- [x] **T014 — the owner-gated micro-tasks recorded (D-095-5).**
  The RT-03 README supersession banner and the tracker's stale
  ledger sentence (with its not-re-verified standings line) are
  recorded in the Stage 0 record as owner-gated micro-tasks,
  outside this spec's stages.

## Stage 1 — Corpus reproducibility (not commissioned)

- [x] **T101 — locate and verify the strict-corpus artifact.**
  Search the candidate venues read-only (custody snapshots,
  desktop-era archives, surviving trees); hash every candidate;
  the PR #393 pin decides. Any other digest stops the task
  (D-095-3). (C095-2.)
- [x] **T102 — place read-only and reproduce.** Place the verified
  file at the canonical path with read-only permissions; reproduce
  the census (3,916 / 3,137 / 2,665 / 12,494) and the canonical
  export pin through the V3 loader; file the reproduction record.
  (C095-2.)
- [x] **T103 — Spec 053 step 0 re-execution.** Under a new
  execution order naming this task, gates byte-unchanged from Spec
  053's frozen step 0; the outcome files as its own record and
  moves no frozen text. (C095-2.)
- [x] **T104 — the corpus identity standard.** State the identity
  of record for every claim-bearing corpus (version, content hash,
  source, licensing, counts under a named basis, normalization
  rules) and make the covered loaders verify it and fail closed.
  (C095-3.)
- [x] **T105 — the twelve-case battery.** The twelve fail-closed
  cases as a named CI suite over the covered loaders, each case's
  refusal or flag as defined, running on every covered-loader
  change. (C095-4.)

## Stage 2 — Validator and synthetic containment (not commissioned)

- [x] **T201 — the five-validator consumer census completed.**
  corpus_frames and replay076 brought to the Stage 0 census
  standard; every consumer of every corrected family named.
  (C095-5.)
- [x] **T202 — the four v1 node paths discharged.** Each path
  migrated to its v2 module, retired from the registry, or
  mechanically guarded, with the disposition recorded per path.
  (C095-5.)
- [x] **T203 — the planted legacy-rule pinning test.** A legacy
  v1-rule call planted in a claim-bearing path fails the test;
  the test runs in CI. (C095-5.)
- [x] **T204 — synthetic containment.** Every
  `indus_public_corpus` consumer censused and classified; the
  synthetic labelling machine-checked; the planted
  synthetic-as-real fixture fails its pinning test. (C095-6.)

## Stage 3 — Evidence machinery (not commissioned)

- [x] **T301 — the contamination gate class.** The six shapes
  flagged at intake in the ledger gate; the six historical
  instances re-detected from their records in the acceptance
  fixtures. (C095-7.)
- [x] **T302 — the standards stated once.** Equivalence and
  statistical-reporting standards of record, program-wide;
  later studies cite them. (C095-8.)
- [x] **T303 — the identifiability protocol, first application.**
  Rival constructions against M044, M047, M124, M202, M329, M330;
  the NOT IDENTIFIABLE amendment recorded; the six standings
  re-stated under the outcome. (C095-9.)
- [x] **T304 — reading direction as data.** Orientation basis
  carried in the claim-bearing corpora; positional results
  re-issued with named assumptions and reversed variants or
  undefined-reversal statements. (C095-10.)

## Stage 4 — Platform and surfaces (not commissioned)

- [x] **T401 — the multi-script specification.** Seventeen
  entities with claims and falsifiers; sign shape separated from
  value and meaning; no Indus or Proto-Dravidian assumption in the
  generic layer. (C095-11.)
- [x] **T402 — the Indus instantiation.** The Indus record
  instantiates the model with zero changed facts, counts, or
  standings, proven by before/after census. (C095-11.)
- [x] **T403 — the dashboard home and feature set.** Wireframes
  approved by the owner by name; features built to them;
  Playwright desktop and mobile verification before any verified
  claim; refusals named per feature. (C095-12.)
  (Stage 4: wireframes filed in this spec's wireframes/
  directory. Build: owner approved the wireframes by name
  2026-11-18; built and verified the same day — build record
  records/t403-dashboard-build-record-2026-11-18.md, screenshot
  set in records/t403-screenshots/. C095-12's build half is
  discharged in the build record's terms.)
- [ ] **T404 — the audit package run.** Functional checklist,
  eight-step new-researcher protocol, accessibility pass; scored
  against pre-fixed thresholds; failures filed with screenshots.
  (C095-13.)
  (Stage 4: the run is complete and its package verdict is
  FAIL — see the Stage 4 record; not ticked. Remainders: the
  dashboard leg after the T403 build, and the authenticated
  legs on the owner's sessions.)
  (2026-11-18: the dashboard leg has now run against the built
  dashboard — addendum records/t404-dashboard-leg-addendum-
  2026-11-18.md: protocol 8/8 (P1 met), A1 not met, A2 met.
  T404 remains unticked: the authenticated legs and the
  remediation-scope decision stand.)
- [x] **T405 — the composed release gate.** Thirteen components,
  results recorded per candidate, exceptions only as recorded
  owner-approved entries; the planted RT-03-shape stale claim
  blocks its candidate. (C095-14.)
- [x] **T406 — the derived document set.** docs/red-team/
  documents generated under the no-authority rule, sources named
  on their faces. (C095-17.)

## Stage 5 — Second targets, scoping only (not commissioned)

- [x] **T501 — the Eteocypriot proposal and preregistration
  draft.** Corpus legal status and source, bilingual and
  sign-list basis, held-out design, adjudication route; no
  analysis executed. (C095-15.)
  (Stage 5: proposal and preregistration draft filed in this
  spec's second-targets/ directory; execution is a separate
  owner decision — see the Stage 5 scoping record.)
- [x] **T502 — the Meroitic benchmark scoping.** The reproduction
  benchmark scoped as a study spec on the existing fixture;
  success criteria and falsifier fixed in the scoping record; no
  execution. (C095-16.)
  (Stage 5: benchmark scoped as a study spec in this spec's
  second-targets/ directory, with success criteria and a
  falsifier fixed there; execution is a separately
  commissioned study — see the Stage 5 scoping record.)
- [ ] **T503 — closeout.** The register re-checked against
  C095-1 (no duplicate worked twice, no NEW item lost); every
  claim discharged or carried as a named remainder; the closeout
  record filed in this directory.
