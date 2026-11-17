# Spec 091 — Stage 3 first-leg record (T301 + T302), 2026-11-17

Executed on the mini-server in a fresh clone at base `b9232cfe`
(the Spec 091 Stage 2 merge) on branch `feat/091-s3-battery-v2`.
This leg covers T301 and T302 only; T303 is a separate later
commission and is not touched here. The historical battery and
every frozen record are untouched: their SHA-256 pins from the
T104 record were re-verified before and after the work
(historical battery `e7fa7c17…`, WP5 audit `c1382017…`, audit
script `8957a1d8…`).

## 1. T301 — Battery v2, no pass-by-default (C091-8, v2 side)

Battery v2 is a new file, `backend/scripts/phase48_medium_validation_v2.py`
(SHA-256 `68c0bcd6dc00c573545338dc70c23bbee05612b8e7a16ade9faa0372c98bdda6`),
battery id `phase48-battery-v2`. The historical script
(`backend/scripts/phase48_medium_validation.py`) stays frozen
under D-091-4 and is imported by the tests only as the contrast
oracle. v2's outcomes are tri-state — pass / fail / not_run —
and a not_run never counts toward a score. Every path enumerated
in Stage 1's T104 record is removed:

| Path | Historical behaviour | v2 behaviour |
|---|---|---|
| P2 positional, no expectation (hist. lines 116–117) | pass, 0 credits recorded | not_run `no_expectation—not_run` |
| P3 DEDR, reading too short (hist. lines 138–139) | pass, **9 credits** | not_run `too_short—not_run` |
| P6 bigram, reading char not in LM (hist. lines 157–158) | pass, **5 credits** | not_run `char_not_in_lm—not_run` |
| P7 bigram, no anchor neighbours (hist. lines 189–190) | pass, 0 credits recorded | not_run `no_anchor_neighbours—not_run` |
| Non-credit input default (hist. line 110) | a missing `avg_position` silently becomes 0.5, which satisfies CASE_MARKER_SUFFIX's minimum — a credit computed on an input that does not exist | not_run `avg_position_absent—not_run` (a missing role record is likewise not_run) |

Fixture evidence (T301 acceptance, test side): the fixtures live
in `backend/tests/test_spec091_stage3_battery_v2.py` and RUN
against both batteries. For each removed path, a fixture in which
the historical battery awards credit and v2 returns not_run —
all five contrasts hold. Genuine checks are proven preserved on
the same fixtures: a positional pass and fail, a DEDR exact-match
pass and a no-match fail, and a bigram neighbour pass come out
identical in both batteries; a synthetic sign whose every
historical pass would be a default scores 0 in v2 and is never
promoted. 14 tests in the file, all passing (the three T302
real-record tests among them, §2).

Two v2 construction decisions, stated here because they are part
of the battery's definition:

- **P8 determinism correction.** The genuine bigram path's
  top-5 was backend-dependent in the historical script (torch
  top-k when torch was importable, all continuations otherwise),
  so the same inputs could score differently by environment.
  v2 computes the top-5 deterministically from the LM itself
  (probability descending, character ascending on ties) and
  never imports torch. v2 runs are `deterministic` under the
  registered run definitions.
- **An unheld dataset is a not_run, never a scan.** Where an
  input the program does not hold is required, the check returns
  not_run with the reason, per sign. The historical loader's
  contrasting behaviour — a missing DEDR dataset became an empty
  entry list and was scored as ordinary no-match fails — is
  exactly the silent-absence shape v2 refuses (§2).

Gate (T301 acceptance): the foundation check, run the way the
program runs it (`_run_checks()` / `_summarize()` behind
`GET /api/v1/foundation/check`) over the tree with the battery's
code landed and its run inputs staged: **17 PASS / 0 FAIL /
0 WARN, overall PASS**. Filed at
`records/t301-foundation-check-2026-11-17.json`.

## 2. T302 — The re-run over the 28 + dispositions (C091-9, C091-13)

**Population.** Derived mechanically from the WP5 audit
(`docs/repair-2026-10-26/anchor-support-audit.json`,
`phase48_summary.promoted_signs_in_recorded_order`): the
recorded Phase-48 promotions standing at `requires_revalidation`
under disposition rule R5a — 28 signs, in recorded order: M328,
M059, M162, M391, M233, M089, M051, M336, M012, M305, M073, M013,
M060, M080, M057, M039, M063, M077, M018, M030, M017, M020, M004,
M014, M026, M034, M027, M041. The two remaining recorded
promotions, M367 and M048, stand at `insufficient_evidence`
under R4 (the GR-088-27 pair, outside Spec 091) and are recorded
in the run record as excluded, with the reason. Census: 28/28
accounted; the run refuses to execute on any other census.

