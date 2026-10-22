# Phase-43 positional battery — methods record

This record states the Phase-43 positional battery exactly as it ran. It is
the methods record of record for the battery, deposited by the Phase-43
battery record amendment (owner-approved 2026-10-21). The producing script is
`backend/scripts/phase43_part2.py`, restored byte-for-byte alongside this
record; every rule below is stated from that code. The sibling script
`backend/scripts/phase43_all.py` is identified at the end of this record.

## Corpus construction

The battery runs on the V3 corpus: sequences from
`indus_corpus_v3.load_corpus(min_length=2)` — Mahadevan-numbered sign
sequences reconstructed from the Firestore `indusarrays` dump (`texts` array
per record; `*NNN` supplementary signs, empty strings, and `"0"` filtered at
load; per (dockey, sideline) the longest clean sequence kept; sequences
shorter than 2 signs dropped).

Deposited corpus statistics (from the results file of record,
`outputs/phase43_all.json`): 3,916 records; 2,665 unique dockeys; 3,137
sequences; 12,494 sign instances.

## Position rule

For each sequence of length ≥ 2, each sign occurrence is counted once:
position 0 (first) → initial (I); last position → terminal (T); any position
between → medial (M). A two-sign sequence therefore contributes one I and
one T and no M. Sequence order is the dump's `texts` order; no reversal is
applied anywhere in loader or script. Per sign: `total` = I + M + T;
`t_rate` = T / total, `i_rate` = I / total, `m_rate` = M / total.

## Count floor

A sign enters classification only if `total ≥ 5` (the script's own summary
line names it `min_count=5`). 201 signs passed the floor in the recorded
run.

## Classification cascade (T2.2)

First match wins, in this order, on unrounded rates:

| Order | Condition | Class |
|---|---|---|
| 1 | t_rate ≥ 0.60 | TERMINAL_STRONG |
| 2 | i_rate ≥ 0.55 | INITIAL_STRONG |
| 3 | m_rate ≥ 0.65 | MEDIAL_STRONG |
| 4 | t_rate ≥ 0.40 | TERMINAL_MODERATE |
| 5 | i_rate ≥ 0.40 | INITIAL_MODERATE |
| 6 | otherwise | MIXED |

The cascade order is part of the rule: a sign with t_rate ≥ 0.60 is
TERMINAL_STRONG even if its i_rate also clears 0.55. Recorded class counts:
TERMINAL_STRONG 20, INITIAL_STRONG 40, MEDIAL_STRONG 61,
TERMINAL_MODERATE 10.

## Opening-formula counting rule (T2.3)

Start bigrams (seq[0], seq[1]) are counted over all sequences of length ≥ 2;
the scan takes the top-100 most common start bigrams. For a candidate pair
(a, b) with start-count `cnt`: `total_a` = the number of bigrams at ANY
position whose first sign is a; dominance = start-count / total_a. A pair is
a candidate iff `total_a ≥ 8`, `cnt ≥ 5`, `a.i_rate ≥ 0.35`, and
`dominance ≥ 0.15`. Candidates are ranked by `cnt`.

## Fish test floors (T2.4)

Candidate fish signs [267, 72, 65, 59, 60, 70]. A sign is scanned iff its
total ≥ 10. `terminal_frac` = share of its any-position bigrams whose second
sign is TERMINAL_STRONG or TERMINAL_MODERATE. A sign is "supported" iff
terminal_frac > 0.15 AND sign total ≥ 20. Recorded: sign 267 — total 356,
terminal_frac 0.038, not supported; sign 72 — total 181, terminal_frac 0.259,
supported.

## What the battery does not contain

**The battery contains NO chance-baseline step.** Neither script computes
any permutation, shuffle, or expected-rate baseline for the positional
classes; classification is the threshold cascade on observed rates, full
stop. No chance-baseline method ever existed in this battery, so none is
restored by this deposit; adding one would be a new element, not a
restoration.

**The full member lists were never written to any file.** The full member
lists for the INITIAL_STRONG (40) and MEDIAL_STRONG (61) classes, and the
TERMINAL_STRONG ranks 11–20, were never written to any file. The scripts
print top-8/top-10 lists to stdout and the results file stores the top-10
terminal table only. The full lists exist only as a computation: script +
dump.

## Producing script and sibling

- `backend/scripts/phase43_part2.py` is the producing script: it wrote the
  Phase-43 results file of record (`outputs/phase43_all.json`). Its writer
  keys and its terminal-table `i_rate` / `m_rate` fields match the deposited
  results exactly.
- `backend/scripts/phase43_all.py` is the sibling Phase-43 run. It runs the
  same T2 battery with identical T2.2 constants, but its T2.3 candidate-scan
  constants differ — top-50 start-bigram scan; floors total_a ≥ 10,
  cnt ≥ 5, a.i_rate ≥ 0.40, dominance ≥ 0.20 — and it did NOT produce the
  deposited results.
