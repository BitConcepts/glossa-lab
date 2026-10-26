# Spec 077 — Outcome (Phase 443, executed 2026-10-26)

The execution ran once, as frozen, after the freeze
merged (PR #417, merge commit 95da5dc8; freeze digest
a9d10a2ba4f8e03fe77f7815a9fbd9a8860270f3a7a56801f02458507250f55f).
Step 0 passed on every item (`step0-record.md`).
Machine record: `reports/phase443_results.json`.

## F077-C01 — NOT SUPPORTED. Closure word: SIGNARY NOT WITNESSED AT THE STATED LEVEL

Of the 557 population signs, **399 are witnessed**
under the frozen match rules — **71.63%**, against a
frozen bar of 90% (at least 502 of 557). The shortfall
is 103 signs. The numbers, all of them, on the record:

| Reading | Witnessed | Share |
|---|---|---|
| Raw (any witness list) | 399 / 557 | 71.63% |
| Ancestry-adjusted (root list, M77) | 399 / 557 | 71.63% |
| S1 (strictest ancestry reading) | 399 / 557 | 71.63% |
| S2 (registry-construction exclusion; excluded 0) | 399 / 557 | 71.63% |
| — of which witnessed in M77 | 399 | |
| — of which witnessed in Wells 1998 | 42 | |
| — of which witnessed in both | 42 | |
| — witnessed only in Wells 1998 | 0 | |

Why all four readings coincide: a population sign is
witnessed exactly when Registry v2's crosswalk gives
it at least one Mahadevan number (399 signs carry
one; every such number is a number of the M77 list).
Wells 1998, joined through Figure 3.6's pairings,
witnesses 42 signs — every one of them already
M77-witnessed, so the descendant list adds no sign,
exactly as the filed ancestry map said it could not
be counted on to do. The FF-4 collision administration
excluded no sign (§4 of the step-0 record).

**The gap list** (the §5 deliverable — the 158
unwitnessed signs by their Wells codes, in population
order): 036, 041, 042, 050, 056, 058, 059, 065, 067,
069, 082, 084, 092, 096, 132, 136, 138, 141, 143, 145,
150, 152, 157, 172, 173, 180, 191, 195, 219, 221, 224,
229, 230, 250, 252, 253, 257, 263, 276, 277, 278, 279,
298, 311, 316, 319, 320, 326, 328, 330, 351, 376, 381,
383, 386, 389, 401, 409, 410, 412, 424, 441, 442, 444,
445, 452, 479, 481, 490, 491, 494, 495, 501, 506, 514,
515, 516, 519, 521, 525, 528, 534, 541, 542, 552, 563,
576, 577, 585, 586, 596, 597, 606, 617, 620, 629, 640,
647, 681, 697, 698, 702, 710, 711, 712, 720, 723, 727,
728, 729, 748, 751, 775, 781, 791, 792, 793, 794, 795,
799, 808, 810, 811, 818, 821, 822, 824, 826, 828, 829,
830, 836, 838, 842, 843, 844, 849, 852, 855, 859, 862,
866, 872, 876, 879, 893, 897, 898, 910, 912, 914, 918,
919, 922, 933, 956, 958, 999. Token 999 is in the gap
by construction (it has no crosswalk entry at all).
These are the signs the crosswalk reaches only through
the Wells/ICIT side, or not at all — the shopping list
for ICIT-route questions if the owner opens Gate G1,
as the design states.

What this verdict means, in plain terms: the 557-sign
frame behind Rung 1 is a Wells-lineage frame. Counted
by sign number through the program's own crosswalk,
the older external tradition — Mahadevan's list and,
through it, Wells's own 1998 list — attests just
under three quarters of it, not the nine tenths the
claim stated. Rung 1's placement must be argued down
on this record, as the design's falsifier provides.

## F077-C02 — the attack ran; no identity is named; token 999 stands NO PUBLISHED IDENTITY

