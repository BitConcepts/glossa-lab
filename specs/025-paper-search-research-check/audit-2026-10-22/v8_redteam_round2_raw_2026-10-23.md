# Glossa Lab Indus Preprint v8 — Red-Team Round 2: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 74,076 chars, SHA-256 of PDF 1ef5eb721f4b9cdd7fc4f1afbe790793cd2c0ba74d48898c0331a0ae0309d2b0), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs.



## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## Findings — internal consistency, arithmetic, reproducibility

1. **Headline positional z-score does not recompute from the printed numbers.**  
   **(a) Passage:** §2.3: “real corpus (coefficient of determination 𝑅2 = 0.992) … shuffled mean 𝑅2 = 0.438, standard deviation 0.053). The z-score is … z = 10.3.”  
   **(b) Defect:** From the printed inputs, \(z=(0.992-0.438)/0.053=0.554/0.053=10.45\), i.e. 10.5 if rounded to one decimal, not 10.3. The reported z may be based on unprinted more precise mean/SD, but it cannot be reproduced from the paper.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the exact unrounded observed statistic, shuffled mean, shuffled SD, and formula used.

2. **Permutation-test minimum p-value statement is arithmetically wrong for 2,000 permutations.**  
   **(a) Passage:** Abstract and §5: “no permutation in 2,000 exceeded the observed statistic (p < 0.001; 0.001 is the smallest value a test of this size can report)”  
   **(b) Defect:** With 2,000 permutations, the naïve resolution is \(1/2000=0.0005\). With the common add-one correction, the smallest nonzero reportable p is \(1/(2000+1)=0.0004998\). “0.001 is the smallest value” is false. Reporting “p < 0.001” is compatible with zero exceedances, but the parenthetical explanation is wrong.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** State the exact permutation p convention: exceedances/2000, or \((b+1)/(n+1)\), and correct the parenthetical.

3. **Corpus-level headline statistics are declared non-reproducible by the paper itself.**  
   **(a) Passage:** Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” §6: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
   **(b) Defect:** Many headline counts—7,002 tokens, 1,670 seals, 390 attested signs, positional rates, bigrams, KL values, bootstrap intervals, fish counts—depend on a private corpus. Some percentages recompute from printed totals, but the underlying counts cannot be independently audited from the paper.  
   **(c) Severity:** **CRITICAL** for reproducibility of corpus-level claims.  
   **(d) Settle by:** Release the corpus or at minimum publish the full inscription-level sign sequences and metadata needed to recompute every count.

4. **Gulf fish-sign denominator is a unit shift: seals vs catalog contexts are combined as if commensurable.**  
   **(a) Passage:** Abstract: “0 isolated fish signs in the 1,670-seal corpus (0/113 across 9 corpus sites) and 0 in the Gulf deposit catalog (0/27; Laursen 2010), for a combined result of 0/140.” §3.19: “Counting the 27 Indus-script contexts in Laursen’s catalog … gives the combined figure of 0/140 used in the abstract; the two parts count different units (seals and catalog contexts) and should be cited separately.”  
   **(b) Defect:** The paper admits the combined denominator mixes different units: 113 fish-bearing Holdat seals + 27 Gulf “contexts.” The abstract nevertheless reports “combined result of 0/140,” which implies one denominator. That is statistically invalid.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Report only separate denominators: 0/113 fish-bearing Holdat seals and 0/27 Gulf catalog contexts, with no combined fraction unless units are harmonized.

5. **Gulf fish-sign evidence is contradicted between §3.19 and §4.5.**  
   **(a) Passage:** §3.19: “That text search found no mention of an isolated fish sign — and … no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits). An absence in catalogue prose is weaker evidence than inspection of the seal images … the Gulf material provides no counterexample … but it does not independently confirm it.” §4.5: “No isolated fish signs found in Gulf context. Verdict: COMPOUND_ONLY_EXTENDED — fish sign is compound-only across both mainland and Gulf corpora.”  
   **(b) Defect:** §3.19 says the Gulf search found no fish-sign mentions at all and does not independently confirm compound-only behavior. §4.5 upgrades this to “fish sign is compound-only across both mainland and Gulf corpora.” That is a strength-of-evidence contradiction.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Either provide image-inspection counts for the 27 Gulf contexts or downgrade §4.5 to match §3.19.

6. **Fish-sign “across all 9 sites” claim is not supported by the printed table.**  
   **(a) Passage:** Abstract: “0/113 across 9 corpus sites.” §3.5 table rows: “Lothal … Harappa … Mohenjo-daro … Dholavira … All others … Total.”  
   **(b) Defect:** The paper claims site-invariance across 9 sites, but the printed table collapses five sites into “All others.” The total 6+33+35+11+28=113 checks, but the per-site 9-site claim cannot be checked.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print all nine site rows separately.

7. **M267 chi-square test cannot be reproduced from printed inputs.**  
   **(a) Passage:** §3.4: “M267 appears across all motif types — unicorn (127 tokens), zebu bull (72), elephant (37), rhinoceros (25), etc. … chi-square = 12.98, p = 0.1124.”  
   **(b) Defect:** The motif counts are incomplete (“etc.”), expected counts are not printed, and the number of motif categories/degrees of freedom is not stated. The p-value roughly suggests df≈8, but that is not stated.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the full motif contingency table, expected counts, degrees of freedom, and exact test formula.

8. **Iconographic chi-square values in §3.8 cannot be reproduced from printed observed/expected cells.**  
   **(a) Passage:** §3.8: “394 INITIAL-sign × iconography pairs … chi-square … Strongest associations: M060 observed 20 expected 2.0 chi-square 158.5; M045 observed 24 expected 2.9 chi-square 155.3 …”  
   **(b) Defect:** A one-cell approximation \((O-E)^2/E\) gives M060 \(=18^2/2=162\), not 158.5. Other rows are close but not exact. Full 2×2 margins are not printed, so the stated chi-square values cannot be reproduced.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the 2×2 table for each association or the exact formula and all margins.

9. **Bigram and PMI claims cannot be reproduced from printed data.**  
   **(a) Passage:** §3.7: “we extracted 2,647 distinct bigrams … including 1,485 H+M-by-H+M bigrams … M342·M176 … 122 seals (7.3% of corpus, PMI=2.43) … M267·M099 (84 seals), M099·M342 (81 seals), and M176·M099 (74 seals).”  
   **(b) Defect:** 122/1670=7.31%, so the percentage checks. But the distinct-bigram count, H+M-by-H+M count, PMI=2.43, and next-cluster counts cannot be recomputed because total bigram tokens, marginal frequencies, and PMI definition/log base are not printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the full bigram count table, marginal counts, and PMI formula.

10. **Formula-type count cannot be checked.**  
   **(a) Passage:** §3.7: “97 distinct formula types are identified, organised by INITIAL sign.”  
   **(b) Defect:** No definition of “formula type” sufficient to reproduce the count is printed, and no table is included in the paper.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Define “formula type” operationally and print the 97-type list or enough counts to verify it.

11. **CISI 87% opening-sign figure lacks denominator.**  
   **(a) Passage:** §3.10: “87% of CISI multi-sign inscriptions open with an INITIAL-class sign (the number of multi-sign inscriptions in that subset is not recorded in the Phase-145 report).”  
   **(b) Defect:** The paper explicitly says the denominator is not recorded. The 87% cannot be audited, and no integer numerator/denominator can be recovered.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the number of CISI multi-sign inscriptions and the count opening with INITIAL-class signs.

12. **KL-divergence statistics lack formula, smoothing, and full inputs.**  
   **(a) Passage:** §3.10: “KL divergence = 0.591.” §3.14: “all 36 site-pair KL divergences … Mohenjo-daro vs Rakhigarhi KL=0.509, 95% CI [0.483, 0.750] … Mohenjo-daro vs Harappa … KL=0.070.”  
   **(b) Defect:** KL divergence is undefined operationally: sign repertoire distribution? token distribution? smoothing? direction \(D_{KL}(P||Q)\) or symmetrized? The bootstrap resampling unit is not fully specified. None of the KL values or CIs can be reproduced from printed data.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the site-by-sign count matrix, KL formula, smoothing convention, direction/symmetrization, and bootstrap procedure.

13. **Rakhigarhi KL range is internally inconsistent with the listed values.**  
   **(a) Passage:** §3.14: “The other Rakhigarhi pairs have observed KL values between 0.249 and 0.481 (Harappa 0.481, Kalibangan 0.350, Lothal 0.348, Dholavira 0.320, Chanhu-daro 0.291, Surkotada 0.290, Banawali 0.250).”  
   **(b) Defect:** The listed minimum is 0.250, not 0.249.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Correct the range or add the missing 0.249 pair if it exists.

14. **Polysemy permutation p-value cannot be reproduced from the printed summary.**  
   **(a) Passage:** §3.13: “Observed collocate divergence rate: 66.7% of the 21 tested signs … Null distribution mean: 80.7% (SD=0.088). The observed rate is below the null mean (z = −1.6; one-tailed permutation p = 0.955).”  
   **(b) Defect:** 66.7% of 21 implies 14/21. \(z=(0.667-0.807)/0.088=-1.59\), so z≈−1.6 checks. But the permutation p=0.955 cannot be reproduced from the mean/SD alone; the permutation exceedance count is not printed.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Print the number of permutations at or beyond the observed statistic and define the tail.

15. **Phonological exclusivity p-value is only partially reproducible.**  
   **(a) Passage:** §3.11: “35/157 (22%) contain Dravidian-side markers … below the rate the test’s own null model expects (35%; binomial p = 0.9996).”  
   **(b) Defect:** 35/157=22.3%, so the percentage checks. A binomial calculation with \(n=157,p_0=0.35\) can plausibly produce a very large one-tailed p, but the tail direction is not stated. “p = 0.9996” is not fully reproducible without knowing whether the test is \(P(X \ge 35)\), \(P(X \le 35)\), or two-sided.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** State the exact binomial null and tail.

16. **Tamil-Brahmi broader 8/11 count is explicitly not reproducible.**  
   **(a) Passage:** §3.18: “A second, broader count … reaches 8 of the 11 categories (73%), but it is post hoc, its derivation is not fully recorded.”  
   **(b) Defect:** 8/11=72.7%, so the percentage checks, but the paper admits the derivation is not fully recorded. This count should not be used as evidence.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the sign-to-terminal-category mapping and pre/post hoc status for each category.

17. **Vowel-harmony status contradicts itself between §3.17 and §3.21.**  
   **(a) Passage:** §3.17: “The V12 vowel-harmony warning is unresolved … V12_ACTIVE_CONCERN … vowel harmony is an open problem for the reading set.” §3.21: “consistent with our Phase-154 finding that V12 is a methodology artifact.”  
   **(b) Defect:** §3.17 explicitly withdraws the “methodology artifact” explanation; §3.21 reinstates it.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Make §3.21 match §3.17, or provide evidence that the Phase-154 concern was resolved.

18. **Vowel-harmony counts mix pass rates and violation counts without reconciling denominators.**  
   **(a) Passage:** §3.17: “75.3% (Phase-132: 476 of 632 decoded seals …), 64.2% …, or 36.1% (Phase-154: 417 of 1,154 seals checked), where … 418 violations are word-internal.”  
   **(b) Defect:** 476/632=75.3% and 417/1154=36.1% check. But “417 of 1,154 seals checked” and “418 violations” are different units. The paper does not say whether multiple violations per seal are allowed or whether 418 violations correspond to 417 passing, failing, or checked seals.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Print pass/fail seal counts and violation counts separately.

19. **Mahadevan grammar-hit counts are inconsistent or unreconciled.**  
   **(a) Passage:** §3.21: “the grammar paper contains 79 positional-class references and 61 grammar structure agreement hits.” §3.23: “Grammar of Indus Texts (1986): 8 hits; What Do We Know (1989): 7 hits; Terminal Ideograms (1982): 6 hits.”  
   **(b) Defect:** The paper gives 61 grammar-structure hits in §3.21 but only 8+7+6=21 hits for the named Mahadevan papers in §3.23. These may be different mining definitions, but the distinction is not explained.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Define each hit type and provide the complete per-document hit table.

20. **“10/10 Mahadevan papers” claim is unsupported by the later disclosure.**  
   **(a) Passage:** §1.3 bullet 12: “Cross-validation: 10/10 Mahadevan papers (1972–2018) are consistent with the positional grammar model.” §3.23: “the aggregate counts ‘10 papers, 1972–2018’ … are this program’s own corpus counts and could not be tied to a verifiable external source.”  
   **(b) Defect:** A headline “10/10” claim is later admitted to be an internal, unverifiable corpus count. That is not auditable cross-validation.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** List the 10 papers, the mined passages, and the coding rule for “consistent.”

21. **§3.23 says “independent decades” while also admitting one-scholar dependence.**  
   **(a) Passage:** §3.23: “These are one scholar’s works across four decades, not independent witnesses” and later: “Across four independent decades of scholarship…”  
   **(b) Defect:** The section contradicts itself. Decades are chronological bins, not independent witnesses, especially when the source is one scholar’s corpus.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Remove “independent” or justify statistical independence.

22. **Provisional-medium status of the four sibilant signs is inconsistent.**  
   **(a) Passage:** §2.2: “PROVISIONAL_MEDIUM (4 signs — M330, M165, M202, M198).” §3.1: “PROVISIONAL_MEDIUM … 4.” §3.27: “M198 … stays provisional while the other three do not.”  
   **(b) Defect:** The confidence table and methods say all four are PROVISIONAL_MEDIUM; §3.27 says only M198 remains provisional. This changes the category counts.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** State whether M330, M165, and M202 are ordinary MEDIUM or PROVISIONAL_MEDIUM, and update all counts consistently.

23. **Phase-163/166 sibilant promotion thresholds conflict.**  
   **(a) Passage:** §3.25: “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits…” §3.27: “M198 … met the >=3 promotion threshold of Phase-163 but not the >=4 threshold Phase-166 uses for a ‘strong’ reference count.”  
   **(b) Defect:** Two thresholds are used for closely related status decisions, but the effect on category labels is unclear. If >=4 makes signs no longer provisional, then §2.2 and §3.1 are wrong; if not, §3.27 is wrong.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Provide a decision table showing hit count, DEDR support, position, final confidence label, and whether “provisional” remains.

24. **Hypothetical blocker coverage increase cannot be derived.**  
   **(a) Passage:** §3.29: “If these 19 blockers were promoted to MEDIUM, token coverage would rise from 90.96% to an estimated 92.35%.”  
   **(b) Defect:** The increase is 1.39 percentage points. On 7,002 tokens, that implies about \(0.0139 \times 7002 = 97.3\) additional tokens. The paper does not print the token counts of the 19 blockers, so 92.35% cannot be checked.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the 19 signs and their token counts.

25. **Phase-133 comparison arithmetic is wrong in §3.31.**  
   **(a) Passage:** §3.31: “Phase-133’s 44.3%, which measured how well the grammar pattern matched whole inscriptions (full match 5.1%, partial 38.4%).”  
   **(b) Defect:** 5.1% + 38.4% = 43.5%, not 44.3%. Either one of the components or the total is wrong.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Print the Phase-133 numerator/denominator for full, partial, and total matches.

26. **Phase-170 “classification” has undefined tie/overlap handling.**  
   **(a) Passage:** §3.31: “TERMINAL if T>=0.60, INITIAL if I>=0.50, MEDIAL if M>=0.65.”  
   **(b) Defect:** The thresholds can in principle overlap or fail to assign a sign. The paper reports “137/147 signs (93.2%) are classified,” but does not define precedence if multiple thresholds are met, or how unclassified signs are counted.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** State the decision order and provide the 147-sign classification table.

27. **Appendix B frequency statement conflicts with body.**  
   **(a) Passage:** §3.6: “18 signs with corpus frequency 5–7.” §4.3: “Eighteen signs with corpus frequency 5–7.” Appendix B: “These 18 signs have corpus frequencies of 5 (sixteen signs) or 6 (M270, M386) — 92 tokens in total.”  
   **(b) Defect:** The body says 5–7, but Appendix B says only 5 or 6. Appendix arithmetic checks: \(16\times5 + 2\times6 = 92\). No sign of frequency 7 is present.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Change “5–7” to “5–6” or identify the omitted frequency-7 sign.

