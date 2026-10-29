# Implementation Plan: Spec 077 — Three-Witness Sign-List Triangulation + Token 999 (Method M7)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/077-signary-triangulation/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**FROZEN — 2026-10-26.** This is the M7 design draft of
2026-10-25 (program goal record,
`2026-10-25-spec-draft-m7-signary-triangulation.md`), as
amended by that draft's own 2026-10-25 iteration-pass
amendment, carried into frozen form. The draft's sections
are preserved in substance; the freeze-fixed completions
of §0 below are the only additions, and each is marked as
a completion, not draft text. The freeze record is
`freeze.md` / `freeze.json` in this directory; the
drafting rulings are `adjudication.md` (DD-077-1 …
DD-077-8).

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/077-signary-triangulation/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 10 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/077-signary-triangulation/
├── adjudication.md
├── build_claims.py
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── outcome.md
├── spec.md
├── step0-record.md
├── tasks.md
├── aee/
├── gate-records/
```

## Phases (from this spec's own tasks/spec structure)

- 0. Freeze-fixed completions
- 1. Purpose
- 2. Claims
- 3. Inputs (pinned at this freeze)
- 4. Method
- 5. Verdict bands
- 6. Sensitivities
- 7. What this spec does not establish
- 8. Execution
- 9. Cost / dependencies
