# Spec 029 — Retroactive Realignment Audit: The Existing Claim Set Under the Tao Standard

> Audit date: 2026-10-12. Auditor: program (AI agent,
> Muse Spark, at the direction of Tristen Pierson).
> Codebase state: `origin/main` at `5c1f7d5e`; live backend
> queried 2026-10-12. Companion records:
> `assessment.md` (gap assessment of the claim machinery),
> `spec.md` (claims-first draft, F029-C01…C10, all draft),
> `reclassification-ledger.json` in this directory (the
> machine-readable per-item ledger this audit writes).
>
> Owner directive (2026-10-12): the Tao realignment is
> retroactive — audit and re-run the discipline across all
> previously done work in Glossa-Lab and prove the current
> claim set is disciplined under the eight points. This
> audit is that re-run for the Indus claim set. It changes
> **no code and no live record**: every correction below is
> a dated, appended record (the ledger). Display-rule
> fixes stay gated behind Spec 029 adjudication (OD-1).
> History is never rewritten — including by this audit.

## 1. Method

**Sources, all read live on 2026-10-12:**

- `backend/reports/INDUS_FINAL_ANCHORS.json` — the 287
  anchor readings (canonical file).
- `reports/phase108_provenance_register.json` — the
  Phase-108 provenance register (287 records), joined with
  the strict-set rule in
  `backend/glossa_lab/pipelines/phase109_followthrough.py`
  (`strict_sa_independent_hm`).
- The running backend (localhost:8001), via the MCP
  client: `list_indus_claims` (aee=true),
  `get_indus_claim_aee_scores`, `get_foundation_status`,
  `get_discovery_stats`, `list_discovery_items` (sampled),
  `list_experiments`, `list_indus_hypotheses`,
  `list_reports`, `list_anchor_sets`, `get_status`.
- `reports/foundation_check_report.json` — the foundation
  suite's last recorded run.
- The Spec 026 impact register and appended historical
  assessments (116 items) — the governing correction
  record for the pre-026 study span.
- Presentation surfaces read directly: `README.md`,
  `frontend/src/components/DeciphermentPanel.tsx`,
  `frontend/src/components/IndusEvidenceView.tsx`,
  `backend/glossa_lab/aee_core.py`,
  `backend/glossa_lab/api/dashboard.py`, and the live
  GitHub repository description.

**Disclosure — backend restart.** The backend was down
when the audit began (connection refused; the 2026-10-11
VM replacement had killed the long-running process). The
auditor started it with the documented recipe (project
venv uvicorn on :8001). All API figures below are from
that live instance. One consequence is itself a finding
(§5, P8): the foundation status endpoint returned nulls
in the fresh process although a current report file
exists on disk.

**Staging rules applied (uniform, stated in advance of
the results).** A claim is staged by the strongest
completed lifecycle act *evidenced in its own records*:

- `created` — the claim exists as a record (proposed,
  extracted, or registered). Registration counts as
  creation, not checking.
- `checked` — a lane-1 check with a recorded outcome ran
  against the claim under a live (not falsified) method:
  a test outcome status, a frozen-design study verdict,
  or passage of the Phase-108/109 SA-free provenance rule
  for anchors. A computed AEE *score* alone does not make
  an `untested` claim checked: the score evaluates the
  record's evidence profile, and the record's own status
  says no test ran.
- `explained` — requires a named-human explanation
  artifact (Spec 029 FR-029-06). Program/AI-authored
  outcome documents do not satisfy named-human authorship.
- `accepted` / `digested` — require the FR-029-06/07
  records. No such records exist anywhere in the audited
  set, so no claim is staged above `checked`. This is a
  statement about evidence, not about quality: it is the
  standard's central point that checking alone never
  settles a claim.

