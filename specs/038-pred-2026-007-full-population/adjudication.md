# Spec 038 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-20
>
> This spec has two adjudication inputs, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's draft order of 2026-10-20**:
>    D-31 will be frozen for execution; this step
>    drafts its spec only (Spec 038, the next free
>    number after Spec 036 and the Spec 037 CISI
>    concordance draft). That order is the
>    adjudicating act for this **draft**. The
>    freeze and any execution are separate owner
>    decisions, and this draft performs neither.
>    The population is **not** enumerated by this
>    draft — enumeration is execution work.
> 2. **The freeze coordinator's Stage-0
>    preparation flags of 2026-10-20**
>    (`~/workspace/glossa-run/d31-freeze/PREP.md`):
>    three design-integrity flags the draft must
>    dispose of explicitly. §3 below disposes of
>    each, one by one; the freeze will be judged
>    against them.

## 1. The adopted basis (operative substance)

The registered test, carried into `spec.md`
without deviation:

- **Prediction.** Signs with ICIT function code
  ITM will cluster into TERMINAL class in CGSA
  Phase 5 at rate ≥ 70% (PRED-2026-007, H4:
  ICIT Function Alignment, registered
  2026-04-22).
- **Success criterion (verbatim).** "≥ 70% of
  ITM-coded signs are TERMINAL or cluster in
  TERMINAL clusters."
- **Recorded partial test.** P385 (ITM) Cluster
  21 TERMINAL; P378 (ITM) Cluster 39 TERMINAL;
  P098 (LOG) Cluster 10 INITIAL; recorded rate
  "2/3 ITM in TERMINAL (67%)"; outcome
  PARTIALLY CONFIRMED. A pre-execution record
  on three named signs — the total number of
  ITM-coded signs has never been recorded.
- **Population.** Every distinct sign the
  primary function-code source codes exactly
  ITM (`spec.md` §2; sources at §3 check 0.1).
  P098 (LOG) is excluded by rule.
- **Scoring.** Recorded CGSA Phase 5 output
  only; no re-clustering. Cluster classes per
  DD-038-9.
- **Verdict rule (mechanical).** Share of
  TERMINAL-counting signs over the denominator
  the coverage rule fixes, against 70%:
  CONFIRMED at or above, NOT CONFIRMED below.
  No band. No pre-written outcome anywhere.
- **Coverage rule.** The design's, verbatim in
  substance (`spec.md` §6).
- **Census branch.** If the enumerated
  population is exactly the ITM signs already
  tested, the design closes with the census as
  its finding — a completion, scored by the
  mechanical rule.
- **Register handling.** Dated §6 appends only;
  the registered §3 text is never edited
  (`spec.md` §7).

## 2. Verification record at draft

Every fact this design rests on was verified
first-hand at drafting, 2026-10-20, against
the record on `main` (head `5e7f3cdb`, the
PRED-2026-011 registration-completion merge;
hash rerun for the outcome record:
`5e7f3cdbdf208bf65f58d2ea84366e064848a469`):

- **Register entry** — read in
  `docs/PREDICTION_REGISTER.md` §3
  (PRED-2026-007) and §6: prediction, withheld
  line, criterion, Tested note, Outcome — all
  as designed here. SHA-256 of the file as read:
  `425cf07b7532d4ef8baab7a81463502650b59ba54ea98f6ee34ee11e48ce8829`.
- **Design D-31** — read in full on PR #195's
  branch (`designs/035-open-questions` @
  `43f56191`),
  `docs/research/experiment-designs-2026-10-13/05-predictions.md`:
  step-0 enumeration and provenance, recorded
  output only, census closure, coverage rule,
  P098 exclusion, per-sign table, the
  would-not-establish boundary. All carried.
- **Primary function-code source** — verified
  by form only:
  `reports/indus_cgsa_cluster_analysis.json`
  holds `data.a` with 611 per-sign records
  whose keys include `sign_id`, `icit_function`,
  `start_rate`, `end_rate`, `internal_rate`,
  `mahadevan_ids`, `wells_ids`. The
  `icit_function` **values were not inspected**
  — reading them across signs would be the
  enumeration, which this draft does not do.
  SHA-256: `8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3`.
- **Cross-check source** — verified by form:
  `data/crosswalks/canonical_sign_registry.csv`
  header carries the `icit_function` column.
  Values not inspected for ITM membership.
  SHA-256: `228a4e138c7fdb9016dae50e24db8d96767620825da7959d30963b4dd0bcee035`.
