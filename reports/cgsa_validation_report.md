# CGSA Pipeline Validation Report
Generated: 2026-04-22T18:44:49Z

## Phase 1 Validation Checkpoint

- ✅ Total unique signs in inventory: 803
  (threshold: >300 — PASS)
- P-signs (Parpola): 396
- Y-signs (Yajnadevam/ICIT): 407
- Signs appearing in corpus: 589

## Phase 3 Validation
- ✅ Canonical registry: 803 entries with UUIDs
- ✅ Crosswalk: Parpola ↔ Wells ↔ Mahadevan

## Phase 4 Validation
- ✅ Co-occurrence graph: 389 nodes, 2660 edges

## Phase 5 Validation (FAILURE CONDITIONS CHECK)

- Best k: 40
- Largest cluster: 12/160 = 7.5%
  (PASS: no collapse)
- Entropy reduction: 0.3204
  (PASS: reasonable reduction)

## Phase 6 Validation
- Raw sequence entropy: 10.5268 bits
- Class sequence entropy: 10.1366 bits
- Reduction: 3.7% (PASS)
- Distinct sequences preserved: 1938 raw → 1677 class

## CRITICAL RULES COMPLIANCE
- [x] NO symbol mapping to alphabet characters
- [x] NO sign space reduction (all sign IDs preserved in registry)
- [x] NO sign collapse (each distinct sign has its own registry entry)
- [x] Inscription boundaries maintained throughout
- [x] Sequence integrity: sign order preserved in all outputs

## Overall Status
PASS