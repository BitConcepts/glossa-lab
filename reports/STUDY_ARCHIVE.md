# Glossa Lab — Study Archive

Authoritative reproduction guide for all results in the paper:
**"Glossa Lab: A Computational Toolkit for Ancient Script Analysis"**

---

## Identification

| Field | Value |
|---|---|
| Repository | github.com/BitConcepts/glossa-lab |
| Branch | main |
| Python version | 3.12.x |
| Key commit | See `git log --oneline -1` |
| Date of experiments | 2026-04-01 through 2026-04-02 |
| Platform tested | Windows 11, Ubuntu 22.04, macOS (CI) |

---

## Software dependencies

All dependencies are pinned in `backend/pyproject.toml`.

```bash
# Clone and set up
git clone https://github.com/BitConcepts/glossa-lab
cd glossa-lab
./setup-os.sh install   # Linux/macOS
# or
setup-os.cmd install    # Windows

# Verify
shell.cmd test backend/tests -v
# Expected: 152+ passed
```

Key packages:
- Python 3.12, FastAPI 0.115, uvicorn 0.34
- aiosqlite 0.20, reportlab 4.x
- pytest 8.x, ruff 0.9.x

---

## Data sources and provenance

### Linear B corpus
- **Source:** DĀMOS — Database of Mycenaean at Oslo, University of Oslo
- **URL:** https://damos.hf.uio.no/
- **Licence:** CC BY-NC-SA 4.0
- **File:** `backend/tests/corpora/fixtures/linear_b.txt`
- **Content:** 49 lines of representative Pylos (PY) and Knossos (KN) tablet words in CIPEM syllabic transliteration (~628 syllable tokens)
- **Citation:** Aurora, F. (2015). DĀMOS. Procedia Social and Behavioral Sciences, 198, 21–31.

### Ugaritic corpus
- **Source:** Manually transcribed from published editions (KTU 1.1–1.6)
- **File:** Embedded in `backend/tests/corpora/synthetic.py` (Ugaritic benchmark)
- **Content:** 83 lines of Baal Cycle, sign IDs U01–U30 with answer key
- **Citation:** Dietrich, M., Loretz, O. & Sanmartín, J. (2013). TUAT/KTU3.

