# Glossa Lab Indus Preprint v8 — Red-Team Round 5: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 117,822 chars, SHA-256 of PDF ea924ec13f3e8a33fa7045bca386a5baed68bd94357800ceb339e6eedf38e942), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs. Each finding was briefed to carry a kind label: (i) a defect in what the paper says, or (ii) a limitation the paper itself already discloses at the same strength.


## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## Findings

### 1. Conclusion upgrades “compatible” to “favours” despite body saying discrimination is not established
- **Kind: (i)**
- **Quoted passage:** “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”
- **Defect:** This is stronger than the limitations section permits. The paper’s own §4.4 says: “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” “Favours” is a discriminative claim; “merely compatible” is not.
- **Severity:** MAJOR
- **What would settle it:** A preregistered or fully specified comparative test against Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan, and language-neutral baselines, with reported effect sizes and error rates; or downgrade the conclusion to “compatible with Proto-Dravidian under the tested assumptions.”

---

### 2. Data-availability commit statement is self-contradictory
- **Kind: (i)**
- **Quoted passage:** “A reader who checks out the named commit therefore sees the paper’s text exactly as frozen; the only sentence that differs in that checkout is this one, which there names the previous round’s commit.”
- **Defect:** This cannot both be true. If the checkout differs in “this one” sentence, then the checkout does **not** show “the paper’s text exactly as frozen.” The paper claims the branch/commit identifies the exact text, then immediately says the text at that commit differs.
- **Severity:** MAJOR
- **What would settle it:** Archive the exact PDF/source text as a Zenodo artifact or tag a repository commit whose paper text is byte-identical to the submitted draft, including §6.

---

### 3. Broken cross-reference for checking the z-score inputs
- **Kind: (i)**
- **Quoted passage:** “The z-score can therefore be checked arithmetically from the printed inputs (§5), but the fit itself can be re-run only from the script and the corpus.”
- **Defect:** §5 does not print the required inputs for the arithmetic check. The required inputs are in §2.3: observed \(R^2 = 0.9916\), null mean \(0.4385\), SD \(0.05347\). §5 repeats only the headline z/p wording.
- **Severity:** MINOR
- **What would settle it:** Change “§5” to “§2.3,” or print the observed value, null mean, and null SD in §5.

---

### 4. Iconographic enrichment test applies a Bonferroni χ² threshold while admitting the printed statistic is only a single-cell contribution
- **Kind: (i)**
- **Quoted passage:** “We tested 394 INITIAL-sign × iconography pairs for enrichment (chi-square, one degree of freedom per pair, Bonferroni-corrected threshold 𝜒2 ≈ 14.7).”
- **Quoted passage:** “The chi-square printed for each pair is that pair’s single-cell contribution, 𝜒2 = (𝑂 − 𝐸)2 /𝐸 … It is not a full 2 × 2 chi-square for the pair.”
- **Defect:** The paper uses a one-degree-of-freedom χ² threshold and “pass” language, but the statistic printed is explicitly not the full 2×2 χ² test statistic. A single-cell contribution is not automatically distributed as χ² with 1 df under the stated pairwise independence test. The threshold/passing claims are therefore under-justified as stated.
- **Severity:** MAJOR
- **What would settle it:** Report the full 2×2 tables and full χ² or exact-test p-values for all 394 pairs, with the multiple-testing correction applied to those valid p-values; or empirically calibrate the single-cell statistic by permutation.

---

### 5. Several named Mahadevan papers used in §3.23 lack corresponding §8 references
- **Kind: (i)**
- **Quoted passage:** “For the record, the Phase-160 counts give per-paper hits for all ten papers mined: Grammar of Indus Texts (1986) 8; What Do We Know (1989) 7; Terminal Ideograms (1982) 6; Encyclopaedia (1994) 5; Place Signs (1981) 4; Akam-Puram (2011) 4; Toponyms (2018) 3; Bilingual Parallels (1972) 3; Murukan (1999) 2; Blue Neck (2008) 2.”
- **Defect:** §8 contains entries for Mahadevan 1981, 1982, 1986, 1989, 2011, but not clear bibliographic entries for “Encyclopaedia (1994),” “Toponyms (2018),” “Bilingual Parallels (1972),” “Murukan (1999),” or “Blue Neck (2008).” These are used as mined sources but are not reference-resolvable from the paper.
- **Severity:** MINOR
- **What would settle it:** Add complete §8 entries for every mined paper named in §3.23, or state explicitly that those items are unidentified internal corpus labels.

---

### 6. HIGH-confidence rule is not auditable from the paper’s own records
- **Kind: (ii)**
- **Quoted passage:** “HIGH (75 signs): Two or more of the following evidence criteria are met.”
- **Quoted passage:** “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”
- **Defect:** The paper’s category definition says HIGH means two or more criteria are met, but the paper also discloses that neither the paper nor the audit file records criterion-by-criterion pass/fail data sufficient to verify that claim for any particular HIGH sign.
- **Severity:** MAJOR
- **What would settle it:** Publish a sign-by-sign criterion matrix with explicit pass/fail fields for iconographic match, distributional exclusivity, terminal-marker evidence, and any other criterion actually used.

---

### 7. DEDR matching lacks recorded candidate universe and multiple-comparison control
- **Kind: (ii)**
- **Quoted passage:** “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”
- **Defect:** The DEDR evidence route cannot be assigned a false-positive rate from the paper’s records. This is especially damaging because many readings depend on DEDR-backed rebus matches.
- **Severity:** MAJOR
- **What would settle it:** Publish the full search protocol, all candidate readings considered per sign, rejection reasons, allowed transformations, and a null/randomization or multiple-comparison correction estimating chance DEDR-hit rates.

---

### 8. Corpus-level counts cannot be independently rerun because the corpus is private
- **Kind: (ii)**
- **Quoted passage:** “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”
- **Quoted passage:** “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”
- **Defect:** Most headline quantities are corpus-level counts, but the underlying corpus is unavailable. The paper discloses this plainly, but it remains a critical reproducibility limitation.
- **Severity:** CRITICAL
- **What would settle it:** Public release of the Holdat corpus with sign sequences, site labels, motif labels, and inscription boundaries; or exact replication on a public corpus with a published crosswalk.

---

### 9. Fish-sign isolation result is untestable as fish-specific because the corpus has no single-sign inscriptions
- **Kind: (ii)**
- **Quoted passage:** “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”
- **Defect:** The fish isolation count is arithmetically clear but evidentially vacuous for fish-specific behavior. The paper states this at full strength.
- **Severity:** MAJOR
- **What would settle it:** Test a corpus or object class containing single-sign inscriptions and compare fish signs against other sign families under the same isolation opportunity.

---

### 10. Fish-family supplement contains an acknowledged unresolved mismatch
- **Kind: (ii)**
- **Quoted passage:** “The supplemental file fish_sign_compound_context.csv lists 27 compound occurrences with their contexts (13 for M047 and 14 for M001; M001 is not in the family list printed above, and that mismatch is on record and unresolved).”
- **Defect:** The citable fish-family list excludes M001, but the supplemental fish context file includes 14 M001 cases. The paper discloses the mismatch but leaves the family definition internally unresolved.
- **Severity:** MAJOR
- **What would settle it:** Either justify M001 as fish-family and add it to the printed family list, or remove M001 rows from the fish-family supplement and recompute any dependent counts.

---

### 11. CISI opening-sign percentage is carried without numerator or denominator
- **Kind: (ii)**
- **Quoted passage:** “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed, and we report it as an uncountable figure carried from that record, not as a verified result.”
- **Defect:** The 87.08% CISI opening-sign figure cannot be recomputed from the paper or its stated records. The paper discloses this plainly.
- **Severity:** MAJOR
- **What would settle it:** Provide the numerator, denominator, inclusion criteria, and the list of CISI inscriptions/signs used.

---

### 12. Phase-152 Shu-ilishu /i/ slot includes a sign whose recorded reading lacks /i/
- **Kind: (ii)**
- **Quoted passage:** “/i/ by the candidate signs the Phase-152 record lists — M267, M162, M336, M305, M045 — of which M305’s recorded reading, ōṭu/comitative, contains no /i/ sound; the record’s slot list is reported here as recorded, and this mismatch is one reason the test’s result is stated as inventory overlap only”
- **Defect:** The paper carries a phonological-slot list with an internally wrong member. It discloses the mismatch and weakens the claim accordingly.
- **Severity:** MINOR
- **What would settle it:** Correct the Phase-152 slot list, rerun the slot-coverage calculation, and report the revised coverage.

---

### 13. Phase-153 sibilant count in the record conflicts with the checkable count
- **Kind: (ii)**
- **Quoted passage:** “The Phase-153 record asserts a count of 7 without listing the signs; on the readings printed in this paper and recorded in the audit file, 6 is the checkable figure.”
- **Defect:** The phase record and the paper/audit-readable sign list disagree. The paper discloses and corrects the count, but the underlying record remains inconsistent.
- **Severity:** MINOR
- **What would settle it:** Amend the Phase-153 record to list the six signs, or identify the seventh sign and justify its inclusion.

