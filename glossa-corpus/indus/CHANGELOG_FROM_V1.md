# CHANGELOG_FROM_V1.md — Preprint v1 → v2 Changes

## Breaking Changes (affect headline claims)

| Change | v1 | v2 | Reason |
|---|---|---|---|
| H+M anchor count | 268 | 161 genuine (+ 4 PROVISIONAL_MEDIUM) | Phase-133 removed 107 heuristic placeholder signs from the H+M count |
| Token coverage | 96.2% | 90.96% | Complementary to anchor count correction |
| Seals fully covered | 85.6% (1,429/1,670) | 69.8% (1,165/1,670) | Same Phase-133 correction |
| MEDIUM count | 193 | 86 | Phase-133 correction |
| LOW count | 129 | 236 | Phase-133 correction (heuristic signs re-classified) |
| Foundation checks | 45 | 59 | Phases 166–170 added |
| Irresolvable signs list | 20 (with M198, M223×2) | 18 (M198 removed, M223 deduplicated) | M198=co promoted to PROVISIONAL_MEDIUM by Phase-166 |
| Blocked seals percentage | 14.4% | 30.2% | Complement of corrected decoded count |

## Title Change

- v1: *Computational Decipherment of the Indus Valley Script: 268 Anchors, 96.2% Token Coverage, and a Proto-Dravidian Guild-Name Grammar*
- v2: *A Reproducible Computational Grammar and Candidate Proto-Dravidian Anchor Model for the Indus Valley Script*

## Abstract Changes

- Removed: "computational decipherment…achieving 268 sign anchors"
- Removed: "full decoding of 1,429/1,670 (85.6%) seals"
- Removed: "foundation validation (45/45 independent checks) confirms the Dravidian phonetic hypothesis"
- Added: Corrected metrics (161 H+M, 90.96%, 69.8%)
- Added: "we propose" / "candidate readings" framing
- Added: Explicit limitation and falsifiability statement
- Added: Coverage-caveat sentence (coverage ≠ verified phonetic reading)

## New Sections Added

| Section | Purpose |
|---|---|
| §3 Evidence Tiers and Claim Scope | Maps all claims to Tier 1/2/3; prevents overclaiming |
| §5 Adversarial Tests and Failure Conditions | Addresses hostile reviewer objections proactively |
| §5.1 Non-Linguistic Emblem Hypothesis | Shuffled-sign and motif-conditioned null tests |
| §5.2 Rebus Overfitting Risk | DEDR constraint criteria and candidate count |
| §5.3 Competing Language Families | Explicit statement of what was and was not tested |
| §5.4 Motif Circularity | Hold-out test design for icon-reading independence |
| §5.5 False Discovery Control | FDR/Bonferroni statements for multiple-comparison tests |
| §5.6 Failure Conditions | Explicit falsification criteria |

## Methods Section Changes

- §2.1: Added explicit inclusion/exclusion criteria for corpus
- §2.2: Formalized positional classification definitions
- §2.3: HIGH/MEDIUM/LOW criteria now stated as necessary and sufficient conditions
- §2.4: Added DEDR matching constraints (accepted sound correspondences, candidate count, tie-breaking)
- §2.5: Defined each null model type explicitly
- §2.6: Separated structural, phonological, lexical, and archaeological validation

## Results Section Changes

- Moved §3.7–§3.31 (25 phase-history subsections) to **Supplement A** 
- Main body §3 now contains §3.1–§3.6 (core results) + Evidence Tiers section
- Added corpus summary table (Table 1) 
- Added confidence summary table (Table 2) with corrected numbers
- Added null model results table (Table 5)
- Added failure conditions table (Table 6)
- All "full decoding" → "fully covered by H+M candidate readings"

## Discussion Section Changes

- §4.1 renamed: "What the Seals Say" → "Proposed Readings Under the Model"
- §4.2 Munda substrate: now explicitly Tier 3 with caveat
- §4.3 Irresolvable signs: count updated to 18; caveat added that ICIT may resolve them
- §4.4 Limitations: corpus size power analysis note added; Nair 2026 reframed as structural-only replication
- Added §4.5 Arthaśāstra caveat: parallel is illustrative, not evidential
- Added non-finality sentence in §5 Conclusion

## Reference Changes

- Completed: Martini (2025) — full citation added
- Completed: Roif (2025a) — full title and preprint URL added
- Clarified: Nair (2026) explicitly labelled as preprint, not peer-reviewed
- Added: Krishnamurti (2003) for phonotactic criteria
- Removed: Informal citation of personal correspondence as evidence

## Appendix Changes

- Appendix B: "20 Irresolvable Signs" → "18 Irresolvable Signs"
- Appendix B: M198 removed (now PROVISIONAL_MEDIUM)
- Appendix B: M223 deduplicated
- Appendix B: Added note: "Signs resist MEDIUM promotion under current methodology; ICIT corpus may provide resolution"
- Appendix C: Updated foundation check count from 45 to 59

## Language Replacements

See `CLAIM_AUDIT.md` §Language Replacements for full table. Key changes:
- "computational decipherment" → "computational decipherment hypothesis" / "grammar and anchor model"
- "the script is decipherable" → "the corpus shows structure consistent with a decipherable linguistic system"
- "confirms" → "supports" (for Dravidian hypothesis)
- "full decoding" → "fully covered by H+M candidate readings"
- "beyond reasonable doubt" → removed
- "what the seals say" → "proposed readings under the model"
