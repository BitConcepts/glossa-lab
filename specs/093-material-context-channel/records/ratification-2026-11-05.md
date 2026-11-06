# Ratification + adoption record — Spec 093 (2026-11-05)

**Scope:** tasks.md Stage 0 (T003), executed on this branch
(`docs/093-material-channel-draft`) after the owner's block
ratification. This record covers the ratification act, the
program-map assignment, the AEE assessment at adoption, and —
in its appendix — the claims-ledger intake, which was
**executed end-to-end on this branch and then reverted
(held)**, because the refreshed tree cannot pass gate class
V11 leg (c) today for a named Spec 089 machinery gap (the
same gap Spec 084's C084-12 intake hit the same day, PR
#531). **This PR does not touch the ledger** (verified at
landing: 943 lines, SHA-256
`15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`).
No study stage (Stage 1 onward) is started by this motion.
T003 is **not** ticked: its ratification-record and
assignment clauses are complete in this landing, its intake
clause is held, and the tick lands with the intake replay
(Appendix A states the replay exactly).

## The ratification act (T003, first clause)

**Owner block ratification: Tristen Pierson, 2026-11-05.**
The package (spec.md, claims.md with falsifiers, plan.md,
tasks.md, the grounding inventory) was presented in the
Glossa-Lab chat and the owner ratified it **AS A BLOCK** —
decisions D-093-1..8 all as drafted, each carrying the
recommendation text it was ratified with:

- **D-093-1 — This front's home: a new spec (093), not a
  stage of Spec 090 and not a wave of Spec 088.**
  *Recommendation: (a) new spec.*
- **D-093-2 — The channel's field set for Stage 2: the five
  recorded sides (site, material class, artifact type,
  holding/provenance, find context), with ductus and
  iconography excluded until data exists.**
  *Recommendation: (a), with ductus and iconography carried
  as gap-register entries (Stage 6).*
- **D-093-3 — The independence test's form: prediction
  under permutation, per field.** *Recommendation: (a).*
- **D-093-4 — The material arm runs only on an audited
  join.** *Recommendation: (a) — Stage 4's material pass is
  gated on C093-9's audit clearing its frozen precision
  floor.*
- **D-093-5 — The gap register's form: a culture-side
  section of the existing register.** *Recommendation:
  (a), with the adoption task owing the check extension in
  the same PR that lands the first entries (Stage 6).*
- **D-093-6 — The map layer's form: a generated layer, not
  a new map.** *Recommendation: (a).*
- **D-093-7 — Comparanda seeding: the catalogue plus the
  contact-zone records, nothing wider at v1.**
  *Recommendation: adopt.*
- **D-093-8 — The report: the outcome goes to the VEXA
  chat either way.** (The parent chat makes this report
  after the merge; it is not part of this PR.)

The spec's Status line is stamped RATIFIED with the date
and the hold stated, in spec.md on this branch.

## AEE at adoption (T003, assessment clause)

The bundle was re-verified mechanically against claims.md
at adoption: the same 14 ids (C093-1..14) in the same
order, exactly one falsification test each, and every
bundle text opening with its claims.md body — the bundle
in the package is the claims.md bundle, unaltered. Under
the pinned AEE (glossa-ci venv), from the package
directory:

- `aee validate aee-claims.json` — `valid: 14 claim(s) in
  aee-claims.json`, exit 0.
- `aee assess --no-ledger --input aee-claims.json
  --output records/adoption-aee-assessment.json` — exit
  1, outcome **iterate**, recorded verbatim:
  "Assessed 14 claim(s); found 63 failure mode(s); 14
  claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 14 of 14
  claim(s); the same evidence set supports multiple claims
  (FR-2.8, reporting only, no outcome effect in this
  phase). Draft cap: 14 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 14 claim(s)
  below stage 'explained'; the outcome cannot be 'pass'
  (Spec 004 R1.4). Not understood: 28 residual unknown(s)
  are recorded on this assessment (Spec 004 R5.2). Lane 1
  (machine verification): outcome iterate; 0 claim(s) at
  or above the 0.70 threshold, 14 below. Lane 2 (human
  acceptance): stages by effective stage: created 14.
  Lane-2 lag: 14 claim(s) below explained."

"Iterate" is the normal reading for a draft bundle at
adoption (Spec 090's adoption assessment read the same
way); it is recorded, not chased. The assessment of
record is `records/adoption-aee-assessment.json` on this
branch.

## The program-map assignment (T003, assignment clause)

`093-material-context-channel` is assigned in
`glossa-indus/map/program-map-taxonomy.json` — domain
**Claim families by study line**, subdomain **Site,
object & repertoire tests** (the object-join lineage's
subdomain: 024, 028, 031, 033, 040, 041,
042-arm-b-object-type-split, 059-f1-object-join, 061,
062, 067-f1-enlarged-join) — appended at the end of the
studies list, as Spec 090's entry was appended at its
adoption. The program map was regenerated through its
own generator over the unchanged ledger: **912 claims ·
92 studies · 29 unjudged studies · judgment calls 0**.
The finds list records this study as bundle-less
(`bundle_less_study` 28 → 29) — the truthful state while
its claims are held out of the ledger (Appendix A).

