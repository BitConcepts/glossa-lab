# Phase-135 Pilot Report — Spec 024 Stage 1: Motif-Coding Re-Pilot (clarified codebook, fresh sample)

**Phase:** 135 · **Spec:** 024 (evidence integration), Stage 1
continuation · **Design freeze:**
`specs/024-evidence-integration/stage1-freeze-2.md` (freeze
commit `dee4e5c2`, committed before the frame was drawn and
before any re-pilot image was viewed) · **Frame:**
`data/evidence_integration/phase135_pilot_frame.json` (frame
commit `07de144a`) · **Dataset:**
`data/evidence_integration/phase135_pilot_dataset.json`
(+ `_meta.json`) · **Metrics:**
`reports/phase135_pilot_metrics.json`, computed by
`backend/scripts/phase135_metrics.py` from the on-disk coding
records only. **No association statistic of any kind was
computed in this phase** (spec §4.1 fence).

> **AI disclosure (constitution §VI; spec §4.4).** Every
> coding role in this re-pilot — pass A, pass B, the gold third
> coding, and the adjudicator — was executed by an AI agent
> (Muse Spark, via Muse) in a blinded,
> role-isolated instance, at the direction of Tristen
> Pierson. Agreement numbers below are properties of this
> coding pipeline. They are not, and must not be cited as,
> measurements of human expert coding.

## 1. Question

Phase-134 measured exact agreement 0.84 / κ 0.7885 —
**MIDDLE BAND** under the frozen §4.5 gates — with its
disagreement concentrated on the legibility boundary
(10 of 16 disagreements involving ILLEGIBLE). The owner
directed the combined path (2026-10-09): clarify that
boundary from Phase-134's adjudicated record, re-pilot on a
fresh sample under identical gates, and freeze a Stage 2(b)
design only if the proceed gate is met. This report is the
re-pilot. It measures **coding reliability only**, under the
clarified codebook. It tests no association and validates
no motif against any external coding.

## 2. What changed, and what did not

Changed, by `stage1-freeze-2.md` §2 only: five decision
rules (B1–B5) defining the ILLEGIBLE / SCRIPT_ONLY /
GEOMETRIC boundary and the classifiability threshold,
distilled from the 16 adjudicated Phase-134 disagreements
and given to coders as worked examples — the only
Phase-134 material any coder saw.

Unchanged, restated in freeze-2 §3 so there is no
ambiguity: the 12-code taxonomy and its visual
definitions; the primary-motif precedence rule; the
metric definitions; the protocol; and **every gate
threshold** — proceed at exact agreement ≥ 0.85 **and**
κ ≥ 0.75, stop below 0.70 or κ < 0.50. No gate moved by
any amount.

## 3. Frame and freshness

Population: the frozen §4.2 eligible population (3,245
objects) **minus the 100 Phase-134 frame objects** →
3,145 eligible. Draw: exactly 100 objects, stratified
site-group × object type, proportional largest-remainder
allocation with a 2-per-cell floor over the reduced
population, selection by ascending
sha256(`phase135-20261009|` + canonical key) within each
cell; gold subset = every 5th object of the hash-ordered
frame (20 objects). Cell quotas: Mohenjo-Daro Seals 32 /
Tablets 11 / Graffiti 2; Harappa Seals 17 / Tablets 14 /
Graffiti 8; Other Seals 12 / Tablets 2 / Graffiti 2 (the
reduced population's proportions round to the same quotas
as Phase-134). **Freshness check: overlap with the
Phase-134 frame = 0**, asserted by the frame script at
draw time and verified independently against both
committed frame records. All 100 objects yielded crops
(210 crops, 0 failures); no replacement was needed and
the frame never changed after commitment.

## 4. Protocol as executed, and deviations

Identical to Phase-134 in every procedural respect:
packets of canonical keys + image paths only (no site,
type, chapter, Holdat field, or prior coding); passes A
and B coded all 100 objects in four batches of 25 (pass B
in rotated order); the gold pass coded the 20-object
subset; a separate adjudicator instance ruled all 22
disagreements from the photographs with both passes'
codes and notes visible. Each coder wrote one JSON record
per object immediately after coding it; record-file
timestamps are the effort record. All quantities below
were computed by script from the final on-disk record
sets, verified complete before the metrics run (A 100,
B 100, gold 20, adjudication 22 — the metrics script's
fail-loud checks passed on the first run: record sets
exact, no duplicates, adjudication set identical to the
disagreement set).

**Deviations: none.** No top-up coding was commissioned;
no record was excluded; the codebook as executed is the
frozen §4.3 taxonomy plus the freeze-2 clarification,
verbatim.

