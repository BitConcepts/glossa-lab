# Scholar Outreach Drafts — Phase-131+

Generated: May 2026  
Purpose: Secure peer review for Phase-124 fish-sign polysemy results and preprint validation.

---

## Target 1: Nisha Yadav / TIFR (Mumbai)

Nisha Yadav (Tata Institute of Fundamental Research) is co-author of the quantitative
Indus script analyses (Yadav et al. 2008, 2010) that established the conditional entropy
framework. She is likely the most technically compatible reviewer for our distributional
methodology.

### Draft Email

Subject: Computational Indus Script Decipherment — Request for Review / Correspondence

Dear Dr. Yadav,

I am writing to share results from an independent computational decipherment of the 
Indus Valley Script and to request your assessment of a specific finding that your
prior work (Yadav et al. 2008, 2010) has bearing on.

Working from the Holdat LLC corpus (1,670 seals, 9 sites), I have built a systematic
five-layer evidence framework that achieves 268 sign anchors at HIGH or MEDIUM confidence,
covering 96.2% of corpus tokens. The methodology builds directly on your conditional
entropy framework and Mahadevan's M-number system.

The specific finding I would value your input on concerns the fish-sign polysemy
hypothesis proposed by Avishai Roif (Ben Gurion, 2025): that isolated fish signs
encode commodity units while compound fish signs encode occupational titles.

Our test across all 9 sites — including Lothal, the IVC's coastal port — finds 
0/113 fish-sign seals isolated (all compound, site-invariant). We also tested whether
M267 (frequency=400) is the fish sign; it is not — it's a genitive particle distributed 
uniformly across all motif types.

I would be grateful for:
1. Your assessment of our distributional methodology for the fish-sign result
2. Any access to CISI data that includes tablet/tag inscriptions (beyond formal seals)
3. Feedback on the grammar model ([CLASSIFIER]–[TITLE]–[SUFFIX]) before preprint submission

All data, scripts, and anchor tables are openly available.

With respect,
Tristan [Last name]
Glossa-Lab

---

## Target 2: Asko Parpola (University of Helsinki)

Parpola (1994, 2010) is the field's foremost authority and the architect of the 
Dravidian rebus framework we build upon. He is retired but still active in correspondence.
A review from Parpola would be the gold standard for the preprint.

### Draft Email

Subject: Building on Deciphering the Indus Script — 268-Anchor Computational Update

Dear Professor Parpola,

Your work in *Deciphering the Indus Script* (1994) and the subsequent 2010 article
provides the foundational framework for the system I am writing to share with you.

I have built a computational implementation of the Dravidian rebus decipherment
that achieves 268 sign anchors at HIGH or MEDIUM confidence (96.2% token coverage,
1,670-seal corpus). Every HIGH-confidence anchor is traceable to DEDR entries you
identified; the MEDIUM anchors extend your framework using positional statistics and
syllabic language model simulation.

Three findings I believe would interest you:

1. M267 ≠ fish: The sign at frequency=400 distributed across all motif types is not 
   the fish sign. M047 (P47 in your concordance, frequency=13) is the actual fish sign.
   This corrects a widespread misassignment in computational literature.

2. Munda substrate in the sign corpus: Two signs (M374=kul, M351=vī) show Munda/Austroasiatic
   substrate readings (kul=clan/lineage, vī=seed), consistent with Witzel's (1999) substrate
   hypothesis. These are the first corpus-level quantitative identification of Munda substrate
   signs in the IVS.

3. Fish-sign polysemy (0/113 isolated): Site-invariant result across all 9 sites, including
   Lothal. Consistent with your reading of fish+numeral compounds as administrative titles.

I have prepared a preprint and would be honored to receive any correspondence. The full
anchor table with DEDR citations is available on request.

With deep respect for your life's work,
Tristan [Last name]
Glossa-Lab

---

## Target 3: Rajesh P.N. Rao (University of Washington)

Rao led the 2009 PNAS paper demonstrating IVS linguistic entropy. His group would be
the natural venue for quantitative validation of our distributional results.

### Draft Email

Subject: Extending Your 2009 PNAS Markov Model — 268-Anchor Decipherment Results

Dear Professor Rao,

Your 2009 PNAS paper on the Markov model of the Indus Script provided the entropy
validation that underpins quantitative IVS research. I am writing to share results
that extend your framework to a full distributional decipherment.

Working from the Holdat LLC corpus (7,002 tokens, 1,670 seals), I have applied
positional analysis, bigram collocational analysis, and syllabic language model
simulation to achieve 268 sign anchors at MEDIUM+ confidence (96.2% token coverage).

Key results relevant to your work:

1. The grammar model [ANIMAL_CLASSIFIER]–[GUILD_TITLE]–[PERSONAL_NAME_SUFFIX] is
   derivable from positional statistics alone — consistent with your entropy findings
   (short inscriptions with high conditional entropy given position).

2. 0/113 fish-sign seals are isolated across 9 sites — the fish sign is exclusively
   compound, supporting an occupational-title reading over a commodity-tally model.

3. The 20 irresolvable signs (freq 5-7, MEDIAL position) show the entropy floor:
   personal name syllables that are informationally irreducible without more data.

I would welcome the opportunity to discuss these findings and receive your assessment
of the methodology before preprint submission.

Best regards,
Tristan [Last name]
Glossa-Lab

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