---

### 14. V12 vowel-harmony status is unresolved because the program has three incompatible test versions
- **Kind: (ii)**
- **Quoted passage:** “Depending on the version of the test, the pass rate is 75.3% (Phase-132: 476 of 632 decoded seals, against an 85% threshold), 64.2% on a stricter cross-reading version (Phase-133e), or 36.1% (Phase-154: 417 of the 1,154 seals checked passed; 737 seals failed), where the recorded verdict is V12_ACTIVE_CONCERN.”
- **Quoted passage:** “No one of these three procedures is currently the program’s authoritative V12 test: the records disagree because the test was redefined between runs, and the full rule changes are not recorded for every version.”
- **Defect:** The vowel-harmony diagnostic cannot currently clear or condemn readings because the test definition changed and the changes are not fully recorded. The paper discloses this.
- **Severity:** MAJOR
- **What would settle it:** Freeze one V12 protocol, document all rules, rerun it on the current 161-sign set, and publish sign/seal-level outputs.

---

### 15. Gulf fish-sign text search is not rerunnable from the record
- **Kind: (ii)**
- **Quoted passage:** “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”
- **Defect:** The Gulf extension’s text-search result cannot be reproduced from the paper’s records. The paper states this plainly.
- **Severity:** MAJOR
- **What would settle it:** Publish the exact extracted text files, search terms/regexes, preprocessing steps, and the 27-context enumeration.

---

### 16. Phase-170 grammar retest is a self-consistency check but could be misread as validation
- **Kind: (ii)**
- **Quoted passage:** “Results: 137/147 signs (93.2%) are classified by the thresholds into the positional class that is already their dominant class.”
- **Quoted passage:** “This is a self-consistency check, not an accuracy measurement: the thresholds … are applied to the same rates that define each sign’s dominant class, so a high figure is expected by construction and the check can only catch internal contradictions.”
- **Defect:** The 93.2% number is not an independent validation statistic. The paper discloses this correctly.
- **Severity:** MINOR
- **What would settle it:** Test fixed positional classes on a genuinely held-out corpus or on inscriptions/signs not used to define the classes.

---

## Positives / arithmetic checks I could confirm

1. **Site counts sum correctly:**  
   \(606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670\).

2. **Catalogue arithmetic checks:**  
   M001–M416 with 19 unused numbers gives \(416 - 19 = 397\) catalogue entries.  
   \(390\) attested + \(7\) zero-token catalogue-only signs = \(397\).

3. **H+M token coverage checks:**  
   \(4,925 + 1,444 = 6,369\).  
   \(6,369 / 7,002 = 0.9096 = 90.96\%\).

4. **Coverage without provisional signs checks:**  
   \(6,369 - 15 = 6,354\).  
   \(6,354 / 7,002 = 0.90746 = 90.75\%\).

5. **Confidence table token totals check:**  
   \(4,925 + 1,429 + 15 + 633 = 7,002\).  
   HIGH: \(4,925/7,002 = 70.34\%\).  
   MEDIUM excluding provisional: \(1,429/7,002 = 20.41\%\).  
   PROVISIONAL_MEDIUM: \(15/7,002 = 0.21\%\).  
   LOW: \(633/7,002 = 9.04\%\).

6. **Sign-category totals check:**  
   \(75 + 86 + 236 = 397\).  
   \(75 + 86 = 161\).

7. **SA-removal bound checks:**  
   \(161 - 43 = 118\).  
   \(6,369 - 398 = 5,971\).  
   \(5,971/7,002 = 85.28\%\).

8. **Phase-134 z-score checks:**  
   \((0.9916 - 0.4385)/0.05347 = 10.344\), correctly printed as \(z = 10.3\).

9. **Permutation add-one p estimate checks:**  
   \((0+1)/(2,000+1) = 1/2,001 = 0.00049975\), correctly rounded to \(0.0005\).

10. **Held-out split arithmetic checks:**  
   \(1,176 + 494 = 1,670\).  
   \(1,176/1,670 = 70.4\%\), \(494/1,670 = 29.6\%\).  
   \(85/87 = 97.7\%\).  
   \(64 + 5 + 13 + 3 = 85\); denominators \(64 + 5 + 15 + 3 = 87\).

11. **M267 motif counts sum correctly:**  
   \(147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = 400\).  
   \(324/400 = 81.0\%\).  
   \(400/7,002 = 5.71\%\), matching the printed 5.7%.

12. **Fish-bearing site counts sum correctly:**  
   \(6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113\).

13. **Seal coverage checks:**  
   \(1,165 + 505 = 1,670\).  
   \(1,165/1,670 = 69.76\%\), printed as 69.8%.  
   \(505/1,670 = 30.24\%\), printed as 30.2%.

14. **Appendix B token total checks:**  
   Sixteen 5-token signs plus two 6-token signs gives \(16 \times 5 + 2 \times 6 = 92\).

15. **PMI example checks if total bigram tokens are \(7,002 - 1,670 = 5,332\):**  
   \(P(a,b)=122/5,332\).  
   \(P(M342)=584/7,002\).  
   \(P(M176)=356/7,002\).  
   \(\log_2[(122/5,332)/((584/7,002)(356/7,002))] \approx 2.43\), matching the printed PMI.

16. **Bonferroni threshold is numerically plausible:**  
   For 394 tests at familywise \(\alpha=0.05\), \(\alpha/394 \approx 0.0001269\), corresponding to \(\chi^2_1 \approx 14.7\). The issue is not the arithmetic; it is the use of a single-cell contribution as the test statistic.

17. **Iconographic table χ² values recompute approximately from printed expected counts:**  
   Example M045: \((24 - 2.874)^2/2.874 \approx 155.3\).  
   M016: \((23 - 2.754)^2/2.754 \approx 148.8\).

18. **Phonological exclusivity percentages check:**  
   \(35/157 = 22.3\%\), printed as 22%.  
   \(35/161 = 21.7\%\).  
   \(39/161 = 24.2\%\).

19. **Polysemy null z-score checks:**  
   Observed \(66.7\%\), null mean \(80.7\%\), SD \(0.088\):  
   \((0.667 - 0.807)/0.088 \approx -1.59\), matching \(z=-1.6\).

20. **V12 arithmetic checks:**  
   \(476/632 = 75.3\%\).  
   \(417/1,154 = 36.1\%\).  
   \(417 + 737 = 1,154\).  
   \(418 + 319 = 737\).

21. **Tamil-Brahmi comparison checks:**  
   \(4/7 = 57.1\%\), printed as 57%.  
   \(270/1,154 = 23.4\%\), matching the V07 violation rate.

22. **Decode-blocker hypothetical coverage checks:**  
   Two 6-token signs plus seventeen 5-token signs gives \(12 + 85 = 97\).  
   \(6,369 + 97 = 6,466\).  
   \(6,466/7,002 = 92.345\%\), consistent with 92.35%.

23. **Master evidence synthesis category total checks:**  
   \(12 + 8 + 8 + 4 = 32\).

24. **Phase-170 retest percentage checks:**  
   \(137/147 = 93.2\%\).  
   Phase-133 full + partial match: \(5.1\% + 38.4\% = 43.5\%\), correctly distinguished from the separate 44.3% quantity.

CALL-META pass1: finish_reason=stop; max_completion_tokens=48000; completion_tokens=10942; prompt_tokens=30440; output_chars=17467.


## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

## Kind (i) findings — defects in what the paper says

### 1. False claim that all 161 H+M readings have DEDR citations
**Quoted passage(s):**  
> “A publish-ready anchor table covering all 161 H+M candidate readings with DEDR citations” (§1.3 item 7)

> “M342 … ay/ā … DEDR —” (§3.3 table)

> “M060=kāṇṭāmirukam (a descriptive compound gloss, ‘rhinoceros’; no DEDR entry is recorded for this sign — its support is iconographic and distributional only, 20 tokens)” (§3.2)

**Defect:** The paper explicitly claims all 161 H+M readings have DEDR citations, but it also prints at least two H+M/high-salience signs without DEDR backing: M342 has “DEDR —”, and M060 is stated to have “no DEDR entry.” The claim “all 161 … with DEDR citations” is false on the paper’s own text.

**Severity:** MAJOR

**What would settle it:** Provide DEDR citations for every one of the 161 H+M readings, or revise the claim to say that some H+M readings are iconographic/distributional without DEDR citations.

---

### 2. Conclusion overstates Proto-Dravidian support relative to the paper’s own limitation
**Quoted passage(s):**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.” (§5)

> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” (§4.4 item 6)

**Defect:** The conclusion says the evidence “favours” Proto-Dravidian. The limitation section says the model cannot yet be treated as discriminative and is only “merely compatible with Proto-Dravidian” until formal baselines are tested. “Favours” is stronger than “compatible” and stronger than the body warrants.

**Severity:** MAJOR

**What would settle it:** Run and report a controlled comparison against Proto-Munda, early Indo-Aryan, and language-neutral baselines with pre-specified metrics, or change the conclusion to “compatible with Proto-Dravidian under the tested assumptions.”

