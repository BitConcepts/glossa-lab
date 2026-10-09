# Spec 024 — Evidence Integration: Tying the Inscriptions to Non-Textual Evidence

> ## DRAFT — PROPOSAL FOR OWNER ADJUDICATION — NOT FROZEN
>
> This document is a **proposal only**. It authorizes
> nothing. No stage of it runs, and no data work beyond
> the drafting-time verification recorded in Appendix A
> has been performed under it. It becomes operative
> only if the owner approves a stage (§11) and the
> approved text is frozen under the §12 procedure.

**Status:** DRAFT 2026-10-09 (proposal for owner
adjudication). Drafted 2026-10-09 from origin/main
`3511c497` on the owner instruction "Draft the
Spec 024 evidence-integration proposal." The facts of
record cited below are quoted from committed results
(Phase-124 / 125 / 127 / 128 / 131 / 132 reports and
results files; specs 018, 022, 023) or computed at
drafting time from the local files and recorded in
Appendix A. Nothing in this draft has been run as a
study.

---

## 0. Rationale — why context, and why now

Every text-internal route this program has tried is
closed, by verdict or by owner decision:

- **Validation batteries** (specs 011 / 014 / 016 /
  017; Phases 113 / 115 / 117 / 118) were rejected at
  their own calibration gates; the battery line was
  **formally closed by owner decision 2026-10-07**.
  The 44 anchors remain `pending_non_sa_validation`.
- **Cross-compilation positional comparison**
  (Phase-125, spec 019) returned **FAIL —
  DISAGREEMENT**; Phase-127 (spec 021) showed the
  disagreement is **not a sampling artifact**
  (matched-size null median TV 0.0826 vs observed
  0.636931; 0 of 999 replicates); Phase-131
  (spec 022) could attribute only **6.1%** of it
  (composition), leaving a **93.9% residual
  unexplained**, because the legitimate
  Holdat↔CISI matched-object join is ~0 — Holdat's
  `cisi_number` is internal sequential numbering,
  not a CISI key.
- **Building the missing keyed layer ourselves**
  (spec 023, Stage P pilot = Phase-132) **stopped
  at its frozen stop-rule**: two blinded independent
  transcription passes over CISI Vol. 1–2 plate
  photographs agreed on the full sign sequence for
  only **0.20** of 50 objects (floor 0.80). AI
  transcription from the plates is not reliable
  enough to manufacture the join.
- **PRED-2026-001 / 002 / 003 remain PENDING.** The
  Soviet positional dataset was adjudicated **NO**
  (spec 020); no large, fully independent,
  machine-readable Indus corpus exists anywhere the
  program could lawfully reach (deep sweep,
  2026-10-08). The program is in watch-and-respond
  posture (ledgers, 2026-10-09).

What none of those routes used is **context**: where
each inscribed object was found, what kind of object
it is, what is depicted on it, what it is made of and
how big it is, and where else in the world such
objects turn up. Context evidence has one property
no transcription can have: **it was recorded by
archaeologists without any theory of what the signs
mean.** A seal's findspot, object type, and motif do
not depend on the Mahadevan sign list, the Parpola
sign list, or any decipherment hypothesis. That
independence-by-construction is this axis's entire
claim to value — and §8 states, with equal plainness,
what it cannot buy: associations describe how the
writing system was **used**, not what any sign
**means**.

This proposal therefore asks, in strict stages:

- **Stage 0** — an inventory: what context fields
  actually exist, in which layers, with what
  coverage, recorded by whom — and which join keys
  survive empirical audit. *This is the only stage
  whose authorization this proposal seeks first.*
- **Stage 1** — a motif-coding pilot, designed here,
  which runs only on a separate go: can depictions
  be coded reliably enough to use as evidence at
  all?
- **Stage 2** — association tests, **designed only**
  in this proposal: each requires the Stage 0/1
  evidence beneath it and its own freeze before it
  runs.

## Epistemic boundaries

These boundaries bind every stage of this spec,
including its drafting:

1. **No stage of this program can mint, promote,
   demote, or validate any sign reading**, change any
   anchor, or touch PRED-2026 in either direction.
   (§8 is the controlling text.)
2. **Context fields are graded by recorder
   provenance** before any use (§3.4): observational
   fields (findspot, object type, dimensions) are
   context evidence; depiction-coded fields
   (iconography / motif) are context evidence of a
   weaker, coder-dependent kind; interpretive fields
   (a compilation's own morpheme / noun / verb /
   "translation" annotations) are **text-internal
   theory wearing a context costume** and are
   excluded from context evidence by construction.