**Scope limits, stated plainly.** Study verdicts from
Specs 001–023 and the phase lines to Phase-141 are
ledgered as one grouped entry governed by Spec 026's
per-item historical assessments (116 items), rather than
duplicated item-by-item here. Published surfaces outside
this repository (the program's web pages) are outside
this audit's remit; immutable published deposits are
dealt with in §7. Zenodo deposit texts were not
re-fetched; §7 names them from the program's own records
(the README re-base note and the release ledger).

## 2. Inventory — counts by source, reconciled

| # | Source | Count | What it is |
|---|---|---|---|
| A | Anchors (`INDUS_FINAL_ANCHORS.json`) | **287** | the program's headline decipherment claims |
| B | Extracted claims (backend, `GET /claims`) | **31** | literature claims scored through the AEE wiring |
| C | Hypothesis Library models | **3** (8 sub-claims) | encoded rival/interpretive models |
| D | PRED-2026 register (live items) | **5** | 001/002/003 pending; 006/007 partially confirmed (004/005/008/009 retired 2026-10-12, before this audit) |
| E | Study headline claims (Specs 001–028 + phase lines) | **28 spec records**; Spec 026 register: **116 items** | lane-1 verdicts under (mostly) frozen designs |
| F | Foundation check suite | **48 recorded checks** (40 OK / 0 fail / 8 warn) | lane-1 integrity instrument, not claims |
| G | Discovery corpus | **654 items** | intake records, not claims |
| H | Experiment registry | **27 definitions** | definitions, not claims; results live in E |
| I | Report stores | **791** backend-registered records (736 data / 55 document); 40 files in `backend/reports/`; 273 files in `reports/` | artifacts and trails |
| J | Stored anchor sets | **104** | working artifacts; the strict 94 is **not** a stored set — it is computed by rule |

**Reconciliation (every cross-source count checked):**

- Anchors: the file's `total`, `total_all_entries`, and
  `metadata.total_count` all read 287; the Phase-108
  register holds exactly 287 records; the foundation
  report's anchor check reads "total=287 actual=287
  (H+M=171, LOW+CANDIDATE=116)". **287 reconciles
  everywhere.** Tier split in the file: HIGH 166 /
  MEDIUM 5 / LOW 3 / CANDIDATE 113.
- The strict set: recomputed from the register + the
  Phase-109 rule during this audit = **94 (90 HIGH +
  4 MEDIUM)** — exactly the published
  figure (73.68% = 5,159/7,002 Holdat tokens). The
  headline number has an inspectable trail, but only via
  this join: the anchors file itself carries no
  strict-set flag (see P8).
- The 44 `pending_non_sa_validation` anchors reconcile
  three ways: the file's `validation_status` count (44 =
  43 HIGH + 1 MEDIUM), the register's SA-lineage
  categories (SA_CONFIRMED_ONLY 20 + SA_DERIVED 24), and
  the Phase-128 dossier set (44 dossiers).
- H+M decomposition (auditor-computed, exact):
  171 = **94 strict** + **44 pending** + **33 HIGH with
  SA in their provenance chain** (`sa_in_chain` true;
  register categories DEDR 15 / LITERATURE 9 / MIXED 9).
  The 33 are the audit's sharpest anchor finding (§5, P1).
- Extracted claims: the backend reports `total: 31` —
  the directive's "31+" is verified as **exactly 31**.
  **Discrepancy against the last recorded distribution**
  (Phase-104, 2026-10-05: 16 untested / 6 contradicted /
  4 partially_supported / 4 strongly_supported /
  1 partially_falsified): the live distribution is
  **21 untested / 1 contradicted / 1 partially_falsified /
  4 partially_supported / 4 strongly_supported**. Cause,
  evidenced not smoothed: the current set is a single
  re-extraction batch — all 31 records carry
  `extracted_at` timestamps within one second on
  2026-10-09, from 10 source documents. The claim set is
  an extraction artifact, regenerated wholesale; it is
  not a stable register, and two propositions are
  recorded twice from different documents (§5, P2).
- Foundation: the suite's last recorded run
  (`reports/foundation_check_report.json`, regenerated
  2026-10-12) reads 40 OK / 0 fail / 8 warn, verdict
  "READY WITH CAVEATS" — consistent with the Spec 028
  closeout record (2026-10-11).

## 3. Stage distribution after the honest re-run

Per-item assignments are in
`reclassification-ledger.json` (345 entries: 336 staged
claim items + 9 grouped/surface records). Summary:

| Class | created | checked | explained | accepted | digested |
|---|---|---|---|---|---|
| Anchor readings (287) | 193 | 94 | 0 | 0 | 0 |
| Extracted claims (31) | 21 | 10 | 0 | 0 | 0 |
| PRED-2026 live (5) | 3 | 2 | 0 | 0 | 0 |
| Hypothesis models (3 records / 8 sub-claims) | 3 | 0 | 0 | 0 | 0 |
| Study headline claims (10 ledger entries: Specs 019–028 named + 001–023 grouped) | 0 | 10 | 0 | 0 | 0 |
| **Total staged** | **220** | **116** | **0** | **0** | **0** |

Anchor `created` composition: 44 pending SA-lineage +
33 HIGH with SA in chain + 113 premise-superseded
CANDIDATEs + 3 LOW. Anchor `checked` = the strict 94,
every one flagged `verified_unexplained`.

**The headline of this audit is the zero columns.**
Nothing in the program — not one anchor, claim,
prediction, or study headline — carries a named-human
explanation record or any digestion evidence. Under the
adopted standard, the entire claim set stands at the
first two stages. Everything the program has verified
is, in the standard's terms, verified-but-unexplained:
a flagged risk state, now flagged in the ledger item by
item (105 entries carry the `verified_unexplained`
flag: the strict 94 anchors, the 8 supported-class
claim records, and the SUPPORTED study headlines
F1, F3, and G1).

## 4. Demotions — every display that outran its evidence, named

A "demotion" here is a ledger reclassification from an
acceptance-flavoured *display* to the honest stage. No
record was edited; the displays below are what a reader
of the surface would reasonably take the claim to be.

1. **The 287 anchors as "signs deciphered"**
   (`DeciphermentPanel` footer) → staged **created (193)
   / checked (94)**. The single largest display-versus-
   evidence gap in the program (§5, P5).
2. **33 HIGH anchors with SA in their provenance chain**
   → **created**. They display at the top tier with no
   per-record marker distinguishing them from strict-set
   HIGH anchors, yet they fail the program's own strict
   rule and have no SA-free validation outcome.
3. **8 extracted-claim records** displayed
   `strongly_supported` (4) / `partially_supported` (4),
   all with AEE band `high` → **checked**. Two of the
   four `strongly_supported` records carry **no
   falsifier at all**; two propositions in this set are
   double-recorded (§5, P2), so the 8 records state
   ~6 distinct propositions.
4. **1 extracted claim** displayed `partially_falsified`
   with AEE band **`high`** → **checked**, band recorded
   as a lane-1 artifact in conflict with its own status
   (the band derives from the propagated score, not from
   the test outcome).
5. **PRED-2026-006 / 007** displayed "PARTIALLY
   CONFIRMED" → **checked** (partial lane-1 outcomes;
   wording flagged, records untouched).
6. **The dashboard's SA aggregate and "fully decoded %"
   ** → recorded as a falsified-method display
   (SURFACE-DASHBOARD-API-SA-AGGREGATE); the underlying
   SA result set stands falsified at Phase-107 and
   nothing staged in this audit rests on it.

## 5. Nonconformances by Tao point

### P1 — Five stages: ABSENT in machinery; re-run shows a two-stage program

`assessment.md` established the machinery gap (one flat
`claim_status`; no stage fields anywhere). This audit's
re-run adds the population-level consequence: staged
honestly, the program's 336 claim items sit at `created`
(220) and `checked` (116), with **zero** at `explained`
or beyond — while at least three display surfaces
(§4.1, §4.3, §4.5) present lane-1 outcomes in
acceptance language. The 33 HIGH anchors (§4.2) are the
purest P1 failure at item level: a top-tier display with
no completed live-method check behind it, invisible as
such in the canonical file (their `validation_status`
field is simply absent — 130 anchors carry no
`validation_status` at all).

### P2 — Decomposition: ABSENT for anchors; PARTIAL and defective for claims

