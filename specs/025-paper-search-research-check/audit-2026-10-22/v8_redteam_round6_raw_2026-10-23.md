# Glossa Lab Indus Preprint v8 — Red-Team Round 6: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 121,394 chars, SHA-256 of PDF 969c45d8da58a110371fabdf48875641a466eb20daacec0a78b65efb3b2c7a1f), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs. Each finding was briefed to carry a kind label: (i) a defect in what the paper says, or (ii) a limitation the paper itself already discloses at the same strength.

## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## Findings

### 1. DEDR-count accounting is internally impossible
**Kind: (i)**

**(a) Quoted passage(s)**  
> “A DEDR citation is recorded in that table for 15 of the 161 signs; the other 146 rows carry no DEDR entry in the table, and their support is of the other kinds stated row by row in the table’s Basis column. No claim is made that every reading carries a DEDR citation.”

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv.”

> “All four upgrades have DEDR backing and Proto-Dravidian phonotactic validity”

**(b) Defect**  
These statements cannot all be true as written. If 43 MEDIUM signs carry “SA+DEDR,” and four provisional signs “have DEDR backing,” then the paper cannot also say that only 15 of the 161 H+M rows have DEDR citations and that the other 146 have support “of the other kinds.” The printed paper itself lists DEDR numbers for at least 20 distinct sign rows: 11 in the selected HIGH table, 5 Phase-128/129 anchors, and 4 provisional sibilant signs. This is not a rounding issue; it is contradictory evidence accounting.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
Publish/reconcile the anchor table and audit schema: define whether “DEDR citation,” “DEDR match,” “DEDR-backed,” and “SA+DEDR evidence type” are the same or different fields; give the actual count of signs with each; correct the 15/146 statement or the 43 SA+DEDR statement.

---

### 2. Repository/commit identification is self-contradictory
**Kind: (i)**

**(a) Quoted passage**  
> “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 88a6bf46).”

> “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand: the first sentence of this section there names a92c53aa, the commit the round-4 revision started from, where this draft names ba5b4bf9.”

**(b) Defect**  
The section gives three different commit identifiers: `88a6bf46`, `a92c53aa`, and `ba5b4bf9`. Worse, it says “this draft names ba5b4bf9,” but the draft in hand actually names `88a6bf46`. This breaks the paper’s own mechanism for identifying the exact text and artifacts.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
Replace §6 with one coherent repository statement: one branch, one frozen paper-text commit, one artifact commit if different, and an explicit diff statement that is true for the current draft.

---

### 3. Conclusion overstates Proto-Dravidian discrimination relative to the paper’s own limitation section
**Kind: (i)**

**(a) Quoted passage(s)**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

**(b) Defect**  
The conclusion says the evidence “favours” Proto-Dravidian. The limitation section says the model is not yet discriminative and is only “merely compatible with Proto-Dravidian” until formal baselines are run. “Favours” is stronger than “compatible” and stronger than the body warrants.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Either run and report formal comparative tests against Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan, and language-neutral baselines, or revise the conclusion to “compatible with a Proto-Dravidian framework under the tested assumptions.”

---

### 4. “Tier 2 = probable” is stronger than the paper’s own evidence calibration permits
**Kind: (i)**

**(a) Quoted passage(s)**  
> “Tier 2 means a probable linguistic interpretation — supported, not proven”

> “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”

> “The readings have not yet been externally reviewed.”

**(b) Defect**  
The paper explicitly says no numerical probability or error rate attaches to the labels, yet the conclusion defines Tier 2 as “probable.” That is a probability-strength verdict without calibration. The caveat “supported, not proven” does not fix the misuse of “probable.”

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Calibrate the labels against known scripts or blinded expert validation, or remove “probable” and use non-probabilistic wording such as “model-supported candidate interpretation.”

---

### 5. Missing reference for Parpola 1975
**Kind: (i)**

**(a) Quoted passage**  
> “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)”

**(b) Defect**  
“Parpola 1975” is cited but no Parpola 1975 entry appears in §8. The references include Parpola 1994, Parpola 2010, and Parpola, Parpola & Brunswig 1977, but not Parpola 1975. This is a broken citation for an external-name dataset.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Add the full Parpola 1975 bibliographic entry, or correct the citation to the actual source used.

---

### 6. “Four-decade” label is numerically wrong for the cited span
**Kind: (i)**

**(a) Quoted passage(s)**  
> “Mahadevan Four-Decade Grammar Consistency (Phase-160)”

