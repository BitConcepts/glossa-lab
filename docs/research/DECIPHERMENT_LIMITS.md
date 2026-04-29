# DECIPHERMENT_LIMITS
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / Layer1Labs Silicon, Inc.  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document records the hard limits of the Glossa-Lab Indus decipherment methodology. These are not disclaimers — they are precise statements of what the evidence does and does not support. Keeping this document current is as important as recording successes.

---

## 2. What We Can Currently Claim

| Claim | Confidence | Supporting Evidence |
|-------|-----------|---------------------|
| The Indus corpus has a 3-slot positional grammar (INITIAL-MEDIAL-TERMINAL) | HIGH | CGSA, holdatllc, Fuls prior, 85.3% cross-site stability |
| P385 is a frequent TERMINAL sign | HIGH | end_rate=0.785, SA 0.8591, ICIT ITM, holdatllc convergence |
| P324 is a frequent INITIAL sign | HIGH | start_rate=0.690, SA anchor, ICIT ITM |
| The corpus shows formulaic structure inconsistent with pure heraldic/emblem system | HIGH | 86.0% recurrent template coverage; H2=3.48 bits |
| Structural classes are cross-site stable | HIGH | 85.3% full stability across 52 sites |
| Sign system complexity is consistent with linguistic encoding | MODERATE | Nair (2026) scorecard: 4/4 metrics in linguistic range |

---

## 3. What We Cannot Currently Claim

| Claim | Reason |
|-------|--------|
| Indus script encodes Dravidian language | No confirmed phonetic reading; Dravidian is the leading structural hypothesis only |
| Any specific sign has a specific phoneme value | No bilingual text; no held-out prediction confirmed for phonetics |
| Any inscription has a specific meaning | Translation requires phonetic assignment + vocabulary; neither is confirmed |
| Reading direction is definitively RTL or LTR | SA experiments show RTL slightly favored; not definitively resolved |
| The corpus is complete | CISI/ICIT has ~6,800 inscriptions; we have analyzed 2,722 (40%) |
| Sign identity across numbering systems | No image-backed crosswalk; P122↔M342 error demonstrates this risk |
| The script is syllabic/alphabetic/logographic | Inventory size (803 signs) is between syllabary and logographic; not resolved |
| Undeciphered portions can be read | No phonetic framework; reading attempts are structural projections only |

---

## 4. Hard Methodological Limits

### 4.1 No Bilingual Text
There is no confirmed bilingual text, bilingue, or digraphic inscription that provides a cryptanalytic key for the Indus script. Without this, phonetic assignments remain speculative.

### 4.2 No Visual Sign Validation
The canonical sign registry is built from text-format sign IDs (P-numbers, Y-numbers, M-numbers). We have not confirmed sign identities by examining the original CISI plate images or ICIT images. The P122↔M342 crosswalk error shows this is a real risk.

### 4.3 Corpus Size Constraint
The 2,722 inscriptions analyzed represent approximately 40% of the known corpus. Structural patterns in a larger corpus may differ from current findings.

### 4.4 SA Stochasticity
Substitution analysis (SA) results are LLM-dependent. SA results are not deterministic and cannot be cited as definitive evidence without replication. SA is used for hypothesis generation, not hypothesis confirmation.

### 4.5 Site Bias
The CISI component (179 inscriptions) is Mohenjo-daro-only. The Yajnadevam component (2,543) covers 52 sites but with uneven site representation. Site-specific structural patterns may not generalize.

---

## 5. Signals That Would Upgrade the Claims

| Signal | Would Enable |
|--------|-------------|
| Held-out prediction success on CISI corpus subset | Upgrade structural hypothesis to HIGH confidence |
| Confirmed held-out prediction on new acquisition (ICIT data) | Possible HIGH SIGNAL upgrade |
| External expert (Fuls or equivalent) confirms non-trivial finding | Required for CRITICAL SIGNAL |
| Bilingual text or evolutionary link to Brahmi confirmed | Would unlock phonetic hypothesis testing |
| Image-backed crosswalk for top 30 signs | Would allow visual sign validation |

---

## 6. Falsifiability Statements

The following observations would falsify or severely weaken our structural model:

1. Cross-site analysis on ICIT data showing < 60% class stability (our model predicts 85%+)
2. Positional class assignments proven reversed by independent image-backed analysis
3. Formulaic template structure proven absent in Harappa tablet sequence data
4. Entropy reduction shown to be ≤ 5% (matching random clustering baseline)
5. SA mean_consistency on Indus + Dravidian shown to match SA on Indus + any random language
