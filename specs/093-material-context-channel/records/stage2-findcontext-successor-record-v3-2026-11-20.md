# Spec 093 Stage 2 — T202 find-context successor record v3 (2026-11-20)

The third administration of Stage 2's find-context
field, executed 2026-11-20 under freeze v3, on the
owner's approval of git work in the tower-compute
clones given in the Glossa-Lab chat on 2026-11-20 at
19:51 ET (delegated-decisions package Item 5). One
field, one new freeze, two runs, one independent
audit, one mechanical adjudication. The outcome is
the first **valid** administration of this field:
the control battery clears the unmoved 0.10 validity
ceiling, and under the unmoved bar the field is
**NOT RECOVERED** — find context survives and joins
site in C093-1's surviving set. No claim's status,
stage, or score was changed (C093-13); no ledger,
matrix, or map file is touched by this landing;
C093-1's standing is restated in §5.

## 1. The obstruction this attempt addressed

Freeze v1 adjudged find context on one stratified
70/30 split — 35 held-out records — and its control
battery's 99th-percentile κ was 0.1322, at or above
v1 §7's 0.10 validity ceiling (max 0.1351, mean
−0.0077; 11 of 200 permuted-label κ values at or
above 0.10). Freeze v2 repaired the evaluation design
(repeated stratified 5-fold cross-validation, the
repeat-mean statistic over all 125 adjudged records)
and its battery's 99th-percentile κ̄ was 0.1106, still
at or above the ceiling (max 0.1207, mean −0.0007; 3
of 200 values at or above 0.10). Under both freezes
the administration was invalid and the field took NOT
YET: the machinery, not the channel, is what failed.
The v2 successor record named the remaining axis as
the control construction or the validity rule itself,
and the delegated package's decision of record chose
the control construction: the validity rule — the
0.10 ceiling — does not move.

## 2. Freeze v3 — what changed, what did not

Freeze: `records/t202-findcontext-freeze-v3.md`
(SHA-256
`0dea3b2b2738cc9221282803fb3a98001fd7296518c483dbe86de473335c64bd`),
committed (`57295768`, PR #625, merge `62f5eaca`)
before any computation under it; the tools were
committed after it (`d579bebe`). It supersedes v2 for
the find-context field only.

**Changed: the control construction alone**, in the
three particulars freeze v3 §6 registers, with the
methodological justification stated in the freeze
itself before computation (a permutation null must be
generated under the same statistic and exchangeability
structure as the test statistic it calibrates —
Fisher 1935 through Hemerik & Goeman 2018 — and the
freeze states why this is an instrument repair, not
ceiling-shopping):

- the identical-statistic registration made exact:
  every control value is a repeat-mean κ̄ computed by
  the administration's own §5 procedure — no
  single-draw statistic enters the battery anywhere;
- stratified permutation **within site** with matched
  marginals (v2 permuted labels globally): labels are
  shuffled only inside their site stratum, preserving
  each stratum's label marginals exactly. As freeze
  v3 §2 states plainly, all 179 joined pairs sit at
  Mohenjo-daro (the field's values are excavation
  areas within that one site), so the stratification
  realizes a single stratum of 125 adjudged records —
  recorded here as the runs themselves report it
  (`permutation_strata: {"Mohenjo-daro": 125}`);
- an ensemble of **2,000** control draws (v2 used
  200), so the 99th-percentile estimate (index 1979 of
  2,000 ordered values) is stable against single-draw
  movement.

This freeze's streams are its own (administration
`random.Random(20261123 + r)`; controls
`random.Random(20261124)`), registered in §§5–6.

