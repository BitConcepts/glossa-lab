# Spec 091 — Stage 2, T202 run record (addendum to the stage-2 record), 2026-11-17

**Task:** T202 — the locator pass executed (the §4 remainder of
`records/stage-2-record-2026-11-17.md`).
**Branch / PR:** `feat/091-s2-t202-run` (PR number in the PR record).
**Base:** `b9232cfe` (main at commissioning; the Spec 091 Stage 2 merge).
**Claim:** C091-1 (pass side).
**Authority:** the owner approved the dataset transfer and the
execution of the locator pass in chat on 2026-11-17.
**Run id:** `study-20261117T105335Z-4d667e` (surface `study`, written
through `glossa_lab.run_records`; run record at
`records/study-20261117T105335Z-4d667e.json`, indexed in
`records/run-index.jsonl`). Per the stage-2 record §5, the run
machinery as it stands implements run-defs v2
(`glossa-indus/ledger/RUN-DEFINITIONS.md`); the tasks file's
"run-defs v1" is the definitions' earlier version.

## 1. Step 1 — the transfer (owner-approved)

Four files, tower-compute archive → this VM → the execution clone
on the mini-server, placed at the canonical source-store paths the
stage-2 record §4 names. SHA-256 was read at every hop; all three
readings are identical for every file:

| File | Canonical path in the clone | SHA-256 (archive = VM = box) |
|---|---|---|
| `m77_sign_list.csv` | `glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv` | `ec26651f1bcbb3081ee4cc4e0ce3c5c4b6e4aed104c6a581397947c6cf75caff` |
| `m77_sign_list.json` | `glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.json` | `774e886457771d0be4e0c81dbfb800f8abc0846c93d251217577999efa25516d` |
| `wells1998_sign_list.csv` | `glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.csv` | `22bde128551adbd6d91cd76bb41b4f40199ab3e45af76d500a1008d27c5bea95` |
| `wells1998_sign_list.json` | `glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.json` | `bdcb8ef32f5172e4d1ddbb057e4344bccbc7aeacc1928d86c2175c12290a4bf0` |

Archive sources: `glossa-run/m77-verify/v2_backup/` and
`glossa-run/wells1998-extract/` under
`/home/tpierson/Development/glossa-archive/`. The datasets are
gitignored source-store files (`glossa-corpus/.gitignore`:
`sources/`); they were placed for the run and are **not** in this
PR's commit (verified from `git status` and `git show --stat`).

**The M77 discrepancy, carried as a named finding (not resolved,
not smoothed).** The extraction record of record
(`glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list_extraction_2026-10-25.md`)
pins the landed M77 dataset at CSV `ce5dd5a5…` / JSON `63059d64…`.
The copy that survives in the archive, and the copy this pass
searched, is the m77-verify v2 backup: CSV `ec26651f…` / JSON
`774e8864…` (the JSON's hash is the one the in-repo visual
adjudication record lists for its adjudicated `m77_sign_list.json`,
121,812 bytes). The pinned copy was not found; the discrepancy is
carried, per the stage-2 record §4's instruction, as the searched
copy's measured identity: the run's declared input pins record the
searched files' actual hashes (M77 CSV `ec26651f…`; see §2), and
no record was edited to make them agree. The extraction record
stands unedited. **Wells carries no discrepancy:** both Wells
files hash exactly to their extraction-record pins (CSV
`22bde128…`, JSON `bdcb8ef3…`).

## 2. Step 2 — the run

`python backend/scripts/spec091_stage2_locator_pass.py --execute`
(detached on the mini-server, CI-faithful venv; log read back):

```
run_id:          study-20261117T105335Z-4d667e
artifact:        backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_locators.json
artifact_sha256: 0074f2cc36a13943c758969430d0fdc8e3a7d0f2c5250e1594c02601534f3ef0
run_record:      specs/091-anchor-comparison-integrity/records/study-20261117T105335Z-4d667e.json
```

The generator ran unmodified — no fix was needed or made. Its
declared input pins (in the artifact and the run record) are the
frozen provenance file `b7543523…`, the crosswalk `3c54ed09…`, the
phoneme compilation `2aee1d0c…`, the M77 sign list as searched
`ec26651f…`, and the Wells sign list as searched `bdcb8ef3…`.

`--verify-sample` then re-executed the sample's searches from
fresh reads and filed `records/t202-sample-verification.json`.

## 3. Census — and the comparison against the prediction

| Field | Located | Not-found | Examined |
|---|---|---|---|
| `phonetic_reading` | 0 | 184 | 184 |
| `semantic_reading` | 0 | 184 | 184 |

**The result AGREES with the stage-2 record §2's predicted census
exactly** (phonetic 0 located / 184 not-found; semantic 0 / 184),
stated there before the run so the result is checkable against it.
The pass is total: 184 examined of 184, every entry carrying
exactly one outcome per field (C091-1's census; its falsifier —
an entry with neither outcome, or a census below 184 — does not
fire). No entry's outcome diverges from the prediction, so there
is no surprising outcome to name; the population nearest to
located is the near-miss set of §5.

## 4. Sample verification

