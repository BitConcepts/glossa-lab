# Spec 087 — Stage S4 record (generated manual)

- Stage: S4 — generated manual (tasks T401–T404)
- Branch: `feat/087-s4-manual`, base main `0b200911`
- Date: 2026-11-03
- Seat: build worker (parent gates and merges)
- Claims answered: C087-8, C087-9, and the S4 leg of C087-15

## 1. What was built

One generation, three surfaces (decision D5; delimited blocks
only, narrative stays prose):

- `backend/glossa_lab/manual_generate.py` — the pure builder
  (the `tools/ledger` precedent: builder in a backend package,
  thin CLI over it). It reads the LIVE registry
  (`ATOMIC_NODES`) and the graph files on disk, and builds
  three outputs in memory before any file is touched:
  1. the Node Reference block in `docs/user-manual.md`
     (markers `<!-- BEGIN/END GENERATED node-reference -->`),
  2. the experiments table in `docs/USER_GUIDE.md`
     (markers `<!-- BEGIN/END GENERATED experiments-table
     -->`, sourced from `backend/glossa_lab/experiments/
     graphs/*.json`, `_archive/` excluded),
  3. `frontend/src/components/help/nodeReference.generated.ts`
     — a whole-file generated data module (header carries the
     do-not-edit notice); HelpView imports `NODE_REFERENCE` /
     `NODE_REFERENCE_COUNTS` from it and renders the reference
     from that data, so the in-app reference and the manual
     block are the same generation, never two.
- `tools/manual/generate_node_reference.py` — the CLI
  (`--check` builds without writing and exits 1 naming any
  drifted surface). A splice that finds its markers missing,
  duplicated, or out of order REFUSES by name and writes
  nothing — generation can never escape its delimited blocks.
- The node reference covers the PALETTE set (non-legacy
  nodes) with each node's id, name, category, description,
  inputs/outputs (name, type, required), and params (name,
  type, default, description) exactly as the registry carries
  them. Legacy nodes are not listed; the generated counts
  line carries the registered / legacy / palette numbers.
  One registry shape needed explicit handling:
  `ResearchLoopRunner`'s `params_schema` is a flat properties
  dict rather than a `{properties: ...}` schema; the builder
  normalizes both shapes.
- CI wiring: a pytest conformance test in the existing backend
  job — `backend/tests/test_manual_conformance.py` — following
  the Spec 084 pattern (committed generated output +
  regenerate-and-diff). That is the repo's established
  mechanism for generated-truth conformance; no new CI job or
  step was added. The ledger gate's separate job exists
  because it also regenerates matrix/map through a publish
  gate; here the check is a byte-compare plus set-identity and
  absence assertions, which the pytest carries directly
  against the same builder the CLI uses.

Counts, computed from the live registry at build time (never
arithmetic): **556 registered / 425 legacy / 131 palette /
24 palette categories / 65 registry categories / 27 graph
experiments**. (An early shell-side hand count said 25
palette categories; the generator's computed 24 governs, and
the conformance tests pin the outputs to the live registry by
set identity, so a hand count is never load-bearing.)

## 2. Generator + conformance output

Generator check, verbatim:

```
$ python tools/manual/generate_node_reference.py --check
OK: generated manual surfaces match the live registry
```

Delete-and-regenerate (T401 acceptance): the two markdown
blocks were emptied to their markers and the generated module
deleted; regeneration reproduced all three files
byte-identically (sha256 verified against the pre-delete
hashes; working tree clean afterwards).

Conformance + targeted suites (venv `glossa-ci`, this VM):

```
tests/test_manual_conformance.py                     7 passed
Spec 087 targeted set (registry integrity, palette
curation, S3 conversions A–F) + manual conformance
+ Spec 084 policy-sync conformance                 313 passed
```

Full backend suite, one run (no `-x`; ignores and the one
deselection per the standing local discipline):

```
1 failed, 2512 passed, 77 skipped, 1 deselected in 256.78s
FAILED tests/test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs
```

The single failure is the named phase133 local-only baseline
(missing download; green in CI). The 1 deselected is the
named phase392 determinism test (`test_phase392_q2_gate.py::
test_pipeline_deterministic_under_seed`), whose authoritative
runner is CI. No tray teardown error appeared this run.
In-tree regenerations the suite produces (`glossa-indus/`,
`outputs/`) were restored via `git checkout` before
committing and are not in this PR.

Frontend: `npm ci` + `npm run build` green (`tsc -b` clean;
vite build succeeded; the >500 kB chunk notice is the
pre-existing pattern, the bundle now carries the reference
data). `frontend/dist` is tracked for deployment by repo
convention (`.gitignore` note; the S1 PR shipped its rebuild
the same way) and is rebuilt and committed in this PR. The
Playwright e2e suite was not run locally; CI runs it against
the served build.

Ruff (CI scope, `ruff check backend/`): all checks passed.

## 3. Teeth (T402) — seeded, failed by name, restored