---

### 3. “Tier 2” claims are invoked without a defined tier system and are overstated as “supported by multiple tests”
**Quoted passage:**  
> “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage — assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings) are Tier 2 claims supported by multiple tests.” (§5)

**Defect:** The paper does not define a Tier 1 / Tier 2 / Tier 3 evidentiary hierarchy in the methods. “Tier 2” appears as an unexplained label. Also, “supported by multiple tests” overstates the evidence for the 161 readings as a set: the paper itself says MEDIUM can rest on one source, some readings rest on SA+DEDR with uncalibrated false-positive risk, four rest on text-proximity promotions, and the readings have unresolved V12/V07 problems.

**Severity:** MAJOR

**What would settle it:** Define the tier system formally and map each claim/readings class to it; replace “supported by multiple tests” with a per-class statement matching the actual evidence routes.

---

### 4. “Reproducible” is overstated because key corpus-level results cannot be independently rerun
**Quoted passage(s):**  
> “We propose a reproducible computational grammar and candidate Proto-Dravidian anchor model for the Indus Valley Script.” (§5)

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.” (§6)

> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.” (Abstract)

**Defect:** Calling the model/grammar “reproducible” is stronger than the paper’s own data-availability facts. Most headline quantities are corpus-level counts, and the corpus is private. The repository may contain scripts and outputs, but independent reproduction of the central results is not currently possible.

**Severity:** MAJOR

**What would settle it:** Release the corpus, or qualify the claim as “partially reproducible from repository outputs; full corpus-level reproduction awaits corpus release.”

---

### 5. Internal contradiction in §3.30: it says no top-label tally is printed while printing exactly such a tally
**Quoted passage(s):**  
> “Results: 32 total evidence items (up from 23 at Phase-141), in the Phase-169 record’s own categories: 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT.” (§3.30)

> “The full per-item list, with each item’s label, is in the Phase-169 record (backend/reports/phase169_master_synthesis.json); it is not printed in this paper, and no single tally at the top labels is printed, because any such tally would mix the two kinds.” (§3.30)

**Defect:** The section prints the category tally, then says no such tally is printed. This is stale corrective text or a direct contradiction.

**Severity:** MINOR

**What would settle it:** Delete or rewrite “no single tally at the top labels is printed,” or remove the printed tally.

---

### 6. Gulf fish-sign summary overstates what §3.19 actually reports
**Quoted passage(s):**  
> “The search found no fish-sign mentions at all, so the Gulf material provides no counterexample to the compound-only pattern — and, because the search found no fish signs in the text, no confirmation of it either (§3.19).” (§4.5 item 2)

> “That text search found no mention of an isolated fish sign — and, to be precise about what a text search can show, no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits).” (§3.19)

**Defect:** §4.5 says “the search found no fish-sign mentions at all,” apparently across the Gulf search using Laursen and Mitchell. §3.19 only says “no fish-sign mentions at all in the Laursen text,” while the broader search is described as finding no mention of an isolated fish sign. The summary is stronger than the source-specific body statement.

**Severity:** MAJOR

**What would settle it:** Print source-specific hit counts and search terms for both Laursen and Mitchell, or revise §4.5 to “no fish-sign mentions in Laursen; no isolated fish sign reported in the searched Gulf texts.”

---

### 7. Cross-corpus “point of agreement” is not supported by recorded counts
**Quoted passage:**  
> “The opening-sign figure (87.08%, above) is the only quantity in this comparison that points the same way in both corpora, but because its numerator and denominator are not on record it is reported here as an uncountable carried figure, not as a point of agreement.” (§3.10)

**Defect:** The sentence says the figure “points the same way in both corpora” but also says it is “not as a point of agreement.” It also admits the numerator and denominator are not recorded. This is internally muddled: either it is evidence of agreement or it is not. As written, it tries to retain the rhetorical benefit of agreement while disclaiming it.

**Severity:** MINOR

**What would settle it:** Provide the CISI numerator/denominator and the comparable Holdat opening-sign statistic, or delete “points the same way in both corpora.”

---

### 8. “ICIT corpus … is required” is stronger than the evidence
**Quoted passage:**  
> “The ICIT corpus (5,318 texts) with contextual metadata is required to identify name-bearing seal sequences.” (§3.28)

**Defect:** The paper has shown that the current 1,670-seal corpus did not produce discriminative Meluhhan name matches. It has not shown that ICIT is required, nor that ICIT would be sufficient. “Required” is an unsupported necessity claim.

**Severity:** MINOR

**What would settle it:** Rephrase to “would be a natural next test” or demonstrate, by power analysis or successful ICIT run, that ICIT-level scale/metadata is necessary and sufficient for the intended identification.

---

### 9. The heading/title-level “Three-Slot Positional Grammar” remains stronger than the whole-inscription result
**Quoted passage(s):**  
> “A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar” (Title)

> “Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).” (Abstract)

> “Results: 137/147 signs (93.2%) are classified by the thresholds into the positional class that is already their dominant class. This is a self-consistency check, not an accuracy measurement” (§3.31)

**Defect:** The title advertises a “Three-Slot Positional Grammar.” The body repeatedly narrows this to sign-level positional regularity; whole-inscription full matches are only 5.1%, partial matches 38.4%, and the 93.2% retest is explicitly self-consistency, not accuracy. The title remains at pre-cure strength relative to the corrected body.

**Severity:** MAJOR

**What would settle it:** Retitle as “three-slot positional tendency/model at sign level,” or demonstrate that a substantial share of whole inscriptions match the grammar under a pre-specified rule.

---

## Kind (ii) findings — real limitations already disclosed at comparable strength

### 10. The central corpus is private, so corpus-level counts are not independently reproducible
**Quoted passage:**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” (Abstract)

**Defect:** This is a serious limitation: most headline results depend on corpus-level counts from a non-public corpus. The paper does disclose it plainly.

**Severity:** CRITICAL

**What would settle it:** Public release of Holdat LLC Indus Corpus v3, or publication of an independently reusable corpus with a validated crosswalk and rerun results.

---

### 11. No bilingual text; all readings remain provisional
**Quoted passage:**  
> “No bilingual text: All readings remain provisional until a bilingual inscription (IVS + Sumerian, Akkadian, or Sanskrit) is discovered.” (§4.4 item 1)

**Defect:** The decipherment cannot be validated in the strongest epigraphic sense without a bilingual. This is disclosed plainly.

**Severity:** CRITICAL

**What would settle it:** Discovery and analysis of a bilingual inscription containing IVS plus a known script.

---

### 12. HIGH/MEDIUM labels are rule-based, not calibrated probabilities
**Quoted passage:**  
> “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.” (§2.2)

**Defect:** The confidence labels invite epistemic interpretation, but no false-positive or error calibration exists. The paper states this clearly.

**Severity:** MAJOR

**What would settle it:** Blind validation on a known script or a held-out externally anchored corpus, yielding empirical error rates for each label.

---

### 13. HIGH signs cannot be criterion-by-criterion verified from the paper or audit file
**Quoted passage:**  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.” (§2.2)

**Defect:** The HIGH category depends on criteria that are not auditable from the printed record or audit file. The paper discloses this at full strength.

**Severity:** MAJOR

**What would settle it:** Publish a criterion-by-criterion pass/fail matrix for every sign, with denominators, coding rules, and supporting data.

---

### 14. DEDR matching lacks candidate logs and multiple-comparison control
**Quoted passage:**  
> “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.” (§2.2)

**Defect:** The DEDR rebus search is vulnerable to uncontrolled cherry-picking and multiple testing. The paper states the limitation plainly.

**Severity:** CRITICAL

**What would settle it:** Pre-register matching rules, record all considered/rejected candidates, define admissible transformations, and run a null/randomization or multiple-comparison correction.

---

### 15. SA simulation failed a held-out test and carries no information by itself
**Quoted passage:**  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.” (§2.4)

**Defect:** A major route into MEDIUM support is acknowledged to have no independent signal by itself. The paper discloses this directly.

**Severity:** CRITICAL

**What would settle it:** A successful pre-specified held-out validation where the Dravidian SA model discriminates known values from controls.

---

### 16. SA training data cannot be reconstructed
**Quoted passage:**  
> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.” (§2.4)

**Defect:** The language model’s training basis is unreconstructable. The paper discloses it.

**Severity:** MAJOR

**What would settle it:** Archive the exact training corpus, preprocessing, syllable inventory, model files, and run parameters.

---

### 17. The main permutation statistic cannot be exactly rerun from the record
**Quoted passage:**  
> “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.” (§2.3)

**Defect:** The headline z = 10.3 result is arithmetically checkable from printed summaries, but the actual permutation experiment is not exactly reproducible from the record alone. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Publish the exact data matrix, inclusion rules, random seed, and executable script version.

---

### 18. Fish-sign isolation result is not fish-specific
**Quoted passage:**  
> “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result” (§3.5)

