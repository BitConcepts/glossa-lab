# T011 record addendum — the C084-12 intake replayed and landed (2026-11-05)

Act: the follow-on intake act the T011 stage record
(`records/t011-privacy-fixture-2026-11-05.md`) prescribed.
Branch `feat/084-c084-12-intake-replay`, PR #533. The
machinery repair it waited on is PR #532 (Spec 089
amendment: run-defs v2 — departed-generation accounting,
merged at `a805e20b`). The privacy statement, fixture,
and serving surface landed in PR #531; this act is the
ledger intake and everything it forces, nothing else.

## The chain, executed in the stage record's order

- `claims.json` re-created as this spec's second bundle
  file from the stage record's appendix, byte-faithful
  (the appendix block is exactly the bundle's canonical
  serialization; verified programmatically before the
  import). `aee-claims.json` untouched — frozen at its
  2026-10-31 intake.
- `tools/ledger/import_bundle.py --spec
  specs/084-policy-sync-conformance --date 2026-11-05`:
  **1 appended (C084-12), 11 already canonical, 12
  propositions**. Ledger 943 → **944 lines**, canonical
  SHA-256
  `6a997a31be478e33106c40753f90653c4155141324ee198904dc333e2ebda922`.
- Matrix regenerated without refusal.
- `run_settling.py verify-canonicals` over the new
  build: **6/6 reproduce**, before the pin was touched.
  `settling-canonical.json` provenance pin and the
  comparison's `inputs.ledger_sha256` refreshed to the
  new build; the refresh is recorded in the file itself
  as `re_derivations[4]` (act, reason, both pins,
  verification). Expectations unchanged; semantics
  unchanged.
- The T405 pair re-derived over the new build: both
  scenarios recomputed in memory over the same
  candidates and the same 286-sign full-frame scope;
  result blocks byte-equal to the standing records;
  only the pins block moved. Refreshed records renamed
  under the content rule to
  `t405-incumbent-over-full-frame--17334e1dfc65.json`
  (37,957 bytes, SHA-256 `65999c2d…`) and
  `t405-full-register-over-full-frame--47287ced3385.json`
  (87,209 bytes, SHA-256 `028a22d9…`); the superseded
  pair removed from the store, preserved in git
  history.
- The Stage 4 dual-run comparison re-filed via
  `run_settling.py compare` over the refreshed pair;
  its diff against the prior filing is exactly the two
  ledger pin leaves (sha256, lines).
- Layered map regenerated (falsifier census 904 of
  913; settling runs carried: 2); program map
  regenerated at **913 claims**. After the index
  completion below, all three gated publications
  (matrix, map, program map) were re-run and published
  byte-identical bytes: the final artifact state is
  the product of passing gated runs.
- **Run-index completion** — the step the first attempt
  could not take. `tools/ledger/build_legacy_index.py`
  under run-defs v2 appended exactly 5 acts, appends
  only (index 15 → 20 lines; the first 15 lines
  byte-identical):
  - `departure` for
    `legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e`
    (blob SHA-256 `17d7dbae…`, git blob `49d06bd3…`,
    superseded_by_commit `72629bf8…`, this act's
    intake commit);
  - `departure` for
    `legacy:t405-full-register-over-full-frame--f8c86443e924`
    (blob SHA-256 `176ca660…`, git blob `f960d1b2…`,
    same superseding commit);
  - standing `entry` acts for the refreshed pair;
  - the canonical event `entry` for
    `re_derivations[4]`;
  - and it skipped-with-record the one post-spec record
    in the history (the a7b4e5 materialization record).
  The departure acts' derived values match the values
  PR #532's amendment record computed independently
  from git history (same blob hashes, same git blob
  ids). Folded census after completion: 18 entries.
  A second builder run appends nothing (idempotent —
  verified on the finished tree).
- Gate over the completed tree, verbatim summaries:
  full **29 PASS / 0 FAIL / 1 NOT-RUN**; `--regen`
  **32 PASS / 0 FAIL / 0 NOT-RUN** — all four V11 legs
  PASS, leg (c) among them (the leg that read FAIL,
  28/1/1, over the first attempt's refreshed tree).

## Against the preserved executed values

The stage record preserved the first attempt's numbers
so this replay could be checked against them, and it
is: the grown ledger is **byte-identical** to the
preserved executed state (944 lines, the same
canonical SHA-256); the import's counts are the same
(1 appended, 11 canonical); canonicals 6/6, the same;
the refreshed T405 filenames are the preserved ones,
byte counts the same (37,957 / 87,209); the program
map stands at the preserved 913 claims. Differences,
all of them the repair working rather than divergence:
the run index gained the 5 acts the first attempt
could not append at all; the departure acts name this
act's intake commit as the superseding commit (the
first attempt never reached a commit); and the census
pins in the test tree moved by exactly the one claim
(below).

