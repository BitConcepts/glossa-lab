# WP8 — Exposure accounting and realistic negative controls

**Repair program:** Glossa Lab external-audit repair, 2026-10-26.
**Work package:** 8 of the governing brief (Work Package 8, “Establish exposure accounting and realistic negative controls”).
**Status of this document:** A design only. It builds no registry, runs no control, scores no reading, and validates no instrument. It specifies the registry schema, the grouping rules, and the control suite that any future discrimination or validation claim must satisfy before that claim is made. Where this document records the current status of the Step 0-G instrument line (§5), it reports completed records; it does not change them.
**Standing position, unchanged:** The script is not deciphered.

The plain-language idea behind this whole package is simple: a test only counts as independent if the material it tests on did not already shape the thing being tested. If a reading, a statistic, or a threshold was built by looking at certain inscriptions, those inscriptions cannot later be presented as a fresh check on it. This package makes that history explicit, sign by sign and artifact by artifact, so that no exposed dataset is ever relabeled as fresh validation.

---

## 1. The exposure registry — design

### 1.1 Purpose

The registry records, for each artifact, derived statistic, and source interpretation in the program, **where it influenced the work**: whether it shaped which candidates were generated, how data was prepared, where a threshold was set, or which model or design was selected. A validation split, a control, or a claim is then checked against the registry before it is called independent.

The registry is an accounting tool. It does not judge whether an influence was proper. Early, open use of material during exploration is normal and is recorded as exposure, not as a fault. The fault this registry exists to prevent is only one: presenting exposed material, later, as if it had never been seen.

### 1.2 Schema

One row per (subject, influence point) pair. A subject that influenced the work at two points gets two rows. The fields:

| Field | Content | Rules |
|---|---|---|
| `subject_id` | Stable identifier of the subject: an artifact (inscription, object, image, dataset file), a derived statistic, or a source interpretation (a named reading, crosswalk, or published claim, with its source) | Must resolve to a held record, a pin, or a named external source. Free-text subjects are not allowed |
| `subject_kind` | `artifact` / `statistic` / `interpretation` | Exactly one |
| `subject_pin` | Hash, version, or revision of the subject as used, where one exists | If no pin exists, the field records `unpinned` — it is never left blank and never filled with a later version’s pin |
| `influence_point` | The stage at which the subject influenced the work: `candidate_generation` / `preprocessing` / `thresholds` / `model_selection` | One per row. These four are the brief’s named points; a future extension adds a value by a dated design note, never by reusing one of the four to mean something else |
| `influenced_target` | What was influenced: the candidate set, pipeline, threshold, model, or design that the subject shaped, named by its own stable identifier and version | Must name the specific target. “The program generally” is not a valid target |
| `exposure_class` | `known-exposed` / `known-unexposed` / `UNKNOWN` | See §1.3. This is the registry’s load-bearing field |
| `evidence_basis` | The record that supports the exposure class: a dated run record, freeze record, coding file, commit, or design draft that shows the influence — or, for `known-unexposed`, the record that shows the separation (for example, a coding sealed and hash-pinned before the test material existed in the project, with the seal recorded) | For `UNKNOWN`, this field records what was checked and why it did not settle the question. It never records a guess as a basis |
| `lineage_group` | The source-lineage group the subject belongs to (§2.2) | Assigned at registration; changed only by a dated correction that keeps the old value visible |
| `object_family` | The object-family group the subject belongs to, where the subject is or derives from a physical object (§2.1) | `not-applicable` for subjects with no object basis, stated as such |
| `recorded_by` / `recorded_at` | Who or what created the row, and when | Append-only: corrections are new rows or dated amendments that preserve the original entry |
| `notes` | Anything needed to interpret the row, in plain language | Never used to carry a fact that belongs in a field above |

### 1.3 The exposure classes — and the rule for unknown

