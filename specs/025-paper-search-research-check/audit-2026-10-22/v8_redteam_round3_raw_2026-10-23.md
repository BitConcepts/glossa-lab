# Glossa Lab Indus Preprint v8 — Red-Team Round 3: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 95,644 chars, SHA-256 of PDF 8d0d676eee187de71ad268c6ff374b9d6d6e8a788582552f366e9dc59365ddd0), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs.



## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

1. **(a) Quoted passage:** “A separate search of the Gulf deposit catalog’s text (Laursen 2010) found no fish-sign mentions at all, so it provides no counterexample to that pattern but also no confirmation of it; the two results count different units and are not combined (§3.19).”  
   **and:** “Counting the 27 Indus-script contexts in Laursen’s catalog, in which likewise no isolated fish sign is reported, gives the combined figure of 0/140 used in the abstract; the two parts count different units (seals and catalog contexts) and should be cited separately.”  
   **(b) Defect:** §3.19 says the abstract uses a combined 0/140 figure. The abstract does not use 0/140 and explicitly says the two results “are not combined.” §4.5 also says “no extended verdict across both corpora is claimed,” and Appendix C says the Gulf search “contributes no denominator.” This is a stale internal contradiction.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Delete the “0/140 used in the abstract” sentence or actually revise the abstract and all later echoes consistently. If the intended policy is non-combination, print only “0/113 Holdat” plus “0 fish-sign mentions in Laursen text” as separate results everywhere.

2. **(a) Quoted passage:** “Validation path §4.5.2 was executed using Laursen (2010) Arabian Archaeology and Epigraphy 21:96-134 and Mitchell (1986) in Bahrain Through the Ages.”  
   **(b) Defect:** There is no subsection “§4.5.2” in the paper. §4.5 is a numbered list, not a subsectioned §4.5.1/§4.5.2 structure. The cross-reference does not land where stated.  
   **(c) Severity:** MINOR.  
   **(d) What would settle it:** Change the reference to “§4.5, item 2” or create an actual §4.5.2 heading.

3. **(a) Quoted passage:** “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”  
   **and:** “SA simulation: The syllabic language model is trained on modern Tamil; phonological drift over 4,000 years may introduce systematic errors.”  
   **(b) Defect:** §2.4 says the training set cannot be reconstructed and no specific corpus is stated. §4.4 then states as fact that the model is “trained on modern Tamil.” These cannot both be true at the stated precision. This is a stale limitation echo.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Either identify the actual modern-Tamil training corpus, inventory, and size, or revise §4.4 to say only that the records describe “Tamil/Dravidian syllable sequences” and that the exact training data are unknown.

4. **(a) Quoted passage:** “Two signs assigned candidate Munda substrate readings (see §4.2; speculative)”  
   **and:** “In both cases the recorded basis is a Dravidian Etymological Dictionary entry (DEDR 1709 and DEDR 5388 respectively), reached through the Phase-128 re-review. A Munda derivation was proposed for each, but no Munda source, sound correspondence, or borrowing pathway is established in our records for either, so neither promotion rests on substrate evidence.”  
   **and:** “Two signs (M374=kul, M351=vī, six tokens each) are assigned candidate Munda substrate readings under the model (see §3.3 for the limits of both).”  
   **(b) Defect:** The summary and discussion still call these “Munda substrate readings,” while the methods/results state that neither promotion rests on substrate evidence and that the basis is DEDR, not Munda. “Speculative” does not cure the categorical inconsistency.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Rename them consistently as “DEDR-backed readings with speculative Munda proposals,” or print the missing Munda sources, sound correspondences, and borrowing pathway that would justify the substrate label.

5. **(a) Quoted passage:** “A targeted audit of sibilant-initial Dravidian readings in the current H+M set finds 7 signs with ca-/ce-/ci-/co- phonemes (M025=cem, M078=cēr, M066=cōḻ, M028=cōḻ, M237=ce, M118=car, M305=ōṭu/comitative).”  
   **and:** “Testing the four phonological slots /su/, /i/, /li/, /shu/ against the pre-Phase-163 157 H+M readings: 2/4 slots are covered (/i/ by 5 candidate signs — M267, M162, M336, M305, M045; /li/ by 4 signs including M162=il/iḷ).”  
   **(b) Defect:** M305 is counted in §3.16 as one of seven signs with ca-/ce-/ci-/co- phonemes, but the printed reading there is “ōṭu/comitative,” which is not ca-/ce-/ci-/co-. In §3.15 the same sign is also counted as covering /i/. The paper does not print a reading for M305 that reconciles these uses. The “7 signs” count is therefore not internally checkable from the printed readings.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print the exact reading(s) assigned to M305 and specify whether “comitative” is a gloss, a category, or a phonological value. Recompute the sibilant-initial count with only signs whose printed readings actually begin ca-/ce-/ci-/co-.

6. **(a) Quoted passage:** “H+M signs with strictly TERMINAL-dominant positional profiles (t_rate >= 0.50): 7 signs. Testing these against the Tamil-Brahmi epigraphy terminal phoneme inventory … 4/7 match (57%). The non-matching signs (M233=ūr, M051=pū/puḷ, M249=tii) are content nouns…”  
   **(b) Defect:** The ratio 4/7 recomputes arithmetically, but the seven-sign denominator is not printed. Only the three non-matches are named. The four matching signs are not listed, so the claim cannot be checked from the paper text.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print a seven-row table giving sign, reading, t_rate, matched Tamil-Brahmi category, and match/non-match decision.

7. **(a) Quoted passage:** “The Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed…”  
   **(b) Defect:** The paper retains an exact percentage while admitting that both numerator and denominator are absent from all records. This is not a recomputable result; it is an orphaned number.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Remove the 87.08% figure or provide the exact numerator, denominator, inclusion rule for “multi-sign inscriptions,” and sign-class mapping used.

8. **(a) Quoted passage:** “The 36 observed site-pair values in this section are descriptive; intervals are printed for one pair only…”  
   **and:** “A bootstrap confidence interval was computed for the most divergent pair: Mohenjo-daro vs Rakhigarhi KL=0.509, 95% CI [0.483, 0.750]. The other Rakhigarhi pairs have observed KL values between 0.250 and 0.481…”  
   **(b) Defect:** The claim that Mohenjo-daro–Rakhigarhi is the “most divergent pair” cannot be checked from the paper, because the 36 site-pair values are not printed. Only eight Rakhigarhi-related values and one large-site pair are given. Any non-Rakhigarhi pair could exceed 0.509, and the printed text does not rule that out.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print the full 9×9 or 36-row KL matrix, including all site pairs, with the same smoothing and H+M-token rule.

9. **(a) Quoted passage:** “From the full corpus (1,670 seals, 7,002 tokens), we extracted 2,647 distinct bigrams — adjacent sign pairs within inscriptions, in reading order — including 1,485 H+M-by-H+M bigrams; the full table is the supplemental file formula_bigram_table.csv. The dominant formula backbone is M342·M176 … appears on 122 seals (7.3% of corpus, PMI=2.43)… 97 distinct formula types are identified…”  
   **(b) Defect:** Only 122/1670 = 7.3% can be recomputed from the printed text. The distinct-bigram count, H+M-by-H+M count, PMI=2.43, and 97 formula-type count cannot be recomputed because the bigram counts, sign-token marginal counts, and INITIAL-sign list are not printed. The paper exports the necessary arithmetic to an unavailable supplemental file.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print at least the marginal counts for M342 and M176, total bigram-token denominator, M342·M176 bigram count, and a summary table giving total distinct bigrams, H+M/H+M bigrams, and the 97 INITIAL signs.

10. **(a) Quoted passage:** “We tested 394 INITIAL-sign × iconography pairs for enrichment… 63 pairs (16%) pass the corrected threshold; an adversarial recheck (Phase-149) estimates about 43 of the 63 are robust…”  
   **(b) Defect:** The five printed chi-square examples recompute, and 63/394 = 16.0% recomputes. But the “63 pairs” and “about 43” robust count cannot be checked from the paper because the full 394-pair table is not printed. The “about 43” count is especially uncheckable because the recheck rule is described only generically.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print the full enrichment table or at least a 63-row pass list with observed, expected, chi-square, and robust/marginal flag.

11. **(a) Quoted passage:** “The exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.”  
   **and:** “A reader who checks out the named commit therefore sees the paper’s text exactly as frozen; the only sentence that differs in that checkout is this one, which there names the previous round’s commit.”  
   **(b) Defect:** The paper claims the named commit identifies the exact text, then admits the checked-out text differs by at least one sentence. That defeats the “exact text” claim as written.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Use an immutable tag/archive whose content exactly matches the submitted text, or revise the data-availability statement to say the commit approximates the text except for the explicitly named self-referential sentence.

12. **(a) Quoted passage:** “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage) are Tier 2 claims supported by multiple tests.”  
   **and:** “The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”  
   **and:** “a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS.”  
   **(b) Defect:** The conclusion’s “Proto-Dravidian readings … supported by multiple tests” overstates the body. The body says the framework is not discriminative against major alternatives and even records an equal Dravidian/Sanskrit fit in one comparison. The conclusion echo is stronger than the results it summarizes.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Revise the conclusion to “Proto-Dravidian-compatible candidate readings under this model” and explicitly state that discriminative superiority over Proto-Munda, early Indo-Aryan, Sanskrit-profile baselines, or language-neutral models has not been established.

13. **(a) Quoted passage:** “The corpus shows structure consistent with a decipherable linguistic system; the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”  
   **and:** “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”  
   **and:** “these measures do not separate the one certain writing system from systems that are not writing, so a close Indus fit on them is evidence neither for nor against the script being language.”  
   **(b) Defect:** The conclusion bundles “decipherable linguistic system” and “favours Proto-Dravidian” more strongly than the body permits. The body explicitly withdraws frequency-curve evidence for linguistic status and says the positional pattern was not tested against rival non-linguistic or alternative-functional templates.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Restrict the conclusion to “non-random positional structure” and “compatibility with the proposed Proto-Dravidian framework,” unless rival-template and rival-language tests are actually performed and printed.