- Anchors: **0 of 287** records carry a falsifier or
  falsification field (full field census run during this
  audit). Falsification exists at *set* level (phonotactic
  violation counts, site-invariance tests, the Phase-134
  falsification suite) but no anchor decomposes into
  soundness / scholarship-accounting / attribution /
  intelligibility sub-claims. One correction to
  `assessment.md`'s sample-based wording, recorded in its
  spirit: the anchor record is *not* uniformly the bare
  4-field shape — only 7 of 287 records have exactly
  `{reading, confidence, basis, reading_direction}`;
  the file accreted **56 distinct field shapes** over
  successive phases (basis text median 167 chars, max
  831). The gap is therefore worse in kind, not better:
  annotation-rich but schema-drifted, with no governed
  structure in any shape.
- Extracted claims: **17 of 31 carry no
  `falsification_condition`** — including 2 of the 4
  `strongly_supported` records. A claim displayed at the
  strongest support level with no stated falsifier is a
  direct P2 violation, named here and per-item in the
  ledger.
- Duplication: two propositions are each recorded twice
  (the Zipf–Mandelbrot frequency claim ×2, both
  `strongly_supported`, score 1.0; the text-begin/end
  sign claim ×2, both `strongly_supported`, no
  falsifier). Evidence counted per record therefore
  double-counts these propositions wherever record
  counts are read as claim counts.

### P3 — Digestion: ABSENT everywhere; the risk state is the program's normal state

No explanation artifact, named-human account, or
digestion record exists for any item in any class
(verified by surface search: the only "not understood"
hit in the codebase is an unrelated sentence in
`backend/glossa_lab/data/meroitic.py:77`). The closest
artefacts — Spec 026's appended historical assessments
and Specs 027/028's outcome and assessment documents —
are program (AI) authored and disclosed as such; under
FR-029-06 they do not satisfy named-human explanation.
105 ledger entries are flagged `verified_unexplained`.
Digestion is not a gap in this program; it is, at
present, an entirely unoccupied stage — which is
precisely the condition the standard orders tracked.

### P4 — Attribution: PARTIAL at document level; ABSENT as a governed claim; live contests unflagged

- Anchors: 236 of 287 carry a `source` string; **51
  carry none**. Provenance *classes* exist (Phase-108
  register categories) but no per-anchor completeness
  record ("all prior scholarship accounted for, on this
  search") exists, and no record carries a contest state.
- Contests are live in the program's own data and
  invisible on the records: the Phase-125
  cross-compilation DISAGREEMENT verdict (median TV
  0.637; Phase-131: 93.9% of it unattributed); 25 of the
  44 Phase-128 dossiers close as crosswalk-contested;
  sign M402 is triage-CONTESTED in the Bhaskar comparison;
  M222's reading was reclassified on its dossier
  (`kur` → CANDIDATE, premise superseded). None of this
  renders on the affected anchor records as attribution
  under contest.
- Extracted claims: `source_document_id` on 31/31
  (document attribution exists); `author` on **2/31**;
  no completeness evidence on any.

### P5 — Anti-gradability: VIOLATED on live surfaces (worst findings of this audit)

1. `DeciphermentPanel.tsx` (archived-state footer,
   verified at lines 553–557 of the current file):
   "**{totalAnchors} signs deciphered** — all signs
   encountered in the publicly accessible Holdat + ICIT
   + Firestore corpora have Proto-Dravidian readings
   ({high} HIGH confidence)." A volume count as a
   decipherment claim, plus an unqualified assertion of
   readings for every sign in three corpora — against
   the program's standing position (repo description,
   owner statements) that **the script is not
   deciphered**.
