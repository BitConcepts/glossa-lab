# Sequence Analysis Report
Generated: 2026-04-22T17:16:01Z
**Site scope**: Mohenjo-daro only (179 inscriptions). All results are site-limited.
Multi-site comparison will be possible after Harappa / Dholavira data acquisition.

---

## Phase 6.1 — Frequency Analysis

- Total sign tokens: 1003
- Distinct signs: 182
- Hapax signs (appear once): 77 (42.3%)
- Unigram entropy H1: 6.2859 bits
- Mean inscription length: 5.6 signs
- Median inscription length: 5 signs
- Max inscription length: 13 signs

### Top 30 signs by frequency

  - P324: 99
  - P122: 76
  - P385: 35
  - P086: 35
  - P050: 32
  - P145: 27
  - P230: 23
  - P120: 22
  - P062: 21
  - P060: 20
  - P316: 19
  - P000: 19
  - P217: 18
  - P378: 17
  - P364: 17
  - P058: 15
  - P147: 14
  - P154: 14
  - P325: 14
  - P123: 13
  - P256: 12
  - P202: 11
  - P268: 11
  - P332: 11
  - P121: 10
  - P205: 10
  - P011: 10
  - P349: 10
  - P056: 9
  - P013: 9

### Length distribution

  - 1 signs: 1 inscriptions
  - 2 signs: 8 inscriptions
  - 3 signs: 26 inscriptions
  - 4 signs: 20 inscriptions
  - 5 signs: 35 inscriptions
  - 6 signs: 32 inscriptions
  - 7 signs: 25 inscriptions
  - 8 signs: 17 inscriptions
  - 9 signs: 7 inscriptions
  - 10 signs: 5 inscriptions
  - 11 signs: 1 inscriptions
  - 13 signs: 2 inscriptions

---

## Phase 6.2 — Positional Analysis

- H(sign|position=0, i.e. start): 3.3197 bits
- H(sign|position=-1, i.e. end): 5.7541 bits

Low end-position entropy means few signs dominate the terminal slot.
High start-position entropy (3.3197 bits) means many different signs appear at the start.

### Candidate terminal markers (end_rate ≥ 0.55, freq ≥ 5)

  - P385: end_rate=0.8286, end_count=29, total=35
  - P256: end_rate=0.75, end_count=9, total=12
  - P378: end_rate=0.5882, end_count=10, total=17
  - P011: end_rate=0.5, end_count=5, total=10

### Candidate initial markers (start_rate ≥ 0.55, freq ≥ 3)

  - P013: start_rate=1.0, start_count=9, total=9
  - P051: start_rate=1.0, start_count=5, total=5
  - P001: start_rate=1.0, start_count=4, total=4
  - P004: start_rate=1.0, start_count=6, total=6
  - P301: start_rate=0.8333, start_count=5, total=6
  - P324: start_rate=0.7778, start_count=77, total=99
  - P217: start_rate=0.7778, start_count=14, total=18
  - P098: start_rate=0.75, start_count=3, total=4
  - P000: start_rate=0.5789, start_count=11, total=19
  - P086: start_rate=0.5429, start_count=19, total=35

---

## Phase 6.3 — N-gram and Adjacency Analysis

- Conditional entropy H2 (bigram): 2.5149 bits
- Distinct bigrams: 551
- Distinct trigrams: 583

### Top 30 bigrams

  - P122 → P385: 29
  - P147 → P316: 10
  - P324 → P332: 10
  - P062 → P060: 9
  - P364 → P122: 9
  - P013 → P324: 9
  - P050 → P145: 8
  - P120 → P256: 7
  - P145 → P122: 7
  - P217 → P050: 6
  - P060 → P122: 6
  - P122 → P086: 6
  - P122 → P378: 6
  - P268 → P268: 5
  - P060 → P364: 5
  - P324 → P086: 5
  - P086 → P276: 5
  - P050 → P092: 5
  - P230 → P062: 5
  - P122 → P205: 5
  - P217 → P147: 5
  - P324 → P175: 5
  - P056 → P122: 4
  - P324 → P154: 4
  - P062 → P122: 4
  - P058 → P122: 4
  - P324 → P194: 4
  - P000 → P122: 4
  - P086 → P123: 4
  - P301 → P230: 4

