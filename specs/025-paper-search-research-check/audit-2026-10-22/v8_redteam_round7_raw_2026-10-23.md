# Glossa Lab Indus Preprint v8 — Red-Team Round 7: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 123,853 chars, SHA-256 of PDF 48dfb48ed0d860af64c8d74786b79638dc8cd6185c491c2df2f76efe57a3a69b), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs. Each finding was briefed to carry a kind label: (i) a defect in what the paper says, or (ii) a limitation the paper itself already discloses at the same strength.


## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## PASS 1 — Internal consistency & arithmetic audit findings

### 1. Corpus-level arithmetic is not independently recomputable from the paper because the corpus is unavailable  
**Quoted passage:** Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” Also Abstract: “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”  
**Defect:** Most numerical claims depend on the private Holdat corpus. I can recompute ratios from printed numerators/denominators where supplied, but I cannot audit the underlying counts, sign frequencies, site tables, positional profiles, or permutation inputs from the paper alone. The paper discloses this at the same strength.  
**Severity:** CRITICAL  
**What would settle it:** Public release of the Holdat corpus, or a complete printed/exported count matrix sufficient to reproduce every corpus-level statistic.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 2. “H+M-covered seals” is used inconsistently in the formula-cluster material  
**Quoted passage:** §3.6: “Fully covered by H+M candidate readings 1,165 (69.8%).”  
§3.7: “A ‘formula type’ is one INITIAL sign together with the seals whose inscriptions begin with it: the 97 types are the 97 distinct INITIAL signs found among the H+M-covered seals (Phase-142 formula classification) — which is why §3.12’s clusters are organised by INITIAL sign.”  
§3.12: “Grouping the 97 INITIAL-sign clusters — the 97 distinct INITIAL signs found among the H+M-covered seals, as defined in §3.7…” followed by the table whose seal counts are “845, 446, 145, 135, 99.”  
**Defect:** The §3.12 seal counts sum to 1,670, i.e. the whole corpus, not the 1,165 “H+M-covered seals” defined in §3.6. Either “H+M-covered seals” is being used with two meanings, or the §3.12 cluster table is not actually restricted to H+M-complete seals as stated.  
Arithmetic: 845 + 446 + 145 + 135 + 99 = 1,670, not 1,165.  
**Severity:** MAJOR  
**What would settle it:** State whether §3.12 is over all seals or only the 1,165 fully H+M-covered seals; if the latter, recompute the table with denominator 1,165.  
**Kind:** (i) defect in what the paper says.

---