> “Mining the Mahadevan papers in this program’s text corpus (the aggregate counts ‘10 papers, 1972–2018’”

> “Across these works — one scholar’s papers over four decades”

**(b) Defect**  
1972–2018 spans 46 years and covers five calendar decades: 1970s, 1980s, 1990s, 2000s, and 2010s. Calling it “four-decade” is stale or wrong.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Change to “nearly five decades,” “1972–2018,” or “across multiple decades.”

---

### 7. §3.30 says no top-label tally is printed, but it prints one
**Kind: (i)**

**(a) Quoted passage(s)**  
> “Results: 32 total evidence items (up from 23 at Phase-141), in the Phase-169 record’s own categories: 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT.”

> “The full per-item list, with each item’s label, is in the Phase-169 record (backend/reports/phase169_master_synthesis.json); it is not printed in this paper, and no single tally at the top labels is printed, because any such tally would mix the two kinds.”

**(b) Defect**  
A top-label tally is printed immediately before the sentence saying no such tally is printed: 12 STRUCTURAL, 8 LINGUISTIC, 8 EXTERNAL, 4 DECIPHERMENT. This is a stale corrective sentence.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Delete or rewrite the “no single tally” sentence. If the intended meaning is “no pass/fail support tally,” say that.

---

### 8. Corpus-level reproducibility is blocked by the private Holdat corpus — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage(s)**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

> “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect**  
This is a real reproducibility limitation: most headline counts are corpus-level counts and cannot be independently rerun from the paper or public data. The paper discloses it plainly and repeatedly.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Public release of the Holdat corpus, or a full rerun on a public corpus with a published sign-code crosswalk and reproduced tables.

---

### 9. The z = 10.3 arithmetic checks, but the underlying permutation fit is not exactly reproducible from the paper — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage(s)**  
> “z = (0.9916 − 0.4385) / 0.05347 = 10.344, printed as 10.3.”

> “The Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

> “The z-score can therefore be checked arithmetically from the printed inputs in this section … but the fit itself can be re-run only from the script and the corpus.”

**(b) Defect**  
The printed z-score recomputes correctly, but the underlying test is not exactly reproducible from the text/record because the seed, inclusion rules, data matrix, and private corpus are not available in the paper. The paper states this at the right strength.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish the data matrix, random seed, shuffling code/inclusion rules, and corpus or a public reproducible surrogate.

---

### 10. Fish-sign isolation result is not fish-specific — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “One fact about this corpus governs what the count can show: the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”

**(b) Defect**  
The “0 isolated fish signs” result is tautological given the corpus has no single-sign inscriptions at all. It cannot support a fish-specific rule. The paper discloses this plainly.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Run the test on a corpus or object class containing single-sign inscriptions, so fish signs have an actual opportunity to occur isolated.

---

### 11. Fish supplement contains a non-family sign in a fish-family context list — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “The supplemental file fish_sign_compound_context.csv lists 27 compound occurrences with their contexts (13 for M047 and 14 for M001; M001 is not in the family list printed above, and that mismatch is on record and unresolved).”

**(b) Defect**  
The cited supplement apparently includes 14 contexts for M001 even though M001 is not in the printed fish-family list. That is a concrete data/supplement mismatch. The paper discloses it explicitly.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Correct the supplement or correct the fish-family definition, then state whether the 27 rows are fish-family rows or a mixed contextual file.

---

### 12. SA machinery failed its own held-out test; SA-derived MEDIUM support remains uncalibrated — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage(s)**  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect**  
A major component of MEDIUM promotion has no demonstrated discriminative value by itself, and its threshold is uncalibrated. The paper does disclose this and gives a removal bound.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
A preregistered/calibrated SA validation on known scripts, with false-positive rates, plus a current rerun showing SA discriminates target-language readings from controls.

---

### 13. DEDR search lacks recorded candidate set, rejected alternatives, and multiple-comparison control — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect**  
The DEDR evidence cannot be assigned a chance rate from the records. This is a serious evidentiary limitation, but the paper states it plainly.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
A recorded search protocol: candidate-generation rules, allowed transformations, all rejected candidates, null model, and multiple-comparison correction across signs and DEDR entries.

---

### 14. HIGH-confidence criteria cannot be independently verified sign-by-sign from the paper/audit — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**(b) Defect**  
The paper’s HIGH label is rule-defined, but the records do not expose criterion-by-criterion pass/fail evidence for individual signs. This prevents independent verification of HIGH status from the printed paper or audit file. The limitation is explicitly disclosed.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish a per-sign criterion matrix showing pass/fail values for iconographic match, distributional exclusivity, and terminal-marker evidence, with coding protocol and denominators.

---

### 15. V12 vowel harmony remains unresolved and V07 phonotactic violations hit headline signs — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage(s)**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”

> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**(b) Defect**  
The reading set has unresolved internal phonological problems, including violations concentrated in high-frequency headline signs. The paper discloses this at full strength.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Freeze one V12/V07 protocol, rerun it on the current 161-sign set, publish the per-sign violation table, and either revise readings or provide a linguistic/morphological explanation that actually accounts for the violations.

---

### 16. Shu-ilishu slot inventory contains a known bad /i/ listing — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “/i/ by the candidate signs the Phase-152 record lists — M267, M162, M336, M305, M045 — of which M305’s recorded reading, ōṭu/comitative, contains no /i/ sound; the record’s slot list is reported here as recorded, and this mismatch is one reason the test’s result is stated as inventory overlap only”

**(b) Defect**  
The test’s own listed /i/ inventory contains at least one sign whose reading does not contain /i/. The paper discloses the mismatch and downgrades the result accordingly.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Correct the Phase-152 slot list and rerun the inventory and seal-match test.

---

### 17. Iconographic enrichment test depends on an unpublished full pair list and selected test family — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “Pairs that never occur together are not in the 394, so the family of tests is selected from the data, and the pair list itself exists only in the Phase-143 record’s working outputs.”

> “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested — and it cannot be re-derived from the published files, because the full pair list is not published.”

**(b) Defect**  
The multiple-testing family is data-selected and the full set is not published, so the Bonferroni denominator cannot be independently reconstructed from the paper or supplements. The paper discloses this.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish the full 394-pair table, the complete universe of possible sign × icon pairs, all filters, expected counts, and full 2×2 statistics.

---

### 18. AI/text-mining counts are not reproducible from archived prompts/settings and have no precision/recall benchmark — correctly disclosed
**Kind: (ii)**

**(a) Quoted passage**  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

> “no benchmark of the mining pipeline’s recall or precision exists”

**(b) Defect**  
The text-mining counts and proximity hits cannot be rerun from a complete specification, and their error rates are unknown. The paper discloses this clearly.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Archive model versions, prompts, settings, OCR sources, search terms, proximity windows, adjudication rules, and benchmark the pipeline against a hand-coded gold set.

---

## Positives / arithmetic and cross-checks I could confirm

1. **Site counts sum correctly:**  
   606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = **1,670**.

2. **Catalogue arithmetic checks:**  
   M001–M416 with 19 unused numbers gives 416 − 19 = **397** catalogue signs.  
   390 attested + 7 zero-token catalogue signs = **397**.

3. **Phase-134 z-score recomputes:**  
   \[
   (0.9916 - 0.4385) / 0.05347 = 10.344
   \]  
   Printed as **z = 10.3**, correct.

4. **Permutation add-one p-value recomputes:**  
   \[
   (0+1)/(2000+1) = 1/2001 = 0.00049975
   \]  
   Printed as **0.0005**, correct.

5. **Train/test site split arithmetic checks:**  
   606 + 492 + 78 = **1,176**.  
   1,670 − 1,176 = **494**.  
   1,176/1,670 = **70.4%**, 494/1,670 = **29.6%**.

6. **Held-out agreement arithmetic checks:**  
   85/87 = **97.7%**.

7. **H+M token coverage recomputes:**  
   6,369/7,002 = **90.96%**.

8. **Seal coverage recomputes:**  
   1,165/1,670 = **69.8%**; 505/1,670 = **30.2%**.

9. **Without provisional signs recomputes:**  
   6,354/7,002 = **90.75%**.  
   161 − 4 = **157** signs.

10. **Confidence table token percentages recompute:**  
   - HIGH: 4,925/7,002 = **70.34%**  
   - MEDIUM excluding provisional: 1,429/7,002 = **20.41%**  
   - PROVISIONAL_MEDIUM: 15/7,002 = **0.21%**  
   - MEDIUM including provisional: 1,444/7,002 = **20.62%**  
   - LOW: 633/7,002 = **9.04%**

11. **Confidence-token totals sum correctly:**  
   4,925 + 1,429 + 15 + 633 = **7,002**.

12. **SA-removal bound recomputes:**  
   6,369 − 398 = **5,971**.  
   5,971/7,002 = **85.28%**.  
   161 − 43 = **118**.

13. **M267 motif counts sum correctly:**  
   147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

14. **M267 token share checks:**  
   400/7,002 = **5.71%**, printed as 5.7%.

15. **M267 positional counts sum and percentage check:**  
   324 + 59 + 17 = **400**.  
   324/400 = **81.0%**.

16. **Fish-bearing seal counts sum correctly:**  
   6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

17. **Fish table percentages are arithmetically correct:**  
   Every listed site has 0 isolated and all fish-bearing seals compound; totals 0/113 and 113/113.

18. **Bigram PMI for M342·M176 recomputes if total bigram tokens are 7,002 − 1,670 = 5,332:**  
   \[
   P(pair)=122/5332,\quad P(M342)=584/7002,\quad P(M176)=356/7002
   \]  
   \[
   \log_2\left(\frac{122/5332}{(584/7002)(356/7002)}\right)=2.43
   \]  
   The printed PMI = **2.43** checks.

19. **122 seals as corpus percentage checks:**  
   122/1,670 = **7.3%**.

20. **Iconographic enrichment percentages/checks:**  
   63/394 = **16.0%**.  
   394 × 0.05 = **19.7**, matching the stated expected uncorrected false positives.

21. **Printed chi-square values for first three iconographic rows recompute from unrounded expected counts:**  
   - M060: (20 − 2.036)² / 2.036 ≈ **158.5**  
   - M045: (24 − 2.874)² / 2.874 ≈ **155.3**  
   - M016: (23 − 2.754)² / 2.754 ≈ **148.8–148.9**

22. **Semantic-cluster table sums correctly:**  
   Clusters: 51 + 25 + 6 + 9 + 6 = **97**.  
   Seals: 845 + 446 + 145 + 135 + 99 = **1,670**.  
   Percentages recompute to **50.6%, 26.7%, 8.7%, 8.1%, 5.9%**.

23. **Polysemy permutation z-score checks:**  
   Observed 66.7% vs null mean 80.7%, SD 0.088:  
   \[
   (0.667 - 0.807)/0.088 = -1.59
   \]  
   Printed as **z = −1.6**, correct.

24. **V12 pass-rate arithmetic checks:**  
   476/632 = **75.3%**.  
   417/1,154 = **36.1%**.  
   417 + 737 = **1,154**.

25. **Tamil-Brahmi terminal comparison arithmetic checks:**  
   4/7 = **57.1%**, printed as 57%.

26. **V07 violation rate checks:**  
   270/1,154 = **23.4%**.

27. **Sibilant provisional token counts sum to the stated 15:**  
   M330 3 + M165 2 + M202 4 + M198 6 = **15**.

28. **Blocker-token arithmetic checks:**  
   Two signs at 6 tokens plus seventeen signs at 5 tokens gives 12 + 85 = **97**.  
   6,369 + 97 = **6,466**.  
   6,466/7,002 = **92.35%**.

29. **Phase-170 grammar retest percentage checks:**  
   137/147 = **93.2%**.

30. **Phase-133 full + partial match sum checks:**  
   5.1% + 38.4% = **43.5%**, as stated.

31. **Parpola overlap percentage checks:**  
   44/75 = **58.7%**, rounded to **59%**.

CALL-META pass1: finish_reason=stop; max_completion_tokens=48000; completion_tokens=13140; prompt_tokens=31311; output_chars=21606.

## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

## Findings

### 1. Stale/contradictory commit-identification text in §6
**Kind:** (i)  
**Quoted passage:**  
> “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 88a6bf46).”  
> “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand: the first sentence of this section there names a92c53aa, the commit the round-4 revision started from, where this draft names ba5b4bf9.”

**Defect:** The current draft says the named commit is `88a6bf46`, but the corrective self-description says the “draft in hand” names `ba5b4bf9`. That is false on the face of the paper. The passage is stale corrective text and directly undermines the paper’s claim that the exact text is identified by §6.

**Severity:** CRITICAL

**What would settle it:** Provide one authoritative commit hash for this exact draft, remove the obsolete `a92c53aa`/`ba5b4bf9` explanation, and show a clean diff between the manuscript text and the repository version at that commit.

---

### 2. “Exact text” claim is contradicted by admitted text mismatch
**Kind:** (i)  
**Quoted passage:**  
> “The exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.”  
> “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand…”

**Defect:** The paper first says the exact text is identified by the commit, then says the commit text differs from the draft in hand. That is not “exact text”; it is an admitted mismatch.

**Severity:** CRITICAL

**What would settle it:** Archive the exact PDF/text and supplements together under a single immutable DOI or commit, with no self-described manuscript difference.

---

### 3. Anchor-table scope is internally inconsistent: “all 397 signs” vs “all 161 HIGH/MEDIUM rows”
**Kind:** (i)  
**Quoted passage:**  
> “Sign catalogue: 390 distinct M-number signs attested in the corpus; the anchor table assigns readings to all 397 signs in the Mahadevan catalogue…”  
> “The anchor table — all 161 HIGH/MEDIUM rows, with each sign’s reading and basis, and a DEDR citation on the 15 rows that have one — is research/indus/anchor_table.csv; the full 397-sign inventory, with each sign’s status and corpus frequency, is glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv…”

**Defect:** The paper gives two incompatible descriptions of the anchor table. In §2.1 it says the anchor table assigns readings to all 397 catalogue signs. In §6 it says the anchor table is “all 161 HIGH/MEDIUM rows,” while the 397-sign inventory is a different file. Both cannot be true.

**Severity:** MAJOR

**What would settle it:** Print the actual row counts and schemas of `anchor_table.csv` and `ANCHOR_STATUS_AUDIT.csv`, and correct every section to use one consistent definition.

---

### 4. DEDR citation count is internally inconsistent with the paper’s own printed DEDR-backed signs
**Kind:** (i)  
**Quoted passage:**  
> “A DEDR citation is recorded in that table for 15 of the 161 signs; the other 146 rows carry no DEDR entry in the table…”  
> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv.”  
> “Results: M330=can PROVISIONAL_MEDIUM (DEDR 2322…); M165=cul PROVISIONAL_MEDIUM (DEDR 2700…); M202=can PROVISIONAL_MEDIUM (DEDR 2322…); M198=co PROVISIONAL_MEDIUM (DEDR 2816…)”

