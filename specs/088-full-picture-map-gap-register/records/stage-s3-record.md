# Spec 088 — Stage S3 record (gate extension V10, program-map equivalence)

Executed 2026-11-04 on branch `feat/088-s3-gate-v10` off
origin/main `24ec876a` (the PR #506 S2 merge; main had not
advanced). Tasks T301–T303. All numbers below are quoted
from the gate CLI's own output over the real tree, the
pytest runs' own summaries, or `sha256sum` — read
first-hand this session, nothing extrapolated.

## What landed

- **T301** — `backend/glossa_lab/ledger_gate.py` gains
  class **V10 (program-map equivalence)**: the gate's own
  registered copies of program-map-defs v1 (derivation
  table, claim/study class vocabularies, standing
  template, restricted name-only forms, forbidden
  taxonomy keys, find kinds — not imported from the
  builder) and an independently coded recomputation route
  (`_pm_taxonomy`, `_derive_program_map`, `_pm_roll_up`).
  Four legs: (1) taxonomy coverage and format,
  bidirectional; (2) `program-map.json` byte-equality
  against the gate's recomputation — the recomputation is
  built only from resolving citations (governing ledger
  entries, spec directories, taxonomy assignments), so
  byte-equality carries the citation-resolution check;
  (3) `program-map-finds.json` byte-equality (find-list
  equality); (4) stamp freshness against the current
  ledger (hash, line count, latest entry date, versions).
  The gate header gains a `program-map definitions` line;
  the module docstring's class list gains V10.
- **T301 (CLI)** — `tools/ledger/check_ledger_gate.py`:
  docstring now reads V1–V10; the PR-scope layer map gains
  a `program_map` layer carrying V10, and `_layer_of`
  routes the `glossa-indus/map/program-map*` paths and
  `backend/glossa_lab/program_map_generate.py` to it, so a
  program-map-only change no longer enumerates V10 as
  NOT-RUN under the generic map layer. (A change touching
  `ledger_gate.py` itself is machinery and runs the full
  gate, as before.)
- **T302** — ten new tests in
  `backend/tests/test_spec086_ledger_gate.py`: the
  definitions-copies agreement test (gate copies vs
  builder copies, field for field), the four legs live and
  passing on a program-map scratch tree, the NOT-RUN
  posture where the layer has not landed, and six seeded
  teeth (below). `test_gate_passes_clean_tree`'s class
  enumeration gains V10.
- **T303** — confirmed, not re-landed: the writer
  registration itself landed at S1 (its record's departure
  (d)); the artifact-pattern side needs no new pattern —
  the existing `glossa-indus/map` prefix in
  `ARTIFACT_PATH_PATTERNS` covers the program-map paths,
  and the clean-tree V9 census names
  `backend/glossa_lab/program_map_generate.py` among the
  registered writers (visible in the verbatim gate output
  below). S3 adds the negative case as a test (below).

## Gate on the clean tree — full mode (verbatim)

