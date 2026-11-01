# Spec 076 — Pilot record (Phase 442)

**Executed 2026-10-26**, once, exactly as frozen
(spec §8, FF-5), after the freeze merged (PR #412,
merge commit e0d173ac; CI 8/8 including the
required C4 check). Freeze digest:
`83259ed3d3a20189e5c22e4645d26452c9c3b79a60348b3f5c38b8405addde9a`.

## Verdict

**PILOT FAILS — ASSUMPTION SET DOES NOT HOLD**
(the design's §8 step-3 closure word). Step 0 and
step 1 passed exactly; both step-2 bars passed by
wide margins; step 3, the positive control,
excluded **36** of the strict core's blind-coded
claimed types against a frozen bar of **at most
5**. Under the frozen text, claim **F076-C02 is
not filed**, and **no register is produced**. The
route's status is the design's own: the closure
word is appended to the design draft with this
record, exploratory-labelled, in the advance
plan's iteration loop (cap: three iterations,
then the move re-ranks on evidence or closes
PARKED).

The design's presumption, stated in advance and
recorded here as the standing reading: the failure
indicts the machinery — the §3.4 vocabulary, the
coding rules CR-1…CR-7, or A-FACE — not the strict
core. §5 below records the texture that supports
that presumption; it adjudicates nothing beyond
the closure word.

## 1. Step 0 — reproduction gate: PASS

Re-derived from the pins exactly as frozen:
2,906 indusscript-m77 records; 680 placeholder +
452 marked tokens dropped; **11,507 tokens**;
**5,883 strict tokens**; 2,880 non-empty
sequences. Every figure equals the expected
value. The gate that closed the M2 pilot at its
first door does not close this one.

## 2. Step 1 — derivation: PASS

Slot totals init 2,655 / fin 2,655 / solo 225 /
med 5,972 (sum 11,507; the §7.2 identities exact).
Finals partition: strict 1,707 / pending 250 /
anchored-other 520 / no-anchor **178**, summing to
2,655. Headline numbers reproduced: **677**
(sign, type) exclusions over the 122 no-anchor
signs; U2 finals residual **178**; solo-only set
**13**. The derivation is what §8 said it must be
before any test was run.

## 3. Step 2 — the shuffle null: BOTH BARS PASS, by wide margins

Marginals-preserving shuffle, B = 999, seed
20261026 (FF-1), implemented as frozen (pooled
token multiset re-dealt into the frozen sequence
lengths; label permutation used nowhere).

- **(i) U2 finals residual.** Real **178**. Null:
  min 371, 5th percentile **395.0**, median 421,
  max 474. Not one of the 999 shuffles produced a
  residual at or below the real value (empirical
  fraction 0.000). Bar (real below the null's 5th
  percentile): **PASS**.
