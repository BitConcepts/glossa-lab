# Meroitic Benchmark — Verdict Restatement (Spec 097)

**Date: 2026-11-20. This record restates the citation form of
the Spec 097 benchmark verdict, following the whole-program
red team of 2026-11-20 (findings F-02 and F-07). The original
outcome record
(`records/meroitic-benchmark-outcome-record-2026-11-20.md`)
is NOT edited and stands as filed; from this record onward,
the benchmark is cited in the restated form below, and the
single undifferentiated headline "NOT REPRODUCED" is not used
for the three legs together.**

## Leg A — census of the paper's published counts

**Cited as: REPRODUCED IN PART / DEPOSIT INCOMPLETE.**

The ten Leg A counts, in three tallies, from the numbers as
filed in the outcome record:

- **Exact: 4** — A1 (193 translated Meroitic entries), A6
  (1,729 Egyptian types), A8 (1,868 distinct Meroitic forms
  post-augmentation), A10 (782,761 words post-augmentation).
- **Positively contradicted: 2 counts, plus one Table 2
  size** — A9 (17,257 phrases post-augmentation published;
  18,090 deposited lines counted, Δ +833: the deposited file
  is not the exact augmented file the paper counted) and the
  Table 2 names size (18 published; 22 reproduced on the
  standalone-file basis, traced to repository state after
  publication).
- **Untestable for absence: 3** — A3 (302 Egyptian texts),
  A4 (708 Nubian pages), A7 (99,338 Egyptian tokens). The
  material these counts were taken from is not in the
  repository in any form, so no counting basis could confirm
  or contradict them. Absence of the material is evidence
  about the deposit, not a failed reproduction of the count.
- **Basis-unstated divergences: 2** — A2 (897 phrases; the
  frozen envelope brackets it, 878–907, and no frozen basis
  reproduces it exactly) and A5 (871 phrases
  pre-augmentation; closest frozen basis 872, Δ1). Both are
  the signature of a counting basis the paper did not state,
  on an intermediate the paper did not publish.

Application of the falsifier, shown both ways: as filed, 6 of
10 counts diverged and the C097-5 majority condition fired.
On the testable counts only, 4 exact of 7, with 2 positively
contradicted and 2 of the divergences basis-unstated (A2 and
A5 are both testable and are counted in the 7; A9 is the
second positive contradiction). The strength of the Leg A
result therefore rests on the deposit's incompleteness — the
counted intermediates and source materials were never
published (A2, A3, A4, A5, A7) or the deposited file is not
the counted file (A9) — which is the claim this leg
establishes. Every citation of Leg A carries the custody
caveat recorded in the step-0 identity record and restated
in the custody record filed with this sequence.

## Leg B — sign inventory and distribution

**Cited as: internal fixture calibration.**

Leg B's comparator is the program's own pre-existing fixture
(`meroitic.py`, 551 tokens, 19 signs), not a claim of Otten &
Anastasopoulos. Its result (attested set 22 under the full
fold, extras L, P, U; Spearman ρ = 0.314 / 0.258 against the
ρ ≥ 0.90 bar) is a finding about that fixture's fit to the
2025 corpus. It is not cited as a result about the paper.

## Leg C — alignment

**Cited as: independent reimplementation — headline pattern
reproduced, fixed points not held.**

The authors' alignment code was not retrievable (an
unpopulated gitlink), so Leg C ran the program's own
implementation of the published method. Under it, the
paper's 100-dimension headline pattern reproduces (training
accuracy at or below 20 percent, numerals best in the
primary arm in 2 of 3 seeds, no meaningful unseen transfer),
but the fixed points do not hold cell-for-cell (unseen
precision@10 not exactly 0 percent in the seeded cells; the
at-most-25 percent training band exceeded in some
non-100-dimension cells).

## Citation rule

From now on, any use of this benchmark's outcome — in this
repository, in the program's standings, or on any public
surface — cites Leg A as REPRODUCED IN PART / DEPOSIT
INCOMPLETE with its tallies, Leg B as internal fixture
calibration, and Leg C as independent reimplementation with
the headline pattern reproduced and the fixed points not
held. The original outcome record remains the evidence of
record for every number above; this record changes no
number, no claim standing, and no other program's record.
