# Non-Linguistic Benchmark Suite (Sproat 2014 / 2023)

Benchmark scripts comparing Indus Script statistical metrics against
non-linguistic symbol systems, following the methodology of:

- Sproat, R. (2014). *A statistical comparison of written language and
  nonlinguistic symbol systems*. Language, 90(2), 457–481.
- Sproat, R. (2023). *Symbols: An Evolutionary History from the Stone Age
  to the Future*. Springer.

## Purpose

Entropy/Zipf/conditional-entropy results alone cannot distinguish writing
from structured non-linguistic systems (Sproat 2014). This suite explicitly
benchmarks IVS metrics against known non-linguistic corpora so the manuscript
can make appropriately scoped claims.

## Data Sources

1. **Published statistics** from Sproat 2014 Table 1 and supplementary
   materials (Project MUSE). These are embedded in
   `sproat_2014_reference_stats.json`.

2. **Sproat 2023 simulation code**: https://github.com/rwsproat/symbols
   (code for computational simulations; does not contain the raw
   non-linguistic corpora).

3. **LDC non-linguistic corpora** (NSF grant BCS-1049308): totem poles,
   Pictish stones, Vinča, Mesopotamian deity symbols (kudurrus), weather
   icons, barn stars, heraldry. These require manual acquisition from the
   Linguistic Data Consortium. If you have access, place the XML files in
   `data/non_linguistic/` and run `fetch_or_prepare_corpus.py`.

## Scripts

| Script | Function |
|--------|----------|
| `sproat_2014_reference_stats.json` | Published statistics from Sproat 2014 |
| `fetch_or_prepare_corpus.py` | Adapter stubs for LDC corpora |
| `run_entropy_metrics.py` | Compute H₀, H₁, block entropy for IVS |
| `run_repetition_metrics.py` | Compute r/R repetition rate for IVS |
| `run_comparison_report.py` | Compare IVS metrics vs Sproat reference stats |

## Running

```bash
# Compute IVS metrics and compare against published Sproat benchmarks
python scripts/benchmarks/non_linguistic_sproat2014/run_comparison_report.py
```

Output: `outputs/benchmarks/sproat_comparison_report.csv` and `.md`
