# Spec 052 — Amendment draft (2026-10-23): battery NB-1 on the Shakti corpus layer

> ## AMENDMENT — FOR OWNER MINI-GATE — 2026-10-23
>
> Drafted under Item 2 of the owner-approved
> waiting-decisions package of 2026-10-23, on the
> rulings recorded in `adjudication.md` §9. This
> amendment is a draft: it returns to the owner as a
> mini-gate, and nothing in it freezes, files, or
> executes Spec 052. Where this amendment and the
> unamended draft disagree, the amendment governs
> once the owner approves it; until then the draft
> stands as written, with its freeze failure of
> 2026-10-21 as the operative record.

> ## APPROVED — OWNER MINI-GATE — 2026-10-23
>
> Approved as specified by the owner on
> 2026-10-23 at 22:59 EDT ("Approve both
> mini-gates as specified"), recorded in
> `adjudication.md` §10. The freeze followed
> the same evening: Spec 052 is frozen as
> amended (`freeze.md` / `freeze.json`), and
> its OSF registration is filed
> (`osf-spec-registration.md`). Execution
> remains a separate owner order.

## 1. What this amendment does

The 2026-10-21 freeze attempt failed for two reasons
(`adjudication.md` §8): the Phase-43 battery cannot be
reconstructed from the record that survives (gate 0.5,
BATTERY NOT PINNABLE), and the Soviet mapping the design
required cannot be built from the records the program
holds (§8.3–§8.4). The owner's rulings of 2026-10-23
(§9.1, §9.2) settle both: nothing may be invented or
borrowed under the Phase-43 name, and arm A as designed
is closed, its Soviet tables retired.

This amendment therefore does two things, and no more:

1. It defines a **new battery, NB-1**, in full — every
   element, every constant, each with its derivation or
   its honest basis stated next to it (§3 below).
2. It re-points the spec's surviving machinery — the
   two sub-predictions F and O, the outcome words, the
   append duties — at inscription-level material the
   program actually holds: the **Shakti corpus layer**
   (§4), under amended step-0 gates (§5).

What it does not do: it does not touch the parent
claim's status (contradicted, as recorded; §6 of the
spec stands); it does not reopen arm B (campaign E-3
stands); it does not claim NB-1 reproduces, recovers,
or approximates the Phase-43 battery — the Phase-43
record is used only where §3 says it is used, as a
consistency check on two constants, and as the source
of the partition property NB-1 adopts.

## 2. The question, restated for the amended run

Farmer, Sproat and Witzel's thesis rests on measured
absences in the Soviet compilation's dataset: no
dedicated final-position sign sets of the kind mature
writing systems show, and no fixed inscription-opening
formula. Spec 052 asks whether that pattern is a fact
about the Indus material or an artefact of one
compilation's dataset. The original arm A could not ask
it: its battery was unrecoverable and its mapping
unbuildable.

The amended run asks the same question of a different
compilation: the Shakti corpus layer, assembled in this
program from the CISI corpus tradition (see §4). If the
Farmer pattern — no dedicated final sets, no opening
formula — is present there too, under a battery defined
before the run, the "artefact of the Soviet dataset"
caveat on the thesis narrows. If the pattern is absent
there, the caveat widens. Either way the run is a
consistency check on a settled claim, exactly as the
design (D-01) made arm A; it moves no verdict.

One limit is stated plainly, because the amendment
could otherwise overclaim: the two compilations are
distinct lineages of scholarship — different editors,
different sign numbering, different segmentation
decisions — but they are editions of substantially the
same excavated objects. Agreement between them is
evidence about the pattern's robustness across
compilations, not independent discovery of the pattern
in new material.

## 3. Battery NB-1 — full specification

NB-1 is a new battery. It is not the Phase-43 battery,
and no element of it is presented as recovered from the
Phase-43 pipeline: that pipeline's rules were never
recorded (`adjudication.md` §8.2), and the owner's
ruling (§9.1) forbids supplying them under its name.
Two things are taken from the Phase-43 record, both
labelled where they are used: the **partition property**
(NB-1.2) that the results file observably has, and a
**consistency check** on the strength band (NB-1.5):
the ten TERMINAL_STRONG signs the record exhibits, with
their counts and rates, are the one piece of the old
battery's output a new battery can be checked against
without inventing anything.

