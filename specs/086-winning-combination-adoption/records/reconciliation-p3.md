# Reconciliation — P3 research-check annotations (Spec 086 Stage 1, T104)

Migration run: `migration-2026-11-01-stage1`, 2026-11-01. Source store:
`glossa-indus/claims/research_checks/` (31 sidecar
files, read-only). The Spec 025 contract stands untouched:
sidecars stay advisory and never modify a claim; what enters
the ledger is one annotation entry per sidecar, recording the
sidecar's id, content hash, the claim it bears on, and the
bearing its own record states.

## Headline counts

| Measure | Count |
|---|---|
| Sidecar files in | 31 |
| Annotation entries out | 31 |
| Annotations whose target claim is a merged instance (canonical entry named in `canonical_claim_id`) | 8 |
| Sidecars with a verdict | 0 |

Every annotation's `canonical_claim_id` resolves to a P1
canonical ledger entry (validator-checked). No claim's status,
stage, or score is changed by any annotation.