28. **Internal-consistency-suite result changes across abstract and appendix.**  
   **(a) Passage:** Abstract: “Internal consistency checks pass (59/59, Phases 1–170).” Appendix C: “At Phase-170 (May 2026) … 59 checks, all passing … the suite has since changed: on the October 2026 execution tree it reported 40 passed, 0 failed, 8 warnings.”  
   **(b) Defect:** The paper is dated “revised October 2026,” but the abstract reports the older 59/59 May suite rather than the October 40-pass/8-warning suite. This is a denominator shift in the paper’s own consistency audit.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Report the current October suite in the abstract, or explicitly label 59/59 as historical and not current.

29. **“All phase reports, scripts, and anchor table” availability does not make corpus-level numbers reproducible.**  
   **(a) Passage:** §5: “All phase reports, scripts, and the anchor table are available…” §6: “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus…”  
   **(b) Defect:** The conclusion’s availability statement can be read as reproducibility; §6 says corpus-level reproduction is impossible without private data. For an arithmetic audit, the latter controls.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** In §5, explicitly state that corpus-level numerical results are not reproducible from the repository alone.

30. **Text-mining counts are not auditable from printed inputs.**  
   **(a) Passage:** §3.20: “Mining Wells … 284 sign references, 96 Dravidian language claims, 403-reference positional analysis appendix.” §3.22: “Mining Parpola … 1,566,507 chars: 44/75…” §3.24: “Systematic mining of Parpola (1994), 38 Mahadevan papers … and Wells (2015) … yielded 0 new direct M-number reading assignments…”  
   **(b) Defect:** Counts from OCR/text mining depend on preprocessing, OCR quality, search strings, and relevance coding. The paper does not print enough to reproduce them. Some are also admitted as internal counts “could not be tied to a verifiable external source” in §3.23.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Publish the exact text corpus, OCR outputs, search queries, match lists, and manual coding rules.

31. **Parpola 44/75 overlap is arithmetically correct but evidentially narrower than abstract wording suggests.**  
   **(a) Passage:** Abstract: “44 (59%) also appear in Parpola (1994).” §3.22: “the count records appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”  
   **(b) Defect:** 44/75=58.7%, so 59% is correct. But “readings … appear in Parpola” can be mistaken for sign-level agreement; §3.22 says it is not.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** In the abstract, say “44/75 reading strings appear in Parpola’s text; not sign-by-sign agreement.”

32. **§3.21 claims V12 absence in Mahadevan supports artifact status, but Mahadevan did not run the paper’s V12 test.**  
   **(a) Passage:** §3.21: “The vowel harmony issue (V12 warning) is absent from Mahadevan’s analysis, consistent with our Phase-154 finding that V12 is a methodology artifact…”  
   **(b) Defect:** Absence from Mahadevan’s analysis is not a numerical test result and cannot resolve the Phase-154 violation counts. It is also inconsistent with §3.17’s “open problem” statement.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Remove this inference or provide a direct reanalysis showing the violations are artifacts.

33. **End-matter word count is not credible.**  
   **(a) Passage:** End: “Word count: ~3,800.”  
   **(b) Defect:** The supplied paper spans 23 pages with dense sections, tables, appendices, references, and far exceeds ~3,800 words. The stated word count is not internally credible.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Recompute word count from the actual manuscript text and state whether references/appendices are included.

34. **SA-based MEDIUM criterion is internally undercut by the stated held-out failure.**  
   **(a) Passage:** §2.2: “MEDIUM … DEDR rebus match with SA-consistency >= 0.15…” §2.4: “Phase-107 … held-out test: its agreement on held-out anchors was 0.000 … SA agreement by itself carries no information…”  
   **(b) Defect:** A MEDIUM promotion criterion uses SA consistency, while §2.4 says SA agreement has zero held-out agreement and no information by itself. This is not an arithmetic error, but it is an internal evidentiary inconsistency affecting counts of MEDIUM signs.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle by:** Recompute MEDIUM counts excluding signs whose only support is SA, or print a provenance table separating SA-only from independently supported MEDIUM signs.

35. **Substrate promotion count is underspecified.**  
   **(a) Passage:** §2.5: “For signs resisting Dravidian decipherment (25 signs, Phase-123), we check…” §4.2: “Two signs (M374=kul, M351=vī, six tokens each) are assigned candidate Munda substrate readings…”  
   **(b) Defect:** The paper gives 25 checked signs and 2 promoted substrate readings, but no table of the 25 or rejection counts. The “two signs” count is consistent with §3.3, but the substrate-analysis denominator cannot be audited.  
   **(c) Severity:** **MINOR**  
   **(d) Settle by:** Print the 25-sign substrate-audit table.

---

## Verified arithmetic / consistency checks that do pass

1. **Site counts sum to total seals.** §2.1: 606+492+110+106+124+78+61+60+33 = 1,670.

2. **Catalogue arithmetic checks.** §2.1: M001–M416 with 19 unused gives 416−19 = 397 catalogue signs. 390 attested + 7 zero-token catalogue signs = 397.

3. **Confidence-count table adds correctly.** §3.1: HIGH 75 + MEDIUM 86 + LOW 236 = 397. MEDIUM excluding provisional 82 + provisional 4 = 86. H+M 75+86 = 161.

4. **Token coverage headline checks.** §3.1: 6,369/7,002 = 90.9597% → 90.96%. Remaining 633/7,002 = 9.0403% → 9.04%.

5. **Without provisional signs checks.** §3.1: 6,354/7,002 = 90.7455% → 90.75%. Provisional tokens: 6,369−6,354 = 15; 15/7,002 = 0.214% → 0.21%.

6. **Implied HIGH/MEDIUM token percentages are plausible integer-rounded values.** §3.1: If HIGH tokens are 4,925, 4,925/7,002 = 70.34%; if MEDIUM-including-provisional tokens are 1,444, 1,444/7,002 = 20.62%; 4,925+1,444 = 6,369.

7. **Seal coverage checks.** §3.6: 1,165/1,670 = 69.76% → 69.8%; 505/1,670 = 30.24% → 30.2%; 1,165+505=1,670.

8. **Fish-sign table total checks.** §3.5: 6+33+35+11+28 = 113 fish-bearing seals; isolated 0/113 = 0%; compound 113/113 = 100%.

9. **M267 positional percentages check.** §3.4: 324+59+17 = 400; 324/400 = 81.0%.

10. **M342 and M176 terminal percentages check approximately.** §3.3: “96%” of 584 implies about 561 terminal tokens; “94%” of 356 implies about 335 terminal tokens. These are plausible rounded percentages, though raw terminal counts are not printed.

11. **Bigram percentage checks.** §3.7: 122/1,670 = 7.31% → 7.3%.

12. **Iconographic-pair percentage checks.** §3.8: 63/394 = 15.99% → 16%.

13. **Semantic-cluster table checks.** §3.12: clusters 51+25+6+9+6 = 97. Seals 845+446+145+135+99 = 1,670. Percentages: 50.6%, 26.7%, 8.7%, 8.1%, 5.9% all recompute.

14. **Phonological-marker percentages check.** §3.11: 35/157 = 22.3% → 22%; 39/161 = 24.2%; 0/157 and 0/161 are consistent.

15. **Tamil-Brahmi percentages check.** §3.18: 4/7 = 57.1% → 57%; 8/11 = 72.7% → 73%; 270/1,154 = 23.4%.

16. **Parpola overlap percentage checks.** §3.22: 44/75 = 58.7% → 59%.

17. **LOW-sign reduction after four promotions checks.** §3.24: 240 LOW at Phase-161 minus 4 sibilant promotions = 236 current LOW signs.

18. **H+M increase after sibilant additions checks.** §3.25: 157+4 = 161.

19. **Phase-166 corpus-token counts for four sibilants sum to the stated provisional-token total.** §3.27: M330 3 + M165 2 + M202 4 + M198 6 = 15, matching §3.1’s “four PROVISIONAL_MEDIUM signs … account for 15” tokens.

20. **Master-evidence category breakdown checks.** §3.30: 12 STRUCTURAL + 8 LINGUISTIC + 8 EXTERNAL + 4 DECIPHERMENT = 32 evidence items. Challenge count 4+6 = 10.

21. **Phase-170 percentage checks.** §3.31: 137/147 = 93.197% → 93.2%. Also 147/161 qualifying signs implies 14 H+M signs have fewer than 3 corpus tokens.

22. **Appendix B token total checks.** Appendix B: sixteen signs at frequency 5 plus two signs at frequency 6 gives \(16×5 + 2×6 = 92\). 92/7,002 = 1.31%.

23. **Combined fish denominator arithmetic itself checks, even though the unit combination is invalid.** Abstract/§3.19: 113+27 = 140. The defect is the unit shift, not the addition.