## 5. Results (pre-adjudication pass A vs pass B, full sample, n = 100)

| Quantity | Value |
|---|---|
| Exact primary-motif agreement | **0.78** (78/100) |
| Cohen's κ | **0.7129** (observed agreement 0.78; chance agreement Pe = 0.2338 from the marginals below) |
| Adjudication rate | 0.22 (22/100) |
| Adjudication outcomes | pass A upheld 16 · pass B upheld 6 · neither 0 |

Marginals (counts of primary codes assigned):

| Code | Pass A | Pass B |
|---|---|---|
| UNICORN | 29 | 29 |
| ZEBU | 0 | 0 |
| BUFFALO | 2 | 4 |
| ELEPHANT | 3 | 7 |
| RHINOCEROS | 2 | 1 |
| GOAT_ANTELOPE | 2 | 1 |
| TIGER | 2 | 2 |
| COMPOSITE | 0 | 0 |
| HUMAN_CULT | 2 | 2 |
| GEOMETRIC | 8 | 8 |
| SCRIPT_ONLY | 36 | 34 |
| ILLEGIBLE | 14 | 12 |

Per-category agreement (agreements ÷ objects coded with
that category by either pass): SCRIPT_ONLY 0.750 (30/40) ·
UNICORN 0.758 (25/33) · GEOMETRIC 0.778 (7/9) · ILLEGIBLE
0.368 (7/19) · TIGER 1.0 (2/2) · HUMAN_CULT 1.0 (2/2) ·
RHINOCEROS 0.5 (1/2) · ELEPHANT 0.429 (3/7) · BUFFALO 0.2
(1/5) · GOAT_ANTELOPE 0 (0/3) · ZEBU, COMPOSITE — (no
objects). The small categories rest on 2–7 objects and
their rates are correspondingly unstable; the
interpretable mass sits in the four large categories.

**Confusion structure.** 12 of the 22 disagreements
involve ILLEGIBLE on one side: SCRIPT_ONLY×ILLEGIBLE 8
(5 + 3 by direction), ILLEGIBLE×UNICORN 2,
ILLEGIBLE×ELEPHANT 1, ILLEGIBLE×GEOMETRIC 1. The
remaining 10 are identity/boundary calls among
depictions: UNICORN×ELEPHANT 2, UNICORN×BUFFALO 2, and
GOAT_ANTELOPE×BUFFALO, GOAT_ANTELOPE×UNICORN,
RHINOCEROS×UNICORN, BUFFALO×ELEPHANT,
GEOMETRIC×SCRIPT_ONLY, SCRIPT_ONLY×GOAT_ANTELOPE (1
each). Two shifts against Phase-134 are descriptive
facts of this run: ILLEGIBLE was used far less (marginals
14/12 vs 27/23 in Phase-134 — the clarification's Rules
B3/B5 push coders to commit where a depiction is absent
or a feature is discernible), yet ILLEGIBLE's own
per-category agreement fell (0.368 vs 0.667); and
depiction-identity disagreements roughly doubled their
share (10 of 22 vs 6 of 16).

**Gold-subset drift (20 triple-coded objects).**
Pairwise exact agreement: A–B 0.75, A–G 0.90, B–G 0.75;
all three unanimous on 0.75. The third coding sits inside
the same agreement band as the A–B pair; no pass is an
outlier.

**Adjudicated final distribution (descriptive):**
SCRIPT_ONLY 38, UNICORN 30, ILLEGIBLE 10, GEOMETRIC 8,
ELEPHANT 4, GOAT_ANTELOPE 2, RHINOCEROS 2, TIGER 2,
BUFFALO 2, HUMAN_CULT 2, ZEBU 0, COMPOSITE 0. Stated as
composition only: 78 of 100 objects resolved to
script-only, illegible, or unicorn; identifiable
non-unicorn depictions remain thin. This re-pilot draws
no inference from it.

## 6. Gate application (frozen §4.5, identical numbers, applied exactly)

- **Proceed gate** — exact agreement ≥ 0.85 **and**
  κ ≥ 0.75: agreement 0.78 < 0.85 and κ 0.7129 < 0.75 →
  **NOT MET** (both arms short this time).
- **Stop rule** — exact agreement < 0.70 **or**
  κ < 0.50: **NOT FIRED** (0.78 and 0.7129 are both
  clear).

**Verdict: MIDDLE BAND — for the second time.** Per
freeze-2 §5, no Stage 2(b) design is drafted on this
outcome; the motif arm is **not** eligible for
Stage 2(b) on either pilot, and this report makes no
recommendation dressed as a verdict.

