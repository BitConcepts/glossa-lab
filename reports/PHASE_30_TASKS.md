# Phase-30 Master Task List — Path to Full Decipherment

**Date:** 2026-04-30
**Predecessor:** Phase-29 (commit `3e3f775`)
**Decipherment progress at start:** ~12-15%
**Target:** ~25-40% by end of Phase-30 (months of compute possible)

This document lists every test/experiment we should run next, organized by
category and ranked by expected lift. Each task includes:

- **ID** — unique identifier (P30-{category}{number})
- **Priority** — P0 (do first), P1 (high), P2 (medium), P3 (low/optional)
- **Effort** — S (hours), M (days), L (weeks)
- **Lift** — expected delta in decipherment progress (pp = percentage points)
- **Depends on** — prerequisite tasks
- **Cite** — primary data source(s) per CITATIONS.md

---

## Category A. Statistical validation of Phase-29 findings (P0 — must run first)

The Enmenanak/Enheduana finding from Phase-29 needs proper validation before
we can claim significance.

### P30-A1. Permutation null model on the 1,222-PN search
- **Priority:** P0
- **Effort:** M (1-3 days)
- **Expected lift:** +1-3 pp (if significant) or 0 pp (if rejected)
- **Plan:** Build `M77ReverseJanabiyahPermNull` atomic node. Permute the
  miin-rendering set 10,000× while keeping the 1,222-PN corpus fixed; compute
  the rank-percentile of Enmenanak's score 7.0 vs the null distribution.
- **Cite:** Section A.1 (Mahadevan 1977), B.1 (ePSD2)

