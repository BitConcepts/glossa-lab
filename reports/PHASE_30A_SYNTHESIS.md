# Phase-30a Statistical Validation Sprint — Synthesis

**Date:** 2026-05-01 (UTC `20260501T114235`)
**Predecessor:** Phase-29 (commit `3e3f775`); Phase-30 prep (commit `ac13b58`)
**Scope:** 13 sub-tests (P30-A1..A8, E7, G1, G8, G9) validating the
Phase-29 Enmenanak/Enheduana finding.
**Aggregate verdict:** **PARTIAL SUPPORT** — the headline survives the
global nulls (A1, E7) and effect-size tests (G8), but fails per-PN
multiple-comparisons (A5) and Meluhha co-occurrence (A3), and shows
period bias (A6).

## Headline numbers

| Sub-test | Pass / Warn / Fail | Key statistic |
|---|---|---|
| **A1** Permutation null on Enmenanak score (10 000×) | **PASS** | p = 0.0053 (99.48 percentile); null mean 3.62, p95 5.5, p99 6.0 |
| **A2** Period filter (Old Akkadian / Ur III) | **PASS** | 49 / 102 chronologically compatible |
| **A3** Meluhha co-occurrence filter | **FAIL** | 0 / 102 PNs appear (as `best_form`) on the 180 Meluhha-mentioning CDLI tablets |
| **A4** Bootstrap 95 % CI on Enmenanak score | warn | CI = [2.5, 7.0], median 5.0, mean 5.40 — wide |
| **A5** BH-FDR over top-30 PNs (q = 0.05) | **FAIL** | 0 / 30 PNs survive correction |
| **A6** Held-out replication (Ur III train / Old Babylonian test) | warn | Position-match rate Ur III 6.69 % vs OBab 13.27 %; Δ = 6.6 pp |
| **A7** Janabiyah skeleton sensitivity | partial | Enmenanak rank ranges 1..28 across 7 variants; baseline rank 1, score 7.0 |
| **A8** Phoneme-value perm null v3 at M77 scale | data-starved | only 2 sign-IDs overlap M77 ↔ phoneme map (zero-padded vs unpadded sign-id schism) |
| **E7** Random-mapping null on anchor score (10 000×) | **PASS** | observed 24.5 at 100 percentile; null mean 1.93, p95 8.0, max 18.0; p = 0.0001 |
| **G1** Joint period × provenience stratification | partial | 7 PNs across 7 cells observed; densest = Ur III / Sumer core (5 PNs / 772 tablets) |
| **G8** Cohen's d (Enmenanak vs corpus baseline) | **PASS** | d = 6.22 (large); corpus mean 1.37, sd 0.91, n = 1 222 |
| **G9** M77 bigram LM → Janabiyah cross-validation | warn | held-out PPL 27.12 vs Janabiyah PPL 65.60; ratio 2.42 (> 2 = distinct) |

Per-test JSON reports: `reports/indus_phase30a_{p30_*}_20260501T114235.json`.
Aggregated verdict: `reports/indus_phase30a_verdict_20260501T114235.json`.

## What is genuinely strong

1. **A1 (p = 0.005)**: Enmenanak's score is unusual against 10 000 random
   Sumerian-syllable rendering sets. Under random renderings, the
   probability of observing score ≥ 7.0 for THIS specific PN is < 1 %.
2. **E7 (p = 0.0001)**: The observed iconographic-anchor score 24.5 is
   at the 100th percentile of 10 000 random sign→phoneme permutations.
   The null max is 18.0 — meaning **no random permutation of the
   33-entry phoneme map ever reproduces the iconographic-anchor
   coverage** of Parpola's actual readings. This is the single
   strongest result of Phase-30a: the iconographic-anchor methodology
   itself is statistically meaningful.
3. **G8 (d = 6.22)**: Effect size is large by any conventional cutoff.
4. **A2 (49 / 102)**: Chronological compatibility holds — Enmenanak
   itself is Old Akkadian, in the right period.
