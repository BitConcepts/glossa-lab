# Spec 088 — implementation plan

**Date**: 2026-11-04. **Package branch**: `feat/088-spec-package` (this
package; repo home on adoption: `specs/088-program-map-gap-register/`).
**Proposal basis**: the owner's adoption of RCPH's full-picture system
(2026-11-04; `records/adoption-2026-11-04.md`), carrying constraints C1
(the gate extension rides the build) and C2 (prose-only standings are
register finds, never map data) as design rules, §6 below.

Build order, following the Spec 086 discipline — definitions before
derivation, the gate before the surface it verifies, generation before
judgment:

**defs + taxonomy + builder core → standing derivation → GATE EXTENSION →
page → scans → register.**

## Stage 0 — package adoption (precondition for every build stage)

- The package (spec.md, claims.md, aee-claims.json, plan.md, tasks.md,
  records/) lands in the repo as `specs/088-program-map-gap-register/` on
  the package branch, PR'd and merged on the owner's block approval.
- **T002 (done at drafting, re-verified at adoption)** — the C088 bundle
  was run through the pinned assessor in the CI-faithful venv, the same
  invocation as Spec 087's T002:

  ```
  ~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
  → valid: 19 claim(s) in aee-claims.json   (exit 0)
  ~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger \
      --input aee-claims.json --output records/t002-aee-assessment.json
  → exit 1; outcome: iterate
  ```

  Verbatim summary of record: "Assessed 19 claim(s); found 80 failure
  mode(s); 19 claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 19 of 19 claim(s)… Draft
  cap: 19 draft claim(s) capped at gather_evidence/iterate (FR-2.3).
  Stage cap: 19 claim(s) below stage 'explained'; the outcome cannot be
  'pass' (Spec 004 R1.4)…" (full text: `records/t002-note.md`; the
  assessment itself: `records/t002-aee-assessment.json`). `iterate` is
  the expected outcome for a draft bundle on a single asserted source;
  the owner's approval (T003) is the human act.
- **Pre-append gate check (the freeze discipline)**: before the intake
  append, the adoption PR runs the gate CLI on the un-appended tree and
  records ALL PASS, so any post-append failure is attributable to the
  append and not to drift. (Spec 087's C4 freeze does not apply — Spec
  088 amends no gate records — but the append grows the ledger, and the
  matrix/map layers must be regenerated over it; see T004.)
- **T003 — owner block approval** of spec + 19 claims + this plan + the
  taxonomy v0 draft + decisions D-088-1..6. No build task starts before
  it.
- **T004 — adoption intake**: the claims enter the ledger through
  `tools/ledger/import_bundle.py --spec specs/088-program-map-gap-register
  --date <adoption date>` — never a hand-edit of claims.jsonl — followed,
  in the same motion, by regeneration of the Spec 086 generated layers
  over the grown ledger (matrix + map rebuilt and republished through
  `tools/ledger/gated_publish.py`, gate output recorded), exactly the
  Spec 087 adoption shape. The bundle-reconciliation test must pass:
  ledger bundle population == bundles on disk. Claim C088-15 bounds the
  whole spec's ledger diff to this append.

## Dependencies

- Spec 086 complete (ledger, gate V1–V9, gated publish, the generated
  layers) — landed 2026-11-02. Spec 087 complete (registry discipline,
  generated-manual precedent) — landed 2026-11-03.
- The manual generator (`backend/glossa_lab/manual_generate.py`,
  `tools/manual/generate_node_reference.py`, its conformance test) as the
  builder pattern — in the tree.
- The ledger schema (`glossa-indus/ledger/SCHEMA.md`, ledger-schema v1)
  and the matrix definitions registration model
  (`glossa-indus/matrix/DEFINITIONS.md`) as the defs pattern — in the
  tree.
- S3 depends on S1+S2 (the gate verifies what the builder produces). S4
  depends on S3 (C1: no publication before V10). S5 depends on S2's find
  list (not on S4 — scans read the JSON, not the page). S6 depends on S5.

## Stage 1 — Definitions, taxonomy, builder core

**PR**: `feat/088-s1-defs-builder` → one PR (defs + taxonomy + builder +
CLI + builder tests).

**Contents**:

- `glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md` — **program-map-defs v1**,
  registered exactly as matrix-defs was: a version header, the statement
  that amendment is a new version propagated to every registered copy in
  the same motion, and the rules:
  - *Inputs (closed list)*: the ledger (`claims.jsonl`, read through the
    canonical-hash discipline), the taxonomy file, and the spec tree's
    directory names. Nothing else is read for any standing (C2).
  - *Claim derivation*: resolve reclassification chains in ledger order
    (the governing entry is the chain's head; the ledger today contains
    zero reclassification entries, so the rule is registered ahead of
    need); annotation entries never affect standings. The status→class
    table of D-088-3, applied to the governing entry; an unregistered
    status fails the build naming the entry. Standing text is a
    mechanical template over verbatim fields: `Ledger standing: status
    <status> · stage <stage|none> · falsifier <present|absent>`, plus the
    class chip. (`aee_state` plays no part: it is null for all 857
    entries today.)
  - *Study membership*: a claim belongs to study S iff it is a bundle
    claim and any of its `sources[]` carries `spec` == S's directory
    name. Extracted claims belong to no study; their nodes take the
    taxonomy's extracted-claim assignments (by source document).
  - *Study roll-up* (over member classes; first match wins): no members →
    **unjudged**; any positive and any negative → **judgment call**
    (displayed class: open; the case is listed in the build record with
    member counts); all members closed_other → **closed_other**; any
    negative → **negative**; any positive → **positive**; otherwise
    **open**.
  - *Find kinds emitted by the builder*: bundle-less study (one per
    unjudged study); judgment call (one per mixed study); extracted claim
    with a null falsifier (the 9, enumerated); restricted node (name-only
    rendering notice).
  - *Coverage block*: per-domain × per-class node counts; the unjudged
    study list; the judgment-call list; falsifier coverage recomputed
    from the ledger at build time.
  - *Stamp*: ledger canonical SHA-256, ledger line count, the ledger's
    latest entry date, `ledger-schema v1`, `program-map-defs v1`,
    `program-map-taxonomy v1`. No wall clock.
  - *in_flight*: registered, no derivation rule in v1; emitting one fails
    the build (D-088-4).
- `glossa-indus/map/program-map-taxonomy.json` — **program-map-taxonomy
  v1**, the file shape of `records/taxonomy-v0-draft.md` (RCPH's shape,
  minus the `curated` mechanism, which the format does not carry at all —
  C088-17): declared domains/subdomains, the 88 study assignments, the
  extracted-claim document assignments, the restricted list.