### 3. Phase-167 report path is malformed and does not land as printed  
**Quoted passage:** §3.28: “In the Phase-167 record (backend/reports/phase167_meluhhan_names_expanded.jso each name is pre-split into syllable-like segments…”  
**Defect:** The path is missing the expected final “n” in `.json` and lacks a closing parenthesis. As printed, the cross-reference/path is malformed.  
**Severity:** MINOR  
**What would settle it:** Correct the path, presumably to `backend/reports/phase167_meluhhan_names_expanded.json`, and close the parenthesis.  
**Kind:** (i) defect in what the paper says.

---

### 4. HIGH-confidence labels cannot be audited criterion-by-criterion from the paper or the described records  
**Quoted passage:** §2.2: “HIGH (75 signs): Two or more of the following evidence criteria are met.”  
§2.2: “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field…”  
§2.2: “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”  
**Defect:** The paper’s headline category “HIGH” is defined by satisfying two criteria, but the available records as described do not record criterion-level pass/fail status. This is a major audit limitation, though the paper states it explicitly.  
**Severity:** MAJOR  
**What would settle it:** Publish a per-sign criterion matrix showing pass/fail for each §2.2 HIGH criterion, with the underlying counts or coding basis.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 5. The CISI 87.08% cross-corpus figure is uncountable from the paper or records as described  
**Quoted passage:** §3.10: “the Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed…”  
**Defect:** The percentage has no recorded numerator or denominator. This is an arithmetic-audit failure for that figure, disclosed by the paper.  
**Severity:** MAJOR  
**What would settle it:** Provide the numerator, denominator, inclusion rule, and crosswalk used to compute 87.08%.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 6. Phase-143 iconographic enrichment denominator and full tested family cannot be reconstructed from published files  
**Quoted passage:** §3.8: “Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”  
§3.8: “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”  
**Defect:** The multiple-testing denominator and tested family are not reproducible from the paper or published supplement. The paper discloses this.  
**Severity:** MAJOR  
**What would settle it:** Publish the full 394-pair table, the excluded-pair universe, row/column totals, expected counts, and the exact filter implementation.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 7. Key positional permutation statistic cannot be exactly rerun from the record as described  
**Quoted passage:** §2.3: “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”  
§2.3: “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script…”  
**Defect:** The printed z-score arithmetic recomputes, but the underlying statistic and exact permutation run cannot be reproduced from the paper/record alone. The paper discloses this.  
**Severity:** MAJOR  
**What would settle it:** Archive the seed, full shuffle code, inclusion rules, data matrix, and exact observed/null vectors.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 8. V12 vowel-harmony results are internally unresolved, with incompatible pass rates and no authoritative protocol  
**Quoted passage:** §3.17: “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1%…”  
§3.17: “No one of these three procedures is currently the program’s authoritative V12 test: the records disagree because the test was redefined between runs, and the full rule changes are not recorded for every version.”  
**Defect:** The paper contains three incompatible V12 measurements and explicitly says no authoritative rule exists. This prevents a clean internal audit of the V12 claim.  
**Severity:** MAJOR  
**What would settle it:** Freeze one V12 protocol, publish the rule changes and inputs, and rerun it on the current 161-sign set.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 9. Site KL confidence interval method is not identified  
**Quoted passage:** §3.14: “Neither the Phase-151 record nor its script names the interval method (percentile, basic, or bias-corrected), so the printed interval is reported as recorded, without a method name.”  
**Defect:** The CI `[0.483, 0.750]` cannot be methodologically audited from the paper because the bootstrap interval construction is not specified. The paper discloses this.  
**Severity:** MINOR  
**What would settle it:** Name and implement the interval method, or publish the bootstrap resample distribution.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 10. Gulf text-search result cannot be rerun from the record because search terms are absent  
**Quoted passage:** §3.19: “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
**Defect:** The Gulf search claim is not reproducible from the paper or record as described. The paper discloses this.  
**Severity:** MAJOR  
**What would settle it:** Publish the exact term list, text files/versions, extraction method, and the 27-context enumeration.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 11. The four provisional sibilant promotions depend on an incompletely specified proximity-mining rule  
**Quoted passage:** §2.2: “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved.”  
§3.25: “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits in the mined literature…”  
**Defect:** The arithmetic count of hits is printed, but the hit-generation rule is not fully specified, so the four promotions cannot be reproduced from the paper/record alone. The paper discloses this and keeps them provisional.  
**Severity:** MAJOR  
**What would settle it:** Publish the proximity window, OCR sources/versions, disambiguation rules, and per-hit contexts.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 12. Phase-170 grammar retest has an unstated threshold-overlap/tie rule  
**Quoted passage:** §3.31: “The Phase-170 record states the rules in the order TERMINAL, INITIAL, MEDIAL, else MIXED; it does not state what happens when a sign’s rates satisfy more than one threshold, and that tie/overlap handling is not on record.”  
**Defect:** The 137/147 = 93.2% arithmetic recomputes, but the classification rule is incomplete for overlapping thresholds. The paper discloses this.  
**Severity:** MINOR  
**What would settle it:** State the precedence/tie rule and report whether any of the 147 signs hit overlapping thresholds.  
**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

## POSITIVES — arithmetic / internal claims checked and found sound

1. **Site counts sum to the corpus total.**  
   **Passage checked:** §2.1: “Mohenjo-daro (n=606), Harappa (n=492), Kalibangan (n=110), Dholavira (n=106), Lothal (n=124), Chanhu-daro (n=78), Surkotada (n=61), Banawali (n=60), Rakhigarhi (n=33).”  
   **Check:** 606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670.

2. **Catalogue arithmetic is internally consistent.**  
   **Passage checked:** §2.1: “390 distinct M-number signs attested… the additional 7 … have zero corpus tokens…” and “397 catalogue entries carry numbers running from M001 to M416, with 19 numbers unused.”  
   **Check:** 390 + 7 = 397; 416 − 19 = 397.

3. **Headline z-score recomputes from printed inputs.**  
   **Passage checked:** §2.3: “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **Check:** `(0.9916 − 0.4385) / 0.05347 = 10.344`, so 10.3 is correct.

4. **Permutation add-one p estimate recomputes.**  
   **Passage checked:** Abstract and §5: “(0+1)/(2,000+1) = 0.0005.”  
   **Check:** 1 / 2001 = 0.00049975, i.e. 0.0005.

5. **H+M token coverage arithmetic is correct.**  
   **Passage checked:** §3.1: “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”  
   **Check:** 6,369 / 7,002 = 0.9096.

6. **Confidence-table token counts sum correctly.**  
   **Passage checked:** §3.1 table: HIGH 4,925; MEDIUM excluding provisional 1,429; PROVISIONAL_MEDIUM 15; LOW 633.  
   **Check:** 4,925 + 1,429 + 15 + 633 = 7,002. H+M = 4,925 + 1,429 + 15 = 6,369.

7. **Without-provisional coverage arithmetic is correct.**  
   **Passage checked:** §3.1: “without them, 157 anchors cover 6,354 tokens (90.75%).”  
   **Check:** 6,369 − 15 = 6,354; 6,354 / 7,002 = 90.75% after rounding.

8. **SA+DEDR removal bound arithmetic is correct.**  
   **Passage checked:** §2.4: “43 MEDIUM signs, accounting for 398 corpus tokens… If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain.”  
   **Check:** 161 − 43 = 118; 6,369 − 398 = 5,971; 5,971 / 7,002 = 85.28%.

9. **Fish-bearing seal table sums correctly.**  
   **Passage checked:** §3.5 table: Lothal 6, Harappa 33, Mohenjo-daro 35, Dholavira 11, Kalibangan 13, Chanhu-daro 5, Banawali 4, Rakhigarhi 3, Surkotada 3.  
   **Check:** 6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113.

10. **M267 motif and positional counts sum correctly.**  
    **Passage checked:** §3.4: “unicorn 147 tokens, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20, script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens in total…” and “324 … MEDIAL, 59 TERMINAL, and 17 INITIAL.”  
    **Check:** Motif counts sum to 400; positional counts 324 + 59 + 17 = 400. 324 / 400 = 81.0%.

11. **M267 chi-square p-value is consistent with the printed statistic and df.**  
    **Passage checked:** §3.4: “chi-square = 12.98, p = 0.1124, 9 motif categories, 8 degrees of freedom.”  
    **Check:** For χ² = 12.98 with 8 df, the survival probability is about 0.112, matching 0.1124.

12. **Bigram-token count and PMI worked example recompute.**  
    **Passage checked:** §3.7: “5,332 bigram tokens — the corpus’s 7,002 sign tokens minus one for each of its 1,670 inscriptions… P(M342·M176) = 122/5,332, P(M342) = 584/7,002 and P(M176) = 356/7,002, and the printed PMI of 2.43 recomputes…”  
    **Check:** 7,002 − 1,670 = 5,332. PMI = log₂[(122/5332) / ((584/7002)(356/7002))] ≈ 2.43.

13. **Phase-143 percentages and expected false-positive arithmetic check out.**  
    **Passage checked:** §3.8: “63 pairs (16%)…” and “394 × 0.05 = 19.7.”  
    **Check:** 63 / 394 = 15.99%; 394 × 0.05 = 19.7.

14. **Formula semantic clustering table sums correctly, apart from the denominator-label defect noted above.**  
    **Passage checked:** §3.12 table: clusters 51, 25, 6, 9, 6; seals 845, 446, 145, 135, 99.  
    **Check:** Clusters sum to 97; seals sum to 1,670; percentages are correct against 1,670.

15. **Polysemy permutation z-score approximately recomputes.**  
    **Passage checked:** §3.13: “Observed collocate divergence rate: 66.7%… Null distribution mean: 80.7% (SD=0.088). The observed rate is below the null mean (z = −1.6…).”  
    **Check:** (0.667 − 0.807) / 0.088 = −1.59, i.e. −1.6.

16. **V12 printed arithmetic is internally correct.**  
    **Passage checked:** §3.17: “75.3% (Phase-132: 476 of 632…)” and “36.1% (Phase-154: 417 of the 1,154 seals checked passed; 737 seals failed)” and “418 root violations plus 319 boundary violations…”  
    **Check:** 476 / 632 = 75.3%; 417 / 1,154 = 36.1%; 417 + 737 = 1,154; 418 + 319 = 737.

17. **Tamil-Brahmi and V07 percentages recompute.**  
    **Passage checked:** §3.18: “4/7 match (57%)” and “23.4% (270 of 1,154 decoded seals…).”  
    **Check:** 4 / 7 = 57.1%; 270 / 1,154 = 23.4%.

18. **Sibilant provisional-token total matches the coverage table.**  
    **Passage checked:** §3.27: M330 has 3 tokens, M165 2, M202 4, M198 6. §3.1 says the four PROVISIONAL_MEDIUM signs account for 15 tokens.  
    **Check:** 3 + 2 + 4 + 6 = 15.

19. **Blocker-token hypothetical coverage recomputes.**  
    **Passage checked:** §3.29: “M270 (6 tokens) and M386 (6); and, at 5 tokens each, [17 signs] — 97 tokens in total… 6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”  
    **Check:** 6 + 6 + 17×5 = 97; 6,369 + 97 = 6,466; 6,466 / 7,002 = 92.35%.

20. **Phase-170 retest percentage recomputes.**  
    **Passage checked:** §3.31: “137/147 signs (93.2%).”  
    **Check:** 137 / 147 = 93.20%.

21. **Abstract/conclusion echo of the fish-sign caveat matches the body.**  
    **Passage checked:** Abstract: “That count is not fish-specific evidence: the corpus contains no single-sign inscriptions of any kind…”  
    §3.5: “the corpus contains no single-sign inscriptions of any kind… so no sign — fish or otherwise — can be isolated in it…”  
    §5: “a count that follows from the corpus’s containing no single-sign inscriptions at all, and so is not a fish-specific pattern…”  
    **Check:** The qualification is preserved consistently.

22. **Abstract/conclusion echo of “coverage means assignment, not verification” matches the body.**  
    **Passage checked:** Abstract: “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
    §5: “90.96% token coverage — assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings.”  
    **Check:** No strengthening found in the echo; the limitation is repeated.

CALL-META pass1: finish_reason=stop; max_completion_tokens=48000; completion_tokens=12106; prompt_tokens=31959; output_chars=17651.

## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

## Red-team pass (paper text only)

I reviewed only the supplied preprint text. I did not inspect the repository, DOI, corpus, phase records, or cited works.

---

## Findings

### 1. Corpus-level results are not independently reproducible from the paper because the primary corpus is private

**(a) Quoted passage — Abstract / §6 Data Availability**

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
>  
> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”  
>  
> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect / limitation**

Most headline numerical claims — token coverage, seal coverage, positional statistics, fish counts, motif distributions, bigram counts, site divergences — depend on a corpus unavailable to readers. This is a severe reproducibility limitation. The paper does disclose it at the same strength.

**(c) Severity**

CRITICAL

**(d) What would settle it**

Public release of the Holdat corpus with sign sequences, site/object metadata, motif metadata, and inclusion/exclusion rules; or a complete rerun on a public corpus with crosswalks and scripts.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 2. The representativeness claim for the private corpus is stronger than the paper’s evidence allows

**(a) Quoted passage — §2.1 Corpus**

> “Primary corpus: Holdat LLC Indus Corpus v3 (Miller 2025). 7,002 sign tokens, 1,670 seals, 9 sites: Mohenjo-daro (n=606), Harappa (n=492), Kalibangan (n=110), Dholavira (n=106), Lothal (n=124), Chanhu-daro (n=78), Surkotada (n=61), Banawali (n=60), Rakhigarhi (n=33). Sign encoding: Mahadevan M-numbers. This corpus covers the major excavated IVC sites and represents the primary published formal-seal assemblage.”

**(b) Defect / limitation**

The paper asserts that the private corpus “represents the primary published formal-seal assemblage,” but gives no inclusion criteria, exclusion criteria, object list, source concordance, or comparison to the full published assemblage. Because the corpus is private, the representativeness claim cannot be checked from the paper.

**(c) Severity**

MAJOR

**(d) What would settle it**

A published corpus manifest: object IDs, source publications, inclusion/exclusion rules, site/object-type coverage, and comparison against known published catalogues.

**Kind**

(i) defect in what the paper says.

---

### 3. The HIGH label is defined by criteria that the paper later admits cannot be verified sign-by-sign from the records

**(a) Quoted passage — §2.2 Evidence Hierarchy**

> “HIGH (75 signs): Two or more of the following evidence criteria are met.”  
>  
> “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field…”  
>  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect / limitation**

The paper defines HIGH as satisfying “two or more” specified criteria, but then says neither the paper nor the audit file allows a reader to verify that any particular HIGH sign actually satisfies those criteria as worded. That makes the HIGH label operationally unverifiable from the stated evidence record.

**(c) Severity**

CRITICAL

**(d) What would settle it**

A per-sign criterion matrix with explicit pass/fail values for each §2.2 criterion, including underlying counts, motif denominators, positional rates, iconographic coding, and decision rules.

**Kind**

(i) defect in what the paper says.

---

### 4. The selected HIGH examples include labels whose displayed evidence does not itself meet the stated HIGH criteria

**(a) Quoted passage — §3.3 Selected High-Confidence Readings**

> “M176’s printed terminal figure — 94% of its 356 tokens inscription-final — does not by itself meet §2.2’s terminal-marker criterion (>95%); its HIGH status rests on the audit’s recorded evidence pair, stated here so that a reader applying §2.2 to this table alone is not misled.”  
>  
> “The audit’s two types are recorded as types, not scored criterion by criterion, and they do not map one-to-one onto the three criteria named in §2.2.”

**(b) Defect / limitation**

The paper presents M176 as HIGH while acknowledging that the quantitative terminal evidence printed for it fails the stated terminal criterion, and that the audit evidence types do not map one-to-one onto the formal criteria. This is an internal evidentiary mismatch between the label and the displayed criteria.

**(c) Severity**

MAJOR

**(d) What would settle it**

A full criterion-by-criterion audit for M176 and all HIGH signs, showing which two §2.2 criteria each sign satisfies.

**Kind**

(i) defect in what the paper says.

---

### 5. The DEDR rebus-matching procedure lacks the information needed to estimate chance matches or multiple-comparison risk

**(a) Quoted passage — §2.2 Evidence Hierarchy**

> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect / limitation**

A major part of the reading evidence depends on DEDR rebus matches, but the search space, rejected candidates, transformation rules, and multiple-comparison controls are absent. The paper itself states this at full strength.

**(c) Severity**

MAJOR

**(d) What would settle it**

A pre-specified DEDR matching protocol, full candidate/rejection logs per sign, allowed sound-correspondence rules, and null simulations estimating false-positive rates across the sign inventory.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 6. The SA route remains in the MEDIUM evidence system despite the paper’s own held-out test finding SA agreement uninformative

**(a) Quoted passage — §2.4 Syllabic Language Model**

> “Signs with SA consistency >= 0.15 and a DEDR entry matching the modal reading were promoted to MEDIUM.”  
>  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”  
>  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”  
>  
> “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect / limitation**

The paper continues to count 43 SA+DEDR signs inside the MEDIUM headline set even though its own held-out test says SA agreement “carries no information” by itself, and the DEDR matching risk is also uncalibrated. Unless DEDR alone is shown sufficient for those signs, the MEDIUM label is stronger than the paper’s own evidence supports.

**(c) Severity**

MAJOR

**(d) What would settle it**

A calibrated SA validation on known scripts; a DEDR-only audit showing which of the 43 signs independently meet a non-SA MEDIUM criterion; and a recomputed headline excluding unsupported SA-dependent promotions.

**Kind**

(i) defect in what the paper says.

---

### 7. The four PROVISIONAL_MEDIUM promotions are counted in headline coverage despite incomplete generation rules and unverified text-proximity evidence

**(a) Quoted passage — §2.2 Evidence Hierarchy / §3.25**

> “PROVISIONAL_MEDIUM readings are included within the MEDIUM count for coverage accounting but are flagged for expert review before any HIGH-confidence promotion.”  
>  
> “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded…”  
>  
> “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign”

**(b) Defect / limitation**

The four provisional signs are included in the headline MEDIUM count and token coverage, although their promotion rule is partly undocumented and the hits are explicitly not verified sign assignments. The paper discloses this limitation and gives coverage without them.

**(c) Severity**

MAJOR

**(d) What would settle it**

A fully specified text-mining protocol, archived OCR sources, proximity windows, ambiguity rules, hand verification of each hit, and expert review of the four assignments.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 8. The headline positional statistic is arithmetically checkable but not independently reproducible from the paper

**(a) Quoted passage — §2.3 Positional Analysis**

> “The headline positional statistic (z = 10.3) comes from the Phase-134 F1 test.”  
>  
> “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”  
>  
> “The Phase-134 JSON record reports the statistic’s inputs and outputs … but not the data matrix, and this section does not reproduce the script’s procedure.”  
>  
> “the fit itself can be re-run only from the script and the corpus.”

**(b) Defect / limitation**

The reported z-score can be recomputed from printed summary numbers, but the underlying fit and permutation cannot be reproduced from the paper, and exact rerun is impossible from the record as described. The paper discloses this.

**(c) Severity**

MAJOR

**(d) What would settle it**

Public corpus, data matrix, exact script, inclusion rules, random seed, and permutation outputs.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 9. The three-slot grammar’s semantic interpretation is not tested against rival non-linguistic or administrative templates

**(a) Quoted passage — §3.2 Grammar Model**

> “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics…”  
>  
> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**(b) Defect / limitation**

The positional regularity may be real, but the semantic labels “classifier,” “title,” and “name/case” are not established by the positional tests and have not been tested against plausible rival templates. The paper discloses this at the same strength.

**(c) Severity**

MAJOR

**(d) What would settle it**

Explicit rival models with discriminating predictions, fitted to the same corpus and compared by pre-specified metrics.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 10. The fish-sign isolation result is not fish-specific because the corpus contains no single-sign inscriptions of any kind

**(a) Quoted passage — Abstract / §3.5 Fish Sign Isolation Test**

> “That count is not fish-specific evidence: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9), so no sign of any family can occur isolated in it…”  
>  
> “One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind … so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result…”  
>  
> “What the count establishes is only that fish signs occur in this corpus in multi-sign inscriptions — as every sign in this corpus does.”

