# PREPRINT_OUTLINE
**Version**: 1.0 (DRAFT)  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts, LLC  
**Confidentiality**: INTERNAL

---

## 1. Target Publication Strategy

- **Format**: arXiv preprint (cs.CL + econ.GN cross-listing)
- **Fallback**: SSRN for social sciences readership
- **Journals (post-preprint)**: Journal of Archaeological Science; *Language* (LSA); Journal of the Economic and Social History of the Orient
- **Timing**: After HIGH signal achieved; patent review completed; expert review obtained

---

## 2. Proposed Title

"A Corpus-Grounded Structural Analysis of the Indus Sign System: Reproducible Positional Grammar Across 52 Archaeological Sites"

(Alternative: "Cross-Site Stability of Positional Classes in the Indus Script: Evidence from 2,722 Inscriptions")

---

## 3. Authors

Tristen Pierson (BitConcepts, LLC) — sole author unless co-authorship agreement signed

---

## 4. Abstract (Draft)

We present CGSA (Corpus-Grounded Structural Analysis), a computational methodology applied to 2,722 Indus inscriptions from 52 archaeological sites. CGSA identifies 40 structural sign clusters exhibiting a three-slot positional grammar (INITIAL-MEDIAL-TERMINAL) with 85.3% cross-site stability — a new empirical measurement not previously reported in Indus script literature. The structural classes are independently confirmed by the holdatllc corpus (different researcher, different methodology), and are inconsistent with non-linguistic generator models per the Nair (2026) scorecard. We further present substitution analysis results suggesting closer structural compatibility with Dravidian morphological patterns than Sanskrit or Pali controls. We do not claim a confirmed decipherment. We present this as a structural finding with clear reproducibility and explicit falsifiability criteria.

---

## 5. Paper Structure

### 1. Introduction (2 pages)
- Problem statement: Indus script remains undeciphered; previous computational approaches and criticisms
- Our contribution: CGSA methodology, cross-site validation, non-linguistic baseline comparison
- What we claim and what we do not claim

### 2. Corpus (1.5 pages)
- CISI Vol. 1 (179 inscriptions, Mohenjo-daro)
- Yajnadevam (2,543 inscriptions, 52 sites)
- Normalization rules
- Dataset statistics

### 3. Methodology (3 pages)
- CGSA Phases 1–6: sign inventory, registry, structural analysis, clustering
- Positional classification thresholds
- Global-then-local stability assessment
- Baseline comparison framework (Nair 2026)
- Substitution analysis for linguistic compatibility

### 4. Results (4 pages)
- Sign distribution statistics
- 40-cluster structural model
- 3-slot positional grammar
- Cross-site stability: 85.3% full, 95.1% partial
- Entropy reduction: 21.6%
- Nair scorecard: 4/4 linguistic-consistent
- holdatllc cross-validation: 2 INITIAL signs confirmed
- SA results: Dravidian vs Pali vs Sanskrit

### 5. Discussion (2 pages)
- Structural findings vs previous analyses
- Implications for linguistic hypothesis (Dravidian)
- Limitations: corpus size, no bilingual text, no image-backed crosswalk
- Comparison with Rao et al. (2009) and response to Sproat (2010)
- Non-linguistic alternatives and why they fail

### 6. Conclusion (0.5 pages)
- Summary of findings
- Falsifiability criteria
- Next steps: ICIT data access, held-out predictions, expert review

### Appendix
- Normalization rules (ref NORMALIZATION_RULES.md)
- Full cluster table (ref cluster_characterization.md)
- Reproduction instructions (ref REPRODUCIBILITY_PROTOCOL.md)
- SHA256 artifact hashes

---

## 6. Key References to Include

- Parpola, A. (1994). Deciphering the Indus Script. Cambridge.
- Mahadevan, I. (1977). The Indus Script: Texts, Concordance and Tables.
- Rao, R.P.N. et al. (2009). A Markov Model of the Indus Script. *Science*.
- Sproat, R. (2010). Ancient Symbols, Computational Linguistics, and the Reviewing Practices of the General Science Journals. *Computational Linguistics*.
- Fuls, A. (2014). A computational analysis of the Indus script.
- Wells, B. (2011). The Archaeology and Epigraphy of Indus Writing.
- Nair, A. (2026). How Non-Linguistic Is the Indus Sign System? arXiv:2604.17828.

---

## 7. Figures Needed

1. Map of 52 sites with inscription counts
2. Positional slot grammar diagram (INITIAL-MEDIAL-TERMINAL)
3. Cluster heatmap (40 clusters × positional metrics)
4. Cross-site stability heatmap
5. Nair scorecard comparison chart
6. Top-20 recurrent templates frequency chart
7. Entropy reduction before/after clustering
