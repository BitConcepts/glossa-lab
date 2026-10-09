# Program note, Spec 023 and Phase-132 (program closeout): the keyed transcription layer stopped at its pilot stop-rule, and the program moves to watch-and-respond

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Program note, 2026-10-09. Prepared as an addendum to the program's
preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; previous published version v4.4.0, DOI
10.5281/zenodo.23261517, record 23261517). Program provenance
registry: OSF [osf.io/ybd65](https://osf.io/ybd65/). Code, frozen
specs, and machine-readable results: BitConcepts/glossa-lab
(Spec 023; Phase-132; repository main at commit
a6577d7f23571d799cbf4da7525ff4d863c1283c, merge of PR #101; the
release-source commit for this note is recorded in
`RELEASE_VALIDATION.json`).

This note reports Spec 023 and Phase-132 exactly as they stand in
the merged report (`reports/phase132_pilot_report.md`), negatives
included, and then records the program closeout. Neither the spec
nor the phase changed any decipherment anchor: the anchors file
`backend/reports/INDUS_FINAL_ANCHORS.json` is byte-identical
throughout (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed).
The Phase-125 verdict — **FAIL — DISAGREEMENT** — is final and
unchanged; spec 020's adjudication outcome — **NO** — stands
untouched. **PRED-2026-001, PRED-2026-002, and PRED-2026-003
remain PENDING.** Nothing in this note is evidence that any
particular reading of any Indus sign is right or wrong.

## Abstract

Spec 023 proposed the one remaining self-powered route to a
legitimately keyed corpus layer: transcribe CISI Vols. 1–2
inscriptions directly from the published plates, keyed to true
printed CISI object IDs, under a double-pass blinded protocol
with pre-registered quality gates and a pilot stop-rule.
Phase-132 executed the Stage P pilot exactly as frozen — and
**the frozen pilot stop-rule FIRED**: exact-sequence inter-pass
agreement over all 50 pilot objects was **0.20 (10/50)** against
the frozen 0.80 floor. All three release gates failed on the gold
sample, so the pilot dataset was **not published**. Per the
spec, the build stops and no tranche (Stage T) is proposed,
scoped, or scheduled. With this result, the program's internal
lines are closed: the within-compilation validation batteries
(closed by owner decision, 2026-10-07), the cross-compilation
positional attribution (closed; its key mechanisms are not
estimable for lack of a legitimate join), and now the keyed
transcription-layer build (stopped at pilot). The program's
posture is **watch-and-respond**: the registered predictions
await a genuinely independent corpus, and the intake machinery
for one (Phase-130) is built and ready.

## 1. Spec 023 — frozen with owner adjudication

Spec 023 (keyed transcription layer over CISI Vols. 1–2) was
drafted as a proposal, then **frozen on 2026-10-09 with the
owner's adjudication recorded** (owner: Tristen Pierson —
"merge #99 and execute the new plan"; freeze + merge: PR #99).
The five decision asks were answered with the proposed values as
drafted: pilot go; tranche scope approved in principle only
(Stage T requiring a separate post-pilot go); the §5.6 quality
gates as proposed; CC BY 4.0 publication of gate-passing stage
datasets approved in principle; impression-primary orientation.
The spec's canonical key is volume-scoped
(`cisi:v{volume}:{printed_id}`); the Holdat `cisi_number` field
is expressly prohibited as a join key.

## 2. Phase-132 — Stage P pilot, executed as specified

Deterministic frame draw (rule and seed 20261009 recorded in
`data/keyed_transcription/phase132_pilot_frame.json`): **50
objects — Mohenjo-Daro 25 / Harappa 15 / Lothal 6 / Kalibangan
4; seals 34 / tablets 11 / type-unrecorded 5; 10-object gold
sample; ambiguity log EMPTY, no exclusions.** The mayig-overlap
sub-quotas were corrected **pre-transcription** (the mayig layer
resolved against the catalogue as 176 Mohenjo-Daro / 3
site-uncaptured / 0 elsewhere, so the original Harappa and
Lothal+Kalibangan sub-quotas were unfillable), and **all 10
mayig-overlap objects in the frame are Mohenjo-Daro**. Ten key
disagreements were logged across the frame and ruled at
adjudication from the plates; none produced an ambiguity-log
entry and no object was excluded.

Protocol as frozen: orientation declared before transcription
(impression-primary); two independent passes (Pass A, Pass B)
per object, plus a third independent gold pass on the 10 gold
objects, followed by adjudication of all inter-pass
disagreements; comparison in P space (crosswalk-v1 primary
counterparts) and M space, which agree throughout this pilot.

**AI disclosure.** All roles in this pilot — pass_a, pass_b,
pass_gold, and adjudicator — were executed by AI agents (Muse
Spark, via Muse) in role-isolated blinded instances, at the
direction of Tristen Pierson, per constitution §VI and the spec
§5.6 freeze block. Blindness held: no pass saw another pass, an
adjudicated record, or any existing transcription of a frame
object. Every quantity below is computed from the on-disk
records, never from pass batch self-reports (see the process
finding, §4).

## 3. Verdict — the frozen pilot stop-rule FIRED

| Frozen check | Measured | Threshold | Outcome |
|---|---|---|---|
| Stop-rule: exact-seq agreement, all-50, P | 0.20 (10/50) | < 0.80 fires | **FIRES** |
| Stop-rule: gold error estimator, P | 0.05 (2/40) | > 0.05 fires | does not fire |
| Release gate (i): exact-seq, gold, P | 0.10 (1/10) | ≥ 0.90 | **FAIL** |
| Release gate (ii): per-token, gold, P | 0.4286 (18/42) | ≥ 0.95 | **FAIL** |
| Release gate (iii): gold estimator, P | 0.05 (2/40) | ≤ 0.02 | **FAIL** |

The error arm of the stop-rule did **not** fire: the gold
per-sign error estimator is **0.05 (2 differing positions /
40)**, and the frozen error condition is strictly greater than
0.05. The agreement arm fired, and one arm is sufficient.

**Release gates (gold scope) ALL FAIL** — so **no dataset
publication occurs**. The owner-approved CC BY 4.0 publication
route (Decision Ask 4) is **not exercised**. The dataset JSON in
`data/keyed_transcription/` is the in-repo build record only.

Per spec §3.1 the build **STOPS**: **no tranche is proposed.**
Stage T is not recommended, scoped, or scheduled. A stopped
pilot is a result (spec §3.1): the pilot measured per-object
effort, measured agreement and error against the frozen gates,
and exercised the full pipeline end to end.

## 4. Measured quantities, as found

**Agreement.** Exact-sequence agreement, all 50: **0.20
(10/50)** in both P and M space; gold 10: 0.10 (1/10).
**Per-token agreement, all 50: 0.4798 (95/198)**; gold 10:
0.4286 (18/42).

**Disagreement taxonomy** over all 50 adjudication records
(computed from the on-disk records): **162 total — identity 93,
legibility 45, count 11, key 10, orientation 2, order 1.** Only
5 of 50 objects had zero disagreements.

**Tokens.** Pass A 191; Pass B 190; gold pass (10 objects) 40;
adjudicated final 189 (mean 3.78, median 4 per object; the
mayig-layer reference is ≈ 5.6 tokens per inscription).

**Unknown and unmapped share.** Adjudicated UNK share 40.7%
(77/189); crosswalk-unmapped share 8.5% (16/189); **UNK +
unmapped share 49.2% (93/189)**. That share exceeds spec §7's
25% NOT-EVALUABLE unmapped-share boundary (spec 018 §6.1) **as
a property of this layer**: had this layer been put to the
spec-018 harness, that share alone would place it on the NOT
EVALUABLE side of the boundary. This is reported as a measured
property; no evaluation was run.

**Empty final sequences.** 6 objects have empty final
(adjudicated) sequences — `cisi:v1:M-566`, `cisi:v2:M-1542`,
`cisi:v2:H-886`, `cisi:v2:Pk-24`, `cisi:v1:K-21`,
`cisi:v1:K-88` (heavily corroded tablets, faces with no
discernible glyph slot, inscription fields broken away or not
among the supplied crops). All 6 are retained in the dataset
and in every denominator above.

**Attestation checks.** P125 attested (1 token); P076 **not
attested**; P000 **not attested**. Recorded as found; the build
did not select for these signs.

**Intake path.** Intake validator: pass-with-warnings (0
errors, 21 warnings). License gate: pass on the declared
transcription-facts basis — the gate passing does **not**
release the dataset, because the §5.6 release gates failed.
Spec-018 dedup on the pilot frame: 50 → 39 kept.

**Deviation, named.** Pass B batch 2 used the 200-DPI page
renders (`page_cache_200`) for several Vol. 2 objects after
page-render access failures, and a self-made tighter re-crop
for M-195. All sources remained plate-only throughout; no
external transcription was consulted at any point.

**Process finding — self-reports are not data.** Several pass
batch self-reports' token tallies disagreed with the on-disk
records those same batches wrote. Every quantity in the pilot
report is therefore computed from the on-disk records, never
from self-reports. Any future stage must treat batch
self-reports as unverified narrative until reconciled against
the records.

**Effort — the pilot's explicit product.** Measured from the
local store's effort log (320 events): Pass A median 51.5
s/object (mean 66.68; total 3,334 s); Pass B median 70 (mean
76.36; total 3,818 s); gold pass median 110 (mean 97.9; total
979 s); adjudication median 30.5 (mean 38.9; total 1,945 s).
**All-in: 10,076 s ≈ 201.5 s per object; 53.3 s per final
(adjudicated) token.** These are AI-agent wall times under this
pipeline, stated as such — not estimates of expert human
effort.

## 5. Program closeout statement

With the Phase-132 result, the program's internal lines are
closed, and its posture is now **watch-and-respond**:

- **Within-compilation validation batteries — CLOSED**
  (owner decision, 2026-10-07). Specs 011/014/016/017
  (Phases 113/115/117/118) were all rejected at their own
  calibration gates; no anchor ever received a
  within-compilation validation; no further battery redesign
  is authorized.
- **Cross-compilation positional attribution — CLOSED.**
  The Phase-125 verdict (FAIL — DISAGREEMENT) stands;
  Phase-127 showed the disagreement is not a sampling
  artifact (matched-size null median TV 0.082613 vs observed
  0.636931; 0 of 999 replicates); Phase-131 attributed only a
  composition share of 0.061321, leaving a residual unexplained
  share of 0.938679, with the segmentation, substitution, and
  insertion-deletion shares NOT ESTIMABLE because the
  legitimate matched-object join does not exist (4 matched
  pairs, 0 exact). Reopening requires a legitimately keyed
  corpus layer, which is external-data-dependent.
- **Keyed transcription-layer build — STOPPED AT PILOT**
  (Spec 023 / Phase-132, this note). The frozen stop-rule
  fired on measured agreement. No Stage T is proposed, scoped,
  or scheduled. A retry would require a new owner decision
  **and** a materially different transcription basis (for
  example, human expert transcription) — not a parameter
  change to the stopped design.

**Standing state.** PRED-2026-001, PRED-2026-002, and
PRED-2026-003 remain **PENDING**, awaiting a qualifying
independent corpus under the frozen spec-018 evaluability
matrix. The 44 anchors flagged `pending_non_sa_validation`
remain in that state; the strict SA-free core (94 readings,
73.68% corpus coverage) stands as a hypothesis, not a validated
decipherment. The Phase-130 intake pack (schema, license-gated
validator, shared dedup module, runbook) is built, so any
qualifying dataset that appears can be ingested and classified
without further construction.

**Watch-and-respond.** The program now responds to external
triggers only: replies to the 2026-10-08 data-request letters
(RMRL concordance and graffiti corpora; Mitra/Dixit
image-derived transcriptions; Tiedekirja digital CISI enquiry);
hits from the weekly independent-data watch (Mahadevan Chair
concordance, CISID, CISI Vol. 3.4, newly released site corpora,
any complete digital CISI volume appearing anywhere); and the
GitHub garbage-collection closeout for the 2026-10-08 history
purge. Any data trigger follows the Phase-130 intake path —
provenance, license gate, dedup, spec-018 evaluability
classification — and is reported to the owner **before** any
study is designed. No study, battery, or PRED scoring will run
without fresh owner authorization.

**AI disclosure for this note.** This note was prepared by an
AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, from the merged Phase-132 report and the
program ledgers; every quantity in it is taken from those
on-disk records.
