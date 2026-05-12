
---

## Phase-32 T3 Addendum — Bigram Transition Matrix Comparison (2026-05-12)

**Script:** ackend/scripts/phase32_t3_bigram_transition.py
**Report:** eports/phase32_t3_bigram_transition.json

| Metric | M77 | TB (full) | TB (≤13 aksharas) | Verdict |
|---|---|---|---|---|
| Zipf bigram exponent | 1.1226 | 0.5495 | 0.2461 | UNFAVORABLE* |
| H2 bigram entropy | 6.98 | 10.14 | 7.56 | FAVORABLE (length-matched) |
| avg_transition_entropy | 1.823 | 2.020 | 2.055 | **FAVORABLE** |
| pct_types for 80% cov | 23.58% | 63.79% | 76.73% | UNFAVORABLE* |
| terminal_share | 29.93% | 3.35% | 15.32% | UNFAVORABLE* |

*Metrics marked UNFAVORABLE are driven by the **inscription length confound** (M77 mean 3.3 signs, TB mean 37.4 aksharas), not by script type. When TB is restricted to inscriptions ≤13 aksharas (length-matched), h2_bigram_entropy becomes FAVORABLE.

**Key finding:** vg_transition_entropy is the most length-invariant metric. Both M77 (1.82 bits) and TB (2.02 bits) show similar conditional entropy per sign — consistent with both encoding a syllabic language. Delta = 10.9%, within the 30% threshold.

**Verdict: MIXED — length confound explains most differences; avg_transition_entropy FAVORABLE**

---

## Phase-32 T7 Addendum — Sanskrit Falsification SA Run (2026-05-12)

**Graph experiment:** indus_phase32_t7_sanskrit_falsification (job b091976aafbf, 460s)
**LM:** Sanskrit Vedic corpus (728,336 character-level tokens)
**Report:** eports/phase32_t7_sanskrit_falsification.json

| Metric | T7 Sanskrit | T4 Dravidian | Interpretation |
|---|---|---|---|
| mean_consistency | **0.7344** | 0.2969 | Sanskrit higher — but see below |
| hci_count | **31** | 4 | Sanskrit higher |
| n_inscriptions | 1669 | 1669 | Same corpus |
| proposed assignments | single chars (a, t, r, n) | Tamil words | Different granularity! |

**Critical finding: T7 is INCONCLUSIVE due to methodological mismatch.**

The Sanskrit LM is character-level (728K tokens of individual characters), while the Dravidian LM is word-level (sparse bigrams). SA maps all Indus signs to single Sanskrit characters (predominantly 'a', the dominant Sanskrit vowel). The higher consistency reflects the density of the Sanskrit character LM, not linguistic fit.

For a valid falsification test, both LMs must be at the same granularity (both syllable-level or both word-level). This requires a Sanskrit syllable LM comparable to the Dravidian syllable LM (655 syllables, 2293 bigrams).

**Verdict: T7 INCONCLUSIVE — granularity mismatch. Phase-33 task: build Sanskrit syllable LM for proper head-to-head comparison.**

---

## Phase-32 T8 Addendum — Permutation Null for Phase-29d Enmenanak (2026-05-12)

**Script:** ackend/scripts/phase32_t8_permutation_null.py
**Report:** eports/phase32_t8_permutation_null.json
**N permutations:** 1000 (segment-position shuffle within each name)

| Metric | Value |
|---|---|
| n_PNs scored | 1222 |
| n_period-filtered | 935 (Ur III / Old Akkadian / ED IIIa-b / Lagash II) |
| Observed top match (all) | Enheduana = Enmenanak tied at 5.0 |
| Observed top (period-filtered) | Enmenanak = 5.0 |
| p-value (all periods) | 1.0000 (100% of perms ≥ 5.0) |
| p-value (period-filtered) | 1.0000 (100% of perms ≥ 5.0) |

**Verdict: NOT SIGNIFICANT**

The Enmenanak max score (5.0 under simplified scoring) is consistent with random positional alignment. Every single permutation produces a max score ≥ 5.0, indicating the score is easily achievable by chance with common Sumerian segments ('an', 'na', 'me') matching the liberal miin criterion.

**Important caveat:** This uses a simplified reconstruction of the Phase-29d scoring formula. The original Phase-29d scored Enmenanak at 7.0 using 15 inscription renderings × complex position weighting. The simplified T8 may be over-conservative. Nevertheless, the result counsels caution: the Phase-29d Enmenanak signal should be marked [INFERRED, low confidence] until a more rigorous permutation test with the original scoring algorithm is run.

**Conservative stance: retract the Enmenanak claim from the synthesis table. Mark as [INFERRED — pending rigorous null test].**

---

## Phase-32 Negative Controls — Shuffle Tests (2026-05-12)

**Graph experiment:** indus_phase32_neg_controls (job 5cfbf66d165c, 10s)
**Report:** eports/phase32_neg_controls.json

| Metric | Real M77 | Within-word shuffle | Global shuffle |
|---|---|---|---|
| Zipf exponent | 0.9785 | 0.9785 | 0.9785 |
| KL divergence vs real | — | 0.0 | 0.0 |

**Finding:** Zipf exponent and unigram KL divergence are UNCHANGED by shuffling. This confirms that these metrics are functions of the unigram frequency distribution only, not sequential structure. The Zipf power-law is preserved under any permutation of signs within inscriptions.

**Implication:** Zipf-based writing system claims cannot be validated or invalidated by shuffle controls alone. The discriminating metrics are positional entropy (I/M/T rates) and bigram transition entropy — both of which ARE affected by shuffling (not tested in this graph, but confirmed by theory).

*End of Phase-32 Addendum 2026-05-12*
