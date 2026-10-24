# Glossa Lab Indus Preprint v8 — Red-Team Round 8: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 124,867 chars, SHA-256 of PDF 5335cdaba21c88c7ae6b56a75e5ec0f1a4db109ad480e57c652568709920b035), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs. Each finding was briefed to carry a kind label: (i) a defect in what the paper says, or (ii) a limitation the paper itself already discloses at the same strength.


## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## PASS 1 — Findings

### 1. Conclusion strengthens the body’s stated language-family limitation

**(a) Quoted passage(s)**

§4.4, limitation 6:

> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

Abstract:

> “the evidence is consistent with a Proto-Dravidian reading framework under the tested assumptions, though Dravidian superiority over proto-Munda has not been formally quantified.”

§5 Conclusion:

> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

**(b) Defect**

The conclusion’s “favours” is stronger than the body’s “merely compatible” and the abstract’s “consistent,” especially because the body explicitly says formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral baselines is still required before the interpretation can be treated as discriminative.

**(c) Severity**

MAJOR

**(d) What would settle it**

Either weaken the conclusion to “compatible with” / “consistent with,” or provide a formal comparative baseline showing that Proto-Dravidian is discriminatively preferred over the named alternatives.

**Kind label**

(i) defect in what the paper says


### 2. Corpus-level counts cannot be independently recomputed from the paper because the corpus is unavailable

**(a) Quoted passage**

Abstract:

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

Abstract:

> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”

§6 Data Availability:

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect / limitation**

Most headline arithmetic depends on corpus-level counts that cannot be independently recomputed from the paper or public data. This includes token coverage, seal coverage, positional counts, fish-bearing seal counts, motif distributions, bigram counts, and many phase-level statistics.

**(c) Severity**

MAJOR

**(d) What would settle it**

Public release of the Holdat corpus used for the paper, or a fully specified public surrogate corpus plus crosswalk and scripts sufficient to reproduce the counts.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 3. The Phase-134 permutation result’s printed z-score recomputes, but the underlying fit/permutation cannot be rerun exactly from the paper

**(a) Quoted passage**

§2.3:

> “The headline positional statistic (z = 10.3) comes from the Phase-134 F1 test. We fit the three-slot grammar model to the real corpus (coefficient of determination 𝑅2 = 0.9916) and to 2,000 copies of the corpus in which the signs inside each inscription were shuffled (mean 𝑅2 = 0.4385, standard deviation 0.05347 — the Phase-134 record’s values before rounding). The z-score is the distance between the real value and the shuffled mean, measured in standard deviations: z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

§2.3:

> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

§2.3:

> “The z-score can therefore be checked arithmetically from the printed inputs in this section … but the fit itself can be re-run only from the script and the corpus.”

**(b) Defect / limitation**

The arithmetic z-score recomputes: \((0.9916 - 0.4385) / 0.05347 = 10.344\). But the statistic’s underlying data matrix, fitting procedure, random seed, inclusion rules, and corpus are not printed, so the test cannot be independently rerun exactly from the paper.

**(c) Severity**

MAJOR

**(d) What would settle it**

Publication of the corpus, exact data matrix, fitting rule, shuffling rule, inclusion/exclusion rules, random seed, and script version.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 4. DEDR-related counts use non-interchangeable definitions

**(a) Quoted passage**

§1.3 item 7:

> “A DEDR citation is recorded in that table’s DEDR column for 15 of the 161 signs; the other 146 of the 161 rows carry no entry in that column, and their support is of the other kinds stated row by row in the table’s Basis column. No claim is made that every reading carries a DEDR citation. Three DEDR counts in this paper count three different recorded things, and they are not interchangeable: this count (entries in the anchor table’s DEDR column); the combined evidence type SA+DEDR recorded in the status audit for 43 MEDIUM signs (§2.4), which records the route by which those readings were promoted — in the audit file’s own DEDR column, only 15 of those 43 signs carry an entry; and the DEDR entry numbers printed for individual signs in §3.3 and §3.27, which are taken from those signs’ basis statements and phase records and are not all recorded in either file’s DEDR column.”

**(b) Defect / limitation**

The paper uses DEDR in at least three numerically distinct senses: 15 anchor-table DEDR-column entries, 43 SA+DEDR evidence-type promotions, and individual DEDR numbers printed in narrative tables. These are not the same quantity, so DEDR support cannot be counted by a single number from the printed paper.

**(c) Severity**

MAJOR

**(d) What would settle it**

A single audit table with one row per sign and separate explicit fields for: DEDR-column citation, DEDR used in basis statement, DEDR used in SA+DEDR promotion, and DEDR used in later phase checks.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 5. The SA-free headline coverage cannot be computed from the records

**(a) Quoted passage**

§2.4:

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv. The label records that a DEDR match was part of each sign’s promotion route; it is not a count of entries in that file’s DEDR column, where 15 of the 43 signs carry an entry and 28 do not. If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain. That is a bound, not a recomputed headline: the audit file does not record whether any of the 43 also meets a non-SA MEDIUM criterion (a positional profile or allograph support), so a true SA-free headline cannot be computed from the records.”

**(b) Defect / limitation**

The paper gives a bound, not an actual SA-free coverage figure. The printed arithmetic recomputes: 5,971 / 7,002 = 85.28%. But because the records do not encode whether the 43 SA+DEDR signs also meet non-SA MEDIUM criteria, the real coverage without SA support cannot be determined.

**(c) Severity**

MAJOR

**(d) What would settle it**

Criterion-level pass/fail fields for every sign, allowing a recomputation excluding SA while retaining signs independently satisfying non-SA MEDIUM criteria.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 6. CISI opening-sign percentage is explicitly uncheckable

**(a) Quoted passage**

§3.10:

> “Comparison with the CISI corpus (179 inscriptions, Parpola P-numbers, mayig digitization): the Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed, and we report it as an uncountable figure carried from that record, not as a verified result.”

**(b) Defect / limitation**

The 87.08% figure cannot be recomputed because the numerator and denominator are absent. It is therefore not auditable from printed inputs or records described in the paper.

**(c) Severity**

MAJOR

**(d) What would settle it**

Print or release the denominator, numerator, corpus inclusion rules, sign crosswalk, and positional class mapping used for the CISI comparison.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 7. Fish-sign supplemental context file conflicts with the printed fish-family list

**(a) Quoted passage**

§3.5:

> “Testing the full fish sign family — M047, M049, M052, M053, M054, M055, M056, M145, the signs this program’s Mahadevan–Parpola crosswalk file lists as fish-shaped — across all 9 sites.”

§3.5:

> “The supplemental file fish_sign_compound_context.csv lists 27 compound occurrences with their contexts (13 for M047 and 14 for M001; M001 is not in the family list printed above, and that mismatch is on record and unresolved). It is not an occurrence-by-occurrence listing of all 113 fish-bearing seals, and earlier wording that described it as one is corrected here.”

**(b) Defect / limitation**

The supplemental file includes 14 contexts for M001 even though M001 is not in the printed fish-family list. This is an unresolved internal mismatch in the fish-sign supporting material.

**(c) Severity**

MINOR

**(d) What would settle it**

Correct the fish-family list or the supplemental file, and document whether M001 is or is not part of the tested fish-sign family.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 8. Shu-ilishu phonological slot list contains an acknowledged reading mismatch

**(a) Quoted passage**

§3.15:

> “Testing the four phonological slots /su/, /i/, /li/, /shu/ against the pre-Phase-163 157 H+M readings: 2/4 slots are covered (/i/ by the candidate signs the Phase-152 record lists — M267, M162, M336, M305, M045 — of which M305’s recorded reading, ōṭu/comitative, contains no /i/ sound; the record’s slot list is reported here as recorded, and this mismatch is one reason the test’s result is stated as inventory overlap only; /li/ by 4 signs including M162=il/iḷ).”

**(b) Defect / limitation**

One sign listed as contributing to the /i/ slot, M305, has the recorded reading ōṭu/comitative and therefore does not contain /i/. The paper says this does not change the narrow “inventory overlap only” interpretation, but the slot evidence list is internally contaminated.

**(c) Severity**

MINOR

**(d) What would settle it**

Correct the Phase-152 slot list and recompute the slot-coverage statement from the corrected readings.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 9. V12 vowel-harmony results are internally inconsistent across phases and no authoritative version exists

**(a) Quoted passage**

§3.17:

> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% (Phase-132: 476 of 632 decoded seals, against an 85% threshold), 64.2% on a stricter cross-reading version (Phase-133e), or 36.1% (Phase-154: 417 of the 1,154 seals checked passed; 737 seals failed), where the recorded verdict is V12_ACTIVE_CONCERN.”

§3.17:

> “No one of these three procedures is currently the program’s authoritative V12 test: the records disagree because the test was redefined between runs, and the full rule changes are not recorded for every version.”

**(b) Defect / limitation**

The paper reports three materially different V12 pass rates: 75.3%, 64.2%, and 36.1%. The printed arithmetic for two of them checks — 476/632 = 75.3%, 417/1,154 = 36.1% — but the definitions changed and the rule changes are incompletely recorded, so the V12 result is not a stable, auditable statistic.

**(c) Severity**

MAJOR

**(d) What would settle it**

Freeze one V12 protocol, document it fully, rerun it on the current 161-sign set, and report only that authoritative result, with prior versions clearly marked as obsolete provenance.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 10. Gulf text-search result cannot be rerun from the record because search terms and context enumeration are missing

**(a) Quoted passage**

§3.19:

> “The Gulf extension searched about 145,000 characters of extracted text in the two source files named in the Phase-156 record: the extracted text of Laursen (2010) and the extracted text of the Bahrain volume (Mitchell 1986). The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”

**(b) Defect / limitation**

The Gulf-search counts are not reproducible from the paper or record as described because the search terms and the 27-context enumeration are absent.

**(c) Severity**

MAJOR

**(d) What would settle it**