### NB-1.1 — Population

The battery runs on a named population of inscriptions.
Each inscription enters as the corpus layer's own
record of it: the layer's sign numbering, and the
layer's own segmentation of the inscription into a
sequence of signs. No re-segmentation, no renumbering,
and no crosswalk is applied at any point in the run.

### NB-1.2 — Position classes

In a sequence of length n ≥ 2: the first sign is an
**initial** occurrence, the last sign is a **terminal**
occurrence, and every sign between them is a **medial**
occurrence. A sequence of length 2 contributes one
initial and one terminal occurrence and no medial
occurrence. Sequences of length 1 are counted and
reported separately (their number is part of the run
record) and enter no count below. Every counted
occurrence of a sign therefore belongs to exactly one
of the three classes — the partition property the
Phase-43 results file observably has (its three
tables' counts sum exactly to each sign's total).

### NB-1.3 — Counts and rates

For each sign s: N(s) = its total occurrences in
sequences of length ≥ 2; I(s), T(s), M(s) = its
occurrences in the initial, terminal, and medial
classes. By NB-1.2, I(s) + T(s) + M(s) = N(s) exactly.
The class rates are i(s) = I(s)/N(s), t(s) = T(s)/N(s),
m(s) = M(s)/N(s).

### NB-1.4 — Count floor

A sign is **classifiable** in a population iff
N(s) ≥ 20. Signs below the floor are reported with
their counts and marked TOO THIN for that population;
they are members of no strong set, and they are never
silently dropped from the report.

*Basis.* In the Phase-43 results file, the smallest
total count among the ten exhibited TERMINAL_STRONG
signs is 22 occurrences. A floor of 20 therefore
excludes none of the signs the recorded class actually
contains, while bounding every rate's resolution at
1/20 = 0.05. The floor is a stated design constant
checked against the record in this one respect; it is
not a recovered Phase-43 value (the record states no
floor).

### NB-1.5 — Strength bands

For a classifiable sign:

- **TERMINAL_STRONG** iff t(s) ≥ 2/3;
  **TERMINAL_MODERATE** iff 1/2 ≤ t(s) < 2/3.
- **INITIAL_STRONG** iff i(s) ≥ 2/3;
  **INITIAL_MODERATE** iff 1/2 ≤ i(s) < 2/3.
- **MEDIAL_STRONG** iff m(s) ≥ 2/3;
  **MEDIAL_MODERATE** iff 1/2 ≤ m(s) < 2/3.

*Basis.* The ten exhibited Phase-43 TERMINAL_STRONG
signs have terminal rates from 0.683 to 0.892. The
STRONG edge 2/3 ≈ 0.667 lies just below the lowest
rate in that recorded class, so every exhibited member
of the class is TERMINAL_STRONG under NB-1. That is a
consistency property this battery was checked against
before being proposed — it is **not** a derivation of
2/3, and NB-1 does not claim the Phase-43 threshold was
2/3 (it was never recorded). The MODERATE edge 1/2 is
the plain reading "in this position more often than
not", a design choice. No exhibited rates exist for
the initial class (the Phase-43 record exhibits initial
counts but no initial strong set and no rates for one),
so the initial and medial bands carry no recorded
anchor at all: the same bands apply there by symmetry
of definition, labelled a design choice, not a
recovery.

### NB-1.6 — Opening bigrams and dominance (Spec 052 element)

The **opening bigrams** of a population are the first
two signs of each sequence of length ≥ 2, one per
sequence. Let B = the number of sequences of length
≥ 2. The **dominance** of the most frequent opening
bigram is its count divided by B.

