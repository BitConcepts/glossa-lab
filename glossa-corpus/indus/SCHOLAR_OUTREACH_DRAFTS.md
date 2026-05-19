# Scholar Outreach Drafts — Phase-141 (Updated)

Generated: May 2026 — Updated with Phase-134/135/136-140 falsification + structural results  
Purpose: Secure peer review before preprint submission. Emails updated with new quantitative results.

---

## Target 1: Nisha Yadav / TIFR (Mumbai)

Nisha Yadav (Tata Institute of Fundamental Research) is co-author of the quantitative
Indus script analyses (Yadav et al. 2008, 2010) that established the conditional entropy
framework. She is likely the most technically compatible reviewer for our distributional
methodology. Also likely to have access to the full CISI dataset.

### Draft Email (Updated Phase-141)

```
To: nisha.yadav@tifr.res.in
Subject: Computational Indus Script study — requesting CISI data access and methodological review

Dear Dr. Yadav,

I am writing to you as the lead computational linguist on Yadav et al. (2008, 2010),
which established the entropy framework that underpins quantitative IVS research.

I have been conducting a systematic distributional decipherment study using the Holdat
LLC corpus (1,670 seals, 7,002 tokens, 9 sites) and would greatly value your review of
the methodology and findings before submitting a preprint to arXiv.

Key results I would like your assessment of:

1. PERMUTATION NULL TEST (new): 2,000 shuffled-corpus permutations show the real corpus
   grammar model R² = 0.992 vs shuffled mean 0.438 (z = 10.3, p ≈ 0, N = 2,000).
   A blind 80/20 site split confirms the model generalises: 97.7% sign-class prediction
   accuracy on held-out seals. I believe this is the strongest published evidence for
   non-random positional structure in the script.

2. DRAVIDIAN LANGUAGE IDENTIFICATION: At 157 H+M anchor signs, 88% of readings are
   better explained by a Sangam Tamil syllabic LM than Sanskrit (Δ mean log-P = +4.1).
   Bigram conditional entropy H(X₂|X₁)/H(X₁) = 0.611, within the natural-language
   range (0.5–0.8; random ≥ 0.95).

3. ZIPF CONTROL FINDING: Indus Zipf exponent α = 1.28 is intermediate between Semitic
   short-inscription corpora (Hebrew α ≈ 1.01, NW Semitic α ≈ 0.96) and Sangam Tamil
   (α ≈ 1.63). This pattern may be diagnostic for Dravidian-family administrative corpora.

4. DATA REQUEST: Our F9 test (single-sign seal terminal-dominance census) is blocked
   because the Holdat corpus is pre-filtered. The raw CISI Vol.1–3 dataset retains
   single-sign seals. Would you be able to facilitate access through TIFR or the ASI?

All code (GitHub: glossa-lab), data, and anchor tables with DEDR citations are available.
I am not seeking co-authorship — only honest critical review before public submission.

With respect,
Tristen Kyle Pierson
Glossa Lab / BitConcepts LLC
tpierson@bitconcepts.tech
```

---

## Target 2: Asko Parpola (University of Helsinki)

Parpola (1994, 2010) is the field's foremost authority and the architect of the
Dravidian rebus framework we build upon. He is retired but still active in correspondence.
A review from Parpola would be the gold standard for the preprint.

### Draft Email (Updated Phase-141)

```
To: aparpola@gmail.com
Subject: Computational re-examination of Dravidian Indus decipherment - requesting methodological review

NOTE: asko.parpola@helsinki.fi bounced (account deactivated after retirement).
Correct address confirmed from INDOLOGY mailing list (2017): aparpola@gmail.com

Dear Professor Parpola,

Your five decades of work on the Indus script, and particularly your 2010 Coimbatore
lecture on the Dravidian solution, have been foundational to the framework I am testing
computationally.

I have completed 141 phases of systematic distributional analysis using the Holdat LLC
corpus (1,670 seals, 7,002 tokens) and would like to bring specific findings to your
attention before submitting a preprint to arXiv (cs.CL).

1. YOUR ICONOGRAPHIC ANCHORS VALIDATED: Your 7 iconographic anchor signs (fish = mīn,
   unicorn sign = ai, genitive particle, etc.) were used as the HIGH-confidence seed set.
   A blind held-out test shows the grammar model built from these anchors predicts sign
   classes on unseen seals with 97.7% accuracy (Pearson r = 0.994 between training and
   held-out positional rates). This strongly confirms that the anchors encode real
   phonological values rather than arbitrary assignments.

2. M267 CORRECTION: We confirmed in Phase-45/70 that M267 (frequency = 400) is a
   genitive particle, not a fish sign. M047 (P47 in your concordance, frequency = 13)
   is the actual fish sign. This corrects a widespread misassignment.

3. ZIPF FINDING: Indus Zipf exponent α = 1.28 falls between Semitic corpora (~1.0) and
   Sangam Tamil (~1.63). This pattern may be distinctive of Dravidian-family short-text
   administrative corpora — potentially a diagnostic for language identification.

4. REQUEST — SHU-ILISHU SEAL: The Shu-ilishu interpreter seal (Ur III, c.2020 BCE) is
   the single best archaeologically-grounded external anchor. Our phonological decomposition
   of "Shu-i-li-shu" reaches 50% coverage with current H+M readings. Do you have any
   unpublished analysis of this seal's inscription sequence that might constrain the
   remaining phonemes?

All data and code are openly available. I am not seeking co-authorship.

With deep respect for your scholarship,
Tristen Kyle Pierson
Glossa Lab / BitConcepts LLC
tpierson@bitconcepts.tech
```