**Defect:** The paper says only 15 of 161 anchor-table rows have DEDR citations, but elsewhere says 43 MEDIUM signs carry SA+DEDR evidence and prints multiple additional DEDR-backed signs. From the printed tables alone, the count already exceeds 15: §3.3 prints DEDR numbers for 11 selected HIGH signs, 2 substrate MEDIUM signs, and 3 positional MEDIUM signs = 16 signs, before the 4 provisional sibilant DEDR-backed signs in §3.27, giving at least 20 printed H+M signs with DEDR numbers. The “15” count does not reconcile with the paper’s own contents.

**Severity:** MAJOR

**What would settle it:** Publish a definitive 161-row table with a DEDR field and reconcile: number of rows with DEDR citation, number with DEDR evidence type, and number with DEDR mentioned only in prose.

---

### 5. The conclusion’s “favours Proto-Dravidian” claim is stronger than the body’s own limitations
**Kind:** (i)  
**Quoted passage:**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”  
> “The present model tests Proto-Dravidian compatibility more extensively than competing baselines. A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”  
> “the evidence is consistent with a Proto-Dravidian reading framework under the tested assumptions, though Dravidian superiority over proto-Munda has not been formally quantified.”

**Defect:** The conclusion upgrades “consistent with” / “compatible with” into “favours.” The body explicitly says formal comparison against rival baselines is still necessary before the interpretation can be treated as discriminative rather than merely compatible. “Favours” is therefore stronger than the evidence section permits.

**Severity:** MAJOR

**What would settle it:** Either replace “favours” with “is compatible with,” or run and report formal comparative tests against Proto-Munda, early Indo-Aryan, Sanskrit/Indo-Aryan, and language-neutral baselines with pre-specified metrics.

---

### 6. “Tier 2 claims supported by multiple tests” overstates support for the 161 readings
**Kind:** (i)  
**Quoted passage:**  
> “The candidate Proto-Dravidian readings (161 H+M signs; 90.96% token coverage …) are Tier 2 claims supported by multiple tests.”  
> “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”  
> “On that record, SA agreement by itself carries no information about a sign’s value.”  
> “no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”  
> “the set also carries the unresolved V12 warning and the 23.4% V07 phonotactic violation rate…”

**Defect:** The conclusion’s “supported by multiple tests” label is stronger than the actual evidence: no error rates, no multiple-comparison control for DEDR matching, SA agreement failed its held-out test, V12 is unresolved, and V07 has a high violation rate concentrated in headline signs. The body supports “candidate assignments under rule-based criteria,” not “probable linguistic interpretation” at a validated Tier-2 strength.

**Severity:** MAJOR

**What would settle it:** Define Tier 2 operationally before use, report calibrated false-positive rates for HIGH/MEDIUM assignments, and show that the 161 readings survive independent expert review and rival-language baselines.

---

### 7. Appendix C reintroduces strong “Dravidian Tier 1” language without support in the paper
**Kind:** (i)  
**Quoted passage:**  
> “Items from the May 2026 suite include: - Dravidian Tier 1 lift ratio: 3.13x above null (Phase-44) - Contact zone HIGH anchors: supported within internal checks (Phase-46)…”

**Defect:** “Dravidian Tier 1 lift ratio: 3.13x above null” is not explained, defined, recomputed, or tied to the current limitations. It also clashes with the body’s repeated admission that Dravidian superiority over alternatives has not been formally quantified. This is a stale high-strength echo in an appendix.

**Severity:** MAJOR

**What would settle it:** Either remove the item or define the null, numerator, denominator, corpus, test date, and relation to current Phase-170/October-2026 results. If it is internal-only, label it as non-evidential.

---

### 8. Validation Path is mislabeled: two of three “falsification” points are admitted not to be usable tests
**Kind:** (i)  
**Quoted passage:**  
> “The candidate model is falsifiable in principle at the first of the following points. None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

**Defect:** The section is titled “Validation Path” and says the model is falsifiable at the listed points, but immediately admits: item 1 requires a future discovery, item 2 has already failed to confirm, and item 3 has no discriminating prediction. Calling this a validation/falsification path overstates what is actually available.

**Severity:** MAJOR

**What would settle it:** Rename the section to “Possible Future Tests and Completed Non-confirmatory Checks,” and provide at least one current, pre-specified, discriminating test that can actually be run.

---

### 9. Wrong or stale cross-reference for Phase-134 grammar support
**Kind:** (i)  
**Quoted passage:**  
> “The support for positional grammar in this paper rests on the Phase-134 tests (§2.3, §3.10), not on this one.”

**Defect:** §2.3 contains the Phase-134 positional tests. §3.10 is “Cross-Corpus Structural Comparisons (Phase-145 + Nair 2026)” and does not present the Phase-134 test as a result section; it only mentions it in passing. The cross-reference is stale or misleading.

**Severity:** MINOR

**What would settle it:** Replace “§2.3, §3.10” with the actual section(s) containing the Phase-134 tests, likely §2.3 only.

---

### 10. Missing reference: “Parpola 1975” is cited but not listed
**Kind:** (i)  
**Quoted passage:**  
> “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)…”

**Defect:** The references list includes “Parpola, S., Parpola, A. & Brunswig, R.H. (1977)” but no “Parpola 1975.” The citation is not resolvable from the bibliography.

**Severity:** MINOR

**What would settle it:** Add the correct Parpola 1975 reference or correct the in-text citation to the listed 1977 work.

---

### 11. The corpus-level results are not independently reproducible because the primary corpus is private
**Kind:** (ii)  
**Quoted passage:**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
> “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**Defect:** The paper’s central numerical claims depend on a private corpus. This is a real limitation, and the paper states it plainly.

**Severity:** CRITICAL

**What would settle it:** Public release of the exact Holdat corpus version used, or an escrowed/restricted reproducibility audit by independent researchers with access to the corpus and scripts.

---

### 12. No bilingual text; no reading can be final
**Kind:** (ii)  
**Quoted passage:**  
> “This study does not claim epigraphic finality…”  
> “No bilingual text: All readings remain provisional until a bilingual inscription (IVS + Sumerian, Akkadian, or Sanskrit) is discovered.”

**Defect:** The decipherment remains provisional because there is no bilingual inscription. The paper discloses this at full strength.

**Severity:** MAJOR

**What would settle it:** Discovery and analysis of a bilingual or otherwise externally anchored inscription with IVS signs and a known script/language.

---

### 13. SA simulation failed its own held-out test and has unknown false-positive behavior
**Kind:** (ii)  
**Quoted passage:**  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

**Defect:** The SA component is not validated and, by the paper’s own report, failed to discriminate held-out anchors from controls. This is severe for any reading route involving SA.

**Severity:** CRITICAL

**What would settle it:** A pre-registered validation on known scripts showing nonzero held-out recovery and discrimination from scrambled/language-control models, with calibrated error rates.

---

### 14. DEDR rebus matching lacks candidate logs and multiple-comparison control
**Kind:** (ii)  
**Quoted passage:**  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**Defect:** The DEDR matching procedure is not auditable as a search process and has no chance-match correction. The paper discloses this clearly.

**Severity:** MAJOR

**What would settle it:** A frozen DEDR-search protocol with allowed transformations, full candidate/rejection logs, and an empirical null or multiple-testing correction across signs and dictionary entries.

---

### 15. HIGH-confidence labels cannot be verified criterion-by-criterion from the paper or audit file
**Kind:** (ii)  
**Quoted passage:**  
> “The audit file records the same evidence-type pair (iconographic + distributional) for all 75 HIGH signs…”  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

**Defect:** The paper’s HIGH label is not reconstructible against its own stated criteria. This is disclosed at full strength, but it is still a major evidentiary weakness.

**Severity:** MAJOR

**What would settle it:** A sign-by-sign criterion matrix showing pass/fail for iconographic match, distributional exclusivity, and terminal-marker evidence, with denominators and coding rules.

---

### 16. Iconographic coding and motif-exclusivity criteria are not independently re-applicable
**Kind:** (ii)  
**Quoted passage:**  
> “the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record…”  
> “A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**Defect:** Iconographic/motif evidence is central to HIGH signs, but the coding protocol and reliability evidence are absent. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** A published coding manual, blinded independent coders, inter-coder agreement statistics, and full motif denominators.

---

### 17. Fish-sign isolation result is not fish-specific because the corpus has no single-sign inscriptions
**Kind:** (ii)  
**Quoted passage:**  
> “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9), so no sign of any family can occur isolated in it…”  
> “the fish count of 0 is therefore not a fish-specific result: it is the F9 fact restated for the fish family.”

**Defect:** The fish isolation count cannot support a special fish-sign rule. The paper states this plainly.

**Severity:** MAJOR

**What would settle it:** A corpus including single-sign inscriptions, with a pre-specified comparison of fish vs non-fish isolation rates by object class and site.

---

### 18. Gulf fish-sign search is not confirmation and is not reproducible from the record
**Kind:** (ii)  
**Quoted passage:**  
> “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
> “the Gulf material provides no counterexample to the Holdat count, but it does not independently confirm it.”

**Defect:** The Gulf extension is a weak text-search negative, with no reproducible query specification. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Publish search terms, OCR/text sources, context enumeration, and ideally direct image-based coding of Gulf seals.

---

### 19. M267 motif test is token-level, not seal-level
**Kind:** (ii)  
**Quoted passage:**  
> “the chi-square treats M267’s 400 tokens as independent observations, but a motif is a property of a seal, not of a token. The Phase-132 record does not state how many distinct seals the 400 tokens occur on, and no seal-level version of this test is on record, so the printed p-value should be read as a token-level result whose seal-level strength has not been measured.”

**Defect:** The reported p-value for motif independence may overstate evidence if tokens cluster within seals. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Re-run the motif association test at seal level, with one observation per seal or a clustered model.

---

