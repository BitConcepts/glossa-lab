# Phase-437 — Spec 052 (amended arm A): battery NB-1 on the Shakti corpus layer

Dataset: **the Shakti corpus layer (CISI-compilation lineage)**. Battery: **NB-1 (Spec 052 amendment as frozen)**. Freeze digest `83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019`; OSF registration 7cu23 (approved, public). Executed 2026-10-24 under the owner's execution order of 2026-10-24.

Lineage limit: The Shakti layer is a CISI-tradition compilation, a distinct lineage from the Soviet compilation and from Holdat/M77, but its editions cover substantially the same excavated objects: agreement is cross-compilation robustness, not independent discovery.

## Step-0 gates (amendment section 5, in order)

- **Gate A — Corpus pin: PASS**
- **Gate B — Population reproduction: PASS**
- **Gate C — Determinism: PASS**
- **Gate D — Thinness (NB-1.9): PASS**

## Census (gate B extraction, pinned layer)

- **primary**: 3045 rows; 11805 tokens; 557 distinct signs; sequences of length >= 3: 2068; classifiable signs: 90
- **sensitivity**: 5131 rows; 17216 tokens; 707 distinct signs; sequences of length >= 3: 2889; classifiable signs: 111

Census note: Sensitivity classifiability: sign 540 carries 22 total occurrences but only 13 in sequences of length >= 2; under NB-1.2/NB-1.3 (length-1 sequences enter no count) N(540) = 13 < 20, so it is not classifiable and the sensitivity classifiable count under NB-1 is 111, one below the freeze section 3 length-census figure of 112, which counted total occurrences. No gate turns on the sensitivity count; the primary count (90) is identical under both readings.

## Primary population — per-sign quantities (NB-1)

Sequences: 3045 total; 103 of length 1 (counted, entering no count); 2942 of length >= 2 (B = 2942); 2068 of length >= 3. Classifiable signs (N >= 20): 90 of 557.

