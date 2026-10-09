# Phase-134 Pilot Report — Spec 024 Stage 1: Motif-Coding Pilot

**Phase:** 134 · **Spec:** 024 (evidence integration), Stage 1 ·
**Design freeze:** `specs/024-evidence-integration/stage1-freeze.md`
(freeze commit `633e943e`, before any sample image was viewed) ·
**Frame:** `data/evidence_integration/phase134_pilot_frame.json`
(frame commit `e51d0637`) · **Dataset:**
`data/evidence_integration/phase134_pilot_dataset.json` (+ `_meta.json`) ·
**Metrics:** `reports/phase134_pilot_metrics.json`, computed by
`backend/scripts/phase134_metrics.py` from the on-disk coding records
only. **No association statistic of any kind was computed in this
phase** (spec §4.1 fence).

> **AI disclosure (constitution §VI; spec §4.4, as adjudicated at
> freeze).** Every coding role in this pilot — pass A, pass B, the
> gold third coding, and the adjudicator — was executed by an AI agent
> (Muse Spark, via Muse) in a blinded, role-isolated
> instance, at the direction of Tristen Pierson. Agreement numbers
> below are properties of this coding pipeline. They are not, and must
> not be cited as, measurements of human expert coding.

## 1. Question

Can the frozen 12-code motif taxonomy (spec §4.3) be applied to CISI
Vol. 1–2 object photographs reproducibly — two independent blinded
codings agreeing at the frozen §4.5 level? The pilot measures
**coding reliability only**. It tests no association and validates no
motif against any external coding.

## 2. Premise correction (recorded at freeze, before the draw)

The commissioning shorthand described the population as the 909
catalogue objects carrying a `motif_chapter` value. That population is
degenerate for a reliability pilot: **899 of the 909 (98.9%) sit in
unicorn chapters** (counted from the catalogue, counting OCR chapter
variants), so a sample drawn from it could not exercise the taxonomy.
The frozen spec's §4.2 population governs and was used instead: all
catalogue objects with at least one parseable photo box and
`object_type` ∈ {Seals, Tablets, Graffiti} — **3,245 eligible objects**
(249 catalogue objects excluded: other types or no parseable box).
`motif_chapter` enters only as the §6 descriptive concordance.

Frame: exactly 100 objects, stratified site-group (Mohenjo-Daro /
Harappa / Other) × object type, proportional allocation by largest
remainder with a 2-per-cell floor; selection by ascending
sha256(`phase134-20261009|` + canonical key) within each cell; gold
subset = every 5th object of the hash-ordered frame (20 objects,
triple-coded). Cell quotas: Mohenjo-Daro Seals 32 / Tablets 11 /
Graffiti 2; Harappa Seals 17 / Tablets 14 / Graffiti 8; Other Seals 12
/ Tablets 2 / Graffiti 2. All 100 sampled objects yielded crops (220
crops, 0 failures); **no replacement was needed and the frame never
changed after commitment.**

## 3. Protocol as executed, and deviations

Coders received packets containing canonical keys and image paths
only — no site, type, chapter, Holdat field, or any prior coding.
Each coder viewed enlarged crops of the object's plate boxes and
wrote one JSON record per object immediately after coding it
(record-file timestamps are the effort record). Passes A and B coded
all 100 objects in four batches of 25; the gold pass coded the
20-object subset; a separate adjudicator instance ruled the 16
disagreements from the photographs with both passes' codes and notes
visible. Agreements stand as coded; the disagreement log is preserved
in full in the dataset.

**Deviation D1 — a completion handoff raced its own final writes
(process finding; data impact: none).** Pass A batch 2's completion
message reported 25 records written; a verification snapshot taken at
that moment found 23 on disk (the final two records landed seconds
later — the same failure *shape* as the Phase-132 §4(d) finding,
arriving from the opposite direction). Acting on the snapshot, the
coordinator commissioned a fresh blinded top-up coding of the two
apparently-missing objects (`cisi:v1:K-52`, `cisi:v1:M-545`). When the
batch's own two records were found on disk, the metrics script's
fail-loud duplicate check stopped assembly until the conflict was
resolved by rule: **the original batch records govern; the top-up
records are excluded from every quantity** (they remain in the local
store, unused). The duplication was substantively benign — the two
codings agree on both objects (K-52: SCRIPT_ONLY in both; M-545:
ILLEGIBLE in both) — but it is recorded here because the pilot's own
quantities were nearly assembled from a snapshot instead of the
records. All numbers in this report are computed from the final
on-disk record sets, verified complete (A 100, B 100, gold 20,
adjudication 16) before the metrics run.

