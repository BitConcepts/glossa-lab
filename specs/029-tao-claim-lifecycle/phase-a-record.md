# Spec 029 — Phase A Record: Stage Axis and Transition Core

> Phase A of `tasks.md` (FR-029-01…03; claims F029-C01, F029-C02;
> plan §0, §2.1 Workstream 1). Base: main `a38cf92e` (spec + plan +
> freeze, PR #168). Branch: `impl/029-phase-a-stage-core`.
> Date: 2026-10-12.

## What was built, and where

**A1 — Record shapes.** New module
`backend/glossa_lab/claim_stage.py` defines the additive stage shape
shared by the extracted-claims record shape and the anchor record
shape: `stage`, `stage_source`, `stage_as_of`, and append-only
`stage_history` entries of `{from_stage, to_stage, actor, timestamp,
evidence_refs, reason}`. `stage_defaults()` / `with_stage_defaults()`
supply the shape with **unstamped** defaults (`stage=None`): shapes
and defaults only — no live record was stamped, edited, or migrated
in this phase (that is Phase D, whose ledger-sourced values are the
only ones this shape will carry). A record without a stamped stage
behaves sanely everywhere the shape is read: it serializes with
`stage=None, stamped=False`, it is never silently assigned a stage,
and its first legal transition is to `created`. No existing field
changed meaning anywhere in this phase.

**A2 — AEE mapping.** `backend/glossa_lab/aee_core.py`:
`claim_from_glossa` now maps the stage axis as a distinct object —
`serialize_stage(raw)` preserved in
`Claim.metadata["glossa_stage"]` — never folded into `ClaimStatus`
or confidence, and not an input to scoring. The regression test
captures the pre-change behaviour first: the expected scores in
`backend/tests/fixtures/spec029_pre_change_aee_scores.json` were
produced by running the code at main `a38cf92e`, before any Phase A
edit, over the current 31-claim set; the test asserts every claim's
`ClaimScore.to_dict()` after the change equals the captured dict
byte-for-byte under canonical JSON serialization (and the summary
`mean_propagated_score` is unchanged at 0.484903).

**A3 — Transition service.** `claim_stage.transition_stage` is the
single writer of stage changes. It enforces: forward moves exactly
one step along created → checked → explained → accepted →
digested (an unstamped record's first step is `created`); backward
moves to any earlier stage only with a recorded reason; automated
actors (allowlist plus process-token detection:
extraction / scoring / research loop / batch jobs, and any actor
declared `actor_kind="automated"`) may write only
`created`/`checked` transitions and fail closed at or above
`explained` on either side of a move; any transition touching a
stage above `checked` requires a named-human actor — a process name
never validates (`is_named_human` rejects allowlisted/process-token
names, non-human `actor_kind`s, and empty/non-alphabetic names) —
and an advance above `checked` additionally requires a non-empty
`evidence_refs` trail. Every successful write updates `stage`,
`stage_source` (`transition-service:stage_history[<n>]`, the §0
provenance of the cache) and `stage_as_of` together, and appends
the history entry; a refused transition writes nothing.

**A4 — Endpoint serialization.** Stage and lane-1 score serialize
as distinct objects on every Phase A surface:

- `GET /claims` (`backend/glossa_lab/api/indus_evidence.py`): each
  claim carries `stage` = the serialized stage object (value,
  provenance, full history, count, latest transition) and the
  computed `verified_unexplained`; with `?aee=true` the lane-1 score
  is a separate object (`aee_score`, aliased `lane1_score`).
  Scoring runs over the raw records, not the serialized entries.
- `GET /claims/aee-scores` (via `aee_core.assessment_summary`): each
  per-claim entry gains `stage` (object), `lane1_score` (the lane-1
  score under its lane name; `aee_score` kept for compatibility),
  and `verified_unexplained`.
- Anchor surfaces: the signs API (`backend/glossa_lab/api/signs.py`,
  the `INDUS_FINAL_ANCHORS.json` surface) adds the same `stage`
  object and `verified_unexplained` to each entry — final anchors
  from their own record fields, and staging / anchor-set entries
  (which share the index) as unstamped stage objects from
  `_build_sign_entry` — separate from its lane-1 `confidence` tier;
  the dashboard decipherment
  summary (`backend/glossa_lab/api/dashboard.py`) gains an additive
  lane-2 `by_stage` distribution plus `n_unstamped_stage` (287 at
  this phase, honestly unstamped until Phase D), distinct from
  `by_confidence`.

**A5 — Risk flag.** `claim_stage.compute_verified_unexplained`
implements FR-029-03 exactly: true when the lane-1 state includes a
SUPPORTED-class verdict/status (`supported`, `strongly_supported`,
`partially_supported`, or a `SUPPORTED` verdict) **or** a high AEE
score band, while the stage is below `explained` (an unstamped
stage is below `explained` — no evidence of having reached it).
Exposed on all A4 surfaces and filterable via
`GET /claims?verified_unexplained=true`. Tests cover the audit's
flagged shapes: the 8 supported-class extracted-claim records (the
audit's extracted-claim flags) all fire; with scores in hand the
audit's `partially_falsified` / band-`high` record also fires under
the rule's high-band disjunct (9 flagged on the scored surface; the
status-only surface flags the 8). A confidence tier alone never
fires the flag — an anchor's HIGH tier is not a lane-1 verdict or
band, and the audit's 94 strict-set anchor flags are Phase D
ledger-stamped state, not something Phase A recomputes from tiers.

## Tests

`backend/tests/test_spec029_phase_a.py` (31 tests) plus the A2
fixture above: shape/default tests, distinct-object mapping tests,
the byte-identical score regression, transition legality tests with
the plan §2.4 discriminating control (automated actor →
`explained` must fail), named-human / process-name controls,
demotion-reason control, and risk-flag shape tests including the
current-claim-set audit reconciliation. Targeted run (Phase A +
`test_aee_core.py` + `test_indus_evidence_api.py`): all passing.

## Phase gate evidence (A6)

- **Foundation check** (`backend/scripts/foundation_check.py`, the
  backend's own entry point; run with the gitignored Holdat corpus
  CSVs present in the worktree): **40 passed / 0 failed /
  8 warnings** — identical to the pre-change baseline measured the
  same day (40 OK / 0 fail / 8 warn, "READY WITH CAVEATS"); no new
  warnings.
- **Full backend suite** (`pytest backend/tests`, CI's GPU-only
  files excluded as in CI): **2112 passed, 5 skipped, 0 failed**
  (28m09s, local venv, Python 3.12, AEE 1.0.4).
- **Lint**: ruff clean on every authored/edited Python file.
- **Branding sweep**: no other-company or other-program names in
  any authored file (grep over the new module, tests, fixture, and
  this record).
- **Frozen bytes**: nothing under `specs/029-tao-claim-lifecycle/`
  that is digest-covered was edited; this record is a new file in
  that directory, as the phase instructions allow. (Running the
  backend test suite regenerates extraction timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a pre-existing
  side effect; those files were restored byte-identical before
  commit and are not part of this phase's diff.)
- **CI**: verified from the check runs' own conclusions.
  First CI run on head `f2d3e44b` (run 38265919153): 6 of 7 checks
  succeeded; **Backend tests (pytest) failed** on this phase's
  anchor-surface test — in CI the signs index also holds
  anchor-set entries, which then carried no `stage` key (the local
  data dir had none, so the defect was invisible locally). Fixed
  within phase scope: `_build_sign_entry` now serializes the
  unstamped stage object for every entry source, and the test
  checks a full page and no longer assumes the tier set.
  Re-verified locally against a fresh data dir (86 targeted tests
  passing, including the anchor-sets suite that seeds those
  entries). Second CI run on the fixed code head `3ef6d225`
  (run 38270045482): **all 7 checks completed / success** —
  Backend tests (pytest), Frontend tests (Playwright), Evidence
  Graph script smoke tests, Indus public validation checks, and
  Shell wrappers (ubuntu / macos / windows). This record-filling
  commit touches no code; its own CI run was likewise verified
  all-green before the merge.
- **Merge**: PR #169 (`impl/029-phase-a-stage-core` → main),
  merge method `merge`, merged after the all-green CI above was
  verified from the check runs' own conclusions. This record
  ships inside that PR, so it cannot contain the PR's own merge
  sha; the merge sha is named in the delivering report and is
  verifiable as the head of main after the merge.

## Deviations and honest limitations

- **Gate records above `checked` are Phase B, by design.** Plan
  §2.1 also names the FR-029-06/07 gate records as validated on
  transitions above `checked`; those record types are built in
  Phase B (tasks B3/B4). Phase A's service enforces the A3 rules
  (legality, actor, reason, evidence trail) and fails closed on
  each; it does not yet check explanation/digestion records.
- **Anchor risk flags.** Phase A computes `verified_unexplained`
  for anchors only from lane-1 verdict/band fields a record itself
  carries (currently none), so all anchors serialize `false` here.
  The audit's 94 strict-set anchor flags derive from the Phase-108/
  109 strict rule and the frozen ledger; Phase D stamps them.
- **`GET /claims` `stage` key.** On this endpoint the serialized
  stage object replaces the record's flat `stage` value in the
  response (the flat provenance fields remain available inside the
  object); stored records are untouched. No existing consumer read
  a `stage` key on this endpoint (records carried none).

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