**(b) Defect / limitation**

The fish-sign isolation count cannot support a fish-specific rule in this corpus. The paper states this honestly and repeatedly.

**(c) Severity**

MAJOR

**(d) What would settle it**

A corpus or object class containing single-sign inscriptions, allowing fish signs and non-fish signs to be compared for isolation rates.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 11. The iconographic enrichment test uses a data-selected family of tested pairs and lacks the full published pair table

**(a) Quoted passage — §3.8 Iconographic Cross-Encoding**

> “Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”  
>  
> “The supplemental file iconographic_formula_pairs.csv contains the 15 strongest enriched pairs … it is not the full 394-pair table…”  
>  
> “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”  
>  
> “for signs whose reading was itself suggested by the animal motif, ‘the reading matches the animal’ is circular and is not claimed here as validation.”

**(b) Defect / limitation**

The enrichment analysis is post-filtered on attested pairs, the full tested family is not published, the Bonferroni denominator is not the full possible test family, and some associations are circular with respect to reading assignment. The paper discloses these limits.

**(c) Severity**

MAJOR

**(d) What would settle it**

Publication of the full pair table, pre-specified test family including zero cells, complete 2×2 statistics, and separation of discovery data from validation data.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 12. The Tamil-Brahmi terminal comparison cannot validate readings and uses an uncited working inventory

**(a) Quoted passage — §3.18 Tamil-Brahmi Terminal Comparison**

> “Testing these against the Tamil-Brahmi epigraphy terminal phoneme inventory (11 categories…): 4/7 match (57%). No published source for that 11-category inventory is cited in this paper or in the Phase-155 record; the inventory is the test’s own working list…”  
>  
> “Tamil-Brahmi is roughly two thousand years later than the Indus material, so agreement can show only that the proposed endings are of kinds later attested in Dravidian epigraphy — it cannot validate the readings…”  
>  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% … concentrated in high-frequency signs… three of them headline signs of this model.”

**(b) Defect / limitation**

The comparison is temporally remote, uses an uncited inventory, has only 4/7 strict matches, and coexists with a substantial phonotactic violation rate in headline signs. The paper discloses this.

**(c) Severity**

MAJOR

**(d) What would settle it**

A sourced terminal inventory, pre-specified matching rules, comparison to rival language baselines, and resolution of V07 violations.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 13. Literature-mining comparisons are not reproducible from a re-runnable specification and have unmeasured recall/precision

**(a) Quoted passage — §3.24 / §7 AI Disclosure**

> “That is a null result for this search method only: its recall has never been measured against a hand-checked list of known proposals…”  
>  
> “AI tooling was used for scripting, data management, and literature search — including the text-mining counts reported in §§3.21–3.24 and the text-proximity hits behind the four PROVISIONAL_MEDIUM promotions (§2.2).”  
>  
> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24).”  
>  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect / limitation**

The literature-mining evidence is not reproducible from a complete specification and its recall/precision are unknown. The paper discloses this at the same strength.

**(c) Severity**

MAJOR

**(d) What would settle it**

Archived source texts/OCR, exact prompts/models/settings, deterministic scripts, full hit lists, hand-coded validation set, and measured recall/precision.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 14. The “Tier 2” conclusion for the 161 readings is stronger than the paper’s own adverse evidence permits

**(a) Quoted passage — §5 Conclusion**

> “The tier labels used in this conclusion are this program’s claim-audit labels … Tier 2 means a probable linguistic interpretation — supported, not proven…”  
>  
> “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage …) are Tier 2 claims supported by multiple tests.”  
>  
> “Those tests are not independent of each other — most are computed from the same corpus, and several from the same seals (§2.2) — the HIGH/MEDIUM labels are rule-based categories with no measured error rate, and the set also carries the unresolved V12 warning and the 23.4% V07 phonotactic violation rate (§§3.17–3.18) — a rate concentrated in high-frequency headline signs … The readings have not yet been externally reviewed.”

**(b) Defect / limitation**

Calling the 161 readings “Tier 2” and defining Tier 2 as “probable linguistic interpretation” overstates the paper’s own evidence. The same sentence cluster admits non-independent tests, no measured error rates, unresolved vowel-harmony warnings, a 23.4% phonotactic violation rate concentrated in headline signs, and no external review. Those conditions do not justify “probable” for the reading set as a whole.

**(c) Severity**

CRITICAL

**(d) What would settle it**

Independent expert review; calibrated false-positive rates for confidence labels; resolution of V07/V12; validation on an independent corpus; and formal comparison to rival language/non-language baselines.

**Kind**

(i) defect in what the paper says.

---

### 15. The conclusion’s “favours Proto-Dravidian” claim is stronger than the paper’s own discriminative evidence

**(a) Quoted passage — §4.4 Limitations / §5 Conclusion**

> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”  
>  
> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”  
>  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

**(b) Defect / limitation**

The paper itself says the existing comparisons are mixed and that formal comparison against major rival baselines is necessary before the interpretation can be discriminative. The conclusion’s “favours a Proto-Dravidian reading framework” is therefore stronger than “compatible with Proto-Dravidian,” which is the strength supported by the disclosed evidence.

**(c) Severity**

CRITICAL

**(d) What would settle it**

A pre-registered or otherwise fixed comparative test against Proto-Dravidian, Proto-Munda, early Indo-Aryan, Sanskrit, and language-neutral baselines, with clear discriminative metrics and held-out validation.

**Kind**

(i) defect in what the paper says.

---

### 16. The “falsifiable” framing is only partly satisfied; the paper’s own validation path says key tests are not currently open or not discriminating

**(a) Quoted passage — Title / §4.5 Validation Path**

> “A Falsifiable Computational Decipherment Hypothesis…”  
>  
> “The candidate model is falsifiable in principle at the first of the following points. None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”  
>  
> “Radiocarbon-dated stratigraphic contexts: a future test of this kind could separate the guild-identity interpretation from the commodity-tally model only if the two are first made to predict different things…”  
>  
> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**(b) Defect / limitation**

The title foregrounds falsifiability, but the paper’s own validation section says the listed tests are not currently runnable on available data, one has already failed to confirm, and one lacks a discriminating prediction. The model may be falsifiable in principle, but the present paper has not supplied a complete current falsification protocol for important semantic claims.

**(c) Severity**

MAJOR

**(d) What would settle it**

Explicit, pre-specified falsification tests runnable on existing data, plus discriminating predictions separating guild, ownership, commodity, clan, cultic, and non-linguistic models.

**Kind**

(i) defect in what the paper says.

---

### 17. The data-availability claim that repository artefacts can be “re-run and checked” is too broad for several components

**(a) Quoted passage — Abstract / §6 / §7 AI Disclosure**

> “This study … proposes a falsifiable computational model whose method and repository artefacts (scripts, phase reports, and the anchor table) can be re-run and checked.”  
>  
> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released…”  
>  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”  
>  
> “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

**(b) Defect / limitation**

The paper’s broad statement that method and artefacts “can be re-run and checked” is not true for corpus-level counts, exact permutation reruns, and AI/text-mining steps as described. The paper contains the caveats, but the broad claim is stronger than them.

**(c) Severity**

MAJOR

**(d) What would settle it**

Release of corpus data, exact seeds and scripts, full data matrices, archived AI model/prompt/settings, and deterministic re-run instructions.

**Kind**

(i) defect in what the paper says.

---

### 18. The M267 motif-independence test is token-level while the relevant motif property is seal-level

**(a) Quoted passage — §3.4 Major Correction: M267 Is Not the Fish Sign**