### P30-A2. Period filter for the 102 position-matched candidates
- **Priority:** P0
- **Effort:** S (4-8 hours)
- **Expected lift:** +1 pp
- **Plan:** Filter the 102 candidates to those attested in Old Akkadian or
  Ur III periods (overlapping Janabiyah's Early Dilmun ~2100-2000 BCE).
  Build `EPSD2PeriodFilter` atomic node.
- **Cite:** Section B.1 (ePSD2 period tags)

### P30-A3. Meluhha co-occurrence filter
- **Priority:** P0
- **Effort:** M (1-3 days)
- **Expected lift:** +2-3 pp (if any candidate co-occurs with me-luh-ha)
- **Plan:** For each of the 102 candidates, search the 1,462 CDLI Meluhha
  tablets to see if any tablet co-mentions the candidate name AND a Meluhha
  keyword. Build `MeluhhaCooccurrenceFilter` atomic node.
- **Cite:** Section B.3 (CDLI), B.1 (ePSD2)

### P30-A4. Bootstrap CI on Enmenanak score
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Plan:** Bootstrap 1,000× the segment-position assignment to compute 95%
  CI on the Enmenanak score 7.0.

### P30-A5. Bonferroni / FDR correction
- **Priority:** P1
- **Effort:** S
- **Expected lift:** validates A1 (no separate lift)
- **Plan:** Apply Benjamini-Hochberg FDR correction across the 1,222 PNs.
  Compute corrected p-values for Enmenanak, Enheduana, top 30.

### P30-A6. Replication on a held-out ePSD2 PN subset
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp (if replicates)
- **Plan:** Split ePSD2 PNs by period: train heuristic on Ur III (older), test
  on Old Babylonian (newer). Verify Enmenanak-class scores generalize.

### P30-A7. Janabiyah-pattern variant tests
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** Test alternative Janabiyah readings (sign 53 vs 60 alternates,
  positions 1/3/6 vs 0/2/5, etc.) — sensitivity analysis on the predicted
  skeleton.

### P30-A8. Phoneme-VALUE permutation null v3 at M77 scale
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** Phase-27 had this at CISI scale (data-starved at p=0.556). Re-run
  on M77's 1,669 inscriptions × 35-entry phoneme map.

---

## Category B. Phoneme map expansion (P0 — biggest source of new info)

Current state: 35 entries in `parpola_phonemes.json`. Target: 100+ entries.

### P30-B1. Mine M77 corpus for sign-position pattern alignments with Tamil-Brahmi
- **Priority:** P0
- **Effort:** L (1-2 weeks)
- **Expected lift:** +3-5 pp
- **Plan:** For each of the 64 distinct M77 signs, compute its
  positional profile (I/M/T) on 1,669 inscriptions; match against Tamil-Brahmi
  syllabic position profiles. Build `M77TamilBrahmiPositionalAligner` atomic
  node. Output candidate sign→phoneme assignments with confidence.
- **Cite:** A.1 (Mahadevan 1977), A.12 (Mahadevan 2003), E.1 (DEDR)

### P30-B2. Add Wells 2015 readings (17 signs)
- **Priority:** P0
- **Effort:** S
- **Expected lift:** +1 pp
- **Plan:** Wells 2015 identifies 17 signs with various confidence including
  Dholavira place-name reading. Acquire Wells 2015 ($16 PDF), extract the
  17 readings, add to phoneme map with `source: "Wells 2015"` and confidence.
- **Cite:** A.7 (Wells 2015)

### P30-B3. Add Mahadevan 2010 "Akam and Puram" address signs
- **Priority:** P0
- **Effort:** S
- **Expected lift:** +1 pp
- **Plan:** Mahadevan 2010 paper identifies signs as 'address' markers. Add
  to phoneme map.
- **Cite:** C.5 (Mahadevan 1970-2018 papers, RMRL)

### P30-B4. Add Mahadevan's 1999 Murukan signs
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Plan:** Mahadevan 1999 "Murukan in the Indus Script" — add specific
  sign-to-Murukan mappings.
- **Cite:** C.5

### P30-B5. Add Mahadevan 2018 Toponyms / Directions / Tribal Names
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Plan:** Mahadevan & Bhaskar 2018 — extract toponym/direction/tribal-name
  signs.
- **Cite:** C.5

### P30-B6. Cross-validate against Mukhopadhyay 2019 sign-context analysis
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** Mukhopadhyay 2019 inferred sign categories statistically. Compare
  with Parpola's phoneme map for consistency.
- **Cite:** D.5

### P30-B7. Build Yajnadevam Sanskrit map as competing hypothesis
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1-2 pp (falsification value)
- **Plan:** Implement Yajnadevam's 76-allograph map as
  `parpola_phonemes_yajnadevam_sanskrit.json` (separate file, same schema).
- **Cite:** C.7

### P30-B8. Build S.R. Rao Sanskrit map as competing hypothesis
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** Same approach for S.R. Rao 1982's 15-20 sign Sanskrit map.
- **Cite:** C.10

### P30-B9. Build Bonta 2010 hypothesis as competing
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.11

### P30-B10. Phoneme-confidence Bayesian re-ranking
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +1 pp
- **Plan:** Bayesian model: P(phoneme | sign) ∝ P(iconographic anchor) ×
  P(positional fit) × P(co-occurrence in compound names).

---

## Category C. Iconographic anchor expansion (P0)

Current state: 12 anchors in `iconographic_anchors.json` (anchor score 27.0).
Target: 25-40 anchors.

### P30-C1. Read Parpola 2010 figs 5-23 + extract additional anchors
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1-2 pp + anchor score increase to ~50
- **Plan:** Phase-27 only used 12 anchors from Parpola 2010 figs 5/6/7/9/14/
  17/19/20/22/23. Read full Parpola 2010 + add ~10 more anchors from figs
  10/11/12/13/15/16/18/21.
- **Cite:** C.2

### P30-C2. Add Parpola 1985 Sky-Garment iconographic anchors
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.4

### P30-C3. Add Parpola 2018 Indus Seals overview anchors
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.4

### P30-C4. Add Mahadevan 1999 Murukan iconographic anchors
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** C.5

### P30-C5. Add Frenez 2018 BMAC seal iconography
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** F.3

### P30-C6. Add Vidale & Frenez 2015 Bactrian seal iconography
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** F.4

### P30-C7. Add Wells 2015 Dholavira reading as anchor
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** A.7

### P30-C8. Re-run AllographAwareIconographicScore at expanded anchor count
- **Priority:** P0
- **Effort:** S
- **Expected lift:** +1 pp
- **Depends on:** C1-C7
- **Plan:** With ~30 anchors instead of 12, expected anchor score 60-70.

---

## Category D. Allograph family expansion (P0)

Current state: 4 families (fish, numerals, intersecting circles, fig tree)
in `mahadevan_parpola_crosswalk.json`. Target: 15-20 families.

### P30-D1. Build Wells 2015 typology integration
- **Priority:** P0
- **Effort:** L
- **Expected lift:** +2 pp
- **Plan:** Wells 2015 has 676 graphemes grouped into ~50 typological classes.
  Cross-cluster Wells classes against Mahadevan/Parpola allographs.
- **Cite:** A.7

### P30-D2. Build Fuls 2023 catalog typology
- **Priority:** P0
- **Effort:** L
- **Expected lift:** +2 pp
- **Plan:** Fuls 2023 ME vol. 4 has ~700 graphemes. Cross-cluster against
  Wells + Mahadevan + Parpola.
- **Cite:** A.10

### P30-D3. Cross-cluster across all 4 systems (Mahadevan/Parpola/Wells/Fuls)
- **Priority:** P0
- **Effort:** L
- **Expected lift:** +2 pp
- **Depends on:** D1, D2
- **Plan:** Build a unified sign-id crosswalk across all 4 numbering systems.
  Build `UnifiedSignCrosswalk` atomic node.

### P30-D4. Add zoomorphic allograph families (lion, eagle, cobra, buffalo, bull)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp
- **Cite:** A.1, C.2, C.5

### P30-D5. Add anthropomorphic allograph families (man-with-arm, goddess, archer)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** A.1, C.2

### P30-D6. Re-run AllographAwareIconographicScore at expanded families
- **Priority:** P0
- **Effort:** S
- **Expected lift:** +1 pp
- **Depends on:** D1-D5

---

## Category E. Falsification rounds (P0)

The framework now produces strong scores. We need to test it against competing
hypotheses to ensure it's not overfitting.

### P30-E1. Yajnadevam Sanskrit map vs Parpola Dravidian map — head-to-head
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +2-3 pp (clean falsification)
- **Plan:** Run IconographicAnchorScore + AllographAwareIconographicScore +
  ReverseJanabiyahSearch on BOTH maps. Compare scores. If Yajnadevam scores
  higher: framework reconsiders Sanskrit. If lower: clean rejection.
- **Cite:** C.7

### P30-E2. S.R. Rao Sanskrit map test
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp
- **Cite:** C.10

### P30-E3. Mahaveer Muhammad Sindhu Prakrit map test
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.8

### P30-E4. Bonta 2010 Munda hypothesis test
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.11

### P30-E5. Florian Neukart 2025 cosmological reading test
- **Priority:** P3
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** C.9

### P30-E6. Farmer/Sproat/Witzel 2004 "non-language" structural test
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp (rebuts central anti-decipherment claim)
- **Plan:** FSW argued Indus has < 100 sign sequences shared across find-spots.
  Run this stat on M77 + CISI corpus. If we find > 100, FSW's claim is empirically
  refuted.
- **Cite:** C.12

### P30-E7. Random-mapping null
- **Priority:** P1
- **Effort:** S
- **Expected lift:** validates significance
- **Plan:** Generate 10,000 random sign→phoneme assignments. Compute anchor
  score distribution. Test where Parpola's score 27.0 sits.

---

## Category F. Corpus expansion (P0 — multiple data sources to acquire)

### P30-F1. Acquire Fuls ME vol. 3 ($45)
- **Priority:** P0
- **Effort:** S (purchase + parse)
- **Expected lift:** +2 pp (3.3× corpus expansion + spatial/temporal metadata)
- **Plan:** Amazon paperback. OCR text → JSON.
- **Cite:** A.9

### P30-F2. Request ICIT API access from Andreas Fuls
- **Priority:** P0
- **Effort:** S (email)
- **Expected lift:** +1-2 pp (live, growing corpus)
- **Plan:** Email andreas.fuls@tu-berlin.de.
- **Cite:** A.11

### P30-F3. Acquire CISI Vol 3.1 (€220)
- **Priority:** P1
- **Effort:** M (purchase + OCR)
- **Expected lift:** +2-3 pp (Mohenjo-daro + Harappa actual catalogue plates)
- **Cite:** A.4

### P30-F4. Acquire CISI Vol 3.2 (€160)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1-2 pp (Kalibangan, Nausharo, Mehrgarh, Rojdi)
- **Cite:** A.5

### P30-F5. Re-attempt Crawford 2001 download (alternative mirrors)
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +1 pp (95 Saar Dilmun seals)
- **Cite:** F.1

### P30-F6. Add Tepe Yahya graffiti (Potts 2022 in CISI 3.3)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** A.6 (Potts 2022)

### P30-F7. Add Konar Sandal LPIW (Linear Proto-Iranian Writing)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** F.4

### P30-F8. Add Linear Elamite (Desset 2020-2022)
- **Priority:** P2
- **Effort:** L
- **Expected lift:** +1 pp (already-deciphered adjacent script)
- **Cite:** G.2

### P30-F9. Add Tamil-Brahmi inscriptions (Mahadevan 2003) as parallel corpus
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +2 pp (the parallel corpus for Dravidian validation)
- **Cite:** A.12

### P30-F10. Add Pallava cave inscriptions (Mahadevan 1971)
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.5

### P30-F11. Add Old Tamil Sangam corpus (DEDR-aligned)
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +2 pp (the Dravidian etymological substrate)
- **Cite:** E.1, E.2

### P30-F12. Add CDLI BDTNS Ur III tablets (5,000+ via ePSD2 import)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp
- **Cite:** B.4

### P30-F13. Add Vandorpe Sukkalmah Susa prosopography
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +2 pp (Susa is THE contact zone)
- **Cite:** B.5

### P30-F14. Add ETCSL royal inscriptions (600+)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp
- **Cite:** B.2

### P30-F15. Add Iravatham Mahadevan Indus Concordance web app data
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** indusscript.in has the live concordance.
- **Cite:** A.1, C.5

---

## Category G. Statistical innovations (P0-P1)

### P30-G1. Joint period × provenience stratification (8 × 5 = 40 cells)
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1-2 pp (already on Phase-29 priority list)
- **Plan:** Phase-25c had 4-bucket period; Phase-26a had 5 prov; combine.
- **Cite:** B.1, A.1, A.2

### P30-G2. Bayesian hierarchical model
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +1 pp
- **Plan:** PN ~ period + provenience + corpus. PyMC3 or Stan.

### P30-G3. Information-theoretic criterion: H1 + H2 + bigram MI on M77
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** D.1

### P30-G4. Length-stratified spectral analysis on M77 (Phase-20 style)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-G5. Repetition collapser on M77 (Phase-21 style)
- **Priority:** P2
- **Effort:** S
- **Expected lift:** +0.5 pp

### P30-G6. Zipf-Mandelbrot fit per-corpus (M77 vs CISI vs Tamil-Brahmi)
- **Priority:** P1
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** D.3

### P30-G7. Power analysis: how many seals do we need?
- **Priority:** P1
- **Effort:** M
- **Expected lift:** roadmap (no direct lift)
- **Plan:** Given current effect sizes, compute n_seals required for p<0.001 on
  the Janabiyah readout.

### P30-G8. Cohen's d effect size for Enmenanak vs random PN
- **Priority:** P1
- **Effort:** S
- **Expected lift:** validates A1

### P30-G9. Cross-validation: M77 train vs Janabiyah test
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1-2 pp
- **Plan:** Build LM on 1,500 of 1,669 M77 inscriptions; predict Janabiyah's
  remaining sign sequence.

### P30-G10. Anisotropy detection (Bhaskar 2024)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** D.8

---

## Category H. Computational decipherment (P0)

### P30-H1. SA-based mapping: M77 → Tamil-Brahmi
- **Priority:** P0
- **Effort:** L
- **Expected lift:** +3-5 pp (the BIG decipherment test)
- **Plan:** SA decipher with M77 corpus → Tamil-Brahmi LM. Phase-30 anchor
  = the 35-entry phoneme map. Use existing `SADecipher` atomic node.
- **Cite:** A.1, A.12, E.1

### P30-H2. Beam search: M77 → Tamil-Brahmi
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1 pp (validation of H1)
- **Cite:** A.1, A.12

### P30-H3. Neural HMM: M77 → Tamil-Brahmi (Knight & Sproat 2009 method)
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +2 pp
- **Cite:** I.1

### P30-H4. CipherConstructor self-test on M77
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +1 pp (validates the framework)
- **Plan:** Cipher M77 with random permutation; verify SA decipher recovers
  the original mapping. Phase-15 framework already exists.

### P30-H5. AnchorConvergenceBenchmark on M77 → Tamil-Brahmi
- **Priority:** P0
- **Effort:** L
- **Expected lift:** +2 pp
- **Plan:** Sweep anchor counts [0, 5, 10, 20, 50, 100]. Existing node.

### P30-H6. AnchorConvergenceBenchmark with word-final priority (Fuls 2026)
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +1 pp
- **Cite:** A.9

### P30-H7. Iterative LLM-in-the-loop hypothesis ranker
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +1 pp
- **Plan:** Mistral generates candidate phoneme assignments; framework scores
  each via existing IconographicAnchorScore + AnchorConvergenceBenchmark;
  retain top-K, mutate, repeat.

### P30-H8. CNN sign embeddings + cross-language alignment
- **Priority:** P2
- **Effort:** L
- **Expected lift:** +1 pp

### P30-H9. Length-conditioned position model
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-H10. Constraint sweep with M77 corpus
- **Priority:** P1
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** Phase-25/26 had ConstraintSweep at CISI scale. Run on M77.

### P30-H11. Coordinated decipherment: many small maps under joint constraint
- **Priority:** P2
- **Effort:** L
- **Expected lift:** +1 pp

---

## Category I. Multimodal AI (P1-P2)

### P30-I1. Florida Tech ASR-net integration
- **Priority:** P0
- **Effort:** M
- **Expected lift:** +2 pp (automatic seal-image → sign sequence)
- **Plan:** Build `IndusGraphemeRecognizer` atomic node using YOLOv3 +
  MobileNet from Dixit et al. 2025.
- **Cite:** D.7

### P30-I2. CISI Vol 1 + 2 OCR via call_llm_vision (after acquiring PDFs)
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +2-3 pp (3,500+ Mohenjo-daro/Harappa inscriptions)
- **Cite:** A.2, A.3

### P30-I3. Fine-tune vision model on Indus seal photos (HARP 22k objects)
- **Priority:** P2
- **Effort:** L
- **Expected lift:** +2 pp
- **Plan:** HARP has 22k inscribed objects. Fine-tune Pixtral or LLaVA on
  the seal-photo → sign sequence task.

### P30-I4. Sign similarity via vision embeddings
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +1 pp
- **Plan:** Compute CLIP embeddings of all 700 signs; cluster automatically;
  compare with Wells 2015 manual classification.
- **Cite:** A.7

### P30-I5. Image-to-sign sequence pipeline (end-to-end)
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +2 pp

### P30-I6. Anomaly detection on sign sequences (autoencoder reconstruction error)
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp

---

## Category J. Cross-civilizational anchors (P1-P2)

### P30-J1. Linear Elamite (Desset 2020-2022) parallel decipherment as anchor
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +1-2 pp
- **Plan:** Linear Elamite was deciphered by Desset 2020 using contact-zone
  Akkadian anchors. Apply the same methodology to Indus.
- **Cite:** G.2

### P30-J2. Proto-Elamite (4th millennium) precursor structural similarities
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-J3. BMAC/Bactrian-Margiana corpus integration
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** F.3, G.1

### P30-J4. Akkadian → Indus loanword candidates
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Plan:** "tamkārum" (Akkadian merchant) → Indus seal IDs?

### P30-J5. Sumerian → Indus loanword candidates
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-J6. Old Tamil Sangam → Indus name comparison
- **Priority:** P1
- **Effort:** L
- **Expected lift:** +1 pp
- **Cite:** E.1

### P30-J7. Vedic Sanskrit substrate words (Witzel 2003)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-J8. Munda comparative (Bonta 2010 hypothesis)
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** C.11

---

## Category K. Genetics / archaeology (P2-P3)

### P30-K1. Narasimhan 2019 ancient DNA cluster as prior
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +1 pp (strengthens Dravidian prior)
- **Plan:** Document the genetic evidence supporting the Dravidian-language
  hypothesis as the prior in our Bayesian model.
- **Cite:** H.1

### P30-K2. Y-chromosome haplogroup vs Indus seal find-spots
- **Priority:** P3
- **Effort:** M
- **Expected lift:** +0.5 pp

### P30-K3. Cross-reference with Reich 2018 study
- **Priority:** P3
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** H.2

### P30-K4. Add Shinde 2019 Rakhigarhi aDNA result
- **Priority:** P2
- **Effort:** S
- **Expected lift:** +0.5 pp
- **Cite:** H.3

### P30-K5. Archaeological context for Janabiyah (Dilmun period)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** F.6

### P30-K6. Find-spot stratigraphy refinement (Konasukawa 2020)
- **Priority:** P2
- **Effort:** M
- **Expected lift:** +0.5 pp
- **Cite:** D.10

---

## Category L. External engagement (P0-P1)

### P30-L1. Submit to Tamil Nadu $1M prize panel (Roja Muthiah Library / IRC)
- **Priority:** P0
- **Effort:** L (full submission packet)
- **Expected lift:** validates externally + funding
- **Plan:** Phase-29 framework + Phase-30 statistical validation = potentially
  prize-eligible. Email Roja Muthiah Research Library and Indus Research Centre.
- **Cite:** E.5, C.5

### P30-L2. Email Asko Parpola (Helsinki) with Phase-29 findings
- **Priority:** P0
- **Effort:** S
- **Expected lift:** scholarly engagement (not progress, but validation)
- **Plan:** Forward Phase-29 synthesis + Enmenanak/Enheduana finding to
  asko.parpola@helsinki.fi.
- **Cite:** C.1, C.2

### P30-L3. Email Andreas Fuls (TU Berlin) re ICIT API + Phase-29 cross-check
- **Priority:** P0
- **Effort:** S
- **Expected lift:** API access + collaboration
- **Cite:** A.9, A.11

### P30-L4. Email Steffen Laursen (Moesgaard) re Janabiyah seal data
- **Priority:** P1
- **Effort:** S
- **Expected lift:** new seal data + collaboration
- **Cite:** F.2

### P30-L5. Email R. Balakrishnan (IRC) re Mahadevan endowment chair work
- **Priority:** P1
- **Effort:** S
- **Cite:** E.3, C.5

### P30-L6. Submit to JCAA (Journal of Computer Applications in Archaeology)
- **Priority:** P1
- **Effort:** L (paper-writing)
- **Expected lift:** publication
- **Cite:** D.7

### P30-L7. Submit to Studia Orientalia Electronica
- **Priority:** P1
- **Effort:** L
- **Cite:** D.11

### P30-L8. Submit to Journal of the American Oriental Society
- **Priority:** P2
- **Effort:** L

### P30-L9. arXiv preprint of Phase-29 Enmenanak/Enheduana finding
- **Priority:** P0
- **Effort:** M
- **Expected lift:** community feedback

### P30-L10. Open-issue tracker for the framework on GitHub
- **Priority:** P1
- **Effort:** S

### P30-L11. Email Bahata Mukhopadhyay (Palgrave Comm. 2019) with cross-check
- **Priority:** P2
- **Effort:** S
- **Cite:** D.5

### P30-L12. Email Yajnadevam re falsification round
- **Priority:** P2
- **Effort:** S
- **Cite:** C.7

### P30-L13. Email Florian Neukart (Leiden) re competing computational map
- **Priority:** P3
- **Effort:** S
- **Cite:** C.9

### P30-L14. Engage with Indus Research Centre's web concordance (indusscript.in)
- **Priority:** P1
- **Effort:** M
- **Cite:** C.5

---

## Category M. Reproducibility / sharing (P1-P2)

### P30-M1. GitHub Pages site
- **Priority:** P1
- **Effort:** M
- **Plan:** Auto-generate from existing `reports/*.md` + atomic-node graph viz.

### P30-M2. Containerize via Docker
- **Priority:** P2
- **Effort:** M

### P30-M3. Reproducibility checklist (every Phase-N has machine-runnable
recipe)
- **Priority:** P1
- **Effort:** M

