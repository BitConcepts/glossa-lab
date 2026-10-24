# Spec 052 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign
>    plan, approved by the owner as written on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`).
>    Spec 052 is the plan's Part 2 **member 1**:
>    design D-01, arm A — Farmer's thesis that
>    the script is "not writing at all," with
>    its three restatement fragments; falsifier:
>    the frozen Phase-43 positional battery, run
>    on the held Soviet records, returns the
>    structure writing predicts; inputs: the
>    Soviet dataset (109 hand-verified records)
>    and the frozen Phase-43 battery. Decisions
>    E-1 to E-7 stand as written; **E-3** is
>    the one that binds this spec's scope:
>    trigger-armed arms do not auto-join.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    D-01 found **RIPE (arm A)** — the frozen
>    Phase-43 positional battery on the held
>    Soviet dataset (109 records, hand-verified
>    in Phases 120–124) is a complete, draftable
>    consistency test today; arm B stays blocked
>    inside the design on a genuinely independent
>    corpus, re-tested on 2026-10-20 when both
>    newly arrived candidate datasets closed as
>    ICIT-lineage on provenance.
> 3. **Design D-01** in the PR #195 packet,
>    which governs substance throughout.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 052: both remain
> separate later acts (the campaign's freeze
> wave and execution pass).

## 1. The adopted basis (operative substance)

- **The design.** D-01 (PR #195 packet,
  `docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
  §D-01): the frozen Phase-43 positional
  battery — same position rules, count floors
  and strength thresholds, no threshold
  adjusted after seeing the data — run on the
  Soviet dataset; per sign, final- and
  initial-position rates with counts;
  crosswalk-conflict pairs reported separately;
  criteria CONSISTENT / INCONSISTENT / TOO
  THIN fixed in advance; arm A a consistency
  check that narrows or widens the caveat on
  a SETTLED claim and re-opens nothing.
- **The claim.** `farmer_sproat_witzel_2004_manual_001`:
  contradicted, on Rao et al. 2009's published
  entropy (outside this program) and on the
  Phase-43 battery's 20 TERMINAL_STRONG signs
  and fixed [M77/267][M77/99] opening formula
  (both produced in-lineage) — claim F052-C02.
- **The fragments.** Three restatement
  records — `…_critique_0001`, `…_critique_0002`,
  `without_kings…_language_0001` — carrying no
  separate substance; §4.2 of the spec gives
  each a dated append in the parent's words
  under every outcome, no separate verdict,
  no status change, and no bookkeeping
  disposition (the design assigns that to a
  record act outside the experiment) —
  claim F052-C05.
- **The data.** The Phase-121 Soviet dataset:
  109 records, seven printed tables, as pinned
  in spec §2.1.
- **Arm B's contingent status (recorded, per
  E-3).** Arm B — the identical battery plus a
  conditional-entropy computation on a
  genuinely independent full corpus entering
  through Phase-130 intake — is
  **trigger-armed and not a member of this
  campaign pass**. The trigger (genuinely new,
  independent inscription data; the weekly
  data watch tests for it) had **not** fired
  at this draft: its precondition was
  re-tested on 2026-10-20 and both candidate
  datasets closed as ICIT-lineage. If the
  trigger fires mid-pass, arm B **queues for
  a mini planning gate**; it does not join
  this pass, and this spec does not design
  arm B's execution, register its criteria, or
  compute any entropy quantity (claim
  F052-C06). A future gate may commission an
  arm B spec; nothing here pre-judges it.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
