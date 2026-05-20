# A Reproducible Computational Grammar and Candidate Proto-Dravidian Anchor Model for the Indus Valley Script

**Tristen Kyle Pierson**  
Glossa-Lab / BitConcepts LLC  
Correspondence: tpierson@bitconcepts.tech  
Date: May 2026  
Version: Preprint v2 — Not peer-reviewed

---

## Abstract

The Indus Valley Script (IVS, ca. 2600–1900 BCE) remains officially undeciphered owing to the absence of a bilingual text, short median inscription length (~4–5 signs), and a limited corpus of approximately 7,002 tokens. We present a reproducible computational study of the Holdat LLC Indus Corpus V3 (1,670 seals, 9 sites, 390 distinct signs) that applies positional analysis, bigram/trigram collocational methods, DEDR (Dravidian Etymological Dictionary) rebus matching, and syllabic language-model simulation to construct a candidate anchor model for IVS sign readings. We find robust non-random positional structure (permutation null z = 10.3, p < 0.001; held-out accuracy 97.7%) and a recurring three-slot inscription formula consistent with a Proto-Dravidian administrative vocabulary framework; 161 signs are assigned HIGH or MEDIUM candidate readings (90.96% token coverage, 69.8% of seals consisting entirely of candidate-covered signs), and the proposed readings show 59% overlap with independently published Dravidian assignments in Parpola (1994). The corpus shows no isolated fish signs across all 9 sites or in the Gulf deposit catalog (0/113), corroborating an occupational rather than commodity reading for that sign family. We also correct a prior sign-counting error: an earlier inflated count of 268 H+M signs included 107 heuristic placeholder assignments that do not meet the stated evidence criteria; the genuine count is 161. Coverage figures measure candidate-model assignment, not verified phonetic transcription. The present study does not claim epigraphic finality in the absence of a bilingual inscription; it proposes a reproducible, falsifiable computational model whose structural predictions and candidate phonetic readings can be tested against larger corpora and future discoveries.

---

## 1. Introduction

### 1.1 The Indus Valley Script Problem

The Indus Valley Civilization (IVC, ca. 2600–1900 BCE) produced approximately 5,000 inscribed objects bearing a script of approximately 400 distinct signs. Despite a century of scholarship, the script remains officially undeciphered. Primary obstacles are: (1) the absence of a bilingual text; (2) uncertainty about the underlying language; (3) short average inscription length (~4–5 signs); (4) limited corpus size relative to modern decipherment corpora. Competing hypotheses have proposed proto-Dravidian (Parpola 1994; Mahadevan 1977), proto-Munda (Witzel 1999), an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected), and a non-linguistic semasiographic system (Farmer, Sproat & Witzel 2004). The Dravidian hypothesis has the strongest prior support from geographical distribution of Dravidian languages and archaeological continuity.

### 1.2 Prior Computational Work

Rao et al. (2009) demonstrated IVS conditional entropy is consistent with a linguistic system. Mahadevan (1977) produced the definitive sign concordance. Parpola (1994, 2010) assembled the most comprehensive Dravidian rebus framework. Wells (2011) produced an independent sign list. Nair (2026, preprint) independently confirms non-random structural properties on the ICIT corpus. No prior published work provides a fully open, versioned, reproducible anchor table with explicit confidence criteria.

### 1.3 This Work

We present a computational grammar and candidate anchor model (Glossa-Lab, Phases 1–170) that:

1. Defines a tiered confidence hierarchy (HIGH/MEDIUM/PROVISIONAL_MEDIUM/LOW) with stated necessary and sufficient criteria
2. Proposes 161 candidate readings at MEDIUM or HIGH confidence (90.96% token coverage; note: coverage = anchor-model assignment, not verified phonetic reading)
3. Identifies a recurring three-slot positional formula [CLASSIFIER]–[TITLE]–[SUFFIX] across 97 formula types
4. Tests and rejects the hypothesis that the fish sign (M047) appears in isolated contexts at any of the 9 corpus sites
5. Corrects an earlier misassignment: M267 is not the fish sign; it is a high-frequency functional sign with a MEDIUM-confidence genitive-particle reading
6. Reports explicit failure conditions and adversarial test designs
7. Makes all code, phase reports, and the anchor table openly available for inspection and replication

We do not claim that the script is deciphered. The proposed readings are candidate assignments that require external validation, preferably via the ICIT corpus (Dr. Andreas Fuls, 5,318 inscriptions) or a bilingual find.

---

## 2. Data and Methods

### 2.1 Corpus and Encoding

