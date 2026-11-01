# Implementation Plan: Spec 078 — The Bridge Redesign: A Two-Axis Vocabulary for the Projected-Constraint Corpus Model (Method M13)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/078-projected-constraint-bridge-redesign/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Status: FROZEN at the freeze act of 2026-10-26** (see
`freeze.md` in this directory). This spec carries the
M13 design (method M13 of the advance-to-decipherment
plan; design draft of 2026-10-26, SHA-256 8bb02c07…)
into the programme's frozen-contract form. The design
text is carried as written except where this spec's
§0 records a freeze-fixed completion — a place the
design expressly left open for the freeze to close
(the counted population stated mechanically, the
blindness protocol stated in full, the pattern clause
operationalised, the pilot execution order). Every
such completion is st

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/078-projected-constraint-bridge-redesign/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 9 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/078-projected-constraint-bridge-redesign/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── pilot-record.md
├── spec.md
├── tasks.md
├── aee/
├── gate-records/
├── pilot/
```

## Phases (from this spec's own tasks/spec structure)

- 0. Freeze-fixed completions (ruled at adjudication DD-078-3)
- 1. Purpose — the redesign target is the bridge, not the census
- 2. What exactly died in 076, named part by part
- 3. The two-axis vocabulary
- 4. A-FACE-2 — the successor assumption, filed as a claim
- 5. The coding rules — NC-1…NC-8
- 6. Worked re-codings — the pilot's three texture cases, under the new rules
- 7. Successor pilot design — the bridge, tested on its own standards
- 8. What a pass would license — the register under the new vocabulary
- 9. Relationship map — inheritance and fences
- 10. Claims of this spec
- 11. What this spec does not establish
- 12. Cost and dependencies
- 13. The S4 note (queued at the rerun audit of 2026-10-26, F4)