### 20. Positional statistics do not establish the semantic labels “classifier/title/name”
**Kind:** (ii)  
**Quoted passage:**  
> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests…”  
> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**Defect:** The statistical result is positional regularity, not administrative grammar semantics. The paper discloses this directly.

**Severity:** MAJOR

**What would settle it:** Pre-specified rival-model comparison against owner/clan/commodity/cultic templates with discriminating predictions.

---

### 21. Phase-170 grammar retest is self-consistency by construction
**Kind:** (ii)  
**Quoted passage:**  
> “Results: 137/147 signs (93.2%) are classified by the thresholds into the positional class that is already their dominant class.”  
> “This is a self-consistency check, not an accuracy measurement… a high figure is expected by construction…”

**Defect:** The 93.2% figure should not be read as validation of grammar accuracy. The paper discloses this plainly.

**Severity:** MAJOR

**What would settle it:** Test the grammar against held-out inscriptions or rival corpora using fixed rules not defined from the same positional rates being evaluated.

---

### 22. V12 vowel harmony remains unresolved
**Kind:** (ii)  
**Quoted passage:**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”  
> “Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1%…”  
> “No one of these three procedures is currently the program’s authoritative V12 test…”

**Defect:** The reading set has an unresolved internal phonological problem with inconsistent test definitions. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Freeze one V12 protocol, document rule changes, rerun it on the current 161-sign set, and report sign-level drivers.

---

### 23. V07 phonotactic violation rate is high and concentrated in headline signs
**Kind:** (ii)  
**Quoted passage:**  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”  
> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**Defect:** Nearly a quarter of decoded seals violate the stricter phonotactic test, and the problem is concentrated in central signs rather than marginal rare signs. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Provide corrected readings, segmentation rules, or a demonstrated reason the V07 violations are false positives under a frozen phonotactic protocol.

---

### 24. Iconographic enrichment test is data-selected and partly circular for animal-derived readings
**Kind:** (ii)  
**Quoted passage:**  
> “Pairs that never occur together are not in the 394, so the family of tests is selected from the data…”  
> “The Bonferroni denominator of 394 is therefore the count of attested, filter-passing pairs — not the count of all sign × icon combinations that could have been tested…”  
> “for signs whose reading was itself suggested by the animal motif, ‘the reading matches the animal’ is circular and is not claimed here as validation.”

**Defect:** The test is not a clean independent validation of readings; the tested family is data-selected, and some reading/icon agreement is circular. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Define the full hypothesis family before looking at pair occurrence, publish all tested pairs, and separate readings derived from iconography from readings independently predicted.

---

### 25. Parpola overlap is not independent validation
**Kind:** (ii)  
**Quoted passage:**  
> “This is not independent cross-validation: Parpola’s framework guided the choice of readings (§7), so agreement with his book is partly expected by construction, and the count records appearances in his text, not a sign-by-sign check that he proposed the same reading for the same sign.”

**Defect:** The 44/75 overlap cannot validate the model independently. The paper states this clearly.

**Severity:** MAJOR

**What would settle it:** A sign-by-sign external comparison coding whether Parpola assigned the same value to the same sign, performed by independent coders.

---

### 26. Text-mining pipeline has unmeasured recall/precision and unarchived model settings
**Kind:** (ii)  
**Quoted passage:**  
> “its recall has never been measured against a hand-checked list of known proposals…”  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”  
> “no benchmark of the mining pipeline’s recall or precision exists…”

**Defect:** Literature-mining counts and proximity-based promotions cannot be independently reproduced from a complete method specification and have unknown accuracy. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Archive model versions/prompts/settings, benchmark against hand-coded gold standards, and report precision/recall.

---

### 27. Provisional sibilant promotions rest on partly unspecified OCR proximity rules
**Kind:** (ii)  
**Quoted passage:**  
> “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved.”  
> “a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign…”

**Defect:** The four PROVISIONAL_MEDIUM upgrades are based on weak, partly undocumented proximity evidence. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Hand-verify each proposed assignment in the source literature and publish exact OCR sources, search windows, and disambiguation rules.

---

### 28. Meluhhan name tests produced no discriminative match
**Kind:** (ii)  
**Quoted passage:**  
> “No seal in the corpus matched three or more of the four slots (Phase-152: candidate seals = 0).”  
> “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.”

**Defect:** The external personal-name route currently gives no discriminative support. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** A larger corpus with contextual metadata and a pre-specified name-matching algorithm that yields matches not produced by common short readings.

---

### 29. Site repertoire divergence for Rakhigarhi is based on only 33 seals
**Kind:** (ii)  
**Quoted passage:**  
> “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site, so its distinctiveness should be read as a measured difference on a small sample, not as proof that the difference is not a small-sample effect.”

**Defect:** The Rakhigarhi divergence result may be sample-size driven. The paper discloses this.

**Severity:** MINOR

**What would settle it:** More Rakhigarhi inscriptions or an analysis explicitly modeling small-sample uncertainty across all site pairs.

---

### 30. Frequency-curve evidence is uninformative for linguistic status
**Kind:** (ii)  
**Quoted passage:**  
> “Under the rule fixed before the run, that result makes the comparison UNINFORMATIVE: these measures do not separate the one certain writing system from systems that are not writing, so a close Indus fit on them is evidence neither for nor against the script being language.”

**Defect:** Zipf/Zipf–Mandelbrot-style curve fitting cannot support linguistic status under this test. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** A frequency/statistical method that demonstrably separates known writing systems from non-writing systems in pre-specified controls.

---

## Positives / checks I can honestly confirm from the printed text

1. **Corpus site counts sum correctly:**  
   606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = **1,670**.

2. **Token coverage arithmetic checks out:**  
   4,925 + 1,429 + 15 + 633 = **7,002**.  
   6,369 / 7,002 = **90.9597%**, printed as **90.96%**.  
   6,354 / 7,002 = **90.7455%**, printed as **90.75%**.

3. **Category percentages in §3.1 recompute:**  
   4,925 / 7,002 = **70.34%**.  
   1,429 / 7,002 = **20.41%**.  
   15 / 7,002 = **0.21%**.  
   1,444 / 7,002 = **20.62%**.  
   633 / 7,002 = **9.04%**.

4. **Seal coverage recomputes:**  
   1,165 / 1,670 = **69.76%**, printed as **69.8%**.  
   505 / 1,670 = **30.24%**, printed as **30.2%**.

5. **SA-removal bound recomputes:**  
   6,369 − 398 = **5,971**.  
   5,971 / 7,002 = **85.28%**.  
   161 − 43 = **118**.

6. **Phase-134 z-score recomputes from printed inputs:**  
   (0.9916 − 0.4385) / 0.05347 = **10.344**, printed as **10.3**.

7. **Permutation add-one p-value recomputes:**  
   (0 + 1) / (2,000 + 1) = **0.00049975**, printed as **0.0005**.

8. **F7 held-out agreement recomputes:**  
   85 / 87 = **97.70%**, printed as **97.7%**.

9. **M267 motif-token counts sum correctly:**  
   147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

10. **M267 positional percentage recomputes:**  
   324 / 400 = **81.0%**.

11. **M267 corpus-token share recomputes:**  
   400 / 7,002 = **5.71%**, printed as **5.7%**.

12. **Fish-bearing site counts sum correctly:**  
   6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

13. **M342·M176 PMI is consistent with the printed definition if bigram tokens are 7,002 − 1,670 = 5,332:**  
   Pair share = 122 / 5,332.  
   Marginals = (584 / 7,002) × (356 / 7,002).  
   log2 ratio ≈ **2.43**, matching the paper.

14. **V12 figures recompute:**  
   476 / 632 = **75.3%**.  
   417 / 1,154 = **36.1%**.  
   417 + 737 = **1,154**.

15. **Tamil-Brahmi terminal comparison recomputes:**  
   4 / 7 = **57.1%**, printed as **57%**.

16. **V07 violation rate recomputes:**  
   270 / 1,154 = **23.4%**.

17. **Blocker hypothetical coverage recomputes:**  
   6,369 + 97 = **6,466**.  
   6,466 / 7,002 = **92.35%**.

18. **Appendix B token total recomputes:**  
   Two signs at 6 tokens = 12; sixteen signs at 5 tokens = 80; total = **92**.

19. **Phase-169 category total recomputes:**  
   12 + 8 + 8 + 4 = **32**.

20. **The paper repeatedly and explicitly discloses many of its severe limitations rather than hiding them:** private corpus, no bilingual, uncalibrated confidence labels, failed SA held-out test, unresolved V12, V07 violations, non-independent Parpola overlap, non-confirmatory Gulf search, and absence of formal rival-language baselines.

CALL-META pass2: finish_reason=stop; max_completion_tokens=48000; completion_tokens=12182; prompt_tokens=31320; output_chars=28954.

## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

## Adverse findings — methods & reproducibility audit

### 1. §6 commit pinning is self-contradictory and stale

**Kind:** (i)  
**Severity:** CRITICAL

**(a) Quoted passage**

> “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 88a6bf46).”

and:

> “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand: the first sentence of this section there names a92c53aa, the commit the round-4 revision started from, where this draft names ba5b4bf9.”

**(b) Defect**

The paper names **three different commit strings** for the same pinning story: `88a6bf46`, `a92c53aa`, and `ba5b4bf9`. The first sentence of §6 in the paper actually names `88a6bf46`, not `ba5b4bf9`. The sentence claiming “where this draft names ba5b4bf9” is literally false relative to the provided text.

This destroys the claimed exact-text reproducibility pin. The title page also depends on §6:

> “The DOI identifies this preprint and its version record on Zenodo; the exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.”

But §6 does not identify the text coherently.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

Print one unambiguous immutable commit hash for the exact draft text, remove stale commit strings, and archive the exact PDF/source bundle at Zenodo or another immutable archive. The checked-out commit must contain the same §6 text it claims to contain, or the paper must explicitly identify a later pin commit as the text-bearing commit.

