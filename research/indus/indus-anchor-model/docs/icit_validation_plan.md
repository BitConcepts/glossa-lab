# ICIT Validation Plan
## Testing the Indus Anchor Model Against a Public Corpus

---

## Purpose

The current model was developed on the Holdat LLC Indus Corpus v3 (1,670 seals, 7,002 tokens, Miller 2025), which is not publicly redistributable. The Indus Corpus of Inscribed Texts (ICIT; Fuls 2014, ~5,318 inscriptions) is the largest available public Indus corpus and uses its own sign coding system.

This plan specifies the technical steps and success criteria for running the Mahadevan-coded 161-anchor model against ICIT data, so that all structural and candidate-anchor claims can be independently tested.

---

## What This Plan Does NOT Claim

This validation plan does not assert:
- Final decipherment of the Indus script
- Proof that the proposed readings are correct
- Recovery of personal names
- Complete phonetic transcription
- That the model outperforms all alternatives

The plan tests whether the structural patterns found in Holdat also appear in ICIT, and whether the candidate anchor assignments remain consistent under a different corpus.

---

## Required Crosswalk

Before any tests can run, a sign-code crosswalk is needed:

```
Mahadevan M-number → ICIT sign ID
```

The crosswalk must cover at minimum the 161 H+M anchor signs. A partial crosswalk covering the top-50 by token frequency is sufficient for Tests 1–3.

**Existing resources:**
- `data/public/anchor_table_397.csv` — all 397 Mahadevan M-numbers with candidate readings
- Mahadevan–Parpola crosswalk (45 entries): `data/public/mahadevan_parpola_crosswalk.csv`
- Wells (2011) sign list can serve as a bridge for some entries

**Open question:** Is there an existing Mahadevan-to-ICIT crosswalk already compiled? If so, it should be used in preference to constructing a new one.

---

## Tests to Rerun on ICIT

### Test 1 — Token Coverage Under 161 H+M Anchors
**Question:** What fraction of ICIT tokens are covered by the 161 H+M anchor signs, after crosswalk?
**Metric:** H+M token coverage (%)
**Current Holdat value:** 90.96%
**Falsification threshold:** Coverage <70% would indicate the anchor set does not transfer

### Test 2 — Positional Grammar Accuracy
**Question:** Do the 161 H+M signs maintain their predicted positional classes (INITIAL/MEDIAL/TERMINAL) in ICIT sequences?
**Metric:** Fraction of H+M signs correctly classified by the 3-slot model (TERMINAL if T≥0.60, INITIAL if I≥0.50, MEDIAL if M≥0.65)
**Current Holdat value:** 93.2% sign-level accuracy
**Falsification threshold:** <70% accuracy would undermine the grammar model

### Test 3 — Fish-Sign Isolated vs Compound
**Question:** Do M047-equivalent fish signs appear in isolation in ICIT formal inscription contexts?
**Metric:** Isolation rate (isolated / total occurrences)
**Current Holdat value:** 0% (0/113 occurrences isolated)
**Falsification threshold:** >5% isolation rate would contradict the compound-only claim

### Test 4 — M267-Equivalent Functional Sign Distribution
**Question:** Does the sign crosswalked to M267 (genitive particle) behave functionally (distributed across all motif types, predominantly MEDIAL) rather than iconographically?
**Metric:** Chi-square test for independence from seal iconography; positional MEDIAL rate
**Current Holdat value:** M267 is motif-independent (p≈0 for independence), 81% MEDIAL
**Falsification threshold:** Significant enrichment with a specific icon type, or <50% MEDIAL

### Test 5 — Bigram Backbone and Terminal-Sign Convergence
**Question:** Does the M342-equivalent terminal sign remain the highest-PMI terminal in ICIT bigrams? Does the formula backbone (terminal·masculine-suffix) reproduce?
**Metric:** Top-5 PMI bigrams, terminal sign betweenness centrality
**Current Holdat value:** M342·M176 is top PMI pair (2.43); M342 has rank-1 BC (0.055)
**Falsification threshold:** Formula backbone unrecognizable; terminal signs no longer dominant

### Test 6 — Betweenness Centrality Stratification
**Question:** Does the H+M network split into grammar signs (BC>0) and name-syllable signs (BC=0) in ICIT?
**Metric:** Fraction of H+M crosswalked signs with BC>0 vs BC=0
**Current Holdat value:** 20/161 BC>0 (grammar), 141/161 BC=0 (name-syllable)
**Falsification threshold:** BC=0 signs do not cluster around the anchor set's name-syllable candidates

### Test 7 — Site-Level Repertoire Divergence
**Question:** Is Rakhigarhi's distinct sign repertoire robust in ICIT data?
**Metric:** Bootstrap CI for KL divergence between Rakhigarhi and other major sites
**Current Holdat value:** Rakhigarhi KL=0.509 from Mohenjo-daro (95% CI [0.483, 0.750])
**Falsification threshold:** Rakhigarhi CI overlaps with other sites substantially

### Test 8 — Failure-Case Analysis
**Question:** Which H+M anchors fail to crosswalk cleanly, and do those failures cluster in a specific confidence tier or positional class?
**Metric:** Proportion of H+M signs with no ICIT equivalent; breakdown by confidence tier
**Diagnostic output:** If >30% of HIGH-confidence signs have no ICIT crosswalk, the crosswalk methodology needs review

---

## Falsification Criteria

The model is weakened or refuted if ANY of the following hold:

1. H+M token coverage in ICIT falls below 70% after crosswalk
2. Positional grammar accuracy falls below 70% in ICIT
3. Fish signs appear in isolation at >5% rate in ICIT formal seals
4. M267-equivalent sign is significantly enriched with a specific iconographic context
5. The formula bigram backbone does not reproduce (terminal sign not among top-5 PMI)
6. The BC=0 / BC>0 stratification does not separate the grammar / name-syllable classes

---

## Outputs Requested from ICIT Testing

1. Mahadevan-to-ICIT crosswalk table (CSV)
2. Token counts per crosswalked sign
3. Positional profiles (I/M/T rates) for top-100 signs
4. Top-30 directed bigrams with counts and PMI
5. Fish-sign context listing (all occurrences, isolation status)
6. Model pass/fail summary against Tests 1–8

---

## Suggested Contact

The ICIT corpus is associated with Dr. Andreas Fuls and the International Centre for Indus Texts and Images. The first contact should be a narrow technical question: is a Mahadevan-to-ICIT crosswalk available, and is there a preferred export format for running these tests?

See `outreach/icit_package_manifest.md` for the materials to send with the initial contact.
