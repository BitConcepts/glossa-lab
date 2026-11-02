# T504 — Playwright comparison: built surface vs the approved wireframes

Date: 2026-11-02. Builder: the Stage 5 build worker (this PR).
Method: the backend was started the way CI starts it
(`GLOSSA_DATA_DIR=<tmp> GLOSSA_DEV_MODE=1
GLOSSA_API_TOKEN=ci-e2e-token`, uvicorn on 127.0.0.1:8001)
serving the production frontend build (`npm run build`). Shots
were taken with `render-shots.py` (alongside this file) at
desktop 1440 wide and mobile 390 wide, the viewport grown to
each screen's full content height; the shots are in `shots/`
next to this file and are the final build's. The approved
renders compared against are
`records/stage-5-wireframes/wireframes/shots/`.

## Served-identity check

Before any shot, the script asserts the stamp line on the
served surface reads "map data · ledger c4e2326e… · fresh" —
the published artifact's ledger hash, a marker only the new
build carries. Both viewports printed:

```
[desktop] served stamp: map data · ledger c4e2326e… · fresh
[mobile]  served stamp: map data · ledger c4e2326e… · fresh
```

## Per-screen results

- **01 System view — match, with named differences D1–D4
  below.** Header strip (840 claims, status line, 44 pending,
  the three nearest dated items), standing-position callout,
  and all five cards render with the artifact's values: 286
  signs in frame, H003 out of frame, incumbent 94 of 286,
  1,363 cells, the 7 opposes cells named, 14 empty rows, the
  falsifier census 831 of 840 with the extracted/bundle split,
  AEE state null on 840 of 840, 14 unresolved mentions plus
  the 3 sign_refs under the matrix's key, the sign×sign block
  (1,631 edges, 200 emitted, 80 nodes).
- **02 Claim view — match.** The specimen claim's statement
  verbatim; chips in ledger order (sign_refs mahadevan:72 ·
  64 · 70); falsifier verbatim with "1 present · 0 evaluable";
  "This does not establish" in full; both settling-bearing
  runs with via signs and tallies; the displayed-score slot in
  its empty state under the Q6 label; the empty matrix row
  with the yadav contrast inset (supports on yadav_2010_ngrams
  R1 — the artifact's rule for that cell; opposes on study 054
  R3 with both appends cited).
- **03 Evidence view — match, with named difference D3.** The
  five column-class minis (316/10/287/31/0 columns, 0 cells,
  each empty class's note); source of record with its hash;
  the claim's own research check (26 nearest neighbours, 1
  gap, verdict none recorded, the audit protocol, the sidecar
  and its hash); the sign-references table in both layers'
  keys (M64/M70/M72 unresolved; M064 va, M070 vēl, M072 mā,
  strict only on M070) and the Q8 divergence callout.
- **04 Matrix view — match.** Form and class chips with the
  artifact's counts; relations as words in the specimen grid
  (opposes on study 055 for the first row, supports on the
  document columns, empty rows labeled); aggregated unused
  classes; the selected-cell callout for yadav × study 054
  (opposes, R3, both appends cited, governing labeled); the
  empty-row callout naming the 14; the sign row-filter chip
  (1 claim, its three sign_refs). "Showing 6 of 840 rows."
- **05 Settling panel — match.** The run records' label
  verbatim as the lede; the computed-layer callout; run
  inputs (both assignment sets, scope 286, the Q3 exclusion
  stated, the pins callout); the five canonical scenarios
  with their expected results, including the seeded conflict
  named (mahadevan:70, M070, ka ≠ vēl); the stored-runs table
  (94/94/94/94/0/1.00/0 and 286/286/94/94/192/0/1.00/0) with
  the pins line; the divergence view (1 compared, 0
  divergent, deltas 94 → 286, 192 signs full-register only,
  the absence statement verbatim); the reach card with S-R3
  UNMEASURED and 839 of 840 untouched.

## Named differences (data governs in every case)

- **D1 — the header's validated share reads 32.8%, the
  wireframe's strip says 32.9%.** The header contract's value
  is the strict share over the 287 register records
  (94/287 = 0.3275…, 32.8% at one decimal), recomputed by the
  gate's V6 leg. The wireframe's 32.9% is the share over the
  286-sign frame (94/286), which is the figure the sign
  inventory card shows for the incumbent set's coverage. The
  surface renders the artifact's header value exactly
  (C086-17); the wireframe paired the frame share with the
  register count.
- **D2 — unresolved mentions sit on 6 claims, not 5.**
  conformance.md §1(c) says 5; the ledger's population is 6
  (the mentions group and the sign_refs group together). The
  built card counts the artifact's population.
- **D3 — the research-check line shows the claim's own
  check.** The wireframe's specimen line combined the two
  checks recorded against the parpola *document* ("24–26
  nearest neighbours across two checks"); the artifact
  carries the annotation recorded against this *claim*
  (26 neighbours, 1 gap), and the surface renders that.
- **D4 — within-date ordering of the nearest dated items.**
  On 2026-10-24 the built strip lists study 052 before study
  074 (the registered rule: date descending, then study
  ascending); the wireframe's strip lists 074 first. The
  groups and counts are identical.
- **D5 — the signary sizes (557 / 527 / 584) are surface
  copy.** They appear in the approved wireframe's sign
  inventory callout and are rendered as that approved copy;
  no machine-readable source for them exists in the gated
  chain, and the artifact carries only register-derived
  inventory numbers. Recorded as a judgment in the stage
  record.

## Defects found and fixed in this PR

- Long claim ids and paths overflowed three cards (matrix
  coverage hotspots, unresolved mentions, research-check
  sidecar): wrap rules added; re-rendered.
- Stage rows rendered in the artifact's alphabetical order;
  they now render in the ladder's order (created, explained,
  checked) as the wireframe draws them. Values unchanged.
- The seeded-conflict scenario's conflict is now named on
  the settling panel (sign, anchor, assigned ≠ reading), as
  the wireframe shows it.

## E2E

`frontend/e2e/system-graph.spec.ts` (new, 3 tests) passes
against the same server, as do the navigation, program-home
and Spec 029 guard suites (42 tests) — the Spec 029 guard
testids on the program home are untouched, and the new
surface's own testids are distinct (`indus-map-header`,
`indus-map-stamp`, `indus-map-standing-position`).