---

### 2. §6 describes a circular/impossible “pin commit” state

**Kind:** (i)  
**Severity:** CRITICAL

**(a) Quoted passage**

> “The commit named here is the revision commit: the commit at which this paper’s text was frozen for the current round. Commits after it on this branch add only records — the rebuilt PDF, the version note, and this pin itself — and do not change the paper’s text.”

and:

> “No other sentence differs, and the commits that follow the named commit on this branch — the pin commit, which changes only that commit string, and the records commits — change no other paper text.”

**(b) Defect**

The paper says the named commit is where the text was frozen, but also says a later “pin commit” changes the commit string in the paper text. That means the named commit cannot contain the final pinned text. A commit cannot contain a self-reference to a later commit unless the later commit changed the text. The paper tries to have both: the named commit is exact, but a later commit changes the commit string.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

Use an external immutable archive or tag: e.g., “Zenodo archive X contains source/PDF Y; Git commit Z contains identical source except for no self-referential hash.” Alternatively, state plainly that the exact text is at the later pin commit and provide that hash.

---

### 3. Anchor-table scope is internally inconsistent: all 397 signs vs only 161 H/M rows

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §2.1:

> “Sign catalogue: 390 distinct M-number signs attested in the corpus; the anchor table assigns readings to all 397 signs in the Mahadevan catalogue…”

From §3.1:

> “Token counts by sign and category are recorded in ANCHOR_STATUS_AUDIT.csv in the repository, and the full anchor list is research/ indus/anchor_table.csv.”

From §6:

> “The anchor table — all 161 HIGH/MEDIUM rows, with each sign’s reading and basis, and a DEDR citation on the 15 rows that have one — is research/indus/anchor_table.csv; the full 397-sign inventory, with each sign’s status and corpus frequency, is glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv…”

**(b) Defect**

The paper gives incompatible descriptions of `research/indus/anchor_table.csv`:

- §2.1: anchor table assigns readings to **all 397 signs**.
- §3.1: anchor table is the **full anchor list**.
- §6: anchor table contains **all 161 HIGH/MEDIUM rows**.

Those are not the same file contents. This is central reproducibility metadata, not a cosmetic inconsistency.

**(c) Severity**

MAJOR.

**(d) What would settle it**

State the exact row count and schema of each file. If `anchor_table.csv` has 397 rows, say so. If it has only 161 H/M rows, revise §2.1 and §3.1. If LOW readings live elsewhere, name the file.

---

### 4. DEDR-citation count is contradicted by the paper’s own printed examples

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §1.3:

> “A DEDR citation is recorded in that table for 15 of the 161 signs; the other 146 rows carry no DEDR entry in the table…”

From §6:

> “The anchor table — all 161 HIGH/MEDIUM rows, with each sign’s reading and basis, and a DEDR citation on the 15 rows that have one…”

But §3.3 prints DEDR entries for at least 16 H/M signs:

> “M045 … 5175”  
> “M062 … 820”  
> “M073 … 2206”  
> “M176 … 135”  
> “M211 … 2173”  
> “M125 … 5407”  
> “M261 … 4988”  
> “M264 … 4394”  
> “M328 … 340”  
> “M391 … 1166”  
> “M059 … 912”  
> “M374 … 1709”  
> “M351 … 5388”  
> “M072 … 4751”  
> “M149 … 987”  
> “M185 … 4336”

§3.27 then adds four more DEDR-backed provisional signs:

> “M330=can … DEDR 2322…”  
> “M165=cul … DEDR 2700…”  
> “M202=can … DEDR 2322…”  
> “M198=co … DEDR 2816…”

§2.4 also says:

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR in ANCHOR_STATUS_AUDIT.csv.”

**(b) Defect**

The paper repeatedly says only **15** rows have DEDR citations, but the paper itself prints DEDR numbers for **at least 16** H/M signs in §3.3 alone, and more in §3.27. It also says 43 MEDIUM signs carry SA+DEDR evidence. The distinction between “DEDR match,” “DEDR citation,” and “DEDR entry in the table” is not made consistently enough to reproduce the evidence chain.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Provide a table with, for every one of the 161 H/M signs: sign, reading, confidence, evidence type, DEDR ID if any, and whether the DEDR ID is actually present in `anchor_table.csv`. Reconcile the number 15 with the printed examples or correct it.

---

### 5. §6 falsely says central tables are “not summarised by selected rows anywhere,” despite selected-row tables in the paper

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §6:

> “Both tables are the paper’s central evidence and are deliberately not summarised by selected rows anywhere in this paper: a reader who wants to check any single reading should go to the anchor table itself, at the commit named in §6, rather than to the examples in §3.3, which are illustrative only.”

But §3.3 is explicitly:

> “3.3 Selected High-Confidence Readings”

and it prints selected rows of readings. Appendix A also prints:

> “Appendix A: Summary of New Phase-128/129 Anchors”

with selected rows.

**(b) Defect**

The sentence contradicts the paper’s own structure. The paper does summarise the anchor evidence by selected rows in §3.3 and Appendix A. The caveat “examples in §3.3” does not save the prior absolute claim “not summarised by selected rows anywhere.”

**(c) Severity**

MAJOR.

**(d) What would settle it**

Replace the sentence with something literal, e.g.: “Selected illustrative rows are printed in §3.3 and Appendix A; the complete tables are only in the repository.”

---

### 6. Citation completeness failure: cited works missing from §8

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §1.1:

> “Competing hypotheses have proposed proto-Dravidian (Parpola 1994; Mahadevan 1977), protoMunda (Witzel 1999), an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected), and a non-linguistic semasiographic system (Farmer, Sproat & Witzel 2004).”

From §3.28:

> “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)…”

From §4.1:

> “The Arthaśāstra … documents Sanskrit superintendent titles of a broadly similar kind…”

**(b) Defect**

The §8 reference list contains no entry for **Jha & Rajaram 2000** and no entry for **Parpola 1975**. The reference list has:

> “Parpola, S., Parpola, A. & Brunswig, R.H. (1977). The Meluḥḥa village…”

but that is not the cited “Parpola 1975.” The Arthaśāstra claim is also unsupported by any edition, translation, or citation.

This matters especially for §3.28 because the 25-name Meluhhan matching test depends on the source list for external names.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Add complete §8 entries for Jha & Rajaram 2000, Parpola 1975, and the Arthaśāstra source used, or remove/replace the citations.

---

### 7. Reverse citation problem: §8 contains references not cited in the text

**Kind:** (i)  
**Severity:** MINOR

**(a) Quoted passage**

From §8:

> “Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”

The in-text discussion cites:

> “Rao et al. (2009, Science 324:1165)…”

and the reference list separately contains:

> “Rao, R.P.N. et al. (2009). Entropic Evidence for Linguistic Structure in the Indus Script. Science, 324(5931), 1165.”

**(b) Defect**

The PNAS “Markov model” paper appears in §8 but is not cited by title/date distinction in the text. With two Rao et al. 2009 entries, the citation is ambiguous unless the text distinguishes 2009a/2009b or names the venue.

**(c) Severity**

MINOR.

**(d) What would settle it**

Use 2009a/2009b labels or cite the PNAS paper explicitly where intended.

---

### 8. PMI worked example is not recomputable from the printed inputs

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §3.7:

> “The dominant formula backbone is M342·M176 (ay/ā·an/aṇ), which appears on 122 seals (7.3% of corpus, PMI=2.43)…”

and:

> “PMI is pointwise mutual information, in bits: 𝑃 𝑀 𝐼(𝑎, 𝑏) = log2 [𝑃 (𝑎, 𝑏)/(𝑃 (𝑎) ⋅ 𝑃 (𝑏))], where P(a, b) is the pair’s share of all bigram tokens and P(a) and P(b) are the two signs’ shares of all sign tokens…”

and:

> “For the worked example in this section: M342·M176 occurs 122 times; M342 accounts for 584 of the corpus’s 7,002 sign tokens and M176 for 356 (§3.3); the pair’s share is taken over all bigram tokens in the Phase-142 record…”

**(b) Defect**

The paper calls this a worked example but omits the denominator needed for `P(a,b)`: the total number of bigram tokens. It gives 122 pair occurrences and sign-token marginals, but not the total adjacent-pair count used in the PMI calculation. Therefore PMI=2.43 cannot be recomputed from the paper.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Print the total bigram-token denominator used for PMI, or print the exact `P(a,b)`, `P(a)`, and `P(b)` values used.

---

### 9. Phase-143 “about 43 genuinely significant” is an overclaim from subtraction of expected false positives

**Kind:** (i)  
**Severity:** MAJOR

**(a) Quoted passage**

From §3.8:

> “An adversarial recheck (Phase-149) estimates about 43 of the 63 are genuinely significant — by subtracting the roughly 20 false positives expected among 394 tests at an uncorrected 5% level, not by counting pairs at the threshold…”

**(b) Defect**

Subtracting an expected number of false positives from a selected set of 63 does not identify “about 43” pairs as “genuinely significant.” It is at best a crude excess-count heuristic under assumptions not established here. It does not supply pair-level adjusted p-values, FDR, posterior probabilities, or confidence intervals. The phrase “genuinely significant” is stronger than the method supports.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Publish the full 394-pair table with observed counts, expected counts, full 2×2 statistics, p-values, and an explicit multiple-testing procedure such as Bonferroni, Holm, or Benjamini–Hochberg. Then report the number passing that procedure.

---

### 10. The paper’s HIGH-confidence criteria are not reproducible from the paper or stated records

**Kind:** (ii)  
**Severity:** MAJOR

**(a) Quoted passage**

From §2.2:

> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.”

Also:

> “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field…”

**(b) Defect**

