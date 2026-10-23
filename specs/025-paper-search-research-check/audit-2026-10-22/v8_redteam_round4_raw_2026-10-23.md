# Glossa Lab Indus Preprint v8 — Red-Team Round 4: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`, auth via custom.openai Secure Vault surrogate (PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin). Source text: PDF-extracted text of pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated, 111,888 chars, SHA-256 of PDF ddf71f1db2f6655c651420a7c103e0492c9325e5a0fa36d8019173206dd1934d), supplied in full in every call — no chunking. Four calls, max_completion_tokens 48000/48000/60000/48000. All four finished with finish_reason=stop; none truncated or empty. The outputs below are reproduced verbatim, unedited (each pass's trailing CALL-META line is the worker's). The attacker saw only the paper text and the attack briefs. Each finding was briefed to carry a kind label: (i) a defect in what the paper says, or (ii) a limitation the paper itself already discloses at the same strength.



## PASS 1 — INTERNAL CONSISTENCY & ARITHMETIC AUDIT

## Findings

### 1. Fish-sign “isolation test” is tautological given the paper’s own corpus statement
**Kind (i)**

**(a) Quoted passage(s)**  
Abstract:  
> “A systematic fish-sign isolation test finds 0 isolated fish signs among the 113 fish-bearing seals in the 1,670-seal corpus, across all 9 corpus sites (§3.5).”

§2.3:  
> “The corpus contains no single-sign inscriptions (Phase-134, test F9: 0 single-sign seals), so the SOLO positional class arises only as a profile category, not from one-sign texts.”

§3.5:  
> “A fish sign counts as ‘isolated’ if it is the only sign in its inscription; the count is of fishbearing seals (113), and the occurrence-by-occurrence listing is in the supplemental file fish_sign_compound_context.csv.”

**(b) Defect**  
If the corpus has **0 single-sign inscriptions of any kind**, then **no sign whatsoever** can be “isolated” under the paper’s own definition. The fish-sign result is therefore not a fish-sign-specific pattern; it is forced by the corpus-level fact that there are no one-sign inscriptions. The abstract and conclusion still present it as a meaningful fish-sign isolation result.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Report the isolation rate for all sign families and explicitly state that fish isolation is untestable in this corpus if there are no single-sign inscriptions. Alternatively, test a corpus/object class that actually contains single-sign inscriptions, or redefine “isolated” in a way not equivalent to “one-sign inscription.”

---

### 2. Conclusion overstates Proto-Dravidian support relative to the body’s own nondiscriminative framing
**Kind (i)**

**(a) Quoted passage(s)**  
§5:  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

§4.4:  
> “A formal comparison against Proto-Munda, early IndoAryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

§4.4:  
> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonologicalprofile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”

**(b) Defect**  
The conclusion says the evidence “favours” Proto-Dravidian. The limitations section says the model is not yet discriminative and is “merely compatible” until formal competing baselines are run, and the existing comparisons are mixed. “Favours” is stronger than the body supports.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Either downgrade the conclusion to “compatible with Proto-Dravidian under the tested assumptions,” or provide a formal, quantitative comparison against Proto-Munda, early Indo-Aryan, and language-neutral baselines.

---

### 3. §1.3 says blocker plausibility is not counted in §3.30, but §3.30 counts it
**Kind (i)**

**(a) Quoted passage(s)**  
§1.3 item 16:  
> “Decode-blocker plausibility check (Phase-168): the existing LOW readings of the 19 top blocking signs are phonotactically plausible. This is a methods check, not a result about the readings; the signs remain LOW, and the check is not counted among the evidence items in §3.30 (see §3.29)”

§3.30:  
> “Among the new items: Gulf seal text search (E06 — no fish-sign mentions found; no counterexample, not corroboration, §3.19), Wells 2015 mining summary (E07 — this program’s text-mining summary of Wells’s book, not a quotation and not a sign-by-sign check; the mining’s coding rules and recall were not validated, §3.23), Mahadevan grammar text-mining comparison (L07), Parpola 1994 reading overlap count, 44/75 = 59% (E08), literature extraction null (S09 — a null for this mining pipeline only, recall unmeasured, §3.24), sibilant DEDR check (L08), adversarial challenge battery (S10 — an internal battery run by this program against its own claims; the 10 challenges, their pass criteria, and the caveat attached to each of the 6 caveated survivals are in the Phase-149 record and are not summarised here): of 10 challenges, 4 survived outright and 6 survived with caveats, none failed outright (Phase-149). S10 is an internal consistency item, not an external comparison, and is counted with the internal items wherever §3.30’s counts are used, M267 chi-square motif-independence (S11), and blocker phonotactic plausibility (S12 — a plausibility check, listed for completeness; it is not evidence that the blocker readings are correct, §3.29).”

**(b) Defect**  
Direct contradiction. §1.3 says the blocker plausibility check is “not counted among the evidence items in §3.30”; §3.30 explicitly lists it as “S12” among the evidence items.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Either remove S12 from the §3.30 evidence item count and recompute the 32-item synthesis, or revise §1.3 to say it is counted only as an internal/plausibility item, not as evidence that the readings are correct.

---

### 4. Sibilant inventory count is stale or wrong for the stated “current H+M set”
**Kind (i)**

**(a) Quoted passage(s)**  
§3.16:  
> “A targeted audit of sibilant-initial Dravidian readings in the current H+M set finds 6 signs whose readings begin with a ca-/ce-/ci-/co- sound (M025=cem, M078=cēr, M066=cōḻ, M028=cōḻ, M237=ce, M118=car).”

§3.25:  
> “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 text-proximity hits in the mined literature (a hit means the proposed reading appears near the sign’s number in OCR’d text; it is not a verified assignment of that reading to that sign): M165 (‘cul’, 4 Parpola references), M330 (‘can’, 4 Parpola references), M202 (‘can’, 4 Mahadevan references), M198 (‘co’, 3 Parpola references; upgraded to PROVISIONAL_MEDIUM in Phase-166).”

§3.27:  
> “Results: M330=can PROVISIONAL_MEDIUM ... M165=cul PROVISIONAL_MEDIUM ... M202=can PROVISIONAL_MEDIUM ... M198=co PROVISIONAL_MEDIUM ...”

**(b) Defect**  
The “current H+M set” includes PROVISIONAL_MEDIUM signs, and §3.25/§3.27 add four more c-initial readings: **can, cul, can, co**. The checkable current count is therefore not 6; it is at least **10** if provisional H+M signs are included, as the paper elsewhere says they are.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
State whether §3.16 is a pre-Phase-163 count or a current 161-anchor count. If current, recount including M330, M165, M202, and M198, or explicitly exclude PROVISIONAL_MEDIUM from this inventory.

---

### 5. §3.11 changes the phonological marker definition midstream by counting c-initial additions as “Dravidian-side markers”
**Kind (i)**

**(a) Quoted passage(s)**  
§3.11:  
> “F3 redesign using phonemes that occur in Dravidian but are absent from the Sanskrit inventory used in this test (ḷ U+1E37 retroflex lateral; ṟ U+1E5F alveolar trill; ṉ U+1E49 alveolar nasal; ḻ U+1E3B retroflex approximant).”

§3.11:  
> “Note: this test was run on the 157-sign set (pre-Phase-163). The four later sibilant additions all begin with c-, which is a valid Proto-Dravidian onset (Krishnamurti 2003) but is not Dravidian-exclusive — Sanskrit also has c-initial words. Counting them, the figures would be 39/161 (24.2%) readings with Dravidian-side markers and 0/161 with Sanskrit-side markers, under the same limits just stated.”

**(b) Defect**  
The defined “Dravidian-side markers” are **ḷ, ṟ, ṉ, ḻ**. The paper then adds four **c-** readings while admitting c- is “not Dravidian-exclusive.” That is not “under the same limits”; it changes the marker set. The arithmetic 39/161 = 24.2% is fine, but the category is not.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Keep the original marker definition and report the updated exclusive-marker count on 161 signs, or define a separate “valid Proto-Dravidian onset” count that includes c- and does not call it Dravidian-exclusive.

---

### 6. Broken cross-reference for the Wells mining summary
**Kind (i)**

**(a) Quoted passage**  
§3.30:  
> “Wells 2015 mining summary (E07 — this program’s text-mining summary of Wells’s book, not a quotation and not a sign-by-sign check; the mining’s coding rules and recall were not validated, §3.23)”

**(b) Defect**  
The Wells & Fuls mining summary is in **§3.20**, not §3.23. §3.23 is the Mahadevan four-decade grammar-consistency mining section.

**(c) Severity**  
MINOR

**(d) What would settle it**  
Change the cross-reference to §3.20, or point to both §3.20 and the general mining-disclosure section if that is intended.

---

### 7. “Sole sign in a 2-sign formula” is internally incoherent wording
**Kind (i)**

**(a) Quoted passage**  
§3.18:  
> “The non-matching signs (M233=ūr, M051=pū/puḷ, M249=tii) are content nouns that appear terminally in short inscriptions, not grammatical suffixes — their terminal position is structural (sole sign in a 2sign formula) rather than morphological.”

**(b) Defect**  
A sign cannot be the “sole sign” in a “2-sign formula.” The intended meaning is probably “final sign in a 2-sign formula.”

**(c) Severity**  
MINOR

**(d) What would settle it**  
Replace “sole sign in a 2-sign formula” with “final sign in a 2-sign formula” or give the exact structural definition.

---

### 8. Some §3.8 chi-square values do not recompute from the printed rounded expected counts; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
§3.8:  
> “The unrounded expected counts are on record for the first three rows (2.036, 2.874, 2.754); for M067 and M039 the record gives the expected counts to two decimals only (1.53, 2.16), so those two 𝜒2 values do not recompute exactly from the printed table.”

**(b) Defect**  
Using the printed rounded expected counts:  
- M067: \((15 - 1.53)^2 / 1.53 = 118.6\), not 118.9.  
- M039: \((18 - 2.16)^2 / 2.16 = 116.2\), not 116.5.  