| Sign | N | I | T | M | i | t | m | Bands |
|---|---|---|---|---|---|---|---|---|
| 740 | 1299 | 919 | 3 | 377 | 0.707 | 0.002 | 0.290 | INITIAL_STRONG |
| 002 | 549 | 26 | 7 | 516 | 0.047 | 0.013 | 0.940 | MEDIAL_STRONG |
| 700 | 384 | 362 | 8 | 14 | 0.943 | 0.021 | 0.036 | INITIAL_STRONG |
| 400 | 355 | 325 | 1 | 29 | 0.915 | 0.003 | 0.082 | INITIAL_STRONG |
| 032 | 334 | 8 | 150 | 176 | 0.024 | 0.449 | 0.527 | MEDIAL_MODERATE |
| 033 | 315 | 5 | 162 | 148 | 0.016 | 0.514 | 0.470 | TERMINAL_MODERATE |
| 220 | 286 | 19 | 37 | 230 | 0.066 | 0.129 | 0.804 | MEDIAL_STRONG |
| 240 | 254 | 1 | 67 | 186 | 0.004 | 0.264 | 0.732 | MEDIAL_STRONG |
| 520 | 246 | 213 | 1 | 32 | 0.866 | 0.004 | 0.130 | INITIAL_STRONG |
| 390 | 202 | 101 | 6 | 95 | 0.500 | 0.030 | 0.470 | INITIAL_MODERATE |
| 861 | 193 | 33 | 115 | 45 | 0.171 | 0.596 | 0.233 | TERMINAL_MODERATE |
| 235 | 188 | 1 | 85 | 102 | 0.005 | 0.452 | 0.543 | MEDIAL_MODERATE |
| 003 | 184 | 2 | 114 | 68 | 0.011 | 0.620 | 0.370 | TERMINAL_MODERATE |
| 176 | 167 | 0 | 76 | 91 | 0.000 | 0.455 | 0.545 | MEDIAL_MODERATE |
| 590 | 160 | 8 | 42 | 110 | 0.050 | 0.263 | 0.688 | MEDIAL_STRONG |
| 060 | 158 | 1 | 1 | 156 | 0.006 | 0.006 | 0.987 | MEDIAL_STRONG |
| 741 | 148 | 1 | 14 | 133 | 0.007 | 0.095 | 0.899 | MEDIAL_STRONG |
| 820 | 144 | 11 | 112 | 21 | 0.076 | 0.778 | 0.146 | TERMINAL_STRONG |
| 031 | 142 | 15 | 54 | 73 | 0.106 | 0.380 | 0.514 | MEDIAL_MODERATE |
| 817 | 140 | 2 | 127 | 11 | 0.014 | 0.907 | 0.079 | TERMINAL_STRONG |
| 233 | 136 | 1 | 28 | 107 | 0.007 | 0.206 | 0.787 | MEDIAL_STRONG |
| 705 | 135 | 2 | 42 | 91 | 0.015 | 0.311 | 0.674 | MEDIAL_STRONG |
| 001 | 128 | 11 | 7 | 110 | 0.086 | 0.055 | 0.859 | MEDIAL_STRONG |
| 034 | 124 | 4 | 117 | 3 | 0.032 | 0.944 | 0.024 | TERMINAL_STRONG |
| 415 | 117 | 6 | 42 | 69 | 0.051 | 0.359 | 0.590 | MEDIAL_MODERATE |
| 407 | 113 | 60 | 0 | 53 | 0.531 | 0.000 | 0.469 | INITIAL_MODERATE |
| 090 | 110 | 87 | 8 | 15 | 0.791 | 0.073 | 0.136 | INITIAL_STRONG |
| 920 | 108 | 3 | 61 | 44 | 0.028 | 0.565 | 0.407 | TERMINAL_MODERATE |
| 806 | 103 | 1 | 51 | 51 | 0.010 | 0.495 | 0.495 | — |
| 803 | 102 | 0 | 43 | 59 | 0.000 | 0.422 | 0.578 | MEDIAL_MODERATE |
| 798 | 93 | 0 | 28 | 65 | 0.000 | 0.301 | 0.699 | MEDIAL_STRONG |
| 255 | 91 | 1 | 38 | 52 | 0.011 | 0.418 | 0.571 | MEDIAL_MODERATE |
| 100 | 90 | 1 | 5 | 84 | 0.011 | 0.056 | 0.933 | MEDIAL_STRONG |
| 156 | 90 | 73 | 0 | 17 | 0.811 | 0.000 | 0.189 | INITIAL_STRONG |
| 405 | 87 | 29 | 1 | 57 | 0.333 | 0.011 | 0.655 | MEDIAL_MODERATE |
| 760 | 87 | 1 | 7 | 79 | 0.011 | 0.080 | 0.908 | MEDIAL_STRONG |
| 840 | 81 | 2 | 18 | 61 | 0.025 | 0.222 | 0.753 | MEDIAL_STRONG |
| 550 | 77 | 4 | 34 | 39 | 0.052 | 0.442 | 0.506 | MEDIAL_MODERATE |
| 061 | 74 | 0 | 20 | 54 | 0.000 | 0.270 | 0.730 | MEDIAL_STRONG |
| 690 | 72 | 5 | 12 | 55 | 0.069 | 0.167 | 0.764 | MEDIAL_STRONG |
| 368 | 71 | 25 | 4 | 42 | 0.352 | 0.056 | 0.592 | MEDIAL_MODERATE |
| 900 | 71 | 1 | 11 | 59 | 0.014 | 0.155 | 0.831 | MEDIAL_STRONG |
| 706 | 70 | 4 | 27 | 39 | 0.057 | 0.386 | 0.557 | MEDIAL_MODERATE |
| 151 | 69 | 61 | 1 | 7 | 0.884 | 0.014 | 0.101 | INITIAL_STRONG |
| 503 | 68 | 1 | 51 | 16 | 0.015 | 0.750 | 0.235 | TERMINAL_STRONG |
| 140 | 66 | 4 | 28 | 34 | 0.061 | 0.424 | 0.515 | MEDIAL_MODERATE |
| 231 | 63 | 1 | 20 | 42 | 0.016 | 0.317 | 0.667 | MEDIAL_STRONG |
| 004 | 62 | 2 | 24 | 36 | 0.032 | 0.387 | 0.581 | MEDIAL_MODERATE |
| 017 | 62 | 0 | 17 | 45 | 0.000 | 0.274 | 0.726 | MEDIAL_STRONG |
| 892 | 61 | 19 | 10 | 32 | 0.311 | 0.164 | 0.525 | MEDIAL_MODERATE |
| 617 | 56 | 36 | 12 | 8 | 0.643 | 0.214 | 0.143 | INITIAL_MODERATE |
| 615 | 55 | 1 | 5 | 49 | 0.018 | 0.091 | 0.891 | MEDIAL_STRONG |
| 435 | 52 | 4 | 1 | 47 | 0.077 | 0.019 | 0.904 | MEDIAL_STRONG |
| 142 | 51 | 2 | 17 | 32 | 0.039 | 0.333 | 0.627 | MEDIAL_MODERATE |
| 575 | 51 | 1 | 12 | 38 | 0.020 | 0.235 | 0.745 | MEDIAL_STRONG |
| 527 | 48 | 42 | 2 | 4 | 0.875 | 0.042 | 0.083 | INITIAL_STRONG |
| 752 | 47 | 0 | 1 | 46 | 0.000 | 0.021 | 0.979 | MEDIAL_STRONG |
| 845 | 47 | 0 | 0 | 47 | 0.000 | 0.000 | 1.000 | MEDIAL_STRONG |
| 055 | 45 | 0 | 12 | 33 | 0.000 | 0.267 | 0.733 | MEDIAL_STRONG |
| 125 | 44 | 2 | 14 | 28 | 0.045 | 0.318 | 0.636 | MEDIAL_MODERATE |
| 692 | 41 | 0 | 36 | 5 | 0.000 | 0.878 | 0.122 | TERMINAL_STRONG |
| 005 | 40 | 1 | 22 | 17 | 0.025 | 0.550 | 0.425 | TERMINAL_MODERATE |
| 413 | 40 | 3 | 33 | 4 | 0.075 | 0.825 | 0.100 | TERMINAL_STRONG |
| 416 | 37 | 6 | 23 | 8 | 0.162 | 0.622 | 0.216 | TERMINAL_MODERATE |
| 923 | 37 | 0 | 3 | 34 | 0.000 | 0.081 | 0.919 | MEDIAL_STRONG |
| 585 | 36 | 1 | 0 | 35 | 0.028 | 0.000 | 0.972 | MEDIAL_STRONG |
| 904 | 36 | 2 | 5 | 29 | 0.056 | 0.139 | 0.806 | MEDIAL_STRONG |
| 016 | 34 | 2 | 15 | 17 | 0.059 | 0.441 | 0.500 | MEDIAL_MODERATE |
| 440 | 33 | 1 | 10 | 22 | 0.030 | 0.303 | 0.667 | MEDIAL_STRONG |
| 717 | 33 | 1 | 14 | 18 | 0.030 | 0.424 | 0.545 | MEDIAL_MODERATE |
| 388 | 32 | 0 | 7 | 25 | 0.000 | 0.219 | 0.781 | MEDIAL_STRONG |
| 850 | 32 | 2 | 8 | 22 | 0.062 | 0.250 | 0.688 | MEDIAL_STRONG |
| 154 | 31 | 23 | 0 | 8 | 0.742 | 0.000 | 0.258 | INITIAL_STRONG |
| 335 | 31 | 1 | 1 | 29 | 0.032 | 0.032 | 0.935 | MEDIAL_STRONG |
| 482 | 31 | 3 | 3 | 25 | 0.097 | 0.097 | 0.806 | MEDIAL_STRONG |
| 501 | 30 | 0 | 29 | 1 | 0.000 | 0.967 | 0.033 | TERMINAL_STRONG |
| 595 | 29 | 7 | 3 | 19 | 0.241 | 0.103 | 0.655 | MEDIAL_MODERATE |
| 630 | 27 | 0 | 16 | 11 | 0.000 | 0.593 | 0.407 | TERMINAL_MODERATE |
| 158 | 26 | 11 | 1 | 14 | 0.423 | 0.038 | 0.538 | MEDIAL_MODERATE |
| 460 | 26 | 0 | 2 | 24 | 0.000 | 0.077 | 0.923 | MEDIAL_STRONG |
| 742 | 26 | 1 | 4 | 21 | 0.038 | 0.154 | 0.808 | MEDIAL_STRONG |
| 455 | 25 | 1 | 6 | 18 | 0.040 | 0.240 | 0.720 | MEDIAL_STRONG |
| 070 | 24 | 0 | 1 | 23 | 0.000 | 0.042 | 0.958 | MEDIAL_STRONG |
| 350 | 24 | 1 | 3 | 20 | 0.042 | 0.125 | 0.833 | MEDIAL_STRONG |
| 790 | 24 | 7 | 6 | 11 | 0.292 | 0.250 | 0.458 | — |
| 013 | 23 | 1 | 13 | 9 | 0.043 | 0.565 | 0.391 | TERMINAL_MODERATE |
| 236 | 23 | 8 | 4 | 11 | 0.348 | 0.174 | 0.478 | — |
| 226 | 21 | 14 | 4 | 3 | 0.667 | 0.190 | 0.143 | INITIAL_STRONG |
| 384 | 21 | 0 | 4 | 17 | 0.000 | 0.190 | 0.810 | MEDIAL_STRONG |
| 745 | 20 | 0 | 8 | 12 | 0.000 | 0.400 | 0.600 | MEDIAL_MODERATE |

