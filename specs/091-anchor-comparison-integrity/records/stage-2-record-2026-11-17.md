# Spec 091 — Stage 2 record (the locator pass), 2026-11-17

**Stage:** 2 — W1 in-house leg: the locator pass (tasks T201–T202).
**Branch / PR:** `feat/091-s2-locator-pass` (PR number in the PR record).
**Base:** `8aff1188` (main at commissioning; the Spec 091 Stage 1 merge).
**Claims:** C091-1 (artifact side, T201; pass side, T202), C091-13.

## State of this stage, stated plainly

**T201 is complete. T202 is built and ready but NOT executed: its
run is blocked on a data transfer that needs the owner's approval.**
The two held sign-list datasets the pass must search —
`m77_sign_list.csv` and `wells1998_sign_list.json` — are gitignored
source-store files. They are absent from this clone, from the live
origin, and from everywhere else on the mini-server (swept
2026-11-17); the only surviving copies stand in the tower-compute
archive (`glossa-run/m77-verify/v2_backup/` and
`glossa-run/wells1998-extract/`). The transfer to the mini-server
was attempted on 2026-11-17 and its approval was not answered in
time, so the transfer was not performed and is not retried here.
The generator refuses, by design, to file not-found outcomes
against held copies it did not search — so the run waits rather
than papering over the gap. The unblock is one approved transfer
plus two commands (§4).

## 1. Per-task outcomes

- **T201 — The locator record artifact + generator** (`backend/scripts/spec091_stage2_locator_pass.py`; artifact `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_locators.json`, beside the frozen provenance file, which this stage never writes). Per entry, per reading field (`phonetic_reading`, `semantic_reading`), exactly one outcome: a **locator** (the three-part triple of eligibility-defs v1 §2 — work, page/table/figure pinpoint, sign scheme — whose cited passage carries the field's value) or a **not-found** carrying the documented search (sources consulted, in order, each with status, method, per-entry facts, and the run date — C091-1's form). Entries are referenced by sign id. Acceptance: **test** — met on fixtures (§3): the schema files a locator from a held primary source, an in-repo pointer never grounds one, and the validator refuses an entry filed with neither outcome, a locator missing a part, and an undocumented not-found. The registered search order (§2) is data in the generator, and the generator refuses to run when a registered held source is absent at its canonical path.
  *This does not establish:* that the searches behind not-found outcomes were adequate — adequacy is sampled under T202.
- **T202 — The locator pass executed.** NOT EXECUTED (see the state note above). The execution machinery is the same generator: `--execute` mints the run id at start (D-089-1), runs the pass as a run under the program's run discipline (surface `study`, record written through `glossa_lab.run_records` into this spec's `records/`), writes the artifact by verified write, and `--verify-sample` re-executes the searches for the rule-drawn sample from fresh reads and files `records/t202-sample-verification.json`. The sample rule, stated here before any drawing: **every entry carrying a locator (a census — each locator verified against its cited source text), plus every 12th entry in sign order starting with the 1st (16 entries), plus every entry whose phoneme-map consultation hit (the near-miss population; 17 entries at the staged crosswalk as read 2026-11-17)**. T202's tick waits for the run; its human-as-oracle leg (the reviewer rules the sampled not-found searches were real searches of the named sources) stands on the parent reviewer's ruling at gating, per the Stage 1 pattern.
  *This does not establish:* eligibility — located readings still need independent coding (T401) before any class moves.

## 2. The search design (what the run will search, in order)

Per entry and reading field, against the entry's staged value and
stated source in the frozen provenance file (184 entries; stated
sources: "Parpola 1994 Appendix B" ×171, the Phase-28 predecessor
table ×6, the spec 004 WS2 expansion ×5, a literature-synthesis
label ×2):

1. **The entry's stated source.** For the 171, Parpola 1994
   Appendix B — a sign-correspondence table, which WP4 established
   supplies the mapping, not readings. For the 13, the in-repo
   derivative the label names (carries the value at file level
   only; a pointer to another in-repo table is not a locator).
2. **Parpola 1994, *Deciphering the Indus Script*** — the primary
   work the readings are attributed to. **Not held** (no copy in
   the repo, on the mini-server, or in the tower-compute archive,
   surveyed 2026-11-17); its text cannot be searched. Named
   limitation L1.
3. **Parpola 2010, *A Dravidian solution to the Indus script
   problem*** — **not held** (a metadata record only; the raw PDF
   stood on the retired Windows desktop); cannot be searched.
   Named limitation L2.
4. **Mahadevan 1977 sign list** — held dataset, transcribed from
   the pinned MASI 77 scan (SHA-256 `ef68fe8d…`); row lookup by
   Mahadevan sign number. Its columns carry number, variant
   marker, morphological class, and pages: it attributes no
   phonetic value and no meaning to any sign.
5. **Wells 1998 sign list** — held dataset, transcribed from the
   pinned thesis scan (SHA-256 `5720dc01…`); row lookup by the
   dataset's Mahadevan cross-reference. Wells attributes no
   phonetic value to any sign; his pictorial identifications are
   his own, not the entry's Parpola reading.
6. **The program's Parpola phoneme compilation**
   (`parpola_phonemes.json`, in-repo) — consulted by Parpola sign
   number as a pointer only; an in-repo table cannot ground a
   locator (WP4). 17 of the 184 entries are covered by it; 8
   entries record no Parpola number and cannot be consulted by key.