The paper already states the reason: unrounded expected counts are not printed.

**(c) Severity**  
MINOR

**(d) What would settle it**  
Print the unrounded expected counts for all five rows, or print only values recomputable from the table.

---

### 9. CISI 87.08% opening-sign figure cannot be recomputed; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
§3.10:  
> “Comparison with the CISI corpus (179 inscriptions, Parpola P-numbers, mayig digitization): the Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed, and we report it as an uncountable figure carried from that record, not as a verified result.”

**(b) Defect**  
The percentage is printed without numerator or denominator and cannot be independently recomputed from the paper. This is a real defect in auditability, but it is plainly disclosed.

**(c) Severity**  
MINOR

**(d) What would settle it**  
Provide the numerator, denominator, inclusion rule, and sign mapping used for the 87.08%.

---

### 10. DEDR matching lacks candidate-space records and multiple-comparison control; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
§2.2:  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect**  
The rebus/DEDR component is not statistically calibrated. Without the search space, transformation rules, rejected candidates, and multiplicity correction, the false-positive rate of DEDR matches cannot be computed.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Archive the full candidate-generation protocol, all rejected candidates, allowed transformations, and a null/multiple-comparison procedure across signs and DEDR entries.

---

### 11. SA model carries no demonstrated information in held-out testing; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
§2.4:  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown. And a later test inside this program (Phase-107, October 2026) put the SA machinery itself to a held-out test whose protocol, primary metric, and discrimination rule were fixed in advance in this program’s Spec 005 (specs/005-phase52-v2/spec.md), recorded in this repository before the runs; no external or public registration of that test was filed. Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

**(b) Defect**  
The SA component failed its own held-out discrimination test and has an uncalibrated threshold. This directly weakens any MEDIUM route involving SA+DEDR.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Freeze and publish the SA training data, context definition, threshold rationale, and a successful preregistered validation against a known script or a genuinely held-out anchor set.

---

### 12. Corpus-level counts cannot be independently rerun because the primary corpus is unavailable; the paper discloses this repeatedly
**Kind (ii)**

**(a) Quoted passage(s)**  
Abstract:  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

§6:  
> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing. Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**(b) Defect**  
Most headline numbers are corpus-level counts, but the corpus is private. External readers cannot fully reproduce them from the paper.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Release the Holdat corpus, or rerun all headline corpus-level results on a public corpus with a published sign-code crosswalk.

---

### 13. V12 vowel harmony and V07 phonotactic violations remain unresolved; the paper discloses this
**Kind (ii)**

**(a) Quoted passage(s)**  
§3.17:  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”

§3.17:  
> “The V12 warning therefore stands as unresolved at every strength the three versions give (pass rates 75.3%, 64.2% and 36.1%), and no reading in this paper is either cleared or condemned by V12 until one protocol is frozen and re-run on the current 161-sign set.”

§3.18:  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

§5:  
> “the set also carries the unresolved V12 warning and the 23.4% V07 phonotactic violation rate (§§3.17–3.18) — a rate concentrated in highfrequency headline signs (M328, M211, M176 and M342 drive it, §3.18), not spread over rare or doubtful readings.”

**(b) Defect**  
The reading set has an unresolved vowel-harmony warning and a substantial phonotactic violation rate concentrated in headline signs. The paper discloses this plainly.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Freeze one V12/V07 protocol, rerun it on the current 161-sign set, publish the per-sign/per-seal failures, and either revise readings or justify why the violations are acceptable under a linguistic model.

---

### 14. Phase-134 permutation test cannot be exactly rerun from the record; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
§2.3:  
> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

**(b) Defect**  
The headline z-score recomputes arithmetically from printed inputs, but the underlying permutation cannot be exactly reproduced from the record as described.

**(c) Severity**  
MINOR

**(d) What would settle it**  
Publish the exact shuffling script version, random seed, inclusion/exclusion rules, and input matrix.

---

### 15. AI/text-mining counts are not fully reproducible from archived prompts/settings; the paper discloses this
**Kind (ii)**

**(a) Quoted passage**  
AI Disclosure:  
> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect**  
Several literature-mining counts and the four PROVISIONAL_MEDIUM promotions depend on a pipeline whose recall/precision and run configuration are not archived.

**(c) Severity**  
MAJOR

**(d) What would settle it**  
Archive the exact OCR inputs, prompts, model versions, run settings, hit definitions, and a benchmark against hand-coded known examples.

---

## Positives / arithmetic I could confirm from printed inputs

1. **Site counts sum correctly:**  
606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = **1,670**.

2. **Catalogue accounting is internally consistent:**  
75 HIGH + 86 MEDIUM + 236 LOW = **397** catalogue signs; 390 attested + 7 zero-token catalogue-only signs = **397**.

3. **Headline token coverage recomputes:**  
6,369 / 7,002 = **90.958%**, printed as **90.96%**.

4. **Seal coverage recomputes:**  
1,165 / 1,670 = **69.76%**, printed as **69.8%**.  
505 / 1,670 = **30.24%**, printed as **30.2%**.

5. **Provisional removal recomputes:**  
6,369 − 15 = **6,354** tokens; 6,354 / 7,002 = **90.7455%**, printed as **90.75%**.

6. **SA+DEDR removal bound recomputes:**  
6,369 − 398 = **5,971** tokens; 5,971 / 7,002 = **85.276%**, printed as **85.28%**.  
161 − 43 = **118** signs.

7. **HIGH/MEDIUM/LOW token table recomputes:**  
4,925 + 1,429 + 15 + 633 = **7,002**.  
4,925 / 7,002 = **70.34%**.  
1,429 / 7,002 = **20.41%**.  
15 / 7,002 = **0.21%**.  
633 / 7,002 = **9.04%**.

8. **Phase-134 z-score recomputes:**  
\((0.9916 - 0.4385) / 0.05347 = 10.344\), printed as **10.3**.

9. **Held-out positional agreement recomputes:**  
85 / 87 = **97.70%**, printed as **97.7%**.  
Class subtotals also match: 64 + 5 + 15 + 3 = **87**; 64 + 5 + 13 + 3 = **85**.

10. **M267 motif counts sum correctly:**  
147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

11. **M267 positional counts sum and percentage recompute:**  
324 + 59 + 17 = **400**; 324 / 400 = **81.0%**.

12. **M267 chi-square p-value is plausible:**  
For χ² = 12.98 with 8 df, upper-tail p ≈ **0.1124**, matching the printed value.

13. **Fish-bearing site counts sum correctly:**  
6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

14. **Zero-event upper bounds are arithmetically plausible:**  
For 0/113, one-sided 95% upper bound ≈ **2.6%**.  
For 0/6, ≈ **39%**.  
For 0/3, ≈ **63%**.

15. **Parpola overlap percentage recomputes:**  
44 / 75 = **58.67%**, printed as **59%**.

16. **§3.13 permutation z-score recomputes:**  
Observed 66.7%, null mean 80.7%, SD 0.088:  
\((0.667 - 0.807) / 0.088 ≈ -1.59\), printed as **z = −1.6**.

17. **Tamil-Brahmi terminal comparison recomputes:**  
4 / 7 = **57.14%**, printed as **57%**.

18. **V07 violation percentage recomputes:**  
270 / 1,154 = **23.40%**, printed as **23.4%**.

19. **Blocker-token hypothetical coverage recomputes:**  
19 blockers: 6 + 6 + 17×5 = **97** tokens.  
6,369 + 97 = **6,466**.  
6,466 / 7,002 = **92.35%**.

20. **Appendix B token total recomputes:**  
Sixteen signs at 5 tokens plus two signs at 6 tokens = 80 + 12 = **92** tokens; 92 / 7,002 = **1.31%**.

CALL-META pass1: finish_reason=stop; max_completion_tokens=48000; completion_tokens=11750; prompt_tokens=28968; output_chars=20488.


## PASS 2 — CLAIMS-VS-EVIDENCE AUDIT

## Findings

### 1) Conclusion overstates Proto-Dravidian support as “favours” despite body saying only compatibility and non-discrimination
**Kind (i)**

**(a) Quoted passage(s)**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

Body limitation:  
> “A formal comparison against Proto-Munda, early IndoAryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”  
> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonologicalprofile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”

**(b) Defect**  
The conclusion’s “favours” is stronger than the body permits. The body explicitly says the model is not yet discriminative and that existing comparisons are mixed. “Favours Proto-Dravidian” is a comparative evidential claim; the paper itself says the necessary comparative baselines are absent.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
A preregistered or fully specified comparative test against Proto-Munda, early Indo-Aryan, and language-neutral baselines, using the same corpus, same scoring rules, and calibrated null/error rates. Otherwise the conclusion must say “compatible with Proto-Dravidian under the model’s assumptions,” not “favours.”

---

### 2) §4.2 calls two signs “Munda substrate readings” after the paper repeatedly says the Munda derivations are unestablished and not the basis of promotion
**Kind (i)**

**(a) Quoted passage(s)**  
> “Two signs (M374=kul, M351=vī, six tokens each) are assigned candidate Munda substrate readings under the model (see §3.3 for the limits of both).”

Earlier body text:  
> “In both cases the recorded basis is a Dravidian Etymological Dictionary entry (DEDR 1709 and DEDR 5388 respectively), reached through the Phase-128 re-review.”  
> “A Munda derivation was proposed for each, but no Munda source, sound correspondence, or borrowing pathway is established in our records for either, so neither promotion rests on substrate evidence.”

**(b) Defect**  
This is a stale/pre-cure echo. The paper’s corrected body says the two promotions are DEDR-backed and do **not** rest on substrate evidence. §4.2 nevertheless re-labels them as “candidate Munda substrate readings,” which is stronger and materially different.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Either provide actual Munda sources, regular sound correspondences, borrowing pathway, and an explicit promotion rule for substrate evidence; or revise §4.2 to say only that the paper has two DEDR-backed readings for which speculative Munda derivations were proposed but not established.

---

### 3) §3.11’s “39/161 Dravidian-side markers” arithmetic is inconsistent with its own marker definition
**Kind (i)**

