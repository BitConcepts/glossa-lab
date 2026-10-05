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
  the Indus evidence API as additive fields. `falsification_condition`
  maps natively onto AEE's `Claim.falsification_tests`; Glossa-only
  fields AEE has no concept for (claim-type taxonomy, testability,
  quote fragments, sign lists, `confidence_in_source`) are preserved in
  the adapter's mapping layer via `Claim.metadata` / `source_ref`, as
  documented in the module docstring.

Development flow:
- spec-kit (`specify` 1.0.10, copilot integration) with the AEE and
  evaluator extensions vendored as real files under
  `.specify/extensions/`; hooks in `.specify/extensions.yml` run AEE
  assessment after specify/plan/tasks/implement and gap regeneration
  after verify.
