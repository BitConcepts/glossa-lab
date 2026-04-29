# Phase-18 — State of decipherment + roadmap to Indus
This report consolidates everything Phase-15 → Phase-18 has measured, identifies
the structural signal we now have on M77, ranks the live decipherment hypotheses
against that signal, and lists the next-step experiments by expected value.

## 1. What we have right now

Corpus inventory (post Phase-18 acquisitions):

| Corpus | Tokens | Types | Source | Phase added |
|---|---:|---:|---|---|
| Indus M77 | 5,361 | 64 | Mahadevan 1977 (rank-corr-mapped) | pre-existing |
| CISI mayig (subset) | 1,003 | 182 | mcskware digitization of Parpola CISI Mohenjo-daro M-1..M-200 | **18** |
| CDLI Sumerian Ur III | 3,468,699 | 109,948 | CDLI bulk ATF | 16 |
| CDLI Sumerian OB-lit | 425,147 | 90,024 | CDLI bulk ATF | 16 |
| CDLI Akkadian OB | 397,977 | 77,524 | CDLI bulk ATF | 16 |
| CDLI Akkadian NA | 486,011 | 76,964 | CDLI bulk ATF | 16 |
| Kee2u Tamil morphemes | 17,414 | 1,924 | Kee2u Indus_Decipherment | 16 |
| Kalyanaraman Devanagari | 98,707 | 49,140 | zanodor/CORPUS_INDEX BoW | 16 |
| DAMOS Linear B | 44,850 | 8,507 | https://damos.hf.uio.no scrape | 17 |
| **RV padapatha** (running Sanskrit) | **163,172** | **27,152** | **Hellwig 2018 morpho-lexical** | **18** |
| Ferrara 2006 PhD (Cypro-Minoan) | catalog | 96 (Olivier) / 57-70 (Valério) | UCL Discovery PDF (478 MB) | 18 |

Plus reference works: DEDR OCR, Mahadevan 2003 Tamil-Brahmi, CHIC, Linear B Tselentis,
Tselentis Linear B Lexicon, Everson N5135 Cypro-Minoan, Project Madurai HTML, Kee2u
Indus repo, zanodor CORPUS_INDEX.

## 2. The M77 structural fingerprint, fully measured

```
zipf_alpha          0.978   |   power-law unigram distribution close to natural language
zipf_r2             0.662   |   *low* fit-quality on Zipf (only 64 distinct types -- small-sample)
mi_gamma            0.098   |   weak long-range MI decay
mi_r2_pow           0.978   |   power-law MI fit is excellent
epistatic_2nd_norm  0.597   |   ~60% of pairwise info beyond independence
epistatic_3rd_norm  0.422   |   ~42% of triple-wise info beyond pairwise *unusually high*
h1_norm             0.897   |   ~90% of theoretical max H1 (small alphabet, well-spread)
h1_nats             3.732   |   raw unigram entropy
```

## 3. M77 vs. all reference corpora (Phase-18 measurement)

```
                     zipf_a  zipf_r2  mi_gam  mi_r2  eps2   eps3   h1n
indus_m77            0.978   0.662    0.098   0.978  0.597  0.422  0.897
cisi_mayig (M001-M200)  1.098 0.937    0.039   0.798  0.562  0.239  0.837
rv_padapatha (RV)    1.018   0.935    0.018   0.913  0.633  0.312  0.825
kee2u_tamil          1.175   0.974    0.092   0.750  0.569  0.282  0.775
cdli_sumerian_ur3    1.098   0.920    0.141   0.926  0.510  0.256  0.567
cdli_sumerian_ob_lit 0.821   0.923    0.026   0.912  0.726  0.510  0.783
cdli_akkadian_ob     0.794   0.895    0.052   0.921  0.658  0.399  0.739
cdli_akkadian_na     0.961   0.953    0.038   0.922  0.732  0.531  0.771
damos_linear_b       0.822   0.894    0.049   0.838  0.596  0.340  0.716
kalyanaraman_vedic   0.585   0.902    0.010   0.972  0.902  0.819  0.936
```