14. **(a) Quoted passage:** “No site-by-site coverage table for the 161-sign set exists: it was never computed, in this paper or in the program’s records.”  
   **and:** “H+M-candidate seal coverage = 69.8% (was 69.1%).”  
   **(b) Defect:** The paper gives a global 161-set seal-coverage percentage but admits no site-by-site 161-set coverage table exists. That is not itself an arithmetic error, but it leaves the 69.8% coverage distribution uncheckable by site while the paper repeatedly emphasizes nine-site corpus coverage. The only site percentages printed belong to the obsolete 157-sign set.  
   **(c) Severity:** MINOR.  
   **(d) What would settle it:** Print the 161-set fully covered / total seals by site, or state explicitly that all site-distribution claims are limited to the obsolete 157-sign set and cannot be inferred for the headline 161-set.

15. **(a) Quoted passage:** “End of Preprint v8 / Glossa-Lab, May 2026”  
   **and:** “Date: May 2026 (revised October 2026)”  
   **and:** “on the October 2026 execution tree the changed suite reported 40 passed, 0 failed, 8 warnings”  
   **(b) Defect:** The terminal date line says “May 2026” although the paper repeatedly identifies itself as revised in October 2026 and includes October 2026 results. This is a stale end-matter echo.  
   **(c) Severity:** MINOR.  
   **(d) What would settle it:** Change the final date line to “May 2026; revised October 2026” or remove the stale date.

16. **(a) Quoted passage:** “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository…”  
   **and:** “The anchor table — all 161 HIGH/MEDIUM rows… Neither table is printed in this paper…”  
   **and:** “The corpus itself is not publicly released… so corpus-level counts cannot yet be re-run by other researchers.”  
   **(b) Defect:** Many headline corpus-level quantities depend on tables and a corpus not printed in the paper and, for the corpus, not publicly available. Percentages such as 6,369/7,002 can be checked arithmetically once the numerator is accepted, but the numerator itself cannot be audited from the paper text. This is a remaining internal-audit limitation, not cured by repository pointers when the instruction is to audit the printed text only.  
   **(c) Severity:** MAJOR.  
   **(d) What would settle it:** Print the complete 397-sign status/frequency table or at minimum a per-confidence token-frequency table sufficient to reproduce 6,369 H+M tokens, 633 LOW tokens, 15 provisional tokens, and 1,165 fully covered seals from the paper alone.

## POSITIVES

1. **Quoted passage:** “Mohenjo-daro (n=606), Harappa (n=492), Kalibangan (n=110), Dholavira (n=106), Lothal (n=124), Chanhu-daro (n=78), Surkotada (n=61), Banawali (n=60), Rakhigarhi (n=33).”  
   **Confirmable positive:** The site counts sum correctly: 606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670.

2. **Quoted passage:** “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%). The remaining 633 tokens (9.04%)…”  
   **Confirmable positive:** 75 + 86 = 161; 6,369 + 633 = 7,002; 6,369/7,002 = 90.9597%, rounding to 90.96%; 633/7,002 = 9.0403%, rounding to 9.04%.

3. **Quoted passage:** “The four PROVISIONAL_MEDIUM signs (§2.2) account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”  
   **Confirmable positive:** 161 − 4 = 157; 6,369 − 15 = 6,354; 6,354/7,002 = 90.7455%, rounding to 90.75%.

4. **Quoted passage:** “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **Confirmable positive:** The printed z-score recomputes: 0.9916 − 0.4385 = 0.5531; 0.5531/0.05347 ≈ 10.344.

5. **Quoted passage:** “the standard add-one estimate is (0+1)/(2,000+1) = 0.0005”  
   **Confirmable positive:** 1/2,001 = 0.00049975, correctly rounded to 0.0005.

6. **Quoted passage:** “Total seals 1,670; Fully covered by H+M candidate readings 1,165 (69.8%); Blocked by LOW-confidence signs 505 (30.2%).”  
   **Confirmable positive:** 1,165 + 505 = 1,670; 1,165/1,670 = 69.76%, rounding to 69.8%; 505/1,670 = 30.24%, rounding to 30.2%.

7. **Quoted passage:** “Lothal 6… Harappa 33… Mohenjo-daro 35… Dholavira 11… Kalibangan 13… Chanhu-daro 5… Banawali 4… Rakhigarhi 3… Surkotada 3… Total 113.”  
   **Confirmable positive:** The fish-bearing site counts sum correctly: 6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113.

8. **Quoted passage:** “Grouping the 97 INITIAL-sign clusters… UNRESOLVED 51… ANIMAL_GUILD 25… MATERIAL 6… DEITY_TITLE 9… CIVIC_ROLE 6.”  
   **Confirmable positive:** Cluster counts sum correctly: 51 + 25 + 6 + 9 + 6 = 97. The seal counts also sum correctly: 845 + 446 + 145 + 135 + 99 = 1,670.

9. **Quoted passage:** “The 19 signs… M270 (6 tokens) and M386 (6); and, at 5 tokens each, [17 signs] — 97 tokens in total. … 6,369 + 97 = 6,466 tokens, and 6,466 / 7,002 = 92.35%.”  
   **Confirmable positive:** The blocker arithmetic checks: 2×6 + 17×5 = 97; 6,369 + 97 = 6,466; 6,466/7,002 = 92.346%, rounding to 92.35%.

10. **Quoted passage:** “Results: 137/147 signs (93.2%)…”  
    **Confirmable positive:** 137/147 = 93.197%, rounding to 93.2%.