- **known-exposed:** a record shows the subject influenced the named target at the named point.
- **known-unexposed:** a record shows the separation — the target was fixed (sealed, frozen, or hash-pinned) without the subject, or the subject did not exist in the project when the target was fixed, and the timing is itself recorded.
- **UNKNOWN:** the available records do not settle whether the subject influenced the target.

> **Unknown stays unknown.** An `UNKNOWN` class is a final answer for that row until a record settles it. It is never resolved by plausibility, by memory, by how the work “must have” proceeded, or by the needs of a validation design that would prefer the row to be unexposed. Any validation that depends on a row classed `UNKNOWN` must either treat the subject as exposed for that validation, or report the validation as conditional on an unresolved exposure — stated in the validation’s own record, in those words.

Two further rules:

- **Exposure is relative to a target, not a property of a subject.** The same inscription may be known-exposed for one candidate set and known-unexposed for another that was sealed before it was consulted. Rows therefore always name their target, and no report may shorten a row to “this artifact is exposed” without its target.
- **The registry is append-only.** A corrected row keeps its original entry visible with a dated correction beside it. This matters because a validation already published against the old entry must remain interpretable.

### 1.4 How the registry is used — the pre-claim check

Before any future discrimination or validation claim is filed, its record must include an exposure statement produced from the registry:

1. Every artifact, statistic, and interpretation that influenced the claim’s candidate generation, preprocessing, thresholds, or model selection is listed, with its rows.
2. Every item in the claim’s test or validation material is listed, with its exposure class relative to the claim’s targets.
3. Any overlap — test material that is known-exposed to any of the claim’s targets — is named, and the claim is restated to match: either the exposed items are removed and the claim is re-stated on the remainder (with the reduced denominator reported), or the claim is labeled a consistency check on exposed material, not a validation.
4. Any `UNKNOWN` item the claim depends on is named, with the treatment required by §1.3.

A claim filed without this statement is incomplete under this design, whatever its numbers say.

---

## 2. Grouping rules for validation splits

A validation split that separates copies of the same thing — putting one impression of a seal in the fitting set and another impression of the same seal in the test set — manufactures independence that does not exist. Splits are therefore made by group, never by row.

### 2.1 Object-family grouping

Inscriptions and artifacts are grouped into **object families**: sets that share a physical origin or a copying relationship, including at least:

- repeat impressions of the same seal or die;
- the same physical object recorded more than once (multiple faces, multiple photographs, multiple catalog entries for one object);
- duplicate publications of the same object;
- duplicate transcriptions of the same object, including the same inscription carried in two compilations.

**Rule:** all members of an object family fall on the same side of any validation split. A split is specified by listing its families, not only its rows, and a split record that cannot state its families has not shown that its sides are independent at the object level.

Where family membership is itself uncertain — a possible but unconfirmed duplicate — the uncertain pair is grouped together for splitting purposes and the uncertainty is recorded. Grouping on suspicion costs a little data; splitting a true family costs the validation’s meaning.

### 2.2 Source-lineage grouping

Artifacts and interpretations are also grouped by **source lineage**: the chain of derivation that produced them. Material belongs to one lineage group when it descends from a common source in a way that makes agreement expected rather than informative. At minimum:

- compilations that share a lineage (transcriptions, sign lists, or crosswalks derived from the same underlying compilation or from each other) are one lineage group for validation purposes;
- a derived statistic and the data it was derived from are one group;
- an interpretation and any comparator, crosswalk, or restatement copied from it are one group — agreement inside the group is restatement, not corroboration;
- synthetic or generated material is grouped by its generator and its calibration sources: a generator calibrated on a corpus shares lineage with that corpus for any validation that uses both.

**Rule:** a validation may not place a subject in its test material if a member of the subject’s lineage group influenced the target being validated — unless the resulting claim is labeled, in its own record, as within-lineage consistency rather than independent validation.

The two groupings are applied together: a split must respect object families **and** source lineages. Passing one grouping does not excuse failing the other.

---

## 3. The negative-control suite — design for any future discrimination or validation claim

### 3.1 What the suite is for

