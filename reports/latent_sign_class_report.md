# Latent Sign Class Report
Generated: 2026-04-22T17:16:01Z
**Site scope**: Mohenjo-daro only. Clustering is provisional and site-limited.

---

## Important Caveats

- Classes are derived from positional behavior only.
- Visual similarity has NOT been incorporated (requires image data).
- These are CANDIDATE STRUCTURAL CLASSES, not phoneme assignments.
- Multi-site data will likely refine class boundaries.
- No class should be treated as final without visual crosswalk confirmation.

---

## Classification Method

Feature vector per sign: (freq, start_rate, end_rate, internal_rate)
Classification: threshold rules on positional rates.
Class labels are structural descriptors, not linguistic categories.

## Class Inventory

- Total signs classified: 182
- Unigram entropy (sign ID space): 7.5078 bits
- Class entropy: 2.1078 bits
- Entropy reduction from sign→class: 71.9%

### Class distribution

  - HAPAX: 77 signs
  - MEDIAL_STRONG: 48 signs
  - LOW_FREQUENCY: 32 signs
  - INITIAL_STRONG: 9 signs
  - MIXED: 8 signs
  - TERMINAL_STRONG: 7 signs
  - BIMODAL_INIT_TERM: 1 signs

---

## Per-Class Profiles

### BIMODAL_INIT_TERM (1 members)
  - Mean end_rate: 0.5
  - Mean start_rate: 0.5
  - Mean internal_rate: 0.0
  - Variance (end_rate): 0.0
  - Members: P320

### HAPAX (77 members)
  - Mean end_rate: 0.4286
  - Mean start_rate: 0.0909
  - Mean internal_rate: 0.4805
  - Variance (end_rate): 0.2449
  - Members: P007, P010, P012, P014, P020, P022, P023, P032, P037, P038, P041, P044, P047, P048, P053, P054, P061, P065, P070, P071, P083, P084, P089, P094, P099, P136, P156, P166, P170, P177...

### INITIAL_STRONG (9 members)
  - Mean end_rate: 0.0486
  - Mean start_rate: 0.8575
  - Mean internal_rate: 0.0939
  - Variance (end_rate): 0.0101
  - Members: P000, P001, P004, P013, P051, P098, P217, P301, P324

### LOW_FREQUENCY (32 members)
  - Mean end_rate: 0.2187
  - Mean start_rate: 0.0469
  - Mean internal_rate: 0.7344
  - Variance (end_rate): 0.0824
  - Members: P003, P026, P040, P043, P067, P082, P103, P110, P111, P114, P117, P128, P151, P172, P182, P186, P188, P234, P238, P251, P265, P275, P303, P310, P342, P352, P353, P358, P359, P368...

### MEDIAL_STRONG (48 members)
  - Mean end_rate: 0.0828
  - Mean start_rate: 0.021
  - Mean internal_rate: 0.8961
  - Variance (end_rate): 0.0084
  - Members: P009, P031, P035, P050, P056, P058, P060, P062, P073, P075, P091, P092, P096, P120, P121, P122, P126, P127, P139, P142, P145, P147, P154, P160, P174, P175, P194, P201, P202, P204...

### MIXED (8 members)
  - Mean end_rate: 0.3829
  - Mean start_rate: 0.0835
  - Mean internal_rate: 0.5336
  - Variance (end_rate): 0.0248
  - Members: P011, P086, P123, P124, P125, P144, P221, P355

### TERMINAL_STRONG (7 members)
  - Mean end_rate: 0.7405
  - Mean start_rate: 0.0168
  - Mean internal_rate: 0.2427
  - Variance (end_rate): 0.0177
  - Members: P076, P095, P108, P226, P256, P378, P385

---

## Interpretation

Classes are derived from positional behavior only (start/end/internal rates). These are candidate structural classes, NOT phoneme assignments. TERMINAL_STRONG signs are candidates for morpheme-final markers. INITIAL_STRONG signs are candidates for title/initial determinatives.

## Next Steps for Class Refinement

1. Add visual feature vectors once sign plate images are acquired.
2. Re-run clustering on multi-site corpus (Harappa, Dholavira).
3. Add graph-neighbor features to the feature vector.
4. Run hierarchical and spectral clustering for stability comparison.
5. Do NOT collapse classes into phoneme assignments until Phase 9 gates are met.