# Implementation Plan: Spec 074 — Hunt Opening Signs on the Repaired Keying Surface: The Opening Signs Are the Animal Signs, on the Shakti Corpus (Successor to Spec 070, Design D-06)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/074-hunt-opening-signs-repaired-surface/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Design source:** D-06 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-06), as drafted in **Spec 049**, re-scoped
in **Spec 070** (frozen 2026-10-22; freeze
digest
`763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`),
and executed as Phase 433 (closure record:
`specs/070-hunt-opening-signs-successor/outcome.md`;
machine record `reports/phase433_results.json`).
This spec carries Spec 070's design **verbatim
in substance** — the same claim, the same
falsifier, the same §2 battery, the same §4
test and §4.3 preceden

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/074-hunt-opening-signs-repaired-surface/`); runtime state in `.glossa-state/` (never committed)

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
specs/074-hunt-opening-signs-repaired-surface/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── step0-record.md
├── tasks.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order