```
Ledger gate — glossa-indus chain (Spec 086, Point 4)
mode: full
root: /home/hatch/workspace/glossa-run/system-coupling-audit
ledger: glossa-indus/ledger/claims.jsonl — 907 lines, canonical sha256 9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c
definitions: matrix-defs v1 (the gate's registered copies); ledger schema: ledger-schema v1
map definitions: map-defs v1 (the gate's registered copies)
program-map definitions: program-map-defs v1 (the gate's registered copies)
settling semantics: glossa-settle-1 (the gate's registered copies); canonicals: glossa-indus/ledger/settling-canonical.json
falsifier coverage: 867 of 876 claim entries carry a falsifier (published on every gate run, C086-5) — by population: bundle 853/853, extracted 14/23
checks:
PASS V1 ledger validity — pinned schema, fingerprints (spec029-phase-i-v1), D-B uniqueness, field provenance, pointers (Stage 1 validator)
  907 lines validate against ledger-schema v1; every fingerprint recomputes; no duplicates
PASS V1 recorded source hashes — every sources[] and sidecar hash verifies (canonical hash)
  1722 recorded hashes verified against the files on disk via ledger_intake.sha256_file
PASS V2 count equivalence — claims by status: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — claims by stage: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — claims by population: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — falsifier coverage block: ledger == matrix
  matrix carries {'covered': 867, 'total': 876, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 853, 'total': 853}}}; recomputed {'covered': 867, 'total': 876, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 853, 'total': 853}}}
PASS V2 count equivalence — claims by status: ledger == map header
  map header carries {'contradicted': 4, 'draft': 852, 'partially_falsified': 1, 'partially_supported': 3, 'strongly_supported': 2, 'superseded': 1, 'unsupported': 1, 'untested': 12}
  census: 876 claims counted across 8 statuses in the map header
PASS V3 matrix recomputation — cells cell-for-cell (relation, citation ids, derivation rule id)
  1399 cells recomputed from the ledger by the gate's own route; every cell equal
PASS V3 matrix recomputation — rows, columns, coverage, as-of stamp, sign×sign block
  rows, columns, coverage, the as-of stamp and the sign×sign block all equal the gate's recomputation
PASS V4 relation-carrying citations — every citation ties under T1–T4 (incl. the numeric arm)
  1399 matrix cells and 1399 map edges checked; 4198 citations required to carry their relation under T1–T4
  numeric arm: 0 citations in the live population carry a measurement with a machine-readable bound (the arm is exercised on fixtures in the teeth battery)
  map edge census: supports 1392, opposes 7, constrains 0
  UNPROVEN on the live population: constrains map edges — 0 live instances (the class is empty in the artifact and says so; its teeth are fixtures in the battery)
PASS V5 map recomputation — elements trace, embedded fields equal, loads block deep-equals the matrix's
  1520 elements trace to ledger ids; loads block equal
PASS V5 map recomputation — full artifact, the gate's own route (map-defs v1 copies)
  every section of the map artifact equals the gate's recomputation from the ledger (header, elements, edges, loads, matrix, system, claims, settling)
  census: 876 claim elements; column elements by class: studies 10, documents 316, research_checks 31, anchors 287, corpus_texts 0
  census: 1399 map edges by relation: supports 1392, opposes 7, constrains 0; 876 per-claim records; 2 stored settling runs recomputed
  UNPROVEN on the live population: corpus_texts elements — 0 live instances (the class exists in the definitions and carries no columns in v1; its teeth are fixtures in the battery)
  UNPROVEN on the live population: constrains edges — 0 live instances (the relation class is empty in the generated matrix and the artifact says so; its teeth are fixtures in the battery)
PASS V6 anchor shares — strict set recomputes under the recorded D-A rule (strict_sa_independent_hm)
  strict anchors: 94 of 287; strict share 0.3275; validated-anchor share (the strict share, spec.md Point 5) 0.3275; rule version as recorded: Phase-109 follow-through (spec 007, 2026-10-06) applying the Phase-108 strict definition
PASS V6 anchor shares — map header leg
  map header shares equal the recomputation
  census: the share is computed over 287 register records, 94 of them strict
NOT-RUN V7 lossless regeneration
  runs under --regen (the push CI job runs it)
PASS V8 settling canonicals — scenarios reproduce under the gate's own glossa-settle-1 route
  5 registered canonical scenarios reproduced exactly under the gate's own glossa-settle-1 route (S-R4 result blocks, field-for-field), over provenance pins that verify against this tree
PASS V8 settling canonicals — the registered comparison reproduces
  comparison incumbent-vs-full-register-over-subset reproduced exactly (claims compared, per-claim divergences, coverage deltas, signs assigned by one only, expectations named); the expectations note is checked on its mechanically derivable part — the absence clause matches verbatim; the registered note's remainder is brief-specific prose (FINDING-S4-1, stage record)
PASS V8 scenario/verdict separation — the settling layer carries no reachable ledger write path
  1 settling/scenario module(s) scanned; none imports or reaches a ledger write path (append_entry, write_ledger, write_matrix) — the settling layer's outputs are computed records, never ledger verdicts
PASS V9 no write path — gate import hygiene
  the gate modules import no write entry point (append_entry, write_ledger, write_matrix) and contain no write call
PASS V9 no write path — settling/scenario import audit
  1 settling/scenario module(s) audited; none imports a ledger write path
PASS V9 no write path — matrix/map writer census
  writers of the gated artifacts: ['backend/glossa_lab/gated_publish.py', 'backend/glossa_lab/map_generate.py', 'backend/glossa_lab/matrix_generate.py', 'backend/glossa_lab/program_map_generate.py']
  readers (no write call): 6 module(s)
  census scope: backend/glossa_lab, backend/scripts, tools (test code writes fixtures under tmp dirs by design and is not a publication path)
PASS V10 program-map equivalence — taxonomy coverage and format (bidirectional)
  taxonomy assigns all 89 spec directories exactly once (set equality both directions); every extracted document the ledger carries is assigned (7) and every assignment is carried; the format carries no standing-shaped key (defs §8)
PASS V10 program-map equivalence — program-map.json byte-equals the gate's recomputation (program-map-defs v1 copies)
  every claim node cites its governing ledger entry, every study node its spec directory, every extracted document its taxonomy assignment — the recomputation is built only from resolving citations, and the published bytes equal it exactly
  census: 876 claim nodes by class {'closed_other': 1, 'negative': 6, 'open': 867, 'positive': 2}; 89 study nodes by class {'closed_other': 0, 'negative': 0, 'open': 60, 'positive': 0, 'unjudged': 28} (+1 restricted, name-only)
  census: judgment calls 0; unjudged studies 28; falsifier coverage 867 of 876 claims
  census: domain 'Anchors & readings': 13 studies, 0 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Claim families by study line': 40 studies, 568 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Contact zone & external corpora': 2 studies, 33 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Program infrastructure': 17 studies, 150 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Sign inventory & corpus': 17 studies, 125 claims (per-domain counts only; no cross-domain aggregate, C088-14)
PASS V10 program-map equivalence — program-map-finds.json byte-equals the gate's recomputation (find-list equality)
  find list equal: bundle_less_study 28, extracted_null_falsifier 9, restricted_node 1
PASS V10 program-map equivalence — stamp freshness against the current ledger
  stamp ledger hash, line count, latest entry date, and versions all equal the current ledger's
summary: 24 PASS / 0 FAIL / 1 NOT-RUN
RESULT: PASS
```