### P30-M4. Open Phase-29 graphs to WebUI Experiment Builder
- **Priority:** P2
- **Effort:** M

### P30-M5. Export findings to CDLI metadata format (P/Q/X numbers)
- **Priority:** P3
- **Effort:** M
- **Cite:** B.3

### P30-M6. Build interactive Plotly dashboard of Phase-22..29 results
- **Priority:** P2
- **Effort:** L

### P30-M7. Public dataset release via Zenodo (DOI'd, citeable)
- **Priority:** P1
- **Effort:** M

### P30-M8. JOSS / softwareX paper on the framework
- **Priority:** P2
- **Effort:** L

### P30-M9. SKILL.md for repository workflow
- **Priority:** P3
- **Effort:** S

---

## Category N. Documentation / reporting (P1)

### P30-N1. Phase-30 PDF report
- **Priority:** P0 (after all P30 tasks done)
- **Effort:** M

### P30-N2. Decipherment Progress Notebook (combined Phase-22..30 narrative)
- **Priority:** P1
- **Effort:** L

### P30-N3. Frontend tour walkthrough document
- **Priority:** P2
- **Effort:** M

### P30-N4. Methodology paper (the framework + atomic-node architecture)
- **Priority:** P1
- **Effort:** L

### P30-N5. CITATIONS.md kept current
- **Priority:** P0 (ongoing)
- **Effort:** S per phase