This is a real reproducibility limitation: the headline HIGH/MEDIUM classification cannot be independently recomputed criterion-by-criterion from the paper or audit file. The paper itself discloses this at full strength, so this is not a hidden defect.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Publish criterion-level fields for every sign: iconographic criterion pass/fail, distributional-exclusivity pass/fail with denominators, terminal-marker pass/fail with token counts, and the rule used to combine them.

---

### 11. DEDR matching lacks search-space and multiple-comparison documentation

**Kind:** (ii)  
**Severity:** MAJOR

**(a) Quoted passage**

From §2.2:

> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.”

**(b) Defect**

This is a serious method limitation: without the candidate set, allowed transformations, rejected alternatives, and multiplicity handling, chance DEDR matches cannot be assessed. The paper states this plainly, so it is kind (ii).

**(c) Severity**

MAJOR.

**(d) What would settle it**

Publish a preregistered or frozen DEDR search protocol, all candidate hits per sign, rejection reasons, and a null/multiple-comparison analysis.

---

### 12. SA model training data and scoring rule are not reconstructable

**Kind:** (ii)  
**Severity:** MAJOR

**(a) Quoted passage**

From §2.4:

> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

Also:

> “One part of the SA+DEDR criterion cannot be reconstructed from our records: the ‘consistency’ score is described in the Phase-52 lineage as the fraction of a sign’s contexts agreeing on its modal reading, but no record defines how a context is delimited, how contexts are weighted, or how ties are handled.”

**(b) Defect**

The SA component is not reproducible: training data, syllable inventory, context delimitation, weighting, and tie handling are missing. The paper discloses this explicitly, so it is kind (ii).

**(c) Severity**

MAJOR.

**(d) What would settle it**

Archive the exact training corpus, syllable inventory, preprocessing, context definition, weighting, tie-breaking rule, and code version.

---

### 13. Phase-134 headline permutation statistic cannot be exactly rerun from the record

**Kind:** (ii)  
**Severity:** MAJOR

**(a) Quoted passage**

From §2.3:

> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

Also:

> “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script…”

**(b) Defect**

The z-score arithmetic is checkable, but the underlying permutation test is not exactly reproducible from the record alone. The paper states this limitation directly.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Publish the exact script, seed, input matrix, inclusion/exclusion rules, and output for all 2,000 permutations.

---

### 14. Corpus-level reproducibility is blocked by the unavailable Holdat corpus

**Kind:** (ii)  
**Severity:** CRITICAL

**(a) Quoted passage**

From the abstract:

> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

From §6:

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

and:

> “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect**

This is the central reproducibility limitation of the paper: most headline counts depend on a private corpus. The paper discloses this repeatedly and plainly, so it is kind (ii), not a hidden defect.

**(c) Severity**

CRITICAL.

**(d) What would settle it**

Release the corpus, or provide a public corpus with a frozen crosswalk and rerun all corpus-level results on it.

---

### 15. Text-mining reproducibility is not possible from archived prompts/settings

**Kind:** (ii)  
**Severity:** MAJOR

**(a) Quoted passage**

From the AI Disclosure:

> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

Also:

> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24).”

**(b) Defect**

The text-mining pipeline cannot be rerun as performed. The output totals may be inspectable, but the procedure is not reproducible. The paper discloses this.

**(c) Severity**

MAJOR.

**(d) What would settle it**

Archive model identifiers, prompts, OCR sources, preprocessing, scripts, settings, and validation benchmarks against a hand-coded sample.

---

## Line-by-line audit of §6 data-availability / commit-pinning paragraph

1. **Quote:**  
   > “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 88a6bf46).”  
   **Audit:** Defective because the commit later conflicts with `a92c53aa` and `ba5b4bf9`. See Findings 1–2.

2. **Quote:**  
   > “The DOI named on the title page identifies this preprint and its version record on Zenodo.”  
   **Audit:** No internal contradiction found from the paper alone.

3. **Quote:**  
   > “The exact text of this draft is identified by the branch and commit named here, not by the DOI.”  
   **Audit:** Defective because the branch/commit story is internally inconsistent. See Findings 1–2.

4. **Quote:**  
   > “The supplemental files named in this paper (the anchor table, the status audit, and the CSV supplements in research/indus/supplemental/) are in the same repository at the same commit; no separate archive copy of them exists yet.”  
   **Audit:** The lack of separate archive is openly disclosed. No separate kind (i) defect from the paper alone.

5. **Quote:**  
   > “The commit named here is the revision commit: the commit at which this paper’s text was frozen for the current round.”  
   **Audit:** Defective in combination with the later claim that a following pin commit changes the commit string. See Finding 2.

6. **Quote:**  
   > “Commits after it on this branch add only records — the rebuilt PDF, the version note, and this pin itself — and do not change the paper’s text.”  
   **Audit:** Defective: “this pin itself” necessarily changes the paper text if it changes the commit string. See Finding 2.

7. **Quote:**  
   > “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand: the first sentence of this section there names a92c53aa, the commit the round-4 revision started from, where this draft names ba5b4bf9.”  
   **Audit:** Defective: this draft names `88a6bf46`, not `ba5b4bf9`. See Finding 1.

8. **Quote:**  
   > “No other sentence differs, and the commits that follow the named commit on this branch — the pin commit, which changes only that commit string, and the records commits — change no other paper text.”  
   **Audit:** Defective because it admits a later text-changing pin commit while claiming exact identification by the earlier named commit. See Finding 2.

9. **Quote:**  
   > “The anchor table — all 161 HIGH/MEDIUM rows, with each sign’s reading and basis, and a DEDR citation on the 15 rows that have one — is research/indus/anchor_table.csv; the full 397-sign inventory, with each sign’s status and corpus frequency, is glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv; per-phase results are in backend/reports/.”  
   **Audit:** Defective: contradicts §2.1/§3.1 on anchor-table scope and contradicts printed DEDR evidence counts. See Findings 3–4.

10. **Quote:**  
   > “Neither table is printed in this paper; both are in the repository, on the branch and at the commit named above.”  
   **Audit:** The repository location depends on the broken commit pin. Otherwise no independent internal contradiction.

11. **Quote:**  
   > “Both tables are the paper’s central evidence and are deliberately not summarised by selected rows anywhere in this paper: a reader who wants to check any single reading should go to the anchor table itself, at the commit named in §6, rather than to the examples in §3.3, which are illustrative only.”  
   **Audit:** Defective: §3.3 and Appendix A are selected-row summaries. See Finding 5.

12. **Quote:**  
   > “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
   **Audit:** Disclosed limitation; no contradiction found.

13. **Quote:**  
   > “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”  
   **Audit:** Disclosed limitation; see Finding 14.

14. **Quote:**  
   > “Supplemental datasets (fishsign compound-context listing, iconographic formula enrichment table, formula bigram table, and positional grammar permutation summary) are available in research/indus/supplemental/.”  
   **Audit:** Not checkable from the paper alone, but no internal contradiction beyond the broken commit pin.

---

## Positives / checks that recompute correctly from the printed text

- Site counts in §2.1 sum correctly:  
  606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = **1,670**.

- H/M token coverage in §3.1 recomputes:  
  4,925 + 1,429 + 15 = **6,369**;  
  6,369 / 7,002 = **90.958%**, printed as **90.96%**.

- LOW token share recomputes:  
  633 / 7,002 = **9.040%**, printed as **9.04%**.

- Without provisional signs:  
  6,369 − 15 = **6,354**;  
  6,354 / 7,002 = **90.746%**, printed as **90.75%**.

- SA+DEDR removal bound recomputes:  
  6,369 − 398 = **5,971**;  
  5,971 / 7,002 = **85.276%**, printed as **85.28%**.

- Phase-134 z-score arithmetic recomputes from printed inputs:  
  (0.9916 − 0.4385) / 0.05347 = **10.34**, printed as **10.3**.

- Add-one permutation estimate recomputes:  
  (0 + 1) / (2,000 + 1) = **0.00049975**, printed as **0.0005**.

- Fish-bearing seal site counts in §3.5 sum correctly:  
  6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

- M267 motif counts in §3.4 sum correctly:  
  147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

- Seal coverage in §3.6 recomputes:  
  1,165 / 1,670 = **69.76%**, printed as **69.8%**;  
  505 / 1,670 = **30.24%**, printed as **30.2%**.

- Appendix B token total recomputes: sixteen 5-token signs plus two 6-token signs = 80 + 12 = **92**.

- Phase-168 blocker hypothetical recomputes:  
  6,369 + 97 = **6,466**;  
  6,466 / 7,002 = **92.35%**.

- Parpola overlap percentage recomputes:  
  44 / 75 = **58.67%**, printed as **59%**.

CALL-META pass3: finish_reason=stop; max_completion_tokens=60000; completion_tokens=12306; prompt_tokens=31372; output_chars=24573.

## PASS 4 — HOSTILE SUMMARY

## Kind (i) defects in what the paper says

### Finding I-1 — DEDR-count contradiction inside the paper  
**Kind:** (i)  
**Quoted passage:**  
> “A DEDR citation is recorded in that table for 15 of the 161 signs; the other 146 rows carry no DEDR entry in the table” (§1.3)

But the paper itself prints more than 15 H+M readings with DEDR numbers. In §3.3 and Appendix A alone it prints DEDR entries for:  
> “M045 … 5175”  
> “M062 … 820”  
> “M073 … 2206”  
> “M176 … 135”  
> “M211 … 2173”  
> “M125 … 5407”  
> “M261 … 4988”  
> “M264 … 4394”  
> “M328 … 340”  
> “M391 … 1166”  
> “M059 … 912”  
> “M374 … 1709”  
> “M351 … 5388”  
> “M072 … 4751”  
> “M149 … 987”  
> “M185 … 4336”

