# Spec 029 — Gap Assessment: Current Claim Handling vs. the Tao Standard

> Assessment date: 2026-10-12. Assessor: program (AI agent,
> Muse Spark, at the direction of Tristen Pierson).
> Codebase state: `origin/main` at `5c1f7d5e`. Method: direct
> read of the claim machinery — `backend/glossa_lab/aee_core.py`,
> `backend/glossa_lab/api/indus_evidence.py`, the extracted-claims
> record shape, `backend/reports/INDUS_FINAL_ANCHORS.json`, and
> the frontend surfaces that render claims, scores, and anchors.
> Every finding below carries file evidence. This assessment is
> the input record for `spec.md`; it is not itself a governed
> artifact and it changes no claim, score, anchor, or verdict.

## The standard (owner directive, 2026-10-12)

A claim is settled by five stages — **created, checked,
explained, accepted, digested** — of which scoring is only the
checking stage. Headline claims decompose into sub-claims, each
scored on its own evidence with its own falsifier. Digestion
(explanation by named humans) is first-class tracked work.
Attribution is itself a claim; contested attribution stays
visible and caps the parent. Easily graded metrics never stand
in for understanding; no score or volume rankings; every
verdict states what remains not understood. Machine-speed
verification (lane 1) and human-paced acceptance (lane 2) are
tracked separately and never displayed as each other.
Registration protects priority so openness is rewarded. Every
verdict ships an inspectable evidence trail.

## Findings by point

### P1 — Five stages: ABSENT

There is no lifecycle anywhere in the claim machinery. A claim
carries exactly one flat status:

- `backend/glossa_lab/aee_core.py` (`_STATUS_MAP`, and the
  module docstring): Glossa `claim_status` values
  (`supported`, `partially_supported`, `contradicted`,
  `untested`, …) map onto AEE `ClaimStatus`; `untested` maps to
  `DRAFT` because "AEE has no UNTESTED status". The vocabulary
  mixes checking outcomes (`contradicted`) with acceptance
  language (`supported`) in a single field.
- The extracted-claims record shape (sample:
  `glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`)
  has keys `claim_id, claim_status, claim_type,
  confidence_in_source, extracted_at, normalized_claim,
  quote_fragment, source_document_id, testability` (fuller
  records add `falsification_condition`,
  `glossa_lab_evidence`, `contradicting_evidence`,
  `signs_involved`). No stage field, no stage history, no
  actor or timestamp for any status change.
- The claims API (`backend/glossa_lab/api/indus_evidence.py:157`
  `GET /claims`, `:215` `GET /claims/aee-scores`) returns the
  raw records plus an optional `aee_score`. Nothing in the API
  can express "checked but not yet explained".

**Gap:** created → checked → explained → accepted → digested
does not exist as data, as transitions, or as display.

### P2 — Decomposition: ABSENT for decipherment claims

The program's headline objects — the 287 anchor readings — are
not claims in the claims system at all. An anchor record in
`backend/reports/INDUS_FINAL_ANCHORS.json` carries exactly
`{reading, confidence, basis, reading_direction}`, where
`basis` is a single line (sample: "Terminal marker, Dravidian
case suffix") and `confidence` is a bare tier
(HIGH/MEDIUM/LOW/CANDIDATE). There is no per-anchor falsifier,
no separate scoring of (a) the reading's soundness, (b) prior
scholarship accounted for, (c) attribution, (d) intelligibility
of the explanation. The extracted-claims system decomposes
*literature* claims, not the program's own decipherment
claims; the two systems do not meet.

**Gap:** a decipherment claim is one opaque tier label where
the standard requires a bundle of independently scored
sub-claims.

### P3 — Digestion: ABSENT

No explanation artifact, no named-human account, and no
digestion state exist for any claim or anchor. A repository
search for explanation/digestion records in the claim
surfaces returns nothing (the only "not understood" hit in
`backend/` is an unrelated data description in
`backend/glossa_lab/data/meroitic.py:77`). Statuses are
assigned at extraction time by the extraction process; no
surface can distinguish "verified by machine checks" from
"explained by a human others can challenge".

**Gap:** the two stages that, under the standard, actually
settle a claim (explained, digested) are unrepresented;
verified-but-unexplained is not even a flaggable state.

### P4 — Attribution as a claim: ABSENT

`aee_core.py` preserves an `author` field in `Claim.metadata`
when the source record happens to carry one, and claims carry
`source_document_id`. That is the whole of it: no attribution
sub-claim, no prior-scholarship completeness record, no
contested-attribution flag, and no cap mechanism. (Phase-131's
"attribution" is a different sense — apportioning cross-
compilation *disagreement* — not scholarly priority or
completeness.) A reading whose priority or completeness is
disputed renders identically to one that is not.

**Gap:** attribution is metadata-at-best, never a governed
claim with evidence, a contest state, and a parent cap.

### P5 — Anti-gradability: VIOLATED on a headline surface

- `frontend/src/components/DeciphermentPanel.tsx:554`
  renders "**{totalAnchors} signs deciphered**" as a headline
  — a volume count presented as a decipherment achievement,
  over a corpus where the program's own standing position is
  that the script is **not deciphered**.
- The same panel's framing (lines 5–7, 324–335, 590) leads
  with "current confidence level + weighted %" and
  HIGH/MEDIUM/LOW anchor counts as the primary summary.
- `aee_core.assessment_summary` computes a
  `mean_propagated_score` over all claims — a single
  program-level average of checking-stage numbers, exposed
  by `GET /claims/aee-scores`.
- The AEE `ClaimScore` (`aee/scoring.py:39–64`) derives a
  `band` (a ConfidenceBand) directly from
  `propagated_score`; band language reads as confidence in
  the claim, i.e. acceptance-flavoured output of a
  checking-stage computation.
- No verdict or claim display anywhere carries a "what
  remains not understood" statement (search: zero hits on
  the claim/report/frontend surfaces).