> “Its distribution across seal motifs does not differ significantly from the counts expected if its 400 tokens were spread across the nine motif types in proportion to each type’s overall share (chi-square = 12.98, p = 0.1124…”  
>  
> “One limit of this test belongs on the record: the chi-square treats M267’s 400 tokens as independent observations, but a motif is a property of a seal, not of a token. The Phase-132 record does not state how many distinct seals the 400 tokens occur on, and no seal-level version of this test is on record, so the printed p-value should be read as a token-level result whose seal-level strength has not been measured.”

**(b) Defect / limitation**

The p-value supporting motif-independence is not a seal-level test, even though motifs belong to seals. The paper discloses this, so the limitation is not hidden.

**(c) Severity**

MAJOR

**(d) What would settle it**

A seal-level contingency analysis using distinct seals rather than token counts, including seals with multiple M267 occurrences handled appropriately.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 19. The site-divergence result for Rakhigarhi rests on a small sample and only one pair has a confidence interval

**(a) Quoted passage — §3.14 Site Repertoire Divergence Bootstrap**

> “Bootstrap confidence intervals (n=1,000 resamples) were computed for the most divergent pair only.”  
>  
> “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site, so its distinctiveness should be read as a measured difference on a small sample, not as proof that the difference is not a small-sample effect.”  
>  
> “no confidence intervals for those pairs are on record…”

**(b) Defect / limitation**

The Rakhigarhi distinctiveness claim is descriptive and sample-limited; it is not robustly interval-tested across all relevant pairs. The paper discloses this.

**(c) Severity**

MINOR

**(d) What would settle it**

More Rakhigarhi data, confidence intervals for all site pairs, and sensitivity analyses for sampling and object-type composition.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

### 20. The master evidence synthesis is not independently interpretable because it mixes internal consistency and external evidence under program-defined labels

**(a) Quoted passage — §3.30 Master Evidence Synthesis**

> “Results: 32 total evidence items … in the Phase-169 record’s own categories…”  
>  
> “These ratings are assigned by this program, on labels defined by this program…”  
>  
> “The items mix two different kinds of check — internal consistency checks (which can show the model agrees with itself) and external comparisons (which can test it against something outside) — and only the second kind is evidence about the world.”  
>  
> “The full per-item list, with each item’s label, is in the Phase-169 record … it is not printed in this paper…”

**(b) Defect / limitation**

The 32-item synthesis is not assessable from the paper and mixes internal self-consistency with external evidence. The paper discloses this and withdraws the earlier aggregate confidence score.

**(c) Severity**

MAJOR

**(d) What would settle it**

Print or archive the full item list with definitions, classify internal vs external separately, and avoid aggregate evidence claims unless weights and validation are specified.

**Kind**

(ii) limitation the paper itself already discloses at the same strength.

---

## Positives checked

### P1. The z-score arithmetic is internally consistent

**Passage checked — §2.3**

> “observed 𝑅2 = 0.9916, null mean 0.4385, standard deviation 0.05347”  
> “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

**Check**

The arithmetic is correct: \((0.9916 - 0.4385) / 0.05347 ≈ 10.34\).

---

### P2. The headline token-coverage arithmetic is internally consistent

**Passage checked — §3.1**

> “HIGH … 70.34% (4,925 tokens)”  
> “MEDIUM … 20.62% (1,444 tokens)”  
> “LOW … 9.04% (633 tokens)”  
> “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”

**Check**

4,925 + 1,444 = 6,369.  
6,369 / 7,002 ≈ 90.96%.  
6,369 + 633 = 7,002.

---

### P3. The paper adequately distinguishes assignment coverage from verified decipherment

**Passage checked — Abstract / §5**

> “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
>  
> “90.96% token coverage — assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings”

**Check**

This is an important and correctly stated disclosure.

---

### P4. The paper correctly refuses to treat the fish-isolation count as fish-specific evidence

**Passage checked — Abstract / §3.5**

> “That count is not fish-specific evidence…”  
>  
> “so no sign — fish or otherwise — can be isolated in it”  
>  
> “What the count establishes is only that fish signs occur in this corpus in multi-sign inscriptions — as every sign in this corpus does.”

**Check**

This is internally sound and prevents a common overclaim.

---

### P5. The paper correctly withdraws or downgrades several earlier claims instead of preserving inflated claims

**Passage checked — §3.1 / §3.4 / §3.17 / §3.30**

> “a prior count of 268 included 107 heuristic placeholder assignments removed by Phase-133.”  
>  
> “Counts printed in earlier drafts … are withdrawn”  
>  
> “we withdraw the earlier description of V12 as a settled methodology artifact”  
>  
> “the earlier draft’s ‘79.8% aggregate confidence score’ is withdrawn”

**Check**

The paper is unusually explicit about corrected errors and withdrawn claims.

---

### P6. The Parpola-overlap claim is appropriately limited

**Passage checked — §3.22**

> “44/75 HIGH-confidence readings appear in Parpola’s text (59%). This is not independent cross-validation…”  
>  
> “the count records appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”

**Check**

The paper states the result at the proper limited strength.

---

### P7. The Phase-170 grammar retest is correctly characterized as self-consistency, not accuracy

**Passage checked — §3.31**

> “This is a self-consistency check, not an accuracy measurement…”  
>  
> “It is not comparable to Phase-133’s figures…”  
>  
> “The evidential weight for the grammar model rests on the Phase-134 permutation and held-out tests, not on this retest.”

**Check**

This is an adequate disclosure of the retest’s evidentiary limits.

---

### P8. The frequency-curve evidence is correctly treated as uninformative

**Passage checked — §2.1.1**

> “Under the rule fixed before the run, that result makes the comparison UNINFORMATIVE…”  
>  
> “these measures do not separate the one certain writing system from systems that are not writing, so a close Indus fit on them is evidence neither for nor against the script being language.”

**Check**

The paper does not overclaim from Zipf/frequency-curve fits and states the negative result clearly.

CALL-META pass2: finish_reason=stop; max_completion_tokens=48000; completion_tokens=10587; prompt_tokens=31961; output_chars=31183.

## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

## PASS 3 — Methods & Reproducibility Audit Findings

### 1. §6 sentence audit: repository availability claim cannot be checked from the paper and is partly overbroad

**(a) Quote (§6 Data Availability):**  
“All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit b28cf2f5).”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**. The paper gives a repository URL and commit, but the preprint text itself does not contain the repository contents, scripts, phase reports, or tables. Also, “the version of the paper you are reading is on … commit b28cf2f5” is later qualified by the claim that the draft in hand differs from that commit by one commit string, so the sentence is not literally true without the later qualification.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A publicly accessible immutable archive or successful checkout of `preprint-v8-f2-spec068` at `b28cf2f5`, showing the paper text and all named files.

**Kind:** (i) defect in what the paper says.

---

### 2. §6 sentence audit: DOI/version-record claim is plausible but not checkable from the paper text

**(a) Quote (§6 Data Availability):**  
“The DOI named on the title page identifies this preprint and its version record on Zenodo.”

**(b) Defect:**  
Literal-truth verdict: **not checkable from the paper alone**. The paper supplies the DOI, but no Zenodo metadata or version record is included in the text.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Access to the DOI landing page showing the preprint and version record.

**Kind:** (i) defect in what the paper says.

---

### 3. §6 sentence audit: branch/commit plus “one-string difference” version identity is inherently awkward and not independently verifiable

**(a) Quote (§6 Data Availability):**  
“The text of this draft is identified by the branch and commit named here, together with the one-string difference explained below, not by the DOI.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**. The paper defines the identity of the draft partly by a commit that allegedly does not itself contain the exact text. That can be made coherent, but the paper gives no hash for the later “pin commit” that allegedly contains the exact string update.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A named immutable commit hash or archival release for the exact text being reviewed.

**Kind:** (i) defect in what the paper says.

---

### 4. §6 sentence audit: supplemental-file availability is not independently verifiable and lacks archive redundancy

**(a) Quote (§6 Data Availability):**  
“The supplemental files named in this paper (the anchor table, the status audit, and the CSV supplements in research/indus/supplemental/) are in the same repository at the same commit; no separate archive copy of them exists yet.”

**(b) Defect:**  
Literal-truth verdict: **not checkable from the paper alone**. The lack of a separate archive is honestly disclosed, but it is a reproducibility weakness: if the repository changes, disappears, or the branch is moved, the supplements are not independently preserved by the paper’s own account.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
An immutable release archive containing the exact supplemental files, preferably tied to the DOI.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 5. §6 sentence audit: “revision commit” role is asserted, not demonstrated

**(a) Quote (§6 Data Availability):**  
“The commit named here is the revision commit: the commit at which this paper’s text was frozen for the current round.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**, and it conflicts in practice with the later statement that the draft in hand differs from the text at that commit in one string.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A visible repository history showing `b28cf2f5` and the exact paper file contents at that commit.

**Kind:** (i) defect in what the paper says.

---

### 6. §6 sentence audit: self-referential commit-hash explanation is logically plausible but depends on unseen repository history

**(a) Quote (§6 Data Availability):**  
“A commit cannot contain its own hash, so the copy of this section at the named commit names, in its first sentence, the commit that the revision started from.”

**(b) Defect:**  
Literal-truth verdict: **logically plausible**, but **not verifiable from the paper alone**. The paper asks the reader to trust a precise repository-history claim without printing the prior commit hash or showing the diff.

**(c) Severity:** MINOR

**(d) What would settle it:**  
The prior commit hash and a diff showing that the only relevant difference is the commit-string update.

**Kind:** (i) defect in what the paper says.

---

### 7. §6 sentence audit: exact-text identity claim is impossible to verify from the paper and needs a diff

**(a) Quote (§6 Data Availability):**  
“The draft in hand differs from the text at the named commit in that one commit string, and in no other sentence.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**. This is a precise text-identity claim, but the paper does not provide the text at the named commit or a diff.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A machine-readable diff between the draft in hand and `b28cf2f5`.

**Kind:** (i) defect in what the paper says.

---

### 8. §6 sentence audit: unnamed “pin commit” defeats exact reproducibility

**(a) Quote (§6 Data Availability):**  
“The commit that follows the named commit on this branch and changes that string — the pin commit — changes no other paper text, and the records commits that follow it (the rebuilt PDF, the version note, and the records of later rounds) change no paper text at all.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable and under-specified**. The paper does not name the “pin commit” hash. Branches are mutable; “the commit that follows” is not a stable identifier unless the commit hash is given.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
The pin commit hash, an immutable tag/release, and diffs for the pin and subsequent “records commits.”

