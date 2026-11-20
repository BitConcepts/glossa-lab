# Meroitic Decipherment Campaign — Stage 4.3 Outcome Record: Candidate Generation and Identifiability (Spec 097)

**Date: 2026-11-20. Claim C097-10. Executed on tower-compute
under freeze v2, after the Stage 4.2 outcome landed in the
same sequence. Generation basis: the development partition
only (335 distinct inscription texts). The held-out
partition was not touched. Because Stage 4.2 licensed no
affiliation family, generation used internal routes only
(formula slot, theonym context, numeral context), exactly
as the campaign design §4 provides. Full register in the
companion `stage-4-3-candidates.json`; pipeline
`pipeline-v2.py` in the campaign scratch on tower-compute.**

## The register

Candidate pool: development-text forms with at least 10
occurrences, not in the frozen vocabulary, at least 3
letters, whose distributional profile met one of the
internal generation routes. **6 candidates** were
generated. Every candidate's profile is in the companion;
the headlines:

| Form | Dev occ. | Route | Candidate reading |
|---|---|---|---|
| soreyi | 137 | theonym context | cult or offering term (theonym-adjacent) |
| asoreyi | 23 | theonym context | cult or offering term (theonym-adjacent) |
| xolkete | 23 | formula slot | closing evaluative term of the funerary formula |
| pxolkete | 20 | theonym context | cult or offering term (theonym-adjacent) |
| xolkte | 16 | formula slot | closing evaluative term of the funerary formula |
| wisi | 10 | formula slot | invocation element of the funerary formula |

All 6 occur only in funerary texts on the development set
(funerary share 1.0), which is the genre skew the design
warned of, not a discovery about the forms.

## Identifiability protocol — applied before any scoring

Registered protocol for this stage (stated here, applied
uniformly): a candidate is identifiable only if (1) a
discriminating dimension exists on which its predicted
profile differs from its named rivals — the proper-name
rival (which predicts name-slot, i.e. filiation-context,
behaviour) and the grammatical-formative rival (which
predicts cross-stratum uniformity); (2) the discriminating
observations occur at the registered minimum count of 10
development occurrences; and (3) no equally simple rival
survives — operationally, the proper-name rival survives,
and the candidate fails, if the form's filiation-adjacency
rate is at least 0.10.

**Result: all 6 candidates passed the screen** (filiation
adjacency 0.0 for every candidate) and were carried to the
blind test as IDENTIFIABLE (provisional, for blind test),
each with a frozen prediction: presence in at least 3
held-out texts, and a held-out funerary share within ±0.25
of its development share.

## The record's own caution, stated before the blind test

Three of the six forms (soreyi, asoreyi, wisi) are, on
their face, spelling variants of the anchored theonyms
sorey "Osiris" and wos "Isis" — the varietas phenomenon
freeze v2 §7 refused to normalize away. They entered the
pool precisely because the freeze keeps variants as
distinct forms and they are absent from the frozen
vocabulary as spelled. Their candidate readings as
generated ("theonym-adjacent cult or offering term") are
weaker than what the anchor tradition already says about
their base forms, and the Stage 4.4 record will score them
as generated, not as the tradition would phrase them. The
remaining three (the xolkte family) are the register's
genuinely unanchored candidates. No candidate was scored
SUPPORTED at this stage, and none could be: SUPPORTED
requires the blind test, which is Stage 4.4.
