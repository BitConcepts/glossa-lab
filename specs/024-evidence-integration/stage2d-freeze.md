# Spec 024 — Stage 2(d) Freeze Record (Phase-138)

> ## FROZEN 2026-10-09 — arm (d), graffiti descriptive protocol
>
> Frozen under spec 024 §5 / §12 on the owner's
> instruction of record: **Tristen Pierson,
> 2026-10-09 — "Do all next things"** (arm (b) is
> CLOSED per `motif-arm-closure.md` and is not
> touched). This freeze is committed and merged
> **before** any Phase-138 code runs. It
> operationalizes the §5.5 sketch **as a
> descriptive protocol only**, on the Phase-133
> Stage 0 numbers. Boundary 4 binds throughout:
> graffiti material is **never pooled** with seal
> texts, and **no test of any kind** is computed in
> this arm — it is not a member of the Stage 2
> family declared in `stage2a-freeze.md` §1.

**Phase:** 138 · **Spec:** 024 §5.5 (arm (d)) ·
**Family role:** none (descriptive only) ·
**Date:** 2026-10-09.

**AI disclosure:** this freeze, and the execution
it governs, are produced by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

---

## 1. Population (frozen; design-audit counts recorded)

All Phase-124 catalogue rows (CISI Vols. 1–2) whose
`object_type` is exactly `Graffiti`: **417 photo
rows** (Vol. 1: 119; Vol. 2: 298) over **395
distinct volume-scoped objects** (canonical key
`cisi:v{volume}:{printed_id}`). Execution
recomputes and reports the population as run. No
other layer's graffiti-labelled rows enter this
arm (the ICIT-lineage and Holdat type fields were
inventoried by Stage 0 as graffiti-adjacent
material; they are not the catalogue population
this protocol describes, and adding them would
pool compilations descriptively in a way this
freeze does not authorize).

## 2. Frozen descriptive outputs (counts, proportions, medians — nothing else)

Computed by script from the catalogue files;
every number traceable to the population of §1:

1. Rows and distinct objects by volume.
2. Distinct objects by catalogue `site` (Class O),
   including the no-site count, all sites shown.
3. Photo-rows-per-object distribution (how many
   objects carry 1, 2, 3, … photographed
   sides/views), by volume and pooled.
4. `side` and `bis` value counts as printed.
5. `motif_chapter` (Class C, CISI editors' chapter
   organization): filled rows / rate, and the
   distinct values with counts as printed —
   including spelling variants and heading strings
   as found (Phase-133 §6.4 discipline: recorded,
   never cleaned).
6. `caption_ocr_score` and `scale_pct`: median and
   interquartile range where present, with the
   present-count stated (extraction-quality
   descriptors of the catalogue itself).
7. Context table (descriptive only): the same
   site distribution and rows-per-object
   distribution computed for catalogue `Seals` and
   `Tablets` rows, placed beside §2.2–2.3 so the
   graffiti subset's catalogue shape can be read
   against the corpus it sits in. This is a
   description of catalogue composition; it is not
   a comparison of repertoires and licenses no
   inference.
8. **Qualitative comparative paragraph** on the
   Kodumanal volume, restating Phase-133 §6.1's
   record: a trench-organized excavation report
   whose Graffiti Marks section describes marks by
   ware and vessel position (shoulder near the
   rim), pre-firing vs surface. Its printed tallies
   are quoted as prose only, with their internal
   inconsistency stated (subtotals summing to 225
   against a stated 175); **no tally from the
   volume is used as a count**.

## 3. Statements that must appear, verbatim in effect, in every output of this arm

- The Tamil Nadu graffiti corpus (tngraffiti.in)
  is **not in hand — 0 records** (access requested
  2026-10-08; no reply on record). No number in
  this arm describes it.
- **Dating-gap caveat:** the Tamil Nadu graffiti
  material is separated from the Indus material by
  **≥ 1,000 years** on the published rebuttal of
  the continuity claims (the Harappa.com critique
  of Rajan & Sivanantham). Any resemblance ever
  noted across that gap is formal resemblance
  across a millennium-plus separation — nothing
  more.
- A permitted output of this arm is
  "resemblance measured / described"; a prohibited
  output is any continuity, descent, or survival
  claim (spec §5.5).

## 4. Prohibited outputs (frozen)

- No association test, significance statement, or
  p-value, in any form.
- No pooling of graffiti rows with seal or tablet
  texts in any table that presents itself as a
  joint repertoire.
- No overlap statistic against the seal-text sign
  repertoire: **no machine-readable sign-form
  repertoire of the catalogue graffiti objects
  exists in hand** (the catalogue records
  photographs and captions, not transcriptions;
  Phase-132 closed the program's attempt to
  manufacture transcriptions from plates). The
  §5.5 sketch's "overlap and distribution
  statistics" are therefore **not computable from
  material in hand**; this freeze narrows the arm
  to the descriptives of §2 and says so, rather
  than substituting another layer's transcriptions
  under the graffiti label.
- No continuity, descent, or survival claim (§3).

## 5. Assumptions and epistemic boundaries (H13)

- **Assumptions:** (D1) catalogue `object_type` =
  `Graffiti` is the CISI editors' classification as
  extracted by Phase-124 (sample field accuracy
  98.9%, Phase-124 record); rows are described
  under that classification without re-adjudication.
  (D2) Descriptive statements describe the
  catalogue's record of the objects, which is a
  publication-selection of the excavated material,
  not the excavated population itself; the report
  states this where site distributions are shown.
- **Boundaries:** spec §8 governs verbatim. This
  arm produces description only; it can support no
  claim about what graffiti marks mean, whether
  they are writing, or how they relate historically
  to the Indus script.

## 6. Deliverables (Phase-138)

Per governance H15/H23 (graph-first, 5-step gate —
the graph node exposes the descriptive summary;
no experiment in the inferential sense is run):
script `backend/scripts/phase138_graffiti_descriptive.py`;
graph module
`backend/glossa_lab/experiment_graph_phase138.py`
(node `IndusPhase138GraffitiDescriptive`),
registered and verified before the run; tests
`backend/tests/test_phase138_graffiti_descriptive.py`;
results `reports/phase138_results.json`; report
`reports/phase138_report.md`. Foundation check
(H21): 0 failures. Anchors asserted byte-identical
(sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`).

## 7. Deviations

None at freeze. Execution deviations, if any, are
recorded in the phase report with the rule that
resolved them.