Publish the exact extracted text files, search term list, matching rules, and the enumerated 27 Indus-script contexts.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


### 11. Phase-170 grammar retest is not comparable to the Phase-133 whole-inscription match figures

**(a) Quoted passage**

§3.31:

> “Results: 137/147 signs (93.2%) are classified by the thresholds into the positional class that is already their dominant class. This is a self-consistency check, not an accuracy measurement: the thresholds (TERMINAL if T>=0.60, INITIAL if I>=0.50, MEDIAL if M>=0.65 — program conventions, with no sensitivity analysis on record) are applied to the same rates that define each sign’s dominant class, so a high figure is expected by construction and the check can only catch internal contradictions.”

§3.31:

> “It is not comparable to Phase-133’s figures, which measured how well the grammar pattern matched whole inscriptions: full match 5.1% of seals and partial match 38.4%, together 43.5%. Phase-133’s 44.3% is a different quantity in the same record — its sign-position accuracy (explained variance) — not the sum of the full and partial rates.”

**(b) Defect / limitation**

The 93.2% Phase-170 figure is a sign-level self-consistency statistic, not an accuracy statistic and not comparable to the Phase-133 whole-inscription full/partial match rates. The arithmetic checks: 137/147 = 93.2%, and 5.1% + 38.4% = 43.5%. The limitation is interpretive, not arithmetic.

**(c) Severity**

MAJOR

**(d) What would settle it**

Use one explicitly defined grammar metric across phases, or keep the metrics separate and avoid any implication that the 93.2% retest confirms the 5.1% / 38.4% whole-inscription pattern.

**Kind label**

(ii) limitation the paper itself already discloses at the same strength


## POSITIVES — Internal arithmetic / consistency checks that recomputed

1. **Site counts sum to the stated corpus size.**  
   Passage checked, §2.1:

   > “1,670 seals, 9 sites: Mohenjo-daro (n=606), Harappa (n=492), Kalibangan (n=110), Dholavira (n=106), Lothal (n=124), Chanhu-daro (n=78), Surkotada (n=61), Banawali (n=60), Rakhigarhi (n=33).”

   Check: 606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670.

2. **Catalogue arithmetic is internally consistent.**  
   Passage checked, §2.1:

   > “the anchor table assigns readings to all 397 signs in the Mahadevan catalogue … the 397 catalogue entries carry numbers running from M001 to M416, with 19 numbers unused”

   Check: 416 possible numbers − 19 unused = 397.

3. **Confidence-category sign counts sum correctly.**  
   Passage checked, §3.1:

   > “HIGH 75 … MEDIUM … 86 … LOW 236 … H+M total 161”

   Check: 75 + 86 + 236 = 397; 75 + 86 = 161; 82 + 4 = 86.

4. **Token coverage table recomputes.**  
   Passage checked, §3.1:

   > “HIGH … 70.34% (4,925 tokens) … MEDIUM … 20.62% (1,444 tokens) … LOW … 9.04% (633 tokens) … The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”

   Checks:  
   4,925 / 7,002 = 70.34%;  
   1,444 / 7,002 = 20.62%;  
   633 / 7,002 = 9.04%;  
   4,925 + 1,444 + 633 = 7,002;  
   6,369 / 7,002 = 90.96%.

5. **Coverage without provisional signs recomputes.**  
   Passage checked, §3.1:

   > “The four PROVISIONAL_MEDIUM signs … account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”

   Check: 6,369 − 15 = 6,354; 6,354 / 7,002 = 90.75%.

6. **Seal coverage table recomputes.**  
   Passage checked, §3.6:

   > “Total seals 1,670 … Fully covered … 1,165 (69.8%) … Blocked … 505 (30.2%)”

   Checks: 1,165 + 505 = 1,670; 1,165 / 1,670 = 69.76%, printed as 69.8%; 505 / 1,670 = 30.24%, printed as 30.2%.

7. **Phase-134 z-score recomputes from printed inputs.**  
   Passage checked, §2.3:

   > “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

   Check: correct.

8. **Phase-134 held-out split arithmetic recomputes.**  
   Passage checked, §2.3:

   > “positional classes fitted on 1,176 seals, tested on 494 held-out seals … 85 of those 87 signs … 97.7% … actual shares are 70.4% and 29.6%”

   Checks: 1,176 + 494 = 1,670; 85/87 = 97.7%; 1,176/1,670 = 70.4%; 494/1,670 = 29.6%.

9. **Fish-bearing seal table totals recompute.**  
   Passage checked, §3.5:

   > “Lothal 6 … Harappa 33 … Mohenjo-daro 35 … Dholavira 11 … Kalibangan 13 … Chanhu-daro 5 … Banawali 4 … Rakhigarhi 3 … Surkotada 3 … Total 113”

   Check: 6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113.

10. **M267 motif-count and positional-count arithmetic recomputes.**  
    Passage checked, §3.4:

    > “unicorn 147 tokens, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20, script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens in total”

    Check: these sum to 400.

    Passage checked:

    > “Of its 400 occurrences, 324 (81.0%) are MEDIAL, 59 TERMINAL, and 17 INITIAL”

    Check: 324 + 59 + 17 = 400; 324/400 = 81.0%.

11. **Bigram-token total and PMI example recompute.**  
    Passage checked, §3.7:

    > “5,332 bigram tokens — the corpus’s 7,002 sign tokens minus one for each of its 1,670 inscriptions.”

    Check: 7,002 − 1,670 = 5,332.

    Passage checked:

    > “P(M342·M176) = 122/5,332, P(M342) = 584/7,002 and P(M176) = 356/7,002, and the printed PMI of 2.43 recomputes”

    Check: \(\log_2[(122/5332)/((584/7002)(356/7002))] \approx 2.43\).

12. **Formula semantic clustering table sums correctly.**  
    Passage checked, §3.12:

    > “UNRESOLVED 51 … 845 … 50.6%; ANIMAL_GUILD 25 … 446 … 26.7%; MATERIAL 6 … 145 … 8.7%; DEITY_TITLE 9 … 135 … 8.1%; CIVIC_ROLE 6 … 99 … 5.9%”

    Checks: clusters 51 + 25 + 6 + 9 + 6 = 97; seals 845 + 446 + 145 + 135 + 99 = 1,670; percentages recompute to the printed rounded values.

13. **Blocker hypothetical coverage recomputes.**  
    Passage checked, §3.29:

    > “The 19 signs … 97 tokens in total … 6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”

    Check: correct.

14. **Appendix B token total recomputes.**  
    Passage checked, Appendix B:

    > “frequencies of 5 (sixteen signs) or 6 (M270, M386) — 92 tokens in total”

    Check: 16×5 + 2×6 = 92.

15. **Phase-170 percentage recomputes.**  
    Passage checked, §3.31:

    > “Results: 137/147 signs (93.2%)”

    Check: 137/147 = 93.2%.

CALL-META pass1: finish_reason=stop; max_completion_tokens=48000; completion_tokens=11455; prompt_tokens=32218; output_chars=19578.

## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

## Red-team review — findings

### 1. Central corpus-level results are not independently reproducible at present
**(a) Quoted passage**  
Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
§6 Data Availability: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect / limitation**  
Most headline numbers are corpus-level counts: token coverage, seal coverage, positional statistics, fish-sign counts, bigram counts, site divergences. The paper itself says outside readers cannot rerun them without a private corpus. This is a reproducibility ceiling on the paper’s core evidence.

**(c) Severity**  
CRITICAL.

**(d) What would settle it**  
Public release of the exact Holdat corpus version used, or a complete archived surrogate sufficient to reproduce every corpus-level table and statistic.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 2. The title/headline “falsifiable” claim is stronger than the paper’s own validation path
**(a) Quoted passage**  
Title: “A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar”  
§4.5 Validation Path: “The candidate model is falsifiable in principle at the first of the following points. None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

**(b) Defect / limitation**  
The title presents the hypothesis as falsifiable, but the paper’s own validation section says no listed falsification route is presently an open runnable test on available data: one requires a future bilingual discovery, one was already run and did not confirm the model, and one lacks a discriminating prediction. That makes the headline “falsifiable” stronger than the operational evidence supplied.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A pre-specified discriminating test runnable on an available corpus, with explicit predictions under this model and rival models, plus pass/fail criteria.

**Kind**  
(i) A defect in what the paper says.

---

### 3. The paper’s broad “can be re-run and checked” claim is overbroad
**(a) Quoted passage**  
Abstract: “it proposes a falsifiable computational model whose method and repository artefacts (scripts, phase reports, and the anchor table) can be re-run and checked.”  
§2.3: “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”  
§7 AI Disclosure: “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect / limitation**  
The abstract implies method-level rerunnability. The body says several important pieces cannot be rerun exactly from the records: the corpus is private, the permutation seed/inclusion rules are missing from the record, and text-mining model/prompt/run settings were not archived. “Can be re-run and checked” is therefore too broad unless restricted to some scripts/artifacts, not the full evidentiary chain.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Archive the exact corpus, scripts, seeds, inclusion rules, OCR inputs, prompts/model versions/settings, and all intermediate data matrices needed for exact reruns.

**Kind**  
(i) A defect in what the paper says.

---

### 4. HIGH-confidence labels are not supported by records in the way the paper defines HIGH
**(a) Quoted passage**  
§2.2 Evidence Hierarchy: “HIGH (75 signs): Two or more of the following evidence criteria are met.”  
§2.2: “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field…”  
§2.2: “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect / limitation**  
The paper defines HIGH as satisfying at least two stated criteria, but then says neither the paper nor the audit file lets a reader verify that any particular HIGH sign actually satisfies two criteria “as those criteria are worded.” That is not merely missing detail; it undercuts the paper’s own definition of the HIGH label.

**(c) Severity**  
CRITICAL.

**(d) What would settle it**  
A sign-by-sign criterion matrix recording each §2.2 criterion as pass/fail, with underlying counts, coding decisions, and source citations.