*Basis.* The Phase-43 record contradicts itself about
its own opening pair — the pair (267, 99) carries
count 251 in one table and 278 in the other — and
states no denominator anywhere for its "0.74
dominance", which matches no denominator on the record
(`adjudication.md` §8.2). NB-1 removes the ambiguity by
naming the denominator outright: B, the number of
sequences that have an opening bigram. That is a
definition, labelled as such; nothing is recovered.

### NB-1.7 — Chance baseline: within-sequence permutation null

The null model holds each sequence's length and its
multiset of signs fixed, and permutes the signs within
each sequence uniformly at random, each sequence
independently. For each of **999 permutations**, the
run recomputes: (a) the count of TERMINAL_STRONG signs,
and (b) the dominance of the most frequent opening
bigram. The **chance level** of each statistic is the
95th percentile of its 999 null values, nearest-rank
(the 950th smallest). **Random seed: 43052**, fixed
here; the implementation records its generator
algorithm and library in the run record, and the
amended step-0 gates (§5) require a second run with
the same seed to reproduce the first run's outputs
exactly.

*Basis.* The permutation null asks one narrow
question: could sign order alone — with every
sequence's contents and length held fixed — produce
this much positional concentration? It is a design
choice among null models, stated with its question;
it is deliberately not the Phase-43 baseline, whose
method the record does not state at all (§8.2). 999
permutations give percentile resolution of 0.001;
the 95th percentile is the conventional one-sided 5%
level, labelled a convention.

### NB-1.8 — The two pattern conditions

- **Condition F** (dedicated final sets) holds iff at
  least one TERMINAL_STRONG sign exists **and** the
  observed count of TERMINAL_STRONG signs exceeds the
  NB-1.7 chance level for that count.
- **Condition O** (opening formula) holds iff the most
  frequent opening bigram's count is ≥ 10 **and** its
  dominance exceeds the NB-1.7 chance level for
  dominance.

*Basis for the count floor in O.* Below ten
occurrences, a "formula" is an anecdote; the floor is
a design choice, stated before any run. The floor in
F is NB-1.4's classifiability floor, applied through
the strong set's definition.

### NB-1.9 — TOO THIN gate

The run closes **TOO THIN** — before any rate is
computed — if the population has fewer than 30
sequences of length ≥ 3, or fewer than 10 classifiable
signs.

*Basis.* The draft's own gate 0.6 used 30 records with
texts of at least 3 signs as its thinness line; this
gate keeps that number and that form, and adds the
classifiability line so a strong set is never
pronounced on a handful of signs. Both numbers are
stated before any run.

## 4. The amended run's data — the Shakti corpus layer

**Population, primary.** The inscription-level records
of the Shakti corpus layer whose compilation lineage is
documented — the population the program has already
frozen and run once: Spec 068's primary set (3,045
inscription rows; 11,805 sign tokens; 557 distinct
signs), in the layer's own (ICIT) numbering and
segmentation. **Sensitivity population:** the layer's
full analyzable set (5,131 rows). The battery runs on
the primary population; the sensitivity population is
run and reported with the same prominence if, and only
if, the primary run reaches an outcome word (the
draft's §5 discipline, carried over).

**Venue and custody.** The Shakti source rows are
restricted material: they live only in the restricted
local store, they never enter git, and the run happens
in that venue (the standing restricted-data rule, as
recorded for Spec 068). What publishes is what the
draft's §6 headline rules publish: the dataset label,
the census, the per-sign quantities, the strong sets,
the null percentiles, and the outcome word — derived
statistics, never source rows.

**Pins.** The freeze act pins the corpus-layer file
and its row-grades file by SHA-256, taken at freeze
time from the restricted store, and records the
primary population's extraction counts (rows, tokens,
distinct signs) as the values step 0 must reproduce.
This amendment deliberately pins nothing by hash: the
layer is living restricted material, and pinning it
here, in a draft, would freeze a copy the freeze act
has not examined.

**Lineage, stated once more.** The layer's lineage is
the CISI corpus tradition as documented in the
program's 2026-10-22 readiness decisions (P-F1) — a
different compilation from the Soviet dataset behind
the claim's original outcome, with its own numbering
and segmentation. §2's limit applies: distinct
compilation, same excavated objects.

