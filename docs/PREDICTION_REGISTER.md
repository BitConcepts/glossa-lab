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

### PRED-2026-010 (H3 successor: Cross-Site Class Preservation — clean withholding)
**Date registered**: 2026-10-13  
**Prediction**: Signs assigned to the INITIAL class in training on CISI Mohenjo-daro inscriptions ONLY will appear preferentially in initial position in Harappa-specific Yajnadevam data as well.  
**Successor to**: PRED-2026-006 (above), which Spec 032 / Phase-396 closed at step 0 on 2026-10-13 as CANNOT BE RUN AS WRITTEN (unscored; see the dated §6 entry): its recorded classification had trained on the combined corpus, so the withheld Harappa data sat inside the training pool. This entry restates the same prediction and the same bars with that defect removed at registration, and is registered before its withheld data is touched, per §1.  
**Withheld data**: Harappa-site Yajnadevam sequences in `backend/glossa_lab/data/yajnadevam_inscriptions.csv` (SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`), held separate; byte-hashed only at this registration, not opened for content  
**Trained INITIAL set (derived at registration, frozen)**: P000, P217, P324 — 3 signs. Derived by the recorded `global_class_stability` classification logic (verbatim, as carried in the frozen Phase-396 build `backend/scripts/phase396_pred006_step0.py`, whose step-0 reconstruction reproduced the recorded output exactly) over the CISI Mohenjo-daro pool only: 179 inscriptions, 28 classifiable signs (INITIAL 3, MEDIAL 19, MIXED 3, TERMINAL 3). Derivation: `backend/scripts/pred010_register_derivation.py`; record: `reports/pred010_derivation_record.json`  
**Training pool (fixed by hash)**: `data/normalized/corpus_master.csv` (SHA-256 `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`), filtered to source "Corpus of Indus Seals and Inscriptions (mayig digitization)" — all 179 rows Mohenjo-daro, zero Yajnadevam rows; filtered-pool manifest SHA-256 `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`  
**Crosswalk (fixed by reference)**: `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` (SHA-256 `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`). At scoring, a trained sign with no crosswalk counterpart is UNMAPPABLE (denominator only); if unmappable signs exceed 20% of the trained set — with 3 signs, any single unmappable sign is 33% — the scoring closes as CANNOT BE RUN AS WRITTEN  
**Success criterion**: ≥ 70% of the trained INITIAL signs above show start_rate ≥ 0.40 at Harappa site (bars identical to PRED-2026-006)  
**Small-set caveat**: the clean pool yields 3 trained signs, so the share can only be 0, 1/3, 2/3, or 1, and the 70% bar passes only at 3 of 3; each sign carries a third of the verdict. The set is registered exactly as derived — the pool was not widened to enlarge it, because widening is what voided 006  
**Method constraint**: positional classification only; no semantic anchoring (SA-free)  
**Disclosure**: the Yajnadevam Harappa pool was previously inspected in aggregate during the Spec 032 closure audit, and those counts are published in its record (970 Harappa inscriptions inside the old combined training corpus, carrying 1,013 occurrences of 11 of 006's 12 trained signs). No Harappa start rate has ever been computed for any sign. The cleanliness claimed here is verified training-pool exclusion — the trained set provably never saw the pool — not analyst blindness  
**OSF registration**: https://osf.io/wjebq/ (filed 2026-10-13 from the Predictions & Registrations node `nrb9u`, OSF Preregistration schema; pending admin approval at filing; record: `docs/pred-2026-010-osf-registration.md`)  
**Tested**: PENDING  
**Outcome**: PENDING

---

## 4. Failed Predictions

No predictions have been formally tested and refuted yet. This section will be populated as predictions are evaluated.

---

## 5. Notes

The P122↔M342 crosswalk error (discovered 2026-04-22) is NOT a failed prediction — it was a data quality issue, not a falsification of the structural model. It has been corrected and logged in NORMALIZATION_RULES.md (rule N-CW-04).

---

## 6. Adjudication Notes (append-only)

### 2026-10-08 — Soviet positional dataset (Phase-121) adjudicated NON-QUALIFYING for PRED-2026-001/002 (Spec 020)

Under spec 020 (`specs/020-soviet-pred-adjudication/spec.md`), the Phase-121 Soviet positional dataset (Kondratov 1965 tables, extracted from Zide & Zvelebil 1976; `data/soviet_positional/`) was adjudicated against criteria derived mechanically from this register and spec 018 §§3–7, stated in the spec before application. **Verdict: NO — the dataset does not qualify as an evaluation source for PRED-2026-001 or PRED-2026-002.** It fails five of the six criteria: it falls within none of spec 018 §4's six frozen source classes (C1); it is not the full ICIT database named above as the withheld data, nor a qualifying substitute (C2); its published aggregate tables cannot yield the registered per-sign end_rate/start_rate statistics as spec 018 §6.2 defines them — the only per-sign table is a restricted stable-initial-pair × stable-final co-occurrence matrix with no occurrence denominators (C3); the frozen §5 deduplication protocol cannot be applied to it, as it contains no inscription token sequences (C4); and its signs are in Marshall catalogue numbers, for which no frozen map to Parpola space exists, and no spec 018 §7 adapter ingests aggregate tables (C5). It passes only the independence criterion (C6): its content was not a derivation input of the CGSA classes.

No evaluation was run: the Phase-119 harness scorers were not invoked on this dataset in evaluation mode or as a dry run, and no verdict on either prediction was produced. **PRED-2026-001 and PRED-2026-002 remain PENDING** (Tested/Outcome unchanged above); this note records an adjudication about a candidate data source, not a test of either prediction.

### 2026-10-12 — PRED-2026-004, PRED-2026-005, PRED-2026-008, PRED-2026-009 RETIRED (owner decision)

By owner decision (Tristen Pierson, 2026-10-12), PRED-2026-004, PRED-2026-005, PRED-2026-008, and PRED-2026-009 are **RETIRED**. The retirements are recorded here under this register's append-only discipline; the entries in §3 above are unchanged.

Each retired prediction was **never tested and never scored**, and none is refuted: no evaluation of its withheld data was ever run. The cause of retirement is the same in each case — the registered success criterion is defined on, or depends on, the Phase 9 simulated-annealing (SA) machinery, and Phase-107 falsified that SA method (held-out 0.000, 0/115). Each prediction is therefore untestable as registered:

- **PRED-2026-004 (H1: Morphological Decomposition)** — the success criterion is an SA mean_consistency comparison (Dravidian vs Pali, margin ≥ 0.05). RETIRED.
- **PRED-2026-005 (H2: Terminal Sign Phonotactics)** — the registered P385 phoneme test rests on the Phase 9 SA-line machinery. RETIRED.
- **PRED-2026-008 (H5: Dravidian Functional Projection)** — the success criterion is SA mean_consistency ≥ 0.65 in ≥ 4 of 5 runs. RETIRED.
- **PRED-2026-009 (H6: Negative Control — Chinese LM)** — the negative control for the same SA line (SA mean_consistency ≤ 0.50 under a Classical Chinese LM); with that test line retired, it has no live test to control. RETIRED.

Any successor to any of these hypotheses must be registered as a **new** prediction under a new PRED number, defined on an SA-free method; retired numbers are not reused. PRED-2026-001, PRED-2026-002, and PRED-2026-003 remain **PENDING**, and PRED-2026-006 and PRED-2026-007 remain **PARTIALLY CONFIRMED**; none of those five entries is affected by this note.

### 2026-10-13 — PRED-2026-006 taken to execution (Spec 032 / Phase-396): CLOSED AT STEP 0 — CANNOT BE RUN AS WRITTEN (unscored)

Under Spec 032 (`specs/032-pred-2026-006-harappa-breakdown/`; freeze digest `34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab`; OSF registration https://osf.io/3htn8/, DOI 10.17605/OSF.IO/3HTN8, approved and public before execution), PRED-2026-006 was taken to execution under the owner's order of 2026-10-13, to be scored exactly as registered above: at least 70% of the CISI-trained INITIAL signs showing a start rate of at least 0.40 at Harappa in the withheld Yajnadevam data. The frozen design's step 0 (provenance checks, run before any counting) closed the study at its second check, and this entry records that closure. The §3 entry above is unchanged.

Step 0.1 passed: the trained INITIAL set was reconstructed from the recorded `global_class_stability` lineage and reproduced exactly (105 classifiable signs, no differences), and frozen at the 12 signs P000, P001, P004, P013, P051, P098, P217, P238, P265, P301, P310, P324. Step 0.2 failed: the withholding this registration depends on was not real for that lineage. The recorded classification was trained on the combined corpus (`data/normalized/corpus_master.csv`, 2,722 inscriptions: 179 CISI, Mohenjo-daro only, plus 2,543 Yajnadevam), not on CISI Mohenjo-daro alone; and 970 of the Yajnadevam inscriptions inside that training corpus are Harappa inscriptions, carrying 1,013 occurrences of 11 of the 12 trained signs (P324 alone 468). The Harappa Yajnadevam sequences therefore played a part in training the very assignments the prediction would test. Step 0.3 was not reached, no start rate was computed, and no share exists.

**Recorded outcome: CANNOT BE RUN AS WRITTEN** — a step-0 closure under the frozen Spec 032 design, reported as itself. It is not a verdict: PRED-2026-006 is neither CONFIRMED nor NOT CONFIRMED by this execution, and it remains **unscored**. Its §3 "PARTIALLY CONFIRMED" wording stands as the pre-execution record, resting on the global 72.7% INITIAL figure — a neighbouring quantity, computed across all sites on the same pooled corpus, not the registered Harappa-specific test, which cannot now be produced from that lineage. Any future test of this hypothesis requires a trained set derived without the Yajnadevam corpus in the training pool, registered as a **new** prediction under a new PRED number before its withheld data is touched. Full record: `specs/032-pred-2026-006-harappa-breakdown/outcome.md`; step-0 record: `reports/phase396_results.json` (step-0 record sha256 `26781336c8c34b006e62474448b17be4d895c1d7ea06d5c24418d49a38e7c4e7`). No other prediction is affected by this entry.

### 2026-10-13 — PRED-2026-010 registered (clean-withholding successor to PRED-2026-006)

By owner order (Tristen Pierson, 2026-10-13), **PRED-2026-010** is registered in §3 above as the successor this section's previous entry calls for: the same prediction and the same bars as PRED-2026-006 (≥ 70% of the trained INITIAL signs showing start_rate ≥ 0.40 at Harappa), with the withholding made clean by construction. The trained set — **P000, P217, P324** (3 signs) — was derived at registration from the CISI Mohenjo-daro pool only (179 inscriptions, no Yajnadevam data in any form), by the recorded classification logic carried verbatim, and is fixed in the entry by hash (training pool, filtered-pool manifest, withheld file, crosswalk). The small-set caveat (the 70% bar passes only at 3 of 3) and the aggregate-inspection disclosure are stated in the entry itself. An OSF Preregistration of the successor contract was filed the same day from the Predictions & Registrations node: https://osf.io/wjebq/ (pending admin approval at filing; record: `docs/pred-2026-010-osf-registration.md`). No scoring has run and no Harappa start rate has been computed. PRED-2026-006 is unaffected by this entry and remains **unscored**; no other prediction is affected.