through the GitHub API against `main` at
`83b6a563402b02809ab1143848e4dd2c0cfd9de3`
(the merge of PR #241):

- **Design D-01** — read in full in the
  campaign packet copy: the open point
  (two of three contradicting items produced
  in-lineage), the hypothesis, the falsifier,
  arm A's method and criteria, the controls
  (crosswalk conflicts 383 of 762; exact
  counts), the move (caveat only) and the
  not-establish lines.
- **The parent claim's record** — read on
  `main`: status contradicted, stage
  explained, the three contradicting-evidence
  entries, and the not-understood text naming
  the independent-corpus positional check.
  SHA-256 recomputed: `c4cf441f…`.
- **The Soviet dataset** — dataset JSON,
  results JSON, extraction memo and loader
  read on `main`; all §2.1 pins recomputed
  (dataset `8eaf2bd9…`, results `d1d4f19f…`,
  memo `58bc887f…`, loader `e4438e1d…`, and
  the seven CSVs). Composition verified
  against the memo: per-table counts
  56 / 11 / 21 / 9 / 4 / 3 / 5 = 109;
  provenance_gaps []; K1965-T4 the only
  per-sign positional table; the printed
  anomalies (T3; T4 computed 160 vs printed
  171) recorded as printed. Hand verification
  verified as the memo states it: a 36-cell
  sample, 36/36 (see defect 4).
- **The Phase-43 battery record** —
  `outputs/phase43_all.json` read on `main`
  (SHA-256 `78a6c219…`): 3,137 sequences;
  T2_2 counts (201 profiled; 20 terminal
  strong; 10 terminal moderate; 40 initial
  strong; 61 medial strong); the ten listed
  TERMINAL_STRONG rates (0.683–0.892); T2_3's
  top candidate (267, 99; bigram 251;
  dominance 0.74). The repository tree was
  searched for battery code: **no phase-43
  code file exists on `main`** (see defect 1).
  The corpus-v3 loader was read (SHA-256
  `3e86c934…`); its underlying Firestore dump
  file is not in the repository tree.
- **The crosswalk record** — Phase-122
  results read on `main` (SHA-256
  `b77fcf49…`): 762 pairs, 383 conflict pairs
  across 209 Parpola signs; crosswalk v1 CSV
  and JSON pinned (spec §2.3).
- **Spec 020's adjudication** — noted, not
  revisited: Spec 020 adjudicated this
  dataset as an evaluation source for
  PRED-2026-001/002. Spec 052 scores no
  prediction and takes no position on that
  adjudication (spec §11).
- **Phase-number state** — no execution
  phase number is allocated at this draft
  (DD-052-6).
- **Not done at draft, by design** — no
  positional quantity was computed on the
  Soviet data; no battery definition was
  derived (that is the freeze's gate-0.5
  product); no code was written or run; the
  AEE hooks have not run; nothing was filed
  with OSF. The gate-0.4 census counts (b)
  and (c) are **not** stated in this draft as
  run results: count (b) is described from
  the memo's record (8 K1965-T4 data rows),
  and count (c) does not exist until a freeze
  freezes a mapping.

## 3. Acceptance tests, derived twice (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently**: Derivation A worked from the
requirement text alone (what observable would
settle it?); Derivation B worked from the
outcome side (enumerate every outcome and stop
class, then invert: what check distinguishes
them and catches a mislabelled one?). The two
derivations agreed on the gate-and-inspection
form of every requirement claim (the Spec
032–042 convention) and on the mechanical
form of F052-C04/C11. Four disagreements
arose; all are resolved here, not left for
the freeze to discover:

1. **The TOO THIN denominator.** A read the
   criterion against the 109 dataset records;
   B read it against battery-usable texts and
   found **zero** — the held records are
   printed table rows, and no record *is* a
   text. *Resolution:* the draft refuses both
   shortcuts. The criterion stands verbatim
   (F052-C12); its application runs through
   the record-to-battery-input mapping the
   freeze must freeze under gate 0.5, and
   gate 0.4 publishes all three counts (total,
   per-sign positional, mapped) so the
   application is inspectable. If no honest
   mapping exists, the closure is gate 0.5's
   BATTERY NOT PINNABLE wording — not a
   redefinition of "record." Recorded as
   defect 2 (§6) and OPEN item 2 (§5).
2. **The exactly-one-half outcome.** A's
   derivation produced the design's three
   outcomes and stopped; B's enumeration
   showed a run in which exactly one of F, O
   fires belongs to no outcome word — the
   design's set is incomplete. *Resolution:*
   PARTIAL added as a draft-named outcome
   (DD-052-3), with pre-written wording
   (spec §4.3), for the freeze to confirm or
   replace openly. Recorded as defect 3.
3. **What pins the battery.** A pinned only
   `outputs/phase43_all.json`; B required an
   executable, and found none exists.
   *Resolution:* the record pin stands
   (F052-C08), and gate 0.5 (F052-C09) makes
   the freeze derive the battery definition
   from that record, element by element with
   citations, closing the spec if any element
   cannot be derived. Recorded as defect 1.
4. **Whether a CONSISTENT outcome may be
   worded as retiring the caveat.** A drafted
   "retires" from the design's arm-B sentence;
   B caught that the design assigns retiring
   to arm B only — arm A "narrows or widens."
   *Resolution:* every arm A wording in
   spec §4.3 uses narrow / widen / restate;
   "retire" appears nowhere as an arm A
   consequence (F052-C14).

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-052-1 — Arm A only.** This spec's
  scope is arm A; arm B is recorded as a
  contingent, trigger-armed non-member under
  campaign decision E-3 (§1 above), and its
  execution is not designed here
  (claim F052-C06).
- **DD-052-2 — The outcome appends; settled
  records are untouched.** The arm A outcome
  appends as a dated entry to the parent
  claim's record and to each fragment's
  record. No settled status, verdict wording,
  or frozen record is edited (claims
  F052-C05, F052-C14).
- **DD-052-3 — PARTIAL is the
  exactly-one-half outcome word.** Design
  D-01 names CONSISTENT, INCONSISTENT and
  TOO THIN only. The draft adds PARTIAL so
  the outcome set is complete before any
  run (claim F052-C11, spec §4.1/§4.3).
- **DD-052-4 — The hand-verification fact is
  stated precisely.** Where the campaign
  plan and the triage compress it to "109
  hand-verified records," this draft states
  the memo's record: 109 records; hand
  verification a 36-cell sample, 36 of 36
  (claim F052-C07, spec §2.1).
- **DD-052-5 — BATTERY NOT PINNABLE is a
  step-0 closure class, and no threshold is
  stated at draft.** The Phase-43 record
  does not state its rules numerically;
  inventing them at draft would fit the test
  to its drafter. The draft therefore states
  none, and gate 0.5 carries the consequence
  (claim F052-C09, spec §9).
- **DD-052-6 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-052-7 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  Spec 038/042 precedent is followed at the
  act that actually observed the records.

## 5. OPEN — for the freeze to decide

1. **The battery definition itself**
   (gate 0.5): position rules, count floors,
   the numeric final-position strength
   threshold, the opening formula's
   definition, the chance-baseline method —
   each derived from the Phase-43 record with
   a citation, or the spec closes at that
   gate. This is the freeze's largest item:
   the definition *is* the test, and it does
   not exist yet.
2. **The record-to-battery-input mapping**,
   including: how K1965-T4's aggregated
   pair × final counts enter a battery built
   for inscription texts; the passage from
   Marshall numbering (T4's signs) to the
   battery's Mahadevan numbering; whether the
   opening formula is asked as the same pair
   (267, 99) or as any fixed pair under the
   battery's rules; and how the gate-0.6
   TOO THIN count follows from the mapping.
   Any mapping choice that would change a
   test outcome is a freeze decision recorded
   here, never run-time discretion (campaign
   tripwire rule).
3. **DD-052-3 (PARTIAL)** — confirm the word
   and its §4.3 wording, or replace them
   openly.
4. **DD-052-5 (BATTERY NOT PINNABLE)** —
   confirm the closure class and wording.
5. **OSF registration (campaign decision
   E-1).** The approved plan already settles
   the policy: this spec files its own OSF
   contract registration at its freeze. The
   freeze executes that policy; nothing is
   filed at draft.
6. **Whether execution requires a battery
   reproduction check** beyond gate 0.2's
   read-back — for example, reproducing the
   recorded profile counts from the corpus-v3
   loader. The draft takes no position; the
   loader's underlying dump is not in the
   repository tree, which the freeze must
   weigh before requiring a reproduction it
   may not be able to run.

## 6. Defects found in the sources at drafting

Recorded here, and reported with the draft;
none is repaired inside this spec (campaign
rule: a defect closes or queues; it is never
patched mid-pass).

1. **No executable Phase-43 battery exists
   on `main`, and its rules are not stated
   numerically in its results file.** The
   campaign plan and the design both speak of
   "the frozen Phase-43 battery" as a thing
   that can simply be run; what is frozen is
   a results file (`outputs/phase43_all.json`)
   and a corpus loader whose data file is
   absent. Gate 0.5 is this draft's honest
   consequence. If the freeze cannot derive
   the definition, arm A is a drafting /
   freeze failure to report — not a licence
   to reconstruct the battery from memory.
2. **The design's TOO THIN criterion
   presupposes inscription-text records; the
   held Soviet dataset is aggregated printed
   tables.** Of 109 records, only K1965-T4's
   8 data rows carry per-sign positional
   counts, and they are aggregated pair ×
   final frequencies, not texts. Whether arm
   A as designed can run on this material at
   all is exactly what gates 0.4–0.6 exist to
   decide, in the open, at freeze and step 0.
3. **The design's outcome set is incomplete**:
   it names no outcome for exactly one of its
   two consistency halves appearing.
   (Draft-named PARTIAL, DD-052-3.)
4. **"36 of 36 hand-verified" compresses a
   sample into a census.** The memo's record
   is a 36-cell sample across seven tables.
   The campaign plan's "109 hand-verified
   records" and the triage's "(109 records,
   hand-verified in Phases 120–124)" both
   overstate it; the extraction itself was
   Phase-121's work. (Stated precisely,
   DD-052-4.)
5. **Spec 020 already adjudicated this
   dataset for a neighbouring purpose** (as
   an evaluation source for PRED-2026-001/002,
   with the dataset's own non-claims fence:
   "descriptive dataset only; it scores no
   prediction"). This spec is compatible with
   that record — it scores no prediction —
   but any reading of arm A as quietly
   promoting the dataset to an evaluation
   corpus would collide with it. Spec §11
   states the boundary.

## 7. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record, the §5 items decided, and the
   gate-0.5 battery definition produced and
   frozen as part of the freeze act — or
   decline, leaving the parent claim with its
   recorded caveat exactly as it stands:
   the positional evidence in-lineage only,
   the Soviet check unrun.
2. The OSF filing under E-1, executed at the
   freeze (§5, item 5).

## 10. Owner mini-gate approval and the freeze act — 2026-10-23

### 10.1 Approval

On 2026-10-23 at 22:59 EDT the owner approved the
mini-gate as specified: "Approve both mini-gates as
specified." The three decisions of `amendment.md` §7
stand as there written: (1) battery NB-1 adopted as
specified in `amendment.md` §3; (2) the data re-scoped
to the Shakti corpus layer as §4 states it; (3) the
amended step-0 gates A–D and the re-pointed outcome
semantics of §§5–6 adopted. Approval of this mini-gate
is approval of the freeze path of §9.4. It is not an
execution order; execution still awaits a separate
owner order.

### 10.2 The freeze act

Executed the same evening under that approval:

- The draft branch (forked from main on 2026-10-21 at
  83b6a563) was brought onto the merged record as it
  stands by merging main, so the freeze is built on
  the record that includes the Specs 068–073 freezes
  and the Spec 041 execution.
- L4 ran: the AEE lifecycle hooks (after_specify,
  after_plan, after_tasks) over the register, with
  three recovery rounds (register 0.5-draft →
  0.8-draft). The gate passes on the DD-038-10
  reading: zero correctness failure modes, only
  FR-2.3 draft-cap records, minimum propagated
  confidence 0.72 against the 0.70 threshold. The
  rounds are recorded in the register's note and in
  `aee/freeze-aee-note.md`.
- The corpus-layer pins were taken at the freeze
  from the restricted-local store, and the
  populations were reproduced from the pinned files
  (`freeze.md` §3): corpus SHA-256 `345241b1…`, row
  grades SHA-256 `02394241…`; primary 3,045 rows /
  11,805 tokens / 557 signs; sensitivity 5,131 rows
  / 17,216 tokens / 707 signs.
- **Phase-437** is allocated to this spec's execution
  (DD-052-6, from the merged record: the highest
  phase report on main at the freeze was Phase-436,
  Spec 073).
- L5 stands decided **as amended** (tasks A3): the
  battery-derivation and Soviet-mapping items are
  closed by §9's rulings, not by the freeze;
  DD-052-3 (PARTIAL) is confirmed, retained in the
  amendment's outcome semantics; DD-052-5 is
  superseded by the amendment route; the
  battery-reproduction question is answered by
  amended gate C (determinism) — no Soviet battery is
  reproduced, because none is run; the OSF filing is
  executed under campaign decision E-1.
- The OSF registration for the frozen spec is filed
  at the freeze and recorded in
  `osf-spec-registration.md`. The registration's
  approval is the owner's act; execution does not
  begin while approval is pending, nor after it
  without the separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 8. Freeze-stage adjudication — 2026-10-21: FREEZE FAILURE (gate 0.5 — BATTERY NOT PINNABLE)

This section records a freeze attempt and its outcome. It is a
campaign bookkeeping act only: it is not a freeze, and it repairs
nothing.

- **Freeze attempt.** On 2026-10-21 the freeze for Spec 052
  (D-01 arm A, draft PR #249, branch
  `spec-052-farmer-not-writing-soviet-draft`, head `c31b9fca`)
  attempted gate 0.5: derive the Phase-43 positional battery's
  definition, element by element with citations, from the record
  of record on `main`.
- **Outcome: FREEZE FAILURE — gate 0.5, BATTERY NOT PINNABLE.**
  No element of the battery definition is fully derivable from
  any Phase-43 record. No threshold was invented and no constant
  was borrowed from a neighbouring battery. Under the draft's
  own terms (F052-C09, DD-052-5), the spec therefore cannot
  freeze.

### 8.1 The six missing-rule findings (condensed)

1. **Position rules — not stated.** Nothing in any Phase-43
   record states which occurrence is initial, terminal, or
   medial, or how short (length-1 or length-2) sequences are
   handled. The results file's rates partition a sign's
   occurrences (terminal + initial + medial rates sum to 1.0),
   but the rule that produces that partition is nowhere stated
   for Phase 43.
2. **Count floors — none stated.** No floor appears in the
   Phase-43 record. The listed TERMINAL_STRONG signs have totals
   of 22 to 1,318, which only bounds any floor at ≤22; it does
   not fix it.
3. **Final-position strength threshold — not locatable.** The
   listed TERMINAL_STRONG signs carry terminal rates of 0.683
   to 0.892, bounding any threshold at ≤0.683 only. No
   TERMINAL_MODERATE sign's rate is given anywhere, so the
   STRONG/MODERATE boundary cannot be located from below.
4. **Opening-formula counting rule — not stated, and the
   record contradicts itself.** The pair (267, 99) is recorded,
   but the results file gives its bigram count as 251 in one
   entry and 278 in entry T2_4, and the recorded dominance of
   0.74 matches no stated denominator (251/356 = 0.7051, not
   0.74). Which pair counts, and how, is not derivable.
5. **Chance-baseline method — absent.** No baseline, null,
   permutation, or significance field exists in the results
   file. The claim record's phrase "above random baseline"
   states no method and no number.
6. **Soviet mapping — independently impossible.** Per Spec 020
   facts F3/F5/F6: the Soviet dataset contains no inscription
   sequences; K1965-T4 is verified as 8×7 joint counts (initial
   pairs × final signs) with no per-sign denominators, so no
   per-sign rate can be computed; and no Marshall↔Mahadevan map
   is extractable from sources on `main`. The battery, defined
   over inscription texts in Mahadevan numbering, has no honest
   input mapping from this material.

Further record facts: the results file lists only 10 of the
claimed 20 TERMINAL_STRONG signs; no Phase-43 script or report
exists on `main` — the tree's only phase43 path is
`outputs/phase43_all.json`; the corpus-v3 loader's Firestore
dump is absent from the repository, so even a reproduction run
cannot be run; and five neighbouring batteries carry five
incompatible constant sets, so borrowing any of them would be
invention, not derivation.

### 8.2 Searches performed

- The full recursive tree of `main`: 5,435 blobs, searched for
  any phase43 / phase_43 / phase-43 path (exactly one hit, the
  results file above) and for the loader's data file (absent).
- The Phase-43 claim records, including the farmer claim record
  and the fragment records that carry its strings.
- Specs 019, 020, and 033 in full: none states Phase-43 battery
  rules; Spec 020's F3/F5/F6 record governs the mapping finding.
- The neighbouring batteries (Phase 6.2/7 structural analysis,
  the Phase-113 battery, Phase-45 T3, the candidate
  prefix/suffix report, and Phase-33 positional profiles),
  confirming five incompatible constant sets.
- GitHub code search for the battery's labels and names; two
  queries (`T2_2` and `terminal_suffix`) were cut off by the
  code-search API rate limit and are recorded as a residual —
  both are key names internal to the results file, and the
  completed sweeps enumerated every file using the battery's
  label or name.

### 8.3 Pins verified

Verified by two routes (contents raw and git blob), all
agreeing:

- `outputs/phase43_all.json` — SHA-256 `78a6c219…`
  (78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4)
- Farmer claim record
  (`glossa-indus/claims/extracted_claims/farmer_sproat_witzel_2004.json`)
  — SHA-256 `c4cf441f…`
  (c4cf441fda420bcbf7550984404580c3fdb181818909ff02009b13fb1ab0f9da)
- Corpus-v3 loader (`backend/glossa_lab/data/indus_corpus_v3.py`)
  — SHA-256 `3e86c934…`
  (3e86c934db136ba12c7370c2696573c27b7ec0fc924f231d285360fa7346846b)
- K1965-T4 CSV
  (`data/soviet_positional/kondratov1965_table4_stable_initials_finals.csv`)
  — SHA-256 `e2933bf0…`
  (e2933bf0b36c9db90de2eddac083c215a0e9c6e98dd9f4c580d359da68443f1f)

### 8.4 What did not happen

- **Phase-412 was NOT allocated.** Allocation is a freeze act,
  and no freeze occurred.
- No AEE hooks were run, no digest was computed, and no OSF
  registration was filed.
- The other OPEN items in §5 stand undecided. OPEN-1 (the
  battery definition) is antecedent: deciding the remaining
  items would have been freeze acts, and there is no freeze.
  OPEN-2 through OPEN-6 are neither confirmed nor overturned
  by this entry.

### 8.5 Unblocking conditions and disposition

This failure would be unblocked by a record of record supplying
what is missing:

1. The original Phase-43 script, or a contemporaneous numeric
   methods record, stating the position rules, the count
   floors, the strength threshold, the opening-pair counting
   rule and dominance denominator, and the chance-baseline
   method; or
2. An owner amendment re-scoping Spec 052 to a new,
   explicitly defined battery — a design change, honestly
   labelled as a new test rather than as the frozen Phase-43
   battery; and, for any mapping variant,
3. A frozen Marshall↔Mahadevan map plus per-sign denominators
   for the T4 signs — in practice, an inscription-level
   Soviet-era corpus.

**Disposition: the defect queues as an amendment** (a new mini
planning gate) under Part 7 of the approved campaign plan.
This branch is not repaired in-pass, and draft PR #249 remains
open as the record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 9. Settled rulings — owner approval 2026-10-23 (Item 2)

§8 closed the 2026-10-21 freeze attempt: the battery could not
be pinned out of the Phase-43 record, and the Soviet mapping
could not be constructed from the records the program holds.
§8.5 named three candidate routes to a freeze-grade design and
reserved both questions to the owner. The owner decided both
on 2026-10-23, approving Item 2 of the waiting-decisions
package as written. The rulings are recorded here; the
amendment they commission is `amendment.md` in this
directory, and it returns to the owner as a mini-gate. This
spec is not frozen by anything in this section.

### 9.1 Ruling (a) — the battery: nothing under the Phase-43 name

**Ruled:** no battery element — the chance baseline
included — may be invented or borrowed under the Phase-43
name. The route adopted is §8.5 route (2): an amendment with
a new, explicitly defined battery, honestly labelled as new.
Route (1) — recovery of the original Phase-43 pipeline —
remains open as a standing possibility: if the original
script or scratch directory surfaces, the owner may redirect
this spec to it by a fresh ruling, and the amendment is then
moot. Route (3) — a narrowed Soviet-only design on the
surviving sub-record — is not adopted.

Consequence for this draft: gate 0.5's demand is discharged
differently than §5 item 1 imagined. The battery definition
is no longer "derived from the Phase-43 record and cited,
element by element"; it is defined in full in the amendment,
with every element's derivation — or its honest basis as a
stated design choice — written next to it. Claims
F052-C09's boundary is superseded to that extent by the
amendment (claim F052-C16), and the amendment says so in its
own text.

### 9.2 Ruling (b) — the Soviet mapping: impossible on the current record

**Ruled:** the Soviet mapping is impossible on the current
record. Arm A **as designed** — the Phase-43 battery run on
the Soviet compilation's dataset through a Marshall →
Mahadevan mapping — is closed. The Soviet tables retire from
this member: K1965-T4 and the Phase-121 dataset pins remain
in §2 and in the freeze-failure record as history, but no
amended run consumes them.

The record the ruling rests on is §8.3's and §8.4's:
Spec 020's findings F3, F5 and F6 (the crosswalk carries no
Marshall passage; K1965-T4's cells are aggregated pair-by-
final counts, pair (267, 99) its largest, with no per-sign
denominators and no first-sign marginals; the tabulated signs
are functions of two signs at once, not of single signs);
the Phase-121 dataset is the Bulgarian volume's sign list,
not inscription texts; and the crosswalk's 383 conflict
pairs sit exactly where the mapping would have to work
hardest. A mapping built from these records would have been
invented, and an invented mapping would have decided the
outcome before the run.

### 9.3 What the amendment therefore changes, and what it does not

The amendment keeps the spec's question and its outcome
machinery, and changes the data and the battery:

- The pattern under test is unchanged: §2's two
  sub-predictions of the Farmer–Sproat–Witzel thesis —
  dedicated final-position sign sets (F) and a fixed opening
  formula (O) — evaluated as a consistency check on a settled
  claim, never as a verdict machine (F052-C01 stands).
- The data changes: the amended run evaluates F and O on
  inscription-level material — the Shakti corpus layer —
  whose compilation lineage (the CISI corpus tradition) is
  distinct from the Soviet compilation behind the claim's
  original outcome and distinct from the Holdat/M77 lineage.
  What "distinct lineage" does and does not buy is stated in
  the amendment, not overclaimed.
- The battery changes: NB-1, defined in full in the
  amendment (claim F052-C16), replaces the unrecoverable
  Phase-43 battery. The outcome words of §4.1 and the
  append duties of §4.2 survive, re-pointed at NB-1 and the
  new population (claim F052-C19); the Soviet-specific
  step-0 gates and closure classes of §3 are replaced by the
  amended gates (claim F052-C18).
- The parent claim's status does not move: it stands
  contradicted as recorded, and no outcome of the amended
  run moves it (§6's rule, unchanged).

### 9.4 What returns to the owner

The amendment draft — this section, `amendment.md`, claims
F052-C16…C19, and the amendment tasks — is the mini-gate.
The owner approves it, amends it, or declines it. Only on
approval does the freeze path resume: AEE lifecycle hooks
over the recovered register (L4), the freeze act with the
corpus-layer pins taken at freeze time, the OSF filing, and
then a separate execution order. Nothing in this section
freezes, files, or executes anything.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
