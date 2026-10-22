# Spec 029 — Phase C Record: Priority Register and Trails

> Phase C of `tasks.md` (FR-029-11, FR-029-12; claims
> F029-C08, F029-C09; OD-6; plan §2.1 Priority register +
> Trails). Base: main `411386a6` (Phase B merged as
> PR #182; the aee pin of PR #181 is in this history and is
> untouched). Branch: `impl/029-phase-c-priority`.
> Date: 2026-10-12.
>
> Where the phase instructions' summary and `tasks.md`
> differed, `tasks.md` governed (recorded under Deviations).

## What was built, and where

Two new modules plus additive endpoints on the existing
claims router (`backend/glossa_lab/api/indus_evidence.py`,
mounted at `/api/v1/indus-evidence`). Tests:
`backend/tests/test_spec029_phase_c.py` (36 tests, all
synthetic fixtures — invented claimants marked SYNTHETIC,
example.org references, synthetic readings; no real priority
claim is filed by this phase, per its hard limit).

**C1 — Priority register store + intake**
(`backend/glossa_lab/priority_register.py`). A register in
which a claimant files a reading's priority at intake:

- **Issuance on record completeness alone** (task C1):
  intake requires exactly a claimant public identity, a
  claimant contact, a non-empty reading, and a non-empty
  evidence list. Nothing else is required, and **no score,
  stage, or verdict field exists on an entry** — in the
  stored record or in any serialization (tested by key
  absence over the stored record, the serialized entry, and
  the public record). Assessment-shaped payload fields are
  ignored, never stored.
- **Public record (OD-6).** `public_record(entry)` is
  exactly three fields: `claimant` (the public identity the
  claimant declares for publication), `timestamp` (the
  **server** timestamp — stamped by the register from its
  clock at intake; a claimant-asserted timestamp in the
  payload is never read, tested), and `content_hash`
  (SHA-256 of the reading, below). It is published at
  intake. The claimant's contact is stored only on the
  internal record, for correspondence (plan §5/§V, rule
  H24), and appears in **no** serialization.
- **Canonicalization** (`spec029-priority-canonical-v1`,
  defined in the module and here): the claim content is the
  mapping `{"reading": <reading>, "evidence": [<evidence>,
  ...]}` serialized as JSON with sorted keys, separators
  `(",", ":")`, `ensure_ascii=False`, encoded UTF-8, and
  hashed with SHA-256. There is deliberately **no**
  case-folding, whitespace, or punctuation normalisation
  (contrast the Phase I proposition fingerprint, whose job
  is collision): priority binds the exact content filed,
  so a one-byte difference — in the reading, in any
  evidence item, even a trailing space — produces a
  different hash (tested in both directions).
- **Storage form: stored sealed** (plan §2.1: "the
  reading's content is stored sealed" — see Deviations for
  how the frozen texts decided this over hash-only). The
  canonical content bytes are stored only as a sealed
  envelope: an HMAC-SHA256 counter-mode keystream XOR with
  an HMAC integrity tag, stdlib only (no new dependency).
  The seal key is not part of any register record: in the
  API store it lives in a separate file (mode 0600) beside
  the store file under the gitignored runtime directory
  `.glossa-state/`, and is never serialized. The store
  file at rest contains no plaintext content (tested). A
  tampered envelope, or one opened under a wrong key,
  fails closed (tested), and content opened from an
  envelope is re-verified against the published hash
  before it is revealed.
- **Verification function.** `verify_content(entry,
  reading, evidence)` recomputes the canonical hash and
  compares it to the published hash in constant time;
  matching content verifies, one-byte-different content
  does not (tested).

**C2 — Unseal rules (OD-6).** An entry is `sealed` until
one of two dated, recorded triggers:

- **(a) Claimant publication:** `unseal_by_publication`
  accepts content the claimant presents only when its
  canonical hash matches the published hash; the
  presentation is recorded as a dated `unsealed` history
  event carrying the presented hash. A mismatched
  presentation is **refused and recorded** (a dated
  `unseal_refused` event naming the presented hash); the
  entry stays sealed (both directions tested).
- **(b) Reveal date:** `unseal_due(now)` unseals every
  sealed entry whose reveal date has been reached, opening
  its sealed envelope (integrity- and hash-checked) and
  recording a dated `unsealed` event with trigger
  `reveal_date`. Reading the register through the API
  applies this trigger. The reveal date is
  claimant-chosen at intake, or the **default of
  24 months** from the server timestamp when none is
  chosen (calendar month arithmetic, day-clamped; tested
  at the default date and at a chosen date, sealed the
  day before in both cases). It must lie after intake.