2. The dashboard API still assembles and serves
   `sa_aggregate` (an SA run's `aggregate_confidence`)
   and `fully_decoded_pct` / `n_fully_decoded`
   (`backend/glossa_lab/api/dashboard.py:1206–1236`),
   and the panel consumes both. A falsified method's
   aggregate and a "fully decoded" percentage, live,
   unlabelled as falsified.
3. `GET /claims/aee-scores` exposes
   `mean_propagated_score` — live value **0.484903** —
   a single program-level mean of checking-stage scores
   (`aee_core.py:328`).
4. The AEE `band` derives from the propagated score and
   is displayed beside statuses, producing intra-record
   contradictions (a `partially_falsified` claim wearing
   band `high`; 21 `untested` claims wearing band
   `low` — a graded judgement on claims whose own status
   says untested).
5. `README.md` leads with a "Decipherment Status"
   metric tally (readings count, coverage %, violation
   counts, z-values). The README is simultaneously the
   program's most honest surface — its re-base note
   retires the v4 headline explicitly and two table
   rows label themselves "computed on the retired
   161-anchor set" — and a P5 tension: the tally *is*
   the headline, caveats notwithstanding. Recorded as
   tension, not violation; two factual staleness errors
   in it are recorded separately (§6, surface entries).
6. The foundation report labels scholarly claims
   "VERIFIED" in its `solid_claims` annotations (e.g.
   the Phase-31 Zipf slope) — defensible as data-
   integrity language, but the label attaches to
   scholarly content, not just file integrity, and the
   annotations are stale (§5, P8).

### P6 — Two lanes: ABSENT; lane-1 wears lane-2 clothing on every user surface

`IndusEvidenceView.tsx` renders `claim_status` as a
coloured standing badge beside the claim text
(`strongly_supported` = green `#16a34a`, colour map at
lines 43–51; badge colour applied at line 402), with
no lane label anywhere in
the API response or UI. Extraction outcomes and AEE
scores (lane 1) are the only states the UI can express;
the stage axis (lane 2) does not exist as data
(F029-C01/C07 territory). The expanded claim view shows
falsifier and evidence — good lane-1 material, unlabelled.

### P7 — Priority/credit: ABSENT (no new evidence; confirmed at population level)

No registration instrument exists for an external
scholar's early reading. The program's own PRED-2026
register is the only priority instrument and covers
only the program's predictions. Readings the program
ingests from literature (the anchors' `source` strings;
the wave-1 correspondence now open with three scholars)
acquire no timestamped priority record independent of
the program's assessment. Nothing in the audited
population contradicts `assessment.md`'s ABSENT.

### P8 — Inspectable trails: PARTIAL, with three concrete defects

Strengths first (they are real): the strict-94 headline
reproduces **exactly** from the Phase-108 register +
Phase-109 rule; the anchors file self-documents its
counting rules (`metadata.canonical_counts`) and its
totals reconcile across four independent sources;
Specs 024–028 ship frozen designs, controls, and
outcome records, and F3/G1 carry their confounder
riders in every headline (the program's best
not-understood practice); Spec 026's append-only
historical assessments are the model correction record.

Defects:

1. **Strict-set membership is not inspectable from the
   canonical file.** `INDUS_FINAL_ANCHORS.json` has no
   strict flag; membership requires joining
   `reports/phase108_provenance_register.json` under a
   rule that lives in a pipeline module. A reader of
   the headline file alone cannot tell a strict HIGH
   from a chained HIGH (§4.2) or a pending HIGH.
2. **Claim trails are fragments.** Of 31 claim records:
   `glossa_lab_evidence` on 9, `contradicting_evidence`
   on 1, `quote_fragment` on 15, no actor and no
   timestamp for any status (only `extracted_at`), no
   origin-group serialization anywhere.
3. **The foundation trail is not API-inspectable.**
   `get_foundation_status` returned `last_checked_at:
   null, verdict: null, n_ok/n_fail/n_warn: 0` in the
   fresh backend process, while a current report file
   (40/0/8, "READY WITH CAVEATS") exists on disk. The
   suite's own annotations (`solid_claims` /
   `caveated_claims`) embed Phase-48-era figures —
   "37 HIGH + 36 MEDIUM (Phase-48+51 validated)… 75
   LOW… 1 UNCERTAIN (M267)" — that contradict the
   current anchor table (166/5/3; M267 resolved and
   reclassified): stale prose riding inside a live
   report, unflagged.
4. **No verdict anywhere states what remains not
   understood** as a field (search: zero hits on the
   claim/report/frontend surfaces). Where the substance
   exists — F3's confounders, G1's chronology rider,
   Phase-131's 93.9% residual — it exists as prose
   discipline in specific documents, not as a property
   of verdict records.