### P30-N6. Per-experiment publication-quality figures (Phase-29d top candidates,
Phase-29e corpus stats, Phase-28c anchor table)
- **Priority:** P1
- **Effort:** M

---

## Category O. NEW data sources to investigate (P2-P3)

### P30-O1. ICIPS digital catalogue (if accessible)
- **Priority:** P2
- **Effort:** M

### P30-O2. Iravatham Mahadevan Indus Concordance v2 (web app at indusscript.in)
- **Priority:** P2
- **Effort:** M
- **Cite:** C.5

### P30-O3. Helsinki research portal — all Parpola PDFs
- **Priority:** P2
- **Effort:** M
- **Cite:** C.1, C.2, C.4

### P30-O4. Holdat LLC GitHub: Indus structural analysis (constraint-based)
- **Priority:** P3
- **Effort:** S
- **Plan:** Recent (2025) GitHub repo with corrected co-occurrence metrics on
  1,670 seal sequences. Cross-validate.

### P30-O5. Bryant et al. 2023 — Indus craniofacial + cultural reconstruction
- **Priority:** P3
- **Effort:** M

### P30-O6. Holdat LLC's 4-gate constraint analysis of Indus
- **Priority:** P3
- **Effort:** S

---

## Category P. Engineering / framework (P1-P2)