- **Extension: once only.** `extend_reveal_date` moves the
  reveal later and records a dated `reveal_extended`
  event (previous and new dates). A second extension, an
  extension that does not move the reveal later, and an
  extension on an unsealed entry are each **refused and
  recorded** (a dated `extension_refused` event with the
  reason is appended before the error is raised — tested
  for all three).
- **Clock.** Every operation takes the register's
  injectable clock or an explicit `now=`; no test reads
  the wall clock.

**C3 — Integrity.** Entries are append-only: the register
exposes no edit or delete path (tested over the service
surface and the API routes — no PUT/DELETE priority
routes), sealed fields are never rewritten, and every
transition appends a dated event to the entry's `history`
(intake, extension, refused extension, refused unseal,
unseal, supersession). A correction is a **new** entry
whose intake names the entry it `supersedes`; the old
entry gains a dated `superseded` event and its public
record is byte-identical afterwards (tested). **Credit
invariant:** the public record is a function of claimant +
server timestamp + hash only; the credit-invariance test
runs an extension, a refused unseal, and the unseal itself
against an entry while a (separate, synthetic) claim record
is assessed, and the public record never changes.

**C2 (tasks) / trail view — Per-claim inspectable trail**
(`backend/glossa_lab/claim_trail.py`; endpoint
`GET /claims/{claim_id}/trail` on the claims router, which
resolves extracted claims by `claim_id` and anchors by
sign id from the canonical anchors file). One serialized
view per claim assembling what the earlier phases built:

- stage + `stage_history` (Phases A/D) — one trail event
  per history entry, each carrying the record's
  `stage_source` as its **source pointer**, so every
  displayed stage is traceable/recomputable to its
  evidence (the D-E invariant);
- verdicts: the record's lane-1 status serialized
  FR-029-12-style alongside the transitions — evidence
  refs (each as `{ref, origin_group, kind}`), the
  **falsifier state at decision time**, actor, and
  timestamp. Where an extraction-era verdict records no
  actor, the trail states `actor_recorded: False` and the
  trail's `completeness` block names `actor` as missing —
  gaps are visible, never filled by invention;
- bundle decomposition + gate records (Phase B) when the
  claim is a bundle: the bundle serialization (sub-claims,
  parent-stage computation, contest travelling with the
  parent) plus any explanation / digestion /
  adverse-digestion records the claim carries;
- anchor annotation (Phase H) when present:
  `validation_status`, the computed `strict_set` flag, and
  the strict-set rule read from the anchors file's own
  metadata as the recomputation pointer;
- sources / evidence instances (Phase I): preserved
  evidence instances with their origin groups, and the
  origin-group discipline — groups are the **distinct**
  `source_document_id`s (a merged proposition counts its
  origin group once, not once per instance);
- priority-register entries filed against the claim
  (Phase C), serialized through the register module, so a
  sealed entry's content cannot leak through the trail
  (tested: sealed marker and contact absent from the
  whole trail JSON; revealed content appears only after
  unseal).

The assembler does not mutate the record it reads
(tested by deep comparison).

**API surface.** On the existing router: `POST
/priority-register` (intake; returns the entry id, the
public record, and the sealed-safe entry view),
`GET /priority-register` (public records + sealed-safe
views; applies the reveal-date trigger), `GET
/priority-register/{entry_id}`, `POST
/priority-register/{entry_id}/extend`, `POST
/priority-register/{entry_id}/unseal`, and `GET
/claims/{claim_id}/trail` (404 for an unknown id). The
register store is runtime state (`.glossa-state/`,
gitignored) — no register record, real or synthetic, is
committed. Refused unseal/extension calls save the store
before returning the error, because the recorded refusal
is part of the register.

## Discriminating controls (C5)

Each rule is paired with a must-fail / must-differ twin in
`test_spec029_phase_c.py`:

| Rule | Positive control | Negative controls (each must fail / differ) |
|---|---|---|
| Hash seal (C1/C3) | filed content verifies; sealed envelope opens to the canonical bytes | one byte changed in reading, in evidence, or a trailing space → different hash, no verification |
| Seal holds (C2) | unseal fires on each trigger | sealed the day before the chosen date and before the default 24-month date; public/listing/trail serializations grep-clean for the sealed content marker and the contact |
| Publication unseal (C2) | matching presented content unseals, presentation recorded | one-byte-different presentation refused, recorded as `unseal_refused`, entry stays sealed (service and API) |
| Extension (C2) | first extension recorded, new date governs | second extension refused + recorded; non-later date refused + recorded; extension after unseal refused + recorded (service and API for the second-extension case) |
| Completeness-only issuance (C1) | complete synthetic record issues with no assessment | each missing required field refused, nothing filed; no score/stage/verdict key on any form of the entry |
| Server timestamp (C3) | timestamp equals the register clock | claimant-asserted 1999 timestamp in the payload ignored |
| Sealed storage (C1) | envelope opens under the register key | tampered ciphertext fails closed; wrong key fails closed; store file at rest contains no plaintext content |
| Append-only (C3) | correction files as a new superseding entry; old public record unchanged | no edit/delete method on the service; no PUT/DELETE priority route in the API |
| Trail completeness (C2 tasks) | full synthetic claim: every stage event carries source pointer, actor, timestamp, falsifier state, grouped evidence refs | missing falsifier renders `absent` and is named in `completeness.missing`; actor-less verdict renders `actor_recorded: False`, never an invented actor |

