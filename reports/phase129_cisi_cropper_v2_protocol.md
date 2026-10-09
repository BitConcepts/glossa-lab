# Phase-129 — CISI Cropper v2: FROZEN BENCHMARK PROTOCOL

**Status: FROZEN.** This protocol is committed on its own, before any
v2 code is tuned and before any v2 grading run. Its definitions do not
change after this commit; any deviation discovered later is reported
as a deviation in the final report, not edited away here.

Date: 2026-10-08. Branch `phase/129-cisi-cropper-v2`.
Predecessor: Phase-124 (`reports/phase124_cisi_image_layer.md`,
`reports/phase124_cisi_local_store_manifest.json`).

## Storage governance (unchanged from Phase-124)

The CISI scans and every derived crop are in-copyright research
material. They live **only** in the gitignored local store
(`~/workspace/glossa-lab/corpora/downloads/cisi_image_layer/`, main
checkout; verified ignored via `.gitignore:176:corpora/`). This phase
commits code, tests, this protocol, the final report and a
manifest-schema note only — never an image, a crop, a page render, or
a per-crop grade. v2 outputs go to the local store under
`crops_v2/` (benchmark) and `crops_v2_expansion/` (expansion, if the
gate opens); v2 crop files are prefixed `cv2_` (the v1 files' `v1_`/
`v2_` prefixes denote the *volume*, not a pipeline version, so a
distinct prefix prevents any overwrite of the frozen v1 sample).

## 1. The benchmark sample (frozen)

The benchmark is the Phase-124 worked sample, identically:

- the **32 seal photographs** (sides A/a) on four plate pages —
  Vol. 1 PDF pp. 66 and 46 (printed 30, 10), Vol. 1 PDF p. 91
  (printed 55), Vol. 2 PDF p. 66 (printed 31) — that produced v1
  crops, identified photo-by-photo by the photo boxes recorded in
  the local store's `crops/verification.csv` (sha256
  `6b965fc8db345148b7ac75e0477a5cc749e327f2a0c5fcb0a084a6a0a1430044`,
  200-dpi page renders in `page_cache_200/`);
- v2 runs on exactly those 32 photographs, cut from the same
  200-dpi renders using exactly those recorded photo boxes;
- the one further photo in the v1 manifest (M-667 a, Vol. 2 p. 66),
  skipped by v1 for a degenerate merged photo box, stays excluded:
  it contributed no v1 crop and is not part of the 82.
- v1 produced **82 crops** from those 32 photos.

## 2. The rubric (Phase-124, verbatim — not redefined)

Phase-124 graded every crop by visual inspection on contact sheets:

> **good** (substantially frames one sign), **partial** (a sign cut,
> or two signs merged), **bad** (motif, photo edge, blank or fragment
> with no sign content)

Phase-124's documented failure modes, also verbatim in substance:
touching signs merge into one region; signs split at low-contrast
strokes; motif elements intruding into the top band (horns, the
'manger' standard) add spurious regions; the boss/back side and blank
seal edges yield empty regions; one photo (M-213 A, Vol. 1 printed
p. 55) is so dark that all four of its regions are fragments;
multi-row inscriptions are truncated at the band edge. The pipeline
background (Phase-124 §2): "the raking-light photographs render signs
as pale grooves with dark shadow edges, and a dark-pixel projection
mostly finds the animal motif" — v1 therefore projected per-column
grey-level **std**, and the pale-groove weakness of that single
global projection is the failure mode v2 attacks.

## 3. Frozen baseline

v1's grades are taken from the Phase-124 manifest as-is and are
**not** re-graded:

| pipeline | good | partial | bad | total |
|---|---|---|---|---|
| v1 (frozen) | **38** | 29 | **15** | 82 |

## 4. "v2 beats v1" — frozen definition

v2 is run once, with one fixed parameter set applied uniformly to
all 32 photos (no per-photo hand-tuning), over the sample of §1.
Every crop v2 produces is graded under the §2 rubric. Then:

> **v2 beats v1 iff (a) v2 good-count > 38, AND (b) v2 bad-count
> ≤ 15, AND (c) 41 ≤ v2 total crops ≤ 123.**

Clause (c) is an anti-gaming bound fixed in advance: a win may not
be manufactured by flooding the sample with overlapping candidate
crops (or by emitting almost none). Good-rate, partial-count and
per-photo transitions are reported as context but do not decide the
gate. If any clause fails, v2 does not beat v1, the negative
benchmark is the shipped result, and the expansion gate stays shut.

## 5. Grading procedure (frozen)

Phase-124's grading was a manual visual pass, so v2's grading is
the same kind of pass, documented here so it is reproducible:

1. v2 crops are rendered into contact sheets (per page, labelled by
   crop filename only) plus kept as individual PNGs.
2. The executing agent inspects every v2 crop visually (contact
   sheet first, individual crop at full resolution whenever the
   sheet is ambiguous) and assigns good / partial / bad under §2,
   without consulting the v1 grade of any corresponding v1 crop
   during the pass.
3. Per-crop v2 grades are recorded **only** in the local store
   (`crops_v2/verification_v2.csv`, same columns as v1's
   `verification.csv` plus the v2 crop box). They never enter git.
   Git receives aggregate counts and per-photo transition counts.
4. Correspondence for the regression analysis: a v1 crop and a v2
   crop on the same photo *correspond* when their x-intervals
   overlap by ≥ 50 % of the narrower interval (v1 boxes span the
   full band height, so correspondence is judged on x). A v1 crop
   whose grade worsens against its corresponding v2 crop(s)
   (good→partial/bad, partial→bad), a v1 crop with no corresponding
   v2 crop, and a v2 crop with no v1 correspondent are each listed
   in the final report's regression/improvement tables by photo and
   crop filename (filenames carry object IDs and geometry only, as
   in the Phase-124 committed manifest).

## 6. Method constraints (frozen)

v2 must be deterministic, CPU-only, classical image processing
(numpy + Pillow, as v1) — no neural models, per program doctrine.
It attacks the §2 failure mode (pale raking-light grooves defeating
a single global contrast projection); the permitted attack surface
is illumination/raking-light normalisation, local/adaptive
contrast measures, hysteresis or multi-threshold segmentation,
valley-splitting of merged regions, inscription-band localisation,
and content-based rejection of empty regions. Parameters are tuned
against synthetic tests and aggregate diagnostics only; the graded
run uses the committed parameter set exactly once for the record
(re-runs must reproduce it bit-for-bit; the harness asserts this).

## 7. Expansion gate (frozen)

Expansion happens **only if** §4 is satisfied. If it opens:

- v2 runs over every catalogue row (both volumes, local catalogue
  CSVs) with side A/a, a recorded photo box, and a non-degenerate
  box (h ≤ 1.5 w), cut from the 140-dpi page cache
  (`page_cache/`), excluding the 32 benchmark photos (already
  cropped at 200 dpi);
- expansion crops are **ungraded**, except a fixed-seed (129)
  pseudo-random spot-check of 30 crops graded under §2 for report
  context only — it decides nothing;
- the expansion (total crops, distinct CISI IDs, per-volume counts)
  is recorded in the local manifest; the git report carries
  **counts only**.

If §4 fails, no expansion is run and the report says so.

## 8. What is committed

v2 code (`backend/glossa_lab/cisi_cropper_v2.py`), the benchmark /
expansion harness (`scripts/phase129_cisi/`), tests
(`backend/tests/test_phase129_cisi_cropper_v2.py`), this protocol,
the final report (`reports/phase129_cisi_cropper_v2.md`) with the
v1-vs-v2 grade table, per-class regression list and the expansion
decision, a local-store manifest for Phase-129 in the Phase-124
format (counts and schema only), and ledger entries. Anchors file
(`backend/reports/INDUS_FINAL_ANCHORS.json`, sha256 eccea6d5…) is
not touched by this phase.

**AI disclosure:** execution recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.
