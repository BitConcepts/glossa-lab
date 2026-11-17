# Spec 094 — Stage 2 record (the promotion evidence standard)

**Stage:** 2 — The promotion evidence standard (C094-4..5)
**Date:** 2026-11-16
**Base:** `33484575013b11e60590f1cd8087224b87769084` (origin/main, the
Spec 094 Stage 1 merge, PR #573)
**Branch:** `spec/094-s2-evidence-standard`
**Tasks discharged:** T201, T202.
**Claims discharged:** C094-4, C094-5 (on the evidence named per
claim below).

Nothing in this stage touched the live backend or its stores: all
work ran in a fresh clone on the mini-server against synthetic
fixtures, the research loop was never run, and no live store was
read or written (C094-13 held throughout).

## What was built

### T201 — Evidence pinning (C094-4)

- New module `backend/glossa_lab/evidence_standard.py` carries the
  standard. `pin_evidence(record, artifact_bytes, *,
  evidence_class, pinned_by, pinned_at=None)` is the pin-time act:
  it computes the artifact's SHA-256 and returns a new record dict
  carrying `evidence_sha256`, `evidence_class` (normalized),
  `evidence_pinned_at`, and `evidence_pinned_by`. The input record
  is not mutated, and a refusal raises `EvidenceStandardError` and
  records nothing.
- The candidate record's evidence fields are first-class:
  `CANDIDATE_EVIDENCE_FIELDS = ("evidence_sha256", "evidence_class",
  "evidence_pinned_at", "evidence_pinned_by")`, carried by the
  pipeline's staging write (`pipelines/research_loop.py::
  _save_staging`, `setdefault`, beside Stage 1's gate fields) —
  they start empty, and a record carrying no pin or class cannot
  promote until adjudication records them. Pre-existing records are
  not rewritten (C094-12).
- Promotion verifies the pin: `promote_to_anchors` resolves the
  recorded `evidence_ref` to its artifact (the resolution leg of
  `_evidence_ref_resolves`, now factored as
  `_evidence_artifact_path` with unchanged behaviour), reads its
  bytes, and `evidence_pin_refusal` refuses on absence of a pin, a
  malformed pin, an unreadable artifact, or a byte mismatch.
  Refused signs are reported in the new `blocked_evidence_pin`
  response field; nothing is written for them.
- A pin created by the promote request itself refuses, by the same
  construction as the recorded-ref rule: the promote body may carry
  an `evidence_pins` map, but it is never a source of a pin. An
  entry that differs from the recorded pin refuses the sign — and
  when the record carries no pin, any request-supplied pin differs
  by definition, which is exactly the request-created shape. An
  entry identical to the recorded pin is a no-op echo.
- A promoted anchor's `basis` now records the pin and class the
  promotion verified (`evidence_sha256=…`, `evidence_class=…`)
  beside the existing `evidence_ref=…`.

### T202 — Registered evidence classes (C094-5)

- The admissible-class list lands as a registered artifact:
  `REGISTERED_EVIDENCE_CLASSES` in
  `backend/glossa_lab/evidence_standard.py` — a code-resident
  registry in the repo, amended only by a recorded act (a change to
  that module landed through review), never by configuration,
  environment, or request data. Its initial contents are the four
  classes C094-5 names, each with its grounding recorded in the
  registry itself:
  - `external_corpus_record` — a record in a corpus external to
    this program's research loop and anchor path (a published
    corpus entry, a corpus snapshot record).
  - `published_concordance_entry` — an entry in a published
    concordance (a sign-list or catalogue concordance in print or
    in a published digital edition).
  - `independent_expert_record` — a record authored by an expert
    independent of this program (correspondence, a review, a
    published assessment).
  - `adjudicated_claim_dossier` — the dossier of an adjudicated
    claim in the program's own claims ledger: a claim carried
    through the lifecycle to a recorded verdict with its evidence
    trail. The ledger's adjudication record, not loop output about
    the candidate.
- The loop cannot evidence itself, enforced at three points:
  (a) `class_registration_refusal` is the guard every registration
  must pass — a class name whose normalized tokens name the
  machinery's own product (loop, pipeline, staging, archive,
  run, synthesis, self-referential, anchor-path, internal,
  generated output) is refused registration outright, and the test
  battery proves every registered entry passes the guard;
  (b) `pin_evidence` refuses a self-referential or unregistered
  class at pin time; (c) `evidence_class_refusal` at promotion
  refuses a recorded class that is loop output about the candidate
  even if one were ever written onto a record or into the list,
  and refuses any class absent from the registered list. Refused
  signs are reported in the new `blocked_evidence_class` response
  field.
- Pinning is an adjudication act: `pin_evidence` requires the
  pinner to validate as a named human on the D-094-1 approvers list
  under the `claim_stage` actor rules (`is_listed_approver`,
  reused, not redefined), so an automated identity cannot pin its
  own output as evidence.

### Entry note (plan, Stage 2)

The plan's entry note asks the stage record to name which of the
bug lane's two halves were already landed: **both**. The
corpus-membership precondition (defect 3) and the request-ref
refusal (defect 2's bug-shaped half) are present in the base tree
(`promote_to_anchors`' membership gate and `blocked_evidence_mismatch`
rule, covered by `test_promotion_integrity.py`); this stage builds
the standard itself on top of them and changes neither.

## Design choices taken inside the adopted decisions

1. **Gate placement.** The evidence-standard checks run after the
   approval gate, extending Stage 1's placement discipline (its
   record, design choice 3): membership, then the H26 evidence
   gate, then the approval gate, then pin, then class. Each blocked
   list keeps its established meaning, and `blocked_evidence_pin` /
   `blocked_evidence_class` name exactly the records that passed
   every earlier gate and failed this one. Within the standard, the
   pin check precedes the class check (C094-4 before C094-5: bytes
   first, admissibility second).
2. **The registered list's home.** D-094-2 fixes the list as "a
   registered list … amendable only by a recorded act" without
   naming its home. It lives as a module-level registry in
   `evidence_standard.py`, beside the gate that reads it — the same
   placement pattern D-094-1's approvers list took in Stage 1
   (code-resident, review-gated, no configuration surface). A
   configuration file would be a registration route the claim
   forbids; there is none.
3. **No pin route was added.** Stage 1 set the pattern: gate inputs
   are recorded by adjudication, and no endpoint exists whose
   request supplies them. `pin_evidence` is the pin-time act as a
   library function over a record and the artifact's bytes; wiring
   an adjudication surface that calls it is operations work, not a
   gate. The promote endpoint is the only gate surface, and it
   reads the record alone.
4. **Stage 1's field tuple is untouched.** `CANDIDATE_GATE_FIELDS`
   keeps its exact Stage 1 shape (a Stage 1 test pins it); the
   evidence fields are a sibling constant,
   `CANDIDATE_EVIDENCE_FIELDS`, in the module that owns the
   standard.
5. **Class-name normalization** reuses the actor rules' shape
   (case-folded, spaces/hyphens folded to underscores), so a class
   recorded as "External Corpus Record" matches the registered
   `external_corpus_record`.

## Test actuals

New battery: `backend/tests/test_spec094_stage2_evidence_standard.py`
(19 tests) — the registered list's exact contents and grounding;
the registration guard (seven loop-output class shapes refused,
incl. the probe's own `self_referential_loop_output`); class-name
normalization; `pin_evidence` (pin/class/provenance recorded, input
not mutated; unregistered and self-referential classes refused;
automated and unlisted pinners refused); the pin/class refusal
units; the staging write carrying all four evidence fields; and
probe (b) at promotion in its variants — existing-file ref without
a pin refuses, a request-created pin (the correct hash, supplied
only in the request) refuses, a conflicting request pin refuses, an
echoed request pin is a no-op, a byte-mismatched pin refuses, a
malformed pin refuses, a self-referential class refuses, an
unregistered class refuses, a missing class refuses, a
registered-class pinned artifact promotes with the pin and class
in the anchor's basis, and a mixed batch partitions.

Targeted run (the new battery plus the Stage 1 battery and the
three pre-existing integrity batteries), CI invocation and
environment, local: **57 passed** (19 new + 15 Stage 1 + 11
promotion-integrity + 5 promotion-evidence + 7 staging-action).

Full backend suite, CI invocation (GPU files ignored) with the one
local deselect noted in Deviations — completed locally in two
parts split at the slow Spec 086 gate file (see Deviations):

- Part 1 (the whole suite except `test_spec086_ledger_gate.py`):
  **2,789 passed, 64 skipped, 1 deselected, 0 failed** (196.53s,
  exit 0).
- Part 2 (`test_spec086_ledger_gate.py` alone, same invocation and
  environment): **23 passed, 44 skipped, 0 failed** (33.25s,
  exit 0).

Union: 2,921 tests collected across the two parts — 2,812 passed,
108 skipped, 1 deselected, 0 failed. The union is complete: every
collected test ran in exactly one part.

Ruff on all changed files: clean.

## Existing-test fixture updates (named, per the stage's effect)

The standard changes what a conforming candidate record is, so
three pre-existing fixtures were updated to the conforming shape —
the artifact their `evidence_ref` names (repo-root `LEDGER.md`)
pinned by its actual SHA-256 (computed from the file's bytes at
fixture time, never a hardcoded digest) and the registered class
`external_corpus_record`. No assertion in them was weakened and
their defect coverage is unchanged:

- `tests/test_promotion_integrity.py` — `_candidate()` gains
  `evidence_sha256` / `evidence_class` (its refusal tests still
  refuse on their own earlier gates: skip, membership, mismatch).
- `tests/test_staging_promotion_evidence.py` — `_candidate()` gains
  both fields, so the H26 evidence gate remains the deciding gate
  in its no-ref and request-ref tests.
- `tests/test_spec094_stage1_approval_gate.py` — `_gated()` gains
  both fields, so the Stage 1 promote tests exercise the approval
  gate as their deciding gate exactly as before.

## Ledger gate (this tree, before push)

- `tools/ledger/check_ledger_gate.py --all`:
  `summary: 29 PASS / 0 FAIL / 1 NOT-RUN` — `RESULT: PASS`
- `tools/ledger/check_ledger_gate.py --regen`:
  `summary: 32 PASS / 0 FAIL / 0 NOT-RUN` — `RESULT: PASS`

Both hold the standing profile exactly. In-tree regenerations from
the gate and suite runs were restored before committing; the
committed tree carries only this stage's changes. (Local gate runs
are recorded here as stage evidence; no CI claim is made from
them — the PR's CI read is the parent's gate.)

## Claims discharged

- **C094-4** — promotion evidence is a pinned artifact: the pin is
  recorded on the record at pin time by `pin_evidence`; promotion
  verifies the artifact's bytes against it and refuses on absence,
  mismatch, or a pin created by the promote request itself —
  proven by probe (b)'s no-pin and request-created-pin variants,
  the mismatch and malformed-pin refusals, and the promoting
  pinned artifact.
- **C094-5** — evidence must be of a registered class, and the loop
  cannot evidence itself: the registered list is landed with its
  four ratified classes and groundings; a self-referential class
  refuses at registration, at pin time, and at promotion; an
  unregistered class refuses; a registered-class pinned artifact
  promotes on the record.

## Deviations

- The full local suite deselects
  `tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  by its plain nodeid, per the standing local-run discipline for
  that environment-sensitive test; CI is authoritative for it. No
  CI claim is made from any local run in this record.
- The local full-suite evidence was gathered in two parts, split
  at `tests/test_spec086_ledger_gate.py` (whose tests re-run the
  ledger gate machinery against the real tree and crawl on this
  box). Unlike Stage 1's split, both parts here ran to completion
  as separate invocations with identical environment and exit 0;
  the union covers all 2,921 collected tests.
- The detached suite run's launching ssh session dropped once
  (the known tunnel-proxy broken-pipe); the detached job on the
  box was unaffected, and every result above was read from the
  run's own log files on the box.
- No other deviations. Scope held to T201 + T202 exactly: no
  Stage 3–5 work, no change to `_run_anchor_lifecycle`, no
  live-store access, no loop run.
