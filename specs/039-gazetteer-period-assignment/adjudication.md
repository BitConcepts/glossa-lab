# Spec 039 — Adjudication Record

> ## ADJUDICATED INPUT — 2026-10-20
>
> This spec has two adjudication inputs, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's decisions of 2026-10-20** on the
>    gazetteer period-assignment act, taken on the
>    decision memo of the same date
>    (`~/workspace/research_notes/indus-gazetteer-act-decision-memo-2026-10-20.md`):
>    the act is **authorised**, **bundled with the
>    D-25 chronology test**, and its evidence
>    standard is **Option 1 — published period
>    determinations only**. These are recorded in
>    §1 as **DECIDED**. They are not proposals, and
>    this draft does not re-open them.
> 2. **The owner's instruction of 2026-10-20**:
>    "you plan it and just do them at the right
>    time" — commissioning this draft and the
>    bundle's sequencing. The instruction commissions
>    the design and the plan; the freeze of this
>    contract and its execution remain the bundle
>    cycle's later acts, sequenced in `plan.md`,
>    and this draft performs neither.

## 1. Decisions already made (DECIDED — not proposals)

- **D1 — The act is authorised, bundled with D-25.**
  The gazetteer period-assignment act (Spec 027
  §6.2) will be specified, frozen, and executed as
  the first stage of a bundle whose second stage is
  D-25, the chronology-controlled re-test of Spec
  025's G1 result (design portfolio, PR #195; the
  result stands SUPPORTED under control with
  chronology not controlled — the named rider D-25
  exists to test). One adjudication cycle covers
  both acts; D-25's own spec is a separate document
  and is not designed here.
- **D2 — Evidence standard: Option 1.** Every
  period label must trace to a printed/published
  determination about that site. Sites without one
  stay blank. **No program-derived assignments**:
  Option 2 (published determinations plus
  program-derived assignments under frozen rules,
  e.g. spine dates → period) was put to the owner
  in the decision memo and was **not** adopted.
  Downstream studies therefore never consume a
  program inference dressed as a gazetteer label
  under this act, and the reading-off-the-spine
  that Spec 031's freeze forbade for that study is
  not licensed here either.

## 2. The adopted basis (operative substance)

Carried into `spec.md` without deviation:

- **The field.** Spec 027 §6.2:
  `program_period_assignment` — nullable; mapping
  rule and reviewer recorded when present. The
  gazetteer unit is one source assertion about a
  site; clustering never deletes source rows or
  their disagreements.
- **The gap.** On the gazetteer as it stands
  (36 rows, 30 sites), `period_label_as_published`
  is null on 33 rows and carries only
  pre-Neolithic/Neolithic values on 3 Central Asian
  rows; `program_period_assignment` is null on all
  36 rows.
- **The consumer rule.** Spec 031's frozen period
  rule (adopted 4A; F031-C10): a site is
  period-eligible iff its gazetteer
  `period_label_as_published` or program period
  assignment indicates Mature Harappan occupation
  as published; no finer temporal slicing is
  attempted in that design.
- **The closure this act answers.** Phase-395
  closed Spec 031's arms at the margins step
  (bead/craft NOT-YET-TESTABLE; ceramic NOT
  ESTIMABLE; 0 eligible sites against the floor of
  8) and named a Spec 027 gazetteer act as the
  route that changes the period screen.
- **The disagreement posture.** §6.3: no majority
  vote silently resolves conflicting source rows.
  §6.5: competing assertions are preserved; analyses
  name their scenario and report the rival as a
  sensitivity — the both-ways reporting Spec 030
  used for contested chronology.
- **The boundary.** Spec 030 Ask 2 (CONTESTED
  sensitivity bindingness for a future Q6 freeze)
  is **expressly NOT DECIDED** in Spec 030's own
  adjudication and stays **RESERVED**. This act
  does not decide it, does not depend on it, and
  does not prejudge it: Ask 2 governs chronology
  scenarios in the spine; this act governs period
  labels in the gazetteer.