**Kind:** (i) defect in what the paper says.

---

### 9. §6 sentence audit: central evidence tables are not printed, so claims depend on external files

**(a) Quote (§6 Data Availability):**  
“The anchor table is research/indus/anchor_table.csv: it has 397 rows — one for every sign in the Mahadevan catalogue — of which 161 are the HIGH/MEDIUM rows this paper’s headline claims rest on and the other 236 carry LOW readings; each row gives the sign’s reading and basis, and a DEDR citation is recorded in the table’s DEDR column on 15 rows, all of them among the 161; the full 397-sign inventory, with each sign’s status and corpus frequency, is glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv; per-phase results are in backend/reports/.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**. This sentence identifies crucial evidence files but does not print them. The paper’s headline claims rest on tables the reader cannot inspect from the paper text.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publication of the complete tables in an immutable supplement, or inclusion of enough table content in the paper to audit the headline claims.

**Kind:** (i) defect in what the paper says.

---

### 10. §6 sentence audit: non-printing of core evidence is openly disclosed

**(a) Quote (§6 Data Availability):**  
“Neither table is printed in this paper; both are in the repository, on the branch and at the commit named above.”

**(b) Defect:**  
Literal-truth verdict: **the limitation is honestly disclosed**. The defect for reproducibility is that the paper itself cannot be audited without the repository.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A stable archived supplement containing both tables.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 11. §6 sentence audit: paper admits the tables are central evidence but does not include them

**(a) Quote (§6 Data Availability):**  
“Both tables are the paper’s central evidence.”

**(b) Defect:**  
Literal-truth verdict: **internally coherent**, but it intensifies the reproducibility problem: the central evidence is not in the paper and depends on external repository access.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Archival deposition and complete publication of the two tables.

**Kind:** (i) defect in what the paper says.

---

### 12. §6 sentence audit: selected evidence rows are expressly illustrative only

**(a) Quote (§6 Data Availability):**  
“Selected rows from the anchor evidence are printed in this paper — in §3.3 and in Appendix A — as illustrations only; the complete tables are printed nowhere in this paper and are in the repository.”

**(b) Defect:**  
Literal-truth verdict: **the limitation is honestly disclosed**. The printed examples cannot support a sign-by-sign audit of the model.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Complete table publication in the paper or immutable supplement.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 13. §6 sentence audit: readers are directed outside the paper for any single-reading check

**(a) Quote (§6 Data Availability):**  
“A reader who wants to check any single reading should go to the anchor table itself, at the commit named in §6, rather than to the examples in §3.3.”

**(b) Defect:**  
Literal-truth verdict: **the paper openly admits its examples are insufficient**. This is a reproducibility limitation because the paper cannot substantiate even an individual reading without the external table.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Full anchor table in an immutable public supplement.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 14. §6 sentence audit: private corpus blocks corpus-level reproducibility

**(a) Quote (§6 Data Availability):**  
“The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**(b) Defect:**  
Literal-truth verdict: **clear disclosed limitation**. This is a critical reproducibility blocker because most quantitative claims are corpus-level.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Public release of the Holdat corpus, or a fully specified public substitute plus crosswalk and rerun outputs.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 15. §6 sentence audit: full reproduction requires unavailable corpus or nontrivial crosswalking

**(a) Quote (§6 Data Availability):**  
“Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect:**  
Literal-truth verdict: **clear disclosed limitation**. The paper’s corpus-level counts are not reproducible by an ordinary reader from the paper and public materials alone.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Public corpus release, agreement-access route with documented terms, or a public rerun on a specified compatible corpus with the crosswalk supplied.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 16. §6 sentence audit: supplemental datasets are named but not sufficient for rerunning corpus-level claims

**(a) Quote (§6 Data Availability):**  
“Supplemental datasets (fish-sign compound-context listing, iconographic formula enrichment table, formula bigram table, and positional grammar permutation summary) are available in research/indus/supplemental/.”

**(b) Defect:**  
Literal-truth verdict: **not verifiable from the paper alone**, and even if true, these supplements do not replace the missing corpus needed to rerun corpus-level counts.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Public archived supplements plus the underlying corpus or sufficient derived data matrices to reproduce each statistic.

**Kind:** (i) defect in what the paper says.

---

### 17. The private corpus makes most denominators and selection rules non-auditable

**(a) Quote (§2.1 Corpus):**  
“Primary corpus: Holdat LLC Indus Corpus v3 (Miller 2025). 7,002 sign tokens, 1,670 seals, 9 sites … This corpus covers the major excavated IVC sites and represents the primary published formal-seal assemblage.”

**(b) Defect:**  
The paper gives corpus totals and site counts but not the inclusion/exclusion rules for objects, duplicate handling, inscription direction handling, broken signs, uncertain signs, or how “primary published formal-seal assemblage” was operationalized. Since the corpus is private, these denominators cannot be independently checked.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Public corpus release with object-level metadata and explicit inclusion/exclusion criteria.

**Kind:** (i) defect in what the paper says.

---

### 18. Phase-134 permutation test cannot be exactly rerun because seed and shuffling inclusion rules are missing

**(a) Quote (§2.3 Positional Analysis):**  
“The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

**(b) Defect:**  
The paper itself admits exact rerun is impossible from the record. For the headline statistic, missing random seed and inclusion rules are a serious reproducibility defect.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
The exact script, seed, input matrix, and inclusion/exclusion rules used for the 2,000 permutations.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 19. Phase-134 statistic definition is delegated to an external script, not specified in the paper

**(a) Quote (§2.3 Positional Analysis):**  
“The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script (backend/scripts/phase134_falsification_suite.py). … this section does not reproduce the script’s procedure.”

**(b) Defect:**  
The paper’s headline `z = 10.3` statistic is not fully defined in the paper. A reader can check the arithmetic from printed inputs but not the construction of the fitted statistic.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A full mathematical definition of the fitted model, observations, weighting, length handling, and permutation procedure in the paper or supplement.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 20. The HIGH-confidence criteria cannot be reapplied from the paper or audit file

**(a) Quote (§2.2 Evidence Hierarchy):**  
“A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect:**  
The paper’s HIGH label is not reproducible criterion-by-criterion. The audit records broad evidence-type pairs rather than pass/fail fields for the actual criteria.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A sign-by-sign matrix listing every §2.2 criterion, input counts, thresholds, and pass/fail decision.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 21. DEDR rebus matching lacks candidate universe, rejection record, transformation rules, and multiple-testing control

**(a) Quote (§2.2 Evidence Hierarchy):**  
“For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”

**(b) Defect:**  
The DEDR matching procedure is not reproducible as a statistical search and has no reported false-positive control despite a large search space.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
A pre-specified candidate-generation protocol, full rejected-candidate logs, allowed sound transformations, and a null/multiple-testing analysis.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 22. SA model training data are unreconstructable

**(a) Quote (§2.4 Syllabic Language Model):**  
“No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

**(b) Defect:**  
The SA simulation cannot be rerun or evaluated because the training corpus, inventory source, and training size are unspecified.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Training corpus identity, version, preprocessing, syllable inventory, size, model code, parameters, and seed.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 23. SA consistency score is undefined at the operational level

**(a) Quote (§2.4 Syllabic Language Model):**  
“One part of the SA+DEDR criterion cannot be reconstructed from our records: the ‘consistency’ score is described in the Phase-52 lineage as the fraction of a sign’s contexts agreeing on its modal reading, but no record defines how a context is delimited, how contexts are weighted, or how ties are handled.”

**(b) Defect:**  
A promotion criterion for MEDIUM signs is not operationally defined. This blocks independent recomputation and sensitivity analysis.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A formal definition of context delimitation, weighting, tie handling, and exact implementation.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 24. Phase-107 undermines SA as evidence, yet SA+DEDR remains in the headline set

**(a) Quote (§2.4 Syllabic Language Model):**  
“Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value. … 43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect:**  
The paper retains 43 SA+DEDR MEDIUM signs in the headline count while admitting the SA machinery failed a held-out discrimination test. The paper gives only a removal bound, not a recomputed SA-free headline.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A fully recomputed headline excluding SA-dependent signs, or an independently validated SA model.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 25. Text-proximity promotions lack proximity-window, OCR, and ambiguity-resolution specifications

**(a) Quote (§2.2 Evidence Hierarchy):**  
“The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved.”

**(b) Defect:**  
The four PROVISIONAL_MEDIUM promotions based on text proximity cannot be reproduced from a complete rule.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Exact OCR inputs, versions, proximity windows, search terms, ambiguity rules, and hit lists.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 26. Iconographic and motif-exclusivity criteria lack coding protocol and denominators

**(a) Quote (§2.2 Evidence Hierarchy):**  
“Three of the criteria above are stated at the level this program’s records support and no further: the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record; ‘cases’ in the terminal-marker criterion means the sign’s corpus tokens; and the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table.”

**(b) Defect:**  
Key criteria for confidence labels depend on subjective or unpublished coding and unpublished denominators.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Published coding manual, blinded independent coding, inter-coder reliability, and motif-denominator table.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 27. Substrate-analysis selection set is not printed and no substrate-match standard was fixed

**(a) Quote (§2.5 Substrate Analysis):**  
“For signs resisting Dravidian decipherment (25 signs, Phase-123 — the 25 are listed in the Phase-123 record, outputs/phase123_munda_substrate.json, and are not printed in this paper)…”  
and  
“No general standard for what counts as a substrate match was fixed in advance; substrate proposals are therefore reported in this paper as proposals, not as a promotion route.”

**(b) Defect:**  
The substrate analysis cannot be audited from the paper: the 25-sign set is external, and the match standard was not pre-specified.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Printed 25-sign list, fixed substrate-match criteria, source vocabularies, and rejection records.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 28. Fish-family classification lacks per-sign published support

**(a) Quote (§3.5 Fish Sign Isolation Test):**  
“The fish-family list printed above is the family’s citable form; no record gives a published page or figure for each sign’s fish-shaped classification in the crosswalk, and none is claimed here.”