## 5. Amended step-0 gates

The draft's §3 gates 0.1–0.3 (Soviet records pins) and
gate 0.5 (battery derived from the Phase-43 record) are
replaced by the following. All gates run, in order,
before any positional quantity is computed
(F052-C08's discipline, unchanged). No failure is
repaired at run time; a repaired input is a new
freeze.

- **Gate A — corpus pin.** The corpus-layer file and
  row-grades file hash to the freeze values. Failure:
  **INVALID**.
- **Gate B — population reproduction.** Extracting the
  primary population from the pinned layer reproduces
  the freeze-recorded counts (rows, tokens, distinct
  signs) exactly. Failure: **INVALID**.
- **Gate C — determinism.** The battery implementation,
  run twice over the pinned layer with seed 43052,
  produces identical outputs. Failure: **INVALID**.
  (This replaces the draft's BATTERY NOT REPRODUCED
  question, which belonged to the Phase-43 battery;
  NB-1 has no external original to reproduce, so the
  gate is its own determinism.)
- **Gate D — thinness.** NB-1.9 applied to the primary
  population. Failure: **TOO THIN** closure, with the
  census as its finding.

The draft's remaining closure classes are disposed of
as follows: BATTERY NOT PINNABLE cannot occur (the
battery is this amendment, pinned at freeze);
NOT ADJUDICATED is retained for a chance baseline that
cannot be computed as frozen; the Soviet mapping-failure
closures of §4.3 (MAPPING UNRESOLVED &c.) are retired
with the tables they belonged to — there is no mapping
in the amended run.

## 6. Outcomes under the amendment

§4.1's words, re-pointed at NB-1 and §4's population:

- **CONSISTENT** — neither F nor O holds on the
  primary population. The Farmer pattern is present in
  the CISI-lineage corpus as well; the "artefact of
  the Soviet dataset" caveat narrows. The claim's
  contradicted status and the fragments' split stand
  as recorded (§6 of the spec).
- **INCONSISTENT** — F and O both hold. Positional
  structure of the kind the thesis denies is present
  in this compilation; the caveat widens, and the
  asymmetry with the Soviet outcome becomes the
  recorded finding.
- **PARTIAL** (DD-052-3, retained) — exactly one of F,
  O holds; the outcome names which, and states the
  half of the thesis each condition carries.
- **TOO THIN** — gate D's closure; the census is the
  finding.

The §4.2 append duties survive unchanged in form: the
outcome, in the same words, appended to the parent
claim's record and to each of the three fragments'
records, naming the dataset (the Shakti corpus layer,
CISI-compilation lineage) and the battery (NB-1, this
amendment as frozen). The headline rules of §6 survive:
census and per-sign quantities before the outcome
word; no verdict language about the thesis itself.

## 7. What the owner is asked to decide (the mini-gate)

1. Approve battery NB-1 as specified in §3 — elements,
   constants (floor 20; bands 2/3 and 1/2; 999
   permutations; seed 43052; percentile rule; TOO
   THIN lines 30 and 10) — or amend any of them by
   name.
2. Approve the re-scoped data of §4 (Shakti corpus
   layer; Spec 068's primary population; sensitivity
   population; restricted venue; pins at freeze).
3. Approve the amended gates and outcome semantics of
   §5–§6, including the retirement of the Soviet
   tables and of the §4.3 mapping closures.

On approval, the path is the draft's own: AEE
lifecycle hooks over the recovered register (tasks
L4), the freeze act (L5 as amended by this document,
L6), the OSF filing, and a separate execution order.
On decline, this amendment and §9 of the adjudication
stand as the record, and the spec stays un-frozen.

## 8. What this amendment does not establish

Approving this amendment establishes a testable
design, nothing more. It does not establish that the
Farmer pattern is or is not present in the Shakti
layer (that is the run's question); it does not
establish that NB-1 measures what the Phase-43 battery
measured (the two agree, by construction, only on the
NB-1.5 consistency check); and it does not move, or
promise to move, the parent claim's recorded status.

---

*AI disclosure: drafted by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