**No other deviations.** The codebook as executed is the frozen §4.3
taxonomy verbatim: 12 primary codes, the frozen precedence rule for
the primary code, secondary motifs recorded but unanalysed, the boss /
reverse side never treated as a depiction. No coder saw any field the
freeze forbids.

## 4. Results (pre-adjudication pass A vs pass B, full sample, n = 100)

| Quantity | Value |
|---|---|
| Exact primary-motif agreement | **0.84** (84/100) |
| Cohen's κ | **0.7885** (observed agreement 0.84; chance agreement Pe = 0.2436 from the marginals below) |
| Adjudication rate | 0.16 (16/100) |
| Adjudication outcomes | pass A upheld 10 · pass B upheld 6 · neither 0 |

Marginals (counts of primary codes assigned):

| Code | Pass A | Pass B |
|---|---|---|
| UNICORN | 25 | 27 |
| ZEBU | 1 | 0 |
| BUFFALO | 1 | 3 |
| ELEPHANT | 1 | 2 |
| RHINOCEROS | 1 | 0 |
| GOAT_ANTELOPE | 3 | 3 |
| TIGER | 1 | 1 |
| COMPOSITE | 1 | 2 |
| HUMAN_CULT | 0 | 0 |
| GEOMETRIC | 7 | 5 |
| SCRIPT_ONLY | 32 | 34 |
| ILLEGIBLE | 27 | 23 |

Per-category agreement (agreements ÷ objects coded with that category
by either pass): SCRIPT_ONLY 0.833 (30/36) · UNICORN 0.793 (23/29) ·
GEOMETRIC 0.714 (5/7) · ILLEGIBLE 0.667 (20/30) · TIGER 1.0 (1/1) ·
ELEPHANT 0.5 (1/2) · COMPOSITE 0.5 (1/2) · GOAT_ANTELOPE 0.5 (2/4) ·
BUFFALO 0.333 (1/3) · ZEBU 0 (0/1) · RHINOCEROS 0 (0/1) · HUMAN_CULT —
(no objects). The small categories rest on 1–4 objects and their rates
are correspondingly unstable; the interpretable mass sits in the four
large categories.

**Confusion structure.** 10 of the 16 disagreements involve ILLEGIBLE
on one side: ILLEGIBLE×UNICORN 3, ILLEGIBLE×SCRIPT_ONLY 5 (3 + 2 by
direction), ILLEGIBLE×ELEPHANT 1, GEOMETRIC×ILLEGIBLE 1. The remaining
6 are identity/boundary calls among depictions: ZEBU×UNICORN,
UNICORN×GOAT_ANTELOPE, UNICORN×BUFFALO, RHINOCEROS×BUFFALO,
GOAT_ANTELOPE×COMPOSITE, GEOMETRIC×SCRIPT_ONLY (1 each). The
disagreement mass is therefore concentrated on **the legibility
boundary for worn objects** — whether a depiction is present and
classifiable at all — rather than on animal identity among clearly
visible depictions.

**Gold-subset drift (20 triple-coded objects).** Pairwise exact
agreement: A–B 0.80, A–G 0.85, B–G 0.75; all three unanimous on 0.70.
The third coding sits inside the same agreement band as the A–B pair;
no pass is an outlier, and the same boundary moves all three coders
(e.g. `cisi:v1:H-301`: A and B both ILLEGIBLE, gold HUMAN_CULT — an
A–B agreement the third coder read as a worn human scene).

