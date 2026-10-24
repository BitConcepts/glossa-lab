# Spec 064 — Adjudication (2026-10-21)

> Adjudication for the successor spec to Spec
> 046, opened under the owner's approval of
> 2026-10-21 (amendment package Item 5), on
> the amendment-queue commission of the same
> date (Item 5: drawn-form references for
> Wells's signs 821 and 297). Sections 1–6
> are the draft's own record: the verified
> predecessor closure, the preservation act
> and protocol this successor freezes, the
> decisions decided by this draft, what only
> the freeze may decide, and the
> twice-derived acceptance tests. Section 7
> records the freeze decisions. Nothing here
> executes anything.

## 1. Inputs read at this draft

- Spec 046's full record:
  `specs/046-horned-tiger-concordance/spec.md`,
  `claims.json` (F046-C01…C15),
  `adjudication.md` (DD-046-1…DD-046-18),
  `freeze.json` (successor digest
  `e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6`),
  `outcome.md` (Phase-405, executed
  2026-10-21), and `concordance-297.json`
  (the closure delivery).
- The amendment draft Item 5
  (`~/workspace/research_notes/amendment-queue-2026-10-21/item-5-drawn-form-references.md`),
  in full: §1 (the verified closures), §3.2
  (the thesis-plate route), §4 (the license
  position), §5.2 (the sign-297 finding),
  §6.2 (the reference record), §7 (the
  identification protocol), §8 (the
  successor's charter).
- The pinned inputs of spec §2, recomputed
  at this draft (see §2).

## 2. The predecessor closure, verified (the record this successor stands on)

- Spec 046 (Phase-405) passed step 0 in
  full, named the source's list at step 1.1
  (Wells's own, Wells 2015 Ch. 2 / Fig. 2.6),
  and closed **IDENTIFICATION FAILED (sign
  unmatched)** at step 1.2. Verified against
  the pinned files at this draft:
  - the only `W297` value in the registry
    sits inside the 17-value `wells_ids`
    cell `W289|W290|W291|W292|W293|W294|W295|W296|W297|W299|W300|W301|W302|W303|W304|W305|W306`
    on row **P205** ("Prismed light rays,
    with opposite slanting on top vs bottom,
    more rays on bottom", `mahadevan_ids`
    M180) — the first frozen trap; the cell
    does not by itself identify the
    passage's sign;
  - row **P297** is "Ladder motif. Two
    nearby vertical lines with a number of
    horizontal lines going across the
    middle…" (`wells_ids` empty) — the
    second frozen trap; a different sign;
  - no registry description names a tiger
    (0 of 803);
  - the Phase-123 witness carries no
    grapheme 297 in any row's
    `wells_graphemes` field (the string
    "297" appears only as the Mahadevan
    label M297, whose Wells grapheme is
    924);
  - Figure 2.6's drawn forms did not
    survive the held copy's text extraction
    (captions only, held text lines 868,
    872, 876, 880), so no inspectable
    drawn-form reference existed in the
    held record;
  - the word "297" occurs in the held
    Wells text only in the passage itself
    (printed p. 97; lines 2938–2941).
- The named unblocking act (Spec 046
  outcome §3): "an inspectable drawn-form
  reference for Wells's sign 297 (for
  example the Figure 2.6 figure pages as
  images, or a published drawn-form
  cross-match for this sign) preserved as a
  committed, hashed record." The amendment
  draft establishes that the act is
  satisfiable in text form, without the
  images the headline mentioned, because
  the headline's purpose — that the drawn
  sign can be matched by drawn form, or the
  reference quoted as the source list's own
  entry — is met by the descriptor plus the
  citation, and the program's no-images
  rule bars the image form in any case.
- Spec 046's closure delivery stands
  unedited (SHA-256 `772db4df…`); its OSF
  registration dnts8 is APPROVED + PUBLIC.
  Its IDENTIFICATION FAILED stands until a
  successor execution produces its own
  outcome (DD-064-9).

## 3. The preservation act and the protocol (amendment draft §§6.2, 7 — followed exactly)

**The reference record.** Committed in this
spec's directory as
`drawn-form-reference-297.json` (schema
`glossa.drawn-form-reference/1`), with
exactly the amendment draft §6.2 contents:
the target with its list-naming evidence
(held text lines 414, 665); the purpose and
fragment; the passage of record (Wells
2015, printed p. 97, held text lines
2938–2941, held text SHA-256 `62acf855…`);
the citation-pinned reference (Figure 2.6,
printed pp. 19–22; captions lines 868–880);
the descriptor as drafted in §6.2 (a bundle
of four long parallel strokes bent once —
upper portions slanting steeply down-left,
lower portions near-vertical, splaying
slightly at the base — standing in the
plates' bent-ray run 289–308), with its
recorded limitation as part of the record;
the plate reference (Wells 2006 thesis,
Figure 3.2, thesis p. 90 / PDF p. 102,
bottom row signs 295–308, 297 the third
entry; local file SHA-256 `4b39330c…`); the
family anchor P205 recorded with its frozen
status — corroboration only, NOT an
identification; the traps (P205's cell as
identification; P297 "Ladder motif";
witness M297 → grapheme 924; M180 as
W297's identity; any number-only match);
`continuity_status` **QUALIFIED** with the
recorded limitation; the provenance chain;
and the license position (amendment draft
§4 ¶¶1–2: a derived factual record; no
image; no restricted material used — no
CISI material and no CISI 3.1 ILL material
contributed to this record). Its SHA-256
was computed at commitment —
`33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`
— and is pinned in this successor's freeze.
**No images are committed anywhere in this
spec.**

**Why the reference is lawful and
inspectable, in brief** (the full argument
is the amendment draft §4): a stroke /
feature descriptor is a factual statement
about what a published drawing shows — not
the drawing, not a scan reproduction, not a
passage of the author's text. The PhD
thesis is an open national-library
digitisation deposit (Internet Archive
`epigraphicapproachestoinduswritingbryankennethwellsphd.thesis_230_Z`,
open access; CITATIONS.md §A.8), and
Phase-123 already committed 157 derived
records from these same plates under its
stated governance. A second party with the
committed record and lawful access to the
cited artefacts can check the drawn form
for themselves, without trusting the
recorder.

**The protocol** (amendment draft §7,
frozen as spec §3 gate 0.4 and §4 steps D,
C, M): step 0 gains the reference gates
(input integrity includes the reference at
its pinned digest; reference producible —
the thesis file's digest asserted before
any plate is read, the plate page produced
from the pinned local file; no substitute
artefact). Step D derives the descriptor
twice, independently, without sight of each
other or of the preserved wording;
reconciliation is by recorded features, an
unsettled disagreement resolves against
identification, and a material difference
from the preserved descriptor closes
IDENTIFICATION FAILED (reference not
sustained). Step C — continuity — is
**mandatory** in this successor: each
derivation must affirm that the descriptor
picks out plate 297 and no neighbour in the
289–308 run, with the family anchor carried
at its frozen status; if either cannot, the
run closes **IDENTIFICATION FAILED
(continuity/discrimination not sustained)**
— pre-registered, per DD-064-11. Step M
admits exactly two routes for this sign:
route 1 (a registry row matched by drawn
form) and route 2 (the preserved reference
cited as the source list's own entry). The
composition route is sign-821-only and is
not a route here. No route may be
constructed at run time.

**The qualification is load-bearing.** The
reference's continuity is anchored at
family level only (§5.2 of the amendment
draft): no formation text for 297, no
registry row, no witness row fixes the
number individually from the 2015 side.
This successor therefore does not present
the preserved reference as an identification:
it is the record step 1.2 consumes, under a
mandatory step C that may still close the
run as IDENTIFICATION FAILED, and its
QUALIFIED status is carried into the spec's
reporting wherever its result would be
stated (spec §§1, 5.3, 8, 9; DD-064-13).

## 4. Decisions decided by this draft (DECIDED-BY-DRAFT)

- **DD-064-1 — The delivery form is carried
  from Spec 046.** Spec §6 carries Spec 046
  §6 exactly in substance: file
  (`concordance-297.json`, in **this**
  spec's directory), top-level fields with
  `producer_spec` `"064"`, the one-sign
  record's fields (with the
  `drawn_form_reference` path + digest added
  to `target_sign`), the four list rows,
  the `asset_a_feed` block and its
  per-outcome rules, and the citation /
  locator string form.
- **DD-064-2 — Wells never counts toward
  CONSENSUS.** Carried from DD-046-2: a
  source cannot corroborate itself; the
  Wells row is scored as SOURCE and the
  agreement count runs over CISI, Parpola,
  and Mahadevan (claim F064-C08).
- **DD-064-3 — PARTIAL CONCURRENCE carried.**
  The outcome mapping stays total with Spec
  046's freeze-confirmed fourth word
  (DD-046-3, DD-046-9), in its space form.
- **DD-064-4 — SILENT carries
  `entry_present`.** Carried from DD-046-4.
- **DD-064-5 — Agreement is scored at the
  tiger-kind level.** Carried from DD-046-5;
  the qualifier is recorded verbatim rather
  than scored.
- **DD-064-6 — Step 0 is fail-closed,
  extended to the reference.** Carried from
  DD-046-6 and extended: the gate set adds
  gate 0.4 (reference producible, thesis
  digest asserted); a list or the reference
  that cannot be produced closes the run at
  step 0 (claim F064-C05).
- **DD-064-7 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-064-8 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today.
- **DD-064-9 — Successor, not amendment.**
  Spec 046's frozen record, outcome, and
  closure delivery stand unedited; this
  successor re-runs the question in its own
  directory under its own freeze and its own
  delivery. Asset A consumes only this
  successor's delivery if one is produced
  (amendment draft §8).
- **DD-064-10 — The preservation act is
  performed inside this spec.** The §6.2
  reference record is committed in this
  spec's directory, its SHA-256 computed at
  commitment and pinned in the freeze (spec
  §2). No images anywhere.
- **DD-064-11 — Step C is mandatory, with
  its closure pre-registered.** If either
  independent step-D derivation cannot
  affirm that the descriptor picks out plate
  297 and no neighbour in the 289–308 run,
  the run closes IDENTIFICATION FAILED
  (continuity/discrimination not sustained).
- **DD-064-12 — Two identification routes
  only.** Route 1 (registry, by drawn form)
  and route 2 (the preserved reference as
  the list's own entry, quoted with its
  locator). The composition route is
  821-only and unavailable here; no route
  may be constructed at run time.
- **DD-064-13 — The QUALIFIED status is
  carried into reporting.** Wherever this
  successor's result would be stated, the
  reference's QUALIFIED continuity status
  is stated with it (spec §§5.3, 8, 9;
  claim F064-C13).

## 5. OPEN for the freeze (each blocks the freeze until decided and recorded; each is OWNER-APPROVAL)

- **OP-064-1 — Execution phase number.** Not
  allocated by this draft (Phase-405 was
  Spec 046's; the next number is the
  freeze's allocation, verified against the
  root LEDGER and the frozen specs'
  records).
- **OP-064-2 — OSF registration.** Whether
  this spec files its own OSF contract
  registration at its freeze, under campaign
  decision E-1, as Spec 046 did (DD-046-18).
  The filing act itself is OWNER-APPROVAL;
  no filing is made by this draft.
- **OP-064-3 — The freeze and execution
  acts.** The freeze of this spec, and any
  later execution order, are the owner's
  acts. **OWNER-APPROVAL** for each: freeze,
  OSF filing, execution.

## 6. Acceptance tests derived twice, independently — disagreements and resolutions

Per the campaign doctrine, each claim's
acceptance test was derived twice: once from
the claim text as written (**derivation A**),
and once independently from the underlying
requirement alone — Spec 046's frozen record,
the amendment draft §§6.2/7/8, or the
campaign decisions — without consulting A's
wording.

| Claim | Disagreement between the derivations | Resolution in this draft |
|---|---|---|
| F064-C06 | A let step 1.2 rest on the preserved reference directly (the reference exists precisely so the step is satisfiable); B, from the amendment draft §7, required the descriptor to be derived twice independently and the preserved wording only *checked* — inheriting it would make the preservation act its own verification. | B adopted — step D derives twice without sight of the preserved wording; agreement with the preserved descriptor is required, and a material difference closes IDENTIFICATION FAILED (reference not sustained) (DD-064-10, DD-064-12). |
| F064-C06 / step C | A treated continuity as a reporting note (the QUALIFIED status stated in the outcome); B held that a qualification which cannot change an outcome is decorative: the amendment draft §7 makes the discrimination affirmable-or-failing by each derivation, with a named closure. | B adopted — step C is mandatory and its closure, IDENTIFICATION FAILED (continuity/discrimination not sustained), is pre-registered in spec §§4, 11 and claim F064-C06's boundary (DD-064-11). |
| F064-C11 | A placed the successor's delivery over Spec 046's file (same filename, one feed for Asset A); B noted Spec 046's directory is frozen and its closure delivery digest-pinned — overwriting it would edit a closed record and break its pins. | B adopted — the delivery is produced in this successor's own directory with producer_spec 064; Asset A consumes only the successor's delivery if one is produced (DD-064-1, DD-064-9). |
| F064-C13 | A carried Spec 046's five reporting elements unchanged; B required the qualification and the identification record (reference digest, derivation sheets, step C statement, route, traps) as reporting elements in their own right, since a result stated without them reads stronger than the reference it rests on. | B adopted — spec §8 element 6 and claim F064-C13's boundary carry them (DD-064-13). |

All other claims (C01–C05, C07–C10, C12,
C14, C15): the two derivations agreed on the
operative check (inspection against the
stated boundary, an exact gate, or mechanical
recomputation from the published record), and
no disagreement is recorded because none
arose. The C01/C15 pair carries the same
boundary_confirmation construction as Spec
046's recovered register states it.

**This does not establish:** this draft
establishes, at most, that the §6.2
reference can be preserved in text form
from sources the program lawfully holds,
carrying a stated continuity qualification.
It does not establish that sign 297 is
identified: identification is an act this
successor performs under its own freeze,
and it may still fail — including on the
continuity limb this draft prices in. Spec
046's IDENTIFICATION FAILED stands.

---

*AI disclosure: drafted by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*

## 7. Freeze decisions — 2026-10-21

> ## FREEZE — 2026-10-21
>
> Recorded at the freeze act under the
> owner's approval of 2026-10-21 (amendment
> package Item 5: build Spec 064, the
> successor to Spec 046, through freeze and
> OSF filing). The AEE lifecycle hooks ran
> over the register first (`aee/freeze-aee-note.md`);
> the digest in `freeze.json` was computed
> exactly once over the recovered register
> and the finalised freeze texts (the Spec
> 035 ordering). This section is append-only
> beside §§1–6, which stand unedited.

### 7.1 The pins — verified two routes at this freeze

- Every §2 pin was re-derived at this freeze
  by two independent routes — the git-blob
  route and the contents-API raw route —
  both at `main`
  `e03f7832f99463d3496241676e21bf85e62fb9cc`,
  with the working tree agreeing as a third
  read: registry
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`
  (803 rows), held Wells text
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`,
  witness
  `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da`
  (157 rows), Spec 046 closure delivery
  `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`.
  The Phase-104 evaluation
  (`2d0b83e8…`) and lane-2 drafts
  (`3f645c9a…`) recompute unchanged. The
  claim record recomputes to
  `997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031`:
  its bytes differ from Spec 046's draft pin
  (`bd0f7abd…`) because the record now
  carries Spec 046's dated first-check
  append of Phase-405 beside the frozen
  entry (the append Spec 046's freeze
  foresaw, restored to the record by PR
  #306); the fragment entry itself —
  normalised claim, untested status, created
  stage — is unchanged, verified by read at
  this freeze. The thesis PDF's digest
  (`4b39330c…`, 19,313,853 bytes) is the
  amendment draft's verified value from the
  program's local store; the file is not in
  the repository, and gate 0.4 asserts it on
  the local file at execution before any
  plate is read.
- The preserved reference record's digest,
  computed at its commitment in this spec:
  `33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`
  (7,168 bytes). It is pinned here and in
  `freeze.json`, and the file is a
  digest-covered source of this freeze.

### 7.2 The open items (OP-064-1…OP-064-3) — decided

- **DD-064-14 — The freeze basis.** The
  owner's approval of 2026-10-21 (amendment
  package Item 5) is this freeze's authority:
  Spec 064 is built through freeze and OSF
  filing on the amendment-queue commission
  of the same date. The draft decisions
  DD-064-1 to DD-064-13 stand as drafted;
  none is overturned.
- **DD-064-15 — Execution phase number
  (OP-064-1): Phase-426 is allocated to
  Spec 064's execution.** Verified at this
  freeze: Phase-424 was Spec 062's
  (DD-062-8); a repository search for
  "Phase-426" returns no record, the root
  LEDGER allocates no Phase-426, and no
  phase426 report, script, or graph module
  exists in the tree at `main` e03f7832.
  (Phase-425 is not this spec's: a sibling
  Spec 063 freeze in the same approval
  package is expected to allocate it; this
  allocation takes 426 so the two freezes
  cannot collide, and the number is
  re-verified against the merged record
  before this freeze merges.)
- **DD-064-16 — OSF registration
  (OP-064-2): yes.** This spec files its own
  OSF contract registration at the freeze,
  under campaign decision E-1, as Spec 046
  filed its own (DD-046-18). The filing
  record is `osf-spec-registration.md`,
  completed by append after the filing
  exists.
- **DD-064-17 — The freeze and execution
  acts (OP-064-3): the freeze is taken; the
  execution is not authorised.** The freeze
  act and the OSF filing act are taken under
  the owner's approval of 2026-10-21
  (amendment package Item 5). Execution
  (Phase-426) is a separate later act: it
  begins only after this freeze has merged,
  the OSF registration's approval act has
  completed, and a separate execution order
  is given.
- **DD-064-18 — Carried freeze matter.**
  The lists of record stand as Spec 046's
  freeze named them (DD-046-10 to
  DD-046-12), the lineage note stands in the
  §5.3 CONSENSUS wording (DD-046-13), no
  separate dry-run sign is required
  (DD-046-15's ground carried: the §5.2
  mapping is a total function of the four
  published rows, and its totality is pinned
  mechanically in
  `backend/tests/test_spec064_freeze.py`),
  and the DD-038-10 AEE gate reading is
  adopted (zero correctness failure modes
  and no claim below 0.70 = substantive
  pass; FR-2.3 draft-cap residuals at the
  draft/created lifecycle stage are
  structural, recorded openly in
  `aee/freeze-aee-note.md`, never edited
  away).

**This does not establish:** the freeze
establishes only that the successor contract
— the preserved reference, the mandatory
step C, the two routes, the carried
concordance — is frozen as designed. The
frozen reference is QUALIFIED: it does not
establish that 297's identification will
survive its own step C discrimination
check. Spec 046's IDENTIFICATION FAILED
stands until a successor execution produces
its own outcome, and no list has been opened
for scoring under this spec.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
