# Implementation Plan: Spec 076 — The Projected-Constraint Corpus Model: Demanding What Must Be True of the Missing Signs

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/076-projected-constraint-corpus-model/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Status: FROZEN at the freeze act of 2026-10-26** (see
`freeze.md` in this directory). This spec carries the
M12 design (method M12 of the advance-to-decipherment
plan; design draft of 2026-10-26, SHA-256 8945399d…)
into the programme's frozen-contract form. The design
text is carried as written except where this spec's
§0 records a freeze-fixed completion — a place the
design expressly left open for the freeze to close
(the shuffle seed, the step-3 coding rules, the
resolution-value operationalisation, the A-KEY
clarification). Every such completion is stated in
§0 and ruled in the adjudicat

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/076-projected-constraint-corpus-model/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 8 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/076-projected-constraint-corpus-model/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── pilot-record.md
├── spec.md
├── tasks.md
├── aee/
├── gate-records/
├── pilot/
```

## Phases (from this spec's own tasks/spec structure)

- 0. Freeze-fixed completions (ruled at adjudication DD-076-3)
- 1. Purpose
- 2. The unknowns — six categories, counted from the records
- 3. The honesty architecture — what "must" is allowed to mean
- 4. Constraint sources — named, audited, and assigned a layer
- 5. Frames and keying — what this method trusts, and why
- 6. Outputs — the register, the possibility sets, the ranking
- 7. Worked miniature example — real counts, recomputed for the design
- 8. Pilot design — with the null built in, and the bars stated now
- 9. Feasibility verdict — what scale of exact work is real, and what is not
- 10. Relationship map — what this composes with, and what it must not touch
- 11. Claims of this spec
- 12. What this spec does not establish
- 13. Cost and dependencies
- 14. The S4 note (scan of 2026-10-26)
