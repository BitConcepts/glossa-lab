# Feature Specification: Full-Picture Program Map + Gap Register

**Feature Branch**: `088-program-map` (build stages); this package lands on
`feat/088-spec-package`
**Created**: 2026-11-04
**Status**: Draft package — awaiting the owner's block approval (Stage 0, T003)
**Input**: The owner's instruction, delivered through the RCPH chat on
2026-11-04, that the full-picture system RCPH built for its own program (a
generated whole-program map, four-kind gap scans, and a ratified gap
register) be taught to the framework's other projects; this chat's adoption
assessment and disposition (ADOPTED, with constraints C1 and C2) in
`records/adoption-2026-11-04.md` and the adoption record at
`files/2026-11-04-spec088-adoption-full-picture-map.md`; the owner's go for
the package build-out, 2026-11-04.
**Evidence of record**: RCPH's reference implementation
(`analyses/proposal-engine/program-map/`: `taxonomy.json`,
`build_program_map.py`, `program-map.json`, `index.html`) and its gap
register (`analyses/proposal-engine/gap-register-2026-11-04.md`, entries
GR-01..GR-18, ratified by the owner as a block; its first wave is executing
there). The Glossa inputs counted first-hand on 2026-11-04: the ledger
(`glossa-indus/ledger/claims.jsonl`, 888 lines = 857 claim entries + 31
annotation entries, canonical SHA-256
`f988ed61404daf8200479e9d1a6580526c7b419ba7e802a3b6b41a5a73a167ac`), the spec
tree (88 directories under `specs/`, every one carrying a `spec.md`), and the
Spec 086 verification gate (`backend/glossa_lab/ledger_gate.py`, classes
V1–V9).
**Predecessors**: Spec 086 (the Winning Combination adoption: ledger, matrix,
map, gate — this spec's substrate and its gate), Spec 087 (node-system
tightening), Spec 084 (policy-sync conformance — the conformance-test style
this spec follows), Specs 025/026 (research-check and the RCPH framework
transfer — the channel this teaching arrived through).

## Problem statement

The program's truth lives in three places that do not yet compose into one
picture. The ledger holds 857 claims with standings; the spec tree holds 88
study directories; the generated matrix and map of Spec 086 cover the ledger
population, but they are claim-relation views, not a program picture: no
surface shows every claim and every study as a node, grouped into the
program's domains, each node carrying a standing a reader can trace to its
record. A newcomer (or the owner, returning after a week away) cannot see, in
one place, what the program consists of, what each piece's standing is, and —
the point of the exercise — where the picture is thin: which studies carry no
judged claims at all, which standings rest on few or circular supports, and
which named gaps from the program's own audits have never been consolidated
into one register a wave of work can be commissioned from.

