# DoF Extraction Report (Phase 6)
Generated: 2026-04-22T18:44:49Z

## Sequence Entropy Reduction

- Raw sign sequence entropy: 10.5268 bits
- Structural class sequence entropy: 10.1366 bits
- Entropy reduction: 0.3901 bits (3.7%)
- Distinct raw sequences: 1938
- Distinct class sequences: 1677

A positive entropy reduction means structural classes capture real
regularities — inscriptions become more predictable when described
in terms of structural classes rather than raw sign IDs.

## Structural Slot Occupancy

Which cluster classes dominate each slot (0=initial, 1=internal, -1=terminal):

**INITIAL slot**: {35: 942, 10: 508, -1: 286, 31: 205, 30: 166, 7: 149, 29: 96, 26: 55}
**INTERNAL slot**: {-1: 1015, 25: 693, 33: 629, 2: 612, 11: 576, 8: 509, 35: 419, 1: 413}
**TERMINAL slot**: {-1: 657, 8: 304, 21: 274, 11: 250, 25: 156, 1: 142, 39: 131, 22: 102}

## Dominant Prefix Clusters (initial position)
  {35: 942, 10: 508, -1: 269, 31: 205, 30: 166, 7: 149, 29: 96, 26: 55, 25: 34, 37: 29}

## Dominant Suffix Clusters (terminal position)
  {-1: 657, 8: 304, 21: 274, 11: 250, 25: 156, 1: 142, 39: 131, 22: 102, 17: 94, 27: 89}

## Recurrent Structural Templates (class-space, count ≥ 3)

  - [33, 21]: 278 times
  - [35, 20]: 216 times
  - [10, 35]: 166 times
  - [35, 11]: 142 times
  - [8, 11]: 132 times
  - [25, 8]: 117 times
  - [35, 1]: 114 times
  - [25, 33]: 114 times
  - [8, 33]: 114 times
  - [35, 25]: 114 times
  - [31, 11]: 103 times
  - [11, 8]: 101 times
  - [10, 25]: 99 times
  - [7, 35]: 95 times
  - [11, 2]: 94 times
  - [25, 25]: 92 times
  - [11, 25]: 88 times
  - [35, 13]: 83 times
  - [33, 39]: 83 times
  - [35, 31]: 82 times

## Interpretation
With k=40 structural classes, inscriptions can be described
as combinations of class slots (prefix/root/suffix patterns).
This is the structural DoF schema — NOT a phonetic mapping.

Next step: apply DoF schema to refine latent class assignments
and test cross-site stability of structural templates.