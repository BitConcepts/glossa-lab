# PREDICTION_REGISTER
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts LLC  
**Confidentiality**: INTERNAL

---

## 1. Protocol

Per Section 6 of the Operating Instructions: predictions must be registered BEFORE the withheld data is evaluated. This document is the authoritative register. Adding a prediction after evaluating the withheld data is a scientific integrity violation.

Format per prediction:
- **Prediction ID**: Sequential, format PRED-YYYY-NNN
- **Date registered**: ISO 8601
- **Prediction**: Precise, falsifiable statement
- **Withheld data**: What data is being held back
- **Success criterion**: Quantitative threshold for pass/fail
- **Tested**: Date tested, or PENDING
- **Outcome**: CONFIRMED / REFUTED / INCONCLUSIVE / PENDING
- **Interpretation**: What the result means

---

## 2. Structural Predictions

### PRED-2026-001
**Date registered**: 2026-04-23  
**Prediction**: Signs classified as TERMINAL by the CGSA model will have end_rate ≥ 0.45 in the ICIT full corpus (6,800 inscriptions) when it becomes available.  
**Withheld data**: Full ICIT database (awaiting Dr. Fuls response)  
**Success criterion**: ≥ 10 of the 14 current TERMINAL signs show end_rate ≥ 0.45 in ICIT data  
**Tested**: PENDING  
**Outcome**: PENDING

### PRED-2026-002
**Date registered**: 2026-04-23  
**Prediction**: Signs classified as INITIAL by the CGSA model will have start_rate ≥ 0.45 in the ICIT full corpus.  
**Withheld data**: Full ICIT database  
**Success criterion**: ≥ 8 of the 12 current INITIAL signs show start_rate ≥ 0.45 in ICIT data  
**Tested**: PENDING  
**Outcome**: PENDING

### PRED-2026-003
**Date registered**: 2026-04-23  
**Prediction**: The 3-slot INITIAL-MEDIAL-TERMINAL template structure will account for ≥ 70% of inscription templates in any newly acquired multi-site dataset.  
**Withheld data**: Any dataset not yet acquired (ICIT, ASI archives)  
**Success criterion**: Template coverage ≥ 70% in held-out corpus  
**Tested**: PENDING  
**Outcome**: PENDING

---

## 3. Linguistic Hypotheses (Phase 9)

Seeded 2026-04-22 via scripts/seed_phase9_hypotheses.py. These are the 6 falsifiable hypotheses from Phase 9:

### PRED-2026-004 (H1: Morphological Decomposition)
**Date registered**: 2026-04-22  
**Prediction**: The 3-slot INITIAL-MEDIAL-TERMINAL slot assignment matches Dravidian morphological structure (title + root + case) better than matched-length Pali or Sanskrit sequences.  
**Withheld data**: Dravidian corpus held-out 20% test set  
**Success criterion**: SA mean_consistency on Dravidian > SA mean_consistency on Pali by ≥ 0.05  
**Tested**: PENDING (Phase 9 experiments running)  
**Outcome**: PENDING

### PRED-2026-005 (H2: Terminal Sign Phonotactics)
**Date registered**: 2026-04-22  
**Prediction**: P385 (primary TERMINAL sign) will show highest LM probability under Dravidian terminal phonotactics (final /n/, /l/, /ku/, /al/) vs random phoneme assignment.  
**Withheld data**: Dravidian phonotactic frequency data  
**Success criterion**: P385 Dravidian terminal probability > P385 random-assignment probability  
**Tested**: PENDING (P385 phoneme test experiment queued)  
**Outcome**: PENDING

### PRED-2026-006 (H3: Cross-Site Class Preservation)
**Date registered**: 2026-04-22  
**Prediction**: Signs assigned to INITIAL class in CISI Mohenjo-daro will appear preferentially in initial position in Harappa-specific Yajnadevam data as well.  
**Withheld data**: Harappa-site Yajnadevam sequences (held separate from full corpus analysis)  
**Success criterion**: ≥ 70% of CISI-trained INITIAL signs show start_rate ≥ 0.40 at Harappa site  
**Tested**: PARTIALLY — global_class_stability.py shows 72.7% for INITIAL class; Harappa-specific breakdown pending  
**Outcome**: PARTIALLY CONFIRMED

### PRED-2026-007 (H4: ICIT Function Alignment)
**Date registered**: 2026-04-22  
**Prediction**: Signs with ICIT function code ITM will cluster into TERMINAL class in CGSA Phase 5 at rate ≥ 70%.  
**Withheld data**: ICIT function codes (from mayig features)  
**Success criterion**: ≥ 70% of ITM-coded signs are TERMINAL or cluster in TERMINAL clusters  
**Tested**: PARTIALLY — P385 (ITM) is Cluster 21 TERMINAL; P378 (ITM) is Cluster 39 TERMINAL; P098 (LOG) is Cluster 10 INITIAL. 2/3 ITM in TERMINAL (67%)  
**Outcome**: PARTIALLY CONFIRMED (one more ITM needed for full pass)

### PRED-2026-008 (H5: Dravidian Functional Projection)
**Date registered**: 2026-04-22  
**Prediction**: SA on Indus corpus with Dravidian LM will show mean_consistency ≥ 0.65 across 5 independent runs with different anchor configurations.  
**Withheld data**: 5 independent anchor configurations  
**Success criterion**: mean_consistency ≥ 0.65 in ≥ 4 of 5 runs  
**Tested**: PENDING (multiple anchor runs being conducted)  
**Outcome**: PENDING

### PRED-2026-009 (H6: Negative Control — Chinese LM)
**Date registered**: 2026-04-22  
**Prediction**: SA on Indus corpus with Classical Chinese LM (logographic, non-agglutinative) will show mean_consistency ≤ 0.50.  
**Withheld data**: Classical Chinese LM  
**Success criterion**: mean_consistency ≤ 0.50 (significantly below Dravidian)  
**Tested**: PENDING  
**Outcome**: PENDING

---

## 4. Failed Predictions

No predictions have been formally tested and refuted yet. This section will be populated as predictions are evaluated.

---

## 5. Notes

The P122↔M342 crosswalk error (discovered 2026-04-22) is NOT a failed prediction — it was a data quality issue, not a falsification of the structural model. It has been corrected and logged in NORMALIZATION_RULES.md (rule N-CW-04).
