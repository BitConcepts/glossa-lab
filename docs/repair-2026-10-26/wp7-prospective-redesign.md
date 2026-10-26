# WP7 — Prospective redesign: structural calibration

**Repair program:** Glossa Lab external-audit repair, 2026-10-26.
**Work package:** 7 of the governing brief (Work Package 7, “Redesign structural calibration prospectively”).
**Status of this document:** Prospective design notes only. Nothing in this document is frozen, executed, or registered. No completed study’s record, bar, or threshold is edited by this document. Where an errata note is drafted in §1, it is drafted ready to append — it is **not** appended here to any frozen record.
**Standing position, unchanged:** The script is not deciphered.

This document reconciles the brief with the records as they actually stand on 2026-10-26. The main correction to a casual reading of the brief is this: the M13 design in the brief is not a hypothetical future design. It was drafted, frozen as Spec 078, and its pilot ran. Its outcome governs what a successor may claim. Section 2 is written to that outcome, not to the draft alone.

Sources reconciled, all in the goal files:

- Spec 076 pilot record — `2026-10-26-m12-pilot-record.md`
- M13 draft — `2026-10-26-spec-draft-m13-projected-constraint-bridge-redesign.md`
- Spec 078 (M13) pilot record — `2026-10-26-m13-pilot-record.md`
- M14 pilot record (iteration 1) — `2026-10-26-m14-pilot-record.md`
- M14 iteration 2 pilot record — `2026-10-26-m14-iteration2-pilot-record.md`
- Spec 077 (M7) freeze and execution record — `2026-10-26-spec-077-m7-freeze-and-execution-record.md`

---

## 1. Spec 076 — endpoint correction (errata note, ready to append)

### 1.1 What Spec 076 actually found

Spec 076 (Method M12, the projected-constraint corpus model) ran once, exactly as frozen. Freeze digest: `83259ed3d3a20189e5c22e4645d26452c9c3b79a60348b3f5c38b8405addde9a`.

Its results split into two separate endpoints, and they must stay separate:

**Endpoint A — the step-2 descriptive shuffle endpoints: PASSED, by wide margins.**

- Step 0 (reproduction) and Step 1 (derivation) passed exactly: 11,507 tokens; 5,883 strict tokens; slot totals initial 2,655 / medial 5,972 / final 2,655 / solo 225; finals partition strict 1,707 / pending 250 / anchored-other 520 / no-anchor 178; 677 (sign, type) exclusions over the 122 no-anchor signs; solo-only set 13.
- Step 2 used a marginals-preserving shuffle, 999 draws, seed 20261026:
  - U2 finals residual: real value **178**; null minimum 371, 5th percentile **395.0**, median 421, maximum 474. No shuffle reached the real value (empirical fraction 0.000). Bar — real value below the null 5th percentile: **passed**.
  - Solo-only sign count: real value **13**; null median 2, 95th percentile **5.0**, maximum 12. No shuffle reached the real count (empirical fraction 0.000). Bar — real value above the null 95th percentile: **passed**.

In plain language: in the tested family, the frame’s pattern — unread signs being short of final positions, and solo-only signs being concentrated — is larger than the frame’s own sign frequencies (its marginals) produce by chance in any of 999 shuffles.

**Endpoint B — the step-3 bridge (positive control): FAILED.**

- The 94 strict signs were coded blind, from their `reading` + `basis` texts only, under rules CR-1 to CR-7, into the draft’s nine positional types.
- Of 89 frame-attested signs, **36 claimed types were excluded**, against a frozen bar of **at most 5**. By coded type: ONLY-INIT 22 of 28, ONLY-FIN 8 of 8, ONLY-MED 6 of 7.
- Closure word, as frozen: **PILOT FAILS — ASSUMPTION SET DOES NOT HOLD.** Claim F076-C02 was not filed. No register was produced.