**The run.** One run under the registered run definitions
(run-defs v2 — §4, deviation 1), surface `study`, battery v2,
executed once on the mini-server:

- Run id: `study-20261117T103816Z-a25969`
- Run record: `records/study-20261117T103816Z-a25969.json`
  (SHA-256 `4c0cfbc0a2e78c4262ce58f712e7e1c67ae49b3e21ec5bfe396d43463ef387ab`),
  indexed in `records/run-index.jsonl`; validates under
  `glossa_lab.run_records.validate_record`.
- Inputs pinned in the record: the frozen historical battery,
  the WP5 audit, the anchors file, the Holdat corpus and roles
  CSVs (hashes identical to the live origin's pins: corpus
  `62d14d2b…`, roles `eb6d3b6a…`), the Tamil LM, the T104
  enumeration, and battery v2 itself.

**Outcomes.** Checks across the 28: 47 pass / 4 fail / 33
not_run. Per check: positional — genuine pass for all 28 (the
WP5 reconstruction likewise records the positional credit as
genuinely measured for every promotion); DEDR — not_run for
all 28 (§4, deviation 2); bigram — 19 pass, 4 fail on executed
neighbour comparisons (M162 0/5, M336 0/5, M012 0/5, M077
1/4 = 25.0%), 5 not_run on the removed P6 path (M328, M059,
M233, M305, M039 — readings whose first character the LM does
not contain; the WP5 census counts exactly 5
missing-model-character default credits). Under the promotion
rule (score ≥ 2 of 3; a not_run never counts), and with the
disposition mapping stated in the battery before the run —
promoted → `supported_internal_only`, not promoted →
`insufficient_evidence`, both from the WP5 audit's own
disposition vocabulary:

- **`supported_internal_only` (19):** M391, M089, M051, M073,
  M013, M060, M080, M057, M063, M018, M030, M017, M020, M004,
  M014, M026, M034, M027, M041.
- **`insufficient_evidence` (9):** M328, M059, M162, M233,
  M336, M012, M305, M039, M077.

Consistency with the WP5 reconstruction, as a check on the run:
the three promotions WP5 recorded as standing on no
reading-sensitive non-default pass (M328, M059, M233) are all
among the nine. The nine are not a pure "defaults removed"
shadow of the historical outcome, and the difference is
attributable on the record: every one of the 28 carries
dedr = not_run because the DEDR dataset is not held (deviation
2), so no sign could earn a DEDR credit in this run, genuine or
otherwise. The dispositions are this run's measured outcomes
under the inputs the program actually holds, with the not_run
reason carried in every act; they are battery outcomes, and
per the task's own limit they do not establish independent
support for any surviving promotion.

**Acts.** Filed at `records/t302-reclassification-acts.json`
(SHA-256 `c3708e2ec47c63e67b48e791236381a090c22a1148237d8a8fed4d442b44cfab`):
28 reclassification acts (one per sign, `requires_revalidation`
→ the run's disposition, each carrying its run id, score, and
per-check outcomes) and one `evidence_retirement` act retiring
the Phase-48 medium-validation output as evidence for all 28
in the same motion (C091-9), superseded by this run. The acts
were written through the verified-write library; the frozen
WP5 audit, the anchors file, and the claims ledger are
unmodified — anchor dispositions live in the audit line, and
no act vehicle writes them into the ledger (the same absence
Spec 095 Stage 3 recorded for anchor standings; a vehicle
remains named work for the Spec 095 closeout). The ledger
gates below prove the ledger did not move.

Acceptance, test side: the recomputation check is built into
the test file — it re-derives the 28 from the WP5 audit,
recomputes every disposition from the run record's per-sign
outcomes through the battery's own disposition rule, and
asserts the filed acts match exactly (signs, from/to, scores,
per-check outcomes, retirement scope, census arithmetic). It
passes. Gate side: the foundation check over the touched data
(run record + acts in tree): **17 PASS / 0 FAIL / 0 WARN,
overall PASS**, filed at
`records/t302-foundation-check-2026-11-17.json`.

## 3. Claims discharged by this leg

