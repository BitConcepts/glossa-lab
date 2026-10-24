# Phase-407 — Spec 042: Arm B Split by Object Type

The object-type split cannot be run as designed: the tablet stratum carries fewer than six sites with at least twenty inscriptions of its type (Chanhu-daro 2; Dholavira 15; Harappa 1076; Kalibangan 3; Lothal 2; Mohenjo-daro 164). No stratum quantity was computed. Spec 028 Arm B stands exactly as recorded.

Corpus: the Phase-393 layer (the Yajnadevam-compiled inscription file as held by the program), with its lineage posture as recorded in Specs 027/028. Headline outcome: **THIN**. This result is about repertoire association in recorded data. It is not evidence that any population moved.

## Step 0 (spec section 3, in order)

- **0.1 Input integrity — PASS.** Every section 2 input hashes to its freeze-record value.
- **0.2 Population reproduction — PASS.** The frozen flow re-run reproduces the recorded counts (5679 / 4531 / 4505 / 3605 / 3144 / 3030) and the recorded Arm B analysis set (3030 records, 125 sign columns, cell table identical to the Spec 028 margins audit).
- **0.3 Partition census — PASS.** The analysis population partitions by recorded object type with no record of any other type; the strata sum to 3030.

| Site | SEAL | TAB | Total |
|---|---|---|---|
| Chanhu-daro | 52 | 2 | 54 |
| Dholavira | 96 | 15 | 111 |
| Harappa | 361 | 1076 | 1437 |
| Kalibangan | 49 | 3 | 52 |
| Lothal | 72 | 2 | 74 |
| Mohenjo-daro | 1138 | 164 | 1302 |
| **Total** | **1768** | **1262** | **3030** |

- **0.4 Stratum floor (SEAL) — PASS.** 6 of 6 sites carry at least 20 inscriptions of the type (minimum site count 49).
- **0.4 Stratum floor (TAB) — TOO THIN.** 2 of 6 sites carry at least 20 inscriptions of the type (minimum site count 2).

Gate 0.5 (pooled regression) was **not reached**: the execution closed at gate 0.4 under DD-042-2, and neither stratum was computed.

## Stratum descriptions (spec section 5; described, not controlled)

- **SEAL** (period mix, as recorded in the pinned layer): -: 1005, 1: 1, 2: 37, 3: 33, 4: 23, 4/5: 8, 5: 21, 5/6: 1, 5?: 1, 6: 11, Early: 29, Intermediate: 302, Late: 248, Late : 1, Layer 10: 2, Layer 11: 2, Layer 12: 1, Layer 13: 1, Layer 15: 1, Layer 19: 1, Layer 2: 8, Layer 25: 1, Layer 3: 4, Layer 3-8: 1, Layer 4: 10, Layer 4-6: 1, Layer 5: 2, Layer 6: 3, Layer 6A: 1, Layer 7: 3, Layer 8: 1, Layer 8C: 1, Layer 9: 2, Layer13: 1.
- **SEAL** (preservation, as recorded in the pinned layer): -: 2, chipped: 97, complete: 1101, fragment: 388, partly damaged: 82, slightly chipped: 98.
- **TAB** (period mix, as recorded in the pinned layer): -: 698, 2: 1, 2/3: 2, 3: 495, 4: 1, 5: 2, 6: 8, Early: 2, Intermediate: 32, Late: 21.
- **TAB** (preservation, as recorded in the pinned layer): chipped: 59, complete: 955, fragment: 191, partly damaged: 12, slightly chipped: 45.

Object type is one compilation's recording: Spec 037's census found the CISI volumes and the program's corpus classify matched objects' types differently in 49% of cases. This test uses type only as recorded within the Phase-393 layer, consistently for both strata.

## Provenance

- Freeze: specs/042-arm-b-object-type-split/freeze.md; digest 6be2988d7f4c290591d36f391ac84a772f18a9121e35ddd0e251956b5260f753
- OSF registration of the frozen contract: https://osf.io/tmyzg/ (approved and public before execution)
- Seed 20261012; margin adjusted R^2 0.01; anchors asserted byte-identical before and after (df0cf620a0d6...).
