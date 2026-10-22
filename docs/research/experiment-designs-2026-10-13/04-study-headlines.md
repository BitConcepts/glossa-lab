# Designs 04 — the study headline claims

The program's own study results: one settled disagreement with a 93.9%
unexplained residue (D-20), one contradicted methods claim (D-21), the
site-effect family (D-22 to D-25), the movement line (D-26 to D-28), and the
audit rollup (D-29).

**A rule for this whole file:** the frozen tests of Specs 024, 025, 027, and
028 are never quietly re-run. Every design below is a new, pre-registered
variant that answers a question the frozen test left open, or a test on
different data. The frozen outcomes stand exactly as recorded, whatever these
designs later find.

---

## D-20 — Why do the two great compilations disagree? A matched-object attribution

- **Claim:** `STUDY-SPEC-019/PHASE-125` (SETTLED — FAIL: DISAGREEMENT stands:
  of 286 sign pairs, only 16 were judgeable; their positional profiles differed
  by a median distance of 0.637; Phase-127 showed sampling noise alone produces
  only 0.083, so the disagreement is not a sampling artefact; Phase-131
  attributed just 6.1% of it to named causes, leaving 93.9% unexplained).
- **Feasibility:** RUNNABLE-TODAY, with a step-0 feasibility gate that can
  close it honestly.

**The question in plain words.** The disagreement might live in the objects
(the two compilations publish different inscriptions), in the sign identities
(the crosswalk maps signs differently — 383 of its 762 pairs are conflict
pairs), or in segmentation (where each compilation cuts texts into signs).
Phase-131 could not separate these, because its first arm found **zero shared
object keys** between the two digital layers: there was no way to ask "for
*this same physical object*, what does each compilation say?" This design
builds that join, then asks the question object by object.

**Step 0 — build the bridge, and count it (feasibility gate).** Construct
object pairs (the same physical inscription in both compilations) through the
lawful routes the program holds: (a) the CISI catalogue layer (the 7,705-row
catalogue built in the Phases 120–124 work, 98.9% sample accuracy), which
carries object identifiers on the Parpola/CISI side; (b) the Mahadevan side's
published object references, joined through the Phase-130 intake schema, which
exists precisely to admit object-level data with provenance; (c) the 44
Phase-128 evidence dossiers, which already assemble per-object evidence for
the contested subset. Every bridge pair enters as cited data with its source.
GATE, fixed in advance: if the bridge yields fewer than 150 matched objects
carrying texts of three or more signs in both compilations, the design closes
at step 0 as TOO THIN TO ATTRIBUTE — with the bridge census published as the
finding (how many objects could be paired, by which route, and where the
join ran out). That outcome converts Phase-131's "zero shared keys" from a
dead end into a measured quantity, and it names the unblocking act precisely
(a published concordance or object-level dataset entering through intake).

**Hypothesis (step 1, if the gate passes).** On matched objects, the two
compilations' positional profiles agree far better than the corpus-level
0.637 distance — that is, most of the disagreement is composition (different
objects) rather than transcription (different readings of the same objects).

**Falsifier.** Matched-object disagreement remains at or above half the
corpus-level distance — meaning the compilations genuinely transcribe the
same objects differently, and composition is exonerated.

