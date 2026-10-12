# Spec 029 — Tao Claim Lifecycle: Staging, Decomposition, Digestion, and Lane Discipline for Indus Claims

> ## DRAFT — CLAIMS-FIRST, NOT FROZEN — 2026-10-12
>
> Owner directive (Tristen Pierson, 2026-10-12): realign
> Glossa-Lab's claim handling on Terence Tao's points (five
> stages; decomposition; digestion as first-class work;
> attribution as a claim; anti-gradability; two lanes;
> provenance protecting openness; inspectable evidence
> trails). This spec is drafted CLAIMS-FIRST under the house
> flow: governed claims and a gap assessment precede any
> plan. **No `plan.md` and no `tasks.md` exist for this spec,
> and none are authorised.** Nothing in this spec is frozen;
> every governed claim is `draft` pending owner
> adjudication, and §8 lists the decisions that are the
> owner's alone. The gap assessment is `assessment.md` in
> this directory; the structured claim register is
> `claims.json`.

## 1. Why this spec exists

The program adopted the Tao standard on 2026-10-12: a claim
is settled by five stages — created, checked, explained,
accepted, digested — and a score is only the checking stage.
The assessment in `assessment.md` measured the current claim
machinery against that standard and found it largely absent
and, on one headline surface, in direct violation:

- There is **no lifecycle**: a claim carries one flat
  `claim_status` whose vocabulary mixes checking outcomes
  with acceptance language (`backend/glossa_lab/aee_core.py`,
  `_STATUS_MAP`). A score, a verdict, and scholarly
  acceptance are nowhere distinguished as data.
- The program's headline objects — **the 287 anchor
  readings — are not claims in the claims system at all**:
  an anchor record is `{reading, confidence, basis,
  reading_direction}` with a one-line basis and a bare tier
  (`backend/reports/INDUS_FINAL_ANCHORS.json`). No falsifier,
  no decomposition, no attribution record, no explanation.
- **Digestion does not exist**: no explanation artifact, no
  named-human account, no digestion state for any claim.
- **Attribution is optional metadata** (`author`, preserved
  when present), never a governed claim with a contest state
  and a cap.
- **Anti-gradability is violated on a headline surface**:
  `frontend/src/components/DeciphermentPanel.tsx:554`
  renders "**{totalAnchors} signs deciphered**" as a
  headline over a corpus where the program's standing
  position is that the script is not deciphered; the AEE
  wiring also computes a program-level `mean_propagated_score`
  (`aee_core.assessment_summary`), and AEE's `ClaimScore`
  derives a confidence *band* directly from the propagated
  score (`aee/scoring.py:39–64`) — checking-stage numbers
  wearing acceptance language.
- **One lane only**: extraction-assigned statuses render as
  coloured standing badges in the claims UI
  (`frontend/src/components/IndusEvidenceView.tsx:44,
  402–416`) with no separation between machine verification
  and human-paced acceptance.
- **No priority instrument** exists for external scholars'
  early readings, and **per-claim evidence trails are
  partial**: falsifiers and evidence strings are carried and
  displayed, but no claim-level record serializes evidence
  refs with origin groups, actor, and timestamp, and no
  verdict display states what remains not understood.

This spec defines the claim lifecycle, the decomposition,
the attribution and explanation machinery, the display
discipline, the priority register, and the trail
requirements that bring claim handling under the standard.
It is a *design* spec: it governs what a future
implementation plan must satisfy. Under claim F029-C10 it
itself changes no claim, anchor, verdict, score, or display.

## 2. Scope

### 2.1 In scope

- The lifecycle stage model for governed Indus claims
  (extracted literature claims and anchor-reading claims):
  stage vocabulary, transition rules, actor rules, and the
  stage history log.
- Decomposition of decipherment claims into sub-claim
  bundles, including the attribution sub-claim template.
- The explanation record (gate for `accepted`) and the
  digestion record (gate for `digested`).
- Stage-aware display rules for the API, the frontend, and
  generated reports/exports.
- A priority/credit register for external scholars'
  readings.
- Evidence-trail requirements on every verdict and stage
  transition.

### 2.2 Out of scope

- Any change to existing claim records, anchor records,
  scores, verdicts, or display strings. Retroactivity is an
  open owner decision (OD-1); the flagged DeciphermentPanel
  headline is *not* fixed by this spec (see F029-C10).
