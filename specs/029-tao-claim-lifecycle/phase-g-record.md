# Spec 029 — Phase G Record: CI Gates and Trail Completeness

> Phase G of `tasks.md` (FR-029-12; claim F029-C09; plan §0,
> §2.4). Base: main `587dec70` (Phase E2 merged, PR #186;
> maintenance PR #181's aee pin `>=1.0.4,<1.5` is in this
> history and untouched — the gates are deterministic under
> the pinned resolution, exercised in the CI-parity venv at
> aee 1.4.0). Branch: `impl/029-phase-g-gates`. Date:
> 2026-10-12.
>
> Scope discipline: this phase builds the GATE layer over the
> earlier phases — completeness, recompute integrity, and
> display guards across the whole live data and surfaces. It
> changes no stage, no record, no verdict, no scoring, and no
> display. Where a gate found a real live gap, the gap is
> reported below as a finding with a named disposition; no
> underlying data or machinery was fixed in this phase, and
> nothing was silently allowlisted.

## Live gaps found FIRST (measured before any gate was written)

The gates run over the real live stores. The population is
the Phase D migrated population plus Phase I's preserved
evidence instances: **344 records** — 287 anchors, 31
extracted claims, 15 document-class records (5 registered
predictions + 10 study headlines, from the Phase D
stamped-records sidecar), 3 hypothesis models, and 8
evidence instances preserved on merged claims.

Measured with the Phase C trail builder over that population
at the base head, before any Phase G code existed:

1. **No anchor carries a per-anchor falsifier.** All 287
   anchor trails report `falsifier_state` missing. This is
   the frozen ledger's own flag (`no_per_anchor_falsifier`
   on every anchor entry): the anchor record shape carries a
   basis line, not a falsification condition. The anchors'
   stage transitions are otherwise complete (ledger evidence
   refs, actor, timestamp, source pointer on every event).