3. **Fields a source does not print stay empty.**
   The Phase-124 premise correction stands: CISI
   plates do not print per-object museum, material,
   or dimensions; those catalogue columns stand at
   0% filled and are never back-filled from other
   sources under this spec (a museum record may
   supply its own object's material under its own
   key and provenance — that is a join result, not
   a back-fill, and is labeled as such).
4. **Graffiti is comparative only.** Pottery-graffiti
   material is never pooled with seal texts in any
   test under this spec (standing rule), and the
   Tamil Nadu material carries the published
   dating-gap caveat (§5.5).
5. **Restricted images never enter git.** CISI page
   images and sign/motif crops live only in the
   gitignored local store. Codes, counts, and
   metadata are publishable; images are not.

---

## 1. Objective and deliverable definition

**Objective.** Establish — by inventory first, by
pilot second, and only then by frozen test — whether
the non-textual evidence in hand can be joined to the
inscription layers reliably enough to support
disciplined association findings about the Indus
writing system's **functional organization** (what
kinds of texts live on what kinds of objects, where,
and with what depictions), and thereby about the
society that used it.

**Deliverables, by stage (each separately gated):**

- **Stage 0:** a field × layer coverage matrix with
  counts; a join-key audit with empirical collision
  rates; a field-provenance grading of every field
  inventoried; and a Stage 0 report stating, layer by
  layer, what context evidence exists and what does
  not. Facts only; no associations computed.
- **Stage 1 (separate go):** a motif codebook, a coded
  pilot sample with a preserved disagreement log, and
  measured inter-coder agreement against the gates
  frozen at that stage's approval.
- **Stage 2 (separate freezes):** association test
  results, positive or negative, under the
  pre-registration discipline of §5.

**Non-deliverable, stated once and binding:**
decipherment. No stage of this spec produces,
tests, or revises a reading of any sign (§9).

---

## 2. Evidence base in hand (facts of record)

All layers below are already acquired and local.
Drafting-time field verification is in Appendix A;
Stage 0 re-verifies everything it uses.

### 2.1 Phase-124 CISI catalogue (Vols. 1–2) — the spine

OCR-extracted from all 917 pages of the CISI Vol. 1
and Vol. 2 scans in hand; **7,705 photo rows**
(Vol. 1: 3,320; Vol. 2: 4,385), **22 fields**,
**3,494 distinct volume-scoped objects** (Vol. 1:
1,475; Vol. 2: 2,019). Drafting-time coverage:
`site` filled 94.7% / 92.2% (Vol. 1 / Vol. 2);
`object_type` 95.1% / 96.3% (Seals 4,778 rows;
Tablets 2,180; Graffiti 417; Objects 5);
`motif_chapter` — CISI's own iconographic chapter
organization — 25.1% / 26.8% (2,005 rows);
`material` and `dimensions` **0%** (not printed;
stand empty per boundary 3). Site mass is
Mohenjo-Daro (1,408 + 2,105 rows) and Harappa
(853 + 1,927), with Vol. 1 also carrying Lothal
(502), Kalibangan (237), Banawali (65), Jhukar (45),
Desalpur (12), Rojdi (8). Sample field accuracy
98.9% (Phase-124 hand-verified sample). The catalogue
lives only in the local store
(`corpora/downloads/cisi_image_layer/catalogue/`).

### 2.2 Holdat compilation layer — text + its own context codings

`indus_corpus` file: **7,002 token rows over 1,670
distinct `seal_id`s**, 19 fields including `site`
(100% token-level), `iconography` (100% token-level;
top values: unicorn 2,143 tokens, zebu bull 1,414,
elephant 859, rhinoceros 726, script only 572,
geometric 397), `position`, and `cisi_number`
(**prohibited as a join key**, §3.3). The same file
carries the compilation's interpretive annotations
(`morpheme boundary`, `noun`, `verb`, `prefix`,
`vowel`, semantic-role encodings) — graded Class I
under §3.4 and excluded from context evidence.

### 2.3 mayig CISI layer — text + free-text descriptions