- **(ii) Solo-only sign count.** Real **13**.
  Null: min 0, median 2, 95th percentile **5.0**,
  max 12. Not one shuffle reached the real count
  (empirical fraction ≥ 13: 0.000). Bar (real
  above the null's 95th percentile): **PASS**.

The frame's constraint structure, in the tested
family, is not a marginals artefact: the unread
signs are final-poor and the solo-only signs are
concentrated far beyond anything the frame's own
marginals produce by chance. This is the half of
the pilot that would have licensed F076-C02. It
does not rescue the pilot: the frozen verdict
requires step 3 as well, and the record states
both halves as they fell.

## 4. Step 3 — the positive control: FAIL (36 exclusions, bar ≤ 5)

The 94 strict signs were coded from their anchors
`reading` + `basis` texts only, under CR-1…CR-7,
by a coder blind to every census row (the coding
was produced before and independently of the
comparison; the coder's file is preserved with
this record). Coded distribution over all 94:
ONLY-INIT 28, ONLY-FIN 8, ONLY-MED 9, FREE 49;
among the 89 frame-attested: ONLY-INIT 28,
ONLY-FIN 8, ONLY-MED 7, FREE 46.

Run against the frame's possibility sets:

- Frame-attested strict signs: **89**. Frame-
  absent (CR-7 line, counted neither way): **5**
  — 039 (FREE), 044 (FREE), 046 (FREE), 362
  (ONLY-MED), 374 (ONLY-MED).
- **Exclusions: 36 of 89** — by coded type:
  ONLY-INIT 22 of 28 coded, ONLY-FIN 8 of 8
  (every terminal-function code in the frame was
  excluded), ONLY-MED 6 of 7. The excluded signs,
  with coded type and the contradicting row, are
  listed in full in `pilot/pilot-results.json`.

Bar: at most 5. **36 ≫ 5 → the pilot closes
ASSUMPTION SET DOES NOT HOLD.**

## 5. The texture of the failure (recorded, not adjudicated)

Three patterns in the 36, visible in the filed
numbers, which the iteration loop — not this
record — is charged with weighing:

- **22 of the exclusions are ONLY-INIT codes**
  whose bases are the anchors programme's own
  Round 1/2 distributional assignments ("INITIAL
  position (freq=…), distributional assignment;
  consistent INITIAL"). In this frame those signs
  also occur medially and finally — the basis
  language records where a sign's evidence
  concentrated in the compilation the anchors were
  built on, not an exclusivity claim in §3.4's
  sense. Coded at face value under CR-2/CR-6 (as
  frozen — the rules err toward being able to
  fail), they fall in rows.
- **The ONLY-FIN codes** include the flagship
  strict sign M342 ("Terminal marker, Dravidian
  case suffix"): its frame row holds 349 medial
  occurrences, so ONLY-FIN is excluded — while its
  possibility set is {FREE} precisely because it
  occurs everywhere. A case suffix that other
  material can follow is a terminal *function*
  claim, not an inscription-final *exclusivity*
  claim; §3.4's vocabulary has no type between
  ONLY-FIN and FREE in which to state it.
- **The ONLY-MED codes** rest on bases of the
  form "internal position (never inscription-
  initial/final)" asserted from a few hundred seal
  occurrences in another surface; in this frame
  several of those signs stand at inscription
  edges.

In the design's own terms (§8): the presumption
is that the machinery — vocabulary, coding rules,
or A-FACE's demand that a type-claim carry its
full distributional content — is wrong, not that
the strict core is. The 36 exclusions are
consistent with that presumption: they are
concentrated exactly where the basis language is
a *distributional summary* wearing a *type
claim's* clothes (the mirror image of §7.5's
warning). No part of this record re-codes,
re-runs, or softens the count: 36 is the frozen
run's number, and the closure word stands on it.

## 6. Filings and non-filings

- **F076-C02: NOT FILED** (its condition — a pilot
  pass — did not occur). It remains draft in the
  frozen register, permanently unadvanced by this
  pilot.
- **No register is produced.** The Tier-C
  derivation of step 1 exists as a computation
  (its headline numbers are §2 above); it is not
  filed as claims, per the frozen text.
- F076-C08's falsifier fired as stated; the claim
  stands falsified in its frozen form, recorded
  here (the frozen register itself is not edited —
  its digest is the freeze's).
- The pilot artifacts are preserved under
  `pilot/`: `pilot_run.py` (the single frozen
  run), `pilot-results.json` (the full output,
  including every excluded sign's row and
  possibility set), `strict-coding-input.json`
  (the coder's only input), `strict-coding-output.json`
  (the blind coding, with its per-sign notes).

## 7. What this pilot establishes / does not establish

**Establishes:** the derivation is sound and
reproducible (steps 0–1, the third and fourth
independent reproductions of the census); the
pilot frame's constraint structure exceeds its
marginals in the tested family by margins no
shuffle in 999 approached (step 2); and the
positive control can fail and did — the
machinery as frozen (nine-type vocabulary +
CR-1…CR-7 + A-FACE) excludes the strict core's
own claimed types 36 times in 89, so the
assumption set, as an instrument for judging
completions at face value, does not hold. That
last finding is a result, not an embarrassment:
it is the first measurement of how far the
anchors' basis language is from type-claims in
this vocabulary's sense, and it was bought by a
control designed to be able to deliver it.

**Does not establish:** that the strict core is
wrong (the design's presumption runs the other
way, and nothing here overturns it); that the
necessity programme is empty — step 2's result
stands, and a redesigned instrument (a vocabulary
that can state functional claims without
exclusivity, coding rules that distinguish a
distributional summary from a type-claim) is the
iteration loop's question, under its cap of
three; that any sign's possibility set in §2's
derivation is false — the census arithmetic is
untouched by the control's failure; what remains
false is the *bridge* (A-FACE + the coding rules)
from basis language to that arithmetic. Nothing
about any sign's meaning, and not decipherment:
the standing position is unchanged.

## 8. Route status

Spec 076's pilot is **closed: ASSUMPTION SET DOES
NOT HOLD**. The move returns to the advance plan's
iteration loop, exploratory-labelled (iteration
cap: three, then re-rank on evidence or PARKED).
No re-run of this pilot, under any parameters, is
authorised by this record; a successor design is
a new draft, judged as this one was.
