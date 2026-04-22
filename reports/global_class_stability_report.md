# Global Class Stability Report
Generated: 2026-04-22T18:16:22Z

## Method
Signs are classified GLOBALLY on the full 2,722-inscription corpus.
Then, for each site, we ask: does this sign's local positional behavior
AGREE with its globally assigned class?
Agreement criterion: TERMINAL → site end_rate >= 0.40; INITIAL → site start_rate >= 0.40;
MEDIAL → site internal_rate >= 0.50; MIXED → always agree.
Minimum global freq for classification: 10 tokens.
Minimum site occurrences for assessment: 2 tokens.

This avoids the relative-threshold artefact where different min_freq
values at each site cause the same sign to get different class labels.

## Results

- Signs classifiable globally (freq >= 10): 105
- Signs appearing in >= 2 sites: 102
- Signs with decisive multi-site evidence: 102

- **FULLY STABLE** (all sites agree): 87 (85.3%)
- PARTIALLY STABLE (majority agree): 10
- UNSTABLE (majority disagree): 5
- No decisive data: 0

**Full stability rate: 85.3%**
**Full+partial stability rate: 95.1%**

## Per-Class Stability

- INITIAL: 8/11 stable (72.7%)
- MEDIAL: 37/45 stable (82.2%)
- MIXED: 33/33 stable (100.0%)
- TERMINAL: 9/13 stable (69.2%)

## Global Class Distribution

- INSUFFICIENT_DATA: 77 signs
- MEDIAL: 46 signs
- MIXED: 33 signs
- TERMINAL: 14 signs
- INITIAL: 12 signs

## Review Gate Assessment

Phase 9 gate requires cross-site class stability >= 70%.
Current full stability: 85.3%
Current full+partial stability: 95.1%

**GATE STATUS: PASS** (full stability >= 70%)
Global latent classes are site-independent. Phase 9 cross-site condition is MET.