**(b) Defect:**  
The fish-family inclusion rule cannot be externally checked sign-by-sign from cited iconographic sources.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Per-sign citations to catalogue figures/pages or an explicit coding protocol.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 29. Fish-sign isolation test has a degenerate denominator because the corpus has no single-sign inscriptions

**(a) Quote (§3.5 Fish Sign Isolation Test):**  
“One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result.”

**(b) Defect:**  
The fish-isolation test cannot test fish-specific isolation. It is a restatement of a corpus-wide property.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A corpus containing single-sign inscriptions, with fish and non-fish signs compared under the same rules.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 30. Phase-143 iconographic enrichment family is selected from the data and full tested table is unpublished

**(a) Quote (§3.8 Iconographic Cross-Encoding):**  
“Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”  
and  
“the full table — including the 63 enriched pairs and the pairs that were not enriched — exists only in the Phase-143 record’s working outputs, not as a published file.”

**(b) Defect:**  
The multiple-testing family is data-selected and the full tested universe is unpublished, so the enrichment claims cannot be independently audited from the paper or named supplements.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publication of the full 394-pair table, all filters, all observed/expected counts, full 2×2 statistics, and pre-specified test family.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 31. Phase-143 Bonferroni denominator cannot be re-derived from published files

**(a) Quote (§3.8 Iconographic Cross-Encoding):**  
“The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”

**(b) Defect:**  
The multiple-testing correction denominator is not reproducible from published materials.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Full pair list and all possible sign × icon combinations with inclusion/exclusion flags.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 32. Phase-150 permutation null lacks seed and full matching rule in the paper

**(a) Quote (§3.13 Polysemy Permutation Null):**  
“A permutation null test (n=1,000 within-seal position shuffles) was run against the Phase-142D polysemy finding.”

**(b) Defect:**  
The paper gives `n=1,000` and the broad shuffle type, but no random seed, exact shuffling implementation, or input table. Unlike Phase-151, no fixed seed is reported here.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Seed, script, input data, and exact permutation algorithm.

**Kind:** (i) defect in what the paper says.

---

### 33. Phase-151 bootstrap interval method is unnamed

**(a) Quote (§3.14 Site Repertoire Divergence Bootstrap):**  
“Neither the Phase-151 record nor its script names the interval method (percentile, basic, or bias-corrected), so the printed interval is reported as recorded, without a method name.”

**(b) Defect:**  
The reported 95% CI cannot be methodologically evaluated because the interval construction method is unknown.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Identification and implementation of the bootstrap CI method.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 34. Phase-170 self-consistency test has unspecified tie/overlap handling

**(a) Quote (§3.31 Grammar Variance Retest):**  
“The Phase-170 record states the rules in the order TERMINAL, INITIAL, MEDIAL, else MIXED; it does not state what happens when a sign’s rates satisfy more than one threshold, and that tie/overlap handling is not on record.”

**(b) Defect:**  
Classification rules are incomplete for threshold-overlap cases.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Explicit priority/tie rules and a list of signs affected by overlaps.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 35. Meluhhan-name expanded matching lacks a segment-match rule

**(a) Quote (§3.28 Expanded Meluhhan Name Matching):**  
“The record does not state a fuller rule for how a single segment counts as matched, and none is claimed here.”

**(b) Defect:**  
The matching algorithm cannot be reproduced or evaluated because the basic segment-match criterion is unspecified.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Formal segment-matching rules, examples, code, and all per-name/per-seal match decisions.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 36. Tamil-Brahmi terminal inventory has no cited source

**(a) Quote (§3.18 Tamil-Brahmi Terminal Comparison):**  
“No published source for that 11-category inventory is cited in this paper or in the Phase-155 record; the inventory is the test’s own working list, and the match count can be checked against the record but not against an external authority.”

**(b) Defect:**  
The comparison depends on an uncited, internally constructed terminal inventory.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A published source for the terminal categories or a justified coding protocol with expert validation.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 37. Phonological exclusivity test uses uncited working phoneme inventories

**(a) Quote (§3.11 Phonological Exclusivity Test):**  
“Both sound inventories used in this test are the test’s own working lists, printed in full in this section and existing nowhere else in this program’s records; no published Sanskrit or Dravidian phoneme-inventory source is cited, because none was used.”

**(b) Defect:**  
The test’s result is only about ad hoc inventories and lacks external linguistic authority.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Cited phoneme inventories and a pre-specified mapping from readings to phonological markers.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 38. Gulf seal text search is not reproducible because search terms and context enumeration are missing

**(a) Quote (§3.19 Gulf Seal Fish-Sign Test):**  
“The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”

**(b) Defect:**  
The Gulf text-search result is not reproducible from the paper or record description.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Exact search terms, OCR/text files, context list, scripts, and hit/no-hit logs.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 39. Text-mining pipeline lacks archived model settings and benchmarked precision/recall

**(a) Quote (§7 AI Disclosure):**  
“Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”  
and  
“no benchmark of the mining pipeline’s recall or precision exists (§3.24).”

**(b) Defect:**  
The literature-mining counts and proximity hits cannot be rerun from a complete specification, and their error rates are unknown.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Archived models/prompts/settings, input texts, scripts, benchmark corpus, precision/recall estimates, and full hit lists.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 40. CISI/mayig comparison lacks bibliographic references and numerator/denominator

**(a) Quote (§3.10 Cross-Corpus Structural Comparisons):**  
“Comparison with the CISI corpus (179 inscriptions, Parpola P-numbers, mayig digitization): the Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere … so the percentage cannot be checked or recomputed…”  
and  
“CISI is the Corpus of Indus Seals and Inscriptions; neither it nor the mayig digitization has a §8 entry…”

**(b) Defect:**  
The comparison has missing bibliographic support and missing numerator/denominator.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Full CISI and mayig citations, dataset version, numerator, denominator, and crosswalk.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 41. Spec 068 comparison systems lack §8 bibliographic entries

**(a) Quote (§2.1.1):**  
“this paper gives no §8 entry and no fuller bibliographic identification for the Dering Roll source, the Mesopotamian numerical-sign table, or DAMOS (the source of the Linear B transliterations), and the Shakti corpus and the ICIT line are likewise identified only through that record.”

**(b) Defect:**  
Major comparison datasets used in a methodological control are not bibliographically identified in the paper’s references.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Complete §8 references and dataset/version identifiers for all comparison systems.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 42. Shu-ilishu external facts lack §8 source coverage

**(a) Quote (§3.15 Shu-ilishu Phonological Test):**  
“The external facts in this section (the Ur III date, c. 2020 BCE; the title ‘interpreter of the Meluhha language’; the provenance recorded as ‘excavated at Ur, held at British Museum’) are as recorded in the Phase-152 record … which is the source this section relies on; no §8 entry covers them.”

**(b) Defect:**  
External historical claims are made without a reference in §8.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A proper bibliographic reference for the Shu-ilishu seal facts.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 43. Mahadevan mined-paper references are incomplete in §8

**(a) Quote (§3.23 Mahadevan Grammar Consistency):**  
“the Phase-160 counts give per-paper hits for all ten papers mined: Grammar of Indus Texts (1986) 8; What Do We Know (1989) 7; Terminal Ideograms (1982) 6; Encyclopaedia (1994) 5; Place Signs (1981) 4; Akam-Puram (2011) 4; Toponyms (2018) 3; Bilingual Parallels (1972) 3; Murukan (1999) 2; Blue Neck (2008) 2.”

**(b) Defect:**  
Several named mined papers lack §8 entries: “Encyclopaedia (1994),” “Toponyms (2018),” “Bilingual Parallels (1972),” “Murukan (1999),” and “Blue Neck (2008)” are not separately identifiable from the reference list. This prevents citation completeness and source checking.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Full §8 entries for every mined paper, with titles, publication venues, pages, and dates.

**Kind:** (i) defect in what the paper says.

---

### 44. “38 Mahadevan papers” corpus cannot be tied to a verifiable source list

**(a) Quote (§3.23):**  
“the aggregate counts ‘10 papers, 1972–2018’ and, in §3.24, ‘38 papers’ are this program’s own corpus counts and could not be tied to a verifiable external source”

**(b) Defect:**  
The literature corpus is not bibliographically enumerated, so the scope of the mining cannot be checked.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A complete bibliography of all 38 papers and the exact text files mined.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 45. §8 contains an apparently uncited Rao PNAS reference

**(a) Quote (§8 References):**  
“Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”

**(b) Defect:**  
I found no in-text use of this PNAS “Markov model” reference distinct from the Science entropy citation. The in-text passage says “Rao et al. (2009, Science 324:1165),” which corresponds to the separate Science reference, not the PNAS entry.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Either cite the PNAS paper where used, or remove the unused reference.

**Kind:** (i) defect in what the paper says.

---

### 46. Arthaśāstra analogy has no §8 reference

**(a) Quote (§4.1):**  
“The Arthaśāstra (a layered Sanskrit text whose core is usually placed in the last centuries BCE, roughly a millennium and a half after the end of the IVC period) documents Sanskrit superintendent titles of a broadly similar kind — koṣṭhāgārādhyakṣa (storehouse superintendent), nāvadhyakṣa (ship superintendent).”

**(b) Defect:**  
The paper cites a historical text and makes dating/content claims but gives no §8 reference for the Arthaśāstra or the stated dating.

**(c) Severity:** MINOR

**(d) What would settle it:**  
A proper edition/translation/reference and source for the dating claim.

**Kind:** (i) defect in what the paper says.

---

### 47. Vowel-harmony test has no authoritative frozen protocol

**(a) Quote (§3.17 Vowel Harmony Methodology Resolution):**  
“No one of these three procedures is currently the program’s authoritative V12 test: the records disagree because the test was redefined between runs, and the full rule changes are not recorded for every version.”

**(b) Defect:**  
The V12 warning cannot be interpreted reproducibly because there is no frozen test protocol and rule changes are incompletely recorded.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A frozen V12 protocol, full rule-change history, rerun on the current 161-sign set, and per-seal/per-root outputs.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 48. Corpus-level M267 chi-square treats token observations as independent despite seal-level motif