**(a) Quoted passage(s)**  
> “F3 redesign using phonemes that occur in Dravidian but are absent from the Sanskrit inventory used in this test (ḷ U+1E37 retroflex lateral; ṟ U+1E5F alveolar trill; ṉ U+1E49 alveolar nasal; ḻ U+1E3B retroflex approximant). Results on the 157-sign H+M set: 0/157 readings contain the test’s Sanskrit-side markers …; 35/157 (22%) contain Dravidian-side markers.”

Then:  
> “The four later sibilant additions all begin with c-, which is a valid Proto-Dravidian onset (Krishnamurti 2003) but is not Dravidian-exclusive — Sanskrit also has c-initial words. Counting them, the figures would be 39/161 (24.2%) readings with Dravidian-side markers and 0/161 with Sanskrit-side markers, under the same limits just stated.”

**(b) Defect**  
The printed Dravidian-side marker list is ḷ, ṟ, ṉ, ḻ. The four additions are c-initial, and the paper explicitly says c is **not Dravidian-exclusive**. Adding four c-initial readings to the Dravidian-side marker count is therefore inconsistent with the test definition. The recomputed figure under the printed marker definition remains **35/161 = 21.7%**, not 39/161 = 24.2%, unless the marker definition is changed.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Freeze and print the exact marker inventory. If c-initial readings are to count, justify why they are “Dravidian-side markers” despite also occurring in Sanskrit; otherwise correct the sentence to 35/161.

---

### 4) §3.8’s statement about “roughly 20” expected false positives is statistically incoherent under the Bonferroni threshold it prints
**Kind (i)**

**(a) Quoted passage**  
> “We tested 394 INITIAL-sign × iconography pairs for enrichment (chi-square, one degree of freedom per pair, Bonferroni-corrected threshold 𝜒2 ≈ 14.7).”  
> “63 pairs (16%) pass the corrected threshold; an adversarial recheck (Phase-149) estimates about 43 of the 63 are robust, the rest marginal, and several expected counts are small …”  
> “‘Robust’ in the Phase-149 recheck means the pair stands at the Bonferroni threshold for 394 tests (𝜒2 ≳ 14.7); the remaining roughly 20 of the 63 are about the number of false positives and marginal pairs expected when this many pairs are tested (Phase-149, challenge C2).”

**(b) Defect**  
At a Bonferroni threshold for 394 tests at familywise α≈0.05, the expected number of false positives under the complete null is about **0.05**, not “roughly 20.” If 20 of 63 are marginal, that may be an empirical robustness classification, but it is not “about the number of false positives expected” under the stated corrected threshold.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Print the exact Phase-149 rule producing “43 robust” and “roughly 20” marginal/false-positive estimates. If “20 expected” came from an uncorrected or different threshold, say so; otherwise remove the false-positive-expectation claim.

---

### 5) HIGH-confidence rule is inconsistent with later reliance on evidence types that the paper says do not map one-to-one onto the stated criteria
**Kind (i)**

**(a) Quoted passage(s)**  
Rule:  
> “HIGH (75 signs): Two or more of the following evidence criteria are met.”  
> “- Iconographic match … - Distributional exclusivity … - Terminal marker evidence …”

Later:  
> “HIGH confidence (selected readings): HIGH is assigned when any two of the §2.2 criteria are met; it is not an iconography-only category.”  
> “In this table, most rows rest substantially on iconography or motif exclusivity, but M342 and M176 rest substantially on their terminal distributions, and M261 on a published source (Parpola 1994, via Phase-51).”  
> “The audit file records two evidence types for each of these three signs — iconographic and distributional … and that recorded pair, not any single row of this table, is the basis of their HIGH status under the two-criterion rule in §2.2.”  
> “The audit’s two types are recorded as types, not scored criterion by criterion, and they do not map one-to-one onto the three criteria named in §2.2.”

**(b) Defect**  
The paper first defines HIGH as “two or more” of three named criteria. It then admits the audit records only broad evidence-type labels that “do not map one-to-one” onto those criteria, while still using those labels to justify HIGH status. It also mentions “M261 on a published source,” but “published source” is not one of the three HIGH criteria as stated.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish a sign-by-sign criterion matrix showing, for each HIGH sign, pass/fail for each §2.2 criterion. If “published source” is a criterion, add it explicitly and define its threshold.

---

### 6) §3.18 contains an internally impossible phrase: “sole sign in a 2-sign formula”
**Kind (i)**

**(a) Quoted passage**  
> “The non-matching signs (M233=ūr, M051=pū/puḷ, M249=tii) are content nouns that appear terminally in short inscriptions, not grammatical suffixes — their terminal position is structural (sole sign in a 2sign formula) rather than morphological.”

**(b) Defect**  
A sign cannot be the “sole sign” in a “2-sign formula.” The likely intended meaning is “final sign in a 2-sign formula,” but as written it is self-contradictory.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Correct the phrase and, if relevant, give the actual formula examples/counts showing these signs occur as the final element in two-sign inscriptions.

---

### 7) §4.5 says none of three validation points can be run today, then says the second is complete
**Kind (i)**

**(a) Quoted passage**  
> “None of the three is a test that can be run on the data available today: the first requires a future discovery, the second is complete and did not confirm the model, and the third has no discriminating prediction on record yet.”

**(b) Defect**  
This sentence contradicts itself. If the second test “is complete,” then it was runnable on available data. The intended classification appears to be: first future-only, second already run and non-confirmatory, third not yet specified.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Rewrite the sentence to separate future tests from completed non-confirmatory checks.

---

### 8) §3.30 cross-reference for the Wells mining summary points to the wrong section
**Kind (i)**

**(a) Quoted passage**  
> “Wells 2015 mining summary (E07 — this program’s text-mining summary of Wells’s book, not a quotation and not a sign-by-sign check; the mining’s coding rules and recall were not validated, §3.23)”

**(b) Defect**  
The Wells section is §3.20, not §3.23. §3.23 is Mahadevan four-decade grammar consistency.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Change “§3.23” to “§3.20” or explicitly explain why §3.23 is intended.

---

### 9) §3.20 uses singular “his position” for a coauthored Wells & Fuls book
**Kind (i)**

**(a) Quoted passage**  
> “Mining Wells & Fuls (2015) The Archaeology and Epigraphy of Indus Writing (161 pages): 284 sign references, 96 Dravidian language claims, 403-reference positional analysis appendix (Appendix II). On this program’s text mining of Wells, his position is compatible with a proto-Dravidian reading and with consistent sign positional classes; we cite this as our mining summary of his book, not as a quotation.”

**(b) Defect**  
The cited work is Wells & Fuls (2015), but the paper says “his position” and “his book.” That is sloppy attribution and may misidentify the responsible authorial claim.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Use “Wells & Fuls’s position/book” if the claim is about the coauthored work, or identify which author’s position is being summarized.

---

### 10) “Decode-Blocker Statistical Analysis” is a label stronger than its own section
**Kind (i)**

**(a) Quoted passage(s)**  
Heading:  
> “3.29 Decode-Blocker Statistical Analysis (Phase-168)”

Body:  
> “Note: the planned full-corpus SA run with 161 pinned anchors could not be executed … and the statistical assessment used instead does not substitute for it: it checks plausibility (valid Dravidian initial consonants, positional consistency) and nothing more.”  
> “These 19 signs remain at LOW confidence — phonotactic plausibility is a necessary but not sufficient condition for MEDIUM promotion.”

**(b) Defect**  
The heading calls this a “Statistical Analysis,” but the section itself says the substitute check is only plausibility and “nothing more.” The heading overstates the evidential content.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
Rename the section to “Decode-Blocker Plausibility Check” or provide an actual statistical test with null model, statistic, and p-value/interval.

---

### 11) The central corpus-level results are not independently reproducible because the corpus is private
**Kind (ii)**

**(a) Quoted passage**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”  
> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”

**(b) Defect / limitation**  
This is a severe limitation, and the paper discloses it plainly. Most key claims—coverage, positional profiles, fish isolation counts, motif distributions, bigrams, KL divergences—depend on a private corpus.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
Public release of the Holdat corpus, or rerunning the full pipeline on a public corpus with a documented sign-code crosswalk and publishing all input tables.

---

### 12) The DEDR matching process has no recorded candidate universe, rejection log, transformation rules, or multiple-comparison control
**Kind (ii)**

**(a) Quoted passage**  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**(b) Defect / limitation**  
This directly undercuts the evidential value of DEDR-backed readings. The paper discloses the limitation at full strength.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
A fully specified DEDR search protocol: candidate generation rules, admissible sound transformations, rejected candidates, blinded scoring where possible, and a null/multiple-comparison analysis estimating chance match rates.

---

### 13) SA simulation failed its own held-out discrimination test; SA-supported MEDIUM readings are therefore unconfirmed
**Kind (ii)**

**(a) Quoted passage**  
> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value. MEDIUM readings whose only support is SA consistency should therefore be read as unconfirmed candidates.”

**(b) Defect / limitation**  
The paper plainly discloses that the SA machinery, one route into MEDIUM support, failed to discriminate in held-out testing.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
A successful held-out validation on known-script data or on withheld secure anchors, with predefined metrics and controls showing the Dravidian SA model performs above Sanskrit/scrambled/null baselines.

---

### 14) SA threshold, contexts, weighting, ties, and training set are not reconstructable
**Kind (ii)**

**(a) Quoted passage**  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”  
> “One part of the SA+DEDR criterion cannot be reconstructed from our records: the ‘consistency’ score is described … but no record defines how a context is delimited, how contexts are weighted, or how ties are handled.”  
> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

**(b) Defect / limitation**  
The paper discloses that the SA component is not reproducibly specified and has unknown error properties.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish the training corpus, preprocessing, syllable inventory, scoring function, context definition, tie handling, threshold calibration, and validation results.

---

### 15) Positional tests measure positions, not the semantic labels “classifier/title/name”
**Kind (ii)**