---CALL-META finish_reason=stop usage={"prompt_tokens": 25140, "completion_tokens": 10512, "total_tokens": 35652, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 5632, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=17765---


## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

1. **(a) Quoted passage:** “a recurring three-slot inscription formula consistent with a Proto-Dravidian administrative vocabulary framework”  
   **(b) Defect:** The claim overstates the evidence. The body only establishes positional structure; it explicitly says the semantic labels are interpretive and rival functions were not tested: “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics” and “it was not tested against rival templates such as owner marks, commodity marks, or clan emblems.” Calling the formula “consistent with a Proto-Dravidian administrative vocabulary framework” imports linguistic and administrative content that the positional test itself does not supply.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** A rival-model comparison showing that the three-slot pattern fits the Proto-Dravidian administrative interpretation better than owner-mark, commodity, clan, cultic, or language-neutral templates, with printed criteria and results.

2. **(a) Quoted passage:** “These readings are assigned to signs that together account for 90.96% of the corpus’s sign tokens (69.8% of seals consist entirely of such signs).”  
   **(b) Defect:** The headline coverage is presented as a support claim for “readings,” but the paper later admits that “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified,” that the corpus is unavailable, that HIGH/MEDIUM labels have “no measured error rate,” that DEDR search had no multiple-comparison control, that SA agreement was 0.000, and that the reading set has unresolved V12 and 23.4% V07 phonotactic violations. The numerical coverage therefore supports assignment breadth, not reading validity.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** Separate headline language distinguishing “assignment coverage” from “validated reading coverage,” plus an externally checkable table showing, for each covered token/sign, which non-circular evidence supports the reading and what error rate is expected.

3. **(a) Quoted passage:** “the evidence is consistent with a Proto-Dravidian reading framework under the tested assumptions, though Dravidian superiority over proto-Munda has not been formally quantified.”  
   **(b) Defect:** This still overstates the body’s evidence. The limitations section says “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary,” and also reports mixed existing comparisons: “a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS.” “Consistent with Proto-Dravidian” is not wrong as a weak compatibility claim, but in the abstract it functions as evidential support while the body admits non-discrimination against major alternatives.  
   **(c) Severity:** CRITICAL  
   **(d) What would settle it:** A formal discriminative comparison against Proto-Munda, early Indo-Aryan/Sanskrit, and language-neutral baselines, with preregistered metrics and printed results showing Proto-Dravidian superiority.

4. **(a) Quoted passage:** “This study does not claim epigraphic finality; it proposes a falsifiable computational model whose method and repository artefacts (scripts, phase reports, and the anchor table) can be re-run and checked”  
   **(b) Defect:** The claim is stronger than the access conditions allow. The same abstract says “The corpus itself is not publicly released” and “corpus-level counts cannot yet be re-run by other researchers.” Many central claims are corpus-level: z-score, coverage, fish-sign count, positional profiles, site divergence, bigrams, iconographic enrichments. Repository artefacts without the corpus do not permit full re-running or checking of the paper’s central evidence.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** Public release of the corpus used, or a complete reproducibility package with derived count tables sufficient to regenerate every printed corpus-level result independently.

5. **(a) Quoted passage:** “A three-slot grammar model empirically derived from positional statistics”  
   **(b) Defect:** This headline omits the later weakening that the empirical evidence is positional only, not semantic or functional. Section 3.2 says: “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics.” The phrase “grammar model” is tolerable for positions, but in context it is repeatedly tied to classifier/title/name/case meanings that were not empirically derived.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** A strict separation throughout between “three positional classes” and “classifier/title/name/case grammar,” or a test showing that the semantic slot labels are empirically supported.

6. **(a) Quoted passage:** “HIGH (75 signs): Two or more of the following evidence criteria are met.”  
   **(b) Defect:** The paper later labels signs HIGH while printing only one qualifying basis or a basis that does not meet the stated threshold. Example: “M261 muruku … Wheel/spindle (2 tokens; the reading is muruku, ‘young man’ — the further gloss ‘Tamil Murugan’ is withdrawn…)” and the prefatory note says “M261 on a published source (Parpola 1994, via Phase-51).” A two-token Parpola-derived reading is not one of the printed HIGH criteria in §2.2, and no second qualifying criterion is printed.  
   **(c) Severity:** CRITICAL  
   **(d) What would settle it:** A printed sign-by-sign HIGH audit table listing, for every HIGH sign, the two or more exact criteria met, with corpus counts and source citations.

7. **(a) Quoted passage:** “M176 an/aṇ … Candidate masculine suffix: 356 tokens, 94% of them inscription-final; the gender label is likewise an interpretation of distribution”  
   **(b) Defect:** This is labelled under “HIGH confidence,” but the stated terminal-marker criterion in §2.2 is “sign appears in >95% of cases as inscription-final.” The printed evidence says 94%, below the paper’s own threshold, and the masculine/gender interpretation is explicitly only interpretive.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** Either demote M176 or print the additional independent criterion/criteria that justify HIGH despite failing the stated >95% terminal criterion.

8. **(a) Quoted passage:** “M342 ay/ā … Candidate case suffix: 584 tokens, 96% of them inscription-final; the case-suffix label is an interpretation of that distribution, not a demonstrated paradigm”  
   **(b) Defect:** The HIGH label is not adequately supported by the printed criteria. The passage supplies terminal position and an interpretive case-suffix label, but §2.2 requires two or more criteria for HIGH. The table gives no DEDR entry and no demonstrated paradigm; it prints only distribution plus interpretation.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** A second qualifying criterion for M342, or reclassification as a positional candidate rather than HIGH-confidence reading.

9. **(a) Quoted passage:** “Statistical analysis of inscription structure identifies a consistent three-slot pattern”  
   **(b) Defect:** “Consistent” overstates what the body later reports. Section 3.31 says Phase-133 whole-inscription matching was “full match 5.1% of seals and partial match 38.4%, together 43.5%.” A pattern with full matches on only 5.1% of seals should not be called a consistent inscription formula without immediately qualifying what “consistent” means.  
   **(c) Severity:** MAJOR  
   **(d) What would settle it:** A printed definition of “consistent” tied to the actual match rates, or revised language restricting the claim to sign-level positional regularity rather than inscription-level formula consistency.

10. **(a) Quoted passage:** “For the enriched subset of pairs — above all the largest associations — this shows that the inscription’s INITIAL sign and the carved animal on the same seal are co-selected, not independent decorations.”  
    **(b) Defect:** The claim is stronger than the test as printed. The paper says the statistic printed is “not a full 2 × 2 chi-square for the pair,” expected counts are “as low as 1.0,” and Phase-149 estimates “about 43 of the 63 are robust, the rest marginal.” The broad “co-selected, not independent decorations” wording risks applying to the subset as a whole, even though roughly 20 of 63 are admitted marginal/expected false positives.  
    **(c) Severity:** MINOR  
    **(d) What would settle it:** Restrict the claim explicitly to the individually robust pairs and print the full 2×2 tests or exact tests for the claimed co-selection cases.

11. **(a) Quoted passage:** “the opening-sign pattern is the one point of agreement.”  
    **(b) Defect:** The paper itself says the CISI percentage behind this alleged agreement cannot be checked: “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere.” An uncountable carried-over percentage cannot serve as a “point of agreement,” especially when the same paragraph says structural agreement is LOW.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Print the CISI denominator, numerator, sign crosswalk, and opening-sign classification table, or withdraw the “point of agreement” claim.

12. **(a) Quoted passage:** “All domains share the same terminal sign profile (M342/M176 dominant), consistent with a common grammar skeleton across semantic registers.”  
    **(b) Defect:** The statement overreaches. The domains are assigned from the model’s own readings, and the paper admits “No test in this paper shows that they functioned as registers.” Therefore “semantic registers” and “common grammar skeleton across semantic registers” are not supported as evidence; at most this is an internal description of model-assigned clusters.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** A test independent of the proposed readings showing that the clusters are real semantic/register classes and share terminal profiles beyond what the model construction imposes.

13. **(a) Quoted passage:** “Rakhigarhi (n=33) is distinctively divergent from every other major site”  
    **(b) Defect:** The claim exceeds the evidence immediately provided. The paper says a confidence interval was computed “for the most divergent pair only,” that “no confidence intervals for those pairs are on record,” and that “Rakhigarhi has only 33 seals” so its distinctiveness should not be read as proof against small-sample effects. “Distinctively divergent from every other major site” is therefore too strong.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Confidence intervals or permutation/bootstrap tests for every Rakhigarhi pair, with correction for multiple comparisons and explicit small-sample sensitivity analysis.

14. **(a) Quoted passage:** “On this program’s text mining of Wells, his position is compatible with a proto-Dravidian reading and with consistent sign positional classes; we cite this as our mining summary of his book, not as a quotation.”  
    **(b) Defect:** “Compatible with a proto-Dravidian reading” is an inflated inference from unvalidated text mining. The paper provides no quoted Wells passage, no coding rules, no validation of mining recall/precision, and no sign-by-sign comparison. It converts machine-mined references into a substantive compatibility claim.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Direct quotations or a hand-audited coding table showing exactly which Wells claims support which Proto-Dravidian or positional-class assertions.

15. **(a) Quoted passage:** “the grammar paper contains 79 positional-class references and 61 grammar structure agreement hits with our 3-slot model (classifier/title/suffix terminology).”  
    **(b) Defect:** “Agreement hits” overstates what is shown. The paper later explains that Phase-158 counted “every passage matching the model’s slot terminology,” not demonstrated agreement with this model. Shared terminology in one scholar’s papers is not evidence that the paper’s three-slot model is validated.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Replace “agreement hits” with “terminology overlaps,” or print a hand-coded table showing actual propositions in Mahadevan that match the model’s specific slot definitions.

16. **(a) Quoted passage:** “The akam-puram (2011) paper identifies a crescent-moon sign as an ‘outer city’ marker at INITIAL position, consistent with our INITIAL = title/determinative class. Place Signs (1981) documents 10 settlement/ūr sign references, consistent with M233=ūr.”  
    **(b) Defect:** These are asserted as consistency evidence without the necessary bridge. A crescent-moon “outer city” marker is not shown to equal a title/determinative class, and “settlement/ūr sign references” are not shown to support this paper’s specific M233=ūr assignment. The claim is based on mined compatibility, not printed sign-level agreement.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Print the exact Mahadevan passages, signs, sign numbers, and mappings demonstrating that the same sign and same reading/function are being compared.

17. **(a) Quoted passage:** “It is consistent with that view, at the strength a single unbenchmarked search can support.”  
    **(b) Defect:** This still gives evidential weight to the literature-extraction null despite admitting “its recall has never been measured” and that the null is “for this search method only.” An unbenchmarked OCR/text-mining failure to find LOW-sign proposals cannot meaningfully support the view that the H+M set is near the frontier of published scholarship.  
    **(c) Severity:** MINOR  
    **(d) What would settle it:** Benchmark the pipeline against a hand-checked set of known published sign proposals and report recall/precision before using the null as support for any literature-frontier claim.

18. **(a) Quoted passage:** “Progress from this point requires either the ICIT corpus (5,318 inscriptions vs 1,670) or a new archaeological find.”  
    **(b) Defect:** This overstates the exhaustion of current evidence. Section 3.30 itself says “other approaches — rival-model comparison, expert coding, image inspection — remain open on the same material.” Therefore progress does not “require” ICIT or a new find.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Revise to “the authors’ current text-mining and positional pipeline did not advance further; ICIT or new finds are one route,” or demonstrate that rival-model comparison, expert coding, and image inspection cannot improve the result.

19. **(a) Quoted passage:** “Formal cross-validation of the four Phase-163 provisional MEDIUM sibilant upgrades against DEDR phonological entries, positional profiles, and Proto-Dravidian phonotactic constraints.”  
    **(b) Defect:** “Cross-validation” is misused and overstates the evidential strength. The same section says the upgrades are based on text proximity where “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment,” and that all four remain provisional pending expert review. Checking DEDR availability and phonotactic permissibility is within-model plausibility, not validation.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Rename this as a “within-model plausibility check,” or provide independent expert-coded confirmation that the cited literature assigns the readings to the same signs.

20. **(a) Quoted passage:** “The overall verdict is PROVISIONAL_SUPPORTED_WITHIN_MODEL”  
    **(b) Defect:** Even with “within-model,” the capitalized verdict contains “SUPPORTED” for readings whose evidence is explicitly provisional, OCR-proximity-based, and not verified as direct sign assignments. The label is stronger than the evidence and likely to be read as support for the readings rather than support for continued provisional status.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Replace the verdict with “PROVISIONAL_PLAUSIBLE_UNVERIFIED” unless direct sign-assignment evidence is printed.

21. **(a) Quoted passage:** “adversarial challenge battery (S10): of 10 challenges, 4 survived outright and 6 survived with caveats, none failed outright (Phase-149)”  
    **(b) Defect:** The “survived” verdict is uncheckable from the paper text. The challenges, criteria, outcomes, and caveats are not printed. A capitalized scorecard item is being used as evidence in the master synthesis without enough information for the reader to audit whether “survived” is warranted.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Print the 10 challenges, pass/fail criteria, observed results, and caveats, or remove this item from evidence synthesis.

22. **(a) Quoted passage:** “These are most likely syllabic components of personal names — in a system where personal name syllables could be arbitrary, they would not be recoverable from distributional statistics alone. This is the fundamental ceiling of the current methodology.”  
    **(b) Defect:** “Most likely” and “fundamental ceiling” overstate the evidence. Section 3.9 says the same pattern is also “what any medial-only sign class would look like” and that “the statistics alone do not distinguish the two.” Therefore the personal-name interpretation is not the most likely result shown by the statistics; it is a model preference.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Evidence distinguishing personal-name syllables from other medial-only sign classes, such as repeated name-sequence patterns, external name matches, or a bilingual/control comparison.

23. **(a) Quoted passage:** “High-frequency signs are well-constrained; low-frequency signs (the irresolvable 18) are not.”  
    **(b) Defect:** This limitation understates problems in high-frequency signs. The paper reports that headline high-frequency signs drive phonotactic violations: “M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.” It also reports a prior high-frequency misassignment: “M267 (corpus frequency=400) as ‘mīn/fish’ … was incorrect.” High frequency has not made these signs “well-constrained” in the sense implied.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Replace with a narrower statement such as “high-frequency signs have more positional data,” and provide sign-level constraint diagnostics showing which high-frequency readings are actually stable.

24. **(a) Quoted passage:** “Conservative confidence standards: Our MEDIUM threshold is deliberately strict.”  
    **(b) Defect:** The claim is not supported by the paper’s own admissions. MEDIUM includes signs promoted by SA+DEDR despite SA held-out agreement of 0.000 and unknown false-positive rate; it also includes PROVISIONAL_MEDIUM signs based on OCR text proximity, where hits are “not a verified assignment.” Calling this “deliberately strict” is unsupported.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Provide calibration showing the MEDIUM threshold has an acceptably low false-positive rate, or remove “strict” and state that MEDIUM is an uncalibrated rule-based category.

25. **(a) Quoted passage:** “The candidate model is falsifiable at the first of the following points today.”  
    **(b) Defect:** The first point is “Discovery of a bilingual text,” which is not a test available “today”; the second is already completed and did not confirm; the third says “No such discriminating prediction is yet on record.” The section therefore does not identify a current, executable falsification test for the model’s main readings.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** State a presently executable falsification test using available data, with a clear prediction whose failure would reject the model, or drop “today.”

26. **(a) Quoted passage:** “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage) are Tier 2 claims supported by multiple tests.”  
    **(b) Defect:** “Supported by multiple tests” overstates the evidence for the readings. The same paragraph admits the tests “are not independent,” the labels have “no measured error rate,” and the set has unresolved V12 plus 23.4% V07 phonotactic violations. Earlier sections also admit DEDR multiple-comparison risk and SA failure. Multiple non-independent, uncalibrated, partly failed checks do not support the readings at the strength implied.  
    **(c) Severity:** CRITICAL  
    **(d) What would settle it:** A sign-level evidence matrix separating independent from non-independent tests, calibrated error rates, correction for DEDR search multiplicity, and external expert review of the readings.