### P30-P1. Make ReverseJanabiyah tests parametric (skeleton from any seal)
- **Priority:** P1
- **Effort:** M

### P30-P2. Generalize phoneme map to sets of competing maps
- **Priority:** P0
- **Effort:** M
- **Plan:** Currently we have one parpola_phonemes.json. Extend to
  list-of-maps, with framework comparing all maps simultaneously.

### P30-P3. Add caching/memoization for slow stats
- **Priority:** P2
- **Effort:** S

### P30-P4. Add MCMC sampler atomic node (replaces simple permutation)
- **Priority:** P2
- **Effort:** L

### P30-P5. GPU acceleration for SA decipher on M77 (CuPy already available)
- **Priority:** P1
- **Effort:** M

### P30-P6. Async corpus loading (so all corpora load in parallel)
- **Priority:** P3
- **Effort:** S

---

## Estimated Phase-30 trajectory

If we run **P30-A1, A2, A3, B1, B2, C1, D1, D2, E1, F1, F2, F9, F13, G1, G9,
H1, H2, H4, I1, L1, L2, L3, L9** (the P0 tasks), expected lift:

| Component | Phase-29 | Phase-30 P0 done |
|-----------|----------|------------------|
| Phoneme map | 35 entries | **80-100 entries** |
| Iconographic anchors | 12 | **25-30** |
| Anchor score | 27.0 | **60-75** (vs allograph-only 27→60) |
| Allograph families | 4 | **15+** |
| Inscriptions | 1,669 | **6,000+ (+ Fuls + Tamil-Brahmi)** |
| PNs | 1,222 | **2,500+ (+ Vandorpe + ETCSL)** |
| Validated Janabiyah candidates | 102 (uncorrected) | **~10 (corrected for null + period + Meluhha)** |
| Decipherment progress | ~12-15% | **~25-35%** |

