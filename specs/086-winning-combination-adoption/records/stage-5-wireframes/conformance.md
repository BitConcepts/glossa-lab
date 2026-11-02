# Spec 086, Stage 5 — conformance note (T501)

How the wireframes satisfy spec.md Point 5 and the Stage 5 claims, and what
the later Stage 5 tasks build and verify against them. The wireframes are
the requirements: any deviation found at T502/T503/T504 stops the step and
is reported; it is never absorbed silently.

## 1. Point 5, clause by clause

**Point 5(a) — the map is the primary surface, and every visual element
cites the ledger ids it renders.**
All five screens are one surface under a new "System graph" nav entry; the
three levels are its primary organization. Every card, table, and block on
every screen carries a "Cites:" line naming the exact ids behind it — the
ledger file and its hash, the claim ids, the matrix row and cell ids, the
run record ids, the register records (M064, M070, M072), the comparison
record and its hash. The citation lines are part of the design, not
decoration: T502's builder embeds the ids in the artifact, and the gate's
V5 class checks the embedded values against the ledger and registers.

**Point 5(b) — the header carries claims by status, validated-anchor
share, nearest dated items.**
The shared header strip renders all three, with the real current numbers:
claims by status (draft 816, untested 12, contradicted 4, partially
supported 3, strongly supported 2, partially falsified 1, unsupported 1,
superseded 1 — of 840); validated-anchor share (94 of 287 strict, 0.3275);
nearest dated items (the dated study-outcome blocks, nearest first:
2026-10-25 Spec 054; 2026-10-24 Specs 074 and 052). The gate's V2 and V6
header checks compare the artifact's header against the ledger and the
register, recomputed. Decisions Q3 and Q4 record the two design judgments
inside this clause (falsifier coverage's placement; what "dated items"
are).

**Point 5(c) — the system view.**
The inventory and coverage of the gated chain, composed from the same
artifact: the ledger's sign inventory (286 signs in the Mahadevan frame;
the corpus snapshot's totals; one register record out of frame, named);
matrix coverage (826 of 840 rows with cells; the 14 empty rows named by
id; 1,363 cells by relation and class; the two wholly unused column classes
stated); the claim population by stage and by source population, including
the 15 claims with no stage recorded, shown as a bare count (Spec 072's
contents are never an element of this surface — the register serves that
spec name-only, and 15 is a count, not a window); the unresolved items
(the 3 sign references with no matrix anchor record; the 14 prose sign
mentions, verbatim, on 5 claims); and the falsifier-gap census line. There
is no graph canvas in v1 (decision Q1).

**Point 5(d) — deeper levels behind each element: the claim view and the
evidence view.**
Every element on the upper levels opens its deeper level: a status segment
opens the claims behind it, a row opens the claim view, a cell opens its
citations, a sign opens its register record. The claim view shows the
claim's statement, status, stage, AEE state, falsifier, and "this does not
establish" line (all the ledger's values, verbatim), its matrix row
rendered including the explicit empty state, and its settling bearing under
both stored runs. The evidence view shows the column side: the
source-of-record document as provenance (never as a cell), the advisory
research-check annotation labeled advisory with its null verdict stated,
the anchor register records behind the claim's sign references with
confidence carried verbatim, and the registered matrix-defs vs
glossa-settle-1 divergence named on the screen (decision Q8).

