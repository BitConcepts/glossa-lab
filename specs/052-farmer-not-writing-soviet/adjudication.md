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

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