**What the numbers say**, signal by signal:

* **`zipf_alpha`** — M77 at 0.978 is closest to **RV padapatha (1.018)** and **CISI mayig (1.098)**.
  Akkadian-NA at 0.961 is also close. Tamil is higher (1.175). Kalyanaraman BoW is far away (0.585).
* **`mi_gamma`** — M77 at 0.098 is closest to **Kee2u Tamil (0.092)** and Sumerian Ur III (0.141).
  Running Sanskrit decays slower (0.018). This is the **only DoF where Tamil is the closest match**.
* **`epistatic_2nd_norm`** — M77 at 0.597 is in the middle of the pack; closest matches are **DAMOS Linear B (0.596)**, Akkadian OB (0.658), Kee2u Tamil (0.569).
* **`epistatic_3rd_norm`** — M77 at 0.422 is **higher than every comparator language** except Akkadian-NA (0.531) and Sumerian-OB-lit (0.510). All Aryan/Dravidian/Linear B sit at 0.24–0.34. **This is a real signal: M77 has more 3-way correlations than running prose.** Likely indicator of formulaic/templated content rather than free language.
* **`h1_norm`** — M77 at 0.897 is the second-highest in the table (only Kalyanaraman BoW is higher).
  Closest comparator: CISI mayig (0.837). This reflects M77's tiny alphabet (V=64): with so few signs, even a slightly uneven distribution still uses the inventory efficiently.

## 4. Multi-hypothesis ranking on M77 (Phase-18, post-IA-update)

After updating `indo_aryan_morphology.yaml` with the genuine RV padapatha measurement
(replacing the Kalyanaraman-BoW-only basis), all four serious hypotheses tie on
constraint-violation but rank differently on derived score:

```
rank  hypothesis                   max_violation  n_violated  score
 1    dravidian_morphology         0.1882         2           1.7829
 2    indo_aryan_morphology        0.1882         1           1.6389
 3    sumerian_morphology          0.1882         2           1.5644
 4    akkadian_morphology          0.1882         2           1.5369
 5    vedic_kalyanaraman_morph.    0.2776         5           1.3647   (rejected)
```

* All four serious hypotheses fail by the **same** amount: M77 sits 0.19 outside every
  language manifold on at least one bound.
* **Indo-Aryan** has the fewest individual violations (1) but a slightly lower derived
  score than Dravidian. The single Indo-Aryan violation comes from `epistatic_3rd_norm`
  being above the new RV-padapatha-anchored ceiling (0.55) — the same DoF that M77
  exceeds against every other comparator.
* **Dravidian** has the highest score because the Dravidian YAML weights
  `epistatic_3rd_norm` strongly and M77's high value pushes the score upward — even
  though M77 is outside the Dravidian bounds on 2 constraints.
* **Vedic-Kalyanaraman** is decisively rejected (0.28 max_violation, 5 violations).
  The Kalyanaraman BoW Devanagari fingerprint is **not** what M77 looks like. This
  rules out Kalyanaraman's specific decipherment proposal as a structural-signature match.

## 5. What this tells us, and what it doesn't

**It tells us:**
1. M77 is structurally **inside the natural-language envelope** (zipf_alpha ~ 1, strong
   Zipf/MI fits, epistasis profile in the same order of magnitude as Sumerian/Akkadian/RV).