**Defect:** The fish isolation test cannot test a fish-specific hypothesis in this corpus. The paper states this plainly.

**Severity:** MAJOR

**What would settle it:** Test a corpus or object class containing single-sign inscriptions and compare fish signs against non-fish signs.

---

### 19. M267 chi-square p-value is token-level and may overstate seal-level evidence
**Quoted passage:**  
> “the chi-square treats M267’s 400 tokens as independent observations, but a motif is a property of a seal, not of a token. The Phase-132 record does not state how many distinct seals the 400 tokens occur on, and no seal-level version of this test is on record” (§3.4)

**Defect:** The motif-independence test’s independence assumption is questionable because motif is seal-level. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Redo the test at seal level, reporting distinct seals containing M267 by motif.

---

### 20. Iconographic enrichment includes circularity and incomplete published data
**Quoted passage(s):**  
> “the exact inclusion rule is not stated in the record, so the Bonferroni denominator of 394 is reported as recorded and cannot be re-derived from the published files.” (§3.8)

> “for signs whose reading was itself suggested by the animal motif, ‘the reading matches the animal’ is circular and is not claimed here as validation.” (§3.8)

**Defect:** The iconographic test cannot be fully rederived from published files and cannot validate readings that were selected from the same iconographic information. The paper discloses both limitations.

**Severity:** MAJOR

**What would settle it:** Publish the full 394-pair table, inclusion rule, coding protocol, and separate discovery from validation datasets.

---

### 21. Text-mining and text-proximity evidence is unbenchmarked and incompletely specified
**Quoted passage(s):**  
> “The Phase-163 mining record does not specify the proximity window … the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved.” (§2.2)

> “no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records” (§7)

**Defect:** Several literature-mining counts and four PROVISIONAL_MEDIUM promotions rest on a pipeline whose precision/recall and exact specifications are not archived. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Archive OCR sources, prompts/models/settings, proximity rules, ambiguity rules, and benchmark the pipeline against a hand-coded gold standard.

---

### 22. V12 vowel harmony remains unresolved; V07 phonotactic violations hit headline signs
**Quoted passage(s):**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.” (§3.17)

> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.” (§3.18)

> “M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.” (§3.18)

**Defect:** The reading set has unresolved internal phonological problems, including violations concentrated in central signs. The paper discloses this.

**Severity:** CRITICAL

**What would settle it:** Freeze one V12/V07 protocol, rerun it on the current 161-sign set, publish sign-level violations, and revise readings that drive failures.

---

### 23. No formal discriminative language-family baseline
**Quoted passage:**  
> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” (§4.4 item 6)

**Defect:** The model is not yet shown to discriminate Proto-Dravidian from plausible alternatives. The paper discloses this directly.

**Severity:** CRITICAL

**What would settle it:** Pre-specified comparative tests against Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan, and language-neutral models using the same evidence rules and penalties.

---

### 24. Meluhhan name tests produce no discriminative match
**Quoted passage:**  
> “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.” (§3.28)

**Defect:** External name matching does not validate the readings. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** A pre-specified name-matching test producing statistically discriminative matches against attested external names, with controls for common short readings.

---

### 25. Site divergence result is small-sample descriptive, especially for Rakhigarhi
**Quoted passage:**  
> “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site, so its distinctiveness should be read as a measured difference on a small sample, not as proof that the difference is not a small-sample effect.” (§3.14)

**Defect:** The strongest site-divergence observation rests on a very small site sample. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** More Rakhigarhi inscriptions or a replication on an independent larger corpus with confidence intervals for all site pairs.

---

## Positives checked and confirmed from the printed text

1. **Site counts sum correctly:** 606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670.

2. **Catalogue arithmetic is internally consistent:** M001–M416 with 19 unused numbers gives 416 − 19 = 397 catalogue signs.

3. **Headline z-score recomputes:**  
   \[
   (0.9916 - 0.4385) / 0.05347 = 10.344
   \]  
   Printed as z = 10.3.

4. **F7 held-out agreement recomputes:** 85 / 87 = 97.7%.

5. **F7 split percentages recompute:** 1,176 / 1,670 = 70.4%; 494 / 1,670 = 29.6%.

6. **Coverage table recomputes:**  
   - 4,925 / 7,002 = 70.34%  
   - 1,429 / 7,002 = 20.41%  
   - 15 / 7,002 = 0.21%  
   - 1,444 / 7,002 = 20.62%  
   - 633 / 7,002 = 9.04%  
   - 6,369 / 7,002 = 90.96%

7. **Without provisional signs recomputes:** 6,369 − 15 = 6,354; 6,354 / 7,002 = 90.75%.

8. **SA+DEDR removal bound recomputes:** 6,369 − 398 = 5,971; 5,971 / 7,002 = 85.28%.

9. **Seal coverage recomputes:** 1,165 / 1,670 = 69.8%; 505 / 1,670 = 30.2%.

10. **Fish-bearing site counts sum correctly:** 6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113.

11. **M267 motif counts sum correctly:** 147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = 400.

12. **M267 positional counts sum correctly:** 324 + 59 + 17 = 400; 324 / 400 = 81.0%.

13. **M267 corpus frequency percentage recomputes:** 400 / 7,002 = 5.71%.

14. **Parpola overlap percentage recomputes:** 44 / 75 = 58.7%, rounded to 59%.

15. **Formula bigram corpus percentage recomputes:** 122 / 1,670 = 7.3%.

16. **M342·M176 PMI recomputes if total bigram tokens are 7,002 − 1,670 = 5,332:**  
   \[
   \log_2\left((122/5332)/((584/7002)(356/7002))\right)=2.43
   \]

17. **V07 rate recomputes:** 270 / 1,154 = 23.4%.

18. **Phase-154 V12 pass rate recomputes:** 417 / 1,154 = 36.1%.

19. **Phase-132 V12 pass rate recomputes:** 476 / 632 = 75.3%.

20. **Blocker hypothetical coverage recomputes:** 6,369 + 97 = 6,466; 6,466 / 7,002 = 92.35%.

21. **Appendix B token total recomputes:** sixteen signs × 5 tokens + two signs × 6 tokens = 92 tokens.

22. **Appendix B corpus percentage recomputes:** 92 / 7,002 = 1.31%.

CALL-META pass2: finish_reason=stop; max_completion_tokens=48000; completion_tokens=9860; prompt_tokens=30449; output_chars=22332.


## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

## Findings

### 1. “Reproducible” is overstated in the conclusion despite the paper’s own non-reproducibility disclosures
**Kind: (i)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “We propose a reproducible computational grammar and candidate Proto-Dravidian anchor model for the Indus Valley Script.”

Also:  
> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released”

and:  
> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**(b) Defect:**  
The conclusion’s unqualified “reproducible computational grammar” is stronger than the methods/data-availability body permits. The core corpus is unavailable; the strongest positional statistic requires the corpus and script; the SA training set is not reconstructable; several text-mining procedures lack prompts/model versions/search rules; several phase records lack seeds or inclusion rules. The paper repeatedly admits this, but the conclusion still uses the stronger summary-layer label “reproducible.”

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Either remove/qualify “reproducible” in the conclusion, or release an archived reproduction package containing the corpus or a legally reproducible equivalent, exact scripts, seeds, environments, training data, search terms, and all intermediate tables needed to regenerate the reported counts.

---

### 2. Primary corpus unavailability blocks independent reproduction of most headline numbers
**Kind: (ii)**  
**Severity: CRITICAL**

**(a) Quoted passage:**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

and:  
> “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect / limitation:**  
This is a real reproducibility failure for the main empirical claims: token coverage, seal coverage, positional statistics, fish-sign counts, bigram counts, site divergence, motif tests, and most phase results depend on a private corpus. The paper does disclose this plainly.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
Public release of Holdat LLC Indus Corpus v3, or a public corpus with a complete crosswalk plus regenerated outputs showing that the headline numbers reproduce.

---

### 3. HIGH-confidence labels are stronger than the recorded evidence structure can audit
**Kind: (i)**  
**Severity: CRITICAL**

**(a) Quoted passage:**  
> “HIGH (75 signs): Two or more of the following evidence criteria are met.”

But later in the same section:  
> “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field”

and:  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect:**  
The paper asserts that 75 signs meet “two or more” explicit HIGH criteria, but then admits the records do not contain criterion-by-criterion pass/fail data and that the recorded evidence-type pair does not map one-to-one onto the stated criteria. That makes the HIGH label stronger than the auditable records. This is not just a limitation; it is an internal mismatch between the rule as stated and the evidence as recorded.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
For all 75 HIGH signs, publish a criterion-by-criterion table showing which of the stated HIGH criteria each sign passes, with denominators, counts, motif tables, positional rates, DEDR/iconographic support, and coding protocol.

---

### 4. DEDR rebus matching is not reconstructable and has no recorded multiple-comparison control
**Kind: (ii)**  
**Severity: CRITICAL**

**(a) Quoted passage:**  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”

