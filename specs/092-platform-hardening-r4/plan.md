# Spec 092 — implementation plan

Stages run in the owner's priority order: encryption first (Stage 1),
verified writes second (Stage 2), the harness remainder third
(Stage 3). Stage 0 (adoption) precedes all builds; the closeout ends
the spec. Dependencies between stages are stated per stage; the one
real cross-stage dependency (Stage 1's save path needs the
verified-write construction before the library exists) is discharged
inside Stage 1 and refactored in Stage 2, so no stage waits on a
later one.

## Stage 0 — package adoption (precondition for every build stage)

The package lands as a draft PR (`docs/092-r4-draft`); the claims are
assessed under the pinned AEE (T002) at draft time. On the owner's
block approval — spec, 14 claims, this plan, and decisions D-092-1..4,
with D-092-1's key-custody selection made as part of the approval —
the adoption PR records the ratification and appends the C092 bundle
through `tools/ledger/import_bundle.py` (the only sanctioned path),
regenerates the generated layers, and republishes through
`tools/ledger/gated_publish.py`, with the gate green before and after.
Claims: package-level (no C092 claim discharges here; C092-14's
boundary census starts from the adoption tree).

## Stage 1 — Credential encryption at rest (C092-1..5; C092-7's store leg)

**Objective.** The settings store stops holding plaintext credential
values, under the owner's D-092-1 custody selection, with no caller
moving.

**Design.**
- A registered **credential set** in `api/settings.py`: the key names
  whose values are credential-class (the provider API keys,
  `smtp_password`, `ms_graph_refresh_token`; configuration names —
  hosts, ports, toggles, intervals, `_provider_prefs` — are not in
  it). The set is data, reviewed like the `KNOWN_KEYS` list it sits
  beside, so a future key joins by a one-line registration.
- **Store format v2.** The file remains one JSON dict. A credential
  entry's value becomes an envelope object
  (`{"v": 2, "alg": ..., "nonce": ..., "ct": ...}`, fields named by
  the build under the selected construction) instead of a string;
  every other entry is byte-for-byte the v1 shape. `_load_keys`
  returns plaintext values to callers exactly as today — decryption
  happens inside the store functions, which is what keeps C092-5
  holdable. Format detection is by envelope shape, so v1 and v2
  entries can coexist during the migration act and never after it.
