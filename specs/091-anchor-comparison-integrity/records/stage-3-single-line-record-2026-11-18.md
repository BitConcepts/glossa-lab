# Spec 091 — Stage 3 (second leg): the checker-arm five's site-statistics arms, executed (T303)

**Date:** 2026-11-18 · **Spec:** 091-anchor-comparison-integrity ·
**Stage:** 3 (single-line revalidation), second leg ·
**Tasks closed by this record:** T303 · **Base:** main
`f44cef92ac243ed1327fe81aa44f2a4a3b0dae68`

## 1. Scope and naming

This record covers T303 only: the site-statistics-arm
revalidations of the five anchors Stage 1's T105 split determined
to rest on the checker arms (M042, M046, M108, M176, M342),
executed as one run under the registered run definitions, with
dispositions filed as acts per the checker's outputs. The first
leg (T301/T302, the Phase-48 subset's 28) is recorded in
`stage-3-battery-v2-record-2026-11-17.md`; this leg follows its
pattern.

Naming note, carried from the earlier legs: tasks.md's T302 text
names "run-definitions v1" while the registry's current version
is v2 (`glossa-indus/run-definitions/RUN-DEFINITIONS.md`,
"Version: 2.0"); this leg's run is recorded under the registry
as it stands (v2), the same discrepancy the Stage 2 and Stage 3
first-leg records carry.

The stage-record name follows the spec's own convention:
Stage 3's first leg filed `stage-3-battery-v2-record-2026-11-17.md`
after its task (T301's battery), so this leg files
`stage-3-single-line-record-2026-11-18.md` after Stage 3's name
in tasks.md ("Stage 3 — Single-line revalidation").

## 2. The population, derived mechanically from the T105 split

The runner derives its population from
`records/t105-checker-arm-split.json` at run time and refuses on
any census mismatch; nothing is hardcoded. The split's
determination, re-verified at the run:

| Sign | Reading | T105 class | WP5 audit status | Site-statistics arm | Phonotactic arm |
|---|---|---|---|---|---|
| M042 | vaN | R5b_restored_reading | requires_revalidation | required | not required |
| M046 | kaL | R5b_restored_reading | requires_revalidation | required | not required |
| M108 | kaL | R5b_restored_reading | requires_revalidation | required | not required |
| M176 | an/aṇ | R5c_phase48_cited_as_support | requires_revalidation | required | not required |
| M342 | ay/ā | R5c_phase48_cited_as_support | requires_revalidation | required | not required |

All five stand HIGH in `INDUS_FINAL_ANCHORS.json` with readings
matching the split. The split records no undeterminable member
among the five. The phonotactic arm is required for **none** of
the five — §6.

## 3. The arm, its checker, and its input

**Checker.** `glossa_lab.site_stats_v2.chi_square_independence`
(module version `site-stats-v2.0.0`, checker id `site-stats-v2`):
the corrected Pearson chi-square test of independence between a
sign's position distribution and site. It is the v2 checker the
repair program built for exactly this revalidation (the
historical Phase-69 routine it replaces hard-coded its degrees
of freedom, could only ever report p ∈ {0.0, 0.5, 1.0}, and
dressed degenerate tables with placeholder numbers —
`docs/repair-2026-10-26/README.md`). The v2 checker computes its
p-value, returns `INSUFFICIENT_DATA` with no numbers when a
table cannot support the test, and never returns an equivalence
verdict.

**The table.** The Phase-69 lineage construction, taken verbatim
from the guarded lineage script
`backend/scripts/phase69_site_stratification.py` (its docstring
carries the construction): seals grouped by `cisi_number`, signs
placed by position, a seal's site taken from its first row; per
site, the sign's [initial, medial, terminal] counts under the
lineage binning (position 0 of a multi-sign inscription →
initial; last position of a multi-sign inscription → terminal;
otherwise medial — a single-sign inscription counts medial);
sites sorted; a site's row enters the table iff the sign's total
at that site is ≥ 3.

**Input held.** The arm consumes the Holdat corpus — the same
input the lineage script and the foundation check consume
(`corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`).
It is held: SHA-256
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
(the roles CSV alongside it,
`eb6d3b6ae195a2570e098dc6779dbd6c7bea97da5c4714bf406c3bb98f9d2aaf`,
is the foundation check's second input; this arm does not
consume it). The foundation check's first line reads the staged
corpus directly: "Holdat corpus: 1,670 seals / 7,002 tokens /
390 signs" (§8). No arm is `not_run` for want of input, and no
substitute data was used. The CSVs are gitignored working data:
they were staged into the worker clone for the run and the
foundation check and removed before the ledger gates and the
suite, which run in the CI configuration (the configuration
effect the first leg's record §4.5 documents).

## 4. The disposition rule — this leg's one judgment, stated before the run

T303's text directs dispositions "per the checkers' outputs"
without naming the mapping; the mapping below was fixed in the
runner's docstring before the run executed, and the stage
reviewer is asked to rule on it as this leg's one judgment.

**Rule: every anchor whose arm executes moves
`requires_revalidation` → `insufficient_evidence`, and each act
carries the outcome kind its checker result determines** —
`difference_detected` (checker OK, p < 0.05),
`difference_not_detected` (checker OK, p ≥ 0.05), or
`insufficient_data` (checker INSUFFICIENT_DATA). A checker ERROR
would have refused the run outright; no dispositions would have
been filed on an errored arm.

The authorities the rule rests on:

- **C091-10** carries GR-088-03 candidate 2's falsifier into the
  spec: "the v2 checkers judge the support insufficient → the 5
  move to insufficient evidence, not back to supported."
  Candidate 3's contrasting falsifier ("they stay
  requires-revalidation until a non-checker line is adjudicated")
  belongs by its own text to the R5d four, not to these five.
- **C091-11**'s falsifier bars leaving any of the five at
  `requires_revalidation` after its arm ran, absent a GR-088-04
  dependency where the phonotactic arm was required; it is
  required for none of the five (§6), so no such naming is
  available.
- The checker's own doctrine and the program's standards: a
  non-significant difference test is **not** evidence of
  site-invariance — equivalence is a separate claim requiring a
  prespecified margin and an equivalence procedure
  (`site_stats_v2`'s module doctrine; Spec 095 STANDARDS Part
  II), and none is registered for this arm. The repair record
  states the standing position the historical claim was left in:
  "no site-invariance equivalence has been established" — the
  claim was withdrawn, not replaced. A `difference_not_detected`
  outcome therefore cannot re-earn a supported class; it is
  recorded as the outcome kind, and the disposition is
  `insufficient_evidence`.

## 5. The run and its results

Run `study-20261118T151605Z-4c5c8b` (surface `study`, seed
NO_SEED, environment `mini-server/linux`, stage pin
`stage-3-single-line`), executed by
`backend/scripts/spec091_stage3_site_stats.py` (SHA-256
`e035d89b39cdd7987b0a283364fc83fae3fb76cf831b7b3b913bfff2132445fb`)
over the pinned inputs (§9). Per anchor:

| Sign | Occurrences | Sites in table | Checker | χ² | df | p | Outcome kind | Disposition |
|---|---|---|---|---|---|---|---|---|
| M042 | 13 | Harappa, Mohenjo-daro | INSUFFICIENT_DATA | — | — | — | insufficient_data | insufficient_evidence |
| M046 | 11 | Harappa | INSUFFICIENT_DATA | — | — | — | insufficient_data | insufficient_evidence |
| M108 | 5 | (none) | INSUFFICIENT_DATA | — | — | — | insufficient_data | insufficient_evidence |
| M176 | 356 | 8 sites | OK | 22.8589 | 14 | 0.06261 | difference_not_detected | insufficient_evidence |
| M342 | 584 | 9 sites | OK | 25.2468 | 16 | 0.06559 | difference_not_detected | insufficient_evidence |

Notes on the three INSUFFICIENT_DATA outcomes: M042's 13
occurrences are all initial-position, so its table has a single
nonzero column; M046 has only one site at the ≥3 threshold; M108
has no site at the threshold (5 occurrences, all medial). In
each case the corrected checker returns INSUFFICIENT_DATA with
no statistic — where the historical routine reported placeholder
numbers for the same shapes. The two OK outcomes both carry the
checker's sparse-table warning (smallest expected counts 0.33
and 0.25, below 5; the asymptotic p-values may be inaccurate for
these tables), recorded in the run record with the results.
Census: 5 tested; by outcome kind 3 insufficient_data /
2 difference_not_detected / 0 difference_detected; by
disposition 5 insufficient_evidence.

## 6. The phonotactic arm — not required; the dependency named

Per the T105 split, the phonotactic arm is required for none of
the five and gates none of their dispositions. The acts file
records this explicitly (`phonotactic_arm` block): required_for
empty, gated_dispositions empty, and the dependency named —
**GR-088-04, the WP2 phonotactic certification leg** (the
linguist-certified rule set `phonotactics_v2` awaits) — so that
the absence is a recorded determination, not a silent omission.
No phonotactic verdict is produced for any anchor by this leg,
and no anchor is left at `requires_revalidation` on this
dependency (C091-11's T303 side). The phonotactic-gated
dispositions that do exist in the program belong to the R5d
four (M087, M165, M264, M311), whose sourcing is Stage 4's T403
leg, not this one.

## 7. The acts

`records/t303-reclassification-acts.json` (SHA-256
`0950ab83cbbfc42f0ba9f53f69a4562b6da9cd98ee6f744fda80df6f2996a6b9`),
written through the verified-write library in the T302 acts'
form: five reclassification acts, each carrying its basis (run
id, checker and module version, outcome kind, checker status,
statistic/df/p, the full table with excluded sites and all-site
counts) and its prior basis (the T105 disposition rule and the
support lines the WP5 audit recorded). Claims named on the
file: C091-10, C091-11, C091-13.

**No evidence-retirement act is filed by this leg** — a
deliberate difference from T302. T302 retired the Phase-48
battery's output as evidence because the battery itself was the
defective instrument. Here the defective instrument is the
historical Phase-69 site-stratification routine, which was
already superseded by `site_stats_v2` under the repair program
(its outputs were never carried as a live evidence line for
these five in the WP5 audit — the audit's lines for the five are
the GRAMMAR/distribution lines the acts record as prior basis).
Nothing in this leg retires a historical output; the acts move
standings, and the standings vehicle remains what it was: the
frozen WP5 audit and the claims ledger are unmodified by this
leg, and the anchor standings change only through these acts.

## 8. Acceptance and gates

**Acceptance (T303's criterion): the filed dispositions
recompute from the run record exactly.** The acceptance test
(`test_t303_dispositions_recompute_exactly`) re-derives every
act's outcome kind and disposition from the run record's
per-anchor checker results through the runner's own mapping
functions and compares basis fields (statistic, df, p, table)
value for value: **passes**. The population census is likewise
re-derived from the T105 record in-test and matches the run
record and the acts.

**Targeted tests** (`backend/tests/test_spec091_stage3_site_stats.py`,
14 tests): pre-run 10 passed / 4 skipped (the real-record tests
skip until the run artifacts exist); post-run **14 passed**.
The fixture side proves the lineage binning (including the
single-sign → medial case), the ≥3 site-inclusion boundary, and
the outcome mapping; one fixture runs the M176-shaped table
through the checker and asserts the computed p (≈ 0.063) is a
value the historical routine could never have emitted; the
frozen-input pins are asserted in-test (§9).

**Foundation check** over the touched anchor data, run with the
arm's inputs staged and filed at
`records/t303-foundation-check-2026-11-18.json`: **17 PASS /
0 FAIL / 0 WARN, overall PASS** (first check: "Holdat corpus:
1,670 seals / 7,002 tokens / 390 signs").

**Ledger gates**, run sequentially on the quiet tree after the
staged inputs were removed, holding the standing profile
exactly:

- `--all`: summary: 29 PASS / 0 FAIL / 1 NOT-RUN — RESULT: PASS
- `--regen`: summary: 32 PASS / 0 FAIL / 0 NOT-RUN — RESULT: PASS
- `--contamination`: contamination class: 1025 presentations
  scanned, 0 flag(s) — CONTAMINATION: PASS

**Full backend suite** (CI invocation from `backend/`, GPU
files ignored, phase392 deselected by plain nodeid), two-part
split at `test_spec086_ledger_gate.py`: Part A 2944 passed /
66 skipped / 1 deselected (exit 0), Part B 23 passed /
44 skipped (exit 0) — **union 2967 passed, 0 failed**. (Wall
times on the box were heavily inflated by the known on-access
scanning throttle; the counts, not the times, are the outcome.)

## 9. Pins

Frozen inputs, SHA-256, as pinned in the run record's key and
asserted by the test file:

- WP5 audit (`docs/repair-2026-10-26/anchor-support-audit.json`):
  `c1382017f44d63e7e811b71b77917d9e3bfb40849f95806987135bae895ea52a`
- T105 split (`records/t105-checker-arm-split.json`):
  `ae787ea2148591300b64012164098a5450638d408901f06b1f54e4fd34956347`
- Anchors (`backend/reports/INDUS_FINAL_ANCHORS.json`):
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
- Holdat corpus CSV:
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
- Phase-69 lineage script (`backend/scripts/phase69_site_stratification.py`):
  `24ef7c5c2773328e6517dacf2ec19630c20974213b469a7ab5f3ae9e96eef21f`
- Checker (`backend/glossa_lab/site_stats_v2.py`):
  `1e407232a6592d2d6092e41cc3b4c52fdb75d19f72189ceed70d2cc3e1e4da25`
- Verified-write library (`backend/glossa_lab/verified_write.py`):
  `84846e9597c56bef522d70a91c18374fdb13d5d5fb33b3a9c53f1f10574aee5c`

## 10. What this leg does not establish

These are checker-arm outcomes only. No independent support is
claimed for any anchor by this leg; no anchor's reading is
assessed; no WP5 disposition outside the five is touched; the
eligibility question (Stage 5's T501 recomputation) is not
engaged. The two `difference_not_detected` outcomes are
non-detections under a sparse-table warning, not findings of
site-invariance: no equivalence has been established for any of
the five, and the outcome kinds say exactly that much and no
more. What the leg settles is narrower and complete: the five
standings that rested on the defective checker arms have now
been judged by the corrected checker over the data the arm
consumes, and none of the five re-earns support from it — all
five stand at `insufficient_evidence` on the filed acts, with
the checker's own outputs preserved per anchor in the run
record for any later stage to recompute from.

## 11. Claims discharged by this leg

Per the spec's claim map (claims.md) and the acts/run records:

- **C091-10** — the five's runnable arms executed as runs under
  the registered definitions, dispositions filed as acts per the
  checkers' outputs, recomputation-exact: **discharged**.
- **C091-11** — the T303 side: the phonotactic arm is required
  for none of the five, no disposition is gated on it, the
  GR-088-04 dependency is named on the record, and no anchor is
  left at `requires_revalidation` by this leg: **discharged for
  this leg's population** (the claim's R5d side belongs to
  Stage 4).
- **C091-13** — the T303 side: this leg's population's
  reclassifications are filed as acts in the T302 form:
  **discharged for this leg's population**.

No other claim is discharged by this leg, and none is claimed
beyond what the run record and the acts show.
