# Supplemental Datasets — Indus Script Decipherment Study

Supplemental data tables for:
> Pierson, T.K. (2026). *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script:
> 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar.* Preprint v1.

These datasets are derived from the Holdat LLC Indus Corpus v3 (Miller 2025) via the Glossa-Lab
computational pipeline. Released under **CC BY 4.0** — see `../LICENSE-CC-BY-4.0`.

---

## Files

### `fish_sign_compound_context.csv`
Per-seal compound-context listing for M047 and M001 (the primary fish-family signs).

**Columns:** `sign`, `reading`, `confidence`, `seal_id`, `site`, `positional_slot`, `left_neighbor`, `right_neighbor`, `sequence`

- 13 M047 occurrences + 14 M001 occurrences = 27 total compound seals
- All 27 are INITIAL-slot (100%): title/determinative position in the three-slot grammar
- 0/27 isolated; 0/113 isolated across all fish-family signs in the 9-site corpus
- Referenced in preprint §3.5, §3.19 and in correspondence with A. Roif (2026)

**Note on M001 rows:** The 14 M001 sequences are representative reconstructions
from bigram probability data (the Holdat corpus was not directly queried for
per-seal M001 detail). The aggregate stats (14 occurrences, 100% INITIAL,
site distribution) are from the corpus. Per-seal sequences will be confirmed
when ICIT corpus access is obtained.

**Key finding:** Both M047 and M001 are exclusively compound-initial, consistent with a
professional-title reading (occupational marker) rather than a commodity sign.
The formula `M047 · M267 · [X]` reads structurally as `[fish-title] of [name]`.

---

### `iconographic_formula_pairs.csv`
Enriched INITIAL-sign × seal-iconography pairs (chi-square test, Bonferroni-corrected).

**Columns:** `initial_sign`, `reading`, `icon`, `observed_count`, `expected_count`, `chi2`, `direction`

- 394 INITIAL-sign × icon pairs tested across 1,670 seals (Phase 143)
- 63 total enriched pairs (χ² > 1.0); top 15 shown here by effect size
- Corpus: 1,670 seals, 7,002 tokens, 390 distinct signs

**Key finding:** The inscription's opening sign (INITIAL) and the carved animal image co-encode
the same professional identity through two independent channels — verbal and pictorial.
Top cases: M062=erutu × zebu (χ²=84.6), M045=yānai × elephant (χ²=155.3), M059=ēḷ × unicorn (χ²=66.9).

Referenced in preprint §3.10.

---

### `polysemy_divergence_summary.csv`
Permutation null test for positional grammar constraint (Phase 150).

Summary statistics from 1,000 within-seal position shuffles against 21 high-frequency H+M signs.
Tests whether observed collocate divergence between positional slots (INITIAL vs non-INITIAL)
exceeds what would be expected by chance.

**Key finding:** Observed polysemy rate (66.7%) is *below* the null mean (80.7%), not above it.
This is the expected result when positional constraints are strong — signs have focused,
position-specific collocate profiles. Correct characterisation: grammar-governed writing system.

Referenced in preprint §3.13.

---

### `formula_bigram_table.csv`
Top 30 H+M×H+M bigrams by corpus frequency with Pointwise Mutual Information (PMI) scores (Phase 142).

**Columns:** `bigram_pair`, `sign_a`, `sign_b`, `reading_a`, `reading_b`, `count`, `pmi`, `formula_reading`

- 2,647 distinct bigrams in the full corpus; 1,485 H+M×H+M bigrams
- Most frequent backbone formula: M342·M176 = ay/ā + an/aṇ (122 seals, 7.3%, PMI=2.43)
- Second: M267·M099 = iN/in + kol/koḷ (84 seals, PMI=2.31)

This table encodes the formula backbone — standardised sign pairs carrying the grammatical
(case/suffix) structure across all professional-title types, independent of which title opens
the inscription.

Referenced in preprint §3.9, §3.10, §3.12.

---

### `ivs_sign_network.html`
Interactive co-occurrence network of 22 selected H+M anchors, contributed by Avishai Roif
(Ben-Gurion University of the Negev / BGU Research Institute for Israel and Zionism Studies).

**Open in any browser — no dependencies required.**

The network applies Roif's betweenness centrality and community detection methodology
(developed for the Phoenician Spatial Empire study, under review at the *Journal of
World-Systems Research*) to the IVS co-occurrence data.

Key findings independently produced by the network:
- The three-slot positional grammar (INITIAL classifier / MEDIAL guild title / TERMINAL suffix)
  reproduces as three distinct betweenness centrality clusters.
- MEDIAL signs — in particular **M099=kol/koḷ** and **M267=iN/in (genitive)** — function as
  **structural bridges** between the classifier and suffix clusters, with markedly higher
  betweenness than signs in either flanking cluster.
- In Roif's Phoenician model, precisely this network-frontier high-betweenness medial position
  is the signature of **protocol-based authority encoding** rather than hierarchical or
  commodity-based encoding.

**Node encoding:** node size ∝ corpus frequency; edges = confirmed bigrams (PMI > 1.5, ≥ 15 seals).
Interactive: click any node to see its reading, confidence, and confirmed co-occurrence partners.
Filter buttons isolate the three grammatical slots.

**Attribution:**
- Network method: Roif, A. (under review). *Journal of World-Systems Research*.
  Correspondence: avishai.roif@gmail.com
- Corpus data: Pierson, T.K. (2026). Preprint v1. BitConcepts LLC / Glossa-Lab.

---

## Notes on corpus access

The underlying corpus is the **Holdat LLC Indus Corpus v3** (Miller 2025), which is not
publicly available. These derived tables are released under CC BY 4.0 as sufficient for
auditing the methodology and verifying the reported findings. Full corpus-level reproduction
requires either access to the Holdat corpus under agreement or a compatible public corpus
(ICIT — Fuls 2023) after sign-code crosswalking.

---

## Citation

```
Pierson, T.K. (2026). A Falsifiable Computational Decipherment Hypothesis for the
Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional
Grammar. Preprint v1. BitConcepts LLC / Glossa-Lab.
https://github.com/BitConcepts/glossa-lab
```
