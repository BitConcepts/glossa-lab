# Hard Rules and Stop Conditions

## Hard Rules

These rules are non-negotiable. Violation of any hard rule is a stop condition.

### H1 — Ledger required
No ledger entry = work not done.

### H2 — Proposal required
No proposal = no execution.

### H3 — Cross-platform awareness
All work must consider every target platform (Windows, Linux, macOS). If a platform is unsupported or deferred, that must be stated explicitly.

### H4 — Environment isolation
No system-dependent assumptions. Virtual environments required. No reliance on global interpreters or system packages.

### H5 — Explicit startup
No hidden service logic. All startup behavior must be documented and inspectable.

### H6 — No silent scope expansion
If the task grows beyond the proposal, stop and re-propose.

### H7 — No undocumented state changes
Every file creation, modification, or deletion must be traceable to a proposal and recorded in the ledger.

### H8 — Documentation is implementation
Architecture-affecting changes MUST update relevant docs in the same work cycle.

### H9 — Execution timeout required
All agent-invoked commands MUST have a timeout. No command may run indefinitely. If a command hangs, it must be killed, recorded in the ledger, and escalated after one retry.

### H10 — No hardcoded versions
Version strings MUST NOT be hardcoded in documentation, tests, or source code outside of `pyproject.toml`. Use `importlib.metadata.version()` at runtime. Use `{{ version }}` placeholders in documentation resolved at build time.

### H11 — No unbounded loops or blocking I/O without a deadline
Every loop or blocking wait in agent-written scripts and automation MUST have:

- An explicit deadline or iteration cap (e.g. a `deadline` timestamp, a `max_attempts` counter, or a `timeout` parameter).
- A fallback exit path that executes when the deadline is reached.
- A diagnostic message emitted if the timeout fires (self-diagnosing failures).

Examples of violating patterns: `while True:` / `while ($true)` / `for (;;)` with no deadline guard; serial-port or I/O polling loops with no deadline; `sleep` inside a loop with no termination condition. Review all scripts under `scripts/` for these patterns before committing.

### H12 — Windows multi-step automation via .cmd files
On Windows, multi-step or heavily-quoted automation sequences MUST be written to a temporary `.cmd` file and executed from there. Do NOT emit these as inline shell invocations or as `.ps1` files unless there is a concrete PowerShell-only requirement. Inline multi-line quoting on Windows is fragile and causes avoidable hangs.

### H13 — Epistemic Boundaries Required
All proposals MUST state their epistemic boundaries. A proposal without explicit assumptions is a stop condition, not a warning. Before executing, ask:
- What BeliefArtifact IDs does this proposal rely on?
- What are the hidden assumptions?
- What adversarial challenge could break this proposal?
- Are any P1 requirements in scope and at LOW confidence?

Hidden assumptions are not acceptable. Declare all epistemic boundaries in the `Assumptions:` field of every proposal.

### H14 — No direct email
Agents MUST NOT send, compose, or trigger emails to any external party directly (e.g. via SMTP, API calls, or shell commands). All outbound email MUST be routed exclusively through the glossa-lab backend email system, and only to recipients configured in the project email report settings. This applies to scholar outreach, collaboration messages, and any other external communication. Violation is an immediate stop condition.

### H15 — Graph-first: no new hardcoded experiments
All new research phase experiments MUST be expressed as `AtomicNodeDef` nodes in a dedicated `experiment_graph_phaseNN_MM.py` module. Agents MUST NOT:
- Define new `ExperimentBase` subclasses for phase research scripts.
- Hardcode anchor dicts, report titles, or phase logic inside `experiment_graph.py` directly.
- Run a phase script before its graph module is created and registered (see H23).

The only valid pattern is: phase script → reads pre-computed JSON report; graph node → loads that report or runs script via `subprocess`. Every phase must be navigable from the Experiment Builder palette. Violation is an immediate stop condition.

### H16 — No hardcoded user data in experiments
Experiments MUST NOT hardcode corpus data, language model data, anchor sets, or report templates that should be user-configurable. All such data MUST be loaded from the database (via `CorpusLM`, `AnchorSetLoader`, `ReportGenerator`) or from registered JSON files. New experiments that bypass the database for user-owned data violate the H16 user-definable principle and must be refactored before merging.

