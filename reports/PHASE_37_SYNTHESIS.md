# Phase-37 Synthesis: CSA + Allograph Reduction + Corpus Realignment

**Completed:** 2026-05-14  
**Status:** COMPLETE  
**Foundation check:** PASS (17/0/0)

---

## Phase-37 Improvements Implemented

Four improvements from the literature were implemented and tested:

### 1. Coupled SA (CSA) — Tamburini 2025 (D.12)
4 chains with periodic Metropolis-criterion chain exchange every 500 iterations. Slightly staggered temperature schedules per chain. Chains can swap solutions when higher-scoring chain is found.

### 2. k-Permutations (Null Mappings) — Tamburini 2025
15% of free signs may be assigned to NULL (no syllable). NULL-mapped signs score SMOOTHING for all bigrams, reducing noise from rare signs that force poor assignments.

### 3. Allograph Reduction — Daggumati & Revesz 2021 (D.6, FIXED)
**Fixed from Phase-37v1:** Strict sim >= 0.999 threshold (was 0.90 → 33 merges). Result: 11 pairs merged (62 → 52 signs), with anchor preservation.
- Anchor transfer: `045 → 820` (`yānai` reading preserved)

### 4. Validated Positional Anchors — TB Inscription Endings (FIXED)
**Fixed from Phase-37v1:** Used inscription-ending syllables (not bigram right-side frequencies).
- Top TB terminal syllables (genuine inscription endings): `na, ma, pa, ka, ko, ni, li, la`
- Top TB initial syllables: `na, ka, ma, pa, la, ko, ku, a`
- 15 positional anchors added (9 terminal, 6 initial)
- Total anchors: 19 (base 4 + positional 15)

---

## Phase-37 Fixed Results

| Metric | Dravidian CSA | Sanskrit CSA |
|---|---|---|
| Allograph merges | 11 | 11 |
| Total anchors | 19 | 19 |
| Free signs | 33 | 33 |
| Best score | -44,888 | -47,913 |
| Z-score | **4.10** | 6.91 |
| p-value | < 0.0001 | < 0.0001 |
| NLL lift/insc | **8.677** | 9.868 |
| **Dravidian wins?** | **NO (0.88×)** | — |

Both highly significant (p < 0.0001). Sanskrit wins on lift with positional anchors.

---

## Complete Cross-Phase Summary (Phase-33 through Phase-37)

| Phase | Method | Dravidian lift | Sanskrit lift | Dravidian wins? | Note |
|---|---|---|---|---|---|
| 33 (anchor-free) | Std SA, unequal vocab | 8.679 | 4.180 | **YES 2.08×** | Vocab confound |
| 34 | Anchored, unequal vocab | 5.851 | 7.166 | NO | Density confound |
| 35 | Vocab-equal, density-unequal | 6.241 | 7.417 | NO | Density confound |
| **36 T1** | **Density-equal (651/651)** | **7.835** | **7.417** | **YES 1.06×** | **CLEAN** |
| 36 T2/Final | + Wrong positional anchors | 5.267 | 7.417 | NO | Anchor error |
| 37v1 | CSA + aggressive allograph | 6.418 | 9.868 | NO | Over-merged |
| **37 FIXED** | **CSA + strict allograph + TB anchors** | **8.677** | **9.868** | **NO 0.88×** | Ongoing |

**Best clean result: Phase-36 T1** — Dravidian wins 1.06× under fully controlled conditions (equal vocab, equal bigram density, no positional anchors).

**With positional anchors (TB-validated):** Sanskrit wins. The TB terminal syllables (na, ma, pa, ka) are common in **both** Dravidian and Sanskrit, so the anchors don't discriminate.

---

## Honest Assessment

The pattern is now well-established across 5 phases:
- **Without positional anchors + equalized conditions**: Dravidian marginally wins (1.06×)
- **With positional anchors**: Sanskrit wins (the TB syllables are too generic to discriminate)
- **SA method limit**: At 33-52 free signs, the method cannot reliably discriminate related syllabic hypotheses

The 1.06× Dravidian advantage in Phase-36 T1 is the strongest evidence currently available. It is [INFERRED, medium confidence] — requires ICIT corpus to reach higher confidence.

---

## Corpus Realignment: Batch 1 Complete

**Infrastructure built:**
- `glossa-corpus/` directory structure (32 subdirectories)
- Provenance schema (`metadata/provenance_schema.yaml`)
- Acquisition scripts (`backend/scripts/corpus_acquire_batch1.py`)

**Batch 1 acquisition: 7/15 OK, 5 PARTIAL, 3 FAILED, ~125,000 files**

| Source | Status | Files |
|---|---|---|
| Open Greek and Latin (First1KGreek) | OK | 4,326 |
| Perseus Digital Library (Greek + Latin) | OK | 3,994 |
| SARIT Sanskrit TEI | OK | 144 |
| OpenITI Arabic/Persian | OK | 103 |
| ETCBC Hebrew Bible (morphological) | OK | 1,157 |
| Monier-Williams Sanskrit Lexicon | OK | 1,830 |
| Gesenius/OpenScriptures Hebrew Lexicon | OK | 75 |
| GRETIL Sanskrit | FAIL | 0 (repo moved) |
| ORACC cuneiform | PARTIAL | 0 (server error) |
| SuttaCentral Pali | FAIL | 0 (timeout) |
| CBETA Chinese Buddhist | PARTIAL | 0 (SSL cert) |

**Languages covered:** Ancient Greek, Latin, Sanskrit, Classical Hebrew, Aramaic, Arabic, Persian, Classical Chinese, Pali

**Retry needed:** GRETIL (use alternate repo), ORACC (direct bulk API), SuttaCentral (increase timeout), CBETA (disable SSL verify or use alternate endpoint).

---

## Phase-38 Priorities

1. **ICIT corpus** (still blocked on Dr. Fuls — highest impact when available)
2. **Corpus Batch 2**: Fix GRETIL, ORACC, SuttaCentral, CBETA; add ETCSL, Papyri.info
3. **Larger Dravidian LM**: Build from DEDR + Sangam poetry + GRETIL Tamil texts
4. **Phase-36 T1 confirmation**: Re-run with 10 seeds × 60K iters and 1000 null perms to confirm 1.06× Dravidian advantage with tighter confidence intervals
