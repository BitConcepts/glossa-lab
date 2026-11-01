# Tasks: Winning-Combination Adoption (Spec 086)

Stages run **in the owner's order**: ledger intake validator →
matrix generator → verification gate → executable settling →
layered map. No stage starts before the previous stage's
acceptance gate passes. Every task names its claim(s), its
acceptance mode (**test** = automated check decides;
**human-as-oracle** = the owner or a named human judges;
**gate** = a recorded approval act must exist first), and a *this
does not establish* line that survives into the stage report
verbatim. **Every stage report carries the relevant gate's output
verbatim** (validator output, generator output, gate output,
test output) — not a summary of it.

## Stage 0 — package adoption (PR: `spec/086-winning-combination`)

- [x] T001 Spec package lands in `specs/086-winning-combination-adoption/`:
  spec.md, claims bundle, tasks.md, plan. Acceptance: test
  (documents present, internally consistent). *This does not
  establish that any part of the design is built or correct —
  only that the contract exists in the repo.*
- [x] T002 Claims normalized into `aee-claims.json` (C086-1…21)
  and verified under the pinned AEE (`aee validate` + `aee assess
  --no-ledger`), output recorded in the PR body. Acceptance:
  test. *This does not establish that the claims are true — only
  that they are well-formed and carry falsifiers.*
- [x] T003 LEDGER.md entry for the adoption, including the
  harmonization adoption record for
  `PATTERN-NOTE-2026-11-01-gate-and-settle`. Acceptance: test
  (entry present). *This does not establish anything about the
  system — it is the record that the contract was adopted.*

## Stage 1 — Ledger intake validator (PR: `feat/086-ledger-intake`)

- [x] T101 Ledger home + pinned schema: `glossa-indus/ledger/`
  with `claims.jsonl` (initially empty of claims), `SCHEMA.md`,
  and `ledger-schema.json` (`ledger-schema v1`). (C086-2)
  Acceptance: test — schema loads and validates a fixture entry.
  *This does not establish that the schema is the right one —
  only that it is pinned and enforceable.*
- [x] T102 The validator + intake module
  (`backend/glossa_lab/ledger_intake.py`,
  `tools/ledger/validate_ledger.py`): schema validation;
  proposition-fingerprint recomputation and duplicate refusal
  reusing `proposition_fingerprint.py` under its frozen rules
  (D-B); field-provenance checks (falsifier / does-not-establish /
  explanation fields must trace to a source or a named
  human-authored record — C086-5, C086-6); append via the
  verified-write path with read-back hash. Acceptance: test —
  teeth fixtures: a malformed entry, a duplicate-fingerprint
  entry, and an authorless-explanation entry are each refused
  loudly and nothing is written. *This does not establish that
  honest entries are true — only that unprovenanced ones cannot
  enter quietly.*
- [x] T103 Intake routes wired: extraction intake gains the
  ledger append as its final step; the bundle import tool
  (freeze/adjudication events); the research-check annotation
  intake (sidecars stay advisory; annotation entries only);
  the discovery promotion path (named human act; candidates
  marked). (C086-1) Acceptance: test — one fixture through each
  route, each producing exactly the specified entry kind.
  *This does not establish that future real intake will be
  clean — only that the four doors exist and are the only ones
  the code provides.*
- [x] T104 Migrations, one gated run per population: P1
  (extracted claims, 31), P3 annotations (research checks, 31),
  then P2 (spec bundles; the census's 1,592 records reconciled
  by (spec, claim) — the double-format question answered by the
  report, not assumed). Each run emits its reconciliation
  report: counts in == out per claim id; fingerprint collisions
  listed; mirrored status/stage byte-equal to source;
  falsifier and does-not-establish coverage counted.
  (C086-4, C086-5, C086-20) Acceptance: test + gate — reports
  reconcile exactly; any mismatch stops the stage and is
  reported, not repaired in flight. *This does not establish
  that the migrated claims are correct — only that the ledger
  mirrors the record without loss or invention.*
- [x] T105 Stage 1 closeout: validator output over the migrated
  ledger and both reconciliation reports filed verbatim in the
  stage record; the D-A-generalization pattern note (pinned
  schema + CI validator for a program ledger) written and
  delivered to the RCPH and Atlas chats. (C086-21) Acceptance:
  gate (stage record complete). *This does not establish the
  matrix will be right — only that what it will be generated
  from is now one validated artifact.*

## Stage 2 — Matrix generator (PR: `feat/086-matrix-generator`)