---CALL-META finish_reason=stop usage={"prompt_tokens": 19504, "completion_tokens": 12171, "total_tokens": 31675, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 4503, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=26143---


## PASS 2 — CLAIM-STRENGTH & VERDICT-LABEL AUDIT

## Claim-strength and verdict-label audit — offending sentences, section by section

1. **Abstract — “robust” and Proto-Dravidian/admin claim outrun the actual test**
   - **(a) Quote + section:** Abstract: “We find robust non-random positional structure (z = 10.3; no permutation in 2,000 exceeded the observed statistic (p < 0.001; 0.001 is the smallest value a test of this size can report)), a recurring three-slot inscription formula consistent with a Proto-Dravidian administrative vocabulary framework, and propose 161 candidate readings at HIGH or MEDIUM confidence.”
   - **(b) Defect:** The permutation result supports non-random within-inscription order under one shuffle null. It does **not** establish that the three slots are “Proto-Dravidian,” “administrative,” or a “vocabulary framework.” §3.2 explicitly admits: “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics,” and “it was not tested against rival templates such as owner marks, commodity marks, or clan emblems.” The sentence fuses a strong statistical positional result with untested semantic and linguistic interpretation.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Separate the supported claim — non-random positional ordering under the stated shuffle null — from the unsupported semantic/linguistic claim. To justify the stronger wording, provide formal model comparison against non-Dravidian and non-administrative rival templates.

2. **Abstract — HIGH/MEDIUM confidence promoted despite uncalibrated labels and failed SA machinery**
   - **(a) Quote + section:** Abstract: “We find robust non-random positional structure … and propose 161 candidate readings at HIGH or MEDIUM confidence.”
   - **(b) Defect:** §2.2 says HIGH/MEDIUM/LOW “are not calibrated probabilities: no measured error rate attaches to any label.” §2.4 says the SA machinery had “agreement on held-out anchors” of “0.000” and that “SA agreement by itself carries no information about a sign’s value.” Yet MEDIUM status in §2.2 can be assigned by “DEDR rebus match with SA-consistency >= 0.15.” Calling these readings “HIGH or MEDIUM confidence” in the abstract overstates what the paper’s own evidence standards support.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Report “rule-based HIGH/MEDIUM categories” rather than “confidence,” or provide calibration against known scripts and remove/promote-demote all SA-dependent readings according to the failed Phase-107 result.

3. **Abstract — internal consistency “pass” is stale/misleading in revised version**
   - **(a) Quote + section:** Abstract: “Internal consistency checks pass (59/59, Phases 1–170).”
   - **(b) Defect:** Appendix C says: “At Phase-170 (May 2026), the program’s internal consistency suite … reported 59 checks, all passing,” but also: “the suite has since changed: on the October 2026 execution tree it reported 40 passed, 0 failed, 8 warnings.” The paper is marked “revised October 2026,” so the abstract’s bare “59/59” pass label suppresses the later 8-warning state.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** State both results in the abstract or use the October execution-tree result only.

4. **§1.3 — Mahadevan “10/10” consistency claim is not supported by later disclosure**
   - **(a) Quote + section:** §1.3: “Cross-validation: 10/10 Mahadevan papers (1972–2018) are consistent with the positional grammar model”
   - **(b) Defect:** §3.23 later admits the aggregate counts “‘10 papers, 1972–2018’ and, in §3.24, ‘38 papers’ are this program’s own corpus counts and could not be tied to a verifiable external source.” It further says these are “one scholar’s works,” “not independent witnesses,” and that “consistent with” only means text mining found terminology and positional classes “of the kinds the model uses.” The §1.3 bullet reads like external cross-validation; the later evidence is internal, unverified text mining of one scholar’s corpus.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Replace with a narrower statement: “Program text-mining found positional terminology in some Mahadevan works; this is not independent validation.”

5. **§1.3 — Gulf fish-sign “validation/corroboration” is contradicted by §3.19**
   - **(a) Quote + section:** §1.3: “Gulf seal validation: fish-sign compound-only pattern corroborated in Laursen (2010) Gulf deposit catalog”
   - **(b) Defect:** §3.19 says the Gulf extension found “no fish-sign mentions at all in the Laursen text,” that “An absence in catalogue prose is weaker evidence than inspection of the seal images,” and that “the Gulf material provides no counterexample … but it does not independently confirm it.” “Corroborated” and “validation” are too strong for a text-search null with zero fish-sign hits.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Replace with: “No Gulf counterexample was found in the searched catalog prose; image-level verification remains undone.”

6. **§1.3 / §3.27 — sibilant “supported” labels exceed evidence from text proximity**
   - **(a) Quote + section:** §1.3: “Sibilant DEDR cross-validation (Phase-166): M330=can, M165=cul, M202=can (within-model supported); M198=co (provisional) — all 4 DEDR-backed”
   - **(b) Defect:** §3.25 says the promotion evidence is text proximity in OCR’d literature: “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign.” §3.27 then gives “SUPPORTED_WITHIN_MODEL” labels to signs with only 2–4 corpus tokens for three cases and proximity hits, not verified sign assignments. DEDR backing only shows the syllable/root exists; it does not validate assignment to the Indus sign.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Downgrade to “exploratory candidates with DEDR-compatible forms” until hand-checked literature assignments and independent positional/iconographic evidence are supplied.

7. **§2.2 / §2.4 — MEDIUM promotion criterion relies on SA despite admitted failure**
   - **(a) Quote + section:** §2.2: “MEDIUM (86 signs): Single strong evidence source: - DEDR rebus match with SA-consistency >= 0.15 from syllabic language model simulation”
   - **(b) Defect:** §2.4 says the 0.15 threshold “has never been calibrated against a known script,” and Phase-107 found held-out agreement “0.000,” with Sanskrit and scrambled controls indistinguishable. The paper’s own evidence says SA consistency is not a “strong evidence source.”
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Remove SA-only MEDIUM promotions or relabel them LOW/UNCONFIRMED until SA is calibrated and passes held-out testing.

8. **§2.4 — MEDIUM label remains attached to readings the paper calls unconfirmed**
   - **(a) Quote + section:** §2.4: “MEDIUM readings whose only support is SA consistency should therefore be read as unconfirmed candidates; the provenance of every anchor, including which readings have SA in their chain of support, is recorded in the repository (Phase-108 provenance register; Phase-109 re-review).”
   - **(b) Defect:** The label “MEDIUM” conflicts with “unconfirmed candidates” where SA is the only support and SA has failed a held-out test. The sentence admits the problem but does not propagate the demotion into the headline 161 H+M count.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Publish counts excluding SA-only MEDIUM readings, or split MEDIUM into independently supported vs SA-only unconfirmed candidates.

9. **§2.5 — substrate MEDIUM promotions not supported by later substrate discussion**
   - **(a) Quote + section:** §2.5: “Signs with substrate matches and near-Dravidian cognates are promoted to MEDIUM with substrate notation.”
   - **(b) Defect:** §3.3 says for M374 “no Munda source for it is cited in our records,” and for M351 “no regular sound correspondence or borrowing pathway has been shown, so the Munda derivation is unestablished.” The promotion criterion claims substrate matches; the actual examples lack documented substrate evidence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Demote substrate-based MEDIUM readings unless cited Munda/BMAC/Brahui/Elamo-Dravidian sources and sound correspondences are supplied.

10. **§3.2 — “identifies a consistent three-slot pattern” is acceptable only for positions, not formula semantics**
   - **(a) Quote + section:** §3.2: “Statistical analysis of inscription structure identifies a consistent three-slot pattern: [SLOT 1: INITIAL] – [SLOT 2: MEDIAL] – [SLOT 3: TERMINAL]”
   - **(b) Defect:** The positional trichotomy may be supported, but the paper later treats it as a “formula” with classifier/title/name semantics. Immediately after, §3.2 admits semantic labels are “this model’s interpretation, not outputs of the statistics” and rival templates were not tested. The sentence is too easily read as establishing the whole grammar formula, not merely positional classes.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Rewrite as “identifies recurrent positional classes” and reserve “formula” for a separately tested semantic model.

11. **§3.2 — “establish” overstates threshold-derived positional categories**
   - **(a) Quote + section:** §3.2: “Positional statistics establish the three positions and which signs favour each.”
   - **(b) Defect:** The statistics measure where signs occur; they do not “establish” that the positions are meaningful grammatical slots. §3.31 says positional thresholds are “program conventions, with no sensitivity analysis on record.” “Establish” is too strong without sensitivity analysis and rival-template comparison.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Replace “establish” with “measure” or “classify under the stated thresholds.”

12. **§3.3 — HIGH-confidence table contains non-iconographic, distributional interpretations**
   - **(a) Quote + section:** §3.3: “HIGH confidence (iconographic anchors):”
   - **(b) Defect:** The same table includes M342 and M176, whose bases are explicitly distributional: “the case-suffix label is an interpretation of that distribution, not a demonstrated paradigm” and “the gender label is likewise an interpretation of distribution.” Labeling the table “iconographic anchors” is inaccurate, and HIGH confidence is too strong for grammatical values not demonstrated by a paradigm.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Split iconographic HIGH anchors from distributional grammatical candidates and downgrade labels unless paradigmatic evidence is shown.

13. **§3.6 — personal-name explanation overreaches low-frequency evidence**
   - **(a) Quote + section:** §3.6: “Of these, 18 signs with corpus frequency 5–7 resist MEDIUM promotion entirely (Appendix B); they occur in equal frequency at all sites and motif types, consistent with personal-name syllables whose assignment requires a larger corpus or a bilingual text.”
   - **(b) Defect:** With frequencies of only 5–7 per sign, “equal frequency at all sites and motif types” is not a meaningful support for personal-name syllables. §3.9 admits “the statistics alone do not distinguish” personal-name syllables from “any medial-only sign class.”
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Replace with “one possible interpretation is personal-name syllables; the current evidence does not distinguish this from other medial-only classes.”

14. **§3.7 — descriptive “show” conflicts with INCONCLUSIVE permutation verdict**
   - **(a) Quote + section:** §3.7: “Positional constraint test (Phase-142D): 17/21 tested H+M signs show position-specific collocate profiles — the collocate sets of signs in INITIAL position differ systematically from those same signs in non-INITIAL positions.”
   - **(b) Defect:** The next sentence says: “The permutation test’s own verdict was INCONCLUSIVE … this test is not evidence for or against position-specific collocates.” §3.13 reports the observed rate was below the null mean. “Show” and “differ systematically” are too strong for a test later declared not above chance.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Rewrite as “descriptively differed in 17/21 signs, but the permutation test did not show above-chance divergence.”

15. **§3.8 — co-selection conclusion is generalized beyond the reported enriched subset**
   - **(a) Quote + section:** §3.8: “This shows that the inscription’s INITIAL sign and the carved animal on the same seal are co-selected, not independent decorations.”
   - **(b) Defect:** The test found 63/394 pairs pass a corrected threshold, and the adversarial recheck estimates “about 43 of the 63 are robust.” That supports some enriched sign-icon pairs, not the blanket claim that “the inscription’s INITIAL sign and the carved animal” generally are co-selected.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Limit the claim to “a subset of INITIAL sign/icon pairs shows enrichment.”

16. **§3.12 — common grammar skeleton inferred from model-derived semantic domains**
   - **(a) Quote + section:** §3.12: “All domains share the same terminal sign profile (M342/M176 dominant), consistent with a common grammar skeleton across semantic registers.”
   - **(b) Defect:** The semantic domains are derived from the proposed readings, many of which are model-dependent. Shared terminal signs show shared terminal distribution; “semantic registers” and “common grammar skeleton” are interpretive additions not independently tested.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** State only that clusters grouped by proposed readings have similar terminal profiles; test semantic registers independently.

17. **§3.12 — guild-identity interpretation not established by the clustering**
   - **(a) Quote + section:** §3.12: “The ANIMAL_GUILD domain (animal-named INITIAL signs paired with matching animal icons) accounts for 26.7% of seals — consistent with a totem-based guild identity system.”
   - **(b) Defect:** The paper repeatedly admits guild identity is untested: §3.2 says rival templates such as “owner marks, commodity marks, or clan emblems” were not tested, and §4.1 says directory vs commodity ledger “have not been separated by any test yet.” “Consistent with” is technically hedged, but here it functions as a semantic promotion from circular animal-sign/icon pairing to guild identity.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Add explicit rival-model comparison among guild, clan, ownership, cultic, and commodity interpretations.

18. **§3.12 — administrative/devotional registers are asserted, not shown**
   - **(a) Quote + section:** §3.12: “CIVIC_ROLE (ūr/settlement, pār/look, koḷ/vessel) and DEITY_TITLE (vēl, nal, nēr) clusters represent administrative and devotional registers operating under the same grammar.”
   - **(b) Defect:** “Represent” is too strong. The paper provides proposed readings and cluster labels, but no independent test that these are administrative or devotional registers.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Rephrase as “are interpreted by this model as…” or supply independent contextual/archaeological validation.

19. **§3.14 — Rakhigarhi divergence is overstated despite small sample and missing CIs**
   - **(a) Quote + section:** §3.14: “Key findings: Rakhigarhi (n=33) is distinctively divergent from every other major site A bootstrap confidence interval was computed for the most divergent pair: Mohenjo-daro vs Rakhigarhi KL=0.509, 95% CI [0.483, 0.750].”
   - **(b) Defect:** Only the most divergent pair has a CI. The section itself says “no confidence intervals for those pairs are on record” for other Rakhigarhi comparisons and warns that “Rakhigarhi has only 33 seals.” The claim “from every other major site” is stronger than the recorded uncertainty supports.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Report only the measured KL values and the one CI; do not claim site-wide distinctiveness until all pairwise CIs and small-sample controls are provided.

20. **§3.14 — low Mohenjo-daro/Harappa KL does not establish shared scribal tradition**
   - **(a) Quote + section:** §3.14: “The large-site pair (Mohenjo-daro vs Harappa) shows KL=0.070, consistent with a shared scribal tradition.”
   - **(b) Defect:** A low repertoire divergence is compatible with shared tradition, but also with corpus composition, object-type selection, sign normalization, or broad cultural uniformity. No rival explanation is tested.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Rephrase as “compatible with,” and provide controls for object types and sign-list coding before invoking scribal tradition.

21. **§3.15 — PARTIALLY_SUPPORTED label is too generous for Shu-ilishu**
   - **(a) Quote + section:** §3.15: “Result: PARTIALLY_SUPPORTED as an inventory check only.”
   - **(b) Defect:** The test covers only 2/4 slots, finds “No seal in the corpus matched three or more of the four slots,” and admits “The critical gap is coverage of /su/ and /shu/.” This is at most “inventory incomplete / no external match.” “PARTIALLY_SUPPORTED” invites the impression that the Shu-ilishu anchor supports the decipherment; it does not.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Use “NO_MATCH; partial inventory overlap only.”

22. **§3.21 — V12 claim directly contradicts §3.17**
   - **(a) Quote + section:** §3.21: “The vowel harmony issue (V12 warning) is absent from Mahadevan’s analysis, consistent with our Phase-154 finding that V12 is a methodology artifact of applying modern Tamil harmony rules cross-morpheme in agglutinative sequences.”
   - **(b) Defect:** §3.17 says the opposite: “The V12 vowel-harmony warning is unresolved,” “our own records disagree about it,” “we therefore withdraw the earlier description of V12 as a settled methodology artifact,” and “vowel harmony is an open problem for the reading set.” §3.21 preserves the withdrawn stronger claim.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Delete or rewrite §3.21 sentence to match §3.17: V12 is unresolved and cannot be used as a passed methodology artifact.

23. **§3.22 — “cross-validation” label is admitted not to be cross-validation**
   - **(a) Quote + section:** §3.22 heading and sentence: “Parpola 1994 Reading Cross-Validation (Phase-159)” and “Mining Parpola (1994) Deciphering the Indus Script (1,566,507 chars): 44/75 HIGH-confidence readings appear in Parpola’s text (59%).”
   - **(b) Defect:** The section itself says: “This is not independent cross-validation,” because “Parpola’s framework guided the choice of readings,” and the count is “appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.” The heading and “Cross-validation” label overstate the evidence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Rename to “Parpola-tradition overlap count” and remove it from validation/cross-validation claims.

24. **§3.23 — “independent decades” is false framing**
   - **(a) Quote + section:** §3.23: “Across four independent decades of scholarship, the same three-slot positional grammar structure emerges consistently.”
   - **(b) Defect:** The same paragraph says these are “one scholar’s works across four decades, not independent witnesses,” and that “consistent with” only means program mining found compatible terminology. “Independent decades” is rhetorical inflation; decades are not independent evidentiary witnesses.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Replace with “Across several Mahadevan works, program text-mining found terminology compatible with the model.”

25. **§3.24 — literature-mining null is overstated as frontier evidence**
   - **(a) Quote + section:** §3.24: “It is consistent with that view, at the strength a single unbenchmarked search can support.”
   - **(b) Defect:** The sentence is hedged, but the surrounding paragraph says “No new direct M-number reading assignments for the LOW set were found” and then immediately: “The large majority of LOW signs carry placeholder readings with no proposed phonetic value in any available reference literature.” Since the pipeline’s recall “has never been measured,” the paper cannot claim “any available reference literature.”
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Replace “in any available reference literature” with “in this unbenchmarked mining run.”

26. **§3.24 — personal-name ceiling is asserted from an unbenchmarked null**
   - **(a) Quote + section:** §3.24: “The 18 signs in Appendix B resisting MEDIUM promotion (after M198 was promoted to PROVISIONAL_MEDIUM in Phase-166) are personal-name syllable candidates — irresolvable without a bilingual text or a corpus large enough to identify repeated name sequences.”
   - **(b) Defect:** §3.9 explicitly says medial-only signs could be personal-name syllables or “any medial-only sign class,” and “the statistics alone do not distinguish the two.” “Irresolvable” is too absolute; the paper has not exhausted non-bilingual methods.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Rephrase as “may be personal-name syllable candidates; current methods did not resolve them.”

27. **§3.27 — SUPPORTED_WITHIN_MODEL labels are too strong for tiny-token, proximity-derived upgrades**
   - **(a) Quote + section:** §3.27: “M330=can SUPPORTED_WITHIN_MODEL (DEDR 2322, *can- ‘to do; matter, affair’; INITIAL position; 3 corpus tokens; 4 Parpola references); M165=cul SUPPORTED_WITHIN_MODEL (DEDR 2700, *cul- ‘whirl, depth’; MEDIAL position; 2 corpus tokens; 4 Parpola references); M202=can SUPPORTED_WITHIN_MODEL (DEDR 2322; MEDIAL position; 4 corpus tokens; 4 Mahadevan references); M198=co PROVISIONAL_MEDIUM (DEDR 2816, *co- ‘to say, speech’; INITIAL position; 6 corpus tokens; 3 references — it met the >=3 promotion threshold of Phase-163 but not the >=4 threshold Phase-166 uses for a ‘strong’ reference count, which is why it stays provisional while the other three do not).”
   - **(b) Defect:** The references are inherited from §3.25 text proximity, explicitly “not a verified assignment of that reading to that sign.” The token counts are 2–6. The difference between 3 and 4 OCR proximity hits is not a demonstrated evidentiary boundary. “SUPPORTED_WITHIN_MODEL” is too strong.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Require hand-verified source assignments, preregistered thresholds, and independent corpus evidence before using “supported.”

28. **§3.27 — DEDR and phonotactic validity do not validate sign assignment**
   - **(a) Quote + section:** §3.27: “All four upgrades have DEDR backing and Proto-Dravidian phonotactic validity (c-initial is a valid Proto-Dravidian consonant onset; Krishnamurti 2003).”
   - **(b) Defect:** DEDR backing and legal phonotactics only show the proposed reading is linguistically possible. They do not show that the Indus sign has that value.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Distinguish “linguistically admissible” from “supported sign reading.”

29. **§3.30 — “Gulf seal fish-sign corroboration” contradicts §3.19**
   - **(a) Quote + section:** §3.30: “New items added: Gulf seal fish-sign corroboration (E06) …”
   - **(b) Defect:** §3.19 says the Gulf material “does not independently confirm” the pattern. Calling it “corroboration” in the master scorecard inflates a non-counterexample into positive evidence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Rename E06 to “Gulf text-search found no counterexample; image-level confirmation absent.”

30. **§3.30 — literature null rated HIGHLY_SUPPORTED despite unbenchmarked recall**
   - **(a) Quote + section:** §3.30: “New items added: … literature extraction ceiling (S09, HIGHLY_SUPPORTED — meaningful null) …”
   - **(b) Defect:** §3.24 says the search method’s “recall has never been measured against a hand-checked list of known proposals.” An unbenchmarked text-mining null cannot be “HIGHLY_SUPPORTED” as a meaningful ceiling.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Downgrade to “unbenchmarked null from this pipeline.”

31. **§3.30 — scorecard “strongly/highly supported” labels are internal and mixed with non-world evidence**
   - **(a) Quote + section:** §3.30: “Results: 32 total evidence items (up from 23 at Phase-141), 18 of them rated STRONGLY_SUPPORTED_WITHIN_MODEL or HIGHLY_SUPPORTED.”
   - **(b) Defect:** The same paragraph admits these labels are “assigned by this program,” mix “internal consistency checks” with “external comparisons,” and “only the second kind is evidence about the world.” The headline number invites evidential aggregation despite explicit non-comparability.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Separate internal consistency counts from external validation counts; do not aggregate them under support labels.

32. **§4.5 — Gulf validation path “complete” contradicts §3.19**
   - **(a) Quote + section:** §4.5: “Wells catalog Gulf-deposit seals (Phase-156, now complete): Laursen (2010) Gulf Type seal catalog and Mitchell (1986) Ur seals chapter were mined.”
   - **(b) Defect:** “Now complete” is too strong. §3.19 says the Gulf extension was a text search, found “no fish-sign mentions at all in the Laursen text,” and is “weaker evidence than inspection of the seal images.”
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Say “text-mining stage complete; image-level validation incomplete.”

33. **§4.5 — COMPOUND_ONLY_EXTENDED verdict is unsupported**
   - **(a) Quote + section:** §4.5: “No isolated fish signs found in Gulf context. Verdict: COMPOUND_ONLY_EXTENDED — fish sign is compound-only across both mainland and Gulf corpora.”
   - **(b) Defect:** §3.19 says the Gulf material “provides no counterexample … but it does not independently confirm it,” and that the combined 0/140 uses different units: “seals and catalog contexts.” The verdict converts absence of reported isolated fish signs in catalog prose into a confirmed Gulf corpus pattern.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Withdraw COMPOUND_ONLY_EXTENDED. Use “Holdat compound-only; Gulf catalog prose contains no reported counterexample.”

34. **§4.5 — radiocarbon scenario would not by itself support guild semantics**
   - **(a) Quote + section:** §4.5: “Radiocarbon-dated stratigraphic contexts: If seals from the same stratigraphic layer show consistent ‘guild’ readings, this supports the guild-identity interpretation over the commodity-tally model.”
   - **(b) Defect:** This validation criterion is circular unless “guild readings” are independently established. Repeated model-derived translations in a layer would show model consistency, not necessarily guild identity over commodity tally.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Define independent archaeological predictions distinguishing guild identity from commodity tally before treating stratigraphic repetition as support.

35. **§5 — “Tier 2 claims supported by multiple converging tests” overstates a mixed/failed test record**
   - **(a) Quote + section:** §5: “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage) are Tier 2 claims supported by multiple converging tests but not yet externally reviewed.”
   - **(b) Defect:** Several alleged supports are explicitly weak, circular, failed, or inconclusive: SA held-out agreement is 0.000 (§2.4); phonological exclusivity is INCONCLUSIVE (§3.11); polysemy permutation is INCONCLUSIVE (§3.13); Parpola overlap is not independent cross-validation (§3.22); V12 is unresolved (§3.17); the Gulf extension does not independently confirm (§3.19). “Multiple converging tests” is not an accurate summary for the readings.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** List which tests actually support readings independently, exclude failed/inconclusive/circular tests, and recalculate the supported subset.

