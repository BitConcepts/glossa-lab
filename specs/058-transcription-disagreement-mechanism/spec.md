# Spec 058 — What Drove the Spec 023 Transcription Disagreement (Design D-21, Arm A Only)

> ## FROZEN — 2026-10-21
>
> Frozen at the freeze act of 2026-10-21
> under the runnable-experiments
> campaign plan approved by the owner AS
> WRITTEN on 2026-10-21
> (`2026-10-21-runnable-experiments-
> campaign-plan.md`, Parts 1–4 and Part 6
> item 4): campaign member 15, design
> D-21, arm A only. The portfolio triage
> of 2026-10-21 found D-21 **RIPE (arm A)**.
> The AEE lifecycle hooks ran at the
> freeze gate and passed over the
> recovered register (0.8-draft;
> `aee/freeze-aee-note.md`); the freeze
> record is `freeze.md` / `freeze.json`
> in this directory, and the spec's OSF
> contract registration is filed at the
> freeze under campaign decision E-1
> (`osf-spec-registration.md`). **Execution
> is a separate later act**: it runs as
> Phase-420 (DD-058-17), only after this
> freeze has merged, the registration's
> approval act has completed, and a
> separate execution order is given.
> Nothing has been tabulated, aligned, or
> computed by the freeze itself.
>
> **Arm B is blocked and out of scope.** The
> human-coder calibration arm of D-21 is
> blocked on the owner-held expert engagement
> (hold of 2026-10-12, unchanged; campaign plan
> Part 6 item 4 keeps every engagement of
> people with the owner). This spec covers
> arm A only, records arm B as
> blocked-out-of-scope in §1.3 and claim
> F058-C06, and designs **no** AI substitution
> for the human coders — that substitution is
> forbidden by the plan, and the Spec 023
> record is itself the proof that it answers a
> different question.
>
> The execution phase number was allocated
> at the freeze act: **Phase-420** (DD-058-17,
> completing DD-058-5). Phase-400 is Spec 036's,
> Phase-401 Spec 038's, Phase-402 Spec 037's,
> and Phase-403 Spec 039's; Spec 040 allocated
> none.

**Design source:** D-21, arm A, in the
experiment-design packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-21, read in full at this draft). The design
governs the substance; where the design is
silent and this draft must fix a rule to be
mechanical, the rule is labelled
DECIDED-BY-DRAFT in `adjudication.md` and is
OPEN for the freeze to overturn openly.

**Claim under test (residue only):**
`STUDY-SPEC-023/PHASE-132+383` — SETTLED —
CONTRADICTED: pilot exact-sequence agreement
0.20 against the frozen 0.80 floor; the
Phase-383 rerun's interval [0.10, 0.32] sits
far below it. Every coder was an AI agent of
a single model family — that disclosure is
part of the verdict. This spec tests no part
of that verdict. It answers the residue the
claim's record leaves open: *which* signs,
object types, and segmentation choices drove
the disagreement.

**AI disclosure:** this draft is produced by
an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per
constitution §VI.

---

## 1. The claim and the record it stands on

Spec 023 (FROZEN 2026-10-09) built a keyed
transcription layer over CISI Vols. 1–2 under
a blinded two-pass protocol. Its Stage P pilot
(Phase-132) transcribed 50 frame objects in
two independent passes (Pass A, Pass B), with
a third gold pass on a 10-object gold sample,
followed by adjudication. The pilot report
(`reports/phase132_pilot_report.md`) records,
computed from the on-disk records:

- Exact-sequence inter-pass agreement over
  all 50 objects: **0.20 (10/50)** in both P
  and M space, against the frozen stop-rule
  floor of **0.80** — the stop-rule **FIRED**
  and the build stopped; no tranche was
  proposed and no dataset was published.
- Per-token agreement over all 50 objects:
  **0.4798 (95/198)**; on the gold sample
  0.4286 (18/42).
- Gold per-sign error estimator: **0.05
  (2/40)** — the error arm of the stop-rule
  did not fire (the condition is strictly
  greater than 0.05).
- All three gold-scope release gates failed
  (exact-sequence 0.10 < 0.90; per-token
  0.4286 < 0.95; estimator 0.05 > 0.02).