179 inscriptions / 179 objects / 1,003 tokens / 182
distinct P signs (Phase-122), MIT-licensed, keyed by
CISI object ID (e.g. `M-1`, side IDs `M-1A`). Per
record: `cisi_object_id`, `side_id`, `description`
(free text that typically carries motif + object
type, e.g. "unicorn I seal"), `tokens`, `token_count`,
grapheme `features`, `source_file`. The description
field is an *unstructured* motif source; Stage 0
assesses its parseability and never treats a parse
as ground truth without a stated rule.

### 2.4 ICIT-lineage layer (horus84) — the richest context, the weakest provenance

`inscriptions.csv`: **5,679 rows, 39 fields** — the
deepest context schema in hand: `region`, `site`,
`area-section`, `block-house`, `room-grid`,
`excavation-idno`, `time`, `period`, `phase`,
`depth`, `material`, `color`, `shape`,
`cross-section`, `preservation`, `symbol`, `cult`,
`type`, `sides`, `condition`, `complete`, `dir.`,
`class`, `text length`, `signs`, dimensions
(`h`, `v`, `th`, `horizontal(mm)`, `vertical(mm)`,
`thickness(mm)`), `text`, plus `sanskrit` and
`translation` (Class I — excluded) and `notes`.
Standing determinations bind its use: this is an
ICIT-lineage derivative (the ICIT database in
open file form), admissible for descriptive and QC
purposes; it is **not** an independent witness for
validation, and no Stage 2 result computed on it
may be reported without its lineage label attached.

### 2.5 Museum open-data records — small n, full metadata

Acquired 2026-10-08 under CC0/public-domain terms:
Met (28 objects incl. 4 inscribed seals), Cleveland
(3 seals), Penn Museum (2 records). These carry the
fields CISI does not print — `medium` (material),
`dimensions`, `period`, `culture`, excavation /
accession data — for *their own objects*, keyed by
museum accession / object ID. Joins to CISI objects
exist only where a published cross-reference exists;
Stage 0 counts them, it does not invent them.

### 2.6 Comparative-strand material (graffiti and early material)

- **Kodumanal volume** (152 pp., DLI scan, local
  research copy): megalithic Kodumanal (Tamil Nadu)
  pottery-graffiti publication — context-rich
  (burial assemblages), comparative strand only.
- **Kunal article** (J-STAGE, 2012): Early Harappan
  seals from Kunal with stratigraphic context —
  small, context-dense, journal form (not
  machine-readable as acquired).
- **Catalogue Graffiti rows** (417, §2.1) and the
  Holdat / horus84 type fields are the
  machine-readable graffiti-adjacent material in
  hand. The Tamil Nadu graffiti corpus itself
  (tngraffiti.in; 9,486 records) is **not** in hand
  — access was requested 2026-10-08, no reply at
  drafting — and no Stage of this spec assumes it.

### 2.7 What is NOT in hand (stated so the design does not silently assume it)

- CISI Vols. 3.1 / 3.2 / 3.3 in any form (digital
  hunt closed 2026-10-08: absent everywhere checked;
  digital-only rule and the library-loan hold both
  stand). Stage designs use Vols. 1–2 only.
- Per-object museum / material / dimensions for the
  CISI population (boundary 3).
- Stratigraphic context (area / room / depth) for
  the CISI population — those fields exist only in
  the ICIT-lineage layer (§2.4), under its label.
- Any motif coding of the CISI image store. None
  exists; Stage 1 is the proposal to create a
  pilot's worth, or to find out that it cannot be
  created reliably.

---

## 3. Stage 0 — Context-field inventory (the first and only build this proposal asks to authorize)

### 3.1 Scope

A field-by-field audit of every layer in §2, executed
over the files as they exist locally. Stage 0 computes
**coverage and joinability only** — no associations,
no tests, no statistics beyond counts, rates, and
collision measurements. If a quantity would be a
finding about the inscriptions rather than about the
data, it is out of Stage 0 scope.

### 3.2 The coverage matrix (deliverable shape)

One row per (layer × field), with: field name as it
appears in the source; row count and unit (photo row /
token row / inscription / object); filled count and
rate; distinct-value count; the five most frequent
values with counts; recorder provenance (§3.4 grade);
and a free-text note for anomalies (e.g. the
`holdatllc_seal_catalog.csv` file in `data/raw/` whose
content does not match its name — Stage 0 records such
findings; it does not silently route around them).
The matrix is delivered as a machine-readable table
plus a human-readable report.

### 3.3 Join-key audit (the Spec 022 / 023 lessons, applied)

