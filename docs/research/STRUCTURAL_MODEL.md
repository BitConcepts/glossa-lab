# STRUCTURAL_MODEL
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / Layer1Labs Silicon, Inc.  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document describes the structural model of the Indus sign system derived from Glossa-Lab CGSA (Corpus-Grounded Structural Analysis) Phases 1–6. No phonetic claims are made in this document.

---

## 2. Model Summary

| Property | Value |
|----------|-------|
| Method | CGSA (Corpus-Grounded Structural Analysis) |
| Corpus | 2,722 inscriptions, 52 sites |
| Sign space | 803 distinct sign IDs |
| Classified signs | 160 P-signs (positional data sufficient) |
| Number of clusters | 40 structural clusters |
| Clustering algorithm | Agglomerative hierarchical (ward linkage, n_clusters=40) |
| Features used | start_rate, internal_rate, end_rate, freq_log, co-occurrence graph embedding |
| Cross-site stability | 85.3% (full) / 95.1% (full+partial) |
| Entropy reduction | 2.31 bits (21.6%) from raw to class-label space |

---

## 3. Positional Slot Schema

The Indus inscription structure is consistently modeled as a 3-slot schema:

```
[ INITIAL_SLOT ] [ MEDIAL_SLOT+ ] [ TERMINAL_SLOT ]
```

| Slot | Description | Evidence |
|------|-------------|---------|
| INITIAL_SLOT | Opening sign(s); candidate title, determinative, or personal name marker | 12 signs with start_rate ≥ 0.55; recurrent templates confirm INITIAL-MEDIAL ordering |
| MEDIAL_SLOT | Internal sign(s); candidate root, stem, or commodity specification | 46 signs with internal_rate ≥ 0.70; highest token volume in corpus |
| TERMINAL_SLOT | Closing sign(s); candidate case suffix, number, or formula marker | 14 signs with end_rate ≥ 0.55; strong convergence with holdatllc CASE_MARKER_SUFFIX class |

---

## 4. Recurrent Structural Templates (Top-20)

From decipherment_readiness_report.md — frequencies over 2,722 inscriptions:

| Template | Count |
|----------|-------|
| MEDIAL MEDIAL | 1,689 |
| MEDIAL MIXED | 1,195 |
| INITIAL MEDIAL | 1,161 |
| MIXED MEDIAL | 1,148 |
| INITIAL MIXED | 786 |
| MEDIAL TERMINAL | 742 |
| MIXED MIXED | 670 |
| MEDIAL MEDIAL MEDIAL | 616 |
| INITIAL MEDIAL MEDIAL | 568 |
| MEDIAL MEDIAL MIXED | 435 |
| MEDIAL MIXED MEDIAL | 398 |
| INITIAL MEDIAL MIXED | 378 |
| INITIAL INITIAL | 373 |
| MIXED MEDIAL MEDIAL | 362 |
| INITIAL MIXED MEDIAL | 351 |
| MEDIAL MEDIAL TERMINAL | 322 |

---

## 5. Cluster Inventory (Summary)

40 clusters derived from CGSA Phase 5. Full detail in `reports/cluster_characterization.md`.

| Class | Cluster Count | Total Token Coverage |
|-------|--------------|---------------------|
| TERMINAL | 8 clusters | ~880 tokens (P385, P378 dominant) |
| INITIAL | 8 clusters | ~2,600 tokens (P324, P098/P217 dominant) |
| MEDIAL | 15 clusters | ~5,600 tokens (P122, P050/P062/P145 dominant) |
| BIMODAL | 1 cluster | ~29 tokens |
| MIXED | 8 clusters | ~2,100 tokens |

---

## 6. Cross-Site Validation

From global_class_stability_report.md:

| Site Class | Stability Rate |
|-----------|---------------|
| INITIAL signs | 72.7% (8/11 stable) |
| MEDIAL signs | 82.2% (37/45 stable) |
| MIXED signs | 100.0% (33/33 stable) |
| TERMINAL signs | 69.2% (9/13 stable) |
| **Overall (full)** | **85.3%** |
| **Overall (full+partial)** | **95.1%** |

Phase 9 cross-site gate requirement: ≥ 70%. **PASSED.**

---

## 7. Dravidian Slot-Function Hypothesis

Based on convergence of CGSA, CAS Phase 9, holdatllc semantic roles, and SA phonotactic analysis:

| Slot | Structural class | holdatllc role | Dravidian function (candidate) |
|------|-----------------|----------------|-------------------------------|
| INITIAL | CLASSIFIER_PREFIX | INITIAL | Title/determinative/personal name |
| MEDIAL | MEDIAL_STRONG | (phonetic stem) | Noun root or commodity |
| TERMINAL | CASE_MARKER_SUFFIX | TERMINAL | Dravidian case suffix (genitive, dative) |
| BIMODAL | PERSON_OR_OWNER | BIMODAL | Owner/person marker |

**Status**: This is a structural-functional hypothesis only. No phonemic values are assigned. Falsifiable via held-out prediction (see PREDICTION_REGISTER.md).

---

## 8. Entropy Analysis

| Metric | Value |
|--------|-------|
| Sequence entropy (raw sign space) | 10.6691 bits |
| Sequence entropy (class-label space) | 8.3636 bits |
| Entropy reduction | 2.3055 bits (21.6%) |

Interpretation: the structural class-label representation captures genuine regularities in inscription structure. A random clustering would show near-zero entropy reduction.

---

## 9. Limitations

- Model is derived from 2,722 inscriptions; full CISI/ICIT corpus is ~6,800.
- 77 signs remain INSUFFICIENT_DATA and cannot be positioned in the model.
- No ICIT image validation has been performed for sign identity.
- The Dravidian slot hypothesis requires held-out prediction confirmation for upgrade to HIGH SIGNAL.
- RTL vs LTR reading direction not definitively resolved (see DECIPHERMENT_LIMITS.md).