27. **(a) Quoted passage:** “The corpus shows structure consistent with a decipherable linguistic system; the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”  
    **(b) Defect:** This conclusion overreaches. The frequency-curve test is declared UNINFORMATIVE; Nair “does not settle the linguistic question”; rival language-family baselines remain necessary; Dravidian vs Sanskrit was AMBIGUOUS in one internal comparison; and Proto-Munda superiority was not formally quantified. The paper supports non-random positional structure, not a conclusion that the evidence “favours” Proto-Dravidian over alternatives.  
    **(c) Severity:** CRITICAL  
    **(d) What would settle it:** Formal discriminative testing against non-linguistic, Proto-Munda, early Indo-Aryan/Sanskrit, and language-neutral models, with results showing Proto-Dravidian is preferred.

28. **(a) Quoted passage:** “Grammar model: [CLASSIFIER]–[TITLE]–[SUFFIX] pattern supported”  
    **(b) Defect:** Appendix C presents an internal-suite item as “supported,” but the body says the semantic labels are interpretations, the grammar retest is self-consistency rather than accuracy, and rival templates were not tested. The capitalized internal validation summary therefore overstates what has actually been supported.  
    **(c) Severity:** MAJOR  
    **(d) What would settle it:** Change the item to “positional pattern internally consistent,” or provide external/rival-model evidence supporting classifier-title-suffix semantics.

29. **(a) Quoted passage:** “At Phase-170 (May 2026), the program’s internal consistency suite (foundation_check.py) reported 59 checks, all passing.”  
    **(b) Defect:** This is immediately weakened by “on the October 2026 execution tree it reported 40 passed, 0 failed, 8 warnings,” but the paper still repeats the stronger 59/59 pass result in the abstract and Appendix C. The stale stronger summary remains prominent even though the current execution tree has warnings and a changed suite.  
    **(c) Severity:** MINOR  
    **(d) What would settle it:** Lead with the current October suite result only, and relegate the May 59/59 result to historical provenance without implying current validation.

30. **(a) Quoted passage:** “The full per-item list, with each item’s label, is in the Phase-169 record … it is not printed in this paper, and no single tally at the top labels is printed, because any such tally would mix the two kinds.”  
    **(b) Defect:** The paragraph nevertheless prints the same tally twice: “Results: 32 total evidence items … 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT” and later “Category breakdown: 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT.” The paper says no such tally should be printed because it mixes internal and external checks, then prints it anyway.  
    **(c) Severity:** MINOR  
    **(d) What would settle it:** Remove the category tally from the paper or split it into internal-consistency versus external-evidence counts.

---

## POSITIVES

1. **Quoted passage:** “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.”  
   **Positive:** This is a clear and necessary limitation on the headline 90.96% coverage claim.

2. **Quoted passage:** “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
   **Positive:** The paper explicitly discloses the central reproducibility limitation.

3. **Quoted passage:** “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
   **Positive:** The paper correctly states that its confidence labels are not probabilistic validation.

4. **Quoted passage:** “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”  
   **Positive:** The paper forthrightly reports a severe negative result for the SA machinery.

5. **Quoted passage:** “The domains are assigned from the proposed readings themselves, so the domain shares describe how this model’s own readings are distributed; they cannot be evidence for the readings.”  
   **Positive:** This correctly blocks a circular semantic-clustering argument.

6. **Quoted passage:** “The Gulf material provides no counterexample to the compound-only pattern, but it does not independently confirm it.”  
   **Positive:** The paper properly limits the Gulf fish-sign text-search result.

7. **Quoted passage:** “The Phase-152 record labels this outcome PARTIALLY_SUPPORTED; we do not use that label, because every seal-level result of the test is zero and a label containing ‘supported’ invites misreading even with a qualifier.”  
   **Positive:** This is an honest correction of an overstrong internal verdict label.

8. **Quoted passage:** “The candidate model is falsifiable at the first of the following points today. The other two state, in plain terms, what the completed Gulf work did and did not show, and what a stratigraphic test would have to predict before it could separate rival interpretations.”  
   **Positive:** Although the “today” wording is defective, the section does explicitly acknowledge that the Gulf and stratigraphic paths do not currently validate the model.

---CALL-META finish_reason=stop usage={"prompt_tokens": 25156, "completion_tokens": 8197, "total_tokens": 33353, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 2295, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=26540---


## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

1. (a) “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 2d26b929).”  
   (b) The paper never gives a repository URL, host, access protocol, license, or archive identifier for the “Glossa-Lab repository.” A branch name and commit hash are useless without a repository locator. The claimed reproducibility path is therefore not operational from the printed paper.  
   (c) CRITICAL  
   (d) Provide a public repository URL or archived release DOI containing the exact branch/commit, plus access/licensing instructions and checksums for the files named in §6.

2. (a) “The corpus itself is not publicly released (see §6), so corpuslevel counts cannot yet be re-run by other researchers.” / “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
   (b) The central corpus-level results—token coverage, positional statistics, fish-sign counts, motif counts, bigrams, KL divergences, bootstraps, permutation tests—depend on a non-public corpus. The paper admits these cannot be independently re-run, but still presents them as numerical results. This is a fundamental reproducibility failure for the main analyses.  
   (c) CRITICAL  
   (d) Release the corpus, provide an executable public surrogate with exact crosswalk and expected outputs, or explicitly label every Holdat-dependent number as non-reproducible from the paper.

3. (a) “The DOI identifies this preprint and its version record on Zenodo; the exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.”  
   (b) The paper splits version identity between a Zenodo DOI and an inaccessible/unspecified repository commit. Since the repository is not locatable from the paper, the “exact text” cannot be independently verified. The DOI is explicitly demoted as insufficient, but the replacement identifier is unusable.  
   (c) MAJOR  
   (d) Archive the exact source, data supplements, and PDF for this version under the Zenodo DOI, or give a functioning repository URL and immutable release archive.

4. (a) “HIGH (75 signs): Two or more of the following evidence criteria are met.” / “M261 on a published source (Parpola 1994, via Phase-51).”  
   (b) The printed HIGH criteria do not include “published source” as a qualifying criterion, yet §3.3 says M261 is HIGH based on a published source. The confidence-category rule is therefore internally inconsistent and cannot be applied identically by an independent researcher.  
   (c) MAJOR  
   (d) Print the full rule for HIGH assignment, including whether “published source” is a criterion, and provide for every HIGH sign the exact two or more criteria satisfied.

5. (a) “Iconographic match: the sign’s shape is identified, following the published iconography of Mahadevan and Parpola, as depicting a known object whose Dravidian name yields the reading by the rebus principle”  
   (b) “Identified” is not operational. The paper gives no coding protocol for sign-shape identification, no list of allowable iconographic labels, no adjudication rule for ambiguous signs, no coder blinding, and no inter-coder reliability. A researcher cannot reproduce which signs count as “elephant,” “bow,” “female figure,” etc.  
   (c) MAJOR  
   (d) Provide an iconographic codebook, sign-by-sign assignments, source page/figure references, ambiguity rules, and ideally independent coding/reliability statistics.

6. (a) “Distributional exclusivity: sign appears on one and only one motif type with lift ratio > 5.0”  
   (b) “Motif type” and “lift ratio” are not operationally defined. The paper never prints the full motif taxonomy, motif denominators, the lift formula, the minimum expected-count rule, or how multi-motif/unclear seals were handled.  
   (c) MAJOR  
   (d) Define motif categories, print motif counts, define lift mathematically, state exclusions, and provide the sign × motif contingency table used for all exclusivity claims.

7. (a) “Terminal marker evidence: sign appears in >95% of cases as inscription-final, matching known Dravidian case suffix”  
   (b) This criterion is underdefined. “Cases” could mean sign tokens, inscriptions, seals, or occurrences after excluding SOLO signs. “Matching known Dravidian case suffix” has no listed inventory, source, or phonological matching rule.  
   (c) MAJOR  
   (d) Define the denominator for terminal percentage, treatment of SOLO signs, the exact suffix inventory, source citations, and the matching rule.