36. **§5 — Proto-Dravidian “favours” conclusion exceeds admitted baseline comparisons**
   - **(a) Quote + section:** §5: “The corpus shows structure consistent with a decipherable linguistic system; the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”
   - **(b) Defect:** §4.4 says “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary,” and existing comparisons are “mixed”: Dravidian over Sanskrit in one syllabic LM test, but HIGH-anchor phonological profiles found Dravidian and Sanskrit “equal” and “AMBIGUOUS.” §2.1.1 says frequency fits are UNINFORMATIVE. The evidence may be compatible with Proto-Dravidian, but “favours” is stronger than the admitted discriminative testing.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Replace “favours” with “is compatible with” until preregistered rival-model comparisons are run.

37. **Appendix C — internal suite items labeled “supported” are not external validation**
   - **(a) Quote + section:** Appendix C: “Items from the May 2026 suite include: - Dravidian Tier 1 lift ratio: 3.13x above null (Phase-44) - Contact zone HIGH anchors: supported within internal checks (Phase-46) - Sign coverage: 397 M-numbers all addressed - Dashboard coverage metrics: guaranteed <=1.0 (no inflation) - Grammar model: [CLASSIFIER]–[TITLE]–[SUFFIX] pattern supported - Fish sign isolation: 0/140 isolated (0/113 corpus + 0/27 Gulf; Phases 124/127/156) - Sign accounting: 390 attested corpus signs; 397 Mahadevan catalogue signs; 7 catalogue-only signs with zero corpus tokens”
   - **(b) Defect:** The appendix itself says these are “internal consistency checks, not external validation.” Yet items such as “Grammar model … supported” and “Fish sign isolation: 0/140” are worded like external evidentiary successes. The 0/140 figure also inherits the Gulf-unit problem from §3.19.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Separate software/accounting checks from empirical validation checks, and report the fish result as 0/113 Holdat seals plus non-confirmatory Gulf catalog contexts.

---

## Verified trigger-language checks that pass, with caveat where needed

1. **§1.1:** “Individual rebus readings remain contested; none is treated as established in this paper.”  
   - This is appropriately cautious and matches the lack of bilingual text.

2. **§1.2:** “Rao et al. … reported … ‘increase the probability that the script represents language’ — a probability increase, not a demonstration.”  
   - Correctly avoids overstating entropy evidence.

3. **§2.1:** “we no longer present it as evidence that the script is a language.”  
   - Correctly withdraws the earlier Zipf-based inference.

4. **§2.1.1:** “Under the rule fixed before the run, that result makes the comparison UNINFORMATIVE…”  
   - The verdict matches the described result: Linear B, the known writing system, fit worst.

5. **§2.1.1:** “it is not a general proof that frequency curves can never carry information.”  
   - Properly limited.

6. **§2.2:** “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities…”  
   - Accurate and important; the problem is that later headline wording does not consistently preserve this caveat.

7. **§2.4:** “On that record, SA agreement by itself carries no information about a sign’s value.”  
   - This is an appropriate verdict given the reported held-out failure.

8. **§3.4:** “Its distribution across seal motifs does not differ significantly from uniform (chi-square = 12.98, p = 0.1124, Phase-132)…”  
   - The “not significant” claim matches p = 0.1124.

9. **§3.4:** “This correction is methodologically important: it demonstrates the risk of reading frequency alone as a phonetic indicator.”  
   - Fairly supported by the M267 correction.

10. **§3.5:** “That rules out a purely local, single-site habit; it does not by itself prove a scribal rule…”  
   - Properly bounded: 0 isolated fish signs across sites supports non-locality, not a universal scribal rule.

11. **§3.11:** “The test’s recorded verdict is INCONCLUSIVE…”  
   - Correctly matches the described null result and circular DEDR-source selection.

12. **§3.11:** “This test does not establish Dravidian exclusivity.”  
   - Correct and important.

13. **§3.13:** “The test’s recorded verdict is INCONCLUSIVE…”  
   - Correctly matches observed rate below null mean.

14. **§3.13:** “it neither supports nor refutes the grammar model.”  
   - Correctly limited.

15. **§3.17:** “The V12 vowel-harmony warning is unresolved…”  
   - Correctly reflects conflicting internal records.

16. **§3.18:** “it cannot validate the readings”  
   - Correctly limits the Tamil-Brahmi comparison.

17. **§3.19:** “the Gulf material provides no counterexample to the compound-only pattern, but it does not independently confirm it.”  
   - This is the correct evidentiary strength; the problem is that other sections ignore it.

18. **§3.28:** “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164.”  
   - The verdict matches the described fuzzy-matching failure.

19. **§3.29:** “These 19 signs remain at LOW confidence — phonotactic plausibility is a necessary but not sufficient condition for MEDIUM promotion.”  
   - Correctly prevents plausibility from becoming evidence of reading validity.

20. **§3.31:** “This is a self-consistency check, not an accuracy measurement…”  
   - Correctly characterizes the 93.2% result.

21. **§4.1:** “the two readings have not been separated by any test yet…”  
   - Correct caveat for guild vs commodity interpretation.

22. **§4.4:** “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary…”  
   - Correctly identifies the missing discriminative test.

---CALL-META finish_reason=stop usage={"prompt_tokens": 19526, "completion_tokens": 11229, "total_tokens": 30755, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 2925, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=33933---


## PASS 3 — DEEP SUBSTANTIVE / NEW-CONTENT AUDIT

## Numbered findings

1. **Non-public primary corpus makes the central claims non-reproducible**
   - **(a) Quote + section:** Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” §6: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”
   - **(b) Defect:** The paper repeatedly presents exact corpus-level results — “7,002 sign tokens,” “90.96% token coverage,” “0/113,” “z = 10.3,” “R² = 0.992,” “2,647 distinct bigrams” — while admitting the underlying corpus cannot be inspected or re-run. This is not a reproducible computational decipherment in the ordinary scholarly sense. A repository of derived files does not solve this if the primary tokenization and inscription inventory are inaccessible.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Release the corpus or a legally shareable inscription-level table with sign sequences, site, object type, motif coding, sign-code crosswalks, and all exclusions. Otherwise all corpus-level claims must be downgraded to author-reported, non-replicable measurements.

2. **The SA method is admitted to have failed a held-out test, yet SA-supported readings still enter MEDIUM coverage**
   - **(a) Quote + section:** §2.2: “MEDIUM (86 signs): Single strong evidence source: - DEDR rebus match with SA-consistency >= 0.15 from syllabic language model simulation.” §2.4: “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.” §2.4: “Phase-107… agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it.”
   - **(b) Defect:** This is internally devastating. A criterion is called a “Single strong evidence source” while the paper itself says the threshold is uncalibrated, the false-positive rate is unknown, and the method performed indistinguishably from Sanskrit and scrambled controls with “0.000” agreement. Any MEDIUM reading promoted only through SA+DEDR is not meaningfully supported.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Remove SA-supported promotions from H+M unless independently supported by non-SA evidence. Publish a known-script calibration showing error rates for the 0.15 threshold, with held-out recovery of signs under comparable inscription lengths and sign inventories.

3. **Coverage headline is inflated by including unvalidated SA-derived and text-proximity-derived candidates**
   - **(a) Quote + section:** Abstract: “propose 161 candidate readings at HIGH or MEDIUM confidence… account for 90.96% of the corpus’s sign tokens.” §2.4: “SA agreement by itself carries no information about a sign’s value.” §3.25: “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign.” §3.1: “PROVISIONAL_MEDIUM… included for coverage accounting.”
   - **(b) Defect:** The headline “90.96%” coverage pools solid-looking anchors with readings whose support is explicitly non-probative or unverified. The caveat “coverage means only that the model assigns a candidate reading” helps, but the abstract and conclusion still use coverage as a major achievement. Coverage by arbitrary or weak assignments is not decipherment evidence.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Recompute coverage under evidence tiers excluding SA-only, text-proximity-only, and provisional readings. Provide a table: iconographic-only, distributional-only, DEDR-only, SA-involved, literature-proximity, and combinations.

4. **The confidence hierarchy admits dependence among criteria, undermining “multiple converging tests”**
   - **(a) Quote + section:** §2.2: “The criteria are separate tests, but they are not independent of each other: all except the DEDR and Parpola criteria are computed from the same corpus, and several from the same seals.” Conclusion: “The candidate Proto-Dravidian readings… are Tier 2 claims supported by multiple converging tests.”
   - **(b) Defect:** The paper admits the tests are not independent, then later relies on “multiple converging tests” rhetoric. Reusing the same corpus, same seals, same positional profiles, and often the same iconographic assumptions does not generate independent convergence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Build an explicit dependency graph for every evidence item per sign. Report support after collapsing non-independent evidence families. Use genuinely external validation: unseen corpus, blind expert icon coding, or independently coded sign readings.

5. **The rebus/DEDR matching framework has uncontrolled degrees of freedom**
   - **(a) Quote + section:** Abstract: “DEDR rebus matching.” §2.2: “Iconographic match: the sign’s shape is identified… as depicting a known object whose Dravidian name yields the reading by the rebus principle.” §3.3 examples include “M211 kol,” “M099=kol/koḷ,” “M261=muruku,” “M264=peN,” “M391=ka/kaṇ.”
   - **(b) Defect:** No search space is defined. The paper does not specify how many DEDR entries were searched, how semantic latitude was controlled, what phonological distance was allowed, whether homophones/allomorphs were pre-registered, or how many alternative readings were rejected. Rebus decipherment without a controlled null is a multiple-comparison engine.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Publish the full candidate-generation procedure: all DEDR entries searched, allowed phonological transformations, semantic categories, rejected alternatives, and a false-discovery estimate from shuffled icon labels or non-Dravidian lexica.

6. **Iconographic validation is circular for signs whose readings were chosen from the same motif**
   - **(a) Quote + section:** §3.8: “for signs whose reading was itself suggested by the animal motif, ‘the reading matches the animal’ is circular and is not claimed here as validation.” §3.3: “M045 yānai… Elephant icon, Tamil yānai”; “M062 erutu… Exclusive to zebu bull”; “M073 kōṉ… Exclusive to zebu bull.”
   - **(b) Defect:** The paper correctly admits circularity, but the same signs remain “HIGH confidence” and are used in the model’s semantic apparatus. Icon shape → animal word → reading → animal/classifier semantics is not independent evidence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Separate “iconographic label” from “phonetic reading.” A reading should not become HIGH unless it predicts non-iconographic facts on held-out inscriptions or external corpora.

7. **HIGH confidence is assigned to readings lacking DEDR support or paradigm proof**
   - **(a) Quote + section:** §3.3: “M342 ay/ā DEDR — Candidate case suffix: 584 tokens, 96% of them inscription-final; the case-suffix label is an interpretation of that distribution, not a demonstrated paradigm.” §3.3: “M176 an/aṇ… Candidate masculine suffix: 356 tokens, 94% of them inscription-final; the gender label is likewise an interpretation of distribution.”
   - **(b) Defect:** These are listed under “HIGH confidence,” but the paper says their grammatical labels are interpretations, not demonstrated paradigms. M342 has no DEDR citation in the table. Terminal position alone cannot identify genitive, masculine, or case.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Downgrade these to positional-function candidates unless paradigmatic alternations, syntactic substitution, or external bilingual evidence supports the specific suffix values.

8. **M060 “rhinoceros” reading lacks DEDR support and is admitted to be descriptive**
   - **(a) Quote + section:** §3.2: “M060=kāṇṭāmirukam (a descriptive compound gloss, ‘rhinoceros’; no DEDR entry is recorded for this sign — its support is iconographic and distributional only, 20 tokens).”
   - **(b) Defect:** A descriptive modern-looking gloss with no DEDR entry cannot function as a Proto-Dravidian phonetic anchor. Iconographic identification is not decipherment.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Remove it as a phonetic reading unless a documented Proto-Dravidian lexical form and rebus pathway are supplied, with alternatives considered.

9. **M261 is internally unstable: HIGH table versus withdrawn semantic gloss and only two tokens**
   - **(a) Quote + section:** §3.2: “M261=muruku (young man; 2 tokens only, from Parpola 1994 via this program’s Phase-51 — the further gloss ‘deity Murugan / guild-of-Murugan’ is not supported by anything in our records and is withdrawn).” §3.3: “M261 muruku 4988 Wheel/spindle, Tamil Murugan.”
   - **(b) Defect:** One section withdraws the Murugan/deity/guild gloss as unsupported; the next table lists “Tamil Murugan” as the basis for a HIGH-confidence reading. Two corpus tokens cannot bear this weight.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Reconcile the basis. If “Murugan” is withdrawn, remove it from the HIGH table. If “muruku” remains, provide the actual sign-specific evidence independent of the withdrawn gloss.

10. **The three-slot grammar is fit and interpreted on the same data used to define positional classes**
   - **(a) Quote + section:** §2.3: “INITIAL-dominant signs are classified as title prefixes or classifier-derived words. TERMINAL-dominant signs are classified as case suffixes or proper-name terminals. MEDIAL signs are classified as content words or personal name syllables.” §3.2: “Positional statistics establish the three positions and which signs favour each. The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics.”
   - **(b) Defect:** Positional clustering can show order structure, but the semantic labels “classifier,” “guild title,” “personal-name ending,” and “case marker” are imposed. The grammar is not shown to distinguish language from administrative marks, owner marks, clan marks, commodity labels, or emblem formulas.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Test rival templates explicitly, as the paper itself says was not done. Use model comparison against owner-mark, commodity-mark, clan-emblem, and non-linguistic administrative-symbol baselines.

11. **The headline positional z-score lacks enough methodological detail to audit**
   - **(a) Quote + section:** §2.3: “We fit the three-slot grammar model to the real corpus (coefficient of determination R² = 0.992) and to 2,000 copies of the corpus in which the signs inside each inscription were shuffled… z = 10.3.”
   - **(b) Defect:** The paper does not define the dependent variable for R², the exact fitted model, whether parameters/classes were re-estimated for each shuffle, or whether the statistic was selected after exploration. Shuffling signs within inscriptions may preserve sign frequencies and lengths but destroys any sequential formula; it is an easy null, not a serious rival model.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Publish the exact statistic, code, and permutation protocol. Include stronger nulls: Markov-preserving shuffles, motif-conditioned shuffles, site-conditioned shuffles, and rival-template simulations.

12. **The paper overstates positional grammar despite its own failed collocate permutation test**
   - **(a) Quote + section:** §3.7: “17/21 tested H+M signs show position-specific collocate profiles.” §3.13: “Observed collocate divergence rate: 66.7%… Null distribution mean: 80.7%… one-tailed permutation p = 0.955.” §3.13: “the real corpus does not show more position-specific collocate divergence than shuffled corpora.”
   - **(b) Defect:** The descriptive finding is weaker than chance under the paper’s own null. The paper says it does not use this as support, but the surrounding formula-structure discussion still contributes to the appearance of grammatical confirmation.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Remove Phase-142D from evidential summaries or mark it as failed/inconclusive wherever formula structure is summarized.

13. **Phase-170 grammar retest is admitted tautological but still appears in the program’s result list**
   - **(a) Quote + section:** §1.3 item 18: “Grammar self-consistency retest… 93.2%.” §3.31: “This is a self-consistency check, not an accuracy measurement… a high figure is expected by construction.”
   - **(b) Defect:** A by-construction self-consistency score should not be presented alongside substantive results. It can only detect coding contradictions.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Move it to a software QA appendix and exclude it from evidence synthesis.

14. **M267 correction is useful, but the replacement “genitive particle” is not established**
   - **(a) Quote + section:** §3.4: “Its current MEDIUM reading is iN/in (genitive particle).” §3.4: “Its distribution across seal motifs does not differ significantly from uniform… which is why a motif-bound reading such as ‘fish’ fails and a grammatical-particle reading is preferred.”
   - **(b) Defect:** Showing that M267 is not motif-bound fish does not identify it as a genitive particle. “Not fish” does not imply “genitive.” The inference jumps from distributional breadth and position to a specific grammatical function.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Treat M267 as an unidentified high-frequency functional sign unless paradigmatic alternation or syntactic distribution supports genitive specifically.

15. **The M267 chi-square null is suspect as stated**
   - **(a) Quote + section:** §3.4: “Its distribution across seal motifs does not differ significantly from uniform (chi-square = 12.98, p = 0.1124, Phase-132).”
   - **(b) Defect:** “Uniform” across motif types is not necessarily the right expected distribution. If motifs are unevenly frequent in the corpus, the proper null is proportional to motif base rates, not equal counts per motif. The text gives observed motif counts for M267 but not corpus motif totals.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Re-run using expected counts from the corpus-wide motif distribution, with site/object controls.

16. **Fish-sign isolation test has a weak target and does not discriminate the claimed functions**
   - **(a) Quote + section:** §3.5: “A fish sign counts as ‘isolated’ if it is the only sign in its inscription.” §3.5: “This result is compatible with a range of interpretations of the fish sign’s function; the present study does not adjudicate between them.”
   - **(b) Defect:** Absence of one-sign fish inscriptions only rules out a narrow behavior. It does not establish “guild/title,” “maritime marker,” “scribal rule,” or linguistic status. The paper admits compatibility with many interpretations, yet the abstract presents “0/140” as a systematic test result.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Define competing predictions quantitatively: fish as commodity, numeral, deity, title, star, clan emblem, or phonetic sign. Test frequencies, positions, co-occurrences, site/object associations, and comparison signs under all models.

17. **Fish test site-invariance is overstated with tiny and aggregated site counts**
   - **(a) Quote + section:** Abstract: “0/113 across 9 corpus sites.” §3.5 table: “Lothal… 6”; “All others… 28”; “Total… 113.” §3.5: “site-invariant.”
   - **(b) Defect:** Lothal has only 6 fish-bearing seals. Several sites are collapsed into “All others.” No confidence intervals or power analysis are provided. “Site-invariant” is stronger than the data support.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Provide per-site counts for all nine sites, exact denominators, and binomial uncertainty. Avoid “site-invariant” unless the test has power to detect site differences.

18. **The Gulf fish-sign extension is too weak for the combined 0/140 headline**
   - **(a) Quote + section:** §3.19: “That text search found no mention of an isolated fish sign — and… no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits).” §3.19: “An absence in catalogue prose is weaker evidence than inspection of the seal images.” §3.19: “the two parts count different units (seals and catalog contexts) and should be cited separately.” Abstract: “for a combined result of 0/140.”
   - **(b) Defect:** The abstract combines unlike units despite §3.19 warning they “should be cited separately.” The Gulf component is not image inspection and found no fish-sign mentions at all, making it weak absence-of-prose evidence.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Remove “combined 0/140” from the abstract. Report “0/113 Holdat fish-bearing seals” separately from “0/27 Gulf catalog contexts reported as isolated,” and only after image-based verification.