### Top 20 PMI pairs (high mutual information, freq ≥ 2)

  - P204 ↔ P114: PMI=7.6687
  - P288 ↔ P127: PMI=7.6687
  - P188 ↔ P073: PMI=7.2537
  - P215 ↔ P275: PMI=7.0838
  - P160 ↔ P303: PMI=7.0838
  - P352 ↔ P011: PMI=6.9318
  - P035 ↔ P270: PMI=6.9318
  - P215 ↔ P091: PMI=6.3468
  - P332 ↔ P283: PMI=6.2093
  - P004 ↔ P123: PMI=5.9683
  - P349 ↔ P139: PMI=5.9318
  - P326 ↔ P120: PMI=5.7943
  - P268 ↔ P268: PMI=5.6568
  - P147 ↔ P316: PMI=5.5204
  - P154 ↔ P355: PMI=5.4464
  - P205 ↔ P076: PMI=5.3468
  - P355 ↔ P058: PMI=5.3468
  - P058 ↔ P075: PMI=5.3468
  - P301 ↔ P230: PMI=5.1452
  - P230 ↔ P234: PMI=5.1452

---

## Phase 6.4 — Sequence Segmentation

- Fraction of inscriptions ending in a candidate terminal: 29.6%
- Fraction of inscriptions starting with a candidate initial: 85.5%

### Recurrent templates (length 2-4, count ≥ 3)

  - P122 P385: 29 times
  - P147 P316: 10 times
  - P324 P332: 10 times
  - P062 P060: 9 times
  - P364 P122: 9 times
  - P013 P324: 9 times
  - P050 P145: 8 times
  - P120 P256: 7 times
  - P145 P122: 7 times
  - P217 P050: 6 times
  - P060 P122: 6 times
  - P122 P086: 6 times
  - P122 P378: 6 times
  - P268 P268: 5 times
  - P060 P364: 5 times
  - P324 P086: 5 times
  - P086 P276: 5 times
  - P050 P145 P122: 5 times
  - P050 P092: 5 times
  - P230 P062: 5 times
  - P122 P205: 5 times
  - P217 P147: 5 times
  - P217 P147 P316: 5 times
  - P324 P175: 5 times
  - P056 P122: 4 times

---

## Phase 6.5 — Graph and Community Analysis

### Top 25 hub signs (by co-occurrence weight)

  - P122: weight=341
  - P324: weight=305
  - P050: weight=155
  - P086: weight=122
  - P145: weight=117
  - P385: weight=109
  - P062: weight=104
  - P060: weight=104
  - P120: weight=94
  - P230: weight=92
  - P316: weight=86
  - P364: weight=84
  - P058: weight=74
  - P325: weight=64
  - P147: weight=58
  - P217: weight=55
  - P378: weight=54
  - P154: weight=53
  - P056: weight=47
  - P121: weight=46
  - P000: weight=44
  - P332: weight=44
  - P349: weight=44
  - P202: weight=42
  - P256: weight=42

### Top 30 bidirectional adjacency pairs

  - P050 ↔ P145: (8 + 2)
  - P122 ↔ P145: (1 + 7)
  - P086 ↔ P122: (1 + 6)
  - P062 ↔ P230: (1 + 5)
  - P000 ↔ P122: (4 + 2)
  - P120 ↔ P230: (4 + 1)
  - P324 ↔ P364: (2 + 1)
  - P060 ↔ P324: (2 + 1)
  - P120 ↔ P160: (2 + 1)
  - P000 ↔ P230: (2 + 1)
  - P145 ↔ P349: (1 + 1)
  - P145 ↔ P256: (1 + 1)
  - P056 ↔ P230: (1 + 1)
  - P122 ↔ P142: (1 + 1)
  - P324 ↔ P385: (1 + 1)

---

## Phase 6.6 — Cross-site Comparison

**Note**: Site comparison is not meaningful — only Mohenjo-daro is present. This will become informative once Harappa / Dholavira / Lothal data are ingested.

Sites in corpus: Mohenjo-daro

Cross-site analysis requires ≥ 2 sites. Currently deferred pending corpus expansion.