Any future claim of the form “this procedure can tell a right reading from a wrong one,” “this candidate beats its rivals,” or “this instrument validates at its stated accuracy” must face the whole search procedure — not just its final scoring step — against controls that are wrong in realistic ways. Random shuffles alone are not enough: a shuffle is wrong in a way no serious rival is wrong, and beating only shuffles has repeatedly, in this program’s own record, coexisted with losing to a simple baseline.

The suite below is the standing design. A future study adopts it in its own draft, states its own bars, and may add controls. It may not remove a control family without stating, in its draft, why that family cannot arise for its claim — and that statement is part of what its freeze review judges.

### 3.2 The control families

| # | Control family | What it is | What it tests |
|---|---|---|---|
| C1 | **Meaning permutations** | The proposed meanings or values are permuted among the signs they are assigned to, keeping the assignment machinery, the corpus, and every other choice fixed | Whether the procedure’s result depends on *which* meaning goes with *which* sign, or only on the shape of the assignment as a whole |
| C2 | **Frequency- and position-matched wrong mappings** | Wrong sign-to-value mappings built to match the proposed mapping’s frequency profile and positional profile | Whether the procedure prefers the proposal for any reason beyond “frequent signs in their usual positions fit well” — the baseline failure that ended two Step 0-G instruments (§5) |
| C3 | **Plausible wrong morphology** | Candidate readings with the proposed reading’s morphological machinery (affix shapes, unit structures, boundary placements) applied wrongly — wrong segmentation, wrong affix assignment, wrong unit structure — at the same level of internal plausibility | Whether the procedure detects morphological fit, or merely rewards any internally tidy morphology |
| C4 | **Matched homophony / polyphony flexibility** | Rival candidates given the same freedom the proposal uses: the same allowance for one sign carrying several values, or several signs carrying one value | Whether the proposal wins only because it was allowed more flexibility than its rivals. Flexibility is a budget; rivals get the same budget |
| C5 | **Wrong-language candidates** | Complete candidate readings drawn from a language other than the proposed one, carried through the identical procedure with the identical evidence | Whether the procedure identifies the proposed language, or certifies whichever complete candidate is placed before it |
| C6 | **Structured non-language corpora** | Calibrated generators of structured, non-linguistic inscription-like material (the program’s S4 discipline: seal-like administrative / emblem material with real internal structure, calibrated to the target corpus’s gross statistics before it is allowed to judge anything) | Whether the procedure certifies structure that is not language. A generator that fails its calibration checks does not run as a control, and the leg is reported outstanding — it is never tuned after the fact until it passes or fails as desired |

### 3.3 Fairness conditions across competitors

Controls are only meaningful if the contest is fair. For every comparison under this suite, the draft must state, before any run:

- **Matched tuning budget:** every competitor — the proposal and each control candidate — receives the same number of fitting attempts, the same search effort, and the same opportunity to adjust its free choices. A proposal tuned twenty ways against rivals tuned once has not won a comparison; it has won a budget.
- **Matched available evidence:** every competitor is built from, and judged on, the same evidence, subject to the same exposure rules (§1) and the same grouping rules (§2). Giving the proposal access to material its rivals are denied — or judging rivals on harder material — invalidates the comparison and must be reported as invalidating it, not footnoted.
- **The whole procedure is challenged, not only the scorer:** candidate generation, preprocessing, thresholds, and model selection are all inside the test. A control that is fed into the scorer only after the proposal’s candidates were generated with knowledge the control never had has not challenged the procedure; it has challenged its last step.

### 3.4 Three different questions, kept separate

A future claim must state which of these it is making, and may not borrow the language of one to dress the result of another:

1. **Classification:** does the procedure sort items into stated classes (for example, language-like / not language-like; reading accepted / not accepted) at stated rates? Reported with sensitivity, false-acceptance rate, and abstention rate (§3.5).
2. **Candidate ranking:** among a stated set of candidates, does the procedure rank the proposed candidate above its rivals? A ranking result says the proposal beat *those rivals, under those budgets*. It does not say the proposal is correct, and it does not say the procedure would accept it standing alone.
3. **Calibrated acceptance:** does the procedure accept the proposal at a threshold whose error rates were fixed in advance and measured on controls? Only a calibrated-acceptance result can support language such as “validated at the stated rate” — and only for the scope the controls covered (§4).

