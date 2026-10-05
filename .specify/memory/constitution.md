# Glossa Lab Constitution

Ratified: 2026-10-05 (codifies the standing governance the project was built
under — `docs/governance/`, `AGENTS.md`, `CITATIONS.md`, `ATTRIBUTION.md` —
on adoption of the spec-kit + AEE spec-driven development flow, replacing
specsmith as the active governance tooling).

## I. Citation and provenance discipline

- Every data file in the pipeline has a citation traceable to
  `CITATIONS.md`. No uncited data enters the pipeline; zero tolerance for
  uncited material (see `ATTRIBUTION.md`).
- Contributions from private correspondence that have not been
  independently published must not appear in any tracked file without
  explicit prior consent.

## II. The ledger

- `LEDGER.md` is append-only and is the sole continuity authority across
  sessions. No ledger entry = work not done.
- Historical ledger entries are never rewritten, even when the tooling
  they name is later retired; corrections and migrations are recorded as
  new entries.

## III. The foundation-check gate

- `backend/scripts/foundation_check.py` must PASS (0 failures) before any
  external communication or publication, and after any change touching
  anchor data, confidence promotions, language models, or phase results
  (governance rule H21).
- The foundation check guards anchor data, grammar metrics, and sign
  accounting against regressions; a failing check blocks the commit that
  caused it, not a later one.

## IV. Falsifiable-claims discipline

- Decipherment claims are stated as falsifiable hypotheses with explicit
  falsification conditions, confidence levels, and evidence basis. A claim
  without a stated way to be wrong is not a Glossa claim.
- Epistemic boundaries are declared up front (governance rule H13):
  assumptions, adversarial challenges, and low-confidence dependencies are
  written down, not discovered later.
- Claim scoring and assessment in the core tool run on the Applied
  Epistemic Engineering library (`applied-epistemic-engineering`, the
  `aee` package) through `backend/glossa_lab/aee_core.py` — the same
  library the spec-kit AEE extension is built on — so specification-time
  and run-time epistemics use one engine, not two.

## V. Public / private boundary

- This is a public open-source repository. Private correspondence lives
  only in `.correspondence/` (gitignored, never pushed). No third-party
  email addresses, private drafts, or conversation logs in tracked files
  (governance rule H24).
- No secrets in code or tracked files, ever: API keys resolve through the
  settings store / environment, and credential files (`data/.keys.json`,
  `*.pem`, `*.key`) are gitignored.

## VI. AI disclosure

- All AI-assisted work is disclosed in publications and in the ledger.
  Statistical tests are designed and interpreted by the author; AI
  tooling is used for scripting, data management, and literature search.
- AI-generated or AI-assisted changes state that plainly in the ledger
  entry that records them.

## VII. Spec-driven development

- Non-trivial work follows the spec-kit flow: `specs/NNN-name/`
  (spec.md / plan.md / tasks.md, sequential numbering), with AEE
  assessment hooks (`.specify/extensions.yml`) challenging each phase.
- Graph-first experiments (governance rule H15/H23): new research phases
  are registered as experiment-graph nodes before their scripts run.
- Runtime agent/governance state lives in gitignored local directories
  (`.glossa-state/`, `.chronomemory/`, `.correspondence/`), never in
  tracked files and never in `.specify/`, which is shared project
  configuration.

## VIII. Verification

- Changes are verified before they are reported done: relevant backend
  tests pass, ruff is clean on changed Python files, and the foundation
  check passes when the change touches research state.
- Version strings are not hardcoded outside `pyproject.toml`
  (governance rule H10); documentation refers to the package version
  dynamically.