**(a) Quote (§3.4):**  
“One limit of this test belongs on the record: the chi-square treats M267’s 400 tokens as independent observations, but a motif is a property of a seal, not of a token. The Phase-132 record does not state how many distinct seals the 400 tokens occur on, and no seal-level version of this test is on record…”

**(b) Defect:**  
The test statistic’s independence assumption is mismatched to the unit of motif assignment.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Seal-level contingency table and seal-level chi-square, Fisher/exact, or mixed model.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

## POSITIVES CHECKED

1. **The headline token-coverage arithmetic is internally consistent.**  
   **Passage checked (§3.1):** “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”  
   Calculation: 6,369 / 7,002 = 0.9096.

2. **The provisional-removal arithmetic is internally consistent.**  
   **Passage checked (§3.1):** “The four PROVISIONAL_MEDIUM signs … account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”  
   Calculation: 6,369 − 15 = 6,354; 6,354 / 7,002 = 0.9075.

3. **The Phase-134 z-score arithmetic recomputes from printed values.**  
   **Passage checked (§2.3):** “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   Calculation is correct.

4. **The bigram-token denominator is internally consistent.**  
   **Passage checked (§3.7):** “5,332 bigram tokens — the corpus’s 7,002 sign tokens minus one for each of its 1,670 inscriptions.”  
   Calculation: 7,002 − 1,670 = 5,332.

5. **The M267 motif-count total is internally consistent.**  
   **Passage checked (§3.4):** “unicorn 147 tokens, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20, script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens in total.”  
   Calculation: 147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = 400.

6. **The blocker hypothetical coverage arithmetic is internally consistent.**  
   **Passage checked (§3.29):** “6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”  
   Calculation is correct.

7. **The paper clearly distinguishes positional measurement from semantic interpretation in several places.**  
   **Passage checked (§3.2):** “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics.”  
   This is an adequate disclosure of a major interpretive boundary.

8. **The paper adequately discloses that confidence labels are not calibrated probabilities.**  
   **Passage checked (§2.2):** “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
   This is methodologically important and stated plainly.

9. **The paper adequately discloses that corpus-level counts cannot currently be reproduced by ordinary readers.**  
   **Passage checked (Abstract):** “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
   The limitation is stated at appropriate strength.

10. **The paper correctly avoids treating the Gulf text search as confirmation.**  
   **Passage checked (§3.19):** “the Gulf material provides no counterexample to the Holdat count, but it does not independently confirm it.”  
   This is a sound limitation statement.

CALL-META pass3: finish_reason=stop; max_completion_tokens=60000; completion_tokens=12282; prompt_tokens=31962; output_chars=40789.

## PASS 4 — HOSTILE SUMMARY

## (1) Numbered findings, ordered most-serious first

### 1. Corpus-level headline results are not independently reproducible from the paper.

**(a) Quoted passage**

Abstract:

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

Abstract:

> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”

§6 Data Availability:

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect**

The headline claims depend heavily on corpus-level counts: 90.96% token coverage, 69.8% seal coverage, positional statistics, permutation tests, fish-sign counts, site distributions, collocates, and sign frequencies. The paper admits that these cannot be re-run by outside researchers because the underlying corpus is private. That leaves the central quantitative evidence unverifiable from the paper alone.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

Public release of the exact Holdat corpus version used, or a complete auditable data extract sufficient to reproduce every corpus-level statistic; alternatively, successful independent replication on a public corpus with a documented crosswalk.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 2. The 161-reading / 90.96% “coverage” headline is assignment coverage, not decipherment validation.

**(a) Quoted passage**

Abstract:

> “These readings are assigned to signs that together account for 90.96% of the corpus’s sign tokens (69.8% of seals consist entirely of such signs). ‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”

§5 Conclusion:

> “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage — assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings) are Tier 2 claims supported by multiple tests.”

§2.2 Evidence Hierarchy:

> “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”

**(b) Defect**

The headline number sounds like high decipherment coverage, but the paper itself defines it as only the proportion of tokens whose sign has been assigned a candidate reading. No reading is verified, and no confidence label has a measured error rate. Therefore the central “161 anchors / 90.96% coverage” result is not evidence that 90.96% of the corpus has been deciphered.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

External validation of readings: bilingual text, independently coded iconographic evidence, held-out known-script calibration, blinded expert assessment, or a rival-model comparison with quantified false-positive rates.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 3. The evidence standards for HIGH readings are not auditable sign-by-sign from the paper or even from the described records.

**(a) Quoted passage**

§2.2 Evidence Hierarchy:

> “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field, so questions of the form ‘which signs meet criterion X but not criterion Y’ cannot always be answered from the records”

§2.2 Evidence Hierarchy:

> “Three of the criteria above are stated at the level this program’s records support and no further: the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record; ‘cases’ in the terminal-marker criterion means the sign’s corpus tokens; and the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table.”

§2.2 Evidence Hierarchy:

> “A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone. That limit applies to every HIGH sign, not only to the three discussed in §3.3: the audit file records the same evidence-type pair (iconographic + distributional) for all 75 HIGH signs, §3.3 prints selected rows for 12 of them, and no record gives a criterion-by-criterion pass/fail for any HIGH sign. A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect**

The paper’s top confidence class, HIGH, is central to the decipherment claim, yet the paper admits that no reader can verify whether any particular HIGH sign actually satisfies the stated two-criterion rule. Iconographic coding lacks a protocol, blinding, and reliability measurement; exclusivity denominators are not published; criterion pass/fail results are not recorded.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

A public sign-by-sign evidence matrix showing each criterion as pass/fail, with published motif denominators, coding rules, blinded independent coders, inter-coder reliability, and reproducible scripts.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 4. DEDR rebus matching has no recorded search space, rejection log, or multiple-comparison control.

**(a) Quoted passage**

§2.2 Evidence Hierarchy:

> “One limit of the DEDR criterion must be stated plainly. For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect**

The rebus component is vulnerable to cherry-picking: the adopted DEDR match is recorded, but the candidate universe, transformations allowed, rejected alternatives, and chance-match rate are not. This directly undermines the evidentiary value of DEDR-backed readings.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

A frozen DEDR search protocol, full candidate and rejection logs, explicit phonological transformation rules, and empirical false-positive estimates using controls or rival lexicons.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 5. The syllabic language model component failed its own held-out test, yet contributes to the MEDIUM set.

**(a) Quoted passage**

§2.4 Syllabic Language Model:

> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”

§2.4:

> “And a later test inside this program (Phase-107, October 2026) put the SA machinery itself to a held-out test whose protocol, primary metric, and discrimination rule were fixed in advance in this program’s Spec 005 … Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

§2.4:

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”

§2.4:

> “If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain. That is a bound, not a recomputed headline”

§2.4:

> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

**(b) Defect**

A component used in promoting MEDIUM readings has unknown false-positive rate, unreconstructable training data, and a held-out agreement of 0.000, indistinguishable from Sanskrit and scrambled controls. The paper says no H+M sign rests on SA alone, but 43 MEDIUM signs involve the failed SA+DEDR route.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

A reconstructable training set, calibration on known scripts, a successful preregistered held-out test, and recomputation of the headline readings without SA-dependent promotions.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 6. Internal phonological checks raise unresolved problems concentrated in headline signs.

**(a) Quoted passage**

§3.17 Vowel Harmony Methodology Resolution:

> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”

§3.17:

> “We therefore withdraw the earlier description of V12 as a settled methodology artifact: vowel harmony is an open problem for the reading set”

§3.18 Tamil-Brahmi Terminal Comparison:

> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs. No record supports excusing those violations as mostly short abbreviated seals, and we do not do so here.”

§3.18:

> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

§5 Conclusion:

> “the set also carries the unresolved V12 warning and the 23.4% V07 phonotactic violation rate (§§3.17–3.18) — a rate concentrated in high-frequency headline signs (M328, M211, M176 and M342 drive it, §3.18), not spread over rare or doubtful readings.”

**(b) Defect**

The proposed reading set fails or triggers warnings under the program’s own phonological checks. The problem is not confined to rare signs; it is concentrated in high-frequency headline signs. This directly weakens the claimed Proto-Dravidian compatibility of the anchor set.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

A single frozen phonological protocol, rerun on the current 161-sign set; error analysis showing whether violations arise from notation, segmentation, or genuinely bad readings; and correction or demotion of readings that fail.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 7. The paper does not establish that Proto-Dravidian is superior to rival language or non-language baselines.

**(a) Quoted passage**

Abstract:

> “the evidence is consistent with a Proto-Dravidian reading framework under the tested assumptions, though Dravidian superiority over proto-Munda has not been formally quantified.”

§4.4 Limitations:

> “Language-family baseline: The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

§4.4:

> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”

§5 Conclusion:

> “The corpus shows non-random positional structure of the kind a writing system produces and also of the kind some non-linguistic marking systems produce; the tests in this paper do not separate those two, and the frequency-curve evidence that might have spoken to the question was uninformative (§2.1.1).”

**(b) Defect**

The headline framing is Proto-Dravidian decipherment, but the paper admits that it has not shown Proto-Dravidian to be discriminatively better than Proto-Munda, early Indo-Aryan, Sanskrit-side controls, or non-linguistic marking systems. The result is compatibility, not identification.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

A preregistered model-comparison framework applying the same procedures to Proto-Dravidian, Proto-Munda, early Indo-Aryan/Sanskrit-side, and non-linguistic baselines, with held-out evaluation and calibrated error rates.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 8. The “three-slot grammar” is a positional regularity, not a demonstrated grammar with classifier/title/name semantics.

**(a) Quoted passage**

Abstract:

> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests (§3.2).”

§3.2 Grammar Model:

> “Statistical analysis of inscription structure identifies a three-slot pattern that is consistent at the level of individual signs’ positions. Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).”

§3.2:

> “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics”

§3.2:

> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

§3.2:

> “The model predicts the position of the name element only; it does not read any person’s name (§3.9, §4.3).”

**(b) Defect**

The statistical result is sign-position regularity. The semantic interpretation as classifier/title/name/case is not produced by the statistics, and whole inscriptions fully match the pattern only 5.1% of the time. Rival functional templates that could generate positional structure were not tested.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Tests against explicit rival templates; whole-inscription predictive evaluation; independent identification of names, titles, or classifiers; and external validation from repeated name sequences or bilingual material.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 9. The main positional statistic shows non-random ordering, but its evidential scope is narrower than the headline decipherment claim.