### 3.5 Rules that must be prespecified before any claim

No discrimination or validation claim may be filed under this design unless its draft stated, before any control ran:

- **Sensitivity:** the rate at which the procedure must accept or correctly rank known-answer true cases, and the known-answer material that measures it (independently coded; see Work Package 7, §2.3, Note 3, for the same requirement in the bridge line).
- **False-acceptance rate:** the maximum rate at which the procedure may accept, or rank first, any control candidate, stated per control family in §3.2 — a single pooled rate that lets one family fail silently inside an average is not acceptable.
- **Abstention / eligibility rules:** which items the procedure is allowed to decline to judge (for example, items below a stated attestation floor), how abstentions are counted, and the rule that abstentions are never counted as successes or silently removed from a denominator. An item the procedure cannot judge is reported as unjudged, with its line kept visible — the same discipline as the informative-denominator rule in Work Package 7.
- **Eligibility of controls:** which control instances count (calibration passed, floors met, exposure checked), stated before the run, so that a control cannot be excluded after it produces an inconvenient result.
- **Stop rule:** what outcome ends the study and with what closure word, including the outcome in which the procedure passes some families and fails others.

### 3.6 The non-identifiability rule

> **If two or more readings are observationally equivalent under the available evidence — that is, every observation the procedure can make is equally consistent with each of them — the result is reported as non-identifiability. The procedure does not pick the best-looking one.**

“Best-looking” includes highest-scoring under a compatibility score, most familiar to the reviewers, and most consistent with a preferred language hypothesis. A tie that the evidence cannot break is a finding — it states exactly what new kind of evidence would be needed — and it is filed as a finding, at full strength, not resolved by preference.

---

## 4. Scope limits, stated plainly

These limits bind every use of this design, and any report that uses the suite must carry the ones that apply to it:

- **A structured fake passing a diagnostic defeats that diagnostic — nothing more.** If a calibrated structured non-language corpus produces the signature a diagnostic claims to detect, the diagnostic is retired from that use. This says nothing about whether the Indus script is linguistic: a script can be a language and still be measured by a bad instrument.
- **Passing a finite suite licenses only the tested scope.** A procedure that survives these six control families, at these scales, on this material, has earned a claim about exactly that: those families, that scale, that material. It has not earned a general claim about correctness, about other scales, or about material the suite never touched.
- **Descriptive censuses do not require a fake-language control.** A census — a count or description of what a named corpus contains — requires accurate provenance and stated uncertainty: what was counted, from which pinned source, under which rules, with what gaps and what error bounds. It does not automatically require a non-language control, a power calculation, or a discrimination test. Imposing validation machinery on descriptive work does not make the description stronger; it misstates what kind of claim a description is. (Work Package 9 applies this limit to the contact-zone catalog leg and the completeness design.)

---

## 5. The Step 0-G line under this design — status, and the named successor direction

The Step 0-G line is the program’s attempt to build a scoring instrument at the scale of the 44 pending readings (Method M4’s gate), validated by planted recovery, a wrong-decipherment null, and a structured-generator control. Its record to date is the clearest worked example in the program of why §3’s suite is designed as it is. The status, from the three validation records, is:

| Instrument | Verdict | Core numbers | Reading under this design |
|---|---|---|---|
| **G44** (first instrument) | **FAILED** — planted-recovery leg | Planted batch score 0.442 against a bar of 0.60; 8 of 44 signs recovered against a bar of 33; a per-sign frequency baseline scored **0.767**, beating the planted truth by 32 points. The permutation null was passed (planted score at the 100th percentile of 9,999 shuffles). The structured-generator leg was **outstanding**: its generator failed calibration (12,687 tokens against a ceiling of 12,395; most-frequent-type share 0.0075 against a floor of 0.04) and was not tuned after the fact | The textbook case for control family C2 and §3.3: beating every shuffle (C1-class evidence) coexisted with losing to a frequency-matched baseline. Necessary is not sufficient |
| **G44-S** (successor) | **FAILED** — planted-recovery leg and frequency-baseline leg | Planted batch score 0.405 against 0.60; 2 of 44 signs recovered; baseline 0.570, a margin of **−0.165** against a bar of +0.05. Permutation null passed (100th percentile). The structured-generator leg **ran and passed**: the quota generator passed all five calibration checks, and the strongest claimable batch on the fake corpus scored 0.489 and was not certified, failing four certification conditions on substance. The diagnostic placed the failure in the generator’s own machinery: its planted neighbor tilts overwrote the planted parameters before the scorer saw them (mean planted concentration 0.702; mean realized share 0.440 / 0.434 in the two compilations) | The suite working as designed on both sides: the structured control (C6) is now proven runnable and discriminating, and the baseline leg still caught what the null could not |
| **G44-S2** (second successor) | **INCOMPLETE — GENERATION DEFECT. Kill criterion K2 TRIGGERED** | The run stopped before any leg: its profile-ledger construction could not reconcile the planted parameter family’s implied column sums with its skeleton’s role totals (step-2 column sums off target by +319 / −1,401 / +405 / +677), and its only repair operation provably cannot move mass between columns, so no implementation of the construction as drafted can succeed. No gate criterion was evaluated; no leg ran; no batch, baseline, or fake was scored. A separate swap-picker defect in the run’s implementation advanced the stop without changing the outcome, and is recorded as a defect in that record | K2’s meaning, in the draft’s own terms: the defect is in the validation family — the synthetic planted-parameter family cannot be jointly realized at census scale within tolerances. Under K2 there is no further generator iteration under this parameter family. K1 (the scorer is the defect) was expressly **not** triggered: the scorer was never judged in this run, and no evidence against it may be read into this record |

**Consequence, unchanged by this design document:** Step 0-G remains unsatisfied. Method M4 remains **GATED — DRAFT ONLY**; its pilot remains inside the gate and may not run. The 44 pending readings are untouched and unscored, and carry no weight.

**The named successor direction:** the G44-S2 draft’s own named redirect, recorded in its validation record, is **semi-synthetic implantation** — planting prediction pairs into the real corpus background by relabeling, so that realization is inherited from real distributional structure instead of manufactured by a synthetic parameter family — or, alternatively, a different gate design for M4 altogether.

> **Semi-synthetic implantation is an owner decision. This work package prepares the accounting and control design such a study would have to satisfy (§§1–3); it does not design the implantation study, does not authorize it, and does not start it.**

Any future implantation draft would, under this design, have to state before any run: its exposure rows for every relabeled item (§1 — relabeling is candidate generation and preprocessing, and the real-corpus background’s exposure to every prior target must be classed, with unknowns left unknown); its object-family and lineage groups (§2 — implanted items inherit their host objects’ families); its full control suite with matched budgets (§3); and its prespecified sensitivity, false-acceptance, abstention, and eligibility rules (§3.5).

---

## 6. Package status

| Part | Status |
|---|---|
| §1 Exposure registry schema | **Prepared** — design only; no registry built by this work |
| §2 Grouping rules (object family, source lineage) | **Prepared** — design only |
| §3 Negative-control suite, fairness conditions, prespecified rules, non-identifiability rule | **Prepared** — standing design for adoption, study by study, in each future study’s own draft |
| §4 Scope limits | **Prepared** — binding statement of limits for any use of the suite |
| §5 Step 0-G status | **Recorded** — G44 FAILED, G44-S FAILED, G44-S2 INCOMPLETE with K2 triggered; semi-synthetic implantation noted as the named successor direction, **gated on the owner’s decision — not started** |

**No study was executed, frozen, or registered by this work package. No control was run. No reading was scored.**