**(b) Defect / limitation:**  
The rebus-matching search space is undefined. Without rejected candidates, allowed transformations, or chance-rate correction, the reader cannot estimate how often a DEDR-looking match would arise by chance across hundreds of signs and dictionary entries. The paper discloses this clearly.

**(c) Severity:** CRITICAL

**(d) What would settle it:**  
A preregistered or frozen DEDR-search protocol, complete candidate lists per sign, rejected candidates, allowed phonological transformations, and a null/multiple-comparison analysis estimating false-match rates.

---

### 5. SA simulation training data and scoring are not reproducible
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

Also:  
> “One part of the SA+DEDR criterion cannot be reconstructed from our records: the ‘consistency’ score is described in the Phase-52 lineage as the fraction of a sign’s contexts agreeing on its modal reading, but no record defines how a context is delimited, how contexts are weighted, or how ties are handled.”

**(b) Defect / limitation:**  
The SA method is not reproducible from the paper or phase records. Its training corpus, inventory, size, context definition, weighting, and tie handling are unknown. The paper discloses this at adequate strength.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Release the SA training corpus or exact source, syllable inventory, preprocessing rules, model code, context definition, scoring formula, random seeds, and a regenerated table of all SA modal readings and consistency scores.

---

### 6. SA evidence has already failed a held-out test, yet remains in the MEDIUM route
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

and:  
> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect / limitation:**  
SA failed to discriminate in the paper’s own held-out test, yet 43 MEDIUM signs still carry SA+DEDR as part of their support. The paper does not hide this; it gives a bound removing all 43.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Either remove SA from promotion criteria, or demonstrate with a frozen benchmark on a known script that the SA procedure has a measurable and acceptable false-positive/true-positive rate.

---

### 7. The strongest positional statistic cannot be exactly rerun from the record
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

and:  
> “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script … this section does not reproduce the script’s procedure.”

**(b) Defect / limitation:**  
The z = 10.3 arithmetic can be checked from printed values, but the statistic itself is not fully specified in the paper or phase record. Exact rerun requires unavailable corpus plus script plus unrecorded seed/inclusion details. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the input matrix, exact fitting formula, inscription-length handling, shuffle algorithm, inclusion/exclusion rules, random seed, and corpus data.

---

### 8. The “held-out” positional check is not a random held-out sample
**Kind: (ii)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “The F7 split was by site, not a random selection of seals”

and:  
> “Because the split is by site, the check tests whether classes fitted at the large sites predict the classes of signs at other sites; it is not a random held-out sample of seals.”

**(b) Defect / limitation:**  
The check is valid only as a site-transfer check, not as a random train/test validation. The paper states this plainly.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Report both site-held-out and random-seal-held-out results under frozen split rules and seeds.

---

### 9. Iconographic and exclusivity criteria cannot be reapplied from the paper
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record”

and:  
> “A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**(b) Defect / limitation:**  
Two central HIGH-promotion routes are not independently reproducible from the paper: no iconographic coding protocol, no blinding, no inter-coder agreement, and motif denominators are not published as a table. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish an iconographic coding manual, all sign/motif codings, per-motif denominators, independent coder results, and inter-rater reliability.

---

### 10. Iconographic enrichment test uses an unclear, post-conditioned denominator
**Kind: (i)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “We tested 394 INITIAL-sign × iconography pairs for enrichment”

and:  
> “The 394 pairs are the pairs formed by the INITIAL signs and icon types attested together in the corpus under the Phase-143 script’s inclusion rule; the exact inclusion rule is not stated in the record, so the Bonferroni denominator of 394 is reported as recorded and cannot be re-derived from the published files.”

**(b) Defect:**  
The test denominator is not an independently defined family of possible INITIAL-sign × iconography tests; it is “attested together” pairs under an unstated inclusion rule. That conditions the test family on observed co-occurrence and makes the Bonferroni denominator non-auditable. The inference that enriched pairs show co-selection is therefore methodologically under-specified.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the full initial-sign × icon matrix, including zero-observed pairs, the exact inclusion rule, row/column totals, expected counts, and corrected p-values for a predeclared test family.

---

### 11. Fish-sign isolation result is not fish-specific because the corpus has no single-sign inscriptions
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result”

**(b) Defect / limitation:**  
The 0/113 fish-sign isolation count cannot support a fish-specific rule in this corpus, because the corpus design/counts make isolation impossible for every sign. The paper discloses this plainly.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Run the same test on a corpus/object class containing single-sign inscriptions, with fish-bearing and non-fish-bearing singletons represented.

---

### 12. Fish supplemental context file has an unresolved family-list mismatch
**Kind: (ii)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “The supplemental file fish_sign_compound_context.csv lists 27 compound occurrences with their contexts (13 for M047 and 14 for M001; M001 is not in the family list printed above, and that mismatch is on record and unresolved).”

**(b) Defect / limitation:**  
The supplemental file includes M001 even though M001 is not in the printed fish-family list. The paper discloses the mismatch, but the dataset is internally inconsistent until resolved.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Explain whether M001 is fish-shaped, an allograph, a coding error, or an unrelated sign; then regenerate the fish-family list and supplemental file consistently.

---

### 13. Vowel-harmony test is unresolved and internally inconsistent across phases
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”

and:  
> “Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1%”

and:  
> “No one of these three procedures is currently the program’s authoritative V12 test”

**(b) Defect / limitation:**  
A linguistic plausibility check gives materially different results under different undocumented/redefined procedures. The paper discloses this and does not claim the problem is solved.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Freeze one vowel-harmony protocol, document the rule changes, rerun it on the current 161-sign set, and publish per-seal/per-reading failures.

---

### 14. Phonotactic violations hit high-frequency headline signs
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

and:  
> “M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**(b) Defect / limitation:**  
Nearly one quarter of decoded seals violate the stricter phonotactic test, and the violations are not confined to rare doubtful signs. The paper discloses this clearly.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the V07 rule, all violations, and either correct readings to remove the failures or demonstrate that the violation rule is invalid for Proto-Dravidian/Indus contexts.

---

### 15. Text-mining pipeline is not reproducible at the level needed to verify mined claims
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

and:  
> “no benchmark of the mining pipeline’s recall or precision exists”

**(b) Defect / limitation:**  
The literature-mining results cannot be independently rerun as methods; only the reported outputs can be inspected. Recall and precision are unknown. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Archive source texts/OCR versions, search terms, prompts, model names/versions, run settings, code, sampled validation, and a hand-coded benchmark estimating recall and precision.

---

### 16. Provisional sibilant promotions rest on partly unrecorded proximity rules
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved.”

**(b) Defect / limitation:**  
The four PROVISIONAL_MEDIUM promotions are based on text-proximity hits generated by an incompletely specified rule. The paper discloses this and keeps the signs provisional.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the exact proximity window, OCR source/version, matching rules, ambiguity rules, hit contexts, and a manual verification of whether each hit is a real sign-reading assignment.

---

### 17. Commit-pinning statement is self-contradictory
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “A reader who checks out the named commit therefore sees the paper’s text exactly as frozen; the only sentence that differs in that checkout is this one, which there names the previous round’s commit.”

**(b) Defect:**  
“Exactly as frozen” is immediately contradicted by “the only sentence that differs.” The self-referential commit sentence means the named commit does not contain exactly the text the reader is reading.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Archive the exact PDF/source text under an immutable DOI/version tag, and make the commit sentence match the archived text without self-referential exception.

---

### 18. The paper cites Jha & Rajaram 2000 but gives no reference-list entry
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected)”

**(b) Defect:**  
No “Jha & Rajaram 2000” entry appears in §8. This is a citation-completeness failure.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Add the full bibliographic entry or remove the citation.

---

### 19. The paper cites Parpola 1975 for Meluhhan names but gives no matching reference
**Kind: (i)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)”

**(b) Defect:**  
§8 contains no “Parpola 1975” reference. It contains “Parpola, S., Parpola, A. & Brunswig, R.H. (1977)” instead. Either the in-text year/authorship is wrong or the reference list is missing the cited work. This affects the source basis for the external-name battery.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Provide the exact Parpola 1975 bibliographic source used for the 25 names, or correct the in-text citation to the actual 1977 reference if that is what was used.

---

### 20. Several mined Mahadevan papers named in results lack §8 entries
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “Phase-160 counts give per-paper hits for all ten papers mined: Grammar of Indus Texts (1986) 8; What Do We Know (1989) 7; Terminal Ideograms (1982) 6; Encyclopaedia (1994) 5; Place Signs (1981) 4; Akam-Puram (2011) 4; Toponyms (2018) 3; Bilingual Parallels (1972) 3; Murukan (1999) 2; Blue Neck (2008) 2.”

**(b) Defect:**  
§8 gives entries for some but not all of these. Missing or unmatched items include “Encyclopaedia (1994),” “Toponyms (2018),” “Bilingual Parallels (1972),” “Murukan (1999),” and “Blue Neck (2008).” The 2011 §8 entry is titled “The Indus Fish Swam in the Great Bath,” not “Akam-Puram,” so that mapping is also unclear.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Add full references for all ten mined papers and map each mined-file label to the bibliographic entry.