**Corpus:** Holdat LLC Indus Corpus V3 (Miller 2025). 7,002 sign tokens, 1,670 seals, 9 sites.  
**Encoding:** Mahadevan M-numbers (M001–M416); 390 distinct signs in corpus.  
**Inclusion criteria:** Formal stamp seals only; all single-sign seals retained; no a priori exclusion by site or motif.  
**Exclusion criteria:** Copper tablets, potsherd graffiti, and Dholavira signboard excluded from primary analysis (different medium-type; these are noted as requiring separate treatment).  
**Sign normalization:** M-numbers as assigned by Miller (2025) following Mahadevan (1977). A 45-entry Mahadevan↔Parpola crosswalk (mahadevan_parpola_crosswalk.json) is used for iconographic anchor validation.

**Table 1: Corpus Summary**

| Site | Seals | Tokens | Distinct Signs | Mean Length |
|---|---:|---:|---:|---:|
| Mohenjo-daro | 606 | 2,720 | 285 | 4.5 |
| Harappa | 492 | 2,156 | 250 | 4.4 |
| Kalibangan | 110 | 502 | 132 | 4.6 |
| Dholavira | 106 | 498 | 143 | 4.7 |
| Lothal | 124 | 543 | 148 | 4.4 |
| Chanhu-daro | 78 | 337 | 115 | 4.3 |
| Surkotada | 61 | 255 | 96 | 4.2 |
| Banawali | 60 | 241 | 103 | 4.0 |
| Rakhigarhi | 33 | 150 | 76 | 4.5 |
| **Total** | **1,670** | **7,002** | **390** | **4.4** |

### 2.2 Positional Classification

For each sign, we compute the fraction of tokens appearing in each positional class across multi-sign inscriptions:

- **INITIAL**: position 1 in an inscription of length ≥ 2
- **MEDIAL**: position 2 through (n−1) in an inscription of length ≥ 3
- **TERMINAL**: final position in an inscription of length ≥ 2
- **SOLO**: sole sign in a 1-sign inscription (excluded from positional class assignment; treated as a distinct category)

Positional class thresholds (following Fuls 2013 NWSP method):
- TERMINAL: terminal rate ≥ 0.60
- INITIAL: initial rate ≥ 0.50
- MEDIAL: medial rate ≥ 0.65
- MIXED: does not meet any threshold

**Handling single-sign inscriptions:** Solo signs are excluded from the INITIAL/MEDIAL/TERMINAL computation but retained in frequency counts. Signs with fewer than 3 corpus tokens are not assigned a positional class.

### 2.3 Confidence Assignment

Each sign is assigned to exactly one category. Required and sufficient criteria:

**HIGH (75 signs):** At least two independent evidence types both supporting the same reading. Accepted independent evidence types:
1. Iconographic match: sign shape unambiguously depicts an object whose known Dravidian name yields the reading by the rebus principle; confirmed via published iconographic catalogs (Parpola 1994; Parpola 2010)
2. Distributional exclusivity: sign appears on ≥ 95% of tokens of exactly one seal motif type with lift ratio > 5.0 (measured across Holdat corpus)
3. Terminal marker: sign appears as terminal in > 95% of contexts; reading matches an attested Dravidian case suffix in DEDR
4. Grammar test convergence: SA-consistency ≥ 0.50 across ≥ 5 seeds, with reading matching a DEDR entry that satisfies phonotactic constraints (Krishnamurti 2003)

**MEDIUM (86 signs):** At least one strong evidence type with no contradicting evidence. Accepted evidence:
1. DEDR rebus match: reading attested in DEDR with an acceptable sound correspondence + SA-consistency ≥ 0.15 from syllabic language model + positional profile consistent with the morpheme class claimed for the reading
2. Grammar class positional profile: strong INITIAL or TERMINAL profile consistent with a known morpheme class, with collocation evidence supporting the morpheme interpretation
3. Cross-source confirmation: reading appears in ≥ 2 independent published Dravidian analyses (Parpola 1994; Mahadevan papers) with consistent phonetic assignment

**PROVISIONAL_MEDIUM (4 signs — M330, M165, M202, M198):** Satisfies MEDIUM criteria but has not been independently reviewed by a field expert. These signs are not included in the primary 161 count for coverage calculations where a sharp boundary is needed. They are listed separately. Expert review is explicitly requested.

**LOW (236 signs):** Heuristic or distributional assignment only; does not meet MEDIUM criteria. **Not counted toward coverage. Not used in "fully covered" seal calculations.**

**UNRESOLVED / RETIRED:** No current assignments in this category; sign M267 was previously misassigned as fish/mīn (RETIRED reading) and reassigned as MEDIUM genitive particle iN/in.

### 2.4 Rebus and DEDR Matching

DEDR matching is not unconstrained. The following rules apply:

