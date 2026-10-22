# Spec 026 — Tooling Verification (Glossa-Lab worktree)

Worktree verified: `~/workspace/glossa-lab-spec026` (NOT `~/workspace/glossa-lab`).
No commits made. No tracked files outside `specs/026-rcph-framework-transfer/working/`
were modified — all live tests ran in `/tmp/aee-proj026`, `/tmp/aee-test026`,
`/tmp/eval-demo026`. `git status --porcelain` before and after testing was only:

```
?? specs/026-rcph-framework-transfer/
```

Date of runs: 2026-10-10/11 (EDT, timestamps in outputs are UTC).

## Versions table

| Item | Version / fact | Evidence |
|---|---|---|
| `specify` CLI (`~/workspace/venvs/spec-kit/bin/specify`) | `specify 1.0.10` | `specify --version` → `specify 1.0.10`, exit 0 |
| Spec Kit integration in this worktree | `copilot`, script `sh`, invoke separator `-` | `.specify/integration.json`: `"integration": "copilot"`, `"version": "1.0.10"` |
| AEE extension (`aee`) | **v1.1.0**, Enabled, Commands: 8, Hooks: 5, Priority: 10 | `specify extension list` (see §1) |
| Evaluator extension (`evaluator`, "Evaluator Contract") | **v1.0.0**, Enabled, Commands: 4, Hooks: 4, Priority: 10 | `specify extension list` (see §1) |
| `aee` Python package — glossa-lab venv | **1.0.4** (distribution `applied-epistemic-engineering`) | `importlib.metadata.version('applied-epistemic-engineering')` → `1.0.4`; `~/workspace/venvs/glossa-lab/bin/aee --version` → `aee 1.0.4` |
| `aee` Python package — spec-kit venv | **1.0.2** | `~/workspace/venvs/spec-kit/bin/aee --version` → `aee 1.0.2` |
| `aee` package named literally `aee` in metadata | **No such distribution** | `importlib.metadata.version('aee')` → `No package metadata was found for aee` |
| `glossa-lab` package (glossa-lab venv) | `0.1.0`, editable install pointing at another checkout (`/home/hatch/workspace/glossa-lab-phase120/backend` in `pip list`) | Tests in §5 forced the worktree copy by prepending `~/workspace/glossa-lab-spec026/backend` to `sys.path` and printing `aee_core.__file__` |
| AEE extension's required `aee` tool range | `>=1.0.2,<2` (plus Python `>=3.11`, plus evaluator extension `>=1.0.0,<2`) | `.specify/extensions/aee/extension.yml` `requires.tools` |

Version-split caveat: which `aee` engine actually runs depends on which venv is
on `PATH` (1.0.4 from the glossa-lab venv, 1.0.2 from the spec-kit venv).
`backend/glossa_lab/aee_core.py`'s docstring says its mapping was
"verified against aee 1.0.4, `aee/model.py`".

## 1. specify CLI

Run inside `~/workspace/glossa-lab-spec026`:

```
$ ~/workspace/venvs/spec-kit/bin/specify --version
specify 1.0.10

$ ~/workspace/venvs/spec-kit/bin/specify check
...
├── ● Codex CLI (available)
...
Specify CLI is ready to use!
```
(`specify check` exit 0; almost all other agent CLIs reported "not found" —
irrelevant here because the integration in use is Copilot, which is
"IDE-based, no CLI check".)

```
$ ~/workspace/venvs/spec-kit/bin/specify extension list

Installed Extensions:

  ✓ Applied Epistemic Engineering (v1.1.0)
     aee
     Challenge claims, trace evidence, propagate uncertainty, and route
epistemic failures across phases
     Commands: 8 | Hooks: 5 | Priority: 10 | Status: Enabled

  ✓ Evaluator Contract (v1.0.0)
     evaluator
     Provider-neutral evaluator result contract for evidence, provenance,
uncertainty, and recovery between SDD phases
     Commands: 4 | Hooks: 4 | Priority: 10 | Status: Enabled
```

