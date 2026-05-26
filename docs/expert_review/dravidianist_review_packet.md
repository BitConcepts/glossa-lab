---
title: "Expert Review Packet: Proto-Dravidian Readings for the Indus Script"
author: "Tristen Kyle Pierson, BitConcepts LLC"
date: "May 2026"
geometry: "margin=1in"
fontsize: 11pt
---

**Preprint DOI:** 10.5281/zenodo.20401711 | **Repository:** github.com/BitConcepts/glossa-lab

**Purpose:** We are requesting expert critique of the proposed Proto-Dravidian sign readings. We ask for honest assessment, not endorsement.

---

## 1. What This Paper Claims

- A computational model assigns Proto-Dravidian readings to 605 Indus signs: **413 independently confirmed** (two or more independent evidence sources) and **192 allograph-inferred** (provisional, based on positional profile similarity).
- Each reading is linked to a **DEDR entry** (Burrow & Emeneau 1984).
- The model predicts a **tripartite grammar**: [CLASSIFIER/TITLE] – [NAME/CONTENT] – [CASE SUFFIX].
- Simulated annealing (SA) achieves 83.7% consistency on an independent 5,520-inscription corpus.
- Tamil-Brahmi personal name concordance reaches 58% (z=16.2).

## 2. What This Paper Does NOT Claim

- The paper does **not** claim epigraphic finality or definitive decipherment.
- The readings are **candidate** Proto-Dravidian forms, not established translations.
- The paper does **not** claim the Indus script is purely syllabic; the proposed model is mixed logo-syllabic.
- The statistical profile alone does not prove linguistic status (see Sproat 2014 benchmark comparison in the preprint).
- Individual seal "translations" are interpretive and caveated.
- 192 of 605 readings are allograph-inferred and should be treated as provisional.

## 3. Key Readings for Review

The attached **dravidianist_anchor_subset.csv** contains the 50 highest-leverage sign readings — those with the highest corpus frequency and the strongest bearing on overall model validity. For each sign, the CSV provides:

- Mahadevan M-number
- Proposed reading
- DEDR reference number
- Reconstructed form
- Evidence basis (iconographic, distributional, SA, external)
- Confidence notes and known weaknesses

## 4. Specific Questions for Reviewers

Detailed questions are in Section 7 below. Summary:

1. Are the proposed Proto-Dravidian / Old Tamil forms linguistically plausible for the target period (~2600–1900 BCE)?
2. Are any readings anachronistic or phonologically impossible?
3. Are the DEDR entries being used correctly?
4. Are the semantic shifts reasonable or too loose?
5. Does the Tamil-Brahmi comparison (58% concordance) overreach?
6. Which readings should be downgraded or removed?

## 5. Suspected Weak Readings

The following categories of readings are most likely to contain errors:

- **Low-frequency signs** (corpus frequency < 10): Limited distributional evidence; rely heavily on SA modal + DEDR lookup.
- **Allograph-resolved signs** (192 signs): Promoted via positional profile similarity (L1 distance < 0.2). If the allograph grouping is wrong, the inherited reading is also wrong.
- **Munda substrate readings** (M374=kul, M351=vī): Cross language-family boundaries and require specialist assessment.
- **MEDIAL-only signs**: Signs appearing exclusively in the name/content slot may have correct positional classification but incorrect phonetic assignment.

## 6. How to Use This Packet

1. Review the attached **dravidianist_anchor_subset.csv** for specific sign readings.
2. Consult **Section 7** below for 18 targeted review questions.
3. The full anchor table (605 signs) is in the repository at github.com/BitConcepts/glossa-lab.
4. The full preprint PDF is attached or available at the DOI above.

We welcome critique rather than endorsement. The goal is to identify which readings are linguistically defensible and which should be downgraded or removed before journal submission.
