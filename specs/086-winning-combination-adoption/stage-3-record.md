# Spec 086 — Stage 3 record: the verification gate (T301–T306)

Date: 2026-11-01. Branch: `feat/086-ledger-gate` (off main
`cb055a15`, the Stage 2 merge). This record is the Stage 3
closeout required by T306: the clean-tree gate output, the
regen output, the teeth-battery output, and the
negative-control record are filed verbatim (in the body
below and in `records/`), with the claim assessments for
the Stage 3-scope claims. Standing position, unchanged by
anything in this stage: **the Indus script is not
deciphered**; the gate verifies that the generated layers
are what the ledger generates — it says nothing about
whether any claim in the ledger is true.

## What was built

- `backend/glossa_lab/ledger_gate.py` — the gate library:
  check classes V1–V7 and V9 of spec.md Point 4 (V8 is
  enumerated NOT-RUN; it arrives with Stage 4), the gate's
  **own registered copies** of the matrix definitions
  (an independent recomputation route — the module does
  not import the generator's definition tables), V4's tie
  rules T1–T4 adapted to Glossa's edge types plus the
  numeric arm, and the V9 import/census audits. The gate
  contains no write path.
- `tools/ledger/check_ledger_gate.py` — the CLI: full
  mode, `--pr-scope --base REF`, `--regen`,
  `--candidate`, `--candidate-map`, `--intended-change`.
  It sets `sys.dont_write_bytecode = True` before any
  backend module is imported.
- `backend/glossa_lab/gated_publish.py` +
  `tools/ledger/generate_matrix.py --gated` — gated
  publication (T303): candidate → gate → atomic replace
  only on ALL PASS.
- `backend/tests/test_spec086_ledger_gate.py` — 19 tests:
  the teeth battery, the write-freedom proof, the gated
  publication controls, the numeric-arm fixtures.
- `.github/workflows/ci.yml` — job `ledger-gate` beside
  `freeze-gate` (C4 untouched): machinery tests, then
  `--pr-scope` on PRs, full mode + `--regen` on pushes.
- `glossa-indus/ledger/SCHEMA.md` — one added paragraph:
  the explicit declared-type sentence required by the
  2026-11-01 layer-scoped-duplicates ruling (see the
  harmonization section below).
- Records: `records/stage-3-gate-output.txt`,
  `records/stage-3-regen-output.txt`,
  `records/stage-3-teeth-output.txt`,
  `records/stage-3-negative-control.txt`,
  `records/pattern-note-falsifier-gap-census.md`,
  `records/harmonization-2026-11-01.md`.

## Registered readings (the choices that carry weight)

1. **V1's source-hash arm covers every entry.** spec.md
   Point 4 V1 names "migration entries' source hashes";
   the gate verifies **all 1,686** recorded hashes (every
   `sources[]` item of every entry, plus annotation
   sidecars) against the canonical helper
   `ledger_intake.sha256_file`. This closes the Stage 1
   gap directly: no Stage 1 check compared the recorded
   hashes to the files. On the clean tree all 1,686
   verify.
2. **Map-dependent legs are enumerated NOT-RUN, never
   skipped silently.** No map artifact exists until
   Stage 5, so V2's map-header leg, V5, and V6's
   map-header leg print NOT-RUN with the reason on every
   run — every check is named, per T301's acceptance.
   When a candidate map is supplied (`--candidate-map`),
   those legs run. The gate thereby registers the
   candidate-map contract Stage 5's builder must emit:
   `header {claims_by_status, validated_anchor_share,
   strict_anchor_share, as_of.ledger_sha256}`,
   `elements [{id, kind, …embedded ledger fields}]`,
   `edges [{from, to, rel, citations}]`, and a `loads`
   block deep-equal to the matrix's per-row relation
   tallies (V5's "loads block deep-equals the matrix's").
3. **T2's tie is the governing block.** A study citation
   ties only if the study's governing stored outcome
   block for the claim (latest dated, the gate's own
   ordering) is among the cited pointers **and** its
   outcome maps to the asserted relation under the gate's
   outcome-table copy. A superseded or non-bearing block
   cited alone carries no relation — that is the Atlas
   failure mode, mechanized. Production R3 cells cite all
   blocks, so the governing block is always among them.
4. **T304's Atlas case is seeded at the candidate-map
   layer.** At the matrix layer, any hand-seeded citation
   or relation divergence is also a V3 divergence by
   construction (V3 recomputes citations cell-for-cell),
   so "fails V4 while passing V1–V3" is only producible
   where citations are authored downstream of the
   recomputed layer — the map, which is where the Atlas's
   own failure lived. The battery therefore seeds the
   miscarriage as a candidate-map edge over the clean
   tree: V1, V2, V3, V5, V6 PASS in the same run; V4
   FAILs, naming the citation and the governing block it
   failed to carry.
5. **T303's negative control presents the stale matrix
   as the candidate.** A candidate freshly built from a
   flipped ledger is self-consistent by construction (the
   ledger is the source of truth; the gate checks chain
   consistency, not ledger editorial acts — those are
   intake's and git's discipline). The control therefore
   exercises the publish decision the spec names — a
   builder's candidate presented to the gate ("locally
   and in the app bundle, the same candidate → gate →
   replace mechanics apply"): flipped ledger status +
   the pre-flip published bytes as candidate → the gate
   refuses, naming V2 and V3, and the published artifacts
   stay byte-identical. `gated_publish.publish_matrix`
   accepts both candidate sources (fresh build, or a
   presented candidate directory) so the mechanics are
   one code path.
6. **T305's red-on-a-seeded-divergence-PR acceptance is
   met by construction + battery, recorded plainly.** The
   `ledger-gate` CI job runs the teeth battery as its
   machinery-test step on every PR — a seeded divergence
   in any class turns that step red — and runs the gate
   itself in PR scope. A deliberately red PR was not
   opened against the shared repo to prove the wiring a
   second time; the battery is the standing proof, and it
   runs in the job.
7. **The numeric arm's live population is unexercised —
   stated, not papered over.** No live citation carries
   a measurement with a machine-readable bound (the
   ledger holds zero `measurement` entries, Stage 2
   minted none, and `ledger-schema v1` carries no bound
   field on claim entries). V4 prints that fact on every
   run. The battery exercises the arm on fixtures: a
   supports citation whose value violates the bound is
   refused, and the symmetric opposes case, both directly
   and through the V4 evaluator.
8. **V6's validated share is the strict share**, per
   spec.md Point 5(c)'s own gloss ("validated-anchor
   share (strict share, V6)"): the strict set recomputes
   under the rule the anchors file itself records
   (`strict_sa_independent_hm`, Phase-109 follow-through
   applying the Phase-108 definition, read against
   `reports/phase108_provenance_register.json`) — 94 of
   287, share 0.3275 — and equals the stored `strict_set`
   flags and the recorded count.
9. **V9's writer census scope** is the production trees
   (`backend/glossa_lab`, `backend/scripts`, `tools`):
   modules that both reference a gated-artifact path and
   contain a write call must be registered writers.
   Test code is out of the census — it writes fixtures
   under tmp dirs by design and is not a publication
   path. The census finds exactly the two registered
   writers: `matrix_generate.py` (the thin wrapper) and
   `gated_publish.py`.
10. **Battery scratch trees symlink the read-only
    registers.** /tmp on this machine class is a 512 MB
    tmpfs; full per-test copies of the chain's inputs
    (corpus 9.7 MB + sources 8.6 MB) filled it during
    development. Files a test can mutate (ledger, matrix
    artifacts, anchors) are real copies; the rest are
    symlinks the battery never writes through. Recorded
    here because the first battery run's disk-full
    failure was this stage's, and the fix is part of the
    test design.

## Clean-tree gate output (verbatim; also filed at `records/stage-3-gate-output.txt`)

```text
Ledger gate — glossa-indus chain (Spec 086, Point 4)
mode: full
root: /home/hatch/workspace/glossa-run/spec086-stage3
ledger: glossa-indus/ledger/claims.jsonl — 871 lines, canonical sha256 c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf
definitions: matrix-defs v1 (the gate's registered copies); ledger schema: ledger-schema v1
falsifier coverage: 831 of 840 claim entries carry a falsifier (published on every gate run, C086-5) — by population: bundle 817/817, extracted 14/23
checks:
PASS V1 ledger validity — pinned schema, fingerprints (spec029-phase-i-v1), D-B uniqueness, field provenance, pointers (Stage 1 validator)
  871 lines validate against ledger-schema v1; every fingerprint recomputes; no duplicates
PASS V1 recorded source hashes — every sources[] and sidecar hash verifies (canonical hash)
  1686 recorded hashes verified against the files on disk via ledger_intake.sha256_file
PASS V2 count equivalence — claims by status: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by stage: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by population: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — falsifier coverage block: ledger == matrix
  matrix carries {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}; recomputed {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}
NOT-RUN V2 count equivalence — map header leg
  no map artifact (the map is Stage 5) and no --candidate-map supplied
PASS V3 matrix recomputation — cells cell-for-cell (relation, citation ids, derivation rule id)
  1363 cells recomputed from the ledger by the gate's own route; every cell equal
PASS V3 matrix recomputation — rows, columns, coverage, as-of stamp, sign×sign block
  rows, columns, coverage, the as-of stamp and the sign×sign block all equal the gate's recomputation
PASS V4 relation-carrying citations — every citation ties under T1–T4 (incl. the numeric arm)
  1363 matrix cells and 0 map edges checked; 1364 citations required to carry their relation under T1–T4
  numeric arm: 0 citations in the live population carry a measurement with a machine-readable bound (the arm is exercised on fixtures in the teeth battery)
NOT-RUN V5 map recomputation
  no map artifact (the map is Stage 5) and no --candidate-map supplied
PASS V6 anchor shares — strict set recomputes under the recorded D-A rule (strict_sa_independent_hm)
  strict anchors: 94 of 287; strict share 0.3275; validated-anchor share (the strict share, spec.md Point 5) 0.3275; rule version as recorded: Phase-109 follow-through (spec 007, 2026-10-06) applying the Phase-108 strict definition
NOT-RUN V6 anchor shares — map header leg
  no map artifact (Stage 5) and no --candidate-map supplied
NOT-RUN V7 lossless regeneration
  runs under --regen (the push CI job runs it)
NOT-RUN V8 settling canonicals
  arrives with Stage 4 (the settling engine)
PASS V9 no write path — gate import hygiene
  the gate modules import no write entry point (append_entry, write_ledger, write_matrix) and contain no write call
PASS V9 no write path — settling/scenario import audit
  no settling/scenario package exists yet (Stage 4); the audit is armed and scans for one on every run
PASS V9 no write path — matrix/map writer census
  writers of the gated artifacts: ['backend/glossa_lab/gated_publish.py', 'backend/glossa_lab/matrix_generate.py']
  readers (no write call): 3 module(s)
  census scope: backend/glossa_lab, backend/scripts, tools (test code writes fixtures under tmp dirs by design and is not a publication path)
summary: 13 PASS / 0 FAIL / 5 NOT-RUN
RESULT: PASS
```

## Regen output (T302; full text filed at `records/stage-3-regen-output.txt`)

The `--regen` run: 15 PASS / 0 FAIL / 5 NOT-RUN, RESULT
PASS. Its V7 lines, verbatim:

```text
PASS V7 lossless regeneration — matrix.json
  byte-identical after regeneration (sha256 b3cdbf49e6305ae771468f26858678db568d1b58cb0b200e55b92810adb29849)
PASS V7 lossless regeneration — matrix.md
  byte-identical after regeneration (sha256 7c963ff55c38d4dc9a52d240dacb03da0f2eebfaff5411cc398144727140b255)
NOT-RUN V7 lossless regeneration — map data
  no map artifact exists (Stage 5)
```

(The hashes above are the artifacts' canonical hashes as
printed by the filed run; the byte-compare itself is over
raw bytes.)

## Teeth battery (T304; full output filed at `records/stage-3-teeth-output.txt`)

19 tests, all passing. Case by case:

| Case | Seeded divergence | Required result |
|---|---|---|
| V1 | one `sources[]` sha256 in the ledger replaced with zeros | V1 recorded-source-hash arm FAILs, naming the entry's file |
| V2 | one matrix row's status flipped in matrix.json | V2 by-status FAILs |
| V3 | the Yadav × 054 cell's relation flipped to supports in matrix.json | V3 cells FAILs, naming the cell |
| V4 (Atlas case) | candidate-map edge citing Spec 054's 2026-10-24 closure (`STRICT CORPUS NOT PINNABLE` — the test did not execute; the task text's "UNEXECUTED closure") as **supports** for the Yadav claim | V4 FAILs naming the pointer, the outcome, and the governing 2026-10-25 block; **V1–V3 PASS in the same run** (also V5, V6) |
| V4 (positive control) | edges citing the governing 2026-10-25 `NOT SUPPORTED` block as opposes, and the stored evidence instance as supports | V4 PASSes |
| V5 | a candidate-map element's embedded status altered | V5 FAILs naming the element |
| V6 | one anchor's stored `strict_set` flag flipped | V6 FAILs (recomputation disagrees with the stored flags) |
| V7 | matrix.md hand-edited by one appended line | V7 FAILs, classifying the diff **downstream-defect** and naming the file; the same diff with `--intended-change` classifies **intended-change-named** and matrix.json stays byte-identical |
| V9 (settling audit) | a `settling_fixture.py` importing `append_entry` | V9 settling/scenario audit FAILs naming the module |
| V9 (census) | a module writing to a gated-artifact path | V9 writer census FAILs naming it |
| Numeric arm | fixture measurement value 0.87 against bound `<= 0.8`, cited as supports; and the symmetric opposes case | arm refuses both; conforming pairs pass — directly and through the V4 evaluator |
| Write-freedom | a red gate run over a seeded scratch tree | published matrix artifacts byte-identical before/after |
| Gated publication | clean tree / stale-candidate negative control | publishes on pass; refuses on red (next section) |

*This does not establish immunity to unseeded failure
modes — it establishes the named modes are caught, and
names the battery as the standing place to add new ones.*
(tasks.md T304, carried verbatim.)

## Negative control + write-freedom proof (filed verbatim at `records/stage-3-negative-control.txt`)

Seed: ledger status of `yadav_2009_arxiv_manual_002`
flipped; the pre-flip published bytes presented as the
candidate. The gate over the candidate FAILs
`V2 count equivalence — claims by status` and
`V3 matrix recomputation — rows, columns, coverage,
as-of stamp, sign×sign block`; publication is refused
(`published: False`); the published artifacts after the
run are byte-identical to their pre-run hashes
(matrix.json `b3cdbf49…`, matrix.md `7c963ff5…`); the
staging directory is removed. A direct red gate run over
the same seeded tree likewise leaves both artifacts
byte-identical — Amendment 1 corollary 5, tested, not
asserted. The clean-tree publish control replaces the
artifacts only after ALL PASS and verifies the read-back
bytes against the gated candidate bytes.

## Harmonization entries (full text: `records/harmonization-2026-11-01.md`)

Recorded this stage, all dated 2026-11-01: **(a)** the
Breaking-Point Atlas adopted Glossa's T105 pattern note
(schema v1 beside their ledger from a 541-entry census;
SCHEMA check class; falsifier coverage 541/541 published
per run; gate 206/207 PASS, no check loosened; four
seeded failure controls caught). **(b)** Tristen
**ratified** the T105 note as **Amendment 3** to the
canonical pattern note ("Pin the ledger's schema and
gate it in CI", commit `4e1ff09`) — the generalized D-A
naming is canonical, decided, not pending. **(c)** RCPH
recorded its own adoption the same day (44 entries, 3
field shapes, no falsifier field, no pinned schema,
parse-only CI; schema + validator build queued there).
**(d)** **Amendment 2** (canonicalize-before-you-hash,
from Spec-Kit AEE) was **ratified** by Tristen the same
day (canonical note commit `d1de85d`); Glossa's
conformance stands as adopted — the canonical helper in
force since Stage 1, pinned-LF byte-compared artifacts,
root `.gitattributes` already `eol=lf`, the
write-freedom corollary implemented by this stage's gate
tests — and the framework026 freeze pins are **not**
migrated (a different historical regime; no conflict).
**(e)** The **layer-scoped duplicates ruling** (commit
`3bcd1fd`): Glossa's ledger is a claim ledger, D-B
refusal already the validator's teeth-tested behavior
(unchanged); the explicit declared-type sentence was
added at the head of `glossa-indus/ledger/SCHEMA.md`
after verifying no hash pin or test covers that file's
bytes; Glossa operates no assertion/evidence ledger in
v1, so the ruling's branch (2) has no Glossa surface.

## The falsifier-gap census pattern note (T306)

Written: `records/pattern-note-falsifier-gap-census.md`.
**Delivery to the RCPH and Atlas chats is owed** — as
with T105, delivery is the parent chat's act; this record
flags it rather than claiming it. *This does not
establish that the chain is true — it establishes the
chain is now guarded: what ships is what the ledger
generates, or nothing ships.* (tasks.md T306, carried
verbatim.)

## Test evidence

- Teeth battery + gate tests: **19 passed**
  (`test_spec086_ledger_gate.py`; filed verbatim).
- Spec 086 family + Spec 029 freeze + Spec 086 matrix /
  intake / migration: **64 passed** in one run.
- Spec 084 conformance (`test_policy_sync_conformance.py`):
  **8 passed**.
- Freeze family (`-k freeze`, whole suite selection):
  **263 passed, 1 skipped** — the established count.
- Full backend run (no `-x`, GPU tests ignored as in CI):
  **1 failed, 2218 passed, 14 skipped in 2,433 s.** The
  one failure is
  `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
  — the pre-established environmental failure (the test's
  missing-download precondition), not this stage's: it
  was identified by ordinal position in the run's output
  and confirmed in the run's summary. `test_auth_consumers`
  (the known quiet-window passer) passed in this run. The
  run's in-tree rewrites of the extracted-claims files
  (the pre-existing `test_indus_evidence_api.py` behavior)
  were restored before committing, per the standing
  instruction.

## Claim assessments (Stage 3 scope)

- **C086-9 (citations carry their relations)** —
  SUPPORTED at stage scope. V4 checks every citation on
  every non-empty matrix cell (1,363 cells, 1,364
  citations on the clean tree, all tied) and every
  candidate-map edge, under T1–T4 with the registered
  tie rules; the seeded Atlas miscarriage (Spec 054's
  unexecuted closure cited as support for the Yadav
  claim) fails V4 while passing V1–V3, and the battery
  is the standing place for new miscarriage shapes. The
  map-edge leg over a *production* map awaits Stage 5's
  artifact; the class runs on candidate maps today.
- **C086-10 (the gate guards the chain in CI)** —
  SUPPORTED at stage scope. The `ledger-gate` job stands
  beside C4 in `.github/workflows/ci.yml`: battery +
  `--pr-scope` on PRs, full + `--regen` on pushes; a
  divergence in any class fails the job. (Reading 6
  above records how the red-on-seeded-divergence leg is
  evidenced.) The claim's "V1–V9" reads V1–V7 + V9 at
  this stage; V8 arrives with Stage 4 and is enumerated
  NOT-RUN until then.
- **C086-11 (publication is gated)** — SUPPORTED at
  stage scope for the artifacts that exist: matrix
  publication runs candidate → gate → replace only on
  ALL PASS, and the negative control leaves the
  published artifacts byte-identical on red with the
  build failing. The map builder publishes through the
  same path when it lands in Stage 5.
- **C086-12 (lossless regeneration is a checked mode)**
  — SUPPORTED. `--regen` hashes, regenerates via the
  pure builder, byte-compares, and classifies any diff
  as intended-change-named (only when a name is
  supplied) or downstream-defect; the clean tree is
  byte-identical, and the battery's hand-edited
  matrix.md is named as the defect.
- **C086-21 (harmonization is exercised)** — Stage 3
  leg SUPPORTED: this stage's outgoing improvement (the
  falsifier-gap census) is written as a pattern note;
  three incoming framework acts (Atlas adoption,
  Amendments 2 and 3, the layer-scoped ruling) are
  recorded with their dispositions in
  `records/harmonization-2026-11-01.md`. Delivery of the
  census note to the RCPH and Atlas chats is the
  parent's act and is flagged owed above, as T105's was.
- **C086-5 (no field fabricated; the gate publishes the
  coverage count)** — the gate leg now holds: every gate
  run prints the falsifier-coverage count in its header
  (831 of 840; bundle 817/817, extracted 14/23), and V2
  recomputes the matrix's coverage block against the
  ledger on every full run.

## What this stage does not establish

Per tasks.md, carried with the tasks they belong to:
T301 — *the gate catches everything* (it establishes
the named classes are checked mechanically, and the
teeth tests bound what "catches" means). T302 — *the
artifacts are substantively right* (only that they are
exactly what the ledger generates). T303 — *the
published content is true* (only that nothing unverified
replaces it). T305 — *future PRs will be honest* (only
that the gate stands in the merge path).

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