`specify extension list --json` confirms the same:
`{"id": "aee", "version": "1.1.0", "enabled": true, "provides": {"commands": 8, "templates": 1, "scripts": 2, "hooks": 5}}`
and `{"id": "evaluator", "version": "1.0.0", "enabled": true, "provides": {"commands": 4, "templates": 1, "scripts": 3, "hooks": 4}}`.

Both extensions the task expected (aee + evaluator) are installed and enabled.
`.specify/extensions.yml` has `settings: auto_execute_hooks: true` and hooks:
`after_specify` / `after_plan` / `after_tasks` / `after_implement` →
`speckit.aee.assess` (priority 30, optional) + `speckit.evaluator.run`
(priority 20, optional); `after_verify` → `speckit.aee.gaps` (priority 40, optional).

## 2. How AEE/evaluator assessments were run for recent specs; invocation mechanism

### 2a. Specs 024 and 025 contain NO assessment artifacts

`specs/024-evidence-integration/` contains only:
`motif-arm-closure.md, plan.md, spec.md, stage1-freeze-2.md, stage1-freeze.md,
stage2a-freeze.md, stage2c-freeze.md, stage2d-freeze.md, tasks.md`.

`specs/025-stage2-controlled-followup/` contains only:
`phase139-freeze.md, phase140-freeze.md, phase141-freeze.md, plan.md, spec.md, tasks.md`.

A case-insensitive grep for `aee|evaluator|assessment` over both directories
finds no assessment/evaluator/gaps artifact — the only hits are unrelated
English words ("assesses its parseability", "dating-gap caveat", "evaluation").
There is also no output on disk from any hook run anywhere in the worktree:

```
$ ls .specify/extensions/aee/assessments .specify/extensions/aee/ledger .specify/extensions/evaluator/results
ls: cannot access '.../assessments': No such file or directory
ls: cannot access '.../ledger': No such file or directory
ls: cannot access '.../results': No such file or directory
```

So for Specs 024/025 there is **no evidence the AEE/evaluator hooks were ever
executed**; the hooks are `optional: true` prompts in `extensions.yml`, and those
specs proceeded on their freeze/verdict documents alone. The only spec that
records the extension setup is the baseline: `specs/001-glossa-lab-baseline/tasks.md`

> `- [x] T002 Install AEE + evaluator extensions from local clones (--dev), vendored as real files (no gitlinks, no nested .git/venvs)`
> `- [x] T008 (Stage 2) AEE core adapter aee_core.py + wiring + tests`

and its `plan.md`: "spec-kit (`specify` 1.0.10, copilot integration) with the AEE
and evaluator extensions vendored as real files under `.specify/extensions/`;
hooks in `.specify/extensions.yml` run AEE assessment after
specify/plan/tasks/implement and gap regeneration after verify." (Stated design,
not a per-spec run record.)

### 2b. Exact invocation mechanism — agent markdown commands, NOT a shell CLI

The extension commands are **Markdown prompt/command definitions for a coding
agent**, in two materialisations of the same text:

1. Canonical: `.specify/extensions/aee/commands/speckit.*.md` and
   `.specify/extensions/evaluator/commands/speckit.*.md`.