8. (a) “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”  
   (b) The paper admits the DEDR matching method is irreproducible and statistically uncontrolled. Since DEDR rebus matching is a core route to MEDIUM and HIGH readings, the anchor model cannot be independently audited for search-space inflation or cherry-picking.  
   (c) CRITICAL  
   (d) Provide the full candidate-generation algorithm, allowed transformations, all accepted/rejected candidates per sign, dictionary search space, and a multiple-comparison/null procedure.

9. (a) “SA: a syllabic language model fitted by simulated annealing” / “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data”  
   (b) The SA method is unreconstructable. Missing are the training corpus, preprocessing, syllable inventory, model architecture/order, objective function, annealing schedule, random seed, number of restarts, convergence rule, and implementation version.  
   (c) CRITICAL  
   (d) Publish the training data or exact citation, syllabification procedure, model specification, annealing parameters, seeds, code, and expected outputs.

10. (a) “Signs with SA consistency >= 0.15 and a DEDR entry matching the modal reading were promoted to MEDIUM.”  
   (b) “Consistency score” is vaguely defined as “fraction of contexts agreeing on the reading,” but the paper does not define “context,” how contexts are weighted, how ties are handled, or what counts as “agreeing.” The 0.15 threshold is admitted to be uncalibrated.  
   (c) MAJOR  
   (d) Define context extraction, scoring, tie handling, threshold rationale, and calibration/null performance on a known script.

11. (a) “For each sign, we compute: - Positional profile: fraction of tokens in INITIAL / MEDIAL / TERMINAL / SOLO positions”  
   (b) The positional classes are not fully operational. The paper does not define how one-sign inscriptions are treated relative to INITIAL/TERMINAL, how two-sign inscriptions are classified, whether repeated signs in one inscription count independently, or how damaged/uncertain inscriptions are handled.  
   (c) MAJOR  
   (d) Provide formal position rules for inscription lengths 1, 2, 3+, repeated signs, uncertain signs, and excluded inscriptions.

12. (a) “The headline positional statistic (z = 10.3) comes from the Phase-134 F1 test. We fit the three-slot grammar model to the real corpus (coefficient of determination R² = 0.9916)…”  
   (b) The actual fitted model and response variable are not defined. “F1 test,” “three-slot grammar model,” and R² are invoked without specifying what is being regressed or predicted, what observations enter the fit, or how R² is computed.  
   (c) CRITICAL  
   (d) Print the exact model equation/procedure, data matrix, dependent variable, fitted parameters, F1 definition, and R² computation.

13. (a) “2,000 copies of the corpus in which the signs inside each inscription were shuffled”  
   (b) The permutation procedure lacks required reproducibility details: random seed, RNG/software, whether shuffling preserves duplicate signs, whether SOLO inscriptions are excluded, and whether signs are shuffled within all inscriptions or only multi-sign inscriptions.  
   (c) MAJOR  
   (d) State the exact permutation algorithm, seed(s), software/version, inclusion rules, and provide the permutation statistic vector.

14. (a) “The same Phase-134 suite also ran a held-out check (F7): positional classes fitted on 1,176 seals predicted the classes of signs on 494 held-out seals with 97.7% agreement”  
   (b) The train/test split is not reproducible. The paper gives no split rule, random seed, stratification by site/motif/length, leakage controls, or denominator for the 97.7% agreement.  
   (c) MAJOR  
   (d) Print the split-selection rule, seed, seal IDs or hashes, denominator/count correct, and leakage-prevention procedure.

15. (a) “HIGH 70.34%; MEDIUM (excluding provisional) 20.41%; PROVISIONAL_MEDIUM 0.21%; MEDIUM (including provisional) 20.62%; LOW 9.04%”  
   (b) The category percentages are not accompanied by exact token counts. Some do not recompute cleanly from the printed denominator 7,002 because only rounded percentages are printed. The table is therefore not auditable from the paper.  
   (c) MINOR  
   (d) Add exact token counts for HIGH, MEDIUM excluding provisional, PROVISIONAL_MEDIUM, MEDIUM including provisional, and LOW.

16. (a) “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).” / “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR… If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain.”  
   (b) The paper admits it cannot compute a true SA-free headline because “the audit file does not record whether any of the 43 also meets a non-SA MEDIUM criterion.” This means the evidence provenance table is insufficient for a key sensitivity analysis.  
   (c) MAJOR  
   (d) Record all evidence criteria per sign as separate Boolean fields and recompute coverage under exclusion of SA-supported signs.

17. (a) “The outcome of the criteria for each sign is recorded in the anchor table … ‘Basis’ column.”  
   (b) A free-text “Basis” column is not an operational audit trail for rule-based classification. It does not guarantee that each criterion is separately coded, countable, or reproducible, and the paper elsewhere admits needed provenance is absent.  
   (c) MAJOR  
   (d) Replace/augment free text with machine-readable criterion columns, exact counts, source IDs, and pass/fail flags.

18. (a) “Testing the full fish sign family — M047, M049, M052, M053, M054, M055, M056, M145, the signs this program’s Mahadevan–Parpola crosswalk file lists as fish-shaped”  
   (b) The family-selection rule is not independently reproducible. The crosswalk file is not printed, the source basis for each fish-shaped classification is not cited by page/figure, and the paper says the file “does not mark the family as a separate list.”  
   (c) MAJOR  
   (d) Print a fish-family table with each M-number, Parpola number, source citation/page/figure, and inclusion rationale.

19. (a) “A fish sign counts as ‘isolated’ if it is the only sign in its inscription; the count is of fishbearing seals (113)”  
   (b) The isolation definition is good, but the selection rule for “fish-bearing seals” is still not fully auditable without the occurrence listing and corpus. The denominator 113 depends on the non-public Holdat corpus and unprinted seal IDs.  
   (c) MAJOR  
   (d) Provide the full list of 113 seal IDs, site, inscription sequence, fish sign(s), and isolation status in a public supplement.

20. (a) “Counting the 27 Indusscript contexts in Laursen’s catalog, in which likewise no isolated fish sign is reported, gives the combined figure of 0/140 used in the abstract; the two parts count different units (seals and catalog contexts) and should be cited separately.”  
   (b) This is a stale/contradictory methods statement. The abstract says the two results “count different units and are not combined,” yet §3.19 says a combined 0/140 figure was used in the abstract. The paper cannot simultaneously disown and report a combined denominator.  
   (c) MAJOR  
   (d) Remove all combined 0/140 language or explicitly justify a valid combined denominator with identical units and selection rules.

21. (a) “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
   (b) The Gulf text-search method is admitted to be non-reproducible. Results from this search should not be used as evidence, even weakly, because the query itself is unknown.  
   (c) MAJOR  
   (d) Provide source files, extraction method, exact search terms/regexes, OCR settings, context list, and all hits/non-hits.

22. (a) “PMI is pointwise mutual information, in bits: PMI(a,b)=log₂[P(a,b)/(P(a)⋅P(b))], where P(a,b) is the pair’s share of all bigram tokens and P(a) and P(b) are the two signs’ shares of all sign tokens”  
   (b) The PMI denominator convention is explicitly nonstandard for bigram association because marginals are taken over all sign tokens, not left/right bigram positions. That may be a valid custom statistic, but it makes comparisons to ordinary PMI impossible and requires exact implementation. The paper does not provide enough printed counts to verify PMI=2.43 for M342·M176.  
   (c) MINOR  
   (d) Provide left/right marginal counts, total bigram tokens, total sign tokens, and recompute examples for the printed PMI values.

23. (a) “A ‘formula type’ is one INITIAL sign together with the seals whose inscriptions begin with it: the 97 types are the 97 distinct INITIAL signs found among the H+M-covered seals” / “Grouping the 97 INITIAL-sign clusters (>=3 seals, H+M readings)”  
   (b) The selection rule for the 97 clusters is inconsistent. One passage says all distinct INITIAL signs among H+M-covered seals; another says clusters with ≥3 seals. Those are not the same rule.  
   (c) MAJOR  
   (d) State one rule, print the 97-cluster table, and give counts before/after any ≥3-seal threshold.

24. (a) “We tested 394 INITIAL-sign × iconography pairs for enrichment”  
   (b) The universe of 394 pairs is not defined. The paper does not print the number of INITIAL signs, icon categories, pair inclusion/exclusion rule, or whether unobserved pairs are included. The Bonferroni correction denominator is therefore unauditable.  
   (c) MAJOR  
   (d) Print the full pair universe, icon taxonomy, included/excluded pairs, and the exact multiple-testing denominator.

25. (a) “The chi-square printed for each pair is that pair’s single-cell contribution… It is not a full 2 × 2 chi-square for the pair.”  
   (b) The paper uses a Bonferroni “threshold” on a single-cell contribution while calling the test “chi-square, one degree of freedom per pair.” A single-cell contribution is not the same as a full 2×2 test statistic. The inferential procedure is methodologically underjustified and not reproducibly interpretable from standard chi-square testing.  
   (c) MAJOR  
   (d) Either use and report full 2×2 tests with p-values and correction, or explicitly justify the single-cell statistic with its null distribution.

26. (a) “Bootstrap confidence intervals (n=1,000 resamples) were computed for the most divergent pair only.”  
   (b) The bootstrap lacks essential details: seed, interval type (percentile/basic/BCa), resampling unit confirmation, treatment of zero counts after resampling, and whether “most divergent pair” was selected before or after observing all 36 values.  
   (c) MAJOR  
   (d) State the bootstrap algorithm, seed, interval method, pair-selection rule, and provide the resampled statistic distribution.

27. (a) “The KL divergence in §3.10 is a different quantity: a one-directional divergence, DKL(Holdat|CISI), over the four positional-class shares, with 0.001 added to each share”  
   (b) The paper uses the same label “KL divergence” for two different procedures with different smoothing and symmetry rules. This invites non-reproducible interpretation unless every reported KL value is tied to its exact formula.  
   (c) MINOR  
   (d) Rename the two measures distinctly and provide formulae beside every KL result.

