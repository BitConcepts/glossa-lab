# Spec 072 — Freeze Record (Parpola's Fish-Sign Family, Sign by Sign, in ICIT Numbering on the Shakti Corpus)

> ## FROZEN — 2026-10-22
>
> This contract was frozen on 2026-10-22 under
> the owner's freeze rulings of 2026-10-22 on
> the freeze-gate package for the five
> Shakti-corpus draft specs
> (`research_notes/
> shakti-freeze-gate-package-2026-10-22.md`,
> Spec 072 section). The AEE lifecycle hooks
> ran over the register first (recovered from
> the draft register 0.5-draft to 0.8-draft in
> three recovery rounds finished before the
> digest; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 035
> ordering). The freeze performed the
> freeze-stage step-0 acts of spec §3 in
> order — gates 0.1 and 0.2 asserted, the
> concordance act (gate 0.3) performed and
> pinned, classes and census (gate 0.4)
> computed as margins only, and the verdict
> line derived and recorded (gate 0.5 /
> OPEN-072-1) — all before any fish member
> was scored, as §5.3 requires. The freeze
> also files this spec's own OSF contract
> registration (OPEN-072-7;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-431** under this frozen contract,
> and only after the freeze has merged and a
> separate execution order is given. At the
> freeze itself no member's ending-follower
> fraction has been computed in either
> population.

## 1. Basis

The contract is the ICIT-native re-design of
Spec 048's question, commissioned by the
owner's readiness decisions of 2026-10-22
(decision 4): do the seven fish signs of
Asset F — the fish-family list frozen at Spec
044's step 0 (Mahadevan/Parpola 47, 48, 50,
52, 60, 145, 147) — behave as a family in
their positional profiles, when the family is
expressed in Wells/ICIT codes and measured on
the Shakti corpus? Spec 048 stands closed
exactly as recorded (STRICT CORPUS NOT
PINNABLE, gate 0.3); nothing in this freeze
amends, reopens, or re-runs it. Spec 048's
reference numbers (25.9% / 3.8%) and its 20%
verdict line are **not inputs** to anything
in this freeze (§5.3's exclusion, applied).

## 2. The owner's rulings — OPEN-072-1 … OPEN-072-10

- **OPEN-072-1 — the verdict line (DERIVED,
  recorded in §5 below).** The derivation
  rule of spec §5.3 is applied as drafted:
  the 95th percentile, nearest-rank, of the
  freeze-stage reference distribution of
  non-fish signs clearing the carried
  supported floor (total ≥ 20) on the primary
  (documented-lineage) population, measured
  from non-members only, before any member
  was scored. The distribution holds **86
  signs**; its 95th percentile (nearest-rank,
  rank 82 of 86) is **0.7647** (sign 226: 13
  ending followers of 17 bigrams); stated to
  three decimal places rounding up, the
  verdict line is **L = 0.765**. The
  distribution is neither degenerate (its
  95th percentile is neither 0 nor 1) nor
  below the draft's 30-sign floor, so the
  freeze does **not** fail as VERDICT LINE
  NOT DERIVABLE, and no fallback line —
  inherited, borrowed, or rounded from the
  carried 0.15 label — is substituted. The
  full reference record is
  `reference-distribution.json` in this
  directory (SHA-256
  `55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5`),
  and §5 below exhibits it in full.
- **OPEN-072-2 — the concordance basis and
  act (performed, recorded in §4 below).**
  Ruled per the draft: every member's
  Wells/ICIT identity is stated and pinned on
  the stated basis; any member that cannot be
  identified is named UNIDENTIFIED IN ICIT
  with its disposition ruled here — never
  dropped or substituted quietly. The
  governing basis and the unique-intersection
  rule are stated in §4; the outcome is five
  members identified and two named
  UNIDENTIFIED IN ICIT (M047, M052), whose
  disposition is the draft's proposed ruling
  DD-072-5, **confirmed**: excluded from
  both populations' weighting, reported in
  the headline block; their occurrence share
  in ICIT space cannot be measured (they
  carry no ICIT identity to count), and the
  execution's records will state that plainly
  in place of the draft's share wording.
- **OPEN-072-3 — denominator and as-stored
  readings (CONFIRMED as drafted).** (a)
  §5.2's denominator reading: the fraction is
  over bigrams whose first sign is the
  member; a final-position occurrence enters
  neither numerator nor denominator. (b)
  §5.1's as-stored reading: sequences counted
  as stored, in stored order, with no
  direction normalisation. With one
  clarification carried from the deposit's
  own gating, stated here so it is not a
  silent choice: the `000` placeholder is
  gated out of a sequence before any position
  or bigram is counted (the deposit's
  `chr_lib.gate` rule, and §5.1's "it forms
  no bigram, holds no position class").
- **OPEN-072-4 — carried cascade and
  chance-baseline posture (CONFIRMED as
  drafted).** The positional classes are
  computed per population under the carried
  Item 2 cascade (classification floor
  total ≥ 5; t_rate ≥ 0.60 TERMINAL_STRONG;
  i_rate ≥ 0.55 INITIAL_STRONG; m_rate ≥
  0.65 MEDIAL_STRONG; t_rate ≥ 0.40
  TERMINAL_MODERATE; i_rate ≥ 0.40
  INITIAL_MODERATE; otherwise MIXED). **No
  chance-baseline step is added** — the
  Phase-43 battery had none (Item 2 §2), and
  nothing was commissioned as a new element.
- **OPEN-072-5 — the majority-partition rule
  (CONFIRMED as drafted; flagged here as the
  freeze's substantive partition ruling).**
  DD-072-2's partition stands: over the
  tested members, a passing token-weighted
  share **above 50%** is FAMILY SUPPORTED,
  **below 50%** is FAMILY NOT SUPPORTED, and
  **exactly 50%**, or the §6 coverage
  condition (untested members carrying more
  of the identified family's primary
  occurrences than the tested members),
  is INCONCLUSIVE. Spec 048's 70% / 30%
  family lines are **not carried** — they
  were calibrated between the Phase-43
  reference points this design excludes as
  inputs. This is the more conservative of
  the partitions the draft put to the
  freeze: it claims the family's majority
  only on a strict majority of tested
  occurrences, and it sends the borderline
  to INCONCLUSIVE rather than to either side.
- **OPEN-072-6 — the grade-flip headline
  reading (CONFIRMED as drafted).**
  DD-072-6 stands: the headline outcome is
  the primary population's verdict; if the
  sensitivity's family word differs, the
  headline carries the GRADE-SENSITIVE flag
  and both verdicts are reported; a
  family-level grade-flip is not ruled
  INCONCLUSIVE instead. Any member-level
  grade-flip is reported as a finding, in
  the outcome record's first section.
- **OPEN-072-7 — OSF (FILED at this
  freeze).** The frozen spec files its own
  OSF contract registration under campaign
  decision E-1, following Specs 036–067. The
  filing record is `osf-spec-registration.md`,
  completed by append after filing.
- **OPEN-072-8 — phase number (ALLOCATED).**
  The execution phase is **Phase-431**.
- **OPEN-072-9 — pins re-asserted (PASS).**
  Every Shakti pin in spec §2 was re-asserted
  against the merged intake record
  (`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`,
  merged by PR #339, merge commit `bfc811df`)
  at gate 0.1 (§3 below): the pins agree
  exactly; P-F1 (S1–S4) is confirmed as
  adopted in the form the draft cites.
- **OPEN-072-10 — the Roif gate (CONFIRMED
  in its drafted form).** Per the owner's
  ruling: no publication of this spec's
  results in any form without (i) citation of
  Roif 2025a (Academia.edu doc 129921039) and
  Roif 2025b (Academia.edu doc 143222807) and
  (ii) the owner's clearance of the specific
  act, regardless of outcome (spec §7 limit
  1; claim F072-C14). The gate constrains
  publication, not execution. Nothing is
  published under this freeze.

Draft decisions DD-072-1 … DD-072-6 are
**confirmed** as drafted, with DD-072-5's
disposition wording completed as recorded
under OPEN-072-2 above (an unidentified
member's ICIT occurrence share is not
measurable and is reported as such).

## 3. Step 0 at the freeze — gates 0.1 and 0.2

- **Gate 0.1 — Shakti intake assertion
  (P-F1 S1/S2): PASS.** Recomputed on the
  held restricted-local files at the freeze:
  the corpus file's SHA-256 is
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`
  and the row-grades file's SHA-256 is
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`,
  both equal to the merged intake record's
  pins. The census reproduces exactly:
  5,704 rows; 5,536 analyzable; grades 3,212
  documented-lineage / 2,087
  undocumented-corroborated / 405
  undocumented-uncorroborated; 4,904 of 5,536
  analyzable rows (88.6%) carrying a CISI
  identifier (the corpus's `-` placeholder
  counts as no identifier); 18,065 true sign
  tokens; 713 distinct signs; 77 sites. The
  spec therefore does **not** close as
  SHAKTI INTAKE NOT REPRODUCED. Execution
  step 0 re-asserts this gate on the same
  files before counting (spec §3).
- **Gate 0.2 — Asset F digest assertion:
  PASS.** Asset F's canonical file
  (`specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`)
  was exhibited, and its digest recomputed
  under Spec 044 §4.2's rule (SHA-256 of the
  canonical bytes — `json.dumps` with
  indent 2, keys sorted, `ensure_ascii=False`,
  plus a trailing newline — with the
  `digest` field excluded):
  `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`,
  equal to the recorded pin; member count 7;
  `frozen_at` 2026-10-21. The spec therefore
  does **not** close as ASSET F DIGEST
  MISMATCH or ASSET F NOT AVAILABLE.

## 4. Gate 0.3 at the freeze — the concordance act

**The governing basis (confirmed,
OPEN-072-2).** Two held files, each pinned
by SHA-256 at this act:

- `data/crosswalks/canonical_sign_registry.csv`
  — SHA-256
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`
  (803 data rows; carries a `wells_ids`
  column per registry sign, keyed by
  `parpola_id`);
- `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
  — SHA-256
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`
  (192 data rows; ICIT/Yajnadevam glyph
  numbers to Parpola matches, with review
  status).

`data/crosswalks/sign_crosswalk_master.csv`
(SHA-256
`4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`)
was considered and does **not** govern: it
carries registry sign ids across numbering
systems but no Wells/ICIT code, so it cannot
state an ICIT identity. The programme's
curated Mahadevan–Parpola crosswalk
(`backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`,
SHA-256
`9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b`,
spec §2's locator source) was considered and
does **not** govern the ICIT identity: its
`wells_id` values for this family (W008,
W009, W010, W011, W012, W040, W042) appear in
neither basis file, and ICIT codes 008–042
are absent or near-absent in the pinned
corpus (008, 009, 010, 011, 040 occur zero
times; 012 three times; 042 twice) — it is
Asset F's locator to Parpola's published
list, not a Wells/ICIT concordance.

**The stated rule.** Keyed by the member's
Parpola number (Asset F records Mahadevan
and Parpola numbers equal for every member;
the Parpola number is the asset's own
locator), a member's ICIT identity is the
**unique code in the intersection** of (a)
the `wells_ids` of the registry row for that
Parpola number and (b) the glyph ids of the
crosswalk's **confirmed** rows whose
`best_parpola_match` is that Parpola number.
If the intersection does not hold exactly
one code, the member is **UNIDENTIFIED IN
ICIT** on this basis. ICIT codes are stated
as they appear in the pinned corpus file
(zero-padded three-digit strings).

**The act, member by member:**

| Member | Parpola | Registry entry (basis a) | Crosswalk entry (basis b) | ICIT identity |
|---|---|---|---|---|
| M047 | 47 | P047 → wells_ids `W517\|W518` | no confirmed row for P047 | **UNIDENTIFIED IN ICIT** — the intersection is empty: the registry splits the sign across two Wells codes and the crosswalk confirms neither |
| M048 | 48 | P048 → `W243` ("Fish with no arms, caret hat, diagonal hatching throughout") | glyph 243 → P048, confirmed, confidence 1.0 (1 of 1 alignments) | **243** |
| M050 | 50 | P050 → `W220` ("Fish with no other decoration") | glyph 220 → P050, confirmed, confidence 0.931 (27 of 29 alignments) | **220** |
| M052 | 52 | P052 → `W944` ("Fish and 'table' with four small vertical strokes around the four corners") | no confirmed row for P052 | **UNIDENTIFIED IN ICIT** — the intersection is empty: a single registry code stands unconfirmed by the second basis |
| M060 | 60 | P060 → `W235` ("Fish with a caret shaped hat") | glyph 235 → P060, confirmed, confidence 1.0 (13 of 13 alignments) | **235** |
| M145 | 145 | P145 → `W032` ("Two adjacent full-height vertical strokes") | glyph 32 → P145, confirmed, confidence 0.9565 (22 of 23); glyph 600 also names P145 (1 of 1) but the registry assigns W600 to P262, so 600 is not in the intersection | **032** |
| M147 | 147 | P147 → `W033` ("Three adjacent full-height vertical strokes") | glyph 33 → P147, confirmed, confidence 1.0 (10 of 10 alignments) | **033** |

Five members are identified; two are named
UNIDENTIFIED IN ICIT, with the disposition
ruled under OPEN-072-2. Because at least one
member is identified, the spec does **not**
close as CONCORDANCE FAILED.

**Named divergences, reported not smoothed
(the gate-0.3 cross-check, for the record
only).** (1) The registry's depiction notes
for P145 and P147 describe stroke signs, and
its P047 describes a decorated vertical
line, where Asset F's depiction notes for
the same Parpola numbers describe fish
signs; its P048, P050, P052 and P060 notes
do describe fish. The concordance above is
a **numbering** concordance — Parpola number
to ICIT code on the stated basis — exactly
the act gate 0.3 commissions; membership
remains Asset F's, exactly as frozen, and
this divergence is a finding about the held
bases, carried into the execution's headline
block. (2) Asset F against the claim
record's named trio (Mahadevan 72, 64, 70)
and the Phase-43 six candidates (267, 72,
65, 59, 60, 70): Asset F holds none of 267,
72, 65, 59, 64, or 70; of the Phase-43 six
only 60 appears, as M060. The cross-check
adds and removes no member.

## 5. Gate 0.5 at the freeze — the reference distribution and the line

The reference distribution was produced at
this freeze, from non-members only, before
any member was scored: the ending-follower
fraction (§5.2's definition, OPEN-072-3's
readings) of every non-fish sign in the
primary population clearing the carried
supported floor (total ≥ 20). The family
codes excluded are the five identified at
gate 0.3 (032, 033, 220, 235, 243); the two
unidentified members carry no ICIT code and
so cannot enter the distribution. No sign
clearing the floor had zero bigrams. The
record is pinned as
`reference-distribution.json` (SHA-256
`55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5`);
its entries, in full:

| Rank | Sign | Total | Bigrams | Ending followers | Fraction |
|---|---|---|---|---|---|
| 1 | 501 | 30 | 1 | 0 | 0.0000 |
| 2 | 752 | 47 | 46 | 2 | 0.0435 |
| 3 | 090 | 110 | 102 | 5 | 0.0490 |
| 4 | 503 | 68 | 17 | 1 | 0.0588 |
| 5 | 416 | 37 | 14 | 1 | 0.0714 |
| 6 | 745 | 20 | 12 | 1 | 0.0833 |
| 7 | 400 | 355 | 354 | 31 | 0.0876 |
| 8 | 142 | 51 | 34 | 3 | 0.0882 |
| 9 | 055 | 45 | 33 | 3 | 0.0909 |
| 10 | 350 | 24 | 21 | 2 | 0.0952 |
| 11 | 335 | 31 | 30 | 3 | 0.1000 |
| 12 | 585 | 36 | 36 | 4 | 0.1111 |
| 13 | 690 | 72 | 60 | 7 | 0.1167 |
| 14 | 803 | 102 | 59 | 7 | 0.1186 |
| 15 | 061 | 74 | 54 | 7 | 0.1296 |
| 16 | 407 | 113 | 113 | 15 | 0.1327 |
| 17 | 034 | 124 | 7 | 1 | 0.1429 |
| 18 | 176 | 167 | 91 | 13 | 0.1429 |
| 19 | 413 | 40 | 7 | 1 | 0.1429 |
| 20 | 820 | 144 | 32 | 5 | 0.1562 |
| 21 | 005 | 40 | 18 | 3 | 0.1667 |
| 22 | 741 | 148 | 134 | 23 | 0.1716 |
| 23 | 440 | 33 | 23 | 4 | 0.1739 |
| 24 | 031 | 142 | 88 | 16 | 0.1818 |
| 25 | 630 | 27 | 11 | 2 | 0.1818 |
| 26 | 742 | 26 | 22 | 4 | 0.1818 |
| 27 | 003 | 184 | 70 | 13 | 0.1857 |
| 28 | 231 | 63 | 43 | 9 | 0.2093 |
| 29 | 236 | 23 | 19 | 4 | 0.2105 |
| 30 | 617 | 56 | 44 | 10 | 0.2273 |
| 31 | 798 | 93 | 65 | 15 | 0.2308 |
| 32 | 004 | 62 | 38 | 9 | 0.2368 |
| 33 | 850 | 32 | 24 | 6 | 0.2500 |
| 34 | 520 | 246 | 245 | 62 | 0.2531 |
| 35 | 920 | 108 | 47 | 12 | 0.2553 |
| 36 | 001 | 128 | 121 | 31 | 0.2562 |
| 37 | 904 | 36 | 31 | 8 | 0.2581 |
| 38 | 740 | 1299 | 1296 | 338 | 0.2608 |
| 39 | 760 | 87 | 80 | 21 | 0.2625 |
| 40 | 016 | 34 | 19 | 5 | 0.2632 |
| 41 | 240 | 254 | 187 | 50 | 0.2674 |
| 42 | 151 | 69 | 68 | 19 | 0.2794 |
| 43 | 388 | 32 | 25 | 7 | 0.2800 |
| 44 | 482 | 31 | 28 | 8 | 0.2857 |
| 45 | 384 | 21 | 17 | 5 | 0.2941 |
| 46 | 705 | 135 | 93 | 28 | 0.3011 |
| 47 | 706 | 70 | 43 | 13 | 0.3023 |
| 48 | 100 | 90 | 85 | 26 | 0.3059 |
| 49 | 595 | 29 | 26 | 8 | 0.3077 |
| 50 | 717 | 33 | 19 | 6 | 0.3158 |
| 51 | 255 | 91 | 53 | 17 | 0.3208 |
| 52 | 590 | 160 | 118 | 40 | 0.3390 |
| 53 | 390 | 202 | 196 | 67 | 0.3418 |
| 54 | 415 | 117 | 75 | 26 | 0.3467 |
| 55 | 892 | 61 | 51 | 18 | 0.3529 |
| 56 | 806 | 103 | 52 | 19 | 0.3654 |
| 57 | 455 | 25 | 19 | 7 | 0.3684 |
| 58 | 017 | 62 | 45 | 17 | 0.3778 |
| 59 | 790 | 24 | 18 | 7 | 0.3889 |
| 60 | 550 | 77 | 43 | 17 | 0.3953 |
| 61 | 233 | 136 | 108 | 43 | 0.3981 |
| 62 | 013 | 23 | 10 | 4 | 0.4000 |
| 63 | 125 | 44 | 30 | 12 | 0.4000 |
| 64 | 692 | 41 | 5 | 2 | 0.4000 |
| 65 | 900 | 71 | 60 | 24 | 0.4000 |
| 66 | 405 | 87 | 86 | 43 | 0.5000 |
| 67 | 527 | 48 | 46 | 23 | 0.5000 |
| 68 | 140 | 66 | 38 | 20 | 0.5263 |
| 69 | 156 | 90 | 90 | 49 | 0.5444 |
| 70 | 154 | 31 | 31 | 17 | 0.5484 |
| 71 | 840 | 81 | 63 | 35 | 0.5556 |
| 72 | 158 | 26 | 25 | 14 | 0.5600 |
| 73 | 368 | 71 | 67 | 38 | 0.5672 |
| 74 | 923 | 37 | 34 | 20 | 0.5882 |
| 75 | 070 | 24 | 23 | 14 | 0.6087 |
| 76 | 575 | 51 | 39 | 24 | 0.6154 |
| 77 | 817 | 140 | 13 | 8 | 0.6154 |
| 78 | 002 | 549 | 542 | 343 | 0.6328 |
| 79 | 861 | 193 | 78 | 51 | 0.6538 |
| 80 | 845 | 47 | 47 | 31 | 0.6596 |
| 81 | 460 | 26 | 24 | 17 | 0.7083 |
| 82 | 226 | 21 | 17 | 13 | 0.7647 |
| 83 | 060 | 158 | 157 | 130 | 0.8280 |
| 84 | 435 | 52 | 51 | 47 | 0.9216 |
| 85 | 615 | 55 | 50 | 47 | 0.9400 |
| 86 | 700 | 384 | 376 | 363 | 0.9654 |

**Derivation.** Sorted ascending, the 95th
percentile by the nearest-rank method is
the value at rank ⌈0.95 × 86⌉ = 82:
**0.7647** (sign 226, 13 of 17 bigrams).
Recorded to three decimal places, rounding
the percentile value **up** at the fourth
decimal place, the verdict line is

> **L = 0.765**

A member PASSES at execution iff its
primary-population ending-follower fraction
is at or above 0.765 and it clears the
carried supported floor (total ≥ 20) (§5.3).

## 6. Gate 0.4 at the freeze — classes and census (margins only)

Positional classes were computed on both
populations under the carried cascade
(OPEN-072-4) as margins for the reference
distribution and this census; no member's
ending-follower fraction was computed. The
per-member census (occurrence totals in
sequences of length ≥ 2, `000`-gated,
as stored):

| Member | ICIT | Primary total | Primary class | Sensitivity total | Sensitivity class |
|---|---|---|---|---|---|
| M047 | UNIDENTIFIED IN ICIT | — | — | — | — |
| M048 | 243 | 9 | NOT SCANNED | 12 | SCANNED — BELOW SUPPORTED FLOOR |
| M050 | 220 | 286 | TESTABLE | 426 | TESTABLE |
| M052 | UNIDENTIFIED IN ICIT | — | — | — | — |
| M060 | 235 | 188 | TESTABLE | 240 | TESTABLE |
| M145 | 032 | 334 | TESTABLE | 501 | TESTABLE |
| M147 | 033 | 315 | TESTABLE | 433 | TESTABLE |

Four identified members are testable in the
primary population, so the execution does
not close at gate 0.4 as TOO THIN on the
freeze-stage census (execution step 0
re-derives this census on the asserted
files; the freeze-stage figures stand as
the freeze's exhibit).

## 7. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/072-fish-family-profiles-redesign/freeze.md` (this document)
- `specs/072-fish-family-profiles-redesign/spec.md`
- `specs/072-fish-family-profiles-redesign/claims.json`
- `specs/072-fish-family-profiles-redesign/adjudication.md`
- `specs/072-fish-family-profiles-redesign/reference-distribution.json`
- `specs/072-fish-family-profiles-redesign/aee/freeze-aee-note.md`
- `specs/072-fish-family-profiles-redesign/build_freeze.py`
- `backend/tests/test_spec072_freeze.py`

`tasks.md` is lifecycle bookkeeping and is
not digest-covered (the house rule since
Spec 026: plans change as work proceeds).
`osf-spec-registration.md` is the filing
record for OPEN-072-7: it is completed by
append after the filing exists, and the
filing carries this freeze's digest — so it
cannot itself be a digest-covered source.

## 8. What the freeze fixes

- **The verdict line** (§5.3 / F072-C09):
  L = 0.765, derived at this freeze from the
  pinned reference record under the fixed
  rule; the Phase-43 points and Spec 048's
  20% bar excluded as inputs in any form.
- **The family in ICIT numbering** (§3 gate
  0.3 / F072-C10): the concordance of §4 —
  five members identified (243, 220, 235,
  032, 033), two named UNIDENTIFIED IN ICIT
  (M047, M052) under the confirmed DD-072-5
  disposition.
- **The populations and the measure**
  (§§5.1–5.2 / F072-C07, C08): documented-
  lineage primary; documented +
  undocumented-corroborated sensitivity
  mandatory; undocumented-uncorroborated
  rows in nothing; sequences as stored,
  `000`-gated; the denominator reading and
  the carried cascade and floors as
  confirmed (OPEN-072-3, OPEN-072-4).
- **The partition** (§6 / F072-C03, C04):
  the majority partition of OPEN-072-5, with
  its coverage condition. The coverage
  condition is read over the identified
  family: an UNIDENTIFIED IN ICIT member
  carries no ICIT occurrences, so the
  condition's untested side is the identified
  members that are NOT SCANNED or SCANNED —
  BELOW SUPPORTED FLOOR; the unidentified
  members' unmeasurability is reported in
  the headline block, as OPEN-072-2 rules.
- **The grade-flip rule** (§5.4 / F072-C12):
  flips are findings; the headline is the
  primary verdict, GRADE-SENSITIVE on a
  family-level difference (OPEN-072-6).
- **The step-0 gates in their order**
  (§3 / F072-C11), with gates 0.1–0.5
  exhibited at this freeze as §§3–6 record,
  and re-asserted at execution step 0 before
  any member is scored.
- **The outcome set and wordings** (§6):
  FAMILY SUPPORTED / FAMILY NOT SUPPORTED /
  INCONCLUSIVE, and the step-0 closures
  TOO THIN, SHAKTI INTAKE NOT REPRODUCED,
  ASSET F DIGEST MISMATCH, ASSET F NOT
  AVAILABLE, CONCORDANCE FAILED, INVALID —
  in the pre-written wordings.
- **The Roif gate** (§7 limit 1 /
  F072-C14): confirmed as drafted
  (OPEN-072-10); every record under this
  spec is internal until both of its
  conditions are met for a specific act.

## 9. What the freeze does not do

- **It does not score any member.** No
  ending-follower fraction for any fish
  member exists at the freeze, in either
  population; the reference distribution was
  produced from non-members only, and the
  census is occurrence counts only.
- **It does not settle the depiction
  divergence.** The registry's depiction
  notes and Asset F's depiction notes
  disagree for three Parpola numbers (§4);
  the freeze records the disagreement and
  proceeds on the numbering concordance the
  spec commissions. Whether Asset F's
  Parpola locators name the signs its
  depiction notes describe is a question
  about Spec 044's asset, not one this
  freeze may repair: the asset is consumed
  by digest, exactly as frozen.
- **It re-opens nothing.** Spec 048's
  closure, Spec 044's asset, and the
  Phase-43 record stand exactly as recorded.
- **It establishes nothing about what any
  fish sign meant or was pronounced**
  (§7 limits 2–3): a family verdict under
  this contract states positional behaviour
  on this corpus only.
- **Execution has not begun at the freeze
  itself.** Execution (Phase-431) awaits the
  freeze merge; the execution order for it
  was given in the same owner tasking that
  commissioned this freeze.

## 10. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec072_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.8-draft` →
`0.8-MUTATED`) and the suite was run — the
freeze-replay test and the register-integrity
test went red, as they must, because a covered
source no longer matched its frozen hash and
the register no longer carried its frozen
version. The file was then restored
byte-identically (its SHA-256 re-verified
against the value recorded in `freeze.json`'s
sources) and the full freeze suite was run
again green. The mutation touched no committed
byte; the frozen record replays exactly over
the restored tree.

## 11. OSF registration and the execution gate

Under OPEN-072-7 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-431, the falsifier, the
derived verdict line L = 0.765 with its
reference record's pin, the concordance of §4
with its two UNIDENTIFIED IN ICIT members and
their disposition, the step-0 gates in their
order, the populations and the carried
measure, the majority partition, the
grade-flip rule, and the Roif gate. The filing
record is `osf-spec-registration.md`,
completed by append after filing. The
registration stands **pending approval** after
filing; its approval act is the owner's
approval click on OSF's admin-notification
email, and no mail is handled by this freeze.
Execution (Phase-431) was commissioned in the
same owner tasking as this freeze, to run
after the freeze has merged and the filing
exists, with the approval act remaining the
owner's own: the filing is reported to the
owner with its approve link, and neither this
freeze nor the execution performs that click.

---

*AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution §VI.*
