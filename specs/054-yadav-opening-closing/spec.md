# Spec 054 — Yadav's Opening/Closing Signs: Given a Falsifier, Then Rerun (Design D-08)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`),
> Wave 1, independent members in parallel: this
> spec is campaign member 7 (design D-08). It
> consumes no shared asset — campaign Part 3
> lists D-08 among the members that stand alone
> on inputs already frozen or on record (the
> strict corpus, the Holdat layer, the crosswalk,
> the Phase-43 thresholds). Drafts are
> pre-approved standing in this program; **the
> freeze and the execution of Spec 054 are
> separate later owner acts.** No AEE lifecycle
> hooks have run on this draft; they are a
> freeze gate. Nothing in this draft has been
> run, frozen, registered, or computed.
>
> The execution phase number is **unassigned**
> at this draft. It is allocated at the freeze
> act, from the merged record as it then stands
> (DD-054-7).

**Design source:** D-08 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
§D-08, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-08
found **RIPE**: "Strict corpus, Holdat layer,
and crosswalk are in hand; Phase-43 thresholds
are on record. The design's first product — a
falsifier written onto a record that never had
one — is available whatever the rerun finds.").

**Claim under test:**
`yadav_2009_arxiv_manual_002` — "There are
specific text-beginning and text-ending signs
in the Indus corpus" — standing **strongly
supported** on the Phase-43 counts, but the
record carries **no falsification condition**:
as recorded, the claim could not have failed.
The packet classifies it **IN QUESTION** for
exactly that defect.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The claim record
(`glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`,
SHA-256 `90476623…`, read first-hand at this
draft) states, for
`yadav_2009_arxiv_manual_002`:

- **Normalised claim:** "There are specific
  text-beginning and text-ending signs in the
  Indus corpus."
- **Status:** `strongly_supported`; stage
  `explained` (lane-2 adoption, 2026-10-13).
- **Evidence line:** "Phase-43: 20
  TERMINAL_STRONG + 40 INITIAL_STRONG signs
  identified in V3 corpus [VERIFIED]".
- **Falsification condition:** **none.** The
  record carries no `falsification_condition`
  field for this claim at all — its companion
  claim (`…_manual_001`, the Zipf claim) carries
  one; this one does not. That absence, verified
  field by field at this draft, is the defect
  this design exists to fix.
- **Not-understood text (in substance):**
  positional preference is not meaning; opening
  and closing markers appear in many symbol
  systems, linguistic and not; the counts depend
  on where inscriptions are segmented and on
  the sign inventory of one corpus lineage; the
  cross-compilation disagreement (Phase-125)
  means the same exercise on the other great
  compilation might not return the same sign
  sets. What would change the picture: "a
  falsifier written onto the record, and the
  test rerun on the strict core and on an
  independent corpus with the position rules
  fixed in advance."

The Phase-43 record of those counts
(`outputs/phase43_all.json`, SHA-256
`78a6c219…`, read first-hand at this draft)
states: **initial-strong 40, terminal-strong
20, medial-strong 61, total signs profiled
201** (§T2_2_terminal_suffix_table counts),
on a V3 corpus of 3,137 sequences and 12,494
sign instances (§T1_1_corpus_v3). The companion
positional record
(`glossa-indus/analysis/positional/hunt_tripartite_test.json`,
SHA-256 `0e546962…`) states the same 40/61/20
classes, mean initial rate of the initial signs
0.757, mean terminal rate of the terminal signs
0.805, against an expected-by-chance rate of
0.251. The counts are not in dispute. What has
never existed is a recorded rule by which they
could have come out otherwise — see §3, gate
0.2, and adjudication §6, defect 1, for what
the Phase-43 file does and does not contain.

### 1.1 The question, in plain words

Some signs really do prefer the start of texts
and others the end — the counts are not in
dispute. The open point is whether that pattern
survives when the rules are fixed sharply
enough that it *could* fail: on the strict
sign set, and in the other great compilation.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** Under position rules frozen in
advance, a stable set of signs prefers
text-initial position and a stable set prefers
text-final position, in both the strict corpus
and the Holdat layer, with membership overlap
well above chance.