No key is used for any join under this program until
it has been **empirically validated** in this audit:

- **Canonical CISI key:** `cisi:v{volume}:{printed_id}`
  (volume-scoped — the raw ID `H-311` occurs in both
  volumes; Spec 023 §4.1). The audit re-derives the
  distinct-object counts per volume and reports any
  within-volume duplicate printed IDs.
- **Holdat `cisi_number`: PROHIBITED as a join key**,
  in terms — Phase-131 established it is internal
  sequential numbering; the 179 apparent CISI matches
  validated to 0. It is inventoried as a field and
  never joined on.
- **mayig `cisi_object_id`:** unscoped printed IDs.
  The audit tests each of the 179 against the
  volume-scoped catalogue keys and reports the match
  count, the ambiguous count (ID present in both
  volumes), and the unmatched count — the numbers,
  not an assumed semantics of the ID prefixes.
- **horus84 `cisi` field:** candidate key of
  unverified semantics (ICIT artefact numbering).
  Same empirical treatment: match / ambiguous /
  unmatched counts against the catalogue keys.
- **Holdat `seal_id`:** valid only as an intra-Holdat
  key (1,670 distinct over 7,002 token rows);
  cross-layer use requires a validated bridge through
  one of the audited keys above.
- **Museum accession / object IDs:** joined only via
  published cross-references to CISI IDs; the audit
  counts how many such cross-references exist in the
  records in hand.

Every candidate key's audit result is reported with
its collision rate. A key that fails (collisions
above the rate its Stage 2 use would tolerate, as
judged and recorded in the Stage 0 report) is marked
NOT USABLE, and any Stage 2 design that needed it is
redesigned or dropped at its own freeze — not patched
mid-run.

### 3.4 Field-provenance grading

Every inventoried field receives one grade, with the
grader's reason recorded:

- **Class O — observational.** Recorded from the
  object or its excavation context without
  interpretation of the writing: site, findspot /
  area / room / depth, object type, material,
  dimensions, shape, preservation, collection.
- **Class C — depiction-coded.** A human (or, under
  Stage 1, a disclosed coder) classified what is
  *depicted*: iconography / motif fields, `cult`,
  `symbol`. Context evidence, but coder-dependent —
  usable only with its coding provenance attached
  (whose coding, from what images, under what
  taxonomy).
- **Class I — interpretive.** A compilation's own
  linguistic or semantic theory: morpheme boundaries,
  noun / verb assignments, semantic roles, `sanskrit`,
  `translation`, reading proposals. **Excluded from
  context evidence at every stage.** Inventoried so
  the exclusion is auditable, never used.

### 3.5 Stage 0 exit criteria and deliverables

Stage 0 is complete when the coverage matrix, the
join-key audit, and the provenance grading are
committed with a report that states, in plain terms:
which context questions the in-hand data can and
cannot support, and which Stage 2 sketches (§5)
survive contact with the inventory. Stage 0 makes no
recommendation about Stage 1 beyond reporting whether
the motif-bearing fields and image population it
would draw on exist at the proposed scale.

---

## 4. Stage 1 — Motif-coding pilot (DESIGNED ONLY; runs on a separate go)

### 4.1 Purpose

CISI's `motif_chapter` covers only ~26% of catalogue
rows, Holdat's `iconography` is one compilation's
unverifiable coding, and mayig's `description` is
free text. Before any motif evidence is used, this
pilot answers a prior question in the Spec 023
pattern: **can depictions on these objects be coded
reliably at all** — measured, with a stop-rule, on a
bounded sample.

### 4.2 Sample (PROPOSED)

~100 objects drawn from catalogue rows that (a) have
a photo in the local image store, (b) carry an
adjudicated object key under §3.3, and (c) stratify
across site (Mohenjo-Daro / Harappa / other) and
object_type (Seals / Tablets / Graffiti-bearing
objects), with the draw rule and seed recorded before
any image is viewed. Final size and strata are set
at this stage's freeze, on Stage 0's numbers.

### 4.3 Taxonomy (literature-derived; depictions only)

The codebook is seeded from published iconographic
categories in the CISI literature — the volumes' own
motif-chapter organization and the standard published
classes (unicorn; zebu / bull; buffalo; elephant;
rhinoceros; goat / antelope; tiger; composite
creatures; human figures and cult / narrative scenes;
geometric designs; script only / no depiction;
illegible / cannot code). Coders classify **what is
depicted**. The codebook contains no sign meanings,
no reading hypotheses, and no "what the motif might
stand for" field — such a field would breach
boundary 1.

