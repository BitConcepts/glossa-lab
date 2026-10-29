# Implementation Plan: Spec 071 — Hunt Sky-Signs Endings Successor: Sky Signs at the Ends of Texts, on the Shakti Corpus (Re-scoped Successor to Spec 050, Design D-13)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/071-hunt-sky-signs-successor/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Design source:** D-13 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-13), as frozen in **Spec 050**
(`specs/050-hunt-sky-signs-endings/spec.md` on
`main`, read in full at this draft). Spec 050
froze on 2026-10-21 (contract anchor: Spec
045's freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`)
and closed as a not-run dependency closure,
because no Asset A digest exists: its gate 0.1
asserts an Asset A digest, and Asset A was
never built. This spec is Spec 050's
**re-scoped successor on the Shakti 

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/071-hunt-sky-signs-successor/`); runtime state in `.glossa-state/` (never committed)

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
specs/071-hunt-sky-signs-successor/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── tasks.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order
