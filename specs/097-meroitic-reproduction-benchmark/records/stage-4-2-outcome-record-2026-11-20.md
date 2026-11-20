# Meroitic Decipherment Campaign — Stage 4.2 Outcome Record: Affiliation (Spec 097)

**Date: 2026-11-20. Claim C097-9. Executed on tower-compute
under freeze v2
(`records/campaign-freeze-v2-2026-11-20.md`), which
registered every number below before computation: the
182-form vocabulary (companion
`records/freeze-v2-vocabulary-2026-11-20.json`), the 12
ASJP concepts, the consonant-skeleton correspondence rule,
10,000 permutations (seed 20261120), the pass bars
(p < 0.01 AND S ≥ 5 per vocabulary test; the phonotactic
and formative bars of freeze §4), and the power statement.
Pipeline: the program's own `pipeline-v2.py`, held in the
campaign scratch on tower-compute
(`~/glossa-work/meroitic-scratch/campaign/`); full outputs
in the companion `stage-4-2-results.json`. Computation
basis: the freeze v2 development partition (335 distinct
texts) and the 932 distinct example phrases only; the
held-out partition was not touched. No Otten-derived text
is published; the vocabulary tests ran on the CC BY / CC
BY-SA vocabulary and the CC BY 4.0 ASJP lists.**

## Verdict

**UNDECIDABLE AT THIS POWER. R3 (isolate / null) is
recorded as not displaced, and as nothing more.**

Neither rival passed its registered tests, and freeze v2's
power statement (power 0.81 only if the true per-concept
correspondence rate is 0.50; 0.42 at 0.35) forbids reading a
double failure at n = 12 concepts as a positive
classification. This is the adjudication outcome freeze v2
§5 added for exactly this case.

## The tests, as they ran

**R1 vocabulary test — attested forms only.** Comparator:
ASJP lists for Old Nubian, Nobiin, Dongolawi, Kenzi,
Midob and Nara (attested forms; reconstructions excluded
by construction, per freeze v2). **S = 4 of 12 concepts**
(matching concepts: 21 dog, 46 foot, 72 sun, 75 water),
**permutation p = 0.0326**. The bar was p < 0.01 AND
S ≥ 5: **not passed**. The signal is in the direction R1
predicts and below the registered bar; the record states
both halves of that sentence.

**R1 formative leg (supporting).** **5 formatives** in the
gold morphology carry a published NES comparandum in their
source apparatus and at least 20 development-token
attestations (the determiner -l at 438 among them), against
a bar of 3: **the leg passes**. Under freeze v2 the leg is
supporting only and cannot carry R1 alone; it is recorded
as passing, and it does not change the verdict.

**R2 vocabulary test.** Comparator: ASJP Coptic, Late
Egyptian, Middle Egyptian, Akkadian, Biblical Hebrew,
Amharic, Hausa. **S = 1 of 12** (46 foot), **p = 0.824**:
**not passed**, and not close.

**R2 phonotactic leg (Rowan's restriction).** Same-place
consonant-pair rate among word-internal CVC pairs:
Meroitic **0.3152** over 13,406 pairs (12,863 words);
within-word consonant-shuffle null **p = 0.474** (no
restriction detectable); the same statistic on the NES
reference lists is **0.3038**, so the Meroitic rate is also
not below the NES reference. Both registered conditions
fail: **not passed**. On this corpus basis, Rowan's
restriction does not hold at measurable strength.

## What this establishes, and what it does not

It establishes that, under a freeze registered before
computation, neither affiliation rival earns a SUPPORTED
verdict on the evidence this program can lawfully compute
on today, and that the honest adjudication at this power
is UNDECIDABLE. It does not establish that Meroitic is an
isolate (R3 is not displaced, not supported), that Rilly's
case fails on its own evidence (his case rests on some 170
reconstructed proto-forms and morphology, of which this
stage tested an attested-only 12-concept slice and a
formative leg that passed), or that Rowan's phonotactics
fail on the full published corpus (this stage's basis is
the 368-distinct-text acquired corpus and the example
phrases, with the transcription-quality caveat of the
Stage 4.1 completion record). Comparative candidate
generation is therefore **not licensed** for Stage 4.3,
which proceeds on internal evidence alone, as the campaign
design §4 provides for the case where no rival passes.