### 4.4 Protocol (Spec 023 pattern)

- **Two independent blinded coders** (basis per
  Decision Ask 3), blind to each other, to Holdat /
  mayig motif labels for the same objects, and to
  the catalogue's `motif_chapter` for the sampled
  rows (those labels are unblinded only afterwards,
  as a comparison — never as a coding input).
- **Adjudication** of all disagreements by a third
  pass, with the full disagreement log preserved
  and published with the codes.
- **Gold subset:** 20% of the sample is triple-coded
  to measure coder drift.
- **AI disclosure:** if coders are AI agents, every
  artifact of this stage carries the Phase-132
  disclosure (roles executed by AI agents in blinded
  role-isolated instances, at the owner's direction).
  Agreement numbers are reported as properties of
  *this coding pipeline*, never as properties of
  human expert coding.

### 4.5 PROPOSED gates and stop-rule (owner-set at freeze)

- **Proceed gate** (motif arm usable for a Stage 2(b)
  design): exact primary-motif agreement ≥ 85% **and**
  Cohen's κ ≥ 0.75 on the full sample, both computed
  pre-adjudication.
- **Stop-rule:** exact agreement < 70% **or** κ < 0.50
  → the motif arm **closes**; the pilot report states
  the failure plainly and no motif-based test is
  designed under this spec.
- Between the stop-rule and the proceed gate: the
  motif arm is reported as measured; any use requires
  a fresh owner decision informed by the pilot report.
  No silent middle path.

### 4.6 Publication form of Stage 1 outputs

Codes, the codebook, and the disagreement log are
publishable (they are this program's own work
product). Images and crops never leave the local
store (boundary 5).

---

## 5. Stage 2 — Association tests (DESIGNED ONLY in this proposal)

Each test below is a **sketch for a future freeze**,
not an authorization. Each freeze must restate its
test with the Stage 0/1 numbers in hand, its own
falsifier, and its own analysis code reviewed before
any run. Common discipline (§5.1) binds all of them.

### 5.1 Common pre-registration discipline

- **Family and correction.** All confirmatory tests
  frozen under Stage 2 form one declared family.
  Within the family, Benjamini–Hochberg false
  discovery control at q = 0.05. Anything computed
  outside the frozen family is labeled EXPLORATORY
  in every artifact that reports it, without
  exception.
- **Estimability rule.** A test whose contingency
  structure falls below its frozen minimum-cell rule
  (default sketch: expected count ≥ 5 in at least
  80% of cells, after only the class-collapses the
  freeze pre-declares) is reported **NOT ESTIMABLE**
  with the cell counts shown — never rescued by
  post-hoc collapsing.
- **Composition controls.** Site, object-type mix,
  and text-length mix are the standing confounders.
  Every test states its control (stratification,
  within-stratum permutation, or reweighting) in its
  freeze; an uncontrolled version of a test is not a
  permitted output.
- **Lineage labels.** A result computed wholly or
  partly on the ICIT-lineage layer carries that
  label in its headline, not in a footnote (§2.4).

### 5.2 Test (a) — Terminal-sign class × object type

*Sketch.* Unit: inscriptions in a text layer joined
(via an audited key) to an object type (Seals /
Tablets / other inscribed objects). Variable:
membership of the inscription's terminal sign in the
frozen TERMINAL attestation set (spec 018), vs
object type, controlled within site strata.
*Falsifier:* the association does not survive the
within-site control at the family threshold → the
functional-split hypothesis for terminal signs is
recorded as NOT SUPPORTED on this data.
*Question it serves:* whether the writing system's
closing-sign behavior differs by object class —
a fact about use, prior to any reading.

### 5.3 Test (b) — Motif class × sign-sequence class

*Sketch.* Runs **only if** Stage 1 passes its proceed
gate. Unit: Stage 1-coded objects (extended only
under this test's own freeze) joined to their sign
sequences. Sequence class must be pre-declared from
text-internal structure alone (e.g. the spec 018
three-slot template class, or length class) — never
from candidate readings. Same family discipline and
controls as (a).
*Falsifier:* no motif↔sequence association beyond
composition at the family threshold → recorded
NOT SUPPORTED; the long-standing informal claim that
motif and text "go together" in patterned ways is
then a measured negative, not a premise.

### 5.4 Test (c) — Site repertoire differentiation

*Sketch.* Per-site sign-frequency profiles from the
text layers, compared under a permutation null that
holds object-type mix and text-length mix fixed
within strata. *Falsifier:* differentiation
collapses to the null once composition is controlled
→ site "dialects" of the repertoire are recorded as
an artifact of what each site happens to preserve,
not a finding. (Phase-131's composition share of
6.1% is the standing warning that composition effects
in this corpus are real but small; this test is
designed to measure repertoire composition directly
rather than positional profiles.)

### 5.5 Test (d) — Pottery-graffiti repertoire patterning (COMPARATIVE ONLY)

*Sketch.* Descriptive repertoire comparison:
graffiti sign-form repertoires (catalogue Graffiti
rows; Kodumanal-published forms; Tamil Nadu material
only if it lawfully comes to hand) set beside the
seal-text repertoire as **overlap and distribution
statistics only**. **Never pooled** with seal texts
in any test (boundary 4). **Dating-gap caveat,
stated in every output:** the Tamil Nadu graffiti
material is separated from the Indus material by
≥ 1,000 years on the published rebuttal of the
continuity claims (the Harappa.com critique of
Rajan & Sivanantham), so overlap statistics are
reported as formal resemblance across a millennium
gap — a permitted output is "resemblance measured";
a prohibited output is any continuity, descent, or
survival claim.

---

## 6. Data model and provenance

- Stage outputs conform to the Phase-130 intake
  conventions for dataset records (provenance and
  license fields mandatory; a record without a
  lawful-basis field is rejected by the validator).
- Every context value carries its **recorder
  provenance**: which layer, which field, recorded
  by whom (excavation publication / CISI editors /
  a named compilation / this program's Stage 1
  coders), and its §3.4 grade. A joined dataset that
  strips provenance is a defect, not a convenience.
- Licenses: the catalogue and Holdat/ICIT-lineage
  files are local research material; the mayig layer
  is MIT; museum records are CC0/public domain as
  acquired. Publication under this spec is limited
  to this program's own derived facts (counts,
  codes, matrices) and MIT/CC0 material as their
  licenses allow.

---

## 7. Relation to spec 018 and PRED-2026

None, by design. No output of any stage of this spec
is an input to the PRED-2026 harness, qualifies or
disqualifies any dataset under spec 018's
evaluability matrix, or constitutes validation
evidence for any anchor. If a Stage 2 finding someday
suggests a *new registered prediction*, that
prediction requires its own registration under the
PRED discipline before any data is consulted for it —
it is not a deliverable or a by-product of this spec.

---

## 8. Epistemic limits — what this program can and cannot support

*This section is written to be quoted.*

> Associations describe **use, not meaning**. A
> finding that a sign class clusters on tablets, or
> that a motif travels with a sequence class, is a
> fact about how the writing system was deployed —
> it is not evidence for what any sign sounds like,
> means, or refers to. **No result obtainable under
> this spec can mint, promote, demote, or validate
> any sign reading, change any anchor's status, or
> move PRED-2026 in either direction.**
> Iconography-to-meaning leaps — "this depiction
> shows X, therefore this sign means X" — are
> expressly **out of scope**. They are the precise
> circularity this program has already falsified
> once: Phase-107 showed the syllabic-assignment
> method, which built readings partly on such
> resemblances, failed held-out validation
> (0.000; 0/115). A method's failure does not become
> a foundation because the evidence class changed.
> Hypotheses that Stage 2 findings suggest are
> labeled **hypothesis-grade** in every artifact,
> and enter the same queue as all other hypotheses
> in this program: they wait for genuinely
> independent data and a registered test. They do
> not accumulate informal credibility by being
> repeated.

What this program **can** support, when its gates
are met: (i) verified statements about what context
data exists and how it joins; (ii) association
findings — positive or negative — about the writing
system's functional organization, labeled with their
data lineage; (iii) constraints that prune the
hypothesis space (e.g. a measured absence of
motif↔text patterning closes a family of informal
claims). That is the whole of it.

---

## 9. What success looks like (honestly tiered)

- **Tier (i) — facts.** A verified context-joined
  dataset: coverage matrix, audited keys, graded
  fields. Publishable as data infrastructure
  regardless of what any test later finds.
- **Tier (ii) — knowledge about function and
  society.** Association findings about how the
  system was organized — text-type splits by object
  class, repertoire differences by site that survive
  composition controls, motif↔text patterning or its
  measured absence. These are contributions to
  understanding the Indus society and its
  administrative practices that **do not require the
  script to be read** — the same category of
  knowledge the field already holds about Indus
  weights, seals in Gulf ports, and workshop
  distributions.
- **Tier (iii) — constraints.** At most, findings
  that narrow where future decipherment work should
  look, and close lines that should stop absorbing
  effort.

**Decipherment itself is not a deliverable of this
spec, at any tier.** A reader who finishes the
Stage 2 reports knowing more about what Indus
writing was *for*, and nothing new about what any
sign *says*, has received exactly what this spec
promises.

---

## 10. Alternatives considered

- **(a) Literature-only synthesis.** Write up what
  published scholarship already establishes about
  context and function, with no new data work.
  Cheaper, and honest — but it adds nothing the
  field does not already have, and it cannot answer
  the join questions (§3.3) that determine whether
  *any* future context work is possible on our
  layers. Retained as the fallback if Stage 0 is
  declined.
- **(b) Full context-database build first.** Rejected
  as premature, on Spec 023's controlling lesson:
  the keyed-layer build went to pilot before scale
  precisely so that measurement precedes commitment.
  Building a complete context database before the
  inventory would repeat, at larger cost, the error
  of assuming joins and coverage that have not been
  measured.
- **(c) Remain watch-and-respond only.** The standing
  posture (2026-10-09 ledgers). This proposal does
  not disturb it: every stage here is separately
  gated, and declining all of §11 leaves the posture
  exactly as it stands.

---

## 11. Decision asks — exactly what the owner is asked to approve

1. **Stage 0 inventory go / no-go.** Approve Stage 0 as specified in §3 (field × layer coverage matrix, join-key audit with empirical collision rates, field-provenance grading; facts only, no associations computed), as a bounded build whose products are the matrix, the audit, and the Stage 0 report — or decline it, in which case §10(a) or §10(c) governs.
2. **Motif pilot in principle.** Approve Stage 1's shape — a ~100-object stratified sample from the local CISI image store, a codebook seeded from the published iconographic categories named in §4.3, blinded double-coding with adjudication, and the §4.5 gate pattern — as the design a post-Stage-0 decision will consider, noting that Stage 1 itself requires a separate go after the Stage 0 report; or restrict the in-principle shape now (e.g. smaller sample, or no motif arm at all).
3. **Coder basis.** Direct that Stage 1, if approved, use blinded AI double-coding with the Phase-132 disclosure, accepting that its agreement numbers measure this pipeline — or direct that Stage 1 be deferred until human expert coding is available, accepting that this may mean indefinitely.
4. **Publication form.** Approve in principle that the Stage 0 inventory dataset (coverage matrix, key-audit results, field-provenance grades — facts only, no images, ever) be published under CC BY 4.0 through the release gate at Stage 0 completion — or direct that it remain repository-local until a consuming stage is authorized.

---

## 12. Governance

- **Freeze procedure** (if any stage is approved):
  the owner's values are written into the stage's
  sections, the banner is flipped to FROZEN, and the
  freeze is committed alone — the §12 pattern of
  Spec 023. Each stage freezes separately; approving
  Stage 0 freezes nothing about Stages 1 or 2.
- **No anchor or PRED changes** arise from any stage
  of this spec (boundary 1, §7). Any study that would
  *consume* Stage outputs toward a claim requires its
  own frozen spec and its own owner authorization.
- **Results as found.** Every stage reports its
  measurements as found, including negatives,
  NOT ESTIMABLE outcomes, and gate failures — the
  program's standing rule, applied in Phases 125–132
  without exception.
- **Append-only records.** Ledger entries and stage
  reports are appended; corrections are new dated
  entries, never edits of the record.
- **Restricted material.** CISI images and crops stay
  in the gitignored local store at every stage
  (boundary 5). Repository content is code, counts,
  codes, and text.
- **Standing rules untouched.** The no-contact rule
  for Andreas Fuls, the digital-only rule for CISI,
  the library-loan hold, and the watch-and-respond
  posture are neither modified nor circumvented by
  anything in this spec; no stage requires outreach
  of any kind.

---

## 13. Deviations

None at drafting. (This section is the standing
place for deviations if a stage is approved and
executed; deviations are recorded here and in the
stage report, never silently.)

---

## 14. Deliverables (if approved — proposed)

- **Stage 0:** coverage matrix (machine-readable +
  report), join-key audit, field-provenance grading,
  Stage 0 report. Repository PR; the inventory
  dataset published or held per Decision Ask 4.
- **Stage 1 (separate go):** codebook, coded sample,
  disagreement log, pilot report with gate verdicts.
- **Stage 2 (separate freezes):** one report per
  frozen test, results as found.

---

## Appendix A — Drafting-time verification (computed 2026-10-09 from the local files)

*Stage 0 re-verifies all of this; these numbers are
the proposal's basis, not its results.*

**A.1 Phase-124 catalogue** (`corpora/downloads/cisi_image_layer/catalogue/cisi_vol{1,2}_catalogue.csv`):
7,705 data rows (Vol. 1: 3,320; Vol. 2: 4,385);
3,494 distinct `cisi_id` (1,475 / 2,019). The 22
fields, as printed in the CSV header:
`volume, cisi_id, photo_key, side, bis, caption_raw,
caption_ocr_score, pdf_page, printed_page, site,
object_type, motif_chapter, scale_pct,
collection_scope, material, material_basis,
dimensions, dimensions_basis, photo_box_xywh,
extraction_basis, confidence, notes`.
Fill rates — Vol. 1: site 94.7%, object_type 95.1%,
motif_chapter 25.1%, material 0%, dimensions 0%.
Vol. 2: site 92.2%, object_type 96.3%, motif_chapter
26.8%, material 0%, dimensions 0%.

**A.2 Holdat layer** (`corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`):
7,002 token rows; 1,670 distinct `seal_id`. The 19
fields: `letters, form, cisi_number, site,
iconography, position, seal_id, upos, xpos,
letter_label_encoded, prefix, vowel,
morpheme boundary, noun, verb, FormWithoutLemma,
Counts, MorphemeSeparated, prefix_label_encoded`.
Site and iconography filled 100% at token level;
iconography top values (tokens): unicorn 2,143;
zebu bull 1,414; elephant 859; rhinoceros 726;
script only 572; geometric 397.

**A.3 mayig layer** (`data/corpus_layers/mayig_cisi_layer_v1.json`
+ source corpus): 179 inscriptions / objects, 1,003
tokens, 182 distinct signs. Per inscription:
`cisi_object_id, side_id, description, tokens,
token_count, features, source_file`. Source JSONs
carry per-side `id`, free-text `description`
(e.g. "unicorn I seal"), and graphemes with P-ids
and Wells-derived feature vectors.

**A.4 ICIT-lineage layer** (`…/horus84-computational-linguistics/data/inscriptions.csv`):
5,679 data rows, 39 fields: `id, cisi, region, site,
area-section, block-house, room-grid,
excavation-idno, time, period, phase, depth, boss,
material, color, shape, cross-section, preservation,
symbol, cult, type, sides, condition, complete,
dir., class, text length, signs, h, v, th,
horizontal(mm), vertical(mm), thickness(mm), text,
sanskrit, translation, notes`.

**A.5 Museum open data** (acquisition record,
2026-10-08): Met CC0 — 28 objects incl. 4 inscribed
seals, full museum metadata schema (objectName,
culture, period, medium, dimensions, accession and
excavation fields among them); Cleveland CC0 —
3 seals; Penn Museum — 2 records.

## Appendix B — Frozen facts of record relied on (no new statistics)

- Battery line closed by owner decision 2026-10-07;
  44 anchors `pending_non_sa_validation`.
- Phase-125 FAIL (median TV 0.636931); Phase-127
  not-noise determination (null median 0.0826,
  0/999 replicates); Phase-131 attribution: 6.1%
  composition, 93.9% residual, matched-object join
  ~0 under the only legitimate key discipline.
- Spec 020 verdict NO (Soviet dataset not
  PRED-qualifying); PRED-2026-001/002/003 PENDING.
- Phase-132 pilot: stop-rule fired (exact-sequence
  agreement 0.20 vs 0.80 floor); Stage T not proposed.
- Phase-124 premise correction: CISI plates do not
  print per-object museum / material / dimensions.
- Watch-and-respond posture recorded in both repo
  ledgers, 2026-10-09 (PR #104); Zenodo v4.5.0
  closeout, DOI 10.5281/zenodo.23266588.