## 6. Corrections applied by this audit (records written)

Append-only, all dated 2026-10-12, all in this
directory or the ledger it feeds:

1. **`reclassification-ledger.json`** — 345 entries:
   per-item reclassifications for all 287 anchors and
   all 31 extracted claims (old displayed status,
   honest stage, reason, evidence pointers, flags);
   per-record entries for the 3 hypothesis models and
   the 5 live PRED items; named entries for the
   headline claims of Specs 019, 023, 024 (×3), 025,
   027, 028 (×2) plus one grouped entry for
   Specs 001–023 governed by Spec 026's assessments;
   grouped records for the foundation suite, the
   discovery corpus, and the experiment registry; and
   6 presentation-surface entries recording the
   nonconforming displays (§4, §5-P5) as flagged —
   **flagged, not fixed**: display changes are gated
   behind Spec 029 adjudication (OD-1).
2. **This audit (`audit.md`)** — the written report the
   owner directive requires.
3. **A `LEDGER.md` entry** recording this audit
   session, per house rule H1.

Nothing else was written. No anchor, claim, score,
verdict, register entry, or display string in any live
record was modified, re-scored, or re-worded by this
audit (F029-C10 honoured).

## 7. Historical limitations — unfixable published surfaces, labelled

These surfaces present claims beyond their honest
stage and **cannot be corrected in place**. They are
labelled HISTORICAL LIMITATION here, plainly, and stand
as published; the label, not an edit, is the correction
available.

1. **The v4 preprint** — Pierson (2026), *A
   Falsifiable Computational Decipherment Hypothesis
   for the Indus Valley Script: 161 Candidate
   Proto-Dravidian Anchors and a Three-Slot Positional
   Grammar*, Zenodo DOI 10.5281/zenodo.20414696 (also
   SSRN submission 6827038). Its headline set (161 H+M
   anchors / 90.96% coverage / 59% Parpola agreement)
   is the SA-era basis the program retired on
   2026-10-06. The deposit is immutable; the README
   re-base note is the program's standing correction,
   and a v5 addendum exists only as an unsubmitted
   draft. **HISTORICAL LIMITATION.**
2. **Zenodo program releases v4.1.0–v4.10.0** (records
   23219644 … 23298334). Frozen deposit texts; the
   SA-era releases present the pre-rebase headline
   basis. Later releases (v4.8.0 onward) were
   gate-verified against the rebased record, but no
   frozen text can be amended in place.
   **HISTORICAL LIMITATION** (earlier releases);
   the release series as a whole is superseded in
   interpretation by the 2026-10-06 re-base and this
   audit.
3. **The OSF PRED-2026 registration mirror**
   (osf.io/bg8yx, DOI 10.17605/OSF.IO/BG8YX).
   Registrations are immutable by design; the mirror
   preserves the 2026-04-23 register as registered —
   including PRED-2026-004/005/008/009, whose
   retirements (2026-10-12) live in the repo register's
   §6 and cannot be annotated onto the frozen OSF
   record. **HISTORICAL LIMITATION.**
4. **Phase-era report files** (`reports/`, 273 files;
   `backend/reports/`, 40 files) containing SA-era
   results presented as findings (e.g. the master
   synthesis and readiness reports of the Phase-16x
   span). Internal records, append-only by house rule:
   they stand as the record of what was run. Their
   claims are superseded by Phase-107/109 and staged
   by this audit; they must not be cited as current
   positions. **HISTORICAL LIMITATION** (as a class).