19. **§4.5 falsely upgrades the Gulf fish result beyond the paper’s own caveat**
   - **(a) Quote + section:** §4.5: “Verdict: COMPOUND_ONLY_EXTENDED — fish sign is compound-only across both mainland and Gulf corpora.” §3.19: “the Gulf material provides no counterexample… but it does not independently confirm it.” §3.19: “the corpus result therefore stands on the Holdat count alone.”
   - **(b) Defect:** Direct contradiction. §3.19 says the Gulf evidence does not independently confirm the pattern; §4.5 says the validation path is complete and the pattern is extended across both corpora.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Revise §4.5 to match §3.19: Gulf extension is incomplete/weak unless seal images are inspected and coded.

20. **Power-law/exponent material is correctly caveated but exposes prior evidential instability**
   - **(a) Quote + section:** §2.1: “An earlier version… reported a Zipf exponent of about 1.7… we no longer present it as evidence.” §2.1.1: “The four exponents mentioned… must not be compared with each other.” §2.1.1 table: “about 1.7,” “about 1.35,” “2.004,” “2.59.”
   - **(b) Defect:** The current caveat is appropriate, but it reveals that earlier versions used unstable and non-comparable exponent claims. The comparison set also produces the bizarre result that “Linear B… fitted the curve worst,” which properly makes the test uninformative. Any remaining use of Zipf-like facts elsewhere must be treated as non-evidence.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Keep all frequency-curve claims out of arguments for linguistic status. Archive exact fitting rules and data for each exponent.

21. **Linear B comparison in §2.1.1 is tokenization-confounded by the paper’s own description**
   - **(a) Quote + section:** §2.1.1: “Linear B… counted as its 89 syllabogram types in the DAMOS transliterations, 47,292 tokens.” §2.1.1: “The comparison systems were Mesopotamian numerical signs… heraldic charges… a synthetic emblem process… and Linear B.”
   - **(b) Defect:** The compared systems are not commensurate symbol inventories: syllabograms, numerical signs, heraldic charges, synthetic emblems, and Indus signs. The paper’s conclusion “UNINFORMATIVE” is justified, but the test cannot support anything broader.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** If frequency curves are revisited, compare matched semiotic units and matched corpus genres, with known writing and non-writing controls.

22. **Substrate-promotion method contradicts the actual substrate evidence**
   - **(a) Quote + section:** §2.5: “Signs with substrate matches and near-Dravidian cognates are promoted to MEDIUM with substrate notation.” §3.3: “no Munda source for it is cited in our records”; “no regular sound correspondence or borrowing pathway has been shown, so the Munda derivation is unestablished.”
   - **(b) Defect:** The method says substrate matches can promote signs; the results say the two substrate cases lack necessary sourcing or sound correspondence. These should not be MEDIUM on substrate grounds.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Remove substrate status from M374 and M351 unless primary Munda sources, regular correspondences, and borrowing pathways are documented.

23. **The “Munda substrate” discussion overinterprets two weak signs**
   - **(a) Quote + section:** §4.2: “Two signs (M374=kul, M351=vī, six tokens each) are assigned candidate Munda substrate readings.” §4.2: “Two candidate signs cannot establish that scenario.”
   - **(b) Defect:** The paper mostly caveats this correctly, but still keeps “substrate evidence” as a named discussion section and method component. With six tokens each and admitted unestablished derivations, this is not evidence of substrate.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Reclassify as unsupported speculation; remove from MEDIUM evidence accounting.

24. **Tamil-Brahmi terminal comparison is post hoc, temporally remote, and not discriminative**
   - **(a) Quote + section:** §3.18: “Tamil-Brahmi is roughly two thousand years later than the Indus material.” §3.18: “A second, broader count was made after seeing this result… it is post hoc.” §3.18: “the 4/7 result above is the recorded primary result.”
   - **(b) Defect:** Even the primary 4/7 result has no null model or base rate. The broader 8/11 is admitted post hoc and incompletely recorded. Later Tamil-Brahmi endings cannot validate Bronze Age Indus readings.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Drop as validation. If retained, pre-register categories, use blinded matching, and compare against non-Dravidian terminal inventories and randomized reading sets.

25. **Phonological exclusivity test is self-contaminated by DEDR selection**
   - **(a) Quote + section:** §3.11: “the readings tested were themselves chosen from Dravidian sources (DEDR), so an absence of Sanskrit-only sounds in them is partly built into how they were selected.” §3.11: “This test does not establish Dravidian exclusivity.”
   - **(b) Defect:** Correctly disclosed. This test cannot discriminate Dravidian from Sanskrit or other baselines because the input readings were selected from Dravidian sources.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Use independently generated candidate readings from competing lexica under identical rules, then compare predictive success on held-out sign sequences.

26. **Vowel-harmony sections directly contradict each other**
   - **(a) Quote + section:** §3.17: “The V12 vowel-harmony warning is unresolved… recorded verdict is V12_ACTIVE_CONCERN… vowel harmony is an open problem for the reading set.” §3.21: “consistent with our Phase-154 finding that V12 is a methodology artifact.”
   - **(b) Defect:** §3.17 explicitly withdraws the claim that V12 is a settled methodology artifact. §3.21 then repeats exactly that withdrawn interpretation. This is a direct internal contradiction.
   - **(c) Severity:** **CRITICAL**
   - **(d) Settlement:** Rewrite §3.21 to match §3.17. If V12 remains active, report which high-frequency readings cause violations and how many H+M signs are affected.

27. **V07 phonotactic violations are severe and concentrated in high-frequency signs**
   - **(a) Quote + section:** §3.18: “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”
   - **(b) Defect:** A violation rate of nearly one quarter of decoded seals, concentrated in high-frequency signs, is a major threat to the reading set. The paper reports it but does not propagate its impact into confidence labels.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Identify affected signs/readings, downgrade readings that drive violations, and rerun coverage and grammar examples after correction.

28. **Formula semantic clustering is circular because domains derive from the proposed readings**
   - **(a) Quote + section:** §3.12: “Grouping the 97 INITIAL-sign clusters… by semantic domain of their reading.” §3.12: “ANIMAL_GUILD… accounts for 26.7% of seals — consistent with a totem-based guild identity system.”
   - **(b) Defect:** The semantic domains are not independently observed; they are assigned from the model’s own readings. Then the domains are used to support the model’s guild interpretation. This is circular.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Have external coders assign iconographic and semantic classes blind to the proposed readings, or test whether the proposed domains predict independent archaeological metadata.

29. **Individual seal translations are unsupported composites of uncertain readings**
   - **(a) Quote + section:** §4.1: “M211 M099 M342 = kol-kol-ay = ‘the jar-guild lord’”; “M062 M342 M176 = erutu-ay-an = ‘the bull’s man’”; “M045 M176 M267 M328 = yānai-an-iN-āl = ‘the elephant guild man’s man’.” §4.1: “the two readings have not been separated by any test yet.”
   - **(b) Defect:** These translations depend on multiple candidate readings, grammatical labels, and rebus choices. The paper admits rival functions are not ruled out. The examples create an illusion of decipherment not justified by the evidence.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Present only morpheme-by-morpheme candidate parses with confidence per sign; do not translate as English phrases until external validation exists.

30. **The model allows homophonous reuse without demonstrating how ambiguity is controlled**
   - **(a) Quote + section:** §4.1: “the first, for example, depends on two different signs (M211 and M099) both being read kol.” §3.2: “M211=kol”; “M099=kol/koḷ.”
   - **(b) Defect:** Two different signs receiving the same or near-same value may be possible in real writing systems, but the paper gives no rule for when homophony is allowed, how allographs are distinguished, or how semantic rebus values are selected.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Provide a sign-value inventory with homophony/allography criteria, frequency expectations, and tests against known logosyllabic systems.

31. **Site repertoire divergence claim overstates small-sample evidence**
   - **(a) Quote + section:** §3.14: “Rakhigarhi (n=33) is distinctively divergent from every other major site.” §3.14: “no confidence intervals for those pairs are on record.” §3.14: “Rakhigarhi has only 33 seals… not as proof that the difference is not a small-sample effect.”
   - **(b) Defect:** The first sentence overclaims; the later caveats undercut it. Only one confidence interval is given, for the most divergent pair. Multiple comparisons across 36 site pairs are not handled.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Compute intervals for all pairs, correct for multiple comparisons, and use rarefaction or hierarchical modeling for site sample-size effects.

32. **Cross-corpus comparison with CISI shows structural disagreement, not validation**
   - **(a) Quote + section:** §3.10: “The positional-class distributions of the two corpora differ substantially (KL divergence = 0.591; the Phase-145 record itself rates structural agreement LOW — for example, MEDIAL-class share is 68.75% in CISI against 34.8% in Holdat).”
   - **(b) Defect:** This is a serious non-replication of positional-class proportions. The paper reports it, but still treats cross-corpus structure as broadly compatible because “87%… open with an INITIAL-class sign.”
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Explain the divergence with documented corpus differences or downgrade generality of the grammar model until tested on harmonized corpora.

33. **Nair 2026 is independent work but not independent inscription evidence**
   - **(a) Quote + section:** §3.10: “it is independent work, but it is not an independent body of inscriptions.” §1.3: “External scorecard study… on a separate digitization of the same published inscription assemblage.”
   - **(b) Defect:** Correctly disclosed, but any use as “external” evidence must be limited. It does not test this paper’s readings, grammar, or Dravidian hypothesis.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Keep Nair only as evidence for non-random sequential structure under a different digitization, not as validation of decipherment.

34. **Mahadevan “four-decade” claim contradicts its own non-independence disclosure**
   - **(a) Quote + section:** §3.23: “These are one scholar’s works across four decades, not independent witnesses.” §3.23: “Across four independent decades of scholarship, the same three-slot positional grammar structure emerges consistently.”
   - **(b) Defect:** Same section says “not independent witnesses” and then says “independent decades.” Decades are not independent evidence if the same scholar and tradition are being mined.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Replace “independent decades” with “repeatedly in Mahadevan’s work” and remove from independent evidence counts.

35. **Text-mining literature claims are unbenchmarked and partly withdrawn**
   - **(a) Quote + section:** §3.24: “its recall has never been measured against a hand-checked list of known proposals.” §3.22: “Two further counts from the same mining are withdrawn as evidence.” §3.20: “we cite this as our mining summary… not as a quotation.”
   - **(b) Defect:** Literature-mining outputs cannot support strong claims until recall and precision are known. Several earlier mined claims were noise or could not be located.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Benchmark the mining pipeline against a manually curated gold standard of sign-reading proposals.

36. **Sibilant promotions are based on OCR proximity, not verified sign assignments**
   - **(a) Quote + section:** §3.25: “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign.” §3.25: “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits.”
   - **(b) Defect:** Promoting readings based on unverified proximity in OCR’d text is not a valid decipherment criterion. The later DEDR check only shows phonotactic/lexical plausibility, not that the sign has that value.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Require manual verification of each cited passage and sign assignment before any promotion. OCR proximity should generate hypotheses only.

37. **Phase-166 “SUPPORTED_WITHIN_MODEL” is weak because corpus counts are 2–6 tokens**
   - **(a) Quote + section:** §3.27: “M330=can… 3 corpus tokens”; “M165=cul… 2 corpus tokens”; “M202=can… 4 corpus tokens”; “M198=co… 6 corpus tokens.”
   - **(b) Defect:** These token counts are too small for positional or distributional confidence. DEDR compatibility plus valid onset does not identify sign value.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Keep them LOW/provisional until additional attestations or manually verified external proposals support them.

38. **Meluhhan name matching demonstrates base-rate failure**
   - **(a) Quote + section:** §3.28: “all 25 names produced apparent ‘matches’ at this threshold due to the prevalence of common short readings (ā, kol, il). Effective result: NO_DISCRIMINATIVE_MATCH.”
   - **(b) Defect:** The paper correctly identifies the failure mode: common short readings generate false matches. This also warns against other phonological matching claims using short syllables.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Use calibrated match probabilities, name-length controls, randomized reading inventories, and held-out attestations before claiming any personal-name match.