**Kind**  
(i) A defect in what the paper says.

---

### 5. The 161-reading “supported” claim is stronger than the evidence for a large MEDIUM subset
**(a) Quoted passage**  
§2.4: “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”  
§2.4: “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”  
§2.2: “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”  
§5 Conclusion: “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage …) are Tier 2 claims supported by multiple tests.”

**(b) Defect / limitation**  
For 43 MEDIUM signs, the promotion route includes SA+DEDR. The paper says SA alone carried no information in a held-out test, and the DEDR search lacks recorded candidate sets, rejection rules, and multiple-comparison control. Calling the whole 161-reading set “supported by multiple tests” is therefore too strong for this subset unless “supported” is diluted to “assigned under the program’s uncalibrated rule.”

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A calibrated DEDR-rebus null model, recorded search space and rejection logs, multiple-comparison control, and an external held-out evaluation showing SA+DEDR discriminates true readings from controls.

**Kind**  
(i) A defect in what the paper says.

---

### 6. The Proto-Dravidian preference is not discriminative by the paper’s own language-family evidence
**(a) Quoted passage**  
§4.4 Limitations: “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”  
§4.4: “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”  
§5 Conclusion: “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

**(b) Defect / limitation**  
The body says the interpretation is not yet discriminative and that existing comparisons are mixed, including an equal Dravidian/Sanskrit fit on HIGH anchors. The conclusion’s “evidence favours a Proto-Dravidian reading framework” is stronger than “compatible with Proto-Dravidian under assumptions.”

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A formal, pre-specified comparison against Proto-Munda, early Indo-Aryan/Sanskrit-side, and language-neutral baselines, with calibrated discrimination metrics and held-out evaluation.

**Kind**  
(i) A defect in what the paper says.

---

### 7. “Three-slot positional grammar” is stronger than the whole-inscription evidence
**(a) Quoted passage**  
Title: “... a Three-Slot Positional Grammar”  
Abstract: “We find robust non-random positional structure … a recurring three-slot positional pattern at the level of individual signs’ positions. Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).”  
§3.2: “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics…”  
§3.2: “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**(b) Defect / limitation**  
The title and framing present a “grammar,” but the paper’s own evidence is sign-level positional regularity, not strong whole-inscription fit: only 5.1% full matches and 38.4% partial matches in one check. The semantic slot labels are explicitly interpretive, and rival template explanations were not tested.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A grammar evaluation on whole inscriptions, with pre-specified rival templates and quantitative model comparison showing the proposed three-slot grammar predicts unseen inscriptions better than alternatives.

**Kind**  
(i) A defect in what the paper says.

---

### 8. The headline positional z-score is arithmetically checkable but not independently reproducible from the paper
**(a) Quoted passage**  
§2.3: “The headline positional statistic (z = 10.3) comes from the Phase-134 F1 test.”  
§2.3: “The z-score can therefore be checked arithmetically from the printed inputs in this section … but the fit itself can be re-run only from the script and the corpus.”  
§2.3: “The Phase-134 JSON record reports the statistic’s inputs and outputs … but not the data matrix, and this section does not reproduce the script’s procedure.”  
§6: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**(b) Defect / limitation**  
The z-score arithmetic is transparent, but the underlying fit and permutation cannot be independently reproduced from the paper because the data matrix and corpus are unavailable and the procedure is not reproduced in the text.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Publish the exact data matrix, corpus, code, inclusion rules, and permutation settings used for Phase-134 F1.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 9. The held-out positional check is weaker than a random or external validation
**(a) Quoted passage**  
§2.3: “The F7 split was by site, not a random selection of seals…”  
§2.3: “Because the split is by site, the check tests whether classes fitted at the large sites predict the classes of signs at other sites; it is not a random held-out sample of seals.”  
§2.3: “over the 87 signs attested in both parts; 85 of those 87 signs were assigned the same dominant class in both parts…”

**(b) Defect / limitation**  
The 97.7% agreement is not a random held-out inscription validation. It is a site-split consistency check over only the 87 signs attested in both parts, measuring stability of dominant positional class, not correctness of readings or grammar semantics.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
External-corpus validation or pre-specified random/sequential held-out tests evaluating predictions at the inscription level, not only repeated sign-class dominance.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 10. The M267 evidence supports “not fish” better than it supports the specific “genitive particle” reading
**(a) Quoted passage**  
§3.4: “The actual fish sign is M047 (frequency=13, P47 in Parpola’s system), verified by crosswalk. M267 is a high-frequency functional/suffixal sign.”  
§3.4: “its distribution across seal motifs does not differ significantly from the counts expected … which is why a motif-bound reading such as ‘fish’ fails and a grammatical-particle reading is preferred.”  
§3.4: “Its current MEDIUM reading is iN/in (genitive particle).”  
§3.4: “This correction is methodologically important: it demonstrates the risk of reading frequency alone as a phonetic indicator.”

**(b) Defect / limitation**  
The presented test shows that M267 is not motif-bound and therefore not the fish sign. It does not establish the specific phonetic value iN/in or the grammatical function “genitive particle.” The paper moves from “fish fails” to “genitive particle preferred” without showing adequate positive evidence for that exact reading in this section.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Independent grammatical evidence for M267 as genitive: paradigmatic alternations, distribution with noun classes, external parallels, DEDR/rebus basis, or successful prediction in held-out inscriptions.

**Kind**  
(i) A defect in what the paper says.

---

### 11. The fish-sign isolation result is not fish-specific
**(a) Quoted passage**  
§3.5: “One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”  
§3.5: “The Phase-127 record, which made this count site by site, gives its own conclusion as ‘UNTESTABLE’ for the same reason.”

**(b) Defect / limitation**  
The fish isolation count cannot test a fish-specific rule because the corpus contains no single-sign inscriptions at all. It only shows that fish-bearing inscriptions in this corpus are multi-sign, as every inscription in the corpus is.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A corpus or object class containing single-sign inscriptions, so fish signs could be compared against other signs for isolation/non-isolation rates.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 12. The Gulf fish-sign extension is not a confirmation and is not reproducible from the recorded search
**(a) Quoted passage**  
§3.19: “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
§3.19: “An absence in catalogue prose is weaker evidence than inspection of the seal images, and we report it as such: the Gulf material provides no counterexample to the Holdat count, but it does not independently confirm it.”

**(b) Defect / limitation**  
The Gulf extension is a text-search absence, not an image-based sign count; the search terms and context enumeration are missing. It cannot independently confirm the fish-sign pattern.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A published inventory of Gulf seal images/contexts, explicit search terms, sign identifications, and a complete context-by-context coding table.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 13. Iconographic enrichment evidence is constrained by data-selected tests, unpublished full table, and circularity risks
**(a) Quoted passage**  
§3.8: “Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”  
§3.8: “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”  
§3.8: “for signs whose reading was itself suggested by the animal motif, ‘the reading matches the animal’ is circular and is not claimed here as validation.”

**(b) Defect / limitation**  
The iconographic test family is selected from observed/filter-passing pairs, the full table is not published, and motif-derived readings are circular as validation. The enrichment can support co-selection for some pairs, but not independent validation of the readings.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Publish the full sign × icon contingency universe, predefine the tested family, provide full 2×2 statistics, and separate confirmatory tests from readings derived from the same iconography.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 14. Iconographic and exclusivity criteria are not independently re-applicable from the paper
**(a) Quoted passage**  
§2.2: “the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record”  
§2.2: “the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table.”  
§2.2: “A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**(b) Defect / limitation**  
Two of the core criteria used for HIGH labels cannot be independently applied from the paper. This limits auditability and makes the HIGH category dependent on internal records and subjective/iconographic coding not documented to normal reproducibility standards.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A written coding protocol, blinded independent coding, inter-coder reliability, and published motif denominators/lift calculations.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 15. Tamil-Brahmi terminal comparison has no cited inventory source and cannot validate Indus readings
**(a) Quoted passage**  
§3.18: “No published source for that 11-category inventory is cited in this paper or in the Phase-155 record; the inventory is the test’s own working list, and the match count can be checked against the record but not against an external authority.”  
§3.18: “Tamil-Brahmi is roughly two thousand years later than the Indus material, so agreement can show only that the proposed endings are of kinds later attested in Dravidian epigraphy — it cannot validate the readings”  
§3.18: “the V07 phonotactic violation rate under the stricter redefined test is 23.4% … concentrated in high-frequency signs.”

**(b) Defect / limitation**  
The 4/7 comparison is not externally grounded by a cited Tamil-Brahmi inventory source, is chronologically remote, and coexists with a substantial phonotactic violation rate in high-frequency signs. It cannot validate the readings.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A cited, externally accepted terminal inventory, pre-registered matching rules, historical controls, and resolution of the phonotactic violation problem.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 16. Text-mining/proximity evidence is under-specified and unbenchmarked
**(a) Quoted passage**  
§2.2: “The Phase-163 mining record does not specify the proximity window … the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded…”  
§3.24: “its recall has never been measured against a hand-checked list of known proposals”  
§7 AI Disclosure: “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect / limitation**  
The text-mining evidence used for literature comparisons and provisional promotions is not fully specified, not benchmarked for recall/precision, and not rerunnable from archived settings. The four PROVISIONAL_MEDIUM promotions are appropriately weakened, but the evidence remains fragile.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Archive OCR inputs, proximity rules, disambiguation rules, model/prompt/settings, and benchmark the mining pipeline against hand-coded literature samples.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 17. Meluhhan personal-name matching provides no discriminative support
**(a) Quoted passage**  
§3.28: “The matching algorithm was intentionally broad.”  
§3.28: “All 25 names produced apparent ‘matches’ at this threshold due to the prevalence of common short readings (ā, kol, il) in the seal set decoded with the 161-anchor reading set…”  
§3.28: “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.”

