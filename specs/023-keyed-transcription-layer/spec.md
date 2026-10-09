# Spec 023 — Keyed Transcription Layer over CISI Vols. 1–2 (PROPOSAL)

> ## ⚠ DRAFT — PROPOSAL FOR OWNER ADJUDICATION — NOT FROZEN ⚠
>
> This document is a **proposal**. It has not been
> approved, it freezes nothing, and it authorizes no
> work. No transcription, implementation, or study may
> cite this spec as authority until the owner approves
> it (in whole or in amended form) and a frozen copy is
> committed under a separate freeze commit, in the
> pattern of specs 019 / 021 / 022. Every quantity that
> is a proposal rather than a fact of record is marked
> **PROPOSED**. The numbered decision asks in §11 are
> the complete list of what the owner is being asked
> to decide.

**Status:** DRAFT PROPOSAL, drafted 2026-10-09 on
`spec/023-keyed-transcription-layer` (from origin/main
`a5b69c0b`). Owner instruction of record: "Draft the
Spec 023 keyed transcription-layer proposal"
(2026-10-09). The facts of record cited below are
quoted from committed results (Phase-124 / 125 / 127 /
128 / 131 reports and results JSONs; spec 018; the
Phase-130 intake pack) or computed at drafting time
from the Phase-124 local catalogue files, with the
computation stated where it occurs (Appendix A).
No transcription has been performed under this
proposal and no new statistic about any inscription
appears in it.

**Phase-numbering note:** this proposal claims **no
phase number**. It proposes a dataset build, not a
study. If approved, the build takes the next ledger
phase number at freeze time, and any study consuming
the layer takes its own later number and its own
frozen spec (§12).

**AI disclosure:** this proposal is drafted by an AI
agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI. The
transcription protocol it proposes (§5) is designed
for execution by transcribers blind to existing
transcriptions of the same objects; who or what the
transcribers are is part of what the pilot must make
measurable, not a premise (§5.6).

## 0. Context — the problem this proposal answers

Phase-125 (spec 019) compared anchor positional
profiles between the mayig/CISI compilation and the
Holdat compilation and returned a FINAL verdict:
**FAIL — DISAGREEMENT** (PRIMARY arm: 16 judgeable
pairs of 286; median TV **0.636931**). Phase-127
(spec 021) established that the disagreement is not
sampling noise (matched-size null median TV
**0.082613**, 95% interval 0.046665–0.131316; the
observed value was reached in **0 of 999**
replicates). Phase-131 (spec 022) then attempted
mechanism attribution — and its central arm could
not run:

- **Arm A (matched-object alignment) found that the
  legitimate Holdat↔CISI join is ~0.** The 179
  apparent CISI-ID namesakes between Holdat and the
  mayig layer validated to **0**: Holdat's
  `cisi_number` is Holdat-internal sequential
  numbering, not a CISI object ID (spec 019 §2.1,
  established as a fact of record before Phase-131
  ran). Catalogue cross-references: **0** usable.
  Shared artifact keys: **0**. The fallback content
  matcher — the only legitimate route left — matched
  **4 pairs (0 exact)** out of 32 eligible mayig
  inscriptions, with matched-object positional TV
  **NOT ESTIMABLE** (4 < the frozen minimum of 10).
- **Arm D (synthesis)** could therefore credit only
  composition (share **0.061321**) and reading
  direction (**0**), leaving a **residual unexplained
  share of 0.938679** — 93.9% of a real, non-noise
  disagreement that cannot currently be attributed
  to segmentation, substitution, insertion/deletion,
  or any other mechanism, because the objects on the
  two sides cannot be shown to be the same objects.

**The blocking defect is keying, not statistics.**
Every cross-compilation question this program has
asked since Phase-116 — do the compilations
transcribe the same objects the same way? where do
they differ, sign by sign? — reduces to a join, and
no legitimately keyed corpus layer exists on the
CISI side. The mayig layer (179 inscriptions) is the
only CISI-derived layer in hand; it is small
(1,003 tokens), and its object references resolve to
CISI objects only through the Phase-122 mapping, not
through a keying discipline of its own.

**What this proposal is:** a build, under owner
adjudication, of an image-derived transcription
layer over the CISI Vol. 1–2 scans already in hand,
in which **every record is keyed to the true printed
CISI object ID** — the key the plates themselves
carry — produced under a blinded two-pass protocol
with measured error rates, staged so the owner
decides scale only after the pilot has measured what
transcription actually costs and how accurate it is.

**Non-goals, registered in advance:**

- This is a **dataset proposal, not a study**. It
  computes no positional profile, no TV distance, no
  agreement statistic about any existing compilation,
  and no PRED evaluation. Any study consuming the
  layer requires its own frozen spec (§12).