---

### 21. Several comparison datasets/sources are intentionally not bibliographically identified
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “this paper gives no §8 entry and no fuller bibliographic identification for the Dering Roll source, the Mesopotamian numerical-sign table, or DAMOS (the source of the Linear B transliterations), and the Shakti corpus and the ICIT line are likewise identified only through that record.”

Also:  
> “CISI is the Corpus of Indus Seals and Inscriptions; neither it nor the mayig digitization has a §8 entry, and this paper can give no fuller bibliographic identification for either from its records.”

**(b) Defect / limitation:**  
Important comparison datasets used in methods are not independently citable from the paper. The paper discloses this, but it is still a reproducibility/citation-completeness limitation.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Add full bibliographic/data citations for Dering Roll, Mesopotamian numerical signs, DAMOS, Shakti, ICIT, CISI, and mayig, including access/version identifiers.

---

### 22. Shu-ilishu external facts lack §8 source support
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The external facts in this section (the Ur III date, c. 2020 BCE; the title ‘interpreter of the Meluhha language’; the provenance recorded as ‘excavated at Ur, held at British Museum’) are as recorded in the Phase-152 record … which is the source this section relies on; no §8 entry covers them.”

**(b) Defect / limitation:**  
An external validation section relies on phase-record notes rather than a cited scholarly source or museum catalogue. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Cite the primary publication or museum catalogue for the Shu-ilishu seal, including accession/provenance and text reading.

---

### 23. Tamil-Brahmi terminal comparison uses an uncited working inventory
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “No published source for that 11-category inventory is cited in this paper or in the Phase-155 record; the inventory is the test’s own working list”

**(b) Defect / limitation:**  
The Tamil-Brahmi comparison cannot be checked against an external authority because the inventory is an internal list. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Cite a Tamil-Brahmi epigraphic source for the terminal categories, or publish a justified derivation of the 11-category inventory from primary inscriptions.

---

### 24. Gulf text search is not rerunnable from the record
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”

**(b) Defect / limitation:**  
The Gulf fish-sign text search cannot be reproduced because the search terms and context enumeration are missing. The paper discloses this.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the extracted texts, search terms, regexes or query logic, OCR versions, all hits/nonhits, and the 27-context catalogue.

---

### 25. The validation path does not currently contain an executable discriminating test
**Kind: (i)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

Also:  
> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**(b) Defect:**  
The paper is titled and framed as a “falsifiable computational decipherment hypothesis,” but its own validation path says no currently executable discriminating test exists on available data. Future bilingual discovery would test any decipherment proposal; it is not a presently specified computational falsification test. The summary-level “falsifiable” framing is stronger than the operational methods.

**(c) Severity:** MAJOR

**(d) What would settle it:**  
State specific, preregistered, rival-discriminating predictions that can be tested on currently available or newly released corpora, with pass/fail thresholds.

---

### 26. The methods source inventory is incomplete relative to later analyses
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “Supplementary sources: Crawford (2001), used only for the Saar/Dilmun seal comparanda; Hojlund & Abu-Laban (2012), used only for the Failaka pictorial-fish observation in §3.5; Parpola (1994, 2010), iconographic readings.”

**(b) Defect:**  
This “Supplementary sources” list is not a complete source inventory for the paper’s methods/results. Later sections use Laursen (2010), Mitchell (1986), Wells & Fuls (2015), multiple Mahadevan papers, Steinkeller, Potts, Reade, Kjaerum, Nair, Roif, Krishnamurti, and others. As written, the methods source inventory is misleadingly narrow.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Rename this sentence as a limited list for particular comparanda, or provide a complete source inventory by analysis.

---

### 27. §3.30 says no top-label tally is printed, but the tally is printed
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “Results: 32 total evidence items (up from 23 at Phase-141), in the Phase-169 record’s own categories: 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT.”

Later in the same paragraph:  
> “it is not printed in this paper, and no single tally at the top labels is printed, because any such tally would mix the two kinds.”

**(b) Defect:**  
The paragraph prints exactly the category tally it later says is not printed. This is stale corrective text.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Delete or rewrite the “no single tally” sentence.

---

### 28. Reference list contains at least one apparently unused or mismatched entry
**Kind: (i)**  
**Severity: MINOR**

**(a) Quoted passage:**  
Reference list:  
> “Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”

and:  
> “Parpola, S., Parpola, A. & Brunswig, R.H. (1977). The Meluḥḥa village…”

**(b) Defect:**  
The in-text prior-work citation specifically names the Science entropy paper, not the PNAS Markov-model paper. The Meluhhan-name section cites “Parpola 1975,” not the listed 1977 Parpola/Parpola/Brunswig item. This is a references-both-directions defect: at least one reference is unused or the in-text citation is stale/mismatched.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Run a citation audit: every in-text citation must map to one §8 entry, and every §8 entry must be cited or removed.

---

### 29. The 87.08% CISI opening-sign figure is explicitly uncountable
**Kind: (ii)**  
**Severity: MAJOR**

**(a) Quoted passage:**  
> “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed”

**(b) Defect / limitation:**  
The CISI comparison reports a percentage without numerator or denominator. The paper discloses this and downgrades it to an “uncountable carried figure.”

**(c) Severity:** MAJOR

**(d) What would settle it:**  
Publish the CISI inscription count, multi-sign denominator, opening-INITIAL numerator, sign crosswalk, and script used to compute 87.08%.

---

### 30. Site coverage for the current 161-sign set was never computed
**Kind: (ii)**  
**Severity: MINOR**

**(a) Quoted passage:**  
> “No site-by-site coverage table for the 161-sign set exists: it was never computed, in this paper or in the program’s records.”

**(b) Defect / limitation:**  
The paper reports global seal coverage for the 161-sign set but lacks site-level coverage for that same set. The paper discloses this.

**(c) Severity:** MINOR

**(d) What would settle it:**  
Compute and publish site-by-site full/partial/blocked coverage for the 161-sign set.

---

## Positives / arithmetic I could confirm from the paper text

1. **Site counts sum correctly to 1,670 seals.**  
   606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = 1,670.

2. **Catalogue status counts sum correctly to 397 signs.**  
   75 HIGH + 86 MEDIUM + 236 LOW = 397.

3. **Attested-plus-zero catalogue accounting is internally consistent.**  
   390 attested signs + 7 catalogue-only zero-token signs = 397.

4. **Token coverage table recomputes.**  
   - HIGH: 4,925 / 7,002 = 70.34%.  
   - MEDIUM excluding provisional: 1,429 / 7,002 = 20.41%.  
   - PROVISIONAL_MEDIUM: 15 / 7,002 = 0.21%.  
   - MEDIUM including provisional: 1,444 / 7,002 = 20.62%.  
   - LOW: 633 / 7,002 = 9.04%.  
   - H+M total: 6,369 / 7,002 = 90.96%.

5. **Without provisional signs, the printed coverage recomputes.**  
   6,354 / 7,002 = 90.75%.

6. **The SA+DEDR removal bound recomputes.**  
   6,369 − 398 = 5,971 tokens; 5,971 / 7,002 = 85.28%.

7. **Seal coverage recomputes.**  
   1,165 / 1,670 = 69.76%, printed as 69.8%; 505 / 1,670 = 30.24%, printed as 30.2%.

8. **Phase-134 z-score arithmetic recomputes from printed inputs.**  
   (0.9916 − 0.4385) / 0.05347 = 10.344, printed as z = 10.3.

9. **Held-out positional agreement recomputes.**  
   85 / 87 = 97.70%, printed as 97.7%.

10. **Phase-134 site split counts and percentages recompute.**  
    606 + 492 + 78 = 1,176 training seals; 1,670 − 1,176 = 494 test seals.  
    1,176 / 1,670 = 70.4%; 494 / 1,670 = 29.6%.

11. **M267 motif counts sum correctly.**  
    147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = 400.

12. **M267 positional counts sum correctly.**  
    324 + 59 + 17 = 400; 324 / 400 = 81.0%.

13. **Fish-bearing seal counts sum correctly.**  
    6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = 113.

14. **Phase-148 semantic-cluster counts sum correctly.**  
    Clusters: 51 + 25 + 6 + 9 + 6 = 97.  
    Seals: 845 + 446 + 145 + 135 + 99 = 1,670.

15. **Phase-148 percentages recompute.**  
    845 / 1,670 = 50.6%; 446 / 1,670 = 26.7%; 145 / 1,670 = 8.7%; 135 / 1,670 = 8.1%; 99 / 1,670 = 5.9%.

16. **Parpola overlap percentage recomputes.**  
    44 / 75 = 58.7%, printed as 59%.

17. **Tamil-Brahmi terminal comparison recomputes.**  
    4 / 7 = 57.1%, printed as 57%.

18. **Current Dravidian-marker count recomputes.**  
    35 / 161 = 21.7%.

19. **Appendix B token total recomputes.**  
    Sixteen 5-token signs plus two 6-token signs: 16×5 + 2×6 = 92 tokens.  
    92 / 7,002 = 1.31%.