28. (a) “F3 redesign using phonemes that occur in Dravidian but are absent from the Sanskrit inventory used in this test … Both sound inventories used in this test are the test’s own working lists… no published Sanskrit or Dravidian phoneme-inventory source is cited”  
   (b) The phonological exclusivity test is not externally grounded. The inventories are author-created and unsourced, so another researcher has no authoritative basis for applying the same inclusion/exclusion rules.  
   (c) MAJOR  
   (d) Cite published phoneme inventories or print a justified inventory-construction protocol.

29. (a) “Testing these against the Tamil-Brahmi epigraphy terminal phoneme inventory (11 categories…): 4/7 match… no published source for that inventory is cited in this paper or in the Phase-155 record.”  
   (b) The Tamil-Brahmi comparison has an unsourced target inventory. The denominator 11 and match count 4/7 are not independently reproducible from the paper.  
   (c) MAJOR  
   (d) Cite the epigraphic source for the 11 categories and provide the sign-to-category matching table.

30. (a) “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1%”  
   (b) The vowel-harmony procedure is unstable and undefined across versions. The paper reports multiple incompatible pass rates without supplying the exact rule changes required to reproduce each.  
   (c) MAJOR  
   (d) Provide versioned test definitions, inputs, denominators, segmentation rules, and a decision on which V12 procedure is current.

31. (a) “The matching algorithm was intentionally broad… The record does not state a fuller rule for how a single segment counts as matched, and none is claimed here.”  
   (b) The expanded Meluhhan name matching is not reproducible. Segment matching is the core operation, and the paper admits its rule is absent.  
   (c) MAJOR  
   (d) Define transliteration normalization, segmentation, phonological equivalence classes, sign-reading alternatives, match scoring, and thresholds.

32. (a) “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits in the mined literature (a hit means the proposed reading appears near the sign’s number in OCR’d text)”  
   (b) “Near” is undefined. The method omits OCR source/version, window size, regexes, tokenization, disambiguation of sign numbers, duplicate-hit handling, and false-positive review. These promotions affect the headline 161 count and token coverage.  
   (c) MAJOR  
   (d) Provide the text-mining pipeline, OCR files, search expressions, proximity window, hit table with contexts, and manual validation status.

33. (a) “M198 (‘co’, 3 Parpola references; upgraded to PROVISIONAL_MEDIUM in Phase-166)” / “Phase-166 uses for a ‘strong’ reference count… M198 (3 hits) does not reach.”  
   (b) The paper uses two thresholds—≥3 for promotion and ≥4 for “strong”—without a prospective rationale. The same evidence is sufficient for a category change but insufficient for the internal confirmation label. This is not fatal, but the rule hierarchy is ad hoc.  
   (c) MINOR  
   (d) State prospectively what ≥3 and ≥4 mean, why they differ, and which threshold controls promotion.

34. (a) “Method: for each H+M sign with >=3 corpus tokens (147/161 qualify), compute I/M/T positional rates and test whether the 3-slot grammar model … correctly classifies the sign’s dominant positional class. The Phase-170 record states the rules in the order TERMINAL, INITIAL, MEDIAL, else MIXED; it does not state what happens when a sign’s rates satisfy more than one threshold”  
   (b) The tie/overlap handling for Phase-170 is explicitly missing. Because classification depends on ordered thresholds, overlapping cases can change the 137/147 result.  
   (c) MAJOR  
   (d) Define deterministic tie handling and report how many signs satisfy multiple thresholds.

35. (a) “No site-by-site coverage table for the 161-sign set exists: it was never computed, in this paper or in the program’s records.”  
   (b) The paper gives a global 161-sign coverage result but cannot report its site distribution. Since site composition is central to many claims, this is a missing denominator/selection audit for the headline set.  
   (c) MAJOR  
   (d) Compute and print site-by-site token and seal coverage for the final 161-sign set.

36. (a) “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site”  
   (b) This caveat undercuts the bootstrap inference, but the paper still reports a precise 95% CI for Mohenjo-daro vs Rakhigarhi. With no object-type controls and tiny n, the method cannot distinguish repertoire divergence from sample composition.  
   (c) MINOR  
   (d) Add object-type/motif/length controls or restrict the claim to a descriptive observed KL value.

37. (a) “Systematic mining of Parpola (1994), 38 Mahadevan papers (1970–2018), and Wells (2015)…”  
   (b) The literature-mining corpus is not bibliographically reproducible. The paper elsewhere says the “38 papers” count “could not be tied to a verifiable external source,” and the reference list does not contain 38 Mahadevan entries.  
   (c) MAJOR  
   (d) Print the full document list, source files, editions, OCR/extraction method, and inclusion criteria.

38. (a) “Mining Wells (2015) The Archaeology and Epigraphy of Indus Writing”  
   (b) The in-text citation names “Wells (2015),” but the reference list gives “Wells, B. & Fuls, A. (2015).” The citation is inconsistent with the bibliography.  
   (c) MINOR  
   (d) Use a consistent author citation and bibliographic entry.

39. (a) “Competing hypotheses have proposed … an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected)”  
   (b) “Jha & Rajaram 2000” is cited in the text but absent from the reference list.  
   (c) MAJOR  
   (d) Add the full bibliographic entry or remove the citation.

40. (a) “The comparison systems were Mesopotamian numerical signs…, heraldic charges from the Dering Roll…, and Linear B…” / “this paper gives no §8 entry and no fuller bibliographic identification for the Dering Roll source, the Mesopotamian numerical-sign table, or DAMOS”  
   (b) The paper admits key comparison datasets lack bibliographic entries. The frequency-curve control analysis is therefore not reproducible from the paper’s references.  
   (c) MAJOR  
   (d) Add full references and dataset access paths for the Dering Roll, Mesopotamian numerical signs, DAMOS, Shakti corpus, and ICIT line.

41. (a) “Comparison with the CISI corpus … mayig digitization” / “neither it nor the mayig digitization has a §8 entry”  
   (b) The cross-corpus comparison relies on uncited resources. The corpus and digitization cannot be identified from the bibliography.  
   (c) MAJOR  
   (d) Add full CISI and mayig references/access information and the exact sign-code mapping used.

42. (a) “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)”  
   (b) “Parpola 1975” is cited in text but absent from §8. The reference list instead contains “Parpola, S., Parpola, A. & Brunswig, R.H. (1977),” which is not the cited item.  
   (c) MAJOR  
   (d) Add the actual Parpola 1975 reference or correct the in-text citation to the listed 1977 work if that is intended.

43. (a) “Bilingual Parallels (1972) 3; Murukan (1999) 2; Blue Neck (2008) 2; … Toponyms (2018) 3; Encyclopaedia (1994) 5”  
   (b) These Mahadevan works are cited as mined papers but are absent from the reference list, except for other Mahadevan items. The mined corpus cannot be bibliographically audited.  
   (c) MAJOR  
   (d) Add full references for every mined Mahadevan paper named in §3.23.

44. (a) “The Arthaśāstra … documents Sanskrit superintendent titles…”  
   (b) The Arthaśāstra claim has no citation or edition. Even as an analogy, it is a sourced historical statement and needs bibliographic support.  
   (c) MINOR  
   (d) Cite the edition/translation and passage(s), or remove the claim.

45. (a) “A separate, weaker observation concerns pictures rather than script: Dilmun-style seals at Failaka Island (Hojlund & Abu-Laban 2012) show fish in compound pictorial contexts… This program’s records do not tie the observation to specific catalogue numbers, figures, or pages”  
   (b) The citation is not checkable at the level of the stated content. The paper admits it lacks catalogue numbers/pages/figures, so the cited volume cannot be verified as supporting the claim without independent searching.  
   (c) MAJOR  
   (d) Provide exact catalogue numbers, figure/page references, and a counted table, or delete the observation.

46. (a) “The external facts in this section … are as recorded in the Phase-152 record … no §8 entry covers them.”  
   (b) The Shu-ilishu external anchor facts lack bibliography. A phase report is not a scholarly source for Ur III date, museum provenance, title, or reading of the Akkadian inscription.  
   (c) MAJOR  
   (d) Add authoritative references for the seal, inscription, date, provenance, and title.

47. (a) Reference list entry: “Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”  
   (b) This reference appears orphaned. The text discusses Rao et al. “Science 324:1165” and entropy, but does not cite the PNAS Markov-model paper as a distinct source.  
   (c) MINOR  
   (d) Cite it where used or remove it from the reference list.

48. (a) Reference list entry: “Parpola, S., Parpola, A. & Brunswig, R.H. (1977). The Meluḥḥa village…”  
   (b) This reference appears orphaned. The text cites “Parpola 1975” for Meluhhan names, not this 1977 article.  
   (c) MINOR  
   (d) Cite the 1977 article explicitly if it supports the name list, or replace/add the actual cited 1975 source.

49. (a) Reference list entry: “Crawford, H. (2001). Early Dilmun Seals from Saar: Art and Commerce in Bronze Age Bahrain.”  
   (b) The reference is incomplete: no publisher, place, series, or page information is given.  
   (c) MINOR  
   (d) Supply a complete bibliographic entry.

50. (a) “AI tooling was used for scripting, data management, and literature search — including the text-mining counts…”  
   (b) The AI-assisted pipeline lacks reproducibility metadata: model/tool versions, prompts, deterministic settings, human review protocol, and whether outputs were regenerated. Given that AI-assisted text mining directly affects evidence counts and provisional promotions, this is a methods gap.  
   (c) MAJOR  
   (d) Disclose AI/tool versions, prompts or workflow specifications, validation protocol, and archived outputs sufficient to reproduce the text-mining results.

POSITIVES

1. (a) “The corpus itself is not publicly released (see §6), so corpuslevel counts cannot yet be re-run by other researchers.”  
   Positive: The paper explicitly discloses the central corpus-access limitation rather than pretending full reproduction is possible.

