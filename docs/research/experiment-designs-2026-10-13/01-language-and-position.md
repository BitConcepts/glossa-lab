# Designs 01 — language comparison and positional claims

Claims covered: the Farmer non-linguistic thesis and its three restatement fragments
(D-01), Parpola's Dravidian claim (D-03) and fish-sign reading (D-04), and Yadav's
two frequency/position claims (D-07, D-08).

---

## D-01 — An independent-corpus check of the "not writing at all" thesis (residue design)

- **Claims:** `farmer_sproat_witzel_2004_manual_001` (SETTLED — contradicted),
  and its three restatement fragments `…_critique_0001`, `…_critique_0002`,
  `without_kings…_language_0001` (SETTLED as restatements of the same proposition).
- **Feasibility:** PARTIAL. Arm A runs today; arm B is blocked on a named
  precondition.

**The open point.** The thesis — the Indus signs do not encode spoken language at
all — stands contradicted on three items of evidence. Two of the three (the
positional battery's 20 word-ending-like signs and its fixed two-sign opening
formula) were produced by this program, on corpora from one lineage (Mahadevan/ICIT).
Only the published entropy result was produced entirely outside this program, and
specialists still debate it. The residue the claim's own not-understood text names:
the same positional check on a genuinely independent corpus. The three fragment
records carry no separate substance — they restate this claim — so this design is
their residue design too. (Their bookkeeping disposition — carry-over, own record,
or retirement — is a record act, not an experiment, and is handled outside this
packet.)

**Hypothesis.** If the signs are a non-linguistic emblem set, then on a corpus
compiled independently of the Mahadevan/ICIT lineage, sign behaviour should look
emblem-like: no stable set of signs should prefer text-final position the way word
endings do, and no fixed opening formula should recur above chance.

**Falsifier.** The hypothesis (and with it the residue of doubt about the
contradicted verdict) fails if the independent corpus shows the same grammar-like
habits: a final-position sign set and an opening formula at strengths comparable
to the in-lineage results, under the criteria fixed below.

**Data.** Arm A (today): the Soviet positional dataset held by the program (109
records, 36 of 36 hand-verified in the Phases 120–124 work) — a compilation built
outside the Mahadevan/ICIT lineage, small but genuinely separate. Arm B (blocked):
a full inscription corpus compiled independently of the ICIT lineage. The
program's 2026-10-08 data sweep established that no large, fully independent,
machine-readable Indus corpus exists anywhere the program reached; every in-hand
corpus (the field-cady ICIT data, the horus84 layer, the Fuls 2022 book corpus,
the sriharideveloper data) is an ICIT-lineage derivative, and testing on them
would be circular.

**Method.** Arm A: run the frozen positional battery — the same position rules,
count floors, and strength thresholds as the Phase-43 battery that produced the
in-lineage result — on the Soviet dataset, with no threshold adjusted after seeing
the data. Report, per sign, final-position and initial-position rates with counts.
Arm B: the identical battery plus a conditional-entropy computation (how
predictable each sign is from the signs before it), run if and when an independent
corpus enters the program through the Phase-130 intake path.

**Criteria fixed in advance.** Arm A is a consistency check, not a verdict machine,
because 109 records cannot carry the full claim: it is recorded as CONSISTENT if
at least one sign clears the frozen final-position strength threshold and the
two-sign opening formula recurs above the battery's chance baseline; INCONSISTENT
if neither appears; TOO THIN if fewer than 30 records carry texts of three or
more signs (the counts are reported either way). Arm B moves the parent claim's
residue: if the battery and entropy results on the independent corpus land in the
same ranges as the in-lineage results, the "within-lineage only" caveat is
retired; if they land in the non-linguistic ranges, the contradicted verdict is
reopened as a formal question — it is not silently flipped.

**Controls and named confounders.** Compilation disagreement (Phase-125): the
Soviet compilation's sign identities pass through the program's crosswalk, and
crosswalk-conflict pairs (383 of 762) are reported separately, never silently
dropped. Small-sample noise: exact counts published with every rate. The entropy
debate itself: arm B reports the entropy value alongside the published values for
known linguistic and known non-linguistic systems, so the comparison set is part
of the result.

**What it would move.** Arm A narrows or widens the stated caveat on a SETTLED
claim; arm B could retire the caveat. Neither arm re-opens the verdict on its own.