The pilot record’s own texture, recorded there and not re-adjudicated here: 22 of the 36 exclusions were distributional summaries (“INITIAL position (freq=…), distributional assignment”) coded as exclusivity claims; all 8 ONLY-FIN exclusions were functional terms (“terminal marker,” “case suffix”) coded as positional exclusivity; the ONLY-MED exclusions were summaries and a grammar-slot inference coded the same way.

### 1.2 The errata note — text ready to append

> **Errata note to the Spec 076 pilot record — endpoint separation and the meaning of a failed bar. Drafted 2026-10-26 under repair Work Package 7. This note corrects an implication; it does not change any count, bar, or verdict in the record it would be appended to.**
>
> 1. **The two endpoints are separate findings and must be reported separately.** The step-2 shuffle endpoints passed both pre-committed bars by wide margins. The step-3 bridge control failed its pre-committed bar (36 exclusions against at most 5 allowed). Neither result rescues or cancels the other. The pilot’s overall closure word — ASSUMPTION SET DOES NOT HOLD — is the verdict on the full assumption set as frozen, which required both endpoints. It is not a verdict that the step-2 finding fell.
> 2. **Failing a significance bar does not prove the marginals-only explanation.** As a general rule for this program: if a statistic does not pass its shuffle bar, that shows only that the test, as built, did not separate the observed value from what the marginals produce by chance. It does not prove that the marginals are the true or only explanation. A failed bar can also reflect a weak statistic, a wrong shuffle family, too little data, or a real pattern the chosen statistic does not measure. Any record that moves from “the bar was not passed” to “therefore the marginals explain the pattern” states more than the test established, and that move is corrected wherever it was implied.
> 3. **For Spec 076 in particular, the converse also holds and must not be blurred.** The step-2 endpoints *did* pass. Their passing establishes, in the tested family only: the frame’s constraint pattern, as measured by the two named statistics, exceeds what its own marginals produce by chance in 999 shuffles. It does **not** establish: that any particular sign reading is correct; that the bridge from basis language to positional types is sound (the bridge is the endpoint that failed); that a register was licensed (none was produced); or anything about any sign’s meaning.
> 4. **What the bridge failure establishes, and what it does not.** It establishes: the machinery as frozen — the nine-type positional vocabulary, coding rules CR-1 to CR-7, and the assumption that a type-claim carries its full distributional content (A-FACE, in its Spec 076 form) — excluded the strict core’s own blind-coded claimed types 36 times in 89, so that assumption set, as an instrument for judging completions at face value, does not hold. It does **not** establish: that the strict core’s readings are wrong (the design’s stated presumption, unreversed by this record, is that the machinery is indicted first); that the step-1 derivation is false (its arithmetic is untouched by the control’s failure); that the necessity program is empty (the step-2 finding stands, and the Tier-C derivation exists as a computation exactly as computed); or anything about any sign’s meaning.
>
> **Reporting rule going forward:** any summary of Spec 076 must name the two endpoints separately, with the numbers above, and must carry each endpoint’s “establishes / does not establish” limits with it. A single-sentence summary that reports only the closure word, or only the step-2 pass, is incomplete.

That text is the deliverable for this part of the package. It has not been appended to the frozen pilot record by this work package, and no frozen record has been edited.

### 1.3 Why the correction matters beyond Spec 076

The same blur — treating “did not pass a bar” as proof of the null explanation, or treating one endpoint’s pass as a pass for a whole design — is the failure mode the successor designs in §2 to §4 are built to prevent. Every successor note below therefore reports each claim type on its own denominator, with its own standard, and states what a failure on that line would and would not show.

---

## 2. M13 successor design notes — reconciled with Spec 078’s actual outcome

### 2.1 History that is closed and untouchable

The M13 draft (`2026-10-26-spec-draft-m13-projected-constraint-bridge-redesign.md`) redesigned the bridge that failed in Spec 076. Its main changes were:

- a two-axis vocabulary — a **distributional** component (where a sign’s tokens occur) kept separate from a **functional** component (what the sign’s value does in its unit: TERM-FUNC, INIT-FUNC, MED-FUNC, SOLO-FUNC);
- new coding rules NC-1 to NC-8, replacing CR-1 to CR-7, including: universal positional language codes a distributional claim; functional language codes a functional claim only; sample-marked positional language codes a **summary**, not a checkable claim; compound bases are coded whole, never collapsed to a single strongest type; genuine ambiguity codes the weaker strength, with the ambiguity recorded;
- a successor assumption, A-FACE-2: a claim binds its maker at the strength at which it is stated, and at no other strength, and no claim may be re-stated at a different strength after the census is consulted;
- a successor pilot with a pre-committed bar.

That draft was frozen as **Spec 078** and its pilot ran once, exactly as frozen (freeze merge PR #418, merge commit `e8376d74a29be79114b933391dde34c479a53dcc`; freeze digest `d7ccfae47bcb771bca1c332bdb0f64eb7ef8de23de28d166aba9fb995961427b`; OSF registration 49fgu, filed 2026-10-26T16:00:51Z, admin approval still pending at the time of the pilot record — the registration act itself is recorded as complete in that record).

**The operative design of that completed study — recorded here as history, not as a proposal — was:**

- **Counted panel: 86 signs** (94 strict signs, minus 5 frame-absent signs counted neither way, minus 3 worked-example signs — M002, M342, M347 — coded but excluded from the count and reported on their own line).
- **Failure bar: at most 3 failures** in total among the counted population, with neither the distributional line nor the functional line exceeding 2.
- **Administrability bar: at least 25 of the 86 counted signs** yielding at least one checkable claim (distributional or functional).

Those three numbers — **86 / at most 3 / at least 25** — are a completed study’s thresholds. They are untouchable. No successor note in this document, and no future draft, may present them as adjusted, reinterpreted, or re-run under different values. A successor that wants different numbers must state them as its own, in its own draft, before its own freeze, and must say plainly that they are new.

### 2.2 What Spec 078 found

**Verdict: PILOT CLOSES — CANNOT BE ADMINISTERED: THE CORE MAKES TOO FEW CHECKABLE CLAIMS.**

- Step 0 passed exactly. The inherited census reproduced a fourth independent time (11,507 tokens; 5,883 strict tokens; the same slot totals and finals partition as Spec 076), so the inherited Spec 076 step-2 standing stood, as the design provided.
- The blind coding, checked mechanically against the census, yielded checkable claims from **7 of the 86 counted signs**, against the frozen floor of **25**. Seven is less than 25, so the pilot closed at the administrability door. Claim F078-C02 was not filed. No register was produced.
- The coding totals over all 94 strict signs: **0 distributional type-claims**; **12 functional claims** (TERM-FUNC 6, MED-FUNC 4, INIT-FUNC 2, SOLO-FUNC 0); **38 summaries**; 50 codings in all across 44 signs; **50 signs with no codable content of any kind** under the rules (semantic identifications, glosses, corroborations).
- The zero on the distributional line was verified independently in the pilot record: the words “never,” “always,” and “only” occur in none of the 94 bases, and every “exclusive” phrase in the bases (13 signs) asserts exclusivity over seal motifs, not over positions. Read honestly under NC-1, the strict core states no positional universal at all.
- The 7 counted checkable claims were all functional. Five were incoherent by the pilot’s own functional standard (anchor share below the slot base rate computed from the census): M267 TERM-FUNC 0.0266 against 0.2307; M305 TERM-FUNC 0.0000 (no final occurrence in this frame); M336 TERM-FUNC 0.0388; M351 MED-FUNC 0.0000 (no medial occurrence in this frame); M367 TERM-FUNC 0.1667. Two were coherent: M176 TERM-FUNC and M375 INIT-FUNC. These failure counts are recorded in the pilot record as observations, because the pilot closed at administrability before the failure bar became the verdict’s basis.
- On the worked-example line (excluded from the count, as designed): M342 TERM-FUNC coherent (anchor share 0.6876 against 0.2307) and M347 MED-FUNC coherent (0.8218 against 0.5190) — the blind coder, who never saw the draft’s worked examples, coded both flagship bases exactly as the design’s examples did. M002’s summary (INITIAL, n = 16) did not transfer to this frame: the sign’s plurality here is medial. No failures attach to summaries, by design.
- On the counted summary line: 36 summaries; the named position held the sign’s plurality in this frame in 15 cases and did not in 21. Filed as a tendency observation only.
- A-FACE-2 was adjudicated in the pilot record as **neither confirmed nor falsified**: its residue falsifier did not fire (the two residue candidates, M222 and M233, were adjudicated not to be residue cases, with grounds stated in that record), and its pattern-mode falsifier did not fire either, because the pilot did not fail by the failure bar — it closed one door earlier, at administrability, on a finding about the core’s language, not about the bridge.

In plain language, the finding is about the strict core’s basis language itself: read at the strength at which it is actually stated, that language is overwhelmingly distributional summaries (reports about a sample) and semantic identifications (claims about referents). It makes almost no claims of the kinds a census can judge. The pilot record states the figure plainly: 7 of 86 counted signs (8%) yielded a checkable claim, against a design premise that assumed enough stated claims existed to calibrate a bridge against.

**What Spec 078 establishes:** the census reproduces exactly; the redesigned bridge can be administered honestly — its rules, applied blind, produce a complete and auditable coding; and the calibration premise of the register route, as designed against this core, is false.

**What Spec 078 does not establish:** that the bridge is wrong (it was barely exercised); that the strict core’s readings are wrong (summaries and glosses are not false for being uncheckable, and no reading was re-judged); that the necessity program is empty (the step-2 finding stands); or anything about any sign’s meaning.

One further gap surfaced by the blind coding is carried into any successor as an open design item, not as a patch to Spec 078: rules NC-1 to NC-8 say nothing about assertions that a basis itself retracts or supersedes inside its own text. Three signs carry such passages (M047, M063, M267). The pilot coder coded the retracted material as no current claim and recorded the passages verbatim; that reading was adopted for that record. A rule for retracted material is a successor draft’s to write.

### 2.3 Successor design notes — what a future M13 successor must do differently

These are design notes for a future draft. They are not a draft, not a freeze, and not a pilot design with operative bars. Any successor must state its own panel, bars, and closure words in its own draft, before any freeze, and must be judged as Spec 078 was.

**Note 1 — Separate three kinds of claim, each with its own observable evidence.**

Spec 078 separated distributional claims from functional claims and from summaries. A successor must keep that separation and add the third content kind the brief names, which neither Spec 076 nor Spec 078 had a clean home for:

| Claim kind | What it asserts | Observable evidence that can judge it | What cannot judge it |
|---|---|---|---|
| **Distributional claim** | Where a sign’s tokens occur, stated at universal strength (“only,” “never,” “always,” “exclusively” over positions) | The sign’s census row in a named frame: an attested occurrence in a claimed-forbidden position contradicts it, mechanically | A summary’s sample, a functional coherence rate, or compatibility with a completion |
| **Word-boundary claim** | Where a unit (word or equivalent) begins or ends relative to the sign — for example, that the sign’s value closes a unit, opens a unit, or occurs only unit-internally | Evidence about units, stated independently of inscription edges: a named segmentation or unit analysis, with its own controls, in which the sign’s position *within its unit* is observable. Inscription-initial / inscription-final counts alone do not observe unit boundaries, because a unit at an inscription edge puts its internal signs at that edge | Raw inscription-position counts spent as if they were unit-position counts; a functional label (“suffix,” “prefix”) spent as if it were observed boundary evidence |
| **Functional interpretation** | What the sign’s value does in its unit (for example, case marking, opening a unit, closing a unit) | Two levels, kept separate: (a) attestation — the claimed anchor position is attested for the sign in a named frame; (b) a **testable functional prediction** — a stated, falsifiable consequence beyond position (for example, a stated pattern of co-occurrence, alternation, or unit-shape consequence that would not be expected if the function were different), judged against pre-stated evidence | Anchor attestation alone spent as proof of function; a corpus-only compatibility score (see the closing rule, Note 5) |

A successor that cannot state, for a given basis text, which of the three kinds it is coding — or a summary, or no checkable claim — must code it as no checkable claim and record why. Forcing a text into a kind it does not state is the Spec 076 defect, and coding a summary as a claim is the same defect in slower motion.

**Note 2 — Report by informative denominator and by claim type, before any freeze.**

Spec 078’s headline numbers are honest, but a successor’s reporting must be specified in its draft, before freezing, at a finer grain:

- For each claim kind separately: how many counted signs yielded a claim of that kind; how many claims of that kind were coded; how many were judged; how many passed and failed that kind’s own standard.
- An **informative denominator** for each accuracy-like statement: the denominator includes only rows the test could actually discriminate (see Note 3). Frame-absent signs, worked-example signs, summaries, and non-discriminating rows are reported on their own lines and are never inside an accuracy denominator.
- The administrability question stated per kind, not only in total: a successor whose panel yields checkable claims of only one kind has learned something different from one that yields all three, and its report must say which.
- The summary census reported as a census (counts, named positions, sample sizes, transfer behavior in the frame), with no failures attached and no accuracy language used about it.

**Note 3 — Controls: known-answer, deliberately false, and honestly labeled.**

A successor pilot may not calibrate itself only on the strict core’s own bases, because — as Spec 078 showed — those bases contain too few checkable claims to exercise the machinery. The successor design must therefore include, specified before any freeze:

- **Independently coded known-answer positive controls:** checkable claims whose correct judgment is known from a source independent of the coder and of the bridge being tested, coded blind under the same rules, and judged by the same standards. The bridge must pass them at the successor’s pre-stated rate.
- **Deliberately false checkable controls:** claims written to be checkable and false, in each claim kind the successor tests, coded and judged the same way. The bridge must reject them at the successor’s pre-stated rate. A bridge that passes everything placed before it — true or false — has demonstrated no discrimination, whatever its pass count says.
- **FREE / non-discriminating rows cannot demonstrate accuracy.** A row that makes no checkable claim, or whose coding is compatible with every outcome, contributes nothing to an accuracy numerator or denominator. It may be counted and reported as a row. It may not be reported as a success.
- **Core-derived controls are consistency checks, unless external truth exists.** A control built from the strict core’s own bases, or from a register derived from that core, tests whether the machinery agrees with its own inputs. That is a consistency check, and it must be labeled as one in every report that uses it. It becomes an accuracy control only if the expected answer is established from a source external to the core and to the machinery — and the draft must name that source, claim by claim, before freezing.

**Note 4 — Retracted material needs a rule, written in advance.**

Following the gap recorded in §2.2: a successor draft must state, before any coding, how a basis passage that retracts or supersedes an earlier assertion inside the same basis is coded, how the retraction is recorded verbatim, and which text — retracted, retracting, or neither — can yield a checkable claim. The rule is written in the draft. It is never patched into a running pilot.

**Note 5 — The closing rule, stated plainly.**

> **A vocabulary that cannot express testable functional predictions closes as inadequate. No corpus-only compatibility score licenses a semantic promotion.**

In plain language: if the successor’s vocabulary can state where signs occur and what jobs their values are said to do, but cannot state a functional prediction that evidence could prove wrong, then the vocabulary — not the core, and not the signs — is what closes, and it closes as inadequate. Separately: a score that measures only how well a proposed reading fits the same corpus it was drawn from is a compatibility score. Compatibility is not independent evidence. No reading, value, or meaning may be promoted on a compatibility score alone, in this line or any other.

**Note 6 — What a successor may not do.**

- It may not re-run Spec 078’s pilot under any parameters. The pilot record states this, and this note repeats it as a fence.
- It may not inherit Spec 078’s thresholds (§2.1) as if they were its own without stating them as new, pre-committed choices in its own draft — and if it does restate the same numbers, it must say that they repeat a completed study’s numbers by choice, not by continuity.
- It may not treat A-FACE-2 as confirmed. It stands neither confirmed nor falsified, carried forward exactly as exposed as it was filed.

**Gate for any M13 successor:** a new draft, judged as Spec 078 was; owner’s freeze word through the program’s freeze gate; registration before execution if the draft names one. Until then: **design notes only — nothing frozen, nothing run.**

---

## 3. M14 successor note — PARKED status respected

### 3.1 Status

**The M14 line (signary granularity audit) is PARKED.** That word is the second pilot record’s own closure, executed under the draft’s kill criterion, and this note does not soften, reopen, or re-rank it.

The audit asked whether the program’s 557-sign list carves the script at its own joints — whether proposed sign merges are contextually interchangeable, checked by a distributional-equivalence tool (Tool 1) and, in the full design, an image-based tool (Tool 2). Neither pilot judged any real sign pair. No merge or split is supported or refuted by either pilot. The Daggumati & Revesz candidate list’s standing is untouched: its pairs were never converted or tested, and the candidate-list gate in those drafts remains undone.

### 3.2 What happened, in numbers

Both pilots worked on the same pinned population, re-derived exactly at Step 0 in both runs: **3,045 inscriptions / 557 signs / 11,805 tokens** (550 signs in sequences of length 2 or more). Input pins verified by hash in both runs include the Shakti corpus `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`, the row grades `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`, and Registry v2 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`.

**Iteration 1** (draft SHA-256 `fc3f2ce8…`): Tool 1 measured context as the joint distribution of (left neighbor, right neighbor, position class), distance as total variation distance, with an equivalence margin of 0.20 and a 9,999-draw permutation leg.

- Planted-truth recovery (Step 1): **0 of 20** planted pairs re-merged, against a bar of at least 17. Closure: **INSTRUMENT CANNOT RECOVER (Tool 1, Step 1)**.
- Why, as filed in that record: (a) the joint context space is too sparse at this corpus size — most (left, right, position) triples occur once, so two halves of the same sign’s tokens share few exact triples and their distance lands between 0.13 and 0.87; (b) the percentile leg gives a true pair about one chance in twenty by construction, because a planted random split is itself a typical draw from the permutation distribution it is tested against.
- Restraint legs passed numerically (0 of 200 unproposed attested pairs merged; 0 of 200 pairs merged on a built, calibrated structured non-language corpus) — with the record’s own caveat that an instrument that merges nothing passes a restraint test trivially, so those passes are weak evidence and must not be quoted without the Step 1 failure beside them.

**Iteration 2** (draft SHA-256 `2937da55…`): Tool 1 redesigned — coarse-marginal representation, distance as the mean of three views’ total variation distances, an equivalence-correct decision rule with family simultaneity and a precision condition. Run for Tool 1 only, by owner decision; Tool 2 waited on the segmentation build, which was queued behind this pilot and starts only if this pilot passes. It did not pass, and the build did not start.

- Planted-truth recovery (Step 1): **15 of 20**, against a bar of at least 17. Closure: **INSTRUMENT CANNOT RECOVER (Tool 1, Step 1)**.
- Second, independent closure: **REPRESENTATION TOO COARSE.** The non-equivalent reference distribution (200 unproposed pairs) had median distance 0.397, lower quartile 0.285, and 5th percentile **0.153** — at or below the margin of 0.20, the draft’s stated condition. Genuinely distinct pairs routinely sit inside the margin under this representation.
- Why, as filed in that record: the point statistic was repaired (planted distances 0.037 to 0.096, median 0.054 — an order of magnitude inside iteration 1’s range), but certification is what the population cannot pay for. The simultaneous critical value was 4.42 standard errors, about 2.7 times the single-pair value, driven by the heaviest tail among the 20 pairs. At the smaller planted signs (members of about 70 to 100 tokens), the widened interval no longer fits under the 0.20 margin, and four pairs failed earlier on the precision condition, with interval half-widths of 0.107 to 0.117 against a bound of 0.10.
- Step 2 legs were recorded **VOID — RESTRAINT UNPROVEN (vacuity)**, under the draft’s non-vacuity condition, because Step 1 failed in the same run: false-merge restraint (1 of 200, at the bar numerically) and the structured-generator leg (4 of 200, at the bar numerically) certify nothing, are not banked, and are not carried into later work as evidence of restraint.
- Kill criterion executed: Tool 1 failed Step 1 in two successive designs on materially different representations. **No iteration 3 on distributional equivalence for this population is commissioned.** Downstream work proceeds carrying the signary as an **explicitly untested assumption**, printed as such wherever a verdict leans on it.

### 3.3 The gating dependency: the segmentation build, unstarted

The image leg (Tool 2) was not failed. It was never run, because its input does not yet exist:

- **No segmentation build exists for this audit.** The held image layer contains per-sign crops keyed to catalog objects, not keyed to the pinned population’s token order. The iteration 1 record measures the join: 2,814 of 3,045 population rows carry a catalog key; under the largest crop set’s naming, **654 rows** have a crop set at least as long as their sequence and **1,009 rows** have partial sets. Which crop is which keyed token — across reading directions, object sides, and two keying traditions — is the segmentation build, priced in the draft at one to two weeks.
- Gate G1 (at least 98% crop-to-keying agreement, hand-checked, 60 inscriptions, every token) was therefore not run. Tool 2 (the image-and-context clustering) was not built or run on any material. Its legs are outstanding, not failed, and no number exists for them.
- The external known-inventory control for the image leg was likewise not run: it presupposes the pinned image pipeline, which presupposes G1’s crop set.

Restricted material is referred to here by existence, counts, and coverage only. No restricted content is reproduced.

### 3.4 What a future design must answer — without inventing a new frozen design

This note deliberately does **not** draft a successor instrument, state new bars, or propose a margin. A future design, if the owner commissions one, must answer at least these questions in its own draft, before any pilot:

1. **Representation.** Two representations have now failed at 11,805 tokens in two different ways: a fine joint-context representation too sparse to measure overlap, and a coarse-marginal representation whose genuinely-distinct-pair tail overlaps the equivalence margin. What representation separates planted halves of one sign from genuinely distinct pairs at this scale, demonstrated on planted and reference material before any real pair is judged?
2. **The cost of honest simultaneity.** Iteration 2’s statistic worked and its certification did not: judging a family of pairs together, as honesty requires, widened intervals past the margin at the smaller counts the audit most needs. How does a future design pay that cost — in its family definition, its precision condition, or its stated decidable frontier — without quietly judging pairs one at a time?
3. **The decidable frontier.** At control-pair counts, iteration 2’s instrument resolved few pairs at all (175 of 200 restraint pairs were precision-insufficient, recorded void). A future design must state, in advance, which pairs at which counts it can decide, and must report undecidable pairs as undecidable — not as restraint, and not as equivalence.
4. **The image leg’s standing.** Whether an image-leg-only path is commissioned is a new owner decision. A single-tool audit would not be the method as designed (the two-tool agreement rule was the design), so a future draft must either restore a second independent leg or state plainly what a one-tool result would and would not establish.
5. **The segmentation build as a prior, separate deliverable.** The build and its G1 hand-check are the gating work for any image leg. A future design must treat the build as a deliverable with its own acceptance check, completed and reported before any pilot that depends on it is drafted as runnable.

**Gate:** owner decision to commission any successor at all; owner decision separately on any image-leg-only path; segmentation build not started and not authorized by this note. Until those decisions: **PARKED stands.**

---

## 4. M7 / Spec 077 follow-on note — the 158-sign gap list as input

### 4.1 What Spec 077 found

Spec 077 (Method M7, signary triangulation) froze and executed once, as frozen (freeze digest `a9d10a2ba4f8e03fe77f7815a9fbd9a8860270f3a7a56801f02458507250f55f`; freeze PR #417 merged `95da5dc8`; execution PR #419 merged `7953ecd1`; machine record `reports/phase443_results.json`, SHA-256 `29b84b8e…`). No OSF registration was named by the design; the repository freeze record governs.

- **F077-C01: NOT SUPPORTED — SIGNARY NOT WITNESSED AT THE STATED LEVEL.** Witnessed **399 of 557 signs (71.63%)**, against a bar of **502**. Raw, ancestry-adjusted, and both sensitivity figures are the same: 71.63%. Mahadevan 1977 witnesses 399; Wells 1998 witnesses 42, all already witnessed by Mahadevan, so the descendant witness adds none.
- **Gap list: 158 signs**, filed in full in the execution outcome (the record summarizes it as running from 036 to 958, and including 999). That filed list — in the execution outcome, not re-derived here — is the authoritative version.
- **F077-C02:** the two-condition attack on token 999 ran and named no identity: **token 999 stands NO PUBLISHED IDENTITY.** Thirty-nine witness signs met both frozen conditions (36 via Mahadevan, 3 via Wells 1998), so the rule selects a 39-sign candidate set, not an identity. The set is filed as the attack’s positive result.

**What Spec 077 establishes:** witness presence of the signary by sign number under the stated match rules (71.63%, below the stated level — the design’s consequence, that the relevant ladder placement must be argued down on this record, is stated in that record); the exact 158-sign gap; and that the 999 attack yields a candidate set and no identity.

**What Spec 077 does not establish:** that gap signs are not real signs (the result is attestation through one crosswalk under conservative rules); sign identity beyond the crosswalk’s own claim; any reading’s value; or anything about glyph shapes.

### 4.2 Follow-on note

The 158-sign gap list is the input to any future witness work in this line. Concretely:

- Future witness work starts from the filed gap list as its work list. It does not re-derive the witnessed count, does not re-run Spec 077, and does not treat the 399 witnessed signs as its subject except where a new witness source must be joined against the full 557 for completeness.
- Each gap sign worked on must carry, in any future record: the witness source consulted, the match rule applied, the outcome (witnessed under that rule / not witnessed / uncheckable under that rule), and the source’s revision or pin. A sign leaving the gap list does so on a named witness under a named rule, recorded sign by sign — never by a revised total asserted without the per-sign trail.
- Token 999 stays as Spec 077 left it: no published identity, with a filed 39-sign candidate set. Any future work on 999 starts from that candidate set and that standing. It does not restart the attack under looser conditions and report the result as the same test.
- A future witness result changes the witnessed count only as a new record, against its own stated sources and rules. Spec 077’s 399 of 557, its bar of 502, and its verdict words are a completed study’s record and are not edited.

**Gate:** any future witness study is its own draft, with its own sources, match rules, and bars stated before execution, and the owner’s freeze word where the program’s discipline requires one. This note commissions nothing.

---

## 5. Package status

| Part | Status |
|---|---|
| §1 Spec 076 endpoint correction | **Prepared** — errata text drafted ready to append; not appended to any frozen record by this work |
| §2 M13 successor design notes | **Prepared, gated** — reconciled with Spec 078’s completed outcome (CANNOT BE ADMINISTERED, 7 of 86); any successor requires a new draft and the owner’s freeze word |
| §3 M14 successor note | **Prepared, PARKED respected** — no new design drafted; segmentation build unstarted; any successor or image-leg-only path requires a new owner decision |
| §4 M7 / Spec 077 follow-on note | **Prepared** — the filed 158-sign gap list named as the input to any future witness work; no witness work commissioned |

**No study was executed, frozen, or registered by this work package.**