**(b) Defect / limitation**  
The name-matching test is so broad that every tested name appears to match, driven by common short readings. It supplies no discriminative evidence for the decipherment.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
A stricter pre-specified matching algorithm, negative controls, contextual metadata, and successful discrimination between true candidate names and decoys.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 18. Site-divergence claims are descriptive and weak for Rakhigarhi because of small n and unspecified CI method
**(a) Quoted passage**  
§3.14: “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site, so its distinctiveness should be read as a measured difference on a small sample, not as proof that the difference is not a small-sample effect.”  
§3.14: “Neither the Phase-151 record nor its script names the interval method (percentile, basic, or bias-corrected), so the printed interval is reported as recorded, without a method name.”  
§3.14: “Intervals were computed for that one pair only, so the ordering of the other pairs is descriptive, not interval-tested.”

**(b) Defect / limitation**  
The Rakhigarhi divergence result is based on only 33 seals, with an unspecified bootstrap interval method and intervals for only one pair. It should not be treated as robust site differentiation beyond the measured small-sample description.

**(c) Severity**  
MINOR to MAJOR; MAJOR if used as substantive regional interpretation.

**(d) What would settle it**  
Larger site samples, specified interval method, intervals for all site pairs, and controls for corpus composition/object type.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 19. Master evidence synthesis mixes internal consistency and external evidence
**(a) Quoted passage**  
§3.30: “The items mix two different kinds of check — internal consistency checks (which can show the model agrees with itself) and external comparisons (which can test it against something outside) — and only the second kind is evidence about the world.”  
§3.30: “no single tally at the top labels is printed, because any such tally would mix the two kinds.”

**(b) Defect / limitation**  
The “32 evidence items” tally cannot be read as 32 independent supports for the decipherment. Many are internal consistency checks. The paper discloses this, but any reader-facing synthesis based on the count risks inflating evidential weight.

**(c) Severity**  
MAJOR.

**(d) What would settle it**  
Separate internal consistency checks from external tests, avoid aggregate counts mixing them, and report only external validations as evidentiary support.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

### 20. The paper’s illustrative translations are not tied to identified seals and are not evidence
**(a) Quoted passage**  
§4.1: “The three sequences below are illustrative sequences, built from the model’s readings to show how the grammar is meant to be read. They are sign-number sequences; this paper does not tie them to identified, catalogued seals, and they should not be cited as transcriptions of specific seals.”  
§4.1: “Under the model — and only under the model — these inscriptions read as a directory of guild members rather than a commodity ledger; the two readings have not been separated by any test yet…”

**(b) Defect / limitation**  
The translations are demonstrations of the model, not tested readings of catalogued inscriptions. They cannot be used as validation of the decipherment or of the guild-identity interpretation.

**(c) Severity**  
MINOR, provided they remain illustrative only.

**(d) What would settle it**  
Tie examples to catalogued seals, provide full readings with uncertainty, and test rival functional interpretations.

**Kind**  
(ii) A limitation the paper itself already discloses at the same strength.

---

## Positives checked

### P1. The z-score arithmetic is internally correct from the printed inputs
**Quoted passage checked**  
§2.3: “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

**Check**  
The arithmetic is correct: \((0.9916 - 0.4385) / 0.05347 ≈ 10.344\), which rounds to 10.3.

---

### P2. The H+M token-coverage arithmetic is internally consistent
**Quoted passage checked**  
§3.1: “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%). The remaining 633 tokens (9.04%) have LOW-confidence readings only.”

**Check**  
6,369 + 633 = 7,002.  
6,369 / 7,002 ≈ 90.96%.  
633 / 7,002 ≈ 9.04%.

---

### P3. The “without provisional signs” coverage arithmetic is internally consistent
**Quoted passage checked**  
§3.1: “The four PROVISIONAL_MEDIUM signs (§2.2) account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”

**Check**  
6,369 − 15 = 6,354.  
6,354 / 7,002 ≈ 90.75%.

---

### P4. The M267 motif counts sum correctly
**Quoted passage checked**  
§3.4: “unicorn 147 tokens, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20, script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens in total”

**Check**  
147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = 400.

---

### P5. The M342·M176 PMI example recomputes
**Quoted passage checked**  
§3.7: “M342·M176 occurs 122 times; M342 accounts for 584 of the corpus’s 7,002 sign tokens and M176 for 356 … the pair’s share is taken over all bigram tokens … 5,332 bigram tokens … the printed PMI of 2.43 recomputes…”

**Check**  
Using the paper’s formula:  
P(pair) = 122/5332; P(M342) = 584/7002; P(M176) = 356/7002.  
\(\log_2[(122/5332)/((584/7002)(356/7002))] ≈ 2.43\). Internally sound.

---

### P6. The blocker hypothetical coverage arithmetic is internally consistent
**Quoted passage checked**  
§3.29: “The coverage figure below is therefore checkable from this page: 6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”

**Check**  
6,369 + 97 = 6,466.  
6,466 / 7,002 ≈ 92.35%.

---

### P7. The paper adequately discloses that the fish-sign isolation result is not fish-specific
**Quoted passage checked**  
§3.5: “the corpus contains no single-sign inscriptions of any kind … so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result”

**Check**  
This is a clear and adequate disclosure; the paper does not overstate the fish-isolation count in this passage.

---

### P8. The paper adequately discloses that Phase-170 is only a self-consistency check
**Quoted passage checked**  
§3.31: “This is a self-consistency check, not an accuracy measurement…”  
§3.31: “It is not comparable to Phase-133’s figures…”

**Check**  
The limitation is stated plainly and at appropriate strength.

---

### P9. The paper adequately discloses that internal validation is not external validation
**Quoted passage checked**  
Appendix C: “These are internal consistency checks, not external validation.”  
Appendix C: “this number is not evidence that Dravidian fits better than a rival language…”

**Check**  
The paper correctly prevents the internal foundation suite and old Dravidian lift ratio from being treated as external confirmation.

CALL-META pass2: finish_reason=stop; max_completion_tokens=48000; completion_tokens=9709; prompt_tokens=32220; output_chars=28796.

## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

## PASS 3 — METHODS & REPRODUCIBILITY AUDIT FINDINGS

### 1. §6 commit-pinning / data-availability paragraph is internally inconsistent and not independently checkable from the paper

**Kind:** (i) defect in what the paper says  
**Severity:** MAJOR

**(a) Quoted passage (§6 Data Availability, whole paragraph audited sentence-by-sentence):**

1. “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 649e0e75).”

**Verdict:** Not literally secure as written. Later sentences say the named commit cannot contain the same first sentence and that a later “pin commit” changes the commit string. Therefore “the version of the paper you are reading is on … commit 649e0e75” conflicts with the later explanation unless “version” is being used non-literally.

2. “The DOI named on the title page identifies this preprint and its version record on Zenodo.”

**Verdict:** Could be literally true, but cannot be checked from the paper text alone.

3. “The text of this draft is identified by the branch and commit named here, together with the one-string difference explained below, not by the DOI.”

**Verdict:** This is more precise than sentence 1, but it contradicts the title-page statement: “the exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.” The §6 sentence adds a “one-string difference,” so the commit alone does not identify the exact text.

4. “The supplemental files named in this paper (the anchor table, the status audit, and the CSV supplements in research/indus/supplemental/) are in the same repository at the same commit; no separate archive copy of them exists yet.”

**Verdict:** Could be true, but the paper provides no independent checksum, file listing, archive, or printed table sufficient to verify it from the paper alone. The lack of separate archive is a reproducibility weakness.

5. “The commit named here is the revision commit: the commit at which this paper’s text was frozen for the current round.”

**Verdict:** Not literally compatible with sentences 6–8. If the named commit contains a different commit string in the first sentence, and a following “pin commit” changes that string, then the paper text was not frozen at the named commit in the form read by the reader.

6. “A commit cannot contain its own hash, so the copy of this section at the named commit names, in its first sentence, the commit that the revision started from.”

**Verdict:** The general Git point is plausible, but it proves that the text at the named commit is not identical to the text of §6 as printed here.

7. “The draft in hand differs from the text at the named commit in that one commit string, and in no other sentence.”

**Verdict:** This is an unverifiable self-referential identity claim from the paper alone. No previous commit string, diff, checksum, or named pin commit is supplied in the paper.

8. “The commit that follows the named commit on this branch and changes that string — the pin commit — changes no other paper text, and the records commits that follow it (the rebuilt PDF, the version note, and the records of later rounds) change no paper text at all.”

**Verdict:** Not checkable from the paper. The “pin commit” is not named. “The records commits” also appears syntactically defective, making the claim harder to interpret literally.

9. “The anchor table is research/indus/anchor_table.csv: it has 397 rows — one for every sign in the Mahadevan catalogue — of which 161 are the HIGH/MEDIUM rows this paper’s headline claims rest on and the other 236 carry LOW readings; each row gives the sign’s reading and basis, and a DEDR citation is recorded in the table’s DEDR column on 15 rows, all of them among the 161; the full 397-sign inventory, with each sign’s status and corpus frequency, is glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv; per-phase results are in backend/reports/.”

**Verdict:** The paper asserts the existence and contents of central evidence tables but does not print them. From the paper alone, the row counts, DEDR-column count, and per-sign bases cannot be verified.

10. “Neither table is printed in this paper; both are in the repository, on the branch and at the commit named above.”

**Verdict:** Literally clear and important. It confirms that the paper itself omits the central tables.

11. “Both tables are the paper’s central evidence.”

**Verdict:** Literally clear and damaging for reproducibility: the central evidence is not in the paper.

12. “Selected rows from the anchor evidence are printed in this paper — in §3.3 and in Appendix A — as illustrations only; the complete tables are printed nowhere in this paper and are in the repository.”

**Verdict:** Literally clear. It confirms that the printed paper is insufficient to audit the complete evidence base.

13. “A reader who wants to check any single reading should go to the anchor table itself, at the commit named in §6, rather than to the examples in §3.3.”

**Verdict:** This directs verification outside the paper. Because the commit identity is itself not cleanly pinned in the paper, this is not an adequate paper-internal reproducibility route.

