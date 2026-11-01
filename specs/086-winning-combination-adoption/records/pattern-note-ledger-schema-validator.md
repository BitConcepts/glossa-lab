# Pattern note — Pin the ledger's schema and gate it in CI (the D-A pattern, generalized)

**From:** Glossa-Lab (Spec 086, Stage 1 closeout, task T105)
**Date:** 2026-11-01
**For:** the framework chats — RCPH / projected-constraints
(the framework's home) and the Breaking-Point Atlas
(Axiovex Systems chat). Delivered under the harmonization
rule (winning-combination pattern, point 7).

## The improvement

When a program adopts the winning combination, its claims
ledger is a hand- and machine-written artifact that every
downstream layer trusts. Glossa-Lab's experience (Spec 029
decision D-A, ratified 2026-10-12 for the anchors file) is
that an unpinned record format accretes incompatible field
shapes silently — the anchors file had reached 56 distinct
shapes before D-A pinned it. The ledger is the same kind of
artifact at larger consequence, so Spec 086 generalized the
D-A pattern to it from the start:

1. **A declared schema, versioned and pinned beside the
   artifact** (`ledger-schema v1`: a JSON Schema file +
   a human document stating each field's provenance rule,
   kept in the ledger's own directory).
2. **A validator in the intake path and in CI** that
   enforces the schema on every entry, recomputes the
   proposition fingerprint rather than trusting the stored
   value, and refuses unprovenanced content loudly — a
   refusal writes nothing and names the defect.
3. **Coverage counts published on every validation run** —
   for us, the falsifier-coverage count of the ledger — so a
   pattern-required field the legacy population lacks shows
   up as a standing number, never as silence and never as
   invented content.

## Why it is an extension, stated plainly

D-A as ratified names one artifact (the anchors file). The
adoption order's shorthand ("the pinned-schema validator
pattern (D-A)") generalizes it. Glossa-Lab follows the
decision as written, labels this generalization an
**extension**, and offers it back through the harmonization
path rather than letting a local dialect form silently. If
the framework wants the generalized naming, that is an
amendment to the canonical pattern note, ratified by the
owner — this note is the proposal for it.

## Evidence from the build

- The schema + validator landed before the migrated ledger
  existed (Stage 1, tasks T101/T102 before T104), so the
  migration itself ran through the gate it created.
- Teeth tests: a malformed entry, a duplicate-fingerprint
  entry, an authorless explanation, an untraced falsifier,
  and a falsifier-less new claim are each refused with
  nothing written.
- First full run over the built ledger (871 entries):
  schema valid throughout; falsifier coverage published as
  831 of 840 claim entries (bundle population 817/817;
  extracted population 14/23 — the 9 nulls are a counted,
  named gap, backfillable only by human-authored
  reclassification).
