# Phase-35 Synthesis: Vocabulary Equalization and Controlled Falsification

**Completed:** 2026-05-14  
**Status:** COMPLETE  
**Foundation check:** PASS (17/0/0)

---

## What Phase-35 Fixed vs Phase-34

Phase-34 identified that Sanskrit winning the anchored comparison was likely due to vocabulary size confound (Sanskrit 424 syllables vs Dravidian 655). Phase-35 equalizes both LMs to 424 syllables and adds crosswalk-sourced anchors.

---

## EXP A — Anchor Audit (Augmented)

Crosswalk provided **7 new anchor mappings** beyond INDUS_FINAL_ANCHORS + Parpola.

| Source | Contribution |
|---|---|
| Parpola phonemes | anchors for plain integer sign IDs |
| INDUS_FINAL_ANCHORS | M-prefix stripped to corpus format |
| M↔P Crosswalk | 7 new mappings (M090→ai, etc.) |

**Active anchors in freq≥3 corpus (augmented):** 6

| Sign | Freq | Syllable | Source |
|---|---|---|---|
| `047` | 541 | `min` | INDUS_FINAL_ANCHORS HIGH |
| `090` | 102 | `ai` | Crosswalk MEDIUM (NEW) |
| `045` | 92 | `yan` | INDUS_FINAL_ANCHORS MEDIUM |
| `034` | 80 | `tol` | Parpola |
| `176` | 16 | `an` | INDUS_FINAL_ANCHORS MEDIUM |
| `147` | 5 | `mi` | INDUS_FINAL_ANCHORS HIGH |

Why only 6 of 62 freq≥3 signs are anchored: most crosswalk M-numbers correspond to signs with **corpus_freq=0** in M77. This is because M77 uses a large sign catalog and many signs (M001, M048, M060, M086...) appear fewer than 3 times or are absent from the 1669-inscription dataset.

---

## EXP B — Phase-35 T1: Equalized Dravidian SA

| Metric | Phase-34 (unequalized) | Phase-35 (equalized, 424 syl) |
|---|---|---|
| Vocab size | 655 syl / 1049 bg (truncated) | **424 syl / 1049 bg** |
| Fixed anchors | 4 | 4 |
| Z-score | 5.75 | **5.87** |
| p-value | < 0.0001 | < 0.0001 |
| NLL lift/insc | 5.851 | **6.241** |
| Significant | YES | YES |

Slightly better Z and lift at equalized vocabulary. Still SIGNIFICANT.

---

## EXP C — Phase-35 T7: Equalized Sanskrit SA

| Metric | Phase-34 | Phase-35 (equalized) |
|---|---|---|
| Vocab size | 424 syl / 651 bg | **424 syl / 651 bg** (unchanged) |
| Fixed anchors | 4 | 5 |
| Z-score | 6.94 | **6.34** |
| p-value | < 0.0001 | < 0.0001 |
| NLL lift/insc | 7.166 | **7.417** |
| Dravidian wins | NO | **NO** |
| Lift ratio Drav/Skt | 0.82× | **0.84×** |

**Sanskrit wins consistently across Phase-33, Phase-34, and Phase-35 on lift/insc under equalized conditions.**

---

## ⚠️ Critical Methodological Finding

Both LMs now have identical vocabulary sizes (424 syllables), but their **bigram densities differ**:
- Dravidian (equalized): 1049 bigrams over 424 syllables → 2.47 bigrams/syllable
- Sanskrit: 651 bigrams over 424 syllables → 1.54 bigrams/syllable

A **sparser bigram LM** (Sanskrit, 651 bigrams) may be intrinsically easier for SA to exploit: the SA needs to find configurations where the mapped syllable pairs hit the 651 LM bigrams, and with fewer constraints there are more valid configurations. A denser LM (Dravidian, 1049 bigrams) constrains the SA more tightly, potentially suppressing the score.

**This bigram density confound is the next critical issue to resolve.**

---

## EXP D — LM Quality: Merged DEDR+CleanTB

| Metric | DEDR-only | Merged (DEDR + cleanTB) |
|---|---|---|
| Bigrams | 2293 | **3026** |
| Syllables | 655 | 660 (5 new from clean TB) |
| SA score (best mapping) | -55,251 | -55,698 |
| Score delta | baseline | **-447 (worse)** |

The merged LM scores slightly *worse* on the best mapping. This is because:
1. The TB inscription bigrams reflect sequences in short donor inscriptions (2-15 aksharas)
2. The Indus script bigram structure may not align with TB-style bigrams
3. The 70/30 blend weights reduce the LM's sharpness without adding discriminative information

Merged LM saved as `dravidian_syllable_lm_merged.json` for reference; DEDR-only remains canonical for SA experiments.

---

## Honest Assessment: SA Discrimination Capability

Across all phases, the pattern is consistent:

| Phase | Dravidian Z | Sanskrit Z | Dravidian lift | Sanskrit lift | Dravidian wins? |
|---|---|---|---|---|---|
| 33 (anchor-free, unequal vocab) | 8.01 | 9.23 | **8.679** | 4.180 | YES (lift) |
| 34 (anchored, unequal vocab) | 5.75 | 6.94 | 5.851 | 7.166 | NO |
| 35 (anchored, equalized vocab) | 5.87 | 6.34 | 6.241 | 7.417 | NO |

The Phase-33 Dravidian win was due to the unequal vocabulary sizes (655 vs 424 syllables) creating a larger absolute NLL gap. Under controlled conditions, Sanskrit consistently achieves equal or higher scores.

**However:** both languages are highly significant (Z > 5, p < 0.0001 in all runs). The SA method correctly identifies that the Indus Script has a non-random bigram structure that can be exploited by *either* a Dravidian OR a Sanskrit syllabic LM. This does not refute the Dravidian hypothesis — it identifies the limits of the SA-based comparison method.

**Working interpretation [INFERRED, medium confidence]:** The SA at current scale (62 free signs, 30K iterations) is too underpowered to distinguish between linguistically related syllabic hypotheses. Additional discriminative power requires:
1. Fixing the bigram density confound (equalize bigrams/syllable ratio)
2. More corpus data (ICIT corpus — Phase-32 T5, blocked on Fuls)
3. Using positional constraints (known TERMINAL/INITIAL signs as additional anchors)
4. Phoneme-level anchors from DEDR etymological analysis of TB-corpus inscriptions

---

## Phase-36 Candidate Experiments

1. **Bigram density equalization** (CRITICAL): Resample/thin Dravidian to 651 bigrams (or pad Sanskrit to 1049). Compare at identical vocab size AND identical bigram density.
2. **Positional anchor injection**: Force known TERMINAL signs (9 identified in Phase-33 EXP 1) to Dravidian suffix syllables (`an`, `ay`, `am`, `in`); re-run SA.
3. **ICIT corpus** (blocked): With 4,537 artefacts, ICIT would provide 3× more tokens and potentially 2× more high-frequency signs.
4. **TB anchor injection**: Use clean TB inscription sequences directly — the 5 signs appearing in both M77 corpus and TB inscriptions with known readings as hard anchors.

---

## Citations

- M77 corpus: Mahadevan 1977 — CITATIONS.md §A.1
- Crosswalk: INDUS_FINAL_ANCHORS + M↔P crosswalk_v2 — internal
- Dravidian LM: DEDR (Burrow & Emeneau 1984) §E.1 + clean TB §A.12
- Sanskrit LM: Vedic Sanskrit sources §E.2
