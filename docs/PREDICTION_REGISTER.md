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

### PRED-2026-011 (H3 successor: Cross-Site Class Preservation — clean withholding, disclosed mappability screen)
**Date registered**: 2026-10-20  
**Prediction**: Signs assigned to the INITIAL class in training on CISI Mohenjo-daro inscriptions ONLY, after the disclosed mappability screen below, will appear preferentially in initial position in Harappa-specific Yajnadevam data as well.  
**Successor to**: PRED-2026-010 and, through it, PRED-2026-006. PRED-2026-010 used the same clean CISI Mohenjo-daro training pool and derived the INITIAL set P000, P217, P324. Under the frozen crosswalk reading, P000 has no best-match counterpart; it appears only as a `top3_parpola` alternative. Because one unmappable sign is 33% of that three-sign set, above PRED-2026-010's registered 20% cap, that prediction cannot be scored as written. This successor states the mappability eligibility rule before registration instead of changing PRED-2026-010 after the mapping problem was found.  
**Withheld data**: Harappa-site Yajnadevam sequences in `backend/glossa_lab/data/yajnadevam_inscriptions.csv` (SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`), held separate; byte-hashed only at this registration, not opened for content  
**Trained INITIAL set (derived at registration, frozen)**: P217, P324 — 2 signs. The unscreened classification reproduced PRED-2026-010 exactly: 179 CISI Mohenjo-daro inscriptions, 28 classifiable signs (INITIAL 3, MEDIAL 19, MIXED 3, TERMINAL 3), and unscreened INITIAL set P000, P217, P324. Derivation: `backend/scripts/pred011_register_derivation.py`; record: `docs/research/pred-2026-011-registration/derivation-record.json`  
**Mappability screen (the one disclosed design change)**: before registration, an INITIAL sign is eligible only if at least one row in the frozen public crosswalk names it as `best_parpola_match`. Appearances in `top3_parpola` do not establish a counterpart. P217 is eligible through Y0520 (confidence 1.0, confirmed); P324 is eligible through Y0740 (confidence 0.9867, confirmed); P000 is excluded because it has no best-match row and appears only in `top3_parpola` on Y0527, Y0740, Y0820, and Y0892. The screen used only the public crosswalk (SHA-256 `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`). No Harappa inscription rows, sequences, occurrence counts, or start rates informed the design. P000 was not excluded because of any observed Harappa behaviour; no Harappa behaviour for P000 was examined.  
**Training pool (fixed by hash)**: `data/normalized/corpus_master.csv` (SHA-256 `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`), filtered to source "Corpus of Indus Seals and Inscriptions (mayig digitization)" — all 179 rows Mohenjo-daro, zero Yajnadevam rows; filtered-pool manifest SHA-256 `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`  
**Crosswalk (fixed by reference)**: `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` (SHA-256 `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`). At scoring, sign identity is carried only by rows whose `best_parpola_match` is the trained sign. A trained sign with no counterpart is UNMAPPABLE; if unmappable signs exceed 20% of the trained set — with 2 signs, any single unmappable sign is 50% — the scoring closes as CANNOT BE RUN AS WRITTEN  
**Success criterion**: ≥ 70% of the trained INITIAL signs above show start_rate ≥ 0.40 at Harappa site (bars identical in form to PRED-2026-006 and PRED-2026-010). A sign's start rate is the share of its Harappa occurrences, counted through its best-match counterpart glyphs, in which it is the first sign of a sequence. A mappable sign with zero Harappa occurrences does not meet the bar and remains in the denominator  
**Small-set caveat — read before the criterion**: this is a two-sign test, weaker than PRED-2026-010's already small three-sign test. The possible shares are only 0, 1/2, and 1, so the 70% bar passes only at 2 of 2; each sign carries half the verdict. A pass would establish only that P217 and P324 both met the bar in this pinned dataset. It would not validate the INITIAL class as a whole, estimate a general cross-site preservation rate, say anything about P000's positional behaviour, or establish a decipherment or sign meaning. A failure would likewise be a failure of this exact two-sign criterion, not a refutation of cross-site preservation for the wider INITIAL class  
**Method constraint**: positional classification only; no semantic anchoring (SA-free)  
**Disclosure**: the Yajnadevam Harappa pool was previously inspected in aggregate during the Spec 032 closure audit, and those counts are published in its record (970 Harappa inscriptions inside the old combined training corpus, carrying 1,013 occurrences of 11 of 006's 12 trained signs). No Harappa start rate has ever been computed for P217 or P324. The cleanliness claimed here is verified training-pool exclusion — the trained set provably never saw the pool — not analyst blindness  
**Scoring gate**: registration alone is not a scoring order. Scoring requires its own future spec and a separate owner order.  
**OSF registration**: to be filed 2026-10-20 from the Predictions & Registrations node `nrb9u` (OSF Preregistration schema) under the same owner order; the verified URL and DOI are appended in §6 on approval (record: `docs/research/pred-2026-011-registration/README.md`)  
**Tested**: 2026-10-20 (Spec 036 / Phase-400, executed exactly as registered; step 0 passed in full and the scoring ran)  
**Outcome**: CONFIRMED — 2 of 2 trained signs at Harappa start rate ≥ 0.40 (P217: 104 initial of 119 occurrences, start rate 0.8739; P324: 473 initial of 774 occurrences, start rate 0.6111); share 1.0 against the ≥ 70% bar. The verdict concerns only these two signs in this pinned dataset; see the §6 entry of 2026-10-20 and `specs/036-pred-2026-011-scoring/outcome.md`

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

### 2026-10-20 — PRED-2026-011 registered (clean-withholding successor with disclosed mappability screen)

By owner order (Tristen Pierson, 2026-10-20), **PRED-2026-011** is registered in §3 above as the successor to PRED-2026-010. It asks the same cross-site INITIAL-class question with the same 70% and 0.40 bars, but its trained set was screened for mappability before registration using only the public, hash-pinned crosswalk. The resulting trained set is **P217, P324** (2 signs); P000 was excluded because it has no best-match counterpart, not because of any Harappa behaviour. The registration carries the two-sign caveat in its entry: the bar passes only at 2 of 2, and either outcome would concern only the exact two-sign criterion. An OSF Preregistration is filed the same day from the Predictions & Registrations node under the same owner order; its verified URL and DOI are appended to this section on approval (record: `docs/research/pred-2026-011-registration/README.md`). No scoring has run and no Harappa start rate has been computed. PRED-2026-010 is unaffected by this entry except as its named predecessor; no other prediction is affected. Scoring requires its own future spec and owner order.

### 2026-10-20 — PRED-2026-010 taken to execution (Spec 035 / Phase-399): CLOSED AT STEP 0 — CANNOT BE RUN AS WRITTEN (unscored)

Under Spec 035 (`specs/035-pred-2026-010-scoring/`; freeze digest `d72a50e1943c1af55846dfb2db93e73b50e08a287c06925a331c0304096128c4`; the prediction's OSF preregistration https://osf.io/wjebq/, DOI 10.17605/OSF.IO/WJEBQ, approved and public before execution and re-verified at step 0; the frozen spec's own OSF contract registration https://osf.io/qkj8d/, filed 2026-10-20 before execution and pending admin approval at execution), PRED-2026-010 was taken to execution under the owner's freeze-and-execute order of 2026-10-20, to be scored exactly as registered above: at least 70% of the trained INITIAL signs (P000, P217, P324) showing a start rate of at least 0.40 at Harappa in the withheld Yajnadevam data. The frozen design's step 0 (checks run before any counting, in a fixed order) closed the study at its fourth check, and this entry records that closure. The §3 entry above is unchanged: its Outcome stays **PENDING**, per the frozen claim F035-C15 — a closure is not a verdict.

Checks 0.1–0.3 passed: the preregistration stood accepted and public; every registered input pin matched; and the training pool re-derived exactly as registered (179 CISI Mohenjo-daro inscriptions, filtered-pool manifest SHA-256 `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`), with the recorded classification reproducing the trained set {P000, P217, P324} exactly — the clean withholding verified, not assumed. Check 0.4 (crosswalk coverage) failed: under the frozen best-match reading of the pinned crosswalk, P217 and P324 have confirmed counterparts (Y0520, match confidence 1.0; Y0740, 0.9867), but P000 has none — it appears only as a top-3 alternative on four rows (Y0527, Y0740, Y0820, Y0892). One unmappable sign of three is 33%, above the 20% cap stated in the §3 entry itself, so the scoring closed before the withheld file was opened; it was never opened, and no Harappa count or start rate was computed.

**Recorded outcome: CANNOT BE RUN AS WRITTEN** — a step-0 closure under the frozen Spec 035 design, reported as itself. It is not a verdict: PRED-2026-010 is neither CONFIRMED nor NOT CONFIRMED by this execution, and it remains **unscored**. §4 above gains no entry. Any future test of this hypothesis requires a trained set whose signs all carry crosswalk counterparts under a mapping fixed before counting, registered as a **new** prediction under a new PRED number before its withheld data is touched. Full record: `specs/035-pred-2026-010-scoring/outcome.md`; step-0 record: `reports/phase399_results.json` (step-0 record sha256 `e231baf4cd0c664211089c6758296c10a035062b6566ac5200407872e4aeee1f`). PRED-2026-006 is unaffected by this entry and remains **unscored**; no other prediction is affected.

### 2026-10-20 — PRED-2026-011 OSF registration approved and public (registration complete)

By owner order (Tristen Pierson, 2026-10-20), the OSF Preregistration for **PRED-2026-011** — filed the same day from the Predictions & Registrations node `nrb9u` under the registration order recorded above — has been approved and is public: https://osf.io/t6whq/, DOI **10.17605/OSF.IO/T6WHQ** (registration `t6whq`; `date_registered` 2026-10-20T12:54:02Z; verified by API on 2026-10-20: `reviews_state` accepted, public, `pending_registration_approval` false, not withdrawn, the DOI identifier exactly 10.17605/OSF.IO/T6WHQ, `registered_from` `nrb9u`). The registration of PRED-2026-011 is complete. The prediction stands **PENDING** and **unscored**: no scoring has run and no Harappa start rate has been computed, and scoring requires its own future spec and owner order. Record: `docs/research/pred-2026-011-registration/README.md`. No other prediction is affected.

### 2026-10-20 — PRED-2026-011 taken to execution (Spec 036 / Phase-400): CONFIRMED (2 of 2)

Under Spec 036 (`specs/036-pred-2026-011-scoring/`; freeze digest `bbd5c4fd5abdb69bd79dfc1115a13e7debf56a7ec38d00ab8e2c8ff6132e946`; the frozen spec's own OSF contract registration https://osf.io/gjen4/, filed 2026-10-20 under DD-036-4 before execution), PRED-2026-011 was taken to execution under the owner's do-all order of 2026-10-20, to be scored exactly as registered above: at least 70% of the trained INITIAL signs (P217, P324) showing a start rate of at least 0.40 at Harappa in the withheld Yajnadevam data — with 2 signs, only 2 of 2 passes. The prediction's preregistration (t6whq) is unaffected by this entry except as the registration this execution implemented.

Step 0 passed in full, in the frozen order. Check 0.1: the preregistration t6whq stood accepted and public (API re-verification at execution). Check 0.2: the corpus file, the crosswalk, and the withheld file all hashed to the registered pins (the withheld file byte-hashed only at step 0). Check 0.3: the CISI Mohenjo-daro pool re-derived as registered (179 inscriptions, all Mohenjo-daro, zero Yajnadevam rows; filtered-pool manifest hash matched), the recorded classification reproduced exactly (28 classifiable signs; unscreened INITIAL set P000, P217, P324), and the registered mappability screen re-applied returned the trained set {P217, P324} exactly, with P000's exclusion reproduced as a screen outcome. Check 0.4: under the frozen best-match reading, both trained signs carry confirmed counterparts (P217 → Y0520, confidence 1.0; P324 → Y0740, confidence 0.9867, conflict-flagged) — no unmappable trained sign (share 0.0 against the registered 20% cap), so the scoring opened. The withheld file's content was opened only after all four checks passed.

Scoring (the registered computation, run once, in full): over the withheld file's 2,717 Harappa rows (2,621 tokenised sequences, 7,144 tokens), counted through the frozen crosswalk — **P217: 119 Harappa occurrences, 104 in initial position, start rate 0.8739; P324: 774 Harappa occurrences, 473 in initial position, start rate 0.6111.** Both signs meet the 0.40 bar: share **1.0** (2 of 2), at or above the registered 70% criterion.

**Recorded outcome: CONFIRMED** — on the exact two-sign criterion as registered. The §3 entry above is updated in this same act: its Tested and Outcome fields move from PENDING to this verdict. The verdict's registered limits stand with it: it concerns only P217 and P324 in this pinned dataset; it does not validate the INITIAL class as a whole or estimate a general cross-site preservation rate; it says nothing about P000, whose exclusion was a mapping-eligibility outcome at registration and whose Harappa behaviour was not examined; and it establishes no decipherment or sign meaning. The independence is the registered site withholding (Harappa held out of training, re-verified at step 0), not independence of scholarly lineage, and the cleanliness basis is verified training-pool exclusion, not analyst blindness. Full record: `specs/036-pred-2026-011-scoring/outcome.md`; results: `reports/phase400_results.json` (step-0 record sha256 `2bf0333b7d7fc437c9055299598ee83f0247acd08c7fa8b123044114e0c8e427`; scoring record sha256 `101d54f5bd93d963402d73731962801294452c00f4fe4183e9135ba348ddb07f`). No other prediction is affected by this entry; PRED-2026-006's and PRED-2026-010's entries and records are unchanged.


### 2026-10-20 — PRED-2026-007 taken to execution (Spec 038 / Phase-401): CLOSED AT STEP 0 — CANNOT BE RUN AS WRITTEN (unscored)

Under Spec 038 (`specs/038-pred-2026-007-full-population/`; freeze digest `b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef`; the frozen spec's own OSF contract registration https://osf.io/bkqeh/, filed 2026-10-20 under DD-038-6 and pending admin approval at execution — not a step-0 condition, since the frozen step 0 names this register entry itself), PRED-2026-007 was taken to execution under the owner's freeze-and-execute order of 2026-10-20 ("Freeze D-31 for execution"), to be scored exactly as registered above: at least 70% of ITM-coded signs TERMINAL or in TERMINAL clusters, over the full ITM population enumerated from the frozen primary source. The frozen design's step 0 closed the study at its second check, and this entry records that closure. The §3 entry above is unchanged: its Outcome stays **PARTIALLY CONFIRMED** as the pre-execution record — a closure is not a verdict, and the 67% figure's denominator history (two ITM signs of the three the partial test counted; the third, P098, is LOG-coded and outside the criterion's population) stands visible and unedited.

Check 0.1 passed in full: this register file hashed to the freeze record's value; the PRED-2026-007 entry stood as registered; every source the census reads was present, readable, and hashed to the freeze record's cited values (primary `8c2bd605…`, cross-check `8a0b2a82…`, recorded clustering `623a787d…`, recorded characterisation `54ebf660…`); the coding-source readings stood in the cited form, and the conflict rule was in force. Check 0.2 (enumeration) failed, and the study closed there. The enumeration read all 611 per-sign records of the primary (`reports/indus_cgsa_cluster_analysis.json`, field `data.a[].icit_function`) mechanically — record-count reconciliation exact, no internal conflicts — and returned **zero ITM-coded signs**. The held-record verification, read at the same pass, failed with it: **P385's record in the primary carries an empty `icit_function` value**, not ITM; **P378 has no record in the primary at all**; P098 likewise has no record (its must-not-read-ITM condition was the only one of the three met). The reason is a property of the named file: its `icit_function` field is not a coded field — of its 611 values, **579 are empty and 32 are free-text decipherment glosses** (for example "fish+two -> miiNDu (fish again)"); **no record carries the value ITM, and none carries LOG**. The frozen population frame (Spec 038, DD-038-5) names this field as the source of the ITM codes, and the codes are not in it; under the frozen rule the enumeration's own integrity check therefore closes the study before any Phase 5 lookup. Check 0.3 never ran: the recorded clustering and characterisation were byte-hashed at 0.1 for integrity and never read for assignments. No cluster, class, share, or coverage figure was computed.

**Recorded outcome: CANNOT BE RUN AS WRITTEN** — a step-0 closure under the frozen Spec 038 design, reported as itself. It is not a verdict: PRED-2026-007 is neither CONFIRMED nor NOT CONFIRMED by this execution, and it remains **unscored**. §4 above gains no entry, and the Phase D pin is not advanced (it advances on a verdict; there is none). Any future test of this hypothesis requires a population frame whose coded values are verified in the named primary source itself before the design is frozen, registered as a **new** prediction under a new PRED number. Full record: `specs/038-pred-2026-007-full-population/outcome.md`; step-0 record: `reports/phase401_results.json` (step-0 record sha256 `4c026edc92cdcb0c1ba6821f5ebc8242b498bb9fc4cd158607d9b1ded24a784a`; enumeration sha256 `b849b0d45d37edea7f2c18af7733143b4e631f2e1aad27c6acaf42112a0436c7`). No other prediction is affected by this entry.

### 2026-10-20 — PRED-2026-007 provenance reconciliation (Spec 038, DD-038-2)

This appended note corrects, by append only, the provenance line in §2 above, which describes the per-sign function codes behind the Phase 5 classes as "from mayig features". That wording is not the lineage. The function classifications (ITM, LOG, SYL, NUM, TMK, SHN and the rest) were parsed by the programme's own sign-catalog parser (`backend/glossa_lab/data/fuls_parser.py`, SHA-256 `9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615` as cited at the Spec 038 freeze) from sign-catalog lines of "A Catalog of Indus Signs" (Fuls 2023), whose function classification the parser's own comment attributes to Wells ("Function classification (from Wells)"). The codes therefore descend from Wells-derived catalog lines, not from mayig features; the mayig digitisation produced inscription texts, not the function codes. §2's original wording stands unedited above, superseded by this note as the register's provenance record. This note changes no criterion, no count, and no outcome: it accompanies the Spec 038 execution record (see the entry above), under which PRED-2026-007 remains **unscored** with its §3 PARTIALLY CONFIRMED wording standing.