2. (a) “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
   Positive: The paper correctly states that confidence labels are not probabilistic error estimates.

3. (a) “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control… was applied or recorded.”  
   Positive: The paper candidly identifies a major DEDR-search audit failure.

4. (a) “No sign in the 161-set rests on SA alone… If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain.”  
   Positive: The paper gives a useful sensitivity bound for the compromised SA component.

5. (a) “A fish sign counts as ‘isolated’ if it is the only sign in its inscription; the count is of fishbearing seals (113)”  
   Positive: The fish-isolation test at least defines the event and denominator unit clearly.

6. (a) “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”  
   Positive: The headline token-coverage percentage is accompanied by exact numerator and denominator.

7. (a) “The Phase-170 record states the rules… it does not state what happens when a sign’s rates satisfy more than one threshold, and that tie/overlap handling is not on record.”  
   Positive: The paper explicitly flags missing tie handling for the Phase-170 retest.

8. (a) “No site-by-site coverage table for the 161-sign set exists: it was never computed…”  
   Positive: The paper clearly prevents readers from inferring nonexistent site-level coverage for the final 161-sign set.

---CALL-META finish_reason=stop usage={"prompt_tokens": 25199, "completion_tokens": 9772, "total_tokens": 34971, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 2744, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=29216---


## PASS 4 — HOSTILE SUMMARY

1. **(a) Quoted passage:** “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage) are Tier 2 claims supported by multiple tests. Those tests are not independent of each other — most are computed from the same corpus, and several from the same seals (§2.2) — the HIGH/MEDIUM labels are rule-based categories with no measured error rate”  
   **(b) Defect:** This is the paper’s weakest load-bearing assumption: it treats rule-triggered labels as if they can support a decipherment headline. “161 readings” is not a decipherment result; it is a count of signs assigned candidate strings by an uncalibrated rule system. The paper admits the tests are non-independent and the labels have no measured error rate, yet the title and conclusion still foreground “161 Candidate Proto-Dravidian Anchors” as if the count is substantively meaningful. Without calibration, “HIGH” and “MEDIUM” are administrative labels, not evidential confidence. The entire 161-reading headline depends on an unmeasured false-positive process.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** A validation design with measured error rates: blind application to a known ancient script, a held-out sign-reading benchmark, expert-coded acceptance/rejection of candidate readings, or a formal null estimating how often the stated DEDR/rebus/positional criteria generate plausible but false readings.

2. **(a) Quoted passage:** “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”  
   **(b) Defect:** This destroys the probative value of the rebus/DEDR component. The paper’s reading engine searches a very large lexical target space, records only successes, does not record rejected alternatives, does not define the allowed transformations, and applies no multiple-comparison control. This is textbook post hoc matching. Since the adopted DEDR candidate is often the basis for MEDIUM or HIGH status, the paper’s central 161-reading count is not statistically interpretable.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** A complete candidate-generation protocol fixed in advance, including allowed phonological transformations, all candidates considered and rejected per sign, the size of the search space, and a multiple-comparison/null model estimating false discovery rates.

3. **(a) Quoted passage:** “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”  
   **(b) Defect:** The headline quantities—7,002 tokens, 1,670 seals, 90.96% coverage, 69.8% fully covered seals, fish-sign counts, positional z-score, site counts—are all corpus-level claims, but the corpus is unavailable. The paper repeatedly asks the reader to accept counts that cannot be independently rerun from the printed text. A private corpus may be usable for exploratory work, but it cannot bear headline claims of reproducible computational decipherment.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Public release of the corpus or, at minimum, a printed/repository-verifiable inscription-level table with sign sequences, site, motif, object type, and all derived counts; alternatively, full replication on a public corpus with a published crosswalk.

4. **(a) Quoted passage:** “Neither table is printed in this paper; both are in the repository, on the branch and at the commit named above.”  
   **(b) Defect:** The paper’s central object—the 161-anchor table—is not printed. The reader cannot inspect from the paper which signs are in the headline set, what their frequencies are, what evidence each has, or whether the counts sum correctly except in scattered examples. Since the review brief provides only the paper text, the decisive evidence is absent from the manuscript itself. The DOI is explicitly not the version identifier; the decisive material is external and version-pinned to a repository the paper assumes but does not include.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Print the full 161-row H+M anchor table and the 397-sign status/frequency inventory in the manuscript or appendices, including sign, frequency, confidence, evidence criteria met, DEDR citation, and token contribution.

5. **(a) Quoted passage:** “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%). The remaining 633 tokens (9.04%) have LOW-confidence readings only.”  
   **(b) Defect:** The arithmetic checks—6,369 / 7,002 ≈ 90.96%—but the interpretation is overstated. “Coverage” is only assignment coverage, not reading coverage. The abstract admits this, but the title and conclusion continue to use the coverage figure as a headline support for decipherment. If an uncalibrated procedure can assign readings to common signs, high token coverage follows mechanically from Zipf-like skew; it does not show that the readings are correct.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Reframe the headline as “candidate assignment coverage,” not decipherment coverage, and provide a null comparison showing how much token coverage is achieved by arbitrary plausible assignments to the most frequent signs.

6. **(a) Quoted passage:** “Signs with SA consistency >= 0.15 and a DEDR entry matching the modal reading were promoted to MEDIUM. Two limits must be stated plainly. The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown. And a later test inside this program … Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”  
   **(b) Defect:** A method that failed its own held-out discrimination test is still present in the evidence chain for 43 MEDIUM signs. The paper says no sign rests on SA alone, but the pairing “SA+DEDR” is not reassuring when the DEDR side is itself an uncontrolled post hoc lexical search. The SA component adds no validated information and may launder weak DEDR matches into MEDIUM status.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Remove SA from all promotion criteria unless recalibrated on known scripts; recompute the H+M set using only non-SA evidence; print which of the 43 SA+DEDR signs survive on independent criteria.

7. **(a) Quoted passage:** “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv. If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain. That is a bound, not a recomputed headline: the audit file does not record whether any of the 43 also meets a non-SA MEDIUM criterion … so a true SA-free headline cannot be computed from the records.”  
   **(b) Defect:** The records are insufficient to recompute a central sensitivity analysis. The paper knows that 43 readings are tainted by a failed SA component, but cannot determine how many survive without it. That is not a minor bookkeeping gap; it prevents evaluation of the robustness of the 161-reading headline.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Add per-sign evidence flags for every criterion met, including whether each sign has a non-SA route to MEDIUM/HIGH, and publish a recomputed SA-free anchor count and token coverage.

8. **(a) Quoted passage:** “We fit the three-slot grammar model to the real corpus (coefficient of determination 𝑅2 = 0.9916) and to 2,000 copies of the corpus in which the signs inside each inscription were shuffled … z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **(b) Defect:** The arithmetic of the z-score checks, but the statistic being scored is underspecified in the printed paper. The manuscript does not define exactly what response variable the R² is computed over, what the fitted model is, what observations enter the regression, or how inscriptions of different length are handled. A very large z-score on an undefined statistic is not independently interpretable.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Print the full mathematical definition of the Phase-134 F1 statistic: data matrix, dependent variable, model parameters, fitting procedure, R² calculation, permutation unit, and treatment of one-sign/two-sign inscriptions.

9. **(a) Quoted passage:** “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”  
   **(b) Defect:** This concession undercuts the “three-slot positional grammar” claim. The permutation test shows non-random order relative to within-inscription shuffling; it does not establish that the correct model is classifier–title–name/case, or even that it is linguistic grammar rather than conventional emblem ordering. The paper’s headline grammar claim exceeds the tested alternative.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Formal comparison against explicit rival generative models—owner mark, commodity mark, clan emblem, cultic formula, nonlinguistic administrative tag—with predeclared metrics and out-of-sample prediction.

10. **(a) Quoted passage:** “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics: we interpret Slot 1 as an animal classifier (from the seal motif), Slot 2 as a guild or group title, and Slot 3 as a personal-name ending and case marker.”  
   **(b) Defect:** The semantic grammar is not discovered by the positional analysis; it is imposed after the fact. The paper’s title says “Three-Slot Positional Grammar,” but the substantive version of that claim—classifier/title/name-case—is interpretive and untested. Without semantics, the result is only positional clustering.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Separate “three positional classes” from “three grammatical/semantic slots,” and provide independent tests for the semantic labels, such as motif-blind prediction, repeated-name behavior, or contrastive distribution against commodity/clan alternatives.

11. **(a) Quoted passage:** “Results: 137/147 signs (93.2%) are classified by the thresholds into the positional class that is already their dominant class. This is a self-consistency check, not an accuracy measurement … so a high figure is expected by construction and the check can only catch internal contradictions.”  
   **(b) Defect:** This confirms that one of the grammar-retention tests is circular. The paper mostly discloses the circularity, but still includes the result in the results sequence and abstract-level consistency narrative. A self-classification of signs into their already dominant class contributes no evidence to the grammar claim and should not be rhetorically adjacent to genuine tests.  
   **(c) Severity:** **MINOR**  
   **(d) What would settle it:** Remove Phase-170 from evidentiary summaries or relabel it exclusively as an internal audit, not a result supporting the grammar.

12. **(a) Quoted passage:** “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1% … where the recorded verdict is V12_ACTIVE_CONCERN.”  
   **(b) Defect:** The phonological behavior of the proposed readings is unstable across the paper’s own tests. A decipherment model that cannot give a consistent vowel-harmony diagnostic, and whose own records disagree on pass rates by nearly forty percentage points, cannot use phonological compatibility as support without resolving the contradiction.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Freeze one vowel-harmony protocol, define the unit of analysis, rerun it on the current 161-sign set, report per-sign drivers, and state whether the resulting failure rate invalidates or downgrades affected readings.

