# Spec 096 — Adoption record, 2026-11-20

Stage 0 (program setup) executed under the owner's direction of
2026-11-20: the Eteocypriot work stands as its own program in
Glossa-Lab, not as a deliverable inside Spec 095's package. The
Spec 095 Stage 5 scoping documents
(`specs/095-red-team-remediation/second-targets/eteocypriot-proposal-2026-11-17.md`,
SHA-256 `6034663dba1c7a0bfc88d5475031f7b894240a2e4f0e25eb748733c9f1af12d6`;
`eteocypriot-preregistration-draft-2026-11-17.md`, SHA-256
`ab680522bffcf7a87bfebe784aaae54b5226f0df1deb8330120a0b962277f30f`;
`records/stage-5-scoping-record-2026-11-17.md` §2, SHA-256
`3b1fa6c5587c74b245b40f3a6dcf4682f89d9a78629582739254b8d87624fadf`)
are the founding record, cited as provenance and unedited.

## The package

`specs/096-eteocypriot-program/` carries spec.md, plan.md,
tasks.md, claims.md and aee-claims.json. The claims C096-1..C096-4
re-express the preregistration draft's EC-D1..EC-D4 with the same
falsifiers and does-not-establish bounds, under decisions
D-096-1..D-096-5 as filed in spec.md. The AEE adoption assessment
(aee 1.5.3, `run_aee.py assess --phase after_plan`) returned
outcome "iterate" over 4 claims with 16 failure modes, the
expected shape for draft claims at adoption; the assessment is
filed verbatim at `records/adoption-aee-assessment.json`.

## Program map

The program is registered in
`glossa-indus/map/program-map-taxonomy.json` under Program
infrastructure / Governance, lifecycle & generated layers
(D-096-4), and the generated layers (matrix, program map,
map-data) are regenerated over the grown ledger in this PR.

## Claims intake and the settling-chain refresh

Intake ran through the sanctioned importer only
(`tools/ledger/import_bundle.py --spec specs/096-eteocypriot-program
--date 2026-11-20`): **4 appended, 0 already canonical**
(`096-eteocypriot-program/C096-1..C096-4`), each at status draft /
stage created; no standing is set by intake. Ledger validation
PASS, errors none. The ledger stands at **1,029 lines (from
1,025), 998 claim entries (from 994)**, canonical SHA-256
`09ca2407e2a7769e5fe73ded8402d22998ef8388ede777617fbfa678eb6f9a53`
(from `b200827ce16d643f6567cfb9dac10524c89f592d653c2ae5c775697f87cd4100`).

The settling chain was refreshed in the standing precedent order
(Spec 093 ratification Appendix A; Spec 095 T004):

- verify-canonicals over the grown build, before any pin moved:
  **6/6 PASS**.
- Both T405 scenarios re-executed over the grown ledger (same
  candidates, same 286-sign full-frame scope, run-defs v3): runs
  `settling-20261120T184448Z-337450` (t405-incumbent-over-full-frame)
  and `settling-20261120T184451Z-658fe3`
  (t405-full-register-over-full-frame); **result blocks byte-equal**
  to the superseded generations
  (`settling-20261116T034814Z-3681c4`, `settling-20261116T034819Z-8203db`).
- The Stage 4 comparison re-filed
  (`specs/086-winning-combination-adoption/records/stage-4-dual-run-comparison.json`;
  the diff is the ledger pin only).
- Assignment sets re-materialized unchanged (run
  `settling-20261120T184602Z-1a1d67`; incumbent 94, full-register
  286, H003 out of frame).
- `settling-canonical.json` provenance pin refreshed to the grown
  ledger with the re-derivation recorded as `re_derivations[11]`
  (expectations_changed false).
- The superseded pair departed the store under the D-D rule; their
  departure is accounted in the run index by departure acts
  (run-defs v3 §7.1) appended through `run_records.append_act`,
  carrying the superseding commit `2dc815ecbe1e024966d8e36262a9ee9c4c1124ff`,
  each record's final git blob and its SHA-256 (the field method
  was verified against the 2026-11-16 generation's historical act
  before use). The records stand preserved in git history.