If P0 + P1 tasks all complete: ~35-45% decipherment.

If P0 + P1 + P2 tasks all complete (months of work): ~45-55%.

The remaining ~50%+ is the hard part — the actual unattested compound-name
identifications + bilingual cross-checks. That requires either (a) finding a
real Indus-Akkadian bilingual on a contact-zone seal, or (b) a critical mass
of independent statistical anchors that converges with the proposed phoneme
map.

---

## Risk / failure modes

1. **Enmenanak/Enheduana don't survive A1-A3 correction.** Then Phase-30 falls
   back to corpus expansion + re-analysis; net lift +1-2 pp.
2. **Yajnadevam's Sanskrit hypothesis scores higher than Parpola's.** Then we
   need to seriously consider Indo-European Indus.
3. **No bilingual seal ever found.** Then absolute decipherment plateaus at
   ~40-50% (the Janabiyah-skeleton + iconographic anchor ceiling).
4. **CISI Vol 3.1 acquisition fails.** Phase-30 caps at ~25-30% (corpus
   limit).
5. **Tamil Nadu prize panel finds the framework insufficient.** Doesn't cap
   progress, but reduces external-pressure forcing-function value.

---

*Phase-30 task list maintained as part of the Glossa-Lab Indus decipherment
pipeline. Source citations per `CITATIONS.md`. Last updated: 2026-04-30.*
