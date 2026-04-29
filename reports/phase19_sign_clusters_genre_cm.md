# Phase-19 follow-up — A (sign clustering) + K (genre CDLI) + D (Cypro-Minoan)

## [A] Sign clustering on M77 (mapped + raw) + CISI mayig

| corpus | n_signs_total | n_eligible | n_clusters | n_signs_in_multi_clusters |
|---|---:|---:|---:|---:|
| m77_mapped | 64 | 61 | 3 | 20 |
| m77_raw | 337 | 194 | 21 | 70 |
| cisi_mayig | 182 | 105 | 7 | 53 |

Top 5 M77-mapped clusters (size, members):

- size=16: `034, 106, 157, 237, 307, 427, 461, 520, 617, 708, 712, 718, 817, 855, 858, 866`
- size=2: `003, 413`
- size=2: `047, 920`

## [K] Genre-stratified CDLI baselines

New per-genre Sumerian/Akkadian DoF measurements. Compare these to M77
to see if a *specific* genre is structurally closer than the raw
language baseline.

| bucket | n_tokens | V | zipf_a | mi_gamma | eps2 | eps3 | h1_norm |
|---|---:|---:|---|---|---|---|---|
| sum_ur3_admin | 231847 | 15185 | 1.1394 | 0.1747 | 0.5102 | 0.2537 | 0.6623 |
| sum_oblit_lit | 223223 | 52931 | 0.8325 | 0.024 | 0.6996 | 0.4532 | 0.8137 |
| akk_ob_admin | 120047 | 21851 | 0.8678 | 0.0712 | 0.6414 | 0.3912 | 0.7536 |
| akk_ob_letter | 151286 | 40145 | 0.677 | 0.0375 | 0.6356 | 0.3651 | 0.7397 |
| akk_na_royal | 360158 | 47167 | 1.0501 | 0.0554 | 0.7228 | 0.5214 | 0.7743 |

*M77 reference: zipf_a=0.978, mi_gamma=0.098, eps2=0.597, eps3=0.422, h1_norm=0.897*

## [D] M77 vs all 6 hypotheses (incl Cypro-Minoan typological control)

### M77 (rank-corr-mapped) ranking

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `cypro_minoan_morphology` | 0.0 | 0 | 1.4824 |
| 2 | `dravidian_morphology` | 0.1882 | 2 | 1.7829 |
| 3 | `indo_aryan_morphology` | 0.1882 | 1 | 1.6389 |
| 4 | `sumerian_morphology` | 0.1882 | 2 | 1.5644 |
| 5 | `akkadian_morphology` | 0.1882 | 2 | 1.5369 |
| 6 | `vedic_kalyanaraman_morphology` | 0.2776 | 5 | 1.3647 |

### M77 (raw OCR glyphs) ranking

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `dravidian_morphology` | 0.1858 | 1 | 1.8917 |
| 2 | `cypro_minoan_morphology` | 0.1858 | 1 | 1.5522 |
| 3 | `indo_aryan_morphology` | 0.2846 | 1 | 1.7375 |
| 4 | `sumerian_morphology` | 0.2846 | 1 | 1.6477 |
| 5 | `akkadian_morphology` | 0.4681 | 1 | 1.6284 |
| 6 | `vedic_kalyanaraman_morphology` | 0.7915 | 5 | 1.4395 |