**Adjudicated final distribution (descriptive):** SCRIPT_ONLY 34,
ILLEGIBLE 26, UNICORN 26, GEOMETRIC 6, COMPOSITE 2, GOAT_ANTELOPE 2,
ELEPHANT 1, TIGER 1, BUFFALO 1, RHINOCEROS 1, ZEBU 0, HUMAN_CULT 0.
Stated as composition only: in a proportional draw across seals,
tablets, and graffiti, 86 of 100 objects resolved to script-only,
illegible, or unicorn; identifiable non-unicorn animal depictions are
thin on the ground. Any future Stage 2(b) design inherits that base
rate; this pilot draws no inference from it.

## 5. Gate application (frozen §4.5, applied exactly)

- **Proceed gate** — exact agreement ≥ 0.85 **and** κ ≥ 0.75:
  agreement 0.84 < 0.85 → **NOT MET** (the κ arm is met: 0.7885 ≥
  0.75). The agreement shortfall is one object: 85 agreements would
  have met the arm.
- **Stop rule** — exact agreement < 0.70 **or** κ < 0.50: **NOT
  FIRED** (0.84 and 0.7885 are both well clear).

**Verdict: MIDDLE BAND.** Per the frozen rule, this report presents
the numbers and frames the owner's decision; it makes no
recommendation dressed as a verdict, and the motif arm is **not**
eligible for Stage 2(b) on this pilot alone.

What the owner is deciding, on this record: the measured pipeline
reproduces a primary motif code 84% of the time with κ 0.79, and its
disagreement is dominated by a single, nameable boundary — how worn
an object may be before its depiction is coded ILLEGIBLE, and whether
a faint face counts as a depiction at all. The paths the freeze
leaves open are the owner's to choose among: (a) accept this pilot as
the reliability basis and freeze a Stage 2(b) design that carries a
pre-registered rule for the legibility boundary (a design decision,
not a finding of this pilot); (b) commission a codebook clarification
of the ILLEGIBLE / SCRIPT_ONLY / GEOMETRIC boundary and a re-pilot
before any Stage 2(b) freeze; (c) let the motif arm rest here, with
the Stage 0 inventory and this pilot as its final record. Each path
is a fresh owner decision; none is taken by this report.

Separately framed for the same decision: **publication of the Stage 1
dataset** (codes, notes, disagreement log — no images) beyond this
repository, e.g. as a Zenodo release, is **not pre-authorized** for
Stage 1 and is the owner's call alongside the gate outcome.

## 6. Descriptive concordance (freeze §6 — concordance, never accuracy)

Of the 100 sampled objects, 31 carry a unicorn-family `motif_chapter`
value in the catalogue. Their adjudicated codes: UNICORN 22, other 9.
The catalogue chapter is a finding aid assigned for plate
organization; this count describes how the fresh blinded coding
relates to it and is not an accuracy measurement in either direction.
NONMAPPABLE chapter families (`tigerwithzebu`, page headers) were
excluded by the frozen rule; none occurred in the frame. No comparison
against Holdat's `iconography` field was made — the object-level join
does not exist (Phase-133).

## 7. Effort (record-file timestamps; AI-agent wall times)

Per-object coding time (median, by batch) ran 9.5–12.4 s across the
nine coding batches (pass means 10.0–12.8 s; batch setup 12–22 s).
Adjudication: 16 objects, median 9.2 s per object. These are wall
times of this AI pipeline under this protocol, stated so a future
human or machine replication can budget against them; they are not
human coding times.

## 8. Fences observed

No association statistics; no accuracy claim against any external
coding; no anchor, claim, or PRED change; no Holdat comparison;
images never entered git (crops live only in the gitignored local
CISI store); the dataset carries codes and notes only.

## 9. Artifacts

- Freeze record: `specs/024-evidence-integration/stage1-freeze.md`
- Frame + draw script + tests: `data/evidence_integration/
  phase134_pilot_frame.json`, `backend/scripts/phase134_frame.py`,
  `backend/tests/test_phase134_frame.py`
- Dataset + meta: `data/evidence_integration/
  phase134_pilot_dataset.json`, `..._meta.json`
- Metrics + script + tests: `reports/phase134_pilot_metrics.json`,
  `backend/scripts/phase134_metrics.py`,
  `backend/tests/test_phase134_metrics.py`
- Local only (never in git): the 220 crops, coder packets, and raw
  per-object records under the gitignored CISI image store
  (`corpora/downloads/cisi_image_layer/phase134_pilot/`).
