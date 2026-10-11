# Spec 026 — Requirements Checklist

## Specification quality

- [x] CQ-1 No implementation details leak into spec.md beyond
      named machinery (framework026 module, register files)
      whose construction the spec itself mandates.
- [x] CQ-2 All sections completed; epistemic boundaries stated
      (spec §9, H13) incl. assumptions, adversarial challenges,
      and belief-artifact dependencies.
- [x] CQ-3 Requirements are testable: FR-026-1…8 each name an
      inspectable artifact or a mechanical test.
- [x] CQ-4 Success criteria are measurable (register row count =
      inventory count; rerun set executed or hard-stopped;
      foundation 0 failures; anchors byte-identical).

## Requirement completeness

- [x] CR-1 Transfer covers all twelve RCPH principles +
      the non-transfer section (FR-026-1).
- [x] CR-2 Claim machinery covers cycles AND forbidden-assumption
      inheritance, with planted-case tests (FR-026-2).
- [x] CR-3 Freeze machinery covers definition tamper AND source
      tamper (FR-026-3).
- [x] CR-4 AEE/evaluator stages enumerated with the governing
      threshold (stricter-than-warn blocks) (FR-026-4).
- [x] CR-5 Criteria frozen before register; register before
      reruns (FR-026-5) — enforced by PR stage order.
- [x] CR-6 Rerun discipline incl. H23 five-step gate, no-tuning
      rule, comparison format (FR-026-6).
- [x] CR-7 Historical assessments for status-changed items;
      originals untouched (FR-026-7).
- [x] CR-8 Closeout gates incl. no publication (FR-026-8).

## Feature readiness

- [x] CF-1 Rerun phase numbers reserved (142+) without
      colliding with existing artifacts (max existing = 141).
- [x] CF-2 Hard stops named in advance: unhashable rerun input →
      evidenced hard-stop, never substitution.
- [x] CF-3 Dependencies identified: inventory (working/),
      transfer map, tooling record — all on disk.