14. “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**Verdict:** Literally clear. This is a decisive reproduction blocker for corpus-level counts.

15. “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**Verdict:** Literally clear and adequately disclosed. It means the headline corpus-level results cannot be independently re-run by ordinary readers.

16. “Supplemental datasets (fish-sign compound-context listing, iconographic formula enrichment table, formula bigram table, and positional grammar permutation summary) are available in research/indus/supplemental/.”

**Verdict:** Could be true, but from the paper alone there is no file manifest, checksum, or archive copy. Also, other sections state some full tables are not published, so “supplemental datasets” are only partial.

**(b) Defect:** The data-availability paragraph tries to use a branch/commit as the exact text identifier while simultaneously saying the named commit cannot contain the same text and that an unnamed later “pin commit” changes the paper text. The paper also admits that the central evidence tables and the corpus are outside the paper, with the corpus not public.

**(d) What would settle it:** A named immutable archive containing the exact PDF/source text, all supplemental files, checksums, the exact corpus or a public replacement, and a literal Git diff showing the one-string-only change and the unnamed pin commit.

---

### 2. Headline corpus-level results cannot be reproduced because the primary corpus is private

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** CRITICAL

**(a) Quoted passage (Abstract):** “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

**Additional quoted passage (§6):** “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**(b) Defect / limitation:** The paper’s central numerical claims—token coverage, seal coverage, positional counts, fish-sign counts, bigram counts, motif counts, site divergences—depend on a corpus readers cannot inspect or rerun.

**(d) What would settle it:** Public release of the Holdat corpus with stable sign encodings, inscriptions, site/motif metadata, and license terms allowing independent reproduction; or rerunning all headline analyses on a public corpus with a documented crosswalk.

---

### 3. Corpus selection denominator is undefined: the paper does not state what share of formal Indus seals the Holdat corpus represents

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.1 Corpus):** “It consists of formal stamp seals from those sites; what share of the full published formal-seal assemblage its 1,670 seals represent is not measured in this paper, and no claim about that share is made.”

**(b) Defect / limitation:** The paper cannot support general claims about “formal stamp seals” or site patterns beyond this private corpus, because the sampling frame and coverage fraction are not measured.

**(d) What would settle it:** A complete inclusion/exclusion protocol: source catalogues, object IDs, omitted objects, object classes, damaged/ambiguous inscriptions, duplicates, and per-site coverage relative to a defined published assemblage.

---

### 4. The anchor table is central evidence but absent from the paper

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§6):** “Both tables are the paper’s central evidence. Selected rows from the anchor evidence are printed in this paper — in §3.3 and in Appendix A — as illustrations only; the complete tables are printed nowhere in this paper and are in the repository.”

**(b) Defect / limitation:** The paper’s sign-by-sign evidentiary basis cannot be audited from the paper itself. This is especially serious because the claims are sign-specific decipherment claims.

**(d) What would settle it:** Print or archive the complete anchor table and status audit as citable supplemental material with checksums and version identifiers.

---

### 5. HIGH-confidence labels cannot be independently verified from the stated criteria

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.2 Evidence Hierarchy):** “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field, so questions of the form ‘which signs meet criterion X but not criterion Y’ cannot always be answered from the records”

**Additional quoted passage (§2.2):** “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect / limitation:** The confidence categories are not auditable as rule applications. The paper states criteria but the records do not preserve criterion-by-criterion decisions.

**(d) What would settle it:** A per-sign matrix with each criterion as a separate field, raw counts, motif denominators, terminal-token counts, coder decisions, and allograph-distance calculations.

---

### 6. Iconographic coding lacks a protocol, blinding, and reliability assessment

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.2 Evidence Hierarchy):** “the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record”

**(b) Defect / limitation:** Many HIGH readings rest on iconography or motif exclusivity, but the procedure for assigning iconographic matches is not reproducible or protected against expectation bias.

**(d) What would settle it:** A blinded coding protocol, multiple independent coders, inter-coder reliability, object-level images or catalogue references, and pre-registered rules for ambiguous shapes.

---

### 7. DEDR rebus matching lacks candidate logs and multiple-comparison control

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.2 Evidence Hierarchy):** “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”

**(b) Defect / limitation:** The paper cannot estimate or control the false-positive rate of dictionary matching. This is central because DEDR rebus matches are a major route to MEDIUM and some HIGH readings.

**(d) What would settle it:** A complete search log: all candidate forms considered per sign, allowed transformations, rejection reasons, dictionary search space, and a formal null/multiple-testing correction.

---

### 8. SA simulation is not reproducible: training corpus, syllable inventory, and size are unnamed

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.4 Syllabic Language Model):** “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

**(b) Defect / limitation:** The simulated-annealing language model cannot be rerun or evaluated because its training data are unspecified.

**(d) What would settle it:** Archive the exact training corpus, syllabification rules, inventory, preprocessing scripts, model parameters, random seeds, and outputs.

---

### 9. SA agreement failed its own held-out test but still contributes to the headline set

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.4):** “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

**Additional quoted passage (§2.4):** “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect / limitation:** A method found non-discriminative by the paper’s own held-out test remains part of the promotion route for 43 MEDIUM signs. The paper discloses this, but it materially weakens the headline 161-sign / 90.96% coverage claim.

**(d) What would settle it:** Recompute headline coverage after removing or independently validating all SA-involved signs; or demonstrate calibrated predictive value on a known deciphered script under the same protocol.

---

### 10. The 0.15 SA threshold is arbitrary and uncalibrated

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.4):** “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”

**(b) Defect / limitation:** The MEDIUM promotion threshold has no empirical meaning as a confidence standard.

**(d) What would settle it:** Calibration on known corpora using the same inscription lengths, sign frequencies, dictionary search procedure, and promotion criteria.

---

### 11. Phase-134 headline permutation test cannot be exactly rerun from the record

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.3 Positional Analysis):** “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

**Additional quoted passage (§2.3):** “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script … this section does not reproduce the script’s procedure.”

**(b) Defect / limitation:** The paper’s strongest statistical result depends on a script and corpus rather than a fully specified method in the paper; exact rerun is blocked by missing seed and private corpus.

**(d) What would settle it:** Publish the corpus, exact permutation code, random seed, data matrix, inclusion rules, and a worked definition of the R² statistic.

---

### 12. The held-out positional check is not a random held-out sample despite being a “held-out” validation

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MINOR

**(a) Quoted passage (§2.3):** “The F7 split was by site, not a random selection of seals … Because the split is by site, the check tests whether classes fitted at the large sites predict the classes of signs at other sites; it is not a random held-out sample of seals.”

**(b) Defect / limitation:** The validation question is narrower than a generic train/test claim: it is a large-site-to-smaller-site transfer test over 87 shared signs.

**(d) What would settle it:** Add pre-specified random splits, site-stratified splits, and object-level splits with seeds and confidence intervals.

---

### 13. Phase-143 iconographic enrichment uses data-selected tests and an unpublished full test family

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.8 Iconographic Cross-Encoding):** “Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”

**Additional quoted passage (§3.8):** “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”

**(b) Defect / limitation:** The multiple-testing denominator and full test family cannot be reconstructed from the paper or published supplements. The tested family is post-selected from observed data.

**(d) What would settle it:** Publish all possible and all tested sign × icon pairs, filters, raw contingency tables, expected counts, full 2×2 chi-square values, and corrected p-values.

---

### 14. Several statistical outputs depend on records whose rules are incomplete or missing

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.28 Expanded Meluhhan Name Matching):** “The record does not state a fuller rule for how a single segment counts as matched, and none is claimed here.”

**Additional quoted passage (§3.31 Grammar Variance Retest):** “The Phase-170 record states the rules in the order TERMINAL, INITIAL, MEDIAL, else MIXED; it does not state what happens when a sign’s rates satisfy more than one threshold, and that tie/overlap handling is not on record.”

**Additional quoted passage (§3.14 Site Repertoire Divergence Bootstrap):** “Neither the Phase-151 record nor its script names the interval method (percentile, basic, or bias-corrected), so the printed interval is reported as recorded, without a method name.”

**(b) Defect / limitation:** Multiple reported checks cannot be fully rerun or interpreted because key operational rules are missing.

**(d) What would settle it:** Freeze and publish complete specifications for segment matching, threshold tie handling, and bootstrap interval calculation.

---

### 15. Text-mining evidence is not reproducible because model/prompt/settings and recall/precision are absent

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§7 AI Disclosure):** “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**Additional quoted passage (§3.24):** “its recall has never been measured against a hand-checked list of known proposals”

**(b) Defect / limitation:** Literature-mining counts and proximity hits cannot be independently regenerated. Their sensitivity and error rates are unknown.

**(d) What would settle it:** Archive source texts, OCR versions, search terms, prompts, model versions, scripts, random settings, hit lists, and a hand-coded benchmark estimating recall/precision.

---

### 16. Four PROVISIONAL_MEDIUM promotions rest on partially recorded text-proximity rules

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.2):** “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded”

**(b) Defect / limitation:** The four provisional upgrades cannot be reproduced from the stated method.

**(d) What would settle it:** Specify the proximity window, OCR source/version, sign-number disambiguation rules, all hits, false-positive handling, and expert verification.

---

### 17. The fish-sign isolation test is structurally untestable in this corpus

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.5 Fish Sign Isolation Test):** “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”

**(b) Defect / limitation:** The fish-specific hypothesis cannot be tested in a corpus where no sign can possibly appear isolated.

**(d) What would settle it:** Test an object class or corpus containing single-sign inscriptions, with pre-defined fish-family membership and object-level inclusion rules.

---

### 18. Fish-family supplemental listing is internally mismatched with the printed family list

**Kind:** (i) defect in what the paper says  
**Severity:** MAJOR

