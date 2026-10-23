# Glossa Lab Indus Preprint v8 — Red-Team Round 1: RAW INDEPENDENT-REVIEWER OUTPUTS (verbatim)

Engine: OpenAI API (direct), model `gpt-5.5`. Source text: PDF-extracted text of
pierson_2026_indus_decipherment_preprint_v8.pdf (pdftotext, de-hyphenated), supplied in full
in every call. The three outputs below are reproduced verbatim, unedited. Scaffolding
headers (lines beginning with ## PASS) are the worker's, not the reviewer's.


## PASS 1 — FULL-TEXT HOSTILE REVIEW (reviewer finding IDs F1–F110)

F1.  
(a) “Working from the Holdat LLC Indus Corpus V3 (1,670 seals, 9 sites, 390 distinct signs, 7,002 sign tokens; Mahadevan M-numbers)…”  
(b) Core data are non-public. Every corpus-level number in the paper depends on an unreleased private dataset. The paper cannot be independently checked.  
(c) CRITICAL  
(d) Public release of the exact corpus rows, sign sequences, site labels, motif labels, damaged-sign handling, orientation conventions, duplicate handling, and code producing every reported table.

F2.  
(a) “All sign readings, confidence levels, DEDR citations, basis statements, analysis scripts, and phase reports are available in the Glossa-Lab repository.”  
(b) No repository URL, commit hash, archive DOI, file manifest, or reproducibility instructions are given. “Available” is unverifiable from the paper.  
(c) CRITICAL  
(d) A public archival repository with immutable commit/DOI, scripts, environment files, input/output checksums, and exact commands.

F3.  
(a) “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”  
(b) This directly nullifies the reproducibility claim for all central results: positional statistics, coverage, fish counts, bigrams, KL divergences, bootstrap CIs, grammar accuracy, and motif enrichment.  
(c) CRITICAL  
(d) Release the corpus or rerun the entire paper on a public corpus such as ICIT with a complete sign-code crosswalk.

F4.  
(a) “We find robust non-random positional structure (z = 10.3; 0/2000 permutations exceeded the observed statistic)”  
(b) The statistic is never defined. The paper gives no formula, null model, shuffling unit, treatment of inscription length, orientation, damaged signs, or multiple-testing context. The number is uninterpretable.  
(c) CRITICAL  
(d) Define the test statistic, publish the observed value, null distribution, permutation algorithm, random seed, code, and corpus input.

F5.  
(a) “Phase-134 F1 positional test (z = 10.3; 0/2000 permutations exceeded the observed statistic).”  
(b) The main abstract statistic appears only as a phase-label reference. No Phase-134 methods or outputs are included. A reader cannot verify z = 10.3 or even know what was tested.  
(c) CRITICAL  
(d) Include the Phase-134 report or a methods subsection with the complete derivation and permutation output.

F6.  
(a) “0/2000 permutations exceeded the observed statistic”  
(b) The implied p-value is mishandled. With 2,000 permutations, the smallest unbiased permutation p-value is approximately 1/2001, not zero.  
(c) MAJOR  
(d) Report exact permutation p-values using standard finite-permutation correction and confidence intervals.

F7.  
(a) “161 candidate readings at HIGH or MEDIUM confidence (90.96% token coverage…)”  
(b) The coverage arithmetic does not match the later counts. Section 3.1 says “The 161 H+M anchors … cover 6,363 of 7,002 corpus tokens.” But 6,363 / 7,002 = 90.87%, not 90.96%.  
(c) CRITICAL  
(d) Provide the exact token-count table by sign and recompute percentages consistently.

F8.  
(a) “The remaining 639 tokens (9.1%) have LOW-confidence readings only.”  
(b) 639 / 7,002 = 9.13%, but the table gives LOW = 9.34%. The percentages do not reconcile.  
(c) MAJOR  
(d) Publish the sign-frequency table and the exact denominator used for every percentage.

F9.  
(a) “HIGH 75 76.3%; MEDIUM 86 14.66%; LOW 236 9.34%; H+M total 161 90.96%”  
(b) The table sums to 100.30%, not 100%. The H+M total also does not equal HIGH + MEDIUM if those percentages are used: 76.3 + 14.66 = 90.96, but then LOW should be 9.04, not 9.34.  
(c) CRITICAL  
(d) Correct the table with integer token counts for HIGH, MEDIUM, LOW, PROVISIONAL_MEDIUM, and catalogue-only zero-token signs.

F10.  
(a) “The 161 H+M anchors (75 HIGH + 86 MEDIUM) cover 6,363 of 7,002 corpus tokens.”  
(b) The paper never gives the list of 161 anchors in the preprint. The central claim is asserted without the actual sign-by-sign evidence record.  
(c) CRITICAL  
(d) Include the complete anchor table in the paper or supplement: sign, count, reading, confidence, evidence source, DEDR entry, position rates, motif association, and promotion rationale.

F11.  
(a) “The anchor table assigns readings to all 397 signs in the Mahadevan catalogue…”  
(b) Appendix B lists “M402” among the signs, which is incompatible on its face with “all 397 signs” if sign numbers are Mahadevan M-numbers bounded by 397. At minimum the numbering scheme is unexplained.  
(c) MAJOR  
(d) Provide the full catalogue mapping and explain how M402 exists in a 397-sign Mahadevan catalogue.

F12.  
(a) “390 distinct M-number signs attested in the corpus; the anchor table assigns readings to all 397 signs in the Mahadevan catalogue.”  
(b) The paper conflates “distinct signs,” “M-number signs,” “Mahadevan catalogue signs,” and later “M402.” Without a catalogue table, the accounting is not auditable.  
(c) MAJOR  
(d) Publish a sign inventory with Mahadevan number, corpus frequency, catalogue status, and any crosswalk aliases.

F13.  
(a) “HIGH (75 signs): Two or more independent evidence sources converge…”  
(b) The supposed evidence sources are not independent. Iconography, motif exclusivity, and positional behavior are all extracted from the same corpus and often from the same seal object. Rebus assignment then selects the Dravidian word after looking at the icon.  
(c) CRITICAL  
(d) Demonstrate independence formally, or separate training and testing datasets: derive readings on one corpus and test motif/position predictions on a held-out corpus.

F14.  
(a) “Iconographic match: sign shape unambiguously depicts a known object whose Dravidian name yields the reading by the rebus principle…”  
(b) “Unambiguously” is not operationalized. The rebus method is unconstrained: many Dravidian words can be chosen for a pictured object, and many homophones/near-homophones can be searched post hoc.  
(c) CRITICAL  
(d) Pre-register allowed icon identifications, allowed proto-forms, phonological transformations, semantic domains, and a multiple-comparison correction against alternative language families.

F15.  
(a) “DEDR rebus match with SA-consistency >= 0.15…”  
(b) A threshold of 0.15 is arbitrary and extremely weak. The paper gives no validation showing that 0.15 distinguishes true readings from false ones.  
(c) CRITICAL  
(d) Calibrate SA-consistency on known undeciphered/deciphered scripts or synthetic controls and show ROC/precision-recall behavior for the chosen threshold.

F16.  
(a) “For signs without iconographic anchors, we run a syllabic language model (SA) trained on Tamil/Dravidian syllable sequences…”  
(b) The model is undescribed. No architecture, training corpus, preprocessing, objective, hyperparameters, validation, or output examples are provided. “Tamil/Dravidian” is also vague and temporally mismatched to Proto-Dravidian.  
(c) CRITICAL  
(d) Publish the training data, model code, evaluation benchmarks, held-out tests, and sensitivity analysis using Proto-Dravidian reconstructions and non-Dravidian baselines.

F17.  
(a) “Signs with SA consistency >= 0.15 and a DEDR entry matching the modal reading are promoted to MEDIUM.”  
(b) This is a recipe for confirmation bias. DEDR is large; without reporting how many candidate DEDR matches were searched per sign, the false-positive rate is unknown.  
(c) CRITICAL  
(d) Run the same procedure against shuffled signs, random syllables, Proto-Munda, Indo-Aryan, Elamite, and pseudo-DEDR dictionaries of matched size.

F18.  
(a) “The Dravidian hypothesis is among the most extensively developed linguistic interpretations: the geographic distribution of Dravidian languages, archaeological continuity between IVC and later South Asian cultures, and the demonstrable application of the ‘rebus principle’…”  
(b) “Demonstrable application” overstates the state of the field. Rebus readings of IVS are precisely what is disputed. The paper treats the hypothesis as established background.  
(c) MAJOR  
(d) Cite specific accepted demonstrations, distinguish them from contested proposals, and test against non-Dravidian rebus alternatives.

F19.  
(a) “To my knowledge, no prior work has claimed >90% token coverage with a published sign-by-sign evidence record.”  
(b) This is not a meaningful prior-work review. Claiming nobody else made an inflated coverage claim does not validate this one. It also ignores nearest-neighbour computational work beyond Rao: Yadav et al. n-grams, Sproat/Farmer critiques, sign-ordering studies, corpus concordances, and ICIT-related digitizations.  
(c) MAJOR  
(d) Add a full comparative literature review and define how this model differs from prior positional, entropy, n-gram, and Dravidian decipherment attempts.

F20.  
(a) “Rao et al. (2009, Science 324:1165) demonstrated that IVS sign entropy is consistent with a linguistic system rather than a random or purely symbolic one.”  
(b) This oversimplifies what entropy results can show. Entropy similarity does not demonstrate language; it only rules out some simplistic random/non-random models. The paper itself later admits frequency fits are uninformative, but keeps the stronger framing here.  
(c) MAJOR  
(d) Rephrase to the narrower claim and cite critiques and follow-up work; specify what entropy can and cannot discriminate.

F21.  
(a) “a recurring three-slot inscription formula consistent with a Proto-Dravidian administrative vocabulary framework”  
(b) “Consistent with” is doing all the work. No competing grammar baselines are tested: nonlinguistic emblem sequences, owner marks, commodity marks, clan signs, mixed logosyllabic systems, Proto-Munda, or language-neutral positional templates.  
(c) CRITICAL  
(d) Compare predictive likelihood or classification accuracy across explicit rival models using held-out data.

F22.  
(a) “[SLOT 1: ANIMAL CLASSIFIER] – [SLOT 2: GUILD TITLE] – [SLOT 3: PERSONAL NAME/SUFFIX]”  
(b) The three-slot labels are semantic assertions, not results of positional statistics. Positional statistics might support initial/medial/final structure; they do not identify “animal classifier,” “guild title,” or “personal name.”  
(c) CRITICAL  
(d) Provide independent semantic evidence for each slot, preferably external validation from bilinguals, archaeological context, repeated owner names, or sealed-goods associations.

F23.  
(a) “This grammar predicts that inscriptions encode: ‘the [animal-totem guild title] [person’s name]’”  
(b) The model cannot actually read personal names, and the paper repeatedly says personal-name syllables are unrecoverable. So it cannot substantiate the very formula it claims.  
(c) CRITICAL  
(d) Identify repeated personal-name sequences across seals with independent archaeological ownership/context evidence.

F24.  
(a) “Slot 1 (INITIAL): Animal classifier derived from the seal motif iconography.”  
(b) Circularity: readings are assigned from motif iconography, then motif association is used as evidence that the readings are animal classifiers.  
(c) CRITICAL  
(d) Derive initial sign classes without motif data, then predict motifs on a held-out set.

F25.  
(a) “M060=kāṇṭāmirukam”  
(b) This is an implausible Proto-Dravidian anchor as presented. “kāṇṭāmirukam” looks like a later/modern compound for rhinoceros, not a demonstrated Bronze Age Proto-Dravidian form. No DEDR entry is supplied.  
(c) CRITICAL  
(d) Provide the exact DEDR entry, reconstructed proto-form, chronology, cognate set, and justification that the form existed ca. 2600–1900 BCE.

F26.  
(a) “M261=muruku (young man / deity Murugan, guild-of-Murugan)”  
(b) The deity/title interpretation is anachronistic without evidence. A Bronze Age IVS sign cannot be assigned “Murugan” merely from a later Dravidian religious vocabulary item.  
(c) MAJOR  
(d) Provide archaeological and linguistic evidence for the relevant cult/title in the IVC period and show the sign’s contexts require that reading.

F27.  
(a) “M342=ay/ā — Terminal case suffix (584 tokens, 96% terminal)”  
(b) Frequency and terminal position do not identify a genitive/case suffix, and no DEDR citation is given. This is a grammatical label assigned without linguistic proof.  
(c) CRITICAL  
(d) Show alternations, distributional constraints, syntagmatic contexts, and cross-inscription paradigms matching a specific Proto-Dravidian suffix.

F28.  
(a) “M176=an/aṇ — Masculine suffix (356 tokens, 94% terminal)”  
(b) Terminal position does not prove masculine gender. The semantic category is inferred, not demonstrated.  
(c) MAJOR  
(d) Provide contexts where the sign contrasts with feminine/neuter markers and predicts iconographic or textual gender independently.

F29.  
(a) “M267 is a high-frequency functional/suffixal sign; its current MEDIUM reading is iN/in (genitive particle), derived from its consistent pre-title distribution.”  
(b) “Consistent pre-title distribution” is not quantified. The paper gives no counts, rates, or alternative analyses.  
(c) MAJOR  
(d) Provide M267 positional counts, left/right collocates, motif independence statistics, comparison to known genitive particles, and a null model.

F30.  
(a) “This correction is methodologically important: it demonstrates the risk of reading frequency alone as a phonetic indicator.”  
(b) The paper criticizes one frequency-based error while continuing to promote many readings from positional/frequency behavior plus weak rebus matching. The methodological lesson is not applied consistently.  
(c) MAJOR  
(d) State which readings would survive without frequency/position-based semantic inference and retest coverage.

F31.  
(a) “Testing the full fish sign family (M047, M049, M052–M056, M145)…”  
(b) The “fish sign family” is asserted without showing sign images, classification criteria, or crosswalk evidence. The result depends completely on which signs are included.  
(c) MAJOR  
(d) Publish sign images, catalogue crosswalks, inclusion/exclusion criteria, and independent expert coding of fish-family membership.

F32.  
(a) “The fish sign is never isolated in the formal stamp seal corpus…”  
(b) The denominator is “fish seals,” not fish-sign tokens or all possible isolation contexts. “Isolated” is not defined: single-sign inscription? isolated motif? isolated sign within inscription?  
(c) MAJOR  
(d) Define isolation formally and provide every fish-sign occurrence with inscription length, position, site, object type, and image/source reference.

F33.  
(a) “Lothal (the IVC’s primary coastal port with documented ancient dock).”  
(b) This is asserted without citation and is contested in archaeology. It is unnecessary rhetorical loading for the fish-sign argument.  
(c) MINOR  
(d) Cite current archaeological literature and acknowledge disagreement over the Lothal “dock” interpretation.

F34.  
(a) “The compound-only constraint is site-invariant… indicating it is a scribal rule rather than a geographic pattern.”  
(b) 0 isolated cases across sites does not by itself distinguish a scribal rule from corpus-selection bias, object-type bias, preservation bias, or sign-family definition.  
(c) MAJOR  
(d) Test against all object types, non-seal inscriptions, and independent corpora; model site/object-type effects statistically.

F35.  
(a) “Dilmun-style seals at Failaka Island … show fish in compound pictorial contexts exclusively…”  
(b) The claim shifts from Indus-script signs to pictorial seal motifs. Pictorial fish scenes on Dilmun seals are not the same evidence type as IVS graphemes.  
(c) MAJOR  
(d) Separate graphemic fish signs from pictorial fish motifs and provide image-by-image catalogue coding.

F36.  
(a) “Mining 145,000 characters of extracted text across the Gulf Type seal catalog: no isolated fish signs were found…”  
(b) Text mining a catalogue is not a valid substitute for inspecting seal images. OCR/catalogue prose may omit visual details or use inconsistent terminology.  
(c) CRITICAL  
(d) Publish the list of catalogued seals inspected, images, catalogue numbers, coding decisions, and inter-coder agreement.

F37.  
(a) “giving a combined 0/140 across all tested formal-seal contexts.”  
(b) The combined denominator mixes Holdat corpus fish seals with “Gulf contexts” from catalogues. These are heterogeneous units and not necessarily independent.  
(c) MAJOR  
(d) Keep denominators separate or define a common sampling unit; report confidence intervals and sampling frame.

F38.  
(a) “From the full corpus … we extracted 2,647 distinct bigrams, including 1,485 H+M-by-H+M bigrams.”  
(b) No bigram extraction rule is given: direction, damaged signs, repeated signs, inscription boundaries, seal orientation, duplicates, or length normalization.  
(c) MAJOR  
(d) Provide the bigram table with counts and the extraction script.

F39.  
(a) “M342·M176 … appears on 122 seals … — the highest-PMI, highest-frequency bigram pair.”  
(b) “Highest-PMI” and “highest-frequency” are not substantiated. PMI is biased toward rare events unless controlled; no full ranking or counts are shown.  
(c) MAJOR  
(d) Publish all bigram counts, marginal frequencies, PMI formula, smoothing, and rank table.

F40.  
(a) “17/21 tested H+M signs show position-specific collocate profiles…”  
(b) The 21 signs are not listed and the selection criterion is not given. This invites cherry-picking.  
(c) MAJOR  
(d) List the 21 signs, preregister inclusion rules, and repeat over all eligible signs.

F41.  
(a) “Observed collocate divergence rate: 66.7%… Null distribution mean: 80.7%…”  
(b) The observed statistic is lower than the null, yet the paper spins this as support. As written, the test contradicts the intended claim.  
(c) CRITICAL  
(d) Define a statistic whose direction matches the hypothesis, or admit this test does not support above-null position-specific divergence.

F42.  
(a) “The correct characterisation: signs have tightly constrained, position-specific collocate distributions consistent with a grammar-governed writing system.”  
(b) This conclusion does not follow from the reported null comparison. “Consistent with” is used to rescue a failed or inverted test.  
(c) CRITICAL  
(d) Provide a positive test where the observed corpus differs from null in the predicted direction with a reported p-value/effect size.

F43.  
(a) “We tested 394 INITIAL-sign x iconography pairs for enrichment (chi-square with Bonferroni correction). 63 pairs (16%) are significantly enriched…”  
(b) No p-values, degrees of freedom, contingency tables, correction threshold, or expected-count diagnostics are given. Many expected counts are below 5, making chi-square dubious.  
(c) MAJOR  
(d) Publish all contingency tables and use exact/permutation tests where expected counts are small.

F44.  
(a) “M060 … Observed 20 Expected 2.0 chi-square 158.5”  
(b) The statistic cannot be checked because the 2x2 table is missing. A single observed/expected cell is insufficient.  
(c) MAJOR  
(d) Provide full 2x2 tables for each sign-icon pair and the formula used.

F45.  
(a) “This demonstrates that each seal co-encodes professional identity in two independent channels…”  
(b) Enrichment of initial signs with animal motifs, even if real, does not demonstrate “professional identity.” That is semantic overreach.  
(c) CRITICAL  
(d) Provide external archaeological evidence linking specific signs/motifs to professions or guilds.

F46.  
(a) “The animal reading in the INITIAL sign matches the carved animal at rates far exceeding chance.”  
(b) The readings were partly assigned because of animal/motif matches. This is not independent validation; it is circular confirmation.  
(c) CRITICAL  
(d) Blind-code sign readings without motif information, then test motif prediction on unseen seals.

F47.  
(a) “All top blocking signs … are 100% MEDIAL… This is the expected signature of personal-name syllables…”  
(b) 100% medial position does not imply personal names. It could reflect syntax, sign class, object-type formulae, damage, or classifier structure.  
(c) MAJOR  
(d) Show repeated name-like sequences, genealogical/ownership clustering, or external name correspondences.

F48.  
(a) “The 30.2% uncovered ceiling is structurally irreducible under current methodology — not a methodological failure…”  
(b) This is special pleading. Failure to read 30.2% of seals is declared a structural feature of the preferred model.  
(c) MAJOR  
(d) Quantify model uncertainty and compare with rival explanations for uncovered signs.

F49.  
(a) “Rakhigarhi’s distinctiveness is not a small-sample artifact.”  
(b) Rakhigarhi has n = 33 seals. Bootstrap resampling from a tiny, possibly biased sample does not prove site distinctiveness.  
(c) MAJOR  
(d) Use larger Rakhigarhi samples, object-type controls, rarefaction, Bayesian hierarchical models, and external replication.

F50.  
(a) “Mohenjo-daro vs Rakhigarhi KL=0.509 with 95% CI [0.483, 0.750]”  
(b) The KL method is underspecified: direction of KL, smoothing for zero sign frequencies, feature space, resampling unit, and bias correction are missing.  
(c) MAJOR  
(d) Provide exact KL formula, smoothing parameter, sign-frequency vectors, bootstrap procedure, and code.

F51.  
(a) “F3 redesign using phonemes physically absent from Sanskrit’s phoneme inventory…”  
(b) The phonological premise is sloppy. Sanskrit has palatal nasal ñ in its phonological/phonetic system, and Vedic/Indic phonology cannot be reduced to “physically absent” characters.  
(c) MAJOR  
(d) Use a historical phonologist-reviewed phoneme inventory for Old Indo-Aryan/Vedic and Proto-Dravidian, with explicit chronological stage.

F52.  
(a) “0/157 H+M readings contain Sanskrit-exclusive phonemes … 35/157 contain Dravidian-exclusive phonemes…”  
(b) The test is meaningless if the readings were chosen from Dravidian sources. It proves the output reflects the input bias.  
(c) CRITICAL  
(d) Compare independently generated candidate readings under Dravidian, Indo-Aryan, Munda, and language-neutral models.

F53.  
(a) “all four carry Proto-Dravidian c-initial, which is Dravidian-exclusive.”  
(b) c-initial is not “Dravidian-exclusive” in any useful sense; Indo-Aryan has c/ch-type palatal affricates/stops. The statement is linguistically indefensible as written.  
(c) MAJOR  
(d) Define the exact phoneme and stage, and have the claim checked against Old Indo-Aryan, Munda, Elamite, and other relevant inventories.

F54.  
(a) “The Shu-ilishu seal … provides the only archaeologically-grounded external phonological anchor…”  
(b) The owner name Šu-ilīšu is Akkadian, not necessarily Meluhhan. Matching its syllables to IVS candidate signs is not an external anchor for the Meluhhan language.  
(c) CRITICAL  
(d) Show that the Indus-script portion, if any, encodes the same name, with exact seal inscription, image, archaeological context, and independent epigraphic analysis.

F55.  
(a) “2/4 slots are covered (/i/ by 45 candidate signs…)”  
(b) A phonological slot “covered” by 45 signs is not evidence; it is overgeneration. If dozens of signs can satisfy /i/, the test has no discriminative power.  
(c) MAJOR  
(d) Define a unique or ranked mapping from signs to phonological values and test against false names of matched length.

F56.  
(a) “Tamil-Brahmi terminal phoneme cross-validation (73% TB category coverage)”  
(b) Tamil-Brahmi is roughly two millennia later. Category coverage is not validation of IVS readings; it may simply reflect that the author chose Dravidian-looking suffixes.  
(c) MAJOR  
(d) Use diachronically justified Proto-Dravidian morphology and show predictions not obtainable by chance or by arbitrary suffix selection.

F57.  
(a) “Testing these against the Tamil-Brahmi epigraphy terminal phoneme inventory… 4/7 match (57%)… When the broader set of known suffix signs is included… coverage rises to 8/11 categories (73%).”  
(b) The denominator changes midstream. The reported headline 73% is obtained by expanding the tested set after the stricter test produced 57%.  
(c) MAJOR  
(d) Predefine the tested sign set and report one primary analysis; treat post hoc expansions as exploratory.

F58.  
(a) “V07 phonotactic violation rate under the stricter redefined test: 23.4% — the majority are short abbreviated seals…”  
(b) A nearly one-quarter violation rate is waved away without showing counts, definitions, or why short seals excuse violations.  
(c) MAJOR  
(d) Publish all violations, define the phonotactic rules, and compare violation rates against alternative reading systems.

F59.  
(a) “44/75 HIGH-confidence H+M readings appear in Parpola’s text (59% independent cross-validation…)”  
(b) This is not independent. The paper says Parpola’s framework “grounds all readings.” Agreement with the source used to choose readings is circular.  
(c) CRITICAL  
(d) Separate readings inherited from Parpola from readings independently generated, and validate only the latter against truly independent evidence.

F60.  
(a) “6,869 genitive/possessive references are consistent with M267 as a grammatical particle”  
(b) Counting occurrences of words like “genitive” or “possessive” in Parpola’s book does not validate M267. The number is absurdly uninterpretable without query terms and contexts.  
(c) MAJOR  
(d) Provide the exact text-mining queries, hits, pages, associated signs, and a manual coding of whether each hit supports M267 specifically.

F61.  
(a) “47 classifier/determinative references support our INITIAL-class sign model.”  
(b) Generic references to classifiers/determinatives in a book do not support this specific three-slot grammar.  
(c) MAJOR  
(d) List each reference, page, sign, and how it maps to the model’s INITIAL slot.

F62.  
(a) “Mining 10 Mahadevan papers spanning 1972–2018: all 10 papers independently describe positional grammar consistent with the 3-slot model.”  
(b) “Consistent with” is undefined and the mining results are internal, not externally checkable. Also “independently” is false if these are works by the same scholar in the same research tradition.  
(c) MAJOR  
(d) Provide a coded bibliography with excerpts, page numbers, sign classes, and independent reviewers’ agreement scores.

F63.  
(a) “The paper counts in this section and the next are this program’s own text-mining corpus counts: internal outputs, not externally sourced figures.”  
(b) The paper admits these numbers are internal outputs, then uses them as evidence. They are unverifiable from the preprint.  
(c) MAJOR  
(d) Publish the text corpus, OCR files, queries, scripts, and hit tables.

F64.  
(a) “Systematic mining … yielded 0 new direct M-number reading assignments… This is a meaningful null result…”  
(b) Absence from the author’s OCR/text-mining pipeline is not a meaningful scholarly null unless the search has known recall. OCR failures, sign-number mismatches, and non-M-number references can all hide proposals.  
(c) MAJOR  
(d) Validate the literature-mining recall against a hand-coded benchmark of known sign-reading proposals.

F65.  
(a) “These are exploratory — text proximity in OCR’d academic text does not guarantee a direct sign assignment…”  
(b) Despite admitting this, four signs are promoted to PROVISIONAL_MEDIUM and included in coverage accounting. That inflates the main headline with explicitly unreliable evidence.  
(c) MAJOR  
(d) Exclude OCR-proximity promotions from headline coverage until manually verified by experts.

F66.  
(a) “Four signs promoted to PROVISIONAL_MEDIUM status based on >=3 independent text mentions…”  
(b) The “independent text mentions” are not shown and may not be sign assignments. The threshold is arbitrary.  
(c) MAJOR  
(d) Provide the exact mentions, pages, context windows, and manual verification that each mention assigns the claimed reading to the claimed sign.

F67.  
(a) “M198=co PROVISIONAL_MEDIUM … 3 references — just below the >=4 threshold.”  
(b) The rule shifts. Section 3.25 says promotion used “>=3 independent text mentions”; Section 3.27 says M198 is below a “>=4 threshold.”  
(c) MAJOR  
(d) State one threshold and apply it consistently.

F68.  
(a) “M330=can … INITIAL position; 4 Parpola references”  
(b) No corpus counts, position rates, or references are given. “SUPPORTED_WITHIN_MODEL” is an internal label, not evidence.  
(c) MAJOR  
(d) Provide counts, sign images, Parpola passages, and DEDR details for each provisional sibilant sign.

F69.  
(a) “19/19 blocker LOW readings are phonotactically plausible…”  
(b) Phonotactic plausibility is nearly worthless as evidence; many random syllables are phonotactically plausible. The paper admits it is insufficient but still uses it in the evidence scorecard.  
(c) MAJOR  
(d) Show discriminative likelihood against random syllables and rival language-family phonotactics.

F70.  
(a) “Coverage estimate if these 19 blockers were promoted to MEDIUM: 90.96% -> 92.35%.”  
(b) This hypothetical coverage is prominently reported despite the signs not meeting MEDIUM criteria. It is speculative inflation.  
(c) MINOR  
(d) Move to a clearly labelled sensitivity appendix and keep it out of evidence synthesis.

F71.  
(a) “the full-corpus SA with 161 pinned anchors could not be executed…”  
(b) A failed planned analysis is replaced by a weaker plausibility check, but the paper still treats the phase as an evidence advance.  
(c) MAJOR  
(d) Fix and rerun the SA analysis or remove the claim from the evidence scorecard.

F72.  
(a) “32 total evidence items… 79.8% aggregate confidence score…”  
(b) The aggregate confidence score is meaningless without a scoring rubric, weights, calibration, uncertainty, and independence assumptions.  
(c) CRITICAL  
(d) Publish the scorecard, weights, item definitions, inter-rater procedure, and sensitivity analysis.

F73.  
(a) “18 items rated STRONGLY_SUPPORTED_WITHIN_MODEL or HIGHLY_SUPPORTED.”  
(b) These are self-assigned labels. “Within-model” evidence cannot validate the model; it can only show internal consistency.  
(c) MAJOR  
(d) Separate internal coherence checks from external validation and report them separately.

F74.  
(a) “Internal consistency checks pass (59/59, Phases 1–170).”  
(b) Passing internal scripts proves almost nothing about decipherment. It can simply mean the scripts encode the author’s assumptions.  
(c) MAJOR  
(d) Publish tests and include adversarial tests capable of failing the model against real alternatives.

F75.  
(a) “adversarial challenge battery 10/10 (S10)”  
(b) The battery is not described. This is unverifiable scoreboard rhetoric.  
(c) MAJOR  
(d) Publish all challenges, expected outcomes, actual outputs, and who designed them.

F76.  
(a) “Grammar variance retest… 93.2% sign-level grammar accuracy…”  
(b) The “grammar” classification is based on the same positional thresholds used to define the classes. This is tautological: signs are classified by position and then counted as matching positional classes.  
(c) CRITICAL  
(d) Test grammar predictions on held-out inscriptions or unseen signs, not on the same position rates used to define the categories.

F77.  
(a) “TERMINAL if T>=0.60, INITIAL if I>=0.50, MEDIAL if M>=0.65”  
(b) Thresholds are arbitrary and asymmetric. No justification or sensitivity analysis is provided.  
(c) MAJOR  
(d) Pre-register thresholds or optimize them on training data and evaluate on held-out data.

F78.  
(a) “the metric difference from Phase-133’s 44.3% reflects different methodological definitions… Both results are consistent…”  
(b) A jump from 44.3% to 93.2% caused by redefining the metric is not reassuring. The paper uses incompatible metrics while claiming stability.  
(c) MAJOR  
(d) Report both metrics for both phases and explain why the original 44.3% did not falsify or weaken the grammar.

F79.  
(a) “Comparison with the CISI corpus… KL divergence … = 0.591, a numbering/coverage artifact rather than structural disagreement.”  
(b) The paper declares an unfavorable divergence an artifact without proving it.  
(c) MAJOR  
(d) Provide the crosswalk, show the artifact quantitatively, and repeat the comparison after correction.

F80.  
(a) “Independent scorecard study (Nair 2026, arXiv:2604.17828)…”  
(b) The external study is not used to validate the anchor readings, grammar, or Dravidian hypothesis. The paper admits this, yet lists it in the results as support.  
(c) MINOR  
(d) Remove it from evidence for decipherment unless it directly tests this model’s predictions.

F81.  
(a) “The evidence is consistent with a Proto-Dravidian reading framework under the tested assumptions, though Dravidian superiority over proto-Munda has not been formally quantified.”  
(b) This is the central weakness admitted in the abstract. Without quantified comparison to Proto-Munda, Indo-Aryan, Elamite, language-neutral, or nonlinguistic models, “Proto-Dravidian” is not established.  
(c) CRITICAL  
(d) Run the same pipeline against explicit competing lexicons/phonologies and compare out-of-sample likelihood, coverage, false-positive rates, and semantic fit.

F82.  
(a) “Identification of 2 Munda substrate loans in the sign corpus”  
(b) Two weak candidate matches do not identify substrate loans. They are speculative lexical guesses.  
(c) MAJOR  
(d) Provide exact Munda forms, chronology, borrowing pathway, sign contexts, and statistical evidence that Munda matches exceed chance.

F83.  
(a) “M374 kul … Munda kul (tiger-lord)… kulam (clan/lineage)”  
(b) This bundles Munda and Dravidian-looking material without demonstrating borrowing or substrate status. It reads like opportunistic cognate shopping.  
(c) MAJOR  
(d) Establish the form in relevant Munda languages, its chronology, semantics, and why a Dravidian reading alone is insufficient.

F84.  
(a) “M351 vī … Munda bi … bi -> vī bilabial shift”  
(b) The sound correspondence is asserted ad hoc. No regular correspondence or borrowing model is supplied.  
(c) MAJOR  
(d) Provide regular phonological correspondences and independent examples of the claimed shift.

F85.  
(a) “a Dravidian administrative elite writing in proto-Dravidian, with Munda-speaking communities contributing loanwords…”  
(b) This sociolinguistic scenario outruns the evidence. Two proposed substrate signs cannot establish administrative elites or community structure.  
(c) CRITICAL  
(d) Require independent archaeological, linguistic, and textual evidence for elite language use and substrate integration.

F86.  
(a) “Under the grammar model, a typical seal reads as: M211 M099 M342 = kol-kol-ay = ‘the jar-guild lord’…”  
(b) The translations are presented as if meaningful, but every component is hypothetical and internally generated. No uncertainty or alternative translation is shown.  
(c) MAJOR  
(d) Provide gloss-by-gloss evidence, alternative readings, and independent checks on complete-seal translations.

F87.  
(a) “This is not a commodity ledger — it is a directory of guild members…”  
(b) The paper has not ruled out commodity, ownership, clan, cultic, administrative, or nonlinguistic marking systems. The claim is categorical.  
(c) CRITICAL  
(d) Formally compare the guild-directory model against commodity/ownership/nonlinguistic models using archaeological context and predictive tests.

F88.  
(a) “functionally equivalent to a medieval European guild seal…”  
(b) This analogy is chronologically and culturally remote. It is rhetorical, not evidential.  
(c) MINOR  
(d) Replace with contemporaneous Bronze Age sealing-system comparanda.

F89.  
(a) “The Arthaśāstra … documents nearly identical guild-superintendent titles…”  
(b) “Nearly identical” is an overstatement across roughly two millennia. Later Sanskrit administrative titles do not validate IVS Proto-Dravidian readings.  
(c) MAJOR  
(d) Demonstrate continuous institutional and lexical transmission with intermediate evidence.

F90.  
(a) “The strongest findings … are Tier 1 structural claims that can be stated with high confidence.”  
(b) Several “Tier 1” claims are not established: z = 10.3 is undefined, fish 0/140 uses heterogeneous denominators, three-slot semantics are not proven, and M267’s new reading is not quantified.  
(c) CRITICAL  
(d) Demote these claims or provide full reproducible derivations and independent validation.

F91.  
(a) “The corpus shows structure consistent with a decipherable linguistic system…”  
(b) “Consistent with” is too weak for the conclusion’s rhetorical force. Structured nonlinguistic systems can also show positional constraints.  
(c) MAJOR  
(d) Demonstrate that the observed structure discriminates writing from non-writing under realistic baselines.

F92.  
(a) “the evidence favours a Proto-Dravidian reading framework under the tested assumptions.”  
(b) The assumptions bake in Dravidian: DEDR matching, Tamil-trained model, Dravidian suffix inventories, Parpola-derived readings. The conclusion is not independent of the setup.  
(c) CRITICAL  
(d) Use blinded model comparison with matched Dravidian and non-Dravidian resources.

F93.  
(a) “No bilingual text: All readings remain probabilistic…”  
(b) The limitation understates the problem. Many readings are not merely probabilistic; their probabilities are never quantified.  
(c) MAJOR  
(d) Provide posterior probabilities or calibrated confidence scores for each reading.

F94.  
(a) “HIGH,” “MEDIUM,” “LOW,” “PROVISIONAL_MEDIUM”  
(b) These labels look quantitative but are rule-of-thumb categories. No error rates are attached.  
(c) MAJOR  
(d) Calibrate categories against known scripts or blinded expert evaluation and report expected precision.

F95.  
(a) “coverage measures anchor-model assignment, not verified phonetic transcription”  
(b) This caveat severely weakens the headline “90.96% token coverage.” Coverage means only that the model assigned something, not that it deciphered anything.  
(c) CRITICAL  
(d) Rename the metric “model-assigned token share” and stop presenting it as decipherment coverage unless independently validated.

F96.  
(a) “0 isolated fish signs in the 1,670-seal corpus (0/113 across 9 corpus sites)”  
(b) The abstract says “fish signs” but the table reports “Fish seals.” Those are different denominators.  
(c) MAJOR  
(d) Report both token-level and seal-level counts separately.

F97.  
(a) “site-level H+M-coverage rates range from 70% (Rakhigarhi, n=33 — small sample) to 93% (Dholavira).”  
(b) No site-level table is provided. Readers cannot check the range or denominators.  
(c) MINOR  
(d) Include a full site-by-site coverage table with seals, tokens, H/M/L counts, and confidence intervals.

F98.  
(a) “These 18 signs account for 3.8% of corpus tokens”  
(b) Appendix B says the 18 signs have frequency 5–7 each. Maximum total tokens = 18 × 7 = 126. 126 / 7,002 = 1.8%, not 3.8%. The arithmetic is impossible.  
(c) CRITICAL  
(d) Correct either the frequencies, the sign list, or the percentage; provide token counts by sign.

F99.  
(a) “These 18 signs have corpus frequency 5–7…”  
(b) If true, they cannot explain much of the 30.2% of seals not fully covered unless distributed almost one per blocked seal. The relation between token share and seal blockage is not quantified.  
(c) MAJOR  
(d) Provide the exact seals blocked by each sign and counts of overlapping blockers.

F100.  
(a) “The ICIT corpus (5,318 texts) with contextual metadata is required…”  
(b) The paper repeatedly invokes a larger corpus as necessary, but the headline claims are made before testing it.  
(c) MAJOR  
(d) Run the model on ICIT before making broad claims about the IVS.

F101.  
(a) “Wells independently argues proto-Dravidian language and consistent sign positional classes.”  
(b) The paper gives no page numbers or quotations. This is unverifiable and may overstate Wells’s position.  
(c) MAJOR  
(d) Quote the relevant Wells passages with pages and distinguish Wells’s claims from the author’s interpretation.

F102.  
(a) “The Dholavira place-name identification appears in two separate sections…”  
(b) No details are given: which sign sequence, which sections, what identification, and how it converges with this model.  
(c) MAJOR  
(d) Provide page references, sign numbers, and the exact claimed convergence.

F103.  
(a) “Parpola (1994) Appendix explicitly documents compounds ending in mīn (4 attestations), corroborating compound-only status.”  
(b) Four attestations ending in mīn do not prove no isolated fish signs exist, especially across different corpora and cataloguing systems.  
(c) MAJOR  
(d) Show a complete enumeration of all Parpola fish-sign attestations, including absence evidence.

F104.  
(a) “M267 chi-square motif-independence (S11)”  
(b) The chi-square test is mentioned only in the scorecard, not shown. It cannot support the correction.  
(c) MAJOR  
(d) Provide the contingency table, test statistic, degrees of freedom, p-value, and expected counts.

F105.  
(a) “Phase-128/129 net gain +35 seals”  
(b) The gain is unexplained. Which signs caused the gain? Which seals changed from blocked to covered?  
(c) MINOR  
(d) Provide a before/after seal list and anchor additions responsible.

F106.  
(a) “Phase-163 adds 4 provisional sibilant upgrades”  
(b) The abstract includes provisional upgrades in the headline 161 count, despite explicitly saying they need expert review.  
(c) MAJOR  
(d) Report headline counts excluding provisional signs, with provisional counts separate.

F107.  
(a) “PROVISIONAL_MEDIUM readings are included within the MEDIUM count for coverage accounting…”  
(b) This inflates MEDIUM with a category that is explicitly not fully vetted.  
(c) MAJOR  
(d) Exclude PROVISIONAL_MEDIUM from main MEDIUM coverage or present both numbers prominently.

F108.  
(a) “no further evidence advance is achievable with the current 1,670-seal Holdat corpus and available published literature.”  
(b) This is unjustified. Better statistical modeling, public corpora, object-type controls, image inspection, expert coding, and rival-model testing are all possible without new archaeology.  
(c) MAJOR  
(d) Remove the claim or demonstrate exhaustion with a transparent protocol.

F109.  
(a) “All phase reports, scripts, and the anchor table are available…”  
(b) The paper relies on “phases” as evidence, but phases are not peer-reviewable unless included or archived.  
(c) MAJOR  
(d) Archive phase reports with stable identifiers and cite exact files.

F110.  
(a) “Statistical tests were designed, executed, and interpreted by the author; AI tooling was used for scripting, data management, and literature search.”  
(b) Given the number of internal text-mining claims, OCR proximity promotions, and self-scored evidence labels, the AI-assisted workflow needs audit trails. None are supplied.  
(c) MAJOR  
(d) Provide logs, prompts where relevant, generated code review, manual verification records, and error audits for literature-mining outputs.

## PASS 2 — TARGETED ATTACK on §2.1 / §2.1.1 / §3.10 / §1.2 Rao sentence (reviewer finding IDs T1–T15)

## Direct answers by target

**Target 1:** The revised §2.1 Zipf paragraph is substantially fairer than the old claim: it retracts the unpublished “about 1.7” exponent as language evidence and quotes the Yadav et al. limitation. But the retraction is not fully clean because nearby and later text reintroduces multiple unexplained exponents and the paper still contains broader “distribution/entropy proves language” rhetoric, especially in §1.2.

**Target 2:** §2.1.1 states the intended UNINFORMATIVE verdict, but the presentation is still defective. Placing **1.35**, **~1.7**, **2.004**, and **1.96** close together invites exactly the cross-corpus/exponent comparison the passage says is forbidden. The comparison-system numbers are not checkable from the preprint as given.

**Target 3:** §3.10 now says the paper does **not** rely on Nair’s Zipf slope and instead treats Nair mainly as evidence of non-random ordering/permutation structure. It fairly includes Nair’s hedge, but overstates independence and “external validation”: same broad inscription assemblage, ICIT-family data, unpublished/2026 arXiv scorecard, and only 1,000 permutation trials.

**Target 4:** Yes. “Demonstrated” is an overstatement if Rao et al. themselves only claimed their results “increase the probability” that the script represents language.

---

## Findings

### T1 — §2.1 fairly retracts the old Zipf-language claim, but only locally  
**Quote:** “An earlier version of this paper reported a Zipf exponent of about 1.7 for this distribution and described it as consistent with a natural language writing system. That exponent is this program’s own statistic on this corpus; no derivation of it has been published that a reader can check, and we no longer present it as evidence that the script is a language.”

**Defect:** This is a real and welcome retraction. It admits the exponent was unpublished, non-checkable, and no longer valid as language evidence. However, the correction is only local: the paper later reintroduces other frequency-curve exponents and still uses broad “linguistic system” language elsewhere.

**Severity:** **MINOR** for the wording of this paragraph itself; **MAJOR** in combination with later residue.

**Evidence that would settle it:** A revision audit showing all Zipf/frequency-curve claims removed as evidence for linguistic status, plus a reproducible derivation of any exponent still reported.

---

### T2 — Yadav et al. are mostly represented fairly, but the citation is too thin  
**Quote:** “Yadav et al. (2010), who published a Zipf–Mandelbrot fit for Indus sign frequencies (on a pruned subset of Mahadevan’s corpus), state the limit themselves: the presence of such a distribution ‘is not sufficient to declare a sequence as linguistic’.”

**Defect:** The cautionary quote is appropriate and appears to capture the key limitation. But the paper gives no page, section, fitting details, pruning definition, or exact context. “Pruned subset of Mahadevan’s corpus” is too vague for a technical claim about frequency exponents.

**Severity:** **MINOR**

**Evidence that would settle it:** Exact quotation with page/section from Yadav et al. 2010, the precise data subset used there, the Zipf–Mandelbrot fitting equation, and whether the current paper’s use of “pruned subset” matches Yadav’s actual filtering.

---

### T3 — The old Zipf claim survives indirectly through multiple unexplained exponents  
**Quote:** §2.1 reports “a Zipf exponent of about 1.7.” §2.1.1 then reports “exponent 𝛼 = 2.004,” “𝛼 = 1.96,” and “the Phase-43 exponent of about 1.35 recorded in this program’s files.”

**Defect:** Even while saying none of these exponents should be used as language evidence, the paper leaves four exponent-like numbers in close proximity without a table explaining corpus, statistic, fitting rule, rank convention, pruning, and sign inventory. That creates apparent numerical comparability where the paper itself says there is none.

**Severity:** **MAJOR**

**Evidence that would settle it:** A table explicitly separating: corpus, sign inventory, token count, rank-frequency model, exponent convention, fitting range, error metric, and whether the number is comparable. Or remove the obsolete 1.35 and ~1.7 values entirely except in a correction note.

---

### T4 — Residual “frequency/entropy proves language” rhetoric remains in §1.2  
**Quote:** “Rao et al. (2009, Science 324:1165) demonstrated that IVS sign entropy is consistent with a linguistic system rather than a random or purely symbolic one.”

**Defect:** This undercuts the §2.1 retreat. The paper no longer uses its own Zipf exponent as language evidence, but still says entropy work “demonstrated” linguistic consistency. That is stronger than the cautious probabilistic claim attributed to Rao et al. in the audit note.

**Severity:** **MAJOR**

**Evidence that would settle it:** Replace “demonstrated” with Rao’s actual level of claim, e.g. “argued that entropy results increase the probability of a linguistic interpretation,” and cite the exact passage.

---

### T5 — §2.1.1 correctly states the UNINFORMATIVE verdict, but the surrounding presentation invites forbidden comparison  
**Quote:** “Under the rule fixed before the run, that result makes the comparison UNINFORMATIVE: these measures do not separate the one certain writing system from systems that are not writing, so a close Indus fit on them is evidence neither for nor against the script being language.”

**Quote:** “The Shakti numbers are a measurement of the Shakti corpus only. They are not a measurement of the Holdat corpus used in this paper, and they do not confirm or correct any earlier exponent, including the Phase-43 exponent of about 1.35 recorded in this program’s files.”

**Defect:** The verdict is stated honestly in words. But the paper then keeps the Shakti exponent, wider-Shakti exponent, older Phase-43 exponent, and prior ~1.7 exponent all visible in adjacent sections. That presentation invites readers to compare them despite the explicit warning that they “do not confirm or correct any earlier exponent.”

**Severity:** **MAJOR**

**Evidence that would settle it:** Either remove the historical exponents or add a prominent “not comparable” table explaining exactly why each number differs and forbidding rank-order interpretation.

---

### T6 — The Spec 068 comparison-system numbers are not checkable from the preprint  
**Quote:** “The comparison systems were Mesopotamian numerical signs (error 0.5335), heraldic charges from the Dering Roll (0.1839), a synthetic emblem process (median 0.2405), and Linear B (0.9229).”

**Quote:** “On those counts the fit gave exponent 𝛼 = 2.004 and fit error 0.1584 … On a wider set of rows from the same corpus … 𝛼 = 1.96 and error 0.1544.”

**Defect:** The paper supplies final numbers but not the data vectors, sign counts, rank lists, fitting code, fitting range, exact Zipf–Mandelbrot parameterization, or the comparison corpora. “Spec 068,” “Spec 053,” and “OSF registration 3pbwe” are not enough in the preprint to reproduce the results.

**Severity:** **CRITICAL**

**Evidence that would settle it:** Public archive containing: Spec 053, Spec 068, OSF URL, frozen scripts, input count tables for all five systems, random seeds for the synthetic emblem process, and exact reproduction commands yielding 0.1584, 0.1544, 0.5335, 0.1839, 0.2405, and 0.9229.

---

### T7 — “Linear B fitted worst” is potentially misleading without corpus-normalization details  
**Quote:** “Linear B is the one system in the set that is certainly writing, and it fitted the curve worst of the five.”

**Defect:** This is rhetorically powerful but underdocumented. Linear B sign-frequency behavior depends heavily on whether the corpus uses syllabograms, logograms, numerals, transaction formulae, word dividers, damaged signs, or tablet-level normalization. Without those details, “fitted worst” may reflect coding/corpus mismatch rather than a meaningful negative control.

**Severity:** **MAJOR**

**Evidence that would settle it:** Full Linear B dataset specification, sign classes included/excluded, tokenization rules, and demonstration that the comparison is like-for-like with the Indus and non-writing systems.

---

### T8 — The UNINFORMATIVE verdict is honest but incomplete  
**Quote:** “these measures do not separate the one certain writing system from systems that are not writing, so a close Indus fit on them is evidence neither for nor against the script being language.”

**Defect:** The conclusion is appropriately cautious, but incomplete. With only one certain writing positive control named, the test may show that this particular benchmark design is weak, not that frequency-curve evidence in general is uninformative. The paper does not report uncertainty, sensitivity analyses, or alternative positive writing controls.

**Severity:** **MAJOR**

**Evidence that would settle it:** Add several known writing systems and several non-writing/semasiographic systems, preregister classification thresholds, report confidence intervals or permutation uncertainty, and publish all inputs.

---

### T9 — Nair’s Zipf slope is explicitly disclaimed, which is good  
**Quote:** “One of Nair’s four measures, his Zipf slope, is a frequency-curve fit of the kind tested in §2.1.1 … so we do not use his slope — any more than our own earlier figure — as evidence about linguistic status.”

**Defect:** This passage directly answers the prior problem: the paper says its support does not rest on Nair’s “Zipf slope –1.49.” That is a proper correction.

**Severity:** **MINOR / no adverse finding on this narrow point**

**Evidence that would settle it:** Ensure the abstract, introduction, conclusion, and evidence scorecard do not elsewhere count Nair’s Zipf slope as positive linguistic evidence.

---

### T10 — Nair’s hedged conclusion is reported, but the paper still uses him as “independent external” support  
**Quote:** “Nair’s own conclusion is deliberately hedged: the Indus corpus occupies an intermediate position between his synthetic non-linguistic baselines, matches the administrative baseline on only two of four metrics, and, in his words, the study does not settle the linguistic question.”

**Quote:** §1.3 lists “Independent external scorecard study (Nair 2026, arXiv:2604.17828) on the ICIT corpus.”

**Defect:** The hedge is fairly included in §3.10. But §1.3 still promotes the study as an “Independent external scorecard study,” and §3.10 places it under “Cross-Corpus Structural Validation.” That framing risks turning a hedged, non-settling scorecard into validation of the author’s model.

**Severity:** **MAJOR**

**Evidence that would settle it:** Reword as “external comparison study, not validation of this decipherment model,” and state explicitly that Nair does not test the proposed readings, three-slot grammar, or Dravidian hypothesis.

---

### T11 — Nair’s “independence” is overstated  
**Quote:** “Nair’s corpus is a separate digitization (G-prefix ICIT coding) of the published inscription assemblage, analysed with an independent methodology.”

**Quote:** §2.1.1 says the Shakti corpus is “a restricted corpus in the ICIT line.”

**Defect:** “Separate digitization” and “independent methodology” are not the same as independent evidence. Nair uses the same broad published Indus inscription assemblage, and the paper’s own Spec 068 uses a corpus “in the ICIT line.” So Nair is not independent in the strong validation sense; he is at most an external reanalysis of overlapping source material.

**Severity:** **MAJOR**

**Evidence that would settle it:** Corpus-overlap table showing which inscriptions/sign codings overlap between Holdat, Shakti, ICIT, and Nair; independent replication on a genuinely separate corpus or newly published inscriptions.

---

### T12 — “Permutation null percentile 0.000 against 1,000 trials” is overprecise if treated as a probability  
**Quote:** “permutation null percentile 0.000 against 1,000 permutation trials.”

**Defect:** With 1,000 trials, an empirical result of zero exceedances should usually be reported as 0/1000, p < 0.001, or with a plus-one correction p ≈ 0.001, not as a literal “0.000” probability. The paper does not clarify whether “percentile 0.000” is Nair’s display convention or a statistical p-value.

**Severity:** **MINOR**

**Evidence that would settle it:** Quote Nair’s exact statistic definition and report the exceedance count and corrected empirical p-value.

---

### T13 — A 2026 arXiv scorecard is weak as “external validation”  
**Quote:** “Independent scorecard study (Nair 2026, arXiv:2604.17828).”

**Quote:** The preprint itself is labeled “Version: Preprint v8 — Not peer-reviewed.”

**Defect:** A contemporaneous arXiv scorecard can be cited as outside work, but it should not be treated as strong external validation, especially when it is not peer reviewed, does not test the decipherment readings, and reaches a hedged conclusion.

**Severity:** **MAJOR**

**Evidence that would settle it:** Peer-reviewed publication of Nair’s study, public code/data, and independent replication of the specific positional grammar and anchor readings—not just generic ordering statistics.

---

### T14 — Rao et al. wording is overstated relative to the audit note  
**Preprint quote:** “Rao et al. (2009, Science 324:1165) demonstrated that IVS sign entropy is consistent with a linguistic system rather than a random or purely symbolic one.”

**Audit/Rao wording quoted in prompt:** Rao et al.’s paper itself claims only that its results “increase the probability” that the script represents language.

**Defect:** “Demonstrated” is stronger than “increase the probability.” The preprint converts a probabilistic, evidentiary claim into a declarative result. It also frames the alternatives oddly as “random or purely symbolic”; writing systems are themselves symbolic, so “purely symbolic” is imprecise unless defined as non-linguistic/semasiographic.

**Severity:** **MAJOR**

**Evidence that would settle it:** Exact Rao et al. conclusion text and a revised sentence matching it, e.g. “Rao et al. argued that entropy patterns increase the probability that IVS encodes language, relative to certain random and non-linguistic baselines.”

---

### T15 — The paper’s own availability statement undermines reproducibility of the core corpus claims  
**Quote:** “The Holdat LLC Indus Corpus v3 is not publicly available at time of writing.”

**Quote:** “Because the Holdat corpus is not yet publicly released, full reproduction of corpus-level counts requires either access to that corpus under agreement or re-running the pipeline on a compatible public corpus after sign-code crosswalking.”

**Defect:** This affects Targets 1–3 because the paper repeatedly asks readers to accept corpus-level exponents, positional tests, and validation claims while the primary corpus is unavailable. The author acknowledges this, but the claims are still presented with high numerical precision.

**Severity:** **MAJOR**

**Evidence that would settle it:** Public release of Holdat or a fully reproducible rerun on ICIT with code, crosswalk, and identical outputs.

## PASS 3 — NUMBERS SWEEP (reviewer finding IDs N1–N116)

N1. **Abstract:** “IVS, ca. 2600–1900 BCE.”  
**PARTIALLY CHECKABLE** — archaeological dating depends on cited background, not derived here.  
Arithmetic: span = 700 years. Sev: MINOR.

N2. **Abstract:** “Holdat LLC Indus Corpus V3 (1,670 seals, 9 sites, 390 distinct signs, 7,002 sign tokens).”  
**NOT CHECKABLE** — Holdat corpus is not public (§6); no corpus table/data release.  
Arithmetic only recurs with §2.1 site sum; see N17. Sev: CRITICAL.

N3. **Abstract:** “z = 10.3; 0/2000 permutations exceeded the observed statistic.”  
**NOT CHECKABLE** — no statistic definition/table/permutation outputs supplied; supplemental claimed but not in text.  
Arithmetic: 0/2000 = 0%; upper-bound p often <1/2001≈0.00050, but paper does not state p. Sev: CRITICAL.

N4. **Abstract:** “a recurring three-slot inscription formula.”  
**PARTIALLY CHECKABLE** — formula is described, but no full positional table provided.  
Arithmetic: “three-slot” matches later [Slot 1–3]. Sev: MAJOR.

N5. **Abstract:** “161 candidate readings at HIGH or MEDIUM confidence.”  
**PARTIALLY CHECKABLE** — internally 75 HIGH + 86 MEDIUM = 161 (§3.1), but anchor table/data absent.  
Arithmetic: 75+86=161 PASS; also 268−107=161 in Abstract/§3.1 PASS. Sev: MAJOR.

N6. **Abstract:** “90.96% token coverage.”  
**PARTIALLY CHECKABLE / INCONSISTENT** — later §3.1 says 6,363/7,002 tokens.  
Arithmetic: 6,363/7,002 = 90.87%, not 90.96%; 90.96% of 7,002 ≈ 6,369 tokens. FAIL. Sev: MAJOR.

N7. **Abstract:** “69.8% of seals fully covered by H+M candidates.”  
**PARTIALLY CHECKABLE** — later §3.6 gives 1,165/1,670.  
Arithmetic: 1,165/1,670 = 69.76% → 69.8% PASS. Sev: MINOR if corpus unavailable.

N8. **Abstract:** “0 isolated fish signs in the 1,670-seal corpus (0/113 across 9 corpus sites).”  
**PARTIALLY CHECKABLE** — fish-bearing count table given in §3.5, but raw corpus unavailable.  
Arithmetic: §3.5 fish seals 6+33+35+11+28=113; isolated all 0 PASS. Sev: MAJOR.

N9. **Abstract:** “0 in the Gulf deposit catalog (0/27; Laursen 2010), for a combined result of 0/140.”  
**PARTIALLY CHECKABLE** — 0/27 depends on Laursen extraction not shown.  
Arithmetic: 113+27=140 and 0+0=0 PASS. Sev: MAJOR.

N10. **Abstract:** “earlier count of 268 H+M signs included 107 heuristic placeholders.”  
**PARTIALLY CHECKABLE** — no prior table, but arithmetic aligns current count.  
Arithmetic: 268−107=161 PASS. Sev: MAJOR.

N11. **Abstract:** “Candidate readings show 59% overlap with Parpola (1994).”  
**PARTIALLY CHECKABLE** — later scope is 44/75 HIGH readings (§3.22), not all 161 candidates.  
Arithmetic: 44/75=58.67% → 59% PASS; scope wording in Abstract is broader than later. Sev: MAJOR.

N12. **Abstract:** “Internal consistency checks pass (59/59, Phases 1–170).”  
**NOT CHECKABLE** — no check list/results table supplied, only summary in Appendix C.  
Arithmetic: 59/59 = 100%. Sev: CRITICAL.

N13. **Abstract:** “Phases 1–170.”  
**NOT CHECKABLE** — phase reports said repository-available, not included; no derivation here.  
Arithmetic: inclusive count would be 170 phases if continuous, but not shown. Sev: MINOR.

N14. **§2.1:** “7,002 sign tokens, 1,670 seals, 9 sites.”  
**NOT CHECKABLE** — private Holdat corpus; no row-level data.  
Arithmetic cross-check with site counts in N17 PASS. Sev: CRITICAL.

N15. **§2.1:** “Mohenjo-daro (n=606), Harappa (n=492), Kalibangan (n=110), Dholavira (n=106), Lothal (n=124), Chanhu-daro (n=78), Surkotada (n=61), Banawali (n=60), Rakhigarhi (n=33).”  
**PARTIALLY CHECKABLE** — counts sum internally, but site assignment/data unavailable.  
Arithmetic: 606+492+110+106+124+78+61+60+33=1,670 PASS. Sev: MAJOR.

N16. **§2.1:** “390 distinct M-number signs attested in the corpus.”  
**NOT CHECKABLE** — no frequency table or corpus release.  
Arithmetic: paired with N17: 390 attested + 7 zero-token = 397 catalogue signs PASS. Sev: CRITICAL.

N17. **§2.1:** “anchor table assigns readings to all 397 signs … additional 7 have zero corpus tokens.”  
**PARTIALLY CHECKABLE** — arithmetic only; anchor table not included in text.  
Arithmetic: 390+7=397 PASS. Sev: MAJOR.

N18. **§2.1:** “Zipf exponent of about 1.7.”  
**NOT CHECKABLE** — paper itself says no derivation has been published.  
Arithmetic: none. Sev: MAJOR, mitigated because withdrawn as evidence.

N19. **§2.1:** “45-entry Mahadevan–Parpola crosswalk.”  
**NOT CHECKABLE** — JSON not supplied in text; no entry list.  
Arithmetic: none. Sev: MAJOR.

N20. **§2.1.1:** “Spec 068, executed as Phase-430; OSF registration 3pbwe.”  
**PARTIALLY CHECKABLE** — identifiers exist as claims, but registration content not in text.  
Arithmetic: none. Sev: MINOR/MAJOR depending repository access.

N21. **§2.1.1:** “One fitting rule — the Zipf–Mandelbrot rule frozen by Spec 053.”  
**NOT CHECKABLE** — rule not specified mathematically here.  
Arithmetic: none. Sev: MAJOR.

N22. **§2.1.1:** “applied to Indus sign counts and to four comparison systems.”  
**CHECKABLE internally only** — four systems are listed.  
Arithmetic: listed: numerical signs, heraldic charges, synthetic emblem, Linear B = 4 PASS. Sev: —.

N23. **§2.1.1:** “Shakti corpus … 3,045 analysable rows … 11,805 tokens; 557 distinct signs.”  
**NOT CHECKABLE** — Shakti/ICIT restricted corpus data not supplied.  
Arithmetic: tokens/row = 11,805/3,045 ≈ 3.88. Sev: CRITICAL.

N24. **§2.1.1:** “fit gave exponent α = 2.004 and fit error 0.1584.”  
**NOT CHECKABLE** — no counts, fit formula details, or output table.  
Arithmetic: none reproducible. Sev: MAJOR.

N25. **§2.1.1:** “wider set … α = 1.96 and error 0.1544.”  
**NOT CHECKABLE** — no wider-row definition/data.  
Arithmetic: error improves by 0.0040 vs 0.1584; α decreases by 0.044. Sev: MAJOR.

N26. **§2.1.1:** “Mesopotamian numerical signs (error 0.5335).”  
**NOT CHECKABLE** — comparison dataset not provided.  
Arithmetic: greater than Indus/Shakti errors. Sev: MAJOR.

N27. **§2.1.1:** “heraldic charges … (0.1839).”  
**NOT CHECKABLE** — Dering Roll data/process absent.  
Arithmetic: 0.1839 > 0.1584 and >0.1544. Sev: MAJOR.

N28. **§2.1.1:** “synthetic emblem process (median 0.2405).”  
**NOT CHECKABLE** — simulation design/output absent.  
Arithmetic: median error > Indus errors. Sev: MAJOR.

N29. **§2.1.1:** “Linear B (0.9229).”  
**PARTIALLY CHECKABLE** — value itself not reproducible, but comparison claim testable internally.  
Arithmetic: 0.9229 is largest among 0.5335, 0.1839, 0.2405, 0.1584/0.1544 PASS. Sev: MAJOR.

N30. **§2.1.1:** “Linear B … fitted the curve worst of the five.”  
**CHECKABLE internally** — if five = four comparators + Indus rule run.  
Arithmetic: max error is Linear B 0.9229 PASS. Sev: —.

N31. **§2.1.1:** “Phase-43 exponent of about 1.35.”  
**NOT CHECKABLE** — only says recorded in program files; files not included.  
Arithmetic: differs from §2.1 earlier “about 1.7” and Shakti 2.004/1.96; scopes differ. Sev: MAJOR.

N32. **§3.10:** “CISI corpus (179 inscriptions, Parpola P-numbers, mayig digitization).”  
**NOT CHECKABLE** — no CISI dataset/table shown.  
Arithmetic: none. Sev: MAJOR.

N33. **§3.10:** “87% of CISI multi-sign inscriptions open with an INITIAL-class sign.”  
**NOT CHECKABLE** — denominator for multi-sign inscriptions absent; no classification table.  
Arithmetic: 87% of 179 would be 155.7, but scope is multi-sign subset, denominator unstated. Sev: MAJOR.

N34. **§3.10:** “KL divergence on positional class distribution = 0.591.”  
**NOT CHECKABLE** — no class distributions or formula supplied.  
Arithmetic: none. Sev: MAJOR.

N35. **§3.10:** “1,916 deduplicated ICIT inscriptions (584 unique signs, 11,110 tokens).”  
**PARTIALLY CHECKABLE via citation only** — Nair external paper not included here.  
Arithmetic: tokens/inscription = 11,110/1,916 ≈ 5.80. Sev: MAJOR if citation lacks data.

N36. **§3.10:** “Zipf slope –1.49.”  
**PARTIALLY CHECKABLE via Nair only** — not derivable here.  
Arithmetic: sign convention differs from positive α claims; not directly reconciled. Sev: MAJOR.

N37. **§3.10:** “conditional entropy 3.23 bits.”  
**PARTIALLY CHECKABLE via Nair only** — no calculation/data here.  
Arithmetic: none. Sev: MAJOR.

N38. **§3.10:** “permutation null percentile 0.000 against 1,000 permutation trials.”  
**PARTIALLY CHECKABLE via Nair only** — no null outputs here.  
Arithmetic: 0/1000 exceedances would conventionally imply empirical p ≤0.001 or ≈0.001 by +1 rule; wording “percentile 0.000” needs definition. Sev: MAJOR.

N39. **§3.10:** “Phase-134 F1 positional test (z = 10.3; 0/2000 permutations exceeded…).”  
**NOT CHECKABLE** — repeats N3 with scope “Phase-134 F1”; no statistic details.  
Arithmetic: same 0/2000 = 0%. Sev: CRITICAL.

N40. **§3.10:** “matches the administrative baseline on only two of four metrics.”  
**PARTIALLY CHECKABLE via Nair only** — metrics not named here.  
Arithmetic: 2/4 = 50%. Sev: MAJOR.

N41. **§1.3:** “161 candidate readings … (90.96% token coverage; 69.8% seals…).”  
**PARTIALLY CHECKABLE / INCONSISTENT** — repeats N5–N7.  
Arithmetic: 161=75+86 PASS; 90.96 conflicts with 6,363/7,002 in §3.1 FAIL; 69.8=1,165/1,670 PASS. Sev: MAJOR.

N42. **§1.3:** “Phase-163 adds 4 provisional sibilant upgrades.”  
**PARTIALLY CHECKABLE** — §3.25/§3.27 list four signs.  
Arithmetic: M165, M330, M202, M198 = 4 PASS. Sev: MINOR.

N43. **§1.3:** “Identification of 2 Munda substrate loans.”  
**PARTIALLY CHECKABLE** — §3.3/§4.2 list M374 and M351.  
Arithmetic: 2 signs PASS; linguistic claim not independently checked. Sev: MAJOR.

N44. **§1.3:** “fish-sign isolation test: 0/140 isolated across all 9 sites and Gulf deposit catalog.”  
**PARTIALLY CHECKABLE** — repeats N8–N9.  
Arithmetic: 0/113 + 0/27 = 0/140 PASS. Sev: MAJOR.

N45. **§1.3:** “107 prior heuristic placeholders removed by Phase-133.”  
**PARTIALLY CHECKABLE** — arithmetic with earlier 268/current 161 passes.  
Arithmetic: 268−107=161 PASS. Sev: MAJOR.

N46. **§1.3:** “Rakhigarhi robustly distinct across all 5 site-pair comparisons.”  
**PARTIALLY CHECKABLE** — §3.14 mentions five comparisons but lists only two numerically.  
Arithmetic: no full five-pair table; cannot verify “all 5.” Sev: MAJOR.

N47. **§1.3:** “Tamil-Brahmi terminal phoneme cross-validation (73% TB category coverage).”  
**PARTIALLY CHECKABLE** — §3.18 gives 8/11.  
Arithmetic: 8/11=72.7% → 73% PASS. Sev: MINOR/MAJOR.

N48. **§1.3:** “44/75 HIGH-confidence readings overlap … Parpola (1994).”  
**PARTIALLY CHECKABLE** — no overlap list supplied.  
Arithmetic: 44/75=58.67% → 59%, consistent with Abstract N11 PASS. Sev: MAJOR.

N49. **§1.3:** “10/10 Mahadevan papers … consistent.”  
**NOT CHECKABLE** — no extraction table sufficient to judge consistency.  
Arithmetic: 10/10 = 100%. Sev: MAJOR.

N50. **§1.3:** “25 Ur III names tested — no discriminative match.”  
**PARTIALLY CHECKABLE** — §3.28 repeats, but name list/results not shown.  
Arithmetic: none. Sev: MAJOR.

N51. **§1.3:** “19/19 LOW blocker readings phonotactically plausible; coverage estimate 92.35% if promoted.”  
**PARTIALLY CHECKABLE / NOT REPRODUCIBLE** — §3.29 repeats; no blocker list/frequency contribution.  
Arithmetic: 19/19=100%; 92.35−90.96=1.39 percentage-point gain, tokens ≈97/7002. Sev: MAJOR.

N52. **§1.3:** “32 evidence items, 79.8% aggregate confidence, 18 items strongly/highly supported.”  
**NOT CHECKABLE** — scorecard items/weights absent.  
Arithmetic: 18/32=56.25%; 79.8% weighting cannot be checked. Sev: CRITICAL.

N53. **§1.3:** “93.2% sign-level accuracy at 161 H+M.”  
**PARTIALLY CHECKABLE** — §3.31 gives 137/147.  
Arithmetic: 137/147=93.20% PASS; denominator excludes 14 of 161 signs. Sev: MAJOR.

N54. **§2.2/§3.1:** “HIGH (75 signs), MEDIUM (86 signs), LOW (236 signs).”  
**CHECKABLE internally, NOT corpus-checkable** — no anchor table in text.  
Arithmetic: 75+86+236=397 PASS; H+M=75+86=161 PASS. Sev: MAJOR for missing table.

N55. **§2.2:** “Terminal marker evidence: sign appears in >95% of cases as inscription-final.”  
**NOT CHECKABLE** — criterion stated, no qualifying table except examples.  
Arithmetic: M342 later 96% terminal satisfies >95 if true. Sev: MAJOR.

N56. **§2.2:** “motif type with lift ratio > 5.0.”  
**NOT CHECKABLE** — no contingency tables for lift.  
Arithmetic: none. Sev: MAJOR.

N57. **§2.2:** “SA-consistency >= 0.15.”  
**NOT CHECKABLE** — language-model outputs absent.  
Arithmetic: threshold only; no score table. Sev: MAJOR.

N58. **§2.2:** “positional L1 distance < 0.2.”  
**NOT CHECKABLE** — no positional vectors/allograph pairs listed.  
Arithmetic: threshold only. Sev: MAJOR.

N59. **§3.1:** “Token coverage: HIGH 76.3%, MEDIUM 14.66%, LOW 9.34%, H+M total 90.96%.”  
**PARTIALLY CHECKABLE / INCONSISTENT** — percentages conflict internally.  
Arithmetic: HIGH+MEDIUM=76.3+14.66=90.96 PASS; all three =100.30 FAIL. Sev: MAJOR.

N60. **§3.1:** “161 H+M anchors … cover 6,363 of 7,002 corpus tokens.”  
**PARTIALLY CHECKABLE / INCONSISTENT** — fraction does not match stated 90.96%.  
Arithmetic: 6,363/7,002=90.87%; remaining 639/7,002=9.13%, not LOW table 9.34. FAIL. Sev: MAJOR.

N61. **§3.1:** “remaining 639 tokens (9.1%).”  
**CHECKABLE internally** — uses 7,002 denominator.  
Arithmetic: 639/7,002=9.126% → 9.1% PASS; conflicts with LOW 9.34% in table. Sev: MINOR/MAJOR.

N62. **§3.2/§3.3:** “M342 … most frequent terminal at 584 tokens”; “96% terminal.”  
**NOT CHECKABLE** — no sign frequency/position table.  
Arithmetic: if 584 tokens, 96% terminal ≈561 terminal tokens. Sev: MAJOR.

N63. **§3.3:** “M176 … 356 tokens, 94% terminal.”  
**NOT CHECKABLE** — no frequency/position table.  
Arithmetic: 0.94×356≈335 terminal tokens. Sev: MAJOR.

N64. **§3.3:** “M072 … All 12 tokens INITIAL.”  
**NOT CHECKABLE** — no token list.  
Arithmetic: 12/12=100% initial. Sev: MAJOR.

N65. **§3.4:** “M267 (corpus frequency=400)… unicorn 127, zebu 72, elephant 37, rhinoceros 25, etc.; distributed at 5.7% of all tokens.”  
**PARTIALLY CHECKABLE** — raw counts unavailable; percentage testable.  
Arithmetic: 400/7,002=5.71% PASS; listed motif subtotal 261, leaving 139 “etc.” Sev: MAJOR.

N66. **§3.4:** “actual fish sign is M047 (frequency=13).”  
**NOT CHECKABLE** — no crosswalk/frequency table.  
Arithmetic: 13/7,002=0.186%. Sev: MAJOR.

N67. **§3.5:** Fish table: “Lothal 6, Harappa 33, Mohenjo-daro 35, Dholavira 11, All others 28, Total 113; isolated 0; compound 113.”  
**PARTIALLY CHECKABLE** — table arithmetic only; corpus unavailable.  
Arithmetic: fish totals 6+33+35+11+28=113; compound same; isolated 0%. PASS. Sev: MAJOR.

N68. **§3.6:** “Total seals 1,670; fully covered 1,165 (69.8%); blocked 505 (30.2%); unknown 0 (0%); net gain +35.”  
**PARTIALLY CHECKABLE** — internal arithmetic passes; raw seal-level coverage absent.  
Arithmetic: 1,165+505+0=1,670; 1,165/1,670=69.76%; 505/1,670=30.24%. PASS. Sev: MAJOR.

N69. **§3.6:** “Site-level H+M-coverage rates range from 70% … to 93%.”  
**NOT CHECKABLE** — no site-level coverage table.  
Arithmetic: Rakhigarhi n=33 at 70% implies ≈23 seals, but not given. Sev: MAJOR.

N70. **§3.6:** “18 signs with corpus frequency 5–7 resist MEDIUM promotion.”  
**PARTIALLY CHECKABLE** — Appendix B lists 18 signs, but no frequencies.  
Arithmetic: listed signs count =18 PASS; frequency claim not checkable. Sev: MAJOR.

N71. **§3.7:** “1,670 seals, 7,002 tokens … 2,647 distinct bigrams, including 1,485 H+M-by-H+M bigrams.”  
**NOT CHECKABLE** — no bigram table except claimed supplemental.  
Arithmetic: H+M bigrams share =1,485/2,647=56.1%. Sev: MAJOR.

N72. **§3.7:** “M342·M176 … 122 seals (7.3% of corpus, PMI=2.43).”  
**PARTIALLY CHECKABLE** — percentage checkable; PMI not.  
Arithmetic: 122/1,670=7.31% PASS; PMI no derivation. Sev: MAJOR.

N73. **§3.7:** “M267·M099 84 seals; M099·M342 81; M176·M099 74; 97 formula types.”  
**NOT CHECKABLE** — no formula table.  
Arithmetic: none beyond counts. Sev: MAJOR.

N74. **§3.7:** “17/21 tested H+M signs show position-specific collocate profiles.”  
**PARTIALLY CHECKABLE** — no tested-sign list; arithmetic only.  
Arithmetic: 17/21=80.95% ≈ later “81%” PASS. Sev: MAJOR.

N75. **§3.7/§3.13:** “66.7% vs null mean 80.7%, n=1,000.”  
**NOT CHECKABLE** — no permutation outputs; also interpretation is unusual but stated.  
Arithmetic: if 21 signs, 14/21=66.7%; SD later 0.088. Sev: MAJOR.

N76. **§3.7:** “M267 … 81% MEDIAL in compound contexts.”  
**NOT CHECKABLE** — no context count/denominator.  
Arithmetic: none. Sev: MAJOR.

N77. **§3.8:** “394 INITIAL-sign × iconography pairs; 63 pairs (16%) significantly enriched.”  
**PARTIALLY CHECKABLE** — pair table absent, percentage checkable.  
Arithmetic: 63/394=15.99% → 16% PASS. Sev: MAJOR.

N78. **§3.8:** Enrichment rows: “20 vs 2.0 χ²158.5; 24 vs 2.9 χ²155.3; 23 vs 2.8 χ²148.8; 28 vs 5.8 χ²84.6; 43 vs 13.2 χ²66.9.”  
**NOT CHECKABLE** — no contingency totals; chi-square not reproducible from observed/expected alone.  
Arithmetic: all observed >> expected qualitatively; exact χ² needs full table. Sev: MAJOR.

N79. **§3.11:** “0/157 H+M readings contain Sanskrit-exclusive phonemes; 35/157 contain Dravidian-exclusive phonemes; ratio 35:0; 22%.”  
**PARTIALLY CHECKABLE** — no reading inventory audit; arithmetic passes.  
Arithmetic: 35/157=22.29% → 22%; 0/157=0%. Sev: MAJOR.

N80. **§3.11:** “four PROVISIONAL_MEDIUM sibilant additions … conservative at 161 anchors.”  
**PARTIALLY CHECKABLE / SCOPE SHIFT** — if all four are Dravidian-exclusive, updated count would be 39/161.  
Arithmetic: 39/161=24.2%, not stated; 0/161 remains 0%. Sev: MINOR.

N81. **§3.12:** “97 INITIAL-sign clusters (>=3 seals).”  
**NOT CHECKABLE** — cluster table absent.  
Arithmetic: threshold stated only. Sev: MAJOR.

N82. **§3.12:** Domain table: “845, 446, 145, 135, 99 seals; percentages 50.6, 26.7, 8.7, 8.1, 5.9.”  
**CHECKABLE internally** — table sums to corpus total.  
Arithmetic: seals sum 1,670; percentages match each count/1,670 and sum 100.0. PASS.

N83. **§3.13:** “Observed collocate divergence rate: 66.7% … KL >0.3 bits; null mean 80.7% (SD=0.088).”  
**NOT CHECKABLE** — no tested-sign denominator/output shown here.  
Arithmetic: if denominator 21, 14/21=66.7%; z vs null ≈(0.667−0.807)/0.088=−1.59. Sev: MAJOR.

N84. **§3.14:** “n=1,000 resamples … all 36 site-pair KL divergences across 9-site corpus.”  
**PARTIALLY CHECKABLE** — combinatorics passes; bootstrap results not shown.  
Arithmetic: C(9,2)=36 PASS. Sev: MAJOR.

N85. **§3.14:** “Mohenjo-daro vs Rakhigarhi KL=0.509 CI [0.483,0.750]; Harappa vs Rakhigarhi KL=0.481 CI [0.445,0.704]; all five … lower bounds >0.3.”  
**PARTIALLY CHECKABLE** — two CIs shown pass criterion; other three absent.  
Arithmetic: 0.483 and 0.445 >0.3 PASS for listed only. Sev: MAJOR.

N86. **§3.14:** “Mohenjo-daro vs Harappa … KL=0.070.”  
**NOT CHECKABLE** — no distributions.  
Arithmetic: none. Sev: MAJOR.

N87. **§3.15:** “four phonological slots … 2/4 slots covered; /i/ by 45 candidate signs; /li/ by 4 signs.”  
**NOT CHECKABLE** — no mapping table.  
Arithmetic: 2/4=50%; cited 45+4 sign coverage not verifiable. Sev: MAJOR.

N88. **§3.16:** “7 signs with ca-/ce-/ci-/co- phonemes … 17 DEDR-attested roots … ICIT 5,318 inscriptions vs 1,670.”  
**PARTIALLY CHECKABLE** — listed seven signs count passes; roots/corpus not verifiable.  
Arithmetic: 5,318/1,670=3.18×, consistent with “larger,” later “~3x.” Sev: MAJOR.

N89. **§3.17:** “V12 warning (75.3% vs 85% threshold).”  
**NOT CHECKABLE** — no vowel-harmony calculation or denominator.  
Arithmetic: shortfall =9.7 percentage points. Sev: MAJOR.

N90. **§3.18:** “TERMINAL-dominant … 7 signs; 4/7 match (57%).”  
**PARTIALLY CHECKABLE** — no sign profile table; arithmetic passes.  
Arithmetic: 4/7=57.14% PASS. Sev: MAJOR.

N91. **§3.18:** “11 categories … coverage rises to 8/11 categories (73%).”  
**CHECKABLE internally for arithmetic** — category list has 11 items.  
Arithmetic: 8/11=72.73% → 73% PASS. Sev: MINOR/MAJOR.

N92. **§3.18:** “V07 phonotactic violation rate … 23.4%.”  
**NOT CHECKABLE** — no denominator or violation table.  
Arithmetic: none. Sev: MAJOR.

N93. **§3.19:** “Mining 145,000 characters … Parpola Appendix … 4 attestations … 27 Indus-script contexts … 0/113 + 0/27 = 0/140.”  
**PARTIALLY CHECKABLE** — arithmetic passes, extraction not reproducible here.  
Arithmetic: 113+27=140; 0+0=0; 4 attestations cannot be checked. Sev: MAJOR.

N94. **§3.20:** “Wells (2015) … 161 pages; 284 sign references, 96 Dravidian language claims, 403-reference positional analysis appendix.”  
**PARTIALLY CHECKABLE via cited book only** — text-mining outputs not shown.  
Arithmetic: none. Sev: MAJOR.

N95. **§3.21:** “79 positional-class references and 61 grammar structure agreement hits.”  
**NOT CHECKABLE** — mining method/output absent.  
Arithmetic: none. Sev: MAJOR.

N96. **§3.22:** “Parpola (1994) … 1,566,507 chars; 44/75 … 59%; 6,869 genitive references; 47 classifier references.”  
**PARTIALLY CHECKABLE** — arithmetic passes; mining counts/list absent.  
Arithmetic: 44/75=58.67% →59% PASS. Sev: MAJOR.

N97. **§3.23:** “10 Mahadevan papers spanning 1972–2018: all 10 …; 8, 7, 6 hits; 10 settlement/ūr references.”  
**NOT CHECKABLE** — text-mining corpus counts not shown.  
Arithmetic: span 2018−1972=46 years; “four-decade” roughly OK. Sev: MAJOR.

N98. **§3.24:** “38 Mahadevan papers … yielded 0 new direct M-number assignments … LOW 240 then 236 after 4 promotions; H+M 161 current, 157 then.”  
**PARTIALLY CHECKABLE** — arithmetic coherent, mining not verifiable.  
Arithmetic: 240−4=236; 157+4=161 PASS. Sev: MAJOR.

N99. **§3.25:** “15 sibilant candidates … Four signs promoted based on >=3 independent text mentions: 4,4,4,3 references.”  
**PARTIALLY CHECKABLE** — listed four signs and reference counts; extraction not shown.  
Arithmetic: four promoted; all meet >=3. PASS internally. Sev: MAJOR.

N100. **§3.25:** “With these 4 additions: H+M =161 (was157), token coverage=90.96% (was90.75%), seal coverage=69.8% (was69.1%).”  
**PARTIALLY CHECKABLE / INCONSISTENT with token-count N60**.  
Arithmetic: 157+4=161 PASS; token gain 0.21 pp ≈15 tokens of 7,002; seal gain 0.7 pp ≈12 seals. Current 90.96 conflicts with 6,363/7,002. Sev: MAJOR.

N101. **§3.26:** “6 Meluhhan names … no >=3/4 matches; partial 2/3 slots: 17 seals … 9 seals … ICIT 5,318 texts gives ~3x.”  
**PARTIALLY CHECKABLE** — no name/result table.  
Arithmetic: 5,318/1,670=3.18× → “~3x” PASS. Sev: MAJOR.

N102. **§3.27:** “M198 … 3 references — just below the >=4 threshold.”  
**CHECKABLE internally** — threshold comparison explicit.  
Arithmetic: 3<4 PASS; note §3.25 said promotion based on >=3, so thresholds differ by purpose. Sev: MINOR.

N103. **§3.28:** “Expanding from 6 to 25 names … all 25 names produced apparent matches at >=50% threshold.”  
**NOT CHECKABLE** — no name list or match output.  
Arithmetic: expansion +19 names; 25/25=100% apparent matches. Sev: MAJOR.

N104. **§3.29:** “top 19 decode-blocking LOW signs … 19/19 plausible … coverage 90.96% -> 92.35%.”  
**PARTIALLY CHECKABLE** — no blocker list; arithmetic gain estimable.  
Arithmetic: gain 1.39 pp; ≈97 additional tokens if token coverage. But text says coverage estimate, not explicit token/seal scope. Sev: MAJOR.

N105. **§3.30:** “32 total evidence items (up from 23), 79.8% aggregate confidence (up from 69%), 18 items …; category 12/8/8/4.”  
**PARTIALLY CHECKABLE / NOT REPRODUCIBLE** — arithmetic categories pass, score not.  
Arithmetic: 32−23=9 new items; 12+8+8+4=32; confidence gain 10.8 pp. Sev: CRITICAL for weighted score.

N106. **§3.30:** “adversarial challenge battery 10/10.”  
**NOT CHECKABLE** — no battery items/results.  
Arithmetic: 10/10=100%. Sev: MAJOR.

N107. **§3.31:** “for each H+M sign with >=3 corpus tokens (147/161 qualify).”  
**PARTIALLY CHECKABLE** — no frequency table.  
Arithmetic: 161−147=14 signs excluded. Sev: MAJOR.

N108. **§3.31:** “93.2% sign-level grammar accuracy … 137/147 correctly classified.”  
**CHECKABLE internally for arithmetic** — underlying classification unavailable.  
Arithmetic: 137/147=93.197% →93.2% PASS. Sev: MAJOR for missing classification table.

N109. **§3.31:** “Phase-133’s 44.3% … different methodological definitions.”  
**NOT CHECKABLE** — old metric/denominator absent.  
Arithmetic: 93.2−44.3=48.9 pp difference; explanation cannot be tested. Sev: MAJOR.

N110. **§4.1:** “Arthaśāstra (4th century BCE, ca. 2,000 years after IVC).”  
**PARTIALLY CHECKABLE** — chronology approximate.  
Arithmetic: if IVC ends 1900 BCE to 4th c. BCE ≈1,500 years; from 2600 BCE ≈2,200 years. “ca. 2,000” is rough. Sev: MINOR.

N111. **§4.2:** “Two signs (M374=kul, M351=vī) … Munda substrate.”  
**PARTIALLY CHECKABLE** — internally lists two; linguistic basis not verifiable here.  
Arithmetic: 2 signs PASS. Sev: MAJOR.

N112. **§4.3 / Appendix B:** “Eighteen signs with corpus frequency 5–7 … account for 3.8% of corpus tokens.”  
**INCONSISTENT** — maximum possible tokens from 18 signs at freq 7 is 126.  
Arithmetic: 126/7,002=1.80%, not 3.8%; 3.8% would be ≈266 tokens, requiring avg 14.8/sign. FAIL. Sev: CRITICAL.

N113. **§4.4:** “7,002 tokens is small”; “phonological drift over 4,000 years.”  
**PARTIALLY CHECKABLE** — token count private; time depth approximate.  
Arithmetic: from 2600–1900 BCE to 2026 CE ≈3,925–4,626 years, so “4,000” plausible. Sev: MINOR.

N114. **Conclusion:** “z =10.3; 0/2000 …; 0/140 tested contexts; 161 H+M signs; 90.96% token coverage.”  
**PARTIALLY CHECKABLE / INCONSISTENT** — repeats key figures.  
Arithmetic: 0/140 combines correctly; 161 arithmetic passes; 90.96 still conflicts with §3.1 6,363/7,002. Sev: MAJOR/CRITICAL for unreproducible z.

N115. **§6:** “Holdat LLC Indus Corpus v3 is not publicly available.”  
**CHECKABLE from paper statement** — directly explains why corpus-level counts cannot be independently reproduced from text.  
Arithmetic: affects all corpus-derived counts above; severity generally MAJOR–CRITICAL.

N116. **Appendix C:** “59 independent checks … all pass”; “3.13x above null”; “397 M-numbers”; “390 attested; 397 catalogue; 7 zero-token.”  
**PARTIALLY CHECKABLE / NOT REPRODUCIBLE** — arithmetic 390+7=397 passes; 59 checks and 3.13× not shown.  
Arithmetic: 59/59=100%; 390+7=397 PASS. Sev: CRITICAL for check suite.