**Not changed:** the pins (v3 §1 carries v1/v2's five
pins verbatim — each recomputed from the current tree
before the freeze was committed and reproducing — and
adds the v2 record chain; the one pin the preparation
draft left open, the SHA-256 of the v2 successor
record, `ff7c44ee…`, was completed from the tree at
the origin/main tip the freeze branches from and is
registered in §1 with its provenance), the population
(175) and adjudged class list (DKG. (S) 68, DKG. (N)
17, DK- 16, HRB 13, VSA 11 — 125), the floors, the
feature construction, the predictor and its constants,
the evaluation design (§5 is v2's), the recovery bar
(κ̄ ≥ 0.80 and BĀ ≥ 0.85), and the control validity
ceiling (99th-percentile control κ̄ < 0.10). The
ceiling was deliberately not moved, and neither was
the bar: C093-8 forbids adjusting a threshold to
convert a stop into a pass.

## 3. The runs

| execution | run id |
|---|---|
| find-context administration (freeze v3) | `study-20261121T011046Z-c0c843` |
| find-context control battery (freeze v3) | `study-20261121T011057Z-af6d5d` |

(Run ids carry the study surface's UTC clock,
2026-11-21T01:10–01:11Z, which is 2026-11-20
20:10–20:11 ET; the administration was executed
2026-11-20 ET, on tower-compute.)

**Administration.** Repeat-mean κ̄ **−0.0466**,
repeat-mean balanced accuracy BĀ **0.1846**
(majority rule, for scale: κ̄ 0.0, BĀ 0.2).
Per-repeat κ / balanced accuracy: r0 −0.0492 /
0.1888; r1 −0.0567 / 0.1831; r2 −0.0217 / 0.2072;
r3 −0.0323 / 0.1890; r4 −0.0414 / 0.1853; r5 −0.0181 /
0.1985; r6 −0.0633 / 0.1735; r7 −0.0638 / 0.1735;
r8 −0.0542 / 0.1765; r9 −0.0650 / 0.1706. All 10
per-repeat κ values are negative, as under v1 and v2.

**Control battery.** 2,000 permutations: repeat-mean
κ̄ max **0.1869**, mean **−0.0001**, 99th percentile
**0.0927**; 15 of 2,000 values at or above 0.10.
Against the ceiling: **0.0927 < 0.10 — the controls
are valid.** The battery's maximum shows individual
permuted draws can still reach high κ̄ values on this
population; the validity rule reads the 99th
percentile, as frozen since v1, and at the registered
ensemble size that estimate sits below the ceiling.
The narrowing against v2's battery (200 draws: max
0.1207, p99 0.1106) is in the tail estimate, exactly
where freeze v3 §6 said the 200-draw estimate carried
material Monte Carlo error.

**Audit.** `tools/spec093/audit_stage2_findcontext_v3.py`
— an independent implementation that does not import
the runner — recomputed both executions from the
pinned inputs under freeze v3 and compared result
blocks: **verdict AGREE**
(`records/t202-findcontext-audit-v3-2026-11-20.json`:
every result block matches exactly, header pins
verified against the files in the tree, no unexpected
successor runs). The mechanical adjudication is
`records/t202-findcontext-adjudication-v3-2026-11-20.json`
(`tools/spec093/check_stage2_findcontext_v3.py`,
gated on the audit).

## 4. The outcome under freeze v3

Under freeze v3 §6, the administration is valid only
if the battery's 99th-percentile κ̄ < 0.10. It is
0.0927. The administration is therefore valid, and
under §7 the field is RECOVERED iff κ̄ ≥ 0.80 and
BĀ ≥ 0.85. κ̄ is −0.0466 and BĀ is 0.1846. Under §8
the field's outcome is:

**Find context — NOT RECOVERED** (third
administration, first valid one). Find context
survives: it joins site in C093-1's surviving set,
and downstream claims may cite it as channel data at
exactly that strength.

Under freeze v3 §8's closing condition, this valid
outcome closes the freeze line on these inputs: no
further freeze re-adjudges this field on this
population. (Had the battery breached the ceiling,
the same condition would have closed the line at
three freezes with the field NOT YET, absent new
data; that branch did not occur.)

## 5. C093-1's standing, restated

Per-field outcomes after this administration:

| field | outcome | source |
|---|---|---|
| site | NOT RECOVERED | freeze v1, valid controls (κ 0.0297, BA 0.5092; control p99 0.0851) |
| find context | NOT RECOVERED | freeze v3, valid controls (κ̄ −0.0466, BĀ 0.1846; control max 0.1869, mean −0.0001, p99 0.0927) |
| material class | NOT ADMINISTERED | freeze v1 forcing counts (Steatite 176 adjudged alone; Clay 1, Faience 1 under the class floor; 1 empty of 179) |
| artifact type | NOT ADMINISTERED | freeze v1 forcing counts (3,085 sequence-bearing records, 1 distinct value 'seal'; join concurs 179 of 179) |
| holding/provenance | NOT ADMINISTERED | freeze v1 forcing counts (sequence ∧ holding copresence 0; join pairs carry no holding) |

No field was recovered under any freeze. C093-1's
standing is:

**INDEPENDENT IN PART** — the material-context
channel stands independent for **site and find
context**, the two fields administrations have
validly tested and failed to recover. Material
class, artifact type, and holding/provenance carry
no standing either way and may not be cited
downstream as channel data (FR-093-04). C093-1
continues to be cited per-field, now with find
context among the surviving fields. Stage 4's bounds
from the Stage 2 record stand exactly as stated
there.

*This does not establish:* that the surviving fields
say anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried
verbatim.)