## Test maintenance — census re-pins

The append moved every census number by exactly the
one claim. Pins re-set to the regenerated artifacts'
actuals, each recomputed from `matrix.json` /
`map-data.json` / `program-map.json` (none adjusted to
fit): claims 912 → 913; bundle 889 → 890; open
903 → 904; draft 888 → 889; matrix cells 1435 → 1436
(supports 1428 → 1429, opposes 7, constrains 0); map
elements 1556 → 1557; edges 1436; falsifier census
903/912 → 904/913; ledger lines 943 → 944; claims
untouched by any run 911 → 912; `no_stage_recorded`
15 → 16; the scoped-404 leak canary and the Spec 088
fixture-page canary moved to the new census total
(their teeth are the current total); the e2e ledger
label 912 → 913. One further reference of the same
class: `test_run_junction.py::test_legacy_pair_is_not_comparable`
names the standing T405 pair by its content-addressed
filenames; the refresh renamed the pair, so its four
references (two filenames, two legacy ids) moved to
the refreshed pair — the test's subject (the standing
pair, key-partial, not comparable) is unchanged. No
assertion was weakened, skipped, or deleted.

## Test results

Targeted surface (program-map conformance, Spec 086
map and ledger-gate evidence, Spec 088 program map,
ledger migration incl. `test_p2_reconciliation`,
run junction): all pass after the re-pins.
`test_reconciliation_reports_filed` errored once at
teardown in a combined run and passes standalone and
in its file's run — the known TestClient teardown
flake family, not this change.

Full backend enumeration, run locally from `backend/`
WITHOUT `-x`, with the phase392 determinism test
deselected by its plain nodeid (the known local stall;
CI is its authoritative runner), TMPDIR on disk:
**2 failed, 2715 passed, 108 skipped, 1 deselected,
1 error** (307.60s), run before the junction re-pin
above; after it, the junction file passes in full
(16 passed, 2 skipped). The enumeration's items:

- `test_phase133_stage0_inventory.py::
  test_builder_recomputation_skips_without_inputs`
  FAILED — the known environmental baseline (missing
  download; fails on pristine main on this VM; does
  not fail CI).
- `test_run_junction.py::
  test_legacy_pair_is_not_comparable` FAILED
  (FileNotFoundError on the departed pair's names) —
  the stale reference repaired by the re-pin above.
- `test_workspace_scope_check.py::
  test_run_check_verdict_and_missing_db` ERROR at
  teardown — the known shared-fixture teardown flake
  family (the same signature as PR #528's CI attempt
  1); the file passes standalone (5 passed).
- `test_spec086_map.py::
  test_builder_refuses_a_run_pinned_to_another_build`
  PASSED in this enumeration; it fails when run in
  smaller selections on this VM because it corrupts
  whichever run record `glob("*.json")` enumerates
  first. Reproduced identically on a pristine checkout
  of origin/main (`a805e20b`) on this VM during this
  act — pre-existing, not this change; CI is its
  authoritative runner.

Ruff over `backend/`: all checks passed. After every
suite run the in-tree regenerations the suites cause
(extracted_claims JSONs, one claim report, one outputs
file) were restored; the final tree carries only this
act's intended changes.

## Cleanup determination

This act's clone (`~/workspace/glossa-run/
c08412-replay-clone`) is retained for the parent's
gating; the pristine-main worktree used for the
pre-existing-failure check was removed in the same
session; the scratch drivers live outside the repo
under `~/workspace/glossa-run/c08412-scratch/`. No
Docker containers, no background processes, nothing
spawned left running.

*This does not establish:* that the privacy
statement's facts hold at cloud go-live (the fixture
header carries the go-live re-check list), or anything
about what any settling result means — only that the
held intake now stands in the ledger through the
sanctioned path, with its derived layers regenerated
and its departed generations accounted.
