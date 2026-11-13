# Feature Specification: Research-Loop Acceptance Hardening — Gated Approval, Pinned Evidence, Per-Candidate Verification, and Lifecycle Routing on the Anchor Path

**Feature Branch**: `094-research-loop-acceptance-hardening` (build
stages); this package lands on `spec/094-adoption`
**Created**: 2026-11-13
**Status**: RATIFIED AS A BLOCK by the owner, Tristen Pierson,
2026-11-13 (decisions D-094-1..6 adopted as recommended; record:
`records/ratification-2026-11-13.md`).
**Nothing in this package is a result: no gate has been built,
no candidate has been re-evidenced, and the research loop has
not run. No build stage (Stage 0 onward) is started by this
motion. The claims-ledger intake (the C094 bundle's append
through the sanctioned importer, the program-map assignment,
and the generated-layer regeneration) is NOT executed by the
adoption PR; it stands as a separate gated act, recorded as
such in the ratification record.**
**Input**: The owner's commission in the Glossa-Lab chat,
2026-11-13: he ordered the automated research loop fully
tested ("I suspect issues when accepting signs and things"),
then directed the fix route ("Do what you recommend whether
it's a combination or one or the other") — the bug-lane defects
to direct PRs, the policy layer to this spec — and ratified
this package as recommended the same day (option tap plus
typed confirmation).
**Evidence of record**: the acceptance-path test of 2026-11-13
(code survey and adversarial probes on a scratch backend at
main `25bcbe9a`; the live backend was never written to) and
its supplement (the claim-record storage-edit probe, completed
by the parent the same day), counted and read first-hand in
`records/commission-and-grounding-2026-11-13.md`: the staging
and promotion surface (`backend/glossa_lab/api/research_loop.py`
— `staging_action`, `promote_to_anchors`,
`_evidence_ref_resolves`, `_run_anchor_lifecycle`,
`get_staging`); the lifecycle machinery the anchor path never
calls (`backend/glossa_lab/claim_stage.py` —
`transition_stage`, called only from `claim_bundle.py`); the
atomic write path (`backend/glossa_lab/atomic_io.py`) and the
three anchor-path stores it has not reached; the gap register
entry GR-088-05 / GAP-C07 ("THE LIFECYCLE STATE MACHINE IS NOT
STORAGE-ENFORCED").
**Predecessors**: Spec 029 (the claim lifecycle whose
`transition_stage` guarantees this spec routes the anchor path
through), Spec 086 (the one claims ledger and its gate — the
post-hoc divergence net the storage-edit probe measured, and
the net the anchor path has no equivalent of), Spec 089 (the
V9 writer census and run-defs discipline C094-10/C094-11
register into), Spec 092 (the atomic write's verified-write
successor, Stage 2 there; this spec's build stages run after
092's Stage 1 per D-094-4), Spec 091 (whose Stage 1 locator
pass produces exactly the candidate flow these gates are the
precondition for), Spec 093 (the adoption shape this package's
records follow).

## Problem statement

The 2026-11-13 test mapped every route by which a
machine-staged sign reading becomes an approved, verified,
promoted anchor. The unambiguous bugs (defects 3–7) went to
the bug lane as direct PRs. Four findings are policy — the
acceptance path has no gates where the program's own
discipline requires them — and they are this spec's whole
scope:

- **Approval has no gate (test defect 1).** `POST
  /staging/action` with `action:"approve"`
  (`staging_action`) flips any staged candidate to approved.
  The request body carries no actor at all; the candidate
  schema has no falsifier field (the pipeline writes `sign`,
  `proposed_reading`, `evidence_type`, `review_status` — no
  `falsifier` exists anywhere in the loop or its API); there
  is no evidence threshold and no named-human requirement.
  Probe (a): a genuine candidate approved in one call.
- **Promotion's evidence gate accepts any existing file
  (defect 2).** The H26 gate in `promote_to_anchors` requires
  a recorded evidence reference, but `_evidence_ref_resolves`
  passes when the ref's leading token names any existing
  file — and the ref may be supplied in the promote request
  itself. Probe (b): a candidate whose `evidence_type` was
  literally `self_referential_loop_output` promoted to a
  MEDIUM anchor on `evidence_ref=README.md`. The no-ref
  control was refused; the gate holds exactly as far as
  existence, and no further. (The bug-shaped half — a
  request-supplied ref overriding the record — is in the bug
  lane; the standard itself is this spec's Stage 2.)
- **Auto-verification by global signal (defect 8).**
  `_run_anchor_lifecycle` sets a flat `sa_delta = 0.1`
  whenever a loop run's foundation check reports zero
  failures, flips every approved candidate to "verified" on
  that signal alone, and auto-archives them as verified —
  and "verified" promotes at MEDIUM. No per-candidate
  evidence is consulted at any point.
- **The lifecycle machine is never routed through (defect 9;
  GR-088-05 / GAP-C07).** The gap register's entry stands
  verbatim on current main: "THE LIFECYCLE STATE MACHINE IS
  NOT STORAGE-ENFORCED", status UNSTATED, missing piece "the
  cross-cutting spec the gap-record itself calls for". This
  spec is that spec, scoped to the anchor path.
  `claim_stage.transition_stage` is a real fail-closed gate —
  one-step moves, an automated-actor allowlist capped at the
  `checked` rank, a named human plus an evidence trail above
  it — but its only callers are inside `claim_bundle.py`. The
  anchor path (staging, archive, promote) writes
  `review_status` directly on plain JSON files and never
  touches it; promoted anchors are written with no stage
  fields at all.

Plus one code fact established at drafting, beyond the test's
enumeration: the anchor path's three state stores —
`outputs/anchor_staging.json`,
`outputs/anchor_staging_archive.json`,
`backend/reports/INDUS_FINAL_ANCHORS.json` — are written by
direct truncating `Path.write_text` at eight-plus sites in
`api/research_loop.py`, while the platform's atomic write
(`atomic_io.atomic_write_text`: temp file, fsync, atomic
rename, previous file byte-identical on a named failure)
already exists in the same codebase and is used by the
settings and preset stores. The file a truncating write can
zero is, in one case, the anchor record itself.

The live exposure today is bounded and stated plainly: the
loop has never run a cycle on the re-stood-up backend,
staging is empty, and the live anchor file is still exactly
the audited 287. This is exposure that matters the moment
the loop runs, not damage already done — and Spec 091
Stage 1's locator pass is the flow that would run into it.

## Scope — what this spec builds

- **Stage 0 — Grounding completion (no code).** The
  storage-edit probe's verdict is already observed (parent
  addendum, carried in the ratification record); Stage 0
  inventories the live anchor-path stores (staging count;
  archive entries by status, including the pre-gate
  approved/verified count C094-12 and D-094-6 turn on;
  anchors at 287 as read 2026-11-13) and records every number
  and verdict the later stages cite. Its exit gate is the
  probe's re-run against the built shape (Stage 4) plus this
  inventory.
- **Stage 1 — Record schema and the approval gate
  (C094-1..3).** Candidate records gain falsifier, approver,
  and evidence fields as first-class record fields;
  `staging_action`'s approve route enforces the named-human
  rule, reusing the `claim_stage` actor rules — automated
  actors can never approve, verify, or promote.
- **Stage 2 — The promotion evidence standard (C094-4..5).**
  Evidence pinning (SHA-256 recorded at pin time, verified at
  promotion), the registered evidence-class list, and the
  death of request-supplied refs as gate inputs. Loop output
  about a candidate is not a qualifying class.
- **Stage 3 — Verification redefined (C094-6..9).** The
  flat-delta flip is removed from `_run_anchor_lifecycle`;
  verification becomes a per-candidate recorded evaluation;
  MEDIUM binds to it; the fabricated fallback delta
  (`round(score * 0.12, 3)` in `get_staging`) leaves the
  staging surface.
- **Stage 4 — Lifecycle routing and atomic stores
  (C094-10..11).** Every anchor-path status transition routes
  through a single gated transition service carrying
  `transition_stage`'s guarantees; the three stores move to
  the atomic write path; the storage-edit probe re-runs
  against the built shape.
- **Stage 5 — Closeout (C094-12..13).** The full policy probe
  battery re-runs end to end on a scratch instance; the
  GR-088-05 register entry is amended with the path-scoped
  closure (amend, never delete); C094-12's no-diff boundary
  is verified against the adoption-day anchor and ledger
  state; C094-13's protection is lifted by name in the
  closeout record.

## Non-goals (explicit)

- **Re-adjudicating the standing record.** No existing
  anchor's reading or confidence changes; no claim's stage,
  status, or ledger entry changes (C094-12). The pre-gate
  archive stock is inventoried and labelled, never demoted
  or deleted (D-094-6).
- **The bug lane's defects 3–7.** Corpus membership at
  promotion, LOW/CANDIDATE overwrite protection, rejection
  erasure, the approval state guard, and anchor-set pair
  checks are direct PRs in parallel; this spec takes them as
  ratified context its claims may assume and does not re-spec
  them. The anchor-set surface (defect 7) is expressly not
  covered here.
- **GR-088-05 beyond the anchor path.** Storage enforcement
  for the claim stores generally is not closed by this spec;
  the register entry is amended to record exactly the
  path-scoped closure (C094-10).
- **Running the loop.** No research-loop run against the
  live backend is authorized by this spec (C094-13); the
  loop stays off the live stores until closeout lifts the
  bar by name.
- **The two minor findings.** Promote's coverage misreport
  when the corpus CSV is unavailable (its bug-shaped half —
  the fabricated 0.0 — rides the promotion-integrity PR) and
  the MCP staging tool's shape error against the live
  list-shaped staging file are carried visibly in the bug
  lane, not absorbed here.

## Decisions

- **D-094-1 — Who may approve: a named-humans list, initially
  the owner alone — ADOPTED AS RECOMMENDED.** The gate is the
  `claim_stage` rule (a named human validates; a process
  never does). The decision is whose names validate on this
  path. (a) Owner only: simplest, and a bottleneck the
  program will feel the first time an independence leg needs
  a second approver. (b) A recorded named-humans list,
  initially containing only the owner — identical to (a)
  today, and Spec 091's future independence-leg humans join
  by list amendment instead of code change. (c) Any
  authenticated named human: wider than any current need,
  and approval authority by default is how gates quietly stop
  being gates. The list lives wherever Stage 1's record says
  the actor rules already read their allowlist from, or
  beside it — not a new registry.
- **D-094-2 — The promotion evidence standard: pinned
  artifact AND registered class — ADOPTED AS RECOMMENDED.**
  (a) Both halves, as claimed in C094-4 + C094-5. Neither
  half alone closes defect 2: a pin without a class admits a
  hashed README; a class without a pin admits a mutable file
  whose contents drift after the decision. (b) Pin only:
  cheaper, and leaves the self-reference hole open in hashed
  form. (c) Path-exists (the status quo): rejected by the
  probe record. The cost of (a), stated plainly: someone must
  pin and class evidence per candidate, which is real work
  per promotion — that friction is the gate working as
  intended.
- **D-094-3 — Auto-verification: abolish the automatic route
  — ADOPTED AS RECOMMENDED.** (a) Remove the run-level flip
  outright (C094-7) and let "verified" exist only as a
  per-candidate gated act (C094-6). (b) Keep an automatic
  route but feed it per-candidate evidence: the evidence
  would be assembled by the same system the status certifies,
  and a bulk flip with better inputs is still a bulk flip. If
  a future need for automated verification is real, it can
  arrive as its own claim with its own falsifier; it does not
  ride in on this spec. The cost of (a): verification becomes
  a human-paced act, at anchor-path volumes that are small by
  construction.
- **D-094-4 — Staging order: Stage 0 immediately; build
  stages after Spec 092 S1 and before Spec 091 Stage 1 —
  ADOPTED AS RECOMMENDED.** 094 depends on machinery that
  already exists (`claim_stage`, `atomic_io`), so nothing
  technical queues it behind 092. The order is a program
  decision, and the reasoning is: Spec 092 S1 (credential
  encryption) is already next in the adopted queue and is
  untouched by this; Spec 091 Stage 1's locator pass produces
  exactly the candidate flow that must not enter an ungated
  path, so 094's gates are 091's precondition in substance
  even though not in code. Stage 0 (inventory, and the
  probe's re-run staged for Stage 4) is read-and-probe work
  that can run in parallel with 092 S1 without disturbing it.
  The alternative — 094 after 091 Stage 1 — leaves the
  locator pass flowing into the path this test just mapped.
- **D-094-5 — The storage-edit probe as a stage gate —
  ADOPTED AS RECOMMENDED, with its object adjusted by the
  parent addendum.** The package was drafted while the probe
  was an open item; the parent completed it on 2026-11-13
  (verdict in the ratification record: detected by cross-store
  consistency only, no lifecycle validation). The
  recommendation stands in substance but its object changes:
  the probe no longer needs completing; Stage 0's exit gate
  becomes the probe's RE-RUN against the built shape (already
  Stage 4's plan) plus the live store inventory, which
  remains undone and is Stage 0's real remaining work.
- **D-094-6 — Pre-gate archive stock: promotability
  suspended, not grandfathered — ADOPTED AS RECOMMENDED.**
  (a) Entries approved or verified before these gates land
  keep their recorded status as history but cannot promote
  until re-evidenced onto the new record fields (C094-12).
  (b) Grandfather their promotability: the stock is small,
  but every grandfathered promotion is a promotion this
  spec's claims cannot speak for, taken through the exact
  routes the test falsified. Nothing under (a) is deleted,
  demoted, or re-adjudicated; the only suspended thing is
  forward motion. The re-evidencing cost is bounded by Stage
  0's inventory count.

## Requirements (summary; the claims in claims.md are the normative text)

- **R1 (C094-1..3)** — approval is a gated act: a recorded
  falsifier, a named-human approver from the D-094-1 list,
  and every gate input read from the candidate record, never
  from the deciding request; automated actors hold no
  approve/verify/promote authority on this path.
- **R2 (C094-4..5)** — promotion evidence is a
  content-hash-pinned artifact of a registered class,
  verified at promotion time; loop self-output is not a
  class.
- **R3 (C094-6..9)** — verification is per-candidate and
  recorded, the flat-delta mechanism is removed, MEDIUM binds
  to verification under this spec, and no surface presents a
  fabricated SA delta as measured.
- **R4 (C094-10..11)** — every anchor-path transition routes
  through the gated transition service, and the three stores
  are written only through the atomic write path; GR-088-05
  closes for this path, path-scoped, on the register's own
  amend-never-delete discipline.
- **R5 (C094-12..13)** — the boundary held throughout:
  nothing standing is moved or grandfathered, and the loop
  stays off the live stores until closeout discharges the
  claims and lifts the bar by name.

## Bars fixed in the claims (ratified with the package)

- The 2026-11-13 probe battery is the acceptance instrument:
  re-run on the built system at each stage's exit, the policy
  probes must refuse — approval without a falsifier (probe
  a), promotion on an existing-file or self-referential ref
  (probe b), and the lifecycle flip test written for Stage 3.
  A probe that still passes is a stage failure, not a finding
  to note.
- Stage exits are per-claim: each stage's record names the
  claims it discharges and the probe or census that discharged
  them. No claim is discharged by a stage summary.
- GR-088-05's register entry is amended at closeout to record
  the path-scoped closure (amend, never delete, per the
  register's own discipline).

## Governance

- Stages land as separate PRs, parent-gated on per-job CI
  green plus the delivery checker, per the standing seat
  discipline; each stage record cites the runs it relied on
  by the Spec 089 quadruple.
- The claims-ledger intake is a separate gated act, not part
  of the adoption PR: when executed, it appends the C094
  bundle through `tools/ledger/import_bundle.py` only (the
  sanctioned path, never a hand-edit), assigns the spec in
  the program map, regenerates the generated layers, and
  republishes through the gated path — the ledger grows by
  exactly this bundle, and the gate's summaries on the final
  tree are recorded in that act's record.
- No stage's output is approved in advance; each lands on its
  own evidence. A stage that ends with an undischarged claim
  ends as a failure record, not a closeout.
- The research loop stays off the live stores for the whole
  life of this spec until Stage 5's closeout lifts C094-13's
  bar by name; scratch-instance executions for stage evidence
  are the only loop runs contemplated.
