# Ratification + adoption record — Spec 094 (ratified 2026-11-13; adoption PR `spec/094-adoption`)

**Scope:** tasks.md adoption runs T001–T003, executed on
branch `spec/094-adoption` after the owner's block
ratification. This record covers the ratification act, the
AEE assessment at adoption, the parent addendum's probe
verdict (which adjusts D-094-5's object), the sequencing, and
the two places where this landing departs from the Spec 092
adoption shape — named on the face of the record, not smoothed
over. **The claims-ledger intake (T004) is NOT executed by
this PR** (see "The intake, deferred as its own act" below).
No build stage (Stage 0 onward) is started by this motion: no
gate has been built, no candidate has been re-evidenced, and
the research loop has not run.

## The ratification act (T003)

**Owner block ratification: Tristen Pierson, 2026-11-13.**
The package (spec.md, claims.md with falsifiers, plan.md,
tasks.md, the grounding record) was presented in the
Glossa-Lab chat and the owner ratified it **AS A BLOCK** —
the option tap "Adopt Spec 094 as recommended" plus the typed
confirmation "Adopt Spec 094 as recommended" — decisions
D-094-1..6 all as drafted, each carrying the recommendation
text it was ratified with:

- **D-094-1 — Who may approve: a recorded named-humans list,
  initially the owner alone.** *Recommendation: the gate is
  the `claim_stage` rule (a named human validates; a process
  never does); the list is identical to owner-only today, and
  Spec 091's future independence-leg humans join by list
  amendment instead of code change. The list lives where the
  actor rules already read their allowlist from, or beside it
  — not a new registry.*
- **D-094-2 — The promotion evidence standard: pinned
  artifact AND registered class.** *Recommendation: both
  halves, as claimed in C094-4 + C094-5 — neither half alone
  closes defect 2 (a pin without a class admits a hashed
  README; a class without a pin admits a mutable file).
  Path-exists, the status quo, stands rejected by the probe
  record. The per-promotion friction is the gate working as
  intended.*
- **D-094-3 — Auto-verification: abolish the automatic
  route.** *Recommendation: remove the run-level flip
  outright (C094-7); "verified" exists only as a per-candidate
  gated act (C094-6). A future need for automated verification
  arrives as its own claim with its own falsifier, not on this
  spec.*
- **D-094-4 — Staging order: Stage 0 immediately; build
  stages after Spec 092 S1 and before Spec 091 Stage 1.**
  *Recommendation: 092 S1 is already next in the adopted
  queue and is untouched by this; 091 Stage 1's locator pass
  produces exactly the candidate flow that must not enter an
  ungated path, so 094's gates are 091's precondition in
  substance. Stage 0 runs in parallel with 092 S1.*
- **D-094-5 — The storage-edit probe is Stage 0's exit gate —
  as adjusted by the parent addendum (below).**
  *Recommendation as ratified: the probe's observed verdict,
  not an inference, gates the routing stage's design; with
  the probe now complete, Stage 0's exit gate is the probe's
  RE-RUN against the built shape (Stage 4) plus the live
  store inventory.*
- **D-094-6 — Pre-gate archive stock: promotability
  suspended, not grandfathered.** *Recommendation: entries
  approved or verified before these gates land keep their
  recorded status as history but cannot promote until
  re-evidenced onto the new record fields (C094-12). Nothing
  is deleted, demoted, or re-adjudicated; the only suspended
  thing is forward motion.*

The spec's Status line is stamped RATIFIED with the date, in
spec.md on this branch.

## The parent addendum — the storage-edit probe is COMPLETE

The package was drafted while the claim-record storage-edit
probe was still an open item, and its D-094-5 / Stage 0 / caps
text was written on that premise. The parent completed the
probe on 2026-11-13, after drafting and before ratification;
the addendum is appended to the package in the goal workspace
and its substance is carried here verbatim, because the
ratification was given with it in hand:

> Observed verdict: a bare storage edit flipping one ledger
> claim from stage "created" to "digested" (no
> stage_history, no named human, no evidence) is DETECTED by
> the ledger gate — full mode falls from the standing 29 PASS
> / 0 FAIL / 1 NOT-RUN to 10 FAIL, --regen mode to 13 FAIL —
> but every failure is a cross-store consistency check (ledger
> vs the independently recomputed matrix, map, and settling
> artifacts). No check validates the transition itself.
> Consequences for this package: (1) D-094-5's recommendation
> stands in substance but its object changes — the probe no
> longer needs completing; Stage 0's exit gate becomes the
> probe's RE-RUN against the built shape (already Stage 4's
> plan) plus the live store inventory, which remains undone
> and is Stage 0's real remaining work. (2) The finding
> sharpens C094-10's grounding: for the claims ledger the
> protection is post-hoc divergence detection, and the anchor
> path has no equivalent recomputation net at all — which is
> the exposure this spec exists to close. (3) Nothing else in
> the claims or decisions changes.

