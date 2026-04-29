# Phase-19 omnibus — Tier-1 (B/C/E) + Tier-3 (J/L)

## [B] Multi-hypothesis projection at 8/7/6 DoF

Removing the high-eps3 outlier DoF (and h1_norm secondarily) tells us
whether the Phase-18 4-way tie is structural or driven by one signal.

### 8-DoF baseline

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `dravidian_morphology` | 0.1882 | 2 | 1.7829 |
| 2 | `indo_aryan_morphology` | 0.1882 | 1 | 1.6389 |
| 3 | `sumerian_morphology` | 0.1882 | 2 | 1.5644 |
| 4 | `akkadian_morphology` | 0.1882 | 2 | 1.5369 |
| 5 | `vedic_kalyanaraman_morphology` | 0.2776 | 5 | 1.3647 |

### 7-DoF (excl eps3)

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `dravidian_morphology` | 0.1882 | 2 | 1.7829 |
| 2 | `indo_aryan_morphology` | 0.1882 | 1 | 1.6389 |
| 3 | `sumerian_morphology` | 0.1882 | 2 | 1.5644 |
| 4 | `akkadian_morphology` | 0.1882 | 2 | 1.5369 |
| 5 | `vedic_kalyanaraman_morphology` | 0.2285 | 4 | 1.3647 |

### 6-DoF (excl eps3 + h1_norm)

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `dravidian_morphology` | 0.1882 | 2 | 1.7829 |
| 2 | `indo_aryan_morphology` | 0.1882 | 1 | 1.6389 |
| 3 | `sumerian_morphology` | 0.1882 | 1 | 1.5644 |
| 4 | `akkadian_morphology` | 0.1882 | 1 | 1.5369 |
| 5 | `vedic_kalyanaraman_morphology` | 0.2285 | 4 | 1.3647 |

## [C] Raw M77 (no rank-corr) DoFs

```
  n_tokens                 = 6771
  n_types                  = 337
  zipf_alpha               = 1.5415
  zipf_r2                  = 0.9194
  mi_gamma                 = 0.0714
  mi_r2_pow                = 0.9915
  epistatic_2nd_norm       = 0.6423
  epistatic_3rd_norm       = 0.4486
  h1_norm                  = 0.7771
  h1_nats                  = 4.5227
```

### Raw M77 7-DoF projection

| rank | hypothesis | max_v | n_viol | score |
|---|---|---|---|---|
| 1 | `dravidian_morphology` | 0.1858 | 1 | 1.8917 |
| 2 | `indo_aryan_morphology` | 0.2846 | 1 | 1.7375 |
| 3 | `sumerian_morphology` | 0.2846 | 1 | 1.6477 |
| 4 | `akkadian_morphology` | 0.4681 | 1 | 1.6284 |
| 5 | `vedic_kalyanaraman_morphology` | 0.7915 | 4 | 1.4395 |

## [E] Top epistatic trigrams in M77 (mapped)

Trigrams with the strongest 3-way coupling beyond independence.
Likely candidates for stable seal-formula motifs.

| rank | trigram | count | i3_bits |
|---:|---|---:|---:|
| 1 | `375 375 375` | 30 | 14.684 |
| 2 | `876 876 876` | 20 | 14.099 |
| 3 | `872 872 872` | 23 | 14.0383 |
| 4 | `841 841 147` | 3 | 13.5443 |
| 5 | `841 147 841` | 3 | 13.5443 |
| 6 | `394 394 394` | 43 | 13.5396 |
| 7 | `719 719 719` | 23 | 13.228 |
| 8 | `416 416 416` | 53 | 13.161 |
| 9 | `526 526 526` | 28 | 13.0138 |
| 10 | `527 527 527` | 56 | 12.8638 |
| 11 | `841 841 841` | 13 | 12.7338 |
| 12 | `151 151 151` | 60 | 12.684 |
| 13 | `503 503 503` | 54 | 12.6002 |
| 14 | `169 169 169` | 66 | 12.5591 |
| 15 | `723 723 782` | 13 | 12.477 |
| 16 | `723 782 723` | 12 | 12.3616 |
| 17 | `387 866 176` | 4 | 12.3259 |
| 18 | `723 782 782` | 11 | 12.3082 |
| 19 | `782 723 782` | 11 | 12.3082 |
| 20 | `782 723 723` | 11 | 12.236 |

## [J] Per-inscription DoF distributions (mean +/- stdev)

Reveals heterogeneity within each corpus. Large stdev = corpus is mixed.

| corpus | n_elig | zipf_a | eps2 | eps3 | h1_norm |
|---|---:|---|---|---|---|
| indus_m77 | 478 | 0.2682+-0.2888 | 0.5995+-0.4197 | 0.4595+-0.4039 | 0.6621+-0.418 |
| cisi_mayig | 144 | 0.0365+-0.1043 | 0.9961+-0.0123 | 0.9752+-0.0796 | 0.9966+-0.01 |
| damos_linear_b | 1742 | 0.2177+-0.2359 | 0.963+-0.068 | 0.8901+-0.1511 | 0.9787+-0.0339 |
| rv_padapatha | 1569 | 0.0548+-0.1249 | 0.9938+-0.0256 | 0.9775+-0.0681 | 0.9959+-0.0115 |

## [L] Spectral fingerprint — top bigram-transition eigenvalues

Continuous signature of the Markov structure. Spectral gap between
lambda_1 (always = 1 for stochastic) and lambda_2 measures mixing time;
small gap = slow mixing, more long-range structure.

| corpus | n_states | lambda_1..5 | gap |
|---|---:|---|---:|
| indus_m77 | 64 | 1.0 0.99 0.989 0.9852 0.9824 | 0.01 |
| cisi_mayig | 182 | 1.0 0.4934 0.4934 0.4418 0.4418 | 0.5066 |
| damos_linear_b | 201 | 1.0 0.5331 0.4038 0.4038 0.3694 | 0.4669 |
| rv_padapatha | 201 | 1.0 0.431 0.2172 0.2161 0.1162 | 0.569 |
| kee2u_tamil | 201 | 1.0 0.3953 0.3228 0.3228 0.3083 | 0.6047 |
| cdli_sumerian_ur3 | 201 | 1.0 0.5432 0.534 0.534 0.424 | 0.4568 |
| cdli_akkadian_na | 201 | 1.0 0.4695 0.4282 0.3806 0.3806 | 0.5305 |
| indus_m77_raw | 201 | 1.0 0.9904 0.9851 0.9818 0.9818 | 0.0096 |