---

## Target 3: Rajesh P.N. Rao (University of Washington)

Rao led the 2009 Science paper demonstrating IVS linguistic entropy. His group would be
the natural venue for quantitative validation of our distributional results and the ideal
arXiv endorser (cs.CL).

### Draft Email (Updated Phase-141)

```
To: rao@cs.washington.edu
Subject: Follow-up to Rao et al. 2009 Science — permutation null and conditional entropy results

Dear Professor Rao,

Your 2009 Science paper establishing that the Indus script's conditional entropy profile
is consistent with a structured language system has been a foundational anchor point.
I am writing to share methodological extensions that may interest you.

1. PERMUTATION NULL EXTENSION: Rather than comparing globally to natural languages and
   random controls, we ran 2,000 within-corpus sign permutations. The real corpus R² = 0.992
   vs null mean 0.438 (z = 10.3, p ≈ 0). This is a within-corpus confirmation that the
   structure you identified is not an artefact of corpus size or symbol frequency distribution.

2. BIGRAM CONDITIONAL ENTROPY REPLICATION: H(X₂|X₁)/H(X₁) = 0.611 in the Holdat corpus,
   confirming your finding (NL range 0.5–0.8; randomly shuffled versions yield ≥ 0.95).

3. ZIPF CONTROL COMPARISON: Indus Zipf exponent α = 1.28 is between Semitic short-inscription
   corpora (Hebrew α ≈ 1.01) and Sangam Tamil (α ≈ 1.63). This matches a prediction that if
   the script encodes a Dravidian-family language, its frequency structure should differ
   measurably from alphabetic corpora.

4. LANGUAGE MODEL RESULT: At 157 H+M anchor signs, 88% of readings are better explained by
   a Sangam Tamil syllabic LM than Sanskrit (Δ mean log-P = +4.1). This is a direct extension
   of your entropy-based language identification methodology.

I have prepared a preprint and would be grateful for:
(a) Your assessment of whether the within-corpus permutation methodology is statistically sound
(b) Whether you see circularity concerns in comparing grammar model R² to a within-corpus null
(c) If appropriate, an arXiv cs.CL endorsement

The full data, code, and phase reports are openly available at request.

With thanks for your foundational work,
Tristen Kyle Pierson
Glossa Lab / BitConcepts LLC
tpierson@bitconcepts.tech
```

---

## Wells Catalog Research Plan

**Richard Wells** published *The Archaeology and Epigraphy of Indus Writing* (2011,
Archaeopress, Oxford). This catalog is critical for our next validation step because:

1. It includes Indus-script seals found OUTSIDE South Asia — at Ur, Bahrain (Dilmun),
   Susa, and other Gulf trade sites. These are the seals needed to test the fish-sign
   polysemy hypothesis in a genuine maritime-trade context.

2. Wells uses a W-number sign system (different from Mahadevan M-numbers). A Wells↔
   Mahadevan crosswalk for Gulf-deposit seals would allow us to identify which M-number
   signs appear on Gulf-context Indus seals.

### Acquisition Plan

- Primary: Request through Inter-Library Loan (ILL) at a university library
  (Archaeopress publications are often available through institutional access)
- Secondary: ResearchGate — Wells has an active profile; request PDF directly
- Alternative: British Library or SOAS (School of Oriental and African Studies,
  London) physical copy

### Once Acquired

1. Extract all seal entries tagged with Gulf/Mesopotamian find contexts
   (sites: Ur, Tell Asmar, Susa, Bahrain, Qatar, Failaka)
2. Build Wells-number → M-number crosswalk for these specific seals
3. Check fish-sign (W-equivalent of M047) for isolated vs. compound in Gulf seals
4. If ANY isolated fish signs found at Gulf trade sites: update polysemy hypothesis to
   TESTABLE with positive preliminary evidence
5. Report in Phase-132 or supplementary data to preprint

### Expected yield

Known Indus seals from Gulf contexts: ~20-50 seals (small sample).
Probability of finding isolated fish among these: LOW based on mainland pattern,
but Gulf seals were trade-context objects that may have served different functions
than formal administrative seals.

---

## arXiv Submission Checklist

Target category: **cs.CL** (Computation and Language) with cross-listing to
**eess.SP** (Signal Processing) or **q-bio.QM** (Quantitative Methods)

Alternative venue: **SSRN** (Social Science Research Network) — linguistics/archaeology
preprints are widely accepted here.

Submission requirements for arXiv:
- Institutional affiliation or endorsement (need endorser in cs.CL)
- LaTeX source preferred (convert PREPRINT_DRAFT_v1.md → LaTeX)
- Data availability statement ✓ (included in §6)
- No figures required for initial submission (tables sufficient)

Steps:
1. Convert Markdown → LaTeX using pandoc
2. Add abstract to arXiv metadata
3. Request endorsement from a cs.CL author (Rao group is ideal)
4. Submit to arXiv; simultaneously post to Academia.edu and ResearchGate

---

*End of Scholar Outreach Drafts*
