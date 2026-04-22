# Latent Sign Class Report
Generated: 2026-04-22T17:35:27Z
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

- Total signs classified: 774
- Unigram entropy (sign ID space): 9.5962 bits
- Class entropy: 2.4153 bits
- Entropy reduction from sign→class: 74.8%

### Class distribution

  - HAPAX: 276 signs
  - LOW_FREQUENCY: 146 signs
  - MEDIAL_STRONG: 142 signs
  - MIXED: 93 signs
  - TERMINAL_STRONG: 61 signs
  - INITIAL_STRONG: 45 signs
  - BIMODAL_INIT_TERM: 11 signs

---

## Per-Class Profiles

### BIMODAL_INIT_TERM (11 members)
  - Mean end_rate: 0.5152
  - Mean start_rate: 0.4545
  - Mean internal_rate: 0.0303
  - Variance (end_rate): 0.0023
  - Members: P320, Y0041, Y0127, Y0234, Y0324, Y0391, Y0424, Y0494, Y0795, Y0828, Y0856

### HAPAX (276 members)
  - Mean end_rate: 0.4167
  - Mean start_rate: 0.1558
  - Mean internal_rate: 0.4275
  - Variance (end_rate): 0.2431
  - Members: P007, P010, P012, P014, P020, P022, P023, P032, P037, P038, P041, P044, P047, P048, P053, P054, P061, P065, P070, P071, P083, P084, P089, P094, P099, P136, P156, P166, P170, P177...

### INITIAL_STRONG (45 members)
  - Mean end_rate: 0.05
  - Mean start_rate: 0.8183
  - Mean internal_rate: 0.1317
  - Variance (end_rate): 0.008
  - Members: P000, P001, P004, P013, P051, P098, P217, P301, P324, Y0064, Y0090, Y0136, Y0151, Y0153, Y0154, Y0155, Y0156, Y0159, Y0161, Y0167, Y0215, Y0241, Y0298, Y0400, Y0401, Y0409, Y0422, Y0423, Y0426, Y0520...

### LOW_FREQUENCY (146 members)
  - Mean end_rate: 0.3824
  - Mean start_rate: 0.0902
  - Mean internal_rate: 0.5274
  - Variance (end_rate): 0.1469
  - Members: P003, P026, P040, P043, P067, P082, P103, P110, P111, P114, P117, P128, P151, P172, P182, P186, P188, P234, P238, P251, P265, P275, P303, P310, P342, P352, P353, P358, P359, P368...

### MEDIAL_STRONG (142 members)
  - Mean end_rate: 0.0885
  - Mean start_rate: 0.0317
  - Mean internal_rate: 0.8798
  - Variance (end_rate): 0.0097
  - Members: P009, P031, P035, P050, P056, P058, P060, P062, P073, P075, P091, P092, P096, P120, P121, P122, P126, P127, P139, P142, P145, P147, P154, P160, P174, P175, P194, P201, P202, P204...

### MIXED (93 members)
  - Mean end_rate: 0.3235
  - Mean start_rate: 0.1293
  - Mean internal_rate: 0.5473
  - Variance (end_rate): 0.0212
  - Members: P011, P086, P123, P124, P125, P144, P221, P355, Y0000, Y0003, Y0004, Y0013, Y0016, Y0018, Y0031, Y0032, Y0035, Y0049, Y0061, Y0066, Y0072, Y0095, Y0097, Y0111, Y0125, Y0130, Y0132, Y0140, Y0142, Y0158...

### TERMINAL_STRONG (61 members)
  - Mean end_rate: 0.7455
  - Mean start_rate: 0.0491
  - Mean internal_rate: 0.2054
  - Variance (end_rate): 0.0209
  - Members: P076, P095, P108, P226, P256, P378, P385, Y0005, Y0015, Y0027, Y0028, Y0034, Y0091, Y0098, Y0104, Y0137, Y0171, Y0201, Y0219, Y0221, Y0260, Y0263, Y0272, Y0317, Y0323, Y0347, Y0352, Y0353, Y0360, Y0370...

---

## Interpretation

Classes are derived from positional behavior only (start/end/internal rates). These are candidate structural classes, NOT phoneme assignments. TERMINAL_STRONG signs are candidates for morpheme-final markers. INITIAL_STRONG signs are candidates for title/initial determinatives.

## Next Steps for Class Refinement

1. Add visual feature vectors once sign plate images are acquired.
2. Re-run clustering on multi-site corpus (Harappa, Dholavira).
3. Add graph-neighbor features to the feature vector.
4. Run hierarchical and spectral clustering for stability comparison.
5. Do NOT collapse classes into phoneme assignments until Phase 9 gates are met.