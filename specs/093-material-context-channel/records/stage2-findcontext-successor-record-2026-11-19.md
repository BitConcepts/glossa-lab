# Spec 093 Stage 2 — T202 find-context successor record (2026-11-19)

The successor attempt to Stage 2's find-context
administration, executed 2026-11-19 under freeze v2 at
the owner's order the same day Stage 2 landed. One
field, one new freeze, two runs, one independent audit,
one mechanical adjudication. The outcome is a second
**NOT YET**, landed as freeze v2's own rules direct:
the successor narrowed the obstruction and did not
clear it, and this record names what remains. No
claim's status, stage, or score was changed (C093-13);
no ledger, matrix, or map file is touched by this
landing; C093-1's standing is restated in §5 and is
unchanged.

## 1. The obstruction this attempt addressed

Freeze v1 adjudged find context on one stratified
70/30 split — 35 held-out records — and its control
battery's 99th-percentile κ was 0.1322, at or above
v1 §7's 0.10 validity ceiling (max 0.1351, mean
−0.0077; 11 of 200 permuted-label κ values at or above
0.10). Under v1 §7 the administration was invalid and
the field took NOT YET: the machinery, not the
channel, is what failed (Stage 2 record §T202). The
named defect was resolution: at n = 35 with five
classes, the null κ distribution is wider than the
ceiling any valid administration must sit under.

## 2. Freeze v2 — what changed, what did not

Freeze: `records/t202-findcontext-freeze-v2.md`
(SHA-256 `26444704…`), committed (`079f4a85`) before
any computation under it; the tools were committed
after it (`10e434f4`). It supersedes v1 for the
find-context field only.

**Changed: the evaluation design alone.** The single
70/30 split is replaced by repeated stratified 5-fold
cross-validation (10 repeats): every adjudged record
is predicted out-of-fold in every repeat, each repeat
pools its five folds into one confusion matrix over
all 125 adjudged records, and the adjudged statistic
is the repeat-mean κ (and repeat-mean balanced
accuracy). The control battery's statistic changed
with it — each of the 200 permutations is adjudged by
the same repeated cross-validation, and the battery
reports the distribution of repeat-mean κ.

**Not changed:** the pins, the population (175) and
adjudged class list (DKG. (S) 68, DKG. (N) 17, DK- 16,
HRB 13, VSA 11 — 125), the floors, the feature
construction, the predictor and its constants, the
recovery bar (κ ≥ 0.80 and balanced accuracy ≥ 0.85),
and the control validity ceiling (99th-percentile
control κ < 0.10). The ceiling was deliberately not
moved, and neither was the bar: C093-8 forbids
adjusting a threshold to convert a stop into a pass,
so the successor repaired the statistic's variance
and left every number it is judged against where
v1 put it.

## 3. The runs

| execution | run id |
|---|---|
| find-context administration (freeze v2) | `study-20261119T202359Z-72b357` |
| find-context control battery (freeze v2) | `study-20261119T202434Z-6d1f2a` |

**Administration.** Repeat-mean κ **−0.0468**,
repeat-mean balanced accuracy **0.1855** (majority
rule, for scale: κ 0.0, balanced accuracy 0.2). All
10 per-repeat κ values are negative (range −0.0730 to
−0.0181), and the pooled confusion (1,250 predictions)
is dominated by the majority class, as v1's was. These
numbers are recorded; under §4 they take no verdict.

**Control battery.** 200 permutations: repeat-mean κ
max **0.1207**, mean **−0.0007**, 99th percentile
**0.1106**; 3 of 200 values at or above 0.10. Against
v1's battery (max 0.1351, 99th percentile 0.1322, 11
of 200 at or above 0.10), the successor design
narrowed the null's upper tail on every measure — and
the 99th percentile still sits at or above the 0.10
validity ceiling.

**Audit.** `tools/spec093/audit_stage2_findcontext_v2.py`
— an independent implementation that does not import
the runner — recomputed both executions from the
pinned inputs under freeze v2 and compared result
blocks: **verdict AGREE**
(`records/t202-findcontext-audit-v2-2026-11-19.json`:
every result block matches exactly, header pins
verified against the files in the tree, no unexpected
successor runs). The mechanical adjudication is
`records/t202-findcontext-adjudication-v2-2026-11-19.json`
(`tools/spec093/check_stage2_findcontext_v2.py`,
gated on the audit).

## 4. The outcome under freeze v2

Under freeze v2 §6, the administration is valid only
if the battery's 99th-percentile κ̄ < 0.10. It is
0.1106. The administration is therefore invalid under
this freeze, and under §8 the field's outcome is:

**Find context — NOT YET** (second administration).
Freeze v1's NOT YET stands; freeze v2's runs are void
for adjudication and stand in the record as the
obstruction's evidence, exactly as v1's do. No
re-administration under freeze v2 repairs it
(C093-8).

**What the two attempts together establish about the
machinery** (an observation about the test, not a
verdict about the field): the remaining obstruction
is no longer split size. V2 removed the small-test-set
noise and the null's tail narrowed but did not clear
the ceiling, because the tail is a property of the
permuted-label distribution over this population
itself — 125 records, five classes, one class holding
68 of them, all from one site's excavation areas —
adjudged by a statistic whose repeats share the same
records and features and so do not average the
label-assignment variance away. Both freezes also
record, without adjudging, that the administration's
own statistic sits below its null's mean (v1: κ
−0.1309 against a null mean of −0.0077; v2: κ̄ −0.0468
against −0.0007, all 10 repeats negative). That is
the shape independence would take; it is not a
standing, and this record does not grant it one.

**What a further successor would have to change.**
Not the ceiling and not the bar (C093-8), and not the
split — v2 exhausted that axis. The remaining axis is
the control construction or the validity rule itself:
for example, a validity criterion stated as a
permutation test of the observed statistic against
its null distribution, or permutations blocked within
duplicate-sequence groups so the null prices the
population's redundancy honestly. Either is a design
decision above this record's authority — it changes
what "controls behaving as registered" means for this
spec — and nothing in this record commissions it.
The field stands NOT YET until such a freeze exists
and an administration under it is valid.

## 5. C093-1's standing, restated

Per-field outcomes after the successor: site **NOT
RECOVERED** (v1, valid controls); find context **NOT
YET** (v1 and v2 administrations both invalid as
frozen); material class, artifact type, and
holding/provenance **NOT ADMINISTERED** at v1's
forcing counts. No field was recovered under either
freeze. C093-1's standing is unchanged:

**INDEPENDENT IN PART** — the material-context
channel stands independent for **site**, the one field
any administration has validly tested and failed to
recover. Find context, material class, artifact type,
and holding/provenance carry no standing either way
and may not be cited downstream as channel data
(FR-093-04). Stage 4's bounds from the Stage 2 record
stand exactly as stated there.

## Verification on this tree

- Ledger gate (`tools/ledger/check_ledger_gate.py`,
  glossa-ci venv): default **29 PASS / 0 FAIL / 1
  NOT-RUN — RESULT: PASS**; `--regen` **32 PASS / 0
  FAIL / 0 NOT-RUN — RESULT: PASS** — the standing
  profile; this landing moves no ledger, matrix, map,
  or pin.
- The audit and adjudication above are the
  successor's own acceptance machinery (T202's
  acceptance mode is human-as-oracle: the reviewer
  against the freeze, the runs, and the bar — the
  freeze, the two run records, the audit's AGREE
  verdict, and this record are the surface that
  review reads).

*This does not establish:* that the surviving fields
say anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried
verbatim.)