**(a) Quoted passage (§3.5):** “Testing the full fish sign family — M047, M049, M052, M053, M054, M055, M056, M145, the signs this program’s Mahadevan–Parpola crosswalk file lists as fish-shaped — across all 9 sites.”

**Additional quoted passage (§3.5):** “The supplemental file fish_sign_compound_context.csv lists 27 compound occurrences with their contexts (13 for M047 and 14 for M001; M001 is not in the family list printed above, and that mismatch is on record and unresolved).”

**(b) Defect:** The paper’s fish-family evidence file includes M001, which is explicitly not in the printed fish family, and the mismatch is unresolved.

**(d) What would settle it:** Correct the supplemental file or the family definition, document the source for each fish-shape classification, and rerun the counts.

---

### 19. Gulf fish-sign text search is not reproducible because search terms and context enumeration are absent

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.19 Gulf Seal Fish-Sign Test):** “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”

**(b) Defect / limitation:** The Gulf comparison cannot be independently checked from the described method.

**(d) What would settle it:** Publish the extracted texts, exact search terms, scripts, all hits/non-hits, and the 27 catalog contexts with object identifiers.

---

### 20. Some reported percentages are explicitly “uncountable” because numerators and denominators are absent

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.10 Cross-Corpus Structural Comparisons):** “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed”

**(b) Defect / limitation:** The 87.08% CISI opening-sign claim is not reproducible even from the program’s own records.

**(d) What would settle it:** Provide numerator, denominator, inscription IDs, sign crosswalk, and code.

---

### 21. Phonological exclusivity test uses unsourced working inventories

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.11 Phonological Exclusivity Test):** “Both sound inventories used in this test are the test’s own working lists, printed in full in this section and existing nowhere else in this program’s records; no published Sanskrit or Dravidian phoneme-inventory source is cited, because none was used.”

**(b) Defect / limitation:** The test cannot support language-family discrimination beyond the paper’s own ad hoc phoneme lists.

**(d) What would settle it:** Use cited historical phonological inventories with justified time-depth assumptions and pre-registered marker definitions.

---

### 22. Tamil-Brahmi terminal comparison uses an uncited 11-category inventory

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.18 Tamil-Brahmi Terminal Comparison):** “No published source for that 11-category inventory is cited in this paper or in the Phase-155 record; the inventory is the test’s own working list, and the match count can be checked against the record but not against an external authority.”

**(b) Defect / limitation:** The comparison’s denominator and category set are not externally grounded.

**(d) What would settle it:** Cite a Tamil-Brahmi epigraphic source for the category inventory and predefine matching rules before counting.

---

### 23. Vowel-harmony validation is unresolved and internally inconsistent across runs

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.17 Vowel Harmony Methodology Resolution):** “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1% …”

**Additional quoted passage (§3.17):** “No one of these three procedures is currently the program’s authoritative V12 test: the records disagree because the test was redefined between runs, and the full rule changes are not recorded for every version.”

**(b) Defect / limitation:** A major phonological consistency check has no frozen protocol and gives sharply different results.

**(d) What would settle it:** Freeze one V12 protocol, document all rule changes, rerun on the current 161-sign set, and report sign-level failures.

---

### 24. V07 phonotactic violations hit headline signs, weakening the reading set

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.18):** “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

**Additional quoted passage (§3.18):** “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**(b) Defect / limitation:** The phonotactic problem is not confined to rare speculative signs; it affects high-frequency signs central to the model.

**(d) What would settle it:** Provide sign-level phonotactic rules, rerun under a frozen protocol, and revise or justify readings driving violations.

---

### 25. No formal rival-model comparison exists for the main semantic interpretation

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.2 Grammar Model):** “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**Additional quoted passage (§4.5 Validation Path):** “a future test of this kind could separate the guild-identity interpretation from the commodity-tally model only if the two are first made to predict different things … No such discriminating prediction is yet on record”

**(b) Defect / limitation:** The statistics support positional non-randomness, not the classifier/title/name semantic interpretation.

**(d) What would settle it:** Pre-register rival generative models with different predictions and compare them on held-out inscriptions or independent corpora.

---

### 26. Language-family baseline comparison is incomplete

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§4.4 Limitations):** “The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

**(b) Defect / limitation:** The paper cannot establish Dravidian superiority over alternatives; it can only claim compatibility under its own assumptions.

**(d) What would settle it:** Equal-effort, pre-registered baseline models for Proto-Munda, early Indo-Aryan, and non-linguistic systems with the same data, search space, and evaluation metrics.

---

### 27. §2.1.1 uses comparison datasets with no §8 references or bibliographic identification

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§2.1.1):** “this paper gives no §8 entry and no fuller bibliographic identification for the Dering Roll source, the Mesopotamian numerical-sign table, or DAMOS (the source of the Linear B transliterations), and the Shakti corpus and the ICIT line are likewise identified only through that record.”

**(b) Defect / limitation:** The frequency-curve control comparison cannot be independently sourced from the reference list.

**(d) What would settle it:** Add full references or archived datasets for the Dering Roll, Mesopotamian numerical signs, DAMOS, Shakti corpus, and ICIT lineage.

---

### 28. CISI and mayig are used without §8 references

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.10):** “CISI is the Corpus of Indus Seals and Inscriptions; neither it nor the mayig digitization has a §8 entry, and this paper can give no fuller bibliographic identification for either from its records.”

**(b) Defect / limitation:** The cross-corpus comparison lacks complete source identification.

**(d) What would settle it:** Add full bibliographic and dataset references for CISI and the mayig digitization, with access details and version identifiers.

---

### 29. Shu-ilishu external facts lack §8 support

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.15 Shu-ilishu Phonological Test):** “The external facts in this section (the Ur III date, c. 2020 BCE; the title ‘interpreter of the Meluhha language’; the provenance recorded as ‘excavated at Ur, held at British Museum’) are as recorded in the Phase-152 record … which is the source this section relies on; no §8 entry covers them.”

**(b) Defect / limitation:** The paper relies on external historical/provenance facts without a citable reference.

**(d) What would settle it:** Cite the object publication, museum record, or relevant scholarly source in §8.

---

### 30. Arthaśāstra analogy is uncited

**Kind:** (i) defect in what the paper says  
**Severity:** MINOR

**(a) Quoted passage (§4.1):** “The Arthaśāstra (a layered Sanskrit text whose core is usually placed in the last centuries BCE, roughly a millennium and a half after the end of the IVC period) documents Sanskrit superintendent titles of a broadly similar kind — koṣṭhāgārādhyakṣa (storehouse superintendent), nāvadhyakṣa (ship superintendent).”

**(b) Defect:** No §8 reference is provided for the Arthaśāstra statement, dating claim, or cited Sanskrit titles.

**(d) What would settle it:** Add a reference to the edition/translation or scholarly work used for the Arthaśāstra claims.

---

### 31. §8 contains at least one reference entry not actually cited in the paper body

**Kind:** (i) defect in what the paper says  
**Severity:** MINOR

**(a) Quoted passage (§8 References):** “Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”

**Relevant in-text passage (§1.2):** “Rao et al. (2009, Science 324:1165) reported that IVS sign entropy falls in the range of known linguistic systems”

**(b) Defect:** The paper cites the Science entropy paper in the text, and §8 also lists a PNAS Markov-model paper. I find no in-text citation to the PNAS paper by title, venue, or result. If it is intended to support the entropy discussion, the text points instead to Science 324:1165.

**(d) What would settle it:** Either cite the PNAS paper where used, or remove it from §8.

---

### 32. §8 reference “Jha & Rajaram (2000)” is incomplete relative to normal bibliographic standards

**Kind:** (i) defect in what the paper says  
**Severity:** MINOR

**(a) Quoted passage (§8 References):** “Jha & Rajaram (2000). The Deciphered Indus Script. New Delhi: Aditya Prakashan.”

**(b) Defect:** The author initials/full names are omitted, unlike most other references. This impairs unambiguous identification.

**(d) What would settle it:** Provide full author names or initials consistently.

---

### 33. §8 reference “Crawford (2001)” is incomplete and its use is not traceable in the results

**Kind:** (i) defect in what the paper says  
**Severity:** MINOR

**(a) Quoted passage (§2.1):** “Supplementary sources: Crawford (2001), used only for the Saar/Dilmun seal comparanda”

**Additional quoted passage (§8):** “Crawford, H. (2001). Early Dilmun Seals from Saar: Art and Commerce in Bronze Age Bahrain.”

**(b) Defect:** The reference lacks publisher/place details, and the paper does not present a clearly traceable Saar/Dilmun comparandum result tied to Crawford. The citation is present, but the support role is opaque.

**(d) What would settle it:** Add full bibliographic details and specify exactly where Crawford supports a stated comparison.

---

### 34. Some references are used only through the program’s own mining summaries, not as quoted or manually checked support

**Kind:** (ii) limitation the paper itself already discloses at the same strength  
**Severity:** MAJOR

**(a) Quoted passage (§3.20):** “we cite this as our mining summary of the book, not as a quotation.”

**Additional quoted passage (§3.23):** “These are one scholar’s works across 1972–2018, not independent witnesses, and ‘consistent with’ here means only that the mining found classifier/title/suffix terminology and positional classes of the kinds the model uses.”

**(b) Defect / limitation:** Several literature-support claims are mediated by unvalidated mining rather than direct, auditable citation to passages.

**(d) What would settle it:** Provide the exact quoted passages, page numbers, coding rules, and a hand audit.

---

### 35. The paper’s “all scripts can be re-run” style claims overstate what can be rerun without the corpus

**Kind:** (i) defect in what the paper says  
**Severity:** MAJOR

**(a) Quoted passage (Abstract):** “it proposes a falsifiable computational model whose method and repository artefacts (scripts, phase reports, and the anchor table) can be re-run and checked.”

**Additional quoted passage (Abstract):** “The corpus-level counts in this paper cannot be re-run until the corpus itself is released”

**(b) Defect:** The first sentence is too broad unless restricted to non-corpus artefacts. The same abstract immediately concedes that most corpus-level quantities cannot be rerun.

