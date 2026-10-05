# 001 — Plan (as-built architecture)

The platform as built:

```text
[ Tray ] ─────┐
              │
[ Frontend ] ─┼──→ [ Backend Service (FastAPI) ] ──→ [ Pipelines / Jobs / Models ]
              │              │
[ CLI / Dev ] ┘         [ SQLite DB ]
                              │
                    [ Provider Registry ] ──→ [ Cloud / Ollama / vLLM ]
```

Key principles (from README / `docs/architecture.md`):
- The backend is the source of truth; all communication through explicit
  REST APIs; service lifecycle is deterministic and observable (every
  background process logs START/COMPLETE).

Epistemic layer (Stage 2 of the spec-kit + AEE migration):
- `backend/glossa_lab/aee_core.py` adapts Glossa's extracted-claims JSON
  (`glossa-indus/claims/extracted_claims/*.json`) onto the Applied
  Epistemic Engineering library (`aee` package: `Claim`, `Evidence`,
  `ClaimGraph`, `ScoringEngine`) and surfaces AEE-backed scoring through
  the Indus evidence API as additive fields. The AEE library's native
  model has no field for Glossa's `falsification_condition` text, so the
  adapter preserves it in its own mapping layer (documented in the module
  docstring) rather than dropping it.

Development flow:
- spec-kit (`specify` 1.0.10, copilot integration) with the AEE and
  evaluator extensions vendored as real files under
  `.specify/extensions/`; hooks in `.specify/extensions.yml` run AEE
  assessment after specify/plan/tasks/implement and gap regeneration
  after verify.