13. **(a) Quoted passage:** “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs. No record supports excusing those violations as mostly short abbreviated seals, and we do not do so here. The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”  
   **(b) Defect:** Nearly a quarter of decoded seals violate the model’s own phonotactic test, and the violations are concentrated in high-frequency headline signs. This directly attacks the reliability of the proposed readings, not just rare edge cases. The paper cannot simultaneously present M211, M176, and M342 as core anchors while leaving a major phonotactic failure unresolved.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Per-sign phonotactic error analysis, revised readings where necessary, explicit downgrade/removal of signs driving violations, and recomputed coverage after correction.

14. **(a) Quoted passage:** “The candidate model is falsifiable at the first of the following points today. The other two state, in plain terms, what the completed Gulf work did and did not show, and what a stratigraphic test would have to predict before it could separate rival interpretations. 1. Discovery of a bilingual text … 2. Gulf material … no confirmation of it either … 3. Radiocarbon-dated stratigraphic contexts … No such discriminating prediction is yet on record”  
   **(b) Defect:** The title advertises a “Falsifiable Computational Decipherment Hypothesis,” but the validation path reduces present falsification largely to discovery of a bilingual text. The Gulf test gives no confirmation, and the stratigraphic test has no discriminating prediction. A hypothesis is not made operationally falsifiable by saying that a future bilingual could refute it. The computational model needs current, risky predictions against available data or public held-out corpora.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Pre-register concrete falsification criteria on data not used to build the model: public-corpus predictions, unseen inscription decoding, motif-blind sign-position predictions, or explicit rival-model comparisons with failure thresholds.

15. **(a) Quoted passage:** “Comparison with the CISI corpus … the Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere … so the percentage cannot be checked or recomputed”  
   **(b) Defect:** The cross-corpus generalization evidence contains an uncountable percentage. The paper nevertheless says “the opening-sign pattern is the one point of agreement.” An agreement point whose numerator and denominator are missing is not evidence. This matters because the paper repeatedly gestures toward generalization beyond the private Holdat corpus.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Print the CISI denominator, numerator, inscription inclusion rules, sign crosswalk, and the actual list of inscriptions counted.

16. **(a) Quoted passage:** “The fish sign is never isolated in the formal stamp seal corpus, at any site, including Lothal … This result is compatible with a range of interpretations of the fish sign’s function; the present study does not adjudicate between them but establishes the structural constraint as a corpus-level fact.”  
   **(b) Defect:** “Corpus-level fact” is too strong for a private corpus whose inscription-level data are not printed. The paper’s own caveat says “this corpus contains formal stamp seals only, and selection or object-type effects could produce the same pattern.” The result may be a useful observation, but it cannot support a general fish-sign rule for IVS, nor can it bear much weight in a decipherment argument.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** Publish the fish-bearing inscription list with object type, sign sequence, site, and image/catalog reference; replicate on public corpora including non-stamp-seal media.

17. **(a) Quoted passage:** “The Gulf extension searched about 145,000 characters of extracted text … The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
   **(b) Defect:** The Gulf fish-sign extension is irreproducible by the paper’s own admission. It also searched catalogue prose rather than images and found “no fish-sign mentions at all,” which is absence of evidence, not structural confirmation. Any abstract-level mention of the Gulf test risks overstating a null text-mining exercise.  
   **(c) Severity:** **MINOR**  
   **(d) What would settle it:** Record the search terms, files, OCR/text extraction method, the 27 contexts, and preferably image-based coding of each Gulf seal.

18. **(a) Quoted passage:** “M261 on a published source (Parpola 1994, via Phase-51)” and “M261 muruku 4988 Wheel/spindle (2 tokens; the reading is muruku, ‘young man’ — the further gloss ‘Tamil Murugan’ is withdrawn, as in §3.2)”  
   **(b) Defect:** This HIGH-confidence example appears inconsistent with the stated HIGH rule requiring “Two or more” criteria. The printed basis gives two tokens and a source-mediated reading, but the two qualifying criteria are not identified. If HIGH status can be assigned on opaque inherited authority plus minimal corpus support, the HIGH/MEDIUM distinction is not auditable from the paper.  
   **(c) Severity:** **MAJOR**  
   **(d) What would settle it:** For every HIGH sign, print exactly which two or more criteria it satisfies and the evidence values for each; if M261 does not meet two criteria, downgrade it.

19. **(a) Quoted passage:** “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits in the mined literature (a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign)”  
   **(b) Defect:** The 161 headline includes four signs promoted by OCR text proximity explicitly not verified as sign assignments. The paper flags them as provisional, but still counts them inside MEDIUM and inside the headline total. That is numerically small but conceptually damaging: the paper’s headline count includes candidates that the authors admit require expert review before promotion.  
   **(c) Severity:** **MINOR**  
   **(d) What would settle it:** Exclude PROVISIONAL_MEDIUM from the headline count, or provide expert-verified sign-by-sign literature assignments for the four signs.

20. **(a) Quoted passage:** “This study does not claim epigraphic finality … the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”  
   **(b) Defect:** The phrase “favours” is stronger than the paper’s actual discriminative evidence permits. The paper admits: “Dravidian superiority over proto-Munda has not been formally quantified,” “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary,” and a phonological-profile comparison “found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS.” The paper has shown compatibility under its chosen assumptions, not superiority.  
   **(c) Severity:** **CRITICAL**  
   **(d) What would settle it:** Replace “favours” with “is compatible with,” unless formal competing-baseline tests are run against Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan controls, and language-neutral/nonlinguistic models using the same criteria and predeclared decision rules.

---

## Hostile summary to the editor

The paper’s remaining fatal weakness is not a single arithmetic error; it is the uncalibrated conversion of internally generated candidate assignments into headline decipherment claims. The manuscript has become more candid, but the central architecture still rests on the assumption that rule-based HIGH/MEDIUM labels mean something like evidential confidence. The paper itself says they do not: the labels have no measured error rate, the tests are non-independent, the DEDR search records only adopted candidates, no rejected alternatives, no transformation inventory, and no multiple-comparison control. That is the load-bearing failure. If that assumption falls, the “161 readings” become merely 161 assignments, the “90.96% coverage” becomes assignment coverage over frequent signs, and the Proto-Dravidian claim becomes compatibility under a hand-built framework rather than evidence of decipherment.

The positional structure result is the strongest part of the manuscript, but even there the headline grammar claim outruns the evidence. The z = 10.3 arithmetic is checkable, but the underlying R² statistic is not sufficiently defined in the printed text, and the null model only shuffles signs within inscriptions. The paper explicitly did not test rival templates—owner marks, commodity marks, clan emblems—that could also yield fixed positional patterns. Thus the evidence supports non-random positional order, not the semantic grammar of classifier/title/name-case, and certainly not a Proto-Dravidian administrative grammar.

The phonological side is actively damaging. The SA machinery failed its own held-out test with 0.000 agreement and could not beat Sanskrit or scrambled controls, yet 43 MEDIUM signs still carry SA+DEDR evidence. The paper cannot recompute a true SA-free headline because its audit file lacks the necessary criterion flags. Vowel harmony remains unresolved, with incompatible pass rates across internal records, and the stricter phonotactic test reports a 23.4% violation rate concentrated in high-frequency headline signs. That is not a peripheral caveat; it attacks the readings the model most depends on.

The falsifiability claim is also overstated. The only immediate falsifier is essentially a future bilingual inscription. The Gulf test found no fish-sign mentions and cannot be rerun from the recorded search terms because none are recorded. The stratigraphic test has no discriminating prediction. A computational decipherment hypothesis should make risky predictions on public held-out data; this one mostly says future discoveries may decide.

Individually, several defects are survivable: the fish-sign result is a useful private-corpus observation; the coverage arithmetic itself checks; the paper is now unusually candid about many limits. Jointly, however, the defects are fatal to the headline claims. The paper may be publishable as an exploratory computational model of positional regularities and candidate Dravidian-compatible assignments, but not as a reliable “falsifiable computational decipherment hypothesis” with 161 meaningful anchors and 90.96% decipherment-relevant coverage. Before any field specialist should rely on it, the paper needs public or printed inscription-level data, a full printed anchor table, calibrated false-positive rates, rival-model comparison, and a recomputed reading set after removing failed or circular evidence.

---

## POSITIVES

1. **Quoted passage:** “The arithmetic of the z-score is the distance between the real value and the shuffled mean, measured in standard deviations: z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”  
   **Confirmable positive:** The arithmetic recomputes correctly from the printed inputs.

2. **Quoted passage:** “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,369 of 7,002 corpus tokens (90.96%).”  
   **Confirmable positive:** The percentage 6,369 / 7,002 rounds to 90.96%.

3. **Quoted passage:** “The four PROVISIONAL_MEDIUM signs (§2.2) account for 15 of the 6,369 tokens; without them, 157 anchors cover 6,354 tokens (90.75%).”  
   **Confirmable positive:** The subtraction 6,369 − 15 = 6,354 checks, and 6,354 / 7,002 rounds to 90.75%.

4. **Quoted passage:** “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
   **Confirmable positive:** This is a candid and necessary disclosure.

5. **Quoted passage:** “A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”  
   **Confirmable positive:** The manuscript explicitly acknowledges the uncontrolled DEDR false-positive problem.

6. **Quoted passage:** “On that record, SA agreement by itself carries no information about a sign’s value.”  
   **Confirmable positive:** The paper candidly reports that the SA machinery failed as independent evidence.

7. **Quoted passage:** “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”  
   **Confirmable positive:** The paper correctly states the limitation of its positional null model.

8. **Quoted passage:** “This is a self-consistency check, not an accuracy measurement.”  
   **Confirmable positive:** The paper properly downgrades the evidential status of the Phase-170 grammar retest.

9. **Quoted passage:** “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”  
   **Confirmable positive:** The paper no longer hides the unresolved vowel-harmony conflict.

10. **Quoted passage:** “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
   **Confirmable positive:** The data-access limitation is disclosed plainly.

---CALL-META finish_reason=stop usage={"prompt_tokens": 25164, "completion_tokens": 6765, "total_tokens": 31929, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 912, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=26606---