### Linear A corpus (real tablet data)
- **Primary source:** tylerlengyel.com/linearA/research/output/latest/
- **Data derived from:** Younger, J.G. (2024). Linear A Texts in Phonetic Transcription. academia.edu/117949876
- **Further derived from:** SigLA (https://sigla.phis.me/) and Younger's KU website archive (web.archive.org/web/20190416193018/http://www.people.ku.edu/~jyounger/LinearA/)
- **Files downloaded:**
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_sign_frequency.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_bigram_frequency.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_trigram_frequency.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_initial_position_frequency.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_terminal_position_frequency.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_prefix_patterns.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_suffix_patterns.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_corpus_manifest.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_corpus_provenance_links.csv`
  - `backend/tests/corpora/fixtures/linear_a_real/phase1_normalization_mapping_log.csv`
- **Licence:** CC-compatible (see tylerlengyel.com for terms)
- **Note:** This data is processed from Younger's transliterations. For primary scholarly access, see Younger (2024) on academia.edu.

### Linear A corpus (statistical model)
- **Source:** Packard (1974) Appendix E; Younger (2000) sign-frequency updates
- **File:** `backend/tests/corpora/linear_a_corpus.py` (generator)
- **Seed:** 42 for all reproducible runs

### Indus Script corpus (synthetic)
- **Source:** Statistical model based on Yadav et al. (2010) published distributions
- **File:** `backend/tests/corpora/indus_corpus.py` (generator)
- **Seed:** 42
- **NOT** the actual Mahadevan (1977) M77 corpus

### English, DNA, Fortran, Tamil, Sanskrit, Sumerian corpora
- **Files:** `backend/tests/corpora/fixtures/`
- English: Excerpt from Melville's Moby Dick (public domain)
- DNA: Human beta-globin gene (NCBI, public domain)
- Fortran: Generic numeric code (public domain)
- Tamil: Thirukkural excerpts (transliterated, public domain)
- Sanskrit: Rigveda Mandala 1 (transliterated, public domain)
- Sumerian: Ur III administrative tablet formulae (representative sample, public domain)

---

## Reproducing every result

### Validation benchmarks (Linear B, Ugaritic)

```bash
shell.cmd test backend/tests/test_study_linear_b.py -v
shell.cmd test backend/tests/test_study_rao2009.py -v
```

Or run the report generators directly:

```bash
shell.cmd python backend/generate_report_linear_b.py
# Output: reports/linear_b_decipherment.pdf
# Expected: 62/62 = 100%, Kandles 1.000

shell.cmd python backend/generate_report_linear_a.py
# Output: reports/linear_a_analysis.pdf
```

### Linear A real-corpus phoneme analysis

```bash
shell.cmd python backend/run_linear_a_real_study.py
# Expected output:
#   Sign corpus: 6000 tokens
#   Phonetically decoded: 5213/6000 = 86.9%
#   H1_norm = 0.8742
#   greek score=86.90 kandles=0.9620 word_matches=7

shell.cmd python backend/generate_report_linear_a_real.py
# Output: reports/linear_a_real_analysis.pdf
```

### Anti-circularity experiments (7 experiments)

```bash
shell.cmd python backend/run_circularity_experiments.py
# Runtime: ~5-10 minutes (30 MC trials per experiment)
# Output: reports/circularity_results.json

shell.cmd python backend/generate_report_linear_a_circularity.py
# Output: reports/linear_a_circularity_analysis.pdf
```

**Key expected results:**
- Exp 1 (raw tablets, full scoring): Greek=56.90, margin=39.92
- Exp 5 no-vocab: Greek=16.90 (LAST); Luwian=16.99 (winner)
- Exp 5 Kandles-only: Greek=9.52 (LAST); Luwian=9.94 (winner)
- Exp 4 p-value: ~0.40 (real mapping not distinguishable from random under no-vocab)

### Assumption-free distributional decipherment

```bash
shell.cmd python backend/run_assumption_free_experiments.py
# Output: reports/assumption_free_results.json

shell.cmd python backend/generate_report_assumption_free.py
# Output: reports/assumption_free_analysis.pdf
```

### Full paper

```bash
shell.cmd python backend/generate_paper_full_study.py
# Output: reports/glossa_lab_linear_a_paper.pdf
```

---

## Random seeds used

All Monte Carlo experiments use explicit seeds for full reproducibility.

| Experiment | Seed |
|---|---|
| Linear A Markov chain corpus | seed=42 |
| Indus corpus generator | seed=42 |
| Linear B validation | seed=42 (max_iterations=8000, restarts=5) |
| Anti-circularity MC trials | seed=trial*7+13 (per trial) |
| Distributional clustering | seed=42 |
| Word-structure experiments | seed=42 |

---

## File map

```
reports/
├── glossa_lab_linear_a_paper.pdf       ← Main publication
├── STUDY_ARCHIVE.md                    ← This file
├── circularity_results.json            ← All 7 experiment results (raw data)
├── linear_b_decipherment.pdf           ← Study 1: Linear B validation
├── linear_a_analysis.pdf               ← Study 2: Linear A statistical
├── linear_a_real_analysis.pdf          ← Study 3: Phoneme-level real corpus
├── linear_a_circularity_analysis.pdf   ← Study 4: Anti-circularity suite
├── assumption_free_results.json        ← Study 5: New approach results
├── assumption_free_analysis.pdf        ← Study 5: New approach report
├── block_entropy_analysis.pdf          ← Multi-corpus entropy comparison
├── decipherment_report.pdf             ← Ugaritic + synthetic cipher
└── glossa_lab_project_report.pdf       ← Project overview and collaboration proposal

backend/
├── glossa_lab/
│   ├── pipelines/
│   │   ├── block_entropy.py            ← Entropy analysis (Rao 2009)
│   │   ├── nsb_entropy.py              ← Miller-Madow + Chao-Shen estimators
│   │   ├── char_freq.py                ← Zipf analysis
│   │   ├── kandles.py                  ← Kandles phonetic fingerprint
│   │   ├── positional.py               ← Position-frequency analysis
│   │   ├── sign_cluster.py             ← Distributional clustering
│   │   ├── paradigm.py                 ← Paradigm detection
│   │   ├── cooccurrence.py             ← Co-occurrence networks
│   │   ├── numerals.py                 ← Numeral identification
│   │   ├── decipher.py                 ← Hill-climbing decipherment engine
│   │   ├── hypothesis.py               ← Hypothesis-driven engine
│   │   ├── logosyllabic.py             ← Logosyllabic analysis (Ventris)
│   │   ├── distributional_decipherment.py  ← Assumption-free grid (NEW)
│   │   └── word_structure_hypothesis.py    ← Word-structure scoring (NEW)
│   ├── experiments/
│   │   ├── stats.py                    ← Bootstrap CI, p-values, z-scores
│   │   └── linear_a_circularity.py     ← 7 anti-circularity experiments
│   └── data/
│       ├── dravidian.py                ← Proto-Dravidian vocabulary
│       ├── sanskrit.py                 ← Vedic Sanskrit vocabulary
│       └── linear_b_language.py        ← Mycenaean Greek syllabary
├── tests/
│   ├── corpora/
│   │   ├── fixtures/
│   │   │   ├── english.txt             ← Melville corpus
│   │   │   ├── dna.txt                 ← Beta-globin
│   │   │   ├── fortran.txt             ← Numeric code
│   │   │   ├── tamil.txt               ← Thirukkural
│   │   │   ├── sanskrit.txt            ← Rigveda Mandala 1
│   │   │   ├── sumerian.txt            ← Ur III administrative
│   │   │   ├── linear_b.txt            ← Pylos/Knossos tablets
│   │   │   └── linear_a_real/          ← Real tablet bigram data
│   │   ├── synthetic.py                ← Synthetic corpus generators
│   │   ├── real.py                     ← Real corpus loaders
│   │   ├── indus_corpus.py             ← Indus statistical model
│   │   ├── linear_a_corpus.py          ← Linear A statistical model
│   │   └── linear_a_real_corpus.py     ← Real tablet corpus (bigram Markov)
│   ├── test_study_linear_b.py          ← Linear B validation tests (10)
│   ├── test_study_linear_a.py          ← Linear A analysis tests (10)
│   ├── test_study_rao2009.py           ← Rao 2009 replication tests (13)
│   ├── test_study_synthetic.py         ← Synthetic benchmark tests (7)
│   └── ...                             ← 152 tests total
```

---

## How to cite

If you use Glossa Lab or these study results, please cite:

```
BitConcepts. (2026). Glossa Lab: A Computational Toolkit for Ancient Script Analysis.
Decipherment Validation, Linear A Phonological Analysis, and Anti-Circularity Experiments.
Version 1.0. Available at: github.com/BitConcepts/glossa-lab
```

And acknowledge the data sources listed above, particularly DĀMOS and Younger (2024).

---

## Known issues and limitations

1. The Hurrian, Luwian, and Semitic language models are minimal character-level corpora. The anti-circularity results should be re-run with richer models before final publication claims.

2. The Kandles system ([REDACTED-PATENT-PUB]) uses a phoneme-to-colour mapping calibrated for Greek-family phonology. Its sensitivity to non-IE phonological contrasts has not been validated.

3. The Indus Script corpus is a statistical model, not the actual Mahadevan M77 sign inventory. Results should be reconfirmed on the real corpus when available (ICIT database, Dr. Andreas Fuls, TU Berlin).

4. The Linear A corpus manifest from tylerlengyel.com covers approximately 9 tablets from the source data used. A complete analysis would require the full GORILA corpus.

5. All entropy analyses use MLE estimators. The NSB/Chao-Shen estimators are implemented but not yet systematically applied to the small per-site Linear A corpora.

---

## Contact

For questions about data access, methodology, or collaboration:
**Glossa Lab Research Programme, BitConcepts**

For Indus Script corpus access (ICIT):
**Dr. Andreas Fuls, Technische Universität Berlin**