## Gate on the clean tree — full + --regen mode (verbatim)

```
Ledger gate — glossa-indus chain (Spec 086, Point 4)
mode: full + regen
root: /home/hatch/workspace/glossa-run/system-coupling-audit
ledger: glossa-indus/ledger/claims.jsonl — 907 lines, canonical sha256 9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c
definitions: matrix-defs v1 (the gate's registered copies); ledger schema: ledger-schema v1
map definitions: map-defs v1 (the gate's registered copies)
program-map definitions: program-map-defs v1 (the gate's registered copies)
settling semantics: glossa-settle-1 (the gate's registered copies); canonicals: glossa-indus/ledger/settling-canonical.json
falsifier coverage: 867 of 876 claim entries carry a falsifier (published on every gate run, C086-5) — by population: bundle 853/853, extracted 14/23
checks:
PASS V1 ledger validity — pinned schema, fingerprints (spec029-phase-i-v1), D-B uniqueness, field provenance, pointers (Stage 1 validator)
  907 lines validate against ledger-schema v1; every fingerprint recomputes; no duplicates
PASS V1 recorded source hashes — every sources[] and sidecar hash verifies (canonical hash)
  1722 recorded hashes verified against the files on disk via ledger_intake.sha256_file
PASS V2 count equivalence — claims by status: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — claims by stage: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — claims by population: ledger == matrix
  876 claims; counts equal
PASS V2 count equivalence — falsifier coverage block: ledger == matrix
  matrix carries {'covered': 867, 'total': 876, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 853, 'total': 853}}}; recomputed {'covered': 867, 'total': 876, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 853, 'total': 853}}}
PASS V2 count equivalence — claims by status: ledger == map header
  map header carries {'contradicted': 4, 'draft': 852, 'partially_falsified': 1, 'partially_supported': 3, 'strongly_supported': 2, 'superseded': 1, 'unsupported': 1, 'untested': 12}
  census: 876 claims counted across 8 statuses in the map header
PASS V3 matrix recomputation — cells cell-for-cell (relation, citation ids, derivation rule id)
  1399 cells recomputed from the ledger by the gate's own route; every cell equal
PASS V3 matrix recomputation — rows, columns, coverage, as-of stamp, sign×sign block
  rows, columns, coverage, the as-of stamp and the sign×sign block all equal the gate's recomputation
PASS V4 relation-carrying citations — every citation ties under T1–T4 (incl. the numeric arm)
  1399 matrix cells and 1399 map edges checked; 4198 citations required to carry their relation under T1–T4
  numeric arm: 0 citations in the live population carry a measurement with a machine-readable bound (the arm is exercised on fixtures in the teeth battery)
  map edge census: supports 1392, opposes 7, constrains 0
  UNPROVEN on the live population: constrains map edges — 0 live instances (the class is empty in the artifact and says so; its teeth are fixtures in the battery)
PASS V5 map recomputation — elements trace, embedded fields equal, loads block deep-equals the matrix's
  1520 elements trace to ledger ids; loads block equal
PASS V5 map recomputation — full artifact, the gate's own route (map-defs v1 copies)
  every section of the map artifact equals the gate's recomputation from the ledger (header, elements, edges, loads, matrix, system, claims, settling)
  census: 876 claim elements; column elements by class: studies 10, documents 316, research_checks 31, anchors 287, corpus_texts 0
  census: 1399 map edges by relation: supports 1392, opposes 7, constrains 0; 876 per-claim records; 2 stored settling runs recomputed
  UNPROVEN on the live population: corpus_texts elements — 0 live instances (the class exists in the definitions and carries no columns in v1; its teeth are fixtures in the battery)
  UNPROVEN on the live population: constrains edges — 0 live instances (the relation class is empty in the generated matrix and the artifact says so; its teeth are fixtures in the battery)
PASS V6 anchor shares — strict set recomputes under the recorded D-A rule (strict_sa_independent_hm)
  strict anchors: 94 of 287; strict share 0.3275; validated-anchor share (the strict share, spec.md Point 5) 0.3275; rule version as recorded: Phase-109 follow-through (spec 007, 2026-10-06) applying the Phase-108 strict definition
PASS V6 anchor shares — map header leg
  map header shares equal the recomputation
  census: the share is computed over 287 register records, 94 of them strict
PASS V7 lossless regeneration — matrix.json
  byte-identical after regeneration (sha256 4b40d1269b63be24bdef8aa18d1bb2682b9af2d378856f87b9fcb22406c76a5c)
PASS V7 lossless regeneration — matrix.md
  byte-identical after regeneration (sha256 470570ab89f2eab9e334697f3d865a4674dc16ca1fe2f42077dce8ac17826741)
PASS V7 lossless regeneration — map data
  byte-identical after regeneration (sha256 b419f90b5a3547b19835926f9c78c16dc55c17bdbe40cc8483dec0879fc115f0)
PASS V8 settling canonicals — scenarios reproduce under the gate's own glossa-settle-1 route
  5 registered canonical scenarios reproduced exactly under the gate's own glossa-settle-1 route (S-R4 result blocks, field-for-field), over provenance pins that verify against this tree
PASS V8 settling canonicals — the registered comparison reproduces
  comparison incumbent-vs-full-register-over-subset reproduced exactly (claims compared, per-claim divergences, coverage deltas, signs assigned by one only, expectations named); the expectations note is checked on its mechanically derivable part — the absence clause matches verbatim; the registered note's remainder is brief-specific prose (FINDING-S4-1, stage record)
PASS V8 scenario/verdict separation — the settling layer carries no reachable ledger write path
  1 settling/scenario module(s) scanned; none imports or reaches a ledger write path (append_entry, write_ledger, write_matrix) — the settling layer's outputs are computed records, never ledger verdicts
PASS V9 no write path — gate import hygiene
  the gate modules import no write entry point (append_entry, write_ledger, write_matrix) and contain no write call
PASS V9 no write path — settling/scenario import audit
  1 settling/scenario module(s) audited; none imports a ledger write path
PASS V9 no write path — matrix/map writer census
  writers of the gated artifacts: ['backend/glossa_lab/gated_publish.py', 'backend/glossa_lab/map_generate.py', 'backend/glossa_lab/matrix_generate.py', 'backend/glossa_lab/program_map_generate.py']
  readers (no write call): 6 module(s)
  census scope: backend/glossa_lab, backend/scripts, tools (test code writes fixtures under tmp dirs by design and is not a publication path)
PASS V10 program-map equivalence — taxonomy coverage and format (bidirectional)
  taxonomy assigns all 89 spec directories exactly once (set equality both directions); every extracted document the ledger carries is assigned (7) and every assignment is carried; the format carries no standing-shaped key (defs §8)
PASS V10 program-map equivalence — program-map.json byte-equals the gate's recomputation (program-map-defs v1 copies)
  every claim node cites its governing ledger entry, every study node its spec directory, every extracted document its taxonomy assignment — the recomputation is built only from resolving citations, and the published bytes equal it exactly
  census: 876 claim nodes by class {'closed_other': 1, 'negative': 6, 'open': 867, 'positive': 2}; 89 study nodes by class {'closed_other': 0, 'negative': 0, 'open': 60, 'positive': 0, 'unjudged': 28} (+1 restricted, name-only)
  census: judgment calls 0; unjudged studies 28; falsifier coverage 867 of 876 claims
  census: domain 'Anchors & readings': 13 studies, 0 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Claim families by study line': 40 studies, 568 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Contact zone & external corpora': 2 studies, 33 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Program infrastructure': 17 studies, 150 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Sign inventory & corpus': 17 studies, 125 claims (per-domain counts only; no cross-domain aggregate, C088-14)
PASS V10 program-map equivalence — program-map-finds.json byte-equals the gate's recomputation (find-list equality)
  find list equal: bundle_less_study 28, extracted_null_falsifier 9, restricted_node 1
PASS V10 program-map equivalence — stamp freshness against the current ledger
  stamp ledger hash, line count, latest entry date, and versions all equal the current ledger's
summary: 27 PASS / 0 FAIL / 0 NOT-RUN
RESULT: PASS
```

