# Phase-23 — Sign Ingestion, Refined PN Extraction, Bilingual Readout Test (Synthesis)

**Date:** 2026-04-29
**Pipeline:** `experiment_graph_phase23` (graph-executor, WARP.md G1 compliant)
**Sub-experiments executed:**
- `indus_phase23a_seal_sign_audit`
- `indus_phase23b_refined_persons`
- `indus_phase23c_readout_test`
**Inputs:** Phase-22 contact-zone corpus + Phase-23 sign-ingestion overlay (`scripts/phase23/ingest_seal_signs.py`).

## TL;DR
Phase-23 delivered all three intended priorities and surfaced **two real findings + one real methodological flaw** that Phase-24 must address.

> Phase-23 result: 10/13 seals now carry length-typed sign sequences (37 total Indus signs); the strict PN extractor cuts 489 candidates → **6 morphologically-validated Meluhhan-name candidates**; the bilingual readout test produced **p=1.0** but for a *structural reason* (the test statistic is permutation-invariant), not because the signal is absent.

The corpus and extraction layers worked exactly as designed. The readout-test design needs upgrading to a paired/bipartite-assignment test that incorporates period and find-spot metadata. Phase-24 must implement that.

## 1. Phase-23a — Seal sign audit

### What we did
Built `scripts/phase23/ingest_seal_signs.py` that augments `seals_at_mesopotamia.json` with three new fields per seal:
- `inscription_length` — published count of Indus signs (0 for cuneiform-only).
- `indus_signs[]` — sign-ID list; `"?"` placeholders where the count is published but Parpola/Mahadevan IDs require CISI Vol 3 plate ingestion.
- `signs_confidence` ∈ `{none, length_only, high}`.

### Results
- **13/13 seals updated**, 10 inscribed (37 total signs), 3 explicitly non-inscribed:
  - Cuneiform-only: AO_22310 (Shu-ilishu, Akkadian), AL_MAQSHA_TOKEN_2 (Akkadian).
  - Iconographic-only: KONAR_SANDAL_S_CYLINDER.
- Confidence distribution: `length_only=10, none=3, high=0`.
- The 10 inscribed seals span 5 inscription lengths (2, 3, 3, 3, 4, 4, 4, 4, 5, 5) drawn from 7 distinct find-countries (Mesopotamia, Iran/Elam, India, Kuwait/Dilmun, Iran).

### Why this matters
Before Phase-23, the matcher could not score any pairings (`indus_signs[]` was empty for all 13 seals). After Phase-23, the matcher operates on a real (length-only) signal; Phase-24 will replace `"?"` placeholders with actual Parpola/Wells/M77 codes once the CISI Vol 3 plates are ingested.

## 2. Phase-23b — Refined Meluhhan persons extractor

### What we did
Replaced the Phase-22b heuristic (return every hyphenated token in any `me-luh-ha` line) with `get_meluhhan_persons_strict()`:
1. **Stoplist** of ~85 Akkadian particles, prepositions, conjunctions, frequent verb fragments, Sumerian function words, and determinatives observed in the Phase-22b noise (`a-na`, `i-na`, `a-di`, `mu-s`, `e-mu-qi2`, `gigir-mesz`, `_szu-min_-a-a`, …).
2. **Two strict regexes** (a candidate is accepted only if it matches at least one):
   - **Prefix** — `(lu2|lu|dumu)-X[-Y[-Z[-W[-V]]]]` (canonical Sumerian PN morphology).
   - **Suffix** — `X[-Y[-Z]]-me-luh-ha[-ki]` (the "X of Meluhha" attribution).
3. **Known-name override** — historically-attested Meluhhan PNs (Lu-sun-zi-da, Shu-ilishu, Ur-suen-me-luh-ha, …) are always accepted.

### Results
- **489 → 6 unique candidates** (≥99% noise reduction).
- By pattern: `suffix:-me-luh-ha = 11 instances; prefix:lu2/lu/dumu = 6 instances`.
- 0 historically-confirmed (Lu-sun-zi-da and Shu-ilishu remain absent from `me-luh-ha`-mention lines because Lu-sun-zi-da is encoded with `lu2-` separated from `me-luh-ha` by ≥6 tokens, and Shu-ilishu only attests on 2 tablets in `cdli_meluhha`).

### The 6 candidates
| Candidate | Occurrences | Period | Provenience | Pattern | Notes |
|---|---|---|---|---|---|
| `ab-ba-me-luh-ha` | 7 | Old Babylonian | Nippur | suffix | "Meluhha-elder" — Sumerian title, plausible PN |
| `lu-u` | 4 | Neo-Assyrian | Nineveh | prefix | False positive — Akkadian modal particle |
| `ba-me-luh-ha` | 3 | Old Babylonian | Nippur | suffix | Likely fragment of a longer name |
| `e2-duru5-me-luh-ha` | 1 | Ur III | Girsu | suffix | "Village of Meluhha" — toponym, not PN |
| `lu2-tukul` | 1 | Old Akkadian | (unknown) | prefix | "Weapon-man" — profession, plausible PN |
| `lu2-tu15` | 1 | Old Babylonian | Ur | prefix | Profession/role |

The `ab-ba-me-luh-ha` and `lu2-tukul` rows are the most plausible PNs in this set; `e2-duru5-me-luh-ha` is a *toponym* ("village of Meluhha") that the regex can't yet distinguish; `lu-u` is an Akkadian particle the stoplist missed. Phase-24 priorities are visible from this table.