**Accepted sound correspondences:**
- Proto-Dravidian alveolar trill (ṟ) may correspond to Tamil r
- Proto-Dravidian lateral (ḷ, ḻ) may correspond to Tamil l/ḷ
- Proto-Dravidian nasal (ṇ, ṉ) may correspond to Tamil n/ṇ
- Standard Dravidian vowel-length alternations (a/ā, i/ī, u/ū) are accepted
- No consonant cluster simplifications accepted without specific attestation

**Forbidden:**
- Post-hoc selection: if a reading is proposed, the number of competing DEDR roots fitting the phonological constraints must be reported
- Readings that require consonant substitution (e.g., replacing p with b) without Proto-Dravidian attestation are disallowed
- Semantic stretch without DEDR attestation is disallowed (e.g., "fish sign could mean water" without a DEDR water root matching the phonology)

**Candidate counting:** For HIGH anchor readings, the complete DEDR search results (number of competing roots considered) are available in `backend/reports/INDUS_FINAL_ANCHORS.json` under the `basis` field. Ties are resolved by selecting the reading that best satisfies all three of: positional class match, SA-consistency, and cross-source attestation.

### 2.5 Null Models

The following null models are used. Each is defined precisely so that external groups can replicate them:

- **Within-seal shuffle:** For each seal, the sign sequence is permuted uniformly at random. Positional profiles, bigram statistics, and grammar model fits are recomputed. Comparison: if model R² under shuffle matches real R², the model reflects frequency not sequence structure.
- **Motif-conditioned shuffle:** Permutations are performed within groups of seals sharing the same motif type. Tests whether positional structure is entirely explained by motif-specific sign sets.
- **Site-conditioned shuffle:** Permutations within site-specific sign inventories. Tests pan-Harappan grammar claim.
- **Language-family LM baseline:** Dravidian SA comparison uses Sangam Tamil syllabic LM (944 bigrams; Burrow & Emeneau 1984 DEDR + Sangam corpus). Sanskrit LM is the comparison. Lift ratio = fraction of H+M readings favored by Dravidian LM over Sanskrit LM. All LMs are available in `backend/glossa_lab/data/`.

### 2.6 External Validation

The following validation types are separated:

| Validation Type | What it tests | Current status |
|---|---|---|
| **Structural validation** | Non-random positional structure; grammar model fit | STRONG — permutation null z=10.3; held-out 97.7%; 10/10 Mahadevan papers; Nair 2026 structural replication |
| **Phonological validation** | Dravidian language-family compatibility | MODERATE — 1.85× lift over Sanskrit; Parpola 94 59% overlap; phonotactic validity confirmed; Munda SA not yet executed |
| **Lexical validation** | Individual sign readings | PARTIAL — 44/75 HIGH readings in Parpola 1994; all require further independent confirmation |
| **Archaeological validation** | Fish-sign polysemy; Gulf context | STRONG for fish-sign null; 0/113+27 isolated |

No single validation type constitutes complete external validation. A bilingual inscription or ICIT replication of the phonetic model would constitute higher-level validation.

---

## 3. Results

### 3.1 Sign Anchor Summary

A prior version of this work reported 268 H+M signs based on an anchor count that included 107 heuristic placeholder assignments (Phase-104–115 sprint phases). Phase-133 identified these as non-phonetically-grounded and removed them. **All headline metrics below use the Phase-133 corrected genuine count.**

**Table 2: Confidence Summary**

| Confidence | Signs | Tokens Covered | Token Coverage | Criteria |
|---|---:|---:|---:|---|
| HIGH | 75 | 5,346 | 76.35% | ≥2 independent evidence types |
| MEDIUM | 86 | 1,017 | 14.52% | ≥1 strong evidence type + no contradiction |
| PROVISIONAL_MEDIUM | 4 | 15 | 0.21% | MEDIUM criteria; pending expert review |
| LOW | 236 | 624 | 8.91% | Heuristic only — **not counted toward coverage** |
| **H+M Genuine Total** | **161** | **6,363** | **90.87%** | Genuine phonetically-grounded |

**Coverage caveat:** Token coverage measures the fraction of corpus tokens assigned to signs with at least one HIGH or MEDIUM candidate reading. It does not imply that those readings are verified phonetic transcriptions. The 69.8% seal coverage (1,165/1,670) measures the fraction of seals in which every sign has a candidate H+M reading; it does not imply that those seals have been "read" in any verified phonetic sense.

### 3.2 Grammar Model

Statistical analysis of inscription structure identifies a recurring three-slot pattern:

```
[SLOT 1: CLASSIFIER] – [SLOT 2: GUILD/TITLE] – [SLOT 3: SUFFIX/PERSONAL]
```

This structure is consistent across all 9 sites (100% of H+M signs show consistent positional class, Phase-69) and across 97 identified formula types. The dominant formula backbone is M342·M176 (ay/ā · an/aṇ, PMI = 2.43, 122 seals). Grammar model sign-level accuracy: 93.2% at 161 H+M (Phase-170).

