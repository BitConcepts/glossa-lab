# A Reusable Anchor Table and Validation Package for Computational Analysis of the Indus Script
## Draft — Journal of Open Humanities Data companion submission

**Author:** Tristen Kyle Pierson, Glossa-Lab / BitConcepts LLC

---

## Abstract

We present a public data package accompanying a computational study of the Indus Valley Script. The package includes a 397-sign anchor table with candidate readings at four confidence tiers (HIGH/MEDIUM/PROVISIONAL_MEDIUM/LOW), a Mahadevan–Parpola sign crosswalk, five supplemental datasets (fish-sign compound contexts, formula bigrams, iconographic co-selection pairs, polysemy permutation results), validated analysis scripts, and a formal ICIT cross-corpus validation plan. The package does not claim final decipherment; it provides reusable materials for testing, challenging, and extending a falsifiable positional-grammar model of Indus-script structure. All data are released under CC BY 4.0; all code under MIT License.

---

## 1. Context

The Indus Valley Script (~2600–1900 BCE) remains undeciphered in the absence of a bilingual inscription. Computational approaches have been applied to structural questions (Rao et al. 2009), phonological compatibility (Parpola 1994), and decipherment hypotheses (Mahadevan 1977), but publicly reusable data packages with explicit falsifiability criteria are rare.

This package accompanies the preprint "A Falsifiable Computational Anchor Model for the Indus Script" (Pierson 2026). The data and scripts are designed so that other researchers can: (1) test alternative readings against the same corpus; (2) challenge the structural claims with different statistical methods; (3) apply the scripts to the ICIT or another public Indus corpus after sign-code crosswalking; (4) compare Dravidian, proto-Munda, and language-neutral baselines using the same framework.

---

## 2. Dataset Description

### 2.1 Anchor Table (anchor_table_397.csv)

**Size:** 397 records (all Mahadevan M-numbers M001–M417+)

**Content:** For each sign: Mahadevan M-number, candidate phonetic/morphemic reading, confidence tier (HIGH 75 / MEDIUM 86 / PROVISIONAL_MEDIUM 4 / LOW 236), evidence basis summary, DEDR reference (Burrow & Emeneau 1984), positional class, Holdat corpus token count, and notes.

**Key statistics:**
- 161 HIGH/MEDIUM anchors cover 90.96% of corpus tokens
- 107 heuristic placeholder assignments were removed in Phase-133 (documented)
- 44/75 HIGH-confidence readings appear independently in Parpola (1994)
- 0/157 readings require Sanskrit-exclusive phonemes; 35/157 require Dravidian-exclusive phonemes

### 2.2 Fish-Sign Compound Contexts (fish_sign_contexts.csv)

**Size:** 27 records (13 M047 + 14 M001 occurrences)

**Content:** Seal ID, site, target sign, positional slot, left/right neighbor, full sign sequence, isolation flag (always FALSE).

**Use case:** Testing the fish-sign compound-only claim on alternative corpora.

### 2.3 Formula Bigrams (formula_bigrams.csv)

**Size:** 30 records (top-30 directed H+M×H+M bigrams)

**Content:** Sign pair, bigram label, occurrence count, seal count, PMI, candidate readings.

**Use case:** Testing formula backbone, computing betweenness centrality, comparing bigram structure across corpora.

### 2.4 Iconographic Formula Pairs (iconographic_formula_pairs.csv)

**Size:** 63 records (significantly enriched INITIAL-sign × seal-icon pairs)

**Content:** Initial sign, candidate reading, seal iconography, observed count, expected count, chi-square, Bonferroni-corrected p-value.

**Use case:** Testing professional-identity co-selection hypothesis with different corpora or different icon classification schemes.

### 2.5 Polysemy Divergence Summary (polysemy_divergence_summary.csv)

**Size:** 21 records (H+M signs tested for position-dependent collocate divergence)

**Content:** Sign, reading, KL divergence (bits), polysemy classification, null distribution mean/SD, permutation p-value.

