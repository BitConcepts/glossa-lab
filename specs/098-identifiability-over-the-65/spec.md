# Spec 098 — Identifiability Over the 65: A Locked Out-of-Sample Predictive Comparison

**Status: ADOPTED AND FROZEN 2026-11-21** (owner's directive
2026-11-21: execute all recommendations of the independent
Co-scientist audit of the 94 strict-core readings; this package
executes Q5 item 2 of that audit). The study design in section 3
and the freeze record
(`records/freeze-v1-2026-11-21.md`) are frozen as of this
package's landing. Execution (Stages 1–4 of `tasks.md`) runs
under the freeze; any change to a frozen parameter is a new
freeze version, recorded, never a silent edit.

**Provenance.** The audit's findings are filed at
`specs/095-red-team-remediation/`'s companion audit record and
were delivered to the program 2026-11-21
(`coscientist-audit-94-findings-2026-11-21.md`, Q2 and §5
item 2). Its operative sentences, which this spec implements
verbatim in substance: "Freeze sign identities/allographs,
reading variants, grammatical assumptions, dictionary-search
space, and decision rules before revealing independent test
inscriptions. Compare competing Dravidian assignments and
plausible alternative structural/language models, with
penalties or controls for selection, reuse, and flexibility.
Require predictions that would differ under the alternatives;
success on language-neutral position alone is insufficient.
Rerun identifiability for the six E against stronger
alternatives and extend it to the 65 I."

The identifiability protocol this study operationalizes is
Standards of Record, Part III (`glossa-indus/STANDARDS.md`),
first applied in Spec 095 Stage 3
(`specs/095-red-team-remediation/records/t303-identifiability-application-2026-11-16.md`):
all six externally credited readings returned NOT IDENTIFIABLE
under desk rival construction. This study replaces desk
construction with a locked predictive test: rivals must beat
or match the candidate on inscriptions the scoring path has
never seen, under decision rules fixed here.

## 1. What this spec is

A single study with two arms over one frozen population:

- **Arm I (primary).** The 65 readings the audit relabels
  **I — internally motivated candidates, identifiability
  untested** (population annex,
  `records/population-annex-2026-11-21.md`). Each candidate
  value, frozen exactly as recorded, faces serious rival
  constructions in a genuinely out-of-sample predictive
  comparison on sealed held-out inscriptions.
- **Arm E (secondary).** The six externally credited readings
  (M044, M047, M124, M202, M329, M330), rerun under the same
  machinery against **stronger** alternatives than the desk
  exercise of record used — including cross-sign rivals
  (M202 against M330 and the reverse), shared-comparanda
  rivals (M044 against M124), and the logogram rival for
  every sign. The design supports this arm because the
  population annex, the prediction-sheet template, and the
  scoring path are identical for both arms; excluding it
  would discard machinery already built. Its outcomes
  restate identifiability only, under Part III rule 5.

The study reports, per sign, exactly one outcome from the
frozen vocabulary of section 4. It changes no standing, no
anchor, and no other program record (claim C098-7).

## 2. The grounding, as measured at freeze time

Measured on tower-compute 2026-11-21 from the corpus of
record (section 3.2), by direct count, not by citation:

- The corpus export carries 15,508 records; 3,033 carry a
  non-empty canonical grapheme sequence (13,642 tokens in
  the export overall; the sequence-bearing subset is the
  study's sampling frame).
- 69 of the 71 population signs are attested in the
  grapheme field, for 2,955 population-sign tokens in total.
  **M044 and M374 are not attested in that field** — a named
  gap (freeze §7): Stage 1 must resolve their sequences from
  the diplomatic text codes under the frozen crosswalk, or
  both signs default to UNDECIDABLE AT THIS POWER without
  scoring.
- Under the frozen split rule (freeze §3), the held-out side
  holds 640 sequence-bearing records and 623 population-sign
  tokens; only 19 of 71 signs reach the frozen minimum of 5
  held-out tokens. The study is therefore expected, on the
  record as it stands, to return UNDECIDABLE AT THIS POWER
  for a majority of signs. That is a finding about power,
  stated in advance so it cannot be mistaken for a result
  manufactured after the fact.

## 3. The frozen design

The full frozen parameter set is the freeze record; this
section states the design it freezes.

### 3.1 Population and candidate values

The 71 signs and their candidate values exactly as recorded
in the audit's appendix (population annex). Reading variants
are frozen as written: an unresolved variant (for example
M051 pū/puḷ, M089 tu/tū, M099 kol/koḷ, M391 ka/kaṇ) is scored
as the recorded disjunction, and the flexibility penalty of
section 3.5 is charged for each alternation. No variant may
be resolved, split, or respelled after the freeze.

### 3.2 Corpus of record and sign identity

- Corpus: primary corpus V1,
  `glossa-corpus/indus/exports/indus_research.jsonl`, at
  repository commit `66fcf22f191a10f2073a8309f451121b1f009f03`,
  SHA-256
  `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`
  (computed at freeze time on tower-compute).
- Sign identity: the Mahadevan numbers of the population
  annex, mapped to corpus graphemes through the crosswalk of
  record (`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json`
  at the same commit). Allograph and variant handling is the
  crosswalk's, frozen: no post-freeze merges, splits, or
  reassignments of graphemes to signs.
- Deduplication (reuse control): records whose normalized
  diplomatic text codes are identical form one inscription
  cluster; the cluster is the split unit, and every copy of a
  cluster sits on the same side of the split. Deduplication
  runs before the split, under the normalization of record.

### 3.3 The held-out set and its seal

- Split rule (frozen): a cluster belongs to the held-out set
  if and only if
  `int(SHA-256("098-split-v1:" + cluster_id)) mod 5 == 0`
  (a 20 percent held-out share), where `cluster_id` is the
  cluster's lowest `glossa_id` under the deduplication of
  §3.2.
- Seal mechanism (frozen, following the hash-pinned freeze
  practice of Specs 093/097): Stage 1 generates the held-out
  cluster list on tower-compute, publishes **only** its
  SHA-256 (over the sorted cluster ids, one per line) and its
  count in a seal record committed before any scoring-path
  code runs, and holds the list itself in custody outside
  the repository (the Spec 097 custody pattern). The scoring
  path receives development data only; the held-out list is
  released to it exactly once, at scoring, and the release is
  recorded. A seal whose hash does not recompute at scoring
  time voids the run (outcome: SEAL FAILURE, no per-sign
  outcomes).
- **The contamination gap, named and capped.** The 65
  candidate readings were historically derived using the
  program's full corpus; no in-corpus split is pristine
  against that derivation, and this freeze does not pretend
  otherwise. Two consequences are frozen. (a) The in-corpus
  held-out arm is designated **pseudo-held-out**: a pass on
  it yields at most DISCRIMINATED ON PSEUDO-HELD-OUT, a
  reportable discrimination result that supports no standing
  change and no identification claim beyond the corpus.
  (b) Stage 1 runs a provenance audit: any sequence-bearing
  source in the corpus of record that is documented as
  acquired after the latest candidate-assignment date in the
  population annex, or otherwise demonstrably absent from
  every candidate-generation input, forms the **genuine
  holdout subset**; signs with at least 5 tokens in that
  subset are scored on it as the primary arm, and only a
  pass there can yield IDENTIFIABLE ON HELD-OUT. If no such
  subset exists, that fact is recorded and Arm I's ceiling
  is the pseudo-held-out outcome. The study was **not run**
  in this adoption round for exactly this reason: the seal
  cannot be honestly struck until the Stage 1 provenance
  audit and the M044/M374 gap are resolved on the record.

### 3.4 The rivals (serious alternatives, frozen)

For every sign, the rival set is constructed on development
data only, under WP8 fairness conditions (matched tuning
budget, matched available evidence), from the WP8 control
families of Standards Part III rule 2:

- **R-A, matched wrong Dravidian value (C2/C5).** A Dravidian
  value of the same syllable shape, frequency- and
  position-matched to the candidate, drawn from the frozen
  dictionary-search space (§3.6).
- **R-B, unrelated-family value (C5).** A value drawn from a
  named unrelated family available in the repository's
  lexica of record (Indo-Aryan/Sanskrit comparanda; Munda
  where the lexica carry it), same shape constraints.
- **R-C, logogram rival (C1/C3).** The sign carries the
  candidate's gloss (or, for Arm E, the depicted object) as a
  logogram with no phonetic value.
- **R-D, structural-only model (C6-adjacent baseline).** A
  language-neutral positional/bigram model with no value
  assignment at all. Beating R-D is necessary and **not
  sufficient**: success against R-D alone is success on
  language-neutral position, which the audit expressly rules
  insufficient.
- **R-E, global permutation (C1/C2, model level).** The
  whole candidate assignment set with values permuted among
  same-shape signs, scored as one model. This is the
  alternative structural/language-model arm: it tests
  whether the assignment *system*, not any single value,
  predicts held-out material better than a matched system
  that assigns the same values to the wrong signs.
- **Arm E additions.** Cross-sign rivals (each of M202/M330
  scored under the other's evidence package; M044 under
  M124's comparanda and the reverse) and the comparandum
  itself read as the value (the T303 rivals, now scored
  predictively instead of argued at a desk).

### 3.5 Predictions, scoring, and penalties

- **Prediction sheets (value-relevance gate).** Before the
  seal is opened, each sign gets a prediction sheet naming,
  for the candidate and for each rival, at least one
  observable on held-out data on which their predictions
  **differ in a value-relevant dimension**: the identity or
  class of neighbouring signs predicted by the value's
  grammatical role, motif/context associations that
  distinguish competing words for the same referent (for
  example M006 puli against M080 vēṅkai), or collocations
  that a logogram rival and a phonetic rival predict
  differently. A sheet whose only differing observable is
  position or frequency is rejected at review, before
  unsealing. A sign with no accepted sheet is recorded
  NOT IDENTIFIABLE by construction — the protocol's rule,
  applied prospectively.
- **Score.** Per sign, the held-out log-likelihood of the
  sign's held-out contexts under a value-conditioned context
  model built on development data only (model class, order,
  and smoothing fixed in the freeze), for the candidate and
  for each rival; the sign's margin is the candidate's score
  minus the best rival's score.
- **Flexibility penalties (frozen).** Each free choice the
  candidate's derivation uses — each unresolved variant
  alternation, each homophony allowance (the same value on
  two population signs, as with M002/M020, M053/M054,
  M018/M069, M026/M015-class pairs), each gloss alternation —
  charges 2 nats against the candidate's margin. Rivals are
  charged identically for the free choices they use.
- **Selection and reuse controls (frozen).** The dictionary-
  search space is closed at the freeze (§3.6); no candidate
  or rival may be revised after any held-out observation;
  the permutation null (B = 999, seed 9801, frozen) is built
  from development data; every scoring attempt is indexed
  (Spec 089 run-scoped discipline), failures included; the
  held-out set is opened once.

### 3.6 Dictionary-search space (frozen)

The DEDR entries cited in the population annex, and the
repository lexica of record at the pinned commit
(`glossa-corpus/lexica/` and the `backend/glossa_lab/data/`
lexicon modules named in the freeze). No entry outside that
space may generate a candidate or a rival. Grammatical
assumptions are those of the annex rows as recorded (the
program's Dravidian slot grammar as filed); no new
grammatical role may be introduced for any sign after the
freeze.

## 4. Decision rules and outcome vocabulary (frozen)

Per sign, in this precedence order:

1. **UNDECIDABLE AT THIS POWER** — held-out tokens for the
   sign number fewer than 5, or the Stage 1 power grid shows
   the minimum detectable margin at the sign's held-out count
   exceeds the identification bar, or (M044/M374) the sign's
   sequences could not be resolved under §3.2.
2. **NOT IDENTIFIABLE** — no accepted prediction sheet; or
   the penalized margin over the best rival is below
   **10 nats**; or the margin does not exceed the 99th
   percentile of the frozen permutation null. (A rival
   fitting comparably is exactly this outcome, per Part III
   rule 4.)
3. **IDENTIFIABLE ON HELD-OUT** (genuine-holdout subset
   only) or **DISCRIMINATED ON PSEUDO-HELD-OUT** (in-corpus
   arm) — the penalized margin is at least 10 nats, exceeds
   the null's 99th percentile, the prediction sheet's
   value-relevant predictions are borne out, and the
   candidate also beats the structural-only rival R-D (a
   necessary, not sufficient, condition).

Family-level reporting is counts of per-sign outcomes only.
No outcome moves any standing (C098-7); a future standing
act is a separate program act on this study's outcome
record, not part of this study. Statistical reporting
follows Standards Part II: every margin is reported with its
effect size, an inscription-cluster bootstrap interval
(B and seed in the freeze), its multiplicity family (the 71
signs), and its precision basis.

**The falsifier of the study's premise.** The premise (the
frozen machinery can discriminate at least some candidates
from serious rivals out of sample) is falsified if, on the
genuine-holdout subset or the pseudo-held-out arm, **no**
sign reaches its arm's pass outcome while the planted-
discrimination fixture of TC-098-02 passes — the machinery
demonstrably can discriminate where discrimination exists,
so a uniform failure is a property of the candidates, not
of the test. The outcome record states this verdict
explicitly either way.

## 5. Decisions

- **D-098-1 (number).** At the check of 2026-11-21 the
  highest landed package on origin/main was 097 and no 098
  directory, branch, or open pull request existed; this
  package takes 098. If a parallel package lands 098 first,
  this package renumbers under the Spec 097 precedent rather
  than colliding.
- **D-098-2 (no run in the adoption round).** The study is
  designed and frozen here; it is not executed in this
  round, because the seal cannot be honestly struck until
  Stage 1 resolves the provenance audit (genuine-holdout
  subset) and the M044/M374 grapheme gap on the record
  (§3.3). Running on the in-corpus split alone and calling
  it out-of-sample would repeat, in new dress, the reuse
  defect the audit charged.
- **D-098-3 (registration performed in full, Spec 097
  pattern).** The claims are intaken into the canonical
  ledger in this package's own landing pull request through
  the bundle-import route (C098-1..C098-8 appended,
  2026-11-21), with the taxonomy entry added, the settling
  chain refreshed in the standing order, the generated layers
  regenerated, and every census pin the intake moves updated
  in the same pull request — the registration the program's
  conformance machinery requires of any new spec package, as
  Specs 096/097 performed it. The full account is in
  `records/adoption-and-registration-2026-11-21.md`.
- **D-098-4 (venue).** All execution runs on tower-compute,
  in a fresh clone under `~/glossa-work/`, never in the
  coordination VM and never on the mini-server (which serves
  only). Every run's verdict is its payload verdict (the
  run's own verdict record), never a wrapper state.

## 6. Test cases

Two test cases exercise this package's requirements for
real; both are implemented in `tests/` against the reference
implementation of the frozen seal and decision rules in
`tools/seal_and_score.py`, and both were executed on
tower-compute at adoption with their payload verdicts
recorded in `records/tc-execution-2026-11-21.md`.

- **TC-098-01 — Seal and split integrity.** On a fixture
  corpus: the split is deterministic under the frozen rule;
  the seal hash recomputes from the held-out list and fails
  on a tampered list; the development export contains zero
  held-out cluster ids; the scoring path refuses a
  development input that contains a held-out id.
- **TC-098-02 — Decision-rule behaviour on planted cases.**
  On a fixture with three planted signs — one discriminable
  (candidate and rival predict different held-out contexts,
  margin above the bar), one observationally equivalent
  (margin near zero), one below the minimum held-out count —
  the scorer returns the pass outcome, NOT IDENTIFIABLE, and
  UNDECIDABLE AT THIS POWER respectively, with the
  flexibility penalty applied to a variant-carrying fourth
  case changing its outcome at the bar.
