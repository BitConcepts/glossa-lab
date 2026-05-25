# Falsification Protocol
## Indus Anchor Model — Formal Checklist

Each check specifies: the claim being tested, the required data, the PASS criterion, and the FAIL criterion that weakens or refutes the model.

Status codes: ✓ PASS (Holdat) | ✗ FAIL | — NOT YET TESTED

---

## Tier 1: Structural Falsification Tests

These do not depend on phonetic readings being correct.

### F1 — Positional non-randomness
**Claim:** Sign positions are non-random and cannot be explained by a within-seal shuffle null.
**Test:** Permutation test — compute grammar-position statistic on 2,000 within-seal shuffles.
**PASS:** Observed statistic > all 2,000 shuffled statistics (p = 0/2000).
**FAIL:** >5% of shuffles exceed or match the observed statistic.
**Status:** ✓ PASS (Holdat) — z = 10.3, 0/2000 permutations exceeded observed

### F2 — Fish-sign compound-only (Holdat)
**Claim:** Fish-family signs never appear in isolation in formal stamp-seal contexts.
**Test:** Count isolated vs. compound occurrences across all 9 sites.
**PASS:** 0 isolated occurrences.
**FAIL:** ≥1 isolated occurrence in any formal seal context.
**Status:** ✓ PASS (Holdat) — 0/113 isolated

### F3 — Fish-sign compound-only (Gulf catalog)
**Claim:** Fish-sign compound-only pattern holds in Gulf deposit seals.
**Test:** Search Laursen (2010) Gulf Type seal catalog for isolated fish signs.
**PASS:** 0 isolated occurrences.
**FAIL:** ≥1 isolated occurrence.
**Status:** ✓ PASS — 0/27 Gulf contexts; combined 0/140

### F4 — Three-slot grammar accuracy
**Claim:** The INITIAL/MEDIAL/TERMINAL grammar model correctly classifies ≥70% of H+M signs.
**Test:** For each H+M sign with ≥3 tokens, compute I/M/T rates; classify by 3-slot rules; compare to KNOWN_SLOT assignments.
**PASS:** ≥70% sign-level accuracy.
**FAIL:** <70% accuracy would indicate the grammar model is not predictive.
**Status:** ✓ PASS (Holdat) — 93.2% (137/147 signs)

### F5 — M267 motif-independence
**Claim:** M267 (proposed genitive particle) is not iconographically specific — it appears with all motif types.
**Test:** Chi-square test for independence between M267 occurrence and seal iconography.
**PASS:** Not significantly enriched with any motif type (p > 0.05 after Bonferroni).
**FAIL:** Significant enrichment with a specific motif type would suggest iconographic rather than grammatical function.
**Status:** ✓ PASS (Holdat) — chi-square test confirms motif-independence

### F6 — ICIT positional grammar (not yet tested)
**Claim:** Three-slot grammar holds on ICIT corpus after crosswalk.
**Test:** Rerun Test F4 on ICIT-crosswalked data.
**PASS:** ≥70% grammar accuracy on ICIT.
**FAIL:** <70% accuracy.
**Status:** — NOT YET TESTED

### F7 — ICIT fish-sign test (not yet tested)
**Claim:** Fish-sign compound-only pattern holds in ICIT.
**Test:** Rerun Test F2 on ICIT corpus.
**PASS:** 0 isolated fish signs.
**FAIL:** >5% isolated rate.
**Status:** — NOT YET TESTED

---

## Tier 2: Candidate Anchor Falsification Tests

These test whether the proposed readings are consistent with independent evidence.

### A1 — Parpola (1994) convergence
**Claim:** ≥40% of HIGH-confidence readings appear independently in Parpola (1994).
**Test:** Text-mine Parpola (1994) for each HIGH-confidence reading string.
**PASS:** ≥40% of HIGH readings appear in Parpola's text.
**FAIL:** <40% convergence.
**Status:** ✓ PASS — 44/75 (59%) HIGH readings found in Parpola (1994)

### A2 — Mahadevan grammar consistency
**Claim:** The 3-slot grammar model is consistent with Mahadevan's published analyses spanning 1972–2018.
**Test:** Extract positional-grammar references from 10 Mahadevan papers; check consistency.
**PASS:** All 10 papers describe positional grammar consistent with 3-slot model.
**FAIL:** Any Mahadevan paper describes grammar that contradicts the 3-slot model.
**Status:** ✓ PASS — 10/10 papers consistent

### A3 — Dravidian phoneme exclusivity (no Sanskrit-exclusive phonemes)
**Claim:** No H+M reading requires a phoneme that is physically impossible in Sanskrit.
**Test:** Check each reading against Sanskrit and Dravidian phoneme inventories.
**PASS:** 0 readings require Sanskrit-exclusive phonemes; ≥20% require Dravidian-exclusive phonemes.
**FAIL:** Any reading requires a Sanskrit-exclusive phoneme.
**Status:** ✓ PASS — 0/157 Sanskrit-exclusive; 35/157 Dravidian-exclusive

### A4 — H+M token coverage (Holdat)
**Claim:** 161 H+M anchors cover ≥85% of corpus tokens.
**Test:** Sum tokens for all H+M signs; divide by total corpus tokens.
**PASS:** Coverage ≥85%.
**FAIL:** Coverage <70%.
**Status:** ✓ PASS (Holdat) — 90.96% (6,363/7,002 tokens)

### A5 — H+M token coverage (ICIT, not yet tested)
**Claim:** Coverage ≥70% when crosswalked to ICIT.
**Status:** — NOT YET TESTED

---

## Tier 3: External Anchor Tests

### E1 — Shu-ilishu phonological test
**Claim:** The Shu-ilishu seal (Ur III, c.2020 BCE) provides at least 2/4 phonological slots covered by H+M readings.
**Test:** Test /su/, /i/, /li/, /shu/ against H+M reading inventory.
**PASS:** ≥2/4 slots covered.
**FAIL:** 0/4 slots covered (even /i/ absent).
**Status:** ✓ PASS (partial) — 2/4 slots covered (/i/ and /li/); /su/ and /shu/ absent

### E2 — Tamil-Brahmi terminal cross-validation
**Claim:** Terminal-dominant H+M signs match known Tamil-Brahmi terminal phoneme categories.
**Test:** Compare H+M TERMINAL-class signs against TB terminal phoneme inventory (11 categories).
**PASS:** ≥50% TB coverage from confirmed suffix signs.
**FAIL:** <30% TB coverage.
**Status:** ✓ PASS — 8/11 TB categories covered (73%)

### E3 — Bilingual inscription
**Claim:** Any bilingual Indus–Akkadian/Sumerian inscription discovered at a Gulf trade site would allow direct validation.
**Test:** Not currently possible.
**Status:** — NOT APPLICABLE (no bilingual inscription known)

---

## Summary Status

| Category | Tests | PASS | FAIL | NOT TESTED |
|---|---|---|---|---|
| Structural (Tier 1) | 7 | 5 | 0 | 2 (ICIT pending) |
| Candidate anchors (Tier 2) | 5 | 4 | 0 | 1 (ICIT pending) |
| External anchors (Tier 3) | 3 | 2 | 0 | 1 (bilingual) |
| **Total** | **15** | **11** | **0** | **4** |

The 4 untested items all require ICIT crosswalk (F6, F7, A5) or are contingent on a future archaeological discovery (E3).