- **Provenance lineage** —
  `backend/glossa_lab/data/fuls_parser.py`:
  the catalog parser reads function
  classification "(from Wells)" over the code
  list NUM, LON, SHN, TMK, ITM, LOG, SYL.
  SHA-256: `da873a2e724e574fc0c65747b33cf2ff2aecbb12402a201e669f34a2accaa1f9`.
- **Mayig features carry no function codes** —
  a feature file's fields are `id`,
  `description`, grapheme lists
  (`parpola_graphemes`, `wells_graphemes`,
  `mahadevan_graphemes`), and visual `features`
  — no function field. The design's count was
  396 feature files; the coordinator's contents
  census counts 397 entries in the directory;
  the exact census is execution work and the
  difference changes nothing in the design.
- **Recorded Phase 5 output survives** —
  `outputs/analysis/sign_clusters.json`:
  `best_k` 40, `sign_to_cluster` for 160 signs,
  40 populated cluster lists, `k_results` for
  k ∈ {40, 60, 80, 100}, and **no class
  labels** (see §3, Flag 2). It reproduces the
  register's three named assignments (P385 →
  21, P378 → 39, P098 → 10). SHA-256:
  `27ed99060f6f6d2e3332e070a74c9b43848c1c8cd0dfd2e6abab2f48f6fa55a1`. Corroborated by
  `reports/cgsa_validation_report.md`
  (generated 2026-04-22, the registration day:
  best k 40, largest cluster 12/160, entropy
  reduction 0.3204 — the same 0.3204 the output
  records). The design's "recorded output does
  not survive" closure branch is therefore
  expected to stay unused; it stays written in
  the spec, as a closure branch should.
- **Cluster classes** —
  `reports/cluster_characterization.md`
  (generated 2026-04-22T19:22:14Z; 40 clusters,
  160 P-signs): per-cluster recorded classes,
  including Cluster 21 — TERMINAL (member P385,
  ICIT functions ITM(1)), Cluster 39 — TERMINAL
  (member P378, ITM(1)), Cluster 10 — INITIAL
  (members P098, P217; ICIT functions LOG(1)).
  These are the class labels the register's
  Tested note used. SHA-256:
  `c83fc2e90386a7d349a48d00aee377316a71998f1a03df925a90c2b5c2e09aa97`.
- **Spec 029 audit record** — the adopted
  PRED-2026-007 explanation record states what
  remains not understood: the full ITM
  population's rate is not known, only three
  ITM-coded signs have been through the check,
  and the register does not record how many ITM
  signs exist in total. This design is the
  remedy that record names.
- **Not done at draft, by design** — no source
  was read for ITM membership; no population
  size exists anywhere in this package; no
  Phase 5 assignment was looked up for any sign
  beyond the register's three named signs; no
  share was computed; nothing was frozen or
  executed.

## 3. Disposition of the coordinator's three flags (2026-10-20)

### Flag 1 — Denominator arithmetic: DISPOSED

*The flag.* The register's Tested line counts
three checked signs — P385 (ITM, TERMINAL),
P378 (ITM, TERMINAL), P098 (LOG, INITIAL) — and
reports "2/3 ITM in TERMINAL (67%)". But P098
is LOG-coded, and the design's own P098 rule
puts the denominator = enumerated ITM signs
only. The design's step-0 prose anticipates the
census branch's outcome as "2 of 3", which
would freeze an outcome the criterion's
arithmetic does not produce.

*Disposition.* The spec states the verdict
rule mechanically (`spec.md` §6): the share is
the number of enumerated ITM signs counting as
TERMINAL, divided by the denominator the
coverage rule fixes, against the 70% bar. The
register's 67% figure is identified in the
spec, in so many words, as **a pre-execution
record whose denominator mixed in a non-ITM
sign** (`spec.md` §0.2), and it carries into no
branch. **No pre-written expected outcome
appears anywhere in this package** — not for
the census branch, not for any other: the
census branch completes and scores by the same
mechanical rule, and this package nowhere
states what its result will be (DD-038-1;
claims F038-C02, F038-C08, F038-C13).

### Flag 2 — Cluster-class rule provenance: DISPOSED

*The flag.* The criterion needs "TERMINAL
clusters", but no recorded rule assigning
positional classes to clusters has been
located: the CGSA pipeline's cluster report
lists members only, and
`outputs/analysis/sign_clusters.json` carries
no class labels. A silently assumed rule would
be a freeze-blocking defect.

