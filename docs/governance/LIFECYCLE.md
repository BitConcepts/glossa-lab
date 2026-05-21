# Project Lifecycle — AEE Development Phases

This project follows the 7-phase Applied Epistemic Engineering (AEE) development lifecycle. Each phase has readiness checks that must pass before advancing.

**Current phase:** 🌱 **Inception** (`inception`)

## Phases

1. 🌱 **Inception** — Governance scaffold, AGENTS.md, project type established
2. 🏗 **Architecture** — ARCHITECTURE.md written, components defined, key decisions sealed
3. 📋 **Requirements** — REQUIREMENTS.md populated, stress-tested, equilibrium reached
4. ✅ **Test Specification** — TESTS.md covers all P1 requirements, coverage ≥ 80%
5. ⚙ **Implementation** — Code development loop; audit passes; ledger updated each session
6. 🔬 **Verification** — Epistemic audit passes threshold; trace vault sealed; export clean
7. 🚀 **Release** — CHANGELOG updated; release tag created; compliance report filed

## Phase Flow

```
inception → architecture → requirements → test_spec → implementation → verification → release
                                                                                        ↓
                                                                                  (next cycle)
```

## Advancing Phases

Check readiness: review the Phase Artifacts checklist below against the current codebase.
Advance to next: update `scaffold.yml` `current_phase` field and record in `LEDGER.md`.
Force-advance: add a ledger note explaining the override rationale.

All Phase Artifacts for the current phase must exist and be committed before advancing.

## Phase Artifacts

Each phase produces specific artifacts:

- **Inception**: `scaffold.yml`, `AGENTS.md`, `LEDGER.md`
- **Architecture**: `docs/ARCHITECTURE.md`, trace vault seal
- **Requirements**: `docs/REQUIREMENTS.md`, `docs/TESTS.md`
- **Test Specification**: TESTS.md with ≥ 80% REQ coverage
- **Implementation**: Code, updated LEDGER.md, passing audit
- **Verification**: Epistemic audit, trace vault seals, export report
- **Release**: `CHANGELOG.md`, release tag, compliance report
