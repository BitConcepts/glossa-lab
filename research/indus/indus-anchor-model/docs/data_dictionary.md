# Data Dictionary
## Indus Anchor Model — Public Data Tables

All files in `data/public/` are released under CC BY 4.0.
All sign IDs follow Mahadevan 1977 (M-number system).
Missing values are represented as empty string `""` (not `NA`, `null`, or `0`).

---

## anchor_table_397.csv

**Description:** All 397 signs in the Mahadevan 1977 catalogue with candidate readings, confidence levels, evidence bases, and corpus token counts. The 7 signs with zero corpus tokens are included for catalogue completeness. The 161 HIGH/MEDIUM signs are the primary anchor set used in all analyses.

**Source:** Computed from Holdat LLC Indus Corpus v3 (Miller 2025) by Glossa-Lab pipeline (Phases 1–177). Crosswalk entries from mahadevan_parpola_crosswalk_v2.json.

**Columns:**

| Column | Type | Values | Notes |
|---|---|---|---|
| `sign_id` | string | `M001`–`M417` | Mahadevan M-number |
| `reading_candidate` | string | e.g. `ay/ā` | Proposed phonetic/morphemic reading; slash = variant |
| `confidence` | string | `HIGH`, `MEDIUM`, `PROVISIONAL_MEDIUM`, `LOW` | Evidence tier |
| `confidence_basis` | string | text | Short evidence summary |
| `dedr_id` | string | integer or `""` | DEDR entry number (Burrow & Emeneau 1984); empty if no match |
| `positional_class` | string | `INITIAL`, `MEDIAL`, `TERMINAL`, `SOLO`, `MIXED`, `""` | Dominant positional slot |
| `token_count` | integer | ≥0 | Corpus token count in Holdat v3; derived from restricted corpus |
| `source` | string | text | Phase or reference that established reading |
| `notes` | string | text | Caveats, substrate notation, provisional flags |

**Figures/tables supported:** §3.1 Sign Anchor Summary table; §3.3 Selected High-Confidence Readings.

**Restriction note:** `token_count` column derived from Holdat LLC Indus Corpus v3. The sign IDs, readings, and confidence tiers are public.

---

## fish_sign_contexts.csv

**Description:** Per-seal compound-context listing for the plain fish sign (M047) and the man/anthropomorphic sign (M001). All 13 M047 and 14 M001 occurrences across the 1,670-seal Holdat corpus. Used to verify the fish-sign compound-only result.

**Source:** Derived from Holdat LLC Indus Corpus v3 (Miller 2025) by Glossa-Lab pipeline (Phases 124–127).

**Columns:**

| Column | Type | Values | Notes |
|---|---|---|---|
| `seal_id` | string | e.g. `seal_0319` | Holdat seal identifier |
| `site` | string | e.g. `Harappa` | Excavation site |
| `sign_id` | string | `M047` or `M001` | Target sign |
| `positional_slot` | string | `INITIAL`, `MEDIAL`, `TERMINAL` | Position in sequence |
| `left_neighbor` | string | M-number or `""` | Immediate left neighbor sign |
| `right_neighbor` | string | M-number or `""` | Immediate right neighbor sign |
| `full_sequence` | string | e.g. `M047 · M267 · M342` | Complete sign sequence for the seal |
| `is_isolated` | boolean | `TRUE`, `FALSE` | Whether the fish sign appears alone (always FALSE) |

**Figures/tables supported:** §3.5 Fish Sign Polysemy Test; §3.19 Gulf Seal Fish-Sign Test.

**Restriction note:** Seal IDs and site labels derived from Holdat LLC. The contextual data (sequence, slot) is public research output.

---

## formula_bigrams.csv

**Description:** Top-30 directed H+M×H+M bigram pairs from the full Holdat corpus. H+M = HIGH or MEDIUM confidence anchor signs. Includes raw counts, PMI, and co-occurrence seal counts.

**Source:** Derived from Holdat LLC Indus Corpus v3 (Miller 2025) by Glossa-Lab pipeline (Phase 142).

**Columns:**

| Column | Type | Values | Notes |
|---|---|---|---|
| `sign_a` | string | M-number | Left sign in directed bigram |
| `sign_b` | string | M-number | Right sign in directed bigram |
| `bigram_label` | string | e.g. `M342·M176` | Display label |
| `count` | integer | ≥2 | Number of occurrences across all seals |
| `seal_count` | integer | ≥2 | Number of distinct seals containing this bigram |
| `pmi` | float | — | Pointwise mutual information (log-odds, no threshold applied) |
| `reading_a` | string | text | Candidate reading for sign_a |
| `reading_b` | string | text | Candidate reading for sign_b |

**Figures/tables supported:** §3.7 Collocate Network and Formula Structure; §3.32 Betweenness Centrality Stratification.

**Restriction note:** `count` and `seal_count` derived from restricted Holdat corpus.

---

## iconographic_formula_pairs.csv

**Description:** Enriched INITIAL-sign × seal-iconography pairs, from chi-square test with Bonferroni correction across 394 pairs. 63 pairs were significantly enriched (p < 0.05 after correction). Used to demonstrate co-selection of inscription title and carved animal icon.

**Source:** Computed from Holdat LLC Indus Corpus v3 (Miller 2025) by Glossa-Lab pipeline (Phase 143).

**Columns:**

| Column | Type | Values | Notes |
|---|---|---|---|
| `initial_sign` | string | M-number | INITIAL classifier sign |
| `reading_candidate` | string | text | Candidate reading |
| `iconography` | string | e.g. `rhinoceros` | Seal animal icon label |
| `observed` | integer | ≥1 | Observed co-occurrence count |
| `expected` | float | >0 | Expected count under independence |
| `chi_square` | float | ≥0 | Chi-square statistic |
| `p_value_bonferroni` | float | 0–1 | Bonferroni-corrected p-value |
| `is_enriched` | boolean | `TRUE`, `FALSE` | Whether pair passes Bonferroni threshold |

**Figures/tables supported:** §3.8 Iconographic Cross-Encoding.

---

## polysemy_divergence_summary.csv

**Description:** Summary results from the Phase-150 permutation null test for polysemy (position-dependent collocate profiles). Tests 21 H+M signs for context-dependent behavior using KL divergence > 0.3 bits as threshold.

**Source:** Computed from Holdat LLC Indus Corpus v3 (Miller 2025) by Glossa-Lab pipeline (Phase 150), n=1,000 shuffles.

**Columns:**

| Column | Type | Values | Notes |
|---|---|---|---|
| `sign_id` | string | M-number | Sign tested |
| `reading_candidate` | string | text | Candidate reading |
| `kl_divergence` | float | ≥0 | KL divergence (bits) between INITIAL and non-INITIAL collocate profiles |
| `is_polysemous` | boolean | `TRUE`, `FALSE` | Whether KL > 0.3 bits threshold |
| `null_mean` | float | — | Mean KL divergence under null (shuffled) |
| `null_sd` | float | — | SD of null distribution |
| `p_value` | float | 0–1 | One-tailed permutation p-value |

**Figures/tables supported:** §3.13 Polysemy Permutation Null.