### 3.3 Candidate High-Confidence Readings

**Table 3: Selected HIGH-Confidence Anchor Readings**

| Sign | Reading | Frequency | Evidence 1 | Evidence 2 | DEDR | Notes |
|---|---|---:|---|---|---|---|
| M045 | yānai | 43 | Elephant icon match | Distributional exclusivity | 5175 | Tamil yānai |
| M062 | erutu | 63 | Zebu bull exclusive (lift > 5.0) | Parpola 1994 independent | 820 | Zebu bull |
| M073 | kōṉ | 38 | Zebu bull exclusive (lift > 5.0) | Parpola 1994 independent | 2206 | King/bull |
| M342 | ay/ā | 584 | Terminal rate 96% | Parpola 1994 genitive terminal | — | Case suffix |
| M176 | an/aṇ | 356 | Terminal rate 94% | Parpola 1994 masculine suffix | 135 | Masculine suffix |
| M016 | kaḷiṟu | 52 | Elephant icon match | Distributional exclusivity | — | Elephant |
| M006 | puli | 47 | Tiger icon match | Distributional exclusivity | — | Tiger |
| M047 | min/mīn | 13 | Fish icon (P47 crosswalk) | Parpola 1994 iconographic | — | Fish sign |
| M267 | iN/in | 400 | Motif-independence χ²=12.98, p=0.11 | Grammar position (pre-title) | — | Genitive particle (CORRECTED from mīn) |

**Table 4: Corrected / Retired Readings**

| Sign | Earlier Reading | Problem | Revised Reading | Evidence |
|---|---|---|---|---|
| M267 | fish/mīn | M267 appears across all motif types (unicorn 127, zebu 72, elephant 37, rhino 25); no iconographic specificity; M047 is the actual fish sign | iN/in (MEDIUM genitive particle) | Motif-independence χ²=12.98, p=0.1124; consistent pre-title distribution; 6,869 Parpola genitive references |
| M330, M165, M202, M198 | Not previously assigned | Phase-163 text proximity proposed readings; Phase-166 DEDR cross-validation | PROVISIONAL_MEDIUM: can/cul/can/co | DEDR 2322/2700/2322/2816; positional profiles consistent; 3–4 literature references each; expert review required |

### 3.4 Fish Sign Polysemy Test

We tested the hypothesis (Roif 2025b) that isolated fish signs encode commodity units while compound fish signs encode occupational titles. Testing the full fish sign family (M047, M049, M052–M056, M145) across all 9 sites:

| Site | Type | Fish Seals | Isolated | Compound |
|---|---|---:|---:|---:|
| Lothal | coastal port | 6 | 0 (0%) | 6 (100%) |
| Harappa | inland | 33 | 0 (0%) | 33 (100%) |
| Mohenjo-daro | inland | 35 | 0 (0%) | 35 (100%) |
| Dholavira | inland | 11 | 0 (0%) | 11 (100%) |
| All others | inland | 28 | 0 (0%) | 28 (100%) |
| **Total** | | **113** | **0 (0%)** | **113 (100%)** |

Gulf deposit validation (Laursen 2010; Mitchell 1986): 27 Indus-script contexts in Gulf-type seal catalogs; no isolated fish signs found. Combined: 0/140. The fish sign is consistently compound in all tested contexts. Consistent with Martini (2025) finding that commodity tallies in IVC were recorded on perishable media.

### 3.5 Seal Coverage Statistics

| Metric | Value | Notes |
|---|---|---|
| Total seals | 1,670 | Holdat V3 |
| Seals fully covered by genuine H+M | 1,165 (69.8%) | All signs have candidate H+M reading |
| Seals blocked by LOW-only signs | 505 (30.2%) | At least one sign has no H+M candidate |
| Blocked by fully unknown signs | 0 | All signs have some reading at LOW or above |
| Prior inflated count (heuristic H+M) | 1,429 (85.6%) | Includes Phase-104–115 placeholders |

### 3.6 Null Model Results

**Table 5: Key Null Model Results**

| Test | Observed | Null Mean | Null SD | p-value | Interpretation |
|---|---:|---:|---:|---:|---|
| F1: Grammar model R² vs within-seal shuffle (n=2,000) | 0.992 | 0.438 | 0.031 | < 0.001 | Strong non-random positional structure |
| F7: Held-out sign-class prediction (80/20 site split) | 97.7% | — | — | — | Grammar generalizes to unseen seals |
| Fish-sign isolation (n=140 Gulf+mainland contexts) | 0/140 | — | — | p < 0.001 (binomial) | Compound-only pattern not due to chance |
| Dravidian vs Sanskrit LM lift (F12) | 1.85× | 1.00 | — | — | Dravidian-favoured at 88% of H+M readings |
| M267 motif-independence χ² | χ²=12.98 | — | — | p=0.1124 | UNIFORM distribution — genitive particle |
| Phase-52 SA z-score (59 anchors pinned) | z=16.02 | 0 | 1.0 | p < 0.001 | SA consistency far above null |
| Phase-57 SA z-score (53 anchors pinned) | z=19.07 | 0 | 1.0 | p < 0.001 | Highest SA z-score in project |

