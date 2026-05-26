# A Falsifiable Computational Anchor Model for the Indus Script
## Preprint Release v1 — Reproducibility Package

**Pierson, T. K. (2026).** *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar.* Preprint v2.

> This repository accompanies a preprint. It does not claim final decipherment. It provides data tables, scripts, and validation outputs for testing a candidate positional-grammar and anchor-reading model. Full reproduction of corpus-level counts may require access to the Holdat LLC Indus Corpus v3 or rerunning the pipeline on a compatible public corpus such as ICIT after sign-code crosswalking.

---

## 1. What is this repository?

This package provides the public materials for a computational study of Indus-script structure using positional analysis, bigram collocations, permutation tests, fish-sign polysemy testing, betweenness centrality stratification, and candidate sign-anchor modeling.

**The study does not claim final decipherment.** It proposes a falsifiable model with explicit confidence tiers, documented limitations, and cross-corpus validation targets. The primary corpus (Holdat LLC Indus Corpus v3, Miller 2025) is not redistributed here due to licensing.

---

## 2. What claims can be reproduced from public data?

The following can be tested using only the public tables in `data/public/`:

| Claim | Script | Status |
|---|---|---|
| Fish signs are 0% isolated in all corpus contexts | `scripts/fish_sign_test/` | REPRODUCED_FROM_PUBLIC_DATA |
| M342·M176 is the highest-PMI bigram pair | `scripts/grammar_model/` | REPRODUCED_FROM_PUBLIC_DATA |
| 161 H+M signs have BC > 0 (grammar candidates) | `scripts/network_analysis/` | REPRODUCED_FROM_PUBLIC_DATA |
| Anchor table covers 397 Mahadevan sign numbers | integrity check | REPRODUCED_FROM_PUBLIC_DATA |
| 141/161 H+M signs have BC = 0 (name-syllable signature) | `scripts/network_analysis/` | REPRODUCED_FROM_PUBLIC_DATA |

Run all public checks at once:

```bash
cd scripts/validation/
python run_all_public_checks.py
# Output: outputs/logs/public_validation_report.txt
```

---

## 3. What cannot be reproduced without restricted corpus access?

The following require authorized access to the Holdat LLC Indus Corpus v3 or an equivalent corpus (e.g. ICIT after sign-code crosswalking):

- Token coverage percentages (90.96% H+M, 9.34% LOW)
- Positional rates (I/M/T percentages) from raw seal sequences
- Permutation null test (z = 10.3, 0/2000 permutations)
- Bootstrap confidence intervals for site-level KL divergences
- Site-level sign frequency tables beyond the 5-site summary

See `data/restricted/README_restricted_data.md`.

---

## 4. What data are public?

All files in `data/public/` are released under CC BY 4.0:

| File | Description |
|---|---|
| `anchor_table_397.csv` | All 397 Mahadevan M-number signs with candidate readings and confidence levels |
| `fish_sign_contexts.csv` | Per-seal compound-context listing for M047 (plain fish) and M001 |
| `formula_bigrams.csv` | Top-30 H+M×H+M bigrams with counts and PMI |
| `iconographic_formula_pairs.csv` | 63 enriched INITIAL-sign × seal-icon chi-square pairs |
| `polysemy_divergence_summary.csv` | Phase-150 permutation null test (21 signs, 1,000 shuffles) |

---

## 5. What data are restricted?

The Holdat LLC Indus Corpus v3 (Miller 2025) is not redistributed here. See `data/restricted/README_restricted_data.md` for details on what corpus-level outputs require restricted access and how to request it.

---

## 6. How do I run each analysis?

Each script folder contains a `README.md` with specific instructions. Quick start:

```bash
# Install dependencies
pip install -r requirements.txt

# Run all public reproducibility checks
python scripts/validation/run_all_public_checks.py \
    --data-dir data/public/ \
    --output-dir outputs/

# Run betweenness centrality on public bigram table
python scripts/network_analysis/run_betweenness.py \
    --bigrams-file data/public/formula_bigrams.csv \
    --hm-signs-file data/public/anchor_table_397.csv \
    --output-dir outputs/

# Run fish-sign isolation test
python scripts/fish_sign_test/run_fish_sign_test.py \
    --contexts-file data/public/fish_sign_contexts.csv \
    --output-dir outputs/
```

---

## 7. What outputs should I expect?

After running the public validation suite:

```
outputs/logs/public_validation_report.txt   — human-readable check results
outputs/tables/public_validation_summary.csv — machine-readable status per check
outputs/tables/bc_rankings.csv              — betweenness centrality rankings
outputs/tables/fish_sign_summary.csv        — fish-sign isolation test results
```

Each output file notes whether it was produced from public data alone or requires restricted corpus access.

---

## 8. How do I cite this work?

```bibtex
@misc{pierson2026indus,
  author    = {Pierson, Tristen Kyle},
  title     = {A Falsifiable Computational Decipherment Hypothesis for the
               Indus Valley Script: 161 Candidate Proto-Dravidian Anchors
               and a Three-Slot Positional Grammar},
  year      = {2026},
  note      = {Preprint v2 -- Not peer-reviewed},
  url       = {https://github.com/BitConcepts/glossa-lab}
}
```

See `CITATION.cff` for CFF 1.2.0 format.

---

## 9. What would falsify the model?

The model makes falsifiable predictions. It is weakened or refuted if:

**Structural falsification (Tier 1):**
- Fish signs appear in isolation in formal seal contexts at >0% rate
- Positional structure is indistinguishable from random in a permutation test on ICIT
- The three-slot grammar fails to predict sign position at better than chance on a held-out corpus
- Site-level KL divergences are not bootstrap-robust on ICIT

**Candidate anchor falsification (Tier 2):**
- H+M token coverage collapses to <70% under ICIT sign crosswalk
- Proposed terminal signs do not remain terminal-dominant in ICIT positional profiles
- M267-equivalent sign behaves iconographically rather than functionally in ICIT
- Bigram/centrality structure does not reproduce on ICIT

**External anchor falsification:**
- The Shu-ilishu phonological test fails at >3/4 slots on a larger corpus
- The M267 correction is contradicted by newly discovered bilingual inscription evidence

See `docs/falsification_protocol.md` for the complete formal checklist.

---

## License

- Code and scripts: MIT License
- Documentation and public tables: CC BY 4.0

The Holdat LLC Indus Corpus v3 is not redistributed. See `data/restricted/README_restricted_data.md`.

## Repository

https://github.com/BitConcepts/glossa-lab