- Any change to the AEE library itself
  (`applied-epistemic-engineering`); this spec governs
  Glossa-Lab's adapter (`aee_core.py`), endpoints, data
  records, and surfaces.
- Any new scoring method, any re-scoring of the 287
  anchors, and any PRED-2026 scoring.
- The program verdict taxonomy for study arms
  (INVALID / INCONCLUSIVE / CONTRADICTED / SUPPORTED):
  unchanged. Verdicts are lane-1 objects; lifecycle stages
  are a separate axis. Conflating them is what this spec
  exists to prevent.

## 3. Governing framework

### 3.1 Lifecycle of this spec

Specify (this draft, claims-first) → owner adjudication of
the §4 claims and the §8 decisions → plan → tasks → freeze
→ execution. This draft deliberately stops after the first
step. A plan written before adjudication would smuggle the
§8 decisions into defaults; that is the failure mode the
claims-first order exists to prevent.

### 3.2 Claim register

`claims.json` in this directory is the structured register
(IDs `F029-C…`). Every governed claim carries a stable ID,
one bounded proposition, an epistemic layer (`M` throughout
this spec — these are methodological claims about the
program's own claim handling), a boundary, `depends_on`
links, alternatives considered, at least one falsification
test, a strongest rival, forbidden assumptions, and a
verdict rule in its metadata. The register is mechanically
checked for duplicate IDs, unresolved dependencies, and
dependency cycles.

### 3.3 Two vocabularies, kept apart

- **Verdict** (lane 1): what a machine-speed check concluded
  about a bounded claim — the program taxonomy
  (INVALID / INCONCLUSIVE / CONTRADICTED / SUPPORTED) or an
  AEE score/band. Verdicts answer "what did the check find?"
- **Stage** (lane 2 axis): where a claim stands in
  created → checked → explained → accepted → digested.
  Stages answer "how far has human-paced settlement
  progressed?"

A claim may hold any combination (e.g. verdict SUPPORTED,
stage checked — the normal state of a verified-but-
unexplained claim, which the standard names a flagged risk
state). Neither vocabulary may be rendered in the other's
terms.

### 3.4 The standard, restated as program law

1. Five stages; creation + checking alone never settle a
   claim.
2. Headline results decompose into sub-claims, each scored
   on its own evidence with its own falsifier.
3. Digestion is first-class tracked work; verified-but-
   unexplained is a flagged risk state.
4. Attribution is a claim; contested attribution caps the
   parent and stays visible.
5. Easily graded metrics never stand in for understanding;
   no score or volume rankings; every verdict states what
   remains not understood.
6. Two lanes, tracked separately; lane-1 never displays as
   lane-2.
7. Registration protects priority so openness is rewarded,
   not raced.
8. Every verdict ships an inspectable evidence trail.

## 4. Governed claims

`claims.json` governs; this section is the reading copy.
All claims are `draft`.

| ID | Claim (one line) | Tao point |
|---|---|---|
| F029-C01 | Every governed claim carries a lifecycle stage in {created, checked, explained, accepted, digested}, separate from score, verdict, and extraction status. | P1 |
| F029-C02 | No automated process may advance a claim beyond `checked`; later transitions require a recorded act of a named human. | P1/P6 |
| F029-C03 | A decipherment claim is a bundle (soundness, scholarship accounting, attribution, intelligibility), each sub-claim staged and falsifiable; parent stage = minimum of sub-claim stages. | P2 |
| F029-C04 | `accepted` requires a named-human explanation record (artifact URI + hash, challengeable); `digested` additionally requires a digestion record of independent scholarly engagement. | P3 |
| F029-C05 | Attribution is a registered sub-claim with required completeness evidence; while contested it displays on the parent and caps the parent's stage (default cap `checked`, OD-3). | P4 |
| F029-C06 | No surface may present a score, band, mean, or count as acceptance or decipherment; every verdict display carries a "what remains not understood" statement. | P5 |
| F029-C07 | Lane-1 and lane-2 states are separate fields rendered in separate regions with lane-specific labels; no lane-1 value renders in a lane-2 position. | P6 |
| F029-C08 | External scholars' readings can be registered at intake for timestamped priority/credit, independent of the program's assessment of the reading. | P7 |
| F029-C09 | Every verdict and stage transition carries an inspectable trail (evidence refs + origin groups, falsifier state, actor, timestamp) retrievable from the claim's API representation. | P8 |
| F029-C10 | This claims-first draft itself changes nothing: no re-staging, re-scoring, re-wording, or re-display of any existing record. | guard |

## 5. Functional requirements

Requirements are written against the governed claims; each
names its claim(s). They specify *what an implementation
must provide*, not how — the how is the future plan's,
written only after adjudication.

### 5.1 Lifecycle stage tracking (C01, C02)

- **FR-029-01 — Stage field and history.** The extracted-
  claims record shape and the anchor record shape each gain
  a lifecycle representation: current stage, and an
  append-only stage history (from-stage, to-stage, actor,
  timestamp, evidence refs). `aee_core.claim_from_glossa`
  maps the stage axis without folding it into `ClaimStatus`
  or into confidence; `assessment_summary` and the claims
  endpoints (`GET /claims`, `GET /claims/aee-scores`, and
  the anchor surfaces) serialize stage and lane-1 score as
  distinct objects.
- **FR-029-02 — Transition rules.** Legal transitions move
  one step along created → checked → explained → accepted
  → digested, or backward to any earlier stage with a
  recorded reason (demotion is a normal, publishable event,
  as in the program's existing demotion practice).
  Automated processes — extraction, scoring, the research
  loop, batch jobs — may write only `created` and `checked`
  transitions. Transitions above `checked` validate the
  presence of the records required by FR-029-04/05 and a
  named-human actor, and fail closed otherwise.
- **FR-029-03 — Risk-state flag.** A claim whose lane-1
  state includes a SUPPORTED-class verdict or a high score
  band while its stage is below `explained` is flagged
  `verified_unexplained` in API output, so the risk state
  the standard names is queryable rather than anecdotal.

### 5.2 Decomposition and the attribution sub-claim (C03, C05)

- **FR-029-04 — Bundle representation.** Anchor readings
  are represented as claim bundles: a parent record plus
  sub-claim records of kinds `reading_soundness`,
  `scholarship_accounting`, `attribution`, and
  `explanation_intelligibility`, each with its own evidence
  list, falsification condition, stage, and trail. The
  parent's stage is computed (minimum of sub-claim stages,
  then the FR-029-05 cap), never directly assigned.
- **FR-029-05 — Attribution sub-claim template.** The
  `attribution` sub-claim requires: (i) the prior readings
  accounted for, each with a resolvable citation; (ii) the
  completeness basis — the search record (corpora and
  literature searched, date, searcher) on which "all prior
  scholarship accounted for" is asserted; (iii) a contest
  state in {uncontested, contested} with, when contested,
  a contest record (who contests, on what evidence, when).
  While contested: the parent renders the contest wherever
  the parent renders, and the parent's stage is capped at
  the adjudicated cap (default `checked`, OD-3).

### 5.3 Explanation and digestion gates (C04)

- **FR-029-06 — Explanation record.** An explanation record
  names a human author, points to a readable account
  artifact by URI with a stored content hash, and names
  where challenges to the account are filed and answered.
  The `accepted` transition requires a valid explanation
  record for the claim (for bundles: for the parent's
  intelligibility sub-claim at minimum). Machine-generated
  text does not satisfy named-human authorship; an account
  substantially drafted with machine assistance must say
  so in the record (AI disclosure per constitution §VI).
- **FR-029-07 — Digestion record.** The `digested`
  transition requires a digestion record evidencing
  independent scholarly engagement with the explanation —
  the qualifying evidence classes are set at adjudication
  (OD-5); the record cites the engagement (citation,
  published challenge and response, independent reuse, or
  the adjudicated equivalent) with resolvable references.

### 5.4 Stage-aware display rules (C06, C07)

- **FR-029-08 — Score placement.** On every surface —
  `IndusEvidenceView`, `DeciphermentPanel`, reports,
  exports, public pages — AEE scores and bands appear only
  inside presentations labelled as checking-stage (lane-1)
  evidence, alongside the falsifier and the checking
  method. No surface sorts, ranks, or leaderboards claims
  or anchors by score or band, and no summary position
  carries a score, band, mean score, or count as a standing
  claim. The `mean_propagated_score` program summary is
  withdrawn or re-presented as lane-1 diagnostics under
  this rule at implementation.
- **FR-029-09 — Not-understood statement.** Every verdict
  record gains a required `not_understood` field (what
  remains not understood, in plain language, written when
  the verdict is recorded), and every verdict display
  renders it with the verdict. A verdict record that lacks
  the field is incomplete and renders as such.
- **FR-029-10 — Lane separation in rendering.** Lane-2
  stage renders in its own region with stage vocabulary;
  lane-1 badges keep checking vocabulary (verdicts, scores)
  and may not use stage names, stage colours, or
  acceptance language. Extraction statuses such as
  `supported` are presented as lane-1 extraction outcomes,
  never as scholarly standing.

### 5.5 Priority/credit registration (C08)

- **FR-029-11 — Priority register.** An intake path (API +
  record store) registers an external scholar's reading:
  claimant name and contact, the reading, its evidence,
  and a server timestamp. Registration issues on record
  completeness alone — no score, stage, or verdict is
  required or implied — and the register entry's credit
  display is invariant under later program assessment of
  the reading. Whether the register is public at intake or
  embargoed is OD-6.

### 5.6 Evidence trails (C09)

- **FR-029-12 — Trail completeness.** Every verdict and
  stage-transition record serializes: evidence references
  with origin groups (evidence counted by origin group, per
  the program's Spec 026 discipline), the falsifier state
  at decision time, the actor (named human or named
  process), and the timestamp. The claims API exposes a
  per-claim trail view; a completeness check over new
  records runs in the claims test suite so a trail-less
  verdict fails CI rather than review memory.

## 6. Acceptance criteria for a future plan

A future implementation plan for this spec is acceptable
only if it: (a) implements FR-029-01…12 without weakening
any governed claim; (b) migrates records additively
(existing fields keep their meanings; stage is a new axis,
not a rename); (c) carries its own freeze, discriminating
controls, and foundation check per house rules; and
(d) disposes of each §8 decision by citing the owner's
recorded adjudication, never by default.

## 7. What this spec does not decide

Everything in §8, plus: any timeline; any assignment of
explanation-writing to specific people; any change to the
287 anchors' tiers as lane-1 records (tiers remain what
they are — checking-stage summaries — whatever OD-1
decides about re-staging their display).

## 8. OPEN OWNER DECISIONS

These are the owner's alone. The draft records the options
and the drafting recommendation where one exists; recording
a recommendation decides nothing.

- **OD-1 — Retroactivity.** Do the 287 anchors' and the
  existing extracted claims' displays get re-staged
  immediately when the lifecycle is implemented, or only
  at next touch of each record? (Immediate re-staging
  changes public-facing displays in one step; next-touch
  leaves known non-conforming displays — including the
  flagged DeciphermentPanel headline — live until each
  record is next edited.)
- **OD-2 — Digestion authority.** Who qualifies as the
  named human whose explanation and digestion records
  count: program-internal authors, external scholars only,
  or either (and if either, whether internal and external
  records carry different weight at the `digested` gate)?
- **OD-3 — Contested-attribution cap.** The exact stage cap
  while attribution is contested. Drafting recommendation:
  cap the parent at `checked` — a claim whose priority or
  completeness is disputed has not been *explained into*
  the literature, only checked.
- **OD-4 — Stage naming.** Adopt Tao's five stage names
  verbatim (created, checked, explained, accepted,
  digested) on all surfaces, or map them to program
  vocabulary in displays while keeping the canonical names
  in data?
- **OD-5 — Digestion threshold.** What evidence qualifies
  a digestion record: e.g. one independent scholarly
  citation of the explanation, one published challenge
  that the account survived or answered, independent reuse
  of the reading, or a defined combination?
- **OD-6 — Priority register visibility.** Is the external
  priority/credit register public at intake (maximum
  protection through visibility) or embargoed until the
  claimant publishes (protection through priority proof
  without exposure)?

## 9. Tooling note (deviation recorded)

Specs 027/028 were authored through the specify agent flow
with the AEE + evaluator extension hooks. The specify CLI
(1.0.10) provides project setup and extension management
only — it has no non-interactive spec-generation command —
and the agent flow was not available in the session that
drafted this spec. This spec and its register are therefore
hand-authored in the exact house format of Specs 027/028
(spec.md + claims.json; adjudication and freeze records to
follow at their lifecycle steps), and no plan.md or
tasks.md was generated, by design (claims-first). If the
owner wants the extension-hook passes (AEE specify checks,
evaluator pass) run over this draft before adjudication,
that is a small follow-up under this spec's number.