---

## 4. Evidence Tiers and Claim Scope

### Tier 1: Strong Structural Claims
These may be stated with high confidence given the data:

- **Non-random positional structure** — permutation null z=10.3, p<0.001; held-out accuracy 97.7%; site-invariant across all 9 sites
- **Recurring three-slot formula** — 97 formula types; dominant backbone PMI=2.43; bi-channel (text+icon) co-selection in 63/394 (16%) tested pairs
- **Fish sign exclusively compound** — 0/140 isolated across all tested contexts
- **M267 is not the fish sign** — frequency 400; motif-independence p=0.11; actual fish sign is M047
- **Pan-Harappan scribal system** — 100% of H+M signs show site-consistent positional class (Phase-69)

### Tier 2: Probable Linguistic Interpretation
These are supported but require qualification:

- **Proto-Dravidian compatibility** — Dravidian LM 1.85× lift over Sanskrit; 88% of H+M readings Dravidian-favoured; 44/75 HIGH readings in Parpola (1994); phonotactic validity confirmed. *Note: Munda SA was not constructed to the same resolution; Elamo-Dravidian not tested.*
- **DEDR rebus readings** — 161 signs have candidate readings meeting stated criteria; each reading is a proposal, not a phonetic certainty
- **Terminal suffix interpretation** — M342=ay/ā, M176=an/aṇ consistent with Dravidian case morphology
- **Grammar as administrative encoding** — consistent with administrative seal traditions in broader South Asian context

### Tier 3: Speculative or Provisional Claims
These require explicit caveats:

- **Guild-identity administrative system** — one plausible semantic frame; not the only consistent interpretation
- **Individual seal "translations"** — reflect candidate readings, not verified transcriptions
- **Munda substrate** (M374=kul, M351=vī) — speculative; lacks independent phonological confirmation
- **Arthaśāstra administrative continuity** — illustrative of possible continuity across 2,000 years; not evidential
- **Full semantic decipherment** — not achieved; requires bilingual inscription or ICIT replication

---

## 5. Adversarial Tests and Failure Conditions

### 5.1 Non-Linguistic Emblem Hypothesis

**Hypothesis being tested:** The observed positional structure arises from non-linguistic emblem sequencing, ownership marks, or ritual formulae rather than linguistic encoding.

**Evidence against:**
- Within-seal shuffle null (n=2,000): real corpus R²=0.992 vs null mean 0.438 (z=10.3, p<0.001). If structure were emblem-based without sequential grammar, shuffled sequences should produce similar R².
- Motif-conditioned test: positional class assignments survive after controlling for seal motif type (Phase-69, 100% site-consistency). Emblem-only models predict positional classes would collapse once motif is controlled.
- Bigram conditional entropy H(X₂|X₁)/H(X₁) = 0.611 (natural language range 0.5–0.8; random ≥ 0.95). An emblem sequence model without sequential dependencies predicts values near 0.95.

**Remaining uncertainty:** Non-linguistic highly regular emblem systems (e.g., heraldic sequences) have not been formally modeled. A motif-conditioned bigram null model quantifying emblem-sequence entropy would strengthen this test.

### 5.2 Rebus Overfitting Risk

**Risk:** With ~5,000 DEDR entries, post-hoc Dravidian readings could be constructed for any sign regardless of the true language.

**Controls applied:**
- Readings were proposed before searching DEDR in most cases (iconographic + distributional first, DEDR second)
- Phonotactic constraints (Krishnamurti 2003) restrict valid initial consonants
- SA-consistency requirement (≥ 0.15) provides independent distributional evidence
- Multiple candidate readings per sign are noted in `INDUS_FINAL_ANCHORS.json` `basis` fields

**Remaining gap:** We do not systematically report the total number of DEDR candidates per sign; this should be added in the next version to allow false-positive rate estimation.

### 5.3 Competing Language Families

**What was tested:**
- Dravidian vs Sanskrit: lift ratio 1.85× (Phase-67); Dravidian favoured at 88% of H+M readings
- Phonotactic exclusivity test (Phase-146): 0/157 H+M readings require Sanskrit-exclusive phonemes; 35/157 require Dravidian-exclusive phonemes