- Pass token totals: Pass A 191, Pass B 190,
  gold pass 40, adjudicated final 189.
- UNK shares: Pass A 39.3% (75/191), Pass B
  38.9% (74/190), gold 42.5% (17/40),
  adjudicated final 40.7% (77/189); the
  adjudicated UNK + crosswalk-unmapped share
  is 49.2% (93/189).
- Adjudication disagreement taxonomy over
  the 50 adjudication records: 162
  disagreements — identity 93, legibility 45,
  count 11, key 10, orientation 2, order 1.
  Only 5 of 50 objects had zero
  disagreements.
- Frame as drawn: 50 objects — Mohenjo-Daro
  25, Harappa 15, Lothal 6, Kalibangan 4;
  object types as recorded: Seals 34,
  Tablets 11, unrecorded 5; gold sample 10
  objects (seed 20261009).

Phase-383 (Spec 026 rerun contract) rescored
the pilot from the on-disk coding records
with the original metrics module: every
original point value reproduced exactly, and
the bootstrap interval for exact-sequence
agreement is **[0.10, 0.32]** (B = 9,999,
seed 20261011). Its verdict, in the Spec 026
taxonomy: **CONTRADICTED** (bounded claim:
this AI coding basis at this protocol can
produce a publishable keyed transcription
layer). Its origin-group audit records that
all coding roles in the pilot were executed
by AI agents of **one** model family, so the
agreement statistics measure intra-origin
consistency, not independent corroboration.

The claim's lane-2 record
(`STUDY-SPEC-023/PHASE-132+383`, adopted
2026-10-13) states what remains not
understood, in the words this spec answers:
"Why the passes disagreed is not understood
at the level of mechanism: no named-human
account exists of which signs, objects or
segmentation choices drive the disagreement,
and the program has not produced one." Two
further open points in that text are **not**
this spec's questions and are excluded by
§8: whether the 0.80 floor is the right bar,
and whether a clarified codebook would
improve agreement. Both are asserted in
discussion and tested nowhere; neither is
tested here.

### 1.1 The question, in plain words

The two passes disagreed on 40 of 50 objects.
Was that disagreement spread evenly over
everything the passes read — or did a small
set of signs, one kind of object, or one
kind of reading choice (where to cut a
sequence into signs) produce most of it?
Nobody has ever tabulated the recorded
passes to find out. This spec tabulates
them, under rules fixed here in advance, and
records where the disagreement lives — or
records, in pre-written words, that it does
not localise anywhere.

### 1.2 The hypothesis and its falsifier

**Hypothesis** (design D-21, arm A, verbatim
in substance). The disagreement is
concentrated, not uniform — a minority of
signs or object types accounts for the
majority of sequence mismatches.

**Falsifier** (campaign statement, governing
at execution). The recorded pilot passes do
not localise the disagreement to signs,
object types, or segmentation choices: the
mismatch events distribute across signs and
objects in proportion to their frequencies,
and no locus rule in §5 fires. That outcome
is recorded as **NOT LOCALISED** (§5.2), with
the same prominence as any localisation.

### 1.3 Arm B — blocked, out of scope

D-21 arm B (the human calibration set: 30
objects / 212 tokens, human-derived
reference transcriptions, two independent
human expert coders blinded to each other
and to the references, bars of at least 95%
per-token and at least 85% exact-sequence
agreement) is **not** specified here. It is
blocked on human expert coders: the program
funds a paid calibration set (owner decision
2026-10-10), and the expert-engagement
letters that would recruit the coders are
HELD by the owner (2026-10-12; the campaign
plan of 2026-10-21 carries the hold
unchanged and keeps any new engagement of
people as the owner's own gate, Part 6
item 4). Unblocking act: the owner lifts
that hold and an engagement is made, under
its own planning gate. No part of arm B can
be substituted with AI coders, and this spec
designs no substitute (claim F058-C06).

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

### 2.1 Committed records of record