- `backend/glossa_lab/program_map_generate.py` — the pure builder
  (mirrors `manual_generate.py`'s discipline): reads only the defs'
  inputs; returns the three artifacts (`program-map.json`,
  `program-map-finds.json`, `program-map.html` — the page is rendered in
  S4; S1 emits JSON + finds and a minimal page shell only if needed for
  the conformance test, otherwise the page artifact joins in S4 and the
  defs' artifact list says so); sorts everything; fails closed on
  coverage, unknown ids, undeclared domains, unregistered statuses, and
  in-flight emission.
- `tools/map/generate_program_map.py` — the CLI: default mode writes the
  artifacts; `--check` builds without writing and exits 0 only if every
  committed artifact is byte-identical to the fresh build, else exits 1
  with the named refusal (the manual CLI's exact semantics).
- Builder self-tests with teeth (`backend/tests/`): the derivation table
  exercised per status; the roll-up precedence exercised per rule
  including the judgment-call case; coverage teeth (a fixture with a
  dropped claim id fails; a duplicated assignment fails; an unknown
  taxonomy id fails); a seeded unregistered status fails; determinism
  (two builds byte-identical).

**Verification**: builder test module green; a first real build over the
live ledger + taxonomy reproduces the census of record (857 claim nodes,
88 study nodes, 28 unjudged studies) — the census is recomputed by the
test, not asserted from this plan's numbers.

**CI jobs**: the conformance test (Spec 084/087 style,
`backend/tests/test_program_map_conformance.py`: regenerate in a tmp copy
and byte-compare; `--check` drift case) joins the existing **Backend
tests** job. No new CI job — the precedent is the manual conformance test,
and nothing in S1 needs a runner the existing jobs lack.

**Claims**: C088-1, C088-2, C088-9, C088-15 (format side), C088-17,
C088-18.

## Stage 2 — Standing derivation

**PR**: `feat/088-s2-derivation` → one PR (the derivation is S1's builder
exercised over the real inputs; this stage lands the committed artifacts
and the derivation census).

**Contents**:

- The first committed `program-map.json` + `program-map-finds.json` over
  the live ledger and taxonomy v1.
- The derivation census in the stage record: per-domain counts (from the
  coverage block, quoted); the judgment-call list with member counts; the
  unjudged list (expected: the 28 bundle-less studies); falsifier coverage
  as recomputed (expected 848/857 with the 9 extracted nulls enumerated in
  the find list).
- Determinism proof: delete the artifacts, regenerate, byte-compare;
  recorded with hashes.

**Verification**: `--check` exits 0 on the committed artifacts; the census
numbers in the stage record are the coverage block's own numbers (quoted,
not paraphrased); every judgment call in the record matches a find-list
entry 1:1.

**CI jobs**: Backend tests (conformance now covers real artifacts).

**Claims**: C088-3, C088-4, C088-5, C088-6, C088-13, C088-14.

## Stage 3 — Gate extension (V10)

**PR**: `feat/088-s3-gate-v10` → one PR (gate class + defs copies + teeth
tests + writer registration).

**Contents**:

- `backend/glossa_lab/ledger_gate.py` gains **class V10 — program-map
  equivalence**, following the V3/V5 recomputation pattern exactly: the
  gate carries its **own registered copies** of program-map-defs v1 (the
  derivation table and roll-up precedence as gate-side constants, with
  the registration comment the matrix tables carry — deliberately not
  imported from `program_map_generate`), recomputes the map from the
  ledger + taxonomy by an independent route, and checks: published
  `program-map.json` byte-equals the recomputation; coverage is exact
  (claim ids and spec dirs, set equality both directions); every citation
  resolves; the stamp's ledger hash/lines/latest date equal the current
  ledger's; the find list equals the recomputed find list. The page
  artifact joins V10's equality set when S4 lands it (V10's artifact list
  is versioned with the defs; S3 registers the JSON + finds, S4's PR adds
  the page to the gate's registered copies in the same motion — an
  amendment recorded in the stage record, per the defs discipline).
- **V9 registration**: `program_map_generate` joins the registered-writer
  list and the map artifacts join the artifact path patterns, so a
  hand-edit of a program-map artifact by any unregistered path is itself
  a gate failure.
- **Teeth tests** (`backend/tests/test_ledger_gate.py` additions): a
  seeded divergence in a tmp copy of program-map.json fails V10 (and the
  report names V10); a seeded divergence between the builder's table and
  the gate's copy fails; a stale stamp fails; a dropped node fails.
  Seeded means seeded: the tests mutate copies, never the tree.
- No change to `gated_publish.py`'s CLI or contract; the map artifacts
  publish through it once V10 exists.

**Verification**: gate CLI over the real tree reports ALL PASS with V10
present in the per-class list; the teeth tests pass; the pre-existing
V1–V9 behaviour is unchanged (full gate test module green).

**CI jobs**: the existing **ledger-gate** job runs the gate CLI — V10
joins its report with no workflow change. No new CI job (argued: the
job's contract is "the gate, whole"; splitting V10 into its own job
would let the matrix classes and the map class drift into separate
publication decisions, which is what C1 forbids).

**Claims**: C088-7 (and C088-16's precondition).

## Stage 4 — The page

**PR**: `feat/088-s4-page` → one PR (page rendering in the builder + the
committed page + V10's artifact-list amendment + Playwright evidence).

**Contents**:

- The builder renders `program-map.html`: a single static page with the
  program-map JSON embedded verbatim (RCPH pattern); domains and
  subdomains as collapsible sections; one row per node with its class
  chip, standing text, and citations; class filters (All / Positive /
  Negative / Open / In flight / Closed–other / Unjudged) and a text
  search, both operating only on generated fields; the header shows the
  stamp and the per-domain counts from the coverage block (no aggregate
  score anywhere — C088-14). Restricted studies render name-only
  (C088-19). The design follows the RCPH reference page's layout, which
  the owner has already seen and ratified as a system; the package
  approval (T003) is therefore the design approval for this internal
  page, and no separate wireframe gate applies. (It is not the product
  UI and not a public website.)
- The stage record cites the V10 gate output over the page's own
  artifacts (C088-16's acceptance evidence).

**Verification**: **Playwright render verification before any verified
claim** — the generated page rendered at desktop (1440×900) and mobile
(390×844) widths, screenshotted, and checked against the design points
(sections collapse, filters change the visible set, search narrows to
generated-field matches, restricted node shows no standing); screenshots
kept with the stage record. Source-level checks (grep, JSON parse) are
necessary and not sufficient, per the standing rule.

**CI jobs**: Backend tests (conformance covers the page bytes once S4
lands it).

**Claims**: C088-8, C088-16, C088-19.

## Stage 5 — Gap scans (three clusters)

**PRs**: one per cluster — `feat/088-s5a-corpus-anchors`,
`feat/088-s5b-families-contact`, `feat/088-s5c-infra-bookkeeping` (records
only; no code).

**Contents**: a scan record per cluster
(`specs/088-program-map-gap-register/records/scan-<cluster>.md`) over the
generated map + find list, using the four-kind template of
`records/scan-plan.md` and nothing else. Inputs and pre-answered legs are
fixed by the scan plan: e.g. the falsifier census (848/857, the 9
extracted nulls enumerated by the find list), the WP5 support census
(6/46/37/3/2 over the 94 strict anchors), WP4's 0-of-184 — cited from
their records, never re-derived. Every candidate carries a one-line
falsifier and an honesty-rule type (in-house re-derivation vs independent
confirmation — C088-12).

**Verification**: human-as-oracle on find classification (the reviewer
checks each find is one of the four kinds and each candidate has its
falsifier and type); a template-conformance pass (mechanical: kinds,
falsifiers, types present) recorded per cluster.

**CI jobs**: none (records-only stages; the register stage's completeness
check is where the mechanical teeth live).

**Claims**: C088-10, C088-12.

## Stage 6 — Gap register v1 + ratification

**PR**: `feat/088-s6-register` → one PR (register + completeness annex).

**Contents**:

- `glossa-indus/map/gap-register.md` — **gap register v1**, RCPH's entry
  format: a headline ranked list; entries `GR-088-NN. TITLE (domain).
  STATUS.` in the status vocabulary (UNSTATED / UNMEASURED / UNJUDGED /
  UNCONNECTED / DATA-BLOCKED / TIME-SENSITIVE); each entry names the
  missing node or edge, why its absence blocks decipherment convergence
  or program convergence, the candidate study with its falsifier, its
  honesty-rule type, and its owner gates; a closing section, "Owner
  decisions this register surfaces"; and the ratification block.
- A **source-coverage annex**: every item on C088-11's source lists
  mapped to its entry id(s) or its recorded not-a-gap disposition. The
  completeness check is mechanical where the source is enumerable (the
  find list's items all appear; the 28 unjudged studies all appear; the 9
  null-falsifier claims are dispositioned) and human-as-oracle against
  the annex for the prose source lists (GAP-C07/C12, the brief, the
  residuals) — the annex is the artifact the oracle reads.
- **The owner's block ratification of register v1 ends the spec.** First
  waves are commissioned from the ratified register by a separate owner
  act (non-goal of this spec).

**Verification**: completeness check output recorded (mechanical legs) +
oracle sign-off line in the stage record (prose legs); register entries
cross-checked against the scan records (every scan find is in an entry or
dispositioned).

**CI jobs**: none new (the register is a document; its mechanical legs
run as a stage task, and any later regeneration discipline is a defs
amendment question for a future spec).

**Claims**: C088-10, C088-11, C088-12.

## Closeout

- **T701 — closeout record**: per-claim dispositions for C088-1..19
  (discharged / carried), the final census (nodes by domain and class,
  from the coverage block), the register's entry count and ratification
  reference, and the explicit statement that no first wave is commissioned
  by this spec.

## Design rules carried through every stage (C1/C2 operationalized)

- **C1**: S3 precedes S4's publication; the gate's report is the only
  publication authority for map artifacts; a red V10 is a stop, not a
  waiver.
- **C2**: the builder's input list is closed (defs §inputs); any PR that
  adds an input is a defs amendment and must argue why the new input is a
  record of record, not prose; the taxonomy format carries no standing
  fields, by construction.
- Verdicts and counts come from records (coverage blocks, gate reports,
  find lists), quoted in stage records — never from summaries of them.