1. **Phantom name in prose.** Appended `Try the CorpusLoader
   node for this.` to `docs/user-manual.md` (outside the
   generated block):

   ```
   AssertionError: phantom node names in manual surfaces: {'docs/user-manual.md': ['CorpusLoader']}
   1 failed
   ```

   Restored via `git checkout`; test green again.

2. **Stale port inside the generated block.** Edited one port
   type in the block (`lm` (any, required) → `lm` (text,
   required)):

   ```
   $ python tools/manual/generate_node_reference.py --check
   DRIFT in generated manual surfaces:
     docs/user-manual.md
   Regenerate with: python3 tools/manual/generate_node_reference.py
   (exit 1)
   AssertionError: generated manual surfaces drifted from the live registry: ['docs/user-manual.md']
   ```

   Restored via `git checkout`; check green again.

3. **Hand edit in the generated module.** Edited one
   description string in `nodeReference.generated.ts`:

   ```
   DRIFT in generated manual surfaces:
     frontend/src/components/help/nodeReference.generated.ts
   (exit 1)
   ```

   Restored via `git checkout`; `--check` OK; conformance
   7 passed.

## 4. Phantom census — before / after

Before (line counts per name, at S4 start):

| Surface | Phantom occurrences |
|---|---|
| `docs/user-manual.md` | 11 lines across 6 names (CorpusLoader 2, MappingInference 4, AnchorInjector 2, ConsistencyEvaluator 1, JSONReportWriter 1, MarkdownReportWriter 1) |
| `docs/USER_GUIDE.md` | 0 |
| `frontend/src/components/HelpView.tsx` | CorpusLoader 10, EntropyAnalyzer 6, MappingInference 21, AnchorInjector 4, ConsistencyEvaluator 5, AnchorAccuracyEvaluator 2, RandomBaselineComparator 3, JSONReportWriter 8, MarkdownReportWriter 4, PDFReportWriter 6 |

After: **0 for all 10 names in all four surfaces**
(word-boundary grep, including the generated module; the
absence is also pinned by the conformance test). The stale
21-name Node Reference is replaced by the generated block;
the USER_GUIDE table now lists the real 27 graph experiments
(it previously listed 8 "active graph experiments").

## 5. Claim assessments

- **C087-8 — SUPPORTED AS SPECIFIED.** The manual's node
  reference is the palette set, mechanically: the builder
  generates from the live registry; the conformance test
  asserts set identity between the module/block and the live
  registry's palette (not byte-diff alone), spot-welds ports
  and params for probe nodes against the registry, and diffs
  regeneration in both directions; delete-and-regenerate is
  byte-identical.
- **C087-9 — SUPPORTED AS SPECIFIED** for the enumerable
  surfaces the claim names: none of the 10 phantom names of
  census Table 3 appears in any manual surface (pinned by
  test), and USER_GUIDE's experiment list set-equals the
  graph files on disk (27). Bound, per the task's own "does
  not establish": this pins names and lists; the truth of the
  surrounding prose is T403's human-oracle leg, not a machine
  claim.
- **C087-15 (S4 leg) — SUPPORTED AS SPECIFIED.** This stage's
  manual updates land in the same PR as the behaviour they
  describe (the generation itself, plus the prose pass T403);
  nothing was deferred to a later PR.

## 6. Departures and residuals, stated plainly

1. **Deeper pre-081 walkthrough prose remains.** The prose
   pass covered the plan-named items (screens tables, the
   Logs disposition, the palette confusion both ways, the
   phantom example redrawn, TokenFilter's params, node
   naming throughout, troubleshooting). Panel-interior
   walkthrough prose (e.g. HelpView's per-panel subsections,
   click-by-click tours, the Glossa AI sections) was not
   re-audited line by line in this stage; per T404's own
   bound, the manuals' enumerable claims are now
   machine-kept, and a full prose-truth audit is not claimed.
2. **`docs/USER_GUIDE.md` §16's Evidence Graph node-name
   table was left untouched** — outside the named prose
   scope; recorded here as a residual for closeout triage.
3. **HelpView presentation format is the component's.** The
   data is one generation; HelpView formats it in the same
   list layout as the markdown block so both surfaces read
   the same. The generated module is whole-file rather than
   a delimited block inside a hand-written file (design
   choice, recorded; drift is caught by the same byte-diff).
4. **S3-record reconciliation items carried to T701**
   (per T404): (a) the one-line wording correction to PR-B's
   section of `records/stage-s3-conversions.md` (the "DB
   copied in" phrasing PR-C corrected for its own batch);
   (b) reconciling the M77 fallback-retirement entry into
   the conversions record/tasks narrative; (c) the PR-A
   fitz comment + PDF-pin item named by the PR-F repair.
   None of these is discharged by this PR.
5. **The Logs disposition prose is written against S5's
   approved disposition** (own tab, D2 documented-ephemeral)
   and says the view is being restored under S5 — true at
   this merge; S5's own PR carries its manual update under
   C087-15 when the view ships.
