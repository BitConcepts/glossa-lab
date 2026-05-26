# IVS vs Non-Linguistic Systems: Sproat 2014 Benchmark Comparison

## Purpose

This report compares IVS statistical metrics against Sproat's (2014)
non-linguistic symbol system benchmarks. Per Sproat 2014, conditional
entropy alone does not distinguish writing from structured non-linguistic
systems. The r/R repetition rate is the cleanest discriminator.

## IVS Metrics

- **H0 (unigram entropy)**: 6.9549 bits
- **H1 (conditional entropy)**: 3.5306 bits
- **Zipf slope**: -1.7046
- **r/R repetition rate**: 0.83
- **Corpus**: 7138 inscriptions, 24502 tokens, 649 types

## r/R Comparison (Sproat's discriminator)

| System | Type | r/R |
|--------|------|-----|
| Indus Valley Script (IVS) | unknown (tested) | 0.83 |
| Totem Poles | non_linguistic | 0.63 |
| Pictish Stones | non_linguistic | None |
| Vinča Symbols | non_linguistic | None |
| Mesopotamian Deity Symbols (Kudurrus) | non_linguistic | None |
| Weather Icons | non_linguistic | 0.79 |
| Barn Stars (Hex Signs) | non_linguistic | 0.85 |
| Ancient Chinese (Oracle Bone) | linguistic | 0.048 |
| Amharic | linguistic | 0.018 |
| Oriya | linguistic | 0.0075 |

## Interpretation

Linguistic systems typically have r/R < 0.10; non-linguistic systems
typically have r/R > 0.50 (Sproat 2014). IVS r/R should be evaluated
against these thresholds. However, r/R is partially confounded with
text length — non-linguistic texts tend to be shorter.

**Key finding from Sproat 2014**: Neither conditional entropy (Rao et al.)
nor Lee et al.'s Cr measure at published settings reliably separates
linguistic from non-linguistic systems. The manuscript should not treat
conditional entropy as proof of linguistic status.

## References

- Sproat, R. (2014). A statistical comparison of written language and
  nonlinguistic symbol systems. *Language*, 90(2), 457-481.
- Sproat, R. (2023). *Symbols: An Evolutionary History from the Stone Age
  to the Future*. Springer.