**(d) What would settle it:** Rephrase to distinguish script execution from reproduction of corpus-dependent results, or release the corpus.

---

## POSITIVES CHECKED

1. **The paper correctly discloses that “coverage” is assignment coverage, not validation.**  
   **Passage checked (Abstract):** “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
   **Assessment:** Adequately disclosed and internally important.

2. **The arithmetic for the headline H+M token coverage is internally consistent.**  
   **Passage checked (§3.1):** “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%).”  
   **Check:** 6,369 / 7,002 = 0.9096.

3. **The arithmetic for removing the four provisional signs is internally consistent.**  
   **Passage checked (§3.1):** “The four PROVISIONAL_MEDIUM signs (§2.2) account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%)”  
   **Check:** 6,369 − 15 = 6,354; 6,354 / 7,002 ≈ 90.75%.

4. **The z-score arithmetic is internally consistent from the printed inputs.**  
   **Passage checked (§2.3):** “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **Check:** The calculation is correct to the stated rounding.

5. **The paper honestly distinguishes positional statistics from semantic interpretation.**  
   **Passage checked (§3.2):** “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics”  
   **Assessment:** Adequately disclosed.

6. **The fish-sign result is correctly downgraded as not fish-specific.**  
   **Passage checked (§3.5):** “the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”  
   **Assessment:** This is an honest limitation stated at full strength.

7. **The paper correctly refuses to combine the Holdat fish count with the Gulf text-search result.**  
   **Passage checked (§3.19):** “They are not combined with the Holdat count, no combined figure is used anywhere in this paper, and the two results should always be cited separately”  
   **Assessment:** Internally sound disclosure.

8. **The paper distinguishes internal consistency checks from external validation.**  
   **Passage checked (Appendix C):** “These are internal consistency checks, not external validation.”  
   **Assessment:** Correct and important.

9. **The paper discloses that the Phase-170 grammar retest is self-consistency, not accuracy.**  
   **Passage checked (§3.31):** “This is a self-consistency check, not an accuracy measurement”  
   **Assessment:** Adequately disclosed.

10. **The paper acknowledges the absence of a discriminating Dravidian-vs-rival baseline.**  
   **Passage checked (§4.4):** “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary”  
   **Assessment:** Honest limitation.

11. **Most named in-text scholarly citations have corresponding §8 entries.**  
   **Checked examples:** Mahadevan 1977/1981/1982/1986/1989/2011; Parpola 1994/2010; Farmer, Sproat & Witzel 2004; Witzel 1999; Southworth 2005; Lubotsky 2001; McAlpin 1981; Hojlund & Abu-Laban 2012; Laursen 2010; Mitchell 1986; Nair 2026; Roif 2025a/2025b; Krishnamurti 2003; Yadav et al. 2010.  
   **Assessment:** Apart from the gaps reported above, the main named citations are represented in §8.

12. **The paper is unusually explicit about unreproducible or weak components.**  
   **Passage checked (§7 AI Disclosure):** “no benchmark of the mining pipeline’s recall or precision exists”  
   **Assessment:** This is a proper disclosure, even though it weakens the method.

CALL-META pass3: finish_reason=stop; max_completion_tokens=60000; completion_tokens=12061; prompt_tokens=32221; output_chars=40507.

## PASS 4 — HOSTILE SUMMARY

## (1) Numbered findings, ordered most-serious first

### 1. The paper’s headline corpus-level claims are not independently reproducible because the corpus is private.
**(a) Quoted passage:**  
Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
§6 Data Availability: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect:**  
Most headline numbers—7,002 tokens, 1,670 seals, 90.96% token coverage, 69.8% seal coverage, positional statistics, motif distributions, fish counts, bigrams, site divergences—are corpus-level claims. The paper itself says these cannot currently be re-run by independent researchers. This is fatal to independent verification of the computational evidence as presented.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Public release of the exact Holdat corpus version used, or deposit of a fully auditable, rights-cleared token/sign/site/motif table sufficient to recompute every corpus-level statistic.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 2. The 161 “candidate Proto-Dravidian anchors” have no measured error rate, and the DEDR matching procedure does not record the search space, rejected candidates, or multiple-comparison control.
**(a) Quoted passage:**  
§2.2 Evidence Hierarchy: “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
§2.2: “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect:**  
The central decipherment claim rests on assigned readings, but the paper gives no calibrated false-positive rate for HIGH/MEDIUM labels and no auditable record of the DEDR search process. Without rejected candidates, allowed transformations, and multiple-comparison accounting, the reader cannot distinguish meaningful rebus matches from post-hoc selection among many possible Dravidian forms.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
A preregistered or fully recorded matching protocol listing all candidate readings considered per sign, allowed phonological transformations, rejection criteria, and an empirical or simulated null estimating the chance rate of DEDR matches at the accepted quality threshold.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 3. The paper says no reader can verify that any HIGH sign actually meets the stated HIGH criteria as worded.
**(a) Quoted passage:**  
§2.2 Evidence Hierarchy: “Three of the criteria above are stated at the level this program’s records support and no further: the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record; ‘cases’ in the terminal-marker criterion means the sign’s corpus tokens; and the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table. A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”  
§2.2: “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect:**  
The paper’s strongest anchor category, HIGH, is not independently checkable against its own stated rule. The records apparently preserve coarse evidence-type labels, not criterion-by-criterion pass/fail evidence. This directly undermines the 75 HIGH anchors and the 70.34% token coverage attributed to them.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
For every HIGH sign: publish the criterion-level evidence table, motif denominators, iconographic coding protocol, coder assignments/blinding status, inter-coder reliability, and exact computation showing which two criteria are satisfied.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 4. The syllabic language model failed its own held-out test, yet 43 MEDIUM signs still depend on the combined SA+DEDR route and a true SA-free headline cannot be computed.
**(a) Quoted passage:**  
§2.4 Syllabic Language Model: “And a later test inside this program (Phase-107, October 2026) put the SA machinery itself to a held-out test whose protocol, primary metric, and discrimination rule were fixed in advance in this program’s Spec 005 … Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”  
§2.4: “43 MEDIUM signs, accounting for 398 corpus tokens, carry that combined evidence type in ANCHOR_STATUS_AUDIT.csv.”  
§2.4: “If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain. That is a bound, not a recomputed headline: the audit file does not record whether any of the 43 also meets a non-SA MEDIUM criterion … so a true SA-free headline cannot be computed from the records.”

**(b) Defect:**  
A major route to MEDIUM status uses a model that, by the paper’s own account, showed zero held-out agreement and was indistinguishable from Sanskrit and scrambled controls. The paper cannot reconstruct which of the affected readings would survive without SA. Therefore the 161-anchor / 90.96% headline includes an inseparable block of readings supported partly by a failed mechanism.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Re-audit the 43 signs criterion-by-criterion without SA support, publish which survive on independent non-SA evidence, and rerun coverage metrics on that audited SA-free set.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 5. The paper has not shown that Proto-Dravidian is superior to rival linguistic or non-linguistic explanations.
**(a) Quoted passage:**  
§4.4 Limitations: “Language-family baseline: The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian. For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”  
§5 Conclusion: “The corpus shows non-random positional structure of the kind a writing system produces and also of the kind some non-linguistic marking systems produce; the tests in this paper do not separate those two, and the frequency-curve evidence that might have spoken to the question was uninformative (§2.1.1).”

**(b) Defect:**  
The headline frames the work as a Proto-Dravidian decipherment hypothesis, but the paper admits that the evidence is compatible rather than discriminative: no formal Proto-Munda / early Indo-Aryan / language-neutral comparison has established superiority, Dravidian-vs-Sanskrit tests are mixed, and the structural tests do not separate writing from non-linguistic marking systems.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
A controlled model comparison against explicit Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan, and non-linguistic administrative-mark baselines using the same corpus, same scoring rules, preregistered metrics, and held-out validation.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 6. The strongest phonological checks expose unresolved problems, including a 23.4% phonotactic violation rate concentrated in headline signs.
**(a) Quoted passage:**  
§3.17 Vowel Harmony Methodology Resolution: “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”  
§3.17: “We therefore withdraw the earlier description of V12 as a settled methodology artifact: vowel harmony is an open problem for the reading set…”  
§3.18 Tamil-Brahmi Terminal Comparison: “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”  
§3.18: “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**(b) Defect:**  
The proposed reading set fails or remains unresolved on internal phonological diagnostics. The problem is not confined to rare marginal signs: it is concentrated in frequent, headline anchors such as M211, M176, and M342. That directly weakens the claimed Proto-Dravidian reading framework.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Freeze a single phonological test protocol, rerun it on the current 161-sign set, publish per-sign failures, and either revise readings to reduce violations under independently justified rules or show by external comparison that the violation rate is expected for genuine Proto-Dravidian-like inscriptions.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 7. The “three-slot grammar” has strong positional regularity, but its semantic interpretation as classifier/title/name is not established, and rival templates were not tested.
**(a) Quoted passage:**  
§3.2 Grammar Model: “Positional statistics establish the three positions and which signs favour each. The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics…”  
§3.2: “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”  
§3.2: “Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).”

**(b) Defect:**  
The positional test may show non-random ordering, but it does not establish the proposed administrative grammar or its semantic slot labels. The paper’s own full-inscription match rate is low, and no rival functional templates were tested. Thus the headline “three-slot positional grammar” is much stronger than the semantic evidence actually supports.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Formal comparison of the classifier/title/name model against explicit owner-mark, commodity-mark, clan-emblem, cultic, and non-linguistic administrative templates, with preregistered likelihood or predictive criteria and held-out inscriptions.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 8. The main positional z-score is arithmetically checkable but not independently reproducible from the paper, because the fit definition, data matrix, seed, inclusion rules, and corpus are not supplied.
**(a) Quoted passage:**  
§2.3 Positional Analysis: “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”  
§2.3: “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script…”  
§2.3: “The z-score can therefore be checked arithmetically from the printed inputs in this section … but the fit itself can be re-run only from the script and the corpus.”