- **Key loading.** A single loader resolves the key from the D-092-1
  custody location, once, with its failure modes named as distinct
  exceptions the settings surface translates into C092-3's error
  state. The loader is the only code that touches key material;
  nothing logs it, and tests assert its absence from the data dir and
  the repo (C092-2's falsifier, mechanized).
- **The save path** writes via temp-file + fsync + atomic rename +
  read-back verification from this stage (the construction C092-7
  names), implemented inside the store module; Stage 2 lifts it into
  the library and this path is refactored onto it. The 0600 chmod
  discipline is kept and applied to the temp file before rename, so
  no window exists where the store sits at looser permissions.
- **Migration.** On load, if any credential entry is in v1 shape, the
  store is migrated in the same act: full dict re-saved in v2 through
  the verified construction, then re-read and compared value-by-value
  against the pre-migration dict before the load returns. Any failure
  (no key, denied write, mismatch) leaves the original file untouched
  and raises the named state — the load does not proceed on a
  half-migrated store. The database init's prefs-migration read
  tolerates the named state by skipping with a logged reason
  (C092-3's startup clause).
- **The dependency** the selected construction requires (under the
  recommendation: `cryptography`) is added to `backend/pyproject.toml`
  in this stage's diff, pinned in the house style.
- **Tests.** Attack battery first: substring/encoding sweep over a
  configured fixture store's bytes for every stored value (C092-1);
  data-dir-only decryption attempt (C092-2); wrong-key, missing-key,
  and bit-flipped-ciphertext fixtures → the named state, no values
  served (C092-3); legacy fixture migration, value-identical
  before/after, failure-leaves-original fixtures (C092-4); a
  contract battery running the consumer-facing surface (masked GET,
  PUT semantics, `get_key` resolution incl. env precedence and
  placeholder filtering) identically against v1 and v2 stores
  (C092-5). All fixture values are synthetic.
- **Live leg (T104).** Deployment to the desktop install runs through
  the gatekeeper like every desktop act: the stage record carries
  the live store's key-name census (names and counts, never values)
  before and after, and the backend's health identity check after
  restart. The migration of the one live store is this leg's act; no
  other install exists to migrate (the VM holds no production store).

**Acceptance.** Tests per claim as above (mode: **test**), plus the
live leg's census proof (mode: **gate** — the stage does not close on
fixtures alone).

## Stage 2 — The verified-write library (C092-6..8, C092-13)

**Objective.** The construction Stage 1 hand-rolled becomes the
repo's supported write path, with its failure classes under CI.

**Design.**
- `backend/glossa_lab/verified_write.py` (module name settled by the
  build under repo conventions) carries the safe-write contract
  verbatim in behaviour: temp in the target's directory, fsync,
  atomic rename, directory fsync, read-back SHA-256, the bounded
  retry ladder with fresh-subprocess attempts, empty-content refusal,
  parents never created, one typed error type. The module docstring
  names its provenance (the fleet tooling's contract, carried in) so
  the two implementations' kinship is explicit.
- **Refactor.** `api/settings.py`'s save path is re-pointed at the
  library; Stage 1's in-module construction is deleted, and C092-7 is
  re-proven against the library path (the fault fixtures run again,
  unchanged).
- **Battery in CI.** The fault classes are seeded by monkeypatched
  failure injection (denied open, 0-byte land, short write, parent
  missing / not a directory), each asserting the typed error and the
  target's byte-preservation. The battery lives in the backend suite,
  so CI runs it on every PR — the production path is the tested path
  (C092-8).
- **Census.** The store writers this spec added or moved are
  registered for the gate's V9 writer census (C092-13); the stage
  record states the gate's full and --regen summaries verbatim on its
  final tree.

**Acceptance.** **Test** for C092-6/7/8; **gate** for C092-13 (the
gate's own census output is the evidence).

## Stage 3 — The test-harness remainder (C092-9..12)

Four independent legs; order inside the stage is the builder's, each
leg closes on its own evidence, and no leg's fix may weaken an
assertion anywhere (the design rule below).

**Leg A — tray teardown (C092-9).** Reproduce the ERROR on demand
first (the tray token module under repetition and under suite order);
the reproduction, not intuition, names the mechanism (the standing
hypothesis shape — a fixture or connection closed before a teardown
consumer runs — is a hypothesis until the reproduction speaks). Fix
at the source (fixture lifecycle or the tray helper's connection
handling), then the discharge battery: five consecutive full-suite
runs named by run id with zero tray teardown ERRORs. On discharge,
the run-defs §5 amendment act (D-092-3) is appended through the
definitions document's own amendment discipline.

**Leg B — in-tree rewrites (C092-10).** Census the rewriting tests
from S4's manifest machinery (the manifest over a full run is the
worklist, not a guess): each rewriting test is moved to an isolated
copy of the inputs it regenerates from, or its regeneration becomes
its asserted output in a temp tree. The clean-tree precondition guard
in the run-scoped tests is removed once the tree stays clean — the
guard's skip count reaching zero is proven from a full-suite light
record whose own manifest is empty. The repo-root `outputs/` writer
S4 named is dispositioned the same way.

**Leg C — phase392 (C092-11).** Profile the stall on the VM
(py-spy or cProfile under the test's own seed, the profile artifact
filed with the stage record), then apply D-092-4's branch rule:
pathology → fix and prove in-budget local completion (the budget
stated in the record before the fix is attempted); intrinsic cost →
the environment-scoped deselection registration (run-defs entry
naming the test, the VM environment class, and the CI backend job as
authoritative), wired into the suite-runner configuration so local
enumerations inherit it without a manual flag.

**Leg D — notifications ERROR (C092-12).** The stated battery: 50
standalone repetitions of the notifications test module plus 3
full-suite-order runs, each run's outcome recorded. A reproduction
is classified in the record (mechanism + family or defect) and fixed
under Leg A's pattern if it is a defect; no reproduction across the
battery closes the item UNREPRODUCED, with the closure record
carrying the automatic-reopening term.

**Acceptance.** **Test** for the legs' discharges (named runs and
records are the evidence objects); **gate** for Leg A's run-defs
amendment (it lands through the definitions/gate path like every
registered-definitions change).

## Closeout

The closeout record (T401) discharges C092-1..14 at stage-evidence
strength with stage/PR pointers, restates the standing gate profile
from the gate's own output on the final tree, verifies C092-14 by a
diff census over the spec's stage branches (no claim-status movement,
no token-file or edge-custody diff, no UI behaviour diff), and names
anything left undischarged with its reason. The spec is complete on
the closeout PR's merge.

## Design rules carried through every stage

- **No credential value is ever handled as data.** Fixtures are
  synthetic; records cite names and counts; logs and stage records
  are swept for value-shaped strings before commit (the settings
  module's existing placeholder discipline is the model).
- **The tested path is the production path.** No construction is
  adopted that CI cannot exercise identically (the D-092-1 deciding
  rule); a stage that finds itself testing a fallback stops and
  reports.
- **No assertion is weakened to buy a pass.** A bar fixed in a claim
  (five runs, fifty repetitions, zero skips) is met or the claim is
  reported undischarged — never re-barred inside its own stage.
- **Failures are named states, not absences.** Every new failure mode
  this spec introduces (decryption failure, verified-write failure,
  migration failure) has a name, a surface, and a test; silent
  degradation is the defect class the whole spec exists to close.