## 7. Both pilots, side by side

| Quantity | Phase-134 (original codebook) | Phase-135 (clarified codebook) |
|---|---|---|
| Sample | 100 fresh objects | 100 fresh objects (0 overlap) |
| Exact agreement | 0.84 | 0.78 |
| Cohen's κ | 0.7885 | 0.7129 |
| Disagreements | 16 | 22 |
| … involving ILLEGIBLE | 10/16 | 12/22 |
| ILLEGIBLE marginals (A/B) | 27 / 23 | 14 / 12 |
| ILLEGIBLE per-category agreement | 0.667 | 0.368 |
| Proceed gate | not met (agreement arm) | not met (both arms) |
| Stop rule | not fired | not fired |
| Verdict | MIDDLE BAND | MIDDLE BAND |

The two pilots differ in both sample and codebook, so
this is not a controlled comparison; what can be said
plainly is this: **on a fresh sample, under the clarified
codebook, this pipeline's measured reproducibility was
lower, not higher.** The clarification changed coder
behavior in its intended direction — ILLEGIBLE calls
halved — but agreement did not follow: the coders split
instead on the residual legibility cases and, more often
than before, on which depiction a worn object shows.
The Phase-134 hope that the disagreement was mostly one
definitional boundary is not supported by this run: the
boundary moved, and the disagreement moved with it.

## 8. The owner's decision, framed

Per the frozen rule, the choice is the owner's. On this
record, the measured pipeline reproduces a primary motif
code 78–84% of the time (κ 0.71–0.79) across two fresh
samples and two codebook versions, with neither pilot
reaching the frozen proceed gate and neither approaching
the stop rule. The paths from here are fresh owner
decisions, none taken by this report: (a) accept one of
the measured pilots as the reliability basis for a
Stage 2(b) design, knowingly below the frozen gate —
this would be a new adjudication, not a reading of
either pilot; (b) change the measurement basis itself
(e.g. human expert coders, or a materially different
coding instrument) and re-measure; (c) let the motif arm
rest here, with the Stage 0 inventory and both pilots as
its final record. Each path is available; the frozen
gates as written have now answered twice, and they do
not answer "proceed."

Publication is not among the open questions: the owner
approved publication of the combined motif-arm record
with the combined path, and both pilot datasets are
deposited with that record (Zenodo v4.7.0; codes, notes,
and disagreement logs — no images).

## 9. Descriptive concordance (freeze §6 — concordance, never accuracy)

Of the 100 sampled objects, 30 carry a unicorn-family
`motif_chapter` value in the catalogue. Their adjudicated
codes: UNICORN 26, other 4. The catalogue chapter is a
finding aid assigned for plate organization; this count
describes how the fresh blinded coding relates to it and
is not an accuracy measurement in either direction.
NONMAPPABLE chapter families were excluded by the frozen
rule; none occurred in the frame. No comparison against
Holdat's `iconography` field was made — the object-level
join does not exist (Phase-133).

## 10. Effort (record-file timestamps; AI-agent wall times)

Per-object coding time (median, by batch) ran 9.5–17.3 s
across the eight main-pass batches (pass means
10.1–20.0 s); the gold batch median was 18.8 s.
Adjudication: 22 objects, median 16.8 s per object. These are wall times
of this AI pipeline under this protocol, stated so a
future human or machine replication can budget against
them; they are not human coding times.

## 11. Fences observed

No association statistics; no accuracy claim against any
external coding; no anchor, claim, or PRED change; no
Holdat comparison; images never entered git (crops live
only in the gitignored local CISI store); the dataset
carries codes and notes only. No gate threshold was
altered at any point.

## 12. Artifacts

- Freeze record: `specs/024-evidence-integration/stage1-freeze-2.md`
- Frame + draw script + tests: `data/evidence_integration/
  phase135_pilot_frame.json`, `backend/scripts/phase135_frame.py`,
  `backend/tests/test_phase135_frame.py`
- Dataset + meta: `data/evidence_integration/
  phase135_pilot_dataset.json`, `..._meta.json`
- Metrics + script + tests: `reports/phase135_pilot_metrics.json`,
  `backend/scripts/phase135_metrics.py`,
  `backend/tests/test_phase135_metrics.py`
- Local only (never in git): the 210 crops, coder packets,
  the clarified codebook as issued, and raw per-object records
  under the gitignored CISI image store
  (`corpora/downloads/cisi_image_layer/phase135_pilot/`).