**(b) Defect:**  
The paper’s strongest structural statistic is only partially auditable from the text. The reader can recompute the z-score from printed summary numbers, but cannot reproduce the underlying fit without the private corpus and repository code, and cannot exactly rerun the permutation from the record.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the input matrix, exact inclusion rules, code version, random seed, and corpus table used for Phase-134, plus a standalone reproduction script.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 9. The headline “coverage” is assignment coverage, not verification, so 90.96% token coverage does not mean 90.96% decipherment.
**(a) Quoted passage:**  
Abstract: “These readings are assigned to signs that together account for 90.96% of the corpus’s sign tokens (69.8% of seals consist entirely of such signs). ‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
§5 Conclusion: “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage — assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings)…”

**(b) Defect:**  
The coverage number can easily be mistaken for decipherment coverage, but the paper admits it is merely the share of tokens whose signs have assigned candidate readings. Since the readings are unverified and have no calibrated error rate, the coverage statistic does not establish decipherment success.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Independent validation of readings on held-out inscriptions, external bilingual/name anchors, or a calibrated benchmark showing expected accuracy of HIGH/MEDIUM labels.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 10. The fish-sign isolation result is not fish-specific and cannot support a fish-sign functional rule.
**(a) Quoted passage:**  
Abstract: “That count is not fish-specific evidence: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9), so no sign of any family can occur isolated in it…”  
§3.5 Fish Sign Isolation Test: “One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”  
§3.19 Gulf Seal Fish-Sign Test: “the Gulf material provides no counterexample to the Holdat count, but it does not independently confirm it.”

**(b) Defect:**  
The fish-sign isolation count cannot discriminate a fish-specific rule from a corpus-wide absence of single-sign inscriptions. The Gulf text search adds no confirmation. Therefore this result should carry essentially no evidential weight for fish-sign semantics.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A corpus or object class containing single-sign inscriptions, with enough fish and non-fish signs to test whether fish signs are uniquely or disproportionately non-isolated.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 11. The external personal-name tests do not validate the readings.
**(a) Quoted passage:**  
§3.15 Shu-ilishu Phonological Test: “No seal in the corpus matched three or more of the four slots (Phase-152: candidate seals = 0).”  
§3.15: “Result: NO_SEAL_MATCH — partial inventory overlap only (2 of 4 slots covered; candidate seals = 0).”  
§3.28 Expanded Meluhhan Name Matching: “All 25 names produced apparent ‘matches’ at this threshold due to the prevalence of common short readings (ā, kol, il) in the seal set decoded with the 161-anchor reading set…”  
§3.28: “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.”

**(b) Defect:**  
The attempted external anchors fail to provide discriminative support. Shu-ilishu gives no seal match, and the expanded Meluhhan name test is swamped by common short readings. The model therefore lacks successful external phonological validation.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
A preregistered external-name matching test with a stricter matching algorithm, negative controls, expected false-match rates, and successful held-out matches not driven by high-frequency generic syllables.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 12. The paper’s own validation path says none of its three falsification points is an available open test on current data.
**(a) Quoted passage:**  
§4.5 Validation Path: “The candidate model is falsifiable in principle at the first of the following points. None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”  
§4.5: “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**(b) Defect:**  
The title and abstract emphasize falsifiability, but the concrete validation path contains no currently available decisive test: one awaits a future bilingual, one already failed to confirm, and one has no discriminating prediction. The model is “falsifiable in principle,” but not yet operationally falsifiable on available evidence.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
State precise, risky, currently executable predictions distinguishing the model from named rivals, and run them on public or independently accessible data.

**Kind:** (i) defect in what the paper says, because the headline emphasis on a “falsifiable computational decipherment hypothesis” is stronger than the operational tests the paper says currently exist.

---

### 13. The four provisional sibilant promotions rest on partly recorded OCR text-proximity rules, not verified sign assignments.
**(a) Quoted passage:**  
§2.2 Evidence Hierarchy: “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded…”  
§3.25 Sibilant Exploratory Promotions: “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign”  
§3.27 Sibilant DEDR Check: “This check uses the same framework that proposed the readings; it is not cross-validation and not independent confirmation.”

**(b) Defect:**  
Four of the 161 H+M readings are included in headline coverage despite being based on unverified OCR proximity counts with incomplete generating rules. The later DEDR check is within-model plausibility, not independent validation.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Manual expert verification of each claimed source passage, with exact page/figure/sign references, fixed proximity rules, OCR sources, ambiguity-resolution rules, and independent review.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

### 14. The AI-assisted text-mining evidence is not reproducible from a rerunnable specification and has no recall/precision benchmark.
**(a) Quoted passage:**  
§7 AI Disclosure: “AI tooling was used for scripting, data management, and literature search — including the text-mining counts reported in §§3.21–3.24 and the text-proximity hits behind the four PROVISIONAL_MEDIUM promotions (§2.2). Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect:**  
Several literature-overlap and text-proximity claims depend on an unbenchmarked AI/text-mining pipeline whose prompts, versions, and settings were not archived. These claims are not rerunnable from a specification and cannot be trusted as exhaustive or precise literature evidence.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Archive model/tool versions, prompts, OCR inputs, search terms, extraction rules, and validation samples; benchmark recall and precision against a hand-coded gold standard.

**Kind:** (ii) limitation the paper itself already discloses at the same strength.

---

## (2) Strongest overall hostile referee case

The paper is unusually candid about its weaknesses, but that candor leaves the headline claims in a very weak evidentiary position. The central “decipherment” product is a table of 161 candidate Proto-Dravidian readings, yet the paper admits that confidence labels are not calibrated, the DEDR search space and rejected alternatives were not recorded, no multiple-comparison control exists, and even the HIGH category cannot be verified sign-by-sign against the stated criteria. A major route to MEDIUM status uses an SA model that scored 0.000 on held-out anchors and could not be distinguished from Sanskrit or scrambled controls. The reading set also has unresolved vowel-harmony problems and a 23.4% phonotactic violation rate concentrated in high-frequency headline signs.

The structural part is stronger but still far short of decipherment. The positional z-score supports non-random ordering, but the semantic labels “classifier/title/name” are interpretations, not outputs of the test; rival templates such as owner marks, commodity marks, clan emblems, and non-linguistic administrative systems were not tested. Whole-inscription full matches are only 5.1%, with 38.4% partial. The paper itself states that its tests do not separate linguistic writing from non-linguistic marking systems, and that no formal comparison has established Proto-Dravidian superiority over Proto-Munda, early Indo-Aryan, or language-neutral baselines.

External validation is essentially absent. Fish-sign isolation is a corpus-wide artifact because the corpus has no single-sign inscriptions. Gulf catalog searches give no confirmation. Meluhhan name tests produce no discriminative matches. The validation path offers no currently executable decisive test: one requires a future bilingual, one already failed to confirm, and one lacks a discriminating prediction.

Finally, most corpus-level results cannot be independently rerun because the underlying corpus is private. The repository may contain scripts and tables, but the paper’s central counts and tests depend on data unavailable to reviewers. The strongest defensible conclusion is therefore not “a candidate decipherment with 90.96% coverage,” but: this private-corpus analysis finds non-random positional structure and proposes an internally organized, heavily caveated Proto-Dravidian reading table whose accuracy, language-family specificity, and semantic interpretation remain unvalidated.

## (3) POSITIVES checked and still standing

1. **The z-score arithmetic is internally correct from the printed numbers.**  
   **Passage checked:** §2.3: “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **Check:** The arithmetic is correct.

2. **The token-coverage arithmetic in §3.1 is internally consistent.**  
   **Passage checked:** §3.1: “HIGH … 70.34% (4,925 tokens)”; “MEDIUM … 20.62% (1,444 tokens)”; “LOW … 9.04% (633 tokens)”; “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”  
   **Check:** 4,925 + 1,444 + 633 = 7,002; 6,369 / 7,002 ≈ 90.96%.

3. **The provisional-sign coverage arithmetic is internally consistent.**  
   **Passage checked:** §3.1: “The four PROVISIONAL_MEDIUM signs (§2.2) account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”  
   **Check:** 6,369 − 15 = 6,354; 6,354 / 7,002 ≈ 90.75%.

4. **The M267 motif counts printed in §3.4 sum correctly to 400.**  
   **Passage checked:** §3.4: “unicorn 147 tokens, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20, script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens in total.”  
   **Check:** These counts sum to 400.

5. **The fish-bearing site counts in §3.5 sum correctly to 113 and the paper correctly discloses that the result is not fish-specific.**  
   **Passage checked:** §3.5 table gives fish seals by site: 6, 33, 35, 11, 13, 5, 4, 3, 3; §3.5 says “the fish count of 0 is therefore not a fish-specific result.”  
   **Check:** The site counts sum to 113; the limitation is stated clearly.

6. **The paper correctly flags that M176’s 94% terminal rate does not meet its own >95% terminal-marker criterion.**  
   **Passage checked:** §3.3: “M176’s printed terminal figure — 94% of its 356 tokens inscription-final — does not by itself meet §2.2’s terminal-marker criterion (>95%).”  
   **Check:** This is internally sound and avoids overstating the criterion.

7. **The Phase-168 hypothetical coverage arithmetic is internally correct.**  
   **Passage checked:** §3.29: “The coverage figure below is therefore checkable from this page: 6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”  
   **Check:** 6,369 + 97 = 6,466; 6,466 / 7,002 ≈ 92.35%.

8. **The paper repeatedly and explicitly distinguishes assignment coverage from verified decipherment.**  
   **Passage checked:** Abstract: “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
   **Check:** This limitation is clearly and correctly disclosed.

CALL-META pass4: finish_reason=stop; max_completion_tokens=48000; completion_tokens=7129; prompt_tokens=32178; output_chars=26887.