The expected shape of the run's census, stated before it runs so
the result is checkable against the prediction: with the primary
literature unheld, no held copy can ground a locator, so the pass
is expected to file **not-found for every entry and field
(phonetic 0 located / 184 not-found; semantic 0 / 184)** — the
measured outcome of a total pass over the program's actual
holdings, not a failure of the pass. What would change it is the
program acquiring the primary text (an owner act), not a different
search. The 17 compilation-covered entries are the named near-miss
population: the program's own compilation attributes a Parpola
proposal to each, sourced to passages (1994 Ch. 10 / fig. 5.1;
2010 sections) whose text the program does not hold, so no locator
can be filed for them from the record as it stands. They are
carried into the sample at a census (see §1) so the reviewer
rules on exactly those searches.

## 3. Tests and gates (actuals, from the run logs)

All runs executed on the mini-server in the CI-faithful venv
(`~/glossa-work/venvs/glossa-ci`), sequentially, on the quiet final
tree (the tree as committed, this record included; the suite's
in-tree side-effect files — 10 extracted-claims JSONs, the batch-4
claim report, `outputs/partial_loop_result.json` — were restored
path-by-path after the runs, as every stage does).

Targeted tests (`backend/tests/test_spec091_stage2_locator_pass.py`):
**6 passed, 2 skipped** — the six fixture tests (locator filed from
a held primary source; in-repo pointer never grounds a locator;
validator refusals ×3; execute-refusal on an absent held source)
pass; the two real-record tests (census totality; sample
verification) skip because the T202 run has not executed (§4).

Full backend suite, the CI invocation (from `backend/`:
`python -m pytest tests/ --tb=short -q`, GPU files ignored,
`test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
deselected by plain nodeid, CI authoritative), in the two-part
split at `test_spec086_ledger_gate.py`:

- Part A: **2904 passed, 68 skipped, 1 deselected, 0 failed**
  (626.29s), exit 0.
- Part B: **23 passed, 44 skipped, 0 failed** (570.95s), exit 0.
- Union: **2927 passed, 112 skipped, 1 deselected, 0 failed.**
  The stage's own 8 tests are in Part A (6 passed, 2 skipped as
  above). The known workspace-scope one-off ERROR did not recur.
  Wall times are the box's under its ClamAV on-access throttling
  and are not outcomes. No CI claim is made from these local runs.

Ruff: `ruff check` passes on both new Python files under the repo
config (`backend/pyproject.toml`).

Ledger gate (`tools/ledger/check_ledger_gate.py`), verbatim
summaries:

```
--all:           summary: 29 PASS / 0 FAIL / 1 NOT-RUN
                 RESULT: PASS
--regen:         summary: 32 PASS / 0 FAIL / 0 NOT-RUN
                 RESULT: PASS
--contamination: contamination class (Spec 095 T301, C095-7): 1025 presentations scanned, 0 flag(s)
                 CONTAMINATION: PASS
```

The standing profile, exactly, in all three modes.

## 4. The unblock (exact)

1. Owner-approved transfer, tower-compute → mini-server:
   - `glossa-run/m77-verify/v2_backup/m77_sign_list.csv` (+ `.json`)
     → `glossa-corpus/indus/sources/mahadevan-1977/` in the
     execution clone;
   - `glossa-run/wells1998-extract/wells1998_sign_list.csv` (+ `.json`)
     → `glossa-corpus/indus/sources/wells-1998/`.
   Hash note: the extraction record of record pins the landed M77
   dataset at CSV `ce5dd5a5…` / JSON `63059d64…`; the archive's
   surviving copy is the m77-verify v2 backup (CSV `ec26651f…` /
   JSON `774e8864…` per the archive manifest). The restored copy
   must be hash-read at restore time and the discrepancy either
   resolved (the pinned copy found) or carried into the run record
   as the searched copy's measured identity. The Wells extraction
   record pins CSV `22bde128…` / JSON `bdcb8ef3…`.
2. `python backend/scripts/spec091_stage2_locator_pass.py --execute`
   (mints the run id; writes the artifact + the run record).
3. `python backend/scripts/spec091_stage2_locator_pass.py --verify-sample`
   (files the sample verification), then the two skipped census
   tests in `backend/tests/test_spec091_stage2_locator_pass.py`
   activate and must pass; T202 ticks on that evidence plus the
   reviewer's oracle ruling.

## 5. Deviations

- The stage ships in two motions (this PR: T201 + the T202
  machinery + this record; the run PR follows the unblock) because
  the run's inputs are not on the execution box and their transfer
  is approval-gated. Nothing was searched that was not searched:
  no not-found outcome is filed anywhere in this PR.
- The tasks file's "run-defs v1" is the registered definitions'
  earlier version; the run machinery as it stands implements
  run-defs v2 (`glossa-indus/ledger/RUN-DEFINITIONS.md`), and the
  T202 run record will be written under it, on the `study`
  surface, whose store of record is the citing spec's `records/`.
- No frozen record was modified; no claim status, class,
  standing, or disposition was changed by this stage; no external
  contact was made and nothing was fetched or bought.

*This stage does not establish:* independence or eligibility — it
establishes where each reading can be found in the primary
literature, which is the input the independence test consumes.
(plan.md, Stage 2.) For this motion, it establishes the machinery
and the search design; the pass itself is §4's remainder.