- **C091-8** — on its v2 side: battery v2 exists as a new
  versioned battery in which every pass it awards is earned by
  a check that ran over present inputs; the four enumerated
  pass-by-default paths and the named input default are removed,
  each with a running fixture contrast. (The claim's historical
  side was discharged at Stage 1 by T104's enumeration.)
- **C091-9** — the 28 WP5 `requires_revalidation` promotions
  were re-run under battery v2 in one registered run; the
  historical Phase-48 output is retired as evidence for all 28
  by the retirement act filed in the same motion.
- **C091-13** — for this leg's population: every disposition
  above rests on the run record's per-sign outcomes and is
  recomputed exactly by the acceptance test. (The claim's T303
  side remains with that commission.)

## 4. Deviations and findings

1. **Run-defs naming (carried from Stage 2).** tasks.md's T302
   text says "run-defs v1"; the registered definitions as they
   stand are run-defs v2 (`glossa-indus/ledger/RUN-DEFINITIONS.md`).
   The run followed the registered v2 definitions. A tasks.md
   wording correction is a parent decision, not made here.
2. **The DEDR dataset is not held.** `reports/jambu-dedr` is an
   unpopulated submodule (pinned `d5050e5a…`) in the clone and
   in the live origin alike, and no `dedr_new.csv` exists
   anywhere on the box. The battery therefore could not execute
   its DEDR leg: not_run for all 28, reason
   `dedr_dataset_not_held—not_run` recorded per sign. This is
   the machinery's honest outcome for unheld data — no sign was
   smoothed into a pass or silently skipped, and the census
   stayed 28/28. If the dataset is restored to the program's
   holdings, a future run under a new commission could execute
   the leg; nothing in this record pre-judges that outcome.
3. **P8 determinism correction** (§1): the genuine bigram
   path's historical top-5 was environment-dependent; v2's is
   deterministic by construction. Recorded as part of the
   battery's definition, not as a change to any frozen record.
4. **Disposition mapping.** tasks.md names the acts but not
   their target vocabulary; the mapping used (promoted →
   `supported_internal_only`, not promoted →
   `insufficient_evidence`) is WP5's own disposition vocabulary
   for this population, stated in battery v2's docstring before
   the run executed, so the outcome is checkable against a
   pre-stated rule.
5. **Suite configuration episode, stated plainly.** The first
   full-suite Part A run was executed with the battery's run
   inputs (the two Holdat CSVs) still staged in the clone and
   produced 2 failures — `test_promotion_integrity.py::
   test_coverage_reported_unavailable_not_zero` and
   `test_spec095_release_gate.py::
   test_real_tree_anchor_and_corpus_components_pass` — both of
   which premise a corpus-absent tree (the CI configuration:
   `corpora/` is gitignored). With the staged copies removed,
   both tests pass on this tree, and the reported suite union
   (§5) is the full re-run in the CI configuration. The staged
   copies were execution inputs only, never part of the change;
   the run record pins their hashes.

## 5. Verification actuals

- Targeted: `tests/test_spec091_stage3_battery_v2.py` —
  14 passed (11 fixture/pin tests before the run, with the 3
  real-record tests skipping; all 14 after the run).
- Full backend suite (CI invocation, GPU files ignored,
  phase392 deterministic test deselected by nodeid), two-part
  split at `test_spec086_ledger_gate.py`, CI configuration:
  Part A 2918 passed / 68 skipped; Part B 23 passed /
  44 skipped. **Union: 2941 passed, 0 failed** (Stage 2's union
  was 2927; the delta is exactly this leg's 14 tests). Local
  only — no CI claim is made from local runs.
- Ledger gates, sequentially on a quiet tree, standing profile
  held exactly: `--all` **29 PASS / 0 FAIL / 1 NOT-RUN**;
  `--regen` **32 PASS / 0 FAIL / 0 NOT-RUN**; `--contamination`
  **1025 presentations scanned, 0 flags — PASS**. The filed
  acts did not move the ledger, as designed (§2).
- Ruff: clean on both changed Python files.
- Foundation checks: 17/17 PASS at both gates (§1, §2).
- A confirmation pass over the final tree (this record and the
  tasks ticks included) reproduced the gate profiles and suite
  counts above. In-tree suite side effects (extracted-claims
  JSONs, a claim report, `outputs/`, the foundation report)
  were restored path-by-path; the commit contains exactly the
  intended files, verified from `git show --stat`.

## 6. What remains

- T303 (the 5's site-statistics-arm revalidations) — the
  separate Stage 3 commission, on its own branch.
- The DEDR dataset's custody (deviation 2) — a parent decision:
  restore the jambu-dedr dataset to the program's holdings or
  leave the leg not_run by design.
- The anchor-standings-as-acts vehicle (named at Spec 095
  Stage 3) — if built, these 28 dispositions are its first
  candidates for ledger-side filing.
