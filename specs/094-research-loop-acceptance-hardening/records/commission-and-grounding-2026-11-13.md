# Spec 094 — Commission and grounding record (2026-11-13)

**Commission.** The owner ordered the automated research loop
fully tested in the Glossa-Lab chat on 2026-11-13 ("Also fully
test the automated research loop. I suspect issues when
accepting signs and things"). The test confirmed the suspicion
(§1). Presented with the findings and the fix-route
recommendation — the unambiguous bugs to direct PRs, the policy
questions to a hardening spec — the owner directed: "Do what
you recommend whether it's a combination or one or the other."
This package was drafted the same day under that direction and
ratified as recommended the same day (ratification record,
`records/ratification-2026-11-13.md`). This record is the
package's grounding: the test method and its counts (§1), the
policy findings (§2), the code facts read at drafting (§3), the
live-state reads (§4), and the storage-edit probe's observed
verdict (§5). No live store was written, and no credential or
claim content was read, at any point in the test or this
drafting. The test's full record is the working file
`~/workspace/glossa-run/loop-test-2026-11-13/REPORT.md` with its
supplement; the probe logs live in that directory's `logs/`.

## 1. The test, as run (2026-11-13)

Code survey and adversarial probes against a scratch backend
instance (own data dir, port 8123, torn down after the run),
built from a fresh clone at main `25bcbe9a`; the live backend
was touched read-only only (§4).

- **Existing tests:** 152 passed / 0 failed across the eight
  acceptance-related modules (test_research_loop 20,
  test_research_loop_deep 15, test_staging_promotion_evidence
  5, test_anchor_sets 12, test_spec029_phase_a 31,
  test_spec029_phase_b 60, test_study_loop 7,
  test_indus_claims_carryover 2). The suite is green — and the
  acceptance path is still largely ungated, because the tests
  test the machinery's operation, not its refusal behaviour.
- **Probes:** 18 API calls recorded. Gates held: 3. Gates
  missing or bypassed: 7. Scratch anchors went 287 → 292
  through the probes. Per-probe verdicts and quoted evidence:
  the test report, defects 1–10.

## 2. The policy findings (this spec's scope)

1. **Approval has no gate (defect 1).** Probe (a): a genuine
   candidate (M400) approved in one `POST /staging/action
   {action:"approve"}` call. No falsifier field exists to
   require, no evidence threshold, no actor.
2. **Promotion's evidence gate checks only that a file exists
   (defect 2).** Probe (b): a candidate with `evidence_type`
   literally `self_referential_loop_output` promoted to a
   MEDIUM anchor (ZZZ901, reading "selfref-ka", score 0.99) on
   `evidence_ref=README.md`, the ref supplied in the promote
   request itself. The no-ref control was refused — the gate
   holds exactly as far as existence.
3. **Auto-verification by global signal (defect 8, code-read,
   not probed).** `_run_anchor_lifecycle` flips approved →
   verified for every approved candidate whenever a loop run's
   foundation check has 0 failures (flat `sa_delta = 0.1`, not
   per-candidate evidence), then auto-archives them as
   verified; verified promotes at MEDIUM.
4. **The lifecycle machine is never routed through (defect 9;
   GR-088-05 / GAP-C07).** The gap register
   (`glossa-indus/map/gap-register.md`) reads on current main:
   "THE LIFECYCLE STATE MACHINE IS NOT STORAGE-ENFORCED",
   status UNSTATED, the cross-cutting spec never written.
   §5's probe refines what that means for the claims ledger;
   for the anchor path there is no equivalent net at all.

The remaining findings are the bug lane's, taken as ratified
context: phantom graphemes promote (defect 3); LOW/CANDIDATE
anchors overwriteable — 116 of 287 (defect 4); rejection
erasable by re-staging (defect 5) and no state guard on
approval (defect 6) — both fixed by PR #563, merged
`b6546239`, the adoption branch's base; anchor sets accept
fabricated "verified" pairs at defaulted "high" confidence
(defect 7) — PR #564 in flight at drafting; defects 3, 4, and
defect 2's bug-shaped half (request-supplied refs) — PR #565
in flight at drafting. Two minor findings ride the bug lane:
promote misreports coverage as 0.0 when the corpus CSV is
unavailable, and the MCP `get_anchor_staging` tool errors
against the live list-shaped staging file (§4).

## 3. Code facts read at drafting (clone at `25bcbe9a`)

- `staging_action` (`backend/glossa_lab/api/research_loop.py`)
  carries no actor in its request body; the pipeline writes
  candidates with `sign`, `proposed_reading`, `evidence_type`,
  `review_status` — no `falsifier` field exists anywhere in the
  loop pipeline or its API.
- `claim_stage.transition_stage` is fail-closed as designed —
  one-step moves, a named human plus evidence above `checked`,
  automated actors capped at `checked` — and its only caller
  is `claim_bundle.gated_transition_stage`. The anchor path
  never touches it: staging, archive, and anchors are plain
  JSON files written directly by endpoints, and promoted
  anchors are written with no stage fields at all.
- The three anchor-path stores (`outputs/anchor_staging.json`,
  `outputs/anchor_staging_archive.json`,
  `backend/reports/INDUS_FINAL_ANCHORS.json`) are written by
  direct truncating `Path.write_text` at 12 counted sites in
  `api/research_loop.py`.
- `atomic_io.atomic_write_text` exists (temp file, fsync,
  atomic rename) with exactly two adopters in the codebase —
  the settings store and the preset store — and provides
  atomicity plus fail-closed naming only: no read-back hash
  verification. The full verified-write contract is Spec 092
  Stage 2, not current platform behaviour; C094-11 is written
  against the atomic path's actual guarantees, with the S2
  successor adopted only if landed by build time.
- `get_staging` substitutes `round(score * 0.12, 3)` as a
  candidate's `sa_delta` when no SA comparison was recorded —
  response-shaping only, not persisted, not one of the tested
  defects. It grounds C094-9 as a drafting observation; Stage 3
  demonstrates the built behaviour rather than assuming it.

## 4. Live state, read-only (2026-11-13)

Via the MCP surface and read-only file census on the
mini-server, after the parent restored the VM tailnet
forwarder and verified the backend by its six-key health
identity: the research loop is not running (0 cycles
completed, 0 candidates, empty history; protocol
`integrated_research_loop_v3`); the live staging file
(`outputs/anchor_staging.json`) holds 0 items; the live
anchors file holds 287 anchors, matching the audited register.
The MCP `get_anchor_staging` tool returned an AttributeError
(`'list' object has no attribute 'get'`) against the live
list-shaped staging file — a tool-shape defect, carried in the
bug lane. Conclusion of record: the defects are exposure, not
current contamination — the loop has not run on the
re-stood-up backend, and nothing is sitting wrongly accepted
in the live pipeline.

## 5. The storage-edit probe — observed verdict (parent supplement, 2026-11-13)

The test's claim-record storage-edit probe did not complete in
the main run (one attempt errored on a field name, the file
restored untouched; a later attempt was blocked before
execution). The parent completed it the same day, in the
loop-test clone, afterwards restored to pristine (claims
ledger back at SHA-256 `378f700d…`):

- Baseline, restored tree: the ledger gate reads the standing
  profile exactly — full mode **29 PASS / 0 FAIL / 1 NOT-RUN**.
- The edit: one bare storage change to the first ledger claim
  — `stage` from `created` to `digested` (the top of the
  vocabulary created → checked → explained → accepted →
  digested), `stage_history` none, no named human, no
  evidence, nothing else touched.
- Result: **DETECTED, but by cross-store consistency, not by
  lifecycle validation.** Full mode: 18 PASS / **10 FAIL** / 2
  NOT-RUN. `--regen` mode: 18 PASS / **13 FAIL** / 1 NOT-RUN.
  Every failure is a divergence check (V2 stage counts
  ledger-vs-matrix, V3 matrix recomputation, V5 map
  recomputation, V7 lossless regeneration, V8 settling
  canonicals): the independently recomputed derived artifacts
  no longer agree with the edited ledger. No check examines
  the transition itself — the record carries no `stage_history`
  at all and no check demands one. A coordinated edit across
  the ledger AND all derived artifacts would pass the gate,
  but producing those artifacts requires the program's own
  builders — a republication that git history exposes, not a
  storage edit.
- Logs: `logs/gate-baseline2.log`, `logs/gate-stageedit.log`,
  `logs/gate-stageedit-regen.log` in the test directory. (The
  probe's first baseline attempt, in the still-polluted clone,
  read 23/5/2 — all five failures traced to the test's own
  probe-mutated anchor/staging files, a small confirmation that
  the gate notices anchor-store tampering the same way.)

The bearing on this spec: for the claims ledger, protection is
post-hoc divergence detection. The anchor path has no derived
stores and no recomputation net — a direct edit or a bare API
flip there is detected by nothing. That is the exposure
C094-10 closes, and why D-094-5's gate survives the probe's
completion with its object changed (the re-run against the
built shape, Stage 4, plus Stage 0's inventory).