## Gate on the shipped tree

`tools/ledger/check_ledger_gate.py`, run on this branch's
tree at landing (glossa-ci venv), verbatim summaries:

- default: **29 PASS / 0 FAIL / 1 NOT-RUN** — RESULT: PASS
- `--regen`: **32 PASS / 0 FAIL / 0 NOT-RUN** — RESULT: PASS

The standing profile, unchanged: nothing in this landing
moves a ledger, matrix, map, or settling pin.

## Test maintenance — census re-pins

Only study-count literals moved (every claim literal
stands, the ledger being untouched). Each new value was
recomputed from the regenerated artifacts before pinning:

- `backend/tests/test_program_map_conformance.py`:
  `PIN_STUDIES` 91 → 92; `PIN_UNJUDGED` 28 → 29; domain
  totals, "Claim families by study line" 40 → 41.
- `backend/tests/test_spec086_ledger_gate.py`: "91 study
  nodes" → "92 study nodes"; "bundle_less_study 28" →
  "bundle_less_study 29".

One further failure on this VM is pre-existing and not
this landing's: `test_spec086_map.py::
test_builder_refuses_a_run_pinned_to_another_build` fails
on this VM even on pristine main (reproduced 2026-11-05,
before this adoption); its fixture's run-store glob meets
the materialization record first. CI is authoritative
for it.

## Appendix A — the executed intake, HELD (all numbers as recorded at execution)

Executed on this branch on 2026-11-05, through the
ledger's own machinery, in the standing precedent order,
then reverted in full when the gate over the refreshed
tree failed on leg V11(c). Nothing below is in the
shipped tree; it is preserved here so the intake replays
mechanically once the machinery gap is repaired.

**Intake.** `tools/ledger/import_bundle.py --spec
specs/093-material-context-channel --date 2026-11-05`:
**14 appended, 0 already canonical, 14 propositions**
(093-material-context-channel/C093-1..14). Ledger: 943 →
**957 lines**; SHA-256
`15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`
→
`e6525d04316fe239b31912329230d8e03a091388da7e657f63a6776ca1bb291a`;
append-only verified byte-wise over the first 943 lines.
`tools/ledger/validate_ledger.py` over the grown ledger:
**PASS** — 926 claim entries; does_not_establish
coverage 755 of 926; errors: none.

**Settling chain refresh** (the precedent's procedure,
in full). `run_settling.py verify-canonicals` over the
new build, before any pin moved: **6/6 registered
canonicals reproduce**. Only then:
`glossa-indus/ledger/settling-canonical.json` pin
refreshed `15a5fbad…`/943 → `e6525d04…`/957 (provenance
and the comparison's inputs), with the re-derivation
recorded in the file itself as `re_derivations[4]`
(act, reason, both pins, verification; expectations
unchanged; glossa-settle-1 unchanged). Both T405
scenarios re-executed over the new build through
`run_settling.py run` (same candidates, same 286-sign
full-frame scope): runs **settling-20261105T154607Z-0119fe**
(incumbent; record SHA-256
`819a0ef74a399bfbc6f9e5d48711af1320fcccbd3ab367fa3df28599741777d2`) and
**settling-20261105T154627Z-62f247** (full-register;
record SHA-256
`89d21746d70b60954ff593eddb6ddf253bf2ca2ffe96cde4b60a4ca2a7ae1fd9`); both result blocks
**byte-equal** to the superseded records'; the run index
gained their entry acts and `supersedes` acts naming
`legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e` and
`legacy:t405-full-register-over-full-frame--f8c86443e924`.
The two superseded records left the store under the map
builder's D-D rule (a stale-pinned evaluation record
cannot be carried): incumbent record blob SHA-256
`17d7dbae6daa135ebbcd37387942268283f5be4e6672b9624ccb34c313565bf2`
(git blob `49d06bd3bef4fdac07f1fdabb41528664e0bc787`),
full-register record blob SHA-256
`176ca660d2f43f8f1b68aa6ba27d745cdaf80b8c545962b896aab67449ee8123` (git blob
`f960d1b24b6df75489fe3a817cb017f036fed186`) — both stand
preserved in git history at the draft head. The Stage 4
dual-run comparison was re-filed from the new pair via
`run_settling.py compare`: identical to the previous
filing except the ledger pin; SHA-256
`1371c981ce4c9cd9721fbed3294aee82c2bc512d9b8293390a201cf3a935874b`
→
`908a0d74d16c131d11bee8cbd485288bc2c570e19345c63c2abb560558b52209`.
Assignment sets re-materialized over the new build
(`run_settling.py materialize-sets`, run
**settling-20261105T154733Z-5cb5af**, record SHA-256
`085308d0bcf28eb74d8753672e7d20d40e81b72d4a5d776688b9d0e62f47d0d2`;
sets unchanged — incumbent 94, full-register 286,
out-of-frame H003; artifact SHA-256
`8023d535f8f0ea1791386bea45e11e6d87b33201ed517cbfe8850b0cb0b68b00`).

**Regeneration over the grown ledger** (the gate's own
generators, dependency order): matrix.json SHA-256
`9ee8620cec91e77e9c8eaec32d41a2486a6d2ff8359d965d3fd768cd1be2ba3f`
(779,273 bytes), matrix.md SHA-256
`6cb0ac91d479a84f6f57b7a75104825ec0ca65a28c76905b11b91172f2e11a04`; map-data.json
SHA-256 `80d34269430aa8a5275bf825265d0d0ce5d36ef697c7cde67f72bb509e7e1181`
(settling runs carried: 2); program-map.json SHA-256
`c73f9eff179c91bd36e9d26ed8dd652f118bc00439ed4ece3592c36ce01c6c39`
(claims: 926 · studies: 92 · unjudged studies: 28 on the
grown ledger).

**The gap, named.** Completing the run index for the
departed pair, `tools/ledger/build_legacy_index.py`
refused verbatim: `LEGACY INDEX REFUSED: legacy recovery:
record 'settling-20261105T022535Z-a7b4e5.json' carries no
'candidate' to recover`. And the gate over the refreshed
tree read **28 PASS / 1 FAIL / 1 NOT-RUN** (default) and
**31 PASS / 1 FAIL / 0 NOT-RUN** (`--regen`), the single
failing leg in both being **V11 run-binding — store
census and index integrity**, with exactly these two
findings:

- "the settling runs store: entry
  'legacy:t405-full-register-over-full-frame--f8c86443e924'
  names record
  't405-full-register-over-full-frame--f8c86443e924.json',
  which neither stands in the store nor is accounted as a
  superseded legacy record (a superseding commit and the
  record's blob hash named)"
- "the settling runs store: entry
  'legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e'
  names record
  't405-incumbent-over-full-frame--d9f73e4c4e4e.json',
  which neither stands in the store nor is accounted as a
  superseded legacy record (a superseding commit and the
  record's blob hash named)"

The mechanism: the departed pair was **entered standing**
by the Spec 089 completion builder, so its entry acts
carry no supersession fields; run-defs §7.1 makes entry
acts immutable and the fold refuses a second entry act
for an id; no act kind amends an entry; and the
completion builder both skips entered ids and refuses on
post-spec records in the store history. A legacy
generation that entered standing therefore cannot be
accounted as superseded after it departs. This is the
first ledger growth since the legacy index was completed
(2026-11-05), which is why the gap never fired before;
Spec 084's C084-12 intake hit the identical signature the
same day (PR #531). The follow-on is a Spec 089-lineage
act (run-defs amendment + builder repair), commissioned
separately; **no part of that fix is improvised in this
PR**.

**Replay.** Once the machinery fix lands: re-run the
intake exactly as above (the claim records in Appendix B
are what the import appends — the import is
deterministic over the unchanged bundle), refresh the
settling chain by the same procedure, regenerate,
complete the legacy index, and confirm the gate over the
refreshed tree. The executed state also stands preserved
in the adoption worker's clone under the local tag
`held-intake-executed-2026-11-05` (commit
`82b750486c4b0263aa035c80fba56d2639876474`), for the
fix's author to diff against.

## Adoption completion note (2026-11-05, finishing pass)

The adoption was finished in a second pass after the first
worker's session ended mid-landing (its assignment commit
stood; this record, the assessment, and the spec.md stamp
were still uncommitted). Verification on the final tree:
gate **29 PASS / 0 FAIL / 1 NOT-RUN** (default) and **32
PASS / 0 FAIL / 0 NOT-RUN** (`--regen`), the standing
profile; ledger still 943 lines, SHA-256 `15a5fbad…`.

One named consequence of the hold, from the full local
enumeration (2,701 passed; phase133 baseline and one
TestClient teardown-flake error the only other non-passes):
`backend/tests/test_spec086_ledger_migration.py::
test_p2_reconciliation` FAILS on this tree. Its check globs
every `specs/*/aee-claims.json` and requires the ledger's
bundle population to fingerprint-match all of them; the
held intake leaves this spec's 14 bundle claims unentered,
so the sets differ by exactly those 14 fingerprints.
Controls run 2026-11-05: the test fails identically at the
draft head `e80be6d4` (the bundle on disk, no adoption
commits) and passes at main `0a76d58e` (no 093 package).
The failure is therefore a property of the
bundle-on-disk-without-intake state the hold creates, not
of the adoption mechanics; it is not repaired here (no
check is weakened to accommodate a hold), and it clears
mechanically at the Appendix A intake replay, which is
also when T003's tick lands.

## Replay completion note (2026-11-05) — the hold is discharged

The Appendix A replay has been executed on this branch,
on top of origin/main at `a805e20b` (merged in as
`1227669c`), after the Spec 089 departed-generation fix
landed as **PR #532** (merge `a805e20b`; run-defs v2: the
`departure` act, the builder completion repair, and gate
V11 leg (c)'s second accounting form). T003 is ticked in
this landing; its intake clause is complete. The intake
was re-run through the sanctioned path, not restored
from the preserved state:

- **Intake.** `import_bundle.py --spec
  specs/093-material-context-channel --date 2026-11-05`:
  14 appended, 0 already canonical. Ledger 943 → **957
  lines**, SHA-256 `e6525d04…`; the appended 14-line
  block's SHA-256 is `79c84105…`, Appendix B's preserved
  block hash; append-only verified byte-wise over the
  first 943 lines. `validate_ledger.py`: **PASS** — 926
  claim entries; does_not_establish coverage 755 of 926;
  falsifier coverage 917 of 926.
- **Settling chain.** `verify-canonicals` over the new
  build, before any pin moved: **6/6 reproduce**. The pin
  refresh (provenance + the comparison's input pin →
  `e6525d04…`/957, `re_derivations[4]` appended) produces
  a `settling-canonical.json` **byte-identical** to the
  held execution's file. Both T405 scenarios re-executed
  (same candidates, same 286-sign full-frame scope): runs
  `settling-20261105T175248Z-22295e` (incumbent) and
  `settling-20261105T175309Z-6f8dc4` (full-register);
  both result blocks **byte-equal** to the superseded
  records'; the index gained their entry acts and
  `supersedes` acts naming the legacy pair. The departed
  pair left the store under the D-D rule, preserved in
  git history at exactly Appendix A's values (incumbent
  blob SHA-256 `17d7dbae…`, git blob `49d06bd3…`;
  full-register `176ca660…` / `f960d1b2…`). The Stage 4
  comparison re-filed from the new pair is
  **byte-identical** to the held filing, SHA-256
  `908a0d74…`. Assignment sets re-materialized (run
  `settling-20261105T175400Z-cacd3f`; sets unchanged —
  incumbent 94, full-register 286, H003 out of frame).
- **Regeneration.** Matrix and program map reproduce
  Appendix A's preserved SHA-256 values **exactly**:
  matrix.json `9ee8620c…`, matrix.md `6cb0ac91…`,
  program-map.json `c73f9eff…` (claims 926 · studies 92 ·
  unjudged studies 28 on the grown ledger; the finds
  list's `bundle_less_study` returns to 28).
- **Legacy index completion.** `build_legacy_index.py`
  appended exactly 3 acts — the two `departure` acts for
  the departed pair and the canonical event entry for
  `re_derivations[4]` — and skipped-with-record the four
  post-spec records in the store's history. The departure
  acts carry Appendix A's blob values (above). The index
  is appends-only (its first 20 lines byte-identical
  before and after), and a second builder run appends
  nothing. Folded census 19 entries.
- **Gate over the refreshed tree** (verbatim summaries):
  **29 PASS / 0 FAIL / 1 NOT-RUN** (default) and **32
  PASS / 0 FAIL / 0 NOT-RUN** (`--regen`), all four V11
  legs PASS; leg (c)'s census line reads "folded census
  19 entries = 4 standing record(s) + 8 superseded legacy
  record(s) + 2 departed generation(s) accounted by
  departure act + 5 canonical re-derivation event(s)" —
  the fix's seeded-proof census line, now over the landed
  tree.
- **Test maintenance.** The census re-pins the growth
  moves were re-set from the regenerated artifacts'
  actuals (commit `ad8dca93`): claims 912 → 926 (bundle
  889 → 903, open 903 → 917, draft 888 → 902), matrix
  cells 1435 → 1449 (supports 1428 → 1442), map elements
  1556 → 1570, loads 912 → 926, falsifier census 903/912
  → 917/926, ledger lines 943 → 957, unjudged studies 29
  → 28, `bundle_less_study` 29 → 28, claims untouched by
  any run 911 → 925. `test_p2_reconciliation` **passes**,
  as the adoption completion note said it would at the
  replay. The four pin-bearing files read 96 passed / 1
  failed; the one failure is the documented pre-existing
  VM failure of `test_spec086_map.py::
  test_builder_refuses_a_run_pinned_to_another_build`
  (this VM's run-store glob meets the materialization
  record first, so the corruption lands on a record the
  builder legitimately skips; reproduced on pristine main
  before this adoption; CI is authoritative for it).
- **Store-state test restatements.** The first full
  enumeration over the replayed tree (5 failed, 2712
  passed, 108 skipped, 1 deselected, 1 error) carried,
  beside the phase133 environmental baseline and a
  shared-TestClient teardown ERROR on
  `test_workspace_scope_check.py::
  test_run_check_verdict_and_missing_db` (the documented
  teardown-flake family signature), four failures of one
  kind: tests written against the Spec 089 S5 store state
  (the pre-spec pair standing, entered standing) whose
  premises the first departure expired —
  `test_run_junction.py::
  test_legacy_pair_is_not_comparable`,
  `test_run_records.py::
  test_t104_dry_run_over_standing_store`,
  `test_run_records.py::
  test_legacy_entries_fold_with_minted_runs`, and
  `test_settling_run_scoped.py::
  test_the_standing_store_index_covers_the_pair_by_
  legacy_entries`. They are restated at full strength in
  commit `5d8fd316`: the pair's bytes are preserved as
  fixtures (`backend/tests/fixtures/legacy_t405_pair/`,
  SHA-256 `17d7dbae…` and `176ca660…`, the departure
  acts' own blob hashes, with a provenance README); the
  junction and run-records tests source the pair from
  the fixtures with their assertions unchanged, and the
  settling coverage test now asserts the departed-state
  invariant (the pair does not stand; its legacy entries
  stand in the folded index; its departure acts resolve
  against the preserved bytes, `blob_sha256` equality
  included). No check was weakened, skipped, or deleted.
- **Full local enumeration.** Run on the final tree
  from `backend/`, with the phase392 determinism test
  deselected by its plain nodeid
  (`tests/test_phase392_q2_gate.py::
  test_pipeline_deterministic_under_seed`): **1 failed,
  2716 passed, 108 skipped, 1 deselected** — the single
  failure is the phase133 environmental baseline
  (`test_phase133_stage0_inventory.py::
  test_builder_recomputation_skips_without_inputs`,
  which fails on this VM on pristine main as well). The
  four restated store-state tests pass; no teardown
  error fired this run; the run-store-glob test
  (`test_builder_refuses_a_run_pinned_to_another_build`)
  passed this run (its failure on this VM is
  enumeration-order dependent, as recorded above). The
  suite's in-tree rewrites (extracted-claims and report
  regenerations) were restored before committing.

**Differences from Appendix A's preserved values, stated
plainly.** Everything the fix's own proof named as a
derived value reproduces exactly: the grown ledger (957
lines, `e6525d04…`), the appended block (`79c84105…`),
the refreshed canonical file's bytes, both departure
blob pairs, the re-filed comparison (`908a0d74…`), the
matrix pair, and program-map.json (`c73f9eff…`). Four
values differ, each by the replay's nature, not by
drift: (1) the three new run ids are execution-minted
(`…T175248Z-22295e`, `…T175309Z-6f8dc4`,
`…T175400Z-cacd3f` in place of the held `…T154607Z-0119fe`,
`…T154627Z-62f247`, `…T154733Z-5cb5af`); (2)
assignment-sets.json's SHA-256 is `5c1db877…`, not the
held `8023d535…` — a byte diff shows the producing-run
line is the **only** differing line; the sets are
unchanged; (3) map-data.json's SHA-256 is `cc7d8054…`,
not the held `80d34269…` — verified structurally: the
artifact carries no timestamps, and the new run ids
appear only as the two run records' names (4
occurrences: the settling panel's pair and the one
touched claim's bearing entries); every other byte is
build-determined by inputs that reproduce exactly (this
clone is blobless and the held artifact's blob could
not be fetched over this link for a byte diff, so this
one comparison is structural, and is recorded as such);
(4) the departure acts' `superseded_by_commit` names
`7aa93c9e`, this replay's refresh commit — the
derivation's value over this branch's history (the first
store-touching commit whose tree no longer carries the
records); the seeded proof's `82b750486c4b` was the same
derivation over the preserved snapshot's history, where
the executed intake commit played that role.

*This does not establish:* anything beyond the intake's
landing — no study stage (Stage 1 onward) is started by
this motion, and the ledger growth changes no claim's
status, stage, or score.

## Addendum — combined-ledger completion-chain recompute (2026-11-06)

PR #533 (the C084-12 intake replay, merge `bbdfc865`)
landed on main while this adoption was in flight, growing
main's ledger to 944 lines (SHA-256 `6a997a31…`) with the
original T405 pair's departure acts already appended. This
adoption's chain had been computed over the 943-line base,
so the completion chain was recomputed over the combined
ledger — by recomputation, never by text union:

- **Ledger.** The combined `claims.jsonl` is main's 944
  lines as a strict prefix (verified: the head-944 hash is
  main's file hash) followed by this adoption's appended
  block (the block SHA-256 `79c84105…` recorded in Appendix
  B): **958 lines, SHA-256
  `c55d57822bcd9b2e9a3401d807aea6e5e1ce872c5e239baadea4834310c8f4aa`**,
  927 claims (bundle 904, extracted 23).
- **Settling.** Re-executed over the combined ledger:
  incumbent `settling-20261106T085256Z-316590` (supersedes
  `legacy:t405-incumbent-over-full-frame--17334e1dfc65`),
  full-register `settling-20261106T085304Z-78bf5c`
  (supersedes
  `legacy:t405-full-register-over-full-frame--47287ced3385`),
  materialize-sets `settling-20261106T085304Z-a38e00`
  (sets unchanged: incumbent 94, full-register 286, H003
  out). Both scenarios' result blocks are byte-equal across
  all three generations (943, 944, and combined builds).
  The canonical's provenance and comparison pins moved to
  the combined build, and `re_derivations[5]` records this
  recompute.
- **Store departures.** Under the derived-layers rule
  (every carried scenario record must pin-match the current
  build, exactly two reproducible runs carried), both prior
  scenario generations departed the store — the 944 build's
  pair and this branch's 957 build pair — their bytes
  preserved in git history. The completion builder appended
  exactly the two departure acts for the 944 pair; the
  original pair's departure acts, already standing on
  main's index, were not duplicated. The branch
  materialize record's writer entry act
  (`settling-20261105T175400Z-cacd3f`) was restored verbatim
  from the branch index. The folded index census reads 23
  entries = 5 standing + 8 superseded legacy + 4 departed
  generations accounted by departure act + 6 canonical
  re-derivation events.
- **Fixture correction.** The merge's rename/rename
  resolution placed the refreshed 944-build record bytes at
  the T405 fixture paths; the fixtures are defined by the
  departure acts' `blob_sha256` pins, and were restored
  byte-identical to them (incumbent `17d7dbae…`,
  full-register `176ca660…`).
- **Census at the combined state.** Falsifier coverage
  918 of 927; matrix 1,450 cells; layered map 1,571
  elements and 1,450 edges (supports 1,443, opposes 7);
  program map 92 studies, 28 unjudged. The census literals
  in the test suites and the frontend e2e header were
  re-pinned to these recomputed values, none weakened.

The replay completion note above stands as the record of
the pre-merge replay; this addendum supersedes its grown
values for the combined line.

*This does not establish:* anything beyond the completion
chain's landing — no study stage (Stage 1 onward) is
started by this motion, and the ledger growth changes no
claim's status, stage, or score.

## Appendix B — the claim records of the executed intake, verbatim

The 14 ledger records exactly as `import_bundle.py`
appended them on 2026-11-05 (the block's SHA-256 as a
14-line file:
`79c841058bf66f97d88fb0423f4b9a7361c795e4cead131c249ab56aeed98a45`). On replay these records are
appended again by the same import; they are preserved
here so the held intake's content is auditable without
the worker clone.

```jsonl
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["an accepted statement of this form whose population, controls, or premise citation is absent; or one that survives in the records after C093-1's standing for its field has fallen, unstated at the fallen strength."], "id": "093-material-context-channel/C093-7", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "025f8c422c933b8a2954f4565365e767e2119c99fa51f11eae87288514f5c7d6", "sign_refs": [], "sources": [{"claim_id": "C093-7", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "A statement this spec accepts about how inscription behavior conditions on a culture-side field (for example: sequence length or sign-choice distributions differing by site or by material class beyond the registered controls) is stated as a fact about the joint distribution of the two projections over the named population, and carries C093-1's recorded standing as a premise on its face. This does not establish: anything about why the regularity holds — no reading, function, or historical cause is asserted by a distributional statement, and none may be read into one.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a comparison result in any stage record whose register entry is absent, postdates the computation, or lacks any of (i)–(iv)."], "id": "093-material-context-channel/C093-4", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "057c3f2ddbbc597133c9a8259297aaf898834ac0d6f4766fcc852330adfeeeac", "sign_refs": [], "sources": [{"claim_id": "C093-4", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "A cross-cultural comparison is computed under this spec only if a comparanda-register entry naming (i) the comparanda set, (ii) the transmission mechanism — documented trade, contact, or continuity, stated as a checkable historical claim with its source, (iii) a fixed time window, and (iv) the practice compared, was committed before the computation's first run. Wide windows (centuries to millennia) are admissible only where the entry's mechanism is a continuity claim stated at that span; a window's width is never a substitute for its mechanism. This does not establish: that a registered comparison is a good comparison — only that it was fixed before it met the data, which is what makes its outcome a test rather than a fit.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["an existing claim's status, stage, or score changed with this spec cited as the act; or a stage record stating a reading, a sign value, or a language identification as supported by this spec's work."], "id": "093-material-context-channel/C093-13", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "168a4c21e5bcce24249c17aa3bb5123db764313caadf339cde0e94b8417b2bc5", "sign_refs": [], "sources": [{"claim_id": "C093-13", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "No act under this spec adjudicates, reclassifies, annotates, or scores any claim already in the ledger; no Indus claim changes status, stage, or score citing this spec; the program's standing position (the Indus script is not deciphered) is untouched, and nothing in this spec is a decipherment claim, evidence for a reading, or a step that presupposes one. This does not establish: anything about the existing claims — only that this spec's front is additive and its boundary is where it says it is.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a GR-093 entry missing any of the four elements, exhibited by entry id; or a completeness check that passes over such an entry."], "id": "093-material-context-channel/C093-12", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "505689db2d90fc4adca4d7a9e431c5ac41bef2b44371df16fefb15834ab10028", "sign_refs": [], "sources": [{"claim_id": "C093-12", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "Each entry in this spec's gap register (Stage 6, extending the Spec 088 register's discipline to the culture-side unknowns: GR-093 series) states, on its face: what is not known; a falsifier — the observation that would close or break the entry's present statement; an acceptance test — the administration whose outcome would discharge the entry; and an honesty-rule type in the register's existing vocabulary. An entry lacking any of the four is not an entry, and the register's completeness check counts it as a failure. This does not establish: that the register enumerates all culture-side unknowns there are — only that every entry it carries is stated in the shape that lets it be closed honestly.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a matrix cell, map node, or derived statement in the material-context layer carrying no ledger id, or citing an id the ledger does not contain; a hand-edit to a generated file attributable to this spec; a ledger diff attributable to this spec beyond ratified intakes."], "id": "093-material-context-channel/C093-11", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "5884c897ff971b4ef1a91465eb5a7f71b6e90c384987b26efc39660b366a5f3a", "sign_refs": [], "sources": [{"claim_id": "C093-11", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "Culture-side claims enter the system only as claims in the append-only ledger (the family this spec adds at adoption, C093-1 onward), entered through the sanctioned intake. The matrix rows and the program-map layer for the material-context domain are generated from the ledger by the registered generators; no culture-side statement appears in the matrix, on the map, or in any derived surface that is not a ledger claim cited by its id; no generated file is hand-edited. This spec's ledger diff across its whole life is its adoption intake plus the claim appends its later stages ratify one by one. This does not establish: that the ledger's claims are true — only that the one-way flow (ledger → matrix → map) this program's publication discipline rests on survives the new domain intact.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a CISI scan or other restricted source material present in the repository or in any stage output; a redistribution of restricted content rather than statistics or metadata; or a contact record to the barred person attributable to this spec."], "id": "093-material-context-channel/C093-10", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "5a16d508451093c4a7bdd7c1f2012076a7c311e24baf9ad5c84bc24fcbbdf05c", "sign_refs": [], "sources": [{"claim_id": "C093-10", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "CISI enters this spec only as statistics and data-list metadata lawfully held and publishable under the standing restriction (scans never redistributed, never in the repository); the Laursen author copy never enters the repository (the rebuilt Table 1 is the artifact); no stage act contacts Andreas Fuls, and no stage act creates an account or channel in any person's name. This does not establish: anything about the restrictions themselves — only that this spec's design never needs to touch them.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a stage outcome recorded as accepted over a fired floor; or a floor, threshold, or population in a stage record differing from its freeze without a superseding freeze that voids the earlier runs."], "id": "093-material-context-channel/C093-8", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "6b7aab4623f6f4111aec4830d189bc9e51870b6752d9447baa4f0411cecd766c", "sign_refs": [], "sources": [{"claim_id": "C093-8", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "Where a stage's frozen floors fire — a joint population below its floor, a held-out arm the counts cannot carry (the inventory names the standing case: four of six named sites in the sequence-bearing subset carry 7 or fewer records), a join that fails its audit — the stage records NOT YET (the administration ran and did not meet its bar, obstruction named) or CANNOT BE ADMINISTERED (the frozen administration cannot be run, forcing counts shown) and stops. No threshold, floor, population, or case is adjusted under this spec to convert a stop into a pass. This does not establish: that a stopped stage was badly designed — the floors are the price of the acceptance machinery meaning anything, and a stop is a finding about the record system's present contents. ## The join, the restrictions, and the one truth store", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a consumed join pair the frozen procedure does not produce; or a pass whose join audit record is absent, or whose stated precision is below the frozen floor, with the pass nevertheless run."], "id": "093-material-context-channel/C093-9", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "8163bdccafbb1725e3516fe32ed8a669551e454fa4df9b8a1775a6256dd51739", "sign_refs": [], "sources": [{"claim_id": "C093-9", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "Any identification of a snapshot museum record with a text-bearing record (by accession number, holding, catalogue identity, or published concordance) that a Stage 4 pass consumes was produced by a join procedure frozen at Stage 1 and audited on a hand-checked sample whose size and measured precision the audit record states. A pass resting on an unaudited join, or on a join whose measured precision falls below its freeze's floor, does not run; the stage records the stop under C093-8. This does not establish: that an audited join is correct pair by pair — precision on a sample is the claim, and the audit's sample and errors are part of the record a reader judges.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["one snapshot record, exhibited by `glossa_id`, carrying a non-empty `canonical_grapheme_ids` list and a non-empty `material`; or a Stage 4 pass whose population includes a record pair no audited join produced."], "id": "093-material-context-channel/C093-3", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "87674a7def636850afc7010fcda434e34adc098dec125276abc34b18a34ed7ab", "sign_refs": [], "sources": [{"claim_id": "C093-3", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "Within the corpus snapshot as pinned, the records carrying both a recorded sequence and a non-empty material number **0**, and the records carrying both a recorded sequence and a non-empty site_name number **966**, all in the indusscript-m77 subset. No Stage 4 pass may consume a joint population the snapshot does not contain: a material-side pass over sequences runs only on a Stage 1 join that has passed its audit (C093-9), and a site-side pass runs only on the populations the freeze enumerates. This does not establish: that the underlying objects lack materials or sites in the world — only that this record system does not carry the joint fact, which is the constraint the design answers to. ## Comparanda and acceptance discipline", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a culture-side field, in the census's sense, present in a named source and absent from the census — exhibited by file, key, and one record carrying it."], "id": "093-material-context-channel/C093-2", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "ac7d5abd33b92222602f1b4d7b01c9329c6816e82ba1255bfdc84df8f740257a", "sign_refs": [], "sources": [{"claim_id": "C093-2", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "The grounding record's field census covers every culture-side field present in its named sources (the corpus snapshot, the M77 and ICIT flat files, the CISI coded subset's loader, the three contact-zone rebuild files, and the corpus-catalogue seeder): each field a named source carries that names site, material, artifact type or typology, holding or provenance, find context, period, or execution medium appears in the census with its presence count, or the census names the field and states why it is not culture-side. This does not establish: that the census's sources are all the culture-side data the program holds anywhere — the claim is bounded to the named sources, and a source outside the list is Stage 1's to add by amendment, with the census re-run.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["the spec closing with no outcome record; an outcome stated in vocabulary §5 does not define without mapping to its terms; or no report delivered after the outcome record lands."], "id": "093-material-context-channel/C093-14", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "c4d57ebcf075965ee3ecdc1bc4e8e68907e1840d1232a5a9ad6f4a9ea8bbd497", "sign_refs": [], "sources": [{"claim_id": "C093-14", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "The spec closes with an outcome record stating, per stage and in the vocabulary of spec.md §5, what was administered, what was accepted, what stopped and at what counts; and the outcome is reported to the VEXA chat for the improvement registry as a closeout deliverable, in the outcome record's own words. This does not establish: that the reported outcome settles the channel question — later stages, later joins, and the reader stand after it.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a cited result computed under an entry whose terms differ from the terms frozen when it ran; or an amended entry whose predecessor's results survive anywhere in the spec's records as live."], "id": "093-material-context-channel/C093-5", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "c5b3abcee5891fc197ee76d50fed9096c904a9565f7a10a00ba5aaa255cba668", "sign_refs": [], "sources": [{"claim_id": "C093-5", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "A comparanda entry's window, set, mechanism, or compared practice, once any computation under it has run, may be changed only by a new entry that supersedes it; every result computed under the superseded entry is voided in the same act and may not be cited, including in the superseding entry's rationale. This does not establish: that the original windows were well chosen — only that the register's history is append-only, so a reader can see every window that was ever tried.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["a statable rule or fitted predictor, frozen before its administration, that recovers a registered culture-side field from sequence-table-plus-bookkeeping features at or above the freeze's stated bar on held-out objects — the channel, for that field, is the same information re-expressed, and C093-1 falls for that field (the outcome record names the field)."], "id": "093-material-context-channel/C093-1", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "c6ce52944debce1f5deeffc2a1f27e09ebc7a0b2a5f64c902c57d132529345ab", "sign_refs": [], "sources": [{"claim_id": "C093-1", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "A candidate state in G1 §2.1's sense determines, for each inscribed object, both its text (the sequence the record system's coded corpora carry) and its material-context tuple as this spec defines it at Stage 2: the per-object recorded values of site, material class, artifact type, holding/provenance, and find context, under the vocabularies the Stage 1 normalization registers. The channel claim is that this tuple is not a function of the object's sequence table together with the record system's bookkeeping (source system, frame, derivation): there is no rule, statable in advance of Stage 2's freeze, that computes the tuple from the table and the bookkeeping alone. Stage 2 administers exactly this: a pre-registered prediction test in which the frozen culture-side fields are predicted from table-plus-bookkeeping features under permutation controls, and the channel stands as independent only at the strength the audited outcome records (spec.md §5's vocabulary). This does not establish: that the channel, where independent, carries information about any reading, sign value, or language identification — independence is a claim about projections of the state, not about what either projection says. Condition 1 (Spec 090, DERIVED) is untouched: this claim asserts a second projection exists to be tested; it does not assert the second projection separates any pair of states.", "status": "draft"}
{"aee_state": null, "as_of": null, "author": null, "author_kind": null, "confidence_in_source": null, "confidence_text": null, "date": "2026-11-05", "does_not_establish": null, "evidence_refs": ["spec.md"], "explanation_record": null, "falsifier": ["an accepted pass in any stage record lacking its registered controls' run records, or resting on a bar absent from its freeze."], "id": "093-material-context-channel/C093-6", "kind": "claim", "migration": null, "population": "bundle", "proposition_fingerprint": "d64ae23430b799c5e18492381642626ed617fcbb2c040e0acfed0686d35f0427", "sign_refs": [], "sources": [{"claim_id": "C093-6", "document_id": null, "path": "specs/093-material-context-channel/aee-claims.json", "role": "source_of_record", "sha256": "b7dc85a888cdbd27b71c5ebe8144659cb43ca529c758724980ce0d41d1a8b4c0", "spec": "093-material-context-channel"}], "stage": "created", "stage_source": "specs/093-material-context-channel/aee-claims.json", "statement": "A Stage 4 pass is accepted only if its frozen design's negative controls (permutation or shuffle of the culture-side labels within the strata the design names) and its replication arm (held-out sites where the design names them, and the inventory's counts allow them) were run under Spec 089 run discipline and the audited comparison of pass against controls meets the freeze's bar. A pass whose controls were not run, or whose bar was set after its first run, is recorded as NOT YET with the obstruction named, whatever its uncontrolled numbers look like. This does not establish: that a pass meeting its bar is true in the world — only that it survived the controls this program requires before a number may be cited.", "status": "draft"}
```