### H20 — GPU enforcement in phase scripts
All Indus Decipherment phase scripts that run SA or compute-intensive analysis MUST:
- Import `torch` and detect `torch.cuda.is_available()`.
- Expose `gpu_device` in their JSON report output.
- Use `BigramScorer` from `glossa_lab.pipelines.decipher` for SA (auto-selects CUDA).
- Print a WARNING (never silently fall back) if GPU is not available.

Foundation Check NEW-G (`GPU CUDA available`) MUST pass. Silent CPU fallback is forbidden.

### H21 — Foundation check gate
`backend/scripts/foundation_check.py` MUST be run and show `0 failures` after any phase that:
- Modifies `backend/reports/INDUS_FINAL_ANCHORS.json`
- Promotes anchor confidence (LOW→MEDIUM or MEDIUM→HIGH)
- Updates any `dravidian_*.json` language model
- Adds new `phase*.json` result files to `reports/`

No commit touching anchor or phase data may be pushed with a failing foundation check. This check is the primary regression guard for the decipherment state.

### H24 — No personal information or private correspondence in the repository
This is a public open-source repository. Agents and contributors MUST NOT commit, push, or otherwise add to any tracked file:

- Email addresses of any third party (collaborators, reviewers, institutional contacts)
- Private email drafts, correspondence threads, or outreach content
- Personal contact details (phone numbers, physical addresses, institutional office addresses)
- Conversation logs, chat exports, or academic-platform message exports
- Any document whose primary content is a communication between named individuals

**Permitted exceptions (own professional contact only):**
- The author's own professional email (`tpierson@bitconcepts.tech`, `noreply@bitconcepts.tech`) in `CITATION.cff`, User-Agent strings, and the preprint author block is acceptable as it is already public academic attribution.

**Where private correspondence belongs:**
- Store it in `.correspondence/` at the repo root, which is gitignored and never pushed.
- The `.correspondence/` directory holds the canonical private context store. AI agents reading this rule must write all correspondence summaries there and never to tracked files.

**Pre-commit enforcement:**
The pre-commit hook at `.git/hooks/pre-commit` must block staging of files matching `*.eml`, `*_email.md`, `*_email.py`, `send_*_email.py`, and any file in `.correspondence/`. This rule supersedes convenience — no exception for "just a draft" or "it's my own email only."

Violation is an immediate stop condition and requires a history-rewrite (`git filter-repo`) if the content reached a remote.

### H23 — Mandatory 5-step experiment gate
Before running ANY new phase script, the following 5 steps are MANDATORY in order:
1. **Write the script** (`backend/scripts/phaseNN_name.py`)
2. **Create the graph module** (`backend/glossa_lab/experiment_graph_phaseNN_MM.py`) with `AtomicNodeDef` nodes
3. **Register in `experiment_graph.py`** via a `try/except` import block
4. **Verify registration**: `python -c "from glossa_lab.experiment_graph import ATOMIC_NODES; assert 'NodeID' in ATOMIC_NODES"`
5. **Run the script**

Skipping steps 2–4 before step 5 is a cardinal H23 violation. Running a script before its graph node exists means the phase is unnavigable in the Experiment Builder and violates R17.

---

## Stop Conditions

Agents MUST stop and request clarification if ANY of the following are true:

- Missing inputs (files, context, or dependencies not available)
- Unclear state (ledger is inconsistent or missing)
- Undocumented platform assumptions
- No proposal has been approved
- No ledger path exists (LEDGER.md missing or unwritable)
- Requirement-without-test detected
- Test-without-requirement detected
- Architecture contradicts requirements
- Proposed work would violate a hard rule
- Proposed work would silently expand scope
- **Logic Knot detected** (conflicting accepted requirements without a resolution path)
- **P1 belief artifact below MEDIUM confidence** (H13 stop condition)
- **Trace chain integrity failure** (verify ledger chain manually against git log)