39. **Decode-blocker analysis uses phonotactic plausibility, which has very low evidential value**
   - **(a) Quote + section:** §3.29: “19/19 blocker LOW readings are phonotactically plausible.” §3.29: “it checks plausibility… and nothing more.” §3.29: “These 19 signs remain at LOW confidence.”
   - **(b) Defect:** Correctly caveated, but the result should not be listed as evidence in §1.3 or §3.30 except as a null sanity check. Many arbitrary syllables will be phonotactically valid.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Exclude from evidence synthesis or report expected base rate of phonotactically valid random assignments.

40. **Master evidence synthesis mixes internal checks and external evidence**
   - **(a) Quote + section:** §3.30: “The items mix two different kinds of check — internal consistency checks… and external comparisons… and only the second kind is evidence about the world.” §3.30: “18 of them rated STRONGLY_SUPPORTED_WITHIN_MODEL or HIGHLY_SUPPORTED.”
   - **(b) Defect:** The paper admits the scorecard’s category problem. Counting internally assigned labels risks manufacturing evidential mass from self-consistency.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Split the scorecard into internal QA versus external validation. Do not aggregate them numerically or rhetorically.

41. **Conclusion overstates Dravidian support relative to the stated baseline failure**
   - **(a) Quote + section:** Conclusion: “the evidence favours a Proto-Dravidian reading framework under the tested assumptions.” §4.4: “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” Abstract: “Dravidian superiority over proto-Munda has not been formally quantified.”
   - **(b) Defect:** If formal comparisons against major alternatives remain necessary, “favours” is too strong. The evidence may be compatible with Proto-Dravidian under assumptions, but not discriminative.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Replace “favours” with “is compatible with.” Conduct matched alternative-language analyses with identical candidate-generation rules.

42. **Claimed falsifiability is weakened by flexible fallback explanations**
   - **(a) Quote + section:** §4.5: “The candidate model is falsifiable at three points.” §3.9: “the statistics alone do not distinguish the two.” §4.1: “rival functions… are not ruled out.” §3.5: “selection or object-type effects could produce the same pattern.”
   - **(b) Defect:** The paper lists possible validation paths, but many observed results are insulated by alternative explanations: object-type effects, selection effects, personal-name arbitrariness, rival functions, and corpus limitations. It is unclear what current observation would falsify the model rather than be reclassified as LOW, substrate, personal name, allograph, or corpus effect.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** State explicit falsification thresholds: e.g., how many bilingual mismatches, held-out corpus failures, positional exceptions, or iconographic contradictions would reject each class of readings.

43. **Appendix C internal consistency checks are not external validation but are advertised in abstract/result list**
   - **(a) Quote + section:** Abstract: “Internal consistency checks pass (59/59, Phases 1–170).” Appendix C: “These are internal consistency checks, not external validation, and the suite has since changed: on the October 2026 execution tree it reported 40 passed, 0 failed, 8 warnings.”
   - **(b) Defect:** The abstract uses the stronger 59/59 figure, while Appendix C says the suite changed and now reports a different structure with warnings. This is software QA, not decipherment evidence.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Move to reproducibility appendix; report only current suite status and list warnings.

44. **Reference to “all 397 signs addressed” can mislead because LOW signs are heuristic placeholders**
   - **(a) Quote + section:** §2.1: “the anchor table assigns readings to all 397 signs.” §2.2: “LOW (236 signs): Heuristic assignment only.” §2.2: “Not used for coverage.” §3.24: “The large majority of LOW signs carry placeholder readings with no proposed phonetic value in any available reference literature.”
   - **(b) Defect:** “Assigns readings to all 397 signs” sounds complete, but most catalogue signs are heuristic placeholders. The paper partly corrects this, but the phrasing still risks overstatement.
   - **(c) Severity:** **MINOR**
   - **(d) Settlement:** Say “the table contains entries for all 397 signs; only 161 have H+M candidate readings.”

45. **The paper’s strongest structural result still does not establish language**
   - **(a) Quote + section:** §2.1.1: “these measures do not separate the one certain writing system from systems that are not writing.” §3.2: “rival templates such as owner marks, commodity marks, or clan emblems… could also produce fixed position patterns.” Conclusion: “The corpus shows structure consistent with a decipherable linguistic system.”
   - **(b) Defect:** “Consistent with” is acceptable; anything stronger would not be. Non-random positional structure is compatible with linguistic writing but also with structured non-linguistic administrative notation.
   - **(c) Severity:** **MAJOR**
   - **(d) Settlement:** Add explicit non-linguistic structured-symbol baselines to the positional tests.

---

## Verified checks that pass, narrowly

1. **The paper correctly withdraws Zipf/power-law evidence as linguistic evidence.**  
   §2.1 and §2.1.1 explicitly state the exponent claims are not comparable and “UNINFORMATIVE.”

2. **The paper correctly reports the failed phonological exclusivity test.**  
   §3.11 says the verdict is “INCONCLUSIVE” and admits DEDR selection contaminates the test.

3. **The paper correctly reports the failed/inconclusive polysemy permutation result.**  
   §3.13 gives p = 0.955 and says the descriptive Phase-142D result is not above-chance evidence.

4. **The paper correctly discloses that Parpola overlap is not independent validation.**  
   §3.22: “This is not independent cross-validation.”

5. **The paper correctly discloses that Phase-170 is self-consistency, not accuracy.**  
   §3.31 states the high figure is “expected by construction.”

6. **The paper correctly corrects the M267 fish-sign error.**  
   §3.4 gives an explicit correction: “M267 Is Not the Fish Sign.” The replacement reading remains unproven, but the correction itself is transparent.

7. **The paper correctly states that confidence labels are not calibrated probabilities.**  
   §2.2 and §4.4 both say no measured error rate or numerical probability attaches to the labels.

---CALL-META finish_reason=stop usage={"prompt_tokens": 19557, "completion_tokens": 10647, "total_tokens": 30204, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 1479, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=38561---


## PASS 4 — CHECKABILITY, CITATION & REPRODUCIBILITY AUDIT

## Findings — checkability, citation, reproducibility

1. **Repository is unlocated; branch/commit is useless without a remote.**  
   **(a) Quote + section:** §6: “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 8a9e80cf).”  
   **(b) Defect:** No repository URL, DOI, archive link, organization URL, Git remote, or release artifact is printed. A branch name and commit hash do not let a reader find anything. This invalidates repeated claims that files, scripts, reports, and tables are “available.”  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Print a permanent URL/DOI for the repository or archive, include the exact commit hash, and ensure the named files exist at that commit.

2. **Core corpus is unavailable, so the central quantitative claims cannot be reproduced.**  
   **(a) Quote + section:** Abstract: “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” §6: “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
   **(b) Defect:** The paper’s central claims—7,002 tokens, 1,670 seals, positional z-score, coverage, fish counts, motif distributions, bigrams, KL divergences—depend on an inaccessible corpus. The disclosure is honest, but the paper still repeatedly presents hidden-corpus results as settled corpus-level facts.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Release the corpus or provide a fully auditable substitute: inscription IDs, sign sequences, site/motif metadata, and sign coding sufficient to recompute every count.

3. **Data availability statement names files but gives no access path.**  
   **(a) Quote + section:** §6: “The anchor table is research/indus/anchor_table.csv; sign frequencies and token counts by category are in glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv; per-phase results are in backend/reports/.”  
   **(b) Defect:** File paths inside an unspecified repository are not data availability. The paper depends on these files, but a reader cannot access or verify them from the paper.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Provide an archived repository URL/DOI and include checksums for these files.

4. **Supplemental datasets are unlocated.**  
   **(a) Quote + section:** §6: “Supplemental datasets (fish-sign compound-context listing, iconographic formula enrichment table, formula bigram table, and positional grammar permutation summary) are available in research/indus/supplemental/.”  
   **(b) Defect:** The supplemental directory is not accessible because the repository is not identified. These files are load-bearing for §§3.5, 3.7, 3.8, and the permutation claims.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Archive and link the supplemental files directly, with versioned filenames and checksums.

5. **The anchor table on which the decipherment rests is not printed.**  
   **(a) Quote + section:** §1.3: “A publish-ready anchor table covering all 161 H+M candidate readings with DEDR citations.” §2.2: “The outcome of the criteria for each sign is recorded in the anchor table (research/indus/anchor_table.csv, ‘Basis’ column).”  
   **(b) Defect:** The paper does not print the 161 readings, their criteria, DEDR entries, frequencies, positional profiles, or evidence basis. The reader cannot audit whether signs actually meet the stated HIGH/MEDIUM rules.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Include the full 161-row anchor table in the paper or an accessible archived supplement.

6. **The abstract’s “reproducible” claim is contradicted by the inaccessible corpus and unlocated repository.**  
   **(a) Quote + section:** Abstract: “This study … proposes a reproducible, falsifiable computational model.” Also Abstract: “The corpus itself is not publicly released … so corpus-level counts cannot yet be re-run by other researchers.”  
   **(b) Defect:** The model may be conceptually falsifiable, but it is not presently reproducible for the results reported. The paper cannot both claim reproducibility and admit the corpus-level counts cannot be rerun.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Change the claim to “partially reproducible conditional on corpus access,” or release the corpus and code.

7. **DOI is given, but the cited data/code package is not identified.**  
   **(a) Quote + front matter:** “DOI: 10.5281/ZENODO.20414696.”  
   **(b) Defect:** The DOI may identify the preprint, but the paper never states that this DOI archives the repository, corpus-derived outputs, scripts, or supplements. As written, the DOI does not cure the missing repository location.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** State exactly what the Zenodo DOI contains and whether it includes the repository, data, scripts, and supplements used for the results.

8. **Major factual background claims in §1.1 lack citations.**  
   **(a) Quote + section:** §1.1: “The Indus Valley Civilization (IVC, ca. 2600–1900 BCE) produced approximately 5,000 inscribed objects … bearing a script of approximately 400 distinct signs.”  
   **(b) Defect:** These are factual corpus-history claims, but no source is cited in the sentence. They may be conventional, but the audit standard is checkability from what the paper cites and prints.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Cite a corpus/catalogue source for the object count, date range, object classes, and sign count.

9. **“Officially undeciphered” is uncited and undefined.**  
   **(a) Quote + section:** §1.1: “Despite a century of scholarship, the script remains officially undeciphered.”  
   **(b) Defect:** “Officially” implies an authority or consensus body, but none is identified.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Replace with “widely regarded as undeciphered” and cite standard literature, or identify the authority meant.

10. **Prior hypotheses are cited incompletely; one cited work is absent from the references.**  
   **(a) Quote + section:** §1.1: “Competing hypotheses have proposed proto-Dravidian (Parpola 1994; Mahadevan 1977), proto-Munda (Witzel 1999), an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected) …”  
   **(b) Defect:** “Jha & Rajaram 2000” is not in the reference list. The claim “widely rejected” also has no supporting citation.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Add the full Jha & Rajaram reference and citations documenting rejection.

11. **Heras is invoked but not cited.**  
   **(a) Quote + section:** §1.1: “beginning with Heras in the 1930s and developed most fully by Parpola.”  
   **(b) Defect:** No Heras work appears in the references.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Add the relevant Heras citation(s), with publication details.

12. **Sproat 2014 is cited but missing from the references.**  
   **(a) Quote + section:** §1.2: “That entropy work has been criticised (Sproat 2014) and defended (Rao et al. 2010).”  
   **(b) Defect:** No Sproat 2014 reference appears in §8.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Add the full Sproat 2014 reference.

13. **Rao et al. 2010 is cited but missing from the references.**  
   **(a) Quote + section:** §1.2: “defended (Rao et al. 2010).”  
   **(b) Defect:** The reference list includes Rao et al. 2009 items and Yadav et al. 2010, but no Rao et al. 2010 defense.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Add the full Rao et al. 2010 reference or correct the citation.

14. **Claim of no prior >90% coverage is unsupported and too broad.**  
   **(a) Quote + section:** §1.2: “To my knowledge, no prior work has claimed >90% token coverage with a published sign-by-sign evidence record.”  
   **(b) Defect:** This is a literature-survey claim, but no search method, inclusion criteria, or bibliography is given. It also says “published sign-by-sign evidence record,” while this paper’s own sign-by-sign record is not printed or located.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide a reproducible literature survey and publish the sign-by-sign evidence record.

15. **“Glossa-Lab, Phases 1–170” is not a citable method.**  
   **(a) Quote + section:** §1.3: “We present a computational grammar and candidate anchor model (Glossa-Lab, Phases 1–170).”  
   **(b) Defect:** Phases are repeatedly cited as evidence, but no phase reports are printed, archived, or externally identified.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Archive each phase report or include enough methods/results in the paper to make the phase references unnecessary.

16. **Internal phase numbering is anomalous: the paper claims Phases 1–170 but also invokes Phase-430.**  
   **(a) Quote + sections:** §1.3: “Phases 1–170.” §2.1.1: “Spec 068, executed as Phase-430.”  
   **(b) Defect:** The numbering system is unexplained and internally confusing. A reader cannot know whether Phase-430 postdates Phase-170, belongs to a different pipeline, or supersedes earlier phases.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide a phase chronology, version map, and supersession table.

17. **Spec 068 has an OSF link, but the inputs and comparison datasets are under-specified.**  
   **(a) Quote + section:** §2.1.1: “registered before the run at OSF: https://osf.io/3pbwe.” Also: “The comparison systems were Mesopotamian numerical signs … heraldic charges from the Dering Roll … a synthetic emblem process … and Linear B.”  
   **(b) Defect:** The OSF URL helps, but the paper itself gives no source citations for the Dering Roll extraction, Linear B DAMOS transliterations, Mesopotamian numerical signs, or synthetic emblem process.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite and identify every comparison table, extraction method, and version in the paper or linked archive.

18. **“Shakti corpus” and “ICIT line” are not properly identified.**  
   **(a) Quote + section:** §2.1.1: “the Shakti corpus, a restricted corpus in the ICIT line (3,045 analysable rows of documented lineage; 11,805 tokens; 557 distinct signs).”  
   **(b) Defect:** No reference, URL, editor, release, accession, or coding description is provided for the Shakti corpus or “ICIT line.”  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite or archive the corpus, define “ICIT line,” and provide provenance and coding documentation.

19. **The corpus claim “covers the major excavated IVC sites” is unsupported.**  
   **(a) Quote + section:** §2.1: “This corpus covers the major excavated IVC sites and represents the primary published formal-seal assemblage.”  
   **(b) Defect:** No external catalogue is cited to justify “major” or “primary published formal-seal assemblage.” The corpus is private, so the claim cannot be checked.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Define coverage criteria and compare the Holdat inventory against published catalogues.

20. **Catalogue sign accounting depends on an unprinted inventory.**  
   **(a) Quote + section:** §2.1: “the anchor table assigns readings to all 397 signs in the Mahadevan catalogue … The full sign-by-sign inventory, with each sign’s corpus frequency, is the file ANCHOR_STATUS_AUDIT.csv in the repository.”  
   **(b) Defect:** The sign inventory is load-bearing for all coverage percentages, but it is neither printed nor accessible.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Print the full sign inventory or provide an accessible archived CSV.

21. **Crosswalk file is load-bearing but not printed.**  
   **(a) Quote + section:** §2.1: “Crosswalk: 25-entry Mahadevan – Parpola crosswalk (mahadevan_parpola_crosswalk.json) for iconographic anchor validation.”  
   **(b) Defect:** The fish-sign correction, iconographic anchors, and M047/P47 assertion depend on this crosswalk. The file is not printed or accessible.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Include the 25-entry crosswalk in the paper or an archived supplement.

22. **Supplementary sources are listed without specifying what data were extracted.**  
   **(a) Quote + section:** §2.1: “Supplementary sources: Crawford (2001) Saar seals; Hojlund & Abu-Laban (2012) Failaka Tell F6; Parpola (1994, 2010) iconographic readings.”  
   **(b) Defect:** The paper does not identify seal numbers, figures, pages, tables, or extracted variables.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Give exact page/figure/table references and extracted records.