**What was NOT tested:**
- Munda SA: no Munda-vocabulary SA was constructed to the same resolution as the Dravidian SA. The Munda substrate hypothesis for M374 and M351 is stated but not formally tested against alternatives.
- Elamo-Dravidian: not tested
- Language-neutral syllabic models: partial (syllabic LM z=16.02 at Phase-52 shows SA can find high-consistency mappings; this does not discriminate between language families)

**Summary:** Dravidian superiority over Sanskrit is quantified at 1.85×. Dravidian superiority over Munda is not yet quantified; this is an acknowledged gap.

### 5.4 Motif Circularity

**Risk:** Animal classifier readings (M045=yānai from elephant icon) are inferred from the animal icon, and then the animal icon is cited as "independent corroboration."

**Current status:** The motif enrichment test (Phase-143, 63/394 pairs significantly enriched) tests whether sign-motif co-occurrence is above chance. However, it does not formally test independence from the iconographic-anchor assignment process.

**Proposed test (not yet executed):** Hold out all motif labels; assign positional classes from text statistics alone; then test whether text-derived initial-class signs predict motif type enrichment. If F1 score for motif prediction from text-only classes exceeds chance, this supports genuine (not circular) co-selection. This test is specified for the next analysis cycle.

### 5.5 False Discovery Control

**Tests with Bonferroni correction applied:**
- Motif enrichment (Phase-143): χ² with Bonferroni for 394 sign×motif pairs; significance threshold α = 0.05/394 = 0.000127
- Bootstrap CI for site divergence (Phase-151): 95% CI reported for all 36 site-pair KL values

**Tests where FDR correction was not applied:**
- Sign-level DEDR rebus matching: no formal FDR applied; the "foundation check" tests are treated as internal consistency checks, not multiple-comparison hypothesis tests
- SA-consistency thresholds: the ≥ 0.15 threshold was set a priori; no Benjamini-Hochberg adjustment was applied to sign-level SA verdicts

**Acknowledged gap:** A Benjamini-Hochberg FDR analysis of sign-level SA verdicts is recommended before any HIGH-confidence claims are treated as phonetically definitive.

### 5.6 Failure Conditions

**Table 6: What Would Weaken or Falsify the Model**

| Claim | Would Be Weakened By | Current Status |
|---|---|---|
| Non-random positional structure | Permutation null p > 0.01 after motif and site control | ROBUST — z=10.3, site-invariant |
| Fish sign compound-only | Any isolated fish sign in formal seal context | ROBUST — 0/140 |
| M267 = genitive particle | Non-uniform motif distribution (χ² p < 0.05) | ROBUST — p=0.1124 |
| Proto-Dravidian reading framework | Munda or Sanskrit SA achieving equal or higher z-score with equal anchor density | NOT YET TESTED for Munda |
| Individual HIGH readings | Any reading failing an independent cross-language test (e.g., appearing in non-Dravidian text with incompatible reading) | PARTIALLY TESTED — 59% Parpola overlap supports |
| 3-slot grammar model | Grammar model R² < 0.5 after motif-conditioning null | ROBUST — R²=0.992 vs null 0.438 |
| PROVISIONAL_MEDIUM sibilants | Expert phonological review rejecting DEDR assignments | PENDING — explicitly flagged |
| Candidate model generalizes | H+M readings fail to predict sign classes in ICIT corpus | NOT YET TESTED — ICIT required |

---

## 6. Discussion

### 6.1 Proposed Readings Under the Model

Under the proposed grammar model, a typical seal inscription can be described as follows. The structure [CLASSIFIER]–[TITLE]–[SUFFIX] is consistent across motif types. For example:

- M211 M099 M342: under candidate readings, this is *kol–kol–ay* — consistent with a guild-title formula (unicorn seal)
- M062 M342 M176: under candidate readings, *erutu–ay–an* — consistent with a personal-name suffix formula (zebu bull seal)

**These are proposals under the model, not verified transcriptions.** Each reading carries the confidence level of its anchor (HIGH, MEDIUM, or PROVISIONAL_MEDIUM), and none of these confidence levels implies phonetic certainty without external validation.

### 6.2 Substrate Evidence (Tier 3)

Two signs (M374=kul, M351=vī) have MEDIUM readings assigned on the basis of Munda substrate near-cognates. These are explicitly Tier 3 (speculative): the substrate hypothesis is consistent with known Munda substrate in historical Dravidian and Indo-Aryan, but the readings lack independent phonological confirmation. They are included in the MEDIUM count with explicit substrate notation.

### 6.3 Irresolvable Signs

18 signs with corpus frequency 5–7 resist MEDIUM promotion under current methodology: their SA modals do not match DEDR entries, they show no iconographic or distributional exclusivity, and they appear exclusively in MEDIAL position. This pattern is consistent with personal-name syllables in an identity-encoding system. **They are not proven irresolvable** — ICIT corpus (5,318 texts) may provide sufficient additional context for assignment.