- [x] T201 Registered definitions: `glossa-indus/matrix/
  DEFINITIONS.md` (`matrix-defs v1`) — column classes, the
  supports/opposes/constrains derivation rules, the evidence
  registers named — with machine copies registered in the
  generator (the gate's copies arrive with Stage 3).
  Acceptance: human-as-oracle — the owner or a named reviewer
  reads the definitions as the contract they are. *This does
  not establish the definitions are the right semantics — it
  establishes they are written down, versioned, and the only
  ones the generator may use.*
- [x] T202 The generator (`backend/glossa_lab/matrix_generate.py`,
  invoked as `tools/ledger/generate_matrix.py`): reads only the
  ledger + referenced registers; writes `matrix.json` +
  `matrix.md` with per-cell relation, citation ids, derivation
  rule id; emits the coverage block (empty rows, unused columns,
  falsifier coverage, unresolved sign mentions); imports the
  sign×sign block from the existing co-occurrence pipeline
  output for the same corpus snapshot. (C086-7, C086-8)
  Acceptance: test — delete-and-regenerate byte-identity;
  sampled cells traced to their cited ledger entries. *This
  does not establish that the underlying relations are true —
  only that the matrix is the ledger, in matrix form.*
- [x] T203 Stage 2 closeout: generator output + coverage block
  filed verbatim. Acceptance: gate. *This does not establish
  the matrix is verified — Stage 3 exists because generation
  alone proves nothing about itself.*

## Stage 3 — Verification gate (PR: `feat/086-ledger-gate`)

- [x] T301 The gate (`tools/ledger/check_ledger_gate.py`) with
  check classes V1–V7 and V9 of spec.md Point 4 (V8 arrives
  with Stage 4), including the **relation-carrying citation
  class (V4)** with tie rules T1–T4 adapted to Glossa's edge
  types, and the gate's own registered copies of the matrix
  definitions (independent recomputation route). (C086-9,
  C086-10) Acceptance: test — the gate passes a clean tree and
  its output enumerates every check by name. *This does not
  establish the gate catches everything — it establishes the
  named classes are checked mechanically, and the teeth tests
  below bound what "catches" means.*
- [x] T302 `--regen` mode: hash, regenerate, byte-compare,
  classify any diff as intended-change-named or
  downstream-defect. (C086-12) Acceptance: test — regen over a
  clean tree is byte-identical; regen over a hand-edited
  artifact names that file as the defect. *This does not
  establish the artifacts are substantively right — only that
  they are exactly what the ledger generates.*
- [x] T303 Gated publication wiring: generator and map builder
  write candidates; the gate runs against candidates
  (`--candidate`); published files are replaced only on ALL
  PASS (Atlas `build_graph.py` publish block is the reference
  shape). (C086-11) Acceptance: test + negative control — in a
  scratch tree, a flipped ledger status with a stale matrix
  makes publication refuse, name the diverged checks, and
  leave the published artifact byte-identical to its pre-run
  hash. *This does not establish the published content is true
  — it establishes nothing unverified replaces it.*
- [x] T304 Teeth battery: one seeded divergence per check
  class, each required to turn the gate red and name its
  check — including the Atlas failure mode as a first-class
  case: a citation that exists and is relevant but carries no
  relation (Spec 054's UNEXECUTED closure cited as support)
  must fail V4 while passing V1–V3. (C086-9) Acceptance: test
  — battery output filed verbatim in the stage record.
  *This does not establish immunity to unseeded failure modes
  — it establishes the named modes are caught, and names the
  battery as the standing place to add new ones.*
- [x] T305 CI wiring: job `ledger-gate` in
  `.github/workflows/ci.yml` beside `freeze-gate` (C4
  untouched): `--pr-scope` on PRs, full mode on pushes,
  `--regen` in the push job. (C086-10) Acceptance: test — the
  job runs green on the adopting PR and red on a seeded-
  divergence PR. *This does not establish future PRs will be
  honest — it establishes the gate stands in the merge path.*
- [x] T306 Stage 3 closeout: clean-tree gate output, regen
  output, teeth-battery output, and the negative-control record
  filed verbatim; the falsifier-gap census pattern note
  written and delivered to the RCPH and Atlas chats.
  (C086-21) Acceptance: gate. *This does not establish the
  chain is true — it establishes the chain is now guarded:
  what ships is what the ledger generates, or nothing ships.*

## Stage 4 — Executable settling (PRs: `feat/086-settling-semantics`, then `feat/086-settling-engine`)

- [ ] T401 **Semantics registration FIRST** (its own PR; no
  engine code in it): `glossa-indus/ledger/SETTLING-SEMANTICS.md`
  at `glossa-settle-1` — rules S-R1…S-R4 and the forced-
  consequence definition, derived from Glossa's own ledger
  (D-A tiers; the Spec 073/074 frozen-surface precedent). The
  document states expressly that the Atlas's settle-1 constants
  are not lifted. Acceptance: human-as-oracle — the semantics
  are the contract; the owner or a named reviewer reads them
  as such. *This does not establish the rules are the right
  rules — each carries its grounding so a reviewer can
  disagree in the open.*
- [ ] T402 **Canonical scenarios derived by hand** (same PR as
  T401 or its immediate successor; still no engine):
  `glossa-indus/ledger/settling-canonical.json` with at least
  the four scenarios of spec.md Point 3, each with its prose
  derivation beside the expected output. Acceptance:
  human-as-oracle — the derivations are the review surface.
  *This does not establish the derivations are error-free —
  it establishes they exist in prose, where an error can be
  found by reading, before any code depends on them.*
- [ ] T403 The engine (`backend/glossa_lab/settling.py`):
  evaluates an assignment-set record over one ledger build;
  writes run records only; imports no intake/write module.
  Assignment sets of record registered: incumbent (strict-94)
  and full-register (287), each as a stored record with
  provenance. (C086-14, C086-16) Acceptance: test — store-hash
  diff across a run is empty outside the run store; the V9
  import audit passes. *This does not establish the engine is
  correct — that is T404's bar, not this task's.*
- [ ] T404 **Exact-reproduction test**
  (`backend/tests/test_settling_canonical.py`): the engine
  reproduces every registered canonical exactly — counts,
  enumerations, tallies. Wired into the gate as check V8.
  (C086-13) Acceptance: test — test output filed verbatim; a
  mismatch is fixed in the open (engine or derivation), never
  by quietly editing expectations. *This does not establish
  the semantics are true — it establishes the engine is the
  semantics, mechanically.*
- [ ] T405 First interchangeability run: incumbent vs
  full-register over the same ledger build + corpus snapshot;
  both run records stored; the per-claim divergence list
  emitted, naming pre-registered expectations for touched
  claims (Spec 074's outcome record among them) with
  agreement/divergence scored against each. (C086-15)
  Acceptance: test (input hashes equal across run records) +
  human-as-oracle (the divergence list is readable as a
  research artifact). *This does not establish either reading
  — it establishes exactly where they diverge, claim by claim,
  which is the thing narration cannot do.*
- [ ] T406 The stub's disposition: the Experiment Builder
  constraint-projection node is wired to the settling service
  or removed from the palette with a pointer (Spec 085
  C085-15, carried in). Acceptance: test — node invocation in
  a wired graph returns a well-formed run reference; the
  "engine removed" error is unreachable. *This does not
  establish experiment authors should settle inside pipelines
  — only that the named capability is no longer a trap.*
- [ ] T407 Stage 4 closeout: canonical reproduction output,
  the first dual-run divergence list, and both run records
  filed verbatim. Acceptance: gate. *This does not establish
  any decipherment consequence — settling outputs are
  computations over ledgered relations, labeled as such, and
  enter the research record only through intake.*

## Stage 5 — Layered map (PR: `feat/086-layered-map`)

- [ ] T501 **Wireframes first (gate):** Spec 085's three
  screens conformed to this spec — header strip (claims by
  status; validated-anchor share; nearest dated items);
  every element citing its ledger ids; matrix view's primary
  form = claims×evidence with claim×sign as a column-class
  filter; projection panel → settling panel with the
  incumbent/challenger divergence view. Presented for the
  owner's approval **by name** before any surface code.
  Acceptance: gate (owner approval act on the actual screens).
  *This does not establish the built screens will match —
  that is T504's comparison.*
- [ ] T502 Map builder: generates `glossa-indus/map/
  map-data.json` from the gated matrix (system/claim/evidence
  view data; header state computed, never typed), published
  only through Stage 3's gated publication. (C086-17, C086-18)
  Acceptance: test — gate V5/V6 pass against the candidate;
  builder output filed. *This does not establish the surface
  renders it faithfully — that is T503/T504.*
- [ ] T503 The surface: the System graph screen rebuilt on the
  gated artifact + build-stamped API responses; scoping per
  Spec 083 (C086-19); staleness shown from the as-of stamp
  (C086-18). Acceptance: test + human-as-oracle — rendered
  counts compared against the artifact by automated capture,
  and the owner's read against the approved wireframes.
  *This does not establish the picture is easy to understand
  for anyone else — only that it is faithful, gated, and was
  approved as legible by the oracle named.*
- [ ] T504 Verification: Playwright screenshots at desktop
  1440 and mobile 390 compared screen-by-screen against the
  approved wireframes; any deviation stops the step and is
  reported, not improvised around (Spec 081/083 precedent).
  Acceptance: gate — comparison record filed, gate output for
  the shipped artifact filed verbatim with it. *This does not
  establish behavior beyond the rendered states compared.*
- [ ] T505 Closeout: the audit's six gap items re-scored
  against the built chain (ledger → matrix → gate → settling →
  map) and the re-score filed; LEDGER.md entry; any pattern
  improvement found in this stage written up and delivered
  under C086-21. Acceptance: test (records present) +
  human-as-oracle (owner reads the re-score). *This does not
  establish the owner's sentence now holds in spirit — it
  establishes the evidence on which he can judge it.*