Full method and counts: the grounding record, §5. Logs:
`gate-baseline2.log`, `gate-stageedit.log`,
`gate-stageedit-regen.log` in the test directory
(`~/workspace/glossa-run/loop-test-2026-11-13/`).

## Sequencing (D-094-4, as ratified)

- **Stage 0 (grounding completion) runs immediately**, in
  parallel with Spec 092 S1, which it does not disturb.
- **Build stages 1–4 run after Spec 092 S1 and before Spec
  091 Stage 1.** The intake act (T004) is independent of this
  order and lands on its own gating.
- Nothing in this adoption starts any stage; Stage 0's first
  act is its own record.

## AEE at adoption (T002, assessment clause)

The bundle was verified mechanically against claims.md at
adoption: the same 13 ids (C094-1..13) in the same order,
every claim carrying at least one falsification test, and
every bundle falsifier and statement found in its claims.md
block (whitespace-normalized comparison) — the bundle in the
package is the claims.md bundle, unaltered. Under the pinned
AEE (glossa-ci venv), from the package directory:

- `aee validate aee-claims.json` — `valid: 13 claim(s) in
  aee-claims.json`, exit 0.
- `aee assess --no-ledger --input aee-claims.json
  --output records/adoption-aee-assessment.json` — exit
  1, outcome **iterate**, recorded verbatim:
  "Assessed 13 claim(s); found 56 failure mode(s); 13
  claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 13 of 13
  claim(s); the same evidence set supports multiple claims
  (FR-2.8, reporting only, no outcome effect in this phase).
  Draft cap: 13 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 13 claim(s)
  below stage 'explained'; the outcome cannot be 'pass'
  (Spec 004 R1.4). Not understood: 26 residual unknown(s) are
  recorded on this assessment (Spec 004 R5.2). Lane 1
  (machine verification): outcome iterate; 0 claim(s) at or
  above the 0.70 threshold, 13 below. Lane 2 (human
  acceptance): stages by effective stage: created 13.
  Lane-2 lag: 13 claim(s) below explained."

"Iterate" is the normal reading for a draft bundle at
adoption (Specs 090, 091, 092 and 093 read the same way); it
is recorded, not chased. The assessment of record is
`records/adoption-aee-assessment.json` on this branch.
**No draft-time assessment exists for this package** — the
package was drafted in the goal workspace without an
assessor run — so there is no T002-twin file and no
draft-vs-adoption comparison to make; the adoption
assessment is the first of record and nothing is back-filed
to suggest otherwise.

## The intake, deferred as its own act (T004)

Spec 092's adoption PR (#548) executed its claims intake
inside the adoption PR: program-map assignment, the
`import_bundle.py` append, the settling-chain refresh, the
generated-layer regeneration, and the census re-pins in the
pin-bearing tests. This adoption PR does not, by the
adoption instruction's own scope: it is a records/spec PR —
spec files, this record, the grounding record, the adoption
assessment, and the root LEDGER.md entry — with no code or
test changes and no alteration of gate inputs (claims.jsonl,
matrix, map). The intake therefore stands as tasks.md T004, a
separate gated act on the #548 pattern, executed after this
landing and recorded in its own record. Two consequences are
named here so neither is mistaken for a defect in the spec
files:

- The C094 claims do not yet stand in the claims ledger. The
  bundle of record until the intake lands is this directory's
  `aee-claims.json`; the ledger grows by exactly this bundle
  when T004 executes, and not before.
- The program map's builder enumerates `specs/` directories
  from disk and its gate leg (V10) names an unassigned spec
  directory: until T004 assigns
  `094-research-loop-acceptance-hardening` in
  `glossa-indus/map/program-map-taxonomy.json` and regenerates
  the map layers, the ledger-gate CI job on this PR is
  expected to read that V10 finding. That reading is T004's
  to discharge, exactly as the pre-assignment tree read
  25 PASS / 4 FAIL / 1 NOT-RUN at Spec 092's adoption before
  its assignment landed.

## Directory name

The package's drafting text named the spec directory
`specs/094-loop-acceptance-hardening/`. It lands as
`specs/094-research-loop-acceptance-hardening/`, per the
adoption instruction and the repo's descriptive-slug
convention (cf. `091-anchor-comparison-integrity`,
`093-material-context-channel`): the spec's subject is the
research loop's acceptance path, and the longer name says so.
The package text is carried unaltered in the goal workspace;
this record is the name's correction of record.

*This does not establish:* anything beyond the ratification's
landing — no build stage (Stage 0 onward) is started by this
motion, the claims do not yet stand in the ledger (T004 is a
separate act), no claim's status, stage, or score is changed
by the bundle's existence, and the research loop remains off
the live stores under C094-13, which this adoption asserts
and does not lift.