### 6.4 Limitations

1. **No bilingual text:** All readings remain probabilistic until a bilingual inscription is discovered.
2. **Corpus size:** 7,002 tokens; many claimed patterns are robust by permutation test, but complex phonological claims are underpowered.
3. **Single corpus type:** Formal stamp seals only. Copper tablets, potsherd graffiti, and the Dholavira signboard require separate analysis.
4. **Phonological drift:** SA trained on modern Tamil; 4,000-year drift may introduce systematic errors. Proto-Dravidian phonology is reconstructed, not directly attested.
5. **Munda alternative untested:** No full Munda-lexicon SA has been constructed. Dravidian superiority over Munda is not yet quantified.
6. **Anchor count correction history:** The pre-Phase-133 count of 268 H+M signs included heuristic placeholders. The corrected genuine count is 161. This history is documented in METRIC_AUDIT.md.

### 6.5 Validation Path (Updated)

1. **Bilingual text:** Any inscription alongside a known script at a Gulf trade site
2. **ICIT corpus replication:** The 5,318-inscription Fuls database allows testing whether H+M readings predict sign classes in an independent corpus (contact: fuls@epigraphica.de)
3. **Expert peer review of PROVISIONAL_MEDIUM:** Phase-166 sibilant assignments require phonologist review before HIGH promotion
4. **Munda SA construction:** To formally quantify Dravidian superiority over Munda
5. **Motif circularity test:** Hold-out test specified in §5.4

---

## 7. Conclusion

We propose a reproducible computational grammar and candidate Proto-Dravidian anchor model for the Indus Valley Script based on systematic positional analysis, DEDR rebus matching, and syllabic language-model simulation on the Holdat V3 corpus. The strongest findings — robust non-random positional structure (permutation z=10.3), a recurring three-slot inscription formula, fish-sign compound-only pattern (0/140), and M267 misassignment correction — are Tier 1 structural claims that can be stated with high confidence. The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage) are Tier 2 claims: supported by multiple converging tests but not yet externally validated. Speculative interpretations including the guild-identity semantic frame, Munda substrate readings, and individual seal translations are Tier 3 claims requiring explicit caveats.

The present study does not claim epigraphic finality in the absence of a bilingual inscription; it proposes a reproducible, falsifiable computational model whose structural predictions and candidate phonetic readings can be tested against larger corpora and future discoveries. The ICIT corpus (Dr. Andreas Fuls, 5,318 texts) is the immediate priority for testing whether the candidate model generalizes. All phase reports, scripts, and the anchor table are openly available for inspection and replication.

---

## 8. Data Availability

- **Anchor table:** `backend/reports/INDUS_FINAL_ANCHORS.json` (Glossa-Lab repository)
- **Canonical sign audit:** `glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv`
- **Phase reports:** `backend/reports/phase*.json`
- **Phase scripts:** `backend/scripts/phase*.py`
- **Reproduction checklist:** `glossa-corpus/indus/REPRODUCTION_CHECKLIST.md`
- **Corpus:** Holdat LLC Indus Corpus V3 (Miller 2025) — contact Holdat LLC for access

---

## 9. Acknowledgments

Holdat LLC (W. Miller) for the Indus corpus. Mahadevan (1977) for the sign catalogue. Parpola (1994, 2010) for the Dravidian decipherment framework. Martini (2025) for Arthaśāstra administrative analysis. Avishai Roif (Ben Gurion University) for correspondence on the fish-sign polysemy hypothesis. Ashish Nair for the independent structural replication (Nair 2026, preprint).

**AI Disclosure:** This research was conducted with AI-assisted computational tooling (Glossa-Lab pipeline, Warp/Oz agent, Anthropic Claude). All analysis scripts, corpus data, anchor tables, and phase reports are openly available for independent replication. Statistical tests were designed, executed, and interpreted by the author; AI tooling was used for scripting, data management, and literature search.

---

## 10. References