RCPH built exactly this for its program and the owner directed the teaching
be carried here. Glossa's version must be stricter than the reference in one
respect the adoption record settles: RCPH's map admits curated standings
(a node's standing entered from a ratified source, marked with its source).
Glossa's Spec 086 settlement forbids that shape here — truth flows one way,
ledger → matrix → map, and a standing that exists only in prose is a finding
for the register, not data for the builder (constraints C1/C2, §Decisions).
Glossa's map is therefore derived or unjudged, everywhere, with the
shortfalls emitted as finds.

A second difference is scale: RCPH's ledger holds 44 claims; Glossa's holds
857, with 834 bundle claims across 60 spec directories and 28 spec
directories (the whole pre-026 era, plus `026-core-research-source`) that
carry no ledger claims at all. The map has to cover both masses exactly, and
the 28 unjudged studies are not an embarrassment to be smoothed over — they
are GAP-C13's shape stated per study, and the register's first content.

## Scope — what this spec builds

- **S1 — Definitions, taxonomy, builder core.** `program-map-defs v1`
  registered as a definitions document (the matrix-defs pattern):
  derivation tables, roll-up precedence, stamp contents, find kinds. The
  curated taxonomy `program-map-taxonomy v1` as a versioned JSON file
  (the draft assignment ships with this package:
  `records/taxonomy-v0-draft.md`). A pure builder module
  (`backend/glossa_lab/program_map_generate.py`) + CLI
  (`tools/map/generate_program_map.py`) in the manual-generator pattern:
  pure function of its inputs, `--check` mode that builds without writing
  and fails on drift, self-tests with teeth.
- **S2 — Standing derivation.** Claim classes and standing texts derived
  mechanically from ledger fields under the defs; study classes by the
  registered roll-up; judgment calls and finds emitted into a machine find
  list beside the map; a derivation census in the stage record (per-domain
  counts, the judgment-call list, the unjudged list); determinism proven by
  delete-and-regenerate byte-identity.
- **S3 — Gate extension.** The Spec 086 gate gains class **V10 —
  program-map equivalence**, with the gate's own registered copies of
  program-map-defs v1 (never imported from the builder), recomputing the
  map by an independent route and failing on any divergence, coverage gap,
  unresolvable citation, or stale stamp. Seeded-divergence tests prove the
  teeth. This stage lands before the page publishes (C1).
- **S4 — The page.** A single generated static page (data embedded
  verbatim, RCPH pattern): domains as collapsible sections, class chips,
  filters and text search over generated fields only, per-domain counts
  from the generated coverage block. Restricted studies render name-only.
  Playwright render verification at desktop and mobile widths before any
  verified claim about it.
- **S5 — Gap scans.** Three scan clusters over the generated map —
  corpus+anchors, claim families+contact zone, infrastructure+bookkeeping —
  each classifying every find as exactly one of **missing node / missing
  edge / thin evidence / stale bookkeeping**, each proposed candidate
  carrying a one-line falsifier. Standing pre-answered legs (the falsifier
  census, the WP5 support census, the WP4 circularity count) are cited from
  their records, not re-derived.
- **S6 — Gap register v1.** One consolidated register in RCPH's entry
  format, consolidating every standing named gap (GAP-C07, the GAP-C12
  remnant, GAP-C13, the repair brief's WP2/WP3/WP5 residuals, Spec 086's
  residuals, the T201 divergence, and the adoption record's §4 items),
  gated by a completeness check against those source lists. The spec ends
  with the owner's block ratification of the register.

## Non-goals (explicit)

- **No SPA integration in v1.** The page is a standalone generated artifact
  in the map layer's home (`glossa-indus/map/`), not a view in the Glossa
  web app. App integration is a later spec if the owner wants it.
- **No external publication.** The map and register are internal program
  surfaces. Nothing here is deposited, posted, or sent anywhere.
- **No claim changes.** No stage of this spec adjudicates, reclassifies,
  annotates, or scores any claim. The spec's total ledger diff is its
  adoption intake append (this package's own claims, through
  `tools/ledger/import_bundle.py`) plus the regeneration of the generated
  layers that append forces — exactly the Spec 087 adoption shape.
- **No first-wave execution.** The register, once ratified, is what waves
  are commissioned from. Commissioning and executing a wave is a separate
  owner act, outside this spec.
- **No prose standings, ever (C2).** RCPH's curated-standing mechanism
  (source + token) is not adopted. A standing that exists only in prose
  produces an unjudged node plus a stale-bookkeeping find.
- **No decipherment claim of any kind.** The map reports standings of
  claims; it does not advance, summarize into, or soften the program's
  standing position that the Indus script is not deciphered.

## Constraints carried from the adoption (binding)

- **C1 — the gate extension rides this build.** The program map is a wider
  population than the matrix/map the Spec 086 gate verifies. It never
  ships around the gate: S3 lands before (or with) the page's publication,
  and a red V10 blocks the map artifacts exactly as a red class blocks the
  matrix today (claims C088-7, C088-16).
- **C2 — prose-only standings are register finds, never map data.** The
  builder reads the ledger, the taxonomy, and the spec tree's directory
  names — never a spec's prose, a stage record, or a report — when
  producing a standing (claims C088-3, C088-17).

## Decisions

- **D-088-1 — Node granularity: one node per claim, one per study.**
  Options: (a) RCPH's grouped nodes (a node bundles related claims and
  specs); (b) individual claim nodes (857) + study nodes (88), grouped for
  display by the taxonomy's domains.
  *Recommendation: (b).* At 44 claims, grouping is a convenience; at 857,
  grouping is an editorial act that would bury per-claim standings — above
  all the unjudged and null-falsifier mass the register exists to expose.
  Individual nodes keep every standing visible and every citation exact;
  the taxonomy supplies the grouping for display. (Human-as-oracle: the
  owner settles this by ratifying the package.)
- **D-088-2 — No curated standings (C2 applied).** RCPH's `curated`
  mechanism is rejected for Glossa: it would let prose standings into the
  map layer, against truth-flows-one-way. The unjudged class and the find
  list replace it. *Recommendation: adopt as a constraint, not an option*
  (settled in the adoption record; restated here so the package's
  ratification covers it).
- **D-088-3 — The derivation table's two judgment rows.** The ledger's
  status vocabulary (counted 2026-11-04: draft 833, untested 12,
  partially_supported 3, strongly_supported 2, contradicted 4,
  partially_falsified 1, unsupported 1, superseded 1) maps to classes:
  strongly_supported → positive; contradicted / unsupported /
  partially_falsified → negative; superseded → closed_other; draft /
  untested → open; **partially_supported → open** (registered judgment:
  partial support is not a program judgement of support, and v1 has no
  "mixed" class; the verbatim status is shown in the standing text so
  nothing is hidden). Any status outside the table fails the build.
  *Recommendation: the table as stated*, settled by the owner's package
  ratification (human-as-oracle), thereafter changeable only as a defs
  amendment.
- **D-088-4 — `in_flight` is registered with an empty v1 population.** No
  record of record in the repo carries study run-state (job state lives in
  the live backend, outside the builder's inputs), and deriving it from
  prose is C2-forbidden. The class exists in the defs with no derivation
  rule; a build emitting it fails. Running work is visible through the
  scans and register instead. *Recommendation: as stated* — a named v1
  limitation, not a silent omission.
- **D-088-5 — Map home and stamp.** Artifacts live in `glossa-indus/map/`
  beside Spec 086's map (`program-map.json`, `program-map.html`,
  `program-map-finds.json`). The as-of stamp carries only input-derived
  values (ledger canonical hash, ledger line count, the ledger's own
  latest entry date, defs + taxonomy versions) — the Spec 086 stamp
  discipline; no wall-clock date anywhere (RCPH's builder stamps
  `date.today()`; Glossa deliberately does not).
- **D-088-6 — Restricted studies render name-only.** Spec 072 is under a
  standing owner restriction (public naming only: "executed — held under
  the Roif gate"). Its study node renders name + restricted flag + that
  registered form, with no derived standing displayed. The mechanism is
  general (a `restricted` list in the taxonomy), the v1 population is
  exactly that one study.

## Requirements (summary; the claims in claims.md are the normative text)

- **FR-088-01 — Generated-only map with drift failure** (S1; C088-1,
  C088-13). The map JSON and page are produced only by the builder from
  the ledger, the taxonomy, program-map-defs, and the spec tree; `--check`
  exits nonzero naming any committed output that differs from a fresh
  build, and writes nothing.
- **FR-088-02 — Total, exact, fail-closed coverage** (S1; C088-2). Every
  ledger claim id is assigned to exactly one claim node and every spec
  directory to exactly one study node; duplicates, omissions, unknown ids,
  and unassigned directories fail the build with nothing written.
- **FR-088-03 — Mechanical claim standings** (S2; C088-3). A claim node's
  class and standing text are computed from its governing ledger entry's
  fields under the registered derivation table, reclassification chains
  resolved in ledger order; the builder reads no prose for any standing;
  an unregistered status string fails the build.
- **FR-088-04 — Registered study roll-up with named judgment calls** (S2;
  C088-4). A study node's class is the defs' roll-up over its member
  claims; underdetermined (mixed positive+negative) studies are listed as
  judgment calls in the build record with member counts and the registered
  default class displayed.
- **FR-088-05 — Bundle-less studies: unjudged plus a find** (S2; C088-5).
  A spec directory with no bundle claims in the ledger (28 today) receives
  an unjudged study node and one machine-generated find in the find list.
- **FR-088-06 — Every node cites its record** (S1–S2; C088-6). Every claim
  node carries its ledger id; every study node its spec directory; an
  unresolvable citation fails the build (and the gate).
- **FR-088-07 — Gate class V10 with its own registered defs** (S3; C088-7,
  C088-16). The gate recomputes the program map under its own registered
  copies of program-map-defs v1 and fails unless recomputation equals the
  published artifacts, coverage is exact, citations resolve, and the stamp
  matches the current ledger; no map artifact publishes before V10 is live
  over it (C1).
- **FR-088-08 — The page is a view of generated fields only** (S4;
  C088-8). Filters and search act exclusively on fields in
  program-map.json; the page computes no standing, class, or count of its
  own; restricted studies render name-only (D-088-6, C088-19).
- **FR-088-09 — The taxonomy is curated, versioned, amendment-only**
  (S1; C088-9). Assignments live in `program-map-taxonomy v1`; the builder
  fails on an undeclared domain/subdomain; an assignment change is a new
  taxonomy version recorded in the stage record in the same motion.
- **FR-088-10 — Four-kind scans; a falsifier per candidate** (S5;
  C088-10). Every scan find is exactly one of missing node / missing edge
  / thin evidence / stale bookkeeping; every proposed candidate carries a
  one-line falsifier; anything else fails the register stage's
  completeness check.
- **FR-088-11 — Register v1 consolidates the named gaps, checked** (S6;
  C088-11). Every item on the registered source lists maps to at least one
  register entry or a recorded not-a-gap disposition; the consolidation
  task runs the completeness check and fails on an unmapped item.
- **FR-088-12 — The honesty rule is typed, not aspirational** (S5–S6;
  C088-12). In-house re-derivation and independent confirmation are
  distinct edge/candidate types in the map and register, never recorded as
  each other; an outside-reproduction gap closes only on evidence
  originating outside this lab's lineage (standing instance: WP4's
  eligible independent Parpola comparisons, 0 of 184).
- **FR-088-13 — Per-domain counts only** (S1–S4; C088-14). Summaries
  report node counts per domain and per class within a domain; no output
  computes a cross-domain aggregate progress score.
- **FR-088-14 — The ledger does not move** (all stages; C088-15). Beyond
  the adoption intake append, no stage writes to the ledger; the map
  derives standings and never writes them back.
- **FR-088-15 — No curated-standing mechanism exists** (S1; C088-17). The
  taxonomy format has no standing/status field for any node; the builder
  has no code path that accepts one.
- **FR-088-16 — `in_flight` stays empty in v1** (S1–S2; C088-18). The
  class is registered with no derivation rule; a build emitting an
  in-flight node fails.

## Governance

Claims first (this package's `claims.md` / `aee-claims.json`, C088-1..19),
assessed under the pinned AEE before any build task starts (Stage 0, T002 —
the assessment is in `records/t002-aee-assessment.json`, its invocation and
verbatim outcome in `records/t002-note.md`). Verdicts and citations follow
program doctrine: numbers only from records read first-hand; assessments by
actually running the assessor; CI green or the work is not done; Playwright
screenshots before any verified claim about the page. The owner's block
approval of this package (T003) is the ratification act for the spec, the
taxonomy v0 draft, and decisions D-088-1..6; the owner's block ratification
of gap register v1 (S6) is the act that ends the spec.