The rule as fixed in the stage-2 record §1, not redrawn: every
entry carrying a locator (a census — **0** such entries), plus
every 12th entry in sign order starting with the 1st (**16**),
plus every entry whose phoneme-map consultation hit (**17**). The
two sets overlap in one sign (M001), so the sample is **32**
unique entries; the filed verification's sampled set equals that
union exactly. Result: **`all_verified: true`** — for every
sampled entry and field, the re-derived outcome from fresh reads
matches the filed outcome (32/32 entries, 64/64 field outcomes).

## 5. The not-found documentation (completeness, verified)

Every one of the 368 field outcomes was checked mechanically
against C091-1's form: each not-found carries its documented
search — the sources consulted, in the registered order, each
step with status, method, per-entry facts, result, and the run
date (2026-11-17). The search opens with the entry's stated
source: for the 171 entries stated as "Parpola 1994 Appendix B"
the `parpola_1994` step itself documents the Appendix B pinpoint
and WP4's ruling on it; the 13 derivative-stated entries carry
their stated source first as its own step (spec 004 WS2 expansion
×5, Phase-28 predecessor table ×6, literature-synthesis label
×2), followed by the five registered sources in order (Parpola
1994 — not held, L1; Parpola 2010 — not held, L2; Mahadevan 1977
sign list — searched; Wells 1998 sign list — searched; the
phoneme compilation — consulted as a pointer only). No step in
any outcome is incomplete.

The **near-miss population** (the compilation attributes a
Parpola proposal to the sign, sourced to passages whose text the
program does not hold): **M001, M016, M047, M050, M053, M060,
M086, M087, M088, M091, M092, M099, M117, M124, M126, M145,
M147** — 17 signs, carried into the sample at a census so the
reviewer rules on exactly those searches. The **8 entries
recording no Parpola number** (M175, M211, M220, M261, M264,
M281, M311, M364) document the compilation step as not
consultable by key, with that reason stated in the step's facts.

T202's human-as-oracle leg — the reviewer rules the sampled
not-found searches were real searches of the named sources —
stands on the parent reviewer's ruling at gating, per the Stage 1
pattern; the documentation above is what that ruling reads.

## 6. Tests and gates (actuals, from the run logs)

All runs on the mini-server in the CI-faithful venv
(`~/glossa-work/venvs/glossa-ci`), sequentially, on the final
tree (this record and the T202 tick included; the suite's in-tree
side-effect files — 10 extracted-claims JSONs, the batch-4 claim
report, `outputs/partial_loop_result.json` — were restored
path-by-path after the runs, as every stage does).

Targeted tests (`backend/tests/test_spec091_stage2_locator_pass.py`):
**8 passed** — the six fixture tests plus the two real-record
tests (census totality; sample verification) that skipped in the
stage-2 PR pending this run. They now run and pass.

Full backend suite, the CI invocation (from `backend/`:
`python -m pytest tests/ --tb=short -q`, GPU files ignored,
`test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
deselected by plain nodeid, CI authoritative), in the two-part
split at `test_spec086_ledger_gate.py`:

- Part A: **2907 passed, 66 skipped, 1 deselected, 0 failed**
  (1078.66s), exit 0.
- Part B: **23 passed, 44 skipped, 0 failed** (1100.06s), exit 0.
- Union: **2930 passed, 110 skipped, 1 deselected, 0 failed**
  (the stage-2 union was 2927 passed / 112 skipped; the delta is
  the two formerly-skipped tests now passing, plus one further
  pass in Part A). The known workspace-scope one-off ERROR did
  not recur. Wall times are the box's under a concurrent suite
  and its ClamAV on-access throttling; they are not outcomes. No
  CI claim is made from these local runs.

Ruff: no Python file is changed by this PR (verified from the
commit's file list), so there is nothing to lint.

Ledger gate (`tools/ledger/check_ledger_gate.py`), verbatim
summaries, run on the final tree and reproduced identically in a
confirmation pass over the exact tree as committed:

```
--all:           summary: 29 PASS / 0 FAIL / 1 NOT-RUN
                 RESULT: PASS
--regen:         summary: 32 PASS / 0 FAIL / 0 NOT-RUN
                 RESULT: PASS
--contamination: contamination class (Spec 095 T301, C095-7): 1025 presentations scanned, 0 flag(s)
                 CONTAMINATION: PASS
```

The standing profile, exactly, in all three modes.

## 7. Claims and boundaries

**C091-1 is discharged on its pass side** (its artifact side was
discharged by the stage-2 PR): the pass is total over all 184
entries, each with an entry-level locator or a documented
not-found search, the census is 184/184, and the sample
verification passes. T202 is ticked in tasks.md on this evidence
plus the reviewer's oracle ruling at gating (§5).

No frozen record was modified; the frozen provenance file was
read, never written. No claim status, class, standing, or
disposition was changed by this run. No external contact was
made. *This does not establish:* eligibility — located readings
would still need independent coding (T401) before any class
moves; and here nothing was located, which is a measured property
of the program's holdings (the primary literature is unheld,
limitations L1/L2), not a defect of the pass. What would change
the census is the program acquiring the primary text — an owner
act, outside this task.