- Burrow, T. & Emeneau, M.B. (1984). *A Dravidian Etymological Dictionary* (2nd ed.). Oxford: Clarendon Press. [DEDR]
- Crawford, H. (2001). *Early Dilmun Seals from Saar*. Archaeology International.
- Farmer, S., Sproat, R. & Witzel, M. (2004). The Collapse of the Indus-Script Thesis. *Electronic Journal of Vedic Studies*, 11(2), 19–57.
- Hojlund, F. & Abu-Laban, A. (2012). *Tell F6 on Failaka Island: Kuwaiti-Danish Excavations 2008–2012*. Jutland Archaeological Society.
- Krishnamurti, B. (2003). *The Dravidian Languages*. Cambridge: Cambridge University Press.
- Lubotsky, A. (2001). The Indo-Iranian substratum. In *Early Contacts between Uralic and Indo-European*. Helsinki: Suomalais-Ugrilainen Seura.
- Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. New Delhi: Archaeological Survey of India.
- Martini, G.A. (2025). *Arthaśāstra Administrative Vocabulary and IVC Seal Terminology*. PhD dissertation.
- McAlpin, D.W. (1981). *Proto-Elamo-Dravidian: The Evidence and Its Implications*. Philadelphia: American Philosophical Society.
- Miller, W. (2025). Holdat LLC Indus Corpus V3. [Dataset]. Contact: Holdat LLC.
- Nair, A. (2026). How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard. arXiv:2604.17828. [Preprint — not peer-reviewed]
- Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge: Cambridge University Press.
- Parpola, A. (2010). A Dravidian solution to the Indus script problem. *World Archaeology*, 42(2), 178–193. DOI: 10.1080/00438241003672726
- Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. *PNAS*, 106(33), 13685–13690. DOI: 10.1073/pnas.0906508106
- Roif, A. (2025a). The Indus Script as a Mnemonic Framework. Preprint.
- Roif, A. (2025b). Deciphering the Indus Valley Script: A Phonetic-Mnemonic Akkadian Shorthand Approach. Preprint.
- Southworth, F. (2005). *Linguistic Archaeology of South Asia*. London: Routledge.
- Wells, B. (2015). *The Archaeology and Epigraphy of Indus Writing*. Oxford: Archaeopress.
- Witzel, M. (1999). Substrate Languages in Old Indo-Aryan. *Electronic Journal of Vedic Studies*, 5(1), 1–67.

---

## Supplement A: Phase-by-Phase Results Summary

*(Available in `backend/reports/phase*.json` — Phases 1–170. Key milestones listed below for orientation.)*

| Phase Range | Key Finding |
|---|---|
| 1–30 | Corpus ingestion, positional profiling, first 7 HIGH anchors |
| 31–47 | Language model comparisons; Dravidian lift ratio established |
| 48–61 | SA expansion to 75 HIGH; phonotactic validation |
| 62–73 | Grammar model; Sanskrit normalisation; M267 correction |
| 74–100 | DEDR systematic expansion; grammar cross-validation |
| 101–133 | Phase-133 anchor count correction (268 → 161); coverage audit |
| 134–141 | Falsification battery (10 tests, 0 failures) |
| 142–165 | Literature cross-validation (Parpola, Wells, Mahadevan); literature ceiling confirmed |
| 166–168 | Sibilant DEDR validation; Meluhhan names; blocker analysis |
| 169–170 | Master synthesis (32 items, 79.8% aggregate confidence); grammar retest (93.2%) |

---

## Appendix A: Summary of Substrate Anchor Readings

| Sign | Reading | Confidence | DEDR | Substrate | Evidence |
|---|---|---|---|---|---|
| M374 | kul | MEDIUM | 1709 | Munda *kul* (tiger-lord) | MEDIAL between authority signs; kulam=clan/lineage |
| M351 | vī | MEDIUM | 5388 | Munda *bi* (seed/sprout) | MEDIAL agricultural context; bi→vī bilabial shift |

These are Tier 3 (speculative) readings included with explicit substrate notation.

---

## Appendix B: The 18 Signs Resisting MEDIUM Promotion

Signs with corpus frequency 5–7 that resist MEDIUM promotion under current methodology. They appear exclusively in MEDIAL position with SA modals lacking clear DEDR matches.

Signs (18): M183, M190, M223, M239, M254, M270, M295, M304, M321, M329, M345, M357, M365, M386, M137, M143, M151, M402.

*Note: M198 was removed from this list after Phase-166 promoted it to PROVISIONAL_MEDIUM (reading: co, DEDR 2816). These signs resist MEDIUM promotion under current methodology but are not formally proven irresolvable; the ICIT corpus (5,318 texts) may provide sufficient additional context.*

---

## Appendix C: Internal Consistency Validation

59 automated internal consistency checks (foundation_check.py, Phases 1–170) all pass. These are **internal consistency checks**, not external validation. Key checks include:

- Holdat corpus integrity: 1,670 seals, 7,002 tokens, 390 signs, M-prefixed, position-sorted
- Anchor metadata consistency: `total` field = actual H+M count
- Phase-44: Dravidian lift ratio 3.13× above SA null
- Phase-46: All 7 core HIGH anchors in Janabiyah contact-zone seal
- Phase-57: SA z=19.07 (53 anchors pinned)
- Phase-166: Sibilant DEDR hits = 4, rejected = 0
- Phase-169: Aggregate confidence ≥ 75%
- Phase-170: H+M count = 161, grammar accuracy ≥ 90%

Internal consistency is a necessary but not sufficient condition for the model to be correct.