**Point 5(e) — as-of stamps; staleness is shown, never hidden.**
Every screen carries the stamp line: the ledger hash and line count, the
ledger date, the definitions versions (ledger-schema v1, matrix-defs v1),
the artifact's build stamp, and a computed age line. The topbar chip shows
fresh or stale; a stale artifact renders with its STALE marking and the
reason (the gate is red, or the ledger advanced past the artifact's build).
The surface never recomputes a fresher number than the artifact carries —
a stale map is a labeled stale map (C086-18).

## 2. The Stage 5 claims, as designed

**C086-16 (displayed-score leg).** The claim view's displayed-score block
is the leg's designed discharge: scores display only as
`aee/scoring.py` ScoringEngine outputs over the ledger's relation set,
under that label, and settling outputs never display as scores. Today the
ledger's AEE state is null on all 840 claims, so the block renders its
honest empty state (decision Q6). The leg is *designed* here; it is
*established* only when T503 builds the surface and T504 verifies the
rendered block against this wireframe.

**C086-17 (the map renders generated data exactly).** The wireframes'
numbers are the artifact population's real numbers, computed from the
merged tree for this package; T502's builder produces the map artifact from
the gated matrix by the same rule (embedded values equal the ledger's —
gate V5), and T504 verifies the built surface against these screens.

**C086-18 (as-of stamps and staleness).** §1(e) above; the stamp line and
the stale marking are wired on every screen.

**C086-19 (Spec 083 scoping applies to the map).** The map API is a surface
like any other: responses are scoped to the signed-in member's workspaces,
contain no element whose underlying record is out of scope, and carry the
build stamp (T503's acceptance names the oracle: out-of-scope elements
absent from scoped responses, verified against the API, not the UI). The
wireframes show the signed-in shell and the service chip that carries the
build stamp; the scoping itself is an API property T503 builds and its
tests prove — there is nothing extra for the screens to draw, and nothing
in these screens weakens it.

## 3. What T502 / T503 / T504 build and verify against these screens

- **T502 (map builder)** builds `glossa-indus/map/map-data.json` from the
  gated matrix exactly as these screens compose it: the header strip's
  three items, the system view's cards (including the named empty rows, the
  unused classes, the unresolved lists, the falsifier census), the claim
  view's embedded fields, the evidence view's register traces, the settling
  panel's run records and comparison. Publication is gated publication
  only: a red gate leaves the published artifact byte-untouched.
- **T503 (surface)** builds the five screens in the app's stack against
  these wireframes, served from the gated artifact through the build-stamped,
  workspace-scoped API. Screen by screen, today's app changes as follows:
  a new "System graph" nav entry appears (today there is no such screen —
  the current app's 17 screens have no system graph; T503's "rebuilt" is
  against Spec 085's draft design, not against a shipped screen); all other
  screens are untouched by Stage 5.
- **T504 (verification)** renders the built surface with Playwright at
  desktop 1440 and mobile 390 and compares it screen-by-screen against
  these approved wireframes — layout, labels, numbers, citation lines,
  empty states, and the stale marking. Any deviation stops the step and is
  reported; the comparison record is filed with the stage record.

## 4. Superseded Spec 085 elements (decided upstream, recorded here)

- **085 Q1, reports as graph nodes** — reversed by the Spec 086 package's
  approved D-086-Q1: the layered map is generated data (ledger → matrix →
  map), and app entities such as reports are not map elements. The system
  view carries no report nodes.
- **085 Q3, constraint authorship in the UI** — superseded: the settling
  panel runs registered scenarios and assignment sets of record and authors
  nothing. (User-built anchor sets are excluded as settling contexts in v1
  by the approved Spec 086 §8 Q3; the panel states the exclusion where a
  reader would look for them.)
- **085's four constraint kinds and score-ceiling table** — belonged to the
  projected-constraint engine framing that Spec 086 superseded; the engine
  was never built, and its Experiment Builder stub was removed with a
  pointer at Stage 4 closeout (T406). The settling panel carries
  glossa-settle-1's rules (S-R1–S-R4) and C086-16's score rule instead.
- **085's claim×sign primary matrix form and heatmap shading** — superseded
  by the generated matrix's actual contents (no claim×sign cells exist);
  see decision Q5 and wireframe 04's annotation.
- **085's anchor-edge visuals** — dead under Stage 2's finding (anchors
  contribute zero matrix cells); the evidence view replaces them with
  register-record presentation.
