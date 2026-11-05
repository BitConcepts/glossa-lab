# Spec 089 — Stage 5 record (gate class V11, legacy-index completion, closeout)

Stage 5 of spec 089 (results lumped by the run), built on branch
`feat/089-s5-gate-v11` off `5ec1aca9` (the Stage 4 merge). Scope per
`plan.md` / `tasks.md`: T501 (legacy index completion), T502 (gate class
V11 + the owed V9 writer-census registration), T503 (teeth), T601
(closeout) — plus the assignment-sets binding the stage's own leg (a)
required (§2). Gate classes were censused per the gate-verification
discipline: a leg whose live failing population is zero is named
UNPROVEN-per-census below, with its fixture as its only exercise.

## 1. T501 — the legacy index is complete (`tools/ledger/build_legacy_index.py`)

The builder enumerates the settling store's git history on HEAD's line,
derives a legacy entry for every headerless record version the standing
index does not cover (superseded versions accounted by their superseding
commit and blob), appends the missing acts through
`run_records.append_act`, and indexes the canonical file's recorded
re-derivation events. Run on the real tree it appended **12 acts** (8
superseded records + 4 canonical re-derivation events); a second run
appends 0 (idempotent). The store's folded census is now **15 entries =
3 standing records + 8 superseded legacy records + 4 canonical
re-derivation events**.

Construction verification, independent of the builder's own output: the
superseding commit of each generation was read from git directly
(G0→`491f31cc`, G1→`3f30671c`, G2→`be866b09`, G3→`198e9143`) and the
builder's acts name exactly those commits; the recorded blob SHA-256s
recompute over `git cat-file` bytes and match the ratification record's
historical citations where they exist (G2 `a5597836…` / `ab3db0ec…`,
G3 `89fb596c…` / `018c99ca…`); the standing records' bytes were not
touched (hash-verified by the builder's refusal discipline and the
tests). Historical entries carry no supersedes acts — the supersession
relation is the `superseded_by_commit` field, per the plan's T501 text.

One library repair the completion forced, made in `run_records.py`:
`enumerate_legacy_entries` now skips header-carrying (post-spec)
records when deriving legacy entries — a headed record is entered by
its own writer, so deriving a legacy id for it would double-enter it;
headerless records missing recoverable components still refuse, exactly
as before. The population rule is stated in the function's docstring
and in the gate's leg (c) (departure 4).

## 2. The assignment-sets binding, and the republication it forced

Gate leg (a) verifies a producing binding; the standing
`assignment-sets.json` still carried its S2-era deferral, so the stage
executed the binding: `run_settling.py materialize-sets` ran as run
**`settling-20261105T022535Z-a7b4e5`**; the artifact's sha moved
`36bce404…` → `b1393b83…`, its content modulo the binding verified
byte-identical against the S2 mirror, sets unchanged (incumbent 94,
full-register 286, out-of-frame H003).

The gated map republication the new stamp required was first **refused
by the gate** (artifact byte-untouched) — V5 caught a real latent
defect: with run records now standing in the settling store, the map
builder's store enumeration fed the materialization record to the
settling recomputation degenerately (candidate None), while the gate's
own `_derive_map` refused the same record for unrelated-field reasons.
Repaired at the source, in both copies in the same motion:
`tools/ledger/map_generate.py` and `ledger_gate.py::_derive_map` now
filter the store enumeration to scenario evaluation records (candidate
/ scenario / result present), with comments naming Spec 089 S5.
Republication then passed its gate: `map-data.json` `7b404859…` →
`3ff90022…`, the diff confined to exactly two values
(`header.as_of.assignment_sets_sha256` and
`settling.assignment_sets.sha256`), and the pre-V11 gate read
25 PASS / 0 FAIL / 1 NOT-RUN on the motion.

## 3. T502 — gate class V11 + the V9 writer-census registration

`ledger_gate.py` gains class **V11 (run binding)**, verifying against
the gate's own registered copies of run-defs v1 (surfaces, header
fields, key/constitutive components, determinism classes,
dispositions, absence kinds, act kinds, adjudication states, the
legacy label) — never imported from the run tooling, so tooling drift
cannot move the gate's standard (the copies-agreement teeth pin the
two together). Four legs, both modes:

- **(a) Producing bindings resolve.** The standing assignment-sets
  artifact's `producing_run` resolves to an entered materialization
  record naming the artifact at its current sha256; the three
  generated layers' build stamps equal the ledger's current canonical
  sha; every header-carrying record in a guarded store validates under
  the registered copies.
- **(b) No quarantined citation as verdict support (C089-13).** Every
  run-id-shaped token in every guarded store's files resolves against
  the folded indexes; a token naming a run under open unexplained
  quarantine fails the gate. Tokens resolving to no entered run are
  counted and named in the evidence, not failed (departure 5).
- **(c) Census and index integrity.** Each guarded store's index folds
  under the gate's own copy of §7.1's refusal rules; every standing
  run record is entered exactly once; every folded entry resolves —
  a standing record, a legacy record accounted by its superseding
  commit / git blob / blob sha256, or a canonical event resolving into
  `settling-canonical.json`.
- **(d) Junction completeness (C089-15).** Filed junction reports
  carry in-vocabulary dispositions and well-formed ids; every
  comparable pair (constitutive agreement over full-key entries;
  legacy entries pair with nothing) with divergent outcomes is named
  by a filed report; every unexplained report's runs stand quarantined
  in a guarded index. The gate **scans and never originates** an
  analysis (D-089-2): a missing disposition is a finding, never a
  repair.