- It changes **no anchor, no PRED verdict, no
  status** anywhere. The Phase-125 FAIL and spec
  020's NO stand untouched regardless of what the
  layer later shows.
- It does **not** create, and must never be described
  as creating, independence from the Mahadevan /
  Parpola sign-list tradition in the strong sense.
  §8 states the epistemic limits in full; they are
  part of the proposal, not a caveat to it.
- No plate image, page render, or crop is published
  at any stage. Publication, if approved (Decision
  Ask 4), is of sign sequences and metadata only,
  under the program's existing publication
  discipline.

## Epistemic boundaries

Assumptions and disciplines, declared:

- **K1 — The plates are the only source.** Every
  transcription record derives from the CISI Vol. 1–2
  plate photographs held in the local research store.
  No transcription is copied, adapted, or checked
  against Holdat, the mayig layer, ICIT, or any other
  existing transcription at production time (§5.5
  blindness). Existing transcriptions are comparison
  targets for *later studies*, never inputs.
- **K2 — Keys come from the plates, not from OCR.**
  The Phase-124 catalogue (7,705 photo rows) is the
  sampling frame and the locator (volume, printed
  page, photo box). The canonical key of a record is
  the printed CISI ID **as read from the plate
  caption by the transcriber**, verified against the
  catalogue row — not the catalogue's OCR-derived ID
  taken on trust (§4).
- **K3 — Nothing is back-filled.** A field the plates
  do not print is recorded as not printed / empty,
  per the Phase-124 premise correction (§4.2). No
  museum number, material, dimension, or period is
  imported from outside CISI at any stage.
- **K4 — Conflicts are data.** Where the published
  sign lists or the crosswalk disagree, the record
  carries the conflict flagged (§5.3). No conflict is
  silently resolved at transcription time, by either
  pass, or by adjudication; adjudication resolves
  *transcriber disagreement*, not *list disagreement*.
- **K5 — Every number about quality is measured, not
  assumed.** Error rates, agreement rates, and
  per-object effort exist only after the pilot
  measures them (§3.1). This proposal contains no
  timeline and no total-effort estimate, because the
  unit quantities are unknown until measured (§10).

## 1. Objective and deliverable definition

**Objective (proposed).** Produce a versioned,
provenance-complete transcription dataset over CISI
Vols. 1–2 in which:

1. every record is keyed to the true printed CISI
   object ID, volume-scoped (§4.1);
2. every sign token is identified against the
   published Parpola list with its crosswalk-v1
   Mahadevan counterpart recorded where one exists
   (§5.3);
3. every record is the adjudicated product of two
   independent, blinded transcription passes (§5);
4. the dataset conforms to intake schema v1 and
   carries dataset class `image_transcription`
   (§6);
5. quality is reported as measured quantities —
   inter-transcriber agreement and adjudicated
   per-sign error rate on a gold sample — against
   pre-registered gates (§5.6), not as adjectives.

**Deliverable (proposed).** A dataset directory in
the repository (sign sequences + metadata; no
images), a dataset report (frame, counts, measured
quality, coverage against §7's checks, ambiguity
log summary), and a local-store manifest in the
Phase-124 pattern (counts and schema only). The
plates, renders, and crops remain in the gitignored
local store throughout.

## 2. Source material and sampling frame (facts of record)

- **Scans in hand:** CISI Vol. 1 (= MASI 86,
  *Collections in India*, Joshi & Parpola 1987; 431
  scan pages) and CISI Vol. 2 (Shah & Parpola 1991;
  486 scan pages) — **917 pages** total, held as
  in-copyright local research copies, never
  redistributed (Phase-124 record).
- **Phase-124 catalogue:** 7,705 photo rows over the
  two volumes (Vol. 1: 3,320; Vol. 2: 4,385), 22
  fields per row, sample field accuracy 98.9%
  (87/88). Local store:
  `corpora/downloads/cisi_image_layer/` (gitignored).
- **Sampling frame (computed at drafting time from
  the catalogue CSVs, 2026-10-09):** **3,494
  volume-scoped distinct objects** (Vol. 1: 1,475;
  Vol. 2: 2,019). The volume scoping is not cosmetic:
  the raw printed ID `H-311` occurs in **both**
  volumes, so a bare printed ID is not a unique key
  (§4.1). Frame composition is tabulated in
  Appendix A: Mohenjo-Daro 1,480 objects and Harappa
  1,347 objects dominate; Lothal (243) and Kalibangan
  (112) provide the additional-site depth that §7
  requires; seals (2,016) and tablets (866) are the
  principal object types, with graffiti objects (395)
  treated as a separate class (§3.2).
- **Scale reference:** the mayig layer — the only
  existing CISI-derived transcription layer — covers
  179 of these 3,494 objects (1,003 tokens, 182
  distinct P signs, ≈5.6 tokens per inscription;
  Phase-122 record). The frame is ~19.5× its object
  count.

