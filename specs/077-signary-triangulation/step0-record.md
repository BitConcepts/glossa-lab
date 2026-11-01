# Spec 077 — Step-0 record (Phase 443 execution)

Executed 2026-10-26, after the freeze PR #417 merged
(merge commit 95da5dc8; freeze digest
a9d10a2ba4f8e03fe77f7815a9fbd9a8860270f3a7a56801f02458507250f55f).
Runner: `backend/scripts/phase443_signary_triangulation.py`;
machine record: `reports/phase443_results.json`. Every
step-0 item below was verified first-hand by the runner
at the run; the outcome is in `outcome.md`.

## 1. Pins — all verify

Registry v2 `42ab09fb…` ✓; Spec 075's machine record
`f55ae911…` ✓; M77 raw text (C-7) `11441e38…` ✓; anchors
`df0cf620…` ✓; M77 dataset v3 `9c619bfe…` ✓; Wells 1998
dataset `22bde128…` ✓; Figure 3.6 cross-references
`b0ef40da…` ✓; held Wells thesis `5720dc01…` ✓;
restricted-local corpus `345241b1…` ✓ and row grades
`02394241…` ✓ (read in place, cited by hash only).

## 2. Witness tables' actual columns — verified

Registry v2 carries exactly the 15 columns the frozen
spec's counting reads. The M77 dataset carries
`sign_no / variant_marker / status` among its columns;
the Wells dataset carries `sign_no / total /
mahadevan_xref_fig36 / status`; the Figure 3.6 file
carries `mahadevan_1977 / wells_1997`. Nothing was taken
from any artifact's self-description (the draft
amendment's binding rule).

## 3. Population reproduction — exact

Under Spec 075's frozen construction over the pinned
restricted-local inputs: **3,045 analyzable rows / 557
distinct signs / 550 in sequences of length ≥ 2**, and
token 999's reference behavior **2 occurrences, 0
text-final, final-position rate 0.0** — the frozen
census and FF-6's values reproduced exactly.

## 4. The 13 duplicated Mahadevan ids — resolution table filed

Each of M002, M050, M064, M076, M099, M103, M161, M167,
M168, M199, M216, M264, M409 is claimed by exactly two
parpola_1982 rows in the pinned registry (the pairs of
Spec 073's accounting, recomputed at the run and filed
in the machine record with each claiming row's
`wells_ids` set). FF-4 was administered as frozen. Its
effect on the count, stated plainly: **none** — every
population sign that reaches a Mahadevan number at all
reaches it through a row its own token selects, and the
witnessed count equals the count of signs with any
Mahadevan number (399, §5 of the outcome). The
collisions sit on the M77→registry direction, not on
the population→M77 direction this spec counts.

## 5. The per-sign Mahadevan table — built twice, cross-checked

Step 0 builds the per-sign Mahadevan number table by
two independent constructions (through the registry
maps; by direct row scan) and requires exact agreement
before counting. **399 of 557 signs carry at least one
Mahadevan number** under the crosswalk; the two
constructions agreed.

*First-invocation defect, recorded in full.* The
runner's first invocation produced a machine record
whose per-sign table was empty (0 of 557 witnessed):
its counting loop parsed the registry's `M097`-form
labels with a leading-integer parser written for bare
numbers, got no number for any label, and counted
nothing. The defect was caught on inspection of the
machine record before any record was filed — 0 of 557
is substantively impossible on a crosswalk whose joins
step 0 itself states (sign 001 → P121 → M097|M098) —
and the invocation is void: it is not the execution,
and no number from it is filed anywhere except this
paragraph and the preserved void output in the freeze
working papers. The runner was repaired (a label
parser for the `M###` form; the table moved into step
0 under the two-construction cross-check above) and
the execution then ran once, as frozen, with the
repaired runner. The frozen contract — bars, match
rules, administrations — was not touched; the repair
made the runner implement FF-3 as written.

## 6. Table I — landed in the FF-7 form; hash recorded

The adjudicated dataset landed in the canonical store
before the run: `m77_table1_occurrences.csv`,
**SHA-256
c047c2517474062db9eec508eccb62cd83cb2be045e1fc847fd426030f50b168**,
417 rows. Acceptance form verified at the run: (i)
every complete row satisfies TOT = SOL+INI+MED+FIN
(405 complete rows); (ii) the complete-row column sums
(177 / 2,886 / 6,695 / 2,567 / 12,325) plus the landing
record's stated residuals (13 / 124 / 501 / 409 /
1,047) equal the printed totals row (190 / 3,010 /
7,196 / 2,976 / 13,372) exactly; (iii) the rows with
empty cells are exactly the 12 signs the landing
record names as unsettled: **97, 102, 162, 167, 173,
179, 180, 181, 182, 183, 184, 185**. The landing
record is the M77 Table I extraction and adjudication
record of 2026-10-26 (Phase B). It also establishes,
and the outcome record carries, that the book's printed
totals exceed the sum of its printed per-sign rows by
about 390 with no printed row to support the excess —
the totals were evidently tallied from the author's
underlying counts. C02's arm therefore reads TOT/FIN
from the printed per-sign rows, as FF-7 froze.

## 7. Anchors

`INDUS_FINAL_ANCHORS.json` byte-identical before and
after the run (SHA-256 `df0cf620…` at both reads).

**Step-0 verdict: PASS on every item.** The counting
ran. Its results are in `outcome.md`.