20. **Phase-168 blocker hypothetical coverage recomputes.**  
    6,369 + 97 = 6,466; 6,466 / 7,002 = 92.35%.

21. **Bonferroni false-positive comparison arithmetic is correct.**  
    394 × 0.05 = 19.7.

22. **Add-one permutation estimate is correct.**  
    (0 + 1) / (2,000 + 1) = 1 / 2,001 = 0.00049975, printed as 0.0005.

CALL-META pass3: finish_reason=stop; max_completion_tokens=60000; completion_tokens=12747; prompt_tokens=30412; output_chars=30337.


## PASS 4 — HOSTILE SUMMARY

## PASS 4 — HOSTILE SUMMARY

The paper has become unusually explicit about many weaknesses. The remaining strongest case against the headline is not that the draft hides all limits; it often states them. The case is that several summary/headline formulations still outrun the paper’s own evidentiary base, and the central reading claims remain dependent on private data, uncalibrated criteria, unrecorded search spaces, and non-independent within-model checks.

---

# A. Kind (i) defects — defects in what the paper says

## 1. “Reproducible” is overstated while the corpus-level results are explicitly not reproducible by readers

**Quoted passage**

> “We propose a reproducible computational grammar and candidate Proto-Dravidian anchor model for the Indus Valley Script.”

and:

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

and, in the Abstract:

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

**Defect**

The conclusion’s “reproducible computational grammar” is stronger than the paper’s own data-availability disclosure. Most core results are corpus-level: z-score, coverage, fish counts, positional rates, bigrams, iconographic enrichments, KL divergences, seal coverage. The paper itself says those “cannot yet be re-run by other researchers.” Scripts without the corpus do not make the computational claims reproducible.

**Severity**

MAJOR.

**What would settle it**

Public release or archived access to the exact Holdat corpus used, with the scripts and inputs pinned; or revise the claim to “partially reproducible scripts and records, but corpus-level results are not independently reproducible at present.”

---

## 2. The conclusion’s “evidence favours Proto-Dravidian” is stronger than the body’s disclosed results

**Quoted passage**

> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

But the paper also says:

> “Dravidian superiority over proto-Munda has not been formally quantified.”

and:

> “The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

and:

> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”

**Defect**

The body supports, at most, “compatible with Proto-Dravidian under model assumptions.” It explicitly says discrimination against Proto-Munda, early Indo-Aryan, and language-neutral baselines has not been done, and that existing Sanskrit comparisons are mixed. “Favours” is a stale stronger verdict in the conclusion.

**Severity**

CRITICAL.

**What would settle it**

A formal, pre-specified comparative test against Proto-Dravidian, Proto-Munda, early Indo-Aryan/Sanskrit, and language-neutral/null baselines, using the same scoring rules and reporting effect sizes/error rates; or weaken the conclusion to “compatible with a Proto-Dravidian framework under the tested assumptions.”

---

## 3. The evidence hierarchy contains a stale reference to “DEDR and Parpola criteria” that are not actually listed as HIGH criteria

**Quoted passage**

> “HIGH (75 signs): Two or more of the following evidence criteria are met. The criteria are separate tests, but they are not independent of each other: all except the DEDR and Parpola criteria are computed from the same corpus, and several from the same seals.”

The listed HIGH criteria immediately following are:

> “Iconographic match…”  
> “Distributional exclusivity…”  
> “Terminal marker evidence…”

**Defect**

The sentence refers to “the DEDR and Parpola criteria,” but the HIGH list contains no DEDR criterion and no Parpola criterion. This is a stale or inconsistent description inside the formal confidence-definition section.

**Severity**

MAJOR.

**What would settle it**

Rewrite §2.2 so the HIGH criteria are exactly enumerated, with no ghost criteria; or add DEDR/Parpola as explicit criteria and provide a sign-by-sign pass/fail audit showing their use.

---

## 4. The paper says HIGH requires two §2.2 criteria, but then admits selected HIGH signs rest on evidence types that do not map to those criteria

**Quoted passage**

> “HIGH confidence (selected readings): HIGH is assigned when any two of the §2.2 criteria are met; it is not an iconography-only category.”

But the same paragraph says:

> “M261’s row rests substantially on the published source behind its assignment (Parpola 1994, via Phase-51) — which is not itself one of the §2.2 criteria…”

and:

> “The audit’s two types are recorded as types, not scored criterion by criterion, and they do not map one-to-one onto the three criteria named in §2.2.”

and §2.2 says:

> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**Defect**

The confidence label is presented as rule-based, but the records do not show criterion-level compliance, and the paper admits the recorded evidence types do not map one-to-one onto the stated criteria. This is not merely a limitation; it undercuts the truth of “HIGH is assigned when any two of the §2.2 criteria are met” as an auditable statement.

**Severity**

MAJOR.

**What would settle it**

Publish a 75-row HIGH audit with explicit boolean fields for each §2.2 criterion, the raw counts behind each criterion, and the exact rule used to convert those criteria into HIGH.

---

## 5. The methods section states semantic classifications as if they are outputs, while the results section later says they are interpretations only

**Quoted passage**

From §2.3:

> “INITIAL-dominant signs are classified as title prefixes or classifier-derived words. TERMINAL-dominant signs are classified as case suffixes or proper-name terminals. MEDIAL signs are classified as content words or personal name syllables.”

But §3.2 says:

> “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics…”

and:

> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**Defect**

§2.3 still uses categorical semantic language — “are classified as title prefixes,” “case suffixes,” “personal name syllables” — before the later caveat that those semantic labels are not statistical outputs. This is exactly the kind of summary-layer echo stronger than the body.

**Severity**

MAJOR.

**What would settle it**

Rewrite §2.3 to say only that signs are classified positionally as INITIAL/MEDIAL/TERMINAL, and that all semantic labels are later model interpretations not established by the positional tests.

---

## 6. “Falsifiable” remains overclaimed relative to the paper’s own validation path

**Quoted passage**

Title:

> “A Falsifiable Computational Decipherment Hypothesis…”

Abstract:

> “This study does not claim epigraphic finality; it proposes a falsifiable computational model…”

But §4.5 says:

> “None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

and:

> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**Defect**

The title and abstract advertise “falsifiable” as a headline property. The validation section then admits that, among its three named validation paths, none is an available discriminating falsification test for the present model. “A future bilingual text could falsify readings” is true of almost any decipherment proposal; it is not a current computational falsification design.

**Severity**

MAJOR.

**What would settle it**

State explicit, pre-registered, currently runnable falsification criteria on available data, preferably including rival-model predictions; or weaken the headline to “testable in principle against future discoveries.”

---

## 7. The data-availability paragraph contradicts itself on whether the named commit exactly identifies the frozen paper text

**Quoted passage**

> “A reader who checks out the named commit therefore sees the paper’s text exactly as frozen; the only sentence that differs in that checkout is this one, which there names the previous round’s commit.”

**Defect**

“Exactly as frozen” is immediately contradicted by “the only sentence that differs.” This is a small but real archival-identification defect in a paper that relies heavily on exact phase/commit provenance.

**Severity**

MINOR.

**What would settle it**

Archive the exact PDF/source text at a DOI or immutable release, and remove the self-referential exception; or state plainly that the named commit is not byte-identical to the current draft.

---

## 8. The abstract contains a grammatical/run-on defect in a central claim sentence

**Quoted passage**

> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests (§3.2), and propose 161 candidate readings at HIGH or MEDIUM confidence.”

**Defect**

The sentence has no grammatical subject for “propose.” This matters because it occurs in the abstract’s central summary of what is measured versus what is proposed.

**Severity**

MINOR.

**What would settle it**

Rewrite, e.g. “We also propose 161 candidate readings…” or split the sentence.

---

# B. Kind (ii) already-disclosed limitations — real weaknesses the paper states plainly

These are not hidden defects. The paper itself discloses them at roughly the needed strength. They nevertheless severely weaken the headline reading claims.

## 1. Corpus-level claims cannot be independently rerun because the corpus is private

**Quoted passage**

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

and:

> “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**Defect / limitation**

The core numerical claims are locked behind a non-public corpus.

**Severity**

CRITICAL.

**What would settle it**

Release the exact corpus or provide controlled reproducible access; alternatively rerun on a public corpus with a published crosswalk.

---

## 2. No bilingual text; all readings remain provisional

**Quoted passage**

> “No bilingual text: All readings remain provisional until a bilingual inscription (IVS + Sumerian, Akkadian, or Sanskrit) is discovered. No numerical probability attaches to any individual reading; the confidence labels are rule-based categories (§2.2).”

**Defect / limitation**

The paper’s decipherment claims remain candidate readings, not validated readings.

**Severity**

CRITICAL.

**What would settle it**

A bilingual inscription or independent external anchor that fixes sign values.

---

## 3. The DEDR search space and rejection process are not recorded, and no multiple-comparison control was applied

**Quoted passage**

> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”

and:

> “A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**Defect / limitation**

The central rebus/DEDR matching mechanism lacks a recorded search space and false-positive control.

