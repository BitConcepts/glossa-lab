# CLAIM_AUDIT.md — Evidence Tier Mapping and Risk Assessment

**Tiers:**
- **Tier 1**: Strong structural claims — state confidently if data-backed
- **Tier 2**: Probable linguistic interpretation — framed as supported, not proven
- **Tier 3**: Speculative or provisional — require explicit caveats

---

## Major Claim Audit

| Claim | Tier | Current Strength in v1 | Evidence | Risk | Revised Wording |
|---|---|---|---|---|---|
| Non-random positional structure (INITIAL/MEDIAL/TERMINAL) | T1 | OVERSTATED as "confirms" | Permutation null z=10.3, p≈0; held-out 97.7% accuracy; 10/10 Mahadevan papers; Phase-134 F1/F7 | Low | "We find robust positional structure inconsistent with random sign ordering (permutation null z=10.3, p<0.001; held-out accuracy 97.7%)" |
| Recurring 3-slot inscription structure | T1 | Stated as grammar model — appropriate | 97 formula types identified; dominant backbone M342·M176 PMI=2.43; bi-channel (text+icon) co-selection | Low | "We identify a recurring [CLASSIFIER]–[TITLE]–[SUFFIX] three-slot structure across ≥97 formula types" |
| Fish sign (M047) exclusively compound across all 9 sites | T1 | "Definitively compound" — slightly overclaims | 0/113 isolated in Holdat; 0/27 Gulf contexts (Laursen 2010); Parpola 1994 appendix confirms compound-only attestation | Low | "Under formal testing, no isolated fish signs appear in the 1,670-seal corpus or Gulf deposit catalog (0/113+27)" |
| M267 is not the fish sign | T1 | Stated correctly | M267 frequency=400 across all motif types; M047 = P47 per crosswalk; M267 motif-independence χ²=12.98 p=0.11 | Low | RETAIN — clear, data-backed correction with historical explanation |
| M267 = genitive particle | T2 | "MEDIUM reading iN/in" — correctly qualified | Consistent pre-title distribution; grammar test z=8.04; 6,869 Parpola genitive refs; χ² motif-independence | Medium | "M267 is assigned a MEDIUM-confidence genitive-particle reading (iN/in) on the basis of distributional and grammatical evidence; definitive phonetic value requires external validation" |
| Proto-Dravidian is the best-fit language family | T2 | "Confirms the Dravidian phonetic hypothesis" — overclaims | Dravidian LM lift ratio 1.85× over Sanskrit; 88% of H+M readings Dravidian-favoured; Parpola 94 59% cross-validation; Wells 2015 independent confirmation | Medium-high (no direct alternative-language SA reported) | "The evidence favours a Proto-Dravidian reading framework under the tested assumptions; no equivalent Munda, Sanskrit, or Elamo-Dravidian alternative has been constructed to the same resolution" |
| Individual HIGH-confidence anchor readings (e.g. M045=yānai, M062=erutu) | T2 | "HIGH confidence" — appropriate with stated criteria | Iconographic match + distributional exclusivity (lift>5.0) + cross-source agreement; Parpola 1994 59% confirmation | Low | "HIGH-confidence readings satisfy two independent evidence criteria and show 59% overlap with Parpola (1994)" |
| MEDIUM readings (86 signs) are phonetically grounded | T2 | Mixed — some well-grounded, some weaker | DEDR rebus + SA-consistency ≥0.15 + positional profile | Medium | "MEDIUM readings satisfy one strong evidence criterion each; individual DEDR citations are listed but do not constitute final phonetic assignments" |
| PROVISIONAL_MEDIUM sibilants (M330, M165, M202, M198) | T3 | "Exploratory — require expert review" — correctly stated | Phase-163 text proximity (4× Parpola/Mahadevan refs each); Phase-166 DEDR cross-validation CONFIRMED/PROVISIONAL | Medium | "Four sibilant signs are promoted to PROVISIONAL_MEDIUM status pending expert peer review; they should not be included in coverage calculations without qualification" |
| 90.96% token coverage | T1 (structural count) | Correctly stated as "genuine H+M" | 6,363/7,002 tokens assigned to genuine H+M signs (Phase-133 corrected) | Low — but only valid for genuine H+M; do not quote as "decipherment coverage" | "90.96% of corpus tokens are assigned to signs with at least one HIGH or MEDIUM-confidence candidate reading" |
| 69.8% seals fully covered | T1 (structural count) | Correctly stated with qualification | 1,165/1,670 seals contain only H+M signs (Phase-133 genuine count) | Low | "69.8% of seals consist entirely of signs with candidate H+M readings; this does not imply phonetic certainty for those seals" |
| Guild-identity administrative seal system | T3 | Stated as interpretation — needs tier marker | Consistent with 3-slot grammar; semantic clustering (26.7% ANIMAL_GUILD); Arthaśāstra parallel | High — speculative | "Under the proposed grammar model, inscription structure is consistent with an administrative seal encoding system; the guild-identity interpretation is one plausible semantic frame among others" |
| Munda substrate readings (M374=kul, M351=vī) | T3 | Stated as MEDIUM with substrate notation | SA modal + DEDR/Munda near-cognate + MEDIAL positional | High | "Two signs are assigned MEDIUM readings with a substrate hypothesis; these are explicitly speculative and lack independent phonological confirmation" |
| Arthaśāstra administrative continuity | T3 | Used illustratively — needs caveat | Martini 2025 administrative terminology parallel | High — ~2,000-year gap, no epigraphic bridge | "The Arthaśāstra parallel is illustrative of possible administrative continuity; it does not constitute evidence for the reading model" |
| Full decoding / "the seals say" | T3 | OVERCLAIMS — "full decoding" implies completeness | Each seal's reading depends on H+M candidate readings, which are not definitively phonetic values | Very high | Replace "fully decoded" with "fully covered by H+M candidate readings"; replace "what the seals say" with "proposed readings under the model" |
| "The script is decipherable" | T1 (structural) / T3 (phonetic) | Structural: defensible; phonetic: overclaims | Non-random structure, consistent grammar, DEDR rebus compatibility | High if read as phonetic finality | "The corpus shows structural and distributional properties consistent with a decipherable linguistic system; phonetic assignment requires external validation" |
| "Confirms the Dravidian phonetic hypothesis" | T2 | OVERCLAIMS | Multiple supporting tests but no external phonetic confirmation | High | "Supports the Dravidian phonetic hypothesis under the tested computational assumptions" |
| 59/59 foundation checks pass | T1 | Correct — internal consistency | foundation_check.py automated checks | Low | RETAIN — clearly labeled as internal consistency checks, not external validation |
| Nair 2026 as "independent replication" | T1 (structural) / T2 (phonetic) | Structural replication only | Nair confirms non-random structure on ICIT corpus independently | Medium — Nair does not validate phonetic readings | "Nair (2026) independently replicates key structural properties on a separate ICIT corpus, supporting the linguistic interpretation of the corpus" |

---

## Language Replacements (v1 → v2)

| v1 Phrase | v2 Phrase | Section |
|---|---|---|
| "computational decipherment" | "computational decipherment hypothesis" or "computational grammar and candidate anchor model" | Title, Abstract, throughout |
| "the script is decipherable" | "the corpus shows structure consistent with a decipherable linguistic system" | §5 Conclusion |
| "the underlying language is proto-Dravidian" | "the evidence favours a Proto-Dravidian reading framework under the tested assumptions" | §5 |
| "confirms the Dravidian phonetic hypothesis" | "supports the Dravidian phonetic hypothesis under the tested assumptions" | Abstract, §5 |
| "full decoding" / "fully decoded" | "fully covered by current H+M candidate readings" | §3.6, §5, Abstract |
| "what the seals say" | "proposed readings under the model" | §4.1 |
| "most comprehensive decipherment" | "largest candidate anchor table known to the author" | §5 |
| "definitively compound" | "consistently compound across all tested contexts" | §3.5 |
| "foundation validation confirms" | "internal validation checks pass" | Abstract, Appendix C |
| "beyond reasonable doubt" | (remove) | §3.10 |
| "we deciphered" | "we propose candidate readings for" | Throughout |
