# Spec 038 — PRED-2026-007 at full population: enumerate every ITM-coded sign, then score the registered criterion over the whole population (D-31)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> This is a **draft** design contract, written
> under the owner's draft order of 2026-10-20
> (`adjudication.md`). It implements design
> **D-31** of the experiment-design portfolio
> (PR #195, `docs/research/experiment-designs-
> 2026-10-13/05-predictions.md`, branch
> `designs/035-open-questions` @ `43f56191`) for
> the already-registered prediction
> **PRED-2026-007**. Spec and number: the CISI
> concordance draft took Spec 037 and the
> PRED-2026-011 scoring draft took Spec 036, so
> this draft takes **Spec 038** — the next free
> number. Execution is provisionally
> **Phase-401** (Phase-400 is reserved by Spec
> 036; the phase number is confirmed at the
> freeze act, DD-038-8).
>
> Nothing in this draft is frozen and nothing is
> executed. The freeze is a separate owner
> decision — at which the AEE lifecycle hooks
> run as a gate, under **aee 1.5.0** (adoption in
> flight; §13, DD-038-7) — and execution is a
> further separate owner decision.
> **The ITM population is NOT enumerated by this
> draft.** Enumeration is step 0 of the
> execution, and it has not run. No Phase 5
> assignment has been looked up for any sign
> beyond the three signs the register's own
> Tested note already names, and no share has
> been computed.

## 0. Basis

### 0.1 The registered prediction (the contract this design implements)

PRED-2026-007 (H4: ICIT Function Alignment),
registered 2026-04-22 in
`docs/PREDICTION_REGISTER.md` §3, carried
**verbatim**:

- **Prediction**: "Signs with ICIT function
  code ITM will cluster into TERMINAL class in
  CGSA Phase 5 at rate ≥ 70%."
- **Withheld data**: "ICIT function codes (from
  mayig features)"
- **Success criterion**: "≥ 70% of ITM-coded
  signs are TERMINAL or cluster in TERMINAL
  clusters"

The success criterion is the operative scoring
text. Where the Prediction sentence and the
Success criterion differ in wording, the
criterion governs and the difference is flagged,
not harmonised (DD-038-3).

### 0.2 The recorded partial test (the pre-execution record)

The register's Tested/Outcome fields, carried
verbatim:

- **Tested**: "PARTIALLY — P385 (ITM) is Cluster
  21 TERMINAL; P378 (ITM) is Cluster 39
  TERMINAL; P098 (LOG) is Cluster 10 INITIAL.
  2/3 ITM in TERMINAL (67%)"
- **Outcome**: "PARTIALLY CONFIRMED (one more
  ITM needed for full pass)"

This is a pre-execution record on a sample of
three named signs. It is not the registered
test run at full scope: the register nowhere
records how many ITM-coded signs exist in
total. The Spec 029 claim-lifecycle audit
(2026-10-12) already flagged the
"PARTIALLY CONFIRMED" wording as
acceptance-flavoured over a checking-stage
partial outcome; the claim's own
not-understood text states what would change
the picture — the check run over every
ITM-coded sign, with the population size stated
first. That is this design.

One feature of the recorded note is stated
exactly, because the census branch of this
design turns on it (DD-038-1, disposed in
`adjudication.md` §3): the note names **two**
ITM-coded signs (P385, P378) and one LOG-coded
sign (P098), yet reports the rate as "2/3" — a
denominator of three checked signs. **The
register's 67% figure is a pre-execution
record whose denominator mixed in a non-ITM
sign.** The registered criterion ranges over
ITM-coded signs only, and the design's own
controls state that P098 "is not an ITM sign
and is excluded from the count". The design
text (D-31) nevertheless anticipates "its
outcome is 2 of 3" for the census closure.
This spec carries **no pre-written outcome**
for any branch: §6 states the verdict rule
mechanically — the share over the enumerated
ITM population against the 70% bar, under the
coverage rule — and every outcome, the census
branch included, is whatever that rule yields
at execution over the enumerated population
and the recorded assignments.

### 0.3 The design source

D-31 prescribes, in substance: step 0 first
enumerates the full ITM population from the
authoritative function-code table and fixes the
code table's provenance (including an appended
reconciliation note for the register's "from
mayig features" line — the register text itself
is never edited); scoring then takes each
enumerated sign's cluster assignment from the
**recorded CGSA Phase 5 output only** — no
re-clustering; if the recorded Phase 5 output
does not survive in sign-assignable form, the
design closes as CANNOT BE RUN AS WRITTEN; if
the enumerable population is exactly the signs
already tested, the design closes with the
census as its finding (a completion, not a
failure); the coverage rule for unassigned
signs is fixed in advance (§6); the per-sign
table is published with the outcome; the
LOG-coded P098 is excluded by rule.

D-31's own verification (2026-10-13), restated
here because step 0 is built on it: the mayig
feature files under
`data/raw/other_sites/mayig_features/` carry
visual features and grapheme lists per sign —
**no function codes at all** — while
`backend/glossa_lab/data/fuls_parser.py` reads
the function codes (NUM, LON, SHN, TMK, ITM,
LOG, SYL) from a Wells-derived source text
(its catalog parser is annotated "Function
classification (from Wells)"). The register's
provenance line and the held files therefore
disagree. Step 0 does not go hunting for a
table by preference: §3 check 0.1 names the
**primary source**, the **cross-check**, and
the **conflict rule** in advance (DD-038-5,
disposed), and step 0's provenance job is to
verify those sources, record their hashes, and
append the reconciliation note.

## 1. Question

Does the registered criterion for
PRED-2026-007 hold over the **full enumerated
population** of ITM-coded signs — every such
sign, not the three the partial test happened
to check? Plainly: the prediction says signs
labelled ITM in the old ICIT coding end up in
text-ending (TERMINAL) clusters at least 70% of
the time. The only check ever run looked at
three signs. This study first counts how many
ITM signs there actually are, then checks every
one of them against the clustering the
prediction named.

## 2. The population frame (fixed here, enumerated at step 0)

The population is defined exactly; its
membership is execution work.

- **Unit.** A **distinct sign**, identified by
  the sign ID under which the primary
  function-code source (check 0.1) records it.
  The criterion
  ranges over signs, not inscriptions, tokens,
  or occurrences; frequency plays no part in
  membership.
- **Inclusion.** A sign is in the population
  if and only if the primary function-code
  source named at check 0.1
  (`reports/indus_cgsa_cluster_analysis.json`,
  `data.a[].icit_function`) records its ICIT
  function code as exactly **ITM**. The
  enumeration records the raw field value for
  every included sign.
- **Exclusion.** Every sign whose recorded code
  is anything else — LOG, SYL, TMK, NUM, SHN,
  LON, or no code — is excluded. The standing
  example is **P098 (LOG)**, named in the
  register's Tested note: it is not an ITM sign
  and is excluded by this rule, as the design
  prescribes — stated here so the exclusion is
  a rule, not a convenience (its bearing on the
  recorded 2/3 arithmetic is DD-038-1's, §0.2).
- **No other filter.** No frequency threshold,
  no attestation requirement, no restriction to
  any numbering system beyond the sign IDs the
  table itself records, and no exclusion of
  signs that turn out to lack a Phase 5
  assignment — those signs are handled by the
  coverage rule (§6), never by quietly dropping
  them from the frame.
- **Deduplication.** By sign ID: each distinct
  sign ID counts once, however many rows,
  files, or inscriptions mention it.
- **Ambiguity is a closure, not a judgement
  call.** If the primary source records a sign
  under conflicting codes, or records function
  codes in a multi-code or otherwise ambiguous
  encoding that affects membership, the
  ambiguity is written into the step-0 record
  and the study closes as **CANNOT BE RUN AS
  WRITTEN** rather than resolving membership
  by discretion (§3, check 0.1's conflict
  rule).

## 3. Step 0 — enumeration and provenance, fail-closed, in a fixed order

Step 0 runs before any scoring, in this order.
Each check has a stated failure outcome; no
check is waived, sampled, or repaired by
substitution.

### 0.1 Fix the function-code sources: primary, cross-check, conflict rule

The sources are named here, before any
enumeration, so the population cannot be
chosen by shopping among tables (DD-038-5,
disposed in `adjudication.md` §3):

- **Primary source.**
  `reports/indus_cgsa_cluster_analysis.json`,
  field `data.a` — the recorded CGSA analysis
  output's per-sign records (611 records,
  verified at draft by form: keys include
  `sign_id`, `icit_function`, `start_rate`,
  `end_rate`, `internal_rate`, `mahadevan_ids`,
  `wells_ids`; the `icit_function` **values**
  were not inspected — reading them across
  signs would be the enumeration). A sign's
  function code under this design is its
  primary source record's `icit_function`
  value.
- **Cross-check source.**
  `data/crosswalks/canonical_sign_registry.csv`,
  column `icit_function` — the canonical sign
  registry `docs/research/SIGN_INVENTORY.md` §2
  describes as carrying the ICIT function code
  per sign.
- **Provenance lineage.**
  `backend/glossa_lab/data/fuls_parser.py`
  records where the code vocabulary comes
  from: its catalog parser reads the function
  codes (NUM, LON, SHN, TMK, ITM, LOG, SYL)
  from Wells-derived catalog lines ("Function
  classification (from Wells)"). This is the
  lineage the primary source's field descends
  from; it is cited for provenance, not used
  as a third table.
- **The mayig features are not a source.** The
  files under `data/raw/other_sites/mayig_features/`
  carry no function codes (§0.3); the
  register's "from mayig features" line is
  reconciled by append, not acted on
  (DD-038-2).

Step 0 verifies each source's presence and
records its SHA-256 at the frozen commit; a
missing or structurally changed primary
source (no `data.a`, no `icit_function` field)
closes the study as **CANNOT BE RUN AS
WRITTEN**.

**Conflict rule, fixed in advance.** The
primary source governs membership. Every sign
on which the cross-check's `icit_function`
disagrees with the primary's — in either
direction — is written, sign by sign, into
the step-0 record and published with the
outcome; disagreements do not change
membership. Two exceptions close the study as
**CANNOT BE RUN AS WRITTEN**: the primary
source records conflicting codes for the same
sign, or a sign's primary `icit_function`
value is a multi-code or otherwise ambiguous
encoding that §2's exact-match rule cannot
decide. No union, no intersection, and no
third source is consulted to break a tie.

Step 0 also writes the **provenance
reconciliation note**: a dated addition
appended to the register (§7) reconciling the
register's "ICIT function codes (from mayig
features)" line with what the files actually
contain. The register text itself is not
edited (DD-038-2).

### 0.2 Enumerate the population

From the primary source (check 0.1), enumerate
**every** ITM-coded sign under §2's frame, and
record the enumeration — the full per-sign
list, the source it came from, and the
population size — in the step-0 record, hashed
before any Phase 5 assignment is looked up.
Completeness checks, fixed in advance:

- The enumeration is produced by a mechanical
  read of the primary source's `icit_function`
  field over all 611 of its per-sign records —
  not by searching for signs already believed
  to be ITM.
- The count of records read is recorded and
  reconciled against the source's own structure
  (the `data.a` record count at the frozen
  commit).
- The cross-check (check 0.1) is run over the
  whole cross-check source, and every
  disagreement is recorded under the conflict
  rule — the cross-check never silently adds
  or removes a member.
- Every sign named ITM-coded anywhere else in
  the held record (including the register's
  Tested note) is checked against the
  enumeration: any ITM-coded sign the
  enumeration missed is a discrepancy written
  into the step-0 record; under the conflict
  rule it changes membership only if the
  primary source itself records it as ITM.

### 0.3 Verify the recorded Phase 5 output survives in sign-assignable form

The scoring reads **only** the recorded CGSA
Phase 5 output: the sign → cluster assignment
(`outputs/analysis/sign_clusters.json` —
verified surviving at draft: best_k 40,
`sign_to_cluster` for 160 signs, 40 populated
cluster lists; corroborated by
`reports/cgsa_validation_report.md`, dated
2026-04-22, the registration day: best k 40,
largest cluster 12/160, entropy reduction
0.3204) and the recorded per-cluster class
characterisation (`reports/cluster_characterization.md`,
generated 2026-04-22, 40 clusters). The
design's "recorded output does not survive"
closure branch is therefore expected to stay
unused — but it stays written: if that output
does not survive in a form that assigns a
cluster and a cluster class to a sign, the
study closes as **CANNOT BE RUN AS WRITTEN**,
unscored: a fresh clustering is a new
prediction's business, under a new number
(the design's rule, carried verbatim). **No
re-clustering is run under this spec, for any
reason.**

**Cluster-class rule (DD-038-9, disclosed
operationalisation).** No separate recorded
rule assigning positional classes to clusters
has been located: the CGSA pipeline's own
cluster report lists members only, and
`sign_clusters.json` carries no class labels.
The class of a cluster under this design is
therefore fixed by stated operationalisation,
not assumed: **a cluster's class is the class
recorded for that cluster in
`reports/cluster_characterization.md`** — the
Phase 5 characterisation generated the day
the prediction was registered, whose per-cluster
classes are the very ones the register's
Tested note used (Cluster 21 TERMINAL, Cluster
39 TERMINAL, Cluster 10 INITIAL). The rule is
deterministic (a lookup in a named, hashed
record), it is the recorded test's own usage,
and it invents no threshold. If an enumerated
sign's cluster has no class recorded there,
that sign counts as **unassigned** under the
coverage rule (§6) — its class is never
inferred from rates at execution.

Sanity anchor, fixed at draft: the recorded
output must reproduce the register's three
named assignments — P385 → Cluster 21
(TERMINAL), P378 → Cluster 39 (TERMINAL),
P098 → Cluster 10 (INITIAL). If it does not,
the output in hand is not the output the
registered test named, and the study closes as
CANNOT BE RUN AS WRITTEN.

### The step-0 record

The outcome of every check — the table
selected and its hash, the provenance finding,
the full enumeration and population size, the
completeness reconciliation, the Phase 5
output verification — is written as a step-0
record and hashed before any scoring begins
(the house pattern). If a check closes the
study, that record is the outcome, reported as
a closure, not a verdict (§6) — with the one
exception of the census branch (§6), which is
a completion whose finding is the census
itself.

## 4. Data

- **Function codes (the population side).**
  The primary source and cross-check named at
  §3 check 0.1
  (`reports/indus_cgsa_cluster_analysis.json`
  `data.a[].icit_function`; cross-check
  `data/crosswalks/canonical_sign_registry.csv`).
  At draft, both sources' existence and shape
  were verified (§0.3; `adjudication.md` §2);
  neither was read for its ITM membership, and
  the population was not enumerated.
- **Cluster assignments (the scoring side).**
  The recorded CGSA Phase 5 output only:
  `outputs/analysis/sign_clusters.json`
  (assignment) and
  `reports/cluster_characterization.md`
  (cluster classes, per DD-038-9). Nothing is
  re-clustered, re-characterised, or
  re-derived.
- **The register.** `docs/PREDICTION_REGISTER.md`
  §3 (PRED-2026-007 entry) and its §6 append
  discipline (§7 below).

Rights posture: all sources are the programme's
own held record; the study publishes the
per-sign table and statistics, as the design
prescribes.

## 5. Method

Exactly the registered computation, nothing
added. For every sign in the enumerated
population (§2, §3 check 0.2), take its cluster
assignment from the recorded Phase 5 output
(§3 check 0.3). A sign **counts as TERMINAL**
if and only if its recorded cluster's class —
under the DD-038-9 operationalisation, the
class recorded for that cluster in
`reports/cluster_characterization.md` — is
TERMINAL (DD-038-3: the criterion's "TERMINAL
or cluster in TERMINAL clusters" is carried
verbatim in §0.1; the design's reading — count
TERMINAL-cluster memberships — is the operative
one, and any held record that assigns a sign a
class differing from its cluster's recorded
class is reported in the outcome, not resolved
by discretion). Count the TERMINAL signs;
divide under the coverage rule (§6); compare
to 70%.

One descriptive addition is pre-registered here
so it cannot be mistaken for a criterion: the
**per-sign table** — every enumerated ITM sign,
its cluster, its cluster's class (or "no
recorded Phase 5 assignment") — is published
with the outcome, so no reader has to trust a
bare percentage over a possibly small
population. The table is descriptive only; it
carries no criterion and moves no verdict.

## 6. Criteria and verdict mapping

These are the register's criteria, not this
spec's. **The verdict rule, stated
mechanically:** the share is the number of
enumerated ITM signs that count as TERMINAL
under §5, divided by the denominator the
coverage rule below fixes (the enumerated
population, or the assigned population where
the coverage rule applies), compared against
the 70% bar. Nothing else enters the verdict —
not the register's recorded 67%, not the
sample's history, not any expectation written
anywhere, including in this draft.

- **CONFIRMED** — the share is at least 70%.
- **NOT CONFIRMED** — the share is below 70%.

There is no inconclusive band in the registered
criterion, and this spec does not invent one.

**Coverage rule (the design's, fixed in
advance — DD-038-4).** If some enumerated ITM
signs have no recorded Phase 5 assignment, the
share is computed on the **assigned population**
and the coverage is stated in the verdict's
first sentence — *unless* the unassigned signs
cannot change the outcome arithmetically (the
bar already reached even if all unassigned are
non-TERMINAL, or unreachable even if all are
TERMINAL), in which case the verdict is
decisive and coverage is still stated. If
coverage is below 80% and the outcome is not
arithmetically decisive, the appended register
entry records the test as **run-at-partial-scope**
with the numbers, and the register's
PARTIALLY CONFIRMED wording is replaced by that
precise statement — by append, never by edit
(§7).

**Census branch (the design's honest shrink).**
If the enumerated population is exactly the
ITM signs the recorded partial test already
checked, the design closes with the census as
its finding: the registered test then *has*
been run at full scope. That is a **completion,
not a failure**, and it is scored by the same
mechanical verdict rule above — the appended
entry records whatever share that rule yields
over the enumerated population and the recorded
assignments, and supersedes the PARTIALLY
CONFIRMED wording by append (§7). This draft
pre-writes no outcome for this branch
(DD-038-1): the register's 67% figure does not
carry into it, because that figure's
denominator mixed in a non-ITM sign (§0.2),
and the design text's anticipated "2 of 3" is
recorded as the design's expectation, not as a
rule — the mechanical rule governs.

**Step-0 closures.** A closure under §3
(**CANNOT BE RUN AS WRITTEN**) is reported as
itself, never as a verdict: PRED-2026-007 would
remain unscored by this execution, and the
register's §4 (Failed Predictions) gains no
entry from a closure.

## 7. Register handling at execution

The outcome, whatever it is, is appended to
`docs/PREDICTION_REGISTER.md` as a dated entry
under §6 (insertions only), under the owner's
execution order, and the Phase D register-hash
pin is advanced by name for that authorised
change.

- On a **verdict** (CONFIRMED / NOT CONFIRMED,
  including a decisive verdict under partial
  coverage), the §3 entry's Tested/Outcome
  fields for PRED-2026-007 are updated **in the
  same append's terms** — by the dated §6 entry
  recording the supersession; the §3 text as
  registered is never edited in place, and the
  PARTIALLY CONFIRMED wording stands in the
  record as the pre-execution record it is,
  superseded by the appended entry.
- On a **run-at-partial-scope** record (coverage
  rule, §6), the appended entry replaces the
  PARTIALLY CONFIRMED wording with the precise
  partial-scope statement, as the design
  prescribes.
- On the **census branch**, the appended entry
  records the census, the full-scope outcome
  under the mechanical verdict rule (DD-038-1),
  and the supersession.
- On a **step-0 closure**, the §3 Outcome stays
  **PARTIALLY CONFIRMED** as the pre-execution
  record — the Spec 035 precedent (F035-C15)
  applied to a closure: a closure is not a
  verdict, and the register does not record it
  as one.
- The **provenance reconciliation note** (§3,
  check 0.1) is appended as its own dated entry
  in the same execution act.

Every other prediction's entry stays
byte-identical. This draft changes no register
text, no other prediction's state, and no Spec
026–037 record.

## 8. Controls and named confounders

- **Clustering stability, answered by fidelity,
  not repair.** Cluster membership is asked to
  carry weight while the programme's
  cross-compilation work shows sign treatment
  is contested. The registered test named this
  clustering, so this clustering is what gets
  scored; the caveat rides in the appended
  entry and in every outcome statement. The
  instability is not repaired, averaged over,
  or re-run away (§3, check 0.3).
- **Small-population arithmetic.** If the
  population is in the single digits, each sign
  is worth double-digit percentage points. The
  per-sign table (§5) is published so the
  arithmetic is visible; no outcome statement
  may present the percentage without the
  population size in the same paragraph.
- **The provenance tangle is named, not
  smoothed.** The register's "from mayig
  features" line does not describe the held
  files (§0.3). Step 0 records what the code
  table actually is; the reconciliation is an
  append (DD-038-2). No outcome statement may
  repeat the register's provenance line as if
  it were verified.
- **Table-shopping is the failure mode this
  design exists to prevent.** More than one
  held source records function codes. The
  primary source, the cross-check, and the
  conflict rule are named before any source is
  read for ITM membership (§3, check 0.1), so
  no later preference among tables can move
  the population (DD-038-5).
- **The recorded partial test is not evidence
  about the population.** That the two named
  ITM signs landed TERMINAL says nothing about
  the signs never checked; no outcome statement
  may present the sample's 2-of-2 (or the
  register's 2/3) as a prior estimate of the
  full-population share.

## 9. What this design would move, and what it would not establish

**What it would move.** PRED-2026-007 from a
partial check on three named signs to a scored
result at full enumerated scope — the first
time since April 2026 that its register entry
would rest on its own test — or to the census
finding that the population never exceeded the
sample (a completion that scores the test at
the scope it always had), or to a precise
statement of why its scope cannot be enlarged
(a step-0 closure, or a run-at-partial-scope
record). Each ending replaces an
acceptance-flavoured label with the arithmetic
that actually supports it.

**What it would NOT establish.** That ITM signs
*mean* anything terminal, or that the Phase 5
clustering carves the script at its joints. It
scores one registered prediction about one
coding scheme inside one clustering — no more,
and the appended entry will say no more.

## 10. Execution shape (Phase-401, provisional — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, then run.
2. **Step 0** (§3): table location and
   provenance; enumeration with its completeness
   checks; Phase 5 output verification — in that
   order, fail-closed, with the step-0 record
   written and hashed before any scoring. A
   step-0 failure closes the study as recorded
   in §3, and the closure is the outcome — except
   the census branch (§6), which completes.
3. **Scoring** (§5): the registered computation
   only; the per-sign table produced with it.
4. **Outcome:** the verdict under §6, the census
   completion, the partial-scope record, or the
   closure — appended to the PRED register as a
   dated entry (§7), recorded in this spec's
   directory and the root LEDGER; the foundation
   check (H21) run after the claim consequence
   lands; nothing written into any frozen
   record.

## 11. What this spec does not do

- It does not execute anything. Execution
  (Phase-401, provisional) follows the owner's
  freeze order for this contract and a separate
  execution order.
- **It does not enumerate the population.** No
  held source was read for ITM membership at
  this draft; no sign beyond the register's
  three named signs was looked up in the Phase
  5 output; no share was computed.
- It does not re-run, re-derive, or substitute
  any clustering (§3, check 0.3), adjust the
  70% bar, add a band, or substitute a
  different test (§§5–6).
- It does not edit the PRED register — the
  reconciliation note and every outcome record
  are execution-time appends (§7).
- It files no OSF registration at draft.
  PRED-2026-007 predates the programme's OSF
  registration practice and carries no
  preregistration of its own; whether the
  frozen spec files its own OSF contract
  registration (the Spec 032–036 pattern) is a
  freeze-time decision, recorded as DD-038-6.
- It does not silently harmonise the design and
  the register where they disagree: every
  disagreement found is flagged in
  `adjudication.md` as a DD proposal (§13).

## 12. Governed claims (summary)

The governed register is `claims.json`
(F038-C01…C14):

- **C01** — a verdict under this spec states
  whether the registered criterion for
  PRED-2026-007 is met over the enumerated
  population, and nothing beyond that statement.
- **C02** — the success criterion is the
  registered one, carried verbatim: at least
  70% of ITM-coded signs are TERMINAL or cluster
  in TERMINAL clusters; CONFIRMED at 70% or
  above, NOT CONFIRMED below, no band added.
- **C03** — the population is every distinct
  sign whose function code in the primary
  source named at check 0.1 is exactly ITM —
  no sample, no frequency threshold; P098 (LOG)
  is excluded by rule; the cross-check and
  conflict rule are fixed before enumeration.
- **C04** — step 0 runs in a fixed order,
  fail-closed: sources and provenance,
  enumeration with completeness checks, Phase 5
  output verification; failure closes the study
  as CANNOT BE RUN AS WRITTEN, unscored.
- **C05** — the provenance reconciliation is an
  appended dated note; the register text itself
  is never edited.
- **C06** — scoring reads the recorded CGSA
  Phase 5 output only; a cluster's class is the
  class recorded for it in the Phase 5
  characterisation (DD-038-9); no re-clustering
  is run, and if the output does not survive in
  sign-assignable form the study closes as
  CANNOT BE RUN AS WRITTEN.
- **C07** — the coverage rule is the design's,
  fixed in advance: assigned-population
  denominator, coverage in the verdict's first
  sentence, the arithmetic-decisiveness
  exception, and the partial-scope record below
  80% coverage.
- **C08** — if the enumerated population is
  exactly the ITM signs already tested, the
  design closes with the census as its finding
  — a completion, scored at full scope by the
  mechanical verdict rule; no outcome for this
  branch is pre-written anywhere (DD-038-1).
- **C09** — the per-sign table is published with
  the outcome as a descriptive record; it
  carries no criterion.
- **C10** — the outcome is appended to the
  prediction register as a dated entry
  superseding the PARTIALLY CONFIRMED wording;
  the registered §3 text is never edited and
  every other entry stays byte-identical.
- **C11** — every outcome statement carries the
  clustering-stability caveat: fidelity to the
  named clustering, not repair of it.
- **C12** — no outcome under this spec
  establishes that ITM signs mean anything
  terminal, or that the Phase 5 clustering
  carves the script at its joints.
- **C13** — this draft enumerates nothing,
  scores nothing, and executes nothing; the
  population's membership and size are
  execution-time facts that do not exist yet.
- **C14** — step-0 closures are reported as
  themselves, never as verdicts; a closure is
  not a refutation, and the census completion
  is not a closure.

## 13. Design decisions

- **DD-038-1 — DISPOSED at draft: the verdict
  rule is mechanical; no pre-written outcome.**
  The register's Tested note reports 2/3 over
  two named ITM signs and one named LOG sign;
  the registered criterion ranges over ITM-coded
  signs only; D-31's step-0 prose anticipates
  "its outcome is 2 of 3" for the census
  closure while its controls exclude P098 from
  the count. Disposition (§§0.2, 6): the
  register's 67% is a pre-execution record whose
  denominator mixed in a non-ITM sign; the
  spec's verdict rule is stated mechanically
  (share over the enumerated ITM population
  against the 70% bar, under the coverage
  rule), and **no branch of this design carries
  a pre-written outcome** — the census branch
  included. The design text's anticipation is
  recorded as an expectation, not a rule. Full
  disposition in `adjudication.md` §3.
- **DD-038-2 — The provenance reconciliation is
  an append, never an edit.** The register's
  "from mayig features" line conflicts with the
  held files (the mayig feature files carry no
  function codes; the parser reads the codes
  from a Wells-derived text). Step 0 appends a
  dated reconciliation note recording what the
  authoritative table actually is (D-31's
  prescription, carried).
- **DD-038-3 — The criterion's wording governs
  over the Prediction sentence's.** "Cluster
  into TERMINAL class" (Prediction) vs "TERMINAL
  or cluster in TERMINAL clusters" (Success
  criterion): the criterion is carried verbatim
  (§0.1) and the operative reading is the
  design's — a sign counts iff its recorded
  cluster's recorded class is TERMINAL (§5).
  The difference is flagged here, not smoothed
  over.
- **DD-038-4 — The coverage rule is a design
  addition, adopted as the design wrote it.**
  The register specifies no denominator for
  unassigned signs; D-31's rule (assigned
  population, stated coverage, decisiveness
  exception, 80% floor with a partial-scope
  record) is adopted verbatim (§6) and flagged
  as the design's, not the register's.
- **DD-038-5 — DISPOSED at draft: primary,
  cross-check, conflict rule named before
  enumeration.** Neither the register nor the
  design named the authoritative table. This
  draft names them (§3, check 0.1): primary =
  `reports/indus_cgsa_cluster_analysis.json`
  `data.a[].icit_function`; cross-check =
  `data/crosswalks/canonical_sign_registry.csv`
  `icit_function`; provenance lineage =
  `fuls_parser.py`'s Wells-derived catalog
  reading. Conflict rule: the primary governs
  membership; every cross-check disagreement
  is recorded sign-by-sign and published;
  ambiguity or internal conflict **within**
  the primary closes the study as CANNOT BE
  RUN AS WRITTEN. No union, no intersection,
  no tie-breaking third source. Full
  disposition in `adjudication.md` §3.
- **DD-038-6 — OPEN PROPOSAL: a spec-level OSF
  registration, decided at freeze.** Specs
  032–036 each filed (or, for 036, propose to
  file) their own OSF contract registration at
  freeze. PRED-2026-007 itself was registered
  in April 2026, before that practice, and has
  no preregistration of its own. **Proposal to
  the freeze decision: file the frozen spec's
  own OSF contract registration**, following the
  house pattern. This draft files nothing.
- **DD-038-7 — The freeze gate runs under aee
  1.5.0.** Adoption of aee 1.5.0 is in flight at
  this draft (the Spec 036 draft still records
  the `>=1.0.4,<1.5` pin of PR #181). This
  draft runs **no** AEE hooks; at the freeze
  act the lifecycle hooks (after_specify /
  after_plan / after_tasks) run as the gate
  under aee 1.5.0, and the freeze digest is
  computed over the recovered register exactly
  once, at freeze (`aee/freeze-aee-note.md`).
  The digest in `freeze.json` at this draft is
  a draft digest over this draft contract and
  decides nothing.
- **DD-038-8 — The execution phase number is
  provisional.** Phase-400 is reserved by Spec
  036; this draft provisionally reserves
  **Phase-401** for Spec 038's execution. The
  assignment is confirmed at the freeze act
  against any reservation the Spec 037 draft
  makes; nothing in the design turns on the
  number.
- **DD-038-9 — DISPOSED at draft: the
  cluster-class rule is a disclosed
  operationalisation.** No recorded rule
  assigning positional classes to clusters has
  been located: the CGSA pipeline's cluster
  report lists members only, and
  `sign_clusters.json` carries no class labels.
  Rather than assume a rule silently — a
  freeze-blocking defect — this draft states
  the operationalisation openly (§3, check
  0.3): a cluster's class is the class recorded
  for that cluster in
  `reports/cluster_characterization.md`, the
  Phase 5 characterisation generated on the
  registration day and the source of the very
  class labels the register's Tested note used.
  The rule is a deterministic lookup in a named
  record; it invents no threshold and derives
  no class from rates at execution; a cluster
  with no recorded class leaves its signs
  unassigned under the coverage rule. Full
  disposition in `adjudication.md` §3.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
