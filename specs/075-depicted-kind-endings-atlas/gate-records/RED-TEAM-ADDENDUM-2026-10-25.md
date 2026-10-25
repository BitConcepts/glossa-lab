# Spec 075 — Red-Team Addendum to the Gate Records (2026-10-25)

Filed by the programme-wide red team of 2026-10-25. This addendum
sits beside the freeze's gate-records; it does not alter them,
the freeze digest, or any executed verdict. Spec 075's four
per-kind verdicts recompute exactly from the committed inputs
(verified independently three times in the red team) and stand
as executed. What follows corrects and completes the *record*
around them.

## 1. The floor's units (finding F-11, with C-1)

§4.5 set the sign floor from Asset A row counts ("object_goods,
22 at asset level") and gate 0.5 applied it to population member
signs (object_goods 24). The distinct-row census, recomputed
from `reports/phase441_results.json`'s `keyed_population`, is:
other 307 signs → 204 distinct rows; human 53 → 39; animal
39 → 29; **object_goods 24 → 19**; unidentified 133 → 133.
Under the floor's basis unit, object_goods stands at 19, below
the floor of 20. The execution followed the frozen operative
text; this addendum records the unit switch so no future reader
has to recompute it to see it. **For future specs, the governing
unit for a depicted-kind floor is the distinct depiction (Asset
A row), the unit the floor was set from.**

The same keying pools kinds: 199 of 556 keyed signs and 3,399
of 11,322 identified-kind occurrences (30.0%) inherit their
kind from a shared Asset A row. Exposure: human 46.1% of its
occurrences; other 37.0%; animal 25.3%; object_goods 2.7%. No
frozen sensitivity (S1/S2/S3) splits or excludes the grouped
signs; a split sensitivity is the named follow-up, and until it
runs, the human verdict carries the largest unstated exposure.

## 2. "Significant" and the p-value family (finding B-1)

The four Fisher p-values in the outcome record are per-kind and
uncorrected. Under a Bonferroni family level for four kinds
(α = 0.0125), human and object_goods pass; animal (p = 0.0200)
and other (p = 0.0295) do not. The word "significant" as applied
to "other" in the outcome record should be read as
"significant at the per-kind uncorrected level only." No
verdict word changes: the NOT SUPPORTED words rest on the
ratio bands, and "other" is INCONCLUSIVE regardless. Standing
rule from this addendum forward: any p-value that would mint a
SUPPORTED verdict inside a family is reported at the family's
corrected level.

## 3. What the sensitivity arms could and could not do (B-2)

Stated plainly, per arm: S2 (contested rows) and 074's S-A are
identity functions — Asset A v2 contains 0 contested rows, so
the arms could not have moved any number. S1 (drop borderline)
moved "other" from 1.0796 to 1.0043 — within 0.0043 of the NOT
SUPPORTED boundary — a nearer miss than "agreement in every
word" conveys. Future freezes should state each arm's
discriminating power in advance.

## 4. Recomputability of the population (finding B-3)

The verdicts recompute from committed inputs. The population
rests on two restricted-local inputs this record previously did
not path: `sanitized_corpus.json` (SHA-256 345241b1…, the
Shakti deposit) and the row-grades file (SHA-256 02394241…),
both held locally under the CISI/Shakti restricted discipline,
never in git. The population was reproduced exactly from the
deposit in the red team (3,045 rows / 557 signs / 550 in
sequences ≥ 2). 133 unidentified signs (481 occurrences) have
no per-sign table in the committed record; 190 of 3,045
corpus-wide final occurrences are therefore undecomposable
from the repo alone.

## 5. C2/C3 record limits (findings D-5, D-6)

- The C2 recomputer is recorded anonymously ("independent
  recomputer subagent"). Its session identity is not
  recoverable from the record as filed. The recomputer was of
  the same agent family as the drafter; by the programme's own
  principle the C2 record is a **consistency check, not
  independent origin**, and should be cited as such.
- The C3 verifier was the drafting session itself (session
  d02f80d3). The verdict-bearing set was designated by the
  drafting side (DD-075). F075-C01 and F075-C04 were arguably
  verdict-bearing but were neither designated nor sampled;
  their disposition is recorded here as **not sampled**, with no
  implication either way about their evidence.
- One C2 "agree" is an equality only under a stated rule: the
  pinned kind-count dict lists "sky_cycle": 0 and the
  recomputed dict omits the key. The freeze-gate hardening of
  2026-10-25 now encodes exactly this rule (a zero-count key
  omitted equals a zero-count key listed) and no other
  leniency.

## 6. The family disposition vs the pooled-verdict denial (F-10)

F075-C03's append ("the hypothesis is in question") is a
**claim-status disposition** under C03's own registered family
falsifier (falsified as a family only if every tested kind
returns NOT SUPPORTED — a condition not met, since "other" is
INCONCLUSIVE). It is not a pooled §5.2 verdict: no pooled rate,
pooled test, or pooled verdict word was computed, which is
what F075-C11's append denies. The two sentences are consistent
under this distinction, which the records previously left
undefined; it is defined here.

## 7. The 0.8695 gloss (finding D-7)

"Minimum propagated confidence 0.8695" in freeze.md §4 is an
artefact of the register's confidence propagation arithmetic
(a minimum over per-claim propagated values under the draft
cap), not a measure of the freeze's correctness, and it should
not be read as one. The aee note's wording ("every claim at
the cap" beside a minimum above the 0.70 cap) is internally
inconsistent as a gloss; the number itself is left as filed.

*This addendum establishes: the record's stated limits, in the
record. It does not establish: any change to Spec 075's
verdicts, which stand as executed.*