**Falsifier (written onto the record by this
design, before any rerun — stated verbatim as
the design gives it).** The claim fails if,
under the frozen rules, fewer than half of the
original 40/20 sign sets reappear on the
strict corpus; or if the two compilations'
strong-sign sets overlap no more than shuffled
sign labels do; or if the effect disappears
when inscription segmentation follows the
other compilation's conventions.

This falsifier text is appended to the claim
record as part of this spec's **freeze**,
whichever way the rerun lands (§4; claim
F054-C04) — the record defect is fixed by the
design, not by the outcome. Nothing in this
draft appends it yet: a draft is not a freeze.

## 2. Inputs (pinned at this draft where a pin exists; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`) | SHA-256 `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3` (recomputed at this draft from `main`, head `83b6a563…`, and re-verified by a second, raw fetch). Manual_002's status, evidence line, stage, and the absence of its falsification field were read from this file. |
| Phase-43 battery record (`outputs/phase43_all.json`) — the counts and thresholds of record | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft; the same pin Specs 045 and 048 carry). §T2_2 counts: initial-strong 40, terminal-strong 20, medial-strong 61, signs profiled 201; §T1_1: 3,137 sequences, 12,494 sign instances. The file states counts and, for ten terminal-strong signs, per-sign rates — it does **not** state the battery's strong-sign threshold rule or the full membership lists (adjudication §6, defect 1). |
| Positional companion record (`glossa-indus/analysis/positional/hunt_tripartite_test.json`) | SHA-256 `0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48` (recomputed at this draft; the same pin Spec 045 carries): 40/61/20 strong classes; mean initial rate 0.757; mean terminal rate 0.805; expected by chance 0.251; formula test 805 of 2,267 inscriptions of length ≥ 3. |
| Crosswalk of record (`data/crosswalks/parpola_mahadevan_crosswalk_v1.json`, with its `.csv`) | JSON SHA-256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb`; CSV SHA-256 `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823` (both recomputed at this draft; both are the pins Spec 019's freeze carries). 762 pairs; 383 conflict pairs on the Phase-122 record. Which crosswalk file governs this spec's arm-2 mapping is confirmed at the freeze (OPEN-054-4); no other crosswalk file is used under this spec. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) — the strict sign set's census source | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). Census read at this draft: 287 anchors, 94 carrying validation status `strict_sa_independent`. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Strict corpus (arm 1) — the strict sign set and the V3 corpus the Phase-43 battery ran on | **No file pin is stated at this draft, deliberately.** Spec 033 §4 states this corpus as "the program's V3/Mahadevan-lineage corpus as held in the database" — a database posture, not a pinnable repository file on `main`. The layer is therefore identified, exported, and pinned by digest at step 0, before any counting, under gate 0.3 — and the run closes if it cannot be (DD-054-3; OPEN-054-2). The Phase-393 / Yajnadevam layer pinned by Specs 042 and 045 is a **different layer** and is never substituted for the V3 corpus under this spec. Inventing a pin at draft would repeat the stale-pin failure Spec 040's gate record documents. |
| Holdat layer (arm 2) — the other great compilation, under its own sign numbering, with its published segmentation conventions | **No pin at this draft, for the same reason.** The repository holds Holdat-derived files but no single layer file is asserted here as arm 2's corpus; it is identified and pinned at gate 0.4, with the per-sign crosswalk stated in the step-0 record. Failure closes the run as SECOND ARM NOT RUNNABLE (DD-054-4). |

## 3. Step 0 — gates before any strong-sign set is computed (fail-closed)

Execution runs these gates in order, before
any positional quantity is computed in either
arm. A failure stops the execution in the
class named; nothing is repaired at run time,
and no count produced before a gate failure is
quotable.

- **0.1 Input integrity.** Every §2 input that
  carries a pin hashes to its freeze-record
  value, and the anchors file is asserted
  byte-identical. A mismatch stops the run as
  **INVALID**.
- **0.2 The original sets, exhibited.** The
  step-0 record exhibits the original
  opening-strong set (40 signs) and the
  original closing-strong set (20 signs),
  sign by sign, each sign cited to the pinned
  record it was read from. The Phase-43 file
  of record states the counts and exhibits
  only ten terminal-strong entries; it does
  not exhibit either full set (adjudication
  §6, defect 1). If either full set cannot be
  exhibited from a pinned source on the
  record, the run closes as **ORIGINAL SETS
  NOT EXHIBITABLE** (§6 wording) — the
  falsifier's first condition ("fewer than
  half of the original 40/20 sign sets
  reappear") has no measurable object without
  the sets themselves, and no set is
  reconstructed from memory, from a later
  compilation, or from this draft.
- **0.3 Strict corpus identification, pin, and
  battery reproduction.** Arm 1's layer is
  identified from the database as the V3 /
  Mahadevan-lineage corpus the Phase-43
  battery used, exported in full, and pinned
  by SHA-256 in the step-0 record. The gate
  then re-runs the Phase-43 positional
  battery, under the threshold rule the freeze
  stated from the record (OPEN-054-1), on the
  pinned layer, and requires the recorded
  reference points to reproduce: 201 signs
  profiled; 40 initial-strong, 20
  terminal-strong, 61 medial-strong; the ten
  exhibited terminal-strong signs' rates
  within the record's rounding. If the layer
  cannot be uniquely identified or exported
  whole, the run closes as **STRICT CORPUS
  NOT PINNABLE**; if it is pinned but the
  reference points do not reproduce under the
  frozen threshold rule, the run closes as
  **BATTERY NOT REPRODUCED**. Either way,
  nothing is counted toward a verdict.
- **0.4 Holdat layer, crosswalk, and
  segmentation statement.** Arm 2's layer is
  identified and pinned by digest. The
  crosswalk from the exhibited original sets
  (gate 0.2) to Holdat numbering is stated
  per sign in the step-0 record, through the
  §2 crosswalk of record: every original sign
  is recorded as mapped, unmapped, or a
  **conflict pair** — conflict pairs are
  reported separately in both arms, never
  silently dropped (the Phase-122 record
  counts 383 conflict pairs among the
  crosswalk's 762). The step-0 record also
  states arm 2's segmentation conventions as
  published for that compilation, beside arm
  1's, so the segmentation comparison of §5
  is a stated pair of conventions, not an
  assumption. If the layer cannot be
  identified and pinned, if the per-sign
  crosswalk cannot be stated for an exhibited
  original sign, or if either compilation's
  segmentation conventions cannot be stated
  from its published record, the run closes
  as **SECOND ARM NOT RUNNABLE**.
- **0.5 Census and floor (margins only).** Per
  exhibited original sign, and per arm, the
  total occurrence count in the pinned layer
  is computed — occurrence counts only, no
  positional quantity. The minimum-occurrence
  floor is the single value fixed at the
  freeze (OPEN-054-3), identical in both
  arms, exactly as the design's controls
  require. An original sign below the floor
  in an arm is recorded **TOO THIN** in that
  arm, with its count. If, in arm 1, **no**
  opening original sign or **no** closing
  original sign clears the floor, the
  execution closes as **TOO THIN** (§6
  wording) with the full census as its
  finding — the reappearance share the
  verdict turns on does not exist for that
  set.

## 4. The falsifier append (a freeze act, not an execution outcome)

At this spec's freeze — before any execution,
and whichever way any later rerun lands — the
falsifier text of §1.2 is appended to the
record of `yadav_2009_arxiv_manual_002` as a
dated entry, in the design's words verbatim.
The append is the design's first product and
is not conditional on the rerun's result, on
this spec's execution ever being ordered, or
on the rerun closing at step 0. The claim's
prior status and evidence lines are not
edited; the append sits beside them. If the
freeze does not happen, no append happens
under this spec — a draft writes nothing onto
the claim record.

## 5. The test

**Arm 1 (strict corpus).** Re-run the
Phase-43 positional battery with its
thresholds unchanged — the threshold rule as
stated at the freeze from the record
(OPEN-054-1) and as reproduced at gate 0.3 —
on the pinned strict corpus, restricted as
the design states to the strict sign set.
Report, per sign, initial / medial / terminal
rates with counts, and the arm's opening-strong
and closing-strong sets in full.

**Arm 2 (Holdat layer).** The identical
battery on the Holdat layer under its own
sign numbering and its published segmentation
conventions, mapping results through the
gate-0.4 crosswalk with conflict pairs
reported separately. Report per-sign rates
with counts and both strong sets in full,
beside arm 1's.

**Reappearance.** An original sign
**reappears** in an arm if it is a member of
that arm's corresponding strong set (opening
to opening, closing to closing; for arm 2,
through the gate-0.4 mapping — an unmapped or
conflict-paired sign is reported as such and
counts as not reappeared in the primary, with
the conflict sensitivity of §5.1). A set
**reproduces** in an arm if at least half of
its exhibited members reappear: at least 20
of the 40 opening signs, and at least 10 of
the 20 closing signs. The reading is per-set,
not pooled (DD-054-1): a pooled share would
let one set's collapse hide behind the other's
survival, and the claim is about both sets.

**Cross-compilation overlap.** The overlap
statistic is the number of signs strong in
both compilations for the corresponding
position class, computed on the mapped signs,
pooled over the opening and closing classes
for the headline and reported per class
beside it. Overlap is measured against a
label-shuffle null of **999 shuffles** (the
design's number): sign labels are shuffled,
the strong sets recomputed in size-matched
form, and the observed overlap is placed
against the null distribution. The shuffle
procedure and its seed are fixed at the
freeze before any counting (OPEN-054-5).

**Segmentation.** Each arm runs under its own
compilation's published segmentation
conventions (gate 0.4). The outcome record
reports, per arm, the inscription count, the
length distribution, and the strong sets, so
a reader can see the segmentation basis each
arm's result sits on. The falsifier's third
condition — the effect disappears under the
other compilation's segmentation — is read
through §6's precedence rule (DD-054-2), not
as a separate free-standing test.

### 5.1 Sensitivity (pre-registered, one)

The reappearance shares are recomputed once,
as a stated sensitivity: original signs below
the gate-0.5 floor, unmapped signs, and
conflict-paired signs are removed from the
denominators in both arms. The sensitivity is
reported beside the primary with the same
prominence; it does not replace the primary's
verdict word.

### 5.2 The closing-sign measure, and Spec 045

Spec 045 (design D-05) defines its
suffix/closing measure operationally in its
own §5.2 — the distinct-predecessor rate in
final position — because this design's measure
was not yet a frozen spec when that draft was
written (Spec 045, DD-045-4). This spec's
closing-sign measure is a **different**
measure: membership in the Phase-43 battery's
terminal-strong set, under the battery's
threshold rule. The two measures both speak
of "closing-sign behaviour" and they are not
interchangeable: a sign can sit in the
terminal-strong set without a high
distinct-predecessor rate, and the reverse.
**At this spec's freeze there is a
reconciliation touchpoint with Spec 045:**
the freeze records, against Spec 045's frozen
text if one exists by then, whether the two
measures are stated as the same measure under
two forms or as two distinct measures with
distinct names, and which form governs which
spec's verdict (OPEN-054-6). Whichever form
the freeze adopts is a freeze decision, not a
drafting one; this draft adopts neither, and
no output of either spec may quote the other's
closing-sign result as if the measures were
one.

## 6. Criteria, outcome set, and pre-written verdict wordings

**Criteria (the design's, fixed in advance).**

- **SUPPORTED (re-earned):** both arms
  reproduce at least half the original sets
  (per §5: each set, each arm) **and**
  cross-compilation overlap exceeds the 95th
  percentile of the shuffle null.
- **NOT SUPPORTED:** any falsifier condition
  of §1.2 fires, under the precedence rule
  below.
- **INCONCLUSIVE:** one arm reproduces and
  the other does not, with counts stated —
  under the precedence rule below.

**Precedence rule (this draft's reading,
DD-054-2; the freeze confirms or overturns it
openly — OPEN-054-7).** The design's criteria
and its falsifier overlap on the one-arm
pattern, so the draft fixes the order in
which they are applied:

1. If arm 1 (the strict corpus) reproduces
   **neither** set in full — that is, either
   original set reappears at less than half —
   the falsifier's first condition has fired:
   **NOT SUPPORTED**, whatever arm 2 shows.
2. If arm 1 reproduces both sets and arm 2
   reproduces both sets: overlap above the
   null's 95th percentile → **SUPPORTED
   (re-earned)**; overlap at or below it →
   the falsifier's second condition has
   fired: **NOT SUPPORTED**.
3. If arm 1 reproduces both sets and arm 2
   reproduces one set or neither: **INCONCLUSIVE**,
   with counts stated. The falsifier's third
   (segmentation) condition is **not** treated
   as separately fired by a one-arm shortfall
   alone: a segmentation difference is the
   named confounder that pattern expresses,
   and the design's own criteria name this
   pattern inconclusive. If arm 2 reproduces
   neither set **and** the pooled overlap is
   at or below the null's 95th percentile, the
   second condition has fired on its own
   terms and the outcome is **NOT SUPPORTED**
   under step 2's rule applied to the overlap.

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with the
bracketed quantities filled from the run.
These wordings are written before any data is
touched; no other headline wording may be
used.

- **SUPPORTED (RE-EARNED):** "Rerun under
  position rules frozen in advance — the
  falsifier at Spec 054 §1.2, appended to the
  claim's record at the freeze — the
  opening/closing pattern re-earns its
  support: the strict corpus reproduces
  [n]/40 opening-strong and [n]/20
  closing-strong original signs, the Holdat
  layer reproduces [n]/40 and [n]/20 through
  the crosswalk (conflict pairs reported
  separately: [n]), and the two compilations'
  strong sets overlap at [x] signs, above the
  95th percentile ([p]) of the 999-shuffle
  null. The claim `yadav_2009_arxiv_manual_002`
  stands supported **under a falsifier it
  could have failed**, which its record did
  not carry before this spec. This does not
  establish that the script encodes language,
  or what any opening or closing sign means."
- **NOT SUPPORTED:** "Rerun under the frozen
  rules of Spec 054, the opening/closing
  claim fails its falsifier: [the condition
  that fired, with quantities — e.g. the
  strict corpus reproduces only [n]/40 opening
  and [n]/20 closing original signs, below
  the half lines of 20 and 10 / the two
  compilations' strong sets overlap at [x]
  signs, at or below the 95th percentile
  ([p]) of the shuffle null]. The claim
  `yadav_2009_arxiv_manual_002` is recorded
  as **not supported** under the falsifier
  appended to its record at this spec's
  freeze. The Phase-43 counts stand as
  recorded; what they no longer carry is a
  strongly-supported status that no stated
  rule could have overturned."
- **INCONCLUSIVE:** "Rerun under the frozen
  rules of Spec 054, the result is
  inconclusive: one compilation reproduces
  the original sets and the other does not —
  strict corpus [n]/40 opening and [n]/20
  closing; Holdat layer [n]/40 and [n]/20,
  with [n] conflict pairs reported
  separately. [Per-arm rates with counts.] The
  claim stands exactly as recorded —
  strongly supported on the Phase-43 counts,
  now with a falsifier on its record and an
  unresolved cross-compilation split beside
  it."
- **TOO THIN (step-0 closure, gate 0.5):**
  "Spec 054 closed at step 0, gate 0.5: in
  the pinned strict corpus, no [opening /
  closing] original sign clears the frozen
  minimum-occurrence floor of [f] ([census]).
  No positional quantity was computed. This
  closure is a statement about runnability,
  not about the claim; the claim stands
  exactly as recorded, with the falsifier
  appended at this spec's freeze."
- **ORIGINAL SETS NOT EXHIBITABLE (step-0
  closure, gate 0.2):** "Spec 054 closed at
  step 0, gate 0.2: the original
  opening-strong and closing-strong sets
  cannot be exhibited in full from a pinned
  source on the record — the Phase-43 file
  states the counts (40 and 20) and exhibits
  [n] closing entries, but neither full set.
  The falsifier's reappearance condition
  therefore has no measurable object, and no
  set was reconstructed. No positional
  quantity was computed. This closure is a
  statement about the record, not about the
  claim; the claim stands exactly as
  recorded, with the falsifier appended at
  this spec's freeze."
- **STRICT CORPUS NOT PINNABLE (step-0
  closure, gate 0.3):** "Spec 054 closed at
  step 0, gate 0.3: the strict corpus layer
  of record could not be uniquely identified
  and pinned from the database as the V3 /
  Mahadevan-lineage corpus the Phase-43
  battery used ([reason]). No positional
  quantity was computed. This closure is a
  statement about runnability, not about the
  claim; the claim stands exactly as
  recorded, with the falsifier appended at
  this spec's freeze."
- **BATTERY NOT REPRODUCED (step-0 closure,
  gate 0.3):** "Spec 054 closed at step 0,
  gate 0.3: the pinned strict corpus does not
  reproduce the Phase-43 reference points
  under the frozen threshold rule ([observed
  vs recorded: profiled signs, strong-class
  counts, exhibited terminal rates]). The
  battery that produced the original counts
  could not be shown to be the battery this
  rerun would run, so no new count is
  comparable to the old ones. No verdict is
  recorded; the claim stands exactly as
  recorded, with the falsifier appended at
  this spec's freeze."
- **SECOND ARM NOT RUNNABLE (step-0 closure,
  gate 0.4):** "Spec 054 closed at step 0,
  gate 0.4: the Holdat arm could not be run
  as designed — [the layer could not be
  identified and pinned / the per-sign
  crosswalk could not be stated for [sign] /
  a compilation's segmentation conventions
  could not be stated from its published
  record]. No positional quantity was
  computed in either arm. This closure is a
  statement about runnability, not about the
  claim; the claim stands exactly as
  recorded, with the falsifier appended at
  this spec's freeze."
- **INVALID (integrity closure):** "Spec 054
  closed as INVALID: [the named §2 pin
  mismatched / the anchors assertion failed /
  the step-0 record does not precede the
  first count / a count was produced on an
  unpinned or unmapped basis]. No result is
  recorded under this spec. The claim stands
  exactly as recorded, with the falsifier
  appended at this spec's freeze."

## 7. Epistemic limits (binding on all outputs)

1. **No language conclusion.** Opening and
   closing markers occur in non-linguistic
   systems too. Even a SUPPORTED (RE-EARNED)
   outcome does not establish that the script
   encodes language — the design states this
   limit in its own text, and every output
   carries it.
2. **No meaning conclusion.** No outcome
   establishes what any opening or closing
   sign means, or what any sign was read as.
3. **The falsifier is the product either
   way.** A NOT SUPPORTED or INCONCLUSIVE
   outcome is not a lesser deliverable: the
   record defect — a strongly-supported claim
   that could not have failed — is fixed by
   §4's append at the freeze, before and
   independently of the rerun.
4. **Compilation-relativity.** The two arms
   are two compilations' stories, computed
   inside each compilation and joined only
   through the pinned crosswalk. No output
   pools the corpora, averages the arms, or
   presents a crosswalk pair as a finding
   that two drawn signs are the same sign.
5. **The Phase-43 record stands.** This spec
   edits no Phase-43 file and no prior claim
   status. Its outcome and the §4 falsifier
   append to the claim's record as dated
   entries beside the frozen ones.
6. **No publication by the campaign.**
   Records under this spec are internal
   campaign records; no paper, website,
   article, or public register wording is
   produced from them by this campaign
   (campaign R-6). Any later publication is a
   separate, approval-gated act.
7. Negative, inconclusive, thin, and step-0
   outcomes are recorded with the same
   prominence as a supported finding.

## 8. Controls and named confounders

- **Segmentation dependence** (named in the
  claim's not-understood text): the second
  compilation's conventions are the control —
  each arm runs under its own compilation's
  published conventions, stated at gate 0.4
  and reported per arm (§5).
- **Corpus-size effects:** rates are reported
  with counts in both arms, and the
  minimum-occurrence floor is identical in
  both arms (gate 0.5) — the design's own
  control, with the floor's value fixed at
  the freeze (OPEN-054-3).
- **Crosswalk conflicts:** reported per sign,
  never dropped silently; conflict-paired and
  unmapped original signs count as not
  reappeared in the primary and are handled
  openly in the §5.1 sensitivity.
- **Within-lineage arm 1:** a re-earned
  SUPPORTED is a win inside the
  Mahadevan/V3 lineage plus a cross-compilation
  agreement with Holdat — it is not a win on a
  corpus independent of both lineages, and no
  output may describe it as one. (The designs
  that speak to independent corpora are D-01
  arm B and D-07 arm B, both trigger-armed
  outside this campaign.)
- **Threshold drift:** the battery's threshold
  rule is stated at the freeze from the
  record and proven against the recorded
  reference points at gate 0.3 before any new
  counting; a rerun under a silently adjusted
  rule is the failure mode that gate exists
  to refuse.

## 9. Reporting obligations

Every product of an execution carries, in its
headline section:

1. the falsifier text (§1.2), verbatim, and
   the date of its §4 append to the claim
   record;
2. the step-0 record: every §2 pin as
   asserted, the exhibited original sets, the
   strict corpus pin (gate 0.3), the Holdat
   pin and per-sign crosswalk (gate 0.4), and
   the census (gate 0.5);
3. per arm: per-sign initial / medial /
   terminal rates with counts, both strong
   sets in full, the reappearance counts per
   original set ([n]/40, [n]/20), and the
   TOO THIN / unmapped / conflict dispositions
   of every original sign;
4. the overlap statistic — pooled and per
   class — with the shuffle null's 95th
   percentile and the observed placement;
5. the §5.1 sensitivity, beside the primary;
6. the headline outcome word of §6, in §6's
   pre-written wording.

Deliverables at execution: a results JSON
(step-0 record with all pins and exhibits,
censuses, per-arm per-sign tables, overlap and
null record, sensitivity), a report under
these headline rules, the experiment-graph
node (H15/H23, registered and verified before
the run), the outcome append in this
directory, the dated append to the claim's
record, and the LEDGER entry (H1). Foundation
check (H21) after the execution phase: 0
failures, or the outcome record says why not.
Anchors asserted byte-identical before and
after.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **SUPPORTED (RE-EARNED)**, **NOT
  SUPPORTED**, or **INCONCLUSIVE** — per §6,
  after all gates pass.
- **TOO THIN** — gate 0.5.
- **ORIGINAL SETS NOT EXHIBITABLE** — gate
  0.2.
- **STRICT CORPUS NOT PINNABLE** or **BATTERY
  NOT REPRODUCED** — gate 0.3.
- **SECOND ARM NOT RUNNABLE** — gate 0.4.
- **INVALID** — a §2 pin mismatches, the
  anchors assertion fails, or any count is
  shown to precede its gate or to rest on an
  unpinned or unmapped basis.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity; original
   sets exhibited; strict corpus pin and
   battery reproduction; Holdat pin, per-sign
   crosswalk, and segmentation statement;
   census and floor.
3. **Arm 1** (§5) — the battery on the pinned
   strict corpus.
4. **Arm 2 and overlap** (§5) — the Holdat
   repeat through the crosswalk; the
   999-shuffle null; the §5.1 sensitivity.
5. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured. Freeze-order
   note: this spec's freeze also performs the
   §4 falsifier append and the §5.2 / OPEN-054-6
   reconciliation against Spec 045's frozen
   text, if one exists by then.

## 12. What this spec is not

Not a test of whether the script encodes
language (that is design D-01's question, and
this design's own limit refuses it), not a
meaning or reading for any sign, not a new
corpus, not Spec 045's depicted-kind test or
its §5.2 suffix measure (see §5.2), not a
re-run of the Zipf claim (design D-07), and
not an authorisation to execute or to publish
anything. It is the act that writes a
falsifier onto a claim that never had one,
and then reruns that claim under rules sharp
enough to fail it — designed so that its
honest outcomes, including closing at its own
step 0 on the record's gaps, are written down
before any sign is counted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