**(a) Quoted passage**  
> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests (§3.2).”  
> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**(b) Defect / limitation**  
The paper correctly discloses that the strongest positional result does not establish the semantic interpretation.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Explicit rival-model tests with discriminating predictions: administrative/guild vs owner mark vs commodity tally vs clan/cultic template, scored on held-out data or independent corpora.

---

### 16) Iconographic and exclusivity criteria cannot be reapplied from the paper alone
**Kind (ii)**

**(a) Quoted passage**  
> “Three of the criteria above are stated at the level this program’s records support and no further: the iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record … and the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table. A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**(b) Defect / limitation**  
The paper discloses that two major evidence routes are not independently codable from the paper.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
A public coding manual, blinded independent coding, inter-coder reliability, full motif denominators, and sign-by-sign criterion outcomes.

---

### 17) Phase-134 permutation statistic can be checked arithmetically but not exactly rerun from the record
**Kind (ii)**

**(a) Quoted passage**  
> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”  
> “The z-score can therefore be checked arithmetically from the printed inputs (§5), but the fit itself can be re-run only from the script and the corpus.”

**(b) Defect / limitation**  
The paper discloses that the headline z-statistic is only arithmetically checkable from printed values; exact reproducibility is blocked by missing seed/inclusion details and private corpus access.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish the corpus input matrix, random seed, shuffling code inclusion rules, and exact script version.

---

### 18) Fish-sign isolation result is corpus- and object-type-limited, not a fact about the Indus script at large
**Kind (ii)**

**(a) Quoted passage**  
> “What it establishes is a fact about this corpus — 0 isolated fish signs among its 113 fish-bearing formal stamp seals — and, because the corpus is one private collection of formal stamp seals only, not yet a fact about the Indus script at large.”  
> “That rules out a purely local, single-site habit; it does not by itself prove a scribal rule, because this corpus contains formal stamp seals only, and selection or object-type effects could produce the same pattern.”

**(b) Defect / limitation**  
The limitation is real and plainly disclosed. The result should not be generalized beyond formal stamp seals in this private corpus.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Independent image-based counts across public corpora, copper tablets, potsherds, signboards, and Gulf material, with explicit fish-family coding.

---

### 19) Gulf fish-sign search is text-search evidence only and found no fish mentions at all
**Kind (ii)**

**(a) Quoted passage**  
> “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”  
> “That text search found no mention of an isolated fish sign — and, to be precise about what a text search can show, no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits).”  
> “The Gulf material provides no counterexample to the compound-only pattern, but it does not independently confirm it.”

**(b) Defect / limitation**  
The paper discloses the Gulf extension is non-confirmatory and non-rerunnable from the record.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Image-level inspection of the Gulf seals, published catalogue IDs, sign transcriptions, search terms, and an explicit table of the 27 contexts.

---

### 20) Text-mining counts and proximity promotions are unbenchmarked and not fully reproducible
**Kind (ii)**

**(a) Quoted passage**  
> “The Phase-163 mining record does not specify the proximity window … the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded.”  
> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**(b) Defect / limitation**  
The paper discloses that several literature-mining results and four provisional upgrades rest on an unbenchmarked, partially specified pipeline.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Archive OCR inputs, search windows, prompts/models/settings, disambiguation rules, benchmark recall/precision against a hand-coded gold set, and provide hit-level evidence.

---

### 21) V12 vowel harmony is unresolved and records disagree
**Kind (ii)**

**(a) Quoted passage**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it.”  
> “Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1% … where the recorded verdict is V12_ACTIVE_CONCERN.”  
> “We therefore withdraw the earlier description of V12 as a settled methodology artifact: vowel harmony is an open problem for the reading set.”

**(b) Defect / limitation**  
The paper discloses a serious unresolved internal inconsistency in phonological evaluation.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Freeze one vowel-harmony protocol, document all rule changes, rerun on the current 161-sign set, and publish sign-level/morpheme-level failure tables.

---

### 22) V07 phonotactic violation rate is high and concentrated in headline signs
**Kind (ii)**

**(a) Quoted passage**  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”  
> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**(b) Defect / limitation**  
This is a major limitation, and the paper states it plainly. The failures are not confined to rare signs; they hit central readings.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
Publish the V07 rule, all failing forms, morphology/segmentation assumptions, and either correct the offending readings or demonstrate that the violations are artifacts under a justified protocol.

---

### 23) Grammar variance retest is self-consistency, not accuracy
**Kind (ii)**

**(a) Quoted passage**  
> “This is a self-consistency check, not an accuracy measurement: the thresholds … are applied to the same rates that define each sign’s dominant class, so a high figure is expected by construction and the check can only catch internal contradictions.”  
> “It is not comparable to Phase-133’s figures…”

**(b) Defect / limitation**  
The paper correctly discloses that the 93.2% figure is not independent validation.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Use a held-out corpus, a predefined classifier, and external labels or rival-template predictions; do not score the same positional rates used to define the classes.

---

### 24) CISI cross-corpus opening-sign percentage is explicitly uncountable
**Kind (ii)**

**(a) Quoted passage**  
> “The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere — not in the Phase-145 report and not in any other record we hold — so the percentage cannot be checked or recomputed, and we report it as an uncountable figure carried from that record, not as a verified result.”

**(b) Defect / limitation**  
The paper discloses that the 87.08% CISI figure cannot be audited.

**(c) Severity**  
**MAJOR**

**(d) What would settle it**  
Publish the numerator, denominator, inscription list, sign mappings, and class assignments.

---

### 25) Site-divergence inference is limited by Rakhigarhi’s very small sample
**Kind (ii)**

**(a) Quoted passage**  
> “Rakhigarhi has only 33 seals; resampling those 33 seals cannot add information about the site, so its distinctiveness should be read as a measured difference on a small sample, not as proof that the difference is not a small-sample effect.”

**(b) Defect / limitation**  
The paper correctly discloses that the observed Rakhigarhi divergence is fragile.

**(c) Severity**  
**MINOR**

**(d) What would settle it**  
More Rakhigarhi inscriptions and confidence intervals for all site-pair comparisons, with controls for object type and excavation/corpus composition.

---

### 26) No bilingual text; all readings remain provisional
**Kind (ii)**

**(a) Quoted passage**  
> “No bilingual text: All readings remain provisional until a bilingual inscription (IVS + Sumerian, Akkadian, or Sanskrit) is discovered. No numerical probability attaches to any individual reading; the confidence labels are rule-based categories (§2.2).”

**(b) Defect / limitation**  
This is the central undeciphered-script limitation. The paper states it directly.

**(c) Severity**  
**CRITICAL**

**(d) What would settle it**  
A genuine bilingual or otherwise externally anchored inscription allowing direct sign-value validation.

---

## Positives I checked and can confirm from the printed text

1. **Site counts sum correctly.**  
   Mohenjo-daro 606 + Harappa 492 + Kalibangan 110 + Dholavira 106 + Lothal 124 + Chanhu-daro 78 + Surkotada 61 + Banawali 60 + Rakhigarhi 33 = **1,670**.

2. **Catalogue arithmetic is internally consistent.**  
   75 HIGH + 86 MEDIUM + 236 LOW = **397** catalogue signs. The stated 390 attested + 7 zero-token catalogue-only signs = **397**.

3. **Token coverage recomputes.**  
   4,925 HIGH + 1,444 MEDIUM = 6,369 H+M tokens.  
   6,369 / 7,002 = **90.9597%**, printed as **90.96%**.  
   633 / 7,002 = **9.04%**.

4. **Provisional-medium subtraction recomputes.**  
   6,369 − 15 = 6,354.  
   6,354 / 7,002 = **90.75%**, as printed.

5. **SA+DEDR removal bound recomputes.**  
   161 − 43 = **118** signs.  
   6,369 − 398 = **5,971** tokens.  
   5,971 / 7,002 = **85.28%**, as printed.

6. **Headline z-score recomputes from printed inputs.**  
   z = (0.9916 − 0.4385) / 0.05347 = 0.5531 / 0.05347 = **10.344**, printed as **10.3**.

7. **Held-out positional agreement recomputes.**  
   85 / 87 = **97.70%**, printed as **97.7%**.  
   The class counts also sum: 64 + 5 + 15 + 3 = 87; correct matches 64 + 5 + 13 + 3 = 85.

8. **Fish-bearing site counts sum correctly.**  
   6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113** fish-bearing seals.

9. **Zero-event upper bounds are plausible.**  
   For 0/113, one-sided 95% upper bound ≈ 1 − 0.05^(1/113) = **2.6%**.  
   For 0/6, ≈ **39%**.  
   For 0/3, ≈ **63%**. These match the paper.

10. **M267 positional counts sum correctly.**  
    324 MEDIAL + 59 TERMINAL + 17 INITIAL = **400**.

11. **M267 motif counts sum correctly.**  
    147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

12. **Formula-domain table sums correctly.**  
    Clusters: 51 + 25 + 6 + 9 + 6 = **97**.  
    Seals: 845 + 446 + 145 + 135 + 99 = **1,670**.

13. **Polysemy permutation z-score recomputes.**  
    (0.667 − 0.807) / 0.088 = **−1.59**, printed as **−1.6**.

14. **V12 Phase-154 arithmetic checks.**  
    417 passing + 737 failing = **1,154** seals checked.  
    417 / 1,154 = **36.1%**.

15. **V07 rate checks.**  
    270 / 1,154 = **23.4%**.

16. **Decode-blocker hypothetical coverage checks.**  
    6,369 + 97 = **6,466** tokens.  
    6,466 / 7,002 = **92.35%**, as printed.

17. **Appendix B token total checks.**  
    Sixteen signs at 5 tokens = 80; two signs at 6 tokens = 12; total = **92** tokens, matching Appendix B.

18. **Bonferroni threshold is plausible.**  
    For 394 tests at α=0.05, per-test α ≈ 0.0001269; χ²₁ cutoff ≈ **14.7**, as printed.

