# Indus Script Decipherment — Research Outputs

**Preprint:** *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar*
**Author:** Tristen Kyle Pierson — BitConcepts LLC
**Date:** May 2026 · Preprint v1 — Not peer-reviewed

---

## Files in this directory

| File | Description |
|------|-------------|
| `pierson_2026_indus_preprint_v1.pdf` | Full preprint PDF |
| `anchor_table.csv` | 397-sign anchor table (CSV — open in Excel/Sheets) |
| `anchor_table.json` | Same table in JSON with full metadata |
| `mahadevan_parpola_crosswalk.json` | 45-entry M-number ↔ P-number sign crosswalk |
| `phase_reports/` | 35 computational phase reports (Phases 127–170) |
| `supplemental/` | 4 derived datasets for direct use by collaborators (fish-sign context, iconographic pairs, formula bigrams, polysemy test) |

The LaTeX source for the preprint is in `glossa-corpus/indus/preprint_v1.tex`.

---

## Anchor Table

`anchor_table.csv` / `anchor_table.json` contain the canonical sign reading assignments
for all 397 Mahadevan catalogue signs. Columns:

| Column | Description |
|--------|-------------|
| `Sign` | Mahadevan M-number (e.g. M342) |
| `Reading` | Candidate phonetic reading (e.g. ay/ā) |
| `Confidence` | HIGH / MEDIUM / LOW / PROVISIONAL_MEDIUM |
| `DEDR` | Dravidian Etymological Dictionary reference number |
| `Source` | Phase and method that assigned this reading |
| `Basis` | One-line evidence summary |

**Coverage:** 75 HIGH + 86 MEDIUM = **161 H+M candidates** covering **90.96%** of corpus tokens
(6,363 / 7,002 tokens across 1,670 seals at 9 sites).

**NOT counted toward coverage:** 236 LOW-confidence signs (heuristic assignments only).

---

## Corpus Note

The primary corpus used in this study is the **Holdat LLC Indus Corpus v3** (Miller 2025),
covering 1,670 formal stamp seals, 7,002 sign tokens, 390 distinct signs across 9 major IVC sites.

> **This corpus is not publicly available at time of writing.** Full reproduction of
> corpus-level statistics requires either access to the Holdat corpus under agreement with
> Holdat LLC, or re-running the analysis pipeline on a compatible public corpus (such as
> ICIT — Fuls 2023) after sign-code crosswalking.
>
> The anchor table, phase reports, and analysis scripts in this repository are sufficient
> to audit the methodology and reproduce all non-corpus-dependent checks.

---

## Phase Reports (`phase_reports/`)

Each JSON file records the full computational output of one research phase.
Key phases:

| Phase | File | Content |
|-------|------|---------|
| 127 | `phase127_fish_site_results.json` | Fish-sign polysemy test (0/113 corpus + 0/27 Gulf) |
| 128–129 | `phase128_129_anchor_upgrades.json` | Anchor set upgrades (+35 seals covered) |
| 133 | `phase133_resolution.json` | Correction of M372; count correction 268→161 |
| 134–140 | `phase134_falsification_suite.json`, `phase136_140_battery.json` | Full 10-test adversarial battery |
| 141 | `phase141_synthesis.json` | Master evidence scorecard (Phase-141) |
| 142 | `phase142_collocate_network.json` | Bigram/trigram collocate network; 97 formula types |
| 143 | `phase143_iconographic_formula.json` | 63 enriched INITIAL×icon pairs (chi-square) |
| 147 | `phase147_roif_validation.json` | 8/8 structural predictions confirmed |
| 150 | `phase150_polysemy_permutation.json` | Permutation null test for positional grammar |
| 151 | `phase151_site_kl_bootstrap.json` | Bootstrap CIs for 36 site-pair KL divergences |
| 156 | `phase156_gulf_seal_fish_test.json` | Gulf catalog validation (0/27 isolated fish signs) |
| 163 | `phase163_sibilant_discovery.json` | 4 PROVISIONAL_MEDIUM sibilant promotions |
| 169 | `phase169_master_synthesis.json` | Final master synthesis (32 items, 79.8% confidence) |
| 170 | `phase170_grammar_variance.json` | Grammar variance retest at 161 H+M (93.2% accuracy) |

---

## Reproducing the Analysis

The full Glossa-Lab analysis pipeline is in `backend/`. Key scripts:

```
backend/scripts/phase128_129_anchor_upgrades.py   # anchor upgrade methodology
backend/scripts/phase133_resolution.py             # sign count correction
backend/scripts/phase153_sibilant_anchors.py       # sibilant DEDR cross-validation
```

The pipeline uses `backend/glossa_lab/pipelines/decipher.py` (simulated annealing engine)
and `backend/glossa_lab/experiment_graph*.py` (Experiment Builder node graph system).

To run experiments without the Holdat corpus, upload any compatible corpus via the
Glossa Lab UI (Corpora tab → Upload) and select it in the relevant experiment nodes.

---

## License

All materials in this directory (preprint PDF, anchor table, phase reports, crosswalk) are
released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

See [`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0) for the full license text.

> **arXiv**: CC BY 4.0 is fully compatible with arXiv submission requirements. When submitting
> the preprint to arXiv, select "Creative Commons Attribution 4.0 International (CC BY 4.0)"
> as the license. This allows free reuse with attribution.

The Glossa Lab **source code** (`backend/`, `frontend/`, `tray/`, etc.) is separately
licensed under the MIT License — see the root [`LICENSE`](../../LICENSE) file.

---

## Citation

```
Pierson, T.K. (2026). A Falsifiable Computational Decipherment Hypothesis for the
Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional
Grammar. Preprint v1. BitConcepts LLC / Glossa-Lab.
https://github.com/BitConcepts/glossa-lab
```

---

*All materials in this directory are released before public posting of the preprint
to arXiv. See `glossa-corpus/indus/FINAL_RELEASE_CHECK.md` for the complete pre-arXiv
gating checklist.*
