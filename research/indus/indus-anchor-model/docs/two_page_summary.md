# ICIT Validation Request: Falsifiable Indus Script Anchor Model
## Technical Summary — Tristen Kyle Pierson, Glossa-Lab / BitConcepts LLC

---

## One-Sentence Summary

A Mahadevan-coded computational anchor model proposes 161 HIGH/MEDIUM candidate sign anchors and a three-slot positional grammar validated on Holdat LLC corpus; the critical next test is whether the model generalises to ICIT.

---

## What the Model Claims

**Tier 1 — Structural claims (high confidence, testable independently):**

- Non-random positional structure: z = 10.3, 0/2,000 permutations exceeded the observed statistic in a within-seal shuffling null test
- Three-slot inscription grammar: [ANIMAL CLASSIFIER]–[GUILD TITLE]–[PERSONAL NAME/SUFFIX] accounts for 97 distinct formula types across all semantic domains
- Fish signs are 0% isolated: 0/113 fish-family sign occurrences across all 9 corpus sites are isolated; all appear in compound multi-sign sequences. This holds at Lothal (the primary coastal port) identically to inland sites
- M267 correction: the sign previously misclassified as the fish/star sign (M267, frequency 400) is a high-frequency grammatical particle (81% MEDIAL, motif-independent by chi-square), not an iconographic fish sign. The actual fish sign is M047 (frequency 13, 100% compound)
- Betweenness centrality stratification: 20/161 H+M signs have BC > 0 (grammar candidates); 141/161 have BC = 0 (consistent with personal-name syllables). M342 is the rank-1 structural hub (BC = 0.055); M267 is rank-3 MEDIAL bridge (BC = 0.051)

**Tier 2 — Candidate anchor claims (require expert review and cross-corpus validation):**

- 161 HIGH/MEDIUM candidate anchor readings covering 90.96% of corpus tokens
- Proto-Dravidian compatibility: 44/75 HIGH-confidence readings appear in Parpola (1994); 35/157 contain Dravidian-exclusive phonemes (0/157 contain Sanskrit-exclusive phonemes)
- Grammar model explains 93.2% of sign-level positional behaviour at 161 H+M

**What the model does not claim:**
- Final decipherment
- Proof of Proto-Dravidian
- Validated personal names
- Complete phonetic transcription of any individual seal

---

## Why ICIT Is Needed

The Holdat LLC corpus is not publicly redistributable. ICIT (~5,318 inscriptions, publicly available) provides:

1. An independent test bed with a different coding system — if structural patterns hold across both corpora, that is meaningful cross-corpus validation
2. Approximately 3× the token count, enabling better statistical power for low-frequency sign analysis
3. A publicly citable corpus against which the model's claims can be independently reproduced by other researchers

**The preprint explicitly identifies ICIT as the immediate validation priority** (§3.24, §3.16, §5).

---

## Proposed Tests

Eight tests are specified in full in `docs/icit_validation_plan.md`. In brief:

| Test | What It Measures | Falsification Threshold |
|---|---|---|
| T1 | Token coverage under 161 H+M anchors | <70% coverage |
| T2 | Positional grammar accuracy | <70% classification accuracy |
| T3 | Fish-sign isolation rate | >5% isolated occurrences |
| T4 | M267-equivalent sign — functional vs. iconographic | Iconographic enrichment significant |
| T5 | Formula bigram backbone | Terminal sign not in top-5 PMI |
| T6 | BC stratification (grammar vs. name-syllable) | Stratification does not reproduce |
| T7 | Rakhigarhi site divergence | CI overlaps with other sites |
| T8 | Crosswalk failure analysis | >30% of HIGH signs without ICIT match |

---

## Technical Ask

One narrow question: **Is a Mahadevan-to-ICIT sign crosswalk already available, and is there a preferred format for rerunning corpus-level positional and bigram tests?**

A partial crosswalk covering the top-50 signs by frequency would be sufficient for Tests 1–3. The full 161-anchor crosswalk would be required for the complete validation suite.

---

## Materials Available for Sharing

All public materials are at: https://github.com/BitConcepts/glossa-lab

Specifically relevant:
- `data/public/anchor_table_397.csv` — all 397 Mahadevan M-numbers with candidate readings
- `data/public/formula_bigrams.csv` — top-30 H+M bigrams with counts and PMI
- `docs/icit_validation_plan.md` — full 8-test plan with success criteria
- Preprint PDF (attached)

Scripts for all analyses are in `scripts/` and accept ICIT-format input after crosswalk mapping.

---

## Confidence Calibration

The strongest claims are structural (Tier 1) and do not depend on any proposed phonetic readings being correct. The fish-sign result, the positional structure, and the formula skeleton would all be meaningful findings even if every proposed Proto-Dravidian reading were wrong.

The candidate anchor readings (Tier 2) are hypotheses, not conclusions. The model's contribution is making those hypotheses explicit, citable, and testable.
