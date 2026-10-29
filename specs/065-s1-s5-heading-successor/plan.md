# Implementation Plan: Spec 065 — The Two Unlocated Rows of Spec 057: Search the Acquired Documents' Own Text Layers for the Heading (Successor Recovery Act for S-1 and S-5)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/065-s1-s5-heading-successor/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Predecessor:** Spec 057
(`specs/057-five-sources-heading/`), executed
2026-10-21 as Phase-419, closed headline
class **C — PARTIAL RECOVERY WITH UNLOCATED
SOURCES**, counts *r* = 2, *e* = 1, *u* = 2.
Its freeze digest is
`237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9`
(pinned at §2.3).

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/065-s1-s5-heading-successor/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 12 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/065-s1-s5-heading-successor/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── extraction-S1.txt
├── extraction-S5.txt
├── freeze.json
├── freeze.md
├── intake-S1.json
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── tasks.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Drafting (this draft)
- Lifecycle (freeze gate)
- Execution (NOT authorised by this draft; every step OWNER-APPROVAL)