## Phase gate evidence (C3 in tasks.md — the A6 gate)

- **Foundation check** (`backend/scripts/foundation_check.py`,
  run with the gitignored Holdat corpus CSV present in the
  worktree, as in prior phases, never committed): **40
  passed / 0 failed / 8 warnings** — identical to the
  pre-Phase-A baseline; no new warnings.
- **Targeted suites** (CI-parity venv, aee 1.4.0): Phase C
  36 passed; the neighbouring Spec 029 suites (A, B, C, D,
  H, I, freeze) plus `test_aee_core.py` and
  `test_indus_evidence_api.py` together: **226 passed,
  0 failed**.
- **Full backend suite** (CI-parity venv
  `~/workspace/venvs/glossa-ci-pin`, aee 1.4.0; the
  CI-identical invocation from `.github/workflows/ci.yml`:
  `python -m pytest tests/ --tb=short -q
  --ignore=tests/test_pipelines_gpu.py
  --ignore=tests/test_install_gpu.py` in `backend/`):
  **1352 passed, 6 skipped, 0 failed** — the merged-main
  baseline of 1316 passed / 6 skipped / 0 failed plus
  exactly this phase's 36 new tests.
- **Lint**: ruff clean on every authored/edited Python file.
- **Branding sweep**: no other-company or other-program
  names in any authored file; the synthetic fixture
  persons are invented and named as fixtures; no external
  scholar is named in any authored file.
- **Frozen bytes**: `tasks.md` / `plan.md` / `spec.md` /
  `claims.json` and every other digest-covered file are
  unedited; the aee pin (`>=1.0.4,<1.5`) is untouched; the
  anchors file, the PRED register, and every live claim
  record are untouched — this phase files nothing live.
  Test runs regenerate timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a
  pre-existing side effect; those files are restored to
  committed bytes before every commit.
- **CI / merge**: verified from the check runs' own
  conclusions — all 7 checks green on the PR's final head
  before the merge (merge method `merge`); the new main
  head verified via the GitHub API after the merge. This
  record ships inside that PR, so it cannot contain the
  PR's own merge sha; the merge sha is named in the
  delivering report and is verifiable as the head of main
  after the merge.

## Deviations and honest limitations

- **Storage form decided by the frozen texts (plan over
  the summary's either/or).** The phase instructions'
  summary allowed hash-only storage if the frozen text
  said so. It does not: `plan.md` §2.1 states "the
  reading's content is **stored sealed** and is revealed
  only when the claimant publishes or at a claimant-chosen
  reveal date", and OD-6's reveal-date trigger is only
  meaningful if the register holds the content to reveal.
  This phase therefore stores the content sealed (above)
  **and** implements the hash-verification presentation
  path, so both unseal triggers are real. The summary's
  hash-only branch was not taken, by the frozen text.
- **Sealing is envelope sealing, not a KMS.** The sealed
  envelope (HMAC-SHA256 counter-mode XOR + HMAC tag,
  stdlib only, because `cryptography` is not a declared
  backend dependency and this phase adds none) protects
  the content against reading the register store alone:
  the key is a separate 0600 file, never in the store and
  never serialized. It is not a substitute for managed key
  infrastructure if the register ever holds real filings
  at scale; that hardening is deployment work, recorded
  here rather than silently assumed.
- **Resolvability / identity are not judged.** Intake
  checks completeness of form only — that the declared
  public identity, contact, reading, and evidence are
  present. Whether a claimant is who they declare, and
  whether a presented publication is really theirs, are
  lane-2 human judgments at the desk, exactly as the
  completeness basis is in Phase B. The machinery binds
  content to hash and timestamp; it does not authenticate
  persons.
- **Anchors on the trail endpoint.** Task C2 names a
  per-claim API trail; the endpoint additionally resolves
  anchor sign ids because the Phase H annotation the
  trail must assemble lives on anchors. This is additive:
  unknown ids 404, and no anchor record is written.
- **No live filings, no frontend.** The register is empty
  in production until a real claimant files (claimant /
  owner action, not machinery work). No frontend surface
  is built in this phase; the register and trail are API
  surfaces, as tasks C1/C2 specify.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