2. **No extracted claim's verdict names an actor.** All 31
   verdict events are extraction-era records with no
   `verdict_actor` (Phase C recorded the same gap: its
   synthetic twin's completeness was `missing == ["actor"]`).
   17 of the 31 also carry no falsification condition (named
   in the gate's baseline table, in the test file and below).
3. **The 15 document-class records and 3 hypothesis models**
   carry, in their stamp form, no record-level evidence list
   and no falsifier: their trail profiles are
   `{evidence_refs, origin_groups, falsifier_state}`. The
   sidecar / YAML stamp is a stage record over an underlying
   document (the prediction register, the study reports, the
   model files); the stamp's own stage transitions are
   complete. Measured from the stamp — the form Phase D
   created and Phase G gates — the record-level fields are
   honestly absent.
4. **One real defect, found by the gate (finding, not
   fixed): the Phase C trail builder mis-serializes
   string-form evidence.** 9 live claims carry
   `glossa_lab_evidence` as a *string* (the manual claims:
   the two Parpola claims, the two Yadav 2009 claims, the
   two Yadav 2010 claims, two of the "Without Kings or
   Conquests" claims, and one "Indus Valley Script
   Deciphered" claim). `claim_trail._record_evidence`
   iterates that field as a list before its string branch —
   the string branch is dead code after the loop — so the
   trail serializes one evidence pseudo-ref **per
   character** of the string, including **122
   whitespace-only pseudo-refs** (space characters) across
   the 9 claims and the Yadav 2010 pair's 2 preserved
   instances. The underlying evidence is present and
   meaningful (e.g. "Phase-43: V3 Zipf exponent ~1.35
   (super-Zipfian) [VERIFIED]"); the defect is in the
   trail's serialization of it. Disposition: recorded here
   as a named, dated baseline exception in the gate (the
   test tolerates exactly this violation class on exactly
   these 11 record entries; any other violation anywhere
   fails) — and NOT fixed in this phase, because fixing the
   trail builder is machinery work tasks.md does not assign
   to Phase G. Recommended follow-up (closeout or its own
   change): make `_record_evidence` treat a string value as
   one reference; the exception then empties on its own.
   The 8 evidence instances otherwise match their canonical
   claims' profiles exactly (actor gap on all 8; falsifier
   gap on 6 of them — the Yadav 2010 `manual_001` instance
   carries its falsifier).

**Disposition for gaps 1–3** (the frozen text's own rule):
tasks G1 fails CI on any **new** verdict or stage-transition
record missing the FR-029-12 fields. Gaps 1–3 are properties
of records written before this gate existed. The gate
therefore carries them as an **explicit recorded baseline**
(in `backend/tests/test_spec029_phase_g.py`, named per record
and per field, mirrored by this section): an observed gap
profile must be a subset of the record's baseline profile
(fixing a gap is always allowed); a record with no baseline
entry — any new record — must have an empty profile; a
baseline profile that grows fails. No gap is hidden: the
trail itself still reports every one of them as missing on
every affected record, and this record names them all.

## G1 — Completeness gate

Machinery: `backend/glossa_lab/spec029_gates.py`
(`audit_trail_record`, `trail_gap_profile`,
`evidence_ref_resolves`); tests:
`backend/tests/test_spec029_phase_g.py`.

For every one of the 344 live records, the Phase C trail is
assembled and every event it serializes is hard-checked:

- **stage transitions**: actor present, timestamp present,
  evidence refs non-empty, every ref carrying an origin
  group and resolving (ledger pointers must name a real
  frozen-ledger entry; file pointers must exist with the
  fragment present; URIs/DOIs must have resolvable form;
  a ref naming a live source document must name a real one;
  record-carried evidence resolves to its record of origin),
  falsifier state at decision time serialized (`stated` or
  `absent` — the state is always present), and, on stamped
  records, a source pointer on every event;
- **verdict events**: timestamp, evidence refs with origin
  groups (same resolution rules), falsifier state
  serialized, source pointer;
- **the stage stamp itself**: a stamped stage carries
  `stage_source` and `stage_as_of` (plan §0); an unstamped
  record must be honestly unstamped (a half-stamp — a
  source with no stage — is a defect);
- **transitions above `checked`** in any history were
  written by a named human (the bundle-minimum computation's
  own entries excepted — the sub-claim transitions beneath
  them are the gated ones);
- **gate records (Phase B)**: any record whose stage is
  above `checked` must carry the records that stage
  requires — a valid explanation record at `accepted`, a
  valid digestion record at `digested`, a valid attribution
  template on a bundle parent. No live record sits above
  `checked` today, so this layer is exercised on synthetic
  records (below) and guards the first future promotion.

Live result: **zero hard violations outside the one named
exception** (the whitespace pseudo-refs of finding 4), and
every record's gap profile within its recorded baseline.

Discriminating controls (scratch copies, never committed):
a complete synthetic new record passes both layers; the
same record with `stage_source` stripped, `stage_as_of`
stripped, a history timestamp removed, a history actor
removed, an empty evidence-ref list, or a ledger ref
pointing at a non-existent entry (`…:NOPE-999`) each fails
with the named violation; a new record missing its verdict
actor or its falsifier text acquires a gap profile with no
baseline entry and fails the baseline layer; a record
stamped `accepted` with no (or an invalid) explanation
record, and one stamped `digested` with no digestion
record, each fail the gate-record layer, and their valid
twins pass.

## G2 — Stage-cache recompute integrity (plan §0 / D-E)

`spec029_gates.recompute_stage` / `audit_stage_cache`. Every
stored stage in every live store is recomputed from its
record's evidence, by the rule its `stage_source` names:

- **ledger replay** (all 344 live records today): the
  recomputed stage is the frozen reclassification ledger
  entry's `honest_stage` for the item the source names;
  the record's history tail must land on the stored stage
  and `stage_as_of` must equal that entry's timestamp;
- **bundle-minimum computation**: the Phase B parent-stage
  computation — minimum of sub-claim stages, then the OD-3
  contested-attribution cap and the OD-5 adverse-digestion
  cap (no live bundle parents exist; proven on fixtures);
- **transition-service history tail**: the indexed history
  entry's `to_stage`, with `stage_as_of` equal to its
  timestamp (no live records yet; proven on fixtures);
- **honestly unstamped**: recomputes to `None` and must
  carry no half-stamp.

A stored stage with any other provenance is
**unrecomputable — a defect**, never a pass. The frozen
text's minimum was a sampled population with the full
migrated population on demand; the gate recomputes the
**full** population on every run (344 records, ~1s), which
exceeds the minimum, and any subset can be audited through
the same function on demand.

Live result: **all 344 stored stages recompute equal**
(created 226 · checked 118 across the population — the
Phase D ledger classes' 220 created / 116 checked plus the
8 instances' own stamps: 6 created, 2 checked), all with
`stage_source` / `stage_as_of`
present, and the live provenance is uniformly
ledger-replay today — asserted as its own test, so the
first bundle or transition-service record to enter the
live stores changes a named expectation, not a silent one.

Both-directions corruption controls: a live anchor copied
to scratch with its stored stage **raised** to `digested`
and **lowered** to `created` each fails ("disagrees with
its recomputation"); stripping `stage_source` or
`stage_as_of` fails; a source naming a non-existent ledger
entry is unrecomputable and fails. The same corruption on
a synthetic transition-service record fails, as does a
`stage_as_of` that no longer matches its history entry. A
synthetic contested bundle whose sub-claims are all
`digested` recomputes to `checked` (OD-3) and passes; its
cache corrupted upward to `digested` fails.

## G3 — Gate suite in CI

The Phase B discriminating controls already run under the
standard suite: the CI backend job's invocation is
`pytest tests/` from `backend/` (pyproject
`testpaths = ["tests"]`) with exactly two GPU-only ignores.
Verified by collection under the CI-identical invocation in
the CI-parity venv: **1,712 tests collected**, including
`test_spec029_phase_b.py`'s full file (60 tests) — the
named gate suite in it (the four plan §2.4 controls —
automated actor → `explained`; human `accepted` without an
explanation record; `digested` without independent
engagement; contested bundle rendering above `checked` —
plus the parent-stage computation tests: minimum rule,
OD-3 cap, adverse-digestion pullback ×3) is asserted
present, by name, by a Phase G test that also pins the
workflow invocation and the ignore list, so a future
collection gap (an added ignore, a moved file, a renamed
control) fails CI instead of silently dropping the suite.

The missing meta-test is added
(`test_g3_meta_every_gates_negative_controls_actually_fail_their_gate`):
a registry over the four gates (automated-actor ceiling,
explanation gate, digestion gate, OD-3 attribution cap).
For each gate: its negative-control set is asserted
**non-empty**, every control is executed and must actually
be **rejected** by its gate, and the gate's positive twin
must pass. A control that passes its gate marks the gate
non-differential — INVALID under the program's Spec 026
discipline — and fails this test. Controls include the
subtle ones: an explanation record naming an AI system as
the accountable human, and a digestion record whose
"independent" scholar is the claim's own author.

## G4 — Display guards (program-wide)

Backend guards (served payloads, deep-scanned — the field
may not reappear at any nesting depth):

- dashboard decipherment payload: `sa_aggregate`,
  `fully_decoded_pct`, `n_fully_decoded`, and
  `mean_propagated_score` all absent, and no "signs
  deciphered" headline text anywhere in the payload;
- the aee-scores summary (`assessment_summary`): same
  withdrawals; per-claim lane-1 detail untouched (E1's
  distinction stands);
- the claims payload and one live per-claim trail payload:
  same withdrawals.

Each guard is shown to fail on a reintroduced violation: a
scratch dashboard payload with `sa_aggregate` restored, and
one with `fully_decoded_pct` restored inside a progression
entry, and a scratch summary carrying
`mean_propagated_score`, each raise under the same check
the live payloads pass.

Source/render guards (claim surfaces):

- **Withdrawn headline pattern, program-wide in the
  frontend**: no file under `frontend/src` matches the
  "signs deciphered" headline pattern (the same scan is
  proven to catch the pattern in a scratch source). The
  historical experiment-graph node schemas that declare
  same-named *outputs* (E1's inventory) are backend
  machinery describing historical phase reports, not served
  display payloads — the served-payload guard above is the
  surface the withdrawal governs, and it is deep.
- **Stage synonyms**: on the three claim surfaces
  (`DeciphermentPanel`, `IndusEvidenceView`, `StageLegend`)
  no stage-label synonym (`verified` / `proven` /
  `confirmed`, outside the governed `verified_unexplained`
  flag name) appears; the allowed stage vocabulary is
  exactly the five verbatim names, asserted present in the
  legend source. A scratch mutation reintroducing a synonym
  as a label is caught by the same scan.
- **Lane labels + legend present**: the evidence view
  carries both labelled lane regions and renders the
  legend (source-pinned here; rendered-pinned below).
- **`not_understood` slot**: every verdict display
  serialization carries the slot — `GET /claims` entries
  each carry `not_understood` (the record's own statement
  or `None`) with `not_understood_recorded` agreeing with
  it, for all 31 live claims (all unauthored today: the
  absence form, never substituted text); the renderer's
  two forms (recorded / not-yet-recorded) are pinned in the
  legend source and in the view. Stripping the slot from a
  scratch serialization is detectable by the same check.

Rendered guards (`frontend/e2e/spec029-phase-g.spec.ts`, 4
tests, synthetic fixtures as in E2): the withdrawn headline
pattern appears nowhere on the rendered panel or claims
tab; the rendered stage vocabulary is exactly the five
names with no synonym labels in the legend or either lane
region (`verified` only inside `verified_unexplained`);
every expanded verdict display carries a `not-understood`
slot (one recorded, one not-yet-recorded); lane labels, the
legend, and the panel stage summary naming all five stages
are present. Run locally against this worktree's built
frontend + backend: **4 passed**, with the neighbouring
E2 spec's 5 tests also passing unchanged (9 passed total).

**Inventoried, not guarded (honest scope note).**
`SignsView.tsx` still renders a "{n} deciphered /
{n} undeciphered" per-sign count line from the signs API's
per-sign flags (E1's inventory, deferred by E2's record to
Phase G). It is not one of tasks G4's named guards — G4
names the panel headline pattern, the dashboard fields, and
the scores-summary mean, all of which are guarded above —
and the per-sign flags are a different construction from
the withdrawn "{totalAnchors} signs deciphered" headline
(no such headline text exists anywhere in `frontend/src`,
guarded). Changing the SignsView rendering is a display
change, not a gate; it is recorded here as the standing
follow-up E1/E2 named, for the owner / closeout to
dispose. The CorporaView / HelpView uses of
"undeciphered" for world scripts in general (E1 inventory)
are likewise not Indus decipherment claims and are out of
the guards' scope.

## Evidence (G5 gate)

- **New code**: `backend/glossa_lab/spec029_gates.py` (the
  gate machinery), `backend/tests/test_spec029_phase_g.py`
  (**26 tests**), `frontend/e2e/spec029-phase-g.spec.ts`
  (4 tests). No existing file's behaviour is changed; no
  existing test is weakened or edited.
- **Foundation check**: **40 passed / 0 failed / 8
  warnings** — identical to the pre-change baseline (run
  with the gitignored Holdat CSVs copied in, never
  committed).
- **Full backend suite** (`pytest backend/tests`, CI's
  GPU-only files excluded as in CI; CI-parity venv
  `~/workspace/venvs/glossa-ci-pin`, aee **1.4.0**):
  **1407 passed, 6 skipped, 0 failed** — the 1381 passed /
  6 skipped merged baseline plus exactly this phase's 26
  new tests.
- **Collection check (G3)**: CI-identical `--collect-only`
  run: 1,712 tests collected, Phase B and Phase G files
  included, neither in the workflow's ignore list.
- **Frontend**: the new Playwright spec **4 passed**
  locally (with E2's 5, 9 total) against the locally served
  built frontend + backend on port 8002 (port 8001 held a
  stale-tree backend, left untouched, as in E1/E2). The
  full frontend suite is CI's Frontend tests (Playwright)
  job; its result is in the PR gate evidence.
- **Lint**: ruff clean on every authored Python file.
- **Branding sweep**: no other-company or other-program
  names in any authored or edited file.
- **Frozen bytes**: nothing digest-covered under
  `specs/029-tao-claim-lifecycle/` was edited; this record
  and the LEDGER entry are the phase's additions there.
  Running the backend suite regenerates extraction
  timestamps in `glossa-indus/claims/extracted_claims/*.json`
  (and one claim-report file) as a pre-existing side
  effect; those files were restored byte-identical before
  commit.
- **PR / CI / merge**: PR and CI evidence are completed in
  the gate-evidence follow-up to this record (a merge
  commit cannot name itself in the content it merges; the
  PR number, CI run, merge SHA, and the API-verified new
  main head are stated in the PR timeline and in this
  phase's delivery report).

## Deviations and honest limitations

- **Worktree source**: cloned `--shared` from the Phase
  E2 worktree as briefed; the `github` remote was repointed
  at the GitHub URL (the clone inherits the source
  worktree's local path as its origin) and the branch cut
  from the fetched `github/main` at the exact brief head
  `587dec70`. No deviation in tree.
- **G1 baseline vs. the frozen text**: the frozen text
  says the gate fails on any *new* record with a missing
  field; it does not say the pre-existing records' known
  gaps (recorded by Phases C and D and the frozen ledger
  itself) should turn CI red on day one — a gate that is
  red on day one and ignored is worse than no gate. The
  recorded-baseline mechanism above is how this phase
  implements the frozen rule faithfully: new records are
  held to the full standard mechanically (no baseline
  entry = no gap allowed), and legacy gaps are named,
  dated, and shrinkage-only. This is a judgment the phase
  record owns explicitly.
- **G2 exceeds the frozen minimum**: tasks say "sampled
  population; full migrated population on demand"; the
  gate runs the full population every time. Stronger, and
  cheap; recorded so the difference is visible.
- **Finding 4 is a defect this phase did not fix** (the
  trail builder's string-evidence serialization). It is
  the one live violation class the gates tolerate, under
  the named exception, because the fix belongs to trail
  machinery Phase G was not assigned. If the owner prefers
  the fix inside this spec, it is a small follow-up PR
  against `claim_trail.py` with the Phase C tests as its
  regression suite.
- **Gate records above `checked`** (G1's Phase B layer and
  the bundle recomputation in G2) are fixture-proven only:
  no live record is a bundle parent and none sits above
  `checked`. The gates guard the first such record; they
  do not certify a live population that does not exist.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