Signs below the classifiability floor (N < 20), reported with their counts and marked TOO THIN for this population: 467. Their full counts (N, I, T, M, total occurrences) are carried per sign in reports/phase437_results.json (per_sign); none is a member of any strong set and none was dropped.

Strong sets — TERMINAL_STRONG (7): ['034', '413', '501', '503', '692', '817', '820']; INITIAL_STRONG (10): ['090', '151', '154', '156', '226', '400', '520', '527', '700', '740']; MEDIAL_STRONG (38): ['001', '002', '017', '055', '060', '061', '070', '100', '220', '231', '233', '240', '335', '350', '384', '388', '435', '440', '455', '460', '482', '575', '585', '590', '615', '690', '705', '741', '742', '752', '760', '798', '840', '845', '850', '900', '904', '923']. Moderate sets — terminal 8, initial 3, medial 21 (full lists in the results JSON).

Opening bigrams: most frequent ['400', '740'] with count 179 over B = 2942 (dominance 0.0608); 735 distinct opening bigrams. Permutation null (999 permutations, seed 43052): TERMINAL_STRONG count chance level 0 (null min/median/max 0/0/0); maximum opening-bigram count chance level 76 (null min/median/max 64/68/84).

Conditions: F HOLDS (observed 7 vs chance 0); O HOLDS (top count 179 vs floor 10 and chance 76).