**Use case:** Testing whether position-dependent meaning is a structural property of the corpus or a statistical artifact.

---

## 3. Methods

All datasets were produced by the Glossa-Lab computational pipeline (open-source, MIT License) running against the Holdat LLC Indus Corpus v3 (Miller 2025). The pipeline applies: positional analysis (I/M/T slot assignment per sign), bigram/trigram collocational methods (PMI, directed bigram graphs), chi-square enrichment tests (Bonferroni-corrected), permutation null tests (within-seal shuffles), betweenness centrality (NetworkX, normalized), and bootstrap confidence intervals for site-level KL divergences.

The AI Disclosure in the companion preprint applies to all datasets: AI tooling was used for scripting, data management, and literature search. All statistical methods are standard; interpretations were made by the author.

---

## 4. Quality Control

**Confidence tier system:** Each anchor reading requires a documented evidence basis. HIGH confidence requires two independent evidence sources. MEDIUM requires one strong source. PROVISIONAL_MEDIUM is flagged as requiring expert review. LOW is heuristic only and not used for coverage accounting.

**Heuristic placeholder removal:** Phase-133 removed 107 entries that had been assigned placeholder readings without meeting the stated evidence criteria. The dataset reflects the post-removal anchor inventory.

**Restricted-corpus labelling:** Fields derived from the non-public Holdat corpus are noted in the data dictionary (`docs/data_dictionary.md`). The token_count column in `anchor_table_397.csv` is restricted-corpus-derived; all other columns are public.

**Script validation:** `scripts/validation/run_all_public_checks.py` runs five integrity checks on the public tables and generates a pass/fail report. This script uses only the Python standard library and runs from a clean clone without requiring the restricted corpus.

---

## 5. Reuse Potential

Researchers can use these materials to:

1. **Test alternative linguistic hypotheses** — apply the same positional and bigram framework to proto-Munda, Indo-Aryan, or language-neutral syllabic baselines
2. **Map to ICIT** — the anchor table and scripts accept ICIT sign IDs after crosswalk; the ICIT validation plan (`docs/icit_validation_plan.md`) specifies the exact crosswalk and tests required
3. **Challenge structural claims** — the fish-sign compound-only result, the formula backbone, and the betweenness stratification can all be tested with any Indus corpus
4. **Extend the anchor model** — researchers with access to Holdat or ICIT can add or dispute anchor assignments using the documented confidence-tier criteria
5. **Compare decipherment proposals** — the anchor table provides a structured baseline against which Parpola (1994), Mahadevan (1977), Fuls (2014), and other proposals can be systematically compared

---

## 6. Limitations

- **No restricted corpus redistribution:** Corpus-level counts require access to Holdat LLC or a compatible corpus
- **Candidate readings, not verified transcriptions:** All phonetic readings are hypotheses; the model does not claim final decipherment
- **ICIT crosswalk pending:** Cross-corpus validation against the public ICIT corpus has not yet been completed; see `docs/icit_validation_plan.md`
- **Language-family comparison incomplete:** The model tests Proto-Dravidian compatibility but has not formally compared against Munda or Indo-Aryan baselines

---

## 7. Data Availability

All data and scripts: https://github.com/BitConcepts/glossa-lab/tree/main/research/indus/indus-anchor-model

Zenodo archive: (DOI to be assigned)

License: Code — MIT; Documentation and tables — CC BY 4.0

The Holdat LLC Indus Corpus v3 is not redistributed. See `data/restricted/README_restricted_data.md`.

---

## References

- Burrow, T. & Emeneau, M.B. (1984). *A Dravidian Etymological Dictionary* (2nd ed.). Oxford.
- Fuls, A. (2014). *A Catalog of Indus Signs*. TU Berlin / ICIT.
- Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. New Delhi: ASI.
- Miller, W. (2025). Holdat LLC Indus Corpus v3. Dataset.
- Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge.
- Pierson, T.K. (2026). A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script. Preprint v2.
- Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. *PNAS* 106(33).