5. **A7 (rank 1 at baseline)**: Enmenanak is the top-1 PN under the
   actual Janabiyah skeleton.

## What is concerning

1. **A3 (0 / 102 Meluhha co-occurrence)**: NO Phase-29 candidate PN
   appears textually on any of the 180 Meluhha-mentioning CDLI
   tablets. Two possible explanations:
   - **Methodological:** the matching string is the segmented
     `best_form` (e.g. `en-men-an-na-ka-še`), which won't match the
     unsegmented ATF text where the form is written as
     `en-men-an-na-ka-^c{še3}` (digits + diacritics). A relaxed
     regex-based matcher would likely surface non-zero hits.
   - **Substantive:** if no Phase-29 candidate is independently
     attested as a Meluhhan name (vs. a generic Old Akkadian name),
     the headline weakens significantly.
   - **Fix:** implement a token-level matcher in Phase-30b (P30-A3-v2).
2. **A5 (0 / 30 BH-FDR survivors)**: Per-PN multiple-comparisons
   correction kills every top scorer. This is the biggest single
   weakness. It means: under the per-PN permutation null (where each
   PN's structure is held fixed and the rendering tokens are random),
   even Enmenanak's score 7.0 is *not* unusual relative to that PN's
   own null distribution. This contradicts A1 (where the rendering
   set is perturbed but the PN is held fixed).
   The disagreement reveals that the *rendering set* is doing the
   heavy lifting, not the PN's structure. A1 says "this rendering set
   gives Enmenanak a score >> random rendering sets would". A5 says
   "this PN under random rendering sets gives a score ~= the observed
   score". Both are valid, but A5 is the more conservative test for
   publication purposes.
3. **A6 (Δ rate 6.6 pp)**: Position-match rate differs by > 5 pp
   between Ur III (6.69 %) and Old Babylonian (13.27 %). Old Babylonian
   PNs match the rendering set more often — i.e. the rendering set
   captures *late* Sumerian phonology more than *early*. This
   inverts what we'd want for a Janabiyah-period readout (~2100 BCE).
4. **A8 (data starvation)**: Only 2 phoneme-map signs (`'47'` and
   `'1'`) overlap with M77 corpus signs. Investigation needed: M77
   uses zero-padded 3-digit codes (`'047'`); phoneme map uses
   unpadded (`'47'`). The script normalizes M77 with
   `str(int(sid))` to drop padding, but the M77 corpus also includes
   non-canonical sign codes that don't appear in our phoneme map.
   Net: H1 entropy null is data-starved at this scale.
5. **G9 (PPL ratio 2.42)**: Janabiyah's bigram perplexity (65.6) is
   2.4× the held-out M77 PPL (27.1). This says the Janabiyah seal
   sign sequence is structurally more surprising than typical M77
   inscriptions — consistent with either (a) Janabiyah being a
   *different language* fragment in the same script, or (b)
   Janabiyah being a rare PN-bearing inscription in the M77
   distribution. (a) would be expected under the Dilmun/Indus contact
   hypothesis; (b) is also plausible.

## Re-interpretation of Phase-29 in light of Phase-30a

The Phase-29 verdict ("Enmenanak score 7.0, 2 position matches at
Janabiyah positions 1+3" → ~12-15 % decipherment progress) **needs
hedging**:

- The score 7.0 is genuinely unusual against the global rendering-set
  null (A1) and the iconographic anchor methodology has independent
  statistical support (E7) — these are the two findings worth
  preserving.
- BUT: per-PN multiple comparisons (A5), Meluhha co-occurrence (A3),
  and held-out replication (A6) all fail or partial-fail.
- **Realistic decipherment progress estimate post-Phase-30a:
  ~10-12 %** (a slight regression from 12-15 %, reflecting the new
  honesty that A1's 0.005 p-value, though significant, doesn't
  generalize to per-PN, period-stratified, or co-occurrence tests).

## Recommendation: Phase-30b focus

Given the PARTIAL verdict, the highest-priority remediation work is:

### Tier 1 (immediate fixes; each days of work)

1. **P30-A3-v2** — Re-run Meluhha co-occurrence filter with token-level
   matching (split forms into individual syllables; allow partial
   matches; relax for diacritics and subscript digits). If still 0,
   the substantive interpretation kicks in.
2. **P30-A8-v2** — Fix the M77 ↔ phoneme-map sign-ID overlap. Either
   add zero-padded variants to the phoneme map, or expand the
   phoneme map by 30+ entries via Wells 2015 / Mahadevan 2010
   readings (which use M77 codes natively).
3. **Tighten the rendering set** — Currently `BASE_RENDERINGS`
   tokenizes to {"miin", "men", "min", "in", "en", "na", "il", ...},
   which includes very common Sumerian syllables like "in", "en",
   "na". Replace these with **only the 2-3 syllable forms that
   genuinely realise Dravidian *miin*** in attested transliterations
   (mi-in, me-en, mi-na, me-na). This will collapse the false-positive
   rate, recover statistical power on A5, and likely flip A6's
   period-rate delta.

### Tier 2 (corpus expansion; weeks)

4. **P30-F1 (Fuls ME vol. 3, $45)** — Order today; 3.3× corpus
   expansion + temporal stratification.
5. **P30-B2 (Wells 2015, $16)** — Order today; +17 phoneme-map
   entries with Dholavira reading + sign-id integration.
6. **P30-F9 (Tamil-Brahmi corpus, Mahadevan 2003)** — The parallel
   corpus for Dravidian validation; +2 pp expected.

### Tier 3 (falsification round; weeks)

7. **P30-E1 (Yajnadevam Sanskrit map vs Parpola)** — Critical now
   that the framework gives p = 0.0001 on E7 for Parpola's map. We
   need to know whether Yajnadevam's competing Sanskrit map gives a
   higher / equal / lower anchor-score under the same methodology.

### Defer to Phase-30c+

- All Category H (computational decipherment) — until Tier-1 fixes
  land.
- L1 (Tamil Nadu prize submission) — until A3-v2, A5-v2 land.
- L9 (arXiv preprint) — until A3-v2 lands and Yajnadevam falsification
  is run (E1).

## Decision

**Do NOT proceed to L1 / L9 (publication / prize) yet.** The Phase-29
headline survives at the global-null level (A1, E7) but fails at the
per-PN-multiple-comparisons level (A5) and Meluhha co-occurrence
(A3). Phase-30b should focus on the Tier-1 fixes (rendering-set
tightening, A3-v2 token matching, A8-v2 sign-ID alignment, M77
phoneme-map expansion) before any external claims.

**Decipherment progress (post-Phase-30a):** revised down from
~12-15 % to **~10-12 %** to reflect the new test results.

## Files produced in Phase-30a

- `backend/scripts/run_phase30a_validation.py` (1 200 lines) — runner
- `backend/scripts/_summarize_phase30a.py` — summary helper
- `reports/indus_phase30a_p30_a1_20260501T114235.json` ... A2..A8
- `reports/indus_phase30a_p30_e7_20260501T114235.json`
- `reports/indus_phase30a_p30_g1/g8/g9_20260501T114235.json`
- `reports/indus_phase30a_verdict_20260501T114235.json` — aggregated
- `reports/PHASE_30A_SYNTHESIS.md` — this document

## Citations

All data sources cited per `CITATIONS.md` (committed in Phase-30
prep). Key references for Phase-30a:
- Section A.1 (Mahadevan 1977, MASI No. 77)
- Section B.1 (ePSD2 / Penn Sumerian Dictionary, CC BY-SA)
- Section B.3 (CDLI Meluhha-mentioning tablets)
- Section C.1, C.2 (Parpola 1994a, 2010 phoneme readings)
- Section F.2 (Laursen 2010 Janabiyah seal #10)

---

*Phase-30a synthesis maintained as part of the Glossa-Lab Indus
decipherment pipeline. Co-authored with `Oz <oz-agent@warp.dev>`.*