## Sensitivity population — per-sign quantities (NB-1)

Sequences: 5131 total; 838 of length 1 (counted, entering no count); 4293 of length >= 2 (B = 4293); 2889 of length >= 3. Classifiable signs (N >= 20): 111 of 707.

| Sign | N | I | T | M | i | t | m | Bands |
|---|---|---|---|---|---|---|---|---|
| 740 | 1750 | 1190 | 47 | 513 | 0.680 | 0.027 | 0.293 | INITIAL_STRONG |
| 002 | 788 | 60 | 57 | 671 | 0.076 | 0.072 | 0.852 | MEDIAL_STRONG |
| 032 | 501 | 48 | 194 | 259 | 0.096 | 0.387 | 0.517 | MEDIAL_MODERATE |
| 700 | 498 | 385 | 88 | 25 | 0.773 | 0.177 | 0.050 | INITIAL_STRONG |
| 400 | 472 | 429 | 4 | 39 | 0.909 | 0.008 | 0.083 | INITIAL_STRONG |
| 033 | 433 | 59 | 179 | 195 | 0.136 | 0.413 | 0.450 | — |
| 220 | 426 | 56 | 69 | 301 | 0.131 | 0.162 | 0.707 | MEDIAL_STRONG |
| 240 | 339 | 14 | 94 | 231 | 0.041 | 0.277 | 0.681 | MEDIAL_STRONG |
| 520 | 299 | 245 | 4 | 50 | 0.819 | 0.013 | 0.167 | INITIAL_STRONG |
| 390 | 262 | 127 | 15 | 120 | 0.485 | 0.057 | 0.458 | — |
| 861 | 251 | 41 | 160 | 50 | 0.163 | 0.637 | 0.199 | TERMINAL_MODERATE |
| 003 | 240 | 15 | 137 | 88 | 0.062 | 0.571 | 0.367 | TERMINAL_MODERATE |
| 235 | 240 | 12 | 101 | 127 | 0.050 | 0.421 | 0.529 | MEDIAL_MODERATE |
| 031 | 226 | 32 | 83 | 111 | 0.142 | 0.367 | 0.491 | — |
| 060 | 217 | 9 | 5 | 203 | 0.041 | 0.023 | 0.935 | MEDIAL_STRONG |
| 590 | 214 | 20 | 57 | 137 | 0.093 | 0.266 | 0.640 | MEDIAL_MODERATE |
| 741 | 211 | 10 | 24 | 177 | 0.047 | 0.114 | 0.839 | MEDIAL_STRONG |
| 817 | 207 | 8 | 180 | 19 | 0.039 | 0.870 | 0.092 | TERMINAL_STRONG |
| 820 | 207 | 19 | 160 | 28 | 0.092 | 0.773 | 0.135 | TERMINAL_STRONG |
| 176 | 206 | 10 | 86 | 110 | 0.049 | 0.417 | 0.534 | MEDIAL_MODERATE |
| 705 | 202 | 10 | 61 | 131 | 0.050 | 0.302 | 0.649 | MEDIAL_MODERATE |
| 001 | 195 | 21 | 17 | 157 | 0.108 | 0.087 | 0.805 | MEDIAL_STRONG |
| 233 | 188 | 13 | 46 | 129 | 0.069 | 0.245 | 0.686 | MEDIAL_STRONG |
| 415 | 167 | 12 | 63 | 92 | 0.072 | 0.377 | 0.551 | MEDIAL_MODERATE |
| 090 | 166 | 115 | 20 | 31 | 0.693 | 0.120 | 0.187 | INITIAL_STRONG |
| 034 | 151 | 25 | 120 | 6 | 0.166 | 0.795 | 0.040 | TERMINAL_STRONG |
| 920 | 147 | 7 | 85 | 55 | 0.048 | 0.578 | 0.374 | TERMINAL_MODERATE |
| 798 | 143 | 8 | 41 | 94 | 0.056 | 0.287 | 0.657 | MEDIAL_MODERATE |
| 407 | 141 | 79 | 2 | 60 | 0.560 | 0.014 | 0.426 | INITIAL_MODERATE |
| 255 | 129 | 8 | 53 | 68 | 0.062 | 0.411 | 0.527 | MEDIAL_MODERATE |
| 760 | 129 | 5 | 16 | 108 | 0.039 | 0.124 | 0.837 | MEDIAL_STRONG |
| 100 | 128 | 8 | 10 | 110 | 0.062 | 0.078 | 0.859 | MEDIAL_STRONG |
| 806 | 128 | 5 | 61 | 62 | 0.039 | 0.477 | 0.484 | — |
| 803 | 126 | 4 | 49 | 73 | 0.032 | 0.389 | 0.579 | MEDIAL_MODERATE |
| 368 | 113 | 39 | 10 | 64 | 0.345 | 0.088 | 0.566 | MEDIAL_MODERATE |
| 550 | 113 | 12 | 46 | 55 | 0.106 | 0.407 | 0.487 | — |
| 405 | 112 | 43 | 3 | 66 | 0.384 | 0.027 | 0.589 | MEDIAL_MODERATE |
| 840 | 112 | 7 | 29 | 76 | 0.062 | 0.259 | 0.679 | MEDIAL_STRONG |
| 690 | 111 | 24 | 17 | 70 | 0.216 | 0.153 | 0.631 | MEDIAL_MODERATE |
| 900 | 107 | 4 | 24 | 79 | 0.037 | 0.224 | 0.738 | MEDIAL_STRONG |
| 140 | 101 | 10 | 47 | 44 | 0.099 | 0.465 | 0.436 | — |
| 156 | 98 | 77 | 3 | 18 | 0.786 | 0.031 | 0.184 | INITIAL_STRONG |
| 706 | 95 | 8 | 33 | 54 | 0.084 | 0.347 | 0.568 | MEDIAL_MODERATE |
| 061 | 90 | 3 | 22 | 65 | 0.033 | 0.244 | 0.722 | MEDIAL_STRONG |
| 231 | 90 | 5 | 27 | 58 | 0.056 | 0.300 | 0.644 | MEDIAL_MODERATE |
| 004 | 88 | 9 | 34 | 45 | 0.102 | 0.386 | 0.511 | MEDIAL_MODERATE |
| 151 | 87 | 76 | 1 | 10 | 0.874 | 0.011 | 0.115 | INITIAL_STRONG |
| 503 | 81 | 1 | 58 | 22 | 0.012 | 0.716 | 0.272 | TERMINAL_STRONG |
| 017 | 80 | 2 | 20 | 58 | 0.025 | 0.250 | 0.725 | MEDIAL_STRONG |
| 892 | 79 | 22 | 15 | 42 | 0.278 | 0.190 | 0.532 | MEDIAL_MODERATE |
| 142 | 77 | 5 | 25 | 47 | 0.065 | 0.325 | 0.610 | MEDIAL_MODERATE |
| 617 | 75 | 46 | 17 | 12 | 0.613 | 0.227 | 0.160 | INITIAL_MODERATE |
| 575 | 74 | 1 | 27 | 46 | 0.014 | 0.365 | 0.622 | MEDIAL_MODERATE |
| 692 | 73 | 4 | 56 | 13 | 0.055 | 0.767 | 0.178 | TERMINAL_STRONG |
| 435 | 72 | 7 | 7 | 58 | 0.097 | 0.097 | 0.806 | MEDIAL_STRONG |
| 615 | 67 | 3 | 7 | 57 | 0.045 | 0.104 | 0.851 | MEDIAL_STRONG |
| 904 | 63 | 8 | 10 | 45 | 0.127 | 0.159 | 0.714 | MEDIAL_STRONG |
| 527 | 62 | 52 | 3 | 7 | 0.839 | 0.048 | 0.113 | INITIAL_STRONG |
| 388 | 57 | 5 | 17 | 35 | 0.088 | 0.298 | 0.614 | MEDIAL_MODERATE |
| 585 | 57 | 4 | 2 | 51 | 0.070 | 0.035 | 0.895 | MEDIAL_STRONG |
| 125 | 55 | 7 | 17 | 31 | 0.127 | 0.309 | 0.564 | MEDIAL_MODERATE |
| 845 | 55 | 2 | 1 | 52 | 0.036 | 0.018 | 0.945 | MEDIAL_STRONG |
| 055 | 54 | 2 | 17 | 35 | 0.037 | 0.315 | 0.648 | MEDIAL_MODERATE |
| 717 | 54 | 5 | 18 | 31 | 0.093 | 0.333 | 0.574 | MEDIAL_MODERATE |
| 752 | 53 | 0 | 2 | 51 | 0.000 | 0.038 | 0.962 | MEDIAL_STRONG |
| 413 | 52 | 5 | 40 | 7 | 0.096 | 0.769 | 0.135 | TERMINAL_STRONG |
| 850 | 51 | 8 | 11 | 32 | 0.157 | 0.216 | 0.627 | MEDIAL_MODERATE |
| 790 | 49 | 16 | 18 | 15 | 0.327 | 0.367 | 0.306 | — |
| 016 | 48 | 3 | 21 | 24 | 0.062 | 0.438 | 0.500 | MEDIAL_MODERATE |
| 005 | 47 | 2 | 25 | 20 | 0.043 | 0.532 | 0.426 | TERMINAL_MODERATE |
| 595 | 47 | 14 | 4 | 29 | 0.298 | 0.085 | 0.617 | MEDIAL_MODERATE |
| 416 | 46 | 9 | 27 | 10 | 0.196 | 0.587 | 0.217 | TERMINAL_MODERATE |
| 440 | 45 | 3 | 13 | 29 | 0.067 | 0.289 | 0.644 | MEDIAL_MODERATE |
| 742 | 45 | 7 | 8 | 30 | 0.156 | 0.178 | 0.667 | MEDIAL_STRONG |
| 350 | 44 | 1 | 9 | 34 | 0.023 | 0.205 | 0.773 | MEDIAL_STRONG |
| 335 | 43 | 3 | 5 | 35 | 0.070 | 0.116 | 0.814 | MEDIAL_STRONG |
| 923 | 43 | 0 | 5 | 38 | 0.000 | 0.116 | 0.884 | MEDIAL_STRONG |
| 154 | 42 | 34 | 0 | 8 | 0.810 | 0.000 | 0.190 | INITIAL_STRONG |
| 455 | 41 | 8 | 9 | 24 | 0.195 | 0.220 | 0.585 | MEDIAL_MODERATE |
| 482 | 41 | 4 | 6 | 31 | 0.098 | 0.146 | 0.756 | MEDIAL_STRONG |
| 832 | 41 | 14 | 12 | 15 | 0.341 | 0.293 | 0.366 | — |
| 158 | 38 | 16 | 3 | 19 | 0.421 | 0.079 | 0.500 | MEDIAL_MODERATE |
| 460 | 38 | 2 | 4 | 32 | 0.053 | 0.105 | 0.842 | MEDIAL_STRONG |
| 013 | 37 | 1 | 15 | 21 | 0.027 | 0.405 | 0.568 | MEDIAL_MODERATE |
| 070 | 37 | 0 | 6 | 31 | 0.000 | 0.162 | 0.838 | MEDIAL_STRONG |
| 226 | 35 | 23 | 4 | 8 | 0.657 | 0.114 | 0.229 | INITIAL_MODERATE |
| 630 | 35 | 0 | 21 | 14 | 0.000 | 0.600 | 0.400 | TERMINAL_MODERATE |
| 480 | 33 | 2 | 12 | 19 | 0.061 | 0.364 | 0.576 | MEDIAL_MODERATE |
| 501 | 31 | 0 | 29 | 2 | 0.000 | 0.935 | 0.065 | TERMINAL_STRONG |
| 165 | 29 | 11 | 8 | 10 | 0.379 | 0.276 | 0.345 | — |
| 384 | 29 | 1 | 7 | 21 | 0.034 | 0.241 | 0.724 | MEDIAL_STRONG |
| 632 | 29 | 0 | 15 | 14 | 0.000 | 0.517 | 0.483 | TERMINAL_MODERATE |
| 095 | 28 | 2 | 9 | 17 | 0.071 | 0.321 | 0.607 | MEDIAL_MODERATE |
| 824 | 28 | 18 | 10 | 0 | 0.643 | 0.357 | 0.000 | INITIAL_MODERATE |
| 035 | 27 | 10 | 5 | 12 | 0.370 | 0.185 | 0.444 | — |
| 171 | 27 | 2 | 16 | 9 | 0.074 | 0.593 | 0.333 | TERMINAL_MODERATE |
| 495 | 27 | 1 | 13 | 13 | 0.037 | 0.481 | 0.481 | — |
| 745 | 27 | 0 | 12 | 15 | 0.000 | 0.444 | 0.556 | MEDIAL_MODERATE |
| 175 | 24 | 0 | 12 | 12 | 0.000 | 0.500 | 0.500 | MEDIAL_MODERATE, TERMINAL_MODERATE |
| 236 | 24 | 9 | 4 | 11 | 0.375 | 0.167 | 0.458 | — |
| 104 | 23 | 4 | 16 | 3 | 0.174 | 0.696 | 0.130 | TERMINAL_STRONG |
| 500 | 23 | 1 | 3 | 19 | 0.043 | 0.130 | 0.826 | MEDIAL_STRONG |
| 555 | 23 | 1 | 3 | 19 | 0.043 | 0.130 | 0.826 | MEDIAL_STRONG |
| 621 | 22 | 17 | 3 | 2 | 0.773 | 0.136 | 0.091 | INITIAL_STRONG |
| 636 | 22 | 1 | 3 | 18 | 0.045 | 0.136 | 0.818 | MEDIAL_STRONG |
| 645 | 22 | 3 | 3 | 16 | 0.136 | 0.136 | 0.727 | MEDIAL_STRONG |
| 711 | 21 | 5 | 2 | 14 | 0.238 | 0.095 | 0.667 | MEDIAL_STRONG |
| 091 | 20 | 0 | 18 | 2 | 0.000 | 0.900 | 0.100 | TERMINAL_STRONG |
| 097 | 20 | 0 | 9 | 11 | 0.000 | 0.450 | 0.550 | MEDIAL_MODERATE |
| 463 | 20 | 1 | 3 | 16 | 0.050 | 0.150 | 0.800 | MEDIAL_STRONG |
| 877 | 20 | 3 | 8 | 9 | 0.150 | 0.400 | 0.450 | — |