## 3. Staged scope (all sizes PROPOSED)

Scope is staged so that each stage's cost is known
before the next is authorized. No stage beyond the
pilot is authorized by approval of the pilot.

### 3.1 Stage P — Pilot (PROPOSED: ~50 objects)

- **Frame (PROPOSED):** 50 objects drawn
  deterministically from the catalogue frame
  (printed-page order within stratum, every-*k*-th
  selection with the rule and seed recorded in the
  dataset report), stratified as: **25 Mohenjo-Daro,
  15 Harappa, 10 Lothal-or-Kalibangan** — ≥2 sites
  with margin, per §7's design constraint — spanning
  seals and tablets, and **including ~10 objects from
  the 179-object mayig overlap set** (§3.2 T1) so
  pilot error measurement also yields a first
  keyed comparison set for later studies.
- **The pilot's explicit jobs:** (i) measure
  per-object effort (wall time per pass, per
  adjudication) and tokens per object; (ii) measure
  inter-transcriber agreement and the adjudicated
  per-sign error rate against the §5.6 gates;
  (iii) exercise the full pipeline — keying,
  blindness, adjudication, intake validation, dedup —
  end to end at small scale; (iv) produce the
  measured unit quantities on which the Stage-T
  scale decision (Decision Ask 2) is made.
- **Pilot stop-rule (PROPOSED):** if the pilot's
  post-adjudication per-sign error rate exceeds
  **5%**, or exact-sequence inter-pass agreement is
  below **80%**, the build **stops**: no tranche is
  proposed, the pilot dataset and its measurements
  are reported as found, and the question returns to
  the owner. A stopped pilot is a result, not a
  failure of process.

### 3.2 Stage T — Targeted tranche (PROPOSED, subject to the scale gate)

- **T1 — mayig-overlap core (PROPOSED):** all **179**
  CISI objects corresponding to the mayig layer per
  the Phase-122 mapping, re-transcribed from the
  plates under §5. Payoff: the first keyed,
  provenance-complete matched-object set against an
  existing CISI-derived layer, covering every sign
  the mayig layer attests.
- **T2 — sign-targeted expansion (PROPOSED):** the
  target sign set is the union of (a) the **44
  `pending_non_sa_validation` anchors** (M-space list
  of record: Phase-128 dossiers; Appendix B) and (b)
  the **16 Phase-125 PRIMARY judgeable signs** —
  **59 distinct M signs** (the sets intersect in
  exactly one sign, M072). Sign content cannot be
  known before transcription, so T2 is a **frozen
  sequential rule**, not a sign-selected sample:
  within site strata (Mohenjo-Daro, then Harappa,
  then Lothal/Kalibangan), transcribe catalogue
  objects in printed-page order — seals and tablets;
  graffiti-class objects excluded from T2's main arm
  and recorded as excluded — until each target sign
  reaches the Phase-125 judgeability floor (**≥8
  tokens** in this layer) or the tranche cap
  (**PROPOSED: 600 objects beyond T1**) is exhausted.
  Per-sign coverage is reported as found; signs that
  do not reach the floor within the cap are listed as
  not covered, and chasing them past the cap requires
  a new owner decision.
- **Scale / no-scale gate:** Stage T runs only on a
  separate owner decision (Decision Ask 2) taken
  **after** the pilot report exists, with the pilot's
  measured unit effort and error rates in hand.

### 3.3 Out of scope at every stage

CISI Vol. 3.x in any form (no lawful digital copy
exists; print acquisition and scanning are off the
table by standing owner decision); objects whose
only catalogue presence is in the Addenda; any
object the plates show without a legible printed ID
(§4.3 ambiguity log, not a record).

## 4. Keying discipline

### 4.1 Canonical key

The canonical key of a transcription record is the
**printed CISI object ID, volume-scoped**:
`cisi:v{volume}:{printed_id}` (e.g.
`cisi:v1:M-67`). The volume scope is mandatory: the
frame computation (§2) found the raw ID `H-311` in
both volumes. The printed ID is read from the plate
caption by the transcriber and checked against the
catalogue row for that photo (K2); a disagreement
between plate reading and catalogue OCR is itself
logged (§4.3) and the **plate reading governs**.

### 4.2 Secondary fields — only what CISI prints

Per record: `site` and `object_type` from the plate
header (as captured in the catalogue); photo key
(ID + side + `bis` flag), printed page, and PDF page
from the catalogue row. **Museum number, material,
and dimensions are NOT recorded**: CISI plates do
not print them per object (Phase-124 premise
correction — the fields stand empty / "not printed
per object in CISI plates", never back-filled from
outside sources). Collection scope is a volume-level
fact and is recorded at dataset level only.

### 4.3 Prohibitions and the ambiguity log