**What it would NOT establish.** Even a clean arm-B replication shows
grammar-like *behaviour*, not what language the signs encode, not any sign's
reading, and not that every part of the sign system is linguistic.

**Unblocking act for arm B.** Acquisition of a genuinely independent corpus —
most plausibly a future published dataset entering through Phase-130 intake (the
weekly data watch already flags any new multi-site dataset). No outreach is part
of this design.

---

## D-03 — The language comparison rerun without the falsified method

- **Claim:** `parpola_2010_dravidian_solution_manual_001` (IN QUESTION —
  partially supported, where the support was computed with the semantic-anchoring
  machinery the program later falsified: Phase-107 held-out score 0.000, 0 of 115).
- **Feasibility:** RUNNABLE-TODAY.

**The question in plain words.** Forget the old machinery. Take the signs whose
values are not in dispute, and ask a narrower question that a sound method can
answer: when each candidate language family's word-values are assigned to a small
set of anchor signs, which family's assignments make the actual inscription
sequences look most probable — and does the winner beat not just the other
families but also the result of assigning values at random?

**Hypothesis.** Proto-Dravidian assignments produce inscription sequences with
higher probability than Indo-Aryan (Sanskrit), Munda, and isolate-baseline
assignments, by a margin fixed below, and beat the random-assignment control.

**Falsifier.** The hypothesis fails if any rival family matches or beats the
Dravidian assignments, or if Dravidian's margin over the best rival falls below
the fixed margin, or if random assignments reach the same range — any of which
means the comparison carries no information about language family.

**Data.** The strict sign set (the 94 strict-core readings in
`backend/reports/INDUS_FINAL_ANCHORS.json`, validation status strict) and the
program's V3/Mahadevan-lineage corpus as held in the database — the same corpus
family the original comparisons used, so the rerun is comparable to them. Anchor
candidate values come from published sources only: the Dravidian Etymological
Dictionary tradition for Dravidian, standard Sanskrit lexicon values for
Indo-Aryan, published Munda reconstructions for Munda. All data in hand; all
published; derived statistics publishable.

**Method (SA-free by construction).** No semantic anchoring and no anchor
promotion anywhere in the design (H26). For each family: fix the same small set
of anchor signs (the five-per-language pattern of the original Phase-41
comparison, with the anchor list frozen before any run); assign that family's
published word-values to them; score every inscription sequence under a simple
counted model (sign-sequence probabilities estimated from the corpus itself,
with the assigned values contributing only through the phoneme sequences they
imply — the exact estimator is fixed at freeze time and is the same for every
family). Controls run in the same pass: (a) 999 random assignments of the same
values to the same anchor signs, giving the no-information distribution;
(b) a no-language baseline in which anchor signs carry no values at all.
Harappa concentration is handled by reporting the comparison a second time with
Harappa's inscriptions removed, as a pre-registered sensitivity — the verdict
rests on the primary run only.