2. M77 is **not** Kalyanaraman-style BoW Indo-Aryan vocabulary — categorically rejected.
3. The structural signal is **weakly Dravidian-leaning** (Tamil's mi_gamma is the best
   match for M77's mi_gamma) but **only weakly**: with the YAML constraints honestly
   anchored to measured values, M77 violates every hypothesis by the same margin.
4. M77's high `epistatic_3rd_norm` is a **genuine outlier signal**. None of our running
   reference languages (Tamil Kee2u, RV padapatha, DAMOS Linear B) reach 0.42; only
   the Akkadian/Sumerian admin streams come close. This is consistent with M77 being
   **formulaic** (seals, short recurring sequences) rather than free prose.

**It does NOT tell us:**
1. **Which language family.** The four-way near-tie at max_violation=0.19 is not
   resolvable with the 8 DoFs alone. We need additional structural channels.
2. **Whether M77 is a fully phonographic script or part-logographic.** All our
   reference corpora are mixed (Sumerian Ur III is heavily logographic; RV padapatha
   is fully phonographic). M77 sits in between but doesn't clearly favor either.
3. **The phonetic identity of any sign.** The 8-DoF projection is structural-only.

## 6. Roadmap: what to do next, ranked by expected value

### Tier 1 — high-leverage analytical work (no new corpora needed)

**A. Joint sign-clustering across M77 + CISI-mayig + Ferrara 2006 catalog.**
Apply the Phase-16 Daggumati allograph detector (`sign_clusters.py`) to all three
Indus-script datasets in a common feature space. The 179-inscription mayig CISI
(1003 signs, 182 distinct types) is too small alone but is critical because it uses
**Parpola-numbered signs** which can be cross-walked with the Mahadevan rank-corr 64
in M77. This would give us:
  - Independent confirmation/rejection of the M77→Parpola sign-id crosswalk
  - A unified Indus sign-cluster that aggregates positional evidence across the two
    largest digital Indus corpora.
ETA: ~1 day.

**B. Re-run M77 multi-hypothesis ranker with `epistatic_3rd_norm` as an excluded DoF
or down-weighted.** Since M77's high eps3 is the single biggest tie-breaker against
every hypothesis, removing it (or weighting it lower) tells us whether the 4-way tie
holds on the *other* 7 DoFs alone. If Indo-Aryan or Dravidian wins decisively on
the 7-DoF projection, that's the strongest signal we can extract from current data.
ETA: 30 min.

**C. Replace M77's rank-corr-mapped 64-sign alphabet with raw Mahadevan 3-digit codes
(no merging) and re-measure all 8 DoFs.** The current M77 mapping merges signs aggressively
(64 distinct from ~417 raw); this is what's causing M77's V=64 vs CISI mayig's V=182.
Measuring on the unmerged codes will reset the alphabet-size scale and probably
flip several DoF comparisons (h1_norm in particular).
ETA: 1–2 days (need to revisit the rank-corr pipeline).

**D. Build the Cypro-Minoan typological-control CAS-YAML.** Per Phase-17, we have
Valério's 57–70-sign inventory and the Eteocypriot grammatical hint. Add CM as a
6th competing hypothesis to test whether **any small-inventory undeciphered
script** projects through the M77 manifold differently than the four mainstream
language families. CM has only 4,000 signs across 250 inscriptions, but Ferrara's
2006 PhD thesis (478 MB PDF, just acquired) contains the full catalog with signs;
extracting transliterations is OCR-able.
ETA: 2–3 days (heavy OCR work on the 478 MB PDF).

**E. Implement the epistatic-anchor seed for M77.** The high `epistatic_3rd_norm`
suggests there are stable 3-sign motifs in M77 that are ripe for anchor-pin tests.
Identify the top-K most epistatically-coupled triples in M77 and check whether they
correlate with archaeological metadata (provenience, object type, period) in the
Mukhopadhyay 2023 patterned-text dataset. ETA: 1 day.

### Tier 2 — corpus expansion (needs human acquisition)

**F. Wells 2015** (*Epigraphic Approaches to Indus Writing*) — paid book, ~$60.
This is the **single most valuable remaining acquisition** for Indus-specific work.
Wells's 676-sign inventory + Fuls's positional-analysis appendices give us the right
structural framework to compare against our rank-corr 64. Without Wells we are
working with a sign list that's 10× smaller than what serious Indus epigraphers use.

**G. Parpola CISI Vols 1, 2, 3.1, 3.2, 3.3** — the canonical seal corpus. We have
the mcskware partial digitization (~179/4537 inscriptions); the rest is locked in
print. Vol 3.1 (Mohenjo-daro/Harappa) and 3.2 (excavation sites) are searchable on
academia.edu but blocked behind login (we got 137 KB HTML wrappers, not PDFs).
Buying or library-ILL one volume at a time is the sustainable path.

**H. ICIT (Fuls-Wells)** — request access from Andreas Fuls
(`andreas.fuls@tu-berlin.de`). We have Fuls's 21-page documentation PDF describing
the database structure (sign list, frequencies, position histograms) and his
2022/2023 books (Corpus + Catalog) are buyable. The online ICIT corpus (4537
inscriptions, 5509 texts, 19616 sign occurrences) is the single largest digital
Indus dataset; getting access would supersede mayig's 179-inscription subset.

**I. Ferrara/HoChyMin** — currently blocked at $185 hardcover for Vol II (Corpus).
The 478 MB Ferrara 2006 thesis we just acquired contains essentially the same
catalog material, slightly older but free. **Ferrara 2006 is enough to enable
Cypro-Minoan as a typological control without buying HoChyMin.**

### Tier 3 — methodological extensions

**J. Sentence-level/inscription-level DoFs.** All our current measurements concatenate
inscriptions into one stream. Computing DoFs per-inscription and aggregating with
mean ± stdev would reveal heterogeneity within M77 (admin seals vs. complex texts
vs. miniature ration tokens per Mukhopadhyay 2018).

**K. Genre-stratified Sumerian/Akkadian baselines.** CDLI Ur III is dominated by
short admin texts. Re-measure DoFs separately for admin / lit / lex / royal-inscription
genre filters (the catalog has these). The current "Sumerian" baseline is really
"Sumerian admin-dominated"; what M77 should be compared against is whatever genre is
typologically closest, not raw cuneiform.

**L. Daggumati-Revesz 2021 epigraphic spectral analysis.** They derive a "language
fingerprint" from the eigenstructure of the n-gram transition matrix. Implement and
run on all 10 corpora plus M77. This would give us a *continuous* similarity score
between M77 and each comparator, instead of the discrete in-manifold/out-of-manifold
projection we currently use.

## 7. Updated remaining-gaps (post-Phase-18)

✅ Acquired this round: RV padapatha (Hellwig), VedaWeb morphology (Zenodo + GitHub),
Ferrara 2006 PhD thesis (UCL), mayig CISI JSON, Fuls ICIT documentation, Parpola CISI
metadata.

❌ Still gated:
* Wells 2015 — paid book.
* Parpola CISI Vols (full) — paid set, ~$200 each volume.
* ICIT online database — email Fuls.
* Ferrara 2012/2013 HoChyMin (final published version) — paid.
  Mostly redundant with Ferrara 2006 PhD thesis though.

## Citations

* Aurora 2015 — DAMOS, Procedia Soc Behav Sci 198:21-31.
* Daggumati & Revesz 2021 — A method of identifying allographs in undeciphered scripts and its application to the Indus Valley Script. HSS Communications.
* Everson 2020 — N5135 = L2/20-154, ISO/IEC JTC1/SC2/WG2.
* Ferrara 2006 — An interdisciplinary approach to the Cypro-Minoan script. PhD thesis, UCL.
* Hellwig, Hettrich, Modi, Pinkal 2018 — Multi-layer Annotation of the Rigveda. LREC.
* Mukhopadhyay 2018 — arxiv 1812.00049 (Indus ration tokens).
* Mukhopadhyay 2023 — Semantic scope of Indus inscriptions, HSS Communications.
* Parpola, Pande, Koskikallio (eds) — Corpus of Indus Seals and Inscriptions Vols 1, 2, 3.1, 3.2, 3.3.
* Valério 2016 — Investigating the Signs and Sounds of Cypro-Minoan, PhD thesis, Univ. Barcelona.
* Wells 2015 — Epigraphic Approaches to Indus Writing. Archaeopress.
* Wells, Fuls — ICIT (Interactive Corpus of Indus Texts), epigraphica.de.
