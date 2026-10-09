# Phase-129 — CISI Cropper v2 (benchmarked against the frozen v1 sample)

**ENABLING ASSET ONLY — NO SIGN IDENTIFICATIONS, NO COMPARISON STUDY**

Date: 2026-10-08. Branch `phase/129-cisi-cropper-v2`. Protocol
frozen in advance at commit `8a85c55f`
(`reports/phase129_cisi_cropper_v2_protocol.md`, committed before
any v2 tuning or grading). Predecessor: Phase-124
(`reports/phase124_cisi_image_layer.md`). Storage governance is
Phase-124's, unchanged: the scans and every derived crop live only
in the gitignored local store; this PR contains code, tests, the
protocol, this report, a counts/schema manifest
(`reports/phase129_cisi_local_store_manifest.json`) and ledger
entries — no image, crop, render or per-crop grade. Verified with
`git check-ignore -v` and a final `git status` sweep (see §6).

## 1. Method

v2 keeps v1's interpretable core signal (per-column grey-level std
over the top band of the seal photo — contrast, not darkness, for
the reason Phase-124 gave) and rebuilds the stages around it, all
deterministic, CPU-only, numpy + Pillow (no neural models):

1. **Illumination normalisation** — subtract a multi-pass box-blur
   background (18 % of photo width) before measuring, flattening
   raking-light falloff and lifting dark photos (Phase-124's
   M-213 A failure case).
2. **Sharper projection** — smoothing 2.0 % of width (v1: 4.5 %),
   so narrow signs and inter-sign gaps survive.