- **Holdat's `cisi_number` is expressly prohibited
  as a join key, a record field, or a selection
  criterion**, in any stage, in either direction. It
  is Holdat-internal numbering (spec 019 §2.1). No
  record in this layer carries it.
- **Ambiguity log (first-class dataset artifact):**
  every object whose printed ID is duplicated within
  its volume beyond the catalogue's `bis` handling,
  illegible, contradicted between caption and plate
  header, or colliding in any way the keying rule
  does not mechanically resolve, is entered in the
  log with its catalogue row reference and the
  reason. Ambiguous objects are **excluded from the
  dataset and counted** — never keyed by guess,
  never silently dropped.

## 5. Transcription protocol (PROPOSED)

### 5.1 Reading-order declaration, before transcription

For each object, before any sign is identified, the
record declares: which photograph(s) were transcribed
(catalogue side `A` = original object, `a` = modern
impression, both where both exist), and the
**orientation convention applied**: the primary
sequence is recorded in **impression orientation**
(the text as a reader of the stamped impression
reads it), with the seal-face sequence being its
exact reversal, derivable mechanically and recorded
as a derived field — never as a second, independent
transcription. (Decision Ask 5 offers the owner the
face-primary alternative; whichever is chosen is
declared once, dataset-wide, in the dataset
provenance.) A record without a prior orientation
declaration is invalid under §6 validation.

### 5.2 Sign identification

Each glyph token is identified against the published
Parpola sign list. The token record carries: the P
ID; the glyph's plate region reference (catalogue
photo + position index); a legibility grade
(clear / partial / trace); and the §5.4 uncertainty
fields. A glyph that cannot be identified is
recorded as the `UNK` sentinel (spec 018 convention)
with its legibility grade — counted, positioned, and
never dropped, because the unmapped-token share is
an evaluability quantity (§7).

### 5.3 Crosswalk recording — conflicts flagged, never resolved

Each P-identified token is mapped through
**crosswalk v1** (Phase-122: 762 P↔M pairs; 372
high-confidence; 383 conflict pairs; 4 P signs
unmapped — P000, P225, P261, P358). The token record
carries the M counterpart where the crosswalk
provides one, plus a `crosswalk_conflict` flag where
the pair is among the 383 conflict pairs, and
`crosswalk_unmapped` where none exists. **No
conflict is resolved at transcription time** — not
by a transcriber, not by adjudication (K4). Which
side of a conflict a later study uses is that
study's frozen choice, made with the flags visible.

### 5.4 Damage and uncertainty as first-class fields