Signs below the classifiability floor (N < 20), reported with their counts and marked TOO THIN for this population: 596. Their full counts (N, I, T, M, total occurrences) are carried per sign in reports/phase437_results.json (per_sign); none is a member of any strong set and none was dropped.

Strong sets — TERMINAL_STRONG (9): ['034', '091', '104', '413', '501', '503', '692', '817', '820']; INITIAL_STRONG (10): ['090', '151', '154', '156', '400', '520', '527', '621', '700', '740']; MEDIAL_STRONG (33): ['001', '002', '017', '060', '061', '070', '100', '220', '233', '240', '335', '350', '384', '435', '460', '463', '482', '500', '555', '585', '615', '636', '645', '711', '741', '742', '752', '760', '840', '845', '900', '904', '923']. Moderate sets — terminal 9, initial 4, medial 34 (full lists in the results JSON).

Opening bigrams: most frequent ['400', '740'] with count 235 over B = 4293 (dominance 0.0547); 1345 distinct opening bigrams. Permutation null (999 permutations, seed 43052): TERMINAL_STRONG count chance level 0 (null min/median/max 0/0/1); maximum opening-bigram count chance level 95 (null min/median/max 80/86/107).

Conditions: F HOLDS (observed 9 vs chance 0); O HOLDS (top count 235 vs floor 10 and chance 95).