- The run-index completion pass (`build_legacy_index.py`) entered
  the `re_derivations[11]` event; folded census 47 entries.
- Generated layers regenerated with the plain generators in
  dependency order: matrix, program map, map-data (map-data.json
  SHA-256 `75712e1ee5b77b57aabecef9ba8c0d5389b5a1e415ef8c24bb182accbdd25f8e`;
  settling runs carried: 2).

Every census pin in the test suites was re-set from the
regenerated artifacts' actuals (claims 994 -> 998, bundle
971 -> 975, open 985 -> 989, draft 970 -> 974, studies 96 -> 97,
Program infrastructure studies 23 -> 24, falsifier-present
985 -> 989, claims untouched by any run 993 -> 997, matrix
cells and map edges 1517 -> 1521, map edge census supports
1510 -> 1514, ledger lines 1025 -> 1029, map element kinds
1638 -> 1642, AEE-state census 994 -> 998, dashboard and
system-graph e2e censuses 994 -> 998, and the T405 run of record
in the Spec 095 T403 dashboard tests re-pinned to the incumbent
generation settling-20261120T184448Z-337450, whose quantities
are the superseded generation's, byte-equal), per the standing
intake-refresh discipline.

The ledger gate on the final tree, both modes, run standalone:
**default 29 PASS / 0 FAIL / 1 NOT-RUN (RESULT: PASS)** and
**--regen 32 PASS / 0 FAIL / 0 NOT-RUN (RESULT: PASS)**. (The
single NOT-RUN in default mode is the V7 lossless-regeneration
check, which runs under --regen.)

## Platform registration (live backend, mini-server)

The program also stands in the Glossa-Lab platform itself, under
the owner's direction of 2026-11-20:

- **Project created** through the platform's own project API
  (`PUT /api/v1/projects/eteocypriot_program`), the same machinery
  the dashboard uses: id `eteocypriot_program`, label "Eteocypriot
  Program", slug `eteocypriot-program`, with the program's
  description, prompt context, question and standing position as
  filed in the create body of record. Created
  2026-11-20T19:00:18Z. **Read-back verified**: `GET
  /api/v1/projects/eteocypriot_program` returns the record as
  created; the project list shows `indus_decipherment` (active),
  `meroitic_reproduction_benchmark` and `eteocypriot_program`
  (both inactive); `GET /api/v1/projects/active` still returns the
  Indus project. The Indus program's project, records and stores
  were not touched.
- **Claims and the spec register in the platform**: the platform
  models claims as the repo claims ledger it serves (there is no
  claims table in the platform database) and the spec register
  (`GET /api/v1/spec-studies`) is enumerated from the serving
  checkout's `specs/` tree. C096-1..C096-4 therefore reach the
  platform's claim surfaces, and Spec 096 reaches the spec
  register, when the serving checkout is next updated to the
  merged main; that update is an operations act on the serving
  tree and is **not** performed by this setup. Verification route
  once it lands: `GET /api/v1/spec-studies/096` and the foundation
  check.
- **What the platform cannot carry**: the corpus catalogue
  (`GET /api/v1/corpus-catalogue`, 39 entries) carries no
  Eteocypriot or Cypriot-syllabic entry, and the catalogue API
  exposes no create route (entries are seeded in code), so the
  project record's `corpus_ids` stands empty and the frozen corpus
  lives as the program's repo record (Stage 1). Seeding a
  catalogue entry is a code change outside this setup act and is
  recorded here as a named gap, not improvised around.

## Venue

Every computation in this stage ran on the mini-server (the
claims importer, the AEE assessment, the settling re-executions,
the generators, both gate modes, and the platform API calls
against the backend on the same host), under the owner's standing
execution-home rule.

**AI disclosure:** executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution sec. VI.