**Live-population census** (final tree, from the gate's own evidence):
leg (a) POPULATED — 1 artifact binding + 3 layer stamps + 4
header-carrying records validate. Leg (b) POPULATED on the resolution
side (140 record files scanned on the final tree, 4 cited runs resolve, none
quarantined); its forbidden side has **zero live instances** — no
quarantined run exists to be cited — so the quarantine-citation
failure is fixture-proven only. Leg (c) POPULATED — 18 entries across
2 stores (settling 15; the spec's citation store 3). Leg (d)
**UNPROVEN-per-census on live data** — 0 comparable pairs and 0
junction reports exist today (14 entered runs are key-partial and pair
with nothing); the leg is exercised by its fixtures here and the tool
it backstops was exercised live in S3 (the PR #509 pair; the
freeze-gate precedent of run-defs §10).

**V9 registration (run-defs §9's owed act).** The artifact census's
path patterns now cover the run stores and indexes
(`glossa-indus/ledger/runs`, `glossa-indus/ledger/junctions`,
`run-index\.jsonl`, `assignment-sets\.json`), and the writer census
registers exactly the three store writers the extended census finds:
`run_records.py` (the index itself, via `append_act`),
`run_junction.py` (quarantine acts), `settling.py` (run records). The
`tools/` CLIs write only through the library and read as readers.
`WRITE_ENTRY_POINTS` is unchanged (departure 6). The CLI's layer map
gains the `runs` layer {V11}; `ledger` carries V11; the machinery map
names the run modules.

## 4. T503 — teeth

- `backend/tests/test_legacy_index.py` (new, 3 tests): the builder as a
  subprocess over a two-generation tmp git store — census arithmetic
  (2 standing + 2 superseded + 2 events), superseding commits and blob
  hashes verified against git's own record, idempotency, standing
  bytes untouched.
- Twelve V11 tests appended to `test_spec086_ledger_gate.py` (the gate
  test module of record; departure 7): a self-contained conforming
  fixture passes all four legs; the registered copies agree with
  `run_records`' constants; and each seeded violation fails exactly
  its leg — unbound artifact (a), unknown-run binding (a),
  quarantined citation (b), dropped record (c), dangling supersedes
  (c), divergent pair without a report (d), out-of-vocabulary
  disposition (d), unexplained without quarantine (d) — plus the two
  conforming junction shapes (explained report satisfies; unexplained
  + quarantine passes (d) and fails (b) on the citation). All pass.
- Three S1/S2 teeth restated to the invariants they protect, because
  S5 legitimately moved their premises (the S2-repairs-T104 precedent;
  no assertion weakened): the T104 dry-run census now scopes to the
  pre-spec headerless subset; the materialize-sets mirror test now
  expects the mirror bound (content modulo the binding) with a new
  run id; the standing-pair coverage test scopes its legacy loop to
  the headerless pair. `test_run_records` + `test_settling_run_scoped`
  + `test_run_junction` + `test_settling_canonical` = 96 passed.

## 5. Enumeration and gates on the final tree

Full backend suite (glossa-ci venv, from its log
`089-s5-fullsuite.log`; the documented phase392 local-stall test
deselected by name), bound as light record
**`suite-20261105T023551Z-84136b`** in the spec's records store, its
rewrite manifest naming the 11 regenerated paths under the watched
roots, every one restored hash-verified:

```
1 failed, 2681 passed, 108 skipped, 29 warnings in 505.57s (0:08:25)  [+ 1 deselected]
```

The one failure is the phase133 environmental baseline
(`test_builder_recomputation_skips_without_inputs`); no ERROR entries
(the tray-teardown error of suite shape #1 did not appear in this
enumeration). Against S4's enumeration (2,665 passed): +15 new teeth
(3 legacy-index + 12 V11) and a residual +1 in the guard-dependent
family whose skip/pass state follows suite order (both directions
documented in the S2/S3 records). Ruff over `backend/`: clean.

Ledger gate, both modes, on the final tree — the new standing profile:

```
full:    summary: 29 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 32 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
verify-canonicals: 6/6 registered canonicals reproduce
```

(V11's four checks add exactly 4 to each mode over the S4 profile
25/0/1 and 28/0/0; the full-mode NOT-RUN remains V7, by design.) The
ledger itself is untouched by this stage and by the spec: 943 lines,
canonical sha256
`15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`,
as the final gate run's header reads it.

## 6. Claims discharged by this stage

- **C089-15** — junction completeness is a gate finding, never a gate
  repair: leg (d), with the S3 tool as the analysis of record.
- **C089-16** — the class itself: V11's four legs in both modes + the
  V9 writer-census registration (run-defs §9's owed act).
- **C089-17 (completion)** — the legacy reach-back is now complete:
  every historical settling-store generation and canonical
  re-derivation is indexed under the permanent
  `legacy — key partial` label.
- Per-claim dispositions for all twenty claims are the closeout record
  (`records/closeout-2026-11-05.md`, T601). T001 and T002 are ticked in
  this stage per the ratification record (the package landed at
  adoption; the AEE verification was completed at drafting).

## 7. Departures, stated plainly

1. **The re-derivation count is 4, not the plan text's "two."** The
   plan/tasks text was written before the adoption append it counts;
   the canonical file now carries four `re_derivations` entries (the
   087, 088, 089 and 090 adoptions). All four are indexed;
   completeness (C089-17) governs over the stale numeral.
2. **The assignment-sets binding was executed in this stage.** S2
   deliberately left the standing artifact pre-machinery; leg (a)
   needs a live binding to verify, so the deferral is discharged here
   (§2), with the gated map republication it forced — confined to the
   two stamp values, verified by diff.
3. **A latent builder/gate divergence was repaired at the source**
   (§2): the settling-store enumeration in both `map_generate.py` and
   the gate's `_derive_map` now filters to scenario evaluation
   records. surfaced by the gate's own refusal, not by inspection.
4. **Leg (c)'s census population for citation stores is their
   header-carrying files.** A `specs/*/records/` directory also holds
   assessments and stage records, which are not run population; the
   dedicated settling store's population remains every record file in
   it. The library's legacy derivation follows the same rule (§1).
5. **Leg (b) reports unresolved run-id tokens; it does not fail
   them.** Stores legitimately name runs in prose and fixtures (the
   two live instances are S3's fixture ids); the leg fails what
   C089-13 prohibits — a citation of a quarantined run.
6. **`WRITE_ENTRY_POINTS` is unchanged.** The plan's V9 act is the
   census registration (patterns + writers); that constant's own text
   scopes it to the settling write path.
7. **Gate teeth live in `test_spec086_ledger_gate.py`**, the gate test
   module of record since Spec 086, not under the plan text's
   `test_ledger_gate.py` name.
8. **Three S1/S2 teeth were restated** (§4) under the
   invariant-restatement discipline; each still fails on its seeded
   violation class.
9. **Carried standing departures stand as registered**: the study
   surface's determinism class (S1: deterministic under the freeze
   record's fixed pins); citation-time minting for the experiment
   surface (S4); the explained shape's tray-module-name scope (S3).
   The S2 assignment-sets deferral is discharged by §2 and is not
   carried further.

## 8. What this stage does not establish

- T501: legacy results are not bound — the `legacy — key partial`
  label says the opposite, permanently; indexing history does not
  retroactively give it keys it never recorded.
- T502: V11 makes missing bindings, missing dispositions and forbidden
  citations unpublishable; it does not make any run's result true, and
  its legs (b)-forbidden and (d) are proven by fixtures against live
  populations of zero, named as such in §3.
- T503: only the named failure modes are proven caught; an unlisted
  mutation of a run artifact is future work for the census, not a
  covered case.

## 9. Repair round — the CI gate failure (2026-11-05)

CI attempt 1 on this stage's PR (#521, run `41957645343`) failed in
exactly one job, "Ledger/matrix/map equivalence gate" (job
`127016285488`); the other nine jobs passed. Read from that job's
log: inside the test battery's constructed tree the gate reported
`22 PASS / 2 FAIL / 2 NOT-RUN`, legs (a) and (c) failing —
`settling-20261105T022535Z-a7b4e5` named by leg (a) as a producing
run "not entered in the settling runs store's index", and by leg
(c) together with both T405 records as files standing "with no
index entry". Two tests failed:
`test_map_legs_live_and_pass_on_a_clean_map_tree` and
`test_gated_publication_of_the_map_and_its_negative_control`.
Reproduced locally, standalone, with the identical failure text
before any repair was attempted.

**Mechanism.** The `map_scratch` fixture
(`backend/tests/test_spec086_ledger_gate.py`) assembled the map
chain's records into the battery's scratch tree and copied the
settling runs store with `glob("*.json")`. That glob does not
match `run-index.jsonl`, so the constructed tree carried the
store's three record files and no index: the fold yielded nothing,
the §2 binding could not resolve, and the census covered no
record. The gate's verdict on that tree was correct — a store
whose records stand without their covering index is
non-conforming under C089-15a/C089-17.

**Owning side: the test fixture — not the gate, and not the
publication path.** The real tree carries the index (tracked,
committed in `2ed4970`); `gated_publish.publish_map` gates the
root tree in place, and this stage's own republication (§2) had
already passed through that path against the real tree. The
failure surfaced in the one job that runs the gate module
standalone against a pristine checkout, where the battery's
clean-tree precondition holds and the fixture is exercised for
real. The fixture existed in that form because it was written
for the Spec 088 map legs, when the store held only `*.json`
records; Spec 089 S2 added `run-index.jsonl` to the store, and
no gate leg consumed the index inside a scratch tree until V11 —
the stale glob was invisible until the first index-verifying leg
ran against the fixture. Both tests reach the store through the
same fixture (the publication test gates the `map_scratch`
tree), so one defect produced both failures.

**Repair.** `map_scratch` now copies the store closure — every
regular file in the runs directory, not only `*.json` — and the
junction store likewise when the real tree has one (it comes
into existence with the first filed report; leg (d) reads it
from the tree root, and a records-only copy would lose it the
same way). No V11 leg changed; no tolerance for a missing index
was added; no fixture id was special-cased.

**Post-repair verification** (all read from records): the two
tests pass; the gate module is whole again at **64 passed** (CI's
62 passed + 2 failed reconciles exactly). Full backend
enumeration, from its log
(`~/workspace/glossa-run/tmp-suite/089-s5-repair-fullsuite.log`,
phase392 stall test deselected by name):

```
1 failed, 2681 passed, 108 skipped, 29 warnings, 1 error in 674.05s (0:11:14)  [+ 1 deselected]
```

The one failure is the phase133 environmental baseline; the one
error is the tray-teardown error (suite shape #1 — absent from
§5's enumeration, present here; an acceptable non-pass of record
in either state). The passed count is unchanged at 2681 — the
repair adds and removes no tests — and the gate profile is
unchanged:

```
full:    summary: 29 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 32 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Ruff over `backend/`: clean. The enumeration's in-tree
regenerations (ten extracted-claims files, the batch-4 claims
report, `outputs/partial_loop_result.json`) were restored before
committing; the repair commit touches only the test module and
these two records. No counts moved anywhere: the census, the
ledger (`15a5fbad…`, 943 lines), and the claim dispositions are
exactly as §§3–6 state them.