2. Copilot integration rendering (this worktree's integration is `copilot`):
   `.github/skills/speckit-aee-assess/SKILL.md`, `speckit-aee-gaps/SKILL.md`,
   `speckit-evaluator-run/SKILL.md`, etc. — `SKILL.md` files whose body is the
   same command text (verified for `speckit-aee-assess`; it even rewrites the
   compose cross-reference to `/speckit-evaluator-compose …`).

There is no `specify aee …` / `specify evaluator …` subcommand and no executable
named after these commands. An agent (Copilot/agent session) reads the Markdown,
follows its Prerequisites/Execution steps, and runs the underlying script/CLI
itself. `speckit.*` is the dotted name inside the Markdown; the Copilot skill
name uses hyphens (`speckit-aee-assess`).

AEE command definitions (`.specify/extensions/aee/commands/`, 8):

| Command | File | What its Execution step actually runs |
|---|---|---|
| `speckit.aee.assess` | `speckit.aee.assess.md` | `python .specify/extensions/aee/scripts/python/run_aee.py assess --input <artifact> --phase <phase> --threshold <threshold>` (default threshold `0.70`) |
| `speckit.aee.challenge` | `speckit.aee.challenge.md` | `run_aee.py challenge …` |
| `speckit.aee.trace` | `speckit.aee.trace.md` | `run_aee.py graph …` (per adapter) |
| `speckit.aee.verify` | `speckit.aee.verify.md` | `run_aee.py verify …` → `aee verify-ledger` |
| `speckit.aee.gate` | `speckit.aee.gate.md` | `python .specify/extensions/aee/scripts/python/run_aee.py gate --input <assessment>` |
| `speckit.aee.gaps` | `speckit.aee.gaps.md` | `python .specify/extensions/aee/scripts/python/run_aee.py gaps --matrix <matrix> --evidence <evidence> --output <output>` (+ optional `--close GAP-XXX`, `--existing <prior>`) |
| `speckit.aee.route-evidence` | `speckit.aee.route-evidence.md` | agent procedure / token-economy script |
| `speckit.aee.report-savings` | `speckit.aee.report-savings.md` | `scripts/python/aee_token_economy.py` |

Evaluator command definitions (`.specify/extensions/evaluator/commands/`, 4):
`speckit.evaluator.run`, `speckit.evaluator.compose`, `speckit.evaluator.report`,
`speckit.evaluator.route` — see §4 for the important difference (only `compose`
has a real script behind it).

The AEE adapter `.specify/extensions/aee/scripts/python/run_aee.py` is a real,
path-safe Python CLI (argparse subcommands `assess|challenge|graph|verify|gate|gaps`).
It rejects symlinked/escaping paths, then shells out to the external `aee`
executable found via `shutil.which("aee")`:

```python
executable = shutil.which("aee")
if executable is None:
    print("Missing required 'aee' command. Install applied-epistemic-engineering>=1.0.2,<2.", file=sys.stderr)
    return 2
```

Verified live (default shell has no `aee`): `which aee` → not found, and
`run_aee.py assess …` without a venv on `PATH` prints exactly that message and
exits **2**. So the mechanism is runnable here only with a venv that provides
`aee` on `PATH` (either venv above satisfies the version range).

`assess` writes (paths hardcoded in the adapter):
`.specify/extensions/aee/assessments/aee-<phase>-<timestamp>.json`,
`.specify/extensions/evaluator/results/aee-<phase>-<timestamp>.json`, and appends to
`.specify/extensions/aee/ledger/epistemic-ledger.jsonl` (unless `--no-ledger`).

### 2c. `.specify/scripts/`

Only core Spec Kit shell scripts — no AEE/evaluator code:
`.specify/scripts/bash/{check-prerequisites.sh, common.sh, create-new-feature.sh,
resolve-template.sh, setup-plan.sh, setup-tasks.sh}`.

## 3. The `aee` Python package and `backend/glossa_lab/aee_core.py`

### Imports cleanly; public API

`aee_core.py` imports `from aee.graph import ClaimGraph`, `from aee.model import
Claim, ClaimKind, ClaimStatus, Evidence, EvidenceDirection, EvidenceKind,
SourceQuality`, `from aee.scoring import ClaimScore, ScoringEngine`.
Its own public surface (from the §5 live run, `aee_core.__file__` =
`…/glossa-lab-spec026/backend/glossa_lab/aee_core.py`):

```
public API: ['Claim', 'ClaimGraph', 'ClaimKind', 'ClaimScore', 'ClaimStatus',
 'Evidence', 'EvidenceDirection', 'EvidenceKind', 'ScoringEngine', 'SourceQuality',
 'assessment_summary', 'build_graph', 'claim_from_glossa', 'claims_from_record',
 'load_claims_from_dir', 'map_kind', 'map_status', 'score_claim_dicts', 'score_claims']
```
(plus re-exported `Any/Iterable/Path/json/logging/annotations`.)

Functions: `map_status()` / `map_kind()` (Glossa→AEE enum translation;
`untested` → `ClaimStatus.DRAFT`, original preserved in `Claim.metadata`),
`claim_from_glossa(raw, source_file="")`, `claims_from_record()`,
`load_claims_from_dir()` (deduplicates claim_ids — "ClaimGraph forbids duplicates"),
`build_graph(claims) -> ClaimGraph`, `score_claims(claims) -> dict[str, ClaimScore]`,
`score_claim_dicts()`, and `assessment_summary(claims_dir) -> dict` returning
`{engine, total_claims, mean_propagated_score, claims[], graph{healthy, conflicts,
cycles, missing_dependencies}, status_counts}`. Existing tests:
`backend/tests/test_aee_core.py`.

The upstream `aee` package itself also exports (among others) `AEEEngine`,
`AEESession`, `Assessment`, `EvaluatorAdapter`, `GapEngine/GapRegister`,
`HashChainLedger`, `StressTester`, `RecoveryOperator` and a CLI with subcommands
`{assess, challenge, verify-ledger, gate, graph, gaps, demo}`.

### Cycle detection — YES, explicit

In upstream `aee/graph.py`, `ClaimGraph`:

- `cycles()` — iterative DFS (docstring notes the previous recursive version
  raised `RecursionError` past ~1,000 claims), returns normalised cycle lists.
- `topological_order()` — "Return dependency-first order; **raise when the graph
  contains a cycle**": `raise ValueError(f"claim dependency graph contains cycles: {cycles}")`.
- `missing_dependencies()`, `conflicts()`, `report() -> GraphReport`,
  `GraphReport.healthy` = no missing deps **and** no cycles **and** no conflicts.
- `aee/scoring.py::ScoringEngine.score()` calls `graph.cycles()`; on a cycle it
  skips dependency propagation and appends to every score's notes:
  `"Dependency propagation skipped: cycle(s) present: {cycles}"`.
- `aee/challenge.py` turns each cycle into a failure: `"Dependency cycle: " +
  " -> ".join(cycle)`, recovery "Break the cycle with independently observed evidence."
- `aee_core.assessment_summary()` surfaces `graph.cycles()` and computes
  `healthy = not missing_dependencies() and not cycles() and not conflicts()`.

Live proof in §5: A↔B gave `cycles= [['A', 'B', 'A']]`,
`topological_order` raised that `ValueError`, and scoring noted the skip.

### Forbidden-assumption inheritance — NO such check exists

Searched upstream `aee/*.py` and `aee_core.py` for `forbidden`: **zero hits**.
There is no forbidden-assumption list, no assumption-inheritance rule, and no
check that a claim must not inherit an assumption from a dependency:

- `aee.model.Claim` has a plain free-text field `assumptions: list[str]`
  (plus `depends_on`, `conflicts_with`, `boundary`, `falsification_tests`).
  Nothing in `graph.py`, `scoring.py`, or `challenge.py` reads `claim.assumptions`
  to block, flag, or propagate a forbidden assumption.
- What does exist, and must not be confused with it:
  1. **Dependency score capping (inheritance of weakness, not of assumptions):**
     in `ScoringEngine.score()`, for a non-cyclic graph,
     `propagated_score = min(own, weakest dependency's propagated_score)`, with note
     `"Capped by weakest dependency at {weakest:.3f}"`. Live proof in §5: a claim
     depending on a scoreless assumption claim was capped 0.25 → 0.0, while its
     graph reported `healthy= True`.
  2. **Assumption-adjacent challenges** in `aee/challenge.py::_test_claim()`:
     a claim with empty `boundary` gets a HIGH `assumption_unvalidated` failure
     ("Scope and operating assumptions are not explicit" / "Declare where, when,
     and under which assumptions the claim holds."); absolute language without a
     boundary gets the same category. That is about *undeclared* scope, not about
     inheriting a *forbidden* assumption.
  3. `aee_core.py` itself does not even populate `Claim.assumptions` —
     `claim_from_glossa()` sets `boundary=[f"testability={testability}"]`,
     evidence, `falsification_tests`, `source_ref`, `domain="indus_script"`,
     and `metadata`; Glossa fields with no AEE concept are preserved in metadata.

Conclusion for Spec 026 / RCPH transfer: any "forbidden-assumption inheritance"
rule from RCPH would be **new logic to build on top of** `depends_on` +
`Claim.assumptions`; the installed engine (1.0.4 / 1.0.2) does not implement it.
Cycle detection, missing-dependency detection, conflict detection, and
weakest-dependency score capping are available off the shelf.

## 4. Evaluator extension — what it runs, outcome scale, RCPH closure rule

### What it actually runs

The evaluator extension is a **contract, not an evaluator**. Its only executable
code is composition:

- `scripts/python/compose_results.py` (plus `scripts/bash/compose-results.sh` and
  `scripts/powershell/compose-results.ps1`) — a real stdlib CLI:
  `compose_results.py --results-dir <dir> --phase <phase> [--strategy strict|majority|optimistic] [--output <path>]`.
  Strict precedence (most severe first) in the script:
  `_STRICT_PRECEDENCE = ["block", "gather_evidence", "iterate", "clarify", "warn", "pass"]`.
  Verified working in §5.
- `commands/speckit.evaluator.run.md` is an **agent prompt procedure with no
  script**: the agent must load the schema
  (`.specify/extensions/evaluator/schemas/evaluator-result.schema.json`),
  "discover evaluators", run each, validate, and write
  `.specify/extensions/evaluator/results/<evaluator-id>-<phase>-<timestamp>.json`.
  Discovery looks for `.specify/extensions/evaluator/evaluators.yml` — **that
  file does not exist in this worktree** (only `extension.yml` is present).
  Per the command's own step 2.3: "If no evaluators are registered, produce a
  single result with `outcome: "pass"` and a note that no evaluators are configured."
  In practice the one concrete evaluator that produces contract results here is
  AEE itself, via `aee.adapters.evaluator.EvaluatorAdapter` (in the `aee` package,
  `evaluator_version = "1.0.0"`), invoked by `aee assess --evaluator-output …`
  through `run_aee.py assess`.
- `speckit.evaluator.report.md` and `speckit.evaluator.route.md` are likewise
  agent procedures (render a report / recommend a model tier) with no dedicated
  script in the extension; `speckit.evaluator.compose.md` is the one that
  delegates to `{SCRIPT}` = `compose_results.py` / `.sh` / `.ps1`.
- `examples/demo.py` is a self-contained stdlib demo (fabricates 3 evaluator
  results, composes, renders formats, shows routing) — the closest thing to a
  self-check. **It is currently broken**: see §5 (it expects a `composed_outcome`
  key that `compose_results()` no longer returns; the compose function returns
  `outcome`). The underlying `compose_results.py` CLI works correctly.

### Outcome scale — six outcomes, not pass/warn/fail

Schema enum (`evaluator-result.schema.json`, required top-level fields
`schema_version, evaluator, phase, outcome, findings`):

```
"outcome": ["pass", "warn", "iterate", "clarify", "gather_evidence", "block"]
```

Meanings (from `speckit.evaluator.run.md`): `pass` = continue; `warn` = issues
found but not blocking, continue with warnings recorded; `iterate` = return to
`target_phase`; `clarify` = pause for human input; `gather_evidence` = pause for
evidence collection; `block` = hard blocker, stop the workflow.
Finding severities: `critical|high|medium|low|info`. Finding kinds include
`unsupported_claim, contradiction, missing_evidence, ambiguous_requirement,
unverified_assertion, provenance_gap, schema_violation, policy_violation,
security_concern, coverage_gap, traceability_gap, risk_unaddressed,
assumption_unvalidated, other`.

Gate exit-code contract (from `speckit.aee.gate.md`, mirrored in the demo):
**0 for `pass` or `warn`; 1 for `iterate`, `clarify`, or `gather_evidence`;
2 for `block` or malformed input.** Verified live in §5 (`AEE gate: iterate`, exit 1).

### RCPH rule mapping

RCPH's rule as given for this transfer — *outcomes stricter than `warn` block
closure* — maps exactly onto that gate contract: `pass`/`warn` are the only
non-blocking outcomes; `iterate`, `clarify`, `gather_evidence`, and `block`
all block (exit 1 or 2). No translation layer is needed; Spec 026 should cite
the outcome by name and require composed outcome ∈ {`pass`, `warn`} for closure.

### Constitution fallback — and whether the extension commands ARE runnable here

Constitution §IV (`.specify/memory/constitution.md`):

> "Claim scoring and assessment in the core tool run on the Applied Epistemic
> Engineering library (`applied-epistemic-engineering`, the `aee` package)
> through `backend/glossa_lab/aee_core.py` — **the same library the spec-kit
> AEE extension is built on** — so specification-time and run-time epistemics
> use one engine, not two."

**Verdict: the extension commands ARE runnable in this environment**, by the
mechanism in §2b — an agent executes the Markdown command (Copilot `SKILL.md`
rendering in this worktree), which runs `run_aee.py`, which runs the `aee` CLI —
provided a venv providing `aee` is on `PATH`. This was demonstrated end-to-end in
§5, not merely inferred. They are **not** runnable as a bare shell command
(`specify` has no such subcommand; `aee` is not on the default `PATH`).
If an agent session cannot execute the Markdown commands, the constitution's
same-engine fallback is direct use of the library through `aee_core.py`
(`score_claims` / `assessment_summary` / `build_graph`), also demonstrated in §5.
The one command with no evaluator behind it by default is
`speckit.evaluator.run` in isolation (no `evaluators.yml` registered) — its
meaningful producer in this repo is `speckit.aee.assess`, which emits the
Evaluator Contract result as a by-product.

## 5. Live tests performed (all outputs in /tmp sandboxes)

### 5a. `aee_core` library test — sample claims, cycle, assumption-dependency probe

Script `/tmp/aee-test026/test_aee_core.py`, run with
`~/workspace/venvs/glossa-lab/bin/python`, `sys.path` prepended with the worktree
`backend/` (printed `aee_core file: …/glossa-lab-spec026/backend/glossa_lab/aee_core.py`).
Sample claims are the three fixtures from `backend/tests/test_aee_core.py`
(partially-supported / untested / contradicted). Key output:

```
t_supported_001 propagated= 1.0 band= high penalty= 0 notes= []
t_untested_001 propagated= 0.289375 band= low penalty= 0 notes= ['No observed supporting evidence', 'Fewer than two independent supporting sources']
t_contra_001 propagated= 0.0 band= unknown penalty= 0.75 notes= ['No observed supporting evidence', 'Fewer than two independent supporting sources', 'Contradiction penalty 0.750']
graph healthy(no deps): cycles= [] missing= {} conflicts= []
cycle graph cycles= [['A', 'B', 'A']]
topological_order ValueError: claim dependency graph contains cycles: [['A', 'B', 'A']]
cyclic score notes A: [..., "Dependency propagation skipped: cycle(s) present: [['A', 'B', 'A']]"]
assumption-dep graph: cycles= [] missing= {} conflicts= [] healthy= True
ASM1 score= 0.0 DEP1 direct= 0.25 DEP1 propagated= 0.0 DEP1 notes= ['No supporting evidence', 'Fewer than two independent supporting sources', 'Capped by weakest dependency at 0.000']
assessment_summary: {"engine": "applied-epistemic-engineering", "total_claims": 3, "mean_propagated_score": 0.429792, ...}
```

Imports cleanly; scoring orders supported > untested > contradicted as the
repo's own tests assert; cycle detection and weakest-dependency capping behave
as §3 describes; the assumption-dependency graph is reported **healthy** —
confirming there is no forbidden-assumption check.

### 5b. Extension mechanism end-to-end — `run_aee.py assess` in a disposable project root

In `/tmp/aee-proj026` with the extension's own template
(`templates/aee-claims.json`, single draft claim `REQ-LATENCY-001`) copied as
`claims.json`, and `PATH` prefixed with the glossa-lab venv:

```
$ python .specify/extensions/aee/scripts/python/run_aee.py assess --input claims.json --phase after_specify --threshold 0.70
{
  "assessment": ".specify/extensions/aee/assessments/aee-after_specify-20261011T024818Z.json",
  "evaluator_result": ".specify/extensions/evaluator/results/aee-after_specify-20261011T024818Z.json",
  "ledger": ".specify/extensions/aee/ledger/epistemic-ledger.jsonl",
  "aee_exit_code": 1
}
EXIT:1
```

The emitted Evaluator Contract result (in the sandbox only):

```json
{"evaluator": {"id": "aee", "version": "1.0.0", "name": "Applied Epistemic Engineering"},
 "phase": "after_specify", "outcome": "iterate",
 "summary": "Assessed 1 claim(s); found 0 failure mode(s); 1 claim(s) below the 0.70 confidence threshold.",
 "next_action": {"kind": "iterate", "target_phase": "specify", ...}}
```
(Claim scored `propagated_score 0.25`, band `low` — below threshold, hence
`iterate`, hence exit 1: stricter than `warn`, would block closure under the
RCPH rule.) Then the gate on that same assessment:

```
$ run_aee.py gate --input .specify/extensions/aee/assessments/aee-after_specify-*.json
AEE gate: iterate
GATE_EXIT:1
```

Negative control: the identical `run_aee.py assess` with no `aee` on `PATH`
printed `Missing required 'aee' command. Install applied-epistemic-engineering>=1.0.2,<2.`
and exited **2** — the one setup condition for the mechanism.

### 5c. `aee` CLI self-contained demo

```
$ ~/workspace/venvs/glossa-lab/bin/aee demo
{"schema_version": "1.0", "methodology_version": "1.0", "project": "demo",
 "phase": "after_specify", "outcome": "pass",
 "summary": "Assessed 1 claim(s); found 0 failure mode(s); 0 claim(s) below the 0.70 confidence threshold.", ...}
EXIT:0
```

### 5d. Evaluator demo / compose

```
$ python .specify/extensions/evaluator/examples/demo.py --output /tmp/eval-demo026
  Schema Validator: WARN (2 findings: 1 low, 1 medium)
  Epistemic Evaluator: ITERATE (3 findings: 2 high, 1 medium)
  Security Scanner: BLOCK (2 findings: 1 critical, 1 high)
  COMPOSED RESULT (strict strategy)
Traceback (most recent call last):
  File ".../evaluator/examples/demo.py", line 259, in main
    print(f"  Outcome:          {composed['composed_outcome'].upper()}")
KeyError: 'composed_outcome'
EXIT:1
```

The demo script writes its three result files, then crashes on the stale
`composed_outcome` key. Running the real compose CLI on those same files works:

```
$ python .../evaluator/scripts/python/compose_results.py --results-dir /tmp/eval-demo026 --phase after_specify --strategy strict --output /tmp/eval-demo026/composed.json
Composed result written to /tmp/eval-demo026/composed.json
EXIT:0
{"evaluator": {"id": "composed", "version": "1.0", "name": "Composed (strict)"},
 "phase": "after_specify", "outcome": "block",
 "summary": "3 evaluator(s) ran. Outcomes: epistemic=iterate, schema-validate=warn, security-scan=block. 7 finding(s) total.", ...}
```

Strict composition correctly lets the single `block` dominate `iterate`/`warn`.

## Bottom line for Spec 026

1. Tooling is present and current: specify 1.0.10, aee extension 1.1.0,
   evaluator extension 1.0.0, `aee` library 1.0.4 (glossa-lab venv) / 1.0.2
   (spec-kit venv).
2. Extension "commands" are agent-executed Markdown (Copilot `SKILL.md` in this
   worktree), backed — for AEE — by `run_aee.py` → the `aee` CLI, and — for the
   evaluator — mainly by the contract + `compose_results.py`. Runnable here
   (proven), conditional on `aee` being on `PATH`.
3. Specs 024/025 left no assessment artifacts; hook execution for them is
   unevidenced, not merely unfiled.
4. `aee_core.py` is a clean, tested adapter over the same engine; cycle /
   missing-dependency / conflict detection and weakest-dependency score capping
   are built in. **Forbidden-assumption inheritance is not implemented
   anywhere in the installed engine or the adapter** — RCPH's version of that
   rule would be new code.
5. Evaluator outcomes are the six-value scale
   `pass|warn|iterate|clarify|gather_evidence|block`; the gate contract
   (0 = pass/warn, 1 = iterate/clarify/gather_evidence, 2 = block) already
   implements "stricter than warn blocks". Known defect: evaluator
   `examples/demo.py` crashes with `KeyError: 'composed_outcome'` after writing
   its sample results; `compose_results.py` itself is unaffected.