**Severity**

CRITICAL.

**What would settle it**

A fully logged DEDR-candidate generation protocol, all rejected candidates, allowed transformations, and null/randomization or multiple-comparison correction.

---

## 4. HIGH labels cannot be verified criterion-by-criterion from the paper or audit file

**Quoted passage**

> “The audit file records the same evidence-type pair (iconographic + distributional) for all 75 HIGH signs, §3.3 prints selected rows for 12 of them, and no record gives a criterion-by-criterion pass/fail for any HIGH sign.”

and:

> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded…”

**Defect / limitation**

The most important confidence category is not auditable against its own stated rule.

**Severity**

CRITICAL.

**What would settle it**

A sign-by-sign criterion audit with raw supporting counts and iconographic coding evidence.

---

## 5. Iconographic and exclusivity criteria cannot be reapplied from the paper alone

**Quoted passage**

> “The iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record…”

and:

> “A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**Defect / limitation**

A large part of the HIGH evidence is subjective or underdocumented.

**Severity**

MAJOR.

**What would settle it**

A blinded coding protocol, multiple coders, inter-coder reliability, and published motif denominators.

---

## 6. The SA model failed its own held-out test and has unreconstructable training data

**Quoted passage**

> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

and:

> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

**Defect / limitation**

One route to MEDIUM support is compromised: the model is uncalibrated, unreconstructable, and failed discrimination.

**Severity**

CRITICAL.

**What would settle it**

A specified training corpus, frozen algorithm, held-out validation on known scripts, and demonstrated discrimination against controls.

---

## 7. 43 MEDIUM signs rely on the SA+DEDR route, and a true SA-free headline cannot be computed

**Quoted passage**

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv. If all 43 were removed, 118 signs and 5,971 tokens (85.28%) would remain. That is a bound, not a recomputed headline…”

and:

> “A true SA-free headline cannot be computed from the records.”

**Defect / limitation**

A substantial part of the 161-sign headline depends on a route whose independent evidentiary value is acknowledged as weak.

**Severity**

MAJOR.

**What would settle it**

Criterion-level provenance showing which of the 43 survive on non-SA evidence, then recompute the headline without SA support.

---

## 8. The fish-sign isolation result is not fish-specific

**Quoted passage**

> “One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result…”

and:

> “What the count establishes is only that fish signs occur in this corpus in multi-sign inscriptions — as every sign in this corpus does.”

**Defect / limitation**

The fish result cannot support a fish-specific rule.

**Severity**

MAJOR.

**What would settle it**

A corpus/object class containing single-sign inscriptions, with fish and non-fish isolation rates compared.

---

## 9. The three-slot semantic interpretation has not been tested against rival templates

**Quoted passage**

> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

and:

> “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics…”

**Defect / limitation**

The positional structure is real within the corpus, but the classifier/title/name semantics are not established.

**Severity**

CRITICAL.

**What would settle it**

Explicit rival templates with discriminating predictions, fit to the same corpus under the same scoring rules.

---

## 10. Whole-inscription grammar matching is weak compared with sign-level positional regularity

**Quoted passage**

> “Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).”

and:

> “It is not comparable to Phase-133’s figures, which measured how well the grammar pattern matched whole inscriptions: full match 5.1% of seals and partial match 38.4%, together 43.5%.”

**Defect / limitation**

The headline “three-slot grammar” is strongest at sign-position level, not at whole-inscription level.

**Severity**

MAJOR.

**What would settle it**

A transparent whole-inscription grammar evaluation against rival grammars and shuffled/null baselines.

---

## 11. Vowel harmony remains unresolved

**Quoted passage**

> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”

and:

> “We therefore withdraw the earlier description of V12 as a settled methodology artifact: vowel harmony is an open problem for the reading set…”

**Defect / limitation**

The reading set has an unresolved internal phonological problem.

**Severity**

MAJOR.

**What would settle it**

Freeze one V12 protocol, publish it, rerun it on the current 161-sign set, and report sign-level failures.

---

## 12. The phonotactic violation rate is high and concentrated in headline signs

**Quoted passage**

> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

and:

> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**Defect / limitation**

The phonotactic problem is not confined to rare marginal readings; it hits central signs.

**Severity**

CRITICAL.

**What would settle it**

A sign-level explanation and correction, or an externally justified phonotactic model showing these are not violations.

---

## 13. The phonological exclusivity test does not establish Dravidian exclusivity

**Quoted passage**

> “The test’s recorded verdict is INCONCLUSIVE…”

and:

> “This test does not establish Dravidian exclusivity.”

and:

> “the readings tested were themselves chosen from Dravidian sources (DEDR), so an absence of Sanskrit-only sounds in them is partly built into how they were selected.”

**Defect / limitation**

The test cannot independently discriminate Dravidian from Sanskrit/other baselines.

**Severity**

MAJOR.

**What would settle it**

A blinded comparison using matched candidate sets from multiple language families and pre-specified phonological diagnostics.

---

## 14. Text-mining evidence is unbenchmarked and not fully reproducible

**Quoted passage**

> “No new direct M-number reading assignments for the LOW set were found by this pipeline. That is a null result for this search method only: its recall has never been measured against a hand-checked list of known proposals…”

and, from the AI disclosure:

> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**Defect / limitation**

Literature-mining counts cannot be treated as reliable exhaustive scholarship surveys.

**Severity**

MAJOR.

**What would settle it**

Archive OCR sources, prompts, models, search terms, coding rules, and benchmark recall/precision against a hand-coded gold set.

---

## 15. The Gulf fish-sign extension provides no confirmation

**Quoted passage**

> “That text search found no mention of an isolated fish sign — and, to be precise about what a text search can show, no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits).”

and:

> “the Gulf material provides no counterexample to the Holdat count, but it does not independently confirm it.”

**Defect / limitation**

The Gulf extension cannot support the fish-sign pattern; it found no fish-sign mentions at all.

**Severity**

MINOR.

**What would settle it**

Direct image/catalog inspection with listed seal IDs and sign identifications.

---

# C. Positives — claims/numbers I checked and can honestly confirm from the printed paper

1. **Site counts sum correctly.**  
   Mohenjo-daro 606 + Harappa 492 + Kalibangan 110 + Dholavira 106 + Lothal 124 + Chanhu-daro 78 + Surkotada 61 + Banawali 60 + Rakhigarhi 33 = **1,670**.

2. **Confidence sign counts sum correctly.**  
   75 HIGH + 86 MEDIUM + 236 LOW = **397** catalogue signs.

3. **Token category counts sum correctly.**  
   4,925 HIGH + 1,444 MEDIUM including provisional + 633 LOW = **7,002** tokens.

4. **Headline H+M coverage recomputes.**  
   6,369 / 7,002 = **90.96%**.

5. **Without four provisional signs recomputes.**  
   6,354 / 7,002 = **90.75%**.

6. **Seal coverage recomputes.**  
   1,165 / 1,670 = **69.76%**, printed as 69.8%.

7. **The z-score recomputes from printed inputs.**  
   (0.9916 − 0.4385) / 0.05347 = **10.344**, printed as z = 10.3.

8. **The held-out positional agreement recomputes.**  
   85 / 87 = **97.7%**.

9. **The held-out split percentages recompute.**  
   1,176 / 1,670 = **70.4%** and 494 / 1,670 = **29.6%**.

10. **M267 motif counts sum to 400.**  
    147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

11. **M267 positional counts sum to 400 and the medial rate is correct.**  
    324 + 59 + 17 = **400**; 324 / 400 = **81.0%**.

12. **Fish-bearing site counts sum to 113.**  
    6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

13. **Parpola HIGH overlap percentage recomputes.**  
    44 / 75 = **58.67%**, printed as 59%.

14. **Tamil-Brahmi terminal comparison percentage recomputes.**  
    4 / 7 = **57.1%**, printed as 57%.

15. **Phase-168 blocker hypothetical coverage recomputes.**  
    6,369 + 97 = **6,466**; 6,466 / 7,002 = **92.35%**.

16. **Appendix B token total recomputes.**  
    Sixteen signs at frequency 5 = 80; two signs at frequency 6 = 12; total = **92**.

17. **Current phonological marker update recomputes.**  
    35 / 161 = **21.7%**.

18. **The M342·M176 PMI is plausible from printed inputs.**  
    With no single-sign inscriptions, total bigram tokens = 7,002 − 1,670 = 5,332. Pair share = 122/5,332. Sign marginals = 584/7,002 and 356/7,002.  
    log₂[(122/5,332) / ((584/7,002)(356/7,002))] ≈ **2.43**, matching the printed PMI.

19. **The paper is unusually explicit about several serious limitations.**  
    It plainly states no public corpus, no bilingual, uncalibrated confidence labels, unrecorded DEDR search space, SA failure, non-independent tests, unresolved V12, 23.4% V07 violations, and lack of formal rival-language comparison.

CALL-META pass4: finish_reason=stop; max_completion_tokens=48000; completion_tokens=9660; prompt_tokens=30414; output_chars=24421.