**Gap:** scores, bands, means, and counts currently *are* the
headline. The standard forbids exactly this.

### P6 — Two lanes: ABSENT (single lane, mislabelled)

Extraction-assigned statuses (`supported`, …) are rendered by
`frontend/src/components/IndusEvidenceView.tsx` as coloured
badges (status colour map at line 44, `strongly_supported` =
green `#16a34a`; badge render at lines 402–416) next to the
claim text. These statuses originate in lane 1 (machine
extraction and AEE scoring) but are displayed with the
visual language of settled scholarly standing, with no lane
separation in the API response or the UI. The expanded view
(line 424+) does show the falsification condition and
Glossa-Lab evidence — good lane-1 material — under no lane
label at all.

**Gap:** lane-1 outputs wear lane-2 clothing. Nothing in the
data model prevents it.

### P7 — Priority/credit for external scholars: ABSENT

The program registers its *own* predictions
(`docs/PREDICTION_REGISTER.md`) and ingests literature by PDF
intake, but there is no registration instrument by which an
external scholar's early reading is timestamped and credited
independent of the program's assessment of it. A scholar who
published a reading early has no priority record in this
system; openness is not structurally rewarded.

**Gap:** no priority/credit register exists.

### P8 — Inspectable evidence trails: PARTIAL

Strengths: extracted claims carry `falsification_condition`,
`glossa_lab_evidence`, and `contradicting_evidence`, and the
UI's expanded view displays the first two; AEE scores expose
their components (evidence, independence, falsifiability,
boundary, contradiction penalty — `aee/scoring.py:54–64`);
spec-level verdicts since Spec 026 ship with frozen designs,
controls, and outcome records.

Gaps at the claim level: a per-claim API record does not
serialize a complete trail (evidence refs with origin groups,
falsifier state, who/what assigned the status, when); anchor
records carry no trail at all beyond the one-line `basis`;
and no display pairs a verdict with what remains not
understood (see P5).

## Summary table

| Point | State | Headline evidence |
|---|---|---|
| P1 five stages | Absent | one flat `claim_status`; no stage fields anywhere |
| P2 decomposition | Absent | anchor = `{reading, confidence, basis, reading_direction}` |
| P3 digestion | Absent | no explanation artifact or named-human record exists |
| P4 attribution claim | Absent | `author` is optional metadata; no contest state or cap |
| P5 anti-gradability | **Violated** | "287 signs deciphered" headline; mean score; score-derived bands |
| P6 two lanes | Absent | lane-1 statuses rendered as settled-standing badges |
| P7 priority/credit | Absent | no external-scholar registration instrument |
| P8 evidence trails | Partial | falsifier + evidence strings carried; no complete per-claim trail; no "not understood" |

## What this assessment does not do

It re-stages nothing, re-scores nothing, and re-words no
existing display. Whether existing claims and anchors are
re-staged immediately or at next touch is an open owner
decision recorded in `spec.md` (OD-1). The DeciphermentPanel
headline is flagged as a current violation of the adopted
standard; changing it is implementation work under a future
frozen plan, not part of this claims-first draft.