**Criteria fixed in advance.** The margins are set from the original results so
the rerun can fail the claim, not just re-confirm it: the original Phase-41
margin was a likelihood ratio of 1.0566 to 1 and Phase-43's was 0.484 log units
per sign. SUPPORTED (for the bounded claim "Dravidian assignments fit better
than the named rivals under this method"): Dravidian beats the best rival by at
least 0.10 log units per sign on the primary run **and** sits above the 99th
percentile of the random-assignment distribution. NOT SUPPORTED: any rival at or
above Dravidian, or Dravidian inside the random distribution's range.
INCONCLUSIVE: Dravidian first but by less than 0.10 log units per sign, or the
Harappa-removed sensitivity reverses the ranking. The claim's status after the
run is re-earned under this method or it is not: if the result is NOT SUPPORTED,
the inherited partial support is replaced by the new record in an appended,
dated entry — the old SA-based numbers stay in history, labelled as produced by
a falsified method.

**Controls and named confounders.** Only-two-families bias (the original defect):
three families plus two controls, all named in advance. Anchor-picking bias: the
anchor list is frozen before any family is scored, and a second pre-registered
anchor list (the next five published candidates per family) is run as a
robustness arm. Within-lineage corpus: named in the verdict wording — a win is a
win inside the Mahadevan lineage, and D-01/D-24 are the designs that speak to
other lineages.

**What it would move.** The claim from IN QUESTION to a re-earned checked status
(supported, not supported, or inconclusive) under a method the program trusts —
the first time its status would rest on post-falsification evidence.

**What it would NOT establish.** Not the rebus method itself, not any single
sign's reading, not a decipherment. A statistical fit between one family's
word-values and the sign sequences is one kind of evidence, and the design says
so in its own verdict wording.

---

## D-04 — The fish-sign family, tested sign by sign

- **Claim:** `parpola_2010_dravidian_solution_manual_002` (IN QUESTION —
  partially supported: Mahadevan sign 72 passed its positional test; sign 267,
  the family's most frequent member, failed it clearly).
- **Feasibility:** RUNNABLE-TODAY.

**The question in plain words.** The claim says *the fish sign* — a family of
related fish signs — works as the script's primary sound-sign (the 'meen'
reading). One member behaves as the reading predicts; the commonest member does
not. Is the family uniform, or was the one pass the exception?

**Hypothesis.** If the fish family carries one reading, its members should share
the positional behaviour the reading predicts: what follows a fish sign should
look like word endings at similar rates across the family.

**Falsifier.** The hypothesis fails if the family's token-weighted majority
behaves like sign 267 rather than sign 72 under the criteria below — that is, if
most fish-sign occurrences are *not* followed by text-ending behaviour.

**Data.** The strict corpus (the same strict sign set as D-03) with the
Phase-43 positional framework. Family membership is fixed in advance from
Parpola's published list (the record names Mahadevan signs 72, 64, 70, and the
Phase-43 test's six fish candidates) — the membership list is frozen in the
design's freeze step, before any counting, and no sign is added or removed after
results are seen.

**Method.** For every family member with at least 30 occurrences in the strict
corpus: compute the rate at which the following sign is a text-ending sign (the
Phase-43 test T2.4 measure, unchanged). Recorded reference points: sign 72 —
181 occurrences, 25.9% ending-followers; sign 267 — 356 occurrences, 3.8%.
Report each member separately and the token-weighted family rate. Because
which drawn sign counts as "the fish sign" differs across compilations
(Phase-125), the whole test is repeated on the Holdat layer's numbering as a
pre-registered second arm, with the crosswalk stated per sign.

**Criteria fixed in advance.** A member PASSES at an ending-follower rate of
20% or more (the level sign 72's recorded behaviour establishes as the
reading's signature; the exact bar is confirmed at freeze against the T2.4
record before any new counting). FAMILY SUPPORTED: members carrying at least
70% of the family's total occurrences pass. FAMILY NOT SUPPORTED: members
carrying 30% or less of occurrences pass. INCONCLUSIVE: between those, or the
two compilation arms disagree about the family's most frequent member. Any
member below the 30-occurrence floor is reported as TOO THIN and excluded from
the weighting, with its count stated.

**Controls and named confounders.** Position effects that have nothing to do
with sound values (a sign could sit before endings for structural reasons):
a control set of non-fish animal signs, matched for frequency, run through the
identical measure — if control animals pass at the same rate, the fish result
is reported as a positional fact, not as support for the reading. Compilation
disagreement: the second arm above. Family-definition discretion: the frozen
membership list, plus a stated sensitivity using only signs 72, 64, 70 (the
three the claim's own record names).

**What it would move.** The claim from IN QUESTION to supported / not supported
/ inconclusive as a *family* claim — replacing the current average of one pass
and one failure.

**What it would NOT establish.** That any fish sign was pronounced 'meen', the
fish/star wordplay, or the reading of any inscription. Positional behaviour is
a necessary shadow of the reading, not the reading.

---

## D-07 — How much is a curve fit worth? (residue design for the Zipf claim)

- **Claim:** `yadav_2009_arxiv_manual_001` (SETTLED — strongly supported; the
  recorded exponent is about 1.35, in the range the original work reported).
- **Feasibility:** PARTIAL. Arm A runs today; arm B is the same blocked
  precondition as D-01 arm B.

**The open point.** The verdict stands — the frequencies do fit the
Zipf-Mandelbrot curve on this corpus. The residue is what the fit is *worth*:
many non-language systems produce the same curve, and the fitted exponent moves
with corpus size and with how signs are split or merged. The claim's
not-understood text asks for two things: the fit measured against known
non-linguistic systems, and the same fit on an independent corpus.

**Arm A — the control-systems comparison (RUNNABLE-TODAY).** Hypothesis: the
Indus fit is *distinguishable* from the fits of known non-linguistic symbol
systems. Falsifier: at least one named non-linguistic system fits as well or
better under the same fitting rules. Method: fit the identical Zipf-Mandelbrot
estimator to (a) the Indus strict corpus, (b) at least three published
non-linguistic symbol inventories named at freeze (for example heraldic charge
frequencies, Mesopotamian numerical-sign frequencies from published counts,
and a synthetic emblem inventory generated under a stated random process), and
(c) at least one known linguistic corpus as a positive control. Also report
the exponent's movement under corpus subsampling (halving, quartering) and
under the crosswalk's sign split/merge variants — a sensitivity table, fixed in
advance. Criteria: the arm's conclusion is a stated comparison ("the Indus fit
is / is not separable from the non-linguistic controls on these measures"),
reported as a bounded finding attached to the claim, not a verdict change.

**Arm B — the independent-corpus fit (BLOCKED).** The identical fit on a corpus
independent of the Mahadevan lineage, with the sign inventory fixed in advance.
Blocked on the same precondition as D-01 arm B: no such corpus exists in hand
today (the 2026-10-08 sweep's answer was no). Unblocking act: an independent
corpus entering through Phase-130 intake.

**What it would NOT establish.** Arm A cannot promote the fit into evidence
that the script encodes language — that is exactly the over-reading the residue
exists to prevent. Its product is an honest strength label for a settled claim.

---

## D-08 — Give the opening/closing-sign claim its falsifier, then rerun it

- **Claim:** `yadav_2009_arxiv_manual_002` (IN QUESTION — strongly supported on
  the counts, but the record carries no falsification condition: as recorded,
  the claim could not have failed, which is the precise defect the program's
  current discipline flags).
- **Feasibility:** RUNNABLE-TODAY.

**The question in plain words.** Some signs really do prefer the start of texts
and others the end — the counts (40 opening-strong signs, 20 closing-strong, in
the Phase-43 battery) are not in dispute. The open point is whether that
pattern survives when the rules are fixed sharply enough that it *could* fail:
on the strict sign set, and in the other great compilation.

**Hypothesis.** Under position rules frozen in advance, a stable set of signs
prefers text-initial position and a stable set prefers text-final position,
in both the strict corpus and the Holdat layer, with membership overlap well
above chance.

**Falsifier (written onto the record by this design, before any rerun).** The
claim fails if, under the frozen rules, fewer than half of the original 40/20
sign sets reappear on the strict corpus; or if the two compilations' strong-sign
sets overlap no more than shuffled sign labels do; or if the effect disappears
when inscription segmentation follows the other compilation's conventions.

**Data.** The strict sign set and V3 corpus (arm 1); the Holdat layer (arm 2) —
both in hand. Segmentation conventions per compilation as published.

**Method.** Re-run the Phase-43 positional battery with its thresholds
unchanged, on the strict corpus; then on the Holdat layer under its own sign
numbering, mapping results through the crosswalk with conflict pairs reported
separately. Overlap between compilations measured against a label-shuffle
null (999 shuffles).

**Criteria fixed in advance.** SUPPORTED (re-earned): both arms reproduce at
least half the original sets **and** cross-compilation overlap exceeds the 95th
percentile of the shuffle null. NOT SUPPORTED: any falsifier condition above
fires. INCONCLUSIVE: one arm reproduces and the other does not, with counts
stated. The falsifier text itself is appended to the claim record as part of
the design's freeze, whichever way the rerun lands — the record defect is
fixed by the design, not by the outcome.

**Controls and named confounders.** Segmentation dependence (named in the
claim's not-understood): the second compilation's conventions are the control.
Corpus-size effects: rates reported with counts, and a minimum-occurrence
floor identical in both arms. Crosswalk conflicts: reported, never dropped
silently.

**What it would move.** The claim from IN QUESTION to a re-earned status with a
falsifier on its record — or to not supported, which the current record makes
impossible and is therefore the more informative outcome if it comes.

**What it would NOT establish.** That the script encodes language (opening and
closing markers occur in non-linguistic systems too), or what any opening or
closing sign means.