## 3. Verification record at draft

Every fact this design rests on was verified
first-hand at drafting, 2026-10-20, against the
record on `main` (head `5e7f3cdb`):

- **Gazetteer census** — computed from
  `data/movement/gazetteer_rows.jsonl` itself:
  SHA-256
  `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`;
  36 rows; 30 distinct `program_site_id`; sources
  XRONOS 21 / CISI Vol. 1 catalogue 11 / CISI
  Vol. 2 catalogue 4; licence states
  `verified_open` 21 / `open_access_read_only` 15;
  `period_label_as_published` null ×33,
  `["PN", "Neo.?"]` ×2, `["PN", "Neo."]` ×1;
  `program_period_assignment` null ×36.
- **Phase-395's pin agrees** —
  `reports/phase395_results.json` records the same
  gazetteer SHA-256 as its input hash, and its
  population record carries
  `link_eligible_sites_in_gazetteer` = 2
  (Harappa, Mohenjo-daro), both arms at 0 eligible
  sites. Spec 031's outcome record states the
  floors (8 eligible sites, 10 linked pairs) and
  the closures as designed here.
- **Spec 027 text** — §5.1 (licence states,
  including `catalogue_only`), §5.2 (coordinate
  states), §6.2 (fields), §6.3 (no majority vote),
  §6.5 (contested assertions) read in
  `specs/027-movement-culture-language/spec.md`.
- **Spec 031 text** — the period-eligibility rule
  (adopted 4A; F031-C10) read in
  `specs/031-stage2-q7-provenance-networks/spec.md`
  §6, and the margins record in its `outcome.md`.
- **Spec 030 text** — Ask 2's expressly-undecided
  status read in
  `specs/030-q6-chronology-spine-extension/adjudication.md`.
- **Masudpur record** — read in
  `reports/phase394_results.json`: 28
  determinations for Masudpur VII (Bhim Wada
  Jodha) and Masudpur I (Sampolia Khera) extracted
  in full, not admitted; the record's own words
  name the route: rule 7 admits coordinate-less
  rows only for gazetteer-established sites, and
  "a future build (or a Spec 027 gazetteer act)
  can admit the rows without re-extraction."
- **Stage 0 deposit** — Zenodo record 23300361
  read back at this draft: "Glossa Lab Spec 027
  Stage 0 — Indus Settlement Gazetteer and
  Chronology Spine (Phase-391)", DOI
  10.5281/zenodo.23300361, files exactly the
  release package. The deposit's gazetteer CSV is
  the 21-row `verified_open` subset.
- **Not done at draft, by design** — no published
  determination for any site was located, read for
  its period content, or recorded; no label was
  assigned, provisionally or otherwise; the
  mapping table of spec §4 exists as a rule shape,
  not as filled entries. Evidence assembly is
  execution work under the frozen contract.

## 4. Open points for the freeze decision (DD-039)

### DD-039-1 — The label set

**Recommendation: the coarse three-period set —
Early Harappan, Mature Harappan, Late Harappan.**
It is the vocabulary of the frozen consumer rule
(F031-C10 turns on Mature Harappan occupation and
attempts no finer slicing), it is what D-25's
strata consume, and nothing currently frozen needs
finer labels. Finer labels are more work per site
and more disagreement to adjudicate, for no named
consumer. Under this set, a published determination
outside the Harappan sequence (e.g. the gazetteer's
own PN/Neo. values) grounds no assignment, and a
multi-period occupation statement grounds a
multi-label record stated as such (spec §4 rule 2).
The register (F039-C05) carries the recommended
set; overturning it at freeze is a register change
and a new digest, openly made.

### DD-039-2 — The source hierarchy