*Disposition.* The draft does not assume a
rule. It discloses a stated, deterministic
operationalisation as **DD-038-9**: a
cluster's class is the class recorded for that
cluster in `reports/cluster_characterization.md`
— the Phase 5 characterisation generated on
the registration day (2026-04-22), whose
per-cluster classes are the very ones the
registered partial test used (Cluster 21
TERMINAL, Cluster 39 TERMINAL, Cluster 10
INITIAL — verified above). The rule is a
lookup in a named, hashed record; it invents
no threshold and derives no class from
positional rates at execution. A cluster with
no class recorded there leaves its enumerated
signs unassigned under the coverage rule —
their classes are never inferred. The
characterisation's own class labels are
recorded descriptors from the Phase 5 work;
this design takes them as fixed recorded data,
exactly as the registered test did, and says
so (`spec.md` §3 check 0.3; claim F038-C06).

### Flag 3 — Code-table provenance: DISPOSED

*The flag.* Two candidate authoritative
function-code sources exist —
`fuls_parser.py`'s Wells-derived catalog lines,
and the CGSA analysis record's per-sign
`icit_function` field — and they could disagree
per sign. The spec's step 0 must name the
primary source, the cross-check, and the
conflict rule before enumeration.

*Disposition.* Named in `spec.md` §3 check 0.1
and claim F038-C03, before any enumeration:

- **Primary:** `reports/indus_cgsa_cluster_analysis.json`,
  `data.a[].icit_function` (611 per-sign
  records — the recorded CGSA sign-level table
  carrying the field; verified by form at
  draft, values uninspected).
- **Cross-check:** `data/crosswalks/canonical_sign_registry.csv`,
  `icit_function` column.
- **Provenance lineage:** `fuls_parser.py`'s
  Wells-derived catalog reading — cited as the
  codes' lineage (the register's "from mayig
  features" line is false to the files and is
  reconciled by append, DD-038-2), not used as
  a third table.
- **Conflict rule:** the primary governs
  membership; every cross-check disagreement
  is written sign-by-sign into the step-0
  record and published with the outcome;
  ambiguity or internal conflict **within**
  the primary closes the study as CANNOT BE
  RUN AS WRITTEN. No union, no intersection, no
  tie-breaker consulted after the fact
  (DD-038-5).

## 4. Remaining disagreements flagged, not harmonised

Beyond the three flags, the draft records the
design/register differences it found, each as
a DD in `spec.md` §13:

- **DD-038-2** — the register's provenance line
  ("from mayig features") conflicts with the
  held files; reconciled by dated append at
  execution, never by editing the register.
- **DD-038-3** — the Prediction sentence
  ("cluster into TERMINAL class") vs the
  Success criterion ("TERMINAL or cluster in
  TERMINAL clusters"): the criterion is carried
  verbatim and governs; the difference is
  flagged, not smoothed.
- **DD-038-4** — the coverage rule is a design
  addition the register does not specify;
  adopted as the design wrote it, and labelled
  the design's.
- **DD-038-6 (open, for the freeze decision)**
  — whether the frozen spec files its own OSF
  contract registration (the Spec 032–036 house
  pattern). PRED-2026-007 predates the
  programme's OSF practice and has no
  preregistration of its own. Proposal: file
  one at freeze. This draft files nothing.
- **DD-038-7** — the freeze gate runs under
  **aee 1.5.0** (adoption in flight): the AEE
  lifecycle hooks have not run on this draft
  and are a freeze gate (`aee/freeze-aee-note.md`).
  Earlier drafts recorded the `>=1.0.4,<1.5` pin
  of PR #181; this draft records the 1.5.0
  freeze gate as instructed by the programme's
  current direction, and the digest at draft is
  computed with the environment
  `freeze.json` itself records.
- **DD-038-8** — the execution phase number
  (Phase-401) is provisional, to be confirmed
  at the freeze act against any reservation the
  Spec 037 draft makes; Phase-400 is Spec
  036's.

## 5. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), knowing: step
   0 enumerates a population whose size nobody
   currently knows; the verdict follows
   mechanically from that population and the
   recorded Phase 5 assignments; the census
   branch would complete the test at the scope
   it always had; a step-0 closure would leave
   PRED-2026-007 unscored with its PARTIALLY
   CONFIRMED wording standing as the
   pre-execution record. Or decline, leaving
   the prediction as it stands.
2. **DD-038-6 (proposal): whether the frozen
   spec files its own OSF contract
   registration.** Recommendation: yes — follow
   the house pattern of Specs 032–036.
3. The disposed readings stand as drafted
   unless the freeze overturns them openly:
   the mechanical verdict rule (DD-038-1), the
   primary / cross-check / conflict rule
   (DD-038-5), the cluster-class
   operationalisation (DD-038-9), the fixed
   step-0 order (DD via F038-C04), and the
   coverage rule as the design's own
   (DD-038-4). The criterion itself is
   registered text and is not among the
   decidable items.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
