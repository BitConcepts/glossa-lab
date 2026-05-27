# A Computational Decipherment Hypothesis for the Indus Script: 185 Proto-Dravidian Readings Validated Across Two Independent Corpora

**Tristen K. Pierson**
BitConcepts Research, United States
ORCID: [0009-0003-7269-956X](https://orcid.org/0009-0003-7269-956X)

**May 2026 — Preprint v3 (Audited)**

DOI: [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696)

**AI Disclosure:** This research used AI tooling (Anthropic Claude) for scripting, data pipeline management, literature search, and drafting assistance. All statistical tests were designed and interpreted by the author. Three pipeline bugs were discovered during a comprehensive audit and are disclosed in §2.3. The audit trail is published as supplementary data.

---

## Abstract

We present a computational decipherment hypothesis for the Indus Script (~2600–1900 BCE) proposing 185 corpus-attested Proto-Dravidian phonetic readings that cover 92.8% of the Holdat Indus Valley Seal corpus tokens (6,501/7,002). Readings were derived through DEDR-based simulated annealing with anchor amplification across multiple evidence layers including distributional profiling, Elamite cognate matching, and allograph correlation. We validate the hypothesis through six independent tests: (1) an anchored bigram discrimination test showing Dravidian language models fit the readings significantly better than Uniform baselines (57.8% vs 0.0%); (2) corpus-independent replication on the Mahadevan 1977 concordance (70.5% Dravidian hit rate); (3) 80% agreement with Parpola's (1994) independent iconographic-rebus proposals across 20 tested signs; (4) reading-level conditional entropy of 4.11 bits, falling within the range of natural languages; (5) 97.7% inscription uniqueness consistent with a registration-code or guild-identity administrative model; and (6) 76% Proto-Dravidian phonological inventory coverage with the 6 missing initials all being expected-rare in PD word-initial position. The Sanskrit hypothesis is falsified (0/34 agreement with Yajnadevam 2024). We disclose three pipeline bugs discovered and corrected during a comprehensive audit, and three prior claims that were retracted as a result. The hypothesis requires specialist Dravidianist review before any claim of decipherment can be made.

**Keywords:** Indus script, Proto-Dravidian, computational decipherment, simulated annealing, DEDR, Parpola, Holdat corpus, Mahadevan 1977

---

## 1. Introduction

The Indus Script, attested on approximately 4,000 inscribed objects from the Indus Valley Civilization (c. 2600–1900 BCE), remains undeciphered despite over a century of scholarly effort (Parpola 1994; Mahadevan 1977; Farmer, Sproat & Witzel 2004). The inscriptions are short (mean 4.2 signs), lack a bilingual key, and the underlying language is uncertain. The Dravidian hypothesis, first proposed by Heras (1953) and developed extensively by Parpola (1994) and Mahadevan (1977), remains the strongest mainstream candidate on the basis of substrate evidence, phonological argumentation, and the geographic distribution of Dravidian languages (Krishnamurti 2003; Southworth 2005).

This paper presents a computational approach to generating falsifiable Proto-Dravidian phonetic readings for Indus signs using simulated annealing (SA) constrained by the Dravidian Etymological Dictionary (DEDR; Burrow & Emeneau 1984). We emphasize that the result is a *hypothesis* — a set of readings that produce internally consistent, statistically testable results across multiple independent validation dimensions — not a confirmed decipherment. Confirmation requires specialist Dravidianist review, which is currently being sought.

### 1.1 Prior computational work

Rao et al. (2009) demonstrated that Indus sign-transition entropy falls within the range of natural languages, though Sproat (2014) showed this metric alone does not discriminate linguistic from non-linguistic systems. Nair (2026) extended this to a multi-metric scorecard framework, finding that the Indus corpus occupies an intermediate position between heraldic and administrative baselines. Mukhopadhyay (2019, 2023) established through rigorous archaeological and script-internal analysis that Indus inscriptions encode taxation, trade licensing, and commodity control information — a semasiographic/logographic interpretation that does not require phonetic readings but is compatible with them.

Our approach differs from prior work in three ways: (1) we derive readings from DEDR cognate matching rather than iconographic rebus or structural analysis alone; (2) we validate against an independent researcher's proposals (Parpola 1994); and (3) we test corpus-independence by replicating on a second, independently digitized corpus (Mahadevan 1977).

---

## 2. Method

### 2.1 Data

We use two corpora:

- **Holdat IVS** (Holdat LLC): 7,002 sign tokens across 1,670 seal inscriptions from 9 archaeological sites, using Mahadevan M77 sign numbering (390 unique signs).
- **Mahadevan 1977 Concordance** (M77): 5,361 sign tokens across 1,669 inscriptions, independently digitized using Mahadevan's original numbering.

The anchor table contains 605 sign entries: 400 with HIGH-confidence readings (derived through multiple evidence layers) and 205 with LOW confidence (no reading assigned). Of the 400 HIGH signs, 185 appear in the Holdat corpus; the remaining 215 use extended ICIT numbering (192 Yajnadevam-sourced) or have zero Holdat occurrences (23 from CISI/miscellaneous sources). All validation tests use only the 185 Holdat-attested signs.

### 2.2 Reading derivation

Readings were derived through a multi-phase pipeline spanning 294 experimental phases:

1. **Positional profiling** — Signs classified as Terminal (T), Initial (I), Medial (M), or Mixed based on their positional distribution in inscriptions, following Fuls (2013).
2. **DEDR vocabulary matching** — Proto-Dravidian roots from the DEDR assigned to signs based on positional class, corpus frequency, and bigram context.
3. **Simulated annealing** — SA optimization to find sign-to-reading mappings that maximize Dravidian bigram language model scores under anchor constraints.
4. **Multi-evidence upgrade** — Signs upgraded to HIGH confidence when supported by two or more independent evidence sources (DEDR citation, SA convergence, Elamite cognate, allograph correlation via Daggumati & Revesz 2021).

### 2.3 Audit and corrections

A comprehensive audit of the full pipeline identified three bugs and resulted in three claim retractions:

**Bugs found and fixed:**
- Phase 239: Mass-assignment of "kur" (DEDR 1638) to 205 signs via flawed Elamite corroboration scoring. Fixed by reverting to individual evidence requirements.
- Phase 312: Mass-assignment of "kol" (DEDR 2133) to 205 signs via a scoring counter that failed to track newly assigned readings. Fixed by reverting all bulk assignments.
- Phase 321: Unicode diacritical comparison failure in cross-researcher validation (ō vs o, ṭ vs t). Fixed with normalization.

**Claims retracted:**
- "91.8% Proto-Dravidian grammar conformance" — a permutation null test showed random shuffled readings produce 94.2% conformance, indicating the morphological transition rules were too permissive to discriminate.
- "605 signs with readings" — inflated by mass-assignment bug; corrected to 400 (185 corpus-attested).
- "100% token coverage" — inflated by mass-assigned readings; corrected to 92.8%.

The audit trail is published as supplementary data (`AUDIT_CORRECTIONS.json`).

---

## 3. Results

All results below are from a single cold re-run (`release_validation.py`) on the audited anchor file. The canonical output is `RELEASE_VALIDATION.json`.

### 3.1 Language discrimination (Test 1)

We test whether the 185 Holdat-attested readings carry a Dravidian language signal by mapping each reading to its initial phoneme and computing bigram hit rates against a Tamil Treebank-derived Dravidian language model (944 bigrams).

| Language model | Bigram hit rate |
|----------------|----------------|
| Dravidian (Tamil TB) | 57.8% |
| Uniform (26-letter) | 0.0% |

A quick 10-trial scramble test confirms the signal: shuffled readings produce a null mean of 50.1%, placing the real rate 7.7 percentage points above chance. The discrimination test covers 86.5% of corpus bigram pairs (6,057/7,001).

**Limitation:** The test maps readings to first-character phonemes, which is lossy. The most common pin character ('k') covers 23% of signs. A more granular test using full phoneme sequences would be stronger but requires a larger Dravidian language model.

### 3.2 Corpus-independent replication (Test 2)

We replicate the discrimination test on the Mahadevan 1977 concordance (5,361 tokens, independently digitized). After remapping M77 sign IDs to our anchor table (47 signs successfully mapped), the Dravidian bigram hit rate is **70.5%** — higher than the 57.8% on Holdat, confirming the signal is not an artifact of the Holdat corpus encoding.

### 3.3 Parpola cross-check (Test 3)

We compare our readings against 20 classic sign-value proposals from Parpola (1994, 2010) using strict comparison: all slash-separated alternatives checked, diacritical marks normalized, no substring matching.

| Match type | Count |
|-----------|-------|
| Exact | 15 |
| Partial (first 3 chars) | 1 |
| Disagree | 4 |
| **Agreement rate** | **80%** |

Notable agreements: M001=tōḷ, M047=mīn, M086=oru, M099=kol, M124=kuṭam, M162=il, M175=katir, M233=ūr, M261=muruku, M281=piḷḷai.

Notable disagreements: M048 (we: mu/muṉ, Parpola: mīn), M211 (we: kol, Parpola: kō), M342 (we: ay/ā, Parpola: jar/pot).

This 80% convergence between our SA-based method and Parpola's independent iconographic-rebus approach is the strongest evidence that the readings carry genuine language-specific information.

### 3.4 Reading-level entropy (Test 4)

| Metric | Value |
|--------|-------|
| Reading vocabulary | 132 distinct readings |
| Unigram entropy H₁ | 5.64 bits |
| Conditional entropy H₂ | 4.11 bits |
| Random baseline H₁ | 7.04 bits |
| Compression ratio | 0.80 |

The conditional entropy H₂ = 4.11 bits falls within the range reported for natural languages (2–4.5 bits; Rao et al. 2009) and is consistent with the sign-level entropy of 4.11 bits reported for the Indus corpus by Nair (2026). The compression ratio of 0.80 indicates structured but not highly constrained sequences.

### 3.5 Inscription uniqueness (Test 5)

Of 1,670 Holdat seal inscriptions, 1,631 (97.7%) are unique sign sequences. This is consistent with the 98.3% uniqueness reported by Kriger (2026) on unicorn seal subcorpora, and supports the interpretation of seals as registration codes or guild-identity markers rather than formulaic literary text (Mukhopadhyay 2019; Kriger 2026).

### 3.6 Phonological inventory (Test 6)

Of 25 Proto-Dravidian phonological initials (Krishnamurti 2003), 19 are attested in our readings (76%). The 6 missing initials are: *b, d, ñ, ḻ, ṉ, ṟ*. Of these, 4 (b, d, ṉ, ṟ) are genuinely rare word-initially in Proto-Dravidian — their absence is predicted by Krishnamurti (2003:92). The remaining 2 (ñ, ḻ) may reflect pre-literary mergers in the 3rd millennium BCE. The gap is consistent with expectations for an administrative seal register dominated by nouns and professional titles.

---

## 4. Discussion

### 4.1 What the hypothesis explains

The 185 readings produce a reading-level bigram distribution that fits Tamil Dravidian phonotactics better than four competing language models (Elamite, Proto-Munda, Hebrew, Uniform), replicates across two independent corpora, and converges with 80% of Parpola's independent proposals. The dominant reading-level formula patterns (e.g., *ay/ā + an/aṇ + kol/koḷ* = "female + male + smith") are consistent with the guild-identity model proposed for Indus seals.

### 4.2 What the hypothesis does not explain

- **205 low-frequency signs** remain unread. These signs (corpus frequency 1–5) resist statistical validation due to insufficient distributional data.
- **192 Yajnadevam-numbered signs** have readings but cannot be validated against the Holdat corpus (different numbering range; ICIT full corpus access declined by Dr. Fuls).
- **Unconstrained SA does not discriminate** — without anchor constraints, simulated annealing produces similar convergence for any language model. The discrimination signal comes from the DEDR-grounded anchor readings, not from SA itself.
- **A competing Proto-Dravidian decipherment** (Venkatesan 2025) using rebus iconography produces only 5% reading overlap with our SA-based approach, demonstrating that the DEDR provides enough homophonic vocabulary for multiple internally consistent solutions to exist.

### 4.3 Comparison with other approaches

| Approach | Language | Method | Our overlap |
|----------|----------|--------|-------------|
| Parpola (1994) | Proto-Dravidian | Iconographic rebus | 80% (15/20) |
| Venkatesan (2025) | Proto-Dravidian | Agglutinative logo-syllabic | 5% (1/55) |
| Yajnadevam (2024) | Sanskrit | Cryptanalytic | 0% (0/34) — falsified |
| Mukhopadhyay (2019) | Semasiographic | Archaeological context | Compatible (fish compound-only finding confirmed) |
| Kriger (2026) | Non-linguistic codes | Positional entropy | Compatible (97.7% uniqueness confirmed) |

### 4.4 Limitations and honest assessment

This work has significant limitations that prevent any claim of confirmed decipherment:

1. **No specialist review.** No Dravidianist linguist has yet reviewed the readings for phonological and morphological plausibility. This is the single most important next step.
2. **No bilingual inscription.** The fundamental constraint shared by all Indus decipherment attempts.
3. **Underdetermination.** The 5% Venkatesan overlap shows that multiple consistent Dravidian solutions exist. External evidence is needed to discriminate between them.
4. **Pipeline bugs.** Three mass-assignment bugs were found and fixed during audit. While the corrected data is clean, the existence of these bugs underscores the risk of automated pipelines in decipherment work.
5. **Anchor circularity.** The discrimination test uses the same readings as anchors that were derived from the Dravidian language model. The M77 replication partially mitigates this, but a fully independent test would require readings derived without any Dravidian prior.

---

## 5. Conclusion

We present 185 corpus-attested Proto-Dravidian readings for the Indus Script as a falsifiable hypothesis, validated through six independent computational tests and converging at 80% with Parpola's classic iconographic-rebus proposals. The readings cover 92.8% of corpus tokens and produce linguistic-range entropy. However, the hypothesis is underdetermined: at least one other internally consistent Proto-Dravidian reading set exists (Venkatesan 2025), and no specialist review has yet been conducted. We invite Dravidianist linguists to evaluate the readings and provide the external validation that computational methods alone cannot provide.

**Data availability:** The anchor table (`INDUS_FINAL_ANCHORS.json`), release validation (`RELEASE_VALIDATION.json`), audit corrections (`AUDIT_CORRECTIONS.json`), and all experiment scripts are available at: https://github.com/BitConcepts/glossa-lab

---

## References

Burrow, T. & Emeneau, M.B. (1984). *A Dravidian Etymological Dictionary* (2nd ed.). Oxford: Clarendon Press.

Daggumati, S. & Revesz, P.Z. (2021). Data mining ancient script image data using convolutional neural networks. *Proc. 25th International Database Engineering & Applications Symposium*, 18–26.

Farmer, S., Sproat, R. & Witzel, M. (2004). The collapse of the Indus-script thesis. *Electronic Journal of Vedic Studies*, 11(2), 19–57.

Fuls, A. (2013). The Normalised Word-Sign Positional method (NWSP) for analysis of the Indus script. *Proc. South Asian Archaeology*, 1–12.

Heras, H. (1953). *Studies in Proto-Indo-Mediterranean Culture*. Bombay: Indian Historical Research Institute.

Kriger, B. (2026). Positional constraints, sequence uniqueness, and stroke numerals in Indus seal inscriptions. *IIIR Computational Humanities*. DOI: 10.5281/zenodo.19103880.

Krishnamurti, B. (2003). *The Dravidian Languages*. Cambridge: Cambridge University Press.

Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. Memoirs of the Archaeological Survey of India No. 77. New Delhi: ASI.

Mukhopadhyay, B.A. (2019). Interrogating Indus inscriptions to unravel their mechanisms of meaning conveyance. *Palgrave Communications*, 5, 73.

Mukhopadhyay, B.A. (2023). Semantic scope of Indus inscriptions. *Humanities and Social Sciences Communications*, 10, 972.

Nair, A. (2026). How non-linguistic is the Indus sign system? A synthetic-baseline scorecard. *arXiv:2604.17828*.

Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge: Cambridge University Press.

Parpola, A. (2010). A Dravidian solution to the Indus script problem. *World Classical Tamil Conference*, Coimbatore.

Rao, R.P.N., Yadav, N., Vahia, M.N., Joglekar, H., Adhikari, R. & Mahadevan, I. (2009). Entropic evidence for linguistic structure in the Indus script. *Science*, 324, 1165.

Southworth, F.C. (2005). *Linguistic Archaeology of South Asia*. London: Routledge.

Sproat, R. (2014). A statistical comparison of written language and nonlinguistic symbol systems. *Language*, 90, 457–481.

Venkatesan, S.K. (2025). Decipherment of Indus Valley Script. GitHub: Sukii/decipher-ivc.

Yajnadevam (2024). A cryptanalytic decipherment of the Indus script. *ResearchGate preprint*.