**(a) Quoted passage**

§2.3 Positional Analysis:

> “The headline positional statistic (z = 10.3) comes from the Phase-134 F1 test. We fit the three-slot grammar model to the real corpus (coefficient of determination 𝑅2 = 0.9916) and to 2,000 copies of the corpus in which the signs inside each inscription were shuffled”

§2.3:

> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

§2.3:

> “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script … The Phase-134 JSON record reports the statistic’s inputs and outputs … but not the data matrix, and this section does not reproduce the script’s procedure. The z-score can therefore be checked arithmetically from the printed inputs in this section … but the fit itself can be re-run only from the script and the corpus.”

§5 Conclusion:

> “The corpus shows non-random positional structure of the kind a writing system produces and also of the kind some non-linguistic marking systems produce; the tests in this paper do not separate those two”

**(b) Defect**

The impressive z-score supports non-random within-inscription ordering under this statistic. It does not validate the readings, the semantic slot labels, or linguistic status. Exact rerun is also blocked by missing seed/inclusion details and the private corpus.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Public corpus and scripts sufficient to reproduce the statistic; comparison against explicit non-linguistic administrative/owner/commodity/clan baselines; and demonstration that the positional model predicts unseen data better than rivals.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 10. External name-anchor tests do not validate the readings.

**(a) Quoted passage**

§3.15 Shu-ilishu Phonological Test:

> “No seal in the corpus matched three or more of the four slots (Phase-152: candidate seals = 0).”

§3.15:

> “Result: NO_SEAL_MATCH — partial inventory overlap only (2 of 4 slots covered; candidate seals = 0).”

§3.28 Expanded Meluhhan Name Matching:

> “All 25 names produced apparent ‘matches’ at this threshold due to the prevalence of common short readings (ā, kol, il) in the H+M-covered seal set. Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.”

§3.26 Meluhhan Name Phonological Matching:

> “Testing 6 attested Meluhhan personal names from Mesopotamian cuneiform against corpus sign sequences: no strong matches (>=3/4 phonological slots) found in the 1,670-seal corpus.”

**(b) Defect**

The paper’s direct external-name tests fail to produce a discriminative match. This is especially damaging because personal-name identification would be one of the strongest forms of validation for a proposed administrative/name-bearing decipherment.

**(c) Severity**

MAJOR.

**(d) What would settle it**

A preregistered name-matching test with explicit segment-matching rules, larger corpus, contextual metadata, and matches that are rare under controls and recover known external names at seal level.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 11. Literature-mining and overlap evidence is circular or unbenchmarked, not independent validation.

**(a) Quoted passage**

§3.22 Parpola 1994 Reading Overlap Count:

> “This is not independent cross-validation: Parpola’s framework guided the choice of readings (§7), so agreement with his book is partly expected by construction, and the count records appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”

§3.24 Literature Extraction Ceiling:

> “That is a null result for this search method only: its recall has never been measured against a hand-checked list of known proposals”

AI Disclosure:

> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

§3.30 Master Evidence Synthesis:

> “The items mix two different kinds of check — internal consistency checks (which can show the model agrees with itself) and external comparisons (which can test it against something outside) — and only the second kind is evidence about the world.”

**(b) Defect**

The paper’s literature evidence is not independent where it overlaps Parpola, and the text-mining pipeline lacks validated recall/precision and archived run settings. The scorecard mixes internal consistency with external evidence, limiting its probative value.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Hand-audited literature extraction, archived reproducible mining specifications, measured recall/precision against a gold standard, and separation of internal consistency checks from external validation.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

### 12. The claimed falsifiability is mostly future or in-principle; the paper’s own validation path contains no current decisive test.

**(a) Quoted passage**

Title:

> “A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script”

§4.5 Validation Path:

> “The candidate model is falsifiable in principle at the first of the following points. None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

§4.5:

> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**(b) Defect**

The title foregrounds falsifiability, but the paper admits that its listed validation path has no presently executable decisive test: one depends on a future bilingual discovery, one has already failed to confirm, and one lacks a discriminating prediction. The model is therefore falsifiable mainly in principle, not operationally on available data.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Pre-registered discriminating predictions that can be tested on existing public or releasable data, with clear failure conditions against rival models.

**Kind**

(i) A defect in what the paper says.

---

### 13. Generalization beyond the private formal-seal corpus is not established.

**(a) Quoted passage**

§4.4 Limitations:

> “Single corpus: The Holdat corpus covers formal stamp seals only. Copper tablets, potsherd graffiti, and the Dholavira signboard require separate analysis.”

§3.10 Cross-Corpus Structural Comparisons:

> “The positional-class distributions of the two corpora differ substantially (KL divergence = 0.591; the Phase-145 record itself rates structural agreement LOW — for example, MEDIAL-class share is 68.75% in CISI against 34.8% in Holdat). Because the two corpora use different sign numberings and different coverage, we report the difference without explaining it away.”

§3.10:

> “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed”

§5 Conclusion:

> “The ICIT corpus is the immediate priority for testing whether the candidate model generalises to a larger public corpus.”

**(b) Defect**

The model is built on one private formal-stamp-seal corpus. The cross-corpus comparison presented is weak: one figure is uncountable, and positional-class distributions differ substantially. The paper has not shown that the anchor model generalizes to the wider Indus inscriptional record.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Replication on a larger public corpus such as ICIT with a documented sign crosswalk, plus separate analyses for non-seal object classes.

**Kind**

(ii) A limitation the paper itself already discloses at the same strength.

---

## (2) Strongest overall hostile referee-report case

The paper’s strongest defensible result is that this private formal-seal corpus contains non-random positional structure. That is far short of a decipherment. The headline “161 Proto-Dravidian anchors” rests on candidate assignments, not verified readings; the confidence labels have no calibrated error rates; the HIGH class is not auditable criterion-by-criterion; the DEDR rebus search has no recorded candidate universe or multiple-comparison control; and one computational promotion route, the syllabic model, failed its own held-out test with 0.000 agreement and indistinguishable Sanskrit/scrambled controls.

The proposed Proto-Dravidian interpretation is therefore compatible with the author’s assumptions, not discriminatively established. The paper itself admits that Dravidian superiority over Proto-Munda, early Indo-Aryan, Sanskrit-side controls, and language-neutral/non-linguistic baselines has not been demonstrated. Its internal phonological checks raise unresolved problems, including a 23.4% phonotactic violation rate concentrated in high-frequency headline signs. External validation attempts through Meluhhan names and the Shu-ilishu seal do not produce discriminative matches. Literature overlap is partly circular, and text-mining evidence is unbenchmarked and not fully reproducible.

The three-slot grammar is likewise over-strong as a decipherment claim. The measured result is positional regularity; the semantic labels classifier/title/name/case are interpretations. Whole-inscription full matches are only 5.1%, and rival explanations such as owner marks, commodity marks, clan emblems, or other administrative non-linguistic systems are not tested. Finally, almost all central numbers depend on a private corpus that cannot be independently rerun. A hostile expert could fairly say: this is an internally self-critical exploratory model with interesting positional statistics, but it does not yet supply reproducible, externally validated, discriminative evidence for a Proto-Dravidian decipherment of the Indus script.

---

## (3) POSITIVES checked and still standing after hostile scrutiny

### Positive 1. The paper honestly distinguishes assignment coverage from verified decipherment.

**Passage checked**

Abstract:

> “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”

**Assessment**

This is an important and accurate internal caveat. The paper does not explicitly claim that 90.96% of tokens are deciphered.

---

### Positive 2. The headline coverage arithmetic is internally consistent from the printed numbers.

**Passage checked**

§3.1:

> “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%).”

§3.1 table:

> “HIGH … 70.34% (4,925 tokens)”  
> “MEDIUM (including provisional) … 20.62% (1,444 tokens)”  
> “H+M total … 90.96%”

**Assessment**

4,925 + 1,444 = 6,369, and 6,369 / 7,002 ≈ 90.96%. The arithmetic is internally sound.

---

### Positive 3. The z-score arithmetic is checkable from the printed inputs.

**Passage checked**

§2.3:

> “The z-score is the distance between the real value and the shuffled mean, measured in standard deviations: z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

**Assessment**

The arithmetic is correct: (0.9916 − 0.4385) / 0.05347 ≈ 10.34.

---

### Positive 4. The paper explicitly limits the evidential meaning of the positional statistic.

**Passage checked**

§5:

> “The corpus shows non-random positional structure of the kind a writing system produces and also of the kind some non-linguistic marking systems produce; the tests in this paper do not separate those two”

**Assessment**

This is an adequate disclosure. The paper does not claim that the positional statistic alone proves linguistic writing.

---

### Positive 5. The fish-sign isolation result is correctly demoted as non-fish-specific.

**Passage checked**

§3.5:

> “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result”

**Assessment**

This is a strong and appropriate correction. The paper does not overclaim the fish-sign count as independent evidence.

---

### Positive 6. The M267 correction is clearly stated and methodologically useful.

**Passage checked**

§3.4:

> “Version 6 of the anchor table assigned M267 (corpus frequency=400) as ‘mīn/fish.’ This was incorrect.”

§3.4:

> “This correction is methodologically important: it demonstrates the risk of reading frequency alone as a phonetic indicator.”

**Assessment**

The paper forthrightly corrects a major prior error and draws the right methodological warning from it.

---

### Positive 7. The paper discloses the failed SA held-out test rather than burying it.

**Passage checked**

§2.4:

> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

**Assessment**

This is a severe negative result, but it is disclosed plainly and at the necessary strength.

---

### Positive 8. The paper separates speculative interpretations from measured results in several places.

**Passage checked**

§4.1:

> “Under the model — and only under the model — these inscriptions read as a directory of guild members rather than a commodity ledger; the two readings have not been separated by any test yet”

§4.2:

> “We record, as speculation and nothing more, the scenario they would fit if they were correct”

**Assessment**

The paper repeatedly marks guild semantics, substrate scenarios, and individual translations as model-dependent or speculative rather than established facts.

CALL-META pass4: finish_reason=stop; max_completion_tokens=48000; completion_tokens=8071; prompt_tokens=31919; output_chars=29507.