5. **The retired GitHub repository description**
   ("161 H+M proto-Dravidian readings, 90.96% token
   coverage…") — already replaced on 2026-10-11 with
   an honest description ("The script is not
   deciphered"); the retired text survives in
   screenshots and caches outside the program's
   control. **HISTORICAL LIMITATION**, residual only.

## 8. What already conforms (recorded so the audit is a proof, not only an indictment)

- The **GitHub repository description** (live, verified
  2026-10-12) states the strict core as a hypothesis
  and says plainly: "The script is not deciphered."
- **PRED-2026-001/002/003** are displayed PENDING and
  have never been scored on a non-qualifying corpus;
  the register's append-only discipline held again on
  2026-10-12 (retirements appended at §6, originals
  untouched).
- **Specs 024–028** ran under designs frozen and (027,
  028) OSF-registered before execution, with
  discriminating controls, INVALID outcomes recorded
  against the program's own first attempts (Phase-384
  v1, Phase-392's stopped first launch), and
  confounder riders carried in headlines (F3, G1).
- **Spec 026** is the program's own precedent for this
  audit: 116 items re-read, 75 statuses changed, all by
  appended historical assessments, originals never
  rewritten.
- The **anchors file's counting discipline**
  (`metadata.canonical_counts`; four-way reconciliation
  in §2) and the **Phase-128 dossiers** (evidence
  assemblies for all 44 pending anchors, including
  their contested breakdowns) are genuine trail
  artefacts — partial P8 conformance to build on.

## 9. Owner decisions needed

This audit is the evidence base for two of Spec 029's
open decisions, and surfaces five further decisions.
None is taken here.

**Bearing on OD-1 (retroactivity — re-stage displays
immediately vs at next touch).** The audit's evidence:
two of the nonconforming displays are *live machinery*,
not archived text — the DeciphermentPanel headline
(§5-P5.1) and the dashboard API's SA aggregate /
fully-decoded percentage (§5-P5.2) are served by the
running program today. "Next touch" for these surfaces
may never arrive as a natural edit; leaving them live
leaves the program's own dashboard asserting a
decipherment the program disclaims. The audit records
this as the strongest evidence for immediate re-staging
of *displays* (records are untouched either way — the
ledger above already stages every item on paper).

**Bearing on OD-3 (contested-attribution cap).** The
audit's evidence: attribution contest is not an edge
case in this claim set — a FAIL-verdict cross-compilation
disagreement with a 93.9% unattributed residual, 25 of
44 pending-anchor dossiers crosswalk-contested, and at
least one named contested sign (M402) sit inside the
population the cap would govern, and the strict set's
own crosswalk comparison is recorded in the README as
"partially tautological (identity-only entries)". A cap
set at `checked` (the draft's recommendation) would, on
this evidence, bind on a material share of headline
readings the moment attribution sub-claims exist; the
owner should choose the cap knowing it is a working
constraint, not a formality.

**Further decisions surfaced by the audit:**

- **D-A — The 33 chained HIGH anchors.** Annotate in
  place (additive record field), demote their display
  tier, or leave display as-is under this audit's
  ledger staging alone? The audit recommends annotation
  at minimum: at present nothing in the canonical file
  distinguishes them from strict HIGH anchors.
- **D-B — Duplicate extracted claims.** Two propositions
  are double-recorded (§5-P2). Deduplication is a data
  change to the claims store — owner call, with the
  extraction batch (2026-10-09) as the unit of repair.
- **D-C — README factual errata.** Two statements are
  factually wrong against the canonical file (tier
  split 112 LOW / 4 CANDIDATE; "44 further HIGH").
  Are factual errata of this kind correctable
  immediately as errata, distinct from interpretive
  re-staging under OD-1? The audit recommends yes:
  they misstate the record, not a framing.
- **D-D — Foundation report annotations.** Refresh the
  embedded `solid_claims` / `caveated_claims` prose to
  the current anchor table, or freeze the file with a
  dated as-of label? Either removes the present state:
  stale figures riding unflagged in a live report.
- **D-E — Where the stages live.** Attach this audit's
  stage assignments to the anchors file and claims
  store as additive fields now (a record change under
  the owner's retroactivity directive), or hold them
  in this ledger until the Spec 029 implementation
  plan lands? The ledger is complete either way; the
  question is whether the live records carry their
  stages before the machinery exists to maintain them.

---

*Audit closes. Records written: `audit.md`,
`reclassification-ledger.json` (345 entries), and the
`LEDGER.md` session entry — all appended to draft PR
#164's branch, which remains DRAFT and unmerged for
owner adjudication. AI disclosure: executed by an AI
agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
