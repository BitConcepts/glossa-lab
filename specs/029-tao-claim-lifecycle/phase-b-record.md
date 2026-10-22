# Spec 029 — Phase B Record: Bundles, Attribution, Explanation, Digestion

> Phase B of `tasks.md` (FR-029-04…07; claims F029-C03, F029-C04,
> F029-C05, F029-C11, F029-C12; OD-2, OD-3, OD-5; plan §2.1
> Workstream 1 gates, §2.4 controls). Base: main `92e8f392`
> (Phase I merged as PR #180; the aee pin of PR #181 is in this
> history and is untouched). Branch:
> `impl/029-phase-b-bundles`. Date: 2026-10-12.
>
> Where the phase instructions' summary and `tasks.md` differed,
> `tasks.md` governed (recorded under Deviations).

## What was built, and where

All machinery is in one new module,
`backend/glossa_lab/claim_bundle.py`, plus one additive guard in
`backend/glossa_lab/claim_stage.py`. Tests:
`backend/tests/test_spec029_phase_b.py` (60 tests, all synthetic
fixtures — invented names, example.org references, a hash of a
synthetic artifact string).

**B1 — Bundle representation.** A bundle is a parent record
carrying `sub_claims`: exactly the four governed kinds —
`reading_soundness`, `scholarship_accounting`, `attribution`,
`explanation_intelligibility` — each once (a missing, duplicated,
or unknown kind is refused). Each sub-claim is a first-class
record (`make_subclaim`): its own evidence list, its own
falsification condition (required, non-empty), its own
proposition, and its own stage carried by the Phase A stage shape
and moved only by the Phase A transition service — there is no
parallel stage system. The parent's stage is **computed**
(`compute_parent_stage` / `compute_parent_stage_detail`): the
minimum of the sub-claim stages (F029-C11), then the caps below.
An unstamped sub-claim makes the parent honestly unstamped.
`sync_parent_stage` is the computation's only writer: it stores
`stage` with `stage_source` =
`bundle-minimum-computation:spec029-phase-b-v1` and `stage_as_of`
together (plan §0 cache), exposes the workings on the record as
`stage_computation`, and appends a dated history entry whenever
the computed stage changes, so a decomposition- or cap-driven
demotion is a recorded event, not a silent edit. The parent stage
is **never directly assignable**: the Phase A
`transition_stage` now refuses any record carrying `sub_claims`
(an additive guard — no Phase A record shape carries that key, so
no Phase A behaviour changes; Phase A's suite passes unchanged),
and the Phase B gate layer refuses a bundle parent the same way.
Lane-1 fields are untouched: a test asserts a bundle parent's
`claim_status` / `confidence` pass through unchanged, and the
Phase A byte-identical score-propagation regression still passes
— bundle machinery never reads or writes an AEE score.

**B2 — Attribution template + OD-3 cap.** The attribution
sub-claim (`make_attribution_subclaim`,
`validate_attribution_subclaim`) carries the FR-029-05 template:
`prior_readings`, each with a resolvable citation (a URI or a
DOI — a bare title is not resolvable); a completeness basis,
`search_record` (corpora searched, literature searched, date,
named-human searcher); and a `contest_state` in
{`unexamined`, `uncontested`, `contested`}. For
`uncontested`/`contested` the template must be complete;
`contested` additionally requires a `contest_record` (who
contests, on what resolvable evidence, when; a resolution, when
present, must itself be a durable adjudication record —
resolvable `adjudication_ref`, date, named-human resolver).
**Contested** is mechanical (`attribution_is_contested`):
state `contested` and no valid resolution. It caps the parent
at `checked` **inside the parent-stage computation** — not in a
display layer. **Unexamined** (the default state: template
incomplete, accounting not yet assessed) is not contested and
carries no cap; the bundle minimum rule alone applies. A valid
durable resolution lifts the cap; a stored resolution whose
reference does not resolve fails closed — the cap stays.
`serialize_bundle` carries the contest with the parent
(`attribution_contested`, the full `contest_record`, the
adverse state), so any surface rendering the parent from this
serialization renders the contest with it (FR-029-05 display
half; the E2 frontend rendering is a later phase).

**B3 — Explanation record (gate for `accepted`).**
`validate_explanation_record` requires: `author` — **one**
named accountable human (a list is refused; AI-system names —
including the house's own agent names — and process names are
refused via an AI/process token check layered on the Phase A
named-human rule); an optional `drafter` field, where an AI
system may be recorded — drafting is permitted, being the named
human is not (OD-2); `artifact_uri` (resolvable); the artifact's
stored SHA-256 `content_hash` (format-validated);
`challenge_venue`; and a non-empty
`ai_assistance_disclosure` field (constitution §VI). The gate
layer (below) refuses an `accepted` transition without a valid
record and writes nothing.

**B4 — Digestion record (gate for `digested`) + adverse
digestion.** `validate_digestion_record` requires one of the
three OD-5 classes — `independent_reuse`,
`published_challenge_answered`, `mechanism_engaging_citation` —
with class-specific resolvable references (a reuse reference;
both the challenge reference and a durable response reference;
for a mechanism-engaging citation, a named intake reviewer with
a stored rationale). Every class requires
`independent_scholar` (a named human) and the
program-independence fields `scholar_is_claim_author` /
`scholar_is_program_staff`, each explicitly `False` — a missing
field fails closed, and the scholar is cross-checked against
any claim-author / program-staff lists supplied to the gate
(falling back to lists the record itself carries). The
`digested` gate additionally re-validates the explanation
record the `accepted` gate required. **Adverse digestion**
(`make_adverse_digestion_record`, `record_adverse_digestion`,
`answer_adverse_digestion`): an unanswered substantive
refutation (named human refuter, resolvable reference) flags
the record `contested`, blocks any advance above `checked` at
the gate layer, and pulls the record back to at most `checked`
— for a plain claim by a recorded demotion transition through
the Phase A service (named-human actor, reason naming the
refutation), for a bundle parent by the computation's adverse
cap via `sync_parent_stage`. Answering it in a durable record
clears the adverse flag and the block; for a bundle parent the
stage is then recomputed from the sub-claims, while a plain
claim re-advances through the gates step by step (a demotion is
not silently undone).

**The gate layer.** `gated_transition_stage` is the Phase B
transition path: it validates the gate records for the target
stage (explanation for `accepted`, digestion + persisting
explanation for `digested`, no unanswered refutation for any
advance above `checked`, no direct transitions at all on a
bundle parent), then delegates the write to the Phase A
transition service, which remains the single writer. All
validation runs on a trial copy and the record is committed
only on success — a refused transition writes nothing, and a
gate record supplied with a refused transition is not stored.

## B5 — Discriminating controls

Each gate is paired with a must-fail control whose positive
twin passes, in `test_spec029_phase_b.py`. Every control was
observed failing for its named defect during development (the
first local run caught five real defects in the new module —
an AI-name token gap and a resolution-validation gap — which
were fixed in scope; the controls are differential, not
ceremonial):

| Gate | Positive control | Negative controls (each must fail) |
|---|---|---|
| Actor rule (Phase A, via gate layer) | named human → `explained` passes | automated actor → `explained`; human name with `actor_kind="automated"` |
| Parent computation (B1) | minimum of sub-claim stages stored as the computation's cache | direct assignment via `transition_stage` and via the gate layer (both refused, record unchanged); bundle missing / duplicating / inventing a sub-claim kind; sub-claim with no falsifier |
| OD-3 cap (B2) | uncontested bundle at sub-claim minimum `explained` computes to `explained`; resolved contest lifts the cap back to `explained` | contested bundle with all sub-claims stamped `digested` still computes and renders at `checked`; unresolvable stored resolution keeps the cap |
| Unexamined ≠ contested (B2) | unexamined attribution, template incomplete, computes to the bundle minimum with no cap | — (the differential is the contested twin above) |
| Explanation gate (B3) | valid record (AI recorded as drafter) → `accepted` passes, record stored | no record; AI as named human (three AI-name shapes); process name; missing author; a list of authors; missing / unresolvable artifact URI; missing / malformed content hash; missing challenge venue; missing disclosure — record byte-identical after each refusal |
| Digestion gate (B4) | each of the three OD-5 classes → `digested` passes | no record; scholar flagged claim-author or program-staff; scholar cross-checked as a claim author; AI as scholar; missing independence fields; empty / unresolvable references; class-specific defects (no reuse ref, no response ref, no intake reviewer, reviewer a process name, no rationale); explanation record tampered after `accepted` |
| Adverse digestion (B4) | answered refutation lifts the block; advance resumes | unanswered refutation: advance above `checked` refused; plain claim pulled `accepted` → `checked` with a recorded demotion; bundle parent pulled to `checked` and rendered contested |

## Phase gate evidence (B6)

- **Foundation check** (`backend/scripts/foundation_check.py`,
  run with the gitignored Holdat corpus CSVs present in the
  worktree, as in prior phases, never committed): **40 passed /
  0 failed / 8 warnings** — identical to the pre-Phase-A
  baseline; no new warnings.
- **Targeted suites** (canonical venv, aee 1.0.4): Phase B 60
  passed; Phase A + B together 91 passed; the neighbouring
  Spec 029 suites (A, D, H, I, freeze) plus `test_aee_core.py`
  and `test_indus_evidence_api.py` together: **190 passed,
  0 failed**.
- **Full backend suite** (CI-parity venv, aee 1.4.0; the
  CI-identical invocation from `.github/workflows/ci.yml`:
  `python -m pytest tests/ --tb=short -q
  --ignore=tests/test_pipelines_gpu.py
  --ignore=tests/test_install_gpu.py` in `backend/`):
  **1316 passed, 6 skipped, 0 failed** in 7m53s — the
  merged-main baseline of 1256 passed / 6 skipped / 0 failed
  plus exactly this phase's 60 new tests.
- **Lint**: ruff clean on every authored/edited Python file.
- **Branding sweep**: no other-company or other-program names
  in any authored file; the synthetic fixture persons are
  invented and named as fixtures; no external scholar is named
  in any authored file.
- **Frozen bytes**: `tasks.md` / `plan.md` / `spec.md` /
  `claims.json` and every other digest-covered file are
  unedited; the aee pin (`>=1.0.4,<1.5`) is untouched; the
  anchors file, the PRED register, and every live claim record
  are untouched — this phase stamps nothing live. Test runs
  regenerate timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a
  pre-existing side effect; those files are restored to
  committed bytes before every commit.
- **CI / merge**: verified from the check runs' own
  conclusions — all 7 checks green on the PR's final head
  before the merge (merge method `merge`); the new main head
  verified via the GitHub API after the merge. This record
  ships inside that PR, so it cannot contain the PR's own
  merge sha; the merge sha is named in the delivering report
  and is verifiable as the head of main after the merge.

## Deviations and honest limitations

- **Summary-vs-frozen-text deviations (tasks.md governed).**
  The phase instructions' summary described the sub-claim
  decomposition in Tao's generic five-part form and named the
  explanation record "the gate for stage `explained`". The
  frozen texts govern otherwise, and this phase follows them:
  the sub-claim kinds are the four of tasks B1 / FR-029-04
  (`reading_soundness`, `scholarship_accounting`,
  `attribution`, `explanation_intelligibility`), and the
  explanation record gates **`accepted`** (tasks B3, spec
  FR-029-06, claim F029-C04: "Acceptance of a claim requires a
  filed explanation record"; the `explained` transition remains
  governed by the Phase A rules — named human plus an evidence
  trail). No governed claim is weakened by this reading: C04's
  falsifier is a claim at `accepted` with no explanation
  record, which the gate makes impossible through the
  transition path.
- **Phase A additive change.** `claim_stage.transition_stage`
  gained exactly one guard (bundle parents refuse direct
  assignment, above) and a docstring note. No Phase A rule,
  signature, or behaviour for any pre-existing record shape
  changed; the Phase A suite passes unmodified.
- **Resolvability is mechanical.** A citation counts as
  resolvable when it carries a URI scheme or is a DOI. This
  checks the *form* of a reference, not that the target exists
  or says what the record claims — that judgment is lane-2
  human work at the gates, exactly as the completeness basis
  itself is a claim with its own falsifier.
- **No live record is a bundle yet.** Decomposition of live
  anchors/claims into bundles, and any real explanation or
  digestion record, are lane-2 human work for later phases;
  this phase builds and tests the machinery on synthetic
  fixtures only, per its hard limit. Display of the contest on
  the frontend surfaces is Phase E2's work; this phase
  supplies the serialized form that carries it.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