Per token: `legibility` (§5.2); per inscription:
`damage_notes` (free text, transcriber's), `partial`
flag where the text is visibly incomplete (broken
edge, missing corner), and `orientation_basis`
(§5.1). Uncertainty is represented in the data,
never absorbed into a best guess: a partial glyph is
a graded token, not a silent identification.

### 5.5 Two passes, blinded, plus adjudication

- **Pass A and Pass B are independent.** Each
  transcriber works from the plate images alone.
  Neither sees the other's transcription, the
  adjudicated record, **or any existing transcription
  of the same object** (Holdat, mayig, ICIT-derived,
  or any other) at any point before both passes are
  committed. Blindness is a protocol property, logged
  per object (pass timestamps + a blindness
  attestation field in the record provenance).
- **Disagreement adjudication.** Where the passes
  differ — token identity, token count, order,
  legibility grade — an adjudicator (not a pass
  transcriber for that object) examines the plate
  and rules. Every disagreement and its ruling is
  preserved in the record's adjudication log;
  the pre-adjudication pass values are retained in
  the local store and summarized (counts only) in
  the dataset report. Adjudication may rule a token
  `UNK`; it may not import an outside transcription
  as evidence (K1).
- **No silent convergence.** Pass agreement is a
  measured output (§5.6), not a target the passes
  may coordinate toward.

### 5.6 Gold sample, quality gates, and the error rate (PROPOSED)

- **Gold sample (PROPOSED):** a random **20%** of
  each stage's objects (seed recorded) receives a
  third, independent transcription by a transcriber
  who did neither pass, followed by adjudication.
  The per-sign error rate is estimated on the gold
  sample as the share of adjudicated tokens whose
  final value differs from the two-pass adjudicated
  value's expectation under the frozen estimator
  defined at freeze time — the operational estimator
  (three-way token agreement decomposition) is
  specified in the freeze commit, not improvised
  after data exists.
- **Quality gates (PROPOSED, for owner adjudication
  as Decision Ask 3):** a stage's dataset is
  released only if, on its gold sample:
  (i) exact-sequence inter-pass agreement ≥ **90%**
  of objects; (ii) per-token inter-pass agreement ≥
  **95%**; (iii) adjudicated per-sign error rate ≤
  **2%**. A stage that fails a gate is reported with
  the failing measurements and is **not** released as
  a dataset; its records remain local pending an
  owner decision.
- **Pilot stop-rule** as §3.1 (error > 5% or
  exact-sequence agreement < 80% stops the build).

## 6. Data model — intake schema v1 conformance

Every record conforms to **intake schema v1**
(`data/intake/intake_dataset_schema_v1.json`,
Phase-130), dataset class **`image_transcription`**:

- `inscription_id` = the §4.1 canonical key.
- `site`, `object_type`: as printed (§4.2);
  `period` and `context`: absent (not printed per
  object in CISI), recorded as the schema's
  optional-but-declared absence, never back-filled.
- `provenance.source_reference` (schema-required):
  volume + printed page + PDF page + catalogue photo
  key. `provenance.object_id`: the printed CISI ID.
  `provenance.image_ref`: the local-store plate
  reference (never a published image).
  `provenance.transcriber`: pass/adjudicator role
  identifiers (not names of outside persons).
  `provenance.transcription_date`: per pass.
- `sign_list`: the declared list — Parpola numbering
  as published in CISI, with the crosswalk-v1 version
  and its content hash recorded at dataset level.
- Token sequences carry P IDs with M counterparts
  and flags per §5.3, `UNK` per §5.2.
- **Provenance and license fields** follow the intake
  runbook (`docs/INTAKE_RUNBOOK.md`): source = CISI
  Vols. 1–2 plates held as in-copyright local
  research copies; the dataset's own license basis is
  declared in the dataset provenance (transcription
  facts — sign sequences and printed metadata —
  produced by this program), and publication form is
  Decision Ask 4. The intake validator's license gate
  must pass on the declared basis before any release,
  exactly as for an external dataset.
- **Dedup** runs through the shared spec-018 dedup
  module at dataset intake (the Phase-130 lifted
  path). `bis` second exemplars are distinct records
  linked by base printed ID; the dedup module, not
  the transcriber, is what later stages use to detect
  duplicate texts.

## 7. Evaluability mapping (spec 018) — design constraints, not promises

Under spec 018 §4's frozen matrix, dataset class
`image_transcription` **QUALIFIES** for
PRED-2026-001 and PRED-2026-002, and qualifies for
PRED-2026-003 **if** the dataset carries ≥2 distinct
site values (spec 018 §6.1, condition 5). This
proposal treats that matrix as **design constraints
on the build**, and nothing more:

- **Site coverage by construction:** the frame spans
  Mohenjo-Daro, Harappa, Lothal, Kalibangan and more
  (Appendix A); the pilot frame (§3.1) already spans
  ≥3 sites, and Stage T's strata preserve ≥2 sites at
  every scale. Site is a printed field (§4.2), so the
  §6.1 site input is satisfied by data, not by
  assertion.
- **Unmapped-share constraint:** spec 018 §6.1 makes
  a dataset with >25% unmapped-token share NOT
  EVALUABLE. The `UNK` rate (§5.2) and the
  crosswalk-unmapped rate (§5.3) are therefore
  reported per stage as evaluability-relevant
  measurements. (For scale: the mayig layer's token
  coverage under the primary crosswalk map was
  0.725823 — Phase-131 record — i.e. near this
  boundary; a layer that cannot beat it materially
  has limited evaluative use, and the pilot report
  must say where this layer stands.)
- **Attestation coverage checks (not promises):**
  the register's attestation of record (Phase-119)
  is TERMINAL 12/14 (P076 and P125 unattested in the
  ICIT-layer attestation) and INITIAL 11/12 (P000
  unattested; P000 is also one of crosswalk v1's 4
  unmapped P signs). Each stage report records
  whether P076, P125, and P000 are attested in this
  layer and with what token counts. If the frame
  never encounters them, the report records **not
  attested** — the build does not promise, target, or
  select for them beyond T2's frozen rule (§3.2),
  which operates on the 59-sign M-space union and
  does not include P076/P125/P000 as M targets.
- **No verdict is implied.** Whether a completed
  layer is ever *used* to evaluate PRED-2026-001/002
  /003 is a separate owner-authorized act under spec
  018's harness and §8's limits — and, as spec 020's
  adjudication of the Soviet dataset showed,
  qualification by class does not end the inquiry.
  This proposal pre-judges none of that.

## 8. Epistemic limits — what this layer can and cannot support

*This section is plain on purpose. It is the section
a future reader — friendly or hostile — will check
first, and it is written to be quoted.*

The transcribers who produce this layer identify
glyphs against the **published Parpola and Mahadevan
sign lists** — the same lists from which the anchor
framework's sign inventory, the canonical registry,
and crosswalk v1 are drawn. That is unavoidable: a
sign list is the instrument by which any Indus
transcription is made, and there is no list-free way
to transcribe. It has a precise consequence:

**This layer cannot, by itself, manufacture
independence from the Mahadevan tradition in the
strong sense.** Its sign *identifications* inherit
that tradition's segmentation decisions — where one
sign ends and another begins, which forms are one
sign and which are two. (Phase-123/126 record how
contestable those decisions are: Wells, working from
the same plates tradition, splits 27 of the 113
CANDIDATE anchors.) If the tradition's segmentation
is wrong somewhere, this layer will faithfully
reproduce the error, and no quantity of careful
keying changes that.

**What the layer IS independent of:** the
*transcription acts* of Holdat and of the mayig
digitization. Its records are new readings from the
plates, made blind (§5.5), by a protocol whose error
rate is measured (§5.6). It is likewise not derived
from the ICIT database — the property whose absence
disqualified the Soviet dataset's comparanda and the
ICIT-lineage derivatives under spec 018 / spec 020.

**Claims the layer can support** (each under its own
future frozen study spec, §12):

- transcription-consistency claims: measured
  agreement between independent readings of the same
  plates, and between this layer and the mayig layer
  over the keyed T1 overlap;
- matched-object claims: sign-by-sign difference
  classification (segmentation / substitution /
  insertion-deletion / order) against compilations
  whose objects can be legitimately joined — by key
  where the other side carries true CISI IDs, by the
  content matcher where it cannot — i.e. Phase-131
  Arm A becomes estimable instead of void;
- positional-behaviour claims on a keyed corpus:
  Phase-131 Arm C's stratification becomes estimable
  (site and object type are printed fields of this
  layer), and positional comparisons gain judgeable
  signs by T2's design rather than by the mayig
  layer's accidents of coverage;
- evaluability under spec 018's matrix as an
  `image_transcription` dataset (§7) — subject to a
  future adjudication, in the spec-020 pattern, of
  whether class qualification suffices for the
  specific claim at issue.

**Claims the layer cannot support:**

- that any anchor reading (a proposed sound or
  meaning for a sign) is correct — transcription
  agreement is agreement about *which sign* is
  present, not about what it *says*;
- that the sign list's segmentation is correct
  (above);
- strong-sense independence from the Mahadevan
  tradition (above) — and any future artifact that
  describes this layer as "an independent corpus"
  without §8's qualification misdescribes it;
- any PRED verdict by itself: verdicts issue only
  from the spec-018 harness under separate
  authorization, and this layer's existence changes
  no registered criterion.

## 9. What it unlocks (concretely)

1. **A legitimate join surface.** Every record
   carries a true CISI key. Any source keyed on
   printed CISI IDs — the Phase-124 catalogue itself,
   the mayig layer via the Phase-122 mapping, any
   future CISI-keyed release (CISID, CISI 3.4 if it
   ever appears digitally) — joins by key, with the
   §4.3 ambiguity log stating the exceptions.
   Against Holdat, identity remains content-based
   (spec 019 §2.1 is not repealed) — but the matcher
   then runs against a corpus whose own identity,
   provenance, and size are not in question, which is
   the side of the Phase-131 join that failed.
2. **Attribution becomes estimable.** Phase-131
   Arms A and C, rerun under a successor spec,
   operate on matched sets sized by design (T1: 179
   objects; Arm A's frozen minimum was 10 pairs) and
   on printed site/type strata — the two arms whose
   Phase-131 outputs were NOT ESTIMABLE and a 93.9%
   residual.
3. **Judgeable-sign expansion.** Phase-125 could
   judge 16 of 286 pairs because the mayig layer
   attests few signs at floor. T2's frozen rule
   (§3.2) is built to push the 59-sign target union
   to the ≥8-token floor in a keyed layer, expanding
   the judgeable set for any successor positional
   study.
4. **A standing intake-ready asset.** Because the
   layer is born conforming to intake schema v1 (§6),
   it slots into the spec-018 harness's dry-run path
   immediately and into an evaluation path if and
   when the owner authorizes one — no re-keying, no
   re-provenancing, no archaeology of the kind
   Phase-131 had to perform.

## 10. Alternatives and effort drivers

**Alternatives considered:**

- **(a) Wait for RMRL / Mitra.** Zero build effort;
  the letters of 2026-10-08 stand, and the Wednesday
  watch covers the Mahadevan Chair concordance,
  CISID, and CISI 3.4. Costs: unbounded and
  unmeasurable wait; RMRL's concordance, if released,
  is itself a Mahadevan-tradition artifact (the §8
  limit applies to it too); and nothing that arrives
  later repairs the keying defect for CISI-side
  comparisons — an arrived RMRL export and this layer
  are complements, not substitutes. This proposal
  does not close that door; it proceeds in parallel
  if approved.
- **(b) Commissioned external transcription.** Expert
  transcribers outside this program would add
  transcriber independence from our own pipeline.
  Costs: procurement, per-object pricing this
  program has no data to estimate, and the experts
  would use the same published sign lists — §8's
  limit is unchanged. If the pilot's measured error
  rates (§5.6) fail their gates, this alternative is
  the natural successor question, asked with pilot
  numbers in hand.
- **(c) 44-signs-only scope.** Cheaper in intent,
  illusory in mechanism: sign content is unknowable
  before transcription, so a "44-only" build *is* T2's
  sequential rule with the judgeable-16 dropped —
  saving little while forfeiting the judgeable-set
  expansion (§9.3) and the T1 overlap. Recorded as
  considered and not recommended; the owner may
  still choose it under Decision Ask 2.

**Effort drivers (no totals — see K5):** objects ×
(2 passes + adjudication share); tokens per object
(mayig-layer mean ≈5.6 is the only in-hand reference,
and the frame's tablets run longer than its seals);
plate legibility mix (the crop pipeline's v2 grades
— Phase-129: 50 good / 29 partial / 15 bad on its
frozen sample frame — are a rough legibility proxy,
not a transcription-difficulty measure); the gold
sample's third pass (+20% of objects); the
adjudication rate, which is itself a pilot output.
**Unit effort is unknown until the pilot measures
it. This proposal states no timeline, and any
artifact that attaches one before the pilot report
exists misstates the record.**

## 11. Decision asks — exactly what the owner is asked to approve

1. **Pilot go / no-go.** Approve Stage P as specified
   in §3.1 (~50 objects, stratified frame as stated,
   including ~10 mayig-overlap objects), with its
   stop-rule (§3.1 / §5.6), as a bounded build whose
   only further product is the pilot report and the
   measured unit quantities — or decline the build
   entirely.
2. **Tranche scope in principle.** Approve Stage T's
   shape — T1 mayig-overlap core (179 objects) plus
   T2 sequential sign-targeted expansion (59-sign
   union; PROPOSED 600-object cap) — as the scope the
   post-pilot scale decision will consider, noting
   that Stage T itself requires a separate go after
   the pilot report; or restrict the in-principle
   scope now (e.g. T1 only, or the §10(c) variant).
3. **Quality-gate thresholds.** Approve the PROPOSED
   gates of §5.6 (release gates: exact-sequence
   agreement ≥90%, per-token agreement ≥95%,
   gold-sample per-sign error ≤2%; pilot stop-rule:
   error >5% or exact-sequence agreement <80%) — or
   set different thresholds, which will be recorded
   in the freeze commit as the owner's values.
4. **Publication form.** Approve in principle that a
   completed, gate-passing stage dataset (sign
   sequences + metadata only; no images, ever) be
   published under CC BY 4.0 through the release
   gate at stage completion — or direct that datasets
   remain repository-local until a consuming study is
   authorized.
5. **Orientation convention.** Approve the
   impression-orientation primary sequence of §5.1
   (seal-face sequence derived by reversal) — or
   direct face-primary instead. One convention,
   dataset-wide, declared in provenance either way.

## 12. Governance

- **The layer changes nothing by existing.** No
  anchor, claim, PRED verdict, status, or prior
  report is modified by the build, by its quality
  results, or by its coverage results. The anchors
  file's sha256 is asserted unchanged at each stage's
  close, in the pattern of specs 021/022.
- **Studies are separate.** Any use of the layer —
  matched-object, positional, evaluative — requires
  its own spec, frozen before its statistics exist,
  and its own owner authorization where the standing
  rules require one. This spec, even once approved
  and frozen, authorizes the build only.
- **Append-only record.** Stage reports, the
  ambiguity log, adjudication summaries, and quality
  measurements are append-only; corrections are new
  dated entries. Dataset versions are content-hashed;
  a corrected dataset is a new version, never an
  edited one (spec 018 §6.5 pattern).
- **Storage discipline.** Plates, renders, crops,
  and pre-adjudication pass files live only in the
  gitignored local store; repository artifacts are
  sequences, metadata, counts, and code, verified
  before every commit in the Phase-124 pattern.
- **Freeze procedure (if approved).** Approval is
  recorded, the owner's values for Decision Asks
  2/3/5 are written into the text, the DRAFT banner
  is replaced by a freeze header naming the approval,
  and the frozen spec is committed alone before any
  implementation commit — the spec 021/022 pattern.

## 13. Deviations

None. This is a proposal; there is nothing to deviate
from. Deviations from the frozen text, if it is
approved and frozen, will be recorded here in the
pattern of specs 021/022 §Deviations.

## 14. Deliverables (if approved — proposed)

1. This spec, frozen per §12, with plan.md and
   tasks.md.
2. Per stage: the dataset (repository; §6-conformant,
   content-hashed), the stage report (frame as drawn,
   counts, measured quality vs §5.6 gates, §7 coverage
   checks, ambiguity-log summary), and a local-store
   manifest (counts and schema only).
3. The pilot report as the Stage-T decision input,
   including measured per-object effort — the first
   artifact in the program that can state what Indus
   transcription costs, because it will have measured
   it.
4. Ledger entries per stage (both ledgers; AI
   disclosure), and a PR per stage merged only under
   the standing complete + green rule.

## Appendix A — Sampling frame (computed at drafting time)

Computed 2026-10-09 from the Phase-124 catalogue
CSVs in the local store (`cisi_vol1_catalogue.csv`,
`cisi_vol2_catalogue.csv`; 7,705 photo rows),
deduplicated on (volume, printed CISI ID) =
**3,494 distinct objects**. Photo rows count
photographs (an object may have several: sides,
impressions, `bis` exemplars); objects are the
transcription unit.

Objects by site (as printed; 233 objects carry no
site in the catalogue header capture and are
frame-visible as such — they are eligible only where
a stage's rule does not require site):

| Site | Objects |
|---|---|
| Mohenjo-Daro | 1,480 |
| Harappa | 1,347 |
| Lothal | 243 |
| (not captured) | 233 |
| Kalibangan | 112 |
| Banawali | 37 |
| Jhukar | 18 |
| Desalpur | 7 |
| Amri | 5 |
| Rojdi | 4 |
| Addenda | 4 |
| Rangpur | 3 |
| Surkotada | 1 |

Objects by type (as printed): Seals 2,016; Tablets
866; Graffiti 395; (not captured) 214; Objects 3.

Raw-ID collision of record: `H-311` appears in both
volumes — the empirical basis for §4.1's mandatory
volume scoping.

## Appendix B — Frozen facts of record (no new statistics)

- Anchors: 287 entries; sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`;
  exactly 44 carry `pending_non_sa_validation`.
- The 44 (M-space, Phase-128 dossiers of record):
  M011, M021, M024, M028, M031, M033, M035, M036,
  M040, M058, M071, M072, M102, M103, M127, M149,
  M153, M155, M168, M169, M177, M178, M183, M223,
  M235, M237, M239, M254, M262, M270, M272, M281,
  M293, M304, M332, M345, M350, M355, M365, M383,
  M401, M402, M412, M416.
- Phase-125 PRIMARY judgeable pairs (16, P/M):
  P011/M017, P013/M001, P050/M059, P056/M070,
  P058/M072, P060/M065, P062/M067, P073/M051,
  P145/M087, P147/M089, P194/M048, P217/M211,
  P316/M336, P324/M342, P378/M391, P385/M267.
  Target union (§3.2): 44 + 16 − 1 (M072 in both)
  = **59 distinct M signs**.
- Phase-125: median TV 0.636931; Spearman ρ initial
  −0.424758 / terminal 0.316034; shuffle null
  p = 0.824; verdict FAIL — DISAGREEMENT (FINAL).
- Phase-127: matched-size null median TV 0.082613
  [0.046665, 0.131316]; observed reached in 0/999
  replicates; bootstrap CI for the median TV
  0.548638–0.722042.
- Phase-131: Arm A join stages — S1 179 apparent /
  0 validated; S2 0; S3 0; S4 4 matched pairs
  (NEAR 1, NEAR-REV 3), 0 exact; classes
  insertion-deletion 2, substitution 2; matched
  coverage mayig 0.022346 / Holdat 0.002395;
  matched-object TV NOT ESTIMABLE. Arm B direction
  share 0 (median TV 0.582205 both arms). Arm C/D:
  composition share 0.061321; residual unexplained
  0.938679.
- Phase-122: crosswalk v1 — 762 P↔M pairs, 412 P /
  412 M signs, 372 high-confidence, 383 conflict
  pairs, unmapped P: P000, P225, P261, P358; mayig
  layer 179 inscriptions / 179 CISI objects / 1,003
  tokens / 182 distinct P signs; primary-map token
  coverage over mayig tokens 0.725823 (Phase-131).
- Phase-124: catalogue 7,705 rows / 22 fields;
  sample field accuracy 98.9% (87/88); plates do not
  print per-object museum / material / dimensions.
- Spec 018: `image_transcription` QUALIFIES for
  PRED-2026-001/002; for 003 if ≥2 distinct sites
  (§6.1 condition 5); unmapped-token share >25% ⇒
  NOT EVALUABLE (§6.1). Register criteria
  (2026-04-23): 001 — TERMINAL end_rate ≥ 0.45 in
  ≥10 of 14; 002 — INITIAL start_rate ≥ 0.45 in
  ≥8 of 12; 003 — 3-slot template ≥70% in a multi-site
  dataset. Attestation of record: TERMINAL 12/14
  (missing P076, P125); INITIAL 11/12 (missing P000).
- Spec 020: Soviet dataset adjudicated NO for
  PRED-2026-001/002 (stands untouched).
- PRED-2026-001/002/003: PENDING.
