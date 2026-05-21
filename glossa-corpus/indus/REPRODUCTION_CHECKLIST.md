# REPRODUCTION_CHECKLIST.md

Every quantitative claim in `preprint_v2_hardened.md` must be traceable to one of:
1. A named table in this directory
2. A named script in `backend/scripts/`
3. A cited external source with DOI/arXiv ID
4. A clearly labelled manual judgment

---

## Corpus and Anchor Files

| File | Description | Status |
|---|---|---|
| `ANCHOR_STATUS_AUDIT.csv` | Canonical sign list: 397 signs, confidence, frequency, evidence type, DEDR | ✅ Generated |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | Full anchor table with readings, confidence, basis, source | ✅ Exists |
| `corpora/.../indus_corpus 2.csv` | Holdat V3 corpus: 1,670 seals, 7,002 tokens, 390 signs | ✅ Exists |

## Required New Files (for full reproducibility)

| File | Content | Script to Generate | Status |
|---|---|---|---|
| `CORPUS_STATS_FINAL.json` | Site counts, seal counts, token counts, mean inscription length | `backend/scripts/foundation_check.py` (partial) | ⬜ Needed |
| `SIGN_POSITIONAL_PROFILES.csv` | I/M/T rates for all 390 signs | Compute from corpus | ⬜ Needed |
| `BIGRAM_TRIGRAM_COUNTS.csv` | Top-200 bigrams/trigrams with PMI | `backend/scripts/phase142_collocate_network.py` (partial) | ⬜ Needed |
| `MOTIF_ENRICHMENT_TESTS.csv` | 394 sign×motif pairs, χ², Bonferroni-corrected p-values | `backend/scripts/phase143_iconographic_formula.py` | ⬜ Needed |
| `NULL_MODEL_RESULTS.csv` | Permutation null results: test name, observed, null mean, null SD, p-value | `backend/scripts/phase134_falsification_suite.py` | ⬜ Needed |
| `FIGURE_GENERATION.md` | Instructions to regenerate each table/figure | Manual | ⬜ Needed |
| `SITE_SUMMARY_TABLE.csv` | Per-site: seals, tokens, distinct signs, mean inscription length | Compute from corpus | ⬜ Needed |

## Claim-to-Source Traceability

| Quantitative Claim | Source |
|---|---|
| 161 H+M anchors (75 HIGH, 86 MEDIUM) | `INDUS_FINAL_ANCHORS.json` → `ANCHOR_STATUS_AUDIT.csv` |
| 4 PROVISIONAL_MEDIUM signs | Phase-163/166 reports + `ANCHOR_STATUS_AUDIT.csv` |
| 90.96% token coverage | `INDUS_FINAL_ANCHORS.json` field `corpus_token_coverage` |
| 1,165/1,670 (69.8%) seals fully covered | `backend/reports/phase133_resolution.json` |
| Permutation null z=10.3, p<0.001 | `backend/reports/phase134_falsification_suite.json` field `F1_permutation_null` |
| Held-out accuracy 97.7% | `backend/reports/phase134_falsification_suite.json` field `F7_blind_held_out` |
| 0/113 isolated fish signs | `backend/reports/phase150_polysemy_permutation.json` + corpus computation |
| M267 motif-independence χ²=12.98, p=0.1124 | `backend/reports/phase132_validation_report.json` |
| Dravidian lift ratio 1.85× over Sanskrit | `backend/reports/phase67_sanskrit_norm.json` |
| 44/75 HIGH readings in Parpola 1994 | `backend/reports/phase157_160_reference_mining.json` |
| 10/10 Mahadevan papers confirm grammar | `backend/reports/phase157_160_reference_mining.json` |
| 93.2% sign-level grammar accuracy | `backend/reports/phase170_grammar_variance.json` |
| Bigram backbone M342·M176 PMI=2.43 | `backend/reports/phase142_collocate_network.json` |
| 63/394 (16%) motif×sign pairs enriched | `backend/reports/phase143_iconographic_formula.json` |
| 59/59 foundation checks pass | Run `backend/scripts/foundation_check.py` |

## README for External Reproducers

### Corpus
- **Source**: Holdat LLC Indus Corpus V3 (Miller 2025)
- **Download**: Contact Holdat LLC; corpus requires permission
- **Version**: V3 (1,670 seals, 7,002 sign tokens, 390 distinct signs)
- **Encoding**: Mahadevan M-numbers (M001–M416)
- **Sites**: Mohenjo-daro (606), Harappa (492), Kalibangan (110), Dholavira (106), Lothal (124), Chanhu-daro (78), Surkotada (61), Banawali (60), Rakhigarhi (33)
- **Exclusions**: Single-sign seals retained; graffiti/tablets excluded (formal stamp seals only)
- **Normalization**: Sign IDs are Mahadevan M-numbers; see `INDUS_FINAL_ANCHORS.json` for Mahadevan↔Parpola crosswalk

### Anchor Table
- Full table: `backend/reports/INDUS_FINAL_ANCHORS.json`
- Confidence criteria: see Methods §2.3 of `preprint_v2_hardened.md`
- HIGH = ≥2 independent evidence types; MEDIUM = ≥1 strong type; LOW = heuristic only
- PROVISIONAL_MEDIUM = MEDIUM pending expert peer review

### Running Foundation Check
```
cd glossa-lab
backend\venv\Scripts\python.exe backend\scripts\foundation_check.py
# Expected: 59 checks passed, 0 failed
```

### Key Phase Scripts
| Phase | Script | Output |
|---|---|---|
| Grammar null test | `phase134_falsification_suite.py` | F1–F12 verdicts |
| Fish-sign polysemy | `phase150_polysemy_permutation.py` | Isolation counts |
| Dravidian vs Sanskrit | `phase67_sanskrit_norm.py` | Lift ratio |
| M267 validation | `phase132_comprehensive_validation.py` | χ² + agreement |
| Grammar variance | `phase170_grammar_variance.py` | Sign-level accuracy |
| Sibilant validation | `phase166_sibilant_dedr_validation.py` | DEDR verdicts |
