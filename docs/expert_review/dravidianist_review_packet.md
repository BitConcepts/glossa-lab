# Dravidianist / Old Tamil Expert Review Packet

**Paper**: *A Complete Computational Decipherment Hypothesis for the Indus Script*
**Author**: Tristen Kyle Pierson, BitConcepts LLC
**DOI**: 10.5281/zenodo.20401711

---

## 1. What This Paper Claims

- A computational model assigns **Proto-Dravidian readings** to all 605 known Indus
  signs using a five-layer evidence hierarchy.
- Each reading is linked to a **DEDR entry** (Burrow & Emeneau 1984).
- The model predicts a **tripartite grammar**: [CLASSIFIER/TITLE] – [NAME/CONTENT] – [CASE SUFFIX].
- Simulated annealing (SA) achieves 83.7% consistency on an independent 5,520-inscription corpus.
- Tamil-Brahmi personal name concordance reaches 58% (z=16.2).

## 2. What This Paper Does NOT Claim

- The paper does **not** claim epigraphic finality or definitive decipherment.
- The readings are **candidate** Proto-Dravidian forms, not established translations.
- The paper does **not** claim the Indus script is purely syllabic; the proposed
  model is mixed logo-syllabic.
- The statistical profile alone does not prove linguistic status (see §3.16 and
  the Sproat 2014 benchmark comparison).
- Individual seal "translations" (§4.1) are interpretive and caveated.

## 3. Key Readings for Review

The attached `dravidianist_anchor_subset.csv` contains the **50 highest-leverage
sign readings** — those with the highest corpus frequency and the strongest
bearing on overall model validity. For each sign, the CSV provides:

- Mahadevan M-number
- Proposed reading
- DEDR reference number
- Reconstructed form
- Evidence basis (iconographic, distributional, SA, external)
- Confidence notes and known weaknesses

## 4. Specific Questions for Reviewers

See `old_tamil_review_questions.md` for detailed questions. Summary:

1. Are the proposed Proto-Dravidian / Old Tamil forms linguistically plausible
   for the target period (~2600–1900 BCE)?
2. Are any readings anachronistic or phonologically impossible?
3. Are the DEDR entries being used correctly?
4. Are the semantic shifts reasonable or too loose?
5. Does the Tamil-Brahmi comparison (58% concordance) overreach?
6. Which readings should be downgraded or removed?

## 5. Suspected Weak Readings

The following categories of readings are most likely to contain errors:

- **Low-frequency signs** (corpus frequency < 10): These have limited
  distributional evidence and rely heavily on SA modal + DEDR lookup.
- **Allograph-resolved signs**: 192 signs promoted via allograph resolution
  (L1 distance < 0.2). If the allograph grouping is wrong, the reading inherits
  the error.
- **Munda substrate readings** (M374=kul, M351=vī): These cross language-family
  boundaries and require specialist assessment.
- **MEDIAL-only signs**: Signs appearing exclusively in MEDIAL (name) position
  may have correct positional classification but incorrect phonetic assignment.

## 6. How to Use This Packet

1. Review `dravidianist_anchor_subset.csv` for specific sign readings.
2. Consult `old_tamil_review_questions.md` for targeted questions.
3. The full anchor table (605 signs) is in the repository at
   `research/indus/anchor_table.json`.
4. The full preprint PDF is at the DOI link above.

We welcome critique rather than endorsement. The goal is to identify which
readings are linguistically defensible and which should be downgraded or
removed before journal submission.
