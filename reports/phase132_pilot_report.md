# Phase-132 — Stage P Pilot Report (Spec 023, Keyed Transcription Layer)

**Spec:** 023 — Keyed Transcription Layer over CISI Vols. 1–2,
**FROZEN 2026-10-09** (owner: Tristen Pierson — "merge #99
and execute the new plan"). **Freeze + merge:** PR #99.
**Build:** PR #100 (merged at main `c789f7ad`). **Date of
this report:** 2026-10-09. **Dataset scope:** Stage P pilot —
50 frame objects, 10-object gold sample (seed 20261009).

**AI disclosure:** all roles in this pilot — pass_a, pass_b,
pass_gold, and adjudicator — were executed by AI agents
(Muse Spark, via Muse) in role-isolated blinded
instances, at the direction of Tristen Pierson, per
constitution §VI and the spec §5.6 freeze block. This report
was likewise prepared by an AI agent under the same
direction.

Every quantity in this report is computed from the on-disk
records — the local-store pass / adjudication records and
`reports/phase132_pilot_metrics.json` (produced by
`backend/scripts/phase132_metrics.py`) — never from pass
batch self-reports (see §4(d), the process finding).

## 1. VERDICT — the frozen pilot stop-rule FIRED; the build stops

> **The frozen pilot STOP-RULE FIRED.** Exact-sequence
> inter-pass agreement over all 50 objects (P space) is
> **0.20 (10/50)**, below the frozen **0.80** floor
> (spec §3.1 / §5.6 freeze block). The error arm of the
> stop-rule did **not** fire: the gold per-sign error
> estimator is **0.05 (2/40)**, and the frozen error
> condition is strictly greater than 0.05.
>
> Per spec §3.1 the build **STOPS**: **no tranche is
> proposed.** Stage T is not recommended, scoped, or
> scheduled by this report.
>
> **Release gates (gold scope) ALL FAIL** — (i)
> exact-sequence **0.10 < 0.90**, (ii) per-token
> **0.4286 < 0.95**, (iii) gold error estimator
> **0.05 > 0.02** — so **NO dataset publication occurs**.
> The owner-approved CC BY 4.0 publication route
> (Decision Ask 4) is **not exercised**. The dataset JSON
> in `data/keyed_transcription/` is the in-repo build
> record only.
>
> **A stopped pilot is a result (spec §3.1).** The pilot
> did the jobs §3.1 assigned it: it measured per-object
> effort, measured agreement and error against the frozen
> gates, and exercised the full pipeline end to end. The
> measurements below are reported as found.

| Frozen check | Measured | Threshold | Outcome |
|---|---|---|---|
| Stop-rule: exact-seq agreement, all-50, P | 0.20 (10/50) | < 0.80 fires | **FIRES** |
| Stop-rule: gold error estimator, P | 0.05 (2/40) | > 0.05 fires | does not fire |
| Release gate (i): exact-seq, gold, P | 0.10 (1/10) | ≥ 0.90 | **FAIL** |
| Release gate (ii): per-token, gold, P | 0.4286 (18/42) | ≥ 0.95 | **FAIL** |
| Release gate (iii): gold estimator, P | 0.05 (2/40) | ≤ 0.02 | **FAIL** |

## 2. Frame as drawn

Deterministic draw per spec §3.1 (rule and seed 20261009
recorded in `data/keyed_transcription/phase132_pilot_frame.json`):

| Dimension | As drawn |
|---|---|
| Objects | 50 |
| Sites | Mohenjo-Daro 25 / Harappa 15 / Lothal 6 / Kalibangan 4 |
| Object types (as printed; counted from the frame records) | Seals 34 / Tablets 11 / unrecorded 5 |
| mayig-overlap objects | 10 — all Mohenjo-Daro |
| Gold sample | 10 objects (seed 20261009) |
| Ambiguity log (§4.3) | **EMPTY** — no exclusions |

**Quota-correction record.** The mayig layer resolved
against the catalogue as 176 Mohenjo-Daro / 3
site-uncaptured / 0 elsewhere, so the original Harappa and
Lothal+Kalibangan mayig sub-quotas were unfillable. The
sub-quotas were corrected **pre-transcription** to MD 10 /
H 0 / LK 0 (commit `33cb4c86`), and the frame was drawn
under the corrected quotas.

**Key disagreements.** 10 key disagreements were logged
across the frame and ruled at adjudication from the
plates; the plate reading governs (§4.1). None produced
an ambiguity-log entry and no object was excluded.

## 3. Protocol as executed

- Two independent passes (Pass A, Pass B) per object, plus
  a third independent gold pass on the 10 gold objects,
  followed by adjudication of all inter-pass disagreements
  under §5.5. Orientation was declared before
  transcription (§5.1), impression-primary per the freeze.
- Comparison space, alignment, and the gold estimator are
  exactly the §5.6 freeze-block definitions, implemented
  in `backend/scripts/phase132_metrics.py`: P space is the
  crosswalk-v1 primary counterpart of each matched M
  (highest-confidence row, tie → lowest P number);
  crosswalk-unmapped tokens compare as `UNMAPPED:<M_ID>`;
  `UNK` compares as `UNK`; per-token agreement uses
  minimum-edit alignment with substitution preferred over
  insertion/deletion at equal cost.

## 4. Deviations and findings, named plainly

**(a) Transcribers.** The transcribers were AI agents in
role-isolated blinded instances; each pass was split
across 5 batch instances (roles pass_a / pass_b /
pass_gold / adjudicator per the §5.6 freeze block).
Blindness held: no pass saw another pass, an adjudicated
record, or any existing transcription of a frame object.

**(b) Pass B source renders.** Pass B batch 2 used the
200-DPI page renders (`page_cache_200`) for several
Vol. 2 objects after page-render access failures, and a
self-made tighter re-crop for M-195. All sources remained
plate-only throughout; no external transcription was
consulted at any point.

**(c) Two-sided-tablet B-face ordering.** B-face ordering
on two-sided tablets was flagged by the passes and ruled
at adjudication. Disagreement taxonomy over all 50
adjudication records (computed from the on-disk records):

| Type | Count |
|---|---|
| identity | 93 |
| legibility | 45 |
| count | 11 |
| key | 10 |
| orientation | 2 |
| order | 1 |
| **Total** | **162** |

Only **5 of 50** objects had zero disagreements.

**(d) PROCESS FINDING — self-reports are not data.**
Several pass batch self-reports' token tallies disagreed
with the on-disk records those same batches wrote. Every
quantity in this report is therefore computed from the
on-disk records, never from self-reports. Any future stage
must treat batch self-reports as unverified narrative
until reconciled against the records.

**(e) Empty final sequences.** 6 objects have empty final
(adjudicated) sequences, as found in the dataset:
`cisi:v1:M-566`, `cisi:v2:M-1542`, `cisi:v2:H-886`,
`cisi:v2:Pk-24`, `cisi:v1:K-21`, `cisi:v1:K-88` — heavily
corroded tablets, faces with no discernible glyph slot,
and objects whose inscription field is broken away or was
not among the supplied crops. An empty sequence here is a
record of what the plates show, not a dropped object: all
6 remain in the dataset and in every denominator above.

## 5. Measured quantities

From `reports/phase132_pilot_metrics.json` (P and M space
agree throughout this pilot; both are printed).

### Agreement

| Quantity | Scope | P | M |
|---|---|---|---|
| Exact-sequence agreement | all 50 | 0.20 (10/50) | 0.20 (10/50) |
| Exact-sequence agreement | gold 10 | 0.10 (1/10) | 0.10 (1/10) |
| Per-token agreement | all 50 | 0.4798 (95/198) | 0.4798 (95/198) |
| Per-token agreement | gold 10 | 0.4286 (18/42) | 0.4286 (18/42) |

### Gold error estimator

**0.05 (2 differing positions / 40)** in both P and M
space. Frozen limitation, stated with the estimate:
errors identical across all three passes are invisible to
this estimator.

### Tokens

| Stream | Tokens |
|---|---|
| Pass A | 191 |
| Pass B | 190 |
| Gold pass (10 objects) | 40 |
| Adjudicated final | 189 |

Adjudicated tokens per object: mean **3.78**, median
**4** (mayig-layer reference ≈ 5.6 tokens per inscription).

### UNK, crosswalk-unmapped, conflicts (adjudicated final unless noted)

| Quantity | Value |
|---|---|
| UNK share — Pass A | 39.3% (75/191) |
| UNK share — Pass B | 38.9% (74/190) |
| UNK share — gold pass | 42.5% (17/40) |
| UNK share — adjudicated | 40.7% (77/189) |
| Crosswalk-unmapped share — adjudicated | 8.5% (16/189) |
| UNK + unmapped share — adjudicated | **49.2% (93/189)** |
| Crosswalk-conflict tokens — adjudicated | 69 |

The adjudicated UNK + unmapped share of **49.2%** exceeds
spec §7's 25% NOT-EVALUABLE unmapped-share boundary
(spec 018 §6.1) **as a property of this layer**: had this
layer been put to the spec-018 harness, that share alone
would place it on the NOT EVALUABLE side of the boundary.
This is reported as a measured property; no evaluation
was run (see §7 below).

### Attestation checks (spec §7, adjudicated final P sequences)

| Sign | Attested | Tokens |
|---|---|---|
| P125 | yes | 1 |
| P076 | **not attested** | 0 |
| P000 | **not attested** | 0 |

Recorded as found; the build did not select for these
signs (§7).

### Intake, license gate, dedup (spec §6 / Phase-130 path)

- Intake validator: **pass-with-warnings** — 0 errors,
  21 warnings: `TOKEN_FORMAT_MISMATCH` ×10 (the
  `UNMAPPED:<M_ID>` values, by design not P-format),
  `EMPTY_TOKEN_SEQUENCE` ×6 (the §4(e) objects),
  `RECOMMENDED_FIELD_MISSING` ×5 (`object_type` not
  printed for those objects; never back-filled, §4.2).
- License gate: pass (on the declared transcription-facts
  basis). The gate passing does **not** release the
  dataset: the §5.6 release gates failed (§1), and no
  publication occurs.
- Spec-018 dedup: 50 → **39 kept** (stage A −8, stage B
  −3, stage C −0).

## 6. Effort — the pilot's explicit product (spec §3.1(iv))

Measured from the local store's effort log (320 events):

| Role | n objects | Median s/object | Mean s/object | Total s |
|---|---|---|---|---|
| Pass A | 50 | 51.5 | 66.68 | 3,334 |
| Pass B | 50 | 70 | 76.36 | 3,818 |
| Gold pass | 10 | 110 | 97.9 | 979 |
| Adjudication | 50 | 30.5 | 38.9 | 1,945 |
| **All roles** | — | — | — | **10,076** |

All-in: **10,076 s ≈ 201.5 s per object**; **53.3 s per
final (adjudicated) token**. These are the measured unit
quantities the Stage-T decision (§7) would use. They are
AI-agent wall times under this pipeline, stated as such —
not estimates of expert human effort.

## 7. Stage T readiness — facts only

The stop-rule outcome means **this report makes NO Stage T
recommendation**.

Facts of record for the owner's separate Stage T decision
(spec §11 Decision Ask 2, revisited as task T9):

- The measured unit quantities of §5–§6 — agreement,
  error estimator, UNK/unmapped shares, per-object and
  per-token effort — are the inputs that decision would
  use, and they are now in hand.
- Spec §10(b) — commissioned external transcription — is
  the alternative the spec names when pilot error /
  agreement fails its gates. That question is now askable
  with pilot numbers in hand.

This report advocates neither way.

**Evaluability, stated exactly.** By class, this layer
QUALIFIES for PRED-2026-001 / 002 / 003 (4 distinct sites;
spec 018 matrix, dataset class `image_transcription`) —
**class qualification only**. The §5.6 quality gates
failed, the §7 unmapped-share boundary is exceeded
(§5 above), and **no evaluation was run or is implied**.

## 8. Interpretation discipline (spec §8, restated)

This pilot measured **this pipeline** — AI transcribers,
these plate renders, the Mahadevan-1977 sign drawings as
the identification reference — failing the frozen
agreement gates. It does **not** measure expert human
transcription. It does not bear on any anchor reading:
transcription agreement is agreement about which sign is
present, not about what it says. It changes **no PRED
verdict**; Phase-125's FAIL — DISAGREEMENT and spec 020's
NO stand untouched.

**Anchors assertion.** `backend/reports/INDUS_FINAL_ANCHORS.json`
sha256, computed for this report:
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
— **unchanged**, identical to the frozen value of record
(spec 023 Appendix B).

## 9. Artifact inventory

Repository:

- Frame: `data/keyed_transcription/phase132_pilot_frame.json`
- Dataset (build record only — NOT published, §1):
  `data/keyed_transcription/phase132_pilot_dataset_v1.json`
  + meta `phase132_pilot_dataset_v1_meta.json`; dataset
  content hash
  `7bdc73f5e0f6a959f8d94a4317c642ebe36638e841f7bb80bae97c75477f224a`
- Metrics: `reports/phase132_pilot_metrics.json`
- This report: `reports/phase132_pilot_report.md`
- Scripts: `backend/scripts/phase132_frame.py`,
  `phase132_metrics.py`, `phase132_build_dataset.py`,
  `phase132_comprehensive_validation.py`
- Tests: `backend/tests/test_phase132_frame.py`,
  `test_phase132_metrics.py`, `test_phase132_pilot_report.py`

Local store (gitignored; counts only, Phase-124 pattern) —
`corpora/downloads/cisi_image_layer/phase132_pilot/`:

- 50 object directories
- 50 Pass A records, 50 Pass B records, 10 gold-pass records
- 50 adjudication records
- Effort log: 320 events
- No plate image, render, or crop is in the repository or
  in this report, at any stage (spec §12 storage
  discipline).