CALL-META pass2: finish_reason=stop; max_completion_tokens=48000; completion_tokens=11439; prompt_tokens=28977; output_chars=29326.


## PASS 3 — METHODS & REPRODUCIBILITY AUDIT

## Findings

### 1. Fish-sign “isolation” test is structurally tautological, not fish-specific
**Kind:** (i)  
**Severity:** CRITICAL  

**Quoted passages:**  
> “The corpus contains no single-sign inscriptions (Phase-134, test F9: 0 single-sign seals), so the SOLO positional class arises only as a profile category, not from one-sign texts.”

> “A fish sign counts as ‘isolated’ if it is the only sign in its inscription…”

> “What it establishes is a fact about this corpus — 0 isolated fish signs among its 113 fish-bearing formal stamp seals…”

> “Two further structural results are stated at the strength their tests support: the fish-sign compound-only pattern in the Holdat corpus (0 isolated among 113 fish-bearing seals…”

**Defect:**  
If the entire corpus has **0 single-sign inscriptions**, then **no sign of any kind** can ever be “isolated” under the paper’s own definition. The fish-sign test therefore does not establish a fish-specific “compound-only pattern”; it merely inherits a corpus-wide exclusion. The abstract, §3.5, §3.19, Appendix C, and conclusion still present this as a meaningful fish-sign result.

**What would settle it:**  
Report the isolation rate for all signs/sign families under the same definition, include corpora/object classes that actually contain one-sign inscriptions, or redefine “isolated” in a way that is not automatically impossible in the Holdat corpus.

---

### 2. Exact-version reproducibility claim contradicts itself
**Kind:** (i)  
**Severity:** MAJOR  

**Quoted passages:**  
> “The DOI identifies this preprint and its version record on Zenodo; the exact text of this draft is identified by the repository branch and commit named in §6, not by the DOI.”

> “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository (https://github.com/BitConcepts/glossa-lab; the version of the paper you are reading is on branch preprint-v8-f2-spec068, commit 196ea0a2).”

> “A reader who checks out the named commit therefore sees the paper’s text exactly as frozen; the only sentence that differs in that checkout is this one, which there names the previous round’s commit.”

**Defect:**  
The paper says the named commit identifies the exact text, then says checking out that commit gives a text with one sentence different. That is not exact identification. This is a self-referential version-pin failure.

**What would settle it:**  
Archive the exact submitted PDF/source text with a content hash or Zenodo record, or name a commit/tag whose checked-out text is byte-identical to the submitted draft.

---

### 3. HIGH-confidence rule is not actually checkable against the printed evidence
**Kind:** (i)  
**Severity:** MAJOR  

**Quoted passages:**  
> “HIGH (75 signs): Two or more of the following evidence criteria are met.”

> “Terminal marker evidence: sign appears in >95% of cases as inscription-final…”

> “M176’s printed terminal figure — 94% of its 356 tokens inscription-final — does not by itself meet §2.2’s terminal-marker criterion (>95%); its HIGH status rests on the audit’s recorded evidence pair…”

> “The audit’s two types are recorded as types, not scored criterion by criterion, and they do not map one-to-one onto the three criteria named in §2.2.”

**Defect:**  
The stated HIGH rule requires two §2.2 criteria. The paper then admits the audit evidence does not map one-to-one onto those criteria and that at least M176 fails the printed terminal criterion. The HIGH label is therefore stronger than what the printed rule and printed evidence allow a reader to verify.

**What would settle it:**  
Publish a per-sign pass/fail matrix for every §2.2 HIGH criterion, including the exact evidence supporting M176 and any other HIGH signs whose printed evidence does not meet the stated thresholds.

---

### 4. §3.11 changes the phonological-marker definition midstream
**Kind:** (i)  
**Severity:** MAJOR  

**Quoted passages:**  
> “F3 redesign using phonemes that occur in Dravidian but are absent from the Sanskrit inventory used in this test (ḷ U+1E37 retroflex lateral; ṟ U+1E5F alveolar trill; ṉ U+1E49 alveolar nasal; ḻ U+1E3B retroflex approximant).”

> “Note: this test was run on the 157-sign set (pre-Phase-163). The four later sibilant additions all begin with c-, which is a valid Proto-Dravidian onset (Krishnamurti 2003) but is not Dravidian-exclusive — Sanskrit also has c-initial words. Counting them, the figures would be 39/161 (24.2%) readings with Dravidian-side markers…”

**Defect:**  
The test’s “Dravidian-side markers” are explicitly four non-Sanskrit phonemes: ḷ, ṟ, ṉ, ḻ. The four later additions begin with **c-**, which the paper itself says is **not Dravidian-exclusive**. They cannot simply be added to the Dravidian-side marker count under the stated definition. The printed 39/161 figure is not justified by the printed marker list.

**What would settle it:**  
Recompute the 161-sign count using the original four-marker definition, or formally redefine the marker set to include c- and rerun the Sanskrit/Dravidian contrast under that new definition.

---

### 5. Tamil-Brahmi terminal explanation contains a nonsensical positional description
**Kind:** (i)  
**Severity:** MINOR  

**Quoted passage:**  
> “The non-matching signs (M233=ūr, M051=pū/puḷ, M249=tii) are content nouns that appear terminally in short inscriptions, not grammatical suffixes — their terminal position is structural (sole sign in a 2-sign formula) rather than morphological.”

**Defect:**  
A sign cannot be the “sole sign in a 2-sign formula.” If the intended meaning is “the only content sign” or “the second sign in a two-sign formula,” the text does not say that. This is especially problematic because §2.3 states there are no one-sign inscriptions.

**What would settle it:**  
Replace the phrase with the actual structural definition and give examples/counts for the relevant terminal uses.

---

### 6. Held-out positional test lacks the split rule needed to audit leakage
**Kind:** (i)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The same Phase-134 suite also ran a held-out check (F7): positional classes fitted on 1,176 seals predicted the classes of signs on 494 held-out seals with 97.7% agreement…”

**Defect:**  
The paper gives the train/test sizes and outcome but not how the 1,176/494 split was made, whether it was random, stratified, chronological, site-balanced, seal-order based, or whether the same signs’ positional dominance was affected by leakage through preprocessing. From the paper alone, the held-out claim cannot be audited.

**What would settle it:**  
Print the split construction rule, random seed if random, seal identifiers in each split, and the exact class-fitting procedure used before looking at the held-out set.

---

### 7. Broken cross-reference for Wells mining caveat
**Kind:** (i)  
**Severity:** MINOR  

**Quoted passage:**  
> “Wells 2015 mining summary (E07 — this program’s text-mining summary of Wells’s book, not a quotation and not a sign-by-sign check; the mining’s coding rules and recall were not validated, §3.23)”

**Defect:**  
The Wells mining summary is in §3.20, not §3.23. §3.23 is the Mahadevan four-decade grammar-mining section. This is a stale/broken cross-reference.

**What would settle it:**  
Change “§3.23” to “§3.20” or move the relevant caveat.

---

### 8. Missing reference-list entries for cited works
**Kind:** (i)  
**Severity:** MAJOR  

**Quoted passages:**  
> “Competing hypotheses have proposed proto-Dravidian (Parpola 1994; Mahadevan 1977), protoMunda (Witzel 1999), an Indo-Aryan language ancestral to Sanskrit (Jha & Rajaram 2000 — widely rejected)…”

> “Expanding Phase-164 from 6 to 25 attested Ur III Meluhhan personal names (Parpola 1975; Steinkeller 1982; Potts 1994; Reade 2001; Kjaerum 1983)…”

> “For the record, the Phase-160 counts give per-paper hits for all ten papers mined: Grammar of Indus Texts (1986) 8; What Do We Know (1989) 7; Terminal Ideograms (1982) 6; Encyclopaedia (1994) 5; Place Signs (1981) 4; Akam-Puram (2011) 4; Toponyms (2018) 3; Bilingual Parallels (1972) 3; Murukan (1999) 2; Blue Neck (2008) 2.”

**Defect:**  
The reference list has no entries for **Jha & Rajaram 2000**, **Parpola 1975**, Mahadevan’s **Encyclopaedia (1994)**, **Toponyms (2018)**, **Bilingual Parallels (1972)**, **Murukan (1999)**, or **Blue Neck (2008)**. These are cited or mined as identifiable works but are not bibliographically recoverable from §8.

**What would settle it:**  
Add full §8 entries for every cited/mined work, or remove claims depending on works not bibliographically specified.

---

### 9. Reference-list entry appears uncited or mismatched
**Kind:** (i)  
**Severity:** MINOR  

**Quoted reference entry:**  
> “Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690.”

**Defect:**  
The text cites Rao et al. for the Science entropy article:  
> “Rao et al. (2009, Science 324:1165)…”

The PNAS “Markov model” entry is not clearly cited in the body. This is either an uncited reference or a missing in-text citation.

**What would settle it:**  
Either cite the PNAS paper where used or remove the unused reference.

---

### 10. Central corpus-level results are unreproducible because the corpus is private
**Kind:** (ii)  
**Severity:** CRITICAL  

**Quoted passages:**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**Defect:**  
This is a real, central reproducibility failure: most counts, rates, positional tests, collocates, motif distributions, and coverage numbers depend on a private corpus. The paper discloses this plainly, so this is not hidden, but it remains a critical limitation.

**What would settle it:**  
Public release of the Holdat corpus with sign sequences, metadata, motif labels, site labels, and object inclusion/exclusion rules; or rerunning all claims on a public corpus with a printed crosswalk.

---

### 11. Phase-134 positional statistic cannot be rerun from the paper alone
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The operative definition of this statistic — what the grammar model fits, over which observations the R² is computed, and how inscriptions of different lengths enter the fit — is the Phase-134 script… The Phase-134 JSON record reports the statistic’s inputs and outputs… but not the data matrix, and this section does not reproduce the script’s procedure. The z-score can therefore be checked arithmetically from the printed inputs (§5), but the fit itself can be re-run only from the script and the corpus.”

**Defect:**  
The paper’s headline z-score arithmetic is checkable, but the underlying statistic is not defined in the paper sufficiently to reproduce it. The paper discloses this at adequate strength.

**What would settle it:**  
Print the data matrix definition, inscription weighting rule, exact model fitted, R² formula, shuffling rule, and seed, or provide a self-contained reproducibility supplement independent of the private corpus.

---

### 12. Permutation test lacks exact rerun information
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

**Defect:**  
The paper already admits exact rerun is impossible from the recorded materials. For a headline statistic, missing seed and inclusion/shuffling rules are material.

**What would settle it:**  
Archive the exact permutation script, seed, input matrix, and inclusion/exclusion rules.

---

### 13. DEDR matching lacks a recorded search space and multiple-comparison control
**Kind:** (ii)  
**Severity:** CRITICAL  

**Quoted passage:**  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**Defect:**  
This undercuts the statistical meaning of the candidate readings. With hundreds of signs and a large dictionary, unrecorded search freedom makes chance matches unknowable. The paper discloses this clearly.

**What would settle it:**  
Define the candidate-generation rules, list all rejected candidates, preregister allowed sound correspondences, and run a null/multiple-comparison analysis.

---

### 14. SA model training set is unreconstructable
**Kind:** (ii)  
**Severity:** CRITICAL  

**Quoted passages:**  
> “No record we hold names a specific training corpus, a syllable-inventory source, or the size of the training data, so none is stated here: the SA’s training set cannot be reconstructed from this paper or from the phase records.”

> “The syllabic language model is described in this program’s records as trained on modern Tamil material, but no record names the specific corpus, the syllable-inventory source, or the size of the training data, so the training set cannot be reconstructed (§2.4).”

**Defect:**  
A model used for MEDIUM promotions has no reconstructable training data. This is fully disclosed, but it is a severe reproducibility defect.

**What would settle it:**  
Archive the training corpus, syllable inventory, preprocessing, model code, hyperparameters, random seeds, and outputs.

---

### 15. SA threshold is uncalibrated and the held-out SA test failed
**Kind:** (ii)  
**Severity:** CRITICAL  

**Quoted passage:**  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown. And a later test inside this program… Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

**Defect:**  
The paper discloses that one promotion route has no known false-positive rate and failed a held-out discrimination test. This is not hidden, but it is severe.

**What would settle it:**  
Benchmark the SA procedure on known undeciphered/deciphered-script simulations, publish calibration curves, and require SA-supported readings to pass an externally meaningful discrimination test.

---

### 16. Iconographic and exclusivity criteria cannot be reapplied from the paper
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The iconographic-match criterion has no written coding protocol, coder-blinding step, or inter-coder reliability figure on record… the lift ratio in the exclusivity criterion is computed over the corpus’s motif distribution, whose per-motif denominators are in the Phase-132 record’s working outputs rather than a published table. A reader cannot re-apply the iconographic or exclusivity criteria to a new sign from this paper alone.”

**Defect:**  
Two major evidence routes are not reproducible or auditable from the paper. The paper states this plainly.

**What would settle it:**  
Publish a coding manual, blinded independent coding, inter-coder agreement, full motif denominators, and per-sign iconographic decisions.

---

### 17. Phase-163 provisional promotions depend on incompletely specified text-proximity mining
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The Phase-163 mining record does not specify the proximity window (how near a reading must appear to a sign’s number to count as a hit), the OCR source and version for every mined text, or how ambiguous sign-number matches were resolved. The four promotions therefore rest on a count whose generating rule is only partly recorded…”

**Defect:**  
The four provisional MEDIUM promotions depend on a mining procedure that cannot be rerun or audited from the record. The paper discloses this.

**What would settle it:**  
Archive OCR sources, term lists, proximity windows, disambiguation rules, hit contexts, and a hand-coded validation set.

---

### 18. Gulf fish-sign search is not reproducible from the record
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The record names those files and the hit counts, but it does not record the search terms used, any term list, or an enumeration of the 27 Indus-script contexts, so the search cannot be re-run from the record as it stands.”

**Defect:**  
The Gulf extension is explicitly non-rerunnable from the paper/record. The paper discloses this correctly.

**What would settle it:**  
Print the exact search terms, OCR/text files, context list, catalog identifiers, and negative/positive hit logs; ideally inspect seal images rather than prose only.

---

### 19. CISI opening-sign percentage is an uncheckable carried figure
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The Phase-145 record reports 87.08% for the share of CISI inscriptions opening with an INITIAL-class sign. The number of multi-sign inscriptions behind that percentage, and the count opening with an INITIAL-class sign, are recorded nowhere… so the percentage cannot be checked or recomputed…”

**Defect:**  
The percentage lacks numerator and denominator. The paper discloses this, but the number should not function as evidence.

**What would settle it:**  
Provide numerator, denominator, inclusion rule, sign crosswalk, and the list of inscriptions counted.

---

### 20. Spec 068 comparison systems lack normal bibliographic identification in §8
**Kind:** (ii)  
**Severity:** MINOR  

**Quoted passage:**  
> “This paper gives no §8 entry and no fuller bibliographic identification for the Dering Roll source, the Mesopotamian numerical-sign table, or DAMOS (the source of the Linear B transliterations), and the Shakti corpus and the ICIT line are likewise identified only through that record.”

**Defect:**  
The paper discloses that several comparison data sources are not bibliographically identified in the reference list. That is poor scholarly reproducibility even if the repository record may identify them.

**What would settle it:**  
Add full references/URLs/access dates for Dering Roll, Mesopotamian numerical-sign data, DAMOS, Shakti, and ICIT.

---

### 21. Text-mining counts are not reproducible from prompts/settings and have no measured recall/precision
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

> “No benchmark of the mining pipeline’s recall or precision exists (§3.24).”

**Defect:**  
The mining outputs cannot be regenerated from a complete specification, and their error rates are unknown. The paper discloses this plainly.

**What would settle it:**  
Archive prompts, model versions, temperatures/settings, OCR inputs, scripts, and benchmark the pipeline against a hand-coded gold set.

---

### 22. Phase-151 confidence interval method is unnamed
**Kind:** (ii)  
**Severity:** MINOR  

**Quoted passage:**  
> “Neither the Phase-151 record nor its script names the interval method (percentile, basic, or bias-corrected), so the printed interval is reported as recorded, without a method name.”

**Defect:**  
The KL bootstrap interval cannot be interpreted precisely without knowing the interval construction. The paper discloses this.

**What would settle it:**  
Name and implement the interval method, archive the bootstrap samples, and provide code/output.

---

### 23. Phase-170 positional retest has unspecified tie/overlap handling and is self-consistency only
**Kind:** (ii)  
**Severity:** MAJOR  

**Quoted passage:**  
> “The Phase-170 record states the rules in the order TERMINAL, INITIAL, MEDIAL, else MIXED; it does not state what happens when a sign’s rates satisfy more than one threshold, and that tie/overlap handling is not on record.”

> “This is a self-consistency check, not an accuracy measurement…”

**Defect:**  
The check is not externally probative and has an unspecified decision rule for overlapping thresholds. The paper discloses both points.

**What would settle it:**  
Specify tie handling, publish all sign rates and classifications, and test the classifier on independent data or a preregistered external corpus.

---

### 24. No site-by-site coverage exists for the current 161-sign set
**Kind:** (ii)  
**Severity:** MINOR  

**Quoted passage:**  
> “No site-by-site coverage table for the 161-sign set exists: it was never computed, in this paper or in the program’s records.”

**Defect:**  
The paper’s current headline coverage cannot be examined for site concentration or unevenness. The paper discloses this.

**What would settle it:**  
Compute and publish site-by-site token coverage and seal coverage for the 161-sign set.

---

## Positives / arithmetic I checked and can confirm

1. **Token coverage arithmetic is correct.**  
   4,925 HIGH + 1,444 MEDIUM including provisional = 6,369 H+M tokens.  
   6,369 / 7,002 = 90.9626%, printed as **90.96%**.

2. **LOW token complement is correct.**  
   7,002 − 6,369 = 633.  
   633 / 7,002 = 9.0403%, printed as **9.04%**.

3. **Provisional-token arithmetic is correct.**  
   15 / 7,002 = 0.214%, printed as **0.21%**.  
   Without them: 6,369 − 15 = 6,354; 6,354 / 7,002 = 90.748%, printed as **90.75%**.

4. **SA+DEDR removal bound recomputes.**  
   6,369 − 398 = 5,971 tokens.  
   5,971 / 7,002 = 85.276%, printed as **85.28%**.  
   161 − 43 = **118 signs**.

5. **Seal coverage arithmetic is correct.**  
   1,165 / 1,670 = 69.76%, printed as **69.8%**.  
   505 / 1,670 = 30.24%, printed as **30.2%**.

6. **Site counts sum to corpus total.**  
   606 + 492 + 110 + 106 + 124 + 78 + 61 + 60 + 33 = **1,670**.

7. **Fish-bearing seal table sums correctly.**  
   6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

8. **Zero-event upper bounds are plausible.**  
   For 0/113, one-sided 95% upper bound ≈ 1 − 0.05^(1/113) = **2.6%**.  
   For 0/6, ≈ **39%**.  
   For 0/3, ≈ **63%**.

9. **Headline z-score arithmetic is correct.**  
   (0.9916 − 0.4385) / 0.05347 = 10.344, printed as **10.3**.

10. **Held-out agreement arithmetic is correct.**  
    85 / 87 = 97.70%, printed as **97.7%**.

11. **M267 motif counts sum correctly.**  
    147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

12. **M267 positional counts sum correctly.**  
    324 + 59 + 17 = **400**.

13. **M342/M176 PMI recomputes if bigram tokens are 7,002 − 1,670 = 5,332.**  
    PMI = log2[(122/5332) / ((584/7002)(356/7002))] ≈ **2.43**.

14. **Phase-168 blocker arithmetic is correct.**  
    Two signs at 6 tokens = 12; seventeen signs at 5 tokens = 85; total = **97**.  
    6,369 + 97 = 6,466.  
    6,466 / 7,002 = **92.35%**.

15. **Appendix B token total is correct.**  
    Sixteen signs at 5 tokens = 80; two signs at 6 tokens = 12; total = **92**.  
    92 / 7,002 = 1.31%.

16. **Tamil-Brahmi strict-terminal match fraction is correct.**  
    4 / 7 = 57.14%, printed as **57%**.

17. **V12 Phase-154 arithmetic is internally consistent.**  
    417 passing + 737 failing = 1,154 checked.  
    417 / 1,154 = 36.14%, printed as **36.1%**.  
    418 root violations + 319 boundary violations = 737 violations.

18. **Phase-151 site-pair count is correct.**  
    Nine sites produce 9 × 8 / 2 = **36** unordered site pairs.

CALL-META pass3: finish_reason=stop; max_completion_tokens=60000; completion_tokens=10513; prompt_tokens=28940; output_chars=24177.


## PASS 4 — HOSTILE SUMMARY

## Kind (i) defects in what the paper says

### 1. Fish-sign “isolation” result is effectively trivial under the paper’s own corpus description  
**Severity: CRITICAL**

**Quoted passage(s):**  
> “The corpus contains no single-sign inscriptions (Phase-134, test F9: 0 single-sign seals), so the SOLO positional class arises only as a profile category, not from one-sign texts.”

> “A fish sign counts as ‘isolated’ if it is the only sign in its inscription”

> “The fish sign is never isolated in the formal stamp seal corpus, at any site, including Lothal”

> “What it establishes is a fact about this corpus — 0 isolated fish signs among its 113 fish-bearing formal stamp seals”

**Defect:**  
If the corpus has **zero single-sign inscriptions**, then **no sign of any kind can be “isolated” under the paper’s own definition**. The reported fish result, “0 isolated fish signs among 113 fish-bearing seals,” is not a fish-specific pattern; it is forced by the sampling frame. The paper repeatedly treats it as a meaningful “fish-sign compound-only pattern,” but under the printed definition and the printed corpus fact it has no discriminating content.

**What would settle it:**  
Report the rate of isolated signs for **all signs** and test fish signs against that baseline, or use a corpus/object class that actually contains single-sign inscriptions. Alternatively redefine “isolated” to mean something not logically impossible in this corpus, and rerun the test.

---

### 2. The binomial confidence bounds for fish isolation are misleading because the event is structurally absent  
**Severity: MAJOR**

**Quoted passage(s):**  
> “A word on what 0 can and cannot show at these sizes. With 0 events in 113 seals, the pooled isolated rate is bounded at about 2.6% (one-sided 95% bound for zero events).”

> “The corpus contains no single-sign inscriptions (Phase-134, test F9: 0 single-sign seals)”

**Defect:**  
The paper gives binomial-style bounds as if each fish-bearing seal had an opportunity to contain an isolated fish sign. But if the corpus has no single-sign inscriptions at all, the event is not merely unobserved; it is unavailable under the corpus composition. The 2.6% upper bound is therefore not a meaningful estimate of a fish-sign isolation rate in a population that could have isolated signs.

**What would settle it:**  
Use a sampling frame where isolated inscriptions occur, or explicitly condition the statistical statement on the corpus’s exclusion/absence of single-sign inscriptions and withdraw the fish-specific rate inference.

---

### 3. Abstract-level “three-slot pattern in inscriptions” is stronger than the body’s own result  
**Severity: MAJOR**

**Quoted passage(s):**  
> “We find robust non-random positional structure (z = 10.3; no permutation in 2,000 exceeded the observed statistic …), a recurring three-slot positional pattern in inscriptions.”

> “Statistical analysis of inscription structure identifies a three-slot pattern that is consistent at the level of individual signs’ positions. Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31). ‘Consistent’ in this paper refers to the sign-level regularity unless a sentence says otherwise”

**Defect:**  
The abstract says “a recurring three-slot positional pattern in inscriptions,” but the body says full inscription-level matches are only **5.1%**, with **38.4%** partial. The body narrows the claim to **sign-level positional regularity**. The abstract echoes the claim at a stronger level than the paper’s own section supports.

**What would settle it:**  
Rewrite the abstract to say “sign-level positional regularity compatible with a three-slot model,” and include the full/partial inscription rates there or in an immediately adjacent summary.

---

### 4. “Falsifiable” headline is stronger than the actual validation path for the decipherment model  
**Severity: MAJOR**

**Quoted passage(s):**  
> “A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script”

> “The candidate model is falsifiable in principle at the first of the following points. None of the three is a test that can be run on the data available today: the first requires a future discovery, the second is complete and did not confirm the model, and the third has no discriminating prediction on record yet.”

> “No such discriminating prediction is yet on record, so this point is a direction for future work, not a falsification test of the present model.”

**Defect:**  
The title sells a “falsifiable computational decipherment hypothesis,” but the paper’s own validation section says the listed falsification points are not presently executable: one awaits a future bilingual, one was completed and did not confirm, and one lacks a discriminating prediction. That leaves the decipherment readings themselves without a current decisive falsification test.

**What would settle it:**  
State concrete, pre-registered, currently runnable predictions that distinguish this model from rival models on available data, or weaken the headline to “potentially falsifiable if future bilingual or discriminating data appear.”

---

### 5. The conclusion’s “favours Proto-Dravidian” exceeds the paper’s own comparative evidence  
**Severity: CRITICAL**

**Quoted passage(s):**  
> “Within that limit, the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”

> “Dravidian superiority over proto-Munda has not been formally quantified.”

> “A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian.”

> “For the record, the comparisons that do exist are mixed: a syllabic language-model comparison favoured Dravidian over Sanskrit on the 157-sign set (Phase-134 F12), while a phonological-profile comparison of the HIGH anchors found Dravidian and Sanskrit fits equal and rated the question AMBIGUOUS (Phase-134 F3).”

**Defect:**  
The paper’s own limitations say the model is not yet discriminative among language baselines, Dravidian superiority over Munda is unquantified, and one comparison found Dravidian and Sanskrit equal. The conclusion nevertheless says the evidence “favours” Proto-Dravidian. “Compatible with Proto-Dravidian under this model’s assumptions” would match the evidence; “favours” is stronger than the disclosed comparative basis.

**What would settle it:**  
Run a formal, parallel comparison against Proto-Dravidian, Proto-Munda, early Indo-Aryan/Sanskrit, and language-neutral models with fixed metrics and error controls. Until then, replace “favours” with “is compatible with.”

---

### 6. HIGH-confidence assignment criteria are not actually reconstructable for at least some cited HIGH examples  
**Severity: MAJOR**

**Quoted passage(s):**  
> “HIGH (75 signs): Two or more of the following evidence criteria are met.”

> “HIGH confidence (selected readings): HIGH is assigned when any two of the §2.2 criteria are met”

> “M261 on a published source (Parpola 1994, via Phase-51).”

> “The audit file records two evidence types for each of these three signs — iconographic and distributional … and that recorded pair, not any single row of this table, is the basis of their HIGH status under the two-criterion rule in §2.2.”

> “The audit’s two types are recorded as types, not scored criterion by criterion, and they do not map one-to-one onto the three criteria named in §2.2.”

**Defect:**  
The paper defines HIGH as meeting two of three explicit criteria, but then says a selected HIGH sign, M261, rests substantially on “a published source,” which is not one of the listed HIGH criteria. It further admits the audit records “evidence types,” not pass/fail results for the criteria, and that these types “do not map one-to-one” onto the criteria. The HIGH label is therefore not reconstructable from the printed rule for at least the showcased cases.

**What would settle it:**  
Publish a per-sign criterion matrix with explicit pass/fail fields for each §2.2 HIGH criterion, including M261, M176, and M342. If “published source” is a HIGH criterion, add it to §2.2 and define it.

---

### 7. The M267 motif-independence test treats token counts as independent evidence without addressing seal-level clustering  
**Severity: MAJOR**

**Quoted passage:**  
> “Its distribution across seal motifs does not differ significantly from the counts expected if its 400 tokens were spread across the nine motif types in proportion to each type’s overall share (chi-square = 12.98, p = 0.1124, 9 motif categories, 8 degrees of freedom …), which is why a motif-bound reading such as ‘fish’ fails and a grammatical-particle reading is preferred.”

**Defect:**  
The test is framed over **400 tokens**, but inscriptions are nested within seals and motif type is a seal-level attribute. Multiple occurrences and formulaic contexts can violate the independence assumption of a simple chi-square over tokens. The paper uses the p-value to prefer a grammatical-particle reading over a motif-bound reading, but it does not show a seal-level or permutation-by-seal test.

**What would settle it:**  
Redo the M267 motif test at seal level, or use a permutation/bootstrap procedure that preserves seal structure, inscription length, and within-seal token dependence.

---

### 8. Appendix B converts token frequencies into seal-blocking counts without showing that each token is on a distinct seal  
**Severity: MINOR**

**Quoted passage:**  
> “These 18 signs have corpus frequencies of 5 (sixteen signs) or 6 (M270, M386) — 92 tokens in total … Each of them blocks the 5 or 6 seals it occurs on, so together they account for at most 92 of the 505 seals not fully covered by H+M candidate readings (§3.6)”

**Defect:**  
The statement assumes token frequency equals the number of seals on which the sign occurs. That need not follow unless each sign occurs at most once per seal. The “at most 92” bound is safe, but “Each of them blocks the 5 or 6 seals it occurs on” is not demonstrated from the printed data.

**What would settle it:**  
Print seal-level occurrence counts for the 18 signs, or state explicitly that none repeats within a seal and cite the record establishing that.

---

## Kind (ii) already-disclosed limitations, stated at roughly the same strength by the paper

### 9. Corpus-level results are not independently reproducible because the corpus is private  
**Severity: CRITICAL**

**Quoted passage(s):**  
> “The corpus itself is not publicly released (see §6), so corpus-level counts cannot yet be re-run by other researchers.”

> “The corpus-level counts in this paper cannot be re-run until the corpus itself is released; that limit is stated here, not only in §6, because most of the paper’s numbers are corpus-level counts.”

> “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**Defect / limitation:**  
Most headline numbers depend on a private corpus. The paper discloses this plainly. This is still a severe limitation on verification.

**What would settle it:**  
Release the corpus or provide a public corpus crosswalk and fully rerunnable pipeline producing the same counts.

---

### 10. DEDR rebus matching has no recorded candidate universe, rejection log, or multiple-comparison control  
**Severity: CRITICAL**

**Quoted passage:**  
> “For each sign, the anchor table records only the DEDR candidate that was adopted. How many candidate readings were considered for a sign, which sound changes or reading transformations were allowed when matching, and which candidates were rejected were not recorded; and no multiple-comparison control across the roughly 390 signs and the Dravidian Etymological Dictionary was applied or recorded. A reader therefore cannot compute from our records how often a DEDR match of this quality would arise by chance.”

**Defect / limitation:**  
This directly undercuts the evidential value of many candidate readings. The paper discloses the limitation fully.

**What would settle it:**  
Publish the full search protocol, candidate lists, allowed transformations, rejected candidates, and a null model estimating chance DEDR-match rates.

---

### 11. SA support failed a held-out test and has unknown false-positive rate  
**Severity: CRITICAL**

**Quoted passage(s):**  
> “The 0.15 threshold is a working cut-off chosen by this program; it has never been calibrated against a known script, so its false-positive rate is unknown.”

> “Its agreement on held-out anchors was 0.000, and control runs using a Sanskrit model and a scrambled model could not be told apart from it. On that record, SA agreement by itself carries no information about a sign’s value.”

> “43 MEDIUM signs, accounting for 398 corpus tokens, carry the combined evidence type SA+DEDR”

**Defect / limitation:**  
SA cannot presently validate readings. The paper states this plainly and provides a bound on affected signs.

**What would settle it:**  
Calibrate SA on known scripts and show above-control held-out performance before using SA consistency as promotion evidence.

---

### 12. The HIGH/MEDIUM confidence labels have no measured error rates and are not probabilities  
**Severity: MAJOR**

**Quoted passage:**  
> “The HIGH, MEDIUM, and LOW labels are rule-based categories defined by the criteria above. They are not calibrated probabilities: no measured error rate attaches to any label.”

**Defect / limitation:**  
“Confidence” can be misread as probability or reliability. The paper explicitly warns that it is only a rule label.

**What would settle it:**  
Estimate false-positive and false-negative rates on known writing systems or via blinded expert review.

---

### 13. The semantic interpretation of the three slots is not produced by the positional statistics  
**Severity: MAJOR**

**Quoted passage(s):**  
> “The positions are measured; the reading of the three slots as classifier, title, and name/case elements of an administrative vocabulary is this model’s interpretation, not a result of the positional tests”

> “The meanings attached to the positions below are this model’s interpretation, not outputs of the statistics”

> “The pattern was tested against inscriptions with their signs shuffled; it was not tested against rival templates such as owner marks, commodity marks, or clan emblems, which could also produce fixed position patterns.”

**Defect / limitation:**  
The structural result does not establish administrative/guild semantics. The paper discloses this clearly.

**What would settle it:**  
Predefine rival templates and test discriminating predictions among them on the same corpus.

---

### 14. Whole-inscription grammar fit is weak; the strong grammar result is sign-level  
**Severity: MAJOR**

**Quoted passage:**  
> “Whole inscriptions match the full pattern less often: in the Phase-133 check, 5.1% of seals matched fully and 38.4% partially (§3.31). ‘Consistent’ in this paper refers to the sign-level regularity unless a sentence says otherwise”

**Defect / limitation:**  
The “grammar” is not a robust full-inscription parse for most seals. The paper does disclose the distinction in the body.

**What would settle it:**  
Report full-inscription parse rates prominently and compare them to rival grammars and null models.

---

### 15. Vowel harmony remains unresolved, with internally inconsistent test versions  
**Severity: MAJOR**

**Quoted passage:**  
> “The V12 vowel-harmony warning is unresolved, and our own records disagree about it. Depending on the version of the test, the pass rate is 75.3% … 64.2% … or 36.1% …”

> “No one of these three procedures is currently the program’s authoritative V12 test”

**Defect / limitation:**  
An unresolved phonological diagnostic remains against the reading set. The paper states this plainly.

**What would settle it:**  
Freeze one V12 protocol, document the rule changes, rerun it on the current 161-sign set, and publish per-sign/per-seal outputs.

---

### 16. The V07 phonotactic violation rate is high and concentrated in headline signs  
**Severity: CRITICAL**

**Quoted passage:**  
> “the V07 phonotactic violation rate under the stricter redefined test is 23.4% (270 of 1,154 decoded seals, Phase-155), concentrated in high-frequency signs.”

> “The signs driving the V07 rate are recorded in the Phase-155 record, Part C: M328 (53 violations), M211 (49), M176 (46) and M342 (45) — three of them headline signs of this model.”

**Defect / limitation:**  
A nearly one-quarter violation rate, concentrated in important signs, is a serious unresolved problem. The paper discloses it directly.

**What would settle it:**  
Explain the violations under a fixed phonotactic/morphological protocol, or revise the affected readings.

---

### 17. The reading model is not yet externally reviewed  
**Severity: MAJOR**

**Quoted passage:**  
> “The readings have not yet been externally reviewed.”

**Defect / limitation:**  
The sign readings are author/program assignments without expert adjudication. The paper states this explicitly.

**What would settle it:**  
Independent expert review of the anchor table, ideally blinded to the model’s preferred readings.

---

### 18. Text-mining evidence is unbenchmarked and not rerunnable from archived model settings  
**Severity: MAJOR**

**Quoted passage:**  
> “Those machine-produced counts were checked by the author against the phase records at the level of totals and sampled contexts, not by a full hand recount, and no benchmark of the mining pipeline’s recall or precision exists (§3.24). Model names, versions, prompts, and run settings for the mining steps were not archived with the phase records; the counts are therefore reproducible from the records’ outputs, not from a re-runnable specification.”

**Defect / limitation:**  
The literature-mining counts cannot be treated as robust external evidence. The paper discloses the weakness.

**What would settle it:**  
Archive models/prompts/settings, benchmark against hand-coded literature samples, and publish recall/precision.

---

### 19. Gulf fish-sign extension provides no confirmation  
**Severity: MAJOR**

**Quoted passage:**  
> “That text search found no mention of an isolated fish sign — and, to be precise about what a text search can show, no fish-sign mentions at all in the Laursen text (Phase-156: 0 hits).”

> “the Gulf material provides no counterexample to the compound-only pattern, but it does not independently confirm it.”

**Defect / limitation:**  
The Gulf extension adds no positive evidence. The paper states this correctly.

**What would settle it:**  
Direct image/catalog inspection of Gulf seals with enumerated fish-sign contexts, not merely text search.

---

### 20. The Phase-134 permutation statistic cannot be exactly rerun from the record alone  
**Severity: MAJOR**

**Quoted passage:**  
> “The permutation check behind z = 10.3 used 2,000 shuffled copies (§2.3); the Phase-134 record gives the count and the null moments but does not record the random seed or the shuffling code’s inclusion rules, so the permutation cannot be re-run exactly from the record.”

> “the fit itself can be re-run only from the script and the corpus.”

**Defect / limitation:**  
The arithmetic z-score is checkable, but the underlying statistic is not independently reconstructable from the paper or phase record alone. The paper discloses this.

**What would settle it:**  
Publish the exact data matrix, random seed, inclusion rules, and runnable code with public corpus access.

---

## Positives a hostile reader must concede

1. **The main coverage arithmetic recomputes.**  
   - 4,925 + 1,429 + 15 = 6,369 H+M tokens.  
   - 6,369 / 7,002 = 0.9096, i.e. **90.96%**.  
   - Without provisional signs: 6,354 / 7,002 = 0.9075, i.e. **90.75%**.  
   - LOW tokens: 633 / 7,002 = 0.0904, i.e. **9.04%**.

2. **The sign-category totals are internally consistent.**  
   - 75 HIGH + 86 MEDIUM + 236 LOW = **397** catalogue signs.  
   - 75 + 86 = **161** H+M signs.

3. **The z-score arithmetic recomputes from printed inputs.**  
   - \((0.9916 - 0.4385) / 0.05347 = 10.344\), printed as **z = 10.3**.

4. **The held-out positional-class percentage recomputes.**  
   - 85 / 87 = **97.7%**.

5. **The fish-bearing site counts sum correctly.**  
   - 6 + 33 + 35 + 11 + 13 + 5 + 4 + 3 + 3 = **113**.

6. **The reported zero-event upper bounds are numerically plausible if the binomial framing were otherwise appropriate.**  
   - For 0/113, one-sided 95% upper bound is about **2.6%**.  
   - For 0/6, about **39%**.  
   - For 0/3, about **63%**.

7. **The M267 percentage recomputes.**  
   - 400 / 7,002 = **5.71%**, matching “5.7%.”

8. **The M267 motif counts sum correctly.**  
   - 147 + 78 + 43 + 26 + 20 + 34 + 19 + 17 + 16 = **400**.

9. **The V07 phonotactic violation rate recomputes.**  
   - 270 / 1,154 = **23.4%**.

10. **The Phase-154 V12 pass rate recomputes.**  
   - 417 / 1,154 = **36.1%**.

11. **The hypothetical blocker-coverage arithmetic recomputes.**  
   - 6,369 + 97 = 6,466.  
   - 6,466 / 7,002 = **92.35%**.

12. **The paper now repeatedly and plainly discloses major weaknesses rather than hiding them:** private corpus, uncalibrated confidence labels, failed SA held-out test, unresolved V12/V07 problems, no bilingual, no discriminative language-family baseline, non-independent internal checks, and unbenchmarked AI-assisted text mining.

CALL-META pass4: finish_reason=stop; max_completion_tokens=48000; completion_tokens=9727; prompt_tokens=28942; output_chars=21619.