23. **SA-consistency is used before the SA method is defined.**  
   **(a) Quote + section:** §2.2: “DEDR rebus match with SA-consistency >= 0.15 from syllabic language model simulation.” §2.4 later defines “SA.”  
   **(b) Defect:** The method is invoked in the evidence hierarchy before being defined.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Define SA before §2.2 or move the evidence hierarchy after the method description.

24. **MEDIUM criteria rely on an SA threshold admitted to be uncalibrated and later failed.**  
   **(a) Quote + sections:** §2.2: “Signs with SA consistency >= 0.15 and a DEDR entry matching the modal reading were promoted to MEDIUM.” §2.4: “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.” §2.4: “its agreement on held-out anchors was 0.000.”  
   **(b) Defect:** A failed, uncalibrated model is allowed to promote signs to MEDIUM. The paper discloses the problem, but downstream counts still include MEDIUM readings that may rest on SA.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Identify every MEDIUM sign whose support includes SA and remove or downgrade SA-only promotions until calibrated against known scripts.

25. **Training data for the syllabic language model are not specified.**  
   **(a) Quote + section:** §2.4: “trained on Tamil/Dravidian syllable sequences.” §4.4: “The syllabic language model is trained on modern Tamil.”  
   **(b) Defect:** No corpus, source, preprocessing, tokenizer, train/test split, or parameterization is given.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the training corpus, preprocessing scripts, model configuration, and random seeds.

26. **Phase-107 is called pre-registered, but no registration is identified.**  
   **(a) Quote + section:** §2.4: “a later test inside this program (Phase-107, October 2026) put the SA machinery itself to a pre-registered held-out test.”  
   **(b) Defect:** No preregistration URL, timestamp, protocol, or identifier is given.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide the preregistration link and the frozen analysis plan.

27. **Substrate-analysis vocabulary is not printed.**  
   **(a) Quote + section:** §2.5: “we check SA modals against: - Munda/Austroasiatic substrate vocabulary … - BMAC … - Brahui cognates … - Proto-Elamo-Dravidian forms.”  
   **(b) Defect:** No wordlists, matching rules, or candidate matches are printed. The reader cannot verify substrate assignments.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide the exact lexical tables, matching criteria, and all accepted/rejected matches.

28. **HIGH/MEDIUM counts cannot be audited from the paper.**  
   **(a) Quote + section:** §3.1: “The 161 H+M anchors … cover 6,369 of 7,002 corpus tokens (90.96%).”  
   **(b) Defect:** The paper gives aggregate counts but not the sign-by-sign frequencies and classifications needed to recompute them. The named audit file is inaccessible.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Print or archive the sign-frequency table and confidence category per sign.

29. **The “independently recounted” claim names only an internal phase.**  
   **(a) Quote + section:** §3.1: “without them, 157 anchors cover 6,354 tokens (90.75%), a figure independently recounted in Phase-132.”  
   **(b) Defect:** “Independently” here means internal to the same unlocated program. No independent researcher, data release, or external code path is identified.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide the Phase-132 report and independent reproduction package, or remove “independently.”

30. **Several selected HIGH readings lack checkable evidence in the paper.**  
   **(a) Quote + section:** §3.3: “M211 … Unicorn seals exclusively”; “M125 … Bow iconography”; “M261 … Wheel/spindle, Tamil Murugan”; “M264 … Female figure”; “M328 … Man figure.”  
   **(b) Defect:** No image, catalogue reference, sign-shape evidence, seal IDs, or page references are printed for these iconographic identifications.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide exact Mahadevan/Parpola sign references, images or figure IDs, and corpus counts for every iconographic anchor.

31. **M342 and M176 are labelled HIGH despite no DEDR entry for M342 and purely interpretive morphology.**  
   **(a) Quote + section:** §3.3: “M342 ay/ā DEDR — Candidate case suffix: 584 tokens, 96% of them inscription-final; the case-suffix label is an interpretation…” and “M176 an/aṇ … Candidate masculine suffix: 356 tokens, 94% of them inscription-final; the gender label is likewise an interpretation…”  
   **(b) Defect:** The HIGH category requires two or more evidence criteria, but the table as printed gives positional dominance plus interpretation. For M342 the DEDR column is blank. The paper does not show how these satisfy HIGH rules.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** For each HIGH sign, print the exact criteria met and the evidence satisfying each criterion.

32. **M267 correction depends on hidden motif counts and hidden sign sequences.**  
   **(a) Quote + section:** §3.4: “M267 appears across all motif types — unicorn (127 tokens), zebu bull (72), elephant (37), rhinoceros (25), etc.”  
   **(b) Defect:** The correction is important, but the underlying motif-coded occurrences are not printed or available.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the M267 occurrence table with seal IDs, motif, position, and neighboring signs.

33. **The chi-square test for M267 is not reproducible from printed data.**  
   **(a) Quote + section:** §3.4: “Its distribution across seal motifs does not differ significantly from uniform (chi-square = 12.98, p = 0.1124, Phase-132).”  
   **(b) Defect:** The paper does not print the full observed and expected motif counts, degrees of freedom, or exact null definition. “Uniform” across what categories is not specified.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Print the contingency table, df, expected counts, and code.

34. **Fish-sign family list depends on an unprinted crosswalk.**  
   **(a) Quote + section:** §3.5: “Testing the full fish sign family (M047, M049, M052–M056, M145 — the signs this program’s Mahadevan–Parpola crosswalk file lists as fish-shaped).”  
   **(b) Defect:** The classification of signs as fish-shaped is central, but the crosswalk is not printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the crosswalk and cite the exact Parpola/Mahadevan basis for each fish-shaped sign.

35. **Fish isolation listing is unlocated.**  
   **(a) Quote + section:** §3.5: “the occurrence-by-occurrence listing is in the supplemental file fish_sign_compound_context.csv.”  
   **(b) Defect:** The file is inaccessible. Without it, the 0/113 claim cannot be checked.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Archive the CSV with seal IDs, sign sequences, site, and isolation/compound coding.

36. **Lothal “primary coastal port” and dock-basin claim lack citation.**  
   **(a) Quote + section:** §3.5: “including Lothal (the IVC’s primary coastal port, where a large basin has traditionally been interpreted as a dock — an interpretation some archaeologists dispute).”  
   **(b) Defect:** The archaeological characterization and dispute are factual claims with no citation.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Cite sources for Lothal’s port status and the basin/dock debate.

37. **Failaka pictorial-fish claim lacks figure/page evidence.**  
   **(a) Quote + section:** §3.5: “Dilmun-style seals at Failaka Island (Hojlund & Abu-Laban 2012) show fish in compound pictorial contexts … never as a solitary motif.”  
   **(b) Defect:** No seal numbers, figures, pages, or counted denominator are provided.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide the inspected catalogue entries and images/figure references.

38. **Site-by-site H+M coverage is explicitly unpublished.**  
   **(a) Quote + section:** §3.6: “A site-by-site table for the 161-sign set has not been published.”  
   **(b) Defect:** Site robustness is load-bearing for generalization claims, but the current table is not given.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the site-by-site table for the 161-sign set.

39. **Claim that 18 signs occur “in equal frequency at all sites and motif types” is unsupported and conflicts with Appendix B granularity.**  
   **(a) Quote + sections:** §3.6: “18 signs with corpus frequency 5–7 … occur in equal frequency at all sites and motif types.” Appendix B: “These 18 signs have corpus frequencies of 5 (sixteen signs) or 6 (M270, M386).”  
   **(b) Defect:** A sign with frequency 5 or 6 cannot be demonstrated as occurring “in equal frequency at all sites and motif types” across 9 sites and multiple motifs without a table; no such table is printed. §3.6 also says frequency 5–7, while Appendix B says only 5 or 6.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Print site/motif occurrence counts for each of the 18 signs and reconcile “5–7” with Appendix B.

40. **Bigram and formula claims rely on an unlocated table.**  
   **(a) Quote + section:** §3.7: “we extracted 2,647 distinct bigrams … including 1,485 H+M-by-H+M bigrams; the full table is the supplemental file formula_bigram_table.csv.”  
   **(b) Defect:** The full bigram table is not accessible; no top-N list beyond a few examples is printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Archive the bigram table with counts, PMI, sign categories, and inscription IDs.

41. **“97 distinct formula types” are not listed.**  
   **(a) Quote + section:** §3.7: “97 distinct formula types are identified, organised by INITIAL sign.”  
   **(b) Defect:** The formula inventory is a central structural claim but is not printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Include the 97 formula types and their counts.

42. **Phase-142D and Phase-150 descriptions are numerically confusing.**  
   **(a) Quote + sections:** §3.7: “17/21 tested H+M signs show position-specific collocate profiles.” §3.13: “Observed collocate divergence rate: 66.7% of the 21 tested signs … show KL > 0.3 bits.” §3.13: “the Phase-142D descriptive result (81% of the tested signs show positionally distinct collocate sets).”  
   **(b) Defect:** The paper reports 17/21 = 81% and 66.7% of 21 in adjacent discussions without clearly distinguishing the criteria. This is checkability noise around an already inconclusive test.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** State explicitly which signs satisfy each criterion and provide the two definitions side by side.

43. **Iconographic enrichment table is unlocated.**  
   **(a) Quote + section:** §3.8: “the full table is the supplemental file iconographic_formula_pairs.csv.”  
   **(b) Defect:** The enrichment analysis cannot be checked without the table.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Archive the table with observed/expected counts and correction procedure.

44. **The “43 robust” adversarial recheck is not reproducible.**  
   **(a) Quote + section:** §3.8: “an adversarial recheck (Phase-149) estimates about 43 of the 63 are robust.”  
   **(b) Defect:** “About 43” is vague; no criteria, list, or Phase-149 report is printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the recheck criteria and robust/marginal classification for all 63 pairs.

45. **“Co-selected, not independent decorations” exceeds what can be checked from the paper.**  
   **(a) Quote + section:** §3.8: “This shows that the inscription’s INITIAL sign and the carved animal on the same seal are co-selected, not independent decorations.”  
   **(b) Defect:** The conclusion may follow from the hidden table, but the paper prints only five strongest associations. The reader cannot inspect the full multiple-testing result.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide full enrichment data and code.

46. **CISI/mayig corpus is not cited or identified.**  
   **(a) Quote + section:** §3.10: “Comparison with the CISI corpus (179 inscriptions, Parpola P-numbers, mayig digitization).”  
   **(b) Defect:** No reference, URL, release, or digitization protocol is given for CISI or “mayig.”  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite the CISI corpus and mayig digitization source.

47. **The 87% CISI opening-sign claim lacks denominator.**  
   **(a) Quote + section:** §3.10: “87% of CISI multi-sign inscriptions open with an INITIAL-class sign (the number of multi-sign inscriptions in that subset is not recorded in the Phase-145 report).”  
   **(b) Defect:** The paper itself admits the denominator is missing. The percentage is therefore not auditable.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Recompute and report numerator/denominator from an accessible corpus.

48. **Phonological exclusivity test depends on an unstated Sanskrit inventory.**  
   **(a) Quote + section:** §3.11: “phonemes that occur in Dravidian but are absent from the Sanskrit inventory used in this test.”  
   **(b) Defect:** The Sanskrit inventory used in the test is not cited, printed, or justified.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the exact Sanskrit and Dravidian inventories and their sources.

49. **Semantic clustering depends on an unlocated phase report.**  
   **(a) Quote + section:** §3.12: “The per-cluster list … is in the Phase-148 record (backend/reports/phase148_formula_semantics.json).”  
   **(b) Defect:** The semantic-domain assignments are interpretive and central to guild/civic/deity claims, but the list is inaccessible.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Archive the Phase-148 JSON and print domain assignment rules.

50. **Rakhigarhi divergence claim is under-supported by one CI and hidden data.**  
   **(a) Quote + section:** §3.14: “Rakhigarhi (n=33) is distinctively divergent from every other major site … no confidence intervals for those pairs are on record.”  
   **(b) Defect:** The broad “every other major site” claim is made while CIs are absent for most pairs. The paper partly discloses this, but still uses “distinctively divergent.”  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Compute and publish CIs for all Rakhigarhi pairs and provide the site sign-frequency tables.

51. **Shu-ilishu external-anchor facts are uncited in the relevant section.**  
   **(a) Quote + section:** §3.15: “The Shu-ilishu seal (Ur III, c.2020 BCE) … owner is named ‘Shu-ilishu’ … and his title is ‘interpreter of the Meluhha language.’”  
   **(b) Defect:** No source is cited in §3.15 for the seal, date, name, title, or transliteration.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite the publication of the Shu-ilishu seal and give catalogue/inscription references.

52. **Sibilant candidate roots are not printed.**  
   **(a) Quote + section:** §3.16: “17 DEDR-attested Dravidian sibilant roots were identified … The 17 roots … are listed in the Phase-153 record.”  
   **(b) Defect:** The roots are load-bearing for the later sibilant promotions, but the Phase-153 record is inaccessible.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Print the 17 roots, DEDR numbers, glosses, candidate signs, and rejected alternatives.

53. **Direct contradiction on V12/vowel harmony.**  
   **(a) Quote + sections:** §3.17: “vowel harmony is an open problem for the reading set.” §3.21: “consistent with our Phase-154 finding that V12 is a methodology artifact.”  
   **(b) Defect:** The paper first says V12 is unresolved and explicitly withdraws artifact language, then later states Phase-154 found it to be an artifact. This is an internal factual contradiction.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Decide one position. If unresolved, remove §3.21’s artifact claim; if artifact, provide the analysis resolving §3.17’s stated open problem.

54. **Tamil-Brahmi terminal comparison lacks a citation.**  
   **(a) Quote + section:** §3.18: “Testing these against the Tamil-Brahmi epigraphy terminal phoneme inventory (11 categories: -an/-aṉ, -ār/-ar, -ai, -iṉ/-in, -il, -ku/-kku, -um, -oṭu, -al/-āl, -am, -ām).”  
   **(b) Defect:** No Tamil-Brahmi source is cited for the inventory.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite the epigraphic source and define how categories were compiled.

55. **The post hoc Tamil-Brahmi expansion is admitted unrecorded but still reported.**  
   **(a) Quote + section:** §3.18: “a second, broader count was made after seeing this result … it is post hoc, its derivation is not fully recorded.”  
   **(b) Defect:** An unrecorded post hoc count should not be part of evidentiary reporting except as an explicit discarded analysis.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Remove it from results or reconstruct and archive the derivation.

56. **Gulf fish-sign abstract claim overstates §3.19’s admitted weak evidence.**  
   **(a) Quote + sections:** Abstract: “0 in the Gulf deposit catalog (0/27; Laursen 2010), for a combined result of 0/140.” §3.19: “That text search found no mention of an isolated fish sign — and … no fish-sign mentions at all in the Laursen text.” §3.19: “the Gulf material provides no counterexample … but it does not independently confirm it.”  
   **(b) Defect:** The abstract presents Gulf 0/27 as if it were a systematic isolation count. §3.19 admits the search found no fish-sign mentions at all and does not independently confirm the pattern.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Remove the combined 0/140 claim or replace it with separate wording: Holdat image/sign count 0/113; Gulf prose search found no counterexample but did not confirm fish-bearing cases.

57. **§4.5 repeats the Gulf overstatement.**  
   **(a) Quote + section:** §4.5: “No isolated fish signs found in Gulf context. Verdict: COMPOUND_ONLY_EXTENDED — fish sign is compound-only across both mainland and Gulf corpora.”  
   **(b) Defect:** This contradicts §3.19’s statement that the Gulf evidence “does not independently confirm it.”  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Downgrade §4.5 to the weaker §3.19 formulation or provide image-based Gulf counts.

58. **Laursen/Mitchell text-search method is inadequately reproducible.**  
   **(a) Quote + section:** §3.19: “searched 145,000 characters of extracted text from the Gulf Type seal catalog … and the Bahrain volume.”  
   **(b) Defect:** Search terms, OCR/extraction method, editions, pages, and scripts are not given.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish OCR text, search terms, scripts, and page ranges.