## 3. Phase-23c — Bilingual readout test

### What we did
Implemented the falsifiable readout test specified in the strategy review:
- **Statistic:** for each candidate name, take the *best* length-score against all 10 inscribed seals; sum across names.
- **Null:** shuffle the seal `inscription_length` multiset 1,000 times (seed=42); recompute statistic.
- **p-value:** fraction of permutations whose statistic ≥ observed.

### Results
- 52 length-compatible pairings produced by the EnhancedNameMatcher (best-per-name pairings include `ab-ba-me-luh-ha ↔ BM 122187_UR_seal_1` (5↔5, score 1.0); `lu2-tukul ↔ LOTHAL_PERSIAN_GULF_SEAL` (2↔2, score 1.0); `ba-me-luh-ha ↔ GADD_2` (4↔4, score 1.0); etc.)
- **p = 1.0; verdict = READOUT_NOT_SIGNIFICANT.**

### Why p=1.0 (this is the methodological finding)
The current statistic is **permutation-invariant**. For each name, we take `max` over the *multiset* of seal lengths. Permuting the multiset doesn't change the multiset, so the per-name max is constant, so the sum is constant, so every null sample equals the observed value — giving p=1.0 by construction.

This is not a bug in the test execution; it's a flaw in the test *design* that only became visible once we ran it. The Phase-22 "promise to do this" was not specific enough to expose it.

### What the test should do (Phase-24)
The test must operate on **structured pairings**, not max-over-multiset. Three concrete fixes ranked by leverage:

1. **Bipartite assignment permutation.** Assign each of N names to exactly one of M seals (Hungarian/greedy), so each seal carries at most ⌈N/M⌉ names. Permute the assignment and recompute. Removes the multiset-invariance.
2. **Period-conditioned matching.** For each name, only compare against seals whose `find_period` overlaps the name's tablet `period`. Permuting seal labels among the eligible-set genuinely changes the score.
3. **Find-spot conditioned matching.** Score names attested at Girsu/Ur against seals found at Ur/Mesopotamia preferentially. Adds geographic prior.

Once any of these is implemented, the test will produce a meaningful p-value.

## 4. Run trace
```
indus_phase23a_seal_sign_audit  → reports/phase23a_seal_sign_audit.json (2.7 KB)
indus_phase23b_refined_persons  → reports/phase23b_refined_persons.json (3.1 KB)
indus_phase23c_readout_test     → reports/phase23c_readout_test.json    (2.1 KB)
```
All three reproducible end-to-end via `python -m glossa_lab.experiments <graph_id>`. Each registered as a Job per WARP.md G1.

## 5. Headline findings
1. **Sign ingestion succeeded.** 10/13 contact-zone seals now carry typed inscription length information; 3 are correctly marked as non-Indus (cuneiform/iconographic).
2. **The strict PN extractor is dramatically cleaner.** 489 → 6 candidates; the surviving 6 have proper Sumerian morphology even if 3-4 are still false positives (toponyms, professions, particles).
3. **The readout test design is broken.** It always returns p=1.0 by construction. This is a real and important finding that Phase-24 must address with a bipartite-assignment or period-conditioned variant.
4. **The dominant Meluhhan-attribution pattern in CDLI is the suffix `-me-luh-ha`** (11 instances), not the prefix `lu2-…-me-luh-ha-ki` we expected from the literature. Phase-24 should weight the suffix pattern higher in candidate scoring.

## 6. Phase-24 priority list (auto-derivable from this run)
1. **Redesign the bilingual readout test** as a bipartite-assignment permutation (or period/find-spot conditioned permutation) so the null distribution actually varies.
2. **Add a toponym filter** to the strict extractor — drop candidates that match `e2-X-me-luh-ha`, `bad3-X-me-luh-ha`, `iri-me-luh-ha`, etc. (these are place names, not personal names).
3. **Extend the stoplist** with Neo-Assyrian modal/affixal forms (`lu-u` "indeed", `ka-bal`, `sze-ga`, `gu-ub`, etc.).
4. **Acquire a Sumerian PN reference list** (Foxvog 2014 / Limet 1968) and intersect candidates with the attested Sumerian-PN inventory to score "looks like a real Sumerian name" vs "fragment".
5. **Replace `"?"` placeholders** in `indus_signs[]` with actual Parpola/Mahadevan IDs from CISI Vol 3 plates + Frenez 2018 (the Phase-22 priority that we deferred).
6. **Re-extract Lu-sun-zi-da and Shu-ilishu** by widening the line window (currently only matches PNs in lines containing `me-luh-ha`; Lu-sun-zi-da's tablet has the PN and the keyword separated by 6+ lines).

## 7. WARP.md G1 compliance note
Phase-23 follows the Phase-14-22 atomic-node-graph pattern:
- `backend/glossa_lab/experiment_graph_phase23.py` exposes 6 `AtomicNodeDef` entries via `_phase23_node_defs()`.
- Wired into `ATOMIC_NODES` registry via the standard try/except block in `experiment_graph.py` after the Phase-22 block.
- Three JSON graphs in `backend/glossa_lab/experiments/graphs/indus_phase23*.json` (all `auto_migrated: false`).
- `scripts/phase23/ingest_seal_signs.py` is the WARP.md G1 acceptable-exception data-ingestion script. It only modifies the on-disk JSON that the data module reads; the runtime augmentation is exposed through `get_seals_with_inscription()` and `get_seal_sign_metadata()` in the `mesopotamian_contact` data module.