3. **Hysteresis edges** — runs seeded above the high threshold
   (median + 0.50 · (p97.5 − median), as v1's halfway rule), edges
   extended down to a low threshold but capped at the valley
   between neighbouring runs, so extension cannot bridge signs.
4. **Valley splitting** of over-wide runs (the "two signs merged"
   class).
5. **Content rejection** — a run must contain stroke pixels (local
   std above a photo-level bar across ≥ 30 % of its columns);
   near-uniform runs are dropped, not emitted as empty crops.
6. **Band localisation** — crop height fitted to the rows where
   the region's energy lives (padded), not the full band.

Two correctness defects were found and fixed *during development,
before grading*, each pinned by a unit test: the box blur's
cumsum slicing was wrong (a constant image did not blur to a
constant), and the y-fit's peak search could be captured by the
photo's border rows, collapsing some crops to thin top strips
(the fixed code falls back to the full v1 band when the fitted
run is implausibly short). The graded run below used the fixed
code; the harness asserts a bit-identical re-run.

## 2. Benchmark result (frozen sample, frozen rubric)

Sample identity note: the 82 v1 crops trace to **34 distinct
photo boxes** spanning the 32 CISI ID+side groups Phase-124
counted (the two `bis` exemplars carry their own boxes). v2 ran on
exactly those 34 boxes from the same 200-dpi renders; re-running
the untouched v1 segmenter reproduced all 82 frozen v1 boxes
exactly (harness assertion), so the comparison is on identical
inputs. Grades are the protocol's manual visual pass under the
Phase-124 rubric verbatim — **good** (substantially frames one
sign), **partial** (a sign cut, or two signs merged), **bad**
(motif, photo edge, blank or fragment with no sign content) —
with 15 sheet-ambiguous crops re-examined at full resolution in
photo context before finalising (changes ran in both directions:
3 partial→good, 2 good→partial, 3 bad→partial). Per-crop v2 grades
live only in the local store (`crops_v2/verification_v2.csv`).

| pipeline | good | partial | bad | total | good rate |
|---|---|---|---|---|---|
| v1 (frozen, Phase-124) | 38 | 29 | 15 | 82 | 46.3 % |
| **v2 (Phase-129)** | **50** | 42 | **15** | 107 | 46.7 % |

Frozen win definition (protocol §4): good > 38 **and** bad ≤ 15
**and** 41 ≤ total ≤ 123. **All three clauses met — v2 beats v1.**
The honest shape of the win: it is a *recall* win at constant bad
count and constant good *rate* — v2 finds more of the signs that
are actually on the plates (v1's worked sample missed whole signs:
e.g. M-214 A/a carry ~5 signs each, v1 cropped 2). It is not a
precision breakthrough, and the bad count sits exactly at the cap.

### Per-photo grade counts (v1 → v2)

| photo | v1 g/p/b | v2 g/p/b (n) | photo | v1 g/p/b | v2 g/p/b (n) |
|---|---|---|---|---|---|
| M-11 A | 0/0/2 | 0/0/3 (3) | M-214 A | 2/0/0 | 3/0/0 (3) |
| M-11 a | 0/0/3 | 0/0/1 (1) | M-214 a | 2/0/0 | 3/0/0 (3) |
| M-12 A | 3/0/0 | 2/0/0 (2) | M-215 A | 0/2/0 | 1/2/0 (3) |
| M-12 a | 0/1/0 | 1/1/0 (2) | M-215 a | 1/0/0 | 1/2/0 (3) |
| M-209 A | 1/2/0 | 0/4/0 (4) | M-216 A | 1/2/0 | 1/1/1 (3) |
| M-209 a | 1/1/0 | 3/1/1 (5) | M-216 a | 2/1/0 | 2/2/0 (4) |
| M-210 A | 1/1/0 | 1/1/0 (2) | M-217 A | 1/2/0 | 2/1/0 (3) |
| M-210 a | 1/1/0 | 1/1/0 (2) | M-217 a | 2/1/0 | 1/3/0 (4) |
| M-211 A | 1/1/0 | 1/2/0 (3) | M-67 A | 1/1/0 | 2/2/0 (4) |
| M-211 a | 0/1/0 | 2/0/0 (2) | M-67 a | 1/2/0 | 1/4/0 (5) |
| M-212 A | 2/0/0 | 3/1/0 (4) | M-68 A | 1/1/0 | 2/0/0 (2) |
| M-212 a | 2/1/0 | 1/3/0 (4) | M-68 a | 2/1/0 | 3/1/0 (4) |
| M-213 A bis | 2/0/0 | 1/1/0 (2) | M-69 A | 4/0/0 | 3/0/0 (3) |
| M-213 A | 0/0/4 | 0/0/3 (3) | M-665 A | 0/1/1 | 2/2/0 (4) |
| M-213 a | 0/1/1 | 0/2/1 (3) | M-665 a | 2/2/0 | 4/1/0 (5) |
| M-666 A | 1/0/1 | 0/1/2 (3) | M-666 a bis | 0/2/1 | 1/1/1 (3) |
| M-666 a | 1/1/1 | 1/0/1 (2) | M-667 A | 0/0/1 | 1/2/1 (4) |

### Correspondence (protocol §5: x-overlap ≥ 50 % of the narrower)

Of the 82 v1 crops: **27 good stayed good, 8 good → partial,
3 good dropped** (no v2 correspondent — in each case the sign is
inside a wider v2 crop that the 50 % rule credits to a neighbouring
v1 crop); **9 partial → good, 17 partial stayed, 2 partial → bad,
1 partial dropped**; **2 bad → good, 1 bad → partial, 9 bad stayed
bad, 3 bad dropped** (v2 emits nothing there — the desired outcome
for the M-11 / M-213 junk regions). 25 v2 crops have no v1
correspondent (10 good / 11 partial / 4 bad) — signs v1 never
proposed, plus a few new fragments.

**Regressions (grade worsened, per-crop):**
good→partial: `v1_M-209_A_p55_s02` (→ cv2_…_s02),
`v1_M-212_a_p55_s02` (→ cv2_…_s03), `v1_M-213_A_bis_p55_s01`
(→ cv2_…_s01), `v1_M-215_a_p55_s01` (→ cv2_…_s01),
`v1_M-216_a_p55_s02` (→ cv2_…_s03), `v1_M-217_a_p55_s02`
(→ cv2_…_s02), `v1_M-67_a_p30_s02` (→ cv2_…_s02),
`v2_M-666_A_p31_s01` (→ cv2_…_s02);
partial→bad: `v1_M-216_A_p55_s02` (→ cv2_…_s01),
`v2_M-666_a_p31_s03` (→ cv2_…_s02);
dropped v1 crops: `v1_M-11_a_p10_s03` (bad), `v1_M-12_A_p10_s03`
(good), `v1_M-213_A_p55_s04` (bad), `v1_M-216_A_p55_s01`
(partial), `v1_M-68_A_p30_s01` (good), `v1_M-69_A_p30_s02`
(good), `v2_M-666_a_p31_s01` (bad).
Per-photo weak spots: M-209 A (v1's one good became partial-led;
v2 over-segments that pale inscription), M-666 A (v2 emits 2 bad
of 3 — the coarse dark plate still defeats the projection), M-11
(both pipelines emit only bad crops; v2 emits fewer on the `a`
photo, more on the `A` photo).

## 3. Expansion (gate opened — win definition met)

v2 ran over the full Phase-124 catalogue: every row with side
A/a, a recorded photo box and a non-degenerate box (h ≤ 1.5 w),
excluding the 34 benchmark photo boxes — **5,247 photos processed
of 5,281 eligible, 0 skipped for missing renders** — cut from the
140-dpi page cache. Result: **14,166 crops** (Vol. 1: 6,438;
Vol. 2: 7,728) covering **3,287 distinct CISI IDs** (of the
catalogue's 3,494), all in the local store under
`crops_v2_expansion/`. Manifest↔disk consistency is exact
(14,166 rows = 14,166 unique filenames = 14,166 PNGs).

Engineering note, kept because it changed numbers: the first
expansion attempt was discarded — its benchmark exclusion matched
only 4 of 34 photos (it re-scaled catalogue boxes with `round()`
where the v1 driver used `int()` truncation) and 7 of its
filenames collided (the same ID+side+printed page occurs on two
distinct photos). The harness now truncates identically, embeds
the PDF page + box origin in expansion filenames, and asserts
filename uniqueness; an early runtime summary quoting yet another
(physically impossible: > 5,281 eligible photos) set of counts
was likewise discarded unverified. All counts above are from the
clean re-run, verified against the catalogue and the disk.

Fixed-seed (129) spot-check of 30 expansion crops, graded under
the same rubric for context only: **8 good / 10 partial / 12 bad**
— materially below the benchmark rate, as expected: the expansion
pool covers every catalogue object type (tablets, pottery and
other objects whose text is not a top-band seal inscription) at
140 dpi, not only seal plates. The expansion is an ungraded
candidate pool for later human/machine study, exactly as v1's
crops were region proposals.

## 4. Verification

- New unit tests: `backend/tests/test_phase129_cisi_cropper_v2.py`
  — **12 passed** (normalisation, gate map, blank rejection,
  three-sign detection, the dark-photo case, pale grooves,
  valley split / no-split, border-strip y-fit, determinism).
- Benchmark harness assertions: v1 boxes reproduced exactly;
  v2 re-run bit-identical.
- Full backend suite: **923 passed / 13 skipped / 0 failed**
  (includes the 12 new tests; the skip split differs from the
  main-checkout baseline because the gitignored corpora are absent
  in a fresh worktree, as in CI). Foundation check (corpora
  symlinked from the main checkout): **40 passed / 0 failed /
  8 warnings** — unchanged from the Phase-119 baseline.
  Test side-effect modifications (claims JSONs, outputs/) were
  reverted before commit.
- Ruff: clean on all new files.
- Anchors file sha256 unchanged (eccea6d5…), asserted before and
  after.

## 5. Non-claims

- Enabling asset only: no sign identifications are asserted by
  any crop; filenames carry object IDs and geometry only.
- The win is stated exactly as the frozen protocol defined it —
  a good-count win at the bad-count cap, not a claim that v2 is
  uniformly better (per-photo regressions are listed above).
- Expansion crops are ungraded proposals (30-crop spot-check
  excepted, context only); no anchor, tier or corpus statistic
  was changed by this phase.
- No in-copyright image or derived table is in this PR.

**AI disclosure:** execution recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.