And §3.27 adds four more provisional H+M DEDR-backed entries:  
> “M330=can PROVISIONAL_MEDIUM (DEDR 2322…”  
> “M165=cul PROVISIONAL_MEDIUM (DEDR 2700…”  
> “M202=can PROVISIONAL_MEDIUM (DEDR 2322…”  
> “M198=co PROVISIONAL_MEDIUM (DEDR 2816…”

**Defect:** The statement that only 15 of 161 anchor-table rows carry a DEDR citation is irreconcilable with the paper’s own printed H+M examples, which already show at least 16 non-provisional H/M DEDR-numbered rows, and 20 if the four provisional H+M rows are included. Either the anchor table count is wrong, the printed examples are not actually represented in the table as claimed, or the paper is using “DEDR citation” inconsistently without saying so.

**Severity:** MAJOR

**What would settle it:** Publish or print the 161-row anchor table with the DEDR field exactly as counted, and reconcile every printed DEDR-numbered example with the stated “15 of 161” count.

---

### Finding I-2 — §6 contains a self-referential commit-hash contradiction  
**Kind:** (i)  
**Quoted passage:**  
> “the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 88a6bf46” (§6)

Later in the same section:  
> “A reader who checks out the named commit therefore sees the paper’s text as it was frozen at that commit, with one difference from the draft in hand: the first sentence of this section there names a92c53aa, the commit the round-4 revision started from, where this draft names ba5b4bf9.”

**Defect:** The draft in hand does not name “ba5b4bf9” in the first sentence of §6; it names “88a6bf46.” This is a stale self-reference in the very section meant to identify the exact text. It makes the reproducibility pin internally incoherent.

**Severity:** MAJOR

**What would settle it:** A corrected data-availability section with one unambiguous frozen commit, plus a public archived copy of the exact paper text and tables corresponding to that commit.

---

### Finding I-3 — The HIGH-confidence rule is not actually supported by the records as described  
**Kind:** (i)  
**Quoted passage:**  
> “HIGH (75 signs): Two or more of the following evidence criteria are met.” (§2.2)

But later:  
> “The anchor table records one basis statement and one evidence-type label per sign. It does not record each §2.2 criterion as a separate pass/fail field” (§2.2)

And still later:  
> “A reader therefore cannot verify from this paper, or from the audit file, that any particular HIGH sign meets two of the three criteria in §2.2 as those criteria are worded; what can be verified is the recorded evidence-type pair.” (§2.2)

The selected HIGH table also admits:  
> “M261’s row rests substantially on the published source behind its assignment (Parpola 1994, via Phase-51) — which is not itself one of the §2.2 criteria” (§3.3)

**Defect:** The paper defines HIGH as a rule requiring two criteria, but then says the records do not record criterion-level pass/fail and that no reader can verify that any HIGH sign meets the rule as worded. It then explicitly points to a selected HIGH example whose displayed basis is not one of the stated criteria. That is not merely a limitation; it is a breakdown between the confidence label and the evidence record supporting the label.

**Severity:** CRITICAL

**What would settle it:** A criterion-by-criterion audit table for all 75 HIGH signs, with explicit pass/fail fields for the three §2.2 criteria, denominators, calculations, and source/coder evidence for iconographic and distributional claims.

---

### Finding I-4 — The conclusion’s “favours Proto-Dravidian” claim is stronger than the body permits  
**Kind:** (i)  
**Quoted passage:**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.” (§5)

Also:  
> “The candidate Proto-Dravidian readings … are Tier 2 claims supported by multiple tests.” (§5)

But the paper’s own limitations say:  
> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” (§4.4)

And:  
> “a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS” (§4.4)

And the SA test says:  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.” (§2.4)

**Defect:** The conclusion still says the evidence “favours” Proto-Dravidian, but the body says the model is not discriminative against Proto-Munda, early Indo-Aryan, or language-neutral baselines; one comparison found Dravidian and Sanskrit equal; and the SA machinery failed against Sanskrit and scrambled controls. “Compatible with Proto-Dravidian” is supported by the disclosed body. “Favours” is a stronger headline echo.

**Severity:** CRITICAL

**What would settle it:** A pre-specified, blinded, quantitative comparison against Proto-Dravidian, Proto-Munda, early Indo-Aryan/Sanskrit, and language-neutral models using identical selection rules and held-out evaluation.

---

### Finding I-5 — “Falsifiable” is overstated relative to the paper’s actual validation path  
**Kind:** (i)  
**Quoted passage:**  
Title:  
> “A Falsifiable Computational Decipherment Hypothesis…”

But §4.5 says:  
> “None of the three is an open test that can still be run on the data available today: the first requires a future discovery, the second has already been run and did not confirm the model, and the third has no discriminating prediction on record yet.”

And for the third:  
> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.” (§4.5)

**Defect:** The title/headline advertises a falsifiable computational hypothesis, but the validation section says there is no currently open discriminating test on available data, the Gulf test did not confirm the model, and the stratigraphic test has no prediction yet. “Could be falsified by a future bilingual” is generic to any decipherment proposal and does not supply an operational falsification test for this model now.

**Severity:** MAJOR

**What would settle it:** Pre-registered discriminating predictions runnable on a public corpus or on specified future finds, with failure criteria fixed before inspection.

---

### Finding I-6 — Appendix C reintroduces an undefined “Dravidian Tier 1 lift ratio” after the paper disclaims quantified superiority  
**Kind:** (i)  
**Quoted passage:**  
> “Items from the May 2026 suite include: - Dravidian Tier 1 lift ratio: 3.13x above null (Phase-44)” (Appendix C)

But the abstract says:  
> “Dravidian superiority over proto-Munda has not been formally quantified.”

And §4.4 says:  
> “The present model tests Proto-Dravidian compatibility more extensively than competing baselines.”

**Defect:** Appendix C imports an unexplained “Dravidian Tier 1 lift ratio: 3.13x above null” that is not defined in the paper, not tied to a current result, and sits in tension with the repeated disclosure that Dravidian superiority has not been formally quantified. This reads like a stale internal-validation echo surviving in an appendix.

**Severity:** MAJOR

**What would settle it:** Define “Tier 1,” define the null, print the calculation and inputs, say whether it is current or obsolete, and reconcile it with the paper’s no-quantified-superiority disclaimer—or remove it.

---

## Kind (ii) already-disclosed limitations, stated plainly by the paper

### Finding II-1 — Central corpus-level counts are not independently reproducible  
**Kind:** (ii)  
**Quoted passage:**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.” (Abstract)

Also:  
> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.” (§6)

**Defect / limitation:** The paper’s central numbers—token coverage, sign frequencies, positional rates, motif distributions, bigrams, fish counts, seal coverage—depend on a private corpus. The paper discloses this at full strength.

**Severity:** CRITICAL

**What would settle it:** Public release of the exact corpus version, or a complete replication on a public corpus with sign-code crosswalks and frozen scripts.

---

### Finding II-2 — “Coverage” is assignment coverage, not decipherment success  
**Kind:** (ii)  
**Quoted passage:**  
> “‘Coverage’ here means only that the model assigns a candidate reading to a sign; it does not mean the reading is verified.” (Abstract)

Also:  
> “assignment coverage in the sense of §2.2: the share of tokens whose sign carries a candidate reading, not a share of verified readings” (§5)

**Defect / limitation:** The headline “90.96% token coverage” does not mean 90.96% of tokens are correctly read. It means they are assigned candidate readings. The paper states this plainly.

**Severity:** CRITICAL

**What would settle it:** External validation of readings—bilingual evidence, blinded expert review, or predictive success on held-out inscriptions not used in assigning readings.

---

### Finding II-3 — DEDR rebus matching lacks a recorded search space or multiple-comparison control  
**Kind:** (ii)  
**Quoted passage:**  
> “How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded.” (§2.2)

**Defect / limitation:** The DEDR component is vulnerable to uncontrolled post-hoc matching. Because rejected candidates and allowed transformations are not recorded, false-positive rates cannot be computed. The paper discloses this directly.

**Severity:** CRITICAL

**What would settle it:** A pre-specified DEDR search protocol, full candidate/rejection logs, allowed phonological transformations, and a null model estimating chance match rates across the full sign set.

---

### Finding II-4 — The syllabic language model failed its own held-out test  
**Kind:** (ii)  
**Quoted passage:**  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.” (§2.4)

**Defect / limitation:** The SA machinery cannot currently discriminate correct readings from Sanskrit or scrambled controls. The paper states this at full force.

**Severity:** CRITICAL

**What would settle it:** A re-run with specified training data, known-script calibration, held-out accuracy above controls, and confidence intervals.

---

### Finding II-5 — The training data for the SA model cannot be reconstructed  
**Kind:** (ii)  
**Quoted passage:**  
> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.” (§2.4)

**Defect / limitation:** A language-model component central to MEDIUM promotions is not reproducible because its training data are unspecified. The paper discloses this plainly.

**Severity:** MAJOR

**What would settle it:** The exact training corpus, preprocessing, syllable inventory, model parameters, and scripts.

---

### Finding II-6 — Three-slot semantics are interpretation, not statistical output  
**Kind:** (ii)  
**Quoted passage:**  
> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests (§3.2).” (Abstract)

Also:  
> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.” (§3.2)

**Defect / limitation:** The positional regularity does not establish the administrative/guild semantics. Rival non-linguistic or semi-linguistic templates remain untested. The paper discloses this clearly.

**Severity:** CRITICAL

**What would settle it:** Formal rival-template models with predictions, fit statistics, and held-out comparisons.

---

### Finding II-7 — Whole inscriptions rarely match the full three-slot pattern  
**Kind:** (ii)  
**Quoted passage:**  
> “Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31).” (Abstract)

And §3.31:  
> “Phase-133’s figures … full match 5.1% of seals and partial match 38.4%, together 43.5%.”

**Defect / limitation:** The three-slot grammar is strong at the sign-position level, not at the whole-inscription level. Full formula coverage of actual seals is low. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** A grammar evaluation on complete inscriptions with explicit parse criteria, rival grammars, and held-out testing.

---

### Finding II-8 — Fish-sign isolation result is not fish-specific  
**Kind:** (ii)  
**Quoted passage:**  
> “the corpus contains no single-sign inscriptions of any kind (Phase-134, test F9: 0 single-sign seals in 1,670), so no sign — fish or otherwise — can be isolated in it, and the fish count of 0 is therefore not a fish-specific result” (§3.5)

**Defect / limitation:** The 0/113 fish-isolation count follows mechanically from a corpus-wide absence of single-sign inscriptions. The paper discloses this fully.

**Severity:** MAJOR

**What would settle it:** A corpus including object classes with single-sign inscriptions, with fish and non-fish isolation rates compared.

---

### Finding II-9 — Vowel harmony remains unresolved  
**Kind:** (ii)  
**Quoted passage:**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.” (§3.17)

Also:  
> “We therefore withdraw the earlier description of V12 as a settled methodology artifact: vowel harmony is an open problem for the reading set” (§3.17)

**Defect / limitation:** The reading set fails or partially fails multiple vowel-harmony procedures, and the protocol itself is unstable. The paper discloses this directly.

**Severity:** CRITICAL

**What would settle it:** Freeze one V12 protocol, document the rule changes, re-run it on the current 161-sign set, and report sign-level failures.

---

### Finding II-10 — Phonotactic violations hit headline signs  
**Kind:** (ii)  
**Quoted passage:**  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.” (§3.18)

And:  
> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.” (§3.18)

**Defect / limitation:** The phonotactic problem is not confined to rare marginal signs; it affects high-frequency signs central to the model. The paper states this plainly.

**Severity:** CRITICAL

**What would settle it:** A documented phonotactic protocol, sign-level error analysis, revised readings, and independent expert review.

---

### Finding II-11 — Proto-Dravidian is not shown to beat competing language-family baselines  
**Kind:** (ii)  
**Quoted passage:**  
> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.” (§4.4)

**Defect / limitation:** The model is at best Proto-Dravidian-compatible, not demonstrated as superior to rivals. The paper discloses this.

**Severity:** CRITICAL

**What would settle it:** Equal-footing baseline comparisons with the same scoring rules and held-out evaluation.

---

### Finding II-12 — Text-mining evidence is unvalidated and not reproducible from model/run specifications  
**Kind:** (ii)  
**Quoted passage:**  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.” (§7 AI Disclosure)

Also:  
> “no benchmark of the mining pipeline’s recall or precision exists (§3.24).” (§7 AI Disclosure)

**Defect / limitation:** Several literature-overlap and text-proximity claims rest on AI-assisted mining whose recall, precision, prompts, models, and settings are not archived. The paper discloses this.

**Severity:** MAJOR

**What would settle it:** Archived inputs, OCR versions, prompts, model versions, exact scripts, and a hand-coded benchmark for recall/precision.

---

### Finding II-13 — The Gulf fish-sign extension is not a real image/catalogue check  
**Kind:** (ii)  
**Quoted passage:**  
> “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.” (§3.19)

Also:  
> “An absence in catalogue prose is weaker evidence than inspection of the seal images, and we report it as such” (§3.19)

**Defect / limitation:** The Gulf extension is a weak text search, not a reproducible image-based or sign-based catalogue audit. The paper says this.

**Severity:** MAJOR

**What would settle it:** Image inspection or sign-by-sign catalogue coding of the Gulf seals, with search terms, contexts, and denominators published.

---

### Finding II-14 — External Meluhhan name matching gives no discriminative support  
**Kind:** (ii)  
**Quoted passage:**  
> “Effective result: NO_DISCRIMINATIVE_MATCH — consistent with Phase-164. Personal name decipherment using the current 1,670-seal corpus is not feasible.” (§3.28)

**Defect / limitation:** The attempted external-name validation fails to discriminate. The paper discloses this directly.

**Severity:** MAJOR

**What would settle it:** Larger corpus testing with fixed phonological matching rules, contextual metadata, and false-match controls.

---

### Finding II-15 — Illustrative translations are not tied to real catalogued seals  
**Kind:** (ii)  
**Quoted passage:**  
> “The three sequences below are illustrative sequences, built from the model’s readings to show how the grammar is meant to be read. They are sign-number sequences; this paper does not tie them to identified, catalogued seals, and they should not be cited as transcriptions of specific seals.” (§4.1)

**Defect / limitation:** The attractive sample translations are demonstrations of the model, not readings of identified inscriptions. The paper discloses this.

**Severity:** MINOR

**What would settle it:** Catalogued seal IDs, photographs/drawings, sign transcriptions, and independent reading attempts.

---

## Hostile summary: strongest remaining case against the headline claims

### Kind (i) defects that still directly damage the headline

1. The paper’s own DEDR accounting is internally inconsistent: it claims only 15 DEDR-cited H+M rows, while printing at least 16 non-provisional H/M DEDR-numbered examples and 20 including provisional entries. That undermines the auditability of the anchor table.

2. The exact-version claim in §6 is self-contradictory: the section says the current draft names commit `88a6bf46`, then says the current draft names `ba5b4bf9`. The reproducibility pin is therefore not reliable as written.

3. The HIGH-confidence system is structurally defective: HIGH is defined as meeting two criteria, but the paper admits the records do not allow verification that any HIGH sign meets the criteria as worded, and a selected HIGH example relies substantially on a non-criterion source.

4. The conclusion’s “favours Proto-Dravidian” language remains stronger than the body allows. The body supports compatibility under assumptions, while explicitly saying formal rival-family comparisons remain necessary and one comparison found Dravidian and Sanskrit equal.

5. The title’s “falsifiable” framing is stronger than the actual validation path: the paper itself says none of its listed validation routes is an open discriminating test runnable on present data, and one route has no discriminating prediction yet.

6. Appendix C preserves an undefined “Dravidian Tier 1 lift ratio: 3.13x above null,” despite the paper’s own disclaimer that Dravidian superiority has not been formally quantified.

### Kind (ii) disclosed limitations that still leave the headline unproven

1. The private Holdat corpus prevents independent re-running of the central corpus-level counts.

2. “90.96% coverage” is assignment coverage, not verified decipherment.

3. DEDR rebus matching has no recorded search space, rejected-candidate log, or multiple-comparison correction.

4. The SA model failed its own held-out test, with 0.000 agreement and no separation from Sanskrit or scrambled controls.

5. The semantic reading of the three positional slots as classifier/title/name is interpretation; rival templates such as owner marks, commodity marks, and clan emblems were not tested.

6. Whole-inscription grammar fit is weak: only 5.1% full matches and 38.4% partial matches in the disclosed Phase-133 check.

7. The fish-sign isolation result is not fish-specific because the corpus contains no single-sign inscriptions of any kind.

8. V12 vowel harmony is unresolved, and V07 phonotactic violations affect high-frequency headline signs.

9. Proto-Dravidian has not been shown to beat Proto-Munda, early Indo-Aryan, Sanskrit, or language-neutral baselines.

10. External-name matching and Gulf fish-sign checking do not validate the readings.

---

## Positives a hostile reader must concede

1. **The basic arithmetic for the main coverage table checks out.**  
   - 4,925 / 7,002 = 70.34%  
   - 1,429 / 7,002 = 20.41%  
   - 15 / 7,002 = 0.21%  
   - 1,444 / 7,002 = 20.62%  
   - 633 / 7,002 = 9.04%  
   - 6,369 / 7,002 = 90.96%  
   - 6,354 / 7,002 = 90.75%

2. **The z-score arithmetic printed in §2.3 recomputes.**  
   The paper gives observed R² = 0.9916, null mean = 0.4385, SD = 0.05347.  
   \[
   (0.9916 - 0.4385) / 0.05347 = 10.344
   \]  
   Printed as z = 10.3, this is arithmetically correct.

3. **The seal-coverage arithmetic checks out.**  
   1,165 / 1,670 = 69.76%, printed as 69.8%.  
   505 / 1,670 = 30.24%, printed as 30.2%.

4. **The provisional-removal arithmetic checks out.**  
   Removing 15 provisional tokens from 6,369 gives 6,354; 6,354 / 7,002 = 90.75%.

5. **The blocker hypothetical arithmetic checks out.**  
   §3.29 says 6,369 + 97 = 6,466 tokens.  
   6,466 / 7,002 = 92.35%, as printed.

6. **The paper is unusually explicit about many limitations.**  
   It plainly says the corpus is private, coverage is not verification, SA failed a held-out test, DEDR matching lacks multiple-comparison control, the fish result is not fish-specific, semantic slot labels are interpretation, rival language baselines are not yet decisive, V12 is unresolved, and V07 violations hit headline signs.

7. **The fish-isolation caveat is correctly stated in the current draft.**  
   The paper no longer presents 0/113 fish isolation as fish-specific evidence; it correctly says the result follows from the corpus having no single-sign inscriptions at all.

8. **The paper correctly withdraws or downgrades several earlier overclaims.**  
   Examples include the withdrawn M267 fish reading, withdrawn Zipf-language evidence, withdrawn V12 “methodology artifact” resolution, withdrawn broad Tamil-Brahmi 8/11 expansion, and downgraded Gulf text-search result.

9. **The M267 correction is strongly and transparently framed.**  
   The paper gives the corrected motif counts summing to 400 and explicitly notes that the chi-square is token-level and not seal-level.

10. **The current draft repeatedly distinguishes internal consistency from external validation.**  
   That distinction is essential, and the paper usually states it plainly.

CALL-META pass4: finish_reason=stop; max_completion_tokens=48000; completion_tokens=10587; prompt_tokens=31285; output_chars=25056.