59. **“27 Indus-script contexts in Laursen’s catalog” is not listed.**  
   **(a) Quote + section:** §3.19: “Counting the 27 Indus-script contexts in Laursen’s catalog…”  
   **(b) Defect:** The 27 contexts are not identified by catalogue number/page/figure.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** List the 27 contexts and their sign readings or image references.

60. **Wells mining claims lack quotes, pages, and a benchmark.**  
   **(a) Quote + section:** §3.20: “Mining Wells (2015) … 284 sign references, 96 Dravidian language claims, 403-reference positional analysis appendix.”  
   **(b) Defect:** No page references, extracted snippets, mining code, or validation sample is provided.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish extraction outputs and hand-check precision/recall.

61. **Mahadevan mining claims lack quotes, pages, and auditable extraction.**  
   **(a) Quote + section:** §3.21: “the grammar paper contains 79 positional-class references and 61 grammar structure agreement hits with our 3-slot model.”  
   **(b) Defect:** No extracted passages, page numbers, or matching rules are printed. “Agreement hits” is undefined and internal.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide a coded table of hits with source page, quote, category, and reviewer validation.

62. **“10 papers, 1972–2018” and “38 papers” are admitted unverifiable but still used.**  
   **(a) Quote + section:** §3.23: “the aggregate counts ‘10 papers, 1972–2018’ and, in §3.24, ‘38 papers’ are this program’s own corpus counts and could not be tied to a verifiable external source.”  
   **(b) Defect:** The paper itself says the counts cannot be tied to a verifiable external source, yet they are used in §1.3 and §3.24 as literature-extraction evidence.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Replace with a bibliographic list of every mined document and stable identifiers.

63. **§1.3 overstates Mahadevan cross-validation.**  
   **(a) Quote + sections:** §1.3: “Cross-validation: 10/10 Mahadevan papers (1972–2018) are consistent with the positional grammar model.” §3.23: “could not be tied to a verifiable external source.”  
   **(b) Defect:** The abstracted result in §1.3 is based on document counts later admitted unverifiable.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Remove the 10/10 claim or provide the exact paper list and extraction evidence.

64. **“Across four independent decades” is misleading because the paper says these are one scholar’s works.**  
   **(a) Quote + section:** §3.23: “These are one scholar’s works across four decades, not independent witnesses…” Later same section: “Across four independent decades of scholarship…”  
   **(b) Defect:** The section contradicts itself: decades are not independent witnesses.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Remove “independent.”

65. **Parpola “cross-validation” is admitted not to be cross-validation.**  
   **(a) Quote + section:** §3.22: “This is not independent cross-validation … the count records appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”  
   **(b) Defect:** The paper still labels the result “Cross-validation” in §1.3 and §3.22. A text-hit count is not validation of sign readings.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Rename as “Parpola textual overlap” and provide sign-by-sign comparison if validation is intended.

66. **§1.3 says “44/75 HIGH-confidence readings overlap with readings or interpretive proposals in Parpola,” but §3.22 says only appearances in text were counted.**  
   **(a) Quote + sections:** §1.3: “44/75 HIGH-confidence readings overlap with readings or interpretive proposals in Parpola (1994).” §3.22: “appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”  
   **(b) Defect:** “Overlap with readings or interpretive proposals” overstates what was measured.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Rephrase §1.3 to match §3.22 or perform a real sign-by-sign comparison.

67. **Literature extraction ceiling overclaims after admitting recall is unmeasured.**  
   **(a) Quote + section:** §3.24: “its recall has never been measured against a hand-checked list of known proposals.” Same section: “The large majority of LOW signs carry placeholder readings with no proposed phonetic value in any available reference literature.”  
   **(b) Defect:** An unbenchmarked mining pipeline cannot support a claim about “any available reference literature.”  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Benchmark recall against hand-coded known proposals and limit the claim to the mined corpus.

68. **ICIT corpus is repeatedly invoked but not cited or located.**  
   **(a) Quote + sections:** §3.24: “ICIT corpus (5,318 inscriptions vs 1,670).” §4.4: “a compatible public corpus such as ICIT after sign-code crosswalking.”  
   **(b) Defect:** No ICIT reference, URL, release, coding system, or access instructions appear in the references.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Cite ICIT and specify version, access URL, sign coding, and crosswalk requirements.

69. **Sibilant promotions do not follow the stated MEDIUM criteria.**  
   **(a) Quote + sections:** §2.2 MEDIUM criteria: “Single strong evidence source: - DEDR rebus match with SA-consistency >= 0.15 … - Positional profile … - Supported allograph…” §3.25: “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits in the mined literature.”  
   **(b) Defect:** OCR text-proximity hits are not listed as a MEDIUM criterion in §2.2. The promotion rule is introduced ad hoc later.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Add text-proximity promotion to the hierarchy with validation data, or remove these signs from MEDIUM coverage.

70. **OCR proximity hits are not verified assignments.**  
   **(a) Quote + section:** §3.25: “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign.”  
   **(b) Defect:** The paper admits the evidence does not establish the sign-reading assignment, yet promotes signs into PROVISIONAL_MEDIUM and includes them in coverage.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Require manual verification of the cited passages before promotion or exclude from coverage.

71. **Sibilant provisional category is internally inconsistent.**  
   **(a) Quote + sections:** §2.2: “PROVISIONAL_MEDIUM (4 signs — M330, M165, M202, M198).” §3.27: “M198 … stays provisional while the other three do not.” §3.1: “The MEDIUM count includes 4 PROVISIONAL_MEDIUM signs.”  
   **(b) Defect:** The paper cannot decide whether all four are provisional or only M198 is. This affects counts and confidence labels.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide a single category table and update all sections consistently.

72. **Phase-166 “SUPPORTED_WITHIN_MODEL” is not external validation.**  
   **(a) Quote + section:** §3.27: “All four upgrades have DEDR backing and Proto-Dravidian phonotactic validity.”  
   **(b) Defect:** DEDR existence plus phonotactic validity does not verify that the sign has that value; countless readings can be DEDR-backed and phonotactically valid. The paper’s label risks overstating support.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide discriminative tests against alternative DEDR readings and non-Dravidian baselines.

73. **Meluhhan name list is not printed.**  
   **(a) Quote + section:** §3.28: “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names …”  
   **(b) Defect:** The 25 names, segmentation, and sources per name are not printed.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Include the full name list, transliteration, segmentation, source citation, and matching output.

74. **Fuzzy matching algorithm is under-specified.**  
   **(a) Quote + section:** §3.28: “The fuzzy prefix matching algorithm was intentionally broad (>=50% of phonological segments matching).”  
   **(b) Defect:** Segment definition, scoring, prefix handling, alternative readings, and tie handling are not specified.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish algorithm pseudocode/code and per-name results.

75. **Decode-blocker list is missing.**  
   **(a) Quote + section:** §3.29: “Statistical assessment of the top 19 decode-blocking LOW signs…”  
   **(b) Defect:** The 19 signs are not listed in §3.29. Their readings, frequencies, positions, and blocker effects are not shown.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Print the 19 signs and all assessed features.

76. **Hypothetical coverage increase is not reproducible.**  
   **(a) Quote + section:** §3.29: “If these 19 blockers were promoted to MEDIUM, token coverage would rise from 90.96% to an estimated 92.35%.”  
   **(b) Defect:** No sign counts are printed for the 19 blockers, so the estimate cannot be checked.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide token counts per blocker and exact recalculation.

77. **Master scorecard is not printed and mixes internal and external evidence.**  
   **(a) Quote + section:** §3.30: “32 total evidence items … 18 of them rated STRONGLY_SUPPORTED_WITHIN_MODEL or HIGHLY_SUPPORTED.”  
   **(b) Defect:** The 32 items and rating rules are not printed. The paper admits the labels are program-defined and that internal consistency is mixed with external evidence.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish the full scorecard, rating rubric, and separate internal checks from external validations.

78. **“Gulf seal fish-sign corroboration” in scorecard contradicts §3.19’s weaker conclusion.**  
   **(a) Quote + sections:** §3.30: “Gulf seal fish-sign corroboration (E06).” §3.19: “it does not independently confirm it.”  
   **(b) Defect:** The scorecard labels the Gulf result as corroboration despite the methods section saying it is not confirmatory.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Rename E06 as “no counterexample in text search” or perform image-based confirmation.

79. **Grammar variance retest is correctly disclosed as self-consistency, but then should not appear as evidential support.**  
   **(a) Quote + section:** §3.31: “This is a self-consistency check, not an accuracy measurement.” §1.3 lists: “Grammar self-consistency retest … 93.2%…”  
   **(b) Defect:** Listing the 93.2% among “components and results” risks presenting it as support. The paper itself says it is expected by construction.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Move it to an internal QA appendix and do not list it among substantive results.

80. **Example translations lack seal IDs and are not checkable.**  
   **(a) Quote + section:** §4.1: “M211 M099 M342 = kol-kol-ay = ‘the jar-guild lord’ (unicorn seal, formal guild title).”  
   **(b) Defect:** No actual seal ID, site, motif record, sign sequence source, or alternative parsing is given.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Provide seal IDs, images/catalogue references, sign segmentation, and all competing readings.

81. **Arthaśāstra analogy is uncited and absent from references.**  
   **(a) Quote + section:** §4.1: “The Arthaśāstra … documents Sanskrit superintendent titles…”  
   **(b) Defect:** No edition, translation, book/chapter, or reference appears in §8.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Cite the Arthaśāstra edition/translation and exact passages.

82. **Appendix B gives SA modals but not sign-by-sign assignments.**  
   **(a) Quote + section:** Appendix B: “Their modals from the syllabic LM are syllables without clear DEDR matches (e.g., ‘o’, ‘e’, ‘pi’, ‘du’, ‘pit’).”  
   **(b) Defect:** The examples are not mapped to the 18 signs, so the claim cannot be checked.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Add a table with sign, frequency, position counts, SA modal, DEDR search result, and reason for rejection.

83. **Appendix C contradicts the abstract’s 59/59 internal checks.**  
   **(a) Quote + sections:** Abstract: “Internal consistency checks pass (59/59, Phases 1–170).” Appendix C: “the suite has since changed: on the October 2026 execution tree it reported 40 passed, 0 failed, 8 warnings.”  
   **(b) Defect:** The abstract reports the older 59/59 as if current, while Appendix C says the current execution tree has a different suite with warnings.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Report the current suite in the abstract or explain exactly why the old 59/59 remains relevant.

84. **Appendix C contains internal metrics not auditable from the paper.**  
   **(a) Quote + section:** Appendix C: “Dravidian Tier 1 lift ratio: 3.13x above null (Phase-44).”  
   **(b) Defect:** The null model, numerator, denominator, signs, and code are not provided.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Publish Phase-44 inputs, null definition, code, and outputs.

85. **References omit several cited or necessary sources.**  
   **(a) Quote + sections:** Cited in text but missing from §8 include “Jha & Rajaram 2000” (§1.1), “Sproat 2014” (§1.2), “Rao et al. 2010” (§1.2), “Heras” (§1.1), Arthaśāstra source (§4.1), CISI/mayig (§3.10), ICIT (§§3.24, 4.4), Shakti corpus (§2.1.1), DAMOS transliterations (§2.1.1), and Tamil-Brahmi source (§3.18).  
   **(b) Defect:** Missing references prevent readers from checking multiple factual and methodological claims.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Add complete bibliographic entries and stable access links where relevant.

86. **Several “external” studies are future-dated or unpublished/preprint-level without adequate archiving context.**  
   **(a) Quote + sections:** Abstract date: “May 2026 (revised October 2026).” §3.10: “Nair 2026, arXiv:2604.17828.” References: “Roif (2025a)… Academia.edu”; “Roif (2025b)… Academia.edu.”  
   **(b) Defect:** Preprint/Academia sources can be cited, but the paper leans on them for model comparison and fish-sign predictions. No archival snapshot, version, or access date is given for mutable Academia.edu documents.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Archive cited web documents and provide access dates/version identifiers.

87. **Terminology “H+M” is used in the abstract before being formally defined.**  
   **(a) Quote + section:** Abstract: “69.8% of seals consist entirely of such signs”; “H+M signs” appears later in §1.3 and §3.1.  
   **(b) Defect:** Readers infer H+M means HIGH+MEDIUM, but the abbreviation is not explicitly defined at first use.  
   **(c) Severity:** **MINOR**  
   **(d) Settle/correct:** Define “H+M = HIGH plus MEDIUM” at first occurrence.

88. **“Mahadevan M-numbers” are used as if sufficient to identify sign shapes, but no sign list is printed.**  
   **(a) Quote + section:** Abstract: “Mahadevan M-numbers.” §2.1: “Sign encoding: Mahadevan M-numbers.”  
   **(b) Defect:** M-numbers require access to Mahadevan’s sign table; the paper does not reproduce the relevant signs or provide sign images for anchors.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Include sign images or a sign appendix for all H+M signs.

89. **The paper repeatedly cites “program records” instead of evidence.**  
   **(a) Quote + examples:** §3.2: “from Parpola 1994 via this program’s Phase-51.” §3.20: “we could not locate that claim in our records.” §3.23: “this program’s own text-mining counts.”  
   **(b) Defect:** Internal records are not evidence unless archived and inspectable. The paper uses them as an evidentiary substrate throughout.  
   **(c) Severity:** **MAJOR**  
   **(d) Settle/correct:** Archive all cited records and replace vague “records” language with exact files/IDs.

90. **“All phase reports, scripts, and the anchor table are available” is not true from the paper as provided.**  
   **(a) Quote + section:** §5: “All phase reports, scripts, and the anchor table are available in the Glossa-Lab repository.”  
   **(b) Defect:** Again, no repository is identified. This is a checkability failure repeated in the conclusion.  
   **(c) Severity:** **CRITICAL**  
   **(d) Settle/correct:** Provide the repository URL/DOI or remove the availability claim.

---

## Verified disclosures / checks that pass narrowly

1. **Corpus unavailability is explicitly disclosed.**  
   Quote: Abstract: “The corpus itself is not publicly released … so corpus-level counts cannot yet be re-run by other researchers.” This is an adequate disclosure of a major reproducibility limit, but downstream claims still often overstate certainty.

2. **The Zipf/frequency-curve evidence is properly downgraded.**  
   Quote: §2.1: “we no longer present it as evidence that the script is a language.” §2.1.1: “UNINFORMATIVE.” This disclosure is clear.

3. **SA model failure is explicitly reported.**  
   Quote: §2.4: “its agreement on held-out anchors was 0.000.” This is a strong negative disclosure. The problem is that SA-supported MEDIUM readings remain in the model without a full printed audit.

4. **Polysemy permutation null is honestly reported as inconclusive.**  
   Quote: §3.13: “the real corpus does not show more position-specific collocate divergence than shuffled corpora.” This limitation is clear.

5. **Parpola overlap is correctly caveated in §3.22.**  
   Quote: §3.22: “This is not independent cross-validation.” The defect is inconsistent labeling elsewhere, not the caveat itself.

6. **Vowel-harmony problem is honestly disclosed in §3.17.**  
   Quote: §3.17: “vowel harmony is an open problem for the reading set.” This is adequate locally, but contradicted by §3.21.

7. **Grammar retest is correctly described as self-consistency in §3.31.**  
   Quote: §3.31: “This is a self-consistency check, not an accuracy measurement.” The caveat is appropriate.

8. **The paper distinguishes positional statistics from semantic interpretation in §3.2.**  
   Quote: §3.2: “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics.” This is a useful limitation statement.

9. **The Gulf fish-sign weakness is honestly stated in §3.19.**  
   Quote: §3.19: “it does not independently confirm it.” The problem is that the abstract, §4.5, and §3.30 overstate it.

10. **M267 correction is at least internally specific.**  
   Quote: §3.4 gives frequency, positions, motif counts, neighbor count, chi-square, and p-value. The result is not independently reproducible without data, but the claim is more concretely specified than most others.

---CALL-META finish_reason=stop usage={"prompt_tokens": 19544, "completion_tokens": 16596, "total_tokens": 36140, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 3072, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}} content_chars=50947---