| Input | Pin / state |
|---|---|
| Spec 023 specification (`specs/023-keyed-transcription-layer/spec.md`) — the frozen protocol, §5.6 freeze block comparison space, alignment, and gates | SHA-256 `c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2` (recomputed at this draft from `main` @ `83b6a563`) |
| Phase-132 pilot metrics (`reports/phase132_pilot_metrics.json`) | SHA-256 `e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554` (recomputed at this draft) |
| Phase-132 pilot report (`reports/phase132_pilot_report.md`) | SHA-256 `e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00` (recomputed at this draft) |
| Pilot frame (`data/keyed_transcription/phase132_pilot_frame.json`) — 50 objects with canonical key, site, recorded object type, gold flag | SHA-256 `a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea` (recomputed at this draft) |
| Pilot dataset, build record (`data/keyed_transcription/phase132_pilot_dataset_v1.json`) — adjudicated final sequences only; content hash of record `7bdc73f5…` in its meta file | SHA-256 `adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400` (recomputed at this draft) |
| Pilot dataset meta (`data/keyed_transcription/phase132_pilot_dataset_v1_meta.json`) | SHA-256 `b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4` (recomputed at this draft) |
| Phase-383 results (`reports/phase383_results.json`) | SHA-256 `4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334` (recomputed at this draft) |
| Phase-383 report (`reports/phase383_report.md`) | SHA-256 `9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca` (recomputed at this draft) |
| Phase-132 metrics module (`backend/scripts/phase132_metrics.py`) — the frozen P-space derivation, alignment, and store loader this spec reuses unchanged | SHA-256 `238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984` (recomputed at this draft) |
| Phase-383 rescoring module (`backend/scripts/phase383_pilot_rescoring.py`) — the precedent for rescoring from the on-disk records with the original module imported, not reimplemented | SHA-256 `b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec` (recomputed at this draft) |
| Crosswalk v1 (`data/crosswalks/parpola_mahadevan_crosswalk_v1.json`) | SHA-256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` (recomputed at this draft; identical to the value the pilot records themselves carry) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. The pin is stated from a fresh recompute because the pilot report's own anchors assertion (`eccea6d5…`, the frozen value of 2026-10-09) no longer recomputes against the current file — the same stale-pin caution Spec 042's draft recorded. |

### 2.2 The pilot-pass record set — the design's premise, stated exactly

The design says arm A re-analyses "the
recorded Phase-132 pilot passes (both
passes' codings are on record)". Stated
exactly, the record is split:

- **Committed in the repository:** the
  pilot's aggregate and per-object metrics
  (lengths, exact-match flags, match counts
  — not sequences), the frame, the
  adjudicated final dataset, and the two
  reports (§2.1).
- **Not committed:** the per-pass codings
  themselves. Pass A, Pass B, the gold pass,
  and the adjudication records live only in
  the Phase-132 local store
  (`corpora/downloads/cisi_image_layer/phase132_pilot/`,
  gitignored), in the layout the frozen
  metrics module's loader defines:
  `frame.json`; `pass_a/<canonical-key>.json`
  × 50; `pass_b/<canonical-key>.json` × 50;
  `pass_gold/<canonical-key>.json` × 10;
  `adjudication/<canonical-key>.json` × 50;
  `effort_log.csv`. The pilot report's §9
  inventory (50 Pass A records, 50 Pass B
  records, 10 gold-pass records, 50
  adjudication records, effort log of 320
  events) is the inventory of record. Both
  the Phase-132 metrics and the Phase-383
  rescoring were computed from that store;
  neither was computed from committed files.

This draft does **not** repair that split by
substituting another source: the adjudicated
final dataset cannot stand in for the two
passes (it is their adjudicated product, not
either pass), and the metrics file's
per-object flags cannot yield sign-level or
segmentation-level tabulations. Instead,
step 0 (§3) makes production of the store
record set — inventoried, hashed, and proven
to reproduce the committed metrics exactly —
a fail-closed gate. If the set cannot be
produced intact, this spec closes at step 0
with its pre-written wording (§5.2), and that
closure is a result: it converts the design's
premise into a measured statement about what
the program's record actually holds. The
defect and its handling are recorded in
`adjudication.md` §2.

Plate images, renders, and crops are **not**
inputs to this spec at any point. Arm A is a
re-analysis of recorded codings; it performs
no transcription and consults no image.

## 3. Step 0 — gates before any localisation quantity (fail-closed)

Execution runs these checks in order, before
any mismatch event is tabulated. A failure
stops the execution in the class named;
nothing is repaired at run time.

- **0.1 Committed-record integrity.** Every
  §2.1 input hashes to its freeze-record
  value. A mismatch stops the run as
  **INVALID**.
- **0.2 Pilot-pass record production.** The
  Phase-132 store record set of §2.2 is
  produced at the execution venue and
  inventoried against the pilot report's §9
  inventory: `frame.json`, 50 Pass A records,
  50 Pass B records, 10 gold-pass records,
  50 adjudication records, and
  `effort_log.csv`, keyed by the frame's 50
  canonical keys (gold records keyed by the
  10 gold keys). A per-file SHA-256 manifest
  of the produced set is computed and
  recorded with the outcome. If the set
  cannot be produced, or any expected record
  is missing, the execution closes at this
  gate as **PILOT-PASS RECORDS NOT
  PRODUCIBLE** (§5.2 wording), unscored, and
  no localisation quantity is computed.
  Production is a records act only: no
  record is edited, completed, or
  re-created; a re-created record is not
  the record.
- **0.3 Frame identity.** The produced
  store's `frame.json` frame list equals the
  committed pilot frame (§2.1) exactly — the
  same 50 canonical keys with the same site,
  recorded object type, and gold flag per
  key. A mismatch stops the run as
  **INVALID**: the produced records are not
  the pilot's frame.
- **0.4 Reproduction of the committed
  metrics.** The frozen metrics module
  (§2.1, imported unchanged, per the
  Phase-383 precedent) computes metrics from
  the produced store, and the computed
  values equal the committed metrics file
  exactly: exact-sequence agreement 0.20
  (all-50, P and M), per-token agreement
  0.4798 (all-50) and 0.4286 (gold),
  gold estimator 0.05, pass token totals
  191 / 190 / 40 / 189, and every per-object
  exact flag and match count. Any mismatch
  stops the run as **INVALID** — the
  produced set is not the record set the
  pilot's published numbers came from, and
  no localisation proceeds on an unproven
  record set.
- **0.5 Adjudication-taxonomy cross-check.**
  The disagreement taxonomy recomputed from
  the produced adjudication records equals
  the pilot report's §4(c) counts exactly:
  identity 93, legibility 45, count 11,
  key 10, orientation 2, order 1, total 162.
  A mismatch stops the run as **INVALID**.
  (The taxonomy is an identity check on the
  produced records here — it is not an input
  to the §4 tabulations; DD-058-3.)
- **0.6 Analysis census.** The mismatched
  population is enumerated from the
  reproduced per-object flags: the objects
  whose Pass A and Pass B P-sequences differ
  — 40 objects on the record as committed.
  A reproduced count other than 40 is
  already excluded by gate 0.4; this gate
  publishes the census (the 40 keys, with
  site, recorded object type, gold flag,
  and both sequence lengths) as the
  population every §4 share is taken over.
  The gold pass and the adjudicated
  sequences are not inputs to the primary
  analysis (DD-058-2).

## 4. The localisation method (mechanical)

The analysis runs on the gate-proven record
set only. Every definition below is stated
so that two independent implementations of
this section, given the same record set,
produce the same tables.

### 4.1 Comparison space and sequences

For each of the 50 frame objects, Pass A's
and Pass B's token records (ordered by
their recorded `position`) are converted to
P-space value sequences by the frozen
metrics module's derivation, unchanged:
each token's value is the crosswalk-v1
primary P counterpart of its matched M
(highest-confidence row, tie → lowest P
number); `UNK` compares as `UNK`; an M with
no crosswalk row compares as
`UNMAPPED:<M_ID>`. P space is the primary
space (Spec 023 §5.6 freeze block). The same
tabulations computed in M space are reported
as a stated sensitivity, descriptive only —
they move no headline (DD-058-4).

### 4.2 Alignment and mismatch events

For each mismatched object, the two
P-sequences are aligned by the frozen
module's minimum-edit alignment (unit cost;
backtracking prefers the diagonal —
match/substitution — over deletion over
insertion at equal cost). The alignment is
a list of columns, each holding a Pass A
value, a Pass B value, or a gap on one side.

- A **mismatch event** is an alignment
  column whose two sides are not equal
  values present on both sides. Events are
  typed mechanically:
  - **SUBSTITUTION** — both sides present,
    values unequal. The event involves both
    values: the ordered pair (A value,
    B value).
  - **INDEL** — exactly one side present
    (an insertion in one pass or a deletion
    relative to the other; the alignment
    does not distinguish, and this spec does
    not pretend to). The event involves the
    one present value.
- The **event total E** is the count of
  mismatch events over all 40 mismatched
  objects. Every share in §5 is a share of
  E unless its definition says otherwise.
  (On the committed record, E is not yet
  known: the metrics file records 95 matched
  aligned pairs over a denominator of 198,
  so E is determined by the produced
  alignments at execution — one more reason
  no quantity is stated at draft.)
- **First divergence.** Per mismatched
  object, the first mismatch-event column
  in alignment order, recorded with its
  1-based alignment position, its type, and
  the value(s) involved. The distribution of
  first-divergence positions and the signs
  at first divergence are tabulated and
  reported (§6) — descriptive mechanism
  detail the design asks for ("localise the
  first position of divergence and the signs
  involved"); they are not verdict-bearing.

### 4.3 Tabulations

- **T1 — by sign.** For every distinct
  P-space value v, its **involvement
  count**: the number of mismatch events
  involving v (a substitution counts once
  for each of its two values; an indel
  counts once for its present value).
  Values are ranked by involvement count,
  ties broken by value string ascending —
  the ranking is total and deterministic.
  The **top-10 share** is the summed
  involvement of the 10 highest-ranked
  values divided by the summed involvement
  over all values. (With substitutions
  counting for two values, summed
  involvement exceeds E; the share is taken
  over summed involvement, so the design's
  "share of all mismatches" is computed on
  the involvement basis throughout —
  DD-058-6.)
  The **frequency share** of those same 10
  values is their share of all tokens
  across both passes' full sequences (Pass A
  + Pass B token streams over all 50
  objects, P space: the recorded totals are
  191 + 190 = 381 tokens).
- **T2 — by object type.** Mismatch events
  are grouped by the frame's recorded
  object type of the object they occur in:
  **Seals**, **Tablets**, or **Unrecorded**
  (the frame records no type for 5 objects;
  the category is carried as recorded and
  never back-filled, per Spec 023 K3). Per
  type: its event count and share of E, its
  object count and share of the 50 frame
  objects, and its mismatched-object count.
- **T3 — by divergence type.** Mismatch
  events grouped by §4.2 type: SUBSTITUTION
  count and share of E; INDEL count and
  share of E. The INDEL share is this spec's
  registered proxy for segmentation: two
  passes that cut the same glyph stream
  differently produce length differences,
  which the alignment surfaces as indels.
  §8 states the limit of that proxy plainly.

### 4.4 The UNK question, settled in advance

UNK is the single largest value class in
both passes (39.3% / 38.9% of tokens). The
primary tabulations count every recorded
value as recorded — UNK and
`UNMAPPED:<M_ID>` values included — because
the design tabulates the mismatches the
pilot actually produced, and removing the
largest class after the fact would redefine
the pilot. Alongside the primary tables, a
pre-registered **descriptive secondary**
recomputes T1–T3 excluding every event
involving an UNK value on either side. The
secondary is reported wherever the primary
is; it never carries the headline, and no
outcome wording is drawn from it
(DD-058-7). If the sign locus fires (§5)
only with UNK in the count, the headline
wording says so (§5.2).

## 5. Criteria fixed in advance

### 5.1 Locus rules

A **locus fires** under exactly one of:

- **SIGNS** — the design's CONCENTRATED
  criterion, verbatim: the top-10 values by
  involvement (T1) account for **at least
  50%** of summed involvement. The design's
  companion states are computed and
  reported with the result: **UNIFORM** if
  the top-10 share is within **10 points**
  of those values' frequency share;
  **BETWEEN** otherwise when the 50% line
  is not met.
- **OBJECT TYPES** — one recorded object
  type (Seals or Tablets; the Unrecorded
  category cannot fire this locus —
  DD-058-8) accounts for **at least 50%**
  of E **and** its event share exceeds its
  share of the 50 frame objects by at
  least **10 points** (the design's
  10-point band, applied as an enrichment
  margin, so a type cannot "localise" the
  disagreement merely by being most of the
  frame — Seals are 34 of 50 objects).
  The design fixes no numeric rule for
  object types; this rule is
  DECIDED-BY-DRAFT (DD-058-8) and OPEN for
  the freeze.
- **SEGMENTATION** — INDEL events (T3)
  account for **at least 50%** of E. The
  design names segmentation as a tabulation
  axis without a numeric rule; the 50%
  line mirrors its sign criterion.
  DECIDED-BY-DRAFT (DD-058-3) and OPEN for
  the freeze.

### 5.2 The headline outcome and its pre-written wordings

The execution's headline is exactly one of
the following, determined mechanically from
the set of loci that fire:

- **LOCALISED TO SIGNS** — only the sign
  locus fires: "Re-analysed under Spec 058,
  the disagreement between the two recorded
  Phase-132 pilot passes is localised to
  signs: the 10 most-involved signs account
  for [s]% of all mismatch involvement, led
  by [values]. The pilot's failure stands
  exactly as recorded; this account names
  where its disagreement sits, in this
  pilot's passes, and says nothing about
  human coders."
- **LOCALISED TO OBJECT TYPES** — only the
  object-type locus fires: "Re-analysed
  under Spec 058, the disagreement between
  the two recorded Phase-132 pilot passes
  is localised to object types: objects
  recorded as [type] carry [s]% of all
  mismatch events on [n] of 50 frame
  objects. [Census sentence.] The pilot's
  failure stands exactly as recorded; this
  account says nothing about human coders."
- **LOCALISED TO SEGMENTATION** — only the
  segmentation locus fires: "Re-analysed
  under Spec 058, the disagreement between
  the two recorded Phase-132 pilot passes
  is localised to segmentation choices, as
  registered in Spec 058 §4.3: [s]% of
  mismatch events are insertion/deletion
  events — the passes differ more in how
  they cut sequences than in which signs
  they name. The pilot's failure stands
  exactly as recorded; this account says
  nothing about human coders."
- **LOCALISED TO MULTIPLE LOCI** — two or
  more loci fire (a combination class the
  draft adds because the three rules are
  not mutually exclusive — DD-058-9):
  "Re-analysed under Spec 058, the
  disagreement between the two recorded
  Phase-132 pilot passes is localised to
  [the firing loci, named]: [per-locus
  shares]. No single locus accounts for
  the disagreement on its own. The pilot's
  failure stands exactly as recorded; this
  account says nothing about human coders."
- **NOT LOCALISED** — no locus fires (the
  falsifier's outcome): "Re-analysed under
  Spec 058, the disagreement between the
  two recorded Phase-132 pilot passes does
  not localise: no sign set, object type,
  or segmentation proxy meets the frozen
  criteria (top-10 sign share [s]% against
  a frequency share of [f]% — [UNIFORM /
  BETWEEN]; largest object-type event share
  [t]%; indel share [i]%). The disagreement
  is distributed across the passes'
  readings in proportion too close to
  their frequencies to name a locus. The
  pilot's failure stands exactly as
  recorded."

If the sign locus fires and UNK is among
the top-10 values, the headline paragraph
of any signs-carrying outcome adds, in its
first paragraph: "UNK — the passes' 'no
identification' value — is itself among the
most-involved values ([u]% of involvement);
the localisation is in part a localisation
to illegibility, stated as such."

Step-0 and stop wordings:

- **PILOT-PASS RECORDS NOT PRODUCIBLE**
  (gate 0.2): "Spec 058 closes at step 0:
  the recorded Phase-132 pilot passes could
  not be produced as a complete record set
  ([inventory shortfall as found]). The
  committed repository record carries the
  pilot's metrics, frame, and adjudicated
  dataset, but not the per-pass codings
  arm A exists to re-analyse. No
  localisation quantity was computed, and
  no substitute source was used. Design
  D-21 arm A remains unrun; its unblocking
  act is the preservation of the pilot-pass
  record set as a committed, hashed record."
- **INVALID** (gates 0.1 / 0.3 / 0.4 /
  0.5): "Spec 058 stops as INVALID at gate
  [gate]: [the observed mismatch]. No
  localisation quantity was computed. The
  Spec 023 pilot record stands exactly as
  recorded; the failure is in this spec's
  inputs, not in the pilot."

## 6. Reporting obligations

Every product of an execution carries:

1. the step-0 record — each gate's verdict,
   the produced-set manifest (per-file
   SHA-256) when gate 0.2 passes, and the
   reproduction comparison of gate 0.4;
2. the §3 gate-0.6 census (the 40 mismatched
   objects with site, recorded type, gold
   flag, sequence lengths);
3. tables T1 (full ranked involvement
   table, with frequency shares), T2, T3 —
   primary (P space) and the §4.4
   descriptive secondary, with the M-space
   sensitivity stated beside T1;
4. the first-divergence table (per
   mismatched object: position, type,
   value(s)) and its distribution summary;
5. the per-locus verdicts with the numbers
   that decided them, the headline word of
   §5.2, and the headline paragraph in its
   pre-written form with quantities filled;
6. the fence sentence: "This account is
   about why two recorded AI pilot passes
   disagreed. It is not evidence about
   human transcription, and it changes no
   verdict."

Deliverables at execution: a results JSON
(gate record, manifest reference, census,
T1–T3, first-divergence table, locus
verdicts), a report under these rules, the
experiment-graph node (H15/H23, registered
and verified before the run), the outcome
append in this directory, and the LEDGER
entry (H1). Foundation check (H21) after
the execution phase: 0 failures, or the
outcome record says why not. Anchors
asserted byte-identical before and after.

## 7. Controls and named confounders

- **Alignment determinism.** The frozen
  alignment's tie-breaking (substitution
  preferred over indel at equal cost) is
  part of the machinery of record; a
  different alignment could type the same
  disagreement differently. The control is
  identity: the module is imported
  unchanged and gate 0.4 proves it
  reproduces the pilot's own numbers before
  it types a single event.
- **UNK mass.** With ~39% of each pass's
  tokens UNK, UNK-involved events may
  dominate every tabulation. §4.4 settles
  the handling in advance; the descriptive
  secondary and the mandatory UNK sentence
  (§5.2) keep the dominance visible rather
  than letting it pass as a sign finding.
- **Frame composition.** The pilot frame is
  Mohenjo-Daro-heavy (25 of 50) and
  seal-heavy (34 of 50), with 5 objects of
  unrecorded type. Object-type shares are
  therefore read against the frame's own
  composition (the §5.1 enrichment margin),
  and every type statement carries the
  census with it. Site is tabulated in the
  census but is not a locus under this
  spec: the design names signs, object
  types, and segmentation, and no site
  rule is invented here.
- **Small population.** 40 mismatched
  objects is the whole evidence base. The
  criteria are shares, not significance
  tests; no interval is placed on a share,
  and no share is quoted without its
  counts.
- **One origin group.** Both passes are one
  model family's codings (Phase-383 audit).
  A localisation describes this pilot's
  passes; it is not a finding about
  transcription passes in general, and §8
  binds the wording.
- **Crosswalk derivation.** P values are
  derived through crosswalk v1's primary
  map, identically for both passes (Spec
  023 freeze block: the derivation "cannot
  manufacture agreement"). `UNMAPPED:<M_ID>`
  values are distinct per M by construction,
  so unmapped tokens can be involved in
  events but can never spuriously match.

## 8. Epistemic limits (binding on all outputs)

1. **The contradicted verdict stands.**
   `STUDY-SPEC-023/PHASE-132+383` remains
   CONTRADICTED, exactly as recorded. A
   localisation — or a NOT LOCALISED —
   appends a mechanism account to the
   claim's record as a dated entry beside
   the frozen one; it does not soften,
   re-open, or re-adjudicate the verdict,
   and no output may present it as doing so.
   Design D-21 says this in advance: arm A
   "changes no verdict (the pilot still
   failed, and stays failed)".
2. **Nothing about humans.** Every coder in
   the pilot was an AI agent of a single
   model family. No outcome under this spec
   is evidence about human coders, expert
   or otherwise. The human question is arm
   B's, it is blocked, and it stays blocked
   (§1.3).
3. **Nothing about the 0.80 floor or the
   codebook.** Whether the floor was the
   right bar, and whether a clarified
   codebook would raise agreement, are
   named open points in the claim's record
   that this spec does not test. A
   localisation may inform a future
   protocol revision; it does not evaluate
   one.
4. **Segmentation is a proxy here.** From
   token sequences alone, an indel event
   cannot be separated into "the passes cut
   the same glyphs differently" and "one
   pass recorded a sign the other omitted".
   The SEGMENTATION headline therefore
   means exactly what §4.3 registers — the
   indel share of mismatch events — and
   every output that uses the word carries
   that definition with it.
5. **The pilot frame only.** All statements
   are about these 50 objects, these two
   passes, this protocol. Nothing
   generalises to Stage T (never run), to
   other objects, or to other coders.
6. Negative, not-localised, step-0, and
   invalid outcomes publish with the same
   prominence as a localisation.

## 9. Risks and honest weaknesses

- **The record set may simply be gone.**
  The per-pass codings were never
  committed; they survive, if they survive,
  in one local store. Gate 0.2 exists
  because PILOT-PASS RECORDS NOT PRODUCIBLE
  is a realistic outcome of this design —
  and, if it fires, the honest product of
  this spec is the closure and its named
  unblocking act (preserving the record set
  as a committed, hashed record), not a
  quieter analysis of lesser inputs.
- **The headline may be an UNK finding.**
  Given the passes' UNK shares, the most
  likely localisation is to illegibility
  itself. §4.4 and §5.2 force that to be
  stated as what it is; a reader who wants
  named-sign findings may find the account
  thinner than its headline word suggests.
- **Event counts are unknown until the
  run.** Shares over an event total that
  cannot be stated at draft are less
  stable than the criteria's clean 50%
  lines imply; the counts travel with every
  share (§7) for exactly that reason.
- **Two draft-fixed rules carry the
  headline.** The object-type and
  segmentation criteria (§5.1) are this
  draft's constructions on design-silent
  points. They are labelled, reasoned, and
  OPEN — but a freeze that changes them
  changes what the headline can say, which
  is why they are freeze items and not
  execution details.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **PILOT-PASS RECORDS NOT PRODUCIBLE** —
  gate 0.2 fails. No quantity is computed.
- **INVALID** — gate 0.1, 0.3, 0.4, or 0.5
  fails.
- **LOCALISED TO SIGNS**, **LOCALISED TO
  OBJECT TYPES**, **LOCALISED TO
  SEGMENTATION**, **LOCALISED TO MULTIPLE
  LOCI**, or **NOT LOCALISED** — per §5,
  after all gates pass.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
   The script imports the frozen metrics
   module for derivation, alignment, store
   loading, and reproduction; it does not
   reimplement them.
2. **Step 0** (§3) — committed-record
   integrity; record-set production,
   inventory, and manifest; frame identity;
   metrics reproduction; taxonomy
   cross-check; census.
3. **Tabulations** (§4) — alignments, events,
   T1–T3, first divergence, descriptive
   secondary, M-space sensitivity.
4. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 12. What this spec is not

Not arm B, and not any substitute for it.
Not a re-coding, re-transcription, or new
pass over any object. Not a re-run or
re-adjudication of Spec 023 or Phase-383.
Not a Stage T proposal. Not a test of the
0.80 floor or of any codebook revision. Not
an authorisation to execute. It is a
re-analysis of two recorded pilot passes,
designed so that its honest outcomes —
including closing at step 0 because the
record set cannot be produced — are written
down before any event is tabulated.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
