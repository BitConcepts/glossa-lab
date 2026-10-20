# Proposed PREDICTION_REGISTER.md text for PRED-2026-011

> ## PROPOSED TEXT — DRAFT — NOT REGISTERED
>
> This file is not part of the authoritative register.
> It holds the text proposed for a future registration
> act. Do not cite it as a completed registration.
>
> At filing, the registration act must replace the
> draft status, registration date, and OSF placeholders
> with the verified filing facts before appending the
> entry. No OSF registration has been filed for
> PRED-2026-011.

## Proposed §3 entry

### PRED-2026-011 (H3 successor: Cross-Site Class Preservation — clean withholding, disclosed mappability screen)
**Registration status**: DRAFT — NOT REGISTERED  
**Draft prepared**: 2026-10-20  
**Date registered**: NOT REGISTERED  
**Prediction**: Signs assigned to the INITIAL class in training on CISI Mohenjo-daro inscriptions ONLY, after the disclosed mappability screen below, will appear preferentially in initial position in Harappa-specific Yajnadevam data as well.  
**Successor to**: PRED-2026-010 and, through it, PRED-2026-006. PRED-2026-010 used the same clean CISI Mohenjo-daro training pool and derived the INITIAL set P000, P217, P324. Under the frozen crosswalk reading, P000 has no best-match counterpart; it appears only as a `top3_parpola` alternative. Because one unmappable sign is 33% of that three-sign set, above PRED-2026-010's registered 20% cap, that prediction cannot be scored as written. This successor states the mappability eligibility rule before registration instead of changing PRED-2026-010 after the mapping problem was found.  
**Withheld data**: Harappa-site Yajnadevam sequences in `backend/glossa_lab/data/yajnadevam_inscriptions.csv` (SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`), held separate; byte-hashed only for this draft, not opened for content  
**Trained INITIAL set (derived for this draft; proposed for registration)**: P217, P324 — 2 signs. The unscreened classification reproduced PRED-2026-010 exactly: 179 CISI Mohenjo-daro inscriptions, 28 classifiable signs (INITIAL 3, MEDIAL 19, MIXED 3, TERMINAL 3), and unscreened INITIAL set P000, P217, P324. Derivation: `backend/scripts/pred011_register_derivation.py`; record: `docs/research/pred-2026-011-registration/derivation-record.json`  
**Mappability screen (the one disclosed design change)**: before registration, an INITIAL sign is eligible only if at least one row in the frozen public crosswalk names it as `best_parpola_match`. Appearances in `top3_parpola` do not establish a counterpart. P217 is eligible through Y0520 (confidence 1.0, confirmed); P324 is eligible through Y0740 (confidence 0.9867, confirmed); P000 is excluded because it has no best-match row and appears only in `top3_parpola` on Y0527, Y0740, Y0820, and Y0892. The screen used only the public crosswalk. No Harappa inscription rows, sequences, occurrence counts, or start rates informed the design. P000 was not excluded because of any observed Harappa behaviour; no Harappa behaviour for P000 was examined.  
**Training pool (fixed by hash)**: `data/normalized/corpus_master.csv` (SHA-256 `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`), filtered to source "Corpus of Indus Seals and Inscriptions (mayig digitization)" — all 179 rows Mohenjo-daro, zero Yajnadevam rows; filtered-pool manifest SHA-256 `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`  
**Crosswalk (fixed by reference)**: `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` (SHA-256 `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`). At scoring, sign identity is carried only by rows whose `best_parpola_match` is the trained sign. A trained sign with no counterpart is UNMAPPABLE; if unmappable signs exceed 20% of the trained set — with 2 signs, any single unmappable sign is 50% — the scoring closes as CANNOT BE RUN AS WRITTEN  
**Success criterion**: ≥ 70% of the trained INITIAL signs above show start_rate ≥ 0.40 at Harappa site (bars identical in form to PRED-2026-006 and PRED-2026-010). A sign's start rate is the share of its Harappa occurrences, counted through its best-match counterpart glyphs, in which it is the first sign of a sequence. A mappable sign with zero Harappa occurrences does not meet the bar and remains in the denominator  
**Small-set caveat — read before the criterion**: this is a two-sign test, weaker than PRED-2026-010's already small three-sign test. The possible shares are only 0, 1/2, and 1, so the 70% bar passes only at 2 of 2; each sign carries half the verdict. A pass would establish only that P217 and P324 both met the bar in this pinned dataset. It would not validate the INITIAL class as a whole, estimate a general cross-site preservation rate, say anything about P000's positional behaviour, or establish a decipherment or sign meaning. A failure would likewise be a failure of this exact two-sign criterion, not a refutation of cross-site preservation for the wider INITIAL class  
**Method constraint**: positional classification only; no semantic anchoring (SA-free)  
**Disclosure**: the Yajnadevam Harappa pool was previously inspected in aggregate during the Spec 032 closure audit, and those counts are published in its record (970 Harappa inscriptions inside the old combined training corpus, carrying 1,013 occurrences of 11 of 006's 12 trained signs). No Harappa start rate has ever been computed for P217 or P324. The cleanliness claimed here is verified training-pool exclusion — the trained set provably never saw the pool — not analyst blindness  
**OSF registration**: NOT FILED. The ready-to-file text is `docs/research/pred-2026-011-registration/osf-registration-payload.md`; filing awaits a separate owner registration order  
**Tested**: NOT REGISTERED  
**Outcome**: NOT REGISTERED

---

## Proposed §6 note for the future registration act

The following note is also proposed text only. Its
date and OSF fields must be completed from the actual
registration act; it is not a current register note.

### [REGISTRATION DATE] — PRED-2026-011 registered (clean-withholding successor with disclosed mappability screen)

By owner order (Tristen Pierson, [REGISTRATION DATE]), **PRED-2026-011** is registered in §3 above as the successor to PRED-2026-010. It asks the same cross-site INITIAL-class question with the same 70% and 0.40 bars, but its trained set was screened for mappability before registration using only the public, hash-pinned crosswalk. The resulting trained set is **P217, P324** (2 signs); P000 was excluded because it has no best-match counterpart, not because of any Harappa behaviour. The registration carries the two-sign caveat in its entry: the bar passes only at 2 of 2, and either outcome would concern only the exact two-sign criterion. An OSF Preregistration was filed the same day from the Predictions & Registrations node: [OSF URL AND DOI TO BE COMPLETED AFTER VERIFIED FILING]. No scoring has run and no Harappa start rate has been computed. PRED-2026-010 is unaffected by this entry except as its named predecessor; no other prediction is affected.