999's frozen reference behavior: 2 occurrences, 0
text-final (rate 0.0). The administered conditions: a
witness total of exactly 2, and a final rate of at
most 0.10 (at a total of 2, a final count of 0).

**39 witness signs meet both conditions** — the full
candidate table is in the machine record:

- **36 M77 signs** (Table I TOT 2, FIN 0): 11, 21, 27,
  31, 34, 36, 43, 44, 49, 64, 74, 77, 90, 105, 116,
  120, 143, 159, 199, 203, 213, 257, 309, 313, 324,
  335, 346, 355, 359, 362, 368, 369, 376, 378, 394,
  416. (A further 11 M77 signs have TOT 2 with FIN ≥
  1 and fail the second condition; the 12 unsettled
  Table I rows cannot be shown to meet either
  condition, per FF-7.)
- **3 Wells 1998 signs** (dataset total 2, Figure 3.6
  pairing's final rate 0.0): 438 and 439 (both paired
  to M77 178, FIN 0 of 35) and 533 (paired to M77 244,
  FIN 0 of 89). The remaining 56 Wells signs with
  total 2 have no Figure 3.6 pairing and cannot meet
  the second condition.

So the stated default's trigger — *no* witness sign
meeting both — did not occur; candidates exist. But
the frozen rule states a necessary condition ("only
if it matches on both"), not a sufficient one, and it
contains no further test and no tie-break. Thirty-nine
signs meet it. An identity that is 39 different signs
is not an identity, and none may be selected after
counting. **No identity is therefore named, and token
999 stands NO PUBLISHED IDENTITY** — its Spec 073
standing unchanged — with the 39-sign candidate set
filed as the attack's positive result: any future
published identity for 999 must come from this set or
rebut it. (The machine record's
`identities_meeting_both` is this candidate set; its
`verdicts` entry is read as this outcome states.)

In plain terms: 999's behavior in the population —
twice, never final — is not distinctive. Thirty-six
of Mahadevan's signs and three of Wells's share it
exactly. The two-condition attack cannot pick 999's
counterpart out of the older lists, for the same
reason M2's machinery could not discriminate: the
test is honest, and what it measures does not
separate.

## The file, claim by claim

- F077-C01: **NOT SUPPORTED** (closure word above).
- F077-C02: attack run as frozen; no identity named;
  999 stands **NO PUBLISHED IDENTITY**; candidate set
  of 39 filed.
- F077-C03: supported — every pin verified at step 0.
- F077-C04: supported — the census and 999's
  reference behavior reproduced exactly.
- F077-C05: supported as filed — the ancestry map
  stood; its consequence is visible in the count
  (the descendant list added no sign).
- F077-C06: supported — the 13 ids resolved on the
  record before counting; the administration
  excluded no sign, and the record says why.
- F077-C07 (S1): computed and reported — 71.63%,
  equal to the adjusted share, for the reason the
  claim states.
- F077-C08 (S2): administered as frozen — exclusion
  set empty, share equal to the raw share, reasoning
  and per-witness breakdown filed above.
- F077-C09: discharged — the gap list is filed
  above, all 158 signs.
- F077-C10: supported — the C02 arm ran only on the
  landed Table I in its FF-7 form, hash recorded at
  step 0 (c047c251…).

## What this outcome establishes / does not establish

It establishes: the population frame is witnessed by
the external lists at 71.63% by sign number under
the stated match rules — below the stated level, so
the signary is NOT WITNESSED AT THE STATED LEVEL and
Rung 1's placement must be argued down on this
record; the exact gap (158 named signs); and that
token 999's two-condition attack selects a 39-sign
candidate set and no identity.

It does not establish: that the 158 gap signs are not
real signs (the count measures attestation through
one crosswalk, under conservative rules — a sign the
crosswalk cannot key to Mahadevan counts as
unwitnessed whether or not the older lists contain
its counterpart under another division); that any
witnessed sign is the same sign beyond the
crosswalk's own claim; any reading's value; anything
about glyph shapes. Nothing here is a decipherment
result, and the script is not deciphered.
