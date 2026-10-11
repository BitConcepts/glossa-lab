# Phase-393 — Spec 028: Harappa Robustness of the M77 Site Effect

**Arm A verdict (primary): INCONCLUSIVE** — bounded claim: "site-linked repertoire structure at/above the practical margin exists among the non-Harappa sites."

**Arm B verdict (secondary): INCONCLUSIVE** — bounded claim: "the site effect is not an inscription-count artifact of the large corpora."

Arm C is exploratory and descriptive only; it carries no verdict. Reporting is hierarchical (freeze §6): Arm A is the headline; Arm B is a separate secondary bounded claim; there is no pooled headline. Period is not controlled in either arm (inherited stated boundary: the layer's period field is 59.2% uninformative).

## Arm A — Harappa excluded (confirmatory, primary)

- Records: 1593; inscriptions per draw: 294
- Median adjusted R²: **0.00878**; interval [0.00463, 0.01297] vs margin 0.01
- Rejection share at α=0.05: 0.623; median p 0.0340
- Median raw R²: 0.02232

### Controls (failure = this arm INVALID)

| Control | Median adj R² | Interval | Share rejecting | Result |
|---|---|---|---|---|
| negative_control | 0.00046 | [-0.00352, 0.00540] | 0.040 | PASS |
| positive_control | 0.02396 | [0.01565, 0.03363] | 1.000 | PASS |

### Leave-one-site-out

| Dropped site | Median adj R² | Interval | Share rejecting |
|---|---|---|---|
| Mohenjo-daro | 0.00656 | [0.00368, 0.01147] | 0.508 |
| Dholavira | 0.00948 | [0.00450, 0.01384] | 0.548 |
| Lothal | 0.00884 | [0.00389, 0.01378] | 0.573 |
| Chanhu-daro | 0.00761 | [0.00214, 0.01333] | 0.578 |
| Kalibangan | 0.00859 | [0.00319, 0.01486] | 0.477 |

S-complete sensitivity (labelled, no verdict): median adjusted R² 0.00647, interval [0.00224, 0.01089], rejection share 0.241.

## Arm B — site-equal weight (confirmatory, secondary)

- Records: 3030; inscriptions per draw: 312
- Median adjusted R²: **0.02237**; interval [0.01222, 0.03333] vs margin 0.01
- Rejection share at α=0.05: 0.955; median p 0.0040
- Median raw R²: 0.03809

### Controls (failure = this arm INVALID)

| Control | Median adj R² | Interval | Share rejecting | Result |
|---|---|---|---|---|
| negative_control | 0.00204 | [-0.00182, 0.00707] | 0.055 | PASS |
| positive_control | 0.01670 | [0.01047, 0.02396] | 1.000 | PASS |

### Leave-one-site-out

| Dropped site | Median adj R² | Interval | Share rejecting |
|---|---|---|---|
| Harappa | 0.00661 | [0.00159, 0.01153] | 0.588 |
| Mohenjo-daro | 0.02376 | [0.01459, 0.03683] | 0.889 |
| Dholavira | 0.02436 | [0.01331, 0.04075] | 0.663 |
| Lothal | 0.02475 | [0.01490, 0.03920] | 0.945 |
| Chanhu-daro | 0.02256 | [0.01269, 0.03345] | 0.910 |
| Kalibangan | 0.02454 | [0.01421, 0.03874] | 0.945 |

## Arm C — Harappa decomposition (EXPLORATORY, descriptive only)

Harappa records: 1437 (0.4743 of the analysis population). Harappa centroid vs the pooled other sites: Bray–Curtis 0.3410; within SEAL only 0.1114; within TAB only 0.4953; Harappa SEAL vs TAB centroids 0.4501.

Site-centroid Bray–Curtis matrix (analysis population):

| | Harappa | Mohenjo-daro | Dholavira | Lothal | Chanhu-daro | Kalibangan |
|---|---|---|---|---|---|---|
| Harappa | 0.000 | 0.346 | 0.402 | 0.441 | 0.406 | 0.465 |
| Mohenjo-daro | 0.346 | 0.000 | 0.273 | 0.257 | 0.280 | 0.296 |
| Dholavira | 0.402 | 0.273 | 0.000 | 0.322 | 0.351 | 0.347 |
| Lothal | 0.441 | 0.257 | 0.322 | 0.000 | 0.314 | 0.342 |
| Chanhu-daro | 0.406 | 0.280 | 0.351 | 0.314 | 0.000 | 0.303 |
| Kalibangan | 0.465 | 0.296 | 0.347 | 0.342 | 0.303 | 0.000 |

Largest per-column contributions to Harappa vs pooled others (|p − q| / 2, top 25):

| Sign | Contribution | Share of distance |
|---|---|---|
| M328 | 0.07345 | 0.2154 |
| M089 | 0.02755 | 0.0808 |
| M095 | 0.02164 | 0.0635 |
| M087 | 0.01717 | 0.0504 |
| M176 | 0.01615 | 0.0474 |
| M122 | 0.01447 | 0.0424 |
| UNMAPPED | 0.01320 | 0.0387 |
| M086 | 0.01276 | 0.0374 |
| M342 | 0.01100 | 0.0322 |
| OTHER | 0.00804 | 0.0236 |
| M121 | 0.00663 | 0.0194 |
| M387 | 0.00486 | 0.0143 |
| M391 | 0.00465 | 0.0136 |
| M072 | 0.00436 | 0.0128 |
| M211 | 0.00427 | 0.0125 |
| M343 | 0.00408 | 0.0120 |
| M336 | 0.00407 | 0.0119 |
| M015 | 0.00371 | 0.0109 |
| M065 | 0.00355 | 0.0104 |
| M293 | 0.00311 | 0.0091 |
| M017 | 0.00308 | 0.0090 |
| M059 | 0.00308 | 0.0090 |
| M012 | 0.00300 | 0.0088 |
| M125 | 0.00271 | 0.0079 |
| M053 | 0.00210 | 0.0062 |

Token mass by object type (eligible population):

| Site | Type | Inscriptions | Tokens |
|---|---|---|---|
| Allahdino | SEAL | 7 | 29 |
| Altyn Depe | SEAL | 1 | 2 |
| Bala-kot | SEAL | 4 | 20 |
| Banawali | SEAL | 15 | 41 |
| Banawali | TAB | 1 | 7 |
| Baror | SEAL | 1 | 3 |
| Bhirrana | SEAL | 3 | 9 |
| Chanhu-daro | SEAL | 52 | 258 |
| Chanhu-daro | TAB | 2 | 10 |
| Desalpur | SEAL | 2 | 11 |
| Dholavira | SEAL | 96 | 378 |
| Dholavira | TAB | 15 | 43 |
| Failaka | SEAL | 2 | 7 |
| Farmana | SEAL | 4 | 8 |
| Ganweriwala | TAB | 1 | 3 |
| Gharo Bhiro | SEAL | 1 | 3 |
| Girsu | SEAL | 1 | 4 |
| Gola Dhoro (Bagasra) | SEAL | 5 | 28 |
| Gonur Depe | SEAL | 1 | 8 |
| Hajar | TAB | 1 | 2 |
| Harappa | SEAL | 361 | 1582 |
| Harappa | TAB | 1076 | 2857 |
| Janabiyah | SEAL | 1 | 7 |
| Jhukar | SEAL | 1 | 5 |
| Kalibangan | SEAL | 49 | 204 |
| Kalibangan | TAB | 3 | 9 |
| Kanmer | SEAL | 1 | 2 |
| Karanpura | SEAL | 1 | 2 |
| Karzakan | SEAL | 3 | 10 |
| Khirsara | SEAL | 4 | 27 |
| Kish | SEAL | 2 | 10 |
| Lakhanjo-daro | SEAL | 3 | 12 |
| Lakhanjo-daro | TAB | 1 | 3 |
| Lohumjo-daro | SEAL | 1 | 10 |
| Lothal | SEAL | 72 | 298 |
| Lothal | TAB | 2 | 8 |
| Luristan | SEAL | 1 | 4 |
| Miri Qalat | SEAL | 2 | 4 |
| Mohenjo-daro | SEAL | 1138 | 5360 |
| Mohenjo-daro | TAB | 164 | 636 |
| Nausharo | SEAL | 12 | 67 |
| Nindowari-damb | SEAL | 2 | 12 |
| Nuhato | SEAL | 1 | 3 |
| Ornach area | SEAL | 1 | 2 |
| Pabumath | SEAL | 1 | 5 |
| Pirak | SEAL | 1 | 5 |
| Qala'at al-Bahrain | SEAL | 1 | 5 |
| Rahman-deri | SEAL | 1 | 2 |
| Rajanpur | TAB | 1 | 2 |
| Rakhigarhi | SEAL | 6 | 28 |
| Rupar | TAB | 1 | 3 |
| Saar | SEAL | 1 | 6 |
| Salut | SEAL | 1 | 5 |
| Shikarpur | SEAL | 1 | 5 |
| Shortughai | SEAL | 1 | 2 |
| Surkotada | SEAL | 2 | 11 |
| Susa | SEAL | 2 | 13 |
| Tello | SEAL | 1 | 4 |
| Ur | SEAL | 5 | 18 |
| Wattoowala | SEAL | 1 | 2 |

## Provenance

- Freeze: specs/028-harappa-robustness/freeze.md; digest 619ab0c30048b934a14f2f2e7583a1a2e93c25c0599488f97165c285cd38bb61
- OSF registration of the frozen contract: https://osf.io/7m35w/ (filed before execution)
- Seed 20261012; draws 199; permutations per draw 499; elapsed 540.6s
- Population guard: reproduced the frozen margins exactly (see results JSON).
