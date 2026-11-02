# Spec 086, Stage 5 — wireframes for the layered map (T501)

**Status: DRAFT for Tristen's approval.** Nothing in this package is approved
until Tristen approves it in the Glossa-Lab chat. Approval here is the gate
that unblocks T502 (the map builder), T503 (the surface), and T504
(Playwright verification against these screens). If the built surface later
deviates from the approved screens, the build stops and the deviation is
reported — it is never absorbed silently.

Format precedent: the Spec 081 wireframes package (2026-10-29) and the
Spec 085 design input (2026-11-01). Screens are rendered as static HTML
wireframes sharing `wireframes/wireframes.css`; every screen carries an
annotation block at the bottom (purpose · primary action · what changed and
why · spec claims). Everything on the screens is plain language, US English.

## What this package is

Spec 086's Point 5 makes the layered map the primary surface: system view →
claim view → evidence view, with the header carrying claims by status, the
validated-anchor share, and the nearest dated items, and every visual
element citing the ledger ids it renders. The map is the last layer of the
Winning Combination chain — ledger (Stage 1) → matrix (Stage 2) → gate
(Stage 3) → settling (Stage 4) → map (Stage 5) — and it is built only from
the gated, gated-published artifacts of the earlier stages. These wireframes
are the requirements for that build (tasks T502–T504 build and verify
against them).

The map renders the program's epistemic state, labeled as such. The Indus
script is not deciphered; nothing in these screens presents a settling
output as a reading of the script, and the settling surfaces carry the run
records' own label: "Establishes what the ledger implies under these rules,
not what the script says."

## Contents

| File | What it is |
|---|---|
| `wireframes/wireframes.css` | Shared wireframe stylesheet (the 081/085 package stylesheet, unchanged). |
| `wireframes/01-system-view.html` | L1 system view: the header strip, the ledger's sign inventory, matrix coverage, claim population, and the unresolved items — the program's gated state in one screen. |
| `wireframes/02-claim-view.html` | L2 claim view: one claim in full — statement, status, stage, falsifier, "this does not establish" line, displayed-score block, settling bearing, matrix row rendered. |
| `wireframes/03-evidence-view.html` | L3 evidence view: the column side behind one claim — documents, studies, anchors, research checks, corpus texts, each traced to its register record. |
| `wireframes/04-matrix-view.html` | The generated claims×evidence matrix as a grid, with the sign×sign block as a secondary form and claim×sign as a row filter. |
| `wireframes/05-settling-panel.html` | The settling panel: registered candidate runs, stored run records, the incumbent/challenger divergence view, the canonicals, and the rules' stated reach. |
| `wireframes/render-shots.py` | Render script (Playwright; desktop 1440 + mobile 390 screenshots into `wireframes/shots/`). |
| `decisions.md` | The open choices this package leaves to Tristen, each with the worker's recommendation: Q1–Q8. Approval is by name, on these questions. |
| `conformance.md` | How each wireframe satisfies spec.md Point 5(a)–(e) and claims C086-16/17/18/19, and what T502/T503/T504 will build and verify against these screens. |

## The decisions the owner is asked to make

Eight questions, in `decisions.md`, each with a recommendation. In short:

- **Q1** — the system view carries no graph canvas in v1 (the gated chain
  has no verified claim-graph edge set to draw). *Recommend: adopt as
  wired.*
- **Q2** — five screens, with the three levels as full views. *Recommend:
  adopt.*
- **Q3** — the header strip holds the spec's three items; falsifier
  coverage lives on the system view, not in the strip. *Recommend: as
  wired.*
- **Q4** — "nearest dated items" are the dated study-outcome blocks; the
  44 pending validations appear as a count (the register records no review
  dates). *Recommend: as wired*, or direct a register change as separate
  work.
- **Q5** — claim×sign is a row filter, not a matrix form. *Recommend: as
  wired.*
- **Q6** — the claim view's displayed-score slot is shown in its honest
  empty state today (no AEE state on any of the 840 claims), with the
  ScoringEngine-only labeling. *Recommend: as wired.*
- **Q7** — the settling panel opens on the stored T405 incumbent vs
  full-register comparison. *Recommend: as wired.*
- **Q8** — the matrix-defs vs glossa-settle-1 divergence over
  mahadevan:64/70/72 is named on the evidence view itself. *Recommend:
  named.*

Items that are **not** open questions, because an earlier approved act
decided them, are recorded in `conformance.md` §4 (085's reports-as-nodes
question, reversed by the approved Spec 086 D-086-Q1; 085's constraint
authorship, superseded by registered settling; the Spec 083 scoping and the
glassbreak-era membership perimeter, which apply to the map API exactly as
to every other surface).

## The numbers on the screens are the real ones

Every figure in the wireframes was computed from the merged tree at main
`2bac69cd` (2026-11-01): the ledger (871 lines, sha256 `c4e2326e…`, 840
claims: draft 816, untested 12, contradicted 4, partially supported 3,
strongly supported 2, partially falsified 1, unsupported 1, superseded 1;
falsifier coverage 831/840, the 9 gaps all in the extracted population); the
validated-anchor share (94 of 287 strict, 0.3275, gate V6); the matrix
(840 rows, 644 columns, 1,363 cells — supports 1,356, opposes 7, constrains
0; 14 named empty rows; 287 anchor and 31 research-check columns unused);
the anchors register (287 records: HIGH 166, MEDIUM 5, LOW 3, CANDIDATE 113;
94 strict, 44 pending); and the settling layer (assignment sets of record:
incumbent 94, full-register 286; the two stored T405 run records and their
comparison: 0 conflicts under both runs, 0 per-claim divergences, 192 signs
assigned by the full register only). Specimen claims are real claims
(parpola_2010_dravidian_solution_manual_002, yadav_2009_arxiv_manual_002,
farmer_sproat_witzel_2004_manual_001, without_kings…_manual_003), quoted
verbatim from the ledger.

## Renders

`render-shots.py` produces desktop (1440) and mobile (390) screenshots of
each screen into `wireframes/shots/`, the same way the 081 and 085 packages
were rendered. All 10 screenshots (5 screens × 2 widths) were produced for
this package and are in `wireframes/shots/`; the render outcome is also
recorded in the stage record (`stage-5-record.md`, T501 section).

## What approval unblocks, and what it does not

Approval of this package lets T502 build the map artifact
(`glossa-indus/map/map-data.json`, from the gated matrix, published only
through gated publication) and T503 build the surface against these screens,
with T504 verifying the built surface against them by Playwright capture at
both widths. Approval here does **not** approve any text for publication,
any change to the ledger, matrix, or settling layers, or the separate
owner rulings already on the program's list (the T201 matrix-defs v1 oracle
read; the mahadevan:64 resolution divergence as a definitions matter — Q8
covers only how visibly the evidence view names it).
