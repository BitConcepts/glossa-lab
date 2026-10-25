# Phase-438 — Spec 054 (amended): Yadav's opening/closing signs under battery NB-1

Claim under test: `yadav_2009_arxiv_manual_002` — "There are specific text-beginning and text-ending signs in the Indus corpus" (strongly supported as recorded; this run moves no claim status). Freeze digest `d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`; OSF registration 8spvf (approved, public). Executed 2026-10-24 under the owner's execution order of 2026-10-24.

## The falsifier (appended to the claim's record at the freeze, 2026-10-23)

> This claim, as evaluated under battery NB-1 (the Spec 054 amendment, as frozen), is falsified if any of the following holds when the frozen battery is run on the frozen arm-1 and arm-2 corpora: (1) either arm-1 positional-strong set (opening or closing) is empty; (2) for either class, fewer than half of arm 1's positional-strong signs are also positional-strong in arm 2 in the same class, through the pinned crosswalk; or (3) the pooled cross-arm overlap of positional-strong signs does not exceed the 95th percentile of the 999-shuffle label-permutation null — the three conditions applied under the precedence rule of the Spec 054 amendment (§5.5).

## Step-0 gates (amendment section 6, in order)

- **Gate G1 — Pin checks (draft 0.1): PASS**
- **Gate G2 — Strict corpus identification and pin (draft 0.3): PASS**
- **Gate G3 — Thinness (draft 0.5 census): PASS**
- **Gate G4 — Second arm runnability (draft 0.4): PASS**
- **Gate G5 — Determinism: PASS**

## Step-0 record — strict corpus identification (gate G2)

Reference census (C3, from the pinned Phase-43 record, T1_1): source "indusscript.in Firestore 'indusarrays' (2026-05-14)"; 3916 records; 2665 unique dockeys; 3137 sequences; 12494 sign instances.

C1 — the V3 loader's data file (the Firestore 'indusarrays' dump): found at /home/tpierson/workspace/glossa-lab/glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl.

C2 — database copies: no database copy exists in the execution tree; the programme database (backend/data/glossa.db, main checkout) holds 13 texts, of which the only Indus entry is the synthetic prototype ("Indus Script (synthetic, Yadav 2010 / Fuls 2014)", 923 inscriptions by its metadata) — not the V3 layer.

C4 — other layers held, censused; none is the corpus the Phase-43 record names, and none was substituted:

- **yajnadevam_inscriptions.csv (the programme's site-attributed layer; Specs 042/045's layer of record)** — records 5679. a different layer: not the Firestore 'indusarrays' reconstruction the Phase-43 record names (its record count also differs from C3's 3,916).
- **mayig CISI layer v1 (data/corpus_layers/mayig_cisi_layer_v1.json)** — inscriptions 179, tokens 1003, distinct_signs 182. the CISI compilation in Parpola numbering (Spec 019's arm) — a different compilation from the Mahadevan-lineage V3 layer.
- **indus_research.jsonl (the V1 research export)** — records 15508. a mixed-source-system export, not the Firestore 'indusarrays' reconstruction the Phase-43 record names.
- **the Holdat downloads layer (indus_corpus 2.csv; arm 2's layer)** — inscriptions 1670, tokens 7002, distinct_signs 390. the other compilation: the Phase-43 record itself treats it as a different corpus (its T4_3 cross-validation against V3); it is arm 2's layer, never a substitute for arm 1.

## ARM1 — per-sign quantities (NB-1)

Sequences: 3137 total; 0 of length 1 (counted, entering no count); 3137 of length >= 2; 2267 of length >= 3. Classifiable signs (N >= 20): 103 of 393.

| Sign | N | I | T | M | i | t | m | Bands |
|---|---|---|---|---|---|---|---|---|
| 342 | 1318 | 26 | 927 | 365 | 0.020 | 0.703 | 0.277 | TERMINAL_STRONG |
| 99 | 642 | 35 | 54 | 553 | 0.055 | 0.084 | 0.861 | MEDIAL_STRONG |
| 267 | 356 | 287 | 17 | 52 | 0.806 | 0.048 | 0.146 | INITIAL_STRONG |
| 176 | 344 | 0 | 307 | 37 | 0.000 | 0.892 | 0.108 | TERMINAL_STRONG |
| 87 | 344 | 143 | 20 | 181 | 0.416 | 0.058 | 0.526 | MEDIAL_MODERATE |
| 59 | 334 | 34 | 35 | 265 | 0.102 | 0.105 | 0.793 | MEDIAL_STRONG |
| 328 | 299 | 18 | 255 | 26 | 0.060 | 0.853 | 0.087 | TERMINAL_STRONG |
| 89 | 299 | 133 | 23 | 143 | 0.445 | 0.077 | 0.478 | — |
| 67 | 269 | 74 | 13 | 182 | 0.275 | 0.048 | 0.677 | MEDIAL_STRONG |
| 336 | 225 | 75 | 9 | 141 | 0.333 | 0.040 | 0.627 | MEDIAL_MODERATE |
| 169 | 223 | 6 | 121 | 96 | 0.027 | 0.543 | 0.430 | TERMINAL_MODERATE |
| 211 | 218 | 1 | 178 | 39 | 0.005 | 0.817 | 0.179 | TERMINAL_STRONG |
| 65 | 203 | 80 | 10 | 113 | 0.394 | 0.049 | 0.557 | MEDIAL_MODERATE |
| 162 | 202 | 12 | 89 | 101 | 0.059 | 0.441 | 0.500 | MEDIAL_MODERATE |
| 245 | 201 | 31 | 50 | 120 | 0.154 | 0.249 | 0.597 | MEDIAL_MODERATE |
| 123 | 187 | 6 | 12 | 169 | 0.032 | 0.064 | 0.904 | MEDIAL_STRONG |
| 391 | 183 | 130 | 17 | 36 | 0.710 | 0.093 | 0.197 | INITIAL_STRONG |
| 72 | 181 | 49 | 7 | 125 | 0.271 | 0.039 | 0.691 | MEDIAL_STRONG |
| 343 | 168 | 22 | 12 | 134 | 0.131 | 0.071 | 0.798 | MEDIAL_STRONG |
| 249 | 161 | 41 | 16 | 104 | 0.255 | 0.099 | 0.646 | MEDIAL_MODERATE |
| 48 | 159 | 70 | 6 | 83 | 0.440 | 0.038 | 0.522 | MEDIAL_MODERATE |
| 102 | 136 | 69 | 7 | 60 | 0.507 | 0.051 | 0.441 | INITIAL_MODERATE |
| 293 | 131 | 70 | 7 | 54 | 0.534 | 0.053 | 0.412 | INITIAL_MODERATE |
| 86 | 129 | 54 | 15 | 60 | 0.419 | 0.116 | 0.465 | — |
| 171 | 124 | 44 | 5 | 75 | 0.355 | 0.040 | 0.605 | MEDIAL_MODERATE |
| 53 | 124 | 40 | 7 | 77 | 0.323 | 0.056 | 0.621 | MEDIAL_MODERATE |
| 1 | 123 | 17 | 84 | 22 | 0.138 | 0.683 | 0.179 | TERMINAL_STRONG |
| 389 | 123 | 56 | 6 | 61 | 0.455 | 0.049 | 0.496 | — |
| 15 | 114 | 2 | 84 | 28 | 0.018 | 0.737 | 0.246 | TERMINAL_STRONG |
| 347 | 112 | 10 | 10 | 92 | 0.089 | 0.089 | 0.821 | MEDIAL_STRONG |
| 8 | 100 | 7 | 4 | 89 | 0.070 | 0.040 | 0.890 | MEDIAL_STRONG |
| 51 | 97 | 30 | 6 | 61 | 0.309 | 0.062 | 0.629 | MEDIAL_MODERATE |
| 387 | 95 | 33 | 4 | 58 | 0.347 | 0.042 | 0.611 | MEDIAL_MODERATE |
| 402 | 95 | 12 | 32 | 51 | 0.126 | 0.337 | 0.537 | MEDIAL_MODERATE |
| 97 | 89 | 4 | 7 | 78 | 0.045 | 0.079 | 0.876 | MEDIAL_STRONG |
| 403 | 88 | 20 | 4 | 64 | 0.227 | 0.045 | 0.727 | MEDIAL_STRONG |
| 149 | 86 | 9 | 22 | 55 | 0.105 | 0.256 | 0.640 | MEDIAL_MODERATE |
| 287 | 86 | 19 | 5 | 62 | 0.221 | 0.058 | 0.721 | MEDIAL_STRONG |
| 98 | 86 | 5 | 13 | 68 | 0.058 | 0.151 | 0.791 | MEDIAL_STRONG |
| 17 | 85 | 37 | 5 | 43 | 0.435 | 0.059 | 0.506 | MEDIAL_MODERATE |
| 244 | 85 | 29 | 5 | 51 | 0.341 | 0.059 | 0.600 | MEDIAL_MODERATE |
| 216 | 84 | 39 | 10 | 35 | 0.464 | 0.119 | 0.417 | — |
| 124 | 76 | 20 | 5 | 51 | 0.263 | 0.066 | 0.671 | MEDIAL_STRONG |
| 70 | 72 | 17 | 6 | 49 | 0.236 | 0.083 | 0.681 | MEDIAL_STRONG |
| 204 | 71 | 48 | 2 | 21 | 0.676 | 0.028 | 0.296 | INITIAL_STRONG |
| 254 | 70 | 3 | 58 | 9 | 0.043 | 0.829 | 0.129 | TERMINAL_STRONG |
| 12 | 68 | 2 | 59 | 7 | 0.029 | 0.868 | 0.103 | TERMINAL_STRONG |
| 121 | 67 | 13 | 6 | 48 | 0.194 | 0.090 | 0.716 | MEDIAL_STRONG |
| 112 | 66 | 19 | 1 | 46 | 0.288 | 0.015 | 0.697 | MEDIAL_STRONG |
| 104 | 65 | 30 | 5 | 30 | 0.462 | 0.077 | 0.462 | — |
| 307 | 63 | 13 | 18 | 32 | 0.206 | 0.286 | 0.508 | MEDIAL_MODERATE |
| 130 | 60 | 2 | 8 | 50 | 0.033 | 0.133 | 0.833 | MEDIAL_STRONG |
| 95 | 60 | 55 | 1 | 4 | 0.917 | 0.017 | 0.067 | INITIAL_STRONG |
| 150 | 59 | 47 | 2 | 10 | 0.797 | 0.034 | 0.169 | INITIAL_STRONG |
| 194 | 58 | 5 | 6 | 47 | 0.086 | 0.103 | 0.810 | MEDIAL_STRONG |
| 197 | 57 | 26 | 5 | 26 | 0.456 | 0.088 | 0.456 | — |
| 341 | 57 | 16 | 6 | 35 | 0.281 | 0.105 | 0.614 | MEDIAL_MODERATE |
| 373 | 57 | 17 | 14 | 26 | 0.298 | 0.246 | 0.456 | — |
| 375 | 52 | 14 | 13 | 25 | 0.269 | 0.250 | 0.481 | — |
| 175 | 50 | 18 | 5 | 27 | 0.360 | 0.100 | 0.540 | MEDIAL_MODERATE |
| 230 | 49 | 2 | 8 | 39 | 0.041 | 0.163 | 0.796 | MEDIAL_STRONG |
| 25 | 49 | 11 | 4 | 34 | 0.224 | 0.082 | 0.694 | MEDIAL_STRONG |
| 294 | 49 | 6 | 2 | 41 | 0.122 | 0.041 | 0.837 | MEDIAL_STRONG |
| 155 | 47 | 8 | 3 | 36 | 0.170 | 0.064 | 0.766 | MEDIAL_STRONG |
| 252 | 47 | 4 | 15 | 28 | 0.085 | 0.319 | 0.596 | MEDIAL_MODERATE |
| 28 | 47 | 17 | 6 | 24 | 0.362 | 0.128 | 0.511 | MEDIAL_MODERATE |
| 345 | 47 | 25 | 2 | 20 | 0.532 | 0.043 | 0.426 | INITIAL_MODERATE |
| 407 | 46 | 1 | 2 | 43 | 0.022 | 0.043 | 0.935 | MEDIAL_STRONG |
| 180 | 43 | 6 | 8 | 29 | 0.140 | 0.186 | 0.674 | MEDIAL_STRONG |
| 182 | 42 | 16 | 3 | 23 | 0.381 | 0.071 | 0.548 | MEDIAL_MODERATE |
| 127 | 40 | 8 | 5 | 27 | 0.200 | 0.125 | 0.675 | MEDIAL_STRONG |
| 327 | 39 | 11 | 3 | 25 | 0.282 | 0.077 | 0.641 | MEDIAL_MODERATE |
| 284 | 38 | 17 | 12 | 9 | 0.447 | 0.316 | 0.237 | — |
| 106 | 36 | 18 | 1 | 17 | 0.500 | 0.028 | 0.472 | INITIAL_MODERATE |
| 173 | 36 | 22 | 5 | 9 | 0.611 | 0.139 | 0.250 | INITIAL_MODERATE |
| 178 | 35 | 20 | 1 | 14 | 0.571 | 0.029 | 0.400 | INITIAL_MODERATE |
| 296 | 35 | 4 | 1 | 30 | 0.114 | 0.029 | 0.857 | MEDIAL_STRONG |
| 109 | 32 | 18 | 1 | 13 | 0.562 | 0.031 | 0.406 | INITIAL_MODERATE |
| 135 | 32 | 6 | 2 | 24 | 0.188 | 0.062 | 0.750 | MEDIAL_STRONG |
| 344 | 32 | 5 | 3 | 24 | 0.156 | 0.094 | 0.750 | MEDIAL_STRONG |
| 358 | 32 | 0 | 1 | 31 | 0.000 | 0.031 | 0.969 | MEDIAL_STRONG |
| 186 | 29 | 13 | 2 | 14 | 0.448 | 0.069 | 0.483 | — |
| 100 | 27 | 12 | 1 | 14 | 0.444 | 0.037 | 0.519 | MEDIAL_MODERATE |
| 319 | 27 | 6 | 9 | 12 | 0.222 | 0.333 | 0.444 | — |
| 261 | 26 | 9 | 4 | 13 | 0.346 | 0.154 | 0.500 | MEDIAL_MODERATE |
| 103 | 25 | 19 | 0 | 6 | 0.760 | 0.000 | 0.240 | INITIAL_STRONG |
| 233 | 25 | 5 | 2 | 18 | 0.200 | 0.080 | 0.720 | MEDIAL_STRONG |
| 326 | 25 | 5 | 2 | 18 | 0.200 | 0.080 | 0.720 | MEDIAL_STRONG |
| 60 | 25 | 2 | 18 | 5 | 0.080 | 0.720 | 0.200 | TERMINAL_STRONG |
| 193 | 24 | 3 | 0 | 21 | 0.125 | 0.000 | 0.875 | MEDIAL_STRONG |
| 205 | 24 | 17 | 1 | 6 | 0.708 | 0.042 | 0.250 | INITIAL_STRONG |
| 209 | 23 | 6 | 3 | 14 | 0.261 | 0.130 | 0.609 | MEDIAL_MODERATE |
| 153 | 22 | 7 | 2 | 13 | 0.318 | 0.091 | 0.591 | MEDIAL_MODERATE |
| 18 | 22 | 6 | 1 | 15 | 0.273 | 0.045 | 0.682 | MEDIAL_STRONG |
| 190 | 22 | 1 | 16 | 5 | 0.045 | 0.727 | 0.227 | TERMINAL_STRONG |
| 210 | 22 | 17 | 1 | 4 | 0.773 | 0.045 | 0.182 | INITIAL_STRONG |
| 222 | 22 | 3 | 1 | 18 | 0.136 | 0.045 | 0.818 | MEDIAL_STRONG |
| 253 | 21 | 10 | 3 | 8 | 0.476 | 0.143 | 0.381 | — |
| 137 | 20 | 4 | 4 | 12 | 0.200 | 0.200 | 0.600 | MEDIAL_MODERATE |
| 192 | 20 | 5 | 1 | 14 | 0.250 | 0.050 | 0.700 | MEDIAL_STRONG |
| 348 | 20 | 2 | 1 | 17 | 0.100 | 0.050 | 0.850 | MEDIAL_STRONG |
| 409 | 20 | 11 | 1 | 8 | 0.550 | 0.050 | 0.400 | INITIAL_MODERATE |
| 81 | 20 | 1 | 4 | 15 | 0.050 | 0.200 | 0.750 | MEDIAL_STRONG |

Signs below the classifiability floor (N < 20), reported with their counts in the results JSON and marked TOO THIN for this population: 290. None is a member of any strong set and none was dropped.

Strong sets — opening-strong (8): [103, 150, 204, 205, 210, 267, 391, 95]; closing-strong (10): [1, 12, 15, 176, 190, 211, 254, 328, 342, 60]; medial-strong (37): [112, 121, 123, 124, 127, 130, 135, 155, 18, 180, 192, 193, 194, 222, 230, 233, 25, 287, 294, 296, 326, 343, 344, 347, 348, 358, 403, 407, 59, 67, 70, 72, 8, 81, 97, 98, 99].

## ARM2 — per-sign quantities (NB-1)

Sequences: 1670 total; 0 of length 1 (counted, entering no count); 1670 of length >= 2; 1401 of length >= 3. Classifiable signs (N >= 20): 36 of 390.

| Sign | N | I | T | M | i | t | m | Bands |
|---|---|---|---|---|---|---|---|---|
| M342 | 584 | 12 | 70 | 502 | 0.021 | 0.120 | 0.860 | MEDIAL_STRONG |
| M267 | 400 | 17 | 59 | 324 | 0.043 | 0.147 | 0.810 | MEDIAL_STRONG |
| M099 | 389 | 24 | 67 | 298 | 0.062 | 0.172 | 0.766 | MEDIAL_STRONG |
| M176 | 356 | 13 | 68 | 275 | 0.037 | 0.191 | 0.772 | MEDIAL_STRONG |
| M211 | 249 | 12 | 67 | 170 | 0.048 | 0.269 | 0.683 | MEDIAL_STRONG |
| M328 | 234 | 15 | 70 | 149 | 0.064 | 0.299 | 0.637 | MEDIAL_MODERATE |
| M293 | 232 | 16 | 77 | 139 | 0.069 | 0.332 | 0.599 | MEDIAL_MODERATE |
| M059 | 222 | 43 | 75 | 104 | 0.194 | 0.338 | 0.468 | — |
| M162 | 205 | 14 | 72 | 119 | 0.068 | 0.351 | 0.580 | MEDIAL_MODERATE |
| M391 | 193 | 22 | 60 | 111 | 0.114 | 0.311 | 0.575 | MEDIAL_MODERATE |
| M367 | 190 | 20 | 92 | 78 | 0.105 | 0.484 | 0.411 | — |
| M089 | 171 | 17 | 75 | 79 | 0.099 | 0.439 | 0.462 | — |
| M233 | 171 | 19 | 92 | 60 | 0.111 | 0.538 | 0.351 | TERMINAL_MODERATE |
| M051 | 163 | 33 | 84 | 46 | 0.202 | 0.515 | 0.282 | TERMINAL_MODERATE |
| M336 | 161 | 13 | 76 | 72 | 0.081 | 0.472 | 0.447 | — |
| M048 | 157 | 31 | 72 | 54 | 0.197 | 0.459 | 0.344 | — |
| M065 | 154 | 36 | 84 | 34 | 0.234 | 0.545 | 0.221 | TERMINAL_MODERATE |
| M012 | 143 | 29 | 61 | 53 | 0.203 | 0.427 | 0.371 | — |
| M125 | 132 | 10 | 74 | 48 | 0.076 | 0.561 | 0.364 | TERMINAL_MODERATE |
| M087 | 130 | 14 | 63 | 53 | 0.108 | 0.485 | 0.408 | — |
| M305 | 83 | 0 | 81 | 2 | 0.000 | 0.976 | 0.024 | TERMINAL_STRONG |
| M249 | 73 | 0 | 70 | 3 | 0.000 | 0.959 | 0.041 | TERMINAL_STRONG |
| M220 | 62 | 0 | 61 | 1 | 0.000 | 0.984 | 0.016 | TERMINAL_STRONG |
| M062 | 28 | 28 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M073 | 25 | 25 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M045 | 24 | 24 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M079 | 24 | 24 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M013 | 23 | 23 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M016 | 23 | 23 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M008 | 22 | 22 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M022 | 22 | 22 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M052 | 22 | 22 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M061 | 22 | 22 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M058 | 21 | 21 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M019 | 20 | 20 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |
| M060 | 20 | 20 | 0 | 0 | 1.000 | 0.000 | 0.000 | INITIAL_STRONG |

Signs below the classifiability floor (N < 20), reported with their counts in the results JSON and marked TOO THIN for this population: 354. None is a member of any strong set and none was dropped.

Strong sets — opening-strong (13): ['M008', 'M013', 'M016', 'M019', 'M022', 'M045', 'M052', 'M058', 'M060', 'M061', 'M062', 'M073', 'M079']; closing-strong (3): ['M220', 'M249', 'M305']; medial-strong (5): ['M099', 'M176', 'M211', 'M267', 'M342'].

## Decision record (amendment section 5)

- **opening reappearance (primary): 0/8** (rate 0.0; reappears at >= 1/2: False). Named not reappeared: [(103, 'CONFLICT'), (150, 'CONFLICT'), (204, 'TOO THIN'), (205, 'UNMAPPED'), (210, 'TOO THIN'), (267, 'CONFLICT'), (391, 'CONFLICT'), (95, 'CONFLICT')]. Sensitivity (named signs removed from the denominator): 0/0 (reappears: False).
- **closing reappearance (primary): 0/10** (rate 0.0; reappears at >= 1/2: False). Named not reappeared: [(1, 'CONFLICT'), (12, 'CONFLICT'), (15, 'CONFLICT'), (176, 'CONFLICT'), (190, 'TOO THIN'), (254, 'TOO THIN'), (328, 'CONFLICT'), (342, 'CONFLICT'), (60, 'CONFLICT')]. Sensitivity (named signs removed from the denominator): 0/1 (reappears: False).
- **Pooled overlap: 0** against the label-permutation null's chance level 1 (999 shuffles, seed 44054; null min/median/max 0/0/1); exceeds the chance level: False.
- Precedence: amendment section 5.5(3) decided the verdict.

## Outcome

**NOT SUPPORTED**

The amended statement is not supported under battery NB-1 as frozen: a positional class reappears at less than one half, with the pooled overlap at or below the label-shuffle null's 95th percentile. This verdict falsifies the amended statement only. It does not falsify Yadav et al. (2010)'s original statement — the original battery's sets cannot be exhibited — and it does not move the parent claim's recorded status.

## Limits

- No language conclusion: opening and closing markers occur in non-linguistic systems too; no outcome of this run establishes that the script encodes language (spec section 7.1).
- No meaning conclusion: no outcome establishes what any opening or closing sign means, or what any sign was read as.
- Compilation-relativity: the arms are two compilations' stories, computed inside each compilation and joined only through the pinned crosswalk; no output pools the corpora or presents a crosswalk pair as a finding that two drawn signs are the same sign.
- The Phase-43 record stands: this run edits no Phase-43 file and no prior claim status; the parent claim's record, including its strongly-supported status, is untouched by any verdict (amendment section 9).
- This spec's closing measure is "closing-strong under NB-1" (a per-sign terminal-rate band on an inscription-position basis), a different quantity from Spec 045's "Holdat final-position concentration" (amendment section 10).
- Negative, inconclusive, thin, and step-0 outcomes are recorded with the same prominence as a supported finding.