The class census, counted from these runs: full mode
**24 PASS / 0 FAIL / 1 NOT-RUN** (sole NOT-RUN: V7, which
runs only under `--regen`); `--regen` **27 PASS / 0 FAIL /
0 NOT-RUN**. The pre-S3 counts (T004 record) were 20/0/1
and 23/0/0; the delta is exactly V10's four legs, all PASS.
The V10 census lines reproduce the S2 record's census of
record from the gate's independent route: 876 claim nodes
(positive 2, negative 6, open 867, closed_other 1), 89
study nodes (open 60, unjudged 28, +1 restricted
name-only), 0 judgment calls, falsifier coverage 867 of
876, finds 38 (bundle_less_study 28,
extracted_null_falsifier 9, restricted_node 1).

## Seeded-failure results (T302/T303 teeth)

Each case runs on a tmp copy (`pm_scratch`: the real
ledger, taxonomy, and artifacts as mutable copies, plus
the 89 spec-directory names) and asserts the seeded tree's
SHA-256 hashes — program-map.json, program-map-finds.json,
taxonomy, ledger — are identical before and after the gate
run: **the gate wrote nothing in any case.**

| Seeded divergence | Gate result |
|---|---|
| Hand-edited claim standing in program-map.json | V10 program-map.json leg **FAIL**, divergence named (`standing`) |
| Dropped claim node from program-map.json | V10 program-map.json leg **FAIL** |
| Dropped find from program-map-finds.json | V10 finds leg **FAIL** |
| Builder-vs-gate defs drift (artifacts rebuilt with the builder's table monkeypatched, draft → closed_other) | V10 program-map.json leg **FAIL** — never silent agreement |
| Stale stamp (`stamp.ledger_lines` + 1) | V10 stamp leg **FAIL**, naming `ledger_lines` |
| Dropped taxonomy assignment (one study) | V10 coverage leg **FAIL**, naming the dropped directory |
| Unregistered writer of program-map.json seeded into backend/glossa_lab (T303 negative case) | V9 writer census **FAIL**, naming `rogue_pm_writer.py` |

## Tests and checks

- New V10/T303 tests, filtered run: **10 passed** (37
  deselected).
- Gate module `tests/test_spec086_ledger_gate.py` in
  full: **47 passed**.
- Regression batch — Spec 086 (intake, migration, map,
  matrix, stub disposition), Spec 087 (events doc, palette
  curation, registry integrity, S3 conversions a–f), Spec
  088 (`test_spec088_program_map.py`): **391 passed**.
- `ruff check backend/`: **all checks passed**.
- Published artifacts byte-untouched by every gate run
  above: after all runs, `program-map.json` SHA-256
  `672cfb7850a77dc3a81f67cb09571dc45b9643ea9bf1fe2885bb3b36aa606b3d`,
  `program-map-finds.json`
  `7a6cd13719dc5a15b08240278161863f7e7401461c5867439e5b6c389ccb1e4b`,
  taxonomy
  `dd437fee28778d610677b6713079ded7fa9b46ff03412691c9bf7fc1af194781`,
  ledger
  `9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c`
  — identical to the S2 record's values; `git status`
  showed only this stage's intended files modified, so no
  in-tree regeneration needed restoring.

## Departures and decisions

(a) **Branch name.** The stage brief named
`feat/088-s3-gate`; tasks.md's Stage 3 header names
`feat/088-s3-gate-v10`. Followed tasks.md (the brief's own
precedence rule: the spec files govern where they differ);
the branch was renamed before any commit, so no history
moved.

(b) **Test placement.** The plan's phrase was
"test_ledger_gate.py additions"; the gate's battery module
in the tree is `backend/tests/test_spec086_ledger_gate.py`,
and the V10 tests live there with the rest of the battery.

(c) **Absence posture.** Where the program-map layer has
not landed at all (no taxonomy and neither artifact — a
pre-088 tree, or the gate battery's own scratch trees),
V10 enumerates a single NOT-RUN check rather than three
FAILs: the V5 posture toward a layer that did not exist
yet, and the posture the existing scratch battery
(`test_precondition_holds_and_full_gate_passes_on_scratch`)
requires. Once any part of the layer is present, absence
of the rest is a named FAIL in the affected leg.

(d) **T303's registration predates S3.** The
registered-writer line landed at S1 because V9's census
required it the moment the builder existed (S1 record,
departure (d)). S3's T303 share is the pattern
confirmation and the negative case, as recorded above —
stated so the tick does not read as S3 landing the line
twice.

(e) **Run environment.** The gate and tests were run under
the project venv (`~/workspace/venvs/glossa-ci`); the
system `python3` lacks `aiosqlite` (a declared backend
dependency), under which V3/V5 refuse with "No module
named 'aiosqlite'". Observed, resolved by using the venv,
no code change.

*This does not establish:* that the derivation is correct
— the gate's route and the builder agreeing is
consistency between two implementations of the same
registered definitions; the defs' semantics were the
owner's call at T003/T101 (C088-7's own limit, carried
from T301).
