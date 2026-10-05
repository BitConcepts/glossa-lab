# 001 — Tasks

Baseline adoption tasks (spec-kit + AEE migration, 2026-10-05):

- [x] T001 `specify init` (v1.0.10, copilot, sh) into the existing repo
- [x] T002 Install AEE + evaluator extensions from local clones (`--dev`),
      vendored as real files (no gitlinks, no nested `.git`/venvs)
- [x] T003 Ratify `.specify/memory/constitution.md` from existing governance
- [x] T004 Write this as-built baseline spec (spec / plan / tasks)
- [x] T005 Remove specsmith as active tooling (skills, `scaffold.yml`,
      tracked `backend/.specsmith/` runtime state)
- [x] T006 Move runtime rate-limit state from `.specsmith/` to
      `.glossa-state/` (`fetchers/base.py`, `model_intelligence.py`),
      gitignore the new dir
- [x] T007 Update `AGENTS.md` to the spec-kit flow; append LEDGER entry
- [x] T008 (Stage 2) AEE core adapter `aee_core.py` + wiring + tests —
      tracked in this baseline's plan; executed in the same migration PR
- [x] T009 (Stage 3) GDELT ngrams fetcher — tracked in
      `specs/002-gdelt-ngrams-and-frontier-methods/`