## Outcome

Spec 052 (Phase-437), executed 2026-10-24 under the frozen amended contract (freeze digest 83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019; OSF registration 7cu23): battery NB-1 (Spec 052 amendment as frozen) run on the Shakti corpus layer (CISI-compilation lineage), primary population 3,045 inscriptions / 11,805 tokens / 557 signs. Condition F (dedicated final sets): holds — 7 TERMINAL_STRONG sign(s) against a permutation-null chance level of 0 (999 permutations, seed 43052). Condition O (opening formula): holds — the most frequent opening bigram (400, 740) recurs 179 times (dominance 0.0608 over B = 2942) against a chance level of 76 occurrences. Outcome: INCONSISTENT. Both conditions hold: positional structure of the kind the thesis denies is present in this compilation, and the caveat widens. The sensitivity population's run returned INCONSISTENT under the same battery. The parent claim's contradicted status stands as recorded; this outcome moves no verdict and is not a verdict on the Farmer-Sproat-Witzel thesis.

## Limits

- No verdict moves: the parent claim (`farmer_sproat_witzel_2004_manual_001`) stands contradicted as recorded; this run narrows or widens the stated caveat only, and is not a verdict on the Farmer-Sproat-Witzel thesis.
- The Shakti layer is a CISI-tradition compilation, a distinct lineage from the Soviet compilation and from Holdat/M77, but its editions cover substantially the same excavated objects: agreement is cross-compilation robustness, not independent discovery.
- Consistency is not replication of the whole case: nothing here speaks to what language the signs encode, to any sign's reading, or to conditional entropy.
- Negative, partial, thin, and not-adjudicated outcomes publish with the same prominence as a consistent one.