**Recommendation: a four-tier citation order.**
(1) Published excavation reports and site
monographs — the excavators' own statements of a
site's occupational periods. (2) Published regional
surveys and site catalogues carrying per-site
period assignments. (3) Published compilations and
site lists — Possehl's lists; Law (2011)'s site
compilations — used **as citations only**, under
their Stage 0 licence states (`catalogue_only`),
exactly as §3 of the spec provides. (4) Published
journal literature on individual sites.
The hierarchy orders which determination is cited
first and how a site's evidence is presented. It
**never** suppresses a lower-tier determination,
never breaks a tie, and never resolves a contest:
all admissible determinations are recorded, and
disagreement is flagged under F039-C09/C10. The
gazetteer's existing row sources (XRONOS, the CISI
catalogue layers) are not period-determination
sources for this act; their published labels
already stand in `period_label_as_published`.

### DD-039-3 — When a TwoRains determination counts as published

Stated precisely, because the Masudpur material
(DD-039-4) and any Haryana-site evidence turn on
it. **Recommended rule:** a TwoRains determination
counts as a published determination under Option 1
**if and only if** it appears, with a locator
(page or table), in (a) a peer-reviewed journal
article, (b) that article's published supplementary
material, or (c) a published excavation or survey
report in a named series. Under this rule the
Petrie, Bates, Higham & Singh (2016) published
supplement — the source of the Phase-394 Masudpur
extraction — **is** a published source. **Not**
published under this rule: project-internal
datasets and databases; data deposits that are not
period determinations (the TwoRains Zenodo deposit
inspected in Stage 0, 3909832, is a crop-model R
project, not a gazetteer); unpublished survey
records; and doctoral theses (the Bates 2016
thesis corroborated Phase-394's flags, but under
the conservative default a thesis does not solely
ground an assignment). **Conservative default:**
where a determination's venue is doubtful, it does
not count, and the site is treated as having no
determination from that source. The freeze may
widen the venue list openly; it may not narrow the
locator requirement.

### DD-039-4 — Whether the act also establishes the Masudpur sites

**Recommendation: no — not in this act.** The act
is confined to the existing 30 gazetteer sites.
Establishing Masudpur VII and Masudpur I would
raise the coordinate question as its own subject
(no publication reached states coordinates for
either site; the geographic authorities checked in
Phase-394 carry none; §5.2 forbids defeating a
restriction by inference), and the determinations'
admission is a chronology-spine act under Spec
030's rules, not a gazetteer-labelling act.
Nothing is lost by the default: the 28
determinations are preserved in full in the
Phase-394 record, the establishment route is named
there and here, and a future act can take it with
the coordinate question in front of it. (The owner
may decide otherwise at freeze; the memo's call
(c) is recorded as a freeze decision, with this
default.)

### DD-039-5 — Where the margins re-run lives

**Recommendation: the margins re-run is this act's
own verification step** (spec §8), confined to the
period-eligibility gate of the Phase-395 margins
step, recomputed over the assigned gazetteer and
recorded with the standing link-mass floor stated.
It is not part of D-25's work (D-25 tests a
different claim on a different input), and it
re-opens no Q7 verdict machinery: no response, no
similarity matrix, no verdict language. Spec 031's
closures stand untouched either way (F039-C13).

### DD-039-6 — The spec's own OSF contract registration

**Proposal: yes at freeze** — file this frozen
spec's own OSF contract registration, following the
DD-035-4 / DD-036-4 precedent for specs whose
subject arrived without a registration of its own.
If filed, its record is kept in this directory and
completed by append once the approval verifies.

### DD-039-7 — Execution phase number (procedural)

The execution phase takes the next free phase
number at freeze. "Phase-401" in this draft's texts
is provisional: Specs 036–038 executions may take
numbers first, and the freeze fixes the number
actually used. Nothing substantive turns on it.

## 5. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), in the bundle
   sequence of `plan.md` — after the Spec 038
   execution and the aee 1.5.0 adoption, so the
   freeze gate runs on the adopted engine.
2. DD-039-1…DD-039-6 as recommended above, or
   amended openly in the freeze record.
3. Nothing else: the owner decisions of §1 are
   already made, and this draft re-asks none of
   them.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