**Method.** For each matched object: extract each compilation's sign sequence;
compute the per-sign positional profiles on the matched-object subset only,
in each compilation separately; measure the profile distance exactly as
Phase-125 did (same distance, same count floors). Then decompose what
disagreement remains: align the two sequences per object and classify every
difference as segmentation (same signs, different cuts), substitution (a
sign mapped differently — checked against the crosswalk's conflict pairs), or
composition residue (objects present in one compilation's subset only). The
output is an attribution table in Phase-131's own categories, so the 6.1%
figure and this design's figure are directly comparable.

**Criteria fixed in advance.** ATTRIBUTED TO COMPOSITION: matched-object
median distance at or below 0.20 (near Phase-127's noise band of 0.083,
allowing for the smaller sample). ATTRIBUTED TO TRANSCRIPTION: matched-object
median distance at or above 0.32 (half the corpus-level 0.637). BETWEEN:
reported as a split attribution with the decomposition table as the result —
the design's success is a measured split, whichever way it falls, replacing
"93.9% unexplained" with named shares.

**Controls and named confounders.** The bridge itself is a selection: objects
that *can* be matched may be the better-published ones. The design reports
the matched subset's site and object-type mix against both compilations'
full mixes, and any attribution verdict carries the subset's description
with it. Crosswalk circularity: substitution classification uses the
crosswalk as a *record of disagreement*, never as ground truth. Small
samples per object: profiles are computed on the pooled matched subset, with
per-object distances reported as a distribution, not averaged away.

**What it would move.** The residue on a SETTLED claim: "93.9% unexplained"
becomes a named decomposition. It also reprices every other positional claim
in this packet — if transcription disagreement is large, claims 4, 5, 6, and
8 inherit a measured risk instead of an unmeasured one.

**What it would NOT establish.** Which compilation is *right* where they
differ. Attribution explains disagreement; it does not crown a winner.

---

## D-21 — Why did the transcription passes disagree, and can humans do better?

- **Claim:** `STUDY-SPEC-023/PHASE-132+383` (SETTLED — CONTRADICTED: pilot
  exact-sequence agreement 0.20 against the frozen 0.80 floor; the rerun's
  interval [0.10, 0.32] sits far below it. Every coder was an AI agent of a
  single model family — that disclosure is part of the verdict).
- **Feasibility:** PARTIAL. Arm A runs today on data already recorded; arm B
  is blocked on a named precondition outside this packet's power.

**The open points.** Two, and they are different kinds of question. (1) The
mechanism: *which* signs, objects, and segmentation choices drove the
disagreement was never analysed — there is no named account of it at any
level. (2) The human question: whether trained human coders would clear the
bar is untested, and the record is explicit that the AI result is not
evidence about humans.

**Arm A — disagreement mechanism, on the existing pilot data (RUNNABLE-TODAY).**
Hypothesis: the disagreement is concentrated, not uniform — a minority of
signs or object types accounts for the majority of sequence mismatches.
Falsifier: mismatches distribute across signs and objects in proportion to
their frequencies (no concentration to explain). Method: re-analyse the
recorded Phase-132 pilot passes (both passes' codings are on record): for
every mismatched object, localise the first position of divergence and the
signs involved; tabulate mismatch share by sign, by object type, and by
divergence type (substitution, insertion/deletion, segmentation cut).
Criteria fixed in advance: CONCENTRATED if the top 10 signs by mismatch
involvement account for at least 50% of all mismatches; UNIFORM if their
share is within 10 points of their frequency share; BETWEEN otherwise. The
output is the mechanism account the claim's not-understood text asks for —
it changes no verdict (the pilot still failed, and stays failed), and it is
what any future protocol revision would have to answer.

**Arm B — the human calibration set (BLOCKED).** The design exists in
embryo in the program's own record: a calibration set of 30 objects / 212
tokens with human-derived reference transcriptions, scored by the merged
scoring machinery (PR #128), with proposed bars of at least 95% per-token
and at least 85% exact-sequence agreement. This design adopts that shape and
fixes the verdict rule in advance: the bounded claim "human expert coders
can produce a transcription layer at this protocol" is SUPPORTED if two
independent human coders, blinded to each other and to the references, clear
both bars against the references; NOT SUPPORTED if either coder falls below
either bar; the set, the coders' qualifications (M77-native sign-list
training), and the all-Mohenjo-Daro composition (a stated limitation — the
references exist only for that site) are all named in the design, not
discovered later. BLOCKED ON: human expert coders. The program's standing
position (owner decision, 2026-10-10) funds a paid calibration set, and the
expert-engagement letters that would recruit the coders are currently HELD
by the owner (program not prepared to pay yet, 2026-10-12). Unblocking act:
the owner lifts that hold and an engagement is made. No part of arm B can be
substituted with AI coders — the Spec 023 record is precisely the proof that
the substitution answers a different question.

**What it would NOT establish.** Arm A cannot soften the contradicted verdict;
arm B, even if supported, validates a calibration set at one site, not a
corpus-wide transcription programme.

---

## D-22 — The seal/tablet difference, on a better join (residue design)

- **Claim:** `STUDY-SPEC-024/F1` (SETTLED — SUPPORTED: within sites, a text's
  final sign falls in the frozen TERMINAL14 class at different rates on seals
  than on tablets; odds ratio 2.384, interval [1.847, 3.077], q = 0.00015;
  stable under leave-one-site-out in Phase-141).
- **Feasibility:** RUNNABLE-TODAY, with a step-0 join gate.

**The open point.** The result describes only the joined subset: 49.0% of the
lineage layer's rows could not be joined to the catalogue at all, so half
the corpus is silent in the program's cleanest positive result. The claim's
not-understood text names the fix: the same test on a corpus joined through
object identifiers rather than catalogue concordance.

**Step 0 — join census (gate).** Rebuild the join through object identifiers:
the CISI catalogue layer's object IDs and the Phase-130 intake route, in
place of the original concordance join. GATE, fixed in advance: if the
object-ID join does not raise the joined share above the original 51.0% by
at least 10 points (to 61% or more), the design closes at step 0 — the
unjoined half is then a measured property of the available catalogue data,
not an oversight — and names the unblocking act (a more complete published
object catalogue entering through intake).

**Hypothesis (step 1).** The seal/tablet difference in TERMINAL14 endings,
within sites, replicates on the enlarged joined set at comparable size.

**Falsifier.** On the enlarged set, the within-site test's interval for the
odds ratio includes 1.0, or the point estimate falls below 1.5 — meaning the
original result was partly an artefact of which rows could be joined.

**Method.** The identical test as Phase-136 (within-site stratified
Cochran–Mantel–Haenszel, same TERMINAL14 class, same family correction
across the Spec 024 family), run on the enlarged joined set; then a stated
comparison of the joined and unjoined rows on every covariate the data
carries (site, object type, text length, preservation), so the silent half
is at least described. Leave-one-site-out stability rerun as in Phase-141.

**Criteria fixed in advance.** REPLICATED: q below 0.05 after the family
correction and the odds-ratio interval entirely above 1.5. WEAKENED: q below
0.05 but the interval reaches below 1.5. NOT REPLICATED: q at or above 0.05
or the interval includes 1.0. The original verdict is not edited in any
case; the outcome is appended as the claim's replication record, and the
claim's wording gains or loses the phrase "on the joined subset" as the
evidence dictates.

**Controls and named confounders.** Genre differences (ownership marks
versus accounts) and preservation differences between object types: the
within-site design controls place, not kind — the design states this limit
in its verdict wording, as the original report did. Join-selection bias:
the covariate comparison above is the control, and it is reported whether
or not the test replicates.

**What it would NOT establish.** What the difference *means* (genre, habit,
or survival), or anything about corpora outside this lineage.

---

## D-23 — The Holdat site effect: is the margin the message? (residue design)

- **Claim:** `STUDY-SPEC-024/F2-HOLDAT` (SETTLED — CONTRADICTED at the
  declared margin: the rerun's interval for the effect is [0.059, 0.078],
  entirely below the 0.10 margin fixed in advance; the descriptive value in
  this layer had been 0.1154).
- **Feasibility:** RUNNABLE-TODAY.

**The open point.** Two residues. (1) Margin-dependence: the verdict is
"contradicted *at 0.10*" — an honest verdict, but the claim's usefulness
depends on how the answer moves with the margin, and that curve has never
been published as the primary object. (2) The layer disagreement: the same
question in the ICIT lineage (F3) came out the other way, and Phase-125 says
the compilations themselves disagree beyond noise — so the Holdat result may
be a fact about the Holdat compilation rather than about ancient cities.

**Hypothesis.** On the population the two layers share (same sites, same
object types), the Holdat effect and the ICIT effect move toward each other —
that is, the layer disagreement is substantially a composition difference.

**Falsifier.** On the shared population the two layers' effect intervals
still exclude each other — the disagreement then lives in the compilations'
sign treatment, and D-20's attribution becomes the governing next step (the
design says so in advance, so the hand-off is pre-registered, not improvised).

**Method.** Arm 1 (margin curve): recompute the bounded interval estimate
(the Phase-384 method, unchanged) and report the verdict as a function of
the margin across a pre-registered grid (0.05, 0.075, 0.10, 0.125, 0.15) —
a sensitivity display, explicitly not a verdict change: the recorded verdict
at 0.10 stands. Arm 2 (shared population): restrict both layers to the
sites and object types present in both, with period mix described per layer;
compute the site-effect size in each layer on that shared population with
identical code; compare the two intervals.

**Criteria fixed in advance.** COMPOSITION EXPLAINS THE GAP: on the shared
population, the two layers' intervals overlap. COMPOSITION DOES NOT: the
intervals still exclude each other on the shared population. If the shared
population retains fewer than 5 sites or fewer than 500 inscriptions in
either layer, arm 2 closes as TOO THIN with the counts stated.

**Controls and named confounders.** Site mix, period mix, sign numbering —
the shared-population restriction is the control for the first two; the
third is exactly what the falsifier routes to D-20. Margin shopping: the
grid is fixed here, and arm 1 is labelled sensitivity in every output, so
no one can quote the margin at which the verdict flips as if it were the
verdict.

**What it would move.** No verdict moves. The residue — "is this about
cities or about compilations?" — gets a measured answer or a pre-registered
hand-off, and the margin-dependence is published where anyone citing F2
will meet it.

**What it would NOT establish.** That there is no site effect in Holdat. The
settled verdict already says the effect, if present, is below the size the
program agreed to care about; this design explains the verdict's shape, not
its replacement.

---

## D-24 — The ICIT site effect, replicated outside its own lineage

- **Claim:** `STUDY-SPEC-024/F3-ICIT` (IN QUESTION — SUPPORTED inside one
  lineage: effect interval [0.182, 0.210] above the floor; but the sites
  differ in period mix, preservation, and excavation history, the Holdat
  layer answers the same question the other way, and no replication outside
  the ICIT lineage exists).
- **Feasibility:** BLOCKED as a decisive test today; written as a
  wait/intake-triggered design with its protocol frozen here, so it can run
  the week its precondition clears without a new design round.

**The question in plain words.** Do different cities genuinely use different
sign repertoires — or does that pattern live only inside one family's
version of the corpus? The claim's own not-understood text names both halves
of the answer: period controlled as the primary design (that half is D-25,
on G1), and a replication on data outside the ICIT lineage (this design).

**Why it is blocked, stated plainly.** The program's data sweep
(2026-10-08) asked this question directly and answered it: no large, fully
independent, machine-readable Indus corpus exists anywhere reached. Every
candidate in hand is an ICIT-lineage derivative, and a "replication" on a
derivative would be circular — it would test the lineage against itself
and call the echo independence. This design therefore does not propose a
fake replication. It freezes the protocol and names its trigger.

**The frozen protocol (ready to run).** Data trigger: a multi-site
inscription dataset that (a) is not derived from the ICIT lineage (provenance
checked at intake, with derivation from ICIT counting as disqualifying —
the check itself is recorded), (b) covers at least 5 sites with at least
100 inscriptions each, and (c) enters through the Phase-130 intake pack with
rights posture recorded. On trigger: run the identical site-association
test as Phase-137 (same statistic, same permutation scheme, same effect
measure), with period strata from the chronology spine (D-25's asset)
reported as the primary sensitivity. Criteria fixed in advance: REPLICATED
if the effect interval lies entirely above the 0.10 practical floor used by
the F2/F3 family; NOT REPLICATED if it lies entirely below; INCONCLUSIVE
if it straddles, or the trigger dataset's site count or sizes fall below
the trigger floors on arrival (in which case the dataset is banked and the
design stays armed). Confounders named in advance, as in Spec 024 §5.1:
period mix, preservation, excavation history, text-type and text-length
mix — each described for the trigger dataset before the test runs, and any
the dataset cannot describe is carried into the verdict wording.

**What it would move.** The claim from IN QUESTION to replicated /
not-replicated — the single strongest upgrade available to any claim in
this packet, which is why it is worth freezing now and waiting honestly.

**What it would NOT establish.** Even replicated, an association between
site and repertoire does not establish local sign inventions, dialects, or
movement of people. The movement question has its own line (D-26 to D-28)
and its own, stricter fences.

**Unblocking act.** A qualifying dataset's arrival — the weekly data watch
already flags any newly published multi-site dataset (and marks it as a
PRED-2026-003 candidate where relevant; this design and that prediction
share a trigger but score separately, under their own frozen rules).

---

## D-25 — G1 with time held fixed: the chronology-controlled site test

- **Claim:** `STUDY-SPEC-025/G1` (SETTLED — SUPPORTED under control:
  composition and preservation held fixed, the site association survived,
  effect interval [0.184, 0.210] above the margin. The rider, carried
  wherever the result is stated: **chronology is not controlled** — sites'
  period mixes differ, so part of the "site effect" may be a time effect).
- **Feasibility:** RUNNABLE-TODAY — the asset that was missing now exists:
  the 205-row extended chronology spine from Spec 030 / Phase-394
  (`data/movement/chronology_rows_phase394.jsonl`), on top of the Stage 0
  gazetteer's period labels.

**The question in plain words.** When inscriptions are compared only
against inscriptions from the same period, does the site association
survive the way it survived controlling for preservation and text
composition? This is a new primary test, not a re-run of Phase-140: the
strata change, and the change is the point.

**Hypothesis.** The site association survives within period strata: the
controlled effect stays above the family's practical margin.

**Falsifier.** Within period strata, the effect's interval reaches or
crosses the margin — meaning the G1 result was substantially a period
effect wearing a site label.

**Data.** The ICIT-lineage corpus as in G1 (same rows, same preservation
and composition controls); period assignment from the extended spine at
the coarse level the spine can honestly support — Early / Mature / Late
Harappan site-periods as recorded in the gazetteer and spine rows. The
design states the spine's limit in its own text: Spec 030 closed with the
timing question NOT-YET-TESTABLE at fine resolution (criteria failed 1/3,
6/10, 0.0/0.5), so this design claims only coarse period strata, and any
inscription whose site-period the spine cannot place is excluded by rule
and counted, never assigned by guesswork.

**Method.** Phase-140's controlled permutation test, with the shuffling
done inside groups matched for composition, preservation, **and period
stratum** — one added stratification, nothing else changed: same statistic,
same 9,999 shuffles, same effect estimator as the Phase-385 rerun, so the
new interval is directly comparable to [0.184, 0.210].

**Criteria fixed in advance.** SUPPORTED WITH THE RIDER RETIRED: the
period-controlled interval lies entirely above the 0.10 margin family
precedent — G1's rider is then removed by appended record, and the claim
reads "supported under control, chronology included". RIDER CONFIRMED AS
MATERIAL: the interval straddles or falls below the margin — the claim is
re-stated as a period-confounded association, appended, with the size of
the drop reported. TOO THIN: if fewer than 3 period strata retain at
least 5 sites each after assignment, or more than 40% of rows are
unassignable to a stratum, the design closes INCONCLUSIVE-BY-DESIGN with
the counts stated — the spine's sparsity is then the finding, and it is
reported as a property of the dated record, not massaged.

**Controls and named confounders.** Period assignment quality (the spine's
rows are traced determinations, 205 of them, with contested rows flagged —
contested rows are excluded from stratum assignment in the primary run and
included in a stated sensitivity, echoing Spec 030's two-computation
posture). Composition and preservation: controlled as before, not dropped.
Harappa concentration: leave-one-site-out rerun pre-registered, drop-Harappa
named in advance.

**What it would move.** The rider on a SETTLED claim — either retired or
confirmed as material. This is the difference between "cities wrote
differently" and "times wrote differently", and it is currently the
largest single unknown inside the program's strongest positive result
family.

**What it would NOT establish.** A mechanism (local repertoires versus
genre mixes), and nothing about movement. It also cannot fix the lineage
question — that is D-24.

---

## D-26 — The movement question with period held fixed (a new Stage-1 variant)

- **Claim:** `STUDY-SPEC-027/STAGE1-PHASE-392` (INCONCLUSIVE — site
  similarity accounts for about 1.7% of repertoire variation, median
  adjusted R² 0.01677, interval [0.01032, 0.02397], controls passed, but
  dropping Harappa pulled the median to 0.00928, below the 0.01 margin:
  the frozen SUPPORTED rule's jackknife clause failed, and CONTRADICTED
  did not fire either).
- **Feasibility:** RUNNABLE-TODAY.

**Why a new variant, and why this one.** The frozen Stage-1 test stands.
Its not-understood names two live possibilities: Harappa carries the
signal because it is genuinely central, or because its corpus dwarfs the
others. Spec 028 attacked that question two ways (D-27, D-28's territory)
and both came back inconclusive. What no run has done is hold **period**
fixed in the movement test itself — yet shared period is one of the named
rival explanations for why nearby sites resemble each other (sites near
each other are often occupied at the same times). The 205-row extended
spine now makes a coarse period control possible for the first time.

**Hypothesis.** Within period strata, repertoire similarity still tracks
geographic closeness, at or above the family's margin, and survives the
full site jackknife.

**Falsifier.** Within strata, the association falls below the margin, or
the jackknife fails again in the same place — in which case the record
gains a sharper statement: the Stage-1 signal does not survive period
control, full stop.

**Method.** The Stage-1 estimand and machinery (the MRM-style
similarity–distance framework of Phase-392, identical controls — the
negative control near zero, the positive control behaving as designed),
run within Early/Mature/Late strata from the extended spine, with the
pooled estimate combined across strata by the pre-registered rule
(stratum estimates reported individually first; no pooling rule invented
after seeing them). The Parpola-numbering sensitivity that Stage 1 could
not estimate (crosswalk coverage 17.57%) is **not** re-attempted here: it
becomes estimable only if D-20's bridge thickens the crosswalk, and the
design says so rather than re-recording the same NOT ESTIMABLE.

**Criteria fixed in advance.** Same margins as the frozen contract (0.01
adjusted R²; SUPPORTED requires the estimate above margin **and** every
leave-one-site-out cell above margin, drop-Harappa named; CONTRADICTED
by the frozen family's rule; otherwise INCONCLUSIVE). Strata floors: a
stratum enters only with at least 6 sites; strata below the floor are
reported and skipped by rule. If fewer than two strata qualify, the
design closes INCONCLUSIVE-BY-DESIGN with the census stated.

**Controls and named confounders.** Shared period (the design's point);
shared trade goods and excavation practices (named, uncontrolled — carried
in the verdict wording as before); corpus size (jackknife plus the
equal-weight sensitivity from Arm B reported alongside, not substituted).

**What it would move.** The INCONCLUSIVE claim to supported / contradicted
/ a *sharper* inconclusive — one in which the period explanation has been
removed from the list of live rivals or promoted to the explanation.

**What it would NOT establish.** Movement of people. Even a clean,
period-controlled, Harappa-surviving association is consistent with goods
and habits moving without populations moving; the program's ecological-
fallacy fence (Spec 027) binds this design's wording exactly as it bound
the original's.

---

## D-27 — Arm A: how much more data would settle it? (a precision design)

- **Claim:** `STUDY-SPEC-028/ARM-A` (INCONCLUSIVE — Harappa removed
  entirely: median adjusted R² 0.00878, interval [0.00463, 0.01297], below
  the 0.01 margin; rejection share 0.623; every leave-one-site-out median
  also below the margin).
- **Feasibility:** PARTIAL. Arm A1 (the precision computation) runs today
  on recorded results; arm A2 (the decisive rerun) is blocked on new data.

**The question in plain words.** Without Harappa, the signal is smaller
than the size the program agreed to count — and the current data cannot
tell a real-but-small effect from none. Rather than shrug, measure the
gap: how much more non-Harappa material, of the same kind, would it take
for the interval to resolve at the agreed margin?

**Arm A1 — the precision target (RUNNABLE-TODAY).** Method: from
Phase-393's recorded resampling distribution, compute how the interval
width scales with added inscriptions per site (resampling the recorded
site samples with replacement at multiples of their current sizes — a
simulation over recorded data, labelled as such). Criteria fixed in
advance: the design reports the smallest total added-inscription count,
and its per-site distribution, at which the resampled interval would
exclude the 0.01 margin in at least 80% of trials under two stated
scenarios (true effect at the current point estimate 0.00878 — which,
being *below* the margin, resolves downward, toward "no effect of the
agreed size" — and true effect at 0.015, which resolves upward). The
product is a number the program can act on: the intake target that would
make Arm A decidable, stated before anyone goes looking for data. What
A1 would NOT establish: anything about the ancient world. It is a
measurement of the program's own resolution, reported as such.

**Arm A2 — the decisive rerun (BLOCKED).** The frozen Arm A test,
unchanged in every particular (it is already frozen and registered —
OSF osf.io/7m35w — so the rerun needs no new design, only new data),
triggered when intake brings the non-Harappa corpus to the A1 target
with material outside the ICIT lineage preferred and any lineage stated.
Blocked on: new multi-site inscription data — the same missing input as
D-24 and PRED-2026-003. Unblocking act: that data's arrival through
Phase-130 intake.

---

## D-28 — Arm B split by object type, as a registered primary test

- **Claim:** `STUDY-SPEC-028/ARM-B` (INCONCLUSIVE — equal site weights:
  median adjusted R² 0.02237, interval [0.01222, 0.03333], above the
  margin, rejection share 0.955; but dropping Harappa pulls the median to
  0.00661 and the frozen jackknife clause fails. The exploratory Arm C
  added the clue: Harappa's profile differs from the pooled others far
  more among tablets, dissimilarity 0.4953, than among seals, 0.1114).
- **Feasibility:** RUNNABLE-TODAY.

**The question in plain words.** Arm B's own exploratory arm suggests the
Harappa difference lives in the tablets. If so, the pooled test mixes two
different stories: a seal story (sites alike, Harappa unexceptional) and a
tablet story (Harappa genuinely different). Split the primary test by
object type and find out — as a registered primary test this time, not an
exploratory description.

**Hypothesis.** The similarity–distance association, equally weighted,
differs by object type: the seal stratum survives the jackknife including
drop-Harappa; the tablet stratum is where the Harappa dependence
concentrates.

**Falsifier.** The strata behave alike — both survive or both fail the
jackknife the same way — in which case object type is exonerated and the
Harappa dependence is a whole-corpus property, stated as such.

**Method.** Phase-393's Arm B machinery, unchanged in estimator, weights,
margin, and controls, run separately on the seal-only and tablet-only
repertoire sets (object types as recorded in the corpus; inscriptions of
other or unrecorded type excluded by rule and counted). Full site
jackknife within each stratum, drop-Harappa named in advance in both.
This is a new pre-registered variant of a frozen test — the frozen Arm B
outcome stands untouched beside it.

**Criteria fixed in advance.** Per stratum, the frozen family's rules
apply verbatim (SUPPORTED: median above 0.01 and every jackknife cell
above 0.01; CONTRADICTED by the family rule; else INCONCLUSIVE). Stratum
floors: a stratum enters only with at least 6 sites carrying at least 20
inscriptions of that type; a stratum below the floor is reported as TOO
THIN with counts. The headline outcome is the *pattern* across strata,
pre-registered as one of: SPLIT (strata verdicts differ), UNIFORM-PASS,
UNIFORM-FAIL, or THIN (either stratum too thin).

**Controls and named confounders.** Object-type mix is itself site-dependent
(the confounder that motivates the design — stratification is the control);
preservation differences between seals and tablets (described per stratum);
period mix (described per stratum; D-26's period variant is the
complementary design, and the two are not silently merged).

**What it would move.** The INCONCLUSIVE claim to a split or uniform
verdict that localises the Harappa dependence — the sharpest statement
about "is Harappa unusual, or just unusually excavated?" that in-hand data
can produce.

**What it would NOT establish.** Why tablets would differ (genre,
administration, chronology all remain live), and nothing about movement
of people — the Spec 027 fence binds.

---

## D-29 — The audit rollup: no experiment applies (residue entry)

- **Claim:** `STUDY-SPECS-001-023+PHASES-TO-141` (SETTLED — the Spec 026
  audit reclassified 116 items; 75 changed evidentiary status; the
  assessments stand appended beside the original labels, which were never
  rewritten).
- **Feasibility:** NO EXPERIMENT — recorded here so the claim is not
  skipped silently.

**Why no experiment.** The rollup is an index over 116 per-item
assessments, not a proposition about the ancient world. No measurement can
move it, because there is nothing it asserts that a measurement could be
*of*. Its not-understood text names two open edges, and both are human,
not experimental: (1) the 61 reinterpret-only items carry new readings
without new data — anyone citing a pre-audit label without its appended
assessment misstates the evidence, and the program cannot control
citations it cannot see; (2) the audit's framing — what counts as
"changed" — is a program judgement that has never been independently
reviewed. The moving act for both is the same: engagement by an outside
scholar with the assessment set — in the program's lifecycle language,
*digestion* — which is lane-2 human work, gated on the expert-engagement
route the owner currently holds. When that engagement happens, its
product is a digestion record appended to this claim, not an experiment
result. Until then, the honest entry is this one: **no design, by
reasoned decision, with the gate named